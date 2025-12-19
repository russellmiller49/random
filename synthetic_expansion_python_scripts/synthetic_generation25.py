import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_025.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Elizabeth Larkin (Lung Mass, EBUS/Nav/Biopsy)
            1: "Procedure: Bronchoscopy with EBUS/Nav.\n- Airway cleared of mucus (RMS/LMS/BI).\n- RML lateral segment mass located via Radial EBUS (concentric).\n- TBNA and TBBX performed (6 samples each). ROSE positive for malignancy.\n- BAL RML performed.\n- Linear EBUS staged mediastinum. Stations 11L, 7, 11Rs sampled (needle 22G). Elastography used.\n- No comps.",
            2: "OPERATIVE NARRATIVE: The patient was placed under general anesthesia for evaluation of a lung mass. Initial inspection revealed secretions which were aspirated therapeutically from the central airways. Attention was turned to the right middle lobe lateral segment, where radial endobronchial ultrasound confirmed a concentric, continuous lesion. Diagnostic sampling was achieved via transbronchial needle aspiration and forceps biopsy, alongside bronchoalveolar lavage. Rapid on-site evaluation confirmed malignancy. Subsequently, systematic mediastinal staging utilizing linear endobronchial ultrasound (EBUS) with elastography was performed; lymph node stations 11L, 7, and 11Rs were identified, measured, and sampled via fine-needle aspiration. The procedure concluded without complication.",
            3: "Code Selection Justification:\n31653: Primary service. Linear EBUS sampling of 3 distinct nodal stations (11L, 7, 11Rs).\n31645-59: Therapeutic aspiration of mucus from RMS, LMS, and BI, distinct from biopsy sites.\n31628-59: Transbronchial lung biopsy of separate RML lesion.\n31654: Radial EBUS guidance used for peripheral RML lesion localization.\nNote: Elastography (76982/3) performed but bundled. 31629/31624 bundled into 31628.",
            4: "Procedure Note\nPatient: [PATIENT_NAME]\nAttending: Dr. Johnson\nSteps:\n1. Time out. GA induced.\n2. Therapeutic suctioning of extensive mucus.\n3. Navigated to RML lateral segment.\n4. Radial EBUS confirmed concentric view.\n5. TBBX x6 and TBNA x6 obtained. BAL performed.\n6. Linear EBUS staging: Stations 11L, 7, 11Rs sampled with 22G needle.\n7. ROSE positive.\n8. Extubated stable.",
            5: "We did the bronchoscopy today on the patient for the lung mass  started with cleaning out a lot of mucus from the mainstems right and left  then went to the RML found the spot with radial ebus it was concentric  took biopsies with the needle and the forceps and did a wash  pathology guy in the room said it was cancer  then we switched to the ebus scope and checked the lymph nodes  sampled 11L and 7 and 11Rs  elastography looked soft mostly  patient woke up fine no issues thanks.",
            6: "The patient was brought to the bronchoscopy suite and placed under general anesthesia. Initial inspection required therapeutic aspiration of the Right Mainstem, Bronchus Intermedius, and Left Mainstem to clear mucus. A therapeutic scope was advanced to the RML lateral segment. Radial EBUS confirmed a concentric lesion. TBNA (19G/21G) and TBBX (forceps) were performed obtaining 6 samples each, followed by BAL. ROSE confirmed malignancy. Linear EBUS was then utilized for staging. Lymph node stations 11L, 7, and 11Rs were sampled using a 22G needle under elastographic guidance. The patient tolerated the procedure well.",
            7: "[Indication]\nLung mass, R91.8.\n[Anesthesia]\nGeneral.\n[Description]\nTherapeutic aspiration of central airways performed. RML lesion localized with Radial EBUS (concentric). TBBX, TBNA, and BAL performed at RML. Linear EBUS staging performed at stations 11L, 7, and 11Rs.\n[Plan]\nFollow up pathology. Complete steroids/antibiotics.",
            8: "Under general anesthesia, the procedure commenced with a therapeutic aspiration to clear significant mucus from the right and left mainstems. We then navigated to the right middle lobe lateral segment. Using radial EBUS, we verified the lesion's concentric location. We proceeded to collect samples via transbronchial needle aspiration and alligator forceps biopsy, followed by a lavage; on-site analysis confirmed malignancy. Finally, we performed linear EBUS staging, sampling nodes at stations 11L, 7, and 11Rs with elastography assistance. The patient remained stable throughout.",
            9: "Intervention: Bronchoscopic evaluation.\nActions: Clearances of the airways (suctioning) were executed. The RML mass was pinpointed using ultrasound. Tissue was harvested via needle aspiration and forceps extraction. Lavage was conducted. Mediastinal nodes (11L, 7, 11Rs) were interrogated and sampled using linear ultrasound guidance. Malignancy was verified."
        },
        1: { # Tammy Adams (RUL Mass, Nav/Ablation)
            1: "Procedure: Robotic Nav Bronch + Microwave Ablation.\n- Therapeutic aspiration (Trachea/RMS/BI).\n- RUL Anterior segment mass (4cm) targeted via Ion.\n- CBCT confirmed tool-in-lesion.\n- TBNA x1 (Cyto).\n- Radial EBUS: concentric.\n- Microwave ablation x3 burns (RB3, RB2, RB1) at 90C.\n- Post-proc CBCT: good margins. No pneumo.",
            2: "OPERATIVE REPORT: The patient underwent robotic-assisted navigational bronchoscopy for a 4cm RUL mass. Following therapeutic aspiration of secretions, the Ion platform was utilized to navigate to the anterior segment of the RUL. Localization was confirmed via Cone Beam CT (CBCT) and Radial EBUS. A diagnostic TBNA was performed. Subsequently, therapeutic microwave ablation was delivered to the lesion in three overlapping sessions (RB1, RB2, RB3) at 90 degrees Celsius to ensure adequate margins. Post-ablation imaging confirmed successful targeting without complications.",
            3: "Billing Summary:\n31641: Primary. Microwave ablation of RUL tumor (3 separate burns to cover volume).\n31645-59: Therapeutic aspiration of central airways (distinct from RUL target).\n+31627: Computer-assisted navigation (Ion system) used for target approach.\n+31654: Radial EBUS used for peripheral lesion confirmation.\nNote: 77012/76377 bundled into navigation/ablation codes. 31629 bundled into 31641.",
            4: "Resident Note\nPatient: [PATIENT_NAME]\nProcedure: Ion Bronch + Ablation\nSteps:\n1. GA / LMA.\n2. Suctioned mucus from airways.\n3. Registered Ion catheter. Navigated to RUL mass.\n4. Confirmed with Radial EBUS and Cone Beam CT.\n5. TBNA for diagnosis.\n6. Performed Microwave Ablation (20min, 10min, 10min).\n7. Final spin showed good ablation zone.\nPlan: Admit for obs.",
            5: "We used the robot today for the lung mass in the right upper lobe patient was asleep general anesthesia first we cleaned out some mucus from the trachea and right side then drove the ion catheter out to the lesion it was big like 4 cm confirmed it with the spin ct and the ultrasound needle biopsy first then we burned it with the microwave catheter did three burns total to get the whole thing checked it again with the spin and it looked good no bleeding or collapsed lung.",
            6: "After induction of general anesthesia and therapeutic aspiration of the central airways, robotic navigational bronchoscopy (Ion) was performed targeting a 4cm RUL mass. Localization was verified using Cone Beam CT and Radial EBUS. A single TBNA pass was collected for cytology. Microwave ablation was then performed in three overlapping zones (Anterior, Lateral Superior, Superior Medial) at 90C to treat the tumor. CBCT confirmed tool-in-lesion and treatment effect. The patient was extubated without complication.",
            7: "[Indication]\nR91.1 Solitary Lung Nodule (RUL Mass).\n[Anesthesia]\nGeneral, LMA.\n[Description]\nTherapeutic aspiration performed. RUL mass accessed via Ion Robot. CBCT and Radial EBUS confirmation. TBNA x1. Microwave ablation performed x3 cycles to destroy tumor.\n[Plan]\nAdmit for observation. Post-ablation CXR.",
            8: "The patient presented for evaluation and treatment of a right upper lobe mass. We induced general anesthesia and first cleared the airways of mucus via therapeutic aspiration. Using the Ion robotic platform, we navigated to the target in the RUL anterior segment. We utilized both Cone Beam CT and Radial EBUS to confirm our position within the 4cm lesion. After obtaining a diagnostic needle aspirate, we proceeded to destroy the tumor using microwave ablation, applying energy in three distinct locations to ensure coverage. The procedure was successful with no immediate complications.",
            9: "Operation: Robotic endoscopy with tumor destruction.\nTechnique: The airways were cleared. The RUL lesion was approached via robotic guidance. Position was verified with 3D imaging and ultrasound. Cellular material was acquired. The mass was then ablated using thermal energy (microwave) in multiple passes to ensure eradication. Tolerance was excellent."
        },
        2: { # Sarah Jenkins (Pleural Effusion, Chest Tube)
            1: "Procedure: Ultrasound-guided Chest Tube Placement (Right).\n- US Findings: Large anechoic effusion, R hemithorax. No loculations.\n- Site: Right 7-8 ICS, mid-scapular.\n- 14Fr pigtail inserted via Seldinger.\n- 1250ml serous fluid drained.\n- Secured with suture. CXR ordered.",
            2: "PROCEDURE NOTE: The patient presented with a symptomatic right pleural effusion. Bedside thoracic ultrasound was utilized to identify a large, anechoic effusion free of loculations. Under sterile conditions and local anesthesia, a 14 French pigtail catheter was inserted into the right 7-8th intercostal space using the Seldinger technique. The catheter was connected to a drainage system, yielding 1250ml of serous fluid. The device was secured, and a chest radiograph was ordered to confirm placement.",
            3: "CPT Coding:\n32557: Indwelling tunneled/non-tunneled pleural catheter insertion with imaging guidance. \n- Supports: Insertion of 14Fr pigtail.\n- Imaging: Real-time ultrasound guidance documented with image save.\n- Note: 76604 (US) and 71045 (CXR) are bundled.",
            4: "Resident Procedure Note\nPatient: [PATIENT_NAME]\nProcedure: Chest Tube (Right)\nIndication: Effusion.\nSteps:\n1. Ultrasound check: Large effusion, right side.\n2. Prepped/Draped. Lidocaine local.\n3. Needle entry 7-8 ICS. Wire passed.\n4. Dilated.\n5. 14Fr Pigtail advanced.\n6. 1250cc drained.\n7. Sutured and dressed.",
            5: "Bedside procedure note for Sarah Jenkins we did a chest tube on the right side today for that effusion ultrasound showed a lot of fluid large amount no septations used lidocaine for numbess put in a 14 french pigtail using the kit wire went in easy tube followed got back over a liter of serous fluid sutured it in place patient did fine chest xray pending.",
            6: "Ultrasound examination of the right hemithorax revealed a large anechoic pleural effusion. The patient was positioned, prepped, and draped. Local anesthesia was administered. A 14Fr pigtail catheter was inserted into the right pleural space via the 7-8th intercostal space using the Seldinger technique under real-time ultrasound guidance. 1250ml of serous fluid was evacuated. The catheter was sutured and attached to a Pleurovac. The patient tolerated the procedure well.",
            7: "[Indication]\nPleural Effusion, Right.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nUltrasound guided insertion of 14Fr pigtail catheter, Right 7-8 ICS. 1250ml serous fluid removed.\n[Plan]\nCXR. Fluid studies. Water seal.",
            8: "Ms. Jenkins required drainage of a right pleural effusion. We performed a bedside ultrasound which confirmed a large, free-flowing fluid collection. After sterilizing the site and injecting local anesthetic, we placed a 14 French chest tube using the Seldinger technique. We successfully drained 1250ml of fluid. The tube was secured with sutures, and the patient was left in stable condition pending a follow-up X-ray.",
            9: "Intervention: Pleural drainage catheterization.\nMethod: Sonographic localization identified the collection. A 14Fr catheter was introduced into the pleural cavity. A significant volume (1250ml) of exudate was evacuated. The drain was anchored. Post-procedural imaging was requested."
        },
        3: { # Vince Yound (Airway Obstruction, APC)
            1: "Procedure: Therapeutic Bronchoscopy (APC).\n- Stent RML patent.\n- Obstruction (90%) noted in Trachea, RMS, LMS.\n- APC applied (Pulse effect 4).\n- Result: 100% patency achieved.\n- Therapeutic aspiration of mucus from airways.\n- No comps.",
            2: "OPERATIVE SUMMARY: The patient presented for management of central airway obstruction. Inspection revealed a patent RML stent but significant (90%) malignant obstruction involving the distal trachea, right mainstem, and left mainstem bronchi. Argon Plasma Coagulation (APC) was utilized to ablate the endobronchial tumor tissue. Post-treatment inspection confirmed restoration of 100% airway patency. Additionally, therapeutic aspiration was performed to clear mucous secretions from the bronchial tree.",
            3: "Billing Codes:\n31641: Bronchoscopy with destruction of tumor (APC used on Trachea, RMS, LMS to relieve stenosis).\n31645-XS: Therapeutic aspiration performed in Bronchus Intermedius (distinct site from APC treatment area).\nDiagnosis: J98.09.",
            4: "Procedure Note\nPatient: [PATIENT_NAME]\nAttending: Dr. Johnson\nSteps:\n1. GA induced.\n2. Scope inserted.\n3. RML stent checked - OK.\n4. Found 90% blockage in Trachea/RMS/LMS.\n5. Used APC to burn tumor/open airway.\n6. Suctioned mucus from all airways.\n7. Result: Airway open.\nPlan: Repeat in 4-6 weeks.",
            5: "Vince was here for his airway check today 12/16 stent looks fine but he had regrowth in the trachea and both mainstems about 90 percent blocked so we used the APC to burn it back opened it up to 100 percent also had to suction out a lot of mucus from the lower airways patient did great extubated in room come back in a month or so.",
            6: "Under general anesthesia, a therapeutic bronchoscope was introduced. The RML stent was intact. Significant endobronchial obstruction (90%) was identified in the distal trachea, right mainstem, and left mainstem. This was treated with Argon Plasma Coagulation (APC) achieving 100% patency. Therapeutic aspiration was also performed to clear mucus from the Right Mainstem, Bronchus Intermedius, and Left Mainstem. The patient tolerated the procedure well.",
            7: "[Indication]\nAirway Obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nDiagnostic inspection: 90% obstruction Trachea/RMS/LMS. APC ablation performed. Patency restored to 100%. Therapeutic aspiration of mucus.\n[Plan]\nRepeat bronchoscopy 4-6 weeks.",
            8: "Mr. Yound underwent a therapeutic bronchoscopy to address his airway obstruction. We found the previously placed stent in the RML was functioning well, but there was significant tumor regrowth occluding the trachea and mainstem bronchi. We utilized Argon Plasma Coagulation to ablate this tissue, successfully restoring full airway patency. We also suctioned a significant amount of mucus to further optimize his airway. He recovered well and will return for follow-up.",
            9: "Operation: Endobronchial recanalization.\nDetails: The RML prosthesis was verified. Malignant strictures in the central airways were obliterated using thermal energy (APC). Patency was re-established. Secretions were evacuated via suction. The subject was awakened without incident."
        },
        4: { # Michael Jackson (Recurrent Effusion, Chest Tube)
            1: "Procedure: Left Chest Tube (US Guided).\n- US: Moderate complex effusion (hypoechoic/thin septations), Left.\n- Site: Left 5-6 ICS, mid-axillary.\n- 16Fr Pigtail placed (Seldinger).\n- 650ml serosanguinous fluid.\n- Suction -20cmH2O applied.",
            2: "PROCEDURE NOTE: This 72-year-old male presented with a recurrent left pleural effusion. Thoracic ultrasound demonstrated a moderate, complex effusion with thin loculations. Using aseptic technique and local anesthesia, a 16 French pigtail catheter was introduced into the left 5-6th intercostal space under real-time ultrasound guidance. The procedure yielded 650ml of serosanguinous fluid. The catheter was secured and placed to suction.",
            3: "Coding Justification:\n32557-LT: Insertion of indwelling pleural catheter (16Fr) with imaging guidance.\n- Imaging: Ultrasound used for localization and real-time guidance.\n- Medical Necessity: Recurrent complex effusion.\n- Bundling: US (76604) and CXR (71045) included.",
            4: "Resident Note\nPatient: [PATIENT_NAME]\nProcedure: Left Chest Tube\nSteps:\n1. US check: Loculated effusion left side.\n2. Prepped/Lidocaine.\n3. Needle -> Wire -> Dilator.\n4. 16Fr Pigtail inserted.\n5. Drained 650cc serosanguinous.\n6. Hooked to Pleurovac suction.\nPlan: Fluid studies.",
            5: "Michael Jackson needed a chest tube for that recurrent fluid on the left side ultrasound showed it was a bit complex with some septations used the 16 french tube this time went in mid axillary line drained about 650 of bloody looking fluid put it on suction 20 cm checking the xray later.",
            6: "A 16Fr pigtail catheter was inserted into the left pleural space (5-6 ICS, mid-axillary) for management of a recurrent complex effusion. The procedure was performed under real-time ultrasound guidance using the Seldinger technique. 650ml of serosanguinous fluid was drained. The tube was secured and placed to -20cmH2O suction. Post-procedure CXR confirmed placement.",
            7: "[Indication]\nRecurrent Pleural Effusion, Left.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nUS-guided insertion of 16Fr pigtail catheter. 650ml serosanguinous fluid drained.\n[Plan]\nSuction -20cm. Fluid analysis.",
            8: "We performed a bedside chest tube placement for Mr. Jackson to manage his recurrent left pleural effusion. Ultrasound revealed a complex fluid collection. We inserted a 16 French catheter into the left chest using the Seldinger technique, draining 650ml of serosanguinous fluid. The catheter was connected to suction, and we will monitor the output and fluid studies.",
            9: "Intervention: Thoracic drainage catheterization.\nFindings: Complex sinistral effusion.\nMethod: Under sonographic visualization, a 16Fr conduit was introduced. Serosanguinous exudate (650ml) was evacuated. Negative pressure was applied. Placement verification pending."
        }
    }
    return variations

