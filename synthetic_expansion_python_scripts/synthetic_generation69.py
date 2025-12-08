import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_069.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations from Part 1.
    # Structure: Note_Index (0-5) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Logan Pierce (LUL BLVR)
            1: "Pre-op: LUL emphysema. No collateral ventilation (Chartis).\nAnesthesia: General, 8.0 ETT.\nProcedure:\n- Scope to LUL.\n- Chartis: rapid decay/plateau (CV negative).\n- 4 Zephyr valves deployed: apicoposterior, anterior, lingula.\n- LUL occlusion confirmed.\nFindings: Reduced LUL ventilation, improved diaphragmatic excursion.\nComplications: Minor oozing, stopped w/ saline. No pneumothorax.\nPlan: Extubate. Admit. CXR monitoring.",
            2: "HISTORY OF PRESENT ILLNESS: Mr. Higgins, a 66-year-old gentleman with severe heterogeneous emphysema characterized by marked left upper lobe hyperinflation, presented for elective bronchoscopic lung volume reduction. Preoperative evaluation revealed an intact left oblique fissure and quantitative perfusion demonstrating preservation of the contralateral lung.\nOPERATIVE NARRATIVE: Following the induction of general anesthesia and placement of an 8.0 mm endotracheal tube, the airway was examined. The left bronchial tree was systematically interrogated. A Chartis balloon catheter assessment of the LUL bronchus yielded a CV-negative phenotype (rapid flow decay to zero). Consequently, four Zephyr endobronchial valves were sequentially deployed into the apicoposterior, anterior, and lingular segments. Post-deployment inspection confirmed complete lobar occlusion. Immediate physiological response was noted via improved excursion of the left hemidiaphragm.\nIMPRESSION: Successful LUL BLVR. The patient remained hemodynamically stable and was transferred to the step-down unit for close pneumothorax surveillance.",
            3: "Procedure Justification: Bronchoscopy for lung volume reduction (CPT 31647).\nTechnique:\n1. Access: Flexible bronchoscope introduced through ETT.\n2. Assessment: Chartis catheter inserted into LUL bronchus. Balloon inflated to occlude bronchus. Flow measurements recorded showing absence of collateral ventilation (necessary condition for valve efficacy).\n3. Deployment: Delivery catheter passed through working channel. Four (4) distinct Zephyr valves were sized and deployed into the specific segmental bronchi of the Left Upper Lobe.\n4. Verification: Visual confirmation of valve seating and fluoroscopic confirmation of position performed.\nOutcome: Total occlusion of the target lobe achieved. Codes support single lobe treatment with assessment.",
            4: "Procedure: BLVR LUL\nAttending: Dr. Hart\nSteps:\n1. Time out performed. Patient identified.\n2. Sedation induced (GA). Airway secured with 8.0 ETT.\n3. Scope inserted. Airway anatomy inspected; no secretions.\n4. Chartis assessment performed on LUL; CV negative.\n5. Valves placed: 4 Zephyr valves in LUL segments.\n6. Tolerance: Good. Minimal bleeding at one segment, cold saline applied.\n7. Post-procedure: Extubated. Stable.\nPlan: Admit for pneumothorax watch. Daily CXR.",
            5: "Patient is a 65 year old male here for the lung volume reduction procedure left side uh patient has severe emphysema we used general anesthesia tube size 8 scope went down fine looked at the LUL did the chartis thing and it showed no collateral ventilation so we went ahead. Put in four zephyr valves into the apicoposterior anterior and lingula segments looks like it blocked it off good seen on fluoro too. There was a little bit of bleeding at one spot just put some saline on it and it stopped no pneumothorax right away patient woke up fine sent to step down unit will need xrays to check for lung collapse thanks.",
            6: "Bronchoscopic lung volume reduction with endobronchial valve placement, left upper lobe was performed on Edward Stone, a 68-year-old male with severe heterogeneous emphysema. General anesthesia with endotracheal intubation (8.0 mm ETT) was utilized. High-resolution CT showed severe LUL-predominant emphysema and intact left oblique fissure. Chartis balloon catheter deployed in the left upper lobe bronchus showed rapid flow decay to zero with plateau, consistent with absence of collateral ventilation. Under general anesthesia, a therapeutic flexible bronchoscope was advanced. Four Zephyr endobronchial valves were placed sequentially in the apicoposterior, anterior, and lingular segmental bronchi to completely occlude the LUL. Valve positions were confirmed bronchoscopically and with fluoroscopy. Minimal self-limited oozing occurred. The patient was extubated and transferred to the step-down unit for post-BLVR monitoring.",
            7: "[Indication]\nSymptomatic severe COPD/emphysema with LUL-predominant disease, hyperinflation, candidate for BLVR.\n[Anesthesia]\nGeneral anesthesia, 8.0 mm ETT.\n[Description]\nScope advanced. LUL identified. Chartis assessment: rapid decay/zero flow (No CV). Four Zephyr valves deployed in LUL (apicoposterior, anterior, lingular). Occlusion confirmed via fluoro and visual inspection. Reduction in LUL ventilation noted. Minimal bleeding treated with cold saline.\n[Plan]\nMonitor for pneumothorax (72 hours). Serial CXRs. Resume rehab.",
            8: "The patient, a 67-year-old male with severe heterogeneous emphysema, was brought to the bronchoscopy suite for elective lung volume reduction. After induction of general anesthesia and intubation, the procedure commenced. We advanced the bronchoscope to the left upper lobe. A Chartis assessment was utilized to ensure there was no collateral ventilation, which was confirmed by rapid flow decay. Following this confirmation, we proceeded to place four Zephyr valves into the target segments. Verification was performed using both direct visualization and fluoroscopy, which showed good placement and reduced ventilation to the lobe. The patient tolerated the procedure well with only minor oozing that resolved with saline. He was extubated and transferred for monitoring.",
            9: "Operation: Bronchoscopic lung volume reduction with endobronchial valve implantation, left upper lobe.\nSubject: Gary Wright, 69-year-old male.\nDetails: Under general anesthesia, the scope was navigated through the ETT. The LUL bronchus was isolated. Chartis evaluation indicated a lack of collateral ventilation. A delivery system was then inserted, and four Zephyr endobronchial valves were deposited sequentially in the apicoposterior, anterior, and lingular segmental bronchi to seal the LUL. Valve locations were verified bronchoscopically. There was visible diminution in LUL ventilation.\nAftermath: Minimal oozing managed with cold saline. No immediate pneumothorax.\nStrategy: Observe for post-procedure pneumothorax."
        },
        1: { # Patricia Morales (RUL BLVR)
            1: "Dx: Severe RUL emphysema.\nAnesthesia: GA, LMA #4.\nAction: RUL cannulated. Chartis = No CV.\nImplants: 3 Zephyr valves (Apical, Posterior, Anterior).\nResult: Reduced RUL ventilation. Modest mediastinal shift.\nIssue: Transient hypoxemia during deployment, fixed with FiO2/recruitment.\nPlan: PACU -> Monitored bed. CXR x3 days.",
            2: "INDICATION: Mrs. Carter, a 62-year-old female with severe, refractory COPD and RUL-predominant emphysematous changes, presented for intervention.\nPROCEDURE: The patient was placed under general anesthesia using a laryngeal mask airway. The right bronchial tree was systematically mapped. Collateral ventilation was assessed via the Chartis system in the RUL, demonstrating a 'low flow/no plateau' phenotype consistent with fissure integrity. Subsequently, three Zephyr endobronchial valves were deployed in the apical, posterior, and anterior segments.\nOUTCOME: Post-deployment fluoroscopy confirmed appropriate valve positioning. Clinical examination revealed decreased ventilation to the target lobe. A transient episode of hypoxemia occurred intraoperatively, which responded promptly to recruitment maneuvers and increased fraction of inspired oxygen.",
            3: "Service: Bronchoscopy with Valve Placement (31647).\nTarget: Right Upper Lobe (RUL).\nDevice utilization: 3 Zephyr Endobronchial Valves.\nDiagnostic component: Chartis system used to rule out collateral ventilation prior to placement (included in primary code).\nImaging: Fluoroscopy used for guidance (7.0 min).\nComplication management: Transient hypoxemia managed with ventilator adjustments; no separate procedure code required.\nStatus: Procedure successful, target lobe occluded.",
            4: "Resident Note\nPatient: Karen Smith, 65F.\nProcedure: RUL BLVR.\nStaff: Dr. Wells.\nSteps:\n1. LMA placed.\n2. Bronch to RUL.\n3. Chartis check: Negative for CV.\n4. Deployed 3 valves (Zephyr) to RUL segments.\n5. Checked position with fluoro.\nEvents: Sats dropped during deployment, brought back up with FiO2. No other issues.\nPlan: Admit, daily CXR to watch for pneumo.",
            5: "Procedure note for Barbara Lopez she has bad emphysema RUL predominant we did the valve placement today anesthesia was general with an LMA size 4. Went into the right lung RUL chartis showed no collateral ventilation so good candidate. Put in three valves total apical posterior anterior zephyr type. She desatted a bit in the middle there but we bagged her and turned up the oxygen and she was fine. Valves look good fluoro confirmed it no bleeding really. Sending her to monitored bed check cxr for pneumothorax thanks.",
            6: "Bronchoscopic lung volume reduction with endobronchial valve placement, right upper lobe. Patient is a 63-year-old female with severe COPD. General anesthesia with laryngeal mask airway was used. Chartis assessment performed in the RUL bronchus demonstrated rapid flow decline to zero, consistent with absence of collateral ventilation. Three Zephyr endobronchial valves were deployed in the apical, posterior, and anterior segmental bronchi. Valve positions were verified bronchoscopically and fluoroscopically. There was decreased ventilation to the RUL and modest mediastinal shift toward the treated side. Transient mild hypoxemia occurred during valve deployment, resolved with increased FiO2. No immediate pneumothorax was noted on post-procedure CXR.",
            7: "[Indication]\nSymptomatic severe emphysema, RUL hyperinflation, exercise limitation.\n[Anesthesia]\nGeneral, LMA size 4.\n[Description]\nRUL cannulated. Chartis confirmed absence of collateral ventilation. Three Zephyr valves placed (apical, posterior, anterior). Fluoroscopic verification performed. Decreased RUL ventilation noted.\n[Complications]\nTransient mild hypoxemia, resolved.\n[Plan]\nMonitored bed 48-72h. Daily CXR x3. Outpatient f/u 4-6 weeks.",
            8: "Mrs. Lewis underwent RUL lung volume reduction today. After securing the airway with an LMA, we advanced the bronchoscope and confirmed the absence of collateral ventilation in the right upper lobe using the Chartis system. We then proceeded to place three Zephyr valves in the segmental bronchi. Visual and fluoroscopic inspection confirmed the valves were well-seated. During the deployment, the patient experienced mild transient hypoxemia, but this was quickly corrected by adjusting the oxygen levels and performing recruitment maneuvers. The patient recovered well in the PACU.",
            9: "Procedure: Flexible bronchoscopy with installation of endobronchial valves, right upper lobe.\nPatient: Betty King.\nDetails: A therapeutic flexible bronchoscope was guided via the LMA. The right bronchial tree was examined and the RUL bronchus entered. Chartis analysis confirmed appropriateness for BLVR. Three Zephyr endobronchial valves were then positioned in the apical, posterior, and anterior segmental bronchi. Valve locations were authenticated bronchoscopically. There was diminished ventilation to the RUL.\nAdverse Events: Temporary mild hypoxemia during valve insertion, rectified with increased FiO2."
        },
        2: { # Ethan Cole (Valve Removal RUL)
            1: "Indication: Persistent pneumothorax/air leak 5 days post-BLVR.\nProcedure: Valve Removal RUL.\nFindings: 3 Zephyr valves visualized, good seating. Large air leak present.\nAction: All 3 valves removed via forceps.\nResult: Bronchi patent. Mild edema. Air leak decreased immediately.\nPlan: Maintain chest tube. Daily CXR.",
            2: "REASON FOR PROCEDURE: Mr. Turner, status post RUL BLVR, developed a significant right-sided pneumothorax with a persistent bronchopleural fistula despite thoracostomy drainage.\nPROCEDURE NOTE: Under general anesthesia, the airway was re-accessed. The previously placed Zephyr valves in the RUL were identified. Given the clinical failure to resolve the pneumothorax, the decision was made to abort the volume reduction. All three valves were sequentially grasped and extracted utilizing valve retrieval forceps. Inspection of the bronchial mucosa revealed mild inflammatory changes but no trauma.\nPOST-PROCEDURE COURSE: The air leak volume diminished significantly following extraction. The patient was returned to the step-down unit for continued chest tube management.",
            3: "CPT Code: 31648 (Bronchoscopy with removal of bronchial valves).\nLocation: Right Upper Lobe (Initial lobe).\nDetails:\n- Bronchoscope inserted.\n- Identification of foreign bodies (3 valves).\n- Removal of 3 valves using specialized forceps.\n- Re-inspection of airway.\nMedical Necessity: Complication of prior procedure (Pneumothorax with persistent air leak).",
            4: "Procedure: RUL Valve Removal\nPatient: Joseph Anderson, 70M\nHx: RUL BLVR 5 days ago -> Pneumothorax -> Chest tube -> Persistent leak.\nSteps:\n1. Intubation (8.0 ETT).\n2. Scope down. Saw 3 valves in RUL.\n3. Removed all 3 using forceps. Came out easy.\n4. Checked airway, mild oozing, used epi/saline.\n5. Air leak got better.\nPlan: Keep chest tube, watch air leak.",
            5: "Mr Mitchell is here for valve removal he had the procedure last week and got a pneumothorax chest tube isnt fixing the air leak so we took them out. General anesthesia tube in. Went in saw the three valves in the RUL. Grabbed them with the forceps and pulled them out one by one no problem. Little bit of bleeding put some epinephrine on it. Air leak looked better on the vac. Sending him back to step down keep the chest tube in for now thanks.",
            6: "Flexible bronchoscopy with removal of endobronchial valves, right upper lobe, for post-BLVR pneumothorax. Patient is a 70-year-old male. Large right pneumothorax with persistent air leak was the indication. Three Zephyr valves were visualized in the RUL segmental bronchi. All three valves were removed sequentially using dedicated valve retrieval forceps. Each valve was grasped, collapsed, and withdrawn. Mild oozing from one segmental takeoff controlled with topical epinephrine. Air leak decreased after valve removal. Returned to step-down unit with chest tube on suction.",
            7: "[Indication]\nLarge right pneumothorax, persistent air leak post-RUL BLVR.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nRUL inspected. 3 valves found. All 3 removed via retrieval forceps. Bronchi patent post-removal. Mild edema noted.\n[Complications]\nMild oozing, controlled with epi/saline.\n[Plan]\nMonitor chest tube output. Daily CXR. No further BLVR on right side.",
            8: "Because Mr. Roberts suffered a persistent pneumothorax following his recent BLVR, we proceeded with valve removal today. Under general anesthesia, we visualized the three Zephyr valves in the right upper lobe. Using forceps, we carefully removed each valve. The airways looked a bit swollen but were otherwise fine. We noted a decrease in the air leak almost immediately after the valves were out. We controlled a small amount of bleeding with epinephrine and sent him to recovery with his chest tube still in place.",
            9: "Procedure: Flexible bronchoscopy with extraction of endobronchial valves.\nContext: Large right pneumothorax with continuous air leak.\nAction: Three Zephyr valves were observed in the RUL. Given the ongoing pneumothorax, all three valves were retrieved sequentially. Each valve was clutched, collapsed, and extracted through the bronchoscope.\nResult: The underlying segmental bronchi were open. Air leak lessened after valve withdrawal."
        },
        3: { # Renee Thompson (Valve Removal LLL)
            1: "Indication: Delayed pneumothorax (Day 14 post-BLVR). Persistent leak.\nProcedure: Removal of 4 valves LLL.\nFindings: Valves in superior and basilar segments.\nAction: Forceps removal of all valves.\nOutcome: Improved LLL expansion on post-op CXR.\nPlan: Water seal trial when leak stops.",
            2: "HISTORY: Mrs. Campbell presented with a delayed pneumothorax two weeks following LLL valve placement. Despite chest tube thoracostomy, the lung failed to fully re-expand, suggesting a valvular mechanism or persistent parenchymal leak.\nPROCEDURE: The patient was intubated. Bronchoscopic inspection revealed four Zephyr valves seated in the LLL. To facilitate lung re-expansion, the decision was made to retrieve the devices. All four valves were successfully extracted without complication. Inspection of the bronchial mucosa showed expected post-implantation inflammatory changes but no purulence.\nCONCLUSION: Successful retrieval of LLL valves. Post-procedure imaging demonstrates improved aeration of the left lower lobe.",
            3: "Code: 31648 (Removal of bronchial valves).\nSite: Left Lower Lobe.\nQuantity: 4 valves removed.\nIndication: Complication (Pneumothorax J93.11) refractory to chest tube.\nNote: Procedure performed under General Anesthesia. Fluoroscopy used (3.5 min). No new valves placed (excludes 31647).",
            4: "Procedure: Valve Removal LLL\nPatient: Jennifer Young, 57F\nIndication: Recurrent pneumo 2 weeks after BLVR.\nSteps:\n1. ETT 7.5 placed.\n2. Found 4 valves in LLL.\n3. Used forceps to pull them all out.\n4. No bleeding.\nPlan: Back to floor. Chest tube to suction -20. Watch for leak to stop.",
            5: "Patient is Renee Thompson no wait Linda Hernandez 61 female. She had valves put in the LLL two weeks ago came back with a pneumo. Chest tube not working great so we took the valves out today. Four of them total using the grasp forceps. No bleeding really. Lung looks better on the xray chest tube still in. Will try water seal later when the air leak stops.",
            6: "Flexible bronchoscopy with removal of endobronchial valves, left lower lobe, for delayed post-BLVR pneumothorax. Patient is a 59-year-old female. Recurrent symptomatic left pneumothorax with persistent air leak was the indication. Four Zephyr valves were visualized in the basilar and superior segmental bronchi of the LLL. All four valves were removed sequentially using valve retrieval forceps. Each valve was collapsed and withdrawn. The underlying bronchi demonstrated mild inflammatory changes. No significant bleeding. Post-procedure CXR showed improved LLL expansion.",
            7: "[Indication]\nDelayed pneumothorax (2 weeks post-op), persistent air leak.\n[Anesthesia]\nGeneral, 7.5 ETT.\n[Description]\n4 Zephyr valves identified in LLL. Sequential removal performed using forceps. Mucosa inflamed but intact.\n[Complications]\nNone.\n[Plan]\nDaily CXR. Trial water seal when leak decreases.",
            8: "Ms. Scott came in with a collapsed lung two weeks after her valve procedure. The chest tube wasn't clearing the air leak, so we went in to take the valves out. Under general anesthesia, we found all four valves in the left lower lobe. We used forceps to remove them one by one. There wasn't any bleeding, and the x-ray right after showed the lung was already expanding better. She's back on the floor with the chest tube for now.",
            9: "Procedure: Flexible bronchoscopy with elimination of endobronchial valves.\nIndication: Recurring left pneumothorax.\nAction: Four Zephyr valves were spotted in the LLL. Given the continuous air leak, all four valves were withdrawn sequentially. Each valve was collapsed and pulled through the scope. The underlying bronchi showed mild inflammatory changes.\nOutcome: Improved LLL inflation with the chest tube in place."
        },
        4: { # Marcus Hill (Valve Adjustment RUL)
            1: "Indication: Suboptimal RUL volume reduction. CT shows persistent aeration posterior segment.\nAnesthesia: MAC (Propofol/Dex). LMA #4.\nFindings: Posterior valve proximal/leaking. Apical/Anterior good.\nAction: Removed posterior valve. Replaced with larger Zephyr valve distally. Adjusted apical valve.\nResult: Complete occlusion of RUL.\nPlan: CT in 6-8 weeks. PFTs 3 mos.",
            2: "INDICATION: Mr. Edwards presented for revision bronchoscopy due to incomplete lobar atelectasis six weeks following RUL valve placement. Radiographic review suggested a paravalvular leak in the posterior segment.\nPROCEDURE: Under monitored anesthesia care, the RUL was interrogated. The posterior valve was noted to be malpositioned proximally, allowing collateral airflow. This valve was extracted. A resized, larger Zephyr valve was deployed more distally to ensure a seal. Additionally, the apical valve was repositioned to optimize occlusion.\nIMPRESSION: Successful revision of RUL BLVR. Total lobar occlusion is now visually confirmed.",
            3: "Coding Summary:\n- 31648: Removal of bronchial valve (Posterior segment valve removed due to malposition).\n- 31647: Insertion of bronchial valve (New valve placed in posterior segment; Apical valve adjusted/replaced).\nRationale: Procedure involved both removal of existing hardware and placement of new hardware in the *same* initial target lobe (RUL) to achieve therapeutic effect.\nModifiers: None required for facility setting.",
            4: "Procedure: RUL Valve Revision\nPatient: Charles Martin, 67M\nSteps:\n1. MAC anesthesia. LMA.\n2. Looked at RUL. Posterior valve looked loose (air leak).\n3. Took out posterior valve.\n4. Put in a new bigger valve deeper in.\n5. Tweaked the apical valve too.\n6. Everything looks blocked off now.\nPlan: Discharge to home/floor. Re-scan in 2 months.",
            5: "Marcus Hill no sorry Donald Thompson here for valve check. He had them put in 6 weeks ago but the lung didnt collapse all the way. We went in with MAC anesthesia. Saw the posterior valve was slipping air getting around it. Pulled it out put a new one in deeper larger size. Also moved the apical one a bit. Looks good now tight seal. No bleeding patient woke up fine. Check CT in a couple months.",
            6: "Flexible bronchoscopy with adjustment and replacement of endobronchial valves, right upper lobe. Patient is a 66-year-old male. Suboptimal lobar volume reduction was the indication. The posterior valve was slightly proximal with visible ventilation around the valve. The posterior valve was removed using valve retrieval forceps. A new, slightly larger Zephyr valve was then deployed more distally. The apical valve was briefly removed and reinserted. Final inspection showed all RUL segmental orifices fully occluded.",
            7: "[Indication]\nIncomplete atelectasis RUL post-BLVR.\n[Anesthesia]\nMAC, LMA.\n[Description]\nPosterior valve identified as source of leak (malposition). Removed via forceps. Replaced with larger valve distally. Apical valve adjusted. Complete occlusion achieved.\n[Plan]\nOvernight obs. CT 6-8 weeks. PFTs 3 months.",
            8: "Mr. Robinson came back because his right upper lobe didn't shrink as much as we hoped after the first procedure. We took a look and saw the valve in the posterior segment wasn't sitting right—air was getting around it. We took that one out and put in a bigger one, placing it a bit deeper to get a better seal. We also adjusted the valve in the top segment just to be safe. Everything looks totally blocked off now, which is what we want.",
            9: "Procedure: Flexible bronchoscopy with modification and exchange of endobronchial valves.\nIssue: Deficient lobar volume reduction.\nAction: The posterior valve was withdrawn. A new Zephyr valve was implanted more distally. The apical valve was briefly extracted and re-seated. Final survey showed all RUL segmental orifices fully blocked.\nOutcome: Minimal mucosal oozing."
        },
        5: { # Alison Reed (Valve Replacement LUL)
            1: "Indication: Patient coughed up valve. Symptoms returned.\nSedation: Moderate (Midazolam/Fentanyl).\nFindings: Apicoposterior segment open (valve missing). Anterior valve loose.\nAction: Removed loose anterior valve -> Replaced with new valve. Placed new valve in empty Apicoposterior segment.\nResult: LUL fully occluded (3 valves total).\nPlan: D/C home. Clinic f/u 4-6 wks.",
            2: "HISTORY: Ms. Nelson reported expectoration of an endobronchial prosthesis followed by worsening dyspnea 3 months post-LUL BLVR.\nPROCEDURE: Bronchoscopic inspection confirmed the absence of the valve in the apicoposterior segment. Additionally, the anterior segmental valve was noted to be migrating proximally with peri-valvular leak. The anterior valve was retrieved and replaced with a correctly sized unit. A de novo valve was deployed into the patent apicoposterior segment.\nCONCLUSION: Restoration of complete lobar occlusion.",
            3: "Codes:\n- 31648: Removal of loose anterior valve.\n- 31647: Placement of valves in LUL (Replacement of anterior + Replacement of expectorated apicoposterior).\nJustification: Procedure required both removal of failing hardware and insertion of new devices to restore therapeutic effect in the initial target lobe.\nSetting: Bronchoscopy suite, Moderate Sedation.",
            4: "Procedure: LUL Valve Replacement\nPatient: Carol Mitchell, 61F\nHx: Coughed up valve at home.\nSteps:\n1. Mod sed.\n2. Scope in. Saw apicoposterior bronchus was empty.\n3. Anterior valve looked loose, so we pulled it out (31648).\n4. Put new valves in Anterior and Apicoposterior segments (31647).\n5. Good seal on all 3 segments now.\nPlan: Home today.",
            5: "Alison Reed or wait Sharon Roberts here. She coughed up a valve last week feeling short of breath. We took a look with the scope under moderate sedation. The apicoposterior segment was wide open valve gone. The anterior one looked loose too so we took that out. Put two new valves in one for the anterior one for the apicoposterior. Looks tight now. No bleeding. She can go home today thanks.",
            6: "Flexible bronchoscopy with replacement of expectorated endobronchial valve and optimization of valve set, left upper lobe. Patient is a 61-year-old female. Suspected valve loss after coughing up a valve. One segmental bronchus (apicoposterior) was open without a valve. The proximal anterior valve was removed with retrieval forceps. A new Zephyr valve was deployed more distally in the anterior segment. A second new valve was deployed in the apicoposterior segment. Final inspection showed three LUL segmental bronchi fully occluded.",
            7: "[Indication]\nExpectorated valve, recurrent dyspnea.\n[Anesthesia]\nModerate Sedation.\n[Description]\nMissing valve apicoposterior segment. Loose valve Anterior segment. Loose valve removed. New valves placed in Anterior and Apicoposterior. LUL sealed.\n[Plan]\nDischarge home. Clinic 4-6 weeks.",
            8: "Ms. Evans came in because she actually coughed up one of her valves at home and started feeling short of breath again. We went in with the scope and saw that the valve for the top back part of the lung was indeed missing. We also noticed the one in the front part was loose, so we decided to replace that one too while we were there. We put two brand new valves in, and now everything is sealed up tight again. She did great and went home the same day.",
            9: "Procedure: Flexible bronchoscopy with substitution of expectorated endobronchial valve.\nReason: Presumed valve loss.\nFindings: One segmental bronchus was vacant. One valve appeared unstable.\nAction: The unstable valve was extracted. A new Zephyr valve was anchored more distally. A second new valve was implanted in the vacant segment.\nResult: Three LUL segmental bronchi fully obstructed."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the prompt's examples
    # (In a real script, this data comes from reading the source JSON)
    return [
        {"idx": 0, "orig_name": "Logan Pierce", "orig_age": 67, "names": ["John Vance", "Arthur Higgins", "Robert Kinsley", "William O'Connor", "James P. Miller", "Edward Stone", "Richard Davis", "Thomas Clark", "Gary Wright"]},
        {"idx": 1, "orig_name": "Patricia Morales", "orig_age": 63, "names": ["Sarah Jenkins", "Linda Carter", "Nancy Hughes", "Karen Smith", "Barbara Lopez", "Mary Ann Davidson", "Susan White", "Margaret Lewis", "Betty King"]},
        {"idx": 2, "orig_name": "Ethan Cole", "orig_age": 70, "names": ["Michael Foster", "Robert G. Turner", "David Myers", "Joseph Anderson", "Frank Mitchell", "Paul Reynolds", "George Baker", "Kenneth Roberts", "Steven Phillips"]},
        {"idx": 3, "orig_name": "Renee Thompson", "orig_age": 59, "names": ["Marie Hall", "Patricia Campbell", "Elizabeth Allen", "Jennifer Young", "Linda Hernandez", "Barbara King", "Dorothy Wright", "Helen Scott", "Carol Green"]},
        {"idx": 4, "orig_name": "Marcus Hill", "orig_age": 65, "names": ["James Carter", "William Edwards", "Thomas Harris", "Charles Martin", "Donald Thompson", "Mark Garcia", "Paul Martinez", "George Robinson", "Kenneth Clark"]},
        {"idx": 5, "orig_name": "Alison Reed", "orig_age": 61, "names": ["Betty Adams", "Sandra Nelson", "Donna Carter", "Carol Mitchell", "Sharon Roberts", "Brenda Phillips", "Pamela Campbell", "Deborah Evans", "Laura Turner"]},
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
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            note_entry["note_text"] = variations_text[idx][style_num]
            
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
    output_filename = output_dir / "synthetic_blvr_notes_part_069.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()