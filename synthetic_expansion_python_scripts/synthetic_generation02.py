import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_002.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILE = "synthetic_notes_part_002.json"

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
            "orig_name": "Elizabeth Okafor", 
            "orig_age": 65, 
            "names": ["Margaret Hale", "Eleanor Vance", "Judith Summers", "Beatrice Arthur", "Clara Oswin", "Martha Jones", "Donna Noble", "Rose Tyler", "Sarah Jane Smith"]
        },
        {
            "idx": 1, 
            "orig_name": "Mary Jackson", 
            "orig_age": 82, 
            "names": ["Dorothy Zbornak", "Blanche Devereaux", "Sophia Petrillo", "Betty White", "Estelle Getty", "Rue McClanahan", "Angela Lansbury", "Jessica Fletcher", "Maude Findlay"]
        },
        {
            "idx": 2, 
            "orig_name": "Sarah Martinez", 
            "orig_age": 58, 
            "names": ["Dana Scully", "Ellen Ripley", "Sarah Connor", "Leia Organa", "Nyota Uhura", "Kathryn Janeway", "Beverly Crusher", "Deanna Troi", "Kira Nerys"]
        },
        {
            "idx": 3, 
            "orig_name": "Rosa E. Martinez", 
            "orig_age": 63, 
            "names": ["Laura Roslin", "Kara Thrace", "Sharon Valerii", "Six Caprica", "Ellen Tigh", "Anastasia Dualla", "Cally Tyrol", "Helena Cain", "Sherry Palmer"]
        },
        {
            "idx": 4, 
            "orig_name": "Elizabeth Anne Morrison", 
            "orig_age": 55, 
            "names": ["Peggy Carter", "Natasha Romanoff", "Wanda Maximoff", "Carol Danvers", "Hope Van Dyne", "Gamora Zen", "Nebula Luphomoid", "Mantis Empath", "Valkyrie Brunnhilde"]
        },
        {
            "idx": 5, 
            "orig_name": "Marcus A. Thompson", 
            "orig_age": 69, 
            "names": ["Tony Stark", "Steve Rogers", "Bruce Banner", "Thor Odinson", "Clint Barton", "Nick Fury", "James Rhodes", "Sam Wilson", "Scott Lang"]
        },
        {
            "idx": 6, 
            "orig_name": "Sandra L. Bennett", 
            "orig_age": 74, 
            "names": ["Jean Grey", "Ororo Munroe", "Anna Marie", "Kitty Pryde", "Emma Frost", "Raven Darkholme", "Jubilation Lee", "Betsy Braddock", "Susan Storm"]
        },
        {
            "idx": 7, 
            "orig_name": "Juan Carlos Rodriguez", 
            "orig_age": 59, 
            "names": ["Bruce Wayne", "Clark Kent", "Diana Prince", "Barry Allen", "Arthur Curry", "Victor Stone", "Hal Jordan", "Oliver Queen", "John Stewart"]
        }
    ]

