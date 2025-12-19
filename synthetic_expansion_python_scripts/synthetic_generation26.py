import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_026.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Elen Rogers (Malignant Effusion, Tube)
            1: "PROCEDURE: US Chest + Chest Tube Placement.\n* US: R hemithorax, moderate anechoic effusion, no loculations.\n* Local: Lidocaine 1%.\n* Access: R mid-scapular line, 8th ICS.\n* Device: 12Fr pigtail catheter via Seldinger.\n* Output: 450ml bloody fluid.\n* Complications: None.\n* Disp: Tube to pneumostat. CXR ordered.",
            2: "OPERATIVE NARRATIVE: The patient, presenting with a known malignant pleural process, underwent ultrasound-guided thoracostomy. Thoracic ultrasonography of the right hemithorax delineated a moderate, free-flowing, anechoic effusion with nodular pleural thickening consistent with metastatic disease. Under local anesthesia and aseptic conditions, a 12 French pigtail catheter was introduced into the right pleural space at the 8th intercostal space utilizing the Seldinger technique. A volume of 450 mL of hemorrhagic fluid was evacuated. The catheter was secured and connected to a Pneumostat valve. The patient tolerated the intervention without hemodynamic compromise.",
            3: "Service Performed: Percutaneous pleural drainage with indwelling catheter (32557). \nGuidance: Real-time ultrasonic guidance (76604) was employed to characterize the effusion (anechoic, non-loculated) and determine the optimal entry site (Right 8th ICS). \nTechnique: A 12 French pigtail catheter was placed via needle entry, guidewire advancement, and dilation. \nOutcome: Catheter confirmed in pleural space by return of 450ml bloody fluid. Catheter secured. Procedures substantiate reporting of code 32557.",
            4: "Procedure Note\nResident: Dr. Clark\nAttending: Dr. Smith\nIndication: Malignant Pleural Effusion\nConsent: Obtained.\nTime Out: Performed.\nProcedure Steps:\n1. Bedside US performed identifying R moderate effusion.\n2. Sterile prep and drape.\n3. 1% Lidocaine for local anesthesia.\n4. 12Fr pigtail catheter inserted using Seldinger technique at R mid-scapular line.\n5. 450 cc bloody fluid returned.\n6. Tube sutured and dressing applied.\nComplications: None.\nPlan: CXR to confirm placement.",
            5: "date 12/16/25 procedure chest tube placement right side pt has malignant effusion ultrasound showed moderate fluid no septations used lidocaine for numb 12 french pigtail put in mid scapular line got back 450 of bloody fluid no complications patient did fine chest tube secured hook to pneumostat plan cxr check placement signed dr smith",
            6: "On 12/16/2025 a bedside chest tube placement was performed for a right malignant pleural effusion. Ultrasound of the right chest demonstrated a moderate anechoic effusion with nodular pleura. The site was prepped. 1% lidocaine was used. A 12 Fr pigtail catheter was inserted into the right 8th intercostal space using the Seldinger technique. 450 ml of bloody fluid was drained. The catheter was sutured in place and attached to a Pneumostat. There were no complications. Post-procedure plan includes a chest xray.",
            7: "[Indication]\nSymptomatic malignant pleural effusion, right side.\n[Anesthesia]\nLocal infiltration with 1% Lidocaine (5 mL).\n[Description]\nUltrasound survey of the right chest revealed a moderate anechoic effusion. Using the Seldinger technique, a 12Fr pigtail catheter was introduced at the 8th intercostal space, mid-scapular line. 450 mL of bloody fluid was drained. The device was secured.\n[Plan]\nObtain CXR. Monitor output.",
            8: "The patient was positioned sitting up for the procedure. We began by performing a bedside ultrasound of the right chest, which visualized a moderate-sized effusion that was anechoic and free of loculations. We noted some nodular pleural thickening. After identifying a safe pocket, we prepped the skin and anesthetized the area with lidocaine. We then used a needle and guidewire to place a 12 French pigtail catheter into the pleural space. Once the dilator was removed and the catheter advanced, we drained approximately 450 milliliters of bloody fluid. The tube was secured with suture and a dressing was applied.",
            9: "Operation: Thoracic drainage catheter deployment.\nDiagnostic Imaging: Sonographic evaluation of the thorax identified a fluid collection.\nTechnique: Following administration of local anesthetic, a 12Fr drainage cannula was advanced into the pleural cavity utilizing a guidewire approach. Approximately 450ml of sanguineous fluid was evacuated. The apparatus was affixed to the chest wall. The procedure concluded without adverse events."
        },
        1: { # David Obasi (Empyema, Tube)
            1: "PROCEDURE: US-Guided Thoracostomy (L).\n* Indication: Empyema.\n* US Findings: L moderate loculated effusion, hyperechoic, thickened pleura.\n* Site: L mid-axillary, 4-5 ICS.\n* Tube: 24Fr pigtail.\n* Output: 550ml turbid/purulent fluid.\n* Plan: Suction -20cmH2O. Culture fluid.",
            2: "OPERATIVE REPORT: The patient presented with a complex parapneumonic effusion suggestive of empyema. Thoracic ultrasound of the left hemithorax revealed a moderate, hyperechoic effusion with thickened loculations and pleural thickening. Given the viscosity of the fluid, a larger bore catheter was selected. Under local anesthesia, a 24 French catheter was introduced into the left pleural space via the mid-axillary line at the 4th-5th intercostal space. The procedure yielded 550 mL of turbid, purulent fluid. The catheter was connected to -20 cmH2O suction to facilitate drainage of the infected space.",
            3: "CPT 32557 justified by percutaneous insertion of indwelling pleural catheter with imaging guidance. \n- Guidance: Ultrasound (76604) confirmed loculated complex fluid on Left. \n- Instrumentation: 24Fr catheter used due to purulence.\n- Drainage: 550ml turbid fluid removed.\n- Device left in place: Yes, connected to Pleurovac suction.\n- Medical Necessity: Complex parapneumonic effusion/empyema requiring continuous drainage.",
            4: "Procedure Note\nPatient: [Name]\nMRN: [MRN]\nProcedure: Left Chest Tube Placement\nIndications: Complex effusion/Empyema\n\nSteps:\n1. Ultrasound localizing L loculated effusion.\n2. Local anesthesia with 15ml Lidocaine.\n3. 24Fr catheter placed via Seldinger technique.\n4. Return of 550ml purulent fluid.\n5. Tube secured and placed to suction.\n\nSpecimens sent: pH, cell count, culture, cytology.\nComplications: None.",
            5: "david obasi 33 yo male with empyema left side did ultrasound saw thick loculated fluid hyperechoic put in 24 french chest tube used 15 of lido draining 550 cc of pus essentially turbid fluid hooked it up to suction negative 20 no complications tolerated well send fluid for culture",
            6: "A left-sided chest tube insertion was performed on 12/16/2025. Ultrasound guidance demonstrated a moderate loculated hyperechoic effusion on the left. The left mid-axillary line at the 4-5th intercostal space was selected. 15 mL of lidocaine was infiltrated. A 24 Fr catheter was placed. 550 mL of turbid/purulent fluid was drained. The tube was sutured and placed on -20cmH2O suction. Samples were sent for analysis.",
            7: "[Indication]\nComplex parapneumonic effusion / Empyema, Left side.\n[Anesthesia]\n15 mL Lidocaine 1%.\n[Description]\nUltrasound confirmed loculated, hyperechoic fluid. A 24Fr pigtail catheter was inserted into the L pleural space. 550 mL of purulent fluid was evacuated.\n[Plan]\nConnect to Pleurovac suction (-20cmH2O). Antibiotics as per ID.",
            8: "The patient is a 33-year-old male with a complex effusion. We performed a bedside ultrasound which showed a loculated collection on the left side with thick septations. We decided to place a 24 French chest tube to ensure adequate drainage of the thick fluid. After anesthetizing the site with lidocaine, the tube was placed without difficulty. We immediately drained about 550ml of turbid, purulent fluid. The tube was secured and connected to wall suction.",
            9: "Intervention: Percutaneous pleural drainage.\nLocalization: Sonography depicted a complex fluid pocket.\nDetails: A 24Fr drainage tube was sited in the left hemithorax. A total of 550ml of purulent exudate was aspirated. The conduit was anchored and linked to a negative pressure vacuum system. The procedure was completed successfully."
        },
        2: { # Linda Kim (Large Effusion, Tube)
            1: "PROCEDURE: R Chest Tube Placement.\n* Dx: Large symptomatic effusion.\n* US: R large anechoic fluid.\n* Tube: 14Fr pigtail.\n* Site: R mid-axillary, 6-7 ICS.\n* Output: 1850ml serous fluid.\n* Status: Tube clamped after initial drain. No comps.",
            2: "PROCEDURE NOTE: Ms. [Name], an 81-year-old female with congestive heart failure, presented with a large right-sided pleural effusion causing respiratory compromise. Thoracic ultrasound demonstrated a large, anechoic, free-flowing effusion suitable for drainage. A 14 French pigtail catheter was inserted into the right pleural space at the 6th-7th intercostal space, mid-axillary line. 1850 mL of serous fluid was evacuated, providing immediate symptomatic relief. The catheter was secured for continued management.",
            3: "Coding Data:\nProcedure: 32557 (Pleural drainage w/ imaging).\nUS Findings: Large anechoic effusion Right (supports 76604).\nCatheter: 14 French indwelling catheter.\nVolume: 1850ml removed.\nNotes: Imaging guidance essential for safe placement in elderly patient with large effusion.",
            4: "Procedure: Ultrasound Guided Thoracostomy\nAttending: Dr. Smith\nResident: Dr. Clark\nPatient: [Name], 81F\n\n1. Consent obtained.\n2. R chest ultrasound: Large simple effusion.\n3. Prep/Drape/Local Anesthesia.\n4. 14Fr pigtail inserted R 6-7 ICS.\n5. 1850ml serous fluid drained.\n6. Secured.\n\nPlan: Monitor output, fluid analysis.",
            5: "patient linda kim 81 female has large effusion right side chf likely ultrasound confirmed big fluid pocket anechoic did the chest tube 14 french right mid axillary drained a lot 1850 ml serous looks like transudate patient breathing better now tube secured no issues",
            6: "On 12/16/2025 a 14 Fr pigtail catheter was inserted into the right pleural space for a large pleural effusion. Ultrasound guidance was used to identify the fluid pocket. The entry site was the 6-7th intercostal space at the mid-axillary line. 1850 ml of serous fluid was removed. The patient tolerated the procedure well. There were no complications.",
            7: "[Indication]\nLarge pleural effusion / Decompensated CHF.\n[Anesthesia]\n10 mL Lidocaine 1%.\n[Description]\nUltrasound visualized a large anechoic effusion on the Right. A 14Fr catheter was placed percutaneously. 1850 mL of serous fluid was drained.\n[Plan]\nFluid analysis. Monitor electrolytes post-drainage.",
            8: "Ms. Kim was positioned supine for the procedure. We used ultrasound to locate a large fluid collection on her right side, which appeared clear and anechoic. After prepping the area, we inserted a 14 French pigtail catheter. The procedure went smoothly, and we were able to drain 1850ml of straw-colored fluid. The patient reported feeling immediate relief. We secured the tube and ordered a follow-up chest x-ray.",
            9: "Technique: Sonographically guided thoracostomy.\nTarget: Massive right-sided hydrothorax.\nExecution: A 14Fr cannula was introduced into the pleural cavity. 1850ml of serous transudate was evacuated. The catheter was affixed to the skin. No adverse sequelae noted."
        },
        3: { # Mark Henderson (Complicated Parapneumonic, Lytics)
            1: "PROCEDURE: Intrapleural Fibrinolysis (Day 1).\n* Indication: Complicated parapneumonic effusion.\n* US: R loculated effusion.\n* Action: Instilled tPA 10mg + DNase 5mg via existing chest tube.\n* Plan: Dwell 1 hr, then suction.",
            2: "INTERVENTIONAL PULMONOLOGY NOTE: Mr. [Name] is undergoing treatment for a complicated parapneumonic effusion. Diagnostic ultrasound of the right hemithorax confirmed the persistence of multiloculated fluid collections. To facilitate drainage, intrapleural fibrinolytic therapy was initiated. A solution containing 10mg tPA and 5mg DNase was instilled via the indwelling right chest tube. The tube was clamped to allow a 1-hour dwell time, after which it will be returned to suction.",
            3: "Billing: 32561 (Fibrinolysis, initial day). 76604-26 (US Chest, limited). \nJustification: Ultrasound performed to assess degree of loculation prior to drug administration. 10mg tPA and 5mg DNase instilled to break up septations described in US findings (thick loculations, isoechoic/hyperechoic).",
            4: "Procedure: Fibrinolytic Instillation\nPatient: [Name]\nDay: 1 (Initial)\n\nSteps:\n1. US chest R: Confirmed loculations.\n2. Verified tube patency.\n3. Instilled tPA 10mg / DNase 5mg.\n4. Flushed with saline.\n5. Clamped tube.\n\nPlan: Unclamp in 1 hour. Monitor for bleeding.",
            5: "mark henderson 62 male with the complex effusion right side chest tube was put in yesterday today we started lytics ultrasound shows its still pretty loculated so gave tpa 10 and dnase 5 clamped the tube nurse to open in an hour no pain or bleeding noted",
            6: "On 12/17/2025 intrapleural lytic therapy was administered for a right sided complicated parapneumonic effusion. Ultrasound confirmed thick loculations. 10 mg of tPA and 5 mg of DNase were instilled through the existing chest tube. This represents the initial day of therapy. The tube was clamped for a dwell time of one hour.",
            7: "[Indication]\nComplicated parapneumonic effusion, Right side.\n[Anesthesia]\nNone required.\n[Description]\nUltrasound showed loculations. 10mg tPA and 5mg DNase instilled via chest tube.\n[Plan]\nDwell 1 hr, then suction. Continue bid for 3 days if indicated.",
            8: "We evaluated Mr. Henderson today for fibrinolytic therapy. His right-sided effusion remains loculated on ultrasound. We proceeded to instill tPA and DNase through his chest tube to help break up the septations. He tolerated the injection well without any pain. The tube has been clamped, and the nursing staff will open it back to suction in one hour.",
            9: "Intervention: Administration of intrapleural fibrinolytics.\nAssessment: Sonography displayed septated fluid.\nAction: Tissue plasminogen activator (10mg) and deoxyribonuclease (5mg) were infused via the indwelling catheter. The drain was occluded for the dwell period. No complications."
        },
        4: { # Elena Rodriguez (Loculated Effusion, Lytics)
            1: "PROCEDURE: Intrapleural Fibrinolysis (Day 1).\n* Indication: Loculated effusion L.\n* US: L large loculated effusion.\n* Action: tPA 10mg / DNase 5mg instilled.\n* Plan: 1 hr dwell, then suction.",
            2: "PROCEDURE NOTE: Ms. [Name] presents with a large loculated left pleural effusion. Ultrasound imaging confirmed the presence of thick septations and organized fluid. To promote drainage, fibrinolytic agents (tPA 10mg and DNase 5mg) were instilled into the pleural space via the existing left chest catheter. This marks the initial day of lytic therapy. The patient remained stable throughout the instillation.",
            3: "Code Selection: 32561 (Initial lytics). 76604-26 (US Chest).\nMedical Necessity: Large loculated effusion on Left. Ultrasound required to verify tube position relative to loculations. Fibrinolytics indicated to prevent surgical decortication.",
            4: "Procedure: TPA/DNase Instillation\nPatient: [Name]\nSite: Left Chest Tube\n\n1. US chest: Loculations confirmed.\n2. Medications: tPA 10mg, DNase 5mg.\n3. Instilled via tube.\n4. Tube clamped.\n\nPlan: Open to suction after 1 hour.",
            5: "patient elena rodriguez 55 female loculated effusion left side started the lytics today ultrasound showed the loculations are thick gave the tpa and dnase through the tube she did fine no pain clamp for an hour then back to suction",
            6: "Fibrinolytic therapy was initiated on 12/18/2025 for a loculated left pleural effusion. Diagnostic ultrasound was performed showing a large volume of loculated fluid. 10mg of tPA and 5mg of DNase were instilled via the left chest tube. The patient tolerated the procedure without complications.",
            7: "[Indication]\nLoculated pleural effusion, Left side.\n[Anesthesia]\nNone.\n[Description]\nUS chest confirmed loculations. tPA 10mg and DNase 5mg instilled via chest tube.\n[Plan]\nMonitor for bleeding. Unclamp in 1 hour.",
            8: "We visited Ms. Rodriguez to start the enzyme treatment for her trapped fluid. The ultrasound of her left chest confirmed that the fluid is stuck in pockets (loculated). We injected the tPA and DNase medication through her chest tube. She didn't feel any discomfort. We've clamped the tube to let the medicine work for an hour.",
            9: "Therapy: Introduction of fibrinolytic agents.\nFindings: Ultrasonic imaging revealed a septated collection.\nExecution: The fibrinolytic and mucolytic agents were introduced into the pleural cavity via the catheter. The system was sealed for the prescribed duration."
        }
    }
    return variations

