import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_063.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations for the robotic bronchoscopy dataset.
    Structure: Note_Index (0-14) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # RAB001: 62M, LLL nodule, Ion
            1: "Indication: LLL nodule.\nProcedure: Robotic bronchoscopy, radial EBUS, biopsy.\nFindings: 18mm lesion, tool-in-lesion confirmed via CBCT.\nAction: Forceps bx and brushings taken. Minimal bleeding.\nPlan: Discharge.",
            2: "OPERATIVE REPORT: The patient presented with a suspicious 1.8 cm left lower lobe nodule. Under general anesthesia, the Intuitive Ion robotic platform was utilized for navigation. Radial endobronchial ultrasound (REBUS) identified a concentric, heterogeneous lesion in the lateral basal segment. Cone-beam computed tomography (CBCT) verification ensured precise instrument placement. Transbronchial forceps biopsies and brushings were procured without significant hemorrhage. The airway remained patent upon conclusion.",
            3: "CPT 31627 (Navigational Bronchoscopy): Used Ion system for planning and guidance to LLL target.\nCPT 31654 (Radial EBUS): Confirmed peripheral lesion location (18mm).\nCPT 31628 (Lung Biopsy): Multiple transbronchial forceps samples obtained from single lobe.\nCPT 31623 (Brushing): Cellular sampling performed via catheter brush.",
            4: "Resident Note\nPatient: Case 01\nAttending: Dr. Nguyen\nProcedure: Ion Robotic Bronchoscopy\nSteps:\n1. Time out/GA.\n2. Ion registration (low error).\n3. Navigated to LLL lateral basal.\n4. REBUS: Concentric view.\n5. CBCT spin: Confirmed tool in lesion.\n6. Biopsies: Forceps x5, Brush x1.\n7. Tolerated well.",
            5: "patient 62 male here for robotic bronch lll nodule we used the ion system navigation was good radial ebus showed the lesion 18mm concentric view confirmed with the cone beam ct took biopsies with forceps and brush minimal bleeding patient woke up fine no pneumothorax on post op cxr",
            6: "Robotic navigational bronchoscopy with radial EBUS and transbronchial biopsy. The patient is a 62-year-old male with a left lower lobe nodule. General anesthesia was induced. The Ion catheter was navigated to the lateral basal segment. Radial EBUS showed a concentric 18 mm lesion. CBCT confirmed position. Biopsies and brushings were obtained. Minimal bleeding occurred. No complications.",
            7: "[Indication]\n1.8 cm LLL lateral basal nodule, suspicious for malignancy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon robotic navigation used. REBUS showed concentric lesion. CBCT confirmed tool-in-lesion. Forceps biopsy and brushing performed.\n[Plan]\nDischarge. Follow up pathology.",
            8: "The patient, a 62-year-old male, underwent a diagnostic robotic navigational bronchoscopy for a left lower lobe nodule. After induction of anesthesia, the Ion system was registered. We navigated to the target in the lateral basal segment, where radial EBUS confirmed a concentric lesion. Cone-beam CT was utilized to verify the tool was within the lesion. We then proceeded to take multiple forceps biopsies and brushings. There was only minimal bleeding, and the patient recovered without issues.",
            9: "Indication: LLL mass.\nTechnique: Robotic guidance (Ion), ultrasonic localization (REBUS), tissue sampling (forceps, brush).\nFindings: 18mm concentric abnormality.\nVerification: Volumetric imaging (CBCT).\nOutcome: Specimens harvested. Hemostasis achieved. No pneumothorax."
        },
        1: { # RAB002: 74F, RUL nodule, Ion
            1: "Dx: RUL nodule, susp cancer.\nProc: Ion bronch, REBUS, bx.\nFindings: 22mm eccentric lesion.\nAction: 6 bx, 2 brush. Oozing stopped w/ iced saline.\nResult: Hemostasis. Extubated.",
            2: "PROCEDURE NOTE: This 74-year-old female with a highly metabolic RUL nodule underwent robotic-assisted bronchoscopy. The Ion catheter was driven to the posterior segment of the right upper lobe. Radial EBUS imaging revealed an eccentric, heterogeneous 22 mm mass. Intraprocedural cone-beam CT confirmed the biopsy tool's position within the target. Extensive sampling via forceps and brush was conducted. Minor hemorrhage was managed successfully with cold saline lavage.",
            3: "Billing Codes: 31627 (Robotic Nav), 31654 (Peripheral EBUS), 31628 (Bx), 31623 (Brush).\nJustification: 2.2 cm RUL lesion required advanced navigation and imaging (CBCT) for accurate targeting. Multiple samples taken to ensure diagnostic yield for suspected primary lung cancer.",
            4: "Trainee Note\nPt: 74F\nAttending: Dr. Ortiz\nOp: Ion RUL Bx\n- GA/ETT.\n- Registered Ion.\n- Nav to RUL posterior.\n- REBUS: Eccentric 22mm.\n- CBCT: Good position.\n- Bx: 6 forceps, 2 brush.\n- Bleeding: Mild, stopped w/ saline.",
            5: "case 2 74 female rul nodule likely cancer ion system used for biopsy reg was auto complete nav to posterior segment rebus showed eccentric lesion cbct confirmed we took 6 bites with forceps and 2 brushes little bit of oozing used iced saline stopped fine extubated in room",
            6: "Robotic navigational bronchoscopy, radial EBUS, and biopsy. 74-year-old female with RUL nodule. Ion system used. Radial EBUS showed 22 mm eccentric lesion. CBCT used for verification. Forceps biopsies and brushings obtained. Mild bleeding controlled. Patient extubated and stable.",
            7: "[Indication]\nEnlarging 2.2 cm RUL nodule, SUV 8.1.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon navigation to RUL posterior. REBUS eccentric. CBCT confirmation. 6 biopsies, 2 brushings. Hemostasis achieved.\n[Plan]\nExpedited path review. Staging if malignant.",
            8: "A 74-year-old woman presented with a suspicious right upper lobe nodule. We performed a robotic bronchoscopy using the Ion system. Upon reaching the posterior segment, radial EBUS revealed an eccentric lesion. We used cone-beam CT to confirm our tool was inside the lesion before taking six biopsies and two brushings. Mild bleeding was noted and treated with iced saline. The patient was extubated without complication.",
            9: "Indication: RUL neoplasm.\nMethod: Robotic steering, ultrasonic scanning, tissue acquisition.\nFindings: 22mm irregular mass.\nVerification: 3D fluoroscopy.\nAction: Harvested tissue via forceps and brush. Hemorrhage arrested with saline. Airway patent."
        },
        2: { # RAB003: 59F, RML nodule, Ion
            1: "Indication: RML nodule.\nProc: Ion bronch, REBUS, bx.\nFindings: 12mm adjacent lesion.\nAction: 5 forceps bx. Augmented fluoro used.\nPlan: Discharge.",
            2: "OPERATIVE SUMMARY: The patient underwent elective robotic bronchoscopy for a right middle lobe nodule. The Intuitive Ion system facilitated navigation to the lateral segment. Radial EBUS identified a 12 mm lesion adjacent to the airway. Augmented fluoroscopic guidance verified catheter placement. Five transbronchial biopsy specimens were obtained. There was no active hemorrhage upon completion.",
            3: "Service: Robotic Bronchoscopy (31627), EBUS (31654), Biopsy (31628).\nTarget: RML lateral segment.\nImaging: Augmented fluoroscopy used to refine position (no CBCT).\nSamples: 5 forceps biopsies obtained.",
            4: "Resident Procedure Note\nPatient: Case 03\nSite: RML\nProcedure: Ion Bx\n- Plan loaded, reg complete.\n- Nav to RML lateral.\n- REBUS: Adjacent 12mm.\n- Fluoro check: Good.\n- Bx x5.\n- No bleeding.\n- Stable.",
            5: "59 female incidental rml nodule robotic biopsy done today ion platform navigation to rml lateral segment rebus showed adjacent lesion 12mm augmented fluoro looked good taken 5 biopsies minimal bleeding discharged home after observation",
            6: "Robotic navigational bronchoscopy with biopsy. Patient with 1.2 cm RML nodule. Ion system used. REBUS showed adjacent lesion. Augmented fluoroscopy confirmed position. Five forceps biopsies obtained. No complications. Patient discharged.",
            7: "[Indication]\n1.2 cm RML nodule, mildly avid.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to RML. REBUS adjacent. Augmented fluoro confirmation. 5 biopsies taken. No brushing.\n[Plan]\nDischarge. Watch/wait vs tx based on path.",
            8: "We performed a robotic biopsy on a 59-year-old female with a right middle lobe nodule. Using the Ion system, we navigated to the lateral segment where radial EBUS showed an adjacent 12 mm lesion. We used augmented fluoroscopy to confirm the tool's position. Five biopsies were taken with minimal bleeding. The patient was discharged after the procedure.",
            9: "Indication: RML opacity.\nTechnique: Robotic maneuvering, ultrasonic detection, tissue extraction.\nFindings: 12mm parobronchial lesion.\nConfirmation: Enhanced fluoroscopy.\nAction: Collected 5 specimens. No hemorrhage. Recovery uneventful."
        },
        3: { # RAB004: 67M, LUL nodule, Ion
            1: "Dx: LUL nodule, mediastinal nodes.\nProc: Ion bronch, REBUS, TBNA, forceps bx.\nFindings: 9mm concentric lesion.\nAction: Forceps bx and TBNA performed.\nResult: Mild oozing, resolved.",
            2: "PROCEDURE REPORT: This 67-year-old male with a left upper lobe nodule and lymphadenopathy underwent robotic diagnostic bronchoscopy. The Ion catheter was navigated to the apicoposterior segment. Radial EBUS demonstrated a small 9 mm concentric lesion. Forceps biopsies were obtained, followed by transbronchial needle aspiration (TBNA) of the peribronchial tissue. Hemostasis was secured.",
            3: "CPT 31629 (TBNA): Primary code for needle aspiration of peribronchial tissue.\nCPT 31627 (Nav): Robotic guidance.\nCPT 31654 (REBUS): Localization.\nNote: Forceps biopsy (31628) bundled/not separately billed if same site as TBNA depending on payer, but documented here as performed.",
            4: "Trainee Note\nPt: 67M\nOp: Ion LUL Bx + TBNA\n- Nav to LUL apicoposterior.\n- REBUS: 9mm concentric.\n- Forceps Bx taken.\n- TBNA needle used for peribronchial sample.\n- No CBCT.\n- Mild bleeding, stopped.",
            5: "case 04 67m lul nodule and nodes robotic bronch with ion system nav to apicoposterior segment rebus showed small 9mm lesion did forceps biopsy and then tbna needle passes too mild oozing iced saline used no complications",
            6: "Robotic navigational bronchoscopy with TBNA and biopsy. LUL nodule. Ion system used. REBUS showed 9 mm concentric lesion. Forceps biopsies and TBNA performed. Mild oozing controlled. Patient tolerated well.",
            7: "[Indication]\n9mm LUL nodule, peribronchial tissue.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to LUL. REBUS concentric. Forceps bx and TBNA performed. No CBCT.\n[Plan]\nPath review. Staging if malignant.",
            8: "A 67-year-old male underwent robotic bronchoscopy for a left upper lobe nodule. We navigated to the apicoposterior segment using the Ion system. Radial EBUS showed a small concentric lesion. We performed both forceps biopsies and transbronchial needle aspiration (TBNA). Mild bleeding was controlled with iced saline. The procedure was completed without complications.",
            9: "Indication: LUL lesion.\nProcedure: Robotic piloting, ultrasonic verification, needle aspiration, forceps sampling.\nFindings: 9mm target.\nAction: Acquired tissue via needle and forceps. Hemostasis confirmed."
        },
        4: { # RAB005: 71M, RLL nodule, ILD, Ion Cryo
            1: "Indication: RLL nodule, ILD.\nProc: Ion bronch, REBUS, Cryobiopsy.\nFindings: 25mm heterogeneous lesion.\nAction: 2 cryo samples, 1 brush. Balloon tamponade used.\nPlan: Admit for obs.",
            2: "OPERATIVE NOTE: The patient, a 71-year-old male with interstitial lung disease, presented with a right lower lobe nodule. Robotic bronchoscopy was utilized for navigation. Radial EBUS identified a 25 mm lesion in the superior segment. A cryoprobe was introduced, and two transbronchial cryobiopsies were obtained to maximize diagnostic yield. Moderate bleeding occurred, necessitating balloon tamponade. No pneumothorax was detected post-procedure.",
            3: "Billing: 31628 (Lung Biopsy - Primary for Cryo if single lobe).\n31627 (Nav), 31654 (REBUS), 31623 (Brush).\nNote: Cryobiopsy used for nodule diagnosis in setting of ILD.",
            4: "Resident Note\nPt: 71M, ILD\nProc: Ion RLL Cryobiopsy\n- Nav to RLL superior.\n- REBUS: 25mm.\n- Blocker placed.\n- Cryo x2 (1.7mm probe).\n- Brush x1.\n- Mod bleeding -> Balloon up.\n- Admitted.",
            5: "patient 71 male with fibrosis and rll nodule robotic bronch today used ion nav to rll superior segment rebus 25mm lesion used the cryoprobe for biopsy 2 passes moderate bleeding had to use the balloon blocker stopped eventually admitted for observation",
            6: "Robotic navigational bronchoscopy with cryobiopsy. Indication: RLL nodule in ILD. Ion system used. REBUS showed 25 mm lesion. Two cryobiopsy samples taken. Moderate bleeding controlled with balloon. No pneumothorax. Admitted.",
            7: "[Indication]\n2.5 cm RLL nodule in ILD.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to RLL. REBUS confirmed lesion. 2 cryobiopsies taken. Balloon tamponade for bleeding.\n[Plan]\nAdmit overnight. CXR.",
            8: "This 71-year-old male with ILD and a right lower lobe nodule underwent robotic bronchoscopy. We navigated to the lesion using the Ion system and confirmed it with radial EBUS. We obtained two cryobiopsy samples and one brushing. Moderate bleeding was managed with a bronchial blocker. The patient was admitted for observation.",
            9: "Indication: RLL mass in fibrotic lung.\nTechnique: Robotic guidance, ultrasonic check, cryo-adhesion sampling.\nFindings: 25mm opacity.\nAction: Retrieved frozen specimens. Tamponade applied for hemorrhage. Hospitalization required."
        },
        5: { # RAB006: 64F, LLL nodule, Ion Partial Reg
            1: "Indication: LLL nodule.\nProc: Ion bronch, Partial Reg.\nFindings: 15mm eccentric lesion.\nAction: 4 bx, 1 brush. Augmented fluoro.\nResult: No bleeding. Discharge.",
            2: "PROCEDURE RECORD: Ms. [Name] underwent robotic bronchoscopy for a left lower lobe nodule. To optimize efficiency, a partial ipsilateral registration strategy was employed with the Ion system. Navigation to the basilar segment was successful. Radial EBUS demonstrated an eccentric 15 mm lesion. Tool-in-lesion was confirmed via augmented fluoroscopy. Biopsies and brushings were obtained without incident.",
            3: "Code 31627: Navigational bronchoscopy (Partial registration is sufficient if target reached).\nCode 31654: EBUS.\nCode 31628: Transbronchial biopsy.\nCode 31623: Brushing.\nOutcome: Successful sampling of 1.5cm nodule.",
            4: "Trainee Note\nPt: 64F\nOp: Ion LLL Bx (Partial Reg)\n- Partial reg (left side only).\n- Nav to LLL basilar.\n- REBUS: 15mm eccentric.\n- Aug Fluoro: Confirmed.\n- Bx x4, Brush x1.\n- No complications.",
            5: "64 female lll nodule 1.5cm robotic bronch ion system partial registration used worked fine navigated to basilar segment rebus showed lesion eccentric augmented fluoro used for confirmation took 4 biopsies and a brush no bleeding sent home",
            6: "Robotic navigational bronchoscopy with partial registration. LLL nodule. Ion system used. Partial registration performed. REBUS showed 15 mm eccentric lesion. Augmented fluoroscopy used. Biopsies and brushings obtained. No complications.",
            7: "[Indication]\n1.5 cm LLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon partial registration. Nav to LLL. REBUS eccentric. Aug fluoro confirmation. 4 biopsies, 1 brush.\n[Plan]\nDischarge. Path f/u.",
            8: "A 64-year-old female underwent robotic bronchoscopy for a left lower lobe nodule. We used a partial registration strategy with the Ion system, which was successful. Radial EBUS showed an eccentric lesion, and augmented fluoroscopy confirmed the tool's position. We took four biopsies and one brushing with minimal bleeding. The patient was discharged.",
            9: "Indication: LLL nodule.\nMethod: Robotic steering (partial mapping), ultrasonic detection, tissue sampling.\nFindings: 15mm eccentric target.\nVerification: Enhanced fluoroscopy.\nAction: Acquired specimens. No hemorrhage."
        },
        6: { # RAB007: 58M, RUL nodule, Ion Drift
            1: "Indication: RUL nodule.\nProc: Ion bronch, Re-registration.\nFindings: 19mm concentric lesion.\nAction: Nav drift noted -> Re-registered. 4 bx, brush.\nResult: CBCT confirmed. No bleeding.",
            2: "OPERATIVE SUMMARY: The patient underwent robotic bronchoscopy for a right upper lobe nodule. Intraoperatively, registration drift was noted, necessitating re-registration with tertiary landmarks. Following correction, the catheter was successfully navigated to the RUL apical segment. Radial EBUS and cone-beam CT confirmed the target. Biopsies and brushings were obtained without further issue.",
            3: "CPT 31627: Navigational bronchoscopy (includes registration and correction of drift).\nCPT 31654: EBUS.\nCPT 31628: Biopsy.\nCPT 31623: Brushing.\nNote: Extra time for re-registration included in facility time, not extra CPT.",
            4: "Resident Note\nPt: 58M\nOp: Ion RUL Bx\n- Issue: CT-to-body divergence (drift).\n- Fix: Re-registered.\n- Nav to RUL apical.\n- REBUS: 19mm concentric.\n- CBCT: Tool in lesion.\n- Bx x4, Brush x1.\n- Good hemostasis.",
            5: "case 07 58m rul nodule ion system used we had some drift mid case had to re register then it was fine went to apical segment rebus showed 19mm lesion cbct confirmed biopsy and brush taken mild bleeding stopped discharge home",
            6: "Robotic navigational bronchoscopy with re-registration. RUL nodule. Ion system used. Drift noted and corrected. REBUS showed 19 mm concentric lesion. CBCT confirmed position. Biopsies and brushings obtained. No active bleeding.",
            7: "[Indication]\n1.9 cm RUL apical nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav with re-registration due to drift. REBUS concentric. CBCT confirmation. Forceps bx and brush.\n[Plan]\nDischarge. Path review.",
            8: "We performed a robotic bronchoscopy on a 58-year-old male with a right upper lobe nodule. We encountered registration drift during the procedure and had to re-register the system. Once corrected, we navigated to the apical segment where radial EBUS and CBCT confirmed the lesion. We obtained multiple biopsies and brushings. The patient was discharged home.",
            9: "Indication: RUL opacity.\nProcedure: Robotic guidance (re-calibrated), ultrasonic localization, tissue harvesting.\nFindings: 19mm target.\nVerification: 3D imaging.\nAction: Collected specimens. No complications."
        },
        7: { # RAB008: 63M, RLL nodule, Monarch
            1: "Indication: RLL nodule.\nProc: Monarch bronch, REBUS, bx.\nFindings: 14mm concentric lesion.\nAction: 5 bx, 1 brush. CBCT used.\nResult: No bleeding. Discharge.",
            2: "PROCEDURE REPORT: This 63-year-old male with a right lower lobe nodule underwent robotic-assisted bronchoscopy using the Monarch platform. The robotic sheath was advanced to the basilar segment. Radial EBUS visualized a concentric 14 mm lesion. Cone-beam CT provided confirmation of catheter placement. Forceps biopsies and brushings were collected. The patient tolerated the procedure well.",
            3: "Codes: 31627 (Monarch Nav), 31654 (EBUS), 31628 (Bx), 31623 (Brush).\nPlatform: Auris Monarch.\nImaging: CBCT used for verification.\nTarget: RLL basilar.",
            4: "Trainee Note\nPt: 63M\nAttending: Dr. Flores\nSystem: Monarch\n- Reg completed.\n- Nav to RLL basilar.\n- REBUS: 14mm concentric.\n- CBCT: Tool in lesion.\n- Bx x5, Brush x1.\n- Hemostasis good.",
            5: "patient 63 male rll nodule monarch robot used for this one nav to basilar segment rebus showed 14mm lesion concentric cbct confirmed position took 5 biopsies and a brush no bleeding patient did well",
            6: "Robotic navigational bronchoscopy (Monarch) with biopsy. RLL nodule. Monarch system used. REBUS showed 14 mm concentric lesion. CBCT confirmed position. Forceps biopsies and brushings obtained. No complications.",
            7: "[Indication]\n1.4 cm RLL basilar nodule.\n[Anesthesia]\nGeneral.\n[Description]\nMonarch nav to RLL. REBUS concentric. CBCT confirmation. 5 biopsies, 1 brush.\n[Plan]\nDischarge. Tumor board if malignant.",
            8: "A 63-year-old male underwent robotic bronchoscopy using the Monarch platform for a right lower lobe nodule. We navigated to the basilar segment and confirmed the lesion with radial EBUS and cone-beam CT. We obtained five biopsies and one brushing. The patient was discharged without complications.",
            9: "Indication: RLL nodule.\nTechnique: Monarch robotic piloting, ultrasonic scanning, tissue acquisition.\nFindings: 14mm concentric target.\nVerification: Volumetric CT.\nAction: Harvested tissue. No hemorrhage."
        },
        8: { # RAB009: 52F, Lingula nodule, Monarch
            1: "Indication: Lingular nodule.\nProc: Monarch bronch, REBUS, bx.\nFindings: 10mm subpleural lesion.\nAction: 4 bx. Aug fluoro used.\nResult: No bleeding. Discharge.",
            2: "OPERATIVE NOTE: The patient underwent Monarch robotic bronchoscopy for a small lingular nodule. Navigation was successful to the subpleural space. Radial EBUS identified an adjacent 10 mm lesion. Augmented fluoroscopy was utilized to confirm tool-in-lesion status. Transbronchial biopsies were obtained without complication.",
            3: "CPT 31627 (Monarch Nav), 31654 (EBUS), 31628 (Bx).\nNote: No brushing (31623) performed. No CBCT used, only augmented fluoroscopy.",
            4: "Resident Note\nPt: 52F\nOp: Monarch Lingula Bx\n- Nav to Lingula.\n- REBUS: Adjacent 10mm.\n- Aug Fluoro: Confirmed.\n- Bx x4.\n- No brush.\n- No bleeding.",
            5: "52 female lingular nodule 1cm monarch robot used nav to lingula rebus showed adjacent lesion subpleural used augmented fluoro to check position took 4 biopsies no brush needed patient discharged",
            6: "Robotic navigational bronchoscopy (Monarch). Lingular nodule. Monarch system used. REBUS showed 10 mm adjacent lesion. Augmented fluoroscopy confirmed position. Four biopsies obtained. No complications.",
            7: "[Indication]\n1.0 cm Lingular nodule.\n[Anesthesia]\nGeneral.\n[Description]\nMonarch nav to Lingula. REBUS adjacent. Aug fluoro confirmation. 4 biopsies.\n[Plan]\nDischarge. Path f/u.",
            8: "We performed a robotic bronchoscopy on a 52-year-old female with a lingular nodule using the Monarch platform. Navigation led us to a subpleural location where radial EBUS showed an adjacent 10 mm lesion. Augmented fluoroscopy confirmed the position. We took four biopsies with no complications.",
            9: "Indication: Lingular opacity.\nProcedure: Monarch robotic steering, ultrasonic detection, tissue sampling.\nFindings: 10mm adjacent target.\nVerification: Enhanced fluoroscopy.\nAction: Acquired specimens. Recovery uneventful."
        },
        9: { # RAB010: 69M, RUL mass, Monarch BAL
            1: "Indication: RUL mass.\nProc: Monarch bronch, BAL, bx.\nFindings: 3cm eccentric mass.\nAction: Bx and BAL performed. CBCT used.\nResult: Minimal bleeding.",
            2: "PROCEDURE REPORT: This 69-year-old male with a central RUL mass underwent robotic bronchoscopy via the Monarch system. Navigation to the target was achieved. Radial EBUS revealed an eccentric mass signal. Forceps biopsies were obtained, followed by bronchoalveolar lavage (BAL) of the segment. Cone-beam CT verified tool placement. Hemostasis was maintained.",
            3: "CPT 31627 (Nav), 31654 (EBUS), 31628 (Bx), 31624 (BAL).\nJustification: Central mass required biopsy and washings for diagnosis. CBCT used for confirmation.",
            4: "Trainee Note\nPt: 69M\nOp: Monarch RUL Bx + BAL\n- Nav to RUL central.\n- REBUS: Eccentric mass.\n- Bx x4.\n- BAL x1.\n- CBCT: Tool in lesion.\n- Minimal bleeding.",
            5: "case 10 69m rul mass monarch system used nav to central rul rebus showed mass eccentric took biopsies and did a lavage bal cbct confirmed position bleeding controlled suction discharge",
            6: "Robotic navigational bronchoscopy (Monarch) with BAL and biopsy. RUL mass. Monarch system used. REBUS showed eccentric mass. Forceps biopsies and BAL performed. CBCT confirmed position. Minimal bleeding.",
            7: "[Indication]\n3.0 cm RUL mass.\n[Anesthesia]\nGeneral.\n[Description]\nMonarch nav to RUL. REBUS eccentric. CBCT confirmation. Biopsy and BAL performed.\n[Plan]\nDischarge. Tumor board.",
            8: "A 69-year-old male with a right upper lobe mass underwent robotic bronchoscopy using the Monarch system. We navigated to the central RUL and confirmed the lesion with radial EBUS. We performed forceps biopsies and a BAL. Cone-beam CT confirmed the tool's position. The procedure was uncomplicated.",
            9: "Indication: RUL tumor.\nTechnique: Monarch robotic piloting, ultrasonic scanning, lavage, tissue harvesting.\nFindings: 3cm mass.\nVerification: Volumetric CT.\nAction: Collected tissue and washings. Hemostasis confirmed."
        },
        10: { # RAB011: 61F, LLL cluster, Ion Partial Reg
            1: "Indication: LLL nodules.\nProc: Ion bronch, Partial Reg, bx.\nFindings: 1.4cm dominant nodule.\nAction: Bx of both nodules. Aug fluoro.\nResult: No complications.",
            2: "OPERATIVE NOTE: The patient presented with clustered left lower lobe nodules. Robotic bronchoscopy (Ion) was performed using a partial registration strategy. The dominant 1.4 cm nodule was targeted first, showing a concentric REBUS view. Biopsies and brushings were taken. The smaller satellite nodule was also sampled along the same track. Augmented fluoroscopy confirmed positioning.",
            3: "CPT 31627 (Nav), 31654 (EBUS), 31628 (Bx), 31623 (Brush).\nNote: Multiple lesions sampled in same lobe = single unit of 31628. Partial registration used for efficiency.",
            4: "Resident Note\nPt: 61F\nOp: Ion LLL Bx (Cluster)\n- Partial reg.\n- Nav to LLL.\n- REBUS: Concentric 1.4cm.\n- Aug Fluoro used.\n- Bx dominant & satellite nodules.\n- Brush x1.\n- No bleeding.",
            5: "61 female lll clustered nodules ion robot partial reg used navigated to big one 1.4cm concentric on rebus took biopsies and a brush then took bites of the little one too augmented fluoro confirmed tool in lesion no issues",
            6: "Robotic navigational bronchoscopy with partial registration. LLL clustered nodules. Ion system used. REBUS showed concentric lesion. Augmented fluoroscopy used. Biopsies of both nodules obtained. No complications.",
            7: "[Indication]\nClustered LLL nodules.\n[Anesthesia]\nGeneral.\n[Description]\nIon partial reg. Nav to LLL. REBUS concentric. Aug fluoro. Biopsies of dominant and satellite nodules.\n[Plan]\nDischarge. Path review.",
            8: "We performed a robotic bronchoscopy on a 61-year-old female with clustered nodules in the left lower lobe. Using the Ion system with partial registration, we navigated to the dominant nodule. Radial EBUS showed a concentric view. We biopsied both the dominant and satellite nodules. The patient tolerated the procedure well.",
            9: "Indication: LLL nodules.\nMethod: Robotic steering (partial mapping), ultrasonic detection, tissue sampling.\nFindings: 1.4cm concentric target.\nVerification: Enhanced fluoroscopy.\nAction: Acquired specimens from multiple sites. No hemorrhage."
        },
        11: { # RAB012: 56M, RLL GGO, Ion
            1: "Indication: RLL GGO.\nProc: Ion bronch, REBUS, bx.\nFindings: Faint halo on REBUS.\nAction: 4 bx. Respiratory gating used.\nResult: No bleeding.",
            2: "PROCEDURE REPORT: This 56-year-old male with a right lower lobe ground-glass opacity underwent robotic bronchoscopy. The Ion system was used to navigate to the posterior segment. Radial EBUS revealed a faint acoustic halo compatible with GGO. Respiratory-gated breath-holds and augmented fluoroscopy optimized target alignment. Forceps biopsies were obtained without complication.",
            3: "CPT 31627 (Nav), 31654 (EBUS), 31628 (Bx).\nTarget: Ground-glass nodule.\nTechnique: Respiratory gating used to minimize motion artifact.",
            4: "Trainee Note\nPt: 56M\nOp: Ion RLL GGO Bx\n- Nav to RLL posterior.\n- REBUS: Faint halo (GGO).\n- Used resp gating/breath hold.\n- Aug Fluoro confirm.\n- Bx x4.\n- No bleeding.",
            5: "case 12 56m rll ground glass nodule ion robot used nav to posterior segment rebus showed halo effect typical for ggo used breath hold technique and augmented fluoro took 4 biopsies no bleeding patient fine",
            6: "Robotic navigational bronchoscopy for GGO. RLL nodule. Ion system used. REBUS showed faint halo. Respiratory gating and augmented fluoroscopy used. Forceps biopsies obtained. No complications.",
            7: "[Indication]\n1.3 cm RLL GGO.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to RLL. REBUS halo. Resp gating used. 4 biopsies.\n[Plan]\nDischarge. Path review.",
            8: "A 56-year-old male underwent robotic bronchoscopy for a ground-glass nodule in the right lower lobe. We utilized the Ion system and confirmed the lesion with radial EBUS, which showed a faint halo. We employed respiratory gating to stabilize the target and obtained four biopsies. The procedure was uncomplicated.",
            9: "Indication: RLL ground-glass opacity.\nProcedure: Robotic guidance, ultrasonic localization, tissue acquisition.\nFindings: Acoustic halo.\nTechnique: Breath-hold synchronization.\nAction: Harvested specimens. No hemorrhage."
        },
        12: { # RAB013: 73F, RML nodule, Monarch
            1: "Indication: RML nodule.\nProc: Monarch bronch, REBUS, bx.\nFindings: 20mm eccentric lesion.\nAction: 5 bx, 1 brush. CBCT used.\nResult: Extubated. Stable.",
            2: "OPERATIVE NOTE: The patient, a 73-year-old female with COPD, underwent Monarch robotic bronchoscopy for a right middle lobe nodule. Navigation to the medial segment was achieved. Radial EBUS demonstrated an eccentric 20 mm lesion. Cone-beam CT confirmed the catheter position. Multiple biopsies and a brushing were obtained. The patient was extubated without difficulty.",
            3: "CPT 31627 (Monarch Nav), 31654 (EBUS), 31628 (Bx), 31623 (Brush).\nComorbidity: COPD.\nImaging: CBCT used.\nOutcome: Successful sampling.",
            4: "Resident Note\nPt: 73F, COPD\nOp: Monarch RML Bx\n- Nav to RML medial.\n- REBUS: 20mm eccentric.\n- CBCT: Confirmed.\n- Bx x5, Brush x1.\n- No bleeding.\n- Extubated ok.",
            5: "73 female copd rml nodule monarch robot used nav to medial segment rebus eccentric lesion cbct confirmed position took 5 biopsies and a brush minimal bleeding extubated fine",
            6: "Robotic navigational bronchoscopy (Monarch). RML nodule. Monarch system used. REBUS showed eccentric lesion. CBCT confirmed position. Biopsies and brushings obtained. No complications. Patient extubated.",
            7: "[Indication]\n2.0 cm RML nodule, COPD.\n[Anesthesia]\nGeneral.\n[Description]\nMonarch nav to RML. REBUS eccentric. CBCT confirmation. 5 biopsies, 1 brush.\n[Plan]\nDischarge. Path review.",
            8: "We performed a robotic bronchoscopy on a 73-year-old female with COPD and a right middle lobe nodule. Using the Monarch platform, we navigated to the medial segment. Radial EBUS and CBCT confirmed the lesion. We obtained multiple biopsies and a brushing. The patient was extubated and recovered well.",
            9: "Indication: RML neoplasm.\nTechnique: Monarch robotic piloting, ultrasonic scanning, tissue acquisition.\nFindings: 20mm eccentric target.\nVerification: Volumetric CT.\nAction: Collected specimens. No hemorrhage."
        },
        13: { # RAB014: 65M, LUL nodule, Ion
            1: "Indication: LUL nodule.\nProc: Ion bronch, REBUS, bx.\nFindings: 16mm concentric lesion.\nAction: Bx and brush. CBCT used.\nResult: No complications.",
            2: "PROCEDURE REPORT: This 65-year-old male with a left upper lobe nodule underwent robotic-assisted bronchoscopy (Ion). The catheter was navigated to the anterior segment. Radial EBUS revealed a concentric 16 mm lesion. Cone-beam CT confirmed tool-in-lesion. Biopsies and a brushing were obtained. There were no immediate complications.",
            3: "CPT 31627 (Nav), 31654 (EBUS), 31628 (Bx), 31623 (Brush).\nTarget: LUL anterior segment.\nImaging: CBCT confirmed location.\nOutcome: Samples obtained.",
            4: "Trainee Note\nPt: 65M\nOp: Ion LUL Bx\n- Nav to LUL anterior.\n- REBUS: 16mm concentric.\n- CBCT: Tool in lesion.\n- Bx x4, Brush x1.\n- Minimal oozing.\n- Stable.",
            5: "case 14 65m lul nodule ion robotic bronch nav to anterior segment rebus showed concentric 16mm lesion cbct confirmed tool in lesion took biopsies and brush minimal oozing stopped on its own",
            6: "Robotic navigational bronchoscopy with biopsy. LUL nodule. Ion system used. REBUS showed 16 mm concentric lesion. CBCT confirmed position. Biopsies and brushings obtained. No complications.",
            7: "[Indication]\n1.6 cm LUL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to LUL. REBUS concentric. CBCT confirmation. Biopsies and brush.\n[Plan]\nDischarge. Path review.",
            8: "A 65-year-old male underwent robotic bronchoscopy for a left upper lobe nodule. We used the Ion system to navigate to the anterior segment. Radial EBUS showed a concentric lesion, and CBCT confirmed the tool was inside. We obtained biopsies and a brushing with minimal oozing. The procedure was successful.",
            9: "Indication: LUL opacity.\nProcedure: Robotic guidance, ultrasonic localization, tissue harvesting.\nFindings: 16mm concentric target.\nVerification: 3D fluoroscopy.\nAction: Acquired tissue via forceps and brush. No hemorrhage."
        },
        14: { # RAB015: 60F, LLL nodule, Monarch
            1: "Indication: LLL nodule.\nProc: Monarch bronch, REBUS, bx.\nFindings: 17mm eccentric lesion.\nAction: Bx and brush. Aug fluoro used.\nResult: No bleeding.",
            2: "OPERATIVE SUMMARY: The patient, a 60-year-old female, underwent Monarch robotic bronchoscopy for a left lower lobe nodule. Navigation to the superior segment was successful. Radial EBUS identified an eccentric 17 mm lesion. Augmented fluoroscopy confirmed alignment; CBCT was not required. Biopsies and a brushing were collected. The patient remained stable throughout.",
            3: "CPT 31627 (Monarch Nav), 31654 (EBUS), 31628 (Bx), 31623 (Brush).\nTarget: LLL superior segment.\nImaging: Augmented fluoroscopy sufficient.\nOutcome: Samples obtained.",
            4: "Resident Note\nPt: 60F\nOp: Monarch LLL Bx\n- Nav to LLL superior.\n- REBUS: 17mm eccentric.\n- Aug Fluoro: Good.\n- Bx x4, Brush x1.\n- No bleeding.\n- Stable.",
            5: "60 female lll nodule monarch robot used nav to superior segment rebus eccentric lesion augmented fluoro used to refine position took biopsies and brush minimal bleeding discharged home",
            6: "Robotic navigational bronchoscopy (Monarch). LLL nodule. Monarch system used. REBUS showed eccentric lesion. Augmented fluoroscopy used. Biopsies and brushings obtained. No complications.",
            7: "[Indication]\n1.7 cm LLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nMonarch nav to LLL. REBUS eccentric. Aug fluoro confirmation. Biopsies and brush.\n[Plan]\nDischarge. Path review.",
            8: "We performed a robotic bronchoscopy on a 60-year-old female using the Monarch platform for a left lower lobe nodule. We navigated to the superior segment and visualized the lesion with radial EBUS. Augmented fluoroscopy confirmed the alignment. We collected multiple samples without complications.",
            9: "Indication: LLL lesion.\nProcedure: Monarch robotic steering, ultrasonic detection, tissue sampling.\nFindings: 17mm eccentric target.\nVerification: Enhanced fluoroscopy.\nAction: Harvested specimens. Recovery uneventful."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for patient names and ages to correspond with the 15 source notes.
    """
    return [
        {"idx": 0, "orig_name": "Case 01", "orig_age": 62, "names": ["John Smith", "Robert Jones", "Michael Brown", "David Davis", "William Miller", "Richard Wilson", "Joseph Moore", "Thomas Taylor", "Charles Anderson"]},
        {"idx": 1, "orig_name": "Case 02", "orig_age": 74, "names": ["Mary Johnson", "Patricia Williams", "Linda Jones", "Barbara Brown", "Elizabeth Davis", "Jennifer Miller", "Maria Wilson", "Susan Moore", "Margaret Taylor"]},
        {"idx": 2, "orig_name": "Case 03", "orig_age": 59, "names": ["Karen Anderson", "Nancy Thomas", "Lisa Jackson", "Betty White", "Dorothy Harris", "Sandra Martin", "Ashley Thompson", "Kimberly Garcia", "Donna Martinez"]},
        {"idx": 3, "orig_name": "Case 04", "orig_age": 67, "names": ["Christopher Robinson", "Daniel Clark", "Paul Rodriguez", "Mark Lewis", "Donald Lee", "George Walker", "Kenneth Hall", "Steven Allen", "Edward Young"]},
        {"idx": 4, "orig_name": "Case 05", "orig_age": 71, "names": ["Brian Hernandez", "Ronald King", "Anthony Wright", "Kevin Lopez", "Jason Hill", "Matthew Scott", "Gary Green", "Timothy Adams", "Jose Baker"]},
        {"idx": 5, "orig_name": "Case 06", "orig_age": 64, "names": ["Carol Gonzalez", "Michelle Nelson", "Sarah Carter", "Laura Mitchell", "Kim Perez", "Jessica Roberts", "Cynthia Turner", "Angela Phillips", "Melissa Campbell"]},
        {"idx": 6, "orig_name": "Case 07", "orig_age": 58, "names": ["Larry Parker", "Jeffrey Evans", "Frank Edwards", "Scott Collins", "Eric Stewart", "Stephen Sanchez", "Andrew Morris", "Raymond Rogers", "Gregory Reed"]},
        {"idx": 7, "orig_name": "Case 08", "orig_age": 63, "names": ["Joshua Cook", "Jerry Morgan", "Dennis Bell", "Walter Murphy", "Patrick Bailey", "Peter Rivera", "Harold Cooper", "Douglas Richardson", "Henry Cox"]},
        {"idx": 8, "orig_name": "Case 09", "orig_age": 52, "names": ["Rebecca Howard", "Virginia Ward", "Debra Torres", "Amanda Peterson", "Stephanie Gray", "Carolyn Ramirez", "Christine James", "Marie Watson", "Janet Brooks"]},
        {"idx": 9, "orig_name": "Case 10", "orig_age": 69, "names": ["Carl Kelly", "Arthur Sanders", "Ryan Price", "Roger Bennett", "Joe Wood", "Juan Barnes", "Jack Ross", "Albert Henderson", "Jonathan Coleman"]},
        {"idx": 10, "orig_name": "Case 11", "orig_age": 61, "names": ["Catherine Jenkins", "Ann Perry", "Joyce Powell", "Diane Long", "Alice Patterson", "Julie Hughes", "Heather Flores", "Teresa Washington", "Doris Butler"]},
        {"idx": 11, "orig_name": "Case 12", "orig_age": 56, "names": ["Justin Simmons", "Terry Foster", "Gerald Gonzales", "Keith Bryant", "Samuel Alexander", "Willie Russell", "Ralph Griffin", "Lawrence Diaz", "Nicholas Hayes"]},
        {"idx": 12, "orig_name": "Case 13", "orig_age": 73, "names": ["Gloria Myers", "Evelyn Ford", "Jean Hamilton", "Cheryl Graham", "Mildred Sullivan", "Katherine Wallace", "Joan Woods", "Ashley Cole", "Judith West"]},
        {"idx": 13, "orig_name": "Case 14", "orig_age": 65, "names": ["Roy Jordan", "Benjamin Owens", "Bruce Reynolds", "Brandon Fisher", "Adam Ellis", "Harry Harrison", "Fred Gibson", "Wayne McDonald", "Billy Cruz"]},
        {"idx": 14, "orig_name": "Case 15", "orig_age": 60, "names": ["Rose Marshall", "Janice Ortiz", "Kelly Gomez", "Nicole Murray", "Judy Freeman", "Christina Wells", "Kathy Webb", "Theresa Simpson", "Beverly Tucker"]}
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
            # Check if index exists in variations dictionary to avoid KeyErrors
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing variation for Note {idx}, Style {style_num}. Using original text.")
            
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
    output_filename = output_dir / "synthetic_robotic_notes_part_063.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()