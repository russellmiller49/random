import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_022.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations for the 5 notes in Part 022.
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Note 1: Peripheral Radial EBUS (LLL Nodule) - CPT 31628, 31623, 31654
            1: "Indication: LLL nodule.\nProcedure: Bronchoscopy with REBUS.\n- Airway normal.\n- Radial EBUS: Concentric view of LLL nodule.\n- Interventions: TBLB x1, Brush x1.\n- ROSE: Nondiagnostic.\nComplications: None.",
            2: "PROCEDURE: Diagnostic bronchoscopy with radial endobronchial ultrasound guidance.\nCLINICAL SUMMARY: The patient presented with a left lower lobe pulmonary nodule requiring tissue diagnosis.\nOPERATIVE REPORT: Under general anesthesia, the airways were inspected and found to be patent. A P190 ultrathin bronchoscope was navigated to the left lower lobe target. Utilization of a radial EBUS probe confirmed a concentric orientation to the lesion. Transbronchial biopsies and bronchial brushings were obtained. Preliminary rapid on-site evaluation was nondiagnostic. The patient tolerated the procedure well.",
            3: "Code Selection Justification:\n- 31628 (Transbronchial biopsy): Primary sampling method utilized for peripheral LLL nodule.\n- 31623 (Brushing): Distinct sampling modality employed on the same target.\n- 31654 (Radial EBUS): Add-on code supported by documentation of concentric view localization of the peripheral lesion prior to sampling.\nProcedure Note: Visualization confirmed via radial probe. Tools extended into lesion.",
            4: "Resident Procedure Note\nPatient: [Name]\nAttending: [Name]\nProcedure: Bronchoscopy with EBUS\nSteps:\n1. LMA placed.\n2. Standard inspection: Normal.\n3. Ultrathin scope to LLL.\n4. Radial EBUS found lesion (concentric).\n5. Biopsy and brush performed.\n6. ROSE negative.\nPlan: Await finals.",
            5: "did a bronch today for that LLL nodule used the thin scope and the radial probe found it concentric view took some biopsies with the forceps and a brush rose didn't see any cancer but we got good pieces no bleeding patient did fine extubated in room",
            6: "The patient was brought to the bronchoscopy suite and induced with general anesthesia. An LMA was placed. Initial inspection with a Q190 scope showed normal anatomy. We switched to a P190 ultrathin scope and navigated to the left lower lobe. The radial EBUS probe was inserted and a concentric image of the nodule was obtained. We performed transbronchial biopsies and brushings. There were no complications.",
            7: "[Indication] Left lower lobe nodule.\n[Anesthesia] General via LMA.\n[Description] Radial EBUS localization (concentric view). Sampling via forceps and brush. Airway normal.\n[Plan] Discharge. Follow pathology.",
            8: "After obtaining informed consent, we brought the patient to the procedure room. General anesthesia was administered. We inspected the central airways and found no endobronchial lesions. Using the ultrathin bronchoscope, we targeted the left lower lobe. The radial EBUS probe confirmed the location of the nodule with a concentric return. We then passed biopsy forceps and a brush to collect samples.",
            9: "Diagnostic intervention: Peripheral navigation.\nTarget: LLL pulmonary lesion.\nMethod: The nodule was localized via ultrasonic radial scanning. Tissue acquisition was executed using transbronchial forceps and a cytology brush. Immediate assessment was inconclusive."
        },
        1: { # Note 2: Pleuroscopy & PleurX (Pleural Effusion) - CPT 32609, 32550
            1: "Procedure: Left Medical Thoracoscopy & PleurX.\nFindings: 800cc bloody fluid. Dense adhesions/tethered lung. Diffuse inflammation.\nActions:\n- Biopsy parietal pleura x8.\n- PleurX catheter tunneled and inserted.\nComplications: None.",
            2: "OPERATIVE NARRATIVE: The patient underwent left-sided medical pleuroscopy for evaluation of a recurrent pleural effusion. Approximately 800ml of hemorrhagic fluid was evacuated. Visualization revealed extensive fibrous adhesions and lung entrapment, preventing full inspection of the apex. Biopsies of the parietal pleura and adherent visceral pleura were obtained. Subsequently, a tunneled indwelling pleural catheter (PleurX) was placed via a separate incision to facilitate ongoing drainage.",
            3: "Billing Summary:\n- CPT 32609: Medical thoracoscopy with biopsy of pleura. Supported by rigid thoracoscopy, visualization of adhesions, and 8 biopsies of parietal pleura.\n- CPT 32550: Insertion of tunneled pleural catheter. Supported by creation of subcutaneous tunnel and placement of PleurX device via separate site.\n- Note: Thoracentesis fluid removal bundled.",
            4: "Procedure: Pleuroscopy + IPC Placement\nSteps:\n1. Ultrasound guidance.\n2. Trocar placement 6th intercostal space.\n3. Drained 800cc bloody fluid.\n4. Saw adhesions, took biopsies.\n5. Tunneled PleurX catheter placed.\n6. Sutured and dressed.\nPlan: Home with drain instructions.",
            5: "patient in lateral decubitus put the port in drained a lot of bloody fluid like 800cc lung was stuck down with adhesions couldnt see the top took some biopsies of the pleura then put in a pleurx catheter tunneled it under the skin wife knows how to use it now no issues",
            6: "The patient was prepped and draped. Local anesthesia and sedation were administered. We inserted a trocar into the left chest and evacuated 800cc of bloody effusion. Inspection revealed trapped lung with thick adhesions. Biopsies were taken from the parietal pleura. A PleurX catheter was then tunneled and inserted into the pleural space through a separate site. The incisions were closed.",
            7: "[Indication] Recurrent Pleural Effusion.\n[Anesthesia] Moderate Sedation/Local.\n[Description] Rigid Pleuroscopy. 800cc drained. Dense adhesions. Biopsy x8. Tunneled IPC (PleurX) placed.\n[Plan] Discharge. PleurX education completed.",
            8: "We positioned the patient in the left lateral decubitus position. After placing the primary port, we drained the effusion. The lung appeared entrapped by significant inflammation and adhesions. We utilized forceps to biopsy the parietal pleura. Following the diagnostic portion, we established a subcutaneous tunnel and placed an indwelling pleural catheter for long-term management.",
            9: "Intervention: Thoracic exploration and drainage.\nFindings: Hemorrhagic effusion and fibrous tethering.\nActions: Tissue sampling of the chest wall lining was performed. A tunneled drainage conduit was implanted for chronic management."
        },
        2: { # Note 3: Navigational Bronchoscopy (RUL Nodule Marking) - CPT 31622, 31627, 31654
            1: "Indication: RUL nodule marking.\nTechnique: ENB + Radial EBUS.\nFindings: Normal airway. Target reached.\nAction: Injected 0.75ml ICG dye adjacent to nodule.\nOutcome: Successful marking for robotic resection.",
            2: "PROCEDURE: Electromagnetic navigational bronchoscopy with dye marking.\nINDICATION: Right upper lobe pulmonary nodule planned for resection.\nFINDINGS: The airway examination was unremarkable. Using the SuperDimension navigation system, the catheter was guided to the RUL target. Radial EBUS confirmation was attempted. Isocyanine green (ICG) dye was injected subpleurally to facilitate identification during the subsequent robotic assisted thoracoscopic surgery.",
            3: "CPT Coding:\n- 31627 (Navigation): Use of SuperDimension system to reach peripheral RUL target.\n- 31654 (Radial EBUS): Use of radial probe to verify lesion proximity.\n- 31622 (Diagnostic Bronch): Base code for airway inspection and dye injection (no biopsy performed).\nNote: Procedure performed for localization prior to surgery.",
            4: "Procedure: Navigational Bronch (Dye Marking)\nSteps:\n1. Intubation 8.5 ETT.\n2. Diagnostic bronch normal.\n3. Navigated to RUL nodule using map.\n4. REBUS check.\n5. ICG injection (0.75ml).\n6. Handoff to Thoracic Surgery.",
            5: "did the bronch for marking the RUL nodule used the navigation catheter got right to it checked with the radial probe then injected the green dye for the surgeon no problems blood loss nil turned over to surgery team",
            6: "Under general anesthesia, the patient was intubated. A T190 scope was used to inspect the airway, which was normal. The SuperDimension catheter was navigated to the right upper lobe nodule. Position was checked with radial EBUS. ICG dye was injected into the target area to mark it for resection. The scope was removed.",
            7: "[Indication] Pre-op nodule marking.\n[Anesthesia] General.\n[Description] ENB to RUL nodule. REBUS confirmation. ICG dye injection.\n[Plan] Proceed to surgical resection.",
            8: "The patient was intubated for the planned surgical resection. Prior to the surgery, we performed a navigational bronchoscopy. We utilized the electromagnetic map to guide the catheter to the right upper lobe lesion. Radial ultrasound was used for confirmation. We then injected indocyanine green dye to mark the location for the surgeon.",
            9: "Technique: Computer-assisted endoscopic guidance.\nObjective: Pre-surgical tattooing.\nDetails: The RUL lesion was approached via electromagnetic tracking. Sonographic verification was undertaken. Isocyanine green dye was instilled parenchymally."
        },
        3: { # Note 4: EBUS-TBNA (Lung CA Dx) - CPT 31652
            1: "Procedure: EBUS-TBNA.\nStation 11L: 7mm, 6 passes, Lymphocytes.\nLung Mass (LLL): 31.5mm, 8 passes, Malignant.\nDiagnosis: Lung Cancer (ROSE positive).",
            2: "OPERATIVE REPORT: Endobronchial ultrasound-guided transbronchial needle aspiration.\nThe mediastinum and hila were systematically surveyed. A 7mm lymph node at station 11L was sampled, yielding benign lymphocytes. The scope was then advanced to the left lower lobe, where a 31.5mm mass abutting the airway was identified. Fine needle aspiration of the mass confirmed malignancy on rapid on-site evaluation.",
            3: "Billing Codes: 31652 (EBUS-TBNA 1-2 stations).\n- Target 1: Station 11L (Lymph node).\n- Target 2: LLL Lung Mass (Structure abutting airway).\n- Total Stations/Structures: 2.\n- Documentation supports needle gauges, passes, and ROSE results.",
            4: "Procedure: EBUS TBNA\nStations Sampled:\n1. 11L (6 passes)\n2. LLL Mass (8 passes)\nFindings: Extrinsic compression LLL. ROSE positive for cancer in mass.\nComplications: None.",
            5: "did ebus tbna checked all the nodes 11L was the only one big enough stuck it 6 times just lymphocytes then went to the mass in the LLL stuck that 8 times rose saw cancer cells sent everything to path no bleeding",
            6: "The airway was inspected showing extrinsic compression in the LLL. An EBUS scope was introduced. We sampled station 11L and a large mass abutting the left lower lobe bronchus. ROSE confirmed malignancy in the mass. Samples were sent for final pathology and molecular testing.",
            7: "[Indication] Lung Mass.\n[Anesthesia] Moderate.\n[Description] Linear EBUS. Sampled 11L (benign) and LLL Mass (malignant). Extrinsic compression noted.\n[Plan] Oncology referral pending finals.",
            8: "We performed a systematic EBUS examination. Station 11L met criteria for sampling; needle aspiration yielded lymphoid tissue. We then targeted the primary lung mass located in the left lower lobe. Multiple passes were made into the mass, and immediate cytologic evaluation was consistent with malignancy.",
            9: "Intervention: Ultrasonic-guided needle aspiration.\nTargets: Hilar node (11L) and pulmonary tumor.\nOutcome: Cytopathology confirmed carcinoma in the pulmonary mass. The nodal station was negative for metastasis on preliminary review."
        },
        4: { # Note 5: Mucus Plug Removal - CPT 31645
            1: "Indication: Acute respiratory distress/choking.\nProcedure: Emergency Bronchoscopy.\nFindings: Mucus plug in trachea. Adherent mucus in LMS stent (50% obstructed).\nAction: Suctioned trachea and stent. Stent 95% patent post-procedure.\nOutcome: Symptoms resolved.",
            2: "EMERGENT BRONCHOSCOPY NOTE: The patient presented in acute respiratory failure. Immediate bronchoscopic inspection revealed a large mucus plug occluding the trachea, which was aspirated. Further inspection of the left mainstem stent revealed significant inspissated secretions causing partial obstruction. These were cleared via therapeutic aspiration, restoring stent patency. The patient's respiratory status improved immediately.",
            3: "CPT 31645: Bronchoscopy with Therapeutic Aspiration.\nJustification: Patient in acute distress. Procedure required suctioning of thick mucus plugs from trachea and clearance of adherent secretions from LMS stent to restore airway patency. Diagnostic portion bundled.",
            4: "Emergent Procedure Note\nIndication: Choking/Dyspnea.\nAnesthesia: Topical Lidocaine only.\nFindings: Huge plug in trachea. Left stent clogged.\nIntervention: Suctioned everything out.\nResult: Airway clear. Patient stable.",
            5: "patient ran in choking so i grabbed the scope no sedation just lidocaine went down and saw a huge mucus plug in the trachea sucked it out then looked at his stent on the left it was half blocked with mucus sucked that out too he felt better right away sent to ER",
            6: "The patient presented with acute choking. An emergency bronchoscopy was performed at the bedside. A large mucus plug was removed from the trachea. The left mainstem stent was found to be obstructed by mucus and was cleared to near-complete patency. The patient's symptoms resolved.",
            7: "[Indication] Acute Mucus Plugging.\n[Anesthesia] Local/None.\n[Description] Emergent aspiration. Tracheal plug removed. LMS stent cleared of secretions.\n[Outcome] Respiratory distress resolved.",
            8: "This was an emergency procedure for acute airway obstruction. Upon inserting the bronchoscope, we encountered a large mucus plug in the trachea which was immediately aspirated. We then turned our attention to the left mainstem stent, which was occluded by thick secretions. We successfully cleared the stent, resulting in immediate symptomatic improvement.",
            9: "Urgent airway clearance. Inspissated secretions were extracted from the central airway. The bronchial prosthesis was debrided of adherent exudate, restoring luminal patency. Clinical status normalized post-intervention."
        }
    }
    return variations

