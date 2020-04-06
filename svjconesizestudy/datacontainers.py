# -*- coding: utf-8 -*-
import os, shutil, logging, uuid, copy
import os.path as osp
from array import array
import numpy as np
import svjconesizestudy
logger = logging.getLogger('svjcs')
import ROOT




class Histogram(object):
    """docstring for Histogram"""
    def __init__(self):
        super(Histogram, self).__init__()
        
    def set_binning(self, binning):
        self.binning = np.array(binning)
        self.n_bins = len(binning)-1
        self.bin_centers = 0.5*(self.binning[:-1] + self.binning[1:])
        self._y_values = np.zeros(self.n_bins)

    def fill_bin(self, i_bin, value):
        self._y_values[i_bin] += value

    def find_bin(self, x):
        return (np.abs(self.bin_centers - x)).argmin()

    def fill(self, x, value):
        self.fill_bin(self.find_bin(x), value)

    @property
    def y_values(self):
        return self._y_values

    @y_values.setter
    def y_values(self, ys):
        self._y_values = ys

    def to_th1(self):
        H = ROOT.TH1F(
            str(uuid.uuid4()), '',
            self.n_bins, array('f', self.binning)
            )
        ROOT.SetOwnership(H, False)
        for i_bin in range(self.n_bins):
            H.SetBinContent(i_bin+1, self.y_values[i_bin])
        return H


class AverageHistogram(Histogram):
    """docstring for AverageHistogram"""
    def __init__(self, binning=None):
        super(AverageHistogram, self).__init__()
        if binning: self.set_binning(binning)

    def set_binning(self, binning):
        super(AverageHistogram, self).set_binning(binning)
        if hasattr(self, 'sums'): logger.warning('Deleting sums')
        if hasattr(self, 'counts'): logger.warning('Deleting counts')
        self.sums = np.zeros(self.n_bins)
        self.counts = np.zeros(self.n_bins)

    def fill_bin(self, i_bin, value):
        self.counts[i_bin] += 1
        self.sums[i_bin] += value

    @property
    def y_values(self):
        return self.sums / self.counts

    def to_cumulative(self):
        new = copy.deepcopy(self)
        new.__class__ = Histogram
        summed_y_values = np.zeros(self.n_bins)
        for i in range(self.n_bins):
            summed_y_values[i] = self.y_values[:i+1].sum()
        new._y_values = summed_y_values
        return new
        
