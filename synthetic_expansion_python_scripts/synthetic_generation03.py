import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_003.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations for the notes 
    in consolidated_verified_notes_v2_8_part_003.json.
    Structure: Note_Index (0-8) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Robert Johnson (Nav Bronch/EBUS/Cryo)
            1: "Procedure: Navigational Bronchoscopy, Radial EBUS, Cryobiopsy RLL.\nIndication: 2.8cm RLL nodule.\nActions:\n- 8.0 ETT placed.\n- SuperDimension nav to RLL lateral basal.\n- Radial EBUS: concentric view, 27mm lesion.\n- Cryoprobe 1.9mm used. 4 samples taken (6 sec freeze).\n- Arndt blocker used for hemostasis. Minimal bleeding.\n- No pneumothorax on post-op check.",
            2: "HISTORY: Mr. Johnson, a 67-year-old male, presented with a 2.8 cm spiculated nodule in the right lower lobe. The metabolic activity on PET scan (SUV 4.5) raised concern for malignancy.\nPROCEDURE NARRATIVE: Following the induction of general anesthesia and orotracheal intubation, a systematic navigational bronchoscopy was undertaken utilizing the SuperDimension system. We achieved excellent registration error (4.2mm). The catheter was navigated to the lateral basal segment of the right lower lobe. Radial endobronchial ultrasound confirmed a concentric, heterogeneous lesion measuring 27 mm. Subsequently, transbronchial cryobiopsy was performed. Four specimens were obtained with a 1.9 mm probe using a 6-second freeze cycle. Prophylactic placement of an Arndt endobronchial blocker ensured adequate hemostasis.",
            3: "CPT Coding Justification:\n31627 (Navigational Bronchoscopy): Electromagnetic navigation system loaded with CT data; catheter navigated to RLL target.\n31654 (Radial EBUS): Peripheral lesion identified via radial probe ultrasound (concentric view) prior to biopsy.\n31628 (Transbronchial Biopsy): 1.9mm cryoprobe utilized to obtain parenchymal samples from the RLL lateral basal segment.\nNote: Endobronchial blocker used for control, not separately billable as therapeutic tamponade unless bleeding was excessive (it was minimal).",
            4: "Procedure Note - Pulmonary Service\nAttending: Dr. Williams\nResident: Dr. Lee\nProcedure: EMN Bronchoscopy w/ Cryobiopsy\nSteps:\n1. Time out. GA induced. 8.0 ETT.\n2. Registration with SuperDimension (Auto).\n3. Navigated to RLL nodule (Target 0.8cm away).\n4. Radial EBUS confirmation (Concentric).\n5. Biopsy: Cryoprobe x4 passes.\n6. Hemostasis: Balloon blocker used prophylactically.\n7. Extubation stable.",
            5: "patient robert johnson here for the lung nodule biopsy right lower side. we put him asleep general anesthesia tube size 8. used the superdimension navigation thing it worked good got us right to the spot in the rll. radial ebus showed the nodule perfectly concentric view. did the cryo biopsy took 4 pieces froze for 6 seconds each. david put the blocker up so no bleeding really. patient woke up fine sent to recovery check xray for pneumo.",
            6: "Mr. Johnson underwent electromagnetic navigation bronchoscopy for a right lower lobe nodule. Under general anesthesia with an 8.0 ETT, the SuperDimension system was registered with a fiducial error of 4.2mm. We navigated to the lateral basal segment. Radial EBUS confirmed the lesion location with a concentric view. We performed transbronchial cryobiopsy using a 1.9mm probe for 4 samples. An Arndt blocker was used to manage the airway and prevent bleeding. The patient tolerated the procedure well with no immediate complications.",
            7: "[Indication]\n2.8cm spiculated RLL nodule, PET avid.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nNavigated to RLL lateral basal segment (SuperDimension). Radial EBUS confirmed concentric lesion (27mm). Performed transbronchial cryobiopsy x4 samples (1.9mm probe). Arndt blocker used for hemostasis.\n[Plan]\nPathology pending. Clinic follow-up 1 week.",
            8: "The patient, Mr. Johnson, was brought to the bronchoscopy suite for evaluation of a right lower lobe nodule. After induction of general anesthesia, we proceeded with electromagnetic navigation. The target in the lateral basal segment was reached successfully. We utilized radial EBUS to visualize the lesion, noting a distinct concentric pattern. With the target confirmed, we used a cryoprobe to obtain four biopsies, freezing for six seconds each time. An endobronchial blocker was employed to ensure hemostasis between passes. The procedure concluded without complications, and the patient was extubated.",
            9: "PROCEDURE: Electromagnetic guidance bronchoscopy (CPT 31627), Radial sonography (CPT 31654), Transbronchial freeze-sampling (CPT 31628).\nDETAILS: Navigation established to the RLL target. Sonographic verification revealed a concentric mass. Four tissue samples were harvested using the cryoprobe. An airway occluder was deployed for bleeding control. Hemostasis was secured."
        },
        1: { # Andrew T Lewis (EBUS-TBNA)
            1: "Procedure: EBUS-TBNA.\nIndication: Lymphoma staging.\nFindings:\n- Station 7 (Subcarinal): 31mm, abnormal.\n- Station 4R: 22mm, abnormal.\n- Station 10R/11R: Prominent.\nSampling:\n- 7: 4 passes (Lymphoma +).\n- 4R: 3 passes (Lymphoma +).\n- 10R/11R: 2 passes each (Lymphoma +).\nSpecimens: Flow cytometry sent.",
            2: "CLINICAL SUMMARY: Mr. Lewis, a patient with known follicular lymphoma, presented for staging of new mediastinal adenopathy. \nOPERATIVE REPORT: The EBUS bronchoscope was introduced under MAC anesthesia. Systematic ultrasound evaluation of the mediastinum revealed significant lymphadenopathy. Station 7 (subcarinal) measured 31mm with abnormal echotexture. Station 4R was similarly enlarged (22mm). Hilar stations 10R and 11R were also prominent. \nINTERVENTION: Transbronchial needle aspiration was performed at all identified stations. Rapid on-site evaluation (ROSE) confirmed the presence of lymphoma cells in all sampled stations (7, 4R, 10R, 11R). Specimens were prioritized for flow cytometry.",
            3: "Billing Record:\nPrimary Code: 31653 (Bronchoscopy with EBUS sampling, 3 or more stations).\n- Station 1: Subcarinal (7)\n- Station 2: Right Lower Paratracheal (4R)\n- Station 3: Right Hilar (10R)\n- Station 4: Right Interlobar (11R)\nTools: EBUS Scope, TBNA Needle.\nPathology: Samples sent for Flow Cytometry due to lymphoma suspicion.",
            4: "Resident Procedure Note\nPatient: Andrew Lewis\nAttending: Dr. Singh\nProc: EBUS-TBNA\n\n1. MAC anesthesia.\n2. Scope passed orally.\n3. EBUS landmarks identified.\n4. LN 7, 4R, 10R, 11R visualized and sampled.\n5. ROSE positive for lymphoma in all stations.\n6. Needles rinsed for flow cytometry.\n7. Pt stable.",
            5: "dr singh here doing ebus on andrew lewis for the lymphoma staging. gave him mac anesthesia dr johnson handled that. went down looked at the nodes station 7 was huge 31mm took 4 sticks there. station 4r also big took 3 sticks. 10r and 11r looked suspicous took 2 sticks each. cytology guy in room said yup its lymphoma everywhere. sent it all for flow cytometry no issues during procedure thanks.",
            6: "EBUS-TBNA performed by Dr. Raj Singh for lymphoma staging on patient Andrew Lewis. Under MAC anesthesia, the ultrasound bronchoscope was introduced. We identified and sampled lymph nodes at stations 7 (31mm), 4R (22mm), 10R (17mm), and 11R (19mm). Needle aspiration was performed multiple times at each station. Rapid on-site evaluation confirmed lymphoma cells present in all samples. Material was sent for flow cytometry. The patient tolerated the procedure well without complications.",
            7: "[Indication]\nFollicular lymphoma staging, new mediastinal nodes.\n[Anesthesia]\nMAC.\n[Description]\nEBUS inspection: Nodes 7, 4R, 10R, 11R enlarged/abnormal. TBNA performed at all 4 stations. ROSE confirmed lymphoma cells. Samples sent for flow cytometry.\n[Plan]\nOncology follow-up for treatment planning.",
            8: "We performed an EBUS-TBNA on Mr. Lewis to stage his known follicular lymphoma. After inducing MAC anesthesia, we inserted the bronchoscope and systematically surveyed the mediastinum. We found significant adenopathy at station 7 and 4R, as well as prominent nodes at 10R and 11R. We aspirated each of these nodes using a dedicated needle. The pathologist present in the suite reviewed the slides immediately and confirmed the presence of lymphoma cells in all samples. We ensured adequate tissue was collected for flow cytometry before concluding.",
            9: "Procedure: Ultrasound-guided bronchial aspiration (CPT 31653).\nTarget: Lymphatic structures.\nAction: Sonographic visualization identified enlarged targets at stations 7, 4R, 10R, and 11R. These were accessed via needle aspiration. Cellular analysis confirmed malignancy (lymphoma). Specimens dispatched for immunophenotyping."
        },
        2: { # Duplicate Andrew Lewis (Used as distinct variation source)
            1: "Procedure: EBUS-TBNA\nTarget: Mediastinal/Hilar Nodes\nResults:\n- Stn 7: 31mm (Pos Lymphoma)\n- Stn 4R: 22mm (Pos Lymphoma)\n- Stn 10R: 17mm (Pos Lymphoma)\n- Stn 11R: 19mm (Pos Lymphoma)\nDisposition: Outpatient. Ref to Oncology.",
            2: "PROCEDURE INDICATION: Staging of mediastinal lymphadenopathy in a patient with history of follicular lymphoma.\nTECHNIQUE: Endobronchial ultrasound-guided transbronchial needle aspiration.\nFINDINGS: The subcarinal (7), right paratracheal (4R), right hilar (10R), and right interlobar (11R) lymph nodes were visualized and noted to be abnormal. TBNA was performed at each station. \nPATHOLOGY: Immediate cytologic evaluation was diagnostic for lymphoma at all sites sampled. Tissue was submitted for flow cytometric analysis.",
            3: "Code Selection: 31653\nRationale: EBUS sampling performed on >2 distinct nodal stations.\n- Station 7 sampled (4 passes)\n- Station 4R sampled (3 passes)\n- Station 10R sampled (2 passes)\n- Station 11R sampled (2 passes)\nAll samples adequate and diagnostic.",
            4: "Procedure Note\nPt: Andrew Lewis\nStaff: Dr. Singh\n\n- EBUS scope inserted.\n- Systematic exam of mediastinum.\n- Sampled 7, 4R, 10R, 11R.\n- ROSE: Lymphoma.\n- Complications: None.\n- Plan: Oncology referral.",
            5: "note for mr lewis procedure ebus tbna date 2/15/2025. dr singh performing. indication lymphoma. we saw big nodes at 7 and 4r and smaller ones at 10r 11r. stuck them all with the needle. rose said positive for lymphoma. sent for flow. patient did great no bleeding. discharge home.",
            6: "Under MAC anesthesia, an EBUS-TBNA was performed on Mr. Lewis. The indication was staging for follicular lymphoma. We visualized and sampled lymph nodes at stations 7, 4R, 10R, and 11R. All stations yielded positive results for lymphoma on rapid on-site evaluation. Samples were processed for flow cytometry. There were no complications.",
            7: "[Indication]\nLymphoma staging.\n[Anesthesia]\nMAC.\n[Description]\nEBUS-TBNA of stations 7, 4R, 10R, 11R. All nodes abnormal sonographically. Cytology positive for lymphoma.\n[Plan]\nFlow cytometry pending. Oncology consult.",
            8: "Mr. Lewis underwent an EBUS procedure today. We were looking to stage his lymphoma given new findings on his CT scan. We found several abnormal lymph nodes in the chest, specifically under the trachea and on the right side. We took needle samples from four different areas. The preliminary check in the room showed lymphoma cells in all the samples. We sent everything off for detailed testing.",
            9: "Procedure: Endosonographic needle aspiration.\nFindings: Lymphadenopathy identified at stations 7, 4R, 10R, 11R.\nIntervention: Targets were sampled via transbronchial aspiration.\nAnalysis: Immediate cytology revealed lymphoma. Tissue forwarded for flow cytometry."
        },
        3: { # Rachel Anderson (Nav/EBUS/TBNA/Forceps)
            1: "Procedure: Nav bronch, radial EBUS, TBNA, forceps biopsy, BAL.\nTarget: Left lingular lesion.\nFindings: Concentric EBUS view. Nav success.\nSampling: TBNA (ROSE+), brush, forceps.\nBAL: RUL posterior.\nComp: None. Minimal bleeding.",
            2: "PROCEDURE NOTE: Bronchoscopy with multimodal sampling.\nINDICATION: Migratory lung nodules.\nNARRATIVE: The airway was inspected using a Q190 bronchoscope; anatomy was normal. BAL was performed in the RUL posterior segment. The SuperDimension system was utilized to navigate to a lesion in the left lingula. Position was confirmed with radial EBUS demonstrating a concentric view. We performed TBNA under fluoroscopic guidance (ROSE showed histiocytes/giant cells), followed by triple needle brush and forceps biopsies. Hemostasis was achieved.",
            3: "Billing:\n- 31627: Navigation to lingular lesion.\n- 31654: Radial EBUS confirmation of lesion.\n- 31629: TBNA of lingular lesion.\n- 31628: Forceps biopsy of lingular lesion.\n- 31624: BAL of RUL (distinct lobe from biopsy).",
            4: "Resident Note\nPt: Rachel Anderson\nAttending: Dr. Wright\n1. Inspection: Normal.\n2. BAL: RUL (180cc).\n3. Nav: SuperD to Lingula.\n4. REBUS: Concentric.\n5. Sampling: TBNA, Brush, Forceps.\n6. ROSE: Histiocytes/Giant cells.\n7. Finished.",
            5: "rachel anderson procedure note. dr wright attending. we did a bronch with navigation and ebus. washed the rul first. then navigated to the lingula lesion. radial probe showed it nicely concentric. stuck it with the needle rose saw giant cells so maybe infection or sarcoid? did brush and forceps too. no bleeding really. patient woke up fine.",
            6: "Diagnostic bronchoscopy performed for migratory nodules. Airways inspected and found normal. RUL BAL performed. SuperDimension navigation used to access left lingular lesion. Radial EBUS confirmed concentric view. TBNA, brush, and forceps biopsies performed. ROSE suggested inflammatory process (histiocytes/giant cells). No complications.",
            7: "[Indication]\nMigratory lung nodules.\n[Anesthesia]\nGeneral.\n[Description]\n1. BAL RUL.\n2. Nav bronch to Lingula.\n3. Radial EBUS confirmation.\n4. TBNA, Brush, Forceps of Lingula target.\n[Plan]\nCXR. Pathology pending.",
            8: "We performed a complex bronchoscopy on Ms. Anderson to investigate her lung nodules. First, we washed the right upper lobe to check for infection. Then, using electromagnetic navigation, we guided a catheter to the lesion in the left lingula. We double-checked the position with ultrasound, which confirmed we were right in the lesion. We took samples with a needle, a brush, and forceps. The preliminary look at the slides showed cells consistent with inflammation rather than cancer.",
            9: "Procedure: Guided bronchoscopy (31627), Ultrasound verification (31654), Needle aspiration (31629), Tissue sampling (31628), Bronchial washing (31624).\nTarget: Lingular nodule.\nFindings: Lesion localized via navigation and sonography. Samples obtained via aspiration and forceps. Lavage performed in contralateral lobe."
        },
        4: { # Jennifer Kim (PleurX)
            1: "Procedure: Rt PleurX Catheter Placement.\nIndication: Malignant pleural effusion.\nUS: Free flowing fluid.\nSteps: Local. Tunnel 7.5cm. Seldinger technique. 15.5Fr catheter. 1550mL drained.\nComp: None. CXR confirms placement.",
            2: "OPERATIVE REPORT: Tunneled Pleural Catheter Insertion.\nINDICATION: Recurrent malignant pleural effusion (Adenocarcinoma).\nDESCRIPTION: Under ultrasound guidance, the right pleural space was identified. A subcutaneous tunnel was created. Using the Seldinger technique, a 15.5 Fr PleurX indwelling pleural catheter was inserted. The cuff was positioned within the tunnel. 1,550 mL of clear yellow fluid was drained. Post-procedure imaging confirmed appropriate positioning and lung re-expansion.",
            3: "CPT 32550: Insertion of indwelling tunneled pleural catheter.\nGuidance: Ultrasound used for site selection and wire placement.\nDevice: 15.5 Fr PleurX.\nDrainage: 1550 mL.\nSite: Right hemithorax.",
            4: "Procedure: IPC Placement\nPatient: Jennifer Kim\nAttending: Dr. Reyes\n\n1. US scan: Large Rt effusion.\n2. Prep/Drape/Local.\n3. Tunnel created.\n4. Catheter inserted over wire.\n5. Fluid drained (1.5L).\n6. Teaching done with patient.",
            5: "jennifer kim needed a pleurx for her cancer fluid. right side. dr reyes doing it. we scanned it big effusion. numbed her up made the tunnel put the catheter in. drained about a liter and a half of yellow fluid. she felt way better. taught her how to use the bottles. xray looked good.",
            6: "Ultrasound-guided placement of right indwelling pleural catheter (PleurX) performed for malignant effusion. 15.5 Fr catheter tunneled and inserted without difficulty. 1,550 mL fluid drained. Post-procedure CXR showed good position and re-expansion. Patient educated on home drainage.",
            7: "[Indication]\nRecurrent malignant pleural effusion (Rt).\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nUS guidance. Tunnel created. PleurX catheter inserted. 1550mL drained.\n[Plan]\nDrain Q2 days. Home health setup.",
            8: "Ms. Kim has been suffering from fluid buildup due to her lung cancer. To help manage this at home, we placed a PleurX catheter today. We used ultrasound to find the best spot on her right side. We numbed the area, created a tunnel under the skin, and inserted the drainage tube into the pleural space. We drained over a liter of fluid immediately, which helped her breathing significantly. We taught her and her husband how to use the drainage kits at home.",
            9: "Procedure: Implantation of tunneled pleural drainage system (32550).\nContext: Malignant hydrothorax.\nAction: Sonographic localization. Catheter tunneled and deployed into pleural cavity. Effusion evacuated (1550mL).\nOutcome: Symptomatic relief. Device functional."
        },
        5: { # Christine Davis (EBUS)
            1: "Procedure: EBUS-TBNA.\nIndication: Lymphadenopathy (constitutional sx).\nFindings:\n- 7 (Subcarinal): 45mm, necrotic.\n- 4R: 31mm.\n- 10L/11R sampled.\nROSE: Atypical lymphoid cells (Suspicious for Lymphoma).\nPlan: Heme/Onc consult.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nINDICATION: Evaluation of mediastinal lymphadenopathy in setting of B symptoms.\nFINDINGS: Significant adenopathy identified. Station 7 (subcarinal) was markedly enlarged (45x28mm) and hypoechoic. Station 4R, 10L, and 11R were also sampled. \nCYTOPATHOLOGY: ROSE demonstrated atypical lymphoid proliferation. Samples sent for flow cytometry, cell block, and microbiology.",
            3: "Billing Code: 31653 (EBUS sampling 3+ stations).\nStations Sampled: 7, 4R, 10L, 11R.\nRationale: Diagnostic evaluation of multiple mediastinal and hilar nodes.\nPathology: Samples sent for flow cytometry and culture.",
            4: "Procedure: EBUS\nPt: Christine Davis\nAttending: Dr. Lee\n\n1. Gen Anesthesia.\n2. EBUS scope inserted.\n3. Sampled 7, 4R, 10L, 11R.\n4. ROSE: Atypical lymphoid cells.\n5. No complications.\n6. Plan: Wait for final path.",
            5: "christine davis ebus note. dr lee attending. she has night sweats weight loss. we looked with ebus and station 7 was huge 45mm. 4r was big too. sampled 7 4r 10l and 11r. rose said it looks like lymphoma. sent for flow and cultures just in case. patient stable.",
            6: "EBUS-TBNA performed for mediastinal lymphadenopathy. Stations 7, 4R, 10L, and 11R were visualized and sampled. Station 7 was markedly enlarged (45mm). ROSE cytology showed atypical lymphoid cells concerning for lymphoma. Tissue sent for flow cytometry and cultures. Estimated blood loss <10mL.",
            7: "[Indication]\nMediastinal adenopathy, B-symptoms.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA of stations 7, 4R, 10L, 11R. Large subcarinal node (45mm). ROSE: Atypical lymphoid.\n[Plan]\nHeme/Onc referral. PET-CT.",
            8: "Ms. Davis underwent an EBUS procedure to investigate her enlarged lymph nodes and constitutional symptoms. We found very large nodes, particularly under the carina (station 7). We used a needle to take samples from four different stations in her chest. The preliminary results in the operating room were concerning for lymphoma, so we sent the samples for specialized testing including flow cytometry. She woke up well from the anesthesia.",
            9: "Procedure: EBUS-guided needle aspiration (31653).\nTarget: Mediastinal adenopathy.\nAction: Stations 7, 4R, 10L, 11R accessed. Specimens harvested.\nAnalysis: Preliminary cytology indicates lymphoid malignancy. Samples forwarded for immunophenotyping."
        },
        6: { # James Rodriguez (Thoracentesis)
            1: "Procedure: Therapeutic Thoracentesis.\nIndication: Hepatic hydrothorax (Rt).\nUS: 6.5cm pocket.\nAction: 8Fr catheter inserted. 800mL removed. Stopped early (re-expansion concern).\nComp: None.\nPlan: Diuretics. TIPS eval.",
            2: "PROCEDURE NOTE: Ultrasound-Guided Thoracentesis.\nINDICATION: Recurrent right hepatic hydrothorax in patient with cirrhosis (MELD 18).\nDESCRIPTION: The right hemithorax was scanned, identifying a safe pocket. Under local anesthesia, an 8-French catheter was introduced. 800 mL of clear transudative fluid was removed. Drainage was terminated at 800 mL to prevent re-expansion pulmonary edema and hypotension in this high-risk patient. Post-procedure ultrasound ruled out pneumothorax.",
            3: "CPT 32555: Thoracentesis with imaging guidance.\nGuidance: Ultrasound used to mark site and guide needle.\nVolume: 800 mL.\nComplexity: Patient coagulopathic (Plt 68K, INR 1.7), careful technique required.",
            4: "Procedure: Thoracentesis\nPt: James Rodriguez\nAttending: Dr. Nguyen\n\n1. Pre-proc US: Rt effusion.\n2. Local anesthetic.\n3. Catheter placed.\n4. Drained 800cc yellow fluid.\n5. Stopped to be safe.\n6. Pt breathing better.",
            5: "james rodriguez liver patient with fluid on the lung. dr nguyen supervising. did a tap on the right side. ultrasound looked good. put the catheter in drained about 800cc. didn't want to take too much cause his liver is bad. fluid looked clear. sent for culture. he felt better.",
            6: "Therapeutic thoracentesis performed for right hepatic hydrothorax. Ultrasound guidance used. 800 mL clear transudative fluid removed. Procedure terminated to minimize risk of re-expansion edema/bleeding given coagulopathy. Patient tolerated well. No pneumothorax on post-procedure ultrasound.",
            7: "[Indication]\nRt hepatic hydrothorax, dyspnea.\n[Anesthesia]\nLocal.\n[Description]\nUS guidance. 8Fr catheter. 800mL drained. Clear/yellow.\n[Plan]\nContinue diuretics. Sodium restriction.",
            8: "Mr. Rodriguez needed fluid drained from his right lung due to his liver condition. We performed a thoracentesis using ultrasound to guide us safely. We removed 800 mL of fluid, which looked like typical liver-related fluid. We decided not to take more to avoid complications like bleeding or shock, given his delicate condition. He reported feeling much better afterwards.",
            9: "Procedure: Pleural aspiration (32555).\nContext: Hepatic hydrothorax.\nAction: Sonographically guided puncture. 800mL effusion evacuated.\nOutcome: Respiratory relief. No adverse events."
        },
        7: { # James Patterson (Rigid Bronch/Tumor)
            1: "Procedure: Rigid Bronchoscopy, Tumor Ablation.\nIndication: Tracheal obstruction (tumor).\nFindings: 90% obstruction subglottic.\nAction: Rigid scope. Snare resection of polypoid lesions. APC for base/hemostasis.\nResult: 90% patent airway.\nPlan: Oncology f/u. No stent placed (patient refusal).",
            2: "OPERATIVE REPORT: Rigid bronchoscopy with mechanical and thermal tumor debulking.\nINDICATION: Critical endotracheal obstruction.\nFINDINGS: Multiple polypoid lesions in the subglottic trachea causing 90% expiratory obstruction. \nTECHNIQUE: A 10mm rigid tracheoscope was utilized. The flexible scope was introduced through the rigid barrel. Electrocautery snare was used to resect the dominant polypoid masses. Argon Plasma Coagulation (APC) was applied to the tumor base for destruction and hemostasis. Luminal patency was restored to approximately 90%.",
            3: "CPT 31641: Bronchoscopy with destruction of tumor.\nTechniques: Rigid bronchoscopy, Snare electrocautery, Argon Plasma Coagulation (APC).\nSite: Trachea (Endotracheal tumor).\nComplexity: Debulking of >50 lesions to restore airway.",
            4: "Procedure: Rigid Bronch / Debulking\nPatient: James Patterson\nAttending: Dr. Lee\n\n1. GA / Paralytics.\n2. LMA -> Flex scope check: 90% blocked.\n3. Rigid scope inserted.\n4. Snare used to cut tumors.\n5. APC used to burn the rest.\n6. Airway open now.\n7. Extubated.",
            5: "james patterson rigid bronch. dr lee attending. guy had a huge tumor in his trachea blocking 90 percent. we went in with the rigid scope. used the snare to chop off the big pieces. then apc to burn the rest. got it open pretty good. he didn't want a stent so we didn't put one in. hopefully chemo works.",
            6: "Rigid bronchoscopy performed for symptomatic tracheal tumor. Visualization showed 90% obstruction by polypoid masses. Mechanical debulking performed via snare cautery followed by APC for residual tissue and hemostasis. Airway patency restored to near normal. No stent placed per patient preference. Complications: None.",
            7: "[Indication]\nTracheal tumor, obstruction.\n[Anesthesia]\nGeneral (Rigid).\n[Description]\nRigid bronchoscopy. Snare resection of polyps. APC ablation.\n[Result]\nAirway recanalized (90% open).\n[Plan]\nOncology for chemo/radiation.",
            8: "Mr. Patterson was brought to the OR for management of his tracheal tumor. We found the airway was 90% blocked by growths. We used a rigid bronchoscope to control the airway and then used a snare to cut away the large tumors. We cleaned up the base of the tumors with argon plasma coagulation. By the end, his airway was wide open. He had refused a stent, so we rely on his chemotherapy to prevent regrowth.",
            9: "Procedure: Rigid endoscopy with tumor destruction (31641).\nTarget: Endotracheal neoplasm.\nAction: Mechanical resection (snare) and thermal ablation (APC).\nOutcome: Recanalization of airway."
        },
        8: { # Gerald K Thompson (Robotic Bronch - Ignoring the Martinez artifact)
            1: "Procedure: Robotic Bronchoscopy (Ion).\nTarget: RUL nodule (2.8cm).\nNav: Ion system. Auto registration.\nConfirmation: Radial EBUS (concentric), Cone Beam CT.\nSampling: Brush, Forceps, Needle.\nComp: None.",
            2: "PROCEDURE NOTE: Robotic-assisted bronchoscopy.\nINDICATION: RUL pulmonary nodule (2.8cm), intermediate malignancy risk.\nDETAILS: The Intuitive Ion system was utilized. Registration was excellent. The catheter was navigated to the RUL posterior segment target. Radial EBUS confirmed a concentric lesion. Intraprocedural Cone Beam CT (CBCT) verified tool-in-lesion accuracy. Biopsies were taken using brush, forceps, and needle. Samples sent for pathology.",
            3: "Billing Codes:\n- 31627 (Navigational Bronchoscopy): Ion robotic system used.\n- 31654 (Radial EBUS): Confirmation of lesion position.\n- 31629/31628: Transbronchial needle aspiration and forceps biopsies performed.\nNotes: Cone Beam CT used for verification.",
            4: "Procedure: Robotic Bronch (Ion)\nPt: Gerald Thompson\nAttending: Dr. Patel\n\n1. GA/ETT.\n2. Ion registration.\n3. Nav to RUL.\n4. REBUS check: Concentric.\n5. CBCT spin: Good position.\n6. Biopsy x many.\n7. Extubated.",
            5: "gerald thompson robotic bronch case. dr patel attending. used the ion robot. went to the rul nodule. radial ebus showed it good. did a spin with the c-arm to double check. needle brush forceps everything. samples sent. no pneumo on the scan. done.",
            6: "Robotic-assisted bronchoscopy (Ion) performed for 2.8cm RUL nodule. Navigation to posterior segment successful. Confirmation via Radial EBUS (concentric) and Cone Beam CT. Extensive sampling performed with needle, brush, and forceps. No complications. Estimated blood loss <5mL.",
            7: "[Indication]\n2.8cm RUL nodule.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nIon Robotic Navigation. Radial EBUS confirmation. Cone Beam CT verification. TBNA/Forceps/Brush biopsies.\n[Plan]\nPathology results pending.",
            8: "Mr. Thompson underwent a robotic bronchoscopy today for his lung nodule. We used the Ion robot to navigate deep into his right upper lung. We confirmed we were at the right spot using both a mini-ultrasound probe and a 3D CT scan right in the operating room. We took multiple samples using needles and forceps. The procedure went smoothly with no issues.",
            9: "Procedure: Robotic-guided endoscopy (31627), Sonographic confirmation (31654), Tissue sampling (31628/31629).\nTarget: RUL mass.\nAction: Robotic navigation. Multi-modal sampling.\nVerification: Cone Beam CT."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data to simulate the 'original' names/ages from Part 1/2 for consistency.
    Indices match the source file records.
    """
    return [
        {"idx": 0, "orig_name": "Robert Johnson", "orig_age": 67, "names": ["Frank Miller", "Henry Wilson", "George Davis", "Edward Moore", "Charles Taylor", "Thomas Anderson", "Walter White", "Arthur King", "Louis Scott"]},
        {"idx": 1, "orig_name": "Andrew T Lewis", "orig_age": 65, "names": ["James Brown", "Robert Jones", "Michael Garcia", "William Martinez", "David Robinson", "Richard Clark", "Joseph Rodriguez", "Thomas Lewis", "Charles Lee"]},
        {"idx": 2, "orig_name": "Andrew T Lewis", "orig_age": 65, "names": ["John Doe", "Jane Smith", "Bob Johnson", "Alice Williams", "Charlie Brown", "David Jones", "Eve Davis", "Frank Miller", "Grace Wilson"]}, # Duplicate source, new names
        {"idx": 3, "orig_name": "Rachel Anderson", "orig_age": 65, "names": ["Mary Johnson", "Patricia Williams", "Jennifer Brown", "Linda Jones", "Elizabeth Garcia", "Barbara Miller", "Susan Davis", "Jessica Rodriguez", "Sarah Wilson"]},
        {"idx": 4, "orig_name": "Jennifer Kim", "orig_age": 48, "names": ["Karen Moore", "Nancy Taylor", "Lisa Anderson", "Betty Thomas", "Margaret Jackson", "Sandra White", "Ashley Harris", "Kimberly Martin", "Emily Thompson"]},
        {"idx": 5, "orig_name": "Christine Davis", "orig_age": 58, "names": ["Donna Garcia", "Carol Martinez", "Ruth Robinson", "Sharon Clark", "Michelle Rodriguez", "Laura Lewis", "Sarah Lee", "Kimberly Walker", "Deborah Hall"]},
        {"idx": 6, "orig_name": "James Rodriguez", "orig_age": 54, "names": ["Brian Allen", "Kevin Young", "Ronald Hernandez", "Timothy King", "Jason Wright", "Jeffrey Lopez", "Ryan Hill", "Gary Scott", "Jacob Green"]},
        {"idx": 7, "orig_name": "James Patterson", "orig_age": 65, "names": ["Eric Adams", "Stephen Baker", "Andrew Gonzalez", "Justin Nelson", "Scott Carter", "Brandon Mitchell", "Benjamin Perez", "Samuel Roberts", "Gregory Turner"]},
        {"idx": 8, "orig_name": "Gerald K Thompson", "orig_age": 62, "names": ["Frank Phillips", "Raymond Campbell", "Patrick Parker", "Jack Evans", "Dennis Edwards", "Jerry Collins", "Tyler Stewart", "Aaron Sanchez", "Jose Morris"]}
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
            # Fallback if source has more notes than mocks
            print(f"Warning: No mock data for index {idx}, skipping.")
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
            
            # Update note_text with the variation from our hardcoded dict
            # If we don't have a variation for this index/style, keep original (safety check)
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    # Clean existing MRN if it has _syn already (just in case)
                    base_mrn = str(note_entry["registry_entry"]["patient_mrn"]).split('_syn')[0]
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
    output_filename = output_dir / "synthetic_blvr_notes_part_003.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()