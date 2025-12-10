import json
import random
import datetime
import copy
from pathlib import Path

# Source file for Part 035
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_035.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of pre-generated text variations for the specific notes in Part 035.
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
        0: { # Index 0: EBUS-TBNA (Lawrence Turner) - N3 Disease
            1: "Procedure: EBUS-TBNA.\nNodes Sampled: 7, 4R, 10R, 11R.\nFindings: Stations 7, 4R, 10R positive for Adenocarcinoma. 11R benign.\nTechnique: 22G needle, multiple passes. ROSE confirmed malignancy.\nDx: Stage IIIC (N3 disease).\nPlan: Oncology referral.",
            2: "OPERATIVE NARRATIVE: The patient presented for mediastinal staging. The airway was inspected and found to be patent. A linear array EBUS bronchoscope was utilized to systematically survey the mediastinum. Lymphadenopathy was identified at stations 7 (35mm), 4R (27mm), and 10R (16mm). Transbronchial needle aspiration was performed under real-time ultrasound guidance. Rapid On-Site Evaluation (ROSE) confirmed adenocarcinoma in stations 7, 4R, and 10R. Station 11R was sampled and found to be benign. The findings are consistent with N3 disease.",
            3: "Coding Summary:\n- 31653 (EBUS-TBNA, 3+ stations): Biopsies taken from Stations 7, 4R, 10R, and 11R.\n- Medical Necessity: Staging of lung cancer.\n- Technique: Ultrasound guidance used for all needle passes. Images saved to PACS.\n- Pathology: Malignancy confirmed in 3 stations.",
            4: "Resident Note\nAttending: Dr. Turner\nProcedure: EBUS\nSteps:\n1. Scope inserted.\n2. Examined stations 7, 4R, 10R, 11R.\n3. Station 7 was huge (35mm). Biopsied x4.\n4. Biopsied 4R and 10R. All positive for cancer.\n5. 11R was negative.\nPlan: Patient has N3 disease. Not surgical. Needs chemo/rads.",
            5: "Procedure note EBUS TBNA sedation with propofol airway looked ok went down to station 7 it was big 35 by 23 mm stuck it 4 times ROSE said cancer adenocarcinoma. Then went to 4R and 10R both positive too. 11R was negative. So looks like extensive spread N3 disease. Patient tolerated well no bleeding.",
            6: "Endobronchial ultrasound-guided transbronchial needle aspiration was performed. The EBUS scope was introduced. Lymph node stations 7, 4R, 10R, and 11R were identified and sampled. Real-time ultrasound guidance was used for all aspirations. Cytopathology confirmed adenocarcinoma in stations 7, 4R, and 10R. Station 11R showed benign lymphocytes. The procedure was completed without complications.",
            7: "[Indication]\nMediastinal lymphadenopathy, staging.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nEBUS-TBNA performed on stations 7, 4R, 10R, 11R. ROSE confirmed adenocarcinoma in 7, 4R, 10R.\n[Plan]\nRefer to Oncology for Stage IIIC management.",
            8: "The patient was brought to the bronchoscopy suite for staging of suspected lung cancer. We utilized an EBUS scope to visualize the mediastinal lymph nodes. We found significant enlargement in the subcarinal (Station 7) and right paratracheal (Station 4R) areas. Needles samples were taken from these, as well as the hilar nodes. The preliminary pathology results unfortunately confirmed adenocarcinoma in the mediastinal and hilar nodes, indicating N3 disease. The patient recovered well from the sedation.",
            9: "Procedure: Endosonographic needle extraction.\nTarget: Mediastinal and hilar nodes.\nAction: Stations 7, 4R, 10R, and 11R were visualized. Aspiration was executed. \nResult: Malignant cells harvested from 7, 4R, and 10R. 11R yielded benign tissue.\nOutcome: Staging upgraded to N3.",
        },
        2: { # Index 2: BLVR Valves (Robert Chen)
            1: "Procedure: BLVR RUL.\nIndication: Severe emphysema, CV negative.\nAction: 3 Zephyr valves placed in RB1 (4.0), RB2 (4.0), RB3 (5.5).\nResult: Total lobar occlusion. No air leak.\nPlan: Admit for obs.",
            2: "OPERATIVE REPORT: Mr. Chen presented for elective bronchoscopic lung volume reduction. Pre-procedural Chartis assessment confirmed the absence of collateral ventilation in the Right Upper Lobe (RUL). Using a flexible bronchoscope, the RUL segmental anatomy was identified. Three Zephyr endobronchial valves were deployed: a 4.0mm valve in RB1, a 4.0mm valve in RB2, and a 5.5mm valve in RB3. Bronchoscopic inspection confirmed optimal seating and complete lobar occlusion.",
            3: "CPT 31647 (Bronchoscopy with placement of bronchial valves, initial lobe).\n- Site: Right Upper Lobe.\n- Devices: 3 Zephyr Valves.\n- Assessment: Chartis utilized to rule out collateral ventilation (bundled).\n- Outcome: Complete occlusion achieved.",
            4: "Procedure: Valve Placement (BLVR)\nAttending: Dr. Thompson\nSteps:\n1. Airway inspection. RUL selected.\n2. Chartis negative (good for valves).\n3. Sized airways.\n4. Placed valves in RB1, RB2, RB3.\n5. Checked for leaks - none.\nPlan: CXR to check for pneumothorax.",
            5: "We did the lung volume reduction on Mr Chen today for his emphysema right upper lobe. Chartis balloon showed no collateral ventilation so we proceeded. Put in three valves total two 4s and one 5.5. They fit good no leaks. RUL looks closed off. Patient woke up fine sending to recovery.",
            6: "Bronchoscopic lung volume reduction with endobronchial valve placement. The right upper lobe was targeted for treatment of severe emphysema. Chartis assessment confirmed the absence of collateral ventilation. Three Zephyr valves were deployed in the apical, posterior, and anterior segments of the RUL. Visual inspection confirmed appropriate placement and lobar occlusion. There were no immediate complications.",
            7: "[Indication]\nSevere emphysema, RUL target.\n[Anesthesia]\nModerate Sedation.\n[Description]\nChartis: CV Negative. Valves placed: RB1, RB2, RB3. Total occlusion confirmed.\n[Plan]\nOvernight observation. CXR protocol.",
            8: "Mr. Chen underwent a procedure to help with his severe emphysema. We targeted the right upper lobe of his lung. After confirming that the lobe was isolated using a balloon catheter, we placed three one-way valves into the airways leading to that lobe. These valves will allow air to escape but not enter, hopefully reducing the size of the lobe and helping him breathe better. Everything went smoothly and the valves are sitting perfectly.",
            9: "Procedure: Endobronchial prosthesis implantation.\nTarget: Right Upper Lobe.\nAction: Collateral ventilation was ruled out. Three occlusion devices were deployed in the segmental bronchi. \nResult: Complete lobar isolation observed.",
        },
        3: { # Index 3: Tracheal Stenosis (Ava Harrington)
            1: "Dx: Subglottic stenosis (GPA).\nProcedure: Dilation + Radial cuts.\nFindings: 5cm stenotic segment, 60% obstruction.\nAction: \n- CRE balloon dilation (12-15mm).\n- Electrocautery radial incisions.\n- Repeat dilation.\nResult: Airway patent, bronchoscope passes easily.",
            2: "OPERATIVE NARRATIVE: The patient with Granulomatosis with Polyangiitis presented with complex tracheal and bronchial stenosis. A 5cm long-segment stenosis was identified starting 3cm below the vocal cords (60% obstruction). To restore patency, radial incisions were made using an electrocautery knife to release stricture bands. This was followed by serial balloon dilation using CRE balloons sized 12mm to 15mm. Post-procedure inspection revealed significant improvement in luminal diameter.",
            3: "Code: 31630 (Bronchoscopy with dilation/relief of stenosis).\nTechnique: Combined modality using electrocautery knife for incisions and CRE balloon for mechanical dilation.\nSite: Trachea and bilateral lower lobe segments.\nIndication: Symptomatic stenosis refractory to medical management.",
            4: "Procedure: Airway Dilation\nResident: Dr. Miller\nPatient: Ava Harrington\nSteps:\n1. Identified long tracheal stenosis.\n2. Dilated with CRE balloon.\n3. Used cautery knife to cut scar bands.\n4. Dilated RLL and LLL segments.\n5. Airway looks much better now.\nPlan: PACU.",
            5: "Ava Harrington here for her tracheal stenosis she has wegeners. We looked down and saw the narrowing about 3cm below cords. Used the balloon to stretch it out then the knife to cut the tight bands. Also did some work on the lower lobes right and left. Everything is open now scope goes through easy. No bleeding.",
            6: "Flexible bronchoscopy with radial knife incisions and balloon dilatation. The patient has a history of Granulomatosis with polyangiitis causing multi-level stenosis. A 5cm tracheal stenosis was identified. Serial dilations were performed with 12-15mm balloons. Radial incisions were made with an electrocautery knife to facilitate expansion. Similar interventions were performed on the RLL and LLL segmental bronchi. Excellent anatomical result achieved.",
            7: "[Indication]\nTracheal/Bronchial Stenosis (GPA).\n[Anesthesia]\nGeneral, LMA.\n[Description]\nLong segment tracheal stenosis dilated and incised. Bilateral lower lobe strictures dilated. Patency restored.\n[Plan]\nPRN follow-up.",
            8: "Ms. Harrington came in for treatment of her airway narrowing caused by her autoimmune condition. Under general anesthesia, we found a significant narrowing in her windpipe and lower airways. We used a combination of a small knife to make relief cuts in the scar tissue and balloons to stretch the airways open. By the end of the procedure, the airways were significantly more open, which should improve her breathing.",
            9: "Procedure: Endoscopic recanalization.\nPathology: Fibrotic strictures.\nAction: Radial incisions were executed on the scar tissue. Pneumatic dilation was performed to expand the lumen.\nResult: Restoration of airway caliber.",
        },
        4: { # Index 4: Y-Stent (Ethan Calder)
            1: "Indication: Malignant airway obstruction (Esophageal CA).\nFindings: Distal trachea 20% patent. LMS 100% occluded. RMS 30% patent.\nProcedure: Rigid bronchoscopy.\n- Tumor debulking (APC/Cryo).\n- Silicone Y-Stent (15x12x12) placed.\nResult: Airways 90% patent through stent.",
            2: "OPERATIVE NARRATIVE: The patient presented with critical malignant central airway obstruction. Rigid bronchoscopy was initiated. Extensive tumor infiltration was noted at the carina, completely occluding the Left Mainstem (LMS). Mechanical debulking and APC were utilized to re-establish a lumen. A customized 15x12x12mm silicone Y-stent was deployed to scaffold the airway. Post-deployment, the trachea and both mainstems demonstrated >90% patency.",
            3: "Codes: \n- 31636 (Stent placement, bronchial)\n- 31641 (Tumor destruction/debulking)\nRationale: Critical obstruction required mechanical debulking prior to stent placement. A silicone Y-stent was placed covering the trachea and both mainstems.",
            4: "Procedure: Rigid Bronch + Y-Stent\nPt: Ethan Calder\nSteps:\n1. 12mm Rigid scope inserted.\n2. Tumor debulked with APC and suction.\n3. Measured for Y-stent.\n4. Inserted silicone Y-stent (blind pass technique).\n5. Adjusted with forceps.\n6. Airway open now.\nPlan: ICU, humidified air.",
            5: "Ethan Calder with the esophageal cancer compressing the airway. We took him to the OR for a stent. Rigid scope went in. Debulked a lot of tumor at the carina left side was totally shut. Put in a Y stent silicone type. Had to push it past cords blindly then grab it with forceps. It sat perfectly. Airways look great now. ICU for monitoring.",
            6: "Rigid bronchoscopy with tumor debulking and silicone Y-stent placement. Significant malignant obstruction of the distal trachea and mainstem bronchi was identified. Tumor was debulked using APC and cryotherapy. A 15x12x12 silicone Y-stent was customized and deployed. Post-procedure inspection confirmed excellent stent position and patency of bilateral mainstems.",
            7: "[Indication]\nMalignant Central Airway Obstruction.\n[Anesthesia]\nGeneral, Jet Ventilation.\n[Description]\nRigid bronchoscopy. Tumor debulked (APC/Cryo). Silicone Y-Stent placed. Patency restored to >90%.\n[Plan]\nICU, Saline nebs.",
            8: "Mr. Calder was suffering from severe difficulty breathing due to a tumor blocking his main airways. We performed a rigid bronchoscopy to clear the blockage. After removing a significant amount of tumor tissue using heat and freezing probes, we placed a Y-shaped silicone stent. This stent props open his windpipe and branches to both lungs. We were very pleased to see his airways were 90% open after the stent was in place.",
            9: "Procedure: Rigid endoscopy with tumor ablation and prosthetic scaffolding.\nProblem: Carinal neoplastic infiltration.\nAction: Tissue was excised. A bifurcated silicone prosthesis was inserted.\nResult: Luminal integrity restored.",
        },
        7: { # Index 7: Stent Removal (Daniel Wilbert Conley)
            1: "Indication: Stent migration/infection.\nFindings: Stent migrated to RMS, obstructing LMS. Purulent secretions.\nProcedure: Rigid bronchoscopy.\n- Stent grasped and removed en bloc.\n- Airways irrigated.\nResult: Patent airways, mucosal inflammation. TE fistula visible (covered by esophageal stent).",
            2: "OPERATIVE NARRATIVE: The patient presented with a migrated, infected airway stent. Rigid bronchoscopy revealed the tracheal stent had telescoped and migrated into the right mainstem, occluding the left. The stent was successfully grasped and extracted using rigid forceps. Copious purulent secretions were evacuated from the post-obstructive left lung. Inspection revealed an underlying TE fistula, adequately covered by the esophageal stent.",
            3: "Code: 31638 (Bronchoscopy with removal of foreign body/stent).\nComplexity: Required rigid bronchoscopy and heavy forceps due to stent incarceration and migration.\nMedical Necessity: Stent migration causing complete obstruction of LMS and infection.",
            4: "Procedure: Stent Removal\nResident: Dr. Gallegos\nSteps:\n1. Rigid scope inserted.\n2. Stent found migrated into RMS.\n3. Tons of pus behind it.\n4. Grabbed stent with rigid forceps.\n5. Pulled everything out.\n6. Cleaned up the airway.\nPlan: Antibiotics for pneumonia.",
            5: "Daniel Conley here for stent removal. The old stent slid down and blocked the left lung. It was nasty full of pus. We went in with the rigid scope grabbed the edge of the stent and pulled the whole thing out. Suctioned out a lot of infection. The fistula looks covered by the esophageal stent so thats good. Sending him to PACU.",
            6: "Rigid bronchoscopy for airway stent removal. The patient presented with stent migration and infection. The stent was visualized in the right mainstem bronchus. Using rigid forceps, the stent was grasped and removed. Post-obstructive purulence was evacuated from the left mainstem. The underlying airway was erythematous but patent. The TE fistula appeared covered by the esophageal stent.",
            7: "[Indication]\nStent migration, infection.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Migrated stent removed via forceps. Purulent secretions cleared. TE fistula assessed.\n[Plan]\nAntibiotics, observation.",
            8: "Mr. Conley needed his airway stent removed because it had moved out of place and caused an infection. Using a rigid metal tube, we reached the stent which had slipped into his right lung. We carefully pulled it out. Once it was gone, we were able to clear out a lot of infected fluid from his left lung, which had been blocked. His airways look irritated but open now.",
            9: "Procedure: Endoscopic prosthesis extraction.\nIndication: Device displacement.\nAction: The migrated prosthesis was secured and withdrawn using rigid instrumentation. Purulent exudate was evacuated.\nResult: Airway obstruction resolved.",
        },
        9: { # Index 9: Vapor Ablation (George Martinez)
            1: "Procedure: Bronchoscopic Thermal Vapor Ablation (BTVA).\nTarget: RUL (RB3, RB1).\nAction: InterVapor catheter placed. 14 calories total delivered.\nResult: Good vapor delivery. No complications.\nPlan: ICU admission, prophylactic antibiotics.",
            2: "OPERATIVE NARRATIVE: The patient with severe emphysema underwent bronchoscopic thermal vapor ablation. The Right Upper Lobe was selected based on collateral ventilation status. The InterVapor catheter was navigated to the anterior (RB3) and apical (RB1) segments. A total of 14 calories of thermal energy were delivered (8 cal to RB3, 6 cal to RB1). Fluoroscopy confirmed accurate catheter placement and vapor containment. The patient tolerated the procedure without adverse events.",
            3: "Code: 31641 (Destruction of tumor/tissue, bronchoscopic).\nTechnique: Thermal vapor ablation of emphysematous tissue.\nTarget: Right Upper Lobe.\nDosage: 14 Calories total.\nNote: This is a distinct modality from valve placement.",
            4: "Procedure: Vapor Ablation (InterVapor)\nAttending: Dr. Chen\nSteps:\n1. Navigated to RUL.\n2. Treated RB3 with 8 calories.\n3. Treated RB1 with 6 calories.\n4. Verified with fluoro.\n5. No bleeding.\nPlan: Watch for inflammatory response/fever.",
            5: "George Martinez here for the vapor treatment for his COPD. We did the RUL today. Used the steam catheter put 8 calories in the front segment and 6 in the top one. Vapor went in good seen on xray. Patient is stable. He needs antibiotics and prednisone for the inflammation coming up.",
            6: "Bronchoscopic thermal vapor ablation. The right upper lobe was targeted for lung volume reduction. The vapor catheter was positioned in the RUL anterior and apical segments. Thermal energy was delivered as calculated. Fluoroscopy confirmed appropriate vapor delivery. The procedure was uncomplicated.",
            7: "[Indication]\nSevere Emphysema, RUL target (CV+).\n[Anesthesia]\nMAC/LMA.\n[Description]\nBTVA to RUL. RB3: 8 cal. RB1: 6 cal. Vapor delivery confirmed.\n[Plan]\nICU, Prednisone, Antibiotics.",
            8: "Mr. Martinez underwent a steam treatment for his emphysema today. Since his lung anatomy wasn't right for valves, we used thermal vapor to treat the diseased parts of his right upper lung. We delivered the vapor to two specific segments. This will cause that tissue to scar down and shrink over the next few months, which should help him breathe better. He needs to stay in the hospital for monitoring as this causes a deliberate inflammation.",
            9: "Procedure: Endobronchial thermal therapy.\nTarget: Emphysematous lung tissue.\nAction: Vapor energy was administered to the RUL segments. \nResult: Tissue ablation initiated.\nPost-op: Inflammatory modulation protocol.",
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the patients to maintain consistency across variations.
    Map indices to the specific notes in Part 035.
    """
    return [
        {"idx": 0, "orig_name": "Michael Brown", "orig_age": 68, "gender": "Male", "names": ["James Wilson", "Robert Taylor", "William Anderson", "David Thomas", "Richard Martinez", "Joseph Hernandez", "Charles Lopez", "Thomas Gonzalez", "Christopher Clark"]},
        {"idx": 1, "orig_name": "Unknown", "orig_age": 70, "gender": "Female", "names": ["Mary Lewis", "Patricia Robinson", "Linda Walker", "Barbara Perez", "Elizabeth Hall", "Jennifer Young", "Maria Allen", "Susan Sanchez", "Margaret Wright"]},
        {"idx": 2, "orig_name": "Robert Chen", "orig_age": 67, "gender": "Male", "names": ["John King", "Michael Scott", "David Green", "James Baker", "Robert Adams", "William Nelson", "Richard Hill", "Joseph Ramirez", "Charles Campbell"]},
        {"idx": 3, "orig_name": "Ava Harrington", "orig_age": 45, "gender": "Female", "names": ["Sarah Mitchell", "Jessica Roberts", "Emily Carter", "Ashley Phillips", "Michelle Evans", "Amanda Turner", "Melissa Torres", "Stephanie Parker", "Nicole Collins"]},
        {"idx": 4, "orig_name": "Ethan Calder", "orig_age": 62, "gender": "Male", "names": ["Daniel Edwards", "Matthew Stewart", "Anthony Flores", "Mark Morris", "Donald Nguyen", "Steven Murphy", "Paul Rivera", "Andrew Cook", "Joshua Rogers"]},
        {"idx": 5, "orig_name": "Linda Washington", "orig_age": 65, "gender": "Female", "names": ["Lisa Morgan", "Nancy Bell", "Karen Reed", "Betty Bailey", "Helen Cooper", "Sandra Richardson", "Donna Cox", "Carol Howard", "Ruth Ward"]},
        {"idx": 6, "orig_name": "Caleb Donahue", "orig_age": 58, "gender": "Male", "names": ["Kevin Peterson", "Brian Gray", "George Ramirez", "Edward James", "Ronald Watson", "Timothy Brooks", "Jason Kelly", "Jeffrey Sanders", "Ryan Price"]},
        {"idx": 7, "orig_name": "Daniel Wilbert Conley", "orig_age": 64, "gender": "Male", "names": ["Gary Bennett", "Jacob Wood", "Nicholas Barnes", "Eric Ross", "Stephen Henderson", "Larry Coleman", "Justin Jenkins", "Scott Perry", "Brandon Powell"]},
        {"idx": 8, "orig_name": "Maizie Booth", "orig_age": 71, "gender": "Female", "names": ["Sharon Long", "Cynthia Patterson", "Kathleen Hughes", "Amy Flores", "Shirley Washington", "Angela Butler", "Anna Simmons", "Brenda Foster", "Pamela Gonzales"]},
        {"idx": 9, "orig_name": "George Martinez", "orig_age": 65, "gender": "Male", "names": ["Frank Bryant", "Gregory Alexander", "Raymond Russell", "Patrick Griffin", "Jack Diaz", "Dennis Hayes", "Jerry Myers", "Tyler Ford", "Aaron Hamilton"]},
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
    
    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Process notes
    # We will process all notes available in the source data
    # If a specific variation isn't manually written in get_variations(),
    # we will skip generating variations for that specific index to avoid errors,
    # or rely on the logic below to handle it.
    
    for idx, original_note in enumerate(source_data):
        # Find corresponding mock data
        record = next((item for item in base_data if item["idx"] == idx), None)
        
        if not record:
            # Fallback if more notes exist than mock data
            record = {"orig_name": "Unknown", "orig_age": 60, "names": [f"Patient_{idx}_{i}" for i in range(1, 10)]}
            orig_age = 60
        else:
            orig_age = record['orig_age']

        # Check if we have text variations for this index
        if idx not in variations_text:
            # If we don't have custom text for this index, we skip it to ensure quality
            # Alternatively, one could implement a generic fallback, but for this task,
            # we adhere to the provided examples.
            continue

        # Iterate through the 9 styles
        for style_num in range(1, 10):
            
            # Deep copy the original note structure
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields to maintain validity
            if "registry_entry" in note_entry:
                # Update Age
                note_entry["registry_entry"]["patient_age"] = new_age
                
                # Update Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN to be unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
                else:
                     note_entry["registry_entry"]["patient_mrn"] = f"UNKNOWN_syn_{style_num}"

            # Add metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON
    output_filename = output_dir / "synthetic_notes_part_035.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()