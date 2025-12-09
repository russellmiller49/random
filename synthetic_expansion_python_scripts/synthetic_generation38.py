import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_038.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds manually crafted text variations based on the styles requested.
    # Mapping: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # John M. Anderson (Microwave Ablation RUL)
            1: "Proc: Bronchoscopy w/ Microwave Ablation.\nTarget: 2.3cm RUL nodule.\nNav: SuperDimension + Radial EBUS confirmed lesion.\nAblation: Emprint probe, 65W x 5min. Temp 85C.\nPost-ablation: Hyperechoic zone seen. No bleeding.\nPlan: Admit, CT in 6h.",
            2: "OPERATIVE REPORT: ELECTROMAGNETIC NAVIGATION BRONCHOSCOPY WITH MICROWAVE ABLATION.\nINDICATION: A 67-year-old male with severe COPD and a PET-avid RUL adenocarcinoma presented for non-surgical management. \nPROCEDURE: Under general anesthesia, the airways were surveyed. Using electromagnetic guidance, the RUL posterior segment nodule was localized. Radial EBUS confirmed a concentric view. A microwave ablation catheter was advanced. Ablation was performed at 65 watts for 5 minutes, achieving a target temperature of 85 degrees Celsius. Post-ablation imaging demonstrated a satisfactory zone of coagulative necrosis. The patient tolerated the procedure well.",
            3: "CPT Justification:\n- 31627: Electromagnetic navigation used to guide catheter to RUL target.\n- 31654: Radial EBUS probe utilized to confirm tool-in-lesion position.\n- 31641: Microwave ablation performed (Destruction of tumor). Probe: Emprint. Settings: 65W, 5 min. Target destroyed.\nNote: Diagnostic bronchoscopy (31622) is bundled.",
            4: "Procedure Note (Resident)\nPatient: John Anderson\nAttending: Dr. Chen\nProcedure: MWA of RUL nodule.\nSteps:\n1. Intubated 8.5 ETT.\n2. Navigated to RUL posterior segment.\n3. Confirmed with Radial EBUS (hypoechoic lesion).\n4. Microwave probe inserted.\n5. Burned at 65 Watts for 5 mins.\n6. Re-checked: good ablation zone.\nPlan: Post-op CT.",
            5: "dictation for mr anderson... we did the microwave ablation today right upper lobe... navigation went well used the superdimension... radial ebus saw the lesion clearly... put the emprint probe in and cooked it at 65 watts for five minutes... temp got up to 85... no bleeding noted after... extubated fine sending to pacu.",
            6: "Bronchoscopic electromagnetic navigation with microwave ablation of right upper lobe peripheral nodule. 67-year-old gentleman with incidentally discovered 2.3 cm spiculated nodule. Electromagnetic navigation bronchoscopy performed using superDimension system. Planning software identified target nodule in RUL posterior segment. Radial EBUS performed demonstrating target lesion in contact position. Microwave ablation probe advanced to target site. Ablation parameters: 65 watts, 5 minute duration. Post-ablation radial EBUS demonstrated hyperechoic changes consistent with coagulative necrosis. No complications.",
            7: "[Indication]\nInoperable RUL adenocarcinoma (2.3cm) in patient with severe COPD.\n[Anesthesia]\nGeneral Anesthesia, 8.5 ETT.\n[Description]\nNavigated to RUL posterior segment via EMN. Radial EBUS confirmed target. Cone-beam CT verified tool placement. Microwave ablation performed (65W, 5 min). Post-ablation imaging confirmed necrosis.\n[Plan]\nAdmit for observation. CT chest in 6 hrs.",
            8: "John underwent a bronchoscopy to treat a lung cancer nodule in his right upper lobe using heat energy. Because his lungs are too weak for surgery, we used microwave ablation. We navigated a small catheter to the tumor using a GPS-like system and confirmed its location with ultrasound. We then inserted the microwave probe and treated the area for 5 minutes at high heat. The follow-up ultrasound showed the tumor was effectively treated.",
            9: "Procedure: Bronchoscopic thermal destruction of pulmonary neoplasm.\nTechnique: Electromagnetic guidance deployed to localize RUL lesion. Ultrasonic confirmation achieved. Microwave energy utilized to induce coagulative necrosis (65W/300s). \nOutcome: Target ablated."
        },
        1: { # David W. Thompson (Radiofrequency Ablation RLL)
            1: "Proc: RFA of RLL nodule.\nNav: Veran system to RB9.\nConfirm: Radial EBUS + Cone Beam CT.\nAblation: RFA probe, 90C target. Cycle 1: 8min. Cycle 2: 6min (overlap).\nFindings: Necrosis confirmed on EBUS.\nPlan: Admit, CXR 4hr, CT 24hr.",
            2: "OPERATIVE NARRATIVE: The patient underwent bronchoscopic radiofrequency ablation for a biopsy-proven RLL adenocarcinoma. Following induction of general anesthesia, the Veran navigation system was utilized to catheterize the lateral basal segment. Radial EBUS and Cone-Beam CT confirmed central probe placement within the 2.7 cm lesion. RFA was delivered in two overlapping cycles (8 minutes and 6 minutes) at a target temperature of 90 degrees Celsius. Post-procedural imaging confirmed an adequate ablation zone.",
            3: "Coding Summary:\n- 31641: Bronchoscopic destruction of tumor (RFA). Two cycles performed to cover lesion + margin.\n- 31627: Electromagnetic navigation (Veran system) used for localization.\n- 31654: Radial EBUS used for target confirmation.\nMedical Necessity: Inoperable malignancy.",
            4: "Procedure: RFA Lung\nPt: David Thompson\nSteps:\n1. GA, 8.5 Tube.\n2. Veran nav to RLL (RB9).\n3. REBUS + Spin CT to confirm.\n4. RFA probe in.\n5. Burn 1: 8 mins @ 90C.\n6. Pull back 5mm.\n7. Burn 2: 6 mins @ 90C.\n8. Extubated stable.\nPlan: Admit.",
            5: "procedure note david thompson... rll radiofrequency ablation... used the veran system navigated to the lateral basal segment... confirmed with radial ebus and the cone beam ct... put the rfa probe in did two burns first one 8 mins second one 6 mins both at 90 degrees... impedance looked good... patient did great no pneumothorax on the table.",
            6: "Flexible bronchoscopy with complete airway survey. Electromagnetic navigation bronchoscopy with real-time cone-beam CT guidance. Radial endobronchial ultrasound probe confirmation of target lesion. Radiofrequency ablation of right lower lobe peripheral nodule. Target lesion in right lower lobe lateral basal segment (RB9) identified. Position confirmed with radial endobronchial ultrasound probe. Cone-beam CT performed. Radiofrequency ablation protocol initiated per institutional guidelines. Settings: impedance-controlled algorithm, target temperature 90\u00b0C, duration 8 minutes for initial ablation cycle. Second ablation cycle performed: 6 minutes.",
            7: "[Indication]\nRLL Adenocarcinoma, medically inoperable.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nNavigated to RLL RB9. Confirmed via REBUS and Cone Beam CT. RFA performed: Cycle 1 (8 min), Cycle 2 (6 min). Target temp 90C. Good ablation zone visualized.\n[Plan]\nAdmit 7 East. CT chest in 24h.",
            8: "We performed a procedure to burn a tumor in Mr. Thompson's right lower lung using radiofrequency energy. We used a navigation system and a special CT scan in the operating room to place the probe exactly in the center of the tumor. We heated the tumor to 90 degrees Celsius for a total of 14 minutes. The ultrasound afterwards showed the tumor had been successfully treated.",
            9: "Procedure: Bronchoscopic radiofrequency tumor destruction.\nLocalization: Electromagnetic tracking and endobronchial ultrasonography.\nTherapy: Delivered thermal energy (RFA) to RLL lesion. Two overlapping treatment zones created to ensure margin coverage.\nStatus: Stable."
        },
        2: { # David Kim (Nav Bronch LUL GGO)
            1: "Proc: Nav Bronch LUL.\nTarget: 9mm GGO.\nTools: EMN + Radial EBUS (concentric).\nSamples: TBNA x2, Bx x4, Brush x1.\nFluoro: 2.8 min.\nComplications: None.",
            2: "PROCEDURE NOTE: Electromagnetic Navigation Bronchoscopy.\nINDICATION: Evaluation of a 9mm ground-glass opacity in the left upper lobe.\nPROCEDURE: Using virtual bronchoscopic planning and electromagnetic navigation, the apical-posterior segment of the LUL was catheterized. Radial EBUS confirmed a concentric echotexture consistent with the target lesion. Diagnostic sampling was performed utilizing transbronchial needle aspiration, forceps biopsy, and cytology brushing. There were no immediate complications.",
            3: "CPT Codes Supported:\n- 31627 (Navigation)\n- 31654 (Radial EBUS)\n- 31629 (TBNA)\n- 31623 (Brush)\n- 31628 (Biopsy - bundled into 31629 for same site, but documented performed).\nNotes: Fluoroscopy utilized.",
            4: "Resident Note\nPt: David Kim\nProcedure: Nav Bronch\nSteps:\n1. LUL target mapped.\n2. Navigated to target.\n3. REBUS showed tool-in-lesion.\n4. Needles x2, Biopsies x4, Brush x1.\n5. No pneumo.\nPlan: Pathology f/u.",
            5: "bronch note david kim... lul ggo 9mm... used the navigation system got right to it... radial ebus confirmed concentric view... took a bunch of samples tbna biopsy brush... patient tolerated it well no bleeding no pneumothorax... path pending.",
            6: "LUL peripheral ground-glass nodule 9mm, no bronchus sign. Virtual bronchoscopy planning completed pre-procedure. Electromagnetic navigation system utilized. Target registration successful. Extended working channel advanced to LUL apical-posterior segment. Radial EBUS probe confirmed tool-in-lesion. Transbronchial needle aspiration \u00d72. Transbronchial forceps biopsy \u00d74. Cytology brush \u00d71. No pneumothorax on immediate post-procedure CXR.",
            7: "[Indication]\n9mm LUL ground-glass nodule.\n[Anesthesia]\nLocal/Topical only (Awake).\n[Description]\nEMN guidance to LUL apical-posterior. Radial EBUS concentric view. Samples: TBNA, Bx, Brush.\n[Plan]\nDischarge. Clinic f/u 1 week.",
            8: "Mr. Kim underwent a navigation bronchoscopy to biopsy a small, hazy nodule in his left upper lung. We kept him awake with just numbing medicine. Using a computerized guidance system, we steered a catheter to the nodule and confirmed we were in the right spot with ultrasound. We took needle samples, biopsies, and brushings. He did well with no collapsed lung.",
            9: "Procedure: Guided bronchoscopic sampling.\nTarget: Left Upper Lobe sub-solid lesion.\nGuidance: Electromagnetic tracking + peripheral ultrasound.\nAction: Acquired fine needle aspirates, parenchymal tissue samples, and brush cytology.\nOutcome: Diagnostic material obtained."
        },
        3: { # Susan Taylor (EBUS 5 Stations)
            1: "Proc: EBUS-TBNA.\nStations: 2R, 4R, 4L, 7, 11R.\nROSE: 4R/7 Malignant. Others benign/reactive.\nPlan: Oncology.",
            2: "PROCEDURE: Endobronchial Ultrasound Staging.\nINDICATION: Mediastinal lymphadenopathy.\nFINDINGS: A systematic mediastinal evaluation was performed. Stations 2R, 4R, 4L, 7, and 11R were visualized and sampled. Rapid on-site evaluation (ROSE) indicated metastatic carcinoma in stations 4R and 7. Stations 2R, 4L, and 11R demonstrated reactive lymphocytes. No complications occurred.",
            3: "Billing Code: 31653 (EBUS sampling 3+ stations).\nStations Sampled:\n1. 2R\n2. 4R\n3. 4L\n4. 7\n5. 11R\nTotal: 5 stations. Meets criteria for 31653.",
            4: "Procedure: EBUS\nPt: Susan Taylor\nSteps:\n1. Scope in.\n2. Sampled 2R, 4R, 4L, 7, 11R.\n3. ROSE positive in 4R and 7.\n4. Others benign.\n5. Stable.\nPlan: Staging.",
            5: "ebus note for susan taylor... did the full staging... hit 5 stations 2r 4r 4l 7 and 11r... rose said cancer in 4r and 7... rest looked reactive... patient did fine conscious sedation used... send for molecular markers.",
            6: "EBUS-TBNA systematic approach. Station 2R: 9mm, 3 passes, ROSE shows reactive lymphocytes. Station 4R: 14mm, 4 passes, ROSE positive for metastatic carcinoma. Station 4L: 10mm, 3 passes, ROSE benign. Station 7: 17mm, 4 passes, ROSE positive for metastatic carcinoma. Station 11R: 8mm, 3 passes, ROSE adequate, benign. Staging indication: Yes. Systematic sequence: Yes.",
            7: "[Indication]\nMediastinal adenopathy, PET unavailable.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS-TBNA of 5 stations (2R, 4R, 4L, 7, 11R). Malignancy identified in 4R and 7.\n[Plan]\nOncology referral.",
            8: "Susan underwent an EBUS procedure to investigate enlarged lymph nodes. Since she couldn't have a PET scan, we sampled five different areas in her chest to be thorough. The pathologist in the room found cancer cells in the right paratracheal and subcarinal nodes. The other nodes were benign. We sent the samples for further genetic testing.",
            9: "Procedure: Ultrasonic mediastinal staging.\nAction: Sampled stations 2R, 4R, 4L, 7, and 11R via transbronchial needle aspiration.\nFindings: Cytologic evidence of malignancy in 4R and 7. Benign cellularity elsewhere."
        },
        4: { # Lisa Anderson (Nav Bronch LLL)
            1: "Proc: Nav Bronch LLL.\nTarget: 19mm nodule.\nNav: EMN + Radial EBUS (concentric).\nSamples: TBNA x3, Bx x4, Brush x2.\nResult: No PTX. Stable.",
            2: "PROCEDURE NOTE: Electromagnetic Navigation Bronchoscopy.\nIndication: PET-avid LLL pulmonary nodule (19mm).\nProcedure: The patient was sedated and the airway anesthetized. A virtual pathway was created and followed to the LLL target. Radial EBUS confirmed a concentric tool-in-lesion position. Diagnostic samples were obtained via needle aspiration, forceps biopsy, and cytological brushing. Post-procedure imaging ruled out pneumothorax.",
            3: "CPT Codes:\n- 31627: Navigation.\n- 31654: Radial EBUS.\n- 31629: TBNA.\n- 31623: Brush.\n- 31628: Biopsy (bundled with 31629).\nFluoro time: 5.1 min.",
            4: "Resident Note\nPt: Lisa Anderson\nProc: EMN Bronch\nSteps:\n1. Navigated to LLL.\n2. Radial probe: concentric view.\n3. 3 needle passes.\n4. 4 biopsies.\n5. 2 brushes.\n6. No pneumo on CXR.\nPlan: Clinic f/u.",
            5: "nav bronch for lisa anderson... lll nodule 19mm... got there with the electromagnetic system... radial ebus looked good concentric... took needle biopsy and brush samples... fluoro used about 5 mins... patient stable no pneumothorax... discharge home.",
            6: "EMN for LLL nodule - concentric pattern achieved on radial EBUS. Fluoro 5.1 min, DAP 195 cGy*cm\u00b2. Samples: needle \u00d73, biopsy \u00d74, brush \u00d72. Tool-in-lesion: YES. Localization success: YES. Post-XR: no PTX, patient stable, d/c home after 2hr.",
            7: "[Indication]\n19mm LLL nodule.\n[Anesthesia]\nModerate Sedation.\n[Description]\nNavigation to LLL. Radial EBUS confirmed target. Samples: TBNA, Biopsy, Brush.\n[Plan]\nPathology follow-up.",
            8: "Lisa had a navigation bronchoscopy for a spot in her lower left lung. We successfully guided our tools to the 19mm nodule and confirmed the location with ultrasound. We took multiple samples using a needle, forceps, and a brush. She recovered well and the chest x-ray showed no lung collapse.",
            9: "Procedure: Guided bronchoscopic biopsy.\nTarget: Left Lower Lobe lesion.\nTechnique: Electromagnetic localization verified by peripheral ultrasound.\nAction: Harvested tissue via aspiration, forceps, and brushing.\nOutcome: Successful sampling."
        },
        5: { # Linda Thompson (EBUS Station 7)
            1: "Proc: Targeted EBUS Stn 7.\nIndication: Biopsy enlarged node.\nFindings: Stn 7 (31mm), SUV 9.4.\nAction: 5 passes. ROSE positive.\nCode: 31652 (1 station).",
            2: "PROCEDURE: Targeted Endobronchial Ultrasound.\nINDICATION: Isolated subcarinal lymphadenopathy.\nPROCEDURE: The bronchoscope was advanced to the subcarinal space. Station 7 was identified, measuring 31mm. Transbronchial needle aspiration was performed (5 passes). ROSE confirmed adequate cellularity and molecular sufficiency. No other stations were sampled per pre-procedure plan.",
            3: "Billing: 31652 (EBUS sampling 1-2 stations).\nSpecifics: Only Station 7 was sampled.\nMedical Necessity: Tissue diagnosis of PET-avid node.",
            4: "Procedure: EBUS (Targeted)\nPt: Linda Thompson\nSteps:\n1. Scope to Stn 7.\n2. 5 needle passes.\n3. ROSE said adequate.\n4. Done.\nPlan: Path results.",
            5: "targeted ebus for linda thompson... just went for station 7 big node 31mm... took 5 samples rose said it was good... didn't check other nodes per oncology... patient tolerated fine.",
            6: "Procedure indication: Biopsy of enlarged station 7 node, no staging indication. Single station targeted: STATION 7 - subcarinal node measures 31mm short axis on EBUS, PET SUV 9.4. 5 needle passes performed with 22G Expect needle. ROSE present: technician reported adequate cellularity. Impression: Targeted EBUS-TBNA of PET-avid subcarinal lymphadenopathy.",
            7: "[Indication]\nEnlarged Subcarinal Node (Station 7).\n[Anesthesia]\nModerate Sedation.\n[Description]\nTargeted EBUS-TBNA of Station 7 only. 5 passes obtained.\n[Plan]\nHome.",
            8: "Linda came in for a biopsy of a specific lymph node under her windpipe (Station 7). We focused only on this node as requested by her oncologist. It was large (31mm) and active on PET. We took 5 samples to ensure we have enough for genetic testing. The procedure went smoothly.",
            9: "Procedure: Focal EBUS-guided aspiration.\nTarget: Subcarinal lymph node (Station 7).\nAction: Acquired cytological specimens via needle aspiration.\nResult: Adequate material for molecular profiling."
        },
        6: { # Frank Wilson (EBUS + RUL Bx)
            1: "Proc: EBUS + RUL Biopsy.\nEBUS: Stns 4R, 7 sampled (31652).\nLung: RUL lesion Bx x4, Brush x2 (31628, 31623).\nROSE: Nodes positive.\nPlan: Path pending.",
            2: "PROCEDURE NOTE: Bronchoscopy with EBUS and Transbronchial Biopsy.\nMediastinal staging was performed first; stations 4R and 7 were sampled under EBUS guidance, both showing malignancy on ROSE. Subsequently, the RUL parenchymal lesion was identified and sampled via transbronchial forceps biopsy and brushing. The procedure was uncomplicated.",
            3: "Coding: \n- 31652 (EBUS 1-2 stations: 4R, 7).\n- 31628 (Transbronchial biopsy lung lesion).\n- 31623 (Brushing).\nNote: Diagnostic bronch 31622 is bundled.",
            4: "Procedure: EBUS & Lung Biopsy\nPt: Frank Wilson\nSteps:\n1. EBUS: Sampled 4R and 7.\n2. RUL lesion: Forceps biopsy and brush.\n3. ROSE + for nodes.\n4. Stable.\nPlan: Oncology.",
            5: "frank wilson bronch... did ebus first hit 4r and 7 both positive... then went to the rul lesion took biopsies and brushes... patient did fine ramsay 3... waiting on final path.",
            6: "Dx bronch + EBUS. EBUS: 4R (9mm) x3, 7 (12mm) x4, both ROSE+, PET+ both. N3-N2-N1 systematic, photos. RUL lesion bx x4, brush x2. No cx. Path pending.",
            7: "[Indication]\nLung mass + Adenopathy.\n[Anesthesia]\nModerate Sedation.\n[Description]\n1. EBUS: 4R, 7 sampled (Positive).\n2. RUL Lesion: Biopsied and Brushed.\n[Plan]\nFollow-up.",
            8: "Frank underwent a combined procedure. We first used EBUS to check his lymph nodes; samples from stations 4R and 7 both looked like cancer on the preliminary check. We then moved the scope to biopsy the main mass in his right upper lung using forceps and a brush.",
            9: "Procedure: Staging EBUS and parenchymal sampling.\nAction: Aspirated nodal stations 4R and 7. Acquired tissue from RUL mass via forceps and brush.\nResult: Nodal malignancy confirmed."
        },
        7: { # Robert Mosbey Wiggins (Stent Removal + Cryo)
            1: "Proc: Rigid Bronch, Stent Removal, Cryo.\nFindings: Granulation tissue obstructing Y-stent (50-60%).\nAction: Stent removed intact. Cryotherapy applied to granulation bases.\nPlan: Stent holiday. Observe.",
            2: "OPERATIVE REPORT: Rigid Bronchoscopy with Stent Extraction.\nINDICATION: Obstructed tracheal Y-stent.\nPROCEDURE: Significant granulation tissue was noted at the distal limbs of the Y-stent. Using rigid optical forceps, the stent was grasped and extracted intact. Following removal, cryotherapy was applied to the residual granulation tissue to restore airway patency. Significant tracheobronchomalacia was noted post-removal.",
            3: "Coding: \n- 31638: Removal of tracheal stent (existing Y-stent removed).\n- 31641: Destruction of tumor/stenosis (Cryotherapy to granulation tissue).\nMedical Necessity: Symptomatic airway obstruction.",
            4: "Procedure: Stent Removal\nPt: Robert Wiggins\nSteps:\n1. Rigid bronch in.\n2. Saw blocked stent (granulation).\n3. Pulled stent out with forceps.\n4. Froze the granulation tissue (Cryo).\n5. Airway floppy (TBM).\nPlan: Ward.",
            5: "op note for robert wiggins... stent removal... rigid scope used... granulation tissue blocking the stent ends... pulled the whole y stent out intact... then used cryo to treat the granulation tissue... airway collapses a lot without the stent... sending to pacu.",
            6: "Rigid and flexible bronchoscopy with Tracheal stent removal. Cryotherapy to granulation tissue. At the distal aspect of the right mainstem limb there was granulation tissue causing about 50% obstruction. The forceps were used to grasp the proximal limb of the tracheal stent and were rotated repeatedly while withdrawing the stent into the rigid bronchoscope. The stent was subsequently removed without difficulty. The 1.9mm flexible cryoprobe was inserted through the working channel and cryotherapy was performed.",
            7: "[Indication]\nObstructed Airway Stent.\n[Anesthesia]\nGeneral.\n[Description]\nY-stent removed via rigid bronchoscopy. Granulation tissue treated with Cryotherapy (31641). TBM noted.\n[Plan]\nStent holiday.",
            8: "Robert needed his airway stent removed because tissue was growing over the ends and blocking it. We used a rigid scope to carefully pull the Y-shaped stent out. After it was out, we used a freezing probe (cryotherapy) to treat the overgrowth tissue. His airway is very floppy without the stent, but we are giving him a break from the device to let things heal.",
            9: "Procedure: Rigid endoscopic stent retrieval.\nAction: Extracted indwelling Y-stent. Ablated granulation tissue utilizing cryotherapy.\nFindings: Severe tracheobronchomalacia unmasked."
        },
        8: { # Jennifer Lee (Nav Bronch RLL)
            1: "Proc: Nav Bronch RLL.\nTarget: 22mm solid nodule.\nNav: EMN + Radial EBUS.\nSamples: TBNA x3, Bx x4, Brush x2.\nComplication: 10% Pneumothorax.\nPlan: Conservative management.",
            2: "PROCEDURE NOTE: Electromagnetic Navigation Bronchoscopy.\nINDICATION: 2.2 cm RLL nodule.\nPROCEDURE: The target in the RLL superior segment was localized using electromagnetic navigation. Radial EBUS confirmed concentric visualization. Sampling was performed via needle, forceps, and brush. Post-procedure imaging revealed a small apical pneumothorax which did not require intervention. The patient was monitored and discharged stable.",
            3: "CPT Justification:\n- 31627: EMN used.\n- 31654: Radial EBUS used.\n- 31629: TBNA.\n- 31623: Brush.\n- 31628: Biopsy.\nComplication: Pneumothorax (ICD-10 J93.9), conservative management.",
            4: "Resident Note\nPt: Jennifer Lee\nProc: Nav Bronch\nSteps:\n1. Nav to RLL.\n2. REBUS: Concentric.\n3. Samples: Needle, Bx, Brush.\n4. CXR: Small pneumo.\n5. Pt stable.\nPlan: Obs x4hr then home.",
            5: "nav bronch jennifer lee... rll nodule... took a while to find it had to reposition... eventually got concentric view... took all the samples... patient got a small pneumothorax about 10 percent... watched her for 4 hours she was fine... discharged.",
            6: "Indication: Peripheral RLL nodule 22mm, solid, bronchus sign present on thin-cut CT. Navigation Protocol: Guide sheath advanced under combined EM navigation + fluoroscopic guidance. Tool-in-lesion NOT initially confirmed - repositioned \u00d72. Final radial probe position showed concentric EBUS pattern. Sampling: Aspiration needle \u00d73, Forceps biopsies \u00d74, Brush cytology \u00d72. Post-procedure CXR: Small apical pneumothorax ~10%, patient asymptomatic. Conservative management.",
            7: "[Indication]\n22mm RLL nodule.\n[Anesthesia]\nModerate Sedation.\n[Description]\nNavigated to RLL. Radial EBUS confirmed concentric view. TBNA, Bx, Brush performed. Small PTX noted post-op.\n[Plan]\nObserve and Discharge.",
            8: "Jennifer underwent a navigation procedure for a nodule in her right lower lung. It took a couple of tries to align the catheter perfectly, but we eventually got a good ultrasound view. We took multiple samples. Afterward, the x-ray showed a small lung collapse (pneumothorax), but it was minor enough that she didn't need a chest tube and went home after a few hours of monitoring.",
            9: "Procedure: Guided bronchoscopic biopsy.\nTarget: Right Lower Lobe solid lesion.\nComplication: Iatrogenic pneumothorax (minor).\nAction: Localized lesion via EMN and REBUS. Sampled via needle, forceps, and brush. \nDisposition: Observation."
        },
        9: { # Barbara Wilson (EBUS Lymphoma)
            1: "Proc: EBUS-TBNA (Lymphoma protocol).\nStations: 4R, 4L, 7, 10R.\nFindings: Large atypical cells.\nAction: Samples sent fresh for Flow Cytometry.\nCode: 31653.",
            2: "PROCEDURE: Endobronchial Ultrasound for Lymphoma Staging.\nINDICATION: Hodgkin lymphoma.\nPROCEDURE: Stations 4R, 4L, 7, and 10R were sampled. ROSE demonstrated atypical large cells consistent with lymphoma. Samples were processed specifically for flow cytometry and molecular analysis (fresh/RPMI). The procedure was uncomplicated.",
            3: "Billing: 31653 (3+ stations).\nStations: 4R, 4L, 7, 10R.\nSpecial Handling: Flow cytometry samples obtained (critical for lymphoma Dx).",
            4: "Procedure: EBUS (Lymphoma)\nPt: Barbara Wilson\nSteps:\n1. Sampled 4R, 4L, 7, 10R.\n2. Put samples in pink fluid (Flow).\n3. ROSE said lymphoma.\n4. No issues.\nPlan: Heme/Onc.",
            5: "ebus for barbara wilson... new lymphoma dx... need tissue for flow... hit 4 nodes 4r 4l 7 and 10r... sent everything fresh... rose saw the big cells... patient did fine.",
            6: "EBUS-TBNA TECHNIQUE: Systematic evaluation not strictly required for lymphoma but performed. Stations biopsied: Station 4R (18mm): 3 passes, ROSE shows atypical large cells. Station 4L (21mm): 3 passes, ROSE similar. Station 7 (16mm): 4 passes, ROSE adequate for flow cytometry. Station 10R (14mm): 3 passes, ROSE adequate. Special handling: Samples for flow cytometry, FISH, molecular markers as per heme-onc.",
            7: "[Indication]\nHodgkin Lymphoma Staging.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS-TBNA of 4 stations (4R, 4L, 7, 10R). Samples sent for Flow Cytometry.\n[Plan]\nHeme/Onc follow-up.",
            8: "Barbara needed an EBUS to stage her Hodgkin lymphoma. We sampled lymph nodes on both sides of the trachea and under the carina. Because it's lymphoma, we had to handle the samples carefully, putting them in a special solution for flow cytometry testing. The preliminary look in the room confirmed the presence of lymphoma cells.",
            9: "Procedure: Ultrasonic nodal sampling for hematologic malignancy.\nAction: Aspirated stations 4R, 4L, 7, and 10R. \nHandling: Specimens preserved in media for flow cytometric immunophenotyping.\nResult: Diagnostic material acquired."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the input file structure
    return [
        {"idx": 0, "orig_name": "John M. Anderson", "orig_age": 67, "gender": "Male", "names": ["Robert Miller", "James Davis", "William Wilson", "Richard Moore", "Joseph Taylor", "Charles Anderson", "Thomas Thomas", "Christopher Jackson", "Daniel White"]},
        {"idx": 1, "orig_name": "David W. Thompson", "orig_age": 73, "gender": "Male", "names": ["Michael Harris", "Paul Martin", "Mark Thompson", "Donald Garcia", "George Martinez", "Kenneth Robinson", "Steven Clark", "Edward Rodriguez", "Brian Lewis"]},
        {"idx": 2, "orig_name": "David Kim", "orig_age": 66, "gender": "Male", "names": ["Kevin Lee", "Ronald Walker", "Timothy Hall", "Jason Allen", "Jeffrey Young", "Ryan Hernandez", "Jacob King", "Gary Wright", "Nicholas Lopez"]},
        {"idx": 3, "orig_name": "Susan Taylor", "orig_age": 66, "gender": "Female", "names": ["Mary Hill", "Patricia Scott", "Linda Green", "Barbara Adams", "Elizabeth Baker", "Jennifer Gonzalez", "Maria Nelson", "Susan Carter", "Margaret Mitchell"]},
        {"idx": 4, "orig_name": "Lisa Anderson", "orig_age": 63, "gender": "Female", "names": ["Dorothy Perez", "Lisa Roberts", "Nancy Turner", "Karen Phillips", "Betty Campbell", "Helen Parker", "Sandra Evans", "Donna Edwards", "Carol Collins"]},
        {"idx": 5, "orig_name": "Linda Thompson", "orig_age": 62, "gender": "Female", "names": ["Ruth Stewart", "Sharon Sanchez", "Michelle Morris", "Laura Rogers", "Sarah Reed", "Kimberly Cook", "Deborah Morgan", "Jessica Bell", "Shirley Murphy"]},
        {"idx": 6, "orig_name": "Frank Wilson", "orig_age": 65, "gender": "Male", "names": ["Larry Bailey", "Scott Rivera", "Frank Cooper", "Justin Richardson", "Brandon Cox", "Raymond Howard", "Gregory Ward", "Samuel Torres", "Benjamin Peterson"]},
        {"idx": 7, "orig_name": "Robert Mosbey Wiggins", "orig_age": 70, "gender": "Male", "names": ["Patrick Gray", "Jack Ramirez", "Dennis James", "Jerry Watson", "Tyler Brooks", "Aaron Kelly", "Henry Sanders", "Douglas Price", "Peter Bennett"]},
        {"idx": 8, "orig_name": "Jennifer Lee", "orig_age": 57, "gender": "Female", "names": ["Cynthia Wood", "Angela Barnes", "Melissa Ross", "Brenda Henderson", "Amy Coleman", "Anna Jenkins", "Rebecca Perry", "Virginia Powell", "Kathleen Long"]},
        {"idx": 9, "orig_name": "Barbara Wilson", "orig_age": 58, "gender": "Female", "names": ["Pamela Patterson", "Martha Hughes", "Debra Flores", "Amanda Washington", "Stephanie Butler", "Carolyn Simmons", "Christine Foster", "Marie Gonzales", "Janet Bryant"]}
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
                note_entry["note_text"] = f"Variation {style_num} for Note {idx} (Content Placeholder)"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Some entries might not have patient_age field explicitly, but we can add/update
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
    output_filename = output_dir / "synthetic_blvr_notes_part_038.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()