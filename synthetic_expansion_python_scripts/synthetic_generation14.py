import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_014.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-5) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Robert Martinez (EBUS-TBNA)
            1: "Indication: Staging RUL adenocarcinoma. \nProcedure: EBUS-TBNA.\n- Station 4R: 12mm, 4 passes, Malignant.\n- Station 7: 18mm, 4 passes, Malignant.\n- Station 10R: 8mm, 3 passes, Neg.\n- Station 11R: 6mm, 3 passes, Neg.\nComplications: None.",
            2: "HISTORY: Mr. Martinez, a 66-year-old male with newly diagnosed right upper lobe adenocarcinoma, presented for mediastinal staging. \nPROCEDURE: Moderate sedation was induced. A linear EBUS scope was introduced. A systematic nodal evaluation was performed. Transbronchial needle aspiration (TBNA) was conducted at stations 4R, 7, 10R, and 11R. Rapid On-Site Evaluation (ROSE) confirmed malignancy in stations 4R and 7. \nCONCLUSION: N2 disease confirmed. The patient tolerated the procedure well.",
            3: "Procedure: EBUS-TBNA (CPT 31653).\nTechnique: \n1. Ultrasound evaluation of mediastinal and hilar nodes.\n2. Needle aspiration (22G) of Station 4R, Station 7, Station 10R, and Station 11R (>3 stations sampled).\n3. Cell block preparation and ROSE service utilized for all samples.\nOutcome: Adequate tissue obtained from all 4 sites. Malignancy identified in mediastinum.",
            4: "Procedure Note\nAttending: Dr. X\nResident: Dr. Y\nIndication: Staging RUL CA.\nSteps:\n1. Time out.\n2. Sedation (Versed/Fentanyl).\n3. Airway inspection: Normal.\n4. EBUS Evaluation: Stations 4R, 7, 10R, 11R visualized and sampled.\n5. ROSE: Pos at 4R/7.\n6. Scope removed.\nPlan: Oncology referral.",
            5: "Robert Martinez here for the EBUS staging right upper lobe cancer we gave him midazolam and fentanyl he did fine. Went down looked at the nodes 4R was 12mm sampled it 4 times came back cancer same for station 7 which was bigger 18mm. Then did 10R and 11R those were negative. No bleeding or anything patient woke up ok sending to recovery.",
            6: "Patient Robert Martinez undergoing EBUS-TBNA for RUL adenocarcinoma staging under moderate sedation. Systematic evaluation performed. Station 4R (12mm) sampled x4, ROSE positive. Station 7 (18mm) sampled x4, ROSE positive. Station 10R and 11R sampled x3 each, ROSE negative/adequate. No complications occurred. Plan for oncology follow-up.",
            7: "[Indication]\nRUL Adenocarcinoma, mediastinal staging needed.\n[Anesthesia]\nModerate (Midazolam/Fentanyl).\n[Description]\nEBUS-TBNA performed. Stations 4R and 7 sampled (Positive). Stations 10R and 11R sampled (Negative). All samples adequate.\n[Plan]\nDischarge. Oncology follow up.",
            8: "The patient arrived for scheduled EBUS-TBNA staging of his right upper lobe cancer. We induced moderate sedation and introduced the scope. We proceeded to sample station 4R and station 7, both of which returned positive for malignancy on rapid on-site evaluation. We then sampled 10R and 11R to complete the staging; these were negative. The procedure concluded without any complications.",
            9: "Indication: RUL cancer staging.\nAction: EBUS-TBNA initiated. \nTargeted: Station 4R (aspirated x4), Station 7 (aspirated x4), Station 10R (aspirated x3), Station 11R (aspirated x3).\nFindings: Malignancy detected at 4R and 7. \nOutcome: Patient stable."
        },
        1: { # Angela Davis (Bronchoscopy - Brushing/BAL)
            1: "Indication: LLL infiltrate.\nAnesthesia: Topical lidocaine.\nFindings: LLL basilar segments erythema/edema.\nAction: \n- BAL x3 LLL.\n- Brush x2 LLL.\n- No biopsy.\nComp: None.",
            2: "PROCEDURE: Diagnostic flexible bronchoscopy.\nCLINICAL SUMMARY: Ms. Davis presented for evaluation of a persistent left lower lobe infiltrate. \nFINDINGS: The airway examination revealed moderate mucosal erythema and edema within the basilar segments of the left lower lobe. No endobronchial masses were appreciated.\nINTERVENTION: Bronchoalveolar lavage and bronchial brushings were obtained from the affected segments for microbiologic and cytologic analysis. Transbronchial biopsies were deferred.\nIMPRESSION: Inflammatory changes LLL, ruled out visible endobronchial lesion.",
            3: "Codes Submitted:\n- 31623: Bronchoscopy with brushing (LLL basilar).\n- 31624: Bronchoscopy with bronchoalveolar lavage (LLL basilar).\nJustification: Separate distinct services performed. Brushing performed for cytology; lavage performed for microbiology. No transbronchial biopsy (31628) was performed.",
            4: "Resident Note:\nPatient: Angela Davis.\nProcedure: Flex Bronch.\nSteps:\n1. Local anesthesia (lido).\n2. Scope inserted via mouth.\n3. Inspection: LLL basilar inflammation seen.\n4. BAL performed (150cc total).\n5. Brushings performed x2.\n6. Tolerated well.\nPlan: Await cultures.",
            5: "Note for Angela Davis dob 5/12/1970 we did the bronch today for that LLL infiltrate just used topical numbing spray she was awake. Looked down there LLL basilar segs looked red and swollen but no tumor seen. Did a wash sent for culture and cytology and brushed it twice too. Didnt do biopsies cause she didnt want them. She did fine no issues.",
            6: "Evaluation of LLL infiltrate for Angela Davis. Topical anesthesia used. Inspection revealed erythema and edema in LLL basilar segments. No masses. BAL performed with 50cc aliquots x3. Brushings x2 obtained from the same area. No complications. Procedure time 18 mins.",
            7: "[Indication]\nLLL infiltrate, r/o malignancy vs infection.\n[Anesthesia]\nTopical Lidocaine 4% and 2%.\n[Description]\nScope advanced. LLL basilar inflammation noted. BAL and Brushings collected from LLL. No biopsy performed.\n[Plan]\nDischarge. Follow up culture results.",
            8: "Ms. Davis underwent a flexible bronchoscopy to investigate a left lower lobe infiltrate. We utilized topical anesthesia only. Upon inspection, the left lower lobe basilar segments appeared inflamed with edema, though no discrete mass was visible. We performed a bronchoalveolar lavage and bronchial brushings in this area. She tolerated the procedure well and was discharged shortly after.",
            9: "Indication: Assess LLL infiltrate.\nTechnique: Flexible bronchoscopy.\nObservations: LLL basilar region showed redness and swelling.\nSampling: Lavaged LLL (sent for culture/cyto). Brushed LLL x2.\nStatus: Uncomplicated."
        },
        2: { # James Wilson (EBUS Data Form)
            1: "Indication: Staging.\nProc: EBUS-TBNA.\nNodes:\n- 4R: 10mm, 4 passes, Malignant.\n- 7: 14mm, 4 passes, Malignant.\n- 11R: 7mm, 3 passes, Adequate.\nComp: None.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nINDICATIONS: Mediastinal staging for lung carcinoma.\nFINDINGS: Systematic ultrasound interrogation identified lymphadenopathy at stations 4R, 7, and 11R. Real-time sampling was performed. ROSE confirmed malignancy at stations 4R and 7. Station 11R yielded adequate lymphocytes but was negative for malignancy on preliminary review.\nCONCLUSION: N2 positive disease.",
            3: "Billing Code: 31653 (EBUS-TBNA 3+ stations).\nStations Sampled: \n1. Station 4R\n2. Station 7\n3. Station 11R\nRequirements Met: >3 distinct mediastinal/hilar stations sampled with needle aspiration. ROSE service utilized.",
            4: "Procedure Note\nPatient: James Wilson\nProc: EBUS\nSteps:\n1. Moderate sedation.\n2. EBUS scope passed.\n3. Nodal survey completed.\n4. Sampled 4R, 7, 11R.\n5. Path confirmed cancer in 4R and 7.\n6. Pt stable.\nPlan: Oncology.",
            5: "James Wilson EBUS procedure note. We used moderate sedation he was comfortable. Checked the nodes systematic way. 4R and 7 were positive for cancer on the rapid read. 11R was sampled too looked ok. No complications at all. Saved the images.",
            6: "EBUS-TBNA for James Wilson. Staging indication. Moderate sedation. Systematic N3-N1 exam. Sampled 4R (10mm, positive), 7 (14mm, positive), and 11R (7mm, adequate). Molecular samples sent. No complications recorded.",
            7: "[Indication]\nLung cancer staging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA of stations 4R, 7, 11R. ROSE positive for malignancy at 4R and 7. 11R benign.\n[Plan]\nRefer to Oncology.",
            8: "Mr. Wilson underwent EBUS-TBNA for staging purposes. Under moderate sedation, we identified and sampled nodes at stations 4R, 7, and 11R. Rapid on-site evaluation showed malignant cells in stations 4R and 7. Station 11R was sampled and found adequate but negative. There were no complications.",
            9: "Task: Staging EBUS.\nTargets: 4R, 7, 11R.\nMethod: TBNA with ROSE.\nResults: Malignancy detected in 4R and 7. 11R benign.\nStatus: Patient stable."
        },
        3: { # Thomas Jackson (EBUS Restaging - Station 7)
            1: "Indication: Restaging post-chemo (N2).\nProc: EBUS-TBNA Station 7.\nFindings: Station 7 now 8mm (was 18mm).\nAction: 4 passes. ROSE Neg.\nOther: 4R/4L/10R benign/small, not sampled.\nImpression: Downstaging.",
            2: "HISTORY: Mr. Jackson presented for restaging EBUS following chemotherapy for N2 (Station 7) disease. \nPROCEDURE: Under conscious sedation, the subcarinal station (7) was re-evaluated. The node measured 8mm, significantly reduced from prior imaging. Transbronchial needle aspiration was performed. ROSE was negative for malignancy, demonstrating anthracotic macrophages. \nCONCLUSION: Radiologic and pathologic downstaging of mediastinal disease.",
            3: "CPT: 31652 (EBUS-TBNA 1-2 stations).\nJustification: Only Station 7 was sampled (targeted restaging). Other stations (4R, 4L, 10R) were inspected but not sampled based on benign appearance. \nDocumentation: 4 needle passes obtained from Station 7.",
            4: "Resident Note\nPt: Thomas Jackson\nProc: Restaging EBUS\n1. Sedation started.\n2. Examined mediastinum.\n3. Station 7 (target) sampled x4.\n4. ROSE negative.\n5. Other nodes looked benign.\nPlan: Surgical consult.",
            5: "Thomas Jackson here for restaging he had chemo for that station 7 node. It looks smaller now only 8mm. We sampled it 4 times and the pathologist said no cancer cells seen just pigment. Didn't sample the others they looked tiny. Good response to chemo I think.",
            6: "Restaging EBUS for Thomas Jackson. Conscious sedation. Station 7 reassessed; size reduced to 8mm. 4 passes TBNA performed. ROSE negative. Stations 4R, 4L, 10R surveyed and deemed benign/small, not sampled. No complications.",
            7: "[Indication]\nRestaging mediastinum post-chemo (Station 7).\n[Anesthesia]\nConscious Sedation.\n[Description]\nStation 7 sampled x4. ROSE negative. 4R, 4L, 10R inspected but not sampled.\n[Plan]\nRefer for surgery.",
            8: "Mr. Jackson underwent an EBUS procedure to restage his mediastinal disease after chemotherapy. We focused on station 7, which had previously been positive. It was smaller in size, and sampling revealed no malignant cells. We inspected other stations but did not feel sampling was necessary due to their benign appearance.",
            9: "Indication: Re-evaluation of N2 disease.\nAction: Aspiration of Station 7.\nFindings: Node regression noted. Cytology negative.\nSurvey: 4R, 4L, 10R inspected, no sampling required.\nResult: Treatment response confirmed."
        },
        4: { # Richard Brown (Complex: EBUS + RML Stent + LUL Nav)
            1: "Indication: Mass, Stenosis, Nodule.\nAnesth: GA/ETT.\n1. EBUS: 4R, 10R, 11R sampled (Malignant).\n2. RML: Tumor debulked (APC/Forceps). Stent placed (12x30mm).\n3. LUL: Nav bronch to 16mm nodule. Biopsy x3.\nComp: Bleeding controlled. Transient hypoxia.\nPlan: ICU obs.",
            2: "OPERATIVE REPORT: Mr. Brown underwent a multimodal bronchoscopic procedure. \n1) EBUS Staging: Stations 4R, 10R, and 11R were sampled, confirming malignancy. Station 7 was inaccessible. \n2) Therapeutic Bronchoscopy: The RML bronchus was 80% occluded by tumor. This was debulked using forceps and APC, followed by placement of a 12x30mm metallic stent. \n3) Navigation: Electromagnetic navigation guided biopsy of a LUL apical-posterior nodule.\nIMPRESSION: Advanced malignancy with airway palliation and nodule sampling.",
            3: "Billing Summary:\n- 31653: EBUS 3+ stations (4R, 10R, 11R).\n- 31641: Tumor destruction/debulking RML.\n- 31636: Stent placement RML.\n- 31627: Navigational Bronchoscopy (LUL nodule).\n- 31654: Radial EBUS (tool confirmation).\n- 31628: Transbronchial biopsy (LUL).\nNote: Distinct lesions and services.",
            4: "Procedure Note\nPt: Richard Brown\n1. GA induced.\n2. EBUS: Sampled 4R, 10R, 11R (Pos).\n3. RML Tumor: Debulked and stented (Metal 12x30).\n4. LUL Nodule: Navigated and biopsied.\nEvents: Bleeding in RML (stopped w/ APC), desat during stent (fixed).\nPlan: Admit.",
            5: "Richard Brown complex case today. Did EBUS first found cancer in 4R 10R 11R. Then fixed the RML stenosis debulked the tumor and put a stent in. Then went for that LUL nodule using the navigation system and biopsied it. Had some bleeding and sats dropped a bit but he's stable now.",
            6: "Richard Brown. GA/ETT. 1) EBUS: 4R, 10R, 11R sampled (positive). 2) RML: Exophytic tumor debulked (forceps/APC), 12x30mm stent placed. 3) LUL: EM navigation to 16mm nodule, radial EBUS confirmation, TBBx x3. Complications: Moderate bleeding RML, transient hypoxia.",
            7: "[Indication]\nMediastinal LAD, RML stenosis, LUL nodule.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS staging performed (3 stations). RML tumor debulked and stented. LUL nodule biopsied via navigation.\n[Plan]\nICU observation.",
            8: "This was a complex case for Mr. Brown involving staging, debulking, and biopsy. We started with EBUS, confirming malignancy in multiple stations. We then addressed the RML obstruction by debulking the tumor and placing a stent to keep the airway open. Finally, we used electromagnetic navigation to locate and biopsy a peripheral nodule in the left upper lobe.",
            9: "Indication: Complex airway/lung disease.\nAction 1: Staged mediastinum (EBUS 4R, 10R, 11R).\nAction 2: Recanalized RML (Debulk/Stent).\nAction 3: Sampled LUL nodule (Navigation/Biopsy).\nOutcome: Successful completion."
        },
        5: { # Patricia Anderson (EBUS + RUL Tumor Biopsy)
            1: "Indication: RUL mass + LAD.\nAnesth: GA/ETT.\n1. EBUS: 2R, 4R, 7, 10R sampled. 4R Pos.\n2. RUL Mass: Forceps Bx x6. Bleeding controlled.\nComp: Hypoxia (88%), bleeding.\nPlan: Path pending.",
            2: "PROCEDURE: Bronchoscopy with EBUS staging and endobronchial biopsy.\nFINDINGS: EBUS evaluation of stations 2R, 4R, 7, and 10R was performed. Station 4R was positive for malignancy. Direct inspection revealed an endobronchial mass in the RUL causing obstruction. Multiple biopsies were taken from this lesion.\nCOMPLICATIONS: Intraprocedural hemorrhage managed with cold saline and epinephrine. Transient desaturation.",
            3: "CPT Codes:\n- 31653: EBUS-TBNA 3+ stations (2R, 4R, 7, 10R).\n- 31625: Endobronchial biopsy (RUL mass).\nRationale: Staging of mediastinum performed separately from biopsy of visible endobronchial tumor. \nNote: Bleeding management is incidental/bundled.",
            4: "Resident Note\nPt: Patricia Anderson\n1. ETT placed.\n2. EBUS: 4 stations sampled. 4R malignant.\n3. Bronchoscopy: RUL mass seen.\n4. Biopsied mass x6.\n5. Bleeding occurred, stopped w/ epi.\nPlan: Wait for path.",
            5: "Patricia Anderson procedure note. Did the EBUS first checked 2R 4R 7 and 10R. 4R looked bad and was positive. Then saw the tumor in the RUL airway and biopsied it a bunch of times. It bled a bit but we stopped it. She desatted for a minute but came back up.",
            6: "Patricia Anderson. GA/ETT. EBUS-TBNA performed at 2R, 4R, 7, 10R. 4R positive. RUL endobronchial mass biopsied x6. Moderate bleeding controlled with epinephrine. Transient hypoxia resolved. Plan: Oncology referral.",
            7: "[Indication]\nRUL mass, mediastinal adenopathy.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS staging (4 stations). Endobronchial biopsy of RUL mass. Bleeding controlled.\n[Plan]\nPathology review.",
            8: "Ms. Anderson underwent a bronchoscopy under general anesthesia. We first performed EBUS staging, sampling four stations, with station 4R returning positive for cancer. We then turned our attention to the RUL endobronchial mass and obtained multiple biopsies. There was some bleeding and a brief drop in oxygen levels, but both were managed successfully.",
            9: "Indication: Airway mass and LAD.\nAction 1: Interrogated mediastinum (EBUS).\nAction 2: Sampled RUL tumor (Forceps).\nEvents: Hemorrhage controlled. Hypoxia corrected.\nStatus: Recovery."
        }
    }
    return variations

