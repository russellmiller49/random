import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_021.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted variations for the 10 notes in Part 021.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Kevin Foster - WLL Aborted
            1: "Procedure: Left WLL. Aborted.\nReason: Hypoxemia (78%).\nAction: 6L in, 4.8L out. Stopped. Drained.\nDisposition: ICU, intubated.",
            2: "OPERATIVE NARRATIVE: Therapeutic whole lung lavage. The procedure was initiated on the left lung following double-lumen intubation. After the instillation of 6 L of saline, the patient manifested refractory hypoxemia despite recruitment maneuvers. The procedure was aborted to ensure patient safety. Residual fluid was evacuated, and two-lung ventilation resumed. The patient was transferred to the intensive care unit for ongoing respiratory support.",
            3: "CPT 32997: Therapeutic whole lung lavage (unilateral).\nService Description: Left lung lavage initiated via 39Fr DLT. 6000mL instilled, 4800mL returned. Procedure terminated early due to physiologic instability (desaturation to 78%).\nStatus: Procedure attempted/performed to extent possible.",
            4: "Procedure Note\nPatient: Kevin Foster\nProcedure: Whole Lung Lavage (Left)\nSteps:\n1. General anesthesia, DLT.\n2. Isolated left lung.\n3. Instilled 6L saline.\n4. Patient desatted to 78%.\n5. Aborted procedure, suctioned fluid.\n6. Sent to ICU intubated.",
            5: "Kevin Foster WLL note. We started washing the left lung got about 6 liters in but his sats dropped to the 70s. Couldn't get them up so we stopped. Sucked out what we could. He's going to the ICU still on the vent.",
            6: "Left lung lavage was initiated with 1 L aliquots under general anesthesia with a double-lumen ET tube. After 6 L instilled and 4.8 L returned, patient developed refractory hypoxemia. The lavage was aborted, fluid drained as completely as possible, and both lungs ventilated. The patient was left intubated and transported to the ICU.",
            7: "[Indication]\nPulmonary alveolar proteinosis.\n[Anesthesia]\nGeneral, Double-lumen tube.\n[Description]\nLeft whole lung lavage initiated. 6L instilled. Aborted due to refractory hypoxemia (78%). Fluid drained.\n[Plan]\nICU admission.",
            8: "Mr. Foster underwent an attempted left whole lung lavage for his PAP. We placed a double-lumen tube and began the washing process. Unfortunately, after using about 6 liters of fluid, his oxygen levels dropped dangerously low. We made the decision to stop the procedure immediately, drain the remaining fluid, and transfer him to the ICU while keeping him on the ventilator.",
            9: "Operation: Left lung irrigation stopped early due to low oxygen.\nDetails: Lavage commenced. After 6 L infused and 4.8 L retrieved, patient exhibited stubborn hypoxemia. The cleanse was ceased, liquid siphoned, and both lungs ventilated."
        },
        1: { # Noah Brooks - Rigid Bronch Peanut
            1: "Indication: Peanut aspiration.\nProcedure: Rigid bronch.\nFindings: Peanut fragment RML.\nAction: Removed w/ forceps. Suctioned.\nComplication: Transient desat (88%).\nPlan: Observe.",
            2: "PROCEDURE PERFORMED: Pediatric rigid bronchoscopy with foreign body retrieval.\nCLINICAL SUMMARY: This 2-year-old male presented with findings consistent with foreign body aspiration. Rigid bronchoscopy revealed an organic foreign body, identified as a peanut fragment, obstructing the right middle lobe bronchus. The object was successfully extracted using optical alligator forceps. The airway was subsequently cleared of secretions. There was a transient desaturation event which resolved promptly.",
            3: "Code: 31635 (Bronchoscopy, rigid, with removal of foreign body).\nTarget: Right Middle Lobe Bronchus.\nObject: Organic foreign body (peanut).\nTechnique: Rigid bronchoscopy used for airway control and retrieval forceps for extraction.",
            4: "Procedure Note\nPatient: Noah Brooks\nProcedure: Rigid Bronch/FB Removal\nSteps:\n1. GA/Rigid scope.\n2. Found peanut in RML.\n3. Grabbed with alligator forceps.\n4. Pulled it out.\n5. Checked airway - clear.\n6. Extubated.",
            5: "Noah Brooks 2yo peanut aspiration. We took him to the OR put the rigid scope down. Peanut was stuck in the RML. Pulled it out with the alligator graspers. He desatted a little bit but came right back up. Extubated fine.",
            6: "Rigid bronchoscopy was performed under general anesthesia. An organic foreign body (peanut fragment) was found lodged in the right middle lobe bronchus. The foreign body was removed using alligator forceps and suction. The airway was irrigated. Brief desaturation to 88 percent occurred during retrieval but resolved.",
            7: "[Indication]\nSuspected peanut aspiration; RML collapse.\n[Anesthesia]\nGeneral (Rigid Bronchoscope).\n[Description]\nPeanut fragment visualized in RML. Removed via alligator forceps. Airway cleared.\n[Plan]\nObservation on pediatric ward.",
            8: "We performed a rigid bronchoscopy on Noah to remove a peanut he had inhaled. We found the piece lodged in his right middle lobe. Using special forceps, we were able to grab it and pull it out. He had a brief drop in oxygen levels during the removal, but he recovered quickly and was woken up in the operating room.",
            9: "Procedure: Rigid airway inspection with extraction of foreign object.\nFindings: Organic debris (peanut) in RML.\nAction: Object retrieved utilizing grasping instrument. Airway cleansed.\nOutcome: Obstruction resolved."
        },
        2: { # Sophia King - Rigid Bronch Plastic Toy
            1: "Indication: Plastic toy aspiration.\nProcedure: Rigid bronch.\nFindings: Plastic fragment left mainstem.\nAction: Removed intact w/ optical forceps.\nResult: Airway clear.\nPlan: Discharge.",
            2: "OPERATIVE REPORT: Rigid bronchoscopy for foreign body removal.\nFINDINGS: A brightly colored plastic foreign body was visualized impacting the left mainstem bronchus. \nPROCEDURE: The object was engaged and extracted in a single piece utilizing optical grasping forceps. Re-inspection of the tracheobronchial tree confirmed complete removal with no residual fragments. The patient tolerated the procedure well.",
            3: "CPT 31635: Bronchoscopy (rigid) with removal of foreign body.\nSite: Left Mainstem Bronchus.\nItem: Plastic toy fragment.\nMethod: Optical grasping forceps used via rigid bronchoscope to extract object intact.",
            4: "Procedure Note\nPatient: Sophia King\nProcedure: FB Removal\nSteps:\n1. GA/Rigid bronch.\n2. Saw plastic toy in Left Main.\n3. Removed with optical forceps.\n4. Suctioned airway.\n5. Extubated.\nPlan: Home.",
            5: "Sophia King 5yo swallowed a toy well inhaled it. We went in with the rigid scope and saw the plastic piece in the left mainstem. Used the optical forceps to grab it and pull it out. Came out in one piece. No issues she went home later.",
            6: "General anesthesia was induced via rigid pediatric bronchoscope. A brightly colored plastic toy fragment was found lodged in the left mainstem bronchus. The foreign body was removed using optical grasping forceps in a single piece. Airways were suctioned and re-inspected; no residual fragments were found.",
            7: "[Indication]\nForeign body aspiration (plastic toy).\n[Anesthesia]\nGeneral (Rigid).\n[Description]\nPlastic fragment in Left Mainstem Bronchus. Removed via optical forceps. Airway patent.\n[Plan]\nDischarge.",
            8: "Sophia came in with a wheeze after inhaling a toy part. We performed a rigid bronchoscopy and found the plastic piece in her left main breathing tube. We used forceps with a camera to carefully remove it. The airway was checked and looked clear. She woke up well and went home the same day.",
            9: "Procedure: Rigid airway exam with retrieval of synthetic foreign body.\nFindings: Plastic object in left mainstem.\nAction: Item extracted utilizing optical graspers. Airway cleared.\nOutcome: Foreign body eliminated."
        },
        3: { # Liam Murphy - Flex Bronch Dental Crown
            1: "Indication: Aspirated dental crown.\nProcedure: Flexible bronch (fluoroscopy).\nFindings: Crown in RLL basal.\nAction: Removed w/ flexible alligator forceps.\nResult: Success.\nPlan: Discharge.",
            2: "PROCEDURE: Flexible bronchoscopy with foreign body removal.\nCLINICAL CONTEXT: The patient aspirated a dental crown during a dental procedure. \nFINDINGS: The metallic foreign body was localized to the right lower lobe basal segment. \nINTERVENTION: Under fluoroscopic guidance, the object was secured with flexible alligator forceps and successfully retrieved. Inspection of the bronchial mucosa revealed mild erythema but no perforation.",
            3: "Service: Flexible Bronchoscopy (31635).\nIndication: Iatrogenic foreign body (Dental Crown).\nLocation: RLL Basal Segment.\nTechnique: Fluoroscopic guidance utilized to locate and grasp object with flexible forceps.",
            4: "Procedure Note\nPatient: Liam Murphy\nProcedure: Flex Bronch FB Removal\nSteps:\n1. Moderate sedation.\n2. Scope down. Found crown in RLL.\n3. Used fluoro to help.\n4. Grabbed with alligator forceps.\n5. Pulled it out.\n6. Stable.",
            5: "Liam Murphy aspirated a crown at the dentist. We did a flexible bronch with some sedation. Found the crown deep in the RLL. Used the x-ray to help grab it with the forceps. Got it out fine. Just a little redness inside.",
            6: "Moderate sedation was achieved. A metallic foreign body was visualized in the RLL basal segment bronchus. The foreign body was grasped and removed using flexible alligator forceps under fluoroscopic guidance. Bronchial mucosa was mildly erythematous. There were no complications.",
            7: "[Indication]\nAspirated dental crown.\n[Anesthesia]\nModerate Sedation.\n[Description]\nCrown visualized in RLL basal segment. Removed via flexible alligator forceps and fluoroscopy.\n[Plan]\nDischarge.",
            8: "Mr. Murphy aspirated a dental crown, so we performed a flexible bronchoscopy to get it out. We found the metal crown in the lower part of his right lung. Using real-time x-ray guidance and flexible forceps, we grabbed the crown and pulled it out. He had a bit of a cough but otherwise did great.",
            9: "Procedure: Flexible airway inspection with extraction of dental prosthesis.\nFindings: Metallic object in RLL.\nAction: Object retrieved utilizing flexible graspers and imaging guidance.\nOutcome: Airway cleared."
        },
        4: { # Chloe Adams - BT Session 1 RLL
            1: "Indication: Severe asthma.\nProcedure: Bronchial Thermoplasty (RLL).\nAction: 52 activations delivered to RLL segments.\nComplication: Mild wheeze.\nPlan: D/C on prednisone.",
            2: "PROCEDURE: Bronchial Thermoplasty, initial session.\nTARGET: Right Lower Lobe.\nDETAILS: Under moderate sedation, the Alair catheter was advanced into the distal segmental airways of the right lower lobe. Radiofrequency energy was delivered systematically. A total of 52 activations were completed. The patient experienced mild procedure-induced bronchospasm which responded to bronchodilators.",
            3: "CPT 31660: Bronchoscopy with bronchial thermoplasty, one lobe.\nTarget Lobe: Right Lower Lobe.\nWork Performed: 52 RF activations delivered to segmental/subsegmental airways.\nMedical Necessity: Severe persistent asthma refractory to standard therapy.",
            4: "Procedure Note\nPatient: Chloe Adams\nProcedure: BT Session 1 (RLL)\nSteps:\n1. Sedation.\n2. Treated RLL airways with thermoplasty catheter.\n3. 52 hits total.\n4. Tolerated well, mild wheeze.\nPlan: Prednisone burst, home.",
            5: "Chloe Adams here for her first thermoplasty session on the RLL. We did the usual sedation. Treated all the segments in the right lower lobe got 52 activations. She got a little wheezy so we gave her some treatment. Sent her home on prednisone.",
            6: "Flexible bronchoscope used to sequentially treat RLL segmental and subsegmental bronchi with bronchial thermoplasty catheter. Total of 52 activations delivered to RLL. Mild wheezing and cough occurred during procedure; no significant desaturation. Patient observed and discharged.",
            7: "[Indication]\nSevere persistent asthma.\n[Anesthesia]\nModerate Sedation.\n[Description]\nBronchial Thermoplasty performed on Right Lower Lobe. 52 activations delivered.\n[Plan]\nDischarge with prednisone.",
            8: "Ms. Adams underwent her first session of bronchial thermoplasty for her asthma. We focused on the right lower lobe today. Using the special catheter, we treated the airways with heat energy, completing 52 activations. She had some coughing and wheezing during the procedure, but it settled down. She went home later that day.",
            9: "Procedure: Airway thermal ablation (Session 1).\nTarget: RLL.\nAction: RF energy applied to segmental bronchi. 52 applications performed.\nOutcome: Procedure completed with minor bronchospasm."
        },
        5: { # Jason Miller - BT Session 2 LLL
            1: "Indication: Severe asthma, session 2.\nProcedure: Bronchial Thermoplasty (LLL).\nAction: 48 activations delivered to LLL.\nComplication: Transient bronchospasm.\nPlan: D/C on prednisone taper.",
            2: "PROCEDURE: Bronchial Thermoplasty, second session.\nTARGET: Left Lower Lobe.\nDETAILS: Following the protocol for severe refractory asthma, the left lower lobe was selected for treatment. The thermoplasty catheter was deployed to the distal subsegmental bronchi. A total of 48 radiofrequency activations were delivered. The patient tolerated the procedure with only transient bronchospasm.",
            3: "CPT 31660: Bronchoscopy with bronchial thermoplasty, one lobe.\nTarget Lobe: Left Lower Lobe.\nWork Performed: 48 RF activations delivered.\nNote: Second session (separate date from RLL treatment).",
            4: "Procedure Note\nPatient: Jason Miller\nProcedure: BT Session 2 (LLL)\nSteps:\n1. MAC sedation.\n2. Treated LLL with BT catheter.\n3. 48 activations.\n4. Some spasm, treated.\nPlan: Home.",
            5: "Jason Miller back for session 2 of thermoplasty LLL this time. MAC anesthesia. We did 48 activations in the left lower lobe. He got tight during the case but we gave bronchodilators and he opened up. Discharged him after a few hours.",
            6: "Flexible bronchoscopy performed with BT catheter treatment of LLL segmental and subsegmental bronchi. Total of 48 activations delivered. Transient bronchospasm requiring additional bronchodilator therapy occurred; no respiratory failure. Patient discharged on prednisone taper.",
            7: "[Indication]\nSevere asthma (Session 2).\n[Anesthesia]\nMAC.\n[Description]\nBronchial Thermoplasty performed on Left Lower Lobe. 48 activations delivered.\n[Plan]\nDischarge on prednisone.",
            8: "Mr. Miller returned for his second bronchial thermoplasty treatment, targeting the left lower lobe. We delivered 48 pulses of energy to the airways. He experienced some tightening of the airways during the procedure, which we treated with medication. He was monitored for a few hours and then sent home.",
            9: "Procedure: Airway thermal ablation (Session 2).\nTarget: LLL.\nAction: RF energy applied to segmental bronchi. 48 applications performed.\nOutcome: Procedure completed, transient spasm managed."
        },
        6: { # Hannah Lewis - BT Session 3 Bilateral Upper
            1: "Indication: Severe asthma, final session.\nProcedure: Bronchial Thermoplasty (RUL + LUL).\nAction: 60 activations total (30/side).\nComplication: Mild cough.\nPlan: Admit for observation.",
            2: "PROCEDURE: Bronchial Thermoplasty, final session.\nTARGET: Bilateral Upper Lobes.\nDETAILS: Under general anesthesia, the final stage of thermoplasty was undertaken. The catheter was sequentially deployed in the right upper lobe and left upper lobe segmental airways. A total of 60 activations were delivered (30 per lobe). The patient remained stable with only mild post-procedure cough.",
            3: "CPT 31660: Bronchoscopy with bronchial thermoplasty, one lobe.\n(Note: Bilateral upper lobes treated; coding reflects primary lobe. Institutional protocol may vary on add-on code).\nWork Performed: 30 activations RUL, 30 activations LUL (60 Total).\nSetting: Bronchoscopy suite.",
            4: "Procedure Note\nPatient: Hannah Lewis\nProcedure: BT Session 3 (Upper Lobes)\nSteps:\n1. GA/LMA.\n2. Treated RUL and LUL.\n3. 60 hits total.\n4. Mild cough.\nPlan: Admit overnight.",
            5: "Hannah Lewis for her last thermoplasty session doing both upper lobes today. General anesthesia with an LMA. We did 30 hits on the right and 30 on the left. She did fine just some coughing after. Keeping her overnight since she lives far away.",
            6: "BT catheter deployed sequentially in RUL and LUL segmental airways. Total of 60 activations delivered (30 per side). Mild postprocedure cough and chest tightness noted. Patient admitted overnight for observation.",
            7: "[Indication]\nSevere asthma (Session 3).\n[Anesthesia]\nGeneral, LMA.\n[Description]\nBronchial Thermoplasty performed on Bilateral Upper Lobes. 60 total activations.\n[Plan]\nAdmit for observation.",
            8: "Ms. Lewis underwent her final bronchial thermoplasty session, treating both upper lobes. We used general anesthesia for this session. We delivered 30 activations to the right upper lobe and 30 to the left. She had some chest tightness afterwards, so we decided to keep her overnight for monitoring.",
            9: "Procedure: Airway thermal ablation (Session 3).\nTarget: Bilateral Upper Lobes.\nAction: RF energy applied to segmental bronchi. 60 applications total.\nOutcome: Procedure completed, patient admitted."
        },
        7: { # George Turner - Medical Thoracoscopy
            1: "Indication: Recurrent left effusion.\nProcedure: Medical Thoracoscopy.\nFindings: 1.5L fluid, parietal nodules.\nAction: Biopsies taken. Talc slurry pleurodesis.\nPlan: Admit, chest tube.",
            2: "PROCEDURE: Medical thoracoscopy with pleural biopsy and pleurodesis.\nFINDINGS: Thoracoscopic inspection of the left hemithorax revealed diffuse nodularity and studding of the parietal pleura, highly suspicious for malignancy. Approximately 1.5 L of straw-colored effusion was evacuated. \nINTERVENTION: Multiple targeted parietal pleural biopsies were obtained. Following complete drainage, a talc slurry was instilled to achieve pleurodesis.",
            3: "CPT 32609: Thoracoscopy, surgical; with pleurodesis, including pleural biopsies.\nDetails: Visualization of pleural space, drainage of 1.5L fluid, biopsies of parietal nodules, and instillation of talc agent for pleurodesis.\nGuidance: Ultrasound used for access.",
            4: "Procedure Note\nPatient: George Turner\nProcedure: Med Thoracoscopy + Talc\nSteps:\n1. MAC/Local.\n2. Trocar in 6th ICS.\n3. Drained 1.5L fluid.\n4. Saw nodules, took biopsies.\n5. Put in talc slurry.\n6. Chest tube placed.\nPlan: Admit.",
            5: "George Turner medical thoracoscopy. We went in on the left side drained about a liter and a half of fluid. The pleura looked studded with cancer. Took a bunch of biopsies. Put some talc in there to stick it down. He's admitted with a chest tube.",
            6: "Under ultrasound guidance, left 6th intercostal space was selected. 1.5 L of straw-colored fluid drained. Semi-rigid thoracoscope introduced; diffuse parietal pleural nodularity observed. Multiple parietal pleural biopsies taken. Talc slurry pleurodesis performed after complete drainage. Admitted for chest tube management.",
            7: "[Indication]\nRecurrent left pleural effusion; suspected malignancy.\n[Anesthesia]\nMAC/Local.\n[Description]\nMedical Thoracoscopy performed. 1.5L fluid drained. Parietal nodules biopsied. Talc pleurodesis performed.\n[Plan]\nAdmit for chest tube management.",
            8: "We performed a medical thoracoscopy on Mr. Turner to diagnose and treat his recurrent fluid buildup. We drained 1.5 liters of fluid and found several nodules on the lining of the lung, which we biopsied. To prevent the fluid from coming back, we performed a talc pleurodesis. He will stay in the hospital with a chest tube for a few days.",
            9: "Procedure: Pleuroscopy with tissue sampling and chemical sclerosis.\nFindings: Effusion and pleural studding.\nAction: Fluid evacuated. Biopsies harvested. Talc administered for symphysis.\nDisposition: Admission."
        },
        8: { # Isabel Morales - Thoracentesis
            1: "Indication: Recurrent right effusion.\nProcedure: US-guided Thoracentesis.\nAction: 900mL clear fluid removed.\nComplication: None.\nPlan: Discharge.",
            2: "PROCEDURE: Ultrasound-guided therapeutic thoracentesis.\nNARRATIVE: The right hemithorax was scanned, identifying a locatable pocket of fluid in the 8th intercostal space. Under local anesthesia, a catheter was introduced and 900 mL of clear serous fluid was aspirated. The patient tolerated the procedure without complication.",
            3: "CPT 32555: Thoracentesis, therapeutic, with imaging guidance.\nDetails: Ultrasound guidance utilized to identify pocket. 900 mL fluid removed via catheter. No pleural biopsy performed.",
            4: "Procedure Note\nPatient: Isabel Morales\nProcedure: Thoracentesis\nSteps:\n1. Ultrasound check.\n2. Local numbing.\n3. Needle/catheter in.\n4. Drained 900cc.\n5. Pulled catheter, bandaged.\nPlan: Home.",
            5: "Isabel Morales thoracentesis note. She has heart failure fluid on the right. We used the ultrasound to find a spot. Drained 900ml of clear fluid. She felt better. Sent her home.",
            6: "Right posterior 8th intercostal space chosen under ultrasound guidance. 900 mL of clear serous fluid removed via catheter system. No complications occurred. Patient discharged home.",
            7: "[Indication]\nRecurrent right pleural effusion (HF).\n[Anesthesia]\nLocal.\n[Description]\nUS-guided thoracentesis. 900mL serous fluid drained.\n[Plan]\nDischarge.",
            8: "Ms. Morales needed fluid drained from her right lung due to heart failure. We used ultrasound to guide a small tube into the fluid pocket and drained 900 mL. She tolerated it well and was breathing better afterwards. She was discharged home.",
            9: "Procedure: Image-guided pleural drainage.\nAction: 900mL liquid aspirated via percutaneous catheter.\nOutcome: Symptom relief."
        },
        9: { # Ethan Hall - Med Thoracoscopy + IPC
            1: "Indication: Malignant effusion.\nProcedure: Medical Thoracoscopy + IPC.\nFindings: 1.8L fluid, nodules.\nAction: Talc poudrage performed. Tunneled catheter placed.\nPlan: Admit, d/c next day.",
            2: "PROCEDURE: Medical thoracoscopy with talc poudrage and placement of indwelling pleural catheter.\nFINDINGS: Thoracoscopy revealed extensive parietal pleural implants. 1.8 L of serosanguinous fluid was evacuated. \nINTERVENTION: Talc poudrage was insufflated for pleurodesis. Additionally, a tunneled indwelling pleural catheter was placed to ensure long-term drainage capability. \nDISPOSITION: The patient will be admitted for overnight observation.",
            3: "CPT 32609: Thoracoscopy with pleurodesis (Talc).\nCPT 32550: Insertion of indwelling tunneled pleural catheter.\nRationale: Dual management strategy employed (Talc for immediate symphysis, IPC for long-term failure/drainage).",
            4: "Procedure Note\nPatient: Ethan Hall\nProcedure: Thoracoscopy + Talc + IPC\nSteps:\n1. MAC sedation.\n2. Thoracoscopy: drained 1.8L.\n3. Sprayed talc (poudrage).\n4. Placed PleurX catheter.\n5. Secure.\nPlan: Admit.",
            5: "Ethan Hall thoracoscopy note. Drained 1.8L bloody fluid. Lung looked cancerous. We did the talc spray to glue it and also put in a tunneled catheter just in case. He's staying overnight.",
            6: "Under ultrasound guidance, right 7th intercostal space selected. 1.8 L of serosanguinous pleural fluid drained. Thoracoscopy revealed nodular parietal pleural implants. Talc poudrage pleurodesis performed and indwelling tunneled pleural catheter placed for outpatient drainage. Admitted overnight.",
            7: "[Indication]\nRecurrent malignant pleural effusion.\n[Anesthesia]\nMAC/Local.\n[Description]\nMedical Thoracoscopy. 1.8L drained. Talc poudrage performed. Tunneled pleural catheter placed.\n[Plan]\nAdmit.",
            8: "Mr. Hall underwent a procedure to manage his malignant fluid buildup. We performed a thoracoscopy, drained 1.8 liters of fluid, and sprayed talc to seal the lung. We also placed a permanent tunneled catheter to allow for drainage at home if the fluid comes back. He will stay overnight for monitoring.",
            9: "Procedure: Pleuroscopy with chemical sclerosis and tunnelled drain insertion.\nFindings: Metastatic implants.\nAction: Fluid evacuated. Talc insufflated. Long-term catheter implanted.\nOutcome: Dual modality management established."
        }
    }
    return variations

