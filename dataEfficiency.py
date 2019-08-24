#!/usr/bin/env python

#CHANGE THE PATH ACCORDING TO YOUR INSTALLATION
pathToSDHCALMarlinProcessor = '/home/guillaume/SDHCALMarlinProcessor'

import os
import sys
from os import path
import time

sys.path.insert(0 , pathToSDHCALMarlinProcessor + '/script')

import EfficiencyProcessor

if __name__ == '__main__' :

	if len(sys.argv) < 2 :
		sys.exit('Error : too few arguments')

	runNumber = sys.argv[1]

    #CHANGE THIS DIRECTORY ACCORDING TO DATA FILES LOCATION
	dir = '/home/guillaume/files/DATA/TRIVENT/SPS_Oct2015'	

	print ('Searching files in ' + dir)

	#list files
	fileList = []

	for fileName in os.listdir(dir) :
		if runNumber in fileName :
			fileList.append(dir + '/' + fileName)

	print 'Filelist : '
	print fileList

    #CHANGE THIS LINE 
	os.environ["MARLIN"] = '/home/guillaume/ilcsoft/v02-00-01/Marlin/v01-16'

	os.environ["PATH"] = os.environ["MARLIN"] + '/bin:' + os.environ["PATH"]
	os.environ["MARLIN_DLL"] = pathToSDHCALMarlinProcessor + '/lib/libsdhcalMarlin.so'


	a = EfficiencyProcessor.Params()
	a.collectionName = 'SDHCAL_HIT'

    #ALSO CHANGE THIS LINE TO PUT THE CORRECT GEOMETRY
	a.geometry = pathToSDHCALMarlinProcessor + '/DifGeom/sdhcalOCT2015.json'

	a.outputFileName = 'Eff_' + runNumber + '.root'

	EfficiencyProcessor.launch(a , fileList)

    #YOU MAY WANT TO CHANGE THIS TOO
	outputDir = dir.replace('DATA/TRIVENT' , 'MultiplicityMap/DATA')

	os.system('mkdir -p ' + outputDir)
	os.system('mv ' + a.outputFileName + ' ' + outputDir + '/' + a.outputFileName)