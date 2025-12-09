import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_044.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILENAME = "synthetic_interventional_notes_part_044.json"

def generate_random_date(year=2025):
    """Generates a random date within the specified year."""
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns a list of dictionaries. Each dictionary corresponds to one original note index (0-9).
    It contains the original name/age and a list of 9 new names to be used for the variations.
    """
    return [
        {
            "idx": 0, "orig_name": "Harold Reeves", "orig_age": 68,
            "names": ["Arthur Dent", "Henry Blake", "George Miller", "Edward Norton", "Frank Castle", "Walter White", "James Gordon", "Bruce Wayne", "Clark Kent"]
        },
        {
            "idx": 1, "orig_name": "Maria Alvarez", "orig_age": 74,
            "names": ["Elena Fisher", "Sarah Connor", "Ellen Ripley", "Leia Organa", "Dana Scully", "Clarice Starling", "Hermione Granger", "Katniss Everdeen", "Lara Croft"]
        },
        {
            "idx": 2, "orig_name": "Elise Morgan", "orig_age": 62,
            "names": ["Diana Prince", "Natasha Romanoff", "Wanda Maximoff", "Carol Danvers", "Hope Van Dyne", "Peggy Carter", "Shuri Udaku", "Gamora Zen", "Nebula Kai"]
        },
        {
            "idx": 3, "orig_name": "Corey Daniels", "orig_age": 59,
            "names": ["Tony Stark", "Steve Rogers", "Thor Odinson", "Bruce Banner", "Clint Barton", "Peter Parker", "Scott Lang", "Stephen Strange", "T'Challa Udaku"]
        },
        {
            "idx": 4, "orig_name": "David Cho", "orig_age": 69,
            "names": ["Han Solo", "Luke Skywalker", "Obi-Wan Kenobi", "Anakin Skywalker", "Mace Windu", "Qui-Gon Jinn", "Lando Calrissian", "Poe Dameron", "Finn FN-2187"]
        },
        {
            "idx": 5, "orig_name": "Evelyn Harris", "orig_age": 71,
            "names": ["Jean Grey", "Ororo Munroe", "Anna Marie", "Kitty Pryde", "Emma Frost", "Raven Darkholme", "Jubilation Lee", "Betsy Braddock", "Alison Blaire"]
        },
        {
            "idx": 6, "orig_name": "Patrick O'Neil", "orig_age": 64,
            "names": ["James Kirk", "Spock Vulcan", "Leonard McCoy", "Montgomery Scott", "Hikaru Sulu", "Pavel Chekov", "Jean-Luc Picard", "William Riker", "Geordi La Forge"]
        },
        {
            "idx": 7, "orig_name": "Sheryl Lyons", "orig_age": 63,
            "names": ["Kathryn Janeway", "Seven of Nine", "B'Elanna Torres", "Deanna Troi", "Beverly Crusher", "Nyota Uhura", "Christine Chapel", "Tasha Yar", "Ro Laren"]
        },
        {
            "idx": 8, "orig_name": "Robert Jensen", "orig_age": 75,
            "names": ["Fox Mulder", "Jack O'Neill", "Daniel Jackson", "Teal'c Jaffa", "George Hammond", "Samantha Carter", "John Sheppard", "Rodney McKay", "Ronon Dex"]
        },
        {
            "idx": 9, "orig_name": "Aisha Khan", "orig_age": 58,
            "names": ["Laura Roslin", "Kara Thrace", "Sharon Valerii", "Number Six", "Ellen Tigh", "Anastasia Dualla", "Cally Tyrol", "Helena Cain", "Sherry Palmer"]
        }
    ]

def get_variations():
    """
    Returns a nested dictionary of manual text variations.
    Keys: Note Index (0-9) -> Style Index (1-9) -> Note Text
    """
    variations = {
        # Note 0: Flexible Bronchoscopy with Linear EBUS-TBNA (Stations 4R, 7) - CPT 31652
        0: {
            1: "Procedures: Bronchoscopy, EBUS-TBNA.\nIndication: Staging.\n- Sedation: Mod (Fentanyl/Versed).\n- Airway: Native.\n- EBUS: 4R (22G x3), 7 (22G x3).\n- No comps.\n- Plan: Path f/u.",
            2: "OPERATIVE REPORT\n\nINDICATION: The patient presented with mediastinal lymphadenopathy concerning for metastatic disease. \n\nPROCEDURE: Following the administration of moderate conscious sedation, a curvilinear array echo-bronchoscope was introduced via the oral route. A systematic ultrasonic evaluation of the mediastinum was conducted. Lymph node stations 4R (lower paratracheal) and 7 (subcarinal) were identified as enlarged and sonographically distinct. Real-time ultrasound-guided transbronchial needle aspiration (EBUS-TBNA) was performed on both stations using a 22-gauge needle to obtain diagnostic material. Hemostasis was achieved spontaneously.",
            3: "CPT Justification:\n31652: Bronchoscopy with EBUS-TBNA of 1-2 mediastinal stations.\n- Station 4R sampled under US guidance.\n- Station 7 sampled under US guidance.\nTechnique: Flexible bronchoscopy with linear EBUS probe. Needle aspiration performed real-time.",
            4: "Procedure Note\nAttending: Dr. Porter\nResident: [Name]\nPatient: [Patient Name]\nProcedure: EBUS-TBNA\n\nSteps:\n1. Time out performed.\n2. Sedation started.\n3. Scope passed orally.\n4. Identified nodes 4R and 7.\n5. Biopsied 4R x 3 passes.\n6. Biopsied 7 x 3 passes.\n7. Scope removed. Patient stable.",
            5: "pt came for ebus staging we gave him some versed and fentanyl scope went down fine looked at the airway nothing inside then switched to ebus scope found the 4r node and the 7 node stuck them both three times with the needle minimal bleeding patient woke up fine sent to recovery no issues.",
            6: "INDICATION: Mediastinal adenopathy. PROCEDURE: Flexible bronchoscopy with EBUS-TBNA. SEDATION: Moderate. DESCRIPTION: The scope was introduced. No endobronchial lesions. EBUS identified lymph nodes at stations 4R and 7. TBNA performed on both stations (3 passes each). Samples sent to cytology. Tolerated well.",
            7: "[Indication]\nMediastinal lymphadenopathy (4R, 7) for staging.\n[Anesthesia]\nModerate sedation (fentanyl/midazolam).\n[Description]\nEBUS scope introduced. Station 4R sampled (3 passes). Station 7 sampled (3 passes). No endobronchial lesions seen.\n[Plan]\nPathology follow-up.",
            8: "The patient was brought to the bronchoscopy suite for evaluation of mediastinal lymphadenopathy. After establishing moderate sedation, the EBUS scope was inserted. We systematically examined the mediastinum. We focused on station 4R and station 7, both of which appeared enlarged. We performed transbronchial needle aspiration on both stations, obtaining three passes from each to ensure adequate cellularity. The procedure concluded without complications.",
            9: "Evaluation of mediastinal nodes. Using the ultrasound scope, we visualized and aspirated the 4R and 7 nodal stations. The needle was deployed into the targets under real-time guidance. Samples were collected for cytologic analysis. The patient tolerated the session well."
        },
        # Note 1: Deep sedation, Linear EBUS (Station 7), Transbronchial biopsy (RML) - CPT 31652, 31628
        1: {
            1: "Dx: RML Nodule.\nAnesthesia: Deep (Propofol), ETT.\nAction:\n1. EBUS Station 7 -> 3 passes (31652).\n2. Scope exchange.\n3. Fluoro TBBx RML medial segment -> 4 bites (31628).\nResult: Samples sent. No pneumo.",
            2: "PROCEDURE NARRATIVE: The patient was placed under deep sedation and intubated. Initial interrogation with the linear echo-endoscope revealed a distinct subcarinal lymph node (Station 7), which was sampled via transbronchial needle aspiration. The instrument was then exchanged for a therapeutic flexible bronchoscope. Under fluoroscopic guidance, the right middle lobe medial segment was cannulated. Transbronchial forceps biopsies were obtained from the peripheral nodular opacity. Post-procedural fluoroscopy excluded pneumothorax.",
            3: "Coding Summary:\n- 31652: EBUS-TBNA of 1 nodal station (Station 7).\n- 31628: Transbronchial lung biopsy, single lobe (RML).\nNote: Separate maneuvers. EBUS scope used for staging; Therapeutic scope used for parenchymal biopsy.",
            4: "Procedure: EBUS + TBBx\nStaff: Dr. Lee\n1. ETT placed.\n2. EBUS of Station 7 (3 passes).\n3. Switch to standard scope.\n4. Navigated to RML medial seg.\n5. Fluoro on.\n6. 4 biopsies taken with forceps.\n7. No bleeding. Extubated.",
            5: "procedure note for mrs alvarez or whatever name we use she has that nodule in the right middle lobe and a node under the carina. we put her to sleep with propofol tube in. did the ebus first on the 7 node got good cores. then switched scopes went to the rml used the fluoro to see where we were going took 4 bites with the forceps. no pneumo seen after. patient woke up good.",
            6: "Procedure: Bronchoscopy with EBUS and Transbronchial Biopsy. Diagnosis: RML nodule, subcarinal adenopathy. Anesthesia: Deep/ETT. Description: EBUS-TBNA performed on Station 7 (subcarinal). Standard scope used to access RML medial segment. Transbronchial biopsies obtained under fluoroscopic guidance. No complications.",
            7: "[Indication]\nRML nodule and subcarinal lymphadenopathy.\n[Anesthesia]\nDeep sedation, ETT.\n[Description]\n1. EBUS-TBNA of Station 7.\n2. Transbronchial biopsy of RML nodule (medial segment) using fluoroscopy.\n[Plan]\nDischarge to home.",
            8: "Under deep sedation, we proceeded with a combined staging and diagnostic procedure. First, the EBUS scope was used to sample the subcarinal lymph node (Station 7) to rule out N2 disease. Following this, we switched to a standard bronchoscope. We navigated to the medial segment of the Right Middle Lobe. Using fluoroscopic guidance to locate the nodule, we performed transbronchial biopsies. The patient remained stable throughout.",
            9: "We performed a dual-modality bronchoscopy. First, we aspirated the subcarinal node using ultrasound guidance. Then, we switched instruments to target the parenchymal lesion in the right middle lobe. Forceps were deployed to acquire tissue samples from the lung periphery under x-ray visualization."
        },
        # Note 2: General anesthesia, Linear EBUS (2R, 4R, 4L, 7) - CPT 31653
        2: {
            1: "Indication: LUL CA, mediastinal staging.\nAnesthesia: GA/ETT.\nNodes Sampled (EBUS): 2R, 4R, 4L, 7.\nTotal Stations: 4.\nPasses: 13 total.\nComplications: None.",
            2: "OPERATIVE NOTE: The patient, with known left upper lobe adenocarcinoma, underwent systematic mediastinal staging via endobronchial ultrasound. Under general anesthesia, the following nodal stations were identified and sampled via fine needle aspiration: Right Upper Paratracheal (2R), Right Lower Paratracheal (4R), Left Lower Paratracheal (4L), and Subcarinal (7). This extensive sampling (4 stations) is consistent with complete mediastinal staging guidelines.",
            3: "Billing: 31653 (EBUS sampling 3 or more stations).\nStations sampled:\n1. 2R\n2. 4R\n3. 4L\n4. 7\nTechnique: Linear array EBUS with 22G needle.",
            4: "Resident Procedure Note\nProcedure: EBUS Staging\nAttending: Dr. Hale\n\nStations Biopsied:\n- 2R (3 passes)\n- 4R (3 passes)\n- 4L (3 passes)\n- 7 (4 passes)\n\nTechnique: ETT, General Anesthesia. All samples to cytology. No complications.",
            5: "we did a full staging ebus today on elise morgan she has lung cancer lul. tube was already in. we hit 2r 4r 4l and 7. lots of passes sent everything to the lab. airway looked okay otherwise. woke her up and sent her to pacu.",
            6: "Procedure: EBUS-TBNA. Indication: Staging LUL Adenocarcinoma. Anesthesia: GA. Stations Sampled: 2R, 4R, 4L, 7. Technique: 22G needle aspiration under ultrasound guidance. Outcome: Adequate samples obtained from all 4 stations.",
            7: "[Indication]\nLUL adenocarcinoma, mediastinal staging.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nLinear EBUS performed. Transbronchial needle aspiration of stations 2R, 4R, 4L, and 7.\n[Plan]\nOncology follow-up.",
            8: "The patient required mediastinal staging for her lung cancer. We utilized general anesthesia and an endotracheal tube. The EBUS scope allowed us to visualize and sample four distinct lymph node stations: 2R, 4R, 4L, and 7. We took multiple passes at each site to ensure diagnostic yield. The patient tolerated the procedure well.",
            9: "Comprehensive nodal evaluation via ultrasound bronchoscopy. We targeted and aspirated four separate mediastinal stations (2R, 4R, 4L, 7). The cellular material was collected for staging purposes. No adverse events occurred."
        },
        # Note 3: Robotic Nav (Ion), Radial EBUS, RLL TBBx, Linear EBUS (4R, 7, 10R) - CPT 31653, 31627, 31654, 31628
        3: {
            1: "Proc: Robotic Bronch (Ion) + Radial EBUS + TBBx + Linear EBUS.\nTarget: RLL nodule.\nNav: Robot to lesion (31627). Radial EBUS confirmed (31654).\nBx: TBBx RLL (31628).\nStaging: Linear EBUS 4R, 7, 10R (31653).\nStatus: Stable.",
            2: "OPERATIVE SUMMARY: This patient underwent a complex combined procedure utilizing the Ion robotic platform for peripheral navigation. We successfully navigated to the target lesion in the RLL lateral basal segment. Confirmation was achieved via radial EBUS probe (concentric view). Transbronchial biopsies were obtained. Following the robotic portion, a linear EBUS scope was introduced for mediastinal and hilar staging, sampling stations 4R, 7, and 10R.",
            3: "Code Justification:\n- 31627: Computer-assisted navigation (Robotic).\n- 31654: Peripheral EBUS (Radial probe verification).\n- 31628: Transbronchial biopsy (RLL).\n- 31653: Linear EBUS staging (3 stations: 4R, 7, 10R).",
            4: "Procedure: Robotic Bronchoscopy\n1. GA/ETT.\n2. Ion robot registration.\n3. Navigated to RLL nodule.\n4. Radial EBUS confirmation.\n5. Biopsy x 5.\n6. Removed robot, inserted EBUS scope.\n7. Sampled 4R, 7, 10R.\n8. Extubated.",
            5: "did the robotic bronch today on corey daniels used the ion system. navigated out to that rll nodule radial ebus showed we were right in it. took biopsies. then we pulled the robot and put the ebus scope down to check the nodes. hit 4r 7 and 10r. minimal bleeding.",
            6: "Procedure: Robotic Navigational Bronchoscopy, Radial EBUS, Biopsy, Linear EBUS Staging. Target: RLL nodule. Nodes: 4R, 7, 10R. Anesthesia: GA. Description: Navigated to RLL lesion with robotics. Confirmed with REBUS. Biopsied. Staged mediastinum/hilum with Linear EBUS (3 stations).",
            7: "[Indication]\nRLL nodule, staging.\n[Anesthesia]\nGeneral.\n[Description]\n1. Robotic navigation (Ion) to RLL.\n2. Radial EBUS confirmation.\n3. Transbronchial biopsy RLL.\n4. Linear EBUS-TBNA of 4R, 7, 10R.\n[Plan]\nDischarge.",
            8: "We performed a robotic-assisted bronchoscopy to access a peripheral RLL nodule. Once navigation was complete, we used a radial EBUS probe to verify the lesion's location. Biopsies were then taken. To complete the staging, we switched to a linear EBUS scope and sampled three nodal stations: 4R, 7, and 10R.",
            9: "Robotic exploration of the airways. We guided the catheter to the RLL target and verified position with radial ultrasound. Tissue was sampled via forceps. Subsequently, we interrogated the mediastinum and hilum, aspirating nodes at stations 4R, 7, and 10R."
        },
        # Note 4: Navigational Bronchoscopy (Illumisite), Radial EBUS, LUL TBBx, Fiducial placement - CPT 31626, 31628, 31627, 31654
        4: {
            1: "Ind: LUL Nodule, SBRT planning.\nProc: ENB (Illumisite) + REBUS + TBBx + Fiducials.\nSteps:\n- Nav to LUL apicoposterior (31627).\n- Radial EBUS confirm (31654).\n- TBBx x4 (31628).\n- 3 Gold Fiducials placed (31626).",
            2: "PROCEDURE: Electromagnetic navigational bronchoscopy was performed utilizing the Illumisite platform. The target lesion in the LUL apicoposterior segment was localized. Radial EBUS confirmed an eccentric view. Diagnostic transbronchial biopsies were performed. Subsequently, to facilitate Stereotactic Body Radiation Therapy (SBRT), three gold fiducial markers were deployed in and around the tumor volume under fluoroscopic guidance.",
            3: "CPT Coding:\n- 31627: Navigational bronchoscopy (ENB).\n- 31654: Radial EBUS (Peripheral).\n- 31628: Transbronchial lung biopsy (Single lobe).\n- 31626: Placement of fiducial markers.",
            4: "Resident Note:\nProcedure: Nav Bronch + Fiducials\n1. GA, ETT.\n2. Registered Illumisite.\n3. Drove to LUL target.\n4. REBUS check.\n5. Biopsies taken.\n6. Dropped 3 fiducials for Rad Onc.\n7. All good.",
            5: "david cho came in for fiducials and biopsy. used the superdimension or illumisite whatever we have. navigated to the lul. radial probe showed the lesion. took some bites. then put in 3 gold seeds for the radiation doctors. no issues.",
            6: "Procedure: ENB, REBUS, Biopsy, Fiducials. Site: LUL. Anesthesia: GA. Details: Electromagnetic navigation used to reach LUL lesion. Confirmed with radial EBUS. Biopsies obtained. Three fiducial markers placed for SBRT. No complications.",
            7: "[Indication]\nLUL nodule, biopsy and fiducials.\n[Anesthesia]\nGeneral.\n[Description]\n1. ENB navigation.\n2. Radial EBUS.\n3. Transbronchial biopsy.\n4. Fiducial placement (x3).\n[Plan]\nSBRT planning.",
            8: "We utilized electromagnetic navigation to reach a peripheral nodule in the left upper lobe. Radial EBUS was used to confirm the location. We proceeded to obtain biopsies for diagnosis. Following this, we deployed three fiducial markers into the lesion to assist with future radiation therapy.",
            9: "Guided bronchoscopy for marker deployment. We navigated to the LUL target, verified with radial ultrasound, and sampled the tissue. Finally, we implanted gold markers to guide stereotactic radiation."
        },
        # Note 5: Bronchoscopy with PDT light application (Right Mainstem) - CPT 31641
        5: {
            1: "Indication: RMS SCC, s/p Photofrin.\nProc: Bronchoscopy + PDT Light.\nAction: Light fiber placed RMS. 200 J/cm treated.\nNo biopsy/stent.\nCode: 31641.",
            2: "OPERATIVE REPORT: The patient presented 48 hours post-Photofrin injection for photodynamic therapy activation. The bronchoscope identified the superficial squamous cell carcinoma in the right mainstem bronchus. A cylindrical diffuser fiber was inserted and light energy was delivered to the tumor bed for the prescribed duration to effect tumor necrosis.",
            3: "Billing: 31641 (Destruction of tumor by any method).\nMethod: Photodynamic Therapy (PDT).\nSite: Right Mainstem Bronchus.\nNote: No excision, no stent.",
            4: "Procedure: PDT Light Application\n1. Sedation.\n2. Scope to RMS.\n3. Visualize tumor.\n4. Insert light fiber.\n5. Treat for 20 mins.\n6. Remove scope.",
            5: "patient had the photofrin shot two days ago so we did the light today. right mainstem tumor. put the fiber in and turned the light on for 20 minutes. patient has to stay out of the sun. procedure 31641.",
            6: "Procedure: Bronchoscopy with PDT. Site: Right Mainstem. Anesthesia: Deep. Details: Light application performed on known SCC lesion. Fiber placed, treatment cycle completed. No complications.",
            7: "[Indication]\nRight mainstem SCC, PDT light phase.\n[Anesthesia]\nDeep sedation.\n[Description]\nPDT light diffuser applied to RMS lesion. Tumor destruction via photodynamic activation.\n[Plan]\nLight precautions.",
            8: "This session was for the light application phase of photodynamic therapy. After identifying the tumor in the right mainstem bronchus, we positioned the light fiber. We delivered the therapeutic light dose to activate the photosensitizer and destroy the tumor tissue.",
            9: "Endoscopic tumor ablation. We illuminated the right mainstem lesion with the PDT laser fiber to induce necrosis. No mechanical removal or stenting was required."
        },
        # Note 6: Rigid Bronchoscopy, Tumor Debulking, Stent (LMS) - CPT 31641, 31636
        6: {
            1: "Proc: Rigid Bronch, Debulk, Stent LMS.\nInd: 90% obstruction LMS.\nAction: Coring/Cryo debulking (31641). Stent 12x40mm deployed (31636).\nResult: Patent airway.\nCode: 31641, 31636.",
            2: "OPERATIVE SUMMARY: The patient underwent rigid bronchoscopy for a critical malignant obstruction of the left mainstem bronchus. Mechanical coring and cryotherapy were utilized to debulk the tumor, restoring patency. To maintain the airway, a silicone-covered self-expanding metallic stent was deployed. Post-deployment inspection showed excellent position and patency.",
            3: "Codes: 31641 (Destruction/Debulking), 31636 (Stent placement).\nSite: Left Mainstem.\nTools: Rigid scope, Cryo probe, Covered SEMS.\nMedical Necessity: Critical obstruction, post-obstructive pneumonia.",
            4: "Procedure: Rigid Bronch + Stent\n1. GA, Rigid scope.\n2. Found tumor LMS.\n3. Debulked with cryo/coring.\n4. Placed stent (12x40).\n5. Suctioned blood.\n6. Extubated.",
            5: "mr oneil needed his airway opened up. left main was blocked. we used the rigid scope. cored out the tumor and froze some of it. then put a stent in so it stays open. bleeding was okay. codes 31641 and 31636.",
            6: "Procedure: Rigid Bronchoscopy, Tumor Destruction, Stenting. Site: Left Mainstem. Method: Coring/Cryo (Destruction) + SEMS (Stent). Indication: Malignant obstruction. Outcome: Airway patent.",
            7: "[Indication]\nLMS obstruction.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\n1. Tumor debulking (coring/cryo).\n2. Stent placement (LMS).\n[Plan]\nAntibiotics.",
            8: "We performed a rigid bronchoscopy to relieve a severe obstruction in the left mainstem bronchus. We utilized mechanical coring and cryotherapy to remove the tumor mass. Once the airway was sufficiently open, we placed a covered metal stent to prevent re-occlusion.",
            9: "Rigid airway intervention. We recanalized the left mainstem using mechanical destruction and cryo-ablation. Following tumor removal, we implanted a bronchial prosthesis to maintain patency."
        },
        # Note 7: Rigid Bronchoscopy, Debulking, Stent (RMS), Tunneled Pleural Catheter - CPT 31641, 31636, 32550
        7: {
            1: "Proc: Rigid Bronch RMS (Debulk+Stent) + PleurX Rt Hemithorax.\nActions:\n- APC/Coring RMS (31641).\n- Stent RMS (31636).\n- IPC insertion Rt chest (32550).\nResult: Airway open, fluid drained.",
            2: "OPERATIVE NOTE: This was a combined airway and pleural procedure. Rigid bronchoscopy was performed to address a right mainstem obstruction; tumor was destroyed via APC and coring, followed by stent placement. Subsequently, the patient was repositioned, and an indwelling tunneled pleural catheter was inserted into the right hemithorax under ultrasound guidance for management of malignant effusion.",
            3: "Billing Codes:\n- 31641: Bronchoscopic tumor destruction (RMS).\n- 31636: Bronchial stent placement (RMS).\n- 32550: Tunneled pleural catheter insertion (Right).\nNote: Distinct procedures (Airway vs Pleura).",
            4: "Procedure: Rigid Bronch + Stent + PleurX\n1. Airway part: Debulked RMS, placed stent.\n2. Repositioned patient.\n3. Pleural part: US guidance, placed PleurX catheter right side.\n4. Drained 1.7L.",
            5: "sheryl lyons had a blocked airway and fluid on the lung. we fixed the airway first with the rigid scope apc and a stent in the right main. then we put in a pleurx catheter on the right side for the fluid. drained a lot. shes breathing better now.",
            6: "Procedure: Rigid Bronchoscopy (Debulk/Stent) & IPC Insertion. Sites: RMS & Right Pleura. Anesthesia: GA. Details: RMS opened via APC/Coring and stented. PleurX catheter placed in right chest under US guidance. No complications.",
            7: "[Indication]\nRMS obstruction, Recurrent effusion.\n[Anesthesia]\nGeneral.\n[Description]\n1. Tumor destruction RMS.\n2. Stent RMS.\n3. Tunneled pleural catheter insertion.\n[Plan]\nHome drainage.",
            8: "We addressed both the airway obstruction and the pleural effusion. Using rigid bronchoscopy, we destroyed the tumor in the right mainstem and placed a stent. We then inserted a tunneled pleural catheter on the right side to allow for outpatient fluid drainage.",
            9: "Dual intervention. We ablated the tumor in the right main bronchus and deployed a stent. Afterwards, we implanted a tunneled drain into the right pleural space to manage the recurrence of fluid."
        },
        # Note 8: Flexible Bronchoscopy with BAL (RLL) - CPT 31624
        8: {
            1: "Indication: RLL pneumonia.\nProc: Flex Bronch + BAL.\nSite: RLL superior segment.\nAction: Lavage 120ml.\nNo biopsy.\nCode: 31624.",
            2: "PROCEDURE: Diagnostic flexible bronchoscopy was performed to evaluate nonresolving pulmonary infiltrates in this immunocompromised host. The scope was wedged in the superior segment of the right lower lobe. Bronchoalveolar lavage was performed with sterile saline. The return was collected and submitted for comprehensive microbiology and cytology.",
            3: "Code: 31624 (Bronchoscopy with BAL).\nLocation: RLL.\nJustification: Diagnostic wash for culture/cytology. No tissue biopsy performed.",
            4: "Procedure: Bronch + BAL\n1. Moderate sedation.\n2. Scope to RLL.\n3. Wedged in superior seg.\n4. BAL performed (120cc in, 70cc out).\n5. Sent for cultures.",
            5: "robert jensen has pneumonia that wont go away. did a bronch with bal in the right lower lobe. lung looked clear otherwise. sent the fluid for everything viral fungal bacterial. hopefully we get an answer.",
            6: "Procedure: Bronchoscopy with BAL. Site: RLL. Indication: Pneumonia. Details: 120 mL saline instilled, adequate return. Specimens sent to lab. No biopsy.",
            7: "[Indication]\nNonresolving pneumonia.\n[Anesthesia]\nModerate.\n[Description]\nBronchoalveolar lavage of RLL.\n[Plan]\nWait for cultures.",
            8: "We performed a flexible bronchoscopy to investigate the right lower lobe infiltrate. We performed a bronchoalveolar lavage in the affected segment. The fluid was collected and sent for analysis to identify any infectious pathogens.",
            9: "Diagnostic lavage. We navigated to the right lower lobe and performed a washout of the alveolar space. The effluent was harvested for microbiological testing."
        },
        # Note 9: Ultrasound-guided Tunneled Pleural Catheter insertion - CPT 32550
        9: {
            1: "Ind: Recurrent pleural effusion.\nProc: US-guided PleurX insertion.\nSite: Left hemithorax.\nAction: Seldinger technique, tunneled, cuff buried.\nOutput: 1.5L.\nCode: 32550.",
            2: "OPERATIVE NOTE: The patient presented for management of refractory hepatic hydrothorax. Under ultrasound guidance, a tunneled indwelling pleural catheter was inserted into the left pleural space. The subcutaneous tunnel was created, the polyester cuff positioned appropriately, and the catheter was secured. Spontaneous drainage was observed.",
            3: "Code: 32550 (Insertion of tunneled pleural catheter).\nGuidance: Ultrasound.\nSite: Left.\nNote: PleurX catheter placed for chronic drainage. No pleurodesis.",
            4: "Procedure: IPC Placement\n1. US check: Fluid yes.\n2. Lidocaine.\n3. Needle, wire, tunnel.\n4. Pull catheter through tunnel.\n5. Insert into chest.\n6. Drain fluid.\n7. Stitch up.",
            5: "aisha khan needs a drain for her fluid. put in a pleurx catheter on the left side using the ultrasound. tunneled it under the skin so it stays in. drained about a liter and a half. discharge home with nurse.",
            6: "Procedure: Tunneled Pleural Catheter Insertion. Site: Left Chest. Guidance: Ultrasound. Device: PleurX. Details: Standard tunneling technique. Cuff secured. 1.5L drained. No complications.",
            7: "[Indication]\nRecurrent effusion.\n[Anesthesia]\nLocal/Moderate.\n[Description]\nInsertion of tunneled pleural catheter (PleurX) left side.\n[Plan]\nHome drainage.",
            8: "We placed a tunneled indwelling pleural catheter to manage the recurrent fluid in the left chest. Using ultrasound for safety, we created a subcutaneous tunnel and inserted the catheter into the pleural space. The cuff was seated in the tunnel to prevent infection and dislodgement.",
            9: "Implantation of chronic pleural drain. Under sonographic visualization, we inserted a tunneled catheter into the left hemithorax. The device was secured for long-term intermittent drainage."
        }
    }
    return variations

def main():
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
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Loop through the 10 source notes
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Generate 9 variations for each note
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # 1. Update Note Text
            note_entry["note_text"] = variations_text[idx][style_num]
            
            # 2. Update Demographics (Name, Age, Date)
            new_name = record['names'][style_num - 1]
            new_age = orig_age + random.randint(-3, 3)
            rand_date_obj = generate_random_date(2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # 3. Update Registry Entry
            if "registry_entry" in note_entry:
                reg = note_entry["registry_entry"]
                reg["patient_age"] = new_age
                reg["procedure_date"] = rand_date_str
                
                # Update MRN to be unique
                if "patient_mrn" in reg:
                    reg["patient_mrn"] = f"{reg['patient_mrn']}_syn_{style_num}"
                
                # Update Evidence snippet (if present) to reflect changes
                if "evidence" in reg and isinstance(reg["evidence"], dict):
                    reg["evidence"]["procedure_date"] = f"PROCEDURE DATE: {rand_date_str}"
                    reg["evidence"]["patient_age"] = f"{new_age}-year-old {reg['gender'].lower()} patient"
                    # Note: We can't easily regex replace the name in the text evidence snippet 
                    # without more complex logic, but the metadata is key here.

            # 4. Add Synthetic Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    output_path = output_dir / OUTPUT_FILENAME
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} notes in {output_path}")

if __name__ == "__main__":
    main()