import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_013.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations for the notes 
    in consolidated_verified_notes_v2_8_part_013.json.
    Structure: Note_Index (0-8) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Robert Mosbey Wiggins (Stent Removal/Cryo)
            1: "Procedure: Rigid Bronchoscopy, Stent Removal, Cryotherapy.\nIndication: Stent obstruction (granulation).\nAction:\n- 12mm rigid scope inserted.\n- Flexible scope used to inspect.\n- Y-stent removed intact with rigid forceps.\n- Significant TBM collapse noted post-removal.\n- Cryotherapy applied to granulation tissue (30s freeze x3).\nPlan: Stent holiday.",
            2: "OPERATIVE REPORT: Rigid Bronchoscopy with Airway Intervention.\nINDICATION: Symptomatic airway obstruction due to granulation tissue within an indwelling tracheal Y-stent.\nPROCEDURE: The airway was secured with a 12mm rigid tracheoscope. Inspection revealed significant granulation tissue obstructing the distal limbs of the Y-stent. The stent was grasped proximally with rigid optical forceps and withdrawn en bloc without complication. Following removal, marked dynamic airway collapse consistent with severe tracheobronchomalacia was observed. Residual granulation tissue was treated with cryotherapy (1.9mm probe, multiple activation cycles).",
            3: "CPT Coding Summary:\n31638: Bronchoscopy with removal of tracheal stent (Y-stent removed via rigid forceps).\n31641: Bronchoscopy with destruction of tumor/stenosis (Cryotherapy destruction of granulation tissue causing obstruction).\nNote: Procedure performed under General Anesthesia with Rigid Bronchoscope.",
            4: "Procedure Note\nPatient: Robert Wiggins\nAttending: Dr. Muller\n\n1. GA/Paralysis.\n2. Rigid scope to subglottis.\n3. Flex scope inspection: Stent obstructed by granulation.\n4. Stent Removal: Rigid forceps used to twist and pull stent out.\n5. Post-removal exam: Severe TBM.\n6. Cryo: Applied to granulation sites.\n7. Pt stable to PACU.",
            5: "dr muller here performing bronch on robert wiggins. indication stent blocked by granulation tissue. we put in the rigid scope. saw the stent was clogged up pretty bad. grabbed it with the big forceps and pulled it out came out fine. airway collapsed right away cause of his tbm. froze the bad tissue with the cryo probe. no complications plan is stent holiday.",
            6: "Rigid and flexible bronchoscopy performed for airway stent obstruction. 12mm rigid tracheoscope used. Y-stent removed intact using rigid optical forceps. Examination post-removal showed severe tracheobronchomalacia. Granulation tissue at former stent sites treated with cryotherapy (1.9mm probe, 30 sec freeze). No complications. Patient transferred to PACU.",
            7: "[Indication]\nAirway stent obstruction (granulation tissue), TBM.\n[Anesthesia]\nGeneral (Rigid).\n[Description]\nRigid bronchoscopy. Stent removal via forceps. Cryotherapy to granulation tissue post-removal.\n[Plan]\nStent holiday. Observation.",
            8: "Mr. Wiggins underwent a rigid bronchoscopy today to address an obstruction in his airway stent. We found granulation tissue blocking about half of the stent's limbs. We used heavy-duty forceps through the rigid tube to grab the stent and pull it out completely. Once it was out, we saw his airway collapse significantly, which we expected. We used a freezing probe (cryotherapy) to treat the raw tissue where the stent had been to help it heal.",
            9: "Procedure: Rigid airway endoscopy with prosthesis extraction (31638) and cryoablation (31641).\nTarget: Tracheal Y-stent and granulation tissue.\nAction: Stent retrieval via rigid instrumentation. Cryogenic destruction of obstructive tissue.\nOutcome: Device removed. Tissue treated."
        },
        1: { # Jennifer Lee (Nav Bronch/EBUS/TBNA/TBLB)
            1: "Procedure: Navigational Bronchoscopy, Radial EBUS, Biopsy.\nTarget: 22mm RLL nodule.\nNav: Electromagnetic (SuperDimension) + Fluoro.\nConfirmation: Radial EBUS (Concentric).\nSampling: TBNA x3, Forceps x4, Brush x2.\nComp: Mild pneumothorax (10%), conservative mgmt.",
            2: "PROCEDURE NOTE: Electromagnetic Navigation Bronchoscopy.\nINDICATION: RLL pulmonary nodule (22mm), suspicious for malignancy.\nDETAILS: Navigation was performed to the RLL superior segment. Radial EBUS confirmed a concentric lesion. Transbronchial needle aspiration (TBNA), forceps biopsies, and brushings were obtained under fluoroscopic guidance. \nCOMPLICATION: Post-procedure imaging revealed a small (10%) apical pneumothorax. The patient remained asymptomatic and stable; no chest tube was required.",
            3: "Billing Codes:\n31627: Navigation add-on (EMN system used).\n31654: Radial EBUS add-on (Peripheral lesion confirmation).\n31629: TBNA of RLL nodule.\n31628: Transbronchial lung biopsy of RLL nodule.\nNote: Pneumothorax managed conservatively (observation only).",
            4: "Resident Procedure Note\nPt: Jennifer Lee\nAttending: [Unknown]\n1. Mod Sedation.\n2. Nav to RLL nodule.\n3. REBUS: Concentric.\n4. Biopsies: Needle, Forceps, Brush.\n5. Fluoro used.\n6. CXR: Small pneumo. Observed.\n7. Discharge.",
            5: "jennifer lee bronch case. went after that rll nodule. used the navigation system and radial ebus showed it perfectly. did needle biopsy then forceps then brush. she got a small pneumothorax after but she felt fine so we just watched her for 4 hours and sent her home. no chest tube needed.",
            6: "Electromagnetic navigation bronchoscopy performed for 22mm RLL nodule. Radial EBUS confirmed concentric position. Sampling performed via TBNA, forceps, and brush. Complicated by small 10% pneumothorax, managed conservatively with observation. Patient discharged stable.",
            7: "[Indication]\n22mm RLL nodule, bronchus sign positive.\n[Anesthesia]\nModerate.\n[Description]\nNav bronch to RLL. Radial EBUS confirmation. TBNA/TBLB/Brush samples obtained.\n[Complications]\nMild pneumothorax (10%).\n[Plan]\nObservation. Discharge if stable.",
            8: "Ms. Lee came in for a biopsy of a spot in her right lower lung. We used a navigation system to guide a catheter to the nodule and confirmed its location with a mini-ultrasound probe. We took several samples using a needle, forceps, and a brush. Unfortunately, she developed a small air leak (pneumothorax) from the biopsy, but it was small enough that she didn't need a tube and could go home after we watched her for a few hours.",
            9: "Procedure: Guided bronchoscopy (31627), Sonographic verification (31654), Needle aspiration (31629), Tissue sampling (31628).\nTarget: RLL mass.\nComplication: Pneumothorax (minor).\nAction: Multi-modal sampling.\nOutcome: Stable for discharge."
        },
        2: { # Barbara Wilson (EBUS Lymphoma)
            1: "Procedure: EBUS-TBNA.\nIndication: Hodgkin Lymphoma staging.\nNodes Sampled:\n- 4R (18mm): 3 passes.\n- 4L (21mm): 3 passes.\n- 7 (16mm): 4 passes.\n- 10R (14mm): 3 passes.\nROSE: Atypical large cells. Samples sent fresh for flow cytometry.",
            2: "OPERATIVE REPORT: Endobronchial Ultrasound-Guided TBNA.\nINDICATION: Mediastinal staging for newly diagnosed Hodgkin Lymphoma.\nFINDINGS: Enlarged lymph nodes identified at stations 4R, 4L, 7, and 10R. \nTECHNIQUE: Systematic sampling was performed. ROSE confirmed adequacy and presence of atypical cells. Fresh tissue was prioritized and submitted for flow cytometric analysis to ensure accurate subtyping.",
            3: "Code: 31653 (EBUS sampling 3+ stations).\nStations: 4R, 4L, 7, 10R.\nPathology: Special handling for Flow Cytometry (Lymphoma protocol).\nRationale: Staging of hematologic malignancy.",
            4: "Procedure: EBUS\nPt: Barbara Wilson\n1. Mod Sedation.\n2. EBUS scope inserted.\n3. Sampled 4R, 4L, 7, 10R.\n4. ROSE: Atypical cells.\n5. Sent for Flow Cytometry.\n6. No complications.",
            5: "barbara wilson ebus case. hodgkins lymphoma. we sampled a bunch of nodes 4r 4l 7 and 10r. they all looked abnormal. sent everything fresh for flow cytometry so the path lab can type it. procedure went fine no issues.",
            6: "EBUS-TBNA performed for Hodgkin lymphoma staging. Stations 4R, 4L, 7, and 10R were sampled. ROSE showed atypical large cells. Samples submitted for flow cytometry and molecular markers. No complications.",
            7: "[Indication]\nHodgkin Lymphoma staging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA of stations 4R, 4L, 7, 10R. Fresh samples for flow cytometry.\n[Plan]\nHeme/Onc follow-up.",
            8: "We performed an EBUS procedure on Ms. Wilson to determine the stage of her Hodgkin lymphoma. We found and sampled enlarged lymph nodes on both sides of the trachea and under the carina. We made sure to collect fresh tissue for special testing called flow cytometry, which is crucial for lymphoma diagnosis. The procedure went smoothly.",
            9: "Procedure: EBUS-guided aspiration (31653).\nTarget: Mediastinal adenopathy.\nAction: Stations 4R, 4L, 7, 10R accessed. Specimens harvested.\nAnalysis: Fresh tissue submitted for immunophenotyping."
        },
        3: { # Harold Kim (EBUS Staging)
            1: "Procedure: EBUS-TBNA.\nIndication: NSCLC Staging.\nFindings:\n- 4R (11mm, PET+): Malignant.\n- 7 (14mm, PET+): Malignant.\n- 10R (7mm): Adequate.\nAssessment: N2 disease (4R/7 positive).",
            2: "PROCEDURE: EBUS-TBNA Staging.\nINDICATION: Pre-resection staging for NSCLC.\nFINDINGS: Stations 4R and 7 were enlarged and PET-avid. Station 10R was also sampled. \nPATHOLOGY: ROSE confirmed malignancy in stations 4R and 7, confirming N2 disease. Station 10R was benign. \nPLAN: Referral for neoadjuvant chemotherapy.",
            3: "Billing: 31653 (EBUS sampling >2 stations).\nStations: 4R, 7, 10R.\nDx: Lung Cancer with N2 nodal involvement.\nNotes: Molecular tissue obtained.",
            4: "Procedure: EBUS Staging\nPt: Harold Kim\n1. Mod Sedation.\n2. Systematic EBUS.\n3. Sampled 4R, 7, 10R.\n4. ROSE positive at 4R and 7.\n5. N2 disease confirmed.\n6. Plan: Tumor board.",
            5: "harold kim ebus note. staging his lung cancer. 4r and 7 looked bad on pet and ebus confirmed cancer in both. 10r was negative. so he has n2 disease. needs chemo before surgery probably. no complications.",
            6: "EBUS-TBNA performed for NSCLC staging. Stations 4R, 7, and 10R sampled. ROSE confirmed malignancy in 4R and 7, establishing N2 disease. Adequate tissue obtained for molecular testing. Patient stable.",
            7: "[Indication]\nNSCLC Staging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA 4R, 7, 10R. Malignancy confirmed in 4R and 7 (N2 disease).\n[Plan]\nTumor board. Neoadjuvant therapy.",
            8: "Mr. Kim underwent EBUS to stage his lung cancer. We sampled lymph nodes in the middle of his chest. Unfortunately, the nodes at stations 4R and 7 contained cancer cells, which means the cancer has spread to the mediastinum (N2 disease). We collected enough tissue for genetic testing. He will likely need chemotherapy before any surgery.",
            9: "Procedure: Endosonographic staging (31653).\nFindings: Malignant adenopathy at 4R and 7.\nOutcome: N2 disease confirmed. Tissue banked for molecular analysis."
        },
        4: { # Sarah Miller (EBUS N2)
            1: "Procedure: EBUS-TBNA.\nNodes:\n- 4R: 11mm (Malignant).\n- 7: 16mm (Malignant).\n- 10R: 7mm (Benign).\nAssessment: N2 positive.\nMolecular: Sent from 4R.",
            2: "PROCEDURE NOTE: EBUS-TBNA.\nINDICATION: Lung cancer staging.\nRESULTS: Systematic evaluation performed. Stations 4R and 7 were enlarged, PET-positive, and confirmed malignant on ROSE. Station 10R was negative. \nCONCLUSION: Confirmed N2 mediastinal disease. Samples submitted for molecular profiling.",
            3: "Code: 31653.\nStations: 4R, 7, 10R.\nAdequacy: Confirmed on all.\nSpecial Tests: Molecular ordered.",
            4: "Procedure: EBUS\nPt: Sarah Miller\n1. Mod Sedation.\n2. EBUS of 4R, 7, 10R.\n3. ROSE: Pos for cancer at 4R/7.\n4. N2 disease.\n5. Molecular sent.\n6. Pt discharged.",
            5: "sarah miller ebus. checked the nodes. 4r and 7 were cancer. 10r was fine. so she has n2 disease. sent the 4r sample for molecular testing. procedure went fast 32 mins. no issues.",
            6: "EBUS-TBNA performed. Stations 4R, 7, and 10R sampled. ROSE confirmed malignancy in 4R and 7. Station 10R benign. Molecular testing requested. N2 disease confirmed.",
            7: "[Indication]\nStaging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA 4R, 7, 10R. N2 positive (4R, 7).\n[Plan]\nOncology.",
            8: "We performed an EBUS on Ms. Miller. We sampled three lymph node stations. The nodes at 4R and 7 were positive for cancer, confirming spread to the mediastinum. The hilar node at 10R was negative. We sent the tissue for molecular testing to help guide treatment.",
            9: "Procedure: EBUS aspiration (31653).\nFindings: Metastatic disease at 4R/7.\nAssessment: N2 disease.\nAction: Molecular profiling initiated."
        },
        5: { # Michael Foster (Nav Bronch/EBUS/Biopsy)
            1: "Procedure: Nav Bronch + EBUS-TBNA.\nEBUS: 4R (Pos), 7 (Pos), 10L (Benign).\nNav Bronch: LUL mass biopsied (Forceps/Brush).\nComp: Minor bleeding, controlled.\nAssessment: NSCLC with N2 disease.",
            2: "OPERATIVE SUMMARY: Combined EBUS staging and navigational biopsy.\nEBUS FINDINGS: Stations 4R and 7 were sampled and found to be malignant on ROSE. Station 10L was benign.\nPARENCHYMAL BIOPSY: The LUL mass was accessed via bronchoscopy. Forceps biopsies and brushings were obtained. \nDIAGNOSIS: Lung cancer with mediastinal involvement (N2).",
            3: "Billing:\n31653: EBUS sampling 3 stations (4R, 7, 10L).\n31625: Endobronchial biopsy of LUL mass (separate site).\nNote: Navigational code 31627 not explicitly supported by text (mention of 'Bronch' for mass, but Nav details sparse), conservative coding applied.",
            4: "Procedure: EBUS + Bronchoscopy\nPt: Michael Foster\n1. Mod Sedation.\n2. EBUS: 4R, 7 (Cancer); 10L (Benign).\n3. Bronchoscopy: LUL mass biopsied.\n4. Bleeding controlled.\n5. Plan: Tumor board.",
            5: "michael foster case. did ebus first found cancer in 4r and 7. then went to the lul mass and biopsied that too. got good samples. bit of bleeding but stopped it with epi. looks like n2 disease. tumor board next week.",
            6: "Combined EBUS-TBNA and diagnostic bronchoscopy. EBUS of stations 4R, 7, and 10L performed. ROSE confirmed malignancy in 4R and 7. LUL mass subsequently biopsied using forceps and brush. Hemostasis achieved. Diagnosis: NSCLC with N2 nodal disease.",
            7: "[Indication]\nLUL mass, adenopathy.\n[Anesthesia]\nModerate.\n[Description]\nEBUS: 4R, 7 positive. 10L negative. Bronchoscopy: LUL mass biopsied.\n[Plan]\nOncology.",
            8: "Mr. Foster underwent a bronchoscopy with EBUS. We first checked his lymph nodes and found cancer in the mediastinal nodes (4R and 7), confirming N2 disease. We then biopsied the main mass in his left upper lung. There was some minor bleeding which we stopped with medication. The preliminary diagnosis is lung cancer with spread to the lymph nodes.",
            9: "Procedure: EBUS staging (31653) and tumor biopsy (31625).\nFindings: N2 disease (4R/7 positive). LUL mass sampled.\nOutcome: Diagnosis established."
        },
        6: { # Christopher Lee (Complex EBUS/Cryo)
            1: "Procedure: EBUS-TBNA + Cryobiopsy.\nEBUS: 4R, 7, 11L sampled. Granulomas found (Sarcoid?).\nCryobiopsy: LLL infiltrate. 4 samples. Blocker used.\nComp: Moderate bleeding controlled with blocker.\nAssessment: Granulomatous disease vs ILD.",
            2: "PROCEDURE NOTE: Combined EBUS and Transbronchial Cryobiopsy.\nINDICATION: Lymphadenopathy and LLL infiltrate.\nEBUS: Stations 4R, 7, and 11L sampled. ROSE showed non-necrotizing granulomas.\nPARENCHYMA: Cryobiopsies obtained from LLL infiltrate. Prophylactic blocker utilized. Moderate bleeding encountered and controlled with blocker inflation.\nIMPRESSION: Likely sarcoidosis or other granulomatous process.",
            3: "Billing:\n31653: EBUS sampling 3 stations.\n31628: Transbronchial lung biopsy (Cryobiopsy technique) of LLL.\nNote: Bronchial blocker placement bundled into biopsy codes.",
            4: "Procedure: EBUS + Cryo TBLB\nPt: Christopher Lee\n1. GA / ETT.\n2. EBUS: 4R, 7, 11L (Granulomas).\n3. Cryobiopsy: LLL x4.\n4. Blocker used for bleeding control.\n5. No pneumo.\n6. Overnight obs.",
            5: "christopher lee complex case. did ebus first found granulomas in 4r 7 and 11l. then did cryo biopsy of the lung infiltrate in lll. bled a fair bit but the blocker stopped it. keeping him overnight just to be safe. probably sarcoid.",
            6: "EBUS-TBNA and transbronchial cryobiopsy performed. EBUS of 4R, 7, 11L revealed granulomatous inflammation. Cryobiopsy of LLL infiltrate performed with prophylactic blocker. Moderate bleeding controlled. No pneumothorax. Patient admitted for observation.",
            7: "[Indication]\nAdenopathy + Infiltrate.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS: 4R, 7, 11L (Granulomas). Cryobiopsy LLL x4. Blocker used for hemorrhage control.\n[Plan]\nAdmit for observation.",
            8: "Mr. Lee underwent a procedure to investigate swollen lymph nodes and lung shadows. We used EBUS to sample the nodes, which showed signs of inflammation (granulomas) rather than cancer. We then used a cryoprobe to take larger biopsies of the lung tissue in the lower left lobe. This caused some bleeding, which we managed by inflating a small balloon in the airway. He will stay overnight for monitoring.",
            9: "Procedure: EBUS (31653) and Cryo-TBLB (31628).\nFindings: Granulomatous adenopathy.\nAction: Parenchymal cryobiopsy with balloon tamponade for hemostasis.\nOutcome: Hemostasis achieved. Observation initiated."
        },
        7: { # Robert Anderson (Study EBUS)
            1: "Procedure: EBUS-TBNA (Study Protocol).\nNodes: 4R (Pos), 7 (Pos), 10R (Benign).\nMetrics: Systematic exam, photos, adequacy confirmed.\nResult: N2 disease.\nPlan: Protocol follow-up.",
            2: "PROCEDURE: EBUS-TBNA per Registry Protocol.\nINDICATION: Staging of RLL adenocarcinoma.\nFINDINGS: Stations 4R and 7 were PET-positive and confirmed malignant on ROSE. Station 10R was benign. \nQUALITY: All protocol metrics met (systematic exam, photodocumentation, cell block).\nCONCLUSION: N2 disease confirmed.",
            3: "Code: 31653 (EBUS >2 stations).\nStations: 4R, 7, 10R.\nNotes: High quality metrics documented (ROSE, Photos).",
            4: "Procedure: EBUS\nPt: Robert Anderson\n1. Mod Sedation.\n2. Protocol EBUS.\n3. Sampled 4R, 7, 10R.\n4. ROSE positive 4R/7.\n5. N2 confirmed.\n6. No complications.",
            5: "robert anderson research ebus. followed the protocol. 4r and 7 were cancer. 10r was fine. took pictures of everything. rose was good. n2 disease.",
            6: "EBUS-TBNA performed for staging per protocol. Stations 4R, 7, and 10R sampled. Malignancy confirmed in 4R and 7. Station 10R benign. 100% protocol adherence. N2 disease diagnosed.",
            7: "[Indication]\nStaging RLL Adeno.\n[Anesthesia]\nModerate.\n[Description]\nEBUS 4R, 7, 10R. Malignant 4R/7. Protocol complete.\n[Plan]\nData entry.",
            8: "We performed a staging EBUS on Mr. Anderson as part of a registry study. We systematically checked and sampled lymph nodes. The nodes at 4R and 7 were positive for cancer, confirming N2 disease. We followed all study protocols including taking photos and ensuring sample adequacy.",
            9: "Procedure: Protocol-driven EBUS (31653).\nFindings: N2 malignancy (4R/7).\nAction: Systematic sampling and documentation.\nOutcome: Staging complete."
        },
        8: { # Susan M. O'Brien (Nav/MWA)
            1: "Procedure: Nav Bronch, MWA RML.\nTarget: 2.4cm RML nodule (Adeno).\nNav: SuperDimension + Cone Beam CT.\nAblation: 65W for 6 min (92C).\nResult: Good ablation zone on post-proc CT.\nPlan: Admit, CT f/u.",
            2: "OPERATIVE REPORT: Bronchoscopic Microwave Ablation.\nINDICATION: RML adenocarcinoma in a surgical non-candidate.\nPROCEDURE: General anesthesia. SuperDimension navigation to RML lateral segment target. Confirmation with radial EBUS and Cone Beam CT. Microwave ablation performed (65W, 6 min). Post-ablation EBUS showed coagulation necrosis. No immediate complications.\nIMPRESSION: Successful thermal ablation of RML tumor.",
            3: "Billing:\n31641: Bronchoscopy with destruction of tumor (Microwave Ablation).\n31627: Navigation add-on.\n31654: Radial EBUS add-on.\nNotes: Cone Beam CT used for verification. Complex decision making due to comorbidities.",
            4: "Procedure: Nav Bronch + Ablation\nPt: Susan O'Brien\n1. GA/ETT.\n2. Nav to RML.\n3. REBUS/CBCT confirm position.\n4. MWA: 65W x 6min.\n5. Stable. No pneumo.\n6. Admit for obs.",
            5: "susan obrien ablation case. she cant have surgery so we burned the tumor. used superdimension and the spin ct to get right on it. cooked it for 6 mins at 65 watts. looked good on the scan after. keeping her overnight.",
            6: "Microwave ablation of RML adenocarcinoma performed via electromagnetic navigation bronchoscopy. Target confirmed with radial EBUS and Cone Beam CT. Ablation parameters: 65W for 6 minutes. Post-procedure imaging confirmed appropriate ablation zone. No complications.",
            7: "[Indication]\nRML Adenocarcinoma, medically inoperable.\n[Anesthesia]\nGeneral.\n[Description]\nNav bronch to RML. MWA (65W, 6m). CBCT verification.\n[Plan]\nAdmit. Follow-up CT.",
            8: "Mrs. O'Brien underwent a procedure to treat her lung cancer without surgery. We navigated a probe to the tumor in her right middle lung and verified the position with a 3D X-ray spin. We then used microwave energy to heat and destroy the tumor. She handled the procedure very well, and the post-procedure scan showed we successfully treated the area.",
            9: "Procedure: Tumor destruction via microwave energy (31641), Guidance (31627/31654).\nTarget: RML neoplasm.\nAction: Navigation, verification, and thermal ablation.\nOutcome: Coagulation necrosis achieved. No adverse events."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data to simulate the 'original' names/ages for consistency.
    Indices match the source file records.
    """
    return [
        {"idx": 0, "orig_name": "Robert Mosbey Wiggins", "orig_age": 65, "names": ["Charles Davis", "Thomas Wilson", "James Moore", "Robert Taylor", "Michael Anderson", "William White", "David Martin", "Richard Thompson", "Joseph Garcia"]},
        {"idx": 1, "orig_name": "Jennifer Lee", "orig_age": 65, "names": ["Linda Martinez", "Patricia Robinson", "Barbara Clark", "Elizabeth Rodriguez", "Jennifer Lewis", "Maria Lee", "Susan Walker", "Margaret Hall", "Dorothy Allen"]},
        {"idx": 2, "orig_name": "Barbara Wilson", "orig_age": 65, "names": ["Lisa Young", "Nancy Hernandez", "Karen King", "Betty Wright", "Helen Lopez", "Sandra Hill", "Donna Scott", "Carol Green", "Ruth Adams"]},
        {"idx": 3, "orig_name": "Harold Kim", "orig_age": 71, "names": ["Edward Baker", "George Gonzalez", "Donald Nelson", "Kenneth Carter", "Steven Mitchell", "Paul Perez", "Mark Roberts", "Brian Turner", "Kevin Phillips"]},
        {"idx": 4, "orig_name": "Sarah Miller", "orig_age": 65, "names": ["Deborah Campbell", "Sharon Parker", "Michelle Evans", "Laura Edwards", "Sarah Collins", "Kimberly Stewart", "Jessica Sanchez", "Cynthia Morris", "Angela Rogers"]},
        {"idx": 5, "orig_name": "Michael Foster", "orig_age": 65, "names": ["Ronald Reed", "Anthony Cook", "Jason Morgan", "Jeffrey Bell", "Ryan Murphy", "Jacob Bailey", "Gary Rivera", "Nicholas Cooper", "Eric Richardson"]},
        {"idx": 6, "orig_name": "Christopher Lee", "orig_age": 65, "names": ["Stephen Cox", "Jonathan Howard", "Larry Ward", "Scott Torres", "Frank Peterson", "Justin Gray", "Brandon Ramirez", "Gregory James", "Samuel Watson"]},
        {"idx": 7, "orig_name": "Robert Anderson", "orig_age": 65, "names": ["Raymond Brooks", "Patrick Kelly", "Jack Sanders", "Dennis Price", "Jerry Bennett", "Tyler Wood", "Aaron Barnes", "Jose Ross", "Adam Henderson"]},
        {"idx": 8, "orig_name": "Susan M. O'Brien", "orig_age": 65, "names": ["Rebecca Coleman", "Virginia Jenkins", "Kathleen Perry", "Pamela Powell", "Martha Long", "Debra Patterson", "Amanda Hughes", "Stephanie Flores", "Carolyn Washington"]}
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
    output_filename = output_dir / "synthetic_blvr_notes_part_013.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()