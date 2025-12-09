import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_009.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Michael Brown (EBUS 4R, 7, 10R, 11R)
            1: "Proc: EBUS-TBNA.\nIndication: Staging RUL mass.\nNodes Sampled: 4R, 7, 10R, 11R.\nFindings:\n- 4R/7: Adenocarcinoma.\n- 10R: Reactive.\n- 11R: Benign.\nPlan: Oncology.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the bronchoscopy suite for endobronchial ultrasound-guided transbronchial needle aspiration (EBUS-TBNA) for mediastinal staging of a right upper lobe neoplasm. Under deep sedation, the EBUS bronchoscope was introduced. Systematic sonographic evaluation of the mediastinum was performed. Nodal stations 4R, 7, 10R, and 11R were visualized and sampled sequentially. Rapid On-Site Evaluation (ROSE) demonstrated adenocarcinoma in stations 4R and 7, confirming N2 disease. Stations 10R and 11R yielded benign lymphocytes. The procedure was concluded without complication.",
            3: "Procedure: Bronchoscopy with EBUS sampling (CPT 31653).\nTechnique: Real-time ultrasonic guidance utilized for needle aspiration of four (4) distinct mediastinal and hilar nodal stations.\nStations Sampled:\n1. Station 4R (Right Paratracheal)\n2. Station 7 (Subcarinal)\n3. Station 10R (Right Hilar)\n4. Station 11R (Right Interlobar)\nPathology: Malignancy confirmed in 4R and 7.\nJustification: Sampling of 3+ stations supports 31653.",
            4: "Resident Note\nPt: Michael Brown\nProc: EBUS-TBNA\nStaff: Dr. White\nSteps:\n1. Time out.\n2. Scope inserted.\n3. EBUS landmarks identified.\n4. Biopsied 4R (positive), 7 (positive), 10R (neg), 11R (neg).\n5. ROSE confirmed adenocarcinoma in mediastinum.\nPlan: Consult Onc.",
            5: "Michael Brown here for ebus staging. we looked at the nodes 4R 7 10R and 11R. used the 22 gauge needle for all of them. rose guy said 4r and 7 were cancer adenocaricnoma. 10r and 11r looked fine just reactive. no bleeding patient tol well. n2 disease confirmed sent to recovery.",
            6: "EBUS-TBNA performed for staging of RUL mass. 65-year-old male. Under MAC anesthesia, EBUS scope inserted. Station 4R sampled x4 passes, ROSE positive for adenocarcinoma. Station 7 sampled x4 passes, ROSE positive for malignancy. Station 10R sampled x2 passes, ROSE reactive. Station 11R sampled x2 passes, ROSE benign. N2 disease confirmed. No complications. EBL < 5ml.",
            7: "[Indication]\nLung mass RUL, mediastinal adenopathy, staging.\n[Anesthesia]\nMAC, local lidocaine.\n[Description]\nEBUS scope introduced. Survey performed. Sampled stations: 4R, 7, 10R, 11R. ROSE confirmed malignancy (adenocarcinoma) in stations 4R and 7. Stations 10R and 11R were benign.\n[Plan]\nOncology referral for N2 disease.",
            8: "The patient underwent an EBUS-TBNA for staging of a right upper lobe mass. We systematically evaluated the mediastinum and proceeded to sample lymph nodes at stations 4R, 7, 10R, and 11R utilizing a 22-gauge needle. On-site cytopathology evaluation was positive for adenocarcinoma in the subcarinal (7) and right paratracheal (4R) stations, confirming N2 involvement. The hilar and interlobar nodes were benign. The patient tolerated the procedure well.",
            9: "Procedure: Endobronchial ultrasound with transbronchial needle aspiration.\nAction: The bronchoscope was advanced. We scanned the mediastinum. We sampled stations 4R, 7, 10R, and 11R. \nResult: ROSE verified adenocarcinoma in stations 4R and 7. Stations 10R and 11R contained benign cells.\nOutcome: N2 disease established."
        },
        1: { # Kenji Nakamura (EBUS 5, 7, 10L + EMN LUL Mass)
            1: "Procedures: EBUS + EMN Bronchoscopy.\nEBUS: Stations 5, 7, 10L sampled. All positive for malignancy (NSCLC).\nEMN: Navigated to LUL mass (4.2cm). Radial EBUS eccentric view. \nBiopsy: TBBx x9, brush, needle.\nDx: Stage IIIB Squamous Cell Ca (T3N3?)\nPlan: Chemo/Rad.",
            2: "OPERATIVE REPORT: The patient presented for combined EBUS staging and electromagnetic navigation bronchoscopy of a large LUL mass. \nEBUS PHASE: Stations 5, 7, and 10L were interrogated and sampled via TBNA. Cytology confirmed malignancy in all sampled stations.\nNAVIGATION PHASE: Using the SuperDimension system, the LUL mass was targeted. Radial EBUS confirmed lesion location (eccentric). Transbronchial biopsies, brushing, and needle aspiration were performed. Histology suggests squamous cell carcinoma.",
            3: "Coding Data:\n- 31653: EBUS sampling 3+ stations (5, 7, 10L).\n- 31628: Transbronchial lung biopsy, single lobe (LUL mass).\n- 31627: Navigation add-on (EMN used).\n- 31654: Peripheral EBUS add-on (Radial probe).\nMedical Necessity: Staging and diagnosis of 4.2cm LUL lesion with adenopathy.",
            4: "Procedure Note\nPatient: Kenji N.\nProc: EBUS/Nav.\nSteps:\n1. EBUS scope in. Sampled 5, 7, 10L. All positive for cancer.\n2. Switch to therapeutic scope.\n3. Registered EMN.\n4. Navigated to LUL mass.\n5. Radial probe: eccentric view.\n6. Took biopsies (forceps, brush, needle).\n7. Endobronchial biopsy of anterior segment also done.",
            5: "Combined case today ebus and nav. Patient has big LUL mass. Ebus first we hit stations 5 and 7 and 10L. Rose said all positive for squamous i think. Then switched scopes did the navigation to the mass. Got a signal on radial probe eccentric. Biopsied it good. Also saw some tumor in the airway and grabbed that too. No bleeding pt stable.",
            6: "Combined EBUS and EMN bronchoscopy. Indication: 4.2cm LUL mass and adenopathy. EBUS performed first; stations 5, 7, and 10L sampled and confirmed malignant (NSCLC). Therapeutic scope inserted for EMN. Successfully navigated to LUL posterior segment target. Radial EBUS showed lesion. Transbronchial biopsy, needle aspiration, and brushings obtained. Additional endobronchial biopsy taken from anterior segment. Diagnosis: Stage IIIB Squamous Cell Carcinoma.",
            7: "[Indication]\nLUL mass 4.2cm, mediastinal adenopathy.\n[Anesthesia]\nModerate-deep sedation (Propofol).\n[Description]\n1. EBUS: Sampled 5, 7, 10L. All positive for malignancy.\n2. EMN: Navigated to LUL mass. Confirmed with Radial EBUS. Biopsies taken.\n3. Endobronchial biopsy: Anterior segment lesion sampled.\n[Plan]\nRefer to Onc for Stage IIIB disease.",
            8: "Mr. Nakamura underwent a complex staging procedure today. We began with EBUS to stage the mediastinum, sampling stations 5, 7, and 10L. Unfortunately, all stations were positive for malignancy. We then switched to electromagnetic navigation to biopsy the primary 4.2cm mass in the left upper lobe. We utilized radial EBUS to confirm the location and obtained diagnostic tissue via forceps and needle. We also noted and biopsied an endobronchial component. The preliminary diagnosis is squamous cell carcinoma.",
            9: "Procedure: EBUS-TBNA and Electromagnetic Navigation Bronchoscopy.\nAction: We aspirated lymph node stations 5, 7, and 10L; all yielded malignant cells. We then navigated to the LUL tumor using electromagnetic guidance. Radial ultrasound located the lesion. We harvested tissue using forceps, brushes, and needles.\nDiagnosis: Advanced stage Squamous Cell Carcinoma."
        },
        2: { # Jessica McBee (Rigid, Esophageal stent removal, Y-stent)
            1: "Indication: TE Fistula / Airway obstruction from migrated esophageal stent.\nProc: Rigid Bronch, FB Removal, Stent Placement.\nActions:\n- Rigid scope inserted.\n- Migrated esophageal stent/clips removed piecemeal.\n- Large TEF exposed.\n- Y-Stent (Silicone) placed to cover defect.\nResult: Airway patent. ETT placed through stent.",
            2: "OPERATIVE SUMMARY: This 65-year-old female presented with airway obstruction secondary to a migrated esophageal stent. Rigid bronchoscopy was performed. The esophageal stent was found protruding into the distal trachea and left mainstem. The foreign body was extracted in a piecemeal fashion using rigid forceps and APC. Removal revealed a significant tracheoesophageal fistula involving the posterior tracheal wall. To palliate the airway and seal the fistula, a silicone Y-stent was deployed. Difficulties were encountered seating the stent due to the carinal defect, but final positioning was satisfactory.",
            3: "CPT Coding:\n- 31635: Removal of foreign body (esophageal stent/clips).\n- 31636: Stent placement, initial bronchus (Trachea/Left Main).\n- 31637: Stent placement, additional bronchus (Right Main limb of Y-stent).\nTechnique: Rigid bronchoscopy required for stent extraction and silicone stent deployment.",
            4: "Procedure: Rigid Bronch / Stent / FB Removal\nPatient: Jessica McBee\nSteps:\n1. GA, LMA.\n2. Flex scope: saw esophageal stent in trachea.\n3. Switched to Rigid 14mm.\n4. Removed stent pieces (hard to get out).\n5. Saw huge TE fistula.\n6. Placed Y-stent to cover hole.\n7. ETT placed through stent.",
            5: "Tough case. Patient had an esophageal stent that eroded into the airway blocking the left side. We went in with the rigid scope. Had to cut the stent up and pull it out piece by piece really stuck in there. Once it was out there was a giant hole between trachea and esophagus. We put a silicone Y stent in to cover it up. Took a few tries to get it seated right but looks okay now. Left intubated.",
            6: "Rigid bronchoscopy with esophageal stent removal and dynamic Y-stent placement. Indication: Left mainstem obstruction from stent migration and TE fistula. The esophageal stent was protruding into the trachea and LMB. Using rigid forceps, APC, and scissors, the stent was removed piecemeal. A large TEF was noted at the carina/posterior trachea. A silicone Y-stent was deployed to stent the airway and cover the fistula. Patient remained intubated through the stent.",
            7: "[Indication]\nAirway obstruction, migrated esophageal stent, TE fistula.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nRigid bronchoscopy performed. Migrated esophageal stent removed from trachea/LMB using forceps/APC. Resultant large TEF visualized. Silicone Y-stent deployed to patency and seal fistula. ETT placed through stent.\n[Plan]\nICU, keep intubated, saline nebs.",
            8: "Ms. McBee underwent rigid bronchoscopy to manage a migrated esophageal stent that was obstructing her airway. We successfully removed the stent and clips, though it required piecemeal extraction due to tissue embedding. This revealed a large tracheoesophageal fistula. To manage this, we placed a silicone Y-stent, securing the airway and covering the defect. The patient was left intubated to ensure stent stability.",
            9: "Procedure: Rigid bronchoscopy with extraction of foreign body and implantation of airway stent.\nFindings: Esophageal prosthesis invading distal trachea and left mainstem.\nAction: The prosthesis was fragmented and retrieved. A massive TE fistula was exposed. A silicone Y-stent was inserted to bridge the defect.\nOutcome: Airway restored, fistula covered."
        },
        3: { # Unknown/Turner (EBUS 7, 4R, 10R, 11R)
            1: "Proc: EBUS-TBNA.\nNodes: 4R, 7, 10R, 11R.\nResults:\n- 7 (Subcarinal): Positive (Adeno).\n- 4R: Positive.\n- 10R: Positive.\n- 11R: Negative.\nStage: N3 Disease (contralateral/bilateral involvement implied by text/code logic in source context).",
            2: "PROCEDURE NOTE: Endobronchial ultrasound-guided TBNA. The mediastinum was mapped. Station 7 (subcarinal) was sampled x4, revealing adenocarcinoma. Station 4R and 10R were also sampled and found positive for malignancy. Station 11R was sampled and was benign. The presence of multi-station disease confirms advanced staging.",
            3: "Billing: 31653 (EBUS sampling 3+ stations).\nSpecifics:\n- Station 7: 4 passes, Adenocarcinoma.\n- Station 4R: 3 passes, Adenocarcinoma.\n- Station 10R: 2 passes, Malignant.\n- Station 11R: 2 passes, Benign.\nTotal 4 stations sampled.",
            4: "Resident Note\nProc: EBUS\nStations: 7, 4R, 10R, 11R.\nRose results:\n- 7: Positive\n- 4R: Positive\n- 10R: Positive\n- 11R: Negative\nDx: Lung CA with N2/N3 nodes.",
            5: "We did the EBUS today. Hit the subcarinal 7 and the 4R and 10R and 11R. The cyto tech said 7 and 4R and 10R were all cancer adeno. 11R was okay. No issues patient woke up fine.",
            6: "EBUS-TBNA performed. Stations sampled: 7, 4R, 10R, 11R. ROSE evaluation: Station 7 positive for adenocarcinoma. Station 4R positive for adenocarcinoma. Station 10R positive for malignancy. Station 11R negative/benign. Procedure time 48 mins. No complications.",
            7: "[Indication]\nStaging lung cancer.\n[Anesthesia]\nModerate/MAC.\n[Description]\nEBUS TBNA performed. Sampled Stations: 7, 4R, 10R, 11R. ROSE Results: 7(+), 4R(+), 10R(+), 11R(-).\n[Plan]\nOncology consult for advanced stage disease.",
            8: "The patient underwent EBUS-TBNA for staging. We sampled lymph nodes in station 7, 4R, 10R, and 11R. Preliminary on-site evaluation showed adenocarcinoma in stations 7, 4R, and 10R. Station 11R appeared benign. This pattern of spread indicates advanced nodal disease.",
            9: "Procedure: EBUS-TBNA.\nAction: Sampled nodal stations 7, 4R, 10R, 11R.\nFindings: Malignant cells detected in stations 7, 4R, and 10R. Benign lymphocytes in 11R.\nDiagnosis: Adenocarcinoma with extensive nodal metastasis."
        },
        4: { # Unknown/Montgomery (EBUS 7, 4L, 4R, 10L, 10R, 11L)
            1: "Proc: EBUS-TBNA (6 Stations).\nSampled: 7, 4L, 4R, 10L, 10R, 11L.\nROSE:\n- Positive: 7, 4L, 4R, 10L, 11L.\n- Negative: 10R.\nDx: Adenocarcinoma, Stage IIIC (N3).",
            2: "OPERATIVE REPORT: Extensive EBUS staging was performed. The following stations were aspirated: Subcarinal (7), Left Lower Paratracheal (4L), Right Lower Paratracheal (4R), Left Hilar (10L), Right Hilar (10R), and Left Interlobar (11L). ROSE confirmed adenocarcinoma in stations 7, 4L, 4R, 10L, and 11L. Station 10R was benign. This confirms N3 disease (contralateral mediastinal involvement).",
            3: "Code: 31653 (EBUS sampling 3+ stations).\nWork performed: Sampling of 6 distinct nodal stations (7, 4L, 4R, 10L, 10R, 11L). \nPathology: Widespread metastasis (Adenocarcinoma) found in 5 of 6 stations.\nComplexity: High, bilateral mediastinal sampling.",
            4: "Resident Note\nProc: EBUS\nStations: 7, 4L, 4R, 10L, 10R, 11L.\nResults: Cancer everywhere basically. 7, 4L, 4R, 10L, 11L all positive. Only 10R was neg.\nPlan: Not surgical. Chemo/rads.",
            5: "Big staging case. We sampled 6 nodes total. 7 4L 4R 10L 10R 11L. Rose said positive for adeno in almost all of them 7 4L 4R 10L 11L. 10R was the only clean one. Stage IIIC definitely.",
            6: "EBUS-TBNA with sampling of 6 stations: 7, 4L, 4R, 10L, 10R, 11L. ROSE confirmed adenocarcinoma in stations 7, 4L, 4R, 10L, and 11L. Station 10R was negative. Diagnosis: Stage IIIC Adenocarcinoma (N3 disease). No complications.",
            7: "[Indication]\nLung mass, bilateral adenopathy.\n[Anesthesia]\nModerate.\n[Description]\nEBUS TBNA of 6 stations. Positive: 7, 4L, 4R, 10L, 11L. Negative: 10R. Confirmed N3 disease.\n[Plan]\nMed Onc, Rad Onc, Palliative care.",
            8: "We performed a comprehensive EBUS staging procedure, sampling six lymph node stations: 7, 4L, 4R, 10L, 10R, and 11L. Rapid on-site evaluation showed malignant adenocarcinoma cells in all stations except 10R. This finding of bilateral mediastinal disease (N3) places the patient in Stage IIIC, precluding surgical resection.",
            9: "Procedure: EBUS-TBNA.\nAction: Aspirated stations 7, 4L, 4R, 10L, 10R, 11L.\nResult: Malignancy detected in 7, 4L, 4R, 10L, and 11L. Station 10R showed reactive tissue.\nConclusion: Extensive N3 nodal metastasis."
        },
        5: { # Robert Chen (BLVR RUL 3 valves)
            1: "Indication: RUL Emphysema.\nProc: Bronchoscopy with Valve Placement.\nAction:\n- Chartis: RUL CV Negative.\n- Placed 3 Zephyr valves: RB1, RB2, RB3.\n- Occlusion confirmed.\nResult: Good lobar seal. No PTX.",
            2: "PROCEDURE NOTE: The patient presented for RUL lung volume reduction. Airway inspection revealed severe emphysematous changes. Chartis assessment of the RUL confirmed the absence of collateral ventilation. Consequently, three Zephyr endobronchial valves were deployed into the RB1, RB2, and RB3 segmental bronchi. Complete lobar occlusion was achieved visually and fluoroscopically.",
            3: "CPT: 31647 (Valve placement initial lobe).\nLobe: Right Upper Lobe.\nValves: 3 Zephyr valves (4.0mm, 4.0mm, 5.5mm).\nAssessment: Chartis confirmed fissure integrity.\nOutcome: Successful deployment and occlusion.",
            4: "Resident Note\nPt: Robert Chen\nProc: RUL BLVR\nSteps:\n1. Chartis check RUL: Neg CV.\n2. Sized airways.\n3. Placed 3 valves (RB1, RB2, RB3).\n4. Checked for leaks - none.\nPlan: CXR, admit.",
            5: "Robert Chen here for valves. We did the RUL. Chartis looked good no flow. Put in three valves total one for each segment. RB1 RB2 RB3. Used the zephyrs. Everything looks sealed up tight. No pneumo on the table.",
            6: "Bronchoscopic Lung Volume Reduction (RUL). Indication: Severe Emphysema. Chartis assessment: CV Negative. Three Zephyr valves deployed in RUL segmental bronchi (RB1, RB2, RB3). Complete occlusion achieved. No complications.",
            7: "[Indication]\nSevere RUL emphysema.\n[Anesthesia]\nModerate Sedation.\n[Description]\nRUL selected. Chartis: No CV. 3 Zephyr valves deployed (RB1, RB2, RB3). Good seal.\n[Plan]\nOvernight observation.",
            8: "Mr. Chen underwent bronchoscopic lung volume reduction targeting the right upper lobe. After confirming the absence of collateral ventilation with the Chartis system, we placed three Zephyr valves in the RB1, RB2, and RB3 bronchi. We verified complete occlusion of the lobe. The patient tolerated the procedure well.",
            9: "Procedure: BLVR with valve implantation.\nTarget: Right Upper Lobe.\nAction: Chartis confirmed eligibility. Three Zephyr valves were implanted in the segmental bronchi.\nResult: The lobe was successfully occluded."
        },
        6: { # Ava Harrington (Stenosis 31641)
            1: "Dx: GPA Tracheal/Bronchial Stenosis.\nProc: Rigid Bronch, Radial Knife, Balloon Dilation.\nActions:\n- 12mm Rigid scope.\n- Radial knife incisions to strictures (trachea, RLL, LUL).\n- Balloon dilation (CRE 12-15mm trachea, 6-8mm bronchi).\nResult: Airways recanalized. Good patency.",
            2: "OPERATIVE REPORT: Patient with Wegener's granulomatosis (GPA) and multilevel airway stenosis. Rigid bronchoscopy was utilized. Significant circumferential stenosis was noted in the subglottic trachea and multiple segmental bronchi (RLL, LUL). Treatment consisted of radial incisions using an electrocautery knife followed by serial balloon dilation using CRE balloons. This resulted in significant improvement in airway caliber and patency.",
            3: "Codes: 31641 (Therapeutic bronchoscopy for stenosis).\nTechnique: Complex management of multilevel stenosis using two modalities: electrocautery incision (radial knife) and balloon dilation.\nSites: Trachea, RLL segments, LUL lingula.\nOutcome: Restoration of airway patency.",
            4: "Procedure: Stenosis Dilation\nPt: Ava Harrington\nSteps:\n1. Rigid bronch.\n2. Saw tight stenosis in trachea and lower lobes.\n3. Used the radial knife to cut the scar.\n4. Dilated with balloons.\n5. Airways look much more open now.",
            5: "Ava is here for her stenosis she has wegeners. Airway looked tight especially subglottic and the lower lobes. We used the rigid scope. Cut the bands with the knife then ballooned them open. Trachea opened up nicely so did the segments. No bleeding really.",
            6: "Therapeutic bronchoscopy for GPA-associated airway stenosis. Rigid bronchoscopy performed. Findings: Multi-level stenosis (trachea, RLL, LUL). Intervention: Radial knife incisions + CRE balloon dilation. Result: Successful recanalization of stenotic segments.",
            7: "[Indication]\nTracheal and bronchial stenosis (GPA).\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Stenoses identified. Treated with radial knife incisions and serial balloon dilation. Patency improved.\n[Plan]\nPACU, PRN follow up.",
            8: "Ms. Harrington underwent therapeutic bronchoscopy for her complex airway stenosis caused by Granulomatosis with Polyangiitis. We used a rigid bronchoscope to access the airway. The strictures in the trachea and segmental bronchi were treated by making radial incisions with an electrocautery knife and then dilating them with balloons. This achieved excellent restoration of airway caliber.",
            9: "Procedure: Rigid bronchoscopy with lysis of adhesions and dilation.\nIndication: Airway stenosis.\nAction: Strictures were incised with an electrocautery knife. Serial dilatations were performed with balloons.\nOutcome: The airway was recanalized."
        },
        7: { # Ethan Calder (Rigid Y-stent 31636, 31637, 31641)
            1: "Indication: Malignant CAO.\nProc: Rigid Bronch, Debulking, Y-Stent.\nFindings: Tumor obstructing distal trachea/carina/mainstems.\nActions:\n- APC/Cryo debulking.\n- Silicone Y-Stent placed (15x12x12).\nResult: Airways patent through stent.",
            2: "OPERATIVE NOTE: The patient presented with critical central airway obstruction due to malignancy. Rigid bronchoscopy was performed. Extensive tumor infiltration involved the distal trachea and carina. Mechanical debulking combined with APC and cryotherapy was performed to restore the lumen. Subsequently, a silicone Y-stent was deployed to maintain patency of the trachea and bilateral mainstem bronchi.",
            3: "Codes:\n- 31641: Tumor debulking (APC/Cryo).\n- 31636: Stent placement initial (Trachea/LMB).\n- 31637: Stent placement additional (RMB).\nDevice: Silicone Y-Stent.\nJustification: Critical CAO requiring rigid intervention and stenting.",
            4: "Resident Note\nPt: Ethan Calder\nProc: Rigid/Stent\nSteps:\n1. Intubation with rigid scope difficult (teeth).\n2. Saw tumor blocking carina.\n3. Burned and cleaned it out (APC/Cryo).\n4. Measured for stent.\n5. Placed Y-stent. Position looks good.\nPlan: ICU.",
            5: "Hard intubation lost some teeth sorry. Tumor was everywhere at the bottom of the trachea. We burned it back with APC and used cryo to clean it up. Then put in a Y stent silicone. Had to push it through the cords blindly then grab it. Seated well airways open now.",
            6: "Rigid bronchoscopy for malignant central airway obstruction. Tumor debulking performed using APC and cryotherapy. Silicone Y-stent (15x12x12) deployed to stent distal trachea and both mainstems. Patency restored. Patient admitted to ICU.",
            7: "[Indication]\nMalignant central airway obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Tumor debulked via APC/Cryo. Silicone Y-stent placed. Airways patent.\n[Plan]\nICU, humidity, saline nebs.",
            8: "Mr. Calder required urgent intervention for malignant airway obstruction. Using rigid bronchoscopy, we debulked the tumor at the carina using APC and cryotherapy. To prevent re-obstruction, we placed a silicone Y-stent. Despite difficult access, the stent was deployed successfully, and the airways are now patent.",
            9: "Procedure: Rigid bronchoscopy with tumor ablation and stent implantation.\nAction: Tumor was ablated using APC and cryotherapy. A silicone Y-stent was implanted to bridge the carinal obstruction.\nResult: The airway was secured."
        },
        8: { # Linda Washington (BLVR RML 2 valves)
            1: "Indication: RML Emphysema.\nProc: BLVR RML.\nAction:\n- Chartis: CV Negative.\n- Valves: 2 Zephyr (RB4, RB5).\nResult: RML occluded.",
            2: "PROCEDURE NOTE: Elective bronchoscopy for RML lung volume reduction. The right middle lobe was isolated. Chartis assessment confirmed absence of collateral ventilation. Two Zephyr valves were deployed in the medial (RB5) and lateral (RB4) segments. Complete lobar isolation was confirmed.",
            3: "CPT: 31647 (Valve placement initial lobe).\nTarget: Right Middle Lobe.\nValves: 2 (RB4, RB5).\nChartis: Negative for CV.\nOutcome: Procedure successful.",
            4: "Resident Note\nPt: Linda Washington\nProc: RML Valves\nSteps:\n1. Insp RML.\n2. Chartis negative.\n3. Placed 2 valves (RB4, RB5).\n4. No leaks.\nPlan: Discharge.",
            5: "RML valve case. Chartis said no collateral ventilation so we proceeded. Put in two valves one for lateral one for medial. RML collapsed nicely. No pneumo on xray. Sending home.",
            6: "Bronchoscopic Lung Volume Reduction, Right Middle Lobe. Chartis CV negative. Two Zephyr valves deployed (RB4, RB5). Complete occlusion. Discharged home.",
            7: "[Indication]\nSevere emphysema RML.\n[Anesthesia]\nModerate.\n[Description]\nChartis negative. 2 valves placed RML. Good seal.\n[Plan]\nDischarge.",
            8: "Ms. Washington underwent RML valve placement. After confirming no collateral ventilation with Chartis, we placed valves in the medial and lateral segments. The lobe was fully occluded, and she was discharged the same day.",
            9: "Procedure: BLVR with valve implantation.\nTarget: Right Middle Lobe.\nAction: Chartis confirmed eligibility. Two valves implanted.\nResult: Lobe occluded."
        },
        9: { # Caleb Donahue (Rigid, Debulking, EBUS 7)
            1: "Indication: Hemoptysis, Mass.\nProc: Rigid Bronch, APC Debulking, EBUS.\nFindings: Tumor R Main/Carina/L Main.\nActions:\n- EBUS-TBNA Station 7: Positive.\n- APC debulking of airway tumor.\n- Hemostasis with Surgicel/TXA.\nResult: Airway patency improved.",
            2: "OPERATIVE REPORT: The patient presented with hemoptysis and airway obstruction. Rigid bronchoscopy was performed. Extensive tumor involved the distal trachea and both mainstems. EBUS-TBNA of a subcarinal mass (Station 7) confirmed malignancy. The endobronchial tumor was debulked using Argon Plasma Coagulation (APC) and mechanical techniques, significantly improving airway caliber. Hemostasis was achieved with TXA and Surgicel.",
            3: "Codes:\n- 31641: Tumor debulking (APC/Mechanical).\n- 31652: EBUS sampling 1-2 stations (Station 7).\nRationale: Relief of malignant stenosis and staging of mediastinal nodes.",
            4: "Resident Note\nPt: Caleb Donahue\nProc: Rigid/Debulk/EBUS\nSteps:\n1. LMA then Rigid.\n2. EBUS Station 7 (positive).\n3. Debulked tumor with APC and forceps.\n4. Bleeding controlled with TXA/Surgicel.\n5. Airways much more open.\nPlan: ICU.",
            5: "Messy case lots of blood. Rigid scope used. EBUSed the subcarinal node it was cancer. Then burned the tumor in the airway with APC and scraped it out. Bleeding was tricky used some TXA and surgicel to stop it. Airway looks better now though.",
            6: "Rigid bronchoscopy with tumor debulking and EBUS-TBNA. Indication: Hemoptysis and obstruction. EBUS Station 7 sampled: Positive. Tumor debulked from RMB/LMB/Trachea using APC. Hemostasis achieved. Significant improvement in airway patency.",
            7: "[Indication]\nHemoptysis, airway obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronch. EBUS Station 7 (+). APC debulking of central tumor. Hemostasis with TXA.\n[Plan]\nICU, Oncology consult.",
            8: "Mr. Donahue underwent rigid bronchoscopy for hemoptysis and airway obstruction. We performed EBUS-TBNA of station 7, which was positive for malignancy. We then debulked the obstructing tumor using APC and mechanical means. We controlled localized bleeding with TXA and Surgicel. The airways were significantly more patent at the end of the case.",
            9: "Procedure: Rigid bronchoscopy with tumor ablation and EBUS.\nAction: EBUS sampled station 7. Tumor was ablated with APC. Hemostasis secured.\nResult: Airway obstruction relieved."
        }
    }
    return variations

