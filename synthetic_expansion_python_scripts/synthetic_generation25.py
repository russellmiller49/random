import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_025.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the notes in part_025.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # EMN/EBUS/Cryo RLL
            1: "Procedure: EMN bronchoscopy RLL.\n- Navigated to target.\n- Radial EBUS: concentric view.\n- Cryobiopsy x3.\n- Arndt blocker deployed for prophylactic hemostasis.\n- No bleeding.",
            2: "OPERATIVE REPORT: The patient underwent electromagnetic navigation bronchoscopy for a peripheral right lower lobe nodule. Following navigation, radial endobronchial ultrasound confirmed the lesion's location. Transbronchial cryobiopsy was performed to obtain high-quality tissue. An Arndt bronchial blocker was utilized effectively to ensure hemostasis immediately following biopsy.",
            3: "Procedure coded as: 31628 (Transbronchial lung biopsy, single lobe), 31627 (Navigation add-on), 31654 (Radial EBUS add-on). Cryoprobe used for specimen acquisition. Arndt blocker utilized for hemorrhage control.",
            4: "Procedure Steps:\n1. Time out performed.\n2. Scope introduced.\n3. EMN navigation to RLL nodule.\n4. Radial EBUS confirmation.\n5. Arndt blocker placed.\n6. Cryobiopsies obtained.\n7. Hemostasis confirmed.",
            5: "we did the emn bronch today for the rll spot navigated down there radial ebus looked good took some cryobiopsies put the arndt blocker up just in case for bleeding no issues really patient tolerated it well.",
            6: "EMN-guided bronchoscopy was performed to target a peripheral RLL nodule. Radial EBUS provided confirmation of the lesion. Transbronchial cryobiopsy was executed. An Arndt blocker was employed for hemostasis control.",
            7: "[Indication]\nPeripheral RLL nodule requiring biopsy.\n[Anesthesia]\nGeneral.\n[Description]\nEMN navigation used. Radial EBUS confirmed target. Transbronchial cryobiopsy performed. Arndt blocker used for hemostasis.\n[Plan]\nPathology pending.",
            8: "The patient was brought to the suite for an EMN-guided bronchoscopy. We navigated successfully to the peripheral RLL nodule. Radial EBUS was used to confirm the position. We then performed a transbronchial cryobiopsy. To manage potential bleeding, an Arndt blocker was used for hemostasis.",
            9: "Electromagnetic navigation was utilized to locate the RLL nodule. Radial EBUS verified the position. The lesion was sampled via transbronchial cryobiopsy. An Arndt blocker was deployed to manage hemostasis."
        },
        1: { # EBUS-TBNA Lymphoma (4 stations)
            1: "EBUS-TBNA.\n- Station 7 sampled.\n- Station 4R sampled.\n- Station 10R sampled.\n- Station 11R sampled.\n- ROSE: Follicular lymphoma in all stations.",
            2: "The mediastinum and hilum were systematically evaluated via EBUS-TBNA for lymphoma staging. Nodal stations 7, 4R, 10R, and 11R were visualized and aspirated. Rapid on-site evaluation was consistent with follicular lymphoma across all sampled nodal basins.",
            3: "CPT 31653: Bronchoscopy with EBUS sampling of 3 or more stations. Stations 7, 4R, 10R, and 11R were all distinctly sampled with needle aspiration. Pathologic findings confirm follicular lymphoma.",
            4: "Procedure Note:\n- EBUS scope inserted.\n- Lymph nodes identified.\n- TBNA performed at stations 7, 4R, 10R, 11R.\n- Specimens sent for flow cytometry.\n- Findings: Follicular lymphoma.",
            5: "patient here for staging lymphoma we used the ebus scope hit nodes 7 and 4r also 10r and 11r needle went in easy rapid path said follicular lymphoma in all of them no complications.",
            6: "EBUS-TBNA was performed for lymphoma staging. Sampling included stations 7, 4R, 10R, and 11R. Results demonstrated follicular lymphoma in all sampled nodes.",
            7: "[Indication]\nLymphoma staging.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA performed on stations 7, 4R, 10R, 11R. All positive for follicular lymphoma.\n[Plan]\nOncology referral.",
            8: "We performed an EBUS-TBNA to stage the patient's lymphoma. We successfully sampled stations 7, 4R, 10R, and 11R. The pathology returned showing follicular lymphoma in all the nodes we tested.",
            9: "Endobronchial ultrasound with transbronchial needle aspiration was conducted for lymphoma staging. Stations 7, 4R, 10R, and 11R were aspirated. Follicular lymphoma was detected in all nodes."
        },
        2: { # Flex Bronch + BAL + ENB + EBUS + Biopsy Lingula
            1: "Procedure:\n- BAL RUL.\n- ENB nav to Lingula.\n- Radial EBUS confirm.\n- TBNA and Forceps Bx of Lingula lesion under fluoro.",
            2: "A comprehensive diagnostic bronchoscopy was performed. Bronchoalveolar lavage was first completed in the right upper lobe. Electromagnetic navigation bronchoscopy was then utilized to locate a lingular lesion, confirmed via radial EBUS. Transbronchial needle aspiration and forceps biopsies were obtained under fluoroscopic guidance.",
            3: "Codes: 31624 (BAL RUL), 31627 (Nav), 31654 (REBUS), 31629 (TBNA Lingula), 31628 (Forceps Bx Lingula). Distinct procedures performed on separate sites/lobes.",
            4: "Steps:\n1. Airway inspection.\n2. BAL RUL.\n3. ENB to Lingula.\n4. REBUS check.\n5. TBNA Lingula.\n6. Forceps biopsy Lingula.",
            5: "did the bronch today bal in the rul then used the enb to get to that spot in the lingula radial ebus saw it fine did some needle biopsies and forceps bites using fluoro to see.",
            6: "Flexible bronchoscopy included BAL of the RUL. ENB navigation was used to reach a lingular lesion, confirmed by radial EBUS. TBNA and forceps biopsies were obtained under fluoroscopy.",
            7: "[Indication]\nLung lesion.\n[Anesthesia]\nModerate.\n[Description]\nBAL RUL. ENB to Lingula. REBUS confirmation. TBNA and forceps biopsies obtained.\n[Plan]\nAwait path.",
            8: "We started with a flexible bronchoscopy and performed a BAL in the RUL. Then, using ENB navigation, we targeted a lesion in the Lingula. We confirmed it with radial EBUS and took both TBNA and forceps biopsies under fluoroscopy.",
            9: "Bronchoscopy with lavage in the RUL was conducted. ENB navigation located the lingular lesion, verified by radial EBUS. Needle aspiration and forceps samples were acquired under fluoroscopic guidance."
        },
        3: { # PleurX (Tunneled Catheter)
            1: "Dx: Malignant pleural effusion (R).\nProc: US-guided PleurX placement.\nDrainage: 1.55 L.\nComplications: None.",
            2: "The patient with stage IV NSCLC and recurrent malignant pleural effusion underwent ultrasound-guided placement of a tunneled indwelling pleural catheter (PleurX). The procedure yielded 1.55 liters of fluid and was tolerated well.",
            3: "Code 32550: Insertion of indwelling tunneled pleural catheter with cuff. Imaging guidance (US) utilized. 1.55 L fluid drained.",
            4: "Procedure:\n1. US localization.\n2. Local anesthetic.\n3. Tunnel created.\n4. Catheter inserted into pleural space.\n5. 1.55 L drained.\n6. Dressing applied.",
            5: "put in a pleurx catheter today right side lung cancer patient lots of fluid used ultrasound to find the spot tunneled it in drained about 1.55 liters patient feels better.",
            6: "Ultrasound-guided tunneled PleurX catheter placement was performed for a recurrent right malignant pleural effusion in a stage IV NSCLC patient. 1.55 L was drained.",
            7: "[Indication]\nRecurrent malignant effusion.\n[Anesthesia]\nLocal.\n[Description]\nUS-guided PleurX placement right side. 1.55 L drained.\n[Plan]\nHome nursing setup.",
            8: "We performed an ultrasound-guided placement of a tunneled PleurX catheter for the patient's recurrent right malignant pleural effusion due to stage IV NSCLC. We successfully drained 1.55 L of fluid.",
            9: "Tunneled PleurX catheter insertion was guided by ultrasound for symptomatic recurrent right malignant pleural effusion. 1.55 L of fluid was evacuated."
        },
        4: { # EBUS-TBNA Lymphoma (4 stations different)
            1: "EBUS-TBNA.\n- Stations 7, 4R, 10L, 11R sampled.\n- Indication: Lymphoma staging.\n- Sample adequacy confirmed.",
            2: "Evaluation of mediastinal and hilar lymphadenopathy was conducted via EBUS-TBNA. Systematic sampling of stations 7, 4R, 10L, and 11R was performed to rule out lymphoma.",
            3: "Bill 31653: EBUS sampling of 3 or more stations (7, 4R, 10L, 11R). Procedure indicated for lymphadenopathy concerning for lymphoma.",
            4: "Steps:\n1. EBUS scope passed.\n2. Nodes visualized.\n3. TBNA of 7, 4R, 10L, 11R.\n4. Slides prepared.\n5. Scope removed.",
            5: "ebus for lymphoma check sampled 7 4r 10l and 11r nodes looked big got good samples sent for path.",
            6: "EBUS-TBNA with sampling of stations 7, 4R, 10L, and 11R was performed for mediastinal and hilar lymphadenopathy concerning for lymphoma.",
            7: "[Indication]\nLymphadenopathy/Lymphoma.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA of stations 7, 4R, 10L, 11R.\n[Plan]\nFollow up path.",
            8: "We performed an EBUS-TBNA to investigate mediastinal and hilar lymphadenopathy concerning for lymphoma. We sampled stations 7, 4R, 10L, and 11R.",
            9: "Endobronchial ultrasound with needle aspiration was performed on stations 7, 4R, 10L, and 11R for lymphoma evaluation."
        },
        5: { # US Thoracentesis
            1: "Proc: Therapeutic Thora (US guided).\nSite: Right.\nFluid: 800 mL clear yellow.\nDx: Hepatic hydrothorax.",
            2: "The patient with cirrhosis and right hepatic hydrothorax underwent ultrasound-guided therapeutic thoracentesis. A total of 800 mL of clear yellow pleural fluid was removed without complication.",
            3: "Code 32555: Thoracentesis with imaging guidance. 800 mL drained for hepatic hydrothorax.",
            4: "Steps:\n1. US scan.\n2. Prep and drape.\n3. Needle insertion.\n4. Aspiration of 800 mL.\n5. Catheter removal.",
            5: "did a thora on the right side used ultrasound guide drained 800 ml looks like hepatic hydrothorax fluid was clear yellow.",
            6: "Ultrasound-guided therapeutic thoracentesis for right hepatic hydrothorax in a cirrhotic patient drained 800 mL of clear yellow fluid.",
            7: "[Indication]\nHepatic hydrothorax.\n[Anesthesia]\nLocal.\n[Description]\nUS-guided thoracentesis right. 800 mL removed.\n[Plan]\nMonitor.",
            8: "We performed an ultrasound-guided therapeutic thoracentesis for a right hepatic hydrothorax in this cirrhotic patient. We successfully drained 800 mL of clear yellow fluid.",
            9: "Therapeutic thoracentesis guided by ultrasound was executed for right hepatic hydrothorax. 800 mL of clear yellow fluid was withdrawn."
        },
        6: { # Rigid Bronch Tracheal Polyps
            1: "Rigid Bronchoscopy.\n- Snare resection of tracheal polyps.\n- APC ablation applied.\n- Airway obstruction relieved.",
            2: "The patient underwent rigid bronchoscopy for management of severe endotracheal obstruction. Multiple obstructing polyps were resected using electrocautery snare and the bases were ablated with Argon Plasma Coagulation (APC).",
            3: "Code 31641: Bronchoscopy with destruction of tumor or relief of stenosis. Methods: Electrocautery snare and APC.",
            4: "Procedure:\n1. Rigid scope inserted.\n2. Polyps identified.\n3. Snare resection performed.\n4. APC ablation.\n5. Airway patent.",
            5: "rigid bronch for those tracheal polyps causing blockage used the snare to cut them out and apc to burn the base airway looks much better now.",
            6: "Rigid bronchoscopy with electrocautery snare resection and APC ablation of multiple obstructing tracheal polyps causing severe endotracheal obstruction.",
            7: "[Indication]\nTracheal obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronch. Snare resection. APC ablation of polyps.\n[Plan]\nObs.",
            8: "We performed a rigid bronchoscopy to address severe endotracheal obstruction. We used an electrocautery snare to resect the polyps and applied APC ablation to the bases.",
            9: "Rigid bronchoscopy was utilized for snare resection and APC ablation of tracheal polyps to relieve obstruction."
        },
        7: { # Ion Robotic RUL
            1: "Ion Robotic Bronchoscopy.\n- Radial EBUS used.\n- Target: 2.8 cm RUL posterior nodule.\n- Transbronchial biopsies taken.",
            2: "Navigational bronchoscopy was performed using the Ion robotic platform. The 2.8 cm nodule in the RUL posterior segment was localized and confirmed with radial EBUS. Transbronchial biopsies were obtained.",
            3: "Codes: 31627 (Robotic Nav), 31628 (Biopsy RUL), 31654 (REBUS). Procedure targets peripheral RUL nodule.",
            4: "Steps:\n1. Ion catheter advanced.\n2. Navigation to RUL target.\n3. REBUS confirmation.\n4. Biopsies taken.\n5. Hemostasis.",
            5: "used the ion robot today for that rul nodule about 2.8 cm posterior segment radial ebus confirmed it took some biopsies went smooth.",
            6: "Ion robotic bronchoscopy with radial EBUS and transbronchial biopsies of a 2.8 cm RUL posterior segment nodule.",
            7: "[Indication]\nRUL Nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon robotic nav. REBUS confirm. TBBx of 2.8 cm RUL nodule.\n[Plan]\nPath.",
            8: "We used the Ion robotic system for a navigational bronchoscopy. We targeted a 2.8 cm nodule in the RUL posterior segment, confirmed it with radial EBUS, and took transbronchial biopsies.",
            9: "Ion robotic navigation facilitated access to the RUL nodule. Radial EBUS verified the location. Transbronchial biopsies were acquired."
        },
        8: { # Ion Robotic RUL (PET avid)
            1: "Ion Robotic Bronchoscopy.\n- Target: 2.3 cm PET-avid RUL nodule.\n- Radial EBUS confirmation.\n- Biopsies obtained.",
            2: "The Ion robotic system was utilized for navigational bronchoscopy. A PET-avid 2.3 cm nodule in the right upper lobe was localized, confirmed via radial EBUS, and biopsied transbronchially.",
            3: "Billing 31627 (Nav), 31628 (Bx), 31654 (REBUS). Target is solitary 2.3 cm PET-avid nodule in RUL.",
            4: "Procedure:\n1. Robot setup.\n2. Nav to RUL nodule.\n3. EBUS verification.\n4. Biopsy performed.\n5. Finish.",
            5: "ion robotic case for the pet avid nodule in the rul 2.3 cm radial ebus saw it nicely took biopsies patient did fine.",
            6: "Ion robotic navigational bronchoscopy with radial EBUS and transbronchial biopsies of a PET-avid 2.3 cm RUL nodule.",
            7: "[Indication]\nPET-avid RUL nodule.\n[Anesthesia]\nGeneral.\n[Description]\nIon robotic nav. REBUS. TBBx 2.3 cm nodule.\n[Plan]\nAwait results.",
            8: "We performed an Ion robotic navigational bronchoscopy to biopsy a PET-avid 2.3 cm nodule in the RUL. We confirmed the location with radial EBUS before taking samples.",
            9: "Robotic navigation via the Ion system allowed biopsy of the PET-avid RUL nodule. Radial EBUS confirmed the site."
        },
        9: { # Rigid Bronch Stent (Dumon)
            1: "Rigid Bronchoscopy.\n- Mechanical debridement.\n- Cautery/APC used.\n- 14x60 mm Dumon stent placed in L mainstem.",
            2: "Rigid bronchoscopy was undertaken for critical tumor-related obstruction of the left mainstem bronchus. Following mechanical debridement and application of cautery and APC, a 14x60 mm silicone Dumon stent was successfully deployed.",
            3: "Code 31636: Stent placement, initial bronchus. Includes debridement/cautery of same lesion. Stent size 14x60 mm silicone.",
            4: "Steps:\n1. Rigid scope intubation.\n2. Debridement of tumor.\n3. Hemostasis with APC.\n4. Dumon stent (14x60mm) placement.\n5. Airway patent.",
            5: "rigid bronch for the left mainstem blockage tumor was bad used cautery and debrided it then put in a dumon stent 14x60 mm airway is open now.",
            6: "Rigid bronchoscopy with mechanical debridement, cautery/APC, and placement of a 14x60 mm silicone Dumon stent in the left mainstem bronchus for critical tumor-related obstruction.",
            7: "[Indication]\nL mainstem obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronch. Debridement/APC. Dumon stent 14x60mm placed.\n[Plan]\nMonitor.",
            8: "We performed a rigid bronchoscopy to relieve critical tumor-related obstruction in the left mainstem bronchus. After mechanical debridement and cautery/APC, we placed a 14x60 mm silicone Dumon stent.",
            9: "Rigid bronchoscopy facilitated mechanical debridement and cautery/APC. A 14x60 mm silicone Dumon stent was deployed to resolve the obstruction."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Provides mock base names and ages for the 10 notes in the source file.
    Names list corresponds to the 9 variations.
    """
    return [
        {"idx": 0, "orig_age": 65, "names": ["Robert Smith", "James Johnson", "John Williams", "Michael Brown", "David Jones", "William Garcia", "Richard Miller", "Joseph Davis", "Thomas Rodriguez"]},
        {"idx": 1, "orig_age": 58, "names": ["Mary Martinez", "Patricia Hernandez", "Jennifer Lopez", "Linda Gonzalez", "Elizabeth Wilson", "Barbara Anderson", "Susan Thomas", "Jessica Taylor", "Sarah Moore"]},
        {"idx": 2, "orig_age": 70, "names": ["Charles Jackson", "Christopher Martin", "Daniel Lee", "Matthew Perez", "Anthony Thompson", "Mark White", "Donald Harris", "Steven Sanchez", "Paul Clark"]},
        {"idx": 3, "orig_age": 62, "names": ["Karen Ramirez", "Nancy Lewis", "Lisa Robinson", "Betty Walker", "Margaret Young", "Sandra Allen", "Ashley King", "Kimberly Wright", "Emily Scott"]},
        {"idx": 4, "orig_age": 55, "names": ["Andrew Torres", "Joshua Nguyen", "Kenneth Hill", "Kevin Flores", "Brian Green", "George Adams", "Edward Nelson", "Ronald Baker", "Timothy Hall"]},
        {"idx": 5, "orig_age": 68, "names": ["Donna Rivera", "Michelle Campbell", "Dorothy Mitchell", "Carol Carter", "Amanda Roberts", "Melissa Gomez", "Deborah Phillips", "Stephanie Evans", "Rebecca Turner"]},
        {"idx": 6, "orig_age": 72, "names": ["Jason Diaz", "Jeffrey Parker", "Ryan Cruz", "Jacob Edwards", "Gary Collins", "Nicholas Reyes", "Eric Stewart", "Jonathan Morris", "Stephen Morales"]},
        {"idx": 7, "orig_age": 64, "names": ["Sharon Murphy", "Kathleen Cook", "Cynthia Rogers", "Helen Morgan", "Amy Peterson", "Shirley Cooper", "Angela Reed", "Anna Bailey", "Ruth Bell"]},
        {"idx": 8, "orig_age": 60, "names": ["Larry Gomez", "Scott Kelly", "Frank Howard", "Justin Ward", "Brandon Cox", "Raymond Diaz", "Gregory Richardson", "Benjamin Wood", "Samuel Watson"]},
        {"idx": 9, "orig_age": 75, "names": ["Brenda Brooks", "Pamela Bennett", "Nicole Gray", "Katherine James", "Virginia Reyes", "Debra Cruz", "Rachel Hughes", "Janet Price", "Carolyn Myers"]}
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
            
            # Get the specific name assigned for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            # Handle cases where source note count might exceed variations dictionary
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if specific variation missing (shouldn't happen with correct data)
                note_entry["note_text"] = original_note["note_text"] + f" [Variation {style_num}]"

            # Update registry_entry fields if they exist (some files might not have full registry_entry)
            if "registry_entry" not in note_entry:
                note_entry["registry_entry"] = {}
                
            # Update/Set Patient info
            note_entry["registry_entry"]["patient_age"] = new_age
            note_entry["registry_entry"]["procedure_date"] = rand_date_str
            
            # Update MRN to be unique
            base_mrn = note_entry["registry_entry"].get("patient_mrn", f"IP_PART25_{idx}")
            note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
            
            # Add synthetic metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON
    output_filename = output_dir / "synthetic_blvr_notes_part_025.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()