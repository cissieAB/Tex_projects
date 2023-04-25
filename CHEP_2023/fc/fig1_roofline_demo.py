import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cycler

# Data
# bw in FLOPs/byte, peak in TFLOPS
T4 = {'bw': 245.2, 'fp32': 8.1, 'tc': 65}
A100 = {'bw': 1607.3, 'fp32': 19.37, 'tc': 312}

NX = 200  # number of data points
X_MIN = 0.6
X_MAX = 4.6
Y_MIN = 0.1
Y_MAX = 500


def get_y_data(data_dict, x, dict_key):
    processed_y = []
    for i in range(NX):
        tflops = x[i] * data_dict['bw'] / 1000
        processed_y.append(data_dict[dict_key] if tflops > data_dict[dict_key] else tflops)
    return processed_y


def get_ridge_point(dict, dict_key):
    return dict[dict_key] * 1000 / dict['bw']


def add_one_roof_line(x, ax, x_th, y, y_peak, entry):
    """Plot a single roofline"""
    ax.plot(x, y, alpha=0.7)
    ax.fill_between(x, y, where=(x >= x_th), step='mid', alpha=0.15)
    # Add text
    flag_text = ("FP32" if entry == "fp32" else "TC FP16") + ' peak FLOPS'
    ax.text(x_th * 1.1, 0.45 * y_peak, flag_text)


def add_one_subplot(data_dict, ax, x, title_str):
    """Plot the rooflines of a single device"""
    dict_keys = ["fp32", "tc"]
    for dict_key in dict_keys:
        add_one_roof_line(x, ax, get_ridge_point(data_dict, dict_key),
                          get_y_data(data_dict, x, dict_key), data_dict[dict_key], dict_key)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim((Y_MIN, Y_MAX))
    ax.set_title(title_str)
    # ax[i].text(0.1, Y_MIN + 0.01, 'Memory-bound')
    ax.set_xlabel('Arithmetic intensity (FLOPs/byte)')
    ax.grid(True, which='both', alpha=0.5)


# cmap reference: https://matplotlib.org/stable/gallery/color/colormap_reference.html
cmap = matplotlib.colormaps['OrRd']
matplotlib.rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0.5, 0.8, 2)))

fig, axes = plt.subplots(1, 2, sharey='row', sharex='row', figsize=(7, 3))

x = np.logspace(X_MIN, X_MAX, NX)  # log base is 10
# print(x[:10])

add_one_subplot(T4, axes[0], x, "T4")
add_one_subplot(A100, axes[1], x, "A100 PCIe")
axes[0].set_ylabel('Performance (TFLOPS)')

plt.tight_layout()
# plt.show()
plt.savefig('fig1_roofline-demo.png')
