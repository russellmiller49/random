import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_056_part2.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # John Taylor (Right Thoracoscopy, Biopsy, Talc)
            1: "Proc: Right Medical Thoracoscopy, Biopsy, Talc Poudrage.\nIndication: Suspected mesothelioma.\nFindings: Diffuse pleural nodularity.\nActions:\n- Single port 6th ICS.\n- Pleuroscope inserted.\n- 7 biopsies taken from parietal pleura.\n- Diaphragmatic biopsies taken.\n- Talc poudrage performed.\n- Chest tube placed.\nComp: None. Hemostasis achieved.\nDisp: Floor.",
            2: "OPERATIVE REPORT\n\nINDICATION: This 82-year-old male presented with a right-sided pleural effusion suspicious for malignant mesothelioma. Diagnostic and therapeutic thoracoscopy was indicated.\n\nPROCEDURE NARRATIVE: Under moderate sedation and local anesthesia, the right hemithorax was accessed via the 6th intercostal space. Thoracoscopic inspection revealed diffuse, significant nodularity involving the parietal and diaphragmatic pleura. Seven (7) distinct biopsy specimens were harvested from the parietal surface, with additional sampling of the diaphragm to ensure diagnostic yield. Given the gross appearance consistent with malignancy, definitive pleurodesis was undertaken using sterile talc poudrage. Complete lung re-expansion was verified visually. A chest tube was secured.\n\nIMPRESSION: Right pleural malignancy with successful biopsy and chemical pleurodesis.",
            3: "CPT Rationale: 32609 (Thoracoscopy with biopsy of pleura), 32650 (Thoracoscopy with pleurodesis).\nTechnique: Right chest accessed. Pleura visualized. Multiple biopsies (n=7) obtained using biopsy forceps from parietal pleura to support diagnosis. Talc agent insufflated into pleural space (poudrage) for pleurodesis (32650). Fluid evacuated. Chest tube inserted. \nNote: Biopsy and pleurodesis performed during same session distinct from diagnostic only.",
            4: "Procedure: Medical Thoracoscopy w/ Biopsy and Talc\nAttending: Dr. Park\nResident: Dr. Patel\n\nSteps:\n1. Time out. Moderate sedation.\n2. Local anesthetic to 6th ICS, Mid-axillary line.\n3. Trocar placed. Scope inserted.\n4. Fluid drained. Extensive nodules seen.\n5. Biopsies x7 parietal, plus diaphragmatic.\n6. Talc poudrage for pleurodesis.\n7. Chest tube placed to suction.\n\nPlan: Admit, wait for path.",
            5: "Procedure note for John Taylor right side thoracoscopy looking for mesothelioma. We went in at the 6th rib space used the semi rigid scope. Saw a lot of nodules everywhere on the pleura so we took a bunch of biopsies like 7 of them from the wall and some from the diaphragm too. Since it looked like cancer we puffed in the talc for pleurodesis drained all the fluid put a chest tube in. No air leak bleeding stopped patient went to the floor.",
            6: "Medical Thoracoscopy with Pleural Biopsy and Pleurodesis. Suspected mesothelioma. Right side. Under moderate sedation with local anesthesia, a single-port entry was made at the 6th intercostal space. The semi-rigid pleuroscope was inserted. Inspection revealed diffuse pleural nodularity. Multiple biopsies were obtained from the parietal pleura (7 specimens) and diaphragmatic pleura. Specimens sent for histopathology. Given findings, talc poudrage was performed for pleurodesis. All fluid was evacuated and a chest tube was placed. Hemostasis confirmed. No air leak. Floor admission.",
            7: "[Indication]\nSuspected mesothelioma, right side.\n[Anesthesia]\nModerate sedation, local anesthesia.\n[Description]\nEntry 6th ICS. Inspection: diffuse nodularity. Action: 7 parietal biopsies, diaphragmatic biopsies. Intervention: Talc poudrage pleurodesis. Tube placed.\n[Plan]\nAdmit to floor. Suction. Path pending.",
            8: "The patient, an 82-year-old male, was brought to the endoscopy suite for a right-sided medical thoracoscopy due to suspected mesothelioma. After achieving moderate sedation, we entered the chest wall at the 6th intercostal space. Upon inserting the pleuroscope, we immediately visualized diffuse nodularity across the pleural surface. We proceeded to take seven biopsies from the parietal pleura and additional samples from the diaphragm. Because the findings strongly suggested malignancy, we performed a talc poudrage to prevent fluid recurrence. The chest was drained, and a tube was placed.",
            9: "PROCEDURE: Medical Thoracoscopy with Pleural Sampling and Talc Insufflation\nSide: Right\n\nMethod: Under sedation, the scope was introduced. The pleural space was surveyed. Diffuse nodularity was observed. We harvested 7 specimens from the parietal pleura and sampled the diaphragm. Subsequently, talc was deposited for pleurodesis. The fluid was drained, and a drain was anchored. \nStatus: Hemostasis secured."
        },
        1: { # Susan Rivera (Right Thoracoscopy, Biopsy, No Talc)
            1: "Proc: Medical Thoracoscopy (Right) + Biopsy.\nIndication: Exudative effusion, cytology negative.\nFindings: Inflammatory changes, no nodules.\nAction: 12 parietal biopsies taken. Diaphragmatic biopsies taken. Fluid drained. Chest tube placed.\nNote: No pleurodesis performed.\nPlan: Admit. Suction.",
            2: "PROCEDURE PERFORMED: Diagnostic Medical Thoracoscopy with Parietal and Diaphragmatic Pleural Biopsy.\nINDICATION: The patient is a 76-year-old female with a persistent right-sided exudative effusion of undetermined etiology.\nOPERATIVE FINDINGS: Visual inspection of the right hemithorax demonstrated nonspecific inflammatory changes. There was no evidence of gross nodularity or mass effect. To rule out occult pathology, extensive sampling was performed; twelve (12) biopsies were excised from the parietal pleura, along with diaphragmatic sampling. Mechanical pleurodesis was not indicated or performed. \nCLOSURE: A chestostomy tube was placed following complete fluid evacuation.",
            3: "Service: 32609 (Thoracoscopy; with biopsy of pleura).\nLocation: Right hemithorax.\nProcedure Details:\n- Access: 6th ICS.\n- Visualization: Inflammatory pleura, no masses.\n- Sampling: 12 biopsies obtained from parietal pleura. Diaphragmatic pleura also biopsied.\n- Outcome: Fluid evacuated. Chest tube placed. No pleurodesis agent administered.",
            4: "Resident Note - Thoracoscopy\nPt: Susan Rivera\nSide: Right\nIndication: Recurrent effusion, neg cytology.\n\nSteps:\n1. 6th ICS entry.\n2. Pleuroscope inserted.\n3. Looks inflammatory, no cancer seen.\n4. Took 12 biopsies just to be sure (parietal/diaphragm).\n5. Drained fluid.\n6. Chest tube in.\n\nNo complications. No talc used.",
            5: "Susan Rivera here for the thoracoscopy right side she has that fluid we cant figure out. Sedation was good. Put the scope in at the mid axillary line. Didnt see any tumors just looked red and inflamed. Took a lot of biopsies though 12 of them from the parietal pleura and some from the bottom too. Drained the fluid put the tube in. Did not do talc since it doesnt look malignant. Sending her to the floor.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Cytology-negative exudative effusion. Right side. Under moderate sedation with local anesthesia, single-port entry at 6th intercostal space was achieved. Semi-rigid pleuroscope inserted. Findings included inflammatory changes without nodularity. Multiple biopsies obtained from parietal pleura (12 specimens) and diaphragmatic pleura. All fluid evacuated. Chest tube placed. Hemostasis confirmed. No air leak.",
            7: "[Indication]\nCytology-negative exudative effusion, Right.\n[Anesthesia]\nModerate sedation.\n[Description]\nScope inserted 6th ICS. Findings: Inflammatory, no nodules. Biopsy: 12 parietal specimens + diaphragmatic. Fluid evacuated. Chest tube placed.\n[Plan]\nFloor admission. Chest tube to suction. Path pending.",
            8: "We performed a medical thoracoscopy on Mrs. Rivera to investigate her right pleural effusion. After entering the chest, the pleura looked inflamed but we didn't see any obvious nodules or tumors. To be thorough, we took twelve biopsies from the chest wall and additional samples from the diaphragm. We drained all the fluid and placed a chest tube. We decided against pleurodesis at this time pending the pathology results.",
            9: "Operation: Medical Thoracoscopy with Pleural Sampling\nIndication: Unknown effusion.\nSide: Right\n\nDetails: The pleuroscope was navigated into the space. We observed inflammatory changes but no nodules. We collected 12 specimens from the parietal pleura and additional tissue from the diaphragm. The fluid was extracted. A chest tube was positioned. No air leak detected."
        },
        2: { # Gary Wilson (Right Thoracoscopy, Biopsy, Talc)
            1: "Proc: Right Thoracoscopy, Bx, Talc.\nIndication: Staging lung Ca.\nFindings: Mass on diaphragm.\nAction: 12 parietal biopsies. Diaphragmatic biopsies. Talc poudrage.\nResult: Fluid drained. Tube placed. No leak.\nPlan: Oncology consult.",
            2: "PROCEDURE: Medical Thoracoscopy with Biopsy and Talc Pleurodesis.\nINDICATION: Mr. Wilson presented for pleural staging of known lung carcinoma.\nFINDINGS: Direct visualization revealed a distinct mass lesion located on the diaphragmatic pleura, consistent with metastasis. \nINTERVENTION: Twelve (12) biopsies were taken from the parietal pleura, alongside sampling of the diaphragmatic lesion. Given the confirmed macroscopic involvement, palliative pleurodesis was performed via talc poudrage. The pleural space was evacuated and a chest tube positioned. The patient tolerated the procedure well.",
            3: "Coding: 32609, 32650.\nSite: Right Pleural Space.\nDiagnostic Findings: Diaphragmatic mass.\nProcedures:\n1. Biopsy (32609): 12 samples from parietal pleura + diaphragm.\n2. Pleurodesis (32650): Talc insufflation performed for malignant effusion control.\nFluid Status: Evacuated. Chest tube placed.",
            4: "Procedure: Thoracoscopy (Right)\nStaff: Dr. Martinez\nPt: Gary Wilson\n\n1. Prep/Drape/Sedation.\n2. Port placed 6th ICS.\n3. Saw mass on diaphragm.\n4. Biopsied parietal pleura x12 and the mass.\n5. Talc poudrage done for pleurodesis.\n6. Chest tube placed.\n\nComplications: None.",
            5: "Gary Wilson 68M here for staging. Right side thoracoscopy. Used local and sedation. Went in and saw a mass right on the diaphragm. Took 12 biopsies from the wall and some from the mass itself. Since it looks like spread we did the talc poudrage right then. Drained it all put the tube in. No air leak. He goes to the floor now.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Staging for lung cancer pleural involvement. Right side. Under moderate sedation, the semi-rigid pleuroscope was inserted. A mass lesion was found on the diaphragmatic pleura. Multiple biopsies were obtained from the parietal pleura (12 specimens) and the diaphragmatic pleura. Given findings, talc poudrage was performed. Chest tube placed. Floor admission.",
            7: "[Indication]\nStaging lung cancer, Right side.\n[Anesthesia]\nModerate sedation.\n[Description]\nDiaphragmatic mass visualized. 12 parietal biopsies taken. Diaphragmatic biopsies taken. Talc poudrage performed. Fluid drained.\n[Plan]\nAdmit. Suction. Oncology follow-up.",
            8: "Mr. Wilson underwent a right-sided thoracoscopy for cancer staging. Upon inspection, we identified a mass on the diaphragm. We proceeded to take twelve biopsies from the chest wall and also sampled the mass directly. Because of the likely malignant spread, we performed a talc pleurodesis to prevent the fluid from coming back. We placed a chest tube and confirmed there was no air leak before finishing.",
            9: "Procedure: Medical Thoracoscopy with Pleural Sampling and Talc Poudrage.\nSubject: Gary Wilson.\nFindings: Mass lesion on the diaphragm.\nAction: We harvested 12 specimens from the parietal pleura and sampled the diaphragm. Talc was insufflated for pleurodesis. The fluid was extracted and a tube anchored."
        },
        3: { # Jeffrey Jones (Right Diagnostic Thoracoscopy)
            1: "Proc: Diagnostic Thoracoscopy (Right).\nIndication: Pleural nodularity on imaging.\nFindings: Thickened parietal pleura + nodules.\nAction: Visualization of parietal/visceral/diaphragmatic pleura. Fluid evacuated. Tube placed.\nNote: Diagnostic only (32601).\nPlan: Path pending.",
            2: "OPERATIVE REPORT: DIAGNOSTIC PLEUROSCOPY\n\nINDICATION: Evaluation of radiographic pleural nodularity.\nPROCEDURE: The right pleural space was entered. Systematic inspection revealed thickening of the parietal pleura studded with nodules. The visceral and diaphragmatic surfaces were also visualized. The procedure was limited to diagnostic inspection and fluid evacuation. No biopsy forceps were utilized during this specific sequence (diagnostic code only). A chest tube was placed under direct vision.\n\nIMPRESSION: Pleural nodularity, fluid evacuated.",
            3: "Code: 32601 (Thoracoscopy, diagnostic, without biopsy).\nRationale: Procedure note describes inspection of parietal, visceral, and diaphragmatic pleura. Findings included thickened pleura with nodules. Fluid was evacuated. No tissue samples were documented as harvested in this specific note text, supporting diagnostic code 32601 only.",
            4: "Procedure: Dx Thoracoscopy\nPt: Jeffrey Jones\nSide: Right\n\nSteps:\n1. 6th ICS entry.\n2. Scope in.\n3. Saw thickened pleura and nodules.\n4. Looked at all surfaces.\n5. Drained fluid.\n6. Chest tube in.\n\nDx: Thickened pleura.",
            5: "Jeff Jones right side pleuroscopy. We saw nodules on the scan so we went in to look. Using moderate sedation. Put the scope in. Yeah the parietal pleura is thick and has nodules. We looked at everything drained the fluid and put a chest tube in. Lung expanded fine.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Indication: Pleural nodularity on imaging. Right side. Under moderate sedation, single-port entry was made. Semi-rigid pleuroscope inserted. Findings: Thickened parietal pleura with nodules. Parietal, visceral, and diaphragmatic pleura visualized. All remaining fluid evacuated. Chest tube placed. No air leak. Lung expanded.",
            7: "[Indication]\nPleural nodularity, Right.\n[Anesthesia]\nModerate sedation.\n[Description]\nDiagnostic inspection. Findings: Thickened parietal pleura with nodules. Fluid evacuated. Chest tube placed. Lung expanded.\n[Plan]\nFloor admission. Water seal.",
            8: "Mr. Jones underwent a diagnostic thoracoscopy on the right side to investigate nodules seen on his CT scan. We inserted the scope and confirmed that the parietal pleura was thickened and had nodules. We visualized the entire space, drained the remaining fluid, and placed a chest tube. The lung expanded well.",
            9: "Procedure: Diagnostic Pleuroscopy.\nSide: Right.\nObservations: Thickened parietal pleura with nodules.\nAction: The parietal, visceral, and diaphragmatic pleura were examined. Fluid was purged. A chest tube was positioned. No air leak."
        },
        4: { # Karen Moore (Right Thoracoscopy, Biopsy, Talc)
            1: "Proc: Right Thoracoscopy, Bx, Talc.\nIndication: Suspected TB pleuritis.\nFindings: Inflammatory changes.\nAction: 11 parietal biopsies. Diaphragmatic biopsies. Talc poudrage.\nResult: Fluid drained. Tube placed.\nPlan: Path 5-7 days.",
            2: "PROCEDURE: Medical Thoracoscopy with Biopsy and Pleurodesis.\nINDICATION: 73-year-old female with suspected tuberculous pleuritis.\nFINDINGS: Inspection of the right hemithorax revealed generalized inflammatory changes without distinct nodularity. \nPROCEDURE: To ensure diagnostic adequacy, eleven (11) parietal pleural biopsies were obtained, along with diaphragmatic sampling. Given the clinical context and need for effusion control, sterile talc poudrage was administered. The chest was evacuated and a thoracostomy tube placed. \nDISPOSITION: Inpatient admission.",
            3: "Codes: 32609, 32650.\nLocation: Right.\nTechnique:\n- 11 Biopsies taken from parietal pleura (32609).\n- Diaphragmatic sampling.\n- Talc Poudrage (32650) for pleurodesis.\n- Chest tube placement.\nClinical Context: Suspected TB, inflammatory findings.",
            4: "Procedure: Thoracoscopy/Biopsy/Talc\nPt: Karen Moore\nIndication: TB?\n\nSteps:\n1. Scope in right chest.\n2. Looks inflammatory.\n3. 11 biopsies from wall.\n4. Biopsies from diaphragm.\n5. Talc puffed in.\n6. Fluid out, tube in.\n\nPlan: Monitor suction.",
            5: "Karen Moore here for the right side scope. Thinking it might be TB. Went in with sedation. Pleura just looks angry and inflamed no nodules really. Took 11 biopsies from the parietal side and some from the diaphragm. Did the talc powder just in case to stop the fluid. Drained it put the tube in. She is going to the floor.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Suspected tuberculous pleuritis. Right side. Under moderate sedation, the pleuroscope was inserted. Findings: Inflammatory changes without nodularity. Multiple biopsies obtained from parietal pleura (11 specimens) and diaphragmatic pleura. Talc poudrage performed for pleurodesis. Chest tube placed. Hemostasis confirmed.",
            7: "[Indication]\nSuspected TB pleuritis, Right.\n[Anesthesia]\nModerate sedation.\n[Description]\nInflammatory changes. 11 parietal biopsies + diaphragm. Talc poudrage performed. Fluid evacuated. Tube placed.\n[Plan]\nAdmit. Suction. Await path.",
            8: "We took Mrs. Moore to the suite to check for TB pleuritis. On the right side, the camera showed inflammation but no bumps. We took eleven biopsies from the chest wall and some from the diaphragm to be sure. We then put in talc to seal the space and prevent the fluid from coming back. We left a chest tube in place and she went to the floor.",
            9: "Procedure: Medical Thoracoscopy with Pleural Sampling and Talc Insufflation.\nSide: Right.\nReason: Suspected TB.\nDetails: We observed inflammatory changes. We collected 11 specimens from the parietal pleura. Talc was deposited for pleurodesis. The fluid was extracted and a tube anchored."
        },
        5: { # Timothy Lopez (Left Diagnostic Thoracoscopy)
            1: "Proc: Diagnostic Thoracoscopy (Left).\nIndication: Suspected mesothelioma.\nFindings: Fibrinous adhesions, trapped lung.\nAction: Visualization only. Fluid evacuated. Tube placed.\nNote: Lung trapped.\nPlan: Water seal.",
            2: "OPERATIVE NARRATIVE: DIAGNOSTIC PLEUROSCOPY\n\nINDICATION: Suspected malignant mesothelioma.\nFINDINGS: Examination of the left pleural cavity demonstrated extensive fibrinous adhesions resulting in a trapped lung physiology. \nPROCEDURE: The parietal, visceral, and diaphragmatic surfaces were inspected. Due to the trapped lung and adhesion density, the procedure was limited to fluid evacuation under direct visualization. A chest tube was placed. No air leak was noted despite the trapped lung.\n\nIMPRESSION: Trapped lung, fibrinous adhesions.",
            3: "Code: 32601 (Diagnostic Thoracoscopy).\nSide: Left.\nFindings: Fibrinous adhesions, trapped lung.\nProcedure: Inspection of parietal, visceral, diaphragmatic pleura. Fluid evacuation. \nConstraint: No biopsy or pleurodesis recorded in this note (supports 32601).",
            4: "Procedure: Dx Thoracoscopy\nPt: Timothy Lopez\nSide: Left\n\nSteps:\n1. Entry 6th ICS.\n2. Saw lots of adhesions.\n3. Lung is trapped.\n4. Drained fluid.\n5. Put chest tube in.\n\nNo biopsies mentioned in this note.",
            5: "Tim Lopez left side scope. We think mesothelioma. Went in and it was a mess lots of adhesions and the lung is trapped. We looked around at the pleura drained the fluid and put a tube in. Lung expanded okay but still trapped. No air leak.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Suspected mesothelioma. Left side. Under moderate sedation, the semi-rigid pleuroscope was inserted. Findings: Fibrinous adhesions with trapped lung. Parietal, visceral, and diaphragmatic pleura visualized. All remaining fluid evacuated. Chest tube placed. No air leak. Lung expanded.",
            7: "[Indication]\nSuspected mesothelioma, Left.\n[Anesthesia]\nModerate sedation.\n[Description]\nAdhesions, trapped lung. Diagnostic inspection only. Fluid evacuated. Tube placed.\n[Plan]\nFloor admission. Water seal.",
            8: "Mr. Lopez had a diagnostic thoracoscopy on the left side. We suspected mesothelioma, but when we got in there, we saw a lot of adhesions and it looked like the lung was trapped. We inspected all the pleural surfaces and drained the fluid. We placed a chest tube and confirmed there was no air leak.",
            9: "Procedure: Diagnostic Pleuroscopy.\nSide: Left.\nObservations: Fibrinous adhesions with trapped lung.\nAction: The pleura was examined. Fluid was purged. A chest tube was positioned."
        },
        6: { # Elizabeth Smith (Right Thoracoscopy, Biopsy, Talc)
            1: "Proc: Right Thoracoscopy, Bx, Talc.\nIndication: Persistent effusion.\nFindings: Multiple malignant-appearing nodules.\nAction: 10 parietal biopsies. Diaphragmatic biopsies. Talc poudrage.\nResult: Fluid drained. Tube placed.\nPlan: Oncology consult.",
            2: "PROCEDURE NOTE: Medical Thoracoscopy with Biopsy and Talc Poudrage.\nINDICATION: Ms. Smith presented with a recalcitrant right pleural effusion.\nFINDINGS: Thoracoscopic exploration revealed multiple nodules studding the parietal pleura, highly suggestive of malignancy.\nACTION: Ten (10) biopsies were obtained from the parietal surface, with additional sampling of the diaphragm. Following biopsy, chemical pleurodesis was achieved using sterile talc poudrage. The hemithorax was evacuated of fluid and a chest tube inserted.\nDISPOSITION: Admitted to floor.",
            3: "Coding: 32609, 32650.\nSite: Right.\nFindings: Malignant appearing nodules.\nInterventions:\n- 10 Biopsies (Parietal) + Diaphragmatic sampling (32609).\n- Talc Pleurodesis (32650).\n- Fluid drainage and chest tube placement.",
            4: "Procedure: Thoracoscopy (Right)\nPt: Elizabeth Smith\n\n1. Scope in.\n2. Saw multiple nodules (looks like cancer).\n3. Took 10 biopsies from wall + diaphragm.\n4. Put talc in.\n5. Drained fluid, chest tube in.\n\nStable.",
            5: "Elizabeth Smith right side. Fluid wont go away. We scoped her. Saw a bunch of nodules looks malignant. Took 10 biopsies from the parietal pleura and some from diaphragm. Puffed the talc in for pleurodesis. Drained it put the tube in. She is stable.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Persistent effusion despite thoracentesis. Right side. Under moderate sedation, semi-rigid pleuroscope inserted. Findings: Multiple pleural nodules - malignant appearing. Multiple biopsies obtained from parietal pleura (10 specimens) and diaphragmatic pleura. Talc poudrage performed. All fluid evacuated. Chest tube placed.",
            7: "[Indication]\nPersistent effusion, Right.\n[Anesthesia]\nModerate sedation.\n[Description]\nMalignant-appearing nodules. 10 parietal biopsies + diaphragm. Talc poudrage. Tube placed.\n[Plan]\nAdmit. Oncology consult if malignant.",
            8: "We performed a thoracoscopy on Ms. Smith for her persistent effusion. On the right side, we saw multiple nodules that looked malignant. We took ten biopsies from the chest wall and diaphragm. We then did a talc poudrage to stop the fluid. We placed a chest tube and she went to recovery.",
            9: "Procedure: Medical Thoracoscopy with Pleural Sampling and Talc Poudrage.\nSide: Right.\nFindings: Malignant-appearing nodules.\nAction: We harvested 10 specimens from the parietal pleura. Talc was insufflated. The fluid was extracted and a tube anchored."
        },
        7: { # Kathleen Lee (Left Thoracoscopy, Biopsy, Talc)
            1: "Proc: Left Thoracoscopy, Bx, Talc.\nIndication: Persistent effusion.\nFindings: Visceral pleural tumor implants.\nAction: 11 parietal biopsies. Diaphragmatic biopsies. Talc poudrage.\nResult: Fluid drained. Tube placed.\nPlan: Path pending.",
            2: "PROCEDURE: Medical Thoracoscopy.\nINDICATION: 55-year-old female, persistent left effusion.\nFINDINGS: Visualization revealed tumor implants along the visceral pleura.\nPROCEDURE: Eleven (11) parietal pleural biopsies were taken to minimize risk of visceral injury, along with diaphragmatic sampling. Talc poudrage was insufflated for pleurodesis. Complete fluid evacuation was followed by chest tube placement.\nIMPRESSION: Visceral pleural malignancy, pleurodesis performed.",
            3: "Codes: 32609, 32650.\nSide: Left.\nFindings: Visceral implants.\nTechnique: \n- Biopsy x11 (Parietal) + Diaphragm.\n- Talc Poudrage.\n- Drainage and Tube placement.",
            4: "Procedure: Thoracoscopy Left\nPt: Kathleen Lee\n\n1. Entry 6th ICS.\n2. Saw tumor on the lung (visceral pleura).\n3. Biopsied the wall (11x) and diaphragm instead of the lung to be safe.\n4. Talc poudrage.\n5. Chest tube in.\n\nNo air leak.",
            5: "Kathleen Lee left side effusion. Scoped her. Saw tumor implants on the visceral pleura. Took 11 biopsies from the parietal wall and diaphragm. Did the talc poudrage. Drained the fluid put the tube in. No air leak.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Persistent effusion. Left side. Semi-rigid pleuroscope inserted. Findings: Visceral pleural tumor implants. Multiple biopsies obtained from parietal pleura (11 specimens) and diaphragmatic pleura. Talc poudrage performed for pleurodesis. All fluid evacuated. Chest tube placed.",
            7: "[Indication]\nPersistent effusion, Left.\n[Anesthesia]\nModerate sedation.\n[Description]\nVisceral tumor implants. 11 parietal biopsies. Talc poudrage. Tube placed.\n[Plan]\nAdmit. Suction.",
            8: "Ms. Lee had a left thoracoscopy for her effusion. We saw tumor implants right on the lung surface. We biopsied the chest wall (11 samples) and diaphragm. We performed talc pleurodesis, drained the fluid, and placed a chest tube.",
            9: "Procedure: Medical Thoracoscopy with Pleural Sampling and Talc Poudrage.\nSide: Left.\nFindings: Visceral tumor implants.\nAction: We harvested 11 specimens from the parietal pleura. Talc was deposited. The fluid was extracted and a tube anchored."
        },
        8: { # William Lee (Left Thoracoscopy, Biopsy, No Talc)
            1: "Proc: Left Thoracoscopy, Bx.\nIndication: Biopsy-negative suspected malignancy.\nFindings: Inflammatory changes, no nodules.\nAction: 12 parietal biopsies. Diaphragmatic biopsies. Fluid drained. Tube placed.\nNote: No talc.\nPlan: Admit.",
            2: "PROCEDURE: Medical Thoracoscopy with Biopsy.\nINDICATION: Mr. Lee presented with suspected malignancy despite prior negative workup.\nFINDINGS: The left pleural space demonstrated inflammatory changes; no discrete nodularity was identified.\nINTERVENTION: To maximize diagnostic yield, twelve (12) parietal biopsies and additional diaphragmatic samples were obtained. Fluid was fully evacuated and a chest tube inserted. Pleurodesis was deferred.\nDISPOSITION: Floor admission.",
            3: "Code: 32609.\nSide: Left.\nFindings: Inflammatory.\nTechnique: 12 Biopsies (Parietal) + Diaphragm.\nNote: No pleurodesis performed (excludes 32650).\nFluid drained, tube placed.",
            4: "Procedure: Thoracoscopy Left\nPt: William Lee\n\n1. Scope in.\n2. Looks inflammatory, no cancer seen.\n3. Took 12 biopsies from wall and diaphragm to be sure.\n4. Drained fluid.\n5. Chest tube in.\n\nNo talc.",
            5: "William Lee left side scope. He has suspected cancer but biopsies negative so far. Went in and it just looked inflamed no nodules. Took 12 biopsies from the wall and some from the diaphragm. Drained it put the tube in. Didnt do talc.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Indication: Biopsy-negative suspected malignancy. Left side. Findings: Inflammatory changes without nodularity. Multiple biopsies obtained from parietal pleura (12 specimens) and diaphragmatic pleura. All fluid evacuated. Chest tube placed. No air leak.",
            7: "[Indication]\nSuspected malignancy, Left.\n[Anesthesia]\nModerate sedation.\n[Description]\nInflammatory changes. 12 parietal biopsies + diaphragm. Fluid evacuated. Tube placed. No talc.\n[Plan]\nAdmit.",
            8: "We performed a left thoracoscopy on Mr. Lee. Despite the suspicion of cancer, the pleura just looked inflamed. We took twelve biopsies from the parietal pleura and more from the diaphragm to try and get a diagnosis. We drained the fluid and placed a chest tube, but did not perform pleurodesis.",
            9: "Procedure: Medical Thoracoscopy with Pleural Sampling.\nSide: Left.\nFindings: Inflammatory changes.\nAction: We harvested 12 specimens from the parietal pleura. The fluid was extracted and a tube anchored."
        },
        9: { # Matthew Young (Right Diagnostic Thoracoscopy + Talc, no biopsy mention in text implies 32650 primary?)
             # Wait, original text says "Medical Thoracoscopy (Pleuroscopy) - Diagnostic... Talc poudrage performed...".
             # Registry says CPT 32650.
            1: "Proc: Right Thoracoscopy, Talc.\nIndication: Suspected malignancy.\nFindings: Inflammatory changes.\nAction: Visualized pleura. Talc poudrage performed. Fluid evacuated. Tube placed.\nNote: No biopsies mentioned.\nPlan: Water seal.",
            2: "PROCEDURE: Medical Thoracoscopy with Talc Pleurodesis.\nINDICATION: Mr. Young, 60M, suspected malignant pleural disease.\nFINDINGS: Diffuse inflammatory changes without gross nodularity on the parietal, visceral, or diaphragmatic surfaces.\nINTERVENTION: Sterile talc poudrage was insufflated to achieve pleurodesis. The pleural space was evacuated of fluid and a chest tube placed under direct visualization. \nIMPRESSION: Inflammatory pleura, pleurodesis completed.",
            3: "Code: 32650 (Thoracoscopy with pleurodesis).\nSide: Right.\nFindings: Inflammatory changes.\nProcedure: \n- Visualization of pleura.\n- Talc Poudrage (32650).\n- Fluid evacuation.\n- Chest tube placement.\nNote: No biopsy performed/coded.",
            4: "Procedure: Thoracoscopy w/ Talc\nPt: Matthew Young\nSide: Right\n\n1. Scope in.\n2. Inflammatory changes only.\n3. Did talc poudrage for the fluid.\n4. Drained fluid.\n5. Chest tube in.\n\nNo biopsies.",
            5: "Matt Young right side. Suspect cancer. Went in with the scope. Just looked inflamed no nodules. Decided to do talc poudrage to stop the fluid coming back. Drained it all and put the tube in. No biopsies just talc.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic with Pleurodesis. Suspected malignant pleural disease. Right side. Findings: Inflammatory changes without nodularity. Parietal, visceral, and diaphragmatic pleura visualized. Talc poudrage performed for pleurodesis after drainage. All remaining fluid evacuated. Chest tube placed.",
            7: "[Indication]\nSuspected malignancy, Right.\n[Anesthesia]\nModerate sedation.\n[Description]\nInflammatory changes. Talc poudrage performed. Fluid evacuated. Tube placed.\n[Plan]\nAdmit.",
            8: "Mr. Young had a right thoracoscopy. The pleura looked inflamed but had no nodules. We decided to proceed with talc poudrage to treat the effusion. We drained the fluid and placed a chest tube.",
            9: "Procedure: Medical Thoracoscopy with Talc Insufflation.\nSide: Right.\nFindings: Inflammatory changes.\nAction: The pleura was examined. Talc was deposited. The fluid was extracted and a tube anchored."
        }
    }
    return variations

