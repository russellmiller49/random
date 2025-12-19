import json
import random
import datetime
import copy
from pathlib import Path

# Source file configuration
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_008.json"
OUTPUT_FILENAME = "synthetic_ebus_notes_part_008.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the specified year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each of the 5 notes in the source file.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Note 0: Testicular CA, CPT 31653 (3 stations: 7, 4R, 11R)
            1: "Indication: Hx testicular cancer, mediastinal LAD.\nProcedure: EBUS-TBNA.\n- LMA placed. Airway normal.\n- EBUS scope introduced.\n- Stations sampled: 7 (16.6mm), 4R (5.7mm), 11Rs (8.9mm).\n- 5 passes per station (22G needle).\n- Cytology sent.\nComplications: None. EBL < 5cc.",
            2: "HISTORY: The patient, with a known history of testicular carcinoma status post chemotherapy, presented with mediastinal adenopathy.\nPROCEDURE: General anesthesia was induced. A systematic EBUS examination was conducted. Radiographically enlarged lymph nodes were identified at stations 7, 4R, and 11Rs. Real-time ultrasound guidance facilitated transbronchial needle aspiration (TBNA) using a 22-gauge needle. Five passes were completed at each of the three stations to ensure adequate cellularity for staging. \nIMPRESSION: Successful staging EBUS involving three distinct nodal stations.",
            3: "Procedure: Bronchoscopy with EBUS sampling (CPT 31653).\nTechnique:\n1.  Ultrasound visualization of three distinct nodal stations: Subcarinal (7), Right Lower Paratracheal (4R), and Right Interlobar (11R).\n2.  Needle selection: Olympus 22G EBUS-TBNA.\n3.  Sampling: 5 passes were performed at each of the 3 stations to ensure diagnostic yield.\n4.  Specimen handling: All samples prepared for cytology.\nJustification: Evaluation of mediastinal/hilar nodes in cancer staging requires sampling of 3+ stations.",
            4: "Procedure Note\nAttending: Dr. [Name]\nResident: Dr. [Name]\nIndication: Staging testicular cancer.\nSteps:\n1. Time out performed.\n2. LMA inserted.\n3. Airway inspection: Normal anatomy.\n4. EBUS scope advanced.\n5. TBNA performed on Station 7, 11Rs, and 4R (3 stations total).\n6. 5 passes per node.\n7. Tolerated well.\nPlan: Wait for path.",
            5: "patient here for ebus testicular cancer history we used propofol and an lma... airway looked clear no masses. switched to the ebus scope and found nodes at 7 4r and 11rs. did 5 passes at each spot with the 22 gauge needle sent it all to cytology. no bleeding really just a little bit of suctioning needed. procedure went fine patient woke up ok.",
            6: "Mediastinal adenopathy in setting of testicular cancer s/p chemotherapy. Propofol infusion via anesthesia assistance. Q190 video bronchoscope introduced. Laryngeal mask airway in good position. Vocal cords normal. Trachea normal. Carina sharp. Video scope removed. UC180F convex probe EBUS bronchoscope introduced. Ultrasound identified enlarged station 7, 4R and 11Rs lymph nodes. Station 7 was 16.6 mm, 4R 5.7mm, 11Rs 8.9mm. Sampling by transbronchial needle aspiration performed on all three stations using 22 gauge needle. 5 needle passes at each. Samples sent for cytology. No complications.",
            7: "[Indication]\nMediastinal adenopathy, hx testicular cancer.\n[Anesthesia]\nPropofol/MAC, LMA.\n[Description]\nDiagnostic bronchoscopy: Normal anatomy. EBUS: Stations 7, 4R, and 11Rs identified and sampled. 5 passes each with 22G needle. 3 stations total sampled.\n[Plan]\nPathology review.",
            8: "The patient was brought to the bronchoscopy suite for evaluation of mediastinal adenopathy given his history of testicular cancer. After induction of anesthesia, we inspected the airway and found no endobronchial anomalies. Switching to the linear EBUS scope, we localized three specific lymph nodes: station 7, station 4R, and station 11Rs. We performed transbronchial needle aspiration on each of these three stations, completing five passes per node to ensure sufficient material. There were no immediate complications.",
            9: "Indications: Mediastinal adenopathy.\nAction: The airway was surveyed with a video bronchoscope. The EBUS scope was deployed. Ultrasound imaged enlarged nodes at stations 7, 4R, and 11Rs. These targets were aspirated using a 22G needle. Five passes were executed at each lymph node station. Specimens were dispatched for cytology. The airway was cleared of secretions."
        },
        1: { # Note 1: Unclear Etiology, CPT 31652 (1 station: 4R)
            1: "Indication: Mediastinal adenopathy.\nFindings: Extrinsic compression of distal trachea/R mainstem (85%).\nProcedure: EBUS-TBNA of 4R mass (4.8cm).\n- 6 passes, 19G needle.\n- ROSE: Suspicious for lymphoma.\n- Blood suctioned. No complications.",
            2: "CLINICAL SUMMARY: Patient presents with mediastinal adenopathy of indeterminate etiology. \nOPERATIVE REPORT: General anesthesia was utilized. Airway inspection revealed significant extrinsic compression of the right mainstem bronchus. The convex probe EBUS was advanced to the level of the paratracheal stations. A large mass at station 4R, measuring 4.8 cm, was visualized. Transbronchial needle aspiration was performed utilizing a 19-gauge needle for 6 passes. Preliminary onsite analysis suggests a lymphoproliferative disorder.",
            3: "Service: Bronchoscopy with EBUS sampling (31652).\nAnatomy Evaluated: Right Paratracheal (4R) station.\nFindings: 4.8 cm mass causing airway compression.\nIntervention: EBUS-guided needle aspiration (6 passes) of the single 4R station.\nPathology: Samples sent for Flow Cytometry and Cytology due to suspicion of lymphoma (ROSE positive).\nCoding: Single station sampled supports 31652.",
            4: "Resident Note:\nProcedure: EBUS-TBNA.\n- Patient intubated/LMA.\n- White light bronchoscopy showed compression of R mainstem.\n- EBUS scope used to find 4R mass.\n- Sampled 4R with 19G needle x 6 passes.\n- ROSE reads 'suspicious for lymphoma'.\n- Flow cytometry sent.\n- Stable post-op.",
            5: "ebus for mediastinal mass unclear cause... airway was kinda tight on the right side like 85 percent compressed. put the ultrasound scope down and saw a huge node at 4r measuring almost 5cm. stuck it 6 times with the big 19g needle. path guy in the room said looks like lymphoma so we sent flow. suctioned some blood out and finished up.",
            6: "Mediastinal adenopathy of unclear etiology. General Anesthesia. LMA placed. Q190 video bronchoscope advanced. Distal right trachea partially compressed. Right mainstem 85% compressed. No endobronchial lesions. UC180F EBUS scope introduced. 4R paratracheal mass identified (4.8 cm). TBNA performed with 19 gauge needle. 6 passes total. ROSE suspicious for lymphoma. Samples sent for cytology and flow. Video scope re-inserted to suction blood. Procedure completed.",
            7: "[Indication]\nMediastinal mass, rule out lymphoma.\n[Anesthesia]\nGeneral.\n[Description]\nRight mainstem compression observed. EBUS localization of station 4R mass (4.8cm). 6 needle passes performed (19G). ROSE: Suspicious for lymphoma. Flow cytometry collected.\n[Plan]\nOncology referral pending final path.",
            8: "The patient underwent EBUS bronchoscopy to investigate a large mediastinal mass. Upon entering the airway, we noted significant compression of the right mainstem bronchus. We utilized the EBUS scope to target the 4R paratracheal station, which corresponded to the radiographic mass. We performed six needle aspirations using a 19-gauge needle. The rapid on-site evaluation was concerning for lymphoma, so samples were prioritized for flow cytometry. The patient tolerated the procedure well.",
            9: "Indications: Mediastinal adenopathy.\nAction: The airway was inspected, revealing compression. The EBUS scope was inserted. The 4R station was visualized and aspirated 6 times. Rapid evaluation indicated lymphoma. Specimens were submitted for flow cytometry. The airway was suctioned."
        },
        2: { # Note 2: Brain Mets/Sarcoid vs Infxn, CPT 31653 (4 stations: 11L, 7, 4L, 2R)
            1: "Indication: Mediastinal adenopathy, ?brain mets.\nProcedure: EBUS-TBNA x 4 stations.\n- Sampled: 11L, 7, 4L, 2R.\n- 5 passes each (7 passes at 2R).\n- ROSE: Granulomas found.\n- 2R sent for cx.\nComplications: Oozing RLL/LLL, stopped w/ epi.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nFINDINGS: Symmetric hilar and mediastinal adenopathy was appreciated. Systematic sampling was undertaken at stations 11L, 7, 4L, and 2R. A minimum of five passes were performed at each station. \nPATHOLOGY: Rapid on-site evaluation demonstrated granulomatous inflammation across multiple stations (11L, 4L, 2R). Station 2R was additionally cultured for acid-fast bacilli and fungi.\nHEMOSTASIS: Post-biopsy oozing in the lower lobes required instillation of dilute epinephrine.",
            3: "CPT Code: 31653 (EBUS sampling 3+ stations).\nStations Sampled (4 total):\n1. Station 11L\n2. Station 7 (Subcarinal)\n3. Station 4L\n4. Station 2R\nTechnique: 22G needle used. 5-7 passes per station.\nDiagnostic: ROSE showed granulomas. Cultures sent from 2R.\nComplication: Minor bleeding treated with 1:10000 epinephrine.",
            4: "Procedure Note\nProcedure: EBUS\nStations: 11L, 7, 4L, 2R.\nSteps:\n1. GA/LMA.\n2. Airway exam: Dynamic tracheal obstruction.\n3. EBUS sampling of 4 stations.\n4. ROSE: Granulomas.\n5. Sent cytology + cx (2R).\n6. Bleeding noted LLL/RLL, treated with epi wash.\nPlan: Rule out Sarcoid vs TB.",
            5: "patient with brain mets concern and adenopathy. did the bronch under GA. trachea looked a bit floppy. scanned and sampled 4 spots... 11L 7 4L and 2R. got granulomas on the slides. sent cultures from 2R just in case. had some bleeding at the bottom so we squirted some epi and it stopped. 31653 for the 4 stations.",
            6: "Mediastinal Adenopathy with concern for brain mets. General Anesthesia. Partial dynamic obstruction of trachea. Bronchial mucosa normal. Enlarged nodes seen in stations 11L, 7, 4L, 2R. TBNA performed with 22 gauge needle. 5 passes per station (7 at 2R). ROSE yielded granulomas. Samples sent for cytology and culture (2R). Slow oozing in bilateral lower lobes treated with 2ml lidocaine/epinephrine. Bleeding stopped.",
            7: "[Indication]\nMediastinal adenopathy, r/o mets vs sarcoid.\n[Anesthesia]\nGeneral.\n[Description]\nDynamic airway collapse noted. EBUS-TBNA of 4 stations: 11L, 7, 4L, 2R. ROSE confirmed granulomas. Cultures sent.\n[Complications]\nMinor lower lobe bleeding, resolved with epinephrine.\n[Plan]\nMonitor for infection/sarcoidosis.",
            8: "We performed a complete EBUS staging procedure for this patient with mediastinal adenopathy. We sequentially sampled four distinct lymph node stations: 11L, 7, 4L, and 2R. The pathologist present in the suite identified granulomas in the samples. Consequently, we sent additional material from station 2R for infectious workup (AFB/Fungal). Following the biopsy, we noted some mucosal oozing in the lower lobes which was successfully managed with topical epinephrine.",
            9: "Indications: Adenopathy.\nAction: EBUS visualization utilized. Nodes at 11L, 7, 4L, and 2R were targeted. Aspiration was performed (5-7 passes). ROSE indicated granulomas. Tissue submitted for culture and cytology. Epinephrine was instilled for hemostasis."
        },
        3: { # Note 3: Mediastinal Adenopathy, CPT 31652 (1 station: 2L)
            1: "Indication: Mediastinal adenopathy.\nProcedure: EBUS 2L.\n- 19G and 22G needles used.\n- 8 passes total.\n- ROSE: Lymphocytes (benign).\nNo complications.",
            2: "OPERATIVE REPORT: The patient presented for evaluation of mediastinal lymphadenopathy. Following induction of general anesthesia, the airway was secured. EBUS examination localized a suspicious lymph node at station 2L, distal to the cricoid cartilage. Extensive sampling was performed using both 19-gauge and 22-gauge needles for a total of eight passes. On-site evaluation revealed a lymphoid population without definitive malignancy.",
            3: "Service: Bronchoscopy with EBUS sampling (31652).\nStation: Left Upper Paratracheal (2L).\nCount: 1 station sampled.\nTechnique: 8 total passes utilizing both 19G and 22G needles.\nFindings: Abundant lymphocytes on ROSE.\nDisposition: Outpatient.",
            4: "Resident Note\nIndication: Adenopathy.\nProcedure: EBUS-TBNA.\n1. LMA placed.\n2. Normal airway exam.\n3. Found 2L node.\n4. Biopsied x 8 passes (19G + 22G).\n5. Path said lymphocytes.\n6. Procedure done.",
            5: "doing ebus for adenopathy today... patient asleep lma in. looked down airway clean. found a node at 2L just past the cricoid. stuck it 8 times with different needles 19 and 22 gauge. path saw lymphocytes sent for flow. no bleeding all good.",
            6: "Mediastinal adenopathy. General Anesthesia. LMA in good position. Normal airway exam. UC180F EBUS scope inserted. Suspicious 2L lymph node identified. TBNA performed with 19G and 22G needles. 8 passes total. ROSE: Abundant lymphocytes. Samples sent for flow and cytology. No active bleeding.",
            7: "[Indication]\nMediastinal adenopathy.\n[Anesthesia]\nGeneral.\n[Description]\nStation 2L identified via EBUS. 8 needle passes performed (19G/22G). ROSE: Lymphocytes. Flow cytometry sent.\n[Plan]\nDischarge to home.",
            8: "The patient underwent EBUS bronchoscopy for a suspicious mediastinal node. We identified the target at station 2L. To ensure adequate sampling for flow cytometry, we performed a total of eight passes using both 19-gauge and 22-gauge needles. The preliminary read showed abundant lymphocytes. The procedure was concluded without complication.",
            9: "Indications: Adenopathy.\nAction: The 2L node was located via ultrasound. Aspiration was executed 8 times using varying needle gauges. ROSE verified lymphocytes. Material was dispatched for flow cytometry."
        },
        4: { # Note 4: Mediastinal Adenopathy, CPT 31652 (1 station: 11R composed of 11Ri+11Rs)
            1: "Indication: Mediastinal adenopathy.\nProcedure: EBUS 11R.\n- Sampled 11Ri (6 passes) and 11Rs (5 passes).\n- ROSE: Benign lymphocytes.\n- Flow cytometry sent.\nNo complications.",
            2: "PROCEDURE: The patient underwent EBUS-TBNA for evaluation of right hilar adenopathy. The right interlobar station (11R) was interrogated. Separate samples were obtained from the inferior (11Ri) and superior (11Rs) aspects of the station. A total of 11 passes were completed. Rapid interpretation was negative for malignancy. Tissue was submitted for flow cytometry.",
            3: "Code: 31652 (1-2 stations).\nTarget: Station 11R (Right Interlobar).\nDetails: Sampling performed at two distinct sites within the station (11Ri and 11Rs).\nPasses: 6 at 11Ri, 5 at 11Rs.\nJustification: Despite two sampling sites, location maps to a single IASLC station (11R).",
            4: "Procedure: EBUS\nTarget: 11R.\nSteps:\n1. GA/LMA.\n2. Normal airway.\n3. Found 11Ri -> 6 biopsies.\n4. Found 11Rs -> 5 biopsies.\n5. ROSE neg for cancer.\n6. Sent for flow.",
            5: "ebus for hilar nodes... patient under general. airway looked fine. found the 11R station sampled the inferior part 11ri 6 times then the superior part 11rs 5 times. path said just lymphocytes no cancer. sent for flow cytometry. patient stable.",
            6: "Mediastinal adenopathy. General Anesthesia. LMA used. Airway exam normal. EBUS scope introduced. 11Ri lymph node identified and sampled (6 passes). 11Rs lymph node identified and sampled (5 passes). ROSE negative for malignancy. Samples sent for flow and routine cytology. No bleeding.",
            7: "[Indication]\nMediastinal adenopathy.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA of station 11R. Sampled inferior (11Ri) and superior (11Rs) aspects. 11 total passes. ROSE negative. Flow sent.\n[Plan]\nOutpatient follow-up.",
            8: "We proceeded with EBUS to evaluate the right hilar region. We identified adenopathy at station 11R. To be thorough, we sampled both the inferior aspect (11Ri) and the superior aspect (11Rs) of this station, performing a total of 11 needle passes. The on-site pathologist saw lymphocytes but no malignancy. We submitted the samples for flow cytometry to rule out lymphoma.",
            9: "Indications: Adenopathy.\nAction: Station 11R was targeted. Aspiration was performed at 11Ri and 11Rs. ROSE indicated absence of malignancy. Specimens were submitted for flow cytometry."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns a list of mock data to create variation in patient identity.
    Indices correspond to the notes in the source file.
    """
    return [
        # Note 0: Testicular Cancer (Age ~35-45 usually, but synthetic can vary)
        {"idx": 0, "orig_name": "John Doe", "orig_age": 38, 
         "names": ["Liam Smith", "Noah Johnson", "Oliver Williams", "Elijah Brown", "James Jones", "William Garcia", "Benjamin Miller", "Lucas Davis", "Henry Rodriguez"]},
        
        # Note 1: Unclear Adenopathy
        {"idx": 1, "orig_name": "Jane Smith", "orig_age": 55, 
         "names": ["Emma Martinez", "Ava Hernandez", "Charlotte Lopez", "Amelia Gonzalez", "Mia Wilson", "Harper Anderson", "Evelyn Thomas", "Abigail Taylor", "Emily Moore"]},
        
        # Note 2: Brain Mets/Sarcoid
        {"idx": 2, "orig_name": "Robert Johnson", "orig_age": 62, 
         "names": ["Alexander Jackson", "Daniel Martin", "Michael Lee", "Sebastian Perez", "Ethan Thompson", "Matthew White", "Joseph Harris", "Samuel Sanchez", "David Clark"]},
        
        # Note 3: 2L Adenopathy
        {"idx": 3, "orig_name": "Mary Williams", "orig_age": 49, 
         "names": ["Sofia Ramirez", "Avery Lewis", "Ella Robinson", "Madison Walker", "Scarlett Young", "Victoria Allen", "Luna King", "Grace Wright", "Chloe Scott"]},
        
        # Note 4: 11R Adenopathy
        {"idx": 4, "orig_name": "Patricia Brown", "orig_age": 58, 
         "names": ["Penelope Torres", "Layla Nguyen", "Riley Hill", "Zoey Flores", "Nora Green", "Lily Adams", "Eleanor Nelson", "Hannah Baker", "Lillian Hall"]},
    ]

def main():
    # Load original data from source file
    input_path = Path(SOURCE_FILE)
    if not input_path.exists():
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
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
            print(f"Warning: No mock data for note index {idx}. Skipping.")
            continue
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Iterate through the 9 styles
        for style_num in range(1, 10):
            
            # Deep copy the original note structure
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 5 years)
            new_age = orig_age + random.randint(-5, 5)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned for this style
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation if it exists
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: No variation text found for Note {idx}, Style {style_num}. Keeping original.")

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Insert generated name into providers (or create patient field if strictly needed, 
                # but instruction implies mostly metadata updates. We will add a synthetic patient name field).
                note_entry["registry_entry"]["patient_name"] = new_name
                
                # Update MRN to be unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    if base_mrn == "UNKNOWN":
                        base_mrn = f"IP2026_{idx}"
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
                
                # Update age if exists, or add it
                # Note: The source file registry_entry structure varies slightly from the previous example.
                # It has patient_demographics -> age_years in some, or just assumed in context.
                # We will check common paths.
                if "patient_demographics" in note_entry["registry_entry"] and note_entry["registry_entry"]["patient_demographics"] is not None:
                     note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                else:
                    # If structure is flat or missing, inject for consistency
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

    # Output to JSON
    output_filename = output_dir / OUTPUT_FILENAME
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()