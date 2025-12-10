import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_068.json"
OUTPUT_FILENAME = "synthetic_ion_robotic_notes_part_068.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Mary Mitchell (RML Nodule, Ion, TBNA/Cryo/Brush, Benign)
            1: "Procedure: Robotic Bronchoscopy RML.\n- Airway: Normal.\n- Nav: Ion to RML Medial (RB5). 1.9mm error.\n- Confirmation: rEBUS (adjacent). Cone beam CT (spin).\n- Sampling: 23G TBNA x5. 1.7mm Cryo x3 (5s freeze). Brush x2.\n- ROSE: Benign epithelium/macrophages.\n- Complications: None.\n- Plan: CXR. Discharge.",
            2: "OPERATIVE NARRATIVE: The patient was intubated and general anesthesia induced. The tracheobronchial tree was inspected and cleared of secretions via therapeutic aspiration. Utilizing the Ion robotic platform, the catheter was navigated to the Medial Segment of the Right Middle Lobe (RB5). Shape-sensing registration yielded an error of 1.9mm. Radial EBUS demonstrated an adjacent acoustic signature. 3D volumetric confirmation was achieved via the Cios Spin Cone Beam CT system. Subsequently, the lesion was sampled via 23G transbronchial needle aspiration (5 passes), 1.7mm transbronchial cryobiopsy (3 specimens, 5-second freeze), and protected cytologic brushing (2 passes). Rapid On-Site Evaluation (ROSE) indicated benign respiratory epithelium and macrophages. The procedure concluded without adverse events.",
            3: "Code Selection Justification:\n31629 (TBNA): Performed 5 passes with 23G needle in RML.\n31628 (Cryo): Performed 3 biopsies with 1.7mm probe.\n31623 (Brush): 2 protected brush samples obtained.\n31627 (Nav): Ion robotic platform used with 3D planning and registration (1.9mm error).\n31654 (REBUS): Radial probe used to confirm lesion adjacency.\nTechnique: Navigation to RML (RB5), confirmation via Cone Beam CT/rEBUS. Tool-in-lesion confirmed. No complications.",
            4: "Resident Procedure Note\nPatient: Mary Mitchell\nAttending: Dr. Wilson\nProcedure Steps:\n1. Time out/Anesthesia.\n2. Airway inspection (normal).\n3. Ion robot navigation to RML Medial Segment (RB5).\n4. rEBUS check: Adjacent view.\n5. Cone Beam CT spin for tool-in-lesion confirmation.\n6. Biopsies: 23G needle (x5), 1.7mm cryo (x3), Brush (x2).\n7. ROSE: Benign.\n8. Extubation. Stable.",
            5: "Procedure note pt mitchell mary here for lung nodule rml we used the ion robot anesthesia was general. Airway looked fine cleared some mucus out. Navigated to the medial segment RB5 got close 1.9mm error. Checked with radial ebus it was adjacent then did the spin ct to confirm. Took samples with 23g needle five times then the cryo probe 1.7mm three times five sec freeze also brushed it twice. Pathologist said benign cells. No bleeding patient woke up fine check xray for pneumo.",
            6: "Mary Mitchell. 10/23/2025. Indication: Lung-RADS 4B nodule RML. General Anesthesia. Airway clear. Ion robotic bronchoscopy performed. Navigated to RML Medial segment. rEBUS: Adjacent. CBCT performed for confirmation. Samples: 5x 23G TBNA, 3x 1.7mm Cryo, 2x Brush. ROSE: Benign respiratory epithelium. No complications. Plan: Recovery/Discharge.",
            7: "[Indication]\nLung-RADS 4B nodule, 35mm in RML.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon robotic navigation to RML (RB5). rEBUS (adjacent) and Cone Beam CT confirmation. 5 TBNA samples (23G), 3 Cryobiopsies (1.7mm), 2 Brushings. ROSE: Benign.\n[Plan]\nCXR, Discharge.",
            8: "Under general anesthesia, Mary Mitchell underwent a robotic bronchoscopy. The airway was inspected and found to be normal. We utilized the Ion platform to navigate to the 35mm target in the Medial Segment of the Right Middle Lobe. Confirmation was achieved using radial EBUS, which showed an adjacent view, and Cone Beam CT scans. We proceeded to collect samples using a 23G needle for five passes, a 1.7mm cryoprobe for three biopsies with a 5-second freeze time, and a cytology brush for two samples. The on-site pathology review showed benign cells. The patient tolerated the procedure well.",
            9: "Procedure: Robotic bronchoscopy with endobronchial valve placement.\nTarget: RML nodule.\nActions: Guided Ion catheter to RB5. Verified location with rEBUS (adjacent) and CBCT. Sampled lesion using 23G needle (5x), 1.7mm cryoprobe (3x), and brush (2x). Acquired ROSE result: Benign. Retracted instruments. Extubated patient."
        },
        1: { # Dorothy White (LLL Nodule, Ion, TBNA/Cryo/Brush/BAL, Benign)
            1: "Procedure: Ion Bronchoscopy LLL.\n- Target: 30mm nodule Anteromedial-Basal (LB7+8).\n- Nav: Ion, 2.5mm error.\n- Verify: rEBUS (concentric), CBCT.\n- Samples: 21G TBNA x8, 1.7mm Cryo x6 (5s), Brush x2, BAL.\n- ROSE: Benign.\n- Outcome: Stable.",
            2: "OPERATIVE SUMMARY: Ms. White presented for evaluation of a screen-detected LLL nodule. Following induction, the Ion robotic catheter was navigated to the Anteromedial-Basal Segment (LB7+8). Radial EBUS demonstrated a concentric view, and Cone Beam CT 3D reconstruction confirmed tool-in-lesion. Extensive sampling was performed: 8 passes with a 21G needle, 6 cryobiopsies using a 1.7mm probe (5-second freeze), and 2 brushings. Additionally, a bronchoalveolar lavage was instilled. Preliminary ROSE analysis indicated benign respiratory epithelium. The patient remained hemodynamically stable.",
            3: "Billing Codes:\n31629: TBNA 21G x8.\n31628: Cryobiopsy 1.7mm x6.\n31624: BAL instilled/returned.\n31623: Brushing x2.\n31627: Robotic Nav (Ion) used.\n31654: rEBUS utilized.\nSpecifics: LLL LB7+8 target. 30mm lesion. CBCT verification used.",
            4: "Fellow Note\nPatient: Dorothy White\nTarget: LLL Nodule\nSteps:\n1. GA/ETT.\n2. Ion Nav to LB7+8.\n3. rEBUS (concentric) + CBCT confirmation.\n4. TBNA: 21G x 8 passes.\n5. Cryo: 1.7mm x 6 biopsies.\n6. Brush: x 2.\n7. BAL: 60cc instilled.\n8. ROSE: Benign.\nNo complications.",
            5: "Dorothy White procedure note. We did the ion bronch for the LLL nodule 30mm. Anesthesia was fine tube in good position. Navigated to the anteromedial basal segment LB7+8 reg error 2.5mm. Used radial ebus saw it concentric then did the spin CT. Took a lot of samples 8 with the 21g needle 6 with the cryo probe and 2 brushes plus a lavage. Rose said benign cells. Patient did fine no bleeding.",
            6: "Dorothy White. Ion Bronchoscopy. LLL Nodule (30mm). Navigation to LB7+8. rEBUS: Concentric. CBCT: Tool-in-lesion. Samples: 8x 21G TBNA, 6x 1.7mm Cryo, 2x Brush, BAL. ROSE: Benign. Disposition: Recovery.",
            7: "[Indication]\nLung cancer screening nodule, LLL.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB7+8. Verified with rEBUS (concentric) and CBCT. Sampled via 21G TBNA (x8), 1.7mm Cryo (x6), Brush (x2), and BAL. ROSE: Benign.\n[Plan]\nDischarge if stable.",
            8: "Ms. White underwent a robotic bronchoscopy targeting a 30mm nodule in the Left Lower Lobe. We used the Ion platform to navigate to the Anteromedial-Basal Segment. Once there, we confirmed the position with a concentric radial EBUS view and Cone Beam CT. We then performed extensive sampling, including eight needle aspirations with a 21G needle, six cryobiopsies, two brushings, and a bronchoalveolar lavage. The rapid on-site evaluation showed benign cells.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: LLL nodule.\nTechnique: Steered Ion catheter to LB7+8. Confirmed with rEBUS and CBCT. Aspirated with 21G needle (8x). Biopsied with 1.7mm cryoprobe (6x). Brushed (2x). Lavaged. ROSE Result: Benign. Patient stable."
        },
        2: { # Kevin Jackson (Lingula Nodule, Ion, TBNA/Cryo/Brush, Malignant)
            1: "Procedure: Ion Bronchoscopy Lingula.\n- Target: 11mm nodule Inferior Lingula (LB5).\n- Nav: Ion, 2.5mm error.\n- Verify: rEBUS (eccentric).\n- Samples: 21G/23G TBNA x4, 1.7mm Cryo x6 (5s), Brush x2.\n- ROSE: Malignant (Adenocarcinoma).\n- Outcome: Stable.",
            2: "PROCEDURE NOTE: Mr. Jackson, with a history of malignancy, presented for biopsy of an 11mm Lingula nodule. Using the Ion robotic platform, we navigated to the Inferior Lingula (LB5). Radial EBUS revealed an eccentric view. Following active locking of the robotic arm, sampling was performed utilizing both 21G and 23G needles (4 passes), a 1.7mm cryoprobe (6 biopsies), and a cytology brush (2 samples). ROSE confirmed malignancy consistent with adenocarcinoma. There were no immediate complications.",
            3: "Coding Data:\n31629 (TBNA): 4 samples, 21G/23G.\n31628 (Cryo): 6 samples, 1.7mm.\n31623 (Brush): 2 samples.\n31627 (Nav): Ion platform.\n31654 (REBUS): Eccentric view.\nLocation: Lingula (LB5). Diagnosis: Adenocarcinoma confirmed on ROSE.",
            4: "Resident Procedure Note\nPatient: Kevin Jackson\nTarget: Lingula Nodule\nSteps:\n1. Intubation.\n2. Ion Nav to LB5.\n3. rEBUS check: Eccentric.\n4. Biopsies: TBNA (x4), Cryo (x6), Brush (x2).\n5. ROSE: Malignant/Adenocarcinoma.\n6. Extubation.\nPlan: Oncology referral.",
            5: "Procedure on Kevin Jackson for that lingula nodule 11mm. Anesthesia general. Ion robot used to get to inferior lingula LB5. Reg error was 2.5mm. Saw it eccentric on rebus. Locked the arm and took samples 4 needle passes 21 and 23g then 6 cryo and 2 brushes. Rose came back malignant adenocarcinoma. Patient woke up ok.",
            6: "Kevin Jackson. Ion Bronchoscopy. Lingula Nodule (11mm). Nav to LB5. rEBUS: Eccentric. Samples: 4x TBNA (21/23G), 6x 1.7mm Cryo, 2x Brush. ROSE: Malignant (Adenocarcinoma). No complications.",
            7: "[Indication]\nPulmonary nodule, prior malignancy.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to Lingula (LB5). rEBUS eccentric. Sampled via TBNA (x4), Cryo (x6), Brush (x2). ROSE: Adenocarcinoma.\n[Plan]\nOncology follow-up.",
            8: "Mr. Jackson underwent a robotic bronchoscopy to biopsy an 11mm nodule in the Lingula. We navigated the Ion catheter to the Inferior Lingula segment. Radial EBUS confirmed the location with an eccentric view. We collected four needle aspirates, six cryobiopsies using a 1.7mm probe, and two brush samples. The on-site pathologist identified malignant cells consistent with adenocarcinoma. The patient tolerated the procedure well.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: Lingula nodule.\nTechnique: Guided Ion catheter to LB5. Verified with rEBUS. Aspirated with 21G/23G needles (4x). Biopsied with 1.7mm cryoprobe (6x). Brushed (2x). ROSE Result: Malignant. Patient stable."
        },
        3: { # Charles Baker (LLL Nodule, Ion, TBNA/Cryo/Brush, Benign)
            1: "Procedure: Ion Bronchoscopy LLL.\n- Target: 22mm nodule Posterior-Basal (LB10).\n- Nav: Ion, 3.3mm error.\n- Verify: rEBUS (eccentric), CBCT.\n- Samples: 21G/23G TBNA x3, 1.1mm Cryo x3 (7s), Brush x2.\n- ROSE: Benign lymphocytes.\n- Outcome: Stable.",
            2: "OPERATIVE REPORT: Mr. Baker underwent robotic bronchoscopy for a suspected LLL malignancy. The Ion catheter was navigated to the Posterior-Basal Segment (LB10) with a 3.3mm registration error. Localization was confirmed via eccentric rEBUS and Cone Beam CT 3D reconstruction. Sampling included 3 passes with 21G/23G needles, 3 cryobiopsies using a 1.1mm probe (7-second freeze), and 2 brushings. ROSE evaluation showed lymphocytes and benign cells. The procedure was uncomplicated.",
            3: "CPT Justification:\n31629: TBNA x3 (21G/23G).\n31628: Cryo x3 (1.1mm).\n31623: Brush x2.\n31627: Ion Navigation.\n31654: rEBUS.\nSite: LLL (LB10). Verification: CBCT/REBUS. Result: Benign/Adequate.",
            4: "Fellow Note\nPatient: Charles Baker\nTarget: LLL Nodule\nSteps:\n1. GA/ETT.\n2. Ion Nav to LB10.\n3. rEBUS (eccentric) + CBCT confirmation.\n4. TBNA: x3 passes.\n5. Cryo: x3 biopsies (1.1mm probe).\n6. Brush: x2.\n7. ROSE: Benign lymphocytes.\nNo complications.",
            5: "Charles Baker procedure note. We did the LLL nodule 22mm today. General anesthesia. Used the Ion robot to get to the posterior basal segment LB10 error was 3.3mm. Eccentric on rebus and confirmed with spin ct. Did 3 needle passes mixed gauges and 3 cryo with the small 1.1 probe plus 2 brushes. Rose said benign lymphocytes. All good.",
            6: "Charles Baker. Ion Bronchoscopy. LLL Nodule (22mm). Nav to LB10. rEBUS: Eccentric. CBCT: Confirmed. Samples: 3x TBNA, 3x 1.1mm Cryo, 2x Brush. ROSE: Benign lymphocytes. Disposition: Stable.",
            7: "[Indication]\nSuspected lung malignancy, LLL.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB10. rEBUS eccentric + CBCT. Sampled via TBNA (x3), Cryo (x3), Brush (x2). ROSE: Benign lymphocytes.\n[Plan]\nDischarge.",
            8: "Mr. Baker underwent a robotic bronchoscopy for a 22mm nodule in the Left Lower Lobe. We navigated the Ion catheter to the Posterior-Basal Segment. We confirmed the location with an eccentric radial EBUS view and Cone Beam CT. We then collected three needle aspirates, three cryobiopsies using a 1.1mm probe, and two brush samples. The preliminary pathology showed lymphocytes and benign cells.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: LLL nodule.\nTechnique: Directed Ion catheter to LB10. Verified with rEBUS and CBCT. Aspirated with needles (3x). Biopsied with 1.1mm cryoprobe (3x). Brushed (2x). ROSE Result: Benign. Patient stable."
        },
        4: { # Kimberly Garcia (LUL Nodule, Ion, TBNA/Brush, Atypical)
            1: "Procedure: Ion Bronchoscopy LUL.\n- Target: 35mm nodule Apicoposterior (LB1+2).\n- Nav: Ion, 2.2mm error.\n- Verify: rEBUS (adjacent), CBCT.\n- Samples: 21G TBNA x6, Brush x2.\n- ROSE: Atypical cells.\n- Outcome: Stable.",
            2: "PROCEDURE NOTE: Ms. Garcia underwent robotic bronchoscopy for a 35mm LUL ground glass opacity. Navigation to the Apicoposterior Segment (LB1+2) was achieved using the Ion platform. Confirmation via adjacent rEBUS and Cone Beam CT was obtained. Sampling consisted of 6 passes with a 21G needle and 2 brushings. ROSE identified atypical cells, preventing exclusion of malignancy. No cryobiopsy was performed. The patient was extubated without issues.",
            3: "Coding:\n31629: TBNA x6 (21G).\n31623: Brush x2.\n31627: Ion Navigation.\n31654: rEBUS.\nSite: LUL (LB1+2). Note: No cryobiopsy performed. CBCT used for verification.",
            4: "Resident Note\nPatient: Kimberly Garcia\nTarget: LUL Nodule\nSteps:\n1. GA/ETT.\n2. Ion Nav to LB1+2.\n3. rEBUS (adjacent) + CBCT confirmation.\n4. TBNA: 21G x 6 passes.\n5. Brush: x 2.\n6. ROSE: Atypical cells.\nNo complications.",
            5: "Kimberly Garcia procedure note. LUL nodule 35mm ground glass. Anesthesia general. Ion robot used to get to apicoposterior segment. Rebus showed adjacent and we did the cone beam ct. Took 6 needle samples 21g and 2 brushes. Path said atypical cells. No bleeding patient fine.",
            6: "Kimberly Garcia. Ion Bronchoscopy. LUL Nodule (35mm). Nav to LB1+2. rEBUS: Adjacent. CBCT: Confirmed. Samples: 6x 21G TBNA, 2x Brush. ROSE: Atypical cells. Disposition: Stable.",
            7: "[Indication]\nGround glass opacity LUL.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB1+2. rEBUS adjacent + CBCT. Sampled via 21G TBNA (x6), Brush (x2). ROSE: Atypical cells.\n[Plan]\nDischarge.",
            8: "Ms. Garcia underwent a robotic bronchoscopy for a 35mm nodule in the Left Upper Lobe. We navigated the Ion catheter to the Apicoposterior Segment. We confirmed the location with an adjacent radial EBUS view and Cone Beam CT. We collected six needle aspirates using a 21G needle and two brush samples. The on-site evaluation showed atypical cells.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: LUL nodule.\nTechnique: Guided Ion catheter to LB1+2. Verified with rEBUS and CBCT. Aspirated with 21G needle (6x). Brushed (2x). ROSE Result: Atypical. Patient stable."
        },
        5: { # Amy Campbell (Lingula Nodule, Ion, TBNA/BAL, Atypical)
            1: "Procedure: Ion Bronchoscopy Lingula.\n- Target: 17mm nodule Inferior Lingula (LB5).\n- Nav: Ion, 2.0mm error.\n- Verify: rEBUS (concentric), CBCT.\n- Samples: 21G/23G TBNA x3, BAL.\n- ROSE: Atypical/Suspicious.\n- Outcome: Stable.",
            2: "OPERATIVE SUMMARY: Ms. Campbell presented for biopsy of a 17mm Lingula nodule. The Ion robotic platform was used to navigate to the Inferior Lingula (LB5). Localization was confirmed with concentric rEBUS and Cone Beam CT. Sampling included 3 transbronchial needle aspirations (21G/23G) and a bronchoalveolar lavage. ROSE results were suspicious for malignancy due to the presence of atypical cells. The procedure was completed without complication.",
            3: "Codes:\n31629: TBNA x3 (21G/23G).\n31624: BAL.\n31627: Ion Navigation.\n31654: rEBUS.\nSite: Lingula (LB5). Verification: CBCT/REBUS. Result: Suspicious for malignancy.",
            4: "Fellow Note\nPatient: Amy Campbell\nTarget: Lingula Nodule\nSteps:\n1. GA/ETT.\n2. Ion Nav to LB5.\n3. rEBUS (concentric) + CBCT confirmation.\n4. TBNA: x3 passes.\n5. BAL: 80cc instilled.\n6. ROSE: Atypical/Suspicious.\nNo complications.",
            5: "Amy Campbell procedure note. Lingula nodule 17mm. General anesthesia. Ion robot used to get to inferior lingula LB5. Concentric view on rebus and confirmed with spin ct. Did 3 needle passes and a lavage. Rose said suspicious for malignancy. Patient woke up fine.",
            6: "Amy Campbell. Ion Bronchoscopy. Lingula Nodule (17mm). Nav to LB5. rEBUS: Concentric. CBCT: Confirmed. Samples: 3x TBNA, BAL. ROSE: Suspicious for malignancy. Disposition: Stable.",
            7: "[Indication]\nSuspected lung malignancy, Lingula.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB5. rEBUS concentric + CBCT. Sampled via TBNA (x3), BAL. ROSE: Suspicious.\n[Plan]\nDischarge.",
            8: "Ms. Campbell underwent a robotic bronchoscopy for a 17mm nodule in the Lingula. We navigated the Ion catheter to the Inferior Lingula segment. We confirmed the location with a concentric radial EBUS view and Cone Beam CT. We collected three needle aspirates and performed a bronchoalveolar lavage. The on-site evaluation showed atypical cells suspicious for malignancy.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: Lingula nodule.\nTechnique: Steered Ion catheter to LB5. Verified with rEBUS and CBCT. Aspirated with needles (3x). Lavaged. ROSE Result: Suspicious. Patient stable."
        },
        6: { # Sarah Martin (Lingula Nodule, Ion, TBNA/Fiducial, Malignant)
            1: "Procedure: Ion Bronchoscopy Lingula.\n- Target: 18mm nodule Inferior Lingula (LB5).\n- Nav: Ion, 3.1mm error.\n- Verify: rEBUS (adjacent).\n- Samples: 23G TBNA x4.\n- Marker: 1 fiducial placed.\n- ROSE: Malignant (Adenocarcinoma).\n- Outcome: Stable.",
            2: "PROCEDURE NOTE: Ms. Martin underwent robotic bronchoscopy for an 18mm Lingula ground glass opacity. Navigation to the Inferior Lingula (LB5) was achieved via the Ion platform. Radial EBUS showed an adjacent view. The catheter was locked, and 4 transbronchial needle aspirations were performed with a 23G needle. A single gold fiducial marker was placed under fluoroscopic guidance. ROSE confirmed adenocarcinoma. No complications occurred.",
            3: "Coding:\n31629: TBNA x4 (23G).\n31626: Fiducial placement (1 marker).\n31627: Ion Navigation.\n31654: rEBUS.\nSite: Lingula (LB5). Result: Malignancy confirmed.",
            4: "Resident Note\nPatient: Sarah Martin\nTarget: Lingula Nodule\nSteps:\n1. GA/ETT.\n2. Ion Nav to LB5.\n3. rEBUS (adjacent).\n4. TBNA: 23G x 4 passes.\n5. Fiducial placement: x1.\n6. ROSE: Malignant/Adenocarcinoma.\nNo complications.",
            5: "Sarah Martin procedure note. Lingula nodule 18mm. General anesthesia. Ion robot used to get to inferior lingula LB5. Adjacent view on rebus. Did 4 needle passes 23g. Put in a fiducial marker too. Rose said malignant adenocarcinoma. Patient fine.",
            6: "Sarah Martin. Ion Bronchoscopy. Lingula Nodule (18mm). Nav to LB5. rEBUS: Adjacent. Samples: 4x 23G TBNA. Marker: 1 fiducial. ROSE: Malignant (Adenocarcinoma). Disposition: Stable.",
            7: "[Indication]\nGround glass opacity Lingula.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB5. rEBUS adjacent. Sampled via 23G TBNA (x4). Placed 1 fiducial. ROSE: Adenocarcinoma.\n[Plan]\nDischarge.",
            8: "Ms. Martin underwent a robotic bronchoscopy for an 18mm nodule in the Lingula. We navigated the Ion catheter to the Inferior Lingula segment. We confirmed the location with an adjacent radial EBUS view. We collected four needle aspirates using a 23G needle and placed one fiducial marker. The on-site evaluation confirmed malignant cells consistent with adenocarcinoma.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: Lingula nodule.\nTechnique: Guided Ion catheter to LB5. Verified with rEBUS. Aspirated with 23G needle (4x). Implanted fiducial. ROSE Result: Malignant. Patient stable."
        },
        7: { # Matthew Young (LUL Nodule, Ion, TBNA/Cryo/Fiducial/BAL, Malignant)
            1: "Procedure: Ion Bronchoscopy LUL.\n- Target: 27mm nodule Apicoposterior (LB1+2).\n- Nav: Ion, 2.0mm error.\n- Verify: rEBUS (concentric), CBCT.\n- Samples: 21G/23G TBNA x7, 1.7mm Cryo x6 (7s), BAL.\n- Marker: 1 fiducial placed.\n- ROSE: Malignant (Squamous Cell).\n- Outcome: Stable.",
            2: "OPERATIVE REPORT: Mr. Young presented for biopsy of a 27mm LUL nodule. The Ion robotic platform was used to navigate to the Apicoposterior Segment (LB1+2). Localization was confirmed with concentric rEBUS and Cone Beam CT 3D reconstruction. Sampling included 7 needle passes (21G/23G), 6 cryobiopsies (1.7mm probe, 7-second freeze), and BAL. A gold fiducial marker was deployed for future localization. ROSE confirmed squamous cell carcinoma. The patient tolerated the procedure well.",
            3: "CPT Data:\n31629: TBNA x7.\n31628: Cryo x6 (1.7mm).\n31626: Fiducial placement.\n31624: BAL.\n31627: Ion Navigation.\n31654: rEBUS.\nSite: LUL (LB1+2). Result: Squamous Cell Carcinoma.",
            4: "Fellow Note\nPatient: Matthew Young\nTarget: LUL Nodule\nSteps:\n1. GA/ETT.\n2. Ion Nav to LB1+2.\n3. rEBUS (concentric) + CBCT confirmation.\n4. TBNA: x7 passes.\n5. Cryo: x6 biopsies (1.7mm).\n6. Fiducial placement: x1.\n7. BAL: 60cc instilled.\n8. ROSE: Malignant/Squamous Cell.\nNo complications.",
            5: "Matthew Young procedure note. LUL nodule 27mm. General anesthesia. Ion robot used to get to apicoposterior segment. Concentric view on rebus and confirmed with spin ct. Did 7 needle passes and 6 cryo biopsies. Put in a fiducial marker and did a lavage. Rose said squamous cell carcinoma. Patient woke up fine.",
            6: "Matthew Young. Ion Bronchoscopy. LUL Nodule (27mm). Nav to LB1+2. rEBUS: Concentric. CBCT: Confirmed. Samples: 7x TBNA, 6x 1.7mm Cryo, BAL. Marker: 1 fiducial. ROSE: Malignant (Squamous Cell). Disposition: Stable.",
            7: "[Indication]\nSuspected lung malignancy, LUL.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB1+2. rEBUS concentric + CBCT. Sampled via TBNA (x7), Cryo (x6), BAL. Placed 1 fiducial. ROSE: Squamous Cell Carcinoma.\n[Plan]\nDischarge.",
            8: "Mr. Young underwent a robotic bronchoscopy for a 27mm nodule in the Left Upper Lobe. We navigated the Ion catheter to the Apicoposterior Segment. We confirmed the location with a concentric radial EBUS view and Cone Beam CT. We collected seven needle aspirates, six cryobiopsies, and performed a bronchoalveolar lavage. We also placed one fiducial marker. The on-site evaluation confirmed squamous cell carcinoma.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: LUL nodule.\nTechnique: Steered Ion catheter to LB1+2. Verified with rEBUS and CBCT. Aspirated with needles (7x). Biopsied with 1.7mm cryoprobe (6x). Lavaged. Implanted fiducial. ROSE Result: Malignant. Patient stable."
        },
        8: { # Laura Carter (LLL Nodule, Ion, TBNA/Cryo/Brush/BAL, Benign)
            1: "Procedure: Ion Bronchoscopy LLL.\n- Target: 21mm nodule Posterior-Basal (LB10).\n- Nav: Ion, 1.9mm error.\n- Verify: rEBUS (eccentric), CBCT.\n- Samples: 23G TBNA x6, 1.7mm Cryo x3 (5s), Brush x2, BAL.\n- ROSE: Benign lymphocytes.\n- Outcome: Stable.",
            2: "PROCEDURE NOTE: Ms. Carter underwent robotic bronchoscopy for a 21mm LLL nodule. Navigation to the Posterior-Basal Segment (LB10) was achieved using the Ion platform. Confirmation via eccentric rEBUS and Cone Beam CT was obtained. Sampling consisted of 6 passes with a 23G needle, 3 cryobiopsies (1.7mm probe, 5-second freeze), 2 brushings, and BAL. ROSE identified benign lymphocytes. No complications occurred.",
            3: "Billing Codes:\n31629: TBNA x6 (23G).\n31628: Cryo x3 (1.7mm).\n31624: BAL.\n31623: Brush x2.\n31627: Ion Navigation.\n31654: rEBUS.\nSite: LLL (LB10). Verification: CBCT/REBUS. Result: Benign.",
            4: "Resident Note\nPatient: Laura Carter\nTarget: LLL Nodule\nSteps:\n1. GA/ETT.\n2. Ion Nav to LB10.\n3. rEBUS (eccentric) + CBCT confirmation.\n4. TBNA: 23G x 6 passes.\n5. Cryo: 1.7mm x 3 biopsies.\n6. Brush: x 2.\n7. BAL: 80cc instilled.\n8. ROSE: Benign lymphocytes.\nNo complications.",
            5: "Laura Carter procedure note. LLL nodule 21mm. General anesthesia. Ion robot used to get to posterior basal segment. Eccentric view on rebus and confirmed with spin ct. Did 6 needle passes 23g 3 cryo and 2 brushes plus a lavage. Rose said benign lymphocytes. Patient fine.",
            6: "Laura Carter. Ion Bronchoscopy. LLL Nodule (21mm). Nav to LB10. rEBUS: Eccentric. CBCT: Confirmed. Samples: 6x 23G TBNA, 3x 1.7mm Cryo, 2x Brush, BAL. ROSE: Benign. Disposition: Stable.",
            7: "[Indication]\nLung-RADS 4X nodule, LLL.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB10. rEBUS eccentric + CBCT. Sampled via 23G TBNA (x6), 1.7mm Cryo (x3), Brush (x2), BAL. ROSE: Benign.\n[Plan]\nDischarge.",
            8: "Ms. Carter underwent a robotic bronchoscopy for a 21mm nodule in the Left Lower Lobe. We navigated the Ion catheter to the Posterior-Basal Segment. We confirmed the location with an eccentric radial EBUS view and Cone Beam CT. We collected six needle aspirates, three cryobiopsies, two brush samples, and performed a bronchoalveolar lavage. The on-site evaluation showed benign lymphocytes.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: LLL nodule.\nTechnique: Directed Ion catheter to LB10. Verified with rEBUS and CBCT. Aspirated with 23G needle (6x). Biopsied with 1.7mm cryoprobe (3x). Brushed (2x). Lavaged. ROSE Result: Benign. Patient stable."
        },
        9: { # Ashley Williams (RUL Nodule, Ion, TBNA/Cryo/BAL, Granulomatous)
            1: "Procedure: Ion Bronchoscopy RUL.\n- Target: 27mm nodule Anterior Segment (RB3).\n- Nav: Ion, 2.4mm error.\n- Verify: rEBUS (eccentric), CBCT.\n- Samples: 21G/23G TBNA x8, 1.1mm Cryo x5 (5s), BAL.\n- ROSE: Granulomatous inflammation.\n- Outcome: Stable.",
            2: "OPERATIVE SUMMARY: Ms. Williams presented for biopsy of a 27mm RUL nodule. The Ion robotic platform was used to navigate to the Anterior Segment (RB3). Localization was confirmed with eccentric rEBUS and Cone Beam CT 3D reconstruction. Sampling included 8 needle passes (21G/23G), 5 cryobiopsies using a 1.1mm probe, and a bronchoalveolar lavage. ROSE results indicated granulomatous inflammation. The procedure was uncomplicated.",
            3: "CPT Justification:\n31629: TBNA x8 (21G/23G).\n31628: Cryo x5 (1.1mm).\n31624: BAL.\n31627: Ion Navigation.\n31654: rEBUS.\nSite: RUL (RB3). Verification: CBCT/REBUS. Result: Granulomatous inflammation.",
            4: "Fellow Note\nPatient: Ashley Williams\nTarget: RUL Nodule\nSteps:\n1. GA/ETT.\n2. Ion Nav to RB3.\n3. rEBUS (eccentric) + CBCT confirmation.\n4. TBNA: x8 passes.\n5. Cryo: 1.1mm x 5 biopsies.\n6. BAL: 40cc instilled.\n7. ROSE: Granulomatous inflammation.\nNo complications.",
            5: "Ashley Williams procedure note. RUL nodule 27mm. General anesthesia. Ion robot used to get to anterior segment. Eccentric view on rebus and confirmed with spin ct. Did 8 needle passes and 5 cryo biopsies plus a lavage. Rose said granulomas. Patient woke up fine.",
            6: "Ashley Williams. Ion Bronchoscopy. RUL Nodule (27mm). Nav to RB3. rEBUS: Eccentric. CBCT: Confirmed. Samples: 8x TBNA, 5x 1.1mm Cryo, BAL. ROSE: Granulomatous inflammation. Disposition: Stable.",
            7: "[Indication]\nSuspicious nodule RUL.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to RB3. rEBUS eccentric + CBCT. Sampled via TBNA (x8), Cryo (x5), BAL. ROSE: Granulomatous inflammation.\n[Plan]\nDischarge.",
            8: "Ms. Williams underwent a robotic bronchoscopy for a 27mm nodule in the Right Upper Lobe. We navigated the Ion catheter to the Anterior Segment. We confirmed the location with an eccentric radial EBUS view and Cone Beam CT. We collected eight needle aspirates, five cryobiopsies using a 1.1mm probe, and performed a bronchoalveolar lavage. The on-site evaluation showed granulomatous inflammation.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: RUL nodule.\nTechnique: Guided Ion catheter to RB3. Verified with rEBUS and CBCT. Aspirated with needles (8x). Biopsied with 1.1mm cryoprobe (5x). Lavaged. ROSE Result: Granulomatous. Patient stable."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns list of mocks for names and ages. 
    Indices correspond to the note order in the source JSON.
    """
    return [
        {"idx": 0, "orig_name": "Mary Mitchell", "orig_age": 67, "names": ["Linda Johnson", "Patricia Brown", "Barbara Davis", "Elizabeth Miller", "Jennifer Wilson", "Maria Moore", "Susan Taylor", "Margaret Anderson", "Dorothy Thomas"]},
        {"idx": 1, "orig_name": "Dorothy White", "orig_age": 66, "names": ["Lisa Jackson", "Nancy White", "Karen Harris", "Betty Martin", "Helen Thompson", "Sandra Garcia", "Donna Martinez", "Carol Robinson", "Ruth Clark"]},
        {"idx": 2, "orig_name": "Kevin Jackson", "orig_age": 51, "names": ["James Rodriguez", "John Lewis", "Robert Lee", "Michael Walker", "William Hall", "David Allen", "Richard Young", "Charles Hernandez", "Joseph King"]},
        {"idx": 3, "orig_name": "Charles Baker", "orig_age": 78, "names": ["Thomas Wright", "Christopher Lopez", "Daniel Hill", "Paul Scott", "Mark Green", "Donald Adams", "George Baker", "Kenneth Gonzalez", "Steven Nelson"]},
        {"idx": 4, "orig_name": "Kimberly Garcia", "orig_age": 70, "names": ["Sharon Carter", "Michelle Mitchell", "Laura Perez", "Sarah Roberts", "Kimberly Turner", "Deborah Phillips", "Jessica Campbell", "Shirley Parker", "Cynthia Evans"]},
        {"idx": 5, "orig_name": "Amy Campbell", "orig_age": 67, "names": ["Angela Edwards", "Melissa Collins", "Brenda Stewart", "Amy Sanchez", "Anna Morris", "Rebecca Rogers", "Virginia Reed", "Kathleen Cook", "Pamela Morgan"]},
        {"idx": 6, "orig_name": "Sarah Martin", "orig_age": 52, "names": ["Martha Bell", "Debra Murphy", "Amanda Bailey", "Stephanie Rivera", "Carolyn Cooper", "Christine Richardson", "Marie Cox", "Janet Howard", "Catherine Ward"]},
        {"idx": 7, "orig_name": "Matthew Young", "orig_age": 73, "names": ["Edward Torres", "Brian Peterson", "Ronald Gray", "Anthony Ramirez", "Kevin James", "Jason Watson", "Matthew Brooks", "Gary Kelly", "Timothy Sanders"]},
        {"idx": 8, "orig_name": "Laura Carter", "orig_age": 59, "names": ["Diane Price", "Alice Bennett", "Julie Wood", "Heather Barnes", "Teresa Ross", "Doris Henderson", "Gloria Coleman", "Evelyn Jenkins", "Jean Perry"]},
        {"idx": 9, "orig_name": "Ashley Williams", "orig_age": 79, "names": ["Joyce Powell", "Judith Long", "Rosed Patterson", "Beverly Hughes", "Denise Flores", "Marilyn Washington", "Amber Butler", "Danielle Simmons", "Brittany Foster"]}
    ]

def main():
    # Load original data
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file '{SOURCE_FILE}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        return

    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Verify input data alignment
    if len(source_data) > len(base_data):
        print("Warning: Source data has more entries than base mock data. Extra entries will be skipped.")
    
    generated_notes = []
    
    # Process each note
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Generate 9 variations
        for style_num in range(1, 10):
            # Deep copy to avoid modifying original
            note_entry = copy.deepcopy(original_note)
            
            # Generate synthetic demographics
            new_age = orig_age + random.randint(-3, 3)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            new_name = record['names'][style_num - 1]
            
            # Apply text variation
            # Use safety check in case dictionary is missing a specific index
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                note_entry["note_text"] = f"Error: Missing variation text for Note {idx}, Style {style_num}"

            # Update Registry Entry fields
            if "registry_entry" in note_entry:
                reg = note_entry["registry_entry"]
                if "patient_age" in reg:
                    reg["patient_age"] = new_age
                if "procedure_date" in reg:
                    reg["procedure_date"] = rand_date_str
                if "patient_mrn" in reg:
                    reg["patient_mrn"] = f"{reg['patient_mrn']}_syn_{style_num}"
            
            # Add Synthetic Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Save output
    output_path = Path(OUTPUT_DIR) / OUTPUT_FILENAME
    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in '{output_path}'")

if __name__ == "__main__":
    main()