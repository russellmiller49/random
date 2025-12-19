import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_024.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Dictionary holding manually crafted text variations for the 5 notes in bronch_notes_part_024.json
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Note 0: Emergent Mucus Plug (31645)
            1: "Indication: Acute respiratory failure/choking.\nProcedure: Emergent bronchoscopy. No sedation.\nFindings: Thick mucus plug in trachea. Left mainstem stent 50% obstructed by mucus.\nAction: Suctioned trachea. Cleared stent to 95% patency.\nOutcome: Symptoms resolved.",
            2: "HISTORY: The patient presented emergently to the bronchoscopy suite with acute respiratory distress and stridor immediately following a clinic visit. \nPROCEDURE: Flexible bronchoscopy was performed without sedation due to the acuity of the event. Topical anesthesia was achieved with 1% lidocaine. Upon insertion, a dense mucus plug was visualized obstructing the trachea and was successfully aspirated. Further examination revealed the left mainstem stent was partially occluded (approx. 50%) by tenacious secretions. Thorough suctioning was performed, restoring stent patency to 95%.\nIMPRESSION: Acute airway obstruction secondary to mucus plugging, resolved with therapeutic aspiration.",
            3: "Service: Therapeutic Bronchoscopy (31645).\nIndication: Acute Respiratory Failure.\nTechnique: Scope introduced nasally. Therapeutic aspiration performed in trachea and left mainstem bronchus.\nFindings: Mucus plugging in central airways. Left mainstem stent found 50% occluded by secretions; cleared to 95% patency via suction. No tumor destruction or stent manipulation performed (supports 31645, excludes 31638).",
            4: "Procedure: Emergency Flexible Bronchoscopy\nIndication: Choking/Respiratory Distress\nSedation: None (Emergent)\nSteps:\n1. Lidocaine applied to nares/cords.\n2. Scope inserted.\n3. Large mucus plug identified in trachea -> Suctioned.\n4. Left mainstem stent inspected; found 50% occluded with mucus.\n5. Stent suctioned clear (95% patent).\n6. Patient stabilized.",
            5: "Patient ran into the room choking said he couldnt breathe so we took him right to the bronch room no time for sedation used some lidocaine scope went in right nose saw a huge mucus plug in the trachea sucked it out then looked down the left side the stent was clogged up with mucus too about halfway blocked cleaned that out too until it was open again patient felt better right away sent him to the ER to be safe.",
            6: "Emergent flexible bronchoscopy was performed for acute respiratory failure. Patient presented choking. 18cc Lidocaine used. No sedation. Scope passed via right naris. Thick mucus plug visualized in trachea and aspirated. Further inspection revealed left mainstem stent 50% occluded by adherent mucus. Therapeutic aspiration performed clearing stent to 95% patency. Airways otherwise patent. Procedure terminated as symptoms resolved. Patient transferred to ED.",
            7: "[Indication]\nAcute respiratory failure, choking sensation.\n[Anesthesia]\nLocal (Lidocaine) only; no sedation due to urgency.\n[Description]\nEmergent airway inspection revealed thick mucus plugging in trachea. This was aspirated. Left mainstem stent found 50% obstructed by inspissated mucus. Therapeutic aspiration performed, restoring lumen to 95%. \n[Plan]\nTransfer to ED for monitoring.",
            8: "The procedure was conducted emergently after the patient presented with signs of choking. We utilized topical lidocaine but bypassed sedation given the severity of his distress. The bronchoscope was introduced, immediately identifying a large mucus plug within the trachea which was cleared. We continued to the left side, where the existing left mainstem stent was noted to be significantly obstructed by thick secretions. We performed extensive suctioning, effectively recanalizing the stent to near-total patency. The patient's breathing improved markedly immediately following the intervention.",
            9: "REOPERATIVE DIAGNOSIS: Acute respiratory failure\nPROCEDURE: Flexible bronchoscopy\nDETAILS: The procedure was executed emergently. The patient presented with choking. Lidocaine was applied. The scope was inserted. A dense mucus plug was observed in the trachea and extracted. The left mainstem stent was found partially blocked by sticky mucus. This was cleared, achieving 95% patency. The patient's status improved immediately."
        },
        1: { # Note 1: Ion/Fiducial/TBNA LUL & Lingula (31626, 31629, 31628, +31627, +31654)
            1: "Indication: Lung nodules.\nTechnique: Robotic Bronchoscopy (Ion), rEBUS, CBCT.\nTargets:\n1. Lingula (LB4): 1cm nodule. rEBUS eccentric. Fiducial placed. TBNA x4, TBBX x1, Cryo x6, Brush, BAL.\n2. LUL Anterior (LB3): 1cm nodule. rEBUS eccentric. TBNA x6, BAL. Cryo attempted/failed.\nEBUS: Stations 4L, 7 inspected (benign). No sampling.\nROSE: Malignant.",
            2: "OPERATIVE SUMMARY: The patient underwent robotic-assisted navigational bronchoscopy for evaluation of bilateral pulmonary nodules. The Ion platform was utilized. Target 1 (Lingula) was localized via radial EBUS (eccentric view) and Cone Beam CT. Transbronchial needle aspiration, forceps biopsy, cryobiopsy, and brushing were performed. A fiducial marker was deployed. Target 2 (LUL Anterior) was similarly localized; TBNA and BAL were obtained. Linear EBUS inspection of stations 4L and 7 revealed benign sonographic features; no nodal sampling was required.",
            3: "Billing Summary:\n- 31626: Placement of fiducial markers (Lingula).\n- 31629: TBNA of LUL Anterior nodule (Initial TBNA).\n- 31628: Transbronchial biopsy of Lingula nodule (Separate lesion, Modifier 59).\n- 31627: Navigation add-on.\n- 31654: Radial EBUS add-on.\n- Note: Linear EBUS inspection (31622) bundled. 31645 bundled.",
            4: "Resident Procedure Note\nProcedure: Ion Robotic Bronchoscopy, EBUS.\nTargets: Lingula & LUL Anterior.\nSteps:\n1. EBUS inspection 4L, 7 (benign, not sampled).\n2. Ion navigation to Lingula nodule. rEBUS eccentric.\n3. Biopsies: Needle, Forceps, Cryo, Brush.\n4. Fiducial placed in Lingula.\n5. Nav to LUL Anterior. rEBUS eccentric.\n6. Biopsies: Needle only. Cryo failed.\n7. ROSE: Malignant.",
            5: "We did a robotic bronch on this lady for lung nodules used the Ion system first went to the lingula found the spot on radar and cone beam ct put a needle in it then forceps and cryo probe also a brush and placed a fiducial marker rose said cancer then we went to the LUL anterior segment found that one too did needle biopsies cryo didnt work there washed it out ebus looked at the lymph nodes 4L and 7 they looked fine so we didn't stick them.",
            6: "General anesthesia. Ion robotic bronchoscopy performed. Target 1 Lingula: Radial EBUS eccentric. CBCT confirmation. TBNA, Forceps, Cryobiopsy, Brush performed. Fiducial marker placed. Target 2 LUL Anterior: Radial EBUS eccentric. TBNA performed. Cryo unsuccessful. Linear EBUS performed for staging: Stations 4L and 7 visualized, appeared benign, not sampled. ROSE consistent with malignancy.",
            7: "[Indication]\nLung nodules (Lingula, LUL Anterior).\n[Anesthesia]\nGeneral.\n[Description]\n1. Linear EBUS: Stations 4L, 7 assessed (benign).\n2. Ion Nav to Lingula: rEBUS eccentric. Samples: TBNA, TBBX, Cryo, Brush. Fiducial placed.\n3. Ion Nav to LUL Anterior: rEBUS eccentric. Samples: TBNA.\n[Plan]\nFollow up pathology.",
            8: "The patient was placed under general anesthesia for evaluation of lung nodules. We began with linear EBUS, inspecting stations 4L and 7, which appeared benign and were not sampled. We then utilized the Ion robotic platform to navigate to a nodule in the Lingula. Confirmation was achieved with radial EBUS and Cone Beam CT. We obtained samples via needle, forceps, cryoprobe, and brush, and placed a fiducial marker. We then navigated to a second target in the LUL anterior segment, obtaining needle aspirates. ROSE confirmed malignancy.",
            9: "Indication: Lung nodules.\nProcedure: Robotic navigation and sampling.\nDetails: The Lingula lesion was localized. We sampled it using needle, forceps, and cryoprobe. A marker was deployed. The LUL anterior lesion was then engaged and aspirated with a needle. Linear EBUS was used to visualize mediastinal nodes, which were not sampled due to benign appearance."
        },
        2: { # Note 2: Ion/RLL/EBUS Sampling (31653, 31626, 31629, 31628, 31623, 31624, +31627, +31654)
            1: "Indication: RLL Nodule.\nProcedure: Ion Bronch + EBUS.\nEBUS: Sampled 11L, 7, 11Rs (TBNA).\nNav: RLL (RB10) nodule. rEBUS concentric.\nBiopsies: TBNA x6, TBBX x1, Cryo x6, Brush, BAL.\nFiducial: Placed in RLL.\nROSE: Suspicious for malignancy.",
            2: "OPERATIVE REPORT: The patient presented for evaluation of a 1.5 cm RLL nodule. Robotic navigation (Ion) was utilized to localize the target in the posterior-basal segment (RB10). Radial EBUS showed a concentric view. We performed extensive sampling including TBNA, forceps biopsy, cryobiopsy, and brushing. A fiducial marker was deployed. Staging was performed via linear EBUS with TBNA of stations 7, 11L, and 11Rs.",
            3: "Billing Codes Supported:\n- 31653: EBUS sampling 3+ nodes (7, 11L, 11R).\n- 31626: Fiducial placement (RLL).\n- 31629: Navigated TBNA (RLL) - Mod 59.\n- 31628: TBBX (RLL) - Mod 59.\n- 31623: Brushing.\n- 31624: BAL.\n- 31627: Navigation.\n- 31654: Radial EBUS.",
            4: "Procedure Note\nPatient: Leticia Rayos.\nProc: Ion Bronchoscopy + EBUS.\n1. EBUS-TBNA of stations 11L, 7, 11Rs.\n2. Navigation to RLL (RB10). rEBUS concentric.\n3. Samples: Needle, Forceps, Cryo, Brush.\n4. Fiducial placed.\n5. ROSE: Suspicious for malignancy.",
            5: "Leticia came in for a lung nodule on the right side we used the robot to get there found it with the radar and the spinny CT scan took a bunch of samples needle forceps cryo brush and put a seed in there for radiation later then we did the ebus and sampled lymph nodes 7 11L and 11R everything went fine patient woke up okay.",
            6: "General anesthesia. Ion robotic bronchoscopy. Target: RLL posterior-basal segment. Radial EBUS: Concentric. CBCT confirmation. Biopsies: TBNA, Forceps, Cryo, Brush. Fiducial marker placed. Linear EBUS staging performed: TBNA of stations 7, 11L, and 11Rs. ROSE: Suspicious for malignancy. No complications.",
            7: "[Indication]\nRLL Nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to RLL target. Confirmed with rEBUS/CBCT. Performed TBNA, TBBX, Cryo, Brush. Placed fiducial. Performed EBUS-TBNA of nodes 7, 11L, 11Rs.\n[Plan]\nOncology referral pending path.",
            8: "We performed a combined robotic bronchoscopy and EBUS procedure. The EBUS scope was used first to sample lymph node stations 7, 11L, and 11Rs for staging. We then switched to the Ion robotic catheter, navigating to the target lesion in the right lower lobe. Once localized with radial EBUS and cone beam CT, we obtained diagnostic tissue using a variety of tools including needle, forceps, and cryoprobe. A fiducial marker was placed at the site prior to withdrawal.",
            9: "Indication: Pulmonary nodule.\nProcedure: Robotic navigation and nodal staging.\nActions: We navigated to the RLL lesion. The lesion was sampled via needle, forceps, cryo, and brush. A marker was deployed. We then staged the mediastinum by aspirating nodes at stations 7, 11L, and 11Rs."
        },
        3: { # Note 3: Rick Smith (Sarcoid?) - 31652, 31628, 31625, 31624, +31654
            1: "Indication: Lung infiltrates (Sarcoid?).\nProcedure: Flex Bronch + EBUS.\nFindings: Mucosa nodular (NBI).\nActions:\n- BAL RML.\n- EBBX: RUL, RML, Lingula carinas.\n- Radial EBUS LLL: Concentric.\n- TBBX LLL (LB10).\n- Linear EBUS: Station 7 sampled (8 passes). 11R/11L inspected.\nResult: Stable.",
            2: "PROCEDURE NOTE: Bronchoscopy was performed for evaluation of suspected sarcoidosis. Airway inspection with NBI revealed diffuse nodular changes. Endobronchial biopsies were taken from the RUL, RML, and Lingula carinas. BAL was performed in the RML. Radial EBUS was used to localize a target in the LLL, followed by transbronchial forceps biopsies. Linear EBUS was utilized to inspect stations 4R, 4L, 7, 10R, 10L, 11R, 11L. Only station 7 met criteria for sampling and was biopsied via TBNA.",
            3: "CPT Justification:\n- 31652: EBUS sampling 1-2 nodes (Station 7 sampled).\n- 31628: TBBX Single Lobe (LLL).\n- 31625: Endobronchial biopsy (Multiple carinas).\n- 31624: BAL (RML).\n- 31654: Radial EBUS (LLL).\n- 31645: Bundled (mucus aspiration).",
            4: "Resident Note\nPatient: Rick Smith, 32M.\nDx: Infiltrates/Sarcoid.\nSteps:\n1. Airway exam: Nodular mucosa.\n2. BAL RML.\n3. EBBX carinas (RUL, RML, Lingula).\n4. Radial EBUS LLL (concentric).\n5. TBBX LLL.\n6. Linear EBUS: Sampled station 7. Inspected others.",
            5: "Young guy Rick Smith here for infiltrates maybe sarcoid we put him to sleep looked inside airways looked bumpy with the special light so we biopsied the carinas on both sides did a wash in the middle lobe then went down to the left lower lobe used the radar probe found the spot took biopsies then used the ebus scope to sample the subcarinal lymph node station 7 others looked okay so we left them alone.",
            6: "General anesthesia. Flexible bronchoscopy. NBI showed nodular mucosa. BAL performed RML. Endobronchial biopsies taken from RUL, RML, Lingula carinas. Radial EBUS LLL posterior basal segment: Concentric view. Transbronchial biopsies LLL performed. Linear EBUS performed. Station 7 sampled (8 passes). Stations 11R and 11L inspected but not sampled. No complications.",
            7: "[Indication]\nLung infiltrates, r/o Sarcoid.\n[Anesthesia]\nGeneral.\n[Description]\n1. BAL RML.\n2. EBBX: RUL, RML, Lingula carinas.\n3. rEBUS LLL -> TBBX LLL.\n4. EBUS-TBNA Station 7.\n[Plan]\nClinic f/u.",
            8: "Mr. Smith underwent bronchoscopy for evaluation of lung infiltrates. We noted nodular mucosal changes and performed endobronchial biopsies at multiple carinas. A bronchoalveolar lavage was conducted in the right middle lobe. We then directed our attention to the left lower lobe, using radial EBUS to guide transbronchial biopsies. Finally, we performed EBUS staging, sampling the subcarinal node (station 7) while inspecting other stations which did not require biopsy.",
            9: "Indication: Lung infiltrates.\nProcedure: Diagnostic bronchoscopy.\nActions: We washed the RML. We biopsied the mucosa at several carinas. We utilized radial ultrasound to locate the LLL target and sampled it with forceps. We employed linear ultrasound to aspirate the subcarinal lymph node."
        },
        4: { # Note 4: Michael Jordan - Pleural (32561)
            1: "Indication: Complicated pleural effusion.\nProcedure: Intrapleural fibrinolysis (Day 1).\nAction: Instilled 10mg tPA / 5mg DNase via existing chest tube.\nComplications: None.\nPlan: Continue protocol.",
            2: "PROCEDURE NOTE: Bedside instillation of fibrinolytic agents. The patient has a indwelling right-sided chest tube for a complex parapneumonic effusion. Sterile technique was maintained. A solution containing 10 mg tPA and 5 mg DNase was instilled via the chest tube. The tube was clamped according to protocol. The patient tolerated the procedure without adverse events.",
            3: "Billing Code: 32561 (Instillation of fibrinolytic agent, initial day).\nDate of Service: 12/16/2025.\nMedication: tPA 10mg / DNase 5mg.\nAccess: Existing chest tube (placed 12/15/2025).\nDiagnosis: Complicated pleural effusion.",
            4: "Procedure: Fibrinolytic Instillation\nPatient: Michael Jordan, 47M.\nTube: Right chest tube.\nMeds: tPA/DNase.\nDose: Initial.\nSteps: Meds instilled, tube clamped. Vitals stable.",
            5: "Went to see Mr Jordan for his chest tube put in the tpa and dnase for his empyema dose number one clamp the tube for a while he did fine no pain or bleeding will do it again tomorrow.",
            6: "Instillation of agents for fibrinolysis via chest tube. Patient with complex pleural effusion. Chest tube placed yesterday. 10mg tPA and 5mg DNase instilled. Tube clamped. Patient monitored. No complications. Disposition: Home/Floor.",
            7: "[Indication]\nComplicated pleural effusion.\n[Anesthesia]\nNone.\n[Description]\nInstilled tPA/DNase via right chest tube (Initial day).\n[Plan]\nUnclamp in 1 hour. Repeat dosing per protocol.",
            8: "Mr. Jordan requires fibrinolytic therapy for a loculated pleural effusion. We visited him at the bedside today to administer the first dose. We instilled tPA and DNase through his existing right chest tube without difficulty. The patient denied discomfort. We will continue with the fibrinolysis protocol.",
            9: "Indication: Pleural effusion.\nProcedure: Administration of fibrinolytics.\nAction: We injected tPA and DNase into the pleural space via the catheter. This was the primary treatment session. The catheter was secured."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the prompt's examples
    # Note: Source file has 5 notes.
    return [
        {"idx": 0, "orig_name": "Unknown (Emergent)", "orig_age": 60, "names": ["John Doe", "Arthur Dent", "Robert Paulson", "William Riker", "James Kirk", "Edward Nygma", "Richard Grayson", "Thomas Wayne", "Gary Oak"]},
        {"idx": 1, "orig_name": "Erica Nunley", "orig_age": 88, "names": ["Sarah Connor", "Linda Hamilton", "Nancy Wheeler", "Karen Page", "Barbara Gordon", "Mary Watson", "Susan Storm", "Margaret Carter", "Betty Ross"]},
        {"idx": 2, "orig_name": "Leticia Rayos", "orig_age": 58, "names": ["Michelle Yeoh", "Roberta Draper", "Davina Claire", "Josephine March", "Francine Smith", "Paula Patton", "Georgette Costanza", "Kelly Kapowski", "Stephanie Tanner"]},
        {"idx": 3, "orig_name": "Rick Smith", "orig_age": 32, "names": ["Mario Rossi", "Patrick Star", "Elijah Wood", "Jeremy Piven", "Liam Neeson", "Benjamin Linus", "Daniel LaRusso", "Harry Potter", "Carl Winslow"]},
        {"idx": 4, "orig_name": "Michael Jordan", "orig_age": 47, "names": ["James Bond", "William Wallace", "Thomas Anderson", "Charles Xavier", "Donald Draper", "Mark Hamill", "Paul Atreides", "George Costanza", "Kenneth Parcell"]},
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
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}")
                note_entry["note_text"] = "VARIATION_MISSING"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_demographics" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                # Fallback if age is at root of registry_entry (some formats vary)
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    if base_mrn == "UNKNOWN" or base_mrn == "Unknown":
                        base_mrn = f"IP202603{idx}" # Invent a base if unknown
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"

            # Add metadata about the synthetic generation
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_bronch_notes_part_024.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()