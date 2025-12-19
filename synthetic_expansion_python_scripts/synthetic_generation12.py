import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_012.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns the dictionary of manually crafted text variations.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Therapeutic Aspiration (Mucus) - CPT 31645
            1: "Indication: RLL obstruction.\nAnesthesia: Conscious sedation (Fentanyl/Versed).\nProcedure:\n- Scope passed.\n- Findings: Diffuse tracheobronchitis, thick yellow mucus plugs bilaterally.\n- Action: Extensive suctioning of mucous plugs to clear airways (31645).\n- Wash: RLL lateral segment lavage performed.\nComplications: None.",
            2: "OPERATIVE REPORT\n\nINDICATION: The patient presented with radiographic evidence of right lower lobe obstruction.\n\nPROCEDURE: Flexible bronchoscopy with therapeutic aspiration.\n\nNARRATIVE: Following informed consent and the administration of moderate sedation, the bronchoscope was introduced via the left naris. Examination revealed diffuse, erythematous tracheobronchitis accompanied by tenacious, yellow mucous plugging throughout the bronchial tree. Therapeutic aspiration was performed, systematically clearing these secretions from the segmental bronchi. A bronchial wash was obtained from the right lower lobe lateral segment for microbiological analysis. The patient tolerated the procedure well.",
            3: "Procedure: Therapeutic Bronchoscopy (31645).\nMedical Necessity: Patient presented with RLL segmental obstruction.\nTechnique: Flexible bronchoscope advanced. Visualization confirmed diffuse mucous plugging causing airway obstruction. Suction was utilized to aspirate thick mucus plugs from bilateral bronchial trees, restoring airway patency. A separate bronchial wash was collected. Diagnostic inspection (31622) is bundled.",
            4: "Procedure Note\nAttending: [Name]\nResident: [Name]\n\nIndication: RLL obstruction.\n\nProcedure Steps:\n1. Time out performed.\n2. Moderate sedation administered.\n3. Scope inserted through left nare.\n4. Airway inspection showed diffuse tracheobronchitis and significant mucous plugging.\n5. Therapeutic aspiration of mucus plugs performed bilaterally.\n6. RLL washing obtained.\n\nPlan: Await cultures.",
            5: "Procedure note patient came in with RLL obstruction we gave fentanyl and versed for sedation scope went in fine saw a lot of thick yellow mucus everywhere diffuse bronchitis really boggy mucosa. We spent time suctioning out all the plugs to clear the airways and then did a wash in the RLL lateral segment couldn't get a wedge cause he was coughing. No bleeding toleratd well send cultures.",
            6: "After appropriate consent was obtained the patient was sedated with Fentanyl and Versed and the bronchoscope was inserted. The vocal cords moved normally. Upon entering the trachea mild tracheomalacia was noted along with diffuse tracheobronchitis and thick yellow mucous plugs extending throughout the right and left bronchial trees. Therapeutic aspiration was performed to remove these mucous plugs. Inspection was performed to the subsegmental level. A bronchial wash was performed in the RLL lateral segment. No lesions were seen. The patient tolerated the procedure without complication.",
            7: "[Indication]\nRight lower lobe segmental obstruction, mucous plugging.\n[Anesthesia]\nConscious sedation (Fentanyl 100mcg, Versed 4mg).\n[Description]\nFlexible bronchoscopy performed. Diffuse tracheobronchitis and thick yellow mucus identified throughout bilateral airways. Therapeutic aspiration of mucus plugs completed. RLL lateral segment wash obtained.\n[Plan]\nMonitor for resolution. Await culture results.",
            8: "The patient was brought to the endoscopy suite for evaluation of a right lower lobe obstruction. After the administration of local anesthesia and conscious sedation, the bronchoscope was navigated through the upper airway. We observed mild tracheomalacia and significant inflammation consistent with tracheobronchitis. Thick, yellow mucous plugs were visualized throughout the bronchial tree. We proceeded to suction these plugs to clear the airways. A specific wash was collected from the right lower lobe. The procedure concluded without adverse events.",
            9: "PREOPERATIVE DIAGNOSIS: Right lower lobe segmental blockade.\nPROCEDURE: Flexible bronchoscopy with airway clearance.\nDETAILS: After obtaining consent, the scope was introduced. We observed diffuse inflammation and heavy secretions. We extracted the mucous plugs via suction from both the right and left sides. We also sampled the RLL via lavage. No masses were visualized. The patient withstood the procedure well."
        },
        1: { # Complex Stent FB Removal + Y-Stent - CPT 31636, 31637, 31635
            1: "Dx: Esophageal stent migration to airway.\nAnesthesia: GA.\nProcedure:\n- Flex bronch: Stent visualized blocking distal trachea/LMS. Pus suctioned.\n- Rigid bronch (14mm): Inserted.\n- Removal: Migrated esophageal stent and clips removed piecemeal (forceps/scissors).\n- Repair: TE fistula identified. 13x10x10 Dynamic Y-stent placed to cover defect.\n- Airway secured with ETT.\nComplications: TE fistula extension.",
            2: "OPERATIVE NARRATIVE: The patient presented with airway obstruction secondary to a migrated esophageal stent. Under general anesthesia, rigid bronchoscopy was utilized. The esophageal prosthesis was found protruding into the distal trachea and occluding the left mainstem. Using rigid forceps and optical scissors, the foreign body was disassembled and extracted piecemeal to relieve the obstruction (CPT 31635). Examination revealed a significant tracheoesophageal fistula. To manage the airway and fistula, a Dynamic Y-stent was deployed, stenting the trachea and bilateral mainstems (CPT 31636, 31637). The airway was secured with an endotracheal tube post-deployment.",
            3: "Coding Summary:\n- 31635: Bronchoscopy with removal of foreign body (Migrated esophageal stent and clips removed via rigid scope).\n- 31636: Placement of bronchial stent, initial bronchus (Y-stent tracheal/bronchial limb).\n- 31637: Placement of bronchial stent, additional bronchus (Y-stent contralateral limb).\nNote: Procedure required rigid bronchoscopy due to complexity and need for piecemeal extraction.",
            4: "Procedure: Rigid Bronchoscopy, FB Removal, Stent Placement.\nIndication: Migrated esophageal stent.\nSteps:\n1. GA induced, LMA placed.\n2. Flex bronch showed stent occluding trachea/LMS.\n3. Rigid bronch inserted.\n4. Foreign body (esophageal stent) removed using forceps and APC.\n5. Large TE fistula noted.\n6. Dynamic Y-stent deployed to cover fistula and patent airway.\n7. ETT placed through stent.",
            5: "Patient has a migrated esophageal stent in the airway causing obstruction so we went to the OR for rigid bronchoscopy. Under GA we saw the stent sticking into the trachea and blocking the left side. We used the rigid scope and forceps to pull the stent out it broke apart so we had to take it out in pieces. There was a big hole between the trachea and esophagus so we put in a Y stent to cover it. It was hard to place but we got it in eventually. Intubated through the stent at the end.",
            6: "Under general anesthesia a therapeutic flexible bronchoscope visualized an esophageal stent protruding into the distal trachea and left mainstem. A 14mm rigid bronchoscope was inserted. The foreign body was removed piecemeal using forceps and scissors. Following removal a large tracheoesophageal fistula was evident. A 13x10x10mm Dynamic Y-stent was deployed to bridge the defect and maintain airway patency involving the trachea and both mainstem bronchi. An ETT was placed through the stent for ventilation.",
            7: "[Indication]\nLeft mainstem obstruction via migrated esophageal stent.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nRigid bronchoscopy performed. Esophageal stent found eroding into airway. Foreign body removed piecemeal using rigid techniques. Resultant TE fistula identified. Dynamic Y-stent placed to stent trachea and bilateral bronchi. Airway secured.\n[Plan]\nICU monitoring. Keep intubated.",
            8: "We performed a complex airway intervention for a patient with a migrated esophageal stent. Upon inspection, the stent was found compromising the distal trachea and left mainstem. We utilized rigid bronchoscopy to carefully extract the stent fragments and associated clips. This process revealed a significant tracheoesophageal fistula. To restore airway integrity and cover the defect, we deployed a silicone Y-stent, ensuring limbs were seated in the right and left mainstems. The patient was intubated through the stent for post-op management.",
            9: "DIAGNOSIS: Airway blockade due to prosthesis migration.\nPROCEDURE: Rigid endoscopy with retrieval of foreign material and prosthetic implantation.\nDETAILS: We identified the esophageal device obstructing the airway. Using heavy graspers, we extracted the device in sections. A fistula was noted. We implanted a Y-shaped silicone prosthesis to scaffold the airway and cover the defect. Ventilation was established via an endotracheal tube."
        },
        2: { # Whole Lung Lavage - CPT 32997
            1: "Indication: PAP, hypoxia.\nAnesthesia: GA, Left DLT.\nProcedure:\n- DLT placed, isolation confirmed.\n- Left Whole Lung Lavage initiated.\n- 1L aliquots warm saline instilled/drained.\n- Total 8L instilled. Effluent cleared.\n- Extubated to NiPPV.\nComplications: Transient hypoxia/agitation.",
            2: "OPERATIVE REPORT: The patient with pulmonary alveolar proteinosis presented for therapeutic whole lung lavage. Following induction of general anesthesia, a left-sided double-lumen tube was placed and position verified bronchoscopically to ensure lung isolation. We proceeded with large-volume lavage of the left lung using warm saline in 1-liter aliquots. Percussion was applied to facilitate clearance. A total of 8 liters was instilled with excellent clearing of the proteinaceous effluent. The patient was extubated and transferred to the ICU.",
            3: "Service: Total Lung Lavage (32997).\nSide: Unilateral (Left).\nTechnique: Double-lumen endotracheal tube placement with bronchoscopic confirmation (bundled). Instillation of 8 liters of saline with gravity drainage and chest physiotherapy until effluent cleared.\nIndication: Pulmonary Alveolar Proteinosis.",
            4: "Procedure: Left Whole Lung Lavage\nIndication: PAP\nSteps:\n1. GA, Left DLT placed.\n2. Confirmed isolation with scope.\n3. Instilled 1L saline aliquots.\n4. Chest PT performed.\n5. Drained fluid (milky -> clear).\n6. Repeated for 8L total.\n7. Extubated.\nDisposition: ICU for monitoring.",
            5: "Procedure note for whole lung lavage on the left side patient has PAP. We put in a double lumen tube checked it with the scope. Started running warm saline into the left lung 1 liter at a time. Fluid came out really milky at first. We did chest percussion. After about 8 liters the fluid looked clear so we stopped. Patient woke up a bit wild and hypoxic so we sent them to the ICU instead of the floor.",
            6: "Under general anesthesia a left-sided double-lumen endotracheal tube was placed and isolation was confirmed bronchoscopically. The patient was positioned and 1 liter of warm saline was instilled into the left lung followed by chest percussion and drainage. This cycle was repeated until 8 liters had been instilled and the effluent cleared of sediment. The procedure was terminated and the patient was extubated and transferred to the ICU for observation of hypoxia.",
            7: "[Indication]\nDyspnea/Hypoxia due to Pulmonary Alveolar Proteinosis.\n[Anesthesia]\nGeneral, Left DLT.\n[Description]\nLeft whole lung lavage performed. 8L warm saline instilled in aliquots with chest physiotherapy. Drainage progressed from cloudy/sediment-rich to clear. DLT removed.\n[Plan]\nICU admission for respiratory monitoring.",
            8: "The patient underwent a left whole lung lavage for symptomatic pulmonary alveolar proteinosis. We secured the airway with a double-lumen tube to isolate the lungs. We then systematically lavaged the left lung with warm saline, utilizing chest percussion to mobilize the sediment. Initial returns were opaque, but after 8 liters of lavage, the fluid ran clear. We concluded the procedure and transferred the patient to the intensive care unit for post-anesthesia recovery.",
            9: "DIAGNOSIS: Alveolar Proteinosis.\nPROCEDURE: Unilateral total lung washing.\nDETAILS: Under anesthesia, we isolated the lungs. We flooded the left lung with saline solution and applied percussion. The returned fluid was initially turbid but clarified after multiple cycles. We completed the cleansing and removed the airway tube. The patient required close monitoring post-op."
        },
        3: { # Pediatric Stent Removal & Cryo - CPT 31641, 31635
            1: "Indication: Stent obstruction (granulation).\nAnesthesia: GA, LMA.\nProcedure:\n- Flex/Rigid bronch.\n- Y-stent removed intact via rigid forceps (31635).\n- Cryotherapy applied to LMS granulation tissue (31641).\n- Airway patent post-procedure.\nPlan: PACU -> Peds ward.",
            2: "OPERATIVE NARRATIVE: The patient, a pediatric male with a mediastinal mass, presented for airway stent management. Under general anesthesia, bronchoscopy revealed granulation tissue partially obstructing the left mainstem limb of the Y-stent. A rigid bronchoscope was utilized to grasp and extract the Y-stent intact (Foreign Body Removal). Following stent removal, flexible cryotherapy was applied to the residual granulation tissue in the left mainstem to destroy the obstruction (Destruction of Tumor/Stenosis). The airway was patent at the conclusion.",
            3: "Codes:\n- 31635: Removal of foreign body (Tracheal Y-stent removal via rigid scope).\n- 31641: Bronchoscopy with destruction of tumor/stenosis (Cryotherapy to LMS granulation tissue).\nRationale: Procedure involved removal of indwelling hardware and separate ablative treatment of tissue obstruction.",
            4: "Procedure: Stent Removal, Cryotherapy\nIndication: Stent obstruction\nSteps:\n1. GA, LMA.\n2. Flex bronch: Granulation in LMS.\n3. Rigid bronch inserted.\n4. Y-stent removed using forceps.\n5. Flex bronch re-inserted.\n6. Cryotherapy (3 cycles) to LMS granulation.\n7. Good result.",
            5: "Patient is a kid with a Y stent that has granulation tissue blocking it. We did this in the OR with general anesthesia. Went in with the flex scope saw the tissue. Switched to rigid scope grabbed the stent and pulled it out spinning it a bit it came out whole. Then went back with the flex scope and used the cryo probe to freeze the granulation tissue in the left mainstem. No bleeding everything looks okay.",
            6: "The patient was brought to the operating room for stent management. General anesthesia was induced. Diagnostic bronchoscopy showed granulation tissue in the left mainstem limb of the Y-stent. A rigid tracheoscope was inserted and the stent was removed intact using rigid forceps. Following removal flexible bronchoscopy with cryotherapy was performed to ablate the granulation tissue in the left mainstem. The procedure was uncomplicated.",
            7: "[Indication]\nAirway stent obstruction, resolving mediastinal mass.\n[Anesthesia]\nGeneral, LMA/Rigid.\n[Description]\nRigid bronchoscopy used to remove tracheal Y-stent (foreign body). Flexible bronchoscopy with cryotherapy performed to debulk granulation tissue in the left mainstem. Airway patency restored.\n[Plan]\nAdmit to pediatric ward.",
            8: "We performed a combined rigid and flexible bronchoscopy to manage this patient's airway stent. The Y-stent was found to be obstructed by granulation tissue in the left mainstem. We successfully extracted the stent using rigid instrumentation. Once the stent was out, we treated the underlying granulation tissue with cryotherapy to open the airway further. The patient remained stable and was transferred to the pediatric unit.",
            9: "DIAGNOSIS: Stent blockage.\nPROCEDURE: Rigid endoscopy for prosthesis retrieval and cryo-ablation.\nDETAILS: We accessed the airway and confirmed tissue overgrowth. The Y-prosthesis was gripped and withdrawn using the rigid tube. We then applied freezing energy to the tissue obstructing the left bronchus to clear the passage. The patient recovered without incident."
        },
        4: { # TBM Stent Removal & Cryo/Asp - CPT 31641, 31635, 31645
            1: "Indication: Stent obstruction, TBM.\nAnesthesia: GA, Rigid.\nProcedure:\n- Rigid bronch.\n- Suctioned purulent secretions LLL/RLL (31645).\n- Removed Y-stent intact (31635).\n- Cryotherapy to RMB/LMB granulation (31641).\n- TBM collapse noted.\nPlan: Stent holiday.",
            2: "OPERATIVE REPORT: The patient with severe tracheobronchomalacia presented with stent obstruction. Rigid bronchoscopy was performed. Initially, copious purulent secretions were aspirated from the lower lobes to clear the airway (Therapeutic Aspiration). The indwelling Y-stent was then grasped and removed intact via the rigid scope (Foreign Body Removal). Inspection revealed granulation tissue causing stenosis in the bilateral mainstems, which was treated with cryotherapy (Destruction of Stenosis). Significant dynamic collapse was noted post-removal.",
            3: "Coding Summary:\n- 31635: Removal of foreign body (Y-stent).\n- 31641: Destruction of stenosis (Cryotherapy to RMB/LMB granulation).\n- 31645-59: Therapeutic aspiration (Clearance of copious purulent secretions from lower lobes, distinct from stent/cryo sites).\nMedical Necessity: Management of stent complications and infection.",
            4: "Procedure: Stent Removal, Cryo, Aspiration\nIndication: Stent obstruction\nSteps:\n1. GA, Rigid scope.\n2. Flex scope through rigid.\n3. Suctioned thick pus from lower lobes.\n4. Removed Y-stent with rigid forceps.\n5. Cryotherapy to granulation in RMB/LMB.\n6. Observed TBM collapse.\nPlan: Stent holiday.",
            5: "Procedure note for stent removal. Patient has TBM and the stent was getting blocked. We put them under GA used the rigid scope. First we had to suck out a ton of pus from the lower lobes it was really thick. Then we grabbed the stent and pulled it out. There was granulation tissue on both sides so we froze it with the cryo probe. Airway collapses a lot without the stent but we are doing a holiday.",
            6: "Under general anesthesia a rigid tracheoscope was inserted. Flexible inspection revealed purulent secretions which were aspirated from the lower lobes. The tracheal Y-stent was removed intact using rigid forceps. Granulation tissue causing stenosis in the right and left mainstems was treated with cryotherapy. Significant tracheobronchomalacia was observed following stent removal. The patient was transferred to the ward for a stent holiday.",
            7: "[Indication]\nAirway stent obstruction, TBM.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nTherapeutic aspiration of purulent secretions performed. Tracheal Y-stent removed via rigid bronchoscopy. Cryotherapy applied to granulation tissue in bilateral mainstems. TBM collapse documented.\n[Plan]\nStent holiday. Monitor symptoms.",
            8: "We brought the patient to the OR to manage an obstructed airway stent. Using the rigid bronchoscope, we first cleared significant purulent secretions from the distal airways. We then successfully removed the Y-stent. To address the stenosis caused by granulation tissue at the stent ends, we applied cryotherapy. The airway showed marked collapse consistent with the underlying malacia. We plan to observe the patient without the stent for now.",
            9: "DIAGNOSIS: Malacia and stent blockage.\nPROCEDURE: Rigid endoscopy, prosthesis extraction, cryo-ablation, and mucus clearance.\nDETAILS: We cleared heavy secretions from the lungs. The indwelling prosthesis was extracted. We used freezing therapy to reduce the tissue growth in the main bronchi. The airway exhibited collapse. A stent-free period is planned."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data for the 5 notes in bronch_notes_part_012.json.
    Assigns names and ages to generate consistent synthetic identities.
    """
    return [
        {"idx": 0, "orig_name": "Arthur Dent", "orig_age": 65, "names": ["John Smith", "Robert Jones", "Michael Brown", "David Wilson", "Richard Taylor", "Joseph Anderson", "Thomas Thomas", "Charles Martinez", "Christopher Hernandez"]},
        {"idx": 1, "orig_name": "Ford Prefect", "orig_age": 55, "names": ["Daniel White", "Matthew Lopez", "Anthony Gonzalez", "Mark Moore", "Donald Jackson", "Steven Martin", "Paul Lee", "Andrew Perez", "Joshua Thompson"]},
        {"idx": 2, "orig_name": "Zaphod Beeblebrox", "orig_age": 45, "names": ["Kenneth White", "Kevin Harris", "Brian Sanchez", "George Clark", "Edward Ramirez", "Ronald Lewis", "Timothy Robinson", "Jason Walker", "Jeffrey Young"]},
        {"idx": 3, "orig_name": "Trillian Astra", "orig_age": 12, "names": ["Sarah Hall", "Jessica Allen", "Emily King", "Ashley Wright", "Jennifer Scott", "Amanda Torres", "Melissa Nguyen", "Stephanie Hill", "Nicole Flores"]},
        {"idx": 4, "orig_name": "Marvin Android", "orig_age": 70, "names": ["Elizabeth Green", "Heather Adams", "Tiffany Nelson", "Andrea Baker", "Julie Roberts", "Jamie Mitchell", "Mary Carter", "Christina Phillips", "Rachel Evans"]}
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
        if idx not in variations_text:
            print(f"Warning: No variations found for note index {idx}. Skipping.")
            continue
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Iterate through the 9 styles
        for style_num in range(1, 10):
            
            # Deep copy the original note structure
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            if new_age < 1: new_age = 1 # Ensure no negative/zero ages
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                re = note_entry["registry_entry"]
                
                # Update demographic info if patient_demographics exists
                if "patient_demographics" in re and re["patient_demographics"] is not None:
                    re["patient_demographics"]["age_years"] = new_age
                # Fallback or additional age field
                if "patient_age" in re: 
                    re["patient_age"] = new_age
                    
                if "procedure_date" in re:
                    re["procedure_date"] = rand_date_str
                
                # Update MRN
                if "patient_mrn" in re:
                    base_mrn = re["patient_mrn"] if re["patient_mrn"] != "UNKNOWN" else f"IP_SYN_{idx}"
                    re["patient_mrn"] = f"{base_mrn}_style_{style_num}"
                else:
                    re["patient_mrn"] = f"IP_SYN_{idx}_style_{style_num}"

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
    output_filename = output_dir / "synthetic_bronch_notes_part_012.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()