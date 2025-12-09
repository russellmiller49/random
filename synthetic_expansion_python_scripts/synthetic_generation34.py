import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_034.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds manually crafted text variations based on the styles requested.
    # Mapping: Note_Index -> Style_Index (1-9) -> Text
    # Note: Indices 1 and 7 in the source are duplicates/fragments of 0 and 6 respectively. 
    # They share variations but will have unique patient metadata generated.
    
    variations = {
        0: { # Martinez (EBUS-TBNA 2R, 4R, 7)
            1: "Procedure: EBUS-TBNA.\nIndication: 62mm R paratracheal node.\nActions:\n- Scope inserted.\n- Sampled 2R (atypical), 4R (adenocarcinoma), 7 (benign).\n- 10R inspected, too small.\n- No complications.\nPlan: Oncology.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the bronchoscopy suite for staging of mediastinal lymphadenopathy. Under moderate sedation, a linear EBUS bronchoscope was introduced. A systematic evaluation of the mediastinum was conducted. Station 2R was identified (24mm) and sampled with a 22G needle; ROSE indicated atypia. Station 4R (31mm) demonstrated distinct malignant features and was sampled; cytology confirmed adenocarcinoma. Station 7 (18mm) yielded benign lymphoid tissue. Station 10R was visualized but deemed sub-centimeter and not sampled. The procedure concluded without adverse events.",
            3: "CPT Justification (31653):\n- EBUS-TBNA performed on 3 distinct mediastinal stations.\n- Station 2R: Aspiration performed.\n- Station 4R: Aspiration performed.\n- Station 7: Aspiration performed.\n- Ultrasound guidance utilized for all needle passes.\n- Station 10R visualized but not aspirated (does not count toward sampling total).\n- Pathological evidence obtained confirming malignancy in 4R.",
            4: "Resident Procedure Note:\nPre-op: Lymphadenopathy.\nStaff: Dr. Chen.\nSteps:\n1. Time out.\n2. Sedation (Fentanyl/Versed).\n3. EBUS scope to trachea.\n4. Sampled 2R, 4R, 7. ROSE showed cancer in 4R.\n5. 10R looked small, skipped.\n6. Pt tolerated well.\nPlan: Onc consult.",
            5: "dictation for patient roberto martinez dob 03/15/67 date of service today... we did the ebus tbna for that big node indicated for malignancy eval anesthesia was moderate sedation lidocaine used... findings scope went down fine 2R was 24mm heterogenous 5 passes rose said atypical 4R was 31mm hypoechoic 4 passes rose said adenocarcinoma 7 was 18mm 3 passes benign... 10R was small didnt touch it... no complications minimal bleeding suctioned out... impression ebus tbna successful malignancy in 4R plan oncology... end dictation.",
            6: "Endobronchial Ultrasound with Transbronchial Needle Aspiration. 62mm right paratracheal lymphadenopathy, evaluate for malignancy. Moderate sedation with Fentanyl 100mcg IV, Midazolam 4mg IV. Topical lidocaine 2% 20mL. Linear EBUS bronchoscope advanced through oral route. Systematic mediastinal survey performed. Station 2R: 24mm, heterogeneous, oval shape. 5 passes with 22G needle. ROSE: adequate, atypical cells present. Station 4R: 31mm, round, hypoechoic center. Elastography score 3. 4 passes performed. ROSE: malignant cells identified, consistent with adenocarcinoma. Station 7: 18mm, homogeneous echo pattern. 3 passes performed. ROSE: benign lymphoid tissue. Station 10R: 12mm, not sampled. No complications.",
            7: "[Indication]\nEvaluation of 62mm right paratracheal lymphadenopathy.\n[Anesthesia]\nModerate sedation (Fentanyl/Midazolam) + local Lidocaine.\n[Description]\nLinear EBUS employed. Systematic survey completed. \n- Station 2R sampled (5 passes, atypical).\n- Station 4R sampled (4 passes, adenocarcinoma).\n- Station 7 sampled (3 passes, benign).\n- Station 10R inspected only.\n[Plan]\nRefer to Oncology for staging.",
            8: "The patient arrived for evaluation of a large right paratracheal lymph node. After consent and sedation, we introduced the linear EBUS scope. We began by surveying the mediastinum. We located Station 2R, which appeared heterogeneous, and performed five needle passes, yielding atypical cells. Moving to Station 4R, the ultrasound showed a hypoechoic center; four passes confirmed adenocarcinoma. Station 7 was also sampled three times, showing benign tissue. We decided against sampling Station 10R as it was below the size threshold. The procedure was completed with only minimal bleeding.",
            9: "Procedure: Endobronchial Ultrasound with Transbronchial Needle Aspiration.\nAction: The mediastinum was interrogated. Station 2R was accessed (5 passes). Station 4R was accessed (4 passes), yielding malignant cells. Station 7 was accessed (3 passes). Station 10R was visualized but not accessed.\nResult: Malignancy verified in 4R."
        },
        2: { # Emma Thompson (Peds Rigid Bronch FB Removal 31635)
            1: "Indication: FBA (peanut), R mainstem.\nAnesthesia: GA, spont vent.\nProcedure: Rigid bronch (3.5mm).\nFindings: Peanut fragment R mainstem.\nAction: Optical forceps used. FB removed intact.\nResult: Airway clear. Mucosa mild edema.\nPlan: Observe, CXR.",
            2: "PROCEDURE NOTE: Pediatric Rigid Bronchoscopy for Foreign Body Retrieval.\nFollowing the induction of general anesthesia, a 3.5mm Storz rigid bronchoscope was introduced. The larynx and trachea were patent. Upon inspection of the right mainstem bronchus, an organic foreign body consistent with a peanut was visualized approximately 2cm distal to the carina. Optical forceps were utilized to grasp the object. The bronchoscope and forceps were withdrawn in unison to ensure intact removal. Re-inspection confirmed the airway was free of residual particulate matter.",
            3: "CPT Code: 31635 (Bronchoscopy, rigid or flexible, with removal of foreign body).\nTechnique: Rigid bronchoscopy utilizing 3.5mm pediatric scope.\nLocation: Right Mainstem Bronchus.\nDetails: Visualization of organic foreign body (peanut). Use of optical forceps for extraction. Complete removal achieved. Post-extraction survey of RUL, RML, RLL and Left system confirmed patency.",
            4: "Procedure: Rigid Bronch FB Removal\nPatient: Emma T (3yo)\nStaff: Dr. Martinez\nSteps:\n1. GA, spontaneous breathing maintained.\n2. 3.5mm rigid scope inserted.\n3. Found peanut in RMS.\n4. Grabbed with optical forceps.\n5. Pulled everything out together.\n6. Re-looked: airway clear.\nPlan: Overnight obs.",
            5: "note for emma thompson 3 year old female came in with wheezing after eating peanuts... did the rigid bronchoscopy today under GA... used the 3.5 storz scope saw the peanut in the right mainstem about 2cm down... used the optical forceps to grab it it was a bit friable but got it all out intact... checked the other lobes right upper middle lower and left side all clear... suctioned some secretions... mild edema no bleeding... extubated fine... dr martinez attending present.",
            6: "Rigid Bronchoscopy with Foreign Body Removal. General anesthesia with spontaneous ventilation. A 3.5mm Storz pediatric rigid bronchoscope was introduced via the mouth under direct laryngoscopy. The vocal cords were visualized and appeared normal. The bronchoscope was advanced into the right mainstem bronchus. A foreign body was visualized 2cm distal to the carina - a tan-brown, irregular object consistent with a peanut fragment. Optical forceps were advanced through the rigid bronchoscope. The peanut fragment was grasped carefully. The foreign body was removed intact. Final inspection showed complete foreign body removal.",
            7: "[Indication]\nSuspected foreign body aspiration (peanut) in 3yo female.\n[Anesthesia]\nGeneral anesthesia, spontaneous ventilation maintained.\n[Description]\n3.5mm Rigid scope advanced. Peanut fragment identified in Right Mainstem. Extracted using optical forceps. Re-inspection of all lobes negative for residue.\n[Plan]\nPost-op CXR. Discharge tomorrow if stable.",
            8: "Emma, a 3-year-old female, was brought to the OR for suspected aspiration. Under general anesthesia, we inserted a pediatric rigid bronchoscope. We navigated to the right mainstem bronchus where we found a peanut fragment causing partial occlusion. Using optical forceps, we carefully grasped the peanut and removed it intact along with the scope to prevent it from breaking apart. We then re-inserted the scope to verify that the right lung and left lung were completely clear of debris.",
            9: "Procedure: Rigid Bronchoscopy with Foreign Body Retrieval.\nTarget: Right mainstem bronchus.\nItem: Organic material (peanut).\nTechnique: The object was localized and clasped using optical forceps. The object was withdrawn successfully. The airway was surveyed and found to be patent."
        },
        3: { # Aisha Patel (Thoracentesis 32555)
            1: "Procedure: US-Guided Thoracentesis.\nSite: R chest, 8th ICS.\nFluids: 420mL turbid yellow removed.\nLabs: pH 7.18, Glucose 32.\nFindings: Complicated effusion.\nPlan: Consult Thoracic for chest tube.",
            2: "PROCEDURE: Therapeutic and Diagnostic Thoracentesis.\nUnder ultrasound guidance, a pocket of complex pleural fluid was identified in the right hemithorax. Following sterile preparation and local anesthesia, an 18-gauge catheter was introduced into the 8th intercostal space. Approximately 420 mL of turbid, viscid fluid was aspirated. Analysis revealed a pH of 7.18 and glucose of 32 mg/dL, indicative of a complicated parapneumonic effusion. The procedure was terminated, and the patient referred for tube thoracostomy.",
            3: "Billing Code: 32555 (Thoracentesis with imaging guidance).\nDocumentation of Guidance: Ultrasound used to verify fluid depth (4.8cm) and complex nature prior to needle entry.\nVolume: 420 mL removed.\nProcessing: Samples sent for pH, Cell Count, Culture, Cytology.\nMedical Necessity: Complicated parapneumonic effusion (pH 7.18) requiring drainage.",
            4: "Procedure: Thoracentesis\nAttending: Dr. Mendez\nSteps:\n1. US check: R effusion.\n2. Local lidocaine.\n3. Needle in 8th ICS.\n4. Drained 420cc cloudy fluid.\n5. Pulled needle, bandaged.\nNote: Fluid looks infected (low pH). Needs chest tube.",
            5: "procedure note for aisha patel... ultrasound guided thoracentesis right side... saw the fluid on echo complex looking debris... prepped with betadine numbed with lido... put the 18g catheter in got out 420ml of turbid yellow fluid hard to drain... sent for labs immediate ph was 7.18 glucose 32 so its complicated... no pneumothorax on post xray... plan is antibiotics and call surgery for a chest tube likely needs tpa dnase.",
            6: "Diagnostic thoracentesis revealing complicated parapneumonic effusion based on pH 7.18, low glucose, and turbid appearance. Ultrasound examination: Right pleural effusion with maximum depth 4.8 cm, echogenic/complex appearance with debris. Ultrasound-guided placement of 18-gauge catheter. Initial fluid: turbid, cloudy yellow appearance. Total volume removed: 420 mL. Fluid with high viscosity, difficult drainage. Post-procedure ultrasound: residual complex effusion, no pneumothorax.",
            7: "[Indication]\nPersistent right pleural effusion post-pneumonia.\n[Anesthesia]\nLocal Lidocaine 1%.\n[Description]\nUltrasound localized complex fluid. 18G catheter inserted. 420mL turbid fluid aspirated. Catheter removed.\n[Plan]\nFluid analysis shows pH 7.18. Consult Thoracic Surgery for tube thoracostomy.",
            8: "Aisha presented with a persistent right-sided effusion. We performed an ultrasound which showed complex fluid. After numbing the area, we inserted a catheter into the 8th intercostal space. We were able to drain 420 mL of cloudy, thick fluid. Bedside analysis showed a very low pH, suggesting a complicated infection. We finished the drainage and ordered a chest x-ray, planning to consult surgery for a more permanent drain.",
            9: "Procedure: Ultrasound-guided pleural aspiration.\nTarget: Right pleural space.\nAction: Validated fluid pocket via imaging. Inserted catheter. Withdrew 420 mL of turbid fluid.\nAssessment: Complicated effusion (pH 7.18).\nDisposition: Thoracic surgery referral."
        },
        4: { # Christopher Hayes (Rigid Bronch, APC, Stent, Chest Tube 31641, 32551)
            1: "Dx: L mainstem stenosis (GPA).\nProc: Rigid bronch, APC, dilation, chest tube.\nFindings: L mainstem 90-100% occluded.\nAction: Radial cuts, APC, tissue shaving. Dilation attempted. Micro-perf to PA suspected. Sealed w/ fibrin glue. 14F chest tube placed for PTX.\nPlan: ICU, keep intubated.",
            2: "OPERATIVE REPORT: Rigid Bronchoscopy with Recanalization and Tube Thoracostomy.\nINDICATION: Wegener's granulomatosis with complete left mainstem (LMS) obstruction.\nPROCEDURE: The LMS was found to be totally occluded. Mechanical dilation and argon plasma coagulation (APC) were utilized to destroy the obstructing granulation tissue and shave the scar. During deep dilation, a micro-perforation communicating with a pulmonary vessel was suspected; fibrin sealant was immediately applied for hemostasis. Post-procedural imaging suggested a pneumothorax, necessitating the insertion of a 14F pigtail thoracostomy catheter. The patient was transferred to the ICU intubated.",
            3: "Coding Summary:\n- 31641: Bronchoscopy with destruction of tumor/relief of stenosis (APC and shaving of tissue in Left Mainstem).\n- 32551: Tube thoracostomy (Chest tube placed for pneumothorax complication).\n- Note: Dilation (31630) is bundled into 31641.\nComplication: Suspected airway-vascular fistula managed with fibrin glue.",
            4: "Procedure: Rigid Bronch & Chest Tube\nPt: Christopher Hayes\nSteps:\n1. Flex bronch showed L mainstem blocked.\n2. Rigid bronch inserted.\n3. Used APC and cuts to open airway (31641).\n4. Saw small bleeder/hole, used glue.\n5. CXR showed pneumothorax.\n6. Placed chest tube (32551).\nPlan: ICU.",
            5: "op note for christopher hayes history of gpa with airway stenosis... rigid bronchoscopy performed... left mainstem was totally socked in... used the knife and balloon then the rigid scope... did apc and shaving of the tissue to open it up... got down about 3cm then saw a pulsatile vessel likely pa... put fibrin glue in right away... patient had a pneumothorax on xray so we put in a 14 french chest tube... patient to picu intubated.",
            6: "Rigid bronchoscopy. Tube thoracostomy. Preoperative Diagnosis: Bronchial stenosis secondary to Granulomatosis with polyangiitis. Left mainstem obstruction. Radial knife cuts were performed within the proximal left mainstem followed by attempted CRE balloon dilatation. We performed APC to the left mainstem followed by gentle shaving of coagulated tissue. Instilled fibrin glue into the left mainstem. In the setting of a known airway tear and need for positive pressure ventilation, we felt that chest tube placement was warranted. A 14F pigtail catheter was placed without complications.",
            7: "[Indication]\nLeft mainstem obstruction due to GPA.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nRigid bronchoscopy utilized. APC and mechanical debridement used to recanalize LMS. Procedure complicated by suspected micro-perforation to PA. Hemostasis secured with fibrin glue. Post-op PTX noted.\n[Intervention]\n14F chest tube placed.\n[Plan]\nAdmit to ICU.",
            8: "Christopher underwent a rigid bronchoscopy to treat a severe blockage in his left mainstem bronchus caused by GPA. We used a combination of laser-like burning (APC) and physical shaving of the tissue to try and open the airway. During the process, we suspected a tiny tear connecting to a blood vessel, so we sealed it with glue to prevent bleeding. Because a chest x-ray showed a collapsed lung afterwards, we inserted a chest tube to re-expand it. He is currently stable in the ICU.",
            9: "Procedure: Rigid bronchoscopic recanalization and thoracostomy.\nAction: Employed APC and tissue shaving to relief stenosis in the left mainstem. Applied fibrin sealant to a suspected defect. Inserted a pleural drainage catheter for pneumothorax management."
        },
        5: { # Elizabeth Thompson (Pleuroscopy, Talc 32650)
            1: "Proc: Medical Pleuroscopy w/ Talc.\nFindings: Multifocal nodules parietal/visceral pleura.\nAction: Biopsies x10. 1250mL fluid drained. 5g Talc insufflated. 28F Chest tube placed.\nImpression: Suspicious for malignancy/lymphoma.",
            2: "PROCEDURE NOTE: Thoracoscopy with Pleurodesis.\nUnder monitored anesthesia care, a rigid pleuroscope was introduced into the right hemithorax. Inspection revealed extensive nodularity consistent with metastatic disease. Multiple biopsies were taken from the parietal and visceral surfaces. Given the complete lung re-expansion following drainage of 1,250 mL of exudate, talc poudrage (5g) was performed for pleurodesis. A 28F chest tube was positioned under direct visualization.",
            3: "Code: 32650 (Thoracoscopy, surgical; with pleurodesis).\nDetail: Rigid pleuroscope inserted. Pleural fluid evacuated. Biopsies taken (bundled). 5 grams of sterile talc insufflated for chemical pleurodesis. Chest tube placed.\nNote: 32551 is bundled into 32650.",
            4: "Procedure: Pleuroscopy & Talc\nPt: Elizabeth T\nSteps:\n1. Lateral decubitus.\n2. Trocar in 6th ICS.\n3. Drained 1.2L fluid.\n4. Saw nodules, took biopsies.\n5. Sprayed 5g Talc for pleurodesis.\n6. Chest tube in.\nPlan: Admit, pain control.",
            5: "procedure note for elizabeth thompson... medical pleuroscopy right side... recurrent effusion... mac anesthesia... put the trocar in drained 1250 ml yellow fluid... saw bunch of nodules on the pleura took like 10 biopsies... lung came up good so we did the talc pleurodesis with 5 grams... put a 28 french chest tube in... patient to floor pain meds ordered.",
            6: "Medical pleuroscopy revealing multifocal pleural nodules suspicious for metastatic disease or lymphoma. Talc pleurodesis performed given adequate lung expansion. Comprehensive tissue sampling obtained for diagnosis. 700 mL clear yellow fluid initially evacuated. 10 mm trocar inserted. 5 grams sterile graded talc insufflated. Talc distributed evenly throughout pleural space under direct visualization. 28 French chest tube placed under direct vision.",
            7: "[Indication]\nRecurrent exudative right pleural effusion.\n[Anesthesia]\nMAC.\n[Description]\nPleuroscopy performed. Multifocal nodules visualized and biopsied. 1250mL fluid drained. 5g Talc poudrage administered. 28F chest tube placed.\n[Plan]\nAdmit. Pain control. Water seal tomorrow.",
            8: "Elizabeth came in for a pleuroscopy to check her recurrent right-sided fluid. We drained over a liter of fluid and saw several nodules on the lining of her lung, which we biopsied. Since her lung expanded well after the fluid was gone, we sprayed medical talc into the space to seal it and prevent the fluid from coming back. We left a chest tube in place to help the lung heal and admitted her to the hospital.",
            9: "Procedure: Thoracoscopic poudrage.\nAction: Evacuated pleural effusion. Sampled pleural nodules. Insufflated 5g of talc agent to induce adherence. Positioned indwelling pleural catheter.\nAssessment: Successful pleurodesis."
        },
        6: { # Michael Brown (EBUS N2 Disease 31653) - Source note 6
            1: "Proc: EBUS-TBNA.\nIndication: RUL mass staging.\nStations Sampled: 4R, 7, 10R, 11R.\nROSE: 4R and 7 Malignant (Adeno).\nCode: 31653 (3+ stations).",
            2: "PROCEDURE: Endobronchial Ultrasound Staging.\nThe mediastinum was systematically mapped. Transbronchial needle aspiration was performed at stations 4R, 7, 10R, and 11R. Rapid on-site evaluation confirmed adenocarcinoma in the N2 nodes (4R and 7), confirming stage IIIA/N2 disease. Stations 10R and 11R were benign/reactive.",
            3: "Billing: 31653 (EBUS sampling 3+ stations).\nSupport: \n- Station 4R: Sampled.\n- Station 7: Sampled.\n- Station 10R: Sampled.\n- Station 11R: Sampled.\nTotal stations: 4.\nPathology: Malignancy confirmed in 4R/7.",
            4: "Procedure: EBUS\nPt: Michael Brown\nSteps:\n1. EBUS scope in.\n2. Sampled 4R, 7, 10R, 11R.\n3. ROSE said cancer in 4R and 7.\n4. No issues.\nPlan: Oncology.",
            5: "ebus tbna for michael brown staging lung mass... sampled four stations 4R 7 10R and 11R... rose positive for adeno in the mediastinal nodes 4r and 7... patient tolerated well mac anesthesia used... refer to onc for n2 disease.",
            6: "EBUS-TBNA with Rapid On-Site Evaluation. Indication: Lung mass RUL with mediastinal adenopathy - staging. 4R: 28mm, abnormal echotexture SAMPLED x4 passes. ROSE: Positive for malignancy. 7: 35mm, hypoechoic SAMPLED x4 passes. ROSE: Malignant cells present. 10R: 15mm SAMPLED x2 passes. 11R: 19mm SAMPLED x2 passes. Diagnosis: N2 disease confirmed.",
            7: "[Indication]\nStaging RUL Mass.\n[Anesthesia]\nMAC.\n[Description]\nEBUS-TBNA performed. \n- 4R: Malignant.\n- 7: Malignant.\n- 10R: Benign.\n- 11R: Benign.\n[Plan]\nMultidisciplinary Tumor Board.",
            8: "Michael underwent an EBUS procedure to stage a mass in his right upper lung. We sampled lymph nodes in four different areas: 4R, 7, 10R, and 11R. The pathologist in the room confirmed that the nodes in the center of the chest (4R and 7) contained cancer cells, which confirms N2 disease. We will refer him to oncology to discuss treatment options.",
            9: "Procedure: EBUS-guided needle aspiration.\nAction: Accessed stations 4R, 7, 10R, and 11R. \nResult: Malignant cytology identified in 4R and 7. Benign findings in 10R and 11R."
        },
        8: { # Kenji Nakamura (EMN, Radial EBUS, TBBx 31653, 31627, 31654, 31628, 31625, 31624)
            1: "Proc: EBUS + EMN + TBBx.\nEBUS: Stations 5, 7, 10L sampled (31653). N2/N3 positive.\nNav: EMN to LUL mass. Radial EBUS confirmed (31627, 31654).\nSampling: TBBx (31628), Brush, Needle. Endobronchial bx of anterior segment (31625). BAL (31624).\nDx: Stage IIIB Squamous Cell.",
            2: "OPERATIVE REPORT: Combined EBUS Staging and Electromagnetic Navigation.\nMediastinal staging via EBUS-TBNA of stations 5, 7, and 10L confirmed N2/N3 disease. Following this, electromagnetic navigation with radial EBUS verification was utilized to localize the peripheral LUL mass. Transbronchial biopsies were obtained. Additionally, endobronchial forceps biopsies were taken from a visible lesion in the anterior segment. Bronchoalveolar lavage was performed. Rapid pathology confirmed squamous cell carcinoma.",
            3: "Coding Summary:\n- 31653: EBUS sampling 3 stations (5, 7, 10L).\n- 31627: Navigation Add-on.\n- 31654: Radial EBUS Add-on.\n- 31628: Transbronchial Biopsy (LUL Mass).\n- 31625: Endobronchial Biopsy (Distinct lesion anterior segment).\n- 31624: BAL.\nDx: Squamous Cell CA.",
            4: "Procedure: EBUS/Nav Bronch\nPt: Kenji N.\nSteps:\n1. EBUS: Sampled 5, 7, 10L. Positive.\n2. Switched scopes.\n3. Navigated to LUL mass. Confirmed w/ Radial EBUS.\n4. Biopsied mass (TBBx).\n5. Saw tumor in airway, biopsied that too (Endobronchial).\n6. BAL.\nPlan: Chemo/Rad.",
            5: "bronchoscopy note for kenji nakamura... big case... started with ebus sampled stations 5 7 and 10L rose called it squamous... then did the superdimension navigation to the lul mass found it with radial probe... took biopsy brush needle... also saw tumor sticking out in the anterior segment biopsied that directly... did a wash too... patient has stage 3b cancer.",
            6: "EBUS-TBNA of mediastinal/hilar lymph nodes. Electromagnetic navigation bronchoscopy. Radial EBUS. Transbronchial biopsy of LUL mass. Station 5: Sampled. Station 7: Sampled. Station 10L: Sampled. EMN Navigation: Target LUL mass. Radial EBUS: Lesion >35mm. Sampling via guide sheath: Forceps biopsies, Brush cytology, Needle aspiration. Direct endobronchial biopsies: 4 specimens. ROSE: Squamous cell carcinoma confirmed. Stage IIIB.",
            7: "[Indication]\nLUL Mass, Staging.\n[Anesthesia]\nMAC.\n[Description]\n1. EBUS-TBNA: Stations 5, 7, 10L (Positive).\n2. EMN/REBUS: Localized LUL mass.\n3. Sampling: TBBx, needle, brush of mass. BAL.\n4. Endobronchial Bx: Anterior segment lesion.\n[Plan]\nOncology consult.",
            8: "Kenji underwent a complex bronchoscopy for a large lung mass. First, we used EBUS to sample lymph nodes in the AP window, subcarinal, and hilar areas; all showed cancer. We then used electromagnetic navigation and radial ultrasound to find the main tumor deep in the lung and biopsied it. We also noticed tumor tissue growing into the airway and biopsied that separately. The wash and biopsies confirmed squamous cell carcinoma.",
            9: "Procedure: Multimodal Bronchoscopic Staging and Diagnosis.\nAction: Performed ultrasonic needle aspiration of 3 nodal stations. Navigated to peripheral lesion utilizing electromagnetic guidance and radial ultrasound. Acquired parenchymal tissue (transbronchial). Acquired endoluminal tissue (endobronchial). Performed lavage.\nResult: Diagnosed Squamous Cell Carcinoma."
        },
        9: { # Jessica McBee (Rigid, Esophageal Stent Removal, Y-Stent 31631, 31635)
            1: "Indication: Esophageal stent migrated into airway. TE Fistula.\nProc: Rigid Bronch, FB Removal, Y-Stent.\nAction: Remnant esophageal stent removed piecemeal (31635). Large TEF exposed. Hybrid Y-stent placed (31631) to cover defect.\nPlan: ICU, nebulizers.",
            2: "OPERATIVE REPORT: Rigid Bronchoscopy with Esophageal Stent Extraction and Airway Stenting.\nThe patient presented with a migrated esophageal stent occluding the left mainstem. Using rigid bronchoscopic techniques and endoscopic scissors, the stent was extracted piecemeal from the trachea. This revealed a significant tracheoesophageal fistula involving the carina. To restore airway patency and seal the fistula, a dynamic Hybrid Y-stent was deployed. The limbs were seated in the mainstems and the tracheal limb secured.",
            3: "Coding Summary:\n- 31635: Removal of foreign body (Migrated esophageal stent fragments removed piecemeal).\n- 31631: Placement of tracheal stent (Y-stent placed covering trachea and mainstems).\nMedical Necessity: Critical airway obstruction and TE fistula.",
            4: "Procedure: Rigid Bronch Stent Removal/Placement\nPt: Jessica McBee\nSteps:\n1. Rigid scope inserted.\n2. Saw esophageal stent in airway.\n3. Cut it out piece by piece (FB removal).\n4. Saw huge fistula.\n5. Placed Y-stent to cover the hole.\n6. Intubated through stent.\nPlan: ICU.",
            5: "op note for jessica mcbee... airway emergency esophageal stent came through the trachea... used the rigid scope to pull the stent out had to cut it into pieces very difficult... huge hole te fistula found... placed a hybrid y stent to cover it up took a few tries but got it seated... intubated through the stent patient stable for now.",
            6: "Rigid bronchoscopy with esophageal stent removal. Dynamic Y (hybrid) Tracheal stent placement. Bronchoscopic intubation. 14mm ventilating rigid bronchoscope was inserted. The stents traversed into the left mainstem causing complete occlusion. Using multiple techniques to include rigid endoscopic scissors, APC, and forceps we slowly removed exposed wires and attempted to transect the stent. The majority of the stents had to be removed in a piecemeal fashion. Large defect at the main carina extending directly into the esophagus. Placed a 13X10X10 mm dynamic Y stent.",
            7: "[Indication]\nAirway obstruction from migrated esophageal stent.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy performed. Esophageal stent fragments removed piecemeal from airway. TE fistula identified. Dynamic Y-stent deployed to cover fistula and maintain patency.\n[Plan]\nICU, humidity, check CXR.",
            8: "Jessica required emergency rigid bronchoscopy because her esophageal stent had eroded into her airway, blocking her left lung. We carefully removed the metal stent pieces from her windpipe using heavy scissors and forceps. Once removed, we saw a large hole (fistula) between the airway and esophagus. We placed a silicone Y-shaped stent to cover this hole and keep her breathing passages open.",
            9: "Procedure: Rigid bronchoscopic foreign body extraction and airway stenting.\nAction: Retrieved migrated prosthetic material from the tracheobronchial tree. Deployed a bifurcated silicone stent (Y-stent) to bridge the resultant tracheoesophageal defect.\nResult: Airway patency restored."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the input file structure
    # Mapping Note Indices to their original data for transformation
    return [
        {"idx": 0, "orig_name": "Roberto Martinez", "orig_age": 58, "gender": "Male", "names": ["Juan Garcia", "Carlos Rodriguez", "Luis Hernandez", "Miguel Lopez", "Jose Gonzalez", "David Perez", "Jorge Sanchez", "Ricardo Ramirez", "Antonio Torres"]},
        {"idx": 1, "orig_name": "Roberto Martinez", "orig_age": 58, "gender": "Male", "names": ["Juan Garcia", "Carlos Rodriguez", "Luis Hernandez", "Miguel Lopez", "Jose Gonzalez", "David Perez", "Jorge Sanchez", "Ricardo Ramirez", "Antonio Torres"]}, # Fragment of 0
        {"idx": 2, "orig_name": "Emma Thompson", "orig_age": 3, "gender": "Female", "names": ["Sophia Miller", "Olivia Davis", "Ava Wilson", "Isabella Moore", "Mia Taylor", "Charlotte Anderson", "Amelia Thomas", "Harper Jackson", "Evelyn White"]},
        {"idx": 3, "orig_name": "Aisha Patel", "orig_age": 43, "gender": "Female", "names": ["Priya Sharma", "Anjali Gupta", "Fatima Ali", "Zara Khan", "Yasmin Ahmed", "Diya Singh", "Meera Kumar", "Sana Desai", "Riya Shah"]},
        {"idx": 4, "orig_name": "Christopher Hayes", "orig_age": 45, "gender": "Male", "names": ["James Owen", "Robert Cole", "Michael Wood", "William Bennett", "David Ross", "Richard Jenkins", "Joseph Perry", "Thomas Powell", "Charles Long"]},
        {"idx": 5, "orig_name": "Elizabeth Thompson", "orig_age": 71, "gender": "Female", "names": ["Mary Johnson", "Patricia Williams", "Linda Brown", "Barbara Jones", "Susan Garcia", "Margaret Miller", "Dorothy Davis", "Lisa Rodriguez", "Nancy Martinez"]},
        {"idx": 6, "orig_name": "Michael Brown", "orig_age": 60, "gender": "Male", "names": ["James Wilson", "John Moore", "Robert Taylor", "Michael Anderson", "William Thomas", "David Jackson", "Richard White", "Joseph Harris", "Charles Martin"]},
        {"idx": 7, "orig_name": "Michael Brown", "orig_age": 60, "gender": "Male", "names": ["James Wilson", "John Moore", "Robert Taylor", "Michael Anderson", "William Thomas", "David Jackson", "Richard White", "Joseph Harris", "Charles Martin"]}, # Fragment of 6
        {"idx": 8, "orig_name": "Kenji Nakamura", "orig_age": 67, "gender": "Male", "names": ["Hiroshi Tanaka", "Takeshi Yamamoto", "Yuki Sato", "Ken Suzuki", "Daiki Takahashi", "Haruto Watanabe", "Riku Ito", "Sora Kobayashi", "Kaito Saito"]},
        {"idx": 9, "orig_name": "Jessica McBee", "orig_age": 55, "gender": "Female", "names": ["Sarah Lewis", "Jessica Clark", "Emily Robinson", "Ashley Walker", "Jennifer Hall", "Amanda Young", "Melissa Allen", "Stephanie King", "Nicole Wright"]}
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
        
        # Handle duplicate/fragment notes mapping
        # 1 maps to 0's variations, 7 maps to 6's variations
        var_idx = idx
        if idx == 1: var_idx = 0
        if idx == 7: var_idx = 6
        
        # Iterate through the 9 styles
        for style_num in range(1, 10):
            
            # Deep copy the original note structure
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age
            # For the 3yo (Note 2), keep it pediatric (1-6 range)
            if idx == 2:
                new_age = max(1, min(6, orig_age + random.randint(-2, 3)))
            else:
                new_age = max(18, orig_age + random.randint(-3, 3))
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if var_idx in variations_text and style_num in variations_text[var_idx]:
                note_entry["note_text"] = variations_text[var_idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen with full dict)
                note_entry["note_text"] = f"Variation {style_num} for Note {idx} (Content Placeholder)"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Some entries might not have patient_age field explicitly, but we can add/update
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
    output_filename = output_dir / "synthetic_blvr_notes_part_034.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()