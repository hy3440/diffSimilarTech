import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
import os


doc1 = "offers more security functionality".split()
x1 = [1.6, 1.95, 1.675, 1.9]
y1 = [1.955, 1.995, 1.979, 1.96]
doc2 = "provides less safety features".split()
x2 = [1.65, 2, 1.625, 1.92]
y2 = [1.95, 2, 1.982, 1.95]

fig = plt.figure(figsize=(4,3))

ax = axisartist.Subplot(fig, 111)

fig.add_axes(ax)

ax.axis["bottom"].set_axisline_style("->", size=1.5)
ax.axis["left"].set_axisline_style("->", size=1.5)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('word embedding')

ax.axis["top"].set_visible(False)
ax.axis["right"].set_visible(False)

for i in range(4):
    plt.scatter(x1[i], y1[i], marker='o', c='', edgecolors='black')
    plt.scatter(x2[i], y2[i], c='blue', edgecolors='black')
    if y1[i] > y2[i]:
        annotate_y1 = y1[i] + 0.005
        annotate_y2 = y2[i] - 0.005
    else:
        annotate_y1 = y1[i] - 0.005
        annotate_y2 = y2[i] + 0.005
    ax.annotate(doc1[i], xy=(x1[i], y1[i]), xytext=(x1[i], annotate_y1))
    ax.annotate(doc2[i], xy=(x2[i], y2[i]), xytext=(x2[i], annotate_y2))
    ax.annotate("", xy=(x1[i], y1[i]), xytext=(x2[i], y2[i]),arrowprops=dict(arrowstyle="->"))

plt.show()
image_path = os.path.join(os.pardir, "figures", "wmd.pdf")
fig.savefig(image_path)
