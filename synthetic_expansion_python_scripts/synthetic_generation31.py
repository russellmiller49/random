import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_031.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary mapping Note_Index (0-8) -> Style_Index (1-9) -> Text.
    Styles:
    1. Terse Surgeon
    2. Academic Attending
    3. Billing Coder
    4. Trainee/Resident
    5. Sloppy Dictation
    6. Header-less
    7. Templated
    8. Narrative Flow
    9. Synonym Swapper
    """
    
    variations = {
        0: { # David Kim: Bronch + RUL/LLL Biopsies + BAL
            1: "Proc: Bronchoscopy, TBNA/Bx RUL & LLL, BAL.\n- Airway: RUL mass obstructing sup/ant segments. LLL lesion seen w/ REBUS.\n- RUL: TBNA x5, Forceps x6. Mod bleeding (Epi).\n- LLL: TBNA x4, Forceps x5. Mod bleeding (Epi).\n- BAL LLL sup segment.\n- ROSE: RUL malignant, LLL necrosis.\n- Stable.",
            2: "OPERATIVE REPORT: The patient presented with bilateral lung masses. Under general anesthesia (8.5 ETT), the tracheobronchial tree was examined. A fungating endobronchial mass was observed in the RUL, obstructing the superior and anterior segments. Transbronchial needle aspiration (TBNA) and forceps biopsies were obtained. Radial EBUS localization facilitated sampling of a second lesion in the LLL superior segment via TBNA and forceps. A bronchoalveolar lavage was also performed in the LLL. Hemostasis was achieved with topical epinephrine.",
            3: "CPT Coding Summary:\n- 31629 (Primary): TBNA of RUL mass and LLL lesion (multiple sites).\n- 31628 (Secondary): Transbronchial biopsies of LLL lesion (separate lobe).\n- 31625 (Secondary): Endobronchial biopsy of RUL mass (separate site/technique).\n- 31624 (Secondary): BAL LLL.\n- 31654 (Add-on): Radial EBUS used for LLL localization.",
            4: "Procedure Note (Resident)\nIndication: Bilateral masses.\nSteps:\n1. Intubation 8.5 ETT.\n2. RUL mass seen -> TBNA x5, Bx x6.\n3. LLL lesion found via Radial EBUS -> TBNA x4, TBBx x5.\n4. BAL LLL (110cc in, 20cc out).\n5. Hemostasis w/ Epi.\nROSE: RUL + for malignancy.",
            5: "david kim bronchoscopy general anesthesia tube 8.5 we went down saw the rul mass big fungating thing biopsied it needle and forceps then went to the left lower lobe used the radial ebus to find that one biopsied it too needle and forceps little bleeding used epi lavage done left side rose said cancer on the right side left was necrotic patient stable to pacu.",
            6: "The flexible bronchoscope was introduced through the 8.5 ETT. Inspection revealed a fungating mass in the RUL obstructing the superior and anterior segments. TBNA (5 passes) and forceps biopsies (6 samples) were taken from the RUL. A second lesion in the LLL superior segment was localized with radial EBUS; TBNA (4 passes) and transbronchial biopsies (5 samples) were obtained. BAL was performed in the LLL. Moderate bleeding was controlled with epinephrine. ROSE confirmed malignancy in the RUL.",
            7: "[Indication]\nBilateral lung masses, suspected malignancy.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nRUL fungating mass biopsied (TBNA/Forceps). LLL lesion localized via REBUS and biopsied (TBNA/TBBx). BAL LLL performed. Hemostasis achieved.\n[Plan]\nPathology pending. Extubated.",
            8: "Mr. Kim was brought to the bronchoscopy suite for evaluation of bilateral lung masses. We utilized general anesthesia and an 8.5 ETT. Upon inspection, a large mass was found blocking the RUL segments, which we sampled extensively. We then turned our attention to the left lung, using radial EBUS to locate a lesion in the LLL superior segment for additional sampling. A lavage was also done in this area. Bleeding was controlled, and the patient tolerated the procedure well.",
            9: "Procedure: Flexible endoscopic airway inspection and tissue acquisition.\nAction: RUL fungating lesion sampled via needle aspiration and forceps extraction. LLL target localized with radial sonography and sampled via needle and transbronchial forceps. Lavage executed in LLL. Hemorrhage managed with vasoconstrictors."
        },
        1: { # Douglas Diaz: Ion RUL + Chartis
            1: "Proc: Ion Bronch RUL + Chartis LUL.\n- Navigated to RUL anterior seg (1.4cm nodule) w/ Ion.\n- Confirmed w/ CBCT.\n- TBNA x6, Cryo x5.\n- BAL RUL.\n- Chartis LUL: CV Negative (no flow).\n- No complications.",
            2: "PROCEDURE: Robotic-Assisted Bronchoscopy and Collateral Ventilation Assessment. The Ion platform was utilized to navigate to a 1.4 cm nodule in the RUL anterior segment. Target confirmation was achieved via Cone-Beam CT (Cios Spin). Diagnostic sampling included TBNA and transbronchial cryobiopsy. Subsequently, a Chartis balloon occlusion assessment was performed in the LUL to evaluate for collateral ventilation; findings were consistent with absence of CV.",
            3: "Billing:\n- 31629: TBNA RUL.\n- 31628: Transbronchial Cryobiopsy RUL (Single lobe).\n- 31634: Chartis assessment (LUL).\n- 31627: Navigation add-on.\n- 31624: BAL.\nNote: Chartis performed in separate lobe from biopsy.",
            4: "Resident Note\nProcedure: Ion RUL + Chartis\n1. Navigated to RUL nodule (Ion/CBCT).\n2. TBNA/Cryo obtained.\n3. ROSE: Atypical cells.\n4. Chartis LUL: Balloon inflated, flow ceased (CV-).\nPlan: Await final path for possible valves.",
            5: "douglas diaz 74m copd rul nodule used the ion robot navigated to the anterior segment nodule used cone beam to check position took tbna and cryo samples then did a bal went to the left side for chartis check balloon up no flow so cv negative good for valves maybe later patient woke up fine.",
            6: "Robotic bronchoscopy performed for RUL nodule and LUL Chartis assessment. Ion platform used to navigate to 1.4 cm RUL lesion. Cone beam CT confirmed tool-in-lesion. TBNA and cryobiopsies obtained. BAL performed. Chartis evaluation of LUL showed no collateral ventilation. Patient extubated and stable.",
            7: "[Indication]\nRUL Nodule, COPD, CV assessment.\n[Anesthesia]\nGeneral.\n[Description]\nIon Nav to RUL nodule. CBCT confirmation. TBNA/Cryo/BAL performed. Chartis LUL: CV negative.\n[Plan]\nDischarge. Follow up for potential valves.",
            8: "We performed a robotic bronchoscopy on Mr. Diaz. Using the Ion system and Cone Beam CT, we precisely targeted a nodule in his right upper lobe and obtained multiple biopsies using needle and cryoprobe. Following the biopsy, we assessed his left upper lobe for collateral ventilation using the Chartis system, which indicated he might be a good candidate for valves in the future.",
            9: "Procedure: Robotic navigational airway exploration and physiologic assessment.\nAction: RUL nodule accessed via Ion system. Verified with 3D imaging. Tissue harvested via needle and cryo-probe. LUL collateral ventilation assessed via balloon occlusion (Chartis)."
        },
        2: { # Daniel Cooper (Blob 1): EBUS N3 Disease
            1: "Proc: EBUS-TBNA.\n- Stations sampled: 4R, 4L, 7, 10L, 11L.\n- ROSE: Squamous cell CA (4R, 4L, 7).\n- Diagnosis: N3 Disease (Stage IIIB).\n- No complications.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration. Indications included LUL mass and mediastinal adenopathy. Systematic EBUS survey revealed enlarged nodes. TBNA was performed at stations 4R, 4L, 7, 10L, and 11L. Rapid on-site evaluation confirmed squamous cell carcinoma in contralateral (4R) and subcarinal (7) nodes, consistent with N3 disease.",
            3: "Code: 31653 (EBUS-TBNA 3+ stations).\nStations Sampled: 4R, 4L, 7, 10L, 11L (5 stations).\nPathology: Squamous Cell Carcinoma.\nComplexity: High (bilateral sampling).",
            4: "Resident Note\nProcedure: EBUS Staging\n1. Scope passed.\n2. Sampled 7, 4R, 4L, 10L, 11L.\n3. ROSE positive for SCC in mediastinal stations.\n4. Diagnosis: N3 positive.\nPlan: Oncology/Rad Onc.",
            5: "daniel cooper ebus procedure smoker lul mass checked the nodes 4r 4l 7 10l 11l all sampled rose showed squamous cell ca in the mediastinum so n3 disease confirmed minimal bleeding tolerated well.",
            6: "EBUS-TBNA performed for staging of LUL mass. Stations 4R, 4L, 7, 10L, and 11L sampled. ROSE confirmed squamous cell carcinoma in multiple stations including contralateral nodes. Findings consistent with N3 disease. No complications.",
            7: "[Indication]\nLUL mass, staging.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS-TBNA x5 stations (4R, 4L, 7, 10L, 11L). SCC confirmed on ROSE.\n[Plan]\nOncology referral (Stage IIIB).",
            8: "Mr. Cooper underwent EBUS-TBNA to stage his lung cancer. We sampled five lymph node stations across the mediastinum. Unfortunately, the rapid pathology results showed cancer cells in lymph nodes on both sides of the chest (N3 disease), indicating advanced stage IIIB squamous cell carcinoma.",
            9: "Procedure: Sonographic mediastinal staging.\nAction: Aspiration of nodes 4R, 4L, 7, 10L, and 11L. Cytology revealed malignant squamous cells in bilateral stations."
        },
        3: { # Cooper/Scott/Taylor (Blob 2): EBUS (Generic/Mixed source - using Taylor/Scott elements)
            1: "Proc: EBUS-TBNA.\n- Survey: 2R, 4R, 4L, 7, 10R, 11R.\n- Sampled: 4R, 4L, 7, 10R, 11R.\n- ROSE: Granulomas (Sarcoid pattern).\n- No malignancy.",
            2: "PROCEDURE: EBUS-TBNA. The patient presented with mediastinal lymphadenopathy. Ultrasound survey visualized enlarged nodes at stations 4R, 7, and 10R. Transbronchial needle aspiration was performed at 5 stations (4R, 4L, 7, 10R, 11R). Cytopathology revealed non-necrotizing granulomas with no evidence of malignancy, consistent with sarcoidosis.",
            3: "Code: 31653 (EBUS-TBNA 3+ stations).\nStations: 4R, 4L, 7, 10R, 11R.\nFindings: Non-necrotizing granulomas.",
            4: "Resident Note\nProcedure: EBUS\n1. Indication: Adenopathy, R/O Sarcoid.\n2. Sampled: 4R, 4L, 7, 10R, 11R.\n3. ROSE: Granulomas, no cancer.\nPlan: Pulm follow-up.",
            5: "ebus case suspect sarcoid sampled nodes 4r 4l 7 10r 11r rose showed granulomas non necrotizing no cancer cells seen patient did fine home today.",
            6: "EBUS-TBNA performed for evaluation of mediastinal adenopathy. Stations 4R, 4L, 7, 10R, and 11R were sampled. ROSE demonstrated non-necrotizing granulomas consistent with sarcoidosis. No malignancy identified. Discharged stable.",
            7: "[Indication]\nMediastinal adenopathy.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS-TBNA x5 stations. ROSE: Granulomas.\n[Plan]\nSarcoidosis workup.",
            8: "We performed an EBUS procedure to investigate the patient's swollen lymph nodes. We sampled five different areas in the chest. The preliminary results show granulomas, which strongly suggests sarcoidosis rather than cancer. We will await final cultures to rule out infection.",
            9: "Procedure: Endobronchial ultrasound-guided nodal aspiration.\nAction: Stations 4R, 4L, 7, 10R, and 11R accessed. Cytologic analysis indicated granulomatous inflammation typical of sarcoidosis."
        },
        4: { # Linda Harrison: PleurX
            1: "Proc: Tunneled Pleural Catheter (Right).\n- Indication: Malignant effusion (Ovarian CA).\n- US marked.\n- 15.5Fr PleurX placed.\n- Drained 1.1L clear yellow fluid.\n- CXR: Good pos.",
            2: "PROCEDURE: Insertion of Indwelling Tunneled Pleural Catheter. The patient with metastatic ovarian cancer and recurrent right pleural effusion was positioned. Under ultrasound guidance and local anesthesia, a 15.5 French PleurX catheter was tunneled and inserted into the right pleural space. 1,100 mL of fluid was drained. The catheter functioned well and was secured.",
            3: "Code: 32550 (Tunneled pleural catheter).\nGuidance: Ultrasound (included).\nDrainage: 1100 mL.\nPathology: Fluid sent for cytology.",
            4: "Resident Note\nProcedure: PleurX Placement\n1. US scan R chest.\n2. Lidocaine prep.\n3. Tunnel created.\n4. Catheter inserted (Seldinger).\n5. Drained 1.1L.\n6. Dressing applied.\nPlan: Home health education.",
            5: "linda harrison pleurx catheter right side ovarian cancer met effusion ultrasound used numbed skin tunneled the line put it in drained about a liter of fluid patient relieved chest xray looks good.",
            6: "Ultrasound-guided placement of right-sided indwelling pleural catheter (PleurX) for recurrent malignant effusion. 15.5 Fr catheter tunneled and inserted without complication. 1,100 mL fluid drained. Post-procedure CXR confirms placement.",
            7: "[Indication]\nRecurrent malignant pleural effusion.\n[Anesthesia]\nLocal.\n[Description]\nUS guidance. Tunneled PleurX catheter placed Right. 1.1L drained.\n[Plan]\nDischarge with drain supplies.",
            8: "Ms. Harrison underwent the placement of a PleurX catheter to manage her recurrent pleural effusion. We used ultrasound to find the best spot on her right side, created a small tunnel under the skin, and inserted the drainage tube. We removed over a liter of fluid, which should help her breathing significantly.",
            9: "Procedure: Implantation of tunneled pleural drainage device.\nAction: Right hemithorax accessed via sonographic guidance. Subcutaneous tract formed. Indwelling catheter positioned. Effusion evacuated."
        },
        5: { # David Johnson: Pleuroscopy
            1: "Proc: Medical Pleuroscopy (Left).\n- Findings: Diffuse nodules, trapped lung.\n- Bx: Parietal x10, Visceral x3.\n- Intervention: 24Fr Chest tube placed (No pleurodesis due to trapped lung).\n- Suspicion: Mesothelioma.",
            2: "PROCEDURE: Left Medical Pleuroscopy. A rigid pleuroscope was introduced into the left hemithorax. Inspection revealed diffuse nodular thickening of the parietal and visceral pleura, consistent with malignancy (suspected mesothelioma), and trapped lung physiology. Extensive biopsies were taken. Pleurodesis was deferred due to lack of lung expansion. A 24 Fr chest tube was placed for drainage.",
            3: "Code: 32601 (Dx Thoracoscopy w/ biopsy).\nNote: Pleurodesis (32650) NOT performed due to trapped lung. Chest tube (32551) bundled with thoracoscopy.\nPathology: Suspicious for Mesothelioma.",
            4: "Resident Note\nProcedure: Pleuroscopy Left\n1. Trocar placed L 7th ICS.\n2. Fluid drained (1.3L).\n3. Scope in: Nodules everywhere.\n4. Biopsies x13.\n5. Lung trapped -> No talc.\n6. Chest tube placed.\nPlan: Oncology.",
            5: "david johnson pleuroscopy left side looking for cause of effusion went in drained fluid saw nodules all over pleura looks like mesothelioma took lots of biopsies lung wouldn't expand so didn't use talc put a chest tube in admitting.",
            6: "Medical pleuroscopy performed on the left hemithorax. Findings included diffuse pleural thickening and nodularity suspicious for mesothelioma, and trapped lung. Multiple parietal and visceral biopsies obtained. 1,350 mL fluid drained. 24 Fr chest tube placed. No pleurodesis performed.",
            7: "[Indication]\nExudative effusion, rule out meso.\n[Anesthesia]\nMAC.\n[Description]\nPleuroscopy Left. Diffuse nodules. Biopsies x13. Trapped lung. Chest tube placed.\n[Plan]\nAdmit. Pain control.",
            8: "We performed a pleuroscopy on Mr. Johnson to diagnose his pleural effusion. Inside the chest, we found extensive nodules covering the lining of the lung and chest wall, which looks suspicious for mesothelioma. Because the lung was trapped and wouldn't expand, we didn't perform a pleurodesis. We took many biopsies and left a chest tube in place.",
            9: "Procedure: Diagnostic thoracoscopy with pleural sampling.\nAction: Left pleural cavity visualized. Diffuse nodularity observed. Trapped lung physiology noted. Multiple biopsy specimens harvested. Indwelling tube positioned for drainage."
        },
        6: { # Jennifer Taylor: EBUS (Another one)
            1: "Proc: EBUS-TBNA.\n- Stations: 7, 4R, 4L, 10R, 11R.\n- ROSE: Adenocarcinoma (Station 7 positive).\n- Stage: N2 confirmed.",
            2: "PROCEDURE: EBUS-TBNA for mediastinal staging. The patient, with known RLL adenocarcinoma, underwent sampling of lymph node stations 2R, 4R, 4L, 7, 10R, and 11R. ROSE confirmed adenocarcinoma at the subcarinal station (7), confirming N2 disease. The procedure was uncomplicated.",
            3: "Code: 31653 (EBUS 3+ stations).\nPathology: Adenocarcinoma.\nStaging: N2 (Mediastinal involvement).",
            4: "Resident Note\nProcedure: EBUS Staging\n1. Nodes sampled: 4R, 4L, 7, 10R, 11R.\n2. ROSE positive at Station 7.\n3. Diagnosis: Adenocarcinoma N2.\nPlan: Oncology.",
            5: "jennifer taylor ebus staging rll cancer checked all the nodes 7 was positive for cancer so she has n2 disease samples sent for final path no issues.",
            6: "EBUS-TBNA performed. Stations 7, 4R, 4L, 10R, and 11R sampled. ROSE positive for adenocarcinoma at Station 7. Consistent with N2 disease.",
            7: "[Indication]\nRLL Adeno, Staging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS x5 stations. Station 7 positive for malignancy.\n[Plan]\nOncology.",
            8: "Ms. Taylor underwent EBUS staging for her lung cancer. We sampled nodes throughout the mediastinum. Unfortunately, the subcarinal node (Station 7) tested positive for cancer cells, indicating the disease has spread to the lymph nodes (N2 disease).",
            9: "Procedure: Sonographic nodal aspiration for staging.\nAction: Multiple mediastinal stations aspirated. Cytology at Station 7 confirmed metastatic adenocarcinoma."
        },
        7: { # Maria Rodriguez: WLL
            1: "Proc: Whole Lung Lavage (Left).\n- Indication: PAP.\n- DLT placed.\n- 6L saline instilled/drained.\n- Returns cleared.\n- Extubated in PACU.",
            2: "PROCEDURE: Whole Lung Lavage (Left Lung). The patient with pulmonary alveolar proteinosis was intubated with a 37Fr double-lumen tube. Single lung ventilation was established. The left lung was lavaged with 6 liters of warmed saline in 1L aliquots. Effluent cleared significantly. The patient tolerated the procedure well.",
            3: "Code: 32997 (Total lung lavage).\nFluid: 6 Liters.\nLung: Left.\nTechnique: Double-lumen intubation, serial aliquots.",
            4: "Resident Note\nProcedure: WLL Left\n1. DLT placed/confirmed.\n2. Right lung ventilated.\n3. Left lung lavaged w/ 6L saline.\n4. Fluid cleared over time.\n5. Suctioned & extubated.\nPlan: Watch O2.",
            5: "maria rodriguez pap whole lung lavage left side put the double lumen tube in washed the left lung with 6 liters of saline milk came out first then clear fluid patient stable extubated later.",
            6: "Whole lung lavage of the left lung performed for pulmonary alveolar proteinosis. 37Fr DLT used. 6000 mL saline instilled; 5820 mL returned. Effluent cleared. No complications.",
            7: "[Indication]\nPAP, dyspnea.\n[Anesthesia]\nGA, DLT.\n[Description]\nLeft Whole Lung Lavage. 6L Saline. Returns clear.\n[Plan]\nRecovery, plan for Right side later.",
            8: "We performed a whole lung lavage on Ms. Rodriguez's left lung to treat her PAP. We used a double-lumen tube to isolate the lungs, then washed the left lung with 6 liters of saline until the fluid ran clear, removing the protein build-up.",
            9: "Procedure: Total pulmonary lavage.\nAction: Left lung isolated via DLT. Large-volume saline irrigation performed to clear alveolar proteinosis. Effluent transition from turbid to clear observed."
        },
        8: { # Brian Foster: Rigid Bronch
            1: "Proc: Rigid Bronch, Debulking, Dilation.\n- Obstruction: Left Mainstem (Tumor).\n- Interventions: APC, Cryo, Forceps, Balloon Dilation.\n- EBUS-TBNA: Subcarinal mass sampled.\n- Result: 50% improvement in patency.",
            2: "PROCEDURE: Rigid Bronchoscopy with Therapeutic Intervention. The patient presented with left mainstem obstruction. A 12mm rigid scope was inserted. The tumor was debulked using APC, cryotherapy, and mechanical forceps. A CRE balloon was used to dilate the airway, achieving improved patency. Additionally, EBUS-TBNA of a subcarinal mass was performed for diagnosis.",
            3: "Codes: 31629 (EBUS-TBNA bundled? No, TBNA needle used), 31652 (EBUS), 31630 (Dilation), 31641 (Destruction/Debulking - if usually 31641 vs 31630 logic applies).\nNote: Complex airway case. Dilation and Debulking performed.",
            4: "Resident Note\nProcedure: Rigid Bronch + Debulking\n1. Rigid scope inserted.\n2. LMS obstructed by tumor.\n3. Debulked w/ APC/Cryo.\n4. Dilated w/ balloon.\n5. EBUS bx of subcarinal node.\nResult: Airway open.",
            5: "brian foster rigid bronchoscopy left mainstem blocked by tumor we cored it out used apc and cryo then balloon dilated it opened up pretty good also biopsied a node under the carina with ebus.",
            6: "Rigid bronchoscopy performed for left mainstem obstruction. Tumor debulked using APC, cryotherapy, and forceps. Airway dilated with balloon. EBUS-TBNA of subcarinal mass performed. Patency improved.",
            7: "[Indication]\nLMS Obstruction.\n[Anesthesia]\nGA, Rigid.\n[Description]\nTumor debulking (APC/Cryo). Balloon dilation. EBUS-TBNA subcarinal.\n[Plan]\nRad Onc consult.",
            8: "Mr. Foster underwent a rigid bronchoscopy to open his blocked left main airway. We used a combination of heat (APC), cold (cryo), and mechanical tools to remove the tumor, followed by a balloon to stretch the airway open. We also biopsied a lymph node for diagnosis.",
            9: "Procedure: Rigid endoscopic airway recanalization.\nAction: Left mainstem tumor ablated and debulked. Stenosis dilated via balloon. Subcarinal mass sampled via sonographic needle aspiration."
        }
    }
    return variations

def get_base_data_mocks():
    return [
        {"idx": 0, "orig_name": "David Kim", "orig_age": 60, "names": ["Robert Kim", "James Park", "Michael Lee", "William Chen", "David Wu", "Richard Chang", "Joseph Wang", "Thomas Liu", "Charles Yang"]},
        {"idx": 1, "orig_name": "Douglas Diaz", "orig_age": 74, "names": ["Arthur Martinez", "Henry Gomez", "Edward Rodriguez", "Frank Hernandez", "George Lopez", "Walter Gonzalez", "Harold Perez", "Albert Sanchez", "Raymond Ramirez"]},
        {"idx": 2, "orig_name": "Daniel Cooper", "orig_age": 68, "names": ["Samuel Turner", "Benjamin Parker", "Jack Collins", "Alexander Stewart", "Henry Morris", "Sebastian Rogers", "Julian Reed", "Gabriel Cook", "Caleb Morgan"]},
        {"idx": 3, "orig_name": "Jennifer Scott", "orig_age": 54, "names": ["Lisa Baker", "Karen Nelson", "Nancy Carter", "Betty Mitchell", "Sandra Roberts", "Donna Phillips", "Carol Campbell", "Ruth Parker", "Sharon Evans"]},
        {"idx": 4, "orig_name": "Linda Harrison", "orig_age": 66, "names": ["Patricia Edwards", "Barbara Collins", "Susan Stewart", "Jessica Sanchez", "Sarah Morris", "Mary Rogers", "Margaret Reed", "Dorothy Cook", "Lisa Morgan"]},
        {"idx": 5, "orig_name": "David Johnson", "orig_age": 59, "names": ["Christopher Bell", "Matthew Murphy", "Andrew Bailey", "Joshua Rivera", "Ryan Cooper", "Brandon Richardson", "Justin Cox", "Austin Howard", "Ethan Ward"]},
        {"idx": 6, "orig_name": "Jennifer Taylor", "orig_age": 55, "names": ["Amanda Torres", "Melissa Peterson", "Stephanie Gray", "Rebecca Ramirez", "Laura James", "Cynthia Watson", "Kathleen Brooks", "Amy Kelly", "Julie Sanders"]},
        {"idx": 7, "orig_name": "Maria Rodriguez", "orig_age": 38, "names": ["Angela Price", "Christine Bennett", "Debra Wood", "Rachel Barnes", "Janet Ross", "Catherine Henderson", "Carolyn Coleman", "Virginia Jenkins", "Diane Perry"]},
        {"idx": 8, "orig_name": "Brian Foster", "orig_age": 65, "names": ["Jerry Powell", "Dennis Long", "Tyler Patterson", "Gary Hughes", "Larry Flores", "Scott Washington", "Eric Butler", "Stephen Simmons", "Frank Foster"]},
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
            
            # Update note_text with the variation
            # Use get() to handle cases where variation might not be defined (though it is here)
            note_entry["note_text"] = variations_text.get(idx, {}).get(style_num, f"Variation {style_num} not found")
            
            # Update registry_entry fields if they exist, or create if missing (to hold the synthetic data)
            if "registry_entry" not in note_entry:
                note_entry["registry_entry"] = {}
                
            # Update or Set fields
            note_entry["registry_entry"]["patient_age"] = new_age
            note_entry["registry_entry"]["procedure_date"] = rand_date_str
            
            # Ensure unique MRN if present, or create one
            current_mrn = note_entry["registry_entry"].get("patient_mrn", f"MRN_SYN_{idx}")
            note_entry["registry_entry"]["patient_mrn"] = f"{current_mrn}_style_{style_num}"

            # Add synthetic metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_blvr_notes_part_031.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()