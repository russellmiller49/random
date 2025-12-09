import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_024.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary mapping Note_Index (0-9) -> Style_Index (1-9) -> Text.
    Styles:
    1. Terse Surgeon
    2. Academic Attending
    3. Billing Coder
    4. Trainee/Resident
    5. Sloppy Dictation
    6. Header-less
    7. Templated
    8. Narrative Flow
    9. Synonym Swapper
    """
    
    variations = {
        0: { # EBUS-TBNA 3 stations (4R, 7, 10R)
            1: "Proc: EBUS-TBNA. Sedation: Moderate.\n- Stations sampled: 4R, 7, 10R.\n- Result: Metastatic adenocarcinoma confirmed.\n- No complications.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA). Under moderate sedation, the EBUS bronchoscope was advanced. A systematic interrogation of the mediastinum identified FDG-avid lymphadenopathy. Stations 4R (right lower paratracheal), 7 (subcarinal), and 10R (right hilar) were sequentially sampled. Rapid on-site evaluation (ROSE) confirmed metastatic adenocarcinoma.",
            3: "CPT Code Justification: 31653 (EBUS-TBNA 3+ stations).\nTechnique: Linear EBUS scope used. Needle aspiration performed at three distinct nodal stations: 4R, 7, and 10R. All samples adequate for diagnosis.",
            4: "Resident Note:\nProcedure: EBUS-TBNA\n1. Moderate sedation initiated.\n2. Scope inserted orally.\n3. Identified target nodes (4R, 7, 10R).\n4. 22G needle passes x3 each station.\n5. Diagnosis: Adenocarcinoma.\nPlan: Oncology referral.",
            5: "ebus procedure patient sedated moderate we checked the nodes 4r 7 and 10r they lit up on pet so we sampled them needle went in fine got the tissue confirmed cancer adeno type no bleeding really patient woke up good.",
            6: "EBUS-TBNA under moderate sedation with sampling of FDG-avid stations 4R, 7, and 10R confirming metastatic adenocarcinoma. The procedure was tolerated well. Assessment of the airways revealed no endobronchial lesions. Rapid on-site pathology was consistent with malignancy.",
            7: "[Indication]\nMediastinal adenopathy, FDG-avid.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS-TBNA of stations 4R, 7, and 10R. Metastatic adenocarcinoma confirmed.\n[Plan]\nRefer to Oncology.",
            8: "The patient underwent an EBUS-TBNA procedure under moderate sedation to investigate avid lymph nodes. We specifically targeted stations 4R, 7, and 10R. Using the ultrasound-guided needle, we obtained samples from each station. The preliminary pathology results confirmed the presence of metastatic adenocarcinoma.",
            9: "Procedure: Endobronchial sonographic needle extraction.\nAction: Sampled FDG-hot nodes at loci 4R, 7, and 10R. Analysis validated metastatic adenocarcinoma."
        },
        1: { # ENB + Radial + Cryoablation LUL
            1: "Proc: Nav Bronch + Cryoablation LUL.\n- ENB/REBUS used for loc.\n- Target: LUL peripheral adeno.\n- Cryoablation performed.\n- No complications.",
            2: "OPERATIVE REPORT: Electromagnetic navigation bronchoscopy (ENB) combined with radial endobronchial ultrasound (REBUS) was utilized to localize a peripheral adenocarcinoma in the left upper lobe. Following confirmation of the probe position, a flexible cryoprobe was deployed. Cryoablation was executed to achieve tumor destruction. The patient tolerated the procedure without adverse events.",
            3: "Codes: 31641 (Destruction), 31627 (Nav), 31654 (REBUS).\nNote: Peripheral lesion ablation. Navigation and ultrasound used for guidance. Cryo energy applied for therapeutic intent.",
            4: "Procedure: Nav Bronch & Cryoablation\nSteps:\n1. ENB planning/registration.\n2. Navigated to LUL lesion.\n3. Radial EBUS confirmation (concentric view).\n4. Cryoprobe insertion.\n5. Ablation cycles completed.\n6. Extubation.",
            5: "patient here for ablation lul cancer used the electromagnetic nav and the radial ebus to find the spot confirmed it then put the cryo probe in and froze it good margins hopefully no bleeding seen patient extubated fine.",
            6: "Navigational bronchoscopy with ENB and radial EBUS confirmation followed by bronchoscopic cryoablation of a peripheral LUL adenocarcinoma. Navigation successful. Lesion localized. Cryoablation performed without incident.",
            7: "[Indication]\nLUL Adenocarcinoma, ablation candidate.\n[Anesthesia]\nGA.\n[Description]\nENB and REBUS used to target lesion. Bronchoscopic cryoablation performed.\n[Plan]\nPost-op imaging monitoring.",
            8: "We performed a navigational bronchoscopy to treat a left upper lobe adenocarcinoma. Using electromagnetic navigation and radial EBUS, we pinpointed the tumor's location. Once confirmed, we used a cryoprobe to freeze and destroy the tumor tissue (cryoablation). The procedure was successful.",
            9: "Procedure: Guided bronchoscopy with thermal freezing.\nAction: ENB and radial ultrasound located the LUL malignancy. Cryo-destruction of the mass was executed."
        },
        2: { # EBUS (4R, 7) + Ion + REBUS + TBBx RLL Mass
            1: "Proc: EBUS (4R, 7) + Ion Nav RLL Mass.\n- Staging: Negative.\n- RLL Mass: Radial EBUS confirmed.\n- TBBx: Samples obtained.\n- Complications: None.",
            2: "PROCEDURE: Combined staging and diagnostic bronchoscopy. First, linear EBUS was used to sample stations 4R and 7 (CPT 31652). Subsequently, the Ion robotic platform was deployed. Navigation to the right lower lobe mass was successful, with radial EBUS confirmation. Transbronchial biopsies were obtained (CPT 31628, 31627, 31654).",
            3: "Coding:\n- 31652: EBUS-TBNA 2 stations.\n- 31628: TBBx RLL.\n- 31627: Robotic Nav Add-on.\n- 31654: REBUS Add-on.\nJustification: Concurrent staging and diagnosis of peripheral mass.",
            4: "Resident Note\nProcedure: EBUS + Robotic Bronch\n1. EBUS: 4R, 7 sampled.\n2. Switch to Ion.\n3. Nav to RLL mass.\n4. REBUS check.\n5. Biopsies taken.\nPlan: Await path.",
            5: "two part procedure first ebus checking 4r and 7 then the ion robot for the rll mass radial probe showed it nicely took biopsies sent for path no issues.",
            6: "Combined EBUS nodal staging (4R and 7) and Ion robotic navigational bronchoscopy with radial EBUS and transbronchial biopsies of an RLL mass. Staging negative on ROSE. Diagnostic samples of mass adequate.",
            7: "[Indication]\nRLL Mass, Staging.\n[Anesthesia]\nGA.\n[Description]\nEBUS 4R/7. Ion Nav to RLL. REBUS confirm. TBBx performed.\n[Plan]\nDischarge.",
            8: "The patient underwent a combined procedure. We started with EBUS to stage the lymph nodes at 4R and 7. Then, we used the Ion robotic system to navigate to the mass in the right lower lobe. We confirmed the location with radial EBUS and took transbronchial biopsies for diagnosis.",
            9: "Procedure: Combined sonographic staging and robotic sampling.\nAction: Nodes 4R and 7 aspirated via EBUS. Ion platform guided instruments to RLL mass. Radial ultrasound verified. Biopsies harvested."
        },
        3: { # Ion + REBUS + TBBx + Fiducials LLL
            1: "Proc: Ion Nav LLL.\n- Target: LLL Mass.\n- Guides: REBUS.\n- Actions: TBBx x5, Fiducials x3 placed.\n- No pneumo.",
            2: "PROCEDURE: Ion robotic-assisted bronchoscopy. The left lower lobe mass was cannulated. Radial EBUS confirmed the target. Transbronchial biopsies were obtained for histopathology. Subsequently, three fiducial markers were deployed under fluoroscopic and robotic guidance to facilitate future stereotactic radiation therapy. (CPT 31626, 31628, 31627, 31654).",
            3: "Codes: 31626 (Fiducials), 31628 (Biopsy), 31627 (Nav), 31654 (REBUS).\nPrimary intent: Fiducial placement and diagnosis. Note: 31626 is the primary code by RVU usually, or 31628 depending on carrier, but both distinct.",
            4: "Resident Note\nProcedure: Ion Biopsy + Fiducials\n1. Nav to LLL.\n2. REBUS check.\n3. Biopsies taken.\n4. 3 Fiducials dropped.\n5. Fluoro confirmed position.\nPlan: SBRT referral.",
            5: "robotic case lll mass we navigated there with ion used radial ebus to see it took biopsies then put in fiducial markers for radiation later everything went smooth.",
            6: "Ion robotic bronchoscopy with radial EBUS, transbronchial biopsies, and fiducial marker placement for an LLL mass. Biopsies positive. Markers visible on fluoro.",
            7: "[Indication]\nLLL Mass, requires fiducials.\n[Anesthesia]\nGA.\n[Description]\nIon Nav. REBUS. TBBx x4. Fiducials x3 placed LLL.\n[Plan]\nRadiation Oncology.",
            8: "We utilized the Ion robotic bronchoscope to access a mass in the left lower lobe. After confirming the site with radial EBUS, we performed transbronchial biopsies. We then placed fiducial markers in the lesion to assist with upcoming radiation treatment.",
            9: "Procedure: Robotic navigational fiducial implantation and sampling.\nAction: LLL mass accessed. Radial ultrasound verification. Tissue sampled. Fiducial markers deposited."
        },
        4: { # EBUS (7) + EMN + REBUS + TBBx RLL (Met breast)
            1: "Proc: EBUS (Station 7) + EMN TBBx RLL.\n- Indication: Met Breast Ca.\n- EBUS: Subcarinal sampled.\n- EMN/REBUS: RLL nodule.\n- TBBx: Samples taken.\n- No complications.",
            2: "PROCEDURE: Mediastinal staging via EBUS-TBNA of the subcarinal station (7) was performed. Following this, electromagnetic navigation bronchoscopy (EMN) with radial EBUS confirmation was utilized to biopsy a right lower lobe nodule. Clinical context is metastatic breast cancer.",
            3: "Codes: 31652 (EBUS 1 station), 31628 (TBBx), 31627 (Nav), 31654 (REBUS).\nRationale: Single station EBUS staging followed by navigational biopsy of peripheral nodule.",
            4: "Resident Note\nProcedure: EBUS + EMN\n1. Station 7 TBNA.\n2. EMN Nav to RLL.\n3. REBUS confirm.\n4. Biopsy RLL.\nHistory: Breast CA.\nPlan: Path check.",
            5: "met breast cancer case did the ebus on station 7 first then the navigation to the rll nodule radial probe showed it well took biopsies bleeding was minimal.",
            6: "EBUS-TBNA of subcarinal node plus EMN-guided bronchoscopy with radial EBUS and transbronchial biopsies of an RLL nodule in a patient with metastatic breast cancer. Procedure completed successfully.",
            7: "[Indication]\nMetastatic Breast Cancer, RLL nodule.\n[Anesthesia]\nGA.\n[Description]\nEBUS Station 7. EMN Nav RLL. REBUS. TBBx.\n[Plan]\nOncology f/u.",
            8: "This patient with metastatic breast cancer required evaluation of a right lower lobe nodule and mediastinal nodes. We sampled the subcarinal node (station 7) using EBUS. Then, using electromagnetic navigation and radial EBUS, we located and biopsied the RLL nodule.",
            9: "Procedure: Subcarinal sonographic aspiration and navigational biopsy.\nAction: Station 7 sampled. EMN and radial ultrasound guided biopsy of RLL nodule."
        },
        5: { # EBUS (4R, 7) + Ion + REBUS + Forceps/Cryo RML
            1: "Proc: EBUS (4R, 7) + Ion RML Biopsy.\n- EBUS: Staging.\n- Ion/REBUS: RML nodule.\n- Sampling: Forceps + Cryobiopsy.\n- No complications.",
            2: "PROCEDURE: EBUS-TBNA nodal sampling of stations 4R and 7 was performed for staging (CPT 31652). This was followed by Ion robotic bronchoscopy to the right middle lobe. Radial EBUS verified the target. Diagnostic tissue was obtained using both standard forceps and a cryobiopsy probe (CPT 31628, 31627, 31654).",
            3: "Codes: 31652 (EBUS), 31628 (Biopsy), 31627 (Nav), 31654 (REBUS).\nNote: Cryobiopsy for diagnosis is coded as 31628 (biopsy), not ablation.",
            4: "Resident Note\nProcedure: EBUS + Ion\n1. EBUS 4R, 7.\n2. Ion Nav to RML.\n3. REBUS.\n4. Forceps bx.\n5. Cryo bx.\nPlan: Path.",
            5: "staging ebus 4r and 7 then ion robot to rml used radial ebus then forceps and cryo probe for biopsies got good pieces no bleeding.",
            6: "EBUS nodal sampling of 4R and 7 plus Ion robotic bronchoscopy with radial EBUS and combined forceps and cryobiopsy of an RML nodule. Samples sent for pathology.",
            7: "[Indication]\nRML Nodule.\n[Anesthesia]\nGA.\n[Description]\nEBUS 4R/7. Ion Nav RML. REBUS. Forceps and Cryobiopsy performed.\n[Plan]\nRecovery.",
            8: "We staged the patient using EBUS at stations 4R and 7. Then, we used the Ion robot to reach a nodule in the right middle lobe. We used both forceps and a cryoprobe to get high-quality biopsy samples, confirmed with radial EBUS.",
            9: "Procedure: Sonographic staging and robotic cryo-sampling.\nAction: Nodes 4R and 7 sampled. Ion platform guided to RML. Radial ultrasound used. Tissue harvested via forceps and cryoprobe."
        },
        6: { # EBUS (4 stations) + EMN/Standard Bx Cavitary LUL SCC
            1: "Proc: EBUS (4 stations) + EMN/Standard Bx LUL.\n- Indication: Cavitary LUL SCC.\n- EBUS: Extensive nodal sampling.\n- Bronch: Endobronchial biopsies.\n- No complications.",
            2: "PROCEDURE: Extensive EBUS-TBNA staging of four mediastinal/hilar stations was performed (CPT 31653). Subsequently, EMN guidance facilitated approach to a cavitary LUL squamous cell carcinoma. Standard endobronchial biopsies were obtained from the lesion (CPT 31625).",
            3: "Codes: 31653 (EBUS 3+), 31625 (Endobronchial Bx).\nNote: EMN (31627) is generally not reimbursed with 31625 (endobronchial biopsy) unless the target is peripheral/parenchymal. Given 'cavitary LUL SCC', if lesion is visible endobronchially, 31625 applies.",
            4: "Resident Note\nProcedure: EBUS + LUL Biopsy\n1. EBUS x4 stations.\n2. Nav to LUL cavity.\n3. Endobronchial lesion seen.\n4. Biopsied (forceps).\nPlan: Oncology.",
            5: "patient with lul cavity scc did extensive ebus four stations then went to lul used nav but could see it endobronchially so took biopsies forceps.",
            6: "EBUS-TBNA of four mediastinal/hilar stations plus EMN-guided and standard endobronchial biopsies of a cavitary LUL squamous cell carcinoma with extensive nodal disease.",
            7: "[Indication]\nLUL SCC, Nodal disease.\n[Anesthesia]\nGA.\n[Description]\nEBUS x4 stations. EMN to LUL. Endobronchial Bx.\n[Plan]\nAdmit.",
            8: "We performed a thorough EBUS staging, sampling four lymph node stations. We then navigated to the LUL cavitary mass using EMN. Since the tumor was visible within the airway (endobronchial), we performed standard biopsies of the squamous cell carcinoma.",
            9: "Procedure: Multi-station sonographic staging and endobronchial sampling.\nAction: Four nodal stations aspirated. LUL cavitary lesion biopsied via endobronchial approach."
        },
        7: { # EBUS (7, 4R, 4L, 10R, 11R) N2 disease
            1: "Proc: EBUS-TBNA.\n- Stations: 7, 4R, 4L, 10R, 11R.\n- Dx: N2 Adenocarcinoma.\n- 5 stations sampled.",
            2: "PROCEDURE: EBUS-TBNA was performed for mediastinal staging. Lymph node stations 7, 4R, 4L, 10R, and 11R were systematically sampled. Cytopathology revealed adenocarcinoma in contralateral mediastinal nodes, consistent with N2 disease (CPT 31653).",
            3: "Code: 31653 (EBUS-TBNA 3+ stations).\nDetail: 5 distinct stations sampled (7, 4R, 4L, 10R, 11R).",
            4: "Resident Note\nProcedure: EBUS\n1. Sampled 7, 4R, 4L, 10R, 11R.\n2. ROSE: Positive for Adeno.\n3. N2 disease confirmed.\nPlan: Oncology.",
            5: "big ebus case hit five stations 7 4r 4l 10r 11r all positive for adeno looks like n2 disease patient tolerated well.",
            6: "EBUS-TBNA with sampling of stations 7, 4R, 4L, 10R, and 11R showing adenocarcinoma in mediastinal lymph nodes consistent with N2 disease.",
            7: "[Indication]\nStaging, Adenocarcinoma.\n[Anesthesia]\nModerate.\n[Description]\nEBUS x5 stations (7, 4R, 4L, 10R, 11R). Confirmed N2 disease.\n[Plan]\nReferral.",
            8: "We performed a comprehensive EBUS-TBNA to stage the patient's cancer. We sampled five different lymph node stations: 7, 4R, 4L, 10R, and 11R. The results show adenocarcinoma in the mediastinum, confirming N2 disease.",
            9: "Procedure: Extensive endobronchial sonographic aspiration.\nAction: Five nodal stations (7, 4R, 4L, 10R, 11R) were aspirated. Findings indicate N2 adenocarcinoma."
        },
        8: { # EBUS (7, 4R, 10R, 11R) Sarcoid
            1: "Proc: EBUS-TBNA Sarcoid Protocol.\n- Stations: 7, 4R, 10R, 11R.\n- Path: Non-necrotizing granulomas.\n- Dx: Sarcoidosis.",
            2: "PROCEDURE: EBUS-TBNA was undertaken to evaluate mediastinal and hilar adenopathy in a non-smoker. Stations 7, 4R, 10R, and 11R were sampled. Histological evaluation demonstrated non-necrotizing granulomas, consistent with a diagnosis of sarcoidosis (CPT 31653).",
            3: "Code: 31653 (EBUS 3+ stations).\nIndication: Adenopathy.\nPathology: Granulomas (Sarcoid).",
            4: "Resident Note\nProcedure: EBUS\n1. Indication: Rule out Sarcoid.\n2. Sampled 7, 4R, 10R, 11R.\n3. ROSE: Granulomas seen.\nPlan: Pulm clinic.",
            5: "ebus for sarcoid suspicion never smoker checked 7 4r 10r 11r got granulomas non necrotizing looks like sarcoid no cancer seen.",
            6: "Detailed EBUS-TBNA for mediastinal and hilar adenopathy in a never-smoker, with stations 7, 4R, 10R, and 11R sampled showing non-necrotizing granulomas consistent with sarcoidosis.",
            7: "[Indication]\nAdenopathy, suspect Sarcoid.\n[Anesthesia]\nModerate.\n[Description]\nEBUS x4 stations. Path: Non-necrotizing granulomas.\n[Plan]\nFollow up.",
            8: "To investigate the swollen lymph nodes in this non-smoker, we performed an EBUS-TBNA. We sampled stations 7, 4R, 10R, and 11R. The pathology returned showing non-necrotizing granulomas, which fits with a diagnosis of sarcoidosis.",
            9: "Procedure: Endobronchial ultrasound aspiration for granulomatous disease.\nAction: Nodes at 7, 4R, 10R, and 11R were sampled. Morphology revealed non-necrotizing granulomas."
        },
        9: { # US Thoracentesis Left
            1: "Proc: US Thoracentesis Left.\n- Guidance: Ultrasound.\n- Fluid: 650mL blood-tinged.\n- Complications: None.",
            2: "PROCEDURE: Ultrasound-guided diagnostic thoracentesis. The left hemithorax was scanned, and a pocket of fluid was identified. Under sterile conditions and local anesthesia, a needle was introduced. 650 mL of hemorrhagic fluid was drained from the patient with a known LUL mass (CPT 32555).",
            3: "Code: 32555 (Thoracentesis with imaging guidance).\nVolume: 650 mL.\nCharacter: Hemorrhagic.",
            4: "Resident Note\nProcedure: Left Thoracentesis\n1. US marked site.\n2. Prep/Drape.\n3. Needle in.\n4. Drained 650cc bloody fluid.\n5. Bandage applied.\nPlan: Fluid analysis.",
            5: "bedside thoracentesis left side used ultrasound found the fluid put the needle in got about 650ml bloody fluid out patient tolerated fine.",
            6: "Ultrasound-guided diagnostic thoracentesis of a left hemorrhagic effusion in a patient with LUL lung mass, draining 650 mL of blood-tinged fluid. No complications.",
            7: "[Indication]\nLeft effusion, LUL mass.\n[Anesthesia]\nLocal.\n[Description]\nUS guidance. Left thoracentesis. 650mL bloody fluid removed.\n[Plan]\nFluid analysis.",
            8: "We performed a thoracentesis on the left side to check the fluid in the patient with an LUL mass. Using ultrasound guidance, we successfully drained 650 mL of blood-tinged fluid.",
            9: "Procedure: Sonographic pleural aspiration.\nAction: Left pleural space accessed via ultrasound guidance. 650 mL of hemorrhagic effusion evacuated."
        }
    }
    return variations

def get_base_data_mocks():
    return [
        {"idx": 0, "orig_name": "Patient Zero", "orig_age": 65, "names": ["John Smith", "Jane Doe", "Michael Brown", "Emily Davis", "Chris Wilson", "Sarah Miller", "David Taylor", "Jessica Anderson", "Daniel Thomas"]},
        {"idx": 1, "orig_name": "Patient One", "orig_age": 55, "names": ["Robert Martinez", "Linda Hernandez", "James Moore", "Barbara Martin", "William Jackson", "Elizabeth Thompson", "Richard White", "Jennifer Lopez", "Joseph Lee"]},
        {"idx": 2, "orig_name": "Patient Two", "orig_age": 70, "names": ["Charles Harris", "Susan Clark", "Thomas Lewis", "Margaret Robinson", "Christopher Walker", "Dorothy Perez", "Daniel Hall", "Lisa Young", "Matthew Allen"]},
        {"idx": 3, "orig_name": "Patient Three", "orig_age": 60, "names": ["Anthony King", "Nancy Wright", "Mark Scott", "Karen Torres", "Donald Nguyen", "Betty Hill", "Paul Flores", "Sandra Green", "Steven Adams"]},
        {"idx": 4, "orig_name": "Patient Four", "orig_age": 50, "names": ["Andrew Nelson", "Ashley Baker", "Kenneth Carter", "Kimberly Mitchell", "Joshua Roberts", "Donna Phillips", "George Campbell", "Carol Parker", "Kevin Evans"]},
        {"idx": 5, "orig_name": "Patient Five", "orig_age": 75, "names": ["Brian Edwards", "Michelle Collins", "Edward Stewart", "Laura Sanchez", "Ronald Morris", "Sarah Rogers", "Timothy Reed", "Deborah Cook", "Jason Morgan"]},
        {"idx": 6, "orig_name": "Patient Six", "orig_age": 68, "names": ["Jeffrey Bell", "Stephanie Murphy", "Ryan Bailey", "Rebecca Rivera", "Jacob Cooper", "Sharon Richardson", "Gary Cox", "Cynthia Howard", "Nicholas Ward"]},
        {"idx": 7, "orig_name": "Patient Seven", "orig_age": 62, "names": ["Eric Torres", "Kathleen Peterson", "Stephen Gray", "Amy Ramirez", "Larry James", "Anna Watson", "Justin Brooks", "Brenda Kelly", "Scott Sanders"]},
        {"idx": 8, "orig_name": "Patient Eight", "orig_age": 58, "names": ["Brandon Price", "Pamela Bennett", "Frank Wood", "Nicole Barnes", "Gregory Ross", "Katherine Henderson", "Raymond Coleman", "Virginia Jenkins", "Patrick Perry"]},
        {"idx": 9, "orig_name": "Patient Nine", "orig_age": 72, "names": ["Alexander Powell", "Debra Long", "Jack Patterson", "Rachel Hughes", "Dennis Flores", "Janet Washington", "Jerry Butler", "Catherine Simmons", "Tyler Foster"]},
    ]

def main():
    # Load original data from source file
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        print("Please ensure the file exists or update SOURCE_FILE path.")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        return
    
    if not isinstance(source_data, list):
        print(f"Error: Source file must contain a JSON array, got {type(source_data)}")
        return
    
    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through each original note in source data
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            print(f"Warning: More notes in source than base_data entries. Skipping note {idx}.")
            continue
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Iterate through the 9 styles
        for style_num in range(1, 10):
            
            # Deep copy the original note structure
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            # Use get() to handle cases where variation might not be defined (though it is here)
            note_entry["note_text"] = variations_text.get(idx, {}).get(style_num, f"Variation {style_num} not found")
            
            # Update registry_entry fields if they exist, or create if missing (to hold the synthetic data)
            if "registry_entry" not in note_entry:
                note_entry["registry_entry"] = {}
                
            # Update or Set fields
            note_entry["registry_entry"]["patient_age"] = new_age
            note_entry["registry_entry"]["procedure_date"] = rand_date_str
            
            # Ensure unique MRN if present, or create one
            current_mrn = note_entry["registry_entry"].get("patient_mrn", f"MRN_SYN_{idx}")
            note_entry["registry_entry"]["patient_mrn"] = f"{current_mrn}_style_{style_num}"

            # Add synthetic metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_blvr_notes_part_024.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()