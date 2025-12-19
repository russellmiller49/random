import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_049.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Sarah Jenkins (Combined EBUS/Nav/Radial) - 31653, 31627, 31654, 31628
            1: "Indication: LUL nodule, mediastinal adenopathy.\nAnesthesia: GA, LMA #4.\nProcedure:\n- EBUS-TBNA: Stations 7, 4R, 4L sampled. Lymphocytes on ROSE.\n- Navigation (SuperDimension): Tool-in-lesion confirmed.\n- Radial EBUS: Concentric view, 20mm lesion.\n- TBBx LUL: 6 passes. Brush x2.\n- ROSE: Adenocarcinoma.\nComplications: None.\nPlan: Oncology.",
            2: "HISTORY: Ms. Jenkins, a 70-year-old female, presented with a spiculated 2.2 cm left upper lobe nodule and mediastinal lymphadenopathy. PET-CT demonstrated hypermetabolism in both the primary lesion and the subcarinal station.\nPROCEDURE: The patient was placed under general anesthesia with a laryngeal mask airway. A comprehensive mediastinal staging was performed utilizing linear endobronchial ultrasound. Transbronchial needle aspiration was conducted at stations 7, 4R, and 4L. Rapid on-site evaluation (ROSE) revealed lymphocytes. Subsequently, electromagnetic navigation bronchoscopy was employed to guide instruments to the LUL apical-posterior segment. Radial probe EBUS confirmed a concentric hypoechoic lesion. Transbronchial biopsies were obtained, yielding a diagnosis of adenocarcinoma on preliminary review.\nIMPRESSION: Primary lung malignancy with mediastinal sampling.",
            3: "Code Selection: 31653 (EBUS-TBNA 3+ stations), 31627 (Navigational Bronchoscopy), 31654 (Radial EBUS peripheral), 31628 (Transbronchial biopsy single lobe).\nTechnique:\n1. Linear EBUS: Distinct sampling of stations 7, 4R, and 4L (3 stations).\n2. Navigation: SuperDimension system utilized for planning and guidance to peripheral LUL target.\n3. Radial EBUS: Utilized to verify peripheral lesion location (concentric view).\n4. Biopsy: Forceps biopsies taken from LUL parenchyma (separate service from EBUS).\nMedical Necessity: Staging and diagnosis of lung cancer.",
            4: "Procedure: EBUS / Nav Bronch / Biopsy\nPatient: Sarah Jenkins\nAttending: Dr. Wright\nSteps:\n1. Time out. GA induced. LMA placed.\n2. Linear EBUS scope introduced. Sampled 7, 4R, 4L. ROSE neg for malig.\n3. Switched to therapeutic scope. Navigated to LUL nodule using EM system.\n4. Radial EBUS probe confirmed lesion (concentric).\n5. Biopsied nodule x6. Brushed x2. ROSE positive for Adeno.\n6. LMA removed. Patient stable.\nPlan: Oncology referral.",
            5: "Procedure note Sarah Jenkins 70F LUL nodule. We did the combined case today general anesthesia LMA. Started with EBUS sampled 7 4R and 4L all looked like lymph tissue on rose. Then did the navigation part used the superdimension stuff got to the LUL nodule. Radial probe showed it nice and concentric. Took biopsies brushes. Path said adenocarcinoma right there in the room. No bleeding really patient woke up fine sent to PACU.",
            6: "Combined EBUS and electromagnetic navigation bronchoscopy. Patient 70F. LUL nodule and adenopathy. General anesthesia LMA. Linear EBUS performed first. Stations 7, 4R, 4L sampled. ROSE benign. Navigation to LUL apical-posterior segment. Radial EBUS confirmation. Transbronchial biopsy x6 and brush x2. ROSE positive for adenocarcinoma. Complications none. Disposition PACU.",
            7: "[Indication]\n2.2 cm LUL nodule, mediastinal adenopathy.\n[Anesthesia]\nGeneral, LMA #4.\n[Description]\nLinear EBUS-TBNA of stations 7, 4R, 4L performed. EMN navigation utilized to reach LUL target. Radial EBUS confirmed concentric lesion. Transbronchial biopsies obtained. ROSE confirmed Adenocarcinoma.\n[Plan]\nOncology referral, molecular testing.",
            8: "Dr. Wright and Dr. Chen performed a combined EBUS and navigational bronchoscopy on Ms. Jenkins. Under general anesthesia, they first staged the mediastinum by sampling lymph node stations 7, 4R, and 4L using linear EBUS. Initial evaluation showed only lymphocytes. They then used electromagnetic navigation to locate the spiculate nodule in the left upper lobe. Radial EBUS confirmed the position. Biopsies taken from this site were positive for adenocarcinoma. The patient tolerated the procedure well.",
            9: "Procedure: Combined ultrasonic staging and guided bronchoscopy.\nAction: The mediastinum was interrogated via linear ultrasound. Stations 7, 4R, and 4L were aspirated. The peripheral lesion was localized using electromagnetic guidance. Radial sonography verified the target. The lesion was sampled via forceps and brush.\nResult: Malignancy confirmed."
        },
        1: { # Robert K. Miller (Chest Tube) - 32557
            1: "Indication: Massive recurrent right pleural effusion.\nProcedure: US-Guided Chest Tube.\n- US: Large free-flowing effusion.\n- 14Fr pigtail placed (Seldinger).\n- 1200mL drained.\n- Fluid sent for cytology/culture.\n- CXR confirmed placement.\nPlan: Drain to dry.",
            2: "HISTORY: Mr. Miller, a 62-year-old male with Stage IV lung malignancy, presented with severe dyspnea secondary to a massive recurrent right pleural effusion.\nPROCEDURE: The right hemithorax was prepared. Bedside ultrasound localized a large, free-flowing effusion amenable to drainage. Under local anesthesia, a 14 French pigtail catheter was inserted utilizing the Seldinger technique. Immediate drainage of 1200 mL of serous fluid provided symptomatic relief. The catheter was secured and placed to suction. Post-procedural imaging verified appropriate positioning.\nIMPRESSION: Successful palliation of malignant pleural effusion via indwelling catheter.",
            3: "Code: 32557 (Pleural drainage with insertion of indwelling catheter, with imaging guidance).\nTechnique: Percutaneous insertion of 14Fr pigtail catheter.\nGuidance: Real-time ultrasound used to identify pocket and guide needle entry.\nDrainage: 1200mL removed.\nDevice: Indwelling catheter left in place for continued drainage.",
            4: "Procedure: Chest Tube Placement\nPatient: Robert K. Miller\nSteps:\n1. Consent obtained. Time out.\n2. US scan of right chest - large fluid pocket.\n3. Lidocaine prep.\n4. Needle in, wire down, dilated tract.\n5. 14Fr pigtail over wire.\n6. Drained 1.2L straw fluid.\n7. Stitched in place. Hooked to suction.\nPlan: CXR.",
            5: "Note for Robert Miller 62M lung ca with big effusion right side. Put a chest tube in today. Used ultrasound to find the spot. Put in a 14 french pigtail using the kit. Got a liter two out right away straw colored. Patient felt way better. Sewed it in connected to wall suction. Xray looks good.",
            6: "Ultrasound-guided right chest tube placement. Patient 62M with metastatic lung cancer. Large right effusion. Local anesthesia. 14Fr pigtail catheter inserted via Seldinger technique. 1200mL drained. Catheter secured. Complications none. CXR confirms position. Plan drainage and possible pleurodesis.",
            7: "[Indication]\nRecurrent massive right pleural effusion, Stage IV lung cancer.\n[Anesthesia]\nLocal (1% Lidocaine).\n[Description]\nUS-guided insertion of 14Fr pigtail catheter (Seldinger technique). 1200mL drained. Tube secured and placed on suction.\n[Plan]\nDrain to dry, consider talc.",
            8: "Mr. Miller was admitted with a massive pleural effusion related to his lung cancer. We decided to place a chest tube for drainage. Using ultrasound guidance, we inserted a small-bore pigtail catheter into the right chest. We drained 1200mL of fluid immediately, which relieved his shortness of breath. The tube was secured, and he will be monitored on the floor.",
            9: "Procedure: Image-guided pleural drainage with catheterization.\nAction: The effusion was visualized sonographically. Access was established percutaneously. An indwelling catheter was advanced into the pleural space. Significant volume (1200mL) was evacuated. The device was anchored.\nResult: Effective drainage."
        },
        2: { # James T. Kirk (Rigid Bronch / Laser / Stent) - 31641, 31631
            1: "Indication: Malignant tracheal stenosis.\nAnesthesia: General (TIVA), Rigid.\nProcedure:\n- Rigid scope inserted.\n- Tumor mid-trachea (80% block).\n- Nd:YAG Laser (30W) destruction.\n- Mechanical debulking.\n- Dumon stent (16x40mm) placed.\n- Airway 90% patent.\nPlan: Extubate.",
            2: "OPERATIVE REPORT: The patient presented with critical central airway obstruction due to malignant tracheal stenosis. General anesthesia was induced. A 14mm rigid bronchoscope was introduced, revealing an exophytic tumor occluding the mid-trachea. Tumor destruction was achieved utilizing the Nd:YAG laser for coagulation and vaporization, supplemented by mechanical coring with the bronchoscope beveled tip. Following hemostasis and restoration of caliber, a 16x40mm silicone Dumon stent was deployed. Final inspection confirmed excellent stent apposition and patency.",
            3: "Coding: 31641 (Destruction of tumor/relief of stenosis), 31631 (Placement of tracheal stent).\nTechnique:\n1. Destruction: Nd:YAG Laser and mechanical debulking of tracheal tumor.\n2. Stenting: Placement of indwelling silicone stent (16x40mm) in the trachea.\nNote: Multiple therapeutic maneuvers performed in the same anatomical region (Trachea).",
            4: "Procedure: Rigid Bronch / Laser / Stent\nPatient: James T. Kirk\nSteps:\n1. General TIVA.\n2. Rigid scope in.\n3. Laser used to burn tumor in trachea.\n4. Cored out the rest with the scope.\n5. Measured for stent.\n6. Deployed 16x40 Dumon stent.\n7. Verified position with flex scope.\nPlan: Recovery.",
            5: "Op report James Kirk. Tracheal tumor. Did rigid bronch. Burned it with the laser then scraped it out. Opened up good. Put a silicone stent in there 16 by 40. Looks solid no bleeding. Woke him up in the room.",
            6: "Rigid bronchoscopy with laser tumor destruction and tracheal stent placement. Patient 60M. Malignant tracheal stenosis. Nd:YAG laser used for tumor ablation. Mechanical debulking performed. 16x40mm Dumon silicone stent deployed in mid-trachea. Airway patent. Hemostasis achieved. Complications none.",
            7: "[Indication]\nMalignant tracheal stenosis (80% obstruction).\n[Anesthesia]\nGeneral (TIVA), Rigid Bronchoscopy.\n[Description]\nNd:YAG laser tumor destruction. Mechanical debulking. Deployment of 16x40mm Dumon silicone stent. Airway patent.\n[Plan]\nExtubate, observe.",
            8: "We took Mr. Kirk to the operating room for a rigid bronchoscopy to treat his tracheal stenosis. We found a tumor blocking most of his windpipe. We used a laser to destroy the tumor tissue and physically removed the debris. To keep the airway open, we placed a silicone stent. The airway is now 90% open, and the stent is sitting perfectly.",
            9: "Procedure: Rigid endoscopy with photo-ablation and prosthetic insertion.\nAction: The tracheal obstruction was targeted. The lesion was vaporized via Nd:YAG energy. Residual tissue was debrided. A silicone prosthesis was positioned within the tracheal lumen to ensure patency.\nResult: Airway caliber restored."
        },
        3: { # Greg (Thoracoscopy) - 32650
            1: "Indication: Undiagnosed right effusion.\nProcedure: Medical Thoracoscopy.\n- Local + MAC.\n- 1.5L bloody fluid drained.\n- Findings: Diffuse parietal nodules.\n- Biopsy x6.\n- Talc poudrage (4g).\n- 24Fr chest tube.\nDx: Suspicious for Mesothelioma.\nPlan: Admit.",
            2: "PROCEDURE NOTE: Medical Thoracoscopy. The patient was positioned in the left lateral decubitus position. Following induction of MAC, a trocar was introduced into the right 5th intercostal space. Thoracoscopic inspection revealed hemorrhagic effusion (1.5L evacuated) and extensive nodularity of the parietal pleura, sparing the visceral surface. Multiple parietal pleural biopsies were obtained. To prevent recurrence, talc poudrage was performed under direct vision. A chest tube was placed. Clinical impression suggests mesothelioma.",
            3: "Code: 32650 (Thoracoscopy, surgical; with pleurodesis).\nRationale:\n- Method: Surgical thoracoscopy (VATS/Medical Thoracoscopy).\n- Therapeutic Agent: Talc poudrage insufflated for pleurodesis.\n- Bundling: Biopsies (32602) are typically bundled into the comprehensive pleurodesis code when performed in the same session for the same pathology.",
            4: "Procedure: Pleuroscopy / Talc\nPatient: Greg\nSteps:\n1. MAC sedation. Local.\n2. Trocar in.\n3. Suctioned 1.5L bloody fluid.\n4. Saw nodules all over chest wall.\n5. Grabbed biopsies x6.\n6. Sprayed talc (4g).\n7. Chest tube in.\nPlan: Wait for path.",
            5: "Thoracoscopy note for Greg MRN 12345. Right effusion. Went in with the scope found bloody fluid and nodules everywhere on the parietal pleura. Looks like mesothelioma. Took a bunch of biopsies. Sprayed talc for pleurodesis. Put a tube in. Admitting him.",
            6: "Medical thoracoscopy right. Patient 50M. Undiagnosed effusion. 1.5L hemorrhagic fluid drained. Diffuse parietal pleural nodules visualized. Biopsies performed. Talc poudrage pleurodesis performed. 24Fr chest tube placed. Diagnosis suspicious for mesothelioma. Disposition admission.",
            7: "[Indication]\nUndiagnosed right pleural effusion.\n[Anesthesia]\nMAC + Local.\n[Description]\nTrocar entry. Drainage of 1.5L bloody fluid. Parietal nodules biopsied. Talc poudrage (4g) administered. Chest tube placed.\n[Plan]\nAdmit, Oncology consult.",
            8: "We performed a medical thoracoscopy on Greg to investigate his pleural effusion. After draining a large amount of bloody fluid, we saw many nodules lining the chest wall. We took several biopsies of these nodules. To stop the fluid from coming back, we sprayed sterile talc into the chest cavity. A chest tube was left in place to drain any remaining fluid.",
            9: "Procedure: Thoracoscopic exploration with pleurodesis.\nAction: The pleural space was accessed. Hemorrhagic fluid was evacuated. Nodular pathology on the parietal surface was sampled. A sclerosing agent (talc) was insufflated. A drainage catheter was sited.\nResult: Tissue obtained; symphysis attempted."
        },
        4: { # Lisa Simpson (Bronchial Thermoplasty) - 31660
            1: "Indication: Severe asthma.\nProcedure: Bronchial Thermoplasty (Session 1/3).\n- GA/ETT.\n- Alair catheter.\n- Treated RLL segments (Posterior, Lateral, Anterior, Medial, Superior).\n- 59 activations total.\n- No bleeding.\nPlan: Discharge. Next session in 3 weeks.",
            2: "PROCEDURE NOTE: The patient presented for the initial session of Bronchial Thermoplasty for refractory severe asthma. Under general anesthesia, the Alair system was deployed. Systematic treatment of the right lower lobe was undertaken. Radiofrequency energy was delivered to the distal airways of all basal segments and the superior segment, totaling 59 activations. The bronchial mucosa appeared blanched consistent with effective treatment. The patient tolerated the procedure well without bronchospasm.",
            3: "Code: 31660 (Bronchial Thermoplasty, one lobe).\nTarget: Right Lower Lobe (RLL).\nDetails:\n- Initial session.\n- System: Alair.\n- Activations: 59 total across RLL segments.\n- Scope: Diagnostic bronchoscopy included.",
            4: "Procedure: Thermoplasty RLL\nPatient: Lisa Simpson\nSteps:\n1. GA / Tube.\n2. Airway check.\n3. Alair catheter used.\n4. Zapped RLL segments (59 times total).\n5. Checked for bleeding - none.\n6. Woke patient up.\nPlan: Home.",
            5: "Thermoplasty session 1 for Lisa Simpson. Severe asthma. Did the RLL today. General anesthesia. Used the Alair probe. Did about 59 activations in the lower lobe. Went fine no bleeding. Patient stable.",
            6: "Bronchoscopy with bronchial thermoplasty. Patient 8F (Adult size/context). Severe asthma. General anesthesia. RLL treated. 59 activations delivered to basal and superior segments. Alair system used. Complications none. Extubated. Stable.",
            7: "[Indication]\nSevere refractory asthma.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nBronchial thermoplasty of RLL performed. 59 activations delivered via Alair catheter. Mucosa blanched. No bleeding.\n[Plan]\nDischarge, Session 2 in 3 weeks.",
            8: "Lisa came in for her first bronchial thermoplasty treatment for severe asthma. We focused on the right lower lobe today. Under anesthesia, we used a special catheter to deliver heat energy to the airway walls, completing 59 activations. This helps reduce the smooth muscle mass. She woke up fine with no issues.",
            9: "Procedure: Endobronchial radiofrequency ablation (Thermoplasty).\nAction: The RLL was targeted. Thermal energy was applied to the bronchial walls via the Alair device. 59 applications were administered. Mucosal reaction was observed.\nResult: Treatment of RLL completed."
        }
    }
    return variations

