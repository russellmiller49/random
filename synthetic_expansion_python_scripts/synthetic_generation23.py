import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_023.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILE = "synthetic_bronch_notes_part_023.json"

def generate_random_date(year=2025):
    """Generates a random date within the specified year."""
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock names and base ages for the 5 notes in the source file.
    Note indices correspond to the order in bronch_notes_part_023.json.
    """
    return [
        {
            "idx": 0, 
            "orig_name": "Unknown (LUL Nodule Patient)", 
            "orig_age": 65, 
            "names": ["James Wilson", "Robert Chen", "Michael Rossi", "David Kim", "William Baker", "Thomas Moore", "Richard Lee", "Joseph Clark", "Charles Hall"]
        },
        {
            "idx": 1, 
            "orig_name": "Unknown (LLL Nodule Patient)", 
            "orig_age": 60, 
            "names": ["Mary Johnson", "Patricia Davis", "Jennifer Garcia", "Elizabeth Rodriguez", "Linda Martinez", "Barbara Hernandez", "Susan Lopez", "Margaret Gonzalez", "Dorothy Wilson"]
        },
        {
            "idx": 2, 
            "orig_name": "Unknown (Pleuroscopy Patient)", 
            "orig_age": 55, 
            "names": ["John Smith", "James Johnson", "Robert Williams", "Michael Brown", "William Jones", "David Garcia", "Richard Miller", "Joseph Davis", "Thomas Rodriguez"]
        },
        {
            "idx": 3, 
            "orig_name": "Unknown (Nav Bronch Patient)", 
            "orig_age": 62, 
            "names": ["Sarah Anderson", "Karen Thomas", "Nancy Jackson", "Lisa White", "Betty Harris", "Sandra Martin", "Ashley Thompson", "Kimberly Garcia", "Donna Martinez"]
        },
        {
            "idx": 4, 
            "orig_name": "Unknown (EBUS Patient)", 
            "orig_age": 68, 
            "names": ["Daniel Robinson", "Paul Clark", "Mark Rodriguez", "Donald Lewis", "George Lee", "Kenneth Walker", "Steven Hall", "Edward Allen", "Brian Young"]
        }
    ]

def get_variations():
    """
    Returns the dictionary of manually crafted text variations for the 5 notes.
    Keys are the note index (0-4). Inner keys are the style ID (1-9).
    """
    return {
        0: { # Note 0: LUL Nodule, Radial EBUS, Forceps
            1: "Procedure: Bronchoscopy, Radial EBUS, Biopsy.\n- LMA placed.\n- Inspection: Normal except fused anterior LUL segment.\n- Radial EBUS: Concentric view of LUL lesion.\n- Fluoroscopy: Used.\n- Samples: TBNA (ROSE malignant) + 6 forceps biopsies.\n- Hemostasis: Achieved.\n- Complications: None.",
            2: "OPERATIVE REPORT: DIAGNOSTIC BRONCHOSCOPY WITH ENDOBRONCHIAL ULTRASOUND\n\nINDICATION: Evaluation of a suspicious pulmonary nodule in the left upper lobe.\n\nNARRATIVE: The patient was brought to the endoscopy suite and placed under general anesthesia. Airway access was established via a laryngeal mask airway. Initial bronchoscopic inspection revealed an anatomical variant characterized by the fusion of the anterior segment of the left upper lobe with the lingula. No endobronchial lesions were overtly visible. A radial endobronchial ultrasound (REBUS) probe was deployed via a guide sheath, identifying a concentric sonographic signature corresponding to the target lesion. Transbronchial needle aspiration was performed under fluoroscopic guidance; rapid on-site evaluation (ROSE) confirmed the presence of malignant cells. Subsequently, six transbronchial forceps biopsies were obtained from the same location to ensure adequate tissue for molecular profiling. Post-biopsy inspection confirmed hemostasis. The patient tolerated the procedure without adverse events.",
            3: "PROCEDURE CODES SUPPORTED:\n- 31628 (Bronchoscopy with Transbronchial Lung Biopsy, Single Lobe): 6 forceps biopsies taken from the Left Upper Lobe under fluoroscopic guidance.\n- 31654 (Bronchoscopy with Radial EBUS, Peripheral Lesion): Radial probe inserted, concentric view obtained to localize peripheral nodule.\n\nTECHNIQUE:\nGeneral anesthesia. Fluoroscopy time utilized for guidance. Needle aspiration performed (ROSE positive). Forceps biopsies performed at same site. No complications.",
            4: "Procedure Note\nResident: Dr. Smith\nAttending: Dr. Jones\n\nSteps:\n1. Time out performed.\n2. LMA inserted.\n3. Airway inspection: Normal mostly, fused LUL anterior/lingula.\n4. Radial EBUS passed to LUL target -> Concentric view found.\n5. TBNA x 1 pass -> Malignant on ROSE.\n6. Forceps biopsy x 6 -> Good samples.\n7. Scope removed. No pneumothorax on fluoro.\n\nPlan: Discharge to home. Follow up path.",
            5: "procedure note for bronchoscopy patient had a nodule left upper lobe we used propofol and an lma airway looked ok mostly except some fused segments in the lul put the radial probe down saw the lesion concentric view used fluoro to guide the needle rose said cancer so we took 6 biopsies with the forceps no bleeding really 5cc maybe patient woke up fine check a cxr and send them home when ready.",
            6: "Procedure Name: Peripheral bronchoscopy with radial EBUS localization. Indications: Pulmonary nodule requiring diagnosis. Medications: Propofol infusion via anesthesia assistance. Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The laryngeal mask airway was in good position. The vocal cords appeared normal. The subglottic space was normal. The trachea was of normal caliber. The carina was sharp. The tracheobronchial tree was examined to at least the first subsegmental level without endobronchial lesions visualized. Anatomy was normal with exception of what appears to be a fused anterior segment of left upper lobe with lingula. The video bronchoscope was then removed and the T190 Therapeutic video bronchoscope was inserted into the airway. A sheath catheter was advanced through the working channel into the segment of suspicion. A radial US was advanced through the sheath and concentric view of lesion was seen. Using fluoroscopy, transbronchial needle biopsies were performed. ROSE was consistent with malignancy. We then performed 6 bronchoscopic lung biopsies in the same area under fluoroscopic visualization with forceps. We then removed the therapeutic scope and re-inserted the Q190 videoscope. After cleaning of blood and debris no active bleeding and none was identified. Fluoroscopy was then used to scan for evidence of pneumothorax which was not seen. The bronchoscope was removed and the procedure completed.",
            7: "[Indication]\nPulmonary nodule requiring histological diagnosis.\n[Anesthesia]\nGeneral anesthesia with Propofol; LMA used.\n[Description]\nDiagnostic inspection revealed fused LUL anterior/lingula segments. Radial EBUS confirmed concentric view of the lesion. TBNA performed (ROSE positive). 6 transbronchial biopsies taken with fluoroscopic guidance.\n[Plan]\nDischarge home. Follow up on pathology.",
            8: "The patient presented for evaluation of a pulmonary nodule. After informed consent and a time-out, anesthesia induced general sedation and placed an LMA. We introduced the bronchoscope, noting largely normal anatomy aside from a fused anterior segment of the left upper lobe. We utilized a radial EBUS probe to localize the target lesion, obtaining a clear concentric view. Under fluoroscopic guidance, we first performed needle aspiration which ROSE confirmed as malignant. We followed this with six forceps biopsies to ensure adequate tissue volume. The airway was cleared, hemostasis was confirmed, and fluoroscopy ruled out immediate pneumothorax.",
            9: "Procedure: Bronchoscopy with radial EBUS localization.\nIndications: Pulmonary lesion requiring sampling.\nAction: The Q190 scope was navigated into the airway via LMA. Inspection revealed fused LUL segments. We swapped for a therapeutic scope and deployed a radial US probe, visualizing a concentric signal. We aspirated the lesion with a needle (ROSE: malignant). We then harvested 6 tissue samples using forceps under fluoroscopy. The site was inspected and deemed stable. No pneumothorax detected."
        },
        1: { # Note 1: LLL Nodule, Radial EBUS, Forceps + Brush
            1: "Procedure: Bronchoscopy (LLL).\n- Airway: LMA.\n- Findings: Normal anatomy.\n- Target: LLL nodule.\n- Tech: Radial EBUS (concentric).\n- Samples: Forceps biopsy x1, Brush x1.\n- ROSE: Nondiagnostic.\n- Complications: None.",
            2: "PROCEDURE: Peripheral radial endobronchial ultrasound (EBUS) guided bronchoscopy.\n\nHISTORY: The patient presented with a pulmonary nodule in the left lower lobe (LLL) requiring diagnostic interrogation.\n\nOPERATIVE SUMMARY: Under general anesthesia utilizing a laryngeal mask airway, a comprehensive airway inspection was performed using a Q190 bronchoscope, revealing normal mucosa and anatomy without endobronchial lesions. A P190 ultrathin bronchoscope was subsequently employed to navigate to the peripheral LLL target. Radial EBUS localization demonstrated a concentric orientation to the lesion. Sampling was executed utilizing peripheral needle forceps and a bronchial brush. Although ROSE analysis was nondiagnostic, the procedural localization was technically successful. No immediate complications, such as significant hemorrhage or pneumothorax, were observed.",
            3: "BILLING CODES:\n- 31628: Bronchoscopy with transbronchial lung biopsy, single lobe (LLL).\n- 31623: Bronchoscopy with bronchial brushing.\n- +31654: Radial EBUS used for peripheral lesion localization.\n\nDETAILS:\nGeneral anesthesia. Ultrathin scope used. Radial probe confirmed concentric view. 1 forceps biopsy and 1 brush sample obtained. ROSE nondiagnostic.",
            4: "Resident Procedure Note\nPatient: [Name]\nAttending: Dr. X\n\nProcedure: LLL Bronchoscopy with EBUS.\n1. LMA placed by anesthesia.\n2. Initial survey with Q190: Normal exam.\n3. Switched to P190 ultrathin scope.\n4. Navigated to LLL nodule.\n5. Radial EBUS: Concentric view confirmed.\n6. Biopsy: Forceps and Brush used.\n7. ROSE: Nondiagnostic.\n8. Procedure ended, minimal bleeding.\n\nPlan: Await final path.",
            5: "patient has a nodule in the left lower lobe we did the bronchoscopy today general anesthesia with lma airway looked normal no masses in the central airways took the thin scope down to the lll found the spot with the radial ebus it was concentric used the forceps and the brush to get samples rose didnt show cancer but we think we got it no bleeding patient did fine.",
            6: "Procedure Name: Peripheral radial EBUS guided bronchoscopy. Indications: left lower lobe pulmonary nodule. Medications: via anesthesia assistance. Procedure, risks, benefits, and alternatives were explained to the patient. Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The laryngeal mask airway is in good position. The tracheobronchial tree was examined to at least the first subsegmental level. Bronchial mucosa and anatomy were normal. The bronchoscope was then removed and the P190 ultrathin video bronchoscope was inserted into the airway and based on anatomical knowledge advanced into the left lower lobe to the area of known nodule and a concentric view of the lesion was identified with the radial EBUS. Biopsies were then performed with a variety of instruments to include peripheral needle forceps and brush. After adequate samples were obtained the bronchoscope was removed. ROSE did not identify malignancy.",
            7: "[Indication]\nLeft lower lobe pulmonary nodule.\n[Anesthesia]\nGeneral anesthesia (LMA).\n[Description]\nNormal airway inspection. Ultrathin scope advanced to LLL. Radial EBUS showed concentric view. Biopsy taken with forceps and brush. ROSE nondiagnostic.\n[Plan]\nAwait final pathology.",
            8: "The patient arrived for evaluation of a left lower lobe nodule. Under general anesthesia, we secured the airway with an LMA. Initial inspection with a standard bronchoscope was unremarkable. We then utilized an ultrathin bronchoscope to access the periphery of the left lower lobe. The radial EBUS probe provided a concentric view of the lesion, confirming our location. We proceeded to sample the area using both needle forceps and a bronchial brush. While the rapid on-site evaluation was nondiagnostic, we believe the samples are representative. There were no immediate complications.",
            9: "Procedure: Peripheral radial EBUS guided bronchoscopy.\nReason: Left lower lobe lesion.\nAction: The airway was surveyed with a Q190 scope; no abnormalities found. An ultrathin P190 scope was then deployed to the LLL. Radial EBUS detected a concentric signal. The lesion was sampled using forceps and a brush. ROSE was negative. The procedure was concluded with minimal blood loss."
        },
        2: { # Note 2: Pleuroscopy, IPC, Biopsy
            1: "Procedure: Pleuroscopy + IPC Placement (Left).\n- Pos: L lateral decubitus.\n- Access: 6th intercostal space.\n- Fluid: 800cc dark/bloody removed.\n- Findings: Dense adhesions, tethered lung, inflammation.\n- Biopsy: 8 forceps biopsies parietal pleura.\n- IPC: 15.5Fr PleurX placed via separate tunnel.\n- CXR: Catheter good.",
            2: "OPERATIVE REPORT: MEDICAL THORACOSCOPY AND TUNNELED PLEURAL CATHETER PLACEMENT\n\nINDICATION: Recurrent symptomatic pleural effusion, suspected malignancy.\n\nFINDINGS: Upon entry into the left pleural space via the 6th anterior axillary line, approximately 800cc of hemorrhagic fluid was evacuated. The lung parenchyma exhibited extensive tethering to the posterior chest wall with dense adhesions preventing full visualization of the diaphragm or apex. The parietal pleura appeared relatively normal in exposed areas.\n\nPROCEDURE: Under moderate sedation and local anesthesia, a single port pleuroscopy was performed. Eight biopsies of the parietal pleura and adherent lung tissue were obtained using optical forceps. Subsequently, a PleurX indwelling pleural catheter was tunneled and inserted into the pleural space. The patient tolerated the procedure well.",
            3: "CPT CODES:\n- 32609 (Thoracoscopy with biopsy of pleura): Performed via rigid scope, 8 biopsies taken.\n- 32550 (Insertion of tunneled pleural catheter): PleurX catheter tunneled and placed via separate incision.\nNote: Thoracentesis fluid removal included in thoracoscopy.\n\nTECHNIQUE:\nLeft side. Rigid scope. 800ml drained. Biopsies taken. PleurX catheter placed and tunneled.",
            4: "Procedure Note\nResident: Dr. X\nAttending: Dr. Y\n\nProcedure: Left Pleuroscopy and PleurX.\n1. Lat decubitus position. Prep and drape.\n2. Incision 6th ICS. Trocar placed.\n3. Drained 800cc bloody fluid.\n4. Scope in: Lots of adhesions.\n5. Biopsied parietal pleura x 8.\n6. Exchanged trocar for PleurX placement.\n7. Tunneled catheter, inserted peel-away sheath.\n8. Catheter placed, incisions closed.\n\nComplications: None.",
            5: "procedure note for pleuroscopy patient had fluid on the left side we laid them on the side gave fentanyl and versed put the port in the 6th rib space drained about 800cc of bloody fluid looked inside tons of adhesions lung stuck to the wall couldnt see the diaphragm took 8 biopsies of the pleura though then put in a pleurx catheter tunneled it under the skin everything drained fine at the end wife taught how to use it.",
            6: "Procedure Name: Pleuroscopy. Indications: Pleural effusion. Medications: Fentanyl 3, versed 75, Lidocaine 30cc 1%. The patient was placed on the standard procedural bed in the L lateral decubitus position. The pleural entry site was identified by means of the ultrasound. A 5 mm disposable primary port was then placed on the left side at the 6th anterior axillary line. After allowing air entrainment and lung deflation, suction was applied through the port to remove pleural fluid with removal of approximately 800cc of dark bloody fluid. The rigid pleuroscopy telescope was then introduced. There were multiple thick adhesions and areas of lung tethering to the posterior chest wall. Biopsies of the parietal pleura posteriorly as well as areas of non-ventilated fused lung were performed with forceps. A 15.5 pleural catheter was placed into the pleural space through the primary port with tunneling anteriorly. A subcutaneous tract was then established to the guidewire insertion site with the provided blunt tunneler. The Pleurx catheter was attached to the tunneler and pulled through the subcutaneous tract.",
            7: "[Indication]\nRecurrent left pleural effusion.\n[Anesthesia]\nModerate sedation (Fentanyl/Versed) + Local Lidocaine.\n[Description]\nPleuroscopy: 800cc bloody fluid drained. Extensive adhesions noted. 8 biopsies of parietal pleura performed.\nIPC: PleurX catheter tunneled and placed.\n[Plan]\nPathology pending. Catheter education provided.",
            8: "The patient underwent a left-sided pleuroscopy for evaluation of a pleural effusion. After sedation and local anesthesia, we accessed the pleural space and drained 800cc of dark, bloody fluid. Visual inspection revealed significant adhesions and lung tethering, limiting our view of the diaphragm. We successfully obtained eight biopsies from the parietal pleura and adherent lung tissue. Following the diagnostic portion, we placed a tunneled PleurX catheter to manage the recurrent fluid. The catheter functioned well upon testing.",
            9: "Procedure: Pleuroscopy and IPC insertion.\nReason: Pleural effusion.\nAction: We accessed the left pleural space and evacuated 800cc of fluid. Inspection showed dense adhesions. We harvested 8 biopsy samples from the pleura. We then implanted a tunneled PleurX catheter for chronic drainage.\nResult: Successful placement, fluid drained."
        },
        3: { # Note 3: Nav Bronch, ICG Marking RUL
            1: "Procedure: Navigational Bronchoscopy (SuperDimension) + ICG Marking.\n- Indication: RUL nodule for resection.\n- Anesthesia: General (ETT).\n- Navigation: Reached RUL target.\n- Confirmation: Radial EBUS.\n- Action: Injected 0.75ml ICG dye.\n- Outcome: Handed off to thoracic surgery.",
            2: "OPERATIVE NARRATIVE: ELECTROMAGNETIC NAVIGATION BRONCHOSCOPY WITH DYE MARKING\n\nThe patient was placed under general anesthesia and intubated. A T190 therapeutic bronchoscope was advanced into the airway. Using the SuperDimension electromagnetic navigation system and a pre-procedural map, we navigated an edge catheter to the peripheral right upper lobe nodule. Radial EBUS was utilized to confirm proximity to the lesion. Subsequently, a needle was advanced, and 0.75 mL of Indocyanine Green (ICG) dye was injected into the subpleural space adjacent to the nodule to facilitate robotic resection. The patient was then transferred to the surgical team.",
            3: "BILLING SUMMARY:\n- 31622 (Diagnostic Bronchoscopy)\n- +31627 (Electromagnetic Navigation): SuperDimension system used to navigate to RUL target.\n- +31654 (Radial EBUS): Used to confirm lesion location.\n- Note: No biopsies performed; procedure was for fiducial/dye marking only (ICG injected).\n\nTECHNIQUE: General anesthesia. Navigational map followed. Radial probe verification. ICG marking completed.",
            4: "Procedure Note\nTrauma/Resection Marking\n\n1. Intubation with 8.5 ETT.\n2. Scope: T190.\n3. Inspection: Normal.\n4. Navigation: SuperDimension catheter to RUL nodule.\n5. Confirmation: Radial EBUS.\n6. Intervention: Injected ICG dye for surgeon.\n7. Scope out. Surgery to follow.",
            5: "doing a nav bronch today for a rul nodule surgeon wants it marked patient asleep tube in airway looked fine used the superdimension stuff to get out to the nodule radial ebus confirmed we were there injected some icg green dye right next to it pulled the scope out and let the robot team take over no bleeding.",
            6: "PROCEDURE PERFORMED: Flexible bronchoscopy with electromagnetic navigation under flouroscopic and EBUS guidance with isocyanate green dye injection for surgical resection. FINDINGS: Following intravenous medications as per the record the patient was intubated with an 8. 5 ET tube by anesthesia. The T190 video bronchoscope was then introduced through the endotracheal tube and advanced to the tracheobronchial tree. The trachea was of normal caliber. The carina was sharp. The super-dimension navigational catheter was inserted through the T190 therapeutic bronchoscope and advanced into the airway. Using the navigational map created preprocedurally we advanced the 180 degree edge catheter into the proximity of the right upper lobe nodule. Radial probe was used to attempt to confirm presence within the lesion. A super dimension needle was then inserted through the bronchoscope and 0.75 milliliters of isocyanate Green were injected just below the pleura adjacent to the nodule for planned robotic surgical resection immediately following.",
            7: "[Indication]\nPre-operative marking of RUL nodule.\n[Anesthesia]\nGeneral (8.5 ETT).\n[Description]\nNavigated to RUL nodule using SuperDimension. Confirmed with Radial EBUS. Injected 0.75ml ICG dye subpleurally.\n[Plan]\nProceed to robotic resection.",
            8: "The patient required marking of a right upper lobe nodule prior to surgical resection. Under general anesthesia, we navigated to the lesion using the SuperDimension electromagnetic system. We confirmed our position adjacent to the nodule using a radial EBUS probe. Once confirmed, we injected 0.75 mL of Indocyanine Green dye to tattoo the area for the surgeon. The bronchoscope was removed, and the surgical team assumed care.",
            9: "Procedure: Navigational bronchoscopy with dye tattooing.\nReason: RUL nodule marking.\nAction: We navigated the scope to the RUL target using electromagnetic guidance. Radial EBUS verified the location. We deposited ICG dye into the tissue to flag the lesion for the surgeon.\nResult: Successful marking."
        },
        4: { # Note 4: EBUS-TBNA (11L, Lung Mass)
            1: "Procedure: EBUS-TBNA.\n- Scope: UC180F.\n- Stations: 11L (Lymphocytes), LLL Lung Mass (Malignant).\n- Needle: 21G.\n- Passes: 6 at 11L, 8 at Mass.\n- Complications: None.\n- Plan: Oncology referral.",
            2: "OPERATIVE REPORT: ENDOBRONCHIAL ULTRASOUND TRANSBRONCHIAL NEEDLE ASPIRATION (EBUS-TBNA)\n\nINDICATION: Diagnosis and staging of a left lower lobe lung mass.\n\nFINDINGS: Diagnostic bronchoscopy revealed extrinsic compression of the LLL superior segment. EBUS examination identified a 7mm lymph node at station 11L and a 31.5mm mass abutting the airway in the LLL. \n\nSAMPLING: \n1. Station 11L: 6 passes. ROSE showed lymphocytes.\n2. LLL Mass: 8 passes. ROSE consistent with malignancy.\n\nCONCLUSION: Successful EBUS-TBNA confirming malignancy in the primary mass. Nodal staging pending final pathology.",
            3: "CPT CODE: 31652 (EBUS-TBNA 1-2 stations).\n- Target 1: Station 11L lymph node.\n- Target 2: LLL Lung Mass (structural target).\n\nDETAILS:\nAirway exam performed. EBUS scope used. 21G needle. Adequate sampling confirmed by ROSE. Specimen sent for molecular testing.",
            4: "Resident Note\nPatient: [Name]\nProcedure: EBUS-TBNA\n\n1. LMA placed.\n2. White light bronch: Extrinsic compression LLL.\n3. EBUS scope inserted.\n4. Surveyed mediastinum/hila.\n5. Sampled 11L (benign on ROSE).\n6. Sampled LLL Mass (malignant on ROSE).\n7. No complications.\n\nPlan: Wait for final path.",
            5: "ebus procedure for a lung mass in the left lower lobe anesthesia put the lma in airway looked ok except for some squashing in the lll used the ebus scope 11l node looked big enough so we sampled it rose said just lymph cells then we poked the mass itself it was huge 31mm rose said cancer took a bunch of passes for genetics no bleeding patient fine.",
            6: "PROCEDURE TECHNIQUE: Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced. A systematic hilar and mediastinal lymph node survey was carried out. Sampling criteria (5mm short axis diameter) was met in station 11L lymph node. The EBUS scope was positioned in the origin of the left lower lobe and turned posteriorly to visualize the lung mass abutting the airway which measured 31.5mm in short axis diameter. Sampling by transbronchial needle aspiration was performed beginning with the 11L Lymph node using an Olympus EBUSTBNA 21 gauge needle. ROSE indicated adequate lymph node sampling. We then reintroduced the EBUS scope into the left lower lobe and visualized the mass abutting the airway and EBUS guided sampling was performed of the mass with the EBUSTBNA 21 gauge needle. ROSE evaluation yielded tissue concerning for malignancy.",
            7: "[Indication]\nLeft lower lobe mass diagnosis and staging.\n[Anesthesia]\nModerate sedation/General (LMA).\n[Description]\nEBUS survey performed. Station 11L sampled (benign ROSE). LLL Mass abutting airway sampled (malignant ROSE). 21G needle used.\n[Plan]\nPathology pending.",
            8: "The patient underwent EBUS-TBNA for evaluation of a left lower lobe mass. After inspecting the airway and noting extrinsic compression, we switched to the EBUS scope. We identified and sampled a lymph node at station 11L, which showed benign lymphocytes on-site. We then visualized the primary mass abutting the LLL airway and performed needle aspiration. On-site evaluation of the mass was consistent with malignancy. Multiple passes were taken for molecular profiling.",
            9: "Procedure: EBUS-TBNA.\nReason: Mass diagnosis.\nAction: We surveyed the nodes with EBUS. Station 11L was aspirated (ROSE: benign). The LLL mass was then targeted and aspirated (ROSE: malignant). Specimens were harvested for molecular analysis.\nResult: Malignancy confirmed."
        }
    }

def main():
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file '{SOURCE_FILE}' not found.")
        return
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Loop through each original note
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Generate 9 variations
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # Randomize Age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # Randomize Date
            rand_date_obj = generate_random_date(2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get Name
            new_name = record['names'][style_num - 1]
            
            # Update content
            note_entry["note_text"] = variations_text[idx][style_num]
            
            if "registry_entry" in note_entry:
                # Update MRN
                orig_mrn = note_entry["registry_entry"].get("patient_mrn", "UNKNOWN")
                note_entry["registry_entry"]["patient_mrn"] = f"{orig_mrn}_syn_{style_num}"
                
                # Update Date
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update Age (if present in structure, usually derived or in demographics)
                # The provided json schema varies, checking common locations
                if "patient_demographics" in note_entry["registry_entry"]:
                     # Sometimes demographics is null in source, we can init it if needed or skip
                     pass 
                
                # Because the source schema has patient_age at top level of registry_entry in BLVR examples
                # but might be different here, let's inject it if not strictly defined or just update metadata
                # For this specific dataset, let's assume we might need to inject a 'patient_age' field 
                # into registry_entry for consistency if it was missing, or update it if present.
                note_entry["registry_entry"]["patient_age"] = new_age

            # Add Synthetic Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)
            
    # Save Output
    output_path = output_dir / OUTPUT_FILE
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated {len(generated_notes)} notes in {output_path}")

if __name__ == "__main__":
    main()