def get_base_data_mocks():
    # Names and ages to match the flow (mocking extraction from a real source)
    return [
        {"idx": 0, "orig_name": "Robert Martinez", "orig_age": 66, "names": ["John Smith", "David Johnson", "Michael Williams", "James Brown", "Robert Jones", "William Garcia", "Richard Miller", "Thomas Davis", "Charles Rodriguez"]},
        {"idx": 1, "orig_name": "Angela Davis", "orig_age": 65, "names": ["Mary Wilson", "Patricia Martinez", "Jennifer Anderson", "Linda Taylor", "Elizabeth Thomas", "Barbara Hernandez", "Susan Moore", "Jessica Martin", "Sarah Jackson"]},
        {"idx": 2, "orig_name": "James Wilson", "orig_age": 65, "names": ["Joseph White", "Thomas Lopez", "Charles Lee", "Christopher Gonzalez", "Daniel Harris", "Matthew Clark", "Anthony Lewis", "Mark Robinson", "Donald Walker"]},
        {"idx": 3, "orig_name": "Thomas Jackson", "orig_age": 65, "names": ["Paul Perez", "Steven Hall", "Andrew Young", "Kenneth Allen", "Joshua Sanchez", "Kevin Wright", "Brian King", "George Scott", "Edward Green"]},
        {"idx": 4, "orig_name": "Richard Brown", "orig_age": 65, "names": ["Ronald Baker", "Timothy Adams", "Jason Nelson", "Jeffrey Hill", "Ryan Ramirez", "Jacob Campbell", "Gary Mitchell", "Nicholas Roberts", "Eric Carter"]},
        {"idx": 5, "orig_name": "Patricia Anderson", "orig_age": 65, "names": ["Karen Phillips", "Nancy Evans", "Lisa Turner", "Betty Torres", "Margaret Parker", "Sandra Collins", "Ashley Edwards", "Kimberly Stewart", "Donna Flores"]},
    ]

def main():
    # Load original data
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
    
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Iterate through the 9 styles
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # Variations
            new_age = orig_age + random.randint(-3, 3)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            new_name = record['names'][style_num - 1]
            
            # Apply changes
            note_entry["note_text"] = variations_text[idx][style_num]
            
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                if "patient_mrn" in note_entry["registry_entry"]:
                    # Create a synthetic MRN
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"

            # Add synthetic metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON
    output_filename = output_dir / "synthetic_blvr_notes_part_014.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()