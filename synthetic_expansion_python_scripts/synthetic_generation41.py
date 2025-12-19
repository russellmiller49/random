import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_041.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Janet S. Williams (PFA LUL)
            1: "Indication: LUL 1.9cm SCC. Protocol PULSE-LUNG.\nAnesthesia: GA.\nProcedure: ENB to LUL apicoposterior. rEBUS confirmed. PFA catheter placement. 3 cycles 1500V.\nFindings: Increased echogenicity post-ablation. No thermal damage.\nComplications: None.\nPlan: Protocol follow-up.",
            2: "OPERATIVE NARRATIVE: Ms. Williams, a 58-year-old female enrolled in the PULSE-LUNG Phase II trial, underwent bronchoscopic Pulsed Field Ablation (PFA) for a biopsy-proven squamous cell carcinoma in the left upper lobe. Under general anesthesia, the lesion was localized via electromagnetic navigation and radial EBUS. The investigational FarapulsePulm catheter was deployed. Irreversible electroporation was delivered in three cycles of 1500V pulses. Post-ablation imaging demonstrated cellular disruption consistent with successful non-thermal ablation. The patient tolerated the procedure without arrhythmia or hemodynamic instability.",
            3: "CPT Coding: 31641 (Bronchoscopic destruction of tumor - Investigational PFA).\nGuidance: 31627 (ENB), 31654 (Radial EBUS).\nDevice: FarapulsePulm PFA catheter.\nDetails: Non-thermal energy, 1500V, 3 cycles.\nTarget: LUL Peripheral Nodule.\nStatus: Clinical Trial (IDE #BR-PFA-2024-017).",
            4: "Procedure Note\nAttending: Dr. Patel\nPatient: Janet Williams\nProcedure: PFA of LUL nodule\nSteps:\n1. GA/ETT.\n2. Navigated to LUL apicoposterior segment.\n3. Confirmed with rEBUS.\n4. Inserted PFA catheter.\n5. Delivered 3 cycles of pulsed energy (1500V).\n6. Monitored impedance - good delivery.\n7. Extubated stable.\nNote: No arrhythmias observed.",
            5: "janet williams here for the research study pulsed field ablation. she has squamous cell in the lul. we put her to sleep used the nav system to find the spot. put the special catheter in and zapped it 3 times with the electric pulses. no heat damage which is good. heart rhythm stayed fine. patient woke up ok going to follow the study protocol for scans.",
            6: "PATIENT: Williams, Janet S. || MRN: PFA-2025-447 || DOB: 05/19/1967 DATE OF PROCEDURE: November 18, 2025 INSTITUTION: Cleveland Clinic Foundation, OH OPERATOR: Dr. Richard Patel, MD (Director, Thoracic Innovation Laboratory) PRE-PROCEDURE DIAGNOSIS: Left upper lobe peripheral nodule, 1.9 cm, proven squamous cell carcinoma PROCEDURE: Bronchoscopic Pulsed Field Ablation (PFA) of pulmonary nodule - INVESTIGATIONAL... [Rest of text follows]",
            7: "[Indication]\nLUL SCC, 1.9cm. PULSE-LUNG Trial candidate.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nENB and rEBUS localization. PFA delivered (1500V x 3 cycles). Non-thermal ablation confirmed via rEBUS changes.\n[Plan]\nCT at 48 hours. Long-term registry.",
            8: "Ms. Williams participated in our PFA clinical trial today to treat her left upper lobe tumor. We used electromagnetic navigation to guide the specialized catheter to the site. Instead of heat, we used high-voltage electrical pulses to destroy the tumor cells. The procedure went perfectly according to protocol, and we saw immediate signs on the ultrasound that the tissue was treated. Her heart rhythm remained stable throughout.",
            9: "Subject: Williams, Janet S. Procedure: Bronchoscopic Pulsed Field Ablation (PFA). Methodology: General anesthesia. ENB performed. Target: LUL apicoposterior segment. Radial EBUS verification. Novel PFA catheter advanced. Ablation Parameters: Voltage 1500 V. Energy delivery: Non-thermal. Outcomes: Successfully completed per protocol. No arrhythmias observed. Disposition: Research protocol follow-up."
        },
        1: { # Elizabeth Chen (RML Obstruction)
            1: "Indication: RML collapse.\nFindings: Exophytic tumor obstructing RML.\nAction: Forceps biopsy x6. Wash.\nComp: Moderate bleeding, controlled with epi/iced saline.\nImpression: Endobronchial tumor.",
            2: "PROCEDURE REPORT: Ms. Chen presented for evaluation of right middle lobe collapse. Bronchoscopy revealed a near-complete obstruction of the RML bronchus by a necrotic, exophytic mass. Diagnostic sampling was performed via forceps biopsy and bronchial lavage. Hemostasis was achieved using topical vasoconstrictors after moderate hemorrhage was encountered.",
            3: "Code: 31625 (Bronchoscopy with endobronchial biopsy).\nSite: Right Middle Lobe Bronchus.\nPathology: Exophytic tumor.\nSampling: 6 forceps biopsies.\nNote: Bronchial wash (31622) performed but bundled. 31623 (Brush) not performed.",
            4: "Resident Note\nPatient: Elizabeth Chen\nProcedure: Bronchoscopy\n- Local anesthesia.\n- Airway: RML obstructed by tumor.\n- Biopsy: 6 bites taken from RML mass.\n- Bleeding: Moderate, stopped with epi.\n- Lavage collected.\n- Patient stable.",
            5: "patient elizabeth chen date of birth 1962. indication rml collapse. topical lidocaine used patient awake. rml is blocked by a tumor looks necrotic. took about 6 biopsies bleeding was moderate so we used epinephrine and cold saline. rll and left side looked normal. lavage sent for cytology. tolerated well.",
            6: "[START RECORDING 14:32] Patient name is Elizabeth Chen, medical record Papa Lima dash four eight two nine dash Quebec, date of birth November twenty-third nineteen sixty-two. [14:33] Indication is evaluation of right middle lobe collapse with concern for endobronchial obstruction. [14:34] Topical anesthesia achieved with nebulized lidocaine four percent followed by transtracheal injection of two percent lidocaine... [Rest of text]",
            7: "[Indication]\nRML collapse, rule out obstruction.\n[Anesthesia]\nTopical Lidocaine.\n[Description]\nRML obstructed by exophytic tumor. Biopsy x6 and Lavage performed. Bleeding controlled.\n[Plan]\nPathology pending.",
            8: "We examined Ms. Chen's airways to investigate why her right middle lung was collapsed. We found a tumor blocking the airway to that section. We took six biopsy samples from the mass. There was some bleeding, which is common with these tumors, but we stopped it with medication. We also washed the area to collect cells for analysis.",
            9: "Patient name is Elizabeth Chen. Indication is evaluation of right middle lobe collapse. Right middle lobe bronchus displays near complete obstruction by an exophytic tumor. Multiple forceps biopsies acquired from the tumor. Moderate hemorrhage encountered, controlled with topical epinephrine. Bronchial lavage acquired from RML. Patient tolerated well."
        },
        2: { # Barbara Kim (Massive Bleed/Stent)
            1: "Emergency Bronchoscopy.\nIndication: Central airway obstruction (RML).\nEvent: Massive hemoptysis (300mL) during debulking.\nAction: Hemostasis (blocker/epi). Stent placed (14x40mm).\nDispo: ICU, intubated.",
            2: "OPERATIVE SUMMARY: Ms. Kim underwent therapeutic bronchoscopy for RML tumor debulking. The procedure was complicated by massive hemoptysis estimated at 300mL. Hemodynamic stability was maintained while hemostasis was achieved using a bronchial blocker and iced saline. A 14x40mm silicone stent was deployed to secure the airway and tamponade the bleeding vessel. The patient was transferred to the MICU intubated for monitoring.",
            3: "Codes: 31641 (Tumor destruction), 31636 (Stent placement - bronchial).\nContext: Complex therapeutic bronchoscopy.\nComplication: Severe hemorrhage requiring tamponade.\nDevice: Silicone stent 14x40mm.\nDisposition: Critical care.",
            4: "Resident Note\nPatient: Barbara Kim\nProcedure: Therapeutic Bronchoscopy\n- RML tumor debulking started.\n- Massive bleeding occurred.\n- Blocked RML, used epi/ice.\n- Placed silicone stent.\n- Bleeding stopped.\n- Patient remains intubated in ICU.",
            5: "barbara kim 69 female therapeutic bronch for rml obstruction. started debulking with apc and cautery then massive bleeding started like 300ml. scary moment. put a blocker in and used ice. put a stent in 14 by 40 silicone. bleeding stopped. keep her asleep in the icu check blood counts.",
            6: "Pt: Barbara Kim | MR: PP-8473 | DOB: 06/30/1955 | AGE: 69 PROCEDURE: Therapeutic bronchoscopy - central airway obstruction AIRWAY: General anesthesia, ETT 7.5, maintained throughout INTERVENTION PERFORMED: - RML tumor debulking (electrocautery + APC) - Massive hemoptysis during procedure (est. 300mL) - Controlled with: epi, iced saline, blocker in RML - Silicone stent 14x40mm placed... [Rest of text]",
            7: "[Indication]\nRML Tumor Obstruction.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nDebulking initiated. Complicated by massive hemoptysis. Hemostasis achieved. Silicone stent placed (14x40mm).\n[Plan]\nMICU admission. Mechanical ventilation.",
            8: "Ms. Kim's procedure was intended to clear a tumor blocking her right middle airway. During the removal process, she experienced severe bleeding. We acted quickly to block the area and apply cold saline to stop the flow. We then placed a silicone stent to keep the airway open and put pressure on the bleeding site. She is currently stable but remains on a ventilator in the ICU for close watching.",
            9: "Pt: Barbara Kim. PROCEDURE: Therapeutic bronchoscopy. INTERVENTION EXECUTED: RML tumor debulking. Massive hemoptysis during procedure. Controlled with: epi, iced saline, blocker in RML. Silicone stent 14x40mm deployed. COMPLICATION: MAJOR AIRWAY HEMORRHAGE. CURRENT STATUS: Still intubated, sedated. TRANSFERRED TO: MICU."
        },
        3: { # Karen White (Failed ENB)
            1: "Indication: 14mm LLL nodule.\nTechnique: ENB attempted. Failed to visualize lesion (no rEBUS signal).\nAction: Aborted nav. Blind biopsy x3 and brush x1 performed.\nResult: Nondiagnostic likely.\nPlan: CT biopsy or VATS.",
            2: "PROCEDURE NOTE: Ms. White underwent attempted electromagnetic navigation for a small LLL nodule. Despite extensive maneuvering and fluoroscopy (12.4 min), the radial EBUS probe failed to confirm a tool-in-lesion position. The navigation component was aborted. Blind transbronchial biopsies were obtained from the anatomical segment of interest. The patient was advised regarding the low likelihood of diagnostic yield.",
            3: "Codes: 31628 (Transbronchial biopsy), 31627 (Nav - attempted), 31654 (rEBUS - attempted).\nModifier: None (procedure performed, just unsuccessful localization).\nFluoro time: 12.4 min.\nOutcome: Localization failed.",
            4: "Resident Note\nPatient: Karen White\nProcedure: Attempted ENB\n- Navigated to LLL.\n- Could not find lesion with rEBUS.\n- Tried for 45 mins.\n- Decided to do blind biopsies instead.\n- Forceps x3, Brush x1.\n- No pneumo.",
            5: "karen white here for nav bronch lll nodule 14mm. tried to find it with the magnet system but couldnt get the radial ebus to show the concentric ring. tried for like 45 mins lots of fluoro. gave up on the nav and just took some blind bites with the forceps. probably wont get a diagnosis. discussed vats with her.",
            6: "PATIENT: KAREN WHITE | MED REC: PQ-5847 | DOB: 12/30/1962 INDICATION: LLL peripheral nodule 14mm, no clear bronchus sign, PET SUV 2.8 (indeterminate) ANESTHESIA: Moderate sedation protocol Midazolam 3mg, fentanyl 100mcg Ramsay 3 achieved, stable throughout PROCEDURE ATTEMPTED: Electromagnetic navigation system set up CT registration performed Target: LLL anteromedial segment nodule... [Rest of text]",
            7: "[Indication]\nLLL Nodule 14mm.\n[Anesthesia]\nModerate Sedation.\n[Description]\nENB localization attempted but failed (no rEBUS signal). Blind TBBx x3 and Brush x1 performed. No complications.\n[Plan]\nSurveillance or Surgical Biopsy.",
            8: "We tried to biopsy Ms. White's small lung nodule using the navigation system. Unfortunately, the anatomy was difficult, and we couldn't confirm the exact location with our ultrasound probe despite trying for 45 minutes. We took some samples from the general area, but we explained to her that we might not have hit the target. We may need to consider a needle biopsy or surgery next.",
            9: "PATIENT: KAREN WHITE. INDICATION: LLL peripheral nodule. PROCEDURE ATTEMPTED: Electromagnetic navigation system configured. Navigation attempt: Guide sheath advanced. Radial EBUS probe deployed - NO concentric pattern visualized. Unable to verify tool-in-lesion. Decision: Procedure aborted due to inability to localize. Sampling performed anyway (blind): Forceps biopsies x3. Brush cytology x1."
        },
        4: { # Sarah Chen (EBUS + ENB RLL)
            1: "Indication: RLL nodule + Adenopathy.\nEBUS: 4R(9mm) Pos, 7(11mm) Pos.\nENB: RLL 18mm nodule. rEBUS confirmed.\nSampling: TBNA x2, TBBx x3, Brush x2.\nResult: N2 disease + Primary sampled.",
            2: "OPERATIVE REPORT: Ms. Chen underwent combined staging and diagnostic bronchoscopy. EBUS-TBNA of stations 4R and 7 confirmed N2 nodal involvement (ROSE positive). Following this, electromagnetic navigation was used to localize an 18mm RLL lateral segment nodule. Tool-in-lesion was confirmed via radial EBUS. Transbronchial needle aspiration and forceps biopsies were obtained from the primary lesion.",
            3: "Codes: 31652 (EBUS 2 stations), 31629 (Peripheral TBNA), 31654 (rEBUS), 31627 (Nav).\nEBUS: 4R, 7.\nPeripheral: RLL mass (TBNA, Forceps, Brush).\nDiagnosis: Stage IIIB NSCLC.",
            4: "Resident Note\nPatient: Sarah Chen\nProcedure: Staging EBUS + ENB\n- Deep sedation.\n- EBUS: Sampled 4R and 7. Both malignant.\n- ENB: Navigated to RLL nodule.\n- Confirmed with rEBUS.\n- Took needle, forceps, and brush samples.\n- Bleeding controlled.",
            5: "sarah chen 67 female smoker rll mass and nodes. deep sedation propofol. did ebus first 4r and 7 both positive for cancer. then did navigation to the rll mass. radial ebus confirmed it. took 2 needle passes 3 biopsies and 2 brushes. moderate bleeding stopped with epi. discharged stable.",
            6: "Name: Sarah Chen | MRN# PX-2947-B | Birth: 03/09/1965 Pre-procedure: 67yo former smoker with RLL peripheral nodule 18mm, no bronchus sign on CT. PET shows SUV 4.2. Anesthesia: Deep sedation - propofol infusion 75-100mcg/kg/min, Ramsay 4-5, BP q5min, SpO2 continuous Part 1 - EBUS staging for PET+ N2 nodes: Station 4R (9mm SA) - 4x passes, ROSE+, PET+ Station 7 (11mm SA) - 3x passes, ROSE+, PET+ Molecular testing sent from station 4R sample... [Rest of text]",
            7: "[Indication]\nRLL mass, mediastinal LAD.\n[Anesthesia]\nDeep Sedation.\n[Description]\nEBUS-TBNA of 4R and 7 (Both Positive). ENB to RLL mass. TBNA/TBBx/Brush performed. Bleeding controlled.\n[Plan]\nChemoradiation.",
            8: "We performed a two-part procedure for Ms. Chen. First, we used EBUS to check the lymph nodes in the center of her chest; stations 4R and 7 both showed cancer cells. Second, we used the navigation system to reach the main tumor in her right lower lung and took several biopsy samples. This confirms the cancer has spread to the lymph nodes (Stage IIIB), so we will discuss chemotherapy and radiation.",
            9: "Name: Sarah Chen. Chief Indication: RUL mass with mediastinal LAD. Procedure Performed: 1. EBUS-TBNA for staging. 2. Flexible bronchoscopy with endobronchial biopsy. EBUS Component: Systematic mediastinal evaluation. Station 4R: 5 passes, ROSE Positive. Station 7: 4 passes, ROSE Positive. Bronchoscopy Component: Examination revealed mass effect. Multiple forceps biopsies obtained. Assessment: N2/N3 disease verified."
        },
        5: { # Martin Lee (ENB LLL + Pneumothorax)
            1: "Indication: 17mm LLL nodule.\nNav: ENB + rEBUS (concentric).\nSamples: TBNA x3, TBBx x5, Brush x2.\nComp: Small apical PTX (15%). Stable.\nDispo: Discharge with follow-up CXR.",
            2: "PROCEDURE NOTE: Mr. Lee underwent electromagnetic navigation bronchoscopy for a 17mm LLL nodule. Localization was achieved after repositioning, confirmed by a concentric rEBUS view. Systematic sampling included TBNA, forceps biopsy, and brushing. Post-procedure radiography revealed a 15% apical pneumothorax. The patient remained asymptomatic with stable vitals. Conservative management was elected, and the patient was discharged with close radiographic follow-up.",
            3: "Codes: 31629 (TBNA), 31654 (rEBUS), 31627 (Nav).\nBiopsies: 3 needle, 5 forceps, 2 brush.\nAdverse Event: Pneumothorax (J93.81) - Observation only.\nFluoro time: 7.2 min.",
            4: "Resident Note\nPatient: Martin Lee\nProcedure: ENB\n- Deep sedation.\n- Navigated to LLL superior segment.\n- rEBUS concentric.\n- Samples: Needle, Forceps, Brush.\n- Complication: Small pneumo on CXR.\n- Patient stable, sent home.",
            5: "case c-847 martin lee. enb for lll nodule 17mm. used superdimension system. had to reposition to get good ebus view but got it eventually. took needle biopsy forceps and brush. xray showed a small pneumothorax about 15 percent. he felt fine so we didnt put a tube in. sent him home will check xray tomorrow.",
            6: "CASE PRESENTATION: Complex Navigation Bronchoscopy PATIENT DEMOGRAPHICS: A 64-year-old male (Case ID: C-847, Synthetic Name: Martin Lee, MRN: QQ-8473-R, DOB: 05/22/1960) former smoker with 45 pack-year history presented with an incidentally discovered left lower lobe peripheral pulmonary nodule. IMAGING CHARACTERISTICS: Computed tomography demonstrated a 17mm solid nodule in the left lower lobe superior segment without clear bronchus sign... [Rest of text]",
            7: "[Indication]\nLLL Nodule 17mm.\n[Anesthesia]\nDeep Sedation.\n[Description]\nENB to LLL. rEBUS confirmed. TBNA x3, TBBx x5, Brush x2. Small PTX noted post-op.\n[Plan]\nConservative management of PTX. Discharge.",
            8: "Mr. Lee underwent a navigation bronchoscopy for a spot in his lower left lung. We successfully located the 17mm nodule using the electromagnetic system and confirmed it with ultrasound. We took multiple samples. Afterward, the chest x-ray showed a small lung collapse (pneumothorax). Since he had no symptoms and his oxygen levels were good, we decided he didn't need a chest tube and could go home with a follow-up x-ray scheduled.",
            9: "CASE PRESENTATION: Complex Navigation Bronchoscopy. PROCEDURAL APPROACH: Electromagnetic navigation bronchoscopy was selected. Technical Details: The electromagnetic navigation system was employed. The extended working channel was advanced. Radial endobronchial ultrasound probe deployment demonstrated concentric echogenic pattern. Sampling Protocol: Transbronchial needle aspiration: 3 passes. Transbronchial forceps biopsy: 5 specimens. COMPLICATIONS: Small apical pneumothorax identified. Conservative management elected."
        },
        6: { # Helen Garcia (EBUS LLL Staging + Flumazenil)
            1: "Indication: Staging LLL Adeno.\nEBUS: 4R(10mm)+, 7(19mm)+, 10L(8mm)-.\nEvent: Over-sedation post-op.\nAction: Flumazenil 0.2mg IV.\nResult: Aroused, stable. D/C after 3hr.",
            2: "PROCEDURE NOTE: Ms. Garcia underwent EBUS-TBNA for staging of LLL adenocarcinoma. Lymph node stations 4R and 7 were sampled and confirmed malignant (N3 disease relative to LLL primary). Station 10L was benign. In the recovery phase, the patient exhibited prolonged sedation and bradypnea. Flumazenil was administered with immediate positive effect. She was monitored for an extended period before discharge.",
            3: "Code: 31653 (EBUS 3 stations).\nDiagnosis: LLL Adenocarcinoma.\nNodes: 4R, 7, 10L.\nDrug: Flumazenil used for reversal.\nPathology: Metastatic adenocarcinoma in 4R/7.",
            4: "Resident Note\nPatient: Helen Garcia\nProcedure: EBUS\n- Sampled 4R, 7, 10L.\n- ROSE positive for cancer in 4R and 7.\n- Patient too sleepy in PACU.\n- Gave Flumazenil.\n- Woke up fine.",
            5: "helen garcia for ebus staging. gave midazolam and fentanyl. did the exam 4r and 7 were positive for cancer 10l negative. after the procedure she was really groggy breathing slow. had to give flumazenil to wake her up. she came around quick. kept her a bit longer to make sure she didnt get sleepy again.",
            6: "PATIENT: HELEN GARCIA / ID: QR-8374-M / DATE OF BIRTH: 01/07/1958 INDICATION: Mediastinal staging for LLL adenocarcinoma SEDATION: Moderate sedation protocol initiated Midazolam 4mg IV (given incrementally) Fentanyl 125mcg IV total dose Target Ramsay 3-4 achieved EBUS PROCEDURE: Systematic N3->N2->N1 evaluation - Station 4R (10mm): 4 passes, PET+, ROSE positive for metastatic adenocarcinoma - Station 7 (19mm): 4 passes, PET+, ROSE positive for metastatic adenocarcinoma... [Rest of text]",
            7: "[Indication]\nStaging LLL Ca.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS-TBNA 4R, 7, 10L. N3 disease confirmed. Post-op sedation required reversal with Flumazenil.\n[Plan]\nOncology.",
            8: "Ms. Garcia underwent staging for her lung cancer. We found that the cancer had spread to the lymph nodes on the right side (4R) and the center (7), which is important for her treatment plan. After the procedure, she was very slow to wake up and her breathing was shallow, so we gave her a medication called Flumazenil to reverse the sedation. She woke up immediately and went home safely after extra monitoring.",
            9: "PATIENT: HELEN GARCIA. INDICATION: Mediastinal staging. EBUS PROCEDURE: Systematic evaluation. Station 4R: 4 passes, ROSE positive. Station 7: 4 passes, ROSE positive. Station 10L: 3 passes, ROSE benign. COMPLICATION: Patient remained overly sedated. FLUMAZENIL administered. Immediate improvement in alertness. No other adverse events."
        },
        7: { # Jennifer Wang (EBUS + Bronch RUL Mass)
            1: "Indication: RUL mass, staging.\nEBUS: 2R, 4R, 7 (All Positive). 10R Benign.\nBronch: RUL mass biopsy x6.\nResult: Stage IIIB.\nComp: Mod bleeding, controlled.",
            2: "OPERATIVE REPORT: Ms. Wang presented for diagnostic and staging bronchoscopy. EBUS-TBNA confirmed multi-station N2/N3 disease (Stations 2R, 4R, 7 positive). The bronchoscope was then used to visualize and biopsy a large RUL mass causing partial obstruction. Adequate tissue was obtained for molecular profiling. Hemostasis was secured with topical epinephrine.",
            3: "Codes: 31653 (EBUS 4 stations), 31625 (Bronchial biopsy).\nSites: 2R, 4R, 7, 10R (EBUS); RUL (Biopsy).\nDiagnosis: Lung Ca, Stage IIIB.\nNote: High complexity staging and diagnosis.",
            4: "Resident Note\nPatient: Jennifer Wang\nProcedure: EBUS + Biopsy\n- EBUS: 2R, 4R, 7, 10R.\n- ROSE pos in 2R, 4R, 7.\n- Bronchoscopy: Biopsied RUL mass.\n- Bleeding required epi.\n- Plan: Chemoradiation.",
            5: "jennifer wang 61 female rul mass. did ebus first. 2r 4r and 7 all cancer. 10r was ok. then looked at the rul mass it was blocking the airway a bit. took 6 biopsies and brushed it. bleeding was moderate used iced saline. confirmed stage 3b. need molecular markers.",
            6: "Patient: Jennifer Wang | ID: RR-3847-P | Birth Date: 06/28/1963 Date of Service: 10/22/2024 | Time: 10:30 AM Chief Indication: RUL mass with mediastinal LAD, diagnostic + staging HPI: 61F, 35 pack-year smoker (active), presents with 3-month history of cough and right-sided chest discomfort. CT chest shows 3.2cm RUL mass with bulky mediastinal lymphadenopathy. PET-CT reveals primary lesion SUV 9.4, multiple N2 stations PET-avid (4R, 7, 2R). Procedure Performed: 1. EBUS-TBNA for staging 2. Flexible bronchoscopy with endobronchial biopsy... [Rest of text]",
            7: "[Indication]\nRUL Mass, Staging.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS-TBNA 2R, 4R, 7, 10R. Malignancy in mediastinal nodes. Endobronchial biopsy of RUL mass. Bleeding controlled.\n[Plan]\nOncology.",
            8: "We performed a comprehensive procedure for Ms. Wang to diagnose her lung mass and check the lymph nodes. The EBUS portion showed extensive spread to the lymph nodes (2R, 4R, and 7). We also biopsied the main tumor in the right upper lobe. This confirms advanced stage disease (IIIB). We managed some bleeding during the biopsy, and she recovered well.",
            9: "Patient: Jennifer Wang. Chief Indication: RUL mass with mediastinal LAD. Procedure Performed: EBUS-TBNA for staging. Flexible bronchoscopy with endobronchial biopsy. EBUS Component: Station 2R: 4 passes, ROSE Positive. Station 4R: 5 passes, ROSE Positive. Station 7: 4 passes, ROSE Positive. Station 10R: 3 passes, ROSE benign. Bronchoscopy Component: Examination revealed mass effect. Multiple forceps biopsies acquired. Assessment: N2/N3 disease verified."
        },
        8: { # Mark Thompson (Traditional Bronch RLL)
            1: "Indication: RLL 21mm nodule, bronchus sign+.\nTechnique: Traditional bronch (no nav). Fluoroscopy used.\nSampling: TBNA x3, TBBx x8, Brush x2.\nResult: Lesion visualized. Diagnostic yield high.\nComp: Minor bleeding.",
            2: "PROCEDURE NOTE: Mr. Thompson underwent diagnostic bronchoscopy for an RLL nodule. Due to a positive bronchus sign, traditional thin bronchoscopy was utilized without electromagnetic navigation. The lesion was visualized endobronchially and confirmed with radial EBUS. Transbronchial needle aspiration and forceps biopsies were performed under fluoroscopic guidance. Tolerance was excellent.",
            3: "Codes: 31629 (TBNA), 31654 (rEBUS).\nNote: No 31627 (Nav) charged - traditional approach used.\nBiopsy: RLL nodule.\nFluoroscopy time: 3.1 min.",
            4: "Resident Note\nPatient: Mark Thompson\nProcedure: Bronchoscopy\n- RLL nodule with bronchus sign.\n- Went down with thin scope.\n- Saw the lesion.\n- Confirmed with rEBUS.\n- Needle and forceps biopsies taken.\n- No navigation needed.",
            5: "mark thompson rll nodule. saw a bronchus sign on ct so didnt use the superdimension. just went down there and saw the mucosal irregularity. radial ebus confirmed it was solid. took needle aspirates and forceps biopsies. simple procedure no complications. discharged home.",
            6: "Patient: Mark Thompson | MRN# TK-9472 | Born: 09/03/1964 INDICATION: RLL 21mm solid nodule with clear bronchus sign on CT, PET SUV 4.8 ANESTHESIA: Moderate sedation, midazolam 3mg + fentanyl 75mcg Ramsay 3 throughout, monitoring BP q5min, SpO2 continuous TECHNIQUE: Traditional bronchoscopy (no navigation system needed due to bronchus sign) Procedure: - Thin bronchoscope advanced to RLL - Bronchus sign followed to nodule location - Lesion visualized endobronchially as subtle mucosal irregularity... [Rest of text]",
            7: "[Indication]\nRLL Nodule 21mm.\n[Anesthesia]\nModerate Sedation.\n[Description]\nTraditional bronchoscopy to RLL. Lesion visualized. rEBUS confirmed. TBNA and TBBx performed. No Nav used.\n[Plan]\nDischarge.",
            8: "Mr. Thompson had a nodule in his right lower lung that had a clear airway leading to it, so we didn't need the advanced navigation system. We guided the scope directly to the spot, confirmed it with ultrasound, and took samples with a needle and forceps. He had a little bleeding that stopped on its own, and he went home shortly after.",
            9: "Patient: Mark Thompson. INDICATION: RLL 21mm solid nodule. TECHNIQUE: Traditional bronchoscopy. Procedure: Thin bronchoscope advanced to RLL. Lesion visualized endobronchially. Radial EBUS probe: Solid eccentric pattern. Sampling performed: Transbronchial needle aspiration x3. Transbronchial forceps biopsy x5. Brush cytology x2. Complications: Minor self-limited hemorrhage."
        },
        9: { # Sandra Lopez (EBUS Breast Met)
            1: "Indication: Hx Breast CA, Adenopathy.\nEBUS: 2R, 4R, 7.\nResult: All positive for metastatic breast adenocarcinoma.\nPlan: Oncology for systemic therapy.\nLimit: No PET (CKD).",
            2: "PROCEDURE REPORT: Ms. Lopez, with a history of breast cancer and CKD, presented for evaluation of mediastinal lymphadenopathy. EBUS-TBNA was performed on stations 2R, 4R, and 7. Rapid on-site evaluation was consistent with metastatic adenocarcinoma of breast origin in all sampled stations. Sedation was titrated carefully due to renal dysfunction. The patient remained stable.",
            3: "Code: 31653 (EBUS 3 stations).\nPathology: Metastatic Breast Cancer.\nStations: 2R, 4R, 7.\nComorbidities: CKD Stage 3 (modified sedation).\nAdequacy: Confirmed.",
            4: "Resident Note\nPatient: Sandra Lopez\nProcedure: EBUS\n- History of breast cancer.\n- Sampled 2R, 4R, 7.\n- ROSE showed breast cancer cells.\n- Used lower sedation dose because of kidneys.\n- No issues.",
            5: "sandra lopez 70 female hx breast cancer. kidney disease so no pet scan. did ebus to check lymph nodes. 2r 4r and 7 all looked like cancer on the slide breast origin. reduced fentanyl dose for her kidneys. vitals good. referred back to oncology for chemo.",
            6: "Patient: Sandra Lopez | MRN: TT-6849 | DOB: 12/05/1954 PROBLEM LIST: #1 Mediastinal lymphadenopathy - needs tissue diagnosis #2 History of breast cancer (2019) - in remission #3 Chronic kidney disease stage 3 SUBJECTIVE: 70F referred for EBUS evaluation of mediastinal nodes found on surveillance CT. Denies chest pain, hemoptysis, dyspnea. No PET scan performed due to renal dysfunction. OBJECTIVE: Procedure: EBUS-TBNA Sedation: Moderate (midazolam 2mg, fentanyl 50mcg) - limited doses due to CKD... [Rest of text]",
            7: "[Indication]\nMediastinal adenopathy, hx Breast CA.\n[Anesthesia]\nModerate Sedation (Renal dosing).\n[Description]\nEBUS-TBNA 2R, 4R, 7. Metastatic breast CA confirmed.\n[Plan]\nOncology.",
            8: "Ms. Lopez has a history of breast cancer and kidney disease. We performed an EBUS to check swollen lymph nodes in her chest. We sampled stations 2R, 4R, and 7. Unfortunately, all showed cells consistent with breast cancer returning. We used a lower dose of sedation because of her kidneys, and she tolerated the procedure very well.",
            9: "Patient: Sandra Lopez. PROBLEM LIST: Mediastinal lymphadenopathy. History of breast cancer. Chronic kidney disease stage 3. OBJECTIVE: Procedure: EBUS-TBNA. Sedation: Moderate. Findings: Station 2R: sampled x3, ROSE displays metastatic adenocarcinoma. Station 4R: sampled x4, ROSE positive. Station 7: sampled x3, ROSE positive. ASSESSMENT: Metastatic breast cancer verified."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages (calculated from DOB in source)
    # 0: Janet S. Williams, 58 (1967)
    # 1: Elizabeth Chen, 63 (1962)
    # 2: Barbara Kim, 70 (1955)
    # 3: Karen White, 63 (1962)
    # 4: Sarah Chen, 60 (1965)
    # 5: Martin Lee, 65 (1960)
    # 6: Helen Garcia, 67 (1958)
    # 7: Jennifer Wang, 62 (1963)
    # 8: Mark Thompson, 61 (1964)
    # 9: Sandra Lopez, 71 (1954)

    return [
        {"idx": 0, "orig_name": "Janet S. Williams", "orig_age": 58, "names": ["Alice Brown", "Martha Jones", "Kelly Davis", "Joan Miller", "Diane Wilson", "Frances Moore", "Gloria Taylor", "Evelyn Anderson", "Rose Thomas"]},
        {"idx": 1, "orig_name": "Elizabeth Chen", "orig_age": 63, "names": ["Linda Wu", "Susan Chang", "Patricia Liu", "Nancy Yang", "Karen Huang", "Betty Lin", "Helen Zhao", "Sandra Xu", "Donna Ho"]},
        {"idx": 2, "orig_name": "Barbara Kim", "orig_age": 70, "names": ["Carol Park", "Ruth Choi", "Sharon Lee", "Michelle Han", "Laura Jung", "Sarah Kang", "Kimberly Yoon", "Deborah Shin", "Jessica Lim"]},
        {"idx": 3, "orig_name": "Karen White", "orig_age": 63, "names": ["Cynthia Black", "Kathleen Green", "Amy Gray", "Shirley Brown", "Angela Clark", "Helen Lewis", "Anna Walker", "Brenda Hall", "Pamela Allen"]},
        {"idx": 4, "orig_name": "Sarah Chen", "orig_age": 60, "names": ["Mary Zhang", "Patricia Wang", "Jennifer Li", "Linda Zhou", "Elizabeth Chen", "Barbara Wu", "Susan Liu", "Jessica Yang", "Sarah Huang"]},
        {"idx": 5, "orig_name": "Martin Lee", "orig_age": 65, "names": ["John Kim", "David Park", "Robert Choi", "Michael Lee", "William Han", "Richard Jung", "Joseph Kang", "Thomas Yoon", "Charles Shin"]},
        {"idx": 6, "orig_name": "Helen Garcia", "orig_age": 67, "names": ["Margaret Rodriguez", "Dorothy Martinez", "Lisa Hernandez", "Nancy Lopez", "Karen Gonzalez", "Betty Perez", "Helen Sanchez", "Sandra Ramirez", "Donna Torres"]},
        {"idx": 7, "orig_name": "Jennifer Wang", "orig_age": 62, "names": ["Carol Li", "Ruth Zhou", "Sharon Chen", "Michelle Wu", "Laura Liu", "Sarah Yang", "Kimberly Huang", "Deborah Lin", "Jessica Zhao"]},
        {"idx": 8, "orig_name": "Mark Thompson", "orig_age": 61, "names": ["Christopher Harris", "Daniel Clark", "Paul Lewis", "Mark Robinson", "Donald Walker", "George Young", "Kenneth Allen", "Steven King", "Edward Wright"]},
        {"idx": 9, "orig_name": "Sandra Lopez", "orig_age": 71, "names": ["Alice Martinez", "Martha Hernandez", "Kelly Lopez", "Joan Gonzalez", "Diane Perez", "Frances Sanchez", "Gloria Ramirez", "Evelyn Torres", "Rose Flores"]},
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
            
            # Get the specific name
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                note_entry["note_text"] = f"Variation {style_num} for Note {idx} not found."
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
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
                "generated_age": new_age,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_blvr_notes_part_041.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()