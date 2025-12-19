import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_058.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations for Part 058.
    # Structure: Note_Index (0-6) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Note 022: Oliver Smith (Complicated Effusion, Fibrinolysis)
            1: "Procedure: Intrapleural fibrinolysis (Day 3).\nAction: Instilled 10mg tPA / 5mg DNase via left chest tube.\nStatus: Tube clamped. Dwell time 1 hr scheduled.\nPlan: Unclamp, monitor I/O, daily CXR.",
            2: "PROCEDURE NOTE: Administration of Intrapleural Fibrinolytic Agents.\nINDICATION: This 39-year-old male with a complicated parapneumonic effusion requires ongoing fibrinolytic therapy to facilitate drainage.\nDESCRIPTION: Under sterile conditions, the existing left-sided thoracostomy tube was accessed. A solution containing 10 mg tissue plasminogen activator (tPA) and 5 mg DNase was instilled into the pleural space without resistance. This represents dose #3 in the protocol.\nPLAN: The tube will remain clamped for 60 minutes to ensure adequate dwell time, followed by gravity drainage. We will continue strict input/output monitoring and obtain daily chest radiography to assess for resolution of loculations.",
            3: "CPT Justification: 32562 (Instillation of fibrinolytic agent, subsequent day).\nTechnique:\n1. Identification of existing chest tube (left side).\n2. Preparation of agents (tPA/DNase).\n3. Instillation via catheter.\n4. Clamping of tube.\nMedical Necessity: Treatment of multiloculated effusion (complicated). Dose #3 in series.",
            4: "Resident Procedure Note\nPatient: Oliver Smith\nProcedure: Fibrinolysis Instillation\nAttending: Dr. Shepherd\nSteps:\n1. Verified patient and order (Dose #3).\n2. Accessed left chest tube.\n3. Instilled tPA/DNase cocktail.\n4. Clamped tube.\n5. Patient tolerated well.\nPlan: Unclamp in 1 hour. Monitor outputs.",
            5: "procedure note pt oliver smith here for his 3rd dose of the tpa dnase for the effusion. we put the meds in the left chest tube no issues really clamped it off told the nurse to open it in an hour. no bleeding or anything immediate patient feels fine. continue daily cxr thanks.",
            6: "Oliver Smith is a 39-year-old male presenting for subsequent instillation of fibrinolytic agents for a complicated effusion. Consent was obtained. The existing left chest tube was accessed. 10 mg tPA and 5 mg DNase were instilled as Dose #3. The patient tolerated the procedure well with no immediate complications. The tube was clamped for a 1-hour dwell time. Plan includes strict I/O monitoring and daily CXR.",
            7: "[Indication]\nComplicated pleural effusion requiring fibrinolysis.\n[Anesthesia]\nNone (Instillation via existing tube).\n[Description]\nLeft chest tube accessed. tPA (10mg) and DNase (5mg) instilled. Tube clamped.\n[Plan]\nUnclamp in 1 hr. Nursing protocol for flush. Daily CXR.",
            8: "The patient, a 39-year-old male, presented for the third scheduled dose of intrapleural fibrinolysis for his complicated effusion. After verifying the order, we instilled the tPA and DNase solution through the existing left chest tube. The procedure went smoothly without resistance. We clamped the tube immediately after instillation to allow the medication to dwell. The patient remained stable throughout.",
            9: "PROCEDURE: Infusion of fibrinolytic agents via thoracostomy tube.\nINDICATION: Complex pleural fluid collection.\nDETAILS: The left drainage catheter was utilized. We introduced the tPA/DNase mixture into the pleural cavity. The line was secured and occluded to permit medication soak. No adverse events occurred."
        },
        1: { # Note 023: Sarah Connor (Thoracentesis + Bronch/BAL)
            1: "Procedures: Left Thoracentesis, Bronchoscopy w/ BAL x3 (LUL, LLL, RML).\nThora: US guidance. 660ml serosanguinous fluid removed. No pneumo.\nBronch: Normal airway. BAL performed in 3 distinct lobes. Samples sent.\nComplications: None.",
            2: "OPERATIVE REPORT: Diagnostic Bronchoscopy and Thoracentesis.\nINDICATION: Evaluation of pleural effusion and multifocal lung opacities.\nNARRATIVE: The patient was positioned for thoracentesis. Ultrasound of the left hemithorax confirmed a moderate effusion. Under ultrasound guidance, a catheter was introduced into the 7th intercostal space, yielding 660 mL of serosanguinous fluid. Post-procedure ultrasound showed resolution of fluid and lung sliding. The patient was then transitioned to the supine position for bronchoscopy. The airways were inspected and found to be patent. To evaluate the multifocal opacities, bronchoalveolar lavage was performed in three separate lobes: the Apical-Posterior segment of the LUL, the Anteromedial segment of the LLL, and the Lateral segment of the RML. Specimens were submitted for microbiology and cytology.",
            3: "Coding Summary:\n- 32555: Thoracentesis with imaging guidance (Left side, 660ml removed).\n- 76604-50: Bilateral Chest Ultrasound (Diagnostic findings documented for both Right and Left hemithoraces).\n- 31624-22: Bronchoscopy with BAL. Modifier 22 applied for extensive work involving 3 distinct sites (LUL, LLL, RML).",
            4: "Procedure: Thoracentesis & Bronchoscopy\nStaff: Dr. Cox\nSteps (Thora):\n1. US check: Left effusion seen.\n2. Prepped/Draped.\n3. Needle inserted 7th ICS.\n4. Drained 660cc serosanguinous.\n5. Catheter removed.\nSteps (Bronch):\n1. Scope passed.\n2. Airway normal.\n3. BAL LUL (LB1/2).\n4. BAL LLL (LB7/8).\n5. BAL RML (RB4).\n6. Suctioned clear.",
            5: "note for sarah connor we did a thora and bronch today. for the thora we used ultrasound found fluid on the left stuck the needle in got about 660 ml of pinkish fluid out. then we did the bronchoscopy looked around everything looked okay. washed three spots the lul lll and rml sent all that to lab. patient did fine no issues woke up ok.",
            6: "Consent obtained for thoracentesis and bronchoscopy. Ultrasound showed moderate left effusion. Left thoracentesis performed with US guidance yielding 660 mL serosanguinous fluid. Post-proc US showed lung sliding. Bronchoscopy then performed. Airways normal. BAL performed in LUL (LB1/2), LLL (LB7/8), and RML (RB4). Fluid sent for analysis. Tolerated well.",
            7: "[Indication]\nPleural effusion and lung nodules.\n[Anesthesia]\nLocal (Lidocaine) for thora; MAC for bronch.\n[Description]\n1. US Guided Left Thoracentesis: 660mL removed.\n2. Bronchoscopy: Normal anatomy. BAL x3 (LUL, LLL, RML).\n[Plan]\nCXR. Follow up fluid/cytology results.",
            8: "We began with the left thoracentesis. Using ultrasound to locate the pocket, we successfully drained 660 mL of fluid from the left pleural space. Once that was secured, we proceeded to the bronchoscopy under MAC anesthesia. The scope revealed normal airway anatomy. We performed lavages in the LUL, LLL, and RML to thoroughly sample the multifocal opacities seen on CT. The patient tolerated both procedures well.",
            9: "Operation: Pleural aspiration and airway inspection with lavage.\nDetails: Ultrasound visualization directed the drainage of the left pleural space. 660 mL was extracted. Subsequently, the endoscope was utilized to inspect the bronchial tree. Lavage was executed in three separate lobar segments. All samples were dispatched for analysis."
        },
        2: { # Note 024: Bruce Wayne (Trach Change, Bronch)
            1: "Procedure: Tracheobronchoscopy, Trach Tube Change.\nFindings: Tracheomalacia (dynamic collapse), worse on left.\nAction: Old tube removed. Stoma patent. New Shiley 7.0 XLT placed.\nComplications: None.",
            2: "PROCEDURE: Bronchoscopic Airway Inspection and Tracheostomy Exchange.\nINDICATION: Respiratory failure and evaluation of airway dynamics.\nFINDINGS: Upon inspection via the tracheostomy, excessive dynamic airway collapse (tracheomalacia) was observed, necessitating increased PEEP. The collapse was more pronounced in the left bronchial tree. The mucosal surfaces appeared healthy. Following the exam, the existing Shiley tracheostomy tube was removed. The stoma was widely patent with no granulation tissue. A fresh Shiley Proximal XLT 7.0 mm cuffed tube was inserted without difficulty and the cuff inflated.",
            3: "Billing Codes:\n- 31615: Tracheobronchoscopy (Visualized airway through stoma).\n- 31899: Unlisted procedure (Tracheostomy change in established tract). Note: 31502 not used as tract is established/mature.\njustification: Airway dynamics assessed (malacia), requiring bronchoscopic view during exchange.",
            4: "Resident Note\nPatient: Bruce Wayne\nProcedure: Bronch + Trach Change\nSteps:\n1. Time out.\n2. Scope through trach.\n3. Noted secretions and malacia (L > R).\n4. Deflated cuff, removed old trach.\n5. Placed new Shiley 7.0 XLT.\n6. Confirmed position.\nPlan: Routine trach care.",
            5: "did a bronch and trach change on mr wayne. looked down the tube first saw a lot of collapse especially on the left side. mucosa looked ok though. pulled the old shiley out and put a new one in same size 7.0 xlt. went in easy no bleeding. patient tolerated it fine.",
            6: "Bruce Wayne 58M. Indication: Respiratory failure. Bronchoscopy performed through tracheostomy. Findings: Excessive dynamic airway collapse noted, left greater than right. Secretions suctioned. Tracheostomy tube exchange performed. Old tube removed. Stoma patent. New Shiley 7.0 XLT placed. No complications.",
            7: "[Indication]\nRespiratory failure, airway evaluation.\n[Anesthesia]\nGeneral.\n[Description]\nBronchoscopy via trach showed tracheomalacia. Old trach removed. New Shiley 7.0 XLT inserted.\n[Plan]\nFollow up trach change in 3 months.",
            8: "We inspected the airway through the existing tracheostomy tube. Significant dynamic airway collapse was noted, particularly on the left side, which required higher PEEP settings to maintain patency. After clearing secretions, we proceeded to exchange the tracheostomy tube. The old tube was removed, revealing a healthy stoma. The new Shiley XLT 7.0 was placed smoothly.",
            9: "Procedure: Airway visualization and cannula exchange.\nFindings: Significant tracheomalacia observed.\nAction: The indwelling cannula was extracted. A replacement Shiley 7.0 XLT was inserted into the mature tract. Verification of position was completed."
        },
        3: { # Note 025: Diana Prince (EBUS Station 7)
            1: "Procedure: EBUS-TBNA Station 7.\nFindings: Station 7 node enlarged (28.5mm), stiff on elastography.\nAction: 6 passes w/ 22G needle.\nROSE: Malignant.\nComplications: None.",
            2: "OPERATIVE REPORT: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA).\nINDICATION: Mediastinal lymphadenopathy.\nDETAILS: The airway was inspected and found to be normal. The EBUS scope was introduced. The subcarinal lymph node (Station 7) was identified, measuring 28.5 mm. Elastography demonstrated a Type 3 (stiff) pattern, highly suspicious for malignancy. Six transbronchial needle aspiration passes were performed using a 22-gauge needle. Rapid On-Site Evaluation (ROSE) confirmed adequate cellularity and was suggestive of malignancy.",
            3: "Coding Data:\n- 31652: EBUS sampling of 1-2 stations (Station 7 sampled).\n- 22G needle used.\n- 6 passes performed.\n- Guidance: Ultrasound with elastography used to target stiffest area.\n- Diagnosis: Malignancy confirmed on ROSE.",
            4: "Procedure: EBUS\nAttending: Dr. Cameron\nSteps:\n1. White light bronch: Normal.\n2. EBUS scope inserted.\n3. Identified Station 7 (Subcarinal).\n4. Sampled x6 with 22G needle.\n5. ROSE: Positive.\nPlan: Await final path.",
            5: "procedure note for diana prince ebus today. airway looked normal. went to station 7 the subcarinal node it was big like 2.8 cm. looked blue on the stiffness scan so we sampled it 6 times. cytology came back saying it looks like cancer. patient woke up fine going to recovery.",
            6: "Indication: Mediastinal adenopathy. General anesthesia. Airway inspection normal. EBUS performed. Station 7 (subcarinal) identified, 28.5mm, hypermetabolic. Elastography Type 3 (stiff). TBNA x 6 passes with 22G needle. ROSE: Malignant. No complications.",
            7: "[Indication]\nMediastinal lymphadenopathy.\n[Anesthesia]\nGeneral.\n[Description]\nStation 7 lymph node visualized via EBUS. Elastography showed stiffness. 6 biopsies taken. ROSE positive for malignancy.\n[Plan]\nDischarge. Oncology referral pending final path.",
            8: "After ensuring the airway was clear with a standard inspection, we switched to the linear EBUS scope. We targeted the subcarinal lymph node (Station 7), which appeared enlarged and stiff on elastography. We performed six needle aspirations to ensure a good sample. The pathologist in the room confirmed the presence of malignant cells on the preliminary slides.",
            9: "Procedure: Sonographic airway evaluation and nodal sampling.\nTarget: Station 7 (Subcarinal).\nAction: The lesion was interrogated with ultrasound. Needle aspiration was executed six times. Preliminary analysis indicates carcinoma."
        },
        4: { # Note 026: Ellen Ripley (EBUS 11L, 4R + Cryo)
            1: "Procedures: EBUS-TBNA (11L, 4R), EBUS-Cryo (4R), BAL (RML), EBBx (RUL).\nFindings: Malignant cells in 11L and 4R.\nSpecimens: BAL, RUL mucosal bx, 11L needle bx, 4R needle + cryo bx.\nComplications: None.",
            2: "OPERATIVE SUMMARY: Complex Bronchoscopy with Multimodal Staging.\nINDICATION: Pulmonary nodularity and mediastinal adenopathy.\nPROCEDURE: Airway inspection revealed nodules in the distal trachea and right lung; a biopsy was taken from the RUL. BAL was performed in the RML. EBUS staging was then undertaken. Station 11L was sampled (TBNA x7) showing malignancy with necrosis. Station 4R was also sampled (TBNA x6) and found to be malignant. To maximize tissue yield for molecular testing, transbronchial cryobiopsies were also obtained from the 4R node. All samples were submitted for pathology.",
            3: "Coding Codes:\n- 31652: EBUS sampling 1-2 nodes (11L, 4R).\n- 31625: Bronchoscopy with bronchial biopsy (RUL lesion).\n- 31624: Bronchoscopy with BAL (RML).\n- Note: Cryobiopsy of lymph node is bundled into EBUS sampling codes (31652).",
            4: "Resident Note\nPatient: Ellen Ripley\nProcedure: EBUS + Biopsy\nSteps:\n1. Airway exam: Nodules seen.\n2. BAL RML.\n3. Forceps biopsy RUL nodule.\n4. EBUS 11L: TBNA x7 (Positive).\n5. EBUS 4R: TBNA x6 (Positive) + Cryo biopsy.\nPlan: Oncology consult.",
            5: "ellen ripley here for staging. we looked around saw some bumps in the rul so we biopsied that. washed the rml. then used the ultrasound scope. 11l node looked mixed stiff and soft sampled it 7 times came back cancer. 4r node same thing sampled it with needle and the cryo probe to get more tissue. rose said cancer for both. all good.",
            6: "Bronchoscopy performed. Mucosal nodules noted in RUL/Trachea. RUL biopsy taken. RML BAL performed. EBUS staging: 11L sampled (Positive). 4R sampled (Positive). 4R also biopsied with cryoprobe for larger sample. Patient tolerated well.",
            7: "[Indication]\nLung nodules and adenopathy.\n[Anesthesia]\nGeneral.\n[Description]\n1. RML BAL.\n2. RUL Endobronchial Biopsy.\n3. EBUS-TBNA of 11L and 4R.\n4. EBUS-Cryobiopsy of 4R.\n[Plan]\nFollow up pathology results.",
            8: "We performed a comprehensive evaluation. First, we cleared secretions and performed a lavage in the RML. We noticed nodularity in the RUL and took a standard forceps biopsy. Moving to the mediastinal staging, we used EBUS to locate and sample nodes 11L and 4R. Both showed malignancy on rapid evaluation. We utilized a cryoprobe on the 4R node to obtain a larger core of tissue for genetic testing.",
            9: "Procedure: Airway survey, lavage, and nodal staging.\nActions: Lavage of RML. Structural biopsy of RUL. Sonographic aspiration of nodes 11L and 4R. Cryo-extraction of tissue from node 4R.\nResult: Malignancy confirmed in nodal stations."
        },
        5: { # Note 027: Tony Stark (Nav Bronch + EBUS)
            1: "Procedures: Ion Nav Bronch (RLL Nodule), Radial EBUS, EBUS-TBNA (11L), BAL.\nNodule: RLL (RB8), 2cm. Concentric r-EBUS view. Samples: Needle, Cryo, Brush.\nNodes: 11L sampled (benign/reactive).\nComplications: None.",
            2: "OPERATIVE REPORT: Robotic-Assisted Navigational Bronchoscopy and EBUS Staging.\nINDICATION: Evaluation of solitary RLL pulmonary nodule.\nDETAILS: A virtual pathway was generated and loaded into the Ion robotic platform. The catheter was navigated to the RLL (RB8) target. Radial EBUS confirmed a concentric view of the lesion. Cone Beam CT (Cios Spin) was utilized to refine 3D positioning. The lesion was sampled via TBNA (x5), Cryobiopsy (x6), and Brushing. ROSE suggested malignancy. Mediastinal staging was performed via linear EBUS; station 11L was sampled.",
            3: "Coding Breakdown:\n- 31629: Primary code for Transbronchial Needle Aspiration (RLL nodule).\n- 31652: EBUS sampling (11L).\n- 31624: BAL (RLL).\n- +31627: Navigational Bronchoscopy add-on.\n- +31654: Radial EBUS add-on.\nRationale: 31629 chosen as primary over 31628 (biopsy) per hierarchy, though cryo was performed.",
            4: "Procedure: Ion Bronch\nTarget: RLL Nodule\nSteps:\n1. Registration.\n2. Navigated to RLL.\n3. r-EBUS: Concentric.\n4. Spin CT: Confirmed tool in lesion.\n5. Samples: Needle, Cryo, Brush -> ROSE Positive.\n6. EBUS: Sampled 11L.\n7. BAL RLL.\nPlan: Follow up.",
            5: "tony stark here for the lung nodule. used the robot to get out to the rll. radial ebus showed we were right in the middle of it. did a spin ct to be sure. took a bunch of samples with the needle and the cryo probe rose said it looks like cancer. checked the lymph nodes too sampled 11l. washed the lobe. done.",
            6: "Robotic bronchoscopy (Ion) performed for RLL nodule (2.0 cm). Navigation successful. Radial EBUS: Concentric. Cone Beam CT: Confirmed location. Sampling: TBNA, Cryobiopsy, Brush. ROSE: Malignant. EBUS staging: 11L sampled. BAL performed. No complications.",
            7: "[Indication]\nSolitary lung nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to RLL nodule using Ion. Confirmed with Radial EBUS/Cone Beam CT. Biopsied (Needle/Cryo). Staged mediastinum (11L).\n[Plan]\nOncology referral.",
            8: "We utilized the Ion robotic platform to navigate to the target lesion in the right lower lobe. Confirmation was achieved using both radial EBUS, which showed a concentric signal, and Cone Beam CT spin. We obtained extensive samples using needles and a cryoprobe. Preliminary pathology was positive for malignancy. We also staged the mediastinum by sampling the 11L lymph node using linear EBUS.",
            9: "Procedure: Computer-assisted bronchoscopy and staging.\nTarget: RLL lesion.\nMethods: Robotic navigation, sonographic confirmation, tomographic spin.\nSampling: Aspiration, cryo-extraction, brushing.\nStaging: Nodal sampling of station 11L."
        },
        6: { # Note 028: Natasha Romanoff (Lung Mass + EBUS)
            1: "Procedures: EBUS-TBNA (11L, LLL Mass), LLL Brush, BAL.\nFindings: LLL Mass is station 12L equivalent. Malignant.\n11L: Lymphocytes.\nComplications: Moderate bleeding, controlled.",
            2: "OPERATIVE NOTE: Diagnostic Bronchoscopy and EBUS.\nINDICATION: Left lower lobe lung mass.\nPROCEDURE: The airway was inspected; narrowing was noted in the LLL. EBUS was used to characterize and sample station 11L (benign) and the LLL mass itself (treated as station 12L/mass). The mass was hypermetabolic and sampling confirmed malignancy. A protected cytology brush and BAL were also performed in the LLL lateral basal segment. Hemostasis was achieved after moderate bleeding.",
            3: "Coding Logic:\n- 31652: EBUS sampling 1-2 nodes. (Covers 11L and the Mass which was sampled via EBUS needle).\n- 31623: Bronchial Brushing (LLL).\n- 31624: BAL (RLL - distinct lobe from mass/brush? Note says RLL BAL performed, LLL brush. If BAL was RLL, it is distinct 31624. If LLL, bundled if diagnostic. Text says 'Bronchial alveolar lavage was performed at... RLL'. So 31624 is valid.)",
            4: "Resident Note\nPatient: Natasha Romanoff\nProcedure: EBUS + Brush\nSteps:\n1. Scope in.\n2. EBUS 11L: Benign.\n3. EBUS LLL Mass: Malignant.\n4. Brush LLL (LB9).\n5. BAL RLL.\n6. Suctioned blood.\nPlan: Discharge.",
            5: "natasha romanoff for lung mass. looked down saw some narrowing in the lll. used the ebus to sample the 11l node and the mass itself. mass came back cancer. did a brush in the lll too. and washed the rll. there was some bleeding but we got it stopped. patient ok.",
            6: "Indication: Lung mass. General anesthesia. EBUS performed. Station 11L sampled (benign). LLL mass sampled via EBUS (malignant). LLL Brushing performed. RLL BAL performed. Moderate bleeding controlled. Extubated stable.",
            7: "[Indication]\nLung mass.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA of 11L and LLL Mass. Brushing of LLL. BAL of RLL.\n[Plan]\nOncology referral.",
            8: "We performed an EBUS procedure to sample a large mass in the left lower lobe. We also sampled the 11L node. The mass was positive for malignancy. Additionally, we performed a bronchial brushing in the LLL and a lavage in the RLL to screen for other pathology. Moderate bleeding was encountered but managed successfully.",
            9: "Procedure: Sonographic needle aspiration and bronchial sampling.\nTargets: Nodal station 11L, Pulmonary mass.\nAction: Needle aspiration of targets. Cytologic brushing of LLL. Lavage of RLL.\nResult: Mass confirmed as malignant."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the requested output format.
    # We assign a list of 9 mock names for each of the 7 original patients.
    
    # Original Data from file:
    # 022: Oliver Smith, 39
    # 023: Sarah Connor, 61
    # 024: Bruce Wayne, 58
    # 025: Diana Prince, 63
    # 026: Ellen Ripley, 66
    # 027: Tony Stark, 71
    # 028: Natasha Romanoff, 75
    
    return [
        {"idx": 0, "orig_name": "Oliver Smith", "orig_age": 39, "names": ["James T. Kirk", "Jean-Luc Picard", "Benjamin Sisko", "Kathryn Janeway", "Jonathan Archer", "Christopher Pike", "Michael Burnham", "Saru", "Spock"]},
        {"idx": 1, "orig_name": "Sarah Connor", "orig_age": 61, "names": ["Leia Organa", "Padme Amidala", "Rey Skywalker", "Jyn Erso", "Ahsoka Tano", "Hera Syndulla", "Sabine Wren", "Mon Mothma", "Rose Tico"]},
        {"idx": 2, "orig_name": "Bruce Wayne", "orig_age": 58, "names": ["Clark Kent", "Barry Allen", "Arthur Curry", "Victor Stone", "Hal Jordan", "Oliver Queen", "John Jones", "Billy Batson", "Carter Hall"]},
        {"idx": 3, "orig_name": "Diana Prince", "orig_age": 63, "names": ["Wanda Maximoff", "Carol Danvers", "Natasha Rushman", "Yelena Belova", "Kate Bishop", "Jennifer Walters", "Kamala Khan", "Monica Rambeau", "Hope Van Dyne"]},
        {"idx": 4, "orig_name": "Ellen Ripley", "orig_age": 66, "names": ["Laurie Strode", "Sidney Prescott", "Nancy Thompson", "Gale Weathers", "Sally Hardesty", "Alice Hardy", "Ginny Field", "Julie James", "Kirby Reed"]},
        {"idx": 5, "orig_name": "Tony Stark", "orig_age": 71, "names": ["Steve Rogers", "Thor Odinson", "Bruce Banner", "Clint Barton", "Scott Lang", "Stephen Strange", "T'Challa", "Peter Parker", "Sam Wilson"]},
        {"idx": 6, "orig_name": "Natasha Romanoff", "orig_age": 75, "names": ["Dana Scully", "Clarice Starling", "Olivia Benson", "Temperance Brennan", "Meredith Grey", "Lisa Cuddy", "Miranda Bailey", "Cristina Yang", "Addison Montgomery"]}
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
            
            # Update the text content
            # Note: Input file uses "text_content", example used "note_text". 
            # We will update "text_content" as that is the schema of the input.
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["text_content"] = variations_text[idx][style_num]
            else:
                note_entry["text_content"] = f"Error: Text variation not found for Note {idx} Style {style_num}"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update Age
                if "patient_demographics" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                # Update Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN (if present, usually "UNKNOWN" in this set, but we set a synthetic one)
                note_entry["registry_entry"]["patient_mrn"] = f"SYN_{idx+1:03d}_{style_num}"

                # Update Name in INDICATION text (Basic string replace if name is found in original text)
                # Note: This is a simple heuristic. The "text_content" is already fully rewritten in the variations_text map
                # so we don't need to replace names there. We might need to replace names in other metadata fields if they exist.
                # In this specific dataset, names appear in "INDICATION FOR OPERATION" within the text, which we replaced entirely.
            
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
    output_filename = output_dir / "synthetic_part_058_variations.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()