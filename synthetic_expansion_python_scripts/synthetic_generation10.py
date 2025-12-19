import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_010.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Variations for the 3 specific notes in bronch_notes_part_010.json
    # Structure: Note_Index (0-2) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Note 1: RUL Nodule, EBUS (4R/11R), DECAMP Research samples
            1: "Indication: RUL nodule staging.\nAnesthesia: General (LMA).\nProcedure:\n- Inspection: RML dynamic collapse (fish-mouth). No endobronchial lesions.\n- Radial EBUS (RUL apical): Eccentric view. Bx: Needle, forceps, brush. ROSE: Malignancy.\n- Linear EBUS: 4R (lymphocytes), 11R (non-diagnostic).\n- Research (DECAMP): Brushing/TBLB in RUL, RML, LUL.\nComplications: None. EBL 5cc.\nPlan: Post-procedure unit.",
            2: "OPERATIVE REPORT\nINDICATION: Evaluation of pulmonary nodule.\nPROCEDURE: The patient was placed under general anesthesia. A Q190 videobronchoscope was utilized to inspect the tracheobronchial tree, revealing dynamic collapse of the right middle lobe but no endobronchial abnormalities. A P190 ultrathin scope was subsequently navigated to the right upper lobe apical segment. Radial endobronchial ultrasound (REBUS) confirmed an eccentric acoustic signature of the lesion. Diagnostic sampling via peripheral needle, forceps, and cytological brush confirmed malignancy on rapid on-site evaluation (ROSE). Following this, a UC180F convex probe EBUS was employed for mediastinal staging; stations 4R and 11R were sampled. Finally, per DECAMP protocol, research brushings and transbronchial biopsies were acquired from the RUL, RML, and LUL.\nIMPRESSION: RUL malignancy diagnosed; staging completed.",
            3: "CPT Coding Justification:\n- 31654 (Radial EBUS): Utilized probe to localize peripheral RUL apical lesion (eccentric view).\n- 31628 (TBLB Single Lobe): Biopsies taken from RUL target; malignancy confirmed.\n- 31652 (EBUS-TBNA): Sampled 2 mediastinal/hilar stations (4R, 11R) for staging.\n- +31632 x2 (TBLB Add'l Lobes): Additional biopsies performed in RML and LUL for DECAMP research protocol.\nMedical Necessity: Staging and diagnosis of pulmonary nodule.",
            4: "Procedure Note\nAttending: Dr. [Name]\nPatient: James Wilson\nProcedure: Bronchoscopy with EBUS and Biopsy\nSteps:\n1. Time out. GA induced.\n2. Inspection: RML fish-mouthing noted.\n3. RUL Apical Nodule: Localized with Radial EBUS (eccentric). Biopsied (forceps/brush/needle). ROSE positive for cancer.\n4. EBUS Staging: 4R and 11R sampled.\n5. Research: DECAMP samples taken from RUL, RML, LUL.\n6. No complications.",
            5: "patient here for lung nodule propofol used tube in airway looked ok mostly except rml collapsing a bit used the thin scope to get to the rul apical spot radial ebus saw it eccentric took biopsies rose said cancer then switched to ebus scope poked 4r and 11r nodes then did the research biopsies decamp study in rul rml and lul no bleeding patient woke up fine.",
            6: "Pulmonary nodule requiring diagnosis/staging. Propofol infusion via anesthesia assistance. Procedure, risks, benefits, and alternatives were explained. Following intravenous medications, the Q190 video bronchoscope was introduced. The tracheobronchial tree was examined. Anatomy was normal with exception of fish mouth dynamic obstruction of the right middle lobe. The P190 ultrathin bronchoscope was inserted into the apical segment of the right upper lobe. Radial EBUS showed an eccentric view. Biopsies performed (needle, forceps, brush). ROSE identified malignancy. UC180F EBUS scope introduced. Station 4R and 11R sampled. DECAMP research samples performed with brushing/biopsy in RUL, RML, LUL. No active bleeding. Complications: None.",
            7: "[Indication]\nPulmonary nodule, RUL.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nAirway inspection showed RML dynamic airway collapse. Radial EBUS localized RUL apical lesion (eccentric). Biopsies (forceps/brush/needle) confirmed malignancy (ROSE). Linear EBUS performed on stations 4R and 11R. Additional research samples (DECAMP) taken from RUL, RML, LUL.\n[Plan]\nDischarge when criteria met.",
            8: "The patient presented for evaluation of a right upper lobe pulmonary nodule. Under general anesthesia, we inspected the airways, noting a fish-mouth obstruction in the RML. Switching to the ultrathin scope, we navigated to the RUL apical segment. Radial EBUS provided an eccentric view of the target. We obtained diagnostic tissue using forceps, brush, and needle; on-site pathology confirmed malignancy. We then proceeded to staging with the linear EBUS scope, sampling stations 4R and 11R. Finally, to satisfy the DECAMP research protocol, we performed additional brushings and biopsies in the RUL, RML, and LUL. The patient tolerated the procedure well.",
            9: "Reason: Lung mass assessment.\nTechnique: Propofol sedation. Bronchoscope deployed. RML fish-mouthing observed. Ultrathin scope navigated to RUL apical region. Radial sonography displayed eccentric signal. Lesion sampled via forceps and brush. ROSE verified carcinoma. EBUS scope utilized to aspirate nodes 4R and 11R. Research specimens harvested from RUL, RML, and LUL. Hemostasis achieved."
        },
        1: { # Note 2: Pulmonary Nodule, Failed Navigation, Tracheomalacia
            1: "Indication: Pulmonary nodule.\nAnesthesia: Deep (Propofol).\nFindings:\n- Large/floppy epiglottis.\n- Tracheomalacia present.\n- Distal airways normal.\n- EBUS: Nodule not visualized.\n- EMN: Target not reached.\nAction: No biopsies taken. Secretions suctioned.\nPlan: Thoracic tumor board discussion.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the bronchoscopy suite for evaluation of a pulmonary nodule. Under deep sedation, the airway was examined using a Q190 bronchoscope. Significant findings included large arytenoids, a floppy epiglottis, and tracheomalacia extending to the carina. No endobronchial lesions were observed. An attempt was made to visualize the nodule via endobronchial ultrasound, but the lesion could not be identified. Subsequently, electromagnetic navigation was attempted using a therapeutic bronchoscope; however, the target could not be successfully accessed. The procedure was terminated without tissue acquisition to avoid complications.",
            3: "Billing Summary:\n- 31622 (Diagnostic Bronchoscopy): Primary service. Inspection revealed tracheomalacia.\n- +31627 (Navigation Add-on): Electromagnetic navigation was set up and attempted ('inserted therapeutic bronchoscope for electromagnetic navigation'), justifying the professional work despite inability to reach target.\n- Note: No biopsy codes (31628/31625) reported as no tissue was obtained.",
            4: "Procedure Note\nPatient: Robert Taylor\nStaff: Dr. X\nIndication: Lung Nodule\nProcedure: Bronchoscopy with attempted Navigation\nDetails:\n1. LMA placed.\n2. Airway exam: Tracheomalacia and floppy epiglottis noted.\n3. EBUS attempt: Nodule not seen.\n4. Navigation attempt: Unable to reach nodule.\n5. Outcome: No specimens collected.\nPlan: Discuss at Tumor Board.",
            5: "patient came in for a nodule used propofol lma airway inspection showed floppy epiglottis and tracheomalacia trachea collapsing a bit tried to find the nodule with ebus didn't see it tried the electromagnetic navigation catheter couldn't get out to the lesion so we stopped no biopsy taken today will talk to tumor board next tuesday.",
            6: "Indications: Pulmonary Nodule. Medications: Propofol infusion. The Q190 video bronchoscope was introduced. The arytenoids were large with a large and floppy epiglottis. Tracheomalacia was noted as we advanced the scope to the carina. No evidence of endobronchial disease. We then removed the bronchoscope and inserted the EBUS bronchoscope. We attempted to visualize the nodule with endobronchial ultrasound but did not see the nodule. We then inserted the therapeutic bronchoscope for electromagnetic navigation bronchoscopy. We were not able to get to the nodule using the navigation equipment. Procedure completed without specimen collection.",
            7: "[Indication]\nPulmonary Nodule.\n[Anesthesia]\nPropofol (Deep).\n[Description]\nDiagnostic inspection revealed tracheomalacia and floppy epiglottis. EBUS attempted; nodule not visualized. Electromagnetic navigation attempted; target not reached. No biopsies performed.\n[Plan]\nRefer to Cardiothoracic Tumor Board.",
            8: "We performed a bronchoscopy to evaluate a pulmonary nodule. Upon inspection, the patient exhibited significant upper airway laxity with a floppy epiglottis and tracheomalacia down to the carina. We attempted to locate the nodule first with EBUS and then with electromagnetic navigation. Unfortunately, neither modality allowed us to visualize or reach the target lesion. Consequently, no biopsies were performed. The patient remained stable, and we plan to present the case at the upcoming tumor board meeting.",
            9: "Indication: Lung Nodule.\nTechnique: Propofol infusion. Scope inserted. Observed tracheomalacia and redundant epiglottic tissue. EBUS scan failed to localize the mass. Navigation system deployed but failed to access the target. No tissue harvested. Procedure concluded without sampling."
        },
        2: { # Note 3: LLL Nodule, Accessory Airway, Radial EBUS/Sheath, Complication (ICU)
            1: "Indication: LLL nodule.\nFindings: R accessory airway. LLL nodule.\nProcedure:\n- Slim scope/TBNA: Nondiagnostic.\n- Linear EBUS: 'Wedged' mass, 2 passes (blood only).\n- Therapeutic scope + Fluoroscopy + Sheath: Radial EBUS concentric view.\n- Biopsies: Forceps, brush. ROSE negative.\nComplication: Post-op laryngeal edema/stridor. Glidescope intubation. \nPlan: Admit to ICU.",
            2: "PROCEDURE: Bronchoscopy with Multimodal Biopsy.\nFINDINGS: Anatomic variant noted (accessory airway distal to RLL superior segment). Diagnostic inspection otherwise normal. A peripheral nodule in the LLL was targeted.\nTECHNIQUE: Initial attempt with slim scope and peripheral TBNA was nondiagnostic. Linear EBUS wedging of the target yielded only blood. Finally, a therapeutic scope utilizing a large sheath and fluoroscopic guidance achieved a concentric radial EBUS view. Forceps and brush biopsies were obtained (ROSE negative).\nADVERSE EVENT: Immediate post-procedure respiratory distress with audible stridor. Intubation was required via Glidescope due to laryngeal edema. Patient transferred to ICU for stabilization.",
            3: "Coding: \n- 31652 (EBUS-TBNA): Primary code for linear EBUS sampling of lung mass.\n- 31628 (TBLB): Forceps biopsy of LLL nodule via sheath/fluoro.\n- 31623 (Brushing): Brush biopsy of LLL nodule.\n- +31654 (Radial EBUS): Add-on for peripheral localization (concentric view).\nNote: Complication (Respiratory Failure J96.00) supports high-complexity management.",
            4: "Resident Note\nPatient: Mary Davis\nProcedure: LLL Biopsy\nSteps:\n1. Inspection: Accessory airway right side.\n2. Attempt 1: Slim scope TBNA (neg).\n3. Attempt 2: Linear EBUS wedged (blood).\n4. Attempt 3: Therapeutic scope + Sheath + Fluoro. REBUS concentric. Biopsies taken.\nComplication: Patient developed stridor/edema post-extubation. Emergent intubation performed by anesthesia. Transferred to ICU.",
            5: "did a bronch for a lll nodule saw an accessory airway on the right tried the slim scope first with tbna rose was neg then tried linear ebus wedge just got blood finally used the big scope with the sheath and fluoro got a concentric view on radial ebus took biopsies rose still negative but good samples anyway after we finished patient had stridor couldn't breathe laryngeal edema had to intubate with glidescope going to icu.",
            6: "Indications: Pulmonary Nodule. Anatomy: Accessory airway right lower lobe. Procedure: P190 slim scope used for peripheral TBNA (negative). UC180F EBUS scope wedged in LLL; biopsies showed blood. T190 scope with large sheath and fluoroscopy used. Radial EBUS confirmed concentric view. Forceps and brush biopsies obtained. ROSE negative. Complications: Post-procedure audible upper airway sounds and difficult ventilation. Laryngeal edema noted. Converted to endotracheal intubation via Glidescope. Patient transferred to ICU.",
            7: "[Indication]\nLLL pulmonary nodule.\n[Anesthesia]\nGeneral (Propofol).\n[Description]\nAccessory airway noted on right. LLL nodule targeted. Linear EBUS sampling nondiagnostic. Sheath-guided biopsy with Fluoroscopy and Radial EBUS (concentric) performed. Forceps/brush samples obtained.\n[Complications]\nUpper airway edema requiring emergent re-intubation.\n[Plan]\nICU admission.",
            8: "Ms. Davis underwent bronchoscopy for a left lower lobe nodule. We noted an accessory airway on the right side. Initial attempts to sample the nodule using a slim scope and linear EBUS were nondiagnostic. We then utilized a therapeutic scope with a guide sheath and fluoroscopy; radial EBUS confirmed a concentric view, allowing for forceps and brush biopsies. Unfortunately, upon completion, the patient developed significant laryngeal edema and respiratory distress. We were unable to ventilate effectively, necessitating urgent intubation with a Glidescope. She was admitted to the ICU for monitoring.",
            9: "Indication: LLL mass.\nFindings: Right accessory bronchus. LLL lesion.\nAction: Slim scope TBNA attempted. Linear EBUS aspiration performed (hemodiluted). Therapeutic scope deployed with sheath and fluoroscopy. Radial sonography showed concentric signal. Lesion sampled via forceps and brush. \nAdverse Event: Post-procedural stridor and ventilatory failure due to laryngeal swelling. Endotracheal tube placed via video laryngoscopy. Patient transported to critical care."
        }
    }
    return variations

