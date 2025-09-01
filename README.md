# LELA71000: On How Transformers Recognise Quantifier Depth in First-Order Logic

This repository contains the full implementation of dataset generation and experimental scripts used in the dissertation. It provides synthetic datasets for First-Order Logic (FOL) tasks, processing pipelines, and baseline implementations in RASP, alongside training-ready data for Transformer models.

---

## Repository Structure

### `Dataset_constructions/`
Contains the complete code used to **generate the synthetic datasets** described in the dissertation.  
- Includes scripts for producing **5 FOL datasets** and **2 FOL2NS datasets**.  
- The subdirectory `build_datasets/` provides the detailed build scripts (originally written in VS Code).  
- The `datasets/` subdirectory contains the **finalised datasets** with balanced statistical distributions, which are the datasets later used to train models in our experiments.  

### `RASP/`
Implements algorithms in **Restricted Access Sequence Processing (RASP)** to recognise **Quantifier Depth (QD)** in the first four types of FOL datasets.  
- Two scripts are provided:  
  - `QD_in_FOL.ipynb`: without BOS token.  
  - `QD_in_FOL_with_BOS.ipynb`: with BOS token.  

RASP is a domain-specific language introduced in *Thinking Like Transformers* (Weiss et al., 2021), designed to approximate the self-attention mechanism in the Transformer model.  

⚠️ **Note:** Since the Jupyter kernel used for RASP is an **external tool** (not included as a dependency here), you will need to install it separately to execute the RASP notebooks. You can refer to the RASP Jupyter environment provided in [macleginn/rasp-jupyter](https://github.com/macleginn/rasp-jupyter).

### `BERT/` and `Small_Transformers/`
These directories contain the code and configurations for model training and evaluation, using both pre-trained BERT and smaller Transformer architectures.  

---

## Requirements

The project dependencies are managed via both `requirements.txt` and `uv` environment files (`pyproject.toml`, `uv.lock`):

- **`requirements.txt`**:  
  Contains the essential libraries needed to reproduce experiments in Jupyter notebooks. This should specify exact versions or version ranges following the [pip requirements format](https://pip.pypa.io/en/stable/reference/requirements-file-format/).

- **`pyproject.toml` and `uv.lock`**:  
  These are automatically generated when building datasets using `uv` inside VS Code. They capture the precise dependency resolution for that environment.

If you are primarily running experiments in **Jupyter notebooks** (as in this dissertation), it is usually sufficient to install from `requirements.txt`. If you want to reproduce the dataset construction workflow in VS Code, you may instead rely on `uv` to manage dependencies.  

---
## Small\_Transformers

This directory contains the **core experimental scripts** for training and analysing small-scale Transformer models on the generated datasets. It is divided into two subdirectories:

### `FOL/`
This folder contains the **main experiments of the dissertation**.  
- All required datasets for training the models are included here.  
- The experiments are designed to be run in **Jupyter notebooks**.  

Key scripts:  
- **`explain_nn_model.ipynb`**  
  The central script of this project.  
  - Evaluates small-sized Transformers with different configurations:  
    - Number of layers  
    - Number of attention heads  
    - Two pooling strategies  
    - Different hidden sizes  
  - Extracts and stores internal representations, including:  
    - Attention weights  
    - QK score logits (pre-softmax logits)  
    - Value vectors  
  - Saves the extracted data into JSON files for each FOL type, to be later visualised (e.g., as heatmaps).  

- **`Extract_info.ipynb`**  
  A companion script that processes the extracted attention-related information for **visualisation**.  
  - Uses the saved JSON datasets from the previous step.  
  - Generates plots and heatmaps for deeper inspection of model behaviour.  
  - Also requires running in **Jupyter notebooks**.  

### `FOL2NS/`
This folder contains experiments on the **FOL2NS datasets**, extending the same experimental pipeline to a slightly different formal representation.  
- Similar to `FOL/`, it provides training and evaluation scripts as well as data extraction routines.  

---
### `FOL2NS/` (within `Small_Transformers/`)
This folder contains experiments evaluating a **2-layer, 2-head (2L2H) Transformer** on the **FOL2NS datasets**.  
- **`Small_Transformer_on_FOL2NS.ipynb`**  
  - Trains and evaluates a 2L2H Transformer on the two FOL2NS dataset types.  
  - Demonstrates how a lightweight Transformer architecture performs in comparison to larger models.  
- **`FOL2NS.json`**  
  - The dataset used for these experiments.  

---

## BERT

The `BERT/` directory contains experiments using **pre-trained BERT models** to recognise QD in the **FOL2NS datasets**.  

- **`BERT_QD.ipynb`**  
  - Trains BERT on the FOL2NS dataset.  
  - Provides a large-scale pre-trained language model baseline to compare against the small Transformer architectures used in this project.  
- **`FOL2NS.json`**  
  - The dataset used in BERT-based experiments.  

---


