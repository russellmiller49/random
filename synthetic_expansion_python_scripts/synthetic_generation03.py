import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_003.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations for bronch_notes_part_003.json
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Note 0: Stent Removal (31635)
            1: "Procedure: Rigid Bronchoscopy with Stent Removal.\n- Rigid scope inserted.\n- Tracheal stent removed with forceps.\n- Bilateral mainstem stents removed.\n- APC used for hemostasis at granulation sites.\n- Jet ventilation utilized.\n- Patient stable, transferred to PACU.",
            2: "OPERATIVE REPORT: The patient was brought to the endoscopy suite for elective removal of airway stents. Following induction of general anesthesia, a 13mm rigid tracheoscope was introduced. Inspection via flexible bronchoscope confirmed patency of the Ultraflex stents. Utilizing rigid alligator forceps, the tracheal prosthesis was grasped proximally and explanted. Subsequently, the right and left mainstem stents were removed in sequential fashion. Examination of the mucosa revealed granulation tissue and localized hemorrhage, which was effectively cauterized using Argon Plasma Coagulation. Total rigid bronchoscopy time was 45 minutes.",
            3: "CPT Justification: 31635 (Bronchoscopy with removal of foreign body).\nTechnique: Rigid bronchoscopy required for retrieval of three (3) Ultraflex SEMS stents located in the trachea, RMS, and LMS. Hemostasis achieved via APC (bundled). The procedure involved complex manipulation of the stents using alligator forceps through the rigid barrel under visualization.",
            4: "Procedure Note\nResident: Dr. Smith\nAttending: Dr. Jones\n1. Time out performed.\n2. General anesthesia induced.\n3. Rigid scope (13mm) inserted.\n4. Flexible scope passed; stents visualized.\n5. Tracheal stent removed using forceps technique.\n6. Mainstem stents removed similarly.\n7. Bleeding controlled with APC.\n8. Scope removed. Patient stable.",
            5: "we did the bronchoscopy today patient was asleep rigid scope went in 13 mm size looked at the stents they were open took the tracheal one out first with the alligator forceps then did the main stems left and right... there was some bleeding some granulation tissue so we used the APC to burn it a bit... had to switch ventilation modes because of the malacia but got it done discharged to pacu follow up with ct surgery thanks",
            6: "The procedure was performed in the bronchoscopy suite. Once the patient was sedated and paralyzed a 13 mm non-ventilating rigid tracheoscope was inserted through the mouth into the sublottic glottic space. A flexible T190 Olympus bronchoscope was inserted through the tracheoscope into the trachea and airway inspection was performed. The patient’s uncovered Ultraflex SEM stents in the trachea and bilateral main stems were widely patent with minimal intraluminal mucous. The flexible bronchoscope was removed and the rigid optic was reinserted alongside rigid alligator forceps. The forceps were used to grasp the proximal limb of the tracheal stent and were rotated repeatedly while withdrawing the stent into the rigid bronchoscope. The stent was subsequently removed without difficulty. Once his stent was removed the 12mm ventilating rigid bronchoscope was inserted through the tracheoscope and advanced to the distal trachea at which point the left and right main stem stents were also removed in a similar fashion, flexible bronchoscope was reinserted for repeat airway inspection. There was moderate inflammation with slight granulation issue in the mucosa surrounding the previous stents with slow oozing of blood most predominantly in the distal trachea and main stem bronchi. There was also marked residual malacia which required conversion from open jet ventilation to closed conventional ventilation to main stem airway patency. The areas of active oozing were then treated with APC painting of the mucosa until sufficient hemostasis was achieved. At this point the rigid bronchoscope was removed and the procedure was completed.",
            7: "[Indication]\nCompleted stent trial requiring removal.\n[Anesthesia]\nGeneral Anesthesia with paralysis.\n[Description]\nRigid bronchoscopy (13mm) performed. Identification of Ultraflex stents in trachea and bilateral mainstems. Stents successfully removed using rigid alligator forceps. APC applied to granulation tissue for hemostasis.\n[Plan]\nDischarge to home. CT Surgery follow-up for tracheoplasty.",
            8: "The patient arrived for the scheduled stent removal and was placed under general anesthesia. We began by inserting a 13mm rigid tracheoscope. A flexible inspection revealed the stents were patent. Using alligator forceps, we carefully extracted the tracheal stent first, followed by the left and right mainstem stents. Post-removal inspection showed granulation tissue and oozing, which we treated with Argon Plasma Coagulation. Due to malacia, we managed ventilation carefully throughout. The patient tolerated the procedure well.",
            9: "INDICATIONS: Stent trial concluded.\nSedation: General.\nPROCEDURE: A rigid tracheoscope was deployed. The Ultraflex SEMS were visualized. Using forceps, the tracheal prosthesis was extracted. The bronchial stents were subsequently retrieved. Hemorrhage was managed with APC application. The airway was inspected for residual malacia."
        },
        1: { # Note 1: EBUS 31652 (11L, 4R)
            1: "Procedure: EBUS-TBNA\n- Airway inspected: Tracheomalacia noted.\n- Stations sampled: 11L (5.4mm), 4R (5.5mm).\n- Needle: 22G Olympus.\n- Results: 11L non-diagnostic, 4R benign lymphocytes.\n- No complications.",
            2: "OPERATIVE NARRATIVE: The patient was intubated and a Q190 video bronchoscope was advanced. Anatomic inspection revealed tracheomalacia but no endobronchial lesions. The linear EBUS scope was utilized for mediastinal staging. Systematic sonographic evaluation identified targetable lymph nodes at stations 11L and 4R. Transbronchial needle aspiration was performed under real-time ultrasound guidance using a 22-gauge needle. Rapid On-Site Evaluation (ROSE) was utilized for specimen triage. The procedure concluded without adverse events.",
            3: "Code Selection: 31652 (EBUS sampling 1-2 stations).\nTargets: Station 11L and Station 4R.\nTechnique: Real-time ultrasound guidance used to visualize nodes. Needle aspiration performed. \nMedical Necessity: Staging of presumed malignancy.",
            4: "Procedure Note\nDiagnosis: Lung cancer staging.\n1. ETT placed.\n2. White light bronchoscopy: Tracheomalacia seen. Normal mucosa.\n3. EBUS scope introduced.\n4. Identified nodes 11L and 4R.\n5. TBNA performed on 11L then 4R.\n6. ROSE: 11L non-diagnostic, 4R lymphocytes.\n7. Suctioned airway, scope removed.",
            5: "patient here for staging we put them to sleep general anesthesia... used the Q190 scope first saw some tracheomalacia but otherwise normal. switched to the ebus scope found nodes at 11L and 4R sampled them with the 22 gauge needle... ROSE said 11L was nothing but 4R had lymphocytes so we stopped there sent everything to cytology no bleeding really 5cc blood loss okay thanks",
            6: "Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the ET tube into the tracheobronchial tree. Tracheomalacia was noted in the trachea. The carina was sharp. The right-sided airway anatomy was normal. The left sided airway anatomy was normal. No evidence of endobronchial disease was seen to at least the first sub-segments. A systematic hilar and mediastinal lymph node survey was carried out. Sampling criteria (5mm short axis diameter) were met in station 11L (5.4mm) and 4R (5.5mm) lymph nodes. Sampling by transbronchial needle aspiration was performed beginning with the 11L Lymph node, followed by 4R lymph nodes using an Olympus Visioshot EBUSTBNA 22 gauge needle. ROSE showed non-diagnostic tissue in the low probability 11L lymph node and benign lymphocytes in the 4Rs. All samples were sent for routine cytology. The Q190 video bronchoscope was then re-inserted and after suctioning blood and secretions there was no evidence of active bleeding and the bronchoscope was subsequently removed.",
            7: "[Indication]\nStaging of presumed lung cancer.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nTracheomalacia observed. EBUS-TBNA performed at stations 11L and 4R using 22G needle. ROSE provided preliminary results. No endobronchial lesions seen.\n[Plan]\nAwait final pathology.",
            8: "We performed a bronchoscopy for staging purposes under general anesthesia. Upon entering with the Q190 scope, we noted some tracheomalacia but otherwise normal anatomy. Switching to the EBUS scope, we identified and sampled lymph nodes at stations 11L and 4R using a 22 gauge needle. The on-site pathologist reviewed the slides, finding lymphocytes in the 4R node. We finished the procedure with no complications and sent the patient to recovery.",
            9: "Indication: Staging presumed malignancy.\nAction: The bronchoscope was navigated into the airway. Tracheomalacia was observed. EBUS interrogation located nodes at 11L and 4R. These were aspirated using a 22G needle. Specimens were submitted for cytology. The airway was cleared of secretions."
        },
        2: { # Note 2: EBUS 31653 (11L, 7, 11Ri)
            1: "Procedure: EBUS-TBNA (3+ stations).\n- Findings: RLL obstruction (75%) by tumor.\n- EBUS Nodes: 11L, 7, 11Ri (mass).\n- Action: Biopsied 11L, 7, and 11Ri mass.\n- ROSE: 11Ri positive for Squamous Cell.\n- Samples sent for PD-L1/NGS.",
            2: "OPERATIVE REPORT: The patient underwent diagnostic bronchoscopy for staging. Inspection revealed significant pathology in the right lower lobe with 75% occlusion due to submucosal infiltration. EBUS examination was performed targeting stations 11L, 7, and a large 11Ri mass continuous with the primary tumor. Transbronchial needle aspiration was executed at all three sites. Rapid on-site evaluation confirmed malignancy (favors squamous cell) at the 11Ri station. Adequate tissue was obtained for molecular profiling.",
            3: "Code: 31653 (EBUS sampling 3 or more stations).\nStations Sampled: 11L, 7, and 11Ri.\nDetails: \n- 11L (5 passes)\n- 7 (5 passes)\n- 11Ri (9 passes, mass 28mm)\nNote: 11Rs visualized but not sampled due to 11Ri positivity. 31653 criteria met.",
            4: "Procedure Note\n1. LMA placed.\n2. Scope: T190. RLL obstruction seen (tumor).\n3. EBUS Scope: UC180F.\n4. Nodes identified: 11L, 7, 11Rs, 11Ri.\n5. Biopsied: 11L, 7, and 11Ri (mass).\n6. 11Ri positive for SCC on ROSE.\n7. Complications: None.",
            5: "did a bronch on this patient with the LMA... looked down and the RLL is blocked about 75 percent looks like tumor... switched to the EBUS scope. We sampled station 11L and station 7 and then the mass at 11Ri. Did a lot of passes on the mass to get enough for the genetic testing. ROSE said it looks like squamous cell. Patient did fine minimal bleeding sent to recovery.",
            6: "The T190 video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The right mainstem, right upper lobe and proximal 80% of the bronchus intermedius was normal caliber without endobronchial lesions or mucosal irregularities. Mild extrinsic compression was present in the distal 20% of the bronchus intermedius. There was submucosal infiltration in the right middle lobe take off however it was widely patent. In the right lower lobe bronchus (just past the middle lobe take off) there was approximately 75% airway obstruction from a combination of submucosal infiltration and extrinsic tumor compression. The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced. Sampling by transbronchial needle aspiration was performed with the Olympus EBUSTBNA 22 gauge needle beginning with the 11L Lymph node, followed by the 7 lymph node and finally the 11Ri/mass. A total of 5 biopsies were performed in the 11L and 7 lymph node stations. A total of 9 needle passes were performed on the 11Ri/mass.",
            7: "[Indication]\nStaging of lung cancer.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nRLL 75% obstructed by tumor. EBUS-TBNA performed on stations 11L, 7, and 11Ri. ROSE confirmed malignancy at 11Ri. Samples sent for molecular testing.\n[Plan]\nOncology referral pending final pathology.",
            8: "We performed a bronchoscopy to stage the patient's lung cancer. Visual inspection showed a significant obstruction in the right lower lobe bronchus. We then used the EBUS scope to examine the lymph nodes. We found and sampled nodes at stations 11L, 7, and the 11Ri mass. The rapid on-site evaluation suggested squamous cell carcinoma in the 11Ri node. We took extra samples for genetic testing and concluded the procedure safely.",
            9: "Indication: Malignancy staging.\nAction: The airway was surveyed. Obstruction was noted in the RLL. EBUS was utilized to visualize nodes at 11L, 7, and 11Ri. These targets were aspirated. The 11Ri mass yielded malignant cells on ROSE. Specimens were forwarded for analysis."
        },
        3: { # Note 3: EBUS 31652 + TBNA 31629 + Nav 31627 (4R, 11Rs + Peripheral RUL)
            1: "Procedure: Navigational Bronchoscopy & EBUS.\n- Navigation to RUL lesion. TBNA performed (31629/31627).\n- EBUS Staging: Stations 4R, 11Rs (31652).\n- Findings: Epiglottic plaque. Normal airway otherwise.\n- Plan: ENT consult for plaque.",
            2: "OPERATIVE SUMMARY: The patient was anesthetized and an LMA placed. Diagnostic bronchoscopy revealed a brown plaque on the epiglottis. Electromagnetic navigation was utilized to guide a transbronchial needle aspiration of a peripheral RUL lesion. Subsequently, EBUS-TBNA was performed for mediastinal staging, sampling stations 4R and 11Rs. ROSE confirmed adequate lymphocytes. The patient tolerated the procedure well.",
            3: "Coding: \n- 31652: EBUS sampling of 2 stations (4R, 11Rs).\n- 31629-59: Transbronchial needle aspiration of separate peripheral RUL lesion.\n- 31627: Computer-assisted navigation used for RUL target.\nNote: Plaque on epiglottis noted but not biopsied.",
            4: "Procedure Note\n1. General anesthesia.\n2. White light: Epiglottic plaque seen.\n3. Navigation: Guided TBNA of RUL nodule.\n4. EBUS: Sampled stations 4R and 11Rs.\n5. ROSE: Adequate.\n6. Plan: ENT referral, await path.",
            5: "ok so we did the bronch today... saw this weird brown spot on the epiglottis gonna have ENT look at that. anyway we used the navigation to get to that spot in the RUL and biopsied it with the needle. then we did the EBUS sampled the 4R and 11Rs nodes. everything went fine no bleeding sent samples to cytology.",
            6: "Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the mouth. A brown plaque of unclear significance was seen on the epiglottis. Electromagnetic navigation was utilized to localize the peripheral RUL lesion, and TBNA was performed. The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced. Sampling criteria were met in station 4R and station 11Rs lymph nodes. Sampling by transbronchial needle aspiration was performed beginning with the 4r Lymph node, followed by 11Rs using an Olympus EBUSTBNA 22 gauge needle.",
            7: "[Indication]\nLung cancer staging.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nEpiglottic plaque noted. Navigation-guided TBNA of RUL lesion performed. EBUS-TBNA performed at stations 4R and 11Rs. \n[Plan]\nENT consult. CT guided biopsy backup if needed.",
            8: "The patient was brought in for staging. We noticed a plaque on the epiglottis which we will refer to ENT. We used the navigation system to find the lesion in the right upper lobe and sampled it with a needle. Then we switched to the EBUS scope and sampled lymph nodes at 4R and 11Rs. All samples looked adequate on the rapid exam. We finished up without any issues.",
            9: "Indication: Staging of carcinoma.\nAction: Airway inspection revealed an epiglottic lesion. Navigation assisted in localizing the RUL target for aspiration. EBUS facilitated sampling of nodes 4R and 11Rs. Specimens were collected and the scope was withdrawn."
        },
        4: { # Note 4: EBUS 31653 + Nav 31627 + TBNA 31629 (11L, 7, 4R + RUL Nav)
            1: "Procedure: Navigational Bronch & EBUS\n- Navigated to RUL lesion. Confirmed w/ Radial EBUS.\n- Biopsies: Needle, brush, forceps (RUL).\n- EBUS Staging: 11L, 7, 4R sampled.\n- Outcome: Stable, minimal bleeding.",
            2: "OPERATIVE REPORT: Following induction, a T190 bronchoscope was inserted. SuperDimension navigation was employed to catheterize the RUL lesion, confirmed by concentric radial EBUS view. Transbronchial biopsy, brush, and needle aspiration were performed under fluoroscopy. The EBUS scope was then utilized to systematically sample mediastinal stations 11L, 7, and 4R. All stations yielded diagnostic material.",
            3: "Code Justification:\n- 31653: EBUS sampling of 3 stations (11L, 7, 4R).\n- 31629-59: Peripheral TBNA of RUL lesion.\n- 31627: Navigation guidance.\n- (Note: 31623/31628 bundled or not primary; 31629 is index peripheral code).",
            4: "Procedure Note\n1. General Anesthesia/LMA.\n2. Navigated to RUL lesion with SuperDimension.\n3. Confirmed with REBUS.\n4. Took biopsies (needle, brush, forceps).\n5. EBUS scope passed.\n6. Sampled nodes 11L, 7, 4R.\n7. Complications: None.",
            5: "we did the nav bronch first... went to the RUL lesion used the superdimension stuff radial ebus confirmed we were in it. took a bunch of samples with the needle and brush and forceps. then switched to EBUS and hit the 11L 7 and 4R nodes. 5 passes each. patient did great no issues.",
            6: "The super-dimension navigational catheter was inserted through the T190 therapeutic bronchoscope and advanced into the airway. Using navigational map we attempted to advance the 180 degree edge catheter into the proximity of the lesion within the right upper lobe. Confirmation of placement once at the point of interest with radial ultrasound showed a concentric view within the lesion. Biopsies were then performed with a variety of instruments to include peripheral needle, brush, and forceps, under fluoroscopic visualization. After adequate samples were obtained, the video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced. Sampling by transbronchial needle aspiration was performed with the Olympus EBUSTBNA 22 gauge needle beginning with the 11L Lymph node, followed by the 7 lymph node and finally the 4R lymph node.",
            7: "[Indication]\nStaging lung cancer.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nNavigational bronchoscopy to RUL lesion with REBUS confirmation. Biopsies taken (TBNA/Brush/Bx). EBUS-TBNA performed at 11L, 7, and 4R.\n[Plan]\nDischarge to home.",
            8: "We started with the navigational bronchoscopy to target the lesion in the right upper lobe. Once we were there, we used radial ultrasound to make sure we were in the right spot and took several biopsies. Then we switched scopes to do the EBUS staging. We sampled lymph nodes at stations 11L, 7, and 4R. Everything went smoothly and there was no bleeding.",
            9: "Indication: Diagnosis/Staging.\nAction: Navigation was employed to reach the RUL opacity. Radial EBUS verified position. The lesion was sampled via needle and forceps. Subsequently, EBUS interrogation allowed for aspiration of nodes 11L, 7, and 4R. The procedure was concluded."
        }
    }
    return variations

