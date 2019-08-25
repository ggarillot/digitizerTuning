# Digitization and uniformed states : How to


### Requirements :

* Softwares :
    * [iLCSoft](https://github.com/iLCSoft/iLCInstall)
    * [SDHCALSim](https://github.com/SDHCAL/SDHCALSim)
    * [SDHCALMarlinProcessor](https://github.com/ggarillot/SDHCALMarlinProcessor) which needs [CaloSoftWare](https://github.com/ggarillot/CaloSoftWare)
    * [PolyaFit](https://github.com/ggarillot/PolyaFit)
    * [MarlinReco](https://github.com/iLCSoft/MarlinReco) - automatically installed with iLCSoft

* Perform a complete muon scan

In my case I used the muon scan performed in October 2015, here are the list of runs :

|  Run   | DAC0 | DAC1 | DAC2 |
|:------:|:----:|:----:|:----:|
| 730630 | 188  | 130  | 168  | 
| 730627 | 199  | 147  | 185  | 
| 730626 | 210  | 164  | 202  | 
| 730625 | 221  | 181  | 220  | 
| 730619 | 232  | 197  | 237  | 
| 730618 | 243  | 214  | 254  | 
| 730617 | 254  | 231  | 271  | 
| 730616 | 265  | 248  | 288  | 
| 730615 | 276  | 265  | 305  | 
| 730611 | 287  | 282  | 323  | 
| 730609 | 299  | 298  | 340  | 
| 730607 | 310  | 315  | 357  | 
| 730569 | 321  | 332  | 374  | 
| 730568 | 332  | 349  | 391  | 
| 730567 | 343  | 366  | 408  | 
| 730566 | 354  | 383  | 425  | 
| 730631 | 365  | 399  | 443  | 
| 730633 | 376  | 416  | 460  | 
| 730545 | 387  | 433  | 477  | 
| 730677 | 170  | 498  | 342  | 

(The 730677 run is a 80GeV pion run but it still has a lot of muons)

### Objectives :

* Create an uniformed state for the SDHCAL (uniformed multiplicities and efficiencies)
* Reproduce the non-uniformities in the digitization process

---

## Create an uniformized state for the SDHCAL

### Procedure : 

1. Perform a muon scan
    * As the conditions / configurations / RPCs degradation changes between different beam tests you will have to perform a new muon scan for each test beam if you plan to create an unifomized state
2. Compute the efficiencies / multiplicities for all the runs of the muon scan
3. Adjust the efficiencies versus threshold and multiplicities versus threshold with analytical formulas
4. Create a new database state by asking a certain value of multiplicity and efficiency of 2nd and 3rd thresholds

### Compute the efficiencies / multiplicies for a given run :

Create a `.json` file which describes the configuration of the SDHCAL (DIFs location). You can find existing `.json` files for previous configurations in the `SDHCALMarlinProcessor/DifGeom` folder.

Modify the `dataEfficiency.py` file according to your installation, location of data files and geometry (lines 3, 23, 38, 48 and 55)

Run the `dataEfficiency.py` script for the given run number (example run 730677): 

```shell
chmod +x dataEfficiency
./dataEfficiency.py 730677
```

This produces a `.root` file with a big `TTree` which contains the computed efficiencies and multiplicities (and associated errors) for the three thresholds and for all the layers / DIFs / ASICs / pads.

Example : if you want to access the efficiency for the pad 41 of the ASIC 8 of the DIF 112 : 

    root [] tree->Scan("Efficiencies[0]:Ntrack","DifID==112 && AsicID==8 && PadID==41")
    ************************************
    *    Row   * Efficienc *    Ntrack *
    ************************************
    *   409259 *    0.9375 *        16 *
    ************************************

`Efficiencies[0]` means the efficiencies for the first threshold, you can access second and third thresholds with `Efficiencies[1]` and `Efficiencies[2]` respectively.
`Ntrack` is the statistics (here the efficiency is computed using 16 tracks)

If you want to access the efficiency for the whole ASIC instead you have to put "`PadID==-1`": 

    root [] tree->Scan("Efficiencies[0]:Ntrack","DifID==112 && AsicID==8 && PadID==-1")
    ************************************
    *    Row   * Efficienc *    Ntrack *
    ************************************
    *   409282 * 0.9709702 *      1309 *
    ************************************

Example : Multiplicity for a whole layer : 

    root [] tree->Scan("Multiplicities[0]:Ntrack","LayerID==7 && AsicID==-1")
    ************************************
    *    Row   * Multiplic *    Ntrack *
    ************************************
    *    74887 * 1.5534775 *    178851 *
    ************************************


Example : Efficiency of third threshold for the whole detector : 

    root [] tree->Scan("Efficiencies[2]:Ntrack","LayerID==-1")
    ************************************
    *    Row   * Efficienc *    Ntrack *
    ************************************
    *   458689 * 0.0284023 *   8328716 *
    ************************************



### Adjust the efficiencies and multiplicies versus the threshold :

Once you ran `dataEfficiency.py` for all the runs you have to use the `PolyaFit` package to adjust the efficiencies and multiplicities. You will have the pleasure to notice that this package does not contains any form of documentation nor readable code. 

To install : 

```shell
git clone https://github.com/ggarillot/PolyaFit
cd PolyaFit
mkdir build ; cd build
cmake -C $ILCSOFT/ILCSOFT.cmake
make -j8 install
```

You have to create a `.json` file which contains the list of the runs from the scan and their corresponding thresholds - in DAC values. You can find examples in the `PolyaFit/json` folder.

To draw the efficiency / multiplicity versus threshold for all the ASICs and layers you can run this (example in my case): 

```shell
./bin/drawData json/SPS_Oct2015.json
```

The program looks like it is stuck and will never finish at some point (at the "`Write canvas`" step, but it is not the case (I never found out why). When it is finished you have a big file named `drawData.root` full of curves like this : 

<div align="center">
    <img src="./images/EffVsThrEx1.png" alt="Efficiency" width="300"/>
    <img src="./images/MulVsThrEx1.png" alt="Multiplicity" width="300"/>
</div>

If you study the October 2015 runs you will notice that the fits for the layer 47 fails because of the weird behaviour of the electronics : 

<div align="center">
    <img src="./images/EffVsThrShit.png" alt="EffVsThrShit" width="400"/>
</div>

So in this case you can uncomment the lines 313/314 of the `PolyaFit/src/GraphManager.cpp` : 

```cpp
if ( i != mulRef && layerID == 47 )
    c = 1 ;
```

in order to have good fits : 

<div align="center">
    <img src="./images/EffVsThrLessShit.png" alt="EffVsThrLessShit" width="400"/>
</div>

If you only want to compute the fit parameters you have to run this (example in my case : )

```shell
./bin/fit json/SPS_Oct2015.json
```
This outputs a file named `resData.root` containing only the fit parameters in a `TTree`

### Create a new database state :

To create a new database state you have to use the `bin/findThr` program and choose a target multiplicity and target efficiencies of second and third threshold.

Example : if you want to create a state with a target multiplicity of `1.7`, a second threshold efficiency of `80%` and a third threshold efficiency of `2.5%` : 

```shell
./bin/findThr resData.root 1.7 0.8 0.025
```

This outputs two files : `targetThr.root` and `changeThr.py`. 

The `targetThr.root` file contains the thresholds (in pC and DAC values) of this new state. 

The `changeThr.py` is the python script to launch to upload the new state on the database. You have to change the reference state at the line 2.

---

## Tuning of the digitizer to reproduce non-uniformities

### Procedure : 

1. Perform or use a muon scan
2. Create a simulated muon sample
3. Launch a lot of digitizations for this sample with different set of parameters
4. After the digitization, for each set of parameter : 
    * Compute the efficiencies / multiplicities (SDHCALMarlinProcessor)
    * Adjust the efficiencies and multiplicities curve (PolyaFit)
5. Create and train a neural network 
6. Apply the trained neural network on the muon scan DATA
7. Compare with simulation

### Create a simulated muon sample

You can launch the `muonSimLaunch.py` script to generate the muon sample. Make sure to change the lines 6 and 14 according to your installation. This will output two files : `mu-_100GeV.slcio` and `mu-_100GeV.root`. Only the `.slcio` file is useful to go further.

### The digitization

To tune the digitizer to reproduce efficiency and multiplicity I played with three parameters : 
* q and delta, related to the charge inducing
* d related to the charge spreading

A manual tuning for all the ~7000 ASICs would take too much time, so I decided to use a neural network instead. To train this neural network, I launched a lot of digitizations with different sets of {q,delta,d}.

The choosen sets were : 
* q from 0.25 to 10 with steps of 0.25 and delta from 0.25 to 4 with steps of 0.25 and q < 4 * delta
* q from 8 to 20 with steps of 0.5 and delta from 4 to 12 with steps of 0.5 and q < 2 * delta
* d : {0.025, 0.04, 0.05, 0.07, 0.075, 0.1, 0.12, 0.125, 0.15, 0.17, 0.175, 0.2, 0.25, 0.27, 0.3, 0.4, 0.45, 0.5, 0.6, 0.65, 0.7, 0.8, 0.85, 0.9, 1}

for a grand total of 17650 different sets. This may be a bit too much but I didn't try to train the network with less or more points because I was satisfied with the results after the first try.

As this three parameters changes, the cluster sizes of the digitized tracks will also changes. The problem is that the track reconstuction algorithm is not very consistent with the cluster size changes. For extreme parameters cases (for example d = 1), the average cluster size can reach something like 8 (or maybe more), so if we apply this parameter to the whole SDHCAL, the track algorithm will never reconstruct any track, because too big clusters are not considered as a potential track cluster for the algorithm.

The compromise I choose is to change only the parameters for a certain layer (I choose the layer 25 because it is in the middle of the detector), and keep the default parameters for all the other layers. In this case, the track algorithm will reconstruct the tracks as usual, the clusters from the layer 25 may not always be uncluded in the tracks (if they are too large), but it doesn't matter because they will still be taken into account in the efficiency / multiplicity calculation for this layer.

So, before launching the digitization, I create the parameters input by using the simple `createMap` program in the `MapCreator/` folder. As you can see it is short and straight-forward, it just create a `TTree` with one entry for the whole layer 25 (note the `AsicID = -1`) with the desired set of parameters. This outputs the desired `map.root` input file. The digitizer will not care if it does not found the information for the other layers, it puts the default parameters for the layers without information.

As the number of sets is huge, I ran all the digitizations on the grid. The scripts I ran are in the `GridScriptFolder/` folder. The `launchPolyaStudies.py` is for the job submission, and the `polyaStudies.py` is the job itself.

The `polyaStudies.py` file needs some explanations : 

The 
```python
def download(input , output) :
```
and
```python
def upload(input , output) :
```
are just my functions to download/upload stuff at the storage system 

```python
if __name__ == '__main__' :

	if len(sys.argv) < 3 :
		sys.exit('Error : too few arguments')

	qbar = sys.argv[1]
	delta = sys.argv[2]

	dList = [ str(0.025) , str(0.04) , str(0.05) , str(0.07) , str(0.075) , str(0.1) , str(0.12) , str(0.125) , str(0.15) , str(0.17) , str(0.175) , str(0.2) , str(0.25) , str(0.27) , str(0.3) , str(0.4) , str(0.45) , str(0.5) , str(0.6) , str(0.65) , str(0.7) , str(0.8) , str(0.85) , str(0.9) , str(1) ]
```
Here you can see that a job needs two parameters, `qbar` and `delta`, and it will loop on all the `dList` values (this would have taken too much jobs if I ran one job for each {q,delta,d} set).

```python
    fileNameMu = 'single_mu-_50GeV_I1.slcio'
    sourceFileMu = 'root://lyogrid06.in2p3.fr/dpm/in2p3.fr/home/calice/garillot/PolyaStudies/SimCalorimeterHit/' + fileNameMu

    download( sourceFileMu , 'file:' + fileNameMu )

    fileListMu = [ fileNameMu ]
```

Here I download the simulated muon sample from the storage

```python
    digitParams = SimDigital.Params()
    digitParams.analog = True

    digitParams.splitterOption = 'ExactPerAsic'
    digitParams.dMap = 'map.root'

    digitParams.effOption = 'Uniform'
    digitParams.effValue = '1.0'

    digitParams.polyaOption = 'PerAsic'
    digitParams.polyaMap = 'map.root'

    digitParams.maxRecordNumber = 100000
```
Here I set the parameters for the digitizer. It is very important to put the `digitParams.analog` to `True`. The `map.root` file is the name of the input file generated by the `createMap` program (the job will run this after).

```python
    effProcParams = EfficiencyProcessor.Params()
    effProcParams.collectionName = 'HCALEndcapAnalog'
    effProcParams.thresholds = '0.114 0.14 0.155714 0.171429 0.187143 0.202857 0.218571 0.234286 0.25 0.265714 0.281429 0.298571 0.314286 0.33 0.345714 0.361429 0.377143 0.392857 0.408571 0.424286 0.4 0.6125 0.825 1.0375 1.2375 1.45 1.6625 1.875 2.0875 2.3 2.5 2.7125 2.925 3.1375 3.35 3.5625 3.7625 3.975 4.1875 4.29448 5.33742 6.38037 7.48466 8.52761 9.57055 10.6135 11.6564 12.6994 13.8037 14.8466 15.8896 16.9325 17.9755 19.0184 20.0613 21.1656 22.2086 23.2515'
```

Here I set the parameters for the efficiency / multiplicity calculation (SDHCALMarlinProcessor). You can see that I put a list of thresholds that corresponds (in my case), to the used thresholds of the muon scan runs (converted from DAC values to pC).

```python
    for d in dList :
        #create map
        os.system('./createMap ' + str(qbar) + ' ' + str(delta) + ' ' + str(d))
```
Here the loops on the d parameter begins. First, the `map.root` input file is generated.

```python
        #digit
        os.environ["MARLIN"] = '/gridgroup/gridsoft/ipnls/ilc/v01-17-09/Marlin/v01-08'
        os.environ["PATH"] = '/gridgroup/gridsoft/ipnls/ilc/v01-17-09/Marlin/v01-08/bin' + ':' + os.environ["PATH"]
        os.environ["MARLIN_DLL"] = '/gridgroup/ilc/garillot/MarlinReco/lib/libMarlinReco.so'

        digitParams.outputFileName = str(qbar) + '_' + str(delta) + '_' + str(d) + '.slcio'
        SimDigital.launchDigit(digitParams , fileListMu)
        os.system('rm aida.root')
```
Here, you have a bunch of paths that you need to change according to your installation. You can use the official `libMarlinReco.so` (the official MarlinReco contains all the improvements of the digitizer now). The digitization is launched with the parameters we previously defined. We get rid of the unused `aida.root` file (it is mainly used for debugging).

```python
        #efficiency analysis
        fileListForAnalysis = [ digitParams.outputFileName ]

        os.environ["MARLIN"] = '/gridgroup/gridsoft/ipnls/ilc/v01-17-08/Marlin/v01-07'
        os.environ["PATH"] = '/gridgroup/gridsoft/ipnls/ilc/v01-17-09/Marlin/v01-08/bin' + ':' + os.environ["PATH"]
        os.environ["MARLIN_DLL"] = '/gridgroup/ilc/garillot/SDHCALMarlinProcessor/lib/libsdhcalMarlin.so'

        effProcParams.outputFileName = 'map_' + qbar + '_' + delta + '_' + d + '.root'      
        EfficiencyProcessor.launch(effProcParams , fileListForAnalysis)
```
Here the efficiencies and the multiplicities are computed as described [previously](#compute-the-efficiencies-multiplicies-for-a-given-run)

```python
        #polya fit
        os.system('./fitSim ' + effProcParams.outputFileName)
```
Then, the efficiencies are adjusted as described [previously](#adjust-the-efficiencies-and-multiplicies-versus-the-threshold). The `fitSim` program does the same stuff that the `fit` program, but takes a simulation file instead of a list of DATA files from a `.json` file.

```python 
        outputFileName = 'Fit_' + qbar + '_' + delta + '_' + d + '.root'
        outputFile = 'root://lyogrid06.in2p3.fr/dpm/in2p3.fr/home/calice/garillot/PolyaStudies/Fits/' + outputFileName
        upload('file:' + 'Fit.root' , outputFile)
  
        os.system('rm ' + 'Fit.root')
        os.system('rm ' + effProcParams.outputFileName)
        os.system('rm ' + digitParams.outputFileName)
```
Then I upload the result file on the storage system and I delete the intermediate files. Note that I didn't upload the output file from the digitizer, because if I did so, for all the jobs, it would have taken around 2TB of disk space.

## The neural network

Once we have the fits for all the parameters sets {q,delta,d}, we can train our neural network. First we have to create two `.root` files, one file containing a `TTree` for the training set, and one containing a `TTree` for the testing set. It is done by the `createTree.C` macro in the `NN/` folder

```shell
    root -l createTree.C 
    root [0] 
    Processing createTree.C...
    root [1] createTree()
```
You have to change the path line 46 according to the location of your files. You can see line 13 that I load a `.txt` file. I don't remember what it contains but according to the code it is just a plain text file containing all the sets of parameters so the code can loop on it to open the corresponding files. I don't have the python script to generate this .txt file anymore but it should be easy to recreate.

You now have two `.root` files : `tree.root` and `treeTest.root`, and you can train your neural network.

You first have to change the paths on line 45 and 46 of the `NN/src/TMVARegression.cxx` and line 80 of the file `NN/src/TMVARegressionApplication.cxx` according to the location of your files, then you can compile as usual

```shell
mkdir build ; cd build
cmake -C $ILCSOFT/ILCSOFT.cmake
make -j2 install
```

To train the network you have to run

```shell
./bin/TMVARegression
```
I cannot test it the network trains fine as I don't have all the fits files anymore. Once the training has finished it should have created a `weights/` folder containing the weights of the trained network.

By doing this, you have created a network that can, from desired multiplicities and efficiencies (q and delta), compute the input parameter to give to the digitizer in order from it to produce a simulation file that matches this desired multiplicities and efficiencies.

Then, you have to run

```shell
./bin/TMVARegressionApplication
```
to apply this network on desired multiplicities and efficiencies from the data (the `resData.root` produced by the `PolyaFit/bin/fit` program).

You now have a `map.root` file that you can input to the digitizer in order to take into account the non-uniformities of the detector by using its options like this: 

```python
    digitParams = SimDigital.params()
    digitParams.splitterOption = 'ExactPerAsic'
    digitParams.dMap = 'map.root'
    digitParams.polyaOption = 'PerAsic'
    digitParams.polyaMap = 'map.root'
```

In order to reproduce a certain standard run (standard thresholds 0.114, 5, 15 pC), you also need to pass this option

```python
    digitParams.effOption = 'PerAsic'
    digitParams.effMap = '/path/to/your/files/Eff_730716.root'
```
If you want to reproduce results from the run 730716 for example. To generate such a file, you just have to follow [this section](#compute-the-efficiencies-multiplicies-for-a-given-run).

In the `SimDigitalScript/` folder you can find a simple example script `digitOnLocal.py` to know how to launch the digitization. The default parameters are indicated in the `SimDigital.py` file.

## Compare simulation / data

In progress...





