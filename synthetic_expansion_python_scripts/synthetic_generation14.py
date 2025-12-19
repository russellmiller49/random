import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_014.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations for the 4 notes in bronch_notes_part_014.json
    # Structure: Note_Index (0-3) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Note 0: Left Mainstem Stent for Fistula (CPT 31636, 31625)
            1: "Indication: Broncho-esophageal fistula.\nProcedure: Stent placement, Biopsy.\n- Airways inspected. Purulent secretions cleared.\n- Right airway nodules seen.\n- Left mainstem (LMS) 1.5cm fistula identified posterior wall.\n- Distal left nodules seen.\n- Biopsies taken from right and left nodules.\n- 14x30mm Aero stent placed over wire. Position slightly proximal.\n- Second 14x40mm Aero stent placed; migrated distally, obstructed lobes.\n- 14x40mm stent removed via trach stoma.\n- Original 14x30mm stent repositioned to cover fistula successfully.\nPlan: ICU, CXR, saline nebs.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the operating room for management of a persistent broncho-esophageal fistula. Following the induction of general anesthesia, flexible bronchoscopy was performed via the tracheostomy. Examination revealed purulence and multiple nodular lesions in the right bronchial tree, highly suspicious for metastatic disease. Attention was turned to the left mainstem bronchus, where a 1.5 cm fistula was visualized on the medial posterior wall. Similar nodularity was noted distally. Biopsies were obtained from bilateral sites. Therapeutic intervention ensued with the deployment of a 14x30 mm Aero self-expanding metallic stent. Due to suboptimal proximal coverage, a secondary 14x40 mm stent was deployed, which inadvertently displaced the primary stent distally, compromising lobar patency. This necessitated the removal of the second stent through the tracheostomy stoma. The primary 14x30 mm stent was subsequently repositioned with forceps to achieve optimal fistula exclusion. The airway was patent upon conclusion.",
            3: "Procedures Performed:\n1. Bronchoscopy with bronchial stent placement (31636). Indication: LMS Fistula. Device: Aero 14x30mm. Note: Initial deployment required revision; a secondary stent was placed but removed due to migration. Final successful placement of the 14x30mm stent achieved coverage of the 1.5cm defect.\n2. Bronchoscopy with endobronchial biopsy (31625). Locations: Right airway nodules and Left distal airway nodules. These are distinct lesions separate from the fistula site.\nTechnique: Fluoroscopic guidance utilized for marker placement and stent deployment. Rigid forceps utilized for stent manipulation.",
            4: "Procedure Note\nAttending: [Name]\nResident: [Name]\nIndication: B-E Fistula\n\nSteps:\n1. Time out performed. GA induced.\n2. Flex scope via trach. Suctioned purulence.\n3. Identified 1.5cm fistula in Left Mainstem.\n4. Noted nodules R and L sides -> Biopsied (forceps).\n5. Marked fistula with fluoroscopy.\n6. Deployed 14x30 Aero stent. Coverage suboptimal.\n7. Placed 14x40 Aero. Resulted in distal migration/obstruction.\n8. Removed 14x40 stent via stoma.\n9. Repositioned 14x30 stent to cover fistula.\n10. Final check: Good position.\nPlan: ICU, CXR.",
            5: "We went to the OR for the fistula patient had general anesthesia used the trach tube for access. Saw a lot of pus and suctioned it out there were nodules on the right and left looked like cancer so we biopsied them. Then saw the hole in the left mainstem about 1.5cm. We put in a wire and markers and dropped a 14x30 Aero stent it was a little high so put a 14x40 inside it but that pushed the first one down and blocked the lung so we had to pull the big one out through the trach hole. After that we grabbed the first stent with forceps and pulled it back up to cover the fistula perfectly. Sent to ICU.",
            6: "The procedure was performed in the main operating room under general anesthesia. A flexible bronchoscope was passed through the tracheostomy. Purulent secretions were suctioned. Multiple nodules were seen in the right and distal left airways; biopsies were taken. A 1.5cm fistula was identified in the mid-left mainstem. Using fluoroscopic guidance, a 14x30 mm Aero stent was deployed. Coverage was deemed insufficient, so a 14x40 mm stent was placed, which unfortunately pushed the assembly distally, obstructing lobar orifices. The 14x40 stent was extracted via the stoma. The remaining 14x30 stent was retracted into proper position covering the fistula. The patient was transferred to the ICU.",
            7: "[Indication]\nBroncho-esophageal fistula refractory to esophageal stenting.\n[Anesthesia]\nGeneral Anesthesia via tracheostomy.\n[Description]\nDiagnostic inspection revealed purulence and bilateral airway nodules; biopsies were obtained. The 1.5cm LMS fistula was targeted. A 14x30mm Aero stent was deployed. Attempted extension with a 14x40mm stent caused distal migration and obstruction. The 14x40mm stent was removed. The 14x30mm stent was successfully repositioned to cover the defect.\n[Plan]\nAdmit to ICU. Humidified O2. Post-op CXR.",
            8: "The patient arrived in the operating room for repair of a broncho-esophageal fistula. Under general anesthesia, we navigated the bronchoscope through the tracheostomy. We encountered purulent secretions and suspicious nodules bilaterally, which were sampled using flexible forceps. Focusing on the left mainstem, we identified the 1.5 cm fistula. We deployed a 14x30 mm Aero stent, but placement was slightly proximal. An attempt to extend coverage with a second 14x40 mm stent resulted in distal migration and obstruction of the left lung lobes. We managed this by extracting the second stent through the stoma and carefully retracting the original 14x30 mm stent into the correct position to seal the fistula.",
            9: "The procedure was executed in the main operating room. After delivery of sedatives, a flexible bronchoscope was navigated through the tracheostomy. The trachea was normal. Purulent secretions were evacuated. Inspection of the right airways revealed nodules which were sampled. On the left, a 1.5cm fistula was visualized. Distal nodules were also sampled. We deployed an Aero 14x30 mm stent over a guidewire. To optimize coverage, a second 14x40 stent was inserted, but it displaced the first stent distally. We extracted the 14x40 stent via the stoma and repositioned the remaining 14x30 mm stent to occlude the fistula. The patient was transferred to the ICU."
        },
        1: { # Note 1: Tracheal Stent for Stenosis (CPT 31631)
            1: "Indication: Symptomatic tracheal stenosis.\nProcedure: Rigid bronch, dilation, stent.\n- LMA induction. Flex scope shows complex stenosis 3cm below cords, 4cm long.\n- 60% obstruction.\n- Distal airways clear.\n- Rigid bronch (12mm) inserted.\n- 16x40mm Ultraflex stent (uncovered) deployed.\n- Stent adjusted with forceps.\n- Balloon dilation (16.5mm) performed.\n- Airway 90% patent post-procedure.\nComplications: None.",
            2: "OPERATIVE REPORT: The patient presented with complex tracheal stenosis. Following induction of general anesthesia via LMA, flexible bronchoscopy demonstrated a 4 cm long stenotic segment beginning 3 cm distal to the vocal cords, compromising the lumen by approximately 60%. The airway was converted to a 12 mm non-ventilating rigid tracheoscope. A 16x40 mm uncovered Ultraflex stent was introduced and deployed under direct visualization. Fine adjustments were made with forceps to ensure optimal seating. Subsequent balloon dilation was performed using a multi-stage balloon to a maximum diameter of 16.5 mm. Post-intervention inspection revealed restoration of approximately 90% of the luminal diameter.",
            3: "Procedure: Bronchoscopy with Tracheal Stent Placement (CPT 31631).\nDevice: 16x40mm Uncovered Ultraflex Stent.\nTechnique:\n1. Initial assessment via flexible scope/LMA confirming 4cm complex stenosis.\n2. Rigid bronchoscopy (12mm scope) established.\n3. Stent deployment covering the stenotic segment.\n4. Balloon dilation (bundled) to 16.5mm to expand stent.\nOutcome: Improvement from 60% obstruction to 90% patency.",
            4: "Procedure Note\nDx: Tracheal Stenosis\nStaff: [Attending Name]\n\n1. GA / LMA.\n2. Flex bronch: 4cm stenosis seen, starts 3cm below cords. 60% narrowed.\n3. LLL mucus suctioned.\n4. 12mm Rigid scope inserted.\n5. 16x40 Ultraflex uncovered stent placed.\n6. Stent position adjusted.\n7. Dilated w/ balloon to 16.5mm.\n8. Final result: 90% patent.\n\nPlan: PACU, Discharge home.",
            5: "We did the bronch for tracheal stenosis patient under general. Looked with the flex scope first through the LMA saw the narrowing about 4cm long starting below the cords. Switched to the rigid scope 12mm size. Put in a 16 by 40 ultraflex stent it was uncovered. Had to move it a bit to get it right then used a balloon to blow it up to 16.5. Airway looks great now about 90 percent open. No issues patient to PACU.",
            6: "The procedure was performed in the bronchoscopy suite under general anesthesia. Initial flexible bronchoscopy via LMA revealed a long segment complex tracheal stenosis extending 4cm. The distal airways were clear aside from LLL mucus. A 12mm rigid tracheoscope was passed. A 16x40 uncovered Ultraflex stent was deployed. The stent was manipulated for proper seating and dilated with a balloon to 16.5mm. Post-dilation airway caliber was 90% of normal. The rigid scope was removed.",
            7: "[Indication]\nSymptomatic complex tracheal stenosis.\n[Anesthesia]\nGeneral via LMA, converted to Rigid.\n[Description]\nStenosis visualized: 4cm length, 60% obstruction. LLL secretions cleared. 12mm rigid scope placed. 16x40mm uncovered Ultraflex stent deployed. Balloon dilation performed to 16.5mm. Airway patency improved to 90%.\n[Plan]\nDischarge home when stable. Follow up IP clinic.",
            8: "The patient underwent rigid bronchoscopy for management of tracheal stenosis. After induction, we visualized a 4 cm long stenotic segment reducing the airway by 60%. We transitioned to a 12 mm rigid tracheoscope for intervention. A 16x40 mm uncovered Ultraflex stent was carefully advanced and deployed. We adjusted the positioning with forceps and then dilated the stent using a balloon to 16.5 mm. This resulted in a marked improvement in airway caliber to 90% of normal.",
            9: "The procedure was conducted in the bronchoscopy suite. Following induction, the bronchoscope was inserted. A complex stenosis was visualized. We suctioned thick mucus from the LLL. The flexible scope was withdrawn, and a 12 mm rigid tracheoscope was inserted. A 16 x 40 uncovered Ultraflex stent was advanced and deployed. We manipulated the stent with forceps to seat it correctly. Balloon dilation was performed to 16.5 mm. The airway was approximately 90% patent post-dilation. The equipment was withdrawn."
        },
        2: { # Note 2: Rigid Bronch, Tumor Debulking (RMB) (CPT 31641)
            1: "Indication: RMS tumor obstruction, lung collapse.\nProcedure: Rigid bronch, debulking.\n- 11mm rigid scope inserted.\n- Large mass RMS supra-carinal.\n- Snare resection -> Severe Hemorrhage.\n- Rigid removed, 8.0 ETT placed.\n- Right side down, suction, epi, TXA, cryo for clots.\n- Bleeding controlled.\n- Tumor removed piecemeal w/ cryo.\n- Attempted APC debulking -> Desaturation.\n- Base APC'd for hemostasis.\n- ETT confirmed.\nPlan: ICU intubated.",
            2: "OPERATIVE SUMMARY: The patient presented with right mainstem obstruction due to suspected renal cell carcinoma. Under general anesthesia, an 11 mm rigid bronchoscope was introduced. A polypoid mass obstructing the right mainstem was identified. Electrocautery snare resection was attempted, resulting in immediate, brisk hemorrhage. This necessitated conversion to an endotracheal tube (8.0 mm) and patient positioning to protect the contralateral lung. Hemostasis was achieved using topical epinephrine, tranexamic acid, and cryotherapy extraction of clots. The transected tumor was subsequently removed piecemeal. Further debulking with APC was limited by significant oxygen desaturation. The procedure was terminated after ensuring hemostasis at the tumor base. The patient was transferred to the ICU intubated.",
            3: "Primary Procedure: Bronchoscopy with destruction of tumor/relief of stenosis (31641).\nTechnique: Rigid and flexible bronchoscopy. Modalities included electrocautery snare, cryotherapy for extraction, and Argon Plasma Coagulation (APC).\nComplication Management: Management of severe hemorrhage involved ETT placement, topical agents (Epi, TXA), and clot extraction.\nOutcome: Partial debulking achieved; procedure aborted due to physiological instability (hypoxia).",
            4: "Procedure: Rigid Bronch Debulking\nIndication: RMS Tumor\n\n1. 11mm Rigid scope placed.\n2. Large tumor seen RMS.\n3. Snared tumor -> Massive bleeding.\n4. Rigid out -> ETT 8.0 in.\n5. Pt turned right side down.\n6. Bleeding stopped w/ Epi, TXA, Cryo.\n7. Removed tumor pieces w/ Cryo.\n8. Tried APC debulking -> Pt desatted.\n9. APC'd base to stop bleeding.\n10. Stopped procedure.\n\nPlan: ICU, keep intubated.",
            5: "Patient has a tumor in the right mainstem we took him to the OR for rigid bronch. Put the 11mm rigid in and saw the mass. We tried to snare it and it bled like crazy couldn't see anything. Had to pull the rigid and intubate with an 8.0 tube. Turned him on his side used a lot of epi and txa and cryo to get the clots out. Finally got it stopped. Pulled the tumor out in pieces. Tried to burn the rest with APC but he kept desatting so we just burned the base and stopped. ICU intubated.",
            6: "The procedure was performed in the main operating room. An 11 mm ventilating rigid bronchoscope was inserted. A large mass obstructing the right mainstem was snared, resulting in brisk hemorrhage. The rigid scope was removed and an 8.0 ETT inserted. Hemostasis was achieved with topical TXA, epinephrine, and cryotherapy for clot removal. The transected tumor was removed piecemeal. Attempted APC debulking was limited by desaturation. The tumor base was treated with APC for hemostasis. The patient remained intubated and was transferred to the ICU.",
            7: "[Indication]\nTumor obstruction of right mainstem, complete lung collapse.\n[Anesthesia]\nGeneral, converted from Rigid to ETT.\n[Description]\n11mm rigid scope used. Snare resection of RMS mass precipitated severe hemorrhage. Airway converted to 8.0 ETT. Bleeding controlled with pharmacologic agents and cryo. Tumor removed piecemeal. Further APC debulking limited by hypoxia. Base coagulated.\n[Plan]\nICU admission. Mechanical ventilation. Assess for further options.",
            8: "We engaged in a rigid bronchoscopy to debulk a tumor obstructing the right mainstem. Upon snaring the lesion, we encountered severe hemorrhage that obscured visualization. We immediately converted to an endotracheal intubation to secure the airway and positioned the patient to protect the healthy lung. Using a combination of epinephrine, TXA, and cryotherapy, we managed to halt the bleeding and remove the resected tumor tissues. Although we hoped to perform further APC debulking, the patient's respiratory status deteriorated, forcing us to coagulate the base and terminate the procedure safely.",
            9: "The procedure was executed in the main operating room. An 11 mm rigid bronchoscope was introduced. A large mass was visualized in the right mainstem. We secured the lesion with a snare; however, it hemorrhaged briskly. We exchanged the rigid scope for an ETT. Vision was poor, but we utilized topical agents and a cryotherapy probe to extract blood clots. Once hemostasis was achieved, the transected tumor was extracted piecemeal. We attempted to ablate residual tumor with APC, but the patient desaturated. We coagulated the base and aborted further attempts. The patient was transferred to the ICU."
        },
        3: { # Note 3: Tracheal Tumor Debulking (CPT 31641)
            1: "Indication: Tracheal obstruction (tumor).\nProcedure: Rigid bronch, Snare, APC.\n- 3 polypoid lesions proximal trachea, 90% obstruction.\n- Multiple distal lesions.\n- 10mm Rigid scope placed.\n- Snare resection of 3 large + 10 small lesions.\n- APC used to paint/shave base.\n- Airway 90% open post-op.\n- No stent placed (patient refusal/chemo).\nPlan: Ward, Pathology, Oncology consult.",
            2: "OPERATIVE REPORT: The patient presented with high-grade endotracheal tumor obstruction. Under general anesthesia, inspection revealed three large polypoid lesions 2.5 cm distal to the vocal cords causing 90% expiratory obstruction, with extensive satellite lesions distally. A 10mm rigid tracheoscope was inserted. The T190 flexible scope was utilized to perform electrocautery snare resection of the dominant lesions and approximately ten smaller lesions. The tumor bases and residual disease were treated with Argon Plasma Coagulation (APC) to achieve luminal recanalization. Final inspection demonstrated a 90% patent airway. Stent placement was deferred based on prior patient preference.",
            3: "Procedure: Bronchoscopy with destruction of tumor (31641).\nTechnique: Rigid bronchoscopy (10mm) and flexible bronchoscopy.\nModalities: Electrocautery snare resection (excision) and APC (destruction) performed in the same anatomic location (Trachea).\nFindings: 90% obstruction reduced to <10% obstruction.\nNote: Stenting (31631) was considered but not performed due to patient preference.",
            4: "Procedure: Tracheal Debulking\nIndication: Tracheal Tumor\n\n1. Flex bronch via LMA: 3 large polyps, 90% blocked.\n2. Switched to 10mm Rigid scope.\n3. Snared 3 large + 10 small lesions.\n4. Removed tissue for path.\n5. APC used to clean up base.\n6. Result: 90% open.\n7. No complications.\n\nPlan: Admit to ward.",
            5: "Patient has a tracheal tumor blocking 90 percent of the airway. We put him to sleep and looked with the flex scope first. Saw the polyps. Put in the 10mm rigid scope. Used the snare to cut off the big ones and a bunch of small ones too. Suctioned them out. Used the APC to burn the rest of it down. Got it open to about 90 percent. We wanted to stent it but he said no because of the cough. Sent him to the floor.",
            6: "The procedure was performed in the main operating room under general anesthesia. Initial inspection revealed 3 polypoid lesions causing 90% obstruction in the proximal trachea. A 10mm non-ventilating rigid tracheoscope was inserted. Using an electrocautery snare, the proximal lesions and approximately 10 distal lesions were resected. APC was used to paint and shave the remaining tumor burden. The airway was restored to 90% patency. No stent was placed. The patient was transferred to the ward.",
            7: "[Indication]\nTracheal obstruction, endotracheal tumor.\n[Anesthesia]\nGeneral, LMA converted to Rigid.\n[Description]\n90% obstruction by polypoid lesions visualized. 10mm rigid scope placed. Snare resection of 13+ lesions performed. APC used for residual tumor destruction. 90% luminal patency achieved.\n[Plan]\nWard admission. Oncology consult for PDT/Brachytherapy.",
            8: "We performed a bronchoscopic debulking for a patient with severe tracheal obstruction. Upon entering with the bronchoscope, we found a cluster of polyps blocking nearly the entire airway. We switched to a rigid tracheoscope to facilitate resection. Using a snare, we successfully removed the three main polyps and about ten smaller ones. We then applied APC to the tumor base to ensure hemostasis and further reduce the tumor burden. We achieved a 90% airway opening. Per the patient's request, no stent was placed.",
            9: "The procedure was performed in the main operating room. After administration of sedatives, the bronchoscope was inserted. We advanced into the subglottic space. There were 3 polypoid lesions blocking the airway. A 10mm rigid tracheoscope was inserted. The flexible bronchoscope was introduced, and the electrocautery snare was used to transect the lesions. We removed about 10 other lesions in the same fashion. We used APC to ablate the remaining tumor area. At the end, the trachea was 90% open. The rigid bronchoscope was removed."
        }
    }
    return variations

