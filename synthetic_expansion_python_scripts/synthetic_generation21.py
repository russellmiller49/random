import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_021.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the notes found in bronch_notes_part_021.json.
    Structure: Note_Index -> Style_Index -> Text
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
        0: { # Note 0: EBUS + LUL Nodule + DECAMP research
            1: "Procedure: EBUS, LUL biopsy, DECAMP protocol.\nFindings: Normal airway. 4R sampled (neg). LUL nodule: eccentric rEBUS view. Biopsied (forceps/brush) - neg. Research samples taken RUL/RML/LUL.\nComplications: None. EBL 10cc.\nPlan: PACU, D/C.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the endoscopy suite for evaluation of a left upper lobe pulmonary nodule. Following the induction of general anesthesia, a comprehensive airway inspection revealed normal anatomy barring a fused LUL anterior segment. EBUS was utilized for mediastinal staging; station 4R met sampling criteria and was aspirated without cytologic evidence of malignancy. Attention was then turned to the parenchymal lesion. Utilizing radial EBUS, an eccentric acoustic signal was obtained in the anterior segment of the LUL. Diagnostic sampling via brush and forceps was performed. Subsequently, in accordance with the DECAMP protocol, research specimens were procured from the RUL, RML, and LUL. Hemostasis was assured.",
            3: "Procedures Performed:\n1. EBUS with TBNA (31652): Station 4R sampled.\n2. Bronchoscopy with biopsy, single lobe (31628): LUL nodule biopsied.\n3. Radial EBUS (31654): Peripheral lesion localization.\n4. Additional biopsies (31632 x2): Research samples in RUL and RML.\nNote: LMA used. 4R sampled due to size >5mm. LUL nodule visualized with rEBUS (eccentric). Multiple tools used.",
            4: "Procedure Note\nAttending: [Name]\nResident: [Name]\nIndication: LUL Nodule.\nSteps:\n1. Time out. GA induced. LMA placed.\n2. Airway inspection: Fused LUL anterior segment.\n3. EBUS: 4R sampled (benign).\n4. rEBUS: Localized LUL nodule (eccentric).\n5. Sampling: Brush/forceps to LUL.\n6. Research: DECAMP samples (RUL, RML, LUL).\n7. Hemostasis confirmed.\nPlan: Extubate, PACU.",
            5: "ebus done for lung nodule patient got propofol airway looked fine except weird lul segment. did ebus on 4r it was neg. then went to lul nodule found it with radar probe eccentric view took biopsies. rose said no cancer. did the decamp stuff brushing rul rml and biopsies in all three lobes. no bleeding really maybe 10cc. send to pacu.",
            6: "The patient arrived for EBUS bronchoscopy regarding a pulmonary nodule. General anesthesia was used. We inserted the Q190 and saw a fused anterior segment in the LUL but otherwise normal anatomy. We switched to the EBUS scope. Station 4R was 5mm and was sampled; cytology was negative. We switched to the thin scope P190. We went to the LUL nodule, found it with radial EBUS (eccentric), and biopsied it. ROSE was negative. We then did the DECAMP research biopsies in the RUL, RML, and LUL. No bleeding. Patient stable.",
            7: "[Indication]\nPulmonary nodule diagnosis/staging.\n[Anesthesia]\nGeneral (Propofol, LMA).\n[Description]\n1. Airway: Normal anatomy except fused LUL anterior/lingula.\n2. EBUS: Station 4R sampled (benign).\n3. Peripheral: LUL nodule loc. w/ rEBUS (eccentric). Biopsied (neg).\n4. Research: RUL/RML/LUL sampled per DECAMP.\n[Plan]\nDischarge home.",
            8: "The patient underwent an EBUS bronchoscopy under general anesthesia for a pulmonary nodule. Initial inspection showed a fused anterior segment of the left upper lobe. We proceeded with EBUS-TBNA of station 4R, which was negative on onsite evaluation. We then navigated to the LUL nodule using radial EBUS, obtaining an eccentric view. Biopsies were taken with forceps and brush; preliminary results were negative. Research samples were then collected from the RUL, RML, and LUL per the DECAMP protocol. The procedure was well tolerated.",
            9: "Procedure: EBUS bronchoscopy.\nReason: Lung mass requiring staging.\nAction: Scope deployed. Airway surveyed. Station 4R aspirated (neg). LUL lesion localized with radial probe (eccentric). Tissue harvested via forceps/brush. Research specimens collected from RUL, RML, LUL. No hemorrhage observed."
        },
        1: { # Note 1: EBUS + RML Nodule (Bleeding/TXA)
            1: "Indication: RML nodule.\nProcedure: Bronchoscopy, TBNA, EBUS, Forceps Bx.\nFindings: Vascular tumor RML lateral segment.\nIntervention: TBNA of nodule (6 passes). Bleeding controlled w/ TXA. EBUS of 4L, 7, 4R, 11R (all neg). Forceps bx of RML tumor (5 samples).\nComplications: Moderate bleeding, required tamponade.\nPlan: PACU.",
            2: "PROCEDURE: Diagnostic and Staging Bronchoscopy.\nFINDINGS: A glistening, hypervascular endobronchial lesion was identified in the lateral segment of the RML. Due to its friable nature, needle aspiration was performed first, followed by hemostatic control with tranexamic acid. Subsequent EBUS evaluation of stations 4L, 4R, 7, and 11R yielded benign lymphocytes. Following staging, therapeutic bronchoscopy was utilized to obtain forceps biopsies of the RML mass. Moderate hemorrhage ensued, necessitating mechanical tamponade for control.",
            3: "Coding Data:\n- 31653: EBUS sampling >3 nodes (4L, 7, 4R, 11R).\n- 31629: TBNA of endobronchial lesion (RML).\n- 31625 (bundled): Forceps biopsy of RML.\nMedical Necessity: Pulmonary nodule. Hemostasis required (TXA/Tamponade) due to vascular tumor. EBL 10cc.",
            4: "Procedure Note\nPt: Unk\nStaff: Unk\nProcedure: EBUS/Bronch.\n1. Inspect: RML lateral seg vascular tumor.\n2. TBNA of tumor x6. Bleeding -> TXA 40mg.\n3. EBUS: 4L, 7, 4R, 11R sampled. ROSE neg.\n4. Forceps Bx: RML tumor x5. Moderate bleeding -> Tamponade.\n5. Hemostasis achieved.",
            5: "we did the bronch for the rml nodule. saw a shiny vascular tumor in the rml lateral seg. touched it and it bled so we did needle bx first then put txa on it. then did the ebus part hit 4l 4r 7 and 11r all neg. went back to the rml with the therapeutic scope and took forceps bx. bled pretty good had to wedge the scope to stop it. stopped eventually.",
            6: "Under MAC anesthesia we performed a bronchoscopy. A vascular tumor was seen in the RML lateral segment. We performed 6 needle biopsies. Bleeding occurred and was treated with 4ml of TXA. We then switched to EBUS and sampled nodes 4L, 7, 4R, and 11R; all were negative. We switched to a therapeutic scope and performed 5 forceps biopsies of the RML lesion. Moderate bleeding required tamponade. The procedure was concluded once hemostasis was secure.",
            7: "[Indication]\nRML Pulmonary Nodule.\n[Anesthesia]\nMAC (Propofol).\n[Description]\nRML lateral segment: Vascular tumor. TBNA x6. Hemostasis w/ TXA. EBUS: 4L, 7, 4R, 11R (neg). Forceps Bx RML x5. Hemostasis w/ tamponade.\n[Plan]\nMonitor for hemoptysis. Discharge criteria met.",
            8: "The patient underwent bronchoscopy for a right middle lobe nodule. Upon inspection, a vascular, friable tumor was seen obstructing the RML lateral segment. We performed endobronchial needle aspiration initially to minimize trauma, using tranexamic acid to control subsequent oozing. We then proceeded to stage the mediastinum using EBUS, sampling stations 4L, 4R, 7, and 11R, all of which were benign. Returning to the RML with a therapeutic scope, we obtained forceps biopsies. This resulted in moderate bleeding managed successfully with mechanical tamponade.",
            9: "Procedure: EBUS airway exam.\nTarget: RML mass.\nTechnique: Visualized shiny vascular growth in RML. Aspirated with needle. Hemorrhage managed with TXA. Sonographic staging of nodes 4L, 7, 4R, 11R performed (benign). Tissue harvested via forceps from RML. Moderate bleeding necessitated tamponade."
        },
        2: { # Note 2: EBUS + ILD (TBBx RML/RLL + BAL)
            1: "Dx: Mediastinal adenopathy, ILD.\nProc: EBUS, TBBx, BAL.\nEBUS: 4R, 7, 4L sampled (benign lymphocytes).\nTBBx: Fluoroscopic guidance. RML and RLL biopsies.\nBAL: RML/RLL. 120cc in, 40cc out.\nComp: None.\nPlan: Await path.",
            2: "OPERATIVE REPORT: The patient presented for evaluation of mediastinal lymphadenopathy and interstitial lung disease. EBUS-TBNA was performed on enlarged lymph nodes at stations 4R, 7, and 4L; rapid on-site evaluation demonstrated benign lymphoid tissue. Following the staging component, the bronchoscope was re-inserted. Under fluoroscopic guidance, transbronchial forceps biopsies were obtained from the right middle and right lower lobes to evaluate the interstitial process. A bronchoalveolar lavage was also completed. The patient tolerated the procedure well.",
            3: "CPT Justification:\n- 31653: EBUS sampling 3 stations (4R, 7, 4L).\n- 31628: Transbronchial biopsy initial lobe (RML).\n- 31632: Transbronchial biopsy add'l lobe (RLL).\n- 31624: BAL.\nGuidance: Fluoroscopy used for TBBx. Ultrasound for EBUS.",
            4: "Resident Note\nIndication: LA/ILD.\n1. Airway exam: Normal.\n2. EBUS: 4R, 7, 4L. ROSE: Benign.\n3. TBBx: RML, RLL with fluoro.\n4. BAL: performed.\n5. No bleeding.\nDisposition: Recovery.",
            5: "patient here for nodes and ild. gave propofol. airway looked normal no secretions. did ebus on 4r 7 and 4l all showed lymphocytes benign. then went back in and did biopsies in the right lung rml and rll using fluoro. also washed the lung bal 120cc. no bleeding seen. done.",
            6: "The procedure was EBUS bronchoscopy with TBBx and BAL. Indications were adenopathy and ILD. Using the Q190, the airway was normal. EBUS was used to sample 4R, 7, and 4L; all were benign. We then performed fluoroscopically guided transbronchial biopsies in the RML and RLL. A BAL was performed with 40cc return. No complications occurred.",
            7: "[Indication]\nMediastinal adenopathy, ILD.\n[Anesthesia]\nGeneral (LMA).\n[Description]\nEBUS: 4R, 7, 4L sampled (benign). TBBx: RML, RLL (fluoro guided). BAL: Performed.\n[Plan]\nPathology pending.",
            8: "We performed an EBUS bronchoscopy to investigate mediastinal adenopathy and interstitial lung disease. The airway exam was unremarkable. We utilized the convex probe EBUS to sample lymph nodes at stations 4R, 7, and 4L. On-site pathology showed benign lymphoid tissue. We then switched to a video bronchoscope to perform transbronchial biopsies in the right middle and lower lobes under fluoroscopic guidance. A bronchoalveolar lavage was also performed. There were no immediate complications.",
            9: "Procedure: EBUS staging and lung sampling.\nReason: Enlarged nodes and interstitial markings.\nAction: Airway inspected. Nodes 4R, 7, 4L aspirated (benign). Parenchymal tissue harvested from RML and RLL via forceps. Lavage conducted. Hemostasis confirmed."
        },
        3: { # Note 3: ENB RUL Nodule
            1: "Indication: RUL nodule.\nTechnique: SuperDimension ENB + Radial EBUS.\nProcedure: Navigated to RUL anterior seg. rEBUS concentric view. Needle bx (ROSE: lymphocytes). Forceps bx.\nComp: None. No pneumo on fluoro.\nEBL: <5cc.",
            2: "PROCEDURE: Electromagnetic Navigational Bronchoscopy (ENB).\nINDICATION: Right upper lobe pulmonary nodule.\nNARRATIVE: Following induction, a diagnostic inspection revealed normal anatomy. The SuperDimension navigation catheter was advanced into the anterior segment of the RUL, achieving position within 1cm of the target. Radial EBUS confirmation yielded a concentric signal. Transbronchial needle aspiration and forceps biopsies were performed under fluoroscopic guidance. ROSE indicated inflammatory cells. Post-procedural fluoroscopy ruled out pneumothorax.",
            3: "Billing Codes:\n- 31627: Navigation (SuperDimension).\n- 31629: TBNA of RUL nodule.\n- 31628-59: Transbronchial biopsy RUL nodule.\n- 31654: Radial EBUS guidance.\nDetails: Navigated to lesion. Concentric rEBUS view. Multiple modalities used.",
            4: "Procedure Steps:\n1. GA/LMA.\n2. Normal airway exam.\n3. SuperDimension nav to RUL anterior seg.\n4. rEBUS: Concentric view.\n5. TBNA x passes (lymphocytes).\n6. Forceps biopsy.\n7. Fluoro check: No pneumothorax.",
            5: "enb for rul nodule. used superdimension system. got the catheter into the rul anterior seg and saw the lesion on radial ebus concentric view. poked it with the needle rose just showed inflammation. took some bites with the forceps too. checking fluoro at the end showed no pneumo.",
            6: "Electromagnetic navigational bronchoscopy was performed for a right upper lobe nodule. General anesthesia was used. The airway was normal. Using the SuperDimension system, we navigated to the RUL anterior segment. Radial EBUS showed a concentric view. Needle biopsies showed lymphocytes. Forceps biopsies were also taken. No pneumothorax was seen on fluoroscopy.",
            7: "[Indication]\nRUL Nodule.\n[Anesthesia]\nGeneral.\n[Description]\nENB to RUL anterior seg. rEBUS: Concentric. TBNA: Lymphocytes. Forceps Bx: Performed. No pneumothorax.\n[Plan]\nAwait final path.",
            8: "The patient presented for evaluation of a right upper lobe nodule. We employed electromagnetic navigation to guide a catheter into the anterior segment of the RUL. Localization was confirmed with radial EBUS, displaying a concentric view. We performed needle aspirations, which showed lymphocytes on rapid evaluation, followed by forceps biopsies. Final fluoroscopic inspection confirmed the absence of a pneumothorax.",
            9: "Procedure: Navigational airway inspection.\nTarget: RUL mass.\nAction: Navigated to target. Verified with ultrasound (concentric). Aspirated with needle (inflammatory). Harvested tissue with forceps. Pneumothorax ruled out."
        },
        4: { # Note 4: Peripheral rEBUS LUL (Malignant)
            1: "Indication: Pulmonary nodule.\nProcedure: Bronchoscopy, rEBUS, TBNA, TBBx.\nFindings: Fused LUL/Lingula. Lesion in LUL.\nrEBUS: Concentric view.\nSampling: TBNA (ROSE: Malignant). Forceps bx x6.\nComp: None. No pneumo.",
            2: "OPERATIVE NOTE: The patient underwent peripheral bronchoscopy for a suspicious pulmonary nodule. Airway inspection revealed a fused left upper lobe anterior segment and lingula. The therapeutic bronchoscope was utilized to advance a sheath and radial EBUS probe to the target, revealing a concentric orientation. Transbronchial needle aspiration was diagnostic for malignancy on rapid on-site evaluation. Six additional forceps biopsies were obtained for characterization. Hemostasis was achieved.",
            3: "Code Selection:\n- 31628: Transbronchial biopsy single lobe (LUL).\n- 31654: Radial EBUS guidance.\n- 31629 (bundled): TBNA performed.\nNotes: Guide sheath used. Concentric view. ROSE positive for malignancy. Fluoroscopy utilized.",
            4: "Resident Procedure Note\nIndication: Nodule.\n1. Inspect: Fused LUL/Lingula.\n2. rEBUS: Concentric view in LUL.\n3. TBNA: Positive for malignancy.\n4. TBBx: 6 samples taken.\n5. No bleeding/pneumo.\nPlan: Oncology referral pending final path.",
            5: "peripheral bronch for lung nodule. patient under propofol. anatomy weird fused lul lingula. used the sheath and radial probe saw the lesion concentric. needle biopsy showed cancer on rose. took 6 more biopsies with forceps. no bleeding or pneumothorax. all done.",
            6: "Peripheral bronchoscopy with radial EBUS was performed for a pulmonary nodule. The LUL anterior segment was fused with the lingula. A sheath was advanced to the lesion, and radial EBUS showed a concentric view. TBNA confirmed malignancy. We then performed 6 forceps biopsies. There were no complications or pneumothorax.",
            7: "[Indication]\nPulmonary nodule.\n[Anesthesia]\nGeneral.\n[Description]\nAnatomy: Fused LUL/Lingula. rEBUS: Concentric. TBNA: Malignant. TBBx: x6 samples.\n[Plan]\nAwait final pathology.",
            8: "We performed a peripheral bronchoscopy to diagnose a pulmonary nodule. The patient's anatomy showed a fused left upper lobe and lingula. We navigated a sheath to the lesion and confirmed its location with radial EBUS, obtaining a concentric view. Needle biopsies were immediately diagnostic for malignancy. We proceeded to take six forceps biopsies to ensure adequate tissue for profiling. The procedure concluded without complications.",
            9: "Procedure: Distal airway exam with ultrasound.\nTarget: Lung mass.\nAction: Sheath advanced. Ultrasound confirmed concentric lesion. Aspiration confirmed carcinoma. Tissue harvested x6. No air leak detected."
        }
    }
    return variations

