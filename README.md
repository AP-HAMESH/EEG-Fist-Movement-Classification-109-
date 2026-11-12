# 64-Channel EEG Bilateral Fist Movement Classification (109 Participants)

## Overview
This project implements a reproducible, zero-leakage machine learning pipeline to classify **Left Fist ($T_1$)** versus **Right Fist ($T_2$)** motor execution using 64-channel scalp EEG recordings from the **PhysioNet EEG Motor Movement/Imagery Dataset** across all **109 participants** (`S001`–`S109`, runs `R03`, `R07`, and `R11`, totaling **4,921 trials**).

## Methodology & Signal Pipeline
1. **Preprocessing & Artifact Removal:**
   - Canonical `standard_1005` 64-channel montage alignment.
   - Zero-phase FIR bandpass filtering ($1.0\text{--}40.0\text{ Hz}$).
   - Automated artifact rejection using **Extended Infomax ICA** paired with **ICLabel** ($P_{\text{artifact}} \ge 0.80$) to remove ocular, cardiac, and myogenic components.
   - Resampling to $128\text{ Hz}$ and epoching from $-2.0\text{ s}$ to $+4.0\text{ s}$ (baseline-corrected on $[-2.0, 0.0]\text{ s}$; features extracted from the $[0.0, +4.0]\text{ s}$ motor execution window).
2. **Multi-Domain Feature Engineering (7 Feature Sets):**
   - **Time Domain (576 features):** Mean, Std, Variance (Hjorth Activity), Hjorth Mobility, Hjorth Complexity, Zero Crossings, Katz Fractal Dimension, Skewness, and Kurtosis.
   - **Frequency Domain (640 features):** Welch PSD absolute and relative band power across $\delta$ ($1\text{--}4\text{ Hz}$), $\theta$ ($4\text{--}8\text{ Hz}$), $\alpha$ ($8\text{--}13\text{ Hz}$), $\beta$ ($13\text{--}30\text{ Hz}$), and $\gamma$ ($30\text{--}40\text{ Hz}$).
   - **Time-Frequency Domain (640 features):** Morlet wavelet power mean and standard deviation across all 5 bands.
   - **Combined Domains:** `time_and_frequency` (1,216), `time_and_time_frequency` (1,216), `frequency_and_time_frequency` (1,280), and `combined` (1,856).
3. **Leakage-Free Cross-Subject Validation:**
   - **80/20 Participant Holdout (`GroupShuffleSplit`):** 87 training subjects (3,931 trials) and 22 completely unseen test subjects (990 trials).
   - **5-Fold `GroupKFold` CV:** Executed strictly inside the 87 training subjects with `StandardScaler` fitted independently inside each fold.

## Key Results (109 Participants)

| Rank (Inner CV) | Feature Domain | Classifier | Inner CV Accuracy ($\mu \pm \sigma$) | Held-Out Test Accuracy | Test Balanced Accuracy | Test F1-Score |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | `time_and_time_frequency` | **Linear SVM** | **$63.62\% \pm 0.67\%$** | $62.53\%$ | $62.47\%$ | $0.5963$ |
| **2** | `combined` | **Linear SVM** | $63.41\% \pm 1.35\%$ | $62.53\%$ | $62.47\%$ | $0.5945$ |
| **3** | `time_and_time_frequency` | **Logistic Regression** | $62.89\% \pm 0.75\%$ | **$64.34\%$** | **$64.30\%$** | **$0.6225$** |
| **4** | `combined` | **Logistic Regression** | $62.54\% \pm 1.28\%$ | $62.12\%$ | $62.08\%$ | $0.5989$ |
| **5** | `combined` | **XGBoost** | $62.11\% \pm 1.48\%$ | $62.32\%$ | $62.32\%$ | $0.6221$ |
| **Baseline** | All Domains | **DummyClassifier** | $50.13\%$ | $50.10\%$ | $50.00\%$ | $0.0000$ |

## How to Reproduce End-to-End
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AP-HAMESH/EEG-Fist-Movement-Classification-109.git](https://github.com/AP-HAMESH/EEG-Fist-Movement-Classification-109.git)
   cd EEG-Fist-Movement-Classification-109
