import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_062_part3.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Jasmine Young (RML Carcinoid)
            1: "Proc: Flex Bronch, mechanical debulking RML.\nIndication: Carcinoid, recurrent pneumonia.\nFindings: 70% obstruction RML, vascular mass.\nAction: Snare resection + forceps removal. No thermal used.\nResult: 20ml EBL. Hemostasis w/ cold saline/epi.\nPlan: Home, antibiotics.",
            2: "OPERATIVE REPORT: ENDOBRONCHIAL RESECTION\n\nINDICATION: The patient, a 39-year-old female, presented with a documented endobronchial typical carcinoid tumor occluding the right middle lobe (RML) bronchus, complicated by recurrent post-obstructive pneumonitis.\n\nPROCEDURE NARRATIVE: Under moderate sedation, the airway was accessed via laryngeal mask airway. Inspection revealed a rounded, vascular lesion obstructing approximately 70% of the RML orifice. Mechanical excision was prioritized. The lesion was systematically debulked utilizing a combination of electrocautery-independent snare resection and biopsy forceps. Hemostasis was achieved via cold saline lavage and transient topical epinephrine application.\n\nIMPRESSION: Successful mechanical resection of RML carcinoid tumor.",
            3: "CPT Selection: 31640 (Bronchoscopy with excision of tumor).\nRationale: The procedure involved the specific use of mechanical tools including a snare and forceps to debulk and excise an endobronchial mass in the Right Middle Lobe. No thermal energy (laser/APC) was utilized, confirming the mechanical nature of the excision. The obstruction was relieved from 70% to patency.",
            4: "Procedure: Bronch w/ mechanical debulking\nAttending: Dr. Farouk\n\nSteps:\n1. LMA placed, moderate sedation.\n2. Scope to RML.\n3. Saw vascular mass (carcinoid).\n4. Used snare to cut base.\n5. Used forceps to remove rest of tumor.\n6. Cold saline for bleeding.\n\nComplications: None.",
            5: "Procedure note for Jasmine Young she has that carcinoid in the RML causing pneumonia. We went in with the flex scope used propofol. Saw the mass blocking about 70 percent. We used the snare to grab it and forceps to pull the rest out. Didn't use any heat just mechanical removal. Bleeding was okay controlled with some saline and epi. She went home same day.",
            6: "INTERVENTIONAL PULMONOLOGY - MECHANICAL DEBULKING OF CARCINOID. Patient: 39-year-old female. Indication: Endobronchial typical carcinoid in right middle lobe bronchus causing recurrent pneumonia. Procedure: Flexible bronchoscopy with mechanical debulking/excision of carcinoid (CPT 31640). Findings: Rounded, vascular mass at RML bronchus origin with ~70% obstruction. Interventions: Snare resection and forceps debulking were used to mechanically excise and debulk the tumor. No thermal ablation performed. Hemostasis: Controlled with cold saline; short application of topical epinephrine.",
            7: "[Indication]\nEndobronchial typical carcinoid RML, recurrent pneumonia.\n[Anesthesia]\nModerate sedation (propofol/fentanyl), LMA.\n[Description]\n70% obstruction RML. Snare resection and forceps debulking performed to excise tumor mechanically. No thermal ablation.\n[Plan]\nDischarge home. IP clinic f/u 4 weeks.",
            8: "We performed a flexible bronchoscopy on Ms. Young to address the carcinoid tumor in her right middle lobe. Upon entering the airway, we identified a vascular mass obstructing the bronchus by about 70%. We proceeded to mechanically remove the tumor using a combination of snare resection and forceps debulking. We avoided thermal ablation. Hemostasis was maintained using cold saline and a small amount of epinephrine.",
            9: "Procedure: Flexible bronchoscopy with mechanical extraction of carcinoid.\nReason: Recurrent infection due to blockage.\nFindings: Vascular growth at RML origin.\nMethod: We employed snare resection and forceps to extirpate the lesion. No heat therapy was utilized.\nStatus: Hemostasis secured with vasoconstrictors."
        },
        1: { # Kevin Brooks (Proximal Tracheal Tumor)
            1: "Proc: Rigid Bronch, mechanical debulking.\nIndication: Proximal tracheal tumor, dyspnea.\nFindings: Sessile tumor, anterior trachea, 70% stenosis.\nAction: Rigid coring + forceps removal. Snare for pedunculated part. No laser.\nResult: 15ml EBL. Airway patent.\nPlan: Extubate, home.",
            2: "PROCEDURE: RIGID TRACHEOSCOPY AND TUMOR EXCISION\n\nCLINICAL HISTORY: 55-year-old male with symptomatic proximal tracheal obstruction.\n\nOPERATIVE FINDINGS: A sessile, obstructing lesion was identified on the anterior wall of the proximal trachea, compromising the lumen by approximately 70%.\n\nTECHNIQUE: The rigid tracheoscope was introduced under general anesthesia. Mechanical debulking was executed utilizing the beveled tip of the rigid scope for coring, supplemented by heavy grasping forceps. A snare was utilized for a focal pedunculated component. No thermal ablative modalities were employed. Hemostasis was excellent.",
            3: "Billing Code: 31640.\nSite: Proximal Trachea.\nMethodology: Mechanical debulking via Rigid Bronchoscopy.\nTools:\n- Rigid Coring (mechanical excision).\n- Forceps removal.\n- Snare resection.\nExclusions: No laser, APC, or cryotherapy used.\nOutcome: Restoration of airway patency.",
            4: "Resident Note: Rigid Bronch / Debulking\nPt: Kevin Brooks\n\n1. General Anesthesia, Rigid scope inserted.\n2. Tumor seen in proximal trachea (anterior wall).\n3. Used rigid barrel to core the tumor.\n4. Used forceps to grab pieces.\n5. Snared a loose piece.\n6. Washed with cold saline.\n\nEst blood loss 15cc.",
            5: "Kevin Brooks 55M here for the tracheal tumor. He was having trouble breathing. We took him to the OR used general anesthesia. Put the rigid scope in. Saw the tumor narrowing the trachea about 70 percent. We cored it out with the scope and used forceps to pull the pieces. Also used a snare. Did not use any laser. Bleeding was minimal. He woke up fine.",
            6: "BRONCHOSCOPY PROCEDURE NOTE - MECHANICAL DEBULKING OF TRACHEAL TUMOR. Indication: Proximal tracheal tumor with noisy breathing and exertional dyspnea. Procedure: Rigid bronchoscopy with mechanical debulking/excision of proximal tracheal mass (CPT 31640). Findings: Sessile tumor on anterior proximal tracheal wall narrowing lumen to ~70%. Interventions: Rigid coring and forceps debulking removed most of the lesion. Snare resection used to excise a pedunculated portion. No ablation or balloon used. Hemostasis: Minimal; controlled with cold saline.",
            7: "[Indication]\nProximal tracheal tumor, exertional dyspnea.\n[Anesthesia]\nGeneral, Rigid tracheoscope.\n[Description]\nAnterior tracheal tumor (70% obstruction). Rigid coring and forceps debulking performed. Snare resection utilized. No ablation.\n[Plan]\nDischarge to home.",
            8: "Mr. Brooks underwent a rigid bronchoscopy to treat a tumor in his upper windpipe. We found a mass on the front wall of the trachea blocking most of the airway. Using the rigid scope itself, we cored through the tumor and removed the tissue with forceps. We also used a snare to cut off a hanging piece. We didn't need to use any heat or lasers. The bleeding was very light.",
            9: "Procedure: Rigid endoscopy with mechanical extirpation of tracheal mass.\nIndication: Airway narrowing.\nAction: A sessile growth on the anterior wall was addressed. We utilized rigid coring and forceps to excise the tissue. A snare was employed for a pedunculated segment. No thermal tools were applied."
        },
        2: { # Jonas Meyer (Right Mainstem NSCLC)
            1: "Proc: Rigid Bronch, mechanical debulking RMS.\nIndication: Malignant obstruction (NSCLC).\nFindings: 85% occlusion RMS.\nAction: Rigid coring + forceps excision. No balloon/ablation.\nResult: 50ml EBL. Moderate oozing controlled.\nPlan: Admit oncology.",
            2: "OPERATIVE REPORT: PALLIATIVE AIRWAY RECANALIZATION\n\nINDICATION: Mr. Meyer presented with significant dyspnea secondary to malignant obstruction of the right mainstem bronchus (NSCLC).\n\nPROCEDURE: Rigid bronchoscopy was initiated under general anesthesia. The right mainstem bronchus was noted to be 85% occluded by tumor burden. Mechanical recanalization was performed utilizing the rigid scope for coring and large biopsy forceps for tissue extraction. The airway was successfully opened. Hemostasis was achieved with epinephrine and saline lavage.",
            3: "Service: Bronchoscopy with excision of tumor (31640).\nLocation: Right Mainstem Bronchus.\nTechnique: Mechanical excision via Rigid Bronchoscopy.\nTools utilized: Rigid coring device, Biopsy Forceps.\nModifiers: N/A.\nJustification: Procedure relies on mechanical removal of tissue to relieve 85% obstruction. No thermal modalities reported.",
            4: "Procedure: Rigid Bronch RMS Debulking\nPt: Jonas Meyer\n\nSteps:\n1. GA / Rigid scope.\n2. Identified RMS tumor (85% blocked).\n3. Cored through tumor with scope.\n4. Removed debris with forceps.\n5. Epinephrine for oozing.\n\nNo complications.",
            5: "Jonas Meyer had the rigid bronch today for that lung cancer blocking his right mainstem. It was tight like 85 percent blocked. We used the rigid scope to core it out and forceps to clear the debris. There was some bleeding about 50cc but we stopped it with epi and saline. No laser used just mechanical stuff. Admitted to the floor.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT - MECHANICAL DEBULKING. Indication: Malignant obstruction of right mainstem bronchus from non-small cell lung cancer. Procedure: Rigid bronchoscopy with mechanical debulking of right mainstem tumor (CPT 31640). Findings: Tumor narrowing right mainstem lumen by ~85% with retained secretions. Interventions: Rigid coring and forceps debulking used to mechanically debulk and excise the tumor. No ablation or balloon dilation employed.",
            7: "[Indication]\nMalignant obstruction RMS (NSCLC).\n[Anesthesia]\nGeneral, Rigid bronchoscopy.\n[Description]\n85% obstruction RMS. Mechanical debulking via rigid coring and forceps. No ablation.\n[Plan]\nAdmit to oncology floor.",
            8: "We took Mr. Meyer to the OR to open up his right main breathing tube which was blocked by cancer. Using a rigid metal tube, we mechanically cored out the tumor and pulled the pieces out with forceps. This opened up the airway significantly. There was some bleeding, which is expected, but we managed it with cold salt water and medication. He is going to the oncology ward.",
            9: "Procedure: Rigid bronchoscopy with mechanical resection of RMS mass.\nDiagnosis: NSCLC obstruction.\nTechnique: The airway was narrowed by 85%. We utilized rigid coring and forceps to extirpate the malignancy. No dilation or ablation was required.\nOutcome: Moderate oozing managed."
        },
        3: { # Natalie Ortiz (Tracheostomy Granulation)
            1: "Proc: Flex Bronch via trach, mechanical debulking.\nIndication: Stoma granulation/tumor.\nFindings: 60% obstruction distal trach.\nAction: Forceps + snare excision. No ablation.\nResult: 15ml EBL. Patent airway.\nPlan: Ward, f/u 6 weeks.",
            2: "PROCEDURE NOTE: BRONCHOSCOPIC MANAGEMENT OF AIRWAY OBSTRUCTION\n\nINDICATION: 62-year-old female with mixed granulation/tumor tissue obstructing the distal tracheostomy site.\n\nPROCEDURE: The airway was accessed via the existing tracheostomy stoma using a flexible bronchoscope. Inspection revealed nodular tissue obstructing 60% of the lumen. Mechanical debridement was performed utilizing biopsy forceps and snare cautery-independent resection. The obstructing tissue was successfully excised. Hemostasis was secured.",
            3: "CPT Code: 31640.\nApproach: Trans-tracheostomy.\nPathology: Granulation/Tumor.\nTechnique: Mechanical excision using forceps and snare.\nNote: Documentation specifies mechanical removal without thermal ablation, satisfying criteria for excision of tumor/tissue.",
            4: "Procedure: Flex Bronch via Trach\nPt: Natalie Ortiz\n\n1. Sedation + Lidocaine down trach.\n2. Scope inserted.\n3. Found granulation/tumor at stoma tip.\n4. Used forceps to bite it away.\n5. Used snare to cut larger pieces.\n6. Cleaned up with saline.\n\nAirway looks better.",
            5: "Natalie Ortiz needing her trach cleaned out. There was granulation tissue and tumor growing in there blocking about 60 percent. We went in with the flex scope through the trach. Used forceps and a snare to cut it all out mechanically. Didnt burn anything. Bleeding was mild. She is back on the vent settings.",
            6: "BRONCHOSCOPY PROCEDURE NOTE - MECHANICAL DEBULKING IN PATIENT WITH TRACHEOSTOMY. Indication: Granulation tissue and tumor regrowth around tracheostomy stoma extending into tracheal lumen with dyspnea. Procedure: Flexible bronchoscopy via tracheostomy with mechanical debulking of granulation/tumor (CPT 31640). Findings: Granulation tissue and nodular tumor at distal tracheostomy site protruding into tracheal lumen (~60% obstruction). Interventions: Forceps debulking and snare resection were used to mechanically excise granulation and tumor tissue. No ablation used.",
            7: "[Indication]\nTracheostomy stoma obstruction (granulation/tumor).\n[Anesthesia]\nModerate sedation, topical lidocaine.\n[Description]\n60% obstruction distal trach. Forceps debulking and snare resection performed. No ablation.\n[Plan]\nReturn to ward. F/u 6 weeks.",
            8: "Ms. Ortiz was having trouble breathing due to tissue growth around her trach tube. We went in with a flexible scope through her trach. We found a mix of scar tissue and tumor blocking the airway. We used forceps and a snare to mechanically cut this tissue away and open the windpipe. We didn't use any heat treatments. She is back on her home ventilator settings now.",
            9: "Procedure: Flexible endoscopy via tracheostomy with mechanical resection.\nTarget: Granulation and tumor at stoma.\nAction: We observed 60% occlusion. Forceps and snare were employed to excise the obstructing tissue. Thermal tools were avoided.\nOutcome: Mild hemostasis required."
        },
        4: { # Olivia Martin (LMS Mass)
            1: "Proc: Rigid Bronch, mechanical debulking LMS.\nIndication: 90% obstruction LMS.\nFindings: Bulky tumor.\nAction: Rigid coring, forceps, microdebrider. No ablation.\nResult: 55ml EBL. Moderate oozing.\nPlan: Step-down unit.",
            2: "OPERATIVE REPORT: RIGID BRONCHOSCOPY FOR TUMOR DEBULKING\n\nINDICATION: Ms. Martin presented with critical left mainstem (LMS) obstruction secondary to a bulky endobronchial mass.\n\nPROCEDURE: Under general anesthesia, the rigid bronchoscope was advanced. The LMS was found to be 90% obstructed. Mechanical excision was performed sequentially using rigid coring, followed by forceps removal of debris. A microdebrider was utilized for fine debulking to maximize luminal patency. No thermal ablation was applied. Hemostasis was achieved with epinephrine instillation.",
            3: "Code: 31640.\nAnatomy: Left Mainstem Bronchus.\nMethod: Mechanical excision.\nInstruments:\n1. Rigid Coring (Scope tip).\n2. Forceps.\n3. Microdebrider (Mechanical shaver).\nNote: Use of microdebrider confirms mechanical nature of procedure. No thermal ablation codes applicable.",
            4: "Procedure: Rigid Bronch LMS\nPt: Olivia Martin\n\nSteps:\n1. GA / Rigid scope.\n2. LMS is 90% blocked.\n3. Cored with scope.\n4. Grabbed pieces with forceps.\n5. Used microdebrider to clean edges.\n6. Epinephrine for bleeding.\n\nPatient stable.",
            5: "Olivia Martin 64F for the left mainstem tumor. It was huge blocking like 90 percent. We did the rigid bronch. Used the scope to core it out then forceps. Also used the microdebrider which worked well to clear the rest. No burning or lasers. Bleeding was moderate but stopped with epi. She is in step down.",
            6: "INTERVENTIONAL PULMONOLOGY - MECHANICAL DEBULKING OF LMS MASS. Indication: Left mainstem endobronchial mass with near-complete obstruction and dyspnea at rest. Procedure: Rigid bronchoscopy with mechanical debulking of left mainstem tumor (CPT 31640). Findings: Bulky tumor at left mainstem origin narrowing lumen ~90%. Interventions: Rigid coring and forceps debulking were used to mechanically remove tumor. Microdebrider used for final debulking. No ablation.",
            7: "[Indication]\nLMS obstruction (90%), dyspnea.\n[Anesthesia]\nGeneral, Rigid bronchoscopy.\n[Description]\nRigid coring, forceps debulking, and microdebrider utilized. Mechanical excision of LMS tumor. No thermal ablation.\n[Plan]\nStep-down unit.",
            8: "Ms. Martin had a large tumor almost completely blocking her left main airway. We used a rigid bronchoscope to treat this. We physically cored out the center of the tumor with the tube, pulled out the chunks with forceps, and then used a microdebrider tool to shave away the rest. We didn't use any heat or lasers. It bled a bit, but we controlled it.",
            9: "Procedure: Rigid endoscopy with mechanical resection of LMS lesion.\nFindings: 90% occlusion.\nMethod: We employed rigid coring and forceps for gross removal. A microdebrider was utilized for fine resection. No ablation was performed.\nStatus: Moderate oozing managed."
        },
        5: { # Marcus Allen (RLL Polypoid Lesion)
            1: "Proc: Flex Bronch, mechanical debulking RLL.\nIndication: Recurrent pneumonia, RLL lesion.\nFindings: Polypoid lesion, 70% obstruction.\nAction: Snare + forceps excision. No thermal.\nResult: 10ml EBL. Minimal bleeding.\nPlan: Home, f/u CT.",
            2: "PROCEDURE NOTE: ENDOBRONCHIAL POLYPECTOMY\n\nINDICATION: Mr. Allen presented with a right lower lobe (RLL) endobronchial lesion complicated by post-obstructive pneumonia.\n\nPROCEDURE: Flexible bronchoscopy was performed under moderate sedation. A polypoid lesion was identified obstructing the superior segment of the RLL by approximately 70%. Mechanical excision was achieved utilizing a snare for the base and forceps for residual debulking. No thermal energy or balloon dilation was required. The airway caliber was significantly improved.",
            3: "Billing: 31640.\nTarget: Right Lower Lobe (Superior Segment).\nTools: Snare, Forceps.\nTechnique: Mechanical excision/debulking.\nExclusions: No laser, no APC, no balloon.\nOutcome: Obstruction relieved.",
            4: "Procedure: Flex Bronch RLL\nPt: Marcus Allen\n\n1. LMA/Sedation.\n2. Scope to RLL superior segment.\n3. Found polypoid mass (70% block).\n4. Snared it off.\n5. Cleaned up base with forceps.\n6. Minimal bleeding.\n\nPlan: Discharge.",
            5: "Marcus Allen here for that RLL lesion causing pneumonia. We went in with the flex scope. Found the polyp blocking the superior segment. Used a snare to cut it and forceps to grab the pieces. Just mechanical removal no heat used. Bleeding was minimal. Sending him home.",
            6: "BRONCHOSCOPY PROCEDURE NOTE - MECHANICAL DEBULKING OF RLL BRONCHUS LESION. Indication: Right lower lobe endobronchial lesion with recurrent post-obstructive pneumonia. Procedure: Flexible bronchoscopy with mechanical debulking/excision of RLL bronchus lesion (CPT 31640). Findings: Polypoid lesion at superior segment RLL bronchus with ~70% obstruction. Interventions: Snare resection and forceps debulking used to mechanically remove the lesion. No thermal ablation or balloon dilation.",
            7: "[Indication]\nRLL lesion, recurrent pneumonia.\n[Anesthesia]\nModerate sedation, LMA.\n[Description]\nPolypoid lesion RLL superior segment. Snare resection and forceps debulking performed. No thermal ablation.\n[Plan]\nDischarge. Follow-up CT.",
            8: "Mr. Allen had a growth in his right lower lung causing infections. We did a flexible bronchoscopy to remove it. We found a polyp-like growth blocking the airway. We used a wire snare to loop around it and cut it off, and forceps to remove the pieces. It was a purely mechanical removal without burning. He barely bled and is going home.",
            9: "Procedure: Flexible bronchoscopy with mechanical extirpation of RLL growth.\nFindings: Polypoid mass causing 70% occlusion.\nAction: We utilized snare resection and forceps to excise the lesion. No thermal tools were applied.\nOutcome: Minimal hemostasis required."
        },
        6: { # Sofia Delgado (Carinal/LMS Tumor)
            1: "Proc: Rigid Bronch, mechanical debulking Carina/LMS.\nIndication: Mixed obstruction (Cancer).\nFindings: 80% obstruction left carina/LMS.\nAction: Rigid coring + forceps excision. No thermal.\nResult: 40ml EBL. Hemostasis achieved.\nPlan: Step-down unit.",
            2: "OPERATIVE REPORT: CARINAL TUMOR RESECTION\n\nINDICATION: Ms. Delgado presented with a complex malignant obstruction involving the carina and left mainstem bronchus.\n\nPROCEDURE: Rigid bronchoscopy was undertaken. A tumor was visualized projecting from the left aspect of the carina, occluding the left mainstem by 80%. Mechanical debulking was performed using the rigid bronchoscope for coring and heavy forceps for tissue extraction. The airway was restored. Hemostasis was managed with topical epinephrine.",
            3: "Code: 31640.\nLocation: Carina / Left Mainstem.\nProcedure: Mechanical excision of tumor.\nDevice: Rigid Bronchoscope (Coring), Forceps.\nRationale: Mechanical removal of obstructing tissue. No thermal ablation codes utilized.",
            4: "Procedure: Rigid Bronch / Debulking\nPt: Sofia Delgado\n\n1. GA, Rigid scope.\n2. Tumor at carina going into LMS.\n3. Used rigid tube to core it out.\n4. Forceps to remove tissue.\n5. 80% blockage reduced.\n6. Epi for bleeding.\n\nAdmit to step-down.",
            5: "Sofia Delgado 50F rigid bronch for carinal tumor. It was blocking the left side about 80 percent. We used the rigid scope to core through it and forceps to clear the airway. Did not use any laser. Bleeding was controlled with epi and saline. She is extubated and going to step down.",
            6: "INTERVENTIONAL PULMONOLOGY - RIGID BRONCHOSCOPY WITH MECHANICAL DEBULKING. Indication: Mixed carinal and left mainstem obstruction from endobronchial lung cancer. Procedure: Rigid bronchoscopy with mechanical debulking of carinal/LMS tumor (CPT 31640). Findings: Tumor projecting from left side of carina into LMS with ~80% obstruction. Interventions: Rigid coring and forceps debulking to mechanically debulk tumor at carina and LMS. No thermal ablation.",
            7: "[Indication]\nCarinal/LMS obstruction, lung cancer.\n[Anesthesia]\nGeneral, Rigid bronchoscopy.\n[Description]\n80% obstruction. Rigid coring and forceps debulking performed. No thermal ablation.\n[Plan]\nStep-down unit.",
            8: "Ms. Delgado had a tumor sitting right at the fork of her windpipe, blocking the left side. We used a rigid bronchoscope to mechanically remove it. We cored out the tumor and used forceps to grab the tissue. We successfully opened the airway without using heat or lasers. We controlled the bleeding and she is going to the step-down unit.",
            9: "Procedure: Rigid endoscopy with mechanical resection of carinal mass.\nFindings: 80% occlusion of LMS/Carina.\nAction: We utilized rigid coring and forceps to excise the malignancy. No thermal ablation was performed.\nStatus: Hemostasis secured."
        },
        7: { # Henry Thompson (Tracheal Stenosis/Granulation)
            1: "Proc: Flex Bronch, mechanical debulking.\nIndication: Post-intubation stenosis.\nFindings: Granulation ring distal trachea, 70% narrowing.\nAction: Forceps + snare removal. No balloon.\nResult: 5ml EBL.\nPlan: Home, f/u 2 months.",
            2: "PROCEDURE NOTE: TRACHEAL DEBRIDEMENT\n\nINDICATION: Mr. Thompson presented with dyspnea secondary to post-intubation tracheal stenosis.\n\nFINDINGS: A circumferential ring of granulation tissue was identified in the distal trachea, compromising the lumen by 60-70%.\n\nPROCEDURE: Flexible bronchoscopy was utilized. Mechanical excision of the granulation tissue was performed using biopsy forceps and snare resection. This successfully widened the airway. No balloon dilation or thermal ablation was employed during this session.",
            3: "CPT: 31640.\nPathology: Granulation tissue (Benign).\nLocation: Distal Trachea.\nMethod: Mechanical excision (Forceps/Snare).\nNote: Procedure focus was excision of tissue causing stenosis, not dilation (31630 not used) or ablation (31641 not used).",
            4: "Procedure: Flex Bronch / Granulation removal\nPt: Henry Thompson\n\n1. Sedation.\n2. Scope to distal trachea.\n3. Saw granulation ring (scar).\n4. Used forceps and snare to cut it out.\n5. Airway looks much better.\n6. No bleeding.\n\nDischarge.",
            5: "Henry Thompson here for that tracheal scar. He had a tube before. We looked and saw granulation tissue narrowing the trachea. We used the forceps and a snare to mechanically remove the tissue. Didnt use a balloon or laser. Bleeding was tiny. He is going home.",
            6: "BRONCHOSCOPY PROCEDURE NOTE - MECHANICAL DEBULKING. Indication: Post-intubation tracheal stenosis with progressive dyspnea. Procedure: Flexible bronchoscopy with mechanical debulking of granulation tissue (CPT 31640). Findings: Short circumferential granulation ring in distal trachea causing 60-70% narrowing. Interventions: Forceps debulking and snare resection used to mechanically excise granulation tissue. No balloon or ablation.",
            7: "[Indication]\nPost-intubation tracheal stenosis.\n[Anesthesia]\nModerate sedation.\n[Description]\nGranulation ring distal trachea. Forceps debulking and snare resection performed. No balloon/ablation.\n[Plan]\nDischarge. F/u 2-3 months.",
            8: "Mr. Thompson developed scar tissue in his windpipe from a previous breathing tube. We went in with a flexible scope and found a ring of granulation tissue blocking the way. We used forceps and a snare to mechanically cut this tissue out. We didn't use a balloon or heat. The airway is much more open now.",
            9: "Procedure: Flexible bronchoscopy with mechanical excision of granulation.\nFindings: Tracheal narrowing (60-70%).\nAction: We employed forceps and snare to extirpate the tissue. No dilation or ablation was utilized.\nOutcome: Minimal blood loss."
        },
        8: { # David Price (LMS Tumor/Microdebrider)
            1: "Proc: Rigid Bronch, mechanical debulking LMS.\nIndication: LMS tumor, pneumonia.\nFindings: Friable mass, 85% obstruction.\nAction: Rigid coring, forceps, microdebrider. No thermal.\nResult: 60ml EBL.\nPlan: Ward.",
            2: "OPERATIVE REPORT: LEFT MAINSTEM RECANALIZATION\n\nINDICATION: Mr. Price presented with recurrent pneumonia due to a malignant left mainstem (LMS) obstruction.\n\nPROCEDURE: General anesthesia was induced and the rigid bronchoscope inserted. The LMS was obstructed 85% by a friable tumor mass. Mechanical debulking was performed using the bevel of the rigid scope for coring, followed by forceps extraction. A microdebrider was employed to shave residual tumor and optimize luminal diameter. No thermal ablation was utilized. Hemostasis was achieved.",
            3: "Code: 31640.\nTools: Rigid Scope (Coring), Forceps, Microdebrider.\nTechnique: Mechanical excision.\nSite: Left Mainstem Bronchus.\nRationale: Documentation supports mechanical removal of tumor using multiple instruments including microdebrider. No thermal codes applicable.",
            4: "Procedure: Rigid Bronch / Microdebrider\nPt: David Price\n\n1. GA / Rigid scope.\n2. LMS 85% blocked by tumor.\n3. Used scope to core.\n4. Used forceps to grab.\n5. Used microdebrider to clean it up.\n6. Epi for bleeding.\n\nExtubated.",
            5: "David Price 63M LMS tumor. Rigid bronch today. It was blocking like 85 percent. We cored it out and used forceps. Also used the microdebrider tool to get it really clean. No burning used. Bleeding was moderate about 60cc. He is going to the floor.",
            6: "INTERVENTIONAL PULMONOLOGY - RIGID BRONCHOSCOPY WITH MECHANICAL DEBULKING. Indication: Left mainstem endobronchial tumor with recurrent post-obstructive pneumonia and weight loss. Procedure: Rigid bronchoscopy with mechanical debulking/excision of left mainstem tumor (CPT 31640). Findings: Friable LMS mass causing 80-85% obstruction. Interventions: Rigid coring, forceps debulking, and microdebrider used for mechanical debulking and excision. No thermal methods.",
            7: "[Indication]\nLMS tumor, recurrent pneumonia.\n[Anesthesia]\nGeneral, Rigid bronchoscopy.\n[Description]\n85% obstruction. Rigid coring, forceps, microdebrider used. Mechanical excision. No thermal ablation.\n[Plan]\nOncology ward.",
            8: "Mr. Price had a tumor blocking his left main airway causing pneumonia. We performed a rigid bronchoscopy to clear it. We used the rigid tube to core the tumor, forceps to pull it out, and a microdebrider to shave away the rest. We did this all mechanically without heat. He lost about 60ml of blood but we controlled it.",
            9: "Procedure: Rigid endoscopy with mechanical resection of LMS tumor.\nFindings: Friable mass (85% occlusion).\nAction: We utilized rigid coring, forceps, and a microdebrider to excise the lesion. No thermal tools were applied.\nStatus: Moderate hemostasis required."
        },
        9: { # Chloe Bennett (Mid Tracheal Tumor)
            1: "Proc: Rigid Bronch, mechanical debulking Trachea.\nIndication: Stridor, tracheal tumor.\nFindings: 75% narrowing mid-trachea.\nAction: Rigid coring, forceps, snare. No laser.\nResult: 20ml EBL.\nPlan: Step-down unit.",
            2: "PROCEDURE NOTE: TRACHEAL TUMOR EXCISION\n\nINDICATION: Ms. Bennett presented with stridor and a known proximal/mid tracheal malignancy.\n\nPROCEDURE: The rigid bronchoscope was introduced under general anesthesia. Inspection confirmed a tumor narrowing the mid-trachea by 75%. Mechanical excision was prioritized. The rigid scope was used for coring, followed by forceps debulking. A pedunculated component was excised via snare. No thermal ablation was required to achieve airway patency.",
            3: "Billing: 31640.\nAnatomy: Mid-trachea.\nTechnique: Mechanical excision (Rigid coring, Forceps, Snare).\nDiagnosis: Malignant tracheal tumor.\nNote: Mechanical tools only; no thermal ablation used.",
            4: "Procedure: Rigid Bronch Trachea\nPt: Chloe Bennett\n\n1. GA.\n2. Scope to mid trachea.\n3. 75% blockage.\n4. Cored with scope, pulled with forceps.\n5. Used snare for one piece.\n6. Saline wash.\n\nAirway open.",
            5: "Chloe Bennett 48F. Tracheal tumor causing stridor. We took her to the OR for rigid bronch. Tumor was blocking 75 percent. We used the rigid coring technique and forceps. Also a snare for the hanging part. No laser used. Bleeding minimal. She is going to step down.",
            6: "BRONCHOSCOPY PROCEDURE NOTE - MECHANICAL DEBULKING IN PATIENT WITH MALIGNANT TRACHEAL TUMOR. Indication: Proximal/mid tracheal tumor with progressive stridor and exertional dyspnea. Procedure: Rigid bronchoscopy with mechanical debulking/excision of tracheal tumor (CPT 31640). Findings: Tumor involving anterior and lateral walls of mid trachea, causing ~75% narrowing. Interventions: Rigid coring and forceps debulking used to mechanically debulk and excise tumor tissue. Snare resection of a pedunculated component. No thermal ablation.",
            7: "[Indication]\nTracheal tumor, stridor.\n[Anesthesia]\nGeneral, Rigid bronchoscopy.\n[Description]\n75% mid-tracheal narrowing. Rigid coring, forceps, snare used. Mechanical excision. No thermal ablation.\n[Plan]\nStep-down unit monitoring.",
            8: "Ms. Bennett was having noisy breathing due to a tumor in her windpipe. We used a rigid bronchoscope to remove it. We cored the tumor with the scope, grabbed the tissue with forceps, and used a snare to cut off a hanging piece. We cleared the airway significantly without needing to use lasers.",
            9: "Procedure: Rigid endoscopy with mechanical extirpation of tracheal lesion.\nFindings: 75% narrowing.\nAction: We employed rigid coring, forceps, and snare to excise the malignancy. No thermal tools were utilized.\nOutcome: Minimal blood loss."
        }
    }
    return variations

