import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_007.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILENAME = "synthetic_notes_part_007.json"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Defines the base patient data found in part_007 and provides 
    9 mock names for the synthetic variations.
    """
    return [
        {
            "idx": 0, 
            "orig_name": "Antonio M. Rodriguez", 
            "orig_age": 64, 
            "names": ["Carlos Gomez", "Manuel Ortiz", "Javier Hernandez", "Luis R. Martinez", "Miguel Torres", "Roberto Sanchez", "Alejandro Diaz", "Ricardo Morales", "Jose Castillo"]
        },
        {
            "idx": 1, 
            "orig_name": "William Harris", 
            "orig_age": 68, 
            "names": ["James T. Wilson", "Robert Clark", "Thomas Lewis", "George Walker", "Edward Hall", "Charles Allen", "Frank Young", "Henry King", "Walter Wright"]
        },
        {
            "idx": 2, 
            "orig_name": "Lisa Morgan", 
            "orig_age": 65, 
            "names": ["Karen Brooks", "Susan Bennett", "Linda Gray", "Donna James", "Sandra Watson", "Betty Hughes", "Dorothy Price", "Helen Sanders", "Margaret Ross"]
        },
        {
            "idx": 3, 
            "orig_name": "Tyrone Jackson", 
            "orig_age": 68, 
            "names": ["Marcus Washington", "Darnell Jefferson", "Terrence Robinson", "Andre Banks", "Darius Coleman", "Jamal Hayes", "Malik Jenkins", "Xavier Perry", "Kendrick Bryant"]
        },
        {
            "idx": 4, 
            "orig_name": "Patricia Louise Henderson", 
            "orig_age": 61, 
            "names": ["Deborah A. Collins", "Barbara J. Stewart", "Ruth M. Sanchez", "Sharon L. Morris", "Michelle K. Rogers", "Laura P. Reed", "Sarah T. Cook", "Kimberly D. Morgan", "Cynthia B. Bell"]
        }
    ]

def get_variations():
    """
    Returns a dictionary of stylistic variations for each note index.
    Structure: Note_Index -> Style_Index -> Text
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
        0: { # Antonio Rodriguez (Robotic Bronch + EBUS + TBBx + BAL)
            1: "Procedure: Robotic bronchoscopy, radial EBUS, TBBx, BAL.\nIndication: Bilateral nodules, largest RLL 2.6cm.\nAction:\n- ETT/GA.\n- Ion nav to RLL posterior nodule.\n- REBUS: Concentric lesion confirmed.\n- Biopsy: Forceps x7, Brush x3.\n- BAL RLL performed.\nFindings: Lesion sampled. No bleeding.\nPlan: CXR 2 hours. Clinic 2 wks.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the operating suite for elective robotic-assisted bronchoscopy. Following induction of general anesthesia, the Ion endoluminal system was deployed. Navigation was established to the target lesion in the right lower lobe posterior segment, identified as a 2.6 cm FDG-avid nodule. Radial endobronchial ultrasound (REBUS) interrogation revealed a concentric echogenic signature, confirming tool-in-lesion status. Extensive sampling was performed via transbronchial forceps biopsy and cytology brushing. Additionally, a bronchoalveolar lavage was conducted for microbiological assessment. The patient tolerated the procedure without physiological derangement.",
            3: "Procedures Performed/Justification:\n1. 31627 (Navigational Bronchoscopy): Required for localization of peripheral RLL nodule not visible via standard bronchoscopy. Planning and real-time guidance utilized.\n2. 31654 (Peripheral EBUS): Radial probe used to confirm lesion concentricity and verify tool placement prior to biopsy.\n3. 31628 (Transbronchial Biopsy): Primary diagnostic maneuver; 7 specimens obtained from single site (RLL).\n4. 31624 (BAL): Separate diagnostic wash performed for culture/cytology.\nEquipment: Intuitive Ion, 20MHz radial probe.",
            4: "Resident Procedure Note\nPatient: Carlos Gomez\nAttending: Dr. Anderson\nPre-op Dx: Lung nodules.\nSteps:\n1. Time out. GA induced. 8.0 ETT.\n2. Ion robot docked. Registration error 1.5mm.\n3. Navigated to RLL target.\n4. Radial EBUS showed concentric view.\n5. Taken: 7 biopsies, 3 brushes, 1 BAL.\n6. ROSE: Atypical cells.\n7. Extubated stable.\nPlan: CXR, discharge if negative.",
            5: "pt here for robotic bronchoscopy right lower lobe nodule uh we used general anesthesia intubated. navigated to the rll posterior segment with the ion system looked good on the screen radial ebus showed the lesion concentric so we biopsied it. took about seven bites and some brushes also did a wash. rose said maybe cancer. no bleeding really patient woke up fine sent to recovery check a chest xray thanks.",
            6: "The patient was brought to the OR and placed under general anesthesia with an 8.0 ETT. A time-out was performed. We utilized the Intuitive Ion robotic platform to navigate to a 2.6 cm nodule in the RLL posterior segment. Navigation was successful with a fiducial error of 1.5mm. We inserted a radial EBUS probe which demonstrated a concentric echogenic pattern consistent with a solid lesion. We then performed 7 transbronchial biopsies and 3 brushes. A BAL was also collected. Rapid on-site evaluation suggested atypical cells. There were no complications. The patient was extubated and transferred to PACU.",
            7: "[Indication]\n64M with multiple lung nodules, largest RLL 2.6cm, need tissue diagnosis.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon robotic navigation used to reach RLL posterior segment target. Radial EBUS confirmed concentric lesion. Transbronchial biopsies (x7) and brushings (x3) obtained. BAL performed. Hemostasis achieved.\n[Plan]\nCXR to rule out pneumothorax. Follow-up in 2 weeks.",
            8: "Mr. Morales presented for evaluation of bilateral pulmonary nodules. We proceeded with a robotic-assisted bronchoscopy targeting the largest lesion in the right lower lobe. Under general anesthesia, the scope was successfully navigated to the target in the posterior segment. Confirmation was achieved using radial EBUS, which showed a clear concentric view of the 24mm lesion. We then obtained seven biopsy samples and three cytology brushings, followed by a bronchoalveolar lavage. The preliminary on-site pathology review showed atypical cells. The patient tolerated the procedure well with minimal blood loss.",
            9: "Operation: Robotic navigational bronchoscopy with peripheral interrogation.\nContext: Multi-focal pulmonary nodules.\nAction: The robotic catheter was steered to the RLL posterior segment. Radial ultrasound verified the target's location. The lesion was sampled via forceps and brushing. A lavage was also instilled and retrieved.\nOutcome: Satisfactory tissue acquisition. No adverse events."
        },
        1: { # William Harris (LUL BLVR)
            1: "Indication: Severe emphysema, LUL target.\nProc: LUL Valve Placement.\nSteps:\n- GA, 8.5 ETT.\n- Chartis LUL: CV Negative (flow to zero).\n- 3 Zephyr valves placed: LB1+2, LB1+2c, LB3.\n- Total occlusion confirmed.\nResult: LUL atelectasis initiated. No leaks.\nPlan: Admit. Pneumothorax precautions.",
            2: "PROCEDURE NOTE: The patient, presenting with severe heterogeneous emphysema, underwent therapeutic bronchoscopy for lung volume reduction. Following intubation, the left upper lobe (LUL) was isolated. A Chartis collateral ventilation assessment was performed, demonstrating a 'CV Negative' status (cessation of expiratory flow), confirming fissure integrity. Based on these findings, three Zephyr endobronchial valves were systematically deployed in the apicoposterior, anterior, and superior segments. Bronchoscopic verification demonstrated complete lobar occlusion with no paravalvular leak. The patient remained stable throughout.",
            3: "Service: Bronchoscopic Lung Volume Reduction (BLVR).\nCodes:\n- 31647: Placement of valves in initial lobe (LUL).\n- 31634: Balloon occlusion/Chartis assessment (Bundled but performed).\nJustification: CT showed intact fissure. Chartis confirmed absence of collateral ventilation (required for valve success). Three (3) valves utilized to occlude LB1+2, LB1+2c, and LB3. Procedure medically necessary for severe refractory emphysema.",
            4: "Procedure Note - Fellow\nPatient: Robert Clark\nProcedure: LUL Valves\nStaff: Dr. Lee\n1. Intubated 8.5 ETT.\n2. Bronch to LUL.\n3. Chartis: Flow went to zero (CV Negative).\n4. Sized and placed 3 Zephyr valves in LUL.\n5. Checked for leaks - none.\n6. Extubated.\nPlan: Observe for pneumo x3 days.",
            5: "Mr Harris here for the valve procedure severe emphysema left upper lobe. We put him to sleep tube in. Checked the LUL with the chartis balloon it stopped flowing so no collateral ventilation good to go. Put in three zephyr valves total one in the apicoposterior one anterior one superior. They look seated well no air getting through. Patient woke up fine no issues sending to floor for monitoring.",
            6: "Endobronchial valve placement was performed on a 68-year-old male with severe emphysema. General anesthesia was induced. The left upper lobe was assessed for collateral ventilation using the Chartis system, which showed no collateral ventilation (CV Negative). Subsequently, three Zephyr valves were deployed into the LB1+2, LB1+2c, and LB3 segmental bronchi. Visual inspection confirmed appropriate expansion and seating of the valves with complete occlusion of the lobar orifice. There were no immediate complications.",
            7: "[Indication]\nSevere heterogeneous emphysema, target LUL, intact fissures.\n[Anesthesia]\nGeneral, 8.5 ETT.\n[Description]\nChartis assessment LUL: Negative for collateral ventilation. Three Zephyr valves deployed (LB1+2, LB1+2c, LB3). Complete occlusion achieved. Valves functioning normally.\n[Plan]\nAdmit to monitored bed. Serial CXRs to monitor for pneumothorax.",
            8: "We performed an elective lung volume reduction for Mr. Allen today. After placing the breathing tube, we navigated to the left upper lobe. The Chartis balloon test confirmed that there was no airflow between the lobes, making him a good candidate. We then proceeded to place three valves in the upper lobe segments. We verified that each valve was sitting correctly and that the airway was fully blocked. He tolerated the procedure well and is now recovering.",
            9: "Procedure: Insertion of endobronchial valves, left upper lobe.\nReason: Advanced emphysema.\nMethod: The LUL was isolated. Collateral ventilation was ruled out via balloon occlusion. Three Zephyr valves were implanted in the target segments. Complete lobar obstruction was verified visually.\nResult: No immediate complications. Patient extubated."
        },
        2: { # Lisa Morgan (Tracheal/Bronchial Stenosis)
            1: "Dx: GPA with tracheal/bronchial stenosis.\nProc: Bronchoscopy, radial cuts, balloon dilation.\nAction:\n- 5cm tracheal stenosis: Dilated 12-15mm.\n- RLL/LUL strictures: Radial cuts (electrocautery), then balloon dilation (6-8mm).\n- Airways recanalized.\nResult: Patency improved. No bleeding.\nPlan: PACU.",
            2: "OPERATIVE REPORT: The patient, with a history of Granulomatosis with Polyangiitis, presented with complex multilevel airway stenosis. Under general anesthesia via LMA, a flexible bronchoscope was introduced. A 5cm circumferential tracheal stenosis was identified and treated via serial balloon dilation (CRE 12-15mm). Further inspection revealed web-like stenoses in the RLL and Lingula. These were managed with a hybrid approach utilizing radial electrocautery incisions followed by balloon dilation to 8mm. Excellent anatomic restoration of the airway caliber was achieved without hemorrhagic complication.",
            3: "CPT Coding Rationale:\n- 31641: Therapeutic bronchoscopy with destruction of tumor or relief of stenosis. Justified by use of electrocautery knife ('radial knife incisions') to cut band-like strictures in RLL and Lingula.\nNote: Balloon dilation (31630) was performed but is bundled into 31641 when performed at the same session/site. The primary service is the relief of stenosis via multiple modalities.",
            4: "Resident Note\nPatient: Linda Gray\nProcedure: Airway Dilation/Cuts\nIndication: GPA Stenosis\nSteps:\n1. LMA placed.\n2. Saw long tracheal stenosis -> Dilated w/ balloon up to 15mm.\n3. Saw pinhole stenosis in RLL/Lingula.\n4. Used elec-knife to cut the webs.\n5. Dilated those segments w/ balloon.\n6. Airways open now.\nComplications: None.",
            5: "Lisa morgan here for airway stenosis she has wegeners granulomatosis. We put in an lma and went down with the scope. Trachea was tight so we ballooned it open. Then the right lower lobe and lingula were basically shut so we used the electrocautery knife to make cuts and then ballooned them too. Opened up nicely no bleeding. Patient woke up fine going to pacu.",
            6: "Flexible bronchoscopy with radial knife incisions and balloon dilatation was performed. The patient has tracheal and bronchial stenosis secondary to Granulomatosis with polyangiitis. Under general anesthesia with an LMA, a long segment tracheal stenosis was visualized and dilated using 12, 13.5, and 15mm balloons. Web-like strictures in the RLL and Lingula were then addressed. An electrocautery knife was used to make radial incisions in the strictures, followed by balloon dilation using 6-8mm balloons. Near complete recanalization was achieved.",
            7: "[Indication]\nTracheal and bronchial stenosis (GPA).\n[Anesthesia]\nGeneral, LMA.\n[Description]\nTracheal stenosis (5cm long) dilated with CRE balloons (12-15mm). Bronchial strictures (RLL, Lingula) treated with radial electrocautery incisions and subsequent balloon dilation. Airway patency restored.\n[Plan]\nPACU recovery. PRN follow-up.",
            8: "Ms. Hughes underwent a therapeutic bronchoscopy to treat her airway narrowing caused by her autoimmune condition. We found significant narrowing in her windpipe and several branches of her lungs. We first used a balloon to stretch open the main windpipe. For the smaller branches in the right and left lungs, we used a special heated knife to carefully cut the scar tissue before stretching them open with a smaller balloon. The airways looked much more open by the end of the procedure.",
            9: "Procedure: Bronchoscopic recanalization of airway stenosis.\nEtiology: Granulomatosis with polyangiitis.\nTechnique: The tracheal narrowing was expanded using hydraulic balloons. Complex strictures in the lobar bronchi were incised using electrosurgery and subsequently expanded. \nOutcome: Luminal diameter significantly augmented. Hemostasis maintained."
        },
        3: { # Tyrone Jackson (RUL Mass + EBUS Staging)
            1: "Indication: 3.2cm RUL mass + adenopathy.\nProc: EBUS + Ion Nav Bronch.\nEBUS: Stations 4R, 7, 10R sampled. All positive for SqCC.\nNav Bronch: RUL mass. REBUS concentric. Biopsy x7.\nDx: Squamous Cell Ca, Stage IIIA.\nPlan: Oncology referral.",
            2: "OPERATIVE SUMMARY: This 68-year-old male presented for diagnosis and staging of a right upper lobe mass. EBUS-TBNA was performed initially, sampling stations 4R, 7, and 10R. Rapid on-site evaluation (ROSE) confirmed squamous cell carcinoma in all nodal stations. Subsequently, robotic-assisted navigation (Ion) was utilized to localize the peripheral RLL mass. Radial EBUS confirmed lesion position. Transbronchial biopsies yielded tissue consistent with the nodal findings. The patient has confirmed N2 disease, determining a clinical stage of at least IIIA.",
            3: "Coding Breakdown:\n- 31653: EBUS sampling of 3+ stations (4R, 7, 10R).\n- 31627: Computer-assisted navigation (Add-on) for RUL mass.\n- 31654: Peripheral EBUS (Add-on) for RUL mass confirmation.\n- 31628: Transbronchial lung biopsy, single lobe (RUL).\nMedical Necessity: Staging of lung cancer and diagnosis of primary lesion.",
            4: "Procedure Note\nPatient: Andre Banks\nProcedure: EBUS + Robotic Bronch\n1. EBUS first. Stuck 4R, 7, 10R. All positive for Squamous on ROSE.\n2. Switched to Ion robot.\n3. Navigated to RUL mass.\n4. Confirmed with radial probe.\n5. Took 7 biopsies.\n6. ROSE confirmed Squamous.\nImpression: Stage IIIA lung cancer.",
            5: "Mr Jackson for staging and biopsy he has a rul mass. we did the ebus first hit the lymph nodes 4r 7 and 10r dr park said they were all cancer squamous cell. then we used the robot to go out to the mass in the rul. radial ebus showed it nicely. grabbed some biopsies and brushes. looks like stage 3a so hes gonna need chemo and radiation not surgery. no complications.",
            6: "EBUS-TBNA and robotic navigational bronchoscopy were performed. EBUS was used to sample mediastinal and hilar lymph nodes at stations 4R, 7, and 10R. Cytology was positive for squamous cell carcinoma in all stations. The Ion robotic system was then used to navigate to the 3.2cm RUL mass. Radial EBUS confirmed the target. Forceps biopsies and brushings were obtained, which also showed squamous cell carcinoma. The patient tolerated the procedure well.",
            7: "[Indication]\nRUL mass and PET-positive lymphadenopathy.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS-TBNA of stations 4R, 7, 10R performed; all positive for malignancy. Ion robotic navigation to RUL mass performed. REBUS confirmation. Transbronchial biopsies obtained.\n[Plan]\nRefer to Medical Oncology/Radiation Oncology for Stage IIIA Squamous Cell Carcinoma.",
            8: "We brought Mr. Jenkins in to biopsy a mass in his right lung and check his lymph nodes. We started with the ultrasound scope to check the nodes in the center of his chest. Unfortunately, the samples from three different areas all showed cancer. We then used the robotic system to navigate out to the main mass in the lung and took samples from there as well, which matched the lymph nodes. This confirms the cancer has spread to the lymph nodes, so we will proceed with chemotherapy and radiation rather than surgery.",
            9: "Procedure: Combined endobronchial ultrasound staging and robotic peripheral sampling.\nFindings: Nodal stations 4R, 7, and 10R were aspirated and found to harbor malignant cells (Squamous). The primary RUL lesion was localized via robotic guidance and sampled.\nDiagnosis: Stage IIIA Squamous Cell Carcinoma."
        },
        4: { # Patricia Henderson (EBUS Staging)
            1: "Indication: RUL nodule, mediastinal adenopathy.\nProc: EBUS-TBNA.\nNodes Sampled: 7, 4R, 10R, 11R.\nResults:\n- 7, 4R, 10R: Positive for Adenocarcinoma.\n- 11R: Benign.\nDx: Stage IIIC (N3 disease).\nPlan: Oncology for systemic therapy.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nCLINICAL CONTEXT: 61F with RUL adenocarcinoma presenting for mediastinal staging. \nFINDINGS: Systematic EBUS survey identified adenopathy. FNA was performed at stations 7 (subcarinal), 4R (paratracheal), 10R (hilar), and 11R (interlobar). Rapid on-site evaluation confirmed metastatic adenocarcinoma in stations 7, 4R, and 10R. Station 11R was benign. The presence of contralateral or bulky N2/N3 disease (context dependent) confirms advanced stage IIIC.",
            3: "Code: 31653 (EBUS sampling 3 or more stations).\nStations Sampled: 4 distinct stations (4R, 7, 10R, 11R).\nPathology: Malignancy identified in 3 stations.\nMedical Necessity: Staging of known lung adenocarcinoma to determine surgical candidacy (ruled out due to N3 disease).",
            4: "Resident Note\nPatient: Sharon Morris\nProcedure: EBUS\nAttending: Dr. Turner\n1. Scope down. Examined airways - clear.\n2. EBUS'd station 7, 4R, 10R, 11R.\n3. ROSE said cancer in 7, 4R, 10R.\n4. 11R was negative.\n5. No complications.\nPlan: Consult Med Onc. Not a surgical candidate.",
            5: "Patricia Henderson here for EBUS staging. She has a lung nodule and swollen nodes. We sampled station 7 4R 10R and 11R. The pathologist in the room said 7 4R and 10R were all cancer adenocarcinoma. 11R was just reactive. So she has stage 3 disease extensive. We will send for molecular testing and get her to oncology asap.",
            6: "Endobronchial ultrasound-guided transbronchial needle aspiration was performed for mediastinal staging. The patient has a known RUL adenocarcinoma. Lymph node stations 7, 4R, 10R, and 11R were visualized and sampled. Rapid on-site evaluation confirmed metastatic adenocarcinoma in stations 7, 4R, and 10R. Station 11R showed benign lymphocytes. No complications occurred. The findings are consistent with Stage IIIC disease.",
            7: "[Indication]\nRUL Adenocarcinoma, staging required.\n[Anesthesia]\nGeneral (Tracheostomy/Deep Sedation context).\n[Description]\nEBUS-TBNA performed on stations 7, 4R, 10R, 11R. Malignancy confirmed in 7, 4R, 10R via ROSE. 11R benign.\n[Plan]\nMedical Oncology consult. Molecular testing pending.",
            8: "Mrs. Cook underwent an EBUS procedure today to see if her lung cancer had spread to her lymph nodes. We used the ultrasound scope to guide a small needle into four different lymph node areas in her chest. Unfortunately, three of these areas showed cancer cells. This gives us important information about the stage of her disease, which is more advanced than we hoped. We are sending the samples for genetic testing to help the oncologists pick the best drug treatment for her.",
            9: "Procedure: Mediastinal staging via EBUS-TBNA.\nTarget: Stations 7, 4R, 10R, 11R.\nAction: Needle aspiration performed under sonographic guidance.\nAnalysis: Malignant cells detected in the subcarinal, right paratracheal, and right hilar stations. The interlobar station was benign.\nConclusion: Advanced nodal involvement (N3/Stage IIIC)."
        }
    }
    return variations

def main():
    # Load original data
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return

    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through each original note
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        
        # Generate 9 variations
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # Randomize Age (+/- 2 years)
            new_age = record['orig_age'] + random.randint(-2, 2)
            
            # Randomize Date (Year 2025)
            rand_date = generate_random_date(2025, 2025).strftime("%Y-%m-%d")
            
            # New Name
            new_name = record['names'][style_num - 1]
            
            # Update content
            # 1. Update text with the specific variation style
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # 2. Update Registry Entry
            if "registry_entry" in note_entry:
                note_entry["registry_entry"]["patient_age"] = new_age
                note_entry["registry_entry"]["procedure_date"] = rand_date
                # Append suffix to MRN to ensure uniqueness
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            
            # 3. Add Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Save output
    output_path = output_dir / OUTPUT_FILENAME
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_path}")

if __name__ == "__main__":
    main()