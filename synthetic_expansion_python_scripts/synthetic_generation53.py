import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_053.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # poor_01: E Okafor (Complex Airway + PleurX)
            1: "Indication: Dyspnea, RMS tumor, effusion.\nAnesthesia: General, 8.0 ETT.\nProcedure:\n- RMS obstruction (near complete) identified.\n- Debulking performed via rigid/flex scope (APC, mechanical).\n- Old stent removed/adjusted. New SEMS deployed RMS.\n- US-guided PleurX catheter placed right chest.\n- 1200cc straw fluid drained.\nComplications: Mild ooze, small apical PTX (stable).",
            2: "HISTORY: Ms. Okafor presented with severe dyspnea secondary to malignant central airway obstruction and recurrent pleural effusion.\nOPERATIVE SUMMARY: Under general anesthesia with rigid and flexible bronchoscopy, a near-total obstruction of the right mainstem bronchus was visualized. Multimodal recanalization was achieved utilizing argon plasma coagulation and mechanical debulking, restoring 90% patency. A malpositioned metallic stent was revised, and a new self-expanding metallic stent was deployed. Subsequently, ultrasound-guided placement of a tunneled indwelling pleural catheter was performed on the right, yielding 1200mL of exudative fluid. The patient remained stable.",
            3: "Procedures Performed:\n1. 31641: Bronchoscopy with destruction of tumor (APC/mechanical) in Right Mainstem.\n2. 31636: Bronchoscopy with stent placement (SEMS) in Right Mainstem.\n3. 31645: Therapeutic aspiration of extensive clots/mucus.\n4. 32550: Insertion of tunneled pleural catheter (PleurX) under ultrasound guidance.\nMedical Necessity: Malignant central airway obstruction and recurrent malignant pleural effusion.",
            4: "Procedure: Rigid Bronchoscopy, Tumor Debulk, Stent, IPC.\nAttending: Dr. X\nSteps:\n1. GA induced, 8.0 ETT.\n2. Rigid scope inserted. RMS mass seen.\n3. Debulked with APC and forceps.\n4. Replaced bent stent with new SEMS.\n5. Suctioned clots.\n6. PleurX catheter placed right side using Ultrasound.\n7. 1200cc fluid out.\nPlan: Monitor small PTX, stepdown unit.",
            5: "patient E Okafor here for airway and pleural stuff shes got the bad tumor right side. general anesthesia tube down. lots of junk in the airway cleared it out with apc and scraper tool. old stent looked bad so put a new metal one in. suctioned a ton of mucous. then flipped her for the chest tube used ultrasound put in a pleurx drained 1200 cc straw fluid. cxr showed tiny pneumo but shes fine sending to stepdown.",
            6: "E Okafor 65F came in with bad SOB big R main branch tumor and fluid on R chest. Plan was airway clean out and pleur cath. General anesthesia by gas team 8.0 ETT in I did flex rigid bronch. Lots of junk and endobronch mass almost full block in RMS. Used scope and tools scraped and APC probably 80 90 percent open after. Old metal stent looked bent in pulled adjusted new SEMS put in same area post view ok. Tons of thick clots mucus suctioned no real big bleed just ooz cold saline once. Then turned pt a bit US on R side big effusn. Cut down 5th space mid ax tunneled cath pleurx type in sutured hooked to vac. Straw colored fluid out about 1200. No obvious air leak. Post small apical pneumo R on CXR stable no chest tube. Pt to stepdown.",
            7: "[Indication]\nSymptomatic R mainstem malignant obstruction and recurrent R pleural effusion.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nRigid/Flex bronchoscopy. RMS tumor debulked via APC/mechanical. Old stent revised; new SEMS placed. 31645 aspiration of clots performed. Right PleurX catheter inserted under US guidance; 1200cc drained.\n[Plan]\nStepdown unit. Monitor small apical pneumothorax.",
            8: "The patient presented with severe shortness of breath due to a right mainstem tumor and effusion. We proceeded with general anesthesia and intubation. Upon inspection, the right mainstem was nearly blocked. We used APC and mechanical tools to debulk the tumor, achieving good patency. The existing stent was compromised, so we placed a new self-expanding metal stent. After clearing significant secretions, we used ultrasound to guide the insertion of a PleurX catheter in the right chest, draining 1200cc of fluid. A small pneumothorax was noted post-op but required no intervention.",
            9: "Procedure: Bronchoscopic canalization and tunneled catheter insertion.\nAction: The right mainstem obstruction was ablated and cored out. The compromised prosthesis was extracted and a fresh SEMS was deployed. Significant secretions were evacuated. A tunneled pleural drain was implanted under sonographic visualization, evacuating 1200cc of effusion.\nResult: Airway patency restored. Mild pneumothorax observed."
        },
        1: { # poor_02: 82F (BAL only)
            1: "Indication: Nonresolving pneumonia LLL.\nAnesthesia: Moderate sedation (Fent/Versed).\nAction:\n- Scope via mouth.\n- Thick secretions LLL.\n- BAL LLL (100cc in, 80cc return).\n- Samples: Cx, AFB, Fung, Viral.\nFindings: No masses. Mucosa inflamed.\nPlan: Floor.",
            2: "INDICATION: Evaluation of persistent left lower lobe pulmonary infiltrates in an 82-year-old female.\nPROCEDURE: The patient was placed under moderate sedation. The bronchoscope was introduced trans-orally. The airway inspection revealed thick purulent secretions emanating from the LLL, but no endobronchial masses. A bronchoalveolar lavage (BAL) was performed in the target segment utilizing 100mL of saline with adequate return. Specimens were submitted for comprehensive microbiology.\nIMPRESSION: Purulent bronchitis, LLL. No malignancy visualized.",
            3: "Code: 31624 (Bronchoscopy with BAL).\nTarget: Left Lower Lobe.\nTechnique: Instillation of saline aliquots and aspiration of effluent.\nFindings: Purulent secretions, no mass.\nMedical Necessity: Non-resolving pneumonia (J18.9).\nNote: No biopsies performed.",
            4: "Procedure: Diagnostic Bronch with BAL\nPatient: 82F\nSteps:\n1. Time out. Mod sed started.\n2. Scope passed. Vocal cords normal.\n3. LLL segments inspected - lots of yellow secretions.\n4. BAL performed LLL.\n5. Tol: Good. Mild desat corrected with O2.\nPlan: Await cultures.",
            5: "Quick note for the pneumonia lady in 302. Did the bronch with moderate sedation. Went down to the LLL and it was full of yellow goo. Washed it out with saline sent the fluid for culture and virus checks. Didn't see any cancer or masses. She coughed a bit and sats dropped but came right back up. Back to the floor no issues.",
            6: "Bronch note quick and sloppy pt old lady 82 yo came in w pna not geting better. No intub on NC O2 whole time. Consnt in chart. Mod sed only fent and versed by RN I was in room about 25min not timing perfect. Scope thru mouth cords ok trachea ok no masses seen. Lot of thick yellow junk esp LLL. Did BAL left lower squirt about 100cc NS got back maybe 70 80cc cloudy goo. Sent stuff for cx AFB fung viral etc. No bx no stent no ebus nothing fancy. Pt coughed some sats drop low 90s bumped O2 fine after. CXR after no pnx lungs look same more or less. Done back to floor.",
            7: "[Indication]\nNonresolving pneumonia LLL.\n[Anesthesia]\nModerate sedation.\n[Description]\nInspection revealed thick secretions LLL. No masses. BAL performed LLL with 100cc saline. Return 70-80cc cloudy fluid sent for analysis.\n[Plan]\nReturn to floor. Await cx.",
            8: "We performed a diagnostic bronchoscopy on this 82-year-old female due to her lingering pneumonia. Using moderate sedation, we advanced the scope and found heavy secretions in the left lower lobe. We washed the area with saline and collected the fluid for testing. There were no signs of tumors or other blockages. She tolerated the procedure well aside from some minor coughing and transient oxygen desaturation.",
            9: "Procedure: Diagnostic flexible bronchoscopy with bronchoalveolar lavage.\nFindings: The LLL contained viscous exudate. No neoplasms were detected.\nAction: The segment was irrigated with saline and the effluent was retrieved for microbiological analysis.\nOutcome: Patient stable, oxygen saturation maintained."
        },
        2: { # poor_03: 58F (EBUS 3 stations)
            1: "Indication: Mediastinal adenopathy, r/o Ca.\nProcedure: EBUS-TBNA.\nTargets: 4R, 7, 11L.\nPasses: 3x each station.\nResults: ROSE + for malignancy at 4R.\nComplications: Minor bleed, controlled.\nPlan: PACU, Oncology referral.",
            2: "INDICATION: Staging of mediastinal lymphadenopathy in a 58-year-old female with suspected bronchogenic carcinoma.\nPROCEDURE: Under moderate sedation, the EBUS scope was introduced. Systematic ultrasonic evaluation of the mediastinum was performed. Transbronchial needle aspiration (TBNA) was conducted at stations 4R, 7, and 11L. Rapid On-Site Evaluation (ROSE) confirmed the presence of malignant cells at station 4R. No vascular complications occurred.\nIMPRESSION: Metastatic lymphadenopathy (N2 disease).",
            3: "CPT: 31653 (Bronchoscopy with EBUS-TBNA, 3 or more stations).\nStations Sampled: 4R, 7, 11L.\nTechnique: Ultrasound localization, Doppler avoidance of vessels, needle aspiration.\nPathology: ROSE positive at 4R.\nSetting: Bronchoscopy suite, moderate sedation.",
            4: "Procedure: EBUS Staging\nPatient: 58F\nSteps:\n1. Mod sed. Scope in.\n2. Airway exam normal.\n3. EBUS scope to 4R, 7, 11L.\n4. TBNA x3 passes each.\n5. Path in room said 4R is cancer.\n6. No major bleeding.\nPlan: Follow up with Onc.",
            5: "Staging bronch for the 58 year old lady. Used the ultrasound scope. Poked nodes at 4R 7 and 11L. Got good samples. The cyto guy in the room said 4R is definitely cancer. 11L and 7 looked like just lymph tissue. Procedure went fine little bit of blood stopped with ice. She went to recovery stable.",
            6: "EBUS bronc quick sumry 58yo F med nodes on CT question lung ca. Came NPO IV in consnt already done in clinic. No GA just twilight type sed fent versed pushes by anesthesia nurse pt breathing on own nasal O2 3L airway native no tube. Scope in via mouth brief look no obvious endobronch lesion. Swapped to EBUS scope. Sampled 4R big round node around 2cm x3 passes station 7 x3 11L x2. Used doplar to check no big vessel hit. On site ROSE said lymphs plus malignant cells at 4R. No nav robot no radial probe no transbronchial lung bx no BAL. Tiny bleed but stop with ice saline and suction. Pt went to PACU stable sats mid 90s plan follow up path and oncology.",
            7: "[Indication]\nSuspected lung cancer, mediastinal lymphadenopathy.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS scope introduced. Stations 4R, 7, and 11L identified and sampled (TBNA). ROSE confirmed malignancy at 4R.\n[Plan]\nPACU recovery. Oncology consult.",
            8: "This 58-year-old female underwent EBUS bronchoscopy for staging of suspected lung cancer. Using moderate sedation, we examined the airway and then used the EBUS scope to sample lymph nodes at stations 4R, 7, and 11L. We took multiple passes at each site. The on-site pathologist confirmed cancer cells in the 4R node. The patient had minor bleeding which stopped easily.",
            9: "Procedure: Endobronchial ultrasound-guided transbronchial needle aspiration.\nAction: The mediastinum was scanned. Nodes at 4R, 7, and 11L were punctured and aspirated. Doppler verified vascular safety.\nResult: Cytopathology identified malignant cells at station 4R. Hemostasis was achieved with cold saline."
        },
        3: { # poor_04: 61F (L Main debulk)
            1: "Indication: Symptomatic LM obstruction.\nAnesthesia: GA, 8.5 ETT.\nTechnique: Rigid & Flex bronch.\nAction: Mechanical debulking (forceps), APC, Cryo extraction of LM tumor.\nResult: 80% patency achieved.\nPlan: ICU obs.",
            2: "INDICATION: Severe dyspnea secondary to malignant obstruction of the left mainstem bronchus.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy was initiated. A large, friable exophytic tumor was visualized occluding the left mainstem. Therapeutic debulking was performed utilizing a combination of argon plasma coagulation for hemostasis/ablation and cryotherapy for tissue extraction. Luminal patency was improved to approximately 80%. No stent was required.\nIMPRESSION: Successful recanalization of left mainstem bronchus.",
            3: "Code: 31641 (Bronchoscopy with destruction of tumor).\nLocation: Left Mainstem Bronchus.\nMethod: APC ablation, Cryo-debridement, Forceps removal.\nOutcome: Relief of stenosis from near-total to ~20% residual.\nNote: No stent placed (excludes 31636).",
            4: "Procedure: Therapeutic Bronchoscopy\nPatient: Rosa M, 61F\nSteps:\n1. GA, ETT 8.5.\n2. Rigid scope placed.\n3. Saw tumor blocking Left Main.\n4. Used APC to burn and forceps to pull it out.\n5. Cryo probe used to grab chunks.\n6. Airway opened up nicely.\nPlan: ICU for monitoring.",
            5: "Operative note for Rosa she has that nasty tumor in the left main lung. Put her to sleep with a big tube. Used the rigid scope and the flexible one. Burned the tumor with APC and pulled big chunks out with the cryo probe and forceps. Got it mostly open. Didnt put a stent in this time. She bled a bit but the epi stopped it. Going to ICU.",
            6: "Short op note tumor debulk pt Rosa M hx lung ca w nasty endobronchial chunk L main very SOB walking even to bathroom. In OR gen anes 8.5 ETT. I did flex then rigid scope. Big friable tumer almost closing LM lumen. Used APC and forceps and some cryo pull to open lumen maybe 80 percent. Some blood but not huge cold saline and epi helped. No stent placed no biopsy already dx from prior no nav no ebus no BAL. Post bronch CXR ok no ptx seen. Pt to ICU for obs overnight because COPD and O2 needs.",
            7: "[Indication]\nSymptomatic malignant L mainstem obstruction.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nRigid/Flex bronchoscopy. Tumor destruction via APC, forceps, and cryo-extraction. Lumen restored to 80% patency. Hemostasis achieved.\n[Plan]\nICU observation.",
            8: "Rosa underwent a therapeutic bronchoscopy to treat a tumor blocking her left main airway. Under general anesthesia, we used a rigid scope to access the obstruction. We used APC to cauterize the tissue and forceps along with a cryoprobe to physically remove the tumor mass. We managed to open the airway to about 80% of its normal size. There was some bleeding, but it was controlled with epinephrine and saline.",
            9: "Procedure: Bronchoscopic tumor destruction and stenosis relief.\nTechnique: Ablation via argon plasma coagulation and cryoadhesion extraction.\nTarget: Left mainstem bronchus.\nOutcome: The obstruction was obliterated, restoring luminal caliber. Hemostasis was secured with vasoconstrictors."
        },
        4: { # poor_05: 75M (EBUS + Nav RUL)
            1: "Indication: RUL nodule, med nodes.\nProcedure: EBUS + Nav Bronch.\nEBUS: Stations 4R, 7 (2 stations). ROSE 4R suspicious.\nNav: Monarch system to RUL target. Radial EBUS confirmation.\nBiopsy: TBBx x5.\nPlan: Extubate, PACU.",
            2: "INDICATION: Evaluation of RUL nodule and PET-avid mediastinal adenopathy.\nPROCEDURE: General anesthesia was induced. Linear EBUS staging was performed at stations 4R and 7; ROSE suggested malignancy at 4R. Subsequently, electromagnetic navigation (Monarch platform) was utilized to navigate to the peripheral RUL lesion. Radial EBUS confirmed concentric probe position. Transbronchial biopsies were obtained through the guide sheath.\nIMPRESSION: Diagnosis of lung cancer likely given nodal findings.",
            3: "Codes:\n- 31652: EBUS (4R, 7).\n- 31627: Computer-assisted navigation (Add-on).\n- 31654: Peripheral EBUS (Add-on).\n- 31628: Transbronchial biopsy, single lobe (RUL).\nJustification: Staging followed by targeted peripheral biopsy of 1.8cm lesion.",
            4: "Procedure: Robot Bronch + EBUS\nPatient: 75M\nSteps:\n1. GA, 8.0 ETT.\n2. EBUS first: sampled 4R and 7.\n3. Switched to Nav scope.\n4. Navigated to RUL nodule.\n5. Radial EBUS showed lesion.\n6. Biopsied x5.\nPlan: PACU.",
            5: "Long case today. 75 year old guy with the RUL spot. Did the EBUS first hit 4R and 7. 4R looks bad. Then used the robot system to drive out to the nodule. Found it with the radial probe and took 5 bites with the forceps. Everything went smooth no pneumothorax.",
            6: "Robot bronch case kinda long writing quick and messy pt mid 70s M w spiculated RUL nodule 1.8cm and PET hot mediast nodes. Under GA 8.0 ETT by gas. Quick white light look nothing in trachea or mainstem. Then linear EBUS first and sampled 4R and 7 about 3 passes each. Doplar ok ROSE at 4R suspicious or malig 7 just lymphs. After that switched to nav platform Monarch style computer navgation from CT used to drive out to periph RUL target. Radial EBUS probe in guide sheath showed concentric lesion left sheath parked at spot. Thru sheath did multiple TBBx around 5 pieces from lesion with forceps. No cryo no needle ablation no stents. Mild bleeding but cleared with suction and cold saline hemodyn stable. No complications pt extubated in OR and went to PACU ok.",
            7: "[Indication]\nRUL nodule, mediastinal adenopathy.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nEBUS-TBNA performed at 4R and 7. Navigational bronchoscopy used to access RUL lesion. Radial EBUS confirmation. TBBx x5 performed.\n[Plan]\nPACU. Extubated.",
            8: "We performed a combined staging and diagnostic procedure on this 75-year-old male. First, we used EBUS to sample lymph nodes at 4R and 7; the 4R node appeared suspicious. We then switched to the navigational system to locate the nodule in the right upper lobe. Using radial EBUS, we confirmed the location and took five biopsy samples. The patient tolerated the procedure well and was extubated in the OR.",
            9: "Procedure: Endobronchial ultrasound staging and navigational biopsy.\nAction: Stations 4R and 7 were sampled via linear EBUS. Computer-guided navigation was employed to reach the RUL target. The lesion was visualized sonographically (radial probe). Forceps biopsies were acquired.\nResult: Samples obtained. Hemostasis maintained."
        },
        5: { # poor_06: 69M (Nav RLL + Fiducials)
            1: "Indication: RLL nodule, SBRT planning.\nProcedure: Nav Bronch + Fiducials.\nTechnique: EM Nav to RLL basilar. Radial EBUS eccentric view.\nAction: TBBx x4. 2 Gold fiducials placed.\nComplications: Minor bleed.\nPlan: PACU.",
            2: "INDICATION: Tissue diagnosis and fiducial marker placement for RLL neoplasm in a 69-year-old male.\nPROCEDURE: Under moderate sedation, electromagnetic navigation was utilized to localize the RLL basilar segment lesion. Radial EBUS demonstrated an eccentric signal. Transbronchial forceps biopsies were performed. Subsequently, two gold fiducial markers were deployed under fluoroscopic guidance to facilitate stereotactic body radiation therapy (SBRT).\nIMPRESSION: Successful biopsy and marking of RLL lesion.",
            3: "Codes:\n- 31626: Placement of fiducial markers (Primary).\n- 31628: Transbronchial biopsy (RLL).\n- 31627: Navigation add-on.\n- 31654: Radial EBUS add-on.\nNote: Multiple interventions in same lobe. 31626 is highest RVU.",
            4: "Procedure: Nav Bronch, Bx, Fiducials\nPatient: Marcus T, 69M\nSteps:\n1. Mod sed. Native airway.\n2. Navigated to RLL.\n3. Radial EBUS check.\n4. Biopsy x4.\n5. Dropped 2 gold markers for SBRT.\n6. Checked fluoro - markers in place.\nPlan: CXR to rule out pneumo.",
            5: "Marcus needs radiation for his RLL spot so we went in to get a biopsy and drop markers. Used the superD nav system. Found the spot with the radial probe but it was eccentric. Took some biopsies then dropped two gold seeds. Bleeding was minimal. Xray looks good no collapsed lung.",
            6: "Bronch note nav case w fid markr sorry spelling pt Marcus T 69 y o M w RLL spiculr nodule about 2.4cm plan SBRT but need path and fiducials. No GA just mod sed fent and versed by RN under my sup nasal canula O2 airway native no tube. Used EM nav system superD type w pre loaded CT drove scope to RLL basilar seg. Radial e bus probe showed eccent view of lesion in airway left guide sheath parked there. Thru sheath did several TBBx 4 bites w forceps. Then loaded fiducial needle and dropped 2 gold markrs just distal to lesion under fluoro looked ok not in pleura. Small oozing bleed cleared with suction and iced saline. No linear EBUS no BAL no stent no ablation. Pt woke up chatty sats fine CXR after showed no pneumo.",
            7: "[Indication]\nRLL nodule, need path and fiducials.\n[Anesthesia]\nModerate sedation.\n[Description]\nEM Navigation to RLL. Radial EBUS confirmation (eccentric). TBBx x4 performed. 2 gold fiducial markers placed under fluoro guidance.\n[Plan]\nPACU. CXR.",
            8: "Mr. T, a 69-year-old male, underwent a navigational bronchoscopy for his right lower lobe nodule. We used the navigation system to reach the basilar segment and confirmed the lesion with radial EBUS. We took four biopsy samples and then placed two gold fiducial markers to help with his upcoming radiation therapy. He had a small amount of bleeding which we cleared, and the post-procedure X-ray was clear.",
            9: "Procedure: Electromagnetic navigational bronchoscopy with fiducial deployment.\nAction: The RLL target was accessed via computer guidance. Radial sonography confirmed proximity. Forceps biopsies were harvested. Two metallic markers were implanted for radiotherapy guidance.\nResult: Markers visualized on fluoroscopy. No pneumothorax."
        },
        6: { # poor_07: 62M (Ion LLL TBBx only)
            1: "Indication: LLL peripheral nodule.\nProcedure: Robotic Nav Bronch (Ion).\nAnesthesia: Deep sedation, ETT.\nAction: Navigated to LLL. TBBx x6.\nNote: No radial EBUS used. No BAL.\nResult: Stable.\nPlan: PACU.",
            2: "INDICATION: Diagnostic evaluation of a 1.3cm left lower lobe pulmonary nodule.\nPROCEDURE: The patient was placed under deep sedation and intubated. The Ion robotic bronchoscopy platform was utilized for navigation. Upon reaching the target in the LLL based on virtual geometric alignment, six transbronchial biopsy samples were obtained. No radial ultrasound was employed. There were no immediate complications.\nIMPRESSION: Successful robotic-assisted biopsy of LLL lesion.",
            3: "Code: 31628 (Transbronchial biopsy).\nAdd-on: 31627 (Computer-assisted navigation).\nNote: No 31654 billed (radial EBUS not used). No 31629 (single lobe only).\nTechnique: Robotic platform (Ion) used for guidance.",
            4: "Procedure: Robotic Bronchoscopy\nPatient: 62M\nSteps:\n1. Deep sed, ETT.\n2. Ion robot set up.\n3. Navigated to LLL nodule.\n4. Took 6 biopsies.\n5. No bleeding.\nPlan: PACU.",
            5: "Did the robot case on the 62 year old guy. LLL spot hard to reach. Anesthesia put him deep with a tube. Used the Ion system drove right to it. Didn't use the radar probe just trusted the screen. Took 6 bites. No bleeding. He's waking up now.",
            6: "Robot nav bronch simple half baked note pt 62M w periph LLL lesion around 1.3cm hard spot to reach on regular bronch. Anesthesia did deep sed pt basically out intubated with small ETT for airway control chart says deep not full GA. Vent running low settings. Ion robot used CT path loaded scope advanced to LLL target per navgation. No linear EBUS no radial probe used system relies on imaging. At target we did 6 transbronchial biopsys with forceps through working channel. No BAL no needle no cryo no stent. Very minor bleeding suction only no obvious pneumo on fluoro. Pt to PACU stable on 2L NC by time of sign out.",
            7: "[Indication]\nPeripheral LLL nodule.\n[Anesthesia]\nDeep sedation, ETT.\n[Description]\nRobotic navigation (Ion) to LLL target. 6 transbronchial biopsies obtained. No radial EBUS used.\n[Plan]\nPACU. Discharge.",
            8: "This 62-year-old male underwent a robotic bronchoscopy for a difficult-to-reach nodule in the left lower lobe. Under deep sedation, we used the Ion robot to navigate to the site. We relied on the system's imaging rather than radial EBUS. We successfully took six biopsy samples with the forceps. There was no significant bleeding or pneumothorax.",
            9: "Procedure: Robotic-assisted navigational bronchoscopy.\nAction: The scope was guided to the LLL periphery via the robotic platform. Transbronchial forceps biopsies were executed at the target coordinates. Radial sonography was not utilized.\nResult: Specimens obtained. Hemodynamics stable."
        },
        7: { # poor_08: 67M (Trach EBUS 4 stations)
            1: "Indication: Mediastinal nodes, Chronic Trach.\nProcedure: EBUS-TBNA via Trach.\nAccess: Through existing cuff trach.\nStations: 4R, 4L, 7, 11R.\nPasses: 2-3 per station.\nROSE: 4R positive for Ca.\nPlan: ICU.",
            2: "INDICATION: Nodal staging in a 67-year-old male with COPD and chronic tracheostomy.\nPROCEDURE: General anesthesia was maintained via the tracheostomy. The EBUS bronchoscope was introduced directly through the stoma. Systematic staging was performed with TBNA at stations 4R, 4L, 7, and 11R. Cytopathology (ROSE) indicated malignancy at station 4R.\nIMPRESSION: Lung cancer staging via tracheostomy access.",
            3: "Code: 31653 (EBUS-TBNA, 3+ stations).\nStations: 4R, 4L, 7, 11R (4 distinct stations).\nAccess: Existing tracheostomy (no complex airway code billed for access).\nFindings: Malignancy confirmed.",
            4: "Procedure: EBUS through Trach\nPatient: Juan R, 67M\nSteps:\n1. GA via trach.\n2. Scope through trach.\n3. Sampled 4R, 4L, 7, 11R.\n4. ROSE said cancer at 4R.\n5. No issues.\nPlan: Back to ICU.",
            5: "Juan has a trach and needs his nodes checked. Went in through the trach with the EBUS scope. Poked 4R 4L 7 and 11R. Got good samples. 4R is cancer. He's back on the vent in the ICU.",
            6: "EBUS thru trach rough dictation pt Juan C R long term trach for COPD now big mediast nodes on CT need staging for suspected lung cancer. In OR gen anes via existing cuffed trach. I put EBUS scope right thru trach quick look in trachea and main bronchi no endobronch mass. Using linear EBUS sampled 4R 4L 7 and 11R nodes multiple passes two to three each. Doplar check ok each time. ROSE from 4R said cancer others mostly lympy cells. No radial probe no robot nav no periph lung bx no BAL nothing pleural. Pt back to ICU on vent same settings as pre op stable.",
            7: "[Indication]\nMediastinal adenopathy, suspected Ca, patient has Trach.\n[Anesthesia]\nGeneral via Trach.\n[Description]\nEBUS scope passed via tracheostomy. TBNA performed at 4R, 4L, 7, 11R. ROSE positive 4R.\n[Plan]\nICU.",
            8: "Mr. R, who has a chronic tracheostomy, required staging for suspected lung cancer. We performed the EBUS procedure through his trach under general anesthesia. We sampled lymph nodes at stations 4R, 4L, 7, and 11R. The preliminary results from the 4R node showed cancer cells. He was returned to the ICU on his previous ventilator settings.",
            9: "Procedure: Trans-tracheostomy endobronchial ultrasound.\nAction: The mediastinum was accessed via the tracheostoma. Needle aspiration was performed at four nodal stations (4R, 4L, 7, 11R). Immediate cytologic evaluation suggested carcinoma.\nResult: Staging complete. Patient returned to mechanical ventilation."
        },
        8: { # poor_09: 54F (Trach EBUS 2 stations)
            1: "Indication: Hilar adenopathy, Sarcoid vs other.\nProcedure: EBUS-TBNA via Trach.\nStations: 11L, 7 (2 stations).\nFindings: No ROSE. Path pending.\nPlan: Floor.",
            2: "INDICATION: Evaluation of mediastinal and hilar lymphadenopathy in a patient with chronic tracheostomy; rule out sarcoidosis.\nPROCEDURE: General anesthesia was utilized. Access was achieved via the tracheostomy stoma. Linear EBUS guided TBNA was performed at stations 7 (subcarinal) and 11L (left interlobar). Three passes were obtained at each site. Specimens were submitted for permanent section.\nIMPRESSION: Lymphadenopathy, etiology pending pathology.",
            3: "Code: 31652 (EBUS-TBNA, 1-2 stations).\nStations: 7, 11L.\nNote: Procedure performed via tracheostomy. No ROSE available. No other interventions.",
            4: "Procedure: EBUS for Sarcoid?\nPatient: Michelle B, 54F\nSteps:\n1. GA through trach.\n2. Looked with regular scope first - ok.\n3. Switched to EBUS.\n4. Sampled 11L and 7.\n5. Sent to path.\nPlan: Floor.",
            5: "Michelle has a trach and swollen nodes maybe sarcoid. Went in through the trach. Sampled the 11L and 7 nodes with the EBUS needle. Didn't have the rapid read guy so we just sent it all to the lab. She woke up slow but fine.",
            6: "EBUS for sarc vs other note messy pt Michelle B 54F chronic trach. CT shows bulky 2L and 4R nodes no clear lung mass. Case in bronch suite GA via trach again. Standard bronch scope first airway pretty clean some granln tissue at stoma but left alone. Switched to linear EBUS scanned mediastinum and took TBNA from 11L and 7 only three passes each. No ROSE avail slides sent to path. No nav robot no radial EBUS no lung TBBx no BAL no thoracentesis. Pt woke up slow but ok went back to floor on baseline O2.",
            7: "[Indication]\nBulky nodes, r/o sarcoid.\n[Anesthesia]\nGeneral via Trach.\n[Description]\nEBUS-TBNA of stations 11L and 7. 3 passes each. No ROSE.\n[Plan]\nFloor. Follow pathology.",
            8: "Ms. B underwent an EBUS procedure to investigate her swollen lymph nodes, possibly due to sarcoidosis. Since she has a trach, we used that for access under general anesthesia. We sampled the nodes at stations 11L and 7. We didn't have immediate results available, so we sent everything to the lab and sent her back to the floor.",
            9: "Procedure: Trans-tracheal EBUS-TBNA.\nIndication: Granulomatous disease suspicion.\nAction: Tracheostomy access utilized. Needle aspiration performed at subcarinal (7) and left hilar (11L) stations.\nResult: Specimens procured for histologic examination."
        },
        9: { # poor_10: 60M (Thoracentesis)
            1: "Indication: Large L pleural effusion, dyspnea.\nProcedure: US-guided Thoracentesis.\nSite: L posterior, 8th interspace.\nFluid: 1500cc amber/straw.\nComplications: None. No PTX on post-US.\nPlan: Labs sent.",
            2: "INDICATION: Relief of symptomatic malignant left pleural effusion.\nPROCEDURE: The patient was positioned sitting. Thoracic ultrasound identified a large fluid pocket in the left posterior hemithorax. Under local anesthesia and sterile technique, a catheter was inserted at the 8th intercostal space. 1500mL of serous fluid was evacuated. The catheter was withdrawn without complication.\nIMPRESSION: Successful therapeutic thoracentesis.",
            3: "Code: 32555 (Thoracentesis with imaging guidance).\nGuidance: Ultrasound used to mark site and verify absence of pneumothorax post-procedure.\nVolume: 1500cc drained.\nType: Therapeutic and Diagnostic (samples sent).",
            4: "Procedure: Bedside Thoracentesis\nPatient: 60M\nSteps:\n1. Consent. Local anesthesia.\n2. US check - fluid confirmed Left.\n3. Needle in 8th space.\n4. Drained 1.5L.\n5. Pt coughed a bit at end.\n6. Bandage applied.\nPlan: Check labs.",
            5: "Did a tap on the guy in room 4. He was really short of breath. Used the ultrasound to find the spot on the left back. Stuck him and got 1500 cc of yellow fluid. He started coughing so I stopped. No air in the chest after. Sent the fluid for tests.",
            6: "Thoracentasis bedside note scribbled 60 yo guy L lung mass w big L effusn very dyspnic just talking. Did consent verbal and paper. Pt on NC 2L. No GA just local lido plus tiny amnt fentanyl not full sed kinda light mod sed. Sat on edge of bed leaning fwd. US chest big free fluid left posterior. Picked spot mid scap line 8th space. Cleaned skin w chlorhex numbed skin and pleura pt says stingy. Cath needle in nice straw or amber fluid. Hooked to bottle drained about 1500 cc no blood no pus. Stopped when pt cough more and pressure drop on manom not recorded great. Post US showed only small resid effusn no pnx. Band aid on. Spec sent for labs including cell ct protien LDH and cyto.",
            7: "[Indication]\nSymptomatic L pleural effusion.\n[Anesthesia]\nLocal + light sedation.\n[Description]\nUS-guided thoracentesis. Left 8th interspace. 1500cc straw fluid removed. Post-proc US negative for PTX.\n[Plan]\nSend fluid for cytology/chem.",
            8: "This 60-year-old male needed his chest drained due to a large fluid buildup on the left. We did this at the bedside using ultrasound to guide the needle. We removed 1.5 liters of amber fluid, which should help his breathing significantly. We stopped when he started coughing to be safe. A quick ultrasound check afterwards showed no collapsed lung.",
            9: "Procedure: Ultrasound-guided pleural aspiration.\nAction: The left hemithorax was interrogated sonographically. A catheter was introduced into the effusion. 1500mL of exudate was evacuated. \nResult: Symptomatic relief. No sonographic evidence of pneumothorax."
        }
    }
    return variations