def get_base_data_mocks():
    return [
        {"idx": 0, "orig_name": "Elizabeth Larkin", "orig_age": 89, "names": ["Betty Ross", "Eleanor Rigby", "Martha Kent", "Agnes Skinner", "Gertrude Stein", "Edith Piaf", "Mabel Pines", "Esther Greenwood", "Dorothy Gale"]},
        {"idx": 1, "orig_name": "Tammy Adams", "orig_age": 63, "names": ["Teresa Mendoza", "Tina Fey", "Tara Reid", "Tabitha Twitchit", "Tanya Tucker", "Trish Stratus", "Toni Braxton", "Thelma Dickerson", "Tess Ocean"]},
        {"idx": 2, "orig_name": "Sarah Jenkins", "orig_age": 54, "names": ["Susan Storm", "Sandra Bullock", "Sally Field", "Sharon Stone", "Sylvia Plath", "Simone Biles", "Selena Gomez", "Sigourney Weaver", "Scarlett Johansson"]},
        {"idx": 3, "orig_name": "Vince Yound", "orig_age": 65, "names": ["Victor Von Doom", "Vinnie Jones", "Vance Joy", "Vernon Dursley", "Val Kilmer", "Viggo Mortensen", "Vin Diesel", "Van Morrison", "Vito Corleone"]},
        {"idx": 4, "orig_name": "Michael Jackson", "orig_age": 72, "names": ["Mick Jagger", "Mike Tyson", "Matthew Perry", "Mark Twain", "Martin Sheen", "Morgan Freeman", "Mel Gibson", "Macaulay Culkin", "Matt Damon"]}
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
            
            # Replace placeholder name in the text variation
            text_variation = variations_text[idx][style_num]
            text_variation = text_variation.replace("[PATIENT_NAME]", new_name)
            
            # Update note_text with the variation
            note_entry["note_text"] = text_variation
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update Patient Demographics
                if "patient_demographics" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                # Update Procedure Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN (generate a synthetic one)
                if "patient_mrn" in note_entry["registry_entry"]:
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    if base_mrn == "Unknown" or base_mrn == "UNKNOWN":
                        base_mrn = f"MRN-{idx}"
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
    output_filename = output_dir / "synthetic_bronch_notes_part_025.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()