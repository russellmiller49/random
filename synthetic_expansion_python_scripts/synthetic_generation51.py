import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_051.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILENAME = "synthetic_notes_part_051.json"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the specific notes in Part 051.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Octavia Butler (Tracheal Stent/Laser)
            1: "Indication: Stridor, stent migration. \nProc: Rigid Bronch, Stent Exchange, Laser.\n- 14mm Rigid inserted.\n- Migrated stent in RMB removed with forceps.\n- 70% mid-tracheal obstruction (tumor ingrowth).\n- Tx: Nd:YAG laser (40W), mechanical coring, 12mm CRE balloon dilation.\n- New 16x50mm Dumon stent deployed.\n- Final: Airway patent. EBL 50cc.",
            2: "OPERATIVE NARRATIVE: The patient, a 65-year-old female with adenoid cystic carcinoma, presented with acute dyspnea secondary to prosthesis migration. Under general anesthesia with jet ventilation, the airway was cannulated with a 14mm rigid bronchoscope. The existing silicone stent was identified within the right mainstem bronchus and extracted. Significant tumor recurrence was noted at the proximal stent bed, narrowing the lumen by 70%. We utilized the Nd:YAG laser at 40 Watts for coagulative necrosis, followed by mechanical debridement with the rigid barrel. Balloon tracheoplasty was performed to 14mm. To maintain patency, a fresh 16x50mm Dumon silicone stent was deployed, covering the affected segment. Hemostasis was achieved.",
            3: "Procedures Performed:\n1. Bronchoscopy, Rigid, with removal of foreign body (stent) [31638].\n2. Bronchoscopy, Rigid, with destruction of tumor (Laser/Coring) [31641].\n\nTechnique:\nAccess obtained via rigid bronchoscope. Existing stent found migrated distally; removed using optical forceps. Tumor ingrowth at mid-trachea treated with Nd:YAG laser ablation and coring. Stenosis dilated with CRE balloon. A new 16x50mm Dumon stent was sized and placed. \nMedical Necessity: Critical central airway obstruction/stent failure.",
            4: "Procedure: Rigid Bronchoscopy / Stent Revision\nAttending: Dr. Frankenstein\nSteps:\n1. GA/Jet ventilation started.\n2. 14mm Rigid scope introduced.\n3. Old stent found in RMB -> Removed.\n4. Tumor regrowth (70%) seen mid-trachea.\n5. Laser (Nd:YAG) and coring used to open airway.\n6. Balloon dilation to 14mm.\n7. New Dumon stent (16x50mm) placed.\n8. EBL 50ml. Stable.",
            5: "patient octavia butler here for airway issue she has the adenoid cystic ca. stent slipped down to the right side so we went in with the rigid scope general anesthesia jet vent. pulled the old stent out no problem. saw tumor growing back about 70 percent blocked used the yag laser and the barrel to core it out then dilated with the balloon. put a new dumon silicone stent in 16 by 50 size looks good now airway open. little bit of bleeding stopped with saline.",
            6: "Rigid bronchoscopy was performed for stent migration and tumor ingrowth. The patient was placed under general anesthesia. A 14mm rigid scope was used. The migrated silicone stent was retrieved from the right mainstem. Inspection showed 70% obstruction from tumor regrowth in the mid-trachea. This was treated with 40W Nd:YAG laser, mechanical coring, and 12mm balloon dilation. A new 16x50mm Dumon silicone stent was deployed. The airway was patent at the end of the case. EBL was 50cc.",
            7: "[Indication]\nTracheal Adenoid Cystic Carcinoma, stent migration, stridor.\n[Anesthesia]\nGeneral TIVA, Jet Ventilation.\n[Description]\nRigid bronchoscopy (14mm). Migrated stent removed from RMB. Mid-tracheal tumor (70% stenosis) treated with Nd:YAG laser and mechanical coring. Balloon dilation performed. New 16x50mm Dumon stent placed.\n[Plan]\nICU monitoring.",
            8: "The patient was brought to the operating room for management of a migrated tracheal stent. After induction of general anesthesia and initiation of jet ventilation, a 14mm rigid bronchoscope was introduced. We located the previous stent migrated into the right mainstem bronchus and removed it using forceps. Further inspection revealed tumor ingrowth causing 70% obstruction at the mid-trachea. We applied Nd:YAG laser and performed mechanical coring to clear the obstruction, followed by balloon dilation. Finally, a new 16x50mm Dumon silicone stent was deployed, securing the airway.",
            9: "Operation: Rigid endoscopy, prosthesis extraction, photo-ablation, and stent deployment.\nSubject: 65F with tracheal malignancy.\nAction: The rigid instrument was introduced. The displaced prosthesis was retrieved from the right lung. Exophytic tissue causing 70% occlusion was vaporized with the Nd:YAG laser and cored. The stricture was expanded via balloon. A replacement 16x50mm Dumon stent was implanted.\nOutcome: Patency restored."
        },
        1: { # Leo Spaceman (ENB/EBUS - Failed Nav)
            1: "Proc: EBUS-TBNA + Attempted Nav Bronch.\nLN Sampling:\n- Stn 7 (12mm): 3 passes, benign.\n- Stn 4R (10mm): 3 passes, benign.\n- Stn 4L (8mm): 2 passes, benign.\nNavigation: Veran system. RUL nodule target. Reg error 5mm. Target NOT reached/visualized despite multiple attempts. Radial EBUS negative.\nOutcome: Mediastinum staged. Peripheral biopsy aborted.",
            2: "PROCEDURE SUMMARY: The patient underwent combined EBUS-TBNA and attempted electromagnetic navigation bronchoscopy. Systematic mediastinal staging was performed first. EBUS-guided transbronchial needle aspiration was conducted at stations 7, 4R, and 4L; rapid on-site evaluation indicated benign lymphocytes for all stations. Following this, the scope was exchanged for navigation to the 1.8cm RUL apical nodule. Despite minimizing registration error to 5mm and utilizing radial EBUS, the lesion could not be eccentrically or concentrically visualized. Consequently, the peripheral biopsy component was aborted to avoid non-diagnostic sampling of normal parenchyma.",
            3: "Billing Codes: 31653 (EBUS-TBNA 3+ stations), 31627 (Navigational Bronchoscopy).\n- EBUS: Stations 7, 4R, 4L sampled with needle aspiration. Cytology obtained.\n- Navigation: Planning and registration performed. Catheter advanced to RUL target zone. Lesion not confirmed via Radial EBUS (31654 not billed/bundled as no specific image obtained). Biopsy (31628) not performed.",
            4: "Resident Note\nPt: Leo Spaceman\nProc: EBUS + ENB\n1. EBUS scope in. Sampled 7, 4R, 4L. ROSE: Benign.\n2. Switched to therapeutic scope.\n3. Loaded Veran map. Navigated to RUL.\n4. Could not confirm target with REBUS.\n5. Stopped procedure without biopsy of nodule.\nPlan: Follow up or alternative biopsy method.",
            5: "Procedure note for leo spaceman doing the ebus and navigation today. Ebus went fine we hit station 7 and 4r and 4l all looked benign on the slides. Switched to the nav scope for that RUL nodule. Tried to get there with the veran system but just couldnt see it on the radial probe. tried a few times but no luck so we didnt stick a needle in it. biopsy aborted just the lymph nodes done today.",
            6: "Electromagnetic Navigation Bronchoscopy and EBUS-TBNA were performed. Linear EBUS was used to sample lymph node stations 7, 4R, and 4L; all were benign on ROSE. Electromagnetic navigation was then attempted for a 1.8cm RUL nodule. Despite registration, the target was not localized with radial EBUS. The decision was made to abort the peripheral biopsy due to lack of target confirmation. The procedure was concluded without complications.",
            7: "[Indication]\n1.8cm RUL nodule, mediastinal staging.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS-TBNA performed at stations 7, 4R, 4L. ROSE negative for malignancy. ENB attempted to RUL nodule. Lesion not visualized on Radial EBUS. Biopsy aborted.\n[Plan]\nOutpatient follow-up.",
            8: "We began the procedure with mediastinal staging using the linear EBUS scope. We successfully sampled lymph nodes at stations 7, 4R, and 4L, all of which showed benign lymphocytes on site. We then transitioned to the electromagnetic navigation phase to biopsy the RUL nodule. Although we navigated to the anatomical region, we could not confirm the lesion's location with radial EBUS. Therefore, we decided to abort the biopsy of the lung nodule to ensure patient safety.",
            9: "Procedure: Endobronchial Ultrasound and Guided Navigation.\nDetails: Nodal stations 7, 4R, and 4L were aspirated; onsite analysis showed benign cells. The instruments were exchanged for the electromagnetic guidance system. We navigated to the RUL apex but failed to localize the target lesion with ultrasound. The tissue sampling of the parenchymal nodule was cancelled."
        },
        2: { # G. Washington (Pleural/Thoracentesis/Pigtail)
            1: "Indication: Recurrent pleural effusion (L).\nProc: US-guided pleural drainage/catheter.\n- Site marked US.\n- Thoracentesis attempt 1: Dry tap.\n- Repositioned 2 spaces lower.\n- 18G needle entered fluid. Wire passed.\n- 8Fr Pigtail placed.\n- Output: 1400cc clear yellow.\nPlan: Culture/Cyto. Catheter to drainage.",
            2: "OPERATIVE REPORT: The patient presented with a recurrent large left pleural effusion. Ultrasound guidance was utilized to identify a pocket of fluid. An initial thoracentesis attempt at the primary site yielded no return. The puncture site was adjusted two intercostal spaces caudally. A Seldinger technique was then successfully employed to access the pleural space. An 8-French pigtail catheter was inserted and secured. Immediate drainage yielded 1400 mL of clear, exudative-appearing fluid. The patient tolerated the procedure well.",
            3: "Code: 32557 (Pleural drainage with indwelling catheter, with imaging).\nNarrative:\n- Ultrasound guidance used to verify fluid and entry.\n- Percutaneous entry made (initial dry tap bundled).\n- Guide wire inserted, tract dilated.\n- Tunneled indwelling catheter (Pigtail 8Fr) placed.\n- 1400cc drained.\nNote: Imaging guidance is integral to 32557.",
            4: "Procedure: Chest Tube/Pigtail Placement\nPatient: G. Washington\n1. US scan of L chest.\n2. Local lidocaine.\n3. First stick dry.\n4. Moved down. Hit fluid.\n5. Seldinger technique -> 8Fr Pigtail.\n6. Drained 1.4L yellow fluid.\n7. Secured and dressed.",
            5: "Mr Washington needed his chest drained again recurrent effusion left side. used the ultrasound. tried one spot with the needle and got nothing dry tap. moved down a couple ribs and got it. put the wire in then the 8 french pigtail catheter. drained about 1400cc of yellow fluid. leaving the tube in for now sending fluid to lab.",
            6: "Ultrasound-guided placement of indwelling pleural catheter. Indication was recurrent left pleural effusion. Local anesthesia was administered. An initial thoracentesis attempt was dry. The site was repositioned. The pleural space was accessed, and an 8Fr pigtail catheter was placed using Seldinger technique. 1400cc of clear yellow fluid was drained. The catheter was secured.",
            7: "[Indication]\nRecurrent large left pleural effusion.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nUS guidance used. Initial attempt dry. Successful access 2 interspaces lower. 8Fr Pigtail catheter placed. 1400cc drained.\n[Plan]\nDrainage to bag. Fluid analysis.",
            8: "Due to the patient's recurrent left pleural effusion, we proceeded with drainage. Using ultrasound, we marked the site. Our first attempt with the needle yielded no fluid, so we repositioned lower on the chest wall. On the second attempt, we successfully accessed the fluid pocket. We placed an 8 French pigtail catheter over a guidewire and drained 1400cc of fluid. The catheter was secured for ongoing drainage.",
            9: "Intervention: Percutaneous pleural drainage with catheter insertion.\nMethod: Sonographic localization. The initial aspiration was non-productive. A subsequent puncture inferiorly successfully engaged the effusion. An 8Fr drainage catheter was sited. \nVolume: 1400ml of serous fluid was evacuated."
        },
        3: { # M. Scott (Bronch Sedation/BAL/Brush)
            1: "Proc: Bronchoscopy, BAL, Brush.\nMD: Dr. Halpert (Mod Sed + Bronch).\nTime: 48 min.\nMeds: Fentanyl 100mcg, Versed 4mg.\nFindings: RML infiltrate. Mucous plug.\nAction: Suction, BAL RML, Brush RML.\nCodes: 31623, 31624, 99152, 99153 x2.",
            2: "PROCEDURE NOTE: Flexible fiberoptic bronchoscopy was performed by Dr. Halpert, who also directed the administration of moderate sedation (Fentanyl 100mcg/Versed 4mg). A dedicated independent observer monitored the patient throughout the 48-minute encounter. The airway inspection revealed an RML infiltrate and mucous plugging. Bronchoalveolar lavage and bronchial brushing of the right middle lobe were performed to identify an infectious etiology. The patient remained stable.",
            3: "Billing: \n- 31624: Bronchoscopy w/ BAL (RML).\n- 31623: Bronchoscopy w/ Brushing (RML).\n- 99152: Mod Sedation (Physician/Observer), initial 15 min.\n- 99153 x2: Mod Sedation add-on, 30 min additional.\nDocumentation supports 48 mins total time, dedicated observer present, same physician performing.",
            4: "Procedure: Bronch + BAL + Brush\nStaff: Dr. Halpert\nSedation: Fentanyl/Versed (Mod Sed). 48 mins.\nSteps:\n1. Scope in.\n2. Saw mucous plug RML.\n3. Did BAL.\n4. Did Brush.\n5. Pt tolerated well.\nLabs sent.",
            5: "Bronchoscopy on m. scott for that RML infiltrate. I did the sedation myself with the nurse watching fentanyl and versed used. Took about 48 minutes total. Went down saw some mucous in the middle lobe. Did a wash and a brush there. Patient did fine no oxygen drop.",
            6: "Flexible bronchoscopy with bronchoalveolar lavage and brushing. Indication was RML infiltrate. Moderate sedation provided by the bronchoscopist (48 minutes duration). Fentanyl 100mcg and Versed 4mg were used. Findings included RML mucous plugging. BAL and brush specimens were collected from the RML. Vital signs remained stable.",
            7: "[Indication]\nRML Infiltrate.\n[Sedation]\nModerate (Dr. Halpert + Observer). 48 min total.\n[Description]\nMucous plug RML. Suctioned. BAL and Brush performed RML.\n[Plan]\nCulture results pending.",
            8: "Dr. Halpert performed the bronchoscopy and administered the sedation for Mr. Scott, which lasted 48 minutes. Using Fentanyl and Versed, we achieved moderate sedation. Upon inspection, we found a mucous plug in the right middle lobe. We proceeded to suction the airway and collect both BAL and brush samples from the RML. The patient's vitals were stable throughout.",
            9: "Operation: Fiberoptic airway inspection with lavage and cytology brushing.\nSedation: Moderate, administered by operator (48m).\nFindings: RML consolidation and secretions.\nAction: The segment was irrigated (BAL) and sampled via brush.\nStatus: Stable."
        },
        4: { # Bruce Wayne (Cryobiopsy)
            1: "Indication: ILD (UIP/NSIP).\nTechnique: LMA, Flex Bronch, Radial EBUS.\n- RLL Basilar segments cleared via REBUS.\n- 1.9mm Cryoprobe.\n- Site 1: RLL Posterior Basal (5s freeze).\n- Site 2: RLL Lateral Basal (5s freeze).\n- Fogarty balloon used prophylactically.\n- 2 samples (10mm each).\n- No pneumothorax.",
            2: "OPERATIVE SUMMARY: The patient presented for diagnostic evaluation of progressive fibrotic interstitial lung disease. Under general anesthesia with a laryngeal mask airway, transbronchial cryobiopsy was performed. Radial EBUS confirmed the absence of significant vasculature in the target zones. A 1.9mm cryoprobe was utilized to obtain biopsies from the RLL posterior basal and lateral basal segments using a 5-second activation time. A Fogarty balloon was deployed immediately post-extraction for prophylactic hemostasis. Two substantial parenchymal specimens were retrieved.",
            3: "Codes: 31628 (Transbronchial lung biopsy, single lobe), 31654 (Radial EBUS guidance).\nJustification:\n- Biopsies taken from lung parenchyma (RLL) using cryoprobe supports 31628.\n- Radial EBUS utilized to survey biopsy site for safety supports 31654.\n- Note: Multiple biopsies in same lobe bundle into single 31628.",
            4: "Procedure: Cryobiopsy\nPt: Bruce Wayne\n1. LMA/GA.\n2. Radial EBUS check RLL bases.\n3. Cryoprobe to RLL Post Basal -> Freeze 5s -> Pull.\n4. Balloon up for bleeding control.\n5. Repeat in RLL Lat Basal.\n6. 2 good chunks.\n7. Fluoro/US check neg for pneumo.",
            5: "Did a cryobiopsy on mr wayne for his ILD today. Used the LMA and general. Checked with the radial ebus first to make sure no vessels were there. Froze for 5 seconds in the RLL posterior and lateral basal segments. Pulled the whole scope out with the sample. Used the fogarty balloon to stop any bleeding. Got two big pieces of lung. No pneumothorax on the ultrasound after.",
            6: "Transbronchial cryobiopsy for interstitial lung disease. General anesthesia with LMA. Radial EBUS guidance used. Biopsies obtained from RLL posterior basal and lateral basal segments. 1.9mm probe, 5-second freeze time. Fogarty balloon used for hemostasis. Two specimens obtained. Post-procedure imaging negative for pneumothorax.",
            7: "[Indication]\nFibrotic ILD, suspect UIP/NSIP.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nRadial EBUS used. 1.9mm Cryoprobe biopsies x2 in RLL (Posterior/Lateral Basal). Freeze time 5s. Fogarty balloon control. Specimens 10mm.\n[Plan]\nPathology pending. D/C home.",
            8: "We performed a cryobiopsy to evaluate Mr. Wayne's ILD. After placing an LMA, we used radial EBUS to ensure the biopsy sites in the right lower lobe were safe. We then advanced the cryoprobe and obtained biopsies from the posterior and lateral basal segments, freezing for 5 seconds each time. We used a Fogarty balloon to manage potential bleeding. We retrieved two large lung samples and confirmed there was no pneumothorax before finishing.",
            9: "Procedure: Transbronchial cryo-sampling of parenchyma.\nContext: Pulmonary fibrosis.\nMethod: Under LMA anesthesia, sonographic clearance was obtained. The cryo-instrument was applied to the RLL basilar segments. Freezing activation yielded two substantial tissue aggregates. Prophylactic balloon occlusion was employed.\nResult: Hemostasis secured. Lung intact."
        }
    }
    return variations