def get_base_data_mocks():
    # Base data to ensure consistency with the original file content
    return [
        {"idx": 0, "orig_name": "E Okafor", "orig_age": 65, "names": ["Esther Okafor", "Evelyn Okafor", "Enid Okafor", "Eleanor Okafor", "Eunice Okafor", "Eliza Okafor", "Edith Okafor", "Eva Okafor", "Emma Okafor"]},
        {"idx": 1, "orig_name": "Unknown", "orig_age": 82, "names": ["Margaret Thatcher", "Betty White", "Helen Mirren", "Judi Dench", "Maggie Smith", "Angela Lansbury", "Julie Andrews", "Jane Fonda", "Cicely Tyson"]}, # Just using placeholders for "Old Lady"
        {"idx": 2, "orig_name": "Unknown", "orig_age": 58, "names": ["Sarah Connor", "Ellen Ripley", "Leia Organa", "Dana Scully", "Clarice Starling", "Thelma Dickinson", "Louise Sawyer", "Erin Brockovich", "Beatrix Kiddo"]},
        {"idx": 3, "orig_name": "Rosa M", "orig_age": 61, "names": ["Rosa Martinez", "Rosa Morales", "Rosa Mendez", "Rosa Munoz", "Rosa Medina", "Rosa Moreno", "Rosa Maldonado", "Rosa Murillo", "Rosa Mejia"]},
        {"idx": 4, "orig_name": "Unknown", "orig_age": 75, "names": ["Arthur Dent", "Ford Prefect", "Zaphod Beeblebrox", "Marvin Android", "Slartibartfast", "Trillian Astra", "Deep Thought", "Vogon Jeltz", "Prostetnic Vogon"]},
        {"idx": 5, "orig_name": "Marcus T", "orig_age": 69, "names": ["Marcus Turner", "Marcus Tate", "Marcus Thompson", "Marcus Taylor", "Marcus Thomas", "Marcus Tucker", "Marcus Todd", "Marcus Tyler", "Marcus Trent"]},
        {"idx": 6, "orig_name": "Unknown", "orig_age": 62, "names": ["Bruce Wayne", "Clark Kent", "Diana Prince", "Barry Allen", "Hal Jordan", "Arthur Curry", "Victor Stone", "Oliver Queen", "Billy Batson"]},
        {"idx": 7, "orig_name": "Juan C R", "orig_age": 67, "names": ["Juan Carlos Rivera", "Juan Camilo Rodriguez", "Juan Cristobal Ramirez", "Juan Cruz Reyes", "Juan Claudio Ruiz", "Juan Cesar Romero", "Juan Cortez Ramos", "Juan Castillo Rios", "Juan Cabrera Rojas"]},
        {"idx": 8, "orig_name": "Michelle B", "orig_age": 54, "names": ["Michelle Baker", "Michelle Brown", "Michelle Barnes", "Michelle Brooks", "Michelle Bennett", "Michelle Bell", "Michelle Bailey", "Michelle Butler", "Michelle Boyd"]},
        {"idx": 9, "orig_name": "Unknown", "orig_age": 60, "names": ["Tony Stark", "Steve Rogers", "Thor Odinson", "Bruce Banner", "Natasha Romanoff", "Clint Barton", "Nick Fury", "Phil Coulson", "Maria Hill"]}
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
                print(f"Warning: Missing variation text for Note {idx}, Style {style_num}")
            
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
    output_filename = output_dir / "synthetic_edge_cases_part_053.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()