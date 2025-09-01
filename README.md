# LELA71000: On How Transformers Recognise Quantifier Depth in First-Order Logic

This repository contains the full implementation of dataset generation and experimental scripts used in the dissertation. It provides synthetic datasets for First-Order Logic (FOL) and FOL-to-Natural-Sentence (FOL2NS) tasks, and related interpreted algorithms in RASP, alongside training-ready data for Transformer models and attention-related data for visualisations.

---

## Repository Structure

### Dataset_constructions
Contains the complete code used to **generate the synthetic datasets** described in the dissertation.  
- Includes scripts for producing **5 FOL datasets** and **2 FOL2NS datasets**.  
- The subdirectory `build_datasets/` provides the detailed build scripts (originally written in VS Code).  
- The `datasets/` subdirectory contains the **finalised datasets** with balanced statistical distributions, which are the datasets later used to train models in our experiments (e.g. "Type1_M" and other files named in the same format). Among those dataset files, Type1 represents Standard-1, Type2 represents Standard-2, Type3 represents Standard-3, Type4 represents Nested-1, and FOL2NS are related to both mathematical formulas and English mappings in Nested-2.

### RASP
Implements algorithms in **Restricted Access Sequence Processing (RASP)** to recognise **Quantifier Depth (QD)** in the first four types of FOL datasets.  
- Two scripts are provided:  
  - `QD_in_FOL.ipynb`: without BOS token.  
  - `QD_in_FOL_with_BOS.ipynb`: with BOS token.  

RASP is a domain-specific language introduced in *Thinking Like Transformers* (Weiss et al., 2021), designed to approximate the self-attention mechanism in the Transformer model.  

**Note:** Since the Jupyter kernel used for RASP is an **external tool** (not included as a dependency here), you will need to install it separately to execute the RASP notebooks. You can refer to the RASP-based Jupyter environment provided in [macleginn/rasp-jupyter](https://github.com/macleginn/rasp-jupyter).

### BERT and Small_Transformers
These directories contain the code and configurations for model training and evaluation, using both pre-trained BERT and smaller Transformer architectures.  

---

## Requirements

Most scripts are primarily running experiments in **Jupyter notebooks**. Only the scripts for data constructions are managed via `uv` environment files (`pyproject.toml`, `uv.lock`).

---
## Small\_Transformers

This directory contains the **main experimental scripts** for training and analysing small-sized Transformer models on the generated datasets. It is divided into two subdirectories:

### FOL
This folder contains the **main experiments of the dissertation**.  
- All required datasets for training the models are included here.  
- The experiments are designed to be run in **Jupyter notebooks**.  

Key scripts:  
- **`explain_nn_model.ipynb`**  
  The central script of this project, which allows you to reproduce the main results by training small-sized Transformers on the FOL datasets.  
  - Evaluates small-sized Transformers with different configurations:  
    - Number of layers  
    - Number of attention heads  
    - Two pooling strategies  
    - Different hidden sizes
    - **Hyperparameters** such as `d_model`, number of layers (`n_layers`), and number of attention heads (`n_heads`) can be modified directly in the parameter setting cells. For example:  
  ```python
  d_model = 256
  n_layers = 2
  n_heads = 2
  ```
    - Training is executed via the following line, which runs the main training loop with the selected configuration:
```python
  all_preds1_1, topk_probs1_1, valid_accuracies1_1, valid_macroF1s1_1, valid_perF1s1_1 = main(
    train_data1, valid_data1, epoch, float("-inf"), early_stop, topk, with_mask=True)
```
  - Extracts and stores internal representations, including:  
    - Attention weights  
    - QK score logits (pre-softmax logits)  
    - Value vectors  
  - Saves the extracted data into JSON files (e.g. "valid_type1" and other files named in the same format) for each FOL type, to be later visualised as heatmaps.  

- **`Extract_info.ipynb`**  
  A companion script that processes the extracted attention-related information for **visualisation**.  
  - Uses the saved JSON datasets from the previous step.  
  - Generates plots and heatmaps for deeper inspection of model behaviour.  
  - Also requires running in **Jupyter notebooks**.  

### FOL2NS
This folder contains experiments on the **FOL2NS datasets**, extending the same experimental pipeline to a slightly different formal representation.  
- Similar to `FOL/`, it provides training and evaluation scripts as well as data extraction routines.  

---
### FOL2NS (within Small_Transformers)
This folder contains experiments evaluating a **2-layer, 2-head (2L2H) Transformer** on the **FOL2NS datasets**.  
- **`Small_Transformer_on_FOL2NS.ipynb`**  
  - Mainly trains and evaluates a 2L2H Transformer on the two FOL2NS dataset types.
  - Different configurations can be explored by changing the corresponding hyperparameters in the scripts.  
- **`FOL2NS.json`**  
  - The dataset used for these experiments.  

---

## BERT

The `BERT/` directory contains experiments using **pre-trained BERT models** to recognise QD in the **FOL2NS datasets**.  

- **`BERT_QD.ipynb`**  
  - Trains BERT on the FOL2NS dataset.  
  - Provides the BERT model to compare against the small Transformer architectures used in this project.  
- **`FOL2NS.json`**  
  - The dataset used in BERT-based experiments.  
---


