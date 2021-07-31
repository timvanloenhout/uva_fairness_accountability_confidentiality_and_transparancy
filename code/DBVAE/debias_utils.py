"""
Functions used to create a debiased dataloader.
"""
import numpy as np
import torch

def get_all_latent_means(dataloader, encoder, z_dim, device):
    """ Calculate the means of the latent spaces of all samples. """
    # create an empty matrix of size [n samples, z_dim]
    all_latent = np.zeros((len(dataloader.dataset), z_dim))

    c = 0
    for X, _ in dataloader:
        batch_size = X.shape[0]
        X = X.permute(0, 3, 1, 2).to(device)  # prepare data

        # perform forward pass
        with torch.no_grad():
            mean, _, _ = encoder(X)

        # add to matrix
        all_latent[c:c+batch_size] = mean.cpu()
        c += batch_size

    return all_latent


def get_training_sample_probabilities(all_latent, y_true, bins=10, alpha=0.01):
    """
    Given the latent space samples we calculate the sampler probabilities.
    The probabilities are only adjusted for faces. Non-faces keep an equal
    probability. The probabilities are generated by creating a histogram
    of each latent variable and oversampled when the sample holds an outlier
    in one of the latent variables.
    :param all_latent: Latent means of the samples.
    :param y_true: Labels, 1 if sample is face.
    :param bins: Number of bins to divide latent variable values in.
    :param alpha: Regularization parameter
    :return: Sample probabilities of images
    """
    all_bins_per_sample = np.zeros(all_latent.shape)
    all_histos = []

    # get indices of faces and non faces
    y_true = y_true.squeeze()
    face_idx = np.argwhere(y_true == 1).squeeze()
    non_face_idx = np.argwhere(y_true == 0).squeeze()

    # loop over each latent variable (only for faces)
    for i in range(all_latent.shape[1]):
        latent_variable = all_latent[face_idx, i]

        # get normalized histogram density
        histogram_density, bin_edges = np.histogram(latent_variable.T,
                                                    bins=bins, density=False)
        histogram_density = histogram_density / np.sum(histogram_density)
        all_histos.append((histogram_density, bin_edges.copy()))

        # Smooth density with alpha
        smoothed_density = histogram_density + alpha
        smoothed_density /= np.sum(smoothed_density)

        # Pick the correct bins for all the samples
        bin_edges[0] = -float('inf')
        bin_edges[-1] = float('inf')
        bin_ids = np.digitize(all_latent[:, i], bin_edges) - 1

        # Predict probability for each latent variable and normalize
        latent_var_prob = 1.0 / smoothed_density[bin_ids]
        latent_var_prob[non_face_idx] = 0.0
        latent_var_prob /= np.sum(latent_var_prob)

        all_bins_per_sample[:, i] = latent_var_prob

    # set the max probability for each sample as sample probability
    final_probs = np.max(all_bins_per_sample, axis=1)
    final_probs /= np.sum(final_probs)  # normalize

    # add average probability for non faces and normalize
    final_probs[non_face_idx] = 1 / non_face_idx.shape[0]
    final_probs /= 2

    return final_probs