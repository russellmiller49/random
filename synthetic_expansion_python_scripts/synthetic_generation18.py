import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_018.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the specified year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns the manually crafted text variations for the notes in bronch_notes_part_018.json.
    Structure: Note_Index (0-3) -> Style_Index (1-9) -> Text
    """
    variations = {
        # Note 0: Rigid bronchoscopy, APC/Cryo/Forceps debulking, Fogarty, Hypoxia events.
        0: {
            1: "Procedure: Rigid Bronchoscopy (12mm) w/ Jet Vent.\nIndication: Airway obstruction.\nActions:\n- Rigid scope inserted. Flex scope passed.\n- Tumor at LC2 carina: 100% LUL / 95% LLL block.\n- Forceps biopsy taken.\n- APC for hemostasis/devascularization.\n- Mechanical debulking w/ rigid forceps & cryo.\n- Fogarty balloon passed LLL; purulence suctioned.\n- Hypoxia (sats 50s) required clot extraction/O2 insufflation.\nResult: Partial recanalization only. Bleeding controlled.\nPlan: ICU. CXR. Palliative Onco consult.",
            2: "OPERATIVE REPORT\n\nPREOPERATIVE DIAGNOSIS: Malignant obstruction of the left mainstem bronchus.\nPROCEDURE: Rigid bronchoscopy with multimodal tumor ablation and debulking.\n\nNARRATIVE: Under general anesthesia, a 12 mm ventilating rigid bronchoscope was introduced. The trachea appeared unremarkable. Significant pathology was identified at the mid-left mainstem extending to the LC2 carina, resulting in complete occlusion of the left upper lobe and subtotal occlusion of the left lower lobe. A combination of argon plasma coagulation (APC) for coagulation and cryotherapy for tissue extraction was utilized. Despite aggressive mechanical debulking and the utilization of a Fogarty balloon catheter to clear distal secretions, anatomic restoration was limited by extensive disease burden. Intraoperatively, the patient suffered transient desaturation necessitating clot evacuation and supplemental oxygen insufflation.\n\nDISPOSITION: The patient was transferred to the Intensive Care Unit for close monitoring of airway patency.",
            3: "Procedure: Therapeutic Bronchoscopy (31641).\nTechnique:\n1. Destruction of tumor: Argon Plasma Coagulation (APC) applied to tumor surface at LC2 carina.\n2. Debulking: Cryoprobe and rigid forceps used to physically remove tumor tissue obstructing LUL and LLL.\n3. Secretion Management: Bronchial lavage (31624 bundled) and Fogarty balloon sweep performed to clear purulent secretions.\n4. Biopsy: Forceps biopsies obtained (bundled with 31641).\nSpecifics: 12mm rigid scope used. Patient required management of significant hypoxia/clot removal during case.",
            4: "Procedure Note\nAttending: [Attending Name]\nResident: [Resident Name]\nProcedure: Rigid Bronch + Debulking\n\nSteps:\n1. Time out. GA induced.\n2. 12mm rigid scope -> distal trachea. Jet vent attached.\n3. Flex scope inserted. Tumor seen at LC2 carina (LUL 100% blocked, LLL 95%).\n4. Biopsies taken.\n5. APC used to burn. Cryo/forceps used to debulk.\n6. Fogarty balloon used in LLL to pull out pus.\n7. Complication: Desat to 50s. Suctioned clots, gave O2. Recovered.\n8. Hemostasis achieved.\n\nPlan: ICU admit.",
            5: "rigid bronch performed today for tumor obstruction anesthesia general used 12mm scope jet vent hooked up. saw massive tumor left side blocking almost everything lul and lll. used forceps to biopsy then apc to stop bleeding and cryo to pull chunks out. tried fogarty balloon in lll got lot of pus out. patient desatted bad down to 50s had to stop and clean out clots and give oxygen but they came back up. couldn't open it all the way too much cancer. stopped bleeding sent to icu for watch thanks.",
            6: "The patient was brought to the operating room and placed under general anesthesia. A 12 mm rigid bronchoscope was inserted. Inspection revealed a large tumor mass at the LC2 carina obstructing the LUL (100%) and LLL (95%). We proceeded with forceps biopsy followed by APC ablation. Cryotherapy was utilized for further debulking. A Fogarty balloon was passed into the LLL to facilitate secretion clearance; purulent material was noted. Intraoperatively, the patient experienced hypoxia requiring clot extraction and oxygen insufflation. The airway could not be fully recanalized due to tumor extent. The scope was removed after hemostasis was confirmed.",
            7: "[Indication]\nAirway obstruction, left lung mass.\n[Anesthesia]\nGeneral, 12mm Rigid Bronchoscope, Jet Ventilation.\n[Description]\nTumor noted at LC2 carina obstructing LUL/LLL. Forceps biopsies taken. APC applied for coagulation. Cryotherapy and rigid forceps used for debulking. Fogarty balloon used to clear LLL secretions. Transient hypoxia treated with suction/O2.\n[Plan]\nICU admission. CXR. Palliative Tx.",
            8: "We initiated the procedure by inducing general anesthesia and inserting a 12 mm ventilating rigid bronchoscope. Upon reaching the distal trachea, jet ventilation was established. A flexible scope was passed through the rigid barrel to visualize the left mainstem, where we encountered extensive tumor infiltration at the secondary carina. This lesion caused total obstruction of the upper lobe and near-total obstruction of the lower lobe. We employed forceps to obtain diagnostic tissue, followed by argon plasma coagulation to devascularize the mass. Subsequent debulking was achieved using cryotherapy and rigid forceps. We also utilized a Fogarty balloon to sweep the lower lobe, which yielded copious purulent secretions. During the intervention, the patient experienced transient severe hypoxia managed by clearing blood clots and administering oxygen.",
            9: "Pre-op: Lung mass with blockage.\nProcedure: Rigid scope insertion. \nActions: \n- Visualized tumor at LC2 carina.\n- Sampled tissue with forceps.\n- Cauterized with APC.\n- Extracted tumor using cryo and forceps.\n- Swept airway with Fogarty balloon.\n- Cleared purulent fluid.\nIssues: Hypoxia observed; clots evacuated.\nOutcome: Hemostasis secured. Partial clearance."
        },
        # Note 1: Rigid, EBUS (4 stations), Debulking (APC/Cryo), Fogarty. LMA then Rigid.
        1: {
            1: "Procedure: Rigid Bronchoscopy + EBUS.\n- LMA placed. EBUS TBNA: 4R, 2R, 7, 4L (Benign).\n- Rigid scope (12mm) inserted.\n- Tumor: Distal LMS (85%), LC2 carina infiltrated.\n- Action: APC ablation, Cryo debulking, Forceps removal.\n- Fogarty balloon: Used in LLL, pus drained.\n- LUL: Proximal opening achieved, distal tumor remains.\n- Complications: None.",
            2: "PROCEDURE PERFORMED: Rigid bronchoscopy with tumor debulking and Endobronchial Ultrasound (EBUS) staging.\nFINDINGS: Initial inspection via LMA revealed an endobronchial tumor obstructing the distal left mainstem (85%). EBUS-guided TBNA was performed at stations 4R, 2R, 7, and 4L; rapid on-site evaluation showed lymphocytes without malignancy. The airway was then secured with a 12 mm rigid bronchoscope. The tumor was devascularized using Argon Plasma Coagulation (APC) and debulked using a 'burn and shave' technique with cryotherapy assistance. A Fogarty balloon catheter was utilized to clear purulent secretions from the left lower lobe. Despite these efforts, distal tumor extension prevented complete recanalization.",
            3: "CPT Codes:\n- 31641: Bronchoscopy with destruction of tumor (APC/Cryo debulking of Left Mainstem/LUL/LLL).\n- 31653: EBUS sampling of 3+ stations (4R, 2R, 7, 4L sampled).\n- 31624: Bronchoscopy with BAL (distinct maneuver for culture of purulent secretions in LLL).\nNarrative: Complex airway management requiring transition from LMA/EBUS to Rigid/Jet Ventilation for therapeutic debulking.",
            4: "Procedure Note\nPatient: [Patient Name]\nAttending: [Attending Name]\n\n1. LMA placed. White light check -> Tumor distal LMS.\n2. EBUS scope in. Sampled 4R, 2R, 7, 4L. ROSE negative.\n3. Switched to 12mm Rigid scope + Jet Vent.\n4. Used APC to burn tumor. Used cryo/forceps to remove tissue.\n5. Fogarty balloon to LLL -> lots of pus -> sent for culture.\n6. Opened proximal LUL, but distal disease persists.\n7. Tolerated well.",
            5: "patient had lung mass causing obstruction. started with lma and ebus scope. biopsied nodes 4r 2r 7 and 4l rose said benign. then switched to rigid scope 12mm. tumor was blocking left mainstem and lobar takeoffs. used apc to burn it and cryo to freeze and pull. used fogarty balloon to clean out the lll got a lot of pus. biopsy taken. could not get it all open because cancer goes too deep. no complications discharge on augmentin.",
            6: "Under general anesthesia, the T190 and subsequently the UC180F EBUS scopes were introduced via LMA. EBUS-TBNA was performed on stations 4R, 2R, 7, and 4L with benign ROSE results. A 12 mm rigid bronchoscope was then inserted. An endobronchial tumor obstructing the distal left mainstem and LC2 carina was identified. We performed APC ablation and cryo-debulking. A Fogarty balloon facilitated drainage of purulent secretions from the LLL; bronchial lavage was collected. Proximal recanalization was achieved, but distal obstruction persisted. The patient remained stable.",
            7: "[Indication]\nLung mass, airway obstruction, staging.\n[Anesthesia]\nGeneral (LMA converted to Rigid).\n[Description]\nEBUS TBNA performed on 4R, 2R, 7, 4L (negative). Rigid bronchoscopy performed for debulking of distal LMS tumor. APC and Cryotherapy utilized. Fogarty balloon used for secretion management. Partial recanalization achieved.\n[Plan]\nPACU. Discharge on antibiotics.",
            8: "The patient was induced, and an LMA was placed. We began with an airway survey using a standard gastroscope, identifying an obstructing lesion in the left mainstem. We then utilized the EBUS scope to sample mediastinal lymph nodes at stations 4R, 2R, 7, and 4L; on-site pathology was negative for malignancy. To address the airway obstruction, we transitioned to a 12 mm rigid bronchoscope with jet ventilation. The tumor was treated with argon plasma coagulation and mechanically debulked using cryotherapy and forceps. We successfully cleared the proximal airway but noted persistent distal disease.",
            9: "Staging and clearance procedure. \nNodes sampled: 4R, 2R, 7, 4L via EBUS. \nTumor addressed: Left mainstem/carina. \nMethods: Cautery (APC) and freezing (Cryo) for tissue extraction. \nClearance: Fogarty catheter used to drain secretions. \nOutcome: Proximal airways opened; distal occlusion remains."
        },
        # Note 2: Therapeutic, Stent (Aero), EBUS (11R), Cryo/APC, Balloon.
        2: {
            1: "Procedure: Therapeutic Bronchoscopy + EBUS + Stent.\n- Airway: 8.5 ETT.\n- Findings: RLL complete obstruction. 11R node enlarged.\n- EBUS: 11R sampled -> Malignant.\n- RLL: Cryoextraction + APC used. Fogarty for debris.\n- Dilation: 8-10mm balloon.\n- Stent: 10x15mm Aero stent placed in RLL. Post-dilated.\n- Result: RLL 85% patent.",
            2: "OPERATIVE SUMMARY: The patient underwent general anesthesia with an 8.5 mm ETT. Initial inspection revealed complete malignant obstruction of the Right Lower Lobe (RLL). EBUS-guided TBNA of station 11R confirmed malignancy. A therapeutic scope was introduced for intervention. The RLL tumor was managed via cryoextraction and Argon Plasma Coagulation (APC). Mechanical dilation was performed using an Elation balloon. To maintain patency, a 10 x 15 mm Aero self-expanding metallic stent was deployed across the stenosis, jailing the superior segment but sparing the basilar segments. Post-deployment dilation confirmed excellent apposition and 85% patency.",
            3: "Billing Codes:\n- 31641: Tumor destruction via APC and Cryo in RLL.\n- 31652: EBUS sampling of 1 station (11R).\n- 31636: Placement of bronchial stent (Aero 10x15mm) in RLL.\nNote: Balloon dilation (31630) is bundled with stent placement/tumor destruction and is not separately reported.",
            4: "Procedure Note\nPatient: [Patient Name]\nProcedure: Bronch + Stent + EBUS\n\nSteps:\n1. 8.5 ETT placed.\n2. EBUS: Station 11R sampled. Positive for cancer.\n3. Switched to therapeutic scope.\n4. RLL tumor treated with APC and Cryo.\n5. Balloon dilation (8-9-10mm).\n6. Stent deployment: Aero 10x15mm in RLL.\n7. Stent ballooned open.\n8. RLL now open ~85%.",
            5: "patient with lung cancer and obstruction. intubated with 8.5 tube. looked with ebus and biopsied node 11r it was positive. then went to fix the rll. used apc and cryo to get the tumor out. ballooned it open. put in a stent aero 10 by 15. looks good now rll is open. no complications extubated in room.",
            6: "General anesthesia was induced with an 8.5 mm ETT. Diagnostic bronchoscopy showed RLL obstruction. EBUS-TBNA of station 11R confirmed malignancy. Therapeutic intervention involved forceps biopsy, cryoextraction, and APC ablation of the RLL tumor. A Fogarty balloon removed debris. The airway was dilated with an Elation balloon. A 10 x 15 mm Aero stent was deployed in the RLL, covering the superior segment but opening the basilar segments. The stent was post-dilated. Final patency was estimated at 85%.",
            7: "[Indication]\nMalignant airway obstruction, progression of disease.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nEBUS TBNA 11R (Malignant). RLL tumor treated with Cryo/APC. Balloon dilation performed. 10x15mm Aero stent placed in RLL. Stent dilated.\n[Plan]\nPACU. Oncology follow-up.",
            8: "The patient was intubated with an 8.5 mm endotracheal tube. We performed EBUS staging, identifying and biopsying a malignant node at station 11R. Switching to a therapeutic bronchoscope, we addressed the complete obstruction of the right lower lobe. The tumor was resected using cryoextraction and cauterized with APC. Following balloon dilation to expand the airway, we deployed a 10 x 15 mm covered metal stent. This successfully re-established patency to the basilar segments.",
            9: "Intervention: Therapeutic scope with stenting.\nTarget: RLL malignancy.\nSampling: Node 11R sampled via EBUS.\nClearance: Tumor extracted via cryo; ablated via APC.\nRestoration: Airway dilated; Aero stent deployed.\nOutcome: RLL patent."
        },
        # Note 3: Nav/Radial EBUS, TBNA/Mini-BAL.
        3: {
            1: "Procedure: Navigational Bronchoscopy (SuperD).\nIndication: LUL Nodule.\nSteps:\n- Inspection: Normal airway.\n- Nav: Catheter to LUL apico-posterior.\n- Confirmation: Radial EBUS (view suboptimal).\n- Sampling: Triple needle, TBNA, Forceps, Brush.\n- ROSE: Suboptimal/Inadequate.\n- Add'l: Mini-BAL performed.\n- Complications: None.",
            2: "PROCEDURE: Electromagnetic Navigation Bronchoscopy (ENB) with Radial EBUS and Biopsy.\nINDICATION: Solitary pulmonary nodule, Left Upper Lobe.\nDETAILS: Following airway inspection, the SuperDimension navigation system was utilized to guide a catheter to the target lesion in the LUL apico-posterior segment. Radial EBUS confirmation was attempted but yielded a suboptimal acoustic window. Despite this, multiple diagnostic passes were made using a triple needle brush, TBNA needle, and biopsy forceps. Rapid On-Site Evaluation (ROSE) was non-diagnostic. A mini-bronchoalveolar lavage (BAL) was performed at the site. The procedure was terminated without complications.",
            3: "Coding Summary:\n- 31629: Bronchoscopy with TBNA (primary biopsy code).\n- 31627: Navigation add-on (SuperDimension used).\n- 31654: Radial EBUS add-on (Peripheral lesion localization).\n- 31624: Bronchoscopy with BAL.\nNote: Fluoroscopy (76000) is bundled.",
            4: "Resident Procedure Note\nPatient: [Patient Name]\nProcedure: ENB + Biopsy\n\n1. Airway inspected (normal).\n2. SuperD catheter navigated to LUL nodule.\n3. REBUS check: suboptimal view.\n4. Biopsies: Needle, Brush, Forceps.\n5. ROSE: No tumor seen.\n6. Mini-BAL done.\n7. Scope out. Stable.",
            5: "patient has a nodule in the left upper lobe. did the navigation bronch today using super d system. went to the spot on the map lul apicoposterior. radial ebus didn't look great but we biopsied anyway. used needle brush and forceps. rose didn't show much. did a wash too. patient did fine no bleeding.",
            6: "The patient underwent general anesthesia. A Q190 bronchoscope revealed normal anatomy. The SuperDimension navigation system was used to advance a catheter to the LUL apico-posterior target. Radial EBUS visualization was suboptimal. Biopsies were obtained using triple needle brush, TBNA needle, and forceps under fluoroscopic guidance. ROSE was negative. A mini-BAL was performed. The patient tolerated the procedure well.",
            7: "[Indication]\nLUL Pulmonary Nodule.\n[Anesthesia]\nGeneral.\n[Description]\nNavigated to LUL target using SuperDimension. Radial EBUS confirmation attempted (suboptimal). Samples taken via TBNA, brush, forceps. Mini-BAL performed.\n[Plan]\nAwait pathology. CXR.",
            8: "We performed a navigational bronchoscopy to assess a nodule in the left upper lobe. Using the SuperDimension system, we navigated to the apico-posterior segment. Although the radial EBUS view was not definitive, we proceeded with sampling based on the virtual target. We utilized a combination of needles, brushes, and forceps to obtain tissue. On-site evaluation was indeterminate. We concluded with a mini-lavage of the area.",
            9: "Exam: Navigational airway inspection.\nTarget: LUL lesion.\nLocalization: Electromagnetic guidance + Radial ultrasound.\nSampling: Needle aspiration, brushing, and tissue avulsion (forceps).\nLavage: Segmental wash performed.\nResult: Samples submitted; immediate read inconclusive."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock base data (name, age, gender) for the 4 notes to replace 'UNKNOWN' fields.
    """
    return [
        # Note 0
        {
            "orig_name": "Arthur Dent", "orig_age": 65, "gender": "Male",
            "names": ["John Smith", "Robert Jones", "Michael Brown", "David Miller", "William Wilson", "Richard Moore", "Joseph Taylor", "Thomas Anderson", "Charles Thomas"]
        },
        # Note 1
        {
            "orig_name": "Ford Prefect", "orig_age": 58, "gender": "Male",
            "names": ["James White", "John Harris", "Robert Martin", "Michael Thompson", "William Garcia", "David Martinez", "Richard Robinson", "Joseph Clark", "Thomas Rodriguez"]
        },
        # Note 2
        {
            "orig_name": "Zaphod Beeblebrox", "orig_age": 72, "gender": "Male",
            "names": ["Mary Lewis", "Patricia Lee", "Linda Walker", "Barbara Hall", "Elizabeth Allen", "Jennifer Young", "Maria Hernandez", "Susan King", "Margaret Wright"]
        },
        # Note 3
        {
            "orig_name": "Trillian Astra", "orig_age": 45, "gender": "Female",
            "names": ["Lisa Lopez", "Nancy Hill", "Karen Scott", "Betty Green", "Helen Adams", "Sandra Baker", "Donna Gonzalez", "Carol Nelson", "Ruth Carter"]
        }
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
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Assign a synthetic MRN
                note_entry["registry_entry"]["patient_mrn"] = f"IP2025_{idx+1}_syn_{style_num}"
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update demographics if the block exists, else create minimal
                if "patient_demographics" not in note_entry["registry_entry"] or note_entry["registry_entry"]["patient_demographics"] is None:
                    note_entry["registry_entry"]["patient_demographics"] = {}
                
                note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                note_entry["registry_entry"]["patient_demographics"]["gender"] = record["gender"]

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
    output_filename = output_dir / "synthetic_bronch_notes_part_018.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()