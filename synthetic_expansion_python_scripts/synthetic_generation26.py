import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_026.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILENAME = "synthetic_expansions_part_026.json"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock data for the patients corresponding to the 10 notes in Part 026.
    Includes original names (if known) or placeholders, original ages, and lists of 
    synthetic names for the variations.
    """
    return [
        {
            "idx": 0, "orig_name": "Patient One", "orig_age": 65, 
            "names": ["John Doe", "Albert Camus", "Robert Frost", "William Blake", "James Joyce", "Thomas Mann", "Richard Wright", "Henry James", "George Orwell"]
        },
        {
            "idx": 1, "orig_name": "Patient Two", "orig_age": 58, 
            "names": ["Mary Shelley", "Jane Austen", "Emily Bronte", "Virginia Woolf", "Sylvia Plath", "Toni Morrison", "Alice Walker", "Zora Neale Hurston", "Maya Angelou"]
        },
        {
            "idx": 2, "orig_name": "Patient Three", "orig_age": 72, 
            "names": ["Charles Dickens", "Mark Twain", "Ernest Hemingway", "F. Scott Fitzgerald", "John Steinbeck", "William Faulkner", "Kurt Vonnegut", "Joseph Heller", "J.D. Salinger"]
        },
        {
            "idx": 3, "orig_name": "Patient Four", "orig_age": 69, 
            "names": ["Leo Tolstoy", "Fyodor Dostoevsky", "Anton Chekhov", "Vladimir Nabokov", "Boris Pasternak", "Aleksandr Solzhenitsyn", "Ivan Turgenev", "Mikhail Bulgakov", "Nikolai Gogol"]
        },
        {
            "idx": 4, "orig_name": "Patient Five", "orig_age": 45, 
            "names": ["Franz Kafka", "Herman Hesse", "Gunther Grass", "Heinrich Boll", "Thomas Bernhard", "Stefan Zweig", "Arthur Schnitzler", "Rainer Maria Rilke", "Bertolt Brecht"]
        },
        {
            "idx": 5, "orig_name": "Patient Six", "orig_age": 75, 
            "names": ["Gabriel Garcia Marquez", "Jorge Luis Borges", "Pablo Neruda", "Julio Cortazar", "Mario Vargas Llosa", "Isabel Allende", "Roberto Bolano", "Octavio Paz", "Carlos Fuentes"]
        },
        {
            "idx": 6, "orig_name": "Patient Seven", "orig_age": 82, 
            "names": ["Haruki Murakami", "Kenzaburo Oe", "Yukio Mishima", "Yasunari Kawabata", "Natsume Soseki", "Osamu Dazai", "Ryunosuke Akutagawa", "Banana Yoshimoto", "Kazuo Ishiguro"]
        },
        {
            "idx": 7, "orig_name": "Patient Eight", "orig_age": 50, 
            "names": ["Chinua Achebe", "Wole Soyinka", "Chimamanda Ngozi Adichie", "Ngugi wa Thiong'o", "Ben Okri", "Nadine Gordimer", "J.M. Coetzee", "Doris Lessing", "Buchi Emecheta"]
        },
        {
            "idx": 8, "orig_name": "Patient Nine", "orig_age": 60, 
            "names": ["Victor Hugo", "Alexandre Dumas", "Gustave Flaubert", "Marcel Proust", "Albert Camus", "Jean-Paul Sartre", "Simone de Beauvoir", "Colette", "Marguerite Duras"]
        },
        {
            "idx": 9, "orig_name": "Dennis Jackson", "orig_age": 66, # From note text
            "names": ["Dennis Jackson", "Dennis P. Jackson", "D. Jackson", "Mr. Jackson", "Dennis Jackson Jr.", "Denny Jackson", "D.L. Jackson", "Dennis R. Jackson", "Dennis Jackson"]
        },
    ]

def get_variations():
    """
    Contains the manually crafted text variations for the 10 notes in Part 026.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Ion robotic bronch, bilateral RUL/LUL nodules
            1: "Procedure: Ion Robotic Bronchoscopy\n- Navigated to RUL nodule. REBUS (+). Forceps biopsy taken.\n- Navigated to LUL nodule. REBUS (+). Forceps biopsy taken.\n- Brushings/washings sent.\n- Complications: None.",
            2: "Operative Report: The patient underwent robotic-assisted bronchoscopy utilizing the Ion platform. We sequentially targeted bilateral PET-avid pulmonary nodules. In the right upper lobe, the lesion was localized via shape-sensing technology, confirmed with radial EBUS, and sampled via forceps. Attention was turned to the left upper lobe where a similar process yielded diagnostic tissue. Bronchial brushings and washings were obtained from both sites.",
            3: "Coding Justification:\n31627 (Navigational Bronchoscopy): Ion robot used for path planning/navigation.\n31628 (Biopsy, Single Lobe): Transbronchial biopsy of RUL nodule.\n+31632 (Biopsy, Add'l Lobe): Transbronchial biopsy of LUL nodule.\n+31654 (REBUS): Radial EBUS probe used to verify tool-in-lesion for peripheral targets.\nMedical Necessity: Bilateral PET-avid nodules.",
            4: "Resident Note:\nProcedure: Robotic Bronchoscopy (Ion).\nAttending: Dr. Smith.\n1. Time out.\n2. ETT placed.\n3. Ion catheter advanced.\n4. RUL nodule identified, confirmed w/ REBUS, bx x3.\n5. LUL nodule identified, confirmed w/ REBUS, bx x3.\n6. Stable.",
            5: "patient here for robotic bronchoscopy ion system used. went to the right upper lobe first saw the nodule on the radial ebus took some bites with the forceps then went to the left upper lobe did the same thing radial ebus confirmed forceps biopsy performed. sent brushings and washings too everything went fine no bleeding.",
            6: "Ion robotic bronchoscopy with sequential sampling of bilateral PET-avid RUL and LUL nodules using radial EBUS and forceps biopsies with brushings/washings. Robotic navigation was successfully employed to localize both targets. Radial probe EBUS confirmed eccentric views of the lesions. Transbronchial forceps biopsies were obtained from the RUL and LUL without complication.",
            7: "[Indication] Bilateral PET-avid nodules.\n[Anesthesia] General.\n[Description] Ion robotic bronchoscopy performed. RUL nodule navigated and confirmed via Radial EBUS; forceps biopsy 31628. LUL nodule navigated and confirmed via Radial EBUS; forceps biopsy 31632.\n[Plan] Path pending.",
            8: "The patient was brought to the bronchoscopy suite for evaluation of bilateral lung nodules. We utilized the Ion robotic system for navigation. First, we targeted the right upper lobe nodule, confirming its location with radial EBUS before taking forceps biopsies. We then navigated to the left upper lobe nodule, again utilizing radial EBUS for confirmation prior to biopsy. Brushings and washings were also collected.",
            9: "Ion robotic bronchoscopy with consecutive sampling of bilateral PET-avid RUL and LUL nodules employing radial EBUS and forceps biopsies with brushings/lavage. The robotic platform facilitated precise localization. Radial EBUS verified the targets. Tissue was harvested from the RUL and LUL."
        },
        1: { # EMN-guided bronch, LLL nodule
            1: "- EMN Bronchoscopy (SuperDimension).\n- LLL nodule localized.\n- Radial EBUS confirmation.\n- Transbronchial biopsies x5.\n- Moderate sedation used.",
            2: "Procedure Note: Electromagnetic navigation (EMN) bronchoscopy was performed under moderate sedation. The hypermetabolic nodule within the left lower lobe was successfully registered and navigated to. Radial endobronchial ultrasound (REBUS) provided concentric confirmation of the lesion. Transbronchial forceps biopsies were subsequently obtained.",
            3: "Billable Services:\n- 31628: TBBX of single lobe (LLL).\n- 31627: Computer-assisted navigation (EMN).\n- 31654: Peripheral EBUS (Radial) for lesion confirmation.\nNote: Moderate sedation administered. Documentation supports medical necessity for navigation due to peripheral location.",
            4: "Procedure Step-by-Step:\n1. Moderate sedation started.\n2. Scope introduced.\n3. EMN registration completed.\n4. Navigated to LLL target.\n5. Radial EBUS showed lesion.\n6. Biopsies taken.\n7. Pt tolerated well.",
            5: "doing a bronch with electromagnetic navigation today for a nodule in the lll. used radial ebus to see it looks like we got it. took some biopsies with the forceps. patient was under moderate sedation did okay no issues.",
            6: "EMN-guided bronchoscopy with radial EBUS confirmation and transbronchial biopsies of a hypermetabolic LLL nodule under moderate sedation. Navigation was successful. Verification with radial probe showed the lesion. Biopsies were taken and sent for pathology.",
            7: "[Indication] Hypermetabolic LLL nodule.\n[Anesthesia] Moderate Sedation.\n[Description] EMN guidance used to reach LLL target. Radial EBUS confirmed position. Transbronchial biopsies obtained (31628).\n[Plan] Discharge to home.",
            8: "We performed an electromagnetic navigation bronchoscopy to access a nodule in the left lower lobe. The patient was comfortably sedated. After creating a roadmap, we navigated to the lesion and confirmed its position with radial EBUS. We then proceeded to take several transbronchial biopsies of the nodule.",
            9: "EMN-directed bronchoscopy with radial EBUS verification and transbronchial sampling of a hypermetabolic LLL nodule under moderate sedation. The lesion was localized using electromagnetic guidance. Radial ultrasound validated the target. Specimens were collected."
        },
        2: { # EBUS-TBNA 4L/10R + Ion RLL mass
            1: "Procedures:\n1. EBUS-TBNA: Stations 4L, 10R.\n2. Robotic Bronch (Ion): RLL mass.\n3. REBUS confirmation.\n4. Biopsy: Cryo + Conventional.\nResult: Samples obtained.",
            2: "Operative Summary: A combined staging and diagnostic procedure was undertaken. First, convex probe EBUS was utilized to perform TBNA of lymph node stations 4L and 10R. Subsequently, the Ion robotic platform was deployed to navigate to the right lower lobe mass. Radial EBUS confirmed the target. Diagnostic yield was optimized using a combination of conventional forceps and cryobiopsy techniques.",
            3: "Coding breakdown:\n- 31652: EBUS TBNA 2 stations (4L, 10R).\n- 31627: Robotic Navigation.\n- 31654: Radial EBUS.\n- 31628: TBBX of RLL mass (Cryo/Forceps included in biopsy code).\nNote: 31629 is bundled into 31652 for same targets; separate distinct targets not noted for conventional TBNA.",
            4: "Resident Procedure Note:\n- Airway secured.\n- Linear EBUS scope: Sampled 4L and 10R.\n- Switch to robotic scope.\n- Navigated to RLL mass.\n- Radial EBUS check: Good.\n- Biopsies: Forceps and Cryo probe used.",
            5: "started with the ebus sampled the 4l and 10r nodes using the needle. then switched to the ion robot for the mass in the rll. radial ebus confirmed it. did cryobiopsy and regular forceps biopsy. looks like good samples.",
            6: "EBUS-TBNA of 4L and 10R nodes plus Ion robotic bronchoscopy with radial EBUS and conventional + cryobiopsy sampling of an RLL mass. Lymph nodes were sampled first for staging. The peripheral mass was then targeted using robotic navigation and sampled extensively.",
            7: "[Indication] Lung mass RLL, mediastinal adenopathy.\n[Anesthesia] General.\n[Description] EBUS-TBNA performed at 4L and 10R (31652). Robotic navigation to RLL mass (31627). Radial EBUS (31654). Transbronchial biopsy (31628) using cryo/forceps.\n[Plan] Oncology follow-up.",
            8: "This session involved both nodal staging and peripheral tumor sampling. We began with EBUS-TBNA, successfully sampling stations 4L and 10R. Following this, we utilized the Ion robotic system to navigate to a mass in the right lower lobe. We confirmed the location with radial EBUS and obtained tissue using both cryobiopsy and standard forceps.",
            9: "EBUS-TBNA of 4L and 10R nodes plus Ion robotic bronchoscopy with radial EBUS and standard + cryoprobe sampling of an RLL mass. We aspirated the lymph nodes for staging. The robotic system guided us to the RLL lesion, where we harvested tissue."
        },
        3: { # Combined EBUS + EMN LLL SCC
            1: "- EBUS-TBNA: Multiple stations (Mediastinal/Hilar).\n- Endobronchial biopsy: LLL airway.\n- EMN Navigation: Peripheral LLL biopsy.\n- Dx: Extensive nodal disease, LLL SCC.",
            2: "Procedure: The patient underwent a comprehensive diagnostic evaluation for suspected stage III lung cancer. Endobronchial ultrasound (EBUS) facilitated TBNA of multiple mediastinal and hilar stations. Inspection revealed an endobronchial component in the LLL, which was biopsied. Additionally, electromagnetic navigation (EMN) was employed to sample the peripheral extent of the LLL squamous cell carcinoma.",
            3: "Codes:\n31652 (EBUS TBNA 1-2 stations) or 31653 if >3. Note says 'multiple', assuming 2 for this var or matching source logic.\n31625 (Endobronchial biopsy).\n31628 (Transbronchial biopsy).\n31627 (Navigation).\nRationale: Distinct services; EBUS for nodes, 31625 for central lesion, 31628/27 for peripheral tumor.",
            4: "Steps:\n1. EBUS TBNA of nodes.\n2. White light bronchoscopy.\n3. Saw tumor in LLL bronchus -> Biopsied (31625).\n4. Navigated further out with EMN -> Biopsied peripheral LLL (31628).\n5. No complications.",
            5: "patient has scc with nodes. did ebus tbna on a bunch of stations. then looked in the lll saw the tumor there took a piece. used the navigation to go deeper into the lll and biopsy the peripheral part too. lots of disease.",
            6: "Combined EBUS-TBNA of multiple mediastinal and hilar stations plus endobronchial and EMN-guided peripheral biopsies of an LLL squamous cell carcinoma. Extensive nodal sampling was performed. Direct endobronchial biopsy of the central airway lesion was obtained. Navigation was used for distal sampling.",
            7: "[Indication] LLL SCC, staging.\n[Anesthesia] General.\n[Description] EBUS-TBNA multiple stations. Endobronchial biopsy LLL (31625). EMN guidance (31627) to peripheral LLL; TBBX (31628).\n[Plan] Oncology referral.",
            8: "We performed a combined procedure to stage and diagnose the patient's lung cancer. Using EBUS, we sampled multiple lymph nodes in the mediastinum and hilum. We also performed a biopsy of the visible tumor in the left lower lobe airway. Finally, we used electromagnetic navigation to guide a biopsy of the peripheral portion of the mass.",
            9: "Integrated EBUS-TBNA of numerous mediastinal and hilar stations plus endobronchial and EMN-directed peripheral sampling of an LLL squamous cell carcinoma. We aspirated the nodes. We sampled the central lesion directly and navigated to the distal tumor."
        },
        4: { # EBUS 4R/10R + Ion RUL cryo
            1: "Procedure:\n- EBUS-TBNA: 4R, 10R.\n- Robotic Bronch (Ion): RUL nodule.\n- REBUS (+).\n- Tool: Cryoprobe.\n- Pt: Never-smoker.",
            2: "Operative Note: In this never-smoker with an RUL nodule, we proceeded with EBUS-TBNA of stations 4R and 10R to rule out occult nodal disease. The Ion robotic system was then used to navigate to the right upper lobe nodule. Radial EBUS confirmed the target location. A cryobiopsy was performed to preserve tissue architecture for molecular testing.",
            3: "Billing:\n- 31652: EBUS TBNA (4R, 10R).\n- 31627: Robotic Nav.\n- 31654: Radial EBUS.\n- 31628: Transbronchial biopsy (Cryo).\nJustification: Staging and diagnosis of peripheral RUL nodule.",
            4: "Resident Note:\n- EBUS scope: Biopsied 4R and 10R.\n- Ion Robot: Drove to RUL.\n- Radial EBUS: Confirmed.\n- Cryo biopsy: 3 passes.\n- Frozen section: pending.",
            5: "patient never smoked has a rul nodule. did ebus first on 4r and 10r. then used the ion robot to get out to the nodule. used radial ebus to see it. used the cryo probe to get a biopsy. hopefully we get an answer.",
            6: "EBUS-TBNA of 4R and 10R nodes plus Ion robotic bronchoscopy with radial EBUS and cryobiopsy of an RUL nodule. Staging was negative on ROSE. Robotic navigation allowed access to the RUL lesion. Cryobiopsy was utilized for high-quality tissue acquisition.",
            7: "[Indication] RUL nodule, never-smoker.\n[Anesthesia] General.\n[Description] EBUS-TBNA 4R/10R (31652). Ion Nav (31627) to RUL. Radial EBUS (31654). Cryobiopsy (31628).\n[Plan] Molecular panel if positive.",
            8: "For this patient, a never-smoker with a lung nodule, we performed EBUS staging followed by robotic biopsy. We sampled lymph nodes 4R and 10R. Then, using the Ion system, we reached the nodule in the right upper lobe. After confirming with radial EBUS, we used a cryoprobe to obtain the biopsy.",
            9: "EBUS-TBNA of 4R and 10R nodes plus Ion robotic bronchoscopy with radial EBUS and cryosampling of an RUL nodule. We aspirated the indicated nodes. The robot navigated to the lesion, and we utilized cryotechnology to harvest the specimen."
        },
        5: { # Comprehensive EBUS (5, 7, 10L) + EMN LLL
            1: "- EBUS-TBNA: Stations 5, 7, 10L.\n- EMN Bronchoscopy: LLL mass.\n- REBUS (+).\n- TBBX, BAL, Brushings performed.",
            2: "Procedure: A comprehensive staging EBUS-TBNA was performed, sampling stations 5 (subaortic), 7 (subcarinal), and 10L (hilar). Following this, electromagnetic navigation guided the bronchoscope to a left lower lobe mass. Radial EBUS confirmed the peripheral location. Diagnostic transbronchial biopsy, bronchoalveolar lavage (BAL), and cytologic brushings were obtained.",
            3: "Coding:\n- 31653: EBUS TBNA 3+ stations (5, 7, 10L).\n- 31628: TBBX LLL.\n- 31624: BAL.\n- 31623: Brushings.\n- 31627: EMN Nav.\n- 31654: REBUS.\nNote: High complexity procedure involving staging and full diagnostic workup.",
            4: "Steps:\n1. EBUS of 5, 7, 10L.\n2. EMN setup and reg.\n3. Nav to LLL mass.\n4. REBUS check.\n5. Biopsy x4.\n6. Brushings x1.\n7. BAL x1 aliquot.",
            5: "big case today. did ebus on 5 7 and 10l. then switched to emn for the lll mass. found it with radial ebus. did the works biopsy bal and brushes. patient tolerated it well.",
            6: "Comprehensive combined EBUS-TBNA of stations 5, 7, and 10L plus EMN-guided radial EBUS-confirmed transbronchial biopsy of an LLL mass with BAL and brushings. Triple station nodal sampling was completed. The peripheral mass was sampled via multiple modalities including lavage and brushing.",
            7: "[Indication] LLL mass, staging.\n[Anesthesia] General.\n[Description] EBUS-TBNA stations 5, 7, 10L (31653). EMN Nav (31627) to LLL. REBUS (31654). TBBX (31628), BAL (31624), Brush (31623).\n[Plan] Review path.",
            8: "We conducted a thorough evaluation including EBUS staging and peripheral biopsy. We sampled lymph nodes at stations 5, 7, and 10L. Then, using electromagnetic navigation, we targeted the mass in the left lower lobe. We confirmed the target with radial EBUS and performed biopsies, brushings, and a wash (BAL).",
            9: "Extensive combined EBUS-TBNA of stations 5, 7, and 10L plus EMN-directed radial EBUS-verified transbronchial sampling of an LLL mass with BAL and brushings. We aspirated three nodal stations. We navigated to the LLL tumor and obtained tissue via biopsy, brush, and lavage."
        },
        6: { # Thoracentesis
            1: "Procedure: U/S Guided Thoracentesis.\n- Site: Right.\n- Fluid: 420 mL turbid.\n- Analysis: pH/Glucose low.\n- Complications: None.",
            2: "Procedure Note: The patient presented with a complex right parapneumonic effusion. Ultrasound guidance was utilized to identify a safe pocket of fluid. A catheter was introduced into the pleural space, and 420 mL of turbid fluid was aspirated. Bedside analysis revealed low pH and glucose, consistent with an empyema or complicated effusion.",
            3: "Billing: 32555 (Thoracentesis with imaging guidance). Imaging guidance is integral to this code. 420 mL removed. Diagnostic intent. 32554 not applicable as imaging was used.",
            4: "Resident Note:\n- Pre-procedure US: Loculated effusion.\n- Prep and drape.\n- Local anesthetic.\n- Needle insertion under US.\n- Drained 420cc.\n- Sample sent to lab.",
            5: "did a thoracentesis on the right side used ultrasound to find the fluid. got about 420 ml of cloudy stuff out. sent it for ph and glucose looks like an infection. no pneumothorax.",
            6: "Ultrasound-guided diagnostic thoracentesis of a complex right parapneumonic effusion in a patient with recent pneumonia. 420 mL of turbid fluid was removed. Fluid analysis showed low pH and glucose. The procedure was uncomplicated.",
            7: "[Indication] Right parapneumonic effusion.\n[Guidance] Ultrasound (32555).\n[Description] 420 mL turbid fluid removed. Catheter withdrawn.\n[Plan] Antibiotics, consider tube if pH low.",
            8: "We performed a diagnostic thoracentesis on the patient's right side to evaluate the effusion. Using ultrasound guidance, we inserted a needle and removed 420 mL of turbid fluid. Preliminary tests show low pH and glucose, suggesting a complicated effusion.",
            9: "Ultrasound-directed diagnostic thoracentesis of a complicated right parapneumonic effusion removing 420 mL of turbid fluid. Sonography guided the puncture. The aspirate appeared purulent."
        },
        7: { # Rigid Bronch Stenosis
            1: "Procedure: Rigid Bronchoscopy.\n- Path: L Mainstem stenosis (GPA).\n- Action: Radial cuts, APC, Balloon dilation.\n- Complication: Airway injury -> L Chest Tube (32551).\n- Result: Improved patency.",
            2: "Operative Report: The patient with granulomatosis with polyangiitis and severe left mainstem stenosis underwent rigid bronchoscopy. The stenosis was managed with radial knife incisions, argon plasma coagulation (APC), and balloon dilation. During the procedure, a transmural airway injury occurred. A left-sided tube thoracostomy was immediately performed to manage the resulting pneumothorax.",
            3: "Codes:\n- 31641: Bronchoscopy with lysis of stenosis (Knife/APC/Balloon).\n- 32551: Tube thoracostomy (Chest tube) for complication management.\nNote: 31622 bundled. 31630 bundled into 31641? Or 31641 covers 'any method'.",
            4: "Resident Note:\n- Rigid scope inserted.\n- Severe LMS stenosis found.\n- Tx: Cuts, APC, Balloon.\n- Complication: Tear in airway.\n- Action: Chest tube placed left side.\n- Pt stable.",
            5: "tough case. rigid bronch for gpa stenosis in the left main. used the knife and apc and balloon. balloon caused a tear so we had to put in a chest tube on the left. airway is open now though.",
            6: "Rigid bronchoscopy for severe left mainstem bronchial stenosis due to granulomatosis with polyangiitis. Radial knife incisions, APC, and balloon dilation were used. An airway injury occurred, requiring immediate placement of a left chest tube.",
            7: "[Indication] LMS Stenosis (GPA).\n[Anesthesia] General/Rigid.\n[Description] Stenosis relieved via knife/APC/Balloon (31641). Airway injury noted. Tube thoracostomy performed (32551).\n[Plan] Monitor air leak.",
            8: "We performed a rigid bronchoscopy to treat severe stenosis in the left mainstem bronchus caused by GPA. We used a radial knife, APC, and balloon dilation to open the airway. Unfortunately, the dilation resulted in an airway injury, so we placed a left chest tube to treat the complication.",
            9: "Rigid bronchoscopy for severe left mainstem bronchial constriction using radial knife incisions, APC, and balloon expansion. The procedure was complicated by airway trauma necessitating left tube thoracostomy."
        },
        8: { # Pleuroscopy
            1: "Procedure: Medical Pleuroscopy (32650).\n- Indication: Recurrent exudative effusion, neg cytology.\n- Action: Inspection, Biopsies, Talc Pleurodesis.\n- Result: Fluid drained, talc insufflated.",
            2: "Procedure Note: A semi-rigid pleuroscopy was performed for evaluation of a recurrent right exudative pleural effusion. The pleural space was inspected, revealing nodularities which were biopsied. Given the recurrent nature, a talc poudrage pleurodesis was performed to prevent reaccumulation.",
            3: "Coding: 32650 (Thoracoscopy with pleurodesis). This code includes the diagnostic inspection (32601) and the administration of the pleurodesis agent. Biopsy is technically part of the diagnostic look if not separate code, but 32650 is the primary therapeutic code here.",
            4: "Resident Note:\n- Trocar placed.\n- Pleuroscope inserted.\n- Drained fluid.\n- Saw nodules -> biopsied.\n- Sprayed talc for pleurodesis.\n- Chest tube placed.",
            5: "did a pleuroscopy for the recurrent effusion. looked inside took some biopsies of the pleura. put in talc for pleurodesis so it doesnt come back. chest tube in place.",
            6: "Planned pleuroscopy for recurrent right exudative pleural effusion with prior negative cytology. The pleural space was inspected, biopsies were taken, and talc pleurodesis was performed.",
            7: "[Indication] Recurrent effusion.\n[Anesthesia] MAC/Local.\n[Description] Pleuroscopy performed. Fluid drained. Pleura biopsied. Talc pleurodesis (32650) completed.\n[Plan] Chest tube to suction.",
            8: "We took the patient for a pleuroscopy to investigate their recurrent pleural effusion. We drained the fluid and inspected the pleural cavity, taking biopsies of abnormal areas. We then performed a pleurodesis with talc to seal the space.",
            9: "Scheduled pleuroscopy for recurring right exudative pleural effusion with previous negative cytology, intended for pleural examination, sampling, and pleurodesis."
        },
        9: { # Bronch w/ RFA (Dennis Jackson)
            1: "Procedure: Bronchoscopy w/ RFA.\n- Target: RLL nodule (SCC).\n- Guidance: ENB + Radial EBUS.\n- Ablation: 105C for 10 min.\n- Result: Good ablation zone.",
            2: "Operative Report: Under general anesthesia, Mr. Jackson underwent bronchoscopic ablation of an RLL squamous cell carcinoma. Electromagnetic navigation bronchoscopy (ENB) was used to localize the superior segment lesion. Radial EBUS confirmed the target. A radiofrequency ablation (RFA) catheter was deployed, and treatment was delivered at 105 degrees Celsius for 10 minutes. No immediate complications were observed.",
            3: "Billing Codes:\n- 31641: Destruction of tumor (RFA).\n- 31627: Navigation.\n- 31654: Radial EBUS.\nNote: Diagnosis is SCC. Procedure is therapeutic ablation.",
            4: "Resident Note:\n- Patient: Dennis Jackson.\n- Dx: RLL SCC.\n- ENB to RLL.\n- REBUS confirmed.\n- RFA probe placed.\n- Burned at 105C x 10m.\n- Stable.",
            5: "dennis jackson here for rfa of his lung tumor. used the navigation and the ultrasound to find the rll nodule. cooked it with the rfa probe for 10 mins. everything looks good cxr tomorrow.",
            6: "Bronchoscopy with radiofrequency ablation of a 2.2 cm RLL nodule using ENB and radial EBUS confirmation. The probe was placed, and ablation was performed at 105°C for 10 minutes. The patient tolerated the procedure well.",
            7: "[Indication] RLL SCC (2.2cm).\n[Anesthesia] General.\n[Description] ENB (31627) to RLL. REBUS (31654) confirmed. RFA (31641) performed 105C/10min. No bleeding.\n[Plan] CXR, DC if stable.",
            8: "Mr. Jackson underwent a bronchoscopy for radiofrequency ablation of his right lower lobe tumor. We used electromagnetic navigation and radial EBUS to precisely locate the cancer. We then inserted the RFA probe and treated the lesion at 105 degrees for 10 minutes. There were no complications.",
            9: "Bronchoscopy with radiofrequency destruction of an RLL nodule using ENB and radial EBUS verification. The lesion was localized and ablated. Treatment parameters were 105°C for 10 minutes."
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
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN (Patient ID)
                # If original MRN exists, append suffix. If not, generate one.
                orig_mrn = note_entry["registry_entry"].get("patient_mrn")
                if not orig_mrn:
                    # Some entries in source might not have MRN, generate a placeholder
                    orig_mrn = f"IP20260{idx+40}" # Arbitrary base
                
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