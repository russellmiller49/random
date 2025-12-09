import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_020.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock names for the 10 patients in the source file.
    Indexes 0-9 correspond to the notes in consolidated_verified_notes_v2_8_part_020.json
    """
    return [
        # Note 0: David Brown (EMN LUL)
        {"idx": 0, "orig_age": 59, "names": ["James Miller", "Robert Chen", "William Baker", "Thomas Clark", "David Wilson", "Richard Lee", "Joseph Hall", "Charles Allen", "Christopher Young"]},
        # Note 1: Angela White (Robotic RML + Pneumo)
        {"idx": 1, "orig_age": 63, "names": ["Patricia Davis", "Linda Martinez", "Barbara Taylor", "Elizabeth Anderson", "Jennifer White", "Maria Garcia", "Susan Robinson", "Margaret Wright", "Dorothy King"]},
        # Note 2: Michael Green (Rigid Tracheal Stent)
        {"idx": 2, "orig_age": 72, "names": ["John Scott", "James Green", "Robert Adams", "Michael Nelson", "William Hill", "David Carter", "Richard Mitchell", "Joseph Perez", "Thomas Roberts"]},
        # Note 3: Linda Davis (Rigid LMS Stent)
        {"idx": 3, "orig_age": 69, "names": ["Mary Turner", "Patricia Phillips", "Linda Campbell", "Barbara Parker", "Elizabeth Evans", "Jennifer Edwards", "Maria Collins", "Susan Stewart", "Margaret Sanchez"]},
        # Note 4: Samuel Ortiz (Flex Cryo RMS)
        {"idx": 4, "orig_age": 55, "names": ["Charles Morris", "Christopher Rogers", "Daniel Reed", "Matthew Cook", "Anthony Morgan", "Donald Bell", "Mark Murphy", "Paul Bailey", "Steven Rivera"]},
        # Note 5: Karen Young (BLVR LUL Zephyr)
        {"idx": 5, "orig_age": 68, "names": ["Nancy Cooper", "Karen Richardson", "Lisa Cox", "Betty Howard", "Helen Ward", "Sandra Torres", "Donna Peterson", "Carol Gray", "Ruth Ramirez"]},
        # Note 6: Thomas Baker (BLVR RUL Spiration)
        {"idx": 6, "orig_age": 61, "names": ["George James", "Kenneth Watson", "Andrew Brooks", "Edward Kelly", "Joshua Sanders", "Brian Price", "Kevin Bennett", "Ronald Wood", "Timothy Barnes"]},
        # Note 7: Emily Rogers (BLVR LLL Zephyr)
        {"idx": 7, "orig_age": 70, "names": ["Sharon Ross", "Michelle Henderson", "Laura Coleman", "Sarah Jenkins", "Kimberly Perry", "Deborah Powell", "Jessica Long", "Shirley Patterson", "Cynthia Hughes"]},
        # Note 8: Brian Scott (WLL Left)
        {"idx": 8, "orig_age": 42, "names": ["Jason Flores", "Jeffrey Washington", "Ryan Butler", "Jacob Simmons", "Gary Foster", "Nicholas Gonzales", "Eric Bryant", "Stephen Alexander", "Larry Russell"]},
        # Note 9: Olivia Perez (WLL Right)
        {"idx": 9, "orig_age": 37, "names": ["Melissa Griffin", "Brenda Diaz", "Amy Hayes", "Anna Myers", "Rebecca Ford", "Virginia Hamilton", "Kathleen Graham", "Pamela Sullivan", "Martha Wallace"]}
    ]

def get_variations():
    """
    Contains the 9 stylistic variations for each of the 10 notes in Part 020.
    """
    variations = {
        0: { # David Brown: EMN/Radial EBUS LUL
            1: "Procedure: EMN bronchoscopy LUL.\n- SuperDimension nav used.\n- Radial EBUS: eccentric view.\n- 5 forceps biopsies, 2 brushes taken.\n- Fluoroscopy confirmed tool position.\n- Complications: Minor bleeding, stopped w/ ice/epi.\n- Plan: Discharge home.",
            2: "Operative Report: The patient underwent electromagnetic navigation bronchoscopy utilizing the SuperDimension system. A 22 mm nodule in the left upper lobe was targeted. CT-to-body divergence was minimal (4 mm). Radial endobronchial ultrasound interrogation revealed an eccentric signature consistent with a solid lesion. Transbronchial sampling was performed via forceps and cytology brush under fluoroscopic guidance. Rapid on-site evaluation was suspicious for malignancy.",
            3: "Coding Data: Bronchoscopy with EMN (31627) and Radial EBUS (31654). Diagnostic transbronchial biopsy (31628) performed on a single lesion in the Left Upper Lobe. Navigation required for peripheral access; registration error 4mm. Fluoroscopic guidance utilized. ROSE services utilized.",
            4: "Resident Procedure Note\nAttending: Dr. Hart\nPt: 59M, LUL nodule.\n1. Time out.\n2. EMN mapping (SuperDimension).\n3. Navigated to LUL target.\n4. REBUS showed eccentric view.\n5. Biopsies x5 and brush x2 obtained.\n6. ROSE: Suspicious.\n7. Pt tolerated well, reversed w/ Naloxone.",
            5: "we did the nav bronch on mr brown today for that lul spot using superdimension it went okay registration was like 4mm off. radial ebus showed the lesion eccentric view took 5 bites with forceps and 2 brushes rose guy said it looked bad maybe cancer. little bit of bleeding used ice saline. had to give naloxone at the end cause he was sleepy.",
            6: "Electromagnetic navigational bronchoscopy with radial EBUS and fluoroscopic guidance was performed for a left upper lobe nodule. The SuperDimension platform was used with CT-based planning. Registration error was 4 mm. Radial EBUS showed an eccentric view of the solid lesion. Five forceps biopsies and two brushings were performed. Minor bleeding was controlled with iced saline. ROSE was suspicious for malignancy. The patient was reversed with Naloxone and discharged.",
            7: "[Indication]\n22 mm PET-avid LUL nodule.\n[Anesthesia]\nModerate sedation (Versed/Fentanyl).\n[Description]\nSuperDimension EMN used to navigate to LUL. Radial EBUS: Eccentric view. Fluoroscopy confirmed position. 5 TBBx and 2 brushes collected. ROSE positive for atypia.\n[Plan]\nDischarge. Follow up Oncology.",
            8: "The patient was brought to the bronchoscopy suite for evaluation of a left upper lobe nodule. After inducing moderate sedation, the SuperDimension electromagnetic navigation system was employed to reach the target. We obtained an eccentric view on radial EBUS. Subsequently, five forceps biopsies and two brushings were taken under fluoroscopic visualization. Although there was minor bleeding, it was easily controlled. Preliminary pathology suggests malignancy.",
            9: "Technique: Electromagnetic guidance with radial ultrasound for sampling of a LUL mass.\nSubject: 59-year-old male.\nDetails: Navigated to the lesion using SuperDimension. Acquired an eccentric ultrasound signal. Harvested 5 tissue samples and 2 brushings. Bleeding was halted with vasoconstrictors. Pathology indicates carcinoma."
        },
        1: { # Angela White: Robotic RML + Pneumothorax
            1: "Procedure: Robotic bronch (Monarch) RML nodule.\n- Radial EBUS: concentric.\n- Cryobiopsy x4, Forceps x4.\n- ROSE: Adenocarcinoma.\n- Complication: Pneumothorax.\n- Action: Pigtail chest tube placed.\n- Plan: Admit for chest tube management.",
            2: "Procedural Narrative: The patient underwent Monarch robotic-assisted bronchoscopy targeting a 14 mm RML lesion. Upon navigation, a concentric radial EBUS view was achieved. Confirmatory cone-beam CT verified tool-in-lesion status. Sampling via cryoprobe and forceps yielded tissue consistent with metastatic adenocarcinoma. Post-procedural imaging revealed a right apical pneumothorax, necessitating the insertion of a pigtail catheter connected to water seal.",
            3: "Billable Services: 31627 (Nav), 31654 (REBUS), 31629 (Robotic/Nav Biopsy), 31645 (Cryobiopsy initial lobe). Target: RML. Modality: Robotic Bronchoscopy with Cone Beam CT. Complication managed: Chest tube placement (separate service). Diagnosis: Malignant neoplasm.",
            4: "Procedure: Robotic Bronchoscopy (RML)\nSteps:\n1. General Anesthesia.\n2. Monarch robot navigated to RML.\n3. REBUS concentric view.\n4. Cone beam CT spin.\n5. 4 cryo biopsies, 4 forceps biopsies.\n6. Complication: Pneumothorax on post-op film. Pigtail placed.\nPlan: Admit to floor.",
            5: "procedure note for angela white we used the monarch robot to get to that rml nodule 14mm. radial ebus was concentric which is good. did cone beam to check. took 4 cryo and 4 forceps biopsies rose looks like adeno. unfortunately she popped a lung small pneumo so we put in a pigtail chest tube. admitting her for observation.",
            6: "Monarch robotic-assisted navigational bronchoscopy with radial EBUS, cryobiopsy, and forceps biopsies of a right middle lobe nodule was performed. The patient is a 63-year-old female. Navigation to the RML was successful with a concentric REBUS view. Cone-beam CT confirmed tool-in-lesion. Sampling with cryoprobe and forceps was performed. A small right apical pneumothorax was noted post-procedure requiring pigtail chest tube placement. The patient was admitted.",
            7: "[Indication]\n14 mm PET-avid RML nodule.\n[Anesthesia]\nGeneral endotracheal anesthesia.\n[Description]\nMonarch robotic navigation to RML. REBUS concentric. CBCT confirmation. Cryobiopsy x4 and Forceps x4 performed. Diagnosis: Adenocarcinoma.\n[Complication]\nPneumothorax requiring chest tube.\n[Plan]\nAdmit to telemetry.",
            8: "Under general anesthesia, we utilized the Monarch robotic platform to navigate to a nodule in the right middle lobe. A concentric view was visualized on radial EBUS, and placement was verified via cone-beam CT. We proceeded to take four cryobiopsies and four standard forceps biopsies. While bleeding was mild, a post-procedure chest x-ray revealed a pneumothorax. A pigtail chest tube was inserted without difficulty, and the patient was admitted for monitoring.",
            9: "Operation: Robotic-guided sampling of RML mass.\nTechnique: Utilized Monarch system. Validated location with cone-beam imaging. Extracted tissue using cryoprobe and forceps. \nAdverse Event: Lung collapse (pneumothorax) detected subsequently; managed via thoracic catheter insertion.\nOutcome: Tissue analysis indicates malignancy."
        },
        2: { # Michael Green: Rigid Tracheal Stent
            1: "Procedure: Rigid bronch, debulking, stenting.\n- Lesion: Distal trachea/carina (90% occlusion).\n- Action: Mechanical coring, APC.\n- Stent: 14x50mm Silicone (Dumon) Y-stent equivalent placement.\n- Result: <10% residual obstruction.\n- Plan: Keep intubated, ICU.",
            2: "Operative Summary: The patient presented with critical central airway obstruction due to a distal tracheal tumor involving the carina. Rigid bronchoscopy (size 12) was employed. The exophytic mass was mechanically debrided and cauterized with Argon Plasma Coagulation. Following recanalization, a 14 x 50 mm silicone straight stent was deployed to maintain patency across the carinal involvements. The patient was transferred to the ICU intubated.",
            3: "Codes: 31641 (Tumor destruction/debulking), 31631 (Tracheal stent), 31636 (Bronchial stent - Y stent extension). Indication: Malignant central airway obstruction (90%). Technique: Rigid bronchoscopy with mechanical coring and APC. Device: Silicone stent spanning trachea and mainstem.",
            4: "Resident Note: Rigid Bronchoscopy\nIndication: Tracheal tumor.\n1. Induction GA, Rigid #12 inserted.\n2. Mass at distal trachea/carina coring out.\n3. APC used for hemostasis.\n4. Silicone stent 14x50mm placed.\n5. Airway patent at end.\nPlan: ICU, mechanical ventilation.",
            5: "rigid bronch on mr green for that big tracheal tumor choking him off. we cored it out with the barrel and used some apc. bleeding was about 50cc. put in a silicone stent 14 by 50 to keep it open. blood pressure dropped a bit on induction but he's fine now. sending to icu still on the vent.",
            6: "Rigid bronchoscopy with mechanical debulking, Argon plasma coagulation, and Silicone stent placement was performed for a 72-year-old male with distal tracheal tumor. There was 90 percent obstruction. Mechanical coring and APC reduced obstruction to less than 10 percent. A 14 x 50 mm silicone stent was placed. Transient hypotension occurred during induction. The patient remained intubated and was transferred to the ICU.",
            7: "[Indication]\nCritical central airway obstruction (Trachea/Carina).\n[Anesthesia]\nGeneral, Rigid Bronchoscope #12.\n[Description]\nMechanical debulking and APC of exophytic tumor. 14x50mm Silicone stent deployed.\n[Plan]\nICU admission, remain intubated.",
            8: "We performed a therapeutic rigid bronchoscopy to relieve a 90% obstruction in the distal trachea and carina. Using the rigid barrel, we mechanically cored out the tumor and applied argon plasma coagulation to the base. Once the airway was patent, we deployed a 14 x 50 mm silicone stent to bridge the distal trachea and main carina. The patient tolerated the procedure with only transient hypotension and was transferred to the ICU for ongoing care.",
            9: "Intervention: Rigid airway recanalization and stenting.\nTarget: Distal tracheal malignancy.\nMethod: Physical debulking via rigid scope and thermal ablation (APC). Implanted a silicone prosthesis (14x50mm).\nResult: Luminal patency restored. \nDisposition: Critical care unit."
        },
        3: { # Linda Davis: Rigid LMS Stent
            1: "Procedure: Rigid bronch, LMS debulking, SEMS placement.\n- Findings: LMS 100% occluded by tumor.\n- Action: Mechanical debulking + APC.\n- Stent: 12x40mm Covered SEMS in LMS.\n- Result: Lung re-expanded.\n- Plan: PACU, extubated.",
            2: "Procedure Note: Ms. Davis underwent rigid bronchoscopy for a complete malignant obstruction of the left mainstem bronchus. The lesion was friable and occlusive. Mechanical recanalization was achieved via the rigid barrel and forceps, supplemented by APC. To prevent restenosis, a 12 x 40 mm covered self-expanding metallic stent (SEMS) was deployed under fluoroscopic guidance. Post-operative imaging confirmed left lung re-expansion.",
            3: "Billing: 31641 (Destruction of tumor), 31636 (Stent placement, bronchial). Location: Left Mainstem Bronchus. Devices: Covered SEMS 12x40mm. Technique: Rigid bronchoscopy with jet ventilation. Fluoroscopy utilized for stent deployment.",
            4: "Procedure: Rigid Bronchoscopy w/ Stent\nPt: Linda Davis, 69F.\n1. Rigid scope #11 passed.\n2. LMS completely blocked.\n3. Debulked with suction/forceps/APC.\n4. 12x40mm covered metal stent placed.\n5. CXR shows lung up.\nPlan: PACU, nasal cannula.",
            5: "dictation for linda davis rigid bronch she had that left lung collapse from the tumor in the left main. we opened it up with the rigid scope and apc. put in a metal stent covered 12 by 40. bleeding was minimal. she woke up fine extubated her. xray looks good lung is up.",
            6: "Rigid bronchoscopy with tumor debulking and placement of covered metallic stent in the left mainstem bronchus was performed. The patient had complete collapse of the left lung. Mechanical debulking and APC were used to open the lumen. A 12 x 40 mm covered self-expanding metallic stent was deployed. EBL was 30 mL. The patient was extubated and transferred to PACU.",
            7: "[Indication]\nLeft lung collapse, malignant LMS obstruction.\n[Anesthesia]\nGeneral, Rigid #11, Jet ventilation.\n[Description]\nTumor debulked from LMS. 12x40mm Covered SEMS deployed. Patent airway achieved.\n[Plan]\nPACU, monitor O2 sats.",
            8: "Due to complete collapse of the left lung from a malignant obstruction, we performed a rigid bronchoscopy. We mechanically debulked the tumor in the left mainstem bronchus and applied APC to the base. Once the airway was sufficiently open, we placed a 12 x 40 mm covered metallic stent under fluoroscopic guidance. The patient was extubated in the OR, and immediate chest x-ray showed successful re-expansion of the lung.",
            9: "Service: Rigid airway restoration and prosthesis insertion.\nSite: Left mainstem bronchus.\nTechnique: Tumor excision via rigid barrel and thermal coagulation. Insertion of covered metallic scaffold (SEMS).\nOutcome: Re-aeration of the left lung."
        },
        4: { # Samuel Ortiz: Flex Cryo RMS
            1: "Procedure: Flex bronch, cryo-debulking RMS.\n- Finding: 70% obstruction RMS.\n- Action: Cryoprobe activation x multiple. Mechanical removal.\n- Result: 20% residual.\n- Complication: Mild ooze.\n- Plan: Discharge home.",
            2: "Operative Note: Mr. Ortiz presented with a polypoid tumor obstructing the right mainstem bronchus. Flexible bronchoscopy was initiated. The cryotherapy probe was utilized to perform cryoadhesion and extraction of tumor tissue. This was supplemented by mechanical debridement. The airway caliber was significantly improved from 70% to 20% obstruction. Hemostasis was secured with epinephrine.",
            3: "Coding: 31641 (Tumor destruction, flexible). Note: No stent placed. Technique involved cryotherapy probe for debulking of malignant endobronchial lesion in Right Mainstem. Mechanical forceps used for residual cleanup.",
            4: "Resident Procedure Note\nProcedure: Flex Bronch w/ Cryo\n1. Moderate sedation.\n2. RMS tumor seen (70% blocked).\n3. Cryo probe used to debulk.\n4. Forceps used for cleanup.\n5. Airway now patent.\nPlan: Home today.",
            5: "we did a flex bronch on mr ortiz for that tumor in the right mainstem. used the cryo probe to freeze and pull chunks of it out. got it pretty open maybe 20 percent left. little bit of bleeding used some cold saline. he is going home today.",
            6: "Flexible bronchoscopy with cryotherapy and mechanical debulking for endobronchial tumor was performed. Findings included a polypoid tumor in the right mainstem bronchus causing 70 percent obstruction. Multiple cycles of cryotherapy were applied. Residual obstruction was 20 percent. Mild oozing was controlled. The patient was discharged home.",
            7: "[Indication]\nSymptomatic RMS obstruction (Tumor).\n[Anesthesia]\nModerate Sedation.\n[Description]\nFlexible cryoprobe used to debulk RMS mass. Forceps used for residual. Obstruction reduced from 70% to 20%.\n[Plan]\nDischarge to home.",
            8: "We performed a flexible bronchoscopy to address a tumor obstructing the right mainstem bronchus. Using a cryoprobe, we performed multiple freeze-thaw cycles to adhere to and remove significant portions of the tumor. We cleared the remaining debris with forceps. The airway obstruction was reduced from 70% to approximately 20%. The patient tolerated the procedure well and will be discharged.",
            9: "Procedure: Flexible airway clearance via cryo-ablation.\nTarget: Right mainstem neoplasm.\nAction: Utilized cryo-adhesion to extract tumor tissue. Mechanical removal of debris.\nResult: Restoration of airway patency."
        },
        5: { # Karen Young: BLVR LUL Zephyr
            1: "Procedure: BLVR LUL (Zephyr).\n- Chartis: No CV.\n- Implants: 3 Zephyr valves (LB1+2, LB3).\n- Result: Good seal, no pneumo.\n- Plan: Admit, CXR protocol.",
            2: "Procedure Note: Ms. Young, a candidate for lung volume reduction, underwent flexible bronchoscopy. The left upper lobe was targeted. Chartis assessment confirmed the absence of collateral ventilation. Subsequently, three Zephyr endobronchial valves were deployed into the LB1+2 and LB3 segments. Visual inspection confirmed appropriate seating and occlusion. There were no immediate complications.",
            3: "Billing: 31647 (Initial lobe BLVR), 31651 (Addl segments). Device: Zephyr Valves x3. Location: LUL. Indication: Severe Emphysema. Diagnostic: Chartis assessment (bundled). Disposition: Inpatient observation.",
            4: "Resident Note: BLVR LUL\n1. GA, 8.0 ETT.\n2. Chartis check LUL -> Negative CV.\n3. Placed 3 Zephyr valves (LB1+2, LB3).\n4. Checked for leaks - none.\n5. CXR negative for pneumo.\nPlan: Admit for obs.",
            5: "procedure note for karen young blvr lul. we checked with chartis and it looked good no flow. put in three zephyr valves in the upper lobe segments. everything looks sealed up. no pneumothorax on the xray. admitting her to the floor.",
            6: "Bronchoscopic lung volume reduction with Zephyr endobronchial valves to the left upper lobe was performed. The target was selected based on CT fissure analysis. Chartis confirmed absence of collateral ventilation. Three Zephyr valves were placed in LUL segments. There were no complications. The patient was admitted for observation.",
            7: "[Indication]\nSevere LUL Emphysema.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nChartis negative for CV. 3 Zephyr valves deployed in LUL. Good occlusion.\n[Plan]\nAdmit, serial CXRs.",
            8: "We proceeded with bronchoscopic lung volume reduction targeting the left upper lobe. After inducing general anesthesia, we used the Chartis system to confirm there was no collateral ventilation in the target lobe. We then placed three Zephyr valves into the LB1+2 and LB3 segments. The valves were well-seated with no air leak. The patient was extubated and admitted for routine post-BLVR monitoring.",
            9: "Operation: Endobronchial valve implantation (Zephyr) for volume reduction.\nSite: Left Upper Lobe.\nDetails: Verified lobar isolation via Chartis. Deployed 3 valves. Confirmed occlusion.\nOutcome: Uncomplicated."
        },
        6: { # Thomas Baker: BLVR RUL Spiration
            1: "Procedure: BLVR RUL (Spiration).\n- Analysis: CT fissure only (No Chartis).\n- Implants: 2 Spiration valves (RB1, RB2+3).\n- Result: Good collapse.\n- Plan: Admit, CXR.",
            2: "Operative Report: Mr. Baker underwent bronchoscopic lung volume reduction targeting the Right Upper Lobe. Target selection was based on radiographic fissure integrity; physiologic mapping was not performed. Two Spiration valves were deployed into the apical (RB1) and posterior/anterior (RB2+3) segments. Bronchoscopic evaluation demonstrated effective airway occlusion and distal collapse.",
            3: "Coding: 31647 (Initial lobe). Note: Only 2 valves placed in RUL. Device: Spiration (Olympus). Assessment: Anatomic (CT) only. Anesthesia: MAC. Disposition: Floor admission.",
            4: "Procedure: BLVR RUL\n1. MAC sedation.\n2. Navigated to RUL.\n3. Placed 2 Spiration valves (RB1, RB2+3).\n4. Confirmed position.\n5. No pneumo.\nPlan: Admit.",
            5: "blvr procedure for mr baker using spiration valves. target was rul based on the cat scan. didn't do chartis. put in two valves one in the apical one in the other segments. looks like the lung collapsed down nicely. sending him to the floor.",
            6: "Bronchoscopic lung volume reduction using Spiration valves targeting the right upper lobe was performed. The patient is a 61-year-old male with RUL-predominant emphysema. Two Spiration valves were placed in RUL segments RB1 and RB2+3. There was good collapse of RUL airways. No immediate pneumothorax was noted. The patient was admitted.",
            7: "[Indication]\nRUL Emphysema.\n[Anesthesia]\nMAC.\n[Description]\n2 Spiration valves deployed in RUL (RB1, RB2+3). Good lobar collapse observed.\n[Plan]\nAdmit for observation.",
            8: "We performed lung volume reduction on Mr. Baker using Spiration valves in the right upper lobe. We relied on CT analysis for target selection. Under MAC sedation, we placed two valves into the segmental bronchi of the RUL. Immediate bronchoscopic inspection showed good collapse of the distal airways. He was admitted for overnight observation to monitor for pneumothorax.",
            9: "Procedure: Implantation of Spiration valves for emphysema.\nLocation: Right Upper Lobe.\nAction: Deployed 2 valves into segmental airways. \nResult: Observed airway collapse. \nPlan: Inpatient monitoring."
        },
        7: { # Emily Rogers: BLVR LLL Zephyr
            1: "Procedure: BLVR LLL (Zephyr).\n- Chartis: Low/Borderline flow.\n- Implants: 2 Zephyr valves.\n- Complication: Transient desat (86%).\n- Plan: Admit, monitor closely.",
            2: "Procedure Note: Ms. Rogers underwent BLVR targeting the Left Lower Lobe. Chartis assessment revealed low but persistent airflow, indicative of borderline collateral ventilation; however, the decision was made to proceed. Two Zephyr valves were deployed. Although there was a transient desaturation event, it resolved with oxygen therapy. Valve seating appeared adequate.",
            3: "Billing: 31647 (Initial), 31651 (Addl). Device: Zephyr. Location: LLL. Indication: Heterogeneous Emphysema. Note: Borderline CV status noted. Complication: Hypoxia (transient).",
            4: "Resident Note: BLVR LLL\n1. GA / ETT.\n2. Chartis LLL -> Borderline.\n3. Decided to place valves (x2 Zephyr).\n4. Pt desatted to 86%, fixed with FiO2.\n5. No pneumo on CXR.\nPlan: Admit.",
            5: "emily rogers for blvr lll. chartis was a bit iffy showed some flow but we went ahead. put in two zephyr valves. she dropped her sats to 86 for a minute but came back up. valves look good. admitting her to telemetry.",
            6: "Bronchoscopic lung volume reduction with Zephyr valves to the left lower lobe was performed. Chartis showed low but persistent airflow. Two Zephyr valves were placed in LLL segments. Transient desaturation to 86 percent occurred but was corrected. There was no pneumothorax on immediate CXR. The patient was admitted to a monitored bed.",
            7: "[Indication]\nLLL Emphysema.\n[Anesthesia]\nGeneral.\n[Description]\nChartis: Borderline CV. 2 Zephyr valves deployed in LLL. Transient desaturation managed with O2.\n[Plan]\nAdmit to monitor.",
            8: "Ms. Rogers underwent a BLVR procedure for her left lower lobe emphysema. The Chartis assessment was equivocal, showing some low collateral flow, but we proceeded with valve placement. Two Zephyr valves were implanted in the LLL. The patient experienced a brief period of desaturation which resolved quickly with increased oxygen. We admitted her to a monitored bed out of an abundance of caution.",
            9: "Intervention: Endobronchial valve placement (Zephyr).\nTarget: Left Lower Lobe.\nDetails: Collateral ventilation assessment was borderline. Implanted 2 valves. Managed transient hypoxia.\nDisposition: Inpatient admission."
        },
        8: { # Brian Scott: WLL Left
            1: "Procedure: Whole Lung Lavage (Left).\n- Indication: PAP.\n- Method: DLT, 30L warm saline in, 25L out.\n- Findings: Milky effluent cleared over time.\n- Complication: Hypotension (pressors).\n- Plan: ICU, intubated.",
            2: "Operative Report: Mr. Scott, diagnosed with pulmonary alveolar proteinosis, underwent therapeutic whole lung lavage of the left lung. A double-lumen endotracheal tube was utilized for isolation. We instilled a total of 30 liters of warmed saline in aliquots, retrieving 25 liters. The effluent transitioned from opaque/milky to clear. Hemodynamics were supported with vasopressors during the procedure. The patient was transferred to the ICU intubated.",
            3: "Coding: 32997 (Total lung lavage, unilateral). Side: Left. Volume: 30L instilled. Method: General Anesthesia w/ DLT. Note: This is a therapeutic lavage for PAP, not a diagnostic BAL.",
            4: "Resident Note: WLL Left\n1. 37Fr DLT placed.\n2. Isolated Left lung.\n3. Lavaged with 30L total.\n4. Fluid cleared up nicely.\n5. BP dropped, gave pressors.\nPlan: ICU.",
            5: "doing a whole lung lavage on brian scott for his pap. left side today. put in a dlt. ran about 30 liters of saline through him got 25 back. looked like milk at first then clear. blood pressure got soft so anesthesia gave him some pressors. going to the icu intubated.",
            6: "Whole lung lavage of the left lung for pulmonary alveolar proteinosis was performed. 30 L of warm saline was instilled and 25 L returned. The effluent cleared progressively. Transient hypotension was treated with vasopressors. The patient remained intubated and was transported to the ICU.",
            7: "[Indication]\nPulmonary Alveolar Proteinosis.\n[Anesthesia]\nGA, DLT.\n[Description]\nLeft lung lavage. 30L In / 25L Out. Effluent cleared.\n[Complication]\nHypotension (managed).\n[Plan]\nICU, mech vent.",
            8: "We performed a therapeutic whole lung lavage on the left lung for Mr. Scott's alveolar proteinosis. Using a double-lumen tube, we ventilated the right lung while lavaging the left with 30 liters of warm saline. The return fluid (25L total) cleared significantly by the end. He experienced some hypotension which was managed by anesthesia. He remains intubated for transport to the ICU.",
            9: "Procedure: Total pulmonary lavage (Left).\nIndication: Autoimmune PAP.\nTechnique: Large volume saline instillation (30L) via double-lumen airway.\nResult: Clearance of proteinaceous material.\nStatus: ICU care."
        },
        9: { # Olivia Perez: WLL Right
            1: "Procedure: Whole Lung Lavage (Right).\n- Context: Post-Left WLL 2 wks ago.\n- Method: DLT, 36L in, 30L out.\n- Complication: Desat to 80s, resolved with pause.\n- Plan: Extubated, ICU monitoring.",
            2: "Procedure Note: Ms. Perez returned for the second stage of her treatment for PAP, undergoing right whole lung lavage. A double-lumen tube was placed. The right lung was lavaged with 36 liters of saline, yielding 30 liters of effluent which cleared progressively. A desaturation event occurred during a dwell cycle but resolved with recruitment maneuvers. She was successfully extubated and transferred to the ICU.",
            3: "Coding: 32997 (Total lung lavage, unilateral). Side: Right. Volume: 36L instilled. History: Previous Left WLL 2 weeks prior (separate session). Outcome: Extubated in OR.",
            4: "Procedure: Right Lung Lavage\n1. DLT placed (35Fr).\n2. Lavaged Right lung (36L total).\n3. 30L returned.\n4. Sats dropped to 80s once, paused and recruited.\n5. Extubated.\nPlan: ICU on high-flow.",
            5: "right side lung lavage for olivia perez. she had the left done last week. used a dlt. put in 36 liters got 30 back. she desatted a bit to the 80s but we fixed it. extubated her at the end. sending to icu on high flow.",
            6: "Whole lung lavage of the right lung was performed for pulmonary alveolar proteinosis. The patient is status post left lung lavage. 36 L of saline was instilled with 30 L return. Brief desaturation occurred but improved with recruitment. The patient was extubated in the OR and transported to the ICU.",
            7: "[Indication]\nPAP, Right side.\n[Anesthesia]\nGA, DLT.\n[Description]\nRight lung lavage. 36L In / 30L Out. Cleared secretions.\n[Complication]\nTransient hypoxia.\n[Plan]\nExtubate, ICU.",
            8: "Ms. Perez underwent the planned right-sided whole lung lavage today. We used a double-lumen tube to isolate the lung and instilled 36 liters of saline, recovering 30 liters. The fluid cleared as expected. She had one episode of desaturation that required us to pause and recruit the lung, but she recovered well. We were able to extubate her in the operating room before transfer to the ICU.",
            9: "Procedure: Total pulmonary lavage (Right).\nIndication: Alveolar proteinosis.\nAction: Instilled 36L saline. Recovered 30L. \nAdverse Event: Transient hypoxemia.\nDisposition: Extubated, critical care monitoring."
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
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update text in registry entry as well to match
                if "note_text" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["note_text"] = note_entry["note_text"]

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
    output_filename = output_dir / "synthetic_blvr_notes_part_020.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()