import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_005.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    # Defines mock names for the 8 notes found in the source file
    return [
        {"idx": 0, "orig_name": "James Wilson", "orig_age": 45, "names": ["Robert Miller", "William Davis", "Joseph Garcia", "Charles Rodriguez", "Thomas Wilson", "Christopher Martinez", "Daniel Anderson", "Matthew Taylor", "Anthony Thomas"]},
        {"idx": 1, "orig_name": "David Kim", "orig_age": 65, "names": ["James Lee", "John Park", "Robert Kim", "Michael Chen", "William Wong", "David Nguyen", "Richard Tran", "Joseph Liu", "Charles Chang"]},
        {"idx": 2, "orig_name": "Douglas Diaz", "orig_age": 74, "names": ["Richard Perez", "Joseph Sanchez", "Thomas Rivera", "Charles Torres", "Christopher Ramirez", "Daniel Cruz", "Matthew Flores", "Anthony Gomez", "Mark Reyes"]},
        {"idx": 3, "orig_name": "Daniel Cooper", "orig_age": 68, "names": ["William Turner", "Joseph Parker", "Charles Evans", "Thomas Edwards", "Christopher Collins", "Daniel Stewart", "Matthew Sanchez", "Anthony Morris", "Mark Rogers"]},
        {"idx": 4, "orig_name": "Daniel Cooper", "orig_age": 68, "names": ["Robert Reed", "William Cook", "Joseph Morgan", "Charles Bell", "Thomas Murphy", "Christopher Bailey", "Daniel Rivera", "Matthew Cooper", "Anthony Richardson"]},
        {"idx": 5, "orig_name": "Daniel Cooper", "orig_age": 68, "names": ["Donald Ross", "Kenneth Campbell", "George Mitchell", "Steven Roberts", "Edward Carter", "Brian Phillips", "Kevin Evans", "Ronald Turner", "Jason Torres"]},
        {"idx": 6, "orig_name": "Linda Harrison", "orig_age": 66, "names": ["Mary Cox", "Patricia Howard", "Linda Ward", "Barbara Torres", "Elizabeth Peterson", "Jennifer Gray", "Maria Ramirez", "Susan James", "Margaret Watson"]},
        {"idx": 7, "orig_name": "David Johnson", "orig_age": 59, "names": ["James Brooks", "John Kelly", "Robert Sanders", "Michael Price", "William Bennett", "David Wood", "Richard Barnes", "Joseph Ross", "Charles Henderson"]},
        {"idx": 8, "orig_name": "Jennifer Taylor", "orig_age": 65, "names": ["Patricia Coleman", "Linda Jenkins", "Barbara Perry", "Elizabeth Powell", "Jennifer Long", "Maria Patterson", "Susan Hughes", "Margaret Flores", "Dorothy Washington"]}
    ]

