import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_022.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary mapping Note_Index (0-9) -> Style_Index (1-9) -> Text.
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
        0: { # Note 0: Natalie Reed (BAL + TBBx)
            1: "Proc: Bronch w/ BAL & TBBx.\n- Scope passed to RML -> BAL obtained.\n- TBBx x6 RLL lateral basal segment under fluoro.\n- Bleeding: Mild, cold saline.\n- No pneumo on fluoro.\nPlan: D/C home.",
            2: "OPERATIVE REPORT: The patient presented with diffuse parenchymal opacities. Following moderate sedation, the airways were inspected to the subsegmental level and found to be patent. A bronchoalveolar lavage was meticulously performed in the right middle lobe. Subsequently, fluoroscopic guidance facilitated the acquisition of six transbronchial biopsy specimens from the right lower lobe lateral basal segment using standard forceps. Hemostasis was achieved with cold saline lavage.",
            3: "Procedure: Bronchoscopy with multiple diagnostic interventions.\nTechnique:\n1. 31624: Bronchoscope wedged in Right Middle Lobe; 100mL saline instilled/aspirated for BAL.\n2. 31628: Scope repositioned to Right Lower Lobe. Fluoroscopy utilized to guide forceps to periphery. Six (6) biopsies obtained from single lobe (RLL).\nJustification: Diagnostic evaluation of ILD. Samples sent for pathology and micro.",
            4: "Procedure Note\nResident: Dr. Doe\nAttending: Dr. Allen\nIndication: ILD workup.\nSteps:\n1. Time out.\n2. Sedation start.\n3. Airway inspection: Normal.\n4. BAL: RML (good return).\n5. Biopsy: RLL Lat Basal x 6. Fluoro used.\n6. Complications: Minimal bleeding.\nDisposition: Recovery.",
            5: "patient here for bronchoscopy ild workup we gave midazolam fentanyl airway looked fine went into the right middle lobe did the lavage clear fluid back then moved to the right lower lobe for biopsies used fluoro took about six samples standard forceps little bit of bleeding iced saline stopped it patient tolerated well no pneumo detected discharged home.",
            6: "Flexible bronchoscopy with BAL and transbronchial biopsies for interstitial lung disease evaluation. Patient is a 53-year-old female with progressive dyspnea and bilateral ground-glass opacities. Moderate sedation with fentanyl and midazolam; native airway. Normal airways to subsegmental level. BAL performed in right middle lobe. Fluoroscopy-guided transbronchial biopsies (6 samples) obtained from right lower lobe lateral basal segment using standard forceps. Mild bleeding controlled with iced saline; no pneumothorax on postprocedure CXR. Discharged home from recovery area.",
            7: "[Indication]\nProgressive dyspnea, GGOs.\n[Anesthesia]\nModerate sedation (Fentanyl/Versed).\n[Description]\nScope advanced. RML lavaged (BAL). RLL lateral basal segment biopsied x6 using fluoro guidance. Hemostasis achieved.\n[Plan]\nDischarge home. Follow up in ILD clinic.",
            8: "The patient was brought to the bronchoscopy suite for evaluation of interstitial lung disease. After achieving moderate sedation, we inserted the bronchoscope. We performed a bronchoalveolar lavage in the right middle lobe. We then navigated to the right lower lobe, specifically the lateral basal segment, and used fluoroscopy to guide the forceps for six transbronchial biopsies. There was only mild bleeding which we stopped with iced saline. No pneumothorax was seen.",
            9: "Procedure: Flexible bronchoscopy with lavage and transbronchial sampling.\nDetails: Airways were patent. Lavage was executed in the RML. Fluoroscopy-guided samples (6) were harvested from the RLL lateral basal segment using forceps. Minor hemorrhage was arrested with iced saline."
        },
        1: { # Note 1: Carlos Rivera (Cryobiopsy)
            1: "Proc: Cryobiopsy ILD.\n- ETT/GA.\n- RLL basal segments target.\n- Radial EBUS: Safe zone confirmed.\n- 3x Cryobiopsy (1.9mm), 1x Forceps.\n- Blocker used for hemostasis.\n- No pneumo.",
            2: "PROCEDURE NARRATIVE: Under general anesthesia, the bronchoscope was advanced to the right lower lobe. To minimize hemorrhage risk, a prophylactic bronchial blocker was positioned. Radial EBUS interrogation confirmed a target area free of major vasculature. Three large tissue samples were acquired via a 1.9 mm cryoprobe, supplemented by one standard forceps biopsy. Hemostasis was managed via temporary balloon inflation.",
            3: "Coding Summary:\nCode 31628: Transbronchial lung biopsy, single lobe (RLL).\nTechnique: Cryoprobe activation (freezing) used to obtain parenchymal tissue. Note: Cryobiopsy for parenchymal disease is reported with 31628 (biopsy), not 31641 (cryotherapy).\nGuidance: Fluoroscopy and Radial EBUS utilized for safety.",
            4: "Resident Note:\nProcedure: Cryobiopsy.\nSteps:\n1. Intubation 8.5 ETT.\n2. Scope to RLL.\n3. Radial EBUS check.\n4. Blocker placed.\n5. Cryoprobe: 3 passes RLL basals.\n6. Forceps: 1 pass.\n7. Bleeding controlled with blocker.\nPlan: Admit for obs.",
            5: "carlos rivera 47 male ild study general anesthesia tube down scope to rll we used the radial ebus to check for vessels looked good put the bronchial blocker down just in case did three cryo biopsies with the 1.9 probe and one regular forcep biopsy little bleeding blew up the balloon and used cold saline stopped fine no pneumo on xray admitting for observation.",
            6: "Bronchoscopy with transbronchial cryobiopsies for interstitial lung disease. Patient is a 47-year-old male with suspected fibrotic ILD. General anesthesia with endotracheal intubation. Bronchoscope advanced to RLL; fluoroscopy and radial EBUS used to identify safe parenchymal target areas. Three cryobiopsies obtained from RLL basal segments using 1.9 mm cryoprobe and one standard forceps biopsy. Bronchial blocker placed prophylactically. Mild bleeding controlled with temporary bronchial blocker inflation and iced saline. No pneumothorax on postprocedure CXR. Admitted overnight for observation.",
            7: "[Indication]\nSuspected fibrotic ILD.\n[Anesthesia]\nGA, 8.5 ETT.\n[Description]\nRLL cannulated. Radial EBUS cleared target. Prophylactic blocker placed. 3 cryobiopsies + 1 forceps biopsy taken. Blocker inflated for hemostasis.\n[Plan]\nAdmit overnight. CXR in AM.",
            8: "We performed a bronchoscopy with cryobiopsy on Mr. Rivera to investigate his ILD. Under general anesthesia, we navigated to the right lower lobe. We used radial EBUS to ensure we weren't near large vessels. We took three biopsies using the freezing probe and one with standard forceps. A bronchial blocker was used to manage the mild bleeding that occurred. He is being admitted for observation.",
            9: "Procedure: Bronchoscopy with transbronchial cryo-sampling.\nAction: Scope guided to RLL. Radial EBUS verified safe zone. Three cryo-samples extracted from RLL basal segments using 1.9 mm probe, plus one standard forceps sample. Hemorrhage halted with bronchial blocker."
        },
        2: { # Note 2: Megan Collins (Cryo + Pneumothorax)
            1: "Proc: Cryobiopsy LLL.\n- 3 samples (1.9mm probe).\n- Complication: Desaturation, absent breath sounds L.\n- Dx: Pneumothorax (Fluoro/US).\n- Rx: 14Fr Pigtail placed. Air evacuated.\n- Pt stable. Admitted.",
            2: "OPERATIVE COMPLICATION NOTE: During transbronchial cryobiopsy of the left lower lobe for hypersensitivity pneumonitis, the patient developed acute hypotension and desaturation following the third pass. Fluoroscopy and bedside ultrasound confirmed a left-sided pneumothorax. A 14 French pigtail thoracostomy tube was immediately placed in the 5th intercostal space, resulting in prompt lung re-expansion and hemodynamic stabilization.",
            3: "Codes:\n- 31628: Transbronchial biopsy LLL (3 samples).\n- 32551: Tube thoracostomy (Chest tube) for iatrogenic pneumothorax.\nRationale: Separate distinct procedure required to manage complication (chest tube). Biopsy completed prior to event.",
            4: "Procedure: Cryobiopsy + Chest Tube\nPatient: Megan Collins\nEvents:\n1. ETT/GA.\n2. Cryobiopsy LLL x3.\n3. Patient crashed (Sat 85%, High Pressures).\n4. Fluoro showed pneumo.\n5. Pigtail catheter placed L side.\n6. Improved.\nPlan: Step-down unit.",
            5: "megan collins 60f hp suspicion general anesthesia we did cryobiopsy lll three samples on the last one pressures went up sats dropped breath sounds gone left side fluoro showed pneumothorax so we put in a pigtail chest tube 14 french suction applied patient stabilized lung came up admitting her to step down.",
            6: "Bronchoscopy with transbronchial cryobiopsy complicated by pneumothorax. Patient is a 60-year-old female with suspected hypersensitivity pneumonitis. General anesthesia with ETT. Cryobiopsies obtained from left lower lobe basal segments using 1.9 mm cryoprobe (3 samples). Fluoroscopy used. After third biopsy, patient developed decreased breath sounds and rising airway pressures. Left pneumothorax confirmed on fluoroscopy and ultrasound. A 14 Fr pigtail chest tube placed with immediate improvement. Admitted to step-down unit with chest tube to suction.",
            7: "[Indication]\nSuspected HP, Cryobiopsy.\n[Anesthesia]\nGA, ETT.\n[Description]\n3 Cryobiopsies taken LLL. Complicated by immediate pneumothorax. 14Fr Chest tube inserted. Lung expanded.\n[Plan]\nAdmit step-down. Suction. Daily CXR.",
            8: "The procedure began as a standard cryobiopsy for suspected hypersensitivity pneumonitis. We obtained three samples from the left lower lobe. Unfortunately, after the last sample, the patient developed a pneumothorax. We confirmed this with ultrasound and fluoroscopy and immediately placed a 14 French chest tube. The lung re-expanded and vitals normalized. She is admitted for chest tube management.",
            9: "Procedure: Bronchoscopy with transbronchial cryo-extraction complicated by lung collapse.\nDetails: Samples harvested from LLL. Following the third extraction, signs of pneumothorax appeared. A 14 Fr pigtail catheter was inserted, resolving the collapse. Patient transferred to step-down."
        },
        3: { # Note 3: Zachary Price (Robotic RFA)
            1: "Proc: Robotic Bronch + RFA LLL.\n- Ion robot to 12mm lesion.\n- Confirmed: REBUS + Cone Beam CT.\n- Ablation: 50W / 600s / 90C.\n- Margins: +5mm achieved.\n- Mild bleeding. No pneumo.",
            2: "OPERATIVE REPORT: Using the Ion robotic platform, the left lower lobe lateral basal segment was cannulated. A 12 mm nodule was localized. Confirmation was achieved via radial EBUS (solid lesion) and Cone-Beam CT (tool-in-lesion). Radiofrequency ablation was delivered via a dedicated probe at 50 Watts for 600 seconds. Post-ablation CBCT confirmed an adequate ablation zone encompassing the tumor with a safety margin.",
            3: "Billing Codes:\n- 31641: Therapeutic bronchoscopy, destruction of tumor (RFA).\n- 31627: Navigational Bronchoscopy (Add-on).\n- 31654: EBUS Peripheral (Add-on).\nLogic: Navigation and REBUS used to localize. RFA used to destroy. Single session.",
            4: "Resident Note\nProcedure: Robotic RFA\nSteps:\n1. GA/ETT.\n2. Ion robot registered.\n3. Navigated to LLL nodule.\n4. REBUS/CBCT confirm.\n5. RFA burned for 10 mins @ 50W.\n6. CBCT showed good hit.\nPlan: Admit overnight.",
            5: "zachary price 66 male CRC met to lung ion robot case went to LLL nodule 12mm spin ct confirmed tool in lesion burned it with radiofrequency 50 watts 600 seconds temp 90c spin ct after showed good ablation zone little bleeding nothing major admitting for observation.",
            6: "Robotic navigational bronchoscopy with radiofrequency ablation (RFA) of peripheral left lower lobe nodule. Patient is a 66-year-old male with oligometastatic colorectal cancer to lung. General anesthesia with ETT. Ion robotic platform used to access 12 mm LLL peripheral metastasis. Registration error 2.3 mm. Radial EBUS confirmed solid lesion; cone-beam CT confirmed tool-in-lesion. RFA probe advanced through working channel. Ablation performed at 50 W for 600 seconds with maximum temperature 90 degrees Celsius. Postablation cone-beam CT demonstrated satisfactory ablation zone with 5 mm margin. Mild perilesional hemorrhage without hemodynamic compromise. Admitted overnight for observation.",
            7: "[Indication]\nOligometastatic CRC to Lung.\n[Anesthesia]\nGA, 8.5 ETT.\n[Description]\nIon Robot nav to LLL. REBUS/CBCT confirmed position. RFA performed (50W, 600s). Ablation zone confirmed on CBCT.\n[Plan]\nAdmit. CT Chest 3 mos.",
            8: "We performed a robotic bronchoscopy to ablate a metastasis in Mr. Price's left lung. Using the Ion system and Cone-Beam CT, we perfectly targeted the 12mm nodule. We applied radiofrequency energy to destroy the tumor, reaching 90 degrees Celsius. The post-procedure scan showed we covered the whole tumor with a good margin. There was minimal bleeding and no complications.",
            9: "Procedure: Robotic navigational bronchoscopy with thermal destruction (RFA).\nAction: Ion platform navigated to LLL lesion. REBUS verified target. Thermal ablation executed at 50 W. Post-treatment imaging verified satisfactory necrosis zone."
        },
        4: { # Note 4: Julia Bennett (MWA)
            1: "Proc: Nav Bronch + Microwave Ablation RUL.\n- SuperDimension nav.\n- Lesion: 18mm RUL posterior.\n- Confirmed: REBUS + Fluor + CBCT.\n- MWA: 60W / 420s.\n- Complication: 15ml hemoptysis (stopped).\n- Admit Telemetry.",
            2: "PROCEDURE: The superDimension electromagnetic navigation system facilitated access to an 18 mm nodule in the RUL posterior segment. Radial EBUS imaging demonstrated an eccentric view. Tool-in-lesion was verified via Cone-Beam CT. Microwave ablation was executed using the Emprint system (60 Watts, 420 seconds). Immediate post-ablation imaging confirmed an 8mm ablative margin. Transient hemoptysis was noted and resolved spontaneously.",
            3: "Coding: 31641 (Destruction/Relief) + 31627 (Nav) + 31654 (REBUS).\nDevice: Microwave Ablation Catheter.\nGuidance: EMN + CBCT + Fluoroscopy.\nTarget: Peripheral RUL nodule (RCC met).",
            4: "Procedure: Bronch MWA\nPt: Julia Bennett\nSteps:\n1. GA/ETT.\n2. Navigated to RUL using SuperD.\n3. REBUS/CBCT confirm.\n4. Microwaved: 60W for 7 mins.\n5. Pt coughed up 15cc blood, then stopped.\n6. Stable.\nPlan: Admit.",
            5: "julia bennett 62 f renal cell met RUL nodule superdimension nav used cone beam to check position microwave ablation done 60 watts 420 seconds emprint system she had some hemoptysis about 15 ml but it stopped on its own scan looks good margin achieved admitting to telemetry.",
            6: "Bronchoscopic microwave ablation (MWA) of right upper lobe peripheral nodule. Patient is a 62-year-old female with solitary lung metastasis from renal cell carcinoma. General anesthesia with ETT. superDimension EMN platform used to reach 18 mm RUL posterior segment nodule. Fluoroscopy and cone-beam CT confirmed tool-in-lesion. Microwave antenna advanced through extended working channel. Ablation performed with Emprint MWA system at 60 W for 420 seconds. Postablation imaging demonstrated adequate ablation zone with 8 mm margin. Transient hemoptysis of approximately 15 mL, resolved spontaneously. Admitted overnight to telemetry.",
            7: "[Indication]\nSolitary RCC Met RUL.\n[Anesthesia]\nGA.\n[Description]\nEMN nav to RUL. Confirmed w/ CBCT. MWA performed (60W, 420s). Good ablation zone.\n[Complications]\nSelf-limited hemoptysis (15mL).\n[Plan]\nAdmit Telemetry. CT 3 mos.",
            8: "Ms. Bennett underwent bronchoscopic microwave ablation for her RUL tumor. We used electromagnetic navigation to guide the antenna to the spot, verifying it with CT. We treated the area with 60 Watts of energy for 7 minutes. She coughed up a little blood during the procedure, but it stopped quickly. The final scan showed the tumor was successfully treated with a safety margin.",
            9: "Procedure: Bronchoscopic microwave thermal therapy.\nTarget: RUL peripheral nodule.\nAction: Navigated via EMN. Position verified. Microwave energy applied (60W). Hemorrhage of 15 mL occurred but resolved. Ablation zone deemed adequate."
        },
        5: { # Note 5: Ryan Cooper (Cryoablation)
            1: "Proc: Robotic Bronch + Cryoablation RLL.\n- Monarch robot -> RLL superior seg.\n- 16mm lesion.\n- Confirmed: REBUS + CBCT.\n- Cryo: 3 cycles (freeze/thaw), 300s each.\n- Ice ball confirmed on CBCT.\n- Mild hemoptysis.",
            2: "OPERATIVE SUMMARY: The Monarch robotic endoluminal system was utilized to navigate to a 16 mm lesion in the RLL superior segment. Confirmation of the target was established via radial EBUS and Cone-Beam CT. A flexible cryoprobe was deployed, and cryoablation was performed using a triple freeze-thaw protocol (300 seconds per freeze). Intraprocedural CBCT visualization demonstrated an ice ball completely engulfing the lesion with adequate margins.",
            3: "Codes: 31641 (Destruction), 31627 (Nav), 31654 (REBUS).\nTechnique: Cryoablation (Freezing for destruction, not biopsy).\nTarget: Peripheral malignancy (NSCLC).\nImaging: CBCT used to visualize ice ball formation.",
            4: "Resident Note\nProcedure: Cryoablation\nSteps:\n1. GA/ETT.\n2. Monarch robot nav to RLL.\n3. REBUS/CBCT check.\n4. Cryoprobe in.\n5. 3 freezes, 5 mins each.\n6. Ice ball seen on CT.\n7. Mild bleeding/desat -> fixed.\nPlan: Admit.",
            5: "ryan cooper 69m nsclc poor lung fxn so doing ablation monarch robot used navigated to rll superior seg 16mm nodule confirmed with rebus and cone beam did cryoablation 3 cycles 5 mins each saw the ice ball covering the tumor little bit of hemoptysis and o2 drop but recovered fine admitted.",
            6: "Bronchoscopic cryoablation of peripheral right lower lobe lesion. Patient is a 69-year-old male with small presumed primary NSCLC not amenable to surgery. General anesthesia with ETT. Monarch robotic platform used to reach 16 mm RLL superior segment lesion. Radial EBUS and cone-beam CT confirmed tool-in-lesion. Flexible cryoprobe advanced and three freeze-thaw cycles performed (each 300 seconds). Postablation cone-beam CT demonstrated ice ball encompassing lesion with 5 mm margin. Mild transient hemoptysis and temporary increase in oxygen requirement; no pneumothorax. Admitted overnight to monitored bed.",
            7: "[Indication]\nEarly stage NSCLC, non-surgical.\n[Anesthesia]\nGA.\n[Description]\nMonarch nav to RLL. Cryoablation x3 cycles (300s). Ice ball confirmed on CBCT.\n[Complications]\nMild hemoptysis, transient hypoxia.\n[Plan]\nAdmit. Oncology follow up.",
            8: "We treated Mr. Cooper's lung cancer with cryoablation today. Using the Monarch robot, we guided a freezing probe directly into the tumor in his right lower lobe. We froze the tumor three times for 5 minutes each. The CT scan during the procedure showed a nice ice ball covering the whole area. He had a bit of bleeding and needed some extra oxygen for a moment, but he is doing well now.",
            9: "Procedure: Bronchoscopic cryo-destruction of peripheral lesion.\nAction: Monarch platform used for access. Lesion engaged. Three freeze-thaw sequences executed. Imaging confirmed ice ball formation encompassing the target."
        },
        6: { # Note 6: EBUS Summary Note (Requires inventing patient details)
            1: "Proc: EBUS TBNA + Nav TBBx.\n- EBUS: Systematic staging (3+ stations).\n- Nav/REBUS: Peripheral nodule.\n- TBBx: Samples obtained.\n- No complications.",
            2: "PROCEDURE: The procedure commenced with a linear EBUS systematic mediastinal survey, sampling stations 4R, 7, and 4L (CPT 31653). Following staging, electromagnetic navigation and radial EBUS were utilized to localize a peripheral pulmonary nodule. Transbronchial biopsies were obtained under fluoroscopic guidance (CPT 31628, 31627, 31654).",
            3: "Codes:\n- 31653: EBUS Sampling 3+ stations.\n- 31628: TBBx single lobe.\n- 31627: Navigation Add-on.\n- 31654: Radial EBUS Add-on.\nJustification: Staging concurrent with diagnostic workup of nodule.",
            4: "Resident Note\nProcedure: EBUS + Nav Bronch\nSteps:\n1. EBUS scope: Sampled 4R, 7, 11L.\n2. Switched to therapeutic scope.\n3. Navigated to nodule.\n4. REBUS confirmed.\n5. Biopsied.\nPlan: Path pending.",
            5: "patient here for staging and diagnosis did the ebus first hit three stations mediastinum looks clear then switched scopes used navigation and radial probe to find the nodule in the lung took biopsies looks like cancer maybe no bleeding patient woke up fine.",
            6: "EBUS bronchoscopy with systematic mediastinal survey and transbronchial lung biopsy using navigation and radial EBUS for a pulmonary nodule. Staging performed at multiple stations. Navigation used to access peripheral lesion. Radial EBUS confirmation obtained. Biopsies taken without complication.",
            7: "[Indication]\nPulmonary nodule, staging.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS TBNA x3 stations. Nav bronch to nodule. REBUS confirmation. TBBx x5.\n[Plan]\nDischarge. Follow up path.",
            8: "We performed a complete workup for the patient's lung nodule. First, we used the EBUS scope to sample three lymph node stations in the chest to check for spread. Then, we used navigation technology and a small ultrasound probe (radial EBUS) to find the nodule deep in the lung and took several biopsy samples. The procedure went smoothly.",
            9: "Procedure: Endobronchial ultrasound staging and navigational sampling.\nAction: Mediastinal survey completed via EBUS. Peripheral lesion localized via electromagnetic guidance and radial ultrasound. Transbronchial specimens harvested."
        },
        7: { # Note 7: RFA RLL Summary (Invent details)
            1: "Proc: Nav Bronch + RFA RLL.\n- Target: SCC RLL.\n- Guides: ENB + REBUS.\n- RFA: Tumor ablated.\n- No complications.",
            2: "PROCEDURE: Electromagnetic navigation bronchoscopy (ENB) and radial EBUS were employed to localize a squamous cell carcinoma in the right lower lobe. Upon confirmation of probe placement, radiofrequency ablation (RFA) was performed to achieve local tumor destruction. (CPT 31641, 31627, 31654).",
            3: "Codes: 31641 (RFA), 31627 (ENB), 31654 (REBUS).\nNote: 31622 (Diagnostic) is bundled.\nIndication: Therapeutic ablation of SCC.",
            4: "Resident Note\nProcedure: RFA RLL\nSteps:\n1. Navigated to RLL SCC with ENB.\n2. REBUS check.\n3. RFA probe in.\n4. Burned tumor.\nPlan: Admit.",
            5: "rll squamous cell cancer patient here for ablation used enb and radial ebus to find it put the rfa catheter in and cooked it good margins looks like handled well no bleeding.",
            6: "Bronchoscopy with ENB and radial EBUS guidance to a right lower lobe squamous cell carcinoma followed by radiofrequency ablation of the lesion. Navigation and ultrasound used for localization. Radiofrequency energy applied for tumor destruction.",
            7: "[Indication]\nRLL SCC, non-surgical.\n[Anesthesia]\nGA.\n[Description]\nENB/REBUS nav to RLL. RFA performed for tumor destruction.\n[Plan]\nAdmit.",
            8: "This patient with a right lower lobe squamous cell cancer underwent bronchoscopic ablation. We found the tumor using electromagnetic navigation and ultrasound. Once in position, we used a radiofrequency probe to heat and destroy the cancer cells.",
            9: "Procedure: Navigational thermal destruction (RFA) of airway tumor.\nAction: ENB and radial ultrasound guided the instrument to the RLL malignancy. Radiofrequency energy was applied to obliterate the lesion."
        },
        8: { # Note 8: PleurX (Invent details)
            1: "Proc: Tunneled Pleural Catheter (PleurX).\n- US Guidance.\n- Side: Right.\n- Fluid: Recurrent malignant effusion.\n- Drainage: Large volume.\n- Catheter tunneled/placed successfully.",
            2: "PROCEDURE: Under ultrasound guidance, a tunneled indwelling pleural catheter (PleurX) was placed in the right hemithorax for management of recurrent malignant pleural effusion. A subcutaneous tunnel was created, the catheter inserted, and large-volume drainage was facilitated. (CPT 32550).",
            3: "Code: 32550 (Insertion of tunneled pleural catheter).\nImaging: Ultrasound used (included).\nIndication: Malignant effusion.",
            4: "Resident Note\nProcedure: PleurX Placement\nSteps:\n1. Local anesthetic.\n2. US check.\n3. Tunnel created.\n4. Catheter in R pleural space.\n5. Drained 1L fluid.\nPlan: Home with drain instructions.",
            5: "putting in a pleurx catheter today for the right side effusion recurring cancer fluid used ultrasound to pick the spot numbed it up tunneled the line put it in drained a bunch of fluid worked great.",
            6: "Ultrasound-guided tunneled PleurX catheter placement for recurrent right malignant pleural effusion with large-volume drainage. Catheter tunneled and inserted without complication. Fluid drained.",
            7: "[Indication]\nRecurrent malignant effusion.\n[Anesthesia]\nLocal.\n[Description]\nUS guidance. Tunneled tract created. PleurX catheter inserted Right side. Fluid drained.\n[Plan]\nDischarge. Home nursing.",
            8: "We placed a PleurX catheter for this patient to help manage their recurring fluid buildup on the right side. Using ultrasound to guide us, we numbed the skin, created a tunnel under the skin, and inserted the catheter into the pleural space. We drained a large amount of fluid, and the catheter is working well.",
            9: "Procedure: Insertion of indwelling tunneled pleural drain.\nAction: Sonographic guidance utilized. Subcutaneous tunnel formed. Catheter introduced into right pleural cavity. Significant effusion evacuated."
        },
        9: { # Note 9: Robotic Ion TBBx (Invent details)
            1: "Proc: Robotic Bronch LLL Nodule.\n- Ion Platform.\n- REBUS confirmed.\n- Sampling: Forceps + Brush.\n- No complications.",
            2: "PROCEDURE: Robotic Ion navigational bronchoscopy was utilized to access a peripheral left lower lobe nodule. Radial EBUS confirmation was obtained. Diagnostic sampling was performed via forceps biopsies and bronchial brushing. (CPT 31628, 31623, 31627, 31654).",
            3: "Codes: 31628 (TBBx), 31623 (Brush), 31627 (Nav), 31654 (REBUS).\nNote: 31622 bundled.\nTarget: LLL Nodule.",
            4: "Resident Note\nProcedure: Ion Bronch\nSteps:\n1. Nav to LLL.\n2. REBUS check.\n3. Forceps bx x5.\n4. Brush bx x1.\nPlan: Path pending.",
            5: "robotic case ion system left lower lobe nodule found it with radial ebus took some biopsy bites with forceps and did a brush too sending for path patient did fine.",
            6: "Robotic Ion navigational bronchoscopy with radial EBUS confirmation and forceps biopsies plus brushings of a peripheral left lower lobe nodule. Navigation successful. Samples obtained via forceps and brush.",
            7: "[Indication]\nLLL Nodule.\n[Anesthesia]\nGA.\n[Description]\nIon Nav to LLL. REBUS confirm. TBBx and Brushings taken.\n[Plan]\nRecovery.",
            8: "We used the Robotic Ion system to biopsy a nodule in the left lower lobe. We confirmed the location with ultrasound and then took several samples using both forceps and a brush to ensure we got enough tissue for diagnosis.",
            9: "Procedure: Robotic-assisted navigational sampling.\nAction: Ion platform guided to LLL target. Radial ultrasound verified position. Tissue harvested via forceps and cytological brushing."
        }
    }
    return variations

