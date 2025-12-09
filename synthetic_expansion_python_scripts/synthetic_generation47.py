import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_047.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Maria Lopez (BAL 31624)
            1: "Indication: RLL Pneumonia.\nSedation: Moderate.\nProcedure: Scope passed orally. RLL bronchus contained mucopurulent secretions; suctioned. BAL performed RLL posterior segment (4x30mL). Return turbid.\nComplications: None.\nPlan: Wait for cultures. D/C home.",
            2: "PROCEDURE NOTE: Flexible Bronchoscopy with Bronchoalveolar Lavage.\nThe patient, presenting with non-resolving right lower lobe pneumonia, underwent bronchoscopic evaluation. Under moderate sedation, the airway was inspected, revealing significant mucopurulent secretions in the RLL. These were evacuated. A bronchoalveolar lavage was conducted in the RLL posterior segment utilizing 120 mL of sterile saline. The effluent was turbid and submitted for microbiological analysis. No endobronchial lesions were identified.",
            3: "Service: Bronchoscopy with BAL (CPT 31624).\nTechnique: Flexible scope inserted. Airways inspected to subsegmental level (31622 bundled). Therapeutic suctioning of secretions performed. Distinct procedure: Bronchoalveolar lavage performed in RLL posterior segment. 120 mL instilled, 60 mL recovered. Specimens sent for culture/cytology.",
            4: "Procedure: Bronchoscopy + BAL\nAttending: Dr. Johnson\nSteps:\n1. Time out/Sedation.\n2. Scope introduced native airway.\n3. Inspection: Copious secretions RLL.\n4. Suctioning.\n5. BAL RLL posterior segment (4 aliquots).\n6. Scope removed.\nPlan: Continue abx, check cultures.",
            5: "procedure note maria lopez bronchoscopy for pneumonia moderate sedation used scope went down fine saw a lot of pus in the right lower lobe suctioned it out did the lavage there too sent the fluid for culture no masses seen patient woke up fine discharge home.",
            6: "The patient was brought to the bronchoscopy suite for evaluation of non-resolving pneumonia. After induction of moderate sedation, the bronchoscope was introduced. Inspection revealed normal vocal cords and trachea. The right lower lobe contained copious mucopurulent secretions which were suctioned. A bronchoalveolar lavage was performed in the RLL posterior segment with good return. No endobronchial masses were seen. The patient tolerated the procedure well.",
            7: "[Indication]\nNon-resolving RLL pneumonia.\n[Anesthesia]\nModerate sedation (Fentanyl/Versed).\n[Description]\nScope advanced. Mucopurulent secretions RLL suctioned. BAL performed RLL posterior segment (120cc instilled). Samples sent to lab.\n[Plan]\nDischarge home. Follow up in 4 weeks.",
            8: "Ms. Lopez underwent a flexible bronchoscopy today to investigate her persistent pneumonia. We sedated her comfortably and advanced the scope. Upon reaching the right lower lobe, we encountered a significant amount of mucopurulent secretion, which we cleared. We then performed a bronchoalveolar lavage in the posterior segment to get a sample for culture. The return was turbid. There were no tumors or foreign bodies seen.",
            9: "Evaluation: Bronchoscopy with alveolar washing.\nContext: Recalcimtant RLL infection.\nAction: Airway navigated. Purulence in RLL evacuated. Lavage executed in posterior segment. Effluent collected for analysis.\nOutcome: Tolerance excellent."
        },
        1: { # Daniel Green (Therapeutic Aspiration 31645)
            1: "Indication: LLL collapse/mucus plugging.\nSedation: Moderate.\nFindings: Diffuse mucus plugging L Main/LLL. No mass.\nIntervention: Aggressive suction/saline lavage. Mucus casts removed.\nResult: LLL patent. Subsegments visible.\nPlan: ICU care. CXR.",
            2: "PROCEDURE: Therapeutic Bronchoscopy for Atelectasis.\nMr. Green, a 71-year-old male with severe COPD, presented with complete left lower lobe collapse. Bronchoscopy revealed extensive mucus plugging obstructing the left mainstem and LLL bronchi. Therapeutic aspiration was performed using saline instillation and suction, successfully removing multiple large mucus casts. Post-procedure inspection confirmed re-establishment of patency to the subsegmental airways.",
            3: "CPT 31645: Bronchoscopy with therapeutic aspiration of tracheobronchial tree, initial.\nIndication: Lobar collapse.\nDetails: Visualization of LLL obstruction by mucus. Repeated therapeutic aspiration required to clear airway. Saline lavage used to loosen secretions. Obstruction resolved. No biopsy performed.",
            4: "Resident Note\nPatient: Daniel Green\nProcedure: Therapeutic Bronchoscopy\nSteps:\n1. Sedation/Monitoring.\n2. Scope inserted.\n3. Findings: LLL mucus plug.\n4. Action: Suctioned large plugs, saline flush.\n5. Result: LLL opened up.\nPlan: Aggressive pulmonary toilet.",
            5: "bronch done at bedside icu for mr green he has copd and a collapsed lung saw a lot of thick mucus in the left lower lobe washed it out with saline and sucked it all out looks wide open now no tumor seen oxygen sats dipped a bit but came back up keeping him on the high flow for now check xray later.",
            6: "Bedside bronchoscopy was performed for left lower lobe collapse. Under moderate sedation the scope was passed. The left bronchial tree was occluded by thick mucus. Therapeutic aspiration was performed with saline lavage and suction until the airways were cleared. The left lower lobe bronchus was patent at the end of the case. Patient tolerated well with transient desaturation.",
            7: "[Indication]\nLLL collapse due to mucus plugging.\n[Anesthesia]\nModerate sedation.\n[Description]\nThick mucus casts identified in LLL. Therapeutic aspiration performed. Saline instillation used. Airways cleared to subsegmental level.\n[Plan]\nRepeat CXR. Continue respiratory therapy.",
            8: "We performed a bronchoscopy on Mr. Green to address his collapsed lung. After sedating him, we found significant mucus plugging in the left lower lobe. We spent considerable time suctioning and washing these secretions out. Eventually, we were able to remove the large mucus casts, and the airway opened up nicely. We could see down to the smaller airways by the end.",
            9: "Procedure: Therapeutic clearance of bronchial tree.\nFindings: LLL obstruction via secretions.\nAction: Lavage and evacuation of mucus plugs. Patency restored.\nOutcome: LLL re-expanded."
        },
        2: { # Liam Carter (Foreign Body 31635)
            1: "Indication: FB aspiration (peanut).\nAnesthesia: General/ETT.\nProcedure: Rigid bronchoscopy. Peanut fragment R Mainstem. Removed w/ forceps. Suctioned debris.\nResult: Airway clear.\nPlan: Overnight obs.",
            2: "OPERATIVE REPORT: Rigid Bronchoscopy with Foreign Body Removal.\nThe patient, a 5-year-old male, presented with history of choking. Under general anesthesia, a rigid bronchoscope was introduced. A foreign body consistent with a peanut was identified in the right mainstem bronchus with associated granulation tissue. Optical forceps were utilized to grasp and extract the foreign body in fragments. Documentation of complete removal was confirmed visually.",
            3: "Code: 31635 (Bronchoscopy, rigid or flexible, with removal of foreign body).\nLocation: Right Mainstem Bronchus.\nTool: Rigid forceps.\nDetails: Peanut fragment identified and removed. Proximal airway inspected. No additional procedures (no biopsy/BAL).",
            4: "Procedure: Rigid Bronch FB Removal\nPatient: Liam Carter, 5yo\nSteps:\n1. GA/Intubation.\n2. Rigid scope passed.\n3. Found peanut in RMB.\n4. Removed with forceps.\n5. Re-inspected: Clear.\nPlan: Admit for obs.",
            5: "liam came in choking on a peanut did a rigid bronch in the or under anesthesia saw the peanut in the right lung pulled it out with the grabbers took a few tries to get it all pieces came out fine airway looks clear now no bleeding sending him to recovery.",
            6: "General anesthesia was induced for rigid bronchoscopy. The scope was inserted and the right mainstem bronchus was cannulated. An organic foreign body (peanut) was visualized. Forceps were used to remove the object and surrounding fragments. Suction was applied. The airway was patent upon conclusion.",
            7: "[Indication]\nRight lung hyperinflation, suspected FB.\n[Anesthesia]\nGeneral (ETT).\n[Description]\nRigid bronchoscopy. Peanut found in RMB. Removed via forceps. Granulation tissue noted but not biopsied. Airway cleared.\n[Plan]\nOvernight observation.",
            8: "Liam underwent a rigid bronchoscopy to remove a piece of peanut he had inhaled. We put him under general anesthesia and inserted the rigid scope. We found the peanut lodged in the right mainstem bronchus. Using forceps, we carefully pulled the pieces out. Once it was clear, we double-checked to make sure no debris was left behind. He breathed well afterward.",
            9: "Procedure: Extraction of bronchial foreign body.\nObject: Organic fragment (peanut).\nLocation: Right Mainstem.\nMethod: Rigid instrumentation and forceps retrieval.\nOutcome: Obstruction resolved."
        },
        3: { # Steven Brooks (EBUS 31652)
            1: "Indication: Staging LLL CA.\nAnesthesia: General/ETT.\nProcedure: EBUS. Station 7 and 4R sampled. ROSE: 7 positive, 4R negative.\nComplications: None.\nPlan: Oncology referral.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA).\nMr. Brooks underwent mediastinal staging for LLL adenocarcinoma. Using the linear EBUS scope, systematic nodal survey was performed. Lymph node stations 7 (subcarinal) and 4R (right lower paratracheal) were identified and sampled (3 passes each). Rapid On-Site Evaluation (ROSE) confirmed malignancy in station 7. Procedure concluded without complication.",
            3: "CPT 31652: Bronchoscopy with EBUS-TBNA of 1-2 mediastinal/hilar nodal stations.\nStations Sampled: 4R and 7.\nMethod: Linear EBUS guidance, 21G needle.\nPathology: Adequate samples obtained. ROSE positive station 7.\nNote: No peripheral navigation or biopsies performed.",
            4: "Procedure: EBUS Staging\nPatient: Steven Brooks\nSteps:\n1. GA/ETT.\n2. EBUS scope down.\n3. Sampled 4R: Neg.\n4. Sampled 7: Pos (Adeno).\n5. No other sites.\nPlan: Tumor board.",
            5: "did an ebus on mr brooks for his lung cancer staging general anesthesia tube was already in checked the nodes sampled 4r and 7 with the needle cytology said 7 was positive for cancer cells 4r was clear stopped there patient did fine extubated in room.",
            6: "EBUS bronchoscopy was performed for mediastinal staging. The EBUS scope was advanced via ETT. Stations 4R and 7 were visualized and sampled using a 21G needle. On-site cytology confirmed malignant cells in station 7. No other stations were sampled. The patient tolerated the procedure well.",
            7: "[Indication]\nMediastinal staging for LLL adenocarcinoma.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS scope used. Stations 4R and 7 sampled (TBNA). ROSE positive at station 7.\n[Plan]\nThoracic surgery/Oncology consult.",
            8: "We performed an EBUS procedure to stage Mr. Brooks' lung cancer. After he was asleep, we used the ultrasound scope to look at the lymph nodes in the center of his chest. We took samples from the subcarinal node (station 7) and the right paratracheal node (station 4R). The pathologist in the room confirmed cancer in the subcarinal node. We didn't sample any other areas.",
            9: "Procedure: Ultrasonic nodal sampling.\nTargets: Mediastinal stations 4R, 7.\nTechnique: Transbronchial aspiration.\nFindings: Malignancy confirmed in station 7.\nDisposition: Multidisciplinary review."
        },
        4: { # Evelyn Martin (Robotic Nav + EBUS + Biopsy 31628, 31654, 31627)
            1: "Indication: RUL Nodule.\nProcedure: Ion Robotic Bronch + Radial EBUS.\nTarget: 1.5cm RUL apical nodule.\nActions: Navigated to lesion. Confirmed w/ r-EBUS (concentric). CBCT tool-in-lesion. Biopsy x6, Brush x2, BAL.\nResult: Suspicious for carcinoma.\nPlan: Oncology.",
            2: "PROCEDURE NOTE: Robotic-Assisted Navigation Bronchoscopy.\nMs. Martin presented for biopsy of a PET-avid RUL nodule. The Ion robotic platform was utilized for navigation. Upon reaching the target in the RUL apical segment, radial EBUS confirmed a concentric solid lesion. Cone Beam CT verification demonstrated optimal tool placement. Transbronchial biopsies and brushings were obtained. Cytology suggests non-small cell carcinoma.",
            3: "Coding:\n- 31627: Navigation bronchoscopy (add-on).\n- 31654: Peripheral EBUS (radial probe) for lesion localization (add-on).\n- 31628: Transbronchial lung biopsy, single lobe.\nDetails: Robotic system used for guidance. Radial EBUS confirmed location. Biopsies taken of parenchymal nodule.",
            4: "Procedure: Robotic Bronch/Biopsy\nPatient: Evelyn Martin\nSteps:\n1. GA/ETT.\n2. Ion robot registered.\n3. Navigated to RUL nodule.\n4. Radial EBUS confirmation.\n5. CBCT spin.\n6. Biopsies taken.\nPlan: Wait for path.",
            5: "robotic bronch for ms martin she has that spot in the right upper lobe used the ion system drove out to the nodule radial ebus showed it nicely did a spin with the ct to be sure took a bunch of biopsies and a brush rose said it looks like cancer woke her up no issues.",
            6: "General anesthesia was induced. The Ion robotic bronchoscopy catheter was navigated to a 1.5 cm RUL nodule. Radial EBUS showed a concentric view. Cone beam CT confirmed tool-in-lesion. Transbronchial forceps biopsies and brushings were performed. BAL was also collected. No pneumothorax was observed.",
            7: "[Indication]\n1.5 cm RUL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nRobotic navigation to RUL. Radial EBUS verification. CBCT confirmation. Transbronchial biopsy (31628) and brushing performed.\n[Plan]\nDischarge home. Oncology f/u.",
            8: "We used the robotic bronchoscope to biopsy Ms. Martin's lung nodule. Once the robot guided us to the right upper lobe spot, we double-checked the location with the radial ultrasound probe and the CT spinner. Everything lined up perfectly. We took several biopsies and a brush sample. The preliminary check by the pathologist looked suspicious for cancer.",
            9: "Procedure: Computer-guided bronchoscopy with peripheral sampling.\nTarget: RUL pulmonary lesion.\nVerification: Radial ultrasonography and cone-beam tomography.\nTechnique: Forceps sampling and bronchial brushing.\nOutcome: Diagnostic material obtained."
        },
        5: { # Helen Ortiz (Chartis Only 31634)
            1: "Indication: COPD/BLVR Eval.\nProcedure: Chartis assessment.\nFindings: Balloon occlusion LUL and LLL. Flow persisted (CV positive).\nResult: Not a candidate for valves.\nPlan: Medical management/Transplant referral.",
            2: "PROCEDURE: Bronchoscopic Assessment of Collateral Ventilation.\nMrs. Ortiz underwent evaluation for endobronchial valve candidacy. The Chartis system was deployed in the target segments of the left lung. Measurements in both the LUL and LLL demonstrated persistent expiratory flow without cessation, indicative of collateral ventilation. Consequently, valve placement was not performed.",
            3: "Code: 31634 (Balloon occlusion assessment).\nIndication: Evaluation for lung volume reduction.\nDetails: Catheter placed in segmental bronchi. Balloon inflated. Flow measurements recorded. Positive collateral ventilation detected. Procedure terminated without valve insertion.",
            4: "Procedure: Chartis Eval\nPatient: Helen Ortiz\nSteps:\n1. GA/ETT.\n2. Chartis catheter to LUL then LLL.\n3. Measured flow.\n4. Result: CV positive (flow didn't stop).\nPlan: No valves. Pulmonary rehab.",
            5: "did a chartis on helen ortiz to see if we could put valves in she has bad copd checked the left side with the balloon but the air kept coming out meaning collateral ventilation is positive so we didnt put any valves in woke her up shes not a candidate.",
            6: "Bronchoscopy was performed to assess for collateral ventilation using the Chartis system. The balloon catheter was positioned in the LUL and LLL bronchi. In all tested segments, airflow persisted after occlusion, confirming the presence of collateral ventilation. No endobronchial valves were placed.",
            7: "[Indication]\nBLVR candidacy evaluation.\n[Anesthesia]\nGeneral.\n[Description]\nChartis assessment of LUL and LLL. Persistent airflow noted (CV+).\n[Plan]\nNo valves placed. Continue medical therapy.",
            8: "We brought Mrs. Ortiz in to see if she could get valves for her emphysema. We used a special balloon catheter to block her airways and measure airflow. Unfortunately, the air kept flowing even when we blocked the bronchus, which means her lung sections are connected (collateral ventilation). Because of this, valves wouldn't work, so we didn't put any in.",
            9: "Procedure: Assessment of collateral airflow.\nMethod: Balloon occlusion (Chartis).\nFindings: Interlobar airflow present.\nConclusion: Contraindication for valve therapy."
        },
        6: { # Robert James (BLVR LUL 31647)
            1: "Indication: Emphysema.\nProcedure: BLVR LUL.\nAction: 3 Zephyr valves placed (Apicoposterior, Anterior, Lingula).\nResult: Total occlusion. Good position.\nPlan: Admit. CXR monitoring.",
            2: "PROCEDURE: Endobronchial Valve Placement.\nMr. James presented for bronchoscopic lung volume reduction of the left upper lobe. Following induction, the LUL was inspected. Three Zephyr valves were deployed into the segmental bronchi. Occlusion was verified visually. No immediate complications were observed. Patient admitted for pneumothorax monitoring.",
            3: "CPT: 31647 (Bronchoscopy with valve placement, initial lobe).\nTarget: Left Upper Lobe.\nImplants: 3 Zephyr valves.\nVerification: Visual inspection confirmed segmental occlusion.\nNote: Chartis done previously (not billed this session).",
            4: "Procedure: BLVR LUL\nPatient: Robert James\nSteps:\n1. GA/ETT.\n2. Scope to LUL.\n3. Placed 3 Zephyr valves.\n4. Checked fit.\nPlan: Admit, serial CXRs.",
            5: "put valves in for mr james today left upper lobe used the zephyr ones three of them total fit looked good blocked off the airways no bleeding sent him to the floor watch for pneumo.",
            6: "Bronchoscopic lung volume reduction was performed on the left upper lobe. Three Zephyr valves were placed in the segmental bronchi. Complete occlusion was achieved. There were no intra-procedure complications. Post-procedure chest x-ray was negative for pneumothorax.",
            7: "[Indication]\nSevere emphysema, LUL target.\n[Anesthesia]\nGeneral.\n[Description]\n3 Zephyr valves deployed in LUL. Lobar occlusion confirmed.\n[Plan]\nAdmit. Monitor for pneumothorax.",
            8: "Mr. James had his valve procedure today. We placed three valves in his left upper lobe to help shrink the emphysema. The valves went in smoothly and blocked the airways as intended. We'll keep him in the hospital for a few days to make sure his lung doesn't collapse (pneumothorax) as it shrinks.",
            9: "Procedure: Deployment of bronchial valves.\nTarget: Left Upper Lobe.\nDevice: Zephyr.\nOutcome: Lobar isolation achieved."
        },
        7: { # Angela Rivera (TPC 32550)
            1: "Indication: Recurrent malignant effusion.\nProcedure: Tunneled Pleural Catheter (Right).\nAction: US guidance. Tunnel created. Catheter placed. 1.5L drained.\nComplications: None.\nPlan: Home health drainage.",
            2: "PROCEDURE: Insertion of Tunneled Indwelling Pleural Catheter.\nMs. Rivera, with metastatic breast cancer and recurrent right pleural effusion, underwent catheter placement. Ultrasound identified the fluid pocket. Under local anesthesia and moderate sedation, a subcutaneous tunnel was created, and the catheter was introduced into the pleural space using the Seldinger technique. Good flow was obtained. The cuff was positioned within the tunnel.",
            3: "Code: 32550 (Insertion of indwelling tunneled pleural catheter with cuff).\nGuidance: Ultrasound.\nDrainage: 1.5L removed.\nDetails: Cuff placed in tunnel. Suture secured. No sclerosis performed.",
            4: "Procedure: PleurX Placement\nPatient: Angela Rivera\nSteps:\n1. US check.\n2. Local/Sedation.\n3. Tunnel made.\n4. Catheter in pleural space.\n5. Drained 1.5L.\nPlan: Discharge with visiting nurse.",
            5: "placed a tunneled catheter for angela rivera she has breast cancer and fluid on the right lung used ultrasound to find the spot numbed her up tunneled the line under the skin put it in drained a liter and a half fluid looks bloody but drained well script for home health.",
            6: "Ultrasound-guided placement of a right tunneled pleural catheter was performed for malignant effusion. A subcutaneous tunnel was created. The catheter was advanced into the pleural space. 1.5 liters of fluid were drained. The catheter was secured. Post-procedure CXR confirmed position.",
            7: "[Indication]\nMalignant pleural effusion.\n[Anesthesia]\nModerate sedation/Local.\n[Description]\nRight TPC placed via tunnel. US guidance used. 1.5L drained.\n[Plan]\nHome drainage education.",
            8: "Ms. Rivera needed a permanent drain for the fluid around her lung. We used ultrasound to guide us and placed a tunneled catheter on her right side. We drained about 1.5 liters of fluid during the procedure. We'll set her up with home nursing to help her drain it daily at home.",
            9: "Procedure: Implantation of pleural drainage device.\nType: Tunneled, cuffed catheter.\nGuidance: Sonographic.\nOutput: 1500mL serosanguinous fluid."
        },
        8: { # Marcus Hill (Thoracentesis 32555)
            1: "Indication: Left effusion.\nProcedure: US-guided thoracentesis.\nAction: Needle inserted. 1.2L clear yellow fluid removed.\nComplications: None.\nPlan: Fluid analysis.",
            2: "PROCEDURE: Therapeutic Thoracentesis.\nMr. Hill presented with a symptomatic left pleural effusion. Bedside ultrasound confirmed a safe pocket. Under local anesthesia, a catheter was introduced into the pleural space. 1.2 liters of straw-colored fluid were evacuated. The catheter was withdrawn without complication. Post-procedure imaging showed improvement.",
            3: "Code: 32555 (Thoracentesis with imaging guidance).\nGuidance: Ultrasound (documented).\nVolume: 1.2L.\nAnalysis: Sent for cell count, culture, chemistries.",
            4: "Procedure: Thoracentesis\nPatient: Marcus Hill\nSteps:\n1. US marked site.\n2. Lidocaine.\n3. Catheter in.\n4. Drained 1.2L.\n5. Bandage applied.\nPlan: Check labs.",
            5: "tapped mr hills left lung today he had a decent size effusion used the ultrasound to guide it pulled out 1.2 liters fluid looked like transudate maybe or plain exudate sent it to lab patient feels better breathing easier.",
            6: "Ultrasound-guided therapeutic thoracentesis was performed on the left hemithorax. 1.2 L of clear yellow fluid was removed. The patient tolerated the procedure well. No pneumothorax was noted on post-procedure films.",
            7: "[Indication]\nSymptomatic left effusion.\n[Anesthesia]\nLocal.\n[Description]\nUS-guided thoracentesis. 1.2L removed.\n[Plan]\nFluid studies pending.",
            8: "We performed a thoracentesis on Mr. Hill to help his breathing. Using ultrasound, we found the fluid on the left side. We numbed the skin and inserted a small tube, draining 1.2 liters of fluid. He felt immediate relief. We sent the fluid to the lab to see if it's from an infection.",
            9: "Procedure: Pleural aspiration.\nGuidance: Sonography.\nVolume: 1200mL.\nAnalysis: Diagnostic and therapeutic."
        },
        9: { # Charles Young (Medical Thoracoscopy 32650)
            1: "Indication: Recurrent effusion.\nProcedure: Medical Thoracoscopy + Talc.\nFindings: Nodular pleura. 1.8L fluid.\nAction: Biopsies taken. 4g Talc poudrage.\nPlan: Chest tube to suction.",
            2: "PROCEDURE: Medical Thoracoscopy with Pleurodesis.\nMr. Young underwent rigid thoracoscopy for a recurrent malignant effusion. Inspection of the left pleural space revealed diffuse parietal nodularity. Biopsies were obtained. To prevent recurrence, talc poudrage (4 grams) was performed under direct visualization. A 24 Fr chest tube was placed.",
            3: "Code: 32650 (Thoracoscopy with pleurodesis).\nIncludes: 32601 (diagnostic) and 32604 (biopsy) as bundled services.\nAgent: Sterile Talc.\nOutcome: Fluid evacuated, pleurodesis agent applied.",
            4: "Procedure: Thoracoscopy/Talc\nPatient: Charles Young\nSteps:\n1. GA/Double lumen tube.\n2. Trocar in.\n3. Drained fluid.\n4. Biopsied nodules.\n5. Sprayed Talc.\n6. Chest tube placed.\nPlan: Admit.",
            5: "did a scope in the chest for mr young medical thoracoscopy drained the fluid took some biopsies of the bumps on the pleura sprayed talc in there to stick the lung up chest tube is in place suction -20.",
            6: "Medical thoracoscopy was performed on the left side. 1.8 L of fluid was evacuated. Parietal pleural nodules were biopsied. Talc poudrage was performed for pleurodesis. A chest tube was placed at the conclusion of the procedure.",
            7: "[Indication]\nRecurrent malignant effusion.\n[Anesthesia]\nGeneral (OLV).\n[Description]\nThoracoscopy. Biopsies of pleura. Talc poudrage (4g).\n[Plan]\nChest tube management.",
            8: "We took Mr. Young to the OR for a thoracoscopy. We put a camera into his chest cavity, drained the fluid, and saw widespread cancer nodules on the lining of the chest wall. We took samples of these. Then, we sprayed sterile talc powder everywhere inside to glue the lung to the wall and stop the fluid from coming back.",
            9: "Procedure: Pleuroscopy with chemical sclerosis.\nFindings: Carcinomatosis.\nIntervention: Tissue sampling and insufflation of sclerosing agent (talc).\nDrainage: Indwelling thoracostomy tube."
        }
    }
    return variations

