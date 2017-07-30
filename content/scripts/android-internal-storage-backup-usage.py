#!/usr/bin/env python3

"""
=========================================================================
A Python script to plot my phone's internal storage usage with matplotlib
=========================================================================

Author: Tadej Janež
License: MIT

Based on https://matplotlib.org/mpl_examples/pie_and_polar_charts/pie_demo_features.py

"""
from pathlib import Path

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

# My phone's internal storage usage by file type
file_types_and_usage = (
    ('image | jpeg', 1483),
    ('video | mp4', 678),
    ('audio | mpeg', 642),
    ('audio | ogg', 405),
    ('application | octet-stream', 103),
    ('other', 247),
)

# Prepare fonts
font1 = FontProperties()
font1.set_family('Source Han Sans TW')
font2 = font1.copy()
font2.set_size('small')

# Prepare subplots
fig1, ax1 = plt.subplots()

# Draw pie chart
_, texts, autotexts = ax1.pie(
    # sizes
    [ftu[1] for ftu in file_types_and_usage],
    labels=[ftu[0] for ftu in file_types_and_usage],
    autopct='%1.f%%',
    pctdistance=0.7,
    startangle=90
)
# Set equal aspect ratio to ensure that pie is drawn as a circle
ax1.axis('equal')

# Set fonts
plt.setp(texts, fontproperties=font1)
plt.setp(autotexts, fontproperties=font2)

fig1.savefig(str(Path('..', 'images', 'android-internal-storage-backup-usage.svg')))
