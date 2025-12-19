import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_079.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILE = "synthetic_cao_notes_part_079.json"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Pre-generated variations for the 10 notes in part_079.
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Ian Murphy (Left mainstem tumor)
            1: "Procedure: Rigid Bronchoscopy.\nIndication: LMS obstruction, RCC met.\nAction:\n- Rigid scope introduced.\n- Polypoid tumor 80% obstruction LMS.\n- Mech debulking: coring, forceps, suction.\n- Microdebrider for residuals.\n- Hemostasis: Iced saline, epi, tamponade.\nResult: Lumen 75% patent (25% residual).\nPlan: MICU. Obs.",
            2: "OPERATIVE NARRATIVE: The patient, presenting with metastatic renal cell carcinoma, underwent rigid bronchoscopy for palliative airway restoration. Upon visualization, a vascular polypoid mass was identified originating from the lateral wall of the proximal left mainstem bronchus, compromising the lumen by approximately 80%. Mechanical debulking was executed utilizing the rigid barrel for coring, complemented by forceps extraction. Subsequent fine-tuning was achieved via microdebrider to excise residual neoplastic tissue. Hemostasis was challenging but secured using cold saline lavage, topical epinephrine, and rigid barrel tamponade. The final result yielded a significantly improved lumen with an estimated 25% residual narrowing.",
            3: "Procedure Code: 31640 (Bronchoscopy with excision of tumor).\nTechnique:\n1. Rigid bronchoscope insertion under GA.\n2. Identification of obstructing tumor (Left Mainstem).\n3. Mechanical excision performed using rigid coring technique.\n4. Microdebrider tool utilized to shave residual tissue to base.\n5. Forceps used for removal of debris.\nNote: No stent placed (excludes 31631).",
            4: "Resident Note\nPatient: Ian Murphy\nProcedure: Rigid Bronchoscopy with Debulking\nAttending: Dr. Ramos\n\nProcedure Steps:\n1. Time out performed.\n2. General anesthesia induced. Rigid scope inserted.\n3. Left mainstem tumor visualized (80% block).\n4. Tumor debulked using coring and microdebrider.\n5. Bleeding controlled with saline/epi.\n6. Good airway caliber achieved.\nPlan: ICU for monitoring.",
            5: "op report patient Ian Murphy we did a rigid bronchoscopy today for the left mainstem tumor... went in with the rigid scope saw the mass blocking about 80 percent used the barrel to core it out and then the microdebrider to clean it up got most of it out maybe 25 percent left there was some bleeding pretty brisk but we stopped it with ice saline and holding pressure with the scope sent him to MICU kept him intubated thanks.",
            6: "Left mainstem obstruction from metastatic renal cell carcinoma with dyspnea and post-obstructive pneumonia. Rigid bronchoscopy with mechanical debulking of left mainstem tumor. General anesthesia with rigid bronchoscopy. Polypoid vascular tumor arising from lateral wall of proximal left mainstem causing ~80% lumen compromise; purulent secretions distally. Tumor was debulked mechanically using rigid coring, suction, and forceps. A microdebrider was used to excise residual tumor tissue until a near-circular lumen was achieved. Multiple tumor fragments were removed and sent for pathology. Residual narrowing estimated at 25%; no stent placed due to anticipated systemic therapy response. Brisk bleeding during initial passes controlled with iced saline, topical epinephrine, and temporary tamponade with the rigid barrel. Remained intubated and transferred to the MICU for overnight observation and treatment of pneumonia.",
            7: "[Indication]\nLeft mainstem obstruction, metastatic RCC, post-obstructive pneumonia.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nRigid scope advanced. 80% obstruction of LMS identified. Mechanical debulking performed via coring, forceps, and microdebrider. Bleeding managed with tamponade and epinephrine. Lumen restored to 75% patency.\n[Plan]\nMICU admission. Antibiotics.",
            8: "The patient was brought to the operating room for a rigid bronchoscopy to address a left mainstem obstruction caused by metastatic renal cell carcinoma. Under general anesthesia, we identified a vascular tumor blocking 80% of the airway. We proceeded to debulk the tumor mechanically, using the rigid scope to core through the mass and forceps to remove the debris. A microdebrider was then used to smooth the airway walls. We encountered some brisk bleeding which was managed effectively with iced saline and epinephrine. By the end of the procedure, the airway was largely patent.",
            9: "Procedure: Rigid bronchoscopy with physical removal of left mainstem mass.\nIndication: Airway blockage from metastatic renal cell cancer.\nDetails: A polypoid growth was seen on the lateral wall of the left mainstem. The mass was extracted using rigid coring and forceps. A microdebrider excised the remaining tissue. Bleeding was halted with cold saline and pressure. The airway was opened significantly."
        },
        1: { # Doris Hill (Bronchus Intermedius tumor)
            1: "Indication: BI obstruction (NSCLC).\nProcedure: Rigid bronchoscopy, mechanical debulking.\nFindings: Exophytic tumor BI, 75% occlusion.\nAction: Cored with rigid barrel. Microdebrider used for cleanup.\nResult: 30% residual narrowing. No stent.\nComplications: Mild bleeding.\nDisp: Floor.",
            2: "PROCEDURE NOTE: The patient underwent rigid bronchoscopy for the management of a symptomatic obstruction in the bronchus intermedius secondary to non-small cell lung cancer. Upon airway inspection, an exophytic neoplasm was visualized distal to the right upper lobe takeoff, occluding approximately 75% of the lumen. Mechanical debulking was undertaken utilizing the bevel of the rigid bronchoscope for coring, followed by microdebridement to ensure a smooth endoluminal surface. The procedure successfully re-established airway patency, leaving approximately 30% residual stenosis.",
            3: "Service: Bronchoscopy with tumor excision (31640).\nLocation: Bronchus Intermedius (Right Lung).\nMethod: Mechanical debulking via Rigid Bronchoscopy.\nTools: Rigid barrel, suction, forceps, microdebrider.\nOutcome: Reduction of obstruction from 75% to 30%.\nMedical Necessity: Recurrent post-obstructive pneumonia.",
            4: "Procedure Note\nPatient: Doris Hill, 74F\nProcedure: Rigid Bronchoscopy/Debulking\nSteps:\n1. Anesthesia induction.\n2. Rigid scope placed.\n3. Identified tumor in Bronchus Intermedius.\n4. Mechanically debulked with forceps/suction/microdebrider.\n5. Hemostasis achieved.\n6. Patient extubated.\nComments: Good result, airway open.",
            5: "Doris Hill 74 female with NSCLC obstructing the bronchus intermedius rigid bronch was done today under general anesthesia... saw the tumor blocking about 75 percent or so used the rigid tube to core it out and suctioned the pieces microdebrider used too final result looked good maybe 30 percent narrowing left no stent needed mild bleeding only stopped with saline admitted to floor.",
            6: "Right bronchus intermedius obstruction from non-small cell lung cancer with recurrent post-obstructive pneumonia. Rigid bronchoscopy with mechanical debulking of tumor in bronchus intermedius. General anesthesia with rigid bronchoscopy. Exophytic tumor in bronchus intermedius just distal to right upper lobe takeoff causing ~75% obstruction with distal mucous plugging. Mechanical debulking was performed using the rigid barrel, suction, and forceps to core out tumor and remove large fragments. A microdebrider was then used to excise residual tumor and smooth the airway wall. Final airway lumen had ~30% residual narrowing; no stent was placed. Mild bleeding controlled with cold saline and dilute epinephrine. Extubated in OR and admitted to medical floor for pneumonia management.",
            7: "[Indication]\nNSCLC obstruction of Bronchus Intermedius.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\n75% occlusion of BI found. Mechanical debulking performed using rigid coring and microdebrider. Airway caliber improved to 30% residual stenosis. Distal mucous cleared.\n[Plan]\nAdmit to floor. Pneumonia management.",
            8: "We performed a rigid bronchoscopy on Ms. Hill to treat a tumor obstructing her bronchus intermedius. After inducing anesthesia, we located the tumor which was blocking about 75% of the airway. We used the rigid scope to mechanically remove the bulk of the tumor and then used a microdebrider to clean up the edges. The airway was significantly opened up, with only about 30% narrowing remaining. She tolerated the procedure well with minimal bleeding.",
            9: "Procedure: Rigid bronchoscopy with physical resection of tumor in bronchus intermedius.\nFindings: Growth in the airway causing 75% blockage.\nIntervention: The mass was cored out using the rigid scope. Remaining tissue was shaved with a microdebrider. The airway was cleared.\nResult: Airway flow restored."
        },
        2: { # Anthony Green (Distal trachea + Stent)
            1: "Dx: Critical distal tracheal obstruction (95%).\nProc: Rigid bronch, debulking, silicone stent (14x40mm).\nAction: Aggressive debulking (coring/microdebrider). Stent deployed over carina.\nResult: Patent airway. 30% residual narrowing of lumen, flow restored.\nPlan: ICU, intubated.",
            2: "OPERATIVE REPORT: Mr. Green presented with impending respiratory failure due to a critical distal tracheal obstruction. Rigid bronchoscopy was performed under general anesthesia. A bulky exophytic tumor was noted obstructing 95% of the distal trachea. Aggressive mechanical debulking was performed to recanalize the airway. Following this, a 14 x 40 mm silicone Y-stent (tracheal) was deployed to bridge the carinal involvement. Post-procedure evaluation confirmed stent expansion and restoration of ventilation to both mainstem bronchi.",
            3: "CPT Codes: 31640 (Tumor excision), 31631 (Tracheal stent placement).\nJustification: 95% obstruction required excision to create space for stent.\nDevice: Silicone tracheal stent (14x40mm).\nMethod: Rigid bronchoscopy with balloon dilation and guidewire deployment.\nOutcome: Airway patency restored.",
            4: "Resident Procedure Note\nPatient: Anthony Green\nProcedure: Rigid Bronch, Debulking, Stent\nSteps:\n1. GA/Jet vent.\n2. Rigid scope to trachea.\n3. 95% obstruction visualized.\n4. Debulked with coring/forceps.\n5. Placed 14x40mm silicone stent.\n6. Confirmed position.\nComplications: Mild bleeding.\nDisposition: ICU.",
            5: "Anthony Green 68M critical airway obstruction distal trachea... we went in with the rigid scope saw 95 percent blockage barely any air moving debulked it aggressively with the coring and the microdebrider then we put in a silicone stent 14 by 40 mm right over the lesion bridging the carina looks much better now airway open patient sent to ICU intubated.",
            6: "Distal tracheal tumor with near-critical obstruction and impending respiratory failure. Rigid bronchoscopy with mechanical debulking of tracheal tumor and silicone tracheal stent placement. General anesthesia with rigid bronchoscopy; anesthesia team present. Bulky exophytic tumor at distal trachea extending to carina causing ~95% obstruction; right mainstem partially involved; significant work of breathing pre-procedure. Aggressive mechanical debulking was performed using rigid coring, suction, forceps, and microdebrider until a patent lumen was created. Multiple tumor fragments were removed and sent for histology. A 14 x 40 mm silicone stent was then deployed across the distal tracheal lesion, bridging the carina, with good expansion and coverage. Final lumen showed approximately 30% residual narrowing but robust airflow to both mainstem bronchi. Mild bleeding controlled with iced saline and topical epinephrine; no major complications. Remained intubated and transferred to ICU for close airway monitoring.",
            7: "[Indication]\nCritical distal tracheal obstruction (95%).\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nMassive tumor debulked mechanically to restore lumen. 14x40mm silicone stent deployed covering distal trachea and carina. Good expansion noted.\n[Plan]\nICU. Monitor airway.",
            8: "Mr. Green was in critical condition with a tumor blocking almost his entire windpipe. We performed an emergency rigid bronchoscopy. Once we visualized the tumor, we aggressively removed the bulk of it using coring and suction to open up the airway. To keep it open, we placed a silicone stent across the affected area in the distal trachea. The airflow improved dramatically immediately after the stent was placed.",
            9: "Procedure: Rigid bronchoscopy with mechanical removal of tracheal mass and insertion of airway prosthesis.\nAction: Severe blockage was cleared by scraping and suctioning the growth. A silicone tube was implanted to maintain airway patency.\nResult: Breathing passage restored."
        },
        3: { # Nina Alvarez (Tracheal granulation)
            1: "Indication: Tracheal granulation (post-radiation).\nProcedure: Flex/Rigid bronch, resection.\nFindings: Anterior pedunculated lesion, 60% narrowing.\nAction: Snare resection, microdebrider, rigid coring.\nResult: 15% residual. No stent.\nDisp: Home.",
            2: "PROCEDURE: The patient underwent combined flexible and rigid bronchoscopy for the management of benign tracheal stenosis secondary to post-radiation granulation tissue. A pedunculated polypoid lesion was identified on the anterior tracheal wall. The lesion was resected en bloc using a snare, followed by mucosal smoothing with a microdebrider and rigid coring. The intervention successfully increased the airway caliber, leaving minimal residual irregularity.",
            3: "Code: 31640 (Bronchoscopy with excision of tumor/tissue).\nPathology: Granulation tissue (Benign).\nLocation: Trachea (anterior wall).\nTechnique: Snare resection and Microdebrider.\nOutcome: Restoration of airway lumen from 60% obstruction to 15%.",
            4: "Procedure Note\nPatient: Nina Alvarez\nProcedure: Tracheal Resection\nSteps:\n1. Anesthesia.\n2. Rigid scope insertion.\n3. Found granulation tissue anterior trachea.\n4. Snared and debrided.\n5. Suctioned fragments.\n6. Extubated.\nPlan: Discharge home.",
            5: "Nina Alvarez here for the tracheal granulation tissue post radiation... did a rigid and flex bronch saw the polyp on the anterior wall blocking about 60 percent used a snare to cut it off then the microdebrider to smooth it down looks good now only maybe 15 percent narrowing left no bleeding patient woke up fine going home.",
            6: "Post-radiation polypoid granulation tissue in trachea causing exertional dyspnea and cough. Flexible and rigid bronchoscopy with mechanical resection of tracheal granulation tissue. General anesthesia with ETT. Pedunculated polypoid tissue on anterior tracheal wall ~3 cm above carina causing ~60% narrowing; surrounding mucosa fibrotic. Lesion was grasped and removed using snare resection, followed by microdebrider shaving of residual granulation and rigid coring to smooth the airway. Small fragments were suctioned and sent to pathology. Final lumen with ~15% residual narrowing; no stent placed. Minimal bleeding controlled with cold saline. Extubated in OR and discharged to home the same day after observation.",
            7: "[Indication]\nSymptomatic tracheal granulation tissue.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nPolypoid lesion anterior trachea resected via snare and microdebrider. Rigid coring used to smooth mucosa. Airway patent.\n[Plan]\nDischarge. Follow-up 6-8 weeks.",
            8: "Ms. Alvarez had some scar tissue growing in her trachea after radiation treatment. We performed a bronchoscopy to remove it. We found a polyp-like growth blocking part of her airway. We used a snare tool to grab and remove it, then smoothed out the area with a microdebrider. The airway looks much clearer now, and she went home the same day.",
            9: "Procedure: Rigid bronchoscopy with excision of tracheal growth.\nFindings: Tissue mass causing airway narrowing.\nAction: The growth was snipped and shaved down using specialized tools. The airway wall was smoothed.\nResult: Improved airflow."
        },
        4: { # James Porter (Left mainstem carcinoid)
            1: "Dx: LMS carcinoid.\nProc: Rigid bronch, excision.\nFindings: Pedunculated lesion medial wall LMS, 65% obstruction.\nAction: Snare resection, coring, microdebrider.\nResult: Margins clear. Lumen restored.\nPlan: Ward. Surveillance.",
            2: "OPERATIVE NARRATIVE: Mr. Porter underwent rigid bronchoscopy for a surveillance-detected left mainstem carcinoid tumor. The lesion was pedunculated and vascular, arising from the medial wall. Complete resection was achieved utilizing a snare technique for the stalk, followed by rigid coring and microdebridement of the base. Gross examination suggests clear margins with restoration of the airway lumen.",
            3: "Service: Bronchoscopy with excision (31640).\nDiagnosis: Carcinoid Tumor (Left Mainstem).\nMethod: Mechanical excision (Snare + Microdebrider).\nDetail: En bloc resection of stalk, base debrided.\nComplications: None significant.",
            4: "Resident Note\nPatient: James Porter\nProcedure: Carcinoid resection\nSteps:\n1. GA, Rigid bronch.\n2. Located tumor LMS.\n3. Snared stalk.\n4. Microdebrider to base.\n5. Sent to path.\n6. Hemostasis with epi.\nPlan: Floor.",
            5: "James Porter 52M with the carcinoid in the left main... went in with rigid scope saw the smooth vascular lesion on the medial wall snared it off and then used the coring and microdebrider to clean the base looks like we got it all bleeding was mild stopped with ice saline extubated fine.",
            6: "Left mainstem endobronchial carcinoid tumor discovered on surveillance CT with intermittent hemoptysis. Rigid bronchoscopy with mechanical excision of carcinoid tumor. General anesthesia with rigid bronchoscopy. Smooth, vascular, pedunculated lesion arising from the medial wall of proximal left mainstem bronchus causing ~65% obstruction; distal lung aerated. Tumor stalk was snared and resected en bloc, followed by rigid coring and microdebrider removal of residual tissue at the base. Margins appeared grossly clear. Specimen sent for histology. Airway lumen restored with ~10–15% residual irregularity. Mild bleeding controlled with iced saline and topical epinephrine. Extubated in OR and discharged to ward in stable condition.",
            7: "[Indication]\nLMS Carcinoid tumor, hemoptysis.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nPedunculated tumor resected en bloc with snare. Base debrided. Airway patent. Hemostasis achieved.\n[Plan]\nAdmit. Surveillance.",
            8: "Mr. Porter had a carcinoid tumor in his left main bronchial tube. We performed a rigid bronchoscopy to remove it. The tumor was attached by a stalk, so we were able to snare it and remove it in one piece. We then cleaned up the base where it was attached to ensure we got all the tumor cells. The airway is now open, and he is doing well.",
            9: "Procedure: Rigid bronchoscopy with ablation of carcinoid mass.\nAction: The growth was looped and severed. The remaining tissue base was shaved down.\nResult: The bronchial tube was cleared of obstruction."
        },
        5: { # Harriet Cole (Bronchus Intermedius tumor)
            1: "Indication: BI tumor, acute dyspnea.\nAction: Rigid bronch, mechanical debulking.\nFindings: 85% obstruction BI.\nIntervention: Coring, suction, microdebrider.\nResult: 30% residual. No stent.\nPlan: Oncology.",
            2: "PROCEDURE: Rigid bronchoscopy was indicated for Ms. Cole due to acute dyspnea secondary to a bronchus intermedius neoplasm. The tumor was found to be friable and irregular, occluding 85% of the lumen. Mechanical debulking was performed via rigid coring and microdebridement. This intervention successfully reduced the tumor burden, resulting in a patent airway with approximately 30% residual narrowing suitable for systemic therapy.",
            3: "Code: 31640 (Bronchoscopy w/ excision).\nSite: Bronchus Intermedius.\nTech: Mechanical debulking.\nJustification: 85% obstruction causing symptoms.\nOutcome: Deobliteration of airway.",
            4: "Procedure Note\nPatient: Harriet Cole\nProcedure: BI Debulking\nSteps:\n1. Anesthesia.\n2. Rigid scope.\n3. Cored out tumor in BI.\n4. Microdebrider used.\n5. Bleeding controlled.\n6. Extubated.\nPlan: Oncology admit.",
            5: "Harriet Cole 62F with the BI tumor causing wheezing... did a rigid bronch today saw the mass blocking 85 percent cored it out with the barrel and used the microdebrider to get the rest bleeding was mild stopped with epi no stent put in because shes starting chemo soon.",
            6: "Bronchus intermedius tumor with acute worsening dyspnea and wheeze. Rigid bronchoscopy with mechanical debulking of tumor. General anesthesia with rigid bronchoscopy. Irregular friable tumor occupying ~85% of the bronchus intermedius lumen with distal mucous plugging. Tumor was cored out mechanically using the rigid barrel; large fragments were removed with suction and forceps. A microdebrider was used to excise residual tumor along the airway wall. Final lumen with ~30% residual narrowing; no stent was placed due to anticipated systemic therapy. Mild bleeding controlled with cold saline and topical epinephrine. Extubated in OR and admitted to oncology ward.",
            7: "[Indication]\nSymptomatic BI tumor obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\n85% obstruction reduced to 30% via mechanical coring and microdebridement. Distal airways cleared.\n[Plan]\nOncology ward. Systemic therapy.",
            8: "Ms. Cole was having trouble breathing due to a tumor in her airway. We used a rigid bronchoscope to manually remove the bulk of the tumor from the bronchus intermedius. We scraped out the tumor cells and suctioned them away. We managed to clear most of the blockage, leaving enough room for her to breathe comfortably while she waits for chemotherapy.",
            9: "Procedure: Rigid bronchoscopy with physical reduction of airway mass.\nAction: The obstruction in the intermediate bronchus was hollowed out using the scope. Remaining tissue was trimmed.\nResult: Airway caliber significantly improved."
        },
        6: { # Walter Young (Emergent Carina tumor)
            1: "Indication: Emergent airway obstruction (>90%).\nProcedure: Rigid bronch, rapid debulking.\nFindings: Tumor at distal trachea/carina.\nAction: Rigid coring, forceps. No stent (unstable).\nResult: Airway patent (35% residual).\nPlan: MICU, intubated.",
            2: "OPERATIVE REPORT: Mr. Young presented in extremis with critical central airway obstruction involving the distal trachea and carina. Emergency rigid bronchoscopy was performed. A large friable tumor was identified causing >90% occlusion. Rapid mechanical debulking was executed using the rigid scope and forceps to re-establish ventilation. Although a stent was considered, the patient's hemodynamic instability necessitated termination of the procedure once a patent airway (approx. 60-70% caliber) was achieved.",
            3: "Code: 31640 (Tumor excision).\nContext: Emergent.\nSite: Distal Trachea/Carina.\nMethod: Mechanical debulking (Coring/Forceps).\nNote: No stent placed due to patient stability issues.",
            4: "Resident Note\nPatient: Walter Young\nProcedure: Emergent Debulking\nSteps:\n1. Stat rigid bronch.\n2. Massive tumor at carina.\n3. Cored out to get air.\n4. Suctioned secretions.\n5. Pt unstable (hypotension).\n6. Stopped after airway open.\nPlan: MICU.",
            5: "Walter Young 80M emergent case critical airway... massive tumor at the carina blocking everything we went in fast with the rigid scope cored it out grabbed pieces with forceps just trying to get an airway he got hypotensive so we stopped once we had flow didn't put a stent in sent to MICU intubated.",
            6: "Emergent central airway obstruction from endobronchial tumor with acute respiratory distress. Emergent rigid bronchoscopy with mechanical debulking of tracheal and carinal tumor. General anesthesia with rigid bronchoscopy. Large friable tumor occupying distal trachea and carina with involvement of right mainstem, causing >90% obstruction; copious secretions. Rapid mechanical debulking using rigid coring, suction, and forceps was performed to remove obstructing tumor bulk. Microdebrider was used to excise residual tumor at carina. Airway patency restored with ~30–40% residual narrowing; no stent placed due to hemodynamic instability and need for short procedure. Transient hypotension and tachycardia responded to fluids and vasopressors; bleeding moderate but controlled. Remained intubated and transferred to MICU for continued care.",
            7: "[Indication]\nEmergent malignant airway obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nCritical carinal obstruction debulked mechanically. Airway restored. Procedure curtailed due to hypotension.\n[Plan]\nMICU. Stabilize.",
            8: "Mr. Young was brought in as an emergency with a tumor blocking his windpipe. We performed a rapid procedure to clear the blockage using a rigid bronchoscope. We physically removed the tumor pieces blocking the carina to allow air to pass. His blood pressure dropped during the procedure, so we finished as quickly as possible once the airway was open. He is currently in the ICU.",
            9: "Procedure: Emergency bronchoscopic removal of tracheal blockage.\nAction: The mass at the airway fork was scooped out to allow breathing. The procedure was halted early due to instability.\nResult: Breathing passage opened."
        },
        7: { # Chloe Harris (Right Mainstem tumor)
            1: "Indication: RMS tumor.\nProc: Rigid bronch, excision.\nFindings: Sessile lesion, 60% block.\nAction: Snare, coring, microdebrider.\nResult: 10% residual. Clear margins.\nDisp: Home.",
            2: "PROCEDURE NOTE: Ms. Harris underwent rigid bronchoscopy for a right mainstem endobronchial tumor. A sessile lesion was identified on the lateral wall causing partial obstruction. Mechanical excision was performed utilizing a multimodal approach: snare resection for the bulk, followed by rigid coring and microdebridement for the base. The airway lumen was successfully restored with minimal residual irregularity.",
            3: "Service: 31640 (Bronchoscopy/Excision).\nSite: Right Mainstem Bronchus.\nMethod: Snare, Coring, Microdebrider.\nOutcome: Restoration of lumen.\nDisposition: Outpatient.",
            4: "Procedure Note\nPatient: Chloe Harris\nProcedure: RMS Tumor Excision\nSteps:\n1. GA/Rigid scope.\n2. Saw tumor RMS.\n3. Snared and debrided.\n4. Cleaned up base.\n5. No bleeding.\nPlan: Home.",
            5: "Chloe Harris 55F right mainstem tumor incidental finding... rigid bronch today sessile lesion lateral wall blocking 60 percent used the snare then the coring and microdebrider got it all out looks clean minimal bleeding discharge home.",
            6: "Right mainstem endobronchial tumor with cough and wheezing, incidentally found on CT. Rigid bronchoscopy with mechanical excision of right mainstem tumor. General anesthesia with rigid bronchoscopy. Sessile lesion along lateral wall of proximal right mainstem causing ~60% narrowing; no collapse distally. Mechanical debulking using snare resection, rigid coring, and microdebrider was performed. All visible tumor was removed; fragments were sent for histology. Final lumen had ~10% residual irregularity. Minimal bleeding; no hypoxia. Extubated in OR and discharged home after observation.",
            7: "[Indication]\nSymptomatic RMS tumor.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nSessile tumor excised via snare and mechanical tools. Lumen patent. Minimal bleeding.\n[Plan]\nDischarge. Follow up 2 weeks.",
            8: "Ms. Harris had a tumor in her right main bronchial tube causing a cough. We removed it using a rigid bronchoscope. We used a snare to cut the tumor and a microdebrider to smooth the airway wall. The procedure went very well with no complications, and the airway is now clear.",
            9: "Procedure: Rigid bronchoscopy with resection of bronchial mass.\nAction: The growth in the right airway was excised and the area shaved smooth.\nResult: Airway fully opened."
        },
        8: { # Xavier Bennett (Mid-tracheal tumor)
            1: "Indication: Mid-tracheal SCC, dyspnea.\nAction: Rigid bronch debulking.\nFindings: Fungating mass, 75% narrowing.\nIntervention: Coring, snare, microdebrider.\nResult: Patent lumen. No stent.\nPlan: Radiation oncology.",
            2: "OPERATIVE REPORT: Mr. Bennett underwent rigid bronchoscopy for a mid-tracheal squamous cell carcinoma. A fungating posterior wall mass was identified obstructing 75% of the lumen. The tumor was debulked using rigid coring and snare excision techniques. A microdebrider was employed to fine-tune the resection. A patent airway was achieved without the need for stenting, facilitating future radiation therapy.",
            3: "Code: 31640.\nDiagnosis: Tracheal SCC.\nLocation: Mid-trachea.\nProcedure: Mechanical debulking.\nOutcome: 75% -> 25% obstruction.\nPlan: Radiation.",
            4: "Resident Note\nPatient: Xavier Bennett\nProcedure: Tracheal Debulking\nSteps:\n1. Rigid scope.\n2. Mass mid-trachea.\n3. Debulked with coring/snare.\n4. Microdebrider for cleanup.\n5. Hemostasis.\nPlan: Admit, radiation consult.",
            5: "Xavier Bennett 69M mid tracheal SCC... rigid bronchoscopy fungating mass posterior wall blocking 75 percent we cored it out and snared it used the microdebrider too got a good lumen no stent needed because hes getting radiation mild bleeding only.",
            6: "Mid-tracheal squamous cell carcinoma with progressive dyspnea and cough. Rigid bronchoscopy with mechanical debulking of mid-tracheal tumor. General anesthesia with rigid bronchoscopy. Fungating mass on posterior mid-tracheal wall causing ~75% narrowing; distal airways patent. Tumor was debulked using rigid coring, snare excision, and microdebrider until a patent lumen was achieved. Multiple tumor fragments were removed and sent to pathology. No stent was placed given adequate residual lumen and planned radiation. Mild bleeding controlled with cold saline and dilute epinephrine. Extubated in OR and admitted overnight for observation.",
            7: "[Indication]\nMid-tracheal SCC obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nPosterior mass debulked mechanically. Airway patent. No stent placed.\n[Plan]\nOvernight obs. Radiation.",
            8: "Mr. Bennett had a cancer growth in the middle of his windpipe. We used a rigid bronchoscope to remove the tumor. We cut and scraped the tumor away until the airway was open. We didn't put a stent in because the opening is now wide enough and he is scheduled for radiation treatment.",
            9: "Procedure: Rigid bronchoscopy with removal of tracheal obstruction.\nAction: The mass in the windpipe was excised using mechanical tools.\nResult: Breathing tube cleared."
        },
        9: { # Evelyn Ross (Recurrent distal tracheal tumor)
            1: "Indication: Recurrent tracheal tumor post-chemorad.\nProc: Rigid bronch debulking.\nFindings: Nodular tumor distal trachea, 70% block.\nAction: Rigid coring, microdebrider.\nResult: 25% residual. No stent.\nDisp: Floor.",
            2: "PROCEDURE NOTE: Ms. Ross presented with recurrent distal tracheal obstruction following prior chemoradiation. Rigid bronchoscopy revealed an irregular nodular tumor proximal to the carina. Mechanical debulking was performed utilizing the rigid scope and microdebrider to restore airway caliber. The procedure resulted in a patent airway with approximately 25% residual narrowing. Stenting was deferred.",
            3: "Service: 31640 (Excision of tumor).\nSite: Distal trachea.\nContext: Recurrence.\nTechnique: Mechanical debulking.\nOutcome: Improved patency.",
            4: "Procedure Note\nPatient: Evelyn Ross\nProcedure: Tracheal Debulking\nSteps:\n1. GA.\n2. Rigid scope.\n3. Recurrent tumor distal trachea.\n4. Debrided and cored.\n5. Airway open.\nPlan: Oncology f/u.",
            5: "Evelyn Ross 73F recurrent tumor distal trachea after radiation... rigid bronch today nodular tumor blocking 70 percent used the coring and microdebrider to open it up got it down to 25 percent narrowing bleeding was mild no stent this time admitted for observation.",
            6: "Distal tracheal tumor recurrence after chemoradiation with new dyspnea. Rigid bronchoscopy with mechanical debulking of distal tracheal tumor. General anesthesia with rigid bronchoscopy. Irregular nodular tumor at distal trachea just above carina causing ~70% narrowing; prior scar present. Mechanical debulking with rigid coring, microdebrider, and forceps was used to excise tumor tissue and widen the lumen. Multiple fragments removed and sent for pathology. Final lumen with ~25% residual narrowing; no stent placed given adequate caliber and prior radiation changes. Mild bleeding; no hypoxia or pneumothorax. Extubated in OR and admitted overnight for observation.",
            7: "[Indication]\nRecurrent tracheal tumor.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nNodular mass debulked via rigid bronchoscopy. Lumen restored. Hemostasis secured.\n[Plan]\nAdmit. Oncology follow-up.",
            8: "Ms. Ross had a recurrence of her tumor in the lower windpipe. We went in with a rigid bronchoscope and cleaned out the new growth using a microdebrider and coring technique. The airway is open again, and she did not require a stent.",
            9: "Procedure: Rigid bronchoscopy with clearance of recurrent tracheal growth.\nAction: The regrowth in the airway was scraped and removed.\nResult: Airway widened."
        }
    }
    return variations

