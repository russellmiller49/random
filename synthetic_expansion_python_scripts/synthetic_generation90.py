import json
import random
import datetime
import copy
from pathlib import Path

# Source file configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_090.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the given year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations for the 10 source notes.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Wilson, David (RML Nodule, 21G TBNA, BAL)
            1: "Procedure: Monarch Robotic Bronchoscopy.\nTarget: 23mm RML nodule.\nAction: ETT placed. Registration error 3.7mm. Navigated to RB5. rEBUS adjacent. Telescoped scope.\nSampling: 21G TBNA x7 passes. Continuous visualization confirmed. BAL performed RB5.\nResult: ROSE suspicious for NSCC. No bleeding.\nPlan: Recovery, CXR.",
            2: "OPERATIVE NARRATIVE: The patient was anesthetized and intubated. The Monarch robotic endoscopic platform was utilized for navigation. Electromagnetic registration was achieved with a divergence of 3.7mm. The device was advanced to the Right Middle Lobe (RB5), where the catheter was locked. Radial EBUS confirmed the lesion was adjacent to the airway. Under continuous visual guidance, Transbronchial Needle Aspiration (TBNA) was executed using a 21G needle for seven passes. Subsequent Bronchoalveolar Lavage (BAL) was performed. Preliminary pathology suggests non-small cell carcinoma.",
            3: "CPT Justification: 31627 (Navigational Bronchoscopy) utilized electromagnetic guidance to RML. 31654 (rEBUS) confirmed target peripherally. 31629 (TBNA) performed on 23mm nodule with 7 passes under direct visualization. 31624 (BAL) performed at RB5. Medical necessity: Diagnosis of ground glass opacity.",
            4: "Resident Note:\nProcedure: Robotic Bronchoscopy (Monarch).\nAttending: Dr. Williams.\nSteps:\n1. Time out. GA induced.\n2. Robot docked.\n3. Navigated to RML (Medial Segment).\n4. rEBUS: Adjacent view.\n5. 21G needle biopsy x 7 passes.\n6. BAL x 1.\nFindings: Suspicious for malignancy on ROSE.\nComplications: None.",
            5: "pt brought to bronch suite for biopsy of rml nodule 23mm used monarch robot registration was good 3.7mm error navigated to rb5 saw lesion on rebus adjacent view stuck it 7 times with 21g needle rose said cancer suspected did a wash too no bleeding pt tolerated well extubated sent to pacu cxr ordered.",
            6: "After the successful induction of general anesthesia a timeout was performed confirming patient identity procedure and laterality. An 8.0 ETT was secured. The Monarch robotic endoscope was introduced. Electromagnetic registration was completed with error of 3.7mm. The device was navigated to the RML. The outer sheath was parked at RB5. rEBUS performed showing adjacent view. TBNA performed with 21G needle for 7 passes under continuous visualization. BAL performed. ROSE was suspicious for non-small cell carcinoma. No complications.",
            7: "[Indication] Ground glass opacity, 23mm RML nodule.\n[Anesthesia] General, 8.0 ETT.\n[Description] Monarch robot navigated to Medial Segment RML. Registration error 3.7mm. rEBUS adjacent. 21G TBNA x7 passes performed. BAL performed.\n[Plan] Discharge if stable. Results pending.",
            8: "We proceeded with the induction of anesthesia and secured the airway. The robotic bronchoscope was registered to the electromagnetic field with high accuracy. We navigated specifically to the medial segment of the right middle lobe. Using radial EBUS, we identified the target lesion adjacent to the probe. We then performed transbronchial needle aspiration, ensuring the needle tip was visible exiting the scope before each of the seven passes. A lavage was also collected. The immediate ROSE assessment was concerning for carcinoma.",
            9: "Robotic endoscopy commenced after anesthesia. Registration verified with 3.7mm deviation. The instrument was steered to the RML. The sheath was anchored at the RB5 ostium. Radial EBUS verified the lesion location as adjacent. Biopsies were acquired using a 21G aspiration needle with 7 actuations under direct sight. Lavage was conducted. Preliminary analysis indicated malignancy. The system was withdrawn without trauma."
        },
        1: { # Lee, Melissa (LLL Nodule, 19G TBNA, Forceps, BAL)
            1: "Procedure: Robotic Bronchoscopy LLL.\nTarget: 20mm nodule.\nActions: Navigated to LB7+8. Locked sheath. rEBUS adjacent.\nSampling: 19G TBNA x7. Forceps biopsy x6. BAL performed.\nROSE: Negative for malignancy.\nIssues: None.",
            2: "The patient presented for diagnostic evaluation of a dominant pulmonary nodule. Following general anesthesia, the Monarch robotic system was deployed. Navigation to the Left Lower Lobe (LB7+8) was successful with a registration error of 4.8mm. Radial EBUS demonstrated an adjacent signature. We performed Transbronchial Needle Aspiration (19G, 7 passes) and Transbronchial Forceps Biopsy (6 specimens) under continuous endoscopic monitoring. Bronchoalveolar lavage was completed. Rapid on-site evaluation showed no malignant cells.",
            3: "Codes submitted: 31629 (TBNA), 31628 (Forceps Biopsy), 31627 (Navigation), 31654 (EBUS), 31624 (BAL). Tools: Monarch Platform, 19G Needle, Standard Forceps. Target: LLL Anteromedial-Basal segment. Verification: Continuous visualization maintained.",
            4: "Fellow Note\nPt: Lee.\nProc: Monarch LLL Biopsy.\n1. ETT placed.\n2. Navigated to LB7+8.\n3. rEBUS: Adjacent.\n4. TBNA 19G (7 passes).\n5. Forceps (6 bites).\n6. BAL.\nROSE: Benign so far.\nPlan: PACU.",
            5: "monarch bronch for lll nodule 20mm anesthesia good tube in navigated to lb7+8 registration 4.8mm rebus showed adjacent lesion did 19g needle 7 times then forceps 6 times watched it the whole time no bleeding bal done rose said no cancer seen extubated fine.",
            6: "The patient was positioned and anesthesia induced. The Monarch robotic scope was inserted. Registration accuracy was 4.8mm. Navigation to the LLL Anteromedial-Basal Segment was achieved. rEBUS showed an adjacent view. 19G TBNA was performed for 7 passes followed by forceps biopsy for 6 specimens with continuous visualization. BAL was performed. ROSE result was negative for malignancy. The patient tolerated the procedure well.",
            7: "[Indication] 20mm LLL nodule.\n[Anesthesia] General.\n[Description] Robotic navigation to LB7+8. rEBUS adjacent. 19G TBNA x7. Forceps biopsy x6. BAL x1. Continuous visualization used.\n[Plan] Post-procedure CXR. Discharge.",
            8: "We navigated the robotic device to the left lower lobe, specifically the anteromedial-basal segment. Once the sheath was locked in place, we utilized radial EBUS to confirm the lesion's adjacent location. We then proceeded to sample the area using a 19-gauge needle for seven passes, followed by six biopsies using standard forceps. A lavage was also performed. Fortunately, the on-site evaluation showed no evidence of malignancy.",
            9: "The robotic device was piloted to the LLL. The outer cannula was secured at the LB7+8 opening. Radial EBUS corroborated the target location as adjacent. Needle aspiration was executed with a 19G tool for 7 attempts. Tissue extraction via forceps yielded 6 samples. Fluid wash was collected. Immediate cytology was negative for neoplasm."
        },
        2: { # Williams, Ryan (LLL Nodule, 22G TBNA, Brush, BAL)
            1: "Action: Monarch to LLL (LB10).\nImaging: rEBUS adjacent.\nBx: 22G TBNA x6. Protected brush.\nWash: BAL LB10.\nROSE: Atypical/Suspicious.\nStatus: Stable.",
            2: "PROCEDURE PERFORMED: Robotic-assisted bronchoscopy with electromagnetic navigation. The target was a 14mm nodule in the posterior-basal segment of the LLL. Registration error was 2.2mm. Upon reaching the target, radial EBUS confirmed an adjacent relationship. Diagnostic maneuvers included Transbronchial Needle Aspiration (22G, 6 passes) and Protected Cytology Brushing. Bronchoalveolar lavage was also obtained. Cytopathology review suggests malignancy.",
            3: "Billing 31629 (TBNA), 31623 (Brush), 31627 (Nav), 31654 (EBUS), 31624 (BAL). Navigation utilized to reach LB10. Continuous visualization used for 6 needle passes and brushing. rEBUS confirmed target.",
            4: "Procedure Log: LLL Biopsy.\nMethod: Monarch Robot.\nTarget: 14mm nodule.\n1. Registration (2.2mm).\n2. Nav to LB10.\n3. rEBUS (Adjacent).\n4. 22G Needle x 6.\n5. Brush.\n6. BAL.\nResult: ROSE suspicious.",
            5: "ryan williams bronchoscopy robotic lll nodule 14mm navigated to lb10 error 2.2mm rebus adjacent used 22g needle 6 times then the brush bal done rose says suspicious for cancer no bleeding pt did great.",
            6: "General anesthesia was induced. The Monarch robotic endoscope was inserted. Electromagnetic registration was completed. The device was navigated to the LLL posterior-basal segment. rEBUS view was adjacent. 22G TBNA was performed for 6 passes. Protected cytology brushings were obtained. BAL was performed. ROSE showed atypical cells suspicious for malignancy. The patient was extubated and stable.",
            7: "[Indication] 14mm LLL nodule.\n[Anesthesia] General.\n[Description] Robotic nav to LB10. rEBUS adjacent. 22G TBNA x6. Brush biopsy. BAL. ROSE suspicious.\n[Plan] Monitor. Discharge.",
            8: "We successfully navigated the robotic scope to the posterior-basal segment of the left lower lobe. The registration was highly accurate. Radial EBUS imaging showed the lesion adjacent to the airway. We collected samples using a 22-gauge needle for six passes and also utilized a protected cytology brush. A lavage was performed at the site. The preliminary results indicated atypical cells.",
            9: "The robotic system was directed to the LLL. Registration deviation was 2.2mm. The instrument reached the LB10 bronchus. Ultrasound verification showed an adjacent lesion. Aspiration via 22G needle was conducted 6 times. Brushings were gathered under direct sight. Lavage was completed. Initial findings were wary for malignancy."
        },
        3: { # Rivera, Kenneth (Lingula Nodule, 22G TBNA, Brush)
            1: "Target: 13mm Lingula nodule.\nTech: Monarch robot. rEBUS Concentric.\nBx: 22G TBNA x5. Brush.\nNo BAL.\nROSE: Suspicious.",
            2: "NARRATIVE: The patient underwent robotic bronchoscopy for a 13mm incidental nodule in the Superior Lingula. Electromagnetic navigation was precise (2.0mm error). Navigation to LB4 was achieved. Radial EBUS revealed a concentric view, confirming the target. We proceeded with Transbronchial Needle Aspiration using a 22G needle (5 passes) and protected specimen brushing. No lavage was performed. On-site pathology was suspicious for malignancy.",
            3: "Coding: 31629 (TBNA), 31623 (Brush), 31627 (Nav), 31654 (EBUS). Note: No BAL performed. Navigated to Lingula (LB4). rEBUS concentric view confirmed target. 22G needle used.",
            4: "Steps:\n1. GA/ETT.\n2. Robot to Lingula.\n3. rEBUS: Concentric.\n4. 22G Needle x 5.\n5. Brush.\nROSE: Suspicious.\nPlan: CXR.",
            5: "rivera kenneth lingula nodule 13mm robotic bronchoscopy navigation was good 2mm error went to lb4 rebus concentric 22g needle 5 passes brush too rose says suspicious no bal done bleeding minimal.",
            6: "The patient was intubated. Monarch robotic system used. Navigated to Superior Lingula LB4. Registration error 2.0mm. rEBUS showed concentric view. 22G TBNA performed 5 times. Protected brushings obtained. ROSE reported atypical cells suspicious for malignancy. No complications.",
            7: "[Indication] 13mm Lingula nodule.\n[Anesthesia] General.\n[Description] Nav to Lingula. rEBUS concentric. 22G TBNA x5. Brush. No BAL.\n[Plan] Recovery.",
            8: "We guided the robotic bronchoscope to the superior segment of the Lingula. The electromagnetic registration was excellent. We confirmed the lesion location with a concentric view on radial EBUS. We then took five samples using a 22-gauge needle and obtained additional cells with a cytology brush. The on-site pathologist identified cells suspicious for cancer.",
            9: "The robotic probe was steered to the Lingula. Registration variance was 2.0mm. The scope was parked at LB4. Sonographic assessment showed a concentric target. Needle aspiration was performed with a 22G device for 5 cycles. Brushing was also executed. Early pathology indicated malignancy."
        },
        4: { # Hernandez, Brian (Lingula Nodule, 19G TBNA, Forceps, Brush, BAL)
            1: "Site: 35mm Lingula.\nSystem: Monarch.\nrEBUS: Adjacent.\nTools: 19G needle (7x), Forceps (6x), Brush.\nFluid: BAL LB4.\nROSE: Suspicious NSCC.",
            2: "OPERATIVE REPORT: The patient presented for biopsy of a 35mm Lingula mass. Robotic navigation (Monarch) was employed with 3.0mm accuracy. Upon reaching the Superior Lingula (LB4), radial EBUS demonstrated an adjacent view. Extensive sampling was performed including 19G TBNA (7 passes), Transbronchial Forceps Biopsy (6 specimens), and Protected Brushing. A BAL was also collected. Immediate evaluation suggests non-small cell carcinoma.",
            3: "Codes: 31629 (TBNA), 31628 (Forceps), 31623 (Brush), 31627 (Nav), 31654 (EBUS), 31624 (BAL). Extensive sampling of Lingula mass. 19G needle, standard forceps, and brush used under continuous visualization.",
            4: "Resident Procedure Note:\nLingula Mass Biopsy.\nMonarch Robot used.\nNavigated to LB4.\nrEBUS: Adjacent.\n1. 19G TBNA x 7.\n2. Forceps x 6.\n3. Brush.\n4. BAL.\nROSE: Suspicious.",
            5: "brian hernandez 35mm lingula mass biopsy with monarch robot navigation ok 3mm error saw it on rebus adjacent 19g needle 7 times forceps 6 times brush and bal rose looks like nscc patient did fine.",
            6: "General anesthesia induced. Monarch robotic scope inserted. Navigated to Superior Lingula. rEBUS adjacent. 19G TBNA x 7. Forceps biopsy x 6. Brush biopsy. BAL LB4. ROSE suspicious for non-small cell carcinoma. No complications.",
            7: "[Indication] 35mm Lingula mass.\n[Anesthesia] General.\n[Description] Robotic nav to LB4. rEBUS adjacent. 19G TBNA x7. Forceps x6. Brush. BAL.\n[Plan] Discharge.",
            8: "We navigated the robotic system to the superior lingula segment. Radial EBUS confirmed the target was adjacent to the airway. We performed a comprehensive biopsy using a 19-gauge needle for seven passes, followed by six forceps biopsies and a cytology brush. A bronchoalveolar lavage was also completed. The on-site analysis was suspicious for non-small cell carcinoma.",
            9: "The robotic endoscope was driven to the Lingula. Registration error was 3.0mm. The device was locked at LB4. Ultrasound showed an adjacent lesion. Sampling included 19G aspiration (7x), tissue forceps (6x), and brushing. Lavage was performed. Preliminary findings pointed to carcinoma."
        },
        5: { # Clark, Carol (LUL Nodule, 19G TBNA, Forceps)
            1: "Loc: LUL (LB3).\nSize: 27mm.\nNav: Monarch (4.2mm error).\nrEBUS: Adjacent.\nBx: 19G TBNA (4x), Forceps (6x).\nROSE: Granuloma.",
            2: "PROCEDURE: Robotic bronchoscopy for a growing 27mm LUL nodule. Navigation to the Anterior Segment (LB3) was completed. Radial EBUS identified the lesion with an adjacent orientation. We obtained diagnostic tissue via 19G Transbronchial Needle Aspiration (4 passes) and Transbronchial Forceps Biopsy (6 specimens). No lavage was performed. On-site pathology indicated granulomatous inflammation.",
            3: "Billing 31629, 31628, 31627, 31654. Note: No BAL. 19G TBNA x4 and Forceps x6 in LUL. rEBUS used for confirmation. Continuous guidance maintained.",
            4: "Procedure: Monarch LUL Biopsy.\nTarget: 27mm nodule.\n1. Nav to LB3.\n2. rEBUS: Adjacent.\n3. 19G TBNA x 4.\n4. Forceps x 6.\nROSE: Granulomatous.\nNo BAL.",
            5: "carol clark lul nodule 27mm monarch robot used registration 4.2mm error navigated to lb3 rebus adjacent 19g needle 4 times forceps 6 times rose says granuloma no bal bleeding stopped easily.",
            6: "Anesthesia induced. Monarch robot navigated to LUL Anterior Segment. Registration error 4.2mm. rEBUS adjacent. 19G TBNA performed 4 times. Forceps biopsy performed 6 times. ROSE showed granulomatous inflammation. No BAL performed. Patient stable.",
            7: "[Indication] 27mm LUL nodule.\n[Anesthesia] General.\n[Description] Nav to LB3. rEBUS adjacent. 19G TBNA x4. Forceps x6. ROSE granuloma.\n[Plan] Follow up.",
            8: "We utilized the Monarch robot to navigate to the anterior segment of the left upper lobe. After confirming the target with adjacent radial EBUS views, we sampled the 27mm nodule. We used a 19-gauge needle for four passes and forceps for six bites. The on-site evaluation suggested granulomatous inflammation, so no further sampling was needed.",
            9: "The robotic instrument was guided to the LUL. Registration variance was 4.2mm. The scope reached LB3. Sonography indicated an adjacent mass. Aspiration with a 19G needle was done 4 times. Tissue extraction via forceps occurred 6 times. Initial pathology revealed granuloma."
        },
        6: { # Hall, Edward (Lingula Nodule, 19G TBNA, Forceps, Brush, BAL)
            1: "Target: 14mm Lingula (LB5).\nRobot: Monarch.\nrEBUS: Eccentric.\nBx: 19G TBNA x5, Forceps x5, Brush.\nWash: BAL LB5.\nROSE: Benign/Lymphocytes.",
            2: "NARRATIVE: The patient underwent robotic bronchoscopy for a 14mm nodule in the Inferior Lingula. Navigation to LB5 was successful (4.7mm error). Radial EBUS showed an eccentric view. We performed 19G TBNA (5 passes), Forceps Biopsy (5 specimens), and Protected Brushing. BAL was also performed. ROSE showed lymphocytes and benign cells.",
            3: "CPT: 31629, 31628, 31623, 31627, 31654, 31624. Full sampling suite used on 14mm Lingula nodule. 19G needle, forceps, brush, and lavage.",
            4: "Monarch Case.\nLingula nodule.\n1. Nav to LB5.\n2. rEBUS Eccentric.\n3. 19G Needle x 5.\n4. Forceps x 5.\n5. Brush.\n6. BAL.\nROSE: Benign.",
            5: "edward hall lingula nodule 14mm robotic bronch used monarch nav to lb5 rebus eccentric 19g needle 5 passes forceps 5 passes brush and bal rose benign lymphocytes pt did fine.",
            6: "General anesthesia. Monarch robot used. Navigated to Lingula LB5. rEBUS eccentric. 19G TBNA x 5. Forceps x 5. Brush. BAL. ROSE benign. No complications.",
            7: "[Indication] 14mm Lingula nodule.\n[Anesthesia] General.\n[Description] Nav to LB5. rEBUS eccentric. 19G TBNA x5. Forceps x5. Brush. BAL. ROSE benign.\n[Plan] Discharge.",
            8: "We navigated the robotic scope to the inferior lingula segment. Radial EBUS showed an eccentric view of the target. We performed five needle passes with a 19-gauge needle, followed by five forceps biopsies and brushing. A lavage was also collected. The on-site evaluation showed only benign cells and lymphocytes.",
            9: "The robotic device was steered to the Lingula. Registration error was 4.7mm. The probe was anchored at LB5. Ultrasound showed an eccentric lesion. 19G aspiration (5x), forceps extraction (5x), and brushing were performed. Lavage was done. Pathology was benign."
        },
        7: { # Adams, Jonathan (LUL Nodule, 19G TBNA, Forceps, BAL)
            1: "Target: 20mm LUL (LB3).\nMethod: Monarch.\nrEBUS: Eccentric.\nBx: 19G TBNA x8, Forceps x5.\nWash: BAL LB3.\nROSE: Benign.",
            2: "OPERATIVE REPORT: Robotic bronchoscopy for 20mm LUL nodule. Navigation to Anterior Segment (LB3) achieved with 2.3mm error. rEBUS demonstrated eccentric view. 19G TBNA (8 passes) and Forceps Biopsy (5 specimens) performed under continuous visualization. BAL completed. ROSE was negative for malignancy.",
            3: "Codes: 31629, 31628, 31627, 31654, 31624. Note: High number of needle passes (8). Forceps used. Navigated to LUL. rEBUS eccentric.",
            4: "Resident Note: LUL Biopsy.\nMonarch Robot.\n1. Nav to LB3.\n2. rEBUS Eccentric.\n3. 19G Needle x 8.\n4. Forceps x 5.\n5. BAL.\nROSE: Neg for malignancy.",
            5: "jonathan adams lul nodule 20mm monarch robot navigation good 2.3mm error rebus eccentric 19g needle 8 times forceps 5 times bal done rose benign no cancer seen.",
            6: "Anesthesia induced. Monarch robot navigated to LUL LB3. rEBUS eccentric. 19G TBNA x 8. Forceps x 5. BAL performed. ROSE negative for malignancy. Patient stable.",
            7: "[Indication] 20mm LUL nodule.\n[Anesthesia] General.\n[Description] Nav to LB3. rEBUS eccentric. 19G TBNA x8. Forceps x5. BAL. ROSE benign.\n[Plan] Discharge.",
            8: "We used the Monarch robot to navigate to the anterior segment of the left upper lobe. The registration was very accurate. Radial EBUS showed an eccentric view of the 20mm nodule. We performed eight passes with a 19-gauge needle and took five forceps biopsies. A lavage was also performed. The on-site evaluation was negative for malignancy.",
            9: "The robotic system was piloted to the LUL. Registration deviation was 2.3mm. The instrument reached LB3. Sonography indicated an eccentric mass. Aspiration via 19G needle was conducted 8 times. Tissue extraction via forceps occurred 5 times. Lavage was completed. Initial pathology was benign."
        },
        8: { # Taylor, Stephen (RLL Nodule, 21G TBNA, Forceps, Brush, BAL)
            1: "Loc: 20mm RLL (RB8).\nRobot: Monarch.\nrEBUS: Concentric.\nBx: 21G TBNA x6, Forceps x7, Brush.\nWash: BAL RB8.\nROSE: Atypical/Suspicious.",
            2: "PROCEDURE: Robotic bronchoscopy for 20mm RLL nodule. Navigation to Anterior-Basal Segment (RB8) completed (4.8mm error). rEBUS confirmed concentric view. 21G TBNA (6 passes), Forceps (7 specimens), and Brush biopsy performed. BAL collected. ROSE suspicious for malignancy.",
            3: "Billing: 31629, 31628, 31623, 31627, 31654, 31624. Extensive sampling of RLL nodule. 21G needle, forceps, brush used. rEBUS concentric.",
            4: "Procedure: RLL Biopsy.\nMonarch.\n1. Nav to RB8.\n2. rEBUS Concentric.\n3. 21G Needle x 6.\n4. Forceps x 7.\n5. Brush.\n6. BAL.\nROSE: Suspicious.",
            5: "stephen taylor rll nodule 20mm monarch robot used registration 4.8mm error navigated to rb8 rebus concentric 21g needle 6 times forceps 7 times brush and bal rose suspicious for cancer.",
            6: "General anesthesia. Monarch robot used. Navigated to RLL RB8. rEBUS concentric. 21G TBNA x 6. Forceps x 7. Brush. BAL. ROSE suspicious. No complications.",
            7: "[Indication] 20mm RLL nodule.\n[Anesthesia] General.\n[Description] Nav to RB8. rEBUS concentric. 21G TBNA x6. Forceps x7. Brush. BAL. ROSE suspicious.\n[Plan] Discharge.",
            8: "We navigated the robotic scope to the anterior-basal segment of the right lower lobe. Radial EBUS confirmed a concentric view of the target. We performed six needle passes with a 21-gauge needle, followed by seven forceps biopsies and a cytology brush. A lavage was also performed. The on-site evaluation showed atypical cells suspicious for malignancy.",
            9: "The robotic device was steered to the RLL. Registration error was 4.8mm. The probe was anchored at RB8. Ultrasound showed a concentric lesion. 21G aspiration (6x), forceps extraction (7x), and brushing were performed. Lavage was done. Pathology was suspicious."
        },
        9: { # Johnson, Rebecca (RML Nodule, 19G TBNA, Forceps, Brush)
            1: "Target: 33mm RML (RB4).\nTech: Monarch.\nrEBUS: Concentric.\nBx: 19G TBNA x5, Forceps x7, Brush.\nNo BAL.\nROSE: Benign.",
            2: "NARRATIVE: Robotic bronchoscopy for 33mm RML nodule. Navigation to Lateral Segment (RB4) achieved. rEBUS showed concentric view. 19G TBNA (5 passes), Forceps (7 specimens), and Brush biopsy performed. No lavage. ROSE benign.",
            3: "CPT: 31629, 31628, 31623, 31627, 31654. No BAL. 19G needle, forceps, brush used on RML nodule. rEBUS concentric.",
            4: "Monarch Case.\nRML nodule.\n1. Nav to RB4.\n2. rEBUS Concentric.\n3. 19G Needle x 5.\n4. Forceps x 7.\n5. Brush.\nROSE: Benign.",
            5: "rebecca johnson rml nodule 33mm robotic bronch monarch used navigated to rb4 rebus concentric 19g needle 5 passes forceps 7 passes brush rose benign no bal done.",
            6: "Anesthesia induced. Monarch robot navigated to RML RB4. rEBUS concentric. 19G TBNA x 5. Forceps x 7. Brush. ROSE benign. No BAL. Patient stable.",
            7: "[Indication] 33mm RML nodule.\n[Anesthesia] General.\n[Description] Nav to RB4. rEBUS concentric. 19G TBNA x5. Forceps x7. Brush. ROSE benign.\n[Plan] Discharge.",
            8: "We used the Monarch robot to navigate to the lateral segment of the right middle lobe. Radial EBUS showed a concentric view of the large 33mm nodule. We performed five passes with a 19-gauge needle, followed by seven forceps biopsies and brushing. The on-site evaluation was benign.",
            9: "The robotic system was piloted to the RML. The instrument reached RB4. Sonography indicated a concentric mass. Aspiration via 19G needle was conducted 5 times. Tissue extraction via forceps occurred 7 times. Brushing was performed. Initial pathology was benign."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the 10 patients to ensure unique demographics for variations.
    Each entry contains 9 name variations corresponding to the 9 styles.
    """
    return [
        {"idx": 0, "orig_name": "Wilson, David", "orig_age": 68, "names": ["John Smith", "Arthur King", "Robert Jones", "William Brown", "James Davis", "Edward Miller", "Richard Wilson", "Thomas Moore", "Gary Taylor"]},
        {"idx": 1, "orig_name": "Lee, Melissa", "orig_age": 80, "names": ["Sarah Anderson", "Linda Thomas", "Nancy Jackson", "Karen White", "Barbara Harris", "Mary Martin", "Susan Thompson", "Margaret Garcia", "Betty Martinez"]},
        {"idx": 2, "orig_name": "Williams, Ryan", "orig_age": 67, "names": ["Michael Robinson", "Robert Clark", "David Rodriguez", "Joseph Lewis", "Frank Lee", "Paul Walker", "George Hall", "Kenneth Allen", "Steven Young"]},
        {"idx": 3, "orig_name": "Rivera, Kenneth", "orig_age": 67, "names": ["Daniel Hernandez", "Mark King", "Charles Wright", "Donald Lopez", "Brian Hill", "Kevin Scott", "Edward Green", "Ronald Adams", "Anthony Baker"]},
        {"idx": 4, "orig_name": "Hernandez, Brian", "orig_age": 57, "names": ["Jason Gonzalez", "Jeffery Nelson", "Ryan Carter", "Jacob Mitchell", "Gary Perez", "Nicholas Roberts", "Eric Turner", "Stephen Phillips", "Andrew Campbell"]},
        {"idx": 5, "orig_name": "Clark, Carol", "orig_age": 55, "names": ["Jennifer Parker", "Maria Evans", "Lisa Edwards", "Dorothy Collins", "Sandra Stewart", "Ashley Sanchez", "Kimberly Morris", "Donna Rogers", "Carol Reed"]},
        {"idx": 6, "orig_name": "Hall, Edward", "orig_age": 75, "names": ["Brian Cook", "Timothy Morgan", "Ronald Bell", "George Murphy", "Kenneth Bailey", "Steven Rivera", "Edward Cooper", "Jerry Richardson", "Dennis Cox"]},
        {"idx": 7, "orig_name": "Adams, Jonathan", "orig_age": 65, "names": ["Gregory Howard", "Joshua Ward", "Jerry Torres", "Dennis Peterson", "Walter Gray", "Patrick Ramirez", "Peter James", "Harold Watson", "Douglas Brooks"]},
        {"idx": 8, "orig_name": "Taylor, Stephen", "orig_age": 58, "names": ["Walter Kelly", "Patrick Sanders", "Peter Price", "Harold Bennett", "Douglas Wood", "Henry Barnes", "Carl Ross", "Arthur Henderson", "Ryan Coleman"]},
        {"idx": 9, "orig_name": "Johnson, Rebecca", "orig_age": 64, "names": ["Michelle Jenkins", "Laura Perry", "Sarah Powell", "Kimberly Long", "Deborah Patterson", "Jessica Hughes", "Shirley Flores", "Cynthia Washington", "Angela Butler"]}
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
            
            # Update note_text with the pre-generated variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation is missing (shouldn't happen with full dictionary)
                note_entry["note_text"] = f"Variation {style_num} for note {idx} not found."

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
    output_filename = output_dir / "synthetic_monarch_notes_part_090.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()