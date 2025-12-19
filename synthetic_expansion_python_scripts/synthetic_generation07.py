import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (The new file you uploaded)
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_007.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Mock data for the 4 specific notes in bronch_notes_part_007.json.
    Since the source usually has 'UNKNOWN' for names, we assign base demographics here
    to be varied slightly by the script logic.
    """
    return [
        # Note 0: EUS-B + Radial EBUS (Lung mass)
        {
            "idx": 0, 
            "orig_name": "John Doe_0", 
            "orig_age": 65, 
            "names": [
                "Liam Smith", "Noah Johnson", "Oliver Williams", "Elijah Brown", "James Jones", 
                "William Garcia", "Benjamin Miller", "Lucas Davis", "Henry Rodriguez"
            ]
        },
        # Note 1: EBUS + Radial RLL (Small pneumo complication)
        {
            "idx": 1, 
            "orig_name": "Jane Doe_1", 
            "orig_age": 70, 
            "names": [
                "Olivia Wilson", "Emma Martinez", "Charlotte Anderson", "Amelia Taylor", "Sophia Thomas", 
                "Isabella Hernandez", "Ava Moore", "Mia Martin", "Evelyn Jackson"
            ]
        },
        # Note 2: Medical Thoracoscopy (Malignant Pleural Effusion)
        {
            "idx": 2, 
            "orig_name": "John Doe_2", 
            "orig_age": 55, 
            "names": [
                "Alexander White", "Sebastian Lopez", "Jack Lee", "Owen Gonzalez", "Theodore Harris", 
                "Wyatt Clark", "Jayden Lewis", "Luke Robinson", "Gabriel Walker"
            ]
        },
        # Note 3: EBUS Single Station 4R (Afib complication)
        {
            "idx": 3, 
            "orig_name": "Jane Doe_3", 
            "orig_age": 72, 
            "names": [
                "Harper Perez", "Camila Hall", "Gianna Young", "Abigail Allen", "Luna King", 
                "Ella Wright", "Elizabeth Scott", "Sofia Torres", "Avery Nguyen"
            ]
        }
    ]

def get_variations():
    """
    Contains the manually crafted text variations for the 4 notes in the input file.
    Structure: Note_Index (0-3) -> Style_Index (1-9) -> Text
    """
    
    variations = {
        # ---------------------------------------------------------------------
        # Note 0: EUS-B + Radial EBUS (Paraesophageal mass & LLL Nodule)
        # ---------------------------------------------------------------------
        0: {
            1: "Indication: Lung mass.\nAnesthesia: GA.\nProcedure:\n- EUS-B scope to esophagus. Mass sampled (22G). ROSE: Non-diagnostic.\n- Switched to Bronchoscope (LMA). Airway normal.\n- Radial EBUS to LLL posterior basal. Concentric view.\n- Biopsy: Forceps, needle, brush. BAL performed.\n- No complications.\nPlan: Await pathology.",
            
            2: "OPERATIVE NARRATIVE: The patient was brought to the endoscopy suite and placed under general anesthesia. An Olympus UC180F linear echoendoscope was introduced into the esophagus. The target paraesophageal mass was visualized abutting the aorta; transesophageal needle aspiration (EUS-B-FNA) was performed utilizing a 22-gauge needle. Rapid on-site evaluation (ROSE) was non-diagnostic. The echoendoscope was withdrawn and the airway secured with a laryngeal mask airway. A thin video bronchoscope (P190) was navigated to the left lower lobe posterior basal segment. A radial endobronchial ultrasound (R-EBUS) probe confirmed a concentric lesion. Sampling was executed via transbronchial needle aspiration, forceps biopsy, and cytological brushing, followed by bronchoalveolar lavage. The patient tolerated the procedure without immediate sequelae.",
            
            3: "CPT Coding Justification:\n43237 (EUS-B): Scope introduced orally into esophagus; ultrasound used to visualize and needle aspirate paraesophageal mass.\n31628 (Transbronchial Biopsy): Forceps biopsy performed on peripheral lesion in LLL posterior basal segment.\n31654 (Radial EBUS): Radial probe utilized to localize peripheral lesion prior to biopsy.\n31623 (Brushing): Brush biopsy of the same LLL site.\n31624 (BAL): Lavage performed in LLL.\nNote: EUS-B and Bronchoscopy were distinct services performed in the same session.",
            
            4: "Procedure Note\nAttending: [Name]\nResident: [Name]\nIndication: Lung mass.\nSteps:\n1. Time out. GA induced.\n2. EUS-B scope inserted. Paraesophageal mass biopsied (FNA). ROSE neg.\n3. Airway exchanged for LMA.\n4. Bronchoscope inserted. Inspection normal.\n5. Radial EBUS to LLL posterior basal segment (concentric view).\n6. Samples: TBBx, Brush, Needle, BAL.\n7. Tolerated well.",
            
            5: "patient consented and put under GA tube was already in for the first part used the ultrasound scope in the esophagus saw the mass by the aorta and stuck it with a 22 gauge needle rose didnt show much so we pulled that scope out and put in an LMA and the thin bronchoscope looked at the airways vocal cords normal trachea fine went down to the left lower lobe posterior basal branch used the radial probe saw the lesion concentric view took biopsies with needle forceps brush and did a wash sent everything to lab minimal bleeding no complications.",
            
            6: "Indications: Lung mass. Medications: General Anesthesia. The patient had been previously intubated. The UC180F convex probe EBUS bronchoscope was introduced through the mouth into the esophagus. Using vascular anatomy the scope was directed to the paraesophageal mass abutting the aorta. Sampling by TBNA performed with 22g needle. ROSE non-diagnostic. EBUS scope removed. ETT removed, LMA inserted. P190 scope introduced. Airways normal. LLL posterior basal segment identified. Radial EBUS inserted, concentric view obtained. Biopsies performed with needle forceps and brush. BAL performed. Samples sent. No complications.",
            
            7: "[Indication]\nLung mass requiring diagnosis.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\n1. EUS-B: Scope to esophagus. Mass visualized/sampled (22G). ROSE non-diagnostic.\n2. Bronchoscopy: LMA placed. Scope to LLL posterior basal. Radial EBUS confirmed concentric lesion. Biopsies (forceps, brush, needle) and BAL completed.\n[Plan]\nAwait culture and cytology.",
            
            8: "The procedure began with the patient under general anesthesia. We first introduced the convex probe EBUS scope into the esophagus to evaluate the known paraesophageal mass. Despite good visualization and needle aspiration, the on-site evaluation was non-diagnostic. Consequently, we switched to a flexible bronchoscope via an LMA. We navigated to the posterior basal segment of the left lower lobe, where we observed mucus. A radial EBUS probe confirmed the lesion's location with a concentric view. We proceeded to obtain samples using forceps, a brush, and a needle, concluding with a lavage. The patient remained stable throughout.",
            
            9: "Indications: Pulmonary lesion. Medications: GA. Action: The EBUS scope was deployed into the esophagus. The mass was visualized and aspirated with a 22G needle. ROSE was negative. The scope was withdrawn. An LMA was sited. The bronchoscope was navigated to the LLL. The lesion was localized with radial ultrasound. Tissue was harvested via forceps, brush, and needle. The segment was lavaged. The instrument was extracted. No adverse events."
        },
        
        # ---------------------------------------------------------------------
        # Note 1: EBUS + Radial RLL (Pneumothorax complication)
        # ---------------------------------------------------------------------
        1: {
            1: "Indication: Lung mass.\nAnesthesia: GA, LMA.\nFindings: Airways normal.\nEBUS: Stations 11L, 7, 10R, 11R sampled (22G). ROSE: Benign.\nRadial EBUS: RLL superior segment mass (concentric).\nBiopsy: TBNA x5, Forceps x6, Lavage.\nComplications: Hypoxia, Aspiration, Small Pneumothorax.\nPlan: Admit. Monitor.",
            
            2: "PROCEDURE: Flexible bronchoscopy with EBUS and radial probe guidance.\nINDICATION: Pulmonary mass suspicious for malignancy.\nFINDINGS: Initial airway inspection via LMA was unremarkable. Linear EBUS was utilized to systematically sample hilar and mediastinal nodes (11L, 7, 10R, 11R); ROSE indicated benign lymphocytes. A therapeutic scope was then used with a guide sheath and radial EBUS to localize the right lower lobe mass (superior segment). Transbronchial needle aspiration and forceps biopsies were performed under fluoroscopic guidance. \nCOMPLICATIONS: Post-procedure emesis with aspiration and development of a small pneumothorax.\nDISPOSITION: Admission for observation and antibiotics (Augmentin).",
            
            3: "Services Performed:\n- 31653 (EBUS Sampling 3+ stations): Sampled 11L, 7, 10R, 11R.\n- 31628 (Transbronchial Biopsy): Forceps biopsy of RLL mass.\n- 31654 (Radial EBUS): Used to identify peripheral lesion.\nNote: Fluoroscopy utilized. Procedure complicated by aspiration and pneumothorax requiring admission.",
            
            4: "Procedure: EBUS + Radial Bronch\nPatient: [Name]\n1. GA/LMA.\n2. Inspection: Normal.\n3. EBUS-TBNA: 11L, 7, 10R, 11R. ROSE benign.\n4. Radial EBUS: RLL Superior segment. Concentric view.\n5. Biopsies: Needle x5, Forceps x6. Mini-BAL.\n6. Complication: Aspiration and small pneumo noted post-op.\nPlan: Admit, antibiotics, CXR.",
            
            5: "patient consented risks explained general anesthesia used lma inserted airways looked fine no lesions used the ebus scope first sampled lymph nodes 11L 7 11R 10R rose said benign then switched to regular scope used guide sheath and radial ebus in the right lower lobe superior segment found the mass did needle biopsy 5 passes rose showed inflammation maybe abscess then did forceps biopsy 6 times and a wash patient vomited at the end maybe aspirated and has a small pneumothorax now admitting for observation.",
            
            6: "Indications: Lung mass. Medications: GA. Q190 scope introduced. LMA good position. Airways normal. UC180F EBUS scope introduced. Systematic survey done. Stations 11L, 7, 10R, 11R sampled with 22G needle. ROSE benign. Scope exchanged for Q180. Guide sheath to RLL superior segment. Radial EBUS confirmed mass. Peripheral TBNA x5. ROSE suspicious for abscess. Forceps biopsy x6 and lavage performed. Patient aspirated post-procedure. Small pneumothorax noted. Admitted.",
            
            7: "[Indication]\nLung mass, suspicious for malignancy.\n[Anesthesia]\nGeneral, LMA.\n[Description]\n1. EBUS-TBNA: Stations 11L, 7, 10R, 11R sampled. Benign on ROSE.\n2. Peripheral: Radial EBUS to RLL superior segment. TBNA x5, Forceps x6, Lavage.\n[Complications]\nAspiration, Hypoxia, Small Pneumothorax.\n[Plan]\nAdmit. Start Augmentin.",
            
            8: "We performed a bronchoscopy under general anesthesia to investigate a lung mass. Initially, we used an EBUS scope to sample mediastinal and hilar lymph nodes (stations 11L, 7, 10R, and 11R), all of which appeared benign on rapid evaluation. We then used a radial EBUS probe to locate the mass in the superior segment of the right lower lobe. Once visualized, we obtained multiple needle and forceps biopsies. Unfortunately, the patient vomited and aspirated near the end of the case, and subsequent imaging revealed a small pneumothorax. She was admitted for observation and antibiotics.",
            
            9: "Indication: Pulmonary nodule. Anesthesia: GA. Action: The airway was inspected and found patent. EBUS-guided aspiration was performed on nodes 11L, 7, 10R, and 11R. The therapeutic scope was deployed. Radial ultrasound localized the RLL lesion. The mass was sampled via needle and forceps. Lavage was completed. Complication: The patient regurgitated and aspirated. A pneumothorax was detected. Disposition: Admitted."
        },

        # ---------------------------------------------------------------------
        # Note 2: Medical Thoracoscopy (Left)
        # ---------------------------------------------------------------------
        2: {
            1: "Indication: Malignant Pleural Effusion.\nAnesthesia: Moderate (Fentanyl/Versed).\nProcedure: Left Medical Thoracoscopy.\n- Entry: Left 8th interspace.\n- Fluid: 800cc drained.\n- Findings: Diffuse carcinomatosis, adhesions.\n- Biopsy: Parietal pleura x5.\n- Exit: 14Fr Pigtail placed.\nResult: Lung re-expanded. No immediate complications.",
            
            2: "OPERATIVE REPORT: The patient was positioned in the right lateral decubitus position. Under moderate sedation and local anesthesia, a 14 Fr dilator was introduced into the left pleural space, followed by a trocar. Approximately 800 mL of serosanguinous fluid was evacuated. Rigid pleuroscopy revealed diffuse carcinomatosis and dense adhesions. Forceps biopsies (n=5) were obtained from the parietal pleura. A 14 Fr pigtail catheter was placed under direct visualization. Post-procedure imaging confirmed lung re-expansion.",
            
            3: "Billing Summary:\n- 32609: Thoracoscopy, diagnostic; with biopsy of pleura.\n- 32551 (Bundled): Tube thoracostomy.\n- Procedure: Rigid thoracoscopy left side. 1275cc fluid removed total. 5 biopsies taken of parietal pleura. Chest tube inserted.",
            
            4: "Procedure: Left Medical Thoracoscopy\nIndication: Malignant Effusion.\nSteps:\n1. Moderate sedation.\n2. Access: Left 8th rib space. 14Fr dilator -> Trocar.\n3. Suctioned 800cc fluid.\n4. Scope in. Saw carcinomatosis/adhesions.\n5. Biopsied parietal pleura x5.\n6. Placed 14Fr Pigtail.\n7. CXR: Re-expansion.",
            
            5: "patient positioned right lateral decubitus sterile prep lidocaine local used needle to find fluid put in wire and dilator then the port suctioned out 800 cc fluid looked inside with the rigid scope saw cancer everywhere and adhesions took 5 biopsies caused some bleeding suctioned more fluid put in a pigtail drain stitched it up chest xray showed lung up no complications sent fluid and tissue to lab.",
            
            6: "Indications: Malignant Pleural Effusion. Medications: Fentanyl, Midazolam, Lidocaine. Patient in right lateral decubitus. Ultrasound used to mark site. 18G needle entered pleural space. Guide wire passed. Dilator passed. 5mm port placed. 800cc fluid removed. Rigid telescope introduced. Findings: Diffuse carcinomatosis and adhesions. 5 biopsies taken from parietal pleura. 14Fr pigtail chest tube placed. Incision sutured. CXR confirmed re-expansion.",
            
            7: "[Indication]\nMalignant pleural effusion, need tissue.\n[Anesthesia]\nModerate Sedation + Local.\n[Description]\nLeft medical thoracoscopy performed. 1275ml total fluid removed. Pleura showed diffuse carcinomatosis. 5 parietal pleural biopsies taken. 14Fr pigtail catheter placed.\n[Plan]\nAwait pathology. Remove suture in 2 weeks.",
            
            8: "We performed a medical thoracoscopy on the left side to evaluate a malignant effusion. After achieving access in the 8th intercostal space, we drained about 800cc of fluid. The visual inspection showed extensive carcinomatosis and thick adhesions. We carefully took five biopsies from the parietal pleura. Following the biopsies, we drained the remaining fluid and placed a 14 French pigtail catheter. The patient tolerated the procedure well, and the lung re-expanded nicely.",
            
            9: "Indication: Pleural effusion. Anesthesia: Sedation. Action: Access was established in the left 8th interspace. Effusion was evacuated. The pleural cavity was inspected via rigid scope. Carcinomatosis was observed. The parietal pleura was sampled x5. A drainage catheter was deployed. Outcome: Re-expansion confirmed."
        },

        # ---------------------------------------------------------------------
        # Note 3: EBUS Single Station 4R (Afib complication)
        # ---------------------------------------------------------------------
        3: {
            1: "Indication: Mediastinal adenopathy.\nAnesthesia: GA, LMA.\nFindings: RUL obstruction (tumor/compression). oozing blood.\nEBUS: Station 4R (conglomerate). Sampled 22G. ROSE: Malignant.\nComplication: Intra-op Afib with RVR -> Cardioverted.\nDisposition: ICU.",
            
            2: "PROCEDURE: Bronchoscopy with Endobronchial Ultrasound (EBUS).\nFINDINGS: Diagnostic bronchoscopy revealed tumor infiltration of the bronchus intermedius and obstruction of the right upper lobe with active oozing. EBUS was performed, identifying a conglomerate lymph node mass at station 4R extending to 10R. Transbronchial needle aspiration confirmed malignancy. The procedure was complicated by the sudden onset of atrial fibrillation with rapid ventricular response, requiring bedside cardioversion. Hemostasis was confirmed prior to transfer to the ICU.",
            
            3: "CPT Code: 31652 (Bronchoscopy with EBUS, 1-2 stations).\nDetails: Sampled station 4R (conglomerate with 10R). 22G needle used.\nComplication: Patient developed Afib/RVR and hypotension requiring cardioversion (Critical Care time may apply separately).\nPathology: Malignant on ROSE.",
            
            4: "Procedure: EBUS Bronchoscopy\nPatient: [Name]\n1. GA/LMA.\n2. Inspection: Tumor in BI/RML. RUL obstructed/oozing.\n3. EBUS: Station 4R sampled. ROSE positive for cancer.\n4. Event: Pt went into Afib RVR + Hypotension.\n5. Intervention: Cardioversion (Successful).\n6. Plan: ICU admission. Consult Rad Onc.",
            
            5: "did the bronch under GA looked down and saw tumor everywhere especially right side RUL blocked and bleeding a bit then used the ebus scope looked at node 4R it was huge mixed with 10R stuck it with the needle rose said cancer patient went into afib with rvr and bp dropped had to cardiovert her woke her up checked for bleeding none seen sent to icu.",
            
            6: "Indications: Mediastinal adenopathy. Medications: GA. Q190 scope inserted. Findings: Submucosal infiltration bronchus intermedius/RML. RUL obstructed. EBUS scope inserted. Station 4R sampled (conglomerate). ROSE malignant. Complication: Patient developed tachycardia/hypotension/Afib RVR. Cardioversion performed successfully. Re-examination showed no active bleeding. Transferred to ICU.",
            
            7: "[Indication]\nMediastinal adenopathy, lung mass.\n[Anesthesia]\nGeneral.\n[Description]\nBronchoscopy showed extensive tumor R side. EBUS-TBNA of station 4R performed. ROSE: Malignant. Procedure complicated by new onset Afib/RVR and hypotension.\n[Intervention]\nBedside cardioversion. Successful.\n[Plan]\nICU observation. Rad Onc consult.",
            
            8: "The patient underwent an EBUS bronchoscopy to stage mediastinal adenopathy. Upon inspection, we found significant tumor infiltration in the right bronchial tree, obstructing the right upper lobe. We sampled the 4R lymph node using EBUS, which was positive for malignancy. Towards the end of the case, the patient went into atrial fibrillation with rapid ventricular response and became hypotensive. We successfully cardioverted her at the bedside. She was transferred to the ICU in stable condition.",
            
            9: "Indication: Adenopathy. Anesthesia: GA. Action: The airways were surveyed. Tumor was observed infiltrating the right bronchial tree. Station 4R was identified via ultrasound and aspirated. ROSE confirmed carcinoma. Adverse Event: The patient exhibited atrial fibrillation with hemodynamic instability. Cardioversion was executed. Disposition: The patient was admitted to the intensive care unit."
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
            
            # Get the specific name assigned for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the specific variation text
            # Note: We must ensure the variation exists
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation is missing (should not happen with full dictionary)
                note_entry["note_text"] = f"[VARIATION MISSING FOR IDX {idx} STYLE {style_num}]"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_demographics" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                # Some schemas put age directly in registry_entry
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age

                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update patient MRN to make it unique
                # If MRN is "UNKNOWN", we create a synthetic one
                current_mrn = note_entry["registry_entry"].get("patient_mrn", "UNKNOWN")
                if current_mrn == "UNKNOWN":
                    current_mrn = f"IP2026_{idx}"
                
                note_entry["registry_entry"]["patient_mrn"] = f"{current_mrn}_syn_{style_num}"
            
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
    output_filename = output_dir / "synthetic_bronch_notes_part_007.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()