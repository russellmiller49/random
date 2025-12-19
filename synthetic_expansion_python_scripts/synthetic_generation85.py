import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (The file you uploaded)
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_085.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the crafted text variations for Part 085 (Galaxy/Robotic Bronchoscopy).
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Jessica Flores (Lingula, TBNA/Bx/Brush, TiLT+)
            1: "Indication: Lung-RADS 4B nodule, Lingula.\nAnesthesia: GA, ETT.\nDevice: Noah Galaxy.\nAction: Navigated to LB4. TiLT+ sweep showed 1.8cm divergence. Adjusted. Confirmed via rEBUS (adjacent).\nSampling:\n- TBNA 22G: 5 passes.\n- Forceps: 4 samples.\n- Brush: 1 sample.\nROSE: SqCC.\nPlan: Recovery. CXR.",
            2: "OPERATIVE REPORT: The patient was brought to the endoscopy suite for investigation of a Lingular nodule. Following the induction of general anesthesia, the Noah Galaxy robotic platform was deployed. Initial registration yielded a 2.1mm accuracy. Intraprocedural Tool-in-Lesion Tomosynthesis (TiLT+) identified a significant divergence of 1.8cm, likely secondary to positioning. The target was realigned utilizing augmented fluoroscopy. Radial EBUS confirmed an adjacent signature. Extensive sampling was performed via transbronchial needle aspiration and forceps biopsy. Rapid On-Site Evaluation was positive for malignant cells consistent with squamous cell carcinoma.",
            3: "Procedure Codes Justification:\n- 31629 (TBNA): Performed on Lingula lesion using 22G needle.\n- 31623 (Brush): Cytology brushing performed on same site.\n- 31627 (Navigational Bronchoscopy): Galaxy robotic system used for guidance.\n- 31654 (rEBUS): Radial probe used for localization.\nNote: TiLT+ tomosynthesis was utilized for divergence correction (1.8cm).",
            4: "Resident Procedure Note\nPatient: J. Flores\nAttending: Dr. Wilson\nProcedure: Robotic Bronchoscopy (Galaxy)\nSteps:\n1. ETT placed.\n2. Galaxy registered (2.1mm error).\n3. TiLT+ sweep done; found 1.8cm divergence.\n4. Adjusted to new target.\n5. rEBUS: Adjacent.\n6. Biopsied: TBNA x5, Forceps x4, Brush.\n7. ROSE positive for SqCC.\nNo complications.",
            5: "patient jessica flores here for lung nodule biopsy used the galaxy robot today under general anesthesia tube was fine. navigated to the lingula lb4 registered ok. did the tilt spin and saw the nodule was way off like 1.8cm so we fixed that on the screen. confirmed with rebus then did tbna forceps and brush rose came back squamous cell so we stopped. patient woke up ok sending to recovery thanks.",
            6: "Lung-RADS 4B nodule. 26mm nodule in Lingula. General anesthesia. Noah Galaxy bronchoscope introduced. Navigational registration performed. Scope navigated to LB4. Tool-in-Lesion Tomosynthesis (TiLT+) sweep performed. 1.8cm divergence noted and corrected. Radial EBUS view: Adjacent. Transbronchial needle aspiration (22G, 5 passes). Transbronchial forceps biopsy (4 specimens). Cytology brushings. ROSE Result: Malignant cells identified, consistent with squamous cell carcinoma. No complications.",
            7: "[Indication]\nLung-RADS 4B nodule (26mm, Lingula).\n[Anesthesia]\nGeneral, ETT.\n[Description]\nGalaxy robotic scope used. Registration error 2.1mm. TiLT+ identified 1.8cm divergence; target updated. rEBUS: Adjacent. Sampling: TBNA (5 passes), Forceps (4 samples), Brush.\n[Plan]\nResults conference 5-7 days. CXR.",
            8: "Ms. Flores presented for biopsy of a 26mm Lingular nodule. We utilized the Noah Galaxy robotic system. After intubation, we navigated to the target but noted a 1.8cm divergence on the TiLT+ spin, which we corrected. We confirmed the location with rEBUS and proceeded to sample the lesion using a needle, forceps, and brush. The on-site pathologist confirmed squamous cell carcinoma.",
            9: "Context: Lung-RADS 4B mass.\nTechnique: The Galaxy scope was piloted to the Lingula. A TiLT+ scan exposed a 1.8cm deviation, which was rectified. The lesion was localized via rEBUS. We aspirated the site with a 22G needle, harvested tissue with forceps, and brushed the area.\nResult: ROSE indicated squamous cell carcinoma."
        },
        1: { # Linda White (LLL, TBNA/Brush, TiLT+)
            1: "Target: 11mm LLL nodule.\nSystem: Galaxy Robot.\nNav: Reg error 3.5mm. TiLT+ showed 1.3cm divergence (atelectasis).\nAction: Re-aligned. rEBUS adjacent.\nSampling: TBNA (5 passes), Brush.\nROSE: Granulomatous inflammation.\nComp: None.",
            2: "PROCEDURE NARRATIVE: The subject, with a history of malignancy, presented for evaluation of an 11mm LLL nodule. Under general anesthesia, the Galaxy robotic bronchoscope was advanced to the LB7+8 segment. Intraoperative tomosynthesis (TiLT) revealed a 1.3cm target divergence attributable to atelectasis. Following virtual target update, tool position was verified. Sampling via 22G TBNA and cytology brush yielded granulomatous inflammation on preliminary review.",
            3: "Billing Summary:\n- Primary: 31629 (TBNA of LLL nodule).\n- Secondary: 31623 (Brush), 31627 (Navigation), 31654 (rEBUS).\n- Complexity: High. Required TiLT+ tomosynthesis to correct 1.3cm divergence caused by atelectasis.\n- Outcome: Successful localization and sampling.",
            4: "Procedure: Robotic Bronch (Galaxy)\nPatient: L. White\nIndication: LLL Nodule\nSteps:\n1. Intubation.\n2. Nav to LLL (LB7+8).\n3. TiLT+ spin -> 1.3cm divergence found.\n4. Updated path.\n5. rEBUS adjacent.\n6. TBNA x5, Brush x1.\n7. ROSE: Granulomas.\nPlan: Discharge if CXR clear.",
            5: "linda white 11mm nodule lll. galaxy robot used. registration was a bit loose 3.5mm. did the tilt scan and found the nodule moved 1.3cm probably atelectasis. adjusted and got it with rebus adjacent view. tbna needle and brush used. rose said granulomas so hopefully benign. patient did fine no bleeding.",
            6: "Pulmonary nodule in patient with prior malignancy. 11mm nodule in LLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to LB7+8. TiLT+ sweep revealed 1.3cm divergence due to atelectasis. Target updated. rEBUS view: Adjacent. Transbronchial needle aspiration (22G, 5 passes). Cytology brushings. ROSE Result: Granulomatous inflammation. Disposition: Recovery.",
            7: "[Indication]\n11mm nodule LLL, prior malignancy.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy robot navigated to LB7+8. TiLT+ used to correct 1.3cm divergence. rEBUS adjacent. TBNA and Brush performed.\n[Plan]\nFollow-up pathology.",
            8: "Mrs. White underwent robotic bronchoscopy for her LLL nodule today. Using the Galaxy system, we navigated to the lower lobe. We performed a TiLT+ spin which showed the nodule had shifted by 1.3cm due to atelectasis. We adjusted our targeting, confirmed with ultrasound, and took samples using a needle and brush. Preliminary results suggest granulomatous inflammation.",
            9: "Operation: Robotic-assisted bronchoscopy.\nTarget: LLL mass.\nDetails: The Galaxy scope was steered to the target. TiLT+ imaging uncovered a 1.3cm shift. We realigned the virtual target. The site was sampled via needle aspiration and brushing.\nFinding: Granulomas on ROSE."
        },
        2: { # Elizabeth Lewis (RLL, TBNA/Bx/Brush/Fiducial, TiLT+)
            1: "Indication: RLL nodule (Brock high risk).\nTools: Galaxy, TiLT+, 22G Needle, Forceps, Fiducial.\nNav: 1.7cm divergence found on TiLT. Corrected.\nActions: rEBUS concentric. TBNA x7. Forceps x4. Brush. Gold fiducial placed.\nROSE: Suspicious for malignancy.",
            2: "PROCEDURE: The patient was intubated for robotic bronchoscopy targeting a 9mm RLL nodule. The Galaxy system was utilized. Registration was performed (3.8mm error). Crucially, a TiLT+ spin demonstrated 1.7cm of target divergence. The virtual target was updated to match reality. rEBUS showed a concentric view. We performed TBNA, forceps biopsies, and brushing. A gold fiducial marker was deployed under TiLT-augmented fluoroscopy for future SBRT.",
            3: "CPT Coding:\n- 31626: Placement of fiducial markers (SBRT planning).\n- 31629: TBNA.\n- 31623: Brush.\n- 31627: Navigation (Galaxy).\n- 31654: rEBUS.\nNote: TiLT+ used to verify tool-in-lesion.",
            4: "Resident Note\nPt: E. Lewis\nCase: RLL Nodule Biopsy + Fiducial\n1. GA/ETT.\n2. Nav to RB6.\n3. TiLT showed 1.7cm divergence (atelectasis).\n4. Adjusted.\n5. rEBUS concentric (good view).\n6. Samples: TBNA, Bx, Brush.\n7. Dropped 1 fiducial.\n8. ROSE: Suspicious.",
            5: "elizabeth lewis here for rll nodule biopsy and marker placement. galaxy robot used. pretty big divergence on the tilt spin 1.7cm so good thing we checked. fixed it. concentric view on ultrasound. did 7 needle passes 4 bites and a brush. put a gold marker in for radiation. rose looks suspicious for cancer.",
            6: "Suspicious nodule with high Brock score. 9mm nodule in RLL. General anesthesia. Galaxy robotic platform. Navigated to RB6. TiLT+ sweep generated updated 3D volume showing 1.7cm divergence. Target updated. rEBUS: Concentric. TBNA (22G), Forceps biopsy, Brush. Gold fiducial marker placed. ROSE: Suspicious for malignancy.",
            7: "[Indication]\n9mm RLL nodule, high risk.\n[Anesthesia]\nGA.\n[Description]\nGalaxy nav to RB6. TiLT+ corrected 1.7cm divergence. rEBUS Concentric. TBNA, Bx, Brush done. Fiducial placed.\n[Plan]\nOncology referral pending final path.",
            8: "We performed a robotic biopsy on Mrs. Lewis's right lower lobe nodule. The Galaxy system helped us navigate, and the TiLT+ feature was essential as it showed the nodule was 1.7cm away from the expected spot due to atelectasis. Once corrected, we got a concentric ultrasound view. We took multiple samples and placed a gold marker for future radiation therapy.",
            9: "Procedure: Robotic navigation and sampling.\nLesion: 9mm RLL.\nCorrection: TiLT+ detected a 1.7cm drift; we compensated.\nSampling: Needle aspiration, forceps extraction, and brushing were executed. A fiducial was implanted.\nOutcome: ROSE suspicious."
        },
        3: { # Shirley Walker (LUL, TBNA/Bx/Brush/Fiducial, TiLT+)
            1: "Dx: Lung-RADS 4X, 22mm LUL.\nMethod: Galaxy Robot + TiLT+.\nFindings: 1.5cm divergence on TiLT. Corrected.\nrEBUS: Eccentric.\n intervention: TBNA x5, Forceps x7, Brush, Fiducial.\nROSE: Lymphocytes/benign.",
            2: "OPERATIVE SUMMARY: Ms. Walker presented for biopsy of a 22mm LUL nodule. Under GA, the Galaxy bronchoscope was navigated to LB1+2. Intra-operative TiLT+ tomosynthesis revealed a 1.5cm divergence secondary to respiratory motion. Following target update, an eccentric rEBUS view was obtained. Diagnostic sampling included TBNA, forceps biopsy, and brushing. A fiducial marker was placed to facilitate SBRT if needed. ROSE cytology showed benign lymphocytes.",
            3: "Code Selection:\n31626 (Marker), 31629 (TBNA), 31623 (Brush). Add-ons: 31627 (Nav), 31654 (rEBUS).\nMedical Necessity: 4X nodule requiring diagnosis and marking.\nTech: Galaxy robot with TiLT+ used to correct 1.5cm divergence.",
            4: "Resident Note\nPatient: S. Walker, 82F\nTarget: LUL 22mm\nSteps:\n1. Galaxy nav to LB1+2.\n2. TiLT+ showed 1.5cm divergence.\n3. Re-aligned.\n4. rEBUS eccentric.\n5. Samples: Needle, Forceps, Brush.\n6. Fiducial placed.\nROSE: Benign so far.",
            5: "shirley walker 82 year old female lul nodule. used the galaxy system. tilt scan showed we were off by 1.5cm cause of breathing motion. fixed it. eccentric view on the radar. took a bunch of samples needle and forceps and brush. put a marker in just in case. rose says benign lymphocytes.",
            6: "Lung-RADS 4X nodule. 22mm nodule in LUL. General anesthesia. Noah Galaxy bronchoscope. Navigated to LB1+2. TiLT+ sweep revealed 1.5cm divergence. Target updated. rEBUS view: Eccentric. TBNA performed. Transbronchial forceps biopsy performed. Cytology brushings obtained. Gold fiducial marker placed. ROSE Result: Lymphocytes and benign cells.",
            7: "[Indication]\n22mm LUL nodule (4X).\n[Anesthesia]\nGA.\n[Description]\nGalaxy nav. TiLT+ corrected 1.5cm divergence. rEBUS eccentric. TBNA, Bx, Brush. Fiducial placed.\n[Plan]\nWait for final path.",
            8: "Ms. Walker underwent a robotic biopsy of her left upper lobe nodule. Using the Galaxy system and TiLT+ technology, we identified and corrected a 1.5cm discrepancy in the target location caused by breathing. We obtained samples using a needle, forceps, and brush, and placed a fiducial marker. Preliminary results show benign cells.",
            9: "Task: Robotic biopsy LUL.\nDetail: Galaxy system used. TiLT+ rectified a 1.5cm divergence. rEBUS confirmed location (eccentric). We aspirated, biopsied, and brushed the lesion. A fiducial was deposited.\nPathology: ROSE showed lymphocytes."
        },
        4: { # Rebecca White (RLL, TBNA/Brush, TiLT+)
            1: "Indication: Multiple nodules, dominant RLL 25mm.\nRobot: Galaxy.\nTiLT+: 1.5cm divergence (respiratory motion). Corrected.\nrEBUS: Adjacent.\nAction: TBNA x5, Brush.\nROSE: Negative for malignancy.",
            2: "PROCEDURE NOTE: The patient underwent robotic bronchoscopy for a dominant 25mm RLL nodule. The Galaxy system was employed. Navigation to RB9 was successful, though TiLT+ imaging revealed a 1.5cm divergence requiring adjustment. Verification was achieved via adjacent rEBUS signal. TBNA and brushing were performed. Rapid on-site evaluation showed no evidence of malignancy.",
            3: "Billing: 31629 (TBNA), 31623 (Brush), 31627 (Galaxy Nav), 31654 (rEBUS).\nNote: TiLT+ utilized for intra-operative target correction (1.5cm divergence).",
            4: "Procedure: Galaxy RLL Biopsy\nPt: R. White\nTarget: 25mm RLL\n1. Nav to RB9.\n2. TiLT spin -> 1.5cm divergence.\n3. Updated target.\n4. rEBUS adjacent.\n5. Needle x5, Brush x1.\n6. ROSE negative.",
            5: "rebecca white here for rll nodule biopsy. galaxy robot. navigated down to rb9. tilt showed we were 1.5cm off cause she was breathing deep. adjusted. adjacent view on ultrasound. five passes with the needle and a brush. rose said no cancer seen.",
            6: "Multiple pulmonary nodules. 25mm nodule in RLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB9. TiLT+ sweep revealed 1.5cm divergence due to respiratory motion. Augmented reality target updated. rEBUS view: Adjacent. Transbronchial needle aspiration (22G). Cytology brushings. ROSE Result: No evidence of malignant neoplasm.",
            7: "[Indication]\nDominant RLL nodule 25mm.\n[Anesthesia]\nGA.\n[Description]\nGalaxy nav. TiLT+ corrected 1.5cm error. rEBUS adjacent. TBNA and Brush performed.\n[Plan]\nFollow-up in 1 week.",
            8: "Mrs. White had a robotic biopsy of her right lower lobe nodule. We used the Galaxy system. The TiLT+ scan showed the target had moved 1.5cm due to breathing, so we updated our navigation. We confirmed the spot with ultrasound and took needle and brush samples. The preliminary check didn't show cancer.",
            9: "Procedure: Robotic sampling RLL.\nCorrection: TiLT+ offset of 1.5cm noted and fixed.\nTools: Galaxy scope, 22G needle, brush.\nOutcome: ROSE negative for malignancy."
        },
        5: { # Ronald Green (RML, TBNA/Bx/Brush, Fluoroscopy only - No TiLT divergence mentioned?)
            # Wait, Note 6 in source says "Fluoroscopic guidance used... Navigation alignment confirmed."
            # It does NOT mention TiLT+ divergence like the others. It says "Registration accuracy: 2.1mm"
            1: "Target: 31mm RML nodule.\nNav: Galaxy (2.1mm accuracy).\nCheck: Fluoro + rEBUS (Concentric).\nAction: TBNA x6, Forceps x4, Brush.\nROSE: Atypical cells.",
            2: "OPERATIVE REPORT: Mr. Green presented for biopsy of a PET-avid RML nodule. The Galaxy robotic system was navigated to RB4. Registration error was 2.1mm. Position was confirmed via fluoroscopy and concentric rEBUS view. Sampling proceeded with 21G TBNA, forceps biopsy, and brushing. ROSE indicated atypical cells, malignancy not excluded.",
            3: "Codes: 31629, 31623, 31627, 31654.\nTechnique: Electromagnetic navigation (Galaxy) with fluoroscopic and rEBUS confirmation. No TiLT divergence noted.",
            4: "Resident Note\nPt: R. Green\nSite: RML (RB4)\n1. Galaxy Nav.\n2. Fluoro check good.\n3. rEBUS concentric.\n4. TBNA x6, Bx x4, Brush.\n5. ROSE: Atypical.\nPlan: Wait for final path.",
            5: "ronald green rml nodule 31mm. used the galaxy robot. registration was good 2.1mm. verified with fluoro and concentric rebus. did needle forceps and brush. rose was atypical cells could be cancer. patient discharged ok.",
            6: "PET-avid lung nodule. 31mm nodule in RML. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB4. Registration accuracy: 2.1mm. Fluoroscopic guidance used to confirm scope position. rEBUS view: Concentric. Transbronchial needle aspiration (21G). Transbronchial forceps biopsy. Cytology brushings. ROSE Result: Atypical cells.",
            7: "[Indication]\nPET-avid RML nodule.\n[Anesthesia]\nGA.\n[Description]\nGalaxy nav to RB4. Fluoro confirmed. rEBUS concentric. TBNA, Bx, Brush done.\n[Plan]\nPathology pending.",
            8: "Mr. Green underwent a robotic biopsy of his right middle lobe nodule. We used the Galaxy system and achieved good registration accuracy. We confirmed our position with fluoroscopy and ultrasound, which showed a concentric view. We took multiple samples. The initial pathology showed atypical cells.",
            9: "Procedure: Robotic RML biopsy.\nTools: Galaxy, 21G needle, forceps, brush.\nVerification: Fluoroscopy and rEBUS (concentric).\nResult: Atypical cells on ROSE."
        },
        6: { # Michael Taylor (RUL, TBNA/Bx/Brush, Fluoro only)
            1: "Indication: 24mm RUL nodule.\nSystem: Galaxy Robot.\nVerif: Fluoro + rEBUS (Adjacent).\nSampling: TBNA x6, Forceps x4, Brush.\nROSE: Granulomatous.",
            2: "PROCEDURE: Evaluation of a 24mm RUL nodule was performed using the Noah Galaxy robotic platform. Navigation to RB2 was achieved with 3.2mm accuracy. Fluoroscopy confirmed alignment. rEBUS demonstrated an adjacent lesion signature. TBNA and forceps biopsies were obtained, along with brushings. ROSE suggested granulomatous inflammation.",
            3: "Billing: 31629 (TBNA), 31623 (Brush), 31627 (Nav), 31654 (rEBUS).\nTarget: RUL (RB2).\nMethod: Robotic navigation with fluoroscopic confirmation.",
            4: "Resident Note\nPt: M. Taylor\nRUL Nodule\n1. Galaxy nav to RB2.\n2. Fluoro check.\n3. rEBUS adjacent.\n4. TBNA, Bx, Brush.\n5. ROSE: Granulomas.\nStable.",
            5: "michael taylor rul nodule. galaxy robot used. registration 3.2mm. checked with fluoro looks ok. rebus adjacent. did needle and forceps and brush. rose showed granulomas. patient fine.",
            6: "Multiple pulmonary nodules. 24mm nodule in RUL. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB2. Fluoroscopic guidance used. rEBUS view: Adjacent. Transbronchial needle aspiration (21G). Transbronchial forceps biopsy. Cytology brushings. ROSE Result: Granulomatous inflammation.",
            7: "[Indication]\nRUL nodule.\n[Anesthesia]\nGA.\n[Description]\nGalaxy nav to RB2. Fluoro/rEBUS confirmed. TBNA, Forceps, Brush done.\n[Plan]\nDischarge.",
            8: "Mr. Taylor had a biopsy of his right upper lobe nodule today using the Galaxy robot. We navigated to the site and confirmed with fluoroscopy and ultrasound. We took needle and forceps samples. The preliminary results point towards inflammation (granulomas) rather than cancer.",
            9: "Action: Robotic investigation of RUL mass.\nVerification: Fluoroscopy and rEBUS (adjacent).\nSampling: Aspirated (needle), biopsied (forceps), brushed.\nResult: Granulomatous inflammation."
        },
        7: { # Angela Brown (RLL, TBNA/Bx/Brush/Fiducial, TiLT+)
            1: "Target: 31mm RLL nodule.\nDevice: Galaxy, TiLT+.\nNav: 1.8cm divergence (positioning). Corrected.\nrEBUS: Concentric.\nIntervention: TBNA x6, Bx x5, Brush, Fiducial.\nROSE: Malignant (SqCC).",
            2: "OPERATIVE NOTE: Ms. Brown presented for biopsy of a 31mm RLL nodule. The Galaxy system was used. TiLT+ tomosynthesis revealed a 1.8cm divergence due to patient positioning, which was corrected intra-operatively. rEBUS showed a concentric view. We performed TBNA, forceps biopsy, and brushing. A fiducial was placed for SBRT planning. ROSE confirmed squamous cell carcinoma.",
            3: "Codes: 31626 (Marker), 31629 (TBNA), 31623 (Brush), 31627 (Nav), 31654 (rEBUS).\nNote: High complexity. TiLT+ required to correct 1.8cm positioning divergence.",
            4: "Resident Note\nPt: A. Brown\nRLL Nodule 31mm\n1. Galaxy nav RB9.\n2. TiLT showed 1.8cm error.\n3. Fixed target.\n4. rEBUS concentric.\n5. Samples + Fiducial.\n6. ROSE: Cancer (SqCC).",
            5: "angela brown rll nodule big one 31mm. galaxy robot. tilt spin showed 1.8cm divergence cause of how she was laying. fixed it. concentric ultrasound. six needle passes five forceps bites and a brush. put a marker in. rose is cancer squamous.",
            6: "Peripheral pulmonary nodule. 31mm nodule in RLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB9. TiLT+ sweep revealed 1.8cm divergence. Target updated. rEBUS view: Concentric. TBNA (21G). Transbronchial forceps biopsy. Cytology brushings. Gold fiducial marker placed. ROSE Result: Malignant cells identified, consistent with squamous cell carcinoma.",
            7: "[Indication]\n31mm RLL nodule.\n[Anesthesia]\nGA.\n[Description]\nGalaxy nav. TiLT+ corrected 1.8cm divergence. rEBUS concentric. TBNA, Bx, Brush, Fiducial.\n[Plan]\nOncology.",
            8: "Ms. Brown underwent robotic biopsy of her RLL nodule. The Galaxy system with TiLT+ identified a 1.8cm positioning error which we corrected. We obtained excellent samples and placed a fiducial marker. The preliminary pathology confirms squamous cell carcinoma.",
            9: "Procedure: Robotic RLL biopsy and marking.\nCorrection: 1.8cm divergence fixed via TiLT+.\nSampling: Needle, forceps, brush.\nAddition: Fiducial implanted.\nResult: Squamous cell carcinoma."
        },
        8: { # Susan Gonzalez (RLL, TBNA/Bx/Brush/BAL, Fluoro only)
            1: "Indication: 9mm RLL nodule.\nSystem: Galaxy.\nVerif: Fluoro + rEBUS (Concentric).\nAction: TBNA x4, Bx x6, Brush, BAL (RB10).\nROSE: Negative.",
            2: "PROCEDURE: A 9mm RLL nodule was investigated using the Galaxy robotic scope. Navigation to RB10 was verified with fluoroscopy and a concentric rEBUS view. Diagnostic maneuvers included TBNA, forceps biopsy, brushing, and a bronchoalveolar lavage (BAL) of the target segment. ROSE was negative for malignancy.",
            3: "Codes: 31629 (TBNA), 31624 (BAL), 31623 (Brush), 31627 (Nav), 31654 (rEBUS).\nTarget: RLL (RB10).\nNote: BAL performed for culture/cytology.",
            4: "Resident Note\nPt: S. Gonzalez\nRLL 9mm\n1. Galaxy to RB10.\n2. Fluoro ok.\n3. rEBUS concentric.\n4. TBNA, Bx, Brush.\n5. BAL performed.\n6. ROSE negative.",
            5: "susan gonzalez rll nodule 9mm. galaxy robot. fluoroscopy check good. concentric rebus. did needle forceps brush and a wash bal. rose said no cancer seen.",
            6: "Peripheral pulmonary nodule. 9mm nodule in RLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB10. Fluoroscopic guidance used. rEBUS view: Concentric. TBNA (22G). Transbronchial forceps biopsy. Cytology brushings. Bronchoalveolar lavage performed. ROSE Result: No evidence of malignant neoplasm.",
            7: "[Indication]\n9mm RLL nodule.\n[Anesthesia]\nGA.\n[Description]\nGalaxy nav RB10. Fluoro/rEBUS concentric. TBNA, Bx, Brush, BAL performed.\n[Plan]\nCXR, discharge.",
            8: "Mrs. Gonzalez had a robotic biopsy of her small RLL nodule. We used the Galaxy system, confirmed position with fluoroscopy and ultrasound, and took samples including a lung wash (BAL). Preliminary results are negative.",
            9: "Task: Robotic RLL sampling.\nMethods: TBNA, forceps, brush, BAL.\nGuidance: Galaxy, Fluoro, rEBUS (concentric).\nResult: ROSE negative."
        },
        9: { # Charles Rodriguez (RLL, TBNA/Bx/BAL/Fiducial, TiLT+)
            1: "Target: 22mm RLL nodule.\nTool: Galaxy + TiLT+.\nDiv: 2.3cm (atelectasis). Corrected.\nrEBUS: Adjacent.\nAction: TBNA x4, Bx x4, BAL, Fiducial.\nROSE: Suspicious NSCLC.",
            2: "OPERATIVE SUMMARY: Mr. Rodriguez underwent robotic bronchoscopy for a 22mm RLL nodule. The Galaxy system was deployed to RB10. TiLT+ imaging revealed a significant 2.3cm divergence due to atelectasis, which was corrected. rEBUS showed an adjacent view. We performed TBNA, forceps biopsy, and BAL. A fiducial marker was placed for SBRT. ROSE suggests non-small cell carcinoma.",
            3: "Codes: 31626 (Marker), 31629 (TBNA), 31624 (BAL), 31627 (Nav), 31654 (rEBUS).\nNote: 2.3cm divergence corrected via TiLT+.",
            4: "Resident Note\nPt: C. Rodriguez\nRLL 22mm\n1. Galaxy to RB10.\n2. TiLT found 2.3cm error (atelectasis).\n3. Adjusted.\n4. rEBUS adjacent.\n5. TBNA, Bx, BAL.\n6. Fiducial placed.\nROSE: Suspicious NSCLC.",
            5: "charles rodriguez rll nodule. galaxy robot. huge divergence on tilt 2.3cm atelectasis. fixed it. adjacent ultrasound. needle biopsy forceps and a wash. put a fiducial in. rose thinks its non small cell cancer.",
            6: "Multiple pulmonary nodules. 22mm nodule in RLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB10. TiLT+ sweep revealed 2.3cm divergence due to atelectasis. Target updated. rEBUS view: Adjacent. TBNA (22G). Transbronchial forceps biopsy. Bronchoalveolar lavage. Gold fiducial marker placed. ROSE Result: Suspicious for non-small cell carcinoma.",
            7: "[Indication]\n22mm RLL nodule.\n[Anesthesia]\nGA.\n[Description]\nGalaxy nav. TiLT+ corrected 2.3cm divergence. rEBUS adjacent. TBNA, Bx, BAL, Fiducial.\n[Plan]\nOncology.",
            8: "Mr. Rodriguez underwent a robotic biopsy. The Galaxy system's TiLT+ feature helped us correct a 2.3cm error caused by lung collapse. We sampled the area with a needle, forceps, and wash, and placed a marker. It looks suspicious for lung cancer.",
            9: "Procedure: Robotic RLL biopsy + marker.\nCorrection: TiLT+ fixed 2.3cm offset.\nSampling: TBNA, forceps, BAL.\nMarker: Fiducial implanted.\nResult: Suspicious for NSCLC."
        }
    }
    return variations

