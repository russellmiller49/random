import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_067_part1.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations for the Ion Robotic Bronchoscopy notes.
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Adams, Steven (LUL Ion: TBNA, Cryo, Fiducial, Brush, BAL)
            1: "Indication: 24mm LUL nodule.\nTechnique: Ion Robotic Bronchoscopy.\nFindings: LUL Apicoposterior segment. rEBUS eccentric.\nActions:\n- TBNA x7 (21G)\n- Cryobiopsy x3 (1.1mm, 6s)\n- Fiducial placed (0.8x3mm)\n- Brush x2\n- BAL (LB1+2)\nComplications: None.\nPlan: CXR, discharge.",
            2: "OPERATIVE REPORT\n\nPATIENT: Steven Adams\nPROCEDURE: Robotic-assisted bronchoscopy with multimodal sampling and fiducial marker placement.\n\nNARRATIVE: The patient was anesthetized and intubated. We utilized the Ion endoluminal system to navigate to the apicoposterior segment of the left upper lobe (LB1+2). A 24mm part-solid nodule was identified. Radial endobronchial ultrasound (rEBUS) demonstrated an eccentric orientation. Cone-beam CT (CBCT) provided tomographic confirmation of tool-in-lesion status. We proceeded with transbronchial needle aspiration (7 passes), followed by transbronchial cryobiopsy (3 specimens) and protected brushing. A gold fiducial marker was deployed for future stereotactic guidance. Bronchoalveolar lavage was performed to complete the evaluation. The patient tolerated the intervention well.",
            3: "Code Selection Justification:\n- 31627 (Navigational Bronchoscopy): Ion platform used for guidance to peripheral LUL target.\n- 31654 (REBUS): Radial probe used to confirm lesion location (eccentric view).\n- 31629 (TBNA): 7 samples obtained via 21G needle.\n- 31628 (Lung Biopsy): 3 cryobiopsy samples taken (distinct modality).\n- 31626 (Fiducial): Gold marker implanted.\n- 31623 (Brush): 2 samples.\n- 31624 (BAL): Lavage performed at LB1+2.\nConfirm medical necessity: Diagnosis of 24mm lung nodule.",
            4: "Procedure: Robotic Bronchoscopy (Ion)\nAttending: Dr. Williams\nResident: Dr. Chen\n\nSteps:\n1. Time out. GA induced.\n2. Airway inspected (normal).\n3. Ion catheter nav to LUL (LB1+2).\n4. Nodule localized (24mm); rEBUS eccentric.\n5. CBCT spin confirms position.\n6. Sampling: TBNA x7, Cryo x3, Brush x2.\n7. Fiducial placed.\n8. BAL performed.\n9. ROSE: Lymphocytes/benign.\n\nNo complications.",
            5: "Procedure note for mr adams we used the ion robot today for that lul nodule 24mm went down airway looks ok. Navigated to apicoposterior segment used the radar ebus thing showed eccentric view. Did a spin scan looks good. Put the needle in 7 times then the cryo probe 3 times froze for 6 seconds. Brushed it twice. Put a fiducial marker in there too just in case. Did a wash at the end. Rose said benign cells but we will see final path. Patient woke up fine no pneumo on fluoro.",
            6: "Robotic navigation bronchoscopy was performed with Ion platform for a 24mm nodule in the LUL (Apicoposterior Segment). General anesthesia was used. Registration error was 3.1mm. The catheter was advanced to the target. Radial EBUS showed an eccentric view. Cone Beam CT confirmed tool-in-lesion. Transbronchial needle aspiration (21G, 7 samples), transbronchial cryobiopsy (1.1mm probe, 3 samples), and brushing (2 samples) were performed. A fiducial marker was placed under fluoroscopic guidance. Bronchoalveolar lavage was performed at LB1+2. No complications were noted.",
            7: "[Indication]\nPart-solid 24mm nodule in LUL for tissue diagnosis.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon robotic navigation to LUL Apicoposterior segment. rEBUS: Eccentric. CBCT confirmation. Procedures: TBNA (x7), Cryobiopsy (x3), Brushing (x2), Fiducial placement, BAL. ROSE: Benign cells.\n[Plan]\nCXR to rule out pneumothorax. Discharge if stable.",
            8: "Mr. Adams presented for evaluation of a 24mm LUL nodule. Under general anesthesia, we navigated the Ion robotic catheter to the apicoposterior segment. Radial EBUS confirmed the lesion location with an eccentric view, and Cone Beam CT verified the tool position. We extensively sampled the lesion using a 21G needle for seven passes and a cryoprobe for three biopsies. We also performed brushing and placed a fiducial marker. Finally, a BAL was conducted. The procedure was uncomplicated.",
            9: "Operation: Robotic navigation bronchoscopy.\nTarget: 24mm mass in LUL.\nAction: The robotic catheter was steered to the target. Radial EBUS visualized the lesion. We sampled the tissue via needle aspiration (7x) and cryobiopsy (3x). A fiducial was implanted. Brushing and lavage were also executed. \nOutcome: Samples sent to pathology. No adverse events.",
        },
        1: { # Hill, Dorothy (LUL Ion: TBNA, Brush)
            1: "Target: 31mm LUL nodule.\nMethod: Ion Robot, Shape-sensing.\nConfirm: rEBUS (Concentric), CBCT.\nAction: TBNA x4 (21G/23G), Brush x2.\nROSE: Benign respiratory epithelium.\nComp: None. Stable.",
            2: "PROCEDURE NOTE: Robotic Bronchoscopy\n\nClinical History: 61-year-old female with multiple nodules, dominant 31mm LUL lesion.\nTechnique: Following registration of the Ion platform, the catheter was advanced to the apicoposterior segment of the LUL. Radial EBUS confirmed a concentric view of the lesion. 3D-volumetric imaging (CBCT) was utilized to refine position. We obtained diagnostic tissue via transbronchial needle aspiration (4 passes) and protected specimen brushing (2 passes).\nPathology: Rapid on-site evaluation showed benign cells.",
            3: "CPT Coding:\n31627: Navigation (Ion).\n31629: TBNA (Primary sampling, 4 passes).\n31654: EBUS (Peripheral guidance, Concentric).\n31623: Brushing.\nNote: Cryobiopsy not performed. Lesion size 31mm in LUL.",
            4: "Resident Note\nPt: Dorothy Hill\nProc: Ion Bronch LUL\n\n1. ETT placed.\n2. Navigated to LB1+2.\n3. Found 31mm nodule via rEBUS (Concentric).\n4. CBCT spin done.\n5. Biopsies: TBNA x4, Brush x2.\n6. ROSE: Benign.\n7. Pt extubated, stable.",
            5: "Dorothy hill had the bronch today for the 31mm spot in her left upper lung. We used the ion system registration error was 3.4mm. Found it with the ultrasound looked concentric which is good. Did the needle biopsy 4 times mixed 21 and 23 gauge. Also brushed it twice. Rose says just macrophages and respiratory cells so maybe benign. Patient did fine no bleeding.",
            6: "Robotic navigation bronchoscopy with Ion platform performed on 61-year-old female. Target: 31mm nodule in LUL (Apicoposterior). rEBUS view: Concentric. Cone Beam CT confirmed location. Transbronchial needle aspiration performed x4. Transbronchial brushing performed x2. ROSE result: Benign respiratory epithelium and macrophages. No complications.",
            7: "[Indication]\nDominant 31mm LUL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB1+2. rEBUS concentric. CBCT used. TBNA x4 and Brushing x2 performed. ROSE benign.\n[Plan]\nMonitor for pneumothorax. Follow up results.",
            8: "We performed a robotic bronchoscopy on Ms. Hill to evaluate her 31mm LUL nodule. Using the Ion system, we successfully navigated to the lesion, confirming its position with a concentric rEBUS view and CBCT. We took four needle aspirates and two brush samples. Preliminary pathology on-site showed only benign cells. The patient tolerated the procedure well.",
            9: "Procedure: Robotic assisted bronchoscopy.\nTarget: LUL nodule.\nExecuted: Navigated to site. Verified with rEBUS and CBCT. Aspirated tissue (TBNA) four times. Brushed the area twice.\nResult: Specimen collected. No immediate complications.",
        },
        2: { # Young, Linda (Lingula Ion: TBNA, Cryo)
            1: "Site: Lingula (11mm).\nNav: Ion Robot.\nVis: rEBUS (Eccentric), CBCT.\nSamples: TBNA x4 (21G), Cryo x4 (1.1mm).\nROSE: Negative for malignancy.\nPlan: Outpatient discharge.",
            2: "OPERATIVE SUMMARY: Ms. Young underwent elective robotic bronchoscopy for an 11mm nodule in the superior lingula. General anesthesia was induced. The Ion catheter was navigated to the target (LB4). Radial EBUS revealed an eccentric relationship to the airway. Positional accuracy was verified via Cone Beam CT. Diagnostic sampling included transbronchial needle aspiration (4 passes) and transbronchial cryobiopsy (4 specimens). Preliminary review (ROSE) did not identify malignant cells.",
            3: "Billing Data:\n- 31629 (TBNA): 4 samples.\n- 31628 (Cryobiopsy): 4 samples.\n- 31627 (Navigation).\n- 31654 (REBUS).\nTarget: 11mm nodule, Lingula. Note: No fluoro time recorded, CBCT used.",
            4: "Procedure: Ion Bronchoscopy\nPatient: Linda Young\nSteps:\n- Intubation.\n- Nav to Lingula (LB4).\n- rEBUS: Eccentric.\n- CBCT verification.\n- TBNA x4.\n- Cryo x4.\n- ROSE: No malignancy seen.\n- Extubated.",
            5: "Procedure note for linda young she has a small nodule 11mm in the lingula. Used the robot to get out there. Radar ebus showed it was eccentric. We did a spin to check position. Took 4 needle biopsies and then 4 cryo biopsies frozen for 5 seconds each. Rose didn't see cancer but we sent it all to path. No bleeding patient woke up ok.",
            6: "Robotic navigation bronchoscopy (Ion) for 11mm Lingula nodule. Registration error 2.1mm. rEBUS: Eccentric. CBCT confirmed tool-in-lesion. Sampling: TBNA x4 (21G), Cryobiopsy x4 (1.1mm probe). ROSE: No evidence of malignancy. No complications.",
            7: "[Indication]\n11mm Lingula nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LB4 via Ion. rEBUS eccentric. TBNA x4 and Cryobiopsy x4 performed under CBCT guidance.\n[Plan]\nDischarge. Final path pending.",
            8: "Ms. Young was brought to the bronchoscopy suite for biopsy of an 11mm Lingular nodule. We utilized the Ion robotic system for navigation. Upon reaching the target, rEBUS showed an eccentric view. We confirmed placement with CBCT and proceeded to take four needle aspirates and four cryobiopsies. The on-site pathologist did not see malignancy, but final results are pending.",
            9: "Operation: Robotic endoscopy.\nSite: Lingula.\nAction: Guided catheter to target. Validated with rEBUS/CBCT. Harvested tissue via needle (x4) and cryoprobe (x4).\nStatus: Patient stable.",
        },
        3: { # Jones, Jonathan (RUL Ion: TBNA, Cryo, Fiducial, Brush)
            1: "RUL 33mm GGO.\nIon Nav + rEBUS (Concentric).\nTBNA x6, Cryo x5, Brush x2.\nFiducial placed.\nROSE: Lymphocytes.\nNo complications.",
            2: "PROCEDURE: Robotic Bronchoscopy (RUL)\nPATIENT: Jonathan Jones\nINDICATION: 33mm Ground Glass Opacity.\nDETAILS: Under general anesthesia, the Ion robotic system was driven to the apical segment of the RUL (RB1). A concentric rEBUS view was obtained. Correct positioning was validated via Cone Beam CT. We obtained extensive sampling: 6 transbronchial needle aspirates and 5 cryobiopsies. A gold fiducial marker was implanted to facilitate future stereotactic radiation. Cytology brushing was also performed. The patient remained stable throughout.",
            3: "Codes:\n- 31626 (Fiducial)\n- 31629 (TBNA)\n- 31628 (Cryo)\n- 31623 (Brush)\n- 31627 (Nav)\n- 31654 (REBUS)\nLocation: RUL. Lesion: 33mm.",
            4: "Resident Note: Jonathan Jones\nProcedure: Ion RUL Biopsy\n\n1. ETT.\n2. Nav to RUL (RB1).\n3. rEBUS concentric.\n4. CBCT confirm.\n5. TBNA x6, Cryo x5, Brush x2.\n6. Fiducial placed.\n7. ROSE: Lymphocytes.\n8. Extubated.",
            5: "Mr Jones has a ggo in the right upper lobe 33mm. We used the ion robot. Went to the apical segment. Ultrasound looked concentric. Did a spin. Took a lot of samples 6 needles 5 cryos 2 brushes. Also put a fiducial in for radiation planning. Rose showed lymphocytes. No pneumothorax on the xray.",
            6: "Robotic navigation bronchoscopy (Ion) for 33mm RUL nodule. rEBUS: Concentric. CBCT confirmation. Procedures: TBNA x6 (23G), Cryobiopsy x5 (1.7mm), Brushing x2, Fiducial placement. ROSE: Lymphocytes/benign. No complications.",
            7: "[Indication]\n33mm RUL GGO.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to RB1. rEBUS concentric. Samples: TBNA x6, Cryo x5, Brush x2. Fiducial placed.\n[Plan]\nDischarge. Follow up.",
            8: "We performed a robotic bronchoscopy on Mr. Jones for his RUL ground glass opacity. Using the Ion system, we navigated to the apical segment and confirmed the lesion with a concentric rEBUS view and CBCT. We performed comprehensive sampling including needle aspiration, cryobiopsy, and brushing. A fiducial was placed for future treatment. The patient recovered without incident.",
            9: "Procedure: Robotic assisted biopsy.\nTarget: RUL mass.\nActions: Navigated to site. Confirmed with rEBUS. Sampled via needle, cryoprobe, and brush. Implanted fiducial marker.\nOutcome: Satisfactory samples.",
        },
        4: { # Mitchell, Daniel (RLL Ion: TBNA, Cryo, Brush)
            1: "RLL 33mm nodule.\nIon Nav -> RB8.\nrEBUS: Adjacent.\nTBNA x7, Cryo x5, Brush x2.\nROSE: Suspicious for malignancy.\nDischarged.",
            2: "OPERATIVE REPORT: Mr. Mitchell underwent robotic bronchoscopy for a 33mm RLL nodule suspicious for malignancy. The Ion catheter was navigated to the anterior-basal segment (RB8). rEBUS demonstrated an adjacent lesion. Following CBCT confirmation, we performed diagnostic sampling. Seven TBNA passes and five cryobiopsies were obtained, alongside bronchial brushing. Rapid on-site evaluation revealed atypical cells highly suspicious for malignancy.",
            3: "CPT Justification:\n- 31629 (TBNA - 7 passes)\n- 31628 (Cryo - 5 samples)\n- 31623 (Brush)\n- 31627 (Nav)\n- 31654 (REBUS)\nSite: RLL. Diagnosis: Lung cancer screening nodule.",
            4: "Procedure: Ion RLL\nPatient: Daniel Mitchell\n\n- Time out.\n- Nav to RB8.\n- rEBUS adjacent.\n- CBCT spin.\n- TBNA x7, Cryo x5, Brush x2.\n- ROSE: Suspicious.\n- Stable.",
            5: "Procedure note for Daniel Mitchell he has a 33mm nodule in the RLL. Used the ion robot. Navigated to the anterior basal segment. Ultrasound was adjacent not concentric. Did the spin. Took 7 needle biopsies and 5 cryo biopsies. Brushed it too. Rose guy said it looks like cancer. Patient is fine going home.",
            6: "Robotic navigation bronchoscopy (Ion) for 33mm RLL nodule. rEBUS: Adjacent. CBCT confirmed tool-in-lesion. Sampling: TBNA x7 (23G), Cryobiopsy x5 (1.7mm), Brushing x2. ROSE: Suspicious for malignancy. No complications.",
            7: "[Indication]\n33mm RLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to RB8. rEBUS adjacent. TBNA x7, Cryo x5, Brush x2. ROSE suspicious.\n[Plan]\nOncology referral pending final path.",
            8: "Mr. Mitchell underwent robotic biopsy of his RLL nodule today. We navigated to the anterior-basal segment using the Ion system. Although rEBUS showed an adjacent view, CBCT confirmed we were in the lesion. We obtained extensive samples via needle, cryoprobe, and brush. Preliminary pathology is suspicious for malignancy.",
            9: "Operation: Robotic lung biopsy.\nSite: RLL.\nMethod: Ion navigation. Validated with rEBUS (adjacent) and CBCT.\nHarvest: Needle aspiration (x7), Cryo (x5), Brush (x2).\nResult: Suspicious for carcinoma.",
        },
        5: { # Rodriguez, Rebecca (Lingula Ion: TBNA, Cryo, Fiducial, Brush, BAL)
            1: "Lingula 23mm nodule.\nIon Nav -> LB5.\nrEBUS: Concentric.\nTBNA x4, Cryo x5, Fiducial, Brush x2, BAL.\nROSE: Granulomatous.\nNo complications.",
            2: "PROCEDURE: Robotic Bronchoscopy (Lingula)\nPATIENT: Rebecca Rodriguez\nINDICATION: 23mm Lingular nodule.\nNARRATIVE: General anesthesia was utilized. The Ion system facilitated navigation to the inferior lingula (LB5). A concentric rEBUS signal was identified. CBCT confirmed tool-in-lesion. We performed TBNA (4 passes) and cryobiopsy (5 specimens). A fiducial marker was placed. Brushing and BAL were also performed. On-site pathology suggested granulomatous inflammation.",
            3: "Billing:\n- 31626 (Fiducial)\n- 31629 (TBNA)\n- 31628 (Cryo)\n- 31623 (Brush)\n- 31624 (BAL)\n- 31627 (Nav)\n- 31654 (REBUS)\nTarget: Lingula 23mm.",
            4: "Resident Note: Rebecca Rodriguez\nProc: Ion Lingula\n\n1. ETT.\n2. Nav to LB5.\n3. rEBUS concentric.\n4. CBCT.\n5. TBNA x4, Cryo x5, Fiducial, Brush x2, BAL.\n6. ROSE: Granulomas.\n7. Extubated.",
            5: "Mrs Rodriguez has a nodule in the lingula 23mm. We used the robot to get there. Ultrasound looked concentric. Confirmed with the spin. Took 4 needle biopsies 5 cryo biopsies put a fiducial in brushed it and did a wash. Rose thinks its granulomas not cancer. Patient woke up fine.",
            6: "Robotic navigation bronchoscopy (Ion) for 23mm Lingula nodule. rEBUS: Concentric. CBCT confirmation. Procedures: TBNA x4, Cryobiopsy x5, Fiducial placement, Brushing x2, BAL. ROSE: Granulomatous inflammation. No complications.",
            7: "[Indication]\n23mm Lingula nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LB5. rEBUS concentric. Samples: TBNA x4, Cryo x5, Brush x2, BAL. Fiducial placed.\n[Plan]\nFollow up.",
            8: "We performed a robotic bronchoscopy on Ms. Rodriguez to biopsy a 23mm nodule in the lingula. We navigated to the inferior segment and confirmed the lesion with a concentric rEBUS view. We took multiple samples using needle, cryoprobe, and brush, and also placed a fiducial. A BAL was performed. Preliminary pathology suggests granulomatous inflammation.",
            9: "Procedure: Robotic assisted sampling.\nTarget: Lingula mass.\nAction: Navigated to site. Verified with rEBUS. Sampled via needle, cryoprobe, and brush. Implanted fiducial. Lavaged airway.\nResult: Granulomatous changes noted.",
        },
        6: { # Taylor, Donald (LLL Ion: TBNA, Cryo, Fiducial, Brush, BAL)
            1: "LLL 9mm nodule.\nIon Nav -> LB9.\nrEBUS: Adjacent.\nTBNA x6, Cryo x5, Fiducial, Brush x2, BAL.\nROSE: SCC.\nStable.",
            2: "OPERATIVE NOTE: Mr. Taylor underwent robotic bronchoscopy for a solitary 9mm LLL nodule. Navigation to the lateral-basal segment (LB9) was achieved with the Ion system. rEBUS showed an adjacent view; CBCT confirmed adequate positioning. Diagnostic yield included 6 TBNA passes and 5 cryobiopsies. A fiducial was placed. Brushing and BAL were completed. ROSE confirmed squamous cell carcinoma.",
            3: "Codes: 31629, 31628, 31626, 31623, 31624, 31627, 31654.\nLocation: LLL. Lesion size: 9mm. \nTools: 21G Needle, 1.7mm Cryoprobe.",
            4: "Resident Note: Donald Taylor\nProc: Ion LLL\n\n- Intubation.\n- Nav to LB9.\n- rEBUS adjacent.\n- CBCT.\n- TBNA x6, Cryo x5, Fiducial, Brush x2, BAL.\n- ROSE: SCC.\n- Recovery.",
            5: "Mr Taylor has a small 9mm spot in the LLL. Used the ion robot. Went to the lateral basal segment. Ultrasound adjacent. Did the spin. Took 6 needle samples and 5 cryo samples. Put a fiducial in. Brushed and washed. Rose says squamous cell cancer. Patient ok.",
            6: "Robotic navigation bronchoscopy (Ion) for 9mm LLL nodule. rEBUS: Adjacent. CBCT confirmed position. Procedures: TBNA x6, Cryobiopsy x5, Fiducial placement, Brushing x2, BAL. ROSE: Squamous cell carcinoma. No complications.",
            7: "[Indication]\n9mm LLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LB9. rEBUS adjacent. Samples: TBNA x6, Cryo x5, Brush x2, BAL. Fiducial placed. ROSE: SCC.\n[Plan]\nOncology referral.",
            8: "Mr. Taylor presented for biopsy of a small 9mm LLL nodule. We used the Ion robotic system to navigate to the lateral-basal segment. Despite an adjacent rEBUS view, CBCT confirmed we were in the lesion. We obtained diagnostic tissue via needle and cryoprobe, placed a fiducial, and performed a BAL. Pathology confirmed squamous cell carcinoma.",
            9: "Operation: Robotic biopsy.\nSite: LLL.\nAction: Steered to target. Confirmed adjacent rEBUS. Extracted tissue via needle and cryoprobe. Implanted fiducial. Lavaged.\nOutcome: Malignancy confirmed.",
        },
        7: { # Sanchez, Karen (RLL Ion: TBNA, Cryo)
            1: "RLL 30mm nodule.\nIon Nav -> RB10.\nrEBUS: Adjacent.\nTBNA x5, Cryo x5.\nROSE: SCC.\nNo complications.",
            2: "PROCEDURE: Robotic Bronchoscopy (RLL)\nPATIENT: Karen Sanchez\nINDICATION: Lung-RADS 4B nodule (30mm).\nNARRATIVE: Under general anesthesia, the Ion catheter was navigated to the posterior-basal segment of the RLL (RB10). rEBUS showed an adjacent view. CBCT confirmed tool-in-lesion. We performed 5 passes of TBNA and 5 cryobiopsies. Rapid on-site evaluation was consistent with squamous cell carcinoma.",
            3: "Billing:\n- 31629 (TBNA)\n- 31628 (Cryo)\n- 31627 (Nav)\n- 31654 (REBUS)\nTarget: RLL 30mm nodule.",
            4: "Resident Note: Karen Sanchez\nProc: Ion RLL\n\n1. ETT.\n2. Nav to RB10.\n3. rEBUS adjacent.\n4. CBCT.\n5. TBNA x5, Cryo x5.\n6. ROSE: SCC.\n7. Extubated.",
            5: "Karen Sanchez has a 30mm nodule in the RLL. Used the ion robot. Went to the posterior basal segment. Ultrasound adjacent. Did the spin. Took 5 needle biopsies and 5 cryo biopsies. Rose says squamous cell. Patient woke up fine.",
            6: "Robotic navigation bronchoscopy (Ion) for 30mm RLL nodule. rEBUS: Adjacent. CBCT confirmed position. Procedures: TBNA x5, Cryobiopsy x5. ROSE: Squamous cell carcinoma. No complications.",
            7: "[Indication]\n30mm RLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to RB10. rEBUS adjacent. Samples: TBNA x5, Cryo x5. ROSE: SCC.\n[Plan]\nOncology referral.",
            8: "Ms. Sanchez underwent robotic biopsy of her 30mm RLL nodule. We navigated to the posterior-basal segment using the Ion system. rEBUS was adjacent, but CBCT confirmed tool-in-lesion. We obtained five needle aspirates and five cryobiopsies. On-site pathology confirmed squamous cell carcinoma.",
            9: "Procedure: Robotic assisted biopsy.\nTarget: RLL mass.\nAction: Navigated to site. Validated with rEBUS. Aspirated and cryo-biopsied tissue.\nResult: SCC confirmed.",
        },
        8: { # Garcia, Stephanie (RML Ion: TBNA, Cryo, BAL)
            1: "RML 25mm nodule.\nIon Nav -> RB5.\nrEBUS: Adjacent.\nTBNA x7, Cryo x3, BAL.\nROSE: Atypical.\nStable.",
            2: "OPERATIVE REPORT: Ms. Garcia underwent robotic bronchoscopy for a 25mm RML nodule. The Ion catheter was navigated to the medial segment (RB5). rEBUS revealed an adjacent lesion. CBCT verified positioning. Diagnostic sampling included 7 TBNA passes and 3 cryobiopsies. A BAL was also performed. ROSE showed atypical cells suspicious for malignancy.",
            3: "CPT: 31629, 31628, 31624, 31627, 31654.\nLocation: RML. Size: 25mm.\nTools: 21G needle, 1.1mm cryoprobe.",
            4: "Resident Note: Stephanie Garcia\nProc: Ion RML\n\n- Intubation.\n- Nav to RB5.\n- rEBUS adjacent.\n- CBCT.\n- TBNA x7, Cryo x3, BAL.\n- ROSE: Suspicious.\n- Recovery.",
            5: "Stephanie Garcia has a 25mm nodule in the RML. Used the ion robot. Went to the medial segment. Ultrasound adjacent. Did the spin. Took 7 needle biopsies and 3 cryo biopsies. Did a wash. Rose says atypical suspicious. Patient ok.",
            6: "Robotic navigation bronchoscopy (Ion) for 25mm RML nodule. rEBUS: Adjacent. CBCT confirmed position. Procedures: TBNA x7, Cryobiopsy x3, BAL. ROSE: Atypical cells. No complications.",
            7: "[Indication]\n25mm RML nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to RB5. rEBUS adjacent. Samples: TBNA x7, Cryo x3, BAL. ROSE: Suspicious.\n[Plan]\nFollow up.",
            8: "Ms. Garcia presented for biopsy of a 25mm RML nodule. We used the Ion robotic system to navigate to the medial segment. rEBUS showed an adjacent view, but CBCT confirmed tool-in-lesion. We performed extensive sampling with needle and cryoprobe, followed by a BAL. Pathology is suspicious for malignancy.",
            9: "Operation: Robotic lung sampling.\nSite: RML.\nAction: Steered to target. Confirmed adjacent rEBUS. Extracted tissue via needle and cryoprobe. Lavaged.\nOutcome: Suspicious for malignancy.",
        },
        9: { # Moore, Stephanie (RML Ion: TBNA, Cryo, BAL)
            1: "RML 25mm nodule.\nIon Nav -> RB5.\nrEBUS: Adjacent.\nTBNA x7, Cryo x4, BAL.\nROSE: Granulomas.\nNo complications.",
            2: "PROCEDURE: Robotic Bronchoscopy (RML)\nPATIENT: Stephanie Moore\nINDICATION: 25mm Solitary Pulmonary Nodule.\nNARRATIVE: General anesthesia was induced. The Ion catheter was navigated to the medial segment of the RML (RB5). rEBUS showed an adjacent view. Fluoroscopy and Shape-Sensing verified positioning. We obtained 7 TBNA samples and 4 cryobiopsies. A BAL was performed. ROSE indicated granulomatous inflammation.",
            3: "Codes: 31629, 31628, 31624, 31627, 31654.\nTarget: RML 25mm.\nNote: Fluoroscopy used for verification (no CBCT mentioned in original text, used Fluoro).",
            4: "Resident Note: Stephanie Moore\nProc: Ion RML\n\n1. ETT.\n2. Nav to RB5.\n3. rEBUS adjacent.\n4. Fluoro confirm.\n5. TBNA x7, Cryo x4, BAL.\n6. ROSE: Granulomas.\n7. Extubated.",
            5: "Stephanie Moore has a 25mm nodule in the RML. Used the ion robot. Went to the medial segment. Ultrasound adjacent. Checked with fluoro. Took 7 needle biopsies and 4 cryo biopsies. Did a wash. Rose says granulomas. Patient fine.",
            6: "Robotic navigation bronchoscopy (Ion) for 25mm RML nodule. rEBUS: Adjacent. Positioning confirmed. Procedures: TBNA x7, Cryobiopsy x4, BAL. ROSE: Granulomatous inflammation. No complications.",
            7: "[Indication]\n25mm RML nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to RB5. rEBUS adjacent. Samples: TBNA x7, Cryo x4, BAL. ROSE: Granulomas.\n[Plan]\nFollow up.",
            8: "Ms. Moore underwent robotic biopsy of her RML nodule. We navigated to the medial segment using the Ion system. rEBUS was adjacent. We confirmed position and obtained multiple samples via needle and cryoprobe, followed by a BAL. Preliminary pathology suggests granulomatous inflammation.",
            9: "Procedure: Robotic assisted biopsy.\nTarget: RML mass.\nAction: Navigated to site. Validated with rEBUS. Aspirated and cryo-biopsied tissue. Lavaged.\nResult: Granulomatous inflammation.",
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the input file.
    # Note: 10 entries corresponding to the 10 notes in the source file.
    return [
        {"idx": 0, "orig_name": "Adams, Steven", "orig_age": 65, "names": ["John Smith", "Robert Johnson", "Michael Williams", "David Brown", "Richard Jones", "Charles Garcia", "Joseph Miller", "Thomas Davis", "Christopher Rodriguez"]},
        {"idx": 1, "orig_name": "Hill, Dorothy", "orig_age": 61, "names": ["Mary Martinez", "Patricia Hernandez", "Jennifer Lopez", "Linda Gonzalez", "Elizabeth Wilson", "Barbara Anderson", "Susan Thomas", "Jessica Taylor", "Sarah Moore"]},
        {"idx": 2, "orig_name": "Young, Linda", "orig_age": 60, "names": ["Karen Jackson", "Nancy Martin", "Lisa Lee", "Betty Perez", "Margaret Thompson", "Sandra White", "Ashley Harris", "Kimberly Sanchez", "Emily Clark"]},
        {"idx": 3, "orig_name": "Jones, Jonathan", "orig_age": 53, "names": ["Daniel Ramirez", "Paul Lewis", "Mark Robinson", "Donald Walker", "George Young", "Kenneth Allen", "Steven King", "Edward Wright", "Brian Scott"]},
        {"idx": 4, "orig_name": "Mitchell, Daniel", "orig_age": 50, "names": ["Kevin Torres", "Ronald Nguyen", "Timothy Hill", "Jason Flores", "Jeffrey Green", "Ryan Adams", "Jacob Nelson", "Gary Baker", "Nicholas Hall"]},
        {"idx": 5, "orig_name": "Rodriguez, Rebecca", "orig_age": 81, "names": ["Sharon Rivera", "Cynthia Campbell", "Kathleen Mitchell", "Amy Carter", "Shirley Roberts", "Angela Gomez", "Helen Phillips", "Anna Evans", "Brenda Turner"]},
        {"idx": 6, "orig_name": "Taylor, Donald", "orig_age": 71, "names": ["Eric Diaz", "Stephen Parker", "Larry Cruz", "Scott Edwards", "Frank Collins", "Justin Reyes", "Brandon Stewart", "Raymond Morris", "Gregory Morales"]},
        {"idx": 7, "orig_name": "Sanchez, Karen", "orig_age": 51, "names": ["Pamela Murphy", "Nicole Cook", "Emma Rogers", "Samantha Morgan", "Katherine Peterson", "Christine Cooper", "Debra Reed", "Rachel Bailey", "Carolyn Bell"]},
        {"idx": 8, "orig_name": "Garcia, Stephanie", "orig_age": 66, "names": ["Janet Gomez", "Catherine Kelly", "Maria Howard", "Heather Ward", "Diane Cox", "Virginia Diaz", "Julie Richardson", "Joyce Wood", "Victoria Watson"]},
        {"idx": 9, "orig_name": "Moore, Stephanie", "orig_age": 53, "names": ["Kelly Brooks", "Christina Bennett", "Joan Gray", "Evelyn James", "Lauren Mendoza", "Judith Wallace", "Megan Black", "Cheryl Axelrod", "Martha Hughes"]}
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
            # Use style 1 if the specific style isn't defined in the limited mock set for safety
            # (Though in this script, all 10 notes have 9 styles defined)
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if a specific note/style combo is missing in the manual dictionary
                note_entry["note_text"] = f"[Variation {style_num} not manually defined for Note {idx}]"

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
    output_filename = output_dir / "synthetic_ion_robotic_notes.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()