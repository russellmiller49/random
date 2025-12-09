import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_023.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Medical Thoracoscopy (Pleuroscopy)
            1: "Indication: Large R pleural effusion, nodules.\nProc: Medical Thoracoscopy (Pleuroscopy).\nActions: Pleural fluid drained. Biopsies x6 (parietal/visceral). Talc slurry instilled. Chest tube placed.\nFindings: Carcinomatosis.\nPlan: Admit.",
            2: "PROCEDURE: Medical Thoracoscopy with Pleurodesis.\nNARRATIVE: The right pleural space was accessed via a single port. Inspection revealed diffuse nodularity along the parietal and visceral surfaces. Multiple grasp biopsies were obtained. Following mechanical abrasion, 4g of talc slurry was instilled under direct vision for pleurodesis. A 24Fr chest tube was secured.\nIMPRESSION: Metastatic pleural disease.",
            3: "Code: 32650 (Thoracoscopy with pleurodesis).\nTechnique: Rigid thoracoscope.\nIntervention: Biopsy of pleura followed by chemical pleurodesis (talc).\nDrainage: Large volume effusion evacuated.\nDevice: Chest tube placed at conclusion.",
            4: "Procedure: Pleuroscopy\nPatient: John Doe\nSteps:\n1. Local/Sedation.\n2. Trocar in.\n3. Drained fluid.\n4. Saw nodules everywhere.\n5. Biopsied.\n6. Poured in talc.\n7. Chest tube in.\nPlan: Pain control.",
            5: "medical thoracoscopy right side big effusion. drained it all out. saw nodules took biopsies. put talc in for pleurodesis. put a chest tube in. patient tolerated ok. sending fluid for cytology.",
            6: "Medical thoracoscopy for large right pleural effusion with multiple parietal and visceral pleural nodules. Pleural biopsies performed. Talc slurry pleurodesis performed. Chest tube placement confirmed. Pathology pending.",
            7: "[Indication]\nRecurrent right pleural effusion.\n[Anesthesia]\nMAC/Local.\n[Description]\nThoracoscopy performed. Nodules biopsied. Talc pleurodesis completed. Chest tube placed.\n[Plan]\nAdmit for chest tube management.",
            8: "The patient underwent medical thoracoscopy for a large right-sided effusion. Upon entering the chest, we found numerous nodules on the lung and chest wall. We took several biopsies to confirm the diagnosis. To prevent the fluid from coming back, we instilled a talc slurry into the chest cavity. A chest tube was left in place to drain any remaining fluid and air.",
            9: "Procedure: Thoracoscopic exploration with sclerosis.\nFindings: Diffuse pleural studding.\nAction: The pleural cavity was evacuated. Tissue sampling was performed via optical forceps. Chemical sclerotherapy was administered. A drainage catheter was sited.\nResult: Pleurodesis initiated."
        },
        1: { # Tracheal Dilation
            1: "Indication: Tracheal stenosis.\nProc: Flex bronch, Balloon dilation.\nDetails: Stenosis 40% patency -> dilated to 75%.\nTool: CRE Balloon.\nComp: None.\nPlan: Monitor stridor.",
            2: "PROCEDURE: Flexible Bronchoscopy with Tracheal Dilation.\nINDICATION: Post-intubation tracheal stenosis.\nNARRATIVE: The airway was inspected, revealing a concentric stenotic segment in the mid-trachea reducing the lumen to approximately 40%. Serial balloon dilations were performed using a CRE balloon, achieving a final patency of 75%. No significant mucosal trauma was noted.\nIMPRESSION: Improved tracheal caliber.",
            3: "Code: 31630 (Bronchoscopy with dilation).\nTarget: Trachea.\nMethod: Balloon dilation (serial inflations).\nResult: Improvement from 40% to 75% luminal diameter.\nNote: Diagnostic component bundled.",
            4: "Procedure: Bronch Dilation\nPatient: Jane Smith\nSteps:\n1. Scope in.\n2. Found stenosis in trachea.\n3. Balloon up to 3ATM then 5ATM.\n4. Opened up good.\n5. No bleeding.\nPlan: Decadron, observe.",
            5: "flex bronch for stenosis patient had a tube before. trachea was tight like 40 percent. used the balloon to stretch it out. got it to 75 percent. no bleeding really. patient breathing better.",
            6: "Flexible bronchoscopy with serial balloon dilation of post-intubation tracheal stenosis. Stenosis improved from ~40% to ~75% patency. No complications. Post-procedure airway patent.",
            7: "[Indication]\nTracheal stenosis (post-intubation).\n[Anesthesia]\nModerate sedation.\n[Description]\nFlexible bronchoscopy. Stenosis identified. Serial balloon dilation performed. Patency improved to 75%.\n[Plan]\nDischarge home if stable.",
            8: "We performed a flexible bronchoscopy to treat the patient's tracheal narrowing. The stenosis was significant, blocking about 60% of the airway. We used a balloon catheter to gently stretch the scar tissue in multiple steps. By the end of the procedure, the airway was much more open, with about 75% patency. The patient tolerated the dilation well.",
            9: "Procedure: Endoscopic tracheal expansion.\nIssue: Cicatricial airway stenosis.\nAction: The stricture was radially expanded using a pneumatic dilator. Serial inflations were executed.\nResult: Augmented tracheal cross-section."
        },
        2: { # PDT
            1: "Indication: Endobronchial SCC (LMS).\nProc: PDT Light Application.\nDetails: Photofrin given 48h prior. Light diffuser placed. 200J/cm applied.\nResult: Tumor treatment complete.\nPlan: Clean-up bronch 48h.",
            2: "PROCEDURE: Bronchoscopy with Photodynamic Therapy (PDT).\nINDICATION: Early-stage squamous cell carcinoma, left mainstem.\nNARRATIVE: Following appropriate photosensitizer administration, the patient underwent therapeutic bronchoscopy. The lesion in the LMS was identified. A cylindrical diffuser was positioned, and light energy was delivered to the tumor bed to induce necrosis. The patient tolerated the light activation phase without complication.\nIMPRESSION: Successful PDT application.",
            3: "Code: 31641 (Tumor destruction via PDT).\nAgent: Porfimer sodium (Photofrin) administered previously.\nAction: Light application via bronchoscope.\nTarget: Left Mainstem Bronchus.",
            4: "Procedure: PDT\nPatient: Robert Brown\nSteps:\n1. Meds given 2 days ago.\n2. Scope to LMS.\n3. Put light fiber in.\n4. Turned on laser for prescribed time.\n5. No issues.\nPlan: Come back for necrotic debris removal.",
            5: "doing the light part of the pdt today. patient got the photofrin already. went to the left main saw the cancer. put the light stick in and cooked it. patient did fine. needs to stay out of the sun.",
            6: "Photodynamic therapy light application to an early-stage endobronchial squamous cell carcinoma in the left mainstem bronchus after prior Photofrin administration. Procedure successful. No immediate complications.",
            7: "[Indication]\nLMS Squamous Cell Carcinoma.\n[Anesthesia]\nGeneral.\n[Description]\nPDT light application performed. Diffuser placed at tumor site. Light energy delivered.\n[Plan]\nAvoid sunlight. Follow-up bronchoscopy.",
            8: "The patient returned for the light activation portion of their photodynamic therapy. They had received the photosensitizing drug previously. We guided the bronchoscope to the tumor in the left main airway and inserted the light fiber. The laser light was applied for the calculated time to treat the cancer cells. The procedure went as planned.",
            9: "Procedure: Photo-illumination therapy.\nContext: Oncologic ablation.\nAction: The photosensitized lesion in the LMS was illuminated via an intraluminal diffuser. Photochemical reaction induced.\nResult: Therapeutic irradiation completed."
        },
        3: { # Valve Removal (3 valves)
            1: "Indication: Valve retrieval.\nProc: Bronchoscopy, removal of 3 Zephyr valves (RUL).\nFindings: Mucus plugging distal to valves.\nAction: Valves removed. Airway cleared.\nPlan: Assess for lung re-expansion.",
            2: "PROCEDURE: Flexible Bronchoscopy with Removal of Endobronchial Valves.\nINDICATION: Valve retrieval/clearance.\nNARRATIVE: Under general anesthesia, the RUL was inspected. Three Zephyr valves were identified in situ. Each valve was grasped and removed without difficulty. Significant distal mucus plugging was noted and suctioned clear. The airway mucosa appeared healthy.\nIMPRESSION: Successful removal of bronchial valves.",
            3: "Code: 31648 (Removal of bronchial valves).\nQuantity: 3 valves.\nLocation: Right Upper Lobe.\nNote: Clearance of secretions (31645) bundled into removal if related to the obstruction.",
            4: "Procedure: Valve Removal\nPatient: Michael Wilson\nSteps:\n1. GA.\n2. Scope to RUL.\n3. Pulled 3 valves out.\n4. Sucked out a lot of mucus behind them.\n5. Airway open.\nPlan: Recovery.",
            5: "taking out the valves today from the RUL. patient under GA. went in grabbed the three zephyr valves pulled them out. lots of junk behind them cleaned it up. all done.",
            6: "Flexible bronchoscopy under GA with retrieval of three Zephyr endobronchial valves from the right upper lobe. Clearance of distal mucus plugging performed. Airway patent post-removal.",
            7: "[Indication]\nValve removal (RUL).\n[Anesthesia]\nGeneral.\n[Description]\n3 Zephyr valves removed from RUL. Mucus plugging cleared. No complications.\n[Plan]\nDischarge.",
            8: "We performed a bronchoscopy to remove the valves from the patient's right upper lobe. Under general anesthesia, we located the three valves and removed them one by one. There was a significant amount of mucus trapped behind the valves, which we suctioned out. The airways are now clear and open.",
            9: "Procedure: Endoscopic prosthesis retrieval.\nAction: Three bronchial occluders were extracted from the RUL. Post-obstructive secretions were evacuated.\nResult: Restoration of bronchial patency."
        },
        4: { # Stent Surveillance (Therapeutic Aspiration)
            1: "Indication: Stent surveillance.\nProc: Flex bronch via trach.\nFindings: Dumon stent LMS. Thick secretions.\nAction: Extensive suctioning/clearance.\nResult: Patent stent.",
            2: "PROCEDURE: Therapeutic Bronchoscopy (Stent Maintenance).\nINDICATION: Airway clearance in patient with LMS stent.\nNARRATIVE: The airway was accessed via the tracheostomy. The Dumon stent in the left mainstem was visualized. The lumen was compromised by thick, tenacious secretions. Extensive suctioning and lavage were required to restore patency. No granulation tissue or migration was noted.\nIMPRESSION: Stent patent after secretion clearance.",
            3: "Code: 31645 (Therapeutic aspiration).\nReason: Extensive suctioning required to clear stent (beyond diagnostic).\nRoute: Via tracheostomy.\nTarget: Left Mainstem.",
            4: "Procedure: Bronch/Suction\nPatient: Sarah Davis\nSteps:\n1. Through trach.\n2. Looked at stent in LMS.\n3. Full of goo.\n4. Suctioned it all out.\n5. Stent looks okay now.\nPlan: Continue humidity.",
            5: "bronch through the trach to check the stent. left main stent was plugged up with mucus. spent a while sucking it out. clear now. stent is sitting fine.",
            6: "Flexible bronchoscopy via tracheostomy for Dumon stent surveillance. Extensive suctioning and clearance of thick secretions from the left mainstem stent lumen performed. Stent patent post-procedure.",
            7: "[Indication]\nStent surveillance, secretion retention.\n[Anesthesia]\nLocal/Ventilator support.\n[Description]\nDumon stent inspected. Extensive secretions cleared from LMS. Stent patent.\n[Plan]\nPulmonary hygiene.",
            8: "This was a routine check of the patient's airway stent, done through their tracheostomy tube. We found the stent in the left main airway was partially blocked by thick mucus. We performed extensive suctioning to clear it out. Once cleaned, the stent appeared to be in good position and functioning well.",
            9: "Procedure: Endoscopic airway toilet.\nTarget: Indwelling bronchial prosthesis.\nAction: The Dumon stent was cannulated. Inspissated secretions were evacuated via lavage and suction.\nResult: Luminal patency re-established."
        },
        5: { # Cryobiopsy ILD
            1: "Indication: ILD workup.\nProc: REBUS-guided Cryobiopsy RLL.\nDetails: Arndt blocker placed. REBUS confirmed no vessels. 5 samples taken.\nComp: None.\nDisp: Home.",
            2: "PROCEDURE: Transbronchial Cryobiopsy with Radial EBUS Guidance.\nINDICATION: Interstitial Lung Disease diagnosis.\nNARRATIVE: An Arndt bronchial blocker was positioned for prophylactic control. The RLL target area was screened with radial EBUS to ensure a vessel-free zone. Five cryobiopsies were obtained. The blocker was inflated after each pass to prevent bleeding. Hemostasis was excellent.\nIMPRESSION: Adequate tissue for ILD classification.",
            3: "Codes: 31628 (Lung biopsy), 31654 (REBUS).\nNote: Cryobiopsy is coded as 31628. Blocker is incidental.\nSamples: 5 from RLL.\nGuidance: Radial EBUS used for safety.",
            4: "Procedure: Cryobiopsy\nPatient: Emily White\nSteps:\n1. GA/ETT.\n2. Blocker in RLL.\n3. REBUS checked area.\n4. Freeze biopsy x5.\n5. Inflated blocker each time.\n6. No bleeding.\nResult: ILD tissue.",
            5: "doing a cryo for ild. put the blocker in first. used the radar probe to check for vessels. froze 5 pieces from the right lower lobe. no bleeding problems. hopefully pathology can figure it out.",
            6: "Bronchoscopy with REBUS-guided transbronchial cryobiopsy of the right lower lobe (5 samples) for ILD workup using an Arndt blocker for bleeding control. Procedure uneventful.",
            7: "[Indication]\nILD diagnosis.\n[Anesthesia]\nGeneral.\n[Description]\nREBUS guidance used. Arndt blocker placed. 5 cryobiopsies taken from RLL. Hemostasis secured.\n[Plan]\nFollow up ILD clinic.",
            8: "We performed a cryobiopsy to help diagnose the patient's interstitial lung disease. We placed a balloon blocker in the airway first for safety. Using radial ultrasound, we found a safe spot in the right lower lobe and took five large tissue samples using the freezing probe. There was no significant bleeding, and the patient recovered well.",
            9: "Procedure: Cryo-adhesive parenchymal sampling.\nGuidance: Radial ultrasonography.\nAction: An endobronchial blocker was deployed. Five biopsy specimens were harvested from the RLL via cryoprobe.\nResult: Diagnostic tissue acquisition."
        },
        6: { # Bedside Talc Pleurodesis
            1: "Indication: Malignant effusion.\nProc: Bedside Talc Pleurodesis.\nAccess: Existing chest tube.\nAction: 4g Talc slurry instilled. Tube clamped. Patient rotated.\nResult: Pleurodesis complete.",
            2: "PROCEDURE: Chemical Pleurodesis via Thoracostomy Tube.\nINDICATION: Recurrent malignant pleural effusion.\nNARRATIVE: The existing right-sided chest tube was assessed and found to be functional. A slurry containing 4 grams of sterile talc was instilled through the tube. The tube was clamped, and the patient was repositioned to ensure adequate distribution. The tube was then returned to suction.\nIMPRESSION: Talc pleurodesis administered.",
            3: "Code: 32560 (Pleurodesis via chest tube).\nAgent: Talc slurry.\nRoute: Existing tube (no new insertion code).\nSetting: Bedside.",
            4: "Procedure: Talc Slurry\nPatient: William Green\nSteps:\n1. Mixed talc.\n2. Pushed into chest tube.\n3. Clamped tube.\n4. Rolled patient around.\n5. Unclamped.\nPlan: Remove tube when output drops.",
            5: "bedside talc job. right chest tube. pushed the slurry in. clamped it for a while. moved the patient so it spreads. hooked back up to suction. hope it sticks.",
            6: "Bedside talc slurry pleurodesis via existing large-bore chest tube for right malignant pleural effusion. Position changes performed for talc distribution. Tube returned to suction.",
            7: "[Indication]\nMalignant effusion.\n[Anesthesia]\nLocal/None.\n[Description]\nTalc slurry instilled via existing chest tube. Dwell time and rotation completed. Suction resumed.\n[Plan]\nMonitor output.",
            8: "We performed a pleurodesis procedure at the bedside to prevent fluid from returning. Using the patient's existing chest tube, we injected a mixture of talc. We clamped the tube and helped the patient change positions to coat the inside of the chest. The tube was then unclamped and put back on suction.",
            9: "Procedure: Chemical sclerotherapy administration.\nRoute: Indwelling thoracostomy catheter.\nAction: Sclerosing agent (talc) was introduced. Patient repositioning facilitated distribution.\nResult: Pleural symphysis induction attempted."
        },
        7: { # Emergency Hemoptysis
            1: "Indication: Massive hemoptysis.\nProc: Emergency Bronch, Balloon Tamponade.\nFindings: Bleeding LUL/Lingula.\nAction: Iced saline, Epi, TXA. Fogarty balloon placed/inflated.\nResult: Bleeding controlled/tamponaded.",
            2: "PROCEDURE: Emergency Bronchoscopy for Hemoptysis Control.\nINDICATION: Life-threatening airway hemorrhage.\nNARRATIVE: The airway was filled with fresh blood. Suctioning revealed the source in the LUL/Lingula. Lavage with iced saline and topical epinephrine was insufficient. A Fogarty balloon was deployed into the LUL bronchus and inflated, resulting in cessation of bleeding into the central airway.\nIMPRESSION: Hemoptysis controlled via balloon tamponade.",
            3: "Code: 31634 (Balloon occlusion/tamponade).\nNote: Includes diagnostic inspection.\nMeds: Epi, TXA used.\nDevice: Fogarty catheter.",
            4: "Procedure: Hemoptysis Control\nPatient: James Black\nSteps:\n1. Emergent scope.\n2. Blood everywhere.\n3. Found source LUL.\n4. Tried saline/epi - didn't work.\n5. Put balloon in and blew it up.\n6. Stopped the bleed.\nPlan: ICU, IR embolization?",
            5: "emergency bronch for bleeding. patient coughing up cups of blood. went down saw it coming from the left upper. poured ice water and epi on it. still oozing. put a fogarty balloon in and wedged it. bleeding stopped. leaving it in for now.",
            6: "Emergency bedside bronchoscopy for massive hemoptysis. Localization: Bleeding to the left upper lobe and lingula. Interventions: Iced saline, topical epinephrine, tranexamic acid, and Fogarty balloon tamponade. Result: Hemostasis achieved.",
            7: "[Indication]\nMassive hemoptysis.\n[Anesthesia]\nTopical/Sedation.\n[Description]\nSource localized to LUL. Conservative measures failed. Balloon tamponade performed. Bleeding contained.\n[Plan]\nICU, consider bronchial artery embolization.",
            8: "This was an emergency procedure for severe coughing up of blood. We identified the bleeding coming from the left upper lobe. We tried washing it with cold saline and medicine to shrink the vessels, but it kept bleeding. We then placed a balloon catheter into that airway and inflated it to block the bleeding site. This successfully stopped the blood from filling the rest of the lungs.",
            9: "Procedure: Emergent endoscopic hemostasis.\nIndication: Pulmonary hemorrhage.\nAction: The bleeding source was isolated to the LUL. Pharmacologic lavage was attempted. Mechanical tamponade was achieved via balloon inflation.\nResult: Hemorrhage containment."
        },
        8: { # Hybrid Rigid + IPC (RMS tumor)
            1: "Indication: Malignant obstruction + Effusion.\nProc: Rigid Bronch, RMS Stent, PleurX.\nDetails: Debulked RMS tumor. Placed metallic stent. Extensive suction. Pericardial window (CT Surgery). PleurX placed right.\nPlan: Oncology.",
            2: "PROCEDURE: Combined Hybrid Airway and Pleural Intervention.\nNARRATIVE: Rigid bronchoscopy addressed the right mainstem tumor. Debulking and dilation facilitated the placement of a metallic stent. Post-obstructive secretions were cleared. Concurrently, a pericardial window was performed by the surgical team (separate note). Finally, a tunneled indwelling pleural catheter (PleurX) was inserted for management of the malignant effusion.\nIMPRESSION: Palliation of airway and pleural disease.",
            3: "Codes: 31636 (Bronchial Stent), 31641 (Tumor Destruction), 32550 (IPC).\nNote: 31631 is tracheal; RMS is bronchial (31636). Debulking charged separately.\nProcedures: Rigid bronch + Stent + IPC.",
            4: "Procedure: Hybrid Case\nPatient: Thomas Grey\nSteps:\n1. Rigid scope.\n2. Cleaned out RMS tumor.\n3. Put metal stent in RMS.\n4. Cleaned out pus.\n5. Surgery did their window.\n6. I put in a PleurX drain.\nPlan: Chemo.",
            5: "Big case in the hybrid room. Rigid bronch first. scraped out the tumor in the right main. put a metal stent in. sucked out a ton of junk. surgeons did the heart window. then i put a tunnelled catheter in the chest for the fluid. patient stable.",
            6: "Complex hybrid-OR case. Procedures: Rigid bronchoscopy for right mainstem tumor debulking, balloon dilation, metallic stent placement. Extensive suctioning of post-obstructive secretions. Right PleurX catheter placement. Pericardial window by CT surgery (separate report).",
            7: "[Indication]\nRMS obstruction, malignant effusion.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronch: Tumor debulked, RMS stent placed. IPC: Right PleurX placed.\n[Plan]\nDischarge planning.",
            8: "In a combined procedure in the operating room, we addressed both the patient's airway and fluid issues. Using a rigid scope, we cleared a tumor blocking the right main airway and placed a metal stent to keep it open. We also suctioned out a lot of trapped secretions. After the surgeons finished their part, we placed a permanent PleurX drain for the fluid around the lung.",
            9: "Procedure: Multi-modal palliative intervention.\nAction: Rigid endoscopic recanalization of the RMS was performed via debulking and stenting. A tunneled pleural drainage system was implanted.\nResult: Restoration of airway patency and pleural drainage."
        },
        9: { # Diagnostic BAL
            1: "Indication: Pneumonia.\nProc: Flex Bronch, BAL LLL.\nFindings: Normal airway. No lesions.\nLab: Sent for culture/cyto.\nDisp: Floor.",
            2: "PROCEDURE: Diagnostic Flexible Bronchoscopy with Bronchoalveolar Lavage.\nINDICATION: Evaluation of non-resolving pneumonia.\nNARRATIVE: The tracheobronchial tree was inspected and found to be patent with no endobronchial lesions. The bronchoscope was wedged in a segment of the left lower lobe. 100mL of saline was instilled and aspirated. The return was cloudy and sent for analysis.\nIMPRESSION: Presumed infectious pneumonia.",
            3: "Code: 31624 (BAL).\nTarget: Left Lower Lobe.\nFindings: Negative for mass.\nSpecimen: Lavage fluid sent for microbiology.",
            4: "Procedure: BAL\nPatient: Linda Clark\nSteps:\n1. Scope down.\n2. Lungs look clear.\n3. Wedged LLL.\n4. Washed with saline.\n5. Sucked it back.\nPlan: Antibiotics pending cultures.",
            5: "bronch for pneumonia. looked normal inside. went to the left lower lobe did a wash. fluid looked purulent. sent to lab. done.",
            6: "Diagnostic bronchoscopy with bronchoalveolar lavage of the left lower lobe for pneumonia evaluation. No endobronchial lesions seen. Lavage obtained.",
            7: "[Indication]\nPneumonia.\n[Anesthesia]\nLocal/Sedation.\n[Description]\nAirways patent. BAL LLL performed. No masses.\n[Plan]\nAwait cultures.",
            8: "We performed a bronchoscopy to investigate the patient's pneumonia. The airways looked normal with no signs of tumors or blockage. We washed the left lower lobe with saline and collected the fluid to test for bacteria or other infections.",
            9: "Procedure: Diagnostic alveolar lavage.\nIndication: Pulmonary infiltrate.\nAction: The bronchial tree was surveyed. A liquid biopsy (BAL) was performed in the LLL.\nResult: Specimen submitted for microbiologic analysis."
        }
    }
    return variations

def get_base_data_mocks():
    # Names and mock variations for 10 patients
    return [
        {"idx": 0, "orig_name": "John Doe", "orig_age": 65, "names": ["Robert Smith", "William Johnson", "James Brown", "David Jones", "Charles Miller", "Joseph Davis", "Thomas Garcia", "Christopher Rodriguez", "Daniel Wilson"]},
        {"idx": 1, "orig_name": "Jane Smith", "orig_age": 55, "names": ["Mary Williams", "Patricia Jones", "Jennifer Brown", "Linda Davis", "Elizabeth Miller", "Barbara Wilson", "Susan Moore", "Jessica Taylor", "Sarah Anderson"]},
        {"idx": 2, "orig_name": "Robert Brown", "orig_age": 70, "names": ["Michael Thomas", "Richard Jackson", "Paul White", "Mark Harris", "Donald Martin", "George Thompson", "Kenneth Garcia", "Steven Martinez", "Edward Robinson"]},
        {"idx": 3, "orig_name": "Michael Wilson", "orig_age": 62, "names": ["Brian Clark", "Ronald Lewis", "Anthony Lee", "Kevin Walker", "Jason Hall", "Matthew Allen", "Gary Young", "Timothy Hernandez", "Jose King"]},
        {"idx": 4, "orig_name": "Sarah Davis", "orig_age": 58, "names": ["Karen Wright", "Nancy Lopez", "Lisa Hill", "Betty Scott", "Margaret Green", "Sandra Adams", "Ashley Baker", "Kimberly Gonzalez", "Donna Nelson"]},
        {"idx": 5, "orig_name": "Emily White", "orig_age": 60, "names": ["Carol Carter", "Michelle Mitchell", "Amanda Perez", "Melissa Roberts", "Deborah Turner", "Stephanie Phillips", "Rebecca Campbell", "Laura Parker", "Sharon Evans"]},
        {"idx": 6, "orig_name": "William Green", "orig_age": 72, "names": ["Frank Edwards", "Scott Collins", "Eric Stewart", "Stephen Sanchez", "Andrew Morris", "Raymond Rogers", "Gregory Reed", "Joshua Cook", "Jerry Morgan"]},
        {"idx": 7, "orig_name": "James Black", "orig_age": 45, "names": ["Dennis Bell", "Walter Murphy", "Patrick Bailey", "Peter Rivera", "Harold Cooper", "Douglas Richardson", "Henry Cox", "Carl Howard", "Arthur Ward"]},
        {"idx": 8, "orig_name": "Thomas Grey", "orig_age": 68, "names": ["Ryan Torres", "Roger Peterson", "Joe Gray", "Juan Ramirez", "Jack James", "Albert Watson", "Jonathan Brooks", "Justin Kelly", "Terry Sanders"]},
        {"idx": 9, "orig_name": "Linda Clark", "orig_age": 75, "names": ["Cynthia Price", "Kathleen Bennett", "Amy Wood", "Angela Barnes", "Shirley Ross", "Brenda Henderson", "Pamela Coleman", "Nicole Jenkins", "Ruth Perry"]}
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
                print(f"Warning: Missing variation for Note {idx} Style {style_num}")
                continue

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Add patient fields if missing or update if present
                note_entry["registry_entry"]["patient_age"] = new_age
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Mock MRN if not present or append
                current_mrn = note_entry["registry_entry"].get("patient_mrn", f"MRN-{idx}")
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
    output_filename = output_dir / "synthetic_interventional_notes_part_023.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()