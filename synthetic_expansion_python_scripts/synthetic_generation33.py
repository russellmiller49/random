import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_033.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILENAME = "synthetic_expansions_part_033.json"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock data for the patients corresponding to the 10 notes in Part 033.
    Includes original names (if known) or placeholders, original ages, and lists of 
    synthetic names for the variations.
    """
    return [
        {
            "idx": 0, "orig_name": "Lisa Morgan", "orig_age": 45, # Age estimated based on GPA diagnosis, typically 40-60
            "names": ["Sarah Connor", "Ellen Ripley", "Leia Organa", "Dana Scully", "Kathryn Janeway", "Laura Roslin", "Buffy Summers", "Veronica Mars", "Olivia Dunham"]
        },
        {
            "idx": 1, "orig_name": "Tyrone Jackson", "orig_age": 68, 
            "names": ["James Bond", "Jason Bourne", "Jack Bauer", "Ethan Hunt", "John Wick", "Harry Potter", "Frodo Baggins", "Luke Skywalker", "Han Solo"]
        },
        {
            "idx": 2, "orig_name": "Dorothy Mae Russell", "orig_age": 80, 
            "names": ["Rose Nylund", "Blanche Devereaux", "Dorothy Zbornak", "Sophia Petrillo", "Edith Bunker", "Maude Findlay", "Thelma Dickinson", "Louise Sawyer", "Evelyn Couch"]
        },
        {
            "idx": 3, "orig_name": "Robert E Mills", "orig_age": 70, # Age estimated
            "names": ["Walter White", "Jesse Pinkman", "Saul Goodman", "Mike Ehrmantraut", "Gustavo Fring", "Hank Schrader", "Skyler White", "Marie Schrader", "Ted Beneke"]
        },
        {
            "idx": 4, "orig_name": "Sarah Martinez", "orig_age": 55, # Age estimated
            "names": ["Meredith Grey", "Cristina Yang", "Izzie Stevens", "Alex Karev", "George O'Malley", "Miranda Bailey", "Richard Webber", "Derek Shepherd", "Mark Sloan"]
        },
        {
            "idx": 5, "orig_name": "Patricia Louise Henderson", "orig_age": 61, 
            "names": ["Rachel Green", "Monica Geller", "Phoebe Buffay", "Joey Tribbiani", "Chandler Bing", "Ross Geller", "Gunther", "Janice Litman", "Mike Hannigan"]
        },
        {
            "idx": 6, "orig_name": "Robert Chen", "orig_age": 73, 
            "names": ["Tony Soprano", "Carmela Soprano", "Christopher Moltisanti", "Paulie Gualtieri", "Silvio Dante", "Jennifer Melfi", "Uncle Junior", "Bobby Baccalieri", "Adriana La Cerva"]
        },
        {
            "idx": 7, "orig_name": "Sandra Martinez", "orig_age": 53, 
            "names": ["Carrie Bradshaw", "Samantha Jones", "Charlotte York", "Miranda Hobbes", "Mr. Big", "Aidan Shaw", "Steve Brady", "Harry Goldenblatt", "Stanford Blatch"]
        },
        {
            "idx": 8, "orig_name": "Sarah Chen", "orig_age": 66, 
            "names": ["Lorelai Gilmore", "Rory Gilmore", "Luke Danes", "Emily Gilmore", "Richard Gilmore", "Sookie St. James", "Lane Kim", "Michel Gerard", "Paris Geller"]
        },
        {
            "idx": 9, "orig_name": "Lisa Morgan (Duplicate Placeholder)", "orig_age": 45, # Handling potential duplicate logic or distinct note
             "names": ["Daenerys Targaryen", "Jon Snow", "Tyrion Lannister", "Cersei Lannister", "Jaime Lannister", "Sansa Stark", "Arya Stark", "Bran Stark", "Brienne of Tarth"]
        }
    ]

def get_variations():
    """
    Contains the manually crafted text variations for the notes in Part 033.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Lisa Morgan - Rigid/Flex Bronch Stenosis
            1: "Procedure: Flexible Bronchoscopy with Radial Knife & Balloon Dilation.\nIndication: Tracheal/Bronchial Stenosis (GPA).\nFindings: 5cm tracheal stenosis (60%); RLL/LLL segmental stenosis (80-95%).\nAction: Serial balloon dilation (12-15mm trachea; 6-8mm segments). Radial knife incisions to strictures.\nResult: Recanalization achieved. No bleeding.",
            2: "Operative Report: The patient presented with complex airway stenosis secondary to Granulomatosis with polyangiitis. Under general anesthesia, a flexible bronchoscope was introduced via LMA. Examination revealed a 5cm circumferential tracheal stenosis and multiple severe strictures involving the right lower and left upper lobes. We proceeded with a multimodal intervention utilizing electrocautery radial knife incisions to release fibrous bands, followed by serial balloon dilatations. This resulted in significant luminal restoration across all affected segments.",
            3: "Coding Justification: 31641 (Bronchoscopy with destruction of tumor or relief of stenosis). Procedure involved therapeutic relief of stenosis using multiple modalities (electrocautery knife, balloon dilation) in the trachea and multiple bronchial segments. This single code captures the primary therapeutic intent of stenosis relief.",
            4: "Resident Note:\nProcedure: Flex Bronch, Knife, Balloon.\nAttending: Dr. Hamilton.\n1. LMA placed.\n2. Scope down. Saw stenosis in trachea and lower lobes.\n3. Used radial knife to cut scar tissue.\n4. Dilated with balloons (CRE 12-15mm for trachea, smaller for bronchi).\n5. Airway opened up nicely.",
            5: "did a bronch for lisa morgan she has gpa and bad stenosis. used the knife to cut the strictures and then the balloons to stretch them out. trachea looked bad 60 percent blocked but we opened it. also did the rll and lul segments. everything looks open now no bleeding sent her to recovery.",
            6: "Flexible bronchoscopy with radial knife incisions and balloon dilatation for tracheal and bronchial stenosis secondary to Granulomatosis with polyangiitis. A long segment tracheal stenosis and multiple bronchial strictures were identified. Radial knife incisions were made to the strictures, followed by serial balloon dilatations. Near complete recanalization of the segments was achieved.",
            7: "[Indication] Tracheal and bronchial stenosis (GPA).\n[Anesthesia] General.\n[Description] Tracheal stenosis (5cm, 60%) and bronchial strictures identified. Radial knife incisions performed. Serial balloon dilation (trachea 12-15mm, bronchi 6-8mm) completed.\n[Plan] PACU recovery.",
            8: "We brought Ms. Morgan to the suite to address her airway stenosis caused by GPA. After inducing anesthesia, we visualized a significant tracheal narrowing and multiple bronchial strictures. We used a radial knife to incise the scar tissue and then performed serial balloon dilations to expand the airways. The result was excellent, with good patency restored.",
            9: "Flexible bronchoscopy with electrocautery incision and pneumatic dilation. Diagnosis: Airway constriction due to vasculitis. The stenotic segments were incised and expanded. Luminal patency was restored."
        },
        1: { # Tyrone Jackson - EBUS + Ion RUL
            1: "Procedure: EBUS-TBNA + Ion Robotic Bronch.\n- EBUS: Stations 4R, 7, 10R sampled (Pos for SCC).\n- Ion: Navigated to RUL mass. REBUS confirmed. Bx x7.\n- ROSE: Squamous Cell CA.\n- Plan: Oncology.",
            2: "Operative Summary: A combined staging and diagnostic procedure was performed for a suspected right upper lobe malignancy. Endobronchial ultrasound (EBUS) guided transbronchial needle aspiration of stations 4R, 7, and 10R confirmed N2 disease (squamous cell carcinoma). Subsequently, the Ion robotic platform was utilized to navigate to the 3.2 cm RUL mass. Radial EBUS confirmation was obtained prior to extensive sampling.",
            3: "Codes:\n- 31653: EBUS TBNA 3+ stations (4R, 7, 10R).\n- 31628: Robotic TBBX of RUL mass.\n- 31627: Navigation.\n- 31654: Radial EBUS.\nNote: High complexity staging and diagnostic procedure.",
            4: "Resident Note:\n- EBUS scope: 4R, 7, 10R biopsies -> All SCC.\n- Ion Robot: Drove to RUL lesion.\n- Radial EBUS: Concentric view.\n- Biopsy: 7 passes.\n- Dx: Stage IIIA SCC.",
            5: "tyrone jackson here for staging. did ebus first hit 4r 7 and 10r all positive for squamous. then used the ion robot for the rul mass. found it with radial ebus took a bunch of biopsies. patient has stage 3a disease referral to onc.",
            6: "EBUS-TBNA of stations 4R, 7, and 10R plus Ion robotic bronchoscopy with radial EBUS and biopsy of an RUL mass. Nodal staging was positive for squamous cell carcinoma. Robotic navigation allowed for successful sampling of the primary lesion.",
            7: "[Indication] RUL mass, staging.\n[Anesthesia] General.\n[Description] EBUS-TBNA stations 4R, 7, 10R (31653). Ion Nav (31627) to RUL mass. REBUS (31654). TBBX (31628).\n[Plan] Oncology/Rad Onc.",
            8: "We performed a staging EBUS followed by a robotic biopsy for Mr. Jackson. The EBUS confirmed cancer in the mediastinal and hilar lymph nodes. We then used the Ion robot to biopsy the main tumor in the right upper lobe. The diagnosis is squamous cell carcinoma.",
            9: "EBUS-TBNA of three nodal stations plus Ion robotic bronchoscopy with radial EBUS and sampling of an RUL mass. We aspirated the lymph nodes. We navigated to the RUL tumor and harvested tissue."
        },
        2: { # Dorothy Mae Russell - EBUS 4L, 4R, 7, 10L, 10R, 11L
            1: "Procedure: EBUS-TBNA.\n- Stations Sampled: 7, 4L, 4R, 10L, 10R, 11L.\n- ROSE: Adenocarcinoma in 7, 4L, 4R, 10L, 11L.\n- Diagnosis: Stage IIIC Lung CA.\n- Complications: None.",
            2: "Procedure Note: An extensive endobronchial ultrasound (EBUS) guided transbronchial needle aspiration was performed for mediastinal staging. Systematic survey and sampling of stations 7, 4L, 4R, 10L, 10R, and 11L were conducted. Rapid on-site evaluation confirmed metastatic adenocarcinoma in multiple N2 and N3 stations, establishing a diagnosis of Stage IIIC disease.",
            3: "Billing: 31653 (EBUS TBNA 3 or more stations). Six stations were sampled (7, 4L, 4R, 10L, 10R, 11L). This code captures the entire nodal sampling procedure.",
            4: "Resident Note:\n- EBUS scope introduced.\n- Sampled 6 stations total.\n- 5 stations positive for Adeno (N3 disease).\n- 1 station benign (10R).\n- Pt tol well.",
            5: "long ebus case. sampled 7 4l 4r 10l 10r and 11l. almost all of them positive for adenocarcinoma. poor prognosis stage 3c. sent genetics. no issues during procedure.",
            6: "Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA) of stations 7, 4L, 4R, 10L, 10R, and 11L. Rapid on-site evaluation confirmed metastatic adenocarcinoma in multiple stations. The procedure was uncomplicated.",
            7: "[Indication] LLL mass, extensive adenopathy.\n[Anesthesia] General.\n[Description] EBUS-TBNA performed on 6 stations (31653). ROSE positive for adenocarcinoma in 5 stations.\n[Plan] Medical Oncology.",
            8: "Ms. Russell underwent an EBUS procedure to stage her lung cancer. We sampled lymph nodes from six different areas in her chest. Unfortunately, the results showed cancer has spread to lymph nodes on both sides of her chest, confirming Stage IIIC adenocarcinoma.",
            9: "EBUS-TBNA of six nodal stations. We aspirated multiple mediastinal and hilar lymph nodes. Cytology confirmed extensive metastatic disease."
        },
        3: { # Robert Mills - EBUS Brief
            1: "Procedure: EBUS-TBNA.\n- Stations: 7, 4R, 10R, 11R.\n- ROSE: Pos Adeno (7, 4R, 10R); Neg (11R).\n- Dx: N2 Adenocarcinoma.\n- Plan: Oncology.",
            2: "Operative Summary: EBUS-TBNA was performed to evaluate right-sided lung pathology. Lymph node stations 7, 4R, 10R, and 11R were visualized and sampled. Cytologic evaluation revealed adenocarcinoma in the mediastinal and hilar stations, consistent with N2 disease.",
            3: "Code: 31653 (EBUS TBNA 3+ stations). Four stations (7, 4R, 10R, 11R) were sampled with needle aspiration. Medical necessity supported by cancer diagnosis/staging.",
            4: "Resident Note:\n- EBUS to 4 stations.\n- 7, 4R, 10R = Cancer.\n- 11R = Benign.\n- Stage IIIA/N2.\n- No complications.",
            5: "robert mills ebus. hit 4 nodes 7 4r 10r 11r. three were cancer one was benign. looks like stage 3. refer to onc.",
            6: "EBUS with needle biopsies of stations 7, 4R, 10R, and 11R. Rapid on-site evaluation confirmed adenocarcinoma in three stations. N2 disease confirmed.",
            7: "[Indication] Right lung CA staging.\n[Anesthesia] MAC.\n[Description] EBUS-TBNA stations 7, 4R, 10R, 11R (31653). ROSE positive for malignancy in 3 stations.\n[Plan] Treatment planning.",
            8: "We performed an EBUS procedure on Mr. Mills to check his lymph nodes. We sampled four nodes: 7, 4R, 10R, and 11R. Three of them contained cancer cells, confirming that the disease has spread to the mediastinum (N2 disease).",
            9: "EBUS-TBNA of four nodal stations. We aspirated the target lymph nodes. Malignancy was detected in the subcarinal, paratracheal, and hilar stations."
        },
        4: { # Sarah Martinez - Rigid Bronch, Tumor Debulk, EBUS
            1: "Procedure: Rigid Bronchoscopy, Tumor Debulking (APC/Mechanical), EBUS-TBNA.\n- Finding: Subcarinal mass, severe airway obstruction (R main 90%, L main 50%).\n- Action: APC, mechanical debulking, cryo for clots. EBUS TBNA 7.\n- Result: R main <25%, L main <10% obstruction.",
            2: "Operative Report: The patient underwent rigid bronchoscopy for management of malignant central airway obstruction. Extensive tumor debulking was achieved utilizing mechanical coring and argon plasma coagulation (APC), significantly improving patency in the distal trachea and bilateral mainstem bronchi. Additionally, EBUS-TBNA of a subcarinal mass was performed for diagnosis.",
            3: "Coding: 31641 (Destruction/Debulking), 31652 (EBUS 1-2 stations), 31645 (Therapeutic Aspiration - clots), 31625 (Biopsy). 31640 bundled into 31641. High complexity rigid procedure.",
            4: "Resident Note:\n- Rigid scope placed.\n- Suctioned blood (31645).\n- EBUS TBNA station 7 (31652).\n- APC and mechanical debulking of tumor (31641).\n- Biopsies taken (31625).\n- Hemostasis achieved.",
            5: "rigid bronch for sarah martinez. she had a lot of blood and tumor blocking the airway. suctioned it out. used apc and the rigid scope to core out the tumor. also did an ebus on the subcarinal node. airway looks much better now.",
            6: "Rigid bronchoscopy with tumor debulking and EBUS-TBNA. Extensive endobronchial tumor was debulked using APC and mechanical techniques. EBUS-TBNA of the subcarinal mass was performed. Hemostasis was achieved.",
            7: "[Indication] Malignant airway obstruction.\n[Anesthesia] General.\n[Description] Rigid bronchoscopy. EBUS-TBNA (31652). Tumor debulking via APC/mechanical (31641). Clot aspiration (31645). Biopsy (31625).\n[Plan] ICU observation.",
            8: "Ms. Martinez required an urgent rigid bronchoscopy due to a tumor blocking her airways. We cleared a significant amount of blood and then debulked the tumor using cautery and mechanical tools, opening up her breathing passages. We also sampled the tumor and a nearby lymph node for diagnosis.",
            9: "Rigid bronchoscopy with tumor destruction and EBUS-TBNA. We utilized APC and mechanical methods to recanalize the obstructed airways. We also aspirated the subcarinal lymph node."
        },
        5: { # Patricia Henderson - EBUS Duplicate (Same as #2 style basically)
            1: "Procedure: EBUS-TBNA.\n- Stations: 10R, 11R, 2R, 4R, 7.\n- ROSE: Malignant (7, 4R, 10R); Benign (11R, 2R).\n- Diagnosis: N3 Disease (Sampled contralateral?). Note says RUL nodule but N3 mentioned... assuming extensive spread.",
            2: "Procedure Note: EBUS-TBNA was performed for staging of a right upper lobe lung nodule. Lymph node stations 10R, 11R, 2R, 4R, and 7 were sampled. Rapid on-site evaluation identified adenocarcinoma in stations 7, 4R, and 10R, confirming N2 disease.",
            3: "Code: 31653 (EBUS TBNA 3+ stations). Five stations sampled. Appropriate for staging.",
            4: "Resident Note:\n- EBUS staging.\n- Sampled 5 stations.\n- Positive for Ca: 7, 4R, 10R.\n- Negative: 2R, 11R.\n- No complications.",
            5: "patricia henderson ebus. checked 5 nodes. found cancer in 3 of them. stage 3 disease. patient did fine.",
            6: "Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA) of stations 10R, 11R, 2R, 4R, and 7. ROSE confirmed malignancy in three stations.",
            7: "[Indication] RUL nodule, staging.\n[Anesthesia] General.\n[Description] EBUS-TBNA stations 10R, 11R, 2R, 4R, 7 (31653). ROSE positive in 3 stations.\n[Plan] Oncology.",
            8: "We performed an EBUS on Ms. Henderson to stage her lung cancer. We sampled five lymph nodes. Three of them tested positive for cancer, indicating it has spread to the mediastinum.",
            9: "EBUS-TBNA of five nodal stations. We aspirated the lymph nodes. Malignancy was confirmed in multiple stations."
        },
        6: { # Robert Chen - PleurX Catheter
            1: "Procedure: Indwelling Pleural Catheter (PleurX) Placement.\n- Site: Left, 5th ICS.\n- Action: Tunnel created, 15.5 Fr catheter inserted U/S guidance.\n- Drainage: 1350mL.\n- CXR: Good position.",
            2: "Operative Report: An indwelling tunneled pleural catheter was placed for management of recurrent malignant pleural effusion. Under ultrasound guidance, a 15.5 French PleurX catheter was inserted into the left pleural space via a subcutaneous tunnel. 1,350 mL of fluid was drained without complication.",
            3: "Billing: 32550 (Insertion of indwelling tunneled pleural catheter). Includes tunneling, insertion, and initial drainage. 32554/32555 not billable separately.",
            4: "Resident Note:\n- U/S marked site.\n- Local anesthetic.\n- Tunneled track made.\n- Catheter inserted (Seldinger).\n- Drained 1.3L.\n- Patient educated on use.",
            5: "put in a pleurx catheter for mr chen. left side. used ultrasound. tunneled it properly. got a lot of fluid out. chest xray looks good.",
            6: "Insertion of left-sided indwelling tunneled pleural catheter (PleurX) for recurrent malignant effusion. Ultrasound guidance was used. 1,350 mL of fluid was drained. Catheter function confirmed.",
            7: "[Indication] Recurrent malignant effusion.\n[Anesthesia] Local.\n[Description] PleurX catheter inserted left chest (32550). Tunneled. Drained 1350mL.\n[Plan] Home health drainage.",
            8: "We placed a permanent drainage catheter (PleurX) in Mr. Chen's chest to help manage his fluid buildup. We used ultrasound to guide the placement and created a tunnel under the skin for the catheter. We drained over a liter of fluid, and he is breathing much better.",
            9: "Implantation of an indwelling tunneled pleural catheter. We established a subcutaneous tract and inserted the device under sonographic guidance. Fluid evacuation was performed."
        },
        7: { # Sandra Martinez - Pleuroscopy
            1: "Procedure: Medical Thoracoscopy (Pleuroscopy).\n- Findings: Diffuse nodules (mets).\n- Action: Biopsies x12. Talc Poudrage (5g).\n- Chest Tube: 28Fr placed.\n- Complications: None.",
            2: "Procedure Note: A diagnostic and therapeutic pleuroscopy was performed for a recurrent right pleural effusion. Inspection revealed extensive nodular implants consistent with metastatic disease. Multiple parietal and visceral pleural biopsies were obtained. Talc poudrage was performed for pleurodesis, followed by chest tube placement.",
            3: "Coding: 32650 (Thoracoscopy with pleurodesis). This code includes the diagnostic inspection (32601) and the administration of the pleurodesis agent. Biopsy is technically part of the diagnostic look if not separate code, but 32650 is the primary therapeutic code here.",
            4: "Resident Note:\n- Entry: Right 6th ICS.\n- Pleuroscope: Saw mets everywhere.\n- Biopsy: Took 12 samples.\n- Pleurodesis: Sprayed talc.\n- Exit: 28Fr chest tube.",
            5: "sandra martinez pleuroscopy. went in on the right. lung looked like it had measles lots of nodules. took biopsies. sprayed talc to stick the lung. put a chest tube in.",
            6: "Thoracoscopy with pleurodesis (mechanical or chemical), including diagnostic thoracoscopy and drainage. Extensive pleural metastases were visualized and biopsied. Talc pleurodesis was performed.",
            7: "[Indication] Recurrent effusion, breast CA.\n[Anesthesia] MAC.\n[Description] Pleuroscopy performed. Extensive mets. Biopsies taken. Talc pleurodesis (32650).\n[Plan] Chest tube management.",
            8: "We performed a pleuroscopy on Ms. Martinez. We found extensive cancer spread on the lining of her lung and chest wall. We took multiple biopsies for testing and then sprayed talc to prevent the fluid from coming back (pleurodesis). A chest tube was left in place.",
            9: "Medical thoracoscopy with talc pleurodesis. We inspected the pleural cavity, identifying widespread metastases. Tissue was sampled, and a sclerosing agent was insufflated."
        },
        8: { # Sarah Chen - Thoracentesis
            1: "Procedure: U/S Guided Thoracentesis.\n- Site: Right.\n- Volume: 1200mL clear fluid.\n- Complication: None.\n- Plan: CXR.",
            2: "Procedure Note: A therapeutic thoracentesis was performed for a large symptomatic right pleural effusion. Under ultrasound guidance, an 18-gauge catheter was inserted, and 1,200 mL of straw-colored fluid was removed. The patient tolerated the procedure well with relief of dyspnea.",
            3: "Billing: 32555 (Thoracentesis with imaging guidance). 1.2L removed. Diagnostic and therapeutic intent.",
            4: "Resident Note:\n- U/S: Large effusion.\n- Prep/Drape.\n- Needle in.\n- Drained 1200cc.\n- Catheter out.\n- CXR ordered.",
            5: "sarah chen thoracentesis. used ultrasound to find the spot. pulled off 1.2 liters of fluid. she feels better. sending fluid to lab.",
            6: "Ultrasound-guided therapeutic and diagnostic thoracentesis of right pleural effusion. 1,200 mL of fluid was removed. No complications.",
            7: "[Indication] Symptomatic pleural effusion.\n[Guidance] Ultrasound (32555).\n[Description] 1200mL fluid drained. Catheter removed.\n[Plan] Monitor.",
            8: "We performed a thoracentesis on Ms. Chen to relieve her shortness of breath. Using ultrasound, we drained 1.2 liters of fluid from her right lung. She felt immediate relief.",
            9: "Ultrasound-directed thoracentesis. We aspirated 1,200 mL of pleural fluid under sonographic guidance."
        },
        9: { # Duplicate/Placeholder - Using Generic EBUS
            1: "Procedure: EBUS-TBNA.\n- Stations: 7, 4R, 4L.\n- ROSE: Positive.\n- Dx: Malignancy.",
            2: "Procedure Note: Endobronchial ultrasound was used to sample mediastinal lymph nodes. Stations 7, 4R, and 4L were aspirated. On-site cytology confirmed malignancy.",
            3: "Code: 31653 (EBUS 3 stations).",
            4: "Resident Note:\n- EBUS.\n- 3 stations sampled.\n- Positive for cancer.",
            5: "ebus procedure. sampled 3 nodes. cancer found.",
            6: "EBUS-TBNA of 3 stations. Malignancy confirmed.",
            7: "[Indication] Staging.\n[Description] EBUS 3 stations (31653).\n[Plan] Oncology.",
            8: "We performed an EBUS to sample three lymph nodes. Cancer was found.",
            9: "EBUS-TBNA of three stations. Malignancy detected."
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
            try:
                note_entry["note_text"] = variations_text[idx][style_num]
            except KeyError:
                print(f"Warning: Missing variation for Note {idx}, Style {style_num}. Using original text.")
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]: # Sometimes age might not be there
                     note_entry["registry_entry"]["patient_age"] = new_age
                
                # Check for age in metadata if strictly enforced there, but usually it's derived
                
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN (Patient ID)
                # If original MRN exists, append suffix. If not, generate one.
                orig_mrn = note_entry["registry_entry"].get("patient_mrn")
                if not orig_mrn:
                    # Some entries in source might not have MRN, generate a placeholder
                    orig_mrn = f"IP20260{idx+70}" # Arbitrary base different from previous parts
                
                note_entry["registry_entry"]["patient_mrn"] = f"{orig_mrn}_syn_{style_num}"

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
    output_filename = output_dir / OUTPUT_FILENAME
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()