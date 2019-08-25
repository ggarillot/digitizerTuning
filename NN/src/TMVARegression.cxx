#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <sstream>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#include "TMVA/DataLoader.h"

int main( int argc, char** argv )
{
	std::cout << std::endl ;
	std::cout << "==> Start TMVARegression" << std::endl ;

	// --- Here the preparation phase begins

	TString outfileName( "TMVAReg.root" ) ;
	TFile* outputFile = TFile::Open( outfileName, "RECREATE" ) ;

	TMVA::Factory *factory = new TMVA::Factory( "TMVARegression", outputFile, "!V:!Silent:Color:DrawProgressBar" ) ;

	TMVA::DataLoader* dataloader = new TMVA::DataLoader("dataset") ;

	// Define the input variables that shall be used for the MVA training

	dataloader->AddVariable("outQbar" , 'F') ;
	dataloader->AddVariable("outDelta" , 'F') ;
	dataloader->AddVariable("mul" , 'F') ;

	dataloader->AddTarget("inQbar") ;
	dataloader->AddTarget("inDelta") ;
	dataloader->AddTarget("d") ;
	
	dataloader->AddTarget( "energy" ) ;
		
	TFile* trainFile = TFile::Open("/home/garillot/Code/PolyaStudies/tree.root") ;
	TFile* testFile = TFile::Open("/home/garillot/Code/PolyaStudies/treeTest.root") ;

	if ( !trainFile || !testFile )
	{
		std::cerr << "ERROR : could not open data file" << std::endl ;
		exit(1) ;
	}

	TTree* trainTree = dynamic_cast<TTree*>( trainFile->Get("tree") ) ;
	TTree* testTree = dynamic_cast<TTree*>( testFile->Get("tree") ) ;

	// global event weights per tree (see below for setting event-wise weights)
	Double_t regWeight  = 1.0 ;

	// You can add an arbitrary number of regression trees
	dataloader->AddRegressionTree( trainTree , regWeight , TMVA::Types::kTraining ) ;
	dataloader->AddRegressionTree( testTree , regWeight , TMVA::Types::kTesting ) ;

	// This would set individual event weights (the variables defined in the
	// expression need to exist in the original TTree)
	//   factory->SetWeightExpression( "var1", "Regression" ) ;

	// Apply additional cuts
	TCut mycut = "" ;

	// tell the factory to use all remaining events in the trees after training for testing:
	dataloader->PrepareTrainingAndTestTree( mycut, "MixMode=Random:NormMode=NumEvents:!V" ) ;
	//factory->PrepareTrainingAndTestTree( mycut, "nTrain_Regression=18400:nTest_Regression=73600:SplitMode=Block:NormMode=NumEvents:!V" ) ;

	const char* nCycles = "3000" ;
	const char* networkStructure = "10,10,10" ;
	const char* batchSize = "1" ;

	std::stringstream toto ;
	toto << "!H:!V:VarTransform=N:NeuronType=tanh:" ;
	toto << "NCycles=" << nCycles << ":" ;
	toto << "HiddenLayers=" << networkStructure << ":" ;
	toto << "TestRate=1:TrainingMethod=BFGS:" ;
	toto << "BPMode=batch:BatchSize=" << batchSize << ":" ;
	toto << "ConvergenceImprove=1e-8:ConvergenceTests=50:UseRegulator=True:" ;
	toto << "CalculateErrors=false" ;

	factory->BookMethod( dataloader, TMVA::Types::kMLP, "MLP", toto.str().c_str() ) ;

	// ---- Now you can tell the factory to train, test, and evaluate the MVAs
	factory->TrainAllMethods() ;
	factory->TestAllMethods() ;
	factory->EvaluateAllMethods() ;

	outputFile->Close() ;

	std::cout << "==> Wrote root file : " << outputFile->GetName() << std::endl ;
	std::cout << "==> TMVARegression is done !" << std::endl ;

	delete factory ;

	//	system ("cp weights/TMVARegression_MLP.weights.xml .") ;
	return 0 ;
}
