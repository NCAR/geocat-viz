# https://github.com/PeterRochford/SkillMetrics
import numpy as np


def taylor_stats(t, r):
    """Returns the Pearson correlation coefficient, or pattern correlation, and
    ratios of normalized root mean square test of test and reference data sets.

    :param t: array_like
    Test data array. must be 2d like (nx, ny) or (nlat, mlon)

    :param r: array_like
    Reference data array. Must be same size and shape as test array

    :return:
    Dictionary of correlation coefficient, centered root-means-square difference, and
    standard deviation.
    """

    if t.shape != r.shape:
        raise Exception("t and r must be the same shape")
    else:
        pass

    # Calculate correlation coefficient with Numpy
    corcoef = np.corrcoef(t, r)
    corcoef = corcoef[0]
    corcoef = corcoef[0]

    # Calculate centered root mean square (RMS) difference
    # Calculate means
    tmean = np.mean(t)
    rmean = np.mean(r)

    # Calculate RMS
    rmsd = np.square((t - tmean) - (r - rmean))
    rmsd = np.sum(rmsd) / t.size
    rmsd = np.sqrt(rmsd)

    # Calculate std dev of test field
    sdev_t = np.std(t)

    # Calculate std dev of reference field
    sdev_r = np.std(r)

    # Put two std dev's into array
    sdev = [sdev_t, sdev_r]

    # Store statistics in a dictionary
    t_stats = {'ccoef': corcoef, 'crmsd': rmsd, 'sdev': sdev}
    return t_stats
