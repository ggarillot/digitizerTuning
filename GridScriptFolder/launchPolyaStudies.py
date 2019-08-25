import os
import sys
import string
from Ganga import *

j=Job()
j.application = Executable(exe=File('/gridgroup/ilc/garillot/bigScripts/PolyaStudies/polyaStudies.py'), args=['arg1','arg2'])
j.backend='CREAM'
j.backend.CE='lyogrid07.in2p3.fr:8443/cream-pbs-calice'
j.comment = 'Polya Studies'
j.inputsandbox = ['/gridgroup/ilc/garillot/PolyaFit/bin/fitSim' , '/gridgroup/ilc/garillot/bigScripts/PolyaStudies/MapCreator/bin/createMap'];

def frange(x, y, jump) :
    while y >= x - 1e-10 :
        if abs( round(y,0)-y ) < 1e-10 :
            yield int( round(y,0) )
        else :
            yield y
        y -= jump

par=[]

args = [ [str(qbar) , str(delta)] for qbar in frange(0.25, 10, 0.25) for delta in frange(0.25, 4, 0.25) if qbar < 4*delta ]
args2 = [ [str(qbar) , str(delta)] for qbar in frange(8, 20, 0.5) for delta in frange(4, 12, 0.5) if qbar < 2*delta ]

args = args + args2

for i in args:
	par.append(i)

par
s = ArgSplitter()
s.args=par
j.splitter=s
j.submit()

for subj in j.subjobs :
	subjComment = ""
	for arg in subj.application.args :
		subjComment = subjComment + " " + str(arg)
	subj.comment = str(subjComment)
