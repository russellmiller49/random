import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (as provided in the prompt)
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_017.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date object between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the 4 notes in bronch_notes_part_017.json.
    Structure: Note_Index (0-3) -> Style_Index (1-9) -> Text
    """
    
    variations = {
        0: { # Note 0: Tracheal stenosis, Ultraflex stent placement (CPT 31631)
            1: "Pre-op: Symptomatic tracheal stenosis.\nAnesthesia: General, LMA.\nProcedure:\n- Scope inserted. 3.5cm A-shaped stenosis (90% obstruction) found 2.5cm distal to cords.\n- Markers placed via fluoro.\n- Jagwire placed.\n- 16x40mm Ultraflex stent deployed over wire.\n- Dilated w/ 18mm Elation balloon.\n- Airway patent (90% caliber).\nPlan: PACU. Follow up 2 weeks.",
            2: "INDICATION: The patient presented with symptomatic, complex tracheal stenosis requiring intervention.\nPROCEDURE NARRATIVE: Under general anesthesia, the airway was secured via laryngeal mask airway. Videobronchoscopy revealed a high-grade, A-shaped stenotic segment measuring 3.5 cm in length, located approximately 2.5 cm distal to the vocal cords. Fluoroscopic guidance was utilized to demarcate the lesion. A guidewire was advanced, facilitating the deployment of a 16x40 mm uncovered Ultraflex self-expanding metallic stent. Subsequent balloon dilation was performed using an 18 mm Elation catheter, achieving excellent patency and restoration of airway caliber.",
            3: "Service Performed: Bronchoscopy with Tracheal Stent Placement (31631).\nDevice: 16x40 mm Ultraflex SEMS (Uncovered).\nTechnique: \n1. Evaluation: 90% tracheal obstruction identified.\n2. Fluoroscopy: Used to verify anatomic landmarks (included).\n3. Deployment: Stent placed over guidewire.\n4. Dilation: 18mm balloon used to expand stent against tracheal wall (included in 31631).\nOutcome: Airway patent. No complications.",
            4: "Procedure: Tracheal Stent Placement\nAttending: Dr. [Name]\nSteps:\n1. Time out completed.\n2. LMA placed.\n3. Scope advanced to trachea. 90% stenosis seen.\n4. Guidewire inserted.\n5. 16x40mm Ultraflex stent deployed.\n6. Balloon dilation performed to 18mm.\n7. Good result confirmed.\nPlan: PACU.",
            5: "procedure note for tracheal stenosis we went in with the scope and saw the blockage about 90 percent so we marked it on fluoro and put the wire down. then we slid the ultraflex stent 16 by 40 over it and deployed it looked okay but needed opening so we used the elation balloon up to 18mm looks much better now airway open no bleeding patient tolerated well send to recovery.",
            6: "The procedure was performed in the bronchoscopy suite. After administration of sedatives an LMA was inserted and the flexible bronchoscope was passed through the vocal cords and into the trachea. Approximately 2.5 cm distal to the vocal cords was a long segment of A-shaped stenosis measuring 3.5 cm with maximal airway obstruction of 90%. Distal to the stenosis the mid and distal trachea appeared normal. External markers were placed on the patient’s chest with fluoroscopic observation. A 16x40 mm Ultraflex uncovered self-expandable metallic stent was then inserted over the guidewire and deployed. A 14/16.5/18 mm Elation dilatational balloon was used to dilate the stent. The bronchoscope was removed.",
            7: "[Indication]\nSymptomatic tracheal stenosis.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\n90% A-shaped stenosis identified in proximal trachea. Guidewire placed. 16x40mm Ultraflex stent deployed under fluoroscopic guidance. Post-dilation performed with 18mm balloon to secure stent apposition.\n[Plan]\nPACU. Discharge when stable.",
            8: "The patient arrived in the bronchoscopy suite and was placed under general anesthesia. We inserted the bronchoscope and immediately identified a significant 3.5 cm long stenosis in the trachea. To treat this, we utilized fluoroscopy to mark the boundaries and advanced a guidewire. An Ultraflex stent was carefully positioned and released. We then used a balloon to dilate the stent fully, restoring the airway to near-normal caliber.",
            9: "Tracheal narrowing mapped. Guidewire navigated. Prosthesis (16x40mm Ultraflex) deposited across the stricture. Lumen expanded via balloon angioplasty. Patency restored."
        },
        1: { # Note 1: Rigid bronch, TE fistula, Dual Stent (CPT 31631, 31625)
            1: "Dx: Malignant TE fistula.\nProc: Rigid bronch, Dual tracheal stenting, Biopsy.\nDetails:\n- 70% obstruction mid-trachea + TEF.\n- Rigid scope inserted.\n- Stent 1 (16x60 Aero) placed; migrated distally.\n- Biopsy of tumor taken.\n- Stent 2 (16x60 Aero) placed telescoping into first.\n- Fistula covered. Airway open.\nPlan: Tissue dx pending.",
            2: "OPERATIVE SUMMARY: The patient presented with a malignant tracheoesophageal fistula and airway compromise. Following induction, initial flexible inspection revealed 70% obstruction and a fistulous tract. A 14mm rigid tracheoscope was introduced to facilitate intervention. A 16x60mm Aero stent was deployed but situated distally. Consequently, biopsies of the exposed proximal tumor were obtained. To ensure complete exclusion of the fistula and tumor coverage, a second 16x60mm Aero stent was deployed in a telescoping fashion. This maneuver successfully recanalized the trachea and occluded the fistula.",
            3: "Procedures:\n1. 31631: Placement of tracheal stents (Two 16x60mm Aero stents used telescopically to cover long segment disease).\n2. 31625-59: Endobronchial biopsy of tumor (performed distinct from stenting on exposed tissue).\nTechnique: Rigid bronchoscopy used for airway control. Guidewire navigation. Stent deployment required telescoping technique due to distal migration of first unit. Biopsy performed with forceps.",
            4: "Resident Note\nIndication: TE Fistula/Obstruction\nAttending: Dr. X\nSteps:\n1. GA/LMA. Flex scope survey: 70% obstruction + TEF.\n2. Switched to 14mm Rigid scope.\n3. Placed 16x60 Aero stent (landed low).\n4. Biopsied tumor (forceps).\n5. Placed 2nd 16x60 Aero stent (telescoped).\n6. Confirmed patency and fistula coverage.\nPlan: Admit.",
            5: "patient has a te fistula and tumor causing blockage we tried to stent it first one went too low into the right mainstem so we pulled it back a bit but it wasnt covering the top part. gi couldnt stent the esophagus so we went back in with the rigid scope took a biopsy of the tumor then put a second aero stent inside the first one telescoping it. now the whole thing is covered and airway is open looks good.",
            6: "The procedure was performed in the main operating room. Approximately 3 cm distal to the vocal cords was a long segment of airway obstruction from extrinsic compression. At the distal aspect of the tumor there was an obvious fistulous communication with the esophagus. A 14mm non-ventilating rigid tracheoscope was inserted. A 16x60 mm Aero fully covered stent was placed but deployed distally. Biopsies were taken. A second 16X60 aero SEM was placed telescoping into the first. This resulted in complete occlusion of the fistula.",
            7: "[Indication]\nTE Fistula with malignant obstruction.\n[Anesthesia]\nGeneral (LMA converted to Rigid).\n[Description]\nRigid bronchoscopy performed. Initial 16x60mm Aero stent deployed distally. Tumor biopsied. Second 16x60mm Aero stent telescoped proximally. Fistula sealed. Trachea patent.\n[Plan]\nOncology follow-up.",
            8: "We began the procedure with a flexible inspection which confirmed a nasty tumor and fistula in the trachea. To manage this, we switched to a rigid bronchoscope. We attempted to place a covered stent, but it deployed lower than intended. We took the opportunity to biopsy the exposed tumor mass. To fix the coverage issue, we placed a second identical stent overlapping the first one. This 'telescoping' technique worked perfectly to seal the fistula and open the breathing passage.",
            9: "Tracheoesophageal defect identified. Rigid cannulation performed. Initial prosthesis deployed but migrated. Lesion sampled. Secondary prosthesis implanted in telescoping fashion. Defect occluded."
        },
        2: { # Note 2: Rigid bronch, Stent removal (CPT 31635, 31645)
            1: "Indication: Stent migration/infection.\nProc: Rigid bronch, Stent removal, Therapeutic aspiration.\nFindings: 2 stents migrated to RMB. Pus in LMB.\nActions:\n- Rigid scope inserted.\n- Aspiration of copious pus from LMB.\n- Stents grasped and removed en-bloc.\n- Esophageal stent visible/intact.\nPlan: Abx, Nebs.",
            2: "OPERATIVE REPORT: The patient presented with signs of airway stent migration and post-obstructive pneumonia. Rigid bronchoscopic evaluation revealed the previously placed tracheal stents had migrated into the right mainstem, obstructing the left. Copious purulence was noted. The left mainstem was lavaged and aspirated for therapeutic clearance and culture. Utilizing rigid forceps and the tracheoscope barrel, the migrated stents were firmly grasped and extracted in their entirety. Inspection post-removal showed erythema but no active perforation. The esophageal stent remains in situ.",
            3: "Billable Services:\n- 31635: Removal of foreign body (Two migrated tracheal stents removed via rigid scope).\n- 31645: Therapeutic aspiration (Clearance of copious post-obstructive pus from Left Mainstem).\nMedical Necessity: Stent migration causing obstruction and infection. Rigid bronchoscopy required for retrieval.",
            4: "Procedure: Stent Removal\nPatient: [Name]\nSteps:\n1. Intubation with 12mm Rigid scope.\n2. Visualized stents in RMB.\n3. Suctioned significant pus from LMB (sent for culture).\n4. Used rigid forceps to grab stents.\n5. Removed stents and scope together.\n6. Re-intubated to check airway.\nComplications: None.\nPlan: Antibiotics.",
            5: "stents moved and got infected so we had to take them out patient under general. used the rigid scope saw the stents in the right lung blocking the left. sucked out a lot of pus from the left side then grabbed the stents with the big forceps and pulled them out. airway looks red but okay esophageal stent still there covering the hole.",
            6: "The procedure was performed in the main operating room. Approximately 2 cm distal to the vocal cords the patients previous stent could be visualized. The telescoped distal tracheal stent was noted to have migrated into the right mainstem. A 12mm non-ventilating rigid tracheoscope was inserted. Bronchial lavage was performed. The proximal edge of the distal stent was secured and the stent retracted with the rigid bronchoscope. Both stents were removed. The airways were irrigated and cleaned.",
            7: "[Indication]\nStent migration and infection.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Stents found migrated to RMB. Copious pus aspirated from LMB (Therapeutic). Stents removed via rigid forceps. Esophageal stent intact.\n[Plan]\nCulture directed antibiotics.",
            8: "The patient was brought to the OR due to issues with his previous stents. Upon inserting the rigid scope, we saw the stents had slipped down into the right lung, totally blocking the left side which was full of infection. We cleaned out all the pus first. Then, grabbing the edge of the stents with heavy forceps, we pulled the whole assembly out. The airway tissue looked angry but intact.",
            9: "Prosthesis migration noted. Rigid endoscopy utilized. Purulence evacuated from obstructed bronchus. Prostheses retrieved en-bloc. Airway cleared."
        },
        3: { # Note 3: Y-stent removal, Cryotherapy (CPT 31635, 31641)
            1: "Indication: Completed stent trial.\nProc: Rigid bronch, Y-stent removal, Cryotherapy.\nFindings: Y-stent in place. Granulation tissue at distal limbs (10% R, 40% L).\nActions:\n- Stent removed en-bloc w/ rigid forceps.\n- Cryo applied to granulation tissue bilaterally.\n- Mild bleed controlled w/ epi.\nPlan: D/C.",
            2: "PROCEDURE NARRATIVE: The patient underwent scheduled removal of a silicone Y-stent following a trial for tracheobronchomalacia. A 12mm rigid tracheoscope was employed. The stent was grasped proximally and extracted without fragmentation. Post-removal inspection revealed granulation tissue at the former distal landing zones. Cryotherapy was applied systematically to these areas to reduce stenosis and ablate the tissue. Hemostasis was achieved, and the airway was deemed patent.",
            3: "Coding:\n- 31635: Removal of foreign body (Silicone Y-Stent).\n- 31641: Destruction of lesion/relief of stenosis (Cryotherapy applied to granulation tissue in mainstems).\nTechnique: Rigid bronchoscopy for removal; Flexible scope for cryo application. General anesthesia.",
            4: "Procedure: Y-Stent Removal\nSteps:\n1. Rigid scope inserted.\n2. Flexible scope check: Granulation tissue seen.\n3. Stent removed using alligator forceps.\n4. LMA placed.\n5. Cryotherapy used on granulation tissue (RMS/LMS).\n6. Bleeding controlled.\nPlan: NIV.",
            5: "patient here to get the y stent out trial over. put the rigid scope in grabbed the stent with the alligator forceps and twisted it out came out fine. looked back in with the flex scope and saw some granulation tissue where the legs were so we froze it with the cryo probe a bunch of times. little bit of bleeding stopped with epi.",
            6: "A 12 mm non-ventilating rigid tracheoscope was inserted through the mouth. The patient’s Y stent was well placed. The flexible bronchoscope was removed and the rigid optic was reinserted alongside rigid alligator forceps. The stent was subsequently removed en-bloc with the rigid bronchoscope. Once his stent was removed an I-gel LMA was then placed. The cryotherapy probe was used to perform multiple 30 second freeze thaw cycles at the areas of residual granulation tissue.",
            7: "[Indication]\nStent trial complete.\n[Anesthesia]\nGeneral.\n[Description]\nSilicone Y-stent removed via rigid bronchoscopy. Granulation tissue identified at distal strut sites. Cryotherapy destruction of granulation tissue performed. Hemostasis achieved.\n[Plan]\nDischarge.",
            8: "We proceeded to remove the patient's Y-stent as planned. Using the rigid scope, we grabbed the top of the stent and pulled it out in one piece. Afterward, we switched to a flexible scope to check the airways. There was some tissue overgrowth where the stent legs used to be, so we treated those spots with cryotherapy to freeze the tissue back. Everything looked good at the end.",
            9: "Prosthesis extraction performed via rigid technique. Granulomatous tissue identified. Lesions ablated using cryo-adhesion. Hemostasis confirmed."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock demographic data to replace 'UNKNOWN' fields in the source file.
    Provides unique names for each of the 9 style variations.
    """
    return [
        { # Note 0
            "orig_name": "Arthur Dent", 
            "orig_age": 55, 
            "names": ["Arthur Dent", "Ford Prefect", "Zaphod Beeblebrox", "Tricia McMillan", "Marvin Android", "Slartibartfast", "Vogon Jeltz", "Eddie Computer", "Deep Thought"]
        },
        { # Note 1
            "orig_name": "Ellen Ripley", 
            "orig_age": 65, 
            "names": ["Ellen Ripley", "Dwayne Hicks", "Bishop Android", "Carter Burke", "Newt Jorden", "William Hudson", "Jenette Vasquez", "Scott Gorman", "Apone Sergeant"]
        },
        { # Note 2
            "orig_name": "Rick Deckard", 
            "orig_age": 70, 
            "names": ["Rick Deckard", "Roy Batty", "Rachael Tyrell", "Pris Stratton", "Zhora Salome", "Leon Kowalski", "Eldon Tyrell", "J.F. Sebastian", "Gaff Detective"]
        },
        { # Note 3
            "orig_name": "Sarah Connor", 
            "orig_age": 45, 
            "names": ["Sarah Connor", "Kyle Reese", "T-800 Model", "John Connor", "Miles Dyson", "T-1000 Model", "Peter Silberman", "Enrique Salceda", "Janelle Voight"]
        }
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
            
            # Deep copy the original note structure to avoid modifying the template
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the specific variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation is missing (shouldn't happen with full dict)
                note_entry["note_text"] = f"Variation {style_num} for note {idx} not found."

            # Update registry_entry fields if they exist
            # Note: The source file has a specific structure where 'registry_entry' might contain 'patient_mrn', etc.
            # We need to handle the "UNKNOWN" values in the source.
            
            if "registry_entry" in note_entry:
                reg = note_entry["registry_entry"]
                
                # Update MRN
                base_mrn = f"IP2026_BRONCH_{idx}"
                reg["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
                
                # Update Procedure Date
                reg["procedure_date"] = rand_date_str
                
                # Update Patient Demographics (if structure exists, or create it)
                if "patient_demographics" not in reg or reg["patient_demographics"] is None:
                    reg["patient_demographics"] = {}
                
                reg["patient_demographics"]["age_years"] = new_age
                # Randomize gender slightly just for variety if null, otherwise keep consistent if implied
                if reg["patient_demographics"].get("gender") is None:
                     reg["patient_demographics"]["gender"] = random.choice(["Male", "Female"])

                # Update Providers (Attending)
                if "providers" in reg:
                    reg["providers"]["attending_name"] = f"Dr. {random.choice(['Smith', 'Jones', 'Doe', 'House', 'Strange'])}"

            # Add metadata about the synthetic generation
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "style_description": [
                    "Terse Surgeon", "Academic Attending", "Billing Coder", 
                    "Trainee/Resident", "Sloppy Dictation", "Header-less", 
                    "Templated", "Narrative Flow", "Synonym Swapper"
                ][style_num - 1],
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_bronch_notes_part_017.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()