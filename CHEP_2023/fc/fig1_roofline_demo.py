import math
import numpy as np
import matplotlib.pyplot as plt

COLOR_1 = "#DE9A95"
COLOR_2 = "#8A3324"
COLOR_3 = "#800020"
COLORS = [COLOR_1, COLOR_2, COLOR_3]

# slope in FLOPs/Byte, peak in TFLOPS
T4_f32 = {'slope': 245.2, 'peak': 8.1}
A100_f32 = {'slope': 1607.3, 'peak': 19.37}

NX = 200  # number of data points
X_MIN = -1.0
X_MAX = 4
Y_MIN = 0.01
Y_MAX = 100


def get_y_data(data_dict, x):
    processed_y = []
    for i in range(NX):
        tflops = x[i] * data_dict['slope'] / 1000
        processed_y.append(data_dict['peak'] if tflops > data_dict['peak'] else tflops)
    return processed_y


x = np.logspace(X_MIN, X_MAX, NX)  # log base is 10
# print(x[:10])
y_T4 = get_y_data(T4_f32, x)
y_A100 = get_y_data(A100_f32, x)

T4_x_th = T4_f32['peak'] * 1000 / T4_f32['slope']
A100_x_th = A100_f32['peak'] * 1000 / A100_f32['slope']


def add_sub_plot(x, ax, x_th, y, y_peak, i, title_str, ):
    ax[i].plot(x, y, c=COLORS[i])
    ax[i].set_xscale('log')
    ax[i].set_yscale('log')
    ax[i].set_ylim((Y_MIN, Y_MAX))
    ax[i].fill_between(x, y, where=(x >= x_th), color=COLORS[i], step='mid', alpha=0.2)
    ax[i].set_xlabel('Arithmetic intensity (FLOPs/Byte)')
    if i == 0:
        ax[i].set_ylabel('F32 performance (TFLOPS)')
    ax[i].grid(True, which='major')
    ax[i].text(x_th * 1.1, 0.5 * y_peak, 'Compute bound', color=COLORS[i + 1])
    ax[i].text(0.1, Y_MIN + 0.01, 'Memory bound', color=COLORS[i + 1])
    ax[i].set_title(title_str)


fig, ax = plt.subplots(1, 2, sharey=True, sharex=True, figsize=(8, 3))
add_sub_plot(x, ax, T4_x_th, y_T4, T4_f32['peak'], 0, "T4")
add_sub_plot(x, ax, A100_x_th, y_A100, A100_f32['peak'], 1, "A100 PCIe")

#######################

plt.subplots_adjust(bottom=0.2)

# plt.show()
plt.savefig('fig1_roofline-demo.png')
