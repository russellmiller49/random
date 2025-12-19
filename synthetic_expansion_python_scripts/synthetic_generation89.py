import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_089.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns the dictionary of manually crafted text variations for the 10 notes 
    found in consolidated_verified_notes_v2_8_part_089.json.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Edward Wilson (LUL, 14mm, TBNA/Bx/Brush, ROSE Neg)
            1: "Pre-op: 14mm LUL nodule. \nAnesthesia: GA, 8.0 ETT.\nProcedure:\n- Monarch robot nav to LB1+2.\n- rEBUS: Adjacent view.\n- Sampling: 21G TBNA (x6), Forceps (x6), Protected Brush.\n- ROSE: No malignancy.\nComplications: None.\nPlan: Recovery, D/C if stable.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the endoscopy suite for evaluation of a 14mm peripheral pulmonary nodule in the Apicoposterior Segment of the Left Upper Lobe. Following induction of general anesthesia, the Monarch robotic platform was deployed. Electromagnetic navigation was registered with an error of 4.6mm. Upon reaching the target, radial EBUS demonstrated an adjacent acoustic signature. Transbronchial needle aspiration (21G), forceps biopsy, and cytological brushing were performed under continuous visualization. Rapid On-Site Evaluation (ROSE) was negative for malignant neoplasm. Hemostasis was achieved without intervention.",
            3: "Procedure: Bronchoscopy with Computer-Assisted Navigation (31627) and EBUS (31654).\nTarget: LUL Nodule (14mm).\nTechnique:\n1. Navigated to LB1+2 using electromagnetic guidance.\n2. Confirmed target via rEBUS (Adjacent).\n3. TBNA: 21G needle, 6 passes (31629).\n4. Biopsy: Standard forceps, 6 samples (31628).\n5. Brushing: Protected brush (31623).\nOutcome: Samples to patho. ROSE negative.",
            4: "Resident Note\nPt: Wilson.\nProc: Robotic Bronch LUL.\nSteps:\n1. Time out. GA induced. ETT 8.0.\n2. Monarch scope inserted. Registration 4.6mm error.\n3. Navigated to LUL (Apicoposterior).\n4. rEBUS confirmed lesion (adjacent).\n5. TBNA x6, Bx x6, Brush x1.\n6. ROSE: No malignancy.\n7. Pt tolerated well.\nPlan: CXR, D/C.",
            5: "Procedure note for Mr Wilson we did the robotic bronch today for that LUL nodule. General anesthesia tube size 8.0 registration was okay 4.6mm. Went out to the apicoposterior segment found it with rebus adjacent view. Did the needle biopsy 21 gauge then the forceps then the brush. ROSE said no cancer seen. No bleeding really. Extubated fine sent to recovery check a chest xray.",
            6: "The patient underwent robotic bronchoscopy for a 14mm LUL nodule under general anesthesia with an 8.0 ETT. The Monarch system was navigated to the apicoposterior segment of the LUL. Radial EBUS confirmed the lesion with an adjacent view. Sampling included transbronchial needle aspiration with a 21G needle (6 passes), forceps biopsy (6 specimens), and protected brushings. Continuous visualization was maintained. ROSE result showed no evidence of malignancy. The patient tolerated the procedure without complications.",
            7: "[Indication]\nPeripheral pulmonary nodule, LUL (14mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch robotic navigation to LB1+2. rEBUS: Adjacent. Sampling performed: 21G TBNA, Forceps biopsy, Protected Brush. Continuous visualization confirmed tool exit. ROSE: No evidence of malignant neoplasm.\n[Plan]\nPost-procedure CXR. Discharge if stable.",
            8: "Mr. Wilson presented for biopsy of a 14mm nodule in the left upper lobe. We induced general anesthesia and secured the airway. Using the Monarch robotic system, we navigated to the apicoposterior segment. We confirmed the location with radial EBUS, which showed the lesion adjacent to the airway. We then proceeded to sample the area using a 21-gauge needle, followed by standard forceps biopsies and a brush. The on-site pathologist saw no evidence of malignancy in the preliminary review. The procedure was completed without any immediate complications.",
            9: "Operation: Robotic-assisted bronchoscopy.\nTarget: LUL nodule.\nAction: The device was steered to the LUL apicoposterior segment. rEBUS verified the target. The lesion was aspirated with a 21G needle, sampled with forceps, and brushed. Visual confirmation of tool deployment was maintained.\nResult: ROSE indicated no malignancy. No trauma noted.\nPlan: Recovery."
        },
        1: { # John Hernandez (RLL, 15mm, TBNA only, ROSE Atypical)
            1: "Indication: PET-avid RLL nodule (15mm).\nAnesthesia: GA, 8.0 ETT.\nTechnique: Monarch robotic nav to RLL (Anterior-Basal).\nVerification: rEBUS (Adjacent).\nSampling: 22G TBNA x6 passes.\nResult: ROSE atypical/cannot exclude malignancy.\nComplications: None.",
            2: "PROCEDURE: Robotic bronchoscopy with transbronchial needle aspiration. The patient, a male with a PET-avid 15mm nodule in the Right Lower Lobe, was placed under general anesthesia. We utilized the Monarch platform for navigation to the RB8 segment. Electromagnetic registration error was 2.2mm. Radial EBUS confirmed the target location (adjacent view). We performed 22G needle aspiration under direct visualization. Preliminary pathology (ROSE) revealed atypical cells, malignancy not excluded. The patient remained stable throughout.",
            3: "Code Selection:\n- 31629 (TBNA): Primary intervention, 6 passes with 22G needle.\n- 31627 (Nav): Electromagnetic guidance used to reach RLL target.\n- 31654 (rEBUS): Used to confirm peripheral lesion.\nNote: No forceps or brush used (supports only 31629 for sampling).\nSite: RLL Anterior-Basal Segment.\nOutcome: ROSE atypical.",
            4: "Procedure: RLL Nodule Biopsy\nAttending: Dr. Martinez\nFellow: Dr. Torres\nSteps:\n1. ETT placed.\n2. Monarch nav to RLL (RB8).\n3. rEBUS: Adjacent.\n4. TBNA: 22G needle, 6 passes.\n5. ROSE: Atypical cells.\n6. No bleeding.\nPlan: Monitor, discharge.",
            5: "Hernandez John 15mm nodule in the RLL we used the robot today. Good registration 2.2mm. Navigated down to the anterior basal segment RB8. rEBUS showed it adjacent. Just did the needle today 22 gauge 6 passes. Cytology came back atypical cant rule out cancer. Patient did fine no bleeding extubated sent to PACU.",
            6: "Robotic bronchoscopy was performed for a 15mm RLL nodule. Under general anesthesia, the Monarch endoscope was navigated to the anterior-basal segment. Registration error was 2.2mm. Radial EBUS showed an adjacent view. Transbronchial needle aspiration was performed using a 22G needle for 6 passes under fluoroscopic and endoscopic guidance. ROSE results showed atypical cells. No complications occurred.",
            7: "[Indication]\nPET-avid lung nodule, RLL (15mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to RB8. rEBUS: Adjacent. TBNA performed with 22G needle (6 passes). Continuous visualization maintained. ROSE: Atypical cells, cannot exclude malignancy.\n[Plan]\nRecovery, CXR, discharge.",
            8: "We brought Mr. Hernandez back to the operating room to biopsy a 15mm nodule in his right lower lobe. Once he was asleep, we inserted the Monarch robotic scope and navigated to the target in the anterior-basal segment. The radial EBUS confirmed we were right next to the lesion. We decided to use a 22-gauge needle for aspiration and completed six passes. The preliminary results were atypical, so we couldn't rule out cancer yet. He handled the procedure well.",
            9: "Procedure: Robotic navigational bronchoscopy.\nSite: RLL Anterior-Basal.\nAction: The scope was guided to the target. rEBUS corroborated the location. The lesion was aspirated using a 22G needle. Six samples were collected.\nResult: ROSE suggested atypical cells. No adverse events.\nDisposition: Outpatient discharge."
        },
        2: { # Steven Rodriguez (RUL, 34mm, TBNA/Bx/Brush/BAL/Fiducial, ROSE Suspicious)
            1: "Target: 34mm RUL mass.\nActions:\n- Monarch nav to RB2.\n- rEBUS: Concentric.\n- TBNA (21G), Forceps x8, Brush.\n- BAL (RB2).\n- Fiducial placed.\nROSE: Suspicious for NSCC.\nPlan: SBRT planning/Onc referral.",
            2: "OPERATIVE REPORT: Mr. Rodriguez presented with a suspicious 34mm RUL mass. Following induction of general anesthesia, the Monarch robotic system was introduced. Navigation to the Posterior Segment of the RUL was successful (Registration error 4.0mm). Radial EBUS demonstrated a concentric view. We performed extensive sampling including TBNA (21G), forceps biopsy, and protected brushing. A bronchoalveolar lavage was performed at the target segment. Finally, a gold fiducial marker was deployed for future radiation planning. ROSE was suspicious for non-small cell carcinoma.",
            3: "Billing Summary:\n- 31629 (TBNA)\n- 31628 (Forceps Bx)\n- 31623 (Brush)\n- 31624 (BAL)\n- 31626 (Fiducial)\n- 31627 (Nav)\n- 31654 (EBUS)\nJustification: Multimodal sampling of 34mm RUL lesion plus marker placement for SBRT. All distinct techniques used.",
            4: "Resident Note\nPt: Rodriguez.\nIndication: Lung mass RUL.\nSteps:\n1. GA, ETT.\n2. Nav to RUL Posterior.\n3. rEBUS concentric.\n4. TBNA x5, Bx x8, Brush.\n5. BAL performed.\n6. Fiducial dropped.\nROSE: Suspicious for NSCC.\nComplications: None.",
            5: "Procedure note for Steven Rodriguez big nodule 34mm in the RUL. We used the monarch system navigated to RB2. EBUS was concentric so good hit. Did the works needle 21g forceps brush and a lavage. Also put in a gold marker for radiation. Pathology says suspicious for non small cell. No bleeding patient woke up fine.",
            6: "Robotic bronchoscopy targeting a 34mm RUL mass was performed under GA. Navigation to the posterior segment (RB2) was achieved. rEBUS showed a concentric view. Samples were obtained via 21G TBNA, forceps biopsy, and brush. Bronchoalveolar lavage was performed. A gold fiducial marker was placed under fluoroscopic guidance. ROSE reported suspicion of non-small cell carcinoma. The patient tolerated the procedure well.",
            7: "[Indication]\nSuspected malignancy, RUL mass (34mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to RB2. rEBUS: Concentric. Sampling: 21G TBNA, Forceps, Brush. BAL performed. Gold fiducial placed. ROSE: Suspicious for NSCC.\n[Plan]\nCXR, Discharge, Oncology follow-up.",
            8: "Mr. Rodriguez was scheduled for biopsy of a large 34mm mass in the right upper lobe. Under general anesthesia, we used the Monarch robot to find the lesion in the posterior segment. The EBUS view was concentric, confirming we were inside the lesion. We took multiple samples with a needle, forceps, and brush, and also washed the area (BAL). Since radiation might be needed, we placed a fiducial marker. The preliminary path read was suspicious for non-small cell cancer.",
            9: "Procedure: Robotic bronchoscopy with multimodal sampling and marker implantation.\nSite: RUL Posterior Segment.\nAction: The robotic scope was navigated to the lesion. rEBUS confirmed concentricity. The mass was aspirated, biopsied, and brushed. Lavage was conducted. A fiducial marker was implanted.\nResult: ROSE indicated suspicion of carcinoma. No complications."
        },
        3: { # Robert Rivera (RUL, 17mm, TBNA/Brush/BAL/Fiducial, ROSE Atypical)
            1: "Indication: Lung-RADS 4B nodule RUL (17mm).\nProcedure:\n- Nav to RB1 (Monarch).\n- rEBUS: Concentric.\n- TBNA (21G), Brush, BAL.\n- Fiducial placement.\n- No forceps used.\nROSE: Atypical/Suspicious.",
            2: "PROCEDURE NOTE: The patient underwent robotic-assisted bronchoscopy for a 17mm nodule in the Apical Segment of the RUL. Navigation was achieved with high accuracy (2.1mm error). Radial EBUS confirmed a concentric lesion. We performed transbronchial needle aspiration (21G) and protected brushings. Bronchoalveolar lavage was collected from RB1. A fiducial marker was deployed for potential SBRT. Preliminary cytology showed atypical cells, suspicious for malignancy.",
            3: "CPT Justification:\n- 31629 (TBNA)\n- 31623 (Brush)\n- 31624 (BAL)\n- 31626 (Fiducial)\n- 31627 (Nav) & 31654 (EBUS)\nNote: 31628 (Forceps) NOT billed as no forceps biopsy performed.\nSite: RUL Apical.",
            4: "Trainee Note\nPt: Rivera, R.\nTarget: RUL nodule.\nSteps:\n1. Intubation.\n2. Monarch nav to RB1.\n3. rEBUS concentric.\n4. 21G TBNA x7.\n5. Brush cytology.\n6. BAL.\n7. Fiducial placed.\nROSE: Atypical/Suspicious.\nPlan: D/C after CXR.",
            5: "Robert Rivera here for the RUL nodule 17mm. Used the monarch robot registered well. Went to the apical segment RB1. rEBUS was concentric. Did needle 21 gauge and brush no forceps this time. Did a lavage too. Put in a gold marker. ROSE said atypical suspicious. No bleeding.",
            6: "Robotic bronchoscopy was performed for a 17mm RUL nodule. The scope was navigated to the apical segment. rEBUS showed a concentric view. Sampling included 21G TBNA and protected brushings; no forceps biopsies were taken. BAL was performed at RB1. A gold fiducial marker was placed. ROSE results were suspicious for malignancy. The patient recovered without incident.",
            7: "[Indication]\nLung-RADS 4B nodule, RUL (17mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to RB1. rEBUS: Concentric. Sampling: 21G TBNA, Brush. BAL performed. Fiducial placed. ROSE: Suspicious for malignancy.\n[Plan]\nPost-proc CXR, Discharge.",
            8: "We performed a biopsy on Mr. Rivera's 17mm right upper lobe nodule today. Using the robotic system, we navigated to the apical segment and confirmed the lesion with concentric EBUS. We decided to sample using the needle and the brush, and we also washed the airway. We placed a fiducial marker to help with future treatment planning. The on-site path evaluation showed atypical cells that look suspicious for cancer.",
            9: "Procedure: Robotic navigational bronchoscopy with fiducial deployment.\nTarget: RUL Apical Segment.\nAction: Navigation to RB1 was successful. rEBUS confirmed the target. The lesion was aspirated and brushed. A lavage was performed. A fiducial marker was deposited.\nResult: ROSE suggested malignancy. No forceps biopsy performed."
        },
        4: { # Emily White (RML, 33mm, TBNA/Bx/Brush/Fiducial, ROSE Neg)
            1: "Pre-op: 33mm RML nodule.\nAnesthesia: GA.\nProcedure: Monarch nav to RB5. rEBUS Concentric. TBNA (21G), Forceps x7, Brush. Fiducial placed.\nROSE: Negative for malignancy.\nDisposition: Recovery.",
            2: "OPERATIVE NARRATIVE: Ms. White presented with a PET-avid 33mm nodule in the Medial Segment of the RML. Under general anesthesia, we utilized the Monarch robotic endoscope. Navigation was registered (4.0mm error). We confirmed the lesion location with concentric radial EBUS. Transbronchial needle aspiration (21G), forceps biopsies, and brushings were obtained. A fiducial marker was placed for radiation planning. ROSE was negative for malignant neoplasm.",
            3: "Codes:\n- 31629 (TBNA)\n- 31628 (Forceps)\n- 31623 (Brush)\n- 31626 (Fiducial)\n- +31627 (Nav) / +31654 (EBUS)\nSite: RML Medial Segment.\nTechnique: Robotic nav, rEBUS confirmation, Multimodal sampling.",
            4: "Resident Note\nPt: White, E.\nLoc: RML.\nSteps:\n1. GA induced.\n2. Monarch nav to RB5.\n3. rEBUS concentric.\n4. 21G TBNA x8.\n5. Forceps x7.\n6. Brush.\n7. Fiducial placed.\nROSE: Negative.\nPlan: Follow up 5-7 days.",
            5: "Emily White RML nodule 33mm. We used the monarch robot today. Navigated to the medial segment RB5. Concentric view on rEBUS. Did the needle biopsy 21g then forceps then brush. Dropped a fiducial marker in there too. Cytology says no cancer seen so far. No bleeding patient fine.",
            6: "Robotic bronchoscopy was undertaken for a 33mm RML nodule. Navigation to the medial segment (RB5) was performed with the Monarch system. rEBUS showed a concentric view. The lesion was sampled via 21G TBNA, forceps biopsy, and brushings. A fiducial marker was placed. ROSE results showed no evidence of malignancy. No complications were noted.",
            7: "[Indication]\nPET-avid nodule, RML (33mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to RB5. rEBUS: Concentric. Sampling: 21G TBNA, Forceps, Brush. Fiducial placed. ROSE: No malignancy.\n[Plan]\nCXR, Discharge.",
            8: "Ms. White came in for a biopsy of her right middle lobe nodule. We used the robotic scope to get to the medial segment. The EBUS confirmed we were right in the center of the lesion. We took plenty of samples using a needle, forceps, and a brush. We also placed a marker for radiation therapy just in case. The preliminary results didn't show any cancer, which is good news, but we'll wait for the final report.",
            9: "Procedure: Robotic-assisted bronchoscopic biopsy and marker placement.\nSite: RML Medial Segment.\nAction: The robotic device was steered to RB5. rEBUS confirmed the lesion. Samples were collected via aspiration, forceps excision, and brushing. A fiducial was implanted.\nResult: ROSE was negative for malignancy."
        },
        5: { # Stephanie White (RLL, 16mm, TBNA/Bx, ROSE Adeno)
            1: "Indication: 16mm RLL GGO.\nProcedure:\n- Monarch nav to RB9.\n- rEBUS: Concentric.\n- TBNA (21G) x7.\n- Forceps x8.\n- No brush/BAL.\nROSE: Adenocarcinoma.\nPlan: Onc referral.",
            2: "PROCEDURE NOTE: The patient underwent robotic bronchoscopy for a 16mm ground glass opacity in the Lateral-Basal Segment of the RLL. Navigation was achieved using the Monarch platform. Radial EBUS confirmed the target with a concentric view. We performed transbronchial needle aspiration (21G) and extensive forceps biopsies. No brushings were obtained. ROSE confirmed the presence of malignant cells consistent with adenocarcinoma.",
            3: "Coding:\n- 31629 (TBNA)\n- 31628 (Forceps)\n- 31627 (Nav)\n- 31654 (EBUS)\nSite: RLL Lateral-Basal.\nNote: No brush (31623) or BAL (31624) performed.\nOutcome: Positive for Adenocarcinoma.",
            4: "Trainee Note\nPt: White, S.\nLesion: RLL 16mm.\nSteps:\n1. GA, ETT 8.0.\n2. Nav to RB9 (Monarch).\n3. rEBUS concentric.\n4. TBNA 21G.\n5. Forceps biopsy.\nROSE: Adenocarcinoma.\nComplications: None.",
            5: "Stephanie White 16mm nodule in the RLL lateral basal. Used the monarch robot registration 3.6mm. Navigated down to RB9 rEBUS concentric. Did needle 21 gauge and forceps biopsies 8 passes. ROSE came back adenocarcinoma. No bleeding patient tolerated well.",
            6: "Robotic bronchoscopy was performed for a 16mm RLL nodule. The Monarch system was navigated to the lateral-basal segment (RB9). rEBUS confirmed a concentric view. Sampling consisted of 21G TBNA and forceps biopsies. Continuous visualization was maintained. ROSE confirmed adenocarcinoma. The patient was extubated and recovered without complications.",
            7: "[Indication]\nGround glass opacity, RLL (16mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to RB9. rEBUS: Concentric. Sampling: 21G TBNA, Forceps. Continuous visualization. ROSE: Adenocarcinoma.\n[Plan]\nCXR, Discharge, Oncology.",
            8: "Ms. White underwent a biopsy for a nodule in her right lower lobe. We used the Monarch robot to navigate to the lateral-basal segment. Once the EBUS confirmed we were centered in the lesion, we used a 21-gauge needle and forceps to take samples. The pathologist in the room confirmed it was adenocarcinoma. We finished the procedure without any issues.",
            9: "Procedure: Robotic navigational bronchoscopy.\nSite: RLL Lateral-Basal Segment.\nAction: The robotic scope was guided to the target. rEBUS verified the position. The lesion was aspirated and biopsied with forceps.\nResult: ROSE identified adenocarcinoma. No adverse events."
        },
        6: { # Patricia Lopez (LUL, 20mm, TBNA/Bx/Brush, ROSE Benign)
            1: "Indication: 20mm LUL nodule.\nTechnique: Monarch nav to LB1+2.\nrEBUS: Concentric.\nTools: 19G TBNA, Forceps, Brush.\nROSE: Benign (macrophages).\nDisposition: Recovery.",
            2: "OPERATIVE REPORT: Ms. Lopez presented for evaluation of a 20mm LUL nodule. Under general anesthesia, the Monarch robotic system was navigated to the Apicoposterior Segment. Registration error was 4.5mm. Radial EBUS confirmed a concentric view of the lesion. We performed sampling with a 19G aspiration needle, standard forceps, and a cytology brush. ROSE showed benign respiratory epithelium and macrophages. No immediate complications were noted.",
            3: "Codes: 31629 (TBNA), 31628 (Bx), 31623 (Brush), 31627 (Nav), 31654 (EBUS).\nTarget: LUL Apicoposterior (20mm).\nDetails: 19G needle used for TBNA. Forceps and brush also used. All under continuous guidance.",
            4: "Resident Note\nPt: Lopez.\nTarget: LUL 20mm.\nSteps:\n1. GA, ETT.\n2. Monarch to LB1+2.\n3. rEBUS concentric.\n4. 19G TBNA x7.\n5. Forceps x5.\n6. Brush.\nROSE: Benign.\nPlan: D/C.",
            5: "Patricia Lopez 20mm nodule LUL. Robotic case monarch. Went to the apicoposterior segment LB1+2. rEBUS was concentric. Used the big needle 19g then forceps and brush. ROSE said benign stuff only. No bleeding extubated fine.",
            6: "Robotic bronchoscopy was performed for a 20mm LUL nodule. The Monarch system was navigated to the apicoposterior segment. rEBUS showed a concentric view. Sampling included 19G TBNA, forceps biopsy, and brushings. ROSE results were benign. The patient tolerated the procedure well.",
            7: "[Indication]\nSuspected malignancy, LUL (20mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to LB1+2. rEBUS: Concentric. Sampling: 19G TBNA, Forceps, Brush. ROSE: Benign respiratory epithelium.\n[Plan]\nCXR, Discharge.",
            8: "We performed a biopsy on Ms. Lopez's left upper lobe nodule. Using the robotic scope, we navigated to the apicoposterior segment and confirmed the location with EBUS. We used a 19-gauge needle, forceps, and a brush to get good samples. The preliminary check showed only benign cells. She did well and was sent to recovery.",
            9: "Procedure: Robotic-assisted bronchoscopic sampling.\nSite: LUL Apicoposterior Segment.\nAction: The device was navigated to the lesion. rEBUS confirmed the target. Samples were obtained via 19G aspiration, forceps excision, and brushing.\nResult: ROSE indicated benign findings."
        },
        7: { # Angela Rivera (LLL, 20mm, TBNA/Bx/Brush/BAL, ROSE Suspicious)
            1: "Target: 20mm LLL nodule.\nNav: Monarch to LB10.\nrEBUS: Concentric.\nSampling: 22G TBNA, Forceps x8, Brush, BAL.\nROSE: Suspicious for NSCC.\nPlan: D/C.",
            2: "PROCEDURE NOTE: The patient underwent robotic bronchoscopy for a 20mm nodule in the Posterior-Basal Segment of the LLL. Navigation via Monarch was successful to LB10. Radial EBUS demonstrated a concentric view. We performed 22G TBNA, forceps biopsies, and protected brushings. A BAL was also performed. ROSE indicated cells suspicious for non-small cell carcinoma.",
            3: "Billing: 31629, 31628, 31623, 31624, 31627, 31654.\nSite: LLL Posterior-Basal.\nTools: 22G needle, Forceps, Brush, Lavage.\nGuidance: Robotic + Fluoroscopy + EBUS.",
            4: "Trainee Note\nPt: Rivera, A.\nLoc: LLL.\nSteps:\n1. GA.\n2. Nav to LB10 (Monarch).\n3. rEBUS concentric.\n4. 22G TBNA.\n5. Forceps.\n6. Brush.\n7. BAL.\nROSE: Suspicious.\nComplications: None.",
            5: "Angela Rivera LLL nodule 20mm. Used the monarch robot today. Navigated to LB10 posterior basal. Concentric on rEBUS. Did 22 gauge needle forceps brush and a wash. Cytology looks suspicious for non small cell. No bleeding.",
            6: "Robotic bronchoscopy targeting a 20mm LLL nodule was performed. The Monarch system was navigated to the posterior-basal segment (LB10). rEBUS confirmed a concentric view. Sampling included 22G TBNA, forceps biopsy, brushings, and BAL. ROSE was suspicious for NSCC. No complications occurred.",
            7: "[Indication]\nSuspected malignancy, LLL (20mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to LB10. rEBUS: Concentric. Sampling: 22G TBNA, Forceps, Brush, BAL. ROSE: Suspicious for NSCC.\n[Plan]\nCXR, Discharge.",
            8: "Ms. Rivera came in for a biopsy of a nodule in her left lower lobe. We used the robotic system to reach the posterior-basal segment. The EBUS showed we were right on target. We took samples with a needle, forceps, and brush, and also washed the area. The initial results look suspicious for cancer. She recovered well.",
            9: "Procedure: Robotic navigational bronchoscopy.\nSite: LLL Posterior-Basal Segment.\nAction: The scope was navigated to the target. rEBUS verified the location. The lesion was aspirated, biopsied, and brushed. Lavage was performed.\nResult: ROSE suggested carcinoma."
        },
        8: { # Angela Nelson (Lingula, 33mm, TBNA/Bx/Brush, ROSE Granulomatous)
            1: "Indication: 33mm Lingula nodule.\nProcedure:\n- Monarch nav to LB4.\n- rEBUS: Eccentric.\n- TBNA (22G), Forceps x7, Brush.\nROSE: Granulomatous inflammation.\nDisposition: Recovery.",
            2: "OPERATIVE NARRATIVE: Ms. Nelson presented with a 33mm nodule in the Superior Lingula. Under general anesthesia, the Monarch robotic system was deployed. Navigation to LB4 was achieved (4.8mm error). Radial EBUS showed an eccentric view. We performed 22G TBNA, forceps biopsies, and brushings. Preliminary pathology (ROSE) revealed granulomatous inflammation, consistent with a benign etiology.",
            3: "Codes: 31629, 31628, 31623, 31627, 31654.\nTarget: Lingula (Superior).\nFindings: Eccentric rEBUS view.\nSampling: 22G TBNA, Forceps, Brush.\nOutcome: Granuloma.",
            4: "Resident Note\nPt: Nelson.\nTarget: Lingula 33mm.\nSteps:\n1. GA.\n2. Nav to LB4.\n3. rEBUS eccentric.\n4. 22G TBNA x4.\n5. Forceps x7.\n6. Brush.\nROSE: Granuloma.\nPlan: D/C.",
            5: "Angela Nelson 33mm nodule in the Lingula. Robotic bronch today. Went to LB4 superior lingula. rEBUS was eccentric but we adjusted. Did needle 22g forceps brush. ROSE shows granulomas so probably not cancer. No bleeding.",
            6: "Robotic bronchoscopy was performed for a 33mm Lingula nodule. The Monarch system was navigated to the superior lingula (LB4). rEBUS showed an eccentric view. Sampling included 22G TBNA, forceps biopsy, and brushings. ROSE results indicated granulomatous inflammation. The patient tolerated the procedure well.",
            7: "[Indication]\nSolitary pulmonary nodule, Lingula (33mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to LB4. rEBUS: Eccentric. Sampling: 22G TBNA, Forceps, Brush. ROSE: Granulomatous inflammation.\n[Plan]\nCXR, Discharge.",
            8: "Ms. Nelson had a biopsy of her Lingula nodule today. We navigated the robot to the superior segment. The EBUS view was eccentric, meaning the probe was next to the lesion, but we got good samples using the needle, forceps, and brush. The pathologist saw granulomas, which is a good sign. There were no complications.",
            9: "Procedure: Robotic-assisted bronchoscopic biopsy.\nSite: Lingula Superior Segment.\nAction: The robotic scope was steered to the target. rEBUS confirmed the location. The lesion was aspirated, biopsied, and brushed.\nResult: ROSE indicated granulomatous inflammation."
        },
        9: { # Andrew Adams (LUL, 10mm, TBNA/Bx/Brush/BAL, ROSE Benign)
            1: "Indication: 10mm LUL GGO.\nProcedure:\n- Monarch nav to LB3.\n- rEBUS: Adjacent.\n- TBNA (19G), Forceps x7, Brush, BAL.\nROSE: Benign.\nPlan: D/C.",
            2: "PROCEDURE NOTE: Mr. Adams underwent robotic bronchoscopy for a 10mm ground glass opacity in the Anterior Segment of the LUL. Navigation was performed via the Monarch platform to LB3. Radial EBUS demonstrated an adjacent view. We utilized a 19G needle for TBNA, followed by forceps biopsies and protected brushings. A BAL was performed. ROSE showed benign respiratory epithelium and macrophages.",
            3: "Billing: 31629, 31628, 31623, 31624, 31627, 31654.\nSite: LUL Anterior (LB3).\nNote: 19G needle used.\nOutcome: Benign ROSE.",
            4: "Trainee Note\nPt: Adams.\nLoc: LUL 10mm.\nSteps:\n1. GA.\n2. Nav to LB3.\n3. rEBUS adjacent.\n4. 19G TBNA x5.\n5. Forceps x7.\n6. Brush.\n7. BAL.\nROSE: Benign.\nComplications: None.",
            5: "Andrew Adams 10mm nodule LUL anterior segment. Used the monarch robot registration 2.9mm. Went to LB3 rEBUS adjacent. Used the 19 gauge needle forceps brush and did a wash. ROSE says benign. Patient doing fine.",
            6: "Robotic bronchoscopy was performed for a 10mm LUL nodule. The Monarch system was navigated to the anterior segment (LB3). rEBUS showed an adjacent view. Sampling included 19G TBNA, forceps biopsy, brushings, and BAL. ROSE results were benign. The patient tolerated the procedure without complications.",
            7: "[Indication]\nGround glass opacity, LUL (10mm).\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nMonarch nav to LB3. rEBUS: Adjacent. Sampling: 19G TBNA, Forceps, Brush, BAL. ROSE: Benign.\n[Plan]\nCXR, Discharge.",
            8: "Mr. Adams came in for a biopsy of a small 10mm nodule in his left upper lobe. We used the robotic system to navigate to the anterior segment. EBUS confirmed we were adjacent to the lesion. We took samples with a 19-gauge needle, forceps, and brush, and also washed the area. The preliminary results were benign. He recovered well.",
            9: "Procedure: Robotic navigational bronchoscopy.\nSite: LUL Anterior Segment.\nAction: The scope was navigated to the target. rEBUS verified the position. The lesion was aspirated, biopsied, and brushed. Lavage was performed.\nResult: ROSE indicated benign findings."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock names and original ages for the patients found in the input JSON.
    Indices correspond to the order in the source file.
    """
    return [
        {"idx": 0, "orig_name": "Edward Wilson", "orig_age": 53, "names": ["Thomas Moore", "James Taylor", "Robert Anderson", "Michael Jackson", "William White", "David Harris", "Richard Martin", "Joseph Thompson", "Charles Garcia"]},
        {"idx": 1, "orig_name": "John Hernandez", "orig_age": 63, "names": ["Christopher Martinez", "Daniel Robinson", "Matthew Clark", "Anthony Rodriguez", "Donald Lewis", "Mark Lee", "Paul Walker", "Steven Hall", "Andrew Allen"]},
        {"idx": 2, "orig_name": "Steven Rodriguez", "orig_age": 53, "names": ["Kenneth Young", "George Hernandez", "Joshua King", "Kevin Wright", "Brian Lopez", "Edward Hill", "Ronald Scott", "Timothy Green", "Jason Adams"]},
        {"idx": 3, "orig_name": "Robert Rivera", "orig_age": 68, "names": ["Jeffrey Baker", "Ryan Gonzalez", "Jacob Nelson", "Gary Carter", "Nicholas Mitchell", "Eric Perez", "Jonathan Roberts", "Stephen Turner", "Larry Phillips"]},
        {"idx": 4, "orig_name": "Emily White", "orig_age": 68, "names": ["Patricia Campbell", "Jennifer Parker", "Linda Evans", "Elizabeth Edwards", "Barbara Collins", "Susan Stewart", "Jessica Sanchez", "Sarah Morris", "Karen Rogers"]},
        {"idx": 5, "orig_name": "Stephanie White", "orig_age": 77, "names": ["Nancy Reed", "Lisa Cook", "Margaret Morgan", "Betty Bell", "Sandra Murphy", "Ashley Bailey", "Kimberly Rivera", "Emily Cooper", "Donna Richardson"]},
        {"idx": 6, "orig_name": "Patricia Lopez", "orig_age": 50, "names": ["Michelle Cox", "Dorothy Howard", "Carol Ward", "Amanda Torres", "Melissa Peterson", "Deborah Gray", "Stephanie Ramirez", "Rebecca James", "Sharon Watson"]},
        {"idx": 7, "orig_name": "Angela Rivera", "orig_age": 60, "names": ["Laura Brooks", "Cynthia Kelly", "Kathleen Sanders", "Amy Price", "Shirley Bennett", "Angela Wood", "Helen Barnes", "Anna Ross", "Brenda Henderson"]},
        {"idx": 8, "orig_name": "Angela Nelson", "orig_age": 50, "names": ["Pamela Coleman", "Nicole Jenkins", "Samantha Perry", "Katherine Powell", "Christine Long", "Debra Patterson", "Rachel Hughes", "Carolyn Flores", "Janet Washington"]},
        {"idx": 9, "orig_name": "Andrew Adams", "orig_age": 53, "names": ["Scott Butler", "Frank Simmons", "Justin Foster", "Brandon Gonzales", "Raymond Bryant", "Gregory Alexander", "Samuel Russell", "Benjamin Griffin", "Patrick Diaz"]},
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
            
            # Update note_text with the variation from the dictionary
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing variation text for Note {idx}, Style {style_num}")
                continue
            
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
    output_filename = output_dir / "synthetic_monarch_notes_part_089.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()