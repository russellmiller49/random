import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_052.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the 6 notes in part_052.
    Structure: Note_Index (0-5) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # James Howlett (Pleural Conversion)
            1: "Indication: Empyema suspected.\nProcedure: US guided access. 6F catheter placed -> frank pus. Converted to 14F chest tube via Seldinger. 450cc purulent drainage. tPA/DNase instilled. Tube clamped.\nComplications: None.",
            2: "OPERATIVE REPORT: PLEURAL INTERVENTION\nThe patient presented with signs of pleural sepsis. Ultrasound interrogation of the right hemithorax revealed a complex, loculated effusion. Initial diagnostic thoracentesis yielded frank purulence, necessitating immediate escalation to tube thoracostomy. A 14 French Wayne catheter was sited using the Seldinger technique, draining 450 mL of purulent fluid. To address the loculations, intrapleural fibrinolytic therapy (tPA/DNase) was administered.",
            3: "Primary Service: Tube Thoracostomy (32551).\nSecondary Service: Fibrinolytic Instillation (32561).\nSequence: Diagnostic aspiration (bundled) -> Conversion to therapeutic drainage (billable). \nSite: Right posterior chest.\nDevice: 14Fr Pigtail.\nOutput: 450cc purulent fluid.\nNote: 32555 not billed as it converted to 32551 at same site.",
            4: "Procedure: Chest Tube Placement\nResident: Dr. X\nSteps:\n1. US check: Loculated fluid.\n2. Local lidocaine.\n3. Needle access -> Pus.\n4. Wire placed.\n5. Dilated.\n6. 14Fr chest tube placed.\n7. 10mg tPA / 5mg DNase instilled.\n8. Clamped.",
            5: "Dr Xavier here seeing Mr Howlett for the empyema right side. Started as a tap put in the small catheter got straight pus out so we switched to a chest tube right there. 14 french wayne. Drained about 450 pus. Because of the loculations on the ultrasound we put in tPA and DNase right away. Clamped it. Admitting him.",
            6: "Ultrasound-guided pleural intervention. Initial aspiration yielded frank purulence. Procedure converted to tube thoracostomy. 14 Fr catheter inserted via Seldinger technique. 450 cc purulent fluid evacuated. 10mg tPA and 5mg DNase instilled intrapleurally for loculation management. Tube clamped. Patient stable.",
            7: "[Indication]\nFevers, loculated right pleural effusion, empyema concern.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nDiagnostic thoracentesis revealed pus. Converted to 14Fr chest tube placement. 450cc purulent drainage. Instillation of tPA/DNase.\n[Plan]\nAdmit for empyema protocol.",
            8: "We performed a pleural intervention on Mr. Howlett. Initially, we inserted a small catheter for diagnostic purposes, which revealed frank pus. Consequently, we immediately proceeded to place a 14 French chest tube in the same location to establish drainage. We drained 450cc of fluid. Given the loculations seen on ultrasound, we instilled fibrinolytics (tPA and DNase) directly into the tube before clamping it.",
            9: "Procedure: Thoracostomy conversion.\nAction: The pleural space was accessed. Purulence was aspirated. A drainage catheter was deployed. Effusion was evacuated. Fibrinolytics were administered.\nOutcome: Tube in situ."
        },
        1: { # Logan Roy (Massive Hemoptysis)
            1: "Indication: Massive hemoptysis.\nProc: Rigid bronch. 400cc clot aspirated. RUL bleeding ID'd. Fogarty balloon tamponade x 5 min. APC to tumor bed. Iced saline lavage.\nResult: Hemostasis achieved.",
            2: "OPERATIVE NARRATIVE: EMERGENCY RIGID BRONCHOSCOPY\nIndication: Exsanguinating hemoptysis.\nDescription: The rigid bronchoscope was introduced. Significant clot burden was evacuated from the central airways to restore ventilation. The source was localized to a tumor at the RUL orifice. Hemorrhage control was achieved via a multimodal approach utilizing Fogarty balloon tamponade, thermal ablation (APC) of the tumor bed, and cold saline lavage. The patient was stabilized and extubated.",
            3: "Code 31641: Destruction of tumor (APC to RUL orifice).\nCode 31645: Therapeutic aspiration (400cc blood/clot from trachea/LMS).\nNote: Tamponade is incidental to control. Rigid scope used. General anesthesia.",
            4: "Procedure: Rigid Bronch for Hemoptysis\nAttending: Dr. Roy\nSteps:\n1. GA. Rigid scope in.\n2. Suctioned massive clots (400cc).\n3. Found bleeder RUL.\n4. Balloon tamponade.\n5. APC to tumor.\n6. Iced saline.\nBleeding stopped.",
            5: "Emergency bronch for Logan Roy massive bleeding. Rigid scope. Tube was full of blood sucked out like 400cc just to see. Bleeding coming from RUL tumor. Put a balloon in there to block it for a bit then hit it with APC. Used iced saline too. Stopped bleeding. Extubated in room.",
            6: "Emergency rigid bronchoscopy performed for massive hemoptysis. 400 cc blood/clot aspirated from central airways. Active bleeding RUL tumor. Interventions: Fogarty balloon tamponade, Argon Plasma Coagulation to tumor bed, iced saline lavage. Hemostasis achieved. Extubated.",
            7: "[Indication]\nMassive hemoptysis, RUL SCC.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nEvacuation of 400cc clot. Balloon tamponade RUL. APC destruction of bleeding tumor. Iced saline.\n[Plan]\nICU admission.",
            8: "Mr. Roy required emergency rigid bronchoscopy for massive hemoptysis. We first cleared the airway of approximately 400cc of clot to ventilate him. Identifying the bleeding source at the RUL tumor, we deployed a Fogarty balloon for tamponade. Subsequently, we applied APC to the tumor bed to cauterize the vessels and instilled iced saline. These measures successfully halted the bleeding.",
            9: "Procedure: Rigid endoscopy with hemorrhage control.\nAction: Clot was evacuated (Therapeutic Aspiration). The hemorrhage source was localized. Tamponade was applied. The lesion was cauterized (Destruction). Lavage performed.\nOutcome: Hemostasis."
        },
        2: { # Wade Wilson (Mixed Modality)
            1: "Proc: EBUS, Nav Cryobiopsy, Central Resection.\nEBUS: 4R, 7 sampled (neg).\nLUL: Navigated cryobiopsy x3 (nodule).\nRMB: Incidental tumor resected (snare/APC).\nComp: None.",
            2: "OPERATIVE REPORT: MULTI-MODALITY INTERVENTION\nIndication: Staging and diagnosis.\nEBUS: Stations 7 and 4R were sampled; ROSE negative.\nPeripheral: Using the Ion platform and radial EBUS, the LUL nodule was localized. Transbronchial cryobiopsy was performed.\nCentral: Inspection revealed an incidental obstructive lesion in the RMB. This was resected using electrocautery snare and APC base destruction to restore patency.",
            3: "Coding:\n- 31652: EBUS (Stn 7, 4R).\n- 31627+31628: Navigated Cryobiopsy LUL nodule.\n- 31654: Radial EBUS LUL.\n- 31641: Destruction of RMB tumor (Snare/APC). Distinct target from LUL.\nModifiers required.",
            4: "Procedure: EBUS / Ion / Resection\nPatient: Wade Wilson\nSteps:\n1. EBUS TBNA 7, 4R.\n2. Ion nav to LUL. Radial EBUS verify. Cryobiopsy x3.\n3. Found RMB polyp. Snared and APC'd it.\nNo issues.",
            5: "Busy case for Mr Wilson. Started with EBUS 7 and 4R negative. Then used the robot to get the LUL nodule froze it 3 times. On the way out saw a huge polyp in the right main. Snared it off and APCd the base. 3 separate procedures basically. Patient fine.",
            6: "Flexible bronchoscopy with EBUS-TBNA, robotic navigation, and therapeutic resection. EBUS performed at 4R/7. Robotic navigation with radial EBUS to LUL nodule; cryobiopsy obtained. Incidental RMB tumor identified and resected via snare electrocautery and APC. No complications.",
            7: "[Indication]\nStaging, LUL nodule.\n[Anesthesia]\nGeneral.\n[Description]\n1. EBUS-TBNA 4R, 7.\n2. Navigated cryobiopsy LUL nodule (w/ REBUS).\n3. Snare resection/APC of incidental RMB tumor.\n[Plan]\nDischarge.",
            8: "We performed a complex procedure on Mr. Wilson. First, we staged the mediastinum using EBUS. Next, we used the Ion robot to navigate to and cryobiopsy a nodule in the LUL. Unexpectedly, we found a separate tumor obstructing the Right Mainstem Bronchus. We resected this central tumor using a snare and APC. All three targets were distinct.",
            9: "Procedure: Staging, targeted biopsy, and tumor ablation.\nSites: Mediastinum, LUL, RMB.\nAction: Nodes were aspirated. The peripheral lesion was sampled via cryoprobe. The central obstruction was resected and cauterized.\nOutcome: Multiple targets addressed."
        },
        3: { # F. N. Stein (Stent Exchange)
            1: "Indication: Stent obstruction (granulation).\nProc: Rigid bronch. Proximal granulation cored. Stent removed. Distal granulation treated (APC/Cryo). New 14x40mm silicone stent placed.\nResult: Airway patent.",
            2: "OPERATIVE NARRATIVE: TRACHEAL STENT REVISION\nThe patient presented with symptoms of stent obstruction. Rigid bronchoscopy revealed significant granulation tissue at the proximal and distal ends of the indwelling silicone stent. The device was removed following coring of the proximal tissue. The distal stent bed was treated with APC and cryotherapy to address granulomas. A replacement 14x40mm silicone stent was then deployed in the same anatomical position.",
            3: "Code: 31638 (Revision of tracheal stent).\nRationale: Procedure constitutes a replacement of an existing stent at the same site. Removal of the old stent and therapeutic prep of the airway (APC/Cryo) are bundled into the revision code.",
            4: "Procedure: Stent Exchange\nAttending: Dr. Stein\nSteps:\n1. Rigid scope.\n2. Cored granulation.\n3. Removed old stent.\n4. Cleaned base with APC/Cryo.\n5. Placed new 14x40mm stent.\nEBL 10cc.",
            5: "Dr Stein here. Patient with the tracheal stent has bad breath. Stent was full of granulation. Went in with the rigid took the old one out. Used APC and cryo to clean up the mess at the bottom. Put a fresh 14 by 40 in there. Looks much better.",
            6: "Rigid bronchoscopy for tracheal stent revision. Indication: Granulation tissue obstruction. Old stent removed. Granulation tissue debrided via coring, APC, and cryotherapy. New 14x40mm silicone stent deployed. Airway patent.",
            7: "[Indication]\nBenign tracheal stenosis, stent obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nRemoval of obstructed silicone stent. Ablation of granulation tissue (APC/Cryo). Placement of new 14x40mm silicone stent.\n[Plan]\nDischarge.",
            8: "We performed a stent exchange for this patient. The existing silicone stent was encrusted with granulation tissue. We used the rigid bronchoscope to core out the tissue and remove the stent. After treating the inflamed mucosa with APC and cryotherapy, we placed a brand new silicone stent of the same size in the trachea.",
            9: "Procedure: Prosthesis revision.\nIndication: Stent failure.\nAction: The existing prosthesis was extracted. The tissue bed was ablated. A replacement prosthesis was inserted.\nOutcome: Revision complete."
        },
        4: { # Unknown (Cryo-Ablation vs Biopsy)
            1: "Proc: RLL Mass Ablation + LUL Nodule Biopsy.\nRLL: Squamous CA. Cryo-ablation x5 cycles. Tissue discarded. 80% patency.\nLUL: New nodule. Radial EBUS. Cryobiopsy x2 sent to path.\nCodes: 31641, 31628, 31654.",
            2: "OPERATIVE REPORT: THERAPEUTIC AND DIAGNOSTIC BRONCHOSCOPY\nThe patient presented with a known RLL obstructing mass and a new LUL nodule. \n1. RLL: The cryoprobe was used to therapeutically debulk the endobronchial tumor via freeze-thaw cycles. Extracted tissue was discarded as the diagnosis is established. \n2. LUL: The scope was advanced to the LUL. Radial EBUS confirmed the target. Diagnostic cryobiopsies were obtained and submitted for analysis.",
            3: "Code 31641: RLL Tumor Destruction (Cryo-ablation/debulking).\nCode 31628: LUL Transbronchial Biopsy (Cryo-biopsy).\nCode 31654: Radial EBUS (LUL).\nDifferentiation: RLL intervention was therapeutic (tissue discarded). LUL intervention was diagnostic (tissue sent).",
            4: "Procedure: Cryo Ablation and Biopsy\nSteps:\n1. RLL mass: Frozen/removed x5. Cleared airway.\n2. LUL nodule: Found with REBUS. Biopsied x2.\nPath sent for LUL only.",
            5: "Two part procedure today. First the RLL mass we know its cancer so I just cryo'd it to open the airway threw the tissue away. Then went to the LUL for that new spot. Used the radar to find it and took two biopsies sent those to the lab. Codes are 31641 and 31628.",
            6: "Therapeutic bronchoscopy RLL; Diagnostic bronchoscopy LUL. RLL squamous cell carcinoma debulked via cryotherapy (tissue discarded). LUL nodule localized via radial EBUS and biopsied via cryoprobe (tissue submitted). No complications.",
            7: "[Indication]\nRLL obstruction, LUL nodule.\n[Anesthesia]\nModerate.\n[Description]\n1. Cryo-ablation of RLL mass (therapeutic).\n2. Radial EBUS localization LUL.\n3. Cryobiopsy LUL nodule (diagnostic).\n[Plan]\nPathology pending for LUL.",
            8: "We addressed two issues today. For the known RLL tumor, we performed therapeutic debulking using the cryoprobe to open the airway, discarding the tissue. Then, we investigated the new LUL nodule, verifying its location with radial EBUS and obtaining diagnostic biopsies which were sent to pathology.",
            9: "Procedure: Tumor ablation and parenchymal sampling.\nSites: RLL, LUL.\nAction: The RLL mass was destructed via cryotherapy. The LUL lesion was localized and sampled.\nOutcome: Airway patent, samples collected."
        },
        5: { # Unknown (RMB Incidental Finding - Wade Wilson Context Duplicate/Variant)
            1: "Note: This appears to be a variant of the Wade Wilson case emphasizing the RMB incidental finding.\nProc: Staging + LUL Biopsy + RMB Resection.\nDetails: EBUS 7/4R neg. LUL cryobiopsy. RMB polyp snared/APC'd.\nResult: 3 distinct services.",
            2: "OPERATIVE REPORT: INCIDENTAL CENTRAL AIRWAY TUMOR\nDuring the course of a staging EBUS and LUL nodule biopsy, inspection of the right mainstem bronchus revealed an unexpected polypoid lesion causing obstruction. Following the planned LUL cryobiopsy and EBUS staging, this RMB lesion was resected using a snare and APC to ensure airway patency. This represents a distinct therapeutic intervention.",
            3: "Coding Logic:\n- 31641: RMB Resection (Snare/APC).\n- 31628: LUL Biopsy (Cryo).\n- 31652: EBUS Staging.\nKey: The RMB resection is a separate therapeutic service from the diagnostic work in the LUL and mediastinum.",
            4: "Procedure: Bronchoscopy\nSteps:\n1. EBUS staging.\n2. LUL biopsy (Ion).\n3. RMB lesion found -> Snared and APC'd.\nSeparate sites, separate tools.",
            5: "Went in for staging and the LUL nodule but found a polyp in the right main. So we did the EBUS and the LUL biopsy first. Then came back and cut out the RMB polyp with a snare and burned the base. Unexpected but necessary.",
            6: "Complex bronchoscopy. 1. EBUS-TBNA (staging). 2. Navigated cryobiopsy (LUL nodule). 3. Therapeutic resection of incidental RMB tumor (Snare/APC). All procedures performed successfully.",
            7: "[Indication]\nStaging, LUL nodule, Incidental RMB mass.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA. LUL Cryobiopsy. Snare resection of RMB tumor.\n[Plan]\nMonitor.",
            8: "During a standard staging and biopsy case, we encountered an incidental tumor in the right mainstem bronchus. We proceeded with the planned EBUS and LUL biopsy. Afterwards, we addressed the RMB tumor by resecting it with a snare and treating the base with APC, effectively clearing the central airway.",
            9: "Procedure: Multi-target bronchoscopy.\nAction: Nodal staging performed. Peripheral lesion sampled. Central airway tumor resected.\nOutcome: Complete staging and airway clearance."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for names/ages/dates to simulate reading from a master source.
    Indices match the notes in the JSON file.
    """
    return [
        {"idx": 0, "orig_name": "James Howlett", "orig_age": 55, "names": ["Logan Wolverine", "Jack Howlett", "James Logan", "Wolverine X", "Weapon X", "Logan H.", "James L.", "Old Man Logan", "Patch"]},
        {"idx": 1, "orig_name": "Logan Roy", "orig_age": 77, "names": ["Kendall Roy", "Roman Roy", "Connor Roy", "Ewan Roy", "L. Roy", "Brian Cox", "Waystar Roy", "Logan R.", "King Lear"]},
        {"idx": 2, "orig_name": "Wade Wilson", "orig_age": 45, "names": ["Ryan Reynolds", "Slade Wilson", "W. Wilson", "Merc Mouth", "Wade W.", "Pool Dead", "Regenerating Degenerate", "Weapon XI", "Van Wilder"]},
        {"idx": 3, "orig_name": "Unknown", "orig_age": 50, "names": ["Frank Stein", "Victor Frankenstein", "Monster Herman", "Boris Karloff", "Mary Shelley", "F. Stein", "Prometheus Modern", "Adam Frankenstein", "Creature"]},
        {"idx": 4, "orig_name": "Unknown", "orig_age": 60, "names": ["John Doe", "Jane Doe", "Patient X", "Unknown Subject", "Mystery Patient", "Anonymous A", "No Name", "Blank Slate", "Placeholder"]},
        {"idx": 5, "orig_name": "F. N. Stein", "orig_age": 50, "names": ["Gene Wilder", "Peter Boyle", "Marty Feldman", "Igor Eye", "Frau Blucher", "H. Delbruck", "Fredrick Fronkensteen", "Elizabeth Lavenza", "Kemp Inspector"]} # Using this slot for the variant/duplicate logic or just as a placeholder for the last note in the dict.
    ]

def main():
    # Load original data from source file
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
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
            # Fallback if source has more notes than mock data
            record = {"orig_age": 50, "names": [f"Patient_{idx}_{i}" for i in range(1, 10)]}
        else:
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
            
            # Get the specific name assigned in base_data
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: No text variation found for note {idx}, style {style_num}")
            
            # Update registry_entry fields if they exist to match the "new" patient
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            
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
    output_filename = output_dir / "synthetic_edge_case_notes_part_052.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()