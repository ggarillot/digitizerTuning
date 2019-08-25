#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>
#include <sstream>
#include <stdio.h>

#include "TFile.h"
#include "TTree.h"
#include <TCanvas.h>
#include <TStyle.h>
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TMath.h"
#include "TF1.h"
#include <TH1D.h>

#include "TMVA/Reader.h"
#include "TMVA/Tools.h"
#include "TMVA/MethodCuts.h"

// read input data file with ascii format (otherwise ROOT) ?
Bool_t ReadDataFromAsciiIFormat = kFALSE;

int main( int argc, char** argv )
{
	std::cout << std::endl;
	std::cout << "==> Start TMVARegressionApplication" << std::endl;

	// --- Create the Reader object

	TMVA::Reader *reader = new TMVA::Reader( "!Color:!Silent" );

	float foutQbar ;
	float foutDelta ;
	float fmul ;

	double outQbar ;
	double outDelta ;
	double mul ;
	int layerID ;
	int difID ;
	int asicID ;
	int minimStatus ;

	reader->AddVariable("outQbar" , &foutQbar) ;
	reader->AddVariable("outDelta" , &foutDelta) ;
	reader->AddVariable("mul" , &fmul) ;

	// --- Book the MVA methods

	TString dir    = "./weights/";
	TString prefix = "TMVARegression";

	TString methodName = "MLP method";
	TString weightfile = dir + prefix + "_" + "MLP"  + ".weights.xml";
	reader->BookMVA( methodName, weightfile );


	TFile* resultFile = new TFile("map.root" , "RECREATE") ;
	TTree* resultTree = new TTree("tree","tree") ;
	resultTree->SetDirectory(resultFile) ;

	float qbar , delta , d ;
	std::vector<double> position ;
	std::vector<double>* positionPtr = NULL ;

	resultTree->Branch("LayerID" , &layerID) ;
	resultTree->Branch("DifID" , &difID) ;
	resultTree->Branch("AsicID" , &asicID) ;
	resultTree->Branch("qbar" , &qbar) ;
	resultTree->Branch("delta" , &delta) ;
	resultTree->Branch("d" , &d) ;
	resultTree->Branch("Position" , &position) ;


	TFile* file = new TFile( "/home/guillaume/PolyaFit/resData.root" , "READ") ;
	TTree* tree = dynamic_cast<TTree*>( file->Get("tree") ) ;

	tree->SetBranchAddress("LayerID" , &layerID) ;
	tree->SetBranchAddress("DifID" , &difID) ;
	tree->SetBranchAddress("AsicID" , &asicID) ;
	tree->SetBranchAddress("qbar" , &outQbar) ;
	tree->SetBranchAddress("delta" , &outDelta) ;
	tree->SetBranchAddress("mul" , &mul) ;
	tree->SetBranchAddress("Position" , &positionPtr) ;
	tree->SetBranchAddress("minimStatus" , &minimStatus) ;


	//just tests
	foutQbar = 5.672 ;
	foutDelta = 3.129 ;
	fmul = 1.81813 ;

	std::cout << "qbar : " << (reader->EvaluateRegression( methodName ))[0] << std::endl ;
	std::cout << "delta : " << (reader->EvaluateRegression( methodName ))[1] << std::endl ;
	std::cout << "d : " << (reader->EvaluateRegression( methodName ))[2] << std::endl ;

	int iEntry = 0 ;
	while ( tree->GetEntry(iEntry++) )
	{
		if ( asicID == -1 )
			continue ;
		if ( minimStatus !=0 )
			continue ;

		position = *positionPtr ;

		foutQbar = static_cast<float>( outQbar ) ;
		foutDelta = static_cast<float>( outDelta ) ;
		fmul = static_cast<float>( mul ) ;


		qbar = (reader->EvaluateRegression( methodName ))[0] ;
		delta = (reader->EvaluateRegression( methodName ))[1] ;
		d = (reader->EvaluateRegression( methodName ))[2] ;

		if ( d < 0 )
			d = 0.01f ;

		//		std::cout << "qbar : " << qbar << "  delta : " << delta << "   d : " << d << std::endl ;

		resultTree->Fill() ;
	}

	file->Close() ;

	delete reader;
	resultFile->cd() ;
	resultTree->Write() ;
	resultFile->Close() ;


	std::cout << "==> TMVARegressionApplication is done!" << std::endl << std::endl;

	return 0 ;
}
