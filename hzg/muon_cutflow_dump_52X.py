#!/usr/bin/env python

import ROOT
from ROOT import TFile, TTree, gDirectory, TH1F

import sys

def makeIsoString(prefix):
    result  = '(%sPFChargedIso + '%(prefix)
    result += 'max(%sPFNeutralIso + %sPFPhotonIso - '
    '%sEffectiveArea2012*max(%sRhoHZG2012,0.0), 0.0))'(prefix,prefix,prefix,prefix)
    result += '/%sPt < 0.12'          
    return result

if len(sys.argv) != 2:
    sys.exit("this program accepts one argument (the file name!)")

print "Opening %s"%(sys.argv[1])

pwd = gDirectory.GetPath()
file = TFile.Open(sys.argv[1])
gDirectory.cd(pwd)

eventCount = file.Get("mm").Get("eventCount")
mmNtuple  = file.Get("mm").Get("final").Get("Ntuple")
mmgNtuple = file.Get("mmg").Get("final").Get("Ntuple")

print "Initial: %i"%(eventCount.GetEntries())

def trigger_req(event,i):
    return (event.doubleMuPass[i] == 1 and event.doubleMuPrescale[i] == 1)

def vtx_req(event,i):
    return (event.pvIsValid[i] == 1 and event.pvIsFake[i] == 0)

def mu_id(event,i):
    return (event.m1Pt[i] > 10 and event.m2Pt[i] > 10 and
            event.m1AbsEta[i] < 2.4 and event.m2AbsEta[i] < 2.4 and
            event.m1IDHZG2012[i] == 1 and event.m2IDHZG2012[i] == 1)

def mu_iso(event,i):
    m1Iso = ( (event.m1PFChargedIso[i] +
               max(event.m1PFNeutralIso[i] + event.m1PFPhotonIso[i]
                   -event.m1EffectiveArea2012[i]*
                   max(event.m1RhoHZG2012[i],0.0),
                   0.0))/event.m1Pt[i] )
    m2Iso = ( (event.m2PFChargedIso[i] +
               max(event.m2PFNeutralIso[i] + event.m2PFPhotonIso[i]
                   -event.m2EffectiveArea2012[i]*
                   max(event.m2RhoHZG2012[i],0.0),
                   0.0))/event.m2Pt[i] )

    return (m1Iso < 0.12 and m2Iso < 0.12)

def z_id(event,i):
    return ( (event.m1Pt[i] > 20 or event.m2Pt[i] > 20) and
             event.m1_m2_Mass[i] > 50 and
             event.m1_m2_SS[i] == 0)

def photon_id_debug(event,i):
    #print 'Precalculated PhotonID Result = ', bool(event.gCBID_MEDIUM[i])

    result = []

    ascEta = abs(event.gSCEta[i])

    eVeto = event.gConvSafeElectronVeto[i]
    #print 'Conversion Safe Electron Veto :',eVeto

    result.append(eVeto)

    singleTowerHoE = event.gSingleTowerHadronicOverEm[i]
    #print 'Single Tower H/E              :',singleTowerHoE,' < 0.05 == ', \
    #      (singleTowerHoE<0.05)

    result.append(singleTowerHoE<0.05)

    sihih = event.gSigmaIEtaIEta[i]

    rho = max(event.m1RhoHZG2011[i],0.0) ##HACK!
    pfChgIso = event.gPFChargedIso[i]
    pfChgEA  = event.gEffectiveAreaCHad[i]
    
    chgIso = max(pfChgIso - rho*pfChgEA,0.0)

    pfNeutIso= event.gPFNeutralIso[i]
    pfNeutEA = event.gEffectiveAreaNHad[i]    

    neutIso = max(pfNeutIso - 0.04*event.gPt[i] - rho*pfNeutEA,0.0)

    pfPhoIso = event.gPFPhotonIso[i]
    pfPhoEA  = event.gEffectiveAreaPho[i]

    phoIso = max(pfPhoIso - 0.005*event.gPt[i] - rho*pfPhoEA,0.0)

    if( ascEta < 1.5 ):
        result.append(sihih < 0.011)
        result.append(chgIso < 1.5)
        result.append(neutIso < 1.0)
        result.append(phoIso < 0.7)
    else:
        result.append(sihih < 0.033)
        result.append(chgIso < 1.2)
        result.append(neutIso < 1.5)
        result.append(phoIso < 1.0)

    if( True ):
        print "ALLPHOTON :: run %i  evt: %i  pt:%.4f  scEta: %0.6f  hoe: %f" \
              "  sieie: %f  pfCh: %.6f  pfNe: %.6f  pfGa: %.6f  rho: %f  EACh: %.3f   EANeut: %.3f   EAPho: %.3f" \
              %(event.run[i], event.evt[i], event.gPt[i], event.gSCEta[i],
                event.gSingleTowerHadronicDepth1OverEm[i] +
                event.gSingleTowerHadronicDepth2OverEm[i] ,
                event.gSigmaIEtaIEta[i],
                event.gPFChargedIso[i],
                event.gPFNeutralIso[i],
                event.gPFPhotonIso[i],
                rho,
                pfChgEA,pfNeutEA,pfPhoEA)
        #print 'Conversion Safe Electron Veto :',eVeto,' == True == ', \
        #      (eVeto==True)
        #print 'Single Tower H/E              :',singleTowerHoE,' < 0.05 == ',\
        #      (singleTowerHoE<0.05)
        #if( ascEta < 1.560 ):
        #    print 'sihih        :',sihih,'< 0.011 == ',(sihih < 0.011)
        #    print 'pfChargedIso :',chgIso,' < 1.5 == ',(chgIso < 1.5)
        #    print 'pfNeutralIso :',neutIso,' < 1.0 == ',(neutIso < 1.0)
        #    print 'pfPhotonIso  :',phoIso,' < 0.7 == ',(phoIso < 0.7)
        #else:
        #    print 'sihih :',sihih,'< 0.033 == ',(sihih < 0.033)
        #    print 'pfChargedIso :',chgIso,' < 1.2 == ',(chgIso < 1.2)
        #    print 'pfNeutralIso :',neutIso,' < 1.5 == ',(neutIso < 1.5)
        #    print 'pfPhotonIso  :',phoIso,' < 1.0 == ',(phoIso < 1.0)
    return result

def eleVeto(event,i):
    eVeto = event.gConvSafeElectronVeto[i]

    return eVeto == True

def HoverE(event,i):
    singleTowerHoE = event.gSingleTowerHadronicOverEm[i]
    return singleTowerHoE<0.05

def sihih(event,i):
    sihih = event.gSigmaIEtaIEta[i]
    ascEta = abs(event.gSCEta[i])

    if( ascEta < 1.5 ):
        return (sihih < 0.011)        
    else:
        return (sihih < 0.033)
        
def phoIso(event,i):
    result = []
    ascEta = abs(event.gSCEta[i])

    rho = event.m1RhoHZG2011[i] ##HACK!
    pfChgIso = event.gPFChargedIso[i]
    pfChgEA  = event.gEffectiveAreaCHad[i]
    
    chgIso = max(pfChgIso - rho*pfChgEA,0.0)

    pfNeutIso= event.gPFNeutralIso[i]
    pfNeutEA = event.gEffectiveAreaNHad[i]    

    neutIso = max(pfNeutIso - 0.04*event.gPt[i] - rho*pfNeutEA,0.0)

    pfPhoIso = event.gPFPhotonIso[i]
    pfPhoEA  = event.gEffectiveAreaPho[i]

    phoIso = max(pfPhoIso - 0.005*event.gPt[i] - rho*pfPhoEA,0.0)

    if( ascEta < 1.5 ):        
        result.append(chgIso < 1.5)
        result.append(neutIso < 1.0)
        result.append(phoIso < 0.7)
    else:       
        result.append(chgIso < 1.2)
        result.append(neutIso < 1.5)
        result.append(phoIso < 1.0)
        
    return (result.count(True)==3)

def good_photon(event,i):
    pt_over_m = event.gPt[i]/event.Mass[i]
    ascEta = abs(event.gSCEta[i])
    
    return ( pt_over_m > 15.0/110.0 and
             (ascEta < 1.4442 or (ascEta > 1.566 and ascEta < 2.5)) and
             photon_id_debug(event,i) )

def pho_fiducial(event,i):
    pt_over_m = event.gPt[i]/event.Mass[i]
    ascEta = abs(event.gSCEta[i])
    
    return ( pt_over_m > 15.0/110.0 and
             (ascEta < 1.4442 or (ascEta > 1.566 and ascEta < 2.5)) )

def photon_dr(event,i):
    return min(event.m1_g_DR[i],event.m2_g_DR[i]) > 0.4

def zg_mass_low(event,i):
    return event.Mass[i] > 115.0 

def zg_mass_high(event,i):
    return event.Mass[i] < 180.0

cut_list_mm = [trigger_req, #HLT
               vtx_req, #PV selection
               mu_id, #10 GeV && ID
               mu_iso, #ISO
               z_id #Z ID
               ]
counts_mm = [0 for cut in cut_list_mm] + [0]

cut_list_mmg = list(cut_list_mm)
cut_list_mmg += [pho_fiducial,                
                 eleVeto,
                 HoverE,
                 sihih,
                 phoIso,#good photon
                 photon_dr, #delta r lepton-photon
                 zg_mass_low,
                 zg_mass_high
                 ]
counts_mmg = [0 for cut in cut_list_mmg] + [0]

for event in mmNtuple:
    one_passes = False
    counts_evt = [0 for cut in cut_list_mm]
    
    for i in range(event.N_PATFinalState):
        
        cut_bits = [cut(event,i) for cut in cut_list_mm]
        one_passes = one_passes or (cut_bits.count(True) == len(cut_list_mm))

        passed_last = True
        kbit = 0
        
        while passed_last and kbit < len(cut_bits):
            counts_evt[kbit] += 1*cut_bits[kbit]            
            passed_last = cut_bits[kbit]
            kbit += 1

        

    for i,count in enumerate(counts_evt):
        counts_mm[i] += 1*(count > 0)
        
    counts_mm[len(cut_list_mm)] += int(one_passes)

print 'HLT     : %i'%(counts_mm[0])
print 'VTX     : %i'%(counts_mm[1])
print 'Muon ID : %i'%(counts_mm[2])
print 'Muon Iso: %i'%(counts_mm[3])
print 'Z Sel   : %i'%(counts_mm[4])
print 'Total MM: %i'%(counts_mm[5])
print


for event in mmgNtuple:
    one_passes = False
    counts_evt = [0 for cut in cut_list_mmg]
    
    for i in range(event.N_PATFinalState):

        photon_id_debug(event,i)
        
        cut_bits = [cut(event,i) for cut in cut_list_mmg]
        one_passes = one_passes or (cut_bits.count(True) == len(cut_list_mmg))

        passed_last = True
        kbit = 0
        
        while passed_last and kbit < len(cut_bits):
            counts_evt[kbit] += 1*cut_bits[kbit]            
            passed_last = cut_bits[kbit]
            kbit += 1

    for i,count in enumerate(counts_evt):
        counts_mmg[i] += 1*(count > 0)
        
    counts_mmg[len(cut_list_mmg)] += int(one_passes)
    
print "Fiducial Cuts   : %i"%(counts_mmg[len(cut_list_mm)])
print "Electron Veto   : %i"%(counts_mmg[len(cut_list_mm)+1])
print "ST HoE          : %i"%(counts_mmg[len(cut_list_mm)+2])
print "SIHIH           : %i"%(counts_mmg[len(cut_list_mm)+3])
print "PF Iso          : %i"%(counts_mmg[len(cut_list_mm)+4])
print "DR(l,g) > 0.4   : %i"%(counts_mmg[len(cut_list_mm)+5])
print "ZG Mass > 115   : %i"%(counts_mmg[len(cut_list_mm)+6])
print "ZG Mass < 180   : %i"%(counts_mmg[len(cut_list_mm)+7])
print "Total mmg       : %i"%(counts_mmg[len(cut_list_mmg)]) 

file.Close()