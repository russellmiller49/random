import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_055.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    # Styles:
    # 1: Terse Surgeon (Brief, bullets)
    # 2: Academic Attending (Formal, detailed)
    # 3: Billing Coder (Technique/Tool focused)
    # 4: Trainee/Resident (Boilerplate steps)
    # 5: Sloppy Dictation (Run-ons, no headers)
    # 6: Header-less (Continuous block)
    # 7: Templated (Rigid structure)
    # 8: Narrative Flow (Prose, no bullets)
    # 9: Synonym Swapper (Verb changes)

    variations = {
        0: { # Note 0: Cynthia Jones (Tracheal Stent)
            1: "Indication: Thyroid cancer, tracheal compression.\nPre-op: 79% stenosis.\nProcedure:\n- Rigid bronchoscopy, jet ventilation.\n- Balloon dilation.\n- Dumon stent (12x60mm) deployed in Trachea.\n- Good expansion confirmed.\nPost-op: 11% obstruction.\nComplications: None.",
            2: "HISTORY: Ms. Jones presented with significant airway compromise secondary to thyroid malignancy. Quantitative assessment revealed 79% tracheal stenosis.\nOPERATIVE NARRATIVE: Under general anesthesia utilizing jet ventilation, the airway was secured via rigid bronchoscopy. Mechanical dilation of the stenotic segment was performed to facilitate appliance delivery. A 12x60mm Novatech Silicone Dumon stent was precisely deployed within the trachea. Post-deployment endoscopic inspection confirmed restoration of airway caliber to near-physiologic dimensions (11% residual narrowing) and excellent stent apposition.\nPLAN: Admitted for observation.",
            3: "Procedure: Bronchoscopy with Tracheal Stent Placement (CPT 31631).\nTechnique:\n1. Introduction of rigid bronchoscope under GA.\n2. Assessment of tracheal stenosis (79%).\n3. Therapeutic dilation performed to prepare site.\n4. Measurement and selection of Novatech Dumon Stent (12x60mm).\n5. Deployment of stent into trachea covering the stenotic region.\n6. Verification of patency and lack of migration.\nNecessity: Malignant neoplasm causing central airway obstruction.",
            4: "Procedure: Rigid Bronchoscopy with Stent Placement\nAttending: Dr. Davis\nSteps:\n1. Time out performed.\n2. General anesthesia with jet ventilation.\n3. Rigid scope inserted.\n4. Tracheal stenosis identified and dilated.\n5. Stent (Dumon 12x60mm) placed in trachea.\n6. Position confirmed.\n7. Scope removed.\nNo complications encountered.",
            5: "Patient Cynthia Jones here for the tracheal stent she has thyroid cancer compressing the airway about 80 percent blocked we used the rigid scope with jet vent dilated it open then put in a novatech dumon stent 12 by 60 millimeter right in the trachea looks good now wide open only maybe 10 percent blocked no bleeding really sent to recovery then admit thanks.",
            6: "The patient presented with thyroid cancer causing tracheal compression. Pre-procedure obstruction was estimated at 79%. Under general anesthesia with jet ventilation, rigid bronchoscopy was performed. Sequential balloon dilation of the tracheal stenosis was carried out. The airway was measured, and a Novatech Silicone Dumon stent (12x60mm) was deployed in the trachea. Stent position was confirmed with good expansion and patency. Post-procedure obstruction was reduced to approximately 11%. There were no complications, and EBL was minimal. The patient was sent to recovery and then admitted for overnight observation.",
            7: "[Indication]\nThyroid cancer with 79% tracheal compression.\n[Anesthesia]\nGeneral with jet ventilation.\n[Description]\nRigid bronchoscopy performed. Stenosis dilated. Novatech Dumon stent (12x60mm) deployed in trachea. Patency restored (11% residual).\n[Plan]\nAdmit for observation. Clinic follow-up 4-6 weeks.",
            8: "Ms. Jones underwent a rigid bronchoscopy today to address her tracheal compression caused by thyroid cancer. We utilized general anesthesia and jet ventilation. After identifying the 79% stenosis, we performed sequential balloon dilation. Subsequently, a 12x60mm Novatech Silicone Dumon stent was deployed into the trachea. The stent expanded well, and we confirmed good patency with a residual obstruction of only 11%. She tolerated the procedure well with minimal blood loss.",
            9: "Indication: Thyroid carcinoma with tracheal impingement.\nPre-procedure blockage: ~79% Trachea.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy was executed. Sequential balloon expansion of the trachea stenosis was conducted. The airway was gauged and a Novatech Silicone - Dumon stent (12x60mm) was implanted in the Trachea. Stent seating was validated with good expansion and openness.\nPost-procedure blockage: ~11%.\nNo adverse events."
        },
        1: { # Note 1: Barbara Robinson (RMS Stent)
            1: "Indication: SCC, airway compromise.\nFindings: 91% RMS obstruction.\nAction:\n- Rigid bronch.\n- Balloon dilation.\n- Novatech Dumon stent (20x50mm) placed in RMS.\nResult: 4% residual obstruction. Patent.\nPlan: Admit.",
            2: "INDICATION: Ms. Robinson, a 62-year-old female with squamous cell carcinoma, presented with critical right mainstem (RMS) stenosis.\nPROCEDURE: The patient was brought to the operating suite and placed under general anesthesia. Rigid bronchoscopy was initiated with jet ventilation. The RMS demonstrated severe 91% obstruction. Following balloon dilation to establish a working channel, a 20x50mm Novatech Silicone Dumon stent was delivered and deployed. Final inspection revealed excellent stent expansion and marked improvement in aeration (4% residual stenosis).\nDISPOSITION: The patient remained stable and was transferred to the floor.",
            3: "Service Performed: 31636 (Bronchoscopy with placement of bronchial stent).\nLocation: Right Mainstem Bronchus.\nDevice: Novatech Silicone Dumon Stent (20x50mm).\nDetails:\n- Rigid bronchoscopy used for access.\n- Stenosis (91%) dilated prior to insertion.\n- Stent positioned across the lesion in the RMS.\n- Confirmation of placement and patency documented.\nOutcome: Improvement from 91% to 4% obstruction.",
            4: "Procedure: Rigid Bronchoscopy, Stent Placement RMS\nPatient: Robinson, Barbara\nStaff: Dr. Anderson\nSteps:\n1. Patient intubated/rigid scope placed.\n2. RMS stenosis identified (91%).\n3. Dilation performed.\n4. Dumon stent 20x50mm placed in Right Mainstem.\n5. Airway patent post-procedure.\nComplications: None.\nPlan: Admit overnight.",
            5: "Procedure note for Barbara Robinson she has squamous cell cancer blocking the right mainstem almost completely 91 percent. We did a rigid bronch under GA dilated it up and then put in a silicone dumon stent size 20 by 50. It opened up beautifully down to like 4 percent obstruction. No issues minimal bleeding sending her to the floor for the night check on her in the morning.",
            6: "Indication was squamous cell carcinoma with airway compromise, specifically a 91% obstruction of the right mainstem. Under general anesthesia with jet ventilation, rigid bronchoscopy was performed. Sequential balloon dilation of the RMS stenosis was completed. The airway was measured and a Novatech Silicone Dumon stent (20x50mm) was deployed in the Right mainstem. Stent position was confirmed with good expansion and patency, resulting in a post-procedure obstruction of 4%. There were no complications and EBL was minimal.",
            7: "[Indication]\nSCC with 91% Right Mainstem obstruction.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nRMS stenosis dilated. Novatech Dumon stent (20x50mm) deployed in RMS. Obstruction reduced to 4%.\n[Plan]\nAdmit overnight. Repeat bronch 4-6 weeks.",
            8: "We performed a rigid bronchoscopy on Ms. Robinson to treat her airway compromise due to squamous cell carcinoma. The right mainstem bronchus was found to be 91% obstructed. We first dilated the area with a balloon and then deployed a 20x50mm Novatech Silicone Dumon stent. The stent sat perfectly, reducing the obstruction to approximately 4% and restoring airflow. The patient had no complications and recovery was uneventful.",
            9: "Indication: Squamous cell carcinoma with airway restriction.\nPre-procedure occlusion: ~91% Right mainstem.\nPROCEDURE: Under general anesthesia with jet ventilation, rigid bronchoscopy was conducted. Sequential balloon expansion of RMS narrowing was performed. The airway was sized and a Novatech Silicone - Dumon stent (20x50mm) was installed in the Right mainstem. Stent location was verified with good opening and flow.\nPost-procedure occlusion: ~4%.\nNo mishaps."
        },
        2: { # Note 2: Betty Green (RMS Covered Stent)
            1: "Dx: Lung adenocarcinoma, CAO.\nTarget: RMS (72% block).\nIntervention:\n- Rigid bronch.\n- Dilation.\n- Aero SEMS Covered stent (16x30mm) deployed.\nOutcome: RMS patent (8% residual).\nPlan: Inpatient obs.",
            2: "HISTORY: Ms. Green presented with central airway obstruction complicating primary lung adenocarcinoma.\nPROCEDURE: Rigid bronchoscopy was undertaken under general anesthesia. The right mainstem bronchus exhibited significant malignant stricture (72%). To restore airway patency, the lesion was dilated, followed by the deployment of a self-expanding metallic stent (Aero SEMS, covered, 16x30mm). The prosthesis expanded appropriately, reducing the obstruction to a clinically insignificant 8%.\nCONCLUSION: Successful palliation of RMS obstruction.",
            3: "Coding Data:\n- Primary Code: 31636 (Bronchial Stent Placement).\n- Device: Aero SEMS (Covered).\n- Dimensions: 16mm x 30mm.\n- Site: Right Mainstem Bronchus.\n- Technique: Rigid bronchoscopy with balloon dilation facilitation.\n- Indication: Malignant airway obstruction (72% pre-op).\n- Outcome: Successful deployment, patent airway.",
            4: "Procedure Steps:\n1. GA induced. Rigid scope inserted.\n2. Identified RMS obstruction (72%).\n3. Dilated stenosis with balloon.\n4. Deployed Aero SEMS covered stent (16x30mm) to RMS.\n5. Confirmed position and expansion.\n6. Removed scope.\nPatient tolerated well.",
            5: "Betty Green procedure note she has lung cancer blocking the right mainstem about 72 percent. Did the rigid bronch dilated it and put in an Aero covered stent 16 by 30. Looks really good opened up to 8 percent. No bleeding complications patient goes to the floor for observation thanks.",
            6: "The patient has primary lung adenocarcinoma with CAO, presenting with ~72% obstruction of the Right mainstem. Under general anesthesia with jet ventilation, rigid bronchoscopy was performed. Sequential balloon dilation of the RMS stenosis was performed. The airway was measured and an Aero SEMS Covered stent (16x30mm) was deployed in the Right mainstem. Stent position was confirmed with good expansion and patency. Post-procedure obstruction was ~8%. There were no complications and EBL was minimal.",
            7: "[Indication]\nLung adenocarcinoma, 72% RMS obstruction.\n[Anesthesia]\nGeneral, Rigid Bronch.\n[Description]\nRMS dilated. Aero SEMS Covered stent (16x30mm) placed. Obstruction reduced to 8%.\n[Plan]\nAdmit for observation. Follow up 4-6 weeks.",
            8: "Ms. Green was brought to the OR for management of her malignant airway obstruction. Using rigid bronchoscopy, we identified a 72% blockage in the right mainstem bronchus. We dilated the stricture and then placed a 16x30mm Aero covered SEMS. The stent expanded immediately, clearing the airway to near-normal patency (8% residual). She remained stable throughout and was transferred to the floor.",
            9: "Indication: Primary lung adenocarcinoma with CAO.\nPre-procedure blockage: ~72% Right mainstem.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy was executed. Sequential balloon widening of RMS stenosis was done. The airway was calibrated and an Aero SEMS - Covered stent (16x30mm) was inserted in the Right mainstem. Stent orientation was corroborated with good distension and openness.\nPost-procedure blockage: ~8%.\nNo complications."
        },
        3: { # Note 3: Daniel Allen (RLL APC)
            1: "Indication: Malignant CAO RLL.\nFindings: 78% obstruction.\nProcedure:\n- Rigid bronch.\n- APC tumor destruction/debulking.\n- Multiple passes.\nResult: 18% residual. Hemostasis achieved.\nEBL: 50ml.\nPlan: ICU.",
            2: "OPERATIVE REPORT: Mr. Allen presented with malignant central airway obstruction at the right lower lobe (RLL) orifice. Under general anesthesia, rigid bronchoscopy revealed an endobronchial tumor causing 78% occlusion. Thermal ablation was performed utilizing Argon Plasma Coagulation (APC), followed by mechanical debulking. This sequence was repeated to maximize luminal gain. Post-intervention assessment showed a significant reduction in tumor burden with 18% residual obstruction. Hemostasis was secured via APC application to the tumor base.",
            3: "CPT Code: 31641 (Bronchoscopy with destruction of tumor).\nModality: Argon Plasma Coagulation (APC).\nLocation: RLL Orifice.\nWork Performed:\n- Identification of tumor (78% occlusion).\n- Thermal destruction of tissue.\n- Mechanical removal of debris.\n- Hemostasis.\nOutcome: Obstruction reduced to 18%.",
            4: "Procedure: Tumor Debulking (APC)\nPatient: Allen, Daniel\nSteps:\n1. Rigid bronchoscopy initiated.\n2. Tumor found at RLL orifice (78%).\n3. APC applied for destruction.\n4. Debris removed.\n5. Repeat until maximal debulking achieved (18% residual).\n6. Hemostasis confirmed.\nPlan: ICU observation.",
            5: "Daniel Allen here for debulking of a tumor in the RLL it was blocking about 78 percent. We used the rigid scope and the APC argon plasma to burn and remove the tumor. Did a few passes and got it down to 18 percent. Bleeding was controlled about 50cc loss. Sending him to the ICU for tonight just to be safe.",
            6: "Indication: Malignant central airway obstruction with ~78% obstruction at RLL orifice. Under general anesthesia, rigid bronchoscopy was performed. Endobronchial tumor was identified at the RLL orifice. Argon plasma coagulation (APC) was performed with sequential tumor removal. Multiple passes were performed to achieve maximal debulking. Additional APC/laser was used for hemostasis and tumor base ablation. Post-procedure obstruction was ~18%. EBL was ~50mL and hemostasis was achieved. Specimens were sent for histology.",
            7: "[Indication]\nMalignant CAO, RLL orifice (78%).\n[Anesthesia]\nGeneral, Rigid Bronch.\n[Description]\nAPC destruction of tumor performed. Sequential removal. Hemostasis achieved. Residual obstruction 18%.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "Mr. Allen underwent rigid bronchoscopy for a tumor obstructing his right lower lobe bronchus by about 78%. We used argon plasma coagulation to destroy the tumor tissue and removed it sequentially. After several passes, we successfully debulked the lesion down to an 18% residual obstruction. We ensured all bleeding was stopped using APC. He is going to the ICU for overnight monitoring.",
            9: "Indication: Malignant central airway blockage.\nPre-procedure: ~78% occlusion at RLL orifice.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy was conducted. Endobronchial neoplasm found at RLL orifice. APC (argon plasma coagulation) was utilized with sequential tumor extraction. Multiple passes were done to attain maximal volume reduction. Additional APC/laser used for hemostasis and tumor base cauterization.\nPost-procedure: ~18% residual occlusion.\nEBL: ~50mL."
        },
        4: { # Note 4: Kathleen Baker (LMS Covered Stent)
            1: "Indication: SCC airway compromise LMS.\nFindings: 93% obstruction.\nProcedure:\n- Rigid bronch.\n- Aero SEMS Covered stent (16x30mm) placed.\n- Good expansion.\nResult: 8% residual.\nPlan: Admit.",
            2: "HISTORY: Ms. Baker presented with near-total occlusion (93%) of the left mainstem (LMS) bronchus due to squamous cell carcinoma.\nPROCEDURE: Under general anesthesia with jet ventilation, the airway was accessed via rigid bronchoscopy. Given the severity of the stenosis, a covered self-expanding metallic stent (Aero SEMS, 16x30mm) was selected and deployed across the lesion. The stent demonstrated excellent radial force and expansion, restoring the airway lumen to 8% residual narrowing.\nIMPRESSION: Successful recanalization of the LMS.",
            3: "Procedure Code: 31636 (Bronchial Stent).\nSite: Left Mainstem Bronchus.\nProsthesis: Aero SEMS (Covered), 16x30mm.\nJustification: 93% Malignant Obstruction.\nTechnique: Rigid bronchoscopy, measurement, deployment, verification.\nResult: Patent airway.",
            4: "Procedure: LMS Stent Placement\nPatient: Baker, Kathleen\nSteps:\n1. GA/Rigid scope.\n2. LMS obstruction 93%.\n3. Measured airway.\n4. Deployed Aero SEMS 16x30mm.\n5. Confirmed patency.\nNo complications.\nPlan: Admit.",
            5: "Kathleen Baker procedure note she has squamous cell cancer blocking the left mainstem 93 percent really tight. We went in with the rigid scope measured it out and put in an Aero covered stent 16 by 30. Opened up great down to 8 percent. No bleeding no issues. Admit her for the night.",
            6: "Indication: Squamous cell carcinoma with airway compromise, ~93% Left mainstem obstruction. Under general anesthesia with jet ventilation, rigid bronchoscopy was performed. The airway was measured and an Aero SEMS Covered stent (16x30mm) was deployed in the Left mainstem. Stent position was confirmed with good expansion and patency. Post-procedure obstruction was ~8%. There were no complications and EBL was minimal.",
            7: "[Indication]\nSCC, 93% LMS obstruction.\n[Anesthesia]\nGeneral, Rigid Bronch.\n[Description]\nAero SEMS Covered stent (16x30mm) deployed in LMS. Good expansion. Obstruction reduced to 8%.\n[Plan]\nAdmit overnight. Follow up 4-6 weeks.",
            8: "Ms. Baker required urgent intervention for a 93% blockage of her left mainstem bronchus caused by squamous cell carcinoma. Using a rigid bronchoscope under general anesthesia, we placed a 16x30mm covered Aero SEMS. The stent expanded fully, immediately relieving the obstruction and leaving only an 8% residual narrowing. She tolerated the procedure well and was admitted for observation.",
            9: "Indication: Squamous cell carcinoma with airway impairment.\nPre-procedure blockage: ~93% Left mainstem.\nPROCEDURE: Under general anesthesia with jet ventilation, rigid bronchoscopy was performed. The airway was gauged and an Aero SEMS - Covered stent (16x30mm) was positioned in the Left mainstem. Stent placement was validated with good distension and openness.\nPost-procedure blockage: ~8%.\nNo complications."
        },
        5: { # Note 5: Kevin Hernandez (BI Forceps Excision)
            1: "Indication: Lung adenocarcinoma CAO at BI.\nFindings: 74% obstruction.\nProcedure:\n- Rigid bronch.\n- Mechanical debulking w/ biopsy forceps.\n- Multiple passes.\nResult: 12% residual. Hemostasis achieved.\nEBL: 75ml.\nPlan: ICU.",
            2: "OPERATIVE SUMMARY: Mr. Hernandez presented with a 74% obstruction of the bronchus intermedius (BI) due to lung adenocarcinoma. The patient was placed under general anesthesia. Rigid bronchoscopic inspection identified the exophytic tumor. Mechanical excision was performed utilizing rigid biopsy forceps. Sequential bites were taken to debulk the lesion until the airway lumen was satisfactorily restored (12% residual). Hemostasis was maintained throughout.\nPATHOLOGY: Tissue submitted for histological analysis.",
            3: "Code: 31640 (Bronchoscopy with excision of tumor).\nMethod: Mechanical excision via rigid forceps.\nLocation: Bronchus Intermedius (BI).\nDetails:\n- Tumor visualization (74% block).\n- Physical removal of tissue.\n- Hemostasis.\n- Final patency check (12% residual).\nPathology: Samples sent.",
            4: "Procedure: Tumor Excision (Forceps)\nPatient: Hernandez, Kevin\nSteps:\n1. Rigid scope inserted.\n2. Tumor at BI visualized.\n3. Used biopsy forceps for mechanical debulking.\n4. Removed tumor in pieces.\n5. Hemostasis achieved.\nPlan: ICU obs.",
            5: "Kevin Hernandez here for tumor removal in the BI blocking 74 percent. We used the rigid scope and the big biopsy forceps to just grab and pull the tumor out. Did a bunch of passes got it down to 12 percent. Bleeding was okay about 75cc. Samples sent to lab. He goes to ICU tonight.",
            6: "Indication: Primary lung adenocarcinoma with CAO, ~74% obstruction at BI. Under general anesthesia, rigid bronchoscopy was performed. Endobronchial tumor was identified at BI. Rigid bronchoscopy debulking with biopsy forceps was performed with sequential tumor removal. Multiple passes were performed to achieve maximal debulking. Post-procedure obstruction was ~12% residual obstruction. EBL was ~75mL and hemostasis was achieved. Specimens were sent for histology.",
            7: "[Indication]\nLung adenocarcinoma, BI obstruction (74%).\n[Anesthesia]\nGeneral, Rigid Bronch.\n[Description]\nMechanical debulking with forceps performed. Tumor excised. Residual obstruction 12%. EBL 75ml.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "We performed a rigid bronchoscopy on Mr. Hernandez to clear a tumor obstructing his bronchus intermedius. The blockage was approximately 74%. We used rigid biopsy forceps to mechanically excise the tumor tissue piece by piece. We continued this until the obstruction was reduced to 12%. The bleeding was controlled, and we collected sufficient samples for pathology. He was transferred to the ICU for recovery.",
            9: "Indication: Primary lung adenocarcinoma with CAO.\nPre-procedure: ~74% occlusion at BI.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy was conducted. Endobronchial neoplasm detected at BI. Rigid bronchoscopy resection with biopsy forceps was executed with sequential tumor extraction. Multiple passes were done to attain maximal debulking.\nPost-procedure: ~12% residual occlusion.\nEBL: ~75mL."
        },
        6: { # Note 6: Anthony Baker (RMS Cryo)
            1: "Indication: Malignant CAO RMS.\nFindings: 66% obstruction.\nProcedure:\n- Rigid bronch.\n- Cryoextraction of tumor.\n- APC for hemostasis/base.\n- Balloon dilation.\nResult: 17% residual.\nEBL: 200ml.\nPlan: ICU.",
            2: "OPERATIVE REPORT: Mr. Baker presented with 66% malignant obstruction of the right mainstem (RMS). Rigid bronchoscopy was utilized. The tumor was addressed via cryoextraction, allowing for en bloc removal of significant tissue volume. Following cryodebulking, the tumor base was treated with APC for hemostasis and ablation. Residual stenosis was managed with balloon dilation. Final assessment showed 17% residual obstruction. Estimated blood loss was 200mL.\nDISPOSITION: ICU admission.",
            3: "CPT Code: 31641 (Bronchoscopy with destruction of tumor).\nTechnique: Cryoextraction and APC.\nLocation: Right Mainstem Bronchus.\nNotes: \n- Cryoprobe used to freeze and extract tumor chunks.\n- APC used for base destruction.\n- Balloon dilation included for residual stenosis.\n- EBL 200ml controlled.",
            4: "Procedure: Tumor Debulking (Cryo)\nPatient: Baker, Anthony\nSteps:\n1. Rigid scope to RMS.\n2. Tumor identified (66%).\n3. Cryoprobe used to extract tumor.\n4. APC used for clean up and bleeding.\n5. Balloon dilation for remaining narrowing.\n6. Hemostasis confirmed.\nPlan: ICU.",
            5: "Anthony Baker for tumor debulking in the RMS blocking 66 percent. We used the cryo probe to freeze the tumor and pull it out in big chunks. Then used the APC to stop the bleeding and burn the base. Also dilated it a bit. Got it down to 17 percent. Lost about 200cc of blood but got it stopped. Sending him to ICU.",
            6: "Indication: Malignant central airway obstruction, ~66% obstruction at RMS. Under general anesthesia, rigid bronchoscopy was performed. Endobronchial tumor identified at RMS. Cryoextraction performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC/laser used for hemostasis and tumor base ablation. Balloon dilation performed for residual stenosis. Post-procedure obstruction was ~17% residual obstruction. EBL was ~200mL. Specimens sent for histology.",
            7: "[Indication]\nMalignant CAO, RMS (66%).\n[Anesthesia]\nGeneral, Rigid Bronch.\n[Description]\nCryoextraction of tumor performed. APC for hemostasis. Balloon dilation. Residual obstruction 17%. EBL 200ml.\n[Plan]\nICU observation.",
            8: "Mr. Baker underwent rigid bronchoscopy for a tumor in his right mainstem bronchus. We used cryoextraction to remove the tumor tissue efficiently. After the bulk of the tumor was removed, we used APC to treat the base and control bleeding. We also dilated the airway with a balloon to maximize patency. The obstruction was reduced from 66% to 17%. He lost about 200mL of blood, but hemostasis was achieved before finishing. He is heading to the ICU.",
            9: "Indication: Malignant central airway blockage.\nPre-procedure: ~66% occlusion at RMS.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm identified at RMS. Cryoextraction performed with sequential tumor withdrawal. Multiple passes were done to attain maximal debulking. Additional APC/laser utilized for hemostasis and tumor base cauterization. Balloon dilation executed for residual stenosis.\nPost-procedure: ~17% residual occlusion.\nEBL: ~200mL."
        },
        7: { # Note 7: Lisa Rivera (RMS Silicone Stent)
            1: "Indication: Esophageal ca, tracheal invasion.\nFindings: 86% RMS obstruction.\nProcedure:\n- Rigid bronch, jet vent.\n- Dilation.\n- Novatech Silicone Dumon (20x30mm) placed in RMS.\nResult: 21% residual.\nPlan: Admit.",
            2: "HISTORY: Ms. Rivera, with a history of esophageal carcinoma and tracheal invasion, presented with 86% stenosis of the right mainstem (RMS).\nPROCEDURE: General anesthesia with jet ventilation was established. Rigid bronchoscopy visualized the stenosis. Following mechanical dilation, a 20x30mm Novatech Silicone Dumon stent was deployed. The stent maintained airway patency against the extrinsic compression, resulting in a residual obstruction of 21%.\nOUTCOME: Satisfactory stent placement.",
            3: "Procedure: Bronchoscopy with Stent (31636).\nDevice: Novatech Silicone Dumon (20x30mm).\nLocation: Right Mainstem Bronchus.\nIndication: Extrinsic compression from Esophageal Cancer (86%).\nTechnique: Rigid bronchoscopy, balloon dilation, stent deployment.\nOutcome: Patent airway (21% residual).",
            4: "Procedure: RMS Stent Placement\nPatient: Rivera, Lisa\nSteps:\n1. GA/Jet ventilation.\n2. Rigid scope inserted.\n3. RMS stenosis (86%) dilated.\n4. Dumon stent 20x30mm placed.\n5. Confirmed position.\nComplications: None.\nPlan: Admit.",
            5: "Lisa Rivera here for RMS stent she has esophageal cancer pushing in. Blocked 86 percent. We did the rigid bronch with jet vent dilated it open then put in a silicone dumon stent 20 by 30. Opened up to about 21 percent blocked. No bleeding. She goes to the floor.",
            6: "Indication: Esophageal cancer with tracheal invasion, ~86% Right mainstem obstruction. Under general anesthesia with jet ventilation, rigid bronchoscopy was performed. Sequential balloon dilation of RMS stenosis performed. Airway measured and Novatech Silicone - Dumon stent (20x30mm) deployed in Right mainstem. Stent position confirmed with good expansion and patency. Post-procedure obstruction was ~21%. No complications. EBL minimal.",
            7: "[Indication]\nEsophageal cancer, 86% RMS obstruction.\n[Anesthesia]\nGeneral, Jet Ventilation.\n[Description]\nRMS dilated. Novatech Dumon stent (20x30mm) deployed. Residual obstruction 21%.\n[Plan]\nAdmit. Follow up 4-6 weeks.",
            8: "Ms. Rivera needed a stent for her right mainstem bronchus, which was being compressed by her esophageal cancer. Under general anesthesia, we dilated the 86% stenosis and deployed a 20x30mm Novatech Silicone Dumon stent. The stent held the airway open well, leaving a residual narrowing of about 21%. She did well and was admitted for observation.",
            9: "Indication: Esophageal cancer with tracheal incursion.\nPre-procedure occlusion: ~86% Right mainstem.\nPROCEDURE: Under general anesthesia with jet ventilation, rigid bronchoscopy was conducted. Sequential balloon expansion of RMS narrowing was done. The airway was sized and a Novatech Silicone - Dumon stent (20x30mm) was installed in the Right mainstem. Stent location was verified with good expansion and flow.\nPost-procedure occlusion: ~21%.\nNo adverse events."
        },
        8: { # Note 8: Daniel Nguyen (RUL Laser)
            1: "Indication: Malignant CAO RUL.\nFindings: 73% obstruction.\nProcedure:\n- Rigid bronch.\n- Laser ablation.\n- Sequential removal.\n- APC for hemostasis.\nResult: 39% residual.\nEBL: 150ml.\nPlan: ICU.",
            2: "OPERATIVE NOTE: Mr. Nguyen presented with a malignant obstruction of the right upper lobe (RUL) orifice estimated at 73%. Under general anesthesia, rigid bronchoscopy was performed. The Nd:YAG laser was utilized to coagulate and vaporize tumor tissue. Sequential mechanical debridement was performed. Additional hemostasis was achieved with APC. The airway caliber was improved, with a residual obstruction of 39%. EBL was 150mL.\nDISPOSITION: Transfer to ICU.",
            3: "CPT Code: 31641 (Bronchoscopy with destruction of tumor).\nModality: Laser Ablation.\nLocation: RUL Orifice.\nProcess:\n- Laser application to tumor (73% block).\n- Vaporization and removal of tissue.\n- Hemostasis via APC/Laser.\nOutcome: Partial recanalization (39% residual).",
            4: "Procedure: Tumor Ablation (Laser)\nPatient: Nguyen, Daniel\nSteps:\n1. Rigid scope placed.\n2. Tumor at RUL (73%) identified.\n3. Laser ablation performed.\n4. Debris removed.\n5. Hemostasis confirmed.\nPlan: ICU.",
            5: "Daniel Nguyen procedure note he has a tumor blocking the RUL 73 percent. We used the rigid scope and the laser to burn it down. Removed the pieces. Used APC to stop bleeding. Got it down to 39 percent obstruction. Lost about 150cc blood. He is going to the ICU.",
            6: "Indication: Malignant central airway obstruction, ~73% obstruction at RUL orifice. Under general anesthesia, rigid bronchoscopy was performed. Endobronchial tumor identified at RUL orifice. Laser ablation performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC/laser used for hemostasis and tumor base ablation. Post-procedure obstruction was ~39% residual obstruction. EBL was ~150mL. Specimens sent for histology.",
            7: "[Indication]\nMalignant CAO, RUL orifice (73%).\n[Anesthesia]\nGeneral, Rigid Bronch.\n[Description]\nLaser ablation performed. Tumor debulked. Hemostasis with APC. Residual obstruction 39%. EBL 150ml.\n[Plan]\nICU observation.",
            8: "We performed a rigid bronchoscopy on Mr. Nguyen to treat a tumor obstructing his RUL orifice. We used laser ablation to destroy the tumor tissue and removed it in sequence. We achieved a significant reduction in tumor bulk, leaving a 39% residual obstruction. Bleeding was controlled with the laser and APC. He tolerated the procedure and was sent to the ICU for monitoring.",
            9: "Indication: Malignant central airway blockage.\nPre-procedure: ~73% occlusion at RUL orifice.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm detected at RUL orifice. Laser ablation conducted with sequential tumor extraction. Multiple passes were done to attain maximal debulking. Additional APC/laser utilized for hemostasis and tumor base cauterization.\nPost-procedure: ~39% residual occlusion.\nEBL: ~150mL."
        },
        9: { # Note 9: Daniel Jackson (RMS Laser/Excision - Coded 31640)
            1: "Indication: Malignant CAO RMS.\nFindings: 60% obstruction.\nProcedure:\n- Rigid bronch.\n- Laser ablation/excision.\n- Multiple passes.\nResult: 35% residual.\nEBL: 150ml.\nPlan: ICU.",
            2: "OPERATIVE SUMMARY: Mr. Jackson presented with 60% obstruction of the right mainstem (RMS) bronchus. Under general anesthesia, rigid bronchoscopy was initiated. The tumor was addressed via laser photoresection and mechanical excision to facilitate removal. Multiple passes were required to debulk the lesion. Post-intervention, the obstruction was reduced to 35%. Hemostasis was secured. Specimens were submitted for pathologic evaluation.",
            3: "CPT Code: 31640 (Bronchoscopy with excision of tumor).\nTechnique: Laser ablation and mechanical removal.\nLocation: Right Mainstem Bronchus.\nDetails:\n- Visualization of 60% stenosis.\n- Laser applied to devitalize tissue.\n- Mechanical excision of tumor mass.\n- Hemostasis.\nOutcome: 35% residual obstruction.",
            4: "Procedure: Tumor Excision/Ablation\nPatient: Jackson, Daniel\nSteps:\n1. Rigid scope inserted.\n2. RMS tumor visualized (60%).\n3. Laser used to ablate/excise.\n4. Tumor removed.\n5. Hemostasis confirmed.\nPlan: ICU.",
            5: "Daniel Jackson here for tumor removal in the RMS blocking 60 percent. Used the rigid scope and the laser to cut it out. Did a few passes. Got it down to 35 percent. Bleeding was 150cc stopped it okay. Sending samples to lab and patient to ICU.",
            6: "Indication: Malignant central airway obstruction, ~60% obstruction at RMS. Under general anesthesia, rigid bronchoscopy was performed. Endobronchial tumor identified at RMS. Laser ablation performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Post-procedure obstruction was ~35% residual obstruction. EBL was ~150mL. Hemostasis achieved. Specimens sent for histology.",
            7: "[Indication]\nMalignant CAO, RMS (60%).\n[Anesthesia]\nGeneral, Rigid Bronch.\n[Description]\nLaser ablation and excision performed. Tumor removed. Residual obstruction 35%. EBL 150ml.\n[Plan]\nICU observation.",
            8: "Mr. Jackson underwent rigid bronchoscopy for a tumor in the right mainstem bronchus causing 60% obstruction. We used the laser to ablate and excise the tumor tissue. After multiple passes, we reduced the obstruction to 35%. Bleeding was controlled, and the patient remained stable. He was transferred to the ICU for overnight care.",
            9: "Indication: Malignant central airway blockage.\nPre-procedure: ~60% occlusion at RMS.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy was conducted. Endobronchial neoplasm detected at RMS. Laser ablation executed with sequential tumor extraction. Multiple passes were done to attain maximal debulking.\nPost-procedure: ~35% residual occlusion.\nEBL: ~150mL."
        }
    }
    return variations

