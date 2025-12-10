import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_087.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each note index.
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
        0: { # Note 0: Adams, Steven (LUL Nodule: Ion, TBNA, Cryo, Brush, BAL, Fiducial)
            1: "Procedure: Ion Robotic Bronchoscopy.\nTarget: 24mm LUL Apicoposterior nodule.\nActions:\n- Navigated to target (0.7cm distance).\n- rEBUS: eccentric view.\n- CBCT: tool-in-lesion confirmed.\n- TBNA (21G): 7 passes.\n- Cryobiopsy (1.1mm): 3 samples (6s freeze).\n- Brush: 2 samples.\n- BAL: 60cc instilled, 22cc return.\n- Fiducial: 1 gold marker placed.\nROSE: Lymphocytes/benign.\nComplications: None.",
            2: "OPERATIVE NARRATIVE: The patient, Mr. Adams, presented for diagnostic evaluation of a 24mm partially solid nodule within the apicoposterior segment of the left upper lobe. Following induction of general anesthesia, the Ion robotic platform was utilized for electromagnetic navigation. Registration error was minimized to 3.1mm. The target was approached, and radial endobronchial ultrasound (rEBUS) demonstrated an eccentric, continuous margin. Cone-beam CT (CBCT) with 3D reconstruction verified the tool-in-lesion status. We proceeded with a multi-modal sampling strategy: transbronchial needle aspiration (TBNA) using a 21-gauge needle, transbronchial cryobiopsy utilizing a 1.1mm probe with a 6-second freeze time, and protected specimen brushing. Additionally, a bronchoalveolar lavage (BAL) was performed for microbiological analysis. Finally, a single gold fiducial marker was deployed under fluoroscopic guidance to facilitate future stereotactic radiotherapy. Rapid on-site evaluation (ROSE) indicated benign lymphoid tissue.",
            3: "Coding Data:\nPrimary Procedure: 31626 (Placement of fiducial markers).\nSecondary Procedures:\n- 31629 (TBNA of LUL nodule; 7 samples).\n- 31627 (Computer-assisted navigation; Ion platform).\n- 31654 (REBUS for peripheral lesion).\n- 31628 (Transbronchial cryobiopsy; 3 samples).\n- 31623 (Brushing).\n- 31624 (BAL of LUL).\nClinical Note: Navigation to the LUL apicoposterior segment was successful. Multiple sampling modalities (needle, cryo, brush) were utilized on the single 24mm lesion. A fiducial marker was placed for therapeutic planning.",
            4: "Procedure Note\nResident: Dr. Alex Chen\nAttending: Dr. Sarah Williams\nPatient: Steven Adams\n\nIndication: LUL Nodule.\n\nSteps:\n1. Time out performed.\n2. General anesthesia induced. 8.0 ETT placed.\n3. Airway inspection: Normal.\n4. Navigation: Ion robot to LUL (LB1+2). Reg error 3.1mm.\n5. Confirmation: rEBUS (eccentric) and Cone Beam CT.\n6. Biopsy: \n   - TBNA x7 (21G)\n   - Cryo x3 (1.1mm)\n   - Brush x2\n7. Marker: Gold fiducial placed.\n8. Lavage: BAL LUL performed.\n9. Completion: Stable. Extubated.",
            5: "Steven Adams procedure note date 08/26/2025 doing the robotic bronchoscopy today for that 24mm LUL nodule anesthesia was general tube size 8 used the Ion system got pretty close about 0.7cm away radial ebus showed eccentric view confirmed with the spin CT thing. Did a bunch of biopsies used the 21 gauge needle for 7 passes then the cryo probe 1.1mm for 3 samples frozen for 6 seconds also brushed it twice. Put in a fiducial marker gold one for rad onc. Did a wash too 60cc in. Rose said lymphocytes benign. No bleeding patient woke up fine.",
            6: "The patient was brought to the bronchoscopy suite and placed under general anesthesia. The Ion robotic catheter was navigated to the apicoposterior segment of the LUL to target a 24mm nodule. Registration error was 3.1mm. rEBUS showed an eccentric view. Cone Beam CT confirmed tool-in-lesion. We performed TBNA (7 passes, 21G), cryobiopsy (3 samples, 1.1mm probe), and brushing (2 samples). A gold fiducial marker was placed. BAL was performed in the same segment. ROSE showed lymphocytes and benign cells. The patient tolerated the procedure well.",
            7: "[Indication]\nPart-solid 24mm nodule in LUL (Apicoposterior).\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon robotic navigation used. Target reached (LB1+2). Confirmed via rEBUS (eccentric) and Cone Beam CT. \nBiopsies taken: \n- TBNA (21G)\n- Cryobiopsy (1.1mm)\n- Brush\nFiducial marker placed. BAL performed.\n[Plan]\nDischarge. Follow up pathology.",
            8: "Mr. Adams underwent a robotic-assisted bronchoscopy to investigate a lesion in his left lung. We successfully navigated the Ion catheter to the Apicoposterior segment of the Left Upper Lobe. Once we were close to the 24mm nodule, we used ultrasound and a special CT scan in the room to make sure we were in the right spot. We took several samples using a needle, a freezing probe (cryobiopsy), and a small brush. We also washed the area with saline to check for infection. Before finishing, we placed a small gold marker in the nodule to help with future treatments. The preliminary results suggest benign cells.",
            9: "Procedure: Robotic bronchoscopy.\nTarget: LUL mass.\nTechnique: The Ion system was steered to the lesion. Localization was verified with rEBUS and Cone Beam CT. The lesion was sampled via aspiration (TBNA), freezing (cryobiopsy), and abrasion (brushing). A fiducial was deployed. The segment was lavaged. \nOutcome: Samples acquired. No complications."
        },
        1: { # Note 1: Hill, Dorothy (LUL Nodule: Ion, TBNA, Brush)
            1: "Procedure: Ion Bronchoscopy LUL.\nTarget: 31mm nodule (LB1+2).\nTech: Ion Robot, rEBUS (concentric), CBCT.\nSampling:\n- TBNA: 4 passes (21G/23G).\n- Brush: 2 samples.\nROSE: Benign respiratory epithelium.\nComplications: None.",
            2: "CLINICAL SUMMARY: Ms. Hill is a 61-year-old female presenting with multiple pulmonary nodules; the dominant 31mm LUL lesion was targeted for characterization.\nPROCEDURAL DETAILS: Under general anesthesia, the Ion robotic platform facilitated navigation to the apicoposterior segment of the left upper lobe. Radial EBUS identified a concentric lesion signal. Positional accuracy was validated via Cone Beam CT 3D reconstruction. Transbronchial needle aspiration was executed using both 21G and 23G needles, followed by cytological brushing. Rapid on-site evaluation demonstrated benign respiratory epithelium and macrophages.",
            3: "Billing Codes Submitted:\n- 31629 (Primary): Bronchoscopy with transbronchial needle aspiration (LUL nodule).\n- 31627: Navigation bronchoscopy (Ion system).\n- 31654: Radial EBUS guidance.\n- 31623: Bronchial brushing.\nNote: Cryobiopsy was not performed. Only TBNA and brushing were utilized for the 31mm LUL target.",
            4: "Resident Note\nPatient: Dorothy Hill\nProcedure: Robotic Bronchoscopy (LUL)\nAttending: Dr. Park\n\n1. Induced GA, ETT placement confirmed.\n2. Navigated to LUL (LB1+2) with Ion robot.\n3. Confirmed target with rEBUS (concentric) and CBCT.\n4. TBNA x4 using 21G/23G needles.\n5. Brush biopsy x2.\n6. ROSE: Benign cells.\n7. Extubated stable.",
            5: "dorothy hill 7/20/25 doing a biopsy on that large 31mm nodule in the LUL used the ion robot reg error was 3.4mm navigated to 1.7cm away radial ebus showed concentric view confirmed with cone beam ct. did 4 needle passes mixed 21 and 23 gauge and then brushed it twice rose was just benign stuff macrophages no bleeding really discharged home.",
            6: "General anesthesia was induced for a robotic bronchoscopy on a 31mm LUL nodule. Navigation to the Apicoposterior segment was achieved with the Ion system. Verification was performed using radial EBUS (concentric) and Cone Beam CT. We obtained 4 TBNA samples using 21G and 23G needles, followed by 2 brushings. The rapid onsite evaluation showed benign cells. The patient was extubated without issues.",
            7: "[Indication]\nDominant 31mm LUL nodule.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nRobotic navigation (Ion) to LB1+2. Confirmed with rEBUS/CBCT. \nIntervention: \n- TBNA (21G/23G)\n- Protected Brush\n[Plan]\nPathology pending. Outpatient discharge.",
            8: "We performed a robotic bronchoscopy on Ms. Hill to biopsy a 31mm nodule in her left upper lobe. Using the Ion system, we navigated to the apicoposterior segment. We confirmed the location with ultrasound and a spin CT scan. We then took four needle biopsy samples and two brush samples. The initial look at the cells showed benign tissue. The procedure went smoothly with no bleeding.",
            9: "Procedure: Robotic-assisted airway exploration.\nSite: Left Upper Lobe mass.\nMethods: The catheter was guided to the target. Confirmation provided by ultrasonic and tomographic imaging. The lesion was aspirated with needles and swept with a cytology brush. \nResult: Material collected for analysis. Patient stable."
        },
        2: { # Note 2: Young, Linda (Lingula Nodule: Ion, TBNA, Cryo)
            1: "Procedure: Ion Bronchoscopy Lingula.\nTarget: 11mm nodule (LB4).\nNavigation: Ion (Reg error 2.1mm), rEBUS (eccentric), CBCT.\nBiopsy:\n- TBNA (21G): 4 passes.\n- Cryobiopsy (1.1mm): 4 samples (5s freeze).\nROSE: Negative for malignancy.\nDisp: Home.",
            2: "OPERATIVE REPORT: Ms. Young presented for biopsy of a dominant 11mm nodule in the superior lingula. Following general anesthesia, the Ion robotic system was deployed. Navigation to the LB4 segment was successful with a registration error of 2.1mm. Radial EBUS demonstrated an eccentric view, and Cone Beam CT confirmed the catheter position relative to the nodule. We proceeded with transbronchial needle aspiration (21G) and transbronchial cryobiopsy (1.1mm probe). Despite the small lesion size, adequate tissue was acquired. ROSE was negative for malignant neoplasm.",
            3: "CPT Justification:\n- 31629: Transbronchial needle aspiration (primary sampling).\n- 31628: Transbronchial cryobiopsy (secondary sampling).\n- 31627: Robotic navigation add-on.\n- 31654: Radial EBUS add-on.\nLocation: Lingula (LB4). Tools: Ion catheter, 21G needle, 1.1mm cryoprobe.",
            4: "Procedure Note: Robotic Bronchoscopy\nPatient: Linda Young\nSite: Lingula (11mm nodule)\n\n- GA/ETT.\n- Ion navigation to Superior Lingula.\n- rEBUS: Eccentric.\n- CBCT: Confirmed tool-in-lesion.\n- TBNA x4 (21G).\n- Cryobiopsy x4 (1.1mm, 5s).\n- ROSE: No malignancy seen.\n- No complications.",
            5: "Linda Young procedure note 07/18/25 lingula nodule 11mm used the ion platform robotic nav reg error 2.1mm got to about 1.7cm away used radial ebus eccentric view and the spin ct to confirm. took 4 needle biopsies 21g and 4 cryo biopsies 1.1mm probe 5 sec freeze. rose didn't show cancer no bleeding patient did well.",
            6: "Under general anesthesia, the patient underwent Ion robotic bronchoscopy targeting an 11mm nodule in the Superior Lingula. Navigation utilized shape-sensing technology with a 2.1mm error. Verification via rEBUS (eccentric) and Cone Beam CT was performed. Samples were obtained via 21G TBNA (4 passes) and 1.1mm cryobiopsy (4 samples). ROSE was negative for malignancy. The patient was discharged stable.",
            7: "[Indication]\n11mm Lingula nodule.\n[Anesthesia]\nGeneral.\n[Description]\nRobotic navigation to LB4. Imaging confirmation (rEBUS, CBCT). \nSampling: \n- TBNA (21G)\n- Cryobiopsy (1.1mm)\n[Plan]\nOutpatient follow-up.",
            8: "Ms. Young underwent a biopsy of a small 11mm nodule in the lingula section of her left lung. We used the robotic Ion system to reach the area. Once we navigated there, we double-checked our position with ultrasound and a CT scan. We took samples using both a needle and a freezing probe (cryobiopsy). The preliminary results didn't show cancer, but we sent everything for full analysis. She handled the anesthesia well.",
            9: "Procedure: Robotic navigation bronchoscopy.\nFocus: Lingular lesion.\nTechnique: The device was steered to the superior lingula. Localization verified by sonography and tomography. The nodule was aspirated and cryo-sampled. \nFindings: No immediate evidence of carcinoma."
        },
        3: { # Note 3: Jones, Jonathan (RUL Nodule: Ion, TBNA, Cryo, Brush, Fiducial)
            1: "Procedure: Ion Bronchoscopy RUL.\nTarget: 33mm nodule (RB1).\nNav: Ion, rEBUS (concentric), CBCT.\nActions:\n- TBNA (23G): 6 passes.\n- Cryobiopsy (1.7mm): 5 samples.\n- Fiducial: 1 gold marker.\n- Brush: 2 samples.\nROSE: Lymphocytes/benign.\nComplications: None.",
            2: "PROCEDURE NOTE: Mr. Jones underwent robotic-assisted bronchoscopy for a 33mm ground glass opacity in the RUL apical segment. Utilizing the Ion platform, we navigated to the target with CBCT confirmation. The lesion was concentric on rEBUS. We performed extensive sampling including TBNA (23G), cryobiopsy (1.7mm probe, 7s freeze), and cytological brushing. A gold fiducial marker was deployed for future localization. Immediate cytologic evaluation showed benign lymphoid cells.",
            3: "Code Selection:\n- 31626: Fiducial placement (Primary).\n- 31629: TBNA (Secondary).\n- 31628: Cryobiopsy.\n- 31623: Brushing.\n- 31627: Navigation.\n- 31654: EBUS.\nSite: RUL Apical (RB1). Patient: Jonathan Jones.",
            4: "Procedure: RUL Biopsy / Fiducial\nPatient: Jonathan Jones\nAttending: Dr. Anderson\n\n1. Intubation/GA.\n2. Ion Nav to RB1 (33mm nodule).\n3. Confirmed with rEBUS/CBCT.\n4. TBNA x6 (23G).\n5. Cryobiopsy x5 (1.7mm).\n6. Fiducial placed.\n7. Brush x2.\n8. ROSE: Benign.",
            5: "jonathan jones 8/27/25 rul nodule 33mm ground glass... used ion robot reg error 3.8mm nav to 2.0cm away radial ebus concentric spin ct confirmed. did 23g needle x6 cryo 1.7mm x5 and brush x2. put in a gold marker too. rose benign lymphocytes. no bleeding extubated fine.",
            6: "A robotic bronchoscopy was performed on a 33mm RUL nodule. Navigation to the Apical segment (RB1) was achieved with the Ion system. rEBUS showed a concentric view. Tool-in-lesion was confirmed with Cone Beam CT. The lesion was sampled via TBNA (23G), cryobiopsy (1.7mm), and brushing. A fiducial marker was placed. ROSE indicated lymphocytes and benign cells. The patient was discharged to recovery.",
            7: "[Indication]\n33mm RUL ground glass opacity.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to RB1. Confirmed via rEBUS/CBCT. \nProcedures:\n- TBNA\n- Cryobiopsy\n- Fiducial placement\n- Brushing\n[Plan]\nFollow-up in 5-7 days.",
            8: "Mr. Jones had a 33mm nodule in the top of his right lung that required biopsy. We used the robotic system to navigate to the apical segment. We confirmed we were in the right place using ultrasound and 3D imaging. We took several biopsies using a needle, a freezing probe, and a brush. We also placed a gold marker in the nodule. The initial check of the cells showed benign tissue.",
            9: "Procedure: Robotic airway intervention.\nTarget: RUL opacity.\nSteps: Guided the catheter to the apical segment. Validated position with multimodal imaging. Performed aspiration, cryo-extraction, and brushing. Implanted a fiducial marker. \nResult: Adequate samples obtained."
        },
        4: { # Note 4: Mitchell, Daniel (RLL Nodule: Ion, TBNA, Cryo, Brush)
            1: "Procedure: Ion Bronchoscopy RLL.\nTarget: 33mm nodule (RB8).\nNav: Ion, rEBUS (adjacent), CBCT.\nBiopsy:\n- TBNA (23G): 7 passes.\n- Cryobiopsy (1.7mm): 5 samples.\n- Brush: 2 samples.\nROSE: Suspicious for malignancy (Atypical cells).\nComplications: None.",
            2: "OPERATIVE REPORT: Mr. Mitchell underwent diagnostic bronchoscopy for a screening-detected 33mm RLL nodule. The Ion robotic system facilitated navigation to the anterior-basal segment. rEBUS demonstrated an adjacent lesion signature. Cone Beam CT reconstruction confirmed tool-in-lesion. We performed TBNA (23G), transbronchial cryobiopsy (1.7mm), and brushing. Rapid on-site evaluation revealed atypical cells suspicious for malignancy.",
            3: "Billing Data:\n- 31629: TBNA (Primary sampling).\n- 31628: Cryobiopsy.\n- 31623: Brushing.\n- 31627: Robotic Nav.\n- 31654: EBUS.\nTarget: RLL Anterior-Basal (RB8). ROSE positive for atypical cells.",
            4: "Resident Procedure Note\nPatient: Daniel Mitchell\nSite: RLL Nodule (33mm)\n\n- GA induced.\n- Ion Nav to RB8.\n- rEBUS: Adjacent.\n- CBCT: Confirmed.\n- TBNA x7 (23G).\n- Cryo x5 (1.7mm).\n- Brush x2.\n- ROSE: Suspicious for malignancy.\n- Patient stable.",
            5: "daniel mitchell procedure date 6/14/25 lung cancer screening found a 33mm rll nodule used the ion robot to get to rb8 radial ebus was adjacent cone beam ct looked good. did 7 needle passes 23g and 5 cryo samples 1.7mm plus brushing. rose said atypical cells suspicious for cancer. no bleeding discharged.",
            6: "The patient underwent general anesthesia for Ion robotic bronchoscopy of a 33mm RLL nodule. Navigation to the Anterior-Basal segment was confirmed with rEBUS (adjacent) and Cone Beam CT. Biopsies were obtained using TBNA (23G), cryobiopsy (1.7mm), and brushing. ROSE was suspicious for malignancy. The patient recovered without complications.",
            7: "[Indication]\n33mm RLL nodule (Screening detected).\n[Anesthesia]\nGeneral.\n[Description]\nRobotic navigation to RB8. Validated with rEBUS/CBCT.\nSampling:\n- TBNA\n- Cryobiopsy\n- Brushing\n[Plan]\nOncology referral pending final path.",
            8: "Mr. Mitchell underwent a biopsy for a nodule found during lung cancer screening. We used the robotic catheter to reach the lower right lung. We confirmed the location with imaging. We took multiple samples using a needle, a freezing probe, and a brush. The pathologist in the room saw some atypical cells that look suspicious for cancer. We will wait for the final report to confirm.",
            9: "Procedure: Robotic bronchoscopic investigation.\nLesion: RLL mass.\nMethod: Navigated to anterior-basal segment. Verified via sonography/tomography. Sampled via needle aspiration, cryo-adhesion, and brushing. \nAssessment: Cytology suggests malignancy."
        },
        5: { # Note 5: Rodriguez, Rebecca (Lingula Nodule: Ion, TBNA, Cryo, Brush, BAL, Fiducial)
            1: "Procedure: Ion Bronchoscopy Lingula.\nTarget: 23mm nodule (LB5).\nNav: Ion, rEBUS (concentric), CBCT.\nActions:\n- TBNA (21G): 4 passes.\n- Cryobiopsy (1.1mm): 5 samples.\n- Brush: 2 samples.\n- BAL: 40cc.\n- Fiducial: 1 gold marker.\nROSE: Granulomatous inflammation.\nComplications: None.",
            2: "PROCEDURE NOTE: Ms. Rodriguez presented for biopsy of a 23mm Lingular nodule. Under general anesthesia, the Ion robotic platform was utilized for navigation to the inferior lingula (LB5). Radial EBUS showed a concentric view; CBCT confirmed position. We performed multimodal sampling including TBNA (21G), cryobiopsy (1.1mm), and brushing. A fiducial marker was placed for potential SBRT. BAL was also collected. ROSE findings were consistent with granulomatous inflammation.",
            3: "Coding Summary:\n- 31626: Fiducial (Primary).\n- 31629: TBNA.\n- 31628: Cryobiopsy.\n- 31623: Brush.\n- 31624: BAL.\n- 31627: Navigation.\n- 31654: EBUS.\nLocation: Lingula. ROSE: Granulomas.",
            4: "Procedure: Lingula Biopsy\nPatient: Rebecca Rodriguez\nAttending: Dr. Williams\n\n1. GA/ETT.\n2. Ion Nav to LB5.\n3. rEBUS (Concentric) / CBCT confirm.\n4. TBNA x4.\n5. Cryo x5.\n6. Fiducial placed.\n7. Brush x2.\n8. BAL performed.\n9. ROSE: Granulomatous.",
            5: "rebecca rodriguez 11/16/25 lingula nodule 23mm ion robotic bronchoscopy reg error 3.0mm navigated to lb5 radial ebus concentric. did tbna 21g x4 cryo 1.1mm x5 brush x2 and a wash. put in a fiducial marker. rose showed granulomas so might not be cancer. no bleeding patient fine.",
            6: "A robotic bronchoscopy was performed for a 23mm Lingula nodule. Navigation to the Inferior Lingula (LB5) was achieved with the Ion system. Confirmation via rEBUS (concentric) and CBCT. Sampling included TBNA, cryobiopsy, brushing, and BAL. A fiducial marker was placed. ROSE indicated granulomatous inflammation. The patient was discharged stable.",
            7: "[Indication]\n23mm Lingula nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB5. rEBUS/CBCT confirmation.\nProcedures:\n- TBNA\n- Cryobiopsy\n- Brushing\n- BAL\n- Fiducial placement\n[Plan]\nFollow-up results.",
            8: "Ms. Rodriguez underwent a biopsy of a 23mm nodule in her lingula. We navigated the robotic catheter to the site and confirmed it with imaging. We took extensive samples using needles, cryoprobes, and brushes, and also washed the area. We placed a gold marker as well. The initial results suggest inflammation (granulomas) rather than cancer, but we will await the final report.",
            9: "Procedure: Robotic airway exploration.\nSite: Lingular nodule.\nActions: Guided catheter to inferior lingula. Verified via imaging. Performed aspiration, cryo-extraction, brushing, and lavage. Implanted a fiducial. \nROSE: Granulomatous features."
        },
        6: { # Note 6: Taylor, Donald (LLL Nodule: Ion, TBNA, Cryo, Brush, BAL, Fiducial)
            1: "Procedure: Ion Bronchoscopy LLL.\nTarget: 9mm nodule (LB9).\nNav: Ion, rEBUS (adjacent), CBCT.\nActions:\n- TBNA (21G): 6 passes.\n- Cryobiopsy (1.7mm): 5 samples.\n- Fiducial: 1 gold marker.\n- Brush: 2 samples.\n- BAL: 60cc.\nROSE: Squamous cell carcinoma.\nComplications: None.",
            2: "OPERATIVE REPORT: Mr. Taylor underwent robotic bronchoscopy for a solitary 9mm LLL nodule. Navigation to the lateral-basal segment (LB9) was achieved via the Ion system. Despite the small size, rEBUS (adjacent) and CBCT provided confirmation. We obtained diagnostic tissue via TBNA (21G), cryobiopsy (1.7mm), and brushing. A fiducial was placed to guide therapy. BAL was performed. ROSE confirmed squamous cell carcinoma.",
            3: "CPT Codes:\n- 31626: Fiducial.\n- 31629: TBNA.\n- 31628: Cryobiopsy.\n- 31623: Brush.\n- 31624: BAL.\n- 31627: Nav.\n- 31654: EBUS.\nTarget: 9mm LLL nodule. ROSE: Positive for malignancy.",
            4: "Resident Note\nPatient: Donald Taylor\nSite: LLL Nodule (9mm)\n\n- GA induced.\n- Ion Nav to LB9.\n- rEBUS: Adjacent.\n- CBCT: Confirmed.\n- TBNA x6.\n- Cryo x5.\n- Fiducial placed.\n- Brush x2.\n- BAL done.\n- ROSE: Squamous cell CA.",
            5: "donald taylor 8/26/25 lll nodule small 9mm used ion robot nav to lb9 radial ebus adjacent cone beam ct confirmed. did tbna 21g cryo 1.7mm brush and wash. placed a fiducial marker. rose came back squamous cell carcinoma. no complications discharge planned.",
            6: "The patient underwent general anesthesia for Ion robotic bronchoscopy of a 9mm LLL nodule. Navigation to the Lateral-Basal segment was confirmed with rEBUS and Cone Beam CT. Biopsies included TBNA, cryobiopsy, and brushing. A fiducial marker was placed. BAL was collected. ROSE was positive for squamous cell carcinoma.",
            7: "[Indication]\n9mm LLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LB9. Confirmed via rEBUS/CBCT.\nIntervention:\n- TBNA\n- Cryobiopsy\n- Fiducial\n- Brush\n- BAL\n[Plan]\nOncology referral.",
            8: "Mr. Taylor had a small 9mm nodule in his lower left lung. We used the robotic system to navigate to the lateral-basal segment. We confirmed the location with ultrasound and CT. We took multiple samples using a needle, freezing probe, and brush, and washed the area. We also placed a gold marker. The pathologist confirmed squamous cell carcinoma on site.",
            9: "Procedure: Robotic bronchoscopic biopsy.\nTarget: LLL lesion.\nTechnique: Steered to lateral-basal segment. Validated via multimodality imaging. Sampled via aspiration, cryo-retrieval, and brushing. Lavaged segment. Deployed fiducial. \nDiagnosis: Squamous cell carcinoma."
        },
        7: { # Note 7: Sanchez, Karen (RLL Nodule: Ion, TBNA, Cryo)
            1: "Procedure: Ion Bronchoscopy RLL.\nTarget: 30mm nodule (RB10).\nNav: Ion, rEBUS (adjacent), CBCT.\nBiopsy:\n- TBNA (23G): 5 passes.\n- Cryobiopsy (1.7mm): 5 samples.\nROSE: Squamous cell carcinoma.\nComplications: None.",
            2: "PROCEDURE NOTE: Ms. Sanchez presented with a Lung-RADS 4B nodule in the RLL. Robotic navigation (Ion) guided the catheter to the posterior-basal segment (RB10). rEBUS showed an adjacent signal; CBCT confirmed placement. We performed TBNA (23G) and transbronchial cryobiopsy (1.7mm). Samples were adequate. ROSE confirmed malignant cells consistent with squamous cell carcinoma.",
            3: "Billing:\n- 31629: TBNA (Primary).\n- 31628: Cryobiopsy.\n- 31627: Nav.\n- 31654: EBUS.\nLocation: RLL (30mm). ROSE: Positive.",
            4: "Procedure: RLL Biopsy\nPatient: Karen Sanchez\nAttending: Dr. Lee\n\n1. GA/ETT.\n2. Ion Nav to RB10.\n3. rEBUS: Adjacent.\n4. CBCT confirm.\n5. TBNA x5 (23G).\n6. Cryo x5 (1.7mm).\n7. ROSE: SCC.\n8. Extubated stable.",
            5: "karen sanchez 9/8/25 rll nodule 30mm 4b used ion robot nav to rb10 radial ebus adjacent cone beam ct confirmed tool in lesion. did 5 needle passes 23g and 5 cryo samples 1.7mm. rose said squamous cell ca. bleeding mild stopped fine.",
            6: "Under general anesthesia, Ion robotic bronchoscopy was performed for a 30mm RLL nodule. Navigation to the Posterior-Basal segment (RB10) was verified by rEBUS and CBCT. Sampling was performed via TBNA (23G) and cryobiopsy (1.7mm). ROSE confirmed squamous cell carcinoma. The patient was stable post-procedure.",
            7: "[Indication]\n30mm RLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to RB10. Confirmed rEBUS/CBCT.\nBiopsy:\n- TBNA\n- Cryobiopsy\n[Plan]\nRefer to Oncology.",
            8: "Ms. Sanchez underwent a biopsy of a 30mm nodule in her right lower lung. We used the robotic system to reach the posterior-basal segment. Imaging confirmed we were at the target. We took samples with a needle and a freezing probe. The rapid test confirmed squamous cell carcinoma. She recovered well.",
            9: "Procedure: Robotic airway sampling.\nFocus: RLL mass.\nMethods: Navigated to posterior-basal segment. Verified with sonography/tomography. Performed aspiration and cryo-biopsy. \nResult: Malignancy confirmed."
        },
        8: { # Note 8: Garcia, Stephanie (RML Nodule: Ion, TBNA, Cryo, BAL)
            1: "Procedure: Ion Bronchoscopy RML.\nTarget: 25mm nodule (RB5).\nNav: Ion, rEBUS (adjacent), CBCT.\nBiopsy:\n- TBNA (21G): 7 passes.\n- Cryobiopsy (1.1mm): 3 samples.\n- BAL: 80cc.\nROSE: Suspicious for malignancy.\nComplications: None.",
            2: "OPERATIVE NOTE: Ms. Garcia underwent robotic bronchoscopy for a 25mm RML nodule. The Ion system was utilized to navigate to the medial segment (RB5). rEBUS showed an adjacent lesion; CBCT confirmed tool-in-lesion. We performed TBNA (21G) and cryobiopsy (1.1mm). BAL was also obtained. ROSE revealed atypical cells suspicious for malignancy.",
            3: "Codes:\n- 31629: TBNA.\n- 31628: Cryo.\n- 31624: BAL.\n- 31627: Nav.\n- 31654: EBUS.\nSite: RML. Result: Suspicious.",
            4: "Resident Note\nPatient: Stephanie Garcia\nSite: RML Nodule\n\n- GA/ETT.\n- Ion Nav to RB5.\n- rEBUS: Adjacent.\n- CBCT: Confirmed.\n- TBNA x7.\n- Cryo x3.\n- BAL performed.\n- ROSE: Suspicious.\n- Stable.",
            5: "stephanie garcia 10/15/25 rml nodule 25mm lung rads 4x used ion robot nav to rb5 radial ebus adjacent cone beam ct good. did tbna 21g x7 cryo 1.1mm x3 and a wash. rose suspicious for cancer atypical cells. discharged.",
            6: "A robotic bronchoscopy was performed on a 25mm RML nodule. Navigation to the Medial segment (RB5) was achieved with the Ion system. Verification via rEBUS and CBCT. Samples were taken via TBNA, cryobiopsy, and BAL. ROSE was suspicious for malignancy. No complications occurred.",
            7: "[Indication]\n25mm RML nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to RB5. rEBUS/CBCT confirmation.\nProcedures:\n- TBNA\n- Cryobiopsy\n- BAL\n[Plan]\nFollow-up pathology.",
            8: "Ms. Garcia had a 25mm nodule in her right middle lobe. We used the robotic catheter to navigate to the medial segment. We confirmed the position with imaging. We took needle biopsies and freezing probe samples, and washed the lung segment. The initial results were suspicious for cancer. She was discharged home safely.",
            9: "Procedure: Robotic bronchoscopic assessment.\nTarget: RML lesion.\nAction: Guided to medial segment. Confirmed via imaging. Sampled via aspiration and cryo-technique. Lavaged area. \nFinding: Suspicious cytology."
        },
        9: { # Note 9: Moore, Stephanie (RML Nodule: Ion, TBNA, Cryo, BAL)
            1: "Procedure: Ion Bronchoscopy RML.\nTarget: 25mm nodule (RB5).\nNav: Ion, rEBUS (adjacent), Fluoroscopy.\nBiopsy:\n- TBNA (21G/23G): 7 passes.\n- Cryobiopsy (1.1mm): 4 samples.\n- BAL: 40cc.\nROSE: Granulomatous inflammation.\nComplications: None.",
            2: "PROCEDURE NOTE: Ms. Moore underwent robotic bronchoscopy for a 25mm RML nodule. Navigation to the medial segment (RB5) was performed with the Ion system. rEBUS showed an adjacent lesion. Positioning was verified with fluoroscopy (Shape-sensing lock). We performed TBNA (21G/23G) and cryobiopsy (1.1mm). BAL was collected. ROSE indicated granulomatous inflammation.",
            3: "Coding:\n- 31629: TBNA.\n- 31628: Cryo.\n- 31624: BAL.\n- 31627: Nav.\n- 31654: EBUS.\nNote: Fluoroscopy used for verification instead of CBCT in this instance.",
            4: "Procedure: RML Biopsy\nPatient: Stephanie Moore\nAttending: Dr. Brown\n\n1. GA/ETT.\n2. Ion Nav to RB5.\n3. rEBUS: Adjacent.\n4. Locked catheter (Shape-sensing).\n5. TBNA x7.\n6. Cryo x4.\n7. BAL.\n8. ROSE: Granulomas.\n9. Stable.",
            5: "stephanie moore 8/11/25 rml nodule 25mm ion robot nav to rb5 radial ebus adjacent. locked the arm. did tbna mixed needles and cryo 1.1mm x4 plus a wash. rose showed granulomas so probably benign. no bleeding.",
            6: "Ion robotic bronchoscopy was performed for a 25mm RML nodule. Navigation to the Medial segment (RB5) used shape-sensing technology. rEBUS showed an adjacent signal. Biopsies included TBNA (7 passes), cryobiopsy (4 samples), and BAL. ROSE showed granulomatous inflammation. The patient tolerated the procedure well.",
            7: "[Indication]\n25mm RML nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to RB5. rEBUS confirmation.\nSampling:\n- TBNA\n- Cryobiopsy\n- BAL\n[Plan]\nFollow-up.",
            8: "Ms. Moore underwent a biopsy of a 25mm nodule in her right middle lobe. We used the robotic system to navigate to the correct segment and locked the catheter in place. We took samples using needles and a freezing probe, and washed the area. The preliminary results showed granulomas, which suggests inflammation. She recovered well.",
            9: "Procedure: Robotic airway interrogation.\nFocus: RML mass.\nTechnique: Steered to medial segment. Verified via sonography. Sampled via aspiration and cryo-extraction. Lavaged segment. \nResult: Granulomatous changes."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns extracted base data for the 10 source notes to maintain consistency.
    Names list contains 9 new names for the 9 variations.
    """
    return [
        {"idx": 0, "orig_name": "Steven Adams", "orig_age": 65, "names": ["Robert Redford", "William Black", "James Green", "Michael White", "David Brown", "Richard Gray", "Thomas Blue", "Charles Gold", "Joseph Silver"]},
        {"idx": 1, "orig_name": "Dorothy Hill", "orig_age": 61, "names": ["Mary Jones", "Patricia Davis", "Jennifer Miller", "Elizabeth Wilson", "Linda Moore", "Barbara Taylor", "Susan Anderson", "Margaret Thomas", "Dorothy Jackson"]},
        {"idx": 2, "orig_name": "Linda Young", "orig_age": 60, "names": ["Sarah White", "Karen Harris", "Nancy Martin", "Lisa Thompson", "Betty Garcia", "Sandra Martinez", "Ashley Robinson", "Kimberly Clark", "Donna Rodriguez"]},
        {"idx": 3, "orig_name": "Jonathan Jones", "orig_age": 53, "names": ["Christopher Lewis", "Daniel Lee", "Paul Walker", "Mark Hall", "Donald Allen", "George Young", "Kenneth Hernandez", "Steven King", "Edward Wright"]},
        {"idx": 4, "orig_name": "Daniel Mitchell", "orig_age": 50, "names": ["Brian Scott", "Ronald Torres", "Anthony Nguyen", "Kevin Hill", "Jason Flores", "Matthew Green", "Gary Adams", "Timothy Nelson", "Jose Baker"]},
        {"idx": 5, "orig_name": "Rebecca Rodriguez", "orig_age": 81, "names": ["Helen Carter", "Deborah Mitchell", "Jessica Perez", "Sharon Roberts", "Cynthia Turner", "Kathleen Phillips", "Amy Campbell", "Shirley Parker", "Angela Evans"]},
        {"idx": 6, "orig_name": "Donald Taylor", "orig_age": 71, "names": ["Frank Edwards", "Scott Collins", "Eric Stewart", "Stephen Sanchez", "Andrew Morris", "Raymond Rogers", "Gregory Reed", "Joshua Cook", "Jerry Morgan"]},
        {"idx": 7, "orig_name": "Karen Sanchez", "orig_age": 51, "names": ["Melissa Bell", "Brenda Murphy", "Amy Bailey", "Anna Rivera", "Rebecca Cooper", "Virginia Richardson", "Kathleen Cox", "Pamela Howard", "Martha Ward"]},
        {"idx": 8, "orig_name": "Stephanie Garcia", "orig_age": 66, "names": ["Debra Torres", "Amanda Peterson", "Stephanie Gray", "Carolyn Ramirez", "Christine James", "Marie Watson", "Janet Brooks", "Catherine Kelly", "Frances Sanders"]},
        {"idx": 9, "orig_name": "Stephanie Moore", "orig_age": 53, "names": ["Ann Price", "Joyce Bennett", "Diane Wood", "Alice Barnes", "Julie Ross", "Heather Henderson", "Teresa Coleman", "Doris Jenkins", "Gloria Perry"]}
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
            
            # Deep copy the original note structure to preserve all extraction fields
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Get the variation text for this note index and style
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (should not happen with full dictionary)
                note_entry["note_text"] = f"VARIATION_MISSING_FOR_NOTE_{idx}_STYLE_{style_num}"

            # Update registry_entry fields to match the variation
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
    output_filename = output_dir / "synthetic_ion_robotic_notes_part_087.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()