def get_base_data_mocks():
    # Names corresponding to the 10 source notes
    return [
        {"idx": 0, "orig_name": "Jessica Flores", "orig_age": 74, "names": ["Maria Garcia", "Patricia Martinez", "Linda Hernandez", "Barbara Lopez", "Elizabeth Gonzalez", "Jennifer Wilson", "Susan Anderson", "Margaret Thomas", "Dorothy Moore"]},
        {"idx": 1, "orig_name": "Linda White", "orig_age": 64, "names": ["Sarah Johnson", "Karen Davis", "Nancy Miller", "Lisa Taylor", "Betty White", "Sandra Harris", "Ashley Martin", "Kimberly Thompson", "Donna Garcia"]},
        {"idx": 2, "orig_name": "Elizabeth Lewis", "orig_age": 67, "names": ["Helen Robinson", "Carol Clark", "Ruth Rodriguez", "Sharon Lewis", "Michelle Lee", "Laura Walker", "Sarah Hall", "Kimberly Allen", "Deborah Young"]},
        {"idx": 3, "orig_name": "Shirley Walker", "orig_age": 82, "names": ["Margaret King", "Dorothy Wright", "Martha Scott", "Betty Torres", "Ruth Nguyen", "Helen Hill", "Alice Flores", "Shirley Green", "Virginia Adams"]},
        {"idx": 4, "orig_name": "Rebecca White", "orig_age": 80, "names": ["Mary Nelson", "Patricia Baker", "Linda Hall", "Barbara Rivera", "Elizabeth Campbell", "Jennifer Mitchell", "Susan Carter", "Margaret Roberts", "Dorothy Phillips"]},
        {"idx": 5, "orig_name": "Ronald Green", "orig_age": 68, "names": ["James Evans", "John Turner", "Robert Diaz", "Michael Parker", "William Cruz", "David Edwards", "Richard Collins", "Joseph Reyes", "Thomas Stewart"]},
        {"idx": 6, "orig_name": "Michael Taylor", "orig_age": 71, "names": ["Charles Morris", "Christopher Rogers", "Daniel Reed", "Matthew Cook", "Anthony Morgan", "Donald Bell", "Mark Murphy", "Paul Bailey", "Steven Rivera"]},
        {"idx": 7, "orig_name": "Angela Brown", "orig_age": 59, "names": ["Lisa Cooper", "Nancy Richardson", "Karen Cox", "Betty Howard", "Helen Ward", "Sandra Torres", "Ashley Peterson", "Kimberly Gray", "Donna Ramirez"]},
        {"idx": 8, "orig_name": "Susan Gonzalez", "orig_age": 60, "names": ["Carol James", "Ruth Watson", "Sharon Brooks", "Michelle Kelly", "Laura Sanders", "Sarah Price", "Kimberly Bennett", "Deborah Wood", "Jessica Barnes"]},
        {"idx": 9, "orig_name": "Charles Rodriguez", "orig_age": 59, "names": ["Kenneth Ross", "George Henderson", "Steven Coleman", "Edward Jenkins", "Brian Perry", "Ronald Powell", "Anthony Long", "Kevin Patterson", "Jason Hughes"]}
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
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen with full dict)
                note_entry["note_text"] = f"VARIATION MISSING FOR IDX {idx} STYLE {style_num}"
            
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
    output_filename = output_dir / "synthetic_galaxy_robotic_notes.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()