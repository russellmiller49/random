import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (Targeting Part 080)
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_080.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the 10 notes in Part 080.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Daniel Carter (Left Medical Thoracoscopy, Talc)
            1: "Procedure: Left Medical Thoracoscopy w/ Talc Pleurodesis.\nIndication: Recurrent malignant effusion.\nTechnique: US guidance. 6th ICS. 1.8L serosanguinous fluid drained. Diffuse parietal nodules seen/biopsied. 4g Talc slurry instilled.\nComplications: Transient hypotension (fluids given). No bleeding.\nDisposition: Floor. Chest tube to suction.",
            2: "OPERATIVE REPORT\n\nPATIENT: Daniel Carter\nPROCEDURE: Left-sided medical thoracoscopy with parietal pleural biopsy and talc pleurodesis.\n\nCLINICAL SUMMARY: The patient is a 68-year-old male with metastatic adenocarcinoma presenting with rapid re-accumulation of pleural fluid.\n\nDETAILED NARRATIVE: Following the induction of general anesthesia and isolation of the left lung via a double-lumen tube, the left hemithorax was accessed at the 6th intercostal space under sonographic guidance. Upon trocar entry, approximately 1800 mL of serosanguinous effusion was evacuated. Thoracoscopic visualization revealed extensive nodularity of the parietal pleura. Representative biopsies were harvested. Subsequently, a slurry comprising 4 grams of talc in 50 mL saline was instilled and uniformly distributed. A 24-French thoracostomy tube was positioned apically.\n\nIMPRESSION: Successful diagnostic and therapeutic thoracoscopy.",
            3: "CPT Selection: 32650 (Thoracoscopy, surgical; with pleurodesis).\nRationale:\n1. Access: Trocar placement in left 6th ICS.\n2. Drainage: 1.8 L fluid removed.\n3. Biopsy: Parietal pleura sampled (separate distinct work, but 32650 covers the approach).\n4. Therapeutic Agent: 4 grams Talc slurry instilled for chemical pleurodesis.\n5. Closure: 24 Fr chest tube placed.\nMedical Necessity: Recurrent malignant pleural effusion refractory to thoracentesis.",
            4: "Procedure Note\nPatient: Daniel Carter\nAttending: Dr. Morris\nResident: Dr. Shah\n\nSteps:\n1. Time out. GA with DLT.\n2. US guidance -> Left 6th ICS access.\n3. Drained 1.8L serosanguinous fluid.\n4. Scope in -> Saw nodules on parietal pleura -> Biopsied.\n5. Lung re-expanded well.\n6. 4g Talc slurry injected.\n7. 24 Fr chest tube placed.\n\nPlan: Admit, CXR daily, pull tube when output <150.",
            5: "Procedure note for mr carter we did the thoracoscopy on the left side today general anesthesia used the double lumen tube. ultrasound found the spot 6th rib space put the trocar in and got out a lot of fluid like 1.8 liters looked bloody. looked inside and saw bumps everywhere took some biopsies. put in the talc slurry 4 grams. blood pressure dropped a bit but fluids fixed it. chest tube is in 24 french. send to floor thanks.",
            6: "Medical thoracoscopy with talc pleurodesis for malignant pleural effusion. Patient: Daniel Carter, 68-year-old male. Under ultrasound guidance, the left 6th intercostal space in the midaxillary line was selected. Approximately 1.8 L of serosanguinous pleural fluid was drained through a trocar. A semi-rigid thoracoscope was introduced. Diffuse parietal pleural studding and nodularity were seen, with trapped lung but near-complete re-expansion after drainage. Multiple parietal pleural biopsies were obtained. A talc slurry (4 g in 50 mL normal saline) was distributed evenly over the parietal pleura while rotating the patient. A 24 Fr chest tube was left in place and connected to suction.",
            7: "[Indication]\nSymptomatic, rapidly recurrent left malignant pleural effusion.\n[Anesthesia]\nGeneral, DLT.\n[Description]\nUS guidance used. Entry Left 6th ICS. 1.8L serosanguinous fluid drained. Nodules biopsied. 4g Talc slurry instilled. Lung re-expanded.\n[Plan]\nAdmit. Suction -20cmH2O. Remove tube when output <150ml.",
            8: "Mr. Carter underwent a left medical thoracoscopy today to manage his recurrent pleural effusion. After putting him under general anesthesia and securing the airway, we used ultrasound to find the best spot for entry in the sixth intercostal space. We drained about 1.8 liters of bloody fluid. The camera showed widespread nodules on the lining of the chest wall, which we biopsied. To prevent the fluid from coming back, we coated the area with a talc slurry. He tolerated the procedure well, aside from a brief drop in blood pressure that responded to fluids.",
            9: "Procedure: Medical thoracoscopy with talc pleurodesis.\nAction: The left 6th intercostal space was cannulated. Approximately 1.8 L of serosanguinous fluid was evacuated. The parietal pleura was inspected and sampled. A talc mixture was administered over the pleural surface. A chest tube was inserted.\nOutcome: Near-complete lung re-inflation.\nComplications: Transient hypotension managed with volume expansion."
        },
        1: { # Maria Lopez (Right Medical Thoracoscopy, Mechanical + Doxy)
            1: "Indication: Recurrent R malignant effusion (Mesothelioma).\nProc: Med Thoracoscopy (Right).\nAction: 1.2L serous fluid drained. Tumor implants seen/biopsied.\nPleurodesis: Mechanical abrasion + 500mg Doxycycline.\nDevice: 28 Fr chest tube.\nEBL: 40mL. No complications.",
            2: "PROCEDURE PERFORMED: Right medical thoracoscopy with mechanical pleurodesis and chemical sclerosis (Doxycycline).\nINDICATION: Mrs. Lopez, a 73-year-old female with known epithelioid mesothelioma, presented with intractable dyspnea secondary to a large recurrent effusion.\nDESCRIPTION: Under general anesthesia with bronchial blocker isolation, the right hemithorax was entered at the 5th intercostal space. Evacuation yielded 1.2 Liters of serous fluid. Inspection verified circumferential pleural thickening typical of mesothelioma. Therapeutic pleurodesis was achieved via mechanical abrasion of the parietal pleura followed by the instillation of 500 mg Doxycycline. A 28-French thoracostomy tube was placed.",
            3: "Coding Data:\nCode: 32650.\nDiagnosis: Malignant Pleural Mesothelioma.\nTechnique: Thoracoscopic access (Right).\nFluid: 1200 mL removed.\nIntervention: Mechanical pleurodesis (gauze abrasion) AND Chemical pleurodesis (Doxycycline 500mg).\nNotes: Procedure performed under GA with one-lung ventilation. Biopsies taken for biomarkers.",
            4: "Resident Note / Thoracic Surgery\nPt: Maria Lopez\nDx: Mesothelioma\nProc: Right Thoracoscopy + Pleurodesis\n\n1. Lat decubitus. GA.\n2. Incision 5th ICS.\n3. Drained 1.2L serous fluid.\n4. Scratched pleura (mechanical pleurodesis).\n5. Added Doxycycline 500mg.\n6. Placed 28Fr chest tube.\n\nEst Blood Loss: 40cc. No issues.",
            5: "Maria Lopez 73 female has mesothelioma and the fluid keeps coming back on the right so we did the scope today. General anesthesia with a blocker. Opened the 5th space drained 1.2 liters of yellow fluid. Inside looked thick like tumor. Scratched up the lining for mechanical pleurodesis and also put in doxycycline 500 milligrams to be sure. Chest tube is a 28 french. Bleeding was minor controlled with cautery.",
            6: "Medical thoracoscopy with mechanical pleurodesis for mesothelioma. Right lateral decubitus positioning. The 5th intercostal space at the midaxillary line was opened with a 2 cm incision. Entry into the pleural space resulted in immediate drainage of 1.2 L of serous fluid. A rigid thoracoscope was used to inspect the pleural cavity, revealing circumferential parietal pleural thickening and tumor implants. Mechanical pleurodesis was performed using a gauze pad and thoracoscopic scratcher across the parietal pleura, followed by instillation of 500 mg doxycycline in 50 mL saline as adjunct sclerosing agent. A 28 Fr chest tube was secured in the posterior axillary line.",
            7: "[Indication]\nRecurrent right malignant effusion, Mesothelioma.\n[Anesthesia]\nGeneral, Bronchial Blocker.\n[Description]\n1.2L serous fluid drained. Circumferential thickening noted. Mechanical abrasion performed. Doxycycline 500mg instilled.\n[Plan]\nSuction -20. Oncology follow-up.",
            8: "We took Mrs. Lopez to the OR for her right-sided fluid buildup caused by mesothelioma. We drained 1.2 liters of fluid using the thoracoscope. The lining of the lung looked thickened as expected. To seal the space, we used a two-step approach: first, we mechanically abraded the pleural surface with a gauze pad, and then we instilled doxycycline. We left a large chest tube in place to ensure everything drains well.",
            9: "Procedure: Medical thoracoscopy with mechanical pleurodesis.\nSubject: 73-year-old female with mesothelioma.\nFindings: 1.2 L of serous fluid was extracted. Circumferential parietal pleural thickening was observed.\nIntervention: The parietal pleura was abraded. Doxycycline was introduced as a sclerosing agent.\nOutcome: Chest tube positioned. Mild oozing managed with cautery."
        },
        2: { # Hannah Nguyen (Right Medical Thoracoscopy, Talc, Breast Ca)
            1: "Proc: Right Med Thoracoscopy + Talc.\nPt: 61F Breast Ca.\nAnesth: MAC (Propofol).\nFindings: 1.4L serous fluid. Patchy nodules diaphragmatic/posterior.\nIntervention: Biopsies taken. 4g Talc slurry instilled.\nDisp: Admit. Chest tube 20Fr.",
            2: "OPERATIVE NOTE: Right medical thoracoscopy performed under Monitored Anesthesia Care.\nINDICATIONS: Recurrent symptomatic pleural effusion secondary to metastatic breast carcinoma.\nFINDINGS: Upon entry at the 7th intercostal space, 1400 mL of serous fluid was aspirated. Examination of the pleural cavity demonstrated patchy metastatic deposits along the diaphragm and posterior wall. These were biopsied for receptor status confirmation. A standard dose of 4 grams sterile talc was administered as a slurry for pleurodesis.\nPLAN: Chest tube management and resumption of systemic therapy.",
            3: "Service: Thoracoscopy, Surgical; with pleurodesis (32650).\nSetting: Procedure Suite (MAC anesthesia).\nDetails:\n- Ultrasound localization.\n- Drainage of 1400mL serous fluid.\n- Visual inspection: Patchy nodularity.\n- Biopsy: Performed.\n- Agent: Talc slurry (4g).\n- Device: 20 Fr Chest tube.\nSupport: Recurrent effusion refractory to thoracentesis.",
            4: "Procedure: Right Thoracoscopy\nPatient: Hannah Nguyen\nSteps:\n1. MAC sedation.\n2. Local anesthetic 7th ICS.\n3. Trocar in -> 1.4L fluid out.\n4. Saw nodules -> Biopsy.\n5. Talc slurry 4g put in.\n6. 20Fr tube placed.\n\nPatient stable. EBL 15mL.",
            5: "Did a thoracoscopy on Ms Nguyen for her breast cancer fluid on the right side. We used MAC sedation so she was breathing on her own. Drained about 1.4 liters of fluid. Saw some spots on the diaphragm and took samples. Put in the talc 4 grams to stick the lung. Chest tube is in. No complications really just admitted her for the night.",
            6: "Medical thoracoscopy with talc pleurodesis for recurrent breast cancer–related malignant pleural effusion. Patient is a 61-year-old female. After ultrasound localization, the right 7th intercostal space in the posterior axillary line was infiltrated with lidocaine and bupivacaine. A single-port semi-rigid medical thoracoscope was introduced after trocar insertion. Approximately 1.4 L of serous fluid was drained. The parietal pleura showed patchy nodularity over the diaphragmatic and posterior pleura. Biopsies were obtained. A talc slurry (4 g in 100 mL saline) was instilled. A 20 Fr chest tube was secured.",
            7: "[Indication]\nRecurrent right effusion, metastatic breast cancer.\n[Anesthesia]\nMAC (Propofol).\n[Description]\n1.4L serous fluid drained. Patchy nodules biopsied. 4g Talc slurry instilled.\n[Plan]\nAdmit overnight. Water seal when leak resolves. Resume chemo.",
            8: "Ms. Nguyen came in for a procedure to help with the fluid on her right lung caused by her breast cancer. We kept her comfortable with sedation but didn't need general anesthesia. We drained 1.4 liters of fluid and saw some small nodules which we biopsied. We then put in a talc mixture to seal the space. She tolerated it well and has a small chest tube in place now.",
            9: "Operation: Medical thoracoscopy with talc pleurodesis.\nIndication: Dyspnea from recurrent effusion.\nDetails: 1.4 L of serous fluid was withdrawn. Parietal pleural nodules were sampled. A talc suspension was distributed within the cavity.\nResult: A 20 Fr chest tube was anchored. No significant blood loss."
        },
        3: { # Samuel Ortiz (Right Med Thoracoscopy, Hepatic Hydrothorax)
            1: "Indication: Refractory hepatic hydrothorax (Cirrhosis).\nProc: Right Med Thoracoscopy.\nFindings: 2.1L straw-colored fluid. Smooth pleura (no nodules).\nAction: Mechanical abrasion + 4g Talc slurry.\nPlan: Albumin replacement. Consult Hepatology (TIPS evaluation).",
            2: "PROCEDURE: Right medical thoracoscopy with mechanical and chemical pleurodesis.\nPATIENT: Samuel Ortiz (Decompensated Cirrhosis).\nNARRATIVE: The right pleural space was accessed under general anesthesia. A massive transudative effusion (2100 mL) was evacuated. Inspection revealed smooth, glistening pleura consistent with hepatic hydrothorax; no gross malignancy was identified. To maximize the probability of symphysis in this difficult scenario, a combined approach was utilized: mechanical abrasion of the parietal pleura followed by instillation of 4 grams of talc slurry.\nPOST-OP: Patient transferred to step-down for hemodynamic monitoring and albumin replacement.",
            3: "CPT: 32650.\nDiagnosis: Hepatic Hydrothorax (Refractory).\nProcedure:\n- 2.1 Liters drainage.\n- Visualization: No lesions biopsied.\n- Pleurodesis: Dual modality (Mechanical abrasion + Talc slurry).\nComplexity: High risk patient (ASA 4, Cirrhosis). Albumin given for volume shifts.",
            4: "Resident Note\nPt: Samuel Ortiz\nDx: Hepatic Hydrothorax\n\n1. GA / ETT.\n2. Right 6th ICS entry.\n3. Drained 2.1L clear fluid.\n4. Pleura looked normal.\n5. Scrubbed pleura with gauze (abrasion).\n6. Put in 4g Talc.\n7. 24Fr chest tube.\n\nPlan: Watch BP, give albumin, talk to GI about TIPS.",
            5: "Mr Ortiz has bad liver disease and fluid in the right lung we did the scope today to try and stick it. Drained a lot of fluid 2.1 liters. The lining looked smooth no cancer. We rubbed it with the pad mechanical pleurodesis and also put in talc. Gave him albumin because his pressure dropped a little. Chest tube is in place sending him to step down.",
            6: "Medical thoracoscopy with talc pleurodesis for hepatic hydrothorax. Patient is a 59-year-old male with decompensated cirrhosis. Ultrasound localization identified a large free-flowing right effusion. A 2 cm incision was made in the right 6th intercostal space. After trocar insertion, 2.1 L of clear, straw-colored fluid was drained. Thoracoscopic inspection showed smooth parietal pleura without nodularity. Mechanical abrasion pleurodesis was performed using a thoracoscopic pad; 4 g of sterile talc was then distributed evenly. A 24 Fr chest tube was placed.",
            7: "[Indication]\nRefractory right hepatic hydrothorax.\n[Anesthesia]\nGeneral.\n[Description]\n2.1L clear fluid drained. Pleura smooth. Mechanical abrasion performed. 4g Talc slurry instilled.\n[Plan]\nStep-down unit. Albumin replacement. Evaluate for TIPS.",
            8: "Mr. Ortiz, who suffers from liver cirrhosis, had a large amount of fluid around his right lung. We performed a thoracoscopy to drain it and try to prevent it from coming back. We removed 2.1 liters of fluid. Since the lung lining looked healthy, we roughed it up mechanically and added talc to help it stick to the chest wall. We gave him some albumin to keep his blood pressure stable and placed a chest tube.",
            9: "Procedure: Medical thoracoscopy with talc pleurodesis.\nCondition: Refractory hepatic hydrothorax.\nAction: 2.1 L of straw-colored fluid was evacuated. The parietal pleura was abraded mechanically. 4 g of talc was dispersed.\nResult: A 24 Fr chest tube was secured. Transient hypotension was rectified with albumin."
        },
        4: { # Liam Johnson (Left Med Thoracoscopy, Spontaneous Pneumo, Blebs)
            1: "Indication: Recurrent Left Spontaneous Pneumothorax.\nProc: Med Thoracoscopy + Talc Poudrage.\nFindings: Apical blebs (stapled by Thoracic Surgery). 150ml fluid.\nAction: Mechanical abrasion (apical/parietal) + 4g Talc insufflation (poudrage).\nPlan: Chest tube to suction. Stop smoking.",
            2: "OPERATIVE REPORT: Left medical thoracoscopy with pleurodesis for recurrent primary spontaneous pneumothorax.\nFINDINGS: Entry into the left pleural cavity revealed a small effusion and apical bleb disease. The blebs were resected via stapling (refer to Thoracic Surgery note). Following resection, the Medical Pulmonary team performed mechanical pleurodesis of the apical pleura. This was augmented by the insufflation of 4 grams of sterile talc powder (poudrage) to ensure diffuse pleural symphysis.\nOUTCOME: 24-French chest tube placed. Patient extubated and stable.",
            3: "Code: 32650 (Thoracoscopy w/ pleurodesis).\nNote: Stapling reported separately by surgery.\nTechnique:\n- Lung isolation (DLT).\n- Identification of apical pathology.\n- Mechanical abrasion performed.\n- Talc Poudrage (Insufflation of dry powder) used instead of slurry.\nMedical Necessity: Recurrent pneumothorax (3rd episode).",
            4: "Procedure: Left Thoracoscopy for Pneumo\nPatient: Liam Johnson, 27M\n\n1. GA, DLT.\n2. Surgery stapled blebs first.\n3. We did the pleurodesis.\n4. Scratched the pleura (abrasion).\n5. Puffed in 4g Talc powder.\n6. Chest tube placed.\n\nEvents: Desat to 88% during single lung vent, fixed with recruitment.",
            5: "Liam is the young guy with the collapsed lung again. We went in with the surgeons. They stapled the blebs. We did the pleurodesis part. Rubbed the apex with gauze and blew in the talc powder 4 grams. He desatted a bit when we dropped the lung but came back up. Tube is in. Tell him to stop smoking seriously.",
            6: "Medical thoracoscopy with talc pleurodesis for recurrent spontaneous pneumothorax. Patient is a 27-year-old male. The patient was positioned in right lateral decubitus. Entry into the left pleural space at the 5th intercostal space yielded a small amount of serosanguinous fluid and air. Thoracoscopic inspection revealed several apical blebs. The apical blebs were stapled by the thoracic surgery team. Medical thoracoscopy team performed mechanical pleurodesis along the apical and parietal pleura using gauze pads, followed by insufflation of 4 g sterile talc as dry powder. A 24 Fr chest tube was left at the apex.",
            7: "[Indication]\nRecurrent left spontaneous pneumothorax.\n[Anesthesia]\nGeneral, DLT.\n[Description]\nBlebs stapled by surgery. Mechanical abrasion performed. 4g Talc poudrage insufflated.\n[Plan]\nDaily CXR. Tube removal when air leak resolves. Smoking cessation.",
            8: "Liam came in for his third collapsed lung. We worked with the surgery team; they stapled off the weak spots (blebs) on his lung. Then, we performed the pleurodesis to stick the lung to the chest wall. We used a scratch pad on the lining and blew in dry talc powder. He had a brief drop in oxygen levels during the procedure but recovered quickly. He has a chest tube in now.",
            9: "Procedure: Medical thoracoscopy with talc poudrage.\nContext: Recurrent primary spontaneous pneumothorax.\nIntervention: Apical blebs were resected by surgery. The parietal pleura was abraded. 4 g of talc was insufflated as a dry powder.\nComplication: Intraoperative desaturation resolved with recruitment maneuvers."
        },
        5: { # Olivia Brown (Left Med Thoracoscopy, Loculated, Adhesiolysis)
            1: "Indication: Loculated malignant effusion (Ovarian Ca).\nProc: Left Med Thoracoscopy + Adhesiolysis.\nFindings: Multiple septations/loculations. 900mL drained.\nAction: Blunt lysis of adhesions. Biopsies taken. 4g Talc slurry.\nPlan: Chest tube to suction. Oncology f/u.",
            2: "PROCEDURE: Left medical thoracoscopy with adhesiolysis and pleurodesis.\nINDICATION: 65-year-old female with metastatic ovarian carcinoma and complex, loculated pleural effusion.\nDETAILS: Ultrasound revealed multiloculated fluid. Upon entry, extensive fibrinous adhesions were encountered. Blunt dissection was employed to break down septations and unify the pleural space, facilitating the drainage of 900 mL of fluid. Nodular implants were biopsied. Following adhesiolysis, 4 grams of talc slurry was instilled under direct visualization to ensure adequate coverage.\nDISPOSITION: Admitted to oncology service.",
            3: "CPT: 32650 (includes adhesiolysis if not extensive enough for separate decortication code, typically).\nTechnique:\n- Access: Left 6th ICS.\n- Lysis: Blunt lysis of adhesions to treat loculations.\n- Drainage: 900 mL.\n- Biopsy: Parietal pleura.\n- Pleurodesis: Talc slurry.\nReasoning: Standard thoracentesis failed due to loculations.",
            4: "Resident Note\nPt: Olivia Brown\nDx: Ovarian Ca, Loculated effusion\n\n1. Moderate sedation.\n2. US showed loculations.\n3. Scope in -> broke up adhesions (lysis).\n4. Drained 900cc.\n5. Biopsied nodules.\n6. Put in Talc.\n7. 20Fr tube.\n\nPatient comfortable, minimal pain.",
            5: "Procedure on Ms Brown she has ovarian cancer and the fluid was trapped in pockets. We went in with the scope and had to break up the adhesions to get the fluid out. Got about 900 mls. Took some biopsies of the bumps. Put in the talc 4 grams. She had a little pain so we gave meds. Chest tube is in suction.",
            6: "Medical thoracoscopy with talc pleurodesis for loculated malignant pleural effusion. Patient is a 65-year-old female. Bedside ultrasound showed multiple septations. A 2 cm incision was made at the 6th intercostal space. Trocar insertion yielded 900 mL of serous fluid from the largest locule. A semi-rigid thoracoscope was advanced; adhesions were bluntly lysed to break down septations. Multiple parietal pleural biopsies were taken. After near-complete drainage, 4 g talc in 50 mL saline was instilled. A 20 Fr chest tube was secured.",
            7: "[Indication]\nLoculated left malignant pleural effusion.\n[Anesthesia]\nModerate Sedation.\n[Description]\nAdhesions lysed. 900mL drained. Biopsies performed. 4g Talc slurry instilled.\n[Plan]\nSuction to water seal. Oncology follow-up.",
            8: "Ms. Brown's fluid was trapped in pockets (loculated), so a regular needle drain wouldn't work. We used the thoracoscope to break up these pockets and drained 900ml of fluid. We found some cancer spots and took samples. To keep the fluid from coming back, we put in talc. She had some pain during the procedure but we managed it with medication.",
            9: "Procedure: Medical thoracoscopy with adhesiolysis.\nIndication: Loculated malignant pleural effusion.\nAction: Adhesions were bluntly severed to unify the space. 900 mL of fluid was evacuated. Pleural nodules were sampled. Talc slurry was introduced.\nOutcome: Chest tube placed. Mild pleuritic pain managed with opioids."
        },
        6: { # Ethan Miller (Left Med Thoracoscopy, SCC Lung)
            1: "Indication: Recurrent malignant effusion (SCC Lung).\nProc: Left Med Thoracoscopy.\nFindings: 1.6L serosanguinous fluid. Nodular pleura.\nAction: Biopsies. 4g Talc slurry pleurodesis.\nPlan: Chest tube to suction. Palliative consult.",
            2: "OPERATIVE SUMMARY: Left medical thoracoscopy for palliation of malignant pleural effusion.\nPATIENT: Ethan Miller, 72M (Stage IV Squamous Cell Carcinoma).\nPROCEDURE: General anesthesia. Left 6th ICS access. Evacuation of 1.6 Liters of serosanguinous fluid. Visualization of diffuse parietal and diaphragmatic nodularity. Biopsies obtained. Pleurodesis achieved via instillation of 4 grams talc slurry.\nPLAN: Chest tube management. Monitor for re-expansion. Palliative care engagement.",
            3: "Billing: 32650.\nSite: Left hemithorax.\nPathology: Metastatic Squamous Cell Carcinoma.\nWork:\n- 1.6L drainage.\n- Diagnostic inspection and biopsy.\n- Therapeutic administration of talc agent.\n- Chest tube placement (24 Fr).\nIndication: Dyspnea relief and prevention of recurrence.",
            4: "Procedure: Left Thoracoscopy\nPt: Ethan Miller\n\n1. GA / ETT.\n2. US guidance.\n3. Trocar -> 1.6L bloody fluid.\n4. Nodules all over pleura/diaphragm -> Biopsy.\n5. Talc slurry 4g.\n6. Tube placed.\n\nNo complications.",
            5: "Mr Miller has lung cancer and fluid on the left. We did the thoracoscopy under GA. Drained 1.6 liters. The pleura looked bumpy so we biopsied it. Put in the talc to seal it up. No issues bleeding was minor. Chest tube is hooked up to suction.",
            6: "Medical thoracoscopy with talc pleurodesis for malignant pleural effusion in non–small cell lung cancer. Patient is a 72-year-old male. Left 6th intercostal space was selected under ultrasound guidance. Trocar entry produced a gush of serosanguinous fluid; 1.6 L was drained. Thoracoscopy showed nodular parietal and diaphragmatic pleura. Multiple biopsies were taken. After drainage, 4 g talc in 50 mL saline was instilled and spread evenly. A 24 Fr chest tube was secured.",
            7: "[Indication]\nRecurrent left malignant effusion, SCC Lung.\n[Anesthesia]\nGeneral.\n[Description]\n1.6L serosanguinous fluid drained. Nodules biopsied. 4g Talc slurry instilled.\n[Plan]\nDaily CXR. Palliative care consult.",
            8: "We performed a procedure to drain the fluid around Mr. Miller's left lung and prevent it from returning. We removed 1.6 liters of fluid. We saw many nodules on the lung lining consistent with his cancer and took biopsies to confirm. We then spread talc in the chest cavity. He is recovering on the floor with a chest tube.",
            9: "Procedure: Medical thoracoscopy with talc pleurodesis.\nSubject: 72-year-old male with squamous cell carcinoma.\nFindings: 1.6 L of serosanguinous fluid was aspirated. Nodular parietal pleura was observed and sampled.\nIntervention: Talc slurry was distributed evenly. A 24 Fr chest tube was inserted."
        },
        7: { # Noah Allen (Left Med Thoracoscopy, Renal Cell, Hemorrhagic)
            1: "Indication: Recurrent effusion (Renal Cell Ca). Hemorrhagic fluid.\nProc: Left Med Thoracoscopy.\nFindings: 1.3L hemorrhagic fluid. Hemorrhagic implants.\nAction: Biopsies. 4g Talc slurry.\nPlan: Chest tube. Oncology f/u 1 week.",
            2: "PROCEDURE NOTE: Left medical thoracoscopy.\nINDICATION: Metastatic renal cell carcinoma with recurrent hemorrhagic pleural effusion.\nFINDINGS: 1300 mL of hemorrhagic fluid evacuated. The parietal pleura demonstrated numerous vascular, hemorrhagic implants characteristic of metastatic RCC. Biopsies confirmed the visual impression. Talc pleurodesis (4g) was performed to achieve symphysis.\nDISPOSITION: Stable. Chest tube placement confirmed.",
            3: "Code: 32650.\nDx: Secondary malignant neoplasm of pleura (RCC primary).\nDetails: 1.3L drainage (hemorrhagic). Biopsy of implants. Talc pleurodesis.\nRisk: Hemorrhagic implants noted; hemostasis maintained. EBL 35mL.",
            4: "Resident Note\nPt: Noah Allen\nDx: Renal Cell Ca\n\n1. Moderate sedation.\n2. Left 6th ICS.\n3. Drained 1.3L bloody fluid.\n4. Saw hemorrhagic implants -> Biopsy.\n5. Talc slurry 4g.\n6. 20Fr tube.\n\nPlan: Remove tube when output low.",
            5: "Did the scope on Mr Allen he has kidney cancer. The fluid was very bloody drained 1.3 liters. The spots on the pleura were bleeding a bit too looked like renal cell. Biopsied them. Put in talc. No major bleeding problems surprisingly. Chest tube in.",
            6: "Medical thoracoscopy with talc pleurodesis for malignant pleural effusion from renal cell carcinoma. Patient is a 63-year-old male. Ultrasound identified a large free-flowing effusion. A 2 cm incision at the 6th intercostal space allowed entry with a semi-rigid thoracoscope. 1.3 L of hemorrhagic fluid drained. Numerous hemorrhagic pleural implants were seen. Biopsies were obtained for confirmation. Talc slurry (4 g in 50 mL saline) was instilled with even distribution. A 20 Fr chest tube was secured.",
            7: "[Indication]\nRecurrent left hemorrhagic effusion, Renal Cell Ca.\n[Anesthesia]\nModerate Sedation.\n[Description]\n1.3L hemorrhagic fluid drained. Implants biopsied. 4g Talc slurry instilled.\n[Plan]\nDaily CXR. Oncology follow-up.",
            8: "Mr. Allen has fluid around his lung from his kidney cancer. We drained 1.3 liters of bloody fluid using the thoracoscope. We saw several bleeding spots on the lung lining, which fits with his diagnosis. We took samples and then put in talc to seal the space. He is doing well with the chest tube in place.",
            9: "Procedure: Medical thoracoscopy with talc pleurodesis.\nFindings: 1.3 L of hemorrhagic fluid was evacuated. Hemorrhagic pleural implants were identified and sampled.\nAction: Talc slurry was administered. A 20 Fr chest tube was secured.\nComplications: None."
        },
        8: { # James Cooper (Left Med Thoracoscopy, Mesothelioma, Contralateral)
            1: "Indication: New left effusion (Mesothelioma). Hx of right pleurodesis.\nProc: Left Med Thoracoscopy.\nFindings: 1.5L serous fluid. Nodular pleura.\nAction: Biopsies. 4g Talc slurry.\nPlan: Chest tube. Palliative care.",
            2: "OPERATIVE REPORT: Contralateral (Left) Medical Thoracoscopy.\nPATIENT: James Cooper (Biphasic Mesothelioma).\nINDICATION: Progression of disease with new left-sided symptomatic effusion.\nPROCEDURE: General anesthesia. Left 6th ICS entry. 1500 mL serous fluid drained. Diffuse nodular parietal pleural involvement noted (consistent with mesothelioma). Biopsies taken. 4g Talc slurry instilled for pleurodesis.\nPLAN: Chest tube suction. Palliative care support.",
            3: "CPT: 32650.\nSite: Left (Contralateral to prior procedure).\nHistory: Prior Right-sided pleurodesis.\nProcedure: Drainage 1.5L. Biopsy of nodules. Talc pleurodesis.\nMedical Necessity: Palliation of dyspnea in setting of advanced mesothelioma.",
            4: "Procedure: Left Thoracoscopy\nPt: James Cooper\nDx: Mesothelioma (had Right side done before)\n\n1. GA.\n2. Left side entry.\n3. 1.5L serous fluid.\n4. Nodules seen -> Biopsy.\n5. Talc slurry.\n6. Tube placed.\n\nPlan: Pull tube when dry.",
            5: "Mr Cooper is back with fluid on the other side now the left side. He has mesothelioma. We did the scope drained 1.5 liters. Looks just like the other side did nodules everywhere. Put in talc to freeze it. Chest tube is in. Palliative care is following.",
            6: "Medical thoracoscopy with talc pleurodesis for malignant pleural effusion in mesothelioma (contralateral side). Patient is a 70-year-old male. Ultrasound confirmed a large left effusion. Trocar entry at the 6th intercostal space allowed drainage of 1.5 L of serous fluid. Thoracoscopy showed nodular parietal pleura; no diaphragmatic defects. Biopsies were obtained. Talc slurry (4 g in 50 mL saline) was instilled evenly. A 24 Fr chest tube was placed.",
            7: "[Indication]\nNew left malignant effusion, Mesothelioma.\n[Anesthesia]\nGeneral.\n[Description]\n1.5L serous fluid drained. Nodules biopsied. 4g Talc slurry instilled.\n[Plan]\nMonitor output. Palliative care. Tube removal when drainage low.",
            8: "Mr. Cooper developed fluid on his left side now, having previously had his right side treated. We performed a thoracoscopy to drain 1.5 liters of fluid. The appearance was consistent with his mesothelioma. We used talc to seal this side as well. He is comfortable and being followed by palliative care.",
            9: "Procedure: Medical thoracoscopy with talc pleurodesis.\nIndication: Contralateral malignant pleural effusion.\nAction: 1.5 L of serous fluid was withdrawn. Parietal pleural nodules were sampled. Talc slurry was distributed.\nResult: A 24 Fr chest tube was inserted. No complications."
        },
        9: { # Ava Thompson (Left Med Thoracoscopy, Adeno, Left dominant)
            1: "Indication: Left-dominant malignant effusion (Adeno).\nProc: Left Med Thoracoscopy.\nFindings: 1.7L serosanguinous fluid. Diffuse implants.\nAction: Biopsies. 4g Talc slurry.\nPlan: Chest tube. Monitor right side (may need IPC later).",
            2: "PROCEDURE: Left medical thoracoscopy with talc pleurodesis.\nPATIENT: Ava Thompson (Metastatic Adenocarcinoma).\nINDICATION: Symptomatic left pleural effusion (bilateral disease, left > right).\nFINDINGS: 1700 mL serosanguinous fluid evacuated. Diffuse parietal and diaphragmatic implants visualized and biopsied. 4g Talc slurry instilled for pleurodesis.\nPLAN: Monitor left side re-expansion. If contralateral right effusion becomes symptomatic, will consider Tunneled Pleural Catheter.",
            3: "Code: 32650.\nDiagnosis: Malignant Pleural Effusion (Left).\nVolume: 1.7L.\nPathology: Metastatic Adenocarcinoma.\nIntervention: Talc pleurodesis.\nNote: Patient has bilateral disease; this procedure addressed the symptomatic left side.",
            4: "Procedure: Left Thoracoscopy\nPt: Ava Thompson\n\n1. Mod sedation.\n2. Left 7th ICS.\n3. Drained 1.7L fluid.\n4. Implants seen -> Biopsy.\n5. Talc slurry 4g.\n6. 20Fr tube.\n\nPlan: Watch the right side, might need a catheter there later.",
            5: "Ms Thompson has fluid on both sides but the left is worse so we scoped that one. Moderate sedation. Drained 1.7 liters bloody fluid. Lots of cancer spots inside. Put in talc. She did fine. We'll watch the right side maybe put a PleurX in later if she needs it.",
            6: "Medical thoracoscopy with talc pleurodesis for malignant pleural effusion in lung adenocarcinoma (bilateral disease, unilateral treatment). Patient is a 67-year-old female. Ultrasound-guided entry at the left 7th intercostal space allowed drainage of 1.7 L serosanguinous fluid. Thoracoscopy revealed diffuse parietal pleural implants. Biopsies were obtained. Talc slurry (4 g in 50 mL saline) was instilled and distributed. A 20 Fr chest tube was secured.",
            7: "[Indication]\nSymptomatic left malignant effusion, Adenocarcinoma.\n[Anesthesia]\nModerate Sedation.\n[Description]\n1.7L serosanguinous fluid drained. Diffuse implants biopsied. 4g Talc slurry instilled.\n[Plan]\nDaily CXR. Assess contralateral side for potential IPC.",
            8: "Ms. Thompson has fluid on both lungs, but the left side was causing more trouble. We drained 1.7 liters from the left side using the thoracoscope and biopsied the implants we found. We put in talc to prevent the fluid from coming back on that side. We will keep an eye on her right side and might need to place a drain there later if it bothers her.",
            9: "Procedure: Medical thoracoscopy with talc pleurodesis.\nContext: Left-predominant malignant pleural effusion.\nIntervention: 1.7 L of serosanguinous fluid was evacuated. Diffuse parietal pleural implants were sampled. Talc slurry was introduced.\nFuture Considerations: Potential for contralateral tunneled pleural catheter."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns the base metadata for the 10 patients in Part 080.
    Names are generated to be distinct for each of the 9 variations.
    """
    return [
        # Note 0: Daniel Carter, 68
        {"idx": 0, "orig_name": "Daniel Carter", "orig_age": 68, "names": ["James Smith", "Robert Johnson", "Michael Williams", "David Brown", "Richard Jones", "Charles Garcia", "Joseph Miller", "Thomas Davis", "Christopher Rodriguez"]},
        # Note 1: Maria Lopez, 73
        {"idx": 1, "orig_name": "Maria Lopez", "orig_age": 73, "names": ["Patricia Martinez", "Jennifer Hernandez", "Linda Lopez", "Elizabeth Gonzalez", "Barbara Wilson", "Susan Anderson", "Jessica Thomas", "Sarah Taylor", "Karen Moore"]},
        # Note 2: Hannah Nguyen, 61
        {"idx": 2, "orig_name": "Hannah Nguyen", "orig_age": 61, "names": ["Nancy Jackson", "Lisa Martin", "Betty Lee", "Margaret Perez", "Sandra Thompson", "Ashley White", "Kimberly Harris", "Emily Sanchez", "Donna Clark"]},
        # Note 3: Samuel Ortiz, 59
        {"idx": 3, "orig_name": "Samuel Ortiz", "orig_age": 59, "names": ["Daniel Ramirez", "Paul Lewis", "Mark Robinson", "Donald Walker", "George Young", "Kenneth Allen", "Steven King", "Edward Wright", "Brian Scott"]},
        # Note 4: Liam Johnson, 27
        {"idx": 4, "orig_name": "Liam Johnson", "orig_age": 27, "names": ["Ronald Torres", "Anthony Nguyen", "Kevin Hill", "Jason Flores", "Matthew Green", "Gary Adams", "Timothy Nelson", "Jose Baker", "Larry Hall"]},
        # Note 5: Olivia Brown, 65
        {"idx": 5, "orig_name": "Olivia Brown", "orig_age": 65, "names": ["Michelle Rivera", "Laura Campbell", "Sarah Mitchell", "Kimberly Carter", "Deborah Roberts", "Dorothy Phillips", "Carol Evans", "Amanda Turner", "Melissa Parker"]},
        # Note 6: Ethan Miller, 72
        {"idx": 6, "orig_name": "Ethan Miller", "orig_age": 72, "names": ["Jeffrey Collins", "Frank Edwards", "Scott Stewart", "Eric Morris", "Stephen Rogers", "Andrew Reed", "Raymond Cook", "Gregory Morgan", "Joshua Bell"]},
        # Note 7: Noah Allen, 63
        {"idx": 7, "orig_name": "Noah Allen", "orig_age": 63, "names": ["Dennis Murphy", "Walter Bailey", "Patrick Rivera", "Peter Cooper", "Harold Richardson", "Douglas Cox", "Henry Howard", "Carl Ward", "Arthur Torres"]},
        # Note 8: James Cooper, 70
        {"idx": 8, "orig_name": "James Cooper", "orig_age": 70, "names": ["Ryan Peterson", "Roger Gray", "Joe Ramirez", "Juan James", "Jack Watson", "Albert Brooks", "Jonathan Kelly", "Justin Sanders", "Terry Price"]},
        # Note 9: Ava Thompson, 67
        {"idx": 9, "orig_name": "Ava Thompson", "orig_age": 67, "names": ["Stephanie Bennett", "Rebecca Wood", "Christine Barnes", "Kelly Ross", "Nicole Henderson", "Kathleen Coleman", "Amy Jenkins", "Angela Perry", "Helen Powell"]}
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
            # Safety check if variation exists
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}. Using original.")
            
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
    output_filename = output_dir / "synthetic_thoracoscopy_notes_part_080.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()