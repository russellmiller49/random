import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_042.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-7) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Donald Martinez (Teaching Case)
            1: "Procedure: Diagnostic Bronchoscopy (Teaching).\nIndication: Staging LUL Adeno.\nActions:\n- Airway inspected.\n- Systematic EBUS evaluation (N3->N1).\n- Needle passes performed by fellow.\n- ROSE reviewed.\nPlan: Post-proc monitoring.",
            2: "PROCEDURE NOTE: A diagnostic flexible bronchoscopy was performed for mediastinal staging of a known left upper lobe adenocarcinoma. This procedure was conducted as a formal teaching case. The fellow demonstrated a systematic approach to Endobronchial Ultrasound (EBUS), evaluating nodal stations from N3 to N1. Real-time Rapid On-Site Evaluation (ROSE) was utilized to guide decision-making. Focus was placed on optimal needle agitation techniques and the management of anatomical challenges.",
            3: "Service: Diagnostic Bronchoscopy (31622).\nRole: Teaching physician present/supervising.\nDetails: Evaluation of mediastinal lymph nodes via EBUS approach. Nodal stations assessed systematically. ROSE employed for adequacy. Fellow performed needle passes under direct supervision.",
            4: "Procedure: Bronchoscopy with EBUS (Teaching)\nAttending: [Name]\nFellow: [Name]\nSteps:\n1. Moderate sedation (Versed/Fentanyl).\n2. Scope passed vocal cords.\n3. Systematic EBUS exam performed (N3 to N1).\n4. ROSE tech reviewed slides.\n5. Fellow performed needle passes.\n6. Scope removed.\nPlan: Recover.",
            5: "teaching case for lul adeno staging. donald martinez. fellow did the ebus part looking at the nodes n3 to n1. we looked at the rose slides as we went. worked on needle technique. patient did fine with the versed and fentanyl.",
            6: "TEACHING CASE - BRONCHOSCOPY WITH FELLOW PARTICIPATION. Patient: Donald Martinez. INDICATION: Mediastinal staging, LUL adenocarcinoma. EDUCATIONAL OBJECTIVES: Systematic N3-N2-N1 EBUS evaluation, ROSE interpretation, Optimal needle pass technique. SEDATION: Moderate (midazolam 3mg, fentanyl 75mcg), Ramsay 3.",
            7: "[Indication]\nMediastinal staging, LUL adenocarcinoma.\n[Anesthesia]\nModerate sedation (Midazolam/Fentanyl).\n[Description]\nTeaching case. Systematic EBUS N3->N1 evaluation performed by fellow. Needle technique optimized. ROSE utilized for decision making.\n[Plan]\nPathology review.",
            8: "We performed a bronchoscopy on Mr. Martinez today for staging of his LUL adenocarcinoma. This was a teaching case where the fellow took the lead on the EBUS evaluation. We went through the nodes systematically from N3 to N1. The fellow practiced their needle technique, and we used ROSE to check the samples in real-time. Everything went smoothly.",
            9: "Operation: Educational Bronchoscopy.\nIndication: Staging of LUL neoplasm.\nAction: The fellow executed a methodical EBUS assessment (N3-N1). Needle aspiration technique was refined. ROSE was employed for immediate cytological interpretation.\nResult: Training objectives met."
        },
        1: { # Kevin Brown (Telephone Note/EBUS)
            1: "Indication: RUL Mass Staging.\nProc: EBUS-TBNA, Biopsy.\nFindings: 4R (+), 7 (+), 10R (-).\nActions:\n- EBUS-TBNA: 4R (4 passes), 7 (4 passes), 10R (3 passes).\n- Endobronchial biopsy RUL mass (6 samples).\nResult: N2 disease confirmed. Molecular sent.\nPlan: Oncology referral.",
            2: "PROCEDURE SUMMARY: The patient underwent EBUS-TBNA and endobronchial biopsy for staging of an RUL mass. EBUS evaluation of station 4R (12mm) and station 7 (15mm) yielded malignant cells (Adenocarcinoma) on ROSE. Station 10R was benign. The primary endobronchial mass was biopsied, yielding adequate diagnostic tissue. Findings are consistent with N2 disease. Molecular profiling has been initiated.",
            3: "Codes: 31653 (EBUS 3 stations), 31625 (Endobronchial Biopsy).\nStations Sampled: 4R, 7, 10R.\nBiopsy Site: RUL endobronchial mass.\nPathology: 4R/7 Positive for Adenocarcinoma. 10R Benign.\nNotes: Systematic staging performed. Molecular testing requested.",
            4: "Procedure: EBUS-TBNA & Biopsy\nPatient: Kevin Brown\nSteps:\n1. Mod sedation.\n2. EBUS scope inserted.\n3. Sampled 4R (4 passes, Pos).\n4. Sampled 7 (4 passes, Pos).\n5. Sampled 10R (3 passes, Neg).\n6. Biopsied RUL mass (6 bites).\n7. Photos taken.\nPlan: Tumor board.",
            5: "called dr adams about kevin brown. we did the ebus today. 4r and 7 were hot on rose looks like adeno. 10r was negative. took some bites of the rul mass too. n2 disease for sure. sent off for molecular. patient is fine going home.",
            6: "TELEPHONE CONSULTATION PROCEDURE NOTE. Patient Kevin Brown. 66M with RUL mass. EBUS RESULTS: Station 4R (12mm) ROSE positive, Station 7 (15mm) ROSE positive, Station 10R (8mm) ROSE benign. TUMOR BIOPSY: Primary RUL endobronchial component biopsied. STAGING: N2 disease confirmed. Molecular testing sent. COMPLICATIONS: None.",
            7: "[Indication]\nRUL mass, mediastinal staging.\n[Anesthesia]\nModerate (Midazolam/Fentanyl).\n[Description]\nEBUS-TBNA performed. Station 4R & 7 positive for Adeno. Station 10R benign. RUL mass biopsied (forceps). N2 disease confirmed.\n[Plan]\nTumor board, Molecular results.",
            8: "I called Dr. Adams to give a quick update on Mr. Brown's procedure. We did the EBUS and biopsy today. It looks like N2 disease; stations 4R and 7 were positive for adenocarcinoma on the rapid onsite check. Station 10R was negative. We also grabbed about 6 biopsies of the main mass in the right upper lobe. We've sent the samples for molecular testing.",
            9: "Procedure: EBUS-TBNA and endobronchial sampling.\nDiagnosis: RUL neoplasm.\nTechnique: Aspiration of nodes 4R, 7, and 10R. Forceps sampling of endobronchial lesion.\nFindings: Stations 4R and 7 revealed malignancy. 10R was benign.\nOutcome: N2 stage verification."
        },
        2: { # Nancy Rodriguez (EBUS 3 stations)
            1: "Indication: RLL Adeno Staging.\nProc: EBUS-TBNA.\nActions:\n- 4R: 4 passes, Pos.\n- 7: 4 passes, Pos.\n- 10R: 3 passes, Benign.\n- Systematic N3-N1 exam.\nResult: N2 disease confirmed.\nPlan: MDT.",
            2: "OPERATIVE REPORT: EBUS-TBNA was performed for staging of Right Lower Lobe Adenocarcinoma. A systematic N3-N2-N1 evaluation was conducted. Station 4R (13mm) and Station 7 (19mm) were sampled (4 passes each) and found to be malignant on ROSE. Station 10R was sampled and was benign. Findings confirm multi-station N2 involvement.",
            3: "CPT: 31653 (EBUS-TBNA >= 3 stations).\nStations: 4R, 7, 10R.\nMethod: Needle aspiration under ultrasound guidance.\nResults: 4R/7 Malignant, 10R Benign.\nNote: Molecular testing initiated.",
            4: "Procedure: EBUS Staging\nPatient: Nancy Rodriguez\nSteps:\n1. Sedation start.\n2. EBUS scope in.\n3. Sampled 4R: Positive.\n4. Sampled 7: Positive.\n5. Sampled 10R: Benign.\n6. Photos taken.\nPlan: Discuss neoadjuvant therapy.",
            5: "nancy rodriguez here for staging rll cancer. we did the ebus. hit 4r and 7 both looked malignant on rose. 10r was okay. systematic check done. n2 disease. patient vitals stable throughout.",
            6: "PROCEDURAL FLEXIBLE BRONCHOSCOPY WITH EBUS-TBNA. PATIENT: Nancy Rodriguez. CLINICAL INDICATION: Mediastinal staging for RLL adenocarcinoma. EBUS-TBNA FINDINGS: Station 4R (4 passes, ROSE Positive). Station 7 (4 passes, ROSE Positive). Station 10R (3 passes, ROSE Benign). DIAGNOSTIC IMPRESSION: N2 disease confirmed.",
            7: "[Indication]\nMediastinal staging, RLL Adenocarcinoma.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA of stations 4R, 7, 10R. 4R and 7 positive for malignancy. 10R benign. Systematic evaluation complete.\n[Plan]\nMDT discussion.",
            8: "We performed an EBUS procedure on Ms. Rodriguez to stage her lung cancer. We sampled three stations: 4R, 7, and 10R. Unfortunately, both the 4R and 7 nodes came back positive for malignancy, which confirms N2 disease. Station 10R appeared benign. We've sent the tissue for further testing and will bring this to the multidisciplinary team.",
            9: "Operation: EBUS-guided needle aspiration.\nIndication: Staging of RLL carcinoma.\nStations Sampled: 4R, 7, 10R.\nFindings: Malignancy identified in 4R and 7. Station 10R was negative.\nConclusion: Multi-station N2 involvement established."
        },
        3: { # Paul Anderson (Navigational Bronch)
            1: "Indication: RUL Nodule (19mm).\nProc: Nav Bronch, Radial EBUS.\nActions:\n- EM Nav to RUL posterior.\n- REBUS: Concentric view.\n- TBNA x2, Forceps x4, Brush x2.\n- CBCT: No pneumo.\nResult: Tool-in-lesion confirmed.",
            2: "PROCEDURE NOTE: Navigational bronchoscopy was performed for a 19mm RUL nodule. Using Cone Beam CT (CBCT) and Electromagnetic Navigation (EMN), the lesion was targeted. Radial EBUS confirmed a concentric view. Diagnostic sampling included transbronchial needle aspiration (x2), forceps biopsy (x4), and brush cytology (x2). Post-procedure CBCT ruled out pneumothorax.",
            3: "Codes: 31627 (Nav), 31654 (REBUS), 31629 (TBNA), 31628 (Biopsy), 31623 (Brush - usually bundled).\nTarget: RUL Peripheral Nodule.\nTech: EM Nav + CBCT + Radial EBUS.\nSamples: TBNA x2, Biopsy x4, Brush x2.",
            4: "Procedure: Navigational Bronchoscopy\nPatient: Paul Anderson\nSteps:\n1. Deep sedation/LMA.\n2. Registered EM map.\n3. Navigated to RUL nodule.\n4. Radial EBUS confirmed position.\n5. Took needle, forcep, and brush samples.\n6. Spin CT to check placement and pneumo.\nPlan: Discharge.",
            5: "paul anderson for the rul nodule. used the super dimension or whatever nav system we have plus the cone beam. found the spot in the posterior segment. radial ebus was concentric perfect. took needle biopsies forceps and brush. checked with the spin at the end no pneumo. patient good.",
            6: "Name: Paul Anderson. Indication: RUL peripheral nodule 19mm. Technology: Cone beam CT, EM navigation. Procedure: Target RUL posterior segment. Radial EBUS Concentric. Samples: Needle aspiration x2, Forceps biopsy x4, Brush cytology x2. Tool-in-lesion: CONFIRMED. Post-procedure CBCT: No pneumothorax.",
            7: "[Indication]\nRUL nodule, 19mm.\n[Anesthesia]\nDeep (Propofol).\n[Description]\nEM Nav and CBCT used to locate lesion. Radial EBUS concentric. TBNA x2, Forceps x4, Brush x2 performed. Tool-in-lesion confirmed.\n[Plan]\nDischarge.",
            8: "We used the navigation system and the cone-beam CT to biopsy Mr. Anderson's lung nodule. We found the 19mm spot in the right upper lobe. The radial EBUS probe showed we were right in the middle of it. We took needle samples, forceps biopsies, and some brushings. A final scan showed no collapsed lung, and he's recovering well.",
            9: "Procedure: Electromagnetic navigational bronchoscopy with peripheral localization.\nTarget: RUL pulmonary nodule.\nTechnique: CBCT registration. Radial EBUS confirmation. Sampling via aspiration, forceps extraction, and cytology brushing.\nOutcome: Successful localization, no pneumothorax."
        },
        4: { # William Taylor (Data Table - Nav/REBUS)
            1: "Indication: LLL Nodule (16mm).\nProc: EM Nav, Radial EBUS.\nActions:\n- Navigated to LLL superior.\n- REBUS: Concentric.\n- Needle x3, Forceps x4, Brush x2.\nResult: Localization successful. No pneumo.",
            2: "OPERATIVE REPORT: The patient underwent electromagnetic navigational bronchoscopy for a 16mm peripheral LLL nodule. Localization was confirmed via Radial EBUS (concentric view). Sampling was performed utilizing transbronchial needle aspiration (x3), forceps biopsy (x4), and brush cytology (x2). Fluoroscopy time was 4.7 minutes. No complications occurred.",
            3: "Codes: 31627 (Nav), 31654 (REBUS), 31629 (TBNA), 31628 (Biopsy).\nTarget: LLL Superior Segment.\nTechnique: EM Nav + Radial EBUS.\nSamples: TBNA x3, Forceps x4, Brush x2.\nOutcome: Successful localization.",
            4: "Procedure: Nav Bronch\nPatient: William Taylor\nSteps:\n1. Deep sedation/LMA.\n2. Navigated to LLL target.\n3. Confirmed with Radial EBUS.\n4. Samples: Needle x3, Forceps x4, Brush x2.\n5. Fluoro check.\nPlan: Monitor for pneumo.",
            5: "william taylor lll nodule. em nav worked well got right to the superior segment. radial ebus confirmed it. did 3 needle passes 4 biopsies and 2 brushes. no bleeding no pneumo on the fluoro. patient stable.",
            6: "PATIENT: William Taylor. PROCEDURE: 10/20/2024. INDICATION: Peripheral LLL nodule 16mm. NAVIGATION: Electromagnetic system. Target: LLL superior segment. Tool-in-Lesion: Confirmed (radial EBUS concentric). SAMPLES: Needle aspirate 3, Forceps biopsy 4, Brush cytology 2. OUTCOME: Localization Success YES. Complications None.",
            7: "[Indication]\nLLL Nodule, 16mm.\n[Anesthesia]\nDeep (Propofol).\n[Description]\nEM Navigation to LLL. Radial EBUS concentric. Samples: TBNA x3, Forceps x4, Brush x2.\n[Plan]\nNo pneumothorax noted.",
            8: "Mr. Taylor had a 16mm nodule in his left lower lobe. We used the electromagnetic navigation system to guide our instruments to the spot. We confirmed we were in the right place with the radial ultrasound probe. We took plenty of samples including needle aspirates, forceps biopsies, and brushings. He tolerated it well with no complications.",
            9: "Procedure: Electromagnetic guided bronchoscopy.\nFindings: 16mm LLL lesion.\nIntervention: Radial EBUS localization. Transbronchial aspiration, forceps excision, and brushings.\nResult: Successful target acquisition."
        },
        5: { # Michael Torres (Extensive Staging)
            1: "Indication: Centrally located NSCLC staging.\nProc: EBUS-TBNA.\nActions:\n- Sampled 2R, 4R, 4L, 7, 10R.\n- All stations PET+ and ROSE+.\nResult: Extensive N2/N3 disease.\nPlan: Molecular testing.",
            2: "PROCEDURE NOTE: Endobronchial ultrasound (EBUS) was performed for staging of central NSCLC. A systematic evaluation revealed extensive mediastinal involvement. Transbronchial needle aspiration (TBNA) was performed at stations 2R, 4R, 4L, 7, and 10R. Rapid On-Site Evaluation (ROSE) confirmed malignancy in all sampled stations, indicating N3 disease. Molecular panels were requested.",
            3: "Codes: 31653 (EBUS-TBNA 3+ stations).\nStations: 2R, 4R, 4L, 7, 10R.\nFindings: Malignancy confirmed in all 5 stations.\nNote: High complexity staging. Photodocumentation archived.",
            4: "Procedure: EBUS Staging\nPatient: Michael Torres\nSteps:\n1. Mod sedation.\n2. Systematic EBUS.\n3. Sampled 2R, 4R, 4L, 7, 10R.\n4. All came back positive on ROSE.\n5. Molecular sent from 4R/7.\nPlan: Oncology.",
            5: "michael torres has central lung cancer. we did a full court press on the ebus. hit 2r 4r 4l 7 and 10r. everything was positive on rose. n3 disease basically everywhere. sent for molecular. patient stable.",
            6: "Pt: Michael Torres. CLINICAL: Staging centrally located NSCLC. EBUS-TBNA findings: Station 2R (PET+, ROSE+), Station 4R (PET+, ROSE+), Station 4L (PET+, ROSE+), Station 7 (PET+, ROSE+), Station 10R (PET+, ROSE+). IMPRESSION: Extensive N2/N3 disease confirmed. Molecular testing sent.",
            7: "[Indication]\nCentrally located NSCLC.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA of 5 stations: 2R, 4R, 4L, 7, 10R. All positive for malignancy. N3 disease confirmed.\n[Plan]\nMolecular characterization.",
            8: "We performed an extensive staging EBUS on Mr. Torres. His cancer is centrally located, and unfortunately, we found spread to multiple lymph node stations. We sampled 2R, 4R, 4L, 7, and 10R, and every single one was positive for malignancy. This confirms N3 disease. We made sure to get enough tissue for genetic testing.",
            9: "Procedure: Multi-station EBUS-TBNA.\nDiagnosis: Central NSCLC.\nSampling: Stations 2R, 4R, 4L, 7, 10R underwent aspiration.\nFindings: Cytological evidence of malignancy in all sampled nodes.\nOutcome: N3 stage verification."
        },
        6: { # Maria Rodriguez (Sarcoid vs Lymphoma)
            1: "Indication: Bilateral adenopathy (Sarcoid vs Lymphoma).\nProc: EBUS-TBNA.\nActions:\n- Sampled 4R, 4L, 7, 11R.\n- ROSE: Granulomas (Sarcoid).\n- Flow cytometry sent.\nResult: Consistent with Sarcoidosis.",
            2: "OPERATIVE REPORT: The patient presented with bilateral hilar lymphadenopathy. EBUS-TBNA was performed to differentiate between sarcoidosis and lymphoma. Samples were obtained from stations 4R, 4L, 7, and 11R. On-site evaluation revealed non-necrotizing granulomas consistent with sarcoidosis. Samples were also sent for flow cytometry and culture to rule out other etiologies.",
            3: "Code: 31653 (EBUS 3+ stations).\nStations: 4R, 4L, 7, 11R.\nPathology: Granulomatous inflammation (Sarcoid). \nTesting: Flow cytometry and Microbiology sent to rule out Lymphoma/Infection.",
            4: "Procedure: EBUS\nPatient: Maria Rodriguez\nSteps:\n1. Conscious sedation.\n2. Sampled 4R, 4L, 7, 11R.\n3. ROSE showed granulomas.\n4. Sent for flow and culture just in case.\nPlan: Home.",
            5: "maria rodriguez 53f lymph nodes up everywhere. sarcoid vs lymphoma. did ebus 4r 4l 7 11r. rose said granulomas so probably sarcoid. sent flow cytometry anyway. patient tolerated well.",
            6: "Patient Name: Maria Rodriguez. Clinical context: Bilateral hilar lymphadenopathy. EBUS-TBNA performed: Station 4R (ROSE non-necrotizing granulomas), Station 4L (ROSE granulomatous), Station 7 (ROSE similar), Station 11R (ROSE adequate). Assessment: Adequate tissue obtained for sarcoidosis vs lymphoma differentiation.",
            7: "[Indication]\nBilateral hilar lymphadenopathy.\n[Anesthesia]\nConscious sedation.\n[Description]\nEBUS-TBNA stations 4R, 4L, 7, 11R. Findings: Non-necrotizing granulomas. Flow cytometry sent.\n[Plan]\nConfirm Sarcoidosis.",
            8: "Ms. Rodriguez has swollen lymph nodes on both sides of her chest. We did an EBUS to see if it was sarcoidosis or lymphoma. We sampled four different areas: 4R, 4L, 7, and 11R. The preliminary results show granulomas, which points strongly to sarcoidosis. We sent extra samples for flow cytometry just to be 100% sure it's not lymphoma.",
            9: "Procedure: Endobronchial ultrasound-guided aspiration.\nIndication: Bilateral lymphadenopathy evaluation.\nSampling: Nodes 4R, 4L, 7, 11R.\nFindings: Cytology demonstrated granulomatous inflammation.\nConclusion: Findings favor sarcoidosis."
        },
        7: { # George Martinez (Staging - Extra passes 4R)
            1: "Indication: RUL NSCLC Staging.\nProc: EBUS-TBNA.\nActions:\n- 4R: 5 passes (Benign).\n- 7: 3 passes (Malignant).\n- 11R: 3 passes (Benign).\nResult: N2 disease (Station 7).\nPlan: Molecular testing.",
            2: "PROCEDURE NOTE: Mediastinal staging was performed for RUL NSCLC. Station 4R required 5 passes to achieve adequacy and was found to be benign. Station 7 was PET-positive and confirmed malignant on ROSE. Station 11R was benign. N2 disease is confirmed based on Station 7 involvement.",
            3: "Code: 31653 (EBUS 3+ stations).\nStations: 4R, 7, 11R.\nDetails: 4R required multiple passes for ROSE adequacy. 7 was malignant. 11R benign.\nOutcome: N2 Staging.",
            4: "Procedure: EBUS Staging\nPatient: George Martinez\nSteps:\n1. Mod sedation.\n2. 4R: Hard to get cells, took 5 passes. Benign.\n3. 7: Malignant right away.\n4. 11R: Benign.\n5. Molecular sent from #7.\nPlan: N2 disease management.",
            5: "george martinez staging for rul cancer. 4r gave us trouble had to pass the needle 5 times to get good cells but it was benign. 7 was positive for cancer. 11r was negative. so he has n2 disease. sent tissue for testing.",
            6: "Name: George Martinez. INDICATION: Mediastinal staging, RUL NSCLC. EBUS-TBNA performed: Station 4R (5 passes needed, ROSE benign). Station 7 (ROSE positive malignancy). Station 11R (ROSE adequate benign). Impression: N2 disease confirmed (station 7).",
            7: "[Indication]\nRUL NSCLC Staging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA. Station 4R (Benign, 5 passes). Station 7 (Malignant). Station 11R (Benign). N2 disease confirmed.\n[Plan]\nMolecular testing.",
            8: "We staged Mr. Martinez's lung cancer today. We had a bit of trouble with station 4R; it took 5 passes to get a good sample, but it turned out to be benign. Station 7, however, was clearly malignant. Station 11R was benign. This confirms he has N2 disease. We sent the tissue from station 7 for genetic profiling.",
            9: "Procedure: Systematic EBUS-TBNA.\nIndication: Staging of pulmonary carcinoma.\nSampling: Station 4R (benign lymphocytes), Station 7 (malignant cells), Station 11R (benign).\nNote: Extended sampling required for 4R adequacy.\nResult: N2 nodal involvement verified."
        }
    }
    return variations

