import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_015.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILE = "synthetic_bronch_notes_part_015.json"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns synthetic names and base ages for the 5 patients in the source file.
    Since the source has 'UNKNOWN', we assign realistic names here.
    """
    return [
        {
            "idx": 0, # Esophageal Cancer / Y-Stent
            "orig_name": "Eleanor Vance", 
            "orig_age": 68, 
            "names": ["Eleanor Vance", "Martha Higgins", "Roberta Kinsley", "Wilma O'Connor", "Janet Miller", "Edith Stone", "Rita Davis", "Thelma Clark", "Grace Wright"]
        },
        {
            "idx": 1, # Bilobar LUL/LLL Obstruction
            "orig_name": "Thomas Anderson", 
            "orig_age": 72, 
            "names": ["Thomas Anderson", "Arthur Dent", "Robert Paulson", "William Foster", "James P. Sullivan", "Edward Norton", "Richard Kimble", "Thomas Crown", "Gary Oldman"]
        },
        {
            "idx": 2, # LMS Aero Stent
            "orig_name": "Marcus Wright", 
            "orig_age": 65, 
            "names": ["Marcus Wright", "Lucas Bishop", "Nathan Drake", "Caleb Widogast", "Beau Regard", "Fjord Stone", "Jester Lavorre", "Veth Brenatto", "Caduceus Clay"]
        },
        {
            "idx": 3, # BI Obstruction / Pus / Balloon
            "orig_name": "Samuel Vimes", 
            "orig_age": 75, 
            "names": ["Samuel Vimes", "Havelock Vetinari", "Mustrum Ridcully", "Gytha Ogg", "Esmeralda Weatherwax", "Ponder Stibbons", "Rincewind The Wizzard", "Carrot Ironfoundersson", "Angua von Uberwald"]
        },
        {
            "idx": 4, # BI Obstruction / Laser / Coring
            "orig_name": "Jean-Luc Picard", 
            "orig_age": 70, 
            "names": ["Jean-Luc Picard", "William Riker", "Geordi La Forge", "Worf Rozhenko", "Beverly Crusher", "Deanna Troi", "Data Soong", "Miles O'Brien", "Wesley Crusher"]
        }
    ]

def get_variations():
    """
    Returns a dictionary of 9 stylistic variations for each of the 5 notes.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Note 0: Esophageal Ca / Y-Stent
            1: "Procedure: Rigid Bronchoscopy, Y-Stent Placement.\n- Indication: Esophageal ca, TE fistula, airway compression.\n- Anesthesia: General, LMA then Rigid.\n- Findings: Mass prox LMS (80% obs). TE fistula 2mm distal to carina. RMS 70% compressed.\n- Action: Rigid scope inserted. Forceps bx LMS. APC debulking (90% patent). Silicone Y-stent (14x10x10) deployed via rigid. \n- Outcome: Stent seated. Fistula covered. Airways patent.\n- Plan: CXR, hypertonic saline.",
            2: "OPERATIVE REPORT: RIGID BRONCHOSCOPY AND PALLIATIVE RECANALIZATION.\nThe patient, presenting with advanced esophageal carcinoma complicated by a tracheoesophageal fistula, underwent therapeutic intervention. Under general anesthesia, initial inspection revealed significant extrinsic compression of the right mainstem and direct endobronchial invasion of the left mainstem with an associated fistulous tract. Employing a 12mm ventilating rigid bronchoscope, we performed mechanical debulking and thermal ablation via Argon Plasma Coagulation (APC) to restore luminal patency. Subsequently, a customized Silicone Y-stent was precisely deployed to stent the carina, successfully excluding the fistula and stabilizing the compromised airways.",
            3: "PROCEDURE CODES JUSTIFICATION:\n1. 31641 (Tumor Destruction): Extensive APC thermal ablation and mechanical shaving performed on proximal Left Mainstem tumor to relieve 80% obstruction.\n2. 31631 (Stent Placement, Tracheal/Carinal): Deployment of Silicone Y-stent (tracheal, right, and left limbs) to treat carinal fistula and extrinsic compression. \nNote: Biopsy (31625) performed but bundled. Rigid bronchoscopy utilized for stent delivery.",
            4: "Procedure Note\nResident: Dr. Smith\nAttending: Dr. Jones\nDiagnosis: Esophageal Ca with TE fistula.\nProcedure Steps:\n1. Time out.\n2. LMA placed. Flex bronch showed LMS tumor and fistula.\n3. Switched to Rigid Bronch (12mm).\n4. Biopsied mass. APC used for hemostasis and debulking.\n5. Y-Stent (Silicone) loaded and deployed via rigid scope.\n6. Flexible check confirmed position covering fistula.\nComplications: Tongue laceration.",
            5: "dictation for patient vance unkown mrn date 11/08/2025... we did a rigid bronchoscopy for the esophageal cancer patient she had a fistula... trachea looked ok but left main was blocked 80 percent... used apc and forceps to clear it out... then we put in a silicone y stent had some trouble with the freitag forceps so we used the rigid scope to push it down... stent looks good covers the hole... oh yeah she bit her tongue a bit small cut... plan is hypertonic saline and follow up in a month.",
            6: "The patient was brought to the bronchoscopy suite and placed under general anesthesia. Initial flexible inspection via LMA revealed a large esophageal tumor invading the left mainstem bronchus with a visible TE fistula and extrinsic compression of the right mainstem. We transitioned to a 12mm rigid bronchoscope. Biopsies were taken, followed by APC cautery and mechanical debulking of the left mainstem lesion. A silicone Y-stent was customized and deployed to cover the fistula and open both mainstems. Post-deployment inspection showed excellent stent position and patent airways.",
            7: "[Indication]\nEsophageal cancer with extrinsic airway compression and TE fistula.\n[Anesthesia]\nGeneral Anesthesia (LMA converted to Rigid).\n[Description]\nRigid bronchoscopy performed. Left mainstem tumor debulked using APC and mechanical forceps. Silicone Y-stent (14x10x10) deployed. Stent confirmed to cover fistula and patent airways.\n[Plan]\nAdmit to PACU. CXR. Hypertonic saline nebulizers.",
            8: "The patient presented with esophageal cancer and a suspected TE fistula. We proceeded with a rigid bronchoscopy under general anesthesia. Upon entering the airway, we noted a significant mass in the proximal left mainstem and a small fistula near the carina. We utilized Argon Plasma Coagulation (APC) to debulk the tumor and control bleeding. To manage the fistula and the extrinsic compression on the right side, we deployed a silicone Y-stent. The stent was successfully seated, covering the fistula and maintaining patency in both mainstem bronchi.",
            9: "PREOPERATIVE DIAGNOSIS: Esophageal cancer.\nPROCEDURE: Rigid bronchoscopy, sampled lesion, tumor resection, and Silicone Y-stent deployment.\nDETAILS: The bronchoscope was navigated to the obstruction. The mass was sampled. APC was utilized to cauterize and resect the tissue. A Y-stent was positioned to bridge the fistula. The airway was stabilized."
        },
        1: { # Note 1: Bilobar LUL/LLL Obstruction
            1: "Procedure: Flex Bronch, APC, Snare, Cryo.\n- Indication: Bilobar collapse (LUL/LLL).\n- Findings: Vascular masses obstructing LUL and LLL orifices.\n- LUL: Snare excision + APC. 100% patent.\n- LLL: Snare + Cryoextraction + APC. 70% patent (distal disease).\n- EBL: Moderate, controlled w/ TXA.\n- Plan: PACU, Oncology f/u.",
            2: "OPERATIVE SUMMARY: The patient presented with complete bilobar collapse of the left lung. Under general anesthesia, flexible bronchoscopy revealed vascular endobronchial lesions obstructing both the Left Upper Lobe (LUL) and Left Lower Lobe (LLL). We employed a multimodal interventional approach. For the LUL, electrocautery snare resection and Argon Plasma Coagulation (APC) resulted in complete recanalization. The LLL lesion was more extensive; despite aggressive debulking via cryoextraction and APC, only partial (70%) patency was achieved due to distal tumor infiltration.",
            3: "CODING SUMMARY:\n- 31641 (Destruction/Relief of Stenosis): Primary code for LLL intervention using Cryoextraction and APC to relieve obstruction.\n- 31640-XS (Tumor Excision): Secondary code for LUL intervention using Electrocautery Snare to excise a distinct tumor at a separate anatomic site.\n- 31622 Bundled.",
            4: "Procedure Note\nPatient: Thomas Anderson\nProcedure: Bronchoscopy w/ Debulking\n1. General Anesthesia/LMA.\n2. Inspection: LUL and LLL obstructed by tumor.\n3. LUL: Snare used to remove proximal tumor. APC for base. Open.\n4. LLL: Snare and Cryoprobe used. APC for hemostasis. Partial opening.\n5. Hemostasis achieved with TXA.\nPlan: PACU, Oncology.",
            5: "op note for mr anderson... he had collapse of the left lung... went in with the scope and saw tumor in both the upper and lower lobes... used the snare to cut the top one out worked great... bottom one was harder used the cryo probe and apc to burn it... got it open maybe 70 percent but it goes deep... moderate bleeding used txa... patient stable to recovery.",
            6: "Flexible bronchoscopy was performed under general anesthesia for left lung collapse. Inspection revealed vascular tumors obstructing both the LUL and LLL. The LUL tumor was resected using an electrocautery snare and APC, achieving complete patency. The LLL tumor was debulked using a combination of snare, cryoextraction, and APC; however, due to extensive distal involvement, only 70% patency was restored. Hemostasis was secured with topical TXA.",
            7: "[Indication]\nMalignant bilobar obstruction (LUL and LLL).\n[Anesthesia]\nGeneral Anesthesia via LMA.\n[Description]\nFlexible bronchoscopy performed. LUL tumor excised with snare/APC (fully open). LLL tumor treated with Cryo/Snare/APC (70% open). TXA used for hemostasis.\n[Plan]\nMonitor in PACU. Oncology referral for metastatic disease.",
            8: "Mr. Anderson underwent a flexible bronchoscopy to address a left lung collapse. We identified tumors blocking both the upper and lower lobes. For the upper lobe, we used a snare and APC to remove the mass, fully opening the airway. The lower lobe was more challenging; we used a cryoprobe and APC to remove as much tissue as possible, but the tumor extended deep into the airways. We managed to open it to about 70%. Bleeding was controlled, and the patient was sent to recovery.",
            9: "PROCEDURE: Flexible bronchoscopy with cryo-resection, cautery snare and APC.\nDETAILS: Vascular masses were identified occluding the LUL and LLL. The LUL lesion was resected via snare. The LLL lesion was extracted using a cryoprobe and ablated with APC. Hemostasis was secured. The LUL was recanalized; the LLL was partially cleared."
        },
        2: { # Note 2: LMS Aero Stent
            1: "Procedure: Rigid Bronch, Aero Stent LMS.\n- Indication: LMS obstruction.\n- Findings: Complete obstruction proximal LMS.\n- Action: Rigid scope. Cryo/APC/Forceps debulking. \n- Stent: 12x40mm Aero SEMS placed over guidewire.\n- Result: >90% patency.\n- Plan: ICU, 3% saline nebs.",
            2: "OPERATIVE NARRATIVE: The patient presented with complete malignant stenosis of the Left Mainstem (LMS) bronchus. Rigid bronchoscopy was initiated under general anesthesia. The obstruction was recanalized using a combination of cryoextraction and Argon Plasma Coagulation (APC) 'burn and shave' techniques. Due to significant residual tumor burden and the risk of re-occlusion, a decision was made to deploy a stent. A 12x40mm Aero Self-Expanding Metallic Stent (SEMS) was positioned under fluoroscopic guidance, achieving >90% luminal patency.",
            3: "BILLING DATA:\n- 31641: Bronchoscopy with tumor destruction (APC/Cryo/Forceps) in Left Mainstem.\n- 31636: Bronchoscopy with stent placement (Aero 12x40mm) in initial bronchus (LMS).\nNote: Diagnostic bronchoscopy and fluoroscopy are bundled.",
            4: "Procedure: Rigid Bronchoscopy + Stenting\nResident: Dr. Bishop\nSteps:\n1. General anesthesia.\n2. Rigid scope to distal trachea.\n3. Debulked LMS tumor using Cryo and APC.\n4. Measured obstruction.\n5. Placed Jagwire and markers.\n6. Deployed 12x40mm Aero stent.\n7. Confirmed position >90% open.\nPlan: ICU, Saline nebs.",
            5: "patient with left mainstem blockage... did a rigid bronch in the OR... tumor was blocking everything so we used the cryo probe to pull chunks out and apc to burn the rest... still looked like it might close up so we put in an aero stent 12 by 40... used fluoro to see where it went... looks good now wide open... back to icu start saline nebs.",
            6: "Rigid bronchoscopy was performed for complete left mainstem obstruction. The tumor was debulked using cryoextraction and APC. To maintain patency against residual tumor burden, a 12x40mm Aero covered stent was deployed over a guidewire under fluoroscopic guidance. Final inspection revealed excellent stent position with >90% airway patency. The patient was intubated and transferred to the ICU.",
            7: "[Indication]\nMalignant Left Mainstem Obstruction.\n[Anesthesia]\nGeneral Anesthesia (Rigid Bronchoscopy).\n[Description]\nTumor in LMS debulked via Cryo and APC. 12x40mm Aero stent deployed under fluoroscopy. Airway patent >90%.\n[Plan]\nICU admission. Hypertonic saline nebulizers.",
            8: "We took the patient to the OR for a rigid bronchoscopy to treat a blocked left mainstem bronchus. We removed the bulk of the tumor using a freezing probe (cryo) and cautery (APC). Because there was still some tumor pressing on the airway, we decided to place a stent. We used fluoroscopy to guide a 12x40mm Aero stent into place. This opened the airway up to over 90% of its normal size. The patient is heading to the ICU for recovery.",
            9: "PROCEDURE: Rigid bronchoscopy with Aero tracheobronchial stent deployment.\nFINDINGS: Complete occlusion of the LMS.\nINTERVENTION: The lesion was ablated and extracted using cryotherapy and APC. An Aero stent was positioned to scaffold the airway.\nRESULT: Restored patency to >90%."
        },
        3: { # Note 3: BI Obstruction (Rigid/APC/Balloon)
            1: "Procedure: Rigid Bronch, Tumor Debulking BI/RUL.\n- Indication: Tumor obstruction BI.\n- Findings: Pus distal to obstruction. BI tumor + radiation bronchitis.\n- Action: Radial cuts (electrocautery), drained pus. APC/Forceps debulking. Balloon dilation (6-8mm).\n- Result: BI 70% open, RUL 85% open. No stent placed.\n- Plan: Antibiotics (Augmentin), Oncology f/u.",
            2: "OPERATIVE REPORT: The patient presented with a complex obstruction of the Bronchus Intermedius (BI) and Right Upper Lobe (RUL) complicated by post-obstructive pneumonia. Rigid bronchoscopy was utilized. Initial incision with an electrocautery knife released copious purulent material, which was cultured. Mechanical debulking and APC were employed to remove tumor tissue. Subsequent CRE balloon dilation achieved 70% patency in the BI and 85% in the RUL. Stenting was deferred due to extensive distal tumor infiltration.",
            3: "BILLING CODES:\n- 31641: Destruction of tumor (APC) in Bronchus Intermedius.\n- 31640-XS: Excision of tumor (Forceps) in Right Upper Lobe (separate site).\n- 31645-XS: Therapeutic aspiration of large volume pus (post-obstructive pneumonia).\nNote: Balloon dilation (31630) is bundled.",
            4: "Procedure: Rigid Bronchoscopy\nPatient: Samuel Vimes\n1. General Anesthesia/Paralytics.\n2. Rigid scope inserted.\n3. Found tumor/pus in BI.\n4. Drained pus (culture sent).\n5. Debulked BI and RUL using APC and Forceps.\n6. Dilated with CRE balloon.\n7. Hemostasis w/ APC.\nPlan: Augmentin, CT chest.",
            5: "rigid bronch for tumor in the bronchus intermedius... lots of pus when we cut into it so we sucked that out... looks like radiation damage too... used apc and the balloon to open things up... got the bi open about 70 percent and the rul 85 percent... decided not to stent cause the tumor goes too deep... gave him augmentin for the pneumonia.",
            6: "Rigid bronchoscopy was performed for right-sided airway obstruction. Large volume purulent fluid was drained from the distal airways following incision of the tumor in the bronchus intermedius. The tumor was debulked using APC and forceps, followed by CRE balloon dilation. We achieved 70% patency in the BI and 85% in the RUL. Stenting was contraindicated due to distal disease extension. The patient was treated for post-obstructive pneumonia.",
            7: "[Indication]\nTumor obstruction BI, Post-obstructive pneumonia.\n[Anesthesia]\nGeneral Anesthesia (Rigid).\n[Description]\nPurulent fluid drained. Tumor in BI and RUL debulked with APC/Forceps. Balloon dilation performed. No stent placed.\n[Plan]\nAugmentin 10 days. Repeat CT. Oncology consult.",
            8: "Mr. Vimes had a rigid bronchoscopy to clear a tumor blocking his right lung. When we opened the blockage, we found a lot of infection (pus) behind it, which we drained. We used heat (APC) and balloons to widen the airways in the bronchus intermedius and the right upper lobe. We got them mostly open, but we couldn't put a stent in because the tumor goes too far down. We started him on antibiotics for the infection.",
            9: "PROCEDURE: Rigid bronchoscopy.\nINTERVENTION: The obstruction was incised, and purulence was aspirated. The lesion was ablated with APC and mechanically resected. The airway was dilated via balloon.\nRESULT: The BI was recanalized to 70%; RUL to 85%. Stent deployment was deemed inappropriate."
        },
        4: { # Note 4: BI Obstruction (Rigid/Laser/Coring)
            1: "Procedure: Rigid Bronch, Laser/Coring BI.\n- Indication: BI tumor obstruction.\n- Findings: Large polypoid tumor BI (100% blocked). RUL 30% blocked.\n- Action: Nd:YAG Laser. Rigid 'apple coring'. Suction removal. APC cleanup.\n- Result: BI 85% open proximal, 60% distal. RUL 80% open.\n- Plan: No stent (patient pref). Oncology referral.",
            2: "OPERATIVE NARRATIVE: The patient underwent rigid bronchoscopy for management of a malignant polypoid obstruction in the Bronchus Intermedius (BI). The lesion was devascularized using the Nd:YAG laser. Mechanical resection was achieved via the 'apple coring' technique using the bevel of the rigid scope. Residual tumor was managed with APC. The RUL orifice was similarly treated. We successfully recanalized the proximal BI to 85%. Stent placement was withheld per patient preference and anatomical constraints.",
            3: "CPT CODING:\n- 31641: Destruction of tumor (Nd:YAG Laser, APC) in Bronchus Intermedius.\n- 31640-XS: Excision of tumor (Rigid Coring) in Right Upper Lobe/Distal BI (distinct technique/site consideration).\nNote: Documentation supports multi-modality approach (Laser vs Coring).",
            4: "Procedure: Rigid Bronch + Laser\nPatient: Jean-Luc Picard\nSteps:\n1. General Anesthesia/Paralytics.\n2. Rigid scope (11mm).\n3. Nd:YAG laser to BI tumor.\n4. Coring with rigid scope bevel.\n5. Removed mass en-bloc.\n6. APC for residual.\n7. RUL debulked similarly.\nPlan: CXR, Oncology consult.",
            5: "rigid bronch case for mr picard... had a big polyp blocking the bi... we tried the snare but it wouldnt grab so we used the laser... then used the rigid scope to core it out like an apple... pulled the whole thing out with suction... cleaned up with apc... opened it up pretty good... patient didn't want a stent so we left it as is... check xray.",
            6: "Rigid bronchoscopy was utilized to treat a complete obstruction of the bronchus intermedius. The polypoid lesion was devascularized with Nd:YAG laser and resected using a rigid coring technique. The RUL orifice was also debulked using APC. We achieved 85% patency proximally. Stent placement was deferred based on patient preference and distal tumor anatomy. The patient will follow up with oncology for systemic therapy.",
            7: "[Indication]\nTumor obstruction Bronchus Intermedius.\n[Anesthesia]\nGeneral Anesthesia (Rigid).\n[Description]\nNd:YAG laser and Rigid Coring used to remove polypoid mass in BI. APC used for residuals. RUL debulked. Patency restored to 85%.\n[Plan]\nCXR. Oncology for systemic therapy.",
            8: "We performed a rigid bronchoscopy on Mr. Picard to remove a large tumor blocking his breathing passage. We used a laser to shrink the tumor and then used the metal tube of the scope to core it out. We removed the main chunk of the tumor and used cautery to clean up the rest. The airway is much more open now. We decided against a stent for now, as he prefers to avoid it if possible.",
            9: "PROCEDURE: Rigid bronchoscopy with endobronchial resection.\nDETAILS: A polypoid lesion in the BI was photocoagulated with Nd:YAG and resected via coring. The RUL was also treated. \nOUTCOME: The airway was recanalized. Stent deployment was deferred."
        }
    }
    return variations

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
    
    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Loop through each original note
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Create 9 variations
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # Randomize Age and Date
            new_age = orig_age + random.randint(-3, 3)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            new_name = record['names'][style_num - 1]
            
            # Inject Text Variation
            note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update Registry Data to match
            if "registry_entry" in note_entry:
                if "patient_demographics" in note_entry["registry_entry"]:
                    # Some notes might have null, so we initialize if needed
                    if note_entry["registry_entry"]["patient_demographics"] is None:
                        note_entry["registry_entry"]["patient_demographics"] = {}
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                note_entry["registry_entry"]["patient_mrn"] = f"SYN_015_{idx}_{style_num}"
            
            # Add Synthetic Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Write output
    output_path = output_dir / OUTPUT_FILE
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_path}")

if __name__ == "__main__":
    main()