def get_base_data_mocks():
    # Mock names corresponding to the patients in part 049
    return [
        {"idx": 0, "orig_name": "Sarah Jenkins", "orig_age": 70, "names": ["Mary Williams", "Patricia Brown", "Linda Jones", "Barbara Miller", "Elizabeth Davis", "Jennifer Garcia", "Maria Rodriguez", "Susan Wilson", "Margaret Martinez"]},
        {"idx": 1, "orig_name": "Robert K. Miller", "orig_age": 62, "names": ["James Davis", "John Miller", "Robert Wilson", "Michael Taylor", "William Anderson", "David Thomas", "Richard Jackson", "Joseph White", "Thomas Harris"]},
        {"idx": 2, "orig_name": "James T. Kirk", "orig_age": 60, "names": ["William Shatner", "Christopher Pike", "Jean-Luc Picard", "Leonard Nimoy", "George Takei", "Montgomery Scott", "Pavel Chekov", "Nyota Uhura", "Hikaru Sulu"]},
        {"idx": 3, "orig_name": "Greg", "orig_age": 50, "names": ["Hugh Laurie", "Robert Chase", "Eric Foreman", "James Wilson", "Allison Cameron", "Lisa Cuddy", "Remy Hadley", "Chris Taub", "Lawrence Kutner"]},
        {"idx": 4, "orig_name": "Lisa Simpson", "orig_age": 8, "names": ["Maggie Simpson", "Marge Simpson", "Bart Simpson", "Homer Simpson", "Ned Flanders", "Milhouse Van Houten", "Ralph Wiggum", "Nelson Muntz", "Seymour Skinner"]}
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
            new_age = max(1, orig_age + random.randint(-3, 3)) # Ensure age > 0
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                note_entry["note_text"] = f"VARIATION MISSING for Note {idx} Style {style_num}"

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
    output_filename = output_dir / "synthetic_notes_part_049.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()