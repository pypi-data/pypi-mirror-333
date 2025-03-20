# WaLSAtools

**WaLSAtools** is an open-source library for advanced wave analysis in time series and imaging data. It provides a suite of spectral and spatio-temporal analysis techniques, including:

- **Fast Fourier Transform (FFT)**
- **Wavelet Analysis**
- **Lomb-Scargle Periodogram**
- **Welch Power Spectral Density**
- **Empirical Mode Decomposition (EMD)**
- **Hilbert and Hilbert-Huang Transforms**
- **k-omega Analysis**
- **Proper Orthogonal Decomposition (POD)**
- **Cross-Spectra Analysis**

WaLSAtools features an **interactive interface** available in both **terminal** and **Jupyter notebooks**, enabling an intuitive workflow for wave analysis.  
For detailed installation instructions, method descriptions, and usage examples, visit the **[WaLSAtools Documentation](https://WaLSA.tools/).**

---

## 🚀 **Installation**

### **1️⃣ Install via PyPI**
The easiest way to install WaLSAtools is via **PyPI**:
```bash
pip install WaLSAtools
```

### **2️⃣ Install from Source (GitHub)**
If you prefer the latest development version:
```bash
git clone https://github.com/WaLSAteam/WaLSAtools.git
cd WaLSAtools/codes/python/
pip install .
```
Alternatively, use:
```bash
python setup.py install
```


### **🖥️ Interactive Usage**

WaLSAtools includes an interactive interface to simplify usage. After installation, launch the interactive interface in a Python terminal or (ideally) a Jupyter notebook:

```python
from WaLSAtools import WaLSAtools
WaLSAtools
```

This will launch an interactive menu with options for:

- Selecting a category of analysis.
- Choosing the data type (e.g., 1D time series or 3D data cube).
- Picking an analysis method (e.g., FFT, wavelet, k-omega).

The interface provides instructions and hints on calling sequences and parameter details for your chosen analysis.

---

## **📜 License**

WaLSAtools is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

If you use WaLSAtools in your research, please cite:

**Jafarzadeh, S., Jess, D. B., Stangalini, M. et al. 2025, Nature Reviews Methods Primers, in press.**

---

## **🛠️ Contributing**

Contributions, suggestions, and feedback are always welcome! If you encounter any issues or have ideas for improvements, please visit the **[GitHub repository](https://github.com/WaLSAteam/WaLSAtools)** to open an issue or contribute.

