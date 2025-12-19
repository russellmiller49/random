import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_028.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Contains manually crafted text variations for the 3 specific notes in bronch_notes_part_028.json.
    Keys map to the index of the note in the source list.
    """
    variations = {
        # ---------------------------------------------------------------------
        # Note 0: Tracheal Stenosis / Cryotherapy / Therapeutic Aspiration
        # ---------------------------------------------------------------------
        0: {
            1: "Indication: Tracheal stenosis.\nAnesthesia: General.\nProcedure: \n- Therapeutic scope passed through LMA.\n- Findings: Proximal tracheal stent with anterior/posterior granulation tissue. Thick mucus.\n- Action: Aspiration of all lobes (RUL, RML, RLL, LUL, LLL). Cryotherapy (2.4mm probe) applied to granulation tissue (4 cycles, 30s freeze/thaw). Tissue removed en bloc.\n- Complication: Minor oozing, stopped w/ cold saline.\n- Plan: Extubate. PACU.",
            
            2: "OPERATIVE NARRATIVE: The patient, a 29-year-old male with a history of tracheal stenosis, was brought to the operating suite. General anesthesia was induced via a laryngeal mask airway. Inspection of the proximal trachea revealed an indwelling stent with significant granulation tissue at the anterior and posterior margins, alongside inspissated mucous secretions. \n\nTherapeutic bronchoscopy was commenced. A systematic therapeutic aspiration was performed, clearing the distal trachea and all lobar segments. Subsequently, cryodebridement was utilized for the granulation tissue; a 2.4mm cryoprobe was employed for four distinct 30-second freeze-thaw cycles, successfully extracting the tissue en bloc. Hemostasis was achieved with cold saline lavage.",
            
            3: "Service: Therapeutic Bronchoscopy (31641, 31645).\nPrimary Procedure (31641): Destruction of lesion. Granulation tissue obstructing the proximal stent was identified. A 2.4mm cryoprobe was utilized to freeze and extract tissue en bloc (4 cycles). This constitutes relief of stenosis via ablative technique.\nSecondary Procedure (31645-59): Therapeutic aspiration. Distinct from the cryotherapy site, extensive mucus plugging was identified and suctioned from the distal trachea, right mainstem, and left mainstem to clear the airway.\nOutcome: Improvement in airway patency.",
            
            4: "Procedure Note\nPatient: [Name Redacted]\nAttending: Dr. Van Dyke\n\nSteps:\n1. Time out performed.\n2. General anesthesia/LMA.\n3. Scope inserted. Stent visualized with granulation tissue.\n4. Therapeutic aspiration performed in all lobes to clear mucus (31645).\n5. Cryotherapy applied to granulation tissue at proximal stent (31641). 30 sec freezes x 4.\n6. Tolerance good. No complications.\n\nPlan: Extubate, CXR.",
            
            5: "Procedure note for 29M with tracheal stenosis we did the bronch today anesthesia was general with an LMA. looked down the airway saw the stent there was some granulation tissue on the front and back and a lot of yellow mucus. so we suctioned everything out first cleaned out the lungs then used the cryo probe on the granulation tissue 4 cycles of freezing it pulled the tissue out looks much better now. tiny bit of bleeding used cold saline stopped fine extubated sent to recovery thanks.",
            
            6: "Bronchoscopy performed under general anesthesia via LMA for tracheal stenosis. Inspection revealed a tracheal stent with granulation tissue at the proximal aspect and thick mucus. Therapeutic aspiration was performed initially to clear the distal airways and lobar carinas of secretions. The granulation tissue was then addressed using a 2.4mm cryoprobe. Four cycles of 30-second freeze-thaw were applied, and tissue was removed en bloc. Minimal oozing was controlled with cold saline. The patient was extubated and transferred to recovery in stable condition.",
            
            7: "[Indication]\nTracheal stenosis with stent obstruction.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nBronchoscopy revealed granulation tissue at the proximal stent and mucous plugging. Therapeutic aspiration performed throughout the tracheobronchial tree. Cryotherapy (2.4mm probe) used to destroy and remove granulation tissue (4 cycles). Hemostasis achieved.\n[Plan]\nPathology follow-up. Clinic visit.",
            
            8: "The patient was placed under general anesthesia using an LMA for the treatment of tracheal stenosis. Upon inserting the flexible therapeutic bronchoscope, we observed a tracheal stent with granulation tissue at both the anterior and posterior aspects, as well as mild yellow mucus. We proceeded to perform therapeutic aspiration to clear the airways from the trachea down to the lobar carinas. Following this, we utilized a 2.4mm cryoprobe to treat the granulation tissue, applying four freeze-thaw cycles of 30 seconds each. The tissue was removed en bloc. Any minor bleeding was managed with cold saline, and the patient was extubated without issues.",
            
            9: "DATE OF PROCEDURE: 12/15/2025\nINDICATION: Tracheal narrowing.\nPROCEDURE: \n- Suctioning of airways (initial episode).\n- Ablation of tissue/relief of narrowing via cryotherapy.\nDETAILS: Under GA, the scope was navigated. Stent observed with overgrowth. Airways were cleared of phlegm via suction. The overgrowth was frozen and extracted using the cryoprobe (4 cycles). The airway was opened. Patient stable."
        },

        # ---------------------------------------------------------------------
        # Note 1: Tumor Obstruction / Rigid Bronch / Stent / Electrocautery
        # ---------------------------------------------------------------------
        1: {
            1: "Indication: Tumor obstruction LMS.\nProc: Rigid Bronch, Flex Bronch.\n- Mucus suctioned (RMS, Left Main).\n- LMS 100% obstructed by tumor.\n- Electrocautery knife and Microwave ablation (90C, 2 min) applied.\n- Patency restored to 100%.\n- Stent (Bonastent 10x20) placed in LLL basal segment.\n- BAL Lingula.\nComp: None.",
            
            2: "OPERATIVE REPORT: The patient, a 37-year-old male, presented with complete obstruction of the left mainstem bronchus. A rigid ventilating bronchoscope was introduced. Inspection confirmed 100% occlusion of the LMS by malignant tissue. Multimodal debulking was performed utilizing electrocautery (PreciSect) and microwave ablation (2 minutes at 90C). Post-intervention, airway patency was restored to 100%. To maintain patency in the lower lobe, a 10x20mm Bonastent was deployed in the LLL basal segment. A bronchoalveolar lavage was obtained from the Lingula for microbiologic analysis.",
            
            3: "Coding Justification:\n31641: Destruction of tumor. Rigid bronchoscopy used to access LMS. Electrocautery and Microwave energy used to ablate 100% obstruction.\n31636-XS: Stent placement. Distinct site: LLL basal segment. Bonastent deployed to maintain patency.\n31645-XS: Therapeutic aspiration. Performed in contralateral lung (Right Mainstem) and distal LUL.\n31624-XS: BAL. Performed in Lingula (LB4/LB5), distinct from therapeutic sites.",
            
            4: "Procedure Note - Tumor Debulking\nPatient: [Name Redacted]\nStaff: Dr. Johnson\n\n1. General Anesthesia. Rigid scope inserted.\n2. Suctioned airways (31645).\n3. Identified 100% LMS obstruction.\n4. Used Electrocautery and Microwave to ablate tumor (31641).\n5. Airway now open.\n6. Placed Bonastent in LLL (31636).\n7. Did BAL of Lingula (31624).\n8. Patient stable.",
            
            5: "We did a rigid bronchoscopy on this 37 year old guy for the tumor blocking his left mainstem. used general anesthesia suctioned out a bunch of mucus first from the right side and the left. The tumor was blocking 100 percent of the airway so we used the electrocautery knife and the microwave probe to burn it out. opened it up completely 100 percent patent now. put a bonastent in the left lower lobe to keep it open. also did a lavage of the lingula sent it for cultures no complications.",
            
            6: "Rigid and flexible bronchoscopy performed for tumor obstruction. Initial therapeutic aspiration cleared the right and left mainstems. The left mainstem was noted to be 100% obstructed by tumor. This was treated with electrocautery knife and microwave ablation (90C for 3.5 min total), restoring patency to 100%. A 10x20mm Bonastent was deployed in the LLL basal segment. Bronchoalveolar lavage was performed in the Lingula (LB4/5). Patient tolerated the procedure well.",
            
            7: "[Indication]\nMalignant airway obstruction (LMS).\n[Anesthesia]\nGeneral, Rigid Scope.\n[Description]\nTherapeutic aspiration performed. LMS tumor treated with Electrocautery and Microwave ablation. Patency restored from 0% to 100%. Bonastent deployed in LLL. BAL performed in Lingula.\n[Plan]\nStent hydration protocol. Clinic f/u.",
            
            8: "Mr. [Name] underwent rigid bronchoscopy for management of a left mainstem tumor. We initially cleared secretions from the right and left mainstems. The left mainstem was found to be completely obstructed. We utilized an electrocautery knife and microwave ablation to debulk the tumor, successfully restoring full airway patency. Following this, we placed a Bonastent (10x20) in the left lower lobe basal segment to ensure continued airflow. Finally, we performed a bronchoalveolar lavage of the Lingula to check for infection.",
            
            9: "PROCEDURE: Bronchoscopy with tumor destruction, stenting, aspiration, and lavage.\nDETAILS: Used rigid scope. Vacuumed mucus from airways. The blockage in the Left Mainstem was vaporized using heat (electrocautery/microwave). The blockage was cleared. An airway prosthesis (stent) was implanted in the LLL. The Lingula was washed (lavaged) for samples."
        },

        # ---------------------------------------------------------------------
        # Note 2: Percutaneous Tracheostomy / Ultrasound / Mod 22
        # ---------------------------------------------------------------------
        2: {
            1: "Indication: Respiratory failure.\nProc: Percutaneous Tracheostomy (31600-22), US Neck (76536).\n- US Neck: No vessels/mass at site.\n- Incision: 1cm inf to cricoid.\n- Needle/Wire/Dilator (Blue Rhino) technique used under bronch guidance.\n- 7.0 Portex Trach placed.\n- Note: 22 Modifier. Limited neck mobility/difficult anatomy required 4 attendings and >40% extra effort.",
            
            2: "OPERATIVE NOTE: The patient presented with respiratory failure requiring long-term airway access. A percutaneous dilational tracheostomy was performed. Bedside ultrasound of the neck was utilized to rule out vascular anomalies. Due to the patient's limited neck mobility and challenging anatomy, the procedure required significantly increased effort (>40% increase) and the assistance of multiple attending physicians. Under bronchoscopic visualization, the trachea was accessed between the 1st and 2nd rings. Serial dilation was performed using the single-stage dilator. A 7.0 cuffed tracheostomy tube was placed and confirmed patent.",
            
            3: "Coding Summary:\n31600-22: Percutaneous tracheostomy. Modifier 22 applied due to substantial additional work (>40% increased time/intensity) caused by limited neck mobility and difficult anatomy requiring multiple attendings.\n76536: Ultrasound of neck. Diagnostic exam performed to evaluate vessels/structures prior to incision.\nTechnique: Ciaglia Blue Rhino method under bronchoscopic guidance.",
            
            4: "Procedure: Perc Trach\nPatient: [Name Redacted]\n1. Time out. GA.\n2. Ultrasound neck (neg for vessels).\n3. Bronch into ETT.\n4. Difficult anatomy noted (stiff neck). Needed extra help.\n5. Needle into trachea -> Wire -> Dilators.\n6. 7.0 Trach tube inserted.\n7. Confirmed position with scope.\n8. Sutured in place.",
            
            5: "Did a perc trach on this 63 year old guy for resp failure. it was a really hard case the neck wouldnt move much so we had a hard time getting the angle right had to have 4 attendings helping out definitely took way longer than normal more than 40 percent more work. used ultrasound first to check for veins. stuck the needle in dilated it up put the 7.0 tube in confirmed with the bronch everything looks good now.",
            
            6: "Percutaneous tracheostomy performed under general anesthesia. Diagnostic ultrasound of the neck was negative for intervening vessels. Due to limited neck mobility, the procedure was technically challenging and required significantly increased physician effort and time (>40%). Under bronchoscopic guidance, the trachea was accessed via the 1st/2nd interspace. The tract was dilated using a White Rhino dilator. A 7.0 Portex tracheostomy tube was inserted and position confirmed. The ETT was removed.",
            
            7: "[Indication]\nRespiratory Failure.\n[Anesthesia]\nGeneral.\n[Description]\nNeck Ultrasound performed. Percutaneous tracheostomy performed using Seldinger technique and serial dilation under bronchoscopic visualization. 7.0 Tube placed.\n[Modifier Note]\nDifficult anatomy (limited neck mobility) required substantial extra work and multiple attendings.\n[Plan]\nSuture removal 7 days.",
            
            8: "We performed a percutaneous tracheostomy for this patient with respiratory failure. Before starting, we used ultrasound to scan the neck and ensure there were no blood vessels in the way. The procedure was notably difficult because the patient had very limited neck mobility, which made access hard; this required four attending physicians and significantly more time and effort than a standard case. We successfully placed a 7.0 tracheostomy tube using the dilational technique under direct bronchoscopic vision.",
            
            9: "PROCEDURE: Creation of tracheal airway (tracheostomy) with ultrasound scan.\nDETAILS: Scanned neck to check safety. Access was challenging due to stiff neck, requiring extra effort and staff. Created incision. Inserted needle and wire. Stretched opening with dilator. Inserted breathing tube (7.0 Portex). Verified position with camera. Secured tube."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the user's requested data masking.
    # Note Indices: 0 = Mohammad Alkrad, 1 = Tyler Scott Luna, 2 = Andres Flores Luna
    return [
        {
            "idx": 0, 
            "orig_name": "Mohammad Alkrad", 
            "orig_age": 29, 
            "names": ["John Vance", "Arthur Higgins", "Robert Kinsley", "William O'Connor", "James P. Miller", "Edward Stone", "Richard Davis", "Thomas Clark", "Gary Wright"]
        },
        {
            "idx": 1, 
            "orig_name": "Tyler Scott Luna", 
            "orig_age": 37, 
            "names": ["Sarah Jenkins", "Linda Carter", "Nancy Hughes", "Karen Smith", "Barbara Lopez", "Mary Ann Davidson", "Susan White", "Margaret Lewis", "Betty King"]
        },
        {
            "idx": 2, 
            "orig_name": "Andres Flores Luna", 
            "orig_age": 63, 
            "names": ["Michael Foster", "Robert G. Turner", "David Myers", "Joseph Anderson", "Frank Mitchell", "Paul Reynolds", "George Baker", "Kenneth Roberts", "Steven Phillips"]
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
            
            # Update registry_entry fields if they exist
            # Note: The structure of bronch_notes_part_028 is slightly different from part_069
            if "registry_entry" in note_entry:
                # Update Date
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN (handle if it exists or create one)
                current_mrn = note_entry["registry_entry"].get("patient_mrn", "UNKNOWN")
                note_entry["registry_entry"]["patient_mrn"] = f"{current_mrn}_syn_{style_num}"
                
                # Update Age and Name (Nested inside patient_demographics)
                if "patient_demographics" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                    # There isn't a specific 'name' field in the registry_entry schema shown, 
                    # but usually, we update the MRN. If name is embedded in text, the variation handles it.
            
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
    output_filename = output_dir / "synthetic_bronch_notes_part_028.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()