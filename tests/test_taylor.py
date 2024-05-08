import pytest
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from geocat.viz.taylor import TaylorDiagram


@pytest.mark.mpl_image_compare(tolerance=0.02, remove_text=True, style='default')
def test_add_model_set():
    fig = plt.figure(figsize=(10, 10))
    taylor = TaylorDiagram(fig=fig, label='REF')

    taylor.add_model_set([1.230, 0.988, 1.092], [0.958, 0.973, 0.740],
                         color='red',
                         label='Model A',
                         fontsize=16)

    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02, remove_text=True, style='default')
def test_add_legend():
    fig = plt.figure(figsize=(10, 10))
    taylor = TaylorDiagram(fig=fig, label='REF')

    taylor.add_model_set(
        [1.230, 0.988, 1.092],
        [0.958, 0.973, 0.740],
        percent_bias_on=
        True,  # indicate marker and size to be plotted based on bias_array
        bias_array=[2.7, -1.5, 17.31],  # specify bias array
        color='red',
        label='Model A',
        fontsize=16)

    taylor.add_model_set([1.129, 0.996, 1.016], [0.963, 0.975, 0.801],
                         percent_bias_on=True,
                         bias_array=[1.7, 2.5, -17.31],
                         color='blue',
                         label='Model B',
                         fontsize=16)

    taylor.add_legend(fontsize=16)

    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02, remove_text=True, style='default')
def test_add_bias_legend():
    fig = plt.figure(figsize=(10, 10))
    taylor = TaylorDiagram(fig=fig, label='REF')

    taylor.add_model_set(
        [1.230, 0.988, 1.092],
        [0.958, 0.973, 0.740],
        percent_bias_on=
        True,  # indicate marker and size to be plotted based on bias_array
        bias_array=[2.7, -1.5, 17.31],  # specify bias array
        color='red',
        label='Model A',
        fontsize=16)

    taylor.add_bias_legend()

    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02, remove_text=True, style='default')
def test_add_model_name():
    fig = plt.figure(figsize=(10, 10))
    taylor = TaylorDiagram(fig=fig, label='REF')

    taylor.add_model_set(
        [1.230, 0.988, 1.092],
        [0.958, 0.973, 0.740],
        percent_bias_on=
        True,  # indicate marker and size to be plotted based on bias_array
        bias_array=[2.7, -1.5, 17.31],  # specify bias array
        color='red',
        label='Model A',
        fontsize=16)

    taylor.add_model_name(['a', 'b', 'c'], fontsize=16)

    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02, remove_text=True, style='default')
def test_add_corr_grid():
    fig = plt.figure(figsize=(10, 10))
    taylor = TaylorDiagram(fig=fig, label='REF')

    taylor.add_corr_grid(np.array([0.6, 0.9]))

    taylor.add_model_set(
        [1.230, 0.988, 1.092],
        [0.958, 0.973, 0.740],
        percent_bias_on=
        True,  # indicate marker and size to be plotted based on bias_array
        bias_array=[2.7, -1.5, 17.31],  # specify bias array
        color='red',
        label='Model A',
        fontsize=16)

    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02, remove_text=True, style='default')
def test_add_contours():
    fig = plt.figure(figsize=(10, 10))
    taylor = TaylorDiagram(fig=fig, label='REF')

    taylor.add_model_set(
        [1.230, 0.988, 1.092],
        [0.958, 0.973, 0.740],
        percent_bias_on=
        True,  # indicate marker and size to be plotted based on bias_array
        bias_array=[2.7, -1.5, 17.31],  # specify bias array
        color='red',
        label='Model A',
        fontsize=16)

    taylor.add_contours(levels=np.arange(0, 1.1, 0.25),
                        colors='lightgrey',
                        linewidths=0.5)
    return fig
