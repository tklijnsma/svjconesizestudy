# -*- coding: utf-8 -*-
import os, shutil, logging
import os.path as osp
from array import array
import svjconesizestudy
logger = logging.getLogger('svjcs')
import ROOT

class EventFactory(object):
    """docstring for EventFactory"""

    def __init__(self, rootfile, max_events=None):
        super(EventFactory, self).__init__()
        self.rootfile = rootfile
        logger.info('Opening %s', self.rootfile)
        self.tfile = ROOT.TFile.Open(self.rootfile)
        self.tree = self.tfile.Get('Events')
        self.max_events = max_events

    def __del__(self):
        try:
            self.tfile.Close()
        except:
            pass

    def __iter__(self):
        # for i_event, event in enumerate(self.tree):
        #     if not(self.max_events is None) and i_event > self.max_events:
        #         logger.debug(
        #             'i_event = %s > max_events (%s); stopping',
        #             i_event, self.max_events
        #             )
        #         raise StopIteration
        #     event.__class__ = Event
        #     logger.debug('Yielding event %s', i_event)
        #     yield event
        self.tree.__class__ = Event
        n_events = self.tree.GetEntries()
        for i_event in range(n_events):
            self.tree.GetEntry(i_event)
            yield self.tree


class EventFactoryDir(object):

    @classmethod
    def from_sedir(cls, sedir, max_events=None):
        import qondor
        return cls(qondor.seutils.ls_root(sedir), max_events)

    def __init__(self, rootfiles, max_events=None):
        super(EventFactoryDir, self).__init__()
        self.max_events = max_events
        self.rootfiles = rootfiles
        self.tree = ROOT.TChain('Events')
        for rootfile in self.rootfiles:
            self.tree.Add(rootfile)
        self.tree.__class__ = Event
        self.n_events = self.tree.GetEntries()

    def __iter__(self):
        for i_event in range(self.n_events):
            if i_event == self.max_events: raise StopIteration
            self.tree.GetEntry(i_event)
            yield self.tree

    def get(self, i):
        self.tree.GetEntry(i)
        return self.tree

    def __len__(self):
        return self.n_events if (self.max_events is None) else min(self.n_events, self.max_events)



class Event(ROOT.TTree):

    def iter_genparticlepluss(self):
        for i in self.GenParticlePluss_particleHierarchy__SoftDropGenJets.product():
            # i.__class__ = svjconesizestudy.SubstructurePack
            yield i

    def genparticlepluss(self):
        return list(self.iter_genparticlepluss())

    def iter_substructurepacks(self):
        for i in self.SubstructurePacks_substructurePacks__SoftDropGenJets.product():
            i.__class__ = svjconesizestudy.SubstructurePack
            yield i

    def substructurepacks(self):
        return list(self.iter_substructurepacks())

    def iter_dmparticles(self):
        for i in self.recoGenParticles_DMGenParticles__SoftDropGenJets.product():
            i.__class__ = svjconesizestudy.GenParticle
            yield i

    def dmparticles(self):
        return list(self.iter_dmparticles())

    def iter_genparticles(self):
        for i in self.recoGenParticles_genParticles__GEN.product():
            i.__class__ = svjconesizestudy.GenParticle
            yield i

    def genparticles(self):
        return list(self.iter_genparticles())

    def iter_genparticlesforjets(self):
        # for i in self.recoGenParticles_saveGenParticlesForJetsNoNu__SoftDropGenJets.product():
        for i in self.recoGenParticles_saveGenParticlesForJetsNoNuOnlyZPrime__SoftDropGenJets.product():
            i.__class__ = svjconesizestudy.GenParticle
            yield i

    def genparticlesforjets(self):
        return list(self.iter_genparticlesforjets())

    def ht(self):
        return self.double_htProducer_genHT_SoftDropGenJets.product()[0]