def get_variations():
    """
    Returns a dictionary of manually crafted text variations.
    Structure: Note_Index -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Elizabeth Okafor (Rigid Bronch, Stent, PleurX)
            1: "Indication: Central airway obstruction (R main) and R pleural effusion.\nProcedure: Rigid bronchoscopy. Tumor cored/debrided. APC/Cautery for hemostasis. Balloon dilation. 14x60mm metallic stent placed. PleurX catheter placed right hemithorax.\nComplication: None.\nResult: Airway patent. Effusion drained.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the operating suite for management of complex malignant central airway obstruction and malignant pleural effusion. Under general anesthesia with rigid bronchoscopic intubation, the right mainstem bronchus was visualized, demonstrating 90% occlusion by fungating tumor. Mechanical debulking was performed utilizing the rigid barrel, followed by electrocautery and argon plasma coagulation to the tumor base (CPT 31641). Following balloon dilation, a covered metallic stent was deployed, restoring luminal patency to the right mainstem bronchus (CPT 31636). Subsequently, a tunneled indwelling pleural catheter was inserted into the right hemithorax for palliation of the recurrent effusion (CPT 32550).",
            3: "Procedures Performed:\n1. 31641: Rigid bronchoscopy with destruction of tumor. Justification: APC and mechanical coring used to relieve right mainstem obstruction.\n2. 31636: Bronchoscopy with stent placement. Justification: Covered metallic stent deployed in R mainstem after debulking.\n3. 32550: Insertion of tunneled pleural catheter. Justification: Indwelling catheter placed for recurrent malignant effusion.",
            4: "Procedure Note\nPatient: [PATIENT_NAME]\nAttending: Dr. Kim\nSteps:\n1. Time out. GA induced. Rigid scope inserted.\n2. Saw tumor in Right Main. Debulked with scope tip and APC.\n3. Dilated with balloon.\n4. Placed metal stent (14x60). Good position.\n5. Did PleurX catheter on the right side. Got 850cc fluid.\n6. Extubated/Stable.",
            5: "we did a rigid bronch today on [PATIENT_NAME] for that airway tumor right side. used the storz scope cored out the tumor and burned the rest with APC. put a stent in there looks wide open now. also put in a pleurx catheter for the fluid on the right side. no issues really patient stable to recovery.",
            6: "The patient presented with right lung collapse and effusion. General anesthesia. Rigid bronchoscopy performed. Right mainstem tumor debrided mechanically and with APC. Airway caliber restored. Metallic stent deployed in right mainstem bronchus. Attention turned to right chest. Tunneled pleural catheter placed using standard technique. Fluid drained. Catheter capped. Patient tolerated well.",
            7: "[Indication]\nMalignant airway obstruction (R Main) and Recurrent Pleural Effusion.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nRigid scope introduced. Tumor debulked via mechanical coring and APC (31641). Stent (14x60mm) placed in Right Mainstem (31636). Tunneled PleurX catheter inserted right chest (32550).\n[Plan]\nICU monitoring. CXR.",
            8: "Ms. [PATIENT_NAME] was taken to the OR for airway management. We utilized a rigid bronchoscope to access the airway. A large tumor in the right mainstem was effectively removed using mechanical coring and heat therapy. To prevent re-obstruction, we deployed a metallic stent. While she was under, we also addressed her fluid buildup by placing a tunneled PleurX catheter in the right chest. She tolerated all distinct procedures well.",
            9: "Procedure: Rigid bronchoscopy with tumor ablation and stent deployment; indwelling pleural catheter insertion.\nAction: The right mainstem neoplasm was resected using the rigid barrel and argon plasma coagulation. Patency was re-established. An airway prosthesis was anchored in the right mainstem. A tunneled pleural drainage system was implanted in the right hemithorax.\nOutcome: Successful recanalization and fluid drainage."
        },
        1: { # Mary Jackson (Bronch BAL)
            1: "Indication: Pneumonia, non-resolving.\nSedation: Mod sed.\nProcedure: Scope via nose. Airways patent. No endobronchial lesions.\nAction: BAL LLL. 100cc in, 80cc return.\nPlan: Cultures pending. Continue Abx.",
            2: "PROCEDURE: Diagnostic flexible bronchoscopy with bronchoalveolar lavage.\nINDICATION: 82-year-old female with persistent right-sided infiltrates despite antibiotic therapy.\nFINDINGS: The tracheobronchial tree was systematically inspected. No endobronchial masses, mucosal irregularities, or foreign bodies were visualized. Thick secretions were noted diffusely. A bronchoalveolar lavage was performed in the left lower lobe (target segment) yielding turbid fluid which was submitted for microbiological analysis.",
            3: "Service: Bronchoscopy with BAL (31624).\nMedical Necessity: Non-resolving pneumonia (J18.9).\nDetails: Scope advanced to LLL. 100mL saline instilled in aliquots. 80mL aspirated. Specimen sent for quantitative culture. No biopsy performed (excludes 31628/31625). Diagnostic inspection (31622) included.",
            4: "Resident Note\nPatient: [PATIENT_NAME]\nPre-op Dx: Pneumonia\nSteps:\n1. Vitals stable. Lidocaine spray.\n2. Scope inserted nare.\n3. Inspection: Normal anatomy, some secretions.\n4. BAL LLL: Good return.\n5. Scope out.\nPlan: Wait for culture results.",
            5: "Bronchoscopy for [PATIENT_NAME] she has pneumonia that wont go away. used moderate sedation versed and fentanyl. looked around airways look okay just lots of secretions. washed the LLL collected fluid for culture. patient tolerated it fine no o2 desats.",
            6: "Diagnostic flexible bronchoscopy with bronchoalveolar lavage. Indication was non-resolving pneumonia. Upper airway and vocal cords normal. Trachea and main carina normal. Bilateral bronchial trees patent. Purulent secretions noted. BAL performed in LLL. Fluid sent for bacterial, fungal, and AFB culture. Patient stable.",
            7: "[Indication]\nRefractory Pneumonia.\n[Anesthesia]\nModerate Sedation.\n[Description]\nFlexible bronchoscopy. Airway inspection negative for mass/lesion. BAL performed LLL. Samples sent for micro.\n[Plan]\nAdjust antibiotics based on culture.",
            8: "We performed a bronchoscopy on Ms. [PATIENT_NAME] to investigate her persistent pneumonia. After numbing the nose and throat, the scope was passed easily. We didn't see any tumors or blockages, just some thick mucus. We washed the left lower lobe with saline and collected the fluid to check for specific bacteria. She did great during the procedure.",
            9: "Procedure: Flexible bronchoscopy with lung washing.\nContext: Persistent pulmonary infiltrate.\nAction: The bronchial tree was examined. No obstructions were observed. The LLL was lavaged with saline. Effluent was collected for analysis.\nResult: Specimen acquired for microbiology."
        },
        2: { # Sarah Martinez (EBUS-TBNA)
            1: "Indication: Mediastinal lymphadenopathy.\nProcedure: EBUS-TBNA.\nNodes Sampled: 4R, 7, 10R.\nFindings: Enlarged nodes. ROSE: Malignant cells (Adeno).\nComplications: None.",
            2: "OPERATIVE REPORT: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nINDICATION: Staging of non-small cell lung cancer.\nNARRATIVE: The EBUS scope was introduced. Systematic nodal survey identified lymphadenopathy. Transbronchial needle aspiration was performed at station 4R, station 7, and station 10R (3 distinct stations). Rapid on-site evaluation confirmed the presence of malignant cells consistent with adenocarcinoma in all sampled stations.",
            3: "Code: 31653 (EBUS-TBNA 3+ stations).\nTechnique: Linear EBUS scope used to visualize and biopsy mediastinal/hilar nodes.\nStations Sampled: Station 7 (Subcarinal), Station 4R (Right Paratracheal), Station 10R (Right Hilar).\nPathology: Cytology obtained from 3 distinct stations. ROSE service utilized.",
            4: "Procedure: EBUS\nPatient: [PATIENT_NAME]\nAttending: Dr. Chen\nSteps:\n1. Airway inspection: Normal.\n2. EBUS scope in.\n3. Biopsied 4R (4 passes).\n4. Biopsied 7 (4 passes).\n5. Biopsied 10R (3 passes).\nROSE: Positive for malignancy.\nPlan: Oncology referral.",
            5: "Procedure note EBUS for [PATIENT_NAME] she has a lung mass and nodes. We sampled three spots 4R 7 and 10R. The pathologist in the room said it looks like cancer adenocarcinoma. No bleeding patient woke up fine.",
            6: "Endobronchial ultrasound with needle aspiration performed for staging. Stations 4R, 7, and 10R were visualized and sampled using a 22-gauge needle. Adequate tissue obtained from all three stations. ROSE confirmed adenocarcinoma. No complications. Extubated and transferred to recovery.",
            7: "[Indication]\nLung mass, mediastinal adenopathy.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS-TBNA performed. Stations 4R, 7, 10R sampled. ROSE positive for adenocarcinoma.\n[Plan]\nOncology follow-up.",
            8: "Ms. [PATIENT_NAME] underwent EBUS staging today. We specifically targeted the lymph nodes in the center of the chest. Using the ultrasound needle, we took samples from station 4R, station 7, and station 10R. The preliminary results from the pathologist in the room showed cancer cells in the lymph nodes, confirming Stage IIIB disease.",
            9: "Procedure: Endobronchial ultrasound with transbronchial needle aspiration.\nAction: The mediastinum was interrogated. Lymph nodes at stations 4R, 7, and 10R were punctured and aspirated. \nResult: Cytology confirmed metastatic adenocarcinoma."
        },
        3: { # Rosa E. Martinez (Cryoablation)
            1: "Indication: LUL nodule, NSCLC.\nProcedure: Bronchoscopy with Cryoablation.\nTarget: LUL anterior segment.\nAction: Probe to lesion. 2 freeze-thaw cycles (5 min each). Ice ball visualized.\nResult: Lesion treated. No bleeding.",
            2: "OPERATIVE REPORT: Bronchoscopic destruction of tumor via cryoablation.\nINDICATION: Stage IA1 adenocarcinoma, medically inoperable.\nTECHNIQUE: Under general anesthesia, the LUL target was localized using navigational bronchoscopy and radial EBUS. A flexible cryoprobe was advanced into the lesion. Two cycles of cryoablation were performed (freeze 5 min/thaw 3 min). Fluoroscopy confirmed ice ball formation encompassing the target. Post-procedure inspection revealed no hemorrhage.",
            3: "Code: 31641 (Bronchoscopy with destruction of tumor).\nModality: Cryoablation.\nTarget: LUL peripheral nodule.\nNote: Navigation (31627) and Radial EBUS (31654) used for localization (if separately billable/documented), but primary therapeutic code is 31641 for the destruction.",
            4: "Cryoablation Note\nPatient: [PATIENT_NAME]\nLesion: LUL nodule.\nSteps:\n1. Navigate to lesion.\n2. Confirm with REBUS.\n3. Insert cryoprobe.\n4. Freeze x 5 mins, Thaw, Freeze x 5 mins.\n5. Check for bleeding - none.\nPlan: DC if CXR ok.",
            5: "Dr Patterson here procedure for [PATIENT_NAME] she has that small cancer in the LUL. We went in with the scope navigated to the spot. Used the cryo probe to freeze it twice. Saw the ice ball on the fluoro. No bleeding. She goes home today.",
            6: "Bronchoscopic cryoablation of left upper lobe nodule. Patient with early stage lung cancer. Navigational bronchoscopy used to access LUL anterior segment. Radial EBUS confirmed lesion. Cryoprobe activated for two freeze-thaw cycles. Tumor destruction achieved. Patient stable.",
            7: "[Indication]\nLUL Adenocarcinoma, inoperable.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nNavigation to LUL. Cryoablation performed (2 cycles). Ice ball confirmed. No complications.\n[Plan]\nDischarge, f/u imaging.",
            8: "We performed a cryoablation on Ms. [PATIENT_NAME]'s lung nodule today. Using navigation, we guided a freezing probe directly into the small tumor in the left upper lobe. We froze the tumor twice for 5 minutes each time to ensure cell death. The procedure went very smoothly with no bleeding.",
            9: "Procedure: Bronchoscopic tumor destruction.\nTechnique: Cryotherapy.\nAction: The LUL lesion was reached. The cryoprobe was applied, and the tissue was subjected to freezing cycles. \nOutcome: Ablation of the target nodule."
        },
        4: { # Elizabeth Anne Morrison (Ion + EBUS)
            1: "Indication: RLL mass, N2 nodes.\nProcedure: EBUS (4R, 7) + Ion Nav to RLL.\nFindings: Nodes + for Adeno. RLL mass + for Adeno.\nCodes: 31653 (3+ nodes? No, text says 4R/7 sampled = 31652), 31627, 31654, 31628.\nPlan: Onc consult.",
            2: "OPERATIVE NARRATIVE: Combined EBUS and Robotic Bronchoscopy.\nEBUS PHASE: Stations 4R and 7 were sampled via TBNA; both positive for malignancy.\nROBOTIC PHASE: The Ion catheter was navigated to the RLL posterior basal segment mass. Radial EBUS confirmed eccentric view. Transbronchial biopsies were obtained. ROSE confirmed adenocarcinoma morphologically identical to the nodal samples.",
            3: "Billing Summary:\n1. 31652: EBUS-TBNA (Stations 4R, 7 sampled - 2 stations).\n2. 31627: Robotic Navigation add-on.\n3. 31654: Radial EBUS add-on (Peripheral lesion).\n4. 31628: Transbronchial biopsy single lobe (RLL).\nNote: Nodal staging and peripheral biopsy performed in same session.",
            4: "Procedure: EBUS + Ion\nPatient: [PATIENT_NAME]\nSteps:\n1. EBUS scope. Sampled 4R and 7. ROSE positive.\n2. Switch to Ion scope.\n3. Navigate to RLL mass.\n4. Radial EBUS check.\n5. Biopsy x 8.\nROSE: Adenocarcinoma.\nPlan: Stage IIIA.",
            5: "Dr Foster note for [PATIENT_NAME]. Did the staging first EBUS showed cancer in 4R and 7 so N2 disease. Then used the robot to get the main mass in the RLL. Biopsies positive there too. No pneumothorax. Patient needs chemo/rads.",
            6: "Combined EBUS-TBNA and robotic navigational bronchoscopy. Mediastinal staging performed first. Lymph node stations 4R and 7 sampled; both positive for adenocarcinoma. Robotic system used to navigate to RLL posterior basal mass. Radial EBUS confirmation. Transbronchial biopsies obtained. Diagnosis confirmed as adenocarcinoma.",
            7: "[Indication]\nRLL mass, mediastinal adenopathy.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA of 4R, 7. Ion navigation to RLL mass. Radial EBUS confirmation. TBBx x8. All samples positive for Adeno.\n[Plan]\nRefer to Oncology.",
            8: "We started Ms. [PATIENT_NAME]'s procedure with EBUS to check the lymph nodes. Unfortunately, stations 4R and 7 were positive for cancer. We then switched to the robotic scope to biopsy the main mass in the right lower lobe. The navigation was accurate, and we got good samples which also showed adenocarcinoma. She will need a multidisciplinary treatment approach.",
            9: "Procedure: Endobronchial ultrasound staging and robotic-assisted peripheral biopsy.\nAction: Mediastinal nodes 4R and 7 were aspirated. The RLL mass was accessed via robotic guidance and sampled.\nResult: Diagnosis of Stage IIIA adenocarcinoma established."
        },
        5: { # Marcus A. Thompson (Ion + Fiducials)
            1: "Indication: LLL mass.\nProcedure: Ion Bronch, Radial EBUS, Biopsy, Fiducials.\nAction: Navigated to LLL. Confirmed w/ rEBUS. Biopsied (Adeno). Placed 3 fiducials.\nPlan: Radiation Oncology.",
            2: "OPERATIVE REPORT: Robotic Navigational Bronchoscopy with Fiducial Placement.\nINDICATION: 3.8 cm Left Lower Lobe mass, biopsy and marker placement for SBRT.\nPROCEDURE: The Ion system was utilized to navigate to the LLL target. Radial EBUS confirmed lesion position. Transbronchial biopsies yielded malignancy. Subsequently, fiducial markers were deployed within and around the lesion to facilitate image-guided radiation therapy.",
            3: "Codes:\n- 31627 (Navigation)\n- 31628 (TBBx)\n- 31626 (Fiducial placement)\n- 31654 (Radial EBUS)\nJustification: Robotic navigation used to access peripheral LLL lesion. Biopsy performed for diagnosis. Fiducials placed for stereotactic radiation planning.",
            4: "Resident Note\nPatient: [PATIENT_NAME]\nProcedure: Ion Biopsy + Fiducials\nSteps:\n1. Navigated to LLL mass.\n2. rEBUS confirmation.\n3. Biopsy x 5.\n4. Dropped fiducials x 4.\n5. Fluoro confirmed position.\nPlan: Rad Onc.",
            5: "Procedure for [PATIENT_NAME] LLL mass. Used the robot. Got to the spot used radial ebus. Took biopsies looks like cancer. Put in fiducial markers for the radiation doctors. No bleeding. Patient stable.",
            6: "Robotic bronchoscopy with transbronchial biopsy and fiducial marker placement. Left lower lobe mass. Navigation successful. Radial EBUS confirmed eccentric view. Biopsies obtained. Fiducial markers placed for future radiation therapy. No complications.",
            7: "[Indication]\nLLL mass, SBRT planning.\n[Anesthesia]\nModerate Sedation.\n[Description]\nIon navigation to LLL. Radial EBUS verification. Transbronchial biopsy performed. Fiducial markers placed.\n[Plan]\nPathology pending. Radiation planning.",
            8: "Mr. [PATIENT_NAME] is a candidate for radiation therapy for his left lung mass. We used the robotic bronchoscope to biopsy the mass first to confirm the type of cancer. Then, we placed gold fiducial markers around the tumor. These will help the radiation team target the tumor precisely during his treatments.",
            9: "Procedure: Computer-assisted bronchoscopy with tissue sampling and marker implantation.\nAction: The LLL lesion was localized. Tissue was harvested. Radiopaque markers were deposited.\nResult: Successful preparation for stereotactic radiotherapy."
        },
        6: { # Sandra Bennett (EBUS + EMN - Concatenated Note)
            # Focusing on the Bennett data: EBUS (1 station 7) + EMN RLL
            1: "Indication: Hx Breast Ca, new RLL nodule + subcarinal node.\nProcedure: EBUS (Station 7) + EMN (RLL).\nFindings: Station 7 + for Adeno. RLL nodule + for Adeno.\nImmuno: Pending (Breast vs Lung).\nCodes: 31652, 31627, 31628.",
            2: "OPERATIVE NARRATIVE: EBUS-TBNA and Electromagnetic Navigation Bronchoscopy.\nINDICATION: 74-year-old female with history of breast cancer presenting with new RLL nodule and lymphadenopathy. Rule out metastasis vs primary lung.\nPROCEDURE: EBUS-TBNA of station 7 performed. ROSE showed adenocarcinoma. EMN bronchoscopy then performed to RLL lateral basal nodule. Biopsies obtained. Tissue sent for extensive immunohistochemistry to differentiate breast metastasis from primary lung adenocarcinoma.",
            3: "Codes:\n- 31652: EBUS-TBNA (1 station: #7).\n- 31627: EMN Navigation.\n- 31654: Radial EBUS.\n- 31628: TBBx RLL.\nReason: Diagnostic dilemma (Breast met vs Lung primary). Immunohistochemistry required.",
            4: "Procedure: EBUS + SuperD\nPatient: [PATIENT_NAME]\nHx: Breast cancer.\nSteps:\n1. EBUS Station 7 -> Positive.\n2. Nav to RLL nodule -> Positive.\n3. Sent for stains (TTF1, GATA3).\nPlan: Wait for path to decide treatment.",
            5: "Consult for [PATIENT_NAME] she has breast cancer history but now lung spots. We did EBUS on the subcarinal node and nav bronch on the RLL spot. Both look like adeno. We need the stains to tell if its breast or lung cancer. No complications.",
            6: "EBUS-TBNA and electromagnetic navigation bronchoscopy. History of breast cancer. Station 7 lymph node sampled. RLL nodule sampled using navigation and radial EBUS. Both sites positive for adenocarcinoma. Immunohistochemistry pending to determine origin.",
            7: "[Indication]\nRLL nodule, Station 7 node, Hx Breast Ca.\n[Anesthesia]\nMAC.\n[Description]\nEBUS Station 7: Adeno. EMN RLL Nodule: Adeno. Tissue sent for IHC.\n[Plan]\nDetermine Breast vs Lung primary based on stains.",
            8: "Ms. [PATIENT_NAME] has a history of breast cancer and presented with a new lung nodule and lymph node. We sampled both the lymph node (using EBUS) and the lung nodule (using navigation). Both show cancer, but we can't tell if it's lung cancer or breast cancer spread without special stains. We ordered those tests and will know in a few days.",
            9: "Procedure: Ultrasound-guided nodal aspiration and navigated peripheral biopsy.\nContext: Differentiating metastasis from second primary.\nAction: Station 7 was aspirated. The RLL lesion was biopsied via electromagnetic guidance.\nResult: Tissue secured for immunohistochemical profiling."
        },
        7: { # Juan Carlos Rodriguez (EBUS - 4+ stations)
            1: "Indication: Lung mass, N2/N3 suspicion.\nProcedure: EBUS-TBNA.\nStations: 7, 4R, 10R, 11R.\nFindings: Malignancy in 7, 4R. 10R/11R reactive.\nDx: N2 positive NSCLC.\nCode: 31653.",
            2: "OPERATIVE REPORT: Endobronchial Ultrasound Staging.\nINDICATION: Radiographic lymphadenopathy in setting of lung mass.\nPROCEDURE: Systematic EBUS survey performed. Transbronchial needle aspiration performed at stations 7, 4R, 10R, and 11R. Cytopathology confirmed adenocarcinoma in mediastinal stations 7 and 4R, confirming N2 disease. Hilar stations were negative.",
            3: "Code: 31653 (EBUS-TBNA 3 or more stations).\nStations Sampled: 4 total (7, 4R, 10R, 11R).\nFindings: Positive for malignancy in mediastinum.\nMedical Necessity: Staging for lung cancer treatment planning.",
            4: "Procedure: EBUS\nPatient: [PATIENT_NAME]\nSteps:\n1. Scope in.\n2. Sampled 7 (Subcarinal) - Pos.\n3. Sampled 4R (Paratracheal) - Pos.\n4. Sampled 10R/11R - Neg.\nImpression: Stage IIIB (N2 disease).\nPlan: Chemo/Rad referral.",
            5: "EBUS for [PATIENT_NAME]. We looked at all the nodes. Poked 7, 4R, 10R and 11R. The big ones in the middle 7 and 4R have cancer. The others looked okay. So he has N2 disease. Needs oncology.",
            6: "Endobronchial ultrasound with transbronchial needle aspiration. Four nodal stations sampled: 7, 4R, 10R, 11R. ROSE confirmed malignancy in stations 7 and 4R. Diagnosis is N2-positive non-small cell lung cancer. Patient tolerated procedure well.",
            7: "[Indication]\nLung cancer staging.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA x 4 stations (7, 4R, 10R, 11R). Malignancy confirmed in mediastinal nodes.\n[Plan]\nMultidisciplinary tumor board.",
            8: "Mr. [PATIENT_NAME] underwent staging for his lung cancer. We used the ultrasound scope to sample lymph nodes in four different areas of his chest. Unfortunately, the cancer has spread to the lymph nodes in the mediastinum (N2 nodes), which means surgery isn't the first option. He will likely need chemotherapy and radiation.",
            9: "Procedure: EBUS-guided nodal staging.\nAction: Multiple mediastinal and hilar lymph node stations were identified and aspirated (7, 4R, 10R, 11R). \nResult: Cytological confirmation of mediastinal nodal involvement."
        }
    }
    return variations

def main():
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
            note_entry = copy.deepcopy(original_note)
            
            # 1. Update Note Text
            if style_num in variations_text[idx]:
                raw_text = variations_text[idx][style_num]
                # Replace [PATIENT_NAME] placeholder if present
                new_name = record['names'][style_num - 1]
                final_text = raw_text.replace("[PATIENT_NAME]", new_name)
                note_entry["note_text"] = final_text
            
            # 2. Update Registry Data
            new_age = orig_age + random.randint(-3, 3)
            rand_date = generate_random_date(2025, 2025).strftime("%Y-%m-%d")
            
            if "registry_entry" in note_entry:
                note_entry["registry_entry"]["patient_age"] = new_age
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