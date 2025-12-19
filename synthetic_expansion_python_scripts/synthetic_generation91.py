import json
import random
import datetime
import copy
from pathlib import Path

# Source file configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_091.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILE = "synthetic_notes_part_091.json"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Provides mock names for name replacement. 
    Keys correspond to note_ids from the source file.
    """
    return {
        "TA-001": {"orig_name": "Robert Martinez", "orig_age": 72, "names": ["James Sterling", "Arthur Dent", "Walter White", "Henry Higgins", "Thomas Anderson", "Bruce Wayne", "Clark Kent", "Peter Parker", "Tony Stark"]},
        "TA-002": {"orig_name": "Susan Chen", "orig_age": 57, "names": ["Diana Prince", "Natasha Romanoff", "Carol Danvers", "Wanda Maximoff", "Jean Grey", "Ororo Munroe", "Jennifer Walters", "Jessica Jones", "Kamala Khan"]},
        "TA-003": {"orig_name": "James O'Brien", "orig_age": 74, "names": ["Steve Rogers", "Bucky Barnes", "Sam Wilson", "Clint Barton", "Scott Lang", "Stephen Strange", "T'Challa", "Vision", "Nick Fury"]},
        "WLL-001": {"orig_name": "Maria Gonzalez", "orig_age": 47, "names": ["Pepper Potts", "Peggy Carter", "Jane Foster", "Darcy Lewis", "Monica Rambeau", "Sylvie Laufeydottir", "Yelena Belova", "Kate Bishop", "Maya Lopez"]},
        "WLL-002": {"orig_name": "Thomas Wilson", "orig_age": 60, "names": ["Happy Hogan", "Phil Coulson", "Wong", "Ned Leeds", "Flash Thompson", "Baron Zemo", "Erik Killmonger", "Thanos", "Loki"]},
        "WLL-003": {"orig_name": "Jennifer Adams", "orig_age": 43, "names": ["Gamora", "Nebula", "Mantis", "Valkyrie", "Sif", "Frigga", "Hela", "Ancient One", "Maria Hill"]},
        "TC-001": {"orig_name": "Robert Anderson", "orig_age": 67, "names": ["Hank Pym", "Odin", "Ego", "Grandmaster", "Collector", "Red Skull", "Ultron", "Vision", "Rocket"]},
        "TC-002": {"orig_name": "Linda Martinez", "orig_age": 55, "names": ["May Parker", "Hope Van Dyne", "Janet Van Dyne", "Ramonda", "Shuri", "Okoye", "Nakia", "Ayo", "Proxima Midnight"]},
        "TC-003": {"orig_name": "David Kim", "orig_age": 73, "names": ["Drax", "Groot", "Star-Lord", "Yondu", "Kraglin", "Stakar Ogord", "Taserface", "Ronan", "Korath"]},
        "FB-001": {"orig_name": "Tommy Rodriguez", "orig_age": 4, "names": ["Billy Maximoff", "Tommy Maximoff", "Franklin Richards", "Miles Morales", "Amadeus Cho", "Kid Loki", "Baby Groot", "Morgan Stark", "Cassie Lang"]},
        "FB-002": {"orig_name": "Harold Thompson", "orig_age": 76, "names": ["Stan Lee", "Jack Kirby", "Steve Ditko", "Joe Simon", "Jim Steranko", "John Romita", "Chris Claremont", "Frank Miller", "Alan Moore"]},
        "FB-003": {"orig_name": "Margaret O'Connor", "orig_age": 67, "names": ["Gwen Stacy", "Mary Jane Watson", "Felicia Hardy", "Elektra Natchios", "Karen Page", "Foggy Nelson", "Ben Urich", "Stick", "Claire Temple"]}
    }

def get_variations():
    """
    Returns a dictionary of text variations keyed by note_id.
    Inner keys 1-9 correspond to the requested styles.
    """
    return {
        "TA-001": {
            1: "Pre-op: RLL SCC, 2.4cm. 8.0 ETT. Navigated to RB6. EBUS confirmed. CBCT verified margins. Microwave ablation: 100W for 10 min. Temp 180C. 3.2cm zone. No bleed. Extubated.",
            2: "HISTORY: The patient, a 72-year-old gentleman with significant COPD, presented for ablative therapy of a biopsy-proven RLL squamous cell carcinoma. \nPROCEDURE: Following the administration of general anesthesia, electromagnetic navigation was employed to localize the target in the superior segment. Radial EBUS confirmation was obtained. A microwave ablation catheter was advanced, and thermal energy was delivered at 100 Watts for a duration of 10 minutes. Post-ablation imaging confirmed a satisfactory ablation zone encompassing the lesion with appropriate margins.",
            3: "CPT 31641 (Destruction of tumor): Microwave ablation performed on RLL tumor.\nCPT 31627 (Navigational Bronchoscopy): Electromagnetic guidance used to reach peripheral target RB6.\nCPT 31654 (REBUS): Radial EBUS probe used to confirm lesion centricity.\nProcedure: 100W x 10min ablation performed with Neuwave system. CBCT confirmed placement.",
            4: "Procedure: Bronchoscopy with Ablation\nAttending: Dr. Walsh\nSteps:\n1. Time out.\n2. Induction/ETT.\n3. Scope inserted. Airways clear.\n4. Navigation to RLL RB6.\n5. Radial EBUS check.\n6. Microwave probe placed.\n7. Ablation: 100W, 10 min.\n8. Extubated stable.\nPlan: Admit, CXR.",
            5: "We did the ablation today on Mr. Martinez for his RLL cancer. Used the navigation system to get out there and checked it with the ultrasound probe. Put the microwave needle in and cooked it at 100 watts for ten minutes. Looked good on the scan after. No bleeding really. He woke up fine sending him to the floor check a xray later thanks.",
            6: "72-year-old male with RLL squamous cell carcinoma. General anesthesia. ETT placed. Flexible bronchoscopy performed. Electromagnetic navigation to RLL superior segment. Radial EBUS confirmation. Microwave ablation performed: 100W, 10 minutes, 180C. Ablation zone 3.2cm. No complications. Extubated and transferred to recovery.",
            7: "[Indication]\nRLL Squamous Cell Carcinoma, nonsurgical candidate.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nNavigated to RB6. EBUS confirmation. Microwave ablation 100W for 10m. Zone 3.2cm verified.\n[Plan]\nAdmit, CT in 1 month.",
            8: "The patient was brought to the bronchoscopy suite for treatment of his right lower lobe cancer. After being put to sleep, we navigated a bronchoscope to the tumor in the superior segment. We double-checked the position with ultrasound and a CT spin. Once we were sure, we inserted the microwave probe and treated the area with high heat for ten minutes. The final scan showed we covered the tumor well. The patient woke up without issues.",
            9: "Procedure: Bronchoscopic thermal destruction of pulmonary neoplasm.\nTarget: RLL peripheral nodule.\nMethod: Electromagnetic guidance utilized to localize zone. Radial ultrasound verified positioning. Microwave energy deployed to coagulate tissue (100W, 600 seconds). Post-destruction imaging validated treatment margins. Airway integrity maintained."
        },
        "TA-002": {
            1: "Dx: RML Carcinoid. 70% obstruction. Rigid scope. Electrocautery to base. Forceps debulking. 40W coag. 10% residual. Bleeding controlled. No stent needed.",
            2: "INDICATION: Recurrent endobronchial carcinoid tumor causing significant RML obstruction.\nOPERATIVE REPORT: Rigid bronchoscopy was initiated under general anesthesia. A polypoid mass was visualized occluding the RML bronchus. Electrocautery ablation was applied to the tumor base for hemostasis and tissue destruction. Mechanical debridement was subsequently performed using rigid forceps. Excellent anatomical restoration was achieved with widely patent airways.",
            3: "Code 31641 (Destruction of tumor): Electrocautery used to ablate tumor base.\nNote: Mechanical debulking also performed at same site (bundled). \nDetails: 40W coagulation current applied. Tumor excised piecemeal. Obstruction reduced from 70% to 10%.",
            4: "Procedure: Rigid Bronchoscopy with Laser/Cautery\nPatient: Susan Chen\nSteps:\n1. General anesthesia.\n2. Rigid scope inserted.\n3. RML tumor seen.\n4. Cautery applied.\n5. Tumor removed with forceps.\n6. Hemostasis achieved.\n7. Suctioned airways.\nPlan: Observation.",
            5: "Procedure note for Ms Chen she has that carcinoid in the RML. We used the rigid scope today. Burned the base of it with the electrocautery and then grabbed the pieces with the big forceps. Got most of it out looks like maybe 10 percent left but airway is open now. Minimal bleeding. She did great.",
            6: "Recurrent endobronchial carcinoid tumor RML. Rigid bronchoscopy performed. Electrocautery ablation 40W. Mechanical debulking with forceps. Obstruction reduced from 70% to 10%. Hemostasis achieved. No complications. Extubated.",
            7: "[Indication]\nRecurrent RML carcinoid, symptomatic obstruction.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nTumor cauterized and debulked. Patency improved 70% -> 90%. Hemostasis secured.\n[Plan]\nObserve, CXR, f/u 6 weeks.",
            8: "We performed a rigid bronchoscopy to treat Ms. Chen's airway tumor. Using the rigid scope, we found the tumor blocking the right middle lobe. We used an electric heating tool to burn the tumor and stop any bleeding, then used forceps to pull the tumor out in pieces. By the end, the airway was wide open again. There was very little bleeding, and she woke up safely.",
            9: "Procedure: Rigid airway endoscopy with thermal coagulation and resection.\nPathology: Obstructing RML neoplasm.\nTechnique: Electric cauterization applied to tumor pedicle. Mechanical excision utilized for mass reduction. Airway caliber restored. Hemostasis confirmed."
        },
        "TA-003": {
            1: "Dx: Metastatic RCC, LMS obstruction. Rigid bronch. APC 60W. Coring/Forceps debulking. Balloon dilation 15-18mm. 50mL pus aspirated. Obstruction 90% -> 30%.",
            2: "CLINICAL SUMMARY: Patient with metastatic renal cell carcinoma presenting with critical left mainstem obstruction.\nPROCEDURE: Rigid bronchoscopy was performed via jet ventilation. The LMS was noted to be sub-totally occluded by hemorrhagic tissue. Argon Plasma Coagulation (APC) was utilized for tumor desiccation. Subsequent mechanical coring and forceps extraction yielded significant tumor volume. Balloon angioplasty was performed to address residual stenosis. Copious purulence was evacuated.",
            3: "CPT 31641 (Destruction): APC used for tumor destruction.\nCPT 31645 (Therapeutic Aspiration): 50mL purulent fluid removed.\nNote: Dilation and excision bundled into destruction code for same lesion. \nEquipment: ERBE VIO APC, CRE Balloon.",
            4: "Resident Procedure Note\nPatient: James O'Brien\nProcedure: APC/Debulking LMS.\nSteps:\n1. Rigid scope in.\n2. Saw tumor in LMS.\n3. APC applied for bleeding control.\n4. Debulked with forceps.\n5. Balloon dilated.\n6. Suctioned pus.\n7. Airway open now.\nPlan: ICU monitoring.",
            5: "Dictating procedure on Mr OBrien. He has the kidney cancer in the lung. Left main was blocked bad. We went in with the rigid. Used the argon plasma to burn it then cored it out. Also dilated it with a balloon. Got a lot of pus out too. Airway looks much better now maybe 70 percent open. He is going to stepdown.",
            6: "Metastatic RCC to Left Mainstem. 90% obstruction. Rigid bronchoscopy. APC ablation (60W). Mechanical debulking. Balloon dilation (15-18mm). Therapeutic aspiration of 50mL purulence. Obstruction reduced to 30%. Hemostasis adequate. Admitted to stepdown.",
            7: "[Indication]\nMetastatic RCC, airway obstruction, dyspnea.\n[Anesthesia]\nGeneral, Rigid Bronch + Jet Vent.\n[Description]\nLMS 90% blocked. APC + mechanical removal. Balloon dilation. Pus drained. Lumen now 70% patent.\n[Plan]\nStepdown, Repeat bronch 4-6 wks.",
            8: "Mr. O'Brien needed urgent clearance of his left main airway due to a tumor. We used a rigid tube to access the airway while he was asleep. We used argon plasma to stop the bleeding and shrink the tumor, then mechanically removed large pieces of it. We also used a balloon to stretch the airway open and suctioned out a lot of infected fluid. He is breathing much better now.",
            9: "Procedure: Rigid endoscopy with plasma coagulation and luminal recanalization.\nTarget: Left mainstem metastatic lesion.\nAction: Thermal devitalization via APC. Mechanical resection of tissue. Pneumatic dilation of stenosis. Evacuation of purulent secretions. Airway caliber significantly improved."
        },
        "WLL-001": {
            1: "Dx: PAP (Autoimmune). Left lung WLL. 37Fr DLT. 18.5L in, 17.2L out. 18 cycles. Clear effluent at end. Extubated to ETT. ICU.",
            2: "PROCEDURE: Unilateral Whole Lung Lavage (Left).\nINDICATION: Pulmonary Alveolar Proteinosis.\nDETAILS: Following general anesthesia and isolation of the left lung via double-lumen endotracheal intubation, serial lavages were performed using warmed saline. A total of 18.5 liters was instilled with a 93% recovery rate. The effluent transitioned from opaque/milky to clear. The patient tolerated single-lung ventilation without hemodynamic compromise.",
            3: "CPT 32999 (Unlisted lung procedure): Left Whole Lung Lavage.\nCPT 31624 (Bronchoscopy): For DLT placement/check.\nVolume: 18.5 Liters.\nTime: 5.5 hours.\nComplexity: High, requires single lung ventilation and large volume fluid management.",
            4: "Procedure: Left Whole Lung Lavage\nSteps:\n1. DLT placed/checked with scope.\n2. Left lung isolated.\n3. Warmed saline instilled 1L at a time.\n4. ChestPT performed.\n5. Fluid drained.\n6. Repeated x18 cycles.\n7. Fluid clear at end.\n8. Tube exchanged to single lumen.",
            5: "We did the lavage on Ms Gonzalez today left side. Took a long time about 5 hours. Put in almost 19 liters of saline and got most of it back. It was really milky at first but cleared up nice. She desatted once but we fixed it. Switched her tube at the end shes going to the ICU intubated.",
            6: "Pulmonary Alveolar Proteinosis. Left lung lavage. General anesthesia. 37Fr DLT. 18.5L saline instilled. 17.2L returned. 18 cycles. Effluent cleared. Transient desaturation treated. DLT exchanged for ETT. Transferred to ICU.",
            7: "[Indication]\nAutoimmune PAP, dyspnea.\n[Anesthesia]\nGA, Left 37Fr DLT.\n[Description]\nLeft lung lavage x18 cycles. 18.5L total. Clear return. Tube exchanged.\n[Plan]\nICU, wean vent, Right lung in 2-4 wks.",
            8: "We performed a whole lung washing on Ms. Gonzalez's left lung to treat her PAP. After placing a special breathing tube to separate the lungs, we washed the left lung with warm salt water 18 times. We put in over 18 liters and got almost all of it back. The fluid started out looking like milk and ended up clear. She is currently stable in the ICU.",
            9: "Procedure: Large volume pulmonary irrigation (Left).\nDiagnosis: Alveolar proteinosis.\nTechnique: Lung isolation via double-lumen catheter. Sequential instillation and drainage of saline aliquots. Proteinaceous material successfully evacuated. Effluent clarity achieved."
        },
        "WLL-002": {
            1: "Dx: Silicosis/PAP. Right WLL. 39Fr DLT. 22L in, 20.3L out. 20 cycles. Thick tan return -> clear. Bronchospasm treated. Extubated.",
            2: "INDICATION: Secondary PAP due to silicosis.\nPROCEDURE: Right Whole Lung Lavage.\nNARRATIVE: General anesthesia was induced and a 39Fr DLT positioned. The right lung was lavaged with 22 liters of warmed saline in 1200mL aliquots. Initial returns were heavily sedimented (silica/protein), progressively clearing by cycle 20. Intraoperative bronchospasm was managed pharmacologically. The patient was successfully extubated in the operating theater.",
            3: "CPT 32999 (Unlisted): Right Whole Lung Lavage.\nDiagnosis: Silicosis with secondary PAP.\nDetails: 22L volume, 5 hours duration. \nComplications: Bronchospasm (managed).\nStatus: Successful therapeutic lavage.",
            4: "Procedure: Right WLL\nPatient: Thomas Wilson\nSteps:\n1. DLT placed.\n2. Right lung lavage initiated.\n3. 20 cycles completed.\n4. Percussion used.\n5. Fluid cleared up.\n6. Extubated in OR.\nNote: Patient had some wheezing, gave albuterol.",
            5: "Procedure note for Mr Wilson doing the right lung wash today. He has that sandblaster lung. Used a big tube cause hes a big guy. Put in 22 liters took forever. The fluid was nasty tan stuff at first but it got clear. He got tight in the middle had to give meds but he did ok. Extubated him at the end.",
            6: "Secondary PAP (Silicosis). Right lung lavage. 22L instilled. 20.3L returned. 20 cycles. Initial effluent tan/thick. Cleared. Bronchospasm managed. Extubated in OR. Stable.",
            7: "[Indication]\nSilicosis/PAP, hypoxemia.\n[Anesthesia]\nGA, 39Fr DLT.\n[Description]\nRight WLL performed. 22L total. Tan effluent cleared. Bronchospasm treated.\n[Plan]\nStep-down, O2 as needed, PFTs 4-6wks.",
            8: "We washed out Mr. Wilson's right lung today. He has a history of breathing in silica dust. We put him to sleep and used a special tube to wash the right lung while he breathed with the left. We used 22 liters of water. The stuff coming out was brown and thick at first but cleared up nicely. He had a little wheezing but is doing fine now.",
            9: "Procedure: Whole lung irrigation (Right).\nEtiology: Occupational pneumoconiosis.\nAction: High-volume saline instillation and gravity drainage. 20 iterations. Sediment and proteinaceous debris removed. Airway reactivity managed. Respiratory status stable."
        },
        "WLL-003": {
            1: "Dx: Severe PAP. Bilateral WLL (Sequential). Left: 20L/20 cycles. Right: 19L/19 cycles. Total 39L. DLT repositioned. ICU intubated.",
            2: "PROCEDURE: Bilateral Sequential Whole Lung Lavage.\nINDICATION: Severe autoimmune PAP with respiratory failure.\nSUMMARY: Given the severity of disease, a bilateral approach was undertaken. The left lung was lavaged first (20L), followed by repositioning of the DLT and lavage of the right lung (19L). Hemodynamic stability was maintained during the intermission. Total volume instilled: 39L. Significant improvement in gas exchange noted post-procedure.",
            3: "CPT 32999-LT: Left Lung Lavage.\nCPT 32999-RT: Right Lung Lavage.\nNote: Sequential procedure in same session due to medical necessity. Total time 9 hours. High complexity anesthesia and fluid management required.",
            4: "Procedure: Bilateral WLL\nSteps:\n1. Left lung lavage first (20 cycles).\n2. Tube moved.\n3. Stabilized patient.\n4. Right lung lavage (19 cycles).\n5. Tube swapped for regular ETT.\n6. To ICU.\nBig case, 9 hours.",
            5: "Huge case today Ms Adams with the bad PAP. We did both lungs same day. Left side first took 20 liters. Then we moved the tube and did the right side another 19 liters. She held up pretty good. Gas bloods looked way better after. Shes in ICU on the vent.",
            6: "Severe Autoimmune PAP. Bilateral sequential WLL. Left lung: 20L instilled, 18.5L return. Right lung: 19L instilled, 17.8L return. DLT repositioned between sides. Total 39L instilled. No complications. Post-proc ABG improved. Transported to ICU intubated.",
            7: "[Indication]\nSevere PAP, respiratory failure.\n[Anesthesia]\nGA, DLT (repositioned).\n[Description]\nLeft WLL (20L) then Right WLL (19L). Total 39L. Milky effluent cleared on both sides.\n[Plan]\nICU, wean vent 24hrs.",
            8: "Because Ms. Adams was so sick with PAP, we decided to wash both lungs today. We started with the left lung, washing it until the fluid ran clear. Then we adjusted the breathing tube and did the same for the right lung. It was a very long day, using 39 liters of fluid total, but her oxygen levels are already much better. She is resting in the ICU.",
            9: "Procedure: Bilateral pulmonary lavage (Sequential).\nIndication: Refractory alveolar proteinosis.\nMethod: Left lung irrigated to clearance. Airway device adjusted. Right lung irrigated to clearance. Cumulative volume 39L. Gas exchange markedly enhanced."
        },
        "TC-001": {
            1: "Dx: Malignant pleural effusion (R). US guidance. 1.5L straw fluid removed. No complications. Samples sent.",
            2: "PROCEDURE: Ultrasound-guided right thoracentesis.\nINDICATION: Symptomatic pleural effusion in setting of Stage IV NSCLC.\nDETAILS: Under sterile conditions and real-time sonographic guidance, the right pleural space was accessed. 1,500 mL of serous fluid was evacuated for symptomatic palliation and diagnostic characterization. Post-procedural imaging ruled out pneumothorax.",
            3: "CPT 32555 (Thoracentesis w/ Imaging).\nGuidance: Real-time Ultrasound.\nVolume: 1500mL.\nDiagnostic & Therapeutic.\nFluid: Exudative characteristics likely.",
            4: "Procedure: Thoracentesis\nSteps:\n1. Consent/Timeout.\n2. US check - big effusion right side.\n3. Prepped and numbed.\n4. Needle in, catheter placed.\n5. Drained 1.5L.\n6. Pulled catheter, bandaged.\nPatient feels better.",
            5: "Did a thoracentesis on Mr Anderson. He has lung cancer and fluid on the right. Used ultrasound to find a good spot. Numbed him up. Got about a liter and a half out. Fluid looked clear yellow. He is breathing easier now. Sent fluid to lab.",
            6: "Right pleural effusion. US guidance. 8th ICS. 1500mL clear straw-colored fluid removed. No pneumothorax. Dyspnea improved. Fluid sent for cytology/culture.",
            7: "[Indication]\nDyspnea, R pleural effusion (Ca lung).\n[Anesthesia]\nLocal lidocaine.\n[Description]\nUS guided tap. 1.5L removed. No complications.\n[Plan]\nAwait cytology, follow up 1 wk.",
            8: "Mr. Anderson has fluid around his right lung causing shortness of breath. We used ultrasound to guide a small tube into the fluid pocket and drained 1.5 liters. The fluid was clear and yellow. He felt much better afterwards. We sent the fluid for testing to see if the cancer is spreading there.",
            9: "Procedure: Ultrasound-facilitated pleural aspiration (Right).\nIndication: Respiratory distress secondary to hydrothorax.\nAction: Percutaneous catheter insertion. Evacuation of 1500mL serous fluid. Symptom alleviation achieved."
        },
        "TC-002": {
            1: "Dx: Cirrhosis, L effusion. Bedside US. 650mL clear fluid. R/O SBP/Hepatic hydrothorax. Stable.",
            2: "PROCEDURE: Diagnostic Left Thoracentesis.\nINDICATION: New effusion in decompensated cirrhosis, rule out infection.\nNARRATIVE: The patient was positioned in lateral decubitus. Using ultrasound localization, the left pleural space was accessed. 650 mL of transudative-appearing fluid was aspirated. Preliminary cell count is not suggestive of empyema or spontaneous bacterial pleuritis equivalent.",
            3: "CPT 32555: Thoracentesis with imaging.\nNote: High risk patient (INR 1.8 corrected with FFP). \nVolume: 650mL.\nPurpose: Diagnostic (infection check).",
            4: "Resident Note: Thoracentesis\nPatient: Linda Martinez\nSteps:\n1. US check - fluid on left.\n2. Patient on side.\n3. Needle in 7th space.\n4. Drained 650cc.\n5. Fluid clear.\nNo complications.",
            5: "Bedside tap on Ms Martinez in the ICU. She has liver failure. Needed to check the fluid for infection. Used ultrasound found a pocket on the left. Got about 650ccs out. Looked like regular fluid not pus. Patient did fine.",
            6: "Left pleural effusion. Decompensated cirrhosis. US guidance. 650mL clear fluid removed. Cell count low (non-infectious). Hemodynamically stable. No pneumothorax.",
            7: "[Indication]\nCirrhosis, L effusion, r/o infection.\n[Anesthesia]\nLocal.\n[Description]\nUS guided L thoracentesis. 650ml removed. Transudate.\n[Plan]\nAwait culture, hepatology consult.",
            8: "We performed a tap on the fluid around Ms. Martinez's left lung. She has liver disease and we needed to make sure the fluid wasn't infected. We used ultrasound to guide the needle and took out 650ml of clear fluid. The initial tests look good, no signs of infection.",
            9: "Procedure: Sonographic pleural sampling (Left).\nContext: Hepatic hydrothorax evaluation.\nAction: Needle aspiration of pleural cavity. 650mL withdrawn. Fluid analysis pending. Patient stable."
        },
        "TC-003": {
            1: "Dx: CHF, Bilateral effusions. Right tap. US guided. 1.8L removed. Transudative (Light's criteria). Dyspnea improved.",
            2: "PROCEDURE: Therapeutic Right Thoracentesis.\nINDICATION: Refractory dyspnea in setting of congestive heart failure.\nDETAILS: Pre-procedure ultrasound confirmed a significant right-sided effusion. A catheter was introduced under sonographic guidance. 1,800 mL of straw-colored fluid was drained. Analysis is consistent with a transudative process secondary to cardiac dysfunction. The patient reported immediate symptom relief.",
            3: "CPT 32555.\nVolume: 1800mL.\nDiagnosis: Pleural effusion (CHF).\nCriteria: Light's criteria satisfied for transudate.\nComplication: Mild chest tightness (resolved with cessation).",
            4: "Procedure: Thoracentesis Right\nSteps:\n1. US verified fluid.\n2. Safe-T-Centesis kit used.\n3. 1.8L drained.\n4. Stopped due to cough/tightness.\n5. CXR shows improvement.\nPatient breathing better.",
            5: "Saw Mr Kim for the fluid on his lungs from the CHF. Did a tap on the right side. Got a lot out almost 2 liters. He started coughing so we stopped. Fluid is clear definitely heart failure fluid. He feels way better.",
            6: "Bilateral effusions (CHF). Right thoracentesis. US guidance. 1800mL clear fluid. Transudate per Light's criteria. Mild chest tightness -> procedure stopped. CXR improved. Dyspnea improved.",
            7: "[Indication]\nCHF, R > L effusion, dyspnea.\n[Anesthesia]\nLocal.\n[Description]\nUS guided R tap. 1.8L removed. Transudate.\n[Plan]\nDiurese, Cardio f/u.",
            8: "Mr. Kim has fluid on his lungs from heart failure. We drained the right side today using ultrasound guidance. We removed 1.8 liters of fluid which made his breathing much easier. We stopped when he felt a little tight, which is normal. The fluid looks like typical heart failure fluid.",
            9: "Procedure: Ultrasound-directed pleural drainage (Right).\nEtiology: Cardiogenic effusion.\nAction: Catheter placement. Withdrawal of 1800mL fluid. Symptom resolution. Biochemistry confirms transudate."
        },
        "FB-001": {
            1: "Dx: Peanut aspiration. 4yo male. Rigid bronch. Forceps/Basket removal. R mainstem. Complete removal. No complications.",
            2: "INDICATION: Foreign body aspiration (organic).\nPROCEDURE: Rigid bronchoscopy with foreign body extraction.\nFINDINGS: A peanut fragment was identified in the right bronchus intermedius. Extraction was performed utilizing optical alligator forceps and a retrieval basket. The airway was cleared of all particulate matter. Post-extraction inspection revealed mild mucosal edema but patent airways.",
            3: "CPT 31635 (Bronchoscopy FB removal).\nTechnique: Rigid bronchoscopy (essential for airway control in pediatric FB).\nTools: Optical forceps, Dormia basket.\nComplexity: Emergency procedure, fragmentation of FB.",
            4: "Procedure: Rigid Bronch FB Removal\nPatient: Tommy Rodriguez\nSteps:\n1. General anesthesia.\n2. Rigid scope in.\n3. Saw peanut in right side.\n4. Grabbed with forceps, broke a bit.\n5. Used basket to get the rest.\n6. All out.\n7. Suctioned.\nPlan: Observe.",
            5: "Emergency case 4 year old swallowed a peanut. Went in with the rigid scope. It was stuck in the right bronchus. Broke apart when I grabbed it so had to use the basket to get all the pieces. Got it all though. Kid is doing fine extubated.",
            6: "Foreign body aspiration (Peanut). Right bronchus intermedius. Rigid bronchoscopy. Forceps and basket retrieval. Fragmented but completely removed. Mucosal edema noted. Dexamethasone given. Extubated.",
            7: "[Indication]\nPeanut aspiration, wheezing.\n[Anesthesia]\nGA, Rigid Bronch.\n[Description]\nPeanut in RBI. Removed via forceps/basket. Airway clear.\n[Plan]\nObs overnight, Decadron.",
            8: "Tommy inhaled a peanut and came to the ER. We took him to the OR and used a rigid tube to look in his lungs. We found the peanut in the right airway. It broke into a few pieces but we got them all out using a basket tool. His breathing sounds much better now.",
            9: "Procedure: Rigid endoscopic retrieval of foreign object.\nObject: Organic material (Arachis hypogaea).\nLocation: Right bronchial tree.\nAction: Visualization via rigid endoscope. Mechanical extraction utilizing forceps and basket. Complete clearance verified."
        },
        "FB-002": {
            1: "Dx: Trach brush aspiration. Flex bronch via trach. Cryoprobe removal from RML. 100% removed. Minor bleeding.",
            2: "INDICATION: Aspiration of tracheostomy cleaning implement.\nPROCEDURE: Flexible bronchoscopy via tracheostomy stoma.\nDETAILS: Inspection revealed a plastic bristle cluster impacted in the RML bronchus. A cryoprobe was utilized to adhere to the foreign body, allowing for en bloc extraction. The RML mucosa was noted to be edematous. No residual foreign material remained.",
            3: "CPT 31635: FB removal via bronchoscopy.\nApproach: Via established tracheostomy (bundled).\nTechnique: Cryoadhesion extraction.\nItem: Plastic brush component.",
            4: "Procedure: FB removal via Trach\nSteps:\n1. Scope through trach.\n2. Found brush tip in RML.\n3. Suctioned pus.\n4. Used cryoprobe to freeze it.\n5. Pulled it out.\n6. Cleaned up blood/pus.\nPlan: Antibiotics.",
            5: "Mr Thompson inhaled his trach brush. We went down the trach with the flex scope. Found the blue bristles in the right middle lobe. Hard to grab so used the cryo probe to freeze onto it. Pulled right out. Some bleeding but stopped. Sent him home.",
            6: "Foreign body (plastic bristles). RML bronchus. Flexible bronchoscopy via tracheostomy. Cryoprobe extraction successful. Mucosal edema/bleeding managed. Antibiotics continued.",
            7: "[Indication]\nAspirated trach brush.\n[Anesthesia]\nMAC, via trach.\n[Description]\nPlastic bristles in RML. Removed w/ cryoprobe. Secretions cleared.\n[Plan]\nOutpatient, finish abx.",
            8: "Mr. Thompson accidentally inhaled part of his cleaning brush. We put a scope through his breathing tube and found the plastic bristles stuck in the right lung. We used a freezing probe to stick to the plastic and pull it out. It worked well and he didn't need surgery.",
            9: "Procedure: Flexible endoscopic extraction via stoma.\nObject: Synthetic bristle cluster.\nLocation: RML orifice.\nAction: Cryo-adhesion technique employed. Object retrieved intact. Secretions evacuated."
        },
        "FB-003": {
            1: "Dx: Dental crown aspiration LLL. Rigid bronch. Snare removal (forceps failed). Balloon dilation of stenosis. Antibiotics for pneumonia.",
            2: "INDICATION: Aspiration of dental prosthesis.\nPROCEDURE: Rigid and Flexible Bronchoscopy.\nNARRATIVE: The patient presented with a metallic foreign body in the LLL. Initial attempts with forceps and basket were unsuccessful due to impaction. A snare device was successfully employed to retrieve the dental crown. Post-extraction stenosis of the segmental bronchus was treated with balloon dilation. Purulent secretions were evacuated.",
            3: "CPT 31635: FB removal (Dental crown).\nCPT 31630-59: Balloon dilation of post-obstructive stenosis (distinct service).\nComplexity: Rigid bronch required, multiple tools used, impacted object.",
            4: "Procedure: FB Removal (Crown)\nSteps:\n1. Flex scope -> too much pus/impacted.\n2. Switched to Rigid.\n3. Tried forceps/basket (failed).\n4. Snare worked.\n5. Pulled crown out.\n6. Ballooned the airway (it was swollen).\n7. Cleaned out pus.\nPlan: Admit for IV abx.",
            5: "Tough case Ms OConnor inhaled a gold crown. It was stuck tight in the LLL. Had to use the rigid scope. Tried everything forceps basket cryo nothing worked. Finally lassoed it with a snare and pulled it out. The airway was swollen shut after so we dilated it. She has pneumonia too so admitting her.",
            6: "Dental crown aspiration LLL. Impacted. Rigid bronchoscopy. Snare extraction successful after forceps failure. Post-extraction stenosis dilated (8-10mm balloon). Purulent secretions drained. Admitted for aspiration pneumonia.",
            7: "[Indication]\nAspirated crown, LLL pneumonia.\n[Anesthesia]\nGA, Rigid.\n[Description]\nCrown impacted LB10. Snare removal. Balloon dilation of stenosis. Pus drained.\n[Plan]\nAdmit, IV Abx, Speech path.",
            8: "Ms. O'Connor inhaled a dental crown. It was wedged tight in the lower left lung. We had to use a rigid tube and a snare tool to get it out because it was slippery. After we got it out, the airway was swollen, so we used a balloon to open it up. She has an infection from it so she is staying in the hospital.",
            9: "Procedure: Rigid endoscopic foreign body retrieval.\nObject: Odontologic prosthesis.\nLocation: LLL posterior basal segment.\nAction: Snare traction technique. Object dislodged and removed. Pneumatic dilation of reactive stenosis. Airway patency restored."
        }
    }

def main():
    # Load original data
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        return
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Categories to process
    categories = ['thermal_ablation', 'whole_lung_lavage', 'thoracentesis', 'foreign_body_removal']
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Output structure (maintaining the dictionary structure of input)
    output_json = {
        "metadata": {
            "version": "1.0.0",
            "generated_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "description": "Synthetic expansions of IP notes Part 091",
            "source_file": SOURCE_FILE
        }
    }
    
    # Iterate through categories
    for category in categories:
        if category not in source_data:
            continue
            
        output_json[category] = []
        original_notes = source_data[category]
        
        for note in original_notes:
            note_id = note.get('note_id')
            
            # Skip if we don't have mock data for this note
            if note_id not in base_data:
                continue
                
            record = base_data[note_id]
            orig_age = record['orig_age']
            
            # Generate 9 variations
            for style_num in range(1, 10):
                # Deep copy original
                synthetic_note = copy.deepcopy(note)
                
                # 1. Update ID and MRN to be unique
                new_note_id = f"{note_id}_syn_{style_num}"
                synthetic_note['note_id'] = new_note_id
                
                if 'registry_entry' in synthetic_note:
                    reg = synthetic_note['registry_entry']
                    if 'patient_mrn' in reg:
                        reg['patient_mrn'] = f"{reg['patient_mrn']}_syn_{style_num}"
                    
                    # 2. Update Patient Name
                    new_name = record['names'][style_num - 1]
                    # Update in registry
                    if 'patient_demographics' in reg:
                        # Split name for simplicity or just add a 'full_name' field if schema allows, 
                        # but usually registry splits it. Note text has full name.
                        # For this exercise, we assume the registry might not have name fields explicitly 
                        # in the 'patient_demographics' dict in the source example, but we verify:
                        pass 
                    
                    # 3. Update Age (+/- 3 years)
                    new_age = orig_age + random.randint(-3, 3)
                    if 'patient_demographics' in reg:
                        reg['patient_demographics']['age_years'] = new_age
                        
                    # 4. Update Date (Random within 2025)
                    rand_date = generate_random_date(2025, 2025).strftime("%Y-%m-%d")
                    reg['procedure_date'] = rand_date
                    
                    # Update text with the specific variation
                    # We need to inject the NEW NAME into the text if the variation text contains a placeholder or just use the pre-written text.
                    # The pre-written text in get_variations() doesn't have the *new* names hardcoded, it has *specific* text.
                    # However, to be perfectly consistent, the text in get_variations() should theoretically match the name in get_base_data_mocks().
                    # Checking get_variations above... 
                    # TA-001 Style 5 says "Mr. Martinez". Style 8 says "Mr. Martinez".
                    # To do this correctly dynamically, I should replace the original name in the variation text with the new name.
                    
                    variation_text = variations_text[note_id][style_num]
                    
                    # Simple string replacement for the surname if present in the variation text
                    # Original names:
                    # TA-001: Martinez
                    # TA-002: Chen
                    # TA-003: O'Brien
                    # WLL-001: Gonzalez
                    # WLL-002: Wilson
                    # WLL-003: Adams
                    # TC-001: Anderson
                    # TC-002: Martinez
                    # TC-003: Kim
                    # FB-001: Rodriguez
                    # FB-002: Thompson
                    # FB-003: O'Connor
                    
                    orig_surname = record['orig_name'].split()[-1]
                    new_surname = new_name.split()[-1]
                    
                    # Replace surname in text
                    variation_text = variation_text.replace(orig_surname, new_surname)
                    
                    # Also replace full name if present
                    variation_text = variation_text.replace(record['orig_name'], new_name)
                    
                    synthetic_note['note_text'] = variation_text
                    
                    # Add synthetic metadata
                    synthetic_note['synthetic_metadata'] = {
                        "original_note_id": note_id,
                        "style_type": style_num,
                        "generated_name": new_name,
                        "generated_date": rand_date
                    }
                
                output_json[category].append(synthetic_note)

    # Write to file
    output_path = output_dir / OUTPUT_FILE
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_json, f, indent=2)
        
    print(f"Successfully generated synthetic notes in {output_path}")

if __name__ == "__main__":
    main()