def get_base_data_mocks():
    # Names are mocked for the 10 notes x 9 styles = 90 entries.
    # Note 0: Maria Lopez
    # Note 1: Daniel Green
    # Note 2: Liam Carter
    # Note 3: Steven Brooks
    # Note 4: Evelyn Martin
    # Note 5: Helen Ortiz
    # Note 6: Robert James
    # Note 7: Angela Rivera
    # Note 8: Marcus Hill
    # Note 9: Charles Young
    
    return [
        {"idx": 0, "orig_name": "Maria Lopez", "orig_age": 64, "names": ["Rosa Diaz", "Elena Gomez", "Sofia Martinez", "Lucia Perez", "Camila Sanchez", "Valeria Torres", "Isabella Ramirez", "Martina Flores", "Gabriela Castillo"]},
        {"idx": 1, "orig_name": "Daniel Green", "orig_age": 71, "names": ["James White", "Robert Black", "William Brown", "David Gray", "Richard Blue", "Joseph Silver", "Thomas Gold", "Charles Rose", "Henry Violet"]},
        {"idx": 2, "orig_name": "Liam Carter", "orig_age": 5, "names": ["Noah Smith", "Oliver Jones", "Elijah Williams", "Lucas Brown", "Mason Davis", "Logan Miller", "Ethan Wilson", "Aiden Moore", "Jackson Taylor"]},
        {"idx": 3, "orig_name": "Steven Brooks", "orig_age": 67, "names": ["Paul Fisher", "Mark Hunter", "Donald King", "George Wright", "Kenneth Lopez", "Steven Hill", "Edward Scott", "Brian Green", "Ronald Adams"]},
        {"idx": 4, "orig_name": "Evelyn Martin", "orig_age": 72, "names": ["Doris Baker", "Florence Nelson", "Mildred Carter", "Lillian Mitchell", "Alice Roberts", "Ruby Phillips", "Ethel Campbell", "Edith Parker", "Hazel Evans"]},
        {"idx": 5, "orig_name": "Helen Ortiz", "orig_age": 68, "names": ["Martha Cruz", "Frances Reyes", "Ann Morales", "Jean Gutierrez", "Gloria Ortiz", "Catherine Ramos", "Diane Ruiz", "Julie Alvarez", "Marilyn Mendoza"]},
        {"idx": 6, "orig_name": "Robert James", "orig_age": 73, "names": ["Walter Thomas", "Frank Jackson", "Harry White", "Arthur Harris", "Fred Martin", "Albert Thompson", "Jack Garcia", "Raymond Martinez", "Joe Robinson"]},
        {"idx": 7, "orig_name": "Angela Rivera", "orig_age": 59, "names": ["Lisa Clark", "Nancy Rodriguez", "Karen Lewis", "Betty Lee", "Helen Walker", "Sandra Hall", "Donna Allen", "Carol Young", "Ruth Hernandez"]},
        {"idx": 8, "orig_name": "Marcus Hill", "orig_age": 66, "names": ["Anthony Wright", "Kevin King", "Jason Scott", "Jeff Green", "Timothy Baker", "Gary Adams", "Larry Nelson", "Frank Hill", "Scott Campbell"]},
        {"idx": 9, "orig_name": "Charles Young", "orig_age": 74, "names": ["Samuel Mitchell", "Benjamin Roberts", "Patrick Phillips", "Dennis Evans", "Jerry Turner", "Tyler Parker", "Aaron Collins", "Henry Edwards", "Douglas Stewart"]},
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
            # Handle cases where variations might be missing (safety check)
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                note_entry["note_text"] = f"Error: Variation not found for note {idx}, style {style_num}"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            
            # Update the top-level note text for Name/DOB consistency if present in the text (simple string replacement if easy, 
            # otherwise relying on the fact that the variations usually abstract the name or use the new name implicitly 
            # via the 'variations' dict hardcoding. However, the variations dict provided DOES NOT include the new names dynamically.
            # To make this robust, we will do a simple replace of the original name with the new name in the text 
            # if the text happens to contain the name placeholder or we just trust the variation text).
            # The variation text hardcoded above generally uses the patient name or generic terms. 
            # *Correction*: The variation text hardcoded in `get_variations` uses specific names (e.g., "Mr. Green").
            # To be perfectly distinct, we should replace the hardcoded names in `variations` with `new_name`.
            # For simplicity in this generated script, we will assume the style text is 'base' and we replace the Name if it appears.
            
            # Strategy: Replace the Original Name with New Name in the variation text
            # This is a bit tricky since the variation text in the dictionary above uses specific names (like "Liam Carter").
            # We will perform a replacement:
            current_text = note_entry["note_text"]
            # To do this safely, we map the "hardcoded" name in the variation string to the "new_name".
            # Note 0: Uses "Maria Lopez" or "Ms. Lopez" -> Replace with new_name / split name
            # Note 1: Uses "Daniel Green" or "Mr. Green"
            # Note 2: Uses "Liam Carter" or "Liam"
            # Note 3: Uses "Steven Brooks" or "Mr. Brooks"
            # Note 4: Uses "Evelyn Martin" or "Ms. Martin"
            # Note 5: Uses "Helen Ortiz" or "Mrs. Ortiz"
            # Note 6: Uses "Robert James" or "Mr. James"
            # Note 7: Uses "Angela Rivera" or "Ms. Rivera"
            # Note 8: Uses "Marcus Hill" or "Mr. Hill"
            # Note 9: Uses "Charles Young" or "Mr. Young"
            
            orig_first, orig_last = record['orig_name'].split(' ')
            new_first, new_last = new_name.split(' ')
            
            current_text = current_text.replace(record['orig_name'], new_name)
            current_text = current_text.replace(record['orig_name'].lower(), new_name.lower()) # For sloppy dictation
            current_text = current_text.replace(orig_last, new_last) # Replace Last Name references
            current_text = current_text.replace(orig_first, new_first) # Replace First Name references
            
            note_entry["note_text"] = current_text

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
    output_filename = output_dir / "synthetic_blvr_notes_part_047.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()