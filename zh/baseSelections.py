'''
Common selection used in ZH analysis
'''

def Vetos(row):
    '''
    applies b-tag, muon, electron and tau veto
    '''
    #if row.bjetCSVVeto:            return False
    if bool(row.muGlbIsoVetoPt10): return False
    if bool(row.tauVetoPt20):      return False
    if bool(row.eVetoMVAIso):      return False
    return True

def overlap(row,*args):
    return any( map( lambda x: x < 0.1, [getattr(row,'%s_%s_DR' % (l1,l2) ) for l1 in args for l2 in args if l1 <> l2 and hasattr(row,'%s_%s_DR' % (l1,l2) )] ) )

def ZMuMuSelection(row):
    '''
    Z Selection as AN
    '''
    #Z Selection
    if not row.doubleMuPass:                           return False
    if row.m1Pt < row.m2Pt:                            return False
    if row.m1Pt < 20:                                  return False
    if row.m2Pt < 10:                                  return False
    if row.m1AbsEta > 2.4:                             return False
    if row.m2AbsEta > 2.4:                             return False
    if abs(row.m1DZ) > 0.2:                            return False
    if abs(row.m2DZ) > 0.2:                            return False
    if not bool(row.m1PFIDTight):                      return False
    if bool(row.m1RelPFIsoDB > 0.25):                  return False
    if not bool(row.m2PFIDTight):                      return False
    if bool(row.m2RelPFIsoDB > 0.25):                  return False
    if bool(row.m1_m2_SS):                             return False
    if row.m1_m2_Mass < 71 or row.m1_m2_Mass > 111 :   return False
    return Vetos(row)

def ZEESelection(row):
    '''
    Z Selection as AN
    '''
    if not row.doubleEPass:                          return False
    if row.e1Pt < row.e2Pt:                          return False
    if row.e1Pt < 20:                                return False
    if row.e2Pt < 10:                                return False
    if row.e1AbsEta > 2.5:                           return False
    if row.e2AbsEta > 2.5:                           return False
    if abs(row.e1DZ) > 0.2:                          return False
    if abs(row.e2DZ) > 0.2:                          return False
    if not bool(row.e1MVAIDH2TauWP):                 return False
    if bool(row.e1RelPFIsoDB > 0.25):                return False
    if not bool(row.e2MVAIDH2TauWP):                 return False
    if bool(row.e2RelPFIsoDB > 0.25):                return False
    if bool(row.e1_e2_SS):                           return False
    if row.e1_e2_Mass < 71 or row.e1_e2_Mass > 111 : return False
    return Vetos(row)

def signalMuonSelection(row,muId):
    '''
    Basic selection for signal muons (the ones coming from Higgs). No Isolation applied
    '''
    if getattr(row, '%sPt' % muId) < 10:              return False
    if getattr(row, '%sAbsEta' % muId) > 2.4:         return False
    if abs(getattr(row, '%sDZ' % muId)) > 0.2:        return False
    if not bool(getattr(row, '%sPFIDTight' % muId) ): return False
    return True

def signalTauSelection(row, tauId, ptThr = 20):
    '''
    Basic selection for signal hadronic (the ones coming from Higgs). No Isolation is applied, but DecayMode is
    '''
    if not bool( getattr( row, '%sDecayFinding' % tauId) ):      return False
    if getattr( row, '%sPt' % tauId)  < ptThr:                   return False
    if getattr( row, '%sAbsEta' % tauId)  > 2.3:                 return False
    if abs(getattr( row, '%sDZ' % tauId) ) > 0.2:                return False
    return True


def signalElectronSelection(row, elId):
    '''
    Basic selection for signal electrons (the ones coming from Higgs). No Isolation applied
    '''
    if getattr(row, '%sPt' % elId) < 10:                 return False
    if getattr(row, '%sAbsEta' % elId) > 2.5:            return False
    if abs(getattr(row, '%sDZ' % elId)) > 0.2:           return False
    if not bool(getattr(row, '%sMVAIDH2TauWP' % elId) ): return False
    return True
    