def get_base_data_mocks():
    return [
        {"idx": 0, "orig_name": "Jasmine Young", "orig_age": 39, "names": ["Alice Brown", "Betty Davis", "Carol Evans", "Diana Foster", "Evelyn Green", "Fiona Harris", "Gina Irving", "Hannah Jones", "Iris King"]},
        {"idx": 1, "orig_name": "Kevin Brooks", "orig_age": 55, "names": ["Jack Lewis", "Karl Miller", "Liam Nelson", "Mike Owens", "Noah Parker", "Oscar Quinn", "Peter Ross", "Quinn Scott", "Ryan Turner"]},
        {"idx": 2, "orig_name": "Jonas Meyer", "orig_age": 66, "names": ["Sam Underwood", "Tom Vance", "Victor White", "Will Xavier", "Xander Young", "Yusuf Zane", "Adam Allen", "Ben Baker", "Chris Clark"]},
        {"idx": 3, "orig_name": "Natalie Ortiz", "orig_age": 62, "names": ["Debra Davis", "Elena Edwards", "Faye Franklin", "Gloria Garcia", "Helen Hill", "Irene Ingram", "Judy Johnson", "Kathy Kelly", "Laura Lee"]},
        {"idx": 4, "orig_name": "Olivia Martin", "orig_age": 64, "names": ["Mary Moore", "Nancy Nelson", "Olive Olson", "Penny Peterson", "Queen Roberts", "Rachel Smith", "Sarah Thomas", "Tina Urich", "Uma Victor"]},
        {"idx": 5, "orig_name": "Marcus Allen", "orig_age": 58, "names": ["Frank Walker", "George Young", "Harry Zane", "Ian Adams", "John Brown", "Kyle Carter", "Leo Davis", "Mark Evans", "Ned Foster"]},
        {"idx": 6, "orig_name": "Sofia Delgado", "orig_age": 50, "names": ["Anna Garcia", "Bella Hernandez", "Carla Ibarra", "Donna Jones", "Eva Kelly", "Fran Lopez", "Gia Martinez", "Holly Nunez", "Ivy Ortiz"]},
        {"idx": 7, "orig_name": "Henry Thompson", "orig_age": 72, "names": ["Paul Perez", "Quentin Quinn", "Ralph Ramirez", "Steve Sanchez", "Ted Torres", "Ulysses Underwood", "Vince Vargas", "Walt Wilson", "Xavier Xu"]},
        {"idx": 8, "orig_name": "David Price", "orig_age": 63, "names": ["Yanni Young", "Zack Zimmerman", "Arthur Anderson", "Bill Bailey", "Charles Campbell", "David Douglas", "Edward Edwards", "Fred Fisher", "Greg Gray"]},
        {"idx": 9, "orig_name": "Chloe Bennett", "orig_age": 48, "names": ["Jenny Hall", "Kelly Hill", "Linda Irwin", "Mona Jenkins", "Nina King", "Opal Lee", "Patty Moore", "Qiana Nelson", "Rita Owens"]}
    ]

