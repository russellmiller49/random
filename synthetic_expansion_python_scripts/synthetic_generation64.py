import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_064.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations.
    Structure: Note_Index (0-14) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # TBA-001: RLL Microwave Ablation (Illumisite)
            1: "Procedure: Nav bronchoscopy (Illumisite) w/ microwave ablation.\n- Target: 18mm RLL posterior basal nodule.\n- Action: Navigated to lesion. Confirmed w/ CBCT. Emprint catheter placed.\n- Ablation: 10 min at standard power.\n- Result: Ground-glass ablation zone, 6mm margin. No pneumothorax.\n- Plan: Discharge home.",
            2: "OPERATIVE REPORT: The patient presented with a biopsy-proven, PET-avid nodule in the right lower lobe posterior basal segment. Under general anesthesia, electromagnetic navigation bronchoscopy utilizing the Illumisite platform was performed. Following registration and tomosynthesis correction, the lesion was targeted. An Emprint microwave ablation catheter was precisely positioned under cone-beam CT guidance. A single cycle of microwave energy was delivered for 10 minutes. Post-ablation imaging confirmed a concentric ablation zone with adequate oncologic margins. The patient remained hemodynamically stable throughout.",
            3: "CPT 31641 (Bronchoscopy with destruction of tumor) and 31627 (Navigation Bronchoscopy). The procedure utilized electromagnetic navigation to access a peripheral RLL lesion. Cone-beam CT (CBCT) verified tool-in-lesion. Microwave ablation (Emprint system) was the modality of destruction, applied for 10 minutes to achieve tumor necrosis. Medical necessity: Nonsurgical candidate with early-stage malignancy.",
            4: "Procedure: RLL Microwave Ablation\nAttending: Dr. Rivera\nSteps:\n1. GA, 8.5 ETT.\n2. Navigated to RLL posterior basal segment using Illumisite.\n3. Used CBCT to confirm needle/catheter placement.\n4. Advanced Emprint catheter.\n5. Ablated for 10 mins.\n6. Post-op CBCT showed good margin.\nNo complications. Extubated to PACU.",
            5: "patient with rll nodule here for ablation. used the illumisite nav system. got out to the posterior basal segment. verified with the cone beam ct looks good. put the emprint needle in ran it for 10 minutes. margin looked like 6mm on the scan after. no pneumo seen. patient woke up fine sent to recovery.",
            6: "The patient was brought to the hybrid OR for ablation of an 18 mm RLL nodule. General anesthesia was induced. Using the Illumisite navigation system, we accessed the posterior basal segment. Cone-beam CT confirmed the catheter was centered in the lesion. We performed a 10-minute microwave ablation using the Emprint system. Final imaging showed a 6 mm circumferential margin. The patient tolerated the procedure well without complications.",
            7: "[Indication]\nHigh-risk stage IA NSCLC, RLL posterior basal segment.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nNavigated to RLL. CBCT confirmed position. 10-min microwave ablation delivered via Emprint. 6mm margin achieved. No bleeding.\n[Plan]\nDischarge today. CT in 3 months.",
            8: "Dr. Rivera performed a microwave ablation on a right lower lobe nodule today. Using the Illumisite navigation system, the team guided a catheter to the posterior basal segment. Cone-beam CT scans ensured the tip was right inside the 18 mm tumor. They applied microwave energy for 10 minutes, creating a zone of treated tissue that extended well past the tumor edges. The patient woke up smoothly and is set to go home later today.",
            9: "Indication: Local control of RLL neoplasm.\nProcedure: Electromagnetic guidance with thermal destruction.\nAction: The device was steered to the posterior basal segment. Tomosynthesis validated the location. The Emprint probe was inserted, and thermal energy was administered for 10 minutes. Post-treatment imaging verified a sufficient ablation zone.\nOutcome: Successful tumor necrosis."
        },
        1: { # TBA-002: RUL Microwave Ablation (Ion)
            1: "Procedure: Robotic Bronchoscopy (Ion) w/ Microwave Ablation.\n- Target: 12mm RUL apical nodule.\n- Guidance: Shape-sensing robotic nav + Cios Spin 3D C-arm.\n- Action: Overlapping ablations (8 min + 6 min) w/ Emprint.\n- Result: 7mm margin achieved.\n- Plan: Admit overnight.",
            2: "OPERATIVE NARRATIVE: This patient with a solitary RUL apical nodule and prior lobectomy underwent robotic-assisted bronchoscopy. The Ion endoluminal system facilitated navigation to the ninth-generation airway. Intraoperative 3D fluoroscopy (Cios Spin) verified tool-in-lesion status. To ensure complete eradication of the 12 mm lesion, two overlapping microwave ablation cycles were delivered. Post-procedural imaging demonstrated a confluent ablation zone exceeding the target volume. Hemostasis was secured.",
            3: "Primary Code: 31641 (Destruction of tumor, RUL). Add-on: 31627 (Navigation). The service involved robotic assistance (Ion platform) to navigate to a peripheral apical lesion. 3D rotational fluoroscopy was used for target verification. Microwave energy was applied in two cycles to destroy the tumor. The complexity of the robotic navigation supports the add-on code.",
            4: "Resident Note\nPt: TBA-002\nProc: Robotic Nav + MWA (RUL)\n1. Ion robot docked.\n2. Navigated to apical RUL nodule.\n3. 3D Spin scan confirmed position.\n4. Emprint catheter placed.\n5. Ablated x2 (8 min, 6 min).\n6. Final spin showed good coverage.\nPlan: Admit for obs (prior lobectomy).",
            5: "rul nodule ablation with the ion robot. drove the robot out to the apical segment. used the cios spin for the 3d pic. confirmed we were in the nodule. did two burns 8 mins and 6 mins to make sure we got it all. margin looked big enough like 7mm. minimal bleeding. admitting overnight just to be safe.",
            6: "Under general anesthesia, the Ion robotic system was used to navigate to a 12 mm nodule in the RUL apical segment. Cios Spin 3D imaging confirmed the catheter position. We performed two overlapping microwave ablations using the Emprint catheter to ensure adequate margins. Post-ablation imaging showed a 7 mm margin. The patient was extubated and transferred to the floor for overnight observation.",
            7: "[Indication]\nMetachronous stage IA adenocarcinoma, RUL.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nRobotic navigation to apical segment. 3D C-arm confirmation. Double microwave ablation (8+6 min). 7mm margin obtained. No pneumothorax.\n[Plan]\nAdmit overnight.",
            8: "Using the Ion robotic system, we successfully treated a small nodule in the top of the right lung. We steered the flexible robot arm deep into the airways and used a 3D X-ray spin to confirm we were on target. We then applied microwave heat twice to destroy the tumor and a rim of healthy tissue around it. The final scan showed excellent coverage of the cancer.",
            9: "Indication: RUL lesion eradication.\nProcedure: Robotic-assisted guidance with thermal necrosis.\nAction: The robotic scop was piloted to the apical target. 3D imaging verified alignment. Two cycles of thermal energy were deployed. The treatment volume encompassed the lesion with adequate boundaries.\nOutcome: Effective local therapy."
        },
        2: { # TBA-003: RLL Superior Microwave Ablation (Illumisite)
            1: "Procedure: Nav Bronch w/ MWA.\n- Target: 24mm RLL superior segment nodule.\n- Action: Navigated w/ Illumisite. CBCT confirmation.\n- Ablation: Two burns (10 min + 7 min) w/ retraction.\n- Complication: Small apical pneumothorax, conservative mgmt.\n- Plan: Discharge POD#1.",
            2: "OPERATIVE SUMMARY: The patient presented for palliative local control of a 2.4 cm RLL superior segment neoplasm. Electromagnetic navigation utilizing the Illumisite platform guided the catheter to the lesion, confirmed by tomosynthesis and cone-beam CT. To accommodate the lesion's longitudinal axis, two sequential microwave ablations were delivered with interval catheter retraction. Post-procedural imaging revealed a comprehensive ablation zone but noted a small, asymptomatic apical pneumothorax not requiring thoracostomy.",
            3: "Code 31641 (Destruction of tumor, RLL). Code 31627 (Navigation). Procedure utilized Illumisite EM navigation and CBCT guidance. A 2.4 cm lesion required a composite ablation (10 min and 7 min) to achieve margins. A small pneumothorax occurred but did not require chest tube insertion (no separate code for management of complication unless significant).",
            4: "Procedure: RLL MWA\nStaff: Dr. Patel\n1. Navigated to RLL superior segment.\n2. Updated nodule position with tomo.\n3. Two ablations: 10 min then 7 min pullback.\n4. CBCT showed good zone.\n5. Noted small PTX on final scan, stable.\nPlan: Obs overnight, CXR series.",
            5: "ablation of rll superior nodule big one 24mm. illumisite nav used. had to adjust for divergence. did two burns 10 mins and 7 mins pulling back a bit. looks like we got it all 5mm margin. tiny pneumo at the apex pt feels fine no tube needed. discharge tomorrow.",
            6: "Electromagnetic navigation bronchoscopy was performed to target a 24 mm nodule in the RLL superior segment. Using cone-beam CT guidance, we positioned the microwave catheter. Two overlapping ablations were performed to cover the lesion length. Post-ablation imaging confirmed good margins but revealed a small apical pneumothorax. The patient remained stable and was observed overnight.",
            7: "[Indication]\nInoperable RLL superior segment CA.\n[Anesthesia]\nGeneral, 8.0 ETT.\n[Description]\nNavigated to lesion. Two sequential ablations (10+7 min) performed. 5-6mm margin achieved. Small asymptomatic pneumothorax noted.\n[Plan]\nMonitor overnight, serial CXRs.",
            8: "We treated a 2.4 cm tumor in the right lower lung using a microwave catheter. Because the tumor was large, we burned it in two steps, pulling the catheter back slightly to extend the treatment zone. The follow-up scan showed we successfully covered the tumor, though we did spot a small air leak (pneumothorax) which is stable and doesn't need a tube. We'll watch him overnight.",
            9: "Indication: RLL malignancy treatment.\nProcedure: Electromagnetic steering with thermal ablation.\nAction: The device was guided to the superior segment. Two cycles of energy were administered with catheter repositioning. A resultant pneumothorax was observed but deemed non-critical.\nOutcome: Lesion destroyed, conservative management for PTX."
        },
        3: { # TBA-004: LLL Cryobiopsy + Microwave Ablation
            1: "Procedure: Nav Bronch, Cryobiopsy, MWA.\n- Target: 16mm LLL lateral basal nodule.\n- Action: Radial EBUS confirmation. Cryobiopsy x2 (Adeno CA). MWA 10 min.\n- Result: 5mm margin, mild hemorrhage.\n- Plan: Admit overnight.",
            2: "OPERATIVE REPORT: The patient underwent a combined diagnostic and therapeutic procedure for a peripheral LLL nodule. Electromagnetic navigation and radial EBUS localized the lesion. Transbronchial cryobiopsy provided a diagnosis of adenocarcinoma via frozen section. Subsequently, an Emprint microwave catheter was deployed. A single 10-minute ablation resulted in a ground-glass opacity enveloping the biopsy cavity. Mild perilesional hemorrhage was noted and controlled.",
            3: "Codes: 31641 (Destruction LLL), 31627 (Nav), 31654 (REBUS). Note: 31628 (Biopsy) is bundled into 31641 per NCCI edits when performed at the same site. The procedure involved navigation, radial EBUS confirmation, diagnostic cryobiopsy, and immediate therapeutic microwave ablation of the confirmed malignancy.",
            4: "Resident Note\nPt: TBA-004\nProc: Dx Cryo + MWA (LLL)\n1. Nav to LLL lateral basal.\n2. REBUS verified lesion.\n3. Cryobiopsy x2 -> Adeno CA confirmed.\n4. MWA catheter placed.\n5. Ablated 10 min.\n6. Minor bleeding controlled w/ ice.\nPlan: Admit.",
            5: "lll nodule frozen section case. nav bronch used. radial ebus saw the lesion. took cryo biopsies path said cancer. went ahead and ablated it 10 minutes. some bleeding from the biopsy made the scan a bit fuzzy but margin looks ok. iced saline stopped the bleeding. admit.",
            6: "Combined biopsy and ablation performed for 16 mm LLL nodule. Navigation and radial EBUS located the target. Cryobiopsy confirmed adenocarcinoma. We proceeded to microwave ablation for 10 minutes. Cone-beam CT showed the ablation zone covered the biopsy site. Mild hemorrhage was controlled. Patient stable.",
            7: "[Indication]\nLLL nodule, dx and tx.\n[Anesthesia]\nGeneral.\n[Description]\nNav/REBUS loc. Cryobiopsy: Adenocarcinoma. MWA: 10 min burn. 5mm margin. Mild hemorrhage controlled.\n[Plan]\nAdmit for observation.",
            8: "This was a 'one-stop' procedure for a spot in the left lower lung. First, we navigated to the spot and took biopsies using a freezing probe, which confirmed cancer right there in the room. We immediately switched gears and used a microwave probe to burn the tumor away for 10 minutes. There was a little bleeding from the biopsy, but the final scan showed we effectively treated the area.",
            9: "Indication: LLL lesion diagnosis and eradication.\nProcedure: Navigation with cryo-sampling and thermal necrosis.\nAction: Radial ultrasound localized the target. Tissue was sampled and malignancy confirmed. Thermal energy was delivered for 10 minutes. Hemostasis was secured.\nOutcome: Simultaneous diagnosis and treatment."
        },
        4: { # TBA-005: RML Double Microwave Ablation
            1: "Procedure: Nav Bronch w/ Double MWA.\n- Target: 25mm RML lateral nodule.\n- Action: Navigated w/ Illumisite. 10 min burn (medial margin thin). Repositioned. 8 min burn.\n- Result: Fused ablation zone, 6mm margin.\n- Plan: Cardiac monitoring overnight.",
            2: "OPERATIVE NARRATIVE: A 2.5 cm neoplasm in the RML lateral segment was targeted for ablation. Utilizing the Illumisite navigation system and cone-beam CT, the lesion was accessed. An initial 10-minute microwave ablation was deemed insufficient regarding the medial margin. Consequently, the catheter was repositioned medially, and a secondary 8-minute ablation was delivered. The final fused ablation zone provided adequate circumferential coverage.",
            3: "Code 31641 (Destruction of tumor, RML) and 31627 (Navigation). Despite two separate burns, 31641 is reported once per lobe/lesion. Navigation utilizing Illumisite and CBCT was integral. The procedure involved repositioning to ensure adequate margins for a large (2.5cm) lesion.",
            4: "Procedure: RML MWA\nStaff: Dr. Alvarez\n1. Nav to RML lateral.\n2. Burn 1: 10 mins. CT showed thin medial margin.\n3. Repositioned catheter.\n4. Burn 2: 8 mins.\n5. CT showed fused zone 6mm margin.\nPt has CAD -> cardiac monitor overnight.",
            5: "rml nodule 25mm. navigated out there. did a 10 minute burn first but the margin wasn't great medially. moved the catheter over a bit and did another 8 minutes. now it looks solid 6mm margin all around. no bleeding. keeping him overnight for heart monitoring.",
            6: "Microwave ablation of a 25 mm RML nodule. Navigation was successful. The first 10-minute ablation left a narrow medial margin. We repositioned the catheter and performed a second 8-minute ablation. The two zones fused to create a 6 mm margin. Airway patent. Patient extubated and stable.",
            7: "[Indication]\n25mm RML nodule, poor surgical candidate.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nNavigated to lesion. Two ablations (10 min + 8 min) required for coverage. Fused zone achieved 6mm margin. No complications.\n[Plan]\nAdmit for cardiac monitoring.",
            8: "We treated a fairly large tumor (2.5 cm) in the middle lobe of the right lung. The first burn covered most of it, but the scan showed we needed to get closer to the inner edge. We adjusted our catheter and burned again for 8 minutes. The two treatment areas merged perfectly to destroy the whole tumor with a safe margin.",
            9: "Indication: RML tumor control.\nProcedure: Electromagnetic guidance with multi-cycle thermal destruction.\nAction: Initial energy delivery was insufficient medially. The probe was adjusted. A supplementary cycle was administered. The resultant necrosis volume was verified by imaging.\nOutcome: Complete lesion coverage."
        },
        5: { # TBA-006: LLL Superior Ground-Glass Nodule
            1: "Procedure: Nav Bronch w/ MWA.\n- Target: 9mm LLL superior GGO.\n- Action: Navigated to segment. CBCT confirmed position. Two burns (6 min + 5 min) w/o repositioning.\n- Result: Spherical ablation zone, 5-6mm margin.\n- Plan: Discharge today.",
            2: "OPERATIVE REPORT: The patient presented with a high-risk ground-glass opacity in the LLL superior segment. Electromagnetic navigation bronchoscopy facilitated access. Given the lesion's subsolid nature, cone-beam CT was crucial for localization. The Emprint catheter was positioned, and two short-duration microwave ablations (6 and 5 minutes) were delivered sequentially to prevent parenchymal overheating while ensuring sterility. Post-ablation imaging confirmed a spherical treatment zone centered on the target.",
            3: "Code 31641 (Destruction, LLL) and 31627 (Navigation). Indication: GGO (likely adenocarcinoma). Technique: Navigation to a peripheral subsolid lesion requiring CBCT for visualization. Two ablation cycles were used for a single small lesion to ensure margin without repositioning (protocol driven).",
            4: "Procedure: MWA for GGO\nAttending: Dr. Osei\n1. Nav to LLL superior.\n2. CBCT to see GGO.\n3. Emprint cath placed.\n4. Ablated 6 min then 5 min.\n5. Good margin on final scan.\nNo bleeding. Pt going home.",
            5: "small ggo in lll superior segment. hard to see but nav got us there. cone beam confirmed it. did two short burns 6 and 5 mins just to be sure. ablation zone looks perfect nice ball shape. no bleeding or pneumo. discharge later today.",
            6: "Ablation of 9 mm LLL ground-glass nodule. Navigation and cone-beam CT used for localization. We performed two sequential ablations of 6 and 5 minutes to treat the lesion. The ablation zone was spherical with a 5-6 mm margin. No complications occurred. Discharged same day.",
            7: "[Indication]\n9mm LLL superior GGO.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to GGO. Confirmed w/ CBCT. MWA x2 (6+5 min). Spherical zone created. 5-6mm margin. No complications.\n[Plan]\nDischarge.",
            8: "This patient had a hazy 'ground-glass' spot in the left lower lung. These are tricky to see, so we used a special CT scan in the operating room to guide us. Once in place, we used two short bursts of microwave energy to destroy the spot. The final picture showed a perfect ball of treated tissue right where the nodule was.",
            9: "Indication: Subsolid pulmonary lesion.\nProcedure: Guided endoscopy with thermal eradication.\nAction: The target was localized via tomosynthesis. Two energy cycles were applied. The ablation volume encompassed the opacity with adequate boundaries.\nResult: Effective focal therapy."
        },
        6: { # TBA-007: RUL Apical Posterior Robotic MWA
            1: "Procedure: Robotic Bronchoscopy (Monarch) w/ MWA.\n- Target: 20mm RUL apical posterior nodule.\n- Action: Robotic nav to lesion. Flex microwave catheter used. Two burns (8+7 min).\n- Result: 6mm margin, nerves preserved.\n- Plan: Admit overnight.",
            2: "OPERATIVE NARRATIVE: A robotic-assisted bronchoscopy was performed using the Monarch platform to address a 20 mm apical posterior RUL nodule. The robotic sheath provided stability for the advancement of a flexible microwave catheter. Cone-beam CT verified alignment. Two overlapping ablations were performed to ensure margins while sparing the brachial plexus and chest wall. Post-ablation imaging confirmed precise energy delivery and adequate margins.",
            3: "Codes: 31641 (Destruction RUL) and 31627 (Navigation). Technology: Monarch robotic platform and Neuwave Flex catheter. The procedure required robotic navigation to a difficult apical location. Multiple overlapping burns were used to treat the 2cm lesion. Medical necessity: High-risk patient (CKD, frailty).",
            4: "Procedure: Robotic MWA (Monarch)\nStaff: Dr. Yamada\n1. Driven robot to RUL apical post.\n2. Confirmed w/ CBCT.\n3. Advanced Neuwave flex catheter.\n4. Ablated 8 min then 7 min.\n5. Good margin, away from chest wall.\nAdmit for obs.",
            5: "rul apical nodule tricky spot. used the monarch robot to hold steady. flex microwave cath went right in. did two burns 8 and 7 mins. stayed away from the nerves. scan looks good 6mm margin. admitting because patient is frail.",
            6: "Robotic bronchoscopy with microwave ablation for RUL apical nodule. Monarch system used for navigation. Neuwave Flex catheter placed. Two overlapping ablations (8 and 7 min) delivered. Good margins achieved avoiding apical structures. Patient stable, admitted for observation.",
            7: "[Indication]\n20mm RUL apical posterior nodule.\n[Anesthesia]\nGeneral.\n[Description]\nRobotic nav (Monarch). Flex MWA catheter. Two burns (8+7 min). 6mm margin. No nerve injury.\n[Plan]\nAdmit.",
            8: "We used the Monarch robot to reach a tumor tucked way up in the top of the right lung. The robot held steady while we passed a flexible microwave wire into the tumor. We burned it twice to be sure, carefully avoiding the nerves near the top of the chest. The treatment area looks excellent.",
            9: "Indication: Apical pulmonary neoplasm.\nProcedure: Robotic endoscopy with thermal destruction.\nAction: The robotic arm was anchored in the target airway. A flexible probe delivered two cycles of thermal energy. Imaging confirmed lesion necrosis and structural preservation.\nOutcome: Safe apical ablation."
        },
        7: { # TBA-008: LLL Basal Microwave Ablation (Cios Spin)
            1: "Procedure: Nav Bronch w/ MWA (Cios Spin).\n- Target: 18mm LLL basal nodule (near diaphragm).\n- Action: Navigated w/ Illumisite. 3D spin verification. Two burns (10+5 min).\n- Result: 5-6mm margin, diaphragm spared.\n- Plan: Admit (monitor liver/volume).",
            2: "OPERATIVE REPORT: The patient, with significant hepatic comorbidity, underwent ablation of a juxta-diaphragmatic LLL nodule. Electromagnetic navigation combined with mobile 3D C-arm (Cios Spin) guidance ensured precise catheter placement. The Emprint catheter was positioned to avoid thermal injury to the diaphragm. A stepped ablation protocol (10 and 5 minutes) was utilized. Final imaging demonstrated a circumferential ablation zone with a safe margin from the diaphragmatic surface.",
            3: "Code 31641 (Destruction LLL) and 31627 (Navigation). Technique involved complex imaging (Cios Spin cone-beam) to safely treat a lesion near the diaphragm. Transbronchial needle was used to tunnel into parenchyma. Two ablation cycles delivered. 31627 justified by EM navigation usage.",
            4: "Procedure: LLL MWA\nStaff: Dr. Silva\n1. Nav to LLL basal.\n2. Cios Spin spin to verify.\n3. Tunneled into lesion.\n4. Ablated 10 min then 5 min.\n5. Final spin: good margin, no diaphragm injury.\nAdmit for liver monitoring.",
            5: "lll nodule right on the diaphragm. liver patient. used illumisite and the cios spin. punched out to the nodule. did 10 mins then 5 mins. kept it away from the diaphragm. margin looks solid. admitting to check liver function.",
            6: "Ablation of 18 mm LLL basal nodule using Illumisite and Cios Spin 3D imaging. Catheter positioned 1 cm past lesion center. Ablation performed for 10 and 5 minutes. Final scan showed good margins sparing the diaphragm. No pneumothorax. Patient admitted.",
            7: "[Indication]\n18mm LLL basal nodule, cirrhosis.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LLL. Cios Spin guidance. Tunneled to lesion. MWA x2 (10+5 min). Diaphragm spared.\n[Plan]\nAdmit overnight.",
            8: "This patient had a tumor sitting right on top of the diaphragm, which was risky because of his liver condition. We used a 3D X-ray spinner in the room to guide our tools precisely. We carefully burned the tumor in two stages to avoid damaging the diaphragm. The final check showed we destroyed the tumor while keeping the diaphragm safe.",
            9: "Indication: Juxta-diaphragmatic lesion.\nProcedure: Guided endoscopy with thermal ablation.\nAction: 3D fluoroscopy verified probe placement. Energy was delivered in two phases. The ablation zone excluded the diaphragm.\nOutcome: Safe lesion necrosis."
        },
        8: { # TBA-009: LUL Lingula Microwave (Single Lung)
            1: "Procedure: Nav Bronch w/ MWA.\n- Target: 15mm Lingular nodule (solitary lung).\n- Action: Single 8 min burn at standard power.\n- Result: 5mm margin. No desaturation.\n- Plan: Step-down unit.",
            2: "OPERATIVE NARRATIVE: This patient, status post right pneumonectomy, presented with a new nodule in the lingula. Lung-preserving microwave ablation was elected. Under general anesthesia with protective ventilation, the lesion was targeted via electromagnetic navigation. A single 8-minute ablation was performed to minimize parenchymal impact while ensuring oncologic efficacy. Cone-beam CT confirmed complete tumor coverage with adequate margins. The patient maintained adequate oxygenation throughout.",
            3: "Code 31641 (Destruction LUL) and 31627 (Navigation). Special consideration: Procedure performed on a single lung (post-pneumonectomy). Navigation and CBCT were critical for precision. A single 8-minute ablation was sufficient for the 1.5 cm lesion.",
            4: "Procedure: Lingula MWA (Single Lung)\nAttending: Dr. Nguyen\n1. Nav to lingula.\n2. Confirmed w/ CBCT.\n3. One 8 min ablation.\n4. Good coverage on scan.\nPt did well, no desats. To Step-down.",
            5: "patient has only one lung. nodule in the lingula. carefully navigated there. used the cone beam. did one 8 minute burn didn't want to overdo it. scan showed we got it with a 5mm rim. oxygen stayed good. step down unit for watch.",
            6: "Microwave ablation of 15 mm lingular nodule in a post-pneumonectomy patient. Navigation and cone-beam CT used. Single 8-minute ablation performed. 5 mm margin achieved. No respiratory compromise. Patient extubated to high-flow O2.",
            7: "[Indication]\n15mm Lingular nodule, single lung.\n[Anesthesia]\nGeneral, protective vent.\n[Description]\nNavigated to lingula. Single 8-min MWA. 5mm margin. No desaturation.\n[Plan]\nStep-down unit.",
            8: "Since this patient only has one lung, we had to be extremely careful. We navigated to the small tumor in the lingula and performed a quick, single 8-minute burn. This successfully destroyed the tumor with a safe margin without taking out too much healthy lung tissue. The patient breathed well throughout the procedure.",
            9: "Indication: Solitary lung neoplasm.\nProcedure: Electromagnetic navigation with focal ablation.\nAction: The probe was guided to the lingula. A single cycle of thermal energy was delivered. Imaging verified lesion encasement.\nResult: Tumor destroyed, function preserved."
        },
        9: { # TBA-010: RLL Superior Microwave + Vapor
            1: "Procedure: Nav Bronch w/ MWA + Vapor.\n- Target: 19mm RLL superior nodule + STAS.\n- Action: 10 min MWA. Vapor delivered to adjacent segment.\n- Result: Extended ablation zone covering STAS.\n- Plan: Admit (expect fever).",
            2: "OPERATIVE REPORT: The patient presented with a RLL nodule exhibiting imaging features of spread-through-airspaces (STAS). A multimodal ablation strategy was employed. First, electromagnetic navigation guided a 10-minute microwave ablation of the primary nodule. Subsequently, to address the locoregional risk, bronchoscopic thermal vapor ablation was applied to the surrounding segmental airways. Post-procedure imaging confirmed a composite ablation zone incorporating both the primary tumor and the adjacent parenchyma.",
            3: "Code 31641 (Destruction RLL) and 31627 (Navigation). Although two modalities (microwave and vapor) were used, they treated the same primary lesion/lobe, so 31641 is reported once. Navigation facilitated access. Vapor was an adjunct for extended margins.",
            4: "Procedure: Combined MWA + Vapor\nStaff: Dr. Rossi\n1. Nav to RLL superior.\n2. MWA 10 mins for nodule.\n3. Vapor catheter placed adjacent.\n4. Vapor delivered for STAS coverage.\n5. CT showed big ablation zone.\nWatch for fever. Admit.",
            5: "complex nodule with spread in rll. did the microwave first for 10 minutes. then used the steam vapor catheter to cook the surrounding area. final scan looks like a huge ground glass area covering everything. patient ok expecting some fever. admit.",
            6: "Multimodal ablation for 19 mm RLL nodule with STAS. Navigation used. 10-minute microwave ablation performed for the core lesion. Thermal vapor ablation was then delivered to the adjacent segment to extend margins. Post-op scan showed extensive coverage. Patient stable.",
            7: "[Indication]\n19mm RLL nodule w/ STAS.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to RLL. 10-min MWA performed. Adjunct vapor ablation delivered. Extended ablation zone achieved.\n[Plan]\nAdmit.",
            8: "We treated a tumor in the right lower lung that looked like it was spreading into the surrounding air sacs. First, we burned the main tumor with microwaves. Then, we used a special steam catheter to treat the lung tissue around it, ensuring we caught any microscopic spreading cells. The final scan showed a large, effective treatment area.",
            9: "Indication: Invasive pulmonary adenocarcinoma.\nProcedure: Navigation with hybrid thermal destruction.\nAction: The core lesion was ablated with microwave energy. The periphery was treated with thermal vapor. Imaging confirmed an extended necrosis volume.\nOutcome: Expanded margin achieved."
        },
        10: { # TBA-011: RLL Medial Basal RFA
            1: "Procedure: Nav Bronch w/ RFA.\n- Target: 17mm RLL medial basal met.\n- Action: Cooled RFA catheter. 12 min burn.\n- Result: Sharp ablation zone, 5mm margin.\n- Plan: Discharge 6 hrs.",
            2: "OPERATIVE NARRATIVE: A solitary colorectal metastasis in the RLL medial basal segment was targeted for local control. Utilizing electromagnetic navigation and pre-procedural planning, a cooled radiofrequency ablation (RFA) catheter was guided to the lesion center. Verification was achieved via cone-beam CT. A single 12-minute cycle of radiofrequency energy was delivered. Post-ablation imaging demonstrated a well-demarcated zone of necrosis with clear margins.",
            3: "Code 31641 (Destruction RLL) and 31627 (Navigation). Method: Radiofrequency Ablation (RFA). Navigation and CBCT were used for placement. A cooled RFA probe was used to deliver a 12-minute treatment cycle. Appropriate for metastatic disease control.",
            4: "Procedure: RLL RFA\nAttending: Dr. Malik\n1. Nav to medial basal RLL.\n2. Confirmed w/ CBCT.\n3. Cooled RFA probe placed.\n4. 12 min ablation.\n5. Good zone on scan.\nNo complications. D/C today.",
            5: "colorectal met in rll. used the nav system to get there. put the rfa catheter in. did a 12 minute burn with the cooling on. scan after showed a nice sharp circle around the tumor. no bleeding. sending home later.",
            6: "Navigation bronchoscopy for RLL colorectal metastasis. Cooled RFA catheter positioned in the medial basal segment. 12-minute ablation performed. Cone-beam CT confirmed good margins. Airway intact. Discharged same day.",
            7: "[Indication]\nRLL colorectal metastasis.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to medial basal. Cooled RFA delivered (12 min). 5mm margin. No pneumothorax.\n[Plan]\nDischarge in 6 hours.",
            8: "We treated a single metastatic spot from colon cancer in the right lower lung. Using navigation, we placed a radiofrequency probe right in the middle of the spot. We ran it for 12 minutes with cooling to protect the airway walls. The final scan showed a clean sphere of treated tissue around the tumor.",
            9: "Indication: Pulmonary metastasis.\nProcedure: Guided endoscopy with radiofrequency necrosis.\nAction: The probe was navigated to the target. Radiofrequency energy was applied for 12 minutes. Imaging verified the ablation boundary.\nOutcome: Local control achieved."
        },
        11: { # TBA-012: LUL Posterior RFA + EBUS
            1: "Procedure: Nav Bronch, REBUS, RFA.\n- Target: 22mm LUL posterior nodule (near vessel).\n- Action: Radial EBUS verified vessel. Cooled RFA x2 (8 min each) w/ rotation.\n- Result: Lesion encased, vessel spared.\n- Plan: Admit overnight.",
            2: "OPERATIVE REPORT: The patient presented with a high-risk LUL posterior segment nodule adjacent to vascular structures. Electromagnetic navigation and radial EBUS facilitated safe access and confirmed the relationship to the vessel. A cooled radiofrequency ablation (RFA) catheter was deployed. To avoid vascular injury while ensuring coverage, two overlapping 8-minute cycles were delivered with catheter rotation. Post-ablation imaging confirmed lesion destruction with vascular preservation.",
            3: "Codes: 31641 (Destruction LUL), 31627 (Navigation), 31654 (REBUS). Radial EBUS was utilized to confirm lesion eccentricity and vascular proximity. RFA was the modality of choice. Two cycles were performed to shape the ablation zone away from the vessel.",
            4: "Procedure: LUL RFA\nStaff: Dr. Hart\n1. Nav to LUL posterior.\n2. REBUS: lesion next to vessel.\n3. RFA catheter placed.\n4. Two 8 min burns, rotated cath.\n5. CT: good burn, vessel ok.\nAdmit for obs.",
            5: "lul nodule close to a vessel. used nav and radial ebus to see it. decided on rfa. did two 8 minute burns rotating the catheter so we didn't hit the vessel. scan looks good tumor covered vessel fine. admit.",
            6: "Ablation of 22 mm LUL nodule near vessel. Navigation and REBUS used. Cooled RFA performed in two 8-minute cycles with rotation. Ablation zone encased lesion without vascular injury. Patient stable.",
            7: "[Indication]\n22mm LUL nodule, vascular proximity.\n[Anesthesia]\nGeneral.\n[Description]\nNav/REBUS guidance. Cooled RFA x2 (8 min). Vessel spared. 6mm margin.\n[Plan]\nAdmit.",
            8: "We treated a tumor in the left upper lung that was very close to a blood vessel. We used ultrasound to see exactly where the vessel was. Then, using a cooled radiofrequency probe, we carefully burned the tumor in two steps, rotating the probe to shape the burn area away from the vessel. The tumor is destroyed, and the vessel is fine.",
            9: "Indication: Perivascular neoplasm.\nProcedure: Navigation with ultrasound and radiofrequency ablation.\nAction: Radial ultrasound defined the vascular margin. Two energy cycles were delivered with repositioning. The ablation zone excluded the major vessel.\nResult: Safe perivascular ablation."
        },
        12: { # TBA-013: RLL PEF Trial
            1: "Procedure: Nav Bronch w/ PEF (Trial).\n- Target: 14mm RLL lateral basal nodule.\n- Action: Investigational PEF catheter. Biphasic pulses delivered.\n- Result: Nonthermal ablation zone. No arrhythmia.\n- Plan: Telemetry overnight.",
            2: "OPERATIVE NARRATIVE: As part of an early feasibility trial, the patient underwent pulsed electric field (PEF) ablation of an RLL nodule. Navigation bronchoscopy guided the investigational catheter to the target. Following confirmation, a protocol-defined series of nonthermal biphasic pulses was delivered. No thermal rise was recorded. Post-procedure imaging demonstrated a sharply demarcated treatment effect without collateral damage. The patient tolerated the procedure without arrhythmia.",
            3: "Codes: 31641 (Destruction RLL) and 31627 (Navigation). Modality: Pulsed Electric Field (PEF) - Investigational/Trial context. 31641 captures the destruction service regardless of energy source (thermal vs non-thermal) provided destruction occurs. Navigation verified placement.",
            4: "Procedure: PEF Ablation Trial\nAttending: Dr. Romero\n1. Nav to RLL lateral basal.\n2. Placed study catheter.\n3. Delivered PEF pulses per protocol.\n4. No temp spike.\n5. CT showed good zone.\nTelemetry overnight.",
            5: "patient in the pef trial. rll nodule. got there with nav. put the special cath in. fired the pulses. no heat generated. scan showed a clean ablation zone. heart rhythm stayed fine. admit for telemetry per protocol.",
            6: "Investigational PEF ablation of 14 mm RLL nodule. Navigation used. Catheter placed. Biphasic electric pulses delivered. No thermal effect. Sharply demarcated zone achieved. No arrhythmia. Patient monitored overnight.",
            7: "[Indication]\nTrial: PEF ablation of RLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to lesion. PEF pulses delivered. Nonthermal ablation achieved. No arrhythmia.\n[Plan]\nTelemetry admission.",
            8: "This patient is in a clinical trial for a new type of ablation using electric pulses instead of heat. We navigated to the tumor in the right lower lung and delivered the pulses. The treatment created a precise zone of treated tissue without heating up the lung. The patient's heart rhythm remained normal throughout.",
            9: "Indication: Clinical trial enrollment.\nProcedure: Navigation with pulsed electric field application.\nAction: The investigational probe was positioned. Non-thermal electric pulses were administered. Imaging verified the treatment effect.\nOutcome: Successful non-thermal ablation."
        },
        13: { # TBA-014: RUL + RLL Microwave (Bilateral/Multifocal)
            1: "Procedure: Nav Bronch w/ MWA x2.\n- Targets: 14mm RUL & 11mm RLL nodules.\n- Action: RUL burn (8 min). RLL burn (6 min).\n- Result: Both ablated, no overlap.\n- Plan: Admit (bilateral treatment).",
            2: "OPERATIVE REPORT: The patient presented with synchronous primary lung cancers in the RUL and RLL. A staged single-session ablation strategy was executed. Navigation bronchoscopy first targeted the RUL posterior segment nodule, which was ablated for 8 minutes. The system was then redirected to the RLL superior segment, where a 6-minute ablation was performed. Cone-beam CT confirmed independent, adequate ablation zones for both lesions.",
            3: "Codes: 31641 (Destruction RUL), 31641-59 (Destruction RLL), 31627 (Navigation). Procedure involved treating two separate lesions in separate lobes (Right Upper and Right Lower). Code 31641 is reported twice; the second instance requires modifier -59 (or -XS) to denote a separate anatomic location.",
            4: "Procedure: Double MWA (RUL + RLL)\nStaff: Dr. Ahmed\n1. Nav to RUL post. Burned 8 min.\n2. Nav to RLL sup. Burned 6 min.\n3. Final CT: both lesions covered.\nNo complications.\nAdmit due to multi-lobar treatment.",
            5: "two spots to treat rul and rll. did the upper one first 8 minutes. moved down to the lower one did 6 minutes. scan showed good burns on both. no bleeding. admitting overnight since we did two spots.",
            6: "Bilateral lobar ablation for synchronous nodules. RUL nodule ablated for 8 minutes. RLL nodule ablated for 6 minutes. Navigation used for both. Final scan showed discrete ablation zones. Patient stable.",
            7: "[Indication]\nSynchronous RUL and RLL nodules.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to RUL -> 8 min MWA. Navigated to RLL -> 6 min MWA. Both lesions ablated. No pneumothorax.\n[Plan]\nAdmit.",
            8: "This patient had two separate lung cancers on the right side: one in the upper lobe and one in the lower lobe. We treated both in the same session. We started with the upper one, burning it for 8 minutes, then moved to the lower one for a 6-minute burn. Both tumors are now destroyed, and he's staying overnight for observation.",
            9: "Indication: Multifocal malignancy.\nProcedure: Navigation with multi-lobar thermal destruction.\nAction: The RUL lesion was ablated. The device was repositioned to the RLL. The second lesion was ablated. Imaging verified dual necrosis zones.\nResult: Synchronous tumors treated."
        },
        14: { # TBA-015: LLL Superior Microwave (Prior LVRS)
            1: "Procedure: Nav Bronch w/ MWA.\n- Target: 21mm LLL superior nodule (Prior LVRS/Emphysema).\n- Action: 10 min burn. Repositioned. 5 min burn.\n- Result: 6mm margin.\n- Plan: Obs 23hr.",
            2: "OPERATIVE NARRATIVE: A patient with severe emphysema and prior lung volume reduction surgery presented for ablation of an LLL superior segment nodule. Navigational bronchoscopy was utilized. An initial 10-minute ablation resulted in a narrow posterolateral margin. To ensure safety and efficacy in this compromised lung, the catheter was repositioned, and a supplementary 5-minute ablation was delivered. Final imaging confirmed a robust margin.",
            3: "Codes: 31641 (Destruction LLL) and 31627 (Navigation). Context: Patient has altered anatomy (prior LVRS) and severe emphysema, necessitating careful planning. Two burns were required for one lesion to achieve margins; billed as single unit of 31641.",
            4: "Procedure: LLL MWA (Post-LVRS)\nAttending: Dr. Shah\n1. Nav to LLL superior.\n2. Initial burn 10 min. Margin thin.\n3. Adjusted cath.\n4. Second burn 5 min.\n5. Good margin now.\nObs 23hr due to COPD.",
            5: "lll nodule in a bad lung prior surgery. navigated in. did 10 minutes first. margin looked tight. moved it a bit and did 5 more. looks good now. keeping him 23 hours to watch breathing.",
            6: "Microwave ablation of 21 mm LLL nodule in patient with prior LVRS. Navigation used. Two ablations (10 and 5 min) performed to ensure posterolateral margin. Final margin 6 mm. No pneumothorax. 23-hour observation.",
            7: "[Indication]\n21mm LLL nodule, severe COPD/prior LVRS.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LLL. MWA x2 (10+5 min). Good margin achieved. No air leak.\n[Plan]\n23hr observation.",
            8: "This patient has very poor lungs and previous lung surgery, so we had to be precise. We targeted a 2.1 cm tumor in the left lower lobe. The first burn was good but missed a tiny edge, so we adjusted and burned it again for 5 minutes. We achieved a safe margin all around and will watch him closely for a day.",
            9: "Indication: Malignancy in compromised lung.\nProcedure: Navigation with multi-phase thermal ablation.\nAction: Initial energy delivery left a narrow margin. Probe repositioned. Supplementary energy delivered. Imaging confirmed safe, complete necrosis.\nOutcome: Successful ablation."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the 15 patients in the source file.
    Names are generated to ensure diversity across the 9 variations.
    """
    return [
        # TBA-001
        {"idx": 0, "orig_name": "TBA-001", "orig_age": 70, "names": ["Arthur Dent", "Ford Prefect", "Zaphod Beeblebrox", "Tricia McMillan", "Slartibartfast", "Marvin Android", "Eddie Computer", "Fook Shooter", "Lunkwill Programmer"]},
        # TBA-002
        {"idx": 1, "orig_name": "TBA-002", "orig_age": 65, "names": ["Luke Skywalker", "Han Solo", "Leia Organa", "Obi-Wan Kenobi", "Anakin Skywalker", "Padme Amidala", "Mace Windu", "Qui-Gon Jinn", "Lando Calrissian"]},
        # TBA-003
        {"idx": 2, "orig_name": "TBA-003", "orig_age": 72, "names": ["James Kirk", "Spock Vulcan", "Leonard McCoy", "Montgomery Scott", "Hikaru Sulu", "Pavel Chekov", "Nyota Uhura", "Christine Chapel", "Janice Rand"]},
        # TBA-004
        {"idx": 3, "orig_name": "TBA-004", "orig_age": 68, "names": ["Frodo Baggins", "Samwise Gamgee", "Meriadoc Brandybuck", "Peregrin Took", "Aragorn Elessar", "Legolas Greenleaf", "Gimli Gloin", "Boromir Denethor", "Gandalf Grey"]},
        # TBA-005
        {"idx": 4, "orig_name": "TBA-005", "orig_age": 75, "names": ["Harry Potter", "Ron Weasley", "Hermione Granger", "Albus Dumbledore", "Severus Snape", "Minerva McGonagall", "Rubeus Hagrid", "Sirius Black", "Remus Lupin"]},
        # TBA-006
        {"idx": 5, "orig_name": "TBA-006", "orig_age": 60, "names": ["Tony Stark", "Steve Rogers", "Bruce Banner", "Thor Odinson", "Natasha Romanoff", "Clint Barton", "Nick Fury", "Maria Hill", "Phil Coulson"]},
        # TBA-007
        {"idx": 6, "orig_name": "TBA-007", "orig_age": 78, "names": ["Bruce Wayne", "Clark Kent", "Diana Prince", "Barry Allen", "Arthur Curry", "Victor Stone", "Hal Jordan", "Oliver Queen", "Dinah Lance"]},
        # TBA-008
        {"idx": 7, "orig_name": "TBA-008", "orig_age": 55, "names": ["Peter Parker", "Mary Jane Watson", "Harry Osborn", "May Parker", "Ben Parker", "Gwen Stacy", "Flash Thompson", "J. Jonah Jameson", "Robbie Robertson"]},
        # TBA-009
        {"idx": 8, "orig_name": "TBA-009", "orig_age": 62, "names": ["Walter White", "Jesse Pinkman", "Skyler White", "Hank Schrader", "Marie Schrader", "Saul Goodman", "Mike Ehrmantraut", "Gustavo Fring", "Todd Alquist"]},
        # TBA-010
        {"idx": 9, "orig_name": "TBA-010", "orig_age": 66, "names": ["Jon Snow", "Daenerys Targaryen", "Tyrion Lannister", "Jaime Lannister", "Cersei Lannister", "Sansa Stark", "Arya Stark", "Bran Stark", "Theon Greyjoy"]},
        # TBA-011
        {"idx": 10, "orig_name": "TBA-011", "orig_age": 71, "names": ["Rick Grimes", "Daryl Dixon", "Carol Peletier", "Maggie Greene", "Glenn Rhee", "Michonne Hawthorne", "Carl Grimes", "Negan Smith", "Eugene Porter"]},
        # TBA-012
        {"idx": 11, "orig_name": "TBA-012", "orig_age": 69, "names": ["Michael Scott", "Jim Halpert", "Pam Beesly", "Dwight Schrute", "Angela Martin", "Kevin Malone", "Oscar Martinez", "Stanley Hudson", "Phyllis Lapin"]},
        # TBA-013
        {"idx": 12, "orig_name": "TBA-013", "orig_age": 58, "names": ["Leslie Knope", "Ron Swanson", "Tom Haverford", "April Ludgate", "Andy Dwyer", "Ben Wyatt", "Chris Traeger", "Ann Perkins", "Donna Meagle"]},
        # TBA-014
        {"idx": 13, "orig_name": "TBA-014", "orig_age": 73, "names": ["Sherlock Holmes", "John Watson", "Mycroft Holmes", "Greg Lestrade", "Molly Hooper", "Mrs. Hudson", "Irene Adler", "Jim Moriarty", "Mary Morstan"]},
        # TBA-015
        {"idx": 14, "orig_name": "TBA-015", "orig_age": 64, "names": ["Homer Simpson", "Marge Simpson", "Bart Simpson", "Lisa Simpson", "Maggie Simpson", "Ned Flanders", "Moe Szyslak", "Barney Gumble", "Seymour Skinner"]}
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
                print(f"Warning: Missing variation text for Note {idx}, Style {style_num}")
                continue
            
            # Update registry_entry fields if they exist
            # Note: The structure of registry_entry might vary. Adjust access paths as needed.
            # Here assuming a flat structure or specific keys based on typical datasets.
            # You might need to update this logic if registry_entry has nested fields like 'patient_data' etc.
            
            # Attempt to update common fields if present directly or in known sub-dictionaries
            if "registry_entry" in note_entry:
                # Direct update if keys exist at top level of registry_entry
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
                
                # If patient_name exists (sometimes it's in the note text only, but if in registry)
                if "patient_name" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["patient_name"] = new_name

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
    output_filename = output_dir / "synthetic_part_064.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()