def get_base_data_mocks():
    # Define base names and ages for the 4 distinct patients found in the source file
    return [
        {
            "idx": 0, 
            "orig_name": "Logan Pierce", # From Note 0 text (fistula)
            "orig_age": 67, 
            "names": ["John Vance", "Arthur Higgins", "Robert Kinsley", "William O'Connor", "James P. Miller", "Edward Stone", "Richard Davis", "Thomas Clark", "Gary Wright"]
        },
        {
            "idx": 1, 
            "orig_name": "Unknown", # Note 1 had unknown name
            "orig_age": 55, # Assigning a base age for variation
            "names": ["Sarah Jenkins", "Linda Carter", "Nancy Hughes", "Karen Smith", "Barbara Lopez", "Mary Ann Davidson", "Susan White", "Margaret Lewis", "Betty King"]
        },
        {
            "idx": 2, 
            "orig_name": "Unknown", # Note 2 had unknown name
            "orig_age": 65, # Assigning a base age
            "names": ["Michael Foster", "Robert G. Turner", "David Myers", "Joseph Anderson", "Frank Mitchell", "Paul Reynolds", "George Baker", "Kenneth Roberts", "Steven Phillips"]
        },
        {
            "idx": 3, 
            "orig_name": "Unknown", # Note 3 had unknown name
            "orig_age": 60, # Assigning a base age
            "names": ["Marie Hall", "Patricia Campbell", "Elizabeth Allen", "Jennifer Young", "Linda Hernandez", "Barbara King", "Dorothy Wright", "Helen Scott", "Carol Green"]
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
                print(f"Warning: Variation not found for Note {idx}, Style {style_num}")
                continue
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update Patient MRN
                if "patient_mrn" in note_entry["registry_entry"]:
                    # Create a mock MRN base if 'Unknown' or use existing
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    if base_mrn == "Unknown" or base_mrn == "UNKNOWN":
                        base_mrn = f"IP2025{idx:03d}"
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
                
                # Update Procedure Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update Patient Demographics/Age if present
                if "patient_demographics" in note_entry["registry_entry"] and isinstance(note_entry["registry_entry"]["patient_demographics"], dict):
                     note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                     note_entry["registry_entry"]["patient_demographics"]["gender"] = "Male" if idx in [0, 2, 3] else "Female" # Attempt to infer gender from original
                elif "patient_age" in note_entry["registry_entry"]: # Handle flat structure if present
                     note_entry["registry_entry"]["patient_age"] = new_age

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
    output_filename = output_dir / "synthetic_bronch_notes_part_014.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()