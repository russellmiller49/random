import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_019.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Variations for the 10 notes in Part 019
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Charlene King (Diagnostic Bronch: BAL + TBBx)
            1: "Indication: Suspected sarcoidosis.\nProcedure: Bronchoscopy with BAL and TBBx.\nActions:\n- Scope inserted.\n- Inspection: Cobblestoning noted.\n- BAL: Right Middle Lobe.\n- Biopsy: 6 samples, RLL medial basal segment (forceps).\nComplications: None. No pneumothorax.",
            2: "PROCEDURE NOTE: The patient, a 48-year-old female presenting with bilateral hilar lymphadenopathy, underwent flexible fiberoptic bronchoscopy. Under moderate sedation, the tracheobronchial tree was visualized, revealing diffuse mucosal nodularity consistent with a granulomatous process. A bronchoalveolar lavage (BAL) was performed in the right middle lobe. Subsequently, fluoroscopically guided transbronchial forceps biopsies were obtained from the right lower lobe medial basal segment to secure a histological diagnosis. The patient tolerated the procedure without adverse events.",
            3: "CPT Coding Summary:\n1. 31624: Bronchoscopy with bronchoalveolar lavage (BAL) performed in the Right Middle Lobe.\n2. 31628: Bronchoscopy with transbronchial lung biopsy (TBBx), performed in a separate lobe (Right Lower Lobe). Fluoroscopic guidance utilized for safety. Six specimens obtained.\nMedical Necessity: Evaluation of pulmonary nodules and adenopathy (Sarcoidosis).",
            4: "Procedure Note\nPatient: Ms. King\nAttending: Dr. Allen\nSteps:\n1. Moderate sedation administered.\n2. Airway inspected; cobblestoning seen.\n3. BAL performed in RML.\n4. Transbronchial biopsies taken from RLL (medial basal) under fluoro.\n5. Hemostasis achieved.\n6. Post-op CXR negative.",
            5: "diag bronch for charlene king she has hilar adenopathy so we looked for sarcoid. sedation was midaz and fent. airways looked bumpy cobblestone pattern. did a wash in the rml and then took biopsies from the rll medial basal segment using the forceps. no bleeding really. xray showed no lung collapse she went home after.",
            6: "Flexible bronchoscopy with BAL and transbronchial biopsies (forceps) for suspected sarcoidosis was performed. Patient is a 48-year-old female with bilateral hilar adenopathy. Findings included cobblestoning and mild nodularity at segmental bronchi. BAL was performed in the right middle lobe. Six fluoroscopy-guided transbronchial biopsies were obtained from the right lower lobe medial basal segment. No significant bleeding occurred. Postprocedure CXR was negative for pneumothorax. Discharged home.",
            7: "[Indication]\nSuspected sarcoidosis, bilateral hilar adenopathy.\n[Anesthesia]\nModerate sedation (midazolam/fentanyl).\n[Description]\nCobblestoning observed. BAL performed in Right Middle Lobe. Transbronchial biopsies (x6) taken from Right Lower Lobe medial basal segment with fluoroscopy.\n[Plan]\nDischarge home. Follow up in clinic.",
            8: "Ms. King arrived for a diagnostic bronchoscopy to investigate her hilar adenopathy. We used moderate sedation to ensure her comfort. Upon entering the airways, we noticed cobblestoning, which is often a sign of sarcoidosis. We washed the right middle lobe to collect cells and then moved to the right lower lobe to take six small tissue samples using forceps under X-ray guidance. She did very well, had no bleeding, and her chest X-ray afterwards was clear.",
            9: "Procedure: Flexible bronchoscopy with lavage and transbronchial sampling.\nSubject: Female with pulmonary nodules.\nFindings: Mucosal nodularity.\nTechnique: Lavage was executed in the right middle lobe. Six transbronchial specimens were harvested from the right lower lobe medial basal segment utilizing fluoroscopy. \nOutcome: No hemorrhage or pneumothorax."
        },
        1: { # Anthony Rogers (ICU Bronch: BAL + Mucus Plug)
            1: "Indication: Lobar collapse, hypoxemia.\nSetting: MICU, intubated.\nFindings: RLL basal bronchi obstructed by mucus.\nAction: Aggressive BAL and suction in RLL.\nResult: Plugs removed, airways patent.\nComplication: Transient desat, resolved.",
            2: "OPERATIVE NARRATIVE: The patient, currently mechanically ventilated in the MICU, developed acute right lower lobe atelectasis. Bedside flexible bronchoscopy was initiated to restore airway patency. Visualization confirmed complete obstruction of the RLL basal segments by tenacious secretions. Therapeutic bronchial lavage and suctioning were vigorously applied, resulting in the successful extraction of significant mucus plugs and restoration of lobar aeration.",
            3: "Code Selection: 31624 (Bronchoscopy with bronchoalveolar lavage).\nRationale: Procedure performed in ICU setting for therapeutic purpose (removal of mucus plugs causing lobar collapse). Saline lavage was integral to clearing the inspissated secretions in the Right Lower Lobe. No biopsies taken.",
            4: "Resident Procedure Note\nPatient: Anthony Rogers (ICU)\nIndication: RLL collapse.\nProcedure:\n1. Time out.\n2. Scope passed via ETT.\n3. Found thick mucus plugs in RLL.\n4. Performed BAL and suctioned out plugs.\n5. Re-expanded lung.\nStatus: Stable, sat improved.",
            5: "icu bronch for mr rogers he had a collapsed lung on the xray. tube size 8. went down there and saw a lot of thick mucus blocking the right lower lobe. washed it out with saline and sucked it all up. sat dropped a bit to 84 but came back up. lung should be open now kept him on the vent.",
            6: "Flexible bronchoscopy with BAL and mucus plug removal performed at ICU bedside. Patient is a 68-year-old male intubated with lobar collapse. Thick mucus plugs obstructing right lower lobe basal bronchi were identified. Aggressive saline lavage, suctioning, and BAL were performed in RLL. Plugs were removed and airways cleared. Transient desaturation to 84% occurred during lavage, resolved with recruitment. Patient remained intubated.",
            7: "[Indication]\nRLL collapse, hypoxemic respiratory failure.\n[Anesthesia]\nDeep sedation (Propofol/Fentanyl) in ICU.\n[Description]\nMucus plugs identified in RLL basal segments. Therapeutic BAL and suction performed. Airways cleared.\n[Plan]\nContinue mechanical ventilation. Repeat CXR.",
            8: "Mr. Rogers was struggling with oxygenation in the ICU due to a collapsed right lower lobe. We performed a bedside bronchoscopy and found thick mucus plugging up the airways. We used saline lavage to break up the mucus and suctioned it out, clearing the blockage. His oxygen levels dipped briefly during the washing but recovered quickly once the airways were open.",
            9: "Procedure: Flexible bronchoscopy with lavage and secretion clearance.\nContext: ICU patient with atelectasis.\nFindings: Inspissated mucus obstructing RLL.\nIntervention: Vigorous lavage and aspiration performed. Obstructions eradicated.\nResult: Airways patent."
        },
        2: { # Jennifer Adams (Cryobiopsy + REBUS)
            1: "Indication: Fibrotic ILD.\nAnesthesia: General, 8.5 ETT.\nGuidance: Radial EBUS (parenchymal view).\nAction: 3 cryobiopsies (1.9mm probe) + 1 forceps biopsy from LLL basal segment.\nSafety: Prophylactic bronchial blocker used.\nResult: Mild bleeding controlled. No pneumo.",
            2: "PROCEDURE: The patient underwent bronchoscopic evaluation for interstitial lung disease. Following intubation, the bronchoscope was navigated to the left lower lobe. Radial endobronchial ultrasound (R-EBUS) was utilized to select a biopsy site free of major vascular structures. A 1.9 mm cryoprobe was employed to obtain three transbronchial cryobiopsies, supplemented by one standard forceps biopsy. A bronchial blocker was deployed for prophylactic hemorrhage control.",
            3: "Billing: 31628 (Transbronchial lung biopsy - Forceps/Cryo distinct from aspiration), 31654 (Radial EBUS guidance).\nNote: 31645 (Therapeutic aspiration) is NOT reported as removal of blood/secretions is incidental. 31628 covers the biopsy work. Radial EBUS (31654) documents the search for peripheral lesions/safe sites.",
            4: "Procedure: Cryobiopsy ILD\nPatient: Jennifer Adams, 56F\nSteps:\n1. GA, 8.5 ETT.\n2. Scope to LLL.\n3. Radial EBUS to clear site.\n4. Freezing: 3 passes with cryoprobe.\n5. Forceps: 1 pass.\n6. Balloon up for bleeding control.\nPlan: Admit for obs.",
            5: "Jennifer needs a diagnosis for her fibrosis so we did the cryo biopsy today. put her to sleep with a big tube 8.5. went to the left lower lobe used the radial ebus to make sure no vessels were there. took three freeze biopsies and one regular one. blocked the airway with a balloon for bleeding which was mild. no pneumothorax on the xray sending her to the floor.",
            6: "Bronchoscopic cryobiopsy for fibrotic ILD. Patient is a 56-year-old female with progressive fibrotic interstitial lung disease. General anesthesia with 8.5 ETT was used. Bronchoscope advanced to left lower lobe basal segments. Radial EBUS used to identify parenchymal sites distant from large vessels. Three cryobiopsies obtained using 1.9 mm cryoprobe and one standard forceps biopsy. Bronchial blocker placed prophylactically. Mild bleeding controlled with blocker inflation and iced saline.",
            7: "[Indication]\nFibrotic ILD, etiology unclear.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nLLL basal segment selected. Radial EBUS guidance used. 3 cryobiopsies + 1 forceps biopsy taken. Bronchial blocker used for hemostasis.\n[Plan]\nAdmit overnight. Monitor for pneumothorax.",
            8: "We performed a cryobiopsy on Ms. Adams today to figure out the cause of her lung fibrosis. Under general anesthesia, we navigated to the left lower lobe. We used ultrasound to check the area first, then used a freezing probe to grab three distinct tissue samples, plus one with standard forceps. We used a balloon to stop a little bit of bleeding, and the post-procedure X-ray showed her lungs were still fully inflated.",
            9: "Procedure: Transbronchial cryosampling for ILD.\nMethod: The scope was guided to the LLL. Radial EBUS verified a safe parenchymal site. Three cryosamples and one forceps sample were extracted. A bronchial blocker was utilized to manage mild hemorrhage.\nDisposition: Admitted for monitoring."
        },
        3: { # Kevin White (Robotic RFA)
            1: "Indication: 10mm RLL met.\nPlatform: Ion Robotic.\nGuidance: Radial EBUS + Cone Beam CT (Tool-in-lesion).\nAction: RF Ablation (40W, 480s, 85C).\nResult: Ablation zone confirmed on CBCT (5mm margin).\nComplication: Minor hemorrhage, stable.",
            2: "OPERATIVE REPORT: The patient presented for focal therapy of an oligometastatic RLL lesion. The Ion robotic platform facilitated navigation to the lateral basal segment. Target confirmation was achieved via concentric radial EBUS view and Cone-Beam CT (CBCT) verification of tool-in-lesion. Radiofrequency ablation was delivered via catheter at 40 Watts for 480 seconds. Post-ablation CBCT demonstrated a satisfactory ablation zone encompassing the tumor with margins.",
            3: "Coding: 31641 (Destruction of tumor, bronchoscopic), +31627 (Navigational bronchoscopy), +31654 (Radial EBUS).\nRationale: Primary therapeutic intent was destruction (RFA). Navigation and REBUS used for localization. CBCT (76000/77002) is distinct but noted here for procedural completeness.",
            4: "Robotic Bronch RFA\nPatient: Kevin White\nTarget: RLL nodule\nSteps:\n1. Ion robot registration (CT-to-body).\n2. Navigated to RLL.\n3. Confirmed with REBUS and Spin (CBCT).\n4. RFA catheter in. Burned at 40W for 8 mins.\n5. Re-spun. Good margins.\n6. Minor bleeding.\nPlan: Admit.",
            5: "Kevin has a met in the RLL we treated it with the robot today. Ion system worked well registration was 2mm. Found it with the radial probe and the cone beam ct. Cooked it with the RF catheter 40 watts for almost 10 minutes. Got a good burn zone on the scan after. Little bit of bleeding but stopped on its own. Admitting to telemetry.",
            6: "Robotic navigational bronchoscopy with RF ablation of RLL metastasis. Patient is a 63-year-old male with oligometastatic colorectal cancer. Ion robotic system used to access RLL lateral basal segment. Radial EBUS confirmed solid lesion, cone-beam CT verified tool-in-lesion. RF ablation catheter advanced; ablation performed at 40 W for 480 seconds. Postablation CBCT showed ablation zone with margin. Small perilesional hemorrhage occurred, hemodynamically stable.",
            7: "[Indication]\nOligometastatic colorectal cancer, RLL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon Robot navigation to RLL. REBUS/CBCT confirmation. RF Ablation (40W/480s). Margin confirmed.\n[Plan]\nAdmit to telemetry. CT in 3 months.",
            8: "Mr. White underwent a robotic procedure to treat a tumor in his right lower lung. We used the Ion robot to steer a catheter directly to the spot, confirming the location with both ultrasound and a CT scan right in the room. We then used radiofrequency energy to heat and destroy the tumor. The final scan showed we covered the whole area well. There was a tiny bit of bleeding, but he remained stable.",
            9: "Procedure: Robotic navigational bronchoscopy with thermal destruction of RLL metastasis.\nTechnique: Navigation via Ion system. Confirmation via Radial EBUS and CBCT. \nIntervention: RF energy applied to the lesion. \nOutcome: Tumor ablated with appropriate margins. Minor perilesional hemorrhage noted."
        },
        4: { # Teresa Murphy (MWA + Chest Tube)
            1: "Indication: LUL NSCLC (nonsurgical).\nNav: superDimension + REBUS + CBCT.\nAction: MWA (Emprint, 65W, 360s).\nComplication: Pneumothorax.\nIntervention: 10Fr pigtail catheter placed under fluoro.\nPlan: Admit.",
            2: "PROCEDURE: Electromagnetic navigation bronchoscopy (superDimension) was employed to access a peripheral LUL nodule. Localization was verified with radial EBUS and cone-beam CT. Microwave ablation was performed using the Emprint system (65W, 360s). Post-procedural imaging revealed a left apical pneumothorax. A 10 French pigtail thoracostomy tube was inserted using fluoroscopic guidance without difficulty.",
            3: "Codes: 31641 (Bronchial tumor destruction), 31627 (Navigational bronchoscopy), 31654 (REBUS), 32557 (Pleural drainage with image guidance).\nJustification: MWA constitutes tumor destruction. Navigation and REBUS were utilized. The pneumothorax required a separate procedure (chest tube) involving imaging guidance.",
            4: "Procedure: EMN Bronch + MWA + Chest Tube\nPatient: Teresa Murphy\nSteps:\n1. Navigated to LUL nodule with superDimension.\n2. Confirmed with REBUS/CBCT.\n3. Microwave ablation done.\n4. Patient developed pneumothorax.\n5. Placed pigtail chest tube.\nPlan: Admit, watch chest tube.",
            5: "Teresa is here for ablation of that LUL spot. Used the superdimension and the cone beam to find it. Microwave antenna went in 65 watts for 6 minutes. She coughed up a little blood and then we saw a pneumo on the scan. Had to put in a pigtail catheter 10 french. She is going to the floor for monitoring.",
            6: "EMN-guided microwave ablation of left upper lobe peripheral nodule. Patient is a 60-year-old female with small presumed primary NSCLC. superDimension EMN platform used to access 14 mm LUL anterior segment nodule. Radial EBUS showed eccentric view; cone-beam CT confirmed antenna in lesion. Emprint microwave antenna delivered; ablation performed. Mild hemoptysis and small left apical pneumothorax requiring 10 Fr pigtail catheter occurred. Admitted to monitored bed.",
            7: "[Indication]\nLUL NSCLC, nonsurgical candidate.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LUL. Confirmed position. MWA performed (65W). Complicated by pneumothorax. 10Fr pigtail placed.\n[Plan]\nAdmit. Monitor chest tube.",
            8: "We treated Ms. Murphy's lung nodule using microwave energy today. We guided the catheter to the left upper lobe using the navigation system and confirmed it with a CT scan. The ablation went well, but she developed a small air leak (pneumothorax) afterwards. We placed a small tube in her chest to drain the air, and she is stable and being admitted for observation.",
            9: "Procedure: EMN-guided microwave destruction of LUL nodule.\nDetails: The lesion was accessed via the superDimension platform. Ablation was executed at 65W. \nAdverse Event: Pneumothorax ensued.\nResolution: A pigtail catheter was inserted under imaging guidance. The patient was admitted."
        },
        5: { # Brian Edwards (Cryoablation)
            1: "Indication: RUL NSCLC (high risk).\nSystem: Monarch Robotic.\nGuidance: REBUS + CBCT.\nAction: Cryoablation (2.4mm probe, 2 freeze-thaw cycles, 360s each).\nResult: Ice ball visualized on CBCT.\nComplication: Mild hemoptysis, self-limited.",
            2: "OPERATIVE NOTE: The patient underwent robotic-assisted bronchoscopic cryoablation. The Monarch system was utilized to navigate to the subpleural RUL apical lesion. Positional confirmation was established via radial EBUS and Cone-Beam CT. A flexible cryoprobe was introduced, and two freeze-thaw cycles were completed. Intraprocedural CBCT confirmed the formation of an ice ball encompassing the target volume.",
            3: "Codes: 31641 (Tumor destruction), 31627 (Navigational bronchoscopy), 31654 (REBUS).\nNote: Cryoablation is coded as destruction of tumor (31641). Robotic navigation (Monarch) supports 31627. REBUS supports 31654. No pleural intervention required.",
            4: "Procedure: Robotic Cryoablation\nPatient: Brian Edwards\nSteps:\n1. Monarch robot to RUL.\n2. Verified with EBUS/CT.\n3. Used cryoprobe to freeze tumor x2 cycles.\n4. Saw ice ball on scan.\n5. Little bit of blood, stopped on its own.\nPlan: Admit overnight.",
            5: "Brian has severe copd so we did cryoablation on his cancer. used the monarch robot found the spot in the RUL. put the cryo probe in and froze it twice for 6 minutes each time. saw the ice ball on the ct spin. he bled a little but it stopped. sending him to the floor.",
            6: "Robotic navigational bronchoscopy with cryoablation of subpleural RUL lesion. Patient is a 71-year-old male with small peripheral NSCLC. Monarch robotic system used to reach 12 mm RUL apical segment lesion. Radial EBUS confirmed lesion; CBCT demonstrated tip within lesion. 2.4 mm cryoprobe advanced; two freeze-thaw cycles performed. Ice ball seen on CBCT. Mild transient hemoptysis occurred; no pneumothorax. Admitted overnight.",
            7: "[Indication]\nSmall NSCLC, severe COPD.\n[Anesthesia]\nGeneral.\n[Description]\nMonarch robot to RUL. Cryoablation performed (2 cycles). Ice ball confirmed on imaging. Hemostasis achieved.\n[Plan]\nAdmit. CT f/u 3 months.",
            8: "Mr. Edwards had a robotic procedure to freeze a small tumor in his right lung. Because of his COPD, this was safer than surgery. We used the robot to get there, checked our spot with ultrasound, and then froze the tumor twice to make sure it was destroyed. We could actually see the ice ball on the scanner. He had a tiny bit of coughing up blood, but it stopped quickly.",
            9: "Procedure: Robotic navigational bronchoscopy with cryodestruction.\nTarget: RUL subpleural lesion.\nTechnique: Monarch system navigation. Cryoprobe application (2 cycles). \nVerification: Ice ball visualized via CBCT. \nOutcome: Lesion ablated. Transient hemoptysis resolved."
        },
        6: { # James Carter (EBUS 3 stations)
            1: "Indication: Staging RUL mass.\nProcedure: EBUS-TBNA.\nStations: 4R, 7, 11R (3 stations).\nSampling: 3 passes/station. 21G needle.\nROSE: 4R Malignant (NSCLC). 7/11R Benign.\nComplication: None.",
            2: "PROCEDURE: Linear endobronchial ultrasound (EBUS) was performed for mediastinal staging. The bronchoscope was advanced, and lymph node stations 4R, 7, and 11R were systematically identified and sampled using a 21-gauge aspiration needle. Rapid On-Site Evaluation (ROSE) confirmed malignancy at station 4R, consistent with non-small cell lung cancer, while stations 7 and 11R yielded benign lymphocytes.",
            3: "Billing Summary:\n- 31653: EBUS-TBNA 3+ stations (4R, 7, 11R sampled).\nNote: Do NOT bill 31652 separately; 31653 covers the entire procedure when 3 or more stations are sampled. No other interventions performed.",
            4: "EBUS Note\nPatient: James Carter\nIndication: RUL mass staging\nStations sampled: 4R, 7, 11R\nNeedle: 21G\nResults: 4R positive for cancer. Others neg.\nPlan: Oncology referral.",
            5: "James is here for staging of his RUL mass. We did the EBUS under GA. Poked nodes at 4R 7 and 11R. Used the 21 gauge needle. Pathologist said 4R looks like cancer. The others were just lymph cells. No bleeding no issues. Going home today.",
            6: "Flexible bronchoscopy with linear EBUS-TBNA. Patient is a 64-year-old male with a right upper lobe mass. Enlarged nodes visualized at stations 4R, 7, and 11R. Three passes obtained from each station using a 21G needle. ROSE showed malignant cells at 4R concerning for non-small cell lung cancer; stations 7 and 11R showed benign lymphocytes. Elastography used. No complications. Discharged home.",
            7: "[Indication]\nMediastinal staging, RUL mass.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA of stations 4R, 7, 11R. 3 passes each. ROSE positive at 4R.\n[Plan]\nOncology follow-up.",
            8: "We performed an EBUS procedure on Mr. Carter to stage his lung cancer. We sampled three different lymph node areas: the high right mediastinum, the subcarinal area, and the right hilar area. Unfortunately, the preliminary results show cancer in the 4R lymph node, but the other two spots looked clear. He recovered well and is going home.",
            9: "Procedure: Linear EBUS-TBNA.\nStations: 4R, 7, 11R.\nAction: Aspiration of three nodal stations.\nFindings: Malignancy detected at 4R. Other stations benign.\nDisposition: Discharged."
        },
        7: { # Maria Hernandez (EBUS 3 stations - LUL CA)
            1: "Indication: Staging LUL Adeno.\nProcedure: EBUS-TBNA.\nStations: 4L, 7, 11L (3 stations).\nNeedle: 22G.\nROSE: Lymphocytes present, no malignancy seen.\nDisposition: D/C home.",
            2: "PROCEDURE: The patient presented for staging of a left upper lobe adenocarcinoma. Linear EBUS was utilized to visualize and sample lymph nodes at stations 4L, 7, and 11L. A 22-gauge needle was employed for transbronchial needle aspiration. Rapid on-site evaluation demonstrated adequate lymphocytic cellularity in all samples without definitive evidence of metastatic disease.",
            3: "Code: 31653 (EBUS-TBNA 3 or more stations).\nStations sampled: 4L, 7, 11L.\nNote: All sampling performed during single session. Validates 31653. No add-on codes applicable.",
            4: "EBUS Staging\nPatient: Maria Hernandez\nDx: LUL Adeno\nStations: 4L, 7, 11L\nPasses: 3-4 per station.\nROSE: Neg for malignancy.\nPlan: Home, wait for final path.",
            5: "Maria has LUL cancer needs staging. We did EBUS with MAC anesthesia LMA. Sampled 4L 7 and 11L with the 22 needle. Cytology said just lymphocytes no cancer seen yet. She did fine no bleeding. Discharged.",
            6: "Flexible bronchoscopy with linear EBUS-TBNA under monitored anesthesia care. Patient is a 58-year-old female with LUL adenocarcinoma. Lymph nodes at stations 4L, 7, and 11L identified. A 22G needle was used for TBNA. Four passes were obtained from 7 and 11L, three from 4L. ROSE demonstrated abundant lymphocytes without definite malignant cells. No complications. Discharged home.",
            7: "[Indication]\nStaging LUL adenocarcinoma.\n[Anesthesia]\nMAC (LMA).\n[Description]\nEBUS-TBNA stations 4L, 7, 11L. 22G needle used. ROSE negative for malignancy.\n[Plan]\nDischarge. Oncology f/u.",
            8: "Ms. Hernandez came in for staging of her left lung cancer. Using the EBUS scope, we sampled lymph nodes in three areas: 4L, 7, and 11L. The preliminary check in the room didn't show any cancer in those nodes, which is a good sign, but we have to wait for the final results. She woke up quickly and went home.",
            9: "Procedure: Linear EBUS-TBNA.\nTarget: Stations 4L, 7, 11L.\nAction: Transbronchial needle aspiration performed at three distinct sites.\nFindings: Lymphocytic material obtained; preliminary negative for metastasis.\nDisposition: Discharged."
        },
        8: { # Robert Lee (EBUS 4 stations - SCLC)
            1: "Indication: Recurrent SCLC?\nProcedure: EBUS-TBNA.\nStations: 2R, 4R, 7, 10R (4 stations).\nROSE: Station 7 positive for Small Cell. Others neg.\nPlan: Oncology.",
            2: "PROCEDURE: The patient, with a history of small cell lung cancer, presented with mediastinal adenopathy. Systematic EBUS examination identified targetable nodes at stations 2R, 4R, 7, and 10R. TBNA was performed at all four stations using a 21-gauge needle. Cytopathology confirmed recurrent small cell carcinoma at station 7.",
            3: "Billing: 31653 (EBUS-TBNA 3+ stations).\nStations: 2R, 4R, 7, 10R.\nRationale: Sampling of 4 distinct mediastinal/hilar stations falls under the single comprehensive code 31653.",
            4: "EBUS Note\nPatient: Robert Lee\nQuery: Recurrent SCLC\nStations: 2R, 4R, 7, 10R\nROSE: Pos for SCLC at station 7.\nPlan: Admit to Onc.",
            5: "Robert is back with possible recurrence of small cell. Did EBUS in the OR. Sampled 2R 4R 7 and 10R. Station 7 came back positive for small cell on the rapid read. Others looked okay. Admitting him for chemo eval.",
            6: "Interventional Pulmonology Procedure Note. Procedures performed: Flexible bronchoscopy, Linear EBUS-TBNA. Patient is a 71-year-old male with suspected recurrent small cell lung cancer. Stations 2R, 4R, 7, and 10R identified. TBNA performed. ROSE showed malignant cells at 7 consistent with small cell carcinoma; other stations with lymphocytes. No complications. Admitted to oncology ward.",
            7: "[Indication]\nSuspected recurrent SCLC.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA of 4 stations (2R, 4R, 7, 10R). Recurrence confirmed at Station 7 via ROSE.\n[Plan]\nAdmit to Oncology.",
            8: "Mr. Lee underwent an EBUS procedure to check for recurring cancer. We sampled four different lymph node stations: 2R, 4R, 7, and 10R. The sample from station 7 unfortunately showed small cell cancer cells. We admitted him to the hospital to start planning his treatment with the oncology team.",
            9: "Procedure: Linear EBUS-TBNA.\nScope: Four nodal stations (2R, 4R, 7, 10R) were aspirated.\nDiagnosis: Recurrent small cell carcinoma identified at station 7.\nDisposition: Admitted."
        },
        9: { # Patricia Nguyen (Robotic Nav + REBUS + TBBx)
            1: "Indication: 18mm RLL nodule.\nNav: Ion Robotic + CT-body registration.\nGuidance: REBUS (concentric) + CBCT.\nSampling: TBNA (21G) + TBBx (x6) + Brush.\nROSE: Suspicious for NSCLC.\nResult: No pneumo.",
            2: "PROCEDURE: Robotic-assisted bronchoscopy was performed for a right lower lobe pulmonary nodule. The Ion system was utilized with successful registration. Radial EBUS confirmed a concentric solid lesion. Sampling was conducted via transbronchial needle aspiration, cytology brushing, and forceps biopsies under fluoroscopic and Cone-Beam CT guidance. Rapid on-site evaluation suggested non-small cell carcinoma.",
            3: "Codes: 31629 (TBNA), 31628 (TBBx), +31627 (Navigational bronchoscopy), +31654 (REBUS).\nRationale: TBNA performed (31629 is primary). TBBx performed in same lobe (31628). Navigation and REBUS used for localization. 31626 not used as 31629 takes precedence or specific biopsy codes used.",
            4: "Robotic Bronch\nPatient: Patricia Nguyen\nTarget: RLL superior segment\nSteps:\n1. Ion nav to target.\n2. REBUS confirmed.\n3. Needle aspirate (TBNA).\n4. Forceps biopsies x6.\n5. Brush x2.\nROSE: NSCLC.\nPlan: D/C, Onc referral.",
            5: "Patricia has a spot in the RLL used the ion robot to get there. Radial probe showed it nicely. Did a needle stick and then grabbed some biopsies with the forceps and a brush. Pathologist thinks its cancer. No bleeding or popped lung. She went home.",
            6: "Robotic-assisted navigational bronchoscopy with radial EBUS and transbronchial biopsies of a right lower lobe nodule. Patient is a 67-year-old female. Ion robotic bronchoscopy platform used. Radial EBUS: Concentric solid lesion pattern obtained. Sampling: Tool-in-lesion confirmed by cone-beam CT. Six transbronchial forceps biopsies, two brushings, and one 21G needle aspiration performed. ROSE suggestive of non-small cell carcinoma. Discharged.",
            7: "[Indication]\nRLL nodule, PET positive.\n[Anesthesia]\nGeneral.\n[Description]\nIon Robot nav to RLL. REBUS concentric view. TBNA, TBBx, Brush performed. ROSE positive for NSCLC.\n[Plan]\nDischarge. Staging follow-up.",
            8: "We used the robotic bronchoscope to biopsy a nodule in Ms. Nguyen's right lower lung. Once the robot guided us there, we used ultrasound to confirm we were in the right spot. We took samples using a needle, small forceps, and a brush. The preliminary results look like lung cancer. She tolerated the procedure well and went home.",
            9: "Procedure: Robotic navigational bronchoscopy with multimodal sampling.\nTarget: RLL peripheral nodule.\nTechnique: Navigation, Radial EBUS, CBCT.\nActions: Transbronchial needle aspiration and forceps biopsies executed.\nFindings: Malignancy suspected on ROSE.\nOutcome: No complications."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages
    # Correspond to the 10 notes in Part 019
    return [
        {"idx": 0, "orig_name": "Charlene King", "orig_age": 48, "names": ["Alice Brown", "Martha Jones", "Kelly Smith", "Diana Prince", "Carol Danvers", "Natasha Romanoff", "Wanda Maximoff", "Hope Van Dyne", "Jean Grey"]},
        {"idx": 1, "orig_name": "Anthony Rogers", "orig_age": 68, "names": ["Bill Smith", "Steve Rogers", "Tony Stark", "Bruce Banner", "Thor Odinson", "Clint Barton", "Sam Wilson", "Bucky Barnes", "Scott Lang"]},
        {"idx": 2, "orig_name": "Jennifer Adams", "orig_age": 56, "names": ["Pepper Potts", "Peggy Carter", "Sharon Carter", "Maria Hill", "Gamora", "Nebula", "Mantis", "Okoye", "Shuri"]},
        {"idx": 3, "orig_name": "Kevin White", "orig_age": 63, "names": ["Peter Parker", "Stephen Strange", "T'Challa", "Peter Quill", "Drax", "Rocket Raccoon", "Groot", "Nick Fury", "Phil Coulson"]},
        {"idx": 4, "orig_name": "Teresa Murphy", "orig_age": 60, "names": ["May Parker", "Betty Ross", "Jane Foster", "Darcy Lewis", "Sif", "Frigga", "Hela", "Valkyrie", "Carol Danvers"]},
        {"idx": 5, "orig_name": "Brian Edwards", "orig_age": 71, "names": ["Odin", "Heimdall", "Loki", "Thanos", "Erik Killmonger", "Ulysses Klaue", "Baron Zemo", "Red Skull", "Alexander Pierce"]},
        {"idx": 6, "orig_name": "James Carter", "orig_age": 64, "names": ["Happy Hogan", "Rhodey Rhodes", "Vision", "Pietro Maximoff", "Hank Pym", "Howard Stark", "Edwin Jarvis", "Yondu", "Kraglin"]},
        {"idx": 7, "orig_name": "Maria Hernandez", "orig_age": 58, "names": ["Janet Van Dyne", "Cassie Lang", "Monica Rambeau", "Kamala Khan", "Kate Bishop", "Yelena Belova", "Jennifer Walters", "Maya Lopez", "Riri Williams"]},
        {"idx": 8, "orig_name": "Robert Lee", "orig_age": 71, "names": ["Wong", "Mordo", "Ancient One", "Kaecilius", "Dormammu", "Ego", "Grandmaster", "Collector", "Korg"]},
        {"idx": 9, "orig_name": "Patricia Nguyen", "orig_age": 67, "names": ["Aunt May", "MJ", "Gwen Stacy", "Felicia Hardy", "Elektra", "Karen Page", "Jessica Jones", "Trish Walker", "Claire Temple"]}
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
            # Handle potential missing index in variations_text if data mismatch
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
                
                # Update the note text inside registry_entry if it exists (some formats duplicate it)
                if "note_text" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["note_text"] = variations_text[idx][style_num]

            
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
    output_filename = output_dir / "synthetic_blvr_notes_part_019.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()