def get_base_data_mocks():
    return [
        {"idx": 0, "orig_name": "Elen Rogers", "orig_age": 65, "names": ["Sarah Connor", "Emily Blunt", "Ellen Ripley", "Evelyn Salt", "Elaine Benes", "Eleanor Roosevelt", "Elizabeth Swann", "Elsa Arendelle", "Erin Brockovich"]},
        {"idx": 1, "orig_name": "David Obasi", "orig_age": 33, "names": ["Michael Jordan", "LeBron James", "Kobe Bryant", "Shaquille O'Neal", "Stephen Curry", "Kevin Durant", "Giannis Antetokounmpo", "Luka Doncic", "Nikola Jokic"]},
        {"idx": 2, "orig_name": "Linda Kim", "orig_age": 81, "names": ["Betty White", "Maggie Smith", "Judi Dench", "Helen Mirren", "Jane Fonda", "Lily Tomlin", "Meryl Streep", "Glenn Close", "Diane Keaton"]},
        {"idx": 3, "orig_name": "Mark Henderson", "orig_age": 62, "names": ["Tom Hanks", "Brad Pitt", "George Clooney", "Denzel Washington", "Harrison Ford", "Robert De Niro", "Al Pacino", "Morgan Freeman", "Samuel L. Jackson"]},
        {"idx": 4, "orig_name": "Elena Rodriguez", "orig_age": 55, "names": ["Jennifer Lopez", "Salma Hayek", "Penelope Cruz", "Sofia Vergara", "Eva Mendes", "Rosario Dawson", "Zoe Saldana", "Michelle Rodriguez", "Jessica Alba"]}
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
        print(f"Error: Source file must contain a JSON array.")
        return
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through each original note in source data
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
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
            # Note: Note 4 in source data has index 4 in variations dictionary
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                reg = note_entry["registry_entry"]
                if "patient_demographics" in reg and "age_years" in reg["patient_demographics"]:
                    reg["patient_demographics"]["age_years"] = new_age
                
                if "procedure_date" in reg:
                    reg["procedure_date"] = rand_date_str
                
                # Create a synthetic MRN
                if "patient_mrn" in reg:
                    reg["patient_mrn"] = f"SYN_{idx}_{style_num}_{random.randint(1000,9999)}"

            # Add metadata about the synthetic generation
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON
    output_filename = output_dir / "synthetic_bronch_notes_part_026.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()