import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_011.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Dictionary structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Patricia Thompson (Bilateral Coils - 31647)
            1: "Indication: Severe homogeneous emphysema.\nAnesthesia: Mod Sedation. 4% Lido.\nProcedure:\n- Airway inspected: mild malacia.\n- RUL: 10 RepneuCoils placed (4 Ant, 3 Apic, 3 Post). Fluoroscopy confirmed.\n- LUL: 10 RepneuCoils placed (4 Apicopost, 3 Ant, 3 Ling). Fluoroscopy confirmed.\nFindings: 20 coils total. No pneumothorax. EBL <10ml.\nPlan: Admit. CXR. Antibiotics.",
            2: "HISTORY: The patient, a 72-year-old female with GOLD Stage IV homogeneous emphysema, presented for bronchoscopic lung volume reduction. \nOPERATIVE NARRATIVE: Under moderate sedation and standard monitoring, the airway was interrogated, revealing mild tracheomalacia. The procedure targeted bilateral upper lobes for coil implantation. Utilizing fluoroscopic guidance, ten 125mm RepneuCoils were deployed into the Right Upper Lobe segments. Subsequently, the Left Upper Lobe was cannulated, and an additional ten coils were deployed. \nIMPRESSION: Successful deployment of 20 endobronchial coils total. Radiographic evaluation confirmed appropriate parenchymal compression without pneumothorax.",
            3: "Code Selection: 31647 (Bronchoscopy with valve/coil placement).\nTechnique: Bilateral treatment.\nDevice: RepneuCoils (125mm).\nQuantity: 20 coils total (10 Right / 10 Left).\nGuidance: Fluoroscopy (18 min).\nJustification: Patient has homogeneous emphysema unsuitable for valves. Coils used to restore elastic recoil. Procedure performed under moderate sedation. Post-procedure CXR confirms device position.",
            4: "Procedure Note\nPt: Patricia Thompson\nStaff: Dr. Miller\nSteps:\n1. Moderate sedation (Versed/Fentanyl).\n2. Scope introduced. Airways patent.\n3. RUL selected. 10 coils placed (Zephyr/Repneu type) under fluoro.\n4. LUL selected. 10 coils placed.\n5. Total 20 coils.\nComplications: None.\nPlan: Admit for obs.",
            5: "patient here for coils for emphysema she has the homogeneous type anesthesia was moderate sedation. Scope went in fine mild malacia in the trachea. We did the right side first put in 10 coils in the RUL used fluoro to see them open up like pigtails. Then went to the left side put 10 more in the LUL. 20 coils all together no bleeding really patient tolerated it good. Chest xray looks fine no pneumothorax sending her to the floor thanks.",
            6: "Bronchoscopic lung volume reduction via endobronchial coil placement. 72-year-old female with severe homogeneous emphysema. Moderate sedation. 10 RepneuCoils were placed in the Right Upper Lobe (RUL) segments using fluoroscopic guidance. 10 RepneuCoils were subsequently placed in the Left Upper Lobe (LUL) segments. Total of 20 coils deployed. Fluoroscopy time 18 minutes. No immediate complications. Post-procedure chest radiograph negative for pneumothorax.",
            7: "[Indication]\nSevere homogeneous emphysema, GOLD IV.\n[Anesthesia]\nModerate Sedation (Midazolam/Fentanyl).\n[Description]\nBilateral coil placement. 10 coils deployed in RUL. 10 coils deployed in LUL. Fluoroscopic confirmation of pigtail formation. Minimal blood loss.\n[Plan]\nAdmit overnight. Levofloxacin prophylaxis. Follow up 2 weeks.",
            8: "The patient underwent bilateral endobronchial coil placement today for severe emphysema. We achieved moderate sedation and inserted the bronchoscope. Starting in the right upper lobe, we placed 10 coils distributed across the segments under fluoroscopy. We then moved to the left upper lobe and placed another 10 coils. The patient tolerated the deployment of all 20 coils well with no oxygen desaturation.",
            9: "Operation: Bronchoscopy with implantation of endobronchial coils.\nSubject: 72-year-old female.\nAction: Under moderate sedation, the scope was navigated to the RUL. Ten RepneuCoils were deposited. The scope was then navigated to the LUL, where ten additional coils were deposited.\nResult: 20 coils implanted total. Radiography verified positions."
        },
        1: { # Sharon Kim (LLL BLVR - 31647)
            1: "Dx: Alpha-1 Emphysema. LLL target.\nProcedure: Chartis LLL -> CV Negative (<30mL/min).\nImplants: 2 Zephyr valves (LB6, LB8-10).\nDetails: LB6 valve repositioned once. Complete occlusion confirmed.\nComplications: None.\nPlan: Admit. Monitor for pneumo.",
            2: "CASE SUMMARY: Ms. Kim, a 69-year-old female with Alpha-1 Antitrypsin Deficiency, presented for LLL valve therapy.\nPROCEDURE: The airway was examined utilizing a flexible bronchoscope. The Chartis system assessed the LLL, demonstrating a negative collateral ventilation phenotype (flow decay to zero). Based on CT sizing, a 5.5mm valve was selected for LB6 and a 4.0mm valve for the basilar trunk. The LB6 valve required initial repositioning to ensure an airtight seal. Final inspection confirmed total lobar isolation.\nOUTCOME: Successful LLL BLVR. Patient stable.",
            3: "CPT: 31647 (Endobronchial valve placement, initial lobe).\nTarget Lobe: Left Lower Lobe (LLL).\nDiagnostic: Chartis assessment (performed same session, bundled).\nDevices: 2 Zephyr valves deployed.\nSpecifics: One valve in superior segment (LB6), one in basilar trunk (LB8-10). Repositioning performed to ensure seal (included in base code).",
            4: "Resident Note\nPatient: Sharon Kim\nAttending: Dr. Williams\nProcedure: BLVR LLL\nSteps:\n1. Airway exam.\n2. Chartis LLL: Negative CV.\n3. Measured bronchi. Picked valve sizes.\n4. Deployed valve in LB6 (had to adjust it once).\n5. Deployed valve in LB8-10.\n6. Occlusion confirmed.\nPlan: Admit per protocol.",
            5: "Sharon has alpha 1 we are doing the valves in the lower left lobe today. Chartis showed no flow so good to go. Put a valve in the superior segment and one in the basilar segment. The first one needed to be moved a bit to seal right but we got it. Two valves total both zephyr. No bleeding patient woke up fine admitting for observation.",
            6: "Bronchoscopic lung volume reduction left lower lobe. Patient with Alpha-1 antitrypsin deficiency. Chartis assessment of LLL confirmed absence of collateral ventilation. Two Zephyr valves were deployed. One 5.5mm valve in LB6 and one 4.0mm valve in LB8-10. Complete lobar occlusion was verified visually. Patient tolerated procedure well.",
            7: "[Indication]\nAlpha-1 Antitrypsin Emphysema, LLL predominant.\n[Anesthesia]\nModerate Sedation.\n[Description]\nChartis LLL: CV Negative. Valves placed in LB6 and LB8-10. LB6 valve repositioned for better seal. Total 2 valves. Occlusion achieved.\n[Plan]\nAdmit. Steroids/Antibiotics.",
            8: "We performed a bronchoscopy to place valves in Ms. Kim's left lower lobe. After confirming the fissure was complete using the Chartis system, we sized the airways. We placed one valve in the superior segment and one in the basilars. The superior valve needed a slight adjustment to get a perfect seal. Once both were in, the lobe was completely closed off.",
            9: "Procedure: Flexible bronchoscopy with installation of endobronchial valves.\nTarget: Left Lower Lobe.\nAction: Chartis confirmed lack of collateral ventilation. Two Zephyr valves were implanted in the LLL segmental bronchi. One valve was adjusted to ensure a seal.\nResult: Complete lobar obstruction."
        },
        2: { # Chloe Whitford (Bilateral Mass/Biopsy - 31629, 31625, 31628, 31654)
            1: "Indication: Bilateral lung masses.\nFindings: Fungating mass RUL. Peripheral lesion LLL.\nSampling:\n- RUL: Endobronchial bx x6, TBNA x5.\n- LLL: Radial EBUS utilized. TBNA x4, TBLB x5.\n- BAL LLL superior segment.\nResults: ROSE RUL = Malignant. LLL = Necrosis.\nComplications: Moderate bleeding, epi used.",
            2: "OPERATIVE REPORT: The patient presented with bilateral pulmonary opacities. Inspection revealed a fungating endobronchial lesion obstructing the RUL. This was sampled via endobronchial forceps biopsy and transbronchial needle aspiration. Attention was turned to the LLL, where a peripheral lesion was localized utilizing radial endobronchial ultrasound (r-EBUS). Transbronchial biopsy and needle aspiration were performed. Bronchoalveolar lavage was obtained from the LLL. Hemostasis was achieved with topical epinephrine after moderate hemorrhage.",
            3: "Coding Data:\n- 31625: Endobronchial biopsy (RUL mass).\n- 31629: TBNA (RUL mass).\n- 31628: Transbronchial biopsy (LLL lesion).\n- 31633: TBNA add'l lobe (LLL lesion - *correction: usually 31629 covers multiple, check edits*).\n- 31654: Radial EBUS (LLL guidance).\n- 31624: BAL (LLL).\nJustification: Distinct lesions in separate lobes requiring different sampling techniques.",
            4: "Procedure: Bronchoscopy w/ Biopsy\nPatient: Chloe Whitford\nSteps:\n1. ETT 8.5.\n2. RUL mass seen -> Biopsied (forceps + needle).\n3. LLL lesion found with Radial EBUS -> Biopsied (forceps + needle).\n4. BAL done in LLL.\n5. Bleeding controlled with epi.\nPathology: RUL looks malignant.",
            5: "Patient has two lung masses one in the RUL one in the LLL. The RUL one was visible endobronchially huge mass we took bites and needle aspirates. The LLL one we needed the radial EBUS to find it. Did needle and forceps biopsies there too plus a wash. There was some bleeding we used epi to stop it. ROSE said RUL is cancer LLL uncertain.",
            6: "Flexible bronchoscopy for bilateral lung masses. RUL endobronchial mass identified and sampled via TBNA and forceps biopsy. LLL peripheral lesion identified via radial EBUS and sampled via TBNA and transbronchial biopsy. BAL performed in LLL. Moderate bleeding controlled with epinephrine. ROSE confirmed malignancy in RUL.",
            7: "[Indication]\nSuspected malignancy, bilateral masses.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nRUL fungating mass biopsied (forceps, TBNA). LLL lesion located with Radial EBUS, biopsied (TBLB, TBNA). BAL LLL. Moderate bleeding controlled.\n[Plan]\nPathology pending. CXR.",
            8: "We examined Ms. Whitford's airways and found a large mass blocking the right upper lobe segments. We took several samples using both needles and forceps. Then we moved to the left lower lobe, where we used the ultrasound probe to find a second lesion and sampled that as well. We also did a lavage. There was a fair amount of bleeding, but we stopped it with epinephrine.",
            9: "Procedure: Diagnostic bronchoscopy with tissue sampling.\nFindings: Obstructing mass in RUL; peripheral nodule in LLL.\nAction: The RUL mass was sampled via forceps and needle. The LLL nodule was localized with radial ultrasound and sampled. Lavage was performed.\nOutcome: Samples sent for analysis. Hemostasis secured."
        },
        3: { # William Anderson (LUL Zephyr - 31647)
            1: "Dx: End-stage COPD, LUL predominant.\nChartis: No CV.\nProcedure: 4 Zephyr valves placed in LUL (1x 5.5mm, 3x 4.0mm).\nResult: Complete occlusion.\nComplications: None.\nPlan: Discharge/Obs.",
            2: "PROCEDURE NOTE: Mr. Anderson presented for LUL volume reduction. Following Chartis confirmation of fissure integrity (absence of collateral ventilation), the target lobe was treated. Four Zephyr endobronchial valves were deployed: one 5.5mm unit in the lingula and three 4.0mm units in the upper division. Visual inspection confirmed adequate seating and lobar occlusion. The patient remained stable throughout.",
            3: "Code: 31647 (Bronchoscopy with valve placement).\nSite: Left Upper Lobe.\nUnits: 4 valves.\nMedical Necessity: Severe emphysema, intact fissures confirmed by Chartis (bundled). Valves sized and deployed to occlude Lingula and Upper Division bronchi.",
            4: "Resident Note\nPatient: Bill Anderson\nProcedure: BLVR LUL\nSteps:\n1. Chartis check: No CV.\n2. Measured segments.\n3. Placed 4 valves total (Zephyr).\n4. Checked placement with fluoro.\n5. No issues.\nPlan: Monitor for pneumo.",
            5: "Dr Kim here doing a valve procedure on Mr Anderson. LUL emphysema. We checked with chartis and it was negative for collateral ventilation. Put in four valves total mixed sizes 5.5 and 4.0s. They look good fluoro shows them working. No complications patient woke up fine.",
            6: "Bronchoscopic lung volume reduction left upper lobe. Chartis assessment demonstrated absent collateral ventilation. Four Zephyr endobronchial valves were placed in the LUL segmental bronchi. One 5.5mm valve and three 4.0mm valves were utilized. Complete occlusion achieved. Post-procedure imaging confirmed valve position.",
            7: "[Indication]\nEnd-stage COPD, LUL hyperinflation.\n[Anesthesia]\nModerate Sedation.\n[Description]\nChartis LUL: No CV. 4 Zephyr valves deployed. Complete occlusion. Stable.\n[Plan]\nObservation. Serial CXRs.",
            8: "Mr. Anderson came in for his lung volume reduction. We confirmed that his left upper lobe was a good target using the Chartis balloon. We then placed four valves into the airway segments of that lobe. Everything fit perfectly, and we could see the lobe starting to shrink on the x-ray right away.",
            9: "Procedure: Flexible bronchoscopy with implantation of bronchial valves.\nTarget: Left Upper Lobe.\nAction: Chartis confirmed no collateral flow. Four Zephyr valves were implanted to seal the LUL. \nResult: Target lobe obstructed. No adverse events."
        },
        4: { # Donald Peterson (Revision RUL - 31647, 31648)
            1: "Indication: Migrated valve RB2, incomplete occlusion.\nProcedure:\n- RB2 valve removed (forceps).\n- Debridement of granulation.\n- New 5.5mm Zephyr valve placed RB2.\n- RB1/RB3 valves checked, good.\nResult: RUL occluded.\nPlan: Discharge in 4hrs.",
            2: "OPERATIVE NOTE: Mr. Peterson presented for revision of RUL valves due to migration. Inspection revealed the RB2 valve distally migrated with paravalvular leak. This device was extracted using removal forceps. The airway was prepped, and a larger 5.5mm Zephyr valve was deployed proximally to secure the segment. The remaining valves in RB1 and RB3 were stable. Complete lobar occlusion was re-established.",
            3: "Coding:\n- 31648: Removal of bronchial valve (Migrated RB2 valve).\n- 31647: Insertion of bronchial valve (Replacement valve in RB2).\nRationale: Correction of complication (migration) requiring removal of hardware and placement of new hardware in the initial target lobe.",
            4: "Procedure: Valve Revision\nPatient: Don Peterson\nIssue: Valve in RB2 moved.\nSteps:\n1. Scope in.\n2. Pulled out the migrated valve (RB2).\n3. Cleaned up some tissue.\n4. Put in a bigger valve (5.5mm) in the same spot.\n5. Sealed up now.\nPlan: Home today.",
            5: "Don is back his valve moved in the right upper lobe. We went in and saw the RB2 valve way down there. Pulled it out with the grabbers. Put a new bigger one in its place. Now it looks tight no air getting through. The other valves looked fine. sending him home later.",
            6: "Bronchoscopic revision of right upper lobe valves. Indication: Valve migration RB2. The migrated valve was grasped and removed. The airway was inspected and cleared of mild granulation. A new 5.5mm Zephyr valve was deployed in the RB2 bronchus. Complete RUL occlusion was confirmed bronchoscopically.",
            7: "[Indication]\nValve migration, RUL.\n[Anesthesia]\nModerate Sedation.\n[Description]\nMigrated RB2 valve removed. New 5.5mm valve placed in RB2. RUL occlusion restored.\n[Plan]\nDischarge. Antibiotics x5 days.",
            8: "Mr. Peterson's follow-up CT showed one of his valves had slipped. We went back in and removed the loose valve from the anterior segment. We replaced it with a larger size to make sure it stays put this time. The other valves were fine, so we left them alone. The lobe is completely blocked off again.",
            9: "Procedure: Revision of endobronchial valves.\nProblem: Device migration.\nAction: The migrated valve in RB2 was extracted. A replacement Zephyr valve of larger dimension was implanted. \nOutcome: Restoration of lobar atelectasis."
        },
        5: { # Ilene Ortiez (Thoracoscopy - 32609)
            1: "Indication: Malignant effusion.\nProcedure: Medical Thoracoscopy (Left).\nFindings: Carcinomatosis, adhesions.\nAction: Adhesiolysis. 800cc fluid drained. 5 biopsies parietal pleura.\nClosure: 14Fr Pigtail placed.\nPlan: Await path.",
            2: "PROCEDURE: Left Medical Thoracoscopy (Pleuroscopy). The pleural space was accessed via the 8th intercostal space. Inspection revealed diffuse carcinomatosis and dense adhesions. Approximately 1275cc of serosanguinous fluid was evacuated. Forceps biopsies were obtained from the parietal pleura. A 14Fr chest tube was placed under direct vision. \nIMPRESSION: Malignant pleural effusion with extensive metastatic deposits.",
            3: "Code: 32609 (Thoracoscopy with biopsy of pleura).\nDetails: Rigid pleuroscopy performed. Trocar entry. Visualization of pleural cavity. Biopsy of parietal pleura nodules (x5). Drainage of effusion. Placement of indwelling chest catheter.",
            4: "Resident Note\nPatient: Ilene Ortiez\nProcedure: Pleuroscopy\nSteps:\n1. Local/Sedation.\n2. Trocar in left 8th rib space.\n3. Drained fluid.\n4. Saw nodules -> Biopsied x5.\n5. Put in Pigtail catheter.\nComplications: None.\nPath: Sent fluid and tissue.",
            5: "Doing a thoracoscopy on Ms Ortiez for her effusion. Put the port in the left side drained a liter of bloody fluid. The lung looked stuck down and there were bumps everywhere. Took 5 biopsies of the bumps. Put a pigtail chest tube in at the end. Biopsies went to pathology.",
            6: "Medical Thoracoscopy (Pleuroscopy), left side. Indication: Malignant pleural effusion. 1275cc fluid removed. Diffuse carcinomatosis noted. Multiple biopsies of parietal pleura performed. 14Fr Wayne pigtail catheter placed. Lung re-expansion confirmed on post-procedure CXR.",
            7: "[Indication]\nMalignant pleural effusion.\n[Anesthesia]\nModerate Sedation + Local.\n[Description]\nLeft thoracoscopy. 1275cc drained. Diffuse mets seen. Biopsies taken. Pigtail placed.\n[Plan]\nPathology pending. Suture removal 2 weeks.",
            8: "We performed a procedure to look inside Ms. Ortiez's chest cavity. We drained the fluid and saw extensive signs of cancer on the lining of the lung. We took several biopsy samples for the lab. We left a small chest tube in place to keep the fluid from building up again.",
            9: "Procedure: Medical Thoracoscopy with pleural sampling.\nFindings: Effusion and carcinomatosis.\nAction: Fluid was evacuated. Pleural nodules were sampled. A drainage catheter was inserted.\nResult: Samples submitted for analysis."
        },
        6: { # Tena Hughes (Stent Placement - 31636)
            1: "Indication: Extrinsic compression L Mainstem.\nProcedure: Rigid bronch (failed vent) -> ETT.\nFindings: 90% obstruction L Mainstem.\nAction: Aero stent 12x40mm placed. Dilated w/ balloon.\nResult: Airway diameter improved to 80%.\nPlan: Humidified O2. Nebs.",
            2: "OPERATIVE REPORT: The patient presented with critical left mainstem obstruction due to esophageal malignancy. Initial attempt with rigid bronchoscopy was complicated by ventilation leak, necessitating conversion to ETT. The lesion caused 95% stenosis of the LMS. A 12x40mm Aero hybrid stent was deployed over a guidewire under fluoroscopic guidance. Balloon dilation was performed to optimize stent expansion. Final inspection showed patent airway.",
            3: "Code: 31636 (Stent placement, initial bronchus).\nDevice: Aero Stent 12x40mm.\nLocation: Left Mainstem Bronchus.\nTechnique: Deployment over guidewire with fluoroscopy. Balloon dilation post-deployment. Note: Rigid bronchoscopy attempted but aborted; procedure completed via therapeutic flexible scope through ETT.",
            4: "Procedure: Airway Stenting\nPatient: Tena Hughes\nSteps:\n1. GA. Tried rigid, couldn't vent. Intubated.\n2. Scope passed lesion in LMS.\n3. Dropped guidewire.\n4. Deployed Aero stent (12x40).\n5. Ballooned it open.\n6. Airway open now.\nPlan: Saline nebs.",
            5: "Tena has a blocked airway from her cancer. We tried to use the big rigid scope but couldnt ventilate her so we put a regular tube in. Went down and saw the left main was almost shut. Put a wire down and slid an Aero stent over it. Popped it open with a balloon. Looks much better now airway is open. Keep her on humidified air.",
            6: "Flexible bronchoscopy with placement of tracheobronchial stent. Indication: Malignant extrinsic compression of left mainstem. Rigid bronchoscopy aborted due to leak. 12x40mm Aero stent deployed in LMS under fluoroscopic guidance. Post-dilation with CRE balloon performed. Airway patency restored.",
            7: "[Indication]\nEsophageal cancer, LMS obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronch failed. Converted to ETT. Aero stent 12x40mm placed in LMS. Balloon dilated. Patency improved.\n[Plan]\nSaline nebs. CXR.",
            8: "Ms. Hughes had a tumor pushing on her left main airway. We had to switch from the rigid scope to a breathing tube, but we successfully placed a stent to hold the airway open. We used a balloon to expand the stent fully. She is breathing much better now with the airway reopened.",
            9: "Procedure: Bronchoscopy with deployment of bronchial stent.\nIndication: Airway stenosis.\nAction: An Aero stent was positioned in the left mainstem bronchus. Balloon dilation was utilized to expand the prosthesis.\nResult: Relief of obstruction."
        },
        7: { # Robert Berg (Ablation - 31641)
            1: "Protocol: COMBO-ABLATE.\nTarget: LUL tumor 3.2cm.\nProcedure:\n1. Cryoablation (ProSense): 2 cycles. Ice ball 45mm.\n2. Microwave (Neuwave): 75W x 7min.\nResult: Ablation zone 52mm. No complications.\nPlan: Protocol follow-up.",
            2: "PROCEDURE: Bronchoscopic tumor ablation (multimodality). Under protocol CA-089, a 3.2cm LUL adenocarcinoma was targeted. First, cryoablation was performed (2 freeze-thaw cycles) achieving -158C. Following a defined interval, microwave ablation was delivered (75 Watts). Post-procedure imaging confirmed an ablation zone encompassing the target with margins. No adverse events occurred.",
            3: "Code: 31641 (Destruction of tumor, any method).\nTechnique: Combined Cryoablation and Microwave Ablation.\nTarget: Peripheral LUL tumor.\nGuidance: Fluoroscopy and r-EBUS.\nDetails: Cryo probe used to freeze tissue, followed by microwave antenna for thermal ablation. Research protocol.",
            4: "Research Procedure\nPatient: Robert Berg\nStudy: Combo-Ablate\nSteps:\n1. Navigated to LUL tumor.\n2. Did Cryo freeze (2 cycles).\n3. Waited 15 mins.\n4. Did Microwave burn (75W).\n5. Checked with EBUS.\nEverything went per protocol.",
            5: "Mr Berg is in the ablation study. We did the double whammy on his LUL tumor. First the cryo freeze for two cycles got a good ice ball. Then the microwave for 7 minutes to cook it. Looks like we got the whole thing plus margin. No bleeding no pneumo. He is doing fine.",
            6: "Bronchoscopic destruction of tumor. Protocol CA-089. LUL tumor 3.2cm. Sequential Cryoablation (ProSense) and Microwave Ablation (Neuwave) performed. Total ablation zone estimated 52mm. Tissue samples obtained pre/post. Patient tolerated well.",
            7: "[Indication]\nLUL Adenocarcinoma, Research Protocol.\n[Anesthesia]\nModerate Sedation.\n[Description]\nCryoablation x2 cycles. Microwave Ablation 75W. Target ablated with margins.\n[Plan]\nCT follow-up per protocol.",
            8: "Mr. Berg is participating in a study for his lung tumor. We treated the tumor in his left upper lobe using two methods: freezing it first with a cryo probe, and then heating it with microwaves. The combination created a large treatment zone that covered the whole tumor. He handled the procedure very well.",
            9: "Procedure: Bronchoscopy with tumor destruction.\nMethod: Sequential cryotherapy and thermal ablation.\nTarget: Left Upper Lobe lesion.\nAction: The lesion was frozen and subsequently heated to achieve necrosis.\nResult: Satisfactory ablation zone."
        },
        8: { # Tyler Benfield (Stent Removal - 31635)
            1: "Indication: Stent removal.\nProcedure: Rigid bronch -> Stent removal.\nFindings: Y-stent removed en-bloc. Granulation tissue.\nComplication: Laryngospasm post-extubation, re-intubated, resolved.\nPlan: ICU obs.",
            2: "OPERATIVE REPORT: The patient presented for removal of a tracheal Y-stent. A rigid tracheoscope was utilized. The stent was grasped with rigid forceps and extracted en-bloc. Inspection revealed friable mucosa but patent airways. A retained stent fragment in the left mainstem was removed with flexible forceps. Post-procedure course was complicated by severe laryngospasm requiring temporary re-intubation.",
            3: "Code: 31635 (Removal of foreign body/stent).\nTechnique: Rigid Bronchoscopy.\nDetails: Tracheal stent identified and removed intact. Fragment in LMS removed. \nComplication: Post-op Laryngospasm managed by anesthesia.",
            4: "Procedure: Stent Removal\nPatient: Tyler Benfield\nSteps:\n1. Rigid scope in.\n2. Grabbed stent, twisted, pulled it out.\n3. Found a piece left in the LMS, got that too.\n4. Patient had laryngospasm after, had to re-intubate briefly.\n5. Stable now.",
            5: "Tyler is here to get his stent out. We used the rigid scope. Grabbed the Y stent and pulled the whole thing out. There was a little piece broken off in the left side we got that too. He had a spasm when we woke him up had to put the tube back in for a sec but he is okay now. Sending to PACU.",
            6: "Rigid bronchoscopy with removal of tracheal stent. Indication: Resolved mediastinal mass. 12mm rigid scope used. Stent removed en-bloc. Residual fragment in LMS removed. Mucosa friable but patent. Post-procedure laryngospasm required brief re-intubation.",
            7: "[Indication]\nStent removal.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronch. Y-stent removed. Fragment in LMS removed. Airway patent.\n[Complications]\nLaryngospasm, re-intubated.\n[Plan]\nPACU/ICU.",
            8: "We brought Mr. Benfield in to remove his airway stent since his mass has shrunk. We used a rigid tube to pull the stent out in one piece. We also found and removed a small broken piece. He had some trouble breathing right after the tube came out due to a spasm, so we had to help him breathe for a few minutes, but he recovered well.",
            9: "Procedure: Rigid bronchoscopy with extraction of foreign body.\nObject: Tracheal Y-stent.\nAction: The prosthesis was withdrawn en-bloc. A residual fragment was retrieved.\nAdverse Event: Laryngospasm necessitating airway management."
        },
        9: { # Andrew Thompson (EBUS - 31653)
            1: "Indication: LAD.\nProcedure: EBUS-TBNA.\nStations: 4R, 4L, 7, 11R.\nROSE: Granulomas (Sarcoid).\nPlan: Path pending.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration. Systematic staging of the mediastinum was performed. Lymph node stations 4R, 4L, 7, and 11R were visualized and sampled. Rapid On-Site Evaluation (ROSE) demonstrated non-necrotizing granulomatous inflammation consistent with sarcoidosis across multiple stations. Specimens submitted for flow cytometry and microbiology.",
            3: "Code: 31653 (EBUS sampling 3 or more stations).\nStations Sampled: 4R, 4L, 7, 11R (4 stations).\nPathology: Granulomas.\nJustification: Evaluation of mediastinal lymphadenopathy.",
            4: "Procedure: EBUS\nPatient: Andrew Thompson\nStations:\n- 4R: 4 passes\n- 4L: 4 passes\n- 7: 4 passes\n- 11R: 3 passes\nROSE says Sarcoid. \nNo complications.",
            5: "Did an EBUS on Andrew today for the lymph nodes. Poked 4R 4L 7 and 11R. The pathologist in the room said it looks like sarcoid lots of granulomas. Sent everything for culture too just in case. Patient went home fine.",
            6: "EBUS-TBNA performed for mediastinal lymphadenopathy. Stations 4R, 4L, 7, and 11R sampled. ROSE interpretation: Non-necrotizing granulomas. Samples sent for final pathology and culture. No complications.",
            7: "[Indication]\nLymphadenopathy, R/O Sarcoid.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA stations 4R, 4L, 7, 11R. ROSE: Granulomas.\n[Plan]\nDischarge. Follow up path.",
            8: "We performed an ultrasound bronchoscopy to sample the swollen lymph nodes in Mr. Thompson's chest. We took samples from four different areas. The preliminary results strongly suggest sarcoidosis, which is what we suspected. We will wait for the final report to confirm.",
            9: "Procedure: Endobronchial ultrasound with needle aspiration.\nTarget: Mediastinal lymph nodes.\nAction: Stations 4R, 4L, 7, and 11R were sampled.\nResult: Cytology suggests granulomatous disease."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency
    # Indices 0-9 corresponding to the notes in the source file
    return [
        {"idx": 0, "orig_name": "Patricia Thompson", "orig_age": 72, "names": ["Mary Jones", "Linda Williams", "Barbara Brown", "Susan Miller", "Margaret Davis", "Dorothy Garcia", "Lisa Rodriguez", "Nancy Wilson", "Betty Martinez"]},
        {"idx": 1, "orig_name": "Sharon Kim", "orig_age": 69, "names": ["Helen Anderson", "Sandra Taylor", "Donna Thomas", "Carol Hernandez", "Ruth Moore", "Sharon Martin", "Michelle Jackson", "Laura Thompson", "Sarah White"]},
        {"idx": 2, "orig_name": "Chloe Whitford", "orig_age": 65, "names": ["Kimberly Lopez", "Deborah Lee", "Jessica Gonzalez", "Shirley Harris", "Cynthia Clark", "Angela Lewis", "Melissa Robinson", "Brenda Walker", "Amy Perez"]},
        {"idx": 3, "orig_name": "William Anderson", "orig_age": 68, "names": ["James Hall", "John Young", "Robert Allen", "Michael Sanchez", "William Wright", "David King", "Richard Scott", "Charles Green", "Joseph Baker"]},
        {"idx": 4, "orig_name": "Donald Peterson", "orig_age": 67, "names": ["Thomas Adams", "Christopher Nelson", "Daniel Hill", "Paul Ramirez", "Mark Campbell", "Donald Mitchell", "George Roberts", "Kenneth Carter", "Steven Phillips"]},
        {"idx": 5, "orig_name": "Ilene Ortiez", "orig_age": 65, "names": ["Anna Evans", "Rebecca Turner", "Virginia Torres", "Kathleen Parker", "Pamela Collins", "Martha Edwards", "Debra Stewart", "Amanda Flores", "Stephanie Morris"]},
        {"idx": 6, "orig_name": "Tena Hughes", "orig_age": 65, "names": ["Carolyn Nguyen", "Christine Murphy", "Marie Rivera", "Janet Cook", "Catherine Rogers", "Frances Morgan", "Ann Peterson", "Joyce Cooper", "Diane Reed"]},
        {"idx": 7, "orig_name": "Robert Berg", "orig_age": 71, "names": ["Edward Bailey", "Brian Bell", "Ronald Gomez", "Anthony Kelly", "Kevin Howard", "Jason Ward", "Matthew Cox", "Gary Diaz", "Timothy Richardson"]},
        {"idx": 8, "orig_name": "Tyler Benfield", "orig_age": 65, "names": ["Jeffrey Wood", "Frank Watson", "Scott Brooks", "Eric Bennett", "Stephen Gray", "Andrew James", "Raymond Reyes", "Gregory Cruz", "Joshua Hughes"]},
        {"idx": 9, "orig_name": "Andrew Thompson", "orig_age": 61, "names": ["Jerry Price", "Dennis Myers", "Walter Long", "Patrick Foster", "Peter Sanders", "Harold Ross", "Douglas Morales", "Henry Powell", "Carl Sullivan"]}
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
    output_filename = output_dir / "synthetic_notes_part_011.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()