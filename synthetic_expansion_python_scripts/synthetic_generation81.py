import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_081.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the specified year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Grace Wilson (Medical Thoracoscopy - Undiagnosed Exudative Effusion)
            1: "Indication: L pleural effusion.\nProc: Med thoracoscopy w/ biopsy.\nAction: 1.1L cloudy fluid drained. Diffuse granular parietal thickening seen. 10 biopsies taken. No pleurodesis.\nDevice: 20Fr chest tube placed.\nComp: None.",
            2: "PROCEDURE PERFORMED: Diagnostic medical thoracoscopy with parietal pleural biopsy.\nINDICATION: Recurrent undiagnosed left-sided exudative pleural effusion.\nOPERATIVE FINDINGS: Upon entry into the pleural space via the 6th intercostal space utilizing a semi-rigid thoracoscope, approximately 1100 mL of turbid, straw-colored exudate was evacuated. Inspection revealed diffuse, granular thickening of the parietal and diaphragmatic pleura, interspersed with fibrin deposition. No discrete masses were visualized. Ten biopsy specimens were obtained from representative abnormal areas for histopathologic and microbiologic examination.\nPLAN: Chest tube thoracostomy maintained on water seal pending cessation of drainage.",
            3: "Procedure: 32609 (Thoracoscopy with biopsy of pleura).\nTechnique: Ultrasound guidance used for port placement. Single-port technique. Semi-rigid thoracoscope inserted.\nFluid Removal: 1.1 Liters drained.\nBiopsy: Forceps biopsies (x10) taken from parietal and diaphragmatic pleura to rule out malignancy/TB.\nPost-op: 20 Fr chest tube placed.",
            4: "Procedure Note\nPatient: Grace Wilson\nStaff: Dr. Ross\nPre-op Dx: L pleural effusion.\nSteps:\n1. Moderate sedation.\n2. US guided entry 6th ICS.\n3. Thoracoscope inserted.\n4. Drained 1.1L fluid.\n5. Biopsied parietal pleura (looks granular).\n6. Chest tube placed.\nPlan: Admit, check cxr.",
            5: "medical thoracoscopy note patient grace wilson here for the left effusion used moderate sedation and lidocaine. went in at the 6th rib space drained about a liter of cloudy fluid saw some granular stuff on the wall so took ten biopsies. no pleurodesis done just put a tube in at the end. no complications blood loss minimal admitting her for observation.",
            6: "The patient underwent a medical thoracoscopy for a recurrent left exudative pleural effusion. After moderate sedation and local anesthesia, a semi-rigid thoracoscope was inserted at the 6th intercostal space. We drained 1.1 L of cloudy, straw-colored fluid. The parietal pleura appeared diffusely granular with small nodules. Ten biopsies were taken from the parietal and diaphragmatic surfaces. No pleurodesis was performed. A 20 Fr chest tube was placed to water seal. There were no complications.",
            7: "[Indication]\nRecurrent left exudative pleural effusion, cytology negative.\n[Anesthesia]\nModerate sedation (Midazolam/Fentanyl).\n[Description]\n1.1 L fluid drained. Granular pleural thickening observed. 10 biopsies taken from parietal/diaphragmatic pleura. 20 Fr chest tube placed.\n[Plan]\nAdmit. Await pathology/microbiology.",
            8: "Under moderate sedation, a medical thoracoscopy was performed on Ms. Wilson to investigate her recurrent left pleural effusion. Upon entering the pleural space, we drained approximately 1.1 liters of cloudy, straw-colored fluid. Visual inspection of the pleura revealed diffuse granular thickening along the chest wall and diaphragm, along with fibrin strands. We used biopsy forceps to take ten samples from these abnormal areas. We decided against pleurodesis at this time. The procedure concluded with the placement of a 20 Fr chest tube.",
            9: "Procedure: Pleuroscopy with pleural sampling.\nIndication: Persistent left effusion.\nDetails: Ultrasound located fluid. Scope introduced. 1.1L evacuated. Granular thickening observed. Tissue sampled (10x) from parietal/diaphragmatic surfaces. No chemical sclerosis performed. Drain inserted.\nStatus: Stable."
        },
        1: { # Ryan Brooks (Medical Thoracoscopy - Suspected Mesothelioma)
            1: "Dx: R pleural thickening/effusion.\nProc: Med thoracoscopy.\nFindings: 900cc serous fluid. Diffuse nodules/plaques parietal/diaphragmatic.\nAction: 12 biopsies taken. No pleurodesis.\nPlan: 24Fr chest tube. Admit.",
            2: "OPERATIVE REPORT: Medical Thoracoscopy.\nINDICATIONS: 69-year-old male with asbestos exposure and right-sided pleural thickening suspicious for malignant pleural mesothelioma.\nDESCRIPTION: Under general anesthesia, the right hemithorax was accessed. Approximately 900 mL of serous fluid was aspirated. Thorough inspection demonstrated extensive nodular and plaque-like neoplastic-appearing thickening involving the parietal and diaphragmatic pleura. Twelve large-capacity biopsies were harvested for definitive histopathologic characterization. Pleurodesis was deferred pending final staging. A 24 Fr thoracostomy tube was secured.",
            3: "CPT: 32609 (Thoracoscopy, surgical; with biopsy of pleura).\nApproach: Right 5th intercostal space via trocar.\nFindings: Diffuse nodular thickening consistent with malignancy.\nIntervention: Evacuation of 900 mL fluid. Multiple biopsies (n=12) obtained using rigid forceps for BAP1/MTAP testing.\nClosure: 24 Fr chest tube inserted.",
            4: "Resident Note: Medical Thoracoscopy\nPatient: Ryan Brooks\nAttending: Dr. Stone\nIndication: R effusion, r/o mesothelioma.\nProcedure:\n- GA / ETT.\n- Port placed 5th ICS.\n- Drained 900ml fluid.\n- Saw nodules/plaques on pleura.\n- Took 12 biopsies.\n- Chest tube placed.\nComplications: Minor oozing, cauterized.",
            5: "thoracoscopy note for ryan brooks he has asbestos exposure and a right effusion suspicious for meso. did this under GA tube in. port in the 5th space drained 900 of fluid. looks like nodules everywhere especially diaphragm. took a bunch of biopsies like 12 of them. stopped a little bleeding with cautery. didn't do pleurodesis cause we need to know what it is first. chest tube is in.",
            6: "Medical thoracoscopy was performed under general anesthesia for a 69-year-old male with suspected mesothelioma. Access was established at the right 5th intercostal space. 900 mL of serous fluid was drained. The parietal and diaphragmatic pleura showed diffuse nodular thickening. Twelve biopsies were obtained using rigid forceps. Minor bleeding was controlled with cautery and epinephrine. A 24 Fr chest tube was placed. The patient was admitted to the thoracic surgery floor.",
            7: "[Indication]\nSuspected malignant pleural mesothelioma, R pleural thickening.\n[Anesthesia]\nGeneral Anesthesia, ETT.\n[Description]\n900 mL fluid drained. Diffuse nodular/plaque-like thickening observed. 12 biopsies taken from parietal/diaphragmatic pleura. No pleurodesis.\n[Plan]\nPathology/IHC. PET/CT pending results.",
            8: "The patient was brought to the operating room for a medical thoracoscopy to investigate suspected mesothelioma. After inducing general anesthesia, we accessed the right pleural space and drained 900 mL of fluid. The thoracoscopic view was significant for extensive nodular and plaque-like thickening covering the parietal and diaphragmatic pleura. We utilized rigid forceps to obtain twelve biopsies from these suspicious areas. Given the need for diagnostic clarity before staging, we opted not to perform pleurodesis. A chest tube was placed at the conclusion of the case.",
            9: "Procedure: Thoracoscopic exploration and sampling.\nTarget: Right hemithorax.\nFindings: 900mL serous fluid removed. Widespread nodularity/plaques noted. Tissue harvested (12 specimens) from chest wall and diaphragm. Hemostasis achieved. Drain positioned."
        },
        2: { # Isabella Martinez (Medical Thoracoscopy - Rheumatoid Pleuritis)
            1: "Indication: Recurrent R effusion, RA.\nProc: Med thoracoscopy.\nFluid: 900ml cloudy yellow.\nFindings: Inflamed parietal pleura, small nodules.\nAction: 8 biopsies. No pleurodesis.\nTube: 16Fr placed.",
            2: "PROCEDURE NOTE: Diagnostic Pleuroscopy.\nCLINICAL CONTEXT: 54-year-old female with seropositive rheumatoid arthritis presenting with recurrent exudative right pleural effusion.\nINTRAOPERATIVE FINDINGS: The pleural space was accessed, and 900 mL of turbid, yellow effusion was evacuated. The parietal pleural surface appeared diffusely erythematous with granular, whitish nodularity consistent with chronic inflammation. No gross malignancy was identified. Eight biopsy specimens were procured for histologic analysis. A 16 Fr chest tube was inserted for postoperative drainage.",
            3: "Service: 32609 Medical Thoracoscopy.\nSite: Right 6th intercostal space.\nProcedure: Drainage of 900mL exudative fluid. Visualization of inflamed pleura. Biopsy (x8) of parietal/diaphragmatic pleura using semi-rigid thoracoscope.\nDevice: 16 Fr chest tube placed.\nIndication: Rule out malignancy vs rheumatoid pleuritis.",
            4: "Procedure: Medical Thoracoscopy\nPatient: Isabella Martinez\nIndication: R effusion, RA.\nSteps:\n1. Sedation + local.\n2. Trocar in 6th ICS.\n3. Drained 900cc cloudy fluid.\n4. Biopsied inflamed pleura (8 samples).\n5. Chest tube placed.\nPlan: Rheum follow up.",
            5: "patient isabella martinez with ra has a right effusion we did a thoracoscopy today. moderate sedation used. went in at the 6th space drained 900 ml cloudy fluid. pleura looked red and bumpy white nodules. took 8 biopsies to check for cancer vs ra lung. put in a small chest tube 16 french. no complications she is on the rheum floor.",
            6: "We performed a medical thoracoscopy on a 54-year-old female with rheumatoid arthritis and a recurrent right pleural effusion. Using moderate sedation, we accessed the right pleural space and drained 900 mL of cloudy yellow fluid. The parietal pleura was diffusely inflamed with small nodules. We took eight biopsies to differentiate between rheumatoid pleuritis and other causes. No pleurodesis was performed. A 16 Fr chest tube was left in place.",
            7: "[Indication]\nRecurrent R exudative effusion, h/o Rheumatoid Arthritis.\n[Anesthesia]\nModerate Sedation.\n[Description]\n900 mL cloudy fluid drained. Diffuse inflammation/nodules seen. 8 biopsies taken. 16 Fr chest tube placed.\n[Plan]\nHistology/Microbiology. Adjust RA meds.",
            8: "Ms. Martinez underwent a medical thoracoscopy to evaluate her recurrent right pleural effusion in the setting of rheumatoid arthritis. Under moderate sedation, we entered the chest cavity and removed 900 mL of cloudy fluid. The pleural lining appeared inflamed with multiple small white nodules scattered throughout. We obtained eight biopsies from the parietal and diaphragmatic surfaces to confirm the diagnosis. A 16 Fr chest tube was placed to allow for continued drainage.",
            9: "Operation: Thoracoscopic inspection and tissue acquisition.\nIndication: Persistent right-sided fluid collection.\nObservations: 900mL turbid fluid evacuated. Erythematous pleura with nodules noted. Specimens collected (8x) from chest wall and diaphragm. Drainage catheter inserted."
        },
        3: { # Ahmed Ali (Medical Thoracoscopy - Suspected TB)
            1: "Indication: Suspected TB pleuritis.\nProc: Med thoracoscopy L side.\nFindings: 800ml straw fluid. Diffuse white nodules, adhesions.\nAction: Biopsies parietal/diaphragmatic. No pleurodesis.\nTube: 16Fr placed.",
            2: "PROCEDURE: Medical Thoracoscopy.\nINDICATION: Unilateral left lymphocytic exudative pleural effusion in a patient with epidemiologic risk factors for tuberculosis.\nFINDINGS: Upon thoracoscopic visualization, the parietal pleura demonstrated diffuse miliary-type nodularity and fibrinopurulent adhesions. Approximately 800 mL of straw-colored effusion was drained. Biopsies were obtained from the costal and diaphragmatic surfaces for histopathology and mycobacterial culture. A 16 Fr thoracostomy tube was placed.",
            3: "Code: 32609.\nDiagnosis: Suspected Tuberculous Pleuritis.\nProcedure: Left-sided medical thoracoscopy via 5th ICS. Drainage of 800 mL fluid. Biopsy of parietal pleura (nodules/adhesions observed) for AFB stain/culture/PCR.\nPost-procedure: 16 Fr chest tube to water seal.",
            4: "Procedure Note: Med Thoracoscopy\nPatient: Ahmed Ali\nIndication: R/O TB effusion.\nSteps:\n1. Mod sedation.\n2. Port @ 5th ICS.\n3. Drained 800cc fluid.\n4. Saw white nodules (TB?).\n5. Biopsied nodules.\n6. 16Fr chest tube.\nPlan: Isolation, empiric TB meds if path +.",
            5: "did a thoracoscopy on mr ali for his left effusion thinking it's tb. sedation was fine. put the scope in the 5th space drained 800 ml straw fluid. saw a lot of white nodules and adhesions everywhere looks like tb. took biopsies sent for afb and pcr. put a small chest tube in. sending him to id floor.",
            6: "A medical thoracoscopy was performed for suspected tuberculous pleuritis in a 46-year-old male. Using moderate sedation, the left pleural space was accessed at the 5th intercostal space. 800 mL of straw-colored fluid was drained. The parietal pleura showed diffuse white nodules and adhesions. Biopsies were taken for pathology and microbiology. A 16 Fr chest tube was inserted. The patient was admitted for observation.",
            7: "[Indication]\nSuspected TB pleuritis, lymphocytic effusion, high ADA.\n[Anesthesia]\nModerate Sedation.\n[Description]\n800 mL fluid drained. Diffuse white nodules/adhesions. Biopsies taken for AFB/Path. 16 Fr chest tube placed.\n[Plan]\nInfectious Disease admission. Await culture/PCR.",
            8: "Mr. Ali underwent a medical thoracoscopy to investigate a suspected tuberculous pleural effusion. After sedation, we introduced the thoracoscope and drained 800 mL of fluid. The inspection revealed widespread white nodules and adhesions on the parietal pleura, strongly suggestive of TB. We obtained multiple biopsies from the chest wall and diaphragm for confirmation. The procedure ended with the placement of a 16 Fr chest tube.",
            9: "Procedure: Thoracoscopic evaluation and sampling.\nDiagnosis: Presumed mycobacterial pleurisy.\nFindings: 800mL fluid evacuated. Miliary nodules and adhesions visualized. Tissue harvested for analysis. Drain secured."
        },
        4: { # Mei Chen (Medical Thoracoscopy - Metastatic Gastric CA)
            1: "Indication: R effusion, gastric CA.\nProc: Med thoracoscopy.\nFluid: 1L serous.\nFindings: Small nodules/plaques diaphragm/basal pleura.\nAction: 10 biopsies. No pleurodesis.\nTube: 20Fr placed.",
            2: "OPERATIVE SUMMARY: Medical Thoracoscopy with Biopsy.\nPATIENT: 62-year-old female with metastatic gastric adenocarcinoma.\nINDICATION: New right-sided pleural effusion; rule out pleural carcinomatosis.\nFINDINGS: Thoracoscopy revealed 1000 mL of serous fluid. The diaphragmatic and basal parietal pleura were studded with multiple small implants and plaques. Ten biopsies were obtained for histologic confirmation and HER2 analysis. Pleurodesis was deferred. A 20 Fr chest tube was placed.",
            3: "CPT: 32609 (Thoracoscopy with pleural biopsy).\nSite: Right hemithorax.\nFindings: 1.0L fluid, pleural nodules/plaques consistent with metastasis.\nAction: Biopsies taken for pathology and molecular testing (HER2). Chest tube placed.\nIndication: Determine if effusion is malignant to guide systemic therapy.",
            4: "Resident Note\nPatient: Mei Chen\nDx: Gastric CA, new effusion.\nProc: Med Thoracoscopy.\nSteps:\n1. GA / ETT.\n2. Scope in R 6th ICS.\n3. Drained 1L.\n4. Biopsied nodules on diaphragm.\n5. Chest tube 20Fr.\nPlan: Oncology to review path.",
            5: "procedure note for mei chen she has stomach cancer and now fluid on the right lung. we did a thoracoscopy under ga. drained a liter of fluid. saw some nodules on the bottom pleura looks like mets. took 10 biopsies sent for her2 testing. didnt do pleurodesis cause they might do chemo. chest tube is in.",
            6: "Medical thoracoscopy was performed on a 62-year-old female with metastatic gastric cancer and a new right pleural effusion. Under general anesthesia, the right pleural space was entered. 1.0 L of serous fluid was drained. Small nodules and plaques were visualized on the diaphragmatic and basal pleura. Ten biopsies were obtained. A 20 Fr chest tube was placed. No pleurodesis was performed.",
            7: "[Indication]\nR pleural effusion, metastatic gastric adenocarcinoma.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\n1.0 L fluid drained. Nodules/plaques on diaphragm/basal pleura. 10 biopsies taken. 20 Fr chest tube placed.\n[Plan]\nPathology (HER2). Tumor board discussion.",
            8: "Ms. Chen was brought to the procedure suite for a medical thoracoscopy to evaluate a new right pleural effusion in the context of her gastric cancer. After inducing general anesthesia, we drained 1.0 L of fluid. We observed multiple small nodules and plaques on the diaphragm and lower chest wall. We took ten biopsies from these areas to confirm metastasis and checking HER2 status. We decided not to perform pleurodesis at this time. A 20 Fr chest tube was inserted.",
            9: "Procedure: Thoracoscopic inspection and tissue sampling.\nContext: Gastric malignancy with new effusion.\nFindings: 1L fluid removed. Pleural implants noted. Specimens collected (10x). No sclerosis. Catheter placed."
        },
        5: { # Zoe Ramirez (Medical Thoracoscopy - Drug-Induced Pleuritis)
            1: "Indication: R effusion, eosinophilia, on Amiodarone.\nProc: Med thoracoscopy.\nFluid: 700ml serous.\nFindings: Mild thickening, petechiae. No nodules.\nAction: 6 biopsies taken. 16Fr chest tube.\nPlan: Stop Amiodarone?",
            2: "PROCEDURE REPORT: Medical Thoracoscopy.\nINDICATION: Evaluation of exudative eosinophilic pleural effusion in a patient recently started on amiodarone.\nFINDINGS: 700 mL of serous fluid was drained. The parietal pleura exhibited mild thickening and scattered petechial hemorrhages; no discrete nodularity was observed. Biopsies were obtained to differentiate drug-induced pleuritis from other etiologies. A 16 Fr chest tube was placed.",
            3: "Code: 32609.\nIndication: Undiagnosed pleural effusion (R/O Amiodarone toxicity).\nProcedure: Right medical thoracoscopy via 6th ICS. 700 mL fluid drained. Biopsy (x6) of thickened parietal pleura. \nPost-procedure: 16 Fr chest tube.",
            4: "Procedure: Med Thoracoscopy\nPatient: Zoe Ramirez\nIndication: ?Amiodarone lung/pleura.\nSteps:\n1. Mod sed.\n2. Scope R 6th ICS.\n3. 700ml fluid out.\n4. Pleura looked red/thick, no masses.\n5. Biopsies taken.\n6. 16Fr tube.\nPlan: Check path, maybe stop amio.",
            5: "zoe ramirez here for the right effusion shes on amiodarone might be that. did a thoracoscopy sedation was good. drained 700cc fluid. pleura just looked a bit thick and red no cancer looking bumps. took 6 biopsies just in case. chest tube 16 french in place. admit to floor.",
            6: "We performed a medical thoracoscopy on a 39-year-old female to investigate a right-sided eosinophilic pleural effusion, possibly secondary to amiodarone. Under moderate sedation, we drained 700 mL of serous fluid. The pleura appeared mildly thickened with petechiae but no obvious nodules. Six biopsies were taken for histology. A 16 Fr chest tube was placed.",
            7: "[Indication]\nR eosinophilic pleural effusion, ?Amiodarone toxicity.\n[Anesthesia]\nModerate Sedation.\n[Description]\n700 mL fluid drained. Mild pleural thickening/petechiae. 6 biopsies taken. 16 Fr chest tube placed.\n[Plan]\nPathology. Cardiology consult.",
            8: "Ms. Ramirez underwent a medical thoracoscopy to evaluate her right pleural effusion, which is suspected to be related to her amiodarone therapy. We drained 700 mL of fluid and inspected the pleura, finding mild thickening and some petechial spots but no distinct masses. We collected six biopsies to rule out other causes. A 16 Fr chest tube was inserted for drainage.",
            9: "Procedure: Thoracoscopic visualization and sampling.\nReason: Effusion with eosinophils.\nObservations: 700mL fluid evacuated. Pleural congestion noted. Tissue harvested (6x). Drain inserted."
        },
        6: { # Connor Davis (Medical Thoracoscopy - Lymphoma)
            1: "Indication: L effusion, DLBCL.\nProc: Med thoracoscopy.\nFluid: 1.2L serous.\nFindings: Mild thickening, pale nodules.\nAction: 10 biopsies (flow/cyto). No pleurodesis.\nTube: 20Fr placed.",
            2: "OPERATIVE NOTE: Medical Thoracoscopy.\nPATIENT: 48-year-old male with Diffuse Large B-Cell Lymphoma.\nINDICATION: New left pleural effusion; rule out pleural involvement.\nFINDINGS: 1200 mL of serous fluid was evacuated. The parietal pleura showed mild thickening with scattered pale nodules. Biopsies were obtained for histology, flow cytometry, and cytogenetics to confirm lymphomatous involvement. A 20 Fr chest tube was placed.",
            3: "CPT: 32609.\nDiagnosis: DLBCL with pleural effusion.\nTechnique: Left medical thoracoscopy. 1.2 L drainage.\nSampling: 10 biopsies taken for special studies (Flow cytometry/Cytogenetics).\nOutcome: 20 Fr chest tube placement.",
            4: "Resident Note\nPatient: Connor Davis\nDx: Lymphoma, new effusion.\nProc: Med Thoracoscopy.\nSteps:\n1. GA / ETT.\n2. Scope L 6th ICS.\n3. Drained 1.2L.\n4. Biopsied pale nodules.\n5. Sent for flow.\n6. Chest tube 20Fr.\nPlan: Chemo adjustment.",
            5: "connor davis has lymphoma and a new effusion on the left. did a thoracoscopy under general. drained 1200 ml fluid. saw some pale bumps on the pleura prob lymphoma. took 10 biopsies sent for flow and genetics. tube is in. admitting to heme.",
            6: "Medical thoracoscopy was performed on a 48-year-old male with DLBCL and a new left pleural effusion. Under general anesthesia, 1.2 L of serous fluid was drained. Mild pleural thickening and pale nodules were observed. Ten biopsies were taken for histology and flow cytometry. A 20 Fr chest tube was placed. No complications occurred.",
            7: "[Indication]\nL pleural effusion, DLBCL.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\n1.2 L fluid drained. Pale pleural nodules seen. 10 biopsies for Flow/Cyto. 20 Fr chest tube placed.\n[Plan]\nHeme/Onc follow-up.",
            8: "Mr. Davis underwent a medical thoracoscopy to investigate a new left pleural effusion in the setting of his lymphoma. We drained 1.2 liters of fluid and found the pleura to be mildly thickened with scattered pale nodules. We obtained ten biopsies to send for flow cytometry and other studies to confirm if the lymphoma has spread to the pleura. A 20 Fr chest tube was placed at the end of the procedure.",
            9: "Procedure: Thoracoscopic exploration and sampling.\nContext: Lymphoma with effusion.\nFindings: 1.2L fluid removed. Pale nodules visualized. Specimens collected (10x) for analysis. Catheter secured."
        },
        7: { # William Scott (Medical Thoracoscopy - Heart Failure/Atypical Cells)
            1: "Indication: R effusion, HF, atypical cells.\nProc: Med thoracoscopy.\nFluid: 1.5L clear.\nFindings: Smooth pleura, no nodules.\nAction: 6 random biopsies. No pleurodesis.\nTube: 20Fr placed.",
            2: "PROCEDURE: Medical Thoracoscopy.\nINDICATION: Large right pleural effusion in heart failure patient with atypical cytology.\nFINDINGS: 1500 mL of clear transudative-appearing fluid was drained. The pleural surfaces appeared smooth and glistening without evidence of nodularity or plaque formation. Random biopsies of the parietal pleura were obtained to definitively exclude malignancy. A 20 Fr chest tube was placed.",
            3: "Code: 32609.\nIndication: R/O Malignancy in HF patient.\nProcedure: Right medical thoracoscopy. 1.5 L fluid drained. Random parietal pleural biopsies (x6) taken despite benign gross appearance. 20 Fr chest tube placed.",
            4: "Procedure: Med Thoracoscopy\nPatient: William Scott\nIndication: HF effusion w/ weird cells.\nSteps:\n1. Mod sed.\n2. Scope R 7th ICS.\n3. Drained 1.5L clear fluid.\n4. Pleura looked normal.\n5. Random biopsies taken.\n6. 20Fr tube.\nPlan: Cardiology admit.",
            5: "mr scott has heart failure and a big effusion with some weird cells. did a thoracoscopy to be sure. drained 1.5 liters clear fluid. pleura looked totally fine smooth. took random biopsies anyway just to check. put a 20 french tube in. back to cardio floor.",
            6: "We performed a medical thoracoscopy on a 74-year-old male with heart failure and a large right pleural effusion with atypical cytology. Under moderate sedation, 1.5 L of clear fluid was drained. The pleura appeared smooth and benign. Six random biopsies were taken to rule out occult malignancy. A 20 Fr chest tube was placed.",
            7: "[Indication]\nR pleural effusion, HF, atypical cytology.\n[Anesthesia]\nModerate Sedation.\n[Description]\n1.5 L clear fluid drained. Smooth pleura. 6 random biopsies taken. 20 Fr chest tube placed.\n[Plan]\nCardiology management. Await path.",
            8: "Mr. Scott underwent a medical thoracoscopy to investigate his large right pleural effusion, which had shown atypical cells despite his history of heart failure. We drained 1.5 liters of clear fluid. The pleura looked healthy and smooth, but we took six random biopsies to be certain there was no malignancy. A 20 Fr chest tube was inserted to continue drainage.",
            9: "Procedure: Thoracoscopic inspection and random sampling.\nReason: Effusion with atypical cells.\nObservations: 1.5L fluid evacuated. Pleura appeared benign. Tissue harvested (6x). Drain inserted."
        },
        8: { # Natalie Perez (Medical Thoracoscopy - Sarcoidosis)
            1: "Indication: R effusion, Sarcoidosis.\nProc: Med thoracoscopy.\nFluid: 600ml yellow.\nFindings: Fine nodularity parietal pleura.\nAction: 8 biopsies. No pleurodesis.\nTube: 16Fr placed.",
            2: "PROCEDURE REPORT: Medical Thoracoscopy.\nINDICATION: Right exudative pleural effusion in a patient with pulmonary sarcoidosis.\nFINDINGS: 600 mL of clear, yellow exudate was drained. The parietal pleura demonstrated fine, diffuse nodularity suggestive of granulomatous inflammation. Biopsies were obtained for histologic confirmation. A 16 Fr chest tube was placed.",
            3: "CPT: 32609.\nDiagnosis: Suspected Sarcoid Pleuritis.\nProcedure: Right medical thoracoscopy via 5th ICS. Drainage of 600 mL exudate. Biopsy (x8) of nodular parietal pleura.\nPost-op: 16 Fr chest tube.",
            4: "Procedure: Med Thoracoscopy\nPatient: Natalie Perez\nIndication: Sarcoid effusion?\nSteps:\n1. Mod sed.\n2. Scope R 5th ICS.\n3. Drained 600cc.\n4. Saw fine nodules.\n5. Biopsied nodules.\n6. 16Fr tube.\nPlan: Pulm f/u.",
            5: "natalie perez has sarcoid and a new effusion on the right. did a thoracoscopy to check it out. drained 600 ml yellow fluid. saw these little bumps on the ribs. took 8 biopsies. chest tube is in. admitting to pulmonary.",
            6: "Medical thoracoscopy was performed on a 44-year-old female with sarcoidosis and a right pleural effusion. Under moderate sedation, 600 mL of yellow fluid was drained. The parietal pleura showed fine nodularity. Eight biopsies were obtained to confirm sarcoid pleuritis. A 16 Fr chest tube was placed.",
            7: "[Indication]\nR pleural effusion, Sarcoidosis.\n[Anesthesia]\nModerate Sedation.\n[Description]\n600 mL fluid drained. Fine pleural nodularity. 8 biopsies taken. 16 Fr chest tube placed.\n[Plan]\nPathology (Granulomas). Adjust steroids.",
            8: "Ms. Perez underwent a medical thoracoscopy to evaluate her right pleural effusion in the setting of sarcoidosis. We drained 600 mL of fluid and observed fine nodularity along the chest wall pleura. We took eight biopsies to confirm granulomatous inflammation. A 16 Fr chest tube was placed for drainage.",
            9: "Procedure: Thoracoscopic visualization and sampling.\nContext: Sarcoidosis with effusion.\nFindings: 600mL fluid removed. Nodular pleura noted. Specimens collected (8x). Catheter secured."
        },
        9: { # Jason Wright (Medical Thoracoscopy - Colorectal Mets)
            1: "Indication: L effusion, metastatic colon CA.\nProc: Med thoracoscopy.\nFluid: 1L straw colored.\nFindings: Scattered nodules/plaques.\nAction: 8 biopsies. No pleurodesis.\nTube: 20Fr placed.",
            2: "OPERATIVE NOTE: Medical Thoracoscopy.\nPATIENT: 63-year-old male with metastatic colorectal adenocarcinoma.\nINDICATION: New symptomatic left pleural effusion.\nFINDINGS: 1000 mL of straw-colored fluid was evacuated. Inspection revealed scattered nodules and subtle plaques on the parietal pleura. Biopsies were obtained for histologic confirmation and molecular profiling (KRAS/NRAS). Pleurodesis was deferred pending treatment planning. A 20 Fr chest tube was placed.",
            3: "Code: 32609.\nIndication: Suspected Pleural Metastasis.\nProcedure: Left medical thoracoscopy. 1.0 L fluid drainage. Targeted biopsy (x8) of pleural nodules.\nPlan: Molecular testing to guide systemic therapy. 20 Fr chest tube.",
            4: "Resident Note\nPatient: Jason Wright\nDx: Colon CA, effusion.\nProc: Med Thoracoscopy.\nSteps:\n1. GA / ETT.\n2. Scope L 6th ICS.\n3. Drained 1L.\n4. Biopsied nodules.\n5. Chest tube 20Fr.\nPlan: Onc f/u.",
            5: "jason wright has colon cancer and fluid on the left. did a thoracoscopy under general. drained a liter. saw some nodules and plaques. took 8 biopsies for kras testing. didnt do pleurodesis cause chemo might change. chest tube is in.",
            6: "Medical thoracoscopy was performed on a 63-year-old male with metastatic colorectal cancer and a left pleural effusion. Under general anesthesia, 1.0 L of fluid was drained. Scattered pleural nodules and plaques were biopsied. Eight samples were sent for pathology and molecular testing. A 20 Fr chest tube was placed. No pleurodesis was performed.",
            7: "[Indication]\nL pleural effusion, metastatic colon CA.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\n1.0 L fluid drained. Scattered nodules/plaques. 8 biopsies taken. 20 Fr chest tube placed.\n[Plan]\nOncology follow-up. Molecular testing.",
            8: "Mr. Wright underwent a medical thoracoscopy to evaluate a new left pleural effusion related to his metastatic colorectal cancer. We drained 1.0 L of fluid and found scattered nodules and plaques on the pleura. We obtained eight biopsies to confirm metastasis and for molecular testing. We decided against pleurodesis at this time. A 20 Fr chest tube was inserted.",
            9: "Procedure: Thoracoscopic inspection and tissue sampling.\nContext: Colorectal malignancy with effusion.\nFindings: 1L fluid removed. Pleural implants visualized. Specimens collected (8x). No sclerosis. Catheter placed."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns lists of mock data (names, original ages) to use for generation.
    Indexes match the source file note indexes.
    """
    return [
        {"idx": 0, "orig_name": "Grace Wilson", "orig_age": 58, "names": ["Alice Baker", "Bertha Charles", "Clara Davis", "Dora Edwards", "Evelyn Frank", "Fiona Green", "Gina Harris", "Helen Ives", "Iris Jones"]},
        {"idx": 1, "orig_name": "Ryan Brooks", "orig_age": 69, "names": ["Arthur King", "Ben Lewis", "Carl Moore", "David Nelson", "Edward Owens", "Frank Perry", "George Quinn", "Henry Roberts", "Ian Smith"]},
        {"idx": 2, "orig_name": "Isabella Martinez", "orig_age": 54, "names": ["Jane Thomas", "Kathy Underwood", "Laura Vance", "Mary Walker", "Nora Xavier", "Olive Young", "Paula Zane", "Quinn Adams", "Rachel Bond"]},
        {"idx": 3, "orig_name": "Ahmed Ali", "orig_age": 46, "names": ["Sam Clark", "Tom Drake", "Uriah Evans", "Victor Ford", "Walter Grey", "Xander Hill", "Yusuf Irwin", "Zachary James", "Adam Kelly"]},
        {"idx": 4, "orig_name": "Mei Chen", "orig_age": 62, "names": ["Betty Long", "Cathy Miller", "Donna Nash", "Ellen Otis", "Fran Parker", "Gail Reed", "Holly Scott", "Irene Tate", "Judy Ursa"]},
        {"idx": 5, "orig_name": "Zoe Ramirez", "orig_age": 39, "names": ["Kara Vance", "Lisa West", "Mona Yates", "Nina Zola", "Opal Allen", "Patty Bell", "Queen Cole", "Rita Day", "Sara Earl"]},
        {"idx": 6, "orig_name": "Connor Davis", "orig_age": 48, "names": ["Bob Fry", "Cal Good", "Dan Hall", "Eli Ivy", "Fred Jack", "Gus Kent", "Hal Lee", "Ike Mann", "Joe Nash"]},
        {"idx": 7, "orig_name": "William Scott", "orig_age": 74, "names": ["Ken Ott", "Leo Poe", "Max Quay", "Ned Ray", "Otis Sims", "Paul Todd", "Quincy Ury", "Ray Vale", "Sid Witt"]},
        {"idx": 8, "orig_name": "Natalie Perez", "orig_age": 44, "names": ["Tina Xray", "Uma Yale", "Vera Zink", "Wanda Ash", "Xena Barr", "Yara Carr", "Zelda Dart", "Amy Eads", "Bea Farr"]},
        {"idx": 9, "orig_name": "Jason Wright", "orig_age": 63, "names": ["Ted Gill", "Ulysses Hart", "Vince Inez", "Will Jett", "Xavier Karr", "Yuri Lane", "Zack Moon", "Al North", "Bill Oats"]}
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
            
            # Deep copy the original note structure to avoid modifying the template
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation from the dictionary
            if idx in variations_text and style_num in variations_text[idx]:
                 note_entry["note_text"] = variations_text[idx][style_num]
            else:
                 print(f"Warning: Missing variation text for Note {idx}, Style {style_num}")
                 continue

            # Update registry_entry fields if they exist to match the new identity
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique for this variation
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            
            # Add metadata about the synthetic generation process
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_blvr_notes_part_081.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()