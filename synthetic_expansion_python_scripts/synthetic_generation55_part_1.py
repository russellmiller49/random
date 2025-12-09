import json
import random
import datetime
import copy
from pathlib import Path

# Source file configuration
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_055_part1.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each note in the source file.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
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
        0: { # Pt: Jones, Cynthia (31631 - Tracheal Stent, Silicone 12x60mm)
            1: "Indication: Tracheal compression (Thyroid CA).\nProcedure: Rigid bronch. Balloon dilation. Novatech Dumon stent (12x60mm) deployed in Trachea.\nFindings: Obstruction reduced 79% -> 11%.\nComplications: None. Minimal EBL.\nPlan: Obs overnight. Clinic 4-6 wks.",
            2: "OPERATIVE REPORT: Ms. Jones, a 78-year-old female with thyroid malignancy, presented with critical central airway obstruction. Under general anesthesia with jet ventilation, the airway was secured via rigid bronchoscopy. Significant extrinsic compression of the trachea was noted. Mechanical dilation was performed using a balloon catheter. Subsequently, a 12x60mm Novatech silicone Dumon prosthesis was successfully deployed. Post-deployment assessment confirmed excellent radial expansion and restoration of patency (residual obstruction ~11%). The patient tolerated the procedure without hemodynamic compromise.",
            3: "Procedure: Therapeutic Bronchoscopy with Stent Placement (CPT 31631).\nTechnique:\n1. Introduction of rigid bronchoscope.\n2. Identification of tracheal stenosis (79%).\n3. Balloon dilation of stenosis to facilitate stent delivery.\n4. Deployment of indwelling silicone stent (Novatech Dumon, 12x60mm) into the trachea.\n5. Confirmation of position and patency.\nOutcome: Improvement in airway caliber to 11% residual obstruction.",
            4: "Resident Note\nAttending: Dr. Davis\nPt: Jones, C.\nProcedure: Rigid Bronchoscopy with Tracheal Stent\nSteps:\n1. GA induced, jet ventilation started.\n2. Rigid scope inserted.\n3. Tracheal stenosis visualized (~79%).\n4. Balloon dilation performed.\n5. 12x60mm Silicone stent deployed.\n6. Position verified.\nPlan: Admit for observation.",
            5: "procedure note for cynthia jones thyroid cancer pressing on the trachea rigid bronch used general anesthesia balloon dilation done first then we put in a novatech silicone stent 12 by 60 mm right in the trachea looks much better now only 11 percent blocked no bleeding patient stable to recovery.",
            6: "The patient presented with thyroid cancer and tracheal compression roughly 79% obstruction. Under general anesthesia with jet ventilation rigid bronchoscopy was performed followed by sequential balloon dilation of the tracheal stenosis. The airway was sized and a Novatech Silicone Dumon stent measuring 12x60mm was deployed in the Trachea. Stent position was confirmed with good expansion and patency resulting in a post-procedure obstruction of roughly 11%. There were no complications and EBL was minimal. Disposition is recovery then floor admission for overnight observation.",
            7: "[Indication]\nThyroid cancer causing severe tracheal compression (79%).\n[Anesthesia]\nGeneral with jet ventilation.\n[Description]\nRigid bronchoscopy. Sequential balloon dilation. Deployment of Novatech Dumon silicone stent (12x60mm) in trachea. Obstruction reduced to ~11%.\n[Plan]\nOvernight observation. Repeat bronch in 4-6 weeks.",
            8: "Ms. Jones was brought to the operating room for management of tracheal compression due to thyroid cancer. Under general anesthesia, we proceeded with rigid bronchoscopy. We identified a 79% obstruction in the trachea. We performed balloon dilation to prepare the airway. Following this, a 12x60mm Novatech silicone stent was deployed. The stent expanded well, leaving a residual obstruction of only 11%. The patient remained stable throughout.",
            9: "Indication: Thyroid malignancy with tracheal impingement.\nPre-procedure blockage: ~79% Trachea.\nAction: Utilizing general anesthesia and jet ventilation, rigid bronchoscopy was executed. Consecutive balloon expansion of the tracheal narrowing was achieved. The airway was gauged and a Novatech Silicone Dumon prosthesis (12x60mm) was positioned in the Trachea. Prosthesis location was verified with favorable dilation and openness. Post-procedure blockage: ~11%. No adverse events."
        },
        1: { # Pt: Robinson, Barbara (31636 - RMS Stent, Silicone 20x50mm)
            1: "Dx: SCC, airway compromise.\nProc: Rigid bronch, RMS Stent.\nDetails: RMS stenosis (91%) dilated. Novatech Dumon (20x50mm) placed.\nResult: RMS patency improved (4% residual).\nPlan: Admit. F/U 4-6 wks.",
            2: "PROCEDURE: Rigid bronchoscopy with bronchial stenting.\nINDICATION: Squamous cell carcinoma with critical Right Mainstem (RMS) stenosis.\nNARRATIVE: The patient was anesthetized and the rigid bronchoscope introduced. The RMS revealed a 91% obstruction. Mechanical dilation was performed via balloon angioplasty. A 20x50mm Novatech silicone Dumon stent was selected and deployed into the Right Mainstem bronchus. Inspection confirmed optimal seating and restoration of luminal patency to approximately 96%. Hemostasis was maintained.",
            3: "Service: Bronchoscopy with Stent (31636).\nLocation: Right Mainstem Bronchus (RMS).\nDevice: Novatech Silicone Stent (20x50mm).\nMedical Necessity: 91% obstruction due to malignancy.\nMethod: Rigid bronchoscopy used for visualization and delivery. Balloon dilation used as preparatory adjunct. Stent successfully deployed with reduction of obstruction to 4%.",
            4: "Procedure: RMS Stent Placement\nPatient: Robinson, B.\nStaff: Dr. Anderson / Dr. Torres\nSteps:\n1. Time out.\n2. Rigid bronchoscopy (GA/Jet).\n3. RMS stenosis identified (91%).\n4. Dilation with balloon.\n5. Stent deployed (Silicone 20x50mm) in RMS.\n6. Good expansion noted.\nPost-op: Stable. Residual obstruction 4%.",
            5: "barbara robinson here for airway stent she has scc with 91 percent block in the right mainstem anesthesia was general rigid scope used ballooned the stenosis open then put in a novatech silicone dumon stent 20x50mm looks wide open now maybe 4 percent residual no issues sending to floor.",
            6: "Under general anesthesia with jet ventilation rigid bronchoscopy was performed for indication of squamous cell carcinoma with airway compromise. Pre-procedure obstruction was approximately 91% in the Right mainstem. Sequential balloon dilation of RMS stenosis was performed followed by airway measurement and deployment of a Novatech Silicone Dumon stent 20x50mm in the Right mainstem. Stent position confirmed with good expansion and patency with post-procedure obstruction of roughly 4%. No complications and minimal EBL.",
            7: "[Indication]\nSquamous cell carcinoma, 91% RMS obstruction.\n[Anesthesia]\nGeneral, jet ventilation.\n[Description]\nRigid bronchoscopy. Balloon dilation of RMS. Placement of Novatech Dumon silicone stent (20x50mm). Patency improved to 96%.\n[Plan]\nAdmit for observation. Follow up 4-6 weeks.",
            8: "Mrs. Robinson underwent rigid bronchoscopy today to address a 91% blockage in her right mainstem bronchus caused by squamous cell carcinoma. We used balloon dilation to open the stenosis. Then, we placed a 20x50mm Novatech silicone stent. The stent sat perfectly, and the obstruction was reduced to just 4%. She tolerated the procedure well with minimal blood loss.",
            9: "Reason: Squamous cell carcinoma with airway jeopardy.\nInitial occlusion: ~91% Right mainstem.\nOperation: Under general anesthesia, rigid bronchoscopy was conducted. Serial balloon expansion of the RMS narrowing was performed. The airway was sized and a Novatech Silicone Dumon implant (20x50mm) was inserted in the Right mainstem. Implant alignment was validated with robust expansion and clearance. Final occlusion: ~4%."
        },
        2: { # Pt: Green, Betty (31636 - RMS Stent, Covered SEMS 16x30mm)
            1: "Indication: Lung Adeno, CAO.\nTarget: RMS (72% obst).\nDevice: Aero SEMS Covered (16x30mm).\nAction: Rigid bronch, balloon dilation, stent deployment.\nOutcome: 8% residual obstruction. No complications.",
            2: "OPERATIVE SUMMARY: Ms. Green presented with malignant central airway obstruction (CAO) secondary to primary lung adenocarcinoma. Rigid bronchoscopy was initiated under general anesthesia. The Right Mainstem (RMS) demonstrated 72% stenosis. Following balloon dilation, an Aero self-expanding metallic stent (SEMS, covered, 16x30mm) was precisely deployed within the RMS. Post-deployment evaluation showed excellent wall apposition and patency (residual stenosis ~8%).",
            3: "Code: 31636 (Bronchial Stent).\nSite: Right Mainstem Bronchus.\nImplant: Aero SEMS (Covered, 16x30mm).\nProcedure:\n- Rigid bronchoscopy access.\n- Balloon dilation of 72% stenosis.\n- Measurement and selection of 16x30mm device.\n- Deployment under direct visualization.\n- Verification of patency (8% residual).",
            4: "Resident Procedure Note\nPt: Green, Betty\nAttending: Dr. Garcia\nProcedure: RMS Stenting\nSteps:\n1. Rigid scope inserted.\n2. RMS stenosis identified (72%).\n3. Dilation performed.\n4. Aero SEMS (16x30mm) deployed.\n5. Stent patent.\nPlan: Obs overnight.",
            5: "betty green 71f lung adeno with airway obstruction right mainstem was 72 percent blocked we did rigid bronch under ga dilated it then put in an aero sems covered stent 16x30mm opened up nicely to 8 percent obstruction no complications minimal bleeding plan for clinic f/u.",
            6: "Patient Green Betty DOB 8/26/1954 underwent rigid bronchoscopy under general anesthesia with jet ventilation for primary lung adenocarcinoma with CAO. Pre-procedure obstruction was approximately 72% in the Right mainstem. Sequential balloon dilation of RMS stenosis was performed followed by deployment of an Aero SEMS Covered stent 16x30mm. Stent position confirmed with good expansion and patency and post-procedure obstruction was roughly 8%. No complications were noted.",
            7: "[Indication]\nLung adenocarcinoma with CAO (RMS 72%).\n[Anesthesia]\nGeneral, jet ventilation.\n[Description]\nRigid bronchoscopy. Dilation of RMS. Deployment of Aero Covered SEMS (16x30mm). Residual obstruction 8%.\n[Plan]\nOvernight observation. Repeat bronch in 4-6 weeks.",
            8: "Ms. Green was treated for a 72% blockage in her right mainstem bronchus due to lung cancer. We performed a rigid bronchoscopy under general anesthesia. After dilating the narrowed area with a balloon, we deployed a covered Aero SEMS stent measuring 16x30mm. The airway opened up significantly, leaving only an 8% obstruction. The procedure was uncomplicated.",
            9: "Reason: Primary lung adenocarcinoma with CAO.\nPrior blockage: ~72% Right mainstem.\nProcess: Under general anesthesia, rigid bronchoscopy was undertaken. Successive balloon widening of the RMS constriction was done. The airway was gauged and an Aero SEMS Covered prosthesis (16x30mm) was installed in the Right mainstem. Prosthesis placement was corroborated with fine expansion and openness. Subsequent blockage: ~8%."
        },
        3: { # Pt: Allen, Daniel (31641 - APC/Debulking, RLL)
            1: "Indication: Malignant CAO (RLL 78%).\nProc: Rigid bronch, APC tumor destruction.\nAction: Multiple passes APC/mechanical debulking.\nResult: 18% residual. Hemostasis achieved (50mL EBL).\nPlan: ICU obs.",
            2: "PROCEDURE NOTE: Rigid bronchoscopy with thermal ablation.\nPATIENT: Mr. Allen (51M).\nFINDINGS: Endobronchial tumor obstructing the RLL orifice by approximately 78%.\nINTERVENTION: Argon Plasma Coagulation (APC) was utilized for tumor coagulation and desiccation. Mechanical debulking was performed sequentially. Hemostasis was secured via APC and laser application.\nOUTCOME: The airway caliber was significantly improved to ~18% residual obstruction. EBL estimated at 50mL.",
            3: "CPT 31641 (Destruction of tumor, relief of stenosis).\nModality: Argon Plasma Coagulation (APC) and mechanical debulking.\nLocation: Right Lower Lobe (RLL) orifice.\nDetails: 78% obstruction reduced to 18% via multiple passes of tumor destruction and removal. Hemostasis achieved. Specimens sent to pathology.",
            4: "Procedure: Tumor Debulking (APC)\nPatient: Allen, Daniel\nSteps:\n1. Rigid bronchoscopy initiated.\n2. Tumor seen at RLL orifice (78% obs).\n3. APC used for ablation.\n4. Debris removed mechanically.\n5. Hemostasis confirmed.\nResult: 18% residual obstruction.\nPlan: ICU admission.",
            5: "daniel allen malignant obstruction rll orifice about 78 percent blocked used general anesthesia rigid scope and apc argon plasma coagulation to burn and remove the tumor took a few passes to get it clean used laser too for bleeding control ended up with 18 percent blockage ebl 50ml sending to icu.",
            6: "Malignant central airway obstruction at RLL orifice approximately 78% was treated under general anesthesia with rigid bronchoscopy. Endobronchial tumor was identified and APC argon plasma coagulation was performed with sequential tumor removal. Multiple passes achieved maximal debulking. Additional APC and laser were used for hemostasis and tumor base ablation. Post-procedure residual obstruction was approximately 18% with EBL of 50mL. Specimens were sent for histology.",
            7: "[Indication]\nMalignant CAO, RLL orifice (78%).\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. APC ablation and mechanical debulking of tumor. Hemostasis with APC/Laser. Residual obstruction 18%.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "Mr. Allen underwent a debulking procedure for a tumor blocking 78% of his right lower lobe orifice. Using rigid bronchoscopy and Argon Plasma Coagulation (APC), we sequentially removed the tumor tissue. We made multiple passes to clear the airway as much as possible. By the end of the procedure, the obstruction was reduced to 18%. We controlled minor bleeding with APC and laser. He will go to the ICU for monitoring.",
            9: "Reason: Malignant central airway occlusion.\nPrior blockage: ~78% at RLL aperture.\nProcess: Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm was spotted at the RLL aperture. Argon plasma coagulation (APC) was utilized with serial tumor extraction. Numerous sweeps were done to attain maximal volume reduction. Extra APC/laser was employed for blood stanching and tumor base cautery. Subsequent blockage: ~18%."
        },
        4: { # Pt: Baker, Kathleen (31636 - LMS Stent, Covered SEMS 16x30mm)
            1: "Dx: SCC, LMS obstruction (93%).\nProc: Stent placement.\nDevice: Aero SEMS Covered (16x30mm).\nResult: Patent LMS (8% residual).\nPlan: Floor admit.",
            2: "OPERATIVE REPORT: Kathleen Baker, 69F.\nINDICATION: Airway compromise due to Squamous Cell Carcinoma. LMS 93% obstructed.\nPROCEDURE: Rigid bronchoscopy. The left mainstem was measured. An Aero Covered SEMS (16x30mm) was deployed across the lesion. Visual inspection confirmed immediate expansion and relief of obstruction (post-proc ~8%).\nCOMPLICATIONS: None.",
            3: "Billing: 31636 (Stent placement, bronchial).\nSite: Left Mainstem (LMS).\nDevice: Aero SEMS (Covered, 16x30mm).\nCondition: 93% stenosis reduced to 8% post-deployment.\nNote: Rigid bronchoscopy used. No complications.",
            4: "Resident Note: Stent Placement\nPt: Baker, K.\nLoc: Cedars-Sinai\nSteps:\n1. GA/Jet vent.\n2. Rigid scope to LMS.\n3. Measured stenosis (93%).\n4. Deployed Aero SEMS (16x30mm).\n5. Confirmed patency.\nPlan: Overnight obs.",
            5: "kathleen baker here for lms stent she has squamous cell ca 93 percent blocked general anesthesia used rigid scope put in an aero sems covered stent 16 by 30 mm opened up the airway really well to 8 percent no bleeding recovery then floor.",
            6: "Indication Squamous cell carcinoma with airway compromise Pre-procedure obstruction 93% Left mainstem. Under general anesthesia with jet ventilation rigid bronchoscopy performed. Airway measured and Aero SEMS Covered stent 16x30mm deployed in Left mainstem. Stent position confirmed with good expansion and patency. Post-procedure obstruction roughly 8% with no complications and minimal EBL.",
            7: "[Indication]\nSCC, LMS obstruction 93%.\n[Anesthesia]\nGeneral, jet ventilation.\n[Description]\nRigid bronchoscopy. Deployment of Aero Covered SEMS (16x30mm) in LMS. Residual obstruction 8%.\n[Plan]\nAdmit to floor. Clinic f/u 4-6 weeks.",
            8: "We performed a bronchoscopy on Ms. Baker to relieve a 93% blockage in her left mainstem bronchus caused by cancer. We successfully placed a covered Aero SEMS stent (16x30mm). The stent expanded immediately, opening the airway to a residual obstruction of only 8%. There were no complications, and she was sent to the floor for observation.",
            9: "Reason: Squamous cell carcinoma with airway jeopardy.\nPrior blockage: ~93% Left mainstem.\nProcess: Under general anesthesia with jet ventilation, rigid bronchoscopy was executed. The airway was gauged and an Aero SEMS Covered prosthesis (16x30mm) was positioned in the Left mainstem. Prosthesis location was verified with favorable dilation and openness. Subsequent blockage: ~8%."
        },
        5: { # Pt: Hernandez, Kevin (31640 - Excision/Forceps, BI)
            1: "Indication: Lung Adeno, BI obstruction (74%).\nProc: Rigid bronch debulking.\nTechnique: Biopsy forceps excision.\nResult: 12% residual. 75mL EBL.\nPlan: ICU.",
            2: "PROCEDURE: Rigid bronchoscopy with tumor excision.\nLOCATION: Bronchus Intermedius (BI).\nFINDINGS: 74% obstruction by endobronchial tumor.\nACTION: Mechanical debulking was performed using rigid biopsy forceps. Sequential removal of tumor tissue was achieved through multiple passes.\nOUTCOME: Residual obstruction reduced to ~12%. Hemostasis achieved.",
            3: "CPT: 31640 (Excision of tumor).\nMethod: Rigid bronchoscopy with biopsy forceps.\nSite: Bronchus Intermedius (BI).\nDetails: 74% stenosis debulked to 12%. 75mL blood loss. Tissue to path.",
            4: "Procedure: Tumor Excision\nPt: Hernandez, K.\nSteps:\n1. Rigid scope inserted.\n2. Tumor at BI (74%).\n3. Forceps debulking performed.\n4. Hemostasis achieved.\nResult: 12% residual.\nPlan: ICU.",
            5: "kevin hernandez lung adeno bi blocked 74 percent we did rigid bronchoscopy used the biopsy forceps to grab and pull out the tumor took a bunch of passes got it down to 12 percent bleeding was 75ml but stopped specimens to lab plan for icu.",
            6: "Primary lung adenocarcinoma with CAO pre-procedure 74% obstruction at BI. Under general anesthesia rigid bronchoscopy performed. Endobronchial tumor identified at BI. Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Post-procedure 12% residual obstruction EBL 75mL hemostasis achieved. Disposition Recovery then ICU observation overnight.",
            7: "[Indication]\nLung adenocarcinoma, BI obstruction 74%.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Mechanical debulking with biopsy forceps. Residual obstruction 12%.\n[Plan]\nICU admission. Oncology follow-up.",
            8: "Mr. Hernandez underwent a debulking procedure for a tumor in his bronchus intermedius that was causing 74% obstruction. We used rigid biopsy forceps to mechanically remove the tumor piece by piece. After multiple passes, the obstruction was significantly reduced to 12%. There was about 75mL of blood loss, but hemostasis was achieved before finishing.",
            9: "Reason: Primary lung adenocarcinoma with CAO.\nPrior blockage: ~74% obstruction at BI.\nProcess: Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm was spotted at the BI. Rigid bronchoscopy excision with biopsy pincers was performed with serial tumor extraction. Numerous sweeps were done to attain maximal volume reduction. Subsequent blockage: ~12% residual."
        },
        6: { # Pt: Baker, Anthony (31641 - Cryo/APC/Balloon, RMS)
            1: "Indication: Malignant CAO (RMS 66%).\nProc: Cryoextraction, APC, Balloon dilation.\nResult: 17% residual. 200mL EBL.\nPlan: ICU.",
            2: "OPERATIVE NOTE: Multimodal tumor debulking.\nPATIENT: Anthony Baker.\nINDICATION: RMS malignancy (66% obs).\nTECHNIQUE: Cryoextraction was the primary modality for bulk tumor removal. APC and laser were utilized for base ablation and hemostasis. Residual stenosis was managed with balloon dilation.\nOUTCOME: 17% residual obstruction. Moderate bleeding controlled.",
            3: "CPT 31641 (Tumor destruction/relief of stenosis).\nModalities: Cryoextraction, APC, Laser, Balloon Dilation.\nSite: Right Mainstem (RMS).\nStats: 66% pre-op -> 17% post-op.\nEBL: 200mL.",
            4: "Resident Note: Debulking\nPt: Baker, A.\nSteps:\n1. Rigid bronch.\n2. Cryoextraction of RMS tumor.\n3. APC/Laser for bleeders.\n4. Balloon dilation.\nResult: 66% -> 17%.\nPlan: ICU.",
            5: "anthony baker malignant airway obstruction rms 66 percent blocked we used general anesthesia rigid scope cryoextraction to pull out the tumor chunks used apc and laser to stop the bleeding and burn the base ballooned it too got it down to 17 percent bleeding was 200ml icu for tonight.",
            6: "Malignant central airway obstruction Pre-procedure 66% obstruction at RMS. Under general anesthesia rigid bronchoscopy performed. Endobronchial tumor identified at RMS. Cryoextraction performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC laser used for hemostasis and tumor base ablation. Balloon dilation performed for residual stenosis. Post-procedure 17% residual obstruction EBL 200mL Hemostasis achieved.",
            7: "[Indication]\nMalignant CAO, RMS 66%.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Cryoextraction of tumor. APC/Laser for hemostasis. Balloon dilation. Residual obstruction 17%.\n[Plan]\nICU observation.",
            8: "Mr. Baker required a complex debulking of his right mainstem bronchus, which was 66% obstructed. We used cryoextraction to freeze and remove large portions of the tumor. We also used APC and laser to control bleeding and ablate the tumor base, followed by balloon dilation to open the airway further. We achieved a good result with 17% residual obstruction. Blood loss was 200mL.",
            9: "Reason: Malignant central airway occlusion.\nPrior blockage: ~66% obstruction at RMS.\nProcess: Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm was spotted at the RMS. Cryoextraction was performed with serial tumor extraction. Numerous sweeps were done to attain maximal volume reduction. Extra APC/laser was employed for blood stanching and tumor base cautery. Balloon expansion was performed for remaining narrowing. Subsequent blockage: ~17%."
        },
        7: { # Pt: Rivera, Lisa (31636 - RMS Stent, Silicone 20x30mm)
            1: "Indication: Esophageal cancer, tracheal invasion.\nProc: RMS Stenting.\nDevice: Novatech Dumon (20x30mm).\nResult: 86% -> 21% obstruction.\nPlan: Admit.",
            2: "PROCEDURE: Palliative airway stenting.\nINDICATION: Esophageal carcinoma invading the trachea/RMS.\nFINDINGS: 86% stenosis of the Right Mainstem.\nINTERVENTION: Rigid bronchoscopy with balloon dilation. Deployment of a 20x30mm Novatech silicone Dumon stent.\nOUTCOME: Patent airway (21% residual).",
            3: "Billing: 31636 (Bronchial Stent).\nSite: Right Mainstem.\nDevice: Novatech Silicone (20x30mm).\nIndication: Malignant obstruction (86%).\nMethod: Dilation and stent deployment via rigid scope. 21% residual.",
            4: "Procedure: Stent Placement\nPt: Rivera, L.\nSteps:\n1. GA/Jet.\n2. Rigid scope.\n3. RMS stenosis (86%).\n4. Balloon dilation.\n5. Dumon stent 20x30mm placed.\n6. Position good.\nPlan: Floor.",
            5: "lisa rivera esophageal cancer invading the airway rms 86 percent blocked rigid bronch used ballooned it open put in a novatech silicone stent 20 by 30 mm looks okay 21 percent residual no complications minimal bleeding plan for admit.",
            6: "Indication Esophageal cancer with tracheal invasion Pre-procedure obstruction 86% Right mainstem. Under general anesthesia with jet ventilation rigid bronchoscopy performed. Sequential balloon dilation of RMS stenosis performed. Airway measured and Novatech Silicone Dumon stent 20x30mm deployed in Right mainstem. Stent position confirmed with good expansion and patency. Post-procedure obstruction roughly 21%.",
            7: "[Indication]\nEsophageal cancer, RMS invasion 86%.\n[Anesthesia]\nGeneral, jet ventilation.\n[Description]\nRigid bronchoscopy. Dilation. Novatech Dumon stent (20x30mm) placed in RMS. Residual 21%.\n[Plan]\nAdmit. Repeat bronch 4-6 weeks.",
            8: "Ms. Rivera has esophageal cancer that has invaded her airway, causing an 86% blockage in the right mainstem bronchus. We performed a rigid bronchoscopy and dilated the narrowing. We then placed a 20x30mm Novatech silicone stent. This improved the airway patency significantly, leaving a 21% residual obstruction.",
            9: "Reason: Esophageal cancer with tracheal incursion.\nPrior blockage: ~86% Right mainstem.\nProcess: Under general anesthesia with jet ventilation, rigid bronchoscopy was executed. Serial balloon expansion of the RMS narrowing was performed. The airway was gauged and a Novatech Silicone Dumon prosthesis (20x30mm) was positioned in the Right mainstem. Prosthesis location was verified with favorable dilation and openness. Subsequent blockage: ~21%."
        },
        8: { # Pt: Nguyen, Daniel (31641 - Laser, RUL)
            1: "Indication: Malignant CAO (RUL 73%).\nProc: Laser ablation.\nAction: Tumor vaporization/removal.\nResult: 39% residual. 150mL EBL.\nPlan: ICU.",
            2: "OPERATIVE REPORT: Laser photoresection of airway tumor.\nPATIENT: Daniel Nguyen.\nSITE: RUL Orifice (73% obstructed).\nPROCEDURE: Rigid bronchoscopy. Nd:YAG laser was used to coagulate and vaporize endobronchial tumor tissue. Debridement was performed mechanically.\nOUTCOME: Lumen caliber improved to 39% residual. EBL 150mL.",
            3: "CPT 31641 (Tumor destruction).\nMethod: Laser ablation.\nSite: RUL Orifice.\nStats: 73% debulked to 39%.\nHemostasis: Achieved via laser/APC.",
            4: "Procedure: Laser Ablation\nPt: Nguyen, D.\nSteps:\n1. Rigid bronch.\n2. RUL tumor (73%).\n3. Laser ablation performed.\n4. Debris cleared.\nResult: 39% residual.\nPlan: ICU.",
            5: "daniel nguyen malignant cao rul orifice 73 percent blocked used general anesthesia rigid scope laser ablation to burn the tumor removed the pieces took a few passes residual is 39 percent bleeding 150ml stopped with laser sending to icu.",
            6: "Malignant central airway obstruction Pre-procedure 73% obstruction at RUL orifice. Under general anesthesia rigid bronchoscopy performed. Endobronchial tumor identified at RUL orifice. Laser ablation performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC laser used for hemostasis and tumor base ablation. Post-procedure 39% residual obstruction EBL 150mL Hemostasis achieved.",
            7: "[Indication]\nMalignant CAO, RUL 73%.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Laser ablation of tumor. Mechanical removal of debris. Residual obstruction 39%.\n[Plan]\nICU observation.",
            8: "Mr. Nguyen underwent laser ablation for a tumor blocking 73% of his right upper lobe orifice. Using a rigid bronchoscope, we applied laser energy to vaporize and remove the tumor tissue. We achieved a partial debulking with 39% residual obstruction remaining. Blood loss was approximately 150mL, and hemostasis was secured.",
            9: "Reason: Malignant central airway occlusion.\nPrior blockage: ~73% obstruction at RUL aperture.\nProcess: Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm was spotted at the RUL aperture. Laser ablation was performed with serial tumor extraction. Numerous sweeps were done to attain maximal volume reduction. Extra APC/laser was employed for blood stanching and tumor base cautery. Subsequent blockage: ~39%."
        },
        9: { # Pt: Jackson, Daniel (31640 - Laser/Excision, RMS)
            1: "Indication: Malignant CAO (RMS 60%).\nProc: Excision/Laser.\nAction: Tumor removal.\nResult: 35% residual. 150mL EBL.\nPlan: ICU.",
            2: "PROCEDURE: Rigid bronchoscopy with tumor excision.\nSITE: Right Mainstem (RMS).\nFINDINGS: 60% obstruction.\nINTERVENTION: Laser assisted resection. Mechanical excision of tumor tissue.\nOUTCOME: 35% residual obstruction. Hemostasis achieved.",
            3: "CPT 31640 (Tumor excision).\nNote: Code reflects primary modality of excision despite laser use.\nSite: RMS.\nReduction: 60% -> 35%.\nEBL: 150mL.",
            4: "Procedure: Tumor Excision\nPt: Jackson, D.\nSteps:\n1. Rigid scope.\n2. RMS tumor identified.\n3. Laser/Mechanical removal.\n4. Hemostasis.\nResult: 35% residual.\nPlan: ICU.",
            5: "daniel jackson malignant airway obstruction rms 60 percent used general anesthesia rigid bronch laser and mechanical removal of the tumor got it down to 35 percent bleeding 150ml control with laser plan for icu.",
            6: "Malignant central airway obstruction Pre-procedure 60% obstruction at RMS. Under general anesthesia rigid bronchoscopy performed. Endobronchial tumor identified at RMS. Laser ablation performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Post-procedure 35% residual obstruction EBL 150mL Hemostasis achieved.",
            7: "[Indication]\nMalignant CAO, RMS 60%.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Laser assisted tumor excision. Residual obstruction 35%.\n[Plan]\nICU observation.",
            8: "Mr. Jackson had a 60% obstruction in his right mainstem bronchus. We performed a rigid bronchoscopy and used a combination of laser and mechanical excision to remove the tumor. The obstruction was reduced to 35%. He lost about 150mL of blood, but we controlled the bleeding effectively.",
            9: "Reason: Malignant central airway occlusion.\nPrior blockage: ~60% obstruction at RMS.\nProcess: Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm was spotted at the RMS. Laser ablation was performed with serial tumor extraction. Numerous sweeps were done to attain maximal volume reduction. Subsequent blockage: ~35%."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns list of mock data to ensure distinct names for each variation.
    Indexes correspond to the 10 notes in the source file.
    """
    return [
        {"idx": 0, "orig_name": "Cynthia Jones", "orig_age": 78, "names": ["Mary Smith", "Helen Johnson", "Margaret Williams", "Ruth Brown", "Dorothy Jones", "Virginia Miller", "Frances Davis", "Elizabeth Garcia", "Alice Rodriguez"]},
        {"idx": 1, "orig_name": "Barbara Robinson", "orig_age": 62, "names": ["Patricia Wilson", "Linda Martinez", "Barbara Anderson", "Elizabeth Taylor", "Jennifer Thomas", "Maria Hernandez", "Susan Moore", "Margaret Martin", "Dorothy Jackson"]},
        {"idx": 2, "orig_name": "Betty Green", "orig_age": 71, "names": ["Sarah Thompson", "Karen White", "Nancy Lopez", "Betty Lee", "Lisa Gonzalez", "Sandra Harris", "Helen Clark", "Donna Lewis", "Carol Robinson"]},
        {"idx": 3, "orig_name": "Daniel Allen", "orig_age": 51, "names": ["James Walker", "John Perez", "Robert Hall", "Michael Young", "William Allen", "David Sanchez", "Richard Wright", "Charles King", "Joseph Scott"]},
        {"idx": 4, "orig_name": "Kathleen Baker", "orig_age": 69, "names": ["Michelle Green", "Laura Baker", "Sarah Adams", "Kimberly Nelson", "Deborah Hill", "Jessica Ramirez", "Shirley Campbell", "Cynthia Mitchell", "Angela Roberts"]},
        {"idx": 5, "orig_name": "Kevin Hernandez", "orig_age": 71, "names": ["Thomas Carter", "Christopher Phillips", "Daniel Evans", "Paul Turner", "Mark Torres", "Donald Parker", "George Collins", "Kenneth Edwards", "Steven Stewart"]},
        {"idx": 6, "orig_name": "Anthony Baker", "orig_age": 70, "names": ["Edward Flores", "Brian Morris", "Ronald Nguyen", "Anthony Murphy", "Kevin Rivera", "Jason Cook", "Matthew Rogers", "Gary Morgan", "Timothy Peterson"]},
        {"idx": 7, "orig_name": "Lisa Rivera", "orig_age": 51, "names": ["Melissa Cooper", "Brenda Reed", "Amy Bailey", "Anna Bell", "Rebecca Gomez", "Virginia Kelly", "Kathleen Howard", "Pamela Ward", "Martha Cox"]},
        {"idx": 8, "orig_name": "Daniel Nguyen", "orig_age": 75, "names": ["Frank Diaz", "Scott Richardson", "Eric Wood", "Stephen Watson", "Andrew Brooks", "Raymond Bennett", "Gregory Gray", "Joshua James", "Jerry Reyes"]},
        {"idx": 9, "orig_name": "Daniel Jackson", "orig_age": 66, "names": ["Dennis Cruz", "Walter Hughes", "Patrick Price", "Peter Myers", "Harold Long", "Douglas Foster", "Henry Sanders", "Carl Ross", "Arthur Morales"]}
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
            try:
                note_entry["note_text"] = variations_text[idx][style_num]
            except KeyError:
                print(f"Warning: Missing text variation for Note {idx} Style {style_num}. Skipping.")
                continue
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
            
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
    output_filename = output_dir / "synthetic_stent_notes_part_055.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()