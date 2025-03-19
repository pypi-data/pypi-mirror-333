# pyescher 🎨✨  
*A Python plotting library for elegant and physics-inspired visualizations*

## 📌 Overview  
`pyescher` is a **convenient wrapper** for Matplotlib, designed to create **beautiful, publication-ready plots** with minimal effort. It includes built-in styling, marker cycling, and support for mathematical functions.

## 🚀 Installation  
Install `pyescher` using pip:  
```sh
pip install pyescher
```

## 📜 Quick Example: Bessel and Hankel Functions  
The following example demonstrates how to plot **Bessel** and **Hankel functions** using `pyescher`:

```python
import pyescher as pe
from scipy.special import jn, hankel1
import numpy as np

# Define x-values
x = np.linspace(0, 20, 1000)

# Compute function values
y1 = jn(1, x)        # Bessel function J1
y2 = hankel1(2, x)   # Hankel function H2

# Create Line objects
l1 = pe.Line(x, y1, label='Bessel function of the first kind of order 1')
l2 = pe.Line(x, y2, label='Hankel function of the first kind of order 2')

# Plot using pyescher
pe.plot_lines(l1, l2, 
              xlabel='x', 
              ylabel='y', 
              title='Bessel and Hankel functions',
              show_marker=True,
              nmarkers=21,
              cycle_markers=True,
              cycle_linestyle=True,
              marker_size=5)
```

### 📊 **Example Output**
![Example Plot](assets/bessel_hankel_plot.png)

---

## 🎯 Features  
✅ **Publication-Ready Styling** – Easily generate beautiful plots.  
✅ **Auto-Cycling Markers & Linestyles** – Ensures unique styles per plot.  
✅ **Convenient Plot Handling** – Simplifies function-based plotting.  
✅ **Customizable Annotations & Legends** – Clean, well-labeled visuals.  

---

## 🔧 API Overview  
### 📈 `pe.plot_lines(*lines, **kwargs)`  
Plot multiple `Line` objects with various styling options.  
**Common Parameters:**  
- `xlabel`, `ylabel`, `title` – Axis labels and title.  
- `show_marker=True` – Adds markers automatically.  
- `nmarkers=21` – Controls marker placement frequency.  
- `cycle_markers=True` – Cycles through different marker styles.  
- `cycle_linestyle=True` – Cycles through different line styles.  
- `marker_size=5` – Adjusts marker size.  

---

## 🎨 Why Use pyescher?  
📌 **Optimized for Scientific & Technical Plots**  
📌 **Saves Time on Styling & Formatting**  
📌 **Produces Aesthetic, Readable Visuals for Papers & Presentations**  

---

## 🛠️ Installation & Development  
Clone the repository and install dependencies:  
```sh
git clone https://github.com/fennisrobert/pyescher.git
cd pyescher
pip install -e .
```

---

## 🤝 Contributing  
Contributions are welcome! Feel free to submit an issue or pull request.  

---

## 🏆 Acknowledgments  
Inspired by **physics-style plots** commonly found in **academic papers**.  

📧 **Contact:** [fennisrobert@gmail.com](mailto:fennisrobert@gmail.com)  
📜 **License:** MIT  

---

🚀 **Get started with `pyescher` and create stunning plots effortlessly!** 🎨  
