import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_015.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted variations for the 6 notes in Part 015.
    Structure: Note_Index (0-5) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Gilbert Barkley - Rigid bronch, stents RML/RLL
            1: "Indication: RML/RLL stenosis.\nAnesthesia: General.\nProcedure:\n- Rigid bronch inserted.\n- RML/RLL obstructed by granulation tissue.\n- Stent trial (10x20mm Aero) RLL failed (oversized, removed).\n- 8x20mm Aero stent placed RLL.\n- 8x15mm Aero stent placed RML.\n- CRE balloon dilation performed.\n- Airways patent post-stenting.\nPlan: Admit, nebs, CXR.",
            2: "PROCEDURE PERFORMED: Rigid bronchoscopic recanalization with metallic stenting of the right bronchial tree.\nCLINICAL NARRATIVE: The patient presented with significant anatomical distortion and obstruction of the right-sided airways. Following induction of general anesthesia and establishment of a rigid airway, the right middle and lower lobes were found to be obstructed by granulation tissue. Initial attempts at recanalization via mechanical debulking were insufficient. Consequently, airway stenting was indicated. An initial sizing attempt with a 10mm device in the lower lobe proved oversized and was exchanged. Ultimately, an 8x20mm Aero stent was successfully deployed in the right lower lobe, and an 8x15mm Aero stent was deployed in the right middle lobe. Both devices were dilated with a CRE balloon, resulting in restoration of airway patency.",
            3: "Procedure: Rigid Bronchoscopy (CPT 31641, 31636, 31637)\nTechnique:\n1. Access: 12mm rigid ventilating bronchoscope established access (therapeutic).\n2. Destruction: Extensive debridement of granulation tissue in RML and RLL using mechanical force and cryoprobe (CPT 31641).\n3. Stent 1 (Initial): Deployment of 8x20mm self-expanding metallic stent in Right Lower Lobe (CPT 31636).\n4. Stent 2 (Additional): Deployment of separate 8x15mm self-expanding metallic stent in Right Middle Lobe (CPT 31637).\n5. Dilation: Balloon dilation performed to expand stents.",
            4: "Procedure Note\nPatient: Gilbert Barkley\nAttending: Dr. Gallegos\nProcedure: Rigid bronchoscopy with stenting.\nSteps:\n1. Patient intubated with rigid scope.\n2. Right side inspected; RML/RLL obstructed.\n3. Attempted to clear with saline/forceps.\n4. Placed 10x20mm stent in RLL - too big, removed.\n5. Placed 8x20mm stent in RLL.\n6. Placed 8x15mm stent in RML.\n7. Dilated both with balloon.\n8. Extubated and stable.",
            5: "We did a rigid bronchoscopy on Gilbert Barkley yesterday for bronchial obstruction anesthesia was general. We put the rigid scope down and saw the right side was blocked by granulation tissue. Tried to clean it out but needed stents. Put a 10mm one in first but it was too big so we took it out and put in an 8x20mm in the lower lobe and a 8x15mm in the middle lobe. Dilated them both and they opened up good. Patient went to recovery no issues.",
            6: "The procedure was performed under general anesthesia. A 12 mm rigid bronchoscope was inserted. The right middle and lower lobes were obstructed by granulation tissue. Mechanical debulking was performed but obstruction persisted. We elected to place stents. An initial 10x20 mm stent in the RLL was oversized and replaced with an 8x20 mm covered metallic stent. A second 8x15 mm covered metallic stent was placed in the RML. Both were dilated with a CRE balloon. Final inspection showed patent airways.",
            7: "[Indication]\nRight middle and right lower lobe bronchial stenosis.\n[Anesthesia]\nGeneral Anesthesia via Rigid Bronchoscope.\n[Description]\nRigid bronchoscopy performed. Obstruction of RML and RLL identified. Mechanical and cryo-debulking performed. Stenting required for patency. 8x20mm Aero stent deployed in RLL. 8x15mm Aero stent deployed in RML. Balloon dilation confirmed patency of both segments.\n[Plan]\nAdmit to floor. Nebulizers. Follow-up CXR.",
            8: "Under general anesthesia, the patient's airway was secured with a rigid bronchoscope. Inspection revealed significant obstruction of the right middle and lower lobes due to granulation tissue. Despite efforts to clear the debris with saline and forceps, the obstruction remained. We proceeded to stent placement. After an initial sizing error where a 10mm stent was removed, we successfully placed an 8x20mm covered stent in the right lower lobe and an 8x15mm covered stent in the right middle lobe. Both were dilated, achieving good patency.",
            9: "Procedure: Rigid bronchoscopy with prosthetic positioning.\nFindings: Blockage of RML and RLL.\nAction: The airway was cannulated with a rigid scope. Debris was purged. An 8x20mm stent was deposited in the RLL after a larger trial stent was extracted. An 8x15mm stent was implanted in the RML. Both were expanded via balloon.\nOutcome: Airways recanalized."
        },
        1: { # Oscar Godsey - Rigid bronch, cryo, steroid, stent removal
            1: "Indication: Left lower lobe obstruction, stent removal.\nAnesthesia: General.\nProcedure:\n- LMA placed.\n- LLL obstructed by granulation tissue distal to stent.\n- Cryodebulking performed.\n- Rigid bronch inserted.\n- Left mainstem stent removed.\n- LLL dilated with CRE balloon.\n- Steroid injection (Kenalog) performed.\nPlan: ICU, CXR, repeat bronch 1 week.",
            2: "OPERATIVE SUMMARY: The patient underwent rigid bronchoscopy for management of left mainstem stent obstruction. Upon inspection, the stent itself was patent, but significant granulation tissue was noted distally, obstructing the left lower lobe. This tissue was meticulously debrided using cryotherapy. The decision was made to explant the left mainstem stent given the benign nature of the disease and distal progression. The stent was successfully extracted via the rigid barrel. Subsequent balloon dilation of the left lower lobe bronchi and submucosal injection of corticosteroids were performed to maintain patency and suppress inflammation.",
            3: "Service: Rigid Bronchoscopy (Therapeutic).\nCPT 31641: Destruction of extensive granulation tissue obstructing LLL utilizing cryoprobe and forceps.\nCPT 31631: Removal of indwelling bronchial stent (left mainstem) necessitating rigid bronchoscopy and flexible forceps.\nAdjuncts: Balloon dilation of stenotic segments and steroid injection (bundled or separately reportable depending on payer rules, here coded as part of complex intervention).",
            4: "Procedure Note\nPatient: Oscar Godsey\nStaff: Dr. Parks\nProcedure: Stent removal, cryo, rigid bronch.\nSteps:\n1. LMA induction.\n2. Cryo used to clear granulation tissue in LLL.\n3. Switched to Rigid Bronchoscope.\n4. Grasped and removed left main stent.\n5. Dilated LLL airways with balloon.\n6. Injected Kenalog into granulation tissue.\n7. Extubated.",
            5: "Oscar Godsey 5/15/2019 preop dx stent obstruction. We went in with the LMA first and saw the stent was open but the LLL was blocked by tissue. Used the cryo to freeze and remove it. Then we switched to the rigid scope to take the stent out because we didn't think it was helping anymore. Pulled it out fine. Dilated the airways with a balloon and injected some Kenalog to stop the swelling. Patient went back to ICU.",
            6: "Following induction of general anesthesia, the airway was inspected. The left mainstem stent was patent, but distal granulation tissue obstructed the left lower lobe. This was debulked using cryotherapy. A rigid bronchoscope was then inserted to facilitate stent removal. The left mainstem stent was grasped and removed intact. The underlying airway was patent. We then performed balloon dilation of the LLL segments and injected Kenalog into the mucosal tissue to prevent recurrence.",
            7: "[Indication]\nLeft lower lobe obstruction secondary to granulation tissue; indwelling stent.\n[Anesthesia]\nGeneral Anesthesia (LMA converted to Rigid).\n[Description]\nGranulation tissue at LLL orifice debulked via cryotherapy. Rigid bronchoscope inserted. Left mainstem stent identified and removed. LLL bronchus dilated with CRE balloon. Kenalog injected into mucosa.\n[Plan]\nICU admission. Repeat bronchoscopy in 1 week.",
            8: "We performed a rigid bronchoscopy on Mr. Godsey to address his airway obstruction. Initial inspection showed the left mainstem stent was clear, but tissue overgrowth had blocked the left lower lobe. We cleared this tissue using a cryoprobe. We then decided to remove the stent entirely, which was done successfully using the rigid scope. To ensure the airways remained open, we dilated the lower lobe bronchi with a balloon and injected steroids into the tissue.",
            9: "Procedure: Rigid bronchoscopy with cryo-ablation and prosthesis extraction.\nContext: LLL occlusion.\nAction: Obstructing tissue was eliminated using cryotherapy. The rigid tube was positioned. The left mainstem stent was retrieved. The stenotic segments were widened with a balloon. Steroids were infused into the tissue.\nResult: Improved airway caliber."
        },
        2: { # Gregory Martinez - EBUS-TBNA
            1: "Indication: Lymphadenopathy.\nAnesthesia: Moderate (Midazolam/Fentanyl).\nProcedure:\n- EBUS scope inserted.\n- Systematic staging performed.\n- Station 4R: Sampled x4.\n- Station 7: Sampled x4.\n- Station 11R: Sampled x3.\n- ROSE: Adequate/Positive.\n- No complications.\nPlan: Discharge.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA).\nNARRATIVE: Under moderate sedation, the EBUS bronchoscope was introduced. A systematic evaluation of the mediastinal and hilar lymph node stations was conducted. Significant lymphadenopathy was identified at stations 4R, 7, and 11R. Real-time ultrasound guidance facilitated safe needle aspiration of these targets. Rapid On-Site Evaluation (ROSE) confirmed the presence of diagnostic material in all sampled stations. The patient tolerated the procedure well.",
            3: "Primary Code: 31653 (EBUS-TBNA, 3 or more stations).\nNodes Sampled:\n1. Station 4R (Mediastinal)\n2. Station 7 (Subcarinal)\n3. Station 11R (Hilar)\nTechnique: Real-time ultrasonic guidance with needle aspiration. ROSE confirmation obtained for all sites. Systematic staging documented.",
            4: "Procedure Note\nPatient: Gregory Martinez\nProcedure: EBUS-TBNA\nSteps:\n1. Timeout.\n2. Sedation started.\n3. Examined N3, N2, N1 nodes.\n4. Biopsied 4R, 7, and 11R.\n5. Path confirmed adequacy.\n6. Patient stable.\nPlan: Follow up path results.",
            5: "We did an EBUS on Gregory Martinez today he has some nodes we needed to check. Gave him midaz and fentanyl. Looked at 4R 7 and 11R. Poked them all a few times and the pathologist in the room said we got good samples. Everything went fine no bleeding or anything. Woke him up and sent him home.",
            6: "The patient was sedated with Midazolam and Fentanyl. An EBUS scope was inserted. We identified and sampled lymph nodes at stations 4R, 7, and 11R. Multiple passes were made at each station. Rapid on-site evaluation confirmed adequacy. There were no complications. The patient was discharged in stable condition.",
            7: "[Indication]\nMediastinal and hilar lymphadenopathy.\n[Anesthesia]\nModerate Sedation (ASA II).\n[Description]\nEBUS-TBNA performed. Stations 4R, 7, and 11R visualized and sampled. ROSE confirmed diagnostic material. Molecular samples collected.\n[Plan]\nDischarge. Pathology follow-up.",
            8: "Mr. Martinez underwent an EBUS-TBNA procedure for staging. After achieving moderate sedation, we advanced the scope and systematically evaluated the lymph nodes. We identified enlarged nodes at stations 4R, 7, and 11R. Using ultrasound guidance, we successfully aspirated samples from all three stations. On-site pathology confirmed that the samples were adequate for diagnosis. The patient remained stable throughout.",
            9: "Procedure: EBUS-guided needle sampling.\nTarget: Lymph nodes.\nAction: The scope was navigated to the mediastinum. Stations 4R, 7, and 11R were interrogated. Transbronchial aspiration was executed at all three sites. Specimen adequacy was validated.\nOutcome: Diagnostic cellular material obtained."
        },
        3: { # Janet S. Williams - Pulsed Field Ablation (Investigational)
            1: "Indication: LUL squamous cell CA, research protocol.\nAnesthesia: General.\nProcedure:\n- Navigated to LUL nodule.\n- PFA catheter placed.\n- 3 cycles of non-thermal ablation delivered (1500V).\n- EBUS confirmed cellular disruption.\n- No thermal damage to airway.\nPlan: Research f/u, CT at 48hrs.",
            2: "OPERATIVE REPORT: Investigational Bronchoscopic Pulsed Field Ablation.\nINDICATION: The patient, enrolled in the PULSE-LUNG Phase II trial, presented for ablation of a left upper lobe squamous cell carcinoma. \nPROCEDURE: Under general anesthesia, electromagnetic navigation was utilized to localize the target lesion in the apicoposterior segment. The novel bipolar PFA catheter was deployed. Irreversible electroporation was induced via high-voltage, non-thermal pulses delivered in three cycles. Real-time monitoring confirmed impedance changes consistent with successful treatment. Post-ablation imaging suggested complete tumor necrosis without collateral thermal injury.",
            3: "Code Submitted: 31641 (Destruction of tumor, any method).\nMethodology: Pulsed Field Ablation (Non-thermal irreversible electroporation).\nTarget: Left Upper Lobe Nodule (Malignant).\nGuidance: Electromagnetic Navigation + Radial EBUS.\nDetails: Catheter placed within lesion. 1500V pulses delivered to destroy tumor tissue. Investigational device exemption apply.",
            4: "Procedure Note - Research\nPatient: Janet Williams\nProcedure: Pulsed Field Ablation (PFA)\nSteps:\n1. GA/ETT.\n2. Navigated to LUL lesion with ENB.\n3. Confirmed with REBUS.\n4. Inserted PFA catheter.\n5. Delivered 3 cycles of energy.\n6. Checked site - looks treated.\nNo complications.",
            5: "Janet Williams here for the lung study protocol PULSE-LUNG. She has a cancer in the LUL. We put her under GA and used the navigation system to get there. Put the special PFA catheter in and zapped it with the electrical pulses. Didn't use heat so no burning. Everything looked good on the ultrasound after. She is in the registry now for follow up.",
            6: "General anesthesia was induced. Using the illumiSite navigation platform, we localized the 1.9 cm nodule in the LUL. The PFA catheter was advanced into the lesion. Three cycles of pulsed field ablation were delivered at 1500 V. Intraprocedural monitoring showed effective energy delivery. Post-procedure EBUS demonstrated changes consistent with necrosis. The airways remained intact. The patient was stable.",
            7: "[Indication]\nLeft upper lobe squamous cell carcinoma; Clinical Trial Enrollment.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nNavigation to LUL apicoposterior segment. PFA catheter deployed. 3 cycles of non-thermal irreversible electroporation delivered. Immediate tissue response confirmed via EBUS.\n[Plan]\nProtocol follow-up. Serial CT imaging.",
            8: "Ms. Williams underwent an investigational pulsed field ablation for her lung tumor. We used electromagnetic navigation to reach the nodule in her left upper lobe. Once confirmed, we used the study catheter to deliver electrical pulses that destroy cancer cells without heat. The procedure went exactly as planned, and we saw signs of tumor destruction on the ultrasound immediately afterwards. She will be followed closely as part of the study.",
            9: "Procedure: Bronchoscopic non-thermal tumor destruction.\nTechnique: Pulsed Field Ablation.\nAction: The lesion was targeted via navigation. The electrode was positioned. High-voltage pulses were administered to induce electroporation. The tumor was neutralized without thermal injury to surrounding tissues."
        },
        4: { # Elizabeth Chen - RML Tumor Biopsy
            1: "Indication: RML collapse, rule out obstruction.\nAnesthesia: Moderate/Topical.\nProcedure:\n- RML obstructed by exophytic tumor.\n- 6 forceps biopsies taken.\n- Moderate bleeding, stopped with epi/iced saline.\n- Bronchial wash collected.\nPlan: D/C, awaiting path.",
            2: "PROCEDURE: Diagnostic flexible bronchoscopy.\nFINDINGS: Inspection of the tracheobronchial tree revealed a patent right upper lobe and left bronchial tree. The right middle lobe bronchus, however, was nearly completely occluded by a necrotic, exophytic mass. Endobronchial forceps biopsies were obtained from the lesion to establish a tissue diagnosis. Hemostasis was achieved following moderate hemorrhage. A bronchial washing was also performed for cytological analysis.",
            3: "CPT 31625: Bronchoscopy with bronchial biopsy (Target: RML Tumor).\nCPT 31624: Bronchoscopy with bronchial wash (Target: RML).\nDocumentation of Necessity: Visualization of endobronchial obstruction required tissue sampling. Moderate bleeding management included in base code value.",
            4: "Procedure Note\nPatient: Elizabeth Chen\nProcedure: Bronch with biopsy.\nSteps:\n1. Numbed airway.\n2. Scope down. Normal until RML.\n3. RML blocked by tumor.\n4. Took 6 biopsies.\n5. Washed the area.\n6. Controlled bleeding.\n7. Patient tolerated well.",
            5: "Elizabeth Chen here for RML collapse. We looked down with the scope she was awake just some numbing meds. RML was totally blocked by a tumor looked necrotic. We grabbed like 6 biopsies from it. It bled a fair bit so we used epi and cold saline to stop it. Did a wash too. She did fine oxygen stayed up.",
            6: "Topical anesthesia was applied. The bronchoscope was advanced. The right middle lobe was found to be obstructed by an exophytic tumor. Multiple forceps biopsies were taken from the mass. Bronchial lavage was performed. Moderate bleeding occurred and was controlled with vasoconstrictors. The patient tolerated the procedure well.",
            7: "[Indication]\nRight middle lobe collapse; endobronchial obstruction.\n[Anesthesia]\nModerate Sedation (Topical Lidocaine).\n[Description]\nRML bronchus obstructed by tumor. 6 Forceps biopsies obtained (CPT 31625). Bronchial lavage performed (CPT 31624). Hemostasis achieved after moderate bleeding.\n[Plan]\nMonitor recovery. Pathology pending.",
            8: "We performed a bronchoscopy on Ms. Chen to investigate her collapsed lung. While the upper and left airways looked normal, the right middle lobe was blocked by a large, irregular tumor. We took several biopsies of this mass and collected a fluid sample. There was some bleeding from the biopsy site, which we stopped with medication and cold water. The patient remained comfortable throughout.",
            9: "Procedure: Flexible bronchoscopy with tumor sampling.\nFindings: RML occlusion by neoplasm.\nAction: The airway was scouted. The mass was biopsied using forceps. The area was lavaged. Hemorrhage was arrested with epinephrine.\nOutcome: Specimens sent for analysis."
        },
        5: { # Barbara Kim - Therapeutic Bronch/Bleeding
            1: "Indication: Central airway obstruction.\nAnesthesia: General, ETT.\nIntervention:\n- RML tumor debulking (cautery/APC).\n- Complication: Massive hemoptysis (~300mL).\n- Bleeding controlled (blocker, iced saline).\n- 14x40mm silicone stent placed.\nPlan: ICU, keep intubated, serial HCT.",
            2: "OPERATIVE NOTE: Emergent therapeutic bronchoscopy for massive hemoptysis and tumor debulking.\nCLINICAL COURSE: The patient underwent scheduled debulking of an RML tumor. Intraoperatively, significant hemorrhage was encountered. Hemostasis was achieved through a combination of endobronchial blockade and vasoconstrictive agents. Following stabilization, the airway was recanalized using electrocautery, and a 14x40mm silicone stent was deployed to maintain patency and tamponade the bleeding vessel. The patient remains intubated for airway protection.",
            3: "Procedures Coded:\n1. 31641: Bronchoscopic destruction of tumor (RML) via electrocautery and APC.\n2. 31636: Placement of bronchial stent (Silicone, RML) for airway patency and tamponade.\nJustification: Complex therapeutic intervention required for tumor management and life-threatening hemorrhage control.",
            4: "Procedure Note\nPatient: Barbara Kim\nProcedure: Debulking + Stent.\nEvents:\n1. Started debulking RML tumor.\n2. Massive bleeding started.\n3. Used blocker and iced saline to stop it.\n4. Placed a stent to keep it open and stop bleed.\n5. Patient stable but intubated.\nPlan: ICU.",
            5: "Barbara Kim procedure note. We were debulking her RML tumor when it started bleeding like crazy about 300cc. We had to block it off and use everything we had to stop it. Eventually got it under control. Put a silicone stent in there 14 by 40 to hold it open. She is going to the MICU intubated just to be safe.",
            6: "The patient was intubated for therapeutic bronchoscopy. Debulking of the RML tumor was initiated using electrocautery. This resulted in massive hemoptysis. A bronchial blocker and iced saline were used to achieve hemostasis. A 14x40 mm silicone stent was subsequently placed to secure the airway. The patient was transferred to the ICU for monitoring.",
            7: "[Indication]\nCentral airway obstruction; Tumor debulking.\n[Anesthesia]\nGeneral Anesthesia (ETT).\n[Description]\nRML tumor treated with electrocautery/APC. Complicated by massive hemorrhage. Hemostasis achieved. Silicone stent (14x40mm) deployed.\n[Plan]\nAdmit to MICU. Mechanical ventilation. Monitor H&H.",
            8: "We performed a therapeutic bronchoscopy on Ms. Kim to treat a tumor blocking her airway. During the removal of the tumor using heat therapy, she experienced severe bleeding. We managed to stop the bleeding using a blocker and cold saline. To ensure the airway stayed open and to help prevent further bleeding, we placed a silicone stent. She will remain on the ventilator in the ICU overnight for safety.",
            9: "Procedure: Therapeutic bronchoscopy with tumor ablation and stenting.\nComplication: Significant hemorrhage.\nAction: The neoplasm was ablated. Bleeding was stemmed using a blocker. A silicone prosthesis was inserted to scaffold the airway.\nDisposition: Critical care admission."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the logic
    # Note: In a real scenario, this would be derived dynamically or mapped. 
    # Here, I align them with the indices 0-5 corresponding to the 6 notes in the source file.
    return [
        {"idx": 0, "orig_name": "Gilbert Barkley", "orig_age": 65, "names": ["John Vance", "Arthur Higgins", "Robert Kinsley", "William O'Connor", "James P. Miller", "Edward Stone", "Richard Davis", "Thomas Clark", "Gary Wright"]},
        {"idx": 1, "orig_name": "Oscar Godsey", "orig_age": 65, "names": ["Sarah Jenkins", "Linda Carter", "Nancy Hughes", "Karen Smith", "Barbara Lopez", "Mary Ann Davidson", "Susan White", "Margaret Lewis", "Betty King"]},
        {"idx": 2, "orig_name": "Gregory Martinez", "orig_age": 65, "names": ["Michael Foster", "Robert G. Turner", "David Myers", "Joseph Anderson", "Frank Mitchell", "Paul Reynolds", "George Baker", "Kenneth Roberts", "Steven Phillips"]},
        {"idx": 3, "orig_name": "Janet S. Williams", "orig_age": 58, "names": ["Marie Hall", "Patricia Campbell", "Elizabeth Allen", "Jennifer Young", "Linda Hernandez", "Barbara King", "Dorothy Wright", "Helen Scott", "Carol Green"]},
        {"idx": 4, "orig_name": "Elizabeth Chen", "orig_age": 65, "names": ["James Carter", "William Edwards", "Thomas Harris", "Charles Martin", "Donald Thompson", "Mark Garcia", "Paul Martinez", "George Robinson", "Kenneth Clark"]},
        {"idx": 5, "orig_name": "Barbara Kim", "orig_age": 69, "names": ["Betty Adams", "Sandra Nelson", "Donna Carter", "Carol Mitchell", "Sharon Roberts", "Brenda Phillips", "Pamela Campbell", "Deborah Evans", "Laura Turner"]},
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
            
            # Update note_text with the variation
            # Use style_num as key for text variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                note_entry["note_text"] = f"Variation {style_num} not found for note {idx}."

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry and note_entry["registry_entry"]:
                # Update Age
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                
                # Update Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update Patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    original_mrn = note_entry["registry_entry"].get("patient_mrn", "UNKNOWN")
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
    output_filename = output_dir / "synthetic_blvr_notes_part_015.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()