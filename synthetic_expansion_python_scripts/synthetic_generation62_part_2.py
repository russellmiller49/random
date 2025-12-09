import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_062_part2.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations.
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    # Styles:
    # 1. Terse Surgeon
    # 2. Academic Attending
    # 3. Billing Coder
    # 4. Trainee/Resident
    # 5. Sloppy Dictation
    # 6. Header-less
    # 7. Templated
    # 8. Narrative Flow
    # 9. Synonym Swapper

    variations = {
        0: { # Michael Brown (Flexible, Mid-trachea granulation)
            1: "Indication: Tracheal granulation/stenosis. Post-trach.\nProc: Flex Bronch w/ mechanical debulking.\nFindings: Mid-tracheal granulation, 60% stenosis.\nAction: Forceps removal and snare resection. No ablation.\nEBL: <10cc.\nPlan: D/C on PPI/ICS.",
            2: "PROCEDURE: Flexible Fiberoptic Bronchoscopy with Excision of Tracheal Lesion.\nCLINICAL SUMMARY: The patient, presenting with stridor and cough, was found to have post-tracheostomy granulation tissue. Under moderate sedation, the airway was inspected. Circumferential granulation tissue at the mid-trachea compromised the lumen. Mechanical excision was performed utilizing biopsy forceps and electrocautery snare (cold cut) to restore patency. No thermal ablative modalities were employed. Hemostasis was achieved.",
            3: "CPT Code 31640 Support:\n- Technique: Mechanical excision of endobronchial tissue.\n- Instruments: Forceps and Snare.\n- Location: Mid-trachea (Central Airway).\n- Pathology: Granulation tissue causing stenosis.\n- Note: Thermal ablation was explicitly NOT used, distinguishing this from 31641.",
            4: "Resident Note:\nProcedure: Flex bronch debulking.\nAttending: Dr. Patel.\nSteps:\n1. Sedation start.\n2. Scope introduced.\n3. Identified granulation tissue at old trach site.\n4. Used forceps to debulk.\n5. Snare used for larger piece.\n6. Airway patent at end.\nNo complications.",
            5: "michael brown 70m here for the cough we did the bronchoscopy today mild sedation used saw the tissue in the trachea right where the trach used to be used the forceps to grab it and pull it out also the snare for the big piece no laser or anything just mechanical removal minimal bleeding patient did fine go home on steroids",
            6: "Flexible bronchoscopy with mechanical debulking of tracheal granulation tissue. Indications: Chronic cough and wheeze post-decannulation. Anesthesia: Moderate sedation. Findings: Irregular granulation tissue at mid-trachea, 60% stenosis. Interventions: Piecemeal removal via forceps and snare resection. No thermal therapy. EBL 5-10mL. Disposition: Discharged.",
            7: "[Indication]\nSymptomatic tracheal granulation tissue.\n[Anesthesia]\nModerate Sedation.\n[Description]\nFlexible bronchoscopy performed. Mid-tracheal granulation tissue identified. Mechanical debulking performed using forceps and snare. Tissue removed. Lumen patency improved.\n[Plan]\nSurveillance bronchoscopy in 3 months.",
            8: "We brought Mr. Brown to the bronchoscopy suite to address his tracheal granulation tissue. Under moderate sedation, we advanced the flexible scope and located the obstruction in the mid-trachea. Using a combination of forceps and a snare, we mechanically excised the tissue piece by piece. We did not use any heat or ablation. The airway opened up nicely, and bleeding was minimal.",
            9: "Procedure: Bronchoscopic resection of tracheal outgrowth.\nTechnique: Mechanical extraction via grasping instruments and loop snare.\nTarget: Mid-tracheal lumen.\nResult: The obstructing mass was physically avulsed and retrieved. The airway caliber was restored without the use of cautery or laser."
        },
        1: { # Hannah Lee (Rigid, BI SCLC)
            1: "Dx: SCLC, BI obstruction.\nProc: Rigid Bronch, mechanical debulking.\nFindings: 90% BI obstruction.\nAction: Rigid coring and forceps removal. Lumen 50-60% patent.\nEBL: 40ml.\nDisp: ICU, intubated.",
            2: "OPERATIVE REPORT: Rigid Bronchoscopy with Tumor Excision.\nINDICATION: Malignant central airway obstruction secondary to Small Cell Lung Carcinoma.\nFINDINGS: A bulky, exophytic tumor was visualized occluding the bronchus intermedius. Using the bevel of the rigid bronchoscope, mechanical coring was performed. Residual tumor burden was extracted via large-cup forceps. The airway was recanalized to approximately 60% patency without the use of thermal energy. Hemostasis was secured.",
            3: "Code Selection: 31640 (Bronchoscopy with excision of tumor).\n- Approach: Rigid Bronchoscopy.\n- Method: Mechanical coring and forceps excision.\n- Site: Bronchus Intermedius.\n- Documentation confirms tumor removal to relieve obstruction.",
            4: "Procedure: Rigid Bronch Debulking\nPatient: Hannah Lee\nSteps:\n1. General Anesthesia.\n2. Rigid scope inserted.\n3. Located tumor in BI.\n4. Cored with scope barrel.\n5. Used forceps to pull out tumor chunks.\n6. Suctioned blood/mucus.\n7. ETT placed post-proc.",
            5: "procedure note for ms lee rigid bronchoscopy under ga she has sclc blocking the bronchus intermedius we went in with the rigid scope and cored out the tumor used forceps to grab the rest of it opened it up to maybe 60 percent bleeding controlled with saline and epi keeping her intubated for the icu",
            6: "Rigid bronchoscopy with mechanical debulking of bronchus intermedius tumor. Patient with SCLC and RLL collapse. Under general anesthesia, the rigid scope was introduced. Bulky tumor found in BI. Mechanical debulking performed via rigid coring and forceps. No balloon or thermal ablation. Hemostasis achieved. Patient remains intubated.",
            7: "[Indication]\nMalignant airway obstruction, Bronchus Intermedius.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy performed. Tumor cored and excised using mechanical forceps. Obstruction reduced from 90% to 40%. No thermal ablation utilized.\n[Plan]\nICU admission.",
            8: "Ms. Lee underwent a rigid bronchoscopy to treat the blockage in her airways caused by lung cancer. We found a large tumor blocking the bronchus intermedius. Using the rigid scope itself and forceps, we mechanically removed the tumor in pieces. We successfully opened the airway to about 60% of its normal size without needing to burn the tissue. She will stay in the ICU.",
            9: "Operation: Rigid airway endoscopy with physical tumor morcellation.\nFindings: Neoplasm occluding the intermediate bronchus.\nIntervention: The lesion was sheared using the scope tip and extracted with graspers. The passage was mechanically cleared. No coagulation devices employed."
        },
        2: { # Christopher Adams (Rigid, Distal trachea/Carina)
            1: "Indication: Squamous cell CA, carinal obstruction.\nProc: Rigid bronch, debulking.\nFindings: Distal trachea/carina tumor.\nAction: Coring, forceps, snare. No thermal ablation.\nResult: Airway patent.\nEBL: 25ml.",
            2: "PROCEDURE NOTE: Rigid Bronchoscopic Debridement of Carinal Tumor.\nCLINICAL CONTEXT: Patient with squamous cell carcinoma presenting with mixed obstruction.\nOPERATIVE DETAILS: The rigid bronchoscope was engaged to mechanically core the exophytic tumor burden at the distal trachea and carina. A polypoid component was resected via snare. Forceps were utilized for fine debulking. This mechanical excision restored patency to the mainstem bronchi. Ablative technologies were not required.",
            3: "Billing: 31640.\nService: Bronchoscopy with excision of tumor.\nMethod: Mechanical debulking (Coring, Forceps, Snare).\nSite: Distal Trachea/Carina.\nNote: Documentation explicitly states no thermal ablation (RFA, cryo, etc) was used.",
            4: "Resident Note:\nPt: C. Adams\nProc: Rigid Debulking\n1. GA / Rigid scope.\n2. Tumor at carina/distal trachea.\n3. Mechanical coring done.\n4. Snare used for polypoid part.\n5. Forceps cleanup.\n6. Good airflow after.\n7. Extubated -> Floor.",
            5: "christopher adams rigid bronchoscopy for the carinal tumor general anesthesia used rigid scope went down saw the tumor blocking the distal trachea and carina cored it out with the scope and used the snare and forceps to get the pieces out looks much better now bleeding stopped with cold saline extubated to recovery",
            6: "Rigid bronchoscopy with mechanical debulking of distal tracheal and carinal tumor. Indication: Squamous cell lung cancer with obstruction. Findings: Tumor reducing lumen by 75%. Interventions: Rigid coring, forceps debulking, and snare resection. No thermal ablation. Hemostasis achieved. Patient extubated and stable.",
            7: "[Indication]\nCarinal obstruction, Squamous Cell CA.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nMechanical debulking of distal tracheal and carinal tumor performed. Rigid coring and forceps excision used. Snare resection for polypoid portion. Airway patency restored.\n[Plan]\nAdmit to oncology floor.",
            8: "We performed a rigid bronchoscopy on Mr. Adams to clear the tumor blocking his windpipe and carina. Once asleep, we used the rigid tube to core through the tumor mass. We also used forceps and a snare to remove the pieces. We didn't use any lasers or heat. By the end, both main airways were visible and clear. He was woken up and taken to recovery.",
            9: "Procedure: Rigid endoscopic resection of airway neoplasm.\nSite: Carina and lower trachea.\nMethod: The mass was physically excised using coring maneuvers and grasping tools. A wire loop was used for the polypoid segment. No thermal destruction was applied."
        },
        3: { # Aisha Khan (Flexible, RUL)
            1: "Indication: RUL collapse, tumor.\nProc: Flex bronch, debulking.\nFindings: 80% obstruction RUL bronchus.\nAction: Forceps/snare resection. No thermal tx.\nEBL: 10ml.\nDisp: Home.",
            2: "OPERATIVE REPORT: Flexible Bronchoscopy with Mechanical Tumor Excision.\nINDICATION: Lobar collapse secondary to endobronchial obstruction.\nFINDINGS: A polypoid lesion was identified occluding the Right Upper Lobe (RUL) bronchus. \nPROCEDURE: Mechanical excision was executed utilizing biopsy forceps and a snare device. The tumor was resected piecemeal until the lobar orifice was widely patent. No thermal ablative techniques were employed during this session.",
            3: "CPT 31640.\nRationale: Therapeutic bronchoscopy with excision of tumor.\nTechnique: Mechanical removal via forceps and snare.\nTarget: Right Upper Lobe bronchus.\nDifferentiation: No APC, Laser, or Cryo used (rules out 31641).",
            4: "Procedure: Flex Bronch Debulking\nPatient: Aisha K.\nIndication: RUL tumor.\nSteps:\n1. LMA/Propofol.\n2. Scope to RUL.\n3. Tumor found.\n4. Snare and forceps used to remove it.\n5. RUL open.\nPlan: CT in 6 weeks.",
            5: "bronchoscopy note for aisha khan she has that rul tumor causing collapse we went in with the flex scope and moderate sedation saw the tumor at the rul opening used the snare and forceps to take it out piece by piece opened it up pretty good no laser or anything minimal bleeding she goes home today",
            6: "Flexible bronchoscopy with mechanical debulking of RUL tumor. Indication: Persistent RUL collapse. Anesthesia: Moderate sedation via LMA. Findings: Polypoid tumor at RUL origin, 80% obstruction. Interventions: Forceps and snare resection. No thermal techniques. EBL 10mL. Discharged home.",
            7: "[Indication]\nRUL obstruction, endobronchial tumor.\n[Anesthesia]\nModerate.\n[Description]\nFlexible bronchoscopy. Mechanical debulking of RUL tumor using forceps and snare. Piecemeal removal. RUL bronchus patent post-procedure.\n[Plan]\nDischarge. Follow-up CT.",
            8: "Ms. Khan came in for a bronchoscopy to treat a tumor blocking her right upper lung. We used a flexible scope and moderate sedation. We found the tumor and removed it bit by bit using small forceps and a snare tool. We didn't use any heat or freezing. The airway to the upper lobe is now open. She was discharged home.",
            9: "Operation: Flexible endoscopic extraction of bronchial mass.\nLocation: Right superior lobar bronchus.\nTechnique: The obstruction was physically dismantled using graspers and a wire loop. The mass was avulsed in fragments. No thermal cautery was utilized."
        },
        4: { # Robert Wilson (Rigid, Carina/RMS)
            1: "Indication: NSCLC, RMS/Carina obstruction.\nProc: Rigid bronch, debulking.\nAction: Coring, forceps, microdebrider. No thermal ablation.\nResult: Lumen 50% open.\nBleeding: Moderate, controlled.\nDisp: ICU.",
            2: "PROCEDURE NOTE: Rigid Bronchoscopic Recanalization.\nINDICATION: High-grade obstruction of the carina and right mainstem bronchus due to NSCLC.\nTECHNIQUE: Under general anesthesia, the rigid bronchoscope was used to core through the tumor burden. Additional mechanical debulking was achieved via forceps and a microdebrider to excise tissue and smooth the airway wall. Thermal ablation was not utilized. Patency was restored to approximately 50%.",
            3: "Code: 31640.\nService: Bronchoscopy with excision of tumor.\nMethods: Rigid coring, Forceps excision, Microdebrider.\nSite: Carina and Right Mainstem.\nCompliance: Purely mechanical removal documented.",
            4: "Resident Note:\nPt: R. Wilson\nProc: Rigid Debulking\n1. GA / Rigid scope.\n2. Tumor at Carina/RMS.\n3. Cored with scope.\n4. Used microdebrider and forceps.\n5. Bleeding controlled w/ epinephrine.\n6. Airway better.\nPlan: ICU.",
            5: "robert wilson rigid bronchoscopy for the tumor blocking the right mainstem and carina general anesthesia used rigid coring to cut through the tumor then used the microdebrider to clean it up and forceps to pull out chunks no burning or freezing used bleeding was moderate but stopped it intubated to icu",
            6: "Rigid bronchoscopy with mechanical debulking of carinal/right mainstem tumor. Indication: Severe dyspnea, NSCLC. Findings: 80-85% obstruction. Interventions: Rigid coring, forceps, and microdebrider used for mechanical excision. No thermal ablation. Hemostasis achieved. Patient admitted to ICU.",
            7: "[Indication]\nCarinal and RMS obstruction, NSCLC.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nMechanical debulking performed. Rigid coring, forceps, and microdebrider utilized. Tumor excised. Lumen improved to 50%.\n[Plan]\nICU, intubated.",
            8: "Mr. Wilson underwent a rigid bronchoscopy to open his airways. He has a large tumor at the carina and right mainstem. We mechanically cored through the tumor and used a microdebrider to shave away the tissue. Forceps were used to remove the debris. We avoided thermal therapy. The airway is about half open now, which is an improvement. He remains in the ICU.",
            9: "Procedure: Rigid endoscopic tumor resection.\nTarget: Carina and Right Mainstem Bronchus.\nMethod: The lesion was mechanically reduced using a coring scope, micro-shaver, and grasping forceps. The tissue was excised without thermal application."
        },
        5: { # Emily Garcia (Flexible, LLL)
            1: "Indication: LLL mass, recurrent pneumonia.\nProc: Flex bronch debulking.\nAction: Forceps/snare. No thermal/cryo.\nFindings: Exophytic LLL mass.\nResult: Patency improved.\nDisp: Home on abx.",
            2: "OPERATIVE SUMMARY: Flexible Bronchoscopy with Endobronchial Tumor Excision.\nINDICATION: Post-obstructive pneumonia secondary to Left Lower Lobe (LLL) mass.\nPROCEDURE: The LLL bronchus was visualized and found to be obstructed by an exophytic lesion. Mechanical excision was performed utilizing biopsy forceps and snare resection. The tumor was debulked to restore bronchial patency and facilitate drainage. No ablative modalities were required.",
            3: "CPT 31640.\nProcedure: Excision of tumor.\nModality: Mechanical (Forceps, Snare).\nAnatomy: Left Lower Lobe Bronchus.\nNote: Documentation confirms no cryotherapy, PDT, RFA, or APC used.",
            4: "Procedure: Flex Bronch w/ Debulking\nPt: Emily G.\nSteps:\n1. LMA placed.\n2. Scope to LLL.\n3. Mass found (75% blockage).\n4. Snare and forceps used to remove mass.\n5. Suctioned pus.\nPlan: Home w/ antibiotics.",
            5: "emily garcia bronchoscopy for that lll mass causing pneumonia moderate sedation used saw the tumor blocking the lll used the snare to cut it and forceps to grab the pieces cleaned out the pus no laser or cryo used bleeding minimal discharge home",
            6: "Flexible bronchoscopy with mechanical debulking of LLL endobronchial tumor. Indication: Recurrent post-obstructive pneumonia. Findings: Exophytic lesion LLL bronchus, 75% obstruction. Interventions: Forceps debulking and snare resection. No thermal techniques. EBL 10mL. Discharged home.",
            7: "[Indication]\nLLL obstruction, pneumonia.\n[Anesthesia]\nModerate.\n[Description]\nFlexible bronchoscopy. Mechanical debulking of LLL tumor using forceps and snare. Purulent secretions suctioned. Airway patent.\n[Plan]\nAntibiotics, follow-up in 3 months.",
            8: "We performed a flexible bronchoscopy on Ms. Garcia to treat the mass blocking her left lower lung. We found the tumor and the infection behind it. We used forceps and a snare to mechanically cut and remove the tumor tissue. We did not use any burning or freezing tools. The airway is clear now. She was sent home with antibiotics.",
            9: "Operation: Flexible endoscopic mass excision.\nSite: Left lower lobar bronchus.\nTechnique: The obstruction was physically removed using a wire loop and grasping tools. The tissue was avulsed to restore the lumen. No thermal energy was applied."
        },
        6: { # Steven Park (Rigid, Distal trachea)
            1: "Indication: Critical tracheal obstruction, SCC.\nProc: Rigid bronch debulking.\nAction: Coring, forceps, microdebrider. No ablation.\nFindings: Pinpoint lumen.\nResult: Lumen restored.\nDisp: ICU.",
            2: "PROCEDURE NOTE: Rigid Bronchoscopic Tumor Excision.\nCLINICAL SUMMARY: Patient presenting with critical central airway obstruction due to squamous cell carcinoma.\nOPERATIVE DETAILS: The rigid bronchoscope was utilized to perform mechanical coring of the distal tracheal tumor. Following coring, forceps and a microdebrider were employed to excise residual tumor burden and smooth the airway walls. The procedure relied entirely on mechanical debulking; no thermal ablation was performed.",
            3: "Billing Code: 31640.\nDescription: Bronchoscopy with excision of tumor.\nTechnique: Rigid coring, Microdebrider, Forceps.\nSite: Distal Trachea.\nSpecifics: Mechanical removal only; no thermal modalities documented.",
            4: "Resident Note:\nPt: Steven Park\nProc: Rigid Debulking\n1. GA / Rigid scope.\n2. Critical stenosis distal trachea.\n3. Cored through tumor.\n4. Microdebrider used for cleanup.\n5. Forceps for chunks.\n6. Airway opened up.\n7. Stayed intubated.",
            5: "steven park rigid bronchoscopy for the tracheal tumor it was really tight pinpoint lumen used the rigid scope to core it out and the microdebrider to clean it up forceps to grab the pieces strictly mechanical debulking no laser bleeding was moderate but stopped it icu admit",
            6: "Rigid bronchoscopy with mechanical debulking of distal tracheal tumor. Indication: Critical obstruction, SCC. Findings: Pinpoint lumen. Interventions: Rigid coring, forceps, and microdebrider. Explicit mechanical excision; no ablation. Hemostasis achieved. Patient to ICU.",
            7: "[Indication]\nCritical tracheal obstruction, SCC.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nMechanical debulking performed. Rigid coring, forceps, and microdebrider used. Tumor excised. Lumen restored.\n[Plan]\nICU management.",
            8: "Mr. Park required an urgent rigid bronchoscopy for a tumor blocking his trachea. Under general anesthesia, we used the rigid scope to core through the blockage. We also used a microdebrider and forceps to remove the tumor tissue. This was a mechanical removal; no ablation was used. We managed to open the airway significantly. He is in the ICU.",
            9: "Procedure: Rigid endoscopic resection of tracheal neoplasm.\nMethod: The mass was cored and debrided using mechanical instruments including a micro-shaver. The obstruction was physically excised. No thermal coagulation was utilized."
        },
        7: { # Laura Perez (Flexible, Mid-trachea benign)
            1: "Indication: Benign tracheal stenosis.\nProc: Flex bronch debulking.\nFindings: Granulation/Scar mid-trachea.\nAction: Forceps/snare removal. No dilation/ablation.\nResult: Mild residual narrowing.\nDisp: Home.",
            2: "OPERATIVE REPORT: Flexible Bronchoscopy with Mechanical Excision of Stenosis.\nINDICATION: Symptomatic post-intubation tracheal stenosis.\nFINDINGS: A circumferential area of granulation tissue and scarring was noted in the mid-trachea. \nINTERVENTION: Mechanical debulking was performed utilizing forceps to excise granulation tissue and a snare to resect a fibrotic ridge. No balloon dilation or thermal ablation was performed during this session. The lumen caliber was significantly improved.",
            3: "CPT: 31640.\nDiagnosis: Benign tracheal stenosis (granulation/scar).\nProcedure: Excision of tumor/tissue.\nTools: Forceps, Snare.\nNote: Purely mechanical excision. No dilation (31630) or ablation (31641) performed.",
            4: "Procedure: Flex Bronch Debulking\nPt: Laura P.\nSteps:\n1. Moderate sedation.\n2. Scope to mid-trachea.\n3. Found scar/granulation.\n4. Removed with forceps and snare.\n5. Airway looks better.\nPlan: Home.",
            5: "laura perez bronchoscopy for tracheal stenosis she had a tube before saw some granulation and scar tissue used the forceps and snare to cut it out didn't dilate or burn it just cut it out airway is better minimal bleeding discharge home",
            6: "Flexible bronchoscopy with mechanical debulking of granulation tissue and scar. Indication: Benign post-intubation stenosis. Findings: Mid-tracheal narrowing. Interventions: Forceps debulking and snare resection. No balloon or ablation. EBL 5mL. Discharged home.",
            7: "[Indication]\nBenign tracheal stenosis.\n[Anesthesia]\nModerate.\n[Description]\nFlexible bronchoscopy. Mechanical debulking of granulation tissue using forceps and snare. Fibrotic ridge resected. Lumen improved.\n[Plan]\nObservation, discharge.",
            8: "We performed a flexible bronchoscopy on Ms. Perez to treat her tracheal stenosis. We found scarring and granulation tissue in the mid-trachea. We used forceps and a snare to mechanically remove this tissue. We did not use a balloon or any heat therapy. The airway is much more open now.",
            9: "Operation: Flexible endoscopic excision of tracheal cicatrix.\nFindings: Granuloma and fibrosis in the trachea.\nAction: The tissue was physically avulsed using graspers and a wire loop. The obstruction was resected without dilation or thermal energy."
        },
        8: { # Daniel Scott (Rigid, LMS)
            1: "Indication: LMS obstruction, NSCLC.\nProc: Rigid bronch debulking.\nAction: Coring, forceps. No ablation.\nFindings: 85% obstruction.\nResult: Moderate residual narrowing.\nDisp: Floor.",
            2: "PROCEDURE NOTE: Rigid Bronchoscopic Tumor Debridement.\nINDICATION: Left Mainstem (LMS) obstruction secondary to NSCLC.\nOPERATIVE DETAILS: A rigid bronchoscope was introduced to the left mainstem bronchus. The obstructing tumor was mechanically debulked utilizing the rigid coring technique and biopsy forceps. No thermal ablative tools or balloon dilation were employed. The airway was recanalized to allow ventilation of the left lung.",
            3: "Billing: 31640.\nSite: Left Mainstem Bronchus.\nMethod: Mechanical excision (Rigid Coring, Forceps).\nExclusions: No ablation, no dilation.\nService: Therapeutic debulking of tumor.",
            4: "Resident Note:\nPt: Daniel Scott\nProc: Rigid Debulking LMS\n1. GA.\n2. Rigid scope to LMS.\n3. Cored tumor.\n4. Removed pieces with forceps.\n5. Bleeding controlled.\n6. Can see lobar bronchi now.\nPlan: Oncology floor.",
            5: "daniel scott rigid bronchoscopy for that left mainstem tumor general anesthesia used the rigid scope to core it out forceps to grab the rest no laser or anything just mechanical removal airway is open enough to see the lobes bleeding stopped admit to floor",
            6: "Rigid bronchoscopy with mechanical debulking of left mainstem tumor. Indication: Central obstruction, NSCLC. Findings: 85% occlusion LMS. Interventions: Rigid coring and forceps debulking. No ablation. Lumen improved. Patient extubated and admitted.",
            7: "[Indication]\nLeft mainstem obstruction, NSCLC.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nMechanical debulking performed. Rigid coring and forceps used. Tumor excised. Lobar orifices visualized.\n[Plan]\nAdmit to oncology.",
            8: "Mr. Scott underwent a rigid bronchoscopy to clear a tumor from his left main bronchial tube. We used the rigid scope to core out the tumor and forceps to remove the pieces. It was a mechanical removal without burning. We opened the airway enough to see the branches into the lobes. He is doing well and heading to the floor.",
            9: "Procedure: Rigid endoscopic resection of bronchial neoplasm.\nLocation: Left main bronchus.\nTechnique: The mass was cored and extracted using mechanical instruments. The obstruction was relieved without thermal coagulation."
        },
        9: { # Isabel Ramos (Rigid, BI)
            1: "Indication: BI obstruction.\nProc: Rigid bronch debulking.\nAction: Coring, forceps. No thermal.\nFindings: 80% obstruction.\nResult: 60% patent.\nDisp: Floor.",
            2: "OPERATIVE REPORT: Rigid Bronchoscopy with Mechanical Tumor Excision.\nINDICATION: Symptomatic obstruction of the Bronchus Intermedius (BI).\nFINDINGS: A polypoid mass was identified occluding the BI. \nINTERVENTION: Using the rigid bronchoscope barrel, mechanical coring was performed. Forceps were utilized to excise the remaining tumor fragments in a piecemeal fashion. No thermal ablation or balloon dilation was required. The airway lumen was restored to approximately 60% patency.",
            3: "CPT Code: 31640.\nDescriptor: Bronchoscopy with excision of tumor.\nTechnique: Mechanical (Rigid coring, Forceps).\nSite: Bronchus Intermedius.\nNote: Documentation confirms no thermal energy used.",
            4: "Procedure: Rigid Bronch Debulking\nPt: Isabel R.\nSteps:\n1. GA.\n2. Rigid scope to BI.\n3. Cored tumor.\n4. Forceps removal.\n5. Suctioned blood.\n6. Airway open.\nPlan: Floor.",
            5: "isabel ramos rigid bronchoscopy for the bronchus intermedius tumor general anesthesia used the rigid scope to core the tumor forceps to pull it out strictly mechanical no burning airway looks better bleeding controlled discharge to floor",
            6: "Rigid bronchoscopy with mechanical debulking of BI tumor. Indication: Obstruction, dyspnea. Findings: Polypoid mass BI, 80% obstruction. Interventions: Rigid coring and forceps debulking. No thermal ablation. Hemostasis achieved. Extubated.",
            7: "[Indication]\nBronchus Intermedius obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nMechanical debulking performed. Rigid coring and forceps excision. Tumor removed. Lumen 60% patent.\n[Plan]\nOvernight observation.",
            8: "We performed a rigid bronchoscopy on Ms. Ramos to treat the tumor in her intermediate bronchus. We mechanically cored the tumor with the scope and used forceps to remove the tissue. No heat or balloons were used. The airway is now about 60% open. She was extubated and is stable.",
            9: "Procedure: Rigid endoscopic tumor extraction.\nSite: Intermediate bronchus.\nMethod: The lesion was physically cored and removed with graspers. The passage was cleared mechanically without thermal devices."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency
    # Corresponding to the 10 notes in the source file
    return [
        {"idx": 0, "orig_name": "Michael Brown", "orig_age": 70, "names": ["James Wilson", "Robert Taylor", "John Davis", "William Miller", "David Moore", "Richard Anderson", "Joseph Thomas", "Charles Jackson", "Thomas White"]},
        {"idx": 1, "orig_name": "Hannah Lee", "orig_age": 47, "names": ["Sarah Chen", "Jennifer Kim", "Lisa Park", "Michelle Wu", "Emily Wang", "Jessica Liu", "Ashley Zhang", "Amanda Yang", "Melissa Huang"]},
        {"idx": 2, "orig_name": "Christopher Adams", "orig_age": 62, "names": ["Daniel Lewis", "Paul Clark", "Mark Robinson", "Donald Walker", "George Hall", "Kenneth Allen", "Steven Young", "Edward King", "Brian Wright"]},
        {"idx": 3, "orig_name": "Aisha Khan", "orig_age": 59, "names": ["Fatima Ahmed", "Yasmin Ali", "Zara Hassan", "Amira Hussain", "Layla Malik", "Nora Iqbal", "Sana Rahman", "Mariam Shaikh", "Hina Khan"]},
        {"idx": 4, "orig_name": "Robert Wilson", "orig_age": 73, "names": ["Frank Harris", "Gary Martin", "Larry Thompson", "Scott Garcia", "Stephen Martinez", "Raymond Robinson", "Gregory Clark", "Joshua Rodriguez", "Jerry Lewis"]},
        {"idx": 5, "orig_name": "Emily Garcia", "orig_age": 52, "names": ["Maria Rodriguez", "Linda Hernandez", "Barbara Martinez", "Elizabeth Gonzalez", "Susan Lopez", "Margaret Perez", "Dorothy Wilson", "Lisa Anderson", "Nancy Thomas"]},
        {"idx": 6, "orig_name": "Steven Park", "orig_age": 60, "names": ["Kevin Lee", "Jason Choi", "Brian Kim", "Eric Jung", "Jeffrey Han", "Ryan Kang", "Jacob Moon", "Gary Shin", "Nicholas Song"]},
        {"idx": 7, "orig_name": "Laura Perez", "orig_age": 44, "names": ["Sandra Torres", "Ashley Ramirez", "Kimberly Flores", "Donna Rivera", "Carol Gomez", "Michelle Diaz", "Emily Reyes", "Amanda Morales", "Melissa Castillo"]},
        {"idx": 8, "orig_name": "Daniel Scott", "orig_age": 68, "names": ["Timothy Baker", "Ronald Green", "Jason Adams", "Jeffrey Campbell", "Ryan Mitchell", "Jacob Carter", "Gary Roberts", "Nicholas Phillips", "Eric Evans"]},
        {"idx": 9, "orig_name": "Isabel Ramos", "orig_age": 57, "names": ["Patricia Gutierrez", "Jennifer Ortiz", "Linda Chavez", "Elizabeth Silva", "Susan Nuñez", "Margaret Medina", "Dorothy Vargas", "Lisa Castro", "Nancy Mendez"]}
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
            
            # Determine new random date (within 2024-2025)
            # Keeping year mostly 2024/2025 as per source docs usually
            rand_date_obj = generate_random_date(2024, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            # Check if this index has a variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: No text variation found for Note {idx} Style {style_num}. Using original.")
            
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
    output_filename = output_dir / "synthetic_bronchoscopy_notes_part_062.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()