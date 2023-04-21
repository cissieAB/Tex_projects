import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import colors

# HTML color code: https://htmlcolorcodes.com/
# Latex color code:
COLOR_LIMIT = "#EEDBDA"
COLOR_ACHIEVED = "#DE9A95"
COLOR_LINE = "#6E7F80"

x_entries = {'T4 f32', 'T4 f16', 'A100 f32', 'A100 f16'}
max_flops = {
    'Limit': [8.10, 65, 19.37, 312],
    'Achieved': [5.75, 34.64, 20.30, 214.41],
}

len_x = len(x_entries)
x = list(range(len_x))

#############################################################
# Ax1: bar chart
fig, ax1 = plt.subplots(figsize=(7, 4))

width = 0.4  # the width of the bars
idx = 0
color = [COLOR_LIMIT, COLOR_ACHIEVED]

x_center = [x[i] + width / 2 for i in range(len_x)]  # for central x-tick

for legend, flops in max_flops.items():
    offset = width * idx
    x_i = [x[i] + offset for i in range(len_x)]
    rects = ax1.bar(x_i, flops, width=width, label=legend, color=color[idx])
    ax1.bar_label(rects, padding=3)
    idx += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('Performance (TFLOPS)')
ax1.set_yscale('log')
ax1.set_ylim(0.1, 800)
ax1.set_xticks(x_center, x_entries)
ax1.legend(loc='upper left')

#############################################################
# Ax2: line
utilization = [max_flops['Achieved'][i] / max_flops['Limit'][i] * 100 for i in range(len_x)]
print(utilization)
ax2 = ax1.twinx()
ax2.plot(x_center, utilization, 'o-.', color=COLOR_LINE)
ax2.set_ylabel('Utilization (%)')

ax2.set_ylim(0, 125)

plt.savefig('fig2_max_performance.png')
