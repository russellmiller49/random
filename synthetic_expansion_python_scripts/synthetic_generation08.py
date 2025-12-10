import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_008.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-8) -> Style_Index (1-9) -> Text
    # Note 0: Robert Chen (Left PleurX)
    # Note 1: Sandra Martinez (Right Pleuroscopy/Talc)
    # Note 2: Sarah Chen (Right Thoracentesis)
    # Note 3: Roberto Martinez (EBUS)
    # Note 4: Emma Thompson (Peds Rigid Bronch FB)
    # Note 5: Aisha Patel (Right Thoracentesis/Complex)
    # Note 6: Christopher Hayes (Rigid Bronch Stenosis/Trauma)
    # Note 7: Elizabeth Thompson (Right Pleuroscopy)
    # Note 8: Michael Brown (EBUS)

    variations = {
        0: { # Robert Chen (Left PleurX)
            1: "Pre-op: Recurrent left malignant effusion. Lung expands on CT.\nProcedure: US marked. Local anesthetic. Tunnel created. 15.5Fr PleurX inserted via peel-away sheath. Fluoroscopy confirmed position. 1350mL drained. No complications.\nPlan: Home drainage training. Discharge.",
            2: "HISTORY: Mr. Chen, a 73-year-old gentleman with metastatic adenocarcinoma, presented for management of a recalcitrant left pleural effusion.\nPROCEDURE: Under ultrasound guidance, the left hemithorax was accessed. A subcutaneous tunnel was fashioned to the anterior chest wall. A 15.5 French tunneled indwelling pleural catheter was advanced into the pleural space. Fluoroscopic verification demonstrated appropriate catheter lie. Spontaneous drainage of 1,350 mL of serous fluid was achieved without re-expansion edema.\nIMPRESSION: Successful IPC placement for palliative effusion management.",
            3: "Service: Insertion of Tunneled Pleural Catheter (32550).\nGuidance: Ultrasound and Fluoroscopy utilized.\nDevice: 15.5 Fr PleurX Catheter.\nDetails:\n1. Site identification (Left 5th ICS).\n2. Tunneling (8cm tract created).\n3. Seldinger technique insertion with peel-away sheath.\n4. Cuff positioning within tunnel confirmed.\n5. Drainage of 1,350 mL fluid.\nMedical Necessity: Recurrent malignant effusion requiring long-term intermittent drainage.",
            4: "Procedure: PleurX Catheter Placement (Left)\nAttending: Dr. Johnson\nSteps:\n1. Time out. Sterile prep/drape.\n2. US scan: Large effusion, no loculations.\n3. Local Lidocaine.\n4. Incision made, tunnel created.\n5. Needle access -> wire -> dilator -> sheath.\n6. Catheter placed. Cuff in tunnel.\n7. 1350cc drained.\n8. Dressing applied.\nPlan: Video education for home drainage.",
            5: "Procedure note for mr chen needing the pleurx catheter left side lung cancer recurrent fluid. We marked it with ultrasound 5th intercostal space prepped with chlorhexidine numbed it up good tunnel made about 8 cm. Put the needle in got fluid wire went in easy. Dilated it up put the sheath in then the 15.5 french catheter. Cuff is in the tunnel good. Drained like 1350 of yellow fluid no blood. Patient tolerated it fine vitals stable. Spoke to wife about how to drain it at home.",
            6: "Left-sided indwelling pleural catheter placement was performed on Robert Chen. The patient has metastatic lung adenocarcinoma with recurrent effusion. Ultrasound confirmed a large free-flowing effusion. Under local anesthesia, a subcutaneous tunnel was created. A 15.5 French PleurX catheter was inserted using the Seldinger technique under ultrasound and fluoroscopic guidance. 1,350 mL of straw-colored fluid was drained. The catheter cuff was positioned within the tunnel. The patient tolerated the procedure well with no immediate complications.",
            7: "[Indication]\nSymptomatic recurrent left malignant pleural effusion, metastatic adenocarcinoma.\n[Anesthesia]\nLocal infiltration (Lidocaine 1%).\n[Description]\nUltrasound guidance used. Tunnel created. 15.5 Fr PleurX catheter inserted into left pleural space. Cuff positioned in tunnel. 1,350 mL fluid drained. Position confirmed via fluoro.\n[Plan]\nHome health setup. Drain QOD. Discharge.",
            8: "The patient was brought to the procedure room for elective PleurX placement. After positioning in the right lateral decubitus position, we identified the optimal site on the left chest using ultrasound. A small incision was made and a tunnel created subcutaneously. The pleural space was accessed with a needle, followed by a guidewire. We dilated the tract and inserted the 15.5 French catheter. Once connected, 1,350 mL of fluid drained easily. The catheter was secured, and the patient reported immediate relief of dyspnea.",
            9: "Operation: Implantation of tunneled pleural drain.\nTarget: Left pleural cavity.\nAction: The site was mapped with ultrasound. A tract was tunneled. The 15.5 Fr device was deployed into the pleural space. Verification was achieved via fluoroscopy. 1,350 mL of effusion was evacuated.\nOutcome: Device functional. Dyspnea alleviated."
        },
        1: { # Sandra Martinez (Right Pleuroscopy)
            1: "Indication: New right effusion, hx breast CA.\nProcedure: Right medical thoracoscopy. 6th ICS. 7mm rigid scope.\nFindings: Diffuse parietal/visceral nodules (breast CA mets).\nAction: 12 biopsies taken. 1450mL bloody fluid removed. 5g Talc insufflated. 28Fr chest tube placed.\nComplication: Transient hypoxia, resolved.",
            2: "OPERATIVE NARRATIVE: The patient underwent right-sided medical pleuroscopy for diagnostic staging of a suspected malignant effusion. A single port entry was established in the 6th intercostal space. Visualization revealed extensive carcinomatosis with nodular studding of both the parietal and visceral pleurae. Multiple biopsies were obtained using optical forceps. Given the gross appearance of malignancy and adequate lung expansion, talc poudrage (5 grams) was performed for pleurodesis. A 28 French thoracostomy tube was positioned apically.",
            3: "Code: 32650 (Thoracoscopy, surgical; with pleurodesis).\nNote: Includes diagnostic biopsy and drainage.\nTechnique: Rigid pleuroscopy via trocar.\nPathology: Biopsies of parietal (8) and visceral (4) pleura obtained.\nTherapy: Complete drainage (1,450 mL) followed by insufflation of 5g sterile Talc. Chest tube (28Fr) placed.\nMedical Necessity: Exudative effusion with high suspicion of malignancy.",
            4: "Procedure: Right Medical Thoracoscopy\nPatient: Sandra Martinez\nSteps:\n1. MAC anesthesia. Left lat decubitus.\n2. US guidance -> 6th ICS access.\n3. Trocar placed. Scope inserted.\n4. Findings: extensive nodules.\n5. Biopsies: 12 total taken.\n6. Talc: 5g sprayed.\n7. Chest tube: 28Fr placed.\nPlan: Admit, watch chest tube output.",
            5: "sandra martinez here for the scope procedure right side shes got breast cancer history. We went in with the camera right side 6th space saw tons of nodules everywhere looks like mets. took a bunch of biopsies to be sure. drained the fluid about 1.4 liters it was bloody. put in 5 grams of talc for the pleurodesis since the lung looked like it expanded okay. chest tube in 28 french secured with silk. she desatted a little bit during drainage but came right back up with oxygen.",
            6: "Right medical pleuroscopy was performed for a 53-year-old female with recurrent effusion and breast cancer history. Under MAC, a port was established in the right lateral chest. 1,450 mL of hemorrhagic fluid was evacuated. Inspection revealed extensive nodular disease on parietal and visceral surfaces. Twelve biopsies were obtained. Five grams of sterile talc were insufflated for pleurodesis. A 28 French chest tube was placed. There was a brief episode of hypoxemia managed with supplemental oxygen.",
            7: "[Indication]\nRight pleural effusion, suspected metastatic breast cancer.\n[Anesthesia]\nMAC (Propofol/Fentanyl).\n[Description]\nRight chest accessed. 800mL bloody fluid initially, 1450mL total. Diffuse nodules seen. 12 biopsies taken. 5g Talc insufflated. 28Fr Chest tube placed.\n[Plan]\nAdmit. Suction -20cmH2O. Pain control.",
            8: "Ms. Martinez underwent a right-sided pleuroscopy today. We accessed the chest wall and drained the fluid, which was bloody. Upon inserting the scope, it was immediately apparent that there were extensive nodules covering the lining of the lung and chest wall, consistent with her history of breast cancer. We took multiple biopsies for confirmation. Since the lung expanded well, we decided to proceed with talc pleurodesis to prevent the fluid from coming back. We sprayed 5 grams of talc and left a chest tube in place.",
            9: "Procedure: Right medical thoracoscopy with biopsy and pleurodesis.\nFindings: Widespread nodular implants on the pleural surfaces.\nAction: The effusion was evacuated. Tissue was sampled using optical forceps. Talc was dispersed for chemical pleurodesis. A drainage tube was positioned.\nOutcome: Successful visualization and therapeutic intervention."
        },
        2: { # Sarah Chen (Right Thoracentesis)
            1: "Dx: Large R pleural effusion (Metastatic Breast CA).\nProc: US guided thoracentesis.\nSite: R 8th ICS.\nAction: 18G needle. 1200mL straw fluid removed.\nStop: Pt reported chest discomfort.\nResult: No pneumothorax. Dyspnea improved.",
            2: "PROCEDURE NOTE: Bedside thoracentesis was performed for symptomatic relief of a large right-sided pleural effusion. Ultrasound localization identified an ideal pocket in the 8th intercostal space. Under sterile conditions, the pleural space was accessed utilizing an 18-gauge catheter-over-needle assembly. Approximately 1.2 liters of serous fluid were withdrawn. The procedure was terminated due to the onset of vague chest discomfort, likely related to rapid lung re-expansion. Post-procedure imaging confirmed the absence of pneumothorax.",
            3: "CPT: 32555 (Thoracentesis with imaging guidance).\nGuidance: Real-time ultrasound used to determine site and depth (8.2cm).\nVolume: 1,200 mL removed.\nStatus: Therapeutic and diagnostic.\nNote: No indwelling catheter placed. Procedure terminated due to symptoms (chest discomfort).",
            4: "Resident Note: Thoracentesis\nPatient: Sarah Chen\nSide: Right\nSteps:\n1. Consent/Timeout.\n2. US check: fluid found 8th ICS.\n3. Lidocaine local.\n4. Needle in -> fluid return.\n5. Drained 1200cc via gravity.\n6. Stopped when patient felt pain.\n7. Bandage applied.\nPlan: Send fluid for cytology/cx.",
            5: "Procedure note sarah chen 66 female right effusion. We did the tap at the bedside used ultrasound to find the spot 8th rib space. Numbed it up put the catheter in. Pulled off about 1200 mls of clear yellow fluid. She started saying her chest hurt a little so we stopped there. Ultrasound after showed lung sliding no pneumo. Sent fluid to lab.",
            6: "Ultrasound-guided right thoracentesis performed on 66-year-old female with metastatic breast cancer. Site identified at 8th intercostal space. 18-gauge catheter inserted. 1,200 mL of straw-colored fluid removed via gravity drainage. Procedure halted due to mild chest discomfort. Post-procedure ultrasound showed no pneumothorax. Patient reported improvement in dyspnea. Fluid sent for analysis and cytology.",
            7: "[Indication]\nSymptomatic large right pleural effusion, breast cancer.\n[Anesthesia]\nLocal Lidocaine.\n[Description]\nUS guidance used. Right 8th ICS accessed. 1,200 mL straw-colored fluid removed. Stopped due to chest discomfort. No pneumothorax.\n[Plan]\nCXR. Monitor. Await cytology.",
            8: "We performed a thoracentesis on Ms. Chen to relieve her shortness of breath. Using ultrasound, we found a large pocket of fluid on the right side. We were able to drain 1.2 liters of clear fluid. Towards the end, she mentioned some chest discomfort, which is common when the lung re-expands, so we decided to stop there. She felt better breathing-wise immediately after. We checked with ultrasound and didn't see any complications.",
            9: "Procedure: Ultrasound-guided pleural aspiration.\nSite: Right hemithorax.\nAction: The pleural space was cannulated. 1,200 mL of effusion was withdrawn. The session was concluded due to patient discomfort.\nOutcome: Improved respiratory status. No immediate adverse events."
        },
        3: { # Roberto Martinez (EBUS)
            1: "Indication: 62mm R paratracheal node.\nProc: EBUS-TBNA.\nStation 2R: 24mm, 5 passes, atypia.\nStation 4R: 31mm, 4 passes, POSITIVE adenocarcinoma.\nStation 7: 18mm, 3 passes, benign.\nPlan: Oncology referral.",
            2: "DIAGNOSTIC BRONCHOSCOPY: Endobronchial ultrasound (EBUS) was utilized to stage the mediastinum. Systematic evaluation revealed significant lymphadenopathy. Transbronchial needle aspiration (TBNA) was performed at station 4R (31mm), yielding a diagnosis of adenocarcinoma on rapid on-site evaluation (ROSE). Additional sampling of stations 2R and 7 was performed for completeness. Elastography scores correlated with malignant potential in station 4R.",
            3: "Code: 31653 (Bronchoscopy with EBUS sampling 3+ stations).\nStations Sampled: 2R, 4R, 7 (Total 3 distinct mediastinal stations).\nTechnique: Linear EBUS, 22G needle, multiple passes per station.\nResults: Malignancy confirmed in 4R. Benign/Atypia in others.\nJustification: Staging of mediastinal adenopathy.",
            4: "Procedure: EBUS-TBNA\nPatient: Roberto Martinez\nStations:\n- 2R: 5 passes (atypia)\n- 4R: 4 passes (Adeno CA)\n- 7: 3 passes (Benign)\nEquipment: 22G needle.\nComplications: None.\nPlan: Consult Onc.",
            5: "Done ebus on mr martinez for the big node in the neck area. Sedation was moderate fentanyl versed. Looked with the linear scope. Station 4R was huge 31mm poked it 4 times cytology said it looks like cancer adenocarcinoma. Also checked 2R and 7 just to be thorough. 2R was atypical 7 was benign. No bleeding really. Patient woke up fine.",
            6: "EBUS-TBNA performed for 62mm right paratracheal lymphadenopathy. Moderate sedation used. Systematic survey showed enlarged nodes. Station 2R (24mm) sampled x5. Station 4R (31mm) sampled x4; ROSE positive for adenocarcinoma. Station 7 (18mm) sampled x3. Minimal bleeding. Diagnosis of N2 disease confirmed via station 4R. Plan for oncology staging.",
            7: "[Indication]\nMediastinal lymphadenopathy, r/o malignancy.\n[Anesthesia]\nModerate (Fentanyl/Midazolam).\n[Description]\nEBUS scope. Stations 2R, 4R, 7 sampled. Station 4R positive for Adenocarcinoma. Elastography high score on 4R.\n[Plan]\nFinal path pending. Oncology referral.",
            8: "Mr. Martinez underwent an EBUS procedure to investigate the enlarged lymph nodes in his chest. We focused on station 4R, which was quite large. The pathologist in the room confirmed cancer cells (adenocarcinoma) from that node. We also sampled stations 2R and 7 to complete the staging; those looked less concerning. The procedure went smoothly with no complications.",
            9: "Procedure: Endosonographic mediastinal staging.\nAction: Targeted needle aspiration of nodal stations 2R, 4R, and 7.\nFindings: Station 4R yielded malignant cells (Adenocarcinoma). Station 2R showed atypia. Station 7 appeared benign.\nOutcome: Confirmed malignancy in mediastinum."
        },
        4: { # Emma Thompson (Rigid Bronch FB)
            1: "Indication: 3yo F, peanut aspiration.\nProc: Rigid Bronchoscopy.\nFindings: Peanut fragment 2cm distal to carina in RMB.\nAction: Optical forceps used. Fragment removed intact (8x5mm).\nResult: Airway patent. Mucosa mild edema.\nPlan: Observe overnight.",
            2: "OPERATIVE REPORT: The pediatric patient was induced under general anesthesia. A 3.5mm rigid bronchoscope was introduced. Inspection of the right mainstem bronchus revealed an organic foreign body consistent with a peanut. Optical forceps were utilized to grasp and retrieve the object en bloc. Post-extraction inspection demonstrated patent airways bilaterally with minor mucosal erythema at the site of impaction.",
            3: "Code: 31635 (Bronchoscopy with removal of foreign body).\nTechnique: Rigid bronchoscopy (essential for airway control in pediatric FB).\nDetails: Visualization of FB in Right Mainstem. Removal using optical forceps and telescope withdrawal technique.\nOutcome: Complete removal of 8mm peanut fragment.",
            4: "Resident Note: Rigid Bronch FB Removal\nPatient: Emma Thompson (3yo)\nIndication: Choking on peanut.\nSteps:\n1. GA / Spontaneous vent.\n2. Rigid scope inserted.\n3. Saw peanut in Right Mainstem.\n4. Grabbed with optical forceps.\n5. Pulled scope and forceps out together.\n6. Re-looked: airway clear.\nPlan: CXR, discharge tomorrow.",
            5: "Procedure rigid bronch for emma thompson 3 years old she choked on a peanut. We put her to sleep kept her breathing on her own. Went in with the storz scope saw the peanut in the right lung main bronchus. Grabbed it with the forceps pulled it out carefully so it didnt break. It came out whole. Went back in looked around everything clear just a little red. She woke up fine.",
            6: "Rigid bronchoscopy performed for foreign body aspiration in 3-year-old female. General anesthesia. 3.5mm rigid scope used. Peanut fragment identified in right mainstem bronchus. Removed intact using optical forceps. Final inspection showed patent airways and mild mucosal edema. Extubated in OR. Plan for overnight observation.",
            7: "[Indication]\nForeign body aspiration (peanut), right lung hyperinflation.\n[Anesthesia]\nGeneral, spontaneous ventilation.\n[Description]\nRigid bronchoscopy. Peanut found in RMB. Removed intact with optical forceps. Mucosa edematous but intact.\n[Plan]\nCXR. Overnight obs. D/C AM.",
            8: "Little Emma was brought to the OR because of the peanut she inhaled. We used a rigid bronchoscope to look into her lungs while she was asleep. We found the peanut piece stuck in the main tube leading to her right lung. Using special forceps, we were able to grab it and pull it out in one piece without it breaking apart. We checked again to make sure we got it all, and the airway looked clear.",
            9: "Operation: Rigid endoscopic foreign body retrieval.\nSubject: 3-year-old female.\nFindings: Organic obstruction (peanut) in the right mainstem bronchus.\nAction: The object was engaged with optical forceps and extracted.\nResult: Restoration of airway patency."
        },
        5: { # Aisha Patel (Right Thoracentesis - Complex)
            1: "Indication: Persistent R effusion, pneumonia.\nProc: US guided thoracentesis.\nFindings: Turbid fluid, loculations on US.\nAction: 420mL drained. pH 7.18, Glucose 32.\nAssessment: Complicated parapneumonic effusion.\nPlan: Consult Thoracic Surgery for VATS/Chest tube.",
            2: "PROCEDURE: Diagnostic thoracentesis. Ultrasound interrogation revealed a complex, septated effusion. Access was achieved, yielding turbid fluid. Analysis demonstrated a pH of 7.18 and glucose of 32 mg/dL, diagnostic of a complicated parapneumonic effusion or empyema. Drainage was incomplete due to viscosity and loculation. Immediate surgical consultation was requested for definitive drainage.",
            3: "Code: 32555 (Thoracentesis with imaging guidance).\nNote: Procedure was diagnostic and attempted therapeutic.\nVolume: 420 mL (limited by viscosity).\nComplexity: Fluid analysis (pH 7.18) confirms complicated effusion requiring higher level of care (Chest tube/VATS).\nPlan: Admission and escalation of care.",
            4: "Procedure: Thoracentesis\nPatient: Aisha Patel\nSteps:\n1. US: complex fluid.\n2. Local numbing.\n3. Needle in.\n4. Fluid very thick/cloudy.\n5. Only got 420cc out.\n6. Labs: pH 7.18 (Bad).\nPlan: Needs chest tube or surgery. Admitting.",
            5: "Did a tap on Ms Patel she has that pneumonia that wont go away. Fluid on the right side looked gross on ultrasound thick stuff. Put the needle in and it was cloudy yellow hard to pull out. Only got about 400 mls. Ran the pH right away it was 7.18 so thats an empyema or complicated effusion. She needs a tube or surgery cant just tap this. Admitting her.",
            6: "Ultrasound-guided thoracentesis performed on 43-year-old female with persistent pneumonia. Right pleural effusion appeared complex on ultrasound. 420 mL of turbid fluid removed. Flow was poor due to viscosity. Point-of-care analysis showed pH 7.18 and glucose 32. Findings consistent with complicated parapneumonic effusion. Antibiotics initiated. Surgical consult for chest tube/decortication.",
            7: "[Indication]\nParapneumonic effusion, rule out empyema.\n[Anesthesia]\nLocal Lidocaine.\n[Description]\nUS guided needle aspiration. Fluid turbid/purulent. 420mL removed. pH 7.18.\n[Plan]\nAdmit. IV Antibiotics. Consult Thoracic Surgery.",
            8: "Ms. Patel has a fluid collection that looks infected. We tried to drain it with a needle, but the fluid was very thick and cloudy. We only got a little bit out. The tests on the fluid confirm it's a complicated infection (low pH), so a simple needle drain isn't enough. She is going to need a chest tube or maybe a small surgery to clean it out properly.",
            9: "Procedure: Diagnostic pleural aspiration.\nFindings: Turbid, viscous effusion with low pH (7.18).\nAction: Partial evacuation (420 mL) accomplished.\nInterpretation: Complicated parapneumonic effusion.\nStrategy: Escalate to tube thoracostomy or surgical decortication."
        },
        6: { # Christopher Hayes (Rigid Bronch Stenosis/Trauma)
            1: "Indication: L mainstem stenosis (GPA).\nProc: Rigid Bronchoscopy + Dilatation.\nComplication: L mainstem tear, pneumothorax.\nAction: Fibrin glue applied. 14Fr Pigtail chest tube placed.\nPlan: ICU, keep intubated, CT Surgery consult.",
            2: "OPERATIVE SUMMARY: The patient underwent rigid bronchoscopy for high-grade left mainstem stenosis secondary to granulomatosis with polyangiitis. Mechanical dilation and APC recanalization were attempted. During the procedure, a false lumen communicating with the pulmonary artery interface was suspected, and a pneumothorax developed. Fibrin sealant was applied endobronchially. A left-sided thoracostomy tube was placed immediately for pneumothorax management. The patient was transferred to the ICU intubated.",
            3: "Codes: 31641 (Bronchoscopy with stenosis relief), 32551 (Tube thoracostomy).\nNarrative: Rigid bronchoscopy with lysis of adhesions (knife/APC) and balloon dilation. Complicated by airway perforation and pneumothorax requiring emergent chest tube placement (32551). Fibrin glue used for hemostasis/seal.",
            4: "Resident Note: Rigid Bronch / Complication\nPatient: Christopher Hayes (14M)\nHistory: Wegener's stenosis.\nEvents:\n1. Rigid scope inserted.\n2. L mainstem 90% blocked.\n3. Tried dilating/cutting.\n4. Saw pulsatile vessel (scary).\n5. Patient desatted, CXR showed pneumo.\n6. Put in chest tube (14Fr pigtail).\n7. Glued the airway.\nPlan: PICU, keep intubated.",
            5: "Procedure note for chris hayes 14 year old with the bad stenosis from gpa. We went in with the rigid scope tried to open up the left bronchus it was tight. Used the knife and the balloon. Eventually we saw what looked like the PA so we stopped. He dropped his lung got a pneumothorax. Put a pigtail chest tube in right away. Glued the hole in the airway. Sent him to PICU intubated. Scary case.",
            6: "Rigid bronchoscopy performed for severe left mainstem stenosis. APC and mechanical dilation utilized. Procedure complicated by airway perforation and left pneumothorax. Fibrin glue applied to endobronchial defect. 14 French pigtail catheter placed in left hemithorax. Patient remained intubated and transferred to PICU for stabilization and surgical evaluation.",
            7: "[Indication]\nLeft mainstem bronchial stenosis (GPA).\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Knife/APC/Balloon dilation attempted. Perforation noted. Pneumothorax diagnosed. Fibrin glue applied. 14Fr Chest tube placed.\n[Plan]\nPICU. Mechanical Ventilation. CT Surgery consult.",
            8: "This was a difficult case involving a young man with a blocked airway from his vascular disease. We tried to carefully open the left airway using balloons and heat, but the scarring was very severe. During the attempt, a small tear occurred, leading to a collapsed lung. We immediately placed a chest tube to re-expand the lung and used surgical glue to seal the tear from the inside. He is stable but will stay asleep on the breathing machine in the ICU while we figure out the next steps.",
            9: "Operation: Rigid bronchoscopic recanalization.\nComplication: Iatrogenic airway perforation and pneumothorax.\nIntervention: Endobronchial application of fibrin sealant. Emergent tube thoracostomy.\nDisposition: Critical care unit admission."
        },
        7: { # Elizabeth Thompson (Right Pleuroscopy)
            1: "Indication: Recurrent R effusion, negative cytology.\nProc: Medical Pleuroscopy.\nFindings: Multifocal nodules (parietal/visceral).\nAction: 10 biopsies. 1250mL drained. 5g Talc pleurodesis. 28Fr Chest tube.\nDx: Suspicious for lymphoma/mets.",
            2: "PROCEDURE: Right-sided medical thoracoscopy. A single access port was utilized. Inspection revealed disseminated nodular disease involving the visceral and parietal pleurae, distinct from the typical appearance of adenocarcinoma, raising suspicion for lymphoma. Extensive biopsies were taken for flow cytometry and histology. Given the recurrent nature of the effusion, talc poudrage was performed to achieve pleurodesis. A chest tube was placed for drainage.",
            3: "Code: 32650 (Thoracoscopy with pleurodesis).\nTechnique: Rigid pleuroscopy.\nBiopsy: Multiple biopsies taken (sent for Flow Cytometry).\nTherapy: Talc insufflation (5g) + Chest tube placement.\nMedical Necessity: Undiagnosed exudative effusion requiring tissue diagnosis and management.",
            4: "Procedure: Right Pleuroscopy\nPatient: Elizabeth Thompson\nSteps:\n1. Local/MAC.\n2. Port placed 6th ICS.\n3. Drained 1250cc.\n4. Saw nodules everywhere.\n5. Biopsied (sent for flow).\n6. Sprayed Talc.\n7. Chest tube in.\nPlan: Ward, pain control, watch drainage.",
            5: "Elizabeth Thompson procedure note right side scope. She keeps getting fluid we dont know why. Went in with the camera saw nodules all over looked a bit like lymphoma maybe. Took 10 biopsies sent some fresh for flow. Drained the fluid put in talc to stick the lung. Chest tube placed 28 french. Patient did fine.",
            6: "Medical pleuroscopy, right side. Patient is 71-year-old female with undiagnosed recurrent effusion. 1,250 mL fluid removed. Multifocal small nodules visualized on parietal and visceral pleura. Biopsies taken for pathology and flow cytometry. Talc pleurodesis (5g) performed. 28 French chest tube placed. Uncomplicated procedure.",
            7: "[Indication]\nRecurrent undiagnosed pleural effusion.\n[Anesthesia]\nMAC.\n[Description]\nRight pleuroscopy. Multifocal nodules. Biopsies x10 (Flow cytometry sent). 5g Talc pleurodesis. Chest tube placed.\n[Plan]\nAdmit. Pain control. Await path.",
            8: "Mrs. Thompson has had fluid come back multiple times, so we looked inside with a scope today. We found many small bumps on the lung surface and chest wall. We took samples of these to check for cancer or lymphoma. Since we were already there, we drained the fluid and put in talc powder to seal the space and prevent the fluid from coming back. She has a chest tube now and is recovering comfortably.",
            9: "Procedure: Thoracoscopic biopsy and chemical pleurodesis.\nFindings: Disseminated pleural nodularity.\nAction: Biopsies obtained for histopathology and flow cytometry. Talc insufflated for symphysis. Thoracostomy tube positioned.\nOutcome: Diagnostic tissue secured; therapeutic pleurodesis initiated."
        },
        8: { # Michael Brown (EBUS)
            1: "Indication: RUL mass, staging.\nProc: EBUS-TBNA.\nSampled: 4R (Positive Adeno), 7 (Positive Malignant), 10R/11R (Benign).\nDx: N2 Disease.\nPlan: Oncology.",
            2: "STAGING BRONCHOSCOPY: The patient underwent EBUS-TBNA for mediastinal staging of a right upper lobe lung mass. Systematic assessment revealed enlarged lymph nodes in the right paratracheal (4R) and subcarinal (7) stations. Needle aspiration confirmed malignancy in both N2 stations (4R and 7), establishing stage IIIA/N2 disease. Hilar nodes (10R, 11R) were benign.",
            3: "Code: 31653 (Bronchoscopy with EBUS sampling 3+ stations).\nStations: 4R, 7, 10R, 11R (4 distinct stations sampled).\nResults:\n- 4R: Positive (Adenocarcinoma)\n- 7: Positive (Malignancy)\n- 10R/11R: Negative\nImpact: Confirms inoperable N2 disease, guiding non-surgical management.",
            4: "Procedure: EBUS\nPatient: Michael Brown\nIndication: Staging RUL mass.\nNodes Sampled:\n1. 4R: Positive\n2. 7: Positive\n3. 10R: Benign\n4. 11R: Benign\nROSE: Adenocarcinoma.\nPlan: Chemo/Rad referral (N2 positive).",
            5: "ebus for mr brown he has that mass in the right upper lobe. Checked the nodes in the middle. 4R was abnormal poked it cancer. 7 was also abnormal poked it cancer. 10 and 11 looked ok but we sampled them anyway they were benign. So he has N2 disease. No complications.",
            6: "EBUS-TBNA performed for staging of RUL mass. MAC anesthesia. Stations 4R, 7, 10R, and 11R sampled. Rapid on-site evaluation showed adenocarcinoma in stations 4R and 7. Stations 10R and 11R were reactive. Diagnosis of N2 stage IIIA disease confirmed. Patient tolerated procedure well.",
            7: "[Indication]\nLung cancer staging.\n[Anesthesia]\nMAC.\n[Description]\nEBUS-TBNA. Stations 4R, 7, 10R, 11R sampled. Malignancy confirmed in 4R and 7.\n[Plan]\nRefer to Oncology for Stage IIIA management.",
            8: "We performed an ultrasound bronchoscopy to see if Mr. Brown's lung cancer had spread to the lymph nodes in the center of his chest. Unfortunately, we found cancer cells in both the nodes near the windpipe (4R) and under the airway split (7). This places him at a more advanced stage than localized disease. We sampled some other nodes further out which were clear. We will set him up with the cancer doctors for chemotherapy and radiation.",
            9: "Procedure: EBUS-guided nodal aspiration.\nObjective: Mediastinal staging.\nFindings: Metastatic involvement of station 4R and 7.\nAction: TBNA of four nodal stations.\nConclusion: Pathologically confirmed N2 disease."
        }
    }
    return variations