def get_base_data_mocks():
    # Names and ages to match the 10 notes in the source file
    return [
        {"idx": 0, "orig_name": "Michael Brown", "orig_age": 65, "names": ["James Wilson", "Robert Taylor", "William Anderson", "David Thomas", "Richard Jackson", "Joseph White", "Charles Harris", "Thomas Martin", "Christopher Thompson"]},
        {"idx": 1, "orig_name": "Kenji Nakamura", "orig_age": 67, "names": ["Hiroshi Tanaka", "Takeshi Yamamoto", "Kenji Sato", "Masato Suzuki", "Yuki Takahashi", "Kenta Watanabe", "Daiki Ito", "Naoki Kobayashi", "Ryo Saito"]},
        {"idx": 2, "orig_name": "Jessica McBee", "orig_age": 65, "names": ["Sarah Johnson", "Linda Williams", "Barbara Jones", "Elizabeth Brown", "Jennifer Davis", "Maria Miller", "Susan Wilson", "Margaret Moore", "Dorothy Taylor"]},
        {"idx": 3, "orig_name": "Unknown", "orig_age": 65, "names": ["John Doe", "Jane Smith", "Robert Johnson", "Michael Williams", "William Brown", "David Jones", "Richard Miller", "Joseph Davis", "Charles Garcia"]},
        {"idx": 4, "orig_name": "Unknown", "orig_age": 65, "names": ["James Rodriguez", "Mary Martinez", "Robert Hernandez", "Patricia Lopez", "John Gonzalez", "Jennifer Wilson", "Michael Anderson", "Elizabeth Thomas", "David Taylor"]},
        {"idx": 5, "orig_name": "Robert Chen", "orig_age": 67, "names": ["Wei Zhang", "Jun Li", "Yan Wang", "Min Liu", "Jian Chen", "Lei Yang", "Bo Zhao", "Gang Huang", "Jie Zhou"]},
        {"idx": 6, "orig_name": "Ava Harrington", "orig_age": 65, "names": ["Olivia Smith", "Emma Johnson", "Charlotte Williams", "Amelia Brown", "Sophia Jones", "Isabella Garcia", "Mia Miller", "Evelyn Davis", "Harper Rodriguez"]},
        {"idx": 7, "orig_name": "Ethan Calder", "orig_age": 65, "names": ["Liam Wilson", "Noah Moore", "Oliver Taylor", "Elijah Anderson", "William Thomas", "James Jackson", "Benjamin White", "Lucas Harris", "Henry Martin"]},
        {"idx": 8, "orig_name": "Linda Washington", "orig_age": 65, "names": ["Patricia Johnson", "Mary Williams", "Barbara Jones", "Elizabeth Brown", "Jennifer Davis", "Maria Miller", "Susan Wilson", "Margaret Moore", "Dorothy Taylor"]},
        {"idx": 9, "orig_name": "Caleb Donahue", "orig_age": 65, "names": ["Mason Thompson", "Logan Garcia", "Alexander Martinez", "Ethan Robinson", "Jacob Clark", "Michael Rodriguez", "Daniel Lewis", "Matthew Lee", "Henry Walker"]}
    ]

def main():
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        return
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # Update note text
            try:
                note_entry["note_text"] = variations_text[idx][style_num]
            except KeyError:
                print(f"Warning: Missing text for Note {idx} Style {style_num}")
                continue

            # Randomize Metadata
            new_age = orig_age + random.randint(-3, 3)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            new_name = record['names'][style_num - 1]
            
            if "registry_entry" in note_entry:
                note_entry["registry_entry"]["patient_age"] = new_age
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # We do not update patient_mrn with name, just unique ID
                if "patient_mrn" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"

            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    output_filename = output_dir / "synthetic_blvr_notes_part_009.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} notes.")

if __name__ == "__main__":
    main()