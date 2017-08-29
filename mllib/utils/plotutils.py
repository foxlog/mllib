import pandas as pd
import numpy as np
from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns


def plot(x, y, color= None, linewidth=None, linestyle=None, marker = None, label=None, figsize=None, xlim=None, xlabel=None, ylabel=None):
    plt.rcParams["figure.figsize"] = figsize if figsize else (12, 8)
    # x 轴缩放
    if xlim:
        plt.xlim(xlim)
    if xlabel:
        plt.xlabel(xlim)
    if ylabel:
        plt.ylabel(ylabel)
    plt.plot(x, y, color=color if color else 'blue', linewidth=linewidth if linewidth else 1.5, linestyle=linestyle if linestyle else '-', marker= marker if marker else '.', label=label if label else '')

#散点图
def scatter(x, y, marker = None, linewidths=None, color=None, xlim=None, xlabel=None, ylabel=None, figsize=None):
    plt.rcParams["figure.figsize"] = figsize if figsize else (12, 8)

    if xlim:
        plt.xlim(xlim)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)

    plt.scatter(x, y, s=30, c=color if color else 'r', marker=marker if marker else 'x',
                linewidths=linewidths if linewidths else 1)

#散点图 正负样本
def scatter_2(x_pos, y_pos, x_neg, y_neg, pos_marker = None, neg_marker=None, linewidths=None, pos_color=None, neg_color=None,pos_label=None, neg_label=None, xlim=None, xlabel=None, ylabel=None, figsize=None, axes=None):
    plt.rcParams["figure.figsize"] = figsize if figsize else (12, 8)

    if xlim:
        plt.xlim(xlim)


    # If no specific axes object has been passed, get the current axes.
    if axes == None:
        axes = plt.gca()

    # 正负样本 scatter
    axes.scatter(x_pos, y_pos, marker=pos_marker if pos_marker else '+', c=pos_color if pos_color else 'k', s=60, linewidth=linewidths if linewidths else 2, label=pos_label)
    axes.scatter(x_neg, y_neg, c=neg_color if neg_color else 'y', s=60, label=neg_label)
    if xlabel:
        axes.set_xlabel(xlabel)
    if ylabel:
        axes.set_ylabel(ylabel)
    axes.legend(frameon=True, fancybox=True)



# 正太分布散点图
def scatter_demo():
    x = np.random.normal(size=1000)
    y = np.random.normal(size=1000)
    scatter(x, y, xlabel='xxx', ylabel='yyy')
    plt.show()

def scatter_2_demo():
    pass

def plot_demo():
    x = np.arange(0., 10, 0.2)
    y1 = np.cos(x)
    y2 = np.sin(x)
    y3 = np.sqrt(x)
    y4 = 2 * (x ** 2) + 3

    plot(x, y1, color='blue', linewidth=1.5, linestyle='-', marker='.', label=r'$y = cos{x}$')
    plot(x, y2, color='green', linewidth=1.5, linestyle='-', marker='*', label=r'$y = sin{x}$')
    plot(x, y3, color='m', linewidth=1.5, linestyle='-', marker='x', label=r'$y = \sqrt{x}$')
    plt.show()

if __name__ == '__main__':
    #plot_demo()
    scatter_demo()