def get_variations():
    # Structure: Note_Index (0-8) -> Style_Index (1-9) -> Text
    variations = {
        0: { # James Wilson (Tracheostomy)
            1: "Procedure: Percutaneous Tracheostomy (31600)\n* Airway: 8.0 ETT. Bronchoscope inserted.\n* Landmark: Cricoid visualized. Site: 1st-2nd tracheal ring.\n* Action: Needle insertion -> Air aspiration confirmed -> Guidewire placed.\n* Dilation: 14Fr dilator -> Blue Rhino dilator.\n* Tube: Shiley 8.0 inserted. Cuff inflated.\n* Confirmation: ETCO2 positive. Scope confirms placement 3cm above carina.\n* Outcome: ETT removed. Trach secured. No complications.",
            2: "OPERATIVE SUMMARY: The patient, Mr. Robert Miller, was identified and a time-out was performed. Under general anesthesia with propofol and fentanyl infusions, a bronchoscopic-assisted percutaneous dilatational tracheostomy was undertaken. The bronchoscope was introduced via the existing endotracheal tube, withdrawing to the subglottic space to visualize the anterior tracheal wall. A puncture site was selected between the first and second tracheal rings. Following local anesthetic infiltration, the introducer needle was advanced into the tracheal lumen under direct bronchoscopic visualization. The Seldinger technique was utilized to place a J-wire, followed by serial dilation using a 14 French dilator and the Ciaglia Blue Rhino single-stage dilator. A Shiley 8.0 cuffed tracheostomy tube was smoothly inserted. Placement was confirmed bronchoscopically and via capnography. The device was sutured in place without incident.",
            3: "CPT 31600 Service Description:\nProcedure: Tracheostomy, planned (percutaneous).\nGuidance: Bronchoscopic visualization (included) to ensure midline puncture and avoid posterior wall injury.\nKey Steps:\n1. Identification of cricoid and sternal notch.\n2. Needle entry at 1st/2nd interspace verified by air aspiration.\n3. Guidewire placement and serial dilation (Blue Rhino technique).\n4. Insertion of 8.0 cannula.\nMedical Necessity: Prolonged ventilator dependence (ARDS/COVID-19).\nOutcome: Successful airway establishment.",
            4: "Procedure: Percutaneous Trach\nResident: Dr. Stevens\nAttending: Dr. Taylor\nSteps:\n1. Time out. Neck extended.\n2. Bronch scope down ETT. ETT pulled back.\n3. Poke with needle -> air bubbles seen.\n4. Wire in. Dilated with small dilator then the Rhino.\n5. Trach tube (8.0) put in. Balloon up.\n6. Hooked to vent. Good CO2.\n7. Stitched it in.\nNo issues.",
            5: "op note for mr davis he needed a trach for prolonged vent stuff covid ards. we did the percutaneous one with the blue rhino kit. scope went in dr taylor was watching. i poked the needle in got air put the wire in. dilated it up big then put the shiley 8 in. looked good on the scope after. took the ett out. stitched the trach with nylon. minimal bleeding just a little surgicel needed. patient tolerated it fine thanks.",
            6: "Mr. Joseph Garcia, 45-year-old male. Diagnosis: ARDS, Prolonged intubation. Procedure: Percutaneous Dilatational Tracheostomy. Anesthesia: IV sedation. The neck was prepped. Bronchoscope used to visualize tracheal rings. Needle entered trachea between 1st and 2nd rings. Guidewire advanced. Tract dilated with Blue Rhino dilator. Shiley 8.0 tracheostomy tube inserted under direct vision. Cuff inflated. End-tidal CO2 confirmed ventilation. Tube sutured to skin. Complications: None. EBL: 20ml.",
            7: "[Indication] Prolonged mechanical ventilation secondary to COVID-19 ARDS.\n[Anesthesia] General (Propofol/Fentanyl infusions).\n[Description] Percutaneous tracheostomy performed using Ciaglia Blue Rhino technique. Bronchoscopic guidance confirmed needle entry at 1st-2nd interspace. Tract dilated. Shiley 8.0 tube inserted. Position confirmed 3cm above carina.\n[Plan] Wean sedation. Trach collar trials as tolerated.",
            8: "Mr. Daniel Anderson underwent a planned tracheostomy today due to his inability to be weaned from the ventilator. We positioned him with a shoulder roll and used the bronchoscope to guide the entire procedure. After numbing the neck, we inserted the needle into the trachea, watching from the inside to make sure it was perfectly centered. We then used the dilators to open the path and slid the tracheostomy tube in. Everything went smoothly, and we confirmed the tube was in the right spot before sewing it in place.",
            9: "Operation: Percutaneous tracheostomy with bronchoscopic assistance.\nSubject: Matthew Taylor.\nTechnique: The bronchoscope was navigated through the ETT. The trachea was cannulated between the proximal rings. A guidewire was deployed. The stoma was expanded using the Blue Rhino dilator. An 8.0 Shiley cannula was implanted. Ventilation was verified via capnography. The apparatus was secured."
        },
        1: { # David Kim (Lung Masses)
            1: "Indication: Bilateral lung masses.\nProcedures:\n- RUL Mass: Endobronchial Bx (x6), TBNA (x5). ROSE: Malignant.\n- LLL Lesion: Radial EBUS localization. TBBX (x5), TBNA (x4). ROSE: Necrosis.\n- BAL LLL: Cx sent.\nComplications: Moderate bleeding RUL, stopped w/ epi. No pneumo.\nPlan: Path pending. Outpatient d/c.",
            2: "PROCEDURE NOTE: Mr. James Lee presented for diagnostic bronchoscopy regarding bilateral pulmonary opacities. The airway was secured with an 8.5 ETT. Inspection revealed a fungating endobronchial lesion obstructing the RUL superior segment; this was extensively sampled via forceps biopsy and transbronchial needle aspiration (TBNA), yielding a malignant diagnosis on ROSE. Attention was turned to the LLL, where a peripheral lesion was localized utilizing radial EBUS. Transbronchial biopsies and needle aspirations were obtained. Hemostasis was achieved with topical epinephrine. The patient remained stable.",
            3: "Coding Substantiation:\n1. 31625: Endobronchial biopsy of RUL mass.\n2. 31629: TBNA of RUL mass (distinct technique).\n3. 31628: Transbronchial lung biopsy of LLL lesion (separate lobe).\n4. 31654: Radial EBUS for guidance of LLL biopsy.\n5. 31624: BAL of LLL.\nNote: Distinct lesions in separate lobes support multiple sampling codes. Modifier -59/XS applicable.",
            4: "Procedure: Bronchoscopy w/ Biopsy\nPatient: John Park, 65M\nStaff: Dr. Rodriguez\nSteps:\n1. ETT 8.5. General Anesthesia.\n2. Saw mass in RUL. Biopsied it (forceps + needle). Bleeding controlled.\n3. Went to LLL. Used radial EBUS to find the nodule.\n4. Biopsied LLL (forceps + needle).\n5. Did a BAL in LLL.\n6. ROSE said RUL is cancer. LLL was just necrosis.\nPlan: Wait for final path.",
            5: "Bronch for Robert Kim he has spots on both lungs. Put him to sleep tube in. Right upper lobe had a big ugly mass blocking the airway so we took bites with the forceps and poked it with the needle rose said cancer. Then went to the left lower lobe used the radar probe thing radial ebus found the spot and biopsied that too. Was bleeding a bit in the right side used epi. Woke up fine sending him home.",
            6: "Flexible bronchoscopy, diagnostic. Patient: Michael Chen. Indications: Bilateral lung masses. Findings: RUL endobronchial fungating mass obstructing superior segment. LLL peripheral lesion localized with REBUS. Procedures: RUL endobronchial biopsy and TBNA. LLL transbronchial biopsy and TBNA. LLL BAL. Measurements: 110cc saline instilled, 20cc returned. Complications: Moderate bleeding controlled with epinephrine. Disposition: Stable.",
            7: "[Indication] Bilateral lung masses, suspect malignancy.\n[Anesthesia] General, 8.5 ETT.\n[Description] 1. RUL Mass: Endobronchial. Biopsied (Forceps/TBNA). ROSE+.\n2. LLL Nodule: Peripheral. Navigated with Radial EBUS. Biopsied (TBBX/TBNA).\n3. LLL BAL performed.\n[Plan] Discharge. Follow-up oncology.",
            8: "We performed a bronchoscopy on Mr. David Nguyen today to investigate masses in both his right and left lungs. Upon entering the right upper lobe, we immediately saw a large mass blocking the airway, which we biopsied. The pathologist in the room confirmed it was cancer. We then moved to the left lower lobe and used a special ultrasound probe to find a smaller spot deeper in the lung. We took samples of that as well. He had some bleeding, but we stopped it with medication. He is waking up now.",
            9: "Operation: Fiberoptic bronchoscopy with multisite sampling.\nSubject: Richard Tran.\nFindings: An endobronchial tumor was obstructing the RUL. This was sampled via forceps and needle aspiration. A secondary lesion in the LLL was targeted utilizing radial endobronchial ultrasound. Transbronchial specimens were acquired. Bronchoalveolar lavage was executed in the LLL. Hemostasis was secured."
        },
        2: { # Douglas Diaz (Nav Bronch)
            1: "Indication: RUL Nodule.\nTech: Ion Robotic Bronch + Cone Beam CT.\nAction: Navigated to RUL anterior segment. Target confirmed on CBCT.\nSampling: TBNA x6, Cryobiopsy x5.\nadd-on: Chartis LUL (CV negative).\nResult: ROSE atypical. No pneumothorax.\nPlan: D/C home.",
            2: "PROCEDURE: Robotic-Assisted Navigational Bronchoscopy (Ion Platform).\nPATIENT: Mr. Richard Perez.\nNARRATIVE: Following general anesthesia, the Ion catheter was navigated to a 1.4 cm nodule in the RUL anterior segment. Local alignment was verified via 3D spin (Cone Beam CT). Transbronchial needle aspiration and cryobiopsies were obtained under fluoroscopic and virtual guidance. Subsequently, a Chartis assessment of the LLL was performed to evaluate collateral ventilation for potential future valve therapy; CV was absent. The patient tolerated the procedure well.",
            3: "Billing Record:\n- 31627 (Navigational Bronchoscopy): Ion platform used.\n- 31629 (TBNA): RUL nodule.\n- 31628 (Transbronchial Biopsy): RUL nodule (Cryo).\n- 31634 (Balloon Occlusion): LLL Chartis assessment (distinct lobe).\n- 76377/77012: 3D Rendering/CT Guidance (Check facility billing rules).\nDiagnosis: Solitary lung nodule (R91.1).",
            4: "Procedure: Ion Bronch\nPatient: Joseph Sanchez\nSteps:\n1. Time out. GA.\n2. Set up Ion robot.\n3. Drove to RUL nodule. Spun the C-arm (CIOS) to check spot. Perfect.\n4. Needles and cryo biopsies taken.\n5. Went to LLL with regular scope and did Chartis check. No flow = good for valves later.\n6. Extubated. All good.",
            5: "Thomas Rivera here for the robot bronch. He has a nodule in the RUL and COPD. We used the ion robot to get out there. Spun the ct scan to make sure we were in the right spot. Took a bunch of biopsies with the needle and the freezer probe. Then we checked his left lung with the chartis balloon to see if we can put valves in later looks like no collateral ventilation so thats a go. No complications.",
            6: "Patient: Charles Torres. Procedure: Robotic Navigational Bronchoscopy with Biopsy and Chartis Assessment. Equipment: Ion Endoluminal System, Cios Spin. Findings: 1.4 cm RUL nodule. Actions: Navigation to target. Cone beam CT confirmation. TBNA (21G/23G) and Cryobiopsy performed. ROSE: Atypical cells. Additional: LLL Chartis assessment (CV negative). Complications: None.",
            7: "[Indication] RUL nodule, COPD.\n[Anesthesia] General.\n[Description] Navigational bronchoscopy (Ion) to RUL nodule. Position confirmed with Cone Beam CT. TBNA and Cryobiopsy performed. LLL Chartis assessment performed (CV negative).\n[Plan] Discharge. Await pathology.",
            8: "Mr. Christopher Ramirez underwent a robotic bronchoscopy today. We successfully navigated the robotic catheter to the small nodule in his right upper lung. To be absolutely sure of our location, we took a 3D CT scan right there in the room, which showed we were right on target. We took several biopsies. Since he also has severe COPD, we tested his left lung to see if he might be a candidate for valves in the future, and the test looked promising.",
            9: "Operation: Computer-assisted image-guided bronchoscopy.\nSubject: Daniel Cruz.\nTechnique: The robotic catheter was steered to the RUL target. Localization was validated via Cone Beam CT. Lesion sampled via needle aspiration and cryoprobe. A Chartis occlusion balloon was deployed in the LLL to appraise collateral ventilation. The airway was inspected and found patent."
        },
        3: { # Cooper/Scott (EBUS)
            1: "Indication: Mediastinal Adenopathy.\nProcedure: EBUS-TBNA.\nNodes Sampled:\n- 7 (Subcarinal): ROSE Positive.\n- 4R/4L: Sampled.\n- 10L/11L: Sampled.\nTotal 5 stations. 14 passes.\nDx: N3 Disease (Stage IIIB).\nPlan: Onc consult.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA).\nPATIENT: Mr. William Turner.\nCLINICAL SUMMARY: Evaluation of mediastinal lymphadenopathy in the setting of a LUL mass. A systematic EBUS survey was conducted. Lymph node stations 4R, 4L, 7, 10L, and 11L were visualized and sampled. Rapid On-Site Evaluation (ROSE) confirmed squamous cell carcinoma in the subcarinal (7) and contralateral (4R) stations, confirming N3 disease. The procedure was uncomplicated.",
            3: "CPT 31653 Justification:\n- Modality: EBUS-TBNA.\n- Scope: Linear array EBUS.\n- Work: Sampling of 3 or more mediastinal/hilar nodes.\n- Stations: 4R, 4L, 7, 10L, 11L (5 distinct stations).\n- Outcome: Diagnosis of malignancy established.",
            4: "Procedure: EBUS\nPatient: Joseph Parker\nSteps:\n1. Scope in. Airway exam normal.\n2. Ultrasound survey: 4R, 4L, 7 big.\n3. Needles into 7, 4R, 4L, 10L, 11L.\n4. Pathologist in room said its cancer (Squamous).\n5. No bleeding.\nPlan: Oncology referral.",
            5: "note for Charles Evans doing ebus for staging. he has lul mass. we poked a bunch of nodes station 7 4r 4l 10l 11l. rose said squamous cell ca. looks like stage 3b at least since both sides positive. no issues during case minimal blood. woke up fine.",
            6: "EBUS-TBNA. Patient: Thomas Edwards. Stations Sampled: 4R (21mm), 4L (27mm), 7 (33mm), 10L (15mm), 11L (18mm). Needle: 22G. Passes: 14 total. ROSE Results: Squamous cell carcinoma confirmed in Station 7 and 4L. Diagnosis: N3 Malignancy. Complications: None.",
            7: "[Indication] LUL mass, mediastinal adenopathy.\n[Anesthesia] Moderate Sedation.\n[Description] EBUS-TBNA of stations 4R, 4L, 7, 10L, 11L. ROSE confirmed Squamous Cell Carcinoma.\n[Plan] Oncology referral for Stage IIIB disease.",
            8: "Mr. Christopher Collins underwent an EBUS procedure to check the lymph nodes in the center of his chest. We found enlarged nodes on both the left and right sides. We used a special needle to take samples from five different areas. Unfortunately, the preliminary results show that the cancer has spread to these nodes, which is an important finding for determining the best treatment. We will have the final report in a few days.",
            9: "Operation: Endobronchial ultrasound with transbronchial needle aspiration.\nSubject: Daniel Stewart.\nFindings: Enlarged lymph nodes identified at stations 7, 4R, and 4L. These were aspirated along with 10L and 11L. Cytology confirmed malignancy (Squamous cell). This establishes N3 nodal involvement."
        },
        4: { # Cooper (Short EBUS)
            1: "Procedure: EBUS-TBNA (Summary)\nStations: 2R, 4R, 4L, 7, 10L, 11L.\nResults: ROSE positive for Malignancy (SqCC).\nDx: N3 Disease.\nStatus: Complete.",
            2: "CLINICAL ABSTRACT: This is a summary record for Mr. Robert Reed. An EBUS-TBNA was performed sampling stations 4R, 4L, 7, 10L, and 11L. Pathologic evaluation confirmed Squamous Cell Carcinoma. The findings are consistent with Stage IIIB (N3) disease.",
            3: "Coding Extract:\nService: 31653 (EBUS sampling 3+ nodes).\nNodes: 4R, 4L, 7, 10L, 11L.\nDate: 02/19/2025.\nProvider: Dr. Harris.",
            4: "Procedure: EBUS\nPatient: William Cook\nSampled: 4R, 4L, 7, 10L, 11L.\nResult: Cancer.\nPlan: Oncology.",
            5: "short note for Joseph Morgan ebus done today. hit nodes 7 4r 4l 10l 11l. came back squamous cell. stage 3b. dr harris signing off.",
            6: "EBUS-TBNA Summary. Patient: Charles Bell. Stations: 4R, 4L, 7, 10L, 11L. Pathology: Squamous Cell Carcinoma. Stage: IIIB.",
            7: "[Procedure] EBUS-TBNA.\n[Stations] 4R, 4L, 7, 10L, 11L.\n[Diagnosis] Squamous Cell Carcinoma (N3).\n[Plan] Tumor board.",
            8: "This is a brief record for Mr. Thomas Murphy. We performed an EBUS and sampled five lymph node stations. The results confirm squamous cell carcinoma spread to the mediastinum.",
            9: "Operation: EBUS-TBNA.\nSubject: Christopher Bailey.\nOutcome: Aspiration of mediastinal nodes confirmed Squamous Cell Carcinoma. N3 disease established."
        },
        5: { # Cooper/Scott Duplicate (Treated as EBUS again)
            1: "Indication: Mediastinal Adenopathy.\nProcedure: EBUS-TBNA.\nNodes Sampled:\n- 7 (Subcarinal): ROSE Positive.\n- 4R/4L: Sampled.\n- 10L/11L: Sampled.\nTotal 5 stations. 14 passes.\nDx: N3 Disease (Stage IIIB).\nPlan: Onc consult.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA).\nPATIENT: Mr. Kenneth Campbell.\nCLINICAL SUMMARY: Evaluation of mediastinal lymphadenopathy in the setting of a LUL mass. A systematic EBUS survey was conducted. Lymph node stations 4R, 4L, 7, 10L, and 11L were visualized and sampled. Rapid On-Site Evaluation (ROSE) confirmed squamous cell carcinoma in the subcarinal (7) and contralateral (4R) stations, confirming N3 disease. The procedure was uncomplicated.",
            3: "CPT 31653 Justification:\n- Modality: EBUS-TBNA.\n- Scope: Linear array EBUS.\n- Work: Sampling of 3 or more mediastinal/hilar nodes.\n- Stations: 4R, 4L, 7, 10L, 11L (5 distinct stations).\n- Outcome: Diagnosis of malignancy established.",
            4: "Procedure: EBUS\nPatient: George Mitchell\nSteps:\n1. Scope in. Airway exam normal.\n2. Ultrasound survey: 4R, 4L, 7 big.\n3. Needles into 7, 4R, 4L, 10L, 11L.\n4. Pathologist in room said its cancer (Squamous).\n5. No bleeding.\nPlan: Oncology referral.",
            5: "note for Steven Roberts doing ebus for staging. he has lul mass. we poked a bunch of nodes station 7 4r 4l 10l 11l. rose said squamous cell ca. looks like stage 3b at least since both sides positive. no issues during case minimal blood. woke up fine.",
            6: "EBUS-TBNA. Patient: Edward Carter. Stations Sampled: 4R (21mm), 4L (27mm), 7 (33mm), 10L (15mm), 11L (18mm). Needle: 22G. Passes: 14 total. ROSE Results: Squamous cell carcinoma confirmed in Station 7 and 4L. Diagnosis: N3 Malignancy. Complications: None.",
            7: "[Indication] LUL mass, mediastinal adenopathy.\n[Anesthesia] Moderate Sedation.\n[Description] EBUS-TBNA of stations 4R, 4L, 7, 10L, 11L. ROSE confirmed Squamous Cell Carcinoma.\n[Plan] Oncology referral for Stage IIIB disease.",
            8: "Mr. Kevin Evans underwent an EBUS procedure to check the lymph nodes in the center of his chest. We found enlarged nodes on both the left and right sides. We used a special needle to take samples from five different areas. Unfortunately, the preliminary results show that the cancer has spread to these nodes, which is an important finding for determining the best treatment. We will have the final report in a few days.",
            9: "Operation: Endobronchial ultrasound with transbronchial needle aspiration.\nSubject: Ronald Turner.\nFindings: Enlarged lymph nodes identified at stations 7, 4R, and 4L. These were aspirated along with 10L and 11L. Cytology confirmed malignancy (Squamous cell). This establishes N3 nodal involvement."
        },
        6: { # Linda Harrison (PleurX)
            1: "Indication: Recurrent malignant pleural effusion (Rt).\nProcedure: PleurX Catheter Insertion (32550).\nSteps: US guidance. Local anes. Tunnel created. 15.5Fr catheter inserted. 1.1L drained.\nOutcome: Good flow. CXR confirms position.\nPlan: Home health education.",
            2: "OPERATIVE REPORT: Ms. Mary Cox presented with a symptomatic recurrent right pleural effusion secondary to metastatic ovarian cancer. To facilitate outpatient management, an indwelling pleural catheter (IPC) was placed. Under ultrasound guidance, the 6th intercostal space was identified. A subcutaneous tunnel was created, and the 15.5 French PleurX catheter was introduced into the pleural space using the Seldinger technique. Approximately 1,100 mL of fluid was evacuated. The device functioned appropriately.",
            3: "CPT 32550: Insertion of indwelling tunneled pleural catheter.\nGuidance: Ultrasound (76942 usually bundled or separately reported depending on payer, text says US guidance used).\nDrainage: 1,100 mL removed.\nDevice: PleurX 15.5 Fr.\nDiagnosis: Malignant pleural effusion.",
            4: "Procedure: PleurX Placement\nPatient: Patricia Howard, 66F\nSteps:\n1. US to find spot on Right back.\n2. Numbed skin. Made tunnel.\n3. Put catheter in. Drained 1L yellow fluid.\n4. Stitched it in.\n5. Teaching done with family.\nPlan: Drain every other day.",
            5: "Linda Ward needed a pleurx for her cancer fluid. right side. prepped the skin used ultrasound. tunneled it under the skin put the tube in. drained about a liter. patient got a little coughing but ok. catheter works good. home health to follow up.",
            6: "Procedure: Tunneled Pleural Catheter Insertion (Right). Patient: Barbara Torres. Indication: Malignant effusion (Ovarian Ca). Technique: Ultrasound guided access, 6th ICS. 7cm tunnel. 15.5Fr PleurX placed. Output: 1,100mL clear yellow. Complications: None. Disposition: Discharge.",
            7: "[Indication] Recurrent malignant pleural effusion, palliation.\n[Anesthesia] Local (Lidocaine).\n[Description] Ultrasound guidance. PleurX catheter tunneled and inserted right hemithorax. 1.1L drained.\n[Plan] Home drainage protocol.",
            8: "Ms. Elizabeth Peterson is suffering from fluid buildup around her lung due to her cancer. To help her breathe better at home, we placed a PleurX drain today. We numbed the area on her right side, created a small tunnel under the skin for the tube, and inserted it into the fluid pocket. We drained over a liter of fluid immediately, which should give her relief. We taught her family how to use the bottles.",
            9: "Operation: Implantation of indwelling tunneled pleural catheter.\nSubject: Jennifer Gray.\nTechnique: The right pleural space was accessed under sonographic guidance. A subcutaneous tract was fashioned. The PleurX conduit was advanced into the cavity. 1,100 mL of effusion was evacuated. The external portion was secured."
        },
        7: { # David Johnson (Pleuroscopy)
            1: "Indication: Left exudative effusion, undiagnosed.\nProcedure: Medical Thoracoscopy (32609).\nFindings: Diffuse nodular thickening (visceral/parietal). Trapped lung.\nAction: Biopsies x13. 24Fr Chest Tube placed.\nImpression: Suspicious for Mesothelioma.\nPlan: Admitted.",
            2: "OPERATIVE NARRATIVE: Mr. James Brooks presented for diagnostic pleuroscopy. Under MAC, the left hemithorax was accessed. Inspection revealed diffuse, confluent nodularity of the parietal and visceral pleura, suggestive of malignancy. Multiple biopsies were obtained. Due to extensive visceral restriction (trapped lung), pleurodesis was contraindicated. A 24 Fr chest tube was placed for drainage. The clinical picture strongly favors malignant pleural mesothelioma.",
            3: "Code 32609: Thoracoscopy with biopsy of pleura.\nNote: Lung was trapped, preventing pleurodesis (supports decision not to bill 32650). 24 Fr Chest tube placed for management.\nPathology: Sent for mesothelioma panel.\nSetting: Endoscopy/OR.",
            4: "Procedure: Pleuroscopy\nPatient: John Kelly, 59M\nSteps:\n1. MAC sedation. Left side up.\n2. Trocar in.\n3. Looked around: nodules everywhere. Lung trapped.\n4. Took 10+ biopsies.\n5. Put chest tube in (24Fr).\nIt looks like mesothelioma.\nPlan: Admit.",
            5: "Robert Sanders here for the scope of the pleural space. fluid on the left side. went in with the rigid scope. looks bad lots of nodules all over the pleura probably mesothelioma. lung is trapped so it wont expand. took a bunch of biopsies sent for path. put a chest tube in cant glue it shut if the lung dont expand. admitting him.",
            6: "Procedure: Medical Thoracoscopy. Patient: Michael Price. Findings: Diffuse pleural thickening/nodularity. Trapped lung. Action: Parietal and visceral pleural biopsies (n=13). Drainage of 1,350mL fluid. Chest tube placement (24Fr). Diagnosis: Suspicious for Mesothelioma.",
            7: "[Indication] Undiagnosed left pleural effusion.\n[Anesthesia] MAC.\n[Description] Pleuroscopy performed. Diffuse nodularity seen. Biopsies taken. Trapped lung noted. Chest tube placed.\n[Plan] Admit. Wait for path.",
            8: "Mr. William Bennett underwent a procedure to look inside his chest cavity today. We drained the fluid and saw extensive thickening and nodules on the lining of the lung and chest wall. We are very suspicious this is mesothelioma. Because the lung is trapped by this tissue and cannot expand, we could not seal the space today. Instead, we took biopsies and placed a chest tube to keep the fluid drained while we wait for results.",
            9: "Operation: Medical thoracoscopy with pleural biopsy.\nSubject: David Wood.\nFindings: The pleural cavity exhibited extensive nodularity consistent with malignancy. The lung was incarcerated. Biopsies were harvested from the parietal and visceral surfaces. A thoracostomy tube was sited for drainage."
        },
        8: { # Jennifer Taylor (EBUS - Note 7)
            1: "Indication: Staging RLL Adenocarcinoma.\nProcedure: EBUS-TBNA.\nSurvey: 2R, 4R, 4L, 7, 10R, 11R.\nSampled: 7 (Pos), 4R (Atypical), 4L (Benign), 10R, 11R.\nDx: N2 positive (Station 7). Stage IIIA.\nPlan: Onc consult.",
            2: "PROCEDURE NOTE: Ms. Patricia Coleman underwent EBUS staging for T2aN0M0 RLL adenocarcinoma. Assessment of the mediastinum revealed an enlarged subcarinal node (Station 7). TBNA of Station 7 yielded adenocarcinoma on ROSE, confirming N2 disease. Contralateral station 4L was negative. The patient is upstaged to IIIA.",
            3: "CPT 31653: EBUS sampling of 3+ stations.\nStations sampled: 7, 4R, 4L, 10R, 11R.\nResults:\n- 7: Positive (Adeno).\n- 4R: Atypical.\n- Others: Negative/Reactive.\nClinical Impact: Confirmation of N2 disease significantly alters management (multimodal therapy vs surgery first).",
            4: "Procedure: EBUS\nPatient: Linda Jenkins, 55F\nIndication: Staging lung cancer.\nSteps:\n1. US check of nodes.\n2. Needles into 7, 4R, 4L, 10R, 11R.\n3. ROSE said Station 7 is cancer.\n4. That means N2 disease.\nPlan: Chemo/Rad referral?",
            5: "Barbara Perry here for staging ebus. she has a cancer in the right lower lobe. checked the middle nodes station 7 was big. poked it and it is cancer. poked the other ones 4r 4l 10r 11r mostly benign. so she has n2 disease now. needs oncology.",
            6: "EBUS-TBNA Staging. Patient: Elizabeth Powell. Primary: RLL Adeno. Stations Sampled: 7 (Pos), 4R, 4L, 10R, 11R. Findings: N2 disease confirmed at Station 7 (28mm). Complications: None.",
            7: "[Indication] Staging RLL Adenocarcinoma.\n[Anesthesia] Moderate.\n[Description] EBUS-TBNA stations 7, 4R, 4L, 10R, 11R. Station 7 positive for malignancy.\n[Plan] Oncology consult for Stage IIIA.",
            8: "Ms. Jennifer Long came in for staging of her lung cancer. We used the EBUS scope to sample lymph nodes in the center of her chest. Unfortunately, the lymph node under the main airway (Station 7) tested positive for cancer cells. This changes her stage to IIIA. We sampled other nodes to be thorough, but they were negative. We will discuss the next steps with oncology.",
            9: "Operation: EBUS mediastinal staging.\nSubject: Maria Patterson.\nOutcome: Transbronchial aspiration of the subcarinal node (St 7) demonstrated adenocarcinoma. This confirms mediastinal nodal involvement (N2). Other stations were sampled for completeness."
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
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation is missing
                note_entry["note_text"] = f"VARIATION_MISSING for index {idx} style {style_num}"
            
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
    output_filename = output_dir / "synthetic_notes_part_005.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()