import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_061_part2.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of stylistic variations for the 10 notes in Part 061.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Grace Wilson - Undiagnosed Pleural Effusion (32609)
            1: "• Indication: Recurrent left exudative effusion, negative cytology.\n• Anesthesia: Moderate sedation, local.\n• Action: US guidance. Single port rigid scope 6th ICS.\n• Drained 1.1L straw fluid.\n• Biopsied granular parietal/diaphragmatic pleura x10.\n• Result: No pleurodesis. 20Fr chest tube placed.\n• Plan: Admit.",
            2: "Operative Report: Mrs. Wilson presented with a recalcitrant left-sided exudative pleural effusion of indeterminate etiology. Under moderate sedation, medical thoracoscopy was performed. Access was achieved via the 6th intercostal space following ultrasound localization. Inspection of the pleural cavity revealed diffuse granular thickening of the parietal and diaphragmatic surfaces with associated fibrin deposition. Extensive biopsies were harvested to elucidate the underlying pathology, specifically investigating for occult malignancy or tuberculous pleuritis. A thoracostomy tube was placed for continued drainage.",
            3: "Procedure: Thoracoscopy, surgical; with biopsy of pleura (32609).\nTechnique: Ultrasound guidance utilized for port placement. A semi-rigid thoracoscope was inserted. The pleural space was explored. Multiple biopsies of the parietal pleura were obtained using biopsy forceps to secure adequate tissue for diagnosis. A chest tube was inserted at the conclusion.",
            4: "Procedure Note\nAttending: Dr. Ross\nIndication: Undiagnosed pleural effusion.\nSteps:\n1. Moderate sedation.\n2. US markings.\n3. Trocar placement 6th ICS.\n4. Drained 1.1L fluid.\n5. Biopsies of parietal pleura taken.\n6. 20Fr chest tube placed.\nPlan: Admit for chest tube management.",
            5: "grace wilson here for the thoracoscopy left side effusion keeps coming back negative cytology so far sedation used went in 6th space drained liter of fluid looked granular biopsied a bunch of spots like 10 times no pleurodesis done chest tube in place admitted for observation.",
            6: "Ultrasound guidance identified a moderate free flowing left pleural effusion A single port semi rigid thoracoscope was introduced at the 6th intercostal space Approximately 1 1 L of cloudy straw colored fluid was drained Thoracoscopic inspection revealed diffuse granular parietal pleural thickening with scattered small nodules and fibrin strands Multiple biopsies 10 samples were taken from abnormal parietal pleura and diaphragmatic pleura No chemical or mechanical pleurodesis was performed A 20 Fr chest tube was placed to water seal.",
            7: "[Indication]\nRecurrent undiagnosed left exudative pleural effusion.\n[Anesthesia]\nModerate sedation (midazolam/fentanyl).\n[Description]\nMedical thoracoscopy via 6th ICS. 1.1L fluid drained. Diffuse granular pleural thickening noted. 10 biopsies taken. 20Fr Chest tube placed.\n[Plan]\nAdmit. Await pathology.",
            8: "The patient was brought to the procedure suite for a medical thoracoscopy due to a recurrent left exudative pleural effusion. After inducing moderate sedation, we used ultrasound to guide our entry at the 6th intercostal space. We drained approximately 1.1 liters of cloudy fluid. Upon inspection, the pleura appeared granular with some fibrin strands. We took multiple biopsies from the parietal and diaphragmatic pleura to rule out TB or cancer. No pleurodesis was done, and we left a 20 French chest tube in place.",
            9: "Ultrasound guidance located a moderate left pleural effusion. A single-port thoracoscope was inserted at the 6th intercostal space. Roughly 1.1 L of fluid was evacuated. Thoracoscopic examination showed diffuse granular parietal pleural thickening. Multiple specimens (10 samples) were harvested from abnormal parietal pleura. No pleurodesis was executed. A 20 Fr chest tube was positioned to water seal."
        },
        1: { # Ryan Brooks - Suspected Mesothelioma (32609)
            1: "• Indication: Right pleural thickening/effusion, suspect mesothelioma.\n• Anesthesia: GA, ETT.\n• Procedure: 5th ICS access. Drained 900mL.\n• Findings: Diffuse nodular thickening.\n• Action: 12 biopsies taken. No pleurodesis.\n• Plan: 24Fr Chest tube. Admit.",
            2: "Operative Narrative: Mr. Brooks, with significant asbestos exposure history, underwent diagnostic thoracoscopy for suspected malignant pleural mesothelioma. Under general anesthesia, the right hemithorax was accessed. Exploration revealed pathognomonic diffuse nodular and plaque-like thickening involving the parietal and diaphragmatic pleura. Substantial tissue sampling was performed to facilitate definitive histologic subtyping and biomarker analysis. The procedure concluded with chest tube placement; chemical pleurodesis was deferred pending oncologic staging.",
            3: "Code: 32609 (Surgical thoracoscopy with biopsy). The pleural cavity was entered under general anesthesia. Visual inspection confirmed extensive pleural disease. Rigid forceps were used to obtain multiple biopsies of the parietal pleura for diagnostic confirmation. A chest drainage device was placed.",
            4: "Resident Note\nPatient: Ryan Brooks\nProcedure: Medical Thoracoscopy.\nStaff: Dr. Stone.\nSteps:\n1. GA induced.\n2. Trocar placed 5th ICS.\n3. Fluid drained (900cc).\n4. Nodular pleura biopsied x12.\n5. Hemostasis with cautery.\n6. 24Fr Chest tube placed.\nPlan: Floor admission.",
            5: "ryan brooks note for mesothelioma workup right side effusion ga used went in 5th rib space drained some fluid saw nodules everywhere classic for meso took big biopsies 12 pieces bleeding controlled with cautery chest tube in placed no talc yet wait for path.",
            6: "Right 5th intercostal space midaxillary line was chosen under ultrasound After trocar placement 900 mL of serous fluid was drained Thoracoscopy revealed diffuse nodular and plaque like thickening of the parietal pleura especially over the diaphragmatic and posterior chest wall Multiple large biopsies 12 samples were obtained with rigid forceps from representative areas No pleurodesis was performed due to diagnostic intent and uncertain staging plan A 24 Fr chest tube was placed to water seal.",
            7: "[Indication]\nSuspected malignant pleural mesothelioma.\n[Anesthesia]\nGeneral anesthesia.\n[Description]\nRight medical thoracoscopy. 900mL drained. Diffuse nodular pleural thickening seen. 12 biopsies obtained. 24Fr Chest tube inserted.\n[Plan]\nAdmit. Oncology referral.",
            8: "We performed a medical thoracoscopy on Mr. Brooks to investigate suspected mesothelioma. Under general anesthesia, we entered the right chest at the 5th intercostal space and drained 900 mL of fluid. The pleura showed diffuse nodular thickening, consistent with our suspicion. We took twelve biopsies from various areas for pathology. We decided against pleurodesis at this time to keep staging options open and placed a 24 French chest tube.",
            9: "Right 5th intercostal space was selected under ultrasound. After trocar insertion, 900 mL of serous fluid was evacuated. Thoracoscopy uncovered diffuse nodular thickening of the parietal pleura. Multiple large specimens (12 samples) were acquired with rigid forceps. No pleurodesis was executed. A 24 Fr chest tube was positioned to water seal."
        },
        2: { # Isabella Martinez - Rheumatoid Pleuritis (32609)
            1: "• Indication: Recurrent R effusion, RA hx.\n• Anesthesia: Moderate sedation.\n• Port: 6th ICS. 900mL drained.\n• Findings: Inflamed pleura, whitish nodules.\n• Action: Biopsied x8.\n• Result: 16Fr chest tube placed.\n• Plan: Rheumatology f/u.",
            2: "Procedure Note: Ms. Martinez, presenting with a complex right pleural effusion in the setting of seropositive rheumatoid arthritis, underwent medical thoracoscopy. The objective was to differentiate rheumatoid pleuritis from potential malignancy. Intraoperative findings included diffuse pleural erythema and fine nodularity. Biopsies were systematically obtained to provide histopathologic confirmation. The procedure was uncomplicated, and a small-bore chest tube was sited.",
            3: "Billing: 32609 (Thoracoscopy with biopsy). Ultrasound guidance used. The pleural space was accessed. Visual inspection revealed inflammation. Biopsies of the parietal pleura were taken to rule out malignancy and confirm inflammatory etiology. Chest tube placed.",
            4: "Procedure: Thoracoscopy\nPatient: Isabella Martinez\nIndication: RA pleural effusion.\nSteps:\n1. Sedation.\n2. Access 6th ICS.\n3. Drained 900cc cloudy fluid.\n4. Biopsied inflamed pleura.\n5. 16Fr Chest tube.\nPlan: Admit to Rheum.",
            5: "isabella martinez procedure note she has RA and this effusion wont go away did the thoracoscopy right side drained cloudy yellow fluid pleura looked red with little white bumps biopsied it 8 times no pleurodesis chest tube placed 16fr stable.",
            6: "Ultrasound confirmed a moderate right effusion without loculations A semi rigid thoracoscope was introduced at the 6th intercostal space 900 mL of cloudy yellow fluid was removed Parietal pleura appeared diffusely inflamed with small whitish nodules no bulky tumor Multiple biopsies 8 samples were obtained from parietal and diaphragmatic pleura No pleurodesis performed A 16 Fr chest tube was left in place.",
            7: "[Indication]\nRecurrent right effusion in RA patient.\n[Anesthesia]\nModerate sedation.\n[Description]\nThoracoscopy 6th ICS. 900mL cloudy fluid drained. Inflamed pleura with nodules. Biopsies x8. 16Fr chest tube.\n[Plan]\nAdmit. Rheum consult.",
            8: "Ms. Martinez underwent a medical thoracoscopy to investigate her recurrent right pleural effusion. Given her history of rheumatoid arthritis, we needed to rule out other causes. We accessed the chest under sedation and drained 900 mL of cloudy fluid. The pleura looked inflamed with some small nodules, so we took eight biopsies. We placed a 16 French chest tube and sent her to the floor for observation.",
            9: "Ultrasound verified a moderate right effusion. A semi-rigid thoracoscope was inserted at the 6th intercostal space. 900 mL of cloudy fluid was evacuated. Parietal pleura appeared diffusely inflamed with small whitish nodules. Multiple specimens (8 samples) were acquired. No pleurodesis executed. A 16 Fr chest tube was left in situ."
        },
        3: { # Ahmed Ali - TB Pleuritis (32609)
            1: "• Indication: Suspected TB pleuritis, L effusion.\n• Anesthesia: Moderate sedation.\n• 5th ICS access. 800mL straw fluid.\n• Findings: Whitish nodules, adhesions.\n• Biopsies: Costal/diaphragmatic pleura.\n• Chest tube: 16Fr.\n• Plan: TB w/u.",
            2: "Operative Report: Mr. Ali underwent diagnostic thoracoscopy for evaluation of a lymphocyte-predominant exudative effusion suspicious for tuberculous pleuritis. Visual inspection of the pleural cavity revealed classic findings of diffuse granulomatous inflammation, characterized by whitish nodules and fibrinous adhesions. Biopsies were obtained for AFB staining, culture, and histologic examination to confirm the diagnosis of Mycobacterium tuberculosis infection.",
            3: "Code: 32609. Procedure involved thoracoscopic access to the pleural space. Inspection identified nodules consistent with granulomatous disease. Biopsies of the pleura were performed for microbiological and histological analysis. Chest tube placed for drainage.",
            4: "Procedure Note\nIndication: Rule out TB pleuritis.\nStaff: Dr. Cole\nSteps:\n1. Sedation.\n2. Access 5th ICS.\n3. Drained 800cc.\n4. Biopsied nodules/pleura.\n5. 16Fr Chest tube.\nPlan: ID admission.",
            5: "ahmed ali procedure for tb pleuritis suspicion left side effusion drained 800ml straw colored looks like tb lots of white nodules and adhesions biopsied the pleura sent for afb and culture chest tube in place admit to id floor.",
            6: "Ultrasound demonstrated moderate left pleural effusion A single port thoracoscope was introduced at the 5th intercostal space 800 mL of straw colored fluid was drained Parietal pleura displayed diffuse whitish nodules and fibrinous adhesions Multiple biopsies were obtained from costal and diaphragmatic pleura No pleurodesis was performed A 16 Fr chest tube was placed under water seal.",
            7: "[Indication]\nSuspected tuberculous pleuritis.\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft thoracoscopy. 800mL drained. Whitish nodules and adhesions seen. Biopsies taken for AFB/pathology. 16Fr chest tube placed.\n[Plan]\nAdmit. Empiric TB tx if confirmed.",
            8: "Mr. Ali presented with a left pleural effusion and symptoms suggestive of TB. We performed a medical thoracoscopy under sedation. We drained 800 mL of fluid and observed whitish nodules and adhesions on the pleura, which is often seen with TB. We took multiple biopsies to send for testing. A 16 French chest tube was placed, and he was admitted for further care.",
            9: "Ultrasound showed moderate left pleural effusion. A single-port thoracoscope was inserted at the 5th intercostal space. 800 mL of straw-colored fluid was evacuated. Parietal pleura displayed diffuse whitish nodules. Multiple specimens were acquired. No pleurodesis was executed. A 16 Fr chest tube was positioned under water seal."
        },
        4: { # Mei Chen - Gastric Cancer Mets (32609)
            1: "• Indication: Metastatic gastric ca, R effusion.\n• Anesthesia: GA, ETT.\n• 6th ICS access. 1.0L drained.\n• Findings: Nodules/plaques on diaphragm.\n• Action: Biopsies x10. No pleurodesis.\n• Tube: 20Fr.\n• Plan: Oncology w/u.",
            2: "Procedure Narrative: Ms. Chen, with known metastatic gastric adenocarcinoma, presented with a new right pleural effusion. Thoracoscopy was performed to evaluate for pleural carcinomatosis. Inspection revealed multiple metastatic deposits on the diaphragmatic and parietal pleura. Biopsies were harvested for confirmation and HER2 receptor testing. Pleurodesis was deferred to allow for potential intraperitoneal chemotherapy considerations.",
            3: "Billing Code: 32609 (Surgical thoracoscopy with pleural biopsy). The procedure involved visual inspection of the hemithorax and biopsy of suspicious nodules on the parietal pleura to confirm metastatic disease. A chest tube was placed for drainage.",
            4: "Resident Note\nPatient: Mei Chen\nProcedure: Thoracoscopy.\nIndication: R pleural effusion/mets.\nSteps:\n1. GA.\n2. Trocar 6th ICS.\n3. Drained 1L.\n4. Biopsied nodules x10.\n5. 20Fr Chest tube.\nPlan: Oncology floor.",
            5: "mei chen procedure note gastric cancer with new effusion right side went in with scope drained a liter of fluid saw spots on the diaphragm likely mets biopsied them 10 times didn't do pleurodesis just in case she needs ip chemo chest tube placed.",
            6: "A semi rigid thoracoscope was introduced via the right 6th intercostal space 1 0 L of serous fluid was drained Multiple small nodules and plaques were seen over the diaphragmatic and basal parietal pleura Representative biopsies 10 samples were obtained No pleurodesis was performed due to uncertainty about future systemic therapy plan and potential need for intraperitoneal chemotherapy A 20 Fr chest tube was placed.",
            7: "[Indication]\nSuspected pleural mets from gastric cancer.\n[Anesthesia]\nGeneral.\n[Description]\nRight thoracoscopy. 1L drained. Nodules on diaphragm biopsied. No pleurodesis. 20Fr Chest tube.\n[Plan]\nAdmit. Tumor board discussion.",
            8: "Ms. Chen underwent a medical thoracoscopy to investigate a new right pleural effusion in the context of her gastric cancer. Under general anesthesia, we drained 1 liter of fluid and found multiple small nodules on the diaphragm and pleura. We took ten biopsies for testing. We decided not to perform pleurodesis at this time to keep her treatment options open. A 20 French chest tube was placed.",
            9: "A semi-rigid thoracoscope was inserted via the right 6th intercostal space. 1.0 L of serous fluid was evacuated. Multiple small nodules and plaques were observed over the diaphragmatic and basal parietal pleura. Representative specimens (10 samples) were acquired. No pleurodesis was executed. A 20 Fr chest tube was positioned."
        },
        5: { # Zoe Ramirez - Drug Induced (32609)
            1: "• Indication: R effusion, Amiodarone use.\n• Anesthesia: Moderate sedation.\n• 6th ICS. 700mL drained.\n• Findings: Mild thickening, petechiae.\n• Biopsies: x6. No pleurodesis.\n• Tube: 16Fr.\n• Plan: Stop amiodarone?",
            2: "Operative Report: Ms. Ramirez underwent diagnostic thoracoscopy for evaluation of a right-sided pleural effusion with eosinophilia, temporally associated with amiodarone therapy. Thoracoscopic inspection revealed mild pleural thickening and petechial hemorrhages, findings consistent with drug-induced pleuritis. Biopsies were obtained to exclude other etiologies such as malignancy or autoimmune disease.",
            3: "Code: 32609. Thoracoscopic visualization of the pleural space was performed. Biopsies of the parietal pleura were taken to investigate the etiology of the effusion (suspected drug reaction vs other). Chest tube inserted.",
            4: "Procedure Note\nIndication: Drug-induced pleuritis?\nSteps:\n1. Sedation.\n2. Port 6th ICS.\n3. Drained 700cc.\n4. Biopsied pleura x6.\n5. 16Fr Chest tube.\nPlan: Obs.",
            5: "zoe ramirez note amiodarone lung toxicity suspected right effusion thoracoscopy done drained 700ml looks like mild inflammation with some red spots biopsied it to be sure no nodules seen chest tube in place 16 french.",
            6: "Ultrasound demonstrated a moderate right effusion A semi rigid thoracoscope was advanced via the 6th intercostal space 700 mL of serous fluid was removed Parietal pleura appeared mildly thickened with scattered petechial hemorrhages but no distinct nodules Multiple biopsies 6 samples were obtained No pleurodesis was performed A 16 Fr chest tube was left in situ.",
            7: "[Indication]\nSuspected amiodarone-induced pleuritis.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight thoracoscopy. 700mL drained. Pleura mildly thickened with petechiae. Biopsies x6. 16Fr chest tube.\n[Plan]\nAdmit. Cardio consult.",
            8: "We performed a thoracoscopy on Ms. Ramirez to evaluate her right pleural effusion, suspecting it might be related to her amiodarone medication. We drained 700 mL of fluid and saw some mild thickening and small red spots on the pleura. We took six biopsies to rule out other causes. We didn't do pleurodesis and left a 16 French chest tube in place.",
            9: "Ultrasound showed a moderate right effusion. A semi-rigid thoracoscope was advanced via the 6th intercostal space. 700 mL of serous fluid was removed. Parietal pleura appeared mildly thickened with scattered petechial hemorrhages. Multiple specimens (6 samples) were acquired. No pleurodesis was executed. A 16 Fr chest tube was left in situ."
        },
        6: { # Connor Davis - Lymphoma (32609)
            1: "• Indication: L effusion, DLBCL.\n• Anesthesia: GA.\n• 6th ICS. 1.2L drained.\n• Findings: Mild thickening, pale nodules.\n• Action: Biopsies x10 (Flow, cyto).\n• Tube: 20Fr.\n• Plan: Hem/Onc.",
            2: "Procedure Narrative: Mr. Davis, with a history of diffuse large B-cell lymphoma, presented with a new left pleural effusion. Medical thoracoscopy was performed to distinguish between paramalignant effusion and direct pleural involvement. Inspection revealed scattered pale nodules on the parietal pleura. Biopsies were obtained and submitted for flow cytometry and histology to guide further chemotherapy.",
            3: "Billing: 32609 (Thoracoscopy w/ biopsy). The pleural space was accessed under general anesthesia. Suspicious nodules were biopsied to stage the lymphoma (pleural involvement). Chest tube placed.",
            4: "Resident Note\nPatient: Connor Davis\nIndication: Lymphoma/Effusion.\nSteps:\n1. GA.\n2. Access 6th ICS.\n3. Drained 1.2L.\n4. Biopsied nodules for flow.\n5. 20Fr Tube.\nPlan: Admit.",
            5: "connor davis procedure note lymphoma patient with new left effusion thoracoscopy done drained 1.2 liters saw some pale bumps on the pleura biopsied them sent for flow cytometry and path chest tube placed 20fr.",
            6: "Left 6th intercostal space was accessed under ultrasound guidance 1 2 L of serous fluid was evacuated Parietal pleura appeared mildly thickened with scattered pale nodules Multiple biopsies 10 samples were taken and submitted for histology flow cytometry and cytogenetics No pleurodesis was performed A 20 Fr chest tube was positioned posteriorly.",
            7: "[Indication]\nLeft pleural effusion in DLBCL.\n[Anesthesia]\nGeneral.\n[Description]\nLeft thoracoscopy. 1.2L fluid drained. Pale nodules biopsied for flow/pathology. 20Fr chest tube placed.\n[Plan]\nAdmit. Adjust chemo.",
            8: "Mr. Davis underwent a medical thoracoscopy to check if his lymphoma had spread to the pleura. We drained 1.2 liters of fluid and found some pale nodules. We took ten biopsies to send for flow cytometry and other tests. A 20 French chest tube was placed, and he was admitted to the hematology ward.",
            9: "Left 6th intercostal space was accessed under ultrasound guidance. 1.2 L of serous fluid was evacuated. Parietal pleura appeared mildly thickened with scattered pale nodules. Multiple specimens (10 samples) were acquired. No pleurodesis was executed. A 20 Fr chest tube was positioned posteriorly."
        },
        7: { # William Scott - Transudate? (32609)
            1: "• Indication: Heart failure, R effusion, atypical cells.\n• Anesthesia: Moderate sedation.\n• 7th ICS. 1.5L clear fluid.\n• Findings: Smooth pleura.\n• Action: Random biopsies x6.\n• Tube: 20Fr.\n• Plan: Diuresis.",
            2: "Operative Report: Mr. Scott, with known heart failure, underwent thoracoscopy due to an atypical cytologic finding in a recurrent right pleural effusion. Intraoperative inspection revealed smooth, glistening pleura without gross evidence of malignancy. Random biopsies were performed to definitively exclude neoplastic involvement. A chest tube was placed for continued drainage.",
            3: "Code: 32609. Thoracoscopy performed to investigate an effusion with atypical cytology. Despite benign gross appearance, biopsies of the parietal pleura were taken to rule out malignancy. Chest tube inserted.",
            4: "Procedure Note\nIndication: Atypical cells/HF effusion.\nSteps:\n1. Sedation.\n2. Port 7th ICS.\n3. Drained 1.5L.\n4. Pleura looked normal.\n5. Random biopsies x6.\n6. 20Fr Tube.\nPlan: Cardiology.",
            5: "william scott note heart failure patient with effusion atypical cells on tap did the thoracoscopy right side drained 1.5 liters looked pretty normal inside smooth pleura took some random biopsies just in case 20fr chest tube placed.",
            6: "Ultrasound guided entry at the right 7th intercostal space 1 5 L of clear straw colored fluid was drained Thoracoscopy revealed smooth glistening pleura without nodules Multiple random biopsies 6 samples of parietal pleura were obtained No pleurodesis performed A 20 Fr chest tube was left in place on water seal.",
            7: "[Indication]\nHeart failure effusion with atypical cytology.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight thoracoscopy. 1.5L clear fluid. Pleura grossly normal. Random biopsies obtained. 20Fr chest tube.\n[Plan]\nAdmit. Diuresis.",
            8: "Mr. Scott had a thoracoscopy because of some suspicious cells found in his pleural fluid, despite his history of heart failure. We drained 1.5 liters of clear fluid. The pleura looked smooth and healthy, but we took six random biopsies to be safe and rule out cancer. We left a 20 French chest tube in place.",
            9: "Ultrasound-guided entry at the right 7th intercostal space. 1.5 L of clear, straw-colored fluid was evacuated. Thoracoscopy showed smooth glistening pleura without nodules. Multiple random specimens (6 samples) of parietal pleura were acquired. No pleurodesis executed. A 20 Fr chest tube was left in situ on water seal."
        },
        8: { # Natalie Perez - Sarcoidosis (32609)
            1: "• Indication: Sarcoidosis, R effusion.\n• Anesthesia: Moderate sedation.\n• 5th ICS. 600mL drained.\n• Findings: Fine nodularity.\n• Action: Biopsies x8.\n• Tube: 16Fr.\n• Plan: Pulm f/u.",
            2: "Procedure Narrative: Ms. Perez underwent medical thoracoscopy to investigate a new exudative pleural effusion in the setting of pulmonary sarcoidosis. The procedure revealed fine, diffuse nodularity of the parietal pleura. Biopsies were taken to confirm pleural sarcoidosis and exclude other granulomatous or malignant processes.",
            3: "Billing: 32609. Thoracoscopy with pleural biopsy. The procedure was indicated to diagnose the etiology of the pleural effusion. Visual findings suggested granulomatous disease. Biopsies were obtained for confirmation.",
            4: "Procedure Note\nIndication: Sarcoid effusion?\nSteps:\n1. Sedation.\n2. Access 5th ICS.\n3. Drained 600cc.\n4. Biopsied nodular pleura.\n5. 16Fr Tube.\nPlan: Steroids?",
            5: "natalie perez note sarcoid patient with effusion right side thoracoscopy done drained 600ml saw fine nodules looks like sarcoid pleuritis biopsied it 8 times chest tube in place 16fr stable.",
            6: "Ultrasound demonstrated a small to moderate right free flowing effusion A semi rigid thoracoscope was introduced at the 5th intercostal space 600 mL of clear yellow exudate was drained Parietal pleura showed fine nodularity along the ribs Multiple biopsies 8 samples were obtained No pleurodesis was done A 16 Fr chest tube was left to drain.",
            7: "[Indication]\nRight effusion in sarcoidosis.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight thoracoscopy. 600mL drained. Fine pleural nodularity. Biopsies x8. 16Fr chest tube.\n[Plan]\nAdmit. Pathology pending.",
            8: "We performed a thoracoscopy on Ms. Perez to see if her sarcoidosis was causing her right pleural effusion. We drained 600 mL of fluid and saw fine nodules on the pleura. We took eight biopsies to confirm the diagnosis. A 16 French chest tube was placed, and she is doing well.",
            9: "Ultrasound showed a small-to-moderate right free-flowing effusion. A semi-rigid thoracoscope was inserted at the 5th intercostal space. 600 mL of clear, yellow exudate was evacuated. Parietal pleura showed fine nodularity along the ribs. Multiple specimens (8 samples) were acquired. No pleurodesis was executed. A 16 Fr chest tube was left to drain."
        },
        9: { # Jason Wright - Colorectal Mets (32609)
            1: "• Indication: Colorectal mets, L effusion.\n• Anesthesia: GA.\n• 6th ICS. 1.0L drained.\n• Findings: Nodules/plaques.\n• Action: Biopsies x8.\n• Tube: 20Fr.\n• Plan: Tumor board.",
            2: "Operative Note: Mr. Wright, with metastatic colorectal carcinoma, underwent thoracoscopy for a new malignant-appearing left pleural effusion. Inspection confirmed the presence of scattered metastatic nodules and plaques on the parietal pleura. Biopsies were obtained for histologic confirmation and molecular profiling (KRAS/NRAS).",
            3: "Code: 32609. Thoracoscopy with biopsy of pleura. Access established. Visual confirmation of metastatic disease. Biopsies taken for pathology and molecular testing. Chest tube placed.",
            4: "Resident Note\nPatient: Jason Wright\nIndication: Colorectal mets.\nSteps:\n1. GA.\n2. Access 6th ICS.\n3. Drained 1L.\n4. Biopsied nodules.\n5. 20Fr Tube.\nPlan: Onc.",
            5: "jason wright procedure note colorectal cancer with new effusion left side thoracoscopy done drained a liter saw nodules and plaques likely mets biopsied them 8 times no pleurodesis chest tube placed.",
            6: "Ultrasound guided access at the left 6th intercostal space allowed insertion of a semi rigid thoracoscope 1 0 L of straw colored fluid was drained Parietal pleura showed scattered small nodules and subtle plaques Multiple biopsies 8 samples were taken No pleurodesis performed because systemic therapy options are being reconsidered A 20 Fr chest tube was placed.",
            7: "[Indication]\nMetastatic colorectal cancer, left effusion.\n[Anesthesia]\nGeneral.\n[Description]\nLeft thoracoscopy. 1L drained. Pleural nodules biopsied. No pleurodesis. 20Fr chest tube.\n[Plan]\nAdmit. Molecular testing.",
            8: "Mr. Wright underwent a thoracoscopy to investigate a new left pleural effusion given his history of colorectal cancer. We drained 1 liter of fluid and found scattered nodules on the pleura. We took eight biopsies for testing. We didn't do pleurodesis as his treatment plan is being reviewed. A 20 French chest tube was placed.",
            9: "Ultrasound-guided access at the left 6th intercostal space allowed insertion of a semi-rigid thoracoscope. 1.0 L of straw-colored fluid was evacuated. Parietal pleura showed scattered small nodules and subtle plaques. Multiple specimens (8 samples) were acquired. No pleurodesis executed. A 20 Fr chest tube was positioned."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data to replace names and ages for the 10 source notes.
    """
    return [
        {"idx": 0, "orig_name": "Grace Wilson", "orig_age": 58, "names": ["Alice Smith", "Mary Johnson", "Patricia Brown", "Linda Davis", "Elizabeth Miller", "Barbara Wilson", "Susan Moore", "Jessica Taylor", "Sarah Anderson"]},
        {"idx": 1, "orig_name": "Ryan Brooks", "orig_age": 69, "names": ["James Jackson", "John White", "Robert Harris", "Michael Martin", "William Thompson", "David Garcia", "Richard Martinez", "Joseph Robinson", "Charles Clark"]},
        {"idx": 2, "orig_name": "Isabella Martinez", "orig_age": 54, "names": ["Karen Rodriguez", "Nancy Lewis", "Lisa Lee", "Betty Walker", "Margaret Hall", "Sandra Allen", "Ashley Young", "Kimberly Hernandez", "Donna King"]},
        {"idx": 3, "orig_name": "Ahmed Ali", "orig_age": 46, "names": ["Thomas Wright", "Daniel Lopez", "Paul Hill", "Mark Scott", "Donald Green", "George Adams", "Kenneth Baker", "Steven Gonzalez", "Edward Nelson"]},
        {"idx": 4, "orig_name": "Mei Chen", "orig_age": 62, "names": ["Brian Carter", "Ronald Mitchell", "Anthony Perez", "Kevin Roberts", "Jason Turner", "Matthew Phillips", "Gary Campbell", "Timothy Parker", "Jose Evans"]},
        {"idx": 5, "orig_name": "Zoe Ramirez", "orig_age": 39, "names": ["Larry Edwards", "Jeffrey Collins", "Frank Stewart", "Scott Sanchez", "Eric Morris", "Stephen Rogers", "Andrew Reed", "Raymond Cook", "Gregory Morgan"]},
        {"idx": 6, "orig_name": "Connor Davis", "orig_age": 48, "names": ["Joshua Bell", "Jerry Murphy", "Dennis Bailey", "Walter Rivera", "Patrick Cooper", "Peter Richardson", "Harold Cox", "Douglas Howard", "Henry Ward"]},
        {"idx": 7, "orig_name": "William Scott", "orig_age": 74, "names": ["Carol Torres", "Michelle Peterson", "Emily Gray", "Helen Ramirez", "Amanda James", "Melissa Watson", "Deborah Brooks", "Stephanie Kelly", "Rebecca Sanders"]},
        {"idx": 8, "orig_name": "Natalie Perez", "orig_age": 44, "names": ["Carl Price", "Arthur Bennett", "Ryan Wood", "Roger Barnes", "Joe Ross", "Juan Henderson", "Jack Coleman", "Albert Jenkins", "Jonathan Perry"]},
        {"idx": 9, "orig_name": "Jason Wright", "orig_age": 63, "names": ["Sharon Powell", "Cynthia Long", "Kathleen Patterson", "Amy Hughes", "Shirley Flores", "Angela Washington", "Anna Butler", "Ruth Simmons", "Brenda Foster"]}
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
            
            # Get the specific name assigned for this variation
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            # Use safe get just in case index logic drifts
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Variation text missing for Note {idx} Style {style_num}. Using original.")
            
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
    output_filename = output_dir / "synthetic_thoracoscopy_notes_part_061.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()