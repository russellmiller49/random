import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_088.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations for Part 088.
    # Structure: Note_Index (0-8) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Mary Mitchell (RML RB5, Ion, TBNA/Cryo/Brush)
            1: "Procedure: Robotic Bronchoscopy (Ion).\nTarget: 35mm nodule, RML Medial Segment (RB5).\nActions:\n- Navigated to 1.4cm from target.\n- rEBUS: Adjacent view.\n- CBCT: Tool-in-lesion confirmed.\n- Sampling: TBNA (23G x5), Cryo (1.7mm x3, 5s), Brush (x2).\nROSE: Benign respiratory epithelium.\nComplications: None.\nPlan: Discharge.",
            2: "OPERATIVE NARRATIVE: The patient was anesthetized and the airway secured. We utilized the Intuitive Ion robotic platform to navigate the bronchial tree. The target lesion, a 35mm nodule within the Right Middle Lobe medial segment (RB5), was localized. Radial EBUS demonstrated an adjacent acoustic signature. Cone Beam CT (Cios Spin) with 3D reconstruction verified the catheter's position relative to the lesion. We proceeded with multimodal sampling: transbronchial needle aspiration using a 23-gauge needle, cryobiopsy utilizing a 1.7mm probe with a 5-second freeze time, and protected sheath brushing. ROSE assessment revealed benign respiratory epithelium and macrophages.",
            3: "Procedure: 31629 (TBNA), 31628 (Cryo), 31623 (Brush), +31627 (Nav), +31654 (EBUS).\nTechnique: Computer-assisted image-guided navigation (Ion) employed to reach RML (RB5). Radial EBUS probe used to identify peripheral lesion (adjacent view). Transbronchial needle aspiration performed (5 passes). Cryobiopsy performed (3 specimens). Brushing performed. Medical Necessity: 35mm Lung-RADS 4B nodule requiring tissue diagnosis.",
            4: "Procedure Note\nPatient: [PATIENT_NAME]\nAttending: Dr. Wilson\n\nSteps:\n1. Time out. GA induced.\n2. Ion catheter navigated to RML medial segment (RB5).\n3. rEBUS showed adjacent view.\n4. CBCT spin confirmed tool in lesion.\n5. Samples: 5 TBNA (23G), 3 Cryo (1.7mm), 2 Brush.\n6. ROSE: Benign.\n7. Tolerated well.\n\nPlan: CXR, follow up pathology.",
            5: "patient mary mitchell here for the lung nodule biopsy used the ion robot thing went to the RML medial segment rb5 nodule was big 35mm used the radial ebus saw it adjacent then did the spin ct to confirm. took a bunch of samples 5 needle passes 3 cryo and 2 brushes rose said benign stuff no bleeding really patient woke up fine send to recovery check xray for pneumo thanks.",
            6: "Robotic navigation bronchoscopy was performed with Ion platform on a 35mm nodule in the RML Medial Segment (RB5). Registration error was 1.9mm. Radial EBUS showed an adjacent view. Cone Beam CT confirmed tool-in-lesion. Sampling included Transbronchial needle aspiration (23G, 5 passes), Transbronchial cryobiopsy (1.7mm probe, 3 samples), and Transbronchial brushing (2 samples). ROSE showed benign respiratory epithelium and macrophages. No complications occurred.",
            7: "[Indication]\nLung-RADS 4B nodule, 35mm.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon robotic navigation to RML Medial Segment (RB5). rEBUS: Adjacent. Imaging: Cone Beam CT. \nBiopsy: \n- TBNA (23G x 5)\n- Cryo (1.7mm x 3)\n- Brush (x 2)\nROSE: Benign.\n[Plan]\nDischarge if stable. CXR.",
            8: "We brought the patient to the suite for evaluation of a 35mm RML nodule. Using the Ion robotic system, we successfully navigated to the medial segment (RB5). We confirmed our location first with radial EBUS, which showed an adjacent signal, and then with Cone Beam CT. Once positioned, we obtained samples using a 23G needle, a 1.7mm cryoprobe, and a cytology brush. The preliminary on-site evaluation showed benign cells. The patient remained stable throughout.",
            9: "Operation: Robotic-assisted bronchoscopy.\nTarget: RML Medial Segment (RB5) mass.\nMethod: The Ion catheter was steered to the target. Acoustic confirmation was achieved via radial EBUS (Adjacent). Positional verification was performed via CBCT. The lesion was sampled using needle aspiration (23G), cryo-extraction (1.7mm), and brushing. ROSE indicated benign tissue."
        },
        1: { # Dorothy White (LLL LB7+8, Ion, TBNA/Cryo/Brush/BAL)
            1: "Procedure: Ion Bronchoscopy LLL.\nTarget: 30mm nodule, LB7+8.\nTech: Shape-sensing nav, rEBUS (Concentric), CBCT.\nBiopsy:\n- TBNA: 21G x8.\n- Cryo: 1.7mm x6 (5s freeze).\n- Brush: x2.\n- BAL: 60cc instilled.\nROSE: Benign.\nPlan: Outpatient discharge.",
            2: "PROCEDURE SUMMARY: The patient underwent elective robotic bronchoscopy for a screening-detected nodule. The Anteromedial-Basal Segment of the LLL (LB7+8) was cannulated using the Ion platform. Radial EBUS demonstrated a concentric view, confirming the catheter position within the lesion. Intraoperative Cone Beam CT provided 3D confirmation. Extensive sampling was performed including transbronchial needle aspiration (21G), cryobiopsy (1.7mm probe), and bronchial brushing. Additionally, bronchoalveolar lavage was collected from the target segment. Immediate cytologic evaluation (ROSE) demonstrated benign respiratory epithelium.",
            3: "Codes: 31629 (TBNA), 31628 (Cryo), 31623 (Brush), 31624 (BAL), +31627 (Nav), +31654 (REBUS).\nSite: LLL (LB7+8).\nDetails: Robotic navigation used to access peripheral 30mm nodule. Position verified with concentric rEBUS view and CBCT. 8 needle passes, 6 cryo biopsies, 2 brushings, and lavage performed. Equipment: Ion robot, Cios Spin.",
            4: "Resident Note\nPt: [PATIENT_NAME]\nAttending: Dr. Garcia\nProcedure: Ion Nav Bronchoscopy\n\n1. ETT placed. Airway normal.\n2. Navigated to LLL anteromedial-basal (LB7+8).\n3. rEBUS: Concentric.\n4. Spin CT: Confirmed.\n5. Bx: TBNA (21G), Cryo (1.7mm), Brush, BAL.\n6. ROSE: Benign cells.\n7. No complications.",
            5: "Procedure note for dorothy white we did the ion robotic case today for the LLL nodule in the lb7+8 segment anesthesia was general. Navigated down there registration was ok 2.5mm error. radial ebus was concentric which is good. did the spin ct to be sure. took 8 needle passes 21 gauge then 6 cryo samples and brushed it too. also washed the area with saline for a BAL. rose just showed benign cells. patient did fine.",
            6: "Robotic navigation bronchoscopy (Ion) performed for 30mm LLL nodule (LB7+8). Registration error 2.5mm. Radial EBUS: Concentric. Cone Beam CT confirmed tool-in-lesion. Samples: 8 TBNA (21G), 6 Cryobiopsies (1.7mm), 2 Brushes, and BAL (60cc). ROSE result: Benign respiratory epithelium and macrophages. No complications.",
            7: "[Indication]\nLung cancer screening detected nodule, 30mm LLL.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to Anteromedial-Basal Segment (LB7+8). rEBUS: Concentric. CBCT performed. \n- TBNA (21G x 8)\n- Cryo (1.7mm x 6)\n- Brush (x 2)\n- BAL (LB7+8)\nROSE: Benign.\n[Plan]\nDischarge. Follow up 5-7 days.",
            8: "Ms. White presented for biopsy of a 30mm nodule in the left lower lobe. We utilized the Ion robotic system to navigate to the anteromedial-basal segment (LB7+8). A concentric view on radial EBUS confirmed we were centered in the lesion. We performed extensive sampling including needle aspiration, cryobiopsy, and brushing, followed by a bronchoalveolar lavage. The on-site pathologist saw only benign cells. The patient was extubated and recovered well.",
            9: "Procedure: Robotic-assisted bronchoscopy with multimodal sampling.\nArea: LLL Anteromedial-Basal (LB7+8).\nTechnique: Ion catheter navigation with rEBUS (Concentric) and CBCT verification. The lesion was sampled via needle aspiration (21G), cryoprobe (1.7mm), and brush. The segment was also lavaged (BAL). ROSE finding was benign."
        },
        2: { # Kevin Jackson (Lingula LB5, Ion, TBNA/Cryo/Brush)
            1: "Dx: Nodule Lingula (LB5).\nProc: Ion Nav Bronch + Bx.\nFindings: rEBUS Eccentric.\nAction: Locked catheter. TBNA (21G/23G x4). Cryo (1.7mm x6). Brush x2.\nROSE: Adenocarcinoma.\nComp: None.",
            2: "PROCEDURE NOTE: Mr. Jackson presented with an 11mm nodule in the Lingula (Inferior segment, LB5). Under general anesthesia, the Ion robotic catheter was navigated to the target with a registration error of 2.5mm. Radial EBUS revealed an eccentric view of the lesion. Following shape-sensing lock, transbronchial needle aspiration (21G/23G), cryobiopsy (1.7mm), and brushing were performed. Rapid On-Site Evaluation (ROSE) was positive for malignant cells consistent with adenocarcinoma.",
            3: "Service: Bronchoscopy with Navigation (+31627), REBUS (+31654), TBNA (31629), Cryo (31628), Brush (31623).\nLocation: Lingula (LB5).\nIndication: 11mm nodule, prior malignancy.\nDevice: Ion Robotic System.\nVerification: Eccentric rEBUS view.\nSamples: 4 TBNA, 6 Cryo, 2 Brush.\nPathology: Malignant (Adenocarcinoma).",
            4: "Procedure: Ion Bronchoscopy\nPatient: Kevin Jackson\nTarget: Lingula (LB5)\n\nSteps:\n1. Navigated to LB5.\n2. rEBUS: Eccentric.\n3. Locked catheter.\n4. TBNA x4, Cryo x6, Brush x2.\n5. ROSE: Adenocarcinoma.\n6. No bleeding.\n\nPlan: Oncology referral.",
            5: "kevin jackson here for biopsy of that lingula nodule in lb5. used the ion robot navigation went pretty smooth. radial ebus showed it eccentric but good margin. locked the arm and took samples. used both needles 21 and 23 then the cryo probe and a brush. pathologist in the room said it looks like adenocarcinoma. pulled out no bleeding. recovery then home.",
            6: "Robotic navigation bronchoscopy (Ion) for 11mm Lingula nodule (LB5). Registration error 2.5mm. Radial EBUS: Eccentric. Catheter locked. Sampling: TBNA (21G/23G, 4 passes), Cryobiopsy (1.7mm, 6 samples), Brush (2 samples). ROSE: Malignant cells, consistent with adenocarcinoma. No complications.",
            7: "[Indication]\n11mm nodule Lingula, prior malignancy.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to Inferior Lingula (LB5). rEBUS: Eccentric. \n- TBNA (21G/23G)\n- Cryo (1.7mm)\n- Brush\nROSE: Adenocarcinoma.\n[Plan]\nOutpatient discharge. Oncology.",
            8: "The patient, Mr. Jackson, underwent a robotic bronchoscopy to investigate an 11mm nodule in the inferior Lingula. We navigated the Ion catheter to LB5 and confirmed the lesion location with an eccentric radial EBUS signal. We obtained multiple samples using needles, a cryoprobe, and a brush. Unfortunately, the immediate pathology evaluation indicated adenocarcinoma. The procedure was otherwise uncomplicated.",
            9: "Operation: Robotic-assisted airway endoscopy.\nSite: Inferior Lingula (LB5).\nGuidance: Ion shape-sensing and radial EBUS (Eccentric).\nSampling: The lesion was aspirated (TBNA), frozen (Cryobiopsy), and brushed. ROSE confirmed adenocarcinoma. The airway was inspected and found clear."
        },
        3: { # Charles Baker (LLL LB10, Ion, TBNA/Cryo/Brush)
            1: "Target: 22mm nodule LLL (LB10).\nModality: Ion Robot + rEBUS (Eccentric) + CBCT.\nBx: TBNA (21G/23G x3), Cryo (1.1mm x3), Brush x2.\nROSE: Lymphocytes/Benign.\nOutcome: Stable.",
            2: "NARRATIVE: Mr. Baker underwent robotic bronchoscopy for a suspected malignancy in the left lower lobe posterior-basal segment (LB10). The Ion platform was utilized. Upon navigation to the target, radial EBUS showed an eccentric signature. Intraoperative Cone Beam CT (Cios Spin) was performed to verify tool-in-lesion. Biopsies were taken using 21G and 23G needles, a 1.1mm cryoprobe, and a cytology brush. Preliminary evaluation showed lymphocytes and benign cells.",
            3: "CPT Justification:\n- 31627: Robotic navigation (Ion).\n- 31654: Radial EBUS (Peripheral).\n- 31629: TBNA (3 passes).\n- 31628: Cryobiopsy (3 specimens).\n- 31623: Brushing.\nLocation: LLL Posterior-Basal (LB10).\nConfirmation: CBCT and rEBUS.",
            4: "Resident Note\nPt: Charles Baker\nStaff: Dr. Brown\n\n1. Ion nav to LLL LB10.\n2. rEBUS eccentric.\n3. CBCT spin: Tool in lesion.\n4. Bx: Needles (21/23G), Cryo (1.1mm), Brush.\n5. ROSE: Lymphocytes, benign.\n6. Extubated stable.",
            5: "charles baker procedure note. suspect lung ca. 22mm nodule in the LLL posterior basal lb10. used the ion system full registration. radial ebus was eccentric. did the cone beam spin to confirm. took 3 needle passes 3 cryo with the small probe 1.1mm and 2 brushes. rose said benign lymphocytes. patient did ok no pneumo.",
            6: "Robotic navigation bronchoscopy (Ion) targeting 22mm LLL nodule (LB10). Registration error 3.3mm. Radial EBUS: Eccentric. Cone Beam CT: Confirmed tool-in-lesion. Sampling: TBNA (21G/23G), Cryobiopsy (1.1mm), Brush. ROSE: Lymphocytes/Benign. Patient tolerated well.",
            7: "[Indication]\nSuspected malignancy, 22mm LLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to Posterior-Basal Segment (LB10). rEBUS: Eccentric. CBCT confirmed. \n- TBNA\n- Cryo (1.1mm)\n- Brush\nROSE: Benign/Lymphocytes.\n[Plan]\nFollow-up 5-7 days.",
            8: "We performed a robotic bronchoscopy on Mr. Baker to assess a 22mm nodule in the posterior-basal segment of the LLL. Using the Ion system, we navigated to the target and confirmed our position with both eccentric radial EBUS and Cone Beam CT. We collected samples using needles, a 1.1mm cryoprobe, and a brush. The immediate read was benign, showing lymphocytes. There were no complications.",
            9: "Procedure: Robotic navigation endoscopy.\nLesion: LLL Posterior-Basal (LB10).\nVerification: rEBUS (Eccentric) and CBCT.\nIntervention: The target was sampled via needle aspiration, cryo-adhesion (1.1mm), and brushing. ROSE indicated benign lymphocytes. No adverse events."
        },
        4: { # Kimberly Garcia (LUL LB1+2, Ion, TBNA/Brush - No Cryo)
            1: "Indication: GGO LUL (LB1+2).\nSystem: Ion Robot.\nChecks: rEBUS (Adjacent), CBCT.\nBx: TBNA (21G x6), Brush x2.\nROSE: Atypical cells.\nPlan: Wait for final path.",
            2: "OPERATIVE REPORT: Ms. Garcia presented with a 35mm ground glass opacity in the apicoposterior segment of the LUL (LB1+2). Robotic bronchoscopy (Ion) was performed. Navigation was confirmed via adjacent radial EBUS signal and Cone Beam CT reconstruction. The lesion was biopsied using a 21-gauge needle (6 passes) and a cytology brush. Cryobiopsy was not performed. ROSE assessment revealed atypical cells, malignancy not excluded.",
            3: "Code Selection:\n- 31629: TBNA (6 samples).\n- 31623: Brush (2 samples).\n- 31627: Navigation (Ion).\n- 31654: rEBUS.\nNote: No cryobiopsy performed. Location LUL (LB1+2). Indication GGO.",
            4: "Procedure: Ion Bronch LUL\nPatient: Kimberly Garcia\n\n1. Navigated to LB1+2 (Apicoposterior).\n2. rEBUS: Adjacent.\n3. CBCT: Confirmed.\n4. Samples: 6 TBNA (21G), 2 Brush.\n5. ROSE: Atypical.\n6. Tolerated well.",
            5: "kimberly garcia here for the LUL GGO biopsy. used the ion robot went to the apicoposterior segment lb1+2. radial ebus was adjacent. cone beam ct showed we were in the lesion. used the 21g needle for 6 passes and brushed it twice. didn't do cryo. rose said atypical cells suspicious. no bleeding patient fine.",
            6: "Robotic navigation bronchoscopy (Ion) for 35mm LUL GGO (LB1+2). Registration error 2.2mm. Radial EBUS: Adjacent. Cone Beam CT: Confirmed. Sampling: TBNA (21G, 6 passes) and Brush. ROSE: Atypical cells. No complications.",
            7: "[Indication]\nGround glass opacity LUL, 35mm.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to Apicoposterior Segment (LB1+2). rEBUS: Adjacent. CBCT: Tool-in-lesion. \n- TBNA (21G)\n- Brush\nROSE: Atypical.\n[Plan]\nMonitor for pneumothorax.",
            8: "Ms. Garcia underwent robotic bronchoscopy for a ground glass opacity in the LUL apicoposterior segment. We navigated the Ion catheter to the site and used radial EBUS (adjacent view) and Cone Beam CT to verify the location. We obtained samples using a 21G needle and a brush. The rapid on-site evaluation showed atypical cells. The patient was discharged after recovery.",
            9: "Procedure: Robotic-assisted airway exploration.\nSite: LUL Apicoposterior (LB1+2).\nValidation: rEBUS (Adjacent) and CBCT.\nAction: The lesion was sampled via needle aspiration and brushing. ROSE suggested atypia. No cryobiopsy was undertaken."
        },
        5: { # Amy Campbell (Lingula LB5, Ion, TBNA/BAL - No Cryo/Brush)
            1: "Target: 17mm nodule Lingula (LB5).\nTech: Ion, rEBUS (Concentric), CBCT.\nAction: TBNA (21G/23G x3). BAL (80cc).\nROSE: Suspicious for malignancy.\nDisp: Outpatient.",
            2: "PROCEDURE: Mrs. Campbell was brought to the suite for biopsy of a 17mm Lingular nodule (LB5). The Ion robotic system was employed. Navigation was verified with a concentric radial EBUS view and Cone Beam CT. Transbronchial needle aspiration was performed with 21G and 23G needles. A bronchoalveolar lavage was also performed. ROSE was suspicious for malignancy.",
            3: "Billing Codes: 31629 (TBNA), 31624 (BAL), +31627 (Nav), +31654 (rEBUS).\nLocation: Lingula (LB5).\nTools: Ion, Cios Spin (CBCT).\nNote: No brush or cryo performed. Indication suspected malignancy.",
            4: "Resident Note\nPt: Amy Campbell\nStaff: Dr. Kim\n\n1. Ion nav to Lingula LB5.\n2. rEBUS: Concentric.\n3. CBCT: Confirmed.\n4. Bx: TBNA (21/23G), BAL.\n5. ROSE: Suspicious.\n6. Stable.",
            5: "amy campbell procedure note. 17mm nodule in the lingula lb5. used ion robot. radial ebus concentric. cone beam ct looked good. did 3 needle passes and a bal. pathologist says suspicious for cancer. no bleeding.",
            6: "Robotic navigation bronchoscopy (Ion) for 17mm Lingula nodule (LB5). Registration error 2.0mm. Radial EBUS: Concentric. Cone Beam CT: Confirmed. Sampling: TBNA (21G/23G, 3 passes) and BAL. ROSE: Suspicious for malignancy. No complications.",
            7: "[Indication]\nSuspected malignancy, 17mm Lingula.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to Inferior Lingula (LB5). rEBUS: Concentric. CBCT: Confirmed. \n- TBNA\n- BAL\nROSE: Suspicious.\n[Plan]\nOutpatient discharge.",
            8: "Mrs. Campbell underwent a robotic bronchoscopy for a 17mm nodule in the inferior Lingula. We navigated to LB5 using the Ion system, confirming position with concentric radial EBUS and Cone Beam CT. We performed needle aspiration and a lavage. The on-site pathologist reported cells suspicious for malignancy.",
            9: "Operation: Robotic-assisted bronchoscopy.\nFocus: Inferior Lingula (LB5).\nChecks: rEBUS (Concentric) and CBCT.\nIntervention: The lesion was sampled via needle aspiration and lavage. ROSE indicated suspicion of malignancy."
        },
        6: { # Sarah Martin (Lingula LB5, Ion, TBNA + Fiducial - No Cryo/Brush/BAL)
            1: "Indication: 18mm GGO Lingula.\nProc: Ion Nav, rEBUS (Adjacent).\nAction: TBNA (23G x4). Fiducial placement (0.8x3mm gold).\nROSE: Adenocarcinoma.\nPlan: SBRT planning.",
            2: "NARRATIVE: Ms. Martin presented for biopsy and fiducial placement regarding an 18mm ground glass opacity in the Lingula (LB5). Using the Ion platform, we navigated to the target. Radial EBUS showed an adjacent view. Transbronchial needle aspiration confirmed adenocarcinoma on ROSE. Subsequently, a gold fiducial marker (CIVCO) was deployed under fluoroscopic guidance to facilitate future stereotactic radiotherapy.",
            3: "Coding: 31626 (Fiducials), 31629 (TBNA), +31627 (Nav), +31654 (rEBUS).\nTarget: Lingula (LB5).\nJustification: Biopsy confirmed malignancy (Adeno), fiducial placed for SBRT.\nTools: Ion, Fluoroscopy.",
            4: "Procedure: Ion Bronch + Fiducial\nPt: Sarah Martin\n\n1. Nav to Lingula LB5.\n2. rEBUS: Adjacent.\n3. TBNA x4 (23G).\n4. ROSE: Adenocarcinoma.\n5. Placed 1 gold fiducial.\n6. No complications.",
            5: "sarah martin here for biopsy and fiducial. 18mm ggo in the lingula lb5. ion robot used. radial ebus adjacent. took 4 needle samples. rose said adenocarcinoma. put in a gold fiducial marker for radiation. everything went fine.",
            6: "Robotic navigation bronchoscopy (Ion) for 18mm Lingula GGO (LB5). Registration error 3.1mm. Radial EBUS: Adjacent. Sampling: TBNA (23G, 4 passes). ROSE: Adenocarcinoma. Fiducial marker placed under fluoroscopy. No complications.",
            7: "[Indication]\nGGO Lingula, 18mm.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to Inferior Lingula (LB5). rEBUS: Adjacent. \n- TBNA (23G)\n- Fiducial placement\nROSE: Adenocarcinoma.\n[Plan]\nRadiation Oncology referral.",
            8: "Ms. Martin underwent robotic bronchoscopy for an 18mm nodule in the Lingula. After navigating with the Ion system and confirming location with adjacent radial EBUS, we performed needle aspiration which confirmed adenocarcinoma. We then placed a gold fiducial marker to aid in future radiation treatment.",
            9: "Procedure: Robotic-assisted endoscopy with marker implantation.\nSite: Inferior Lingula (LB5).\nSampling: Needle aspiration (TBNA) confirmed adenocarcinoma.\nIntervention: A fiducial marker was deployed for radiotherapy guidance."
        },
        7: { # Matthew Young (LUL LB1+2, Ion, TBNA/Cryo + Fiducial + BAL - No Brush)
            1: "Target: 27mm nodule LUL (LB1+2).\nProc: Ion Nav, rEBUS (Concentric), CBCT.\nActions: TBNA (x7), Cryo (x6), Fiducial, BAL.\nROSE: Squamous cell CA.\nComp: None.",
            2: "OPERATIVE REPORT: Mr. Young underwent robotic bronchoscopy for a 27mm LUL nodule. The Ion catheter was navigated to the apicoposterior segment (LB1+2). Concentric radial EBUS and Cone Beam CT confirmed the target. We performed transbronchial needle aspiration and cryobiopsy. A gold fiducial marker was placed for potential SBRT. Bronchoalveolar lavage was also collected. ROSE confirmed squamous cell carcinoma.",
            3: "Codes: 31626 (Fiducial), 31629 (TBNA), 31628 (Cryo), 31624 (BAL), +31627 (Nav), +31654 (rEBUS).\nLocation: LUL (LB1+2).\nDetails: 27mm lesion. Multi-modal sampling plus fiducial placement. CBCT used.",
            4: "Resident Note\nPt: Matthew Young\nAttending: Dr. Anderson\n\n1. Nav to LUL LB1+2.\n2. rEBUS concentric.\n3. CBCT confirmed.\n4. TBNA, Cryo, BAL performed.\n5. Fiducial placed.\n6. ROSE: Squamous cell.\n7. Stable.",
            5: "matthew young procedure note. 27mm nodule lul apicoposterior. used ion robot. radial ebus concentric. spin ct good. extensive sampling 7 needles 6 cryos. put in a fiducial too. did a bal. rose said squamous cell carcinoma. no bleeding.",
            6: "Robotic navigation bronchoscopy (Ion) for 27mm LUL nodule (LB1+2). Registration error 2.0mm. Radial EBUS: Concentric. Cone Beam CT: Confirmed. Sampling: TBNA (7 passes), Cryobiopsy (6 samples), BAL. Fiducial marker placed. ROSE: Squamous cell carcinoma. No complications.",
            7: "[Indication]\nSuspected malignancy, 27mm LUL.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to LB1+2. rEBUS: Concentric. CBCT: Confirmed.\n- TBNA\n- Cryo\n- Fiducial placement\n- BAL\nROSE: Squamous cell.\n[Plan]\nOncology.",
            8: "Mr. Young had a 27mm nodule in the LUL. We used the Ion robot to reach the apicoposterior segment. Position was verified with concentric radial EBUS and Cone Beam CT. We took needle and cryobiopsy samples, placed a fiducial marker, and performed a lavage. The on-site pathologist identified squamous cell carcinoma.",
            9: "Operation: Robotic-assisted bronchoscopy.\nLesion: LUL Apicoposterior (LB1+2).\nValidation: rEBUS (Concentric) and CBCT.\nActions: The lesion was sampled via needle, cryoprobe, and lavage. A fiducial was implanted. ROSE confirmed squamous cell carcinoma."
        },
        8: { # Laura Carter (LLL LB10, Ion, TBNA/Cryo/Brush + BAL)
            1: "Indication: Lung-RADS 4X LLL (LB10).\nProc: Ion Nav, rEBUS (Eccentric), CBCT.\nActions: TBNA (x6), Cryo (x3), Brush (x2), BAL.\nROSE: Lymphocytes.\nOutcome: Stable.",
            2: "PROCEDURE: Ms. Carter presented with a 21mm nodule in the LLL posterior-basal segment (LB10). Using the Ion robotic platform, we navigated to the lesion. Radial EBUS showed an eccentric view; Cone Beam CT confirmed tool-in-lesion. We performed transbronchial needle aspiration, cryobiopsy, and brushing. A bronchoalveolar lavage was also performed. ROSE showed lymphocytes and benign cells.",
            3: "Billing: 31629 (TBNA), 31628 (Cryo), 31623 (Brush), 31624 (BAL), +31627 (Nav), +31654 (rEBUS).\nSite: LLL (LB10).\nTech: Ion, Cios Spin.\nPath: Benign/Lymphocytes.",
            4: "Procedure: Ion Bronch LLL\nPt: Laura Carter\n\n1. Nav to LB10.\n2. rEBUS eccentric.\n3. CBCT confirmed.\n4. Samples: TBNA, Cryo, Brush, BAL.\n5. ROSE: Lymphocytes.\n6. No complications.",
            5: "laura carter procedure note. lll nodule lb10. ion robot used. radial ebus eccentric. spin ct confirm. did needle cryo brush and bal. rose just showed lymphocytes. patient woke up fine.",
            6: "Robotic navigation bronchoscopy (Ion) for 21mm LLL nodule (LB10). Registration error 1.9mm. Radial EBUS: Eccentric. Cone Beam CT: Confirmed. Sampling: TBNA (6 passes), Cryobiopsy (3 samples), Brush, BAL. ROSE: Lymphocytes. No complications.",
            7: "[Indication]\nLung-RADS 4X nodule LLL.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to Posterior-Basal (LB10). rEBUS: Eccentric. CBCT: Confirmed.\n- TBNA\n- Cryo\n- Brush\n- BAL\nROSE: Lymphocytes.\n[Plan]\nFollow-up.",
            8: "Ms. Carter underwent robotic bronchoscopy for a 21mm nodule in the LLL posterior-basal segment. We used the Ion system, confirmed with eccentric radial EBUS and Cone Beam CT. We performed comprehensive sampling including needle, cryo, brush, and lavage. The ROSE result was benign, showing lymphocytes.",
            9: "Procedure: Robotic-assisted airway endoscopy.\nTarget: LLL Posterior-Basal (LB10).\nVerification: rEBUS (Eccentric) and CBCT.\nIntervention: Multimodal sampling (TBNA, Cryo, Brush, BAL). ROSE indicated benign lymphocytes."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency
    return [
        {"idx": 0, "orig_name": "Mitchell, Mary", "orig_age": 67, "names": ["Alice Johnson", "Mary Mitchell", "Susan Davis", "Karen Wilson", "Patricia Moore", "Linda Taylor", "Barbara Anderson", "Elizabeth Thomas", "Jennifer Jackson"]},
        {"idx": 1, "orig_name": "White, Dorothy", "orig_age": 66, "names": ["Betty Harris", "Dorothy White", "Helen Martin", "Sandra Thompson", "Donna Garcia", "Carol Martinez", "Ruth Robinson", "Sharon Clark", "Michelle Rodriguez"]},
        {"idx": 2, "orig_name": "Jackson, Kevin", "orig_age": 51, "names": ["James Lewis", "Kevin Jackson", "Robert Lee", "Michael Walker", "William Hall", "David Allen", "Richard Young", "Charles Hernandez", "Joseph King"]},
        {"idx": 3, "orig_name": "Baker, Charles", "orig_age": 78, "names": ["Thomas Wright", "Charles Baker", "Christopher Lopez", "Daniel Hill", "Paul Scott", "Mark Green", "Donald Adams", "George Baker", "Kenneth Nelson"]},
        {"idx": 4, "orig_name": "Garcia, Kimberly", "orig_age": 70, "names": ["Nancy Carter", "Kimberly Garcia", "Lisa Mitchell", "Margaret Perez", "Ashley Roberts", "Sarah Turner", "Kimberly Phillips", "Jessica Campbell", "Emily Parker"]},
        {"idx": 5, "orig_name": "Campbell, Amy", "orig_age": 67, "names": ["Amy Campbell", "Melissa Evans", "Deborah Edwards", "Stephanie Collins", "Rebecca Stewart", "Laura Sanchez", "Cynthia Morris", "Kathleen Rogers", "Amy Reed"]},
        {"idx": 6, "orig_name": "Martin, Sarah", "orig_age": 52, "names": ["Sarah Martin", "Angela Cook", "Shirley Morgan", "Amy Bell", "Anna Murphy", "Brenda Bailey", "Pamela Rivera", "Nicole Cooper", "Katherine Richardson"]},
        {"idx": 7, "orig_name": "Young, Matthew", "orig_age": 73, "names": ["Matthew Young", "Steven Cox", "Edward Howard", "Brian Ward", "Ronald Torres", "Anthony Peterson", "Kevin Gray", "Jason Ramirez", "Jeffrey James"]},
        {"idx": 8, "orig_name": "Carter, Laura", "orig_age": 59, "names": ["Laura Carter", "Christine Watson", "Debra Brooks", "Rachel Kelly", "Carolyn Sanders", "Janet Price", "Maria Bennett", "Heather Wood", "Diane Barnes"]},
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
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen with full data)
                note_entry["note_text"] = f"Variation style {style_num} for note {idx} (Placeholder)"
            
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
    output_filename = output_dir / "synthetic_ion_robotic_notes_part_088.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()