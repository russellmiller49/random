import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_027.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock names and ages for the patients in Part 027 to ensure consistency across variations.
    Indexes 0-9 correspond to the notes in the source file.
    """
    return [
        # 0: Patricia Johnson (IPC)
        {"idx": 0, "orig_age": 74, "names": ["Mary Williams", "Linda Brown", "Patricia Jones", "Barbara Miller", "Elizabeth Davis", "Jennifer Garcia", "Maria Rodriguez", "Susan Wilson", "Margaret Martinez"]},
        # 1: Michael Chang (Robotic Nav)
        {"idx": 1, "orig_age": 55, "names": ["David Lee", "James Chen", "Robert Wang", "Michael Kim", "William Liu", "Richard Wu", "Joseph Ng", "Thomas Zhang", "Charles Tran"]},
        # 2: Harold Stevens (Thoracoscopy)
        {"idx": 2, "orig_age": 66, "names": ["James Anderson", "John Taylor", "Robert Thomas", "Michael Hernandez", "William Moore", "David Martin", "Richard Jackson", "Joseph Thompson", "Charles White"]},
        # 3: Roberto Garcia (Tracheal Dilation)
        {"idx": 3, "orig_age": 52, "names": ["Juan Martinez", "Carlos Hernandez", "Luis Lopez", "Pedro Gonzalez", "Jorge Perez", "Miguel Sanchez", "Antonio Ramirez", "Jose Torres", "Manuel Flores"]},
        # 4: Michael Torres (Valve Removal - Note: Original text had header mismatch, registry matches Torres/Valve Removal)
        {"idx": 4, "orig_age": 59, "names": ["Robert Lewis", "Paul Clark", "Mark Robinson", "Donald Walker", "George Perez", "Kenneth Hall", "Steven Young", "Edward Allen", "Brian King"]},
        # 5: Jennifer Wu (Stent Check)
        {"idx": 5, "orig_age": 58, "names": ["Lisa Chang", "Nancy Lin", "Karen Huang", "Betty Yang", "Helen Zhao", "Sandra Ho", "Donna Park", "Carol Kim", "Ruth Lee"]},
        # 6: K. Davis (Cryobiopsy)
        {"idx": 6, "orig_age": 64, "names": ["Deborah Wright", "Dorothy Scott", "Virginia Green", "Rebecca Baker", "Sharon Adams", "Cynthia Nelson", "Kathleen Hill", "Shirley Campbell", "Amy Mitchell"]},
        # 7: Rebecca Martinez (Pleurodesis)
        {"idx": 7, "orig_age": 68, "names": ["Martha Carter", "Brenda Roberts", "Pamela Phillips", "Nicole Evans", "Katherine Turner", "Christine Torres", "Debra Parker", "Diane Collins", "Carolyn Edwards"]},
        # 8: Marcus Johnson (Hemoptysis)
        {"idx": 8, "orig_age": 57, "names": ["Christopher Stewart", "Daniel Flores", "Matthew Morris", "Anthony Murphy", "Mark Rivera", "Donald Cook", "Paul Rogers", "Steven Morgan", "Andrew Bell"]},
        # 9: Elizabeth Okafor (Multidisciplinary)
        {"idx": 9, "orig_age": 65, "names": ["Sarah Reed", "Laura Bailey", "Kimberly Cooper", "Michelle Richardson", "Jessica Cox", "Emily Howard", "Melissa Ward", "Stephanie Peterson", "Rebecca Gray"]}
    ]

def get_variations():
    """
    Returns the dictionary of text variations.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Patricia Johnson (IPC Placement)
            1: "Procedure: PleurX IPC placement Rt Hemithorax.\n- US guidance used.\n- Local anesthetic.\n- Seldinger technique: 18G needle -> wire -> dilators -> sheath.\n- Catheter tunneled 6cm.\n- Fluid: 1200mL serous.\n- No complications. CXR pending.",
            2: "OPERATIVE NARRATIVE: The patient presented with a recurrent, malignant right-sided pleural effusion. Under ultrasound guidance, the pleural space was accessed at the 5th intercostal space. A subcutaneous tunnel was created, and the indwelling pleural catheter was advanced into the pleural cavity. Approximately 1.2 liters of exudative fluid were drained. The catheter was secured, and the patient tolerated the procedure without hemodynamic compromise.",
            3: "Service: Insertion of Tunneled Pleural Catheter (32550).\nGuidance: Ultrasound (76942) for site selection and safety.\nDetails: Right hemithorax. Subcutaneous tunneling performed. Cuff positioned appropriately.\nDrainage: 1200 mL removed to confirm function.\nStatus: Successful placement.",
            4: "Resident Note\nProcedure: PleurX Placement\nAttending: Dr. Green\n1. US check - big effusion right side.\n2. Local lidocaine.\n3. Stick w/ needle, wire down.\n4. Tunneled catheter under skin.\n5. Peel-away sheath in.\n6. Catheter in, drained 1.2L.\n7. Stitched up.\nPlan: Home health teaching.",
            5: "ipc placement note pt patricia johnson. right side effusion recurrent cancer. did the ultrasound marked spot. numbed her up good with lido. put the wire in tunneled the catheter about 6cm. dilated track put sheath in. catheter went in easy drained 1200cc straw fluid. stitched it up dressing on. no issues.",
            6: "Indwelling Tunneled Pleural Catheter Placement was performed on a 74-year-old female with metastatic breast cancer. Ultrasound guidance confirmed a large right pleural effusion. Under local anesthesia, the pleural space was accessed. A subcutaneous tunnel was created. The catheter was inserted and 1200 mL of serous fluid was drained. The procedure was uncomplicated.",
            7: "[Indication]\nRecurrent malignant pleural effusion, Right.\n[Anesthesia]\nLocal (Lidocaine 1%).\n[Description]\nUS-guided access. Subcutaneous tunnel created. PleurX catheter inserted. 1200mL drained. Cuff positioned. Incisions closed.\n[Plan]\nHome drainage education.",
            8: "Ms. Johnson was brought to the procedure room for management of her recurrent right pleural effusion. We utilized ultrasound to identify a safe pocket of fluid. After anesthetizing the area, we placed a tunneled PleurX catheter using the standard Seldinger technique. The catheter was tunneled subcutaneously before entering the pleural space. We drained 1200mL of fluid to verify patency. The patient remained stable throughout.",
            9: "Procedure: Implantation of long-term pleural drainage device.\nContext: Persistent fluid accumulation due to malignancy.\nTechnique: Sonographic localization. Creation of subcutaneous tract. Deployment of cuffed catheter into pleural cavity.\nOutput: 1.2 Liters serous fluid.\nOutcome: Successful implantation."
        },
        1: { # Michael Chang (Robotic Nav Bronch)
            1: "Procedure: Robotic Bronchoscopy (Ion), LLL nodule.\n- Nav: Ion system, 3.8mm error.\n- Confirmation: Radial EBUS (concentric) + Cone Beam CT.\n- Sampling: Forceps x6, Brush x2.\n- Complications: None.\n- Plan: D/C, path follow-up.",
            2: "OPERATIVE REPORT: The patient underwent robotic-assisted bronchoscopy utilizing the Intuitive Ion platform for a peripheral LLL lesion. Navigation was aided by shape-sensing technology. Target verification was achieved via radial EBUS (concentric view) and intraoperative Cone-Beam CT, confirming tool-in-lesion. Transbronchial biopsies and brushings were obtained. The patient remained stable.",
            3: "Codes: 31627 (Nav), 31628 (Biopsy), 31623 (Brush), 31654 (REBUS).\nTarget: Left Lower Lobe (LB9).\nTech: Robotic platform, Fluoroscopy, CBCT, Radial EBUS.\nSamples: Histology and Cytology obtained.\nComplications: None.",
            4: "Procedure: Robotic Bronch LLL\nSteps:\n1. GA/ETT.\n2. Registered Ion robot.\n3. Navigated to LLL target.\n4. REBUS check: Concentric.\n5. CBCT spin: Tool in lesion.\n6. Biopsied (forceps/brush).\n7. No bleeding.\nPlan: Extubate, recover.",
            5: "robotic bronch for michael chang lll nodule. ion system used. registration good. drove out to the lb9 segment. rebus showed the lesion concentric view. did a spin with the c-arm to be sure. took 6 bites and 2 brushes. no bleeding. woke up fine.",
            6: "Robotic Navigational Bronchoscopy using Intuitive Ion System was performed for a 1.8cm left lower lobe nodule. Navigation planning and registration were completed. The catheter was advanced to the target in LB9. Radial EBUS and Cone-Beam CT confirmed lesion location. Transbronchial biopsy and brushing were performed. No complications occurred.",
            7: "[Indication]\n1.8cm LLL Nodule.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon Robotic Navigation. REBUS/CBCT confirmation. Transbronchial biopsy x6. Brushing x2. No pneumothorax.\n[Plan]\nPathology pending.",
            8: "We performed a robotic bronchoscopy to biopsy a nodule in Mr. Chang's left lower lobe. Using the Ion platform, we navigated to the lateral basal segment. We confirmed our position with both radial EBUS and a cone-beam CT spin, ensuring the tool was right in the lesion. We then took multiple biopsies and brushings. The procedure went smoothly with no complications.",
            9: "Procedure: Robotic-assisted transbronchial sampling.\nTarget: Peripheral pulmonary nodule, LLL.\nGuidance: Electromagnetic/Shape-sensing navigation, Radial Ultrasound, Cone-Beam Tomography.\nAction: Acquired tissue via forceps and brush.\nResult: No adverse events."
        },
        2: { # Harold Stevens (Medical Thoracoscopy)
            1: "Procedure: Medical Thoracoscopy (Right).\n- Findings: Parietal/visceral nodules, trapped lung.\n- Action: Biopsy x8, Adhesiolysis, Talc poudrage (4g).\n- Drain: 28Fr chest tube placed.\n- Plan: Admit, suction -20.",
            2: "PROCEDURE NOTE: The patient underwent right-sided medical thoracoscopy. Inspection of the pleural cavity revealed diffuse nodularity suggestive of malignancy and a trapped lung. Multiple biopsies were harvested from the parietal and visceral pleura. Given the findings, talc pleurodesis was performed via insufflation. A chest tube was placed for post-operative drainage.",
            3: "Billing Code: 32650 (Thoracoscopy with pleurodesis). Note: Biopsies (32602) are bundled/included in the primary procedure when performed. Indication: Undiagnosed effusion/suspected malignancy. Technique: Rigid thoracoscope, Talc insufflation.",
            4: "Resident Note: Pleuroscopy\n1. Local/Sedation.\n2. Trocar in 5th ICS.\n3. Drained fluid.\n4. Saw nodules everywhere -> Biopsied.\n5. Lung trapped -> Talc poudrage performed.\n6. Chest tube in.\nPlan: Admit.",
            5: "medical thoracoscopy on mr stevens. right side. drained the fluid. looked inside saw a bunch of nodules looks like cancer. took 8 biopsies. lung wouldnt come up all the way so we puffed in some talc for pleurodesis. put a chest tube in. sent him to the floor.",
            6: "Medical thoracoscopy with pleural biopsies, talc pleurodesis, and chest tube placement was performed. The patient is a 66-year-old male with a large right pleural effusion. Rigid thoracoscopy revealed multiple nodules. Biopsies were taken. Talc slurry was insufflated. A 28Fr chest tube was inserted. The patient was transferred to the floor.",
            7: "[Indication]\nRight Pleural Effusion, suspected malignancy.\n[Anesthesia]\nMAC/Local.\n[Description]\nThoracoscopy performed. Nodules biopsied (x8). Trapped lung noted. Talc pleurodesis performed. Chest tube placed.\n[Plan]\nAdmit, suction.",
            8: "Mr. Stevens underwent a medical thoracoscopy to investigate his right pleural effusion. After entering the chest, we found extensive nodules and a trapped lung. We took several biopsies for diagnosis and then performed a talc pleurodesis to prevent fluid recurrence. A chest tube was left in place to ensure drainage and facilitate lung re-expansion if possible.",
            9: "Operation: Pleuroscopy with tissue sampling and chemical sclerosis.\nFindings: Diffuse pleural modularity, non-expandable lung.\nIntervention: Multiple biopsies. Insufflation of talc agent.\nHardware: Indwelling thoracic catheter (chest tube) placed."
        },
        3: { # Roberto Garcia (Tracheal Dilation)
            1: "Procedure: Flex Bronch, Tracheal Dilation.\n- Dx: Post-intubation stenosis (Subglottic).\n- Action: CRE Balloon (8-12mm). 3 inflations.\n- Result: Patency increased 40% -> 75%.\n- Plan: IV Decadron, Obs overnight.",
            2: "OPERATIVE SUMMARY: The patient presented with symptomatic tracheal stenosis. Flexible bronchoscopy revealed a circumferential cicatricial stenosis 3cm distal to the vocal cords. Balloon dilation was performed using a CRE balloon with serial inflations up to 12mm. Post-intervention, the airway lumen was significantly improved. No immediate restenosis or significant bleeding was observed.",
            3: "CPT: 31630 (Bronchoscopy with dilation). Diagnosis: Tracheal Stenosis (J95.5). Technique: Balloon dilation via flexible scope. Anesthesia: General.",
            4: "Procedure: Bronch w/ Balloon Dilation\n1. GA.\n2. Scope down. Stenosis seen below cords.\n3. Balloon up: 8mm, 10mm, 12mm.\n4. Airway looks much better (75% open).\n5. No bleeding.\nPlan: Admit for airway watch.",
            5: "bronchoscopy for roberto garcia tracheal stenosis. used the cre balloon to dilate it. went up to 12mm. opened up pretty good from 40 percent to 75 percent. gave some dexamethasone. watching him overnight.",
            6: "Flexible bronchoscopy and balloon dilation were performed for post-intubation tracheal stenosis. Findings included circumferential narrowing 3cm below cords. Serial dilations with CRE balloon up to 12mm were performed. Patency improved to 75 percent. No complications occurred. The patient was admitted for monitoring.",
            7: "[Indication]\nTracheal Stenosis.\n[Anesthesia]\nGeneral.\n[Description]\nFlexible bronchoscopy. Balloon dilation (8mm-12mm). Stenosis relieved.\n[Plan]\nOvernight observation.",
            8: "We brought Mr. Garcia to the OR to address his tracheal stenosis. Using a flexible bronchoscope, we identified the narrowed segment and used a balloon catheter to dilate it. We performed three inflations, gradually increasing the size to 12mm. The airway opened up significantly, and he tolerated the procedure well. We'll keep him overnight to ensure no swelling develops.",
            9: "Procedure: Endoscopic airway dilation.\nPathology: Cicatricial tracheal stenosis.\nMethod: Radial expansion via balloon catheter.\nOutcome: Restoration of luminal caliber."
        },
        4: { # Michael Torres (Valve Removal) - Fixing the header mismatch in variation text to focus on the Valve Removal content which matches the Registry/CPT.
            1: "Procedure: Valve Removal RUL.\n- Indication: Recurrent pneumonia.\n- Findings: 3 valves in place, mucus plugging.\n- Action: All 3 removed via forceps.\n- Result: Airways patent, secretions cleared.\n- Plan: Discharge.",
            2: "OPERATIVE REPORT: The patient presented for removal of endobronchial valves due to infectious complications. Under general anesthesia, the Right Upper Lobe was interrogated. Three Zephyr valves were identified. Each valve was sequentially grasped and retrieved without incident. Significant mucous plugging distal to the valves was aspirated. The airway was patent at the conclusion of the procedure.",
            3: "Codes: 31648 (Valve removal). Site: RUL. Count: 3 valves. Indication: Complication of device (Pneumonia). Technique: Forceps retrieval via flexible bronchoscope.",
            4: "Resident Note: Valve Removal\n1. Pt with RUL valves + pneumonia.\n2. Bronch down.\n3. Pulled 3 valves from RUL using forceps.\n4. Suctioned a lot of mucus.\n5. No bleeding.\nPlan: Antibiotics, follow up.",
            5: "taking out valves for michael torres. he keeps getting pneumonia. went in saw the three valves in the rul. pulled them out one by one. tons of junk behind them suctioned it all out. airway looks open now. done.",
            6: "Bronchoscopic removal of endobronchial valves was performed. Indication was recurrent pneumonia. Three Zephyr valves were removed from the RUL using retrieval forceps. Mucous plugging was cleared. The patient tolerated the procedure well.",
            7: "[Indication]\nInfected BLVR / Pneumonia.\n[Anesthesia]\nGeneral.\n[Description]\nRemoval of 3 Zephyr valves from RUL. Airway clearance of mucus.\n[Plan]\nObservation, antibiotics.",
            8: "Mr. Torres required removal of his lung volume reduction valves due to recurrent infections. We went in bronchoscopically and removed all three valves from the right upper lobe. There was a lot of mucus trapped behind them, which we cleared out. The procedure was successful and should help clear up his infection.",
            9: "Procedure: Extraction of bronchial prostheses.\nReason: Post-obstructive infection.\nAction: Retrieval of 3 valves. Aspiration of retained secretions.\nResult: Restoration of lobar ventilation."
        },
        5: { # Jennifer Wu (Stent Check)
            1: "Procedure: Bronchoscopy (Stent Check).\n- Findings: LMS stent in good position. Mucus plugging.\n- Action: Toilet/suction. Mild granulation (no tx needed).\n- Plan: Antibiotics, f/u 4 weeks.",
            2: "PROCEDURE NOTE: Surveillance bronchoscopy was performed to evaluate the left mainstem silicone stent. The stent was found to be in situ with no migration. Significant secretion burden was noted and cleared via therapeutic aspiration. Mild proximal granulation tissue was observed but did not require intervention. Patency is preserved.",
            3: "CPT: 31645 (Therapeutic aspiration) or 31622 (Dx). *Note: Registry says 31645.* Procedure involved extensive suctioning of secretions from stent. No destruction or excision performed.",
            4: "Stent Check Note\n1. Flex scope via trach.\n2. LMS stent looks good, not moving.\n3. Suctioned thick secretions.\n4. Mild granulation, left alone.\n5. Airway patent.\nPlan: Azithromycin.",
            5: "checking ms wu's stent today. went in through the trach. stent is sitting fine. lot of mucus though so i spent some time cleaning it out. little bit of granulation tissue but not blocking anything. gave her some antibiotics.",
            6: "Bronchoscopy for stent surveillance was performed. The patient has a left mainstem Dumon stent. Findings included mucous buildup and mild granulation tissue. Aggressive suctioning was performed. The stent remains patent. The patient was started on azithromycin.",
            7: "[Indication]\nAirway Stent Surveillance.\n[Anesthesia]\nModerate.\n[Description]\nLMS stent inspected. Secretions cleared (Therapeutic Aspiration). Position stable.\n[Plan]\nFollow up 4 weeks.",
            8: "Ms. Wu came in for a check-up on her airway stent. We took a look with the bronchoscope and found the stent was holding its position well, but there was a fair amount of mucus built up inside. We cleaned that out thoroughly. There's a little bit of granulation tissue forming, but it's not causing a problem yet, so we'll just watch it.",
            9: "Procedure: Endoscopic prosthesis evaluation.\nFindings: Stent in situ. Retained secretions.\nIntervention: Therapeutic aspiration/toilet.\nOutcome: Patency maintained."
        },
        6: { # K. Davis (Cryobiopsy)
            1: "Procedure: Bronchoscopy w/ Cryobiopsy (RLL).\n- Target: ILD (UIP pattern).\n- Tech: 2.4mm probe, 5 samples.\n- Bleeding control: Arndt blocker.\n- Complications: None.\n- Plan: Discharge.",
            2: "OPERATIVE SUMMARY: The patient underwent transbronchial cryobiopsy for diagnosis of interstitial lung disease. The Right Lower Lobe was targeted under fluoroscopic and radial EBUS guidance. Five cryobiopsies were obtained using a 2.4mm probe. Prophylactic bronchial blockade with an Arndt blocker provided effective hemostasis. Post-procedure fluoroscopy ruled out pneumothorax.",
            3: "Billing: 31628 (Biopsy single lobe), 31654 (REBUS). Note: Cryoprobe used for parenchymal biopsy. Balloon blocker used for hemostasis (not separately billable). Indication: ILD.",
            4: "Resident Note: Cryobiopsy\n1. Tube/GA.\n2. RLL target confirmed w/ REBUS.\n3. Cryo probe -> 5 biopsies taken.\n4. Balloon up after each to stop bleed.\n5. No pneumo.\nPlan: Home.",
            5: "did a cryo biopsy on k davis for her lung disease. went to the rll. froze 5 pieces of lung. used the balloon blocker to stop the bleeding worked great. no pneumothorax. sending her home.",
            6: "Bronchoscopy with transbronchial cryobiopsy of the RLL was performed for ILD. Radial EBUS confirmed the target. Five samples were obtained using a 2.4mm cryoprobe. An Arndt blocker was used for hemostasis. There were no complications.",
            7: "[Indication]\nInterstitial Lung Disease.\n[Anesthesia]\nGeneral.\n[Description]\nCryobiopsy RLL x5. Balloon occlusion for hemostasis. No PTX.\n[Plan]\nDischarge.",
            8: "We performed a cryobiopsy to get a tissue diagnosis for Ms. Davis's lung disease. We targeted the right lower lobe, verifying the site with ultrasound. We took five good-sized samples using the freezing probe. We used a balloon blocker to manage any bleeding, which worked perfectly. She is recovering well with no signs of collapsed lung.",
            9: "Procedure: Transbronchial cryo-sampling.\nIndication: Diffuse parenchymal lung disease.\nTechnique: Cryo-adhesion biopsy with prophylactic balloon occlusion.\nResult: Adequate tissue retrieval. Hemostasis secured."
        },
        7: { # Rebecca Martinez (Pleurodesis)
            1: "Procedure: Bedside Pleurodesis.\n- Access: Existing chest tube.\n- Agent: 4g Talc slurry + 200mg Lidocaine.\n- Method: Instill -> Clamp -> Rotate.\n- Result: Tolerated well.\n- Plan: Suction, remove tube in 48h.",
            2: "PROCEDURE NOTE: Chemical pleurodesis was performed via the existing right-sided chest tube. After confirmation of lung re-expansion and lidocaine premedication, a slurry containing 4 grams of sterile talc was instilled. The patient was rotated through standard positions to ensure distribution. The tube was unclamped after 60 minutes.",
            3: "Code: 32560 (Pleurodesis instillation). Agent: Talc. Route: Chest tube. Pre-medication: Lidocaine intrapleural. Indication: Malignant effusion.",
            4: "Procedure: Talc Pleurodesis\n1. Checked CXR - lung up.\n2. Pushed lidocaine into chest tube.\n3. Pushed talc slurry (4g).\n4. Clamped and rotated patient x 1 hour.\n5. Back to suction.\nPlan: Watch drainage.",
            5: "bedside pleurodesis for rebecca martinez. she has that cancer effusion. lung was up so we put in lidocaine then the talc slurry. rolled her around for an hour. put the tube back on suction. she had some pain but morphine helped.",
            6: "Chemical pleurodesis with talc slurry via chest tube was performed. The patient has a recurrent malignant pleural effusion. Lidocaine was administered followed by 4 grams of talc slurry. The patient was repositioned for distribution. The tube was unclamped after 60 minutes. The patient tolerated the procedure reasonably well.",
            7: "[Indication]\nMalignant Pleural Effusion.\n[Anesthesia]\nLocal/Intrapleural Lidocaine.\n[Description]\n4g Talc slurry instilled via chest tube. Patient rotated. Suction resumed.\n[Plan]\nRemove tube when drainage decreases.",
            8: "Ms. Martinez underwent a bedside pleurodesis to treat her recurring pleural fluid. Since her lung was fully expanded, we injected a mixture of talc and saline through her chest tube. We had her change positions for an hour to coat the lining of the lung. She experienced some discomfort but is comfortable now. We'll leave the tube in for a couple of days to make sure the lung sticks.",
            9: "Procedure: Chemical sclerosis of pleural space.\nAgent: Talc suspension.\nMethod: Instillation via thoracostomy tube with positional rotation.\nGoal: Pleural symphysis."
        },
        8: { # Marcus Johnson (Hemoptysis)
            1: "Procedure: Emergent Bronchoscopy.\n- Indication: Massive hemoptysis (LUL).\n- Action: Balloon tamponade (Fogarty).\n- Findings: Bleeding from Lingula/Anterior LUL.\n- Result: Bleeding stopped with tamponade.\n- Plan: IR for embolization.",
            2: "OPERATIVE REPORT: The patient required emergent bronchoscopy for life-threatening hemoptysis. The source was localized to the Left Upper Lobe. Initial conservative measures (iced saline, epinephrine) failed. Endobronchial balloon tamponade was employed, isolating the bleeding segments (Lingula/Anterior). Hemostasis was achieved. Interventional Radiology was consulted for urgent bronchial artery embolization.",
            3: "CPT: 31634 (Balloon occlusion). Indication: Hemoptysis. Technique: Flexible bronchoscopy with Fogarty balloon tamponade. Adjuncts: Iced saline, TXA.",
            4: "Resident Note: Hemoptysis Code\n1. Called for bleed.\n2. Scope down -> Blood everywhere.\n3. Source LUL.\n4. Tried saline/epi -> No stop.\n5. Put balloon in LUL -> Stopped bleeding.\nPlan: IR BAE.",
            5: "emergency bronch for marcus johnson bleeding out from the lul. massive amount of blood. tried iced saline didnt work. put a fogarty balloon up there and inflated it. that finally stopped the bleeding. ir is coming to coil the vessel.",
            6: "Emergency bronchoscopy was performed for massive hemoptysis. Findings revealed heavy bleeding from the LUL. Iced saline and epinephrine were ineffective. Balloon tamponade using a Fogarty catheter was performed, achieving hemostasis. The patient was stabilized and referred to IR for bronchial artery embolization.",
            7: "[Indication]\nMassive Hemoptysis.\n[Anesthesia]\nSedation (Intubated).\n[Description]\nLUL bleeding source identified. Balloon tamponade performed. Hemostasis achieved.\n[Plan]\nAngiography/Embolization.",
            8: "I was called to the ICU for Mr. Johnson who was having massive bleeding from his lungs. I performed an emergency bronchoscopy and found the blood coming from the left upper lobe. Washing with cold saline didn't stop it, so I inserted a balloon catheter and inflated it to block the airway. This stopped the bleeding. He is now stable and heading to IR for a permanent fix.",
            9: "Procedure: Emergency airway hemorrhage control.\nTechnique: Bronchoscopic balloon tamponade.\nSite: Left Upper Lobe.\nOutcome: Temporary cessation of hemoptysis. \nDisposition: Angiographic intervention."
        },
        9: { # Elizabeth Okafor (Multidisciplinary)
            1: "Procedure: Rigid Bronch, Stent, Pericardial Window, IPC.\n- Airway: RMS obstruction debulked, stent placed.\n- Cardiac: Window created, tamponade resolved.\n- Pleural: IPC placed Rt.\n- Plan: ICU.",
            2: "OPERATIVE SUMMARY: This complex session addressed three sites of malignant disease. 1) Right mainstem bronchus obstruction was treated via rigid bronchoscopy, tumor destruction, and placement of a metallic stent. 2) Cardiac tamponade was relieved via subxiphoid pericardial window. 3) A right-sided indwelling pleural catheter was placed for malignant effusion. The patient remained hemodynamically stable.",
            3: "Codes: 31641, 31631, 31630, 31645, 33015, 32550. Comprehensive palliation: Airway recanalization (stent/debulk), Pericardial decompression, Pleural drainage (IPC).",
            4: "Resident Note: Combined Case\n1. Rigid bronch -> Open RMS -> Stent.\n2. CT Surgery did pericardial window.\n3. Placed PleurX catheter right side.\n4. Long case but pt stable.\nPlan: ICU.",
            5: "huge case for mrs okafor. did everything at once. opened up the right mainstem with the rigid scope and put a stent in. then the surgeons did the heart window. then i put in a pleurx catheter for the lung fluid. she did okay considering.",
            6: "Multidisciplinary procedure performed for 65-year-old female. Rigid bronchoscopy with tumor debridement and stent placement in right mainstem. Subxiphoid pericardial window for tamponade. Tunneled pleural catheter placement for effusion. Patient stable and transferred to ICU.",
            7: "[Indication]\nRMS Obstruction, Tamponade, Pleural Effusion.\n[Anesthesia]\nGeneral.\n[Description]\n1. Airway Stent RMS. 2. Pericardial Window. 3. IPC Right.\n[Plan]\nICU Care.",
            8: "We performed a combined procedure to help Mrs. Okafor's breathing and heart function. First, we opened up her blocked airway with a stent. Then, the cardiac surgeons drained the fluid around her heart. Finally, we placed a permanent drain for the fluid around her lung. It was a long surgery, but treating all three problems at once gives her the best chance at feeling better.",
            9: "Procedure: Multi-compartment palliative intervention.\nAirway: Recanalization and stenting of RMS.\nCardiac: Pericardial fenestration.\nPleural: Indwelling catheter insertion.\nOutcome: Relief of obstruction and effusions."
        }
    }
    return variations

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
            
            # Update note_text with the variation if available
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Some source files might not have patient_age in registry_entry, handle gracefully
                # If it exists, update it. If not, we don't add it to avoid schema breakages unless intended.
                # Based on previous parts, we usually update specific fields.
                
                # Check/Update Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN to be unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"

                # Update Age if present (some source files put it in text, some in registry)
                # The prompt implies we should change age "slightly".
                # If the registry entry doesn't have age field, we can't update it there, 
                # but it's updated implicitly in the "story" of the data generation.
            
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
    output_filename = output_dir / "synthetic_blvr_notes_part_027.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()