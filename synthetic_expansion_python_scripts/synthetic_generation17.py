import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_017.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # George Martinez (EBUS-TBNA)
            1: "Indication: Staging RUL NSCLC.\nProc: EBUS-TBNA.\nNodes sampled: 4R, 7, 11R.\nFindings:\n- 4R: 11mm, PET+. 5 passes. Benign.\n- 7: 15mm, PET+. 3 passes. Malignant (N2).\n- 11R: 7mm, PET-. 3 passes. Benign.\nComplications: None.\nImpression: N2 positive (Stn 7).",
            2: "HISTORY: Mr. Martinez presented for mediastinal staging of a right upper lobe non-small cell lung cancer. \nPROCEDURE: Endobronchial ultrasound-guided transbronchial needle aspiration was systematically performed under moderate sedation. The lymph node stations were interrogated in the standard sequence. Station 7 (subcarinal) demonstrated immediate positivity for malignancy on rapid on-site evaluation. Station 4R (right paratracheal), despite PET avidity, required multiple passes to achieve adequate cellularity and appeared benign. Station 11R was also sampled. \nCONCLUSION: Confirmed N2 disease involving the subcarinal station.",
            3: "Procedure: 31653 (EBUS sampling 3+ stations).\nTechnique: Linear EBUS scope introduced. 22G needle used.\nStations:\n1. Station 4R: 5 passes to adequacy.\n2. Station 7: 3 passes, ROSE positive.\n3. Station 11R: 3 passes.\nTotal Stations: 3.\nMedical Necessity: Staging of confirmed malignancy.",
            4: "Procedure Note\nPatient: George Martinez\nAttending: Dr. X\nSteps:\n1. Time out. Sedation (Versed/Fentanyl).\n2. Airway exam normal.\n3. EBUS scope down.\n4. Sampled 4R (took 5 passes to get cells).\n5. Sampled 7 (Positive for cancer).\n6. Sampled 11R (Benign).\nPlan: Oncology referral for Stage IIIA.",
            5: "george martinez here for ebus staging he has the rul lung cancer. sedation was moderate patient comfortable. we looked at the nodes 4r was pet positive but rose kept saying not enough cells took 5 tries finally got lymphocytes. station 7 was huge and positive right away. 11r was normal. no bleeding. n2 disease confirmed.",
            6: "Name: George Martinez / MRN: ZZ-4829-Q / Birth: 07/19/1956 INDICATION: Mediastinal staging, RUL NSCLC. Sedation: Moderate (midazolam/fentanyl). EBUS-TBNA performed with systematic approach. Station 4R (11mm, PET+): 5 total passes needed for adequacy. Station 7 (15mm, PET+): ROSE adequate immediately, positive for malignancy. Station 11R (7mm, PET-): ROSE adequate. No complications. Impression: N2 disease confirmed (station 7). Station 4R benign despite PET avidity. Adequate tissue for molecular testing obtained.",
            7: "[Indication]\nRUL NSCLC, mediastinal staging.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS-TBNA performed. Station 4R (benign), Station 7 (malignant), Station 11R (benign). Systematic sampling achieved.\n[Plan]\nOncology consult for N2 disease.",
            8: "The patient arrived for staging of his right upper lobe cancer. We used moderate sedation and inserted the EBUS scope. We started by sampling station 4R, which was difficult to get a good sample from but eventually showed benign cells. We then moved to the subcarinal node (station 7), which was clearly malignant on the first few passes. Finally, we sampled the hilar node (11R). The procedure confirmed cancer spread to the mediastinum.",
            9: "Procedure: Ultrasonic nodal aspiration.\nIndication: Staging of pulmonary carcinoma.\nAction: Stations 4R, 7, and 11R were interrogated. Transbronchial needle aspiration was performed. \nResult: Malignant cells detected in Station 7. Station 4R yielded benign lymphocytes."
        },
        1: { # Henry Walker (EBUS-TBNA)
            1: "Indication: Staging RUL mass.\nAnesthesia: Deep (Propofol).\nEBUS: Sampled 2R, 4R, 7. 21G needle.\nFindings: Lymphocytes present, no malignancy on ROSE.\nComp: None.\nDisp: Home.",
            2: "PROCEDURE: Flexible Bronchoscopy with Linear EBUS-TBNA.\nCLINICAL SUMMARY: 63-year-old male with RUL mass and borderline adenopathy.\nOPERATIVE NARRATIVE: The patient was placed under deep sedation. A systematic mediastinal survey was conducted using the Olympus BF-UC180F. Lymph node stations 2R, 4R, and 7 were visualized and sampled using a 21-gauge aspiration needle. Rapid on-site evaluation demonstrated adequate lymphoid tissue without evidence of metastasis at all sampled stations.\nIMPRESSION: Negative mediastinal staging by EBUS (N0 by EBUS).",
            3: "Code: 31653 (EBUS 3+ stations).\nStations: 2R, 4R, 7.\nNeedle: 21G Vizishot.\nScope: Olympus BF-UC180F.\nPathology: Samples sent for cell block to confirm ROSE findings (negative for malignancy).",
            4: "Resident Note\nPatient: Henry Walker\nProcedure: EBUS\nSteps:\n1. Propofol sedation.\n2. Scope inserted.\n3. Identified nodes 2R, 4R, 7.\n4. TBNA x3 passes each station.\n5. ROSE: Lymphocytes only.\n6. No complications.\nPlan: Surgery clinic follow-up.",
            5: "Procedure note for henry walker he has that spiculated mass right upper lobe. did the ebus to stage him. deep sedation used. looked at 2r 4r and 7. poked them all 3 times each. rose guy said just lymphocytes no cancer cells seen. so looks like n0 disease. discharged him home after recovery.",
            6: "Interventional Pulmonology Procedure Note. Procedure: Flexible bronchoscopy with linear EBUS-TBNA. Patient: Henry Walker, 63-year-old male. Indication: Mediastinal staging prior to lobectomy. Findings: Normal vocal cords. Central airways patent. EBUS: Olympus BF-UC180F scope used. Lymph nodes identified and sampled at 2R, 4R, and 7 using 21G Vizishot needle. Three passes obtained per station. ROSE adequate at all stations with lymphocytes only. No elastography. Complications: None. Disposition: Discharged home.",
            7: "[Indication]\nRUL mass, staging.\n[Anesthesia]\nDeep sedation (Propofol).\n[Description]\nEBUS-TBNA of stations 2R, 4R, 7. Three passes per node. ROSE negative for malignancy.\n[Plan]\nThoracic surgery referral.",
            8: "Mr. Walker underwent bronchoscopy to check his lymph nodes before potential lung surgery. We used deep sedation to keep him comfortable. The ultrasound scope allowed us to see and sample nodes in the upper and lower trachea (2R, 4R) and under the airway split (7). Preliminary results from the room showed no cancer in the lymph nodes, suggesting the cancer hasn't spread there.",
            9: "Procedure: Linear ultrasonic needle aspiration.\nContext: Pre-resection staging.\nAction: Stations 2R, 4R, and 7 were accessed. Three transbronchial passes were executed per station.\nResult: Cytology revealed lymphoid tissue devoid of malignancy."
        },
        2: { # Allison Parker (EBUS-TBNA)
            1: "Indication: Staging RLL Adeno.\nLocation: OR, GA, ETT.\nEBUS: 4R, 7, 10R sampled.\nResult: Stn 7 positive (Adeno). 4R/10R negative.\nPlan: Admit. Oncology.",
            2: "PROCEDURE: Linear Endobronchial Ultrasound.\nINDICATION: 57F with biopsy-proven RLL adenocarcinoma.\nNARRATIVE: Under general anesthesia, the mediastinum was staged. Stations 4R, 7, and 10R were identified. Transbronchial needle aspiration confirmed metastatic adenocarcinoma in the subcarinal station (7), confirming N2 disease. The paratracheal and hilar stations appeared reactive on preliminary assessment.\nIMPRESSION: Stage IIIA (N2) Adenocarcinoma.",
            3: "Billing: 31653 (EBUS 3 stations).\nSite of Service: Operating Room.\nStations: 4R, 7, 10R.\nPathology: Malignancy confirmed in station 7.\nTechnique: 22G needle aspiration.",
            4: "Procedure: EBUS Staging\nPatient: Allison Parker\nSteps:\n1. Patient intubated (GA).\n2. EBUS scope passed.\n3. Sampled 7 (Positive).\n4. Sampled 4R and 10R (Negative).\n5. Extubated in OR.\nDiagnosis: N2 positive lung cancer.",
            5: "Allison Parker 57 female RLL cancer. did ebus in the OR under GA. Checked 4R 7 and 10R. Station 7 had cancer cells rose confirmed. The others were fine. She's admitted to the floor. Will need chemo rads probably.",
            6: "Interventional Pulmonology Procedure Note. Procedure: Linear EBUS-TBNA under general anesthesia. Patient: Allison Parker, 57-year-old female with RLL adenocarcinoma. Indication: Mediastinal staging. EBUS Details: Stations 4R, 7, and 10R evaluated. A 22G needle was used. ROSE demonstrated malignant cells at station 7 consistent with adenocarcinoma; other stations reactive. Complications: None. Disposition: Admitted to oncology floor.",
            7: "[Indication]\nRLL Adenocarcinoma, N2 staging.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS-TBNA of 4R, 7, 10R. Malignancy found in Station 7. Others benign.\n[Plan]\nAdmit. Tumor board.",
            8: "Ms. Parker was brought to the operating room for staging of her lung cancer. We used general anesthesia. The EBUS procedure focused on three main lymph node areas. Unfortunately, the node underneath the airway division (station 7) contained cancer cells. The other nodes tested were clear. This places her at a more advanced stage than initially hoped, requiring systemic treatment.",
            9: "Procedure: Endobronchial ultrasonic staging.\nFindings: N2 nodal metastasis.\nAction: Stations 4R, 7, and 10R were aspirated. ROSE analysis indicated malignancy in the subcarinal station.\nResult: Upstaging to IIIA."
        },
        3: { # Eric Johnson (EBUS for Sarcoid)
            1: "Indication: Suspected Sarcoidosis.\nProc: EBUS + Elastography + Forceps Bx.\nNodes: 4R, 7, 11L.\nFindings: Blue pattern (4R/7), Green (11L). Granulomas at Stn 7.\nComp: Minor bleeding.\nDisp: Home.",
            2: "PROCEDURE: Linear EBUS with Elastography and Intranodal Forceps Biopsy.\nINDICATION: Evaluation of mediastinal adenopathy, rule out sarcoidosis.\nNARRATIVE: EBUS visualization revealed enlarged nodes at stations 4R, 7, and 11L. Elastography patterns were recorded. TBNA was performed at all stations. To increase diagnostic yield for granulomatous disease, intranodal forceps biopsies were obtained from station 7. ROSE confirmed granulomatous inflammation consistent with sarcoidosis.\nIMPRESSION: Pulmonary Sarcoidosis.",
            3: "Codes: 31653 (EBUS 3 stations).\nTechnique: TBNA + Intranodal Forceps (Mini-forceps).\nNote: Elastography used for target selection (not separately billable).\nPathology: Granulomas.",
            4: "Procedure: EBUS for Sarcoid\nPatient: Eric Johnson\nSteps:\n1. MAC sedation.\n2. EBUS scope inserted.\n3. Saw big nodes at 4R, 7, 11L.\n4. Needled all of them.\n5. Used little forceps in station 7 for tissue.\n6. ROSE: Granulomas.\nPlan: Follow up in clinic.",
            5: "Procedure note Eric Johnson sarcoid workup. MAC anesthesia. EBUS showed nodes 4r 7 11l. elastography was mixed. did needle biopsy on all three then used the forceps on station 7 to get a chunk. rose saw granulomas so its sarcoid. little bit of bleeding but stopped. discharged home.",
            6: "Linear EBUS with elastography and intranodal forceps biopsy. Patient: Eric Johnson, 69-year-old male. Indication: Tissue diagnosis of mediastinal adenopathy. EBUS findings: Enlarged nodes at 4R, 7, and 11L. A 22G needle was used for TBNA at all three stations. Intranodal forceps biopsies were performed at station 7 through prior needle tract. ROSE: Granulomatous-appearing inflammation at station 7. Complications: Self-limited bleeding. Disposition: Discharged home.",
            7: "[Indication]\nMediastinal adenopathy, r/o sarcoid.\n[Anesthesia]\nMAC.\n[Description]\nEBUS-TBNA 4R, 7, 11L. Intranodal forceps Bx Station 7. Elastography performed. Findings: Granulomatous inflammation.\n[Plan]\nPulmonary clinic follow-up.",
            8: "Mr. Johnson underwent an EBUS procedure to investigate swollen lymph nodes in his chest. We suspected sarcoidosis. We sampled three different node stations using a needle. To be sure we got enough tissue to diagnose sarcoidosis, we also used tiny forceps to take a small bite of tissue from the largest node (station 7). The preliminary look in the microscope showed the typical inflammation seen in sarcoidosis.",
            9: "Procedure: Ultrasonic nodal aspiration with forceps augmentation.\nIndication: Granulomatous disease investigation.\nAction: Stations 4R, 7, and 11L were sampled via needle. Intranodal forceps were utilized at Station 7.\nResult: Granulomatous inflammation confirmed."
        },
        4: { # Janice Moore (Radial EBUS RML)
            1: "Indication: RML nodule (15mm).\nProc: Radial EBUS (No Nav).\nDetails: Fluoroscopy guidance. Concentric view. TBBx x4, Brush x2.\nROSE: Suspicious for carcinoma.\nComp: None.\nDisp: Home.",
            2: "PROCEDURE: Radial EBUS-Guided Transbronchial Biopsy.\nINDICATION: Peripheral RML nodule.\nNARRATIVE: The bronchoscope was advanced to the RML lateral segment. A radial EBUS probe was inserted via a guide sheath under fluoroscopic guidance, identifying a concentric, solid lesion. Transbronchial forceps biopsies and brushings were obtained. Preliminary cytology is suspicious for malignancy.\nIMPRESSION: Likely RML Non-Small Cell Lung Cancer.",
            3: "Codes: 31628 (Lung Biopsy), 31654 (Radial EBUS).\nNote: No electromagnetic navigation charged (31627 excluded).\nTechnique: Guide sheath + Fluoroscopy + Radial Probe.\nTarget: Single lesion RML.",
            4: "Procedure: R-EBUS Biopsy\nPatient: Janice Moore\nSteps:\n1. Moderate sedation.\n2. Scope to RML.\n3. Radial probe found lesion (concentric).\n4. Left sheath in place.\n5. Biopsied x4, Brushed x2.\n6. Fluoro used to check position.\nResult: Suspicious for cancer.",
            5: "Janice Moore 71 female RML spot. No navigation just used fluoro and the radial probe. Found it in the lateral segment concentric view. took 4 biopsies and 2 brushes. rose looks like cancer. patient did fine going home.",
            6: "Bronchoscopy Procedure Note. Procedure: Radial EBUS-guided biopsy of right middle lobe nodule (no navigation). Patient: Janice Moore, 71-year-old female. Procedure summary: Radial EBUS catheter advanced through guide sheath into RML lateral segment based on fluoroscopy and CT roadmap. Concentric solid lesion pattern obtained. Four transbronchial forceps biopsies and two brushings performed through guide sheath. ROSE: Suspicious for malignancy. Disposition: Discharged home.",
            7: "[Indication]\n15mm RML nodule.\n[Anesthesia]\nModerate sedation.\n[Description]\nRadial EBUS (concentric view) + Fluoro. TBBx x4, Brush x2. No EMN used. ROSE suspicious for malignancy.\n[Plan]\nNodule clinic follow-up.",
            8: "Ms. Moore had a small nodule in her right middle lobe. We performed a bronchoscopy to biopsy it. We didn't use the navigation system; instead, we found the right airway using x-ray guidance and the radial ultrasound probe. We got a good ultrasound image of the nodule and took several samples. The pathologist is worried it looks like cancer.",
            9: "Procedure: Radial ultrasonic-guided pulmonary sampling.\nMethod: Fluoroscopic triangulation without electromagnetic guidance.\nAction: The RML lateral segment was cannulated. Radial ultrasound confirmed lesion concentricity. Forceps and brushes procured tissue.\nResult: Cytology suggests neoplasm."
        },
        5: { # Olivia Carter (Ion Robotic LUL)
            1: "Indication: LUL nodule (20mm).\nProc: Ion Robotic, Radial EBUS, Cone-Beam CT, Cryo.\nDetails: Nav to LUL apicoposterior. REBUS concentric. CBCT confirmed. Cryo x3, Forceps x3.\nROSE: Adenocarcinoma.\nComp: Mild bleed, wedged.\nDisp: Home.",
            2: "PROCEDURE: Robotic-Assisted Bronchoscopy with Cone-Beam CT and Cryobiopsy.\nINDICATION: Solitary LUL pulmonary nodule.\nNARRATIVE: The Ion robotic catheter was registered and navigated to the target in the apicoposterior segment of the LUL. Localization was multimodal: radial EBUS (concentric) and Cone-Beam CT (tool-in-lesion). Transbronchial cryobiopsies and standard forceps biopsies were obtained. ROSE confirmed adenocarcinoma. \nIMPRESSION: Primary Lung Adenocarcinoma.",
            3: "Codes: 31628 (Biopsy), 31627 (Robotic Nav), 31654 (REBUS).\nNote: Cryobiopsy used for tissue acquisition (billed as biopsy).\nImaging: Cone-beam CT and Radial EBUS used for verification.",
            4: "Procedure: Ion + Cryo\nPatient: Olivia Carter\nSteps:\n1. GA. Ion registered.\n2. Navigated to LUL nodule.\n3. Checked with REBUS and Spin CT.\n4. Cryoprobe used for 3 biopsies.\n5. Forceps used for 3 biopsies.\n6. ROSE: Adeno.\n7. Mild bleeding, stopped.\nResult: Cancer.",
            5: "Olivia Carter 59 female LUL nodule. Used the Ion robot. Navigated out there confirmed with radial ebus and the cone beam spin. Took 3 cryo biopsies and 3 forceps. ROSE says adenocarcinoma. a little bleeding but wedging stopped it. discharged to home.",
            6: "Robotic Bronchoscopy / EBUS Note. Procedures: Ion robotic-assisted bronchoscopy, Radial EBUS and cone-beam CT, Transbronchial cryobiopsy and forceps biopsy of LUL nodule. Patient: Olivia Carter. Robotic catheter navigated to apicoposterior segment of LUL. Concentric radial EBUS view obtained. Cone-beam CT confirmed tool-in-lesion. Three cryobiopsies and three standard forceps biopsies performed. ROSE: Malignant epithelial cells, favor adenocarcinoma.",
            7: "[Indication]\nLUL Nodule (20mm).\n[Anesthesia]\nGeneral.\n[Description]\nIon Robotic Navigation. Radial EBUS concentric. Cone-Beam CT confirmation. Cryobiopsy x3, Forceps x3. Diagnosis: Adenocarcinoma.\n[Plan]\nLung cancer clinic.",
            8: "Ms. Carter underwent a robotic bronchoscopy for her left lung nodule. We drove the robotic catheter to the exact spot and used both ultrasound and a 3D CT spin in the room to make sure we were right inside the nodule. We used a freezing probe (cryobiopsy) to get large samples. The preliminary results show adenocarcinoma. She went home after waking up.",
            9: "Procedure: Robotic navigational parenchymal sampling.\nTools: Ion platform, cryoprobe, Cone-Beam CT.\nAction: The LUL target was localized via shape-sensing robotics and confirmed radiographically. Cryo-adhesion and forceps extraction yielded diagnostic tissue.\nResult: Adenocarcinoma."
        },
        6: { # Daniel Rivera (EMN LLL)
            1: "Indication: LLL nodule (14mm).\nProc: EMN (superDimension) + REBUS.\nDetails: Nav to LLL lateral basal. REBUS eccentric. Fluoroscopy confirmed. Bx x5, Brush x2, Mini-BAL.\nROSE: Nondiagnostic.\nDisp: Home. Re-eval.",
            2: "PROCEDURE: Electromagnetic Navigational Bronchoscopy.\nINDICATION: Indeterminate LLL nodule.\nNARRATIVE: Using the superDimension system, a pathway was mapped to the LLL lateral basal segment. The locatable guide was advanced to the target. Radial EBUS revealed an eccentric view, suggesting the probe was adjacent to the lesion. Fluoroscopy confirmed position. Biopsies and brushings were obtained but ROSE was nondiagnostic.\nIMPRESSION: Nondiagnostic bronchoscopy.",
            3: "Codes: 31627 (Nav), 31628 (Biopsy), 31654 (REBUS).\nTarget: LLL Nodule.\nYield: Nondiagnostic on ROSE.\nTechnique: Electromagnetic navigation with fluoroscopic confirmation.",
            4: "Procedure: EMN Bronch\nPatient: Daniel Rivera\nSteps:\n1. Moderate sedation.\n2. Registered superDimension.\n3. Navigated to LLL.\n4. Radial EBUS: Eccentric.\n5. Biopsied anyway x5.\n6. ROSE: Just bronchial cells.\nPlan: Maybe CT biopsy next?",
            5: "Daniel Rivera LLL nodule small 14mm. Used superdimension. Registration was ok. got to the lesion but ultrasound was eccentric not concentric. took biopsies brushes and a wash. rose didn't see cancer just normal cells. discharged home might need another biopsy.",
            6: "Interventional Pulmonology Procedure Note. Procedures: Electromagnetic navigational bronchoscopy (superDimension) with radial EBUS and transbronchial biopsies of left lower lobe nodule. Patient: Daniel Rivera, 65-year-old male. Highlights: EMN plan created. Radial EBUS showed eccentric view. Fluoroscopy confirmed position at lesion. Five forceps biopsies, two brushings and one mini-BAL obtained. ROSE: Nondiagnostic, bronchial cells only. Disposition: Discharged home.",
            7: "[Indication]\n14mm LLL nodule.\n[Anesthesia]\nModerate sedation.\n[Description]\nEMN (superDimension) to LLL lateral basal. REBUS eccentric. Biopsies/Brush/BAL performed. ROSE negative.\n[Plan]\nRepeat biopsy (CT guided) or surveillance.",
            8: "Mr. Rivera had a small nodule in the left lower lung. We used the electromagnetic navigation system to try and reach it. We got close, but the ultrasound probe was next to the nodule rather than inside it (eccentric view). We took biopsies from that spot, but the preliminary reading didn't show any cancer or specific diagnosis. We may need to try a different biopsy method.",
            9: "Procedure: Electromagnetic guided pulmonary interrogation.\nOutcome: Nondiagnostic sampling.\nAction: The catheter was navigated to the LLL target. Radial sonography displayed an eccentric relation. Tissue was harvested but cytopathology was inconclusive."
        },
        7: { # Patrick Hughes (Tracheal Stenosis - Stent)
            1: "Indication: Tracheal stenosis (post-intubation).\nProc: Rigid bronch, Balloon dilation, Silicone Stent.\nDetails: 70% subglottic stenosis. Dilated to 12mm. 12x40mm Dumon stent placed. Residual 10% narrowing.\nPlan: Admit overnight.",
            2: "PROCEDURE: Therapeutic Rigid Bronchoscopy for Tracheal Stenosis.\nINDICATION: Exertional stridor, benign tracheal stenosis.\nNARRATIVE: Rigid bronchoscopy identified a concentric fibrotic stenosis in the subglottic trachea. The lesion was dilated serially with balloons. A 12x40mm silicone stent was deployed to maintain patency. The airway caliber significantly improved.\nIMPRESSION: Successful recanalization and stenting of benign tracheal stenosis.",
            3: "Code: 31631 (Tracheal Stent Placement).\nNote: Dilation (31630) is bundled/included when stent is placed.\nDevice: Silicone Stent.\nIndication: Benign stenosis.",
            4: "Procedure: Rigid Bronch & Stent\nPatient: Patrick Hughes\nSteps:\n1. GA / Jet ventilation.\n2. Rigid scope 11.\n3. Found tight stenosis in trachea.\n4. Balloon dilated.\n5. Placed silicone stent.\n6. Airway looks good now.\nPlan: Observe overnight.",
            5: "Patrick Hughes 58 male with stridor. Tracheal stenosis from old intubation. Did rigid bronch under jet vent. dilated it up with a balloon then put a silicone stent 12 by 40. looks wide open now. minor bleeding. admit for obs.",
            6: "Central Airway Therapeutic Bronchoscopy Note. Procedures: Rigid bronchoscopy, Balloon dilation of tracheal stenosis, Silicone stent placement. Patient: Patrick Hughes. Findings: Short-segment concentric fibrotic stenosis 2 cm below vocal cords; ~70% luminal narrowing. Intervention: Serial balloon dilations performed to 12 mm, then a 12 x 40 mm silicone straight stent placed across the stenotic segment. Disposition: Extubated to PACU and admitted overnight.",
            7: "[Indication]\nPost-intubation tracheal stenosis.\n[Anesthesia]\nGeneral, Rigid, Jet Vent.\n[Description]\nSubglottic stenosis dilated (balloon). 12x40mm silicone stent placed. Patency restored.\n[Plan]\nAdmit. Airway monitoring.",
            8: "Mr. Hughes was suffering from stridor due to scar tissue in his trachea from a breathing tube. We took him to the OR and used a rigid scope to dilate the scar tissue with a balloon. To keep it open, we placed a silicone stent. His airway is much more open now, and he should breathe easier. We'll watch him overnight.",
            9: "Procedure: Rigid airway dilation and prosthetic scaffolding.\nIndication: Cicatricial tracheal stenosis.\nAction: The stenotic segment was radially expanded via balloon. A silicone prosthesis was deployed to prevent recoil.\nResult: Restoration of tracheal lumen."
        },
        8: { # Brenda Lewis (Transplant Stenosis - Dilation only)
            1: "Indication: LMS anastomotic stenosis (Transplant).\nProc: Rigid bronch, Mechanical + Balloon Dilation.\nDetails: 60% narrowing left anastomosis. Dilated to 10mm. No stent.\nComp: Small mucosal tear, self-limited.\nDisp: Transplant ward.",
            2: "PROCEDURE: Rigid Bronchoscopy with Balloon Dilation.\nINDICATION: Benign anastomotic stenosis post-lung transplant.\nNARRATIVE: The left mainstem anastomosis was inspected via rigid bronchoscopy and found to be stenotic (60% narrowing). Mechanical dilation was performed using the rigid barrel, followed by balloon dilation to 10mm. Stenting was deferred. A small mucosal tear was noted but hemostasis was achieved.\nIMPRESSION: Improved anastomotic patency.",
            3: "Code: 31630 (Bronchial Dilation).\nSite: Left Mainstem.\nTechnique: Rigid + Balloon.\nNote: No stent placed (excludes 31636).",
            4: "Procedure: Rigid Dilation\nPatient: Brenda Lewis\nSteps:\n1. GA / Jet.\n2. Rigid scope to LMS.\n3. Anastomosis tight.\n4. Dilated with scope and balloon.\n5. Opened up to 10mm.\n6. No stent needed today.\nPlan: Transplant ward.",
            5: "Brenda Lewis transplant patient with stenosis left side. went in with rigid scope. dilated the anastomosis with the barrel then a balloon. opened up good. didn't put a stent in. little tear in the mucosa but stopped bleeding. sending her to the floor.",
            6: "Rigid Bronchoscopy Procedure Note. Procedures: Rigid bronchoscopy and mechanical debulking, Balloon dilation of left mainstem bronchus. Patient: Brenda Lewis, 73-year-old female. Findings: Fibrotic annular stenosis at anastomotic site in left mainstem with ~60% narrowing. Interventions: Mechanical dilation with rigid barrel and forceps followed by controlled balloon dilation to 10 mm. No stent placed. Complications: Small mucosal tear without active bleeding.",
            7: "[Indication]\nLMS transplant stenosis.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nAnastomosis 60% stenosed. Dilated mechanically and with balloon to 10mm. No stent placed.\n[Plan]\nAdmit to transplant service.",
            8: "Mrs. Lewis has narrowing at her lung transplant connection site on the left. We used a rigid bronchoscope to stretch this area open, first with the scope itself and then with a balloon. It opened up nicely to 10mm. We decided not to place a stent at this time. There was a tiny tear from the stretching, but it wasn't bleeding significantly.",
            9: "Procedure: Rigid bronchial expansion.\nContext: Post-transplant anastomotic stricture.\nAction: The left mainstem stenosis was addressed via mechanical and pneumatic dilation techniques. Stent deployment was withheld.\nResult: Augmented bronchial diameter."
        },
        9: { # Raymond Scott (Carina Tumor - Y Stent)
            1: "Indication: Carinal SCC, obstruction.\nProc: Rigid bronch, Debulk (Mechanical/APC), Y-Stent.\nDetails: 80% obstruction distal trachea/carina. Debulked. 14x60/40mm Y-stent placed.\nComp: Desat during deployment.\nDisp: ICU, intubated.",
            2: "PROCEDURE: Rigid Bronchoscopy, Tumor Debulking, and Y-Stent Placement.\nINDICATION: Malignant central airway obstruction.\nNARRATIVE: Large squamous cell carcinoma involving the carina was visualized. Significant debulking was achieved using mechanical coring and APC. To maintain patency of the distal trachea and both mainstems, a silicone Y-stent was deployed. Patient required recruitment post-deployment due to desaturation.\nIMPRESSION: Palliation of critical carinal obstruction.",
            3: "Codes: 31641 (Tumor Destruction), 31631 (Tracheal Stent - Y stent counts as tracheal usually, or complex).\nNote: Y-stent involves trachea and bronchi. Coding convention varies, usually primary stent code.\nTechnique: Rigid coring + APC.",
            4: "Procedure: Rigid Bronch Y-Stent\nPatient: Raymond Scott\nSteps:\n1. Rigid scope inserted.\n2. Carina blocked by tumor.\n3. Cored out tumor, used APC.\n4. Placed Y-stent (Silicone).\n5. Patient desatted, bagged up.\n6. Stent looks good.\nPlan: ICU intubated.",
            5: "Raymond Scott carinal tumor. rigid bronch to open it up. mechanical debulking and APC. put in a Y stent to cover trachea and both mains. he desatted during the placement but came back up. keeping him on the vent in the ICU.",
            6: "Central Airway Stenting Note. Procedures: Rigid bronchoscopy with tumor debulking, Y-shaped silicone stent placement. Patient: Raymond Scott. Findings: Bulky endobronchial tumor involving distal trachea and extending into both mainstem bronchi causing ~80% obstruction. Interventions: Mechanical debulking with rigid barrel and forceps followed by argon plasma coagulation. A custom 14 x 60/40 mm silicone Y stent was deployed. Disposition: Remained intubated postprocedure and transferred to ICU.",
            7: "[Indication]\nMalignant carinal obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nTumor debulked (Core/APC). Y-Stent placed (Trachea/RMS/LMS). Airway patent.\n[Plan]\nICU, mechanical ventilation.",
            8: "Mr. Scott had a large tumor blocking the split of his windpipe (carina). We performed an emergency procedure to open the airway. Using a rigid scope, we scraped away the tumor and burned the base. Then, we placed a Y-shaped silicone stent that holds open the trachea and both lung tubes. He had a brief drop in oxygen levels during the stent placement but recovered. He stays on the ventilator in the ICU for now.",
            9: "Procedure: Rigid oncologic debulking and Y-prosthesis insertion.\nIndication: Carinal asphyxiation syndrome.\nAction: The endobronchial mass was excised and cauterized. A bifurcated silicone stent was positioned to scaffold the carina.\nResult: Restoration of central airflow."
        }
    }
    return variations

