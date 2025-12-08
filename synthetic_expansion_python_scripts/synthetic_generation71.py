import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_071.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations for Part 071.
    # Structure: Note_Index (0-5) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Daniel Rivera (Right Whole Lung Lavage)
            1: "Procedure: Right whole lung lavage.\nIndication: PAP, right-predominant crazy-paving.\nAction: GA, 37Fr Left DLT placed. Lung isolation confirmed. Right lung lavaged with 18L warm saline. 15.2L recovered. Effluent cleared.\nComplications: Transient desaturation (85%), resolved with recruitment.\nDisposition: Extubated. ICU.",
            2: "OPERATIVE REPORT: The patient, presenting with symptomatic pulmonary alveolar proteinosis, underwent therapeutic whole lung lavage of the right lung. Following the induction of general anesthesia and the precise placement of a left-sided double-lumen endotracheal tube, single-lung ventilation was established. The right lung was subjected to sequential large-volume lavage utilizing 18.0 liters of warmed isotonic saline. The initially opaque, proteinaceous effluent demonstrated progressive clearing with each cycle. Despite transient intraoperative desaturations necessitating recruitment maneuvers, the procedure was completed successfully with a recovery volume of 15.2 liters. The patient was extubated in the operating theater.",
            3: "Service: Therapeutic Whole Lung Lavage (CPT 32997).\nSite: Right Lung.\nTechnique:\n1. Airway Control: 37 Fr Double-lumen tube placed for lung isolation.\n2. Lavage: Sequential instillation of 18.0L saline into the right lung with chest percussion to mobilize lipoproteinaceous material.\n3. Drainage: Gravity drainage of 15.2L effluent.\nMedical Necessity: Hypoxemic respiratory failure due to PAP.\nStatus: Completed.",
            4: "Resident Note\nPatient: Daniel Rivera\nProcedure: Right WLL\nStaff: Dr. Thompson\nSteps:\n1. L DLT placed, position checked with scope.\n2. Right lung isolated.\n3. Instilled 1L saline aliquots x 18 cycles (Total 18L).\n4. Percussion performed during dwell time.\n5. Fluid cleared nicely.\n6. Extubated.\nIssues: Sats dropped to 80s a few times, fixed with recruitment.",
            5: "daniel rivera for right lung lavage pap symptoms anesthesia general left sided dlt used 37 french lavage right side with 18 liters saline drained about 15 liters looked milky then clear desats to 85 percent handled fine extubated to icu thanks",
            6: "Right whole lung lavage was performed on a 42-year-old male with pulmonary alveolar proteinosis. General anesthesia with a 37 Fr left-sided double-lumen tube was utilized. Single-lung ventilation of the left lung allowed for lavage of the right lung using 18.0 L of warmed normal saline in 1.0 L aliquots. Effluent gradually cleared from opaque to translucent. 15.2 L of fluid were recovered. Transient desaturation occurred but responded to recruitment. The patient was extubated and transferred to the ICU.",
            7: "[Indication]\nSymptomatic PAP with right-predominant disease.\n[Anesthesia]\nGeneral, 37Fr Left DLT.\n[Description]\nRight lung lavage. 18L instilled, 15.2L recovered. Chest percussion applied. Effluent cleared. Transient hypoxemia managed with recruitment.\n[Plan]\nICU admission, monitor oxygenation.",
            8: "Mr. Rivera was brought to the operating room for a therapeutic lavage of his right lung due to PAP. We placed a double-lumen tube to isolate the lungs and verified it with the scope. We then washed the right lung with 18 liters of saline, draining it by gravity between fills. The fluid started out very milky but was clear by the end. He had some dips in his oxygen levels, but we managed those with recruitment maneuvers. We pulled the tube and sent him to the ICU.",
            9: "Operation: Total lung irrigation (right). Reason: Alveolar proteinosis. Method: Under GA, lung isolation was achieved. 18.0 L of saline were infused and extracted from the right lung. Discharge fluid transitioned from opaque to clear. 15.2 L retrieved. The patient was weaned from ventilation and the airway device removed."
        },
        1: { # Sarah McIntyre (Left Whole Lung Lavage)
            1: "Procedure: Left Whole Lung Lavage (Staged).\nIndication: PAP.\nAction: 35Fr Left DLT. Right lung ventilated. Left lung lavaged with 16L warm saline. 13.5L returned. Clear effluent at end.\nComplications: None.\nDisposition: Extubated to Step-down.",
            2: "NARRATIVE: This 51-year-old female underwent a staged contralateral whole lung lavage for pulmonary alveolar proteinosis. Following the successful right lung lavage previously, the left lung was targeted today. General anesthesia was induced, and a 35 Fr left-sided double-lumen tube was positioned to permit right lung ventilation. The left lung was lavaged with 16.0 liters of saline in aliquots. The effluent cleared appropriately. The patient remained hemodynamically stable with excellent oxygenation throughout. Extubation occurred in the operating room.",
            3: "Code: 32997 (Unilateral Whole Lung Lavage).\nTarget: Left Lung (Contralateral to previous procedure).\nDevice: 35 Fr Left DLT.\nDetails: 16.0L saline instilled; 13.5L recovered. \nOutcome: Significant clearance of proteinaceous material documented visually. \nComplexity: Standard, no complications.",
            4: "Procedure: Left WLL\nPt: Sarah McIntyre\nAttending: Dr. Owens\nSteps:\n1. Intubated with 35Fr Left DLT.\n2. Confirmed isolation of left lung.\n3. Lavaged left lung with 16L saline.\n4. Chest PT performed.\n5. Fluid became clear.\n6. Extubated stable.\nPlan: Step-down unit.",
            5: "patient sarah mcintyre here for the left side lavage had the right one done last month general anesthesia left dlt 35 french used washed left lung with 16 liters saline return 13.5 liters fluid clear at end no desats extubated fine to step down",
            6: "Staged whole lung lavage of the left lung was performed for pulmonary alveolar proteinosis. The patient was intubated with a 35 Fr left-sided double-lumen tube. With the right lung ventilated, the left lung was lavaged using 16.0 L of warmed saline. 13.5 L were recovered. The effluent cleared from milky to translucent. The patient tolerated the procedure well without desaturation or hemodynamic instability and was extubated post-procedure.",
            7: "[Indication]\nStaged left WLL for PAP.\n[Anesthesia]\nGeneral, 35Fr Left DLT.\n[Description]\nLeft lung lavage. 16L instilled. 13.5L recovered. Effluent cleared. No hypoxia.\n[Plan]\nStep-down unit, observe.",
            8: "Ms. McIntyre came in for the second part of her treatment, the lavage of the left lung. We used a double-lumen tube to breathe for her right lung while we washed the left. We used 16 liters of saline in total. The fluid cleared up nicely as we went. She didn't have any oxygen issues this time and we were able to wake her up and take the tube out right in the OR.",
            9: "Operation: Unilateral lung washing (left). Indication: PAP (staged). Technique: 16.0 L saline infused into the left lung. 13.5 L drained. Output fluid became transparent. No adverse events. Patient extubated."
        },
        2: { # Marcus Hall (Aborted Right WLL)
            1: "Procedure: Right WLL (Aborted).\nIndication: PAP, hypoxemia.\nAction: DLT placed. Lavage started. 10L in/7.5L out. Severe desaturation (78%) refractory to recruitment.\nResult: Procedure aborted. Fluid suctioned.\nDisposition: Intubated to ICU.",
            2: "OPERATIVE NOTE: The patient presented for therapeutic right whole lung lavage. Following induction and DLT placement, lavage was initiated. However, after the instillation of 10.0 liters, the patient developed profound, refractory hypoxemia (SpO2 78%) unresponsive to standard recruitment maneuvers and increased FiO2. The decision was made to terminate the procedure prematurely to ensure patient safety. Residual fluid was aspirated, and the patient was transferred to the ICU remaining intubated for stabilization.",
            3: "CPT: 32997-53 (Discontinued Procedure).\nRationale: Right whole lung lavage initiated. 10L saline instilled. Procedure terminated due to threat to patient well-being (severe refractory hypoxemia).\nDocumentation: Supports significant physician work prior to termination.",
            4: "Procedure: Aborted Right WLL\nPt: Marcus Hall\nSteps:\n1. DLT placed.\n2. Started lavage right lung.\n3. Got 10L in.\n4. Sats dropped to 78% and stayed down.\n5. Stopped lavage.\n6. Suctioned out fluid.\nPlan: ICU, keep intubated.",
            5: "marcus hall 58 male for right lung wash started fine got 10 liters in then sats crashed to 78 couldnt get them up so we stopped pulled out what we could left him on the vent going to icu hopefully try again later",
            6: "Therapeutic whole lung lavage of the right lung was attempted but aborted due to instability. After induction and DLT placement, lavage commenced. 10.0 L of saline were instilled with 7.5 L recovered. The patient developed severe hypoxemia (78%) refractory to interventions. The procedure was halted. Residual fluid was suctioned. The patient remained intubated and was transferred to the ICU.",
            7: "[Indication]\nPAP, severe hypoxemia.\n[Anesthesia]\nGeneral, DLT.\n[Description]\nRight WLL attempted. 10L instilled. Aborted due to refractory desaturation (78%). Fluid suctioned.\n[Plan]\nICU, mechanical ventilation.",
            8: "We started the lavage on Mr. Hall's right lung, but he didn't tolerate it well. After about 10 liters, his oxygen saturation dropped to 78% and wouldn't improve even with 100% oxygen and recruitment. We had to stop the procedure for his safety. We suctioned out the remaining fluid and sent him to the ICU still on the ventilator.",
            9: "Operation: Incomplete lung irrigation (right). Issue: Intractable hypoxemia. Action: 10L infused. Operation halted. Fluid extracted. Patient remains on ventilator support."
        },
        3: { # Linda Jacobs (Thoracoscopy Bx)
            1: "Procedure: Left Medical Thoracoscopy.\nFindings: 1400mL exudative fluid. Diffuse parietal nodules.\nAction: Fluid drained. Multiple biopsies taken. 24Fr chest tube placed.\nComplications: None.\nPlan: Admit. Await path.",
            2: "PROCEDURE: Left medical thoracoscopy. Under general anesthesia and single-lung ventilation, the left pleural space was accessed. 1400 mL of straw-colored exudate were evacuated. Visualization revealed diffuse nodularity of the parietal pleura. Multiple biopsies were obtained using forceps. A 24 Fr chest tube was inserted via the access site. The patient tolerated the procedure well.",
            3: "CPT: 32609 (Thoracoscopy with biopsy of pleura).\njustification: Diagnostic evaluation of recurrent effusion. Thoracoscope introduced. Parietal pleural biopsies harvested. 1400mL fluid removed (incidental to procedure). Chest tube placed (bundled).",
            4: "Procedure: Left Thoracoscopy\nPt: Linda Jacobs\nSteps:\n1. 7.5 ETT, single lung vent.\n2. Trocar in 6th ICS.\n3. Drained 1.4L fluid.\n4. Saw nodules on pleura -> Biopsied.\n5. Chest tube placed.\nPlan: Floor, watch chest tube.",
            5: "linda jacobs left pleural effusion thoracoscopy drained 1400 cc fluid looked straw colored lots of little nodules on the wall took biopsies put in a 24 french chest tube sent to floor no issues",
            6: "Left medical thoracoscopy was performed for recurrent exudative pleural effusion. 1400 mL of fluid were drained. Inspection showed diffuse fine nodularity of the parietal pleura. Multiple biopsies were obtained. Hemostasis was secured. A 24 Fr chest tube was placed. The patient was admitted for monitoring.",
            7: "[Indication]\nRecurrent left exudative effusion.\n[Anesthesia]\nGA, Single-lung ventilation.\n[Description]\nThoracoscopy. 1400mL drained. Parietal nodules biopsied. 24Fr Chest tube placed.\n[Plan]\nAdmit, await pathology.",
            8: "Mrs. Jacobs underwent a medical thoracoscopy on the left side to investigate her fluid buildup. We drained 1400 mL of fluid and saw a lot of small nodules on the chest wall. We took biopsies of these nodules for the lab. We left a chest tube in place to keep the fluid off while the lung heals.",
            9: "Operation: Pleuroscopy with sampling. Site: Left hemithorax. Findings: 1.4L effusion, pleural nodularity. Action: Fluid evacuated. Tissue samples collected. Drainage catheter inserted."
        },
        4: { # Robert Evans (Thoracoscopy Talc)
            1: "Procedure: Right Medical Thoracoscopy + Talc.\nFindings: 1800mL fluid. Trapped lung. Tumor implants.\nAction: Biopsies taken. 4g Talc poudrage insufflated. Chest tube placed.\nDisposition: Admit.",
            2: "OPERATIVE REPORT: Right medical thoracoscopy was indicated for recurrent malignant pleural effusion. Upon entry, 1800 mL of serosanguinous fluid were drained. The right lower lobe appeared partially trapped with visible tumor implants on the parietal pleura. Biopsies were taken. To achieve pleurodesis, 4 grams of sterile talc were insufflated (poudrage) throughout the pleural cavity. A chest tube was placed to facilitate lung re-expansion and drainage.",
            3: "CPT: 32650 (Thoracoscopy with pleurodesis).\nIncludes: Drainage of effusion, biopsy of pleura (bundled), insufflation of talc agent.\nDiagnosis: Malignant pleural effusion with trapped lung.\nDevice: 24 Fr Chest tube.",
            4: "Procedure: Right Thoracoscopy w/ Talc\nPt: Robert Evans\nSteps:\n1. Port placed 7th ICS.\n2. Drained 1.8L.\n3. Biopsies taken.\n4. Lung looked trapped.\n5. Talc poudrage (4g) performed.\n6. Chest tube in.\nPlan: Admit.",
            5: "robert evans right malignant effusion thoracoscopy drained 1800 cc lung trapped tumor on pleura biopsies taken did talc poudrage 4 grams chest tube placed admit to floor",
            6: "Right medical thoracoscopy with talc pleurodesis was performed. 1800 mL of serosanguinous fluid were drained. Inspection revealed tumor implants and a trapped right lower lobe. Biopsies were obtained. 4 grams of sterile talc were insufflated for pleurodesis. A 24 Fr chest tube was placed. The patient was admitted.",
            7: "[Indication]\nRecurrent malignant effusion, trapped lung.\n[Anesthesia]\nGA.\n[Description]\nRight thoracoscopy. 1800mL drained. Biopsies taken. Talc poudrage (4g) performed. Chest tube placed.\n[Plan]\nAdmit, suction.",
            8: "We performed a thoracoscopy on Mr. Evans' right side. We drained about 1.8 liters of fluid. The lung looked trapped by the tumor. We took some biopsies and then sprayed talc powder into the chest cavity to try and glue the lung to the wall. A chest tube was left in place.",
            9: "Operation: Pleuroscopy with chemical sclerosis. Action: 1800mL evacuated. Tissue sampled. Talc insufflated for symphysis. Drain inserted."
        },
        5: { # Maria Alvarez (Thoracoscopy Talc + IPC)
            1: "Procedure: Right Thoracoscopy + Talc + IPC.\nFindings: 2000mL drained. Trapped lung. Diffuse implants.\nAction: Biopsies. Talc poudrage. Tunneled pleural catheter placed for palliation.\nDisposition: Discharge home.",
            2: "NARRATIVE: The patient underwent right medical thoracoscopy for management of a malignant effusion. 2000 mL of fluid were evacuated. Visualization confirmed diffuse tumor implants and significant lung entrapment. Talc poudrage was performed. Due to the trapped lung physiology, a decision was made to place an indwelling tunneled pleural catheter to ensure effective long-term palliation. The catheter was tunneled and secured without complication.",
            3: "CPT Codes:\n- 32650: Thoracoscopy with pleurodesis (Talc).\n- 32550: Insertion of indwelling tunneled pleural catheter.\nRationale: Distinct services; IPC placed due to trapped lung to provide auxiliary drainage capacity alongside chemical pleurodesis attempt.",
            4: "Procedure: Thoracoscopy + Talc + IPC\nPt: Maria Alvarez\nSteps:\n1. 2L fluid drained via scope.\n2. Biopsies taken.\n3. Talc poudrage performed.\n4. Lung trapped, so IPC placed.\n5. IPC tunneled and secured.\nPlan: Home with drainage supplies.",
            5: "maria alvarez right effusion thoracoscopy drained 2 liters lung trapped so we did talc and also put in a pleurx catheter for home drainage biopsies sent went home same day",
            6: "Right medical thoracoscopy with talc pleurodesis and tunneled pleural catheter placement was performed. 2000 mL were drained. Trapped lung and tumor implants were noted. Biopsies were taken. Talc poudrage was executed. A tunneled pleural catheter was inserted to manage the trapped lung. The patient was discharged to home.",
            7: "[Indication]\nMalignant effusion, trapped lung.\n[Anesthesia]\nGA.\n[Description]\nThoracoscopy. 2L drained. Talc poudrage. Tunneled pleural catheter (IPC) placed.\n[Plan]\nDischarge, home drainage.",
            8: "We did a thoracoscopy on Mrs. Alvarez. We drained 2 liters of fluid and found her lung was trapped by the cancer. We sprayed talc to help, but because the lung was trapped, we also put in a permanent tunneled catheter so she can drain fluid at home. She went home the same day.",
            9: "Operation: Pleuroscopy, sclerosis, and indwelling catheter placement. Action: 2000mL evacuated. Talc applied. Tunneled catheter inserted for chronic drainage. Patient released."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages
    return [
        {"idx": 0, "orig_name": "Daniel Rivera", "orig_age": 42, "names": ["David Ruiz", "Dan Rivers", "Diego Ramirez", "Darren Ross", "Dominic Reed", "Daniel Reyes", "Dustin Rhodes", "Derek Richardson", "Dante Romano"]},
        {"idx": 1, "orig_name": "Sarah McIntyre", "orig_age": 51, "names": ["Susan Mac", "Sally Miller", "Sharon Moore", "Sandra Mitchell", "Stacy Morgan", "Sheila Murphy", "Sylvia Matthews", "Stephanie Meyer", "Simone Martin"]},
        {"idx": 2, "orig_name": "Marcus Hall", "orig_age": 58, "names": ["Michael Harris", "Martin Hughes", "Matthew Hill", "Mark Henderson", "Miles Hayes", "Mitchell Harvey", "Mason Hunt", "Malcolm Hamilton", "Max Harrison"]},
        {"idx": 3, "orig_name": "Linda Jacobs", "orig_age": 63, "names": ["Laura Johnson", "Lisa Jones", "Louise Jackson", "Loretta James", "Lucia Jenkins", "Lydia Jordan", "Lillian Jeffrey", "Leslie Jenson", "Lana Jarvis"]},
        {"idx": 4, "orig_name": "Robert Evans", "orig_age": 69, "names": ["Richard Edwards", "Raymond Ellis", "Roger Elliott", "Ralph Erickson", "Randy Evans", "Ronald East", "Ryan English", "Russell Emery", "Roy Eaton"]},
        {"idx": 5, "orig_name": "Maria Alvarez", "orig_age": 71, "names": ["Martha Anderson", "Mary Adams", "Margaret Allen", "Michelle Armstrong", "Monica Austin", "Melissa Andrews", "Maureen Arnold", "Marilyn Atkins", "Melanie Arthur"]},
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
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
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
    output_filename = output_dir / "synthetic_wll_pleural_notes_part_071.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()