def get_base_data_mocks():
    # Names lists corresponding to 9 variations per note.
    # Note 0: Natalie Reed
    # Note 1: Carlos Rivera
    # Note 2: Megan Collins
    # Note 3: Zachary Price
    # Note 4: Julia Bennett
    # Note 5: Ryan Cooper
    # Note 6: (Summary) -> "Alice Johnson"
    # Note 7: (Summary) -> "Bob Williams"
    # Note 8: (Summary) -> "Charlie Brown"
    # Note 9: (Summary) -> "Diana Prince"
    
    return [
        {"idx": 0, "orig_name": "Natalie Reed", "orig_age": 53, "names": ["Sarah Connor", "Ellen Ripley", "Leia Organa", "Dana Scully", "Clarice Starling", "Laurie Strode", "Sidney Prescott", "Nancy Thompson", "Gale Weathers"]},
        {"idx": 1, "orig_name": "Carlos Rivera", "orig_age": 47, "names": ["Juan Rico", "Tony Montana", "Manny Ribera", "Chaucer", "William Thatcher", "Wat Tyler", "Roland Deschain", "Eddie Dean", "Jake Chambers"]},
        {"idx": 2, "orig_name": "Megan Collins", "orig_age": 60, "names": ["Jessica Fletcher", "Jane Marple", "Harriet Vane", "Nancy Drew", "Veronica Mars", "Lisbeth Salander", "Hermione Granger", "Katniss Everdeen", "Beatrix Kiddo"]},
        {"idx": 3, "orig_name": "Zachary Price", "orig_age": 66, "names": ["Walter White", "Jesse Pinkman", "Saul Goodman", "Mike Ehrmantraut", "Gustavo Fring", "Hank Schrader", "Skyler White", "Marie Schrader", "Flynn White"]},
        {"idx": 4, "orig_name": "Julia Bennett", "orig_age": 62, "names": ["Elizabeth Bennet", "Jane Bennet", "Mary Bennet", "Kitty Bennet", "Lydia Bennet", "Charlotte Lucas", "Caroline Bingley", "Lady Catherine", "Georgiana Darcy"]},
        {"idx": 5, "orig_name": "Ryan Cooper", "orig_age": 69, "names": ["Fox Mulder", "Walter Skinner", "Cigarette Man", "Alex Krycek", "John Doggett", "Monica Reyes", "Deep Throat", "X", "The Lone Gunmen"]},
        {"idx": 6, "orig_name": "Alice Johnson", "orig_age": 55, "names": ["Lara Croft", "Jill Valentine", "Claire Redfield", "Ada Wong", "Samus Aran", "Princess Zelda", "Princess Peach", "Chun Li", "Cammy White"]},
        {"idx": 7, "orig_name": "Bob Williams", "orig_age": 65, "names": ["Mario Mario", "Luigi Mario", "Wario", "Waluigi", "Bowser Koopa", "Toad", "Yoshi", "Donkey Kong", "Diddy Kong"]},
        {"idx": 8, "orig_name": "Charlie Brown", "orig_age": 70, "names": ["Linus Van Pelt", "Lucy Van Pelt", "Schroeder", "Pig-Pen", "Peppermint Patty", "Marcie", "Franklin", "Snoopy", "Woodstock"]},
        {"idx": 9, "orig_name": "Diana Prince", "orig_age": 50, "names": ["Bruce Wayne", "Clark Kent", "Barry Allen", "Arthur Curry", "Victor Stone", "Hal Jordan", "Oliver Queen", "Dinah Lance", "Barbara Gordon"]},
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
        
        # Determine base age - check if it exists in registry, else use mock
        if "registry_entry" in original_note and original_note["registry_entry"].get("patient_age"):
             orig_age = original_note["registry_entry"]["patient_age"]
        else:
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
            
            # Update note_text with the variation if available
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen with full dictionary)
                note_entry["note_text"] = f"Variation {style_num} for note {idx} (Placeholder)"

            # Ensure registry_entry exists
            if "registry_entry" not in note_entry:
                note_entry["registry_entry"] = {}

            # Update registry_entry fields
            note_entry["registry_entry"]["patient_age"] = new_age
            note_entry["registry_entry"]["procedure_date"] = rand_date_str
            
            # Update patient MRN to make it unique
            if "patient_mrn" in note_entry["registry_entry"]:
                note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            else:
                note_entry["registry_entry"]["patient_mrn"] = f"UNKNOWN_syn_{idx}_{style_num}"

            # Update providers/patient name in registry if distinct field exists? 
            # The input JSON structure doesn't always have a 'patient_name' field in registry_entry (it's often in note_text),
            # but we can add it to metadata or just rely on note_text.
            # We will add a synthetic metadata block.
            
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_blvr_notes_part_022.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()