def main():
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return

    if not isinstance(source_data, list):
        print("Error: Source data must be a list of JSON objects.")
        return

    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")

    variations_map = get_variations()
    base_mocks = get_base_data_mocks()
    
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_notes = []

    for idx, original_note in enumerate(source_data):
        if idx >= len(base_mocks):
            break
            
        mock_data = base_mocks[idx]
        orig_age = mock_data['orig_age']
        
        # We need 9 variations per note
        for style_num in range(1, 10):
            new_note = copy.deepcopy(original_note)
            
            # 1. Update Note Text
            if idx in variations_map and style_num in variations_map[idx]:
                new_note["note_text"] = variations_map[idx][style_num]
            
            # 2. Update Demographics in Registry Entry
            if "registry_entry" in new_note:
                # Randomize Age (+/- 3 years)
                new_age = orig_age + random.randint(-3, 3)
                new_note["registry_entry"]["patient_age"] = new_age
                
                # Update Name (using mock list)
                new_name = mock_data['names'][style_num - 1]
                # Note: The registry_entry doesn't strictly have a 'patient_name' field in the schema provided, 
                # but the note_text does. We updated note_text above. 
                # If we need to update a name field inside registry_entry (if it existed), we would do it here.
                
                # Randomize Date (Year 2025)
                rand_date = generate_random_date(2025, 2025)
                new_note["registry_entry"]["procedure_date"] = rand_date.strftime("%Y-%m-%d")
                
                # Update MRN to ensure uniqueness
                orig_mrn = new_note["registry_entry"].get("patient_mrn", "UNKNOWN")
                new_note["registry_entry"]["patient_mrn"] = f"{orig_mrn}-V{style_num}"

            # 3. Add Metadata
            new_note["synthetic_metadata"] = {
                "original_index": idx,
                "style_type": style_num,
                "variation_generated_at": datetime.datetime.now().isoformat(),
                "patient_name_used": mock_data['names'][style_num - 1]
            }
            
            generated_notes.append(new_note)

    output_file = output_dir / "synthetic_mechanical_debulking_part_062.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2)
        
    print(f"Successfully generated {len(generated_notes)} synthetic notes.")

if __name__ == "__main__":
    main()