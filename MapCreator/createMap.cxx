#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>

#include <iostream>

void createMap(float _qbar , float _delta , float _d)
{
    TFile* file = new TFile("map.root" , "RECREATE") ;
    TTree* tree = new TTree("tree" , "tree") ;

    int layerID , asicID ;
    float qbar = _qbar ;
    float delta = _delta ;
    float d = _d ;
    std::vector<double> position ;

    tree->Branch("LayerID" , &layerID) ;
    tree->Branch("AsicID" , &asicID) ;
    tree->Branch("qbar" , &qbar) ;
    tree->Branch("delta" , &delta) ;
    tree->Branch("d" , &d) ;
    tree->Branch("Position" , &position) ;

    layerID = 25 ;
    asicID = -1 ;
    position.push_back(10.408) ;
    position.push_back(10.408) ;
    position.push_back(25*26.131) ;

    tree->Fill() ;
    tree->Write() ;
    file->Close() ;
}

int main(int argc , char** argv)
{
    if ( argc != 4 )
    {
        std::cerr << "ERROR : problem with arguments passed for the program" << std::endl ;
        return -1 ;
    }

    double qbar = atof(argv[1]) ;
    double delta = atof(argv[2]) ;
    double d = atof(argv[3]) ;

    createMap(qbar , delta , d) ;

    return 0 ;
}

