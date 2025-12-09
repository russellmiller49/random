import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_056_part1.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations.
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    # Styles:
    # 1. Terse Surgeon
    # 2. Academic Attending
    # 3. Billing Coder
    # 4. Trainee/Resident
    # 5. Sloppy Dictation
    # 6. Header-less
    # 7. Templated
    # 8. Narrative Flow
    # 9. Synonym Swapper

    variations = {
        0: { # Sarah Green (Right, Bx, Talc)
            1: "Pre-op: Susp lung CA. Right side.\nProc: Med Thoracoscopy.\n- Entry 6th ICS.\n- Findings: Thickened parietal pleura, nodules.\n- Action: Bx x6 parietal. Bx diaphragmatic. Talc poudrage (4g).\n- Chest tube placed.\nPlan: Admit. Suction.",
            2: "OPERATIVE REPORT: The patient presented for right-sided medical thoracoscopy to stage suspected bronchogenic carcinoma. Under moderate sedation, the pleural space was accessed. Inspection revealed diffuse thickening of the parietal pleura with distinct nodularity. Extensive biopsies were harvested for histopathological and immunohistochemical analysis. Given the macroscopic appearance of malignancy, pleurodesis was undertaken utilizing sterile talc insufflation to prevent recurrent effusion. The lung was re-expanded under direct vision.",
            3: "CPT Justification:\n32609 (Thoracoscopy with biopsy of pleura): Performed via semi-rigid pleuroscope. Multiple specimens obtained from parietal and diaphragmatic surfaces.\n32650 (Thoracoscopy with pleurodesis): performed during the same session via insufflation of talc agent.\nMedical Necessity: Staging of malignancy and prevention of recurrent effusion.",
            4: "Resident Procedure Note\nPatient: [Name]\nStaff: Dr. Williams\nSteps:\n1. Local/Mod sedation.\n2. Trocar placed 6th ICS Right.\n3. Scope inserted.\n4. Identified nodules on parietal pleura.\n5. Biopsies taken (x6).\n6. Talc poudrage performed for pleurodesis.\n7. Chest tube placed.\nPlan: Admit to floor.",
            5: "procedure note for mrs green right side thoracoscopy looking for cancer sedation was fine went in 6th rib space saw a lot of nodules and thick pleura took about 6 biopsies sent to path also put in talc for the fluid lung came up good chest tube is in to suction no air leak admit her thanks",
            6: "Right medical thoracoscopy with pleural biopsy and talc pleurodesis was performed on the patient. Under moderate sedation and local anesthesia, a single port was established in the 6th intercostal space at the mid-axillary line. The semi-rigid pleuroscope was introduced. Inspection revealed thickened parietal pleura with distinct nodules. Six biopsies were taken from the parietal pleura and additional samples from the diaphragm. Talc poudrage was performed. A chest tube was placed and the wound closed.",
            7: "[Indication]\nStaging for lung cancer, right pleural effusion.\n[Anesthesia]\nModerate Sedation.\n[Description]\nRight chest accessed. Thickened parietal pleura with nodules visualized. Multiple biopsies obtained (32609). Talc poudrage performed (32650). Fluid evacuated.\n[Plan]\nAdmit. Chest tube management.",
            8: "We performed a right-sided medical thoracoscopy today. After achieving adequate sedation, we entered the chest wall at the 6th intercostal space. Upon inspection, we noted significant thickening of the parietal pleura along with several nodules. We proceeded to take multiple biopsies from these areas. Given the high likelihood of malignancy, we also performed a talc pleurodesis to manage the effusion. The procedure concluded with the placement of a chest tube.",
            9: "Operation: Right-sided pleuroscopy with tissue sampling and chemical sclerosis.\nObserved: Hypertrophic parietal pleura with nodes.\nAction: Harvested 6 specimens from parietal wall. Sampled diaphragmatic surface. Insufflated talc for fusion. Evacuated hydrothorax.\nResult: Hemostasis secured. Tube anchored."
        },
        1: { # George Martinez (Right, Diagnostic)
            1: "Indication: Mesothelioma susp.\nSide: Right.\nProc: Diagnostic Thoracoscopy.\nFindings: Diffuse nodularity.\nAction: Fluid drained. Inspection only (32601). No bx recorded in this specific note section (refer to path if taken separately).\nResult: Lung expanded. Chest tube placed.",
            2: "PROCEDURE: Right Medical Thoracoscopy (Diagnostic).\nFINDINGS: Upon entry into the right pleural cavity, diffuse nodularity was observed affecting the parietal, visceral, and diaphragmatic surfaces, highly suspicious for mesothelioma. The pleural fluid was completely evacuated. As this was a diagnostic inspection, the primary focus was visualization and fluid removal. A chest tube was placed under direct vision to ensure lung re-expansion.",
            3: "Code: 32601 (Thoracoscopy, diagnostic).\nRationale: Procedure involved visualization of the pleural space via pleuroscope. Fluid was drained. Diffuse nodularity noted. No biopsies or pleurodesis explicitly coded in this specific encounter record (Diagnostic only).\nSite: Right hemithorax.",
            4: "Procedure: Diagnostic Pleuroscopy\nSide: Right\nSteps:\n1. 6th ICS entry.\n2. Visualization of pleura.\n3. Found diffuse nodules.\n4. Drained all fluid.\n5. Placed chest tube.\nNote: Sent fluid for cytology.",
            5: "mr martinez needed a look inside the right chest for mesothelioma moderate sedation used went in with the scope saw nodules everywhere very diffuse drained the fluid out lung looks ok expanded fine put a tube in water seal path results pending",
            6: "Diagnostic medical thoracoscopy, right side. The patient was placed under moderate sedation. The pleural space was accessed at the 6th intercostal space. Visualization revealed diffuse pleural nodularity consistent with the indication of suspected mesothelioma. All fluid was evacuated. A chest tube was inserted and connected to a water seal. The lung appeared expanded.",
            7: "[Indication]\nSuspected mesothelioma, Right side.\n[Anesthesia]\nModerate.\n[Description]\nDiagnostic thoracoscopy performed. Diffuse nodularity visualized on parietal and visceral surfaces. Fluid evacuated. Chest tube placed.\n[Plan]\nMonitor output. Await path.",
            8: "Mr. Martinez underwent a diagnostic thoracoscopy on the right side today. We successfully entered the pleural space and visualized diffuse nodularity across the pleural surfaces. We drained the remaining fluid to help with his breathing and visualization. A chest tube was placed to ensure the lung remains expanded. He will be admitted to the floor.",
            9: "Procedure: Right-sided diagnostic pleuroscopy.\nIndication: Presumed mesothelioma.\nObservations: Widespread pleural nodes.\nAction: The cavity was inspected. Hydrothorax was emptied. A drainage catheter was sited.\nOutcome: Lung inflation confirmed."
        },
        2: { # Jacob Martinez (Right, Bx, Talc)
            1: "Indication: Pleural nodules.\nSide: Right.\nFindings: Inflammatory changes, no gross tumor.\nProc: Bx parietal pleura x6. Talc poudrage performed.\nResult: Fluid out. Chest tube in.\nPlan: Admit.",
            2: "OPERATIVE SUMMARY: The patient underwent a right medical thoracoscopy to investigate radiographic pleural nodularity. Intraoperative inspection revealed inflammatory changes; however, distinct nodularity was less prominent than expected. Multiple biopsies were obtained from the parietal and diaphragmatic pleura to rule out occult malignancy or specific infectious etiology. Despite the inflammatory appearance, talc poudrage was instilled to achieve pleurodesis. The patient tolerated the procedure well.",
            3: "Billing: 32609 (Bx), 32650 (Talc).\nLocation: Right.\nTechnique: Flexible trocar entry. Visual inspection showed inflammation. Biopsies taken to establish diagnosis. Talc applied for effusion control.\nDocumentation supports both biopsy and chemical pleurodesis.",
            4: "Resident Note\nPt: Jacob M.\nProc: Right Thoracoscopy w/ Bx and Talc.\nSteps:\n1. Entry 6th ICS.\n2. Saw inflammation (no obvious masses).\n3. Took 6 biopsies.\n4. Sprayed Talc.\n5. Chest tube placed.\nComplications: None.",
            5: "jacob martinez 74 male right side thoracoscopy we went in looking for nodules but it mostly looked like inflammation took biopsies anyway just to be sure and did the talc procedure too drained the fluid chest tube is in no air leak thanks",
            6: "Right medical thoracoscopy with biopsy and pleurodesis. Under moderate sedation, the right pleural space was accessed. Findings included inflammatory changes without distinct gross nodularity. Biopsies were taken from the parietal and diaphragmatic pleura (6 specimens). Talc poudrage was performed to prevent fluid recurrence. A chest tube was placed.",
            7: "[Indication]\nPleural nodularity, Right.\n[Anesthesia]\nModerate.\n[Description]\nInflammatory changes visualized. Biopsies taken (x6). Talc poudrage performed. Fluid drained.\n[Plan]\nFloor admission. Suction.",
            8: "We took Mr. Martinez to the suite for a right-sided thoracoscopy. Upon looking inside, the pleura appeared inflamed but we didn't see large nodules. We took six biopsy samples to be safe. We also decided to perform a talc pleurodesis while we were there to stop the fluid from coming back. A chest tube was placed at the end.",
            9: "Operation: Right pleuroscopy with tissue sampling and talc insufflation.\nFindings: Pleuritis without obvious neoplasm.\nAction: Harvested 6 parietal samples. Deposited talc agent. Evacuated effusion.\nOutcome: Hemostasis achieved. Tube secured."
        },
        3: { # Amanda Ramirez (Left, Diagnostic)
            1: "Dx: Recurrent Left effusion.\nProc: Dx Thoracoscopy.\nFindings: Multiple malignant-appearing nodules.\nAction: Fluid drained. Inspection complete. Tube placed.\nPlan: Admit.",
            2: "PROCEDURE NOTE: Diagnostic Medical Thoracoscopy, Left.\nFINDINGS: Access was established in the left hemithorax. Direct visualization demonstrated multiple nodules along the pleural surface with a macroscopic appearance highly suggestive of malignancy. The procedure was limited to diagnostic inspection and fluid evacuation. A chest tube was inserted to maintain lung expansion pending pathology results.",
            3: "Service: 32601 (Diagnostic Thoracoscopy).\nSide: Left.\nDetails: Visualization of parietal, visceral, and diaphragmatic pleura. Findings of malignant-appearing nodules. Fluid evacuation included.\nNote: No biopsy code (32609) claimed in this text block.",
            4: "Procedure: Left Diagnostic Thoracoscopy\nIndication: Unknown effusion.\nSteps:\n1. Scope in 6th ICS.\n2. Saw multiple nodules (look malignant).\n3. Drained fluid.\n4. Chest tube placed.\nPlan: Wait for path/cytology.",
            5: "amanda ramirez left side effusion we did a thoracoscopy to see whats going on found a bunch of nodules look like cancer drained the fluid put a tube in water seal admit to floor",
            6: "Diagnostic medical thoracoscopy, left side. Indication was recurrent pleural effusion. Under moderate sedation, the scope was inserted. Findings included multiple pleural nodules that appeared malignant. Fluid was evacuated under direct visualization. A chest tube was placed and the patient was admitted.",
            7: "[Indication]\nRecurrent effusion, Left.\n[Anesthesia]\nModerate.\n[Description]\nDiagnostic scope. Malignant-appearing nodules visualized. Fluid drained. Chest tube placed.\n[Plan]\nOncology consult pending results.",
            8: "Ms. Ramirez underwent a diagnostic thoracoscopy on her left side today. We entered the chest and unfortunately visualized multiple nodules that appeared malignant. We drained all the fluid to help her breathing and placed a chest tube. We will await further results.",
            9: "Procedure: Left-sided diagnostic pleuroscopy.\nFindings: Suspicious nodes on pleura.\nAction: Examined cavity. Emptied hydrothorax. Sited drainage catheter.\nStatus: Lung expanded."
        },
        4: { # Timothy Scott (Left, Diagnostic)
            1: "Indication: Left pleural mass.\nProc: Dx Thoracoscopy.\nFindings: Mass lesion diaphragmatic pleura.\nAction: Fluid evacuated. Tube placed.\nResult: No air leak.",
            2: "OPERATIVE REPORT: Left Diagnostic Thoracoscopy.\nOBSERVATIONS: The left pleural space was interrogated. A distinct mass lesion was identified arising from the diaphragmatic pleura. The remainder of the examination involved visualization of the parietal and visceral surfaces and evacuation of pleural fluid. A thoracostomy tube was placed for postoperative management.",
            3: "CPT: 32601.\nLocation: Left.\nFindings: Mass on diaphragm.\nTechnique: Single port entry. Diagnostic inspection only. No biopsy described in this specific note text. Fluid drainage included.",
            4: "Procedure: Left Thoracoscopy (Diagnostic)\nPt: Timothy S.\nSteps:\n1. Entry 6th ICS.\n2. Found mass on diaphragm.\n3. Suctioned fluid.\n4. Placed chest tube.\nPlan: Floor.",
            5: "procedure note for mr scott left side thoracoscopy saw a mass on the diaphragm pretty obvious drained the fluid put the tube in water seal patient tolerated well",
            6: "Diagnostic medical thoracoscopy, left side. Patient presented with pleural nodularity. Procedure revealed a mass lesion on the diaphragmatic pleura. The parietal and visceral pleura were otherwise visualized. Fluid was evacuated and a chest tube was placed.",
            7: "[Indication]\nLeft pleural nodularity.\n[Anesthesia]\nModerate.\n[Description]\nDiagnostic exam. Mass lesion found on diaphragm. Fluid drained. Chest tube in.\n[Plan]\nAdmit.",
            8: "We performed a diagnostic thoracoscopy on Mr. Scott's left side. Upon inspection, we found a mass lesion located on the diaphragm. We ensured all fluid was drained and placed a chest tube to keep the lung expanded. The patient is stable.",
            9: "Operation: Left diagnostic pleuroscopy.\nFindings: Diaphragmatic neoplasm/mass.\nAction: Surveyed pleura. Evacuated effusion. Anchored tube.\nOutcome: Lung re-expanded."
        },
        5: { # Edward Lopez (Right, Diagnostic)
            1: "Indication: Exudative effusion.\nSide: Right.\nProc: Dx Thoracoscopy.\nFindings: Pleural plaques.\nAction: Fluid drained. Tube placed.\nPlan: Admit.",
            2: "PROCEDURE NOTE: Right Medical Thoracoscopy.\nFINDINGS: The right pleural cavity was inspected. The parietal and diaphragmatic pleura exhibited distinct pleural plaques, consistent with asbestos exposure markers or similar pathology. No gross masses were seen. Fluid was evacuated to dryness. A chest tube was placed.",
            3: "Code: 32601.\nSide: Right.\nFindings: Pleural plaques.\nService: Visualization and drainage only. No biopsy performed in this session.",
            4: "Procedure: Right Diagnostic Thoracoscopy\nSteps:\n1. Port placed.\n2. Saw pleural plaques.\n3. Drained fluid.\n4. Chest tube in.\nPlan: Monitor output.",
            5: "edward lopez right side thoracoscopy checking the effusion saw some pleural plaques drained the fluid put in a chest tube no air leak stable",
            6: "Diagnostic medical thoracoscopy, right side. Indication: Cytology-negative effusion. Findings: Pleural plaques visualized on parietal/diaphragmatic surfaces. Fluid evacuated. Chest tube placed. No air leak.",
            7: "[Indication]\nEffusion, Right.\n[Anesthesia]\nModerate.\n[Description]\nPleural plaques identified. Diagnostic inspection only. Fluid drained. Chest tube placed.\n[Plan]\nAdmit.",
            8: "Mr. Lopez underwent a right-sided diagnostic thoracoscopy. We identified pleural plaques along the chest wall. We drained the fluid and placed a chest tube. He recovered well from the sedation.",
            9: "Procedure: Right diagnostic pleuroscopy.\nFindings: Hyaline plaques.\nAction: Inspected surfaces. Emptied hydrothorax. Sited drain.\nResult: Lung expanded."
        },
        6: { # Karen White (Right, Bx)
            1: "Indication: Persistent effusion.\nSide: Right.\nFindings: Fibrinous adhesions, trapped lung.\nProc: Bx parietal pleura x8. Fluid drained. Tube placed.\nPlan: Admit.",
            2: "OPERATIVE SUMMARY: Right Medical Thoracoscopy with Biopsy.\nFINDINGS: Significant fibrinous adhesions were noted, contributing to a trapped lung physiology. Extensive biopsies (8 specimens) were taken from the parietal pleura to determine the etiology. Mechanical lysis was limited; the primary goal was tissue acquisition. Fluid was evacuated and a chest tube placed.",
            3: "CPT: 32609 (Biopsy).\nSide: Right.\nPathology: Fibrinous adhesions/Trapped lung.\nTechnique: 8 biopsies obtained. Fluid drainage included. No extensive lysis coded (32609 covers biopsy).",
            4: "Procedure: Right Thoracoscopy w/ Bx\nPt: Karen W.\nSteps:\n1. Entry 6th ICS.\n2. Found adhesions/trapped lung.\n3. 8 biopsies taken.\n4. Drained fluid.\n5. Chest tube placed.\nPlan: Suction.",
            5: "karen white right side thoracoscopy persistent fluid saw a lot of adhesions and the lung looked trapped took 8 biopsies to figure it out drained the fluid put a tube in admit to floor",
            6: "Right medical thoracoscopy with pleural biopsy. Indication: Persistent effusion. Findings: Fibrinous adhesions and trapped lung. Eight biopsies were obtained from the parietal pleura. Fluid was evacuated and a chest tube was placed.",
            7: "[Indication]\nEffusion, trapped lung, Right.\n[Anesthesia]\nModerate.\n[Description]\nAdhesions visualized. 8 biopsies taken (32609). Fluid drained. Chest tube placed.\n[Plan]\nAdmit.",
            8: "We performed a right-sided thoracoscopy on Ms. White. We found significant adhesions and what appears to be a trapped lung. We took eight biopsy samples from the chest wall. We drained the fluid and placed a chest tube for monitoring.",
            9: "Operation: Right pleuroscopy with tissue sampling.\nFindings: Fibrinous bands, entrapped lung.\nAction: Harvested 8 specimens. Evacuated effusion. Anchored drain.\nOutcome: Hemostasis."
        },
        7: { # Nicholas Green (Left, Diagnostic)
            1: "Indication: Effusion.\nSide: Left.\nProc: Dx Thoracoscopy.\nFindings: Fibrinous adhesions, trapped lung.\nAction: Fluid drained. Tube placed.\nPlan: Admit.",
            2: "PROCEDURE: Left Diagnostic Medical Thoracoscopy.\nFINDINGS: Upon accessing the left pleural space, we encountered fibrinous adhesions and evidence of trapped lung. As this was a diagnostic intervention, the pleura was inspected, fluid was drained, and a chest tube was placed to facilitate drainage and monitoring.",
            3: "Code: 32601.\nSide: Left.\nFindings: Adhesions, trapped lung.\nAction: Visualization and drainage. No biopsy or lysis coded.",
            4: "Procedure: Left Diagnostic Thoracoscopy\nSteps:\n1. Port placed.\n2. Saw adhesions/trapped lung.\n3. Drained fluid.\n4. Chest tube in.\nPlan: Monitor.",
            5: "nicholas green left side thoracoscopy saw adhesions and trapped lung drained the fluid put in a chest tube stable",
            6: "Diagnostic medical thoracoscopy, left side. Indication: Exudative effusion. Findings: Fibrinous adhesions with trapped lung. Fluid evacuated. Chest tube placed.",
            7: "[Indication]\nEffusion, Left.\n[Anesthesia]\nModerate.\n[Description]\nAdhesions and trapped lung visualized. Fluid drained. Chest tube placed.\n[Plan]\nAdmit.",
            8: "Mr. Green underwent a left-sided diagnostic thoracoscopy. We saw fibrinous adhesions and a trapped lung. We drained the fluid and placed a chest tube. He is stable.",
            9: "Procedure: Left diagnostic pleuroscopy.\nFindings: Fibrinous bands, entrapped lung.\nAction: Inspected cavity. Emptied hydrothorax. Sited drain.\nOutcome: Lung expanded."
        },
        8: { # Donald Flores (Left, Bx)
            1: "Indication: Susp TB.\nSide: Left.\nProc: Bx parietal pleura x9.\nFindings: Inflammatory changes.\nAction: Fluid drained. Tube placed.\nPlan: Admit.",
            2: "OPERATIVE REPORT: Left Medical Thoracoscopy with Biopsy.\nINDICATION: Suspected tuberculous pleuritis.\nFINDINGS: The pleural surfaces showed diffuse inflammatory changes without distinct nodularity. Nine biopsies were obtained from the parietal pleura to optimize diagnostic yield for granulomatous disease. Fluid was evacuated and a chest tube inserted.",
            3: "CPT: 32609.\nSide: Left.\nReason: TB suspect.\nTechnique: 9 biopsies taken from parietal pleura. Fluid drained. Tube placed.",
            4: "Procedure: Left Thoracoscopy w/ Bx\nPt: Donald F.\nSteps:\n1. Entry 6th ICS.\n2. Saw inflammation.\n3. Took 9 biopsies.\n4. Drained fluid.\n5. Chest tube in.\nPlan: Path.",
            5: "donald flores left side thoracoscopy thinking tb saw inflammation took 9 biopsies just to be sure drained the fluid chest tube in no air leak",
            6: "Left medical thoracoscopy with pleural biopsy. Indication: Suspected TB. Findings: Inflammatory changes. Nine biopsies obtained. Fluid evacuated. Chest tube placed.",
            7: "[Indication]\nSuspected TB, Left.\n[Anesthesia]\nModerate.\n[Description]\nInflammation visualized. 9 biopsies taken. Fluid drained. Chest tube placed.\n[Plan]\nAdmit.",
            8: "We performed a left-sided thoracoscopy on Mr. Flores to investigate for TB. The pleura looked inflamed. We took nine biopsy samples to send to the lab. We drained the fluid and placed a chest tube.",
            9: "Operation: Left pleuroscopy with tissue sampling.\nFindings: Pleuritis.\nAction: Harvested 9 specimens. Evacuated effusion. Anchored drain.\nOutcome: Hemostasis."
        },
        9: { # Melissa Wilson (Right, Diagnostic)
            1: "Indication: Susp malignancy.\nSide: Right.\nProc: Dx Thoracoscopy.\nFindings: Normal pleura.\nAction: Fluid drained. Tube placed.\nPlan: Admit.",
            2: "PROCEDURE: Right Diagnostic Medical Thoracoscopy.\nFINDINGS: The right pleural cavity was thoroughly inspected. The parietal, visceral, and diaphragmatic pleura appeared macroscopically normal. No nodules or plaques were identified. The effusion was drained, and a chest tube was placed for management.",
            3: "Code: 32601.\nSide: Right.\nFindings: Normal pleura.\nAction: Visualization and drainage only.",
            4: "Procedure: Right Diagnostic Thoracoscopy\nSteps:\n1. Port placed.\n2. Pleura looks normal.\n3. Drained fluid.\n4. Chest tube in.\nPlan: Monitor.",
            5: "melissa wilson right side thoracoscopy looked for cancer but pleura looked normal drained the fluid chest tube in stable",
            6: "Diagnostic medical thoracoscopy, right side. Indication: Suspected malignancy. Findings: Normal-appearing pleura. Fluid evacuated. Chest tube placed.",
            7: "[Indication]\nSusp malignancy, Right.\n[Anesthesia]\nModerate.\n[Description]\nNormal pleura visualized. Fluid drained. Chest tube placed.\n[Plan]\nAdmit.",
            8: "Ms. Wilson underwent a right-sided diagnostic thoracoscopy. The pleura appeared normal upon inspection. We drained the fluid and placed a chest tube.",
            9: "Procedure: Right diagnostic pleuroscopy.\nFindings: Unremarkable pleura.\nAction: Inspected cavity. Emptied hydrothorax. Sited drain.\nOutcome: Lung expanded."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency
    # Corresponding to the 10 notes in the source file
    return [
        {"idx": 0, "orig_name": "Sarah Green", "orig_age": 79, "names": ["Alice Brown", "Mary Smith", "Susan Jones", "Linda Johnson", "Patricia Williams", "Barbara Miller", "Elizabeth Davis", "Jennifer Garcia", "Maria Rodriguez"]},
        {"idx": 1, "orig_name": "George Martinez", "orig_age": 57, "names": ["Robert Wilson", "John Moore", "Michael Taylor", "David Anderson", "Richard Thomas", "Charles Jackson", "Joseph White", "Thomas Harris", "Christopher Martin"]},
        {"idx": 2, "orig_name": "Jacob Martinez", "orig_age": 74, "names": ["Daniel Thompson", "Paul Martinez", "Mark Robinson", "Donald Clark", "George Lewis", "Kenneth Lee", "Steven Walker", "Edward Hall", "Brian Allen"]},
        {"idx": 3, "orig_name": "Amanda Ramirez", "orig_age": 54, "names": ["Nancy Young", "Karen Hernandez", "Betty King", "Helen Wright", "Sandra Lopez", "Donna Hill", "Carol Scott", "Ruth Green", "Sharon Adams"]},
        {"idx": 4, "orig_name": "Timothy Scott", "orig_age": 60, "names": ["Kevin Baker", "Ronald Gonzalez", "Timothy Nelson", "Jason Carter", "Jeffrey Mitchell", "Ryan Perez", "Jacob Roberts", "Gary Turner", "Nicholas Phillips"]},
        {"idx": 5, "orig_name": "Edward Lopez", "orig_age": 52, "names": ["Eric Campbell", "Stephen Parker", "Larry Evans", "Scott Edwards", "Frank Collins", "Justin Stewart", "Brandon Sanchez", "Raymond Morris", "Gregory Rogers"]},
        {"idx": 6, "orig_name": "Karen White", "orig_age": 81, "names": ["Michelle Reed", "Laura Cook", "Sarah Morgan", "Kimberly Bell", "Deborah Murphy", "Jessica Bailey", "Shirley Rivera", "Cynthia Cooper", "Angela Richardson"]},
        {"idx": 7, "orig_name": "Nicholas Green", "orig_age": 71, "names": ["Patrick Cox", "Alexander Howard", "Jack Ward", "Dennis Torres", "Jerry Peterson", "Tyler Gray", "Aaron Ramirez", "Henry James", "Douglas Watson"]},
        {"idx": 8, "orig_name": "Donald Flores", "orig_age": 59, "names": ["Peter Brooks", "Adam Kelly", "Nathan Sanders", "Zachary Price", "Walter Bennett", "Kyle Wood", "Harold Barnes", "Carl Ross", "Arthur Henderson"]},
        {"idx": 9, "orig_name": "Melissa Wilson", "orig_age": 54, "names": ["Kathleen Coleman", "Pamela Jenkins", "Martha Perry", "Debra Powell", "Christine Long", "Rachel Patterson", "Carolyn Hughes", "Janet Flores", "Catherine Washington"]}
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
            # Check if this index has a variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: No text variation found for Note {idx} Style {style_num}. Using original.")
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
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
    output_filename = output_dir / "synthetic_thoracoscopy_notes_part_056.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()