def get_base_data_mocks():
    # Names and original ages corresponding to the 10 source notes
    return [
        {"idx": 0, "orig_name": "Ian Murphy", "orig_age": 65, "names": ["Robert Cole", "James Sullivan", "Michael Drake", "William Frost", "David Chen", "Richard Wolf", "Thomas Pike", "Charles Gray", "Joseph Black"]},
        {"idx": 1, "orig_name": "Doris Hill", "orig_age": 74, "names": ["Mary Jones", "Patricia Lee", "Linda Wang", "Barbara Scott", "Elizabeth Green", "Jennifer Adams", "Maria Rodriguez", "Susan Kim", "Margaret White"]},
        {"idx": 2, "orig_name": "Anthony Green", "orig_age": 68, "names": ["John Doe", "Robert Smith", "Michael Johnson", "William Brown", "David Miller", "Richard Davis", "Thomas Garcia", "Charles Martinez", "Joseph Robinson"]},
        {"idx": 3, "orig_name": "Nina Alvarez", "orig_age": 67, "names": ["Sarah Clark", "Karen Lewis", "Nancy Walker", "Lisa Hall", "Betty Allen", "Sandra Young", "Ashley Hernandez", "Kimberly King", "Donna Wright"]},
        {"idx": 4, "orig_name": "James Porter", "orig_age": 52, "names": ["Daniel Lopez", "Paul Hill", "Mark Scott", "Donald Green", "George Adams", "Kenneth Baker", "Steven Gonzalez", "Edward Nelson", "Brian Carter"]},
        {"idx": 5, "orig_name": "Harriet Cole", "orig_age": 62, "names": ["Dorothy Mitchell", "Carol Perez", "Ruth Roberts", "Sharon Turner", "Michelle Phillips", "Laura Campbell", "Sarah Parker", "Kimberly Evans", "Jessica Edwards"]},
        {"idx": 6, "orig_name": "Walter Young", "orig_age": 80, "names": ["Ronald Collins", "Anthony Stewart", "Kevin Sanchez", "Jason Morris", "Jeff Rogers", "Frank Reed", "Scott Cook", "Eric Morgan", "Stephen Bell"]},
        {"idx": 7, "orig_name": "Chloe Harris", "orig_age": 55, "names": ["Deborah Murphy", "Amanda Bailey", "Stephanie Rivera", "Rebecca Cooper", "Sharon Richardson", "Cynthia Cox", "Kathleen Howard", "Amy Ward", "Shirley Torres"]},
        {"idx": 8, "orig_name": "Xavier Bennett", "orig_age": 69, "names": ["Larry Peterson", "Jeffrey Gray", "Frank Ramirez", "Scott James", "Eric Watson", "Stephen Brooks", "Andrew Kelly", "Raymond Sanders", "Gregory Price"]},
        {"idx": 9, "orig_name": "Evelyn Ross", "orig_age": 73, "names": ["Judith Bennett", "Helen Wood", "Melissa Barnes", "Deborah Ross", "Amanda Henderson", "Stephanie Coleman", "Rebecca Jenkins", "Sharon Perry", "Cynthia Powell"]}
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
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}")
                continue
            
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

    # Output to JSON
    output_filename = output_dir / OUTPUT_FILE
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()