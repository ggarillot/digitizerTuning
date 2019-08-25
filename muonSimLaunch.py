#!/usr/bin/env python

import os
import sys

sys.path.insert(0 , '/path/to/SDHCALSim/script')

import SDHCALSim as sim

import math

if __name__ == '__main__' :

	os.environ["SIMEXE"] = '/path/to/SDHCALSim/bin/SDHCALSim'

	params = sim.Params()
	params.physicsList = 'QGSP_BERT'
	params.nEvent = 100000
	params.seed = 0
	params.outputFileName = 'mu-_100GeV'
	
	charged = sim.Particle()
	charged.particleName = 'mu-'
	charged.energy = 100

	charged.momentumOption = 'gaus'
	charged.sigmaMomentum = 0.15

	charged.positionOption = 'uniform'
	charged.positionX = 0
	charged.positionY = 0
	charged.positionZ = -20  
	charged.uniformDeltaPos = 500

	params.particleList.append(charged)

	sim.launch( params )
