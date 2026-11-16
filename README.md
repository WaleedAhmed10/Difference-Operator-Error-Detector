# Difference Operator Error Detector

A Python-based numerical analysis project designed to compute finite difference operators, construct difference tables, and detect, isolate, and correct localized errors in tabulated data using forward and backward difference methods.

## Overview

In numerical analysis, finite difference operators (such as forward $\Delta$, backward $\nabla$, and central $\delta$ differences) are fundamental tools for polynomial interpolation and numerical differentiation. A key property of difference tables is that a single isolated error in a dataset propagates predictably across subsequent difference columns in a fan-like (binomial coefficient) pattern, making it possible to locate and correct the exact erroneous entry.

This repository contains Python implementations developed across lab exercises (`Lab 3` and `Lab 4`) to demonstrate finite difference calculations and automated/semi-automated error detection in tabulated functions.

## Repository Structure

```text
Difference-Operator-Error-Detector/
├── Lab 3 Q.1 & Q.2.py    # Implementation of basic difference operators and difference table generation
├── Lab 4.py              # Error detection and correction algorithms using higher-order differences
├── LICENSE               # Project license
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## Features

* **Difference Table Generation:** Computes forward ($\Delta^n y_i$) and backward ($\nabla^n y_i$) difference tables for equally spaced data points.
* **Error Propagation Analysis:** Tracks how an error $\epsilon$ at index $k$ expands across higher-order difference columns according to binomial coefficients $\binom{n}{r}(-1)^r \epsilon$.
* **Anomaly Detection:** Identifies the exact row/index where an unexpected deviation occurs when a polynomial of degree $n$ fails to yield constant $n$-th differences.
* **Data Correction:** Estimates the magnitude of the error $\epsilon$ and restores the corrected functional value.

## Mathematical Background

For a set of equally spaced data points $(x_0, y_0), (x_1, y_1), \dots, (x_m, y_m)$ with step size $h$:

* **First Forward Difference:**
  $$\Delta y_i = y_{i+1} - y_i$$

* **Higher-Order Forward Differences:**
  $$\Delta^n y_i = \Delta^{n-1} y_{i+1} - \Delta^{n-1} y_i$$

If $y = f(x)$ is a polynomial of degree $n$, then $\Delta^n y_i$ is constant and $\Delta^{n+1} y_i = 0$. When an error $\epsilon$ is introduced at $y_k$, the $n$-th difference column exhibits alternating terms proportional to $(-1)^r \binom{n}{r} \epsilon$, centered around the affected row, allowing pinpointed error detection.

## 🚀 Getting Started

### Prerequisites

* Python 3.7 or higher
* Standard Python libraries (and `numpy` / `tabulate` if utilized in your local environment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Difference-Operator-Error-Detector.git
   cd Difference-Operator-Error-Detector
   ```

2. (Optional) Install any scientific computing dependencies:
   ```bash
   pip install numpy
   ```

### Usage

Run the individual lab scripts directly via the terminal:

```bash
# Run Lab 3 exercises (Difference Operators & Tables)
python "Lab 3 Q.1 & Q.2.py"

# Run Lab 4 script (Error Detection & Correction)
python "Lab 4.py"
```

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.
