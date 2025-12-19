import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_016.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    # Note 0: LMS Obstruction, Rigid, APC/Cryo/Forceps, EBUS (St 7), Balloon.
    # Note 1: RMS Obstruction, Rigid, APC/Forceps.
    # Note 2: RMS Obstruction, Rigid, Dilation, Intra-op Death (CPR, Chest Tubes).
    # Note 3: LMS/Lingula Obstruction, Rigid, Cryo/APC, BAL.
    # Note 4: Extrinsic Compression, Rigid, Y-Stent.

    variations = {
        0: {
            1: "Procedure: Rigid bronchoscopy, EBUS, tumor debulking.\n- 12mm rigid scope inserted.\n- EBUS TBNA performed on station 7 (6 passes).\n- Left mainstem tumor debulked using APC, electrocautery, and cryotherapy.\n- CRE balloon dilation (8-9-10mm) of left mainstem.\n- Purulent secretions drained.\n- Hemostasis achieved.",
            2: "OPERATIVE REPORT: The patient presented with complex malignant airway obstruction involving the distal trachea and left mainstem bronchus. Under general anesthesia, rigid bronchoscopy was utilized to establish a secure airway. Convex probe endobronchial ultrasound (EBUS) was employed to sample a subcarinal lymph node (Station 7). Subsequently, multimodal tumor ablation was performed within the left mainstem bronchus utilizing argon plasma coagulation, electrocautery, and cryotherapy. Following mechanical debulking, balloon dilation was performed to optimize luminal patency. The procedure yielded significant relief of the obstruction.",
            3: "Procedures Performed for Billing:\n1. Rigid Bronchoscopy with Tumor Destruction (31641): Extensive debulking of left mainstem carcinoma performed using APC, cryotherapy, and electrocautery to relieve high-grade stenosis.\n2. EBUS-TBNA (31652): Ultrasound-guided needle aspiration of subcarinal lymph node (Station 7).\n3. Balloon Dilation: Performed in LMS to facilitate scope passage (bundled).\nNote: General anesthesia used.",
            4: "Procedure Note\nAttending: Dr. [Name]\nResident: Dr. [Name]\nIndication: LMS obstruction.\nSteps:\n1. Induced GA, intubated, then switched to 12mm rigid scope.\n2. EBUS scope passed; bx station 7.\n3. Used APC/Cryo/Forceps to open LMS.\n4. Suctioned pus.\n5. Dilated LMS with balloon.\n6. Hemostasis with APC.\nPlan: Rad Onc consult.",
            5: "rigid bronch performed for left main mass... general anesthesia used... tube out rigid in. used ebus first for station 7 biopsy. then went to work on the left mainstem used apc and cryo and forceps to get the tumor out... drained some pus... balloon dilated the airway to open it up more... stopped bleeding with apc... patient tol well extubated.",
            6: "The patient was brought to the OR and placed under general anesthesia. A 12mm rigid bronchoscope was inserted. EBUS-TBNA was performed on station 7. Attention was turned to the left mainstem obstruction. Tumor was debulked using APC, electrocautery, and cryotherapy. A balloon dilation was performed to 10mm. Purulent secretions were cleared. Hemostasis was achieved and the scope was removed.",
            7: "[Indication]\nLeft mainstem obstruction, lung mass.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy initiated. EBUS-TBNA of station 7 performed. Multimodal debulking of LMS tumor using APC, cryotherapy, and forceps. Balloon dilation of LMS performed. Airways cleared of pus and blood.\n[Plan]\nPathology pending. Radiation oncology consult.",
            8: "The patient was taken to the operating room and general anesthesia was induced. We proceeded with rigid bronchoscopy to manage the left mainstem obstruction. First, we utilized EBUS to sample the subcarinal station. Following this, we aggressively debulked the tumor in the left mainstem using a combination of APC, cryotherapy, and rigid forceps. Once the airway was patent, we further dilated it with a CRE balloon. We cleared purulent secretions from the distal lung and confirmed hemostasis before concluding the case.",
            9: "Rigid bronchoscopy was utilized for left mainstem blockage. We sampled station 7 via EBUS. We then ablated and extracted the tumor in the left mainstem using APC, cryotherapy, and forceps. The airway was expanded with a balloon. Septic fluid was evacuated. The bleeding was arrested with APC."
        },
        1: {
            1: "Dx: RMS obstruction.\nProc: Rigid bronch, debulking.\n- Rigid scope to trachea.\n- RMS 95% occluded.\n- APC and forceps used to debulk/recanalize RMS and Bronchus Intermedius.\n- 85% patency achieved.\n- No bleeding.",
            2: "OPERATIVE NARRATIVE: A 12mm rigid bronchoscope was introduced under general anesthesia to address a high-grade right mainstem obstruction. Inspection revealed 95% occlusion extending into the bronchus intermedius. We employed argon plasma coagulation (APC) to devitalize the intraluminal tumor burden, followed by mechanical debridement using flexible forceps. This approach allowed for successful recanalization of the right bronchial tree.",
            3: "Code Selection: 31641 (Bronchoscopy with destruction of tumor).\nSite: Right Mainstem/Bronchus Intermedius.\nTechnique: Thermal ablation via Argon Plasma Coagulation (APC) followed by mechanical removal of charred tissue. This constitutes relief of stenosis by any method.",
            4: "Procedure: Rigid Bronchoscopy with Debulking.\nIndication: R mainstem obstruction.\nSteps:\n1. Rigid scope inserted.\n2. Tumor seen in RMS (95%).\n3. Biopsies taken.\n4. APC used to burn tumor.\n5. Forceps used to clean up debris.\n6. Good result (85% open).\nComplications: None.",
            5: "patient with right lung mass obstructing airway... did rigid bronch today general anesthesia... airway looked clear on left... right side blocked almost total... used apc to burn it back and forceps to grab the pieces... opened it up pretty good about 85 percent... no big bleeding sent to pacu.",
            6: "Under general anesthesia, a 12mm rigid bronchoscope was inserted. The right mainstem was found to be 95% obstructed by tumor. Endobronchial biopsies were obtained. The tumor was debulked using argon plasma coagulation and mechanical forceps removal. Recanalization of approximately 85% was achieved in the right mainstem and bronchus intermedius. The procedure was terminated without complication.",
            7: "[Indication]\nRight mainstem obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy performed. 95% occlusion of RMS identified. APC and forceps debulking performed. Recanalization to 85% achieved. Biopsies taken.\n[Plan]\nDischarge to home. Urgent Rad Onc consult.",
            8: "We performed a rigid bronchoscopy to treat a malignant obstruction in the right mainstem bronchus. Upon inspection, the airway was nearly completely blocked. We utilized argon plasma coagulation to cauterize the tumor tissue and then removed the debris with forceps. We repeated this process until the airway was significantly more open. We confirmed there was no active bleeding and removed the scope.",
            9: "Rigid bronchoscopy was performed for right mainstem occlusion. We ablated the lesion with APC and extracted the fragments with forceps. We successfully reopened the airway to 85% patency. Biopsies were harvested."
        },
        2: {
            1: "Indication: Malignant airway obstruction.\nProcedure: Rigid bronch, debulking, attempted stent.\nComplication: Intra-op cardiac arrest.\n- Tumor debulked in RMS (APC/Forceps).\n- Balloon dilation performed.\n- Patient developed PEA/Asystole.\n- CPR x 30 min. Bilateral chest tubes placed. TPA given.\n- Patient expired.",
            2: "OPERATIVE SUMMARY: The patient underwent rigid bronchoscopy for management of right mainstem obstruction. Tumor debulking was performed utilizing APC and balloon dilation. Intraoperatively, the patient suffered sudden cardiovascular collapse progressing to PEA and asystole. ACLS protocols were initiated immediately, including cardiopulmonary resuscitation, administration of epinephrine, and placement of bilateral tube thoracostomies to rule out tension pneumothorax. Despite prolonged resuscitative efforts (>30 minutes), return of spontaneous circulation was not achieved, and the patient was pronounced deceased.",
            3: "Billing Summary for Interrupted Procedure/Death:\n- 31641: Rigid bronchoscopy with tumor destruction (APC/Forceps) completed prior to arrest.\n- 31630 (Bundled): Balloon dilation performed.\n- 92950: CPR performed (30 min).\n- 32551-LT: Left chest tube placement.\n- 32551-RT: Right chest tube placement.\nDiagnosis: Malignant obstruction, Cardiac Arrest (I46.9).",
            4: "Resident Note\nProcedure: Rigid Bronchoscopy -> Code Blue.\nEvents:\n1. Rigid scope inserted, tumor debulked in RMS with APC.\n2. Balloon dilation performed.\n3. Patient lost pulse (PEA).\n4. Started CPR.\n5. Placed L chest tube (no air).\n6. Placed R chest tube (no air).\n7. TPA given.\n8. Called death after 30 min code.",
            5: "procedure started normal rigid bronch to open right airway... used apc and balloon to open it up... then bp dropped and heart stopped... code blue called... did cpr for long time... put chest tubes in both sides just in case of pneumo... gave epi and tpa... heart never started again... patient died in or.",
            6: "A 12mm rigid bronchoscope was inserted under general anesthesia. The right mainstem tumor was debulked using APC and forceps, followed by balloon dilation. During the procedure, the patient developed PEA arrest. CPR was initiated. Bilateral chest tubes were placed to rule out pneumothorax. TPA was administered. Resuscitation efforts were unsuccessful after 30 minutes, and the patient was pronounced dead.",
            7: "[Indication]\nRight mainstem obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy with APC debulking and balloon dilation of RMS. Intraoperative cardiac arrest (PEA) occurred. CPR initiated. Bilateral chest tubes placed. TPA administered. \n[Outcome]\nPatient expired in OR.",
            8: "We began the procedure with rigid bronchoscopy to treat the right mainstem tumor. We successfully debulked the lesion using APC and dilated the airway. Unfortunately, the patient went into cardiac arrest during the procedure. We immediately started CPR and placed chest tubes on both sides to ensure there was no collapsed lung contributing to the arrest. Despite aggressive resuscitation for over 30 minutes, the patient did not survive.",
            9: "Rigid bronchoscopy was undertaken for tumor ablation. We employed APC and balloon dilation. The patient suffered cardiac arrest. We executed CPR and inserted bilateral thoracostomy tubes. The patient succumbed to the event."
        },
        3: {
            1: "Procedure: Rigid bronch, cryoextraction, BAL.\nFindings: LLL/Lingula obstruction.\nAction:\n- Cryoextraction of tumor piece-meal.\n- APC for hemostasis.\n- Mini-BAL of Lingula.\nResult: Partial recanalization (LMS 15% obstructed). LLL remains obstructed.",
            2: "OPERATIVE REPORT: The patient underwent therapeutic rigid bronchoscopy for a fungating tumor obstructing the distal left mainstem, LLL, and lingula. Cryoextraction was utilized to remove significant tumor burden. Argon plasma coagulation was applied for hemostasis. A bronchoalveolar lavage (BAL) was performed in the lingula to assess for infection. Due to distal tumor extension, complete recanalization of the LLL was not feasible, though the left mainstem patency was significantly improved.",
            3: "Billing Codes Supported:\n- 31641: Destruction/Relief of stenosis via Cryoextraction and APC in Left Mainstem.\n- 31624-59: BAL performed in Lingula (separate site from primary tumor destruction target) for purulent secretions.\n- Rigid bronchoscopy method used (included in 31641).",
            4: "Procedure: Rigid Bronch with Debulking\nIndication: L mainstem mass.\nSteps:\n1. LMA -> Rigid scope.\n2. Saw tumor blocking LLL and Lingula.\n3. Used cryoprobe to pull out tumor chunks.\n4. Cleaned up with APC.\n5. Did a wash (BAL) in the lingula.\n6. LLL still blocked but LMS better.\nComplications: Mild bleeding.",
            5: "rigid bronch for left lung mass... tumor was blocking lll and lingula... used cryo to pull big pieces out and apc to stop bleeding... did a bal in the lingula cause there was pus... couldn't get the lll open all the way... woke patient up and sent to recovery.",
            6: "Under general anesthesia, a rigid bronchoscope was inserted. A tumor in the distal left mainstem obstructing the LLL and lingula was identified. Cryoextraction was used for debulking. APC was used for hemostasis. A BAL was performed in the lingula. The LLL remained obstructed, but the left mainstem patency improved to 85%.",
            7: "[Indication]\nLeft mainstem/LLL obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Cryoextraction of tumor in distal LMS. APC for hemostasis. BAL of lingula. LLL remains obstructed.\n[Plan]\nDischarge home. Monitor for regrowth.",
            8: "We performed a rigid bronchoscopy to address a tumor blocking the left lower lobe and lingula. We used a cryoprobe to freeze and extract pieces of the tumor, clearing the main airway. We also used APC to stop any oozing. We washed the lingula (BAL) to check for infection. While we couldn't fully open the lower lobe, the main airway is much better.",
            9: "Rigid bronchoscopy was employed. We utilized cryoextraction to debulk the lesion in the left mainstem. APC was applied for coagulation. We lavaged the lingula. The left mainstem was recanalized, though the lower lobe remained occluded."
        },
        4: {
            1: "Indication: Severe extrinsic tracheal compression.\nProcedure: Rigid bronch, Y-stent.\nFindings: 60% tracheal obstruction, 50% LMB obstruction.\nAction: Placed 14x10x10 Silicone Y-Stent (customized).\nResult: Airways stabilized. O2 sats improved.\nPlan: ICU, humidified O2.",
            2: "OPERATIVE NARRATIVE: The patient presented with respiratory failure due to severe extrinsic compression of the mid-trachea and left mainstem bronchus. Rigid bronchoscopy was performed to secure the airway. A silicone Y-stent was customized (14x10x10mm) and deployed to span the carina, effectively stenting the trachea and both mainstems. Post-deployment inspection confirmed relief of the extrinsic compression and stabilization of the airway architecture.",
            3: "Coding Justification: 31631 (Placement of tracheal stent). A silicone Y-stent was placed covering the trachea and carina to treat extrinsic compression. This code captures the placement of the stent extending into the main bronchi as it is a single carinal device.",
            4: "Procedure: Y-Stent Placement\nIndication: Tracheal compression.\nSteps:\n1. Rigid scope passed beyond obstruction.\n2. Measured airways.\n3. Cut Y-stent to size.\n4. Deployed stent using rigid scope.\n5. Fixed position with forceps.\n6. Switched to LMA, patient sats improved.\n7. Stent looks good.",
            5: "rigid bronch for tracheal compression... patient couldn't breathe good... put in the rigid scope and verified the blockage... cut a silicone y stent and put it in... had some trouble ventilating for a minute but got the stent in and placed lma... sats came up... stent looks perfect opening up the trachea.",
            6: "A 14mm rigid bronchoscope was inserted under general anesthesia. Severe extrinsic compression of the trachea and left mainstem was noted. A customized silicone Y-stent was deployed. The limbs were positioned into the right and left mainstems. Ventilation improved immediately. Flexible inspection confirmed patency of the stent limbs.",
            7: "[Indication]\nExtrinsic tracheal compression.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Measurement of airway dimensions. Deployment of customized Silicone Y-stent (14x10x10). Verification of patent airway and improved ventilation.\n[Plan]\nICU admission. Humidified air.",
            8: "Due to severe compression of the trachea from the outside, we performed a rigid bronchoscopy to place a stent. We measured the airways and cut a silicone Y-stent to fit. We deployed the stent to hold the trachea and main airways open. The patient's breathing improved immediately after placement. We confirmed the stent was in a good position before finishing.",
            9: "Rigid bronchoscopy was utilized for extrinsic airway stenosis. We deployed a customized silicone Y-stent. The prosthesis successfully scaffolded the trachea and main bronchi. Ventilation parameters normalized post-deployment."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks based on the input JSON structure to ensure continuity
    return [
        {"idx": 0, "orig_name": "Logan Pierce", "orig_age": 67, "names": ["John Vance", "Arthur Higgins", "Robert Kinsley", "William O'Connor", "James P. Miller", "Edward Stone", "Richard Davis", "Thomas Clark", "Gary Wright"]},
        {"idx": 1, "orig_name": "Patricia Morales", "orig_age": 63, "names": ["Sarah Jenkins", "Linda Carter", "Nancy Hughes", "Karen Smith", "Barbara Lopez", "Mary Ann Davidson", "Susan White", "Margaret Lewis", "Betty King"]},
        {"idx": 2, "orig_name": "Ethan Cole", "orig_age": 70, "names": ["Michael Foster", "Robert G. Turner", "David Myers", "Joseph Anderson", "Frank Mitchell", "Paul Reynolds", "George Baker", "Kenneth Roberts", "Steven Phillips"]},
        {"idx": 3, "orig_name": "Renee Thompson", "orig_age": 59, "names": ["Marie Hall", "Patricia Campbell", "Elizabeth Allen", "Jennifer Young", "Linda Hernandez", "Barbara King", "Dorothy Wright", "Helen Scott", "Carol Green"]},
        {"idx": 4, "orig_name": "Marcus Hill", "orig_age": 65, "names": ["James Carter", "William Edwards", "Thomas Harris", "Charles Martin", "Donald Thompson", "Mark Garcia", "Paul Martinez", "George Robinson", "Kenneth Clark"]},
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
        orig_age = record['orig_age'] if record['orig_age'] else 65 # Default if null
        
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
                note_entry["note_text"] = f"VARIATION_MISSING_FOR_NOTE_{idx}_STYLE_{style_num}"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_demographics" in note_entry["registry_entry"] and note_entry["registry_entry"]["patient_demographics"]:
                     note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                # Some entries might have age at top level or different structure, check generic keys
                if "patient_age" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["patient_age"] = new_age

                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    current_mrn = note_entry["registry_entry"]["patient_mrn"]
                    if current_mrn == "Unknown" or current_mrn == "UNKNOWN":
                         current_mrn = f"IP_BRONCH_{idx}"
                    note_entry["registry_entry"]["patient_mrn"] = f"{current_mrn}_syn_{style_num}"
            
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
    output_filename = output_dir / "synthetic_bronch_notes_part_016.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()