def get_base_data_mocks():
    return [
        {"idx": 0, "orig_name": "Donald Martinez", "orig_age": 68, "names": ["Robert Hughes", "James Wallace", "John Bryant", "William Webb", "Richard Hayes", "Joseph Richardson", "Charles Russell", "Thomas Griffin", "Christopher Diaz"]},
        {"idx": 1, "orig_name": "Kevin Brown", "orig_age": 66, "names": ["Daniel West", "Matthew Jordan", "Anthony Hamilton", "Donald Graham", "Mark Kim", "Paul Coleman", "Steven Jenkins", "Andrew Perry", "Kenneth Powell"]},
        {"idx": 2, "orig_name": "Nancy Rodriguez", "orig_age": 69, "names": ["Linda Long", "Barbara Patterson", "Elizabeth Hughes", "Jennifer Flores", "Maria Washington", "Susan Butler", "Margaret Simmons", "Dorothy Foster", "Lisa Gonzales"]},
        {"idx": 3, "orig_name": "Paul Anderson", "orig_age": 63, "names": ["George Bryant", "Edward Alexander", "Brian Russell", "Ronald Griffin", "Timothy Diaz", "Jason Hayes", "Jeffrey Myers", "Ryan Ford", "Gary Hamilton"]},
        {"idx": 4, "orig_name": "William Taylor", "orig_age": 65, "names": ["Stephen Graham", "Larry Sullivan", "Scott Wallace", "Frank Woods", "Justin Cole", "Brandon West", "Raymond Jordan", "Gregory Owens", "Samuel Reynolds"]},
        {"idx": 5, "orig_name": "Michael Torres", "orig_age": 64, "names": ["Patrick Fisher", "Jack Ellis", "Dennis Harrison", "Jerry Gibson", "Tyler McDonald", "Aaron Cruz", "Jose Marshall", "Adam Ortiz", "Nathan Gomez"]},
        {"idx": 6, "orig_name": "Maria Rodriguez", "orig_age": 53, "names": ["Helen Murray", "Deborah Freeman", "Sandra Wells", "Carol Webb", "Amanda Simpson", "Stephanie Stevens", "Melissa Tucker", "Rebecca Porter", "Laura Hunter"]},
        {"idx": 7, "orig_name": "George Martinez", "orig_age": 68, "names": ["Douglas Hicks", "Peter Crawford", "Harold Boyd", "Kyle Mason", "Walter Morales", "Keith Kennedy", "Jeremy Warren", "Terry Dixon", "Lawrence Ramos"]}
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
                note_entry["note_text"] = f"VARIATION MISSING for Note {idx} Style {style_num}"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]: # Some might not have age field
                     note_entry["registry_entry"]["patient_age"] = new_age
                
                # Update procedure_date
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
    output_filename = output_dir / "synthetic_blvr_notes_part_042.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()