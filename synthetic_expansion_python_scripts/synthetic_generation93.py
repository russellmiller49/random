import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_093.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Provides mock replacement names for the synthetic variations.
    Mapped by (Category Index, Case Index).
    """
    # Names lists for the 9 styles
    males_1 = ["James H. Smith", "Robert K. Jones", "Michael B. Brown", "William D. Davis", "David P. Miller", "Richard Wilson", "Joseph Moore", "Thomas Taylor", "Charles Anderson"]
    females_1 = ["Mary J. Johnson", "Patricia A. Williams", "Linda S. Jones", "Barbara K. Brown", "Elizabeth R. Davis", "Jennifer Miller", "Maria Wilson", "Susan Moore", "Margaret Taylor"]
    
    # Mapping specific cases to gendered lists
    # (Cat 0, Case 0) = Margaret Chen (F)
    # (Cat 1, Case 0) = David Kim (M)
    # (Cat 2, Case 0) = Dorothy Adams (F)
    # (Cat 3, Case 0) = James Wilson (M)
    # (Cat 4, Case 0) = Linda Chang (F)
    # (Cat 5, Case 0) = Harold Johnson (M)
    # (Cat 6, Case 0) = Patricia Moore (F)
    # (Cat 7, Case 0) = Frank Anderson (M)
    
    return {
        (0, 0): {"orig_name": "Margaret Chen", "orig_age": 73, "names": females_1},
        (1, 0): {"orig_name": "David Kim", "orig_age": 70, "names": males_1},
        (2, 0): {"orig_name": "Dorothy Adams", "orig_age": 76, "names": ["Betty White", "Sandra Harris", "Ashley Clark", "Kimberly Lewis", "Donna Robinson", "Carol Walker", "Michelle Hall", "Sarah Allen", "Karen Young"]},
        (3, 0): {"orig_name": "James Wilson", "orig_age": 67, "names": ["Steven King", "Edward Wright", "Brian Scott", "Ronald Torres", "Anthony Nguyen", "Kevin Hill", "Jason Flores", "Matthew Green", "Gary Adams"]},
        (4, 0): {"orig_name": "Linda Chang", "orig_age": 69, "names": ["Helen Baker", "Deborah Gonzalez", "Stephanie Nelson", "Rebecca Carter", "Sharon Mitchell", "Cynthia Perez", "Kathleen Roberts", "Amy Turner", "Anna Phillips"]},
        (5, 0): {"orig_name": "Harold Johnson", "orig_age": 73, "names": ["George Campbell", "Kenneth Parker", "Andrew Evans", "Edward Edwards", "Joshua Collins", "Jerry Stewart", "Dennis Sanchez", "Walter Morris", "Patrick Rogers"]},
        (6, 0): {"orig_name": "Patricia Moore", "orig_age": 67, "names": ["Brenda Reed", "Pamela Cook", "Nicole Morgan", "Katherine Bell", "Virginia Murphy", "Debra Bailey", "Rachel Rivera", "Janet Cooper", "Catherine Richardson"]},
        (7, 0): {"orig_name": "Frank Anderson", "orig_age": 68, "names": ["Frank Cox", "Scott Howard", "Eric Ward", "Stephen Torres", "Larry Peterson", "Justin Gray", "Brandon Ramirez", "Gregory James", "Samuel Watson"]}
    }

def get_variations():
    """
    Returns the manually crafted text variations.
    Keys are (Category Index, Case Index).
    Values are dictionaries mapping Style Index (1-9) to the new Note Text.
    """
    variations = {
        # Category 0: IPC Removal (32552) - Case 0: Margaret Chen
        (0, 0): {
            1: "Pre-op: Recurrent malignant effusion, now minimal output. Spontaneous pleurodesis.\nProcedure: Right PleurX removal (32552).\n- Local lidocaine.\n- Incision at exit site.\n- Cuff dissected from subq tissue.\n- Catheter removed intact.\n- 3-0 Nylon closure.\nComplications: None.\nPlan: Wound care.",
            2: "HISTORY OF PRESENT ILLNESS: Ms. Chen, a 73-year-old female with metastatic ovarian carcinoma, presented for elective removal of a right-sided indwelling pleural catheter. The device was placed four months prior for palliation of malignant pleural effusion. Recent logs indicate drainage has ceased, suggesting successful autopleurodesis.\nOPERATIVE NARRATIVE: The patient was placed in the left lateral decubitus position. Following sterile preparation and infiltration of 1% lidocaine, an incision was made along the catheter track. The Dacron cuff was identified and liberated via blunt dissection from the subcutaneous tissue. The catheter was extracted without resistance. Inspection confirmed the device was intact. The tract was closed with simple interrupted sutures.\nIMPRESSION: Successful removal of right IPC.",
            3: "Service: Removal of tunneled pleural catheter (CPT 32552).\nIndication: Cessation of flow consistent with pleurodesis.\nTechnique:\n1. Anesthesia: Local infiltration (1% lidocaine).\n2. Exposure: Incision performed to expose the subcutaneous cuff (approx. 2cm from exit).\n3. Removal: Cuff dissected free from fibrous capsule. Catheter withdrawn from pleural space.\n4. Closure: Sutures applied.\nFindings: Catheter removed intact (28cm). No signs of tract infection.",
            4: "Procedure: IPC Removal\nAttending: Dr. Morrison\nResident: [Name]\nSteps:\n1. Time out performed. Right chest prepped.\n2. Local anesthetic injected.\n3. Cut down on cuff.\n4. Dissected cuff free using hemostats.\n5. Pulled catheter out. No resistance.\n6. Stitched up with 3-0 nylon.\nPlan: Keep dry for 48h. Suture removal in 10-14 days.",
            5: "pt margaret chen here for pleurx removal right side drainage stopped so we assume pleurodesis used local numbing cut down to the cuff freed it up with the kelly clamp and pulled it out came out fine no issues stitched it up with nylon patient tolerated well discharge home thanks.",
            6: "Margaret Chen 73F presented for removal of right PleurX catheter due to decreased drainage. Under local anesthesia the right lateral chest wall was prepped. The catheter exit site was identified and anesthetized. An incision was made to expose the retention cuff. The cuff was dissected free from the subcutaneous tissues. The catheter was removed intact. The wound was closed with sutures and a sterile dressing applied. The patient tolerated the procedure well.",
            7: "[Indication]\nMetastatic ovarian cancer, s/p Right PleurX, now with autopleurodesis (minimal output).\n[Anesthesia]\nLocal 1% lidocaine.\n[Description]\nIncision made at exit site. Cuff identified and dissected free from adhesions. Catheter withdrawn from right hemithorax intact. Hemostasis achieved. Wound closed with 3-0 nylon.\n[Plan]\nDischarge home. Wound care instructions given. Follow up 2 weeks.",
            8: "The patient is a 73-year-old female with a history of ovarian cancer who came in to have her right lung catheter removed. She has had the catheter for about 4 months, but lately, hardly any fluid has been coming out, which means the lung has likely adhered to the chest wall. We numbed the area with lidocaine and made a small cut to reach the cuff that holds the tube in place. Once we freed the cuff, the tube slid out easily. We stitched up the small cut and put a bandage on it.",
            9: "Operation: Extraction of tunneled pleural drain.\nReason: Accomplished symphysis.\nMethod: Under local blockade, the tissue surrounding the anchor cuff was separated. The conduit was withdrawn from the pleural cavity without incident. The entry site was approximated with sutures."
        },
        # Category 1: Thoracentesis (32554) - Case 0: David Kim
        (1, 0): {
            1: "Indication: Large Left pleural effusion, decompensated CHF.\nProcedure: Therapeutic Thoracentesis (32554).\n- Sitting position.\n- Local: Lido 1%.\n- Needle insertion: 8th ICS, posterior axillary line.\n- Fluid: 1800mL straw-colored removed.\n- No imaging used (Landmark technique).\nComplications: None.\nStatus: Dyspnea improved.",
            2: "PROCEDURE: Therapeutic Thoracentesis (without imaging guidance).\nCLINICAL SUMMARY: Mr. Kim, a 70-year-old male with NYHA Class IV heart failure, presented with acute respiratory distress secondary to a massive left-sided pleural effusion.\nTECHNIQUE: The patient was positioned upright. The left hemithorax was percussed to delineate the fluid level. The 8th intercostal space was selected based on physical landmarks. Following aseptic preparation and local anesthesia, an 18G catheter-over-needle was introduced into the pleural space. A total of 1.8 liters of serous fluid was evacuated via gravity drainage. The catheter was withdrawn, and the patient reported immediate symptomatic relief.",
            3: "CPT Code: 32554 (Thoracentesis without imaging).\nSite: Left Hemithorax.\nVolume: 1800 mL.\nTechnique: Percussion used to identify fluid level. Needle entry at 8th intercostal space. Imaging was NOT utilized for this procedure.\nMedical Necessity: Therapeutic relief of respiratory distress due to large effusion.",
            4: "Procedure: Bedside Thoracentesis\nPatient: David Kim\nStaff: Dr. Johnson\nSteps:\n1. Prepped left back.\n2. Numbed with lido.\n3. Inserted needle 8th rib space.\n4. Drained 1800cc yellow fluid.\n5. Pulled needle.\nPatient feels much better. Sats up to 95%.",
            5: "david kim 70m with chf needs tap on the left side cant breathe good. sat him up leaned over table. tapped out the fluid level used lido. stuck him 8th space got 1800 ml straw fluid out. he coughed a bit at the end so we stopped. no imaging just physical exam. breathing better now.",
            6: "Thoracentesis performed on David Kim for large left pleural effusion. Patient positioned sitting. Percussion identified dullness at left base. Under local anesthesia an 18G needle was inserted at the 8th intercostal space without imaging guidance. 1800mL of straw-colored fluid was removed. The patient tolerated the procedure well with improvement in oxygen saturation.",
            7: "[Indication]\nDecompensated CHF, large left effusion, respiratory distress.\n[Anesthesia]\nLocal 1% Lidocaine.\n[Description]\nSite selected via percussion (8th ICS). Needle introduced. 1800mL serous fluid removed. No imaging used.\n[Plan]\nMonitor O2. Send fluid for analysis if indicated.",
            8: "Mr. Kim was struggling to breathe due to fluid around his left lung from his heart failure. We performed a procedure to drain this fluid at the bedside. We sat him up and tapped on his back to find the best spot. We didn't need to use ultrasound. We numbed the skin and put a small tube in, draining about 1.8 liters of clear yellow fluid. He felt much better right away and his oxygen levels went up.",
            9: "Procedure: Pleural aspiration without radiological steering.\nSite: Left thoracic cavity.\nAction: The effusion was located via physical percussion. A cannula was introduced, and 1800mL of effusion was evacuated.\nOutcome: Alleviation of dyspnea."
        },
        # Category 2: Pleurodesis (32560) - Case 0: Dorothy Adams
        (2, 0): {
            1: "Dx: Recurrent malignant R effusion.\nAction: Chemical Pleurodesis (32560).\n- Chest tube confirmed functional.\n- 4g Talc slurry instilled.\n- Dwell time: 1 hr with rotation.\n- Tube to suction.\nOutcome: Tolerated well w/ morphine.",
            2: "OPERATIVE REPORT: Instillation of Sclerosing Agent.\nINDICATION: Ms. Adams, a 76-year-old female with metastatic breast carcinoma, required palliation for a recurrent right malignant pleural effusion.\nPROCEDURE: The existing right-sided 14Fr chest tube was utilized. A slurry comprising 4 grams of sterile talc suspended in 50mL of normal saline was prepared. This suspension was instilled into the pleural cavity. The tubing was clamped for sixty minutes, during which the patient was rotated to facilitate widespread pleural contact. Subsequently, the tube was unclamped and placed on -20cmH2O suction to appose the pleural surfaces.",
            3: "Code: 32560 (Instillation of agent for pleurodesis).\nAgent: Talc (4g).\nMethod: Slurry via existing chest tube.\nLocation: Right pleural space.\nRequirements met: Instillation of sclerosing agent for therapeutic pleurodesis of malignant effusion.",
            4: "Procedure: Talc Pleurodesis\nPatient: Dorothy Adams\nSteps:\n1. Checked chest tube output (<100ml).\n2. Mixed 4g talc in saline.\n3. Pushed slurry into tube.\n4. Clamped tube.\n5. Rotated patient q15 mins.\n6. Unclamped after 1 hour.\nPain managed with morphine.",
            5: "doing pleurodesis on ms adams right side breast cancer effusion. tube drain looks good so we put the talc in today. 4 grams mixed with saline. shot it in the tube and clamped it. moved her around for an hour then put it back on suction. she had some chest pain gave morphine. hope it sticks.",
            6: "Instillation of talc slurry via chest tube for pleurodesis performed on Dorothy Adams. Indication was recurrent right malignant pleural effusion. 4 grams of talc were mixed in 50mL saline and instilled through the existing chest tube. The tube was clamped for 1 hour with patient rotation. The patient received morphine for chest pain. The tube was returned to suction to facilitate pleurodesis.",
            7: "[Indication]\nRecurrent Right Malignant Pleural Effusion (Breast CA).\n[Anesthesia]\nLocal/IV Morphine for pain.\n[Description]\n4g Talc slurry instilled via 14Fr chest tube. Clamped 1 hour with rotation. Returned to suction.\n[Plan]\nMonitor output. Pull tube when <150mL/day.",
            8: "Mrs. Adams has fluid coming back around her right lung because of her cancer. We decided to 'glue' the lung to the chest wall to stop the fluid. We used her existing chest tube to put a mixture of talc and water inside. We clamped the tube and had her roll around in bed for an hour to coat the inside of her chest. Afterward, we put the tube back on suction. She had some pain but we treated it with medication.",
            9: "Procedure: Introduction of sclerosing agent.\nContext: Recurrent right thoracic effusion.\nAction: Talc suspension (4g) was infused via the indwelling thoracostomy tube. Following a dwell period with repositioning, negative pressure was re-applied to promote symphysis."
        },
        # Category 3: TBLB Add-on (31628, +31632) - Case 0: James Wilson
        (3, 0): {
            1: "Indication: Bilateral nodules (RUL, LUL).\nProcedure: Bronchoscopy w/ TBLB (Bi-lobar).\n- 31628: TBLB RUL x6.\n- 31632: TBLB LUL x5.\n- 31627: Nav used.\n- 31624: BAL RUL.\nResults: Samples obtained. No pneumothorax.",
            2: "PROCEDURE NOTE: Flexible Bronchoscopy with Transbronchial Biopsy of Multiple Lobes.\nINDICATION: Evaluation of PET-avid nodules in the RUL (1.8cm) and LUL (1.2cm).\nNARRATIVE: The bronchoscope was introduced. The Ion navigation system was utilized to localize the target in the Right Upper Lobe. Transbronchial biopsies were obtained (CPT 31628). Subsequently, the scope was navigated to the Left Upper Lobe nodule. A separate set of biopsies was obtained from this second lobe (CPT 31632). A BAL was also performed in the RUL. There were no complications.",
            3: "Billing Summary:\n- 31628: TBLB, Initial Lobe (RUL).\n- 31632: TBLB, Additional Lobe (LUL).\n- 31627: Navigation guidance.\n- 31624: Bronchoalveolar Lavage.\nJustification: Biopsies taken from two distinct lobes (Right Upper and Left Upper) requiring repositioning and separate sampling passes.",
            4: "Procedure: Bronch/Biopsy\nSteps:\n1. Scope in.\n2. Navigated to RUL nodule -> Biopsy x6 (First lobe).\n3. Navigated to LUL nodule -> Biopsy x5 (Add-on lobe).\n4. BAL done in RUL.\n5. Fluoro used.\nNo pneumo on post-op film.",
            5: "james wilson 67m here for nodules on both sides using the ion robot. went to the rul first took 6 bites that counts as the first lobe. then went over to the lul took 5 bites thats the add on code. also did a wash in the rul. no bleeding really. xray clear.",
            6: "Flexible bronchoscopy performed for bilateral nodules. Navigation was used to localize a lesion in the RUL; transbronchial biopsies were obtained (31628). Navigation was then used to localize a second lesion in the LUL; additional transbronchial biopsies were obtained (31632). Bronchoalveolar lavage was performed in the RUL. The patient tolerated the procedure well.",
            7: "[Indication]\nBilateral PET-avid lung nodules (RUL, LUL).\n[Anesthesia]\nGeneral, ETT.\n[Description]\n1. BAL RUL.\n2. TBLB RUL (Initial Lobe) with Nav.\n3. TBLB LUL (Additional Lobe) with Nav.\n[Plan]\nPathology pending. Discharge when stable.",
            8: "Mr. Wilson has spots on both his right and left lungs that we needed to sample. We put him to sleep and used a special navigation scope. First, we went to the top right part of the lung and took several small pieces of tissue. Then, we moved the scope to the top left part of the lung and took more samples from there. We also washed the right lung to check for infection. Everything went smoothly.",
            9: "Procedure: Endoscopy with sampling of multiple lobar sites.\nAction: The RUL lesion was engaged and sampled (primary biopsy). The LUL lesion was subsequently engaged and sampled (supplemental biopsy). Lavage was performed in the primary lobe."
        },
        # Category 4: TBNA Add-on (31629, +31633) - Case 0: Linda Chang
        (4, 0): {
            1: "Indication: Staging RUL CA.\nProcedure:\n- 31653: EBUS 3 stations (4R, 7, 4L).\n- 31629: TBNA RUL mass (First lobe).\n- 31633: TBNA LUL nodule (Add'l lobe).\nResults: N2 disease confirmed.",
            2: "OPERATIVE REPORT: EBUS-TBNA and Conventional TBNA.\nThe mediastinum was staged utilizing EBUS, sampling stations 4R, 7, and 4L. Attention was then turned to parenchymal targets. Using a conventional TBNA needle, the RUL mass was sampled (Initial Lobe, 31629). Subsequently, the separate LUL nodule was identified and sampled (Additional Lobe, 31633). ROSE confirmed malignancy.",
            3: "Code Selection:\n- 31653 (EBUS-TBNA 3+ stations).\n- 31629 (Transtracheal/bronchial needle aspiration, initial lobe/structure - RUL Mass).\n- 31633 (TBNA, each additional lobe - LUL Nodule).\nRationale: Separate parenchymal lesions in distinct lobes sampled via needle aspiration.",
            4: "Procedure: EBUS + TBNA\n1. EBUS done first (3 stations).\n2. Switched to conventional needle.\n3. Poked RUL mass (First lobe).\n4. Poked LUL nodule (Second lobe).\nDiagnosis: Adeno CA.",
            5: "doing staging for linda chang she has rul cancer but also a lul nodule. did the ebus first got the lymph nodes. then used the needle on the rul mass. then went to the left side and needled the lul nodule too. positive for cancer.",
            6: "Bronchoscopy with EBUS and conventional TBNA performed. EBUS sampling of stations 4R, 7, and 4L completed. Conventional transbronchial needle aspiration performed on RUL mass (initial lobe). Conventional TBNA then performed on LUL nodule (additional lobe).",
            7: "[Indication]\nRUL Adeno, Staging.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS: 4R, 7, 4L sampled.\nTBNA: RUL mass sampled (31629).\nTBNA: LUL nodule sampled (31633).\n[Plan]\nOncology referral.",
            8: "We performed a procedure to stage Ms. Chang's lung cancer. First, we used an ultrasound scope to check the lymph nodes in the center of her chest. Then, we used a needle to take samples directly from the main tumor in her right lung. We also saw a spot on her left lung and used the needle to sample that one as well to see if the cancer had spread there.",
            9: "Procedure: Endobronchial ultrasound and multi-lobar needle aspiration.\nAction: Lymph nodes sampled via EBUS. RUL mass aspirated (primary parenchymal target). LUL nodule aspirated (secondary parenchymal target)."
        },
        # Category 5: BLVR Add-on (31647, +31651) - Case 0: Harold Johnson
        (5, 0): {
            1: "Indication: LUL Emphysema.\nProcedure: Valve Placement (4 valves).\n- 31647: LB1+2 (Initial).\n- 31651: LB3 (Add'l).\n- 31651: LB4 (Add'l).\n- 31651: LB5 (Add'l).\nResult: Total occlusion LUL.",
            2: "PROCEDURE: Bronchoscopic Lung Volume Reduction.\nTARGET: Left Upper Lobe.\nDETAILS: The airway was sized. The first valve (Zephyr 5.5) was deployed in the apicoposterior segment (Initial Lobe, 31647). Subsequently, valves were deployed in the Anterior, Superior Lingula, and Inferior Lingula segments (Each additional bronchus, 31651 x3). Complete lobar occlusion was verified visually.",
            3: "Billing Codes:\n- 31647 (1 unit): Initial bronchus valve placement (LB1+2).\n- 31651 (3 units): Additional bronchus valve placements (LB3, LB4, LB5).\nNote: Procedure performed in LUL. Four distinct segmental bronchi treated.",
            4: "Procedure: BLVR LUL\nSteps:\n1. Chartis negative.\n2. Placed valve in LB1+2 (First).\n3. Placed valve in LB3 (Add-on).\n4. Placed valve in LB4 (Add-on).\n5. Placed valve in LB5 (Add-on).\nAll valves look good.",
            5: "harold johnson here for valve placement lul. chartis was good. put the first valve in the top segment. then put three more in the other segments to block the whole lobe. four valves total. patient woke up fine.",
            6: "Bronchoscopic lung volume reduction performed on Left Upper Lobe. Initial valve placed in LB1+2. Additional valves placed in LB3, LB4, and LB5. Total of 4 Zephyr valves deployed. Complete occlusion achieved.",
            7: "[Indication]\nSevere Emphysema, LUL target.\n[Anesthesia]\nGeneral.\n[Description]\nValves placed:\n1. LB1+2 (31647)\n2. LB3 (31651)\n3. LB4 (31651)\n4. LB5 (31651)\n[Plan]\nAdmit for obs.",
            8: "We treated Mr. Johnson's emphysema by blocking off the diseased upper left part of his lung. We placed a total of four one-way valves. The first one went into the top segment, and then we placed three more in the remaining segments of that lobe to make sure no air could get in. This should help the healthier parts of his lung work better.",
            9: "Procedure: Deployment of bronchial flow-control devices.\nTarget: LUL.\nAction: Primary device anchored in LB1+2. Supplemental devices anchored in LB3, LB4, and LB5.\nOutcome: Lobar isolation."
        },
        # Category 6: Image Guided Drainage (32557) - Case 0: Patricia Moore
        (6, 0): {
            1: "Indication: Loculated R effusion.\nProcedure: US-guided pigtail placement (32557).\n- US loc: 7th ICS.\n- Seldinger technique.\n- 14Fr catheter placed.\n- 850mL turbid fluid drained.\nComplications: None.",
            2: "PROCEDURE NOTE: Percutaneous Pleural Drainage with Imaging Guidance.\nINDICATION: Complex parapneumonic effusion, Right.\nDESCRIPTION: Under real-time ultrasound guidance, the effusion was localized. A needle was advanced into the fluid pocket. A guidewire was passed, the tract dilated, and a 14Fr indwelling catheter was inserted. 850mL of purulent fluid was evacuated. Placement was confirmed via ultrasound.",
            3: "Code: 32557.\nDescription: Pleural drainage with insertion of indwelling catheter, with imaging guidance.\nMethod: Ultrasound used for access and placement confirmation.\nDevice: 14Fr Pigtail.\nOutput: 850mL.",
            4: "Procedure: Chest Tube with US\nSteps:\n1. US to find spot (Right 7th intercostal).\n2. Numbed skin.\n3. Needle -> Wire -> Dilator -> Tube.\n4. Hooked up to pleur-evac.\n5. Drained pus.\nCatheter stays in.",
            5: "patricia moore needs a drain for right side empyema. brought ultrasound in saw the pocket. put a pigtail in using the wire technique. got a lot of junk out like 850ml. stitched it in place. us shows it looks good.",
            6: "Ultrasound-guided pleural drainage performed on right hemithorax. 14Fr pigtail catheter inserted using Seldinger technique under continuous imaging. 850mL turbid fluid removed. Catheter secured.",
            7: "[Indication]\nComplex R effusion.\n[Anesthesia]\nLocal + Moderate Sedation.\n[Description]\nUS guidance used. 14Fr catheter inserted into right pleural space. 850mL drained.\n[Plan]\nConnect to suction. Antibiotics.",
            8: "Ms. Moore had a pocket of infected fluid around her right lung that needed draining. Using an ultrasound machine to guide us, we placed a small tube through her back and into the fluid. We drained about 850mL of cloudy fluid and left the tube in place to keep draining it.",
            9: "Procedure: Image-directed thoracostomy.\nAction: Utilizing sonographic visualization, a drainage conduit was introduced into the right pleural cavity. Purulent collection was evacuated."
        },
        # Category 7: Stent Revision (31638) - Case 0: Frank Anderson
        (7, 0): {
            1: "Indication: Migrated LMS stent.\nProcedure: Rigid bronchoscopy with Stent Revision (31638).\n- Stent found protruding into trachea.\n- Granulation tissue debrided.\n- Stent grasped and pushed distal into LMS.\n- Position confirmed.\nPatency restored.",
            2: "OPERATIVE REPORT: Bronchoscopic Revision of Airway Prosthesis.\nINDICATION: Dyspnea secondary to proximal migration of Left Mainstem Stent.\nPROCEDURE: Rigid bronchoscopy revealed the Ultraflex stent extending into the distal trachea. Using rigid forceps, the prosthesis was mobilized. It was successfully repositioned distally into the left mainstem bronchus. Airway patency was fully restored, and the stent is now seated appropriately.",
            3: "Code: 31638 (Revision of tracheal/bronchial stent).\nTarget: Left Mainstem Bronchus.\nAction: Repositioning of migrated SEMS.\nNote: Includes debridement of granulation tissue facilitating the revision.",
            4: "Procedure: Stent Revision\nSteps:\n1. Rigid scope inserted.\n2. Saw stent sticking out of LMS.\n3. Cleaned up tissue.\n4. Grabbed stent and pushed it back in.\n5. Checked with flex scope, looks open.",
            5: "frank anderson has a stent in the left lung that moved up. went in with the rigid scope. saw it blocking the trachea a bit. grabbed it with the big forceps and shoved it back down where it belongs. looks good now breathing better.",
            6: "Rigid bronchoscopy performed for migrated left mainstem stent. Stent found extending into trachea. Granulation tissue removed. Stent grasped and repositioned distally into proper position within the left mainstem. Airway patent.",
            7: "[Indication]\nMigrated LMS Stent, obstruction.\n[Anesthesia]\nGeneral/Jet Ventilation.\n[Description]\nStent protruding into trachea. Repositioned into LMS using rigid forceps. Granulation tissue treated.\n[Plan]\nPACU then home.",
            8: "Mr. Anderson's airway stent had slipped out of place and was blocking his windpipe. We put him to sleep and used a metal tube to reach the stent. We carefully grabbed it and moved it back down into the left lung's airway where it is supposed to be. His breathing passage is now wide open again.",
            9: "Procedure: Readjustment of endobronchial prosthesis.\nIssue: Proximal migration.\nAction: The prosthesis was manipulated and reseated within the left mainstem bronchus. Patency was re-established."
        }
    }
    return variations

def main():
    # Load source data
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return

    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through categories in the source file
    for cat_idx, category in enumerate(source_data):
        # Iterate through cases in each category
        for case_idx, original_case in enumerate(category.get('cases', [])):
            
            # Check if we have manually crafted variations for this specific case
            # If not, we skip (or could implement generic fallback, but here we strictly follow the manual map)
            if (cat_idx, case_idx) not in variations_text:
                continue
                
            record = base_data[(cat_idx, case_idx)]
            orig_age = record['orig_age']
            
            # Generate 9 variations
            for style_num in range(1, 10):
                note_entry = copy.deepcopy(original_case)
                
                # Randomized Data
                new_age = orig_age + random.randint(-3, 3)
                rand_date_obj = generate_random_date(2025, 2025)
                rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
                new_name = record['names'][style_num - 1]
                
                # Apply Text Variation
                note_entry["note_text"] = variations_text[(cat_idx, case_idx)][style_num]
                
                # Apply Metadata Updates
                if "registry_entry" in note_entry:
                    reg = note_entry["registry_entry"]
                    if "patient_mrn" in reg:
                        reg["patient_mrn"] = f"{reg['patient_mrn']}_syn_{style_num}"
                    if "procedure_date" in reg:
                        reg["procedure_date"] = rand_date_str
                    if "patient_demographics" in reg:
                        reg["patient_demographics"]["age_years"] = new_age
                        # Note: We don't change gender here as names are gender-specific in mocks
                        
                # Add Synthetic Metadata
                note_entry["synthetic_metadata"] = {
                    "source_file": SOURCE_FILE,
                    "original_category_index": cat_idx,
                    "original_case_index": case_idx,
                    "style_type": style_num,
                    "generated_name": new_name,
                    "generation_date": datetime.datetime.now().isoformat()
                }
                
                generated_notes.append(note_entry)

    # Output
    output_filename = output_dir / "synthetic_notes_part_093.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()