def get_base_data_mocks():
    # Base data to maintain consistency across variations.
    # We assign a name and age to each of the 5 note indices.
    return [
        {"idx": 0, "orig_name": "Unknown", "orig_age": 65, "names": ["John Doe", "Robert Smith", "Michael Brown", "David Wilson", "James Taylor", "William Anderson", "Richard Thomas", "Joseph Jackson", "Charles White"]}, # Note 1
        {"idx": 1, "orig_name": "Unknown", "orig_age": 60, "names": ["Mary Johnson", "Patricia Williams", "Jennifer Jones", "Linda Miller", "Elizabeth Davis", "Barbara Garcia", "Susan Rodriguez", "Jessica Martinez", "Sarah Hernandez"]}, # Note 2
        {"idx": 2, "orig_name": "Unknown", "orig_age": 70, "names": ["Thomas Moore", "Christopher Martin", "Daniel Lee", "Matthew Perez", "Anthony Thompson", "Donald White", "Mark Harris", "Paul Sanchez", "Steven Clark"]}, # Note 3
        {"idx": 3, "orig_name": "Unknown", "orig_age": 55, "names": ["Lisa Robinson", "Nancy Lewis", "Karen Lee", "Betty Walker", "Helen Hall", "Sandra Allen", "Donna Young", "Carol King", "Ruth Wright"]}, # Note 4
        {"idx": 4, "orig_name": "Unknown", "orig_age": 75, "names": ["Edward Scott", "Brian Green", "Ronald Baker", "Kevin Adams", "Jason Nelson", "Jeffrey Hill", "Ryan Campbell", "Jacob Mitchell", "Gary Roberts"]}  # Note 5
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
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}")
                continue
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update MRN
                if "patient_mrn" in note_entry["registry_entry"]:
                     # If generic UNKNOWN, make a new one, else append
                    if note_entry["registry_entry"]["patient_mrn"] == "UNKNOWN":
                         note_entry["registry_entry"]["patient_mrn"] = f"SYN_PT_{idx}_{style_num}"
                    else:
                        note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
                
                # Update Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update Demographics if present
                if "patient_demographics" in note_entry["registry_entry"]:
                     if note_entry["registry_entry"]["patient_demographics"] is None:
                         note_entry["registry_entry"]["patient_demographics"] = {}
                     note_entry["registry_entry"]["patient_demographics"]["age"] = new_age
                     note_entry["registry_entry"]["patient_demographics"]["name"] = new_name # Usually not in registry, but for completeness
            
            # Add metadata about the synthetic generation
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generated_age": new_age,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_bronch_notes_part_022.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()