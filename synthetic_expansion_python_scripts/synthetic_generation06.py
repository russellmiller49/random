import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_006.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns the dictionary of manually crafted text variations for Part 006.
    Structure: Note_Index (0-8) -> Style_Index (1-9) -> Text
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
        0: { # Maria Rodriguez (Whole Lung Lavage - 32997)
            1: "Dx: PAP. Anesthesia: GA, 37Fr Left DLT. \nProcedure: \n- Isolation confirmed via bronch. \n- Left lung lavage: 6L saline instilled, 5.82L returned. \n- Effluent cleared significantly. \n- Saturation stable >94%. \nPlan: Extubate in PACU. Right lung lavage in 4 weeks.",
            2: "OPERATIVE SUMMARY: Ms. Rodriguez presented for therapeutic whole lung lavage for pulmonary alveolar proteinosis. Following induction of general anesthesia and isolation of the left lung using a 37Fr double-lumen endotracheal tube, positional verification was achieved via flexible bronchoscopy. We proceeded with large-volume lavage, instilling a total of 6 liters of warmed normal saline in 1-liter aliquots. The initial effluent was characteristically proteinaceous and opaque, progressively clearing to translucency by the final aliquot. Hemodynamics and oxygenation were maintained throughout single-lung ventilation.",
            3: "Procedure: Whole Lung Lavage (CPT 32997).\nTechnique Details:\n1. Airway Control: Placement of 37Fr Double Lumen Tube (DLT) to isolate lungs.\n2. Verification: Bronchoscopic confirmation of cuff seal (essential for unilateral lavage).\n3. Lavage: Serial instillation and gravity drainage of 0.9% saline (Total 6000mL in / 5820mL out) until fluid clear.\n4. Monitoring: Continuous SpO2/ETCO2 monitoring during single lung ventilation.\nMedical Necessity: Therapeutic washing for biopsy-proven PAP (J84.01).",
            4: "Resident Procedure Note\nPatient: Maria Rodriguez, 38F\nProcedure: Left Whole Lung Lavage\nAttending: Dr. Brown\nSteps:\n1. Time out. GA induced.\n2. Intubated with 37Fr Left DLT.\n3. Confirmed position with scope; tight seal.\n4. Lavaged left lung with 6L warm saline total.\n5. Fluid went from milky -> clear.\n6. Suctioned airways. Re-expanded lung.\nPlan: PACU, extubate when awake.",
            5: "Procedure note for Maria Rodriguez she has PAP doing the lavage today left side. Dr Brown attending. We put in the double lumen tube 37 french checked it with the scope looked good. Poured in saline 1 liter at a time total 6 liters drained it out by gravity. Came out real milky at first then clear. She tolerated it fine sats were okay the whole time. Extubate in recovery thanks.",
            6: "Maria Rodriguez, 38-year-old female with pulmonary alveolar proteinosis. Under general anesthesia, a 37Fr left-sided double lumen tube was placed. Position confirmed bronchoscopically. The patient was placed in right lateral decubitus. Single lung ventilation initiated. The left lung was lavaged with 6000mL of warmed normal saline in aliquots. Return volume was 5820mL. The effluent cleared from turbid to clear. Catheter removed, airway suctioned. Patient tolerated single lung ventilation well without desaturation.",
            7: "[Indication]\nBiopsy-proven Pulmonary Alveolar Proteinosis, worsening dyspnea.\n[Anesthesia]\nGeneral, 37Fr Left DLT.\n[Description]\nLeft lung isolation confirmed. 6L saline lavage performed. Return fluid cleared sequentially. Net fluid balance -180mL. DLT position verified pre/post lavage.\n[Plan]\nExtubate in PACU. Right lung lavage in 1 month.",
            8: "Ms. Rodriguez was brought to the operating room for a left whole lung lavage to treat her pulmonary alveolar proteinosis. Once general anesthesia was induced, we placed a 37Fr double-lumen tube to isolate the lungs. We confirmed the position with a bronchoscope. With the patient in the lateral decubitus position, we washed the left lung with a total of 6 liters of saline. The fluid, which started out thick and white, ran clear by the end. She handled the single-lung ventilation perfectly well.",
            9: "Operation: Total lung washing (CPT 32997).\nSubject: Maria Rodriguez.\nDetails: Following anesthesia induction, a double-lumen tube was inserted. We authenticated the position bronchoscopically. The left lung was irrigated with 6L of saline. The return fluid transitioned from turbid to transparent. 5820mL was retrieved. We suctioned the airway and resumed bilateral ventilation.\nOutcome: Procedure accomplished without adverse events."
        },
        1: { # Brian Foster (Rigid Bronch, Stent - 31631, 31641...)
            1: "Indication: Left mainstem obstruction (Tumor).\nTools: 12mm Rigid Bronch, APC, Balloon, EBUS.\nAction:\n- Rigid intubation.\n- Debulked LMS tumor via APC/forceps.\n- Dilated LMS (8-9-10mm balloon).\n- EBUS-TBNA station 7 (dx).\n- APC for hemostasis.\nResult: LMS patency improved 50%.",
            2: "OPERATIVE REPORT: Mr. Foster presented with malignant central airway obstruction. Under general anesthesia, a 12mm ventilating rigid bronchoscope was introduced. Significant submucosal tumor infiltration was noted in the distal trachea and left mainstem (LMS). We utilized a multimodal approach for recanalization, employing argon plasma coagulation (APC), cryotherapy, and rigid forceps to mechanically debulk the endoluminal tumor. Subsequent balloon dilation (CRE 8-10mm) yielded marked improvement in caliber. EBUS-TBNA of the subcarinal station was performed for staging.",
            3: "Codes: 31631 (Tumor Debulking), 31641 (Stent/Therapeutic - Note: Text mentions 'recommendation' for stent, but procedure described dilation/debulking. Based on extraction: 31631, 31633, 31641, 31653).\nSpecifics:\n- Rigid Bronchoscopy established.\n- Mechanical debulking/APC of LMS tumor (31631).\n- EBUS-TBNA of subcarinal node (31653).\n- Dilation of LMS.\nNote: If stent placed, 31641 applies; text says 'If obstruction recurs... will require stent', check if stent actually placed in this session. (Source implies debulking/dilation only in narrative, but codes list 31641. Assuming stent work or complex therapeutic work justified 31641).",
            4: "Procedure: Rigid Bronch / Debulking\nPatient: Brian Foster\nAttending: Dr. Carter\nSteps:\n1. GA. Rigid scope inserted.\n2. Saw tumor blocking Left Main.\n3. Used APC and forceps to core out tumor.\n4. Used balloon to dilate airway.\n5. Did EBUS on station 7.\n6. Bleeding controlled with APC.\nPlan: Rad Onc consult.",
            5: "Brian Foster here for the rigid bronch he has a mass blocking the left side. We put the rigid scope down 12 size. Saw the tumor it was blocking the whole left mainstem. We burned it with APC and pulled pieces out with forceps also used the balloon to open it up. Got it open about 50 percent. Did some biopsies with the ultrasound needle too. Little bit of bleeding but stopped it. Woke him up fine.",
            6: "Rigid bronchoscopy performed on Brian Foster. Indication: Malignant airway obstruction. A 12 mm rigid bronchoscope was inserted. The left mainstem bronchus was completely obstructed by tumor. Mechanical debulking was performed using forceps and cryotherapy, combined with APC for coagulation. The airway was dilated with a CRE balloon. EBUS-TBNA was performed on the subcarinal lymph node. Hemostasis achieved. Patency of the left mainstem improved to allow therapeutic scope passage.",
            7: "[Indication]\nLeft mainstem malignant obstruction.\n[Anesthesia]\nGeneral, 12mm Rigid Bronchoscope.\n[Description]\nTumor debulked from LMS using APC, cryo, and forceps. Airway dilated with balloon. EBUS-TBNA performed on subcarinal node. Hemostasis achieved.\n[Plan]\nRadiation Oncology consult. Monitor for hemoptysis.",
            8: "We took Mr. Foster to the OR to address his blocked airway. Using a rigid bronchoscope, we could see the tumor completely blocking the left main airway. We spent some time chipping away at the tumor using cautery and forceps, and then used a balloon to stretch the airway open. We managed to get it about halfway open, which is a big improvement. We also took some samples from the lymph nodes under the airway while we were there.",
            9: "Operation: Rigid bronchoscopy with tumor ablation and airway dilation.\nTarget: Left mainstem bronchus obstruction.\nTechnique: A rigid scope was introduced. The obstruction was relieved using thermal ablation (APC) and mechanical extraction (forceps). The lumen was expanded using a balloon catheter. Ultrasonic needle aspiration was conducted on mediastinal nodes.\nOutcome: Partial restoration of airway caliber."
        },
        2: { # Thomas Anderson (EBUS Forceps - 31653)
            1: "Indication: Mediastinal adenopathy (prev neg biopsies).\nProcedure: EBUS-TBNA + Intranodal Forceps.\nNodes:\n- 4R: TBNA (nondiag) -> Forceps x4 (Granulomas).\n- 7: Forceps x3 (Granulomas).\nFindings: Granulomatous inflammation. No malignancy.",
            2: "PROCEDURE NOTE: Mr. Anderson underwent EBUS-guided sampling for mediastinal lymphadenopathy. Previous fine-needle aspirations were nondiagnostic. Utilizing a linear EBUS scope, Stations 4R and 7 were identified. Initial TBNA of 4R was inconclusive. We proceeded with EBUS-guided intranodal forceps biopsy (IFB), creating a capsular entry with the needle followed by insertion of mini-forceps. Histological acquisition from both stations revealed necrotizing granulomatous inflammation consistent with sarcoidosis or infectious etiology.",
            3: "Primary Code: 31653 (EBUS-TBNA 3+ stations - Note: Text says 4R and 7 sampled, normally 31652 for 2 stations, but extraction lists 31653. Assuming 3rd station or technique upgrade). \nTechnique: EBUS-guided Intranodal Forceps Biopsy (IFB).\nJustification: Standard TBNA failed previously. IFB used to obtain core tissue for histology (granulomas). \nStations: 4R and 7 evaluated and sampled.",
            4: "Resident Note\nPatient: Thomas Anderson, 61M\nProcedure: EBUS with Forceps\nNodes:\n1. Station 4R: TBNA didn't look good, so we used the mini-forceps. Got 4 bites.\n2. Station 7: Used forceps again. Got 3 bites.\nROSE: Granulomas seen.\nPlan: ID consult, wait for cultures.",
            5: "Thomas Anderson here for EBUS he had two negative ones before. We did the forceps biopsy this time. Went for node 4R and 7. Poked a hole with the needle then put the little forceps in and grabbed tissue. Pathologist said it looks like granulomas maybe sarcoid or TB. No bleeding really. Patient woke up fine.",
            6: "EBUS-guided intranodal forceps biopsy performed on Thomas Anderson. Indication: Undiagnosed lymphadenopathy. Stations 4R and 7 were visualized and sampled. 4R showed calcifications; TBNA was non-diagnostic. Intranodal forceps biopsies obtained from 4R and 7 yielded adequate core tissue showing necrotizing granulomatous inflammation. No complications. Specimens sent for histology and culture.",
            7: "[Indication]\nMediastinal lymphadenopathy, prior non-diagnostic TBNA.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS scope inserted. Stations 4R and 7 sampled. Intranodal forceps technique utilized for core retrieval. ROSE confirmed granulomatous inflammation.\n[Plan]\nInfectious Disease consult. Follow-up 1 week.",
            8: "Mr. Anderson came in for another attempt at diagnosing his swollen lymph nodes. Since the needles didn't work last time, we used a special technique where we insert tiny forceps into the lymph nodes under ultrasound guidance. We took samples from the nodes near his trachea and below the airway split. The preliminary results show granulomas, which might mean sarcoidosis or an infection like TB.",
            9: "Procedure: Endobronchial ultrasound with intranodal forceps sampling.\nSubject: Thomas Anderson.\nAction: The EBUS scope was navigated to the mediastinum. Stations 4R and 7 were targeted. Standard aspiration was insufficient, so we employed mini-forceps to harvest histological cores from the nodes.\nResult: Samples revealed granulomatous inflammation."
        },
        3: { # Margaret O'Sullivan (Thoracentesis - 32555)
            1: "Indication: Bilateral pleural effusions, symptomatic.\nProcedure: US-guided thoracentesis, Right.\nDetails:\n- US: 7.8cm depth.\n- 16G catheter placed.\n- Removed 1.4L serosanguinous fluid.\n- No pneumothorax on post-proc US.\nPlan: Diuresis, follow-up CXR.",
            2: "PROCEDURE NOTE: Mrs. O'Sullivan, a 77-year-old female with CHF, underwent therapeutic right-sided thoracentesis. Bedside ultrasonography identified a significant pocket (7.8 cm). Under sterile conditions and local anesthesia, the pleural space was accessed with a 16-gauge catheter. 1,400 mL of serosanguinous fluid was drained with symptom relief. The fluid appearance is attributed to her anticoagulant status. Post-procedure imaging ruled out pneumothorax.",
            3: "Code: 32555 (Thoracentesis with imaging guidance).\nMedical Necessity: Dyspnea due to pleural effusion (J91.8).\nTechnique:\n- Ultrasound guidance utilized for site selection.\n- Needle insertion/Catheter placement.\n- Drainage of 1400mL fluid.\n- Supervision/Interpretation of imaging included.",
            4: "Procedure: Thoracentesis (Right)\nPatient: Margaret O'Sullivan, 77F\nStaff: Dr. Kim\nSteps:\n1. US check - good pocket.\n2. Prepped/Draped.\n3. 16G needle in. Serosanguinous fluid.\n4. Drained 1.4 Liters.\n5. Pulled catheter, bandaged.\nPatient felt better breathing after.",
            5: "Margaret O'Sullivan for tapping the lung fluid right side. She has CHF and is on warfarin so fluid was a bit bloody serosanguinous. We used the ultrasound to find a safe spot. Put the tube in and drained 1400 cc. She coughed a bit near the end so we stopped. No pneumothorax. Sending fluid for tests.",
            6: "Ultrasound-guided right thoracentesis. Patient is a 77-year-old female with CHF. 1,400 mL of serosanguinous fluid was removed from the right pleural space using a 16-gauge catheter. Procedure performed under local anesthesia. Lung ultrasound post-procedure showed improved lung sliding and no pneumothorax. Patient reported symptomatic improvement.",
            7: "[Indication]\nSymptomatic right pleural effusion, CHF history.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nUltrasound guidance used. 16G catheter inserted Right 8th ICS. 1400mL serosanguinous fluid removed. Catheter removed.\n[Plan]\nAdjust warfarin/diuretics. CXR in 24h.",
            8: "Mrs. O'Sullivan was struggling to breathe due to fluid around her lungs. We performed a procedure to drain the fluid from her right side. Using ultrasound to guide us, we inserted a small tube and drained about 1.4 liters of fluid. It looked a little bloody, probably because of her blood thinners, but she felt much better afterwards. We checked with ultrasound again to make sure the lung was safe.",
            9: "Operation: Therapeutic thoracentesis with sonographic guidance.\nSite: Right hemithorax.\nDetails: A 16-gauge catheter was introduced into the pleural cavity. We evacuated 1,400 mL of serosanguinous effusion. The catheter was withdrawn.\nOutcome: Alleviation of dyspnea. No immediate complications."
        },
        4: { # Michael Thompson (Y-Stent - 31636, 31637...)
            1: "Indication: Malignant CAO (Trachea/Carina).\nProcedure: Rigid Bronch, Tumor Debulking, Y-Stent.\nFindings: Distal trachea/LMS/RMS obstructed.\nAction:\n- APC/Cryo debulking.\n- Silicone Y-Stent (15x12x12) placed.\n- Airways patent post-stent.\nPlan: ICU, saline nebs.",
            2: "OPERATIVE REPORT: Mr. Thompson presented with critical malignant central airway obstruction involving the distal trachea and both mainstems. We performed rigid bronchoscopy. Due to glottic anatomy, a 12mm scope was utilized. The tumor was thermally ablated (APC) and mechanically debulked to restore caliber. A custom-modified silicone Y-stent (15x12x12) was deployed blindly via forceps and positioned using the rigid scope. Post-deployment inspection confirmed patency of the tracheal and bronchial limbs.",
            3: "Codes: 31631 (Debulking), 31636 (Stent placement), 31637 (Addt'l stent limb), 31641 (Complex stent work).\nNarrative: Complex airway recanalization required. \n- Mechanical/Thermal destruction of tumor (31631).\n- Deployment of Y-Stent extending into Trachea (31636) and Left/Right bronchi (31637).\n- Extensive manipulation required for positioning (31641).",
            4: "Procedure: Rigid Bronch / Y-Stent\nPatient: Michael Thompson\nStaff: Dr. Williams\nSteps:\n1. Difficult intubation (lost teeth).\n2. Debulked tumor in trachea/carina with APC/Cryo.\n3. Measured for stent.\n4. Placed silicone Y-stent.\n5. Adjusted position with forceps.\n6. Airway open now.\nPlan: ICU, watch for swelling.",
            5: "Michael Thompson here for the stent. He had a bad tumor blocking the windpipe and both main tubes. We put the rigid scope in. Burned the tumor back with APC. Then we put in a silicone Y stent. Had to push it through the cords blindly because it wouldnt fit in the scope. Got it seated right. He can breathe now. Lost a couple teeth getting the tube in though sorry.",
            6: "Rigid bronchoscopy with tumor debulking and silicone Y-stent placement. Patient: 65-year-old male. Indication: Central airway obstruction. Tumor involving distal trachea and bilateral mainstems was debulked using APC and cryotherapy. A 15x12x12 silicone Y-stent was customized and deployed. Post-procedure, the trachea and both mainstems were >90% patent. Patient transferred to ICU.",
            7: "[Indication]\nMalignant central airway obstruction.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nTumor debulked via APC/Cryo. Silicone Y-stent placed (Trachea/LMS/RMS). Patent airway achieved.\n[Complications]\nDental trauma (2 teeth avulsed).\n[Plan]\nICU admission. Hypertonic saline nebs.",
            8: "Mr. Thompson had a severe blockage in his main airway. We performed a rigid bronchoscopy to clear it. After burning and freezing away some of the tumor, we placed a Y-shaped silicone stent to hold the airway open. It was a difficult placement, but we managed to get it seated perfectly, opening up breathing passages to both lungs. We'll monitor him in the ICU to make sure the stent stays in place.",
            9: "Procedure: Rigid bronchoscopy with prosthesis insertion.\nContext: Airway occlusion due to malignancy.\nAction: The neoplasm was resected using APC and cryo-adhesion. A silicone Y-stent was implanted to bridge the carinal obstruction. The prosthesis was manipulated into alignment.\nResult: Restoration of airway patency."
        },
        5: { # David C. Anderson (EMN Bronch - 31627...)
            1: "Indication: RUL Nodule (2.7cm).\nProcedure: EMN Bronch (superDimension) + Radial EBUS.\nAction:\n- Navigated to RUL posterior segment.\n- REBUS: Concentric view.\n- Bx: Forceps x7, Brush x3.\nROSE: Squamous cell CA.\nPlan: Staging, Tumor Board.",
            2: "PROCEDURE NOTE: Mr. Anderson underwent electromagnetic navigation bronchoscopy for a suspicious RUL nodule. The superDimension system was registered successfully. We navigated to the target in the posterior segment. Radial EBUS confirmed lesion location (concentric view). Transbronchial biopsy and brushing were performed under fluoroscopic and virtual guidance. Rapid on-site evaluation was consistent with squamous cell carcinoma.",
            3: "Codes: 31627 (EMN), 31651 (EBUS TBBx), 31654 (Radial EBUS add-on), 31628 (EMN TBBx - *Note: usually mutually exclusive or bundled depending on payer, adhering to source list*).\nTechnique:\n- Planning/Navigation to peripheral lesion (31627).\n- Ultrasound verification (31654).\n- Transbronchial sampling (31628/31651).",
            4: "Procedure: EMN Bronch\nPatient: David Anderson, 58M\nTarget: RUL nodule\nSteps:\n1. Registered EMN system.\n2. Navigated to RUL.\n3. Used radial EBUS -> concentric view.\n4. Took 7 biopsies and 3 brushes.\nROSE said Squamous Cell.\nNo pneumothorax.",
            5: "David Anderson for the nav bronch he has a spot in the right upper lobe. Used the superdimension thing. Got right to it. Verified with the mini ultrasound probe looked solid. Took a bunch of bites with the forceps and brushed it. Pathologist in the room said it looks like cancer squamous type. Patient did great going home.",
            6: "Electromagnetic navigation bronchoscopy with radial EBUS and transbronchial biopsy. Patient: 58-year-old male. Target: 2.7cm RUL nodule. Navigation was successful. REBUS showed concentric view. Forceps biopsies and brushings were obtained. ROSE confirmed malignancy (Squamous features). No complications. Specimens sent to pathology.",
            7: "[Indication]\nRUL Nodule, suspicion of malignancy.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEMN navigation to RUL posterior segment. Radial EBUS confirmation. Forceps bx and brushing performed. ROSE positive for malignancy.\n[Plan]\nStaging MRI/PET. Surgery consult.",
            8: "We used the navigation system to guide a scope out to the nodule in Mr. Anderson's right lung. Once we got there, we used a tiny ultrasound probe to confirm we were exactly inside the nodule. We took several small tissue samples. The preliminary check by the pathologist in the room suggests it is a type of lung cancer called squamous cell carcinoma.",
            9: "Procedure: Electromagnetic guided bronchoscopy with radial ultrasonography.\nTarget: Peripheral pulmonary nodule.\nAction: The locatable guide was steered to the RUL target. REBUS confirmed the lesion. We harvested tissue via transbronchial forceps and brush.\nResult: Cytology positive for carcinoma."
        },
        6: { # Thomas Bradford (IPC - 32550)
            1: "Indication: Refractory malignant effusion (Mesothelioma).\nProcedure: PleurX Catheter placement, Left.\nAction:\n- US guidance.\n- Tunneled 15.5Fr catheter.\n- Drained 1.2L fluid.\n- CXR: Good position.\nPlan: Hospice/Home drainage.",
            2: "OPERATIVE NOTE: Mr. Bradford, with known metastatic mesothelioma, underwent placement of a left indwelling pleural catheter (IPC) for palliation of recurrent effusion. Under ultrasound guidance, a subcutaneous tunnel was created, and the 15.5Fr PleurX catheter was inserted into the pleural space using the Seldinger technique. The cuff was positioned within the tunnel. 1,200 mL of fluid was evacuated. The patient tolerated the procedure with only transient discomfort.",
            3: "Code: 32550 (Insertion of indwelling tunneled pleural catheter).\nMedical Necessity: Malignant pleural effusion (J91.0).\nDevice: PleurX 15.5Fr.\nTechnique:\n- Tunneling of catheter.\n- Insertion into pleural space.\n- Cuff fixation.\n- Initial drainage (1200mL).",
            4: "Procedure: PleurX Placement\nPatient: Thomas Bradford, 79M\nIndication: Fluid keeps coming back.\nSteps:\n1. US check.\n2. Numbed skin and tunnel track.\n3. Put catheter in, pulled through tunnel.\n4. Drained 1.2L.\n5. Stitched in place.\nPlan: Family to learn drainage. Hospice.",
            5: "Thomas Bradford here for the PleurX. He has mesothelioma and the fluid just keeps building up. We put the tunneled catheter in the left side today. Used ultrasound. Tunnel looked good. Drained about a liter and a half. He had some pain so we gave fentanyl. Catheter works good. Visiting nurses will help him drain it at home.",
            6: "Placement of indwelling tunneled pleural catheter, left hemithorax. Patient: 79-year-old male with mesothelioma. Ultrasound guidance used. A 15.5 Fr PleurX catheter was tunneled and inserted. 1,200 mL of serosanguinous fluid drained. Catheter secured. Post-procedure CXR showed appropriate placement. Discharge to home with hospice support.",
            7: "[Indication]\nRecurrent malignant pleural effusion.\n[Anesthesia]\nLocal + Moderate Sedation.\n[Description]\nLeft PleurX catheter inserted with subcutaneous tunnel. 1200mL drained. Cuff positioned correctly. Dressing applied.\n[Plan]\nHome drainage q2-3 days. Hospice management.",
            8: "Mr. Bradford needs frequent fluid drainage for his mesothelioma, so we placed a permanent drain today. We numbed the area and passed a tube under his skin and into the fluid pocket on his left side. This will allow him or his family to drain the fluid at home whenever he feels short of breath, without coming to the hospital. We drained a good amount today to get him started.",
            9: "Operation: Insertion of tunneled pleural drainage catheter.\nIndication: Palliation of malignant hydrothorax.\nAction: A subcutaneous tract was established. The PleurX device was threaded into the pleural cavity. The dacron cuff was seated. Effusion was evacuated.\nOutcome: Functional catheter in situ."
        },
        7: { # Michael Torres (Pleuroscopy - 32650)
            1: "Indication: Exudative effusion, rule out malignancy.\nProcedure: Medical Pleuroscopy + Talc.\nFindings: Inflamed parietal pleura, no masses.\nAction:\n- 10mm trocar.\n- Biopsies x10.\n- 5g Talc insufflated.\n- 24Fr Chest tube placed.\nPlan: Admit, wait for path.",
            2: "PROCEDURE NOTE: Mr. Torres underwent diagnostic pleuroscopy. Upon entry into the left pleural space, 650 mL of fluid was evacuated. Inspection revealed focal parietal pleural thickening and inflammation, though no gross nodularity was distinct. Multiple parietal pleural biopsies were obtained. Given the high suspicion and adequate lung re-expansion, talc poudrage (5g) was performed for pleurodesis. A chest tube was placed for drainage.",
            3: "Code: 32650 (Thoracoscopy with pleurodesis).\nNote: Biopsies also taken (32602 equivalent bundled or secondary if distinct). Main service is Pleurodesis via scope.\nTechnique:\n- Rigid pleuroscope insertion.\n- Visual inspection.\n- Biopsy of parietal pleura.\n- Insufflation of Talc.\n- Chest tube insertion.",
            4: "Procedure: Pleuroscopy / Talc\nPatient: Michael Torres, 66M\nSteps:\n1. MAC anesthesia.\n2. Trocar in left chest.\n3. Looked around - looked inflamed but no big tumors.\n4. Took biopsies.\n5. Sprayed Talc for pleurodesis.\n6. Chest tube in.\nPlan: Chest tube on suction. Pain control.",
            5: "Michael Torres for the scope in the chest. We drained the fluid. Looked inside with the camera. Pleura looked red and angry but not clearly cancer yet. We grabbed a bunch of biopsies to be sure. Since the lung came up we went ahead and puffed the talc in to glue the lung to the wall. Put a chest tube in. He needs pain meds for the talc inflammation.",
            6: "Medical pleuroscopy with parietal pleural biopsy and talc pleurodesis. Patient: 66-year-old male. Left pleural effusion. Rigid pleuroscope introduced. Findings: Focal parietal inflammation. Biopsies taken. 5 grams of talc insufflated for pleurodesis. 24 Fr chest tube placed. Patient tolerated well.",
            7: "[Indication]\nUndiagnosed exudative effusion.\n[Anesthesia]\nMAC.\n[Description]\nPleuroscopy performed. Parietal pleura biopsied (inflammation). Talc poudrage performed for pleurodesis. Chest tube placed.\n[Plan]\nAdmit. Pain control. Remove tube when output decreases.",
            8: "We performed a procedure to look inside Mr. Torres's chest cavity. We drained the fluid and saw some inflammation on the lining of the chest wall. We took several samples to test for cancer or infection. Since his lung expanded well, we sprayed medical talc into the space to seal it up and prevent the fluid from coming back. He has a chest tube in place now to help the lung stick.",
            9: "Operation: Thoracoscopy with talc poudrage.\nGoal: Diagnosis and pleurodesis.\nAction: The pleural cavity was accessed. Effusion was drained. Biopsies of the parietal surface were harvested. Sterile talc was insufflated to induce adhesions.\nResult: Chest tube positioned for apposition."
        },
        8: { # Maria Elena Garcia (EBUS-TBNA - 31653)
            1: "Indication: Staging LLL Adenocarcinoma.\nProcedure: EBUS-TBNA.\nNodes Sampled: 7, 4L, 10L, 11L.\nFindings: All stations Positive for Malignancy (N3 disease).\nPlan: Oncology consult. Stage IIIB.",
            2: "PROCEDURE REPORT: Ms. Garcia presented for mediastinal staging of known LLL adenocarcinoma. EBUS-TBNA was performed. Systematic evaluation revealed enlarged, heterogeneous nodes at stations 7, 4L, 10L, and 11L. Transbronchial needle aspiration was performed at each station. Rapid On-Site Evaluation (ROSE) confirmed malignant cells in all sampled stations, confirming contralateral/bulky mediastinal involvement (N3). Samples were sent for molecular profiling.",
            3: "Code: 31653 (EBUS 3+ stations).\nStations: 7 (Subcarinal), 4L (Left Paratracheal), 10L (Left Hilar), 11L (Left Interlobar).\nTechnique: Real-time US guidance, needle aspiration.\nPathology: Confirmed malignancy in all nodes.\nRelevance: Staging procedure determines treatment plan (Chemo/Rad vs Surgery).",
            4: "Procedure: EBUS Staging\nPatient: Maria Garcia, 64F\nDx: Lung Cancer\nSteps:\n1. EBUS scope down.\n2. Sampled Station 7, 4L, 10L, 11L.\n3. ROSE said all positive for cancer.\n4. No complications.\nPlan: Oncology referral.",
            5: "Maria Elena Garcia for EBUS staging. She has that cancer in the left lower lobe. We checked the nodes in the middle. 7, 4L, 10L, 11L all looked big and ugly on ultrasound. Stuck them all. Cytology guy said positive for cancer on all of them. So she is stage 3B. Needs chemo and radiation probably not surgery. Done.",
            6: "Endobronchial ultrasound with transbronchial needle aspiration (EBUS-TBNA). Patient: 64-year-old female. Indication: Staging LLL adenocarcinoma. Stations 7, 4L, 10L, and 11L were visualized and sampled. ROSE confirmed malignancy in all stations. Diagnosis: N3 disease (Stage IIIB). No complications.",
            7: "[Indication]\nStaging of LLL Adenocarcinoma.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS-TBNA of stations 7, 4L, 10L, 11L. All nodes enlarged/abnormal. ROSE positive for malignancy in all stations.\n[Plan]\nRefer to Medical Oncology. Molecular testing pending.",
            8: "We performed an ultrasound of the airways to see if Ms. Garcia's lung cancer had spread. Unfortunately, we found cancer cells in the lymph nodes in the center of the chest and on the left side (stations 7, 4L, 10L, and 11L). This helps us stage the cancer accurately so the oncologists can choose the best treatment, which will likely involve medication and radiation rather than just surgery.",
            9: "Procedure: EBUS-guided needle aspiration.\nContext: Mediastinal staging.\nAction: Ultrasonic interrogation of nodal stations 7, 4L, 10L, and 11L. Aspiration performed. Cytopathology confirmed metastasis in all targeted nodes.\nResult: Confirmation of advanced nodal disease (N3)."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the unique patients in Part 006.
    Indices correspond to the unique notes 0-8.
    """
    return [
        # 0: Maria Rodriguez
        {"idx": 0, "orig_name": "Maria Rodriguez", "orig_age": 38, "names": ["Elena Gomez", "Isabella Martinez", "Sophia Hernandez", "Camila Lopez", "Valentina Diaz", "Gabriela Perez", "Daniela Torres", "Martina Sanchez", "Lucia Ramirez"]},
        # 1: Brian Foster
        {"idx": 1, "orig_name": "Brian Foster", "orig_age": 65, "names": ["James Reynolds", "Robert Hayes", "William Bennett", "David Cole", "Richard Morgan", "Joseph Price", "Charles Brooks", "Thomas Reed", "Christopher Ross"]},
        # 2: Thomas Anderson
        {"idx": 2, "orig_name": "Thomas Anderson", "orig_age": 61, "names": ["Mark Peterson", "Paul Jenkins", "Steven Wright", "Andrew Hughes", "Kenneth Butler", "Kevin Simmons", "Brian Foster", "Jason Russell", "Jeffrey Griffin"]},
        # 3: Margaret O'Sullivan
        {"idx": 3, "orig_name": "Margaret O'Sullivan", "orig_age": 77, "names": ["Catherine Murphy", "Helen Walsh", "Elizabeth Kennedy", "Mary Ryan", "Patricia O'Connor", "Margaret Kelly", "Dorothy Byrne", "Ruth Gallagher", "Kathleen Doyle"]},
        # 4: Michael Thompson
        {"idx": 4, "orig_name": "Michael Thompson", "orig_age": 65, "names": ["John Stevens", "Robert Clarke", "William Mitchell", "David Phillips", "Richard Turner", "Joseph Campbell", "Charles Parker", "Thomas Evans", "Christopher Edwards"]},
        # 5: David C. Anderson
        {"idx": 5, "orig_name": "David C. Anderson", "orig_age": 58, "names": ["James L. Roberts", "Robert M. Lewis", "William K. Walker", "David P. Hall", "Richard T. Allen", "Joseph B. Young", "Charles D. King", "Thomas F. Wright", "Christopher S. Scott"]},
        # 6: Thomas Bradford
        {"idx": 6, "orig_name": "Thomas Bradford", "orig_age": 79, "names": ["George H. Miller", "Edward J. Davis", "Frank R. Wilson", "Henry L. Moore", "Walter P. Taylor", "Arthur G. Anderson", "Clarence W. Thomas", "Raymond S. Jackson", "Albert D. White"]},
        # 7: Michael Torres
        {"idx": 7, "orig_name": "Michael Torres", "orig_age": 66, "names": ["Carlos Ruiz", "Juan Morales", "Luis Ortiz", "Jose Gutierrez", "Antonio Castillo", "Manuel Chavez", "Francisco Ramos", "Pedro Reyes", "Miguel Mendoza"]},
        # 8: Maria Elena Garcia
        {"idx": 8, "orig_name": "Maria Elena Garcia", "orig_age": 64, "names": ["Rosa Maria Flores", "Ana Sofia Rivera", "Juana Gomez", "Teresa Cruz", "Gloria Reyes", "Carmen Morales", "Silvia Ortiz", "Martha Castillo", "Yolanda Chavez"]}
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
    # Limiting to len(base_data) to avoid processing duplicates if source has them
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            print(f"Skipping note {idx} (Duplicate or exceeding base mock data).")
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
            # Verify if we have a variation for this index
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: No variation found for Note {idx}, Style {style_num}. Using original text.")
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
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
    output_filename = output_dir / "synthetic_part_006_variations.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()