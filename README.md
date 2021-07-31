# Date
01-31-2020
# Authors
Puck de Haan (pdehaan274@gmail.com) <br>
Paul ten Kaate (paultenkaate@outlook.com) <br>
Tim van Loenhout (timvanloenhout@gmail.com) <br>
Jan Erik van Woerden (janerikvw2006@gmail.com) <br>
# TA 
Simon Passenheim (simon.passenheim@googlemail.com)

# Debias VAE
This is a Pytorch implementation of the [Uncovering and Mitigating Algorithmic Bias through Learned Latent Structure ([Amini \& Soleimany et al., 2019](https://lmrt.mit.edu/publications/uncovering-and-mitigating-algorithmic-bias-through-learned-latent-structure)) paper. We ran several experiments and derived some conclusions which can be seen/read in [the report](11305150_10743367_10741577_11033711-FACT-AI-report.pdf).

## Abstract of report
> An attempt was made to reproduce the method described in ``Uncovering and Mitigating Algorithmic Bias through Learned Latent Structure'' (Amini \& Soleimany et al., 2019). Since there was no legitimate open source implementation, the method had to be implemented from scratch. The algorithm is an in-process debiasing model for computer vision, applied on a facial recognition task. Debiasing is done with the help of a debiasing VAE (DB-VAE) that learns the latent space representing the data, which is subsequently used to adaptively resample more diverse batches from the data during training. We found that the specifications provided by the authors were not enough to accurately reproduce their model. Furthermore, these settings did result in a posterior collapse of the VAE, which we solved by shifting weight from the regularization loss to the reconstruction loss. In the end, we did obtain similar debiasing results, however at the expense of a slightly less accurate classifier. Altogether, the reproducability of the main paper is deemed insufficient.