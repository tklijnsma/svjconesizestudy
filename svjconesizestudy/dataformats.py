# -*- coding: utf-8 -*-
import os, shutil, logging
import os.path as osp
from array import array
import svjconesizestudy
logger = logging.getLogger('svjcs')
import ROOT


class SubstructurePack(ROOT.SubstructurePack):

    def get_zprime(self):
        if self.hasZprime():
            z = self.zprime()
            z.__class__ = GenParticle
            return z
        else:
            return None


class GenParticle(ROOT.reco.GenParticle):
    
    def is_dark(self):
        return abs(self.pdgId()) > 4000000