def get_base_data_mocks():
    # Base data corresponding to the 5 notes in bronch_notes_part_021.json
    # Assigning random original data since it's "UNKNOWN" in source
    return [
        {"idx": 0, "orig_name": "John Doe", "orig_age": 65, "names": ["Arthur Dent", "Ford Prefect", "Zaphod Beeblebrox", "Tricia McMillan", "Marvin Android", "Slartibartfast", "Roosta Vogon", "Prostetnic Jeltz", "Deep Thought"]},
        {"idx": 1, "orig_name": "Jane Smith", "orig_age": 72, "names": ["Ellen Ripley", "Dwayne Hicks", "Carter Burke", "Bishop Android", "Rebecca Jorden", "William Hudson", "Scott Gorman", "Jenette Vasquez", "Al Apone"]},
        {"idx": 2, "orig_name": "Bob Jones", "orig_age": 58, "names": ["Rick Deckard", "Roy Batty", "Rachael Tyrell", "Pris Stratton", "Zhora Salome", "Leon Kowalski", "Harry Bryant", "J.F. Sebastian", "Eldon Tyrell"]},
        {"idx": 3, "orig_name": "Alice White", "orig_age": 69, "names": ["Sarah Connor", "Kyle Reese", "T-800 Model", "John Connor", "Miles Dyson", "Peter Silberman", "Janelle Voight", "Todd Voight", "Enrique Salceda"]},
        {"idx": 4, "orig_name": "Charlie Brown", "orig_age": 60, "names": ["Marty McFly", "Emmett Brown", "Lorraine Baines", "George McFly", "Biff Tannen", "Jennifer Parker", "Dave McFly", "Linda McFly", "Goldie Wilson"]}
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
            # Verify we have text for this index/style
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}")
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update MRN to be unique
                current_mrn = note_entry["registry_entry"].get("patient_mrn", "UNKNOWN")
                if current_mrn == "UNKNOWN":
                    current_mrn = f"IP_SYN_{idx+1}"
                note_entry["registry_entry"]["patient_mrn"] = f"{current_mrn}_var_{style_num}"
                
                # Update Date
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update Demographics if present (some notes have it nested, some don't based on input file)
                if "patient_demographics" in note_entry["registry_entry"]:
                    if note_entry["registry_entry"]["patient_demographics"] is None:
                         note_entry["registry_entry"]["patient_demographics"] = {}
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                # Some notes might have age directly in registry_entry (not standard in this specific input but good practice to check)
                if "patient_age" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["patient_age"] = new_age

            # Add metadata about the synthetic generation
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "style_description": [
                    "Terse Surgeon", "Academic Attending", "Billing Coder", 
                    "Trainee/Resident", "Sloppy Dictation", "Header-less", 
                    "Templated", "Narrative Flow", "Synonym Swapper"
                ][style_num-1],
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_bronch_notes_part_021.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()