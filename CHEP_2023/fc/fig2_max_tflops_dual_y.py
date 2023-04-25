import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import colors

# HTML color code: https://htmlcolorcodes.com/
# Latex color code: http://latexcolor.com/
COLOR_LIMIT = "#EEDBDA"
COLOR_ACHIEVED = "#DE9A95"
COLOR_LINE = "#6E7F80"

x_entries = ['T4 FP32', 'T4 FP16', 'A100 FP32', 'A100 FP16']
max_flops = {
    'Limit': [8.1, 65.0, 19.4, 312.0],
    'Achieved': [5.75, 34.64, 20.30, 214.80],
}

len_x = len(x_entries)
x = list(range(len_x))

#############################################################
# Ax1: bar chart
fig, ax1 = plt.subplots(figsize=(6, 4))

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
ax1.set_ylabel('Peak performance (TFLOPS)')
ax1.set_yscale('log')
ax1.set_ylim(0.1, 800)
ax1.set_xticks(x_center, x_entries)  # overlap with table
ax1.legend(loc='upper left')

#############################################################
# Ax2: line
utilization = [max_flops['Achieved'][i] / max_flops['Limit'][i] * 100 for i in range(len_x)]
print("Utilization(%)")
print(utilization)
ax2 = ax1.twinx()
ax2.plot(x_center, utilization, 'o-.', color=COLOR_LINE)
ax2.set_ylabel('Utilization (%)')

ax2.set_ylim(0, 125)

############################################################
# table
# two blank rows to increase vspace
cell_text = [['' for i in range(len_x)], ['' for i in range(len_x)], ['%4.2f %%' %u for u in utilization]]

plt.table(cellText=cell_text,
          rowLabels=['', '', 'Utilization'], cellLoc='center',
          loc='bottom', edges='vertical')
# Adjust layout to make room for the table
plt.subplots_adjust(left=0.13, bottom=0.2)

plt.savefig('fig2_max_performance.png')

##########################################
print("f32 speedup %6.1f"%(max_flops['Achieved'][2]/max_flops['Achieved'][0]))
print("f16 speedup %6.1f"%(max_flops['Achieved'][3]/max_flops['Achieved'][1]))

