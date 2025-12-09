import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_018.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILENAME = "synthetic_notes_part_018.json"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Defines the base patient data found in part_018 and provides 
    9 mock names for the synthetic variations.
    """
    return [
        { # 0: Maria Lopez (BLVR RUL + Pneumo/Chest Tube)
            "idx": 0, 
            "orig_name": "Maria Lopez", 
            "orig_age": 64, 
            "names": ["Elena Rodriguez", "Carmen Ortiz", "Lucia Fernandez", "Isabella Martinez", "Rosa Garcia", "Sofia Rivera", "Teresa Chavez", "Ana Torres", "Paula Diaz"]
        },
        { # 1: Steven Brooks (Aborted BLVR LUL - CV+)
            "idx": 1, 
            "orig_name": "Steven Brooks", 
            "orig_age": 70, 
            "names": ["Arthur Miller", "Harold Davis", "Richard Wilson", "Walter Thomas", "Frank White", "Henry Harris", "Edward Martin", "Charles Thompson", "Raymond Clark"]
        },
        { # 2: Jason Phillips (WLL Right - Full)
            "idx": 2, 
            "orig_name": "Jason Phillips", 
            "orig_age": 39, 
            "names": ["Kevin Scott", "Brian Adams", "Matthew Nelson", "Timothy Carter", "Jeffrey Roberts", "Daniel Lee", "Christopher Walker", "Ryan Hall", "Justin Allen"]
        },
        { # 3: Lauren Young (WLL Left - Partial/Aborted)
            "idx": 3, 
            "orig_name": "Lauren Young", 
            "orig_age": 46, 
            "names": ["Rachel King", "Melissa Wright", "Stephanie Hill", "Nicole Green", "Amanda Baker", "Rebecca Adams", "Jennifer Campbell", "Jessica Mitchell", "Ashley Roberts"]
        },
        { # 4: Michael James (Foreign Body - Chicken Bone)
            "idx": 4, 
            "orig_name": "Michael James", 
            "orig_age": 45, 
            "names": ["David Turner", "James Parker", "Robert Edwards", "William Collins", "Joseph Stewart", "Thomas Sanchez", "Charles Morris", "Christopher Rogers", "Daniel Reed"]
        },
        { # 5: Ava Thompson (Foreign Body - Pen Cap - Pediatric)
            "idx": 5, 
            "orig_name": "Ava Thompson", 
            "orig_age": 6, 
            "names": ["Mia Johnson", "Olivia Brown", "Sophia Davis", "Isabella Miller", "Charlotte Wilson", "Amelia Moore", "Harper Taylor", "Evelyn Anderson", "Abigail Thomas"]
        },
        { # 6: Sarah Mitchell (Bronchial Thermoplasty LLL - Full)
            "idx": 6, 
            "orig_name": "Sarah Mitchell", 
            "orig_age": 42, 
            "names": ["Emily Robinson", "Laura Wood", "Sarah Jackson", "Kimberly Lewis", "Michelle Harris", "Amy Clark", "Lisa Walker", "Angela Hall", "Melissa Allen"]
        },
        { # 7: David Nguyen (Bronchial Thermoplasty RLL - Aborted)
            "idx": 7, 
            "orig_name": "David Nguyen", 
            "orig_age": 50, 
            "names": ["Paul Tran", "Mark Hoang", "John Pham", "Peter Le", "Andrew Vu", "Steven Dang", "Michael Do", "Kevin Vo", "Brian Huynh"]
        },
        { # 8: Patricia Foster (Medical Thoracoscopy)
            "idx": 8, 
            "orig_name": "Patricia Foster", 
            "orig_age": 62, 
            "names": ["Barbara Kelly", "Susan Sanders", "Linda Price", "Karen Bennett", "Nancy Wood", "Betty Barnes", "Sandra Ross", "Donna Henderson", "Carol Coleman"]
        },
        { # 9: William Carter (Thoracentesis + Pneumo)
            "idx": 9, 
            "orig_name": "William Carter", 
            "orig_age": 79, 
            "names": ["Robert Hughes", "James Patterson", "John Simmons", "Michael Foster", "William Bryant", "David Alexander", "Richard Russell", "Joseph Griffin", "Thomas Hayes"]
        }
    ]

def get_variations():
    """
    Returns a dictionary of stylistic variations for each note index.
    Structure: Note_Index -> Style_Index -> Text
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
        0: { # Maria Lopez (BLVR RUL + Pneumo)
            1: "Indication: RUL Emphysema.\nProcedure: RUL BLVR + Chest Tube.\nSteps:\n- GA, 8.5 ETT.\n- Chartis RUL: No CV (Flow=0).\n- 4 Zephyr valves placed (RB1-RB3, RB4+5).\n- Post-op CXR: Pneumothorax.\n- 14Fr pigtail placed to water seal.\nPlan: Admit step-down.",
            2: "OPERATIVE SUMMARY: The patient, a 64-year-old female with severe heterogeneous emphysema, underwent elective bronchoscopic lung volume reduction. Following the induction of general anesthesia, the right upper lobe (RUL) was interrogated. Chartis assessment confirmed fissure integrity (CV negative). Consequently, four Zephyr endobronchial valves were deployed to achieve complete lobar occlusion. Immediate post-procedural imaging revealed a right-sided pneumothorax. A 14 French percutaneous pigtail catheter was inserted using the Seldinger technique and placed to water seal. The patient was transferred to the step-down unit for close monitoring.",
            3: "Procedures Performed:\n1. 31647 (Bronchoscopy with valve placement, initial lobe): 4 Zephyr valves deployed in RUL following confirmation of CV negative status via Chartis (bundled).\n2. 32557 (Pleural drainage with imaging guidance): Performed for immediate post-procedure pneumothorax. 14Fr catheter inserted.\nMedical Necessity: Severe emphysema (J43.9) and iatrogenic pneumothorax (J95.811).",
            4: "Resident Note\nPatient: Elena Rodriguez\nAttending: Dr. Watson\nProcedure: BLVR RUL\nSteps:\n1. Intubation (8.5 ETT).\n2. Chartis check of RUL -> Negative for collateral ventilation.\n3. Valves placed: 4 total (Zephyr) in RUL segments.\n4. Complication: Drop in sats/breath sounds. CXR showed pneumo.\n5. Pigtail chest tube placed.\nPlan: Admit, watch air leak.",
            5: "patient maria lopez here for valve placement right upper lobe. we did general anesthesia tube size 8.5. chartis catheter showed no collateral flow so we went ahead. put in four zephyr valves looks like we got good occlusion. did a chest xray right after and saw a pneumothorax so we had to put in a 14 french pigtail chest tube. patient going to step down unit to watch the leak.",
            6: "Bronchoscopic Lung Volume Reduction with endobronchial valve placement was performed on the right upper lobe. The patient is a 64-year-old female with severe emphysema. General anesthesia was used. Chartis evaluation of the RUL showed absence of collateral ventilation. Four Zephyr valves were deployed to occlude RB1, RB2, RB3, and the RB4+5 combined segment. A small right pneumothorax was noted on immediate post-procedure chest radiograph. A 14 Fr pigtail chest tube was inserted and placed to water seal. The patient was admitted for monitoring.",
            7: "[Indication]\nSevere heterogeneous emphysema, RUL target.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nRUL identified. Chartis assessment negative for CV. Four Zephyr valves placed in RUL segments. Complete occlusion verified. Immediate post-op pneumothorax identified.\n[Intervention]\n14 Fr pigtail chest tube placed.\n[Plan]\nAdmit to step-down. Monitor air leak.",
            8: "Ms. Diaz presented for RUL lung volume reduction to treat her severe emphysema. After inducing anesthesia, we confirmed the right upper lobe was a suitable target using the Chartis system, which showed no airflow between lobes. We then placed four Zephyr valves to block off the diseased segments. Unfortunately, the immediate post-procedure x-ray showed a collapsed lung (pneumothorax). We immediately placed a small chest tube to re-expand the lung. She is being admitted to the step-down unit for close observation.",
            9: "Procedure: Endobronchial valve implantation in right upper lobe.\nSubject: Maria Lopez.\nMethod: Under general anesthesia, the RUL was isolated. Collateral ventilation was ruled out. Four Zephyr prostheses were deployed to obstruct the RUL segments. Visual confirmation of blockage was obtained.\nAdverse Event: Immediate pneumothorax detected radiographically.\nRemedy: Insertion of 14 Fr pleural drain.\nDisposition: Step-down unit admission."
        },
        1: { # Steven Brooks (Aborted BLVR - CV+)
            1: "Indication: Severe emphysema, LUL target.\nProc: Bronchoscopy with Chartis.\nFindings:\n- LUL cannulated with Chartis.\n- Continuous flow observed (CV Positive).\n- Procedure aborted. No valves placed.\nComplications: None.\nDisposition: Home.",
            2: "OPERATIVE REPORT: The patient presented for elective bronchoscopic lung volume reduction targeting the left upper lobe. Under general anesthesia, the airway was inspected. The Chartis system was utilized to assess collateral ventilation in the target lobe. The assessment revealed persistent expiratory airflow consistent with a CV-positive status, indicating significant collateral ventilation. As this precludes effective atelectasis with valve therapy, the procedure was aborted. No endobronchial valves were deployed. The patient was extubated and recovered without incident.",
            3: "Code Selection: 31634 (Bronchoscopy with balloon occlusion/Chartis assessment).\nRationale: Procedure was terminated after diagnostic assessment revealed the patient was not a candidate for valve placement due to collateral ventilation. Codes 31647/31648 are NOT applicable as no valves were placed or removed. Evaluation performed under GA.",
            4: "Procedure Note\nPatient: Harold Davis\nProcedure: Aborted BLVR\nReason: LUL emphysema\nSteps:\n1. ETT placed.\n2. Scope to LUL.\n3. Chartis balloon inflated.\n4. Result: Positive for collateral ventilation (flow didn't stop).\n5. Decision made to abort.\n6. Extubated.\nPlan: Clinic f/u to discuss other options.",
            5: "mr brooks here for lung valves left upper lobe. we put him to sleep and went down with the chartis catheter. balloon up in the LUL but the flow just kept coming it never stopped. that means he has collateral ventilation and the valves wont work. so we stopped didn't put any in. woke him up sending him home.",
            6: "Attempted Zephyr valve placement in left upper lobe. Patient is a 70-year-old male with severe emphysema. General anesthesia with 8.0 ETT was used. The target lobe was the Left Upper Lobe. Chartis assessment was performed and revealed persistent airflow consistent with significant collateral ventilation. Based on this finding, BLVR was not performed and no valves were deployed. The airways were irrigated and inspected. There were no complications. The patient was extubated and discharged home.",
            7: "[Indication]\nSevere emphysema, evaluation for LUL BLVR.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nChartis assessment of LUL performed. Result: Significant collateral ventilation (CV+). Procedure aborted. No valves implanted.\n[Plan]\nDischarge to home. Discuss alternative therapies.",
            8: "Mr. Wilson came in hoping to have valves placed in his left upper lung to help with his emphysema. We put him under anesthesia and used the Chartis balloon to test the lung first. Unfortunately, the test showed that air was leaking in from other parts of the lung (collateral ventilation), which means the valves wouldn't work. We decided not to put them in to avoid unnecessary risk. He woke up fine and went home the same day.",
            9: "Procedure: Attempted endobronchial valve installation.\nTarget: Left Upper Lobe.\nOutcome: The Chartis evaluation indicated the presence of collateral ventilation. Consequently, the implantation was cancelled. No prostheses were deployed. \nDisposition: Discharge to outpatient care."
        },
        2: { # Jason Phillips (WLL Right - Full)
            1: "Indication: PAP.\nProc: Right Whole Lung Lavage.\nAirway: 39Fr Left DLT.\nTechnique:\n- Single lung ventilation (Left).\n- Right lung lavaged 32L saline.\n- Effluent cleared (27L return).\nEvents: Transient hypotension (treated).\nPlan: ICU, mech vent.",
            2: "PROCEDURE: Whole Lung Lavage (Right).\nCLINICAL CONTEXT: 39M with autoimmune Pulmonary Alveolar Proteinosis. \nDETAILS: Following induction of general anesthesia, a 39 Fr left-sided double-lumen endotracheal tube was placed and isolation confirmed via bronchoscopy. The patient was placed on single-lung ventilation. The right lung was systematically lavaged with 32 liters of warmed normal saline in 1-liter aliquots. Effluent transitioned from opaque/milky to clear. Total fluid recovery was 27 liters. Hemodynamics were managed with vasopressors for transient hypotension. The patient was transferred to the ICU intubated.",
            3: "Billing Code: 32997 (Total lung lavage, unilateral).\nSpecifics: Right lung treated. Therapeutic washing for alveolar proteinosis. \nResources: 32 Liters saline instilled. DLT used for isolation. Procedure performed under GA in OR setting. Post-op care involves ICU management (separate 99291).",
            4: "Resident Note\nPatient: Matthew Nelson\nProcedure: Right WLL\nAttending: Dr. Owens\n1. 39Fr Left DLT placed. Confirmed w/ scope.\n2. Isolated Right lung.\n3. Poured in 32L warm saline total.\n4. Drained out 27L. Milky -> Clear.\n5. BP dropped a bit, gave pressors.\n6. Kept intubated for ICU.\nPlan: Wean vent.",
            5: "jason phillips here for right lung lavage he has PAP. used a big double lumen tube 39 french left side. ventilated the left washed the right. used about 32 liters of saline draining out the milky stuff until it got clear. got back 27 liters. blood pressure got soft for a minute but fixed it with meds. keeping him on the vent taking him to icu.",
            6: "Right whole lung lavage for pulmonary alveolar proteinosis was performed on a 39-year-old male. General anesthesia with a 39 Fr left-sided double-lumen tube was utilized for single-lung ventilation of the left lung. The right lung was lavaged with warmed saline aliquots of 800–1000 mL. The total instilled volume was 32 L and total effluent was 27 L. The fluid progressively cleared. A brief episode of hypotension was treated with a vasopressor bolus. Oxygenation remained adequate. The patient remained intubated and was transferred to the ICU.",
            7: "[Indication]\nAutoimmune Pulmonary Alveolar Proteinosis (PAP).\n[Anesthesia]\nGeneral, 39Fr Left DLT, Single Lung Ventilation.\n[Description]\nRight lung lavage performed using 32L warm saline. 27L effluent removed (milky to clear). Transient hypotension managed medically.\n[Plan]\nICU admission. Mechanical ventilation.",
            8: "Mr. Roberts underwent a whole lung washing (lavage) of his right lung today to treat his proteinosis condition. We used a special breathing tube to breathe for his left lung while we filled and emptied his right lung with saline. We used a total of 32 liters of fluid, and by the end, the fluid coming out looked much clearer than the milky fluid at the start. His blood pressure dipped once but recovered quickly. He is going to the ICU on a ventilator to recover.",
            9: "Operation: Unilateral total pulmonary lavage (Right).\nIndication: Pulmonary Alveolar Proteinosis.\nMethod: A double-lumen tube permitted isolation of the right lung. 32 liters of saline were instilled and 27 liters retrieved. The effluent demonstrated progressive clearance.\nComplication: Temporary hypotension.\nDisposition: ICU transfer, intubated."
        },
        3: { # Lauren Young (WLL Left - Partial/Aborted)
            1: "Indication: PAP, poor reserve.\nProc: Partial Left Lung Lavage.\nAirway: 37Fr Right DLT.\nCourse:\n- 10L instilled / 8.4L return.\n- Aborted due to high airway pressures + hypoxia (82%).\n- Switched to 2-lung vent.\nDisposition: Extubated to HFNC. ICU.",
            2: "OPERATIVE REPORT: The patient, a 46-year-old female with severe PAP and limited reserve, underwent attempted left whole lung lavage. A right-sided DLT was utilized. Lavage was initiated with 500-800mL aliquots. After 10L instillation, the procedure was terminated due to desaturation to 82% and rising airway pressures in the ventilated lung. Recruitment maneuvers were applied immediately upon converting to two-lung ventilation. The patient stabilized and was extubated to high-flow nasal cannula.",
            3: "Code: 32997 (Total lung lavage).\nModifier: -52 (Reduced Services) could be considered depending on payer policy, though 10L is significant therapeutic volume.\nNarrative: Procedure performed for PAP. Left lung lavaged with 10L saline (partial volume compared to standard). Terminated early due to patient instability (hypoxia/high pressures). DLT management and critical care monitoring provided.",
            4: "Resident Note\nPatient: Nicole Green\nProcedure: Left WLL (Partial)\n1. Right DLT placed.\n2. Started washing left lung.\n3. Got to 10L in, 8.4L out.\n4. Sats dropped to 82% and pressures went up.\n5. Stopped procedure. Bagged patient.\n6. Extubated in OR.\nPlan: ICU, maybe try again later.",
            5: "lauren young for left lung wash she has bad PAP. used a right sided dlt. started washing the left but she didnt tolerate it well. after 10 liters she desatted to 82 and pressures went high. had to stop. sucked out what we could total 8.4 out. switched to both lungs and she got better. extubated to high flow sending to icu.",
            6: "Partial left lung lavage for PAP was performed on a 46-year-old female with poor cardiopulmonary reserve. General anesthesia with a right-sided DLT was used. The left lung was lavaged with 10 L of warm saline in 500–800 mL aliquots. The procedure was terminated early due to rising airway pressures and modest hypoxia. Total return was 8.4 L. Hypoxemia to 82% occurred but responded to recruitment and a switch to two-lung ventilation. The patient was extubated in the OR to high-flow nasal cannula and admitted to the ICU.",
            7: "[Indication]\nPAP with compromised reserve.\n[Anesthesia]\nGeneral, 37Fr Right DLT.\n[Description]\nLeft lung lavage initiated. 10L instilled, 8.4L returned. Procedure aborted early due to intraoperative hypoxia (82%) and high peak pressures. Stability restored with 2-lung ventilation.\n[Plan]\nICU admission on HFNC. Staged approach for future.",
            8: "Ms. Adams has severe protein buildup in her lungs and her oxygen levels are already low, so we had to be careful. We tried to wash her left lung today. We managed to wash it with 10 liters of saline, but we had to stop earlier than planned because her oxygen levels dropped and the pressure in her lungs got too high. We woke her up in the operating room and put her on high-flow oxygen. She is going to the ICU for close watching.",
            9: "Operation: Incomplete sinister pulmonary lavage.\nReason: Alveolar proteinosis.\nCourse: 10 liters of saline were introduced. The intervention was curtailed due to escalating airway pressures and desaturation. Recruitment maneuvers were employed. \nOutcome: Patient extubated to high-flow oxygen. ICU transfer."
        },
        4: { # Michael James (Chicken Bone - Rigid Bronch)
            1: "Indication: Foreign body aspiration (Chicken bone).\nProc: Rigid Bronchoscopy.\nFindings: Bone in LLL superior segment.\nAction: Removed piecemeal w/ rigid forceps + basket. APC to granulation.\nComplication: Transient desat -> Bagged.\nDisposition: Extubated. Obs 4 hrs.",
            2: "OPERATIVE SUMMARY: The patient presented with acute aspiration. Under general anesthesia utilizing jet ventilation, a rigid bronchoscope was introduced. Inspection revealed a sharp osseous foreign body (chicken bone) impacted in the left lower lobe superior segment, surrounded by granulation tissue. The object was extracted piecemeal utilizing optical forceps and a retrieval basket. Argon Plasma Coagulation (APC) was applied to the granulating mucosa to ensure hemostasis. A transient desaturation event occurred but resolved promptly with manual ventilation.",
            3: "Code: 31635 (Bronchoscopy with removal of foreign body).\nTechnique: Rigid bronchoscopy used (allows for larger forceps/better airway control). Foreign body (bone) removed from LLL. APC used for hemostasis (incidental to removal).\nJustification: Acute airway obstruction/aspiration.",
            4: "Resident Note\nPatient: William Collins\nProcedure: Rigid Bronch FB Removal\n1. Rigid scope inserted. Jet vent.\n2. Found chicken bone in LLL superior seg.\n3. Used forceps and basket to get it out in pieces.\n4. APC on the angry tissue.\n5. Sats dropped to 86 briefly, bagged up.\n6. Extubated.\nPlan: Home after observation.",
            5: "michael james ate a chicken wing and choked. ct showed a bone in the left lung. we took him to OR used the rigid scope. found the bone in the LLL superior segment stuck in granulation. pulled it out in pieces with the forceps. burned the granulation with apc. he desatted a bit but came right back up. extubated fine going home later.",
            6: "Rigid bronchoscopy with removal of chicken bone from left lower lobe bronchus. Patient is a 45-year-old male. General anesthesia with rigid adult bronchoscope and jet ventilation was used. A sharp bone fragment was found lodged in the superior segment bronchus of the LLL with surrounding granulation tissue. The bone was removed piecemeal using rigid forceps and basket. Granulation was cauterized with APC. Airways were suctioned clear. There was a brief desaturation to 86%, resolved with bag ventilation. Patient was extubated in OR and observed for 4 hours.",
            7: "[Indication]\nForeign body aspiration (chicken bone).\n[Anesthesia]\nGeneral, Rigid Bronchoscope, Jet Ventilation.\n[Description]\nBone fragment visualized in LLL superior segment. Removed piecemeal using forceps/basket. Granulation tissue treated with APC. Airway cleared.\n[Plan]\nObservation for 4 hours, then discharge.",
            8: "Mr. Sanchez swallowed a chicken bone that went down the wrong pipe. We took him to the operating room and used a rigid metal tube to look into his lungs. We found the bone stuck in the lower left lung. We carefully broke it up and pulled it out using special grabbers. We also treated the irritated tissue around it. He had a short dip in oxygen levels but recovered quickly. He will go home today.",
            9: "Procedure: Rigid endoscopic retrieval of foreign object.\nObject: Avian bone fragment.\nLocation: Left lower lobe, superior segment.\nMethod: The object was extracted piecemeal using rigid instrumentation. Hemostasis of granulation tissue was achieved via argon plasma coagulation.\nStatus: Extubated and stable."
        },
        5: { # Ava Thompson (Pen Cap - Pediatric Rigid)
            1: "Indication: FB Aspiration (Pen cap).\nProc: Pediatric Rigid Bronchoscopy.\nFindings: Cap in Right Mainstem.\nAction: Removed intact w/ optical forceps.\nResult: Airway patent. RUL/RML cleared.\nDisposition: Extubated. Pediatric recovery. D/C home.",
            2: "OPERATIVE REPORT: 6-year-old female presenting with foreign body aspiration. General anesthesia was induced. A pediatric rigid bronchoscope was advanced into the trachea. A hollow plastic pen cap was visualized obstructing the proximal right mainstem bronchus. Using optical grasping forceps, the object was secured and retrieved intact. Subsequent inspection of the RUL and RML revealed patent airways with no residual fragments. The patient was extubated in the operating room.",
            3: "Code: 31635 (Bronchoscopy with removal of foreign body).\nPatient Age: 6 years (Pediatric).\nTechnique: Rigid bronchoscopy required for retrieval of large plastic object (pen cap) to prevent fragmentation and loss of airway. Optical forceps used.",
            4: "Resident Note\nPatient: Mia Johnson\nProcedure: Peds Rigid Bronch FB Removal\n1. GA. Peds rigid scope.\n2. Saw pen cap in Right Mainstem.\n3. Grabbed it with the optical forceps.\n4. Pulled it out whole.\n5. Checked airway again - all clear.\n6. Extubated.\nPlan: Home.",
            5: "little ava swallowed a pen cap at school. we took her to the OR put her to sleep. used the kid size rigid scope. saw the cap in the right mainstem blocking the lung. grabbed it with the optical forceps and pulled the whole thing out. looked back down everything clear. woke her up shes doing great going home.",
            6: "Rigid bronchoscopy with removal of pen cap from right mainstem bronchus was performed on a 6-year-old female. General anesthesia with a pediatric rigid bronchoscope was utilized. A hollow plastic pen cap was found lodged in the proximal right mainstem causing near-complete obstruction of RUL and RML. The foreign body was grasped and removed intact with optical forceps. Airways were suctioned and inspected to the subsegmental level. There were no complications. The patient was extubated in the OR.",
            7: "[Indication]\nPediatric foreign body aspiration (Pen cap).\n[Anesthesia]\nGeneral, Pediatric Rigid Scope.\n[Description]\nPen cap visualized in Right Mainstem Bronchus. Removed intact using optical forceps. Distal airways inspected and patent.\n[Plan]\nDischarge home after recovery.",
            8: "Little Harper inhaled a pen cap at school. We had to put her to sleep and use a rigid tube to look into her lungs. We found the cap blocking the main breathing tube on the right side. We used special tweezers with a camera on them to grab the cap and pull it out in one piece. Her lungs look clear now and she is breathing well.",
            9: "Procedure: Pediatric rigid endoscopic foreign body extraction.\nObject: Plastic writing instrument cap.\nLocation: Right mainstem bronchus.\nAction: The object was seized and withdrawn intact utilizing optical forceps. \nOutcome: Patency restored to RUL and RML. No complications."
        },
        6: { # Sarah Mitchell (BT LLL - Session 2)
            1: "Indication: Severe Asthma. BT Session 2 (LLL).\nProc: Bronchial Thermoplasty.\nAction: 50 activations delivered to LLL segments/subsegments via Alair catheter.\nEvent: Mild bronchospasm -> Albuterol.\nDisposition: Home on prednisone taper.",
            2: "PROCEDURE NOTE: Bronchial Thermoplasty, Session 2. Under deep sedation, a flexible bronchoscope was navigated to the Left Lower Lobe. The Alair system was utilized to deliver radiofrequency energy to the airway smooth muscle. A systematic treatment of all accessible segmental and subsegmental airways was completed, totaling 50 activations. The patient experienced mild reactive bronchospasm which responded promptly to bronchodilator therapy.",
            3: "Code: 31660 (Bronchial thermoplasty, 1 lobe).\nSpecifics: Left Lower Lobe treated. 50 activations.\nMedical Necessity: Severe persistent asthma refractory to biologics. This is the second of three planned sessions.",
            4: "Resident Note\nPatient: Emily Robinson\nProcedure: Bronchial Thermoplasty (LLL)\n1. Deep sedation.\n2. Scope to LLL.\n3. Used BT catheter to burn airways. 50 hits total.\n4. Patient got a little tight (wheezy), gave albuterol.\n5. Better now.\nPlan: D/C home, prednisone.",
            5: "sarah mitchell here for her second thermoplasty session left lower lobe. she has bad asthma. deep sedation. went to the LLL and did the RF treatments. got 50 activations done. she got a bit wheezy so we gave albuterol and she opened up. watched her for 6 hours then sent her home with steroids.",
            6: "Bronchial Thermoplasty Session 2 (left lower lobe) for severe asthma. Patient is a 42-year-old female. Deep sedation with propofol infusion was used. The flexible bronchoscope was advanced to segmental and subsegmental bronchi in the left lower lobe. The bronchial thermoplasty catheter was deployed and RF energy was delivered per protocol. Total activations delivered: 50. Mild transient bronchospasm occurred and was treated with nebulized albuterol. No intubation was required. Patient was discharged home on a prednisone taper.",
            7: "[Indication]\nSevere Asthma (Session 2/3).\n[Anesthesia]\nDeep sedation (Propofol).\n[Description]\nBronchial Thermoplasty performed on LLL. 50 RF activations delivered to segmental/subsegmental airways. Mild bronchospasm treated with bronchodilators.\n[Plan]\nDischarge home. Prednisone taper. Session 3 in 3 weeks.",
            8: "Ms. Walker came in for her second bronchial thermoplasty treatment for her asthma, focusing on the lower left lung. We used a special catheter to apply heat to the airway walls to reduce the muscle thickness. We performed 50 treatments in that area. She had a little bit of asthma tightening during the procedure, but a nebulizer treatment fixed it right away. She went home after a few hours of monitoring.",
            9: "Procedure: Bronchial thermoplasty, second session.\nTarget: Left Lower Lobe.\nMethod: Radiofrequency energy was applied to the bronchial smooth muscle via the Alair catheter. 50 activations were completed.\nAdverse Event: Transient bronchoconstriction, resolved pharmacologically.\nDisposition: Outpatient discharge."
        },
        7: { # David Nguyen (Aborted BT RLL - Session 1)
            1: "Indication: Severe Asthma. BT Session 1 (RLL).\nCourse: Procedure started. 12 activations to RLL basal segs.\nComplication: Severe bronchospasm + Hypoxia.\nAction: Procedure aborted. Intubated.\nDisposition: ICU admit.",
            2: "OPERATIVE REPORT: The patient presented for the initial session of Bronchial Thermoplasty targeting the Right Lower Lobe. Following the delivery of 12 activations to the basal segments, the patient developed an acute, severe asthma exacerbation characterized by refractory bronchospasm and desaturation. The therapeutic procedure was immediately aborted. Emergent endotracheal intubation was required to secure the airway and facilitate mechanical ventilation. The patient was transferred to the Intensive Care Unit.",
            3: "Code: 31660 (Bronchial thermoplasty, 1 lobe).\nModifier: -53 (Discontinued Procedure) or -74 depending on facility guidelines, though meaningful therapy (12 activations) was delivered before life-threatening complication arose.\nContext: Procedure converted to critical care management (99291) due to respiratory failure.",
            4: "Resident Note\nPatient: Paul Tran\nProcedure: Attempted BT RLL\n1. Started RLL treatments.\n2. Got 12 activations done.\n3. Patient clamped down hard. Sats dropped.\n4. Couldn't break it with meds.\n5. Had to intubate.\n6. Procedure stopped.\nPlan: ICU.",
            5: "david nguyen here for first thermoplasty RLL. started the procedure got about 12 burns done and then he just locked up. severe bronchospasm sats dropped. we tried everything but had to intubate him. stopped the procedure obviously. taking him to the icu to manage the asthma attack.",
            6: "Bronchial Thermoplasty Procedure Note (Aborted). Session 1 (right lower lobe). Patient is a 50-year-old male with severe steroid-dependent asthma. Moderate sedation was used. After initial BT activations in RLL basal segments (12 activations delivered), the patient developed severe bronchospasm and hypoxia despite bronchodilator therapy. The procedure was aborted and no further activations were performed. Acute asthma exacerbation required intubation and mechanical ventilation. Patient was transferred to ICU.",
            7: "[Indication]\nSevere Asthma (Session 1).\n[Anesthesia]\nModerate -> General (Emergent Intubation).\n[Description]\nBT initiated in RLL (12 activations). Procedure complicated by severe refractory bronchospasm and hypoxia. Procedure aborted. Patient intubated.\n[Plan]\nICU admission for mechanical ventilation and asthma management.",
            8: "Mr. Vo came in for his first heat treatment for asthma. We started on the right lower lung, but after only 12 treatments, his lungs had a severe spasm and clamped shut. We couldn't get them to open with just medicine, so we had to put a breathing tube in and stop the procedure to keep him safe. He is currently in the ICU on a ventilator.",
            9: "Procedure: Initiated bronchial thermoplasty.\nTarget: Right Lower Lobe.\nComplication: Intraprocedural status asthmaticus and hypoxic respiratory failure.\nIntervention: The procedure was halted after 12 activations. Emergent intubation was performed.\nDisposition: Critical care admission."
        },
        8: { # Patricia Foster (Medical Thoracoscopy)
            1: "Indication: Right pleural effusion, r/o TB vs Ca.\nProc: Medical Thoracoscopy.\nTechnique:\n- Local/Sedation.\n- 1200mL straw fluid drained.\n- Pleuroscopy: Diffuse fibrin, small nodules.\n- Biopsy: Parietal pleura x multiple.\n- No talc.\nDisposition: Chest tube to water seal. Admit.",
            2: "PROCEDURE NOTE: Diagnostic Medical Thoracoscopy. \nINDICATIONS: Undiagnosed exudative right pleural effusion. \nFINDINGS: Upon entry into the right pleural space, 1.2L of serous fluid was evacuated. Inspection via semi-rigid thoracoscope revealed diffuse fibrinous adhesions and nodularity of the parietal pleura. Targeted biopsies were obtained for histopathology and microbiological analysis (TB). Chemical pleurodesis was deferred pending diagnosis. A chest tube was placed.",
            3: "Code: 32602 (Thoracoscopy, diagnostic; with biopsy of pleura).\nNote: 32602 is specific to *diagnostic* thoracoscopy (often medical/local anesthesia). If mapped to surgical VATS, might be 32606, but 'Medical Thoracoscopy' usually implies 32602 equivalent context. No pleurodesis (32650) performed.",
            4: "Resident Note\nPatient: Barbara Kelly\nProcedure: Pleuroscopy\n1. 7th ICS access.\n2. Drained 1.2L yellow fluid.\n3. Put camera in. Looks like fibrin and bumps.\n4. Took biopsies of the bumps.\n5. Didn't put talc in.\n6. Chest tube placed.\nPlan: Wait for path.",
            5: "patricia foster here for scope of the pleural space right side. effusions keep coming back. we drained 1200cc straw fluid. looked inside with the flex scope saw a lot of fibrin and nodules. took a bunch of biopsies sent for TB and cancer. didnt talc her yet. chest tube in place sending to floor.",
            6: "Diagnostic medical thoracoscopy with pleural biopsies (no pleurodesis) was performed. Patient is a 62-year-old female with unilateral right exudative pleural effusion. Under ultrasound guidance, the right 7th intercostal space was selected. Approximately 1200 mL of straw-colored fluid was drained. A semi-rigid thoracoscope was introduced, revealing diffuse fibrinous exudate and scattered small nodules. Multiple parietal pleural biopsies were obtained. No talc was instilled. There were no complications. A chest tube was left to water seal.",
            7: "[Indication]\nRight exudative effusion, undiagnosed.\n[Anesthesia]\nModerate sedation + Local.\n[Description]\n1200mL fluid drained. Thoracoscopy revealed nodules/fibrin. Parietal pleural biopsies taken. No pleurodesis performed.\n[Plan]\nAdmit. Chest tube management. Await pathology.",
            8: "Mrs. Barnes has fluid around her right lung that we haven't been able to diagnose. Today we did a procedure to look inside the chest cavity with a camera. We drained over a liter of fluid and saw some small bumps and inflammation on the lining of the lung. We took several samples (biopsies) of these bumps to test for tuberculosis or cancer. We decided not to seal the lung (talc) until we know exactly what we are treating. She has a tube in her side to drain any leftover fluid.",
            9: "Procedure: Diagnostic pleuroscopy with parietal biopsy.\nFindings: 1.2L serous effusion. Fibrinous exudate and nodular pleural changes.\nAction: Evacuation of fluid and biopsy of parietal pleura. Pleurodesis withheld.\nDisposition: Ward admission with indwelling pleural catheter."
        },
        9: { # William Carter (Thoracentesis + Pneumo)
            1: "Indication: Recurrent Left effusion, CHF.\nProc: US-Guided Thoracentesis.\nResult: 1100mL clear fluid removed.\nComplication: Post-proc chest pain -> CXR showed small apical PTX.\nAction: No chest tube needed. Oxygen started.\nDisposition: Admit for observation.",
            2: "PROCEDURE NOTE: Ultrasound-Guided Therapeutic Thoracentesis. \nThe left hemithorax was accessed at the 8th intercostal space. 1.1 liters of transudative-appearing fluid were removed. The procedure was complicated by the development of a small apical pneumothorax, likely ex-vacuo or traumatic, confirmed on post-procedure ultrasound and radiography. The patient reported mild pleurisy but remained hemodynamically stable. Intervention with tube thoracostomy was deemed unnecessary. Conservative management with supplemental oxygen was initiated.",
            3: "Code: 32555 (Thoracentesis with imaging guidance).\nNote: The pneumothorax is a complication/finding, not a separate billable procedure unless treated with a chest tube (32557) or aspiration, which was *not* done here. The patient was admitted (E&M code) but the procedure code remains 32555.",
            4: "Resident Note\nPatient: Robert Hughes\nProcedure: Thoracentesis\n1. US guidance -> Left 8th ICS.\n2. Pulled 1.1L straw fluid.\n3. Patient coughed at end, had pain.\n4. CXR showed small pneumo at the top.\n5. Stable, so we didn't put a tube in.\nPlan: Admit, O2, repeat CXR am.",
            5: "william carter heart failure patient with fluid on left lung again. did a tap with ultrasound. got 1100 out. he started coughing and having pain. ultrasound looked like maybe lung down. cxr confirmed small pneumo. its small so no tube just watching him overnight with oxygen.",
            6: "Ultrasound-guided thoracentesis complicated by small pneumothorax. Patient is a 79-year-old male with recurrent left pleural effusion. Using real-time ultrasound, the left 8th intercostal space was selected. 1100 mL of clear straw-colored fluid was removed. Patient developed mild pleuritic pain and cough. Post-procedure ultrasound and CXR showed a small apical pneumothorax. No chest tube was placed. Patient is being observed with supplemental oxygen and admitted overnight.",
            7: "[Indication]\nSymptomatic left pleural effusion (CHF).\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\n1100mL fluid removed via US-guided thoracentesis. Complicated by iatrogenic apical pneumothorax.\n[Plan]\nConservative management (Oxygen). Admit for observation. No chest tube currently indicated.",
            8: "Mr. Patterson needed fluid drained from around his left lung again due to his heart failure. We successfully drained about a liter of fluid. Towards the end, he had some coughing and pain. Unfortunately, the x-ray showed a small pocket of air (pneumothorax) outside the lung. It is small enough that we don't think he needs a tube to drain the air right now, but we are going to keep him in the hospital overnight on oxygen to be safe.",
            9: "Procedure: Echography-guided pleural aspiration.\nVolume: 1100 mL serous fluid.\nAdverse Event: Post-procedural apical pneumothorax.\nManagement: Expectant management with supplemental oxygen therapy. No thoracostomy required.\nDisposition: Inpatient monitoring."
        }
    }
    return variations

def main():
    # Load original data
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return

    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through each original note
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        
        # Generate 9 variations
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # Randomize Age (+/- 2 years)
            new_age = record['orig_age'] + random.randint(-2, 2)
            
            # Randomize Date (Year 2025)
            rand_date = generate_random_date(2025, 2025).strftime("%Y-%m-%d")
            
            # New Name
            new_name = record['names'][style_num - 1]
            
            # Update content
            # 1. Update text with the specific variation style
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # 2. Update Registry Entry
            if "registry_entry" in note_entry:
                note_entry["registry_entry"]["patient_age"] = new_age
                note_entry["registry_entry"]["procedure_date"] = rand_date
                
                # Also update note_text inside registry_entry if it exists there
                if "note_text" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["note_text"] = variations_text[idx][style_num]

                # Append suffix to MRN to ensure uniqueness
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            
            # 3. Add Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Save output
    output_path = output_dir / OUTPUT_FILENAME
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_path}")

if __name__ == "__main__":
    main()