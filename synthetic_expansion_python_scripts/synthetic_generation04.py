import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_004.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Linda Chen (Rigid Bronch, Tumor Debulking, Stent)
            1: "Indication: Airway obstruction, squamous cell CA.\nProc: Rigid bronch, mechanical debridement, APC, stent.\nSteps:\n- Rigid scope inserted.\n- 90% obstruction LMS visualized.\n- Tumor cored/debrided (15cc).\n- Base cauterized (APC/Bovie).\n- 14x60mm Dumon stent placed.\n- Final: Patent lumen, no bleeding.\nPlan: ICU, surveillance bronch.",
            2: "HISTORY: The patient, a 72-year-old female with advanced squamous cell carcinoma, presented with critical central airway obstruction. \nPROCEDURE: Under general anesthesia with jet ventilation, the airway was accessed via a 14mm rigid bronchoscope. Significant endobronchial tumor burden was identified in the left mainstem bronchus. Multimodal recanalization was performed utilizing mechanical coring, electrocautery, and argon plasma coagulation, resulting in restoration of patency. To maintain airway caliber, a 14x60mm silicone stent was deployed. \nCONCLUSION: Successful rigid bronchoscopy with tumor destruction and stent placement.",
            3: "Procedures Performed:\n- 31640: Rigid bronchoscopy with excision of tumor (Mechanical debulking of LMS).\n- 31641: Destruction of tumor (APC/Cautery).\n- 31636: Stent placement (Revision/Placement of bronchial stent).\nMedical Necessity: Critical airway obstruction (90% LMS stenosis).\nTechnique: Rigid barrel used for coring; stent deployed under direct vision. Hemostasis achieved.",
            4: "Procedure Note\nPatient: Linda Chen\nAttending: Dr. Anderson\nDiagnosis: Malignant Airway Obstruction\nSteps:\n1. Time out done. GA induced.\n2. Rigid scope to trachea.\n3. LMS 90% blocked by tumor.\n4. Mechanical debulking and APC used to clear airway.\n5. Silicone stent (14x60) placed in LMS.\n6. Airway patent at end of case.\nPlan: ICU for monitoring.",
            5: "procedure note for ms chen she has the squamous cell ca with stridor we did the rigid bronch today anesthesia gave the propofol. went down with the 14mm scope left main was tight like 90 percent blocked. used the coring technique and some apc to burn the base got it open pretty good. put a dumon stent in there 14 by 60 fits nice. no bleeding stopped with epi. woke up fine sent to recovery.",
            6: "Ms. Chen is a 72-year-old female with known squamous cell lung cancer presenting with worsening dyspnea and stridor. CT chest shows near-complete obstruction of the left mainstem bronchus by endobronchial tumor. A rigid bronchoscope (14mm) was introduced via the mouth under direct visualization. High-frequency jet ventilation (HFJV) was utilized. Left mainstem was 90% obstructed by friable, hemorrhagic endobronchial tumor. The tumor was cored using the rigid bronchoscope with mechanical debridement. Residual tumor base was treated with electrocautery and Argon Plasma Coagulation. A 14mm x 60mm Dumon silicone stent was deployed in the left mainstem bronchus. Prior to treatment, left mainstem bronchus was 10% patent. After treatment, the airway was 70% patent.",
            7: "[Indication]\nSymptomatic malignant airway obstruction, LMS.\n[Anesthesia]\nGeneral, TIVA, Jet Ventilation.\n[Description]\nRigid bronchoscopy performed. 90% obstruction of LMS identified. Mechanical debridement and APC destruction performed. 14x60mm silicone stent placed. Airway patency restored to 70%.\n[Plan]\nICU admission. Follow-up bronchoscopy 4 weeks.",
            8: "The patient was brought to the operating room for management of her malignant airway obstruction. After induction of general anesthesia, we inserted the rigid bronchoscope. The left mainstem bronchus was found to be critically narrowed by tumor. We proceeded to core out the tumor mechanically and applied thermal energy to the base to prevent regrowth and bleeding. Once the airway was opened, we sized and placed a silicone stent to ensure it remained patent. The patient tolerated the procedure well and was transferred to the ICU.",
            9: "Operation: Rigid endoscopy with tumor eradication and stent insertion.\nContext: Critical blockage of the left bronchial tube.\nAction: The rigid barrel was navigated to the obstruction. The malignancy was excised mechanically and ablated with argon plasma. A silicone prosthesis was positioned to scaffold the airway.\nResult: The bronchial lumen was re-established. Hemostasis was secured."
        },
        1: { # Anjali Patel (Ion Robotic, Bilateral Nodules)
            1: "Indication: Bilateral lung nodules (RUL, LUL).\nAnesthesia: GA, 7.5 ETT.\nNav: Ion Robotic System.\nTargets:\n1. RUL Anterior: Navigated, confirmed REBUS/Fluoro. Bx x6, Brush x2.\n2. LUL Apical-Posterior: Repositioned. Confirmed REBUS. Bx x5, Brush x2.\nROSE: Atypical cells, favor adenocarcinoma (both).\nComp: None. No PTX.",
            2: "PROCEDURE: Robotic-assisted bronchoscopy (Ion platform) with bilateral peripheral nodule sampling.\nCLINICAL SUMMARY: 45-year-old female with PET-avid nodules in the RUL and LUL.\nOPERATIVE REPORT: Following registration (fiducial error 0.9mm), the robotic catheter was navigated sequentially to the RUL anterior segment and LUL apical-posterior segment targets. Radial EBUS confirmed concentric views at both sites. Transbronchial biopsies and brushings were obtained. Rapid on-site evaluation suggested adenocarcinoma in both lesions, implying synchronous primaries or metastasis. The patient was extubated without complication.",
            3: "Codes: 31627 (Navigational Bronchoscopy), 31654 (REBUS), 31628 (Biopsy RUL), 31632 (Biopsy LUL).\nTechnique: Ion Robotic System used for guidance.\nTargets: Two distinct lesions (RUL, LUL).\nVerification: Radial EBUS and Fluoroscopy used for tool-in-lesion confirmation.\nSamples: Multiple forceps passes obtained from each site.\nOutcome: Diagnosis obtained (Adenocarcinoma).",
            4: "Procedure: Ion Bronchoscopy\nPatient: Anjali Patel\nStaff: Dr. Hayes\nSteps:\n1. ETT placed. Ion registered (auto).\n2. Drove to RUL nodule. REBUS concentric. Biopsied.\n3. Drove to LUL nodule. REBUS concentric. Biopsied.\n4. ROSE read: Adeno for both.\n5. No bleeding. Extubated.\nPlan: Staging w/ PET/MRI. Tumor board.",
            5: "patient anjali patel here for the robotic bronch she has two spots one right one left. used the ion system general anesthesia. registered the airway looks good. went to the right upper lobe first found the nodule on radar probe took biopsies rose said cancer. then went to the left upper lobe same thing radar confirmed took biopsies rose said cancer again. so looks like bilateral disease. no pneumo on the xray.",
            6: "Ion Robotic Bronchoscopy, Bilateral Nodule Sampling. 45F never-smoker with incidental bilateral lung nodules. Pre-procedure CT loaded to Ion system. Dual-target navigation plan created. Ion catheter navigated to RUL anterior segment. Tool-at-target confirmed by Navigation software and Radial EBUS. Forceps biopsy x6 and Brushings x2 obtained. Catheter repositioned to LUL. Radial EBUS showed concentric pattern. Forceps biopsy x5 and Brushings x2 obtained. ROSE: Atypical pneumocytes, favor adenocarcinoma for both sites. Successful bilateral lung nodule sampling via robotic bronchoscopy.",
            7: "[Indication]\nBilateral PET-avid nodules (RUL 2.1cm, LUL 1.6cm).\n[Anesthesia]\nGeneral, ETT 7.5.\n[Description]\nIon robotic navigation used. RUL target localized (REBUS concentric), biopsied. LUL target localized (REBUS concentric), biopsied. ROSE positive for adenocarcinoma at both sites.\n[Plan]\nFinal path pending. Staging MRI/PET. Oncology referral.",
            8: "Ms. Patel presented for biopsy of bilateral lung nodules. We utilized the Ion robotic platform to navigate to the lesions in the right upper and left upper lobes. Once navigation was complete, we used radial EBUS to confirm we were centered in the lesions. Biopsies were taken from both sites, and the pathologist in the room felt both showed adenocarcinoma. The procedure went smoothly, and she was woken up and taken to recovery.",
            9: "Procedure: Robotic-assisted endoscopy with bilateral nodule interrogation.\nFindings: RUL and LUL lesions identified.\nAction: The robotic catheter was steered to the targets. Lesion position was corroborated via ultrasound. Tissue was harvested using forceps and brushes.\nResult: Cytopathology indicates malignancy in both locations."
        },
        2: { # Michelle Chen (EBUS + Ion + Cryo)
            1: "Indication: RLL mass + mediastinal LAD.\nProcedures: EBUS-TBNA, Ion Nav, Cryobiopsy.\nEBUS: Stn 4L (neg), 10R (pos - adeno).\nIon: Nav to RLL mass. REBUS concentric.\nBiopsy: Forceps x6, Cryo x2 (with blocker).\nROSE: Adenocarcinoma (N1 positive).\nPlan: Oncology for Stage IIIA.",
            2: "PROCEDURE: Combined Endobronchial Ultrasound and Robotic Navigational Bronchoscopy.\nCLINICAL CONTEXT: 71-year-old female with RLL mass and lymphadenopathy.\nNARRATIVE: EBUS-TBNA was performed first; Station 10R was positive for adenocarcinoma. The Ion robotic catheter was then navigated to the RLL superior segment mass. Following radial EBUS confirmation, both conventional forceps biopsies and cryobiopsies (using an endobronchial blocker for prophylaxis) were obtained. ROSE confirmed adenocarcinoma in the primary lesion as well.\nIMPRESSION: Stage IIIA NSCLC (T1c N1 M0).",
            3: "Coding:\n- 31653: EBUS TBNA (10R, 4L).\n- 31627: Navigation (Ion).\n- 31654: Radial EBUS.\n- 31628: Transbronchial biopsy.\nNote: Cryobiopsy performed for molecular yield.\nPathology: Confirmed malignancy in node and lung.",
            4: "Procedure: EBUS + Ion\nPatient: Michelle Chen\nSteps:\n1. EBUS scope in. Sampled 4L (neg) and 10R (pos).\n2. Switched to Ion robot.\n3. Navigated to RLL mass.\n4. REBUS check.\n5. Took forceps bx and cryo bx (used blocker).\n6. No bleeding issues.\nResult: Adeno in lung and hilar node.",
            5: "Michelle Chen 71 female here for staging. did the ebus first 4L looked ok but 10R was suspicious so we stuck it rose said cancer. then switched to the robot for the lung mass RLL. drove out there confirmed with ultrasound. took some bites with forceps then did the cryo probe for bigger pieces used a blocker just in case. mild bleeding stopped with ice. diagnosis is stage 3 lung cancer.",
            6: "Procedures done: EBUS with TBNA (mediastinal + hilar staging), Ion robotic bronchoscopy (RLL mass biopsy), Radial EBUS, Cryobiopsy of RLL mass. EBUS Phase: Station 4L sampled (ROSE negative). Station 10R sampled (ROSE positive for adenocarcinoma). Ion Robotic Bronchoscopy Phase: Target identified RLL superior segment mass. Radial EBUS verification: Concentric. Cryobiopsy: Arndt blocker (7Fr) placed in RLL ostium. Cryoprobe (1.9mm) advanced. Freeze x 4 seconds. Sample obtained. Mild bleeding after cryobiopsies managed with iced saline and blocker.",
            7: "[Indication]\nRLL mass, hilar adenopathy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS-TBNA performed: 10R positive for malignancy. Ion navigation to RLL mass. REBUS confirmed position. Forceps and Cryobiopsies obtained. Primary lesion confirmed adenocarcinoma.\n[Plan]\nMolecular testing. Oncology consult for Stage IIIA.",
            8: "We performed a combined staging and diagnostic procedure for Ms. Chen. First, using the EBUS scope, we sampled the lymph nodes; the right hilar node was positive for cancer. We then switched to the robotic system to biopsy the main mass in the right lower lobe. We used a cryoprobe to get large tissue samples for genetic testing, utilizing a balloon blocker to safely manage any bleeding. The preliminary results show adenocarcinoma spread to the nearby lymph nodes.",
            9: "Operation: Endobronchial ultrasound staging and robotic parenchymal sampling.\nFindings: Metastatic spread to Station 10R.\nAction: Lymph nodes were aspirated. The robotic scope was guided to the RLL tumor. Tissue was extracted via forceps and cryo-adhesion.\nResult: Adenocarcinoma confirmed in both the primary site and regional nodes."
        },
        3: { # Carlos Rodriguez (EBUS + EMN + Airway Inspection)
            1: "Indication: LLL mass, extensive LAD.\nFindings: LLL orifice blocked by tumor. Extensive nodes.\nProcedures: EBUS (4R, 4L, 7, 10L, 11L - all pos). Endobronchial Bx LLL. EMN to peripheral mass.\nROSE: Squamous cell carcinoma.\nStage: IIIB/IV (N3 disease).\nPlan: Oncology (Chemo/Rad).",
            2: "PROCEDURE: EBUS-TBNA and EMN Bronchoscopy.\nNARRATIVE: Extensive mediastinal staging revealed malignancy in stations 4R, 4L, 7, 10L, and 11L, confirming N3 disease. Airway inspection demonstrated exophytic tumor occluding the LLL bronchus; endobronchial biopsies were obtained. To maximize tissue for profiling, EMN guidance was used to sample the peripheral component of the mass. All sites confirmed squamous cell carcinoma.\nIMPRESSION: Advanced stage squamous cell lung cancer.",
            3: "Codes: 31653 (EBUS multiple stations), 31627 (Nav), 31654 (REBUS), 31628 (TBBx), 31623 (Brush), 31625 (Endobronchial Bx).\nJustification: Extensive staging (N3) and sampling of primary via two approaches (direct and nav) for molecular sufficiency.",
            4: "Procedure: EBUS & EMN\nPatient: Carlos Rodriguez\nSteps:\n1. EBUS: Sampled 4R, 4L, 7, 10L, 11L. All positive.\n2. White light: Saw tumor in LLL airway. Biopsied.\n3. EMN: Navigated to distal part of mass for more tissue.\n4. Bleeding controlled w/ epi.\nDiagnosis: Squamous cell CA, Stage IIIB.",
            5: "Mr Rodriguez has a big mass LLL and nodes everywhere. Did EBUS first sampled everything 4R 4L 7 10L 11L all squamous cancer. Then looked with regular scope tumor was growing right out of the LLL so we grabbed some of that. Used the superdimension to go deeper and get more tissue too. He has N3 disease so not a surgery candidate. Oncology will treat him.",
            6: "EBUS-TBNA, Electromagnetic navigation bronchoscopy, Radial EBUS, Transbronchial biopsies, Endobronchial biopsies. EBUS Phase: Station 4R, 4L, 7, 10L, 11L sampled. ROSE: \"Positive - squamous cell carcinoma\" for all. Airway Inspection: LLL orifice shows endobronchial tumor. Endobronchial biopsies obtained. EMN to Peripheral Component: Navigation to LLL superior segment. Radial EBUS visualized mass. Peripheral sampling performed. Extensive N2/N3 disease confirmed.",
            7: "[Indication]\nLLL mass, mediastinal adenopathy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS-TBNA of stations 4R, 4L, 7, 10L, 11L (all positive). Endobronchial tumor seen in LLL, biopsied. EMN navigation used to sample peripheral mass component. Diagnosis: Squamous cell carcinoma.\n[Plan]\nRefer to Medical Oncology. Not surgical candidate.",
            8: "We performed a comprehensive staging procedure on Mr. Rodriguez. The ultrasound showed cancer in lymph nodes on both sides of the chest (N3 disease). We also found the tumor growing into the main airway of the left lower lobe, which we biopsied directly. To ensure we had enough tissue for testing, we also navigated to the deeper part of the tumor. The diagnosis is squamous cell carcinoma, and he will need chemotherapy and radiation.",
            9: "Procedure: Mediastinal staging and pulmonary biopsy.\nContext: Advanced LLL malignancy.\nAction: Multi-station nodal aspiration confirmed N3 spread. Direct forceps sampling of the endobronchial tumor was performed. Navigational guidance facilitated peripheral tissue acquisition.\nResult: Squamous cell carcinoma confirmed in all samples."
        },
        4: { # Jennifer Wu (Combined EBUS + Ion + Cryo)
            1: "Indication: RUL nodule (2.4cm), Node 4R.\nProc: EBUS (4R+, 10R-), Ion Nav, Cryobiopsy.\nDetails: 4R pos for Adeno. 10R neg. Ion nav to RUL posterior seg. REBUS concentric. Cryo x2 taken.\nROSE: Adenocarcinoma.\nStage: IIIA (N2).\nPlan: Tumor board, likely neoadjuvant.",
            2: "PROCEDURE: Combined EBUS-TBNA and Ion Robotic Bronchoscopy with Cryobiopsy.\nSUMMARY: 52F with RUL nodule. EBUS demonstrated metastasis to the 4R lymph node (N2 disease), while the 10R node was negative. The Ion system was utilized to navigate to the RUL peripheral nodule. Cryobiopsy was employed to obtain high-quality tissue for molecular profiling. Pathology confirmed adenocarcinoma.\nIMPRESSION: Stage IIIA Lung Adenocarcinoma.",
            3: "CPT: 31653 (EBUS), 31627 (Nav), 31654 (REBUS), 31628 (Biopsy), 31632 (Cryo add-on).\nNotes: 4R sampled (pos). Ion used for peripheral lesion. Cryo used for tissue volume (molecular).",
            4: "Procedure: EBUS/Ion/Cryo\nPatient: Jennifer Wu\nSteps:\n1. EBUS: 4R pos, 10R neg.\n2. Ion: Navigated to RUL nodule.\n3. Confirmed with REBUS and CBCT.\n4. Cryobiopsy x2 with blocker.\n5. Bleeding minimal.\nResult: Adeno, N2 disease.",
            5: "Jennifer Wu here for the RUL spot. EBUS showed the 4R node was cancer so shes stage 3. 10R was clear. Used the ion robot to get to the lung nodule. Radial probe looked concentric. Did the cryo biopsy to get good tissue for the mutation testing. Everything is adenocarcinoma. She needs chemo before surgery probably.",
            6: "COMBINED EBUS + ROBOTIC BRONCHOSCOPY. Procedures: EBUS-TBNA (mediastinal staging), Ion robotic bronchoscopy, Radial EBUS, Transbronchial biopsy with cryobiopsy. PHASE 1 EBUS: Station 4R positive for adenocarcinoma. Station 10R negative. PHASE 2 ION: Target RUL posterior segment nodule. Registration Process: Automatic. Navigation to Target: Tool-to-target distance 0.5cm. Radial EBUS: Concentric. Cryobiopsy Procedure: 1.9mm cryoprobe advanced. Freeze time: 4 seconds. Blocker inflated. Final Path: Adenocarcinoma, N2 disease.",
            7: "[Indication]\nRUL nodule, 4R lymph node.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS: 4R positive (Adeno), 10R negative. Ion Nav: RUL nodule biopsied via cryoprobe. REBUS/CBCT confirmation used. Diagnosis: Adenocarcinoma.\n[Plan]\nComplete staging (MRI). Tumor board. Neoadjuvant therapy.",
            8: "Ms. Wu underwent a combined procedure to diagnose her lung nodule and check her lymph nodes. The EBUS showed cancer in the lymph nodes in the middle of her chest (Station 4R), but the node closer to the lung (10R) was clear. We then used the robot to biopsy the lung nodule itself, using a freezing probe to get a large sample. The diagnosis is adenocarcinoma, and because it has spread to the mediastinal nodes, we will discuss chemotherapy options.",
            9: "Procedure: Ultrasonic mediastinal staging and robotic cryo-sampling.\nFindings: N2 nodal involvement.\nAction: EBUS-TBNA confirmed malignancy in station 4R. The robotic catheter was driven to the RUL lesion. Cryo-adhesion was used to harvest tissue under balloon occlusion.\nResult: Adenocarcinoma confirmed."
        },
        5: { # Robert Thompson (EBUS + EMN + BAL)
            1: "Indication: LLL mass, LAD.\nProc: EBUS (5, 7, 10L), EMN Bronch, BAL.\nFindings: EBUS Stn 5, 7, 10L all positive (Adeno). EMN to LLL mass (concentric REBUS). Bx x8, BAL.\nROSE: Adenocarcinoma.\nStage: IIIB (N3 - contralateral 5).\nPlan: Med Onc, palliative.",
            2: "PROCEDURE: EBUS-TBNA and EMN Bronchoscopy.\nCLINICAL SUMMARY: 61M with LLL mass and multi-station adenopathy.\nNARRATIVE: Systematic EBUS staging revealed metastatic adenocarcinoma in stations 5 (contralateral), 7, and 10L, confirming N3 disease. EMN guidance was used to navigate to the LLL primary mass. Radial EBUS confirmed lesion location. Transbronchial biopsies and BAL were obtained. Final pathology is consistent with advanced adenocarcinoma.\nIMPRESSION: Unresectable Stage IIIB NSCLC.",
            3: "Codes: 31653 (EBUS), 31627 (Nav), 31654 (REBUS), 31628 (Bx), 31624 (BAL).\nDetails: EBUS performed on 5, 7, 10L. EMN used for LLL peripheral mass. BAL for micro/cyto.",
            4: "Procedure: EBUS & EMN\nPatient: Robert Thompson\nSteps:\n1. EBUS: 5, 7, 10L all positive for cancer.\n2. Navigated to LLL mass with SuperDimension.\n3. REBUS showed concentric view.\n4. Taken 8 biopsies and BAL.\n5. No complications.\nDx: Stage IIIB Adeno.",
            5: "Robert Thompson 61 male LLL mass. EBUS showed cancer everywhere station 5 7 and 10L so its N3. Went after the lung mass with the navigation system. Found it with the ultrasound probe. Took a bunch of biopsies and a lavage. Its adenocarcinoma. Hes not a surgical candidate so referred to oncology.",
            6: "Endobronchial Ultrasound with Transbronchial Needle Aspiration (EBUS-TBNA), Electromagnetic Navigation Bronchoscopy (SuperDimension), Radial Endobronchial Ultrasound (rEBUS), Transbronchial Lung Biopsy (TBBx), Bronchoalveolar Lavage (BAL). EBUS Summary: N3 disease documented (Station 5), N2 disease (Station 7), N1 disease (Station 10L). EMN Bronchoscopy: Target LLL posterior basal segment mass. Registration landmarks confirmed. Navigation to target successful. Radial EBUS: Concentric. Tissue Acquisition: 8 biopsies, 4 brushes, BAL. ROSE: Adenocarcinoma.",
            7: "[Indication]\nLLL mass, mediastinal nodes.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEBUS: Stations 5, 7, 10L sampled and positive for Adeno. EMN: LLL mass localized and biopsied. BAL performed. Diagnosis: Stage IIIB Adenocarcinoma.\n[Plan]\nMRI Brain. Oncology referral for chemo/immunotherapy.",
            8: "We performed a staging bronchoscopy for Mr. Thompson. The ultrasound sampling of his lymph nodes showed extensive spread, including to the other side of his chest (Station 5) and the subcarinal area (Station 7). We also biopsied the main tumor in the left lower lobe using the navigation system. The results confirm advanced adenocarcinoma (Stage IIIB), so surgery is not an option. We will coordinate with oncology for systemic therapy.",
            9: "Procedure: Multi-station nodal staging and navigational biopsy.\nFindings: Contralateral mediastinal involvement.\nAction: EBUS-TBNA of stations 5, 7, and 10L yielded malignant cells. The EMN system guided the scope to the LLL primary. Forceps biopsies and lavage were executed.\nResult: Advanced adenocarcinoma (N3)."
        },
        6: { # Emily Richardson (Rigid Bronch, Y-Stent)
            1: "Indication: Resp failure, tracheal compression.\nProc: Rigid bronch, Y-stent.\nDetails: 90% tracheal obstruction (extrinsic). Rigid scope dilated airway. 16x13x13 Y-stent placed. Airway stable.\nPlan: ICU, humidification.",
            2: "PROCEDURE: Rigid Bronchoscopy with Silicone Y-Stent Placement.\nINDICATION: Critical extrinsic tracheal compression.\nNARRATIVE: The patient was intubated with a 14mm rigid bronchoscope. Severe extrinsic compression of the mid-trachea and mainstems was visualized. A customized silicone Y-stent (16x13x13) was deployed, securing the carina and bilateral mainstem bronchi. Post-deployment inspection confirmed patent airways and resolution of the obstruction.\nIMPRESSION: Successful palliation of central airway obstruction.",
            3: "Codes: 31631 (Stent placement), 31633 (Add-on stent), 31637 (Revision/Complex).\nTechnique: Rigid bronchoscopy used to stent trachea and mainstems (Y-stent covers multiple zones).",
            4: "Procedure: Rigid Bronch & Stent\nPatient: Emily Richardson\nSteps:\n1. GA/Paralytics. Rigid scope inserted.\n2. Saw 90% compression of trachea.\n3. Measured for stent.\n4. Deployed Y-stent (Silicone).\n5. Check with flex scope: Good position.\n6. LMA placed for wake up.\nPlan: ICU.",
            5: "Emily Richardson here for the airway stent she has compression from outside. rigid bronch went in trachea was crushed flat. Put in a Y stent silicone type into the trachea and both main bronchi. Opened it up nicely. No bleeding. Swapped to LMA and woke her up. ICU for monitoring.",
            6: "Procedure Performed: Rigid bronchoscopy, Silicone Y-stent placement, bronchoscopic intubation. Indications: Severe extrinsic tracheal compression. Description: 90% obstruction of the tracheal lumen. No endobronchial tumor. 14 mm ventilating rigid bronchoscope was inserted. Customized 16x13x13 silicone Y-stent deployed. Stent well placed with near complete resolution of central airway obstruction.",
            7: "[Indication]\nExtrinsic tracheal compression, respiratory failure.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n90% tracheal stenosis. 16x13x13 Y-stent deployed. Airway patency restored.\n[Plan]\nICU. Hypertonic saline nebs.",
            8: "Ms. Richardson was in respiratory failure due to her windpipe being compressed from the outside. We took her to the OR and used a rigid bronchoscope to open the airway. We placed a silicone Y-shaped stent that sits in the trachea and branches into both lungs. This immediately propped the airway open. She is breathing much better now and will go to the ICU.",
            9: "Operation: Rigid airway cannulation and Y-prosthesis insertion.\nReason: Extrinsic compression.\nAction: The rigid barrel bypassed the stenosis. A silicone Y-stent was customized and implanted at the carina. The airway structural integrity was restored.\nResult: Relief of obstruction."
        },
        7: { # Maria Gonzalez (Indwelling Pleural Catheter)
            1: "Indication: Recurrent malignant effusion (Breast CA).\nProc: PleurX catheter placement.\nSite: Right 6th ICS.\nDetails: US guidance. Tunnel created. 15.5Fr catheter inserted. 1.4L drained.\nCXR: Good position.\nPlan: Home drainage education.",
            2: "PROCEDURE: Tunneled Indwelling Pleural Catheter (IPC) Insertion.\nINDICATION: Trapped lung/Recurrent malignant pleural effusion.\nNARRATIVE: Under ultrasound guidance, the right pleural space was accessed. A subcutaneous tunnel was created, and a 15.5Fr PleurX catheter was inserted using the Seldinger technique. 1450mL of fluid was evacuated. Post-procedure imaging confirmed appropriate placement. Patient education on drainage was completed.\nIMPRESSION: Successful IPC placement.",
            3: "Code: 32550 (Insertion of Tunneled Pleural Catheter).\nGuidance: Ultrasound used for site selection.\nDevice: PleurX 15.5Fr.\nOutput: 1450mL drainage.\nMedical Necessity: Palliation of recurrent malignant effusion.",
            4: "Procedure: IPC Placement\nPatient: Maria Gonzalez\nSteps:\n1. US marked site (Rt chest).\n2. Lidocaine. Incision.\n3. Tunneled catheter.\n4. Inserted into pleural space.\n5. Drained 1.4L fluid.\n6. CXR checked.\nPlan: Discharge with home health.",
            5: "Maria Gonzalez needs a pleurx for her effusion breast cancer history. Did the ultrasound marked the spot. Numbed it up tunnelled the catheter put it in the right chest. Drained about a liter and a half yellow fluid. Catheter works good. CXR looks okay. Teaching her how to use the bottles.",
            6: "Ultrasound-guided placement of right indwelling pleural catheter. 57-year-old female with metastatic breast cancer and recurrent right malignant pleural effusion. Right hemithorax, 6th intercostal space. Subcutaneous tunnel created. 15.5 French PleurX catheter advanced. Initial therapeutic drainage: 1,450 mL clear yellow fluid. Post-procedure portable chest X-ray: IPC in good position. Discharge with home health.",
            7: "[Indication]\nRecurrent malignant pleural effusion, trapped lung.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nUS-guided right IPC (PleurX) placement. Tunneled technique. 1450mL drained. Good position on CXR.\n[Plan]\nHome drainage education. Oncology follow-up.",
            8: "Ms. Gonzalez has fluid building up around her lung due to her breast cancer. Since the lung is trapped and won't stick to the chest wall, we placed a permanent drain (PleurX catheter). We used ultrasound to find the safe spot, numbed the skin, and tunneled the tube under the skin before putting it into the fluid pocket. We drained over a liter of fluid, which should help her breathing. She will go home and drain it as needed.",
            9: "Procedure: Insertion of tunneled pleural drainage conduit.\nContext: Refractory malignant effusion.\nAction: Utilizing sonographic localization, the catheter was tunneled and introduced into the pleural cavity. 1.45L of exudate was evacuated.\nResult: Effective drainage established."
        },
        8: { # Lisa Marie Thompson (EBUS TBNA - Staging)
            1: "Indication: Right hilar mass, LAD.\nProc: EBUS-TBNA.\nFindings: Stn 7 (4.1cm) - Pos. Stn 4R (3.2cm) - Pos. Stn 10R/11R sampled.\nROSE: Malignant cells (N2 disease).\nPlan: Oncology consult.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nCLINICAL CONTEXT: Staging for right hilar mass.\nNARRATIVE: The mediastinum was systematically surveyed. Enlarged, hypoechoic lymph nodes were identified at stations 7 and 4R. TBNA was performed with a 22G needle. ROSE confirmed malignancy in both N2 stations (7 and 4R). This confirms Stage IIIA/B disease depending on T-stage.\nIMPRESSION: N2 positive non-small cell carcinoma.",
            3: "Code: 31653 (EBUS Staging).\nNodes Sampled: 7, 4R, 10R, 11R.\nPathology: Malignancy confirmed in mediastinum.\nTechnique: 22G needle, ROSE support.",
            4: "Procedure: EBUS\nPatient: Lisa Marie Thompson\nSteps:\n1. EBUS scope in.\n2. 4R and 7 were huge. Sampled them.\n3. ROSE said cancer.\n4. Also sampled 10R and 11R.\n5. No complications.\nDx: N2 Lung Cancer.",
            5: "Lisa Thompson here for staging right hilar mass. EBUS findings station 7 was massive like 4cm also 4R was big. Stuck them both ROSE said cancer. also checked the hilar nodes. So she has N2 disease. Needs chemo rads probably. No bleeding.",
            6: "Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration (EBUS-TBNA). Indication: 42-year-old female, right hilar mass 4.5cm. Mediastinal ultrasound survey: Station 4R (SUSPICIOUS), Station 7 (SUSPICIOUS). Sampling: Station 7 TBNA x4 (ROSE Positive). Station 4R TBNA x3 (ROSE Positive). Station 10R/11R sampled. Impression: N2 disease confirmed. Malignant cells in 7 and 4R.",
            7: "[Indication]\nRight hilar mass, mediastinal LAD.\n[Anesthesia]\nDeep Sedation/GA.\n[Description]\nEBUS-TBNA performed. Stations 7 and 4R sampled and positive for malignancy. N2 disease confirmed.\n[Plan]\nOncology referral. Final path pending.",
            8: "We performed an ultrasound bronchoscopy to stage Ms. Thompson's cancer. We found large lymph nodes in the center of the chest (stations 7 and 4R) that looked suspicious. We took samples with a needle, and the pathologist in the room confirmed they contain cancer cells. This means the cancer has spread to the mediastinal lymph nodes (N2 disease).",
            9: "Procedure: Ultrasonic mediastinal nodal aspiration.\nFindings: Lymphadenopathy in stations 7 and 4R.\nAction: Transbronchial needle aspiration was executed. Cytology confirmed metastatic spread.\nResult: N2 disease established."
        },
        9: { # Patricia Williams (Pleuroscopy, Chest Tube)
            1: "Indication: Recurrent effusion, trapped lung.\nProc: Medical Pleuroscopy.\nFindings: Diffuse nodules (visceral/parietal). Trapped lung.\nAction: Biopsies x10. 24Fr Chest Tube placed.\nAssessment: Carcinomatosis/Mesothelioma.\nPlan: Admit, awaiting path.",
            2: "PROCEDURE: Medical Thoracoscopy (Pleuroscopy).\nINDICATION: Exudative effusion, rule out malignancy.\nNARRATIVE: The pleural space was entered via the 7th ICS. Inspection revealed extensive nodularity involving both visceral and parietal surfaces, consistent with carcinomatosis. Due to trapped lung physiology, chemical pleurodesis was contraindicated. Multiple biopsies were taken using optical forceps. A 24Fr chest tube was placed for drainage.\nIMPRESSION: Malignant pleural effusion with trapped lung.",
            3: "Code: 32550 (Insertion of Pleural Catheter/Tube) - wait, Pleuroscopy is 32601/32606? Note says 32550 in source? I will stick to source code 32550 or correct to 32606 if implied? *Source has 32550*. Sticking to chest tube code.\nProcedure: Pleuroscopy + Biopsy + Chest Tube.\nFindings: Carcinomatosis.",
            4: "Procedure: Pleuroscopy\nPatient: Patricia Williams\nSteps:\n1. Trocar in.\n2. Scope in. Saw nodules everywhere.\n3. Took 10 biopsies.\n4. Lung looked trapped so didn't talc.\n5. Put in chest tube 24Fr.\nResult: Looks like cancer/meso.",
            5: "Patricia Williams 64 female with the effusion. Did the pleuroscopy. looked bad nodules all over the pleura. Took a bunch of biopsies. Lung looks trapped so we couldnt do the talc. Just put a chest tube in to drain. sending fluid and tissue. Probably mesothelioma or metastatic adeno.",
            6: "Medical pleuroscopy for diagnosis and possible therapeutic intervention. 64-year-old female with recurrent right pleural effusion. Right lateral chest, 7th intercostal space. Pleural fluid evacuated: 450 mL. Visceral Pleura: Multiple nodules. Parietal Pleura: Nodular involvement. Lung: Trapped lung physiology. Biopsies: Multiple pleural biopsies obtained. Therapeutic Intervention: Complete fluid drainage. 24 French chest tube placed. Immediate Assessment: Extensive pleural carcinomatosis.",
            7: "[Indication]\nRecurrent exudative effusion, suspected malignancy.\n[Anesthesia]\nMAC/Local.\n[Description]\nPleuroscopy performed. Extensive nodular disease seen. Biopsies x10. Trapped lung noted (no pleurodesis). Chest tube placed.\n[Plan]\nAdmit. Pain control. Oncology consult.",
            8: "Ms. Williams underwent a procedure to look inside her chest cavity. We found widespread nodules on the lining of the lung and chest wall, which is very suspicious for cancer. Because the lung is 'trapped' by disease and won't fully expand, we couldn't seal the space with talc. Instead, we took biopsies and placed a chest tube to keep the fluid drained while we wait for the pathology results.",
            9: "Procedure: Thoracoscopic exploration and biopsy.\nFindings: Diffuse pleural nodularity and trapped lung.\nAction: The pleural cavity was visualized. Tissue samples were harvested via optical forceps. A drainage catheter was sited.\nResult: Assessment suggests carcinomatosis."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages
    # Indices 0-5 from previous request, 6-9 new for this file
    # Note: Source has 10 items (0-9).
    return [
        {"idx": 0, "orig_name": "Linda Chen", "orig_age": 72, "names": ["Margaret Wong", "Susan Lee", "Dorothy Chang", "Betty Liu", "Helen Wu", "Nancy Chen", "Barbara Yang", "Alice Zhao", "Shirley Huang"]},
        {"idx": 1, "orig_name": "Anjali Patel", "orig_age": 45, "names": ["Priya Sharma", "Anita Singh", "Meera Gupta", "Sunita Kumar", "Rina Shah", "Kavita Desai", "Nina Reddy", "Tara Malik", "Leela Patel"]},
        {"idx": 2, "orig_name": "Michelle Chen", "orig_age": 71, "names": ["Catherine Wu", "Elizabeth Liu", "Patricia Wang", "Jennifer Zhang", "Linda Ho", "Barbara Lin", "Susan Tran", "Margaret Kim", "Dorothy Park"]},
        {"idx": 3, "orig_name": "Carlos Rodriguez", "orig_age": 59, "names": ["Juan Martinez", "Jose Garcia", "Luis Hernandez", "Miguel Lopez", "Antonio Gonzalez", "Francisco Perez", "Jorge Sanchez", "Ricardo Ramirez", "Manuel Torres"]},
        {"idx": 4, "orig_name": "Jennifer Wu", "orig_age": 52, "names": ["Sarah Chang", "Michelle Lin", "Jessica Lee", "Amanda Wang", "Melissa Chen", "Stephanie Kim", "Nicole Liu", "Heather Wu", "Amy Yang"]},
        {"idx": 5, "orig_name": "Robert Thompson", "orig_age": 61, "names": ["James Wilson", "John Anderson", "Michael Taylor", "William Thomas", "David Moore", "Richard Jackson", "Charles White", "Joseph Harris", "Thomas Martin"]},
        {"idx": 6, "orig_name": "Emily Richardson", "orig_age": 65, "names": ["Mary Smith", "Patricia Johnson", "Linda Williams", "Barbara Brown", "Elizabeth Jones", "Jennifer Miller", "Maria Davis", "Susan Garcia", "Margaret Rodriguez"]},
        {"idx": 7, "orig_name": "Maria Gonzalez", "orig_age": 57, "names": ["Ana Hernandez", "Rosa Martinez", "Carmen Lopez", "Elena Perez", "Teresa Sanchez", "Isabel Ramirez", "Gloria Torres", "Silvia Flores", "Martha Rivera"]},
        {"idx": 8, "orig_name": "Lisa Marie Thompson", "orig_age": 42, "names": ["Jennifer Ann Smith", "Sarah Jane Doe", "Jessica Lynn White", "Ashley Marie Brown", "Amanda Sue Jones", "Melissa Kay Miller", "Stephanie Ann Davis", "Nicole Marie Wilson", "Heather Lee Taylor"]},
        {"idx": 9, "orig_name": "Patricia Williams", "orig_age": 64, "names": ["Linda Johnson", "Mary Brown", "Barbara Jones", "Susan Miller", "Margaret Davis", "Dorothy Garcia", "Lisa Rodriguez", "Nancy Wilson", "Karen Martinez"]}
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
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen with full dict)
                print(f"Warning: Missing variation for Note {idx} Style {style_num}")
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
    output_filename = output_dir / "synthetic_interventional_notes_part_004.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()