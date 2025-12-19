import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_095.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILE = "synthetic_bronch_biopsy_notes_part_095.json"

def generate_random_date(start_year, end_year):
    """Generates a random date within the given year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations.
    Keys: Original Note Index (0-9)
    Values: Dictionary of Style Index (1-9) -> Text Content
    """
    variations = {
        0: { # William Harrison - RUL Mass Biopsy
            1: "Procedure: Bronchoscopy w/ EBBx\nTarget: RUL mass (RB1).\nAction: Scope passed. Exophytic mass ID'd. 4 biopsies taken with cold forceps. Moderate bleeding -> Cold saline. Hemostasis achieved.\nPlan: Path f/u.",
            2: "OPERATIVE REPORT: The patient was brought to the bronchoscopy suite for evaluation of a right upper lobe endobronchial abnormality suggestive of neoplasia. Upon endoscopic visualization, a polypoid, friable tissue mass was observed nearly obstructing the RB1 segment. Utilizing standard cold forceps, four biopsies were procured to ensure adequate histopathologic characterization. Hemostasis was secured via lavage with cold saline.",
            3: "CPT 31625: Bronchoscopy with endobronchial biopsy.\nProcedure Note: Flexible bronchoscope introduced. Anatomical inspection revealed 6.0mm scope used to access RUL. A specific lesion at the RB1 orifice was identified. Forceps were utilized to obtain 4 distinct tissue samples (endobronchial biopsies). Bleeding was managed with cold saline irrigation. No additional fluoroscopy or needle aspiration required.",
            4: "Procedure Note\nResident: Dr. Chen\nPatient: William Harrison\nIndication: RUL Mass\nSteps:\n1. Moderate sedation initiated.\n2. Scope inserted orally.\n3. Airway inspection: Mass at RB1.\n4. Biopsy: 4 samples taken from RUL mass.\n5. Hemostasis: Cold saline used.\n6. Scope withdrawn.\nPlan: Follow pathology.",
            5: "pt is william harrison here for bronchoscopy found that rul mass looked like cancer red and friable at rb1 took four biopsies bleeding was moderate so we used cold saline to stop it washings sent too patient did fine going home 5 days for path results.",
            6: "Under moderate sedation, a flexible bronchoscope was introduced. The airways were inspected. A pink-red, friable, exophytic mass was identified at the RB1 orifice, causing near-complete occlusion. Four endobronchial biopsies were obtained using cold forceps. Moderate bleeding occurred and was controlled with cold saline irrigation. Bronchial washings were collected. The patient tolerated the procedure well.",
            7: "[Indication]\nRUL endobronchial mass on CT, suspected malignancy.\n[Anesthesia]\nModerate sedation (Midazolam/Fentanyl).\n[Description]\nScope inserted. Exophytic mass found at RB1. 4 biopsies taken. Bleeding controlled with cold saline.\n[Plan]\nDischarge home. Pathology follow-up.",
            8: "The patient, Mr. Harrison, presented for a bronchoscopy due to a suspected RUL mass. After achieving moderate sedation, we advanced the scope and identified a polypoid mass occluding the RB1 segment. We proceeded to take four biopsies using cold forceps. There was some moderate bleeding, which we successfully managed with cold saline. The patient remained stable throughout.",
            9: "Diagnosed RUL endobronchial mass. Performed bronchoscopy with sampling. Under sedation, inspected airways. Spotted exophytic mass at RB1. Harvested 4 tissue samples with forceps. Controlled hemorrhage with saline. Collected washings. Patient tolerated intervention."
        },
        1: { # Sofia Martinez - Sarcoidosis (Biopsy + BAL)
            1: "Dx: Sarcoidosis susp.\nProc: EBBx x6, BAL RML.\nFindings: Cobblestoning main carina/mainstems.\nAction: Biopsies taken (Carina, RMS, LMS). BAL RML 100mL instilled, 55mL return.\nComplications: None.",
            2: "PROCEDURE: Fiberoptic bronchoscopy with endobronchial biopsy and bronchoalveolar lavage.\nFINDINGS: The bronchial mucosa exhibited diffuse nodularity and a 'cobblestone' appearance characteristic of granulomatous disease, particularly at the carina and mainstem bronchi. Six biopsies were harvested from these sites. Subsequently, a bronchoalveolar lavage was conducted in the right middle lobe yielding clear fluid.\nIMPRESSION: Findings consistent with sarcoidosis.",
            3: "Code Selection:\n- 31625: Endobronchial biopsies (multiple sites: Carina, RMS, LMS).\n- 31624: Bronchoalveolar lavage (RML).\nJustification: Biopsies taken from central airways for tissue diagnosis. Lavage performed in a separate lobe (RML) for cellular differential. Modifier XS/59 applicable due to separate sites.",
            4: "Resident Procedure Note\nPatient: S. Martinez\nSteps:\n1. Scope passed. Mucosa looked like cobblestones.\n2. Biopsies taken: 3 from carina, 2 RMS, 1 LMS.\n3. BAL done in RML. 100cc in, 55cc out.\n4. Patient tolerated well.\nPlan: Clinic f/u 2 weeks.",
            5: "sofia martinez bronchoscopy for sarcoidosis suspicion saw cobblestoning everywhere typical sarcoid look took 6 biopsies total from carina and mainstems bleeding was minimal also did a bal in the rml clear fluid back patient fine sending home.",
            6: "Moderate sedation was achieved. The scope was advanced, revealing diffuse mucosal nodularity and cobblestoning at the main carina and bilateral mainstem bronchi. Six endobronchial biopsies were obtained from the carina, RMS, and LMS. A BAL was performed in the RML with 55mL return. The procedure was uncomplicated.",
            7: "[Indication]\nBilateral hilar adenopathy, rule out sarcoidosis.\n[Anesthesia]\nModerate sedation.\n[Description]\nCobblestone mucosa observed. 6 Endobronchial biopsies obtained. BAL performed in RML. Minimal bleeding.\n[Plan]\nOutpatient follow-up. PFTs pending pathology.",
            8: "Ms. Martinez underwent a bronchoscopy to investigate suspected sarcoidosis. We observed the classic cobblestone appearance of the mucosa in the central airways. To confirm the diagnosis, we took six biopsies from the carina and mainstem bronchi. We also performed a lavage in the right middle lobe. She tolerated the procedure well with minimal bleeding.",
            9: "Evaluation for sarcoidosis. Executed bronchoscopy with tissue sampling and lavage. Noted mucosal irregularities. Harvested 6 specimens from central airways. Performed washing of RML. No obstructions noted."
        },
        2: { # Marcus Thompson - LLL Recurrence + APC
            1: "Indication: LLL lesion, ?recurrence.\nFindings: Polypoid lesion LB6, 50% obstructed. Necrotic.\nProcedure: 5 biopsies taken. APC (40W) used for hemostasis.\nDisp: Home. Onc f/u.",
            2: "OPERATIVE SUMMARY: The patient, with a history of NSCLC, presented with a new LLL lesion. Bronchoscopy revealed a necrotic, polypoid mass partially obstructing the LB6 orifice. Five biopsy specimens were obtained for histopathologic and molecular analysis. Hemostasis was achieved utilizing Argon Plasma Coagulation (APC) applied to the biopsy bed.",
            3: "CPT 31625 (Biopsy). Note on APC: Argon Plasma Coagulation was utilized solely for control of procedure-induced hemorrhage (hemostasis), not for tumor destruction. Therefore, CPT 31641 is not reported. Service billed is biopsy of the LLL lesion.",
            4: "Fellow Note\nPt: M. Thompson\nProcedure: Bronch w/ Biopsy\n1. LMA placed.\n2. Scope to LLL.\n3. Lesion at LB6 biopsied x5.\n4. Bleeding noted -> APC applied for control.\n5. Extubated stable.",
            5: "marcus thompson biopsy of lll mass looks like recurrence necrotic tissue at lb6 took 5 samples started bleeding a bit so we used the apc to burn it stop the bleeding airway open enough extubated fine.",
            6: "General anesthesia was administered via LMA. A therapeutic scope was used to identify a polypoid, necrotic lesion at the LB6 origin causing 50% obstruction. Five biopsies were taken. Moderate bleeding necessitated the use of APC (40W) for hemostasis. The patient was extubated and recovered in PACU.",
            7: "[Indication]\nSuspected NSCLC recurrence, LLL lesion.\n[Anesthesia]\nGeneral (LMA).\n[Description]\nLB6 mass biopsied 5 times. Moderate bleeding controlled with APC. Airway patent.\n[Plan]\nOncology follow-up.",
            8: "Mr. Thompson underwent a bronchoscopy to evaluate a suspicious lesion in his left lower lobe. We found a necrotic mass blocking about half of the LB6 segment. We took five biopsy samples. Because of moderate bleeding afterwards, we used Argon Plasma Coagulation to cauterize the area and stop the bleeding. He is discharged to follow up with oncology.",
            9: "Assessment of LLL mass. Conducted bronchoscopy with sampling. Identified necrotic blockage at LB6. Collected 5 tissue specimens. Applied thermal energy (APC) for coagulation. Extubated successfully."
        },
        3: { # Kathleen O'Brien - RML Hemoptysis
            1: "Indication: Hemoptysis.\nFindings: RB4 sessile lesion, clot removed.\nAction: 3 biopsies taken. Bleeding controlled w/ ice saline/epi.\nStatus: Hemostasis confirmed.",
            2: "PROCEDURE: Bronchoscopic evaluation for hemoptysis. An 8mm sessile, erythematous lesion was visualized at the RB4 orifice after removal of an overlying coagulum. Three endobronchial biopsies were performed. The resultant brisk hemorrhage was managed successfully with the instillation of cold saline and topical epinephrine 1:10,000.",
            3: "Billing Rationale: 31625 (Biopsy). Procedure included suctioning of blood/clot to visualize the lesion (incidental) and biopsy of the RB4 lesion. Hemostasis achieved via pharmacological agents (epi) and cold saline. No separate control of bleed code applicable.",
            4: "Procedure: Bronchoscopy\nPatient: K. O'Brien\nSteps:\n1. Nasal approach.\n2. Suctioned clot from RML.\n3. Saw lesion at RB4.\n4. Biopsied x3.\n5. Brisk bleeding -> Epi/Ice saline used.\n6. Bleeding stopped.",
            5: "kathleen o'brien hemoptysis check went in through nose saw blood in rml sucked out a clot found a raised red lesion at rb4 took 3 biopsies it bled pretty good used ice saline and epi stopped eventually no bleeding at end.",
            6: "Moderate sedation was used. The scope was introduced nasally. Blood-tinged secretions and a clot were cleared from the RML, revealing an 8mm sessile lesion at RB4. Three biopsies were taken. Brisk bleeding was controlled with ice saline and epinephrine. The airways were otherwise normal.",
            7: "[Indication]\nRecurrent hemoptysis, RML lesion.\n[Anesthesia]\nModerate sedation.\n[Description]\nClot removed from RB4. Underlying lesion biopsied x3. Bleeding controlled with Epi/Saline.\n[Plan]\nPathology pending. Return precautions.",
            8: "Ms. O'Brien came in for hemoptysis. During the bronchoscopy, we cleared a clot from the right middle lobe and found a reddish lesion underneath. We took three biopsies. This caused some brisk bleeding, but we controlled it effectively with ice saline and epinephrine. She is stable with no further bleeding.",
            9: "Investigation of hemoptysis. Performed nasal bronchoscopy. Cleared coagulum. Sampled sessile lesion at RB4. Managed hemorrhage with vasoconstrictors and cryo-fluid. Hemostasis verified."
        },
        4: { # Tran Nguyen - KS
            1: "Dx: HIV, KS.\nFindings: Violaceous plaques Trachea, RMS, LMS.\nProcedure: Biopsies RMS x2, LMS x2. BAL LLL.\nPlan: ART optimization.",
            2: "CLINICAL SUMMARY: Patient with HIV (CD4 120) and suspected pulmonary Kaposi sarcoma. Endoscopic examination revealed multiple characteristic violaceous, raised plaques distributed throughout the trachea and mainstem bronchi. Diagnostic biopsies were obtained from the right and left mainstems. A bronchial wash was performed in the LLL to rule out opportunistic infection (PCP).",
            3: "Coding: 31625 (Biopsy). Multiple biopsies taken from separate sites (RMS, LMS) map to single CPT 31625. 31622 (Wash) is bundled. Indication is diagnosis of endobronchial lesions in immunocompromised host.",
            4: "Resident Note\nPt: T. Nguyen\nFindings: Purple lesions everywhere (Trachea, RMS, LMS).\nAction:\n- Biopsy RMS x2\n- Biopsy LMS x2\n- Wash LLL (PCP check)\n bleeding mild.",
            5: "tran nguyen hiv positive checking for ks saw purple spots all over trachea and mainstems took biopsies from right and left sides also washed the lll for pcp check bleeding wasn't bad oncology and id to follow up.",
            6: "Moderate sedation with propofol was used. Multiple violaceous raised plaques consistent with Kaposi sarcoma were noted in the trachea and bilateral mainstems. Biopsies were taken from the RMS and LMS. A bronchial wash was performed in the LLL. The patient tolerated the procedure well.",
            7: "[Indication]\nHIV+, pulmonary lesions.\n[Anesthesia]\nPropofol infusion.\n[Description]\nViolaceous plaques identified. Biopsies: RMS, LMS. Wash: LLL. Minimal bleeding.\n[Plan]\nID/Oncology follow-up. ART optimization.",
            8: "Mr. Nguyen underwent a bronchoscopy due to his history of HIV and lung lesions. We saw purple plaques typical of Kaposi sarcoma in his windpipe and main airways. We biopsied lesions on both the right and left sides and did a wash in the lower lung to check for infections. He is discharged to follow up with his specialists.",
            9: "Assessment for Kaposi sarcoma. Executed bronchoscopy. Observed violaceous plaques. Sampled tissue from bilateral mainstems. Lavaged LLL for infectious etiology. Minimal hemorrhage."
        },
        5: { # Robert Davis - Tracheal Mass (Rigid)
            1: "Procedure: Rigid Bronchoscopy.\nIndication: Tracheal mass, stridor.\nFindings: Post. trachea mass 2cm above carina, 70% occlusion.\nAction: 4 biopsies w/ rigid forceps.\nPlan: Await path, potential debulking.",
            2: "OPERATIVE REPORT: The patient was placed under general anesthesia with jet ventilation. A 12mm Karl Storz rigid bronchoscope was introduced. A large, well-vascularized, pedunculated mass was visualized on the posterior tracheal wall, significantly obstructing the airway. Four biopsies were obtained using rigid cup forceps. Hemostasis was achieved via direct pressure and suction.",
            3: "Billing Code: 31625 (Biopsy). Note: Technique used was RIGID bronchoscopy (compatible with 31625). No debulking or excision (31640/31641) performed at this session; procedure limited to diagnostic biopsy of tracheal mass.",
            4: "Fellow Note\nPt: R. Davis\nProc: Rigid Bronch\n1. Rigid scope inserted.\n2. Mass seen in trachea (70% blockage).\n3. Biopsied x4 with cup forceps.\n4. Bleeding controlled with pressure.\n5. Intubated for transport to PACU.",
            5: "robert davis rigid bronch for tracheal mass stridor mass is huge 70 percent block above carina took 4 biopsies with the big forceps bled a moderate amount used pressure to stop it kept him intubated for now pending path results.",
            6: "General anesthesia and jet ventilation were utilized. A 12mm rigid bronchoscope was inserted. A large pedunculated mass on the posterior trachea was identified, causing 70% obstruction. Four biopsies were taken. Moderate bleeding was controlled with pressure. The patient was intubated and transferred to the PACU.",
            7: "[Indication]\nTracheal mass, stridor.\n[Anesthesia]\nGeneral, Jet Ventilation.\n[Description]\nRigid scope used. 70% tracheal obstruction. 4 biopsies taken. Bleeding controlled.\n[Plan]\nAdmit to stepdown. Potential debulking later.",
            8: "Mr. Davis required a rigid bronchoscopy for a large mass in his trachea causing breathing difficulty. Using a rigid scope under general anesthesia, we found the mass blocking about 70% of the airway. We took four biopsy samples. We controlled the bleeding with pressure and decided to wait for results before removing the mass. He remains intubated for safety.",
            9: "Intervention for tracheal obstruction. Performed rigid endoscopy. Identified pedunculated tumor. Sampled 4 areas with rigid forceps. Managed hemorrhage with compression. Patient remains intubated."
        },
        6: { # Linda Anderson - RUL Mass + ROSE
            1: "Indication: RUL mass (PET+).\nFindings: RB1 mucosal invasion.\nAction: 5 biopsies, 1 brush.\nROSE: Suspicious for malignancy.\nPlan: Tumor board.",
            2: "PROCEDURE: Flexible bronchoscopy with rapid on-site evaluation (ROSE). The RUL apical segment revealed extrinsic compression with mucosal irregularities suggestive of invasion. Five biopsy specimens and a protected brush sample were obtained. ROSE preliminary interpretation demonstrated atypical cells consistent with malignancy.",
            3: "CPT Coding: 31625 (Biopsy). 31623 (Brushing) is not separately reportable when performed at the same site (RB1) as the biopsy. Service encompasses the diagnostic sampling of the RUL lesion.",
            4: "Procedure: Bronchoscopy\nPt: L. Anderson\n1. Scope to RUL.\n2. RB1 looks irregular/invaded.\n3. Biopsy x5.\n4. Brush x1.\n5. ROSE: Positive for cancer cells.\nPlan: Oncology referral.",
            5: "linda anderson rul mass on pet scan went in and saw rb1 looking bad mucosa irregular took 5 biopsies and a brush rose guy said it looks like cancer no bleeding going to tumor board.",
            6: "Moderate sedation was used. The RUL apical segment (RB1) showed mucosal invasion and extrinsic compression. Five endobronchial biopsies and a brush specimen were obtained. ROSE confirmed atypical cells suspicious for malignancy. The patient was discharged home.",
            7: "[Indication]\nRUL mass, PET positive.\n[Anesthesia]\nModerate.\n[Description]\nRB1 mucosal invasion noted. 5 Biopsies + Brush taken. ROSE positive.\n[Plan]\nTumor board. Oncology referral.",
            8: "Ms. Anderson underwent bronchoscopy for a PET-positive mass in the right upper lobe. We saw irregular tissue invading the airway at RB1. We took five biopsies and a brush sample. The pathologist in the room confirmed suspicious cells immediately. We will discuss her case at the tumor board.",
            9: "Diagnostic evaluation of RUL mass. Performed endoscopy. Noted luminal invasion at RB1. Sampled tissue via forceps and brush. ROSE indicated malignancy. Referred to oncology."
        },
        7: { # James Wilson - Lung Transplant
            1: "Indication: Post-transplant surveillance.\nFindings: Anastomotic granulation/polyps.\nAction: EBBx anastomoses. TBBx RLL/LLL. BAL RML.\nPlan: Transplant clinic.",
            2: "PROCEDURE: Surveillance bronchoscopy in a post-lung transplant recipient. Anastomotic evaluation revealed granulation tissue at the RMS and LMS. Endobronchial biopsies were performed. Transbronchial biopsies were obtained from the RLL and LLL to assess for rejection. A bronchoalveolar lavage was conducted in the RML.",
            3: "Coding: 31628 (TBBx RLL), 31632 (TBBx LLL), 31625-XS (EBBx Anastomosis), 31624-XS (BAL RML). Procedure involved distinct techniques (forceps vs TBBx) and distinct locations (Anastomosis vs lobes vs lavage site).",
            4: "Resident Note\nPt: J. Wilson (Txp pt)\n1. ETT/GA.\n2. Checked anastomoses: Granulation tissue biopsied.\n3. TBBx: RLL x4, LLL x4.\n4. BAL: RML.\n5. Minimal bleeding.",
            5: "james wilson lung transplant checkup saw some granulation at the hookups took biopsies of that then did the transbronchial biopsies in rll and lll for rejection check and a bal in rml bleeding was fine continue meds.",
            6: "General anesthesia via ETT was used. Bilateral anastomoses showed granulation tissue and polyps; biopsies were taken. Transbronchial biopsies were obtained from the RLL and LLL. A BAL was performed in the RML. The patient tolerated the procedure well.",
            7: "[Indication]\nPost-transplant surveillance.\n[Anesthesia]\nGeneral.\n[Description]\nAnastomotic lesions biopsied. TBBx RLL and LLL performed. BAL RML. Minimal bleeding.\n[Plan]\nTransplant clinic follow-up.",
            8: "Mr. Wilson had his routine post-transplant bronchoscopy. We found some granulation tissue at the connection points and biopsied it. We also took deep lung biopsies from the lower lobes to check for rejection and washed the middle lobe. He had minimal bleeding and will follow up with the transplant team.",
            9: "Surveillance of lung allograft. Examined anastomoses; sampled granulation tissue. Performed transbronchial sampling of RLL and LLL. Lavaged RML. Continued immunosuppression."
        },
        8: { # Maria Garcia - RML Stricture
            1: "Indication: Chronic cough, RML narrowing.\nFindings: RML orifice thickened, 5mm stenosis.\nAction: 4 biopsies taken.\nDx: R/O carcinoid vs inflammation.\nPlan: Path review.",
            2: "PROCEDURE: Diagnostic bronchoscopy. The RML orifice demonstrated significant circumferential mucosal thickening and edema, resulting in stenosis to approximately 5mm. No discrete mass was evident. Four biopsy specimens were obtained to differentiate between inflammatory stricture and neoplastic process (e.g., carcinoid).",
            3: "Billing: 31625 (Biopsy of RML orifice). Medical necessity supported by radiographic finding of bronchial narrowing and symptoms of cough.",
            4: "Resident Note\nPt: M. Garcia\n1. Scope to RML.\n2. Narrowing seen (5mm), red/swollen.\n3. Biopsied x4.\n4. No bleeding.\n5. Patient stable.",
            5: "maria garcia cough rml narrowing on ct went in and rml opening is tight red swollen took 4 biopsies to see what it is maybe carcinoid or just inflammation bleeding was scant patient went home.",
            6: "Moderate sedation was utilized. The RML orifice showed circumferential thickening and narrowing to 5mm. Four biopsies were obtained from the erythematous mucosa. The appearance was concerning for carcinoid or inflammatory stricture. No complications occurred.",
            7: "[Indication]\nChronic cough, RML stenosis.\n[Anesthesia]\nModerate.\n[Description]\nRML orifice narrowed/thickened. 4 Biopsies taken. No complications.\n[Plan]\nPathology follow-up.",
            8: "Ms. Garcia came in for a cough and narrowing of her airway seen on CT. We found the opening to the right middle lobe was swollen and narrowed. We took four biopsies to figure out if it's inflammation or a tumor. There was barely any bleeding, and she went home safely.",
            9: "Investigation of bronchial stenosis. Visualized RML narrowing with mucosal edema. Sampled 4 sites circumferentially. Minimal hemorrhage. Monitoring for pathology."
        },
        9: { # Charles Brown - Melanoma
            1: "Dx: Metastatic melanoma.\nFindings: Black nodules Trachea, RMS, LMS.\nAction: Biopsies x5.\nPlan: Palliative/Onc.",
            2: "PROCEDURE: Bronchoscopy for evaluation of metastatic disease. The airway examination revealed diffuse endobronchial involvement with multiple pigmented, nodular lesions characteristic of metastatic melanoma within the trachea and bilateral mainstem bronchi. Representative biopsies were secured from multiple sites.",
            3: "Code: 31625 (Biopsy). Single code covers multiple biopsies of endobronchial lesions (trachea, RMS, LMS) performed during the same session.",
            4: "Resident Note\nPt: C. Brown\nDx: Melanoma\n1. LMA/GA.\n2. Black nodules seen in trachea/bronchi.\n3. Biopsied 5 spots.\n4. Bleeding mild.\n5. Extubated.",
            5: "charles brown metastatic melanoma coughing ct showed nodules went in and saw black spots everywhere trachea mainstems took 5 biopsies to confirm bleeding mild referral to palliative and oncology.",
            6: "General anesthesia via LMA was used. Multiple pigmented nodular lesions consistent with metastatic melanoma were observed in the trachea, RMS, and LMS. Five biopsies were obtained. The airways remained patent despite the disease burden.",
            7: "[Indication]\nMetastatic melanoma, cough.\n[Anesthesia]\nGeneral (LMA).\n[Description]\nPigmented nodules in central airways. 5 Biopsies taken. Minimal bleeding.\n[Plan]\nPalliative care, Immunotherapy evaluation.",
            8: "Mr. Brown underwent bronchoscopy for metastatic melanoma. We found multiple dark, nodular lesions throughout his windpipe and main airways. We took five biopsies to confirm the diagnosis. He had mild bleeding but is otherwise stable. We are referring him to oncology and palliative care.",
            9: "Assessment of metastatic burden. Identified pigmented endobronchial nodules. Sampled lesions in trachea and mainstems. Verified metastatic melanoma visually. Referred for systemic therapy."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock names and ages to correspond with the 9 variations.
    Each index corresponds to the original note index (0-9).
    """
    # Names lists tailored for 10 distinct notes, 9 variations each
    return [
        # 0: William Harrison
        {"idx": 0, "orig_age": 64, "names": ["James Ford", "Robert Carter", "Michael Grant", "William Hayes", "David Stone", "Richard Brooks", "Thomas Wells", "Charles Cole", "Joseph Reed"]},
        # 1: Sofia Martinez
        {"idx": 1, "orig_age": 50, "names": ["Maria Lopez", "Elena Rodriguez", "Isabella Perez", "Sofia Garcia", "Gabriela Diaz", "Camila Torres", "Valentina Flores", "Martina Reyes", "Lucia Morales"]},
        # 2: Marcus Thompson
        {"idx": 2, "orig_age": 67, "names": ["Arthur King", "Edward Scott", "George Green", "Henry Baker", "Frank Adams", "Walter Nelson", "Raymond Hill", "Jack Campbell", "Dennis Mitchell"]},
        # 3: Kathleen O'Brien
        {"idx": 3, "orig_age": 56, "names": ["Mary Sullivan", "Patricia Kelly", "Jennifer Murphy", "Linda Walsh", "Barbara Quinn", "Elizabeth Kennedy", "Susan Ryan", "Margaret Lynch", "Dorothy Shea"]},
        # 4: Tran Nguyen
        {"idx": 4, "orig_age": 43, "names": ["Minh Pham", "Duc Le", "Tuan Hoang", "Khoa Vu", "Huy Dang", "Bao Bui", "Nam Vo", "Phuc Do", "Long Truong"]},
        # 5: Robert Davis
        {"idx": 5, "orig_age": 70, "names": ["Samuel Clark", "Benjamin Lewis", "Daniel Walker", "Matthew Hall", "Anthony Allen", "Mark Young", "Paul Hernandez", "Steven Wright", "Andrew King"]},
        # 6: Linda Anderson
        {"idx": 6, "orig_age": 54, "names": ["Karen White", "Nancy Martin", "Lisa Thompson", "Betty Garcia", "Helen Martinez", "Sandra Robinson", "Donna Clark", "Carol Rodriguez", "Ruth Lewis"]},
        # 7: James Wilson
        {"idx": 7, "orig_age": 62, "names": ["Kenneth Lee", "Kevin Walker", "Brian Hall", "Jason Allen", "Jeffrey Young", "Ryan Hernandez", "Gary King", "Jacob Wright", "Nicholas Lopez"]},
        # 8: Maria Garcia
        {"idx": 8, "orig_age": 47, "names": ["Ana Torres", "Rosa Flores", "Carmen Rivera", "Juana Gomez", "Teresa Diaz", "Yolanda Reyes", "Silvia Morales", "Gloria Ortega", "Martha Castillo"]},
        # 9: Charles Brown
        {"idx": 9, "orig_age": 75, "names": ["Larry Jones", "Scott Miller", "Frank Davis", "Stephen Wilson", "Eric Taylor", "Jerry Anderson", "Gregory Thomas", "Joshua Jackson", "Patrick White"]}
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
            
            # Deep copy the original note structure to preserve original extraction data
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the specific style variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (should not happen with complete data)
                note_entry["note_text"] = f"Variation {style_num} for note {idx} (Placeholder)"
            
            # Update registry_entry fields to match the new synthetic identity
            if "registry_entry" in note_entry:
                # Update demographics
                if "patient_demographics" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                
                # Update procedure date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update MRN to ensure uniqueness
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"

            # Add metadata about the synthetic generation for tracking
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "style_description": [
                    "Terse Surgeon", "Academic Attending", "Billing Coder", 
                    "Trainee/Resident", "Sloppy Dictation", "Header-less", 
                    "Templated", "Narrative Flow", "Synonym Swapper"
                ][style_num-1],
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / OUTPUT_FILE
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()