def get_base_data_mocks():
    # Mapping original patients to 9 mock names each.
    return [
        {"idx": 0, "orig_name": "John Taylor", "orig_age": 82, "names": ["Robert Smith", "James Johnson", "William Brown", "David Jones", "Richard Miller", "Joseph Davis", "Thomas Garcia", "Charles Rodriguez", "Daniel Wilson"]},
        {"idx": 1, "orig_name": "Susan Rivera", "orig_age": 76, "names": ["Mary Martinez", "Patricia Anderson", "Linda Taylor", "Barbara Thomas", "Elizabeth Hernandez", "Jennifer Moore", "Maria Martin", "Susan Jackson", "Margaret Thompson"]},
        {"idx": 2, "orig_name": "Gary Wilson", "orig_age": 68, "names": ["Christopher White", "Matthew Lopez", "Anthony Lee", "Mark Gonzalez", "Donald Harris", "Steven Clark", "Paul Lewis", "Andrew Robinson", "Kenneth Walker"]},
        {"idx": 3, "orig_name": "Jeffrey Jones", "orig_age": 71, "names": ["George Perez", "Joshua Hall", "Kevin Young", "Brian Allen", "Edward Sanchez", "Ronald Wright", "Timothy King", "Jason Scott", "Jeffrey Green"]},
        {"idx": 4, "orig_name": "Karen Moore", "orig_age": 73, "names": ["Dorothy Baker", "Lisa Adams", "Nancy Nelson", "Karen Hill", "Betty Ramirez", "Helen Campbell", "Sandra Mitchell", "Donna Roberts", "Carol Carter"]},
        {"idx": 5, "orig_name": "Timothy Lopez", "orig_age": 67, "names": ["Frank Phillips", "Scott Evans", "Eric Turner", "Stephen Torres", "Larry Parker", "Justin Collins", "Brandon Edwards", "Gregory Stewart", "Samuel Flores"]},
        {"idx": 6, "orig_name": "Elizabeth Smith", "orig_age": 64, "names": ["Ruth Morris", "Sharon Nguyen", "Michelle Murphy", "Laura Rivera", "Sarah Cook", "Kimberly Rogers", "Deborah Morgan", "Jessica Peterson", "Shirley Cooper"]},
        {"idx": 7, "orig_name": "Kathleen Lee", "orig_age": 55, "names": ["Cynthia Reed", "Angela Bailey", "Melissa Bell", "Brenda Gomez", "Amy Kelly", "Anna Howard", "Rebecca Ward", "Virginia Cox", "Kathleen Diaz"]},
        {"idx": 8, "orig_name": "William Lee", "orig_age": 58, "names": ["Raymond Richardson", "Gregory Wood", "Dennis Watson", "Jerry Brooks", "Tyler Bennett", "Aaron Gray", "Henry James", "Douglas Reyes", "Peter Cruz"]},
        {"idx": 9, "orig_name": "Matthew Young", "orig_age": 60, "names": ["Jose Hughes", "Adam Price", "Nathan Myers", "Zachary Long", "Walter Foster", "Harold Sanders", "Kyle Ross", "Carl Morales", "Arthur Powell"]}
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
    output_filename = output_dir / "synthetic_thoracoscopy_notes_part_056.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()