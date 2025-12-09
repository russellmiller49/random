import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_012.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILE = "synthetic_notes_part_012.json"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Defines the base patient data (Index, Original Name, Original Age) 
    and provides 9 mock names for the variations.
    """
    return [
        {
            "idx": 0, 
            "orig_name": "Maria G. Rodriguez", 
            "orig_age": 70, 
            "names": ["Elena Vasquez", "Carmen Ortiz", "Sofia Ramirez", "Isabella Torres", "Lucia Morales", "Valentina Castillo", "Camila Reyes", "Martina Flores", "Gabriela Diaz"]
        },
        {
            "idx": 1, 
            "orig_name": "Timothy R. Brooks", 
            "orig_age": 72, 
            "names": ["Robert Hayes", "William Turner", "James Sterling", "Richard Coleman", "Edward Gibson", "Charles Porter", "Thomas Mitchell", "Joseph Black", "Daniel West"]
        },
        {
            "idx": 2, 
            "orig_name": "Robert Chen", 
            "orig_age": 62, 
            "names": ["Wei Zhang", "Jun Liu", "Tao Wang", "Minh Nguyen", "Kenji Sato", "Hiroshi Tanaka", "David Wu", "Kevin Lee", "Peter Chan"]
        },
        {
            "idx": 3, 
            "orig_name": "John M. Anderson", 
            "orig_age": 67, 
            "names": ["Michael Peterson", "David Johnson", "Robert Smith", "Christopher Davis", "John Miller", "James Wilson", "William Moore", "Richard Taylor", "Thomas Anderson"]
        },
        {
            "idx": 4, 
            "orig_name": "David W. Thompson", 
            "orig_age": 73, 
            "names": ["Arthur Dent", "Ford Prefect", "Zaphod Beeblebrox", "Marvin Android", "Slartibartfast Magrathea", "Trillian Astra", "Roosta Stardust", "Prosser Vogon", "Deep Thought"]
        },
        {
            "idx": 5, 
            "orig_name": "David Kim", 
            "orig_age": 65, 
            "names": ["Sang-Min Park", "Ji-Hoon Kim", "Min-Su Choi", "Dong-Wook Lee", "Jun-Ho Jung", "Sung-Min Kang", "Hyun-Woo Cho", "Kyung-Soo Yoon", "Jae-Jin Lim"]
        },
        {
            "idx": 6, 
            "orig_name": "Susan Taylor", 
            "orig_age": 65, 
            "names": ["Barbara Gordon", "Diana Prince", "Selina Kyle", "Harleen Quinzel", "Pamela Isley", "Dinah Lance", "Helena Bertinelli", "Cassandra Cain", "Kate Kane"]
        },
        {
            "idx": 7, 
            "orig_name": "Lisa Anderson", 
            "orig_age": 63, 
            "names": ["Sarah Connor", "Ellen Ripley", "Leia Organa", "Dana Scully", "Kathryn Janeway", "Kara Thrace", "Laura Roslin", "Samantha Carter", "Aeryn Sun"]
        },
        {
            "idx": 8, 
            "orig_name": "Linda Thompson", 
            "orig_age": 65, 
            "names": ["Mary Maloney", "Elizabeth Bennet", "Jane Eyre", "Catherine Earnshaw", "Jo March", "Anne Shirley", "Emma Woodhouse", "Elinor Dashwood", "Dorothy Gale"]
        },
        {
            "idx": 9, 
            "orig_name": "Frank Wilson", 
            "orig_age": 65, 
            "names": ["George Costanza", "Jerry Seinfeld", "Cosmo Kramer", "Newman Post", "Frank Costanza", "Morty Seinfeld", "Uncle Leo", "Kenny Bania", "David Puddy"]
        }
    ]

def get_variations():
    """
    Returns a dictionary of manually crafted text variations.
    Structure: Note_Index -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Maria G. Rodriguez (Cryoablation LLL)
            1: "Indication: LLL nodule, 2.6cm, PET+. Surgically ineligible.\nProcedure: Flexible bronchoscopy, EMN (Veran), Radial EBUS, Cryoablation.\nTarget: LLL lateral basal segment.\nAction: Navigated to lesion. Confirmed w/ REBUS (concentric). Cryoprobe inserted. 3 cycles freeze/thaw performed (-165C). Ice ball visualized.\nComplications: None.\nPlan: Admit, CXR, CT in 24h.",
            2: "OPERATIVE SUMMARY: Bronchoscopic Cryoablation of Peripheral Pulmonary Malignancy.\nThe patient, a 70-year-old female with significant comorbidities precluding surgical resection, underwent palliative ablation of a PET-avid left lower lobe nodule. Under general anesthesia, the airway was secured. Utilizing electromagnetic navigation (Veran SPiN) and radial endobronchial ultrasound confirmation, the target lesion in the lateral basal segment was localized. A cryoablation probe was advanced into the tumor core. A modified protocol utilizing three freeze-thaw cycles was executed to ensure adequate tumoricidal effect given the lesion diameter (>2.5cm). Post-procedural imaging via radial EBUS confirmed a hyperechoic ablation zone extending beyond the tumor margins.",
            3: "CPT Justification:\n31641: Bronchoscopy with destruction of tumor. \n- Technique: Cryoablation (Erbecryo system).\n- Target: LLL peripheral nodule (Malignant).\n- Effort: 3 freeze-thaw cycles performed to destroy tumor tissue.\n- Guidance: EMN and Radial EBUS used for localization (integral to successful placement of ablation probe).",
            4: "Procedure Note - Pulmonary\nPatient: [PATIENT_NAME]\nAttending: Dr. Zhang\n\nSteps:\n1. Time out. GA induced. 8.0 ETT placed.\n2. Scope passed. Airways patent.\n3. Veran navigation to LLL lateral basal nodule.\n4. Radial EBUS confirmed lesion (26mm).\n5. Cryoprobe placed. 3 freeze cycles performed.\n6. No bleeding. Extubated.\n\nPlan: Admit for obs.",
            5: "cryo ablation procedure for [PATIENT_NAME] today for that LLL cancer shes not a surgery candidate. used general anesthesia intubated. used the veran system to get out there took a while cause of the angle. radial ebus confirmed it solid mass. stuck the cryo probe in froze it three times just to be sure cause its big. saw the ice ball on fluoro looks good. no bleeding really pulled everything out woke her up sent to pacu.",
            6: "Flexible bronchoscopy with electromagnetic navigation and cryoablation of left lower lobe peripheral pulmonary nodule. Patient is a 70-year-old woman with extensive medical comorbidities. General anesthesia induced. Electromagnetic navigation bronchoscopy commenced using Veran SPiN Planning and Navigation System. Target lesion in left lower lobe lateral basal segment identified. Radial EBUS probe advanced through EWC. Cryoablation probe introduced. Three freeze-thaw cycles performed. Post-ablation radial EBUS repeated showing marked hyperechoic changes. No hemorrhage. Patient reversed from anesthesia.",
            7: "[Indication]\nLLL Nodule (Adenocarcinoma), Medically Inoperable.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nNavigation to LLL lateral basal segment (Veran). Radial EBUS confirmation. Cryoablation performed (3 cycles: 6min/6min/5min). Ice ball confirmed via fluoroscopy and REBUS. No complications.\n[Plan]\nAdmit, Telemetry, post-op CT.",
            8: "Ms. [PATIENT_NAME] presented for treatment of her left lung cancer. Because surgery wasn't safe for her, we proceeded with a bronchoscopic ablation. After she was asleep, we used a navigation system to guide a catheter out to the tumor in the lower part of her left lung. We double-checked the position with ultrasound. Then, we inserted a freezing probe right into the tumor and ran three cycles of extreme cold to destroy the cancer cells. Everything went smoothly, and she woke up well.",
            9: "Operation: Bronchoscopy with tumor destruction.\nTechnique: Cryotherapy.\nAction: The LLL lateral basal tumor was localized via electromagnetic guidance. The cryoprobe was positioned centrally. Three cycles of freezing were administered to ablate the tissue. \nOutcome: Successful destruction of target lesion with adequate margins."
        },
        1: { # Timothy R. Brooks (Emergent RFA Hemostasis)
            1: "Indication: Post-biopsy hemorrhage RUL.\nProcedure: Bronchoscopy + RFA.\nFindings: Blood in RUL. No active bronchial source.\nAction: Navigated to tumor site. RFA probe inserted. Coagulation mode (40W) then Ablation mode (90C). \nResult: Hemostasis achieved. Tumor ablated. Chest tube output decreased.\nPlan: ICU, wean chest tube.",
            2: "PROCEDURE: Emergent Bronchoscopy with Radiofrequency Ablation for Hemostasis and Tumor Control.\nINDICATION: 72-year-old male status post complicated TTNA with active hemothorax and parenchymal bleeding.\nDESCRIPTION: Under general anesthesia, the airway was inspected. Utilizing ENB, the RFA catheter was advanced to the site of the bleeding tumor in the RUL. A modified RFA protocol was employed: initially low-wattage energy was applied to effect hemostasis via tissue coagulation, followed by standard high-temperature ablation to treat the underlying malignancy. Immediate cessation of bleeding was observed.",
            3: "Codes: 31641 (Bronchoscopy with destruction/relief of stenosis).\nJustification: RFA probe used primarily to destroy tumor tissue and secondarily to coagulate bleeding vessels in the tumor bed.\nNote: This was a salvage procedure combining hemostasis (normally 31634/31643) and ablation (31641). 31641 is the primary definitive therapy performed.",
            4: "Procedure: Urgent RFA\nPatient: [PATIENT_NAME]\nIndication: Bleeding after IR biopsy.\nSteps:\n1. Intubated. Bronch to RUL.\n2. Navigated to biopsy site.\n3. Inserted RFA probe.\n4. Cauterized bleeding (40W).\n5. Ablated tumor (90C).\n6. Bleeding stopped.\nPlan: ICU, keep chest tube.",
            5: "emergency bronch for [PATIENT_NAME] he was bleeding from that IR biopsy yesterday chest tube putting out blood. we went in intubated him. used the nav system to find the hole in the tumor. stuck the RFA probe in there. cooked it at low power to stop the bleed then high power to kill the cancer. worked great bleeding stopped chest tube looks clear now. sending back to ICU.",
            6: "Urgent bronchoscopy with radiofrequency ablation. Patient with hemothorax following transthoracic biopsy. General anesthesia. Airway clear of active large airway bleeding. Navigation to RUL posterior segment. RFA probe deployed. Hemostasis protocol (low power) followed by ablation protocol (high power) utilizing Vivant system. Hemostasis achieved. Tumor treated. Chest tube output diminished.",
            7: "[Indication]\nPost-biopsy hemorrhage, RUL tumor.\n[Anesthesia]\nGeneral.\n[Description]\nEmergent navigation to RUL tumor. RFA applied for hemostasis and tumor destruction. Bleeding resolved. Tumor ablated.\n[Plan]\nICU, monitor Hgb/Chest tube.",
            8: "Mr. [PATIENT_NAME] had a complication from his lung biopsy yesterday and was bleeding into his chest. We took him to the bronchoscopy suite urgently. Using a special navigation system, we guided a radiofrequency probe to the bleeding tumor. We used the heat from the probe first to seal the bleeding vessels and then to destroy the tumor itself. It worked perfectly, and the bleeding stopped immediately.",
            9: "Procedure: Bronchoscopic thermal therapy.\nIndication: Iatrogenic hemorrhage and malignancy.\nAction: The hemorrhagic site was accessed via navigation. Thermal energy was applied to coagulate vessels and destroy neoplastic tissue. \nResult: Hemostasis and tumor ablation achieved."
        },
        2: { # Robert Chen (Microwave RUL)
            1: "Indication: RUL Adenocarcinoma.\nProcedure: Microwave Ablation.\nProbe: Neuwave 14mm.\nSettings: 60W, 6 min.\nGuidance: ENB + R-EBUS.\nResult: Good ablation zone. No complications.\nPlan: Discharge tomorrow.",
            2: "OPERATIVE REPORT: Bronchoscopic Microwave Ablation.\nCLINICAL SUMMARY: Patient with medically inoperable RUL adenocarcinoma.\nPROCEDURE: The target lesion in the RUL anterior segment was localized using electromagnetic navigation and confirmed via radial EBUS (contact view). A Neuwave microwave antenna was deployed. Microwave energy was delivered at 60 Watts for 6 minutes. Post-ablation imaging verified adequate coverage of the lesion. The patient tolerated the procedure well.",
            3: "Service: 31641 (Destruction of tumor).\nMethod: Microwave Ablation.\nDevice: Neuwave System.\nSupport: 31627 (Navigation), 31654 (Radial EBUS).\nNarrative: Navigated to RUL nodule. Verified tool-in-lesion. Delivered microwave energy to destroy tumor. Post-procedure check negative for pneumothorax.",
            4: "Procedure: Microwave Ablation\nPatient: [PATIENT_NAME]\nLocation: RUL anterior.\nSteps:\n1. Navigated to lesion (SuperDimension).\n2. Confirmed with Radial EBUS.\n3. Inserted Microwave catheter.\n4. Ablated 60W for 6 mins.\n5. Checked airway - clear.\nPlan: Post-op CT.",
            5: "done by Dr Foster for [PATIENT_NAME]. RUL cancer. used the superD to get there and radial ebus to see it. put the microwave needle in. burned it for 6 mins at 60 watts. looks like we got it all based on the scan after. patient woke up fine no pneumo.",
            6: "Bronchoscopic microwave ablation. Right upper lobe nodule. General anesthesia. Electromagnetic navigation to RUL anterior segment. Target confirmed in contact position with radial EBUS. Microwave probe inserted. Ablation performed at 60W for 6 minutes. Lesion coverage confirmed. Airway patent. Extubated.",
            7: "[Indication]\nRUL Adenocarcinoma.\n[Anesthesia]\nGeneral.\n[Description]\nNavigation to RUL anterior segment. Microwave ablation (60W x 6min). Lesion destroyed. No complications.\n[Plan]\nObservation, CT in 24h.",
            8: "Mr. [PATIENT_NAME] came in for ablation of his right upper lobe lung cancer. We used a microwave probe inserted through the bronchoscope. After finding the tumor with navigation and ultrasound, we applied microwave energy for 6 minutes. This heated the tumor enough to destroy it. He is recovering well.",
            9: "Procedure: Bronchoscopic tumor destruction.\nModality: Microwave energy.\nAction: The RUL neoplasm was targeted. The microwave antenna was positioned. Thermal energy was delivered to ablate the mass. \nResult: Therapeutic destruction of the tumor."
        },
        3: { # John M. Anderson (Microwave RUL - Detailed)
            1: "Indication: RUL posterior nodule (2.3cm). High risk surgical candidate.\nProcedure: EMN Bronchoscopy + Microwave Ablation.\nEquipment: SuperDimension, Emprint 2.0 probe.\nAction: Navigated to RB1. Confirmed w/ R-EBUS & Cone Beam. Ablated 65W x 5 min (Max temp 85C).\nResult: Hyperechoic zone on R-EBUS (necrosis).\nPlan: Admit, CT 6h.",
            2: "OPERATIVE REPORT: Electromagnetic Navigation Bronchoscopy with Microwave Ablation.\nINDICATION: Primary lung adenocarcinoma, RUL posterior segment, in a patient with severe COPD.\nTECHNIQUE: General anesthesia was induced. Using the SuperDimension system, the RUL posterior target was cannulated. Radial EBUS and Cone-Beam CT verified probe placement within 5mm of the lesion center. A microwave ablation catheter was advanced. Energy was delivered (65W, 5 min) achieving a peak tip temperature of 85C. Post-ablation imaging confirmed coagulative necrosis encompassing the tumor.",
            3: "Billing Codes:\n- 31641: Destruction of tumor (Microwave Ablation).\n- 31627: Navigation (SuperDimension).\n- 31654: Radial EBUS.\nNote: No biopsy performed today (diagnostic confirmed prior). 31641 is the primary service.",
            4: "Procedure Note\nPatient: [PATIENT_NAME]\nAttending: Dr. Chen\nSteps:\n1. GA/Intubation.\n2. Navigated to RUL posterior nodule.\n3. Confirmed with REBUS and Cone Beam CT.\n4. Microwave ablation: 65W for 5 mins.\n5. Re-imaged: Good ablation zone.\n6. Extubated.\nPlan: Admit.",
            5: "ablation for [PATIENT_NAME] today. he has that RUL nodule and cant have surgery. used the superD nav system and the emprint microwave probe. got right to the middle of it checked with the spinny CT. cooked it at 65 watts for 5 mins. temp got up to 85. looks fried on the ultrasound. no bleeding.",
            6: "Bronchoscopic electromagnetic navigation with microwave ablation of right upper lobe peripheral nodule. 67-year-old gentleman. General anesthesia. Navigation to RUL posterior segment. Radial EBUS and cone-beam CT confirmation. Microwave ablation probe advanced. Ablation 65 watts for 5 minutes. Hyperechoic changes on EBUS. No complications.",
            7: "[Indication]\nRUL Adenocarcinoma, inoperable.\n[Anesthesia]\nGeneral.\n[Description]\nEMN to RUL posterior. Confirmed w/ REBUS/CBCT. Microwave ablation (65W, 5min). Tumor necrosed.\n[Plan]\nAdmit, f/u CT.",
            8: "We treated Mr. [PATIENT_NAME]'s lung cancer today using a microwave ablation catheter. Because of his COPD, surgery wasn't an option. We navigated a small catheter to the tumor in his right upper lobe and confirmed its position with a 3D X-ray spin. We then heated the tumor to 85 degrees Celsius for 5 minutes to kill the cancer cells. The procedure was successful.",
            9: "Procedure: Image-guided tumor destruction.\nDevice: Microwave antenna.\nAction: The RUL lesion was accessed via electromagnetic guidance. The probe was inserted and activated (65W). Thermal ablation was performed. \nResult: Coagulative necrosis of the target."
        },
        4: { # David W. Thompson (RFA RLL - Detailed)
            1: "Indication: RLL nodule (RB9). Adenocarcinoma.\nProcedure: RFA Ablation via EMN.\nProtocol: 2 overlapping cycles. Cycle 1: 90C x 8 min. Cycle 2: 90C x 6 min (pulled back 5mm).\nVerification: R-EBUS & Cone Beam CT.\nComplications: None.\nPlan: Admit, CXR 4h, CT 24h.",
            2: "OPERATIVE REPORT: Bronchoscopic Radiofrequency Ablation.\nINDICATION: 73-year-old male with RLL adenocarcinoma.\nPROCEDURE: Under general anesthesia, the RB9 segment was navigated using the Veran SPiN system. Cone-beam CT confirmed guide sheath placement 8mm from the lesion center. An RFA probe (Vivant) was introduced. Two overlapping ablation cycles were performed (90C for 8 min, then 90C for 6 min) to ensure adequate margins. Post-ablation R-EBUS demonstrated a 'ice-cream cone' sign consistent with successful ablation.",
            3: "Codes:\n- 31641 (Destruction of tumor - RFA).\n- 31627 (Navigation).\n- 31654 (Radial EBUS).\nJustification: Definitive treatment of malignant nodule via bronchoscopic radiofrequency energy application.",
            4: "Procedure Note\nPatient: [PATIENT_NAME]\nProcedure: RFA RLL.\nSteps:\n1. Navigated to RLL basal segment.\n2. Confirmed with CBCT.\n3. RFA Cycle 1: 8 mins @ 90C.\n4. Repositioned 5mm proximal.\n5. RFA Cycle 2: 6 mins @ 90C.\n6. Extubated.\nPlan: Admit.",
            5: "RFA procedure for [PATIENT_NAME] RLL tumor. Used the veran system. Cone beam looked good 8mm from center. Did two burns first one 8 mins second one 6 mins at 90 degrees. Impedance looked good. No issues patient did great.",
            6: "Flexible bronchoscopy with electromagnetic navigation and radiofrequency ablation. Right lower lobe peripheral pulmonary nodule. General anesthesia. Navigation to RB9. Confirmation with radial EBUS and cone-beam CT. Radiofrequency ablation probe active. Two cycles performed. Ablation zone confirmed. Patient stable.",
            7: "[Indication]\nRLL Adenocarcinoma.\n[Anesthesia]\nGeneral.\n[Description]\nNavigation to RLL (RB9). RFA performed (2 cycles, overlapping). Tumor ablated.\n[Plan]\nAdmit 7 East.",
            8: "We performed a radiofrequency ablation on Mr. [PATIENT_NAME] today. Using a special navigation system and a 3D X-ray, we guided a heat probe right into the tumor in his right lower lung. We heated the tumor to 90 degrees Celsius in two separate steps to make sure we got the whole thing plus a safety margin. He tolerated it well.",
            9: "Procedure: Bronchoscopic thermal ablation.\nModality: Radiofrequency energy.\nAction: The RLL target was localized. The RFA electrode was deployed. Overlapping thermal treatments were administered to destroy the malignancy. \nResult: Successful tumor ablation."
        },
        5: { # David Kim (Diagnostic EMN/EBUS - A47829C)
            1: "Indication: LUL GGO 9mm.\nProcedure: EMN Bronchoscopy + R-EBUS.\nSampling: Needle x2, Forceps x4, Brush x1.\nFluoroscopy: 2.8 min.\nResult: Tool-in-lesion confirmed. Samples sent.\nComplications: None.",
            2: "PROCEDURE: Electromagnetic Navigation Bronchoscopy with Radial EBUS and Biopsy.\nINDICATION: 9mm ground-glass nodule, LUL.\nFINDINGS: The lesion was successfully localized using electromagnetic navigation. Radial EBUS demonstrated a concentric return, confirming tool-in-lesion status. Diagnostic sampling was performed via transbronchial needle aspiration, forceps biopsy, and cytology brush. No immediate complications were noted.",
            3: "Codes:\n- 31627 (Navigation)\n- 31629 (TBNA)\n- 31628 (Biopsy)\n- 31654 (Radial EBUS)\nNote: Multiple modalities used to maximize yield on small GGO.",
            4: "Resident Note\nPatient: [PATIENT_NAME]\nProcedure: Nav Bronch LUL.\nSteps:\n1. Navigated to LUL apical-posterior.\n2. R-EBUS: Concentric view.\n3. TBNA x 2.\n4. Biopsy x 4.\n5. Brush x 1.\nPlan: Follow up path.",
            5: "diagnostic bronch for [PATIENT_NAME] small GGO in the LUL. used the nav system got right to it. radial ebus showed we were in the middle. took a bunch of samples needle biopsy brush. patient did fine no pneumothorax.",
            6: "Bronchoscopy with electromagnetic navigation and biopsy. Indication: LUL peripheral ground-glass nodule. Moderate sedation. Navigation to LUL apical-posterior segment. Radial EBUS confirmation. Sampling via TBNA, forceps, and brush. No complications.",
            7: "[Indication]\nLUL GGO.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEMN navigation to LUL. Concentric R-EBUS view. TBNA, TBBx, Brush performed.\n[Plan]\nPathology pending.",
            8: "We performed a biopsy on Mr. [PATIENT_NAME]'s small lung nodule today. Using a navigation system like a GPS for the lungs, we found the 9mm spot in the left upper lobe. We confirmed we were in the right place with ultrasound and took several samples using a needle, forceps, and a brush. He handled the sedation well.",
            9: "Procedure: Navigational bronchoscopy with multimodal sampling.\nAction: The LUL opacity was localized. The lesion was interrogated with radial ultrasound. Specimens were acquired via needle aspiration, forceps extraction, and mucosal brushing. \nResult: Diagnostic material obtained."
        },
        6: { # Susan Taylor (EBUS Systematic 5 stations)
            1: "Indication: Mediastinal adenopathy.\nProcedure: EBUS-TBNA.\nStations Sampled: 2R, 4R, 4L, 7, 11R.\nFindings: 4R/7 positive for carcinoma. 2R/4L/11R benign.\nCode: 31653 (3+ stations).",
            2: "OPERATIVE REPORT: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nINDICATION: Staging of mediastinal lymphadenopathy.\nPROCEDURE: A systematic evaluation of the mediastinum was performed. Lymph node stations 2R, 4R, 4L, 7, and 11R were visualized and sampled. ROSE confirmed metastatic carcinoma in stations 4R and 7. Stations 2R, 4L, and 11R showed reactive changes. The procedure was uncomplicated.",
            3: "Code: 31653 (EBUS-TBNA 3+ stations).\nJustification: 5 distinct nodal stations were sampled (2R, 4R, 4L, 7, 11R). This meets the criteria for the highest level EBUS code.",
            4: "Procedure: EBUS\nPatient: [PATIENT_NAME]\nStations:\n- 2R: Benign\n- 4R: Malignant\n- 4L: Benign\n- 7: Malignant\n- 11R: Benign\nPlan: Oncology.",
            5: "EBUS for [PATIENT_NAME]. We sampled everything 2R 4R 4L 7 and 11R. 4R and 7 were cancer the rest were fine. No PET to guide us so we did them all. Patient okay.",
            6: "Endobronchial ultrasound with transbronchial needle aspiration. Systematic approach. Stations 2R, 4R, 4L, 7, and 11R sampled. ROSE positive for malignancy in 4R and 7. Molecular testing requested. No complications.",
            7: "[Indication]\nMediastinal adenopathy.\n[Anesthesia]\nModerate Sedation.\n[Description]\nSystematic EBUS-TBNA. Stations 2R, 4R, 4L, 7, 11R sampled. Malignancy confirmed in 4R/7.\n[Plan]\nOncology referral.",
            8: "Ms. [PATIENT_NAME] underwent a full lymph node staging procedure today. Since we didn't have a PET scan, we sampled five different lymph node stations in her chest (2R, 4R, 4L, 7, 11R) to be thorough. We found cancer cells in the station 4R and 7 nodes, but the others appeared clear. This helps us accurately stage her disease.",
            9: "Procedure: Systematic EBUS-guided nodal aspiration.\nAction: Five mediastinal and hilar stations were identified and sampled (2R, 4R, 4L, 7, 11R). \nResult: Diagnosis of N2 disease (positive 4R/7)."
        },
        7: { # Lisa Anderson (EMN Diagnostic - BB-8472-K)
            1: "Indication: LLL nodule 19mm.\nProcedure: EMN Bronchoscopy.\nFindings: Concentric REBUS view.\nSampling: Needle x3, Biopsy x4, Brush x2.\nResult: Tool-in-lesion confirmed. Samples sent.\nPlan: Clinic f/u.",
            2: "PROCEDURE NOTE: Diagnostic Bronchoscopy with Electromagnetic Navigation.\nINDICATION: 19mm PET-positive LLL nodule.\nTECHNIQUE: Navigation was performed to the target lesion. Radial EBUS confirmed a concentric orientation. Transbronchial needle aspiration, forceps biopsy, and brushing were performed. Fluoroscopy time was 5.1 minutes. Post-procedure chest x-ray was negative for pneumothorax.",
            3: "Codes: 31627 (Nav), 31629 (TBNA), 31628 (Bx), 31654 (REBUS).\nJustification: Multimodal sampling of peripheral nodule utilizing navigation and ultrasound confirmation.",
            4: "Resident Note\nPatient: [PATIENT_NAME]\nProcedure: Nav Bronch.\nSteps:\n1. Nav to LLL.\n2. REBUS concentric.\n3. TBNA x 3.\n4. Bx x 4.\n5. Brush x 2.\nNo complications.",
            5: "bronch for [PATIENT_NAME] LLL nodule. used the electromagnetic nav. got a good signal. radial ebus concentric. took biopsies needle and brush. fluoro was 5 mins. patient stable.",
            6: "Flexible bronchoscopy with electromagnetic navigation. Indication: Peripheral LLL nodule. Moderate sedation. EMN localization successful. Radial EBUS concentric. Samples obtained via needle, forceps, and brush. No pneumothorax.",
            7: "[Indication]\nLLL Nodule.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEMN navigation. Concentric REBUS. Sampling: TBNA, TBBx, Brush.\n[Plan]\nFollow pathology.",
            8: "We performed a navigational bronchoscopy on [PATIENT_NAME] to biopsy a 19mm nodule in the left lower lung. We successfully reached the nodule and confirmed it with ultrasound. We took multiple samples using different tools to ensure we get a diagnosis. There were no complications.",
            9: "Procedure: Navigational bronchoscopy.\nAction: The LLL lesion was localized. Concentric ultrasound confirmation was achieved. Tissue was harvested via aspiration, biopsy, and brushing. \nResult: Diagnostic procedure completed."
        },
        8: { # Linda Thompson (EBUS Single Station 7)
            1: "Indication: Station 7 adenopathy.\nProcedure: EBUS-TBNA.\nTarget: Station 7 only (31mm).\nSampling: 5 passes.\nROSE: Adequate.\nCode: 31652 (1 station).\nResult: Samples sent.",
            2: "OPERATIVE NOTE: Targeted EBUS-TBNA.\nINDICATION: Isolated subcarinal lymphadenopathy.\nPROCEDURE: The EBUS scope was introduced. Station 7 was identified, measuring 31mm. Five needle passes were performed. ROSE confirmed adequacy. Per oncology request, no other stations were sampled. Procedure tolerated well.",
            3: "Code: 31652 (EBUS-TBNA 1-2 stations).\nJustification: Only station 7 was sampled per specific clinical request. Systematic staging was not performed.",
            4: "Procedure: EBUS\nPatient: [PATIENT_NAME]\nStation 7: 31mm. 5 passes. ROSE adequate.\nNo other stations sampled.\nPlan: Path pending.",
            5: "targeted EBUS for [PATIENT_NAME]. only needed station 7 oncology said dont bother with the rest. it was huge 31mm. stuck it 5 times. rose said it was good. done.",
            6: "Endobronchial ultrasound with transbronchial needle aspiration. Station 7 subcarinal node targeted. 31mm short axis. 5 passes with 22G needle. ROSE adequate. No other stations sampled. Patient stable.",
            7: "[Indication]\nStation 7 adenopathy.\n[Anesthesia]\nModerate Sedation.\n[Description]\nTargeted EBUS Station 7. 5 passes. ROSE adequate.\n[Plan]\nDischarge.",
            8: "Ms. [PATIENT_NAME] needed a biopsy of a large lymph node under her windpipe (station 7). We performed an EBUS procedure and focused solely on that node as requested by her oncologist. We took five good samples and the pathologist confirmed we had enough tissue for testing.",
            9: "Procedure: Targeted nodal aspiration.\nAction: Station 7 was identified via EBUS. Five aspirations were performed. \nResult: Adequate tissue obtained."
        },
        9: { # Frank Wilson (EBUS + RUL Bx)
            1: "Indication: Dx bronch + EBUS.\nProcedure: EBUS (4R, 7) + RUL Biopsy.\nEBUS: 4R/7 positive.\nRUL: Biopsy x4, Brush x2.\nCodes: 31652, 31625.\nPlan: Path pending.",
            2: "PROCEDURE NOTE: Combined EBUS-TBNA and Endobronchial Biopsy.\nINDICATION: Lung mass with adenopathy.\nEBUS: Stations 4R and 7 were sampled and ROSE confirmed malignancy.\nBRONCHOSCOPY: The RUL lesion was visualized endobronchially. Forceps biopsy and brushing were performed. \nSUMMARY: N2 disease with RUL primary.",
            3: "Codes:\n- 31652: EBUS (2 stations: 4R, 7).\n- 31625: Endobronchial biopsy (RUL lesion).\nJustification: Staging via EBUS and separate diagnostic biopsy of visible airway lesion.",
            4: "Procedure: EBUS + RUL Bx\nPatient: [PATIENT_NAME]\nSteps:\n1. EBUS 4R (Pos).\n2. EBUS 7 (Pos).\n3. Standard bronch RUL.\n4. Biopsied mass x 4.\n5. Brush x 2.\nPlan: Discharge.",
            5: "bronch for [PATIENT_NAME]. did ebus first. 4R and 7 both cancer. then went to the RUL saw the tumor there took bites and a brush. systematic check done. no bleeding.",
            6: "Diagnostic bronchoscopy with EBUS. Stations 4R and 7 sampled; both positive. Systematic evaluation completed. Right upper lobe endobronchial lesion biopsied and brushed. No complications.",
            7: "[Indication]\nLung mass, adenopathy.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS 4R/7 (Positive). RUL Biopsy/Brush performed.\n[Plan]\nWait for final path.",
            8: "Mr. [PATIENT_NAME] underwent a bronchoscopy today. We used the ultrasound scope to check his lymph nodes first; stations 4R and 7 both showed cancer cells. We then looked at the main tumor in the right upper lobe and took direct biopsies and brushings. This confirms the diagnosis and stage.",
            9: "Procedure: Staging EBUS and airway biopsy.\nAction: Nodal stations 4R and 7 were aspirated. The RUL endobronchial mass was biopsied and brushed. \nResult: Tissue obtained from primary and nodes."
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
        print(f"Error: Invalid JSON: {e}")
        return

    base_data = get_base_data_mocks()
    variations_text = get_variations()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through original notes
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Check if we have variations for this index
        if idx not in variations_text:
            continue

        # Generate 9 variations
        for style_num in range(1, 10):
            # Deep copy to avoid mutating the original
            note_entry = copy.deepcopy(original_note)
            
            # 1. Update Note Text
            if style_num in variations_text[idx]:
                raw_text = variations_text[idx][style_num]
                new_name = record['names'][style_num - 1]
                final_text = raw_text.replace("[PATIENT_NAME]", new_name)
                note_entry["note_text"] = final_text
            
            # 2. Update Registry Data (Simulated randomness)
            new_age = orig_age + random.randint(-3, 3)
            rand_date = generate_random_date(2025, 2025).strftime("%Y-%m-%d")
            
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date
                # Update MRN to be unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            
            # 3. Add Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Save output
    output_path = output_dir / OUTPUT_FILE
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_path}")

if __name__ == "__main__":
    main()