import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_027.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the specified year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the 5 notes in bronch_notes_part_027.json.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Jamal Washington (Empyema, tPA/DNase instillation + US)
            1: "Pre-op: Empyema L hemithorax.\nProc: Bedside US + tPA/DNase instillation.\nFindings: US chest left showed moderate complex effusion, thick septations. Hyperechoic. Tube in place.\nAction: Instilled 10mg tPA / 5mg DNase via existing L chest tube. Clamped.\nPlan: Dwell 1 hr then suction.",
            2: "PROCEDURE NOTE: INTRA-PLEURAL FIBRINOLYTIC THERAPY\nINDICATION: Mr. Washington, a 38-year-old male with a loculated left-sided empyema, required therapeutic instillation of fibrinolytic agents to facilitate drainage.\nIMAGING: Real-time thoracic ultrasonography of the left hemithorax demonstrated a moderate volume pleural effusion characterized by hyperechogenicity and thickened septations, consistent with the diagnosis of empyema.\nINTERVENTION: Through the pre-existing left chest tube, a solution containing 10 mg of tissue plasminogen activator (tPA) and 5 mg of deoxyribonuclease (DNase) was instilled using aseptic technique.\nPLAN: The catheter will remain clamped for 60 minutes to maximize therapeutic effect before returning to suction.",
            3: "Service: Intrapleural Instillation (CPT 32561) & Chest Ultrasound (CPT 76604-26)\nDiagnosis: Empyema (J86.9).\nTechnique:\n1. Ultrasound Assessment: Real-time scanning of the left chest was performed. Findings documented: Moderate effusion, hyperechoic with thick loculations. Images saved.\n2. Instillation: Using the indwelling left chest catheter, the initial dose of fibrinolytic agents (10mg tPA/5mg DNase) was administered to break up loculations.\nOutcome: Tolerance good. No immediate complications.",
            4: "Resident Procedure Note\nPatient: Jamal Washington\nProcedure: Chest US and tPA/DNase instillation (Day 1).\nStaff: Dr. Van Dyke.\nSteps:\n1. Timeout performed.\n2. Bedside US of left chest: Saw moderate effusion, very septated/thick.\n3. Existing chest tube checked.\n4. Instilled tPA 10mg and DNase 5mg.\n5. Clamped tube.\nPlan: Unclamp in 1 hour.",
            5: "procedure note for jamal washington he has an empyema on the left side we did the ultrasound first it showed a lot of loculations thick stuff hyperechoic moderate size. so we went ahead and put in the tpa and dnase 10 and 5 mg into the chest tube on the left. patient tolerated it fine no issues clamped it for an hour chest tube to suction after.",
            6: "Jamal Washington 38M with empyema presented for fibrinolytic therapy. Ultrasound of the left chest was performed revealing a moderate hyperechoic effusion with thick loculations. Through the existing left chest tube, 10 mg tPA and 5 mg DNase were instilled for the initial treatment. There were no complications. The tube was clamped for a dwell time of one hour.",
            7: "[Indication]\nLeft-sided Empyema requiring fibrinolysis.\n[Imaging]\nBedside US Left Chest: Moderate volume, hyperechoic, thick loculations confirmed.\n[Description]\nInstillation of 10mg tPA and 5mg DNase via existing left chest tube (Initial day).\n[Plan]\nClamped for 1 hour, then suction.",
            8: "Mr. Washington underwent bedside ultrasound and fibrinolytic instillation for his left-sided empyema today. The ultrasound examination of the left hemithorax revealed a moderate-sized effusion that appeared hyperechoic with thick internal loculations, confirming the need for therapy. Subsequently, we instilled 10 mg of tPA and 5 mg of DNase through his existing left chest tube without difficulty. He tolerated the procedure well, and the tube was clamped to allow the medication to dwell.",
            9: "Indication: Empyema.\nScan: Sonographic evaluation of the left thorax displayed a moderate collection with dense septations.\nTreatment: Administered 10mg tPA and 5mg DNase through the indwelling left pleural catheter to dissolve loculations.\nOutcome: Procedure completed successfully. No adverse events."
        },
        1: { # Priya Perry (Hemothorax, tPA/DNase instillation + US)
            1: "Dx: Organizing Hemothorax (Right).\nProc: US Chest + Fibrinolysis.\nUS Findings: R effusion, moderate, loculated, hyperechoic.\nAction: 10mg tPA / 5mg DNase injected via R chest tube.\nPlan: Clamp 1 hr. Suction.",
            2: "OPERATIVE NARRATIVE: Mrs. Perry, a 72-year-old female with an organizing right hemithorax, underwent ultrasonic evaluation and intrapleural fibrinolytic therapy. Bedside thoracic ultrasound of the right hemithorax revealed a moderate pleural fluid collection with complex, hyperechoic echotexture and significant loculation. Consequently, 10 mg of tPA and 5 mg of DNase were instilled via the indwelling right thoracostomy tube to promote lysis of the organized hematoma. The patient remained hemodynamically stable throughout.",
            3: "Procedures Coded:\n- 76604-26: Ultrasound, chest. Findings: Right hemithorax, moderate volume, hyperechoic, thick loculations documented.\n- 32561: Instillation via chest tube, fibrinolytic agent (initial). Agents: 10mg tPA, 5mg DNase.\nMedical Necessity: Management of multiloculated hemithorax (J94.2) to avoid surgical decortication.",
            4: "Procedure Note\nPt: Priya Perry\nAttending: Dr. Van Dyke\nProcedure: US Chest and tPA/DNase instillation.\nSteps:\n1. Positioned patient L lateral decubitus.\n2. US Right chest: Moderate effusion, looks like blood (hyperechoic), loculated.\n3. Instilled lytics (10 tPA/5 DNase) into right tube.\n4. Flushed line.\n5. Clamped.\nPatient tolerated well.",
            5: "note for priya perry shes got that right hemothorax organizing. we did the ultrasound looks moderate size loculated hyperechoic on the right side. tube is in good position so we put in the tpa 10mg and dnase 5mg. no complications she did fine. keep it clamped for an hour then open it up.",
            6: "Patient Priya Perry 72F with organizing right hemothorax. Bedside ultrasound of the right chest performed showing moderate hyperechoic loculated effusion. 10 mg tPA and 5 mg DNase were instilled via the right chest tube. No complications occurred. Plan for 1 hour dwell time.",
            7: "[Indication]\nOrganizing Right Hemothorax.\n[Imaging]\nUS Right Chest: Hyperechoic, loculated, moderate volume effusion.\n[Description]\nInstillation of fibrinolytic agents (10mg tPA/5mg DNase) via right chest tube.\n[Plan]\nMonitor vitals. Open chest tube in 60 mins.",
            8: "Ms. Perry was seen for management of her organizing right hemothorax. We performed a bedside chest ultrasound which visualized a moderate, hyperechoic effusion with thick loculations on the right side. Based on these findings, we proceeded to instill 10 mg of tPA and 5 mg of DNase through her right chest tube to help break up the clot. The procedure was uncomplicated.",
            9: "Indication: Clotted Hemothorax.\nImaging: Sonography of the right chest revealed a moderate, septated fluid collection.\nTherapy: Infused 10mg Alteplase and 5mg DNase via the right thoracostomy catheter.\nResult: Successful administration. No issues noted."
        },
        2: { # Sean O'Malley (Complex Septated Effusion, tPA/DNase + US)
            1: "Indication: Complex septated effusion L.\nProc: US Chest + Lytic Instillation.\nUS: Left side, large volume, isoechoic, thick loculations.\nIntervention: 10mg tPA / 5mg DNase via L chest tube.\nResult: Tolerated well.",
            2: "PROCEDURE: Intrapleural administration of fibrinolytic agents with ultrasound guidance.\nPATIENT: Sean O'Malley, 50M.\nCLINICAL SUMMARY: The patient presents with a complex septated effusion. Thoracic ultrasound of the left hemithorax demonstrated a large, isoechoic effusion with thick internal septations and diminished diaphragmatic excursion. To address the multiloculated nature of the effusion, 10 mg tPA and 5 mg DNase were instilled via the existing left chest catheter.",
            3: "Billing Record:\n- CPT 76604-26 (US Chest): Left hemithorax scanned. Findings: Large, isoechoic, thick loculations. Image stored.\n- CPT 32561 (Fibrinolysis): Instillation of 10mg tPA/5mg DNase via chest tube for complex effusion.\nNote: Initial day of therapy.",
            4: "Resident Note\nPatient: Sean O'Malley\nProcedure: US & Lytic instillation.\nFindings:\n- Left chest US: Large effusion, really thick septations, isoechoic.\n- Diaphragm not moving much.\nAction: Put tPA 10 and DNase 5 into the left tube.\nPlan: Clamp 1hr.",
            5: "sean omalley 50 year old male complex effusion left side. ultrasound showed large fluid collection thick loculations isoechoic. we put the meds in the tube 10 tpa 5 dnase. no issues patient is fine. check him in an hour.",
            6: "Sean O'Malley 50M with complex septated left effusion. Ultrasound chest performed left side showing large isoechoic effusion with thick loculations and diminished diaphragmatic motion. Instilled 10 mg tPA and 5 mg DNase via left chest tube. No complications. Dwell time 1 hour.",
            7: "[Indication]\nComplex Septated Effusion (Left).\n[Imaging]\nUS Left Chest: Large, isoechoic, thick loculations.\n[Description]\nInstillation of 10mg tPA and 5mg DNase via left chest tube.\n[Plan]\nSuction after 1 hour dwell.",
            8: "We evaluated Mr. O'Malley for his complex left-sided effusion. Bedside ultrasound of the left chest was significant for a large volume effusion that was isoechoic with thick loculations, indicating a complex process. We then instilled 10 mg of tPA and 5 mg of DNase into the left chest tube to facilitate drainage. The patient tolerated the procedure without any adverse events.",
            9: "Indication: Multiloculated Effusion.\nVisualization: Ultrasonic assessment of the left thorax showed a large, septated collection.\nTreatment: Administered 10mg tPA and 5mg DNase through the left pleural drain.\nOutcome: Completed without incident."
        },
        3: { # Nina Hill (Airway Stenosis, Balloon, Biopsy, BAL, Aspiration)
            1: "Indication: Airway stenosis.\nAnesthesia: GA.\nProcedure:\n- Aspiration: Cleared mucus RMS/BI/LMS.\n- Inspection: Stents patent (RLL/RML).\n- Biopsy: BI x2 (NBI guided).\n- BAL: RLL (40cc in/15cc out).\n- Dilation: RB2 orifice to 5mm w/ balloon x3.\nComplications: None.",
            2: "OPERATIVE REPORT: Ms. Hill presented for therapeutic bronchoscopy due to airway stenosis. Under general anesthesia, the airway was inspected. Significant mucus burden was noted and therapeutically aspirated from the right mainstem, bronchus intermedius, and left mainstem. The bronchus intermedius was biopsied under NBI guidance. Inspection of previously placed iCAST stents in the RLL and RML revealed good positioning. Bronchoalveolar lavage was obtained from the RLL. The RB2 orifice stenosis was addressed via balloon dilation using a 5mm Mustang balloon, inflated three times for 60 seconds each to a diameter of 5mm.",
            3: "Coding Justification:\n- 31630: Balloon dilation of RB2 orifice (primary procedure). 5mm balloon used.\n- 31625: Endobronchial biopsy of Bronchus Intermedius (separate site).\n- 31645: Therapeutic aspiration of mucus from RMS, BI, LMS (distinct from lavage).\n- 31624: BAL of RLL (distinct site, separate diagnostic intent).\nDiagnoses: J98.09.",
            4: "Procedure Note\nPt: Nina Hill\nAttending: Dr. Johnson\nProcedures: Bronch, balloon dilation, bx, BAL, aspiration.\nSteps:\n1. Suctioned a lot of mucus out of RMS/BI/LMS.\n2. Biopsied BI x2.\n3. Checked stents (RLL/RML) - looked good.\n4. BAL RLL.\n5. Dilated RB2 with 5mm balloon x3.\nPatient stable.",
            5: "procedure note for nina hill she has airway stenosis. we did a bronch under general. sucked out a bunch of mucus from the right and left mains. did a biopsy of the bronchus intermedius. washed the rll. saw the stents they look okay. dilated the rb2 with a 5mm balloon three times. no complications patient woke up fine.",
            6: "Nina Hill 85F with airway stenosis. Therapeutic aspiration performed clearing mucus from RMS BI and LMS. Endobronchial biopsies taken from Bronchus Intermedius. RLL and RML stents inspected and patent. BAL performed RLL. Balloon dilation of RB2 orifice to 5mm performed 3 times. No complications.",
            7: "[Indication]\nAirway stenosis, mucus plugging.\n[Anesthesia]\nGeneral.\n[Description]\n1. Therapeutic aspiration: RMS, BI, LMS cleared.\n2. Biopsy: BI x2.\n3. BAL: RLL.\n4. Dilation: RB2 to 5mm (balloon).\n[Plan]\nFollow up in clinic.",
            8: "Ms. Hill underwent a complex bronchoscopy today for airway stenosis. We began by performing therapeutic aspiration to clear significant mucus from the right mainstem, bronchus intermedius, and left mainstem. We then took endobronchial biopsies from the bronchus intermedius. We inspected her existing stents in the RLL and RML, which appeared well-positioned. A BAL was performed in the RLL for microbiology. Finally, we treated the stenosis at the RB2 orifice using a 5mm balloon, dilating it three times for 60 seconds each. She tolerated the procedure well.",
            9: "Indication: Bronchial narrowing.\nActions:\n- Cleared secretions from proximal airways.\n- Sampled tissue from Bronchus Intermedius.\n- Lavaged RLL.\n- Expanded RB2 orifice using a pneumatic balloon.\nOutcome: Improved patency."
        },
        4: { # Arvin T Hsu (RPP - Ablation, Cryo, Dilation)
            1: "Indication: RPP / Airway obstruction.\nAnesthesia: GA, LMA.\nProcedure:\n- Flex bronch: Papillomas at larynx, trachea.\n- Cryo/Cautery: Ablated papillomas vocal cords/trachea.\n- Rigid Bronch: Cored/dilated proximal trachea to 12mm.\n- Debridement: Removed debris.\nResult: Patency improved 40% -> 90%.",
            2: "OPERATIVE REPORT: Mr. Hsu presented with recurrent respiratory papillomatosis causing significant airway obstruction. A multimodal approach was utilized. Laryngeal and tracheal papillomas were treated with cryotherapy and electrocautery. A rigid tracheoscope was employed to mechanically debulk and dilate the proximal tracheal stenosis from an initial 40% patency to 12mm diameter. Extensive debridement of coagulated tissue was performed to ensure airway clearance. Post-procedure patency was estimated at 90%.",
            3: "Billing Justification:\n- 31641-22: Bronchoscopic destruction of tumor/stenosis. Modifier 22 applied for extensive multimodal therapy (Cryo, Cautery, Mechanical) across multiple sites (Larynx, Trachea) significantly increasing time/complexity.\n- Note: Rigid dilation (31630) is bundled into 31641 at the same site. Biopsies (31625) bundled.\nOutcome: Restoration of airway.",
            4: "Resident Note\nPt: Arvin Hsu\nDx: RPP\nProcedure: Bronch w/ ablation, rigid dilation.\nSteps:\n1. LMA placed.\n2. Flex scope: Papillomas everywhere (VCs, trachea).\n3. Froze them (cryo) and burned them (cautery).\n4. Used rigid scope to core out the trachea and dilate to 12mm.\n5. Cleaned up all the debris.\nAirway looks much better (90% open).",
            5: "arvin hsu with rpp and airway obstruction. we did a rigid and flex bronch. lots of papillomas on the cords and trachea. used cryo and cautery to kill them. then used the rigid to core it out and dilate the trachea to 12mm. took a while but we got it open from 40 percent to 90 percent. no bleeding. sent tissue to path.",
            6: "Arvin T Hsu 49M with RPP. Multimodal destruction of papillomas performed using cryotherapy electrocautery and mechanical debridement via flexible and rigid bronchoscopy. Proximal trachea dilated to 12mm using rigid scope. Tumor burden reduced significantly with airway patency improving from 40% to 90%. Tolerated well.",
            7: "[Indication]\nRecurrent Respiratory Papillomatosis, Tracheal Stenosis.\n[Anesthesia]\nGeneral.\n[Description]\n1. Ablation (Cryo/Cautery) of laryngeal/tracheal papillomas.\n2. Rigid dilation/coring of proximal trachea to 12mm.\n3. Debridement of debris.\n[Plan]\nRepeat bronch 4-6 weeks.",
            8: "Mr. Hsu underwent a therapeutic bronchoscopy for his recurrent respiratory papillomatosis. We identified extensive papillomas on the vocal cords and in the proximal trachea causing stenosis. We treated these lesions using a combination of cryospray and electrocautery. We then utilized the rigid bronchoscope to mechanically core through the tracheal tumor and dilate the airway to 12mm. After removing the debris, the airway patency improved significantly from 40% to 90%.",
            9: "Indication: Papillomatosis.\nTherapy:\n- Destructed lesions on cords and trachea using thermal and cryo energy.\n- Expanded tracheal narrowing with rigid scope.\n- Extracted tumor debris.\nResult: Airway caliber restored."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data to assign consistent random names for each style index.
    """
    return [
        {"idx": 0, "orig_name": "Jamal Washington", "orig_age": 38, "names": ["Marcus Cole", "David King", "James Brooks", "Robert Hayes", "Michael Turner", "William Bennett", "Richard Foster", "Thomas Reed", "Charles Griffin"]},
        {"idx": 1, "orig_name": "Priya Perry", "orig_age": 72, "names": ["Anita Patel", "Mei Lin", "Sarah Johnson", "Linda Davis", "Barbara Wilson", "Susan Martinez", "Margaret Anderson", "Betty Taylor", "Dorothy Thomas"]},
        {"idx": 2, "orig_name": "Sean O'Malley", "orig_age": 50, "names": ["Liam Connor", "Patrick Ryan", "Kevin Murphy", "Brian Kelly", "John Sullivan", "Daniel Walsh", "Timothy O'Brien", "Joseph Kennedy", "Frank Byrne"]},
        {"idx": 3, "orig_name": "Nina Hill", "orig_age": 85, "names": ["Eleanor Vance", "Florence White", "Clara Hall", "Alice Allen", "Martha Young", "Louise Hernandez", "Frances King", "Rose Wright", "Evelyn Scott"]},
        {"idx": 4, "orig_name": "Arvin T Hsu", "orig_age": 49, "names": ["Kenji Sato", "Wei Chen", "Jun Kim", "Minh Tran", "Hiroshi Tanaka", "Liang Zhang", "Jin Lee", "Takeshi Yamamoto", "Sheng Wang"]}
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
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the specific variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation is missing (should not happen with correct setup)
                note_entry["note_text"] = f"Variation {style_num} for note {idx} not found."

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_demographics" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                # Update procedure date in registry entry
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    original_mrn = note_entry["registry_entry"]["patient_mrn"]
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
    output_filename = output_dir / "synthetic_bronch_notes_part_027.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()