def get_base_data_mocks():
    # Names for the variations (9 names per note index)
    return [
        {"idx": 0, "orig_name": "Robert Chen", "orig_age": 73, "names": ["David Wu", "James Chen", "Robert Liu", "William Zhang", "Thomas Wang", "Richard Yang", "Joseph Huang", "Charles Lin", "Henry Zhao"]},
        {"idx": 1, "orig_name": "Sandra Martinez", "orig_age": 53, "names": ["Maria Garcia", "Elena Rodriguez", "Carmen Lopez", "Ana Hernandez", "Sofia Gonzalez", "Isabella Perez", "Gabriela Sanchez", "Rosa Ramirez", "Lucia Torres"]},
        {"idx": 2, "orig_name": "Sarah Chen", "orig_age": 66, "names": ["Linda Wu", "Patricia Chen", "Barbara Liu", "Susan Zhang", "Margaret Wang", "Jessica Yang", "Dorothy Huang", "Lisa Lin", "Nancy Zhao"]},
        {"idx": 3, "orig_name": "Roberto Martinez", "orig_age": 57, "names": ["Juan Garcia", "Carlos Rodriguez", "Luis Lopez", "Miguel Hernandez", "Jose Gonzalez", "Antonio Perez", "Francisco Sanchez", "Manuel Ramirez", "Pedro Torres"]},
        {"idx": 4, "orig_name": "Emma Thompson", "orig_age": 3, "names": ["Olivia Smith", "Ava Johnson", "Sophia Williams", "Isabella Brown", "Mia Jones", "Charlotte Miller", "Amelia Davis", "Harper Garcia", "Evelyn Rodriguez"]},
        {"idx": 5, "orig_name": "Aisha Patel", "orig_age": 43, "names": ["Priya Sharma", "Diya Singh", "Ananya Gupta", "Sana Khan", "Fatima Ali", "Zara Ahmed", "Aarya Shah", "Kavita Patel", "Riya Kumar"]},
        {"idx": 6, "orig_name": "Christopher Hayes", "orig_age": 14, "names": ["Michael Jordan", "Joshua Jackson", "Matthew White", "Ethan Harris", "Daniel Martin", "Alexander Thompson", "Ryan Martinez", "Jacob Robinson", "Tyler Clark"]},
        {"idx": 7, "orig_name": "Elizabeth Thompson", "orig_age": 71, "names": ["Mary Smith", "Patricia Johnson", "Jennifer Williams", "Linda Brown", "Elizabeth Jones", "Barbara Miller", "Susan Davis", "Jessica Garcia", "Sarah Rodriguez"]},
        {"idx": 8, "orig_name": "Michael Brown", "orig_age": 65, "names": ["James Wilson", "John Moore", "Robert Taylor", "Michael Anderson", "William Thomas", "David Jackson", "Richard White", "Joseph Harris", "Thomas Martin"]}
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
    
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # Randomize age and date
            new_age = orig_age + random.randint(-2, 2)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            new_name = record['names'][style_num - 1]
            
            # Apply variation text
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry fields
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            
            # Add metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    output_filename = output_dir / "synthetic_blvr_notes_part_008.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()