#!/usr/bin/env python

import os
import sys
from os import path
import time

import SimDigital

if __name__ == '__main__' :

	fileList = ['/path/to/simOutput/sim1.slcio','/path/to/simOutput/sim2.slcio']

	a = SimDigital.Params()

	a.outputFileName = 'outputFilename.slcio'
	

	#options to uncomment to enable reproduction of non-homogeneity (tuned with October 2015 SPS DATA)
	#a.polyaOption = 'PerAsic'
	#a.polyaMap = '/path/to/Polya_730677.root'
	#a.splitterOption = 'ExactPerAsic'
	#a.dMap = a.polyaMap

	#uncomment to reproduce efficiency map of a certain runNumber
	#a.effOption = 'PerAsic'
	#a.effMap = '/path/to/EfficiencyMap/Eff_runNumber.root'		
	
	SimDigital.launchDigit(a , fileList)

	os.system('rm aida.root')

