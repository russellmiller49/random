import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_039.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Harold Kim (EBUS 4R, 7, 10R)
            1: "Indication: Staging NSCLC.\nProcedure: EBUS-TBNA.\nNodes sampled: 4R (11mm), 7 (14mm), 10R (7mm).\nFindings: 4R and 7 PET+ and ROSE+. 10R ROSE adequate.\nComp: None.\nPlan: Tumor board.",
            2: "OPERATIVE NARRATIVE: The patient, a 71-year-old male with non-small cell lung carcinoma, underwent endobronchial ultrasound-guided transbronchial needle aspiration for mediastinal staging. Under moderate sedation, the airway was examined. Systematic evaluation of the mediastinum was performed. Lymph node stations 4R, 7, and 10R were identified, measured, and sampled. Rapid On-Site Evaluation (ROSE) confirmed malignancy in the N2 stations (4R and 7). Station 10R demonstrated adequate lymphocytes. The procedure concluded without complication.",
            3: "Procedure: EBUS-TBNA (CPT 31653 - 3 stations).\nTechnique: Dedicated EBUS scope used. Stations sampled: 4R, 7, and 10R.\nTools: 22G needle.\nFindings:\n- 4R: 11mm, PET avid, malignant.\n- 7: 14mm, PET avid, malignant.\n- 10R: 7mm, benign.\nJustification: Evaluation of N2 vs N3 disease for surgical candidacy.",
            4: "Procedure Note\nPatient: Harold Kim\nResident: Dr. Smith\nSteps:\n1. Time out.\n2. Moderate sedation.\n3. EBUS scope inserted.\n4. Identified nodes 4R, 7, 10R.\n5. TBNA performed 4 passes 4R, 4 passes 7, 3 passes 10R.\n6. ROSE interpretation: N2 positive.\n7. Tolerated well.",
            5: "harold kim here for ebus staging he has nsclc 71 male. we used midazolam and fentanyl vitals good. looked at 4R 11mm and 7 which was 14mm both pet positive rose said cancer. also did 10r 7mm rose ok. systematic exam done took photos. n2 disease confirmed bilevel. present at tumor board likely chemo first thanks.",
            6: "S: 71M with NSCLC, needs mediastinal staging before resection O: EBUS performed under moderate sedation (midaz 3mg, fent 75mcg). Ramsay 3. Vitals stable, BP q5min, SpO2 96-99% on 2L NC. Stations: 4R 11mm (PET+) x4 passes ROSE+, 7 subcarinal 14mm (PET+) x4 ROSE+, 10R 7mm x3 ROSE adequate. Systematic N3-N2-N1 done. Photos all stations. A: N2 disease confirmed bilevel (4R, 7). Adequate molecular tissue. P: Present at tumor board. Likely neoadjuvant chemo. Name: Harold Kim | MRN GH-4829-P | DOB 04/12/1953 Complications: none",
            7: "[Indication]\nMediastinal staging for NSCLC.\n[Anesthesia]\nModerate sedation (Midazolam/Fentanyl).\n[Description]\nEBUS-TBNA performed. Stations 4R, 7, and 10R sampled. ROSE confirmed malignancy in 4R and 7. 10R was negative. All samples sent for permanent pathology.\n[Plan]\nOncology referral for neoadjuvant chemotherapy.",
            8: "Mr. Kim, a 71-year-old male with known NSCLC, presented for staging. We performed an EBUS under moderate sedation. We successfully visualized and sampled three specific lymph node stations: 4R, 7, and 10R. The rapid on-site evaluation was positive for malignancy in the mediastinal nodes 4R and 7, confirming N2 disease. The hilar node 10R was adequate but negative. He remained stable throughout.",
            9: "Subject: 71M with NSCLC, requires mediastinal evaluation. Observation: EBUS executed under moderate sedation. Vitals stable. Stations: 4R 11mm (PET+) x4 passes ROSE+, 7 subcarinal 14mm (PET+) x4 ROSE+, 10R 7mm x3 ROSE sufficient. Systematic N3-N2-N1 completed. Images of all stations secured. Assessment: N2 disease verified bilevel. Sufficient molecular tissue. Plan: Discuss at tumor board."
        },
        1: { # Sarah Miller (EBUS 4R, 7, 10R)
            1: "Proc: EBUS Staging.\nNodes: 4R (11mm), 7 (16mm), 10R (7mm).\nAction: TBNA x 3-4 passes each.\nResult: Malignant cells in 4R and 7. 10R benign.\nIssues: None.\nTime: 32 min.",
            2: "PROCEDURE PERFORMED: Endobronchial Ultrasound (EBUS) guided Transbronchial Needle Aspiration (TBNA).\nCLINICAL SUMMARY: Ms. Miller presented for staging of lung malignancy. Under moderate sedation, systematic ultrasonic interrogation of the mediastinum was conducted. Lymphadenopathy was noted in stations 4R and 7, correlating with PET avidity. Both were sampled and confirmed malignant on ROSE. Station 10R was also sampled for completeness and was negative.",
            3: "CPT 31653: EBUS-TBNA 3+ stations.\nTargeted Stations: 4R, 7, 10R.\nMedical Necessity: Pathologic staging of mediastinum.\nSpecifics:\n- 4R: 11mm, 4 passes.\n- 7: 16mm, 4 passes.\n- 10R: 7mm, 3 passes.\n- ROSE service utilized.\nOutcome: Confirmed N2 disease.",
            4: "Resident Procedure Note\nAttending: Dr. X\nPatient: Sarah Miller\nProcedure: EBUS TBNA\nTechnique: \n- Airway secured.\n- EBUS scope introduced.\n- Sampled 4R, 7, 10R.\n- ROSE confirmed cancer in 4R/7.\n- Photos taken.\nComplications: None.",
            5: "case 2024 0847 patient sarah miller ebus staging performed systematic check done. 4r was 11mm rose positive 7 was 16mm rose positive 10r 7mm rose negative but adequate. sedation was moderate ramsay 3 monitoring every 5 mins. no complications duration 32 mins n2 disease check.",
            6: "Case#: 2024-0847 | Pt: Sarah Miller | ID: HH-9482-L | DOB: 07/08/1959 EBUS Staging: Y | Systematic: Y | Photos: Y 4R: 11mm, 4x, ROSE+, PET+ 7: 16mm, 4x, ROSE+, PET+ 10R: 7mm, 3x, ROSE+, PET- Molecular: Y (from 4R) Adequacy: Y (all nodes) Sedation: Moderate | Ramsay: 3 | Monitoring: q5min Cx: None Duration: 32min N2 disease confirmed",
            7: "[Indication]\nStaging of lung cancer.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS scope passed. Stations 4R, 7, and 10R visualized and sampled via TBNA. Malignancy confirmed in 4R and 7 via ROSE.\n[Plan]\nOncology follow-up.",
            8: "Ms. Miller underwent EBUS staging today. We used a systematic approach to examine the lymph nodes. We found enlarged nodes at station 4R and 7, both of which were PET positive. We sampled these, as well as station 10R. The on-site pathologist confirmed cancer cells in the 4R and 7 samples, establishing N2 disease. The procedure took about 32 minutes and she tolerated it well.",
            9: "Case#: 2024-0847 | Pt: Sarah Miller. EBUS Evaluation: Y | Systematic: Y | Photos: Y. 4R: 11mm, 4x, ROSE+, PET+. 7: 16mm, 4x, ROSE+, PET+. 10R: 7mm, 3x, ROSE+, PET-. Molecular: Y (from 4R). Sufficiency: Y (all nodes). Sedation: Moderate | Ramsay: 3 | Monitoring: q5min. Adverse Events: None. Duration: 32min. N2 disease verified."
        },
        2: { # Susan M. O'Brien (Ablation RML)
            1: "Op: Bronchoscopic Microwave Ablation.\nTarget: 2.4cm RML nodule.\nNav: ENB + Radial EBUS.\nAblation: 65W for 6 min.\nPost-op: Necrosis visible on rEBUS. No pneumothorax.\nPlan: Admit obs.",
            2: "OPERATIVE REPORT: Ms. O'Brien, a 64-year-old female with significant comorbidities, underwent elective bronchoscopic microwave ablation for a biopsy-proven RML adenocarcinoma. Following general anesthesia, electromagnetic navigation and radial EBUS were utilized to localize the 2.4 cm lesion. A microwave antenna was advanced, and ablation was delivered at 65 watts for 6 minutes. Immediate post-ablation imaging confirmed a satisfactory ablation zone. The patient remained hemodynamically stable.",
            3: "Code: 31641 (Bronchoscopy with destruction of tumor).\nModality: Microwave Ablation.\nGuidance (Bundled): Electromagnetic Navigation (31627) + Radial EBUS (31654).\nTarget: Right Middle Lobe lateral segment.\nDetails: 65 Watts, 6 minutes.\nMedical Necessity: Patient is high surgical risk (Stage 4 CKD, CHF).",
            4: "Procedure: Navigational Bronchoscopy with Ablation\nPatient: Susan O'Brien\nSteps:\n1. GA/Intubation.\n2. ENB planning to RML nodule.\n3. Navigate to target. rEBUS confirms (24x21mm).\n4. CBCT confirmation.\n5. Insert microwave antenna.\n6. Ablate: 65W/6min.\n7. Check for pneumo (neg).\nPlan: Post-procedure CT.",
            5: "Susan OBrien here for the microwave ablation RML nodule. She has bad kidneys and heart so no surgery. We intubated her used the medtronic system to find the spot in the RML. Radial ebus looked good size 24mm. Put the antenna in burned it for 6 mins at 65 watts. Patient stable no pneumo on xray. Sending her to step down thanks.",
            6: "PATIENT: Susan M. O'Brien MRN: HUP-2025-7734 DOB: July 4, 1961 (64 years old) DATE: November 2, 2025 LOCATION: Hospital of the University of Pennsylvania, Philadelphia, PA PROCEDURALIST: Dr. Michael Steinberg, MD, FCCP ASSISTANT: Dr. Rachel Kim, DO (IP Fellow) INDICATION FOR PROCEDURE: Ms. O'Brien is a delightful 64-year-old former librarian who presents with right middle lobe peripheral nodule... [Rest of text follows without headers]",
            7: "[Indication]\n2.4cm RML Adenocarcinoma, non-surgical candidate.\n[Anesthesia]\nGeneral Anesthesia, 8.0 ETT.\n[Description]\nElectromagnetic navigation to RML. Radial EBUS confirmation. Microwave ablation performed (65W, 6 min). Ablation zone verified via rEBUS and CBCT.\n[Plan]\nAdmit to step-down. CXR in AM.",
            8: "We brought Ms. O'Brien back for ablation of her right middle lobe tumor. Given her heart and kidney issues, surgery wasn't an option. We used the navigation system to get right to the tumor and confirmed it with ultrasound. Then we inserted the microwave probe and treated the tumor for 6 minutes at 65 watts. Everything went smoothly, and the post-procedure scans showed we covered the tumor well.",
            9: "PATIENT: Susan M. O'Brien. INDICATION: Ms. O'Brien presents with right middle lobe peripheral nodule. PROCEDURE DESCRIPTION: Following induction, the therapeutic bronchoscope was introduced. Electromagnetic navigation was commenced. The guide sheath was steered to the target. Radial EBUS verified the lesion. Microwave ablation was initiated at 65 watts for 6 minutes. Post-ablation radial EBUS displayed a hyperechoic region replacing the tumor. Equipment was withdrawn sequentially."
        },
        3: { # Catherine Martinez (Nav LUL + Biopsy)
            1: "Indication: 23mm LUL nodule.\nProc: ENB + rEBUS + Biopsy.\nFindings: Concentric rEBUS view.\nSampling: TBNA x3, Forceps x4, Brush x2.\nComplications: Minimal bleeding, stopped spont.\nResult: No pneumothorax.",
            2: "PROCEDURE NOTE: Ms. Martinez underwent electromagnetic navigation bronchoscopy for a suspicious 23mm left upper lobe nodule. The lesion was localized using preoperative CT planning and verified intraoperatively with radial EBUS, demonstrating a solid, concentric pattern. Diagnostic sampling was performed via transbronchial needle aspiration, forceps biopsy, and cytological brushing. The patient tolerated the procedure well under moderate sedation.",
            3: "Billing: Bronchoscopy with Nav (31627) + rEBUS (31654) + TBNA (31629) + Biopsy (31628) + Brush (31623).\nTarget: LUL apical-posterior.\nMedical Necessity: Diagnosis of PET-avid nodule.\nSamples: 3 needle, 4 forceps, 2 brush.\nFluoro time: 5.1 min.",
            4: "Resident Note\nPatient: Catherine Martinez\nProcedure: ENB LUL\n1. Moderate sedation.\n2. Navigated to LUL apicoposterior.\n3. rEBUS confirmed lesion.\n4. Biopsies: Needle x3, Forceps x4, Brush x2.\n5. Minimal bleeding.\n6. CXR clear.",
            5: "73 year old female catherine martinez here for nav bronch on a LUL nodule 23mm. used midazolam and fentanyl. navigation worked well got the sheath out there. radial ebus showed the lesion solid. took 3 needle samples 4 forceps bites and 2 brushings. little bleeding stopped on its own. fluoroscopy used 5 mins. patient went home fine.",
            6: "This seventy-three year old female patient Catherine Martinez (medical record JJ-8374-Q, born September 8, 1951) presented for electromagnetic navigation bronchoscopy targeting a left upper lobe peripheral nodule measuring twenty-three millimeters in greatest dimension on computed tomography. The lesion demonstrated a positive bronchus sign and had a standardized uptake value of five point two on positron emission tomography imaging suggesting malignancy. She underwent moderate conscious sedation... [Rest of text]",
            7: "[Indication]\n23mm LUL nodule, PET avid.\n[Anesthesia]\nModerate sedation (Midazolam/Fentanyl).\n[Description]\nNavigation to LUL. rEBUS confirmed concentric view. TBNA x3, Forceps x4, Brush x2 performed. Minimal bleeding.\n[Plan]\nDischarge home. Follow pathology.",
            8: "Ms. Martinez came in for a biopsy of a spot in her left upper lung. We used the electromagnetic navigation system to guide our scope to the 23mm nodule. Once we were there, we used ultrasound to confirm we were right on target. We took several samples using a needle, forceps, and a brush to make sure we got enough tissue for diagnosis. She had a tiny bit of bleeding that stopped quickly, and her chest x-ray afterwards was clear.",
            9: "This seventy-three year old female patient Catherine Martinez presented for electromagnetic navigation bronchoscopy targeting a left upper lobe peripheral nodule. The electromagnetic navigation system was employed with successful registration. The guide sheath was steered to the left upper lobe apical-posterior segment. Sampling comprised three needle aspirations, four transbronchial forceps biopsies, and two brush cytology specimens. There was minimal hemorrhage after the forceps biopsies which resolved spontaneously."
        },
        4: { # Michael Foster (EBUS + LUL Biopsy)
            1: "Proc: EBUS + LUL EBBX.\nEBUS: 4R(11mm) ROSE+, 7(15mm) ROSE+, 10L(7mm) neg.\nLUL: Endobronchial lesion biopsy x6 + brush.\nHemostasis: Epi/Saline.\nImpression: Likely NSCLC N2.",
            2: "PROCEDURE RECORD: Mr. Foster presented for combined EBUS staging and biopsy of a Left Upper Lobe mass. Under moderate sedation, EBUS-TBNA was performed on stations 4R, 7, and 10L. Malignancy was confirmed on-site in 4R and 7. Subsequently, the bronchoscope was advanced to the LUL where an endobronchial lesion was identified and biopsied (forceps x6) and brushed. Hemostasis was achieved. Preliminary staging suggests N2 disease.",
            3: "CPT Codes: 31653 (EBUS 3 stations), 31625 (Bronchial biopsy), 31623 (Brush).\nEBUS: 4R, 7, 10L sampled.\nBiopsy: LUL endobronchial mass.\nRationale: Diagnosis and staging performed in same session.",
            4: "Resident Note\nPatient: Michael Foster\nProcedure: EBUS + Bronchoscopy\n- Sedation: Versed/Fentanyl.\n- EBUS: Sampled 4R, 7, 10L. 4R/7 positive.\n- Bronch: Saw mass in LUL.\n- Biopsied LUL mass x6 and brushed.\n- Bleeding controlled.\n- Plan: Oncology.",
            5: "michael foster note hard to read but looks like ebus plus lul mass biopsy. sedation used versed and fentanyl. ebus done on 4r station 7 and 10l. 4r and 7 were cancer on rose. 10l benign. then went to lul saw tumor inside airway took 6 biopsies and a brush. bleeding controlled with epi. likely nsclc with n2 nodes. tumor board next.",
            6: "[Transcribed from handwritten note - some words difficult to read] Pt: Michael ??? (looks like \"Foster\"?) MR#: JJ-9473 or JJ-8473 [unclear] DOB: 9/12/1960 Bronch + EBUS today for LUL mass + nodes Mod sed - versed 3mg, fent 100mcg Stayed comfortable, Ramsay ~3 VS stable throughout EBUS done: - 4R node ~11mm -> 4 passes, ROSE showed cancer cells, PET was positive - Station 7 ~15mm -> 4 passes, also malignant on ROSE, PET+ - 10L ~7mm -> 3 passes, benign [Drawing of mediastinal stations with arrows] Did systematic eval ... [Rest of text]",
            7: "[Indication]\nLUL mass and lymphadenopathy.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS-TBNA of 4R, 7, 10L. N2 (4R, 7) positive. Endobronchial biopsy and brushing of LUL mass performed.\n[Plan]\nPathology pending. Tumor board.",
            8: "We performed a bronchoscopy on Mr. Foster to check a mass in his left lung and his lymph nodes. We started with the lymph nodes using EBUS, sampling stations 4R, 7, and 10L. Unfortunately, the nodes at 4R and 7 looked like cancer. We then looked at the mass in the left upper lobe and took several biopsies and a brushing. There was some bleeding, but we stopped it with cold saline and epinephrine.",
            9: "[Transcribed] Pt: Michael ???. Bronch + EBUS today for LUL mass + nodes. EBUS executed: - 4R node ~11mm -> 4 passes, ROSE showed cancer cells. - Station 7 ~15mm -> 4 passes, also malignant. - 10L ~7mm -> 3 passes, benign. Also sampled LUL tumor - endobronch lesion. Obtained ~6 biopsies + brushings. Some hemorrhage but controlled. Path pending."
        },
        5: { # Christopher Lee (EBUS + Cryo LLL)
            1: "Indication: Adenopathy + LLL infiltrate.\nAnesthesia: GA, ETT.\nEBUS: 4R, 7, 11L. Granulomas on ROSE.\nCryo: LLL infiltrate x4 samples (6 sec freeze). Blocker used.\nComp: Moderate bleeding, controlled.\nPlan: Admit.",
            2: "OPERATIVE REPORT: Mr. Lee underwent diagnostic bronchoscopy for mediastinal adenopathy and an LLL infiltrate. Under general anesthesia, EBUS-TBNA was performed on stations 4R, 7, and 11L, revealing non-necrotizing granulomas. Attention was turned to the LLL parenchymal disease. Using a prophylactic bronchial blocker, transbronchial cryobiopsies (x4) were obtained. Hemostasis was achieved after blocker inflation. No pneumothorax noted.",
            3: "Billing: 31653 (EBUS 3 stations) + 31628 (Transbronchial lung biopsy - Cryo).\nEBUS: 4R, 7, 11L.\nTBLB: LLL x 4 samples.\nNote: Cryobiopsy coded as 31628 per current guidelines. 31624 not applicable as fluoroscopy guidance utilized/implied for parenchymal target.",
            4: "Procedure: EBUS + Cryobiopsy\nPatient: Christopher Lee\n1. GA with ETT.\n2. EBUS: 4R, 7, 11L sampled. Granulomas found.\n3. LLL Cryo: 4 biopsies taken with blocker in place.\n4. Bleeding after 2nd biopsy, blocker inflated.\n5. Bleeding stopped.\n6. Extubated, stable.",
            5: "patient christopher lee dob 1955. complex case lymph nodes and lll lung issue. used general anesthesia. part 1 ebus done 4r 7 and 11l. rose showed granulomas not cancer. part 2 cryobiopsy lll 4 samples 6 sec freeze. used a blocker for safety. moderate bleeding happened but we stopped it. patient admitted for observation.",
            6: "Pt: Christopher Lee Medical Record Number: KJ-7482-N Date of Birth: 10/18/1955 COMPLEX INDICATION: Mediastinal lymphadenopathy + LLL peripheral infiltrate (? ILD vs malignancy) GENERAL ANESTHESIA: ETT, sevoflurane maintenance, Ramsay 6 Continuous monitoring with arterial line PART 1 - EBUS FOR LYMPH NODES: Station 4R: 13mm, 3 passes, ROSE shows non-necrotizing granulomas Station 7: 16mm, 4 passes, ROSE shows similar granulomatous inflammation Station 11L: 9mm, 3 passes, ROSE adequate Staging indication: No... [Rest of text]",
            7: "[Indication]\nMediastinal adenopathy and LLL infiltrate.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nEBUS-TBNA stations 4R, 7, 11L (Granulomas). Transbronchial cryobiopsy of LLL x4. Prophylactic blocker used. Bleeding controlled.\n[Plan]\nAdmit for observation.",
            8: "Mr. Lee had a complex presentation with swollen lymph nodes and a spot in his lower left lung. We put him under general anesthesia to be safe. First, we used EBUS to sample the nodes at 4R, 7, and 11L—preliminary results point to granulomas, not cancer. Then, we used a cryoprobe to freeze and remove pieces of the lung tissue in the lower lobe for diagnosis. We used a balloon blocker to manage the expected bleeding, and he did fine.",
            9: "Pt: Christopher Lee. COMPLEX INDICATION: Mediastinal lymphadenopathy + LLL peripheral infiltrate. GENERAL ANESTHESIA: ETT. PART 1 - EBUS FOR LYMPH NODES: Station 4R: 13mm, 3 passes. Station 7: 16mm, 4 passes. Station 11L: 9mm, 3 passes. PART 2 - TRANSBRONCHIAL CRYOBIOPSY: LLL peripheral infiltrate sampled with cryoprobe. Cryobiopsies x4. SAFETY EVENTS: Moderate hemorrhage after 2nd cryobiopsy. Controlled with blocker inflation."
        },
        6: { # Robert Anderson (EBUS 4R, 7, 10R)
            1: "Protocol: Study #2024-BR-0847.\nPt: Robert Anderson.\nIndication: Staging.\nEBUS: 4R, 7, 10R.\nResults: 4R/7 Malignant (N2). 10R Benign.\nMetrics: Systematic exam complete. Photos taken.",
            2: "PROCEDURE NOTE: Mr. Anderson was enrolled in the Bronchoscopy Registry Study. EBUS-TBNA was performed for staging of RLL adenocarcinoma. Stations 4R, 7, and 10R were identified and sampled systematically. ROSE confirmed malignancy in 4R and 7 (N2 disease). Station 10R was negative. All quality metrics including photodocumentation and molecular sampling were met.",
            3: "Coding: 31653 (EBUS-TBNA 3 stations).\nSites: 4R, 7, 10R.\nDiagnosis: RLL Adenocarcinoma staging.\nNote: N2 disease confirmed. Study protocol followed.",
            4: "Resident Note\nPatient: Robert Anderson\nProcedure: EBUS Staging\n- Mod sedation.\n- EBUS TBNA: 4R, 7, 10R.\n- 4R/7 positive for cancer.\n- 10R negative.\n- No complications.\n- Systematic exam done.",
            5: "protocol bronch registry study subject s-047 robert anderson 68 male. indication staging rll cancer. sedation versed fentanyl. ebus stations sampled 4r 10mm 4 passes rose positive. station 7 15mm 4 passes rose positive. station 10r 7mm 3 passes negative. quality metrics met systematic exam photos taken. n2 disease confirmed no adverse events.",
            6: "PROTOCOL: Bronchoscopy Registry Study #2024-BR-0847 SUBJECT ID: S-047 DEMOGRAPHICS: 68 y.o. male, former smoker (40 pack-years, quit 2018) DATE: 2024-10-15 OPERATOR: De-identified per protocol PRIMARY INDICATION: Mediastinal lymph node staging TARGET PATHOLOGY: Right lower lobe adenocarcinoma (biopsy-proven) ANESTHESIA PROTOCOL: ... [Rest of text]",
            7: "[Indication]\nStaging RLL Adenocarcinoma.\n[Anesthesia]\nModerate Sedation.\n[Description]\nSystematic EBUS. Sampled 4R, 7, 10R. 4R and 7 positive for malignancy. 10R negative.\n[Plan]\nFollow protocol/Tumor board.",
            8: "Mr. Anderson participated in our bronchoscopy study today. We needed to stage his right lower lobe cancer. Using EBUS, we sampled lymph nodes at stations 4R, 7, and 10R. The samples from 4R and 7 came back positive for cancer cells, confirming spread to the mediastinum. We made sure to take photos and follow all the study protocols strictly.",
            9: "PROTOCOL: Bronchoscopy Registry Study #2024-BR-0847. PRIMARY INDICATION: Mediastinal lymph node staging. EBUS-TBNA STATIONS SAMPLED: Station 4R: 10mm, 4 passes, ROSE Positive. Station 7: 15mm, 4 passes, ROSE Positive. Station 10R: 7mm, 3 passes, ROSE Adequate. QUALITY METRICS: Systematic evaluation executed. Photodocumentation complete. DIAGNOSTIC YIELD: N2 disease verified."
        },
        7: { # Robert Martinez (EBUS 4 stations)
            1: "Pt: Robert Martinez.\nIndication: Staging RUL Adeno.\nEBUS: Systematic N3->N1.\nSampled: 4R(12mm), 7(18mm), 10R(8mm), 11R(6mm).\nResult: 4R/7 Malignant. 10R/11R Benign.\nComp: None.",
            2: "OPERATIVE REPORT: Mr. Martinez underwent EBUS-TBNA for staging of a new RUL adenocarcinoma. Under moderate sedation, a systematic review was performed. Transbronchial needle aspiration was conducted at stations 4R, 7, 10R, and 11R. Rapid on-site evaluation confirmed malignancy in the mediastinal stations (4R, 7), while hilar/interlobar stations (10R, 11R) were negative. This confirms N2 disease.",
            3: "CPT: 31653 (EBUS-TBNA 3+ stations).\nStations: 4R, 7, 10R, 11R (4 total).\nFindings: Positive N2 disease (4R, 7).\nAdequacy: ROSE utilized, samples adequate.",
            4: "Procedure: EBUS Staging\nPatient: Robert Martinez\nSteps:\n1. Sedation (Versed/Fent).\n2. EBUS Scope.\n3. Sampled 4R, 7, 10R, 11R.\n4. 4R and 7 positive for cancer.\n5. 10R and 11R negative.\n6. No complications.",
            5: "robert martinez here for staging rul cancer. date 09 15 2024. sedation moderate. procedure systematic ebus tbna. sampled 4r 12mm 4 passes rose pos. 7 18mm 4 passes rose pos. 10r 8mm 3 passes neg. 11r 6mm 3 passes neg. no complications adequate sampling of mediastinum and hilum.",
            6: "Patient: Robert Martinez MRN: KL-847-92 DOB: 07/22/1958 Procedure Date: 09/15/2024 INDICATION: Mediastinal staging for newly diagnosed right upper lobe lung adenocarcinoma. PET-CT shows FDG-avid mediastinal lymphadenopathy. SEDATION: Moderate sedation achieved with midazolam 3mg IV + fentanyl 75mcg IV. Patient remained Ramsay 3 throughout procedure. Continuous SpO2 monitoring maintained >95%. Blood pressure checked every 5 minutes per protocol. PROCEDURE: Systematic EBUS-TBNA evaluation performed following N3->N2->N1 sequence... [Rest of text]",
            7: "[Indication]\nStaging RUL Adenocarcinoma.\n[Anesthesia]\nModerate sedation.\n[Description]\nSystematic EBUS. Sampled 4 stations: 4R, 7, 10R, 11R. Malignancy confirmed in 4R and 7.\n[Plan]\nOncology follow-up.",
            8: "Mr. Martinez came in for staging of his lung cancer. We did a thorough EBUS exam, checking lymph nodes from the mediastinum out to the lung. We sampled four specific stations: 4R, 7, 10R, and 11R. The biopsy results right there in the room showed cancer in the 4R and 7 nodes, but the 10R and 11R nodes looked clear. He handled the sedation well.",
            9: "Patient: Robert Martinez. INDICATION: Mediastinal staging for newly diagnosed right upper lobe lung adenocarcinoma. PROCEDURE: Systematic EBUS-TBNA evaluation executed following N3->N2->N1 sequence. Stations sampled: Station 4R: 4 needle passes, ROSE positive. Station 7: 4 needle passes, ROSE positive. Station 10R: 3 needle passes, ROSE adequate. Station 11R: 3 needle passes, ROSE adequate. IMPRESSION: EBUS-TBNA with sufficient sampling."
        },
        8: { # Angela Davis (BAL + Brush LLL)
            1: "Indication: LLL infiltrate.\nAnesthesia: Topical only (Lido).\nFindings: LLL erythema/edema.\nSamples: BAL x3, Brush x2.\nNo TBBX performed.\nDispo: Home.",
            2: "PROCEDURE NOTE: Ms. Davis presented for evaluation of a persistent LLL infiltrate. The procedure was performed with topical anesthesia only; the patient was awake and cooperative. Inspection revealed moderate erythema and edema in the LLL basilar segments. Bronchoalveolar lavage (BAL) and brush cytology were performed. Transbronchial biopsies were deferred per patient preference.",
            3: "Codes: 31624 (BAL), 31623 (Brush).\nSite: Left Lower Lobe.\nFindings: Inflammation.\nNote: No TBBX (31628) performed.\nTime: 18 min.",
            4: "Resident Note\nPatient: Angela Davis\nProcedure: Bronchoscopy\n- Topical anesthesia.\n- Airway exam: LLL inflammation.\n- BAL x3 performed.\n- Brush x2 performed.\n- No biopsy.\n- Tolerated well.",
            5: "patient angela davis mrn kp 9274 b. indication lll infiltrate. topical anesthesia only no sedation. airway looked ok except lll had redness and edema. did bal times 3 and brush cytology times 2. patient didnt want biopsies so we skipped that. systematic inspection done. no complications discharged.",
            6: "Patient: Angela Davis MR Number: KP-9274-B D.O.B.: 05/12/1970 Indication: Evaluation of LLL infiltrate, r/o endobronchial lesion Topical anesthesia only: Nebulized lidocaine 4% + transtracheal 2% injection Patient awake and cooperative, Ramsay 1-2 Findings: - Upper airways normal - Carina sharp, mobile - RUL/RML/RLL - all subsegments examined, normal - LUL - normal - LLL - moderate erythema and edema of basilar segments, no endobronchial lesion Samples obtained from LLL: - BAL x3 (50cc aliquots) sent for bacterial cx, fungal cx, viral PCR, cytology... [Rest of text]",
            7: "[Indication]\nLLL infiltrate.\n[Anesthesia]\nTopical Lidocaine.\n[Description]\nBronchoscopy showing LLL erythema. BAL x3 and Brush x2 obtained. No biopsies.\n[Plan]\nDischarge home.",
            8: "Ms. Davis needed her left lower lung checked out because of an infiltrate seen on x-ray. She chose to have it done with just numbing medicine and no sedation. We looked down and saw some redness and swelling in the lower lobe. We washed the area (BAL) and used a brush to get some cells for the lab. She decided against having any tissue biopsies taken today.",
            9: "Patient: Angela Davis. Indication: Evaluation of LLL infiltrate. Topical anesthesia only. Findings: LLL - moderate erythema and edema of basilar segments. Samples acquired from LLL: BAL x3 sent for bacterial cx, fungal cx, viral PCR, cytology. Brush cytology x2 from affected area. Transbronchial biopsies not executed."
        },
        9: { # James Wilson (EBUS 3 stations)
            1: "Data Entry: James Wilson.\nProc: EBUS-TBNA.\nNodes: 4R (10mm, 4p), 7 (14mm, 4p), 11R (7mm, 3p).\nFindings: 4R/7 Positive. 11R Adequate.\nComp: None.\nSystematic: Yes.",
            2: "REGISTRY REPORT: Mr. Wilson underwent EBUS-TBNA for staging. Systematic evaluation was documented. Lymph node stations 4R and 7 were sampled and found positive for malignancy on ROSE. Station 11R was sampled and was adequate but negative. No complications occurred.",
            3: "Code: 31653 (EBUS 3 stations).\nStations: 4R, 7, 11R.\nDetail: 4R/7 malignant, 11R benign.\nData: Structured entry confirmed.",
            4: "Procedure: EBUS\nPatient: James Wilson\n- Moderate sedation.\n- Sampled 4R, 7, 11R.\n- ROSE positive in 4R and 7.\n- No complications.\n- Photos taken.",
            5: "data entry form case br 2024 10 0847 james wilson. procedure ebus tbna. sedation moderate. stations sampled 4r 10mm 4 passes rose pos. 7 14mm 4 passes rose pos. 11r 7mm 3 passes rose adequate. complications none. quality metrics systematic eval and photos yes.",
            6: ">>DATA ENTRY FORM: BRONCHOSCOPY REGISTRY<< CASE ID: BR-2024-10-0847 TIMESTAMP: 2024-10-28 14:22:35 [PATIENT IDENTIFIERS] Name: James Wilson MRN: LL-9384-P DOB: 08/25/1957 [PROCEDURE TYPE] ( ) Diagnostic flexible bronchoscopy (X) EBUS-TBNA ( ) Navigation bronchoscopy ( ) Therapeutic bronchoscopy ( ) Combined (specify): ____________ [SEDATION] Type: (X) Moderate ( ) Deep ( ) General ( ) Local Ramsay Max: [3]... [Rest of text]",
            7: "[Indication]\nStaging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA of 4R, 7, 11R. 4R and 7 positive.\n[Plan]\nFollow up.",
            8: "Mr. Wilson had his EBUS procedure logged into the registry today. We sampled three main lymph nodes: 4R, 7, and 11R. The results for 4R and 7 were positive for cancer, while 11R was clear. Everything went according to protocol with no issues.",
            9: "CASE ID: BR-2024-10-0847. Name: James Wilson. [PROCEDURE TYPE] (X) EBUS-TBNA. Station Data Entry: [Add Station] -> Station: [4R] Size: [10]mm Passes: [4] ROSE: (X)Positive. [Add Station] -> Station: [7] Size: [14]mm Passes: [4] ROSE: (X)Positive. [Add Station] -> Station: [11R] Size: [7]mm Passes: [3] ROSE: (X)Adequate."
        }
    }
    return variations

