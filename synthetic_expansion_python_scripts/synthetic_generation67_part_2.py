import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_067.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations for the Ion Robotic Bronchoscopy dataset.
    Structure: Note_Index (int) -> Style_Index (1-9) -> Text (str)
    
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
        0: { # Steven Adams (LUL 24mm: Ion, TBNA, Cryo, Fiducial, Brush, BAL)
            1: "Procedure: Robotic bronchoscopy (Ion). Target: 24mm LUL nodule.\nActions:\n- Navigated to LUL apicoposterior segment.\n- Confirmed w/ rEBUS (eccentric) & CBCT.\n- TBNA (21G) x7 passes.\n- Cryobiopsy (1.1mm) x3 samples (6s freeze).\n- Fiducial placed (CIVCO).\n- Brush x2, BAL (60cc).\nFindings: No bleeding. Stable.",
            2: "OPERATIVE NARRATIVE: The patient presented for diagnostic evaluation of a 24 mm part-solid nodule within the apicoposterior segment of the left upper lobe. Following induction of general anesthesia, the Ion robotic endoluminal system was deployed. Registration was achieved with a minimal error of 3.1 mm. \n\nUpon navigating to the target, radial endobronchial ultrasound (rEBUS) demonstrated an eccentric orientation, and cone-beam CT (CBCT) fusion confirmed accurate tool-in-lesion positioning. We proceeded with a multi-modal sampling strategy: transbronchial needle aspiration (TBNA) utilizing a 21-gauge needle yielded seven specimens; transbronchial cryobiopsy using a 1.1 mm probe with a 6-second freeze time provided three tissue cores. To facilitate future stereotactic radiotherapy, a gold fiducial marker was implanted. The procedure concluded with bronchial brushing and a bronchoalveolar lavage (BAL) of the target segment. The patient remained hemodynamically stable throughout.",
            3: "CPT CODING SUBSTANTIATION:\n1. 31626 (Primary): Placement of fiducial marker (0.8mm x 3mm gold) under fluoroscopic guidance.\n2. 31629: Transbronchial needle aspiration (TBNA) of LUL nodule using 21G needle (7 passes).\n3. 31628: Transbronchial cryobiopsy of single LUL lesion (1.1mm probe, 3 samples). NCCI edit bypass required if distinct work shown.\n4. 31627: Computer-assisted navigation (Ion platform) used for target localization (Add-on).\n5. 31654: Radial EBUS performed to verify peripheral lesion location (Add-on).\n6. 31623: Brushing of target lesion.\n7. 31624: BAL of LUL segment.\nMedical Necessity: Tissue diagnosis of 24mm part-solid opacity.",
            4: "Procedure: Robotic Bronchoscopy (LUL Nodule)\nAttending: Dr. Williams\nSteps:\n1. Time out. GA induced. ETT placed.\n2. Ion catheter advanced to LUL (LB1+2).\n3. Target (24mm) identified via rEBUS (eccentric).\n4. Spin CT (CBCT) confirmed tool in lesion.\n5. Biopsies: TBNA (21G x7), Cryo (1.1mm x3).\n6. Marker: 1 fiducial placed.\n7. Wash/Brush: Brush x2, BAL 60cc instilled.\n8. Complications: None. ROSE benign.",
            5: "patient steven adams here for the lung nodule biopsy LUL 24mm used the ion robot registration was 3.1mm went to the apicoposterior segment looked good on rebus eccentric view. did the needle first 21 gauge got 7 samples then switched to the cryo probe 1.1mm did 3 samples frozen for 6 seconds. put a fiducial in there for radiation later. brush and bal also done no bleeding patient tolerated well recovery room.",
            6: "After the successful induction of anesthesia a timeout was performed. Initial airway inspection showed normal anatomy. Robotic navigation bronchoscopy was performed with Ion platform (registration error 3.1mm). The catheter engaged the Apicoposterior Segment of LUL. Radial EBUS confirmed lesion location (eccentric). Needle was advanced into the 24mm lesion and Cone Beam CT confirmed location. Transbronchial needle aspiration was performed with 21G Needle (7 samples). Transbronchial cryobiopsy was performed with 1.1mm cryoprobe (3 samples). Fiducial marker was placed. Transbronchial brushing and Bronchoalveolar lavage were completed. The patient tolerated the procedure well.",
            7: "[Indication]\nPart-solid 24mm nodule in LUL, need tissue diagnosis.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon robot navigated to LUL apicoposterior segment. rEBUS: Eccentric. CBCT: Tool-in-lesion confirmed. Sampling performed: TBNA (21G x7), Cryobiopsy (1.1mm x3). Fiducial marker placed. Brushing and BAL performed.\n[Plan]\nDischarge. Follow up pathology.",
            8: "Mr. Adams underwent a robotic bronchoscopy today to investigate a 24mm nodule in his left upper lobe. We navigated the Ion catheter to the apicoposterior segment and used radial EBUS and cone-beam CT to confirm we were right on target. Once positioned, we took extensive samples using a 21-gauge needle for aspiration and a cryoprobe for tissue cores. We also placed a gold fiducial marker to help with future treatment targeting. Finally, we performed brushing and a lung wash (BAL) of the area. There were no complications, and the preliminary onsite check showed benign cells.",
            9: "Operation: Robotic assisted bronchoscopy.\nTarget: 24mm LUL mass.\nAction: The Ion catheter was steered to the LUL. rEBUS verified the position. We aspirated the lesion with a 21G needle (7 passes) and harvested tissue using a 1.1mm cryoprobe (3 samples). A fiducial was deposited. The area was scrubbed (brush) and lavaged (BAL).\nResult: Samples acquired. No hemorrhage."
        },
        1: { # Dorothy Hill (LUL 31mm: Ion, TBNA, Brush)
            1: "Target: 31mm LUL nodule.\nTechnique: Ion Robotic Nav + rEBUS + CBCT.\nRegistration error: 3.4mm.\nSamples:\n- TBNA (21G/23G) x4 passes.\n- Brush x2.\nResults: ROSE benign. No complications.\nPlan: D/C.",
            2: "PROCEDURE NOTE: The patient, Ms. Hill, presented with a dominant 31 mm pulmonary nodule in the left upper lobe. Under general anesthesia, the airway was secured. We utilized the Ion robotic platform for navigation, achieving a registration error of 3.4 mm. The catheter was advanced to the apicoposterior segment (LB1+2). Radial EBUS demonstrated a concentric view, and Cone Beam CT confirmed the needle path. Biopsies were obtained via transbronchial needle aspiration using both 21G and 23G needles, followed by protected specimen brushing. On-site cytopathology showed benign respiratory epithelium.",
            3: "Codes:\n- 31629 (TBNA, LUL)\n- 31623 (Brushing, LUL) - Bundled per NCCI\n- 31627 (Navigational Bronchoscopy)\n- 31654 (rEBUS)\nTools: Ion Robot, 21G & 23G needles, Cytology brush.\nJustification: 31mm lesion sampled using multimodal guidance (Nav + US + Fluoro/CBCT).",
            4: "Resident Procedure Note\nPt: Hill, Dorothy\nProc: Ion Bronch LUL\n1. ETT placed.\n2. Navigated to LB1+2.\n3. rEBUS: Concentric.\n4. CBCT: Good alignment.\n5. TBNA x4 (21G/23G).\n6. Brush x2.\n7. ROSE: Benign.\nNo issues.",
            5: "dorothy hill here for lung biopsy she has a 31mm nodule in the LUL we used the ion robot today registration 3.4mm. navigated to the spot used radial ebus got a concentric view which is good. did tbna with 21 and 23 gauge needles 4 samples total. also did a brush 2 samples. rose said benign stuff. woke her up no bleeding shes fine.",
            6: "Robotic navigation bronchoscopy was performed with Ion platform for a 31mm nodule in LUL. Full registration was used (error 3.4mm). Ion robotic catheter engaged the Apicoposterior Segment. Radial EBUS confirmed lesion location with a concentric view. Needle was advanced into the lesion and confirmed with Cone Beam CT. Transbronchial needle aspiration was performed with 21G and 23G Needles (4 samples). Transbronchial brushing was performed (2 samples). ROSE showed benign respiratory epithelium.",
            7: "[Indication]\nDominant 31mm LUL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to LUL. rEBUS concentric. CBCT confirmation. TBNA x4. Brush x2.\n[Plan]\nOutpatient discharge.",
            8: "We performed a biopsy on Ms. Hill's 31mm left upper lobe nodule using the Ion robotic system. After navigating to the lesion, we confirmed its position with radial EBUS, which showed a concentric return, and a spin CT scan. We took four needle samples using different gauge needles and two brush samples. The preliminary results didn't show cancer, just benign cells. She tolerated the procedure well.",
            9: "Procedure: Robotic assisted airway inspection and sampling.\nTarget: 31mm LUL opacity.\nExecution: The robotic catheter was guided to the target. rEBUS corroborated the location. We sampled the lesion via needle aspiration (4x) and brushing (2x). CBCT imaging validated the tool position.\nOutcome: Benign cells observed."
        },
        2: { # Linda Young (Lingula 11mm: Ion, TBNA, Cryo)
            1: "Indication: 11mm Lingula nodule.\nTools: Ion Robot, rEBUS, CBCT.\nAction: Navigated to LB4. rEBUS eccentric.\nSampling: TBNA (21G) x4, Cryobiopsy (1.1mm) x4.\nROSE: Negative for malignancy.\nComplications: None.",
            2: "OPERATIVE REPORT: Ms. Young underwent elective robotic bronchoscopy for a semi-solid 11 mm nodule in the superior Lingula. The Ion catheter was navigated to the target segment (LB4) with a registration accuracy of 2.1 mm. Confirmation of the lesion was achieved via eccentric radial EBUS signal and intraoperative Cone Beam CT. We obtained diagnostic tissue using a 21G transbronchial needle (4 passes) and a 1.1 mm transbronchial cryoprobe (4 samples, 5-second freeze). Immediate cytological evaluation revealed no evidence of malignant neoplasm.",
            3: "Billing Data:\n- 31629 (TBNA)\n- 31628 (Cryobiopsy) - Note: Same lesion, typically bundled.\n- 31627 (Nav)\n- 31654 (rEBUS)\nDevice: Ion Robotic System.\nTarget: Lingula (11mm).\nDetails: 21G needle used for cellular yield; Cryoprobe used for histology.",
            4: "Procedure: Ion Bronchoscopy\nTarget: Lingula 11mm\nSteps:\n- Intubation.\n- Nav to LB4.\n- rEBUS: Eccentric.\n- CBCT: Tool in lesion.\n- TBNA x4 (21G).\n- Cryo x4 (1.1mm).\n- Extubation.\nROSE: No malignancy.",
            5: "linda young 11mm nodule lingula. used the ion system 2.1mm error. went to lb4 segment. radial ebus showed eccentric view. spin ct looked good. did 4 needle passes 21g and 4 cryo biopsies 1.1mm probe. rose says no cancer seen. minimal bleeding stopped on its own. discharge home.",
            6: "Robotic navigation bronchoscopy was performed with Ion platform for an 11mm nodule in the Superior Lingula. Full registration was used. Ion robotic catheter engaged LB4. Radial EBUS confirmed lesion location (Eccentric). Cone Beam CT performed for 3-D confirmation. Transbronchial needle aspiration was performed with 21G Needle (4 samples). Transbronchial cryobiopsy was performed with 1.1mm cryoprobe (4 samples). ROSE result: No evidence of malignant neoplasm.",
            7: "[Indication]\n11mm Lingula nodule.\n[Anesthesia]\nGA.\n[Description]\nIon nav to Superior Lingula. rEBUS eccentric. TBNA (21G) x4. Cryo (1.1mm) x4. CBCT confirmation.\n[Plan]\nDischarge. F/U 5-7 days.",
            8: "Ms. Young's procedure focused on an 11mm nodule in the Lingula. We used the robotic bronchoscope to reach the area. The radial EBUS showed the nodule was off to the side (eccentric), but the spin CT confirmed our needle was in the right spot. We took four samples with a needle and four more with the freezing probe (cryobiopsy). The preliminary check didn't show any cancer cells.",
            9: "Intervention: Robotic guided biopsy.\nSite: 11mm Lingula lesion.\nMethod: The robot was piloted to the target. rEBUS confirmed the site. We extracted cells via aspiration (TBNA) and harvested tissue via cryo-adhesion (Cryobiopsy). CBCT ensured accuracy.\nStatus: No malignancy detected onsite."
        },
        3: { # Jonathan Jones (RUL 33mm: Ion, TBNA, Cryo, Fiducial, Brush)
            1: "RUL mass (33mm). Ion nav used.\nReg error: 3.8mm.\nConf: rEBUS (concentric), CBCT.\nBiopsy: TBNA (23G) x6, Cryo (1.7mm) x5.\nMarker: 1 Fiducial placed.\nBrush: x2.\nROSE: Lymphocytes/benign.",
            2: "PROCEDURE: Mr. Jones presented with a 33 mm ground glass opacity in the RUL apical segment. Robotic bronchoscopy (Ion) was performed. Despite a registration error of 3.8 mm, navigation to the target was successful. rEBUS indicated a concentric view. Utilizing fluoroscopic and CBCT guidance, we performed extensive sampling: 6 passes with a 23G needle and 5 cryobiopsies using a 1.7 mm probe. A gold fiducial marker was deployed for potential SBRT. Brushing was also performed. ROSE showed lymphocytes and benign cells.",
            3: "CPT Selection:\n- 31626 (Fiducial - Primary)\n- 31629 (TBNA)\n- 31627 (Nav)\n- 31654 (rEBUS)\n- 31628 (Cryo - Bundled?)\n- 31623 (Brush - Bundled)\nTechnique: Ion robot, rEBUS, Fluoroscopy, CBCT.\nTarget: RUL 33mm GGO.",
            4: "Resident Note\nPt: Jones, Jonathan\nSite: RUL (RB1) 33mm\n1. Ion nav to target.\n2. rEBUS: Concentric.\n3. CBCT spin: Confirmed.\n4. TBNA 23G x 6.\n5. Cryo 1.7mm x 5.\n6. Fiducial placed.\n7. Brush x 2.\nROSE: Adequate/Benign.",
            5: "jonathan jones RUL 33mm nodule. used ion robot 3.8mm error went to apical segment rb1. rebus concentric. did a lot of samples 6 needle passes 23g and 5 cryo biopsies 1.7mm. also put in a fiducial marker and brushed it. rose benign. patient did fine.",
            6: "Robotic navigation bronchoscopy was performed with Ion platform for a 33mm nodule in RUL. Full registration was used. Ion robotic catheter engaged the Apical Segment. Radial EBUS confirmed lesion location (Concentric). Cone Beam CT performed. Transbronchial needle aspiration performed with 23G Needle (6 samples). Transbronchial cryobiopsy performed with 1.7mm cryoprobe (5 samples). Fiducial marker placed. Transbronchial brushing performed. ROSE: Lymphocytes and benign cells.",
            7: "[Indication]\nRUL GGO 33mm.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to RB1. rEBUS concentric. TBNA x6. Cryo x5. Fiducial placed. Brush x2.\n[Plan]\nObservation.",
            8: "We targeted a large 33mm opacity in Mr. Jones's right upper lobe. Using the Ion robot, we navigated to the apical segment. The ultrasound view was excellent (concentric). We performed a thorough biopsy using both a 23-gauge needle and a 1.7mm cryoprobe. We also placed a gold marker in the lesion to help with future radiation therapy if needed. Brushing was also done. The initial results suggest benign tissue.",
            9: "Procedure: Robotic assisted sampling.\nLesion: 33mm RUL GGO.\nSteps: Navigated to RB1. Validated with rEBUS and CBCT. Aspirated (TBNA) and harvested (Cryo) tissue. Implanted a fiducial. Brushed the area.\nAnalysis: Benign cells."
        },
        4: { # Daniel Mitchell (RLL 33mm: Ion, TBNA, Cryo, Brush)
            1: "Target: RLL 33mm nodule.\nTools: Ion, 23G Needle, 1.7mm Cryo.\nNav: LB8. rEBUS adjacent.\nAction: TBNA x7, Cryo x5, Brush x2.\nROSE: Atypical/Suspicious.\nPlan: Wait for finals.",
            2: "OPERATIVE SUMMARY: Mr. Mitchell underwent robotic bronchoscopy for a screening-detected 33 mm RLL nodule. The Ion system was registered (error 2.4 mm) and navigated to the anterior-basal segment. Radial EBUS showed an adjacent lesion, which was confirmed via CBCT. We obtained high-volume samples: 7 TBNA passes (23G) and 5 cryobiopsies (1.7 mm). Brushing was also performed. Rapid on-site evaluation was concerning for malignancy with atypical cells present.",
            3: "Coding:\n- 31629 (TBNA)\n- 31627 (Nav)\n- 31654 (rEBUS)\n- 31628 (Cryo - Bundled)\n- 31623 (Brush - Bundled)\nDetails: RLL RB8 target. 33mm.\nPathology: Atypical cells found.",
            4: "Procedure: Ion RLL Biopsy\nPt: Mitchell, Daniel\n1. Nav to RB8.\n2. rEBUS: Adjacent.\n3. CBCT: Confirmed.\n4. TBNA 23G x 7.\n5. Cryo 1.7mm x 5.\n6. Brush x 2.\nROSE: Suspicious for Ca.",
            5: "daniel mitchell lung screening nodule RLL 33mm. ion robot used 2.4mm error. went to rb8 anterior basal. rebus adjacent. needle biopsy 23g 7 times then cryo 1.7mm 5 times. brushed it too. rose showed atypical cells probably cancer. no complications.",
            6: "Robotic navigation bronchoscopy with Ion platform. Target: 33mm nodule in RLL (Anterior-Basal Segment). Registration error: 2.4mm. Radial EBUS: Adjacent. Cone Beam CT performed. Transbronchial needle aspiration (23G) x 7 samples. Transbronchial cryobiopsy (1.7mm) x 5 samples. Transbronchial brushing x 2 samples. ROSE Result: Atypical cells present, suspicious for malignancy.",
            7: "[Indication]\nScreening nodule RLL 33mm.\n[Anesthesia]\nGA.\n[Description]\nIon nav to RB8. rEBUS adjacent. TBNA x7. Cryo x5. Brush x2. Suspicious ROSE.\n[Plan]\nOncology referral if final positive.",
            8: "Mr. Mitchell had a 33mm nodule in his right lower lung that we biopsied today. We used the robot to get to the spot and confirmed it with ultrasound and CT scans. We took seven needle samples and five cryo samples, plus a brush sample. The pathologist in the room saw some atypical cells that look suspicious for cancer, so we'll need to wait for the final report to be sure.",
            9: "Procedure: Robotic assisted biopsy.\nSite: 33mm RLL mass.\nTechnique: Navigated to RB8. Verified with rEBUS (adjacent) and CBCT. Sampled via needle (TBNA) and freezing (Cryo). Brushed the airway.\nResult: Suspicious for malignancy."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the first 5 patients to match the variations.
    """
    return [
        {"idx": 0, "orig_name": "Adams, Steven", "orig_age": 65, "names": ["S. Adams", "Mr. Adams", "Steven J. Adams", "Steve Adams", "Adams, S.", "Steven Adams", "S. Adams", "Mr. Adams", "Steven Adams"]},
        {"idx": 1, "orig_name": "Hill, Dorothy", "orig_age": 61, "names": ["D. Hill", "Ms. Hill", "Dorothy M. Hill", "Dot Hill", "Hill, D.", "Dorothy Hill", "D. Hill", "Ms. Hill", "Dorothy Hill"]},
        {"idx": 2, "orig_name": "Young, Linda", "orig_age": 60, "names": ["L. Young", "Ms. Young", "Linda K. Young", "Linda Young", "Young, L.", "Linda Young", "L. Young", "Ms. Young", "Linda Young"]},
        {"idx": 3, "orig_name": "Jones, Jonathan", "orig_age": 53, "names": ["J. Jones", "Mr. Jones", "Jonathan P. Jones", "Jon Jones", "Jones, J.", "Jonathan Jones", "J. Jones", "Mr. Jones", "Jonathan Jones"]},
        {"idx": 4, "orig_name": "Mitchell, Daniel", "orig_age": 50, "names": ["D. Mitchell", "Mr. Mitchell", "Daniel R. Mitchell", "Dan Mitchell", "Mitchell, D.", "Daniel Mitchell", "D. Mitchell", "Mr. Mitchell", "Daniel Mitchell"]},
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
    
    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through notes (limiting to first 5 for this specific script as per prompt constraints on hardcoding)
    for idx, record in enumerate(base_data):
        if idx >= len(source_data):
            break
            
        original_note = source_data[idx]
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
            
            # Get name variation
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen for 0-4)
                continue

            # Update registry_entry fields if they exist to match synthetic changes
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
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
    output_filename = output_dir / "synthetic_ion_robotic_notes.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()