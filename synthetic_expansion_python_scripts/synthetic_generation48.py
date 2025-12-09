import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_048.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the 10 notes in part_048.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Robert McNeil (EBUS-TBNA)
            1: "Proc: EBUS-TBNA mediastinal/hilar nodes.\nAnesthesia: GA, 8.5 ETT.\nDetails:\n- Airway inspection neg.\n- EBUS scope introduced.\n- Sampled 4R (3 passes, ROSE malig), 4L (3 passes, benign), 7 (4 passes, susp), 10L (2 passes, benign).\n- Total 12 passes.\nComp: None. <5mL EBL.\nPlan: Extubated. PACU. F/U 1-2 wks.",
            2: "OPERATIVE NARRATIVE: The patient, Mr. McNeil, presented for staging of a PET-avid left upper lobe mass. Following induction of general anesthesia and placement of an 8.5 mm endotracheal tube, a systematic endobronchial ultrasound examination was conducted. We identified and sampled stations 4R, 4L, 7, and 10L. Rapid On-Site Evaluation (ROSE) indicated malignancy in stations 4R and 7, while stations 4L and 10L yielded adequate lymphocytes without definitive malignant cells. The procedure concluded without complication, and the patient was transferred to the PACU in stable condition.",
            3: "Procedure Code: 31653 (EBUS sampling 3+ stations).\nGuidance: Convex linear EBUS (Olympus BF-UC180F).\nSites Sampled:\n1. Station 4R (Initial): 22G needle, 3 passes.\n2. Station 4L (Add-on): 22G needle, 3 passes.\n3. Station 7 (Add-on): 22G needle, 4 passes.\n4. Station 10L (Add-on): 22G needle, 2 passes.\nMedical Necessity: Staging for lung cancer (LUL mass). General anesthesia utilized. Cytology and molecular profiling ordered.",
            4: "Procedure: EBUS-TBNA\nAttending: Dr. Kim\nSteps:\n1. Time-out performed.\n2. ETT placed by Anesthesia.\n3. White light bronchoscopy: normal anatomy.\n4. EBUS TBNA performed at stations 4R, 4L, 7, and 10L using 22G needle.\n5. ROSE confirmed adequacy/malignancy at 4R/7.\n6. Scope removed. Patient extubated.\nComplications: None.",
            5: "We did the bronch on Mr McNeil today for his lung mass staging used the ebus scope under GA tube size 8.5. Looked at the nodes sampled 4R 4L 7 and 10L got good samples rose said cancer in 4R and 7 so thats likely stage 3. 4L and 10L looked okay just lymphocytes. No bleeding or issues patient woke up fine sending to pacu will follow up path.",
            6: "68-year-old male with LUL mass. Flexible bronchoscopy with EBUS-TBNA performed under general anesthesia. Airway inspected; no endobronchial lesions. EBUS identified target nodes. Needle aspiration performed at stations 4R, 4L, 7, and 10L. ROSE positive for malignancy at 4R and 7. Samples sent for final path and moleculars. Patient tolerated well, no complications.",
            7: "[Indication]\nLung cancer staging; LUL mass with PET-avid adenopathy.\n[Anesthesia]\nGeneral anesthesia, 8.5 mm ETT.\n[Description]\nSystematic EBUS-TBNA performed. Stations 4R, 4L, 7, and 10L sampled with 22G needle. ROSE confirmed malignant cells at 4R and 7. 4L and 10L benign.\n[Plan]\nExtubate, PACU, outpatient follow-up for molecular results.",
            8: "The patient was brought to the bronchoscopy suite for EBUS-TBNA to stage a left upper lobe mass. We utilized general anesthesia and an 8.5 mm ETT. After verifying the airway was clear, we switched to the EBUS scope. We methodically sampled stations 4R, 4L, 7, and 10L. The preliminary onsite evaluation suggested malignancy in the 4R and subcarinal nodes, which alters the staging. The left-sided nodes appeared benign. There were no complications, and the patient was extubated successfully.",
            9: "Procedure: Flexible bronchoscopy with ultrasound-guided aspiration of mediastinal nodes.\nOperator: Dr. Kim.\nActions: The airway was surveyed. The diagnostic scope was swapped for the linear EBUS. Target stations 4R, 4L, 7, and 10L were localized and aspirated. ROSE verified malignant cells in 4R and 7. Specimens were submitted for analysis. The patient was extubated and transferred."
        },
        1: { # Angela Rivera (Nav Bronch + Radial EBUS)
            1: "Proc: Robotic Nav Bronch + Radial EBUS + Biopsy RUL nodule.\nTarget: 8mm RUL posterior seg.\nAction:\n- Monarch nav to target.\n- Radial EBUS: concentric view.\n- Bx: 6 forceps, 3 TBNA, 2 brush.\nResult: Tool in lesion confirmed. No fluoro pneumo.\nPlan: D/C, CXR.",
            2: "OPERATIVE REPORT: Ms. Rivera, a 59-year-old female with a PET-avid RUL nodule, underwent robotic-assisted navigational bronchoscopy. The Monarch platform was utilized to navigate to the posterior segment of the right upper lobe. Radial endobronchial ultrasound (R-EBUS) confirmed a concentric, solid lesion. Transbronchial sampling including forceps biopsy, needle aspiration, and cytology brushing was performed. There was no evidence of pneumothorax or significant hemorrhage.",
            3: "Primary Code: 31627 (Computer-assisted navigation).\nAdd-on Codes: 31654 (Radial EBUS), 31628 (TBLB), 31629 (TBNA), 31623 (Brush).\nTechnique: Robotic platform docked. Registration error <2mm. Target RUL posterior segment localized with radial EBUS (concentric signal). Multiple modalities used to maximize diagnostic yield. General anesthesia administered.",
            4: "Resident Procedure Note\nPatient: Angela Rivera\nProcedure: Robotic Bronchoscopy/Biopsy\nSteps:\n1. GA/LMA. Monarch robot docked.\n2. Navigated to RUL posterior nodule.\n3. Confirmed with radial EBUS (concentric).\n4. Samples: Forceps x6, TBNA x3, Brush x2.\n5. Fluoro check: No pneumo.\nEst Blood Loss: <5 mL.",
            5: "Procedure note for Angela Rivera she has that 8mm nodule in the right upper lobe we used the robot today to get to it. Navigation was good registration error less than 2mm. Found it with the radial probe nice concentric view. Took a bunch of biopsies forceps needle and brush sent for everything including markers. No bleeding really patient did fine extubated in room.",
            6: "Robotic navigational bronchoscopy performed for 8 mm RUL posterior segment nodule. Monarch system used. Target reached; radial EBUS confirmed concentric lesion. Transbronchial forceps biopsies, needle aspiration, and brushings obtained. Fluoroscopy confirmed tool position. No complications. Patient stable for discharge after CXR.",
            7: "[Indication]\n8 mm PET-avid RUL nodule, bronchus sign positive.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nRobotic navigation to RUL posterior segment. Radial EBUS confirmation (concentric). Sampling via forceps, needle, and brush. Hemostasis achieved.\n[Plan]\nCXR, discharge, clinic follow-up 1-2 weeks.",
            8: "We performed a robotic navigational bronchoscopy on Ms. Rivera to biopsy a small RUL nodule. After registering the CT with the Monarch system, we drove the scope to the posterior segment. We utilized a radial EBUS probe to confirm we were exactly in the lesion, seeing a concentric image. We then passed biopsy forceps, a needle, and a brush through the guide sheath to ensure adequate tissue. The patient tolerated the procedure well with no signs of pneumothorax.",
            9: "Procedure: Computer-guided bronchoscopy with ultrasonic localization and transbronchial sampling.\nTarget: RUL nodule.\nTechnique: The robotic scope was steered to the lesion. Ultrasound verification showed a solid mass. Specimens were harvested using forceps, needle, and brush. No adverse events occurred."
        },
        2: { # James Caldwell (Rigid Bronch)
            1: "Dx: Tracheal SCC obstruction.\nProc: Rigid bronch, debulking, APC, stent.\nDetails:\n- Rigid scope inserted.\n- 80% mid-tracheal stenosis.\n- Cored/debulked + APC.\n- 16x50mm silicone stent deployed.\n- Lumen patent.\nPlan: Extubate, PACU, home.",
            2: "PROCEDURE: Rigid therapeutic bronchoscopy with tumor destruction and tracheal stenting.\nINDICATION: 73-year-old male with severe airway obstruction due to squamous cell carcinoma.\nDESCRIPTION: The rigid tracheobronchoscope was introduced. Significant fungating tumor was noted in the mid-trachea. Mechanical debulking was performed using the bevel of the scope and forceps, followed by APC for hemostasis and tumor ablation. A 16 x 50 mm Dumon silicone stent was deployed, covering the lesion and restoring airway patency.",
            3: "Billable Services:\n- 31641: Destruction of tumor (rigid coring + APC).\n- 31636: Placement of tracheal stent (silicone).\nJustification: Critical central airway obstruction (80%). General anesthesia/Jet ventilation required. Stent necessary to maintain patency after debulking.",
            4: "Resident Note: Rigid Bronchoscopy\nPatient: James Caldwell\nAttending: Dr. Bennett\nSteps:\n1. GA/Jet vent.\n2. Rigid scope passed.\n3. Tumor ID'd mid-trachea.\n4. Debulked with scope/forceps/APC.\n5. Stent placed (16x50mm).\n6. Airway inspected: Patent.\nComplications: None.",
            5: "Mr Caldwell here for the tracheal obstruction we did the rigid bronch today. Saw the tumor blocking about 80 percent of the trachea. Used the rigid barrel to core it out and used some APC to clean it up. Put in a silicone stent 16 by 50 fits good. Airway looks wide open now. Extubated in OR doing well.",
            6: "Therapeutic rigid bronchoscopy performed for mid-tracheal squamous cell carcinoma obstruction. 80% stenosis reduced to <20% via mechanical coring and argon plasma coagulation. 16x50 mm silicone stent deployed across lesion. Airway patent. Patient extubated and stable.",
            7: "[Indication]\nSevere malignant mid-tracheal obstruction (SCC).\n[Anesthesia]\nGeneral, rigid bronchoscopy, jet ventilation.\n[Description]\nMechanical debulking and APC of tracheal tumor. Deployment of 16x50mm silicone stent. Restoration of airway patency.\n[Plan]\nPACU, discharge, follow-up 4-6 weeks.",
            8: "Mr. Caldwell underwent rigid bronchoscopy to relieve his tracheal obstruction. We identified the squamous cell carcinoma narrowing the mid-trachea. We mechanically removed the bulk of the tumor and used APC to control bleeding and destroy residual tissue. To prevent re-obstruction, we placed a straight silicone stent. The airway is now widely patent, and he was extubated immediately following the procedure.",
            9: "Procedure: Rigid endoscopy with tumor ablation and airway stenting.\nSubject: James Caldwell.\nFindings: Severe tracheal stenosis.\nIntervention: The mass was resected and cauterized. A silicone prosthesis was positioned to scaffold the airway.\nOutcome: Obstruction resolved."
        },
        3: { # Matthew Li (Thoracentesis + Chest Tube)
            1: "Dx: R empyema.\nProc: US Thora + Chest Tube.\nSteps:\n- US loculated fluid.\n- 40mL asp for labs.\n- 28Fr chest tube placed 6th ICS.\n- 900mL purulent output.\nPlan: ICU, antibiotics, consider TPA/DNAse.",
            2: "PROCEDURE NOTE: Ultrasound-guided thoracentesis and large-bore chest tube insertion.\nPATIENT: Mr. Li, 56M, with complex parapneumonic effusion.\nDETAILS: Under real-time ultrasound guidance, diagnostic aspiration confirmed turbid fluid. Subsequently, a 28 Fr tube thoracostomy was performed using the Seldinger technique via a separate incision. Immediate return of 900 mL of purulent fluid confirmed the diagnosis of empyema. Post-procedure imaging ordered.",
            3: "Codes:\n- 32555: Thoracentesis with imaging guidance (diagnostic/therapeutic).\n- 32551: Tube thoracostomy (separate incision/site).\nMedical Necessity: Septated empyema requiring large-bore drainage. Ultrasound essential for safe localization.",
            4: "Procedure: Chest Tube Placement\nPatient: Matthew Li\nIndication: Empyema\nSteps:\n1. US localization.\n2. Diagnostic tap (19G): turbid fluid.\n3. 28Fr chest tube placed (Seldinger).\n4. Sutured, sterile dressing.\n5. Output: 900mL purulent.\nComplications: None.",
            5: "Bedside procedure for Mr Li in the ICU he has that loculated effusion right side. Used ultrasound to find a pocket. Numbed him up tapped it got pus so we went ahead and put in a chest tube. 28 french big tube. Drained about 900 cc of nasty looking fluid. Hooked to suction he tolerated it fine.",
            6: "Ultrasound-guided diagnostic thoracentesis followed by 28 Fr chest tube insertion for right-sided empyema. 40 mL aspirated for analysis; 900 mL purulent fluid drained via tube. No complications. Patient remains in ICU on vasopressors.",
            7: "[Indication]\nRight complex parapneumonic effusion/empyema.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nUS-guided aspiration of pleural space. Placement of 28 Fr chest tube. Drainage of 900 mL purulent fluid.\n[Plan]\nSuction -20cmH2O, antibiotics, repeat imaging.",
            8: "We performed a bedside procedure for Mr. Li to manage his right-sided empyema. Using ultrasound, we first performed a diagnostic thoracentesis to confirm the nature of the fluid. Upon seeing turbid fluid, we proceeded to place a large-bore 28 French chest tube. This immediately drained nearly a liter of purulent fluid. The tube was secured, and a follow-up chest x-ray was ordered.",
            9: "Procedure: Sonographic-guided pleural aspiration and thoracostomy.\nIndication: Pyothorax.\nAction: The pleural space was accessed under imaging. Fluid was withdrawn for testing. A drainage catheter (28 Fr) was inserted. Purulent effusion was evacuated.\nOutcome: Lung re-expansion pending imaging."
        },
        4: { # Lucille Brown (Landmark Thora)
            1: "Dx: L pleural effusion (CHF).\nProc: Bedside thora (landmark).\nDetails:\n- Sitting pos.\n- Percussion/auscultation localization.\n- 18G needle 8th ICS.\n- 60mL dx, 900mL tx removed.\n- Straw colored.\nPlan: Home, cards f/u.",
            2: "PROCEDURE: Diagnostic and therapeutic thoracentesis without imaging guidance.\nINDICATION: 82-year-old female with CHF and large symptomatic left pleural effusion.\nDESCRIPTION: The left posterior hemithorax was percussed to identify the effusion. Using landmark technique, needle aspiration yielded straw-colored fluid consistent with transudate. A total of 960 mL was drained for symptomatic relief. The patient tolerated the procedure well.",
            3: "Code: 32554 (Thoracentesis w/o imaging).\nJustification: Ultrasound unavailable in clinic; large effusion easily localized by physical exam. Therapeutic drainage (900mL) performed for dyspnea.",
            4: "Procedure: Thoracentesis (Landmark)\nPatient: Lucille Brown\nSteps:\n1. Prepped/draped.\n2. Local anesthesia.\n3. Needle insertion L posterior chest.\n4. Fluid return: straw colored.\n5. Drained 960mL total.\n6. Catheter removed.\nNo complications.",
            5: "Did a thora on Mrs Brown in the clinic she was very short of breath. No ultrasound machine so just tapped it based on exam. Left side. Got back straw colored fluid likely CHF. Took off almost a liter she felt much better. Sending fluid for labs just in case. Discharged home.",
            6: "Left-sided diagnostic and therapeutic thoracentesis performed via landmark technique. 8th intercostal space accessed. 960 mL straw-colored fluid removed. Patient monitored for re-expansion edema/hypotension; none observed. Discharged stable.",
            7: "[Indication]\nSymptomatic left pleural effusion, CHF.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nLandmark-guided thoracentesis. 18G catheter. 960 mL straw-colored fluid drained. Catheter removed.\n[Plan]\nCXR, cardiology follow-up.",
            8: "Mrs. Brown presented with shortness of breath due to a large effusion. Without ultrasound available, we performed a landmark-guided thoracentesis on the left side. We successfully drained nearly a liter of fluid, which appeared clear and consistent with heart failure. She reported immediate symptomatic improvement and was discharged home.",
            9: "Procedure: Blind pleural aspiration.\nSite: Left hemithorax.\nAction: The effusion was localized via physical exam. A catheter was inserted. Fluid was evacuated for diagnosis and symptom relief.\nResult: 960 mL removed. Dyspnea improved."
        },
        5: { # Samuel Patel (PleurX)
            1: "Dx: Recurrent malignant effusion (Lung CA).\nProc: Tunneled IPC (PleurX) placement.\nSteps:\n- US guidance.\n- Seldinger technique R mid-axillary.\n- Subq tunnel created.\n- Catheter placed.\n- 1500mL drained.\nPlan: Home w/ nursing.",
            2: "OPERATIVE NOTE: Insertion of indwelling tunneled pleural catheter.\nINDICATION: 69-year-old male with metastatic lung adenocarcinoma and recurrent right pleural effusion.\nDESCRIPTION: Under ultrasound guidance, the right pleural space was accessed. A subcutaneous tunnel was created, and the PleurX catheter was advanced. 1500 mL of serosanguinous fluid was drained to confirm position and patency. The patient was discharged with home health instructions.",
            3: "Code: 32550 (Insertion of tunneled pleural catheter).\nNotes: Includes drainage at time of placement. Ultrasound guidance used. Catheter tunneled subcutaneously.",
            4: "Procedure: PleurX Placement\nPatient: Samuel Patel\nSteps:\n1. US check: free flowing fluid.\n2. Local anesthetic.\n3. Needle access/wire placement.\n4. Tunnel created.\n5. Catheter inserted/peel-away sheath.\n6. Drained 1.5L.\nComplications: None.",
            5: "Put a PleurX catheter in Mr Patel today for his cancer fluid. Right side. Used ultrasound to find a good spot. Tunneled it nicely. Drained about a liter and a half of bloody fluid. He tolerated it well. Home health is set up to help him drain it at home.",
            6: "Ultrasound-guided placement of right-sided tunneled indwelling pleural catheter (PleurX). 1500 mL serosanguinous fluid drained. Catheter patent. No complications. Discharged with home nursing.",
            7: "[Indication]\nRecurrent malignant right pleural effusion.\n[Anesthesia]\nLocal.\n[Description]\nUS-guided insertion of tunneled IPC. 1500 mL drained. Catheter secured.\n[Plan]\nHome drainage 3x/week.",
            8: "To manage Mr. Patel's recurrent malignant effusion, we placed a tunneled PleurX catheter on the right side. Using ultrasound, we accessed the space and tunneled the catheter subcutaneously to reduce infection risk. We drained 1.5 liters of fluid during the procedure. He will now be able to manage his symptoms at home with intermittent drainage.",
            9: "Procedure: Implantation of tunneled pleural drain.\nIndication: Malignant dropsy.\nAction: The pleural cavity was accessed under sonographic vision. A prosthetic catheter was tunneled and inserted. Fluid was evacuated.\nOutcome: Device functional."
        },
        6: { # Diane Curry (PleurX Removal)
            1: "Indication: Pleurodesis achieved. Catheter not draining.\nProc: PleurX removal.\nAction: Cuff dissected. Catheter pulled intact.\nResult: No air leak. Suture closed.\nPlan: Home.",
            2: "PROCEDURE: Removal of tunneled indwelling pleural catheter.\nPATIENT: Ms. Curry, 64F, with history of breast cancer.\nDETAILS: The right-sided PleurX catheter was removed following successful spontaneous pleurodesis. The cuff was dissected free from the subcutaneous tissue, and the catheter was withdrawn without resistance. The exit site was sutured. No complications occurred.",
            3: "Code: 32552 (Removal of indwelling tunneled pleural catheter).\nCondition: Catheter no longer needed (autopleurodesis). Cuff dissected/removed intact.",
            4: "Procedure: IPC Removal\nPatient: Diane Curry\nSteps:\n1. Prepped site.\n2. Local anesthesia.\n3. Dissected cuff.\n4. Removed catheter.\n5. Sutured wound.\nNo complications.",
            5: "Removed Ms Currys pleurx today shes dried up. Right side. Cut down to the cuff and freed it up pulled it out no problem. Stitched it up. She can go home.",
            6: "Removal of right tunneled pleural catheter. Indication: Autopleurodesis. Cuff mobilized and catheter removed intact. Exit site closed with nylon suture. Patient discharged.",
            7: "[Indication]\nResolved malignant effusion, spontaneous pleurodesis.\n[Anesthesia]\nLocal.\n[Description]\nDissection and removal of right tunneled pleural catheter. Closure of site.\n[Plan]\nSuture removal in 7-10 days.",
            8: "Ms. Curry's pleural effusion has resolved, so we removed her PleurX catheter today. After numbing the area, we dissected the fibrous cuff from the tunnel and pulled the catheter out. The site was closed with a suture. She tolerated the removal well.",
            9: "Procedure: Extraction of tunneled pleural drain.\nReason: Autopleurodesis.\nAction: The retention cuff was liberated. The device was withdrawn.\nResult: Site closed."
        },
        7: { # Miguel Sanchez (Pigtail)
            1: "Dx: Loculated malignant effusion.\nProc: US-guided pigtail (12Fr).\nSteps:\n- US localized pocket.\n- Seldinger technique.\n- 12Fr pigtail placed.\n- 700mL drained.\nPlan: Admit to oncology.",
            2: "PROCEDURE NOTE: Ultrasound-guided placement of small-bore pleural drainage catheter.\nINDICATION: 49-year-old male with metastatic renal cell carcinoma and loculated right pleural effusion.\nDESCRIPTION: Under ultrasound guidance, a 12 Fr pigtail catheter was inserted into the right pleural space using the Seldinger technique. 700 mL of serosanguinous fluid was drained. The catheter was secured and attached to a drainage system.",
            3: "Code: 32557 (Pleural drainage with imaging guidance).\nDevice: 12 Fr pigtail catheter.\nGuidance: Ultrasound (real-time).\nNote: Separate from thoracentesis codes.",
            4: "Procedure: Pigtail Catheter Placement\nPatient: Miguel Sanchez\nSteps:\n1. US scan: loculated fluid.\n2. Local anesthesia.\n3. Needle/wire access.\n4. Dilated tract.\n5. 12Fr pigtail advanced.\n6. Drained 700mL.\nComplications: None.",
            5: "Placed a pigtail for Mr Sanchez today he has those loculated effusions. Right side. Used ultrasound to find the big pocket. Put in a 12 french wire guided. Drained 700cc. Secured it well he's going back to the floor.",
            6: "Ultrasound-guided insertion of 12 Fr pigtail catheter into right pleural space for loculated malignant effusion. 700 mL serosanguinous fluid drained. No pneumothorax. Catheter secured.",
            7: "[Indication]\nLoculated right malignant effusion.\n[Anesthesia]\nLocal/Moderate.\n[Description]\nUS-guided placement of 12Fr pigtail catheter. 700 mL drained.\n[Plan]\nFloor care, daily output monitoring.",
            8: "We placed a small-bore pigtail catheter for Mr. Sanchez to manage his loculated effusion. Using ultrasound to guide us, we accessed the fluid pocket and threaded a 12 French catheter over a wire. We drained about 700 mL of fluid. The catheter was secured for ongoing drainage on the ward.",
            9: "Procedure: Image-guided percutaneous pleural drainage.\nIndication: Complex effusion.\nAction: A pigtail catheter was introduced under sonographic control. Fluid was evacuated.\nOutcome: Catheter in situ."
        },
        8: { # Linda Ngo (EBUS + Nav + TBLB)
            1: "Proc: EBUS (4R, 7, 11R) + EM Nav (RLL mass).\nFindings:\n- EBUS: 4R/7 malignant.\n- Nav: Tool in lesion, fluoroscopy confirmed.\n- Bx: 5 samples RLL mass.\nComp: None.\nPlan: Oncology referral.",
            2: "OPERATIVE REPORT: Combined EBUS-TBNA and electromagnetic navigational bronchoscopy. \nINDICATION: Staging and diagnosis for 71F with RLL mass and adenopathy.\nEBUS: Stations 4R, 7, and 11R sampled. Malignancy confirmed at 4R/7.\nNAVIGATION: The superDimension system was used to navigate to the RLL basilar segment lesion. Transbronchial biopsies were obtained under fluoroscopic guidance. \nCONCLUSION: Stage IIIA/B lung cancer (N2 disease).",
            3: "Codes:\n- 31653: EBUS 3+ stations (4R, 7, 11R).\n- 31627: Navigational bronchoscopy.\n- 31628: TBLB single lobe (RLL).\nRational: EBUS for staging, Nav/TBLB for primary lesion diagnosis. Distinct services.",
            4: "Procedure: EBUS + Nav Bronch\nPatient: Linda Ngo\nSteps:\n1. EBUS: 4R, 7, 11R sampled.\n2. Nav: Registered CT. Navigated to RLL mass.\n3. TBLB: 5 passes.\n4. Fluoro confirmed position.\nEvents: Minor bleeding, stopped w/ saline.",
            5: "Double procedure for Ms Ngo today staging and diagnosis. Started with EBUS hit 4R 7 and 11R rose said cancer in the mediastinum. Then switched to the nav scope for the RLL mass. Got right to it with the superD. Took 5 biopsies looks diagnostic. Patient did fine.",
            6: "Combined EBUS-TBNA and electromagnetic navigational bronchoscopy. Stations 4R, 7, 11R sampled; malignancy at 4R/7. Navigational bronchoscopy to RLL mass performed with fluoroscopic confirmation. Transbronchial biopsies obtained. No complications.",
            7: "[Indication]\nRLL mass, mediastinal adenopathy.\n[Anesthesia]\nGeneral.\n[Description]\n1. EBUS-TBNA stations 4R, 7, 11R.\n2. EM Navigation to RLL mass.\n3. Transbronchial biopsy RLL.\n[Plan]\nOncology follow-up.",
            8: "We performed a combined staging and diagnostic procedure for Ms. Ngo. First, we used EBUS to sample nodes at stations 4R, 7, and 11R, confirming malignancy in the mediastinum. Then, using electromagnetic navigation, we guided a scope to her RLL mass and obtained several biopsies. This provides both the diagnosis and the stage in one session.",
            9: "Procedure: Ultrasound-guided nodal aspiration and computer-assisted parenchymal biopsy.\nTarget: Mediastinal nodes and RLL tumor.\nAction: EBUS-TBNA was performed on 3 stations. The RLL lesion was localized via EM guidance and sampled.\nResult: Diagnosis and staging completed."
        },
        9: { # Omar Rahman (EBUS + Nav + TBLB - Single node)
            1: "Proc: EBUS (Stn 7) + EM Nav (LLL nodule).\nFindings:\n- EBUS: Stn 7 benign.\n- Nav: LLL lesion, 4 bx taken.\nComp: None.\nPlan: D/C, wait for path.",
            2: "PROCEDURE: Flexible bronchoscopy with EBUS-TBNA and electromagnetic navigation.\nINDICATION: 64M with LLL nodule and subcarinal lymphadenopathy.\nDETAILS: EBUS-TBNA of station 7 was performed; ROSE was negative for malignancy. Electromagnetic navigation was then utilized to reach the LLL superior segment nodule. Transbronchial biopsies were obtained under fluoroscopic guidance.",
            3: "Codes:\n- 31652: EBUS 1 station (Stn 7).\n- 31627: Navigational guidance.\n- 31628: TBLB single lobe (LLL).\nNote: Only one nodal station sampled, so 31652 is correct (not 31653).",
            4: "Procedure: EBUS + Nav TBLB\nPatient: Omar Rahman\nSteps:\n1. EBUS Stn 7: 3 passes.\n2. Nav set up. Targeted LLL nodule.\n3. TBLB x4.\n4. Fluoro check.\nBenign ROSE on node. Biopsies sent.",
            5: "Mr Rahman here for the LLL nodule. Checked the subcarinal node first with EBUS it looked benign but we sampled it anyway. Then used the navigation to get out to the lung lesion. Took 4 biopsies. No bleeding. Extubated fine.",
            6: "EBUS-TBNA of station 7 (benign on ROSE) followed by electromagnetic navigational bronchoscopy to LLL superior segment nodule. Transbronchial biopsies obtained. No complications.",
            7: "[Indication]\nLLL nodule, station 7 lymphadenopathy.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA station 7. EM navigation to LLL nodule. Transbronchial biopsies.\n[Plan]\nOutpatient follow-up.",
            8: "We performed a bronchoscopy on Mr. Rahman to investigate his LLL nodule and a nearby lymph node. The EBUS sample of the lymph node (station 7) appeared benign. We then navigated to the lung nodule using the electromagnetic system and took four biopsies to determine its nature.",
            9: "Procedure: Sonographic nodal sampling and guided lung biopsy.\nTarget: Station 7 and LLL lesion.\nAction: The subcarinal node was aspirated. The lung nodule was localized via navigation and biopsied.\nOutcome: Samples to pathology."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for names/ages/dates to simulate reading from a master source.
    Indices match the notes in the JSON file.
    """
    return [
        {"idx": 0, "orig_name": "Robert McNeil", "orig_age": 68, "names": ["John Smith", "David Miller", "James Wilson", "Robert Taylor", "William Anderson", "Richard Thomas", "Charles Jackson", "Joseph White", "Thomas Harris"]},
        {"idx": 1, "orig_name": "Angela Rivera", "orig_age": 59, "names": ["Maria Garcia", "Susan Martinez", "Lisa Robinson", "Nancy Clark", "Karen Rodriguez", "Betty Lewis", "Helen Lee", "Sandra Walker", "Donna Hall"]},
        {"idx": 2, "orig_name": "James Caldwell", "orig_age": 73, "names": ["Paul Allen", "Mark Young", "Donald Hernandez", "George King", "Kenneth Wright", "Steven Lopez", "Edward Hill", "Brian Scott", "Ronald Green"]},
        {"idx": 3, "orig_name": "Matthew Li", "orig_age": 56, "names": ["Kevin Adams", "Jason Baker", "Jeffrey Gonzalez", "Ryan Nelson", "Jacob Carter", "Gary Mitchell", "Nicholas Perez", "Eric Roberts", "Stephen Turner"]},
        {"idx": 4, "orig_name": "Lucille Brown", "orig_age": 82, "names": ["Carol Phillips", "Michelle Campbell", "Emily Parker", "Amanda Evans", "Melissa Edwards", "Deborah Collins", "Stephanie Stewart", "Rebecca Sanchez", "Laura Morris"]},
        {"idx": 5, "orig_name": "Samuel Patel", "orig_age": 69, "names": ["Frank Rogers", "Scott Reed", "Justin Cook", "Brandon Morgan", "Gregory Bell", "Benjamin Murphy", "Samuel Bailey", "Patrick Rivera", "Jack Cooper"]},
        {"idx": 6, "orig_name": "Diane Curry", "orig_age": 64, "names": ["Sharon Richardson", "Cynthia Cox", "Kathleen Howard", "Amy Ward", "Shirley Torres", "Angela Peterson", "Ruth Gray", "Brenda Ramirez", "Pamela James"]},
        {"idx": 7, "orig_name": "Miguel Sanchez", "orig_age": 49, "names": ["Alexander Watson", "Dennis Brooks", "Jerry Kelly", "Tyler Sanders", "Aaron Price", "Henry Bennett", "Douglas Wood", "Peter Barnes", "Adam Ross"]},
        {"idx": 8, "orig_name": "Linda Ngo", "orig_age": 71, "names": ["Virginia Henderson", "Katherine Coleman", "Joan Jenkins", "Christine Perry", "Catherine Powell", "Debra Long", "Rachel Patterson", "Carolyn Hughes", "Janet Flores"]},
        {"idx": 9, "orig_name": "Omar Rahman", "orig_age": 64, "names": ["Nathan Washington", "Zachary Butler", "Walter Simmons", "Kyle Foster", "Harold Gonzales", "Carl Bryant", "Arthur Alexander", "Roger Russell", "Albert Griffin"]}
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
            
            # Get the specific name assigned in base_data
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: No text variation found for note {idx}, style {style_num}")
            
            # Update registry_entry fields if they exist to match the "new" patient
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
    output_filename = output_dir / "synthetic_notes_part_048.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()