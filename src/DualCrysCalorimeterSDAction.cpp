//==========================================================================
//  AIDA Detector description implementation 
//--------------------------------------------------------------------------
// Copyright (C) Organisation europeenne pour la Recherche nucleaire (CERN)
// All rights reserved.
//
// For the licensing terms see $DD4hepINSTALL/LICENSE.
// For the list of contributors see $DD4hepINSTALL/doc/CREDITS.
//
// Author     : M.Frank
//
//==========================================================================

// Framework include files
#include <algorithm>
#include <CLHEP/Units/PhysicalConstants.h>
#include "k4RecCalorimeter/DualCrysCalorimeterHit.h"
//#include "DualCrysCalorimeterHit.h"
#include "DDG4/EventParameters.h"
#include "DDG4/Geant4SensDetAction.inl"
#include "DDG4/Factories.h"
#include "DD4hep/InstanceCount.h"
#include "DDG4/Geant4Random.h"
#include <G4Event.hh>
using namespace std;

// way too slow if track all photons for now
//   so randomly delete photons after creation according to this fraction
//   dialScint=1.0, dialCer=1.0 to keep all photons 
double dialCherC  = 1000 / 1000000.;
double dialCherO  =  100 / 1000000.;

double dialScintC = 1000 / 1000000.;
double dialScintO =  100 / 1000000.;
float betarel=1/1.544;	//depends on the media refractive index
int printlimitSCE=10;
int MAXEVENT=10;

namespace CalVision {
	G4double fromEvToNm(G4double energy){
		// there is some bug somewhere.  shouldn't need this factor
		//return  conversioneVnm/ energy*1000.;
		return 1239.84187 / energy*1000.;
	}	
	int SCECOUNT=0;
	int SCECOUNT2=0;
	int OLDEVENTNUMBER=-1;
	class DualCrysCalorimeterSD {
		public:
			//typedef DualCrysCalorimeterHit Hit;
			typedef dd4hep::sim::Geant4Calorimeter::Hit Hit;
			// If we need special data to personalize the action, put it here
			//int mumDeposits = 0;
			//double integratedDeposit = 0;
			};
}

// Namespace for the AIDA detector description toolkit
namespace dd4hep {  // Namespace for the Geant4 based simulation part of the AIDA detector description toolkit
	namespace sim   {
		using namespace CalVision;

		typedef dd4hep::sim::Geant4Calorimeter::Hit Hit;
		// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		//               Geant4SensitiveAction<MyTrackerSD>
		// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		/** \addtogroup Geant4SDActionPlugin
		 *
		 * @{
		 * \package DualCrysCalorimeterSDAction
		 *
		 * @}
		 */

	  template <> void Geant4SensitiveAction<DualCrysCalorimeterSD>::initialize() {
	    declareProperty("dialCherC", dialCherC);
	    declareProperty("dialScintC",dialScintC);
	    declareProperty("dialCherO", dialCherO);
	    declareProperty("dialScintO",dialScintO);
	    declareProperty("betarel", betarel);
	    declareProperty("printlimitSCE", printlimitSCE);
	    declareProperty("MAXEVENTSCE", MAXEVENT);
	  }

	  
		/// Define collections created by this sensitivie action object
		template <> void Geant4SensitiveAction<DualCrysCalorimeterSD>::defineCollections()    {
			m_hitCreationMode = Geant4Sensitive::DETAILED_MODE;
			m_collectionID = declareReadoutFilteredCollection<Hit>();
			//m_collectionID = declareReadoutFilteredCollection<CalVision::DualCrysCalorimeterSD::Hit>();
		}
		
