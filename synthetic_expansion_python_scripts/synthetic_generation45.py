import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (Targeting part 045 as requested)
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_045.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations for the notes in part 045.
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Lucille Sanders (EBUS 4R, 7; 10R unsampled) - 31652
            1: "Pre-op: RUL mass. Staging.\nAnesthesia: GA, 8.5 ETT.\nProcedure:\n- Airway inspected: Clear.\n- Linear EBUS: Station 4R (1.5cm, hypoechoic) x4 passes. Station 7 (1.2cm) x4 passes.\n- Station 10R visualized (6-7mm), benign appearance, NOT sampled.\n- No radial EBUS.\n- Specimens: cellular/lymphoid tissue.\nComplications: None.\nPlan: Extubate. Recovery.",
            2: "HISTORY: Ms. Sanders, a 59-year-old female with a right upper lobe pulmonary opacity suspicious for non-small cell carcinoma, underwent mediastinal staging.\nPROCEDURE: General anesthesia was induced and an 8.5 mm endotracheal tube secured. The bronchial tree was examined. Linear endobronchial ultrasound (EBUS) was utilized for systematic nodal interrogation. The paratracheal station 4R demonstrated sonographic features of malignancy; transbronchial needle aspiration (TBNA) was performed (4 passes). Similarly, the subcarinal station 7 was sampled (4 passes). Station 10R was visualized but deemed non-pathologic and was deliberately spared from biopsy.\nIMPRESSION: Successful EBUS-TBNA of stations 4R and 7. Station 10R observed only.",
            3: "Code Selection: 31652 (EBUS-TBNA 1-2 stations).\nTechnique:\n1. Scope: Linear EBUS bronchoscope.\n2. Access: ETT (General Anesthesia).\n3. Sampling: Station 4R (4 passes, 22G). Station 7 (4 passes, 22G). Total distinct stations sampled: 2.\n4. Observation: Station 10R visualized but clearly documented as not sampled.\n5. Bundling: Diagnostic bronchoscopy (31622) included.\nOutcome: Adequate cytology obtained.",
            4: "Procedure: EBUS Staging\nPatient: Lucille Sanders\nSteps:\n1. GA with 8.5 ETT.\n2. Airway survey - clear.\n3. EBUS scope in.\n4. Sampled 4R: 4 passes, 22G.\n5. Sampled 7: 4 passes, 22G.\n6. Looked at 10R but didn't touch it.\n7. ROSE said lymphoid tissue.\nPlan: PACU.",
            5: "Procedure note for Lucille Sanders 59F RUL mass staging. We did the EBUS today under general anesthesia tube 8.5. Went down looked around airways fine. Switched to EBUS scope checked the nodes. 4R looked big dark edges so we stuck it 4 times with the 22 needle. Station 7 also poked 4 times. Saw 10R but it looked small so we left it alone didn't biopsy that one. No bleeding really patient woke up fine sent to PACU thanks.",
            6: "Flexible bronchoscopy and endobronchial ultrasound with transbronchial needle aspiration of mediastinal lymph nodes. Patient is a 59-year-old female. General anesthesia with 8.5 ETT. Standard airway survey negative. Linear EBUS performed. Station 4R sampled x4 passes with 22G needle. Station 7 sampled x4 passes with 22G needle. Station 10R visualized but not sampled. No complications. Specimens to cytology.",
            7: "[Indication]\nStaging of PET-avid mediastinal adenopathy, RUL mass.\n[Anesthesia]\nGeneral anesthesia, 8.5 ETT.\n[Description]\nDiagnostic bronchoscopy: normal anatomy. Linear EBUS: Station 4R (1.5cm) biopsied x4. Station 7 (1.2cm) biopsied x4. Station 10R visualized only, not biopsied. ROSE confirmed adequacy.\n[Plan]\nExtubate, PACU, await final path.",
            8: "The patient was brought to the room and placed under general anesthesia with an endotracheal tube. We performed a standard airway inspection which was unremarkable. We then introduced the linear EBUS scope to survey the lymph nodes. We identified an enlarged node at station 4R and performed four needle passes. We also sampled a node at station 7 with four passes. We visualized a smaller node at 10R but decided not to sample it. The procedure was uncomplicated.",
            9: "Procedure: Flexible bronchoscopy with sonographic guidance and nodal aspiration.\nSubject: Lucille Sanders.\nAction: Under general anesthesia, the airway was surveyed. The linear EBUS instrument was deployed. Station 4R was interrogated and aspirated (4 passes). Station 7 was similarly aspirated. Station 10R was observed but not punctured. Material was collected for cytologic analysis.\nResult: No adverse events.",
        },
        1: { # Omar Ruiz (EBUS 11R, 4R, 7; Radial used inside node only) - 31653
            1: "Indication: RLL mass staging.\nAnesthesia: GA, 8.0 ETT.\nProcedure:\n- Airway clear.\n- EBUS-TBNA performed at 3 stations: 11R, 4R, 7.\n- Radial probe used inside 11R node for echotexture (not peripheral lung).\n- Total 10 passes.\nComplications: Minimal bleeding.\nPlan: PACU.",
            2: "HISTORY: Mr. Ruiz presented for staging of an RLL mass and associated adenopathy.\nPROCEDURE: General anesthesia was established via an 8.0 mm ETT. A diagnostic airway survey was unrevealing. A linear EBUS scope was introduced. Systematic staging involved TBNA of station 11R (interlobar), station 4R (lower paratracheal), and station 7 (subcarinal). Note: A radial miniprobe was utilized strictly intravascularly within the 11R node for characterization, not for peripheral lung navigation.\nIMPRESSION: Successful sampling of three distinct nodal stations (11R, 4R, 7).",
            3: "Billing Summary:\n- CPT 31653 (EBUS-TBNA 3+ stations).\n- Stations Sampled: 11R, 4R, 7 (Three distinct stations).\n- Note on 31654: Radial EBUS was used only within the lymph node (11R) for characterization. No peripheral lesion was targeted with radial EBUS. Therefore, 31654 is NOT reported.\n- 31622 Bundled.",
            4: "Procedure: EBUS 3 Stations\nPatient: Omar Ruiz, 64M\nSteps:\n1. GA/ETT.\n2. Scope checked airways.\n3. EBUS scope used.\n4. Sampled 11R (used radial probe to look inside node first).\n5. Sampled 4R.\n6. Sampled 7.\n7. 10 passes total.\nComplications: None.",
            5: "Procedure note Omar Ruiz 64M RLL mass. We did the bronch under GA. Airway looked ok. Used the EBUS scope to sample three nodes. First was 11R used the mini radial probe just to check the inside of the node then biopsied it. Then did 4R and 7. Good samples obtained. No peripheral biopsy done. Patient stable.",
            6: "Flexible bronchoscopy and linear EBUS-TBNA. General anesthesia 8.0 ETT. Diagnostic inspection normal. EBUS nodal survey performed. Station 11R sampled x4 passes (radial probe used for nodal characterization only). Station 4R sampled x3 passes. Station 7 sampled x3 passes. No peripheral lung sampling. Minimal bleeding. Patient stable.",
            7: "[Indication]\nMediastinal/hilar staging, RLL mass.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nEBUS-TBNA performed at stations 11R, 4R, and 7. Radial probe utilized intra-nodally at 11R only. No peripheral lesion targeting. Total 10 passes.\n[Plan]\nPathology review.",
            8: "We performed a bronchoscopy on Mr. Ruiz under general anesthesia. We sampled three separate lymph node stations: 11R, 4R, and 7. At station 11R, we briefly used a radial probe to look at the node structure before sampling, but we did not go out to the lung periphery. All biopsies went well with minimal bleeding.",
            9: "Operation: Endobronchial ultrasound with needle aspiration.\nTarget: Stations 11R, 4R, 7.\nDetails: The linear instrument was advanced. At station 11R, a radial transducer was employed to characterize the node interior prior to aspiration. Stations 4R and 7 were also aspirated. No peripheral lung nodule was targeted.\nOutcome: Samples acquired from three distinct stations.",
        },
        2: { # Tina Nguyen (Nav/Radial/TBLB LLL + EBUS 11L, 7) - 31627, 31654, 31628, 31652
            1: "Indication: LLL nodule + staging.\nAnesthesia: GA, 8.0 ETT.\nProcedure:\n- Ion Robot nav to LLL nodule.\n- Radial EBUS: Concentric view.\n- TBLB LLL x5 passes.\n- Linear EBUS: Stations 11L, 7 sampled.\nComplications: None.\nPlan: Extubate, discharge.",
            2: "HISTORY: Ms. Nguyen presented with a PET-avid 2.1 cm LLL nodule and adenopathy.\nPROCEDURE: Under general anesthesia (8.0 ETT), a robotic bronchoscopy (Ion) was performed. Registration was accurate (2.3mm error). Navigation to the LLL target was achieved, confirmed by concentric radial EBUS view. Transbronchial forceps biopsies were obtained. Subsequently, a linear EBUS scope was introduced for staging. TBNA was performed at stations 11L and 7.\nIMPRESSION: Successful diagnostic robotic bronchoscopy and mediastinal staging.",
            3: "Coding: 31628 (TBLB), 31627 (Nav add-on), 31654 (REBUS add-on), 31652 (EBUS 1-2 stations).\nJustification:\n- Navigation (Ion) used to reach LLL target.\n- Radial EBUS confirmed peripheral lesion.\n- Biopsy taken from LLL (Single lobe).\n- Separate Linear EBUS scope used for stations 11L and 7 (2 stations).",
            4: "Procedure: Robot Bronch + EBUS\nPatient: Tina Nguyen, 50F\nSteps:\n1. GA, ETT.\n2. Ion robot docked. Registered.\n3. Navigated to LLL nodule.\n4. REBUS check - concentric.\n5. Biopsied nodule (TBLB).\n6. Switched to Linear EBUS.\n7. Sampled 11L and 7.\nPlan: Discharge.",
            5: "Note for Tina Nguyen LLL nodule. GA with tube. Used the Ion robot system drove it out to the LLL spot. Radial probe showed the lesion concentric view so we took 5 biopsies. Then pulled that scope and put in the EBUS scope. Sampled the 11L and 7 nodes. Everything went smooth no pneumo on fluoro. Sending her home later.",
            6: "Robotic bronchoscopy with navigation, radial EBUS, TBLB, and linear EBUS-TBNA. Patient 50F. General anesthesia 8.0 ETT. Ion system navigation to LLL nodule. Radial EBUS confirmation. TBLB x5 passes. Linear EBUS sampling of stations 11L and 7. No complications. Extubated.",
            7: "[Indication]\nLLL nodule, mediastinal adenopathy.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nRobotic navigation to LLL target. Radial EBUS confirmation (concentric). TBLB performed. Linear EBUS-TBNA of stations 11L and 7 performed.\n[Plan]\nOutpatient discharge.",
            8: "Ms. Nguyen was placed under general anesthesia for her procedure. We utilized the Ion robotic system to navigate to the nodule in the left lower lobe. We confirmed the location with a radial ultrasound probe and took five biopsies. Afterwards, we switched to the linear ultrasound scope and sampled lymph nodes at stations 11L and 7. The procedure was completed without issues.",
            9: "Procedure: Computer-guided bronchoscopy with peripheral and central ultrasound assessment.\nAction: The robotic catheter was navigated to the LLL lesion. Radial sonography verified the target. Forceps samples were acquired. The linear ultrasound instrument was then introduced to aspirate nodal stations 11L and 7.\nResult: Tissue procured from lung and nodes.",
        },
        3: { # Justin Fowler (Aborted EBUS, BAL only) - 31624
            1: "Indication: Mediastinal adenopathy.\nSedation: Moderate (Versed/Fentanyl). Nasal.\nProcedure:\n- Airways inspected: Clear.\n- Attempted EBUS: Failed due to severe cough/desat.\n- ABORTED EBUS. No nodes sampled.\n- BAL performed RML.\nComplications: Desat, resolved.\nPlan: Discharge. Re-eval.",
            2: "HISTORY: Mr. Fowler presented for evaluation of mediastinal adenopathy.\nPROCEDURE: Under moderate sedation via nasal approach, the vocal cords were traversed. An attempt was made to introduce the linear EBUS scope; however, the patient exhibited severe tussive reflex and desaturation, necessitating abortion of the EBUS component prior to any sampling. A standard bronchoscope was reintroduced, and a bronchoalveolar lavage (BAL) was performed in the RML.\nIMPRESSION: Diagnostic bronchoscopy with BAL only. EBUS aborted.",
            3: "Coding: 31624 (Bronchoscopy with BAL).\nRationale:\n- EBUS codes (31652/53/54) are NOT billable as the scope did not advance/no sampling occurred.\n- 31622 (Diagnostic) is bundled into 31624.\n- Service performed: Inspection + BAL of RML.\n- Sedation: Moderate, inherent.",
            4: "Procedure: Bronch BAL (Failed EBUS)\nPatient: Justin Fowler, 71M\nSteps:\n1. Mod sedation.\n2. Scope in nose.\n3. Tried EBUS, patient coughed too much, desatted to 84%.\n4. Stopped EBUS attempt.\n5. Did BAL in RML with regular scope.\n6. Patient recovered.\nPlan: Home.",
            5: "Procedure note Justin Fowler 71M. Wanted to do EBUS for nodes. Patient under moderate sedation via nose. Tried to get the EBUS scope down but he coughed like crazy and sats dropped. Couldn't do it so we stopped. Switched back to regular scope and just washed the RML (BAL). Sending fluid for labs. No biopsy done. Discharge home.",
            6: "Flexible bronchoscopy with bronchoalveolar lavage. Attempted EBUS aborted. Patient 71M. Moderate sedation. EBUS scope introduction failed due to severe cough and hypoxia. No nodal sampling performed. Standard bronchoscope used for BAL of RML. Patient stabilized. Discharged.",
            7: "[Indication]\nMediastinal adenopathy.\n[Anesthesia]\nModerate sedation (native airway).\n[Description]\nDiagnostic inspection. Attempted EBUS aborted due to intolerance/desaturation. BAL RML performed. No biopsies.\n[Plan]\nDischarge, consider GA for future attempt.",
            8: "We attempted an EBUS on Mr. Fowler today using moderate sedation. Unfortunately, he had a severe cough and his oxygen levels dropped when we tried to pass the EBUS scope, so we had to stop that part of the procedure without sampling any nodes. We did manage to perform a lavage of the right middle lobe with a standard scope. He recovered well afterwards.",
            9: "Procedure: Flexible bronchoscopy with lavage; attempted sonographic staging.\nDetails: Access was achieved via the naris. Introduction of the ultrasonic bronchoscope was precluded by respiratory instability. The EBUS component was terminated. A lavage of the RML was executed successfully.\nOutcome: Lavage fluid collected; no nodal tissue.",
        },
        4: { # Henry Brooks (Stent Maintenance, no new stent) - 31645
            1: "Indication: Stent check/mucus.\nSedation: Moderate.\nProcedure:\n- Left mainstem stent visualized.\n- 70% occluded with mucus.\n- Action: Aggressive suction/lavage (15 mins).\n- Result: >80% patent.\n- No stent removal/replacement/dilation.\nPlan: Discharge.",
            2: "HISTORY: Mr. Brooks, with a history of left mainstem silicone stent, presented for surveillance.\nPROCEDURE: Under moderate sedation, the airway was inspected. The left mainstem stent was in situ but significantly obstructed by tenacious secretions. Therapeutic aspiration and lavage were performed extensively to clear the lumen. Inspection of the stent post-toilet revealed no migration or granulation tissue requiring intervention. The stent was left in place.\nIMPRESSION: Stent surveillance and therapeutic aspiration (clearing).",
            3: "Coding: 31645 (Therapeutic aspiration/toilet).\nRationale:\n- Procedure involved clearing initially obstructing mucus from an existing stent.\n- No stent placement (31636/31631) or removal performed.\n- No dilation (31630).\n- 31645 describes the therapeutic work of establishing patency via suction.",
            4: "Procedure: Bronch Stent Cleanout\nPatient: Henry Brooks, 67M\nSteps:\n1. Mod sedation.\n2. Scope in.\n3. Found LMS stent plugged with mucus.\n4. Cleaned it out with saline and suction.\n5. Stent looks open now.\n6. Didn't move or change the stent.\nPlan: Home.",
            5: "Henry Brooks here for stent check. 67M. Used moderate sedation. The left main stent was clogged up with thick mucus about 60-70 percent. We spent a while suctioning and washing it out. Got it clean stent looks fine no issues. Didn't do anything else. Sending him home.",
            6: "Therapeutic flexible bronchoscopy for airway toilet. Patient 67M with LMS stent. Moderate sedation. Stent lumen occluded by mucus. Aggressive suctioning and lavage performed. Stent patent post-procedure. No stent manipulation or exchange. Complications none. Discharged.",
            7: "[Indication]\nStent surveillance, mucus burden.\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft mainstem stent inspected. Mucus plugging noted. Therapeutic aspiration/lavage performed. Stent widely patent post-procedure. No granulation treated.\n[Plan]\nRoutine follow-up.",
            8: "Mr. Brooks came in for a routine check of his airway stent. We found a significant amount of mucus clogging the stent in the left mainstem bronchus. We performed a thorough cleaning using suction and saline lavage. Once cleared, the stent looked good and was in the correct position. We did not need to replace or move the stent.",
            9: "Procedure: Therapeutic bronchoscopy with clearance of secretions.\nAction: The existing silicone prosthesis in the left mainstem was identified. Significant mucostasis was observed. The airway was cleared via lavage and aspiration. The prosthesis was retained in situ without modification.\nResult: Patency restored.",
        },
        5: { # Maria Alvarez (Rigid, debulk, dilation, stent RMS same segment) - 31636
            1: "Indication: RMS malignant obstruction.\nAnesthesia: GA, Rigid.\nProcedure:\n- Rigid scope inserted.\n- Tumor debulked (suction/forceps).\n- Balloon dilation (CRE 10-14mm) RMS.\n- Metallic stent (14x50mm) deployed RMS.\n- Post-dilation performed.\n- Dilation/stent in same segment.\nPlan: ICU.",
            2: "HISTORY: Ms. Alvarez presented with critical right mainstem obstruction.\nPROCEDURE: General anesthesia was induced. Rigid bronchoscopy facilitated access. Obstructing tumor tissue was mechanically debulked. The stenotic segment was dilated with a CRE balloon. Subsequently, a covered metallic stent was deployed into the right mainstem bronchus. Balloon expansion confirmed apposition. Note: Dilation and stenting occurred in the identical anatomical segment.\nIMPRESSION: Restoration of RMS patency via stenting.",
            3: "Coding: 31636 (Stent placement, initial bronchus).\nRationale:\n- Primary service: Placement of bronchial stent (RMS).\n- Bundling: 31630 (dilation) is NOT separately reported because it was performed in the same segment to facilitate stent placement.\n- Debulking was performed to clear channel but stent is the primary code.\n- 31622 Bundled.",
            4: "Procedure: Rigid Bronch Stent\nPatient: Maria Alvarez, 63F\nSteps:\n1. GA, Rigid scope.\n2. Cleaned out tumor in RMS.\n3. Balloon dilated the narrow spot.\n4. Put in a metal stent (14x50).\n5. Dilated inside the stent.\n6. Airway open.\nPlan: ICU.",
            5: "Procedure note Maria Alvarez 63F. RMS blockage. Did rigid bronch under GA. Debulked the tumor a bit then used a balloon to open the RMS. Put a metallic stent in right there. Blew up the balloon inside to set it. Looks wide open now. Sending to ICU for watch.",
            6: "Rigid bronchoscopy with tumor debulking, dilation, and stent placement. Patient 63F. GA. RMS obstruction. Mechanical debulking performed. Balloon dilation of RMS. Covered metallic stent deployed in RMS. Stent patent. Dilation bundled. ICU admission.",
            7: "[Indication]\nMalignant RMS obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nTumor debulked. RMS dilated. Metallic stent deployed in RMS. Post-deployment dilation performed. Good position.\n[Plan]\nICU monitoring, CXR.",
            8: "We performed a rigid bronchoscopy on Ms. Alvarez to treat her blocked right mainstem airway. After removing some of the tumor, we used a balloon to dilate the narrowing. We then placed a metallic stent in that same area to keep it open. The stent fits well and the airway is now patent.",
            9: "Procedure: Rigid bronchoscopy with prosthetic implantation.\nAction: The RMS obstruction was addressed. Tissue was debrided. The stenosis was expanded via balloon angioplasty. A metallic prosthesis was inserted into the RMS. The prosthesis was further expanded in situ.\nResult: Airway patency achieved.",
        },
        6: { # Alicia Gomez (Rigid, Cryo/APC only - No mech excision) - 31641
            1: "Indication: LLL tumor obstruction.\nAnesthesia: GA, Rigid.\nProcedure:\n- Rigid scope to LLL orifice.\n- Cryotherapy (freeze/thaw) for tumor destruction.\n- APC used for base/hemostasis.\n- NO mechanical excision/coring.\nResult: Lumen 50-60% patent.\nPlan: PACU.",
            2: "HISTORY: Ms. Gomez presented with LLL endobronchial obstruction.\nPROCEDURE: Under general anesthesia with rigid bronchoscopy, the LLL tumor was engaged. A cryoprobe was utilized for freeze-thaw ablation, resulting in tissue necrosis and sloughing. Argon Plasma Coagulation (APC) was applied for further tumor destruction and hemostasis. Mechanical debridement (coring/snare) was not employed. The airway caliber was significantly improved.\nIMPRESSION: Tumor destruction via cryotherapy and APC.",
            3: "Coding: 31641 (Tumor destruction).\nRationale:\n- Method: Cryotherapy and APC.\n- 31640 (Excision) is NOT supported as the note explicitly states 'No mechanical coring, snare resection, or microdebrider'.\n- 31641 covers destruction by any method (laser, cryo, APC).\n- 31622 Bundled.",
            4: "Procedure: Rigid Bronch Ablation\nPatient: Alicia Gomez, 74F\nSteps:\n1. GA, Rigid.\n2. Saw LLL tumor.\n3. Used Cryo probe to freeze and kill tumor.\n4. Used APC to burn the rest.\n5. Didn't cut or snare anything.\n6. Airway open better.\nPlan: PACU.",
            5: "Note for Alicia Gomez LLL tumor. Rigid bronch GA. Used the cryo probe to freeze the tumor chunks off. Then hit it with APC. Cleaned it up pretty good. No coring or cutting done just the ablation. Bleeding stopped. Extubated to PACU.",
            6: "Rigid bronchoscopy with tumor destruction. Patient 74F. GA. LLL obstruction. Cryotherapy and APC applied to tumor. Necrotic tissue removed. No mechanical excision. Lumen improved. 31641 appropriate. Extubated.",
            7: "[Indication]\nLLL tumor obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nCryotherapy applied to LLL mass. APC applied for destruction/hemostasis. Tumor destroyed. No excision performed.\n[Plan]\nPACU recovery.",
            8: "Ms. Gomez underwent a rigid bronchoscopy to treat a tumor blocking her left lower lobe. We used a cryoprobe to freeze and destroy the tumor tissue and APC to cauterize the area. We did not cut or core the tumor out, relying solely on these ablation techniques. The airway is now much more open.",
            9: "Procedure: Rigid bronchoscopy with tissue ablation.\nAction: The LLL lesion was targeted. Cryotherapy cycles were administered to induce necrosis. Argon plasma coagulation was employed for further destruction. Mechanical excision was avoided.\nResult: Destruction of endobronchial pathology.",
        },
        7: { # Marcus Lee (Hemoptysis - Hemorrhage control only) - 31634
            1: "Indication: Massive hemoptysis.\nAnesthesia: Intubated ICU, Deep sed.\nProcedure:\n- Blood in airway.\n- Source: RUL posterior seg.\n- TX: Iced saline, Epi, TXA.\n- Bleeding slowed/stopped.\n- NO biopsies taken.\nPlan: IR Embolization.",
            2: "HISTORY: Mr. Lee presented with acute hemoptysis.\nPROCEDURE: The patient was intubated. Bronchoscopy revealed active hemorrhage from the RUL posterior segment. Hemostasis was achieved utilizing serial aliquots of iced saline, topical epinephrine, and tranexamic acid. No biopsy or brushing was performed to avoid exacerbating bleeding. The airway was cleared of clots.\nIMPRESSION: Hemoptysis control. Referred to IR.",
            3: "Coding: 31634 (Bronchoscopy with control of hemorrhage).\nRationale:\n- Primary intent and action was stopping active bleeding.\n- Methods: Iced saline, Epi, TXA.\n- No diagnostic samples (31622/28/25) taken.\n- 31622 is bundled into 31634.\n- Note supports active intervention for hemorrhage.",
            4: "Procedure: Emergent Bronch for Bleed\nPatient: Marcus Lee, 62M\nSteps:\n1. Already intubated.\n2. Scope down. Lot of blood.\n3. Found bleeder in RUL.\n4. Washed with iced saline, gave Epi and TXA.\n5. Bleeding stopped.\n6. Didn't biopsy anything.\nPlan: IR.",
            5: "Emergency note for Marcus Lee. Coughing up blood. Intubated. Went down with scope. RUL bleeding active. We dumped iced saline and epi on it also TXA. Stopped the flow. Suctioned the clots out. No biopsy cause it was bleeding too much. Consult IR.",
            6: "Emergency bronchoscopy for hemoptysis. Patient 62M. Intubated. Active bleeding RUL. Hemostasis achieved with iced saline, epinephrine, TXA. No biopsies performed. 31634 supported. Plan IR embolization.",
            7: "[Indication]\nAcute hemoptysis.\n[Anesthesia]\nGeneral (Intubated).\n[Description]\nBlood suctioned. Source RUL. Iced saline, Epi, TXA instilled. Hemostasis achieved. No biopsies.\n[Plan]\nIR Bronchial Artery Embolization.",
            8: "We performed an emergency bronchoscopy on Mr. Lee due to severe bleeding. We found the source in the right upper lobe. We used iced saline, epinephrine, and TXA to stop the bleeding. We successfully controlled the hemorrhage and cleared the airway. We did not take any biopsies to prevent further bleeding.",
            9: "Procedure: Emergency bronchoscopy with hemostasis.\nAction: Significant hemorrhage observed. Source localized to RUL. Hemostatic agents (cold saline, epinephrine, TXA) administered. Bleeding arrested. No tissue sampling conducted.\nResult: Control of airway hemorrhage.",
        },
        8: { # Carolyn Smith (PleurX Pleurodesis - No new catheter) - 32560
            1: "Indication: Malignant effusion, existing PleurX.\nProcedure: Bedside pleurodesis.\n- Drained 1L fluid via existing PleurX.\n- Instilled 4g Talc slurry via PleurX.\n- Catheter clamped.\n- NO new catheter placed.\nPlan: Oncology ward.",
            2: "HISTORY: Ms. Smith, with an indwelling tunneled pleural catheter (PleurX), required pleurodesis.\nPROCEDURE: The existing catheter was accessed sterilely. 1000 mL of serosanguinous fluid was evacuated. Subsequently, a slurry containing 4 grams of talc was instilled directly through the existing indwelling catheter. The catheter was clamped to facilitate dwell time. No new thoracostomy or catheter insertion was performed.\nIMPRESSION: Chemical pleurodesis via existing IPC.",
            3: "Coding: 32560 (Pleurodesis via chest tube/catheter).\nRationale:\n- Agent: Talc slurry.\n- Access: Existing tunneled catheter.\n- 32550 (Insertion of tunneled catheter) is NOT billable as the catheter was already in place.\n- 32560 is the standalone code for the instillation.",
            4: "Procedure: PleurX Talc\nPatient: Carolyn Smith, 69F\nSteps:\n1. Sterile prep of existing PleurX.\n2. Drained fluid.\n3. Pushed talc slurry in.\n4. Clamped it.\n5. Didn't put in a new tube.\nPlan: Ward.",
            5: "Carolyn Smith here for pleurodesis. Has a PleurX already. We drained the fluid then put talc in through the PleurX line. 4 grams. Clamped it off. No new tube needed. She did fine.",
            6: "Chemical pleurodesis via existing catheter. Patient 69F. Existing PleurX. 1L drained. Talc slurry instilled via PleurX. Catheter clamped. No new placement. 32560 appropriate. Disposition ward.",
            7: "[Indication]\nRecurrent effusion, existing PleurX.\n[Anesthesia]\nLocal (lidocaine).\n[Description]\nDrained 1L fluid. Instilled Talc slurry via existing PleurX. Clamped. No new catheter.\n[Plan]\nMonitor.",
            8: "Ms. Smith has an existing PleurX catheter. Today we used it to perform a pleurodesis. We drained the fluid and then injected a talc slurry through the catheter into the pleural space. We clamped the catheter afterwards. No new procedures were needed.",
            9: "Procedure: Intrapleural administration of sclerosing agent.\nAction: The resident tunneled catheter was accessed. Effusion evacuated. Sclerosant (talc) instilled. Catheter occluded. No de novo catheterization.\nResult: Pleurodesis initiated.",
        },
        9: { # Rohan Patel (US Thoracentesis, partial drain) - 32555
            1: "Indication: Left effusion.\nProcedure: US-Guided Thoracentesis.\n- Ultrasound: Fluid loculated/small.\n- Needle inserted under US guidance.\n- 180mL removed.\n- Stopped due to cough/pain.\n- No chest tube left.\nPlan: D/C.",
            2: "HISTORY: Mr. Patel presented with a symptomatic left pleural effusion.\nPROCEDURE: Bedside ultrasound identified a pocket of fluid. Under real-time ultrasound guidance, a thoracentesis needle was advanced into the pleural space. Approximately 180 mL of fluid was aspirated. The procedure was terminated due to patient discomfort (pleuritic pain/cough). Post-procedure ultrasound ruled out pneumothorax. No catheter was left in situ.\nIMPRESSION: US-guided thoracentesis, diagnostic/therapeutic.",
            3: "Coding: 32555 (Thoracentesis with Imaging Guidance).\nRationale:\n- Ultrasound guidance was used during the procedure.\n- Fluid was removed (180mL).\n- Procedure stopped early but definition of code met.\n- No chest tube placed (excludes 32557/32551).\n- 32554 (without image guidance) is incorrect.",
            4: "Procedure: US Thoracentesis\nPatient: Rohan Patel, 58M\nSteps:\n1. US check.\n2. Lidocaine.\n3. Needle in with US watching.\n4. Got 180cc straw fluid.\n5. Patient coughed, so we stopped.\n6. Pulled needle.\nPlan: Home.",
            5: "Note for Rohan Patel. Left side tap. Used ultrasound to find the spot and guide the needle. Got about 180ml out but he started coughing and hurting so we quit. Fluid sent to lab. No pneumo. Going home.",
            6: "Ultrasound-guided thoracentesis. Patient 58M. Local anesthesia. Real-time US guidance. 180 mL fluid removed. Terminated due to symptoms. No complications. 32555 supported. Discharged.",
            7: "[Indication]\nLeft pleural effusion.\n[Anesthesia]\nLocal.\n[Description]\nUS-guided needle aspiration. 180mL removed. Stopped due to cough. No chest tube.\n[Plan]\nAnalysis of fluid.",
            8: "We performed a thoracentesis on Mr. Patel using ultrasound guidance. We found a small pocket of fluid and inserted the needle. We managed to get 180 mL of fluid out before he developed some pain and coughing, so we stopped. We didn't leave a tube in. He is safe to go home.",
            9: "Procedure: Image-guided pleural aspiration.\nAction: Sonographic localization performed. Needle introduced under guidance. Fluid aspirated (180 mL). Procedure halted due to intolerance. No drain placed.\nResult: Fluid obtained for analysis.",
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the prompt's examples
    # (In a real script, this data comes from reading the source JSON)
    return [
        {"idx": 0, "orig_name": "Lucille Sanders", "orig_age": 59, "names": ["Mary Jones", "Patricia Miller", "Linda Davis", "Barbara Wilson", "Elizabeth Taylor", "Jennifer Anderson", "Maria Thomas", "Susan Martinez", "Margaret Robinson"]},
        {"idx": 1, "orig_name": "Omar Ruiz", "orig_age": 64, "names": ["James Garcia", "John Rodriguez", "Robert Hernandez", "Michael Lopez", "William Gonzalez", "David Perez", "Richard Sanchez", "Joseph Ramirez", "Thomas Torres"]},
        {"idx": 2, "orig_name": "Tina Nguyen", "orig_age": 50, "names": ["Lisa Tran", "Nancy Le", "Karen Pham", "Betty Huynh", "Helen Hoang", "Sandra Vu", "Donna Vo", "Carol Dang", "Ruth Do"]},
        {"idx": 3, "orig_name": "Justin Fowler", "orig_age": 71, "names": ["Charles King", "Christopher Wright", "Daniel Scott", "Matthew Green", "Anthony Baker", "Donald Adams", "Mark Nelson", "Paul Carter", "Steven Mitchell"]},
        {"idx": 4, "orig_name": "Henry Brooks", "orig_age": 67, "names": ["Andrew Roberts", "Kenneth Turner", "Joshua Phillips", "Kevin Campbell", "Brian Parker", "George Evans", "Edward Edwards", "Ronald Collins", "Timothy Stewart"]},
        {"idx": 5, "orig_name": "Maria Alvarez", "orig_age": 63, "names": ["Dorothy Sanchez", "Martha Morris", "Anita Rogers", "Christine Reed", "Janet Cook", "Catherine Morgan", "Frances Bell", "Ann Murphy", "Joyce Bailey"]},
        {"idx": 6, "orig_name": "Alicia Gomez", "orig_age": 74, "names": ["Alice Rivera", "Julie Cooper", "Diane Richardson", "Evelyn Cox", "Jean Howard", "Rose Ward", "Phillis Peterson", "Marie Gray", "Norma James"]},
        {"idx": 7, "orig_name": "Marcus Lee", "orig_age": 62, "names": ["Gary Watson", "Frank Brooks", "Scott Kelly", "Eric Sanders", "Stephen Price", "Larry Bennett", "Raymond Wood", "Gregory Barnes", "Samuel Ross"]},
        {"idx": 8, "orig_name": "Carolyn Smith", "orig_age": 69, "names": ["Gloria Henderson", "Teresa Coleman", "Doris Jenkins", "Sara Perry", "Janice Powell", "Julia Long", "Grace Patterson", "Judy Hughes", "Theresa Flores"]},
        {"idx": 9, "orig_name": "Rohan Patel", "orig_age": 58, "names": ["Arjun Sharma", "Vihaan Gupta", "Aditya Singh", "Sai Kumar", "Reyansh Verma", "Krishna Mishra", "Ishaan Reddy", "Shaurya Nair", "Aarav Iyer"]}
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
                # Fallback if variation is missing (should not happen with complete data)
                note_entry["note_text"] = f"VARIATION MISSING for Note {idx} Style {style_num}"

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
    output_filename = output_dir / "synthetic_notes_part_045.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()