def get_base_data_mocks():
    # Mock data to replace "UNKNOWN" names/ages from source
    return [
        {"idx": 0, "orig_name": "Unknown", "orig_age": 55, "names": ["John Doe", "James Smith", "Robert Brown", "Michael Miller", "William Davis", "David Garcia", "Richard Rodriguez", "Charles Wilson", "Joseph Martinez"]},
        {"idx": 1, "orig_name": "Unknown", "orig_age": 65, "names": ["Mary Johnson", "Patricia Williams", "Linda Jones", "Barbara Hernandez", "Elizabeth Lopez", "Jennifer Gonzalez", "Maria Perez", "Susan Sanchez", "Margaret Clark"]},
        {"idx": 2, "orig_name": "Unknown", "orig_age": 70, "names": ["Thomas Anderson", "Christopher Taylor", "Daniel Thomas", "Paul Moore", "Mark Jackson", "Donald Martin", "George Lee", "Kenneth Thompson", "Steven White"]},
        {"idx": 3, "orig_name": "Unknown", "orig_age": 60, "names": ["Dorothy Harris", "Lisa Young", "Nancy King", "Karen Wright", "Betty Scott", "Helen Green", "Sandra Baker", "Donna Adams", "Carol Nelson"]},
        {"idx": 4, "orig_name": "Unknown", "orig_age": 62, "names": ["Edward Hill", "Brian Ramirez", "Ronald Campbell", "Anthony Mitchell", "Kevin Roberts", "Jason Carter", "Matthew Phillips", "Gary Evans", "Timothy Turner"]}
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
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen with full dict)
                note_entry["note_text"] = f"VARIATION MISSING FOR IDX {idx} STYLE {style_num}"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update MRN
                if "patient_mrn" in note_entry["registry_entry"]:
                    # Create a unique MRN based on style
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    if base_mrn == "UNKNOWN": base_mrn = "MRN"
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
                
                # Update Procedure Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update demographics if structure exists
                if "patient_demographics" in note_entry["registry_entry"]:
                    if note_entry["registry_entry"]["patient_demographics"] is None:
                        note_entry["registry_entry"]["patient_demographics"] = {}
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                    # Determine gender loosely based on name (simple heuristic for mock data)
                    gender = "Male" if idx % 2 == 0 else "Female" # Alternating mock pattern
                    note_entry["registry_entry"]["patient_demographics"]["gender"] = gender

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
    output_filename = output_dir / "synthetic_bronch_notes_part_003.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()