def get_base_data_mocks():
    # Names lists corresponding to the 9 variations for each original patient record
    return [
        {"idx": 0, "orig_name": "Octavia Butler", "orig_age": 65, "names": ["Mary Shelley", "Virginia Woolf", "Agatha Christie", "Ursula Le Guin", "Toni Morrison", "Jane Austen", "Emily Bronte", "Zora Neale Hurston", "Harper Lee"]},
        {"idx": 1, "orig_name": "Leo Spaceman", "orig_age": 55, "names": ["Jack Donaghy", "Kenneth Parcell", "Tracy Jordan", "Pete Hornberger", "Frank Rossitano", "James Lutz", "Floyd DeBarber", "Dennis Duffy", "Cerie Xerox"]},
        {"idx": 2, "orig_name": "G. Washington", "orig_age": 70, "names": ["John Adams", "Thomas Jefferson", "James Madison", "James Monroe", "John Quincy Adams", "Andrew Jackson", "Martin Van Buren", "William Harrison", "John Tyler"]},
        {"idx": 3, "orig_name": "M. Scott", "orig_age": 50, "names": ["Jim Halpert", "Dwight Schrute", "Stanley Hudson", "Kevin Malone", "Andy Bernard", "Creed Bratton", "Toby Flenderson", "Oscar Martinez", "Ryan Howard"]},
        {"idx": 4, "orig_name": "Bruce Wayne", "orig_age": 45, "names": ["Clark Kent", "Diana Prince", "Barry Allen", "Arthur Curry", "Hal Jordan", "Oliver Queen", "Victor Stone", "Billy Batson", "Carter Hall"]},
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
            # Handle potential missing index in variations map gracefully
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing variation text for Note {idx}, Style {style_num}")
                continue
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                reg = note_entry["registry_entry"]
                if "patient_age" in reg:
                    reg["patient_age"] = new_age
                if "procedure_date" in reg:
                    reg["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in reg:
                    reg["patient_mrn"] = f"{reg['patient_mrn']}_syn_{style_num}"
                
                # Update Evidence snippet if it exists (some fields mirror the text)
                if "evidence" in reg:
                    if "patient_age" in reg["evidence"]:
                        reg["evidence"]["patient_age"] = f"{new_age}"
                    if "procedure_date" in reg["evidence"]:
                        reg["evidence"]["procedure_date"] = f"Date: {rand_date_str}"
            
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
    output_path = output_dir / OUTPUT_FILENAME
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_path}")

if __name__ == "__main__":
    main()