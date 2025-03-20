# Deep Learning DNA: Surviving Architectures and Profound Principles

[![PyPI version](https://badge.fury.io/py/dldna.svg)](https://badge.fury.io/py/dldna)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

**A journey into the core technologies and key architectures of deep learning.**

This package, `dldna`, provides code and resources accompanying the book "Deep Learning DNA: Surviving Architectures and Profound Principles". It delves into the essential techniques and pivotal architectures that have shaped the field of deep learning, offering a practical, hands-on complement to the book's conceptual explanations.

**Key Features:**

*   **Code Examples:** Explore implementations of fundamental deep learning concepts and architectures.
*   **Focus on Efficiency:** Learn how to build and train models with an emphasis on computational efficiency.
*   **Accompanying Material:** This package is designed to be used alongside the book "Deep Learning DNA", providing interactive code to enhance your learning experience.

**Installation:**

*   **Minimal Installation (Recommended for Colab):**

    ```bash
    pip install dldna[colab]
    ```
    This option installs only the packages that are *not* typically pre-installed in Google Colab.

*   **Standard Installation (All Dependencies):**
    ```bash
    pip install dldna
    ```
    install_requires

*   **Full Installation (Including Optional and Development Dependencies):**

    ```bash
    pip install dldna[all]
    ```
    This installs all dependencies, including `manim` (for visualization) and development tools.


**Requirements:**

The specific requirements depend on the installation option you choose. See `setup.py` for the complete list of dependencies.  The minimal installation for Colab requires:

*   Python >= 3.7
*   transformers
*   datasets
*   tqdm
*   pillow
*   opencv-python
*   sentencepiece

**Usage:**

```python
# Example usage (replace with a simple, illustrative example)
import dldna

# ... your code here ...

print(dldna.__version__)  # Check the installed version