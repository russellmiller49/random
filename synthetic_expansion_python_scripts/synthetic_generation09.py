import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_009.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Provides mock names and base ages for the 5 patients in the source file.
    Indexes 0-4 correspond to the 5 notes in bronch_notes_part_009.json.
    """
    return [
        { # Note 0: EBUS 4R (Granuloma)
            "idx": 0, 
            "orig_age": 55, # Placeholder, will be adjusted
            "names": [
                "James Thayer", "Robert C. Miller", "Arthur Vandelay", 
                "Kevin O'Shea", "Bill Henderson", "Marcus Wright", 
                "Thomas Anderson", "Richard Blaine", "Henry Chin"
            ]
        },
        { # Note 1: EBUS 7 + Research Biopsies
            "idx": 1, 
            "orig_age": 62, 
            "names": [
                "Sarah Connor", "Ellen Ripley", "Diana Prince", 
                "Natasha Romanoff", "Leia Organa", "Dana Scully", 
                "Clarice Starling", "Beatrix Kiddo", "Laurie Strode"
            ]
        },
        { # Note 2: EBUS RLL Nodule (Lung mass)
            "idx": 2, 
            "orig_age": 68, 
            "names": [
                "Frank Castle", "Bruce Wayne", "Clark Kent", 
                "Peter Parker", "Tony Stark", "Steve Rogers", 
                "Bruce Banner", "Matt Murdock", "Wade Wilson"
            ]
        },
        { # Note 3: Navigational Bronch Lingula
            "idx": 3, 
            "orig_age": 45, 
            "names": [
                "Walter White", "Jesse Pinkman", "Saul Goodman", 
                "Mike Ehrmantraut", "Gustavo Fring", "Hank Schrader", 
                "Skyler White", "Marie Schrader", "Lydia Rodarte-Quayle"
            ]
        },
        { # Note 4: Complex EBUS + RML + Complications
            "idx": 4, 
            "orig_age": 72, 
            "names": [
                "Homer Simpson", "Ned Flanders", "Barney Gumble", 
                "Seymour Skinner", "Clancy Wiggum", "Moe Szyslak", 
                "Waylon Smithers", "Montgomery Burns", "Apu Nahasapeemapetilon"
            ]
        }
    ]

def get_variations():
    """
    Returns the 9 stylistic variations for each of the 5 notes.
    Keys map to the note index in the original list.
    """
    variations = {
        0: { # Note 0: EBUS 4R (Granuloma)
            1: "Indication: Mediastinal adenopathy.\nProcedure: EBUS-TBNA 4R.\nAction: LMA placed. EBUS scope to 4R. 19G needle x7 passes. Mini-forceps bx via needle tract x2.\nResult: ROSE negative for malignancy. Forceps touchprep: Abundant non-caseating granulomas.\nComplications: None. EBL 5cc.\nPlan: Recovery.",
            2: "OPERATIVE REPORT\n\nINDICATION: The patient presented with mediastinal lymphadenopathy requiring tissue diagnosis.\n\nPROCEDURE: Following induction of general anesthesia, a systematic endobronchial ultrasound examination was conducted utilizing a UC180F convex probe. The tracheobronchial tree was anatomically unremarkable. Attention was directed to station 4R, where a prominent lymph node was visualized. Transbronchial needle aspiration (TBNA) utilizing a 19-gauge Olympus Visioshot needle was performed for a total of seven passes. Additionally, intranodal forceps biopsies were obtained by advancing Olympus mini-forceps through the needle tract under real-time sonographic guidance. Rapid On-Site Evaluation (ROSE) of the forceps samples demonstrated abundant non-caseating granulomas consistent with a granulomatous etiology.\n\nCONCLUSION: Successful EBUS-TBNA and intranodal forceps biopsy of station 4R.",
            3: "Service: Bronchoscopy with EBUS sampling (CPT 31652).\nTarget: Single nodal station (4R).\nTechnique: Linear EBUS guidance used for needle aspiration (19G) and subsequent intranodal forceps biopsy through the same tract.\nMedical Necessity: Diagnosis of mediastinal adenopathy.\nDocumentation of Effort: 7 needle passes and 2 forceps passes were required to obtain adequate tissue, confirmed by ROSE as non-caseating granulomas.",
            4: "Procedure Note\nAttending: Dr. X\nResident: Dr. Y\n\nProcedure: EBUS-TBNA\n\nSteps:\n1. Time out performed.\n2. General anesthesia induced.\n3. Airway inspection with Q190: Normal.\n4. EBUS scope introduced. Station 4R identified.\n5. TBNA x 7 passes using 19G needle.\n6. Mini-forceps biopsy performed through needle tract under ultrasound guidance.\n7. ROSE confirms granulomas.\n8. Scope removed. Patient stable.",
            5: "pt here for lymph nodes mediastinum we put him to sleep lma used. went down with the q190 looks ok normal airway then switched to the ebus scope found a big node at 4r. stuck it 7 times with the 19 gauge needle rose was just lymphocytes so we used the mini forceps through the hole made by the needle grabbed some tissue twice. path said granulomas non caseating so we stopped. sucked out a little blood 5cc maybe. patient woke up fine sent to pacu.",
            6: "Mediastinal adenopathy evaluation. General anesthesia. Airway inspection via LMA with video bronchoscope revealed normal anatomy. EBUS scope inserted. Station 4R lymph node sampled via TBNA (7 passes, 19G needle) and intranodal mini-forceps biopsy. Ultrasound visualization confirmed forceps placement within the node. Pathology onsite evaluation revealed scattered lymphocytes on needle aspirate but abundant non-caseating granulomas on forceps touchpreps. Procedure concluded with no complications.",
            7: "[Indication]\nMediastinal adenopathy.\n\n[Anesthesia]\nGeneral, LMA.\n\n[Description]\nDiagnostic bronchoscopy: Normal anatomy. EBUS bronchoscopy: Station 4R identified. Interventions: 19G TBNA x7 passes and intranodal mini-forceps biopsy x2. Findings: ROSE confirmed non-caseating granulomas.\n\n[Plan]\nAwait final pathology.",
            8: "The patient was brought to the endoscopy suite for evaluation of mediastinal adenopathy. After the induction of general anesthesia, we proceeded with a comprehensive airway exam which was unremarkable. We then utilized the convex EBUS scope to localize station 4R. We performed extensive sampling using a 19-gauge needle followed by a specialized mini-forceps technique through the needle tract. This yielded diagnostic material showing granulomas. The patient tolerated the procedure well.",
            9: "Indication: Mediastinal adenopathy.\nProcedure: EBUS bronchoscopy.\nTechnique: The airway was surveyed with a video bronchoscope; no anomalies detected. The EBUS scope was deployed. Station 4R was targeted. We harvested tissue using a 19G needle (7 passes) and subsequently retrieved core tissue using mini-forceps via the needle track. ROSE verified non-caseating granulomas. No adverse events occurred."
        },
        1: { # Note 1: EBUS 7 + Research
            1: "Indication: Adenopathy.\nProcedure: EBUS-TBNA St 7 + Research Biopsies.\nFindings: Station 7 malignant (ROSE).\nActions:\n- EBUS TBNA St 7 (22G, 7 passes).\n- Research biopsies: Forceps to RUL, RML, LUL.\n- Research brush: Bronchus Intermedius.\nComplications: None.\nPlan: Cytology/Flow.",
            2: "OPERATIVE NARRATIVE: The patient underwent EBUS bronchoscopy for evaluation of mediastinal adenopathy under general anesthesia. Airway inspection was unremarkable. The EBUS scope was utilized to identify a large subcarinal (Station 7) lymph node. Transbronchial needle aspiration (22G) was performed, yielding malignant cells on rapid on-site evaluation. Following the diagnostic portion, the patient participated in the DECAMP research protocol. This involved endobronchial forceps biopsies of the RUL, RML, and LUL carinas, as well as brushing of the bronchus intermedius. Hemostasis was achieved.",
            3: "Coding Summary:\n- 31652: EBUS-TBNA of 1 station (Station 7). 7 passes, confirmed malignant.\n- 31625: Endobronchial biopsy(s) performed in RUL, RML, LUL (Research protocol).\n- 31623: Endobronchial brushing performed in Bronchus Intermedius (Research protocol).\nNote: Diagnostic bronchoscopy (31622) is bundled.",
            4: "Resident Procedure Note\n\n1. General Anesthesia/LMA.\n2. Diagnostic bronchoscopy: Normal.\n3. EBUS: Station 7 sampled (7 passes, 22G). ROSE positive for malignancy.\n4. Protocol Biopsies (DECAMP): Forceps bx of RUL, RML, LUL.\n5. Protocol Brush: Bronchus Intermedius.\n6. Patient stable to PACU.",
            5: "doing ebus for mediastinal nodes pt under general. looked with regular scope first normal then ebus. found big station 7 node stuck it 7 times with 22g needle path said cancer. sent for flow too. then did the research stuff decamp protocol took bites of rul rml and lul and brushed the bronchus intermedius. no bleeding stopped fine. patient to recovery.",
            6: "Mediastinal adenopathy. General anesthesia. Inspection revealed normal airway. EBUS TBNA performed on Station 7 (subcarinal) with 22G needle, 7 passes. ROSE: Malignant. DECAMP research protocol followed: Endobronchial forceps biopsies of RUL, RML, LUL and brushing of bronchus intermedius. Minimal bleeding. Stable transfer.",
            7: "[Indication]\nMediastinal adenopathy.\n\n[Anesthesia]\nGeneral.\n\n[Description]\nEBUS-TBNA performed on Station 7 (Malignant on ROSE). Research procedures performed: Endobronchial biopsies (RUL, RML, LUL) and Brushing (Bronchus Intermedius).\n\n[Plan]\nPathology pending.",
            8: "We performed an EBUS bronchoscopy on this patient for mediastinal staging. Upon entering the airway with the EBUS scope, we identified a large lymph node at station 7. We sampled this using a 22-gauge needle, and the onsite pathologist confirmed malignancy. Following the standard of care procedure, we proceeded with the DECAMP research protocol, which entailed taking forceps biopsies from the right upper, right middle, and left upper lobes, along with a brushing of the bronchus intermedius. The patient tolerated both the diagnostic and research components well.",
            9: "Indication: Mediastinal adenopathy.\nProcedure: EBUS with ancillary research sampling.\nDetails: The airway was visualized. Station 7 was interrogated via EBUS-TBNA; malignancy was confirmed. Subsequently, we acquired tissue from the RUL, RML, and LUL via forceps and harvested cells from the bronchus intermedius via brush for the DECAMP protocol. No complications."
        },
        2: { # Note 2: EBUS RLL Nodule (Lung Mass)
            1: "Indication: Suspected lung ca.\nProcedure: EBUS-TBNA RLL nodule.\nFindings: Systemic LN survey negative (<5mm). 11.4mm hypoechoic nodule in RLL.\nAction: 22G TBNA x9 passes to RLL mass.\nResult: Malignant (ROSE).\nComplications: None.",
            2: "PROCEDURE: Bronchoscopy with Endobronchial Ultrasound (EBUS).\nFINDINGS: A systematic mediastinal and hilar lymph node survey was conducted; however, no lymph nodes met the size criteria for sampling. The EBUS scope was advanced distally into the Right Lower Lobe (RLL), identifying an 11.4mm hypoechoic parenchymal nodule. Transbronchial needle aspiration (TBNA) was performed on this target using a 22-gauge needle. Rapid on-site evaluation confirmed malignancy. The bronchial stumps from prior resections were intact.",
            3: "Billing Justification:\n- CPT 31652: EBUS guided TBNA of 1 structure. NOTE: Target was a parenchymal nodule in the RLL, not a lymph node station, as nodal survey was negative. \n- 9 passes performed to ensure diagnostic yield.\n- General anesthesia used.",
            4: "Procedure: EBUS-TBNA\nTarget: RLL Nodule\n\nSteps:\n1. LMA/GA.\n2. Diagnostic: RUL/RML stumps intact.\n3. EBUS Survey: Negative for adenopathy.\n4. RLL Nodule localized (11.4mm).\n5. TBNA x9 passes.\n6. ROSE: Positive for malignancy.",
            5: "patient here for staging lung cancer. gave general anesthesia. looked around first airway ok old stumps from surgery look fine. did the ebus survey but didnt find any big nodes to sample. went down to the rll found the nodule it was like 11mm. stuck it 9 times with the 22 gauge. cytology said its cancer. no bleeding patient fine.",
            6: "Mediastinal staging and diagnosis. General anesthesia. Airway exam normal; prior RUL/RML resection stumps intact. Systematic EBUS nodal survey negative (all <5mm). EBUS probe advanced to RLL where 11.4mm hypoechoic nodule visualized. TBNA performed (9 passes, 22G). ROSE confirmed malignancy. No complications.",
            7: "[Indication]\nSuspected lung malignancy.\n\n[Anesthesia]\nGeneral.\n\n[Description]\nSystematic EBUS LN survey negative. 11.4mm RLL nodule identified via EBUS. TBNA x9 performed. ROSE: Malignant.\n\n[Plan]\nOncology referral.",
            8: "We brought the patient back for staging and diagnosis of a suspected lung cancer. Despite a thorough search of the mediastinum and hilum with the EBUS scope, no enlarged lymph nodes were found. We successfully navigated the EBUS scope into the right lower lobe to visualize the primary 11.4mm nodule. We obtained nine needle passes from this mass. The preliminary read from pathology is positive for malignancy.",
            9: "Indication: Diagnosis of pulmonary malignancy.\nProcedure: EBUS-guided sampling.\nDetails: Nodal stations were inspected but lacked sampling criteria. The RLL parenchymal lesion was visualized sonographically. We performed aspiration (9 passes) yielding malignant cells. Airway stumps from prior surgeries were unremarkable."
        },
        3: { # Note 3: Nav Lingula
            1: "Indication: Migratory nodules.\nProcedure: Navigational Bronchoscopy (SuperDimension).\nTargets: Left Lingula.\nAction:\n- BAL RUL Posterior.\n- Nav to Lingula (10mm divergence).\n- REBUS: Concentric view.\n- Fluoroscopy used.\n- Samples: TBNA, Brush, Forceps.\nResult: Histiocytes/Giant cells (ROSE).",
            2: "OPERATIVE REPORT: ELECTROMAGNETIC NAVIGATION BRONCHOSCOPY\n\nThe patient was intubated and placed under general anesthesia. A diagnostic inspection revealed thick secretions which were cleared. A bronchoalveolar lavage (BAL) was performed in the RUL posterior segment. Using the SuperDimension system, a pathway was mapped to the target lesion in the Left Lingula. Radial EBUS (REBUS) confirmed the catheter position with a concentric echotexture. Transbronchial needle aspiration, triple-needle brushing, and forceps biopsies were obtained under fluoroscopic guidance. ROSE suggested a granulomatous process (histiocytes/giant cells).",
            3: "CPT Coding:\n- 31629 (Primary): TBNA of Lingula lesion.\n- 31628: Transbronchial biopsy Lingula.\n- 31624: BAL (RUL Posterior - distinct lobe).\n- 31623: Brushing Lingula.\n- +31627: Navigation (SuperDimension).\n- +31654: Radial EBUS confirmation.",
            4: "Procedure Note: Nav Bronch\n\n1. ETT/GA.\n2. Diagnostic: Secretions suctioned.\n3. BAL: RUL posterior segment.\n4. Navigation: To Lingula lesion.\n5. Confirmation: Radial EBUS (Concentric).\n6. Sampling: TBNA, Brush, Forceps.\n7. ROSE: Granulomatous features.\n8. Fluoro time used.",
            5: "lung nodules moving around. ga with ett. looked in airways lots of mucus suctioned it out. did a bal in the rul posterior. then set up superdimension went to the lingula. found it with radial ultrasound concentric view. stuck it with needle then brush then forceps. rose guy said histiocytes giant cells. checked for bleeding none. cxr ordered.",
            6: "Migratory nodules. General anesthesia. Inspection: Thick secretions. BAL performed RUL posterior segment. SuperDimension navigation to Left Lingula. Radial EBUS confirmed concentric view. TBNA, brushing, and forceps biopsies performed under fluoroscopy. ROSE: Histiocytes and giant cells. No active bleeding.",
            7: "[Indication]\nMigratory lung nodules.\n\n[Anesthesia]\nGeneral.\n\n[Description]\nBAL RUL Posterior. Navigational bronchoscopy to Lingula. Radial EBUS confirmation. Biopsies: TBNA, Brush, Forceps.\n\n[Plan]\nCXR, Await pathology.",
            8: "The patient presented for evaluation of migratory lung nodules. After clearing secretions, we performed a BAL in the right upper lobe. We then utilized electromagnetic navigation to reach the target in the lingula. Location was verified with a concentric signal on radial EBUS. We obtained multiple samples using needle, brush, and forceps techniques. Preliminary pathology suggests a granulomatous etiology rather than malignancy.",
            9: "Indication: Pulmonary nodules.\nProcedure: Guided bronchoscopic sampling.\nDetails: Airways cleared of secretions. Lavage performed in RUL. Using electromagnetic guidance and radial ultrasound verification, we located the Lingular lesion. The target was sampled via needle aspiration, brushing, and biopsy forceps. Histology suggests benign granulomatous disease."
        },
        4: { # Note 4: Complex EBUS + RML + Complications
            1: "Indication: RML Nodule.\nProcedure: EBUS (11L, 7, 10R, 11R) + Ultrathin RML Biopsy.\nFindings: EBUS negative. RML nodule concentric on REBUS.\nComplications:\n- Aspiration/Emesis on emergence -> Hypoxia.\n- CXR: Small right apical pneumothorax.\nPlan: Admit. Monitor PTX and Aspiration.",
            2: "PROCEDURE NOTE: EBUS and Peripheral Bronchoscopy.\n\nFollowing systematic EBUS sampling of stations 11L, 7, 10R, and 11R (all ROSE negative), the EBUS scope was exchanged for an ultrathin bronchoscope. The Right Middle Lobe nodule was localized using radial EBUS (concentric view) and biopsied via needle, forceps, and brush. \n\nCOMPLICATIONS: Upon emergence, the patient had a large volume emesis with transient hypoxia, managed with positioning. Post-procedure CXR revealed airspace opacities consistent with aspiration or lavage, and a small right apical pneumothorax. The patient is hemodynamically stable.",
            3: "Billing Codes:\n- 31653: EBUS sampling 3+ stations (11L, 7, 10R, 11R).\n- 31628-XS: Transbronchial biopsy RML (separate site).\n- +31654: Radial EBUS for RML localization.\nNote: Complications (Pneumothorax J95.811, Aspiration J69.0) documented supporting medical necessity for admission.",
            4: "Resident Note\nPatient: [Name]\nProcedure: EBUS + RML Biopsy\n\n1. EBUS TBNA: 11L, 7, 10R, 11R.\n2. RML Nodule: Ultrathin scope + Radial EBUS + Bx (Needle/Brush/Forceps).\n3. Complication: Patient vomited on waking up, stats dropped. Also has small pneumo on CXR.\n4. Plan: Admit to medicine.",
            5: "doing staging for nodule. propofol anesthesia. ebus first hit 11l 7 10r 11r all negative. switched scopes went to rml found nodule with radial probe took biopsies. after we finished patient threw up everywhere maybe aspirated desatted for a bit. xray showed small pneumo on the right and some infiltrates. admitting for observation.",
            6: "Pulmonary nodule staging. General anesthesia. EBUS-TBNA performed on stations 11L, 7, 10R, and 11R (ROSE negative). Ultrathin bronchoscopy to RML nodule; Radial EBUS confirmed concentric view. Sampled with needle, forceps, brush. Post-procedure emesis with aspiration and hypoxia. CXR confirmed aspiration pneumonitis and small right apical pneumothorax. Admitted for observation.",
            7: "[Indication]\nPulmonary nodule.\n\n[Anesthesia]\nGeneral (Propofol).\n\n[Description]\nEBUS-TBNA: Stations 11L, 7, 10R, 11R. Peripheral Bronchoscopy: RML nodule (Radial EBUS confirmed). Biopsies taken.\n\n[Complications]\nAspiration event. Small right pneumothorax.\n\n[Plan]\nAdmit. Serial CXRs. Antibiotics held.",
            8: "This procedure was performed to stage a right middle lobe nodule. We started with a complete EBUS staging, sampling four distinct nodal stations, all of which were benign on rapid eval. We then navigated to the RML lesion using an ultrathin scope and radial ultrasound, obtaining good diagnostic samples. Unfortunately, the patient vomited during emergence, resulting in a likely aspiration event. Subsequent imaging also identified a small pneumothorax. He is stable but will be admitted for close monitoring.",
            9: "Indication: Nodule interrogation.\nProcedure: Multimodal bronchoscopy.\nDetails: EBUS-TBNA performed on four mediastinal/hilar stations. The RML target was located via radial sonography and sampled using diverse instruments. Post-intervention, the patient experienced emesis/aspiration and sustained a minor pneumothorax. He requires inpatient monitoring."
        }
    }
    return variations

def main():
    # Load original data
    source_path = Path(SOURCE_FILE)
    if not source_path.exists():
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return

    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON: {e}")
        return

    if not isinstance(source_data, list):
        print("Error: Source JSON must be a list of notes.")
        return

    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")

    # Prepare output directory
    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    base_mocks = get_base_data_mocks()
    variations_map = get_variations()
    generated_notes = []

    for idx, original_note in enumerate(source_data):
        if idx >= len(base_mocks):
            break
        
        mock_data = base_mocks[idx]
        orig_age = mock_data['orig_age']
        names_list = mock_data['names']
        
        # We generate 9 styles (1 through 9)
        for style_num in range(1, 10):
            note_copy = copy.deepcopy(original_note)
            
            # 1. Update Note Text
            # Retrieve the specific text variation
            if idx in variations_map and style_num in variations_map[idx]:
                note_copy["note_text"] = variations_map[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen with full map)
                note_copy["note_text"] = f"VARIATION_MISSING_FOR_NOTE_{idx}_STYLE_{style_num}"

            # 2. Update Patient Name (Metadata/Synthetic) & MRN
            new_name = names_list[style_num - 1]
            
            # 3. Update Age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # 4. Update Date (Random date in 2025)
            rand_date = generate_random_date(2025, 2025).strftime("%Y-%m-%d")

            # Apply changes to registry_entry if present
            if "registry_entry" in note_copy:
                re = note_copy["registry_entry"]
                
                # Update MRN
                old_mrn = re.get("patient_mrn", "UNKNOWN")
                re["patient_mrn"] = f"{old_mrn}_syn_{style_num}"
                
                # Update Date
                re["procedure_date"] = rand_date
                
                # Update Age (if field exists, though schema usually has specific demographics block)
                if "patient_demographics" in re and re["patient_demographics"]:
                    re["patient_demographics"]["age_years"] = new_age
                
                # Some schema versions might put age at root of registry_entry
                if "patient_age" in re:
                    re["patient_age"] = new_age

            # 5. Add Synthetic Metadata
            note_copy["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }

            generated_notes.append(note_copy)

    # Write output
    output_filename = out_dir / "synthetic_bronch_notes_part_009.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {len(generated_notes)} notes.")
    print(f"Output saved to: {output_filename}")

if __name__ == "__main__":
    main()