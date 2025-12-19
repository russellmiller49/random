import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_065.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock data for names and ages corresponding to the 5 patients 
    in consolidated_verified_notes_v2_8_part_065.json.
    """
    return [
        # Note 0: TBAMWA01 (72M)
        {"idx": 0, "orig_name": "Unknown", "orig_age": 72, "names": ["Robert Ford", "Thomas Anderson", "Arthur Dent", "William Riker", "Henry Jones", "George Jetson", "Edward Stark", "Richard Castle", "James Kirk"]},
        # Note 1: TBAMWA02 (68F)
        {"idx": 1, "orig_name": "Unknown", "orig_age": 68, "names": ["Sarah Connor", "Ellen Ripley", "Leia Organa", "Dana Scully", "Kathryn Janeway", "Laura Roslin", "Kara Thrace", "Nyota Uhura", "Beverly Crusher"]},
        # Note 2: TBAMWA03 (75M)
        {"idx": 2, "orig_name": "Unknown", "orig_age": 75, "names": ["Jean-Luc Picard", "Gandalf Grey", "Albus Dumbledore", "Obi-Wan Kenobi", "Master Yoda", "Professor X", "Magneto", "Spock", "Leonard McCoy"]},
        # Note 3: TBAMWA04 (69F)
        {"idx": 3, "orig_name": "Unknown", "orig_age": 69, "names": ["Hermione Granger", "Katniss Everdeen", "Buffy Summers", "Xena Warrior", "Wonder Woman", "Captain Marvel", "Black Widow", "Scarlet Witch", "Jean Grey"]},
        # Note 4: TBACRYO01 (63M)
        {"idx": 4, "orig_name": "Unknown", "orig_age": 63, "names": ["Tony Stark", "Steve Rogers", "Bruce Banner", "Thor Odinson", "Clint Barton", "Natasha Romanoff", "Nick Fury", "Phil Coulson", "Loki Laufeyson"]},
    ]

def get_variations():
    """
    Returns a dictionary of stylistic variations for the 5 notes.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # TBAMWA01 - RLL MWA
            1: "Procedure: Transbronchial MWA.\nTarget: 18mm RLL nodule.\nAction: Illumisite nav + CBCT. Needle puncture. MWA 10 min/100W.\nResult: 6mm margin. No bleeding.\nPlan: D/C home.",
            2: "OPERATIVE REPORT: The patient, a 72-year-old male with an 18 mm PET-avid nodule in the right lower lobe, underwent electromagnetic navigation bronchoscopy utilizing the Illumisite platform. Following registration and pathway generation, the lesion in the posterior basal segment was targeted. Digital tomosynthesis confirmed alignment. An extended working channel was deployed, and radial EBUS verified a concentric lesion. Microwave ablation was delivered via an Emprint catheter for 10 minutes. Post-procedural cone-beam CT confirmed an adequate ablation zone with a 6 mm margin.",
            3: "CPT 31641: Bronchoscopy with destruction of tumor (MWA).\nCPT +31627: Computer-assisted navigation (Illumisite).\nCPT +31654: Radial EBUS for peripheral lesion.\nDetails: Navigated to RLL posterior basal segment. Confirmed with rEBUS and CBCT. Ablated 18mm lesion using microwave energy.",
            4: "Procedure Note\nResident: Dr. Patel\nAttending: Dr. Rivera\nSteps:\n1. GA/ETT.\n2. Navigated to RLL nodule (Illumisite).\n3. Confirmed with rEBUS (concentric).\n4. Placed Emprint catheter.\n5. Ablated x1 (10 min).\n6. CBCT check: good margin.\nNo complications.",
            5: "Patient 72M RLL nodule likely cancer. Did the microwave ablation today used the illumisite system. Navigated down there rEBUS looked good concentric. Put the needle in then the catheter. Cooked it for 10 mins. CBCT showed a nice burn zone like 6mm margin. No bleeding really. Going home later.",
            6: "A 72-year-old male underwent transbronchial microwave ablation of an 18 mm right lower lobe nodule. Electromagnetic navigation with cone-beam CT guidance was used to localize the target. Radial EBUS confirmed the lesion position. A single 10-minute ablation was performed using an Emprint catheter. Post-ablation imaging demonstrated a satisfactory ablation zone with a 6 mm margin. The patient tolerated the procedure well without immediate complications.",
            7: "[Indication]\n18 mm PET-avid RLL nodule, medically inoperable.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nIllumisite navigation to RLL posterior basal. rEBUS confirmation. MWA 10 min. CBCT confirmed 6mm margin.\n[Plan]\nDischarge home, CT 3 months.",
            8: "The patient presented for treatment of a suspicious right lower lobe nodule. We proceeded with electromagnetic navigation bronchoscopy to localize the 18 mm lesion in the posterior basal segment. Using the Illumisite platform and cone-beam CT, we confirmed the target. Radial EBUS provided further verification. We then inserted a microwave ablation catheter and delivered a 10-minute treatment. Post-ablation imaging showed a successful burn with clear margins.",
            9: "Intervention: Endoscopic destruction of pulmonary tumor.\nMethod: Electromagnetic guidance and microwave energy.\nTarget: Right lower lobe mass.\nAction: The lesion was localized and destroyed using thermal ablation. Verification via tomosynthesis showed effective coverage."
        },
        1: { # TBAMWA02 - RUL Robotic MWA
            1: "Indication: 12mm RUL nodule.\nProcedure: Robotic bronch (Ion), MWA.\nFindings: Apical nodule reached.\nAction: 2 ablations (8+6 min). CBCT confirmed.\nResult: 7mm margin. Stable.\nDisp: Admit.",
            2: "PROCEDURE NOTE: This 68-year-old female with a solitary 12 mm RUL apical nodule underwent robotic-assisted bronchoscopy. The Ion catheter was navigated to the target under shape-sensing guidance. Cone-beam CT and radial EBUS confirmed accurate placement. Transbronchial microwave ablation was performed with two overlapping cycles. Post-ablation imaging revealed a fused ablation zone with a 7 mm circumferential margin.",
            3: "Billing: 31641 (Destruction), 31627 (Navigation), 31654 (rEBUS).\nTechnique: Robotic navigation to RUL apical segment. Microwave ablation of 12mm lesion. Confirmation via CBCT and rEBUS.",
            4: "Resident Note: Robotic MWA\nPatient: TBAMWA02\n1. GA / Ion Robot.\n2. Navigated to RUL apical.\n3. Confirmed with CBCT/rEBUS.\n4. Ablated x2 (Emprint).\n5. Margins good on spin.\nPlan: Admit for obs (single lung).",
            5: "68F with RUL nodule previous lobectomy on other side. Used the Ion robot today. Drove it out to the apical segment. Checked with spin CT and EBUS. Burned it twice 8 and 6 minutes. Looks like we got it all with good margins. She's stable staying overnight just in case.",
            6: "A 68-year-old female underwent robotic-assisted transbronchial microwave ablation for a 12 mm right upper lobe nodule. The Ion platform was used for navigation, confirmed by cone-beam CT and radial EBUS. Two overlapping ablations were delivered. Post-procedural imaging showed a fused ablation zone with a 7 mm margin. The patient was extubated and admitted for observation.",
            7: "[Indication]\n12 mm RUL apical nodule, prior contralateral lobectomy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nRobotic navigation to RUL. MWA x2. CBCT confirmed 7mm margin.\n[Plan]\nAdmit overnight, CT 3 mos.",
            8: "Ms. [Name] underwent a robotic bronchoscopy to treat a nodule in her right upper lobe. We navigated the Ion catheter to the apical segment and confirmed our position with cone-beam CT. We then performed two microwave ablation cycles to destroy the tumor. The final scan showed excellent coverage of the lesion with a safe margin.",
            9: "Procedure: Robotic endoscopic ablation.\nTarget: Apical pulmonary lesion.\nTechnique: Shape-sensing guidance was utilized to reach the target. Thermal destruction was applied via microwave catheter. The treatment zone was verified radiographically."
        },
        2: { # TBAMWA03 - RLL Double MWA
            1: "Indication: 24mm RLL nodule.\nProcedure: Nav bronch, MWA x2.\nFindings: Eccentric lesion on rEBUS.\nAction: 2 ablations (10+7 min). Small pneumo.\nResult: 5-6mm margin. Pneumo obs.\nDisp: Admit.",
            2: "OPERATIVE SUMMARY: A 75-year-old male with a 24 mm RLL superior segment malignancy underwent transbronchial microwave ablation. Electromagnetic navigation (Illumisite) facilitated access. Radial EBUS demonstrated an eccentric relationship. Two overlapping ablation cycles were delivered to ensure complete coverage. Post-ablation CBCT confirmed a 5-6 mm margin. A small, asymptomatic apical pneumothorax was identified and managed conservatively.",
            3: "Codes: 31641, +31627, +31654.\nService: Microwave ablation of RLL tumor.\nDetails: 24mm lesion required two overlapping ablations for coverage. Navigation and rEBUS used for localization. Complication: Small pneumothorax (no chest tube).",
            4: "Procedure: MWA RLL\nSteps:\n1. Navigated to RLL superior.\n2. rEBUS eccentric.\n3. Ablated x2 (10 min, 7 min).\n4. Check CBCT: good zone, small pneumo.\n5. Stable.\nPlan: Admit, CXRs.",
            5: "Patient 75M with the 2.4cm tumor in the RLL. Did the ablation today. Navigated down there needed two burns to cover it all. 10 mins then 7 mins. Looks good on the scan. He popped a lung a little bit small pneumo but hes breathing fine. We'll watch him overnight.",
            6: "Transbronchial microwave ablation was performed on a 75-year-old male with a 24 mm right lower lobe nodule. Electromagnetic navigation and radial EBUS were used for localization. Two sequential ablations were delivered to cover the lesion volume. Post-ablation imaging showed a satisfactory margin. A small apical pneumothorax was noted but did not require intervention. The patient was admitted for observation.",
            7: "[Indication]\n24 mm RLL superior segment cancer.\n[Anesthesia]\nGeneral.\n[Description]\nIllumisite nav. MWA x2 (overlapping). Small pneumothorax noted.\n[Plan]\nAdmit, serial CXRs.",
            8: "We treated a 24 mm tumor in the right lower lobe using microwave ablation. After navigating to the site, we performed two ablation cycles to ensure the entire tumor was treated. The post-procedure scan showed a good safety margin around the tumor. We did notice a small air leak (pneumothorax) on the scan, but it was small enough to watch without inserting a tube.",
            9: "Intervention: Thermal destruction of lung mass.\nLocation: Right lower lobe.\nAction: Dual applications of microwave energy were utilized to encompass the target. A minor pleural air leak was observed and monitored."
        },
        3: { # TBAMWA04 - LLL Biopsy + MWA
            1: "Indication: 16mm LLL nodule.\nProcedure: ENB, Biopsy (frozen: Adeno), MWA.\nFindings: Concentric rEBUS.\nAction: Bx x2 -> MWA 10 min.\nResult: 5mm margin. Mild bleeding.\nDisp: Obs.",
            2: "PROCEDURE NOTE: 69-year-old female with a high-probability LLL nodule. Combined diagnostic and therapeutic bronchoscopy was performed. Navigation and radial EBUS confirmed the lesion position. Transbronchial biopsies yielded adenocarcinoma on frozen section. Immediate microwave ablation was then performed via the same access tract. Post-ablation CBCT confirmed a centered ablation zone with a 5 mm margin.",
            3: "Billing: 31641 (Destruction), +31627 (Nav), +31654 (rEBUS).\nNote: Biopsy (31628/9) bundled if same site/session as destruction? Or separate? *Typically bundled if same target, check local LCD*. Primary service is destruction.",
            4: "Resident Note: Dx + Tx\nPatient: TBAMWA04\n1. Navigated to LLL lateral basal.\n2. Biopsy x2 -> Frozen: Cancer.\n3. Proceeded to MWA (10 min).\n4. Bleeding mild.\n5. Margins looks good.\nPlan: Obs.",
            5: "69F LLL nodule. We went in to biopsy and treat. Got the biopsy first frozen section said adenocarcinoma. So we went ahead and burned it. 10 minutes on the microwave. Bleeding a bit from the biopsy but it stopped. Scan looks decent hard to see exactly with the blood but looks covered.",
            6: "A 69-year-old female underwent same-session biopsy and microwave ablation of a 16 mm left lower lobe nodule. Electromagnetic navigation and radial EBUS were used. Frozen section confirmed adenocarcinoma. A single 10-minute ablation was delivered. Post-ablation imaging showed a 5 mm margin, partially obscured by perilesional hemorrhage. Mild bleeding was self-limited.",
            7: "[Indication]\n16 mm LLL nodule, suspect cancer.\n[Anesthesia]\nGeneral.\n[Description]\nBiopsy confirmed Adeno. Immediate MWA performed (10 min). 5mm margin achieved.\n[Plan]\nObs overnight.",
            8: "This patient underwent a combined procedure for diagnosis and treatment of a left lower lobe nodule. We first navigated to the lesion and took biopsies, which confirmed cancer while the patient was asleep. We then immediately proceeded to treat the tumor with microwave ablation. The procedure went well with only minor bleeding.",
            9: "Procedure: Simultaneous biopsy and ablation.\nTarget: Left lower lobe lesion.\nAction: Tissue sampling confirmed malignancy. Thermal destruction was then applied to the site. Hemostasis was achieved."
        },
        4: { # TBACRYO01 - RLL Cryoablation
            1: "Indication: 15mm RLL nodule.\nProcedure: ENB, Cryoablation.\nFindings: Concentric lesion.\nAction: 3 freeze-thaw cycles (8-5-8). \nResult: Low-attenuation zone on CBCT. 6mm margin.\nDisp: Admit.",
            2: "OPERATIVE REPORT: 63-year-old male with a 15 mm RLL nodule underwent investigational transbronchial cryoablation. Using ENB and CBCT guidance, a flexible cryoprobe was positioned. A triple freeze-thaw protocol was executed. Post-procedural imaging demonstrated a homogeneous ablation zone with ground-glass margins, consistent with effective cryonecrosis.",
            3: "Code: 31641 (Destruction by any method - used for Cryo).\nAdd-ons: 31627, 31654.\nTechnique: Cryoablation (3 cycles) of peripheral lung tumor.\nGuidance: SuperDimension + CBCT.",
            4: "Procedure: Cryoablation\nSteps:\n1. Navigated to RLL lateral basal.\n2. Confirmed position.\n3. Inserted cryoprobe.\n4. Freezes: 8min, 5min, 8min.\n5. CBCT: Ice ball visible.\nNo complications.",
            5: "TBACRYO01 63M RLL nodule. Using the new cryo probe today. Navigated out there. Did three freezes 8 5 and 8 minutes. You can see the ice ball on the CT scan its pretty cool. Got a good margin 6mm. No bleeding no pneumo. Keeping him for the registry.",
            6: "A 63-year-old male underwent transbronchial cryoablation of a 15 mm right lower lobe nodule. Electromagnetic navigation and cone-beam CT were utilized for guidance. Three freeze-thaw cycles were delivered using a flexible cryoprobe. Final imaging showed a well-defined low-attenuation ablation zone with a 6 mm margin. The patient was admitted for monitoring.",
            7: "[Indication]\n15 mm RLL nodule, investigational protocol.\n[Anesthesia]\nGeneral.\n[Description]\nCryoablation x3 cycles. CBCT confirmed ice ball and margin.\n[Plan]\nAdmit, registry follow-up.",
            8: "We performed a cryoablation procedure on Mr. [Name]'s right lower lobe nodule. Instead of heat, we used extreme cold to destroy the tumor. We navigated a special probe to the site and performed three freezing cycles. The scans afterwards showed a nice ice ball covering the tumor with a safe margin.",
            9: "Intervention: Cryogenic destruction of pulmonary mass.\nMethod: Cyclic freezing.\nOutcome: Radiographic evidence of cryonecrosis encompassing the target."
        }
    }
    return variations

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
            # Handle potential missing index in dictionary safely
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}")
                note_entry["note_text"] = "Text generation error."

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_demographics" in note_entry["registry_entry"]:
                    if "age_years" in note_entry["registry_entry"]["patient_demographics"]:
                        note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
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
    output_filename = output_dir / "synthetic_mwa_notes_part_065.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()