def get_base_data_mocks():
    # Mock data for names corresponding to the 10 notes in part_055.json
    return [
        {"idx": 0, "orig_name": "Cynthia Jones", "orig_age": 78, "names": ["Alice Smith", "Mary Johnson", "Patricia Williams", "Jennifer Brown", "Linda Jones", "Elizabeth Miller", "Barbara Davis", "Susan Garcia", "Jessica Rodriguez"]},
        {"idx": 1, "orig_name": "Barbara Robinson", "orig_age": 62, "names": ["Sarah Wilson", "Karen Martinez", "Nancy Anderson", "Lisa Taylor", "Betty Thomas", "Margaret Hernandez", "Sandra Moore", "Ashley Martin", "Kimberly Jackson"]},
        {"idx": 2, "orig_name": "Betty Green", "orig_age": 71, "names": ["Donna Thompson", "Emily White", "Michelle Lopez", "Carol Lee", "Amanda Gonzalez", "Melissa Harris", "Deborah Clark", "Stephanie Lewis", "Rebecca Robinson"]},
        {"idx": 3, "orig_name": "Daniel Allen", "orig_age": 51, "names": ["James Walker", "John Young", "Robert Allen", "Michael King", "William Wright", "David Scott", "Richard Torres", "Charles Nguyen", "Joseph Hill"]},
        {"idx": 4, "orig_name": "Kathleen Baker", "orig_age": 69, "names": ["Laura Flores", "Cynthia Green", "Kathleen Adams", "Amy Nelson", "Shirley Baker", "Angela Hall", "Helen Rivera", "Anna Campbell", "Brenda Mitchell"]},
        {"idx": 5, "orig_name": "Kevin Hernandez", "orig_age": 71, "names": ["Thomas Carter", "Christopher Roberts", "Daniel Gomez", "Paul Phillips", "Mark Evans", "Donald Turner", "George Diaz", "Kenneth Parker", "Steven Cruz"]},
        {"idx": 6, "orig_name": "Anthony Baker", "orig_age": 70, "names": ["Edward Edwards", "Brian Collins", "Ronald Reyes", "Anthony Stewart", "Kevin Morris", "Jason Morales", "Matthew Murphy", "Gary Cook", "Timothy Rogers"]},
        {"idx": 7, "orig_name": "Lisa Rivera", "orig_age": 51, "names": ["Nicole Morgan", "Christina Peterson", "Janet Cooper", "Debra Reed", "Rachel Bailey", "Catherine Bell", "Maria Gomez", "Heather Kelly", "Diane Howard"]},
        {"idx": 8, "orig_name": "Daniel Nguyen", "orig_age": 75, "names": ["Jeffrey Ward", "Frank Cox", "Scott Diaz", "Eric Richardson", "Stephen Wood", "Andrew Watson", "Raymond Brooks", "Gregory Bennett", "Joshua Gray"]},
        {"idx": 9, "orig_name": "Daniel Jackson", "orig_age": 66, "names": ["Jerry James", "Dennis Reyes", "Walter Cruz", "Patrick Hughes", "Peter Price", "Harold Myers", "Douglas Long", "Henry Foster", "Carl Sanders"]}
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
                print(f"Warning: No text variation found for Note {idx}, Style {style_num}")
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

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_blvr_notes_part_055.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()