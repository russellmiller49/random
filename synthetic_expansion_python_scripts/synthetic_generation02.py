import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_002.json"

OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the given year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    variations = {
        # Note 0: 74M, RUL Nodule, Ion, TBNA, Cryo, BAL, Chartis LUL
        0: {
            1: "Indication: RUL nodule.\nProcedure: Ion robotic bronchoscopy (31627) with TBNA (31629) and Cryobiopsy (31628). BAL RUL (31624). Chartis LUL (31634).\nFindings:\n- Airway normal.\n- Navigated to RB3 nodule (1.4cm). CBCT confirmed.\n- TBNA x6, Cryo x5 obtained.\n- ROSE: Atypical cells.\n- Chartis LUL: CV Negative.\nComplications: None.",
            2: "HISTORY: A 74-year-old gentleman presented for diagnostic evaluation of a right upper lobe pulmonary nodule.\nPROCEDURE: General anesthesia was induced. The Ion endoluminal system was utilized to navigate to the anterior segment of the right upper lobe. Target acquisition was verified via cone-beam computed tomography (CBCT) with 3D reconstruction. Extensive sampling was performed utilizing both transbronchial needle aspiration and cryobiopsy techniques. Subsequent Chartis assessment of the left upper lobe demonstrated a complete absence of collateral ventilation, favorable for future valve intervention.\nIMPRESSION: Successful robotic-assisted sampling of RUL lesion; LUL confirmed as CV-negative.",
            3: "CPT Codes Supporting Medical Necessity:\n- 31627 (Navigation): Required for peripheral RUL lesion access.\n- 31629 (TBNA): Primary sampling method (21G/23G).\n- 31628 (Biopsy): Transbronchial cryobiopsy performed for distinct histological yield.\n- 31624 (BAL): Performed in separate aliquots for microbiology.\n- 31634 (Balloon Occlusion): Chartis assessment performed in contralateral (Left) lung to assess collateral ventilation for future therapy.\nTechnique: Ion platform with CBCT confirmation.",
            4: "Procedure: Robotic Bronchoscopy (Ion), TBNA, Cryobiopsy, BAL, Chartis.\nAttending: Dr. [Name].\nSteps:\n1. Time out.\n2. ETT placed. Airway exam normal.\n3. Ion catheter to RUL anterior segment.\n4. Spin CT confirmed tool in lesion.\n5. Biopsies taken (needle + cryo). ROSE atypical.\n6. BAL performed.\n7. Chartis balloon check in LUL (negative for CV).\n8. Extubated stable.",
            5: "patient 74 male here for rul spot used ion robot to get there confirmed with the spin ct took a bunch of biopsies needle and freezing probe rose said maybe atypical cells washed the area too then checked the left side with chartis balloon showed no flow so good for valves later no bleeding patient woke up fine",
            6: "The patient was brought to the bronchoscopy suite and placed under general anesthesia. An airway inspection revealed no endobronchial lesions. Using the Ion robotic platform, we navigated to the target lesion in the RUL anterior segment. Position was verified with 3D spin imaging. Multiple TBNAs and cryobiopsies were obtained. A bronchoalveolar lavage was performed. We then switched to the Chartis system to evaluate the left upper lobe, which showed no collateral ventilation. The patient tolerated the procedure well.",
            7: "[Indication]\nRUL Nodule, COPD.\n[Anesthesia]\nGeneral, ETT.\n[Description]\n1. Inspection: Normal airways.\n2. Navigation: Ion to RUL RB3.\n3. Confirmation: Cone Beam CT.\n4. Sampling: TBNA x6, Cryo x5, BAL.\n5. Staging: Chartis LUL (CV Negative).\n[Plan]\nDischarge. Await pathology.",
            8: "We began the procedure by inducing general anesthesia and securing the airway. The therapeutic bronchoscope was introduced, showing a healthy tracheobronchial tree. We then employed the Ion robotic system to navigate to the 1.4 cm nodule in the right upper lobe's anterior segment. Once near the target, we utilized Cone Beam CT to precisely adjust our position. Samples were collected via needle aspiration and cryoprobe. Following this, we performed a Chartis assessment on the left upper lobe, confirming the absence of collateral ventilation.",
            9: "Indication: Pulmonary mass.\nAction: Deployed Ion catheter to RUL. Verified location via CBCT. Acquired tissue via aspiration and cryo-adhesion. Lavaged the segment. Assessed collateral airflow in LUL.\nResult: Samples secured. LUL isolated.\nOutcome: Uncomplicated."
        },
        # Note 1: 68M, Multiple Nodules (RLL/RUL), Ion, Radial EBUS, TBNA/Bx, PTX
        1: {
            1: "Indication: Multiple nodules.\nProcedure: Ion Nav bronch. R-EBUS (aerated). TBNA/Bx RLL & RUL.\nFindings:\n- RLL basal: Abnormal tissue seen. Biopsied.\n- RUL posterior: Cavitary. TBNA.\n- Mucus plugs suctioned centrally.\nComplication: Post-op Pneumothorax (stable, no chest tube).\nPlan: Discharge with close follow-up.",
            2: "OPERATIVE SUMMARY: The patient presented with multifocal pulmonary nodules. Robotic navigation (Ion) was employed to systematically interrogate targets in the right lower and right upper lobes. Radial EBUS was utilized but remained non-diagnostic due to local aeration. Transbronchial needle aspiration and biopsy were performed under fluoroscopic guidance. Significant mucus plugging was noted and evacuated via therapeutic aspiration. The postoperative course was complicated by a moderate pneumothorax which remained stable without intervention.",
            3: "Billable Services:\n- 31627 (Navigational Bronchoscopy): Used for RLL and RUL targets.\n- 31629 (TBNA): Primary biopsy code (RLL).\n- +31633 (TBNA Add-on): Additional lobe (RUL).\n- 31628 (Biopsy): Forceps biopsy RLL.\n- 31624 (BAL): Lavage RLL.\n- 31645 (Therapeutic Aspiration): Documentation supports clearing of central airways (trachea, carina, mainstems) separate from biopsy sites.\n- +31654 (Radial EBUS): Attempted localization.",
            4: "Resident Note\nPatient: Eduardo Santiago, 68M.\nProcedure: Ion Bronchoscopy.\nTargets: 1. RLL Lateral Basal (solid). 2. RUL Posterior (cavitary).\nSteps:\n- Navigated to RLL. R-EBUS aerated. Visualized tissue. Bx taken.\n- Navigated to RUL. R-EBUS aerated. TBNA taken.\n- Cleared mucus plugs from central airway.\nComplication: PTX on CXR. Stable.",
            5: "procedure for multiple lung nodules used the ion robot went to rll first couldn't see on ebus but saw tissue so biopsied it rose said inflammatory then went to rul cavitary lesion again ebus no help but took needle samples suctioned out a lot of thick mucus plugs patient had a pneumothorax after but didn't need a tube sent home",
            6: "After induction of general anesthesia, the airway was inspected and found to be normal. Robotic navigation was used to approach a lesion in the RLL lateral basal segment. Radial EBUS did not visualize the lesion, but abnormal tissue was seen endoscopically and biopsied. We then navigated to a cavitary lesion in the RUL posterior segment and performed TBNA. Bronchoalveolar lavage was performed in the RLL. Therapeutic aspiration was required to clear significant mucus from the central airways. A post-procedure chest X-ray revealed a moderate pneumothorax that did not require drainage.",
            7: "[Indication]\nMultiple solid/cavitary nodules.\n[Anesthesia]\nGeneral + Lidocaine.\n[Description]\n- Ion Nav to RLL & RUL.\n- Radial EBUS: Aerated (non-diagnostic).\n- Sampling: TBNA, Brush, Forceps.\n- Intervention: Mucus plug removal.\n[Complication]\nPneumothorax (conservative management).\n[Plan]\nFollow-up imaging next week.",
            8: "The patient, a 68-year-old male, underwent robotic bronchoscopy to evaluate multiple nodules. We first navigated to the right lower lobe, where despite non-diagnostic radial EBUS, we visualized and sampled abnormal tissue. We then proceeded to the right upper lobe cavitary lesion for further needle aspiration. Significant mucus plugging in the central airways required extensive therapeutic aspiration. Although a pneumothorax developed post-procedure, it was stable and the patient was discharged.",
            9: "Reason: Polytopic pulmonary lesions.\nTechnique: Robotic guidance engaged. Sonographic interrogation attempted. Tissue acquired via needle and forceps. Lavage executed. Secretions evacuated.\nAdverse Event: Iatrogenic pneumothorax, self-limited."
        },
        # Note 2: Broncholith/Rigid Bronch (Aborted)
        2: {
            1: "Indication: Bronchus intermedius obstruction.\nProcedure: Rigid Bronchoscopy (12mm). Therapeutic Aspiration.\nFindings:\n- Polypoid mass in BI.\n- Soft, pulsatile, brisk bleeding on touch.\n- EBUS: Vascular, no tumor.\nAction: Suctioned purulent secretions. Aborted debulking due to hemorrhage risk.\nDx: Broncholith (CT confirmed).\nComplication: Small PTX.",
            2: "OPERATIVE REPORT: The patient presented with high-grade obstruction of the bronchus intermedius. Rigid bronchoscopy was performed to facilitate airway management. A polypoid, pulsatile mass was visualized obstructing the lumen. Manipulation precipitated brisk hemorrhage, controlled with topical epinephrine. Linear EBUS assessment revealed significant vascularity and absence of distinct tumor architecture, suggestive of a broncholith. Mechanical debulking was deemed unsafe and the procedure was aborted after aspiration of post-obstructive secretions.",
            3: "Coding Rationale:\n- 31645 (Therapeutic Aspiration): Primary service. Cleared purulent secretions from distal airways.\n- 31622 (Diagnostic Rigid Bronch): Bundled.\n- 31640 (Tumor Excision): NOT billed as procedure was aborted due to risk.\nNote: Linear EBUS used for assessment only, no nodes sampled. CT Angio ordered post-op.",
            4: "Procedure: Rigid Bronchoscopy\nFindings: Mass in BI, completely obstructing. Purulent fluid behind it.\nSteps:\n1. LMA -> Flex scope. Saw mass.\n2. Rigid scope inserted.\n3. Suctioned pus (31645).\n4. Touched mass -> Bleeding. Stopped w/ Epi.\n5. EBUS -> Vascular.\n6. Aborted.\nPlan: Consult Thoracic Surgery.",
            5: "attempted bronchoscopy for airway blockage saw a mass in the bronchus intermedius put in the rigid scope suctioned out a lot of pus behind the block tried to touch the mass and it bled heavily used epi and txa looks like a broncholith on scan so we stopped before causing a major bleed patient admitted",
            6: "The patient was placed under general anesthesia. Initial flexible bronchoscopy revealed a mass obstructing the bronchus intermedius. A 12 mm rigid bronchoscope was inserted. We bypassed the obstruction to suction purulent secretions. Manipulation of the mass caused brisk bleeding, and ultrasound examination revealed nearby vessels. We decided to abort any resection to avoid hemorrhage. Post-procedure imaging suggests a broncholith.",
            7: "[Indication]\nBronchus Intermedius Obstruction.\n[Anesthesia]\nGeneral, Rigid/Jet Ventilation.\n[Description]\n- Obstructing mass identified.\n- Post-obstructive pus aspirated.\n- Mass manipulation -> Hemorrhage (controlled).\n- Procedure aborted.\n[Diagnosis]\nBroncholithiasis.\n[Plan]\nSurgical consult.",
            8: "We performed a rigid bronchoscopy to address a blockage in the bronchus intermedius. Upon visualization, the mass appeared polypoid and highly vascular, bleeding easily upon contact. We successfully aspirated purulent secretions from the distal airways to treat the post-obstructive pneumonia. However, ultrasound analysis indicated the mass was likely a broncholith with significant vascular risk, so we aborted the debulking portion of the procedure.",
            9: "Indication: Airway occlusion.\nMethod: Rigid endoscopy. Jet ventilation.\nFindings: Endoluminal obstruction. Hemorrhage upon palpation. Purulence evacuated.\nDecision: Resection halted due to vascular hazard.\nOutcome: Broncholithiasis confirmed."
        },
        # Note 3: EBUS-TBNA + RML Biopsy
        3: {
            1: "Indication: Adenopathy, nodules.\nProcedure: EBUS-TBNA (4R, 11R, 7). Ultrathin bronchoscopy RML.\nFindings: Normal central airway. RML nodule visualized w/ Radial EBUS.\nAction: TBNA nodes. Forceps/Brush RML.\nEBL: <5cc.\nComplications: None.",
            2: "PROCEDURE NOTE: The patient underwent combined endobronchial ultrasound (EBUS) staging and peripheral nodule biopsy. Linear EBUS facilitated transbronchial needle aspiration of mediastinal and hilar stations 4R, 7, and 11R. Subsequently, an ultrathin bronchoscope was utilized to navigate to the right middle lobe. Radial EBUS confirmed the target location, and biopsies were obtained via forceps and brush. The procedure was uncomplicated.",
            3: "Codes:\n- 31653 (EBUS-TBNA): 3 stations sampled (4R, 11R, 7).\n- 31625 (Biopsy): RML endobronchial lesion.\n- 31623 (Brush): RML.\n- +31654 (Radial EBUS): Peripheral localization.\nNote: No navigation code (31627) billed as 'anatomical knowledge' was cited, not EM/Robotic nav.",
            4: "Resident Procedure Note\nStaff: Dr. [Name]\nScope: EBUS & Ultrathin\n1. EBUS TBNA: Stations 4R, 11R, 7.\n2. Diagnostic Bronch: RML lesion seen.\n3. Radial EBUS: Confirmed.\n4. Bx: Forceps and Brush.\nPlan: Await path.",
            5: "patient with nodes and nodules did ebus first sampled 4r 11r and 7 sent for cytology then switched to the thin scope went to the rml found the spot with radar and took biopsies and brushing everything went fine no bleeding",
            6: "Following induction of anesthesia, an airway inspection was performed and found normal. A linear EBUS scope was introduced, and lymph nodes at stations 4R, 11R, and 7 were sampled. The scope was exchanged for an ultrathin bronchoscope. Using anatomical landmarks and radial EBUS, a lesion in the RML was localized and sampled using forceps and a brush. The patient tolerated the procedure well.",
            7: "[Indication]\nAdenopathy, Pulmonary Nodule.\n[Anesthesia]\nPropofol (Anesthesia managed).\n[Description]\n- EBUS-TBNA: 4R, 11R, 7.\n- RML Nodule: Localized w/ REBUS.\n- Samples: Biopsy, Brush.\n[Plan]\nPathology follow-up.",
            8: "We began with mediastinal staging using the convex probe EBUS, sampling lymph node stations 4R, 11R, and 7. Following this, we switched to an ultrathin bronchoscope to address the right middle lobe nodule. Radial EBUS was used to confirm the lesion's location distally. We successfully obtained tissue samples using both biopsy forceps and a cytology brush.",
            9: "Objective: Staging and diagnosis.\nTechnique: Ultrasonic needle aspiration of mediastinum. Distal cannulation of RML. Sonographic confirmation. Tissue acquisition via forceps/brush.\nStatus: Completed."
        },
        # Note 4: Infection/BAL (Chronic Cough)
        4: {
            1: "Indication: Chronic cough, Hx BMT.\nProcedure: Diagnostic Bronchoscopy, BAL, Wash.\nFindings: Diffuse edema, erythema, thick purulent secretions. No masses.\nAction: RLL Wash. RML BAL (90cc).\nPlan: Cultures pending. Start mucus clearance.",
            2: "BRONCHOSCOPY REPORT: A diagnostic bronchoscopy was performed to evaluate chronic cough in a post-bone marrow transplant patient. Visual inspection revealed diffuse mucosal edema, erythema, and copious purulent secretions throughout the tracheobronchial tree. No focal endobronchial lesions were identified. A bronchoalveolar lavage was performed in the right middle lobe, and a bronchial washing was collected from the right lower lobe for microbiological analysis.",
            3: "Billing:\n- 31624 (BAL): RML (Primary code).\n- 99152 (Moderate Sedation): Fentanyl/Versed by proceduralist.\n- 31622 (Diagnostic): Bundled.\n- 31645 (Aspiration): Bundled (incidental suctioning of secretions).\nDiagnosis: J41.1 (Chronic Purulent Bronchitis), Z94.81 (Bone marrow transplant status).",
            4: "Procedure: Bronch + BAL\nIndication: BMT patient with cough.\nSedation: Fent/Versed.\nFindings: Boggy airways, lots of pus. No tumors.\nIntervention: BAL RML, Wash RLL.\nPlan: Await cultures, start saline nebs.",
            5: "bronch for cough history of bmt airways look terrible red swollen pus everywhere did a bal in the rml and a wash in the rll sent it all off for culture gave some sedation patient did fine start flutter valve",
            6: "The patient was sedated with Fentanyl and Versed. The bronchoscope was introduced, revealing diffuse airway edema and thick purulent secretions. No focal masses were seen. We performed a bronchial wash in the RLL and a bronchoalveolar lavage in the RML. The samples were sent for culture and cytology. The patient tolerated the procedure without complications.",
            7: "[Indication]\nChronic cough, immunocompromised (BMT).\n[Anesthesia]\nModerate Sedation.\n[Description]\n- Findings: Diffuse inflammation, purulence.\n- RLL: Bronchial Wash.\n- RML: BAL.\n[Plan]\nMucus clearance regimen.",
            8: "We performed a bronchoscopy to investigate the patient's chronic cough. Upon entering the airways, we noted significant inflammation, with boggy, erythematous mucosa and thick purulent secretions scattered throughout. We washed the right lower lobe and performed a formal lavage of the right middle lobe. These samples were submitted for extensive microbiological testing to rule out opportunistic infection.",
            9: "Reason: Tussis, post-transplant.\nObservations: Mucosal hyperemia, edema, purulence.\nExecuted: Lavage of RML. Washing of RLL.\nDisposition: Pending microbiology."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns a list of mock data to ensure consistency across styles for each original note.
    """
    return [
        # Note 0
        {"idx": 0, "orig_name": "Henry Ford", "orig_age": 74, "names": ["George Miller", "Arthur Dent", "William Stryker", "James Logan", "Edward Stark", "Richard Castle", "Thomas Wayne", "Gary Oak", "Henry Pym"]},
        # Note 1
        {"idx": 1, "orig_name": "Eduardo Santiago", "orig_age": 68, "names": ["Carlos Rivera", "Juan Valdez", "Miguel Sanchez", "Luis Guzman", "Roberto Duran", "Jose Altuve", "Pedro Pascal", "Diego Luna", "Antonio Banderas"]},
        # Note 2
        {"idx": 2, "orig_name": "John Doe", "orig_age": 70, "names": ["Robert Smith", "David Jones", "Michael Brown", "Chris Evans", "Daniel Craig", "Paul Rudd", "Mark Ruffalo", "Jeremy Renner", "Tom Hiddleston"]},
        # Note 3
        {"idx": 3, "orig_name": "Jane Doe", "orig_age": 60, "names": ["Sarah Connor", "Ellen Ripley", "Leia Organa", "Dana Scully", "Clarice Starling", "Laurie Strode", "Sidney Prescott", "Nancy Thompson", "Alice Abernathy"]},
        # Note 4
        {"idx": 4, "orig_name": "Bob Smith", "orig_age": 55, "names": ["Kevin Flynn", "Sam Flynn", "Tron", "Clu", "Rinzler", "Zuse", "Jarvis", "Castor", "Dillinger"]},
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
            continue
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Iterate through the 9 styles
        for style_num in range(1, 10):
            
            # Deep copy the original note structure
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            # Handle cases where age might be missing in original logic, though we use mock orig_age
            new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_demographics" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                # Update procedure_date
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Create/Update patient_mrn
                if "patient_mrn" in note_entry["registry_entry"]:
                     base_mrn = note_entry["registry_entry"]["patient_mrn"]
                     if base_mrn == "UNKNOWN":
                         base_mrn = f"IP202600{idx}"
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
    output_filename = output_dir / "synthetic_bronch_notes_part_002.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()