def get_base_data_mocks():
    # Names and mock variations
    return [
        {"idx": 0, "orig_name": "George Martinez", "orig_age": 69, "names": ["Frank Garcia", "Hector Ramirez", "Luis Torres", "Carlos Sanchez", "Miguel Hernandez", "Jose Rodriguez", "Juan Flores", "Antonio Diaz", "Manuel Gomez"]},
        {"idx": 1, "orig_name": "Henry Walker", "orig_age": 63, "names": ["Robert Hall", "William Allen", "James Young", "Thomas King", "David Wright", "Charles Scott", "Joseph Green", "Richard Baker", "Paul Adams"]},
        {"idx": 2, "orig_name": "Allison Parker", "orig_age": 57, "names": ["Sarah Turner", "Jennifer Collins", "Jessica Cook", "Amanda Murphy", "Melissa Bell", "Stephanie Bailey", "Nicole Rivera", "Heather Cooper", "Elizabeth Richardson"]},
        {"idx": 3, "orig_name": "Eric Johnson", "orig_age": 69, "names": ["Mark Williams", "Donald Jones", "George Brown", "Kenneth Davis", "Steven Miller", "Edward Wilson", "Brian Moore", "Ronald Taylor", "Anthony Anderson"]},
        {"idx": 4, "orig_name": "Janice Moore", "orig_age": 71, "names": ["Betty White", "Dorothy Harris", "Helen Martin", "Margaret Thompson", "Ruth Garcia", "Sandra Martinez", "Sharon Robinson", "Carol Clark", "Brenda Rodriguez"]},
        {"idx": 5, "orig_name": "Olivia Carter", "orig_age": 59, "names": ["Lisa Lewis", "Nancy Lee", "Karen Walker", "Donna Hall", "Susan Allen", "Patricia Young", "Linda King", "Barbara Wright", "Mary Scott"]},
        {"idx": 6, "orig_name": "Daniel Rivera", "orig_age": 65, "names": ["John Lopez", "Michael Hill", "David Flores", "James Green", "Robert Adams", "William Baker", "Richard Gonzalez", "Thomas Nelson", "Charles Carter"]},
        {"idx": 7, "orig_name": "Patrick Hughes", "orig_age": 58, "names": ["Christopher Mitchell", "Matthew Perez", "Daniel Roberts", "Anthony Turner", "Mark Phillips", "Donald Campbell", "Paul Parker", "Steven Evans", "Andrew Edwards"]},
        {"idx": 8, "orig_name": "Brenda Lewis", "orig_age": 73, "names": ["Shirley Collins", "Cynthia Stewart", "Kathleen Sanchez", "Amy Morris", "Angela Rogers", "Debra Reed", "Martha Cook", "Christine Morgan", "Catherine Bell"]},
        {"idx": 9, "orig_name": "Raymond Scott", "orig_age": 69, "names": ["Gregory Murphy", "Jerry Bailey", "Dennis Rivera", "Walter Cooper", "Peter Richardson", "Harold Cox", "Douglas Howard", "Carl Ward", "Arthur Torres"]}
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
                print(f"Warning: Missing variation for Note {idx} Style {style_num}")
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
    output_filename = output_dir / "synthetic_interventional_notes_part_017.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()