def get_base_data_mocks():
    # Base identities to be used for the variations
    return [
        {"idx": 0, "orig_name": "James Wilson", "orig_age": 65, "names": ["John Smith", "Robert Johnson", "Michael Williams", "David Brown", "Richard Jones", "Charles Garcia", "Joseph Miller", "Thomas Davis", "Christopher Rodriguez"]},
        {"idx": 1, "orig_name": "Robert Taylor", "orig_age": 70, "names": ["Daniel Martinez", "Paul Hernandez", "Mark Lopez", "Donald Gonzalez", "George Wilson", "Kenneth Anderson", "Steven Thomas", "Edward Taylor", "Brian Moore"]},
        {"idx": 2, "orig_name": "Mary Davis", "orig_age": 60, "names": ["Patricia Jackson", "Jennifer Martin", "Linda Lee", "Elizabeth Perez", "Barbara Thompson", "Susan White", "Jessica Harris", "Sarah Sanchez", "Karen Clark"]},
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
            # Use style 1 if specific style text is missing (fallback), though all 9 should be there
            variation_text = variations_text[idx].get(style_num, variations_text[idx][1])
            note_entry["note_text"] = variation_text
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update MRN
                if "patient_mrn" in note_entry["registry_entry"]:
                    current_mrn = note_entry["registry_entry"]["patient_mrn"]
                    if current_mrn == "UNKNOWN":
                        current_mrn = f"IP2025_{idx+1:03d}"
                    note_entry["registry_entry"]["patient_mrn"] = f"{current_mrn}_syn_{style_num}"
                
                # Update Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update Demographics (Age/Gender) - check structure
                # The structure varies slightly in the input file (flat vs nested in patient_demographics)
                # We handle both common patterns seen in the input
                
                # Pattern 1: Flat patient_age in registry_entry (not present in this file, but good for robustness)
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                
                # Pattern 2: Nested in patient_demographics
                if "patient_demographics" in note_entry["registry_entry"] and note_entry["registry_entry"]["patient_demographics"] is not None:
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                elif "patient_demographics" in note_entry["registry_entry"]:
                     # If null, initialize it
                     note_entry["registry_entry"]["patient_demographics"] = {"age_years": new_age}

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
    output_filename = output_dir / "synthetic_bronch_notes_part_010.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()