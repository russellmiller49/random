import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_040.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the specific notes in Part 040.
    Keys are the original note index (0-9).
    Values are dictionaries mapping Style ID (1-9) to the new text.
    """
    variations = {
        0: { # Thomas Jackson (EBUS Restaging, Station 7)
            1: "Indication: Restaging N2 disease post-chemo.\n- Station 7 (8mm): 4 passes, ROSE neg. PET neg.\n- 4R/4L/10R: Benign/small, not sampled.\n- Procedure well tolerated.\nImpression: Downstaged N2 disease. Adequate sampling.",
            2: "HISTORY: Mr. Jackson presented for mediastinal restaging following induction chemotherapy for N2 disease. Previous EBUS demonstrated malignant involvement of the subcarinal station.\nPROCEDURE: Under conscious sedation, the station 7 lymph node was re-evaluated. It measured 8mm, significantly reduced from 18mm. Four transbronchial needle aspirations were performed. Rapid On-Site Evaluation confirmed the presence of lymphocytes and anthracotic pigment without malignant cells. Stations 4R, 4L, and 10R were sonographically benign and not sampled.\nCONCLUSION: Significant radiographic and pathologic response to therapy.",
            3: "Procedure: Bronchoscopy with EBUS (CPT 31652 - 1-2 stations).\nTarget: Station 7.\nTechnique: Ultrasound localization of subcarinal node. 22G needle used for 4 aspirations. ROSE interpretation performed.\nAdditional Stations: 4R, 4L, 10R visualized but not sampled (supports staging code).\nOutcome: Adequate tissue, negative for malignancy.",
            4: "Procedure Note\nPatient: 71M, Post-chemo restaging.\nAttending: Dr. X\n\nSteps:\n1. Time out. Conscious sedation (Midaz/Fentanyl).\n2. EBUS scope inserted.\n3. Station 7 identified (8mm). 4 passes taken.\n4. ROSE read: Negative.\n5. Surveyed 4R, 4L, 10R - looked benign.\n6. No complications.\n\nPlan: Surgical referral.",
            5: "pt thomas jackson here for ebus restaging used midazolam and fentanyl. looked at station 7 it shrunk down to 8mm took 4 samples rose said negative just pigment. looked at 4r and 4l and 10r they looked fine didnt stick them. patient did ok no issues. impression is chemo worked good downstaging.",
            6: "Patient Thomas Jackson MRN LM-9283 DOB 04/08/1954 History Initial EBUS 4 months ago showed N2 disease station 7 Now post-chemo restaging requested CONSCIOUS SEDATION Midazolam 2mg Fentanyl 50mcg patient calm Ramsay 2 BP checked q10min continuous SpO2 monitoring EBUS RESTAGING Previously positive station 7 reassessed Station 7 Now 8mm prior 18mm 4 passes obtained ROSE Negative for malignant cells shows anthracotic pigmented macrophages PET now negative at this station Adequate sampling achieved Additional stations surveyed for complete restaging Station 4R 6mm benign appearance not sampled previously negative Station 4L No discrete nodes visualized Station 10R Small 5mm node not sampled Photodocumentation completed No complications during or after procedure INTERPRETATION Excellent response to chemotherapy with downstaging of previously malignant N2 station Adequate negative sampling obtained for surgical planning",
            7: "[Indication]\nPost-chemo restaging of N2 (Station 7) disease.\n[Anesthesia]\nConscious sedation: Midazolam/Fentanyl.\n[Description]\nStation 7 assessed: reduced to 8mm. 4 passes TBNA performed. ROSE negative. Stations 4R, 4L, 10R surveyed, appeared benign, not sampled.\n[Plan]\nProceed with surgical planning given negative staging.",
            8: "Mr. Jackson underwent EBUS restaging today to assess his response to chemotherapy. We focused on the previously positive Station 7, which has decreased in size to 8mm. We performed four needle passes, and the on-site pathologist saw no cancer cells, only benign pigmented macrophages. We also surveyed the surrounding stations like 4R and 10R, but they looked small and benign, so we didn't sample them. The procedure went smoothly without any complications.",
            9: "History: Initial EBUS 4 months ago exhibited N2 disease. Now post-chemo, restaging requested.\nEBUS RESTAGING:\nPreviously positive station 7 reassessed:\n- Station 7: Now 8mm, 4 passes acquired\n- ROSE: Negative for malignant cells\n- PET now negative at this station\nAdditional stations surveyed:\n- Station 4R: 6mm, benign appearance, not aspirated\n- Station 4L: No discrete nodes visualized\n- Station 10R: Small 5mm node, not aspirated\nINTERPRETATION: Excellent response to chemotherapy."
        },
        1: { # Richard Brown (Complex: EBUS, Stent, Nav)
            1: "Procedures: EBUS, RML Stent, LUL Nav/Biopsy.\n- EBUS: 4R, 10R, 11R sampled (malignant). 7 inaccessible.\n- RML: 80% stenosis. APC debulking. 12x30mm stent placed.\n- LUL: EM Nav to 16mm nodule. Radial EBUS +. Biopsy x3.\nComplications: Bleeding (controlled), transient hypoxia.\nPlan: ICU obs.",
            2: "OPERATIVE REPORT: The patient presented with bulky mediastinal adenopathy, central airway obstruction, and a peripheral nodule. \n1. STAGING: EBUS was performed. Station 4R (conglomerate) and 10R were sampled and ROSE confirmed malignancy. Station 7 was compressed and inaccessible.\n2. THERAPEUTIC: The RML bronchus was 80% stenosed by exophytic tumor. Argon plasma coagulation was applied for hemostasis and debulking, followed by deployment of a 12x30mm metallic stent.\n3. DIAGNOSTIC: Electromagnetic navigation targeted a 16mm LUL nodule. Radial EBUS confirmed location. Transbronchial biopsy was performed.",
            3: "Coding Data:\n- 31653: EBUS sampling of 3+ stations (4R, 10R, 11R).\n- 31631: Placement of tracheal/bronchial stent (RML).\n- 31628: Transbronchial lung biopsy (LUL nodule).\n- +31627: Navigation add-on.\n- +31654: Peripheral EBUS add-on.\nMedical Necessity: Bulky disease, symptomatic stenosis, peripheral nodule.",
            4: "Procedure: Complex Bronchoscopy\nResident: Dr. Smith\n\nSteps:\n1. GA/ETT.\n2. EBUS: Sampled 4R, 10R, 11R (Positive).\n3. RML Tumor: Debulked with APC. Stent placed (12x30mm).\n4. LUL Nodule: Navigated with EM system. Radial EBUS verification. Biopsied.\n\nEvents: Bleeding from tumor controlled with epi. Sats dropped to 85% during stenting, recovered.",
            5: "mr brown here for big case. mediastinal nodes rml blockage and lul spot. put him under GA. did the ebus first 4r 10r 11r all positive couldn't get to 7. then looked at the rml blocked 80 percent by tumor burned it with argon and put a stent in 12 by 30. then went for the lul nodule using the magnet nav system found it with radial probe took biopsies. little bit of bleeding and oxygen dropped a bit but we fixed it. icu for tonight.",
            6: "PT RICHARD BROWN ID MD-8472-K DOB 03/27/1952 MULTIFACETED CASE Bulky mediastinal disease RML stenosis LUL peripheral nodule GENERAL ANESTHESIA ETT propofol remi infusion Ramsay 6 A-line monitoring BP continuous PHASE 1 STAGING EBUS Attempted systematic evaluation challenging due to bulky disease Station 4R 28mm conglomerate mass 5 passes ROSE malignant PET molecular sent Station 7 Unable to access compressed by tumor Station 10R 11mm 3 passes ROSE malignant PET Station 11R Difficult anatomy 2 passes obtained ROSE adequate Photodoc limited by distorted anatomy PHASE 2 ENDOBRONCHIAL DISEASE RML bronchus has exophytic tumor causing 80% stenosis Biopsy 6 forceps confirmed same malignancy Argon plasma coagulation applied for debulking 12mm 30mm metallic stent placed for symptom relief PHASE 3 NAVIGATION FOR LUL NODULE EM navigation performed LUL apical posterior nodule 16mm targeted Tool in lesion confirmed radial EBUS Fluoro 5.2 min DAP 201 cGycm2 Sampling needle x2 biopsy x3 COMPLICATIONS Moderate bleeding from endobronchial tumor biopsy site controlled with epi APC Transient hypoxia to 85% during stent deployment resolved with ventilator adjustment Procedure duration 98 minutes Patient recovered well extubated ICU observation overnight",
            7: "[Indication]\nBulky mediastinal disease, RML stenosis, LUL nodule.\n[Anesthesia]\nGeneral, ETT.\n[Description]\n1. EBUS: Sampled 4R, 10R, 11R (Malignant). Station 7 compressed.\n2. RML: Tumor causing 80% stenosis. APC used. 12x30mm stent deployed.\n3. LUL: EM Navigation to 16mm nodule. Biopsies taken.\n[Plan]\nICU observation. Oncology consult.",
            8: "We performed a multi-stage procedure on Mr. Brown. First, we used EBUS to stage the mediastinum, finding malignancy in stations 4R, 10R, and 11R, though station 7 was unreachable. Next, we addressed the symptomatic RML stenosis by debulking the tumor with APC and placing a 12mm metallic stent. Finally, we used electromagnetic navigation to locate and biopsy a 16mm nodule in the left upper lobe. There was some bleeding and transient hypoxia, but both were managed successfully.",
            9: "PHASE 1 - STAGING EBUS:\n- Station 4R: 28mm conglomerate mass, 5 passes, ROSE + malignant.\n- Station 10R: 11mm, 3 passes, ROSE + malignant.\n- Station 11R: Difficult anatomy, 2 passes acquired.\nPHASE 2 - ENDOBRONCHIAL DISEASE:\nRML bronchus has exophytic tumor causing 80% stenosis. Argon plasma coagulation applied for debulking. 12mm x 30mm metallic stent deployed for symptom relief.\nPHASE 3 - NAVIGATION FOR LUL NODULE:\nEM navigation performed. LUL apical-posterior nodule 16mm targeted. Sampling: needle x2, biopsy x3."
        },
        2: { # Patricia Anderson (EBUS + Biopsy)
            1: "Indication: RUL lesion + LAD.\nEBUS: 2R, 4R (Pos), 7, 10R sampled.\nBiopsy: RUL mass, 70% obstruction. Forceps x6, Brush x2.\nComplications: Moderate bleed (Epi/Ice), transient hypoxia.\nPlan: Path pending. Possible stent later.",
            2: "CLINICAL SUMMARY: Ms. Anderson has post-obstructive pneumonia secondary to an RUL endobronchial lesion. Staging was required.\nEBUS STAGING: Systematic evaluation was performed. Stations 2R, 7, and 10R were negative/adequate on ROSE. Station 4R (13mm) was positive for malignancy.\nDIAGNOSTIC BRONCHOSCOPY: The RUL bronchus was 70% occluded by mass. Forceps biopsies and brushings were obtained. Hemostasis was achieved with epinephrine and iced saline lavage.",
            3: "Billing Codes:\n- 31653: EBUS sampling 3+ stations (2R, 4R, 7, 10R).\n- 31625: Endobronchial biopsy (RUL mass).\nNote: Brushing (31623) is bundled/not separately billed at same site.\nProcedure Note: General Anesthesia. 4R positive for malignancy.",
            4: "Procedure: EBUS + Biopsy\nPatient: 68F\nSteps:\n1. GA/ETT.\n2. EBUS: Sampled 2R, 4R, 7, 10R. 4R was malignant.\n3. White light bronch: Saw RUL mass.\n4. Biopsied mass x6 and brushed.\n5. Bleeding controlled with cold saline/epi.\nPlan: Oncology f/u.",
            5: "patricia anderson dob 2/17/57. did the bronch today for that rul mass. general anesthesia. checked the nodes first 2r 4r 7 10r. 4r looked bad and was positive on rose. others negative. then went to the mass in the rul biopsies taken with forceps and brush. bled a fair bit used epi and iced saline to stop it. sats dropped a bit but shes ok now. waiting on pathology.",
            6: "NAME PATRICIA ANDERSON ID MR-K8374 DOB 02/17/1957 INDICATION RUL endobronchial lesion causing post obstructive pneumonia mediastinal LAD ANESTHESIA General via ETT maintained on sevoflurane fentanyl Ramsay 6 Arterial line placed continuous BP SpO2 ETCO2 monitoring PART A STAGING EBUS Systematic evaluation N3 N2 N1 2R 8mm 3 passes ROSE negative for malignancy 4R 13mm 4 passes ROSE positive malignant PET molecular sent 7 9mm 3 passes ROSE negative 10R 7mm 3 passes ROSE adequate Photodoc of all accessible stations completed PART B TUMOR BIOPSY RUL endobronchial mass causing 70% luminal narrowing Multiple forceps biopsies obtained 6 Brush cytology 2 Moderate bleeding controlled with epi 1 20 000 iced saline COMPLICATIONS Transient hypoxia to 88% during tumor manipulation resolved with increased FiO2 and suctioning Moderate bleeding as noted controlled intraprocedurally PLAN Awaiting path for treatment planning May need repeat bronch for stent if airway compromise worsens",
            7: "[Indication]\nRUL endobronchial lesion, mediastinal lymphadenopathy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS performed: 2R, 7, 10R negative. 4R positive. RUL mass biopsied (forceps/brush). Moderate bleeding controlled.\n[Plan]\nTreatment planning based on pathology.",
            8: "We performed a staging EBUS and tumor biopsy on Ms. Anderson. Using the EBUS scope, we systematically sampled stations 2R, 4R, 7, and 10R. Unfortunately, station 4R confirmed malignancy on the rapid onsite eval. We then switched to the standard scope to biopsy the RUL mass causing the obstruction. We took multiple samples and a brush. There was some moderate bleeding which we controlled with epinephrine and iced saline.",
            9: "PART A - STAGING EBUS:\nSystematic evaluation N3-N2-N1\n- 2R (8mm): 3 passes, ROSE negative for malignancy\n- 4R (13mm): 4 passes, ROSE positive malignant\n- 7 (9mm): 3 passes, ROSE negative\n- 10R (7mm): 3 passes, ROSE adequate\nPART B - TUMOR BIOPSY:\nRUL endobronchial mass causing 70% luminal narrowing. Multiple forceps samples obtained x6. Brush cytology x2."
        },
        3: { # Christopher Moore (SCLC EBUS)
            1: "Dx: SCLC staging.\nEBUS: 2R, 4R, 4L, 7, 10R, 10L, 11R evaluated.\nSampled: 7 (Malignant), 4R (SCLC), 4L (Malignant), 10R (Atypical).\nFindings: Extensive N2/N3 disease.\nPlan: Oncology.",
            2: "PROCEDURE: Endobronchial Ultrasound Staging.\nFINDINGS: Extensive mediastinal adenopathy was noted. Station 7 was markedly enlarged (42mm) and heterogeneous. Station 4R (31mm) and 4L (24mm) were also enlarged.\nSAMPLING: Transbronchial needle aspiration was performed on Stations 7, 4R, 4L, and 10R. ROSE confirmed small cell carcinoma in 7 and 4R, with malignant cells in 4L.\nIMPRESSION: Clinical Stage N3 Small Cell Lung Cancer.",
            3: "Service: Bronchoscopy w/ EBUS sampling 3+ stations (31653).\nStations Sampled: 7, 4R, 4L, 10R.\nStations Viewed: 2R, 10L, 11R.\nPathology: Cytology sent for all. ROSE confirmation of SCLC.\nMedical Necessity: Staging of SCLC with enlarged nodes on CT.",
            4: "Procedure: EBUS TBNA\nPatient: 72M\nSteps:\n1. GA/ETT.\n2. Examined stations 2R, 4R, 4L, 7, 10R/L, 11R.\n3. Needled 7, 4R, 4L, 10R.\n4. ROSE said SCLC for 7 and 4R.\n5. No complications.\nPlan: Chemo/Rad.",
            5: "Christoper Moore 72M here for SCLC staging. Used the pentax ebus scope. found huge nodes everywhere especially station 7 was 42mm. stuck 7 4r 4l and 10r. rose guy said its small cell for sure. extensive disease n2 n3. patient woke up fine.",
            6: "Patient Moore Christopher ID MR4729384 Age 72 M Service Date 03/05/2025 Start Time 0745 Physician Dr Patel Anjali Attending Dr Kim Susan Fellow Endobronchial Ultrasound Bronchoscopy Indication Small cell lung cancer staging enlarged mediastinal lymph nodes on imaging Pre op diagnosis Small cell lung cancer clinical stage Post op diagnosis Pending final pathology Anesthesia General anesthesia provided by anesthesia team Dr Martinez Equipment Pentax EB 1970UK linear EBUS scope Procedure narrative After successful intubation and adequate depth of anesthesia timeout performed EBUS bronchoscope inserted via ETT Initial inspection showed normal trachea sharp carina Systematic ultrasound examination Lymph node stations evaluated 2R 11mm normal echogenicity 4R 31mm ENLARGED loss of normal architecture 4L 24mm ENLARGED hypoechoic 7 42mm MARKEDLY ENLARGED heterogeneous 10R 18mm prominent 10L 16mm prominent 11R 21mm abnormal appearance TBNA sampling Station 7 42mm Needle 22G Pass 1 0758 visible tissue core Pass 2 0801 additional sample Pass 3 0803 for molecular studies Pass 4 0805 microbiology ROSE Result MALIGNANT small cell morphology identified Station 4R 31mm 3 passes performed ROSE Small cell carcinoma confirmed Station 4L 24mm 3 passes performed ROSE Malignant cells present Station 10R 18mm 2 passes performed ROSE Atypical cells Procedure completed 0822 Total time 37 minutes EBL 5mL Patient extubated to recovery in stable condition Preliminary findings Extensive N2 N3 disease confirmed Specimens to pathology Cytology cell block molecular testing Patient counseled post procedure regarding findings Next steps Oncology consult PET CT for full staging Signed Dr Anjali Patel MD FCCP Time 03/05/2025 09:15",
            7: "[Indication]\nSCLC staging, mediastinal LAD.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS exam of stations 2R, 4R, 4L, 7, 10R/L, 11R. TBNA performed on 7, 4R, 4L, 10R. ROSE confirmed SCLC in 7 and 4R. Extensive nodal involvement noted.\n[Plan]\nOncology consult, PET-CT.",
            8: "Mr. Moore came in for staging of his small cell lung cancer. Under general anesthesia, we performed a systematic EBUS. We found markedly enlarged nodes, particularly at station 7 which was over 4cm. We sampled station 7, as well as 4R, 4L, and 10R. The rapid onsite evaluation confirmed small cell carcinoma. This confirms extensive N2/N3 disease.",
            9: "Lymph node stations evaluated: 2R, 4R, 4L, 7, 10R, 10L, 11R.\nTBNA sampling:\nStation 7 (42mm) Needle: 22G. ROSE Result: MALIGNANT, small cell morphology identified.\nStation 4R (31mm): 3 passes performed. ROSE: Small cell carcinoma confirmed.\nStation 4L (24mm): 3 passes performed. ROSE: Malignant cells present.\nStation 10R (18mm): 2 passes performed. ROSE: Atypical cells."
        },
        4: { # Christopher Moore (Duplicate content in JSON)
            # Since the content is technically a duplicate in the source but represents a distinct index,
            # I will provide distinct variations assuming it might be a different patient record 
            # or simply a re-run. I'll maintain the specific medical facts (SCLC, 42mm Stn 7).
            1: "Dx: SCLC.\nProcedure: EBUS-TBNA.\nNodes: 7 (42mm), 4R (31mm), 4L, 10R sampled.\nROSE: Malignant (SCLC).\nOutcome: Stable.",
            2: "INDICATIONS: Staging of suspected small cell lung cancer.\nPROCEDURE: EBUS-TBNA. A comprehensive mediastinal survey identified pathologically enlarged lymph nodes at stations 7, 4R, and 4L. Transbronchial needle aspiration confirmed small cell carcinoma via ROSE.\nCONCLUSION: Advanced stage disease.",
            3: "CPT 31653 (EBUS 3+ stations).\nStations: 7, 4R, 4L, 10R sampled.\nPathology: Positive for malignancy.\nNotes: 22G needle used. No complications.",
            4: "Resident Note\nCase: EBUS Staging\nPt: 72M\nFindings: Huge subcarinal node (42mm). Sampled 7, 4R, 4L, 10R.\nPath: SCLC confirmed on site.\nPlan: Oncology.",
            5: "ebus for mr moore. big nodes. station 7 is massive. sampled 7 4r 4l 10r. positive for small cell. no bleeding. done.",
            6: "EBUS BRONCHOSCOPY Indication Small cell lung cancer staging enlarged mediastinal lymph nodes on imaging Pre op diagnosis Small cell lung cancer clinical stage Post op diagnosis Pending final pathology Anesthesia General anesthesia provided by anesthesia team Dr Martinez Equipment Pentax EB 1970UK linear EBUS scope Procedure narrative After successful intubation and adequate depth of anesthesia timeout performed EBUS bronchoscope inserted via ETT Initial inspection showed normal trachea sharp carina Systematic ultrasound examination Lymph node stations evaluated 2R 11mm normal echogenicity 4R 31mm ENLARGED loss of normal architecture 4L 24mm ENLARGED hypoechoic 7 42mm MARKEDLY ENLARGED heterogeneous 10R 18mm prominent 10L 16mm prominent 11R 21mm abnormal appearance TBNA sampling Station 7 42mm Needle 22G Pass 1 0758 visible tissue core Pass 2 0801 additional sample Pass 3 0803 for molecular studies Pass 4 0805 microbiology ROSE Result MALIGNANT small cell morphology identified Station 4R 31mm 3 passes performed ROSE Small cell carcinoma confirmed Station 4L 24mm 3 passes performed ROSE Malignant cells present Station 10R 18mm 2 passes performed ROSE Atypical cells Procedure completed 0822",
            7: "[Indication]\nSCLC Staging.\n[Anesthesia]\nGA.\n[Description]\nEBUS performed. Sampled 7, 4R, 4L, 10R. All enlarged. ROSE positive for SCLC.\n[Plan]\nRefer to Onco.",
            8: "We carried out the EBUS staging for Mr. Moore today. The ultrasound revealed significantly enlarged nodes in the subcarinal and paratracheal regions. We took samples from stations 7, 4R, 4L, and 10R. The onsite pathologist confirmed small cell carcinoma. The patient tolerated the procedure well.",
            9: "Lymph node stations evaluated: 2R, 4R, 4L, 7, 10R, 10L, 11R.\nTBNA sampling:\nStation 7 (42mm): ROSE Result: MALIGNANT, small cell morphology identified.\nStation 4R (31mm): ROSE: Small cell carcinoma confirmed.\nStation 4L (24mm): ROSE: Malignant cells present.\nStation 10R (18mm): ROSE: Atypical cells."
        },
        5: { # James Wilson (RML Tumor/Bleed)
            1: "Indication: RML obstruction.\nProcedure: Debulking + Stent.\nTools: Snare, APC, Cryo. Silicone Stent 14x40mm.\nComplication: Massive hemorrhage (200mL). Controlled w/ epi, ice, blocker.\nOutcome: Stent patent. Patient stable.",
            2: "PROCEDURE: Therapeutic Bronchoscopy.\nFINDINGS: Near-complete RML obstruction by exophytic tumor. \nINTERVENTION: Debulking was achieved via electrocautery snare, APC, and cryotherapy. A significant intraprocedural hemorrhage (200mL) occurred, necessitating bronchial blocker placement and iced saline lavage. Hemostasis was achieved. A 14x40mm silicone stent was deployed.\nCONCLUSION: Restoration of RML patency.",
            3: "Codes:\n- 31640: Tumor excision (Snare).\n- 31631: Stent placement (Silicone).\n- 31634: Balloon occlusion (for hemorrhage control).\nDetails: RML bronchus. Cryo and APC also used. Moderate severity bleeding managed.",
            4: "Procedure: RML Debulking/Stent\nPatient: 72M\nSteps:\n1. Inspection: RML blocked by tumor.\n2. Debulking: Snare, APC, Cryo.\n3. Event: 200cc bleed! Used blocker, epi, ice. Stopped.\n4. Stent: 14x40 silicone placed.\nPlan: ICU monitor.",
            5: "james wilson 12/18/52. rml tumor blocking airway. went in with general lma. removed tumor with snare and cryo. bled a lot like 200ml. had to put a blocker in and use ice. finally stopped. put a silicone stent in 14 by 40. scary moment but hes ok now.",
            6: "PT James Wilson ID MRN A92 555 DOB 12/18/1952 Indication Central airway obstruction from endobronchial tumor RML bronchus Sedation protocol General anesthesia via LMA propofol remifentanil infusion Monitoring Continuous arterial line SpO2 ETCO2 BP q3min Procedure narrative Inspection revealed near complete obstruction of RML bronchus by exophytic tumor with friable surface Tumor debulking performed using Electrocautery snare for bulk removal Argon plasma coagulation for hemostasis Cryotherapy x2 freeze thaw cycles Massive hemorrhage encountered during debulking estimated 200mL Bleeding controlled with Topical epinephrine 1 10 000 Iced saline lavage Bronchial blocker placement temporarily Silicone stent 14mm x 40mm placed in RML bronchus for airway patency Complications Major airway bleeding moderate severity controlled during procedure Patient stable Plan Follow up bronchoscopy in 4 6 weeks for stent assessment and tumor surveillance",
            7: "[Indication]\nRML tumor obstruction.\n[Anesthesia]\nGeneral/LMA.\n[Description]\nTumor debulked (Snare/APC/Cryo). 200mL hemorrhage managed with balloon blocker/ice/epi. 14x40mm silicone stent placed.\n[Plan]\nSurveillance bronch 4-6 weeks.",
            8: "Mr. Wilson had a large tumor blocking his right middle lobe bronchus. We went in to debulk it using a snare, APC, and cryotherapy. During the removal, we encountered significant bleeding, about 200mL. We had to place a bronchial blocker and use iced saline to stop it. Once it was under control, we placed a silicone stent to keep the airway open. He is stable now.",
            9: "Procedure narrative:\nInspection revealed near-complete occlusion of RML bronchus by exophytic tumor. Tumor debulking executed using:\n- Electrocautery snare for bulk extraction\n- Argon plasma coagulation for hemostasis\n- Cryotherapy x2 freeze-thaw cycles\nMassive hemorrhage encountered during debulking. Bleeding checked with:\n- Topical epinephrine\n- Iced saline lavage\n- Bronchial blocker placement\nSilicone stent (14mm x 40mm) deployed."
        },
        6: { # Gilbert Barkley (Stent Removal - Nov 30)
            1: "Indication: Stent removal.\nProcedure:\n- RML Stent: Removed. Granulation/malacia noted.\n- RLL Stent: Removed. Granulation >50% obstruction.\n- Interventions: Cryo debulking, Forceps, CRE Balloon (8-9-10).\nOutcome: Stents out. Airways patent but inflamed.",
            2: "OPERATIVE SUMMARY: Removal of airway stents.\nFINDINGS: RML and RLL stents were identified. Granulation tissue was obstructing the distal edges. \nPROCEDURE: Both stents were successfully grasped and extracted. Significant residual granulation tissue was managed with cryotherapy and mechanical debridement. Balloon dilation (CRE 8-10mm) was performed to optimize luminal patency.\nCONCLUSION: Successful stent removal with management of benign stenosis.",
            3: "Codes: 31638 (Stent removal), 31641 (Tumor/Stenosis relief - Cryo/Balloon).\nNote: Removal of RML and RLL stents. Extensive cryodebridement of granulation tissue performed post-removal. Balloon dilation used.",
            4: "Procedure: Stent Removal\nPt: Gilbert Barkley\nSteps:\n1. Rigid bronch.\n2. RML stent pulled. Granulation treated with cryo.\n3. RLL stent pulled. Mucous cleared. Granulation treated with cryo.\n4. CRE balloon dilation for both.\n5. No complications.",
            5: "gilbert barkley here to get his stents out. 11/30/23. used rigid scope. pulled the rml stent then the rll stent. lot of granulation tissue underneath. used the cryo probe to freeze it off and the balloon to stretch it open. everything looks open now. discharge when ready.",
            6: "DATE OF PROCEDURE 30 Nov 2023 NAME Gilbert Barkley PREOPERATIVE DIAGNOSIS Bronchial obstruction POSTOPERATIVE DIAGNOSIS Bronchial obstruction PROCEDURE s PERFORMED SURGEON Mikie Gallegos MD ASSISTANT s Stephen Pressly M D Nicholas Vance M D INDICATIONS Airway stent removal Consent was obtained SEDATION General Anesthesia DESCRIPTION OF PROCEDURE The procedure was performed in the main operating room Following intravenous medications as per the record a 12 mm ventilating rigid bronchoscope was inserted Using the flexible bronchoscope airway inspection was performed The right middle bronchi had stent in place with minimal mucous but granulation tissue the distal edge causing 50% obstruction The right middle lobe stent was then grasped with flexible forceps by the proximal string and retracted The stent was easily removed The Right lower lobe stent was then removed in a similar fashion Excessive debris and granulation tissue were debulked with a combination of cryoprobe and flexible forceps Finally using an 8 9 10 CRE dilatational balloon we were able to gently dilate the effected bronchi to increased luminal diameter RESULTS Successful removal of bronchial stents within the right middle and right lower lobe bronchi with significant residual granulation tissue COMPLICATIONS None",
            7: "[Indication]\nStent removal.\n[Anesthesia]\nGA, Rigid Bronch.\n[Description]\nRML and RLL stents removed. Significant granulation tissue treated with cryotherapy and forceps. Airways dilated with CRE balloon.\n[Plan]\nRepeat bronch 1 week.",
            8: "We brought Mr. Barkley back to the OR to remove his stents. We used a rigid bronchoscope. The RML and RLL stents were removed without too much trouble, but there was a lot of granulation tissue underneath causing obstruction. We cleaned that up using cryotherapy and forceps, and then dilated the airways with a balloon to ensure they stayed open.",
            9: "PROCEDURE: \nUsing the flexible bronchoscope airway inspection was executed. The right middle bronchi had stent in place. The right middle lobe stent was then grasped and retracted. The stent was easily extracted. The Right lower lobe stent was then withdrawn in a similar fashion. Excessive debris and granulation tissue were debulked with a combination of cryoprobe and flexible forceps. Finally, using an 8-9-10 CRE dilatational balloon we were able to gently dilate the effected bronchi."
        },
        7: { # Gilbert Barkley (Stent Placement - Nov 15)
            1: "Indication: RML/RLL stenosis/granulation.\nProcedure:\n- RLL: Aero 10x20 placed (oversized/distal). Removed.\n- RLL: Aero 8x20 placed. Dilated.\n- RML: Aero 8x15 placed. Dilated.\nOutcome: Patent airways. Kissing stents positioned.",
            2: "OPERATIVE REPORT: Airway Stenting.\nINDICATION: Obstruction of RML/RLL from granulation/tears.\nPROCEDURE: Rigid bronchoscopy. Attempted placement of 10x20mm stent in RLL failed (malposition). Subsequently, an 8x20mm Aero stent was successfully deployed in the RLL and dilated. An 8x15mm Aero stent was deployed in the RML and dilated. 'Kissing' configuration achieved without carinal compression.\nCONCLUSION: Recanalization of RML and RLL.",
            3: "Codes: 31636 (Stent init), 31637 (Stent add-on).\nDetails: RLL stent placed (8x20mm). RML stent placed (8x15mm). Balloon dilation performed. (Initial 10x20 attempt removed/failed, not billed separately).",
            4: "Procedure: Stent Placement\nPt: Gilbert Barkley\nSteps:\n1. Rigid bronch.\n2. RML/RLL blocked by granulation.\n3. Tried 10x20 in RLL - didn't fit.\n4. Put 8x20 in RLL instead.\n5. Put 8x15 in RML.\n6. Balloon dilated both.\n7. Good flow.",
            5: "gilbert barkley 11/15/23. airways blocked by granulation from yesterday. decided to stent. tried a 10x20 in the rll but it was too big and stuck distal. managed to switch it for an 8x20. then put an 8x15 in the rml. kissing stents. dilated both. open now. admit him.",
            6: "DATE OF PROCEDURE 15 Nov 2023 NAME Gilbert Barkley PREOPERATIVE DIAGNOSIS Bronchial obstruction POSTOPERATIVE DIAGNOSIS Bronchial obstruction PROCEDURE s PERFORMED SURGEON Mikie Gallegos MD ASSISTANT s Stephen Pressly M D Nicholas Vance M D INDICATIONS right middle lobe and right lower lobe stenosis SEDATION General Anesthesia DESCRIPTION OF PROCEDURE The right middle and right lower lobe bronchi were completely obstructed by granulation tissue and debris from previous bronchoscopy yesterday Decision was made to place bronchial stents Aero 10 x 20 mm covered self expandable metallic stent was advanced over the guidewire and positioned within the right lower lobe bronchi The stent was deployed however slightly distal Attempts to retract the stent by grasping the proximal string were unsuccessful and it became obvious that the stent was oversized Using rigid forceps we are unable to remove the inappropriately sized stent and using a similar technique placed a 8 x 20 mm arrow fully covered self expanding metallic stent within the area of stenosis Subsequently CRE balloon dilatation of the stent was performed Using a similar technique we then placed a 8 x 15 mm m arrow fully covered self expanding metallic stent within the area of stenosis In the right middle lobe RESULTS Successful insertion of bronchial stents",
            7: "[Indication]\nRML/RLL obstruction.\n[Anesthesia]\nGA.\n[Description]\nPlacement of stents. RLL: 8x20mm Aero (after 10x20 failed). RML: 8x15mm Aero. Balloon dilation performed.\n[Plan]\nAdmit. Airway clearance. Removal in 2 weeks.",
            8: "Because of the obstruction in Mr. Barkley's lower airways, we decided to place stents. We initially tried a 10mm stent in the right lower lobe, but it was too big. We swapped it for an 8x20mm stent which fit well. Then we placed an 8x15mm stent in the right middle lobe. We dilated both with a balloon, and the airways are now open.",
            9: "Decision was made to deploy bronchial stents. An Aero 10 x 20 mm covered self-expandable metallic stent was advanced but was oversized. Using a similar technique we placed a 8 x 20 mm arrow fully covered self-expanding metallic stent within the area of stenosis. Subsequently CRE balloon dilatation of the stent was performed. Using a similar technique we then deployed a 8 x 15 mm m arrow fully covered self-expanding metallic stent in the right middle lobe."
        },
        8: { # Oscar Godsey (LMS Stent Removal)
            1: "Indication: Lobar collapse.\nProcedure:\n- LMS Stent: Patent. Granulation distal.\n- LLL: Obstructed by granulation.\n- Action: LMS stent removed. LLL granulation cryo-debulked. CRE dilation. Kenalog injected.\nOutcome: Improved patency (80%).",
            2: "OPERATIVE NOTE: Management of left mainstem stent and LLL obstruction.\nFINDINGS: The LMS stent was patent but associated with distal granulation causing LLL obstruction. \nPROCEDURE: The LMS stent was removed to facilitate remodeling. Extensive granulation tissue in the LLL was treated with cryotherapy and flexible forceps. The airway was dilated with a CRE balloon. Intralesional steroid injection (Kenalog) was performed to inhibit recurrence.",
            3: "Codes: 31638 (Stent removal), 31641 (Stenosis relief).\nDetails: Removal of left mainstem stent. Cryotherapy destruction of granulation tissue in LLL. Balloon dilation. Submucosal steroid injection.",
            4: "Procedure: Stent Removal + Cryo\nPt: Oscar Godsey\nSteps:\n1. GA/LMA -> Rigid.\n2. LMS stent looked ok but LLL blocked.\n3. Removed LMS stent.\n4. Cryo'd the LLL granulation.\n5. Balloon dilated.\n6. Injected steroids.\n7. Better flow.",
            5: "oscar godsey 5/15/19. lms stent in place. lll blocked by granulation. decided to pull the stent out since it might not be helping. removed it fine. used cryo on the lll tissue. dilated it with a balloon. injected some kenalog. looks 80 percent open now. back to icu.",
            6: "Patient Godsey Oscar DATE OF PROCEDURE 5 15 2019 PREOPERATIVE DIAGNOSIS left mainstem stent obstruction POSTOPERATIVE DIAGNOSIS Distal granulation tissue causing left lower lobe obstruction PROCEDURE PERFORMED Rigid bronchoscopy with cryodebulking cryotherapy of obstructive granulation tissue endobronchial submucosal steroid injection left mainstem bronchial stent removal SURGEON Jordan Parks MD ASSISTANT Michael Manson DO fellow DESCRIPTION OF PROCEDURE The left mainstem stent was widely patent without evidence of stent obstruction At the distal edge of the stent there was some minor granulation tissue which was nonobstructive Distal to the stent there was complete obstruction of the left lower lobe orifice secondary to granulation tissue Using the 1.9 mm cryoprobe we are able to extract granulation tissue to visualize the segmental stenosis in the left lower lobe At this point we decided to remove the left mainstem stent for a few reasons Using flexible forceps to grasp the proximal string on the stent we were able to gently retract the stent and remove it without difficulty Then using a 8 9 10 millimeter CRE balloon dilated each of the left lower lobe subsegments Cryotherapy was then performed Finally using the super dimension 21 gauge needle we injected a total of 5 mL of Kenalog 10 mg milliliter solution into the submucosa",
            7: "[Indication]\nLobar collapse, stent evaluation.\n[Anesthesia]\nGA.\n[Description]\nLMS stent removed. LLL obstruction treated with cryodebulking and CRE balloon dilation. Kenalog injected.\n[Plan]\nICU. CXR. Follow up 1 week.",
            8: "Mr. Godsey had a stent in his left main airway. We found that the stent was fine, but tissue had grown past it, blocking the lower lobe. We decided to take the stent out. We used a cryoprobe to freeze and remove the blocking tissue, then stretched the airway with a balloon. We also injected some steroids to help prevent it from growing back.",
            9: "PROCEDURE PERFORMED: Rigid bronchoscopy with cryodebulking/cryotherapy of obstructive granulation tissue, endobronchial submucosal steroid injection, left mainstem bronchial stent removal.\nAction: The LMS stent was removed. Cryotherapy was executed to extract granulation tissue. Using a 8–9–10 millimeter CRE balloon we dilated each of the left lower lobe subsegments. Cryotherapy was then performed. Finally we injected a total of 5 mL of Kenalog."
        },
        9: { # Gregory Martinez (Checklist)
            1: "Checklist: EBUS-TBNA\n- Pt: Gregory Martinez.\n- 4R, 7, 11R sampled.\n- ROSE: Positive.\n- Sedation: Midaz/Fentanyl. Ramsay 3.\n- No complications.\n- Quality: 100%.",
            2: "PROCEDURE CHECKLIST SUMMARY:\nPatient Identification: Verified (Martinez).\nProcedure: EBUS-TBNA for staging.\nNodes Sampled: 4R (10mm, Pos), 7 (16mm, Pos), 11R (8mm, Adequate).\nProtocol: Systematic evaluation N3-N2-N1 completed. Photodocumentation verified.\nSafety: Time-out performed. Hemodynamics stable.",
            3: "Service: 31653 (EBUS 3 stations).\nStations: 4R, 7, 11R.\nPathology: Malignant (ROSE +).\nTechnique: EBUS guided needle aspiration. 4 passes per node (4R/7), 3 passes (11R).\nSafety: Checklist completed.",
            4: "Procedure: EBUS\nPt: Gregory Martinez\nChecklist:\n- Consent: Yes.\n- Time out: Yes.\n- 4R: Sampled (+).\n- 7: Sampled (+).\n- 11R: Sampled.\n- Sedation: Tolerate well.\n- Complications: None.",
            5: "checklist for gregory martinez. ebus tbna. checked 4r 7 and 11r. all sampled. 4r and 7 were positive on rose. 11r was just adequate. used midaz and fentanyl. patient did fine. checklist complete.",
            6: "BRONCHOSCOPY SAFETY CHECKLIST COMPLETED PRE PROCEDURE Patient identity verified Name Gregory Martinez MRN NN 7482 K DOB 03 22 1957 Informed consent obtained and documented PROCEDURE EBUS TBNA Timeout performed Systematic N3 N2 N1 evaluation Station 4R 10mm 4 passes ROSE positive PET Station 7 16mm 4 passes ROSE positive PET Station 11R 8mm 3 passes ROSE adequate All accessible stations photographed SEDATION RECORD Midazolam 3mg IV administered T 0 Fentanyl 100mcg IV administered T 0 Maximum Ramsay 3 POST PROCEDURE Patient awakened appropriately Vital signs stable No immediate complications QUALITY INDICATORS MET Staging sensitivity documented Systematic evaluation performed Photodocumentation complete Adequate tissue for molecular testing Safety checklist 100% complete",
            7: "[Patient]\nGregory Martinez.\n[Procedure]\nEBUS-TBNA.\n[Stations]\n4R (Pos), 7 (Pos), 11R (Adequate).\n[Safety]\nChecklist complete. No complications.",
            8: "This is the safety checklist for Mr. Martinez's EBUS procedure. We verified his identity and consent. We sampled stations 4R, 7, and 11R. Stations 4R and 7 were positive on the rapid test. The patient was sedated with Midazolam and Fentanyl and tolerated it well. All quality indicators were met.",
            9: "BRONCHOSCOPY SAFETY CHECKLIST - COMPLETED\nPROCEDURE (EBUS-TBNA):\n- Systematic N3-N2-N1 evaluation\n- Station 4R (10mm): 4 passes, ROSE positive\n- Station 7 (16mm): 4 passes, ROSE positive\n- Station 11R (8mm): 3 passes, ROSE adequate\nQUALITY INDICATORS MET:\n- Staging sensitivity documented\n- Systematic evaluation performed"
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the 10 notes in Part 040.
    """
    # 0: Thomas Jackson (71 in 2025)
    # 1: Richard Brown (73 in 2025)
    # 2: Patricia Anderson (68 in 2025)
    # 3: Christopher Moore (72)
    # 4: Christopher Moore (72) - Treated as distinct for variation purposes, maybe a repeat procedure or clerical duplicate.
    # 5: James Wilson (72 in 2025)
    # 6: Gilbert Barkley (Stent Removal)
    # 7: Gilbert Barkley (Stent Place)
    # 8: Oscar Godsey
    # 9: Gregory Martinez
    
    # I will generate unique names for each "Style" within each "Note Index".
    
    return [
        {"idx": 0, "orig_name": "Thomas Jackson", "orig_age": 71, "names": ["Robert Smith", "James Johnson", "Michael Williams", "David Brown", "William Jones", "Richard Miller", "Joseph Davis", "Thomas Garcia", "Charles Rodriguez"]},
        {"idx": 1, "orig_name": "Richard Brown", "orig_age": 73, "names": ["Daniel Wilson", "Matthew Martinez", "Anthony Anderson", "Donald Taylor", "Mark Thomas", "Paul Hernandez", "Steven Moore", "Andrew Martin", "Kenneth Jackson"]},
        {"idx": 2, "orig_name": "Patricia Anderson", "orig_age": 68, "names": ["Barbara Thompson", "Elizabeth White", "Jennifer Lopez", "Maria Lee", "Susan Gonzalez", "Margaret Harris", "Dorothy Clark", "Lisa Lewis", "Nancy Robinson"]},
        {"idx": 3, "orig_name": "Christopher Moore", "orig_age": 72, "names": ["Kevin Walker", "Brian Perez", "George Hall", "Edward Young", "Ronald Allen", "Timothy Sanchez", "Jason Wright", "Jeffrey King", "Ryan Scott"]},
        {"idx": 4, "orig_name": "Christopher Moore", "orig_age": 72, "names": ["Gary Green", "Jacob Baker", "Nicholas Adams", "Eric Nelson", "Stephen Hill", "Larry Ramirez", "Justin Campbell", "Scott Mitchell", "Brandon Roberts"]},
        {"idx": 5, "orig_name": "James Wilson", "orig_age": 72, "names": ["Frank Carter", "Benjamin Phillips", "Gregory Evans", "Samuel Turner", "Raymond Torres", "Patrick Parker", "Alexander Collins", "Jack Edwards", "Dennis Stewart"]},
        {"idx": 6, "orig_name": "Gilbert Barkley", "orig_age": 65, "names": ["Jerry Flores", "Tyler Morris", "Aaron Nguyen", "Henry Murphy", "Douglas Rivera", "Peter Cook", "Adam Rogers", "Nathan Morgan", "Zachary Peterson"]},
        {"idx": 7, "orig_name": "Gilbert Barkley", "orig_age": 65, "names": ["Walter Cooper", "Kyle Reed", "Harold Bailey", "Carl Bell", "Arthur Gomez", "Roger Kelly", "Keith Howard", "Jeremy Ward", "Terry Cox"]},
        {"idx": 8, "orig_name": "Oscar Godsey", "orig_age": 60, "names": ["Lawrence Diaz", "Sean Richardson", "Christian Wood", "Albert Watson", "Joe Brooks", "Ethan Bennett", "Austin Gray", "Jesse James", "Willie Reyes"]},
        {"idx": 9, "orig_name": "Gregory Martinez", "orig_age": 68, "names": ["Billy Cruz", "Bryan Hughes", "Bruce Price", "Jordan Myers", "Ralph Long", "Roy Foster", "Louis Sanders", "Eugene Ross", "Wayne Morales"]}
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
            # Handle potential missing keys if the variation dict is incomplete (safety check)
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}. Using original.")
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update DOB if present in original text (rudimentary replacement or metadata update)
                # Since I am replacing the whole note_text, I don't need to regex replace the old text.
                # Just update metadata.
                
                # Update extracted MRN if it exists to be unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    original_mrn = note_entry["registry_entry"]["patient_mrn"]
                    note_entry["registry_entry"]["patient_mrn"] = f"{original_mrn}_syn_{style_num}"
                
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # If age is not explicitly in registry_entry (it isn't in this specific file schema usually), 
                # we might just leave it or add it if the schema allows. 
                # The prompt asks to change age "slightly". 
                # If the schema has 'patient_age', update it.
                if "patient_age" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["patient_age"] = new_age

            # Add metadata about the synthetic generation
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON
    output_filename = output_dir / "synthetic_blvr_notes_part_040.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()