		// Method for generating hit(s) using the information of G4Step object.
		template <> bool Geant4SensitiveAction<DualCrysCalorimeterSD>::process(const G4Step* step,G4TouchableHistory* /*hist*/ ) {
			Geant4Event&  evt = context()->event();
			int eventNumber = static_cast<G4Event const&>(context()->event()).GetEventID();
			
			G4StepPoint *thePrePoint  = step->GetPreStepPoint();
			G4StepPoint *thePostPoint = step->GetPostStepPoint();
			
			G4VPhysicalVolume *thePrePV 	= thePrePoint->GetPhysicalVolume();
			G4double pretime 		= thePrePoint->GetGlobalTime();
			G4VPhysicalVolume *thePostPV 	= thePostPoint->GetPhysicalVolume();
			G4double posttime 		= thePostPoint->GetGlobalTime();
			
			G4String thePrePVName  = "";
			if (thePrePV)	thePrePVName = thePrePV->GetName();
			G4String thePostPVName = "";
			if (thePostPV)	thePostPVName = thePostPV->GetName();
			G4Track *theTrack = step->GetTrack();
			G4int TrPDGid = theTrack->GetDefinition()->GetPDGEncoding();

			Geant4StepHandler h(step);
			HitContribution contrib = Hit::extractContribution(step);
			Geant4HitCollection*  coll    = collection(m_collectionID);
			VolumeID cell = 0;	
			try {
				cell = cellID(step);
			} catch(std::runtime_error &e) {
				stringstream out;
				out << setprecision(20) << scientific;
				out << "ERROR: " << e.what()  << endl;
				out << "Position: "
					<< "Pre (" <<  setw(24) << step->GetPreStepPoint()->GetPosition() << ") "
					<< "Post (" << setw(24) << step->GetPostStepPoint()->GetPosition() << ") "
					<< endl;
				out << "Momentum: "
					<< " Pre (" <<setw(24) << step->GetPreStepPoint() ->GetMomentum()  << ") "
					<< " Post (" <<setw(24) << step->GetPostStepPoint()->GetMomentum() << ") "
					<< endl;
				cout << out.str();
				return true;
			}
			
			Hit* hit = coll->findByKey<Hit>(cell);
			if ( !hit ) {
				Geant4TouchableHandler handler(step);
				DDSegmentation::Vector3D pos = m_segmentation.position(cell);
				Position global = h.localToGlobal(pos);
				hit = new Hit(global);
				hit->cellID = cell;
				coll->add(cell, hit);

				if ( 0 == hit->cellID )  { // for debugging only!
					hit->cellID = cellID(step);
					except("+++ Invalid CELL ID for hit!");
				}
			}
			G4Track *track =  step->GetTrack();
			string amedia = ((track->GetMaterial())->GetName());
			float avearrival=(pretime+posttime)/2.;
			//if(thePostPoint->GetProcessDefinedStep()->GetProcessName().contains("Inelast")) hit->n_inelastic+=1;
			
			//photons
			if( track->GetDefinition() == G4OpticalPhoton::OpticalPhotonDefinition() )  {
				int phstep = track->GetCurrentStepNumber();
				if ( track->GetCreatorProcess()->G4VProcess::GetProcessName() == "CerenkovPhys")  {
					if (contrib.pdgID == -22) {
						contrib.pdgID *= 2;
					}
					if(amedia.find("kill")!=string::npos){
						hit->truth.emplace_back(contrib);
						track->SetTrackStatus(fStopAndKill);
					}
					else if(amedia.find("BlackHole")!=string::npos) {
						track->SetTrackStatus(fStopAndKill);
					}
					else {
						if( (phstep==1)  ) {
							dd4hep::sim::Geant4Random& rnd = evt.random();
							double dial;
							if((amedia.find("E_PbWO4")!=std::string::npos)||(amedia.find("BGO")!=std::string::npos)) {
								dial = dialCherC;
							} else {
								dial = dialCherO;
							}
							if (rnd.rndm() < dial) {
								std::cout << "contrib.time: " << contrib.time << "  pretime: " << pretime << "  posttime: " << posttime << std::endl;
								hit->truth.emplace_back(contrib);
							} else {
								track->SetTrackStatus(fStopAndKill);
							}
						}
					}
				}
				else if (  track->GetCreatorProcess()->G4VProcess::GetProcessName() == "ScintillationPhys"  ) {
					std::string amedia = ((track->GetMaterial())->GetName());
					if(amedia.find("kill")!=std::string::npos) {
						hit->truth.emplace_back(contrib);
						track->SetTrackStatus(fStopAndKill);
					}
					else if(amedia.find("BlackHole")!=std::string::npos) {
						track->SetTrackStatus(fStopAndKill);
					}
					else {
						if( (phstep==1) ) {
							dd4hep::sim::Geant4Random& rnd = evt.random();
							double dial;
							if((amedia.find("E_PbWO4")!=std::string::npos)||(amedia.find("BGO")!=std::string::npos)) {
								dial = dialScintC;
							} else {
								dial = dialScintO;
							}
							if(rnd.rndm()<dial) {
								hit->truth.emplace_back(contrib);
							} else {
								track->SetTrackStatus(fStopAndKill);
							}
						}
					}
				} else {
					track->SetTrackStatus(fStopAndKill);
				}
			} else {   // particles other than optical photons
				if(amedia.find("BlackHole")!=std::string::npos) {  //edge detector, not the kill PD media
					hit->energyDeposit += track->GetKineticEnergy();
					track->SetTrackStatus(fStopAndKill);
				} 
				else { //add information about each contribution to the hit
					//hit->truth.emplace_back(contrib);
					hit->energyDeposit += contrib.deposit;
				}// comment for this routine says mark the track to be kept for MC truth propagation during hit processing
			}
			mark(h.track);
			return true;
		}
	}
} // end namespace calvision

