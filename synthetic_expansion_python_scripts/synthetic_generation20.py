import json
import random
import datetime
import copy
from pathlib import Path

# Source file containing the original verified notes
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_020.json"
# Output directory for the synthetic file
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the specified years."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    
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
        0: { # Note 0: RLL Tumor Debulking (Snare + APC)
            1: "Indication: Metastatic RLL airway obstruction.\nAnesthesia: General, ETT.\nProcedure:\n- Exam: Normal left side. RLL polypoid tumor obstructing basilar segments.\n- Action: Snare resection performed. APC applied to base for hemostasis.\n- Toileting: Purulent distal secretions suctioned.\nResult: 90% patency achieved.\nPlan: PACU.",
            2: "OPERATIVE REPORT: The patient presented with widely metastatic disease complicated by an endobronchial component. Under general anesthesia, rigid inspection of the tracheobronchial tree revealed a polypoid neoplasm occluding the anterior, lateral, and posterior basilar segments of the right lower lobe. Mechanical debulking was executed utilizing an electrocautery snare. Subsequent thermal ablation via Argon Plasma Coagulation (APC) was applied to the tumor base to ensure hemostasis. Post-obstructive purulence was evacuated via therapeutic aspiration. Re-establishment of lobar patency to approximately 90% was confirmed.",
            3: "Procedures Performed: Bronchoscopy with tumor destruction (CPT 31641) and therapeutic aspiration (CPT 31645).\nDetails: The RLL tumor was identified. Primary destruction was achieved using a combination of electrocautery snare and non-contact APC ablation (31641). Following tumor removal, distinct therapeutic aspiration was required to clear copious purulent secretions from the distal airways (31645). Hemostasis was confirmed.",
            4: "Procedure Note\nAttending: [Name]\nResident: [Name]\nIndication: RLL mass.\nSteps:\n1. Time out performed.\n2. ETT placed.\n3. Scope advanced to RLL.\n4. Tumor visualized blocking basilar segments.\n5. Snare used to remove tumor.\n6. APC used to burn base.\n7. Suctioned pus from behind the blockage.\n8. Scope removed. No complications.",
            5: "procedure note for rll tumor removal patient under general anesthesia used the olympus scope saw the tumor in the right lower lobe blocking the segments used the snare to cut it out and then apc to stop the bleeding sucked out a bunch of pus from behind it looks about 90 percent open now no complications send to recovery.",
            6: "The patient was placed under general anesthesia and intubated. We inserted the bronchoscope and examined the airways. The left side was clear. In the right lower lobe, a polypoid tumor was found obstructing the basilar segments. We used an electrocautery snare to resect the lesion and then applied APC to the base for cauterization. We also performed therapeutic suctioning of purulent secretions found distally. The airway is now patent.",
            7: "[Indication]\nEndobronchial nodule, metastatic disease.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nRLL tumor obstructing basilar segments identified. Lesion removed via electrocautery snare. Base treated with APC. Purulent secretions aspirated.\n[Plan]\nTransfer to PACU. Discharge pending criteria.",
            8: "The patient was brought to the bronchoscopy suite and placed under general anesthesia. We introduced the bronchoscope through the endotracheal tube. Upon reaching the right lower lobe, we identified a polypoid tumor that was obstructing the anterior, lateral, and posterior basilar segments. We successfully removed the mass using an electrocautery snare. Following removal, we used APC to cauterize the base of the lesion. We also noted and removed purulent secretions from the distal airways. The procedure concluded with the airway largely patent.",
            9: "Procedure: Bronchoscopic resection and ablation.\nTechnique: The endobronchial mass in the RLL was excised using a hot loop. The attachment site was coagulated with argon plasma. Post-obstructive exudate was aspirated from the distal bronchi. The lumen was restored to 90% caliber."
        },
        1: { # Note 1: BPF Glue Instillation
            1: "Dx: Post-pneumonectomy BPF.\nAnesthesia: GA, 8.5 ETT.\nFindings: Right tree normal. Left stump has pinpoint fistula.\nAction: Glue applied via Veno-seal catheter.\nResult: Fistula sealed visually.\n complications: None.",
            2: "OPERATIVE NARRATIVE: The patient, status post-pneumonectomy, presented with a broncho-pleural fistula. Following induction of general anesthesia and placement of an 8.5 mm endotracheal tube, the airway was inspected. The right hemithorax was unremarkable. Examination of the left mainstem stump revealed a pinpoint fistulous tract. A Veno-seal delivery catheter was navigated to the site, and cyanoacrylate sealant was instilled. Visual confirmation suggested successful occlusion of the defect without propagation of the fistula.",
            3: "Service: Bronchoscopy (CPT 31622). Note: Therapeutic intervention (glue) performed but billed as diagnostic due to coding limitations.\nFindings: Visualization of left mainstem bronchial stump revealed a pinpoint broncho-pleural fistula.\nIntervention: Endobronchial glue instillation using Veno-seal system. Fistula sealed. Right airways inspected and normal.",
            4: "Resident Note\nIndication: BPF.\nStaff: Dr. X.\nSteps:\n1. Patient intubated (8.5 ETT).\n2. Scope introduced.\n3. Checked right side - normal.\n4. Looked at left stump - saw pinpoint leak.\n5. Passed glue catheter.\n6. Applied glue to hole.\n7. Looks sealed.\nPlan: Monitor.",
            5: "bpf closure procedure patient intubated with 8.5 tube went down with the q190 scope right side looked fine went to the left stump saw the small fistula hole used the veno seal thing to put glue in it looks like it closed up fine no bleeding extubated.",
            6: "The patient was intubated and the bronchoscope was inserted. We examined the right bronchial tree which was normal. On the left, we visualized the post-pneumonectomy stump and identified a pinpoint broncho-pleural fistula. We advanced a catheter through the working channel and applied tissue glue to the fistula. The defect appeared to be sealed successfully. The scope was withdrawn.",
            7: "[Indication]\nPost-pneumonectomy broncho-pleural fistula.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nRight airways normal. Left stump visualized with pinpoint fistula. Sealed with endobronchial glue via Veno-seal catheter.\n[Plan]\nObserve.",
            8: "We proceeded with the bronchoscopy to address the patient's post-pneumonectomy fistula. After establishing an airway with an 8.5 ETT, we navigated the bronchoscope to the carina. The right lung was clear. We carefully inspected the left stump and found a small, pinpoint fistula. Using the Veno-seal system, we applied glue directly to the defect. The fistula appeared to close completely upon inspection.",
            9: "Procedure: Bronchoscopy with sealant application.\nTarget: Left mainstem stump.\nFindings: Dehiscence/Fistula noted.\nIntervention: Tissue adhesive was deployed via catheter to obturate the tract. Complete occlusion was achieved."
        },
        2: { # Note 2: EBUS + LUL Peripheral Biopsy (Microforceps)
            1: "Indication: Lung nodule.\nAnesthesia: LMA, Propofol.\nEBUS: Station 7 sampled (benign).\nPeripheral: LUL Apical-posterior nodule found with ultrathin scope.\nBiopsy: Microforceps x1. ROSE: Malignant.\n complications: None.",
            2: "PROCEDURE: Combined EBUS-TBNA and peripheral bronchoscopy.\nNARRATIVE: The airway was secured with an LMA. A convex probe EBUS was utilized to survey the mediastinum; station 7 met sampling criteria and was aspirated, yielding benign lymphocytes. An ultrathin bronchoscope (PX190) was then navigated to the left upper lobe apical-posterior segment. The target nodule was identified visually. Micro-forceps biopsies were obtained. Rapid On-Site Evaluation (ROSE) confirmed malignancy. Hemostasis was secured.",
            3: "Codes: 31652 (EBUS 1 station), 31625 (Bronchial biopsy).\nDetails:\n1. EBUS-TBNA: Station 7 sampled with 22G needle (1 station).\n2. Endobronchial Biopsy: Ultrathin scope navigated to LUL Apical-posterior segment. Lesion visualized. Biopsy performed with micro-forceps (31625).\nPathology: Cytology sent; ROSE positive for malignancy.",
            4: "Procedure: EBUS + Biopsy\nPatient: [Name]\nSteps:\n1. LMA placed.\n2. White light exam normal.\n3. EBUS scope in. Sampled station 7.\n4. Switched to ultrathin scope.\n5. Went to LUL apico-posterior.\n6. Saw nodule.\n7. Biopsied with little forceps.\n8. Path said cancer.\nPlan: Oncology referral.",
            5: "ebus and biopsy for lung nodule propofol sedation lma used. checked airways first normal. did ebus on station 7 got some lymph nodes benign. switched to the thin scope went to the left upper lobe found the nodule in the apical posterior segment took bites with the micro forceps rose said cancer no bleeding procedure done.",
            6: "We placed an LMA and started with a standard airway inspection which was unremarkable. We then used the EBUS scope to sample station 7. The cytology was benign. We switched to the PX190 ultrathin scope and navigated to the LUL apical-posterior segment. We saw the nodule and biopsied it with micro-forceps. The pathologist confirmed malignancy in the room. No complications.",
            7: "[Indication]\nPulmonary nodule staging.\n[Anesthesia]\nPropofol, LMA.\n[Description]\nEBUS-TBNA of Station 7 (Benign). Ultrathin bronchoscopy to LUL Apical-posterior segment. Nodule visualized. Micro-forceps biopsy performed (Malignant).\n[Plan]\nAwait final path.",
            8: "The patient underwent a diagnostic bronchoscopy for a lung nodule. We used an LMA for the airway. First, we performed EBUS staging, sampling station 7, which appeared benign. We then exchanged scopes for an ultrathin video bronchoscope. Navigating into the left upper lobe, we visually located the nodule in the apical-posterior segment. Using micro-forceps, we obtained tissue samples which were confirmed as malignant by the on-site pathologist.",
            9: "Procedure: EBUS and peripheral sampling.\nTarget: Station 7 and LUL lesion.\nAction: Station 7 aspirated. LUL apical-posterior nodule identified via ultrathin scope. Lesion sampled with micro-forceps.\nResult: Nodal station benign; lung lesion malignant."
        },
        3: { # Note 3: EBUS 3 Stations (7, 4R, 4L)
            1: "Indication: Mediastinal adenopathy.\nAnesthesia: MAC, LMA.\nEBUS: Sampled stations 7, 4R, 4L.\nTechnique: 22G/19G needles. 5 passes/station.\nResult: 4R = Granuloma. Others pending.\nComplications: None.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA).\nCLINICAL SUMMARY: Evaluation of mediastinal lymphadenopathy.\nDETAILS: Under MAC, the EBUS scope was introduced. Sonographic evaluation identified enlargement of subcarinal (7) and paratracheal (4R, 4L) stations. Systematic sampling was performed with 5 passes per station using 22G and 19G needles. ROSE evaluation of station 4R demonstrated granulomatous inflammation. The procedure was concluded without incident.",
            3: "Billing Code: 31653 (EBUS-TBNA 3+ stations).\nJustification: Three distinct mediastinal nodal stations were sampled: Station 7, Station 4R, and Station 4L.\nTechnique: 5 passes per station to ensure adequacy. ROSE performed on 4R (Granuloma).",
            4: "Resident Note\nProcedure: EBUS\nIndication: Lymph nodes.\nSteps:\n1. LMA/Propofol.\n2. White light exam normal.\n3. EBUS scope in.\n4. Found nodes at 7, 4R, 4L.\n5. Stuck each one 5 times.\n6. 4R showed granuloma.\n7. Suctioned airway, all good.",
            5: "ebus for lymph nodes propofol lma. airway looked normal. used the ebus scope to sample station 7 and 4r and 4l. did 5 passes at each one sent for cytology. rose said 4r was granulomas. no bleeding finished up.",
            6: "The patient was sedated with propofol and an LMA was placed. We performed a standard inspection followed by EBUS. We identified and sampled lymph nodes at stations 7, 4R, and 4L. We performed five passes at each station. On-site pathology showed granulomas in station 4R. The airway was cleared of secretions and the patient was recovered.",
            7: "[Indication]\nMediastinal adenopathy.\n[Anesthesia]\nMAC, Propofol.\n[Description]\nEBUS-TBNA performed on 3 stations: 7, 4R, and 4L. 5 passes per station. ROSE: Granuloma in 4R.\n[Plan]\nAwait final cytology.",
            8: "We performed an EBUS bronchoscopy to investigate the patient's enlarged mediastinal lymph nodes. After inserting the LMA, we used the convex probe to locate nodes at stations 7, 4R, and 4L. We thoroughly sampled all three stations with multiple needle passes. Preliminary results from the 4R node indicate granulomatous disease.",
            9: "Procedure: EBUS-TBNA.\nTargets: Subcarinal and bilateral paratracheal nodes.\nAction: Stations 7, 4R, and 4L were aspirated. 5 excursions per target.\nFindings: Granulomatous reaction noted in 4R."
        },
        4: { # Note 4: EBUS 11R (4R measured only)
            1: "Indication: Molecular markers.\nAnesthesia: General, LMA.\nEBUS: Station 4R viewed (8.4mm), not sampled. Station 11R sampled (7 passes).\nROSE: Adenocarcinoma.\nComplications: None.",
            2: "PROCEDURE: EBUS-TBNA for staging and molecular profiling.\nFINDINGS: The airway was inspected via LMA and found to be normal. EBUS examination revealed an enlarged station 4R node (8.4mm), which was not sampled. Station 11R was identified and sampled via transbronchial needle aspiration (22G needle, 7 passes) to ensure adequate cellularity for molecular testing. ROSE confirmed adenocarcinoma.",
            3: "Code: 31652 (EBUS-TBNA 1-2 stations).\nRationale: Only one station (11R) was sampled. Station 4R was imaged/measured but not aspirated, therefore it does not count toward the 31653 threshold.\nPathology: Adenocarcinoma confirmed on site.",
            4: "Resident Note\nProcedure: EBUS\nIndication: Cancer staging.\nSteps:\n1. LMA/General.\n2. Scope in.\n3. Saw 4R node, didn't stick it.\n4. Went to 11R, did 7 passes for markers.\n5. Path said Adeno.\n6. Done.",
            5: "ebus for markers propofol fentanyl lma. looked at 4r it was smallish 8mm didnt biopsy. went to 11r and biopsied that one 7 times to get enough tissue. rose said adenocarcinoma. no bleeding.",
            6: "Under general anesthesia with an LMA, we performed an EBUS. We visualized station 4R but decided not to sample it. We proceeded to station 11R and performed 7 needle passes to obtain tissue for molecular markers. Rapid pathology confirmed adenocarcinoma. The patient tolerated the procedure well.",
            7: "[Indication]\nMolecular markers.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nStation 4R imaged (8.4mm). Station 11R sampled (7 passes). ROSE: Adenocarcinoma.\n[Plan]\nOncology f/u.",
            8: "The patient presented for EBUS staging to obtain tissue for molecular markers. We used an LMA for the airway. We identified a lymph node at station 4R but elected to sample the node at station 11R instead. We performed seven passes to ensure sufficient tissue. The immediate pathology reading was consistent with adenocarcinoma.",
            9: "Procedure: EBUS-guided aspiration.\nTarget: Hilar node 11R.\nAction: 4R was sonographically assessed but not entered. 11R was aspirated 7 times.\nResult: Positive for adenocarcinoma."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data to assign consistent identities to the 5 distinct notes in the source file.
    Names are generated to be distinct across the 9 variations.
    """
    return [
        # Note 0: RLL Tumor
        {"idx": 0, "orig_name": "Unknown", "orig_age": 68, "names": [
            "John Smith", "Robert Jones", "Michael Brown", "David Miller", "William Wilson",
            "Richard Moore", "Joseph Taylor", "Thomas Anderson", "Charles Thomas"
        ]},
        # Note 1: BPF Glue
        {"idx": 1, "orig_name": "Unknown", "orig_age": 72, "names": [
            "Mary Johnson", "Patricia Williams", "Jennifer Davis", "Linda Martinez", "Elizabeth Garcia",
            "Barbara Rodriguez", "Susan Lopez", "Jessica Hernandez", "Sarah Gonzalez"
        ]},
        # Note 2: EBUS LUL
        {"idx": 2, "orig_name": "Unknown", "orig_age": 65, "names": [
            "James White", "John Lee", "Robert Harris", "Michael Clark", "William Lewis",
            "David Robinson", "Richard Walker", "Joseph Perez", "Thomas Hall"
        ]},
        # Note 3: EBUS 3 Stations
        {"idx": 3, "orig_name": "Unknown", "orig_age": 59, "names": [
            "Margaret Young", "Dorothy Allen", "Lisa King", "Nancy Wright", "Karen Scott",
            "Betty Torres", "Helen Nguyen", "Sandra Hill", "Donna Flores"
        ]},
        # Note 4: EBUS 11R
        {"idx": 4, "orig_name": "Unknown", "orig_age": 61, "names": [
            "Daniel Green", "Paul Adams", "Mark Nelson", "Donald Baker", "George Carter",
            "Kenneth Mitchell", "Steven Roberts", "Edward Phillips", "Brian Evans"
        ]}
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
            # Handle potential missing index in variations_text if source has more notes than expected
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if text variation isn't defined (shouldn't happen with correct setup)
                note_entry["note_text"] = f"Variation {style_num} for note {idx} (Content missing in script map)."
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update Patient Age
                # Some registry entries might have patient_age directly or inside patient_demographics
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                elif "patient_demographics" in note_entry["registry_entry"] and note_entry["registry_entry"]["patient_demographics"]:
                     note_entry["registry_entry"]["patient_demographics"]["age"] = new_age

                # Update Procedure Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN
                if "patient_mrn" in note_entry["registry_entry"]:
                    original_mrn = note_entry["registry_entry"]["patient_mrn"]
                    if original_mrn == "UNKNOWN" or original_mrn == "Unknown":
                        # Generate a mock MRN base if unknown
                        original_mrn = f"IP20260{idx}"
                    note_entry["registry_entry"]["patient_mrn"] = f"{original_mrn}_syn_{style_num}"

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
    output_filename = output_dir / "synthetic_bronch_notes_part_020.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()