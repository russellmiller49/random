import json
import random
import datetime
import copy
from pathlib import Path

# Source file configuration
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_061_part1.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each note in the source file.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    Styles:
    1. Terse Surgeon
    2. Academic Attending
    3. Billing Coder
    4. Trainee/Resident
    5. Sloppy Dictation
    6. Header-less
    7. Templated
    8. Narrative Flow
    9. Synonym Swapper
    """
    
    variations = {
        0: { # Pt: Daniel Carter (32650 - Talc, 1.8L, Adeno)
            1: "Indication: Recurrent malignant effusion (Lung Adeno).\nProcedure: Medical thoracoscopy (Left).\n- US guidance: 6th ICS Mid-axillary.\n- 1.8L serosanguinous fluid drained.\n- Findings: Diffuse parietal studding. Lung trapped but re-expanded.\n- Intervention: Biopsies taken. Talc slurry (4g) instilled.\n- 24Fr chest tube placed.\nComplications: None.",
            2: "OPERATIVE REPORT: Mr. Carter, a 68-year-old male with metastatic lung adenocarcinoma, underwent left-sided medical thoracoscopy. Under general anesthesia with lung isolation, the pleural space was accessed at the 6th intercostal space. Thoracoscopic inspection revealed extensive carcinomatosis involving the parietal pleura. Following the evacuation of 1,800 mL of serosanguinous exudate, the lung demonstrated satisfactory re-expansion. Pleurodesis was achieved via the administration of a talc slurry (4g). A 24 Fr thoracostomy tube was sited under direct visualization.",
            3: "Service: Thoracoscopy, surgical; with pleurodesis (CPT 32650).\nDiagnosis: Malignant Pleural Effusion.\nTechnique: Ultrasound localization utilized. Trocar insertion at left 6th ICS. 1.8 liters of fluid removed. Diagnostic evaluation revealed parietal nodularity; biopsies obtained. Therapeutic intervention consisted of instillation of sclerosing agent (4g Talc slurry). Chest tube placed for drainage.",
            4: "Resident Procedure Note\nPatient: Carter, D.\nProcedure: Medical Thoracoscopy w/ Talc\nSteps:\n1. Time out/GA/DLT.\n2. US mark 6th ICS.\n3. Trocar entry -> 1.8L serosanguinous fluid.\n4. Scope: Diffuse nodules seen. Biopsied.\n5. Talc slurry 4g instilled.\n6. 24Fr tube placed to -20cmH2O.\nNo complications.",
            5: "daniel carter lung cancer with recurrent effusion we did a medical thoracoscopy on the left side ultrasound guidance used 1.8 liters serosanguinous fluid came out saw a lot of nodules everywhere took some biopsies then put in 4 grams of talc slurry for pleurodesis patient did fine pressure dropped a bit but fluids fixed it chest tube 24 french in place.",
            6: "The patient is a 68-year-old male with metastatic lung adenocarcinoma presented for management of a recurrent left pleural effusion. Under general anesthesia with a double-lumen tube the left chest was accessed at the 6th intercostal space under ultrasound guidance. Approximately 1.8L of serosanguinous fluid was drained. Direct visualization revealed diffuse parietal pleural studding. Multiple biopsies were obtained. A talc slurry consisting of 4g talc in 50mL saline was distributed over the parietal pleura. A 24Fr chest tube was placed. Estimated blood loss was 25mL.",
            7: "[Indication]\nRecurrent left malignant pleural effusion (Lung CA).\n[Anesthesia]\nGeneral, DLT.\n[Description]\nLeft medical thoracoscopy via 6th ICS. Drainage of 1.8L serosanguinous fluid. Findings: Diffuse nodularity. Interventions: Biopsies and 4g Talc slurry pleurodesis.\n[Plan]\nChest tube to suction. Oncology follow-up.",
            8: "Mr. Carter was brought to the operating room for a medical thoracoscopy to manage his recurrent malignant effusion. We utilized ultrasound to locate the optimal entry point at the left 6th intercostal space. Upon entry, we drained approximately 1.8 liters of serosanguinous fluid. The camera revealed diffuse studding of the parietal pleura. We proceeded to biopsy these lesions and then performed chemical pleurodesis using 4 grams of talc slurry. A chest tube was placed to ensure continued drainage.",
            9: "Indication: Symptomatic, rapidly returning left malignant pleural collection.\nTechnique: Utilizing ultrasound targeting, the left 6th intercostal gap was breached. Roughly 1.8 L of bloody pleural liquid was evacuated. A thoracoscope was inserted. Widespread parietal pleural bumps were visualized. Tissue samples were harvested. A talc mixture (4 g) was dispersed over the lining. A 24 Fr drain was sited."
        },
        1: { # Pt: Maria Lopez (32650 - Mechanical + Doxy, 1.2L, Mesothelioma)
            1: "Dx: Malignant Mesothelioma, Right effusion.\nProc: Thoracoscopy + Mechanical Pleurodesis.\n- Access: 5th ICS, MAL.\n- Fluid: 1.2L serous.\n- Findings: Circumferential thickening/tumor implants.\n- Action: Mechanical abrasion + 500mg Doxycycline instillation.\n- 28Fr Chest tube.\nEBL: 40mL. Stable.",
            2: "PROCEDURE NOTE: Medical Thoracoscopy with Mechanical and Chemical Pleurodesis.\nPATIENT: Ms. Lopez (73F).\nINDICATION: Recurrent effusion secondary to epithelioid mesothelioma.\nFINDINGS: Upon entry into the right hemithorax, 1.2 L of serous fluid was evacuated. Inspection demonstrated circumferential parietal thickening and tumor implants. \nINTERVENTION: Mechanical abrasion was performed via thoracoscopic scratcher. This was augmented by the instillation of 500 mg Doxycycline. A 28 Fr chest tube was secured.",
            3: "CPT Code: 32650 (Thoracoscopy with pleurodesis).\nMethod: Mechanical abrasion and chemical sclerosis (Doxycycline).\nSite: Right Pleural Space.\nDetails: 1200mL drainage. Visualization of diffuse tumor implants (Mesothelioma). Mechanical scarification of parietal pleura performed followed by instillation of 500mg Doxycycline. 28Fr tube placed.",
            4: "Procedure: Med Thoracoscopy\nPt: Lopez, M.\nSteps:\n1. GA / Single lumen ETT + Bronchial Blocker.\n2. 5th ICS incision.\n3. Drained 1.2L serous fluid.\n4. Scoped: Thickening + implants seen.\n5. Abrasion pleurodesis + Doxy 500mg.\n6. 28Fr tube placed.\nPlan: Suction -20.",
            5: "maria lopez has mesothelioma and a big right effusion we took her to the or used general anesthesia and a bronchial blocker made an incision in the 5th intercostal space drained 1200 of fluid saw tumor all over the pleura scraped it up with a scratcher pad and put in doxycycline 500mg for pleurodesis bleeding was minimal chest tube is in.",
            6: "Under general anesthesia with a bronchial blocker the right pleural space was accessed at the 5th intercostal space midaxillary line. Immediate drainage yielded 1.2 L of serous fluid. Rigid thoracoscopy revealed circumferential parietal pleural thickening and tumor implants consistent with the patient's known mesothelioma. Mechanical pleurodesis was performed using a gauze pad and scratcher followed by the instillation of 500 mg doxycycline. A 28 Fr chest tube was placed. The patient tolerated the procedure well.",
            7: "[Indication]\nRecurrent right effusion, Mesothelioma.\n[Anesthesia]\nGeneral, Bronchial Blocker.\n[Description]\nRight medical thoracoscopy. 1.2L serous fluid drained. Findings: Circumferential thickening. Intervention: Mechanical abrasion and Doxycycline (500mg) pleurodesis.\n[Plan]\nAdmit to Thoracic floor. Suction -20cmH20.",
            8: "Ms. Lopez underwent a medical thoracoscopy to address her recurrent right-sided effusion caused by mesothelioma. We accessed the chest at the 5th intercostal space and drained 1.2 liters of serous fluid. The visual inspection confirmed extensive tumor implants and thickening. To prevent recurrence, we performed mechanical pleurodesis by abrading the pleural surface and supplemented this with 500 mg of doxycycline. A 28 Fr chest tube was inserted for postoperative management.",
            9: "Indication: Advancing breathlessness from large recurrent right malignant pleural collection.\nDetails: Right lateral decubitus orientation. The 5th intercostal gap was breached. Entry resulted in immediate evacuation of 1.2 L of serous liquid. A rigid scope was used to survey the cavity, revealing encircling parietal thickening and tumor deposits. Physical sclerosis was executed using a gauze pad, followed by infusion of 500 mg doxycycline. A 28 Fr drain was anchored."
        },
        2: { # Pt: Hannah Nguyen (32650 - Talc, 1.4L, Breast Ca)
            1: "Indication: Recurrent Rt Effusion (Metastatic Breast Ca).\nAnesthesia: MAC.\nProcedure: Single-port semi-rigid thoracoscopy.\n- 7th ICS Posterior Axillary Line.\n- 1.4L serous fluid.\n- Findings: Patchy nodularity.\n- Action: Biopsies taken. 4g Talc slurry pleurodesis.\n- 20Fr Chest tube.\nComp: None.",
            2: "OPERATIVE SUMMARY: Ms. Nguyen, a 61-year-old female with metastatic breast carcinoma, presented for management of a symptomatic right pleural effusion. Under Monitored Anesthesia Care (MAC), a medical thoracoscopy was performed via the 7th posterior intercostal space. 1,400 mL of serous fluid was evacuated. Visualization revealed patchy parietal and diaphragmatic nodularity. Following biopsy acquisition, chemical pleurodesis was effected using 4g of sterile talc slurry. The patient remained hemodynamically stable.",
            3: "Billing: 32650 (Thoracoscopy w/ Pleurodesis).\nDiagnosis: Secondary Malignant Neoplasm of Pleura.\nProcedure: Ultrasound-guided access right 7th ICS. Drainage of 1.4L fluid. Biopsy of parietal nodules. Instillation of talc slurry (4g) for pleurodesis. Chest tube placement (20Fr).",
            4: "Resident Note\nPt: Nguyen, H.\nProc: Med Thoracoscopy (MAC)\nSteps:\n1. US localization 7th ICS.\n2. Local anesthetic + Propofol.\n3. Trocar -> 1.4L serous fluid out.\n4. Scoped: Patchy nodules seen/biopsied.\n5. Talc slurry 4g.\n6. 20Fr tube secured.\nPlan: Floor admit.",
            5: "hannah nguyen breast cancer met to pleura right side effusion done under mac sedation local numbing used 7th intercostal space drained 1.4 liters serous fluid saw some nodules on the diaphragm took biopsies put in 4 grams of talc slurry for the pleurodesis chest tube 20 french placed no complications.",
            6: "After ultrasound localization the right 7th intercostal space in the posterior axillary line was infiltrated with local anesthetic. Under MAC sedation a single-port semi-rigid medical thoracoscope was introduced. Approximately 1.4 L of serous fluid was drained. The parietal pleura showed patchy nodularity over the diaphragmatic and posterior pleura. Biopsies were obtained. A talc slurry 4 g in 100 mL saline was instilled and distributed. A 20 Fr chest tube was secured. Estimated blood loss was 15 mL.",
            7: "[Indication]\nRecurrent Right MPE (Breast Ca).\n[Anesthesia]\nMAC (Propofol).\n[Description]\nRight medical thoracoscopy via 7th ICS. 1.4L serous drainage. Findings: Patchy nodularity. Intervention: Biopsy and Talc (4g) pleurodesis.\n[Plan]\nAdmit. Water seal when leak resolves.",
            8: "Ms. Nguyen was treated for a recurrent right pleural effusion stemming from her breast cancer. We performed the procedure under MAC sedation, entering through the 7th intercostal space. We successfully drained 1.4 liters of serous fluid. The thoracoscopy showed patchy nodules on the diaphragm, which we biopsied. We then instilled a slurry containing 4 grams of talc to induce pleurodesis. A 20 Fr chest tube was placed at the end of the case.",
            9: "Indication: Air hunger and orthopnea from returning right pleural fluid.\nDetails: After ultrasound mapping, the right 7th intercostal gap was numbed. A single-port scope was inserted. Roughly 1.4 L of serous liquid was siphoned. The parietal lining displayed patchy bumps. Samples were acquired. A talc mixture (4 g) was introduced and spread. A 20 Fr drain was fixed."
        },
        3: { # Pt: Samuel Ortiz (32650 - Mechanical + Talc, 2.1L, Hepatic Hydrothorax)
            1: "Indication: Refractory Hepatic Hydrothorax (Rt).\nPt: 59M Cirrhosis.\nProcedure: Medical Thoracoscopy.\n- 6th ICS.\n- 2.1L clear straw fluid.\n- Findings: Smooth pleura, no nodules.\n- Action: Mechanical abrasion + 4g Talc slurry.\n- 24Fr Chest tube.\nPlan: Albumin replacement.",
            2: "PROCEDURE NOTE: Thoracoscopic management of hepatic hydrothorax.\nPATIENT: Samuel Ortiz (59M).\nINDICATION: Refractory right-sided transudative effusion.\nFINDINGS: Entry at the right 6th ICS yielded 2.1 L of clear, straw-colored transudate. Inspection revealed a smooth, glistening parietal pleura devoid of nodularity. \nINTERVENTION: Dual-modality pleurodesis was performed utilizing mechanical abrasion followed by the instillation of 4g talc slurry. Hemodynamics were managed with albumin.",
            3: "CPT: 32650.\nDiagnosis: Hepatic Hydrothorax.\nProcedure: Right medical thoracoscopy. Drainage of 2100mL transudative fluid. Visual inspection negative for malignancy. Pleurodesis performed via mechanical abrasion and 4g talc instillation. 24Fr chest tube placed.",
            4: "Procedure: Thoracoscopy/Pleurodesis\nPt: Ortiz, S.\nSteps:\n1. GA/ETT.\n2. US guidance -> 6th ICS.\n3. Drained 2.1L straw fluid.\n4. Pleura looked normal.\n5. Abrasion + Talc (4g).\n6. 24Fr tube.\nNote: Gave albumin for hypotension.",
            5: "samuel ortiz liver cirrhosis with hepatic hydrothorax right side huge effusion doing thoracoscopy to try and stick it we drained 2.1 liters of clear fluid pleura looked smooth no cancer seen we did mechanical abrasion and put in 4g of talc chest tube placed watch his bp he got a little low gave albumin.",
            6: "Ultrasound localization identified a large free-flowing right effusion. A 2 cm incision was made in the right 6th intercostal space midaxillary line. After trocar insertion 2.1 L of clear straw-colored fluid was drained. Thoracoscopic inspection showed smooth parietal pleura without nodularity. Mechanical abrasion pleurodesis was performed using a thoracoscopic pad followed by 4 g of sterile talc in 100 mL saline. A 24 Fr chest tube was placed posteriorly.",
            7: "[Indication]\nRefractory Right Hepatic Hydrothorax.\n[Anesthesia]\nGeneral.\n[Description]\nRight medical thoracoscopy. 2.1L clear fluid drained. Normal pleura. Intervention: Mechanical abrasion + Talc (4g) pleurodesis.\n[Plan]\nStep-down unit. Albumin replacement. Evaluate for TIPS.",
            8: "Mr. Ortiz underwent a medical thoracoscopy for a refractory hepatic hydrothorax on the right side. We accessed the chest at the 6th intercostal space and drained 2.1 liters of clear fluid. The pleural surface appeared healthy with no signs of cancer. To treat the effusion, we performed mechanical abrasion of the pleura and instilled 4 grams of talc. We placed a 24 Fr chest tube and administered albumin to manage transient hypotension.",
            9: "Indication: Breathlessness and frequent admissions for massive right fluid collection.\nDetails: Ultrasound mapping spotted a large free-flowing right collection. A 2 cm cut was made in the right 6th intercostal gap. After trocar entry, 2.1 L of clear liquid was evacuated. Scope survey showed slick parietal lining without bumps. Physical scraping sclerosis was executed; 4 g of sterile talc was then dispersed. A 24 Fr drain was sited."
        },
        4: { # Pt: Liam Johnson (32650 - Mech + Talc Poudrage, 150ml, Pneumo)
            1: "Indication: Recurrent Left Spontaneous Pneumothorax.\nProc: Thoracoscopy + Pleurodesis.\n- 5th ICS.\n- Findings: Apical blebs (stapled by Thoracic).\n- Action: Mechanical pleurodesis + 4g Talc poudrage.\n- 24Fr Chest tube.\nComp: Transient desat -> recruited.",
            2: "OPERATIVE REPORT: Mr. Johnson presented with a recurrent primary spontaneous pneumothorax (Left). Under general anesthesia with single-lung ventilation, the left pleural cavity was accessed. Apical blebs were identified and managed via stapling (see separate note). The medical thoracoscopy team proceeded with pleurodesis via mechanical abrasion of the apical and parietal pleura, augmented by insufflation of 4g sterile talc (poudrage). A 24 Fr apical chest tube was placed.",
            3: "Service: Thoracoscopy with pleurodesis (32650).\nDiagnosis: Recurrent Pneumothorax.\nDetails: Left 5th ICS access. Limited fluid (150mL). Identification of apical blebs. Mechanical abrasion performed. Insufflation of dry talc (4g poudrage). Chest tube placement (24Fr).",
            4: "Resident Note\nPt: Johnson, L.\nProc: Pleurodesis for Pneumo\nSteps:\n1. GA/DLT (Left lung isolation).\n2. 5th ICS entry.\n3. Blebs seen (stapled).\n4. Mechanical abrasion done.\n5. Talc poudrage 4g.\n6. 24Fr tube.\nPlan: Water seal when leak stops.",
            5: "liam johnson 27yo male recurrent pneumo on the left went to OR used a double lumen tube for isolation found some blebs at the apex thoracic surgery stapled those we did the pleurodesis scrubbed the pleura with gauze and blew in 4g of talc powder chest tube left at the top desatted a bit but fine now.",
            6: "The patient was positioned in right lateral decubitus. Entry into the left pleural space at the 5th intercostal space yielded a small amount of serosanguinous fluid and air. Thoracoscopic inspection revealed several apical blebs. These were stapled by the thoracic surgery team. The medical thoracoscopy team performed mechanical pleurodesis along the apical and parietal pleura followed by insufflation of 4 g sterile talc as dry powder. A 24 Fr chest tube was left at the apex.",
            7: "[Indication]\nRecurrent Left Spontaneous Pneumothorax.\n[Anesthesia]\nGeneral, DLT.\n[Description]\nLeft medical thoracoscopy. Blebs identified/stapled. Mechanical abrasion + 4g Talc poudrage performed. 24Fr apical tube.\n[Plan]\nDaily CXR. Smoking cessation.",
            8: "Mr. Johnson required surgery for a recurrent spontaneous pneumothorax on the left side. We utilized single-lung ventilation to access the chest through the 5th intercostal space. We found apical blebs, which were stapled. Following that, we performed mechanical pleurodesis using gauze and insufflated 4 grams of dry talc powder to prevent recurrence. A 24 Fr chest tube was placed at the apex.",
            9: "Indication: Third episode of left spontaneous lung collapse with lasting air leak.\nDetails: The patient was placed in right lateral decubitus. Entry into the left pleural void at the 5th intercostal gap yielded minimal liquid and air. Scope survey revealed several apical blisters. The blisters were stapled. The team executed physical sclerosis along the lining using gauze pads, followed by puffing of 4 g sterile talc. A 24 Fr drain was left at the peak."
        },
        5: { # Pt: Olivia Brown (32650 - Talc, 900ml, Loculated Ovarian)
            1: "Indication: Loculated malignant effusion (Ovarian).\nProc: Thoracoscopy + Adhesiolysis.\n- 6th ICS.\n- 900mL serous fluid.\n- Action: Blunt lysis of adhesions. Biopsies. 4g Talc slurry.\n- 20Fr Chest tube.\nDisposition: Oncology floor.",
            2: "PROCEDURE NOTE: Medical thoracoscopy with adhesiolysis and pleurodesis.\nPATIENT: Ms. Brown (65F).\nINDICATION: Symptomatic loculated left pleural effusion.\nFINDINGS: Upon entry at the 6th ICS, extensive loculations were noted. 900 mL of fluid was evacuated. Blunt adhesiolysis was required to disrupt septations. Nodular implants were biopsied.\nINTERVENTION: 4g Talc slurry instillation. 20 Fr chest tube placement.",
            3: "CPT 32650.\nSite: Left hemithorax.\nComplexity: Loculated effusion requiring lysis of adhesions.\nVolume: 900mL drained.\nPathology: Metastatic Ovarian Carcinoma.\nTherapy: Talc slurry (4g) pleurodesis. 20Fr Chest tube.",
            4: "Procedure: Thoracoscopy (Loculated)\nPt: Brown, O.\nSteps:\n1. Moderate sedation.\n2. US showed septations.\n3. 6th ICS entry -> 900mL drained.\n4. Adhesions broken down bluntly.\n5. Biopsies taken.\n6. Talc slurry 4g.\n7. 20Fr tube.\nPlan: Floor.",
            5: "olivia brown ovarian cancer loculated effusion left side moderate sedation used went in at the 6th intercostal space had to break up a lot of adhesions bluntly to get the fluid out drained 900ml took biopsies of the nodules put in 4g talc slurry for pleurodesis chest tube 20fr she had some pain but fentanyl helped.",
            6: "Bedside ultrasound showed multiple septations and loculations along the lateral left chest. A 2 cm incision was made at the 6th intercostal space midaxillary line. Trocar insertion yielded 900 mL of serous fluid from the largest locule. A semi-rigid thoracoscope was advanced adhesions were bluntly lysed to break down septations. Multiple parietal pleural biopsies were taken from nodular areas. After near-complete drainage 4 g talc in 50 mL saline was instilled. A 20 Fr chest tube was placed and secured.",
            7: "[Indication]\nLoculated Left MPE (Ovarian).\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft medical thoracoscopy. Lysis of adhesions. 900mL drainage. Biopsies. 4g Talc slurry pleurodesis.\n[Plan]\nAdmit. Water seal POD 1.",
            8: "Ms. Brown presented with a loculated malignant effusion on the left side due to ovarian cancer. Under moderate sedation, we entered the 6th intercostal space. We drained 900 mL of fluid but had to perform blunt lysis of adhesions to break up the septations. We biopsied the nodular areas and then instilled 4 grams of talc slurry. A 20 Fr chest tube was secured for drainage.",
            9: "Indication: Worsening breathlessness from pocketed malignant pleural collection.\nDetails: Bedside scan showed multiple walls and pockets. A 2 cm cut was made at the 6th intercostal gap. Trocar insertion yielded 900 mL of serous liquid. A semi-rigid scope was advanced; bands were bluntly severed to break down walls. Multiple parietal pleural samples were taken. After evacuation, 4 g talc was introduced. A 20 Fr drain was placed."
        },
        6: { # Pt: Ethan Miller (32650 - Talc, 1.6L, SCC Lung)
            1: "Indication: Recurrent Left MPE (SCC Lung).\nAnesthesia: General.\nProcedure: Medical Thoracoscopy.\n- 6th ICS.\n- 1.6L serosanguinous fluid.\n- Findings: Nodular pleura.\n- Action: Biopsies. 4g Talc slurry.\n- 24Fr Chest tube.\nPlan: Floor admit.",
            2: "OPERATIVE REPORT: Mr. Miller (72M) underwent left-sided medical thoracoscopy for a recurrent malignant pleural effusion secondary to squamous cell lung carcinoma. General anesthesia was utilized. Access at the 6th ICS facilitated the drainage of 1.6 L of serosanguinous fluid. Inspection revealed extensive nodular involvement of the parietal and diaphragmatic pleura. Biopsies were procured. Chemical pleurodesis was performed with 4g talc slurry. A 24 Fr thoracostomy tube was placed.",
            3: "Service: Thoracoscopy w/ pleurodesis (32650).\nIndication: Dyspnea, Malignant Effusion.\nProcedure: Left 6th ICS access. 1600mL serosanguinous drainage. Biopsy of pleural nodules. Talc slurry (4g) instillation. 24Fr Chest tube placed.",
            4: "Resident Note\nPt: Miller, E.\nProc: Talc Pleurodesis\nSteps:\n1. GA/ETT.\n2. US mark 6th ICS.\n3. Trocar -> 1.6L fluid.\n4. Nodules seen -> Biopsied.\n5. Talc slurry 4g instilled.\n6. 24Fr tube.\nPlan: Oncology f/u.",
            5: "ethan miller 72 male scc lung cancer recurrent left effusion general anesthesia used tube in went in at the 6th intercostal space drained 1.6 liters bloody fluid pleura looked bumpy took biopsies put in 4 grams of talc mixed with saline chest tube 24 french sending him to oncology floor.",
            6: "Left 6th intercostal space was selected under ultrasound guidance. Trocar entry produced a gush of serosanguinous fluid 1.6 L was drained. Thoracoscopy showed nodular parietal and diaphragmatic pleura. Multiple biopsies were taken. After drainage 4 g talc in 50 mL saline was instilled and spread evenly. A 24 Fr chest tube was secured. Estimated blood loss was 20 mL.",
            7: "[Indication]\nRecurrent Left MPE (Squamous Cell).\n[Anesthesia]\nGeneral.\n[Description]\nLeft medical thoracoscopy. 1.6L drainage. Findings: Nodular pleura. Intervention: Biopsies and 4g Talc slurry.\n[Plan]\nAdmit. Palliative consult.",
            8: "Mr. Miller came in for management of a recurrent left pleural effusion caused by his squamous cell lung cancer. We performed a thoracoscopy under general anesthesia, entering at the 6th intercostal space. We drained 1.6 liters of serosanguinous fluid. The pleura was nodular, so we took biopsies. We completed the procedure by instilling 4 grams of talc slurry for pleurodesis and placing a 24 Fr chest tube.",
            9: "Indication: Worsening air hunger and orthopnea due to returning malignant pleural collection.\nDetails: Left 6th intercostal gap was chosen. Trocar entry produced a gush of bloody liquid; 1.6 L was evacuated. Scope showed lumpy parietal and diaphragmatic lining. Multiple samples were taken. After evacuation, 4 g talc was introduced and spread evenly. A 24 Fr drain was fixed."
        },
        7: { # Pt: Noah Allen (32650 - Talc, 1.3L, Renal Cell)
            1: "Indication: Recurrent Left MPE (Renal Cell).\nProc: Thoracoscopy + Talc.\n- 6th ICS.\n- 1.3L hemorrhagic fluid.\n- Findings: Hemorrhagic implants.\n- Action: Biopsy + 4g Talc slurry.\n- 20Fr Chest tube.\nEBL: 35mL.",
            2: "PROCEDURE NOTE: Thoracoscopic pleurodesis.\nPATIENT: Noah Allen.\nINDICATION: Metastatic renal cell carcinoma with symptomatic effusion.\nPROCEDURE: Under moderate sedation, the left pleural space was accessed (6th ICS). 1.3 L of hemorrhagic fluid was drained. Direct visualization confirmed diffuse hemorrhagic implants. Biopsies confirmed the metastatic nature. 4g talc slurry was instilled for pleurodesis. A 20 Fr chest tube was inserted.",
            3: "CPT 32650.\nDiagnosis: Secondary Malignant Neoplasm (Renal origin).\nDetails: Ultrasound guided access. 1300mL hemorrhagic drainage. Biopsy of implants. 4g Talc slurry pleurodesis. 20Fr Chest tube placement. EBL 35mL.",
            4: "Procedure: Med Thoracoscopy\nPt: Allen, N.\nSteps:\n1. Mod sedation.\n2. 6th ICS entry.\n3. Drained 1.3L hemorrhagic fluid.\n4. Hemorrhagic implants biopsied.\n5. Talc slurry 4g.\n6. 20Fr tube.\nPlan: Floor.",
            5: "noah allen renal cell cancer metastatic left effusion moderate sedation local at the port site drained 1.3 liters of bloody fluid saw hemorrhagic implants all over took biopsies put in 4g talc slurry 20fr chest tube placed no complications.",
            6: "Ultrasound identified a large free-flowing effusion. A 2 cm incision at the 6th intercostal space allowed entry with a semi-rigid thoracoscope. 1.3 L of hemorrhagic fluid drained. Numerous hemorrhagic pleural implants were seen. Biopsies were obtained for confirmation. Talc slurry 4 g in 50 mL saline was instilled with even distribution. A 20 Fr chest tube was secured.",
            7: "[Indication]\nRecurrent Left MPE (Renal Cell).\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft medical thoracoscopy. 1.3L hemorrhagic drainage. Findings: Hemorrhagic implants. Intervention: Biopsies and 4g Talc slurry.\n[Plan]\nAdmit. Oncology f/u 1 week.",
            8: "Mr. Allen underwent a thoracoscopy for a recurrent left malignant effusion related to renal cell carcinoma. Using moderate sedation, we entered the 6th intercostal space and drained 1.3 liters of hemorrhagic fluid. We observed numerous hemorrhagic implants, which we biopsied. We then instilled 4 grams of talc slurry to achieve pleurodesis and secured a 20 Fr chest tube.",
            9: "Indication: Symptomatic returning left pleural collection with prior positive cytology for kidney cancer.\nDetails: Ultrasound identified a large free-flowing collection. A 2 cm cut at the 6th intercostal gap allowed entry with a semi-rigid scope. 1.3 L of bloody liquid drained. Numerous bloody pleural deposits were seen. Samples were obtained for confirmation. Talc mixture (4 g) was introduced with even distribution. A 20 Fr drain was fixed."
        },
        8: { # Pt: James Cooper (32650 - Talc, 1.5L, Mesothelioma Contralateral)
            1: "Indication: New Left Effusion (Mesothelioma).\nHistory: Prior Right pleurodesis.\nProc: Left Thoracoscopy + Talc.\n- 6th ICS.\n- 1.5L serous fluid.\n- Findings: Nodular pleura.\n- Action: Biopsy + 4g Talc slurry.\n- 24Fr Chest tube.",
            2: "OPERATIVE REPORT: Medical thoracoscopy (Left).\nPATIENT: James Cooper (70M).\nINDICATION: Biphasic mesothelioma with contralateral progression.\nPROCEDURE: General anesthesia. Left 6th ICS access yielded 1.5 L serous fluid. Nodular parietal pleura identified and biopsied. No diaphragmatic defects noted. Pleurodesis achieved via 4g talc slurry instillation. 24 Fr chest tube placed.",
            3: "CPT: 32650.\nSite: Left Pleural Space (Contralateral to primary disease).\nVolume: 1500mL drained.\nFindings: Mesothelioma implants.\nProcedure: Biopsy and chemical pleurodesis (4g Talc). 24Fr tube placement.",
            4: "Resident Note\nPt: Cooper, J.\nProc: Left Thoracoscopy\nSteps:\n1. GA/ETT.\n2. US -> 6th ICS.\n3. 1.5L serous drainage.\n4. Biopsied nodules.\n5. Talc slurry 4g.\n6. 24Fr tube.\nNote: Pt has prior Rt pleurodesis.",
            5: "james cooper mesothelioma patient had right side done before now has left effusion took him to or general anesthesia 6th intercostal space drained 1.5 liters serous fluid saw nodules biopsied them put in 4g talc slurry for pleurodesis chest tube 24 french admitting to floor.",
            6: "Ultrasound confirmed a large left effusion. Trocar entry at the 6th intercostal space allowed drainage of 1.5 L of serous fluid. Thoracoscopy showed nodular parietal pleura no diaphragmatic defects. Biopsies were obtained. Talc slurry 4 g in 50 mL saline was instilled evenly. A 24 Fr chest tube was placed. Estimated blood loss was 30 mL.",
            7: "[Indication]\nNew Left MPE (Mesothelioma).\n[Anesthesia]\nGeneral.\n[Description]\nLeft medical thoracoscopy. 1.5L drainage. Findings: Nodular pleura. Intervention: Biopsies and 4g Talc slurry.\n[Plan]\nAdmit. Palliative care.",
            8: "Mr. Cooper presented with a new left-sided effusion due to mesothelioma, having previously had the right side treated. We performed a left medical thoracoscopy under general anesthesia. We drained 1.5 liters of fluid and biopsied the nodular parietal pleura. We then instilled 4 grams of talc slurry to secure pleurodesis. A 24 Fr chest tube was placed for drainage.",
            9: "Indication: Increasing breathlessness due to new opposite-side collection in a patient not eligible for further systemic therapy.\nDetails: Ultrasound confirmed a large left collection. Trocar entry at the 6th intercostal gap allowed evacuation of 1.5 L of serous liquid. Scope showed lumpy parietal lining; no diaphragmatic holes. Samples were obtained. Talc mixture (4 g) was introduced evenly. A 24 Fr drain was placed."
        },
        9: { # Pt: Ava Thompson (32650 - Talc, 1.7L, Adeno Bilateral)
            1: "Indication: Left dominant MPE (Lung Adeno).\nProc: Thoracoscopy + Talc.\n- 7th ICS.\n- 1.7L serosanguinous fluid.\n- Findings: Diffuse implants.\n- Action: Biopsy + 4g Talc slurry.\n- 20Fr Chest tube.\nPlan: Monitor contralateral side.",
            2: "PROCEDURE NOTE: Left medical thoracoscopy.\nPATIENT: Ava Thompson.\nINDICATION: Symptomatic left-dominant bilateral malignant effusions.\nPROCEDURE: Under moderate sedation, the left chest was accessed at the 7th ICS. 1.7 L of serosanguinous fluid was evacuated. Diffuse parietal and diaphragmatic implants were visualized and biopsied. Pleurodesis was performed using 4g talc slurry. A 20 Fr chest tube was inserted.",
            3: "Code: 32650.\nSite: Left Hemithorax.\nCondition: Metastatic Lung Adenocarcinoma.\nIntervention: Drainage of 1700mL fluid. Biopsy of implants. Instillation of sclerosing agent (4g Talc). Chest tube placement (20Fr).",
            4: "Procedure: Med Thoracoscopy (Left)\nPt: Thompson, A.\nSteps:\n1. Mod sedation.\n2. 7th ICS entry.\n3. 1.7L drained.\n4. Implants biopsied.\n5. Talc slurry 4g.\n6. 20Fr tube.\nPlan: Watch right side.",
            5: "ava thompson lung adeno bilateral effusions left is worse did thoracoscopy on left moderate sedation 7th intercostal space drained 1.7 liters bloody fluid saw implants everywhere took biopsies put in 4g talc slurry chest tube 20 french check right side later.",
            6: "Ultrasound-guided entry at the left 7th intercostal space allowed drainage of 1.7 L serosanguinous fluid. Thoracoscopy revealed diffuse parietal pleural implants. Biopsies were obtained. Talc slurry 4 g in 50 mL saline was instilled and distributed. A 20 Fr chest tube was secured. Estimated blood loss was 25 mL. Disposition Admitted to oncology floor.",
            7: "[Indication]\nLeft dominant MPE (Lung Adeno).\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft medical thoracoscopy. 1.7L drainage. Findings: Diffuse implants. Intervention: Biopsies and 4g Talc slurry.\n[Plan]\nAdmit. Monitor right side.",
            8: "Ms. Thompson required treatment for a symptomatic left-sided malignant effusion, complicating her bilateral disease. We performed a left medical thoracoscopy under moderate sedation. We drained 1.7 liters of serosanguinous fluid and noted diffuse pleural implants, which were biopsied. We instilled 4 grams of talc slurry for pleurodesis and placed a 20 Fr chest tube.",
            9: "Indication: Symptomatic left-dominant malignant pleural collection causing orthopnea.\nDetails: Ultrasound-guided entry at the left 7th intercostal gap allowed evacuation of 1.7 L bloody liquid. Scope revealed widespread parietal pleural deposits. Samples were obtained. Talc mixture (4 g) was introduced and distributed. A 20 Fr drain was secured."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns list of mock data to ensure distinct names for each variation.
    Indexes correspond to the 10 notes in the source file.
    """
    return [
        {"idx": 0, "orig_name": "Daniel Carter", "orig_age": 68, "names": ["Robert Smith", "James Johnson", "Michael Williams", "William Brown", "David Jones", "Richard Miller", "Joseph Davis", "Thomas Garcia", "Charles Rodriguez"]},
        {"idx": 1, "orig_name": "Maria Lopez", "orig_age": 73, "names": ["Mary Wilson", "Patricia Martinez", "Linda Anderson", "Barbara Taylor", "Elizabeth Thomas", "Jennifer Hernandez", "Maria Moore", "Susan Martin", "Margaret Jackson"]},
        {"idx": 2, "orig_name": "Hannah Nguyen", "orig_age": 61, "names": ["Dorothy Thompson", "Lisa White", "Nancy Lopez", "Karen Lee", "Betty Gonzalez", "Helen Harris", "Sandra Clark", "Donna Lewis", "Carol Robinson"]},
        {"idx": 3, "orig_name": "Samuel Ortiz", "orig_age": 59, "names": ["Ruth Walker", "Sharon Perez", "Michelle Hall", "Laura Young", "Sarah Allen", "Kimberly Sanchez", "Deborah Wright", "Jessica King", "Shirley Scott"]}, 
        # Note: Index 3 is Male in source, but I generated female names above by mistake? 
        # Wait, Samuel Ortiz is Male. Correcting names to Male for index 3 below.
        
        {"idx": 3, "orig_name": "Samuel Ortiz", "orig_age": 59, "names": ["Christopher Walker", "Daniel Perez", "Paul Hall", "Mark Young", "Donald Allen", "George Sanchez", "Kenneth Wright", "Steven King", "Edward Scott"]},
        
        {"idx": 4, "orig_name": "Liam Johnson", "orig_age": 27, "names": ["Brian Green", "Ronald Baker", "Anthony Adams", "Kevin Nelson", "Jason Hill", "Matthew Ramirez", "Gary Campbell", "Timothy Mitchell", "Jose Roberts"]},
        {"idx": 5, "orig_name": "Olivia Brown", "orig_age": 65, "names": ["Cynthia Carter", "Angela Phillips", "Melissa Evans", "Brenda Turner", "Amy Torres", "Anna Parker", "Rebecca Collins", "Virginia Edwards", "Kathleen Stewart"]},
        {"idx": 6, "orig_name": "Ethan Miller", "orig_age": 72, "names": ["Larry Flores", "Jeffrey Morris", "Frank Nguyen", "Scott Murphy", "Eric Rivera", "Stephen Cook", "Andrew Rogers", "Raymond Morgan", "Gregory Peterson"]},
        {"idx": 7, "orig_name": "Noah Allen", "orig_age": 63, "names": ["Joshua Cooper", "Jerry Reed", "Dennis Bailey", "Walter Bell", "Patrick Gomez", "Peter Kelly", "Harold Howard", "Douglas Ward", "Henry Cox"]},
        {"idx": 8, "orig_name": "James Cooper", "orig_age": 70, "names": ["Carl Diaz", "Arthur Richardson", "Ryan Wood", "Roger Watson", "Joe Brooks", "Juan Bennett", "Jack Gray", "Albert James", "Jonathan Reyes"]},
        {"idx": 9, "orig_name": "Ava Thompson", "orig_age": 67, "names": ["Martha Cruz", "Debra Hughes", "Amanda Price", "Stephanie Myers", "Carolyn Long", "Christine Foster", "Marie Sanders", "Janet Ross", "Catherine Morales"]}
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
    # Mock data list (corrected index 3 logic handled in loop below)
    base_data = get_base_data_mocks()
    # Correcting the list indexing issue if any
    base_data_map = {item['idx']: item for item in base_data}

    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through each original note in source data
    for idx, original_note in enumerate(source_data):
        if idx not in base_data_map:
            print(f"Warning: No base data mock for note index {idx}. Skipping.")
            continue
            
        record = base_data_map[idx]
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
            try:
                note_entry["note_text"] = variations_text[idx][style_num]
            except KeyError:
                print(f"Warning: Missing text variation for Note {idx} Style {style_num}. Skipping.")
                continue
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
            
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
    output_filename = output_dir / "synthetic_thoracoscopy_notes_part_061.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()