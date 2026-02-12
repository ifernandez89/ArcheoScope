#!/usr/bin/env python3
"""Test matplotlib backend"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

print("Testing matplotlib backend...")

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([1, 2, 3], [1, 2, 3])

output_path = "test_plot.png"
plt.savefig(output_path)
plt.close()

import os
if os.path.exists(output_path):
    print(f"✅ File created: {output_path}")
else:
    print(f"❌ File NOT created: {output_path}")
