import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_094.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Provides mapping for original data to verify index alignment 
    and lists of synthetic names for the 9 variations.
    """
    return [
        # 32561 Notes (Fibrinolytics)
        {"idx": 0, "orig_name": "Margaret Chen", "orig_age": 67, "names": ["Alice Wong", "Betty Liu", "Catherine Zhang", "Diana Wu", "Elena Chang", "Fiona Hsu", "Grace Lin", "Helen Yang", "Irene Ho"]},
        {"idx": 1, "orig_name": "Harold Williams", "orig_age": 76, "names": ["Ian Roberts", "Jack Thomas", "Kevin Davis", "Liam Wilson", "Mason Clark", "Noah Lewis", "Oliver Walker", "Peter Hall", "Quinn Allen"]},
        {"idx": 2, "orig_name": "Rosa Martinez", "orig_age": 63, "names": ["Rachel Gomez", "Sofia Perez", "Teresa Diaz", "Ursula Reyes", "Vanessa Cruz", "Wendy Ortiz", "Ximena Ramos", "Yolanda Flores", "Zara Morales"]},
        {"idx": 3, "orig_name": "David O'Brien", "orig_age": 54, "names": ["Adam Kelly", "Brian Murphy", "Connor Sullivan", "Daniel Walsh", "Ethan Ryan", "Frank O'Connor", "George Byrne", "Henry Doyle", "Isaac Flynn"]},
        {"idx": 4, "orig_name": "Jennifer Walsh", "orig_age": 70, "names": ["Jane Smith", "Kelly Johnson", "Laura Brown", "Mary Jones", "Nicole Miller", "Olivia Davis", "Patricia Garcia", "Quinn Rodriguez", "Ruth Wilson"]},
        
        # 32662 Notes (VATS Excision)
        {"idx": 5, "orig_name": "Thomas Anderson", "orig_age": 65, "names": ["Steve Baker", "Tim Carter", "Ulysses Nelson", "Victor Hill", "Walter Adams", "Xavier Green", "Yusuf Campbell", "Zachary Mitchell", "Aaron Roberts"]},
        {"idx": 6, "orig_name": "Linda Petrova", "orig_age": 57, "names": ["Bella Ivanov", "Clara Sokolov", "Daria Volkov", "Eva Morozov", "Fay Popov", "Gia Kozlov", "Hope Lebedev", "Iris Novikov", "Julia Smirnov"]},
        {"idx": 7, "orig_name": "George Nakamura", "orig_age": 73, "names": ["Kenji Tanaka", "Leo Sato", "Mike Suzuki", "Nathan Takahashi", "Oscar Watanabe", "Paul Ito", "Quincy Yamamoto", "Ray Kobayashi", "Sam Saito"]},
        {"idx": 8, "orig_name": "Sandra Kowalski", "orig_age": 50, "names": ["Tina Nowak", "Una Wisniewski", "Vera Zielinski", "Willa Szymanski", "Xena Wozniak", "Yana Kamiński", "Zoe Lewandowski", "Abby Jankowski", "Beth Mazur"]},
        {"idx": 9, "orig_name": "Henry Okonkwo", "orig_age": 60, "names": ["Chidi Okafor", "David Eze", "Emeka Nwosu", "Femi Adebayo", "Gabriel Obi", "Hassan Ibrahim", "Idris Musa", "Jamal Abdullahi", "Kofi Mensah"]},

        # 32606 Notes (Thoracoscopy w/ Biopsy)
        {"idx": 10, "orig_name": "Barbara Mitchell", "orig_age": 67, "names": ["Carol Anderson", "Debra Scott", "Ellen Phillips", "Fran Evans", "Gina Turner", "Holly Parker", "Ida Collins", "Joan Edwards", "Kathy Stewart"]},
        {"idx": 11, "orig_name": "Charles Freeman", "orig_age": 55, "names": ["Larry Morris", "Mark Rogers", "Ned Reed", "Otis Cook", "Phil Morgan", "Quentin Bell", "Ralph Murphy", "Scott Bailey", "Tom Rivera"]},
        {"idx": 12, "orig_name": "Maria Santos", "orig_age": 62, "names": ["Ana Torres", "Bianca Ramirez", "Carla Watson", "Dina Brooks", "Eva Sanders", "Fernanda Price", "Gina Bennett", "Hilda Wood", "Inez Barnes"]},
        {"idx": 13, "orig_name": "Robert Jackson", "orig_age": 70, "names": ["Arthur Ross", "Bill Henderson", "Carl Coleman", "Don Jenkins", "Earl Perry", "Fred Powell", "Greg Long", "Hank Patterson", "Ivan Hughes"]},
        {"idx": 14, "orig_name": "Angela Torres", "orig_age": 47, "names": ["Jessica Flores", "Karen Washington", "Lisa Butler", "Mona Simmons", "Nina Foster", "Olga Gonzales", "Pamela Bryant", "Qiana Alexander", "Rita Russell"]},

        # 32556 Notes (Thoracentesis w/ Catheter)
        {"idx": 15, "orig_name": "William Turner", "orig_age": 64, "names": ["Sam Griffin", "Ted Hayes", "Uriah Myers", "Vince Ford", "Will Hamilton", "Xander Graham", "Yuri Sullivan", "Zack Wallace", "Andy Woods"]},
        {"idx": 16, "orig_name": "Dorothy Williams", "orig_age": 78, "names": ["Betty Cole", "Cindy West", "Doris Jordan", "Edith Owens", "Florence Reynolds", "Gertrude Fisher", "Harriet Ellis", "Irene Harrison", "June Gibson"]},
        {"idx": 17, "orig_name": "James Morrison", "orig_age": 67, "names": ["Kyle McDonald", "Lyle Marshall", "Mitch Gentry", "Nick Ortiz", "Owen Murray", "Pete Freeman", "Quinn Wells", "Rick Webb", "Stan Simpson"]},
        {"idx": 18, "orig_name": "Catherine Brown", "orig_age": 71, "names": ["Ann Stevens", "Barb Tucker", "Cathy Porter", "Debra Hunter", "Eve Hicks", "Faye Crawford", "Gail Henry", "Helen Boyd", "Ivy Mason"]},
        {"idx": 19, "orig_name": "Richard Hernandez", "orig_age": 59, "names": ["Joe Morales", "Ken Kennedy", "Lou Warren", "Moe Dixon", "Nat Ramos", "Otis Reyes", "Paul Burns", "Quincy Gordon", "Ray Shaw"]},
    ]

def get_variations():
    """
    Returns a nested dictionary of note variations.
    Structure: Note_Index (0-19) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Margaret Chen - 32561
            1: "Dx: R complex parapneumonic effusion.\nRx: Intrapleural fibrinolysis Day 1.\n- 14Fr chest tube in situ.\n- Instilled 10mg tPA / 5mg DNase in 50mL NS.\n- Clamp 2h -> Open to drain.\n- No pain/distress.",
            2: "CLINICAL SUMMARY: This 67-year-old female with a right-sided loculated parapneumonic effusion required intervention. The indwelling pleural catheter exhibited poor drainage secondary to loculations.\nINTERVENTION: Therapeutic instillation of fibrinolytic agents. Under sterile conditions, tissue plasminogen activator (10 mg) and dornase alfa (5 mg) were administered into the pleural space via the existing catheter. The device was clamped for a dwell time of 120 minutes to facilitate fibrinolysis, then opened to gravity drainage. The patient tolerated the procedure without adverse hemodynamic sequelae.",
            3: "Procedure: Instillation of fibrinolytic agent (CPT 32561).\nDevice: Indwelling pleural catheter (Right).\nAgents: tPA 10mg + DNase 5mg.\nTechnique: Sterile prep, injection of agents, 2-hour clamp time.\nMedical Necessity: To break down loculations in complex parapneumonic effusion.",
            4: "Procedure Note: Fibrinolytic Instillation\nIndication: Loculated effusion\nSteps:\n1. Sterile prep of catheter hub.\n2. Flush with NS.\n3. Instilled tPA 10mg/DNase 5mg.\n4. Clamped x 2 hours.\n5. Unclamped.\nPatient tolerated well.",
            5: "pt with loculated effusion right side we did the tpa dnase instillation today tube was flushed 10 tpa 5 dnase went in fine clamped it for two hours then opened it up no issues draining better now plan for bid dosing.",
            6: "Right-sided complex parapneumonic effusion with loculations requiring fibrinolysis. 10mg tPA and 5mg DNase mixed in 50mL NS instilled via existing pleural catheter under sterile technique. The catheter was clamped for 2 hours and then returned to drainage. Patient tolerated the procedure well with no chest pain or distress. Plan to continue BID dosing for 3 days.",
            7: "[Indication]\nRight complex parapneumonic effusion with loculations.\n[Anesthesia]\nNone (Local catheter access).\n[Description]\nInstilled 10mg tPA and 5mg DNase via 14Fr chest tube. Dwell time 2 hours.\n[Plan]\nBID dosing x 6 doses.",
            8: "Ms. Chen is a 67-year-old female suffering from a right-sided pneumonia that has developed into a complex, loculated effusion. Today, we proceeded with the first day of intrapleural fibrinolytic therapy. Using her existing 14Fr chest tube, we instilled a mixture of 10mg tPA and 5mg DNase. We clamped the tube for two hours to allow the medication to work, then opened it back up for drainage. She handled it very well.",
            9: "Diagnosis: Right-sided complex parapneumonic collection.\nAction: Administered fibrinolytic therapy via pleural catheter - Day 1.\nDetails: 10mg alteplase and 5mg dornase alfa were injected via the existing tube. The tube was occluded for 2 hours, then released for output. No discomfort noted."
        },
        1: { # Harold Williams - 32561
            1: "Indication: Empyema, multiloculated.\nProcedure: tPA/DNase instillation Day 1.\n- Cath flushed.\n- 10mg tPA / 5mg DNase instilled.\n- 2hr dwell.\n- Unclamped to water seal.",
            2: "PROCEDURE NOTE: Intrapleural administration of fibrinolytic agents.\nINDICATION: A 76-year-old male with a multiloculated empyema post-pneumonia.\nDESCRIPTION: The indwelling pigtail catheter was prepped. A solution containing 10 mg of tissue plasminogen activator and 5 mg of dornase alfa was instilled into the pleural cavity. The catheter was clamped for a dwell period of two hours to maximize therapeutic effect before being unclamped to water seal drainage.",
            3: "Billing Code: 32561 (Instillation of fibrinolytic agent).\nDosage: tPA 10mg, DNase 5mg.\nRoute: Via existing indwelling pleural catheter.\nIndication: Empyema with septations (ICD-10 J86.9).\nNote: First dose of planned regimen.",
            4: "Resident Procedure Note\nPatient: Harold Williams\nProcedure: Fibrinolytic Instillation\nSteps:\n1. Time out performed.\n2. Catheter hub cleaned.\n3. Meds instilled (tPA/DNase).\n4. Clamped x 2h.\n5. Opened to drainage.\nNo complications.",
            5: "Harold Williams 76M with empyema we put in the lytics today tpa 10 and dnase 5 pushed through the pigtail clamped it for a couple hours draining ok now no pain fever or anything will do again tonight.",
            6: "76M with multiloculated empyema. Instillation of fibrinolytic agents via indwelling pleural catheter Day 1. Sterile technique used. Pleural catheter flushed with 10mL saline. tPA 10mg in 30mL NS and DNase 5mg in 30mL NS instilled. Total dwell time 2 hours. Catheter unclamped to water seal. Patient stable.",
            7: "[Indication]\nEmpyema with multiple septations.\n[Anesthesia]\nNone.\n[Description]\nInstilled tPA 10mg and DNase 5mg via left pigtail catheter. Dwell time 2 hours.\n[Plan]\nContinue q12h dosing.",
            8: "Mr. Williams has a complicated empyema that isn't draining well with just the catheter. Today we started fibrinolytic therapy to break up the loculations. We injected tPA and DNase through his chest tube and let it sit for two hours. Afterward, we opened the tube back up to the water seal. He didn't have any pain or fever during the process.",
            9: "Indication: Septated empyema.\nAction: Introduced fibrinolytic agents via pleural tube (Day 1).\nDetails: The catheter was prepped. 10mg alteplase and 5mg dornase alfa were injected. The tube was closed for 2 hours, then released to the water seal. Patient remained stable."
        },
        2: { # Rosa Martinez - 32561
            1: "Dx: Loculated MPE (Breast CA).\nProc: PleurX fibrinolysis Day 1.\n- 10mg tPA instilled.\n- Clamped 1.5h.\n- Drained 450mL serosanguinous.\n- No complications.",
            2: "PROCEDURE: Instillation of fibrinolytic agent via tunneled pleural catheter.\nDIAGNOSIS: Metastatic breast cancer with loculated malignant pleural effusion.\nDETAILS: The patency of the PleurX catheter was confirmed. Ten milligrams of alteplase were instilled into the pleural space. Following a 90-minute clamp period, gravity drainage yielded 450 mL of serosanguinous fluid, suggesting effective lysis of loculations.",
            3: "CPT 32561: Instillation of fibrinolytic agent via chest tube/catheter.\nAgent: Alteplase 10mg.\nAccess: Existing PleurX catheter (Left).\nOutcome: 450mL drainage post-procedure.\nIndication: Malignant pleural effusion with loculations.",
            4: "Procedure: tPA Instillation via PleurX\n1. Sterile prep.\n2. Flushed PleurX.\n3. Instilled 10mg tPA.\n4. Clamped 1.5 hours.\n5. Drained 450mL.\nPatient tolerated well.",
            5: "Rosa Martinez w metastatic breast ca has a loculated effusion pleurx wasn't draining so we put in 10 of tpa clamped it for an hour and half got out 450ml fluid looks bloody but thats expected no issues.",
            6: "Malignant pleural effusion with loculations breast CA metastatic. Fibrinolytic agent instillation via PleurX catheter Day 1. PleurX catheter confirmed patent with flush. Instilled 10mg alteplase in 50mL saline. Catheter clamped 1.5 hours. Released to gravity drainage. 450mL serosanguinous fluid drained over next 4 hours. No complications.",
            7: "[Indication]\nLoculated malignant pleural effusion.\n[Anesthesia]\nNone.\n[Description]\nInstilled 10mg Alteplase via left PleurX. Clamped 90 mins. Drained 450mL.\n[Plan]\nDaily instillations.",
            8: "Ms. Martinez has a malignant effusion that has become loculated, reducing the effectiveness of her PleurX catheter. Today we treated this by injecting 10mg of alteplase through the catheter. We clamped it for about an hour and a half to let the medicine work. When we opened it back up, we were able to drain 450mL of fluid, which is a good result.",
            9: "Diagnosis: Malignant pleural collection with septations.\nAction: Administered thrombolytic via tunneled catheter.\nDetails: 10mg alteplase injected. Tube occluded for 1.5 hours. Released to gravity, yielding 450mL serosanguinous output. Patient comfortable."
        },
        3: { # David O'Brien - 32561
            1: "Indication: Organized hemothorax.\nProc: tPA/DNase instillation.\n- 10mg tPA / 5mg DNase.\n- 2hr dwell.\n- Output: 200mL bloody fluid.\n- Stable.",
            2: "PROCEDURE REPORT: Intrapleural fibrinolytic therapy for organized hemothorax.\nCLINICAL CONTEXT: 54-year-old male post-trauma with retained hemothorax.\nINTERVENTION: To facilitate drainage of the organized collection, sequential instillation of alteplase (10 mg) and dornase alfa (5 mg) was performed via the chest tube. Following a two-hour clamp period, suction was reapplied, yielding 200 mL of dark sanguineous fluid.",
            3: "Code 32561: Instillation of fibrinolytic agent.\nAgents: Alteplase 10mg, Dornase 5mg.\nSite: Right chest tube.\nIndication: Retained hemothorax (Traumatic).\nOutput: 200mL post-instillation.",
            4: "Procedure: Lytic Instillation\nIndication: Hemothorax\nSteps:\n1. Flushed tube.\n2. Instilled tPA then DNase.\n3. Clamped 2 hours.\n4. Suction -20cmH2O.\nOutput 200mL. Patient stable.",
            5: "Trauma patient with the stuck hemothorax we did the lytics tpa dnase put it in clamped for two hours got out about 200 cc dark blood patient is fine sats good on 2L plan for bid dosing.",
            6: "Intrapleural fibrinolytic administration Day 1. Organized hemothorax post-trauma. Confirmed tube patency. Instilled Alteplase 10mg and Dornase alfa 5mg. Sequential instillation. Catheter clamped for 2 hours total dwell. Opened to -20cmH2O suction. Immediate output 200mL dark bloody fluid. Patient hemodynamically stable.",
            7: "[Indication]\nOrganized traumatic hemothorax.\n[Anesthesia]\nNone.\n[Description]\nInstilled tPA 10mg/DNase 5mg via chest tube. 2 hour dwell. 200mL output.\n[Plan]\nBID dosing x 3 days.",
            8: "Mr. O'Brien is dealing with a retained hemothorax from his car accident. To help clear the blood clots, we administered tPA and DNase through his chest tube today. We let the medication sit for two hours before turning the suction back on. This resulted in the drainage of 200mL of dark, bloody fluid, indicating it's breaking up the clot.",
            9: "Indication: Retained blood collection.\nAction: Injected fibrinolytic agents via pleural drain.\nDetails: 10mg alteplase and 5mg dornase alfa administered. Drain closed for 2 hours. Re-opened to suction, yielding 200mL bloody output. Vitals stable."
        },
        4: { # Jennifer Walsh - 32561
            1: "Dx: Loculated MPE (NSCLC).\nProc: IPC fibrinolysis Day 1.\n- 10mg tPA / 5mg DNase.\n- 2hr dwell w/ repositioning.\n- Drained 850mL straw fluid.\n- SpO2 improved 89->94%.",
            2: "PROCEDURE: Intrapleural fibrinolytic therapy via indwelling pleural catheter.\nINDICATION: Recurrent loculated malignant pleural effusion secondary to Stage IV NSCLC.\nDESCRIPTION: A solution of 10 mg tPA and 5 mg DNase was instilled into the pleural space via the PleurX catheter. The patient was repositioned during the two-hour dwell time to ensure distribution. Subsequent drainage yielded 850 mL of fluid, resulting in symptomatic improvement and increased oxygen saturation.",
            3: "CPT 32561. Instillation of fibrinolytic.\nCatheter: Left IPC.\nDose: 10mg tPA / 5mg DNase.\nVolume Drained: 850mL.\nMedical Necessity: Symptomatic loculated MPE.",
            4: "Procedure: IPC Lytic Instillation\n1. Prep and flush.\n2. Instill tPA/DNase.\n3. Clamp 2h, rotate patient.\n4. Drain.\nOutput 850mL. Breathing improved.",
            5: "Jennifer Walsh lung cancer patient with the pleurx that stopped draining we put in tpa and dnase today clamped it moved her around a bit after two hours got out huge amount 850ml she feels way better sats up.",
            6: "Stage IV NSCLC with recurrent loculated left MPE. Fibrinolytic instillation via IPC Day 1. Catheter flushed patent. Instilled 10mg tPA + 5mg DNase in 100mL NS. Catheter clamped. Patient repositioned side-to-side over 2hr dwell period. Drained 850mL straw-colored fluid after unclamping. No complications.",
            7: "[Indication]\nLoculated malignant pleural effusion (NSCLC).\n[Anesthesia]\nNone.\n[Description]\nInstilled 10mg tPA/5mg DNase via IPC. 2 hour dwell. Drained 850mL.\n[Plan]\nDaily x 3 days.",
            8: "Ms. Walsh has a malignant effusion that wasn't draining due to loculations. We treated this by injecting tPA and DNase into her PleurX catheter. We asked her to move side-to-side while the tube was clamped for two hours to spread the medicine. This was very effective, draining 850mL of fluid and significantly improving her oxygen levels and breathing.",
            9: "Diagnosis: Septated malignant fluid collection.\nAction: Administered lytic therapy via indwelling catheter.\nDetails: 10mg alteplase and 5mg dornase alfa injected. Catheter occluded for 2 hours with patient rotation. Released to drain 850mL. Respiratory status improved."
        },
        5: { # Thomas Anderson - 32662
            1: "Indication: Thymoma.\nProcedure: VATS thymectomy/mass excision.\n- 3 ports.\n- Mass dissected from pericardium/innominate.\n- Margins clear.\n- Removed via endobag.\n- 24Fr chest tube.",
            2: "OPERATIVE SUMMARY: Video-assisted thoracoscopic excision of anterior mediastinal mass.\nFINDINGS: A 4.5 cm well-circumscribed thymic mass was identified in the anterior mediastinum. There was no evidence of invasion into the pericardium or great vessels.\nPROCEDURE: Using a three-port VATS approach, the mediastinal pleura was incised. The mass was dissected free from the pericardial and thymic bed using ultrasonic energy. Complete resection was achieved, and the specimen was extracted via an endo-catch bag.",
            3: "CPT 32662: VATS excision of mediastinal cyst, tumor, or mass.\nApproach: 3-port VATS.\nPathology: Thymoma (4.5cm).\nWork: Complete dissection from pericardium and innominate vein; extraction via bag; chest tube placement.",
            4: "Procedure: VATS Resection Mediastinal Mass\n1. GA / DLT / Lateral decubitus.\n2. Ports: 5th, 3rd, 7th ICS.\n3. Identified mass anterior mediastinum.\n4. Dissected with harmonic.\n5. Bagged and removed.\n6. Chest tube placed.",
            5: "Vats for thymoma right side wait left side 3 ports mass was anterior dissected it off the vessels and heart looked contained put it in a bag and pulled it out chest tube in blood loss minimal patient fine.",
            6: "Video-assisted thoracoscopic surgery (VATS) with excision of mediastinal lesion. 65-year-old male with 4.2cm anterior mediastinal mass. Three port placements. Thoracoscope introduced. Anterior mediastinum visualized with well-encapsulated mass arising from thymic tissue. Careful dissection performed using harmonic scalpel separating mass from pericardium and left innominate vein. Specimen removed via endo-bag. Single 24Fr chest tube placed.",
            7: "[Indication]\nAnterior mediastinal mass (Thymoma).\n[Anesthesia]\nGeneral, DLT.\n[Description]\n3-port VATS. 4.5cm mass dissected from anterior mediastinum. Complete excision. Endo-bag extraction.\n[Plan]\nAdmit, chest tube management.",
            8: "Mr. Anderson underwent a VATS procedure to remove a suspicious mass in his chest. We used three small incisions to access the space. The mass, located in the anterior mediastinum, was carefully separated from the heart and major veins. We were able to remove it completely in a retrieval bag. A chest tube was left in place to drain any fluid or air.",
            9: "Diagnosis: Anterior mediastinal neoplasm.\nAction: Thoracoscopic resection of mediastinal tumor.\nDetails: Three-port access established. Tumor separated from surrounding structures. Complete removal achieved via retrieval sac. Drainage tube inserted."
        },
        6: { # Linda Petrova - 32662
            1: "Indication: Post. mediastinal mass (Schwannoma).\nProc: VATS excision.\n- 3 ports.\n- Mass at T6-T7.\n- Dissected from nerve root.\n- Nerve transected.\n- Specimen extracted.\n- 28Fr tube.",
            2: "OPERATIVE REPORT: Video-assisted thoracoscopic resection of posterior mediastinal neurogenic tumor.\nFINDINGS: A 3.5 cm encapsulated schwannoma arising from the intercostal nerve at the T6-T7 level.\nTECHNIQUE: A standard three-port VATS approach was utilized. The parietal pleura overlying the mass was incised. The tumor was dissected from the intercostal nerve of origin, which was transected to ensuring clear margins. The specimen was removed intact.",
            3: "CPT 32662: VATS excision of mediastinal tumor.\nLocation: Posterior mediastinum.\nPathology: Schwannoma.\nDetails: Dissection from spine/nerve root, complete excision, extraction.",
            4: "Procedure: VATS Posterior Mediastinal Mass Excision\n1. Position: LLD.\n2. Ports placed.\n3. Mass identified T6-T7.\n4. Pleura opened.\n5. Tumor dissected off nerve.\n6. Extracted.\n7. Chest tube.",
            5: "Linda Petrova with the nerve tumor in the back chest vats 3 ports found the mass at t6 t7 dissected it out cut the nerve pulled it out in a bag checked for leaks none chest tube in.",
            6: "Video-assisted thoracoscopic excision of posterior mediastinal tumor. 3.5cm encapsulated mass arising from posterior mediastinum at T6-T7 level consistent with nerve sheath tumor. Overlying pleura incised. Tumor carefully dissected from intercostal nerve using bipolar cautery and blunt dissection. Nerve of origin transected proximally and distally with clear margins. Specimen placed in retrieval bag and extracted.",
            7: "[Indication]\nPosterior mediastinal mass (Schwannoma).\n[Anesthesia]\nGeneral, DLT.\n[Description]\n3-port VATS. Mass dissected from T6-T7 intercostal nerve. Nerve transected. Mass removed.\n[Plan]\nAdmit, monitor for CSF leak (none seen).",
            8: "Ms. Petrova had a tumor on a nerve near her spine. We used video-assisted surgery to remove it. Through three small ports, we located the mass and carefully separated it from the nerve, which had to be cut to remove the tumor completely. We checked to make sure there was no fluid leaking from the spine area and then closed up, leaving a chest tube.",
            9: "Diagnosis: Posterior mediastinal nerve sheath neoplasm.\nAction: Thoracoscopic ablation of mediastinal lesion.\nDetails: Lesion isolated at T6-T7. Separated from neural origin. Complete extraction performed. Drain placed."
        },
        7: { # George Nakamura - 32662
            1: "Indication: Middle mediastinal cyst.\nProc: VATS excision.\n- 3 ports.\n- Cyst 6cm, adherent to esophagus/bronchus.\n- Aspirated -> Dissected.\n- Complete wall removal.\n- Chest tube.",
            2: "OPERATIVE SUMMARY: Thoracoscopic resection of bronchogenic cyst.\nFINDINGS: A 6 cm cystic lesion was identified in the middle mediastinum, intimately associated with the esophagus and right mainstem bronchus.\nPROCEDURE: Following aspiration of mucinous fluid to facilitate handling, the cyst wall was meticulously dissected from the airway and esophagus using blunt and sharp dissection. Complete excision of the cyst wall was achieved without injury to surrounding structures.",
            3: "CPT 32662: VATS excision of mediastinal cyst.\nType: Bronchogenic cyst.\nComplexity: Adherent to esophagus and airway.\nSteps: Aspiration, dissection of wall, removal, chest tube.",
            4: "Procedure: VATS Cyst Excision\n1. 3 ports.\n2. Found cyst middle mediastinum.\n3. Aspirated fluid.\n4. Dissected wall off esophagus/bronchus.\n5. Removed specimen.\n6. Chest tube.",
            5: "George Nakamura 73M with the big cyst in the middle of the chest vats 3 ports stuck to the esophagus and airway carefully peeled it off after draining it got the whole wall out chest tube placed no leaks.",
            6: "VATS Excision of Mediastinal Cyst. 6cm middle mediastinal cyst causing dysphagia. Large cystic lesion identified in middle mediastinum closely abutting the esophagus and right mainstem bronchus. Cyst aspirated clear mucinous fluid. Cyst wall dissected carefully from esophagus and airway using combination of sharp and blunt dissection. Complete excision achieved.",
            7: "[Indication]\nSymptomatic mediastinal cyst (Bronchogenic).\n[Anesthesia]\nGeneral, DLT.\n[Description]\n3-port VATS. Cyst aspirated. Wall dissected from esophagus/bronchus. Complete excision.\n[Plan]\nAdmit.",
            8: "Mr. Nakamura had a large cyst pressing on his esophagus. We performed a VATS procedure to remove it. Once we were inside, we drained the fluid from the cyst to make it smaller, then carefully peeled the cyst wall off of the esophagus and the main airway. We got the whole thing out without damaging any organs.",
            9: "Diagnosis: Middle mediastinal fluid-filled lesion.\nAction: Thoracoscopic resection of mediastinal cyst.\nDetails: Lesion drained. Capsule separated from adjacent airway and esophagus. Complete removal. Drainage tube inserted."
        },
        8: { # Sandra Kowalski - 32662
            1: "Indication: Ant. Mediastinal Mass (Lymphoma).\nProc: VATS excision.\n- 3 ports.\n- 5.5cm lobulated mass.\n- Dissected from SVC/pericardium.\n- Frozen section: Hodgkin's.\n- Blake drain.",
            2: "OPERATIVE NOTE: Thoracoscopic excision of anterior mediastinal mass.\nFINDINGS: A 5.5 cm heterogeneous, lobulated mass involving thymic tissue in the anterior mediastinum.\nPROCEDURE: The mass was dissected from the pericardium and superior vena cava. Complete excision was achieved. Frozen section analysis revealed classical Hodgkin lymphoma. A Blake drain was placed prior to closure.",
            3: "CPT 32662: VATS excision of mediastinal mass.\nPathology: Hodgkin Lymphoma.\nSize: 5.5cm.\nWork: Dissection from vascular structures (SVC), complete excision, frozen section, drain placement.",
            4: "Procedure: VATS Mass Excision\n1. 3 ports.\n2. Identified anterior mass.\n3. Dissected off SVC/pericardium.\n4. Removed in bag.\n5. Frozen section -> Lymphoma.\n6. Blake drain.",
            5: "Sandra Kowalski with the mediastinal mass suspected lymphoma vats 3 ports found the mass anteriorly 5.5cm stuck to thymus and svc peeled it off sent for frozen came back hodgkins drain in closed up.",
            6: "Thoracoscopy with excision of anterior mediastinal mass. 5.5cm mass in anterior mediastinum with lobulated appearance and involvement of thymic tissue. Mass dissected from surrounding structures including pericardium and superior vena cava with care. Complete excision achieved. Frozen section consistent with classical Hodgkin lymphoma. 24Fr Blake drain placed.",
            7: "[Indication]\nAnterior mediastinal mass (Lymphoma).\n[Anesthesia]\nGeneral, SLV.\n[Description]\n3-port VATS. 5.5cm mass excised from anterior mediastinum. Dissected from SVC. Frozen section confirmed Hodgkin's.\n[Plan]\nAdmit, Oncology consult.",
            8: "Ms. Kowalski underwent a VATS procedure to diagnose and remove a mass in her chest. We found a large mass in the front part of the mediastinum attached to the thymus. We carefully separated it from the heart sac and the large vein draining the head. The pathologist confirmed it was Hodgkin's lymphoma while we were still in the OR. We placed a drain and finished the surgery.",
            9: "Diagnosis: Anterior mediastinal neoplasm (Lymphoma).\nAction: Thoracoscopic resection of mediastinal lesion.\nDetails: Mass isolated and separated from superior vena cava. Extracted via bag. Diagnosis confirmed intraoperatively. Drain placed."
        },
        9: { # Henry Okonkwo - 32662
            1: "Indication: Superior mediastinal lipoma (SVC syndrome).\nProc: VATS excision.\n- 3 ports.\n- 7cm fatty mass.\n- Dissected from SVC.\n- SVC decompressed.\n- Chest tube.",
            2: "OPERATIVE REPORT: Video-assisted thoracoscopic resection of mediastinal lipoma.\nINDICATION: Symptomatic compression of the superior vena cava.\nFINDINGS: A 7 cm encapsulated adipose tumor in the superior mediastinum causing extrinsic compression of the SVC.\nPROCEDURE: Meticulous dissection was performed to separate the tumor from the great vessels. The mass was excised in toto, resulting in immediate visual decompression of the superior vena cava.",
            3: "CPT 32662: VATS excision of mediastinal tumor.\nPathology: Lipoma.\nSize: 7cm.\nComplication treated: SVC compression.\nWork: Dissection from great vessels, removal via bag, chest tube.",
            4: "Procedure: VATS Lipoma Excision\n1. 3 ports.\n2. Found fatty mass compressing SVC.\n3. Dissected off vessels.\n4. Removed in bag.\n5. SVC looks better.\n6. Chest tube.",
            5: "Henry Okonkwo with the lipoma pushing on his svc vats right side found the big fatty tumor 7cm peeled it off the vein vein opened up nicely mass out in a bag chest tube placed.",
            6: "VATS excision of mediastinal tumor. Superior mediastinal lipoma causing SVC compression symptoms. Large fatty tumor identified in superior mediastinum compressing but not invading SVC. Meticulous dissection performed around great vessels. Tumor completely excised in one piece using endoscopic retrieval bag. SVC decompressed with visible improvement in venous caliber.",
            7: "[Indication]\nMediastinal lipoma with SVC compression.\n[Anesthesia]\nGeneral.\n[Description]\n3-port VATS. 7cm mass dissected from SVC. Complete excision. SVC decompressed.\n[Plan]\nAdmit.",
            8: "Mr. Okonkwo had a benign fatty tumor pressing on his superior vena cava, causing swelling. We used VATS to remove it. The tumor was large, about 7cm, and sitting right on the vein. We carefully dissected it away. Once it was removed, we could see the vein expand back to its normal size. We placed a chest tube and closed.",
            9: "Diagnosis: Superior mediastinal adipose tumor.\nAction: Thoracoscopic removal of mediastinal mass.\nDetails: Lesion compressing the superior vena cava was isolated and resected. Vascular decompression confirmed. Drainage tube inserted."
        },
        10: { # Barbara Mitchell - 32606
            1: "Indication: Mediastinal adenopathy.\nProc: Med Thoracoscopy w/ biopsy.\n- Single port.\n- 5th ICS.\n- Biopsied Station 7 (x6) and AP window (x4).\n- 20Fr chest tube.",
            2: "PROCEDURE NOTE: Medical thoracoscopy with mediastinal lymph node biopsy.\nINDICATION: Undiagnosed mediastinal lymphadenopathy.\nTECHNIQUE: Under local anesthesia and moderate sedation, a single port was established. The mediastinal pleura was opened to access the subcarinal (Station 7) and aortopulmonary window stations. Adequate tissue sampling was achieved using rigid forceps. Hemostasis was secured, and a chest tube was placed.",
            3: "CPT 32606: Thoracoscopy with biopsy of mediastinal space/lymph nodes.\nTarget: Station 7 and AP window nodes.\nMethod: Medical thoracoscopy (semi-rigid scope).\nSpecimens: 10 biopsies total.\nPlacement of chest tube included.",
            4: "Procedure: Medical Thoracoscopy\n1. Local/Sedation.\n2. Port 5th ICS.\n3. Opened mediastinal pleura.\n4. Biopsied station 7 and AP window.\n5. Chest tube placed.",
            5: "Barbara Mitchell for mediastinal nodes biopsy medical thoracoscopy single port found the nodes station 7 and ap window took a bunch of biopsies sent for everything chest tube in tolerated well.",
            6: "Medical thoracoscopy with diagnostic biopsy of mediastinal lymph nodes. Single 1cm incision made in 5th intercostal space mid-axillary line. Trocar inserted and semi-rigid pleuroscope introduced. Enlarged station 7 lymph node and AP window nodes visible. Using blunt dissection mediastinal pleura opened. Multiple biopsies obtained. 20Fr chest tube placed.",
            7: "[Indication]\nMediastinal lymphadenopathy (Sarcoid vs Lymphoma).\n[Anesthesia]\nLocal + Sedation.\n[Description]\nSingle port. Biopsied Station 7 and AP window nodes. 10 samples. 20Fr chest tube.\n[Plan]\nAdmit for observation.",
            8: "Ms. Mitchell needed a biopsy of her lymph nodes. We performed a medical thoracoscopy with sedation. Through a small cut in her side, we used a camera to see the nodes in the center of her chest. We opened the lining covering them and took several samples from two different areas. We left a small tube in her chest to drain air and fluid.",
            9: "Diagnosis: Mediastinal adenopathy.\nAction: Thoracoscopic sampling of mediastinal nodes.\nDetails: Access via single port. Lymphoid tissue at station 7 and AP window harvested. Drain inserted."
        },
        11: { # Charles Freeman - 32606
            1: "Indication: Bulky adenopathy.\nProc: Thoracoscopy w/ biopsy.\n- Single port 6th ICS.\n- Flex-rigid scope.\n- Biopsied 4R and 7 (5x each).\n- 14Fr pigtail.",
            2: "PROCEDURE: Thoracoscopic biopsy of mediastinal lymph nodes.\nFINDINGS: Bulky adenopathy in the right paratracheal (4R) and subcarinal (7) stations.\nDETAILS: Following access via the 6th intercostal space, the mediastinal pleura was incised. Insulated-tip forceps were used to obtain deep tissue biopsies from both stations to rule out lymphoma and sarcoidosis. A 14Fr pigtail catheter was placed for drainage.",
            3: "CPT 32606: Thoracoscopy with biopsy of mediastinal space.\nNodes: 4R and 7.\nTechnique: Single port, flex-rigid scope.\nSpecimens: 10 cores.\nChest tube: 14Fr pigtail.",
            4: "Procedure: Thoracoscopy Biopsy\n1. Moderate sedation.\n2. Port 6th ICS.\n3. Biopsied 4R and 7.\n4. Cautery for hemostasis.\n5. Pigtail placed.",
            5: "Charles Freeman needing biopsy for lymph nodes single port thoracoscopy right side found 4r and 7 nodes huge took good biopsies with the hot forceps pigtail in no pneumo.",
            6: "Thoracoscopy with mediastinal lymph node biopsy. Single-incision thoracoscopy at 6th ICS MAL. Flex-rigid scope inserted. Mediastinal pleura over station 4R and 7 opened. Multiple deep biopsies obtained using insulated-tip forceps. Station 4R 5 specimens. Station 7 5 specimens. Hemostasis with electrocautery. 14Fr pigtail catheter placed.",
            7: "[Indication]\nBulky mediastinal adenopathy.\n[Anesthesia]\nModerate Sedation.\n[Description]\nSingle port thoracoscopy. Biopsies of 4R and 7. Pigtail catheter placed.\n[Plan]\nObs overnight.",
            8: "Mr. Freeman underwent a thoracoscopy to biopsy enlarged lymph nodes in his chest. We used a flexible scope through a single incision. We identified large nodes near his windpipe and under the airway split. We took multiple samples from both areas to ensure a good diagnosis. A small pigtail tube was left in place.",
            9: "Diagnosis: Mediastinal lymph node enlargement.\nAction: Thoracoscopic tissue sampling.\nDetails: Access established. Nodes at 4R and 7 harvested. 14Fr catheter inserted."
        },
        12: { # Maria Santos - 32606
            1: "Indication: Ant. Mediastinal Mass.\nProc: Thoracoscopic biopsy.\n- Single port 4th ICS.\n- 5mm scope.\n- 3.5cm mass.\n- 8 biopsies taken.\n- 14Fr chest tube.",
            2: "OPERATIVE REPORT: Diagnostic thoracoscopy with biopsy of anterior mediastinal mass.\nINDICATION: 3.5 cm anterior mediastinal lesion suggestive of thymoma.\nPROCEDURE: General anesthesia was utilized. A single port was placed in the 4th intercostal space. The mediastinal pleura was incised, and multiple biopsies were taken from the encapsulated mass. Frozen section analysis suggested thymic tissue. A 14Fr chest tube was placed.",
            3: "CPT 32606: Thoracoscopy with biopsy of mediastinal mass.\nLocation: Anterior mediastinum.\nMethod: Single port VATS.\nPathology: Suspected thymoma.\nChest tube: 14Fr.",
            4: "Procedure: VATS Biopsy\n1. GA / LMA.\n2. Port 4th ICS.\n3. Biopsied anterior mass x8.\n4. Frozen section: Thymic tissue.\n5. Chest tube placed.",
            5: "Maria Santos with the anterior mediastinal mass for biopsy vats single port 4th ics found the mass took 8 bites frozen said thymoma maybe chest tube in patient extubated fine.",
            6: "Thoracoscopy with diagnostic biopsy of mediastinal lesion. Patient underwent general anesthesia. Left chest entered via single 2cm incision at 4th ICS anterior axillary line. Anterior mediastinal mass visible through mediastinal pleura approximately 3.5cm encapsulated appearance. Mediastinal pleura incised. Multiple deep forceps biopsies x8 obtained. Frozen section Thymic tissue with features suggestive of thymoma. Small 14Fr chest tube placed.",
            7: "[Indication]\nAnterior mediastinal mass.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nSingle port. Biopsied mass x8. Frozen section: Thymic tissue. 14Fr chest tube.\n[Plan]\nAdmit.",
            8: "Ms. Santos has a mass in the front of her chest that might be a thymoma. We performed a thoracoscopy under general anesthesia to biopsy it. Through a small incision, we took eight samples of the mass. The preliminary results point to a thymus tumor. We left a small chest tube in to help the lung stay expanded.",
            9: "Diagnosis: Anterior mediastinal neoplasm.\nAction: Thoracoscopic biopsy.\nDetails: Lesion sampled multiple times. Frozen section analysis performed. Drainage tube inserted."
        },
        13: { # Robert Jackson - 32606
            1: "Indication: Sarcoidosis suspicion.\nProc: Thoracoscopy w/ biopsy.\n- 5th ICS.\n- Biopsied 4R (x6) and 7 (x4).\n- 16Fr chest tube.",
            2: "PROCEDURE NOTE: Medical thoracoscopy for mediastinal lymph node sampling.\nINDICATION: Evaluation of mediastinal adenopathy for sarcoidosis.\nDESCRIPTION: Under moderate sedation, the pleural space was accessed. The mediastinal pleura was opened to expose stations 4R and 7. Adequate biopsy specimens were obtained from both sites for histological and microbiological analysis. A 16Fr chest tube was placed.",
            3: "CPT 32606: Thoracoscopy with biopsy of mediastinal lymph nodes.\nNodes: 4R and 7.\nIndication: Suspected sarcoidosis.\nSpecimens: Sent for H&E, cultures, polarized light.\nDevice: 16Fr chest tube.",
            4: "Procedure: Thoracoscopy\n1. Sedation.\n2. Port 5th ICS.\n3. Biopsied 4R and 7.\n4. 16Fr tube placed.\nNo complications.",
            5: "Robert Jackson sarcoid workup medical thoracoscopy right side 5th ics normal pleura biopsied 4r and 7 good cores sent for cultures too 16fr tube in done.",
            6: "Thoracoscopy with mediastinal node sampling. Moderate sedation. Right lateral decubitus. Standard thoracoscopic entry 5th ICS. Normal pleural surfaces. Mediastinal pleura over paratracheal region opened. Large 2.5cm node identified at station 4R. Multiple punch biopsies x6 obtained. Additional sampling from subcarinal region station 7 x4 biopsies. 16Fr chest tube placed.",
            7: "[Indication]\nSuspected Sarcoidosis.\n[Anesthesia]\nModerate Sedation.\n[Description]\nThoracoscopy. Biopsied 4R and 7. 16Fr tube placed.\n[Plan]\nObs.",
            8: "Mr. Jackson needed tissue confirmation for suspected sarcoidosis. We performed a thoracoscopy with sedation. We found enlarged lymph nodes in the chest and took several samples from two different locations. These will be tested for sarcoidosis and infections. A chest tube was placed at the end.",
            9: "Diagnosis: Mediastinal adenopathy (Sarcoidosis).\nAction: Thoracoscopic nodal sampling.\nDetails: Nodes at 4R and 7 harvested. Drain inserted."
        },
        14: { # Angela Torres - 32606
            1: "Indication: Mediastinal adenopathy.\nProc: VATS biopsy.\n- 3 ports.\n- Biopsied 4R (x8) and 7 (x6).\n- 24Fr chest tube.",
            2: "OPERATIVE NOTE: Video-assisted thoracoscopic biopsy of mediastinal lymph nodes.\nINDICATION: Extensive mediastinal adenopathy, previous non-diagnostic biopsy.\nPROCEDURE: A three-port VATS approach was used. Large confluent nodes were identified in the paratracheal and subcarinal regions. Generous biopsies were taken from stations 4R and 7 for extensive pathological workup including flow cytometry. A 24Fr chest tube was placed.",
            3: "CPT 32606: VATS biopsy of mediastinal lymph nodes.\nNodes: 4R and 7.\nSpecimens: 14 total biopsies.\nWork: 3-port access, dissection, biopsy, chest tube.\nIndication: Lymphadenopathy.",
            4: "Procedure: VATS Biopsy\n1. GA / ETT.\n2. 3 ports.\n3. Biopsied 4R and 7.\n4. Sent fresh for lymphoma workup.\n5. 24Fr chest tube.",
            5: "Angela Torres for mediastinal biopsy vats 3 ports huge nodes 4r and 7 took tons of biopsies sent for flow and molecular tube in 24fr no issues.",
            6: "Thoracoscopy with mediastinal biopsy. General anesthesia induced. Right thoracoscopy via three-port technique. Large confluent nodal mass in the right paratracheal region. Subcarinal adenopathy. Station 4R 8 large biopsies. Station 7 6 biopsies. Specimens sent fresh to pathology. 24Fr chest tube placed.",
            7: "[Indication]\nMediastinal adenopathy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\n3-port VATS. Biopsies of 4R and 7. 24Fr tube.\n[Plan]\nAdmit.",
            8: "Ms. Torres had swollen lymph nodes in her chest that needed a diagnosis. We did a 3-port VATS procedure under general anesthesia. We found large lymph node masses and took many samples to make sure the lab has enough for all the tests, including for lymphoma. We left a chest tube in to drain the chest.",
            9: "Diagnosis: Mediastinal lymph node enlargement.\nAction: Thoracoscopic tissue acquisition.\nDetails: Nodal stations 4R and 7 sampled. Drain inserted."
        },
        15: { # William Turner - 32556
            1: "Indication: Large R effusion.\nProc: Thoracentesis w/ catheter.\n- US marked.\n- 14Fr catheter.\n- Drained 1800mL serosanguinous.\n- Catheter left in place.",
            2: "PROCEDURE NOTE: Thoracentesis with insertion of indwelling pleural drainage catheter.\nINDICATION: Symptomatic pleural effusion, suspected malignancy.\nDESCRIPTION: Following ultrasound marking, a 14Fr pleural catheter was inserted using the Seldinger technique. A total of 1800 mL of serosanguinous fluid was drained, providing immediate symptomatic relief. The catheter was secured for ongoing drainage.",
            3: "CPT 32556: Pleural drainage with insertion of indwelling catheter.\nGuidance: Ultrasound (marking only).\nOutput: 1800mL.\nCatheter: 14Fr.",
            4: "Procedure: Catheter Drainage\n1. US mark.\n2. Local.\n3. 14Fr catheter placed.\n4. Drained 1800mL.\n5. Secured.",
            5: "William Turner with the big right effusion put in a 14fr catheter today marked with us drained 1.8 liters fluid looks serosanguinous patient breathing better now catheter stayed in.",
            6: "Thoracentesis with insertion of indwelling pleural drainage catheter. 64M former smoker with new right-sided pleural effusion. Using Seldinger technique 14Fr pleural drainage catheter inserted. Total drainage 1800mL serosanguinous fluid over 30 minutes. Patient reported immediate relief of dyspnea. Plan admit for drainage monitoring.",
            7: "[Indication]\nSymptomatic R pleural effusion.\n[Anesthesia]\nLocal.\n[Description]\n14Fr catheter placed (US marked). Drained 1800mL.\n[Plan]\nAdmit.",
            8: "Mr. Turner had a large amount of fluid around his right lung causing shortness of breath. We used ultrasound to find the best spot, then inserted a small tube (catheter) to drain it. We removed 1800mL of fluid, which helped his breathing right away. We left the tube in to continue draining.",
            9: "Diagnosis: Pleural effusion.\nAction: Insertion of pleural drainage catheter.\nDetails: 14Fr catheter placed. 1800mL drained. Catheter secured."
        },
        16: { # Dorothy Williams - 32556
            1: "Indication: Recurrent L effusion (Hepatic hydrothorax).\nProc: Thoracentesis w/ catheter.\n- 12Fr pigtail.\n- No imaging.\n- Drained 2100mL clear yellow.\n- Catheter removed.",
            2: "PROCEDURE NOTE: Large volume thoracentesis via catheter.\nINDICATION: Recurrent hepatic hydrothorax causing dyspnea.\nDETAILS: Without imaging guidance, a 12Fr pigtail catheter was introduced into the left pleural space. Approximately 2.1 liters of transudative fluid were evacuated. The procedure was terminated due to patient cough, and the catheter was removed.",
            3: "CPT 32556: Pleural drainage via indwelling catheter.\nNote: Catheter removed at end of case (still 32556 per CPT definition if catheter used for drainage).\nVolume: 2100mL.\nGuidance: None.",
            4: "Procedure: Thoracentesis\n1. Landmark guidance.\n2. 12Fr pigtail inserted.\n3. Drained 2100mL.\n4. Pulled catheter.\nBreathing improved.",
            5: "Dorothy Williams recurrent hydrothorax drained it again today put in a 12fr pigtail got out 2.1 liters she started coughing so we stopped pulled the tube fluid clear.",
            6: "Thoracentesis with catheter aspiration. 78F with CHF and cirrhosis presenting with recurrent left pleural effusion. Using Seldinger technique without imaging guidance 12Fr pigtail catheter inserted into pleural space. Total of 2100mL drained over 45 minutes. Catheter removed. Post-procedure SpO2 96% on RA.",
            7: "[Indication]\nRecurrent L hepatic hydrothorax.\n[Anesthesia]\nLocal.\n[Description]\n12Fr pigtail placed. Drained 2100mL. Removed.\n[Plan]\nDischarge.",
            8: "Ms. Williams has recurrent fluid buildup due to her liver condition. She needed another drainage today. We inserted a small pigtail catheter into her left chest and drained over 2 liters of fluid. We removed the catheter right after the procedure. She felt much better afterward.",
            9: "Diagnosis: Hepatic hydrothorax.\nAction: Catheter drainage of pleural fluid.\nDetails: 12Fr catheter inserted. 2100mL evacuated. Catheter removed."
        },
        17: { # James Morrison - 32556
            1: "Indication: Complicated parapneumonic effusion.\nProc: Catheter drainage.\n- 14Fr pigtail.\n- No imaging.\n- Drained 900mL turbid.\n- Connected to water seal.",
            2: "PROCEDURE: Placement of pleural drainage catheter.\nINDICATION: Complicated parapneumonic effusion/empyema.\nDESCRIPTION: A 14Fr pigtail catheter was inserted into the right pleural space using the Seldinger technique without imaging guidance. Purulent fluid was encountered, and 900 mL was drained. The catheter was secured and attached to a water seal system for continuous drainage.",
            3: "CPT 32556: Pleural drainage with catheter insertion.\nType: 14Fr Pigtail.\nGuidance: None.\nOutput: 900mL purulent.\nPlan: Continuous drainage.",
            4: "Procedure: Pigtail Placement\n1. Landmark.\n2. 14Fr pigtail in.\n3. Drained 900mL turbid fluid.\n4. Sutured in place.\n5. Water seal.",
            5: "James Morrison with the empyema put in a pigtail 14fr right side landmark guided drained 900cc pus hooked it up to atrium for drainage.",
            6: "Thoracentesis with catheter drainage. Right parapneumonic effusion. Without imaging guidance 14Fr pigtail catheter placed using Seldinger technique. Immediate return of turbid yellow-green fluid. 900mL drained during procedure. Catheter sutured and connected to underwater seal drainage.",
            7: "[Indication]\nComplicated parapneumonic effusion.\n[Anesthesia]\nLocal.\n[Description]\n14Fr pigtail inserted. 900mL drained. Secured to water seal.\n[Plan]\nAdmit.",
            8: "Mr. Morrison has an infected fluid collection around his lung. We placed a pigtail catheter to drain it continuously. We drained 900mL of cloudy fluid initially and hooked the tube up to a drainage system to keep the lung clear.",
            9: "Diagnosis: Complicated pleural effusion.\nAction: Insertion of pleural drain.\nDetails: 14Fr catheter placed. 900mL turbid output. Connected to drainage system."
        },
        18: { # Catherine Brown - 32556
            1: "Indication: Malignant effusion (Mesothelioma).\nProc: Catheter aspiration.\n- 12Fr catheter.\n- Landmark guidance.\n- Drained 1500mL bloody.\n- Catheter removed.",
            2: "PROCEDURE NOTE: Therapeutic thoracentesis via catheter.\nINDICATION: Symptomatic malignant pleural effusion.\nDETAILS: A 12Fr drainage catheter was introduced into the left pleural space using anatomical landmarks. Approximately 1.5 liters of serosanguinous fluid were drained, resulting in symptomatic relief. The catheter was removed at the conclusion of the procedure.",
            3: "CPT 32556: Pleural drainage w/ catheter.\nVolume: 1500mL.\nGuidance: None.\nIndication: Malignant effusion.\nStatus: Catheter removed.",
            4: "Procedure: Thoracentesis\n1. Landmark.\n2. 12Fr catheter.\n3. Drained 1500mL bloody fluid.\n4. Catheter out.\nPatient feels better.",
            5: "Catherine Brown mesothelioma patient large effusion drained 1.5L today using a 12fr kit catheter fluid bloody patient coughed so we stopped pulled line.",
            6: "Thoracentesis with catheter aspiration. Large left-sided malignant pleural effusion mesothelioma. With patient sitting at bedside left posterolateral chest prepped. Using Seldinger technique 12Fr drainage catheter placed. Bloody fluid immediately returned. 1500mL serosanguinous fluid removed over 40 minutes. Catheter removed at completion of procedure.",
            7: "[Indication]\nMalignant pleural effusion.\n[Anesthesia]\nLocal.\n[Description]\n12Fr catheter. Drained 1500mL. Removed.\n[Plan]\nDischarge.",
            8: "Ms. Brown has mesothelioma and a large fluid buildup. We drained it today using a temporary catheter. We removed 1.5 liters of bloody fluid, which helped her breathing a lot. We took the catheter out once we were done.",
            9: "Diagnosis: Malignant pleural effusion.\nAction: Catheter drainage.\nDetails: 12Fr catheter used. 1500mL drained. Catheter removed."
        },
        19: { # Richard Hernandez - 32556
            1: "Indication: Post-CABG effusion.\nProc: Catheter insertion.\n- 14Fr pigtail.\n- Landmark guidance.\n- Drained 2350mL serous.\n- Manometry: Normal elastance.\n- Left to bulb suction.",
            2: "PROCEDURE: Insertion of pleural drainage catheter with manometry.\nINDICATION: Large symptomatic effusion post-CABG.\nDESCRIPTION: A 14Fr pigtail catheter was inserted into the right pleural space without imaging. Manometry was performed, showing normal pleural elastance. A total of 2350 mL of serous fluid was drained. The catheter was left in place and connected to a bulb drain.",
            3: "CPT 32556: Pleural drainage w/ catheter.\nAdd-on: Manometry performed.\nOutput: 2350mL.\nDevice: 14Fr pigtail connected to bulb.\nGuidance: None.",
            4: "Procedure: Pigtail + Manometry\n1. Landmark.\n2. 14Fr pigtail.\n3. Manometry checked (normal).\n4. Drained 2350mL.\n5. Bulb suction.",
            5: "Richard Hernandez post cabg effusion drained it with a pigtail 14fr checked pressures lung expanded fine got out over 2 liters 2350 total left it to bulb suction.",
            6: "Thoracentesis with catheter insertion. Post-cardiac surgery pleural effusion right. Without ultrasound 14Fr pigtail catheter inserted using standard technique. Serous yellow fluid encountered. Total 2350mL drained over 50 minutes with serial manometry demonstrating pleural elastance 12 cm H2O/L. Catheter left in place attached to bulb suction.",
            7: "[Indication]\nPost-CABG effusion.\n[Anesthesia]\nLocal.\n[Description]\n14Fr pigtail. Manometry normal. Drained 2350mL. Bulb suction.\n[Plan]\nReassess tomorrow.",
            8: "Mr. Hernandez had a large fluid collection after his heart surgery. We placed a pigtail catheter to drain it. We checked the pressures in his chest while draining, which showed his lung was expanding well. We drained over 2 liters of fluid and left the tube in with a suction bulb to get the rest out.",
            9: "Diagnosis: Post-surgical pleural effusion.\nAction: Insertion of pleural catheter with manometry.\nDetails: 14Fr catheter placed. 2350mL drained. Elastance normal. Bulb suction applied."
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
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: No variation found for note {idx}, style {style_num}")
            
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
    output_filename = output_dir / "synthetic_blvr_notes_part_094.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()