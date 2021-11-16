#!/usr/bin/env python

import os
import sys

class Params :
	def __init__(self) :
		self.analog = False
		self.thr = '0.114 6.12 16.83'

		self.polyaOption = 'Uniform'
		self.polyaQ = 5.55942
		self.polyaD = 2.42211
		self.polyaMap = ''

		self.effOption = 'Uniform'
		self.effValue = 0.96
		self.effMap = ''

		self.splitterOption = 'Exact'
		self.d = 0.221368
		self.dMap = ''

		self.dCut = 0.5
		self.angleCorr = 0.55

		self.range = 60

		self.outputFileName = 'lcio.slcio'
		self.maxRecordNumber = 0

		#oldCalib
		self.erfWidth = ''
		self.erfWeight = ''

	def oldCalib(self) :
		self.thr = '0.114 5.4 14.5'

		self.polyaOption = 'Uniform'
		self.polyaQ = 4.58
		self.polyaD = 2.16

		self.effOption = 'Uniform'
		self.effValue = 0.96
		self.effMap = ''

		self.splitterOption = 'Erf'
		self.erfWidth = '1.0 9.7'
		self.erfWeight = '1.0 0.00083'

		self.dCut = 0.5
		self.angleCorr = 0.55

		self.range = 30



def launchDigit(a , files) :

	if a.maxRecordNumber == 0 :
		maxRecordNumber = ''

	colname = ''
	doThresholds = ''
	if a.analog :
		doThresholds = 'false'
		colname = 'HCALEndcapAnalog'
	else :
		doThresholds = 'true'
		colname = 'HCALEndcap'


	fileList = ''
	for name in files :
		fileList += name + ' '

	pid = os.getpid()

	steerFileName = 'digitSteer' + str(pid) + '.xml'

	steerXml = '''<marlin xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://ilcsoft.desy.de/marlin/marlin.xsd">
 <execute>
  <processor name="MyAIDAProcessor"/>
  <processor name="MySimDigital"/>
  <processor name="MySimDigitalLinkToParticles"/>
  <processor name="MyLCIOOutputProcessor"/>
 </execute>

 <global>
  <parameter name="LCIOInputFiles">
   ''' + fileList + '''
  </parameter>
  <!-- limit the number of processed records (run+evt): -->
  <parameter name="MaxRecordNumber" value="''' + str(a.maxRecordNumber) + '''" />
  
  <parameter name="SkipNEvents" value="0" />
  <parameter name="SupressCheck" value="false" />
  <parameter name="Verbosity" options="DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT"> MESSAGE </parameter>
  <parameter name="RandomSeed" value="1234567890" />
 </global>

 <processor name="MyLCIOOutputProcessor" type="LCIOOutputProcessor">
 <!--Writes the current event to the specified LCIO outputfile. Needs to be the last ActiveProcessor.-->

  <!--drops all collections of the given type from the event-->
  <parameter name="DropCollectionNames" type="StringVec"> SDHCAL_Proto_EndCap particleGenericObject RelationCaloHit </parameter>

  <!-- name of output file -->
  <parameter name="LCIOOutputFile" type="string">''' + a.outputFileName + '''</parameter>
 
  <!--write mode for output file:  WRITE_APPEND or WRITE_NEW-->
  <parameter name="LCIOWriteMode" type="string"> WRITE_NEW </parameter>

  <!--verbosity level of this processor ("DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT")-->
  <!--parameter name="Verbosity" type="string"> MESSAGE </parameter-->
</processor>


 <processor name="MyAIDAProcessor" type="AIDAProcessor">
 <!--Processor that handles AIDA files. Creates on directory per processor.  Processors only need to create and fill the histograms, clouds and tuples. Needs to be the first ActiveProcessor-->
  <!-- compression of output file 0: false >0: true (default) -->
  <parameter name="Compress" type="int">1 </parameter>
  <!-- filename without extension-->
  <parameter name="FileName" type="string"> aida </parameter>
  <!-- type of output file root (default) or xml )-->
  <parameter name="FileType" type="string"> root </parameter>
  <!--verbosity level of this processor ("DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT")-->
  <!--parameter name="Verbosity" type="string">DEBUG </parameter-->
</processor>

<processor name="MySimDigital" type="SimDigital">
    <!--the transfer Between Induced Charge and Threshold for SDHCAL-->

	<parameter name="CellIDEncodingStringType" type="string"> PROTO </parameter>
	<parameter name="HCALCellSize" type="float"> 10.408 </parameter>

    <parameter name="inputHitCollections" type="StringVec" lcioInType="SimCalorimeterHit"> SDHCAL_Proto_EndCap </parameter>

	<!--parameter name="inputGenericCollections" type="StringVec" lcioInType="LCGenericObject"> particleGenericObject </parameter-->

    <parameter name="outputHitCollections" type="StringVec" lcioOutType="CalorimeterHit"> ''' + colname + ''' </parameter>
    <parameter name="outputRelationCollections" type="StringVec" lcioOutType="LCRelation"> RelationCaloHit </parameter>


    <!--Induced charge simulation parameters-->
	<parameter name="PolyaOption" type="string"> ''' + a.polyaOption + ''' </parameter>
	<parameter name="PolyaMapFile" type="string"> ''' + a.polyaMap + ''' </parameter>
	<!--Parameter for the Polya distribution used to simulate the induced charge distribution : mean of the distribution default = 5.596-->
	<parameter name="PolyaAverageCharge" type="double"> ''' + str(a.polyaQ) + ''' </parameter>
	<!--Parameter for the Polya distribution used to simulate the induced charge distribution : related to the distribution width default = 1.021-->
	<parameter name="PolyaWidthParameter" type="double"> ''' + str(a.polyaD) + ''' </parameter>


    <!--Induced charge dispatching parameters-->
    <!--Induced charge dispatching : which steps to use parameters-->
    <!--Maximum distance (mm) between the Geant4 step position and the cell center, in the RPC width direction, to keep a step for digitization. Default value=0.0005-->
    <parameter name="StepCellCenterMaxDistanceLayerDirection" type="float"> 0.0005 </parameter>
    <!--if true, ensure that each hit will keep at least one step for digitisation independatly of filtering conditions (StepCellCenterMaxDistanceLayerDirection)-->
    <parameter name="KeepAtLeastOneStep" type="bool"> true </parameter>
    <!--Minimum distance (mm) between 2 Geant4 steps, in the RPC plane, to keep the 2 steps. Default value=0.5-->
    <parameter name="StepsMinDistanceRPCplaneDirection" type="float"> ''' + str(a.dCut) + ''' </parameter>


    <!--Induced charge dispatching : dispatching mode-->
    <!-- Define the charge splitter method. Possible option : Erf , Exact , ExactPerAsic -->
	<parameter name="ChargeSplitterOption" type="string"> ''' + a.splitterOption + ''' </parameter>
	  <parameter name="SpreaderMapFile" type="string"> ''' + a.dMap + ''' </parameter>

    <!--Induced charge dispatching : dispatching with function parameters-->
    <!--Width values for the different Erf functions-->
	<parameter name="erfWidth" type="FloatVec"> ''' + a.erfWidth + ''' </parameter>
	<!--Weigth for the different Erf functions-->
	<parameter name="erfWeigth" type="FloatVec"> ''' + a.erfWeight + ''' </parameter>

	<!-- d parameter if exact splitter -->
	<parameter name="ChargeSplitterd" type="double"> ''' + str(a.d) + ''' </parameter>


    <!--distance in mm between two RPC pads : used if UseFunctionForChargeSplitting is true -->
    <parameter name="RPC_PadSeparation" type="float"> 0.408 </parameter>
    <!--maximal distance (in mm) at which a step can induce charge using the 2D function defined with functionFormula-->
    <parameter name="functionRange" type="float"> ''' + str(a.range) + ''' </parameter>



	<!--Power factor for the step length saturation correction. Default value 0.5-->
	<parameter name="AngleCorrectionPower" type="float"> ''' + str(a.angleCorr) + ''' </parameter>
	<!--maximum time (ns) between the start of the event and the time when a step is detected. Default value 600-->
	<parameter name="TimeCut" type="int"> 1000 </parameter>
	<!--Minimal step length (mm) to take the step into account. Default value 0.1-->
	<parameter name="StepLengthCut" type="int"> 0.001 </parameter>


	<!--Step efficiency correction method : should be Uniform or PerAsic-->  
	<parameter name="EffMapOption" type="string"> ''' + a.effOption + ''' </parameter>
	<!--Value of the constant term for efficiency correction if EffMapOption==Uniform-->
	<parameter name="EffMapConstantValue" type="float"> ''' + str(a.effValue) + ''' </parameter>
	<!--File name where prototype efficiency correction is stored if EffMapOption==PerAsic-->
	<parameter name="EffMapFile" type="string"> ''' + a.effMap + ''' </parameter>



    <!--digitisation parameters-->
	<!--Threshold for HCAL Hits in pC-->
	<parameter name="HCALThreshold" type="FloatVec"> ''' + a.thr + ''' </parameter>
	<parameter name="doThresholds" type="bool"> ''' + doThresholds + ''' </parameter>

    <!--verbosity level of this processor ("DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT")-->
    <parameter name="Verbosity" type="string"> MESSAGE </parameter>


</processor><!-- MySimDigital -->

<processor name="MySimDigitalLinkToParticles" type="SimDigitalLinkToParticles">
    <parameter name="inputHitCollections" type="StringVec" lcioInType="CalorimeterHit"> ''' + colname + ''' </parameter>
	<parameter name="inputRelationCollections" type="StringVec" lcioInType="LCRelation"> RelationCaloHit </parameter>
    <parameter name="outputRelationCollections" type="StringVec" lcioOutType="LCRelation"> RelationParticleToHit </parameter>
</processor><!-- MySimDigitalLinkToParticles -->

</marlin>'''


	f = open(steerFileName , 'w')
	f.write(steerXml)
	f.close()

	os.system('Marlin ' + steerFileName)
	os.system('rm ' + steerFileName)
