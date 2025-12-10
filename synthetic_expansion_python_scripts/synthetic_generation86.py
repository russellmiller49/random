import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_086.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(year):
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock data for the 10 patients in part_086.
    Ensures 9 unique names per patient consistent with their gender.
    """
    return [
        {
            "idx": 0, "orig_name": "Nguyen, Brian", "orig_age": 80, "gender": "Male",
            "names": ["Robert Chen", "William Tran", "James Wu", "David Le", "Michael Pham", "Richard Hoang", "Thomas Vo", "Charles Dang", "Joseph Nguyen"]
        },
        {
            "idx": 1, "orig_name": "King, Sandra", "orig_age": 65, "gender": "Female",
            "names": ["Mary Johnson", "Patricia Williams", "Linda Jones", "Barbara Brown", "Elizabeth Davis", "Jennifer Miller", "Maria Wilson", "Susan Moore", "Margaret Taylor"]
        },
        {
            "idx": 2, "orig_name": "Nguyen, James", "orig_age": 51, "gender": "Male",
            "names": ["John Smith", "Robert Anderson", "Michael Thomas", "William Jackson", "David White", "Richard Harris", "Joseph Martin", "Thomas Thompson", "Charles Garcia"]
        },
        {
            "idx": 3, "orig_name": "Mitchell, Kathleen", "orig_age": 58, "gender": "Female",
            "names": ["Karen Robinson", "Nancy Clark", "Lisa Rodriguez", "Betty Lewis", "Dorothy Lee", "Sandra Walker", "Ashley Hall", "Kimberly Allen", "Donna Young"]
        },
        {
            "idx": 4, "orig_name": "Johnson, Sandra", "orig_age": 62, "gender": "Female",
            "names": ["Carol Hernandez", "Michelle King", "Emily Wright", "Helen Lopez", "Melissa Hill", "Deborah Scott", "Stephanie Green", "Rebecca Adams", "Laura Baker"]
        },
        {
            "idx": 5, "orig_name": "Martinez, Barbara", "orig_age": 81, "gender": "Female",
            "names": ["Sharon Gonzalez", "Cynthia Nelson", "Kathleen Carter", "Amy Mitchell", "Shirley Perez", "Angela Roberts", "Anna Turner", "Ruth Phillips", "Brenda Campbell"]
        },
        {
            "idx": 6, "orig_name": "Young, Jason", "orig_age": 52, "gender": "Male",
            "names": ["Christopher Parker", "Daniel Evans", "Paul Edwards", "Mark Collins", "Donald Stewart", "George Sanchez", "Kenneth Morris", "Steven Rogers", "Edward Reed"]
        },
        {
            "idx": 7, "orig_name": "Mitchell, Carol", "orig_age": 82, "gender": "Female",
            "names": ["Virginia Cook", "Martha Morgan", "Evelyn Bell", "Alice Murphy", "Jean Bailey", "Frances Rivera", "Catherine Cooper", "Christine Richardson", "Debra Cox"]
        },
        {
            "idx": 8, "orig_name": "Ramirez, Stephen", "orig_age": 55, "gender": "Male",
            "names": ["Brian Howard", "Ronald Ward", "Anthony Torres", "Kevin Peterson", "Jason Gray", "Matthew Ramirez", "Gary James", "Timothy Watson", "Jose Brooks"]
        },
        {
            "idx": 9, "orig_name": "Brown, Amanda", "orig_age": 77, "gender": "Female",
            "names": ["Janet Kelly", "Carolyn Sanders", "Pamela Price", "Victoria Bennett", "Katherine Wood", "Emma Barnes", "Brenda Ross", "Olivia Henderson", "Nicole Coleman"]
        }
    ]

def get_variations():
    """
    Returns a dictionary of text variations for the 10 notes.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    # Note 0: 22mm RUL nodule, Galaxy/TiLT, TBNA/BAL/Fiducial.
    # Note 1: 14mm RML nodule, Galaxy/TiLT, TBNA.
    # Note 2: 28mm LUL nodule, Galaxy/TiLT, TBNA/Brush/BAL/Fiducial.
    # Note 3: 21mm RLL nodule, Galaxy/TiLT, TBNA/Forceps/Brush/BAL/Fiducial.
    # Note 4: 29mm LLL nodule, Galaxy/TiLT, TBNA/Forceps/Brush.
    # Note 5: 12mm LLL nodule, Galaxy/TiLT, TBNA/Brush.
    # Note 6: 8mm Lingula nodule, Galaxy/TiLT, TBNA/Brush.
    # Note 7: 13mm LLL nodule, Galaxy/TiLT, TBNA only.
    # Note 8: 25mm RUL nodule, Galaxy/TiLT, TBNA/Forceps/BAL/Fiducial.
    # Note 9: 11mm RUL nodule, Galaxy/TiLT, TBNA/Forceps.

    variations = {
        0: { # Brian Nguyen (RUL)
            1: "Indication: Lung-RADS 4X nodule (22mm RUL).\nProcedure: Bronchoscopy with Galaxy robotic navigation.\n- Navigated to RUL (RB3). Reg error 3.6mm.\n- TiLT+ used to correct 1.4cm divergence.\n- rEBUS: Eccentric view.\n- TBNA (22G) x 6 passes.\n- BAL RUL: 60cc in/22cc out.\n- Fiducial placed.\nROSE: Benign respiratory epithelium.\nPlan: Recovery, D/C.",
            2: "The patient presented for diagnostic bronchoscopy regarding a 22mm RUL lesion. Following induction of general anesthesia, the Noah Galaxy robotic system was deployed. Electromagnetic registration was achieved with 3.6mm accuracy. Upon navigation to the RB3 segment, Augmented Fluoroscopy (TiLT+) identified a significant divergence of 1.4cm necessitating alignment correction. Once confirmed via eccentric rEBUS signal, sampling was performed using a 22G needle and bronchoalveolar lavage. A gold fiducial was implanted for future stereotactic planning. Cytopathology revealed benign cells.",
            3: "CPT Coding Justification:\n31627: Navigation (Galaxy system utilized to reach RUL target).\n31654: Radial EBUS (Peripheral probe used to localize 22mm lesion).\n31629: TBNA (22G needle aspiration of RUL nodule).\n31626: Fiducial Markers (Placement of gold marker for SBRT).\n31624: BAL (Separate lavage of target segment).\nTechnique: TiLT+ tomosynthesis used to verify tool-in-lesion.",
            4: "Procedure: Robotic Bronchoscopy (Galaxy)\nTarget: RUL nodule\nSteps:\n1. GA/ETT.\n2. Registration (3.6mm error).\n3. Navigated to RUL anterior segment.\n4. TiLT spin showed 1.4cm divergence; updated target.\n5. Confirmed with rEBUS (eccentric).\n6. TBNA x6, BAL performed.\n7. Fiducial dropped.\n8. ROSE benign.\nPlan: Discharge.",
            5: "pt is here for lung rads 4x nodule rul. we used the galaxy robot scope registered ok 3.6mm. went to the right upper lobe had to use the tilt spin because the target was off by like 1.4cm. once lined up we saw it on ebus eccentric view. did some needle passes 22g and washed it out. put a marker in too. rose said benign stuff. no bleeding really. done.",
            6: "The patient was brought to the endoscopy suite and placed under general anesthesia. A Noah Galaxy bronchoscope was inserted. Registration was performed with a 3.6mm error. Navigation to the 22mm RUL nodule was assisted by TiLT+ tomosynthesis which corrected a 1.4cm divergence. Radial EBUS showed an eccentric view. Transbronchial needle aspiration and BAL were performed. A gold fiducial was placed. There were no complications.",
            7: "[Indication]\nLung-RADS 4X nodule, 22mm RUL.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nGalaxy navigation to RB3. TiLT+ correction of 1.4cm divergence. rEBUS eccentric. TBNA (22G) and BAL performed. Fiducial placed.\n[Plan]\nDischarge to home. Follow up 1 week.",
            8: "We began the procedure by inducing general anesthesia and securing the airway. The Galaxy robotic scope was introduced, and we navigated to the Right Upper Lobe. Utilizing the TiLT+ feature, we identified and corrected a divergence of 1.4cm. After confirming the lesion with radial EBUS, we obtained samples via needle aspiration and lavage. Finally, a fiducial marker was placed to assist with future radiation therapy.",
            9: "Indication: Lung-RADS 4X mass.\nTechnique: The Galaxy scope was steered to the RUL target. TiLT+ imaging rectified a 1.4cm discrepancy. rEBUS verified the location. The lesion was sampled via TBNA and lavage. A marker was deployed for SBRT. ROSE analysis indicated benign tissue."
        },
        1: { # Sandra King (RML)
            1: "Dx: 14mm nodule RML (Lung-RADS 4B).\nMethod: Galaxy Nav + TiLT + rEBUS.\nFindings: 2.1cm divergence corrected via TiLT. rEBUS concentric.\nActions: TBNA 21G x 7 passes.\nROSE: Necrotic debris, rare atypical cells.\nComplication: None. Pneumothorax negative on post-op scan.",
            2: "The patient underwent elective robotic bronchoscopy for a suspicious 14mm nodule in the Right Middle Lobe. The Noah Galaxy platform was utilized. Intra-procedural tomosynthesis (TiLT+) revealed a 2.1cm target divergence attributed to respiratory motion, which was digitally corrected. Following concentric rEBUS confirmation, transbronchial needle aspiration was executed. Rapid on-site evaluation suggested necrosis with atypia.",
            3: "Billable Services:\n- 31627 (Navigational Bronchoscopy): Required for 14mm RML nodule.\n- 31629 (Transbronchial Needle Aspiration): Primary sampling modality.\n- 31654 (Peripheral EBUS): Used for localization.\nNote: High complexity due to 2.1cm divergence requiring TiLT+ correction.",
            4: "Resident Note:\nAttending: Dr. Thompson\nPt: 65F, RML nodule.\n1. ETT placed.\n2. Galaxy nav to RB4.\n3. TiLT spin -> updated target (2.1cm shift).\n4. rEBUS concentric.\n5. TBNA x7.\n6. ROSE: Atypical.\nStable.",
            5: "sandra came in for the rml nodule. galaxy scope used. reg was 3.9mm. got to the rml and did the tilt spin thing, huge shift 2.1cm from breathing i guess. fixed it and saw concentric view on ebus. stuck it with the 21g needle 7 times. rose showed necrotic junk and maybe cancer. shes fine going home.",
            6: "Lung-RADS 4B nodule 14mm in RML. General anesthesia. Noah Galaxy bronchoscope introduced. Registration error 3.9mm. TiLT+ sweep performed showing 2.1cm divergence. Target updated. rEBUS concentric. TBNA 21G performed. ROSE necrotic debris. Patient tolerated well.",
            7: "[Indication]\nLung-RADS 4B, 14mm RML.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy navigation. TiLT+ used to sync target (2.1cm divergence). rEBUS concentric. TBNA performed.\n[Plan]\nMonitor for pneumothorax (negative on immediate check). Discharge.",
            8: "After inducing anesthesia, we inserted the Galaxy scope to biopsy the 14mm nodule in the right middle lobe. Because of significant respiratory motion, the TiLT system showed a 2.1cm difference from the pre-op CT, which we corrected. We confirmed the position with a nice concentric EBUS view and took seven needle passes. The pathologist saw some atypical cells on the slide.",
            9: "Reason: Lung-RADS 4B lesion.\nAction: The Galaxy system was guided to the RML. A 2.1cm divergence was rectified using TiLT+. The nodule was localized via rEBUS. Samples were acquired using a 21G needle.\nResult: ROSE showed atypical cells."
        },
        2: { # James Nguyen (LUL)
            1: "Target: 28mm LUL nodule (PET-avid).\nNav: Galaxy electromagnetic. TiLT correction 1.0cm.\nTools: rEBUS (eccentric), 22G TBNA, Cytology Brush, BAL, Fiducial.\nROSE: Suspicious (necrotic/atypical).\nPlan: Outpatient discharge.",
            2: "A 51-year-old male presented with a hypermetabolic LUL mass. Diagnostic bronchoscopy was performed utilizing the Galaxy robotic system. Registration accuracy was 3.7mm. Intraoperative C-arm tomosynthesis (TiLT) identified a 1.0cm target divergence. Following alignment, the lesion was sampled via multidimensional approach: TBNA, brushing, and lavage. A fiducial was deployed for potential SBRT.",
            3: "Coding Summary:\n31627 (Nav) + 31654 (EBUS) + 31629 (TBNA) + 31623 (Brush) + 31624 (BAL) + 31626 (Marker).\nDocumentation supports use of Galaxy navigation and TiLT+ verification for LUL target. Multiple distinct sampling tools utilized.",
            4: "Procedure: LUL biopsy (Galaxy)\nSteps:\n- ETT.\n- Nav to LB3.\n- TiLT sweep: 1.0cm shift.\n- rEBUS: Eccentric.\n- TBNA x8.\n- Brush x1.\n- BAL.\n- Marker placed.\nROSE: Atypical cells.",
            5: "james has a pet avid nodule lul. we did the galaxy bronch today. registration ok. tilt showed the nodule was 1cm off from the ct so we fixed that. did needles brushes and a wash. also dropped a seed for radiation. rose guy said it looks weird necrotic. no issues.",
            6: "PET-avid lung nodule 28mm in LUL. General anesthesia. Noah Galaxy bronchoscope used. Navigated to LB3. TiLT+ sweep revealed 1.0cm divergence. Corrected. rEBUS eccentric. TBNA 22G, Cytology brush, BAL, and Gold fiducial placement performed. ROSE necrotic debris with rare atypical cells. Discharged stable.",
            7: "[Indication]\nPET-avid nodule, 28mm LUL.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy Nav to LB3. TiLT correction (1.0cm). rEBUS eccentric. TBNA, Brush, BAL performed. Fiducial placed.\n[Plan]\nResults in 5-7 days.",
            8: "We went after a 28mm spot in the left upper lobe today. Using the Galaxy robot, we got close and used the TiLT spin to fine-tune our position, correcting a 1cm error. We threw the kitchen sink at it—needle biopsies, brushing, and a wash. We also left a gold marker behind just in case he needs radiation later. The preliminary slides look suspicious.",
            9: "Indication: PET-avid mass.\nOperation: Galaxy navigation to LUL. TiLT+ adjusted for 1.0cm divergence. Lesion localized with rEBUS. Sampled via TBNA and brush. Lavaged. Marker implanted. ROSE: Atypical."
        },
        3: { # Kathleen Mitchell (RLL)
            1: "Indication: RLL nodule (21mm, 4X).\nNav: Galaxy. Reg error 2.7mm.\nVerify: TiLT+ & Fluoroscopy.\nBiopsy: TBNA, Forceps (4 specs), Brush, BAL.\nMarker: Fiducial placed.\nROSE: Adenocarcinoma.",
            2: "The patient underwent robotic-assisted bronchoscopy for a 21mm RLL lesion. The Galaxy system provided navigational guidance to the RB7 segment. Fluoroscopic and TiLT overlay confirmed tool-in-lesion status. Diagnostic yield was pursued via 22G TBNA, transbronchial forceps biopsy, and brushing. On-site pathology confirmed adenocarcinoma. A fiducial was placed for treatment planning.",
            3: "Codes: 31629 (TBNA), 31624 (BAL), 31623 (Brush), 31627 (Nav), 31654 (EBUS), 31626 (Marker).\nNote: Forceps biopsy (31628) performed but bundled with 31629 at same site per NCCI. High complexity procedure using TiLT augmented fluoroscopy.",
            4: "RLL Nodule Biopsy.\n- Navigated to RB7 using Galaxy.\n- Validated with TiLT/Fluoro.\n- rEBUS eccentric.\n- Needles, Forceps, Brush, BAL done.\n- Fiducial dropped.\n- ROSE: Adeno.",
            5: "kathleen here for the rll nodule 21mm. galaxy scope. reg was super good 2.7mm. fluoroscopy and tilt confirmed we were right on it. did needles forceps brush and wash. put a gold seed in. rose says its cancer adenocarcinoma. told the family we are waiting for finals.",
            6: "Lung-RADS 4X nodule 21mm in RLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB7. Fluoroscopic guidance with TiLT overlay. rEBUS eccentric. TBNA 22G, Forceps biopsy, Cytology brush, BAL, and Fiducial marker placement performed. ROSE Malignant cells identified consistent with adenocarcinoma.",
            7: "[Indication]\nLung-RADS 4X, 21mm RLL.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy Nav to RB7. Verified via TiLT/Fluoro. TBNA, Forceps, Brush, BAL. Fiducial placed.\n[Plan]\nOncology referral pending final path.",
            8: "Ms. Robinson had a suspicious spot in her right lower lung. We used the Galaxy system to guide us right to it. We double-checked our position with x-ray and the TiLT system. We took several different types of samples including needle, forceps, and brush. Unfortunately, the preliminary check in the room showed it is adenocarcinoma. We placed a marker for future treatment.",
            9: "Indication: Lung-RADS 4X lesion.\nProcedure: Galaxy navigation to RLL. Position validated with TiLT overlay. Lesion sampled via TBNA, forceps, and brush. Lavaged. Marker deployed. ROSE: Adenocarcinoma."
        },
        4: { # Sandra Johnson (LLL)
            1: "Target: 29mm LLL nodule.\nSystem: Galaxy + TiLT.\nCorrection: 1.4cm divergence (CT-body drift).\nBiopsy: TBNA, Forceps, Brush.\nROSE: Adenocarcinoma.\nDisposition: Discharge.",
            2: "Evaluation of a 29mm LLL mass was conducted. The Galaxy navigational platform facilitated access to the LB6 segment. Intraprocedural TiLT imaging detected a 1.4cm registration drift, which was corrected in real-time. Following 'adjacent' rEBUS confirmation, extensive sampling (TBNA, forceps, brush) yielded a diagnosis of adenocarcinoma.",
            3: "CPT 31629 (TBNA), 31623 (Brush), 31627 (Nav), 31654 (EBUS). Forceps biopsy performed but bundled. TiLT used to correct 1.4cm divergence to ensure diagnostic yield. ROSE confirmed malignancy.",
            4: "Procedure: LLL Biopsy\nPt: 62F.\n- Galaxy Nav to LB6.\n- TiLT: 1.4cm divergence fixed.\n- rEBUS: Adjacent.\n- TBNA x7, Forceps x4, Brush.\n- ROSE positive for Adeno.\nStable.",
            5: "sandra has a big nodule 29mm in the lll. used galaxy. tilt showed we were 1.4cm off so glad we checked. fixed it. did needles forceps and brushing. rose says adeno. patient did fine.",
            6: "Lung-RADS 4B nodule 29mm in LLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to LB6. TiLT+ sweep showed 1.4cm divergence due to registration drift. Corrected. rEBUS adjacent. TBNA 21G, Transbronchial forceps biopsy, Cytology brushings performed. ROSE Malignant cells identified.",
            7: "[Indication]\nLung-RADS 4B, 29mm LLL.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy Nav to LB6. TiLT correction 1.4cm. rEBUS adjacent. TBNA, Forceps, Brush performed.\n[Plan]\nPathology follow-up.",
            8: "We navigated to the left lower lobe to biopsy a 29mm nodule. The TiLT scan showed that the target had shifted about 1.4cm from where the computer thought it was, likely due to patient movement, so we updated the target. We took needle and forcep samples. The pathologist in the room confirmed it looks like adenocarcinoma.",
            9: "Indication: Lung-RADS 4B mass.\nTechnique: Galaxy navigation to LLL. TiLT+ rectified 1.4cm error. Sampled via TBNA, forceps, and brush. ROSE: Adenocarcinoma."
        },
        5: { # Barbara Martinez (LLL)
            1: "Indication: 12mm LLL nodule.\nNav: Galaxy + TiLT.\nDiv: 2.1cm (atelectasis).\nTools: rEBUS (concentric), TBNA, Brush.\nROSE: Atypical.\nResult: No complications.",
            2: "A high-risk 12mm LLL nodule was interrogated. Galaxy navigation was employed. A significant 2.1cm divergence caused by atelectasis was identified via TiLT+ and corrected. Upon establishing a concentric rEBUS view, 21G TBNA and cytology brushing were performed. Preliminary pathology indicates atypia.",
            3: "Codes: 31629 (TBNA), 31623 (Brush), 31627 (Nav), 31654 (EBUS). Note: Significant 2.1cm divergence required TiLT+ correction to ensure tool-in-lesion.",
            4: "LLL Nodule (12mm).\n- Galaxy nav to LB9.\n- TiLT: 2.1cm shift (atelectasis).\n- rEBUS: Concentric.\n- TBNA x7, Brush.\n- ROSE: Atypical/Suspicious.",
            5: "barbara has a small nodule 12mm lll. galaxy robot used. huge shift 2.1cm probably atelectasis tilt fixed it. concentric ebus which is good. needle and brush used. rose says atypical cant rule out cancer. home.",
            6: "Suspicious nodule 12mm in LLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to LB9. TiLT+ sweep revealed 2.1cm divergence due to atelectasis. Corrected. rEBUS concentric. TBNA 21G and Cytology brushings performed. ROSE Atypical cells. Discharged.",
            7: "[Indication]\nSuspicious nodule, 12mm LLL.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy Nav. TiLT correction 2.1cm. rEBUS concentric. TBNA and Brush performed.\n[Plan]\nAwait final path.",
            8: "This was a tricky 12mm nodule in the left lower lobe. When we got down there with the Galaxy scope, the TiLT scan showed the target was actually 2.1cm away from where we expected, probably because the lung collapsed a bit. We adjusted, got a bullseye view on EBUS, and took our samples. The pathologist is worried it might be cancer but needs to see the final stains.",
            9: "Reason: High Brock score nodule.\nAction: Galaxy navigation to LLL. TiLT+ adjusted for 2.1cm atelectasis shift. Localized via rEBUS. Sampled via TBNA and brush. ROSE: Atypical."
        },
        6: { # Jason Young (Lingula)
            1: "Target: 8mm nodule Lingula.\nNav: Galaxy + TiLT (1.1cm div).\nTools: rEBUS (eccentric), TBNA, Brush.\nROSE: SCC.\nPlan: Oncology.",
            2: "Diagnostic bronchoscopy for a peripheral 8mm Lingular nodule. The Galaxy system was used. TiLT+ tomosynthesis corrected a 1.1cm target divergence. Despite the small size, an eccentric rEBUS signal was obtained. Sampling via TBNA and brush yielded squamous cell carcinoma.",
            3: "31629 (TBNA), 31623 (Brush), 31627 (Nav), 31654 (EBUS). Small 8mm target required TiLT+ precision (1.1cm correction). ROSE positive for malignancy.",
            4: "Lingula Nodule (8mm).\n- Galaxy Nav to LB4.\n- TiLT: 1.1cm divergence.\n- rEBUS: Eccentric.\n- TBNA x8, Brush.\n- ROSE: Squamous Cell.\nStable.",
            5: "jason has a tiny 8mm nodule in the lingula. used galaxy. tilt showed 1.1cm off. fixed it. saw it on ebus. needles and brushes. rose says squamous cell carcinoma. tough case but got it.",
            6: "Peripheral pulmonary nodule 8mm in Lingula. General anesthesia. Noah Galaxy bronchoscope. Navigated to LB4. TiLT+ sweep revealed 1.1cm divergence. Corrected. rEBUS eccentric. TBNA 22G and Cytology brushings performed. ROSE Malignant cells identified consistent with squamous cell carcinoma.",
            7: "[Indication]\n8mm nodule, Lingula.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy Nav. TiLT correction 1.1cm. rEBUS eccentric. TBNA and Brush performed.\n[Plan]\nOncology consult.",
            8: "We went after a small 8mm spot in the Lingula. The Galaxy system got us close, and the TiLT 3D spin helped us close the last 1.1cm gap. We got a signal on the ultrasound and took needle and brush samples. It looks like squamous cell carcinoma unfortunately.",
            9: "Indication: Peripheral nodule.\nProcedure: Galaxy navigation to Lingula. TiLT+ rectified 1.1cm error. Lesion sampled via TBNA and brush. ROSE: Squamous cell carcinoma."
        },
        7: { # Carol Mitchell (LLL)
            1: "Target: 13mm LLL nodule.\nNav: Galaxy + TiLT (1.9cm div).\nTools: rEBUS (adjacent), TBNA.\nROSE: Suspicious for NSCLC.\nDisposition: D/C.",
            2: "The patient underwent evaluation of a 13mm LLL nodule. Galaxy robotic navigation was employed. Intraoperative TiLT imaging revealed a significant 1.9cm divergence due to respiratory motion, which was corrected. Following adjacent rEBUS confirmation, 21G TBNA was performed. Cytology is suspicious for non-small cell lung cancer.",
            3: "31629 (TBNA), 31627 (Nav), 31654 (EBUS). 1.9cm divergence corrected by TiLT+.",
            4: "LLL Nodule (13mm).\n- Galaxy to LB10.\n- TiLT: 1.9cm shift.\n- rEBUS: Adjacent.\n- TBNA x6.\n- ROSE: Suspicious NSCLC.",
            5: "carol here for lll nodule 13mm. galaxy scope. breathing moved the target 1.9cm tilt fixed it. adjacent ebus view. just did needles. rose thinks nsclc.",
            6: "Peripheral pulmonary nodule 13mm in LLL. General anesthesia. Noah Galaxy bronchoscope. Navigated to LB10. TiLT+ sweep revealed 1.9cm divergence. Corrected. rEBUS adjacent. TBNA 21G performed. ROSE Suspicious for non-small cell carcinoma.",
            7: "[Indication]\n13mm nodule, LLL.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy Nav. TiLT correction 1.9cm. rEBUS adjacent. TBNA performed.\n[Plan]\nFollow up.",
            8: "Mrs. Cook had a 13mm nodule in the back of the left lower lobe. We used the Galaxy robot. The TiLT scan showed it was almost 2cm away from where we expected due to her breathing, so we updated the target and found it. We did six needle passes. It looks suspicious for cancer.",
            9: "Reason: Peripheral nodule.\nAction: Galaxy navigation to LLL. TiLT+ adjusted for 1.9cm shift. Sampled via TBNA. ROSE: Suspicious for NSCLC."
        },
        8: { # Stephen Ramirez (RUL)
            1: "Target: 25mm RUL mass.\nNav: Galaxy + TiLT (0.8cm div).\nTools: rEBUS (eccentric), TBNA, Forceps, BAL, Fiducial.\nROSE: Adenocarcinoma.\nPlan: SBRT planning.",
            2: "A 25mm RUL mass was biopsied using the Galaxy robotic system. Navigation to RB2 was accurate, with TiLT confirming a minor 0.8cm divergence. Multimodal sampling (TBNA, forceps, BAL) was performed. A fiducial was placed. Pathology confirmed adenocarcinoma.",
            3: "31629 (TBNA), 31624 (BAL), 31626 (Marker), 31627 (Nav), 31654 (EBUS). Forceps bundled. 0.8cm TiLT correction.",
            4: "RUL Mass (25mm).\n- Galaxy Nav to RB2.\n- TiLT: 0.8cm shift.\n- rEBUS: Eccentric.\n- TBNA x7, Forceps x7, BAL.\n- Fiducial placed.\n- ROSE: Adeno.",
            5: "stephen has a mass 25mm rul. galaxy used. tilt showed small shift 0.8cm. good samples needle and forceps and wash. dropped a seed. rose confirmed adeno.",
            6: "Suspected lung malignancy 25mm nodule in RUL. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB2. TiLT+ sweep revealed 0.8cm divergence. Corrected. rEBUS eccentric. TBNA 21G, Transbronchial forceps biopsy, BAL, and Gold fiducial placement performed. ROSE Malignant cells identified.",
            7: "[Indication]\n25mm mass, RUL.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy Nav. TiLT correction 0.8cm. rEBUS eccentric. TBNA, Forceps, BAL. Fiducial placed.\n[Plan]\nOncology.",
            8: "We biopsied a 25mm mass in the right upper lobe using the Galaxy robot. The TiLT system showed we were very close, just 0.8cm off, which we fixed. We took plenty of samples with needles and forceps and washed the area. We left a marker for the radiation doctors. It is adenocarcinoma.",
            9: "Indication: Suspected malignancy.\nProcedure: Galaxy navigation to RUL. TiLT+ rectified 0.8cm error. Sampled via TBNA, forceps, and lavage. Marker deployed. ROSE: Adenocarcinoma."
        },
        9: { # Amanda Brown (RUL)
            1: "Target: 11mm RUL nodule.\nNav: Galaxy. Reg error 3.0mm.\nVerify: Fluoroscopy.\nTools: rEBUS (eccentric), TBNA, Forceps.\nROSE: Granuloma.\nResult: Benign.",
            2: "Diagnostic bronchoscopy for an 11mm RUL nodule in a patient with prior malignancy history. Galaxy navigation was utilized to reach RB2. Fluoroscopic confirmation was obtained. Sampling via TBNA and forceps revealed granulomatous inflammation, arguing against recurrence.",
            3: "31629 (TBNA), 31627 (Nav), 31654 (EBUS). Forceps bundled. 11mm target reached with Galaxy/Fluoroscopy.",
            4: "RUL Nodule (11mm).\n- Galaxy Nav to RB2.\n- Fluoro confirm.\n- rEBUS: Eccentric.\n- TBNA x5, Forceps x6.\n- ROSE: Granuloma.",
            5: "amanda has a history of cancer now has 11mm nodule rul. galaxy scope. saw it on fluoro. eccentric ebus. needle and forceps. rose says granuloma so probably not cancer. good news.",
            6: "Pulmonary nodule 11mm in RUL. General anesthesia. Noah Galaxy bronchoscope. Navigated to RB2. Fluoroscopic guidance. rEBUS eccentric. TBNA 22G and Transbronchial forceps biopsy performed. ROSE Granulomatous inflammation.",
            7: "[Indication]\n11mm nodule, RUL.\n[Anesthesia]\nGeneral.\n[Description]\nGalaxy Nav. Fluoroscopy. rEBUS eccentric. TBNA and Forceps performed.\n[Plan]\nFollow up.",
            8: "Ms. Kelly has a history of cancer and a new 11mm spot in the right upper lobe. We used the Galaxy system to reach it and confirmed with fluoroscopy. We took samples with needles and forceps. The preliminary read shows granulomas, which is a relief as it suggests inflammation rather than cancer.",
            9: "Reason: Pulmonary nodule.\nAction: Galaxy navigation to RUL. Position verified via fluoroscopy. Sampled via TBNA and forceps. ROSE: Granulomatous inflammation."
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
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Map MRNs to index to ensure we match the right style dict
    # Assuming source_data is in order 0-9 matching get_variations
    
    generated_notes = []
    
    for idx, note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Generate 9 styles
        for style_num in range(1, 10):
            new_note = copy.deepcopy(note)
            
            # Apply Style Text
            if idx in variations_text and style_num in variations_text[idx]:
                new_note['note_text'] = variations_text[idx][style_num]
            else:
                new_note['note_text'] = f"Style {style_num} text not defined for note {idx}"

            # Apply Demographics
            new_name = record['names'][style_num - 1]
            new_age = orig_age + random.randint(-2, 2)
            new_date = generate_random_date(2025).strftime("%Y-%m-%d")
            
            # Update Registry Entry
            if 'registry_entry' in new_note:
                new_note['registry_entry']['patient_mrn'] = f"{new_note['registry_entry']['patient_mrn']}_syn_{style_num}"
                new_note['registry_entry']['procedure_date'] = new_date
                new_note['registry_entry']['patient_age'] = new_age
                # We don't have a name field in registry_entry in this schema, 
                # but if it existed or was in note_text, the note_text is already replaced.
            
            # Add Metadata
            new_note['synthetic_metadata'] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(new_note)
            
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    outfile = output_path / "synthetic_galaxy_notes_part_086.json"
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2)
        
    print(f"Generated {len(generated_notes)} notes in {outfile}")

if __name__ == "__main__":
    main()