def get_base_data_mocks():
    # Names are mocked for the 9 variations per note.
    # Original data:
    # 0: Harold Kim, 71 (1953)
    # 1: Sarah Miller, 65 (1959)
    # 2: Susan M. O'Brien, 64 (1961)
    # 3: Catherine Martinez, 73 (1951)
    # 4: Michael Foster, 64 (1960)
    # 5: Christopher Lee, 69 (1955)
    # 6: Robert Anderson, 68 (1956)
    # 7: Robert Martinez, 66 (1958)
    # 8: Angela Davis, 54 (1970)
    # 9: James Wilson, 67 (1957)
    
    return [
        {"idx": 0, "orig_name": "Harold Kim", "orig_age": 71, "names": ["John Smith", "David Johnson", "Robert Williams", "Michael Brown", "William Jones", "Richard Garcia", "Joseph Miller", "Thomas Davis", "Charles Rodriguez"]},
        {"idx": 1, "orig_name": "Sarah Miller", "orig_age": 65, "names": ["Mary Martinez", "Patricia Hernandez", "Jennifer Lopez", "Linda Gonzalez", "Elizabeth Wilson", "Barbara Anderson", "Susan Thomas", "Jessica Taylor", "Sarah Moore"]},
        {"idx": 2, "orig_name": "Susan M. O'Brien", "orig_age": 64, "names": ["Margaret Jackson", "Dorothy Martin", "Lisa Lee", "Nancy Perez", "Karen Thompson", "Betty White", "Helen Harris", "Sandra Sanchez", "Donna Clark"]},
        {"idx": 3, "orig_name": "Catherine Martinez", "orig_age": 73, "names": ["Carol Ramirez", "Ruth Lewis", "Sharon Robinson", "Michelle Walker", "Laura Young", "Sarah Allen", "Kimberly King", "Deborah Wright", "Jessica Scott"]},
        {"idx": 4, "orig_name": "Michael Foster", "orig_age": 64, "names": ["Christopher Torres", "Daniel Nguyen", "Paul Hill", "Mark Flores", "Donald Green", "George Adams", "Kenneth Nelson", "Steven Baker", "Edward Hall"]},
        {"idx": 5, "orig_name": "Christopher Lee", "orig_age": 69, "names": ["Brian Rivera", "Ronald Campbell", "Anthony Mitchell", "Kevin Carter", "Jason Roberts", "Matthew Gomez", "Gary Phillips", "Timothy Evans", "Jose Turner"]},
        {"idx": 6, "orig_name": "Robert Anderson", "orig_age": 68, "names": ["Larry Diaz", "Jeffrey Parker", "Frank Cruz", "Scott Edwards", "Eric Collins", "Stephen Reyes", "Andrew Stewart", "Raymond Morris", "Gregory Morales"]},
        {"idx": 7, "orig_name": "Robert Martinez", "orig_age": 66, "names": ["Joshua Murphy", "Jerry Cook", "Dennis Rogers", "Walter Morgan", "Patrick Bell", "Peter Reed", "Harold Bailey", "Douglas Cooper", "Henry Richardson"]},
        {"idx": 8, "orig_name": "Angela Davis", "orig_age": 54, "names": ["Cynthia Cox", "Kathleen Howard", "Amy Ward", "Shirley Brooks", "Angela Kelly", "Helen Sanders", "Anna Price", "Brenda Bennett", "Pamela Wood"]},
        {"idx": 9, "orig_name": "James Wilson", "orig_age": 67, "names": ["Arthur Barnes", "Ryan Ross", "Carl Henderson", "Justin Coleman", "Terry Jenkins", "Gerald Perry", "Keith Powell", "Samuel Long", "Willie Patterson"]},
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
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if no variation found (shouldn't happen with full dict)
                note_entry["note_text"] = f"Variation {style_num} for Note {idx} not found."
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update procedure date if it exists
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
                
                # The registry entry in this specific file structure (part 039) 
                # does not explicitly store patient_age in the registry_entry dict in the example provided,
                # but relies on DOB or metadata. If we needed to update metadata:
                if "metadata" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["metadata"]["generated_name"] = new_name
                     note_entry["registry_entry"]["metadata"]["generated_age"] = new_age

            # Add metadata about the synthetic generation
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generated_age": new_age,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_blvr_notes_part_039.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()