namespace dd4hep { 
	namespace sim {
		using namespace CalVision;
		struct WavelengthMinimumCut : public dd4hep::sim::Geant4Filter  {// Energy cut value
			double m_wavelengthCut;
			public: // Constructor.
			WavelengthMinimumCut(dd4hep::sim::Geant4Context* c, const std::string& n);
			virtual ~WavelengthMinimumCut(); // Standard destructor
			
			// Filter action. Return true if hits should be processed
			virtual bool operator()(const G4Step* step) const  override  final  {
				bool test=true;
				G4Track *theTrack = step->GetTrack();
				if(theTrack->GetDefinition() == G4OpticalPhoton::OpticalPhotonDefinition() ) {
					float energy = theTrack->GetTotalEnergy()/eV;
					float wave   = fromEvToNm(energy);
					if(wave < m_wavelengthCut) {
						theTrack->SetTrackStatus(fStopAndKill);
						test=false;
					}
				}
				return test;
			}
			virtual bool operator()(const Geant4FastSimSpot* spot) const  override  final  {
				return true;
			}
		};
		WavelengthMinimumCut::WavelengthMinimumCut(Geant4Context* c, const std::string& n) //Constructor
			: Geant4Filter(c,n) {
				InstanceCount::increment(this);
				declareProperty("Cut",m_wavelengthCut=0.0);
			}
		WavelengthMinimumCut::~WavelengthMinimumCut() { // Standard destructor
			InstanceCount::decrement(this);
		}
		
		struct WavelengthnmwindCut : public dd4hep::sim::Geant4Filter  { // Energy cut value
			double m_wavelengthstart;
			public: // Constructor.
			WavelengthnmwindCut(dd4hep::sim::Geant4Context* c, const std::string& n);
			virtual ~WavelengthnmwindCut(); // Standard destructor
			// Filter action. Return true if hits should be processed
			virtual bool operator()(const G4Step* step) const  override  final  {
				bool test=true;
				G4Track *theTrack = step->GetTrack();
				if(theTrack->GetDefinition() == G4OpticalPhoton::OpticalPhotonDefinition() ) {
					float energy = theTrack->GetTotalEnergy()/eV;
					float wave   = fromEvToNm(energy);
					if((wave < m_wavelengthstart) || (wave > m_wavelengthstart+0.5) ) {
						theTrack->SetTrackStatus(fStopAndKill);
						test=false;
					}
				}
				return test;
			}
			virtual bool operator()(const Geant4FastSimSpot* spot) const  override  final  {
				return true;
			}
		};
		WavelengthnmwindCut::WavelengthnmwindCut(Geant4Context* c, const std::string& n) // Constructor.
			: Geant4Filter(c,n) {
				InstanceCount::increment(this);
				declareProperty("Cut",m_wavelengthstart=0.0);
			}
		WavelengthnmwindCut::~WavelengthnmwindCut() { // Standard destructor
			InstanceCount::decrement(this);
		}
	}
}  // end using namespace

//--- Factory declaration
namespace dd4hep { 
	namespace sim {
		typedef Geant4SensitiveAction<DualCrysCalorimeterSD> DualCrysCalorimeterSDAction;
	}
}

DECLARE_GEANT4SENSITIVE(DualCrysCalorimeterSDAction)
DECLARE_GEANT4ACTION(WavelengthMinimumCut)
DECLARE_GEANT4ACTION(WavelengthnmwindCut)
