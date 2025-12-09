import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (Part 028)
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_028.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of pre-generated text variations for the notes in Part 028.
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
        0: { # Index 0: Rigid Bronch, Tumor Debulk, Stent, PleurX (Mrs. Okafor)
            1: "Procedures: Rigid bronchoscopy, mechanical tumor debridement, APC, balloon dilation, stent placement (RMS), PleurX catheter.\nIndication: Critical RMS obstruction, tamponade, effusion.\nFindings: 90% obstruction RMS (fungating tumor). Effusion.\nActions:\n- Rigid scope inserted. Jet ventilation.\n- Tumor cored/debrided. Hemostasis w/ epi/APC.\n- 14x60mm covered metal stent placed RMS. Patent.\n- Pericardial window (CT Surg).\n- PleurX catheter placed right chest. 850ml drained.\nComplications: None.",
            2: "OPERATIVE NARRATIVE: The patient presented with critical central airway obstruction and tamponade physiology. Following induction, a rigid bronchoscopic approach was utilized for the right mainstem (RMS) lesion. Significant fungating tumor burden obstructing 90% of the RMS was noted. Mechanical coring was performed with the rigid barrel, supplemented by Argon Plasma Coagulation (APC) for hemostasis and tissue destruction (CPT 31641). Following balloon dilation, a 14x60mm partially covered self-expanding metallic stent was deployed (CPT 31636), restoring patency to the RUL, RML, and RLL. Subsequently, a tunneled indwelling pleural catheter was inserted for palliation of malignant effusion (CPT 32550).",
            3: "Code Selection Support:\n1. 31641 (Bronchoscopy, Rigid, with destruction of tumor): Rigid scope used to mechanically core 90% obstruction in Right Mainstem. APC used for destruction.\n2. 31636 (Bronchoscopy with Stent): Placement of Boston Scientific Ultraflex (14x60mm) in Right Mainstem Bronchus following dilation.\n3. 32550 (Tunneled Pleural Catheter): Ultrasound-guided insertion of PleurX catheter for recurrent malignant effusion.\nNote: Pericardial window performed by Thoracic Surgery (billed separately).",
            4: "Resident Procedure Note\nAttending: Dr. Kim\nProcedure: Rigid Bronch, Stent, PleurX.\nSteps:\n1. TFBC showed 90% RMS obstruction.\n2. Switched to Rigid Bronch (Storz 13mm).\n3. Debrided tumor manually and with APC.\n4. Placed stent (14x60mm) in RMS. Confirmed patency to all right segments.\n5. CT surgery did pericardial window.\n6. We placed PleurX tube in right chest using standard Seldinger technique.\nPlan: ICU for airway monitoring.",
            5: "Procedure note for Mrs Okafor we did the rigid bronchoscopy today for that large mass in the right mainstem patient was intubated then we switched to the rigid scope used the tip to core out the tumor lots of bleeding but controlled with iced saline and APC. Put in a stent 14 by 60 covered metal one looks wide open now. Also put in a pleurx catheter for the fluid in the lung drained about 850 cc. Oh and surgery did the heart window thing. Patient stable sent to ICU.",
            6: "The patient was brought to the hybrid OR for management of complex airway and pleural disease. General anesthesia was induced. Initial flexible inspection confirmed near-total obstruction of the right mainstem bronchus. A rigid bronchoscope was introduced. The tumor was mechanically debrided and cauterized using APC. A 14x60mm covered metallic stent was deployed, restoring ventilation to the right lung. Following this, the right hemithorax was accessed under ultrasound guidance, and a tunneled pleural catheter was placed without difficulty. 850mL of fluid was evacuated. The patient tolerated the procedures well.",
            7: "[Indication]\nMetastatic lung cancer with critical airway obstruction and malignant pleural effusion.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy with Jet Ventilation.\n[Description]\n1. Rigid bronchoscopy performed. 90% RMS obstruction debrided via coring/APC. Stent (14x60mm) deployed. Airway patent.\n2. Pericardial window (by CT Surgery).\n3. Tunneled pleural catheter placed right chest. Fluid drained.\n[Plan]\nICU monitoring. CXR. PleurX education.",
            8: "Mrs. Okafor was taken to the operating room for multimodal palliation. We began with the airway intervention, utilizing a rigid bronchoscope to address the critical obstruction in the right mainstem bronchus. Through a combination of mechanical coring and argon plasma coagulation, we successfully debulked the tumor. To maintain patency, we deployed a covered metallic stent. Once the airway was secure, we turned our attention to the pleural space, inserting a tunneled indwelling catheter to manage her recurrent effusion. The procedure concluded successfully with improved aeration of the right lung.",
            9: "Operation: Rigid endoscopy with tumor eradication and stent implantation.\nDetails: The right mainstem bronchus displayed severe blockage. We navigated the rigid scope to the lesion. The tissue was excised using the scope tip and ablated with argon plasma. A prosthetic stent was anchored across the stricture, re-establishing luminal patency. Subsequently, a drainage catheter was installed in the pleural cavity to evacuate fluid collection.",
        },
        1: { # Index 1: EBUS-TBNA (Sarah Martinez)
            1: "Procedure: EBUS-TBNA.\nIndication: Mediastinal staging.\nNodes Sampled:\n- 4R (18mm): Positive for Adeno.\n- 7 (22mm): Positive for Adeno.\n- 10R (14mm): Positive for Adeno.\nTechnique: 22G needle, 3-4 passes per station.\nResult: N3 disease (Contralateral/Supraclavicular not sampled, but extensive N2 involved).",
            2: "DIAGNOSTIC OPERATIVE NOTE: The patient underwent endobronchial ultrasound-transbronchial needle aspiration (EBUS-TBNA) for mediastinal staging. The airway was inspected and found to be patent. Systematic ultrasonic evaluation of the mediastinum revealed lymphadenopathy in stations 4R, 7, and 10R. Real-time guided aspiration was performed utilizing a 22-gauge needle. Rapid On-Site Evaluation (ROSE) confirmed the presence of malignant cells consistent with adenocarcinoma in all sampled stations, confirming multi-station N2 disease.",
            3: "CPT Coding Data:\n- 31653 (EBUS-TBNA, first 3 stations): Biopsies taken from stations 4R, 7, and 10R.\n- 31622 (Dx Bronch): Bundled.\nMedical Necessity: Staging for RUL mass.\nTechnique: Ultrasound guidance used for needle visualization during all passes. Images archived.",
            4: "Procedure: EBUS\nResident: Dr. Rogers\nPatient: Sarah Martinez\nSteps:\n1. Moderate sedation.\n2. Airway exam normal.\n3. EBUS scope down. Found nodes at 4R, 7, 10R.\n4. Biopsied all three with 22G needle.\n5. ROSE said cancer (adeno).\nPlan: Oncology referral.",
            5: "We did the EBUS on Sarah Martinez today indication was staging. Sedation was fine versed fentanyl. Looked at the nodes 4R was big so we stuck it 4 times came back cancer. Station 7 also big stuck that one too cancer. 10R also positive. So looks like stage III disease. No bleeding patient woke up fine.",
            6: "Endobronchial ultrasound-guided transbronchial needle aspiration was performed for staging of a right upper lobe mass. The EBUS bronchoscope was introduced. Lymph node stations 4R, 7, and 10R were identified, measured, and sampled using a 22-gauge needle under real-time ultrasound guidance. Cytopathology confirmed adenocarcinoma in all sampled stations. The procedure was well tolerated without complication.",
            7: "[Indication]\nMediastinal lymphadenopathy, staging for RUL mass.\n[Anesthesia]\nModerate Sedation.\n[Description]\nEBUS performed. Nodes sampled: 4R, 7, 10R. \nPathology: Adenocarcinoma confirmed in all stations.\n[Plan]\nRefer to Oncology for Stage IIIB treatment.",
            8: "Ms. Martinez underwent an EBUS procedure today to stage her lung cancer. After checking her airways, which looked clear, we used the ultrasound scope to locate enlarged lymph nodes in the middle of her chest. We took samples from the right paratracheal, subcarinal, and right hilar nodes. Unfortunately, the preliminary results from the pathologist in the room showed cancer cells in all three areas, indicating the disease has spread to the lymph nodes.",
            9: "Procedure: Endosonography with needle extraction.\nTarget: Mediastinal nodes.\nAction: Stations 4R, 7, and 10R were visualized. A needle was propelled into each node to harvest cells. The specimens were analyzed immediately.\nResult: Malignancy detected in all stations.",
        },
        2: { # Index 2: Cryoablation (Rosa Martinez)
            1: "Procedure: Bronchoscopic Cryoablation LUL.\nTarget: 1.8cm nodule.\nTechnique: ENB + r-EBUS to localize. Cryoprobe inserted.\nAblation: 2 cycles (5 min freeze / 3 min thaw).\nResult: Ice ball visualized. No bleeding.\nPlan: D/C home.",
            2: "OPERATIVE REPORT: The patient presented for bronchoscopic ablation of a biopsy-proven Stage IA1 adenocarcinoma in the LUL. Electromagnetic navigation (SPiN system) was utilized to navigate to the anterior segment. Radial EBUS confirmed concentric probe placement. A 2.4mm cryoprobe was deployed. Therapeutic cryoablation was administered via two freeze-thaw cycles (5 minutes each). Fluoroscopic imaging confirmed the formation of an ice ball encompassing the lesion margin. Post-procedure inspection revealed no hemorrhage.",
            3: "Billing Record:\n- 31641 (Destruction of tumor, bronchoscopic): Cryoablation of LUL nodule.\n- 31627 (Navigational Bronchoscopy): Used for localization.\n- 31654 (Radial EBUS): Used for verification of target.\nDevice: Erbe Cryo 2 system.\nTime: Ablation duration 300s x 2.",
            4: "Procedure: Cryoablation LUL\nStaff: Dr. Patterson\nSteps:\n1. Navigated to LUL nodule with ENB.\n2. Checked with rEBUS - concentric view.\n3. Put cryo probe in.\n4. Freezing x 2 cycles.\n5. Saw ice ball on fluoro.\nNo complications.",
            5: "Rosa Martinez here for the freezing procedure cryoablation. She has that small cancer in the LUL. We used the navigation system to get there and the ultrasound probe to make sure we were in the middle. Put the freezing probe in and froze it for 5 minutes then let it thaw then froze it again. Ice ball looked good on the xray screen. Patient did great no bleeding.",
            6: "Bronchoscopic cryoablation of left upper lobe nodule. Patient is a 63-year-old female with stage IA1 adenocarcinoma. Under general anesthesia, electromagnetic navigation was used to reach the LUL target. Radial EBUS confirmed lesion position. A cryoprobe was advanced and two freeze-thaw cycles were performed to ablate the tumor. An ice ball was visualized fluoroscopically. There were no immediate complications.",
            7: "[Indication]\nLUL Nodule, Stage IA1 NSCLC, non-surgical candidate.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nNavigation to LUL. r-EBUS confirmation. Cryoablation performed (2 cycles). Ice ball confirmed. Airways intact.\n[Plan]\nDischarge. CT chest 4 weeks.",
            8: "Because Ms. Martinez wasn't a candidate for surgery, we proceeded with cryoablation of her lung nodule. We navigated a bronchoscope to the small tumor in her left upper lobe and confirmed its location with ultrasound. We then inserted a specialized freezing probe and performed two freezing cycles to destroy the tumor tissue. We could see the ice ball forming on the x-ray monitor, ensuring we treated the whole area.",
            9: "Procedure: Endobronchial cryotherapy.\nTarget: Peripheral pulmonary lesion.\nAction: The instrument was steered to the LUL using electromagnetic guidance. The position was authenticated via radial ultrasound. A cryo-tip was inserted, and thermal ablation was executed via freezing cycles.\nOutcome: Lesion destruction visually confirmed via fluoroscopy.",
        },
        3: { # Index 3: EBUS + Ion (Elizabeth Morrison)
            1: "Procedure: EBUS-TBNA & Ion Robotic Bronchoscopy.\nEBUS: Stations 4R, 7 sampled. Positive for Adeno.\nIon: Navigated to RLL mass. r-EBUS concentric. Biopsied x8.\nROSE: Adenocarcinoma in node and mass.\nDx: Stage IIIA (N2 positive).",
            2: "OPERATIVE NARRATIVE: A combined staging and diagnostic procedure was performed. First, convex EBUS allowed for sampling of stations 4R and 7; rapid on-site evaluation demonstrated adenocarcinoma. Subsequently, the Ion robotic platform was docked. The catheter was navigated to the RLL posterior basal segment mass. Radial EBUS confirmed concentric alignment. Transbronchial biopsies were obtained. The pathologic findings confirm primary lung adenocarcinoma with mediastinal nodal involvement (N2 disease).",
            3: "Codes:\n- 31652 (EBUS-TBNA 1-2 stations): Sampled 4R, 7.\n- 31628 (Transbronchial lung biopsy): RLL mass via Ion.\n- 31627 (Navigational Bronchoscopy): Ion system used.\n- 31654 (Radial EBUS): Peripheral lesion check.\nNote: Nodal staging performed first.",
            4: "Resident Note\nPt: Morrison, Elizabeth\nProc: EBUS + Ion\nSteps:\n1. EBUS first. Biopsied 4R and 7. Both malignant.\n2. Switched to Ion robot.\n3. Navigated to RLL mass.\n4. rEBUS showed we were in the lesion.\n5. Took biopsies.\nImpression: Stage 3 Lung Cancer.",
            5: "We did a combined case today EBUS and the robot. Started with EBUS sampled the 4R and 7 nodes both looked cancerous on the slide. Then used the Ion robot to go out to that mass in the right lower lobe. Navigation was smooth. Biopsied the mass too confirmed it was the same cancer. So she has stage 3A.",
            6: "Combined endobronchial ultrasound and robotic navigational bronchoscopy. Mediastinal staging was performed first via EBUS-TBNA of stations 4R and 7, revealing metastatic adenocarcinoma. The Ion robotic system was then utilized to navigate to a right lower lobe mass. Radial EBUS confirmed target acquisition. Transbronchial biopsies of the mass also showed adenocarcinoma. The patient was extubated and transferred to recovery.",
            7: "[Indication]\nRLL mass, mediastinal adenopathy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\n1. EBUS-TBNA: 4R, 7 positive for malignancy.\n2. Ion Robotics: Navigation to RLL mass. Biopsies positive for malignancy.\n[Plan]\nOncology consult for Stage IIIA NSCLC.",
            8: "Mrs. Morrison underwent a diagnostic bronchoscopy today. We started by checking the lymph nodes in the center of her chest using the EBUS scope. Unfortunately, the samples from nodes 4R and 7 showed cancer cells. We then used the robotic system to navigate to the main tumor in her lower right lung and took a biopsy of that as well, which matched the lymph nodes. This confirms the cancer has spread to the lymph nodes, placing her at Stage IIIA.",
            9: "Procedure: Endosonography and Robotic-assisted bronchoscopy.\nFindings: Mediastinal nodes 4R and 7 were sampled and found malignant. The primary RLL lesion was accessed via the robotic platform and sampled.\nConclusion: Primary adenocarcinoma with nodal metastasis.",
        },
        4: { # Index 4: Ion + Fiducials (Marcus Thompson)
            1: "Procedure: Ion Nav Bronch + Fiducials.\nTarget: LLL mass (3.8cm).\nAction: Navigated to lesion. r-EBUS eccentric. Biopsied x5. Placed 3 fiducial markers.\nResult: Markers visible on fluoro.\nPlan: Refer for SBRT.",
            2: "OPERATIVE NOTE: The patient presented for fiducial placement to facilitate stereotactic body radiation therapy (SBRT). The Ion robotic system was utilized to navigate to the left lower lobe mass. Following histologic confirmation via transbronchial biopsy (CPT 31628), four gold fiducial markers were deployed within and around the tumor volume (CPT 31626). Fluoroscopy confirmed appropriate spacing and stability of the markers.",
            3: "Coding:\n- 31627 (Navigation)\n- 31626 (Fiducial markers): Primary intent for SBRT guidance.\n- 31628 (Biopsy): Tissue confirmation.\n- 31654 (REBUS): Localization.\nTarget: LLL Mass.",
            4: "Procedure: Ion + Fiducials\nResident: Dr. Mitchell\nPatient: Marcus Thompson\nSteps:\n1. Navigated to LLL mass with Robot.\n2. Confirmed with rEBUS.\n3. Took biopsies.\n4. Dropped fiducials for Rad Onc.\n5. Fluoro showed good placement.",
            5: "Mr Thompson is here for markers. He has that LLL mass. We used the robot to get there. Biopsied it first to be sure then put in the gold markers for the radiation doctors. Put in four of them. Looks good on the screen. No pneumothorax.",
            6: "Robotic navigational bronchoscopy with fiducial placement. The Ion system was used to access a left lower lobe mass. Radial EBUS confirmed lesion location. Transbronchial biopsies were obtained. Subsequently, fiducial markers were deployed into the lesion under fluoroscopic guidance to assist with future radiation therapy. Post-procedure imaging ruled out pneumothorax.",
            7: "[Indication]\nLLL mass, need tissue and markers for SBRT.\n[Anesthesia]\nGeneral.\n[Description]\nIon navigation to LLL. Biopsy performed. Fiducial markers (x4) placed. Position confirmed.\n[Plan]\nRadiation Oncology follow-up.",
            8: "We performed a procedure on Mr. Thompson to prepare him for radiation therapy. Using the robotic bronchoscope, we navigated to the tumor in his left lower lung. We took a sample to confirm the diagnosis and then placed several small gold markers, or fiducials, directly into the tumor. These will act as targets for the radiation machine to treat the cancer precisely.",
            9: "Procedure: Robotic-assisted guidance with implantation of radiotherapy markers.\nAction: The LLL lesion was reached. Tissue was sampled. Metallic markers were deposited within the target volume.\nOutcome: Markers authenticated via fluoroscopy.",
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the 5 base patients to maintain consistency across variations.
    original_index 0: Mrs. Okafor (Female, ~65) -> Rigid Bronch
    original_index 1: Sarah Martinez (Female, 58) -> EBUS
    original_index 2: Rosa Martinez (Female, 63) -> Cryo
    original_index 3: Elizabeth Morrison (Female, 55) -> Ion EBUS
    original_index 4: Marcus Thompson (Male, 69) -> Ion Fiducials
    """
    return [
        {"idx": 0, "orig_name": "Ada Okafor", "orig_age": 65, "gender": "Female", "names": ["Mary Smith", "Susan Johnson", "Linda Williams", "Patricia Brown", "Barbara Jones", "Elizabeth Garcia", "Jennifer Miller", "Maria Davis", "Margaret Rodriguez"]},
        {"idx": 1, "orig_name": "Sarah Martinez", "orig_age": 58, "gender": "Female", "names": ["Lisa Wilson", "Nancy Martinez", "Karen Anderson", "Betty Taylor", "Helen Thomas", "Sandra Hernandez", "Donna Moore", "Carol Martin", "Ruth Jackson"]},
        {"idx": 2, "orig_name": "Rosa Martinez", "orig_age": 63, "gender": "Female", "names": ["Sharon Thompson", "Michelle White", "Laura Lopez", "Sarah Lee", "Kimberly Gonzalez", "Deborah Harris", "Jessica Clark", "Shirley Lewis", "Cynthia Robinson"]},
        {"idx": 3, "orig_name": "Elizabeth Morrison", "orig_age": 55, "gender": "Female", "names": ["Angela Walker", "Melissa Perez", "Brenda Hall", "Amy Young", "Anna Allen", "Rebecca Sanchez", "Virginia Wright", "Kathleen King", "Pamela Scott"]},
        {"idx": 4, "orig_name": "Marcus Thompson", "orig_age": 69, "gender": "Male", "names": ["James Green", "John Baker", "Robert Adams", "Michael Nelson", "William Hill", "David Ramirez", "Richard Campbell", "Joseph Mitchell", "Thomas Roberts"]},
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
    
    # We only have variations for the first 5 distinct notes in this script
    # to demonstrate the capability as per instructions.
    notes_to_process = min(len(source_data), len(base_data))
    
    for idx in range(notes_to_process):
        original_note = source_data[idx]
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
            
            # Get the specific name
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation if available
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen for 0-4)
                continue

            # Update registry_entry fields to maintain validity
            if "registry_entry" in note_entry:
                # Update Age
                # Note: The source json might not have 'patient_age' key directly in registry_entry
                # based on part_028, but if it does, we update it.
                # If not, we might inject it or leave as is. 
                # For safety, we check or create.
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
    output_filename = output_dir / "synthetic_notes_part_028.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()