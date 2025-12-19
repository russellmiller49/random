import json
import random
import datetime
import copy
from pathlib import Path

# Source file configuration
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_019.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILENAME = "synthetic_bronch_notes_part_019.json"

def generate_random_date(start_year, end_year):
    """Generates a random date within the given year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Provides mock base data (names/ages) for the 'UNKNOWN' patients in the source file.
    Ensures consistency across variations for a specific note index.
    """
    return [
        {
            "idx": 0, 
            "orig_name": "Arthur Dent", 
            "orig_age": 68, 
            "names": ["Liam Smith", "Noah Johnson", "Oliver Williams", "Elijah Brown", "James Jones", "William Garcia", "Benjamin Miller", "Lucas Davis", "Henry Rodriguez"]
        },
        {
            "idx": 1, 
            "orig_name": "Tricia McMillan", 
            "orig_age": 72, 
            "names": ["Emma Martinez", "Ava Hernandez", "Charlotte Lopez", "Amelia Gonzalez", "Sophia Wilson", "Mia Anderson", "Isabella Thomas", "Harper Taylor", "Evelyn Moore"]
        },
        {
            "idx": 2, 
            "orig_name": "Ford Prefect", 
            "orig_age": 65, 
            "names": ["Alexander Jackson", "Sebastian Martin", "Jack Lee", "Owen Perez", "Theodore Thompson", "Samuel White", "Wyatt Harris", "Caleb Sanchez", "Ryan Clark"]
        },
        {
            "idx": 3, 
            "orig_name": "Zaphod Beeblebrox", 
            "orig_age": 70, 
            "names": ["Levi Ramirez", "Isaac Lewis", "Gabriel Robinson", "Julian Walker", "Mateo Young", "Anthony Allen", "Jaxon King", "Lincoln Wright", "Joshua Scott"]
        },
        {
            "idx": 4, 
            "orig_name": "Marvin Android", 
            "orig_age": 55, 
            "names": ["Luna Torres", "Aurora Nguyen", "Violet Hill", "Hazel Flores", "Lily Green", "Chloe Adams", "Camila Nelson", "Penelope Baker", "Riley Hall"]
        }
    ]

def get_variations():
    """
    Returns a dictionary of text variations for each note index.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    variations = {
        # Note 0: RUL Cavitary Nodule (Nav + REBUS + TBNA/Bx/Brush + BAL)
        0: {
            1: "Procedure: Navigational Bronchoscopy (SuperDimension), Radial EBUS, Fluoroscopy.\nTarget: RUL cavitary nodule.\nActions:\n- Diagnostic inspection: Normal.\n- Navigation to RUL target.\n- Radial EBUS: Concentric view confirmed.\n- Sampling: TBNA, forceps biopsy, brush.\n- Mini-BAL performed.\nComplications: None.",
            2: "OPERATIVE REPORT\n\nINDICATION: Evaluation of left upper lobe pulmonary nodule (later localized to RUL).\n\nPROCEDURE: The patient was placed under general anesthesia. A T190 therapeutic videobronchoscope was advanced into the tracheobronchial tree, revealing normal anatomy. The SuperDimension electromagnetic navigation system was utilized to guide a catheter to the right upper lobe cavitary lesion. Verification was achieved via radial endobronchial ultrasound (EBUS), which demonstrated a concentric orientation. Subsequently, transbronchial needle aspiration, forceps biopsies, and bronchial brushing were performed under fluoroscopic guidance. A mini-bronchoalveolar lavage was also completed. Hemostasis was assured prior to termination.",
            3: "Coding Data:\n- 31627: Electromagnetic navigation used to access RUL lesion.\n- 31654: Radial EBUS probe used; concentric view obtained confirming peripheral lesion location.\n- 31629: Transbronchial needle aspiration of RUL lesion performed.\n- 31623: Bronchial brushing performed.\n- 31628: Transbronchial biopsies (forceps) performed.\n- 31624: Separate mini-BAL performed for microbiology.\nDevice: SuperDimension. Fluoroscopy time: Standard.",
            4: "Resident Procedure Note\nAttending: Dr. [Name]\nPatient: [Patient Name]\nProcedure: Navigational Bronchoscopy RUL\nSteps:\n1. Time out/Anesthesia (GA).\n2. Airway inspection: Normal.\n3. Navigation: SuperDimension catheter to RUL.\n4. Confirmation: Radial EBUS showed concentric view.\n5. Biopsies: Needle, forceps, and brush used. Mini-BAL done.\n6. Hemostasis: Confirmed.\nPlan: Post-op CXR, await path.",
            5: "Procedure note pt had general anesthesia airway looked fine no masses. Used the super dimension thing to get to the RUL nodule radial probe showed it was concentric so we biopsied it. Used needle forceps and brush also did a wash. No bleeding really. Send to recovery check a cxr thanks.",
            6: "The patient was brought to the bronchoscopy suite and placed under general anesthesia. The T190 scope was inserted. Inspection revealed normal tracheal and bronchial anatomy. We utilized the SuperDimension navigation system to access the right upper lobe cavitary nodule. Radial EBUS confirmed the location with a concentric view. We proceeded to sample the lesion using a peripheral needle, biopsy forceps, and a cytology brush. A mini-BAL was also collected. The patient tolerated the procedure well with no estimated blood loss.",
            7: "[Indication]\nLeft upper lobe nodule (found in RUL during procedure).\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nScope inserted. Normal anatomy. SuperDimension navigation used to reach RUL target. Radial EBUS confirmed concentric view. TBNA, forceps biopsy, and brushing performed under fluoro. Mini-BAL completed. No bleeding.\n[Plan]\nCXR. Discharge home.",
            8: "The patient arrived for evaluation of a pulmonary nodule. After induction of general anesthesia, we inserted a T190 bronchoscope. The airway inspection was unremarkable. We then employed electromagnetic navigation to guide our instruments to the right upper lobe. Once in the vicinity, we used a radial EBUS probe to verify our position, achieving a nice concentric view of the lesion. We took multiple samples using a needle, forceps, and brush, and finished with a mini-lavage. Everything went smoothly without complications.",
            9: "Following induction, the bronchoscope was introduced. The airways were surveyed and found to be patent. We navigated to the right upper lobe lesion using electromagnetic guidance. Localization was corroborated with radial ultrasound showing a concentric return. The lesion was sampled via needle aspiration, forceps excision, and brushing. A lavage was also collected. No hemorrhage occurred."
        },
        # Note 1: RLL Nodule (Nav + REBUS + TBNA/Bx/Brush + ROSE)
        1: {
            1: "Dx: Multiple nodules, RLL target.\nAnesth: GA, 8.0 ETT.\nFindings: Normal airway. No endobronchial lesions.\nAction: SuperDimension nav to RLL. Radial EBUS: Concentric.\nIntervention: TBNA, forceps bx, triple needle brush.\nROSE: Malignancy positive.\nComp: None.",
            2: "PROCEDURE: Electromagnetic navigation bronchoscopy with radial EBUS confirmation and multimodal sampling.\nNARRATIVE: Under general anesthesia with an 8.0 endotracheal tube, the tracheobronchial tree was inspected and found to be unremarkable. Utilizing pre-procedural mapping and the SuperDimension system, the 190-degree edge catheter was navigated to the right lower lobe nodule. Radial endobronchial ultrasound confirmed a concentric orientation. Diagnostic sampling was executed using a transbronchial needle, biopsy forceps, and a triple-needle brush. Rapid On-Site Evaluation (ROSE) confirmed malignancy. Hemostasis was secured.",
            3: "CPT Justification:\n- 31627 (Navigation): Computer-assisted navigation required to reach peripheral RLL nodule.\n- 31654 (REBUS): Ultrasound used to confirm tool-in-lesion (concentric view).\n- 31629 (TBNA): Needle aspiration performed.\n- 31628 (Biopsy): Forceps biopsies taken.\n- 31623 (Brush): Triple needle brush utilized.\nNote: ROSE confirmed malignancy. Fluoroscopy utilized.",
            4: "Procedure: Navigational Bronchoscopy RLL\nStaff: Dr. X\nTechnique:\n1. Intubation with 8.0 ETT.\n2. Diagnostic bronchoscopy: Normal.\n3. Navigation: SuperDimension to RLL.\n4. Confirmation: R-EBUS concentric.\n5. Biopsy: Needle, Forceps, Brush.\n6. ROSE: Positive for cancer.\n7. EBL < 5cc.",
            5: "We did a bronchoscopy today for the lung nodules used general anesthesia put in a tube. Looked around airway was clear. Used the navigation system to get to the RLL nodule radial probe showed we were right in it concentric view. Did needle biopsy forceps and the brush thing. Pathologist said it was cancer right there in the room. No bleeding patient did fine extubated sent to recovery.",
            6: "Following induction of general anesthesia and intubation, a T190 bronchoscope was advanced. Airway anatomy was normal. The SuperDimension navigation catheter was guided to the right lower lobe nodule. Radial EBUS confirmed a concentric view. Sampling was performed with a peripheral needle, forceps, and triple needle brush. ROSE was consistent with malignancy. There were no complications.",
            7: "[Indication]\nMultiple pulmonary nodules, RLL target suspicious for malignancy.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nNavigated to RLL nodule using SuperDimension. Radial EBUS showed concentric view. Biopsies taken with needle, forceps, and brush. ROSE positive for malignancy. No bleeding.\n[Plan]\nCXR. Await final path.",
            8: "The patient was intubated for a bronchoscopy to investigate suspicious lung nodules. We inspected the airways and found no visible tumors. Using the navigational catheter, we steered to the right lower lobe nodule. The radial ultrasound probe confirmed we were centrally located within the lesion. We proceeded to take samples using a needle, forceps, and a brush. The pathologist in the room confirmed cancer cells were present. The patient woke up well.",
            9: "The bronchoscope was deployed through the ETT. The bronchial tree was surveyed. We navigated to the RLL target using electromagnetic guidance. The position was verified with radial ultrasound. We sampled the lesion using needle aspiration, forceps excision, and brushing. Rapid assessment indicated malignancy. The procedure was concluded without incident."
        },
        # Note 2: RUL (Anomalous Segment) Nav Bronch
        2: {
            1: "Indication: RUL nodule.\nAnatomy: RUL anomalous inferior takeoff.\nProcedure: Nav bronch (SuperDimension). Radial EBUS confirmed.\nSampling: TBNA (5 passes), Forceps (3), Brush (1).\nROSE: Adequate.\nEBL: 5cc. No complications.",
            2: "OPERATIVE NOTE: Bronchoscopy with Electromagnetic Navigation.\nANATOMICAL FINDINGS: Normal trachea/carina. Right upper lobe exhibited an anomalous inferior segmental takeoff.\nPROCEDURE: The SuperDimension system was utilized to navigate to the RUL nodule via the anomalous segment. Radial EBUS confirmed the target. Fluoroscopically guided transbronchial needle aspiration (5 passes), forceps biopsies (3 samples), and brushing were performed. Rapid On-Site Evaluation confirmed adequate cellularity.",
            3: "Service Performed: 31627 (Nav), 31654 (REBUS), 31629 (TBNA), 31628 (Bx), 31623 (Brush).\nDetails: Navigation required due to peripheral location in anomalous RUL segment. Radial EBUS used for confirmation. Multiple modalities used (needle, forceps, brush) to ensure diagnostic yield. ROSE performed.",
            4: "Resident Note\nProcedure: Nav Bronch RUL\nKey Finding: Anomalous inferior takeoff RUL.\nSteps:\n1. LMA placed.\n2. Navigated to RUL nodule via anomaly.\n3. R-EBUS confirmed site.\n4. TBNA x5, Forceps x3, Brush x1.\n5. ROSE: Adequate.\nPlan: Discharge when criteria met.",
            5: "Bronchoscopy for the RUL nodule patient has an anomalous segment there. We used the superdimension to find it radial ultrasound confirmed it. Did a bunch of biopsies needle forceps brush. ROSE said we got good tissue. Little bit of bleeding 5cc maybe. Patient did ok sent to recovery.",
            6: "The patient underwent general anesthesia with an LMA. Inspection revealed an anomalous inferior takeoff in the right upper lobe. SuperDimension navigation was used to access the RUL nodule through this segment. Radial ultrasound confirmed the location. We performed TBNA, forceps biopsies, and brushing under fluoroscopic guidance. ROSE confirmed adequate tissue. The patient tolerated the procedure well.",
            7: "[Indication]\nRight upper lobe nodule.\n[Anesthesia]\nGeneral (LMA).\n[Description]\nAnomalous RUL segment identified. Navigated to lesion. Radial EBUS confirmation. 5 needle passes, 3 forceps biopsies, 1 brush. ROSE adequate.\n[Plan]\nDischarge. Await path results.",
            8: "We performed a bronchoscopy on this patient to check a nodule in the right upper lobe. Interestingly, we found an anomalous airway segment in that lobe. We used our navigation system to go down that specific segment and checked our position with ultrasound. It looked good, so we took several samples with a needle, forceps, and a brush. The onsite pathologist said we had enough tissue. The patient is doing fine.",
            9: "The scope was introduced via LMA. We observed an anomalous RUL segment. We navigated to the target and verified position with radial ultrasound. We sampled the area using needle aspiration, forceps excision, and brushing. On-site evaluation deemed the samples adequate. Hemostasis was achieved."
        },
        # Note 3: LLL Accessory Segment (Fibrotic Lesion)
        3: {
            1: "Indication: Ca Lung recurrence suspicion.\nAirway: Accessory airway proximal to RLL superior segment.\nAction: Converted LMA to ETT. Navigated to LLL accessory segment.\nFindings: Concentric REBUS view. Firm lesion.\nBiopsy: Forceps (scant), TBNA x6 (21G/19G).\nResult: Adequate samples.",
            2: "PROCEDURE: Radial EBUS-guided bronchoscopy with TBNA and biopsy.\nFINDINGS: Anatomic variant noted on right (accessory airway). Target lesion located in left lower lobe accessory segment. Due to airway instability, LMA was exchanged for ETT. Radial EBUS demonstrated a concentric view of the lesion within the LLL accessory segment. The lesion was fibrotic/firm.\nSAMPLING: Forceps biopsies yielded scant tissue. Subsequent TBNA using 21G and 19G needles (6 passes total) provided adequate specimens.",
            3: "Codes: 31629 (TBNA - Primary), 31654 (REBUS).\nNote: Forceps biopsy (31628) attempted but scant; TBNA was the primary retrieval method (6 passes). Navigation system mentioned (SuperDimension needle used) but REBUS was primary guidance method. Fluoroscopy not stated.",
            4: "Resident Note\nPt: Lung Ca recurrence?\nIssue: LMA unstable -> Intubated.\nTarget: LLL accessory segment.\nSteps:\n1. Radial EBUS -> Concentric view.\n2. Forceps -> Too hard/scant.\n3. Needles (21G/19G) -> 6 passes.\n4. Samples adequate.\nPlan: Path pending.",
            5: "Patient has lung cancer maybe back again. We tried with LMA but had to switch to a tube because it wouldnt stay. Found a weird accessory segment in the LLL. Radial ultrasound showed the mass. It was super hard forceps didnt get much so we used the needles did 6 passes. Got enough stuff then. No bleeding.",
            6: "Under general anesthesia, the patient required conversion from LMA to ETT due to positioning difficulties. Inspection revealed a right-sided accessory airway, but the target was in the left lower lobe accessory segment. Radial EBUS showed a concentric lesion. Forceps biopsies were scant due to fibrosis. Six TBNA passes were performed with 21G and 19G needles, yielding adequate samples.",
            7: "[Indication]\nLung cancer recurrence suspicion.\n[Anesthesia]\nPropofol (Converted LMA to ETT).\n[Description]\nTarget: LLL accessory segment. Radial EBUS concentric. Lesion firm. Forceps scant. 6 TBNA passes performed for adequate sample.\n[Plan]\nMonitor. Path results.",
            8: "This patient came in for a biopsy of a suspected recurrent lung cancer. We started with an LMA but had to switch to a breathing tube to get a better airway. We found the spot in an accessory segment of the left lower lobe. The ultrasound confirmed we were in the right place. The tumor was really hard, so the forceps didn't work well. We switched to needles and took six samples, which looked better. No complications.",
            9: "The bronchoscope was inserted. Airway exchange to ETT was required. We navigated to the LLL accessory segment. Position was verified with radial ultrasound. The lesion was sampled via forceps (scant) and needle aspiration (6 passes). Samples were adequate. No adverse events."
        },
        # Note 4: LLL BAL (Infiltrates)
        4: {
            1: "Indication: Immunocompromised, infiltrates.\nProcedure: Diagnostic Bronch, BAL.\nFindings: Normal airway anatomy/mucosa.\nAction: Wedged in LLL anterior segment. BAL 150cc instilled, 55cc return.\nPlan: Await Micro/Cyto.",
            2: "PROCEDURE: Flexible fiberoptic bronchoscopy with bronchoalveolar lavage.\nINDICATION: Evaluation of interstitial infiltrates in an immunocompromised host.\nFINDINGS: Visual inspection of the tracheobronchial tree revealed normal mucosa and anatomy without endobronchial lesions. The bronchoscope was wedged in the anterior segment of the left lower lobe.\nLAVAGE: A total of 150 mL of saline was instilled in aliquots, with a return of 55 mL. Fluid sent for cytology and microbiology.",
            3: "Billing Code: 31624 (Bronchoscopy with BAL).\nTechnique: Scope wedged in LLL anterior segment. 150ml saline instilled.\nMedical Necessity: Interstitial infiltrates/infection workup.\nNote: Diagnostic inspection (31622) is bundled. No fluoroscopy or biopsies performed.",
            4: "Resident Note\nProcedure: Bronch/BAL\nIndication: Infiltrates\nSteps:\n1. Scope passed.\n2. Inspection: Normal.\n3. Wedged LLL anterior.\n4. BAL: 150cc in / 55cc out.\n5. Tolerated well.\nPlan: Check culture results.",
            5: "Did a bronch on this immunocompromised patient with infiltrates. Just a wash today. Everything looked normal inside. Went down to the LLL anterior segment put in 150 of saline got back 55. Sent it to the lab. No bleeding patient is fine.",
            6: "The patient underwent moderate sedation. A Q190 bronchoscope was introduced. The airway inspection was unremarkable with normal mucosa and anatomy. The scope was wedged in the left lower lobe anterior segment. Bronchoalveolar lavage was performed using 150 cc of saline with 55 cc recovery. The procedure was uncomplicated.",
            7: "[Indication]\nInterstitial infiltrates, immunocompromised.\n[Anesthesia]\nModerate (Fentanyl/Versed/Lido).\n[Description]\nAirway normal. Wedged LLL anterior segment. BAL performed (150cc/55cc). Fluid sent for analysis.\n[Plan]\nAwait micro/cyto results.",
            8: "We performed a bronchoscopy to check for infection in this immunocompromised patient. The airways looked completely normal. We wedged the scope in the left lower lobe and washed it out with saline. We collected the fluid and sent it to the lab to check for bacteria or other issues. The patient tolerated it well.",
            9: "The bronchoscope was introduced. The airways were surveyed and found unremarkable. We positioned the scope in the LLL anterior segment. Lavage was performed with saline instillation and retrieval. Specimens were submitted for analysis."
        }
    }
    return variations

def main():
    # Load original data
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
        print(f"Error: Source file must contain a JSON array.")
        return
    
    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through each original note
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            print(f"Warning: No mock data for note index {idx}. Skipping.")
            continue
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Iterate through the 9 styles
        for style_num in range(1, 10):
            
            # Deep copy to avoid mutating original
            note_entry = copy.deepcopy(original_note)
            
            # 1. Randomize Age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # 2. Randomize Date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # 3. Get new Patient Name
            new_name = record['names'][style_num - 1]
            
            # 4. Update Note Text (The Style Rewrite)
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # 5. Update Registry Entry Fields (if they exist)
            if "registry_entry" in note_entry and note_entry["registry_entry"]:
                reg = note_entry["registry_entry"]
                
                # Update MRN
                if "patient_mrn" in reg:
                    # If UNKNOWN, create a synthetic one, else append suffix
                    if reg["patient_mrn"] == "UNKNOWN" or reg["patient_mrn"] is None:
                        reg["patient_mrn"] = f"SYN_PT_{idx}_{style_num}"
                    else:
                        reg["patient_mrn"] = f"{reg['patient_mrn']}_syn_{style_num}"
                
                # Update Procedure Date
                if "procedure_date" in reg:
                    reg["procedure_date"] = rand_date_str
                
                # Update Patient Demographics if structure exists, else insert into root of registry_entry if appropriate
                # The schema varies slightly in the input, let's try to find where age/name might go or just leave name out if not strictly in schema
                # Some entries have patient_demographics dict, some might have it at root.
                # We will check specific locations based on the input file structure provided.
                
                # Input file has "patient_age" usually in root of registry_entry or implicit. 
                # Note: The provided input json blocks don't all explicitly show an 'age' field in registry_entry root 
                # (some have 'patient_demographics': null). We will inject it into root for consistency with the request.
                reg["patient_age"] = new_age
                
                # Inject Name (usually not in registry_entry in these specific examples, but good for metadata)
                reg["patient_name"] = new_name

            # 6. Add Synthetic Metadata
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

    # Output to JSON
    output_path = output_dir / OUTPUT_FILENAME
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_path}")

if __name__ == "__main__":
    main()