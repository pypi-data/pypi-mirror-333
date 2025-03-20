# TransferAttacks

## Overview
TransferAttacks is a PyTorch library for implementing adversarial attacks with improved transferability. It includes state-of-the-art methods categorized into different approaches:

- **Gradient-based**: Modify gradients for enhanced transferability.
- **Ensemble-based**: Use multiple models to improve attack success.
- **Generation-based**: Train generative models to craft adversarial examples.

## Installation
```sh
pip install transferattacks
```

## Supported Attacks

### Gradient-based Methods
- **[BPA](https://arxiv.org/abs/2306.12685)**: Recovers truncated gradients in non-linear layers.
- **[AGS](https://ojs.aaai.org/index.php/AAAI/article/view/28365)**: Uses adversary-centric contrastive learning.
- **[MetaSSA](https://arxiv.org//abs/2405.03193)**: Utilizes low-frequency feature mixing.
- **[VDC](https://ojs.aaai.org/index.php/AAAI/article/view/28541)**: Adds virtual dense connections for dense gradient backpropagation.
- **[MA](https://arxiv.org/abs/2311.18495)**: Minimizes KL divergence between models.

### Ensemble-based Methods
- **[Ens](https://arxiv.org/abs/1611.02770)**: Generates adversarial examples using multiple models.
- **[Ghost](https://arxiv.org/abs/1812.03413)**: Uses dropout and random scaling to create ghost networks.
- **[SVRE](https://arxiv.org/pdf/2111.10752)**: Uses variance-reduced gradients.
- **[LGV](https://arxiv.org/abs/2207.13129)**: Ensembles multiple weight sets.
- **[MBA](https://arxiv.org/abs/2302.05086)**: Maximizes average prediction loss using Bayesian optimization.
- **[AdaEA](https://arxiv.org/abs/2308.02897)**: Adjusts surrogate model weights dynamically.
- **[CWA](https://arxiv.org/abs/2303.09105)**: Exploits common weaknesses in an ensemble.
- **[SMER](https://openaccess.thecvf.com/content/CVPR2024/papers/Tang_Ensemble_Diversity_Facilitates_Adversarial_Transferability_CVPR_2024_paper.pdf)**: Uses reinforcement learning for weight refinement.

### Generation-based Methods
- **[CDTP](https://arxiv.org/abs/1905.11736)**: Learns domain-invariant perturbations.
- **[LTP](https://proceedings.neurips.cc/paper/2021/hash/7486cef2522ee03547cfb970a404a874-Abstract.html)**: Uses mid-level features for perturbation generation.
- **[ADA](https://arxiv.org/abs/2208.05650)**: Stochastically perturbs shared salient features.
- **[GE-ADVGAN](https://arxiv.org/pdf/2401.06031)**: Enhances adversarial transferability via gradient editing.

## Usage
```python
from transferattacks import FGSM
attack = FGSM(model, epsilon=0.03)
adv_images = attack.generate(images, labels)
```

## Citation
If you use TransferAttacks in your research, please cite the corresponding papers.

## License
MIT License
