#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>

#include <iostream>
#include <fstream>
#include <sstream>

#include <string>

void createTree()
{
    ifstream txtFile("/home/garillot/files/PolyaScan/toto.txt") ;

    double inQbar , inDelta , inD ;
    double qbarFit , deltaFit , mul ;
    int layerID , asicID ;

    float fInQbar , fInDelta , fD , fOutQbar , fOutDelta , fMul ;

    if ( !txtFile.is_open() )
    	return ;

    TFile* outputFile = new TFile("tree.root" , "RECREATE") ;
    TTree* outputTree = new TTree("tree" , "tree") ;

    TFile* outputTestFile = new TFile("treeTest.root" , "RECREATE") ;
    TTree* outputTestTree = new TTree("tree" , "tree") ;

    outputTree->Branch("inQbar" , &fInQbar) ;
    outputTree->Branch("inDelta" , &fInDelta) ;
    outputTree->Branch("d" , &fD) ;
    outputTree->Branch("outQbar" , &fOutQbar) ;
    outputTree->Branch("outDelta" , &fOutDelta) ;
    outputTree->Branch("mul" , &fMul) ;

    outputTestTree->Branch("inQbar" , &fInQbar) ;
    outputTestTree->Branch("inDelta" , &fInDelta) ;
    outputTestTree->Branch("d" , &fD) ;
    outputTestTree->Branch("outQbar" , &fOutQbar) ;
    outputTestTree->Branch("outDelta" , &fOutDelta) ;
    outputTestTree->Branch("mul" , &fMul) ;

    while ( txtFile >> inQbar >> inDelta >> inD )
    {
        std::stringstream fileName ; fileName << "/home/garillot/files/PolyaScan/Fits/Fit_" << inQbar << "_" << inDelta << "_" << inD << ".root" ;
        //std::cout << "Open " << fileName.str() << std::endl ;

        TFile* file = TFile::Open(fileName.str().c_str() , "READ") ;
        if ( !file )
            continue ;

        TTree* tree = dynamic_cast<TTree*>( file->Get("tree") ) ;
        tree->SetBranchAddress("LayerID" , &layerID) ;
        tree->SetBranchAddress("AsicID" , &asicID) ;
        tree->SetBranchAddress("mul" , &mul) ;
        tree->SetBranchAddress("qbar" , &qbarFit) ;
        tree->SetBranchAddress("delta" , &deltaFit) ;

        int iEntry = 0 ;
        while ( tree->GetEntry( iEntry++) )
        {
            if ( layerID == 25 && asicID == -1 )
            break ;
        }

        std::cout << "qbar : " << inQbar << "  delta : " << inDelta << "  d : " << inD << "  |  qbarFit : " << qbarFit << "  deltaFit : " << deltaFit << "  mul : " << mul << std::endl ;

        fInQbar = static_cast<float>( inQbar ) ;
        fInDelta = static_cast<float>( inDelta ) ;
        fD = static_cast<float>( inD ) ;
        fOutQbar = static_cast<float>( qbarFit - 0.02) ;
        fOutDelta = static_cast<float>( deltaFit - 0.02 ) ;
        fMul = static_cast<float>( mul - 0.05 ) ;


        if ( inD == 0.04 || inD == 0.07 || inD == 0.12 || inD == 0.17 || inD == 0.27 || inD == 0.45 || inD == 0.65 || inD == 0.85 )
            outputTestTree->Fill() ;
        else
            outputTree->Fill() ;

        file->Close() ;
    }

    outputFile->cd() ;
    outputTree->Write() ;
    outputFile->Close() ;

    outputTestFile->cd() ;
    outputTestTree->Write() ;
    outputTestFile->Close() ;
}
