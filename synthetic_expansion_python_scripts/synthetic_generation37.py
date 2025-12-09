import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_037.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each note index (0-9).
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
        0: { # Note 0: William Anderson (LUL BLVR)
            1: "Pre-op: Severe emphysema, LUL target.\nAnesthesia: General.\nSteps:\n- Airway insp: normal.\n- Chartis LUL: CV negative.\n- 4 Zephyr valves deployed: 5.5mm (lingula), 4.0mm x3 (upper).\n- No complications.\n- Verification: Good seating, reduced LUL volume.\nPlan: Admit, CXR.",
            2: "HISTORY: Mr. Anderson, a 68-year-old male with severe emphysema, presented for bronchoscopic lung volume reduction. \nPROCEDURE: Under general anesthesia, the airway was secured. The left upper lobe was identified as the target. Collateral ventilation was excluded via Chartis assessment. Subsequently, four Zephyr endobronchial valves were deployed into the LUL segmental bronchi. \nOUTCOME: Immediate reduction in lobar volume was observed. The patient remained hemodynamically stable throughout.",
            3: "Procedure: Bronchoscopy with Valve Placement (CPT 31647).\nTarget: Left Upper Lobe.\nDevices: 4 Zephyr Valves.\nTechnique: Chartis assessment confirmed absence of collateral ventilation (required for code). Valves were placed in the Lingular and Upper Division segments. Complete occlusion verified by bronchoscopy and fluoroscopy. Procedure meets criteria for single lobe treatment.",
            4: "Procedure Note\nResident: Dr. Chang\nAttending: Dr. Kim\nSteps:\n1. Time out.\n2. ETT placed.\n3. Scope down. Anatomy checked.\n4. Chartis LUL -> Neg CV.\n5. Placed 4 valves (Zephyr) in LUL.\n6. Checked position. Good.\nPlan: Post-op CXR.",
            5: "bill anderson here for the lung volume reduction left side we put him to sleep tube down looked at the left upper lobe chartis said no collateral vent so we put in four zephyr valves one big one three small ones looks good lung is smaller now no bleeding waking him up sent to recovery thanks.",
            6: "The patient was brought to the endoscopy suite and placed under general anesthesia for bronchoscopic lung volume reduction of the left upper lobe. Initial inspection revealed severe emphysematous changes. Chartis assessment of the LUL was performed and was negative for collateral ventilation. We proceeded to place four Zephyr valves into the target segments. One 5.5mm valve went to the lingula and three 4.0mm valves to the upper division. Placement was uncomplicated. Final inspection showed complete occlusion. The patient tolerated the procedure well.",
            7: "[Indication]\nSevere LUL emphysema, candidate for BLVR.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nScope advanced. LUL isolated. Chartis: CV negative. 4 Zephyr valves deployed in LUL. Good position confirmed.\n[Plan]\nAdmit for observation. Serial CXRs.",
            8: "Mr. Anderson underwent a left upper lobe BLVR procedure today. After induction of anesthesia, we examined the airways and confirmed the target lobe. Using the Chartis system, we verified the absence of collateral ventilation. Following this, we sequentially placed four Zephyr valves into the segmental bronchi of the left upper lobe. We confirmed the position of each valve and noted a reduction in lobar volume. The patient was extubated without incident.",
            9: "Operation: Bronchoscopic lung volume reduction.\nTarget: Left Upper Lobe.\nAction: The airway was surveyed. The LUL was interrogated with Chartis, showing no collateral flow. Four Zephyr prostheses were implanted in the target airways. The devices were seated firmly. The lobe showed signs of atelectasis. The patient was awakened and transferred.",
        },
        1: { # Note 1: Donald Peterson (Revision RUL BLVR)
            1: "Indication: RUL valve migration.\nProc: Bronchoscopy.\nFindings: RB2 valve migrated 1.5cm. RB1/3 stable.\nAction: RB2 valve removed w/ forceps. Granulation debrided. New 5.5mm Zephyr valve deployed proximal RB2.\nResult: Complete RUL occlusion restored.\nPlan: Home in 4h. Antibiotics.",
            2: "OPERATIVE REPORT: Mr. Peterson returned for revision of RUL valves due to radiographic evidence of migration. Under moderate sedation, the airway was inspected. The valve in the RB2 segment was found to be displaced distally. This valve was extracted using removal forceps. The bronchus was prepared, and a larger (5.5mm) Zephyr valve was deployed to ensure stability. Total lobar occlusion was re-established.",
            3: "CPT Codes: 31647 (Bronchoscopy with placement of bronchial valves, initial lobe). Note: Procedure involved both removal of a migrated valve and placement of a new valve in the same target lobe (RUL) to restore occlusion. The primary service is the valve placement/revision of the initial lobe.",
            4: "Resident Note: Valve Revision\nPatient: Donald Peterson\nAttending: Dr. Sullivan\n1. Sedation start.\n2. Scope inserted.\n3. RB2 valve migrated. Removed with forceps.\n4. New valve (5.5mm) placed in RB2.\n5. RB1/RB3 valves checking out okay.\n6. RUL is sealed.\n7. Pt stable.",
            5: "donald peterson back for a check on his valves in the right upper lobe the ct showed one moved so we went in there and yeah the rb2 valve slipped down we pulled it out with the grabbers cleaned it up a bit and put a bigger one in there fits tight now no air leak sending him home later today.",
            6: "Patient underwent revision bronchoscopy for a migrated endobronchial valve in the right upper lobe. Upon inspection the valve in the anterior segment RB2 was noted to be distal to the target site. This was removed without difficulty using forceps. The airway was cleared of mild granulation tissue. A replacement Zephyr valve size 5.5mm was deployed in the segment achieving a secure seal. The other valves were untouched. RUL occlusion was confirmed.",
            7: "[Indication]\nValve migration RUL, symptomatic.\n[Anesthesia]\nModerate Sedation.\n[Description]\nRB2 valve migrated. Removed. Replaced with larger 5.5mm Zephyr valve. Other valves stable. RUL occluded.\n[Plan]\nDischarge after observation. Repeat CT 6wks.",
            8: "We performed a revision bronchoscopy on Mr. Peterson to address a migrated valve in his right upper lobe. After achieving moderate sedation, we entered the airway and located the displaced valve in the RB2 segment. We carefully removed this valve and replaced it with a larger size to prevent future migration. The other valves in the lobe were secure. Final check showed the lobe was completely blocked off.",
            9: "Procedure: Endobronchial valve exchange.\nFindings: Displaced prosthesis in the anterior segment of the right upper lobe.\nIntervention: The displaced unit was retrieved. A larger replacement prosthesis was implanted in the same bronchus. The lobe was fully obstructed upon completion.",
        },
        2: { # Note 2: Ilene Ortiez (Medical Thoracoscopy)
            1: "Dx: Malignant Pleural Effusion.\nProc: Med Thoracoscopy (Left).\nFindings: Carcinomatosis, adhesions.\nAction: 800cc fluid drained. 5mm port -> 8mm port. Biopsies x5 parietal pleura. Pigtail drain placed.\nComplications: None.\nPlan: Path pending.",
            2: "PROCEDURE: Left Medical Thoracoscopy.\nINDICATION: Undiagnosed pleural effusion suspicious for malignancy.\nNARRATIVE: The left pleural space was accessed under local anesthesia and sedation. Inspection revealed diffuse nodularity consistent with carcinomatosis. Multiple biopsies were taken from the parietal pleura for histopathologic analysis. The pleural space was drained, and a 14 Fr pigtail catheter was sited for continued drainage.",
            3: "Coding: 32601 (Diagnostic Thoracoscopy of pleura). Biopsies of parietal pleura performed. Note: CPT 32609 is for lung biopsy; since parietal pleura was sampled, 32601 is the appropriate base code. Catheter placement bundled.",
            4: "Procedure: Pleuroscopy\nPatient: Ilene Ortiez\n1. Lat decubitus position.\n2. US guidance -> access 8th ICS.\n3. Trocar placed.\n4. Drained fluid.\n5. Saw nodules on pleura -> Biopsied x5.\n6. Chest tube placed.\n7. Closed up.",
            5: "ilene ortiez here for the pleuroscopy on the left side drained a lot of fluid like a liter then went in with the scope looked like cancer everywhere took some bites of the pleura 5 of them put a pigtail drain in stitched her up chest xray looks okay.",
            6: "Medical thoracoscopy performed on the left side for evaluation of pleural effusion. Entry achieved at the 8th intercostal space. Approximately 1275cc of fluid removed total. Visual inspection showed diffuse carcinomatosis and adhesions. Biopsies of the parietal pleura were obtained. A 14 French chest tube was placed at the conclusion of the procedure. Patient tolerated well.",
            7: "[Indication]\nMalignant pleural effusion, need tissue.\n[Anesthesia]\nConscious sedation + Local.\n[Description]\nLeft thoracoscopy. Drained effusion. Parietal pleura biopsies x5. Chest tube placed.\n[Plan]\nAwait pathology. Remove suture 2 weeks.",
            8: "Ms. Ortiez underwent a medical thoracoscopy to investigate her pleural effusion. We accessed the pleural space on the left side and drained the fluid. Upon visualization, the pleura appeared abnormal with nodules, so we took five biopsies from the chest wall lining. We then placed a small chest tube to drain any remaining fluid and help the lung re-expand.",
            9: "Operation: Pleuroscopy with pleural sampling.\nFindings: Diffuse neoplastic appearance of the pleural surface.\nTechnique: The pleural cavity was accessed. Fluid was evacuated. Tissue samples were harvested from the parietal surface. A drainage catheter was installed.",
        },
        3: { # Note 3: Tena Hughes (Tracheal Stent)
            1: "Indication: Extrinsic compression L mainstem (Esophageal CA).\nProc: Bronchoscopy + Stent.\nFindings: L mainstem 90% obstructed.\nAction: Dilated. Aero stent (12x40mm) placed. Balloon dilated post-deployment.\nResult: Airway patent (80%).\nPlan: Nebs, humidified O2.",
            2: "OPERATIVE SUMMARY: Ms. Hughes presented with critical left mainstem bronchus stenosis secondary to extrinsic esophageal carcinoma. Rigid bronchoscopy was utilized to secure the airway. A 12x40mm Aero tracheobronchial stent was deployed across the stenosis under fluoroscopic guidance. Subsequent balloon dilation resulted in significant restoration of airway patency.",
            3: "Billing: 31636 (Bronchoscopy with placement of bronchial stent, initial bronchus). Site: Left Mainstem Bronchus. Device: Aero Stent. Fluoroscopy used for positioning. Dilation bundled.",
            4: "Procedure: Rigid Bronch + Stent\nPatient: Tena Hughes\n1. General Anesthesia.\n2. Rigid scope inserted.\n3. L mainstem tight (90%).\n4. Guidewire passed.\n5. Deployed 12x40mm Aero stent.\n6. Ballooned it open.\n7. Airway looks much better.",
            5: "tena hughes esophageal cancer pushing on the airway left side strictly closed off almost completely. we went in with the rigid scope couldn't ventilate well so intubated. put a wire down marked it with paper clips on the chest. slid the aero stent in 12 by 40. ballooned it open. looks way better now like 80 percent open.",
            6: "Rigid and flexible bronchoscopy performed for high grade left mainstem obstruction. The lesion was bypassed and defined fluoroscopically. An Aero 12x40mm stent was deployed in the left mainstem bronchus covering the area of extrinsic compression. The stent was dilated with a balloon to optimize patency. Final inspection showed marked improvement in airway caliber.",
            7: "[Indication]\nExtrinsic compression LMSB.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. High grade stenosis LMSB. 12x40mm Aero stent deployed. Balloon dilated. Patency improved to 80%.\n[Plan]\nHumidified O2. Saline nebs.",
            8: "Ms. Hughes had a stent placed in her left main airway today. The tumor from her esophagus was crushing the airway closed. We used a rigid tube to access the airway and then placed a metal and silicone stent to hold the airway open. After placing it, we used a balloon to expand it fully. She is breathing much better now through that lung.",
            9: "Intervention: Bronchial stenting.\nPathology: Extrinsic compression of the left main bronchus.\nProcedure: A 12x40mm Aero prosthesis was inserted into the stenotic segment. Radial expansion was performed with a balloon catheter. Airway caliber was restored.",
        },
        4: { # Note 4: Robert Berg (Combo Ablation)
            1: "Study: COMBO-ABLATE.\nSite: LUL nodule (3.2cm).\nProc: Cryoablation + Microwave.\nCryo: 2 cycles (-158C).\nMicrowave: 75W x 7min.\nResult: 52mm ablation zone. No complications.\nPlan: Protocol follow-up.",
            2: "CLINICAL SUMMARY: Mr. Berg was treated per the COMBO-ABLATE protocol for a 3.2 cm LUL adenocarcinoma. The procedure involved sequential application of cryoablation followed by microwave ablation to achieve synergistic tumor destruction. Real-time monitoring confirmed adequate thermal spread and an ablation margin encompassing the lesion.",
            3: "Codes: 31641 (Bronchoscopy with destruction of tumor, initial). 31654 (Radial EBUS guidance). Note: Combined modalities (Cryo + Microwave) on the same lesion constitute a single unit of 31641.",
            4: "Research Case: Robert Berg\nTarget: LUL Apicoposterior\n1. Navigated to lesion.\n2. Confirmed w/ r-EBUS.\n3. Cryo x2 cycles.\n4. Wait 15 mins.\n5. Microwave 75W 7 mins.\n6. Post-op EBUS: big ablation zone.\n7. Stable.",
            5: "robert berg in the combo study today left upper lobe tumor big one 3cm. we did the cryo freezing first two rounds got a good ice ball. waited the 15 minutes then hit it with the microwave probe 75 watts. cooked it good. total zone looks huge on the ultrasound. patient did fine no issues.",
            6: "Bronchoscopic ablation of LUL neoplasm performed under clinical trial protocol. Guidance achieved via radial EBUS. Dual modality therapy administered: Cryoablation (ProSense) followed by Microwave Ablation (Neuwave). Total procedure time and parameters per protocol. Post-procedure imaging confirmed satisfactory ablation zone. Patient tolerated procedure well.",
            7: "[Indication]\nLUL Adenocarcinoma, Study Protocol.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LUL lesion. Confirmed REBUS. Cryoablation performed. 15 min interval. Microwave ablation performed. Margins adequate.\n[Plan]\nProtocol imaging and follow-up.",
            8: "Mr. Berg underwent a combination ablation procedure for his lung tumor today. We navigated to the tumor in the left upper lobe and confirmed its location with ultrasound. We first froze the tumor using a cryoprobe, then after a short break, we heated it using a microwave probe. This combination created a large treatment zone that completely covered the tumor.",
            9: "Procedure: Multimodality tumor destruction.\nTarget: Left Upper Lobe mass.\nTechnique: Sequential cryotherapy and microwave energy application.\nVerification: Radial endobronchial ultrasound confirmed targeting and treatment effect. \nOutcome: Successful creation of ablation zone.",
        },
        5: { # Note 5: Tyler Benfield (Stent Removal)
            1: "Indication: Stent removal (resolved mass).\nProc: Rigid Bronch + Stent Removal.\nFindings: Y-stent in trachea.\nAction: En-bloc removal via rigid scope/forceps. L mainstem fragment removed w/ flex scope.\nComplication: Laryngospasm (treated).\nPlan: PACU, D/C.",
            2: "OPERATIVE NOTE: Mr. Benfield underwent rigid bronchoscopy for removal of a tracheal Y-stent following resolution of mediastinal compression. The stent was successfully extracted en-bloc. A residual fragment in the left mainstem was retrieved via flexible bronchoscopy. Post-extubation laryngospasm was managed successfully.",
            3: "Code: 31635 (Bronchoscopy with removal of foreign body). Service includes removal of the stent and any fragments. Diagnostic inspection is bundled.",
            4: "Procedure: Stent Removal\nPatient: Tyler Benfield\n1. Rigid scope in.\n2. Grabbed Y-stent with forceps.\n3. Twisting motion, pulled it out.\n4. Checked airway with flex scope.\n5. Found piece in L main, removed it.\n6. Pt had spasm after, re-intubated briefly, then ok.",
            5: "tyler benfield here to get his stent out mediastinal mass is gone. used the rigid scope grabbed the stent twisted it pulled it out. then looked with the flex scope found a little piece broke off in the left lung grabbed that too. he clamped down after we woke him up laryngospasm had to tube him again for a sec but hes fine now.",
            6: "Rigid bronchoscopy performed for removal of tracheal Y-stent. The stent was grasped and removed intact through the rigid barrel. Subsequent flexible inspection revealed a small stent fragment in the left mainstem which was removed. The airway mucosa was noted to be friable but patent. Patient treated for post-procedure laryngospasm.",
            7: "[Indication]\nStent removal, resolved compression.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Y-stent removed en bloc. Fragment in LMSB removed. Airways patent.\n[Plan]\nObserve in PACU. CXR.",
            8: "We removed Mr. Benfield's tracheal stent today as his condition has improved. We used a rigid tube to grasp the main stent and pull it out. We then double-checked with a flexible camera and found a small piece left behind in the left lung, which we also removed. He had a brief spasm of his vocal cords waking up but recovered quickly.",
            9: "Operation: Retrieval of airway prosthesis.\nMethod: Rigid endoscopy with forceps extraction.\nFindings: Main prosthesis retrieved. Secondary fragment identified and retrieved from left bronchial tree.\nComplication: Transient laryngospasm, resolved.",
        },
        6: { # Note 6: Andrew Thompson (EBUS)
            1: "Indication: Mediastinal LAD.\nProc: EBUS-TBNA.\nStations: 4R, 4L, 7, 11R.\nROSE: Granulomas (Sarcoid).\nSpecimens: 4.\nComplications: None.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA).\nINDICATION: Evaluation of mediastinal lymphadenopathy.\nFINDINGS: Systematic evaluation of the mediastinum was performed. Lymph nodes at stations 4R, 4L, 7, and 11R were visualized and sampled. Rapid On-Site Evaluation (ROSE) demonstrated non-necrotizing granulomas consistent with sarcoidosis in multiple stations.",
            3: "Codes: 31653 (EBUS-TBNA 3 or more stations). Sampled 4R, 4L, 7, 11R (4 distinct stations). Conventional TBNA bundled.",
            4: "EBUS Note\nPatient: Andrew Thompson\n1. 4R: 4 passes, granulomas.\n2. 4L: 4 passes, sarcoid-like.\n3. 7: 4 passes, granulomas.\n4. 11R: 3 passes, adequate.\nDx: Sarcoidosis likely.",
            5: "andrew thompson lymph nodes swollen rule out lymphoma sarcoid. did the ebus sampled 4r 4l 7 and 11r. rose guy said looks like granulomas probably sarcoid. took good samples sent for stains. no issues patient went home.",
            6: "EBUS-TBNA performed for mediastinal staging. Lymph nodes identified and sampled at stations 4R (15mm), 4L (17mm), 7 (22mm), and 11R (10mm). ROSE confirmed adequate cellularity with granulomatous features at all stations. Specimens sent for final pathology and microbiology. Procedure tolerated well.",
            7: "[Indication]\nMediastinal LAD, r/o sarcoid.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA stations 4R, 4L, 7, 11R. ROSE: Non-necrotizing granulomas.\n[Plan]\nDischarge. Follow pathology.",
            8: "Mr. Thompson had an EBUS procedure to check the lymph nodes in his chest. We sampled nodes from four different areas: right and left upper chest, center chest, and right lung root. The preliminary results in the room suggest sarcoidosis, as we saw granulomas. We sent the samples for full testing to confirm.",
            9: "Procedure: Endosonographic lymph node sampling.\nSites: Stations 4R, 4L, 7, 11R.\nMethod: Transbronchial needle aspiration under ultrasound guidance.\nPathology: Cytology suggests granulomatous inflammation.",
        },
        7: { # Note 7: Maria Rodriguez (Cryoablation)
            1: "Indication: LLL nodule (2.6cm).\nProc: Nav Bronch + Radial EBUS + Cryoablation.\nNav: Veran SPiN.\nTarget: LLL lateral basal.\nAblation: 3 cycles (-165C). 5mm margins.\nResult: Hyperechoic zone on EBUS.\nPlan: Admit, CT 24h.",
            2: "OPERATIVE REPORT: Mrs. Rodriguez underwent electromagnetic navigation bronchoscopy with cryoablation for a biopsy-proven adenocarcinoma in the left lower lobe. The lesion was localized using the Veran system and confirmed with radial EBUS. A cryoprobe was advanced, and three freeze-thaw cycles were administered to ensure oncologic margins. Post-ablation EBUS demonstrated complete coverage of the target.",
            3: "Codes: 31641 (Destruction of tumor), 31627 (Navigation), 31654 (REBUS). Procedure involved navigation to peripheral lesion, confirmation, and destruction via cryotherapy.",
            4: "Procedure: Cryoablation\nPatient: Maria Rodriguez\n1. Navigated to LLL lateral basal.\n2. Confirmed w/ R-EBUS (2.6cm lesion).\n3. Inserted cryoprobe.\n4. Freezing x3 cycles (modified for size).\n5. Ice ball seen on EBUS.\n6. No bleeding.\nPlan: Admit.",
            5: "maria rodriguez cancer in the left lower lobe cant do surgery. we did the navigation bronch found the spot with the spinner system. checked with the ultrasound probe yup thats it. put the freeze probe in did three cycles extra safe. froze it solid. patient did fine admitted for observation.",
            6: "Electromagnetic navigation bronchoscopy and cryoablation performed for LLL adenocarcinoma. Target lesion 2.6cm in lateral basal segment. Navigation successful. Radial EBUS confirmed concentric view. Cryoablation performed with three freeze-thaw cycles achieving temperatures below -160C. Post-ablation imaging consistent with successful treatment.",
            7: "[Indication]\nLLL Adenocarcinoma, nonsurgical.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LLL. REBUS confirmed. Cryoablation x3 cycles. Margins confirmed.\n[Plan]\nAdmit. Resume apixaban 24h.",
            8: "Mrs. Rodriguez had a procedure to freeze a lung tumor in her left lower lobe. We used a navigation system to guide a catheter to the tumor, confirmed it was the right spot with ultrasound, and then used a cryoprobe to freeze the tumor three times. The ultrasound showed the ice ball covered the whole tumor.",
            9: "Intervention: Tumor destruction via cryotherapy.\nGuidance: Electromagnetic navigation and radial ultrasonography.\nTarget: Left lower lobe nodule.\nOutcome: Successful thermal ablation.",
        },
        8: { # Note 8: Timothy Brooks (RFA)
            1: "Indication: Post-biopsy hemorrhage RUL + Tumor Rx.\nProc: Nav Bronch + RFA.\nTarget: RUL posterior.\nAction: RFA 40W (hemostasis) -> 90C (ablation).\nOutcome: Bleeding stopped. Tumor ablated.\nPlan: ICU, keep chest tube.",
            2: "EMERGENT PROCEDURE: Mr. Brooks required urgent bronchoscopic intervention for hemorrhage following transthoracic biopsy. Navigation was used to localize the bleeding site within the RUL tumor. Radiofrequency ablation was applied first for hemostasis, followed by a full ablation protocol to treat the underlying malignancy. Hemostasis was achieved.",
            3: "Codes: 31641 (Destruction/Hemostasis via RFA), 31627 (Navigation). RFA used for both control of hemorrhage and tumor destruction in the same session.",
            4: "Urgent Bronch: Timothy Brooks\nIndication: Bleeding after IR biopsy.\n1. Intubated.\n2. Navigated to RUL bleeding site.\n3. RFA probe in.\n4. Cauterized bleeding (stopped).\n5. Burned the tumor while we were there.\n6. Chest tube output dropped.",
            5: "timothy brooks bleeding from that biopsy yesterday chest tube putting out blood. went in with the scope navigated to the spot in the right upper lobe. used the rfa probe to stop the bleeding worked great. then just decided to ablate the tumor too since we were there. bleeding stopped chest tube looks good.",
            6: "Emergency bronchoscopy performed for hemothorax post-biopsy. Electromagnetic navigation utilized to reach RUL posterior segment target. Radiofrequency ablation catheter deployed. Initial energy applied for hemostasis successful. Subsequent energy cycles delivered for tumor ablation. Chest tube output diminished significantly.",
            7: "[Indication]\nRUL hemorrhage post-biopsy.\n[Anesthesia]\nGeneral.\n[Description]\nNavigation to RUL. RFA applied for hemostasis and tumor ablation. Bleeding resolved.\n[Plan]\nICU. Monitor output.",
            8: "Mr. Brooks had bleeding after his biopsy yesterday. We performed a bronchoscopy to stop the bleeding. We navigated to the spot in his right lung and used heat (radiofrequency) to seal the bleeding vessels. Once the bleeding stopped, we continued the heat treatment to destroy the tumor itself.",
            9: "Procedure: Hemostasis and tumor destruction via radiofrequency energy.\nMethod: Navigational bronchoscopy.\nOutcome: Cessation of hemorrhage and thermal ablation of the neoplasm.",
        },
        9: { # Note 9: Robert Chen (Microwave)
            1: "Indication: RUL Adenocarcinoma.\nProc: Nav Bronch + REBUS + Microwave.\nTarget: RUL anterior.\nAblation: 60W x 6 min.\nResult: Good coverage.\nPlan: D/C tomorrow.",
            2: "OPERATIVE SUMMARY: Mr. Chen underwent bronchoscopic microwave ablation for an inoperable RUL adenocarcinoma. Electromagnetic navigation and radial EBUS were used to localize the lesion. A microwave antenna was deployed, and ablation was performed at 60 Watts for 6 minutes. Post-ablation imaging confirmed adequate treatment volume.",
            3: "Codes: 31641 (Destruction), 31627 (Navigation), 31654 (REBUS). Microwave ablation of peripheral nodule.",
            4: "Procedure: Microwave Ablation\nPatient: Robert Chen\n1. Navigated to RUL anterior.\n2. Radial EBUS check.\n3. Microwave probe in.\n4. 60W for 6 mins.\n5. No complications.\n6. Extubated.",
            5: "robert chen right upper lobe cancer. did the navigation found it with the ultrasound. put the microwave probe in cooked it for 6 minutes at 60 watts. looks good on the scan afterwards. sending him to pacu.",
            6: "Bronchoscopic microwave ablation performed for RUL malignancy. Localization achieved with electromagnetic navigation and confirmed with radial EBUS. Microwave energy delivered 60W x 6min. Post-procedure assessment indicated successful ablation of target. No complications.",
            7: "[Indication]\nRUL Nodule, Cancer.\n[Anesthesia]\nGeneral.\n[Description]\nENB to RUL. REBUS confirm. Microwave ablation 60W/6min. Good effect.\n[Plan]\nObs overnight.",
            8: "Mr. Chen had a microwave ablation procedure for his lung cancer today. We guided a catheter to the tumor in the right upper lobe, checked the position with ultrasound, and used microwave energy to heat and destroy the tumor. The procedure went smoothly without issues.",
            9: "Intervention: Microwave tumor ablation.\nLocalization: Electromagnetic navigation and radial EBUS.\nSite: Right Upper Lobe.\nExecution: Thermal destruction via microwave antenna.\nStatus: Stable.",
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data to ensure consistency in generated names/ages for the specific indices 
    aligned with the styles.
    """
    return [
        {"idx": 0, "orig_name": "William Anderson", "orig_age": 68, "names": ["Frank Miller", "Arthur P. Henderson", "John Smith", "Bill A.", "william anderson", "Anonymous Male", "William Anderson", "Mr. Anderson", "Subject 876"]},
        {"idx": 1, "orig_name": "Donald Peterson", "orig_age": 67, "names": ["Gary Wilson", "Thomas R. Davies", "Robert Jones", "Don P.", "donald peterson", "Anonymous Male", "Donald Peterson", "Mr. Peterson", "Subject 890"]},
        {"idx": 2, "orig_name": "Ilene Ortiez", "orig_age": 55, "names": ["Maria Garcia", "Elena M. Rodriguez", "Jane Doe", "Ilene O.", "ilene ortiez", "Anonymous Female", "Ilene Ortiez", "Ms. Ortiez", "Subject 117"]},
        {"idx": 3, "orig_name": "Tena Hughes", "orig_age": 60, "names": ["Betty White", "Margaret H. Thatcher", "Susan Black", "Tena H.", "tena hughes", "Anonymous Female", "Tena Hughes", "Ms. Hughes", "Subject 308"]},
        {"idx": 4, "orig_name": "Robert Berg", "orig_age": 71, "names": ["Carl Lewis", "Richard B. Hayes", "Michael Brown", "Bob B.", "robert berg", "Anonymous Male", "Robert Berg", "Mr. Berg", "Subject 323"]},
        {"idx": 5, "orig_name": "Tyler Benfield", "orig_age": 45, "names": ["James Dean", "William T. Riker", "David White", "Ty B.", "tyler benfield", "Anonymous Male", "Tyler Benfield", "Mr. Benfield", "Subject 124"]},
        {"idx": 6, "orig_name": "Andrew Thompson", "orig_age": 61, "names": ["Peter Parker", "Charles X. Xavier", "Chris Evans", "Andy T.", "andrew thompson", "Anonymous Male", "Andrew Thompson", "Mr. Thompson", "Subject 084"]},
        {"idx": 7, "orig_name": "Maria Rodriguez", "orig_age": 70, "names": ["Linda Hamilton", "Sarah J. Connor", "Patricia Moore", "Maria R.", "maria rodriguez", "Anonymous Female", "Maria Rodriguez", "Mrs. Rodriguez", "Subject 984"]},
        {"idx": 8, "orig_name": "Timothy Brooks", "orig_age": 72, "names": ["John Wick", "James B. Bond", "George Clooney", "Tim B.", "timothy brooks", "Anonymous Male", "Timothy Brooks", "Mr. Brooks", "Subject 558"]},
        {"idx": 9, "orig_name": "Robert Chen", "orig_age": 62, "names": ["Bruce Wayne", "Clark K. Kent", "Tom Cruise", "Rob C.", "robert chen", "Anonymous Male", "Robert Chen", "Mr. Chen", "Subject 748"]},
    ]

def main():
    # Load original data
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    generated_notes = []
    
    # Process each note
    for idx, original_note in enumerate(source_data):
        # We only have variations for the first 10 notes in this specific script logic
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Add original note first? No, usually we want the output file to contain the variations.
        # The prompt implies "a python file that has 9 distinct variations for each note...".
        # We will append the modified versions.
        
        # Create 9 variations
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # 1. Update Note Text
            # We use the pre-written variations
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # 2. Randomize Date (Year 2025 fixed for consistency with some prompt logic, or +/- 1 year)
            # Let's stick to 2025 to keep it simple and valid
            new_date = generate_random_date(2025, 2025).strftime("%Y-%m-%d")
            
            # 3. Randomize Age
            new_age = orig_age + random.randint(-3, 3)
            
            # 4. Update Name (in registry entry if exists, mainly metadata)
            new_name = record['names'][style_num - 1]
            
            # Update Registry Fields
            if "registry_entry" in note_entry:
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = new_date
                
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                
                # We don't have a direct 'patient_name' field in registry_entry in the example JSON, 
                # but we can update patient_mrn to be unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"

            # 5. Add Synthetic Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Ensure output directory exists
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    # Save to file
    output_file = output_path / "synthetic_blvr_notes_part_037.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2)
        
    print(f"Generated {len(generated_notes)} notes saved to {output_file}")

if __name__ == "__main__":
    main()