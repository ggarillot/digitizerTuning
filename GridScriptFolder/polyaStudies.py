#!/usr/bin/env python

import gfal2
import os
import sys
import time

sys.path.insert(0 , '/gridgroup/ilc/garillot/MarlinReco/script')
sys.path.insert(0 , '/gridgroup/ilc/garillot/SDHCALMarlinProcessor/script')

import SimDigital
import EfficiencyProcessor

def download(input , output) :

	# Instantiate gfal2
	ctx = gfal2.creat_context()

	# Set transfer parameters
	params = ctx.transfer_parameters()
	params.overwrite = True
	params.timeout = 300

	dlCounter = 0
	isOK = False

	print 'Try to Download ' + input
	while not isOK and dlCounter < 50 :
		source = input
		destination = output
		try :
			r = ctx.filecopy(params, source, destination)
			isOK = True
		except Exception, e :
			print "Download failed : %s" % str(e)
			isOK = False
			time.sleep(20)

		dlCounter = dlCounter + 1
		
	if isOK :
		print 'Download succeeded !'
	else :
		print 'Download failed !'
		sys.exit(1)


def upload(input , output) :

	# Instantiate gfal2
	ctx = gfal2.creat_context()

	# Set transfer parameters
	params = ctx.transfer_parameters()
	params.overwrite = True
	params.timeout = 300

	dlCounter = 0
	isOK = False

	print 'Try to Upload ' + input
	while not isOK and dlCounter < 50 :
		source = input
		destination = output
		try:
			r = ctx.filecopy(params, source, destination)
			isOK = True
		except Exception, e:
			print "Upload failed : %s" % str(e)
			isOK = False
			time.sleep(20)

		dlCounter = dlCounter + 1

	if isOK :
		print 'Upload succeeded !'
	else :
		print 'Upload failed !'
		sys.exit(1)


if __name__ == '__main__' :

	if len(sys.argv) < 3 :
		sys.exit('Error : too few arguments')

	qbar = sys.argv[1]
	delta = sys.argv[2]

	dList = [ str(0.025) , str(0.04) , str(0.05) , str(0.07) , str(0.075) , str(0.1) , str(0.12) , str(0.125) , str(0.15) , str(0.17) , str(0.175) , str(0.2) , str(0.25) , str(0.27) , str(0.3) , str(0.4) , str(0.45) , str(0.5) , str(0.6) , str(0.65) , str(0.7) , str(0.8) , str(0.85) , str(0.9) , str(1) ]
    

	fileNameMu = 'single_mu-_50GeV_I1.slcio'
	sourceFileMu = 'root://lyogrid06.in2p3.fr/dpm/in2p3.fr/home/calice/garillot/PolyaStudies/SimCalorimeterHit/' + fileNameMu

	download( sourceFileMu , 'file:' + fileNameMu )

	fileListMu = [ fileNameMu ]

	digitParams = SimDigital.Params()
	digitParams.analog = True

	digitParams.splitterOption = 'ExactPerAsic'
	digitParams.dMap = 'map.root'

	digitParams.effOption = 'Uniform'
	digitParams.effValue = '1.0'

	digitParams.polyaOption = 'PerAsic'
	digitParams.polyaMap = 'map.root'

	digitParams.maxRecordNumber = 100000


	effProcParams = EfficiencyProcessor.Params()
	effProcParams.collectionName = 'HCALEndcapAnalog'
	effProcParams.thresholds = '0.114 0.14 0.155714 0.171429 0.187143 0.202857 0.218571 0.234286 0.25 0.265714 0.281429 0.298571 0.314286 0.33 0.345714 0.361429 0.377143 0.392857 0.408571 0.424286 0.4 0.6125 0.825 1.0375 1.2375 1.45 1.6625 1.875 2.0875 2.3 2.5 2.7125 2.925 3.1375 3.35 3.5625 3.7625 3.975 4.1875 4.29448 5.33742 6.38037 7.48466 8.52761 9.57055 10.6135 11.6564 12.6994 13.8037 14.8466 15.8896 16.9325 17.9755 19.0184 20.0613 21.1656 22.2086 23.2515'


	for d in dList :
		#create map
		os.system('./createMap ' + str(qbar) + ' ' + str(delta) + ' ' + str(d))
		
		#digit
		os.environ["MARLIN"] = '/gridgroup/gridsoft/ipnls/ilc/v01-17-09/Marlin/v01-08'
		os.environ["PATH"] = '/gridgroup/gridsoft/ipnls/ilc/v01-17-09/Marlin/v01-08/bin' + ':' + os.environ["PATH"]
		os.environ["MARLIN_DLL"] = '/gridgroup/ilc/garillot/MarlinReco/lib/libMarlinReco.so'

		digitParams.outputFileName = str(qbar) + '_' + str(delta) + '_' + str(d) + '.slcio'
		SimDigital.launchDigit(digitParams , fileListMu)
		os.system('rm aida.root')

		#efficiency analysis
		fileListForAnalysis = [ digitParams.outputFileName ]

		os.environ["MARLIN"] = '/gridgroup/gridsoft/ipnls/ilc/v01-17-08/Marlin/v01-07'
		os.environ["PATH"] = '/gridgroup/gridsoft/ipnls/ilc/v01-17-08/Marlin/v01-07/bin' + ':' + os.environ["PATH"]
		os.environ["MARLIN_DLL"] = '/gridgroup/ilc/garillot/SDHCALMarlinProcessor/lib/libsdhcalMarlin.so'

		effProcParams.outputFileName = 'map_' + qbar + '_' + delta + '_' + d + '.root'
		EfficiencyProcessor.launch(effProcParams , fileListForAnalysis)
  
		#polya fit
		os.system('./fitSim ' + effProcParams.outputFileName)

		outputFileName = 'Fit_' + qbar + '_' + delta + '_' + d + '.root'
		outputFile = 'root://lyogrid06.in2p3.fr/dpm/in2p3.fr/home/calice/garillot/PolyaStudies/Fits/' + outputFileName
  
		upload('file:' + 'Fit.root' , outputFile)
  
 		os.system('rm ' + 'Fit.root')
		os.system('rm ' + effProcParams.outputFileName)
		os.system('rm ' + digitParams.outputFileName)
