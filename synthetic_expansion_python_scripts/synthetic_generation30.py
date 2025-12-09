import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_030.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Variations for the 10 notes in Part 030
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Anjali Patel (Bilateral Robotic Bronch)
            1: "Indication: Bilateral nodules (RUL/LUL).\nProcedure: Ion robotic bronchoscopy.\nActions:\n- Registered Ion system.\n- Sampled RUL anterior nodule (forceps x6, brush x2).\n- Sampled LUL apical-posterior nodule (forceps x5, brush x2).\nROSE: Adenocarcinoma both sites.\nResult: No complications.",
            2: "PROCEDURE NOTE: The patient presented for evaluation of synchronous bilateral pulmonary nodules. The Ion robotic platform was deployed. Following successful registration (fiducial error 0.9 mm), navigation was sequentially performed to the right upper lobe anterior segment and the left upper lobe apical-posterior segment. Radial EBUS confirmation and fluoroscopic verification preceded tissue acquisition. Transbronchial forceps biopsies and cytology brushings were obtained from both sites. Rapid on-site evaluation was suggestive of adenocarcinoma in both locations, raising suspicion for synchronous primaries versus metastatic disease.",
            3: "CPT Codes: 31627 (Navigational bronchoscopy), 31654 (Radial EBUS), 31628 (Transbronchial lung biopsy - first lobe), 31632 (Transbronchial lung biopsy - additional lobe), 31623 (Brushings).\nRationale: Robotic navigation and radial EBUS were used to localize peripheral lesions. Biopsies were taken from the RUL (initial lobe) and the LUL (additional lobe). Brushings were also performed.",
            4: "Procedure: Robotic Bronchoscopy (Bilateral)\nPatient: Anjali Patel\nSteps:\n1. General anesthesia, ETT.\n2. Ion registration complete.\n3. Navigated to RUL nodule -> REBUS confirmed -> Biopsied.\n4. Navigated to LUL nodule -> REBUS confirmed -> Biopsied.\n5. ROSE: Adeno in both.\nPlan: Staging workup.",
            5: "Anjali has nodules on both sides so we used the robot. Registered the ion system error was good under 1mm. Went to the right upper lobe first radial probe showed the lesion took biopsies and brushings. Then went to the left upper lobe and did the same thing. Rose said adenocarcinoma for both of them. She woke up fine no pneumothorax on the xray.",
            6: "Ion Robotic Bronchoscopy, Bilateral Nodule Sampling. Patient is a 45-year-old female with incidental bilateral lung nodules. RUL nodule 2.1cm, LUL nodule 1.6cm. Registration using automatic method was completed. Ion catheter navigated to RUL anterior segment and LUL apical-posterior segment. Tool-at-target confirmed by Radial EBUS. Forceps biopsies and brushings obtained from both sites. ROSE showed atypical pneumocytes, favor adenocarcinoma. No pneumothorax.",
            7: "[Indication]\nBilateral lung nodules (RUL/LUL), suspicion of malignancy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nIon robotic navigation performed. Targets localized with REBUS. RUL and LUL nodules biopsied (forceps/brush). ROSE positive for adenocarcinoma bilaterally.\n[Plan]\nFinal path pending. Staging MRI/PET.",
            8: "Ms. Patel underwent a robotic bronchoscopy to biopsy nodules in both her right and left lungs. We used the Ion robot to precisely navigate to each spot, confirming our location with ultrasound. We took tissue samples from both the right upper lobe and left upper lobe. The preliminary results suggests cancer in both spots, likely adenocarcinoma. She tolerated the procedure well and had no complications like a collapsed lung.",
            9: "Procedure: Robotic navigational sampling of bilateral pulmonary lesions.\nTechnique: Ion system utilized for localization. Radial EBUS verification performed.\nIntervention: Transbronchial forceps and brush sampling of RUL and LUL targets.\nFindings: Cytopathology consistent with adenocarcinoma.\nOutcome: Patient extubated and stable."
        },
        1: { # Robert Williams (EMN LLL)
            1: "Indication: LLL nodule.\nProcedure: EMN bronchoscopy.\nGuidance: SuperDimension + Radial EBUS.\nAction: TBBx x6, Brush x3.\nROSE: Adenocarcinoma.\nComplications: None.",
            2: "OPERATIVE REPORT: The patient underwent electromagnetic navigation bronchoscopy for a hypermetabolic left lower lobe nodule. The SuperDimension system facilitated navigation to the superior segment. Radial EBUS demonstrated a concentric, hypoechoic lesion. Transbronchial biopsies and brushings were obtained. Preliminary cytopathologic evaluation confirmed the presence of malignant cells consistent with adenocarcinoma.",
            3: "Code Selection: 31627 (Navigational bronchoscopy), 31654 (Radial EBUS), 31628 (Transbronchial lung biopsy).\nJustification: Computer-assisted navigation was required to reach the peripheral LLL lesion. Radial EBUS confirmed the location. Multiple transbronchial biopsies were obtained for diagnosis.",
            4: "Procedure Note\nPatient: Robert Williams\nIndication: LLL mass.\nSteps:\n1. SuperDimension registration.\n2. Navigated to LLL superior segment.\n3. Confirmed with REBUS (concentric view).\n4. Biopsies (forceps x6) and brushings x3.\n5. ROSE positive for Adeno.\n6. No bleeding.\nPlan: D/C if CXR clear.",
            5: "Robert has a LLL nodule used the superdimension to get there. Radial probe showed it nicely concentric view. Took 6 biopsies and some brushes. Cytotech said it looks like adenocarcinoma. No bleeding patient did great. checking cxr before discharge.",
            6: "Electromagnetic Navigation Bronchoscopy with transbronchial biopsy and radial EBUS. Patient is a 71-year-old male with LLL nodule. Virtual pathway created to LLL superior segment nodule. Extended working channel placed. Radial EBUS demonstrated concentric hypoechoic lesion. Transbronchial forceps biopsies and cytology brush specimens obtained. ROSE positive for malignancy. No complications. Discharged home.",
            7: "[Indication]\nLLL nodule, PET avid.\n[Anesthesia]\nModerate sedation.\n[Description]\nEMN navigation to LLL. REBUS confirmation. Transbronchial biopsy and brushing performed. ROSE positive for adenocarcinoma.\n[Plan]\nOncology referral.",
            8: "We performed a navigational bronchoscopy on Mr. Williams to biopsy a nodule in his left lower lung. Using the electromagnetic navigation system, we guided a catheter to the lesion and confirmed its position with ultrasound. We then took several biopsies and brush samples. The immediate analysis in the room showed cancer cells, likely adenocarcinoma. He recovered well and is being discharged.",
            9: "Procedure: Electromagnetic navigational sampling.\nTarget: LLL superior segment lesion.\nMethod: SuperDimension guidance with REBUS confirmation.\nAction: Forceps and brush acquisition of tissue.\nDiagnosis: Adenocarcinoma confirmed via ROSE."
        },
        2: { # Michelle Chen (Complex Staging: EBUS + Ion + Cryo)
            1: "Indication: RLL nodule + Adenopathy.\nProcedures: EBUS-TBNA + Ion Nav + Cryobiopsy.\nEBUS: 10R positive (Adeno). 4L neg.\nIon: Navigated to RLL mass. REBUS/CBCT confirmed.\nSampling: Forceps x6, Cryo x2.\nROSE: Adenocarcinoma (Primary & N1).\nPlan: Staging workup.",
            2: "PROCEDURE: Combined endobronchial ultrasound and robotic-assisted bronchoscopy. EBUS-TBNA was performed at stations 4L and 10R; station 10R was positive for malignancy. The Ion robotic platform was then utilized to navigate to the RLL superior segment mass. Following radial EBUS and Cone-Beam CT confirmation, both conventional forceps biopsies and transbronchial cryobiopsies were obtained to ensure adequate tissue for molecular profiling.",
            3: "Billing: 31653 (EBUS 3+ stations - note says 4L, 10R sampled, plus others surveyed/considered?), 31627 (Nav), 31654 (REBUS), 31628 (TBBx), 31623 (Brush).\nCorrection: Note lists sampling of 4L and 10R only (2 stations). Should be 31652. Cryobiopsy (31628 covers TBBx method broadly or 31645 if distinct).",
            4: "Combined EBUS/Robotic Bronch\nPatient: Michelle Chen\nIndication: RLL mass + nodes\nSteps:\n1. EBUS: Sampled 4L (neg) and 10R (pos).\n2. Ion Robot: Navigated to RLL mass.\n3. Confirmed with REBUS + CBCT.\n4. Biopsies: Forceps and Cryo.\n5. Bleeding controlled with blocker.\nResult: Stage IIIA Adeno (T1cN1).",
            5: "Michelle needs staging for her RLL mass. Did EBUS first sampled 4L and 10R. 10R was positive for adeno. Then switched to the Ion robot found the RLL mass with rebus and cone beam. Took forceps biopsies and then two cryo biopsies for molecular. Had some bleeding used a blocker and iced saline. Patient stable.",
            6: "EBUS with TBNA, Ion robotic bronchoscopy, Radial EBUS, Cryobiopsy of RLL mass. Patient is a 71-year-old female. EBUS Phase: Sampled stations 4L and 10R. ROSE positive for malignancy at 10R. Ion Robotic Bronchoscopy Phase: Navigated to RLL superior segment mass. Radial EBUS and CBCT confirmed position. Forceps biopsies and cryobiopsies obtained. Mild bleeding managed with blocker. Final staging likely IIIA.",
            7: "[Indication]\nRLL mass, mediastinal adenopathy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS-TBNA (4L, 10R). Ion Nav to RLL. REBUS/CBCT confirmation. Forceps and Cryobiopsy of mass. 10R and Mass positive for Adenocarcinoma.\n[Plan]\nMolecular testing. Oncology consult.",
            8: "We performed a comprehensive staging procedure for Ms. Chen. First, we used EBUS to sample lymph nodes; the right hilar node tested positive for cancer. Then, using the robotic bronchoscope, we biopsied the main tumor in the right lower lobe using both standard forceps and a freezing probe to get a large sample for genetic testing. She is diagnosed with Stage IIIA adenocarcinoma and will need further treatment planning.",
            9: "Procedure: Multimodal staging bronchoscopy.\nComponents: EBUS-TBNA of hilar/mediastinal nodes. Robotic navigation with cryosampling of pulmonary parenchymal lesion.\nFindings: N1 nodal involvement and primary adenocarcinoma confirmed.\nIntervention: Hemostasis secured via bronchial blocker."
        },
        3: { # Carlos Rodriguez (EBUS + EMN + Endobronchial)
            1: "Indication: LLL mass, adenopathy.\nFindings: LLL orifice occluded by tumor.\nProcedures: EBUS (4R, 4L, 7, 10L, 11L sampled). Endobronchial biopsy LLL. EMN to peripheral LLL (partial).\nROSE: Squamous cell CA in all stations and primary.\nDx: Stage IIIB/C SCC.",
            2: "PROCEDURE: Comprehensive staging was performed for a large LLL mass. EBUS-TBNA of stations 4R, 4L, 7, 10L, and 11L confirmed multi-station N2/N3 involvement with squamous cell carcinoma. Airway inspection revealed endobronchial tumor extension obstructing the LLL, which was biopsied directly. Electromagnetic navigation was attempted to sample the peripheral component for molecular adequacy, yielding confirmatory diagnostic tissue.",
            3: "Codes: 31653 (EBUS 3+ stations), 31625 (Endobronchial biopsy), 31627 (Nav), 31654 (REBUS), 31628 (Transbronchial biopsy).\nRationale: Extensive EBUS staging. Endobronchial biopsy of visible tumor (31625). Navigation and TBBx of peripheral component (31627, 31628).",
            4: "Staging Bronchoscopy\nPatient: Carlos Rodriguez\nSteps:\n1. EBUS: Sampled 5 stations. All pos for Squamous.\n2. Standard Bronch: Saw tumor in LLL airway. Biopsied (Endobronchial).\n3. EMN: Navigated past tumor to distal lung. Biopsied.\nDiagnosis: Extensive Squamous Cell CA.\nPlan: Chemo/Rad.",
            5: "Carlos has a big LLL mass and nodes everywhere. EBUS showed cancer in 4R 4L 7 10L 11L. Its squamous cell. Looked in the airway and the tumor is blocking the LLL so i took biopsies there too. Then tried to navigate to the far part of the tumor with superdimension to get more tissue. Got good samples. He has stage 3B or maybe 4.",
            6: "Procedures: EBUS-TBNA, Electromagnetic navigation bronchoscopy, Radial EBUS, Transbronchial biopsies, Endobronchial biopsies. Patient is a 59-year-old male with LLL mass. EBUS sampled stations 4R, 4L, 7, 10L, 11L; all positive for squamous cell carcinoma. Airway inspection showed LLL endobronchial tumor, biopsied. EMN used to sample peripheral component. Extensive N2/N3 disease confirmed.",
            7: "[Indication]\nLLL mass, extensive adenopathy.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA (5 stations). Endobronchial biopsy of LLL tumor. EMN-guided TBBx of peripheral mass. Squamous cell carcinoma confirmed in all sites.\n[Plan]\nMedical Oncology consult.",
            8: "Mr. Rodriguez underwent a major staging procedure. We found that his lung cancer (squamous cell) has spread to lymph nodes on both sides of his chest. We also found the tumor growing into his airway, which we biopsied. We also navigated deeper into the lung to get more tissue for testing. He has advanced stage disease and will need chemotherapy and radiation.",
            9: "Procedure: Staging EBUS and therapeutic/diagnostic bronchoscopy.\nFindings: Contralateral and ipsilateral nodal metastases (Squamous Cell). Endobronchial tumor obstruction.\nIntervention: Nodal aspiration, direct endobronchial biopsy, and navigated peripheral sampling.\nOutcome: Diagnosis of advanced stage carcinoma established."
        },
        4: { # Jennifer Wu (EBUS + Ion + Cryo)
            1: "Indication: RUL nodule, 4R node.\nProcedures: EBUS (4R+, 10R-). Ion Nav to RUL. Cryobiopsy.\nROSE: Adenocarcinoma (4R & RUL).\nResult: Stage IIIA.\nPlan: Molecular testing, Tumor board.",
            2: "PROCEDURE: Combined staging EBUS and robotic bronchoscopy. EBUS-TBNA of station 4R confirmed N2 disease (adenocarcinoma), while station 10R was negative. The Ion platform was utilized to navigate to a spiculated RUL nodule. Following confirmation with radial EBUS and Cone-Beam CT, transbronchial cryobiopsies were performed to ensure adequate tissue for comprehensive molecular profiling. A bronchial blocker was used for hemostasis.",
            3: "Billing: 31653 (EBUS - 2 stations? Note says 4R and 10R sampled -> 31652). 31627 (Nav), 31654 (REBUS), 31628 (Biopsy - Cryo/Forceps). 31623 (Brush), 31624 (BAL).\nCorrection: EBUS code likely 31652 for 2 stations. Cryo coded as TBBx (31628) or Cryo (31645) depending on payer.",
            4: "Procedure: EBUS + Ion\nPatient: Jennifer Wu\nIndication: RUL nodule, N2 suspicion.\nSteps:\n1. EBUS: 4R pos, 10R neg.\n2. Ion Nav to RUL nodule.\n3. REBUS/CBCT verification.\n4. Cryobiopsy x2 for molecular.\n5. Hemostasis with blocker.\nDx: Stage IIIA Adeno.",
            5: "Jennifer has a growing RUL nodule and a suspicious node. Did EBUS first 4R was positive for adeno 10R was negative. Then used the Ion robot to biopsy the lung nodule. Used the cryo probe to get big pieces for genetic testing. She bled a bit so we used the balloon. Everything stopped fine.",
            6: "Combined EBUS + Robotic Bronchoscopy. Patient is a 52-year-old female. EBUS-TBNA of stations 4R and 10R performed. ROSE of 4R positive for adenocarcinoma. Ion robotic bronchoscopy navigated to RUL posterior segment nodule. Radial EBUS and CBCT confirmed position. Transbronchial forceps biopsies and cryobiopsies obtained. Molecular testing requested. No complications.",
            7: "[Indication]\nRUL nodule, mediastinal adenopathy.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA (4R, 10R). Ion Nav to RUL. Cryobiopsy performed. 4R and RUL positive for adenocarcinoma.\n[Plan]\nBrain MRI. Tumor board.",
            8: "We performed a procedure to stage and diagnose Ms. Wu's lung cancer. First, we sampled lymph nodes; the right paratracheal node was positive, but the hilar node was clear. Then, we used the robot to biopsy the main tumor in the right upper lobe, using a freezing technique to get good tissue samples for genetic analysis. She has Stage IIIA cancer.",
            9: "Procedure: EBUS staging and robotic parenchymal sampling.\nFindings: N2 metastatic disease (Adenocarcinoma).\nTechnique: TBNA of mediastinal nodes. Robotic navigation with cryo-assisted biopsy of RUL primary.\nOutcome: Diagnosis confirmed, molecular tissue secured."
        },
        5: { # Robert Thompson (EBUS + EMN)
            1: "Indication: LLL mass, extensive adenopathy.\nProcedure: EBUS (5, 7, 10L) + EMN Bronch (LLL mass).\nROSE: Adenocarcinoma in all sites.\nStage: IIIB (N3).\nPlan: Oncology.",
            2: "PROCEDURE: The patient underwent EBUS-TBNA followed by electromagnetic navigation bronchoscopy. EBUS confirmed contralateral N3 disease (Station 5) as well as N2 (Station 7) and N1 (Station 10L) involvement with adenocarcinoma. EMN guided transbronchial biopsies of the LLL primary lesion were also positive. The findings establish a diagnosis of Stage IIIB adenocarcinoma.",
            3: "CPT: 31653 (EBUS 3+ stations: 5, 7, 10L). 31627 (Nav). 31654 (REBUS). 31628 (Biopsy). 31623 (Brush). 31624 (BAL).\nRationale: Comprehensive staging and diagnostic procedure supporting high complexity billing.",
            4: "Procedure: EBUS + EMN\nPatient: Robert Thompson\nFindings:\n- EBUS: Stations 5, 7, 10L all positive for Adeno.\n- EMN: LLL mass biopsied, positive for Adeno.\nImpression: Stage IIIB Lung CA.\nPlan: Refer for chemo/immuno.",
            5: "Robert has a LLL mass and big nodes. Did EBUS first sampled 5 7 and 10L all cancer. Then used superdimension to find the LLL mass and biopsied it. It's all adenocarcinoma. He is stage 3B because of the N3 node. No surgery for him.",
            6: "Endobronchial Ultrasound with Transbronchial Needle Aspiration and Electromagnetic Navigation Bronchoscopy. Patient is a 61-year-old male. EBUS-TBNA performed on stations 5, 7, and 10L; all positive for adenocarcinoma. EMN bronchoscopy navigated to LLL posterior basal segment mass. Radial EBUS confirmed concentric lesion. Transbronchial biopsies and brushings obtained. ROSE positive. Diagnosed Stage IIIB Adenocarcinoma.",
            7: "[Indication]\nLLL mass, N3 suspicion.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA (5, 7, 10L) positive. EMN biopsy LLL mass positive. Adenocarcinoma.\n[Plan]\nSystemic therapy.",
            8: "We performed a biopsy and staging procedure on Mr. Thompson. We found that his lung cancer had spread to lymph nodes on both the left and right sides of his chest (N3 disease). We also confirmed the main tumor in the left lower lobe is adenocarcinoma. Because of the extent of the spread, surgery isn't an option, and he will need chemotherapy and immunotherapy.",
            9: "Procedure: EBUS-TBNA and EMN-guided biopsy.\nDiagnosis: Stage IIIB Adenocarcinoma.\nFindings: Contralateral mediastinal, subcarinal, and hilar nodal involvement.\nIntervention: Tissue acquired for molecular profiling.\nDisposition: Discharged."
        },
        6: { # Patricia Johnson (EMN + Fiducial)
            1: "Indication: RUL spiculated nodule.\nProcedure: EMN bronchoscopy.\nAction: Biopsied RUL nodule (TBBx, Brush, FNA). Placed fiducial.\nROSE: NSCLC.\nPlan: SBRT evaluation.",
            2: "PROCEDURE: Electromagnetic navigation bronchoscopy was utilized to localize a 3.1 cm spiculated RUL lesion. Following registration and navigation, radial EBUS confirmed a concentric solid lesion. Transbronchial sampling (forceps, brush, needle) yielded non-small cell carcinoma. A fiducial marker was deployed under fluoroscopic guidance to facilitate future stereotactic body radiation therapy (SBRT).",
            3: "Billing: 31627 (Nav), 31654 (REBUS), 31628 (TBBx), 31629 (TBNA), 31626 (Fiducial).\nRationale: Diagnostic sampling and therapeutic marker placement performed in the same session.",
            4: "EMN Bronch + Fiducial\nPatient: Patricia Johnson\nSteps:\n1. Navigated to RUL nodule.\n2. Confirmed with REBUS.\n3. Biopsied (forceps, brush, needle).\n4. ROSE positive for cancer.\n5. Placed gold fiducial for SBRT.\nPlan: Rad Onc consult.",
            5: "Patricia has a RUL nodule we think is cancer. Used superdimension to find it. Took biopsies and aspirates. ROSE said adenocarcinoma. Put a gold seed in for radiation tracking. She did fine.",
            6: "Electromagnetic navigation bronchoscopy with biopsy and fiducial placement. Patient is a 66-year-old female. SuperDimension system used to access RUL anterior segment nodule. Radial EBUS confirmed lesion. Transbronchial forceps biopsies, cytology brush, and needle aspiration performed. ROSE consistent with non-small cell carcinoma. Fiducial marker placed for radiation planning. No complications.",
            7: "[Indication]\nRUL nodule, SBRT candidate.\n[Anesthesia]\nModerate sedation.\n[Description]\nEMN to RUL. REBUS confirm. Biopsies positive for NSCLC. Fiducial placed.\n[Plan]\nRadiation Oncology.",
            8: "We biopsied a nodule in Ms. Johnson's right upper lung using the navigation system. The preliminary results show it is lung cancer. Since she might need focused radiation treatment, we also placed a small gold marker (fiducial) near the tumor to help the radiation doctors target it precisely.",
            9: "Procedure: EMN-guided diagnostic bronchoscopy and fiducial implantation.\nTarget: RUL parenchymal lesion.\nActions: Tissue sampling via multiple modalities. Placement of radiosurgical marker.\nOutcome: Malignancy confirmed; marker position verified."
        },
        7: { # Manuel Garcia (EMN LLL)
            1: "Indication: Enlarging LLL nodule.\nHistory: Colon CA.\nProcedure: EMN Bronchoscopy.\nFinding: 23mm lesion, concentric REBUS.\nAction: TBBx x7, Brush x3, BAL.\nROSE: Malignant cells (Colon vs Primary?).\nPlan: Path.",
            2: "PROCEDURE: The patient underwent electromagnetic navigation bronchoscopy for investigation of an enlarging LLL nodule in the context of prior colon cancer. Navigation to the posterior basal segment was successful, with radial EBUS demonstrating a concentric, heterogeneous lesion. Transbronchial biopsies and brushings were obtained. ROSE confirmed malignancy; immunohistochemistry is pending to differentiate primary lung carcinoma from metastatic colorectal disease.",
            3: "Codes: 31627 (Nav), 31654 (REBUS), 31628 (Biopsy), 31623 (Brush), 31624 (BAL).\nRationale: Standard EMN diagnostic bundle. Separate codes for distinct sampling modalities.",
            4: "Procedure: EMN Bronch\nPatient: Manuel Garcia\nQuery: Met vs Primary\nSteps:\n1. Nav to LLL.\n2. REBUS confirm.\n3. Biopsy x7, Brush x3.\n4. ROSE pos.\nPlan: Wait for IHC.",
            5: "Manuel has a history of colon cancer and a new lung spot. Did the navigation bronch. Found the spot in the LLL. Biopsied it a bunch of times. Cytology says its cancer but need stains to know if its lung or colon. No complications.",
            6: "EMN Bronchoscopy, Radial EBUS, Transbronchial Biopsy, BAL. Patient is a 77-year-old male with enlarging LLL nodule. Navigation to LLL posterior basal segment. Radial EBUS: concentric pattern achieved. Transbronchial biopsies, cytology brushings, and BAL obtained. ROSE findings concerning for malignancy. Final pathology pending.",
            7: "[Indication]\nLLL nodule, hx colon CA.\n[Anesthesia]\nMAC.\n[Description]\nEMN to LLL. REBUS confirmation. Biopsies taken. ROSE positive.\n[Plan]\nPathology for IHC.",
            8: "Mr. Garcia underwent a biopsy of a nodule in his left lower lung. Given his history of colon cancer, we need to know if this is a new lung cancer or spread from his colon. We successfully navigated to the spot and took samples. The preliminary check shows cancer cells, but we need special tests to tell exactly which type it is.",
            9: "Procedure: EMN-guided pulmonary sampling.\nContext: Pulmonary nodule with history of colorectal malignancy.\nTechnique: Navigational localization with REBUS verification.\nFindings: Malignant cytology. \nDisposition: Discharge pending final diagnosis."
        },
        8: { # Jennifer Taylor (EMN + Cryo RML)
            1: "Indication: RML nodule (part-solid).\nProcedure: EMN Bronch + Cryobiopsy.\nGuidance: REBUS (concentric).\nSampling: Forceps x6, Cryo x2.\nROSE: Adenocarcinoma.\nComplication: None.",
            2: "PROCEDURE: Electromagnetic navigation bronchoscopy was performed to assess a part-solid RML nodule. Following radial EBUS confirmation, initial forceps biopsies suggested adenocarcinoma on ROSE. To ensure adequate tissue for molecular testing, transbronchial cryobiopsy was subsequently performed with a bronchial blocker in place for hemostasis. The procedure was uncomplicated.",
            3: "Billing: 31627 (Nav), 31654 (REBUS), 31628 (Forceps biopsy), 31632 (Cryobiopsy - add-on lobe? No same lobe -> usually 31628 covers TBBx, but some code cryo as 31628 or distinct. If same lobe, usually just 31628 x1 unit, but maybe 31629 TBNA if done? Note says Forceps and Cryo. Usually just one 31628 per lobe).",
            4: "EMN + Cryo\nPatient: Jennifer Taylor\nTarget: RML nodule\nSteps:\n1. Navigated to RML.\n2. REBUS confirm.\n3. Forceps biopsy -> ROSE pos.\n4. Cryobiopsy for molecular.\n5. Blocker used.\nPlan: D/C.",
            5: "Jennifer has a RML nodule. Used superdimension. Found it with EBUS. Took regular biopsies and then cryo biopsies to get more tissue for gene testing. ROSE said adenocarcinoma. No bleeding problems.",
            6: "Electromagnetic navigation bronchoscopy, Radial endobronchial ultrasound, Transbronchial lung biopsy, Transbronchial cryobiopsy. Patient is a 62-year-old female. RML lateral segment nodule identified. Radial EBUS showed concentric pattern. Conventional forceps biopsies obtained. ROSE suggested adenocarcinoma. Cryobiopsies obtained for molecular testing. Bronchial blocker used for hemostasis. No complications.",
            7: "[Indication]\nRML part-solid nodule.\n[Anesthesia]\nModerate sedation.\n[Description]\nEMN to RML. REBUS. Forceps biopsy. Cryobiopsy for molecular. ROSE positive.\n[Plan]\nDischarge. Molecular testing.",
            8: "Ms. Taylor had a biopsy of a nodule in her right middle lung. We used navigation to find it and took standard biopsies. Because it looked like cancer, we also used a special freezing probe to get larger pieces of tissue for genetic testing, which will help guide her treatment. She is doing well.",
            9: "Procedure: EMN-guided biopsy with cryo-sampling.\nTarget: RML lesion.\nMethod: Navigation and ultrasonic confirmation.\nAction: Forceps and cryo-extraction of tissue.\nPurpose: Diagnosis and molecular profiling."
        },
        9: { # Catherine Lee (Robotic RML)
            1: "Indication: RML nodule (1.8cm).\nProcedure: Ion Robotic Bronch.\nGuidance: REBUS + CBCT.\nSampling: TBBx x5, Brush x2.\nROSE: Atypical/Bronchioloalveolar.\nPlan: F/u path.",
            2: "PROCEDURE: Robotic-assisted bronchoscopy (Ion) was utilized to biopsy a 1.8 cm RML nodule in a patient with a history of breast cancer. Navigation was facilitated by radial EBUS and Cone-Beam CT fusion. Transbronchial biopsies and brushings were obtained. Preliminary cytopathology showed bronchioloalveolar cells without definitive malignancy, pending final review.",
            3: "Codes: 31627 (Nav), 31654 (REBUS), 31628 (Biopsy), 31623 (Brush), 31624 (BAL).\nRationale: Robotic navigation to RML. Standard sampling bundle.",
            4: "Robotic Bronch\nPatient: Catherine Lee\nTarget: RML nodule\nSteps:\n1. Ion registration.\n2. Nav to RML medial segment.\n3. Confirmed with REBUS/CBCT.\n4. Biopsies taken.\n5. ROSE indeterminate/benign?\nPlan: Wait for final.",
            5: "Catherine has a spot in the RML and breast cancer history. Used the Ion robot. Found the spot easily. Took biopsies. Rose didn't show obvious cancer but we will see what the final path says. She went home.",
            6: "Robotic bronchoscopy (Intuitive Ion platform), radial endobronchial ultrasound, transbronchial biopsy. Patient is a 72-year-old female with RML nodule. Virtual pathway generated to RML medial segment. Radial EBUS demonstrated concentric hypoechoic pattern. CBCT performed. TBBx and cytology brush specimens obtained. ROSE showed bronchioloalveolar cells, no definitive malignancy. Complications: None.",
            7: "[Indication]\nRML nodule, hx breast CA.\n[Anesthesia]\nGeneral.\n[Description]\nIon nav to RML. REBUS/CBCT confirm. Biopsies taken. ROSE indeterminate.\n[Plan]\nFollow-up pathology.",
            8: "We used the robotic bronchoscope to check a nodule in Ms. Lee's right middle lung. We navigated to the site and took samples. The initial look at the cells didn't show cancer, but we need to wait for the full report to be sure. It could be benign or related to her history, but for now, it looks reassuring.",
            9: "Procedure: Robotic navigational biopsy.\nTarget: RML medial segment nodule.\nTechnique: Ion system with REBUS and CBCT.\nFindings: ROSE indeterminate for malignancy.\nDisposition: Discharged."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages
    # Correspond to the 10 notes in Part 030
    return [
        {"idx": 0, "orig_name": "Anjali Patel", "orig_age": 45, "names": ["Priya Sharma", "Mei Lin", "Sarah Gupta", "Nina Patel", "Zara Ali", "Leila Hassan", "Aisha Khan", "Fatima Ahmed", "Riya Singh"]},
        {"idx": 1, "orig_name": "Robert Williams", "orig_age": 71, "names": ["James Brown", "John Smith", "David Jones", "Michael Johnson", "William Davis", "Richard Miller", "Joseph Wilson", "Thomas Moore", "Charles Taylor"]},
        {"idx": 2, "orig_name": "Michelle Chen", "orig_age": 71, "names": ["Betty White", "Susan Green", "Helen Clark", "Margaret Hall", "Dorothy Lewis", "Ruth Young", "Shirley King", "Barbara Wright", "Elizabeth Scott"]},
        {"idx": 3, "orig_name": "Carlos Rodriguez", "orig_age": 59, "names": ["Juan Martinez", "Jose Hernandez", "Luis Garcia", "Jorge Lopez", "Antonio Gonzalez", "Pedro Perez", "Miguel Sanchez", "Ricardo Ramirez", "Fernando Torres"]},
        {"idx": 4, "orig_name": "Jennifer Wu", "orig_age": 52, "names": ["Linda Kim", "Karen Lee", "Nancy Park", "Lisa Choi", "Sandra Chang", "Donna Han", "Carol Yang", "Sharon Lim", "Brenda Ng"]},
        {"idx": 5, "orig_name": "Robert Thompson", "orig_age": 61, "names": ["Paul Anderson", "Mark Thomas", "Donald Jackson", "George White", "Kenneth Harris", "Steven Martin", "Edward Thompson", "Brian Garcia", "Ronald Martinez"]},
        {"idx": 6, "orig_name": "Patricia Johnson", "orig_age": 66, "names": ["Mary Robinson", "Patricia Clark", "Linda Rodriguez", "Barbara Lewis", "Elizabeth Lee", "Jennifer Walker", "Maria Hall", "Susan Allen", "Margaret Young"]},
        {"idx": 7, "orig_name": "Manuel Garcia", "orig_age": 77, "names": ["Roberto Hernandez", "Francisco Lopez", "Carlos Gonzalez", "Jesus Perez", "Angel Sanchez", "Jose Ramirez", "Manuel Torres", "Juan Flores", "Pedro Rivera"]},
        {"idx": 8, "orig_name": "Jennifer Taylor", "orig_age": 62, "names": ["Deborah King", "Lisa Wright", "Karen Scott", "Nancy Green", "Betty Baker", "Helen Adams", "Sandra Nelson", "Donna Carter", "Carol Mitchell"]},
        {"idx": 9, "orig_name": "Catherine Lee", "orig_age": 72, "names": ["Ruth Roberts", "Shirley Phillips", "Barbara Evans", "Elizabeth Turner", "Margaret Torres", "Dorothy Parker", "Martha Collins", "Alice Edwards", "Jean Stewart"]}
    ]

def main():
    # Load original data from source file
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        print("Please ensure the file exists or update SOURCE_FILE path.")
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
            # Handle potential missing index in variations_text if data mismatch
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing variation text for Note {idx}, Style {style_num}")
                continue
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
                
                # Update the note text inside registry_entry if it exists (some formats duplicate it)
                if "note_text" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["note_text"] = variations_text[idx][style_num]

            
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
    output_filename = output_dir / "synthetic_blvr_notes_part_030.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()