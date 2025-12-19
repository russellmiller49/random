import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_005.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Variations for the 5 notes in bronch_notes_part_005.json
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Small Cell Recurrence (11Rs)
            1: "Indication: Hilar adenopathy (Hx Small Cell LC).\nProcedure: EBUS-TBNA.\nActions:\n- LMA placed. Airway normal.\n- EBUS scope introduced.\n- Station 11Rs identified (10.4mm).\n- TBNA x7 passes (22G needle).\n- ROSE: Suspicious for small cell.\n- Bleeding suctioned. Scope out.",
            2: "HISTORY: The patient, with a known history of small cell lung carcinoma, presented with radiographic evidence of hilar adenopathy.\nPROCEDURE: General anesthesia was induced. A Q190 video bronchoscope was utilized to survey the airway; vocal cords, trachea, and bronchial mucosa were unremarkable. Subsequently, a UC180F convex probe endobronchial ultrasound bronchoscope was deployed. The radiographically prominent station 11Rs lymph node was sonographically visualized measuring 10.4 mm in short axis. Transbronchial needle aspiration was executed using a 22-gauge Olympus needle. Seven passes were completed. Rapid On-Site Evaluation (ROSE) suggested small cell carcinoma. Hemostasis was confirmed prior to termination.",
            3: "Procedure: Bronchoscopy with EBUS-guided sampling (CPT 31652).\nDevice: Olympus UC180F Convex Probe EBUS.\nTarget: Station 11Rs (Single station sampled).\nTechnique: Ultrasound localization confirmed node size (10.4mm). A 22-gauge needle was used for 7 passes. ROSE confirmation obtained (suspicious for malignancy). Diagnostic inspection of the airway was performed integrally with the procedure. No other stations sampled.",
            4: "Procedure Note\nAttending: [Name]\nResident: [Name]\nIndication: Hilar adenopathy, r/o recurrence.\nSteps:\n1. Time out.\n2. General anesthesia/LMA.\n3. Inspection: Airway patent, no lesions.\n4. EBUS: Station 11Rs identified (10.4mm).\n5. Sampling: 11Rs sampled x7 passes with 22G needle.\n6. ROSE: Suspicious for small cell.\n7. Tolerated well. Minimal bleeding.",
            5: "indication hilar adenopathy hx small cell lung ca used propofol and fentanyl airway exam with the q190 was normal no lesions seen then switched to the ebus scope found the 11Rs node it was like 10mm took 7 passes with the 22 gauge needle rose guy said looks like small cell cleaned up some blood no active bleeding when we finished patient stable.",
            6: "Indications: hilar adenopathy in setting of previous small cell lung cancer Medications: Propofol, fentanyl infusion via anesthesia assistance Procedure, risks, benefits, and alternatives were explained to the patient. All questions were answered and informed consent was documented as per institutional protocol. A history and physical were performed and updated in the pre-procedure assessment record. Laboratory studies and radiographs were reviewed. A time-out was performed prior to the intervention. Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The laryngeal mask airway is in good position. The vocal cords appeared normal. The subglottic space was normal. The trachea is of normal caliber. The carina is sharp. The tracheobronchial tree was examined to at least the first subsegmental level. Bronchial mucosa and anatomy were normal; there are no endobronchial lesions, and no secretions. The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. Ultrasound was utilized to identify and measure the radiographically enlarged station 11Rs lymph node which ,measured as 10.4 mm in the short axis dimension. Sampling by transbronchial needle aspiration was performed within the 11Rs lymph node using an Olympus EBUS TBNA 22 gauge needle. A total of 7 needle passes were performed. All samples were sent for routine cytology. ROSE was suspicious for small cell. Following completion of EBUS bronchoscopy the video bronchoscope was re-inserted and blood was suctioned from the airway. There was no evidence of active bleeding and the bronchoscope was removed and procedure completed. Complications: No immediate complications Estimated Blood Loss: Less than 5 cc. Post Procedure Diagnosis: Technically successful EBUS bronchoscopy. Will await final pathology results.",
            7: "[Indication]\nHilar adenopathy, history of small cell lung cancer.\n[Anesthesia]\nGeneral (Propofol/Fentanyl) via LMA.\n[Description]\nAirway inspection revealed normal anatomy. EBUS identified enlarged station 11Rs node (10.4mm). 7 transbronchial needle aspiration passes performed with 22G needle. ROSE indicated suspicious for small cell.\n[Plan]\nPathology pending. Follow up in clinic.",
            8: "The patient presented with hilar adenopathy and a history of small cell lung cancer. After induction of anesthesia, we inspected the airway with a video bronchoscope and found normal anatomy with no endobronchial lesions. We then switched to the convex probe EBUS scope. We identified the enlarged 11Rs lymph node, which measured 10.4 mm. Using a 22-gauge needle, we performed seven passes. The on-site pathologist noted cells suspicious for small cell carcinoma. We suctioned a small amount of blood and confirmed hemostasis before removing the scope.",
            9: "Indications: hilar adenopathy in setting of previous small cell lung cancer. Medications: Propofol, fentanyl. The Q190 video bronchoscope was inserted through the LMA. The airway was surveyed and appeared normal. The UC180F EBUS scope was then inserted. We visualized the 11Rs node (10.4mm). We sampled the 11Rs node using a 22 gauge needle. 7 passes were completed. ROSE was suspicious for small cell. After EBUS, we aspirated blood from the airway. There was no active bleeding."
        },
        1: { # 10L Cyst (10L)
            1: "Indication: Hilar adenopathy.\nDx: Hilar cyst (10L).\nProcedure: EBUS-TBNA.\n- LMA adjusted.\n- Airway normal. Green mucus suctioned.\n- 10L: 10mm hypoechoic structure with bands.\n- Aspiration: 22G (2cc fluid) then 19G (3cc fluid). Serous.\n- Cyst shrank.\n- 5 total passes. ROSE: Lymphocytes.\n- No complications.",
            2: "INDICATION: Evaluation of hilar adenopathy.\nPROCEDURE: General anesthesia was utilized. Initial airway inspection via LMA necessitated repositioning of the airway device. Examination revealed normal bronchial anatomy but significant tenacious greenish secretions which were cleared. EBUS examination of the left upper lobe revealed a 10mm hypoechoic, septated structure at station 10L. Transbronchial needle aspiration was initiated with a 22G needle yielding serous fluid, consistent with a cyst. A 19G needle was subsequently employed to evacuate 3cc of fluid, resulting in sonographic resolution of the cyst. Three additional passes were performed for cytology. ROSE demonstrated lymphocytes.\nCONCLUSION: Aspiration of 10L hilar cyst.",
            3: "Procedure: Bronchoscopy with EBUS Sampling (31652).\nTarget: Station 10L (Single station).\nTechnique: EBUS visualization of 10mm hypoechoic structure. Aspiration performed using 22G and 19G needles. 5cc total serous fluid removed. 3 additional passes for tissue. ROSE confirmed lymphocytes. \nAdditional Work: Suctioning of mucus plugs (incidental).\nJustification: Evaluation of hilar abnormality found to be cystic.",
            4: "Procedure Note\nPatient: [Name]\nIndication: Hilar adenopathy.\nSteps:\n1. LMA placed (needed upsizing).\n2. Bronchoscopy: Normal anatomy, thick green mucus suctioned.\n3. EBUS: 10mm structure at 10L. Looked like cyst.\n4. Aspiration: 22G needle got 2cc fluid. 19G needle got 3cc fluid.\n5. Structure collapsed.\n6. 3 more passes for cells. ROSE: Lymphocytes.\n7. Hemostasis achieved.",
            5: "patient has hilar adenopathy so we did ebus under GA lma needed fixing at first vocal cords fine trachea normal lots of green mucus everywhere we sucked it out then used the ebus scope found a 10mm thing at 10L looked like a cyst stuck it with a 22g needle got liquid stuck it with a 19g got more liquid it shrank down did a few more passes rose saw lymphocytes sent fluid for culture and cytology gave augmentin just in case.",
            6: "Indications: Hilar adenopathy Procedure: EBUS bronchoscopy Medications: General Anesthesia Procedure, risks, benefits, and alternatives were explained to the patient. All questions were answered and informed consent was documented as per institutional protocol. A history and physical were performed and updated in the pre-procedure assessment record. Laboratory studies and radiographs were reviewed. A time-out was performed prior to the intervention. Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The laryngeal mask airway initially was not well positioned but after replacement with larger LMA seated in good position. The vocal cords appeared normal. The subglottic space was normal. The trachea is of normal caliber. The carina is sharp. The tracheobronchial tree was examined to at least the first subsegmental level. Bronchial mucosa and anatomy were normal; there are no endobronchial lesions. There were thick greenish mucus plugs throughout the lungs which were easily suctioned. The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The scope was advanced into the proximal left upper lobe and a 10mm hypoechoic structure was seen in the area of the 10L lymph node. Within the hypoechoic structure were hyperechoic bands similar to those seen in loculated pleural effusions. Sampling by transbronchial needle aspiration was performed with the Olympus 22G EBUS-TBNA needle and serous appearing liquid was noted within the suction line and attached syringe (approximately 2cc) consistent with cyst. Subsequent pass with an Olympus 19G EBUS-TBNA needle yielded similar results with another 3cc fluid return. Ultrasound showed shrinkage of the cyst. Three additional needle passes were then performed. Rapid onsite pathological evaluation showed lymphocytes within the samples. Samples and fluid were sent for both flow and routine cytology. Following completion of EBUS bronchoscopy, the Q190 video bronchoscope was then re-inserted and after suctioning blood and secretions there was no evidence of active bleeding and the bronchoscope was subsequently removed. Complications: No immediate complications Post-operative diagnosis: Hilar cyst (bronchogenic vs cardiac) Estimated Blood Loss: 5cc Recommendations: - Transferred patient to post-procedural monitoring unit and discharge when standard criteria are met. - 5 day course of Augmentin to reduce likelihood of infection of residual cystic space. - Will await final pathology results",
            7: "[Indication]\nHilar adenopathy (found to be cyst).\n[Anesthesia]\nGeneral, LMA.\n[Description]\nMucus plugs suctioned. EBUS at 10L showed 10mm cyst with septations. Aspirated 5cc serous fluid using 22G and 19G needles. Cyst size decreased. Additional passes for cytology showed lymphocytes.\n[Plan]\nAugmentin prophylaxis. Discharge home.",
            8: "The patient underwent EBUS for hilar adenopathy. After resolving an initial LMA fit issue, we inspected the airway and suctioned significant green mucus plugs. Using the EBUS scope, we located a 10mm hypoechoic structure at station 10L that contained internal bands. We aspirated the lesion using a 22G needle, obtaining 2cc of serous fluid, and then a 19G needle for another 3cc. This confirmed a cystic nature as the structure collapsed. Additional sampling for cytology revealed benign lymphocytes. We prescribed Augmentin to prevent infection of the cyst remnant.",
            9: "Indications: Hilar adenopathy. Medications: General Anesthesia. The Q190 video bronchoscope was inserted via LMA. Mucus plugs were extracted. The UC180F EBUS scope was inserted. A 10mm structure was visualized at 10L. We aspirated the structure with a 22G needle (2cc fluid) and a 19G needle (3cc fluid). The cyst diminished in size. Three more passes were collected. ROSE showed lymphocytes. Augmentin was prescribed."
        },
        2: { # Breast CA Recurrence (11Ri)
            1: "Indication: Hilar adenopathy (Breast CA).\nProcedure: EBUS-TBNA.\n- LMA used.\n- Airway exam: Normal.\n- EBUS: Station 11Ri identified.\n- Sampling: 22G needle.\n- ROSE: Malignant.\n- EBL: 10cc. No complications.",
            2: "HISTORY: Patient with a history of breast cancer presenting with hilar adenopathy suspicious for metastasis.\nPROCEDURE: General anesthesia was administered via LMA. Complete airway inspection demonstrated normal vocal cords, trachea, and carina with no endobronchial anomalies. EBUS interrogation identified a suspicious lymph node at station 11Ri. Transbronchial needle aspiration was performed utilizing a 22-gauge needle. Rapid On-Site Evaluation (ROSE) confirmed malignancy compatible with metastasis. The procedure was concluded without complication.",
            3: "Service: Bronchoscopy with EBUS (31652).\nTarget: Station 11Ri (Single station).\nTool: Olympus 22G EBUS-TBNA Needle.\nRationale: Radiographically suspicious node in setting of breast cancer.\nFindings: ROSE positive for malignancy.\nDetails: Airway inspection normal. No other stations sampled.",
            4: "Procedure Note\nIndication: Hilar adenopathy, r/o breast mets.\nStaff: [Name]\nSteps:\n1. GA with LMA.\n2. Normal airway inspection.\n3. EBUS to 11Ri.\n4. TBNA with 22G needle.\n5. ROSE: Malignant.\n6. Suctioned airway, procedure done.\nPlan: Oncology follow-up.",
            5: "doing an ebus on a patient with breast cancer history showing hilar nodes used general anesthesia lma placement was fine looked around with the regular scope everything normal no secretions switched to the ebus scope found the 11Ri node looked suspicious on ultrasound poked it with the 22 gauge needle rose path said it was malignant so we stopped suctioned a little blood and finished.",
            6: "Indications: Hilar adenopathy, presumed metastatic breast CA Procedure Performed: EBUS bronchoscopy single station. Pre-operative diagnosis: hilar adenopathy Post-operative diagnosis: malignant hilar adenopathy Medications: General Anesthesia, Procedure, risks, benefits, and alternatives were explained to the patient. All questions were answered and informed consent was documented as per institutional protocol. A history and physical were performed and updated in the pre-procedure assessment record. Laboratory studies and radiographs were reviewed. A time-out was performed prior to the intervention. Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The laryngeal mask airway is in good position. The vocal cords appeared normal. The subglottic space was normal. The trachea is of normal caliber. The carina is sharp. The tracheobronchial tree was examined to at least the first subsegmental level. Bronchial mucosa and anatomy were normal; there are no endobronchial lesions, and no secretions. The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. Ultrasound was utilized to identify and measure the radiographically suspicious station 11Ri lymph node. Sampling by transbronchial needle aspiration was performed beginning with the Olympus EBUS-TBNA 22 gauge needle. Rapid onsite evaluation read as malignancy. All samples were sent for routine cytology. Following completion of EBUS bronchoscopy the video bronchoscope was re-inserted and blood was suctioned from the airway. The bronchoscope was removed and procedure completed. Complications: No immediate complications Estimated Blood Loss: 10 cc. Post Procedure Diagnosis: Technically successful flexible bronchoscopy with endobronchial ultrasound-guided biopsies. The patient has remained stable and has been transferred in good condition to the post-surgical monitoring unit. Will await final pathology results",
            7: "[Indication]\nHilar adenopathy, presumed breast cancer metastasis.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nDiagnostic bronchoscopy negative. EBUS identified suspicious node at 11Ri. TBNA performed with 22G needle. ROSE confirmed malignancy.\n[Plan]\nFinal pathology pending.",
            8: "We performed an EBUS bronchoscopy for a patient with presumed metastatic breast cancer presenting with hilar adenopathy. Under general anesthesia, the initial airway exam was normal. We then utilized the EBUS scope to localize the suspicious 11Ri lymph node. Using a 22-gauge needle, we obtained samples which were immediately read as malignant by the on-site pathologist. We ensured hemostasis and ended the procedure.",
            9: "Indications: Hilar adenopathy. Medications: General Anesthesia. The Q190 video bronchoscope was introduced. The airway was examined. The UC180F EBUS scope was inserted. We visualized the station 11Ri lymph node. We sampled the node with a 22 gauge needle. ROSE indicated malignancy. Samples were submitted for cytology. The bronchoscope was withdrawn."
        },
        3: { # Hemorrhagic Cyst 11L
            1: "Indication: Hilar cyst aspiration.\nDx: Hemorrhagic hilar cyst (11L).\nProcedure: EBUS-TBNA.\n- Airway: Extrinsic compression LUL.\n- EBUS: 45mm heterogeneous cyst at 11L.\n- Sampling: 19G needle. Thick bloody material.\n- ROSE: Heme + foamy macrophages.\n- Plan: Antibiotics, likely surgery.",
            2: "HISTORY: Patient with a large hilar cyst requiring aspiration.\nPROCEDURE: General anesthesia with LMA. Diagnostic bronchoscopy revealed partial extrinsic compression of the LUL bronchus. EBUS identified a 45mm septated, heterogeneous cyst in the proximal LUL (Station 11L). Aspiration was attempted with a 19G Visioshot needle. The aspirate was thick and coagulated, consistent with old blood. ROSE analysis demonstrated heme and foamy macrophages. \nCONCLUSION: Hemorrhagic hilar cyst. Samples sent for culture/cytology.",
            3: "Procedure: Bronchoscopy with EBUS (31652).\nStructure Sampled: Left Hilar Cyst (11L).\nDescription: 45mm heterogeneous lesion. 19G needle used due to viscosity. Thick bloody return.\nFindings: Extrinsic compression of LUL bronchus. ROSE showed macrophages/heme.\nCoding Note: Single structure sampled. No other nodes.",
            4: "Procedure Note\nIndication: Hilar cyst.\nSteps:\n1. GA/LMA.\n2. Bronchoscopy showed LUL compression.\n3. EBUS: 45mm cyst at 11L location.\n4. TBNA with 19G needle.\n5. Aspirated thick bloody material.\n6. ROSE: Heme, macrophages.\nPlan: Augmentin, refer to Thoracic Surgery.",
            5: "hilar cyst aspiration under general anesthesia lma used airway looked ok except for some compression in the left upper lobe ebus showed a huge 45mm cyst near the left pulmonary artery used a 19g needle to try and drain it got thick old blood out rose said it was just heme and macrophages sent for culture gave augmentin probably needs surgery.",
            6: "Indications: Hilar cyst aspiration Procedure: EBUS bronchoscopy Medications: General Anesthesia Procedure, risks, benefits, and alternatives were explained to the patient. All questions were answered and informed consent was documented as per institutional protocol. A history and physical were performed and updated in the pre-procedure assessment record. Laboratory studies and radiographs were reviewed. A time-out was performed prior to the intervention. Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The laryngeal mask airway initially was not well positioned but after replacement with larger LMA seated in good position. The vocal cords appeared normal. The subglottic space was normal. The trachea is of normal caliber. The carina is sharp. The tracheobronchial tree was examined to at least the first subsegmental level. Bronchial mucosa and anatomy were normal with the exception of partial extrinsic compression of the left upper lobe bronchus distal to the lingual and most obvious in the apical segment; there are no endobronchial lesions. The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The scope was advanced into the proximal left upper lobe and a 45mm heterogeneous cyst with multiple septations was seen just distal to the left PA. Sampling by transbronchial needle aspiration was performed with the Olympus 19G Visioshot EBUS-TBNA needle. Material was thick which could not be grossly aspirated through the needle with attached suction. Samples showed thick coagulated bloody material on multiple needle passes consistent with old blood. Rapid onsite pathological evaluation showed heme and multiple foamy macrophages. Samples and fluid were sent for both culture and routine cytology. Following completion of EBUS bronchoscopy, the Q190 video bronchoscope was then re-inserted and after suctioning blood and secretions there was no evidence of active bleeding and the bronchoscope was subsequently removed. Complications: No immediate complications Post-operative diagnosis: Hemorrhagic Hilar cyst Estimated Blood Loss: 10cc Recommendations: - Transferred patient to post-procedural monitoring - 10 day course of Augmentin to reduced likelihood of infection of capsulated cystic space. - Will await final pathology results - Repeat CT in 3-4 weeks or earlier if fevers, persistent/worsening chest pain, hemoptysis or other symptoms concerning for infection or cyst rupture. - Will likely require unroofing and resection with thoracic surgery",
            7: "[Indication]\nHilar cyst aspiration.\n[Anesthesia]\nGeneral, LMA.\n[Description]\nLUL bronchus compressed. 45mm heterogeneous cyst found at 11L. 19G needle used. Thick, bloody material obtained. ROSE: Heme, foamy macrophages.\n[Plan]\nAugmentin 10 days. Thoracic surgery consult.",
            8: "The patient presented for aspiration of a hilar cyst. We performed the procedure under general anesthesia. Inspection revealed compression of the LUL bronchus. EBUS identified a 45mm cyst with septations in the proximal LUL. We used a 19G needle to attempt aspiration, but the material was thick and bloody, suggestive of old hemorrhage. ROSE confirmed the presence of heme and macrophages. The patient was started on Augmentin and will likely require surgical resection.",
            9: "Indications: Hilar cyst aspiration. Medications: General Anesthesia. The Q190 video bronchoscope was inserted. We noted extrinsic compression of the LUL bronchus. The UC180F EBUS scope was utilized. A 45mm cyst was visualized at 11L. We sampled the cyst with a 19G needle. Thick bloody material was extracted. ROSE indicated heme and macrophages. Augmentin was prescribed."
        },
        4: { # LLL Nodule Navigational
            1: "Indication: LLL nodule.\nProcedure: Navigational Bronchoscopy (SuperDimension), Radial EBUS, Biopsy.\n- 7.5 ETT. Difficult intubation.\n- Anatomy: Right accessory airway. Left normal.\n- Navigation to LLL anterior-medial segment.\n- Radial EBUS: Concentric view.\n- Sampling: Needle, Forceps, Brush.\n- ROSE: Non-diagnostic.\n- ICU admit (failed extubation).",
            2: "HISTORY: Patient presenting with a Left Lower Lobe nodule for evaluation.\nPROCEDURE: General anesthesia via 7.5 ETT. The airway was friable with blood noted from a traumatic intubation. Anatomic variant noted on the right (accessory airway). SuperDimension navigational bronchoscopy was utilized to guide a catheter to the anterior-medial segment of the LLL. Radial EBUS confirmed lesion location with a concentric signal. Transbronchial biopsies were performed using needle, forceps, and brush. ROSE was non-diagnostic. \nCOMPLICATIONS: Patient did not meet extubation criteria (no air leak); transferred to ICU intubated.",
            3: "Code Selection: 31627 (Navigation), 31654 (Radial EBUS), 31628 (Lung Biopsy).\nTarget: Left Lower Lobe Nodule.\nTechnique: Electromagnetic navigation used to reach target. Radial EBUS probe used to confirm concentric view. Samples taken via needle, forceps, and brush. \nNote: Primary code 31628 chosen as forceps biopsy is definitive. 31652/31653 not applicable as no lymph nodes sampled.",
            4: "Procedure Note\nIndication: LLL Nodule.\nSteps:\n1. GA/ETT 7.5.\n2. Bloody airway from intubation.\n3. Navigated to LLL anterior-medial segment.\n4. Radial EBUS confirmed concentric view.\n5. Biopsies: Needle, Forceps, Brush.\n6. ROSE negative.\nPlan: ICU admission, delayed extubation.",
            5: "patient has a nodule in the left lower lobe did a navigational bronchoscopy under general anesthesia tube was 7.5 lots of blood in the airway from intubation found the spot with superdimension used radial ebus got a concentric view took biopsies with needle forceps and brush rose said non diagnostic but we took plenty of tissue patient didn't have a cuff leak so we kept him intubated and sent to icu.",
            6: "Indications: Left lower lobe nodule Medications: General Anesthesia, Procedure, risks, benefits, and alternatives were explained to the patient. All questions were answered and informed consent was documented as per institutional protocol. A history and physical were performed and updated in the pre-procedure assessment record. Laboratory studies and radiographs were reviewed. A time-out was performed prior to the intervention. Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree, the Q190 video bronchoscope was introduced through the 7.5 ETT. The airways were friable and significant blood was present from difficult intubation. The trachea was of normal caliber. The carina is sharp. On the right the patient had an anatomic variant with an accessory airway just distal to the superior segment of the right lower lobe. The left sided airway anatomy was normal. No evidence of endobronchial disease was seen to at least the first sub-segments. Following inspection the super-dimension navigational catheter was inserted through the therapeutic bronchoscope and advanced into the airway. Using navigational map we were able to advance the 180 degree edge catheter into the anterior-medial segment on the left lower lobe and navigated to within 1cm of the lesion. The navigational probe was then removed and peripheral radial probe was inserted into the catheter to confirm location. Ultrasound visualization yielded a concentric view affirming the location. Needle biopsies were performed with fluoroscopic guidance. ROSE was non-diagnostic. The catheter was repositioned to sample other areas of the lesion and radial probe continued to show a concentric view of the tumor. ROSE again was read as non-diagnostic. Tissue biopsies were then performed using forceps under fluoroscopic visualization along with brush and triple needle brush biopsies. After samples were obtained the bronchoscope was removed and the diagnostic bronchoscope was re-inserted into the airway. Subsequent inspection did not show evidence of active bleeding and the bronchoscope was removed from the airway. Following completion of the procedure the patient was noted to lack audible airleak when the ETT balloon was deflated. Given the difficult intubation, anesthesia decided to leave patient intubated and transfer to the ICU to monitor and extubate when deemed appropriate. Complications: None Estimated Blood Loss: Less than 10 cc. Post Procedure Diagnosis: Flexible bronchoscopy with successful biopsy of left lower lobe pulmonary nodule. Will transfer to the ICU and attempt extubation later today. Await final pathology",
            7: "[Indication]\nLeft lower lobe nodule.\n[Anesthesia]\nGeneral, 7.5 ETT.\n[Description]\nBloody airway (difficult intubation). SuperDimension navigation to LLL anterior-medial segment. Radial EBUS: Concentric view. Sampled with needle, forceps, brush. ROSE non-diagnostic.\n[Plan]\nTransfer to ICU intubated (no cuff leak). Extubate when appropriate.",
            8: "We performed a navigational bronchoscopy for a left lower lobe nodule. The patient was intubated with difficulty, resulting in a friable, bloody airway. We navigated to the LLL anterior-medial segment using the SuperDimension system. Confirmation was achieved with radial EBUS showing a concentric view. We sampled the lesion using needle, forceps, and brush. Although ROSE was non-diagnostic, ample tissue was collected. Due to the lack of an air leak upon cuff deflation, the patient remained intubated and was transferred to the ICU.",
            9: "Indications: Left lower lobe nodule. Medications: General Anesthesia. The Q190 video bronchoscope was introduced. The airway contained blood. A SuperDimension catheter was inserted and guided to the LLL anterior-medial segment. Radial EBUS confirmed the location (concentric). We sampled the lesion with needle, forceps, and brush. ROSE was non-diagnostic. The patient was transferred to the ICU intubated."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the style logic
    # Note Indices: 0, 1, 2, 3, 4
    return [
        {"idx": 0, "orig_name": "Patient Zero", "orig_age": 65, "names": ["John Smith", "Alice Johnson", "Robert Williams", "Mary Brown", "Michael Jones", "Linda Garcia", "David Miller", "Barbara Davis", "James Rodriguez"]}, # 11Rs Small Cell
        {"idx": 1, "orig_name": "Patient One", "orig_age": 55, "names": ["Patricia Martinez", "Jennifer Hernandez", "Charles Lopez", "Elizabeth Gonzalez", "Thomas Wilson", "Susan Anderson", "Joseph Thomas", "Jessica Taylor", "Christopher Moore"]}, # 10L Cyst
        {"idx": 2, "orig_name": "Patient Two", "orig_age": 60, "names": ["Daniel Jackson", "Sarah Martin", "Paul Lee", "Karen Perez", "Mark Thompson", "Nancy White", "Donald Harris", "Lisa Sanchez", "Kenneth Clark"]}, # 11Ri Breast
        {"idx": 3, "orig_name": "Patient Three", "orig_age": 70, "names": ["Steven Ramirez", "Betty Lewis", "Edward Robinson", "Sandra Walker", "Brian Young", "Ashley Allen", "Ronald King", "Kimberly Wright", "Anthony Scott"]}, # 11L Heme Cyst
        {"idx": 4, "orig_name": "Patient Four", "orig_age": 50, "names": ["Kevin Torres", "Donna Nguyen", "Jason Hill", "Carol Flores", "Matthew Green", "Michelle Adams", "Gary Nelson", "Emily Baker", "Timothy Hall"]}, # LLL Nodule
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
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                note_entry["note_text"] = f"Error: Variation text missing for index {idx} style {style_num}"

            # Update registry_entry fields if they exist
            # Note: The input file structure has 'registry_entry' at the top level
            if "registry_entry" in note_entry:
                re = note_entry["registry_entry"]
                
                # Update MRN
                orig_mrn = re.get("patient_mrn", "UNKNOWN")
                re["patient_mrn"] = f"{orig_mrn}_syn_{style_num}"
                
                # Update Date
                re["procedure_date"] = rand_date_str
                
                # Update Patient Demographics if nested or flat
                # Checking structure from provided file content
                # Some entries might not have explicit age/gender fields in the top of registry_entry
                # or they might be inside 'patient_demographics'
                
                if "patient_demographics" in re and re["patient_demographics"] is not None:
                     re["patient_demographics"]["age_years"] = new_age
                else:
                    # If flat or missing, we can try to add/update if it makes sense, 
                    # but adhering to the 'valid extraction' rule, we mostly care about the text.
                    # However, we can inject the synthetic name into metadata or a new field if desired.
                    pass

            # Add synthetic metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_bronch_notes_part_005.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()