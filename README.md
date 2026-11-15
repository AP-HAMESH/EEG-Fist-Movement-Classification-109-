# 64-Channel EEG Bilateral Motor Execution Classification (109-Participant Cohort)

This repository contains an end-to-end machine learning pipeline for
classifying **left-fist vs. right-fist motor execution** using
64-channel EEG data from 109 participants.

The primary objective is to investigate **zero-calibration inter-subject
generalization** in Brain-Computer Interfaces (BCI). By strictly
isolating test participants from the training phase, this project
evaluates how well multi-domain EEG features (time, frequency, and
time-frequency) generalize across unseen participants, addressing
challenges such as cortical covariate shift and BCI illiteracy.

## 1. Dataset and Instrumentation

This project uses the **PhysioNet EEG Motor Movement/Imagery Dataset
(EEGMMIDB)**.

-   **Source:** [PhysioNet EEGMMIDB
    v1.0.0](https://physionet.org/content/eegmmidb/1.0.0/)
-   **Scope:** **109 participants** (`S001`–`S109`, runs `R03`, `R07`, and `R11`, totaling **4,921 trials**).
-   **Instrumentation:** 64-channel scalp EEG, originally sampled at 160
    Hz and downsampled to 128 Hz.
-   **Hardware/software environment:** Python 3.9+, MNE-Python for
    signal processing, and Scikit-learn/XGBoost for machine learning.
    CUDA acceleration is optional where supported.

## 2. Experimental Pipeline

The `IDSE109.ipynb` notebook is organized into the following execution
steps.

-   **Step 1 -- Problem Statement and Objectives:** Defines the research
    problem, measurable objectives, and zero-leakage hypothesis.
-   **Step 2 -- Environment Setup and Instrumentation:** Configures
    relative paths, creates output directories (`features/`, `plots/`,
    and `results/`), and detects available hardware capabilities
    (CUDA/CPU).
-   **Step 3 -- EEG Preprocessing and ICA Artifact Cleaning:** Applies
    zero-phase bandpass filtering (1--40 Hz). Extended Infomax ICA,
    together with ICLabel, is used to identify ocular, cardiac, and
    myogenic artifacts. Components meeting the configured rejection
    threshold (probability ≥ 0.80) are rejected before epoching from
    −2.0 s to 4.0 s.
-   **Step 4 -- Multi-Domain Feature Extraction:**
    -   **Time domain:** Hjorth parameters, Katz fractal dimension,
        zero-crossings, skewness, and kurtosis.
    -   **Frequency domain:** Welch power spectral density (PSD),
        including absolute and relative power across five standard EEG
        frequency bands.
    -   **Time-frequency domain:** Morlet wavelet power features.
-   **Step 5 -- Batch Extraction and Leak-Free Split:** Processes all
    109 participants and applies an 80/20 `GroupShuffleSplit` so that
    participants in the training cohort do not appear in the test cohort
    (87 training participants and 22 test participants).
-   **Steps 6 and 7 -- Exploratory Data Analysis (EDA):** Performs
    data-quality checks, including missing-value and class-balance
    audits, IQR-based outlier analysis, and neurophysiological
    visualizations such as contralateral alpha event-related
    desynchronization (ERD).
-   **Step 8 -- Modelling and Cross-Validation:** Evaluates Logistic
    Regression, Linear SVM, Random Forest, KNN, and XGBoost using
    five-fold `GroupKFold` cross-validation on the training
    participants.
-   **Step 9 -- Evaluation and Interpretation:** Produces confusion
    matrices, held-out test metrics, and per-subject
    generalization-error analyses to help interpret inter-subject
    performance differences and possible BCI illiteracy.

## 3. Outputs and Results

Running the pipeline generates an `outputs/experiment_109/` directory
containing the following artifacts:

-   **`features/`**
    -   `split_manifest.csv`: Records the participant-level train/test
        split for reproducibility.
    -   Feature matrices (for example, `*_train.csv` and `*_test.csv`)
        are generated locally and are excluded from Git where
        appropriate because of their size.
-   **`results/`**
    -   `master_model_comparison_109.csv`: Contains cross-validation and
        held-out test metrics, including Accuracy, Balanced Accuracy,
        and F1-score.
-   **`plots/`**
    -   High-resolution (300 DPI) visualizations of class balance, ICA
        exclusions, sensorimotor ERD distributions, and per-subject
        generalization variability.

## 4. Reproducibility Instructions

Raw `.edf` recordings and large, uncompressed feature matrices are not
tracked in this repository. Follow these steps to reproduce the
experiment locally.

### 4.1 Clone the repository

``` bash
git clone https://github.com/AP-HAMESH/EEG-Fist-Movement-Classification-109-.git
cd EEG-Fist-Movement-Classification-109-
```

### 4.2 Install dependencies

``` bash
pip install -r requirements.txt
```

### 4.3 Download the dataset

Run the included script to download the required EDF recordings from
PhysioNet:

``` bash
python download_data.py
```

The dataset download is approximately 2.5 GB; the actual download size
may vary depending on the files retrieved.

### 4.4 Run the pipeline

Launch Jupyter Notebook and execute `IDSE109.ipynb` from top to bottom:

``` bash
jupyter notebook IDSE109.ipynb
```

The notebook processes the recordings, extracts features, trains and
evaluates the models, and saves generated plots and results under the
`outputs/` directory.

## 5. Reproducibility Notes

-   Run the notebook cells in order, from the first cell to the last.
-   Keep the raw dataset in the directory expected by the path
    configuration in the notebook or update that configuration before
    running.
-   Preserve the generated split manifest so the participant-level
    train/test assignment can be inspected and reused.
-   The test cohort must remain isolated from preprocessing choices,
    feature-selection decisions, model fitting, and hyperparameter
    tuning if the experiment is intended to measure zero-calibration
    generalization to unseen participants.

## 6. Repository Structure

A typical repository layout is shown below. The exact directory names
may vary depending on the implementation.

``` text
EEG-Fist-Movement-Classification-109-/
├── IDSE109.ipynb
├── download_data.py
├── requirements.txt
├── README.md
├── data/
│   └── (downloaded EDF recordings; not tracked by Git)
└── outputs/
    └── experiment_109/
        ├── features/
        ├── plots/
        └── results/
```

## 7. Project Objective

The project investigates whether a model trained on one group of
participants can distinguish left- and right-fist motor execution in
entirely unseen participants, without participant-specific calibration.
The evaluation therefore emphasizes participant-level separation and
held-out subject performance rather than only trial-level accuracy.