def get_base_data_mocks():
    return [
        {"idx": 0, "orig_name": "Kevin Foster", "orig_age": 49, "names": ["Alan Hughes", "Brian Cole", "Charles Diaz", "David Evans", "Edward Foster", "Frank Green", "George Hill", "Henry Irwin", "Ian Jones"]},
        {"idx": 1, "orig_name": "Noah Brooks", "orig_age": 2, "names": ["Liam Smith", "Oliver Johnson", "Elijah Williams", "James Brown", "William Jones", "Benjamin Garcia", "Lucas Miller", "Henry Davis", "Theodore Rodriguez"]},
        {"idx": 2, "orig_name": "Sophia King", "orig_age": 5, "names": ["Ava Martinez", "Emma Hernandez", "Charlotte Lopez", "Amelia Gonzalez", "Mia Wilson", "Harper Anderson", "Evelyn Thomas", "Abigail Taylor", "Emily Moore"]},
        {"idx": 3, "orig_name": "Liam Murphy", "orig_age": 34, "names": ["Mason Jackson", "Logan White", "Alexander Harris", "Ethan Martin", "Jacob Thompson", "Michael Garcia", "Daniel Martinez", "Matthew Robinson", "Joseph Clark"]},
        {"idx": 4, "orig_name": "Chloe Adams", "orig_age": 45, "names": ["Sofia Lewis", "Avery Lee", "Ella Walker", "Madison Hall", "Scarlett Allen", "Victoria Young", "Luna King", "Grace Wright", "Chloe Scott"]},
        {"idx": 5, "orig_name": "Jason Miller", "orig_age": 52, "names": ["Samuel Green", "Sebastian Baker", "Jack Adams", "Owen Nelson", "Theodore Carter", "Wyatt Mitchell", "Julian Perez", "Luke Roberts", "Gabriel Turner"]},
        {"idx": 6, "orig_name": "Hannah Lewis", "orig_age": 39, "names": ["Penelope Phillips", "Layla Campbell", "Riley Parker", "Zoey Evans", "Nora Edwards", "Lily Collins", "Eleanor Stewart", "Hannah Sanchez", "Lillian Morris"]},
        {"idx": 7, "orig_name": "George Turner", "orig_age": 76, "names": ["Christopher Rogers", "Andrew Reed", "Thomas Cook", "Joshua Morgan", "Christian Bell", "Hunter Murphy", "Ryan Bailey", "Aaron Rivera", "Nathan Cooper"]},
        {"idx": 8, "orig_name": "Isabel Morales", "orig_age": 73, "names": ["Addison Richardson", "Aubrey Cox", "Stella Howard", "Natalie Ward", "Zoe Torres", "Leah Peterson", "Hazel Gray", "Violet Ramirez", "Aurora James"]},
        {"idx": 9, "orig_name": "Ethan Hall", "orig_age": 65, "names": ["Caleb Watson", "Ryan Brooks", "Asher Kelly", "Adrian Sanders", "Leo Price", "Isaiah Bennett", "Jonathan Wood", "Charles Barnes", "Connor Ross"]}
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
            
            # Determine new random age (+/- 2 years)
            new_age = orig_age + random.randint(-2, 2)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                note_entry["note_text"] = f"Variation {style_num} not found for note {idx}."

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry and note_entry["registry_entry"]:
                # Update Age
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                
                # Update Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update Patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    original_mrn = note_entry["registry_entry"].get("patient_mrn", "UNKNOWN")
                    note_entry["registry_entry"]["patient_mrn"] = f"{original_mrn}_syn_{style_num}"
                
                # Update note_text inside registry_entry if it exists (some files duplicate it there)
                if "note_text" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["note_text"] = variations_text[idx][style_num]

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
    output_filename = output_dir / "synthetic_blvr_notes_part_021.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()