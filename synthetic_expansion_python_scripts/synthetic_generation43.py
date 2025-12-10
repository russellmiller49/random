import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (The file provided in the prompt context)
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_043.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
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
        0: { # Note 0: Bronchoscopy with Biopsy/Brush (31625, 31623)
            1: "Procedure: Bronchoscopy w/ biopsy & brush.\n- ETT.\n- Mass R mainstem.\n- Forceps bx x4: good samples.\n- Protected brush x1: cytology.\n- Hemostasis: saline.\n- Extubated stable.",
            2: "OPERATIVE REPORT: The patient was anesthetized and the airway secured via endotracheal intubation. Inspection of the tracheobronchial tree revealed a fungating, friable neoplasm obstructing the right mainstem bronchus. Utilizing forceps, multiple tissue samples were procured for histopathologic examination. Subsequently, a protected specimen brush was deployed to obtain cytologic specimens from the same endobronchial lesion. Hemostasis was achieved via cold saline lavage.",
            3: "Service Justification:\nCPT 31625: Flexible bronchoscopy with endobronchial biopsy. Multiple forceps biopsies taken from right mainstem mass.\nCPT 31623: Flexible bronchoscopy with protected brushings. Separate protected brush passed into the same lesion for cytology.\nNo TBNA or BAL performed.",
            4: "Procedure Note:\n1. Time out/Consent verified.\n2. General Anesthesia/ETT.\n3. Scope inserted to carina.\n4. R mainstem mass identified.\n5. Biopsies taken with standard forceps.\n6. Brushing performed with protected catheter.\n7. Scope removed. Patient stable.",
            5: "patient 68 female here for mass on ct we went down with the scope saw the tumor in the right mainstem looks like cancer took some bites with the forceps bleeding was okay then did a brush too patient did fine woke up in pacu no issues.",
            6: "Flexible bronchoscopy was performed under general anesthesia via oral endotracheal tube. Vocal cords and trachea were normal. A friable, obstructing, exophytic tumor was visualized in the right mainstem bronchus with contact bleeding. Multiple endobronchial forceps biopsies were obtained from the right mainstem tumor for histology with good hemostasis after iced saline and brief suctioning. Additional protected brushings were performed from the same lesion for cytology. The patient was extubated in the procedure room.",
            7: "[Indication]\nHemoptysis, R mainstem mass.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nFriable tumor R mainstem. Forceps biopsies x4. Protected brushings x1. Hemostasis secured.\n[Plan]\nPathology pending. Oncology referral.",
            8: "The patient underwent flexible bronchoscopy under general anesthesia. Upon entering the right mainstem bronchus, we visualized a large, friable mass. We proceeded to take multiple forceps biopsies for tissue diagnosis. Following this, we used a protected brush to gather cells for cytology. The bleeding was minimal and controlled easily. The patient tolerated the procedure well.",
            9: "Flexible bronchoscopy conducted under general anesthesia. An exophytic lesion was observed in the right mainstem. Multiple tissue samples were harvested using forceps. Additionally, cellular material was collected via protected brushing. Hemostasis was maintained. The patient was extubated without incident."
        },
        1: { # Note 1: Foreign Body Removal (31635)
            1: "Indication: FB aspiration.\nAnesthesia: Moderate.\nFindings: Nut in RMS.\nAction: Removal via forceps en bloc.\nOutcome: Airway clear. No fragmentation.",
            2: "PROCEDURE: Therapeutic bronchoscopy for foreign body retrieval. Under moderate sedation with preservation of spontaneous ventilation, the bronchoscope was introduced. An organic foreign body, consistent with a nut, was identified impacting the right mainstem bronchus. Using grasping forceps, the object was secured and extracted en bloc to prevent fragmentation. Re-inspection confirmed patency of the distal airways.",
            3: "Coding: 31635 (Bronchoscopy with removal of foreign body).\nTechnique: Visualization of organic FB in right mainstem. Grasping forceps used to secure and remove object through native airway. No other distinct procedures performed.",
            4: "Resident Note:\n- Patient: 45M, choking episode.\n- Sedation: Moderate.\n- Scope: Flexible.\n- Findings: Nut lodged in R mainstem.\n- Intervention: Forceps removal.\n- Complications: None.",
            5: "guy choked on a nut came in coughing wheezing right side scope went in saw the nut right main bronchus grabbed it with the forcep pulled it all the way out didn't break it looks good now breathing better home today.",
            6: "Flexible bronchoscopy performed with moderate sedation and spontaneous breathing through the native airway. A hard organic foreign body was visualized lodged in the right mainstem bronchus with surrounding edema but no active bleeding. The foreign body was grasped with forceps and removed en bloc through the bronchoscope without fragmentation. Airways were reinspected and no residual material was seen.",
            7: "[Indication]\nChoking, unilateral wheeze.\n[Anesthesia]\nModerate, native airway.\n[Description]\nForeign body (nut) identified in RMS. Removed en bloc with forceps. Mucosa edematous but intact.\n[Plan]\nDischarge home.",
            8: "We performed a flexible bronchoscopy using moderate sedation. Upon inspection, a hard organic object was seen obstructing the right mainstem bronchus. We carefully grasped the object with forceps and removed it completely without breaking it. A follow-up look showed the airway was clear.",
            9: "Flexible bronchoscopy executed with moderate sedation. A foreign object was spotted in the right mainstem. It was seized with forceps and extracted in one piece. The airway was cleared of the obstruction. The patient was discharged."
        },
        2: { # Note 2: EBUS 1-2 Stations (31652)
            1: "Proc: EBUS-TBNA.\nTarget: 4R.\nNeedle: 22G.\nPasses: 3.\nROSE: Malignant.\nNo other stations sampled.",
            2: "OPERATIVE NARRATIVE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration. The 4R paratracheal station was identified ultrasonographically, demonstrating heterogeneous echotexture. A 22-gauge needle was utilized to perform three transbronchial aspirations. Rapid On-Site Evaluation (ROSE) confirmed the presence of malignant cytology. The procedure was terminated without sampling additional stations.",
            3: "CPT 31652: Bronchoscopy with EBUS-TBNA, 1-2 nodal stations.\nDetails: Station 4R sampled under direct ultrasound guidance. 3 passes made. No other stations sampled (supports single code 31652, no 31653).",
            4: "Procedure Steps:\n1. ETT placement.\n2. EBUS scope insertion.\n3. ID station 4R (12mm).\n4. FNA x 3 with 22G needle.\n5. ROSE pos for carcinoma.\n6. Extubate.",
            5: "62 male lung cancer workup ebus done general anesthesia tube in. looked at 4r node it was big poked it three times with the needle rose said cancer so we stopped there didnt do any other nodes patient did fine.",
            6: "Linear EBUS bronchoscopy performed under general anesthesia via oral ETT. The 4R lymph node measured approximately 12 mm short axis with heterogeneous echotexture and no Doppler vessels. Using a 22-gauge EBUS needle, three passes were obtained from station 4R with good cytologic material seen on ROSE, consistent with malignant cells. No additional nodal stations were sampled.",
            7: "[Indication]\nPET-avid 4R node.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS localization of 4R. TBNA x3 (22G). ROSE positive for malignancy. No other stations.\n[Plan]\nOncology consult.",
            8: "Under general anesthesia, we performed an EBUS bronchoscopy. We located an enlarged lymph node at station 4R. We took three needle samples from this node. The pathologist in the room confirmed cancer cells were present. We did not sample any other nodes and ended the procedure.",
            9: "Linear EBUS bronchoscopy conducted under general anesthesia. Station 4R was interrogated and sampled three times using a 22-gauge needle. Cytologic analysis confirmed malignancy. No further nodes were aspirated."
        },
        3: { # Note 3: EBUS 3+ Stations + BAL (31653, 31624)
            1: "Proc: EBUS staging + BAL.\nNodes: 4R, 7, 11R (3 stations).\nPasses: 3 per node.\nROSE: 4R/7 Malignant, 11R benign.\nLavage: RLL, sent for micro.\nCondition: Stable.",
            2: "PROCEDURE: Comprehensive mediastinal staging via EBUS-TBNA followed by bronchoalveolar lavage. Systematic ultrasonic evaluation revealed adenopathy at stations 4R, 7, and 11R. Fine needle aspiration was performed at all three stations (3 passes each, 22G). Cytopathology indicated malignancy in the N2 (4R, 7) stations. Subsequently, a bronchoalveolar lavage of the right lower lobe was performed for microbiological analysis.",
            3: "Billing Summary:\n- 31653: EBUS sampling of 3 or more stations (4R, 7, 11R).\n- 31624: Distinct BAL performed in RLL for microbiology.\n- Justification: Comprehensive staging and separate diagnostic lavage performed.",
            4: "Resident Note:\n- Indication: Staging.\n- Stations Sampled: 4R, 7, 11R.\n- Needle: 22G.\n- Results: Ca in 4R/7.\n- Additional: BAL RLL.\n- Complications: None.",
            5: "stging procedure for 71F general anesthesia ebus scope used. sampled 4r then 7 then 11r three passes each. cancer in the mediastinum. then we washed the rll for culture bal fluid looked clear patient woke up ok.",
            6: "Linear EBUS bronchoscopy performed under general anesthesia with ETT. Systematic nodal survey was performed. Enlarged nodes were seen at stations 4R (15 mm), 7 (18 mm), and 11R (10 mm). Using a 22-gauge EBUS needle, three passes were obtained from each of the three stations for a total of nine passes. ROSE showed malignant cells in 4R and 7. A bronchoalveolar lavage was then performed in the right lower lobe for microbiology and cytology.",
            7: "[Indication]\nMediastinal adenopathy, staging.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS-TBNA of 4R, 7, 11R (3 stations). BAL RLL performed. ROSE positive 4R/7.\n[Plan]\nOncology/ID follow up.",
            8: "We performed a complete EBUS staging procedure under general anesthesia. We sampled three distinct lymph node stations: 4R, 7, and 11R. The onsite evaluation showed cancer in the first two. After the staging, we performed a lung wash (BAL) in the right lower lobe to check for infection.",
            9: "Linear EBUS bronchoscopy executed under general anesthesia. Three nodal stations (4R, 7, 11R) were aspirated. ROSE indicated malignancy in 4R and 7. A bronchoalveolar lavage was subsequently conducted in the right lower lobe."
        },
        4: { # Note 4: Stent + Therapeutic Aspiration (31636, 31645)
            1: "Indication: CAO, post-obstructive pneumonia.\nAction:\n- Suctioned copious pus (Therapeutic asp).\n- Balloon dilation.\n- Placed covered metal stent RMS.\nResult: Airway patent. Pus cleared.",
            2: "OPERATIVE REPORT: Management of malignant central airway obstruction. Following rigid and flexible bronchoscopic access, a near-total occlusion of the right mainstem bronchus was visualized. Copious purulent secretions were evacuated via therapeutic aspiration. To restore airway patency, the stricture was dilated, and a self-expanding covered metallic stent was deployed. Post-deployment visualization confirmed restoration of luminal caliber.",
            3: "Coding Logic:\n- 31636: Deployment of bronchial stent (RMS). Includes dilation.\n- 31645: Therapeutic aspiration of tracheobronchial tree. Justified by 'copious purulent secretions' requiring clearance distinct from the stent placement.",
            4: "Procedure Note:\n1. GA/Rigid Bronch.\n2. RMS obstruction identified.\n3. Aggressive suctioning of pus.\n4. Stent deployed (Covered SEMS).\n5. Confirmed expansion.\n6. Pt to ICU.",
            5: "patient with tumor blocking right main bronchus pneumonia cant breathe. we went in cleared out a ton of pus suctioned it all out. dilated the airway put in a metal stent opened it up good flow now patient back to icu on vent.",
            6: "Rigid and flexible bronchoscopy under general anesthesia. A friable intraluminal tumor was seen nearly occluding the right mainstem bronchus. Therapeutic aspiration and suctioning were used to clear copious purulent secretions. Balloon dilation was performed to facilitate stent placement. A covered metallic bronchial stent was deployed across the right mainstem bronchus with good expansion and restoration of lumen.",
            7: "[Indication]\nRight mainstem malignant obstruction, pneumonia.\n[Anesthesia]\nGeneral, Rigid/Flex.\n[Description]\nTherapeutic aspiration of pus. Dilation. Covered stent placement RMS.\n[Plan]\nICU admission.",
            8: "Under general anesthesia, we treated a blockage in the right mainstem bronchus. First, we had to suction out a large amount of infected mucus that was trapped behind the tumor. Once clear, we placed a metal stent to hold the airway open. The stent expanded well and air flow was restored.",
            9: "Rigid and flexible bronchoscopy conducted. Copious purulent secretions were aspirated. A covered metallic stent was positioned in the right mainstem bronchus. Luminal patency was restored."
        },
        5: { # Note 5: BLVR (31647)
            1: "Procedure: BLVR RUL.\nDevice: 4 Zephyr valves.\nTarget: RUL segments.\nResult: Immediate collapse on fluoro. No complications.\nPlan: Admit for observation.",
            2: "OPERATIVE NARRATIVE: Bronchoscopic Lung Volume Reduction. The right upper lobe was selected for treatment of severe emphysema. Inspection confirmed segmental anatomy. Four Zephyr endobronchial valves were deployed into the segmental bronchi of the RUL. Fluoroscopic and bronchoscopic evaluation confirmed appropriate seating and lobar atelectasis. No collateral ventilation assessment was recorded in this session.",
            3: "CPT 31647: Bronchoscopy with placement of valves, initial lobe (RUL).\nDetails: 4 valves placed. No contralateral or additional lobes treated. No separate Chartis code billed (bundled or not performed).",
            4: "Resident Note:\n- Patient: 69F, Emphysema.\n- Procedure: BLVR.\n- Lobe: RUL.\n- Valves: 4 Zephyr.\n- Outcome: Good seating, lobar collapse seen.\n- Disposition: Telemetry.",
            5: "did the valve procedure for emphysema right upper lobe put in 4 valves zephyr brand they fit good fluoro showed the lung going down no pneumothorax right now sending her to the floor.",
            6: "Flexible bronchoscopy under general anesthesia via ETT. The right upper lobe airways were carefully inspected. Four Zephyr endobronchial valves were placed sequentially into segmental bronchi of the right upper lobe using the manufacturer deployment catheter, with good seating and immediate lobar collapse on fluoroscopy. No valves were placed in other lobes.",
            7: "[Indication]\nSevere Emphysema, BLVR candidate.\n[Anesthesia]\nGeneral.\n[Description]\n4 Zephyr valves deployed RUL. Immediate atelectasis noted on fluoro.\n[Plan]\nPneumothorax watch.",
            8: "We performed a lung volume reduction procedure on the right upper lobe. Using the bronchoscope, we placed four one-way valves into the airways of that lobe. We checked with x-ray (fluoroscopy) and saw the lobe collapsing as intended. The patient tolerated it well.",
            9: "Bronchoscopic lung volume reduction executed. Four Zephyr valves were implanted in the right upper lobe. Immediate lobar collapse was observed. No adverse events occurred."
        },
        6: { # Note 6: BLVR Removal + Toilet (31648, 31645)
            1: "Indication: Migrated valves, pneumonia.\nAction: Removed 4 Zephyr valves RUL. Suctioned thick pus/secretions.\nResult: Airways cleared. Valves retrieved.\nPlan: Antibiotics.",
            2: "PROCEDURE: Removal of bronchial valves and therapeutic aspiration. The patient presented with post-obstructive pneumonia. Bronchoscopy revealed migration of the RUL valves. All four Zephyr valves were retrieved using forceps. Extensive airway toileting was then performed to evacuate inspissated, purulent secretions from the RUL and bronchus intermedius, restoring airway hygiene.",
            3: "Coding: 31648 (Removal of valves, initial lobe) + 31645 (Therapeutic aspiration).\nJustification: Removal of failing devices due to migration. Separate significant effort required to clear 'thick, purulent secretions' justifying the additional aspiration code.",
            4: "Procedure Steps:\n1. Inspect RUL.\n2. ID migrated valves.\n3. Remove 4 valves via forceps.\n4. Suction copious pus (toilet).\n5. Extubate.",
            5: "patient had valves in rul now has pneumonia and coughing. went in valves moved. pulled all 4 out. lots of pus behind them suctioned it all out cleaned up the airway admitted for antibiotics.",
            6: "Flexible bronchoscopy under general anesthesia via ETT. Four previously placed Zephyr valves were visualized in the right upper lobe segmental bronchi, with one partially migrated. All four valves were removed using the manufacturer retrieval forceps without complication. Extensive therapeutic aspiration and suctioning were performed to clear thick, purulent secretions from the right upper lobe and bronchus intermedius.",
            7: "[Indication]\nInfected/Migrated RUL valves.\n[Anesthesia]\nGeneral.\n[Description]\nRemoved 4 Zephyr valves. Therapeutic aspiration of purulent secretions performed.\n[Plan]\nIV Antibiotics.",
            8: "The patient returned with infection and valve issues. We went in and removed all four valves from the right upper lobe; one had moved out of place. There was a lot of infected mucus blocked behind them, so we spent time suctioning and cleaning out the airways (therapeutic aspiration).",
            9: "Flexible bronchoscopy with extraction of endobronchial valves. Four Zephyr valves were retrieved from the right upper lobe. Extensive therapeutic aspiration was utilized to clear purulent secretions."
        },
        7: { # Note 7: Thoracentesis (32554)
            1: "Proc: Bedside Thoracentesis.\nSite: Right posterior.\nVolume: 1.5L serous.\nNo imaging code billed (US for marking only).\nComplications: None.",
            2: "PROCEDURE: Diagnostic and therapeutic thoracentesis. The right hemithorax was percussed and imaged with ultrasound for site selection. A catheter was introduced into the pleural space. 1,500 mL of serous fluid was evacuated. The procedure was terminated following symptom relief. Post-procedure ultrasound confirmed lung sliding.",
            3: "CPT 32554: Thoracentesis without imaging guidance code.\nNote: Ultrasound used for marking but report specifies 'No ultrasound guidance code... performed', implying 32554 is the correct billing assignment over 32555.",
            4: "Resident Note:\n- Indication: R pleural effusion.\n- Prep: Chloraprep/Drape.\n- Device: Thoracentesis kit.\n- Fluid: 1500ml serous.\n- Guidance: US for marking.\n- Complications: None.",
            5: "bedside tap right side 60 year old female. used ultrasound to find the spot but didnt save pics. put the needle in drained 1.5 liters yellow fluid patient feels better sending fluid to lab.",
            6: "At the bedside with the patient sitting, the right posterior hemithorax was imaged with ultrasound showing a large anechoic effusion without loculations. After marking an appropriate site, the skin was prepped and draped, and local anesthetic was infiltrated. A single thoracentesis needle and catheter were advanced into the pleural space without complication. Approximately 1,500 mL of serous fluid was removed with symptomatic relief.",
            7: "[Indication]\nSymptomatic R effusion.\n[Anesthesia]\nLocal.\n[Description]\nNeedle thoracentesis. 1500mL removed. US used for marking only.\n[Plan]\nFluid analysis.",
            8: "We performed a bedside procedure to drain fluid from around the right lung. We utilized ultrasound to find a safe spot, but did not perform a billed ultrasound procedure. We successfully drained 1.5 liters of fluid, and the patient's breathing improved immediately.",
            9: "Therapeutic thoracentesis performed. The right posterior hemithorax was accessed. 1,500 mL of serous fluid was aspirated. Ultrasound was employed for localization."
        },
        8: { # Note 8: Tunneled Catheter + Fibrinolytic (32550, 32561)
            1: "Proc: IPC placement + lytics.\nGuidance: US.\nOutput: 800mL serosanguinous.\nMedication: tPA/DNase instilled via catheter.\nDisp: Admitted.",
            2: "OPERATIVE NARRATIVE: Insertion of tunneled pleural catheter with intrapleural fibrinolysis. Under ultrasound guidance, a tunneled indwelling pleural catheter was placed into the loculated right pleural effusion. 800 mL of fluid was drained. To address loculations, a fibrinolytic agent (tPA/DNase) was instilled through the catheter immediately post-placement.",
            3: "Billing: 32550 (Tunneled catheter insert) + 32561 (Lytic agent, initial day).\nRationale: Indwelling catheter placed for chronic/loculated effusion. Lytics administered through this new catheter during the same session.",
            4: "Procedure Note:\n1. US guidance.\n2. Tunnel created.\n3. IPC inserted R chest.\n4. Drained 800cc.\n5. Instilled tPA/DNase.\n6. Cap placed.",
            5: "put in a tunneled catheter for the trapped lung right side ultrasound guidance. drained some fluid like 800 ml. then put in the tpa and dnase to break up the pockets admitted for more doses.",
            6: "Under ultrasound guidance, a right lateral chest wall entry site was selected and anesthetized. A tunneled indwelling pleural catheter with cuff was placed into the largest loculated collection and connected to drainage bottles, with good flow of serosanguinous fluid. Approximately 800 mL was removed at the time of placement. Through the newly placed catheter, a single dose of tPA and DNase was instilled.",
            7: "[Indication]\nLoculated effusion.\n[Anesthesia]\nLocal/Mod.\n[Description]\nTunneled IPC placed right. 800mL output. tPA/DNase instilled.\n[Plan]\nSerial lytics.",
            8: "To manage the complicated fluid collection on the right, we placed a permanent (tunneled) drainage catheter under ultrasound guidance. We drained what we could (800 mL) and then injected medication (tPA/DNase) directly into the chest cavity through the tube to help break up the remaining pockets of fluid.",
            9: "Insertion of indwelling tunneled pleural catheter. 800 mL of serosanguinous fluid was drained. Fibrinolytic agents were instilled via the catheter."
        },
        9: { # Note 9: CT Biopsy + Chest Tube (32408, 32551)
            1: "Proc: CT Biopsy RLL -> Pneumothorax -> Chest tube.\nBiopsy: 18G core x3.\nComplication: Moderate pneumothorax.\nIntervention: Chest tube placed, air evacuated.\nStatus: Admitted.",
            2: "PROCEDURE: Computed Tomography-guided percutaneous lung biopsy complicated by pneumothorax. The target RLL nodule was biopsied using an 18-gauge core needle. Post-procedure imaging revealed a significant pneumothorax. A tube thoracostomy was immediately performed in the right anterior axillary line, connected to a water seal system, effectively evacuating the air.",
            3: "Coding: 32408 (Core biopsy, inc imaging) + 32551 (Tube thoracostomy).\nJustification: Biopsy performed. Iatrogenic pneumothorax occurred requiring separate, distinct chest tube placement for management.",
            4: "Resident Note:\n- Procedure: CT Biobsy RLL.\n- Samples: 3 cores.\n- Event: Pt developed SOB/pain.\n- Finding: Pneumothorax on scan.\n- Action: Chest tube placed, bubbling confirmed.\n- Plan: Admit.",
            5: "ct guided biopsy of the nodule right lower lobe took some cores patient got short of breath right after scan showed pneumothorax. put in a chest tube hooked it up to the box air leak seen admitted for observation.",
            6: "CT-guided percutaneous core needle biopsy of the right lower lobe nodule was performed in the prone position. Multiple 18-gauge core samples were obtained. Immediately after the biopsy, the patient developed dyspnea and right-sided pleuritic chest pain. CT and bedside ultrasound confirmed a moderate right pneumothorax. A large-bore chest tube was placed in the right anterior axillary line, connected to a water seal drainage system.",
            7: "[Indication]\nRLL Nodule.\n[Description]\nCT-guided core biopsy (32408). Complicated by Pneumothorax. Chest tube placed (32551).\n[Plan]\nChest tube management.",
            8: "We performed a needle biopsy of a nodule in the right lower lung using CT guidance. Unfortunately, the lung collapsed (pneumothorax) during the procedure. To treat this, we inserted a chest tube between the ribs to re-expand the lung. The air leak was controlled, and the patient was admitted.",
            9: "Percutaneous core needle biopsy of the right lower lobe performed. The procedure was complicated by a pneumothorax. A tube thoracostomy was executed to manage the complication."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns base data for randomization based on the notes in part 043.
    """
    return [
        {"idx": 0, "orig_name": "SYNB001", "orig_age": 68, "names": ["Alice Vance", "Bertha Higgins", "Clara Kinsley", "Doris O'Connor", "Evelyn Miller", "Florence Stone", "Grace Davis", "Helen Clark", "Irene Wright"]},
        {"idx": 1, "orig_name": "SYNB002", "orig_age": 45, "names": ["John Jenkins", "Kevin Carter", "Liam Hughes", "Mike Smith", "Noah Lopez", "Oscar Davidson", "Peter White", "Quinn Lewis", "Robert King"]},
        {"idx": 2, "orig_name": "SYNB003", "orig_age": 62, "names": ["Steve Foster", "Tim Turner", "Ursula Myers", "Victor Anderson", "Walter Mitchell", "Xander Reynolds", "Yusuf Baker", "Zachary Roberts", "Adam Phillips"]},
        {"idx": 3, "orig_name": "SYNB004", "orig_age": 71, "names": ["Betty Hall", "Carol Campbell", "Diana Allen", "Elaine Young", "Fiona Hernandez", "Gina King", "Holly Wright", "Iris Scott", "Judy Allen"]},
        {"idx": 4, "orig_name": "SYNB005", "orig_age": 64, "names": ["Brian Hill", "Carl Lewis", "David Scott", "Eric Simmons", "Frank Edwards", "Greg Thompson", "Henry Garcia", "Ian Martinez", "Jack Robinson"]},
        {"idx": 5, "orig_name": "SYNB006", "orig_age": 69, "names": ["Karen Adams", "Lisa Nelson", "Mona Carter", "Nina Mitchell", "Olivia Roberts", "Paula Phillips", "Quinn Campbell", "Rachel Evans", "Sara Carter"]},
        {"idx": 6, "orig_name": "SYNB007", "orig_age": 72, "names": ["Tom Mitchell", "Ulysses Reed", "Vince Roberts", "Will Smith", "Xavier Jones", "Yanni Brown", "Zane Miller", "Arthur Davis", "Ben Wilson"]},
        {"idx": 7, "orig_name": "SYNB008", "orig_age": 60, "names": ["Cathy Taylor", "Debra Anderson", "Elena Thomas", "Fran Jackson", "Gail White", "Hannah Harris", "Ivy Martin", "Jane Thompson", "Kelly Garcia"]},
        {"idx": 8, "orig_name": "SYNB009", "orig_age": 66, "names": ["Larry Martinez", "Mark Robinson", "Nathan Clark", "Oliver Rodriguez", "Paul Lewis", "Quincy Lee", "Ray Walker", "Sam Hall", "Ted Allen"]},
        {"idx": 9, "orig_name": "SYNB010", "orig_age": 63, "names": ["Mary Young", "Nancy Hernandez", "Ophelia King", "Patty Wright", "Queen Scott", "Rose Green", "Sally Baker", "Tina Adams", "Uma Nelson"]}
    ]

def main():
    # Load original data from source file
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through each original note in source data
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
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
            # If a variation is missing, fallback to original
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
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

    # Output to JSON
    output_filename = output_dir / "synthetic_notes_part_043.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()