'''

Plot the EET channel

Usage: python WHPlotterEET.py

'''

import glob
import logging
import os
import ROOT
import sys
import WHPlotterBase

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

class WHPlotterEET(WHPlotterBase.WHPlotterBase):
    def __init__(self, files, lumifiles, outputdir):
        super(WHPlotterEET, self).__init__(files, lumifiles, outputdir)

if __name__ == "__main__":
    jobid = os.environ['jobid']

    print "Plotting EET for %s" % jobid

    # Figure out if we are 7 or 8 TeV
    period = '7TeV' if '7TeV' in jobid else '8TeV'
    sqrts = 7 if '7TeV' in jobid else 8

    samples = [
        'Zjets_M50',
        'WplusJets_madgraph',
        'WZJetsTo3LNu*',
        'ZZ*',
        'VH*',
        'TTplusJets_madgraph',
        "data_DoubleEl*",
    ]

    files = []
    lumifiles = []

    for x in samples:
        files.extend(glob.glob('results/%s/WHAnalyzeEET/%s.root' % (jobid, x)))
        lumifiles.extend(glob.glob('inputs/%s/%s.lumicalc.sum' % (jobid, x)))

    outputdir = 'results/%s/plots/eet' % jobid
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    plotter = WHPlotterEET(files, lumifiles, outputdir)

    ###########################################################################
    ##  Zmm control plots #####################################################
    ###########################################################################

    # Control Z->mumu + jet region
    plotter.plot_mc_vs_data('os/p1p2f3', 'e1e2Mass', xaxis='m_{ee} (GeV)', xrange=(60, 120))
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-os-p1p2f3-e1e2Mass')

    plotter.plot_mc_vs_data('os/p1p2f3/w3', 'e1e2Mass')
    plotter.save('mcdata-os-p1p2f3-w3-e1e2Mass')

    plotter.plot_mc_vs_data('os/p1f2p3', 'e1e2Mass', xaxis='m_{ee} (GeV)', xrange=(60, 120))
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-os-p1f2p3-e1e2Mass')

    # Check PU variables
    plotter.plot_mc_vs_data('os/p1p2f3', 'rho')
    plotter.save('mcdata-os-p1p2f3-rho')

    plotter.plot_mc_vs_data('os/p1p2f3', 'nvtx')
    plotter.save('mcdata-os-p1p2f3-nvtx')

    # Lower stat but closer to signal region
    plotter.plot_mc_vs_data('os/p1p2p3', 'rho')
    plotter.save('mcdata-os-p1p2p3-rho')

    plotter.plot_mc_vs_data('os/p1p2p3', 'nvtx')
    plotter.save('mcdata-os-p1p2p3-nvtx')

    # Make Z->mumu + tau jet control
    def make_styler(color, format=None):
        def unsuck(x):
            x.SetFillStyle(0)
            x.SetLineColor(color)
            x.SetLineWidth(2)
            if format:
                x.format = format
        return unsuck

    #
    # Makes Tau fr control plot
    #
    zmm_weighted = plotter.plot('data', 'os/p1p2f3/w3/e1e2Mass',  'hist', styler=make_styler(2, 'hist'), xrange=(60, 120))
    zmm_weighted.SetTitle("Zee + fake #tau_{h} est.")
    zmm_weighted.legendstyle='l'
    zmm_weighted.GetXaxis().SetTitle("m_{ee} (GeV)")

    zmm_unweighted = plotter.plot('data', 'os/p1p2p3/e1e2Mass', 'same', styler=make_styler(1), xrange=(60, 120))
    zmm_unweighted.SetTitle("Zee observed")
    zmm_unweighted.SetTitle("Zee + fake #tau_{h} obs.")
    zmm_unweighted.legendstyle='pe'

    plotter.add_legend([zmm_weighted, zmm_unweighted])
    plotter.add_cms_blurb(sqrts)
    plotter.save('zmm-os-fr-control')

    #
    # Makes charge fr control plot
    #

    zeet_os_weighted = plotter.plot('data', 'os/p1p2f3/c1/e1e2Mass',  'hist', styler=make_styler(2, 'hist'), xrange=(60, 120))
    zeet_os_weighted.SetTitle("Ze^{#pm}e^{#mp} + fake #tau_{h} charge flip est.")
    zeet_os_weighted.legendstyle='l'
    zeet_os_weighted.GetXaxis().SetTitle("M_{ee} (GeV)")

    zee_ss_unweighted = plotter.plot('data', 'ss/p1p2f3/e1e2Mass', 'same', styler=make_styler(1), xrange=(60, 120))
    zee_ss_unweighted.SetTitle("Ze^{#pm}e^{#pm} + fake #tau_{h} obs.")
    zee_ss_unweighted.legendstyle='pe'

    plotter.add_legend([zeet_os_weighted, zee_ss_unweighted])
    plotter.add_cms_blurb(sqrts)
    plotter.save('zmm-os-ss-charge-flip-control')

    plotter.plot('data', 'os/p1p2p3/prescale', styler=make_styler(1))
    plotter.save('zmm-os-prescale-check')

    plotter.plot('Zjets_M50', 'os/p1p2f3/weight')
    plotter.save('zmm-mc-event-weights')
    # Check MC weights
    plotter.plot('Zjets_M50', 'os/p1p2f3/weight_nopu')
    plotter.save('zmm-mc-event-weight_nopu')


    ###########################################################################
    ##  FR sideband MC-vs-Data ################################################
    ###########################################################################

    plotter.plot_mc_vs_data('ss/p1f2p3', 'e1Pt', rebin=10, xaxis='e_{1} p_{T} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-p1f2p3-e1Pt')

    plotter.plot_mc_vs_data('ss/p1f2p3', 'subMass', rebin=10, xaxis='m_{e2#tau} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-p1f2p3-subMass')

    plotter.plot_mc_vs_data('ss/p1f2p3/w2', 'e1Pt', rebin=10, xaxis='e_{1} p_{T}', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-p1f2p3-w2-e1Pt')

    plotter.plot_mc_vs_data('ss/f1p2p3', 'subMass', rebin=20, xaxis='m_{e2#tau} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-f1p2p3-subMass')

    plotter.plot_mc_vs_data('ss/f1p2p3/w1', 'subMass', rebin=20, xaxis='m_{e2#tau} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-f1p2p3-w1-subMass')

    plotter.plot_mc_vs_data('ss/p1p2f3', 'e1e2Mass', rebin=10, xaxis='m_{ee} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-p1p2f3-e1e2Mass')



    ###########################################################################
    ##  Signal region plots    ################################################
    ###########################################################################

    plotter.plot_final('e1Pt', 10)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-e1Pt')

    plotter.plot_final('e2Pt', 10)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-e2Pt')

    plotter.plot_final('tPt', 10)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-tPt')

    #plotter.plot_final('e1AbsEta', 10)
    #plotter.add_cms_blurb(sqrts)
    #plotter.save('final-e1AbsEta')

    #plotter.plot_final('e2AbsEta', 10)
    #plotter.add_cms_blurb(sqrts)
    #plotter.save('final-e2AbsEta')

    plotter.plot_final('tAbsEta', 10)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-tAbsEta')

    plotter.plot_final('subMass', 20, xaxis='m_{e_{2}#tau} (GeV)')
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-subMass')

    plotter.plot_final('e1tMass', 20, xaxis='m_{e_{1}#tau} (GeV)')
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-e1tMass')

    plotter.plot_final('e1e2Mass', 20, xaxis='m_{ee} (GeV)')
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-e1e2Mass')

    plotter.plot_final('tAbsEta', 5, xaxis='|#eta_#tau|')
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-tAbsEta')

    plotter.plot_final('e2Iso', 10)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-e2Iso')

    plotter.plot_final('metSig', 5)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-metSig')

    plotter.plot_final('LT', 5)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-LT')


    ###########################################################################
    ##  Making shape file     #################################################
    ###########################################################################

    shape_file = ROOT.TFile(
        os.path.join(outputdir, 'eet_shapes_%s.root' % period), 'RECREATE')
    shape_dir = shape_file.mkdir('eet')
    plotter.write_shapes('subMass', 20, shape_dir)
    shape_file.Close()


