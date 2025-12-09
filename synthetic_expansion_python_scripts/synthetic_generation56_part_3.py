import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_056_part3.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations for the thoracoscopy dataset.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Jennifer Allen (Diagnostic, Left, Normal, 32601)
            1: "Indication: Suspected mesothelioma.\nProcedure: Left diagnostic thoracoscopy.\nFindings: Pleura normal. No nodules.\nAction: Fluid evacuated. 24Fr chest tube placed.\nPlan: Admit. Water seal.",
            2: "HISTORY: Ms. Allen presented with a left-sided pleural effusion concerning for mesothelioma. She underwent diagnostic intervention today.\nOPERATIVE NARRATIVE: The patient was brought to the endoscopy suite. Under moderate sedation and local anesthesia, a trocar was introduced into the left 6th intercostal space. A semi-rigid pleuroscope was utilized to inspect the hemithorax. The parietal and visceral surfaces were unremarkable, with no evidence of gross malignancy. Following complete evacuation of the effusion, a chest tube was secured.\nIMPRESSION: Normal left pleural space evaluation.",
            3: "CPT Code: 32601 (Thoracoscopy, diagnostic).\nTechnique: Access via 6th ICS/mid-axillary line using single-port technique.\nVisualization: Inspection of parietal, visceral, and diaphragmatic pleura utilizing semi-rigid pleuroscope.\nFindings: No biopsy performed as pleura appeared normal.\nClosure: Chest tube placement for drainage.",
            4: "Resident Note\nPatient: Jennifer Allen\nAttending: Dr. Garcia\nProcedure: Left Medical Thoracoscopy\nSteps:\n1. Time out.\n2. Local + Moderate sedation.\n3. Trocar placement 6th ICS.\n4. Scope insertion.\n5. Inspection: Normal pleura.\n6. Chest tube placed.\nNo complications.",
            5: "patient jennifer allen here for left thoracoscopy due to possible mesothelioma we did the procedure today under sedation entered at the 6th intercostal space looked around with the scope everything looked normal actually no bumps or masses drained the fluid put a tube in shes going to the floor now thanks dr garcia",
            6: "The patient, Jennifer Allen, underwent a diagnostic medical thoracoscopy on the left side today due to suspected mesothelioma. The procedure was performed under moderate sedation. We entered through the 6th intercostal space. Upon visualization with the semi-rigid pleuroscope, the parietal, visceral, and diaphragmatic pleura all appeared normal. We evacuated the remaining fluid. A chest tube was placed and the patient was transferred to the floor. No air leak was noted.",
            7: "[Indication]\nSuspected mesothelioma, left side.\n[Anesthesia]\nModerate sedation with local lidocaine.\n[Description]\nLeft medical thoracoscopy performed. Single port entry. Pleura inspected and found to be normal. Fluid drained. Chest tube placed.\n[Plan]\nAdmit to floor. Remove tube when output <150mL/day.",
            8: "Under moderate sedation, a diagnostic medical thoracoscopy was performed on the left side for Ms. Allen. We accessed the pleural space via the 6th intercostal space. The semi-rigid pleuroscope was introduced, allowing for a thorough inspection of the parietal, visceral, and diaphragmatic pleura. The findings were reassuring, as the pleura appeared entirely normal. We evacuated all remaining fluid and placed a chest tube to water seal before transferring the patient to the floor.",
            9: "Indication: Query mesothelioma.\nSide: Left.\nMethod: Diagnostic pleuroscopy.\nDetails: Administered sedation. Accessed 6th intercostal space. Inserted semi-rigid scope. Surveyed pleural cavity. Observed normal parietal and visceral surfaces. Drained effusion. Installed chest drainage catheter. No air leak detected."
        },
        1: { # Sharon Lee (Biopsy+Talc, Left, Tumor, 32609, 32650)
            1: "Dx: Lung CA staging.\nProc: L Thoracoscopy w/ bx and talc.\nFindings: Visceral implants.\nActions: 11 biopsies taken. Talc poudrage performed.\nResult: Fluid drained. Tube placed to suction.",
            2: "OPERATIVE REPORT: Ms. Lee underwent left medical thoracoscopy for staging of suspected pleural carcinomatosis. Inspection revealed definitive tumor implants studding the visceral pleura. Eleven biopsies were harvested from the parietal surface for histopathological confirmation. Given the gross malignant appearance, chemical pleurodesis was achieved via talc poudrage insufflation. The hemithorax was evacuated, and a thoracostomy tube was positioned.",
            3: "Codes Submitted:\n- 32609: Thoracoscopy with biopsy (11 specimens taken from parietal pleura).\n- 32650: Thoracoscopy with pleurodesis (Talc poudrage performed for malignant effusion).\nMedical Necessity: Staging lung cancer with pleural involvement.",
            4: "Procedure Note\nPt: Sharon Lee\nStaff: Dr. Thompson\nOp: Left Med Thoracoscopy + Biopsy + Talc\nSteps:\n1. 6th ICS entry.\n2. Scope in.\n3. Found tumor implants.\n4. Biopsied x11.\n5. Insufflated Talc.\n6. Chest tube placed.\nPlan: Admit, suction.",
            5: "sharon lee procedure note we did a left thoracoscopy for staging lung cancer today sedation used entered 6th ics saw a lot of tumor implants on the visceral pleura so we took about 11 biopsies from the parietal side then we did the talc poudrage for pleurodesis drained it all put a chest tube in no air leak sending her to the floor",
            6: "Left medical thoracoscopy performed for staging lung cancer pleural involvement. Under moderate sedation, the semi-rigid pleuroscope was inserted at the 6th intercostal space. Inspection revealed visceral pleural tumor implants. Multiple biopsies (11) were obtained from the parietal and diaphragmatic pleura. Talc poudrage was performed for pleurodesis. All fluid was evacuated and a chest tube was placed. Hemostasis was confirmed.",
            7: "[Indication]\nStaging for lung cancer pleural involvement, left side.\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft thoracoscopy revealed visceral tumor implants. 11 biopsies obtained. Talc poudrage performed for pleurodesis. Fluid drained. Chest tube placed.\n[Plan]\nAdmit to floor. Suction. Oncology consult pending path.",
            8: "We performed a left medical thoracoscopy on Ms. Lee for staging purposes. Upon entering the pleural space, we immediately visualized tumor implants on the visceral pleura. To confirm the diagnosis, we obtained eleven biopsies from the parietal pleura. Given the malignant findings, we proceeded with talc poudrage to achieve pleurodesis. The procedure concluded with the evacuation of fluid and the placement of a chest tube.",
            9: "Indication: Staging malignancy.\nProcedure: Pleuroscopy with sampling and sclerosis.\nFindings: Malignant deposits on visceral surface.\nAction: Harvested 11 tissue samples. Administered Talc for adhesion. Emptying of effusion completed. Catheter installed. Hemostasis verified."
        },
        2: { # Angela Green (Biopsy+Talc, Right, Tumor, 32609, 32650)
            1: "Indication: Persistent effusion.\nProc: R Thoracoscopy, Bx, Talc.\nFindings: Visceral implants.\nAction: 8 parietal biopsies. Talc insufflated.\nPlan: Admit. Chest tube to suction.",
            2: "CLINICAL SUMMARY: Ms. Green presented with a recalcitrant right pleural effusion. Thoracoscopic interrogation demonstrated visceral pleural metastases. Extensive sampling was performed, yielding eight parietal specimens. To prevent recurrence, palliative pleurodesis was executed utilizing sterile talc poudrage. The patient tolerated the procedure well and was transferred for post-operative monitoring.",
            3: "Billing Justification:\n32609: Medical thoracoscopy with biopsy of pleura (8 samples obtained).\n32650: Medical thoracoscopy with pleurodesis (Talc agent used).\nSite: Right hemithorax.\nDiagnosis: Malignant pleural effusion (suspected).",
            4: "Resident Procedure Note\nPatient: Angela Green\nAttending: Dr. Miller\nSide: Right\nProcedure: Thoracoscopy w/ biopsy & talc\nSequence:\n- Port placement 6th ICS.\n- Visualization: Visceral implants.\n- Biopsy: 8 parietal samples.\n- Pleurodesis: Talc.\n- Closure: 24Fr Chest tube.\nComplications: None.",
            5: "angela green procedure note right side thoracoscopy persistent effusion we went in with the scope saw tumor implants on the visceral pleura took 8 biopsies from parietal pleura sent to path then we did talc poudrage to stop the fluid coming back drained everything chest tube in looks good miller md",
            6: "Right medical thoracoscopy performed for persistent effusion. Under moderate sedation, the pleural space was accessed. Findings included visceral pleural tumor implants. Eight biopsies were taken from the parietal pleura. Talc poudrage was performed for pleurodesis. The chest tube was placed after fluid evacuation. The patient was admitted to the floor.",
            7: "[Indication]\nPersistent right pleural effusion.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight thoracoscopy showed visceral implants. 8 biopsies taken. Talc poudrage performed. Fluid evacuated. Chest tube placed.\n[Plan]\nAdmit. Suction. Path pending.",
            8: "Ms. Green underwent a right-sided medical thoracoscopy due to a persistent effusion. During the procedure, we identified tumor implants on the visceral pleura. We collected eight biopsies from the parietal pleura for analysis. To manage the effusion, we performed a talc poudrage pleurodesis. The fluid was fully drained, and a chest tube was inserted before the patient was taken to the recovery area.",
            9: "Indication: Recurrent hydrothorax.\nProcedure: Right pleuroscopy with tissue sampling and pleurodesis.\nFindings: Metastatic deposits visualized.\nAction: Collected 8 specimens. Applied Talc. Drained cavity. Positioned drainage tube. Patient stable."
        },
        3: { # Kevin Allen (Diagnostic/Talc, Left, Nodules, 32650)
            1: "Dx: Exudative effusion.\nProc: L Thoracoscopy + Talc.\nFindings: Diffuse nodules.\nAction: Nodules seen. Talc poudrage performed. Tube placed.\nPlan: Water seal. D/C tube <150ml.",
            2: "PROCEDURE REPORT: Mr. Allen underwent diagnostic left thoracoscopy for evaluation of an undiagnosed exudative effusion. Inspection revealed diffuse pleural nodularity throughout the hemithorax. Following drainage, chemical pleurodesis was achieved via talc poudrage to prevent re-accumulation. A thoracostomy tube was placed under direct visualization to facilitate lung re-expansion.",
            3: "CPT 32650: Thoracoscopy with pleurodesis (Talc).\nNote: Diagnostic inspection performed (nodularity found), followed by therapeutic talc application. CPT 32601 is bundled into 32650. No separate biopsy code billed (visual diagnosis/fluid cytology context).",
            4: "Trainee Note\nPt: Kevin Allen\nAttending: Dr. Davis\nProc: L Thoracoscopy + Talc\nSteps:\n1. 6th ICS access.\n2. Scope: Diffuse nodules.\n3. Fluid drained.\n4. Talc poudrage performed.\n5. Chest tube placed.\nStable.",
            5: "kevin allen 54m here for left thoracoscopy exudative effusion we looked in and saw nodules everywhere diffuse nodularity did the talc poudrage for him drained the fluid chest tube is in water seal davis md",
            6: "Left medical thoracoscopy performed for undiagnosed exudative effusion. Access at 6th intercostal space. Findings included diffuse pleural nodularity. Talc poudrage was performed for pleurodesis. All fluid was evacuated. A chest tube was placed. Lung expanded well.",
            7: "[Indication]\nUndiagnosed exudative left pleural effusion.\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft thoracoscopy revealed diffuse nodularity. Talc poudrage performed. Fluid drained. Chest tube placed.\n[Plan]\nAdmit. Water seal.",
            8: "For Mr. Allen's undiagnosed left pleural effusion, we performed a medical thoracoscopy. The inspection revealed diffuse nodularity across the pleural surface. We decided to proceed with talc poudrage for pleurodesis. After ensuring all fluid was drained and the lung was expanded, we placed a chest tube and admitted him to the floor.",
            9: "Indication: Unknown effusion.\nProcedure: Left pleuroscopy with sclerosis.\nFindings: Widespread nodules.\nAction: Insufflated Talc. Emptying of fluid. Catheter inserted. Lung re-expanded."
        },
        4: { # Patricia Taylor (Biopsy, Left, Tumor, No Talc, 32609)
            1: "Indication: Susp. malignancy.\nProc: L Thoracoscopy w/ Bx.\nFindings: Visceral implants.\nAction: 6 parietal biopsies. No talc. Tube placed.\nPlan: Path pending.",
            2: "OPERATIVE NOTE: Ms. Taylor underwent left medical thoracoscopy for investigation of a biopsy-negative suspected malignancy. Intraoperative evaluation demonstrated tumor implants along the visceral pleura. Six biopsies were carefully harvested from the parietal pleura for histologic analysis. Hemostasis was secured, fluid evacuated, and a chest tube placed. No chemical pleurodesis was performed.",
            3: "Code: 32609 (Thoracoscopy with biopsy).\nTechnique: Semi-rigid pleuroscope, Left side.\nSamples: 6 specimens from parietal pleura.\nNote: No pleurodesis (32650) performed during this session.",
            4: "Resident Note\nPt: Patricia Taylor\nStaff: Dr. Thompson\nProc: L Med Thoracoscopy + Bx\nSteps:\n1. Access 6th ICS.\n2. Visualized visceral implants.\n3. 6 Biopsies taken (parietal).\n4. Fluid drained.\n5. Chest tube placed.\nNo complications.",
            5: "patricia taylor procedure note left side thoracoscopy suspected cancer biopsy negative before so we went in saw visceral implants took 6 biopsies from the parietal wall sent to path fluid out chest tube in no air leak thanks",
            6: "Left medical thoracoscopy with pleural biopsy. Indication: Suspected malignancy. Findings: Visceral pleural tumor implants. Six biopsies were obtained from the parietal pleura. All fluid was evacuated. A chest tube was placed. Hemostasis was confirmed. No air leak.",
            7: "[Indication]\nSuspected malignancy, biopsy negative.\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft thoracoscopy performed. Visceral implants seen. 6 biopsies taken from parietal pleura. Fluid drained. Chest tube placed.\n[Plan]\nAdmit. Suction. Oncology f/u.",
            8: "We performed a left medical thoracoscopy on Ms. Taylor to investigate a suspected malignancy. The visualization revealed tumor implants on the visceral pleura. We successfully obtained six biopsies from the parietal pleura. The fluid was drained, and a chest tube was placed. We did not perform pleurodesis at this time.",
            9: "Indication: Occult malignancy.\nProcedure: Left pleuroscopy with tissue sampling.\nFindings: Tumor deposits.\nAction: Harvested 6 samples. Evacuated effusion. Installed drainage catheter. No sclerosis."
        },
        5: { # Brian Allen (Biopsy+Talc, Right, Inflammatory, 32609, 32650)
            1: "Indication: Lung CA staging.\nProc: R Thoracoscopy, Bx, Talc.\nFindings: Inflammatory changes. No nodules.\nAction: 6 biopsies. Talc poudrage. Tube placed.\nPlan: Admit.",
            2: "PROCEDURE RECORD: Mr. Allen underwent right medical thoracoscopy for lung cancer staging. Visual inspection of the pleural space revealed inflammatory changes but lacked gross nodularity. To rule out microscopic disease, six parietal biopsies were obtained. Given the clinical context, talc poudrage was administered for pleurodesis. The procedure concluded with tube thoracostomy.",
            3: "CPT 32609: Biopsy of pleura (6 samples).\nCPT 32650: Pleurodesis via Talc poudrage.\nRationale: Staging procedure with tissue sampling and preventive pleurodesis for effusion management.",
            4: "Trainee Procedure Note\nPt: Brian Allen\nAttending: Dr. Park\nSide: Right\nProc: Thoracoscopy + Bx + Talc\n- 6th ICS entry.\n- Findings: Inflammatory, no nodules.\n- Bx: x6 parietal.\n- Talc Poudrage done.\n- Chest tube placed.",
            5: "brian allen right thoracoscopy for staging lung cancer park md attending we went in looked inflammatory no big nodules or anything took 6 biopsies just in case then did the talc poudrage drained it chest tube in suction patient fine",
            6: "Right medical thoracoscopy with pleural biopsy and pleurodesis. Indication: Staging. Findings: Inflammatory changes, no nodularity. Six biopsies obtained from parietal pleura. Talc poudrage performed. Chest tube placed after fluid evacuation. Hemostasis confirmed.",
            7: "[Indication]\nLung cancer staging, right pleural effusion.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight thoracoscopy showed inflammation. 6 biopsies taken. Talc poudrage performed. Chest tube placed.\n[Plan]\nAdmit. Suction.",
            8: "Mr. Allen underwent a right medical thoracoscopy for cancer staging. Upon inspection, we noted inflammatory changes but no distinct nodules. We took six biopsies from the parietal pleura to be thorough. Following the biopsies, we performed talc poudrage for pleurodesis. The fluid was drained and a chest tube was inserted.",
            9: "Indication: Staging.\nProcedure: Right pleuroscopy with sampling and sclerosis.\nFindings: Inflammation.\nAction: Collected 6 specimens. Administered Talc. Drained fluid. Installed catheter."
        },
        6: { # Betty Jackson (Biopsy+Talc, Left, Mass, 32609, 32650)
            1: "Indication: Pleural nodularity.\nProc: L Thoracoscopy, Bx, Talc.\nFindings: Diaphragmatic mass.\nAction: 6 parietal biopsies. Talc poudrage. Tube placed.\nPlan: Path pending.",
            2: "OPERATIVE REPORT: Ms. Jackson underwent left medical thoracoscopy due to imaging findings of nodularity. Intraoperatively, a mass lesion was visualized on the diaphragmatic pleura. Six biopsies were obtained from the parietal pleura for characterization. Following sampling, talc poudrage was insufflated to achieve pleurodesis. A chest tube was placed following evacuation of the hemithorax.",
            3: "Billing: 32609 (Biopsy x6), 32650 (Talc Pleurodesis).\nTarget: Left Pleura.\nFindings: Mass on diaphragm.\nDevice: Semi-rigid pleuroscope.\nOutcome: Successful sampling and sclerosis.",
            4: "Resident Note\nPt: Betty Jackson\nStaff: Dr. Chen\nProc: L Med Thoracoscopy\nSteps:\n1. Entry 6th ICS.\n2. Found mass on diaphragm.\n3. 6 Biopsies (parietal).\n4. Talc Poudrage.\n5. Chest tube.\nNo air leak.",
            5: "betty jackson procedure left thoracoscopy nodularity on ct we went in saw a mass on the diaphragm took 6 biopsies from the wall side parietal pleura did talc poudrage too drained the fluid chest tube in suction chen md",
            6: "Left medical thoracoscopy with biopsy and pleurodesis. Indication: Pleural nodularity. Findings: Mass lesion on diaphragmatic pleura. Six biopsies taken from parietal pleura. Talc poudrage performed. Fluid evacuated. Chest tube placed. No air leak.",
            7: "[Indication]\nPleural nodularity, left side.\n[Anesthesia]\nModerate sedation.\n[Description]\nLeft thoracoscopy revealed diaphragmatic mass. 6 parietal biopsies taken. Talc poudrage performed. Chest tube placed.\n[Plan]\nAdmit. Suction.",
            8: "Ms. Jackson had a left medical thoracoscopy to investigate pleural nodularity. We identified a mass lesion on the diaphragmatic pleura. We proceeded to take six biopsies from the parietal pleura. After the biopsies, we performed talc poudrage for pleurodesis. We drained the fluid and placed a chest tube.",
            9: "Indication: Nodularity.\nProcedure: Left pleuroscopy with sampling and sclerosis.\nFindings: Diaphragmatic mass.\nAction: Harvested 6 samples. Administered Talc. Emptying of fluid. Catheter inserted."
        },
        7: { # Kathleen Carter (Diagnostic, Right, Normal, 32601)
            1: "Indication: Undiagnosed effusion.\nProc: R Diagnostic Thoracoscopy.\nFindings: Normal pleura.\nAction: Fluid evacuated. Tube placed.\nPlan: Water seal.",
            2: "PROCEDURE NOTE: Ms. Carter underwent right diagnostic medical thoracoscopy for an undiagnosed exudative effusion. Systematic inspection of the hemithorax revealed normal-appearing parietal, visceral, and diaphragmatic pleura surfaces. No biopsies were indicated. The effusion was fully evacuated, and a chest tube was placed to water seal.",
            3: "Code: 32601 (Diagnostic Thoracoscopy).\nSide: Right.\nFindings: Normal pleura.\nAction: Visualization and drainage only. No biopsy (32609) or pleurodesis (32650) performed.",
            4: "Resident Note\nPt: Kathleen Carter\nAttending: Dr. Kim\nProc: R Diagnostic Thoracoscopy\nSteps:\n1. 6th ICS entry.\n2. Scope: Normal pleura.\n3. Fluid drained.\n4. Chest tube placed.\nNo complications.",
            5: "kathleen carter right side thoracoscopy undiagnosed effusion we looked in everything looks normal no cancer seen drained the fluid put the tube in water seal kim md",
            6: "Right diagnostic medical thoracoscopy. Indication: Undiagnosed effusion. Findings: Normal-appearing pleura. No nodules or masses. All fluid evacuated. Chest tube placed. No air leak.",
            7: "[Indication]\nUndiagnosed right pleural effusion.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight thoracoscopy performed. Pleura appeared normal. Fluid drained. Chest tube placed.\n[Plan]\nAdmit. Water seal.",
            8: "We performed a right diagnostic thoracoscopy on Ms. Carter to evaluate her effusion. The inspection showed that the parietal, visceral, and diaphragmatic pleura all appeared normal. We drained the fluid completely and placed a chest tube. No biopsies were necessary.",
            9: "Indication: Unknown effusion.\nProcedure: Right diagnostic pleuroscopy.\nFindings: Normal surfaces.\nAction: Evacuated fluid. Installed catheter. No sampling."
        },
        8: { # David Garcia (Biopsy, Right, Mass, No Talc, 32609)
            1: "Indication: Pleural nodularity.\nProc: R Thoracoscopy w/ Bx.\nFindings: Diaphragmatic mass.\nAction: 11 parietal biopsies. No talc. Tube placed.\nPlan: Path pending.",
            2: "OPERATIVE NARRATIVE: Mr. Garcia underwent right medical thoracoscopy for investigation of pleural nodularity. The procedure revealed a mass lesion situated on the diaphragmatic pleura. Eleven biopsies were obtained from the parietal pleura to ensure adequate sampling. Following fluid evacuation, a chest tube was placed. Pleurodesis was deferred pending pathologic diagnosis.",
            3: "CPT 32609: Medical thoracoscopy with biopsy.\nDetails: 11 specimens obtained from parietal pleura.\nPathology: Mass on diaphragm.\nExclusions: No pleurodesis (32650) performed.",
            4: "Resident Note\nPt: David Garcia\nStaff: Dr. Brown\nProc: R Med Thoracoscopy + Bx\nSteps:\n1. 6th ICS entry.\n2. Mass seen on diaphragm.\n3. 11 Biopsies (parietal).\n4. Fluid drained.\n5. Chest tube placed.\nNo talc used.",
            5: "david garcia procedure note right thoracoscopy nodularity on imaging we saw a mass on the diaphragm took 11 biopsies from the parietal pleura didnt do talc just drained it and put the tube in brown md",
            6: "Right medical thoracoscopy with biopsy. Indication: Pleural nodularity. Findings: Mass lesion on diaphragmatic pleura. Eleven biopsies were obtained from the parietal pleura. All fluid was evacuated. Chest tube placed. Hemostasis confirmed.",
            7: "[Indication]\nRight pleural nodularity.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight thoracoscopy revealed diaphragmatic mass. 11 parietal biopsies taken. Fluid drained. Chest tube placed.\n[Plan]\nAdmit. Suction. Path pending.",
            8: "Mr. Garcia underwent a right medical thoracoscopy to investigate findings of pleural nodularity. We discovered a mass lesion on the diaphragmatic pleura. To characterize it, we took eleven biopsies from the parietal pleura. We drained the fluid and placed a chest tube, but decided against pleurodesis at this time.",
            9: "Indication: Nodularity.\nProcedure: Right pleuroscopy with sampling.\nFindings: Diaphragmatic mass.\nAction: Harvested 11 samples. Evacuated effusion. Installed catheter. No sclerosis."
        },
        9: { # William Johnson (Biopsy+Talc, Right, Nodules, 32609, 32650)
            1: "Indication: Susp. malignancy.\nProc: R Thoracoscopy, Bx, Talc.\nFindings: Thickened pleura, nodules.\nAction: 12 parietal biopsies. Talc poudrage. Tube placed.\nPlan: Admit.",
            2: "PROCEDURE REPORT: Mr. Johnson underwent right medical thoracoscopy for suspected malignancy. Inspection revealed thickened parietal pleura studded with nodules. Twelve biopsies were obtained from the parietal surface. Given the findings, palliative pleurodesis was performed via talc poudrage. The hemithorax was drained and a chest tube was secured.",
            3: "Billing Codes:\n- 32609: Thoracoscopy with biopsy (12 samples).\n- 32650: Thoracoscopy with pleurodesis (Talc).\nFindings: Malignant appearing nodules/thickening.\nSite: Right hemithorax.",
            4: "Trainee Note\nPt: William Johnson\nAttending: Dr. Wilson\nProc: R Thoracoscopy + Bx + Talc\n- Entry 6th ICS.\n- Findings: Thickened pleura w/ nodules.\n- Bx: 12 samples parietal.\n- Talc: Poudrage done.\n- Tube: Placed.",
            5: "william johnson right thoracoscopy biopsy negative before suspicious for cancer we went in saw thickened pleura and nodules took 12 biopsies from the wall did talc poudrage too drained it chest tube in wilson md",
            6: "Right medical thoracoscopy with biopsy and pleurodesis. Indication: Suspected malignancy. Findings: Thickened parietal pleura with nodules. Twelve biopsies obtained. Talc poudrage performed. Fluid evacuated. Chest tube placed.",
            7: "[Indication]\nSuspected malignancy, right side.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight thoracoscopy showed thickened pleura/nodules. 12 biopsies taken. Talc poudrage performed. Fluid drained. Chest tube placed.\n[Plan]\nAdmit. Suction.",
            8: "We performed a right medical thoracoscopy on Mr. Johnson due to suspected malignancy. The parietal pleura appeared thickened and nodular. We obtained twelve biopsies from these areas. Following the biopsies, we performed talc poudrage for pleurodesis. The fluid was drained and a chest tube was inserted.",
            9: "Indication: Occult malignancy.\nProcedure: Right pleuroscopy with sampling and sclerosis.\nFindings: Nodular thickening.\nAction: Collected 12 specimens. Administered Talc. Drained fluid. Installed catheter."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for patient names and ages to correspond with the 10 source notes.
    """
    return [
        {"idx": 0, "orig_name": "Jennifer Allen", "orig_age": 55, "names": ["Alice Smith", "Brenda Jones", "Clara Williams", "Diana Brown", "Eva Davis", "Fiona Miller", "Gina Wilson", "Hannah Moore", "Ivy Taylor"]},
        {"idx": 1, "orig_name": "Sharon Lee", "orig_age": 71, "names": ["Joan Anderson", "Karen Thomas", "Linda Jackson", "Mary White", "Nancy Harris", "Olivia Martin", "Paula Thompson", "Quinn Garcia", "Rachel Martinez"]},
        {"idx": 2, "orig_name": "Angela Green", "orig_age": 62, "names": ["Sarah Robinson", "Tina Clark", "Ursula Rodriguez", "Vicky Lewis", "Wendy Lee", "Xena Walker", "Yvonne Hall", "Zoe Allen", "Abby Young"]},
        {"idx": 3, "orig_name": "Kevin Allen", "orig_age": 54, "names": ["Bob Hernandez", "Carl King", "Dave Wright", "Ed Lopez", "Frank Hill", "George Scott", "Harry Green", "Ian Adams", "Jack Baker"]},
        {"idx": 4, "orig_name": "Patricia Taylor", "orig_age": 59, "names": ["Kelly Gonzalez", "Laura Nelson", "Mona Carter", "Nina Mitchell", "Ophelia Perez", "Penny Roberts", "Queen Turner", "Rita Phillips", "Sandy Campbell"]},
        {"idx": 5, "orig_name": "Brian Allen", "orig_age": 78, "names": ["Tom Parker", "Uriah Evans", "Victor Edwards", "Will Collins", "Xavier Stewart", "Yusef Sanchez", "Zack Morris", "Adam Rogers", "Ben Reed"]},
        {"idx": 6, "orig_name": "Betty Jackson", "orig_age": 50, "names": ["Cathy Cook", "Debra Morgan", "Ellen Bell", "Fran Murphy", "Grace Bailey", "Helen Rivera", "Iris Cooper", "Jane Richardson", "Kate Cox"]},
        {"idx": 7, "orig_name": "Kathleen Carter", "orig_age": 56, "names": ["Lisa Howard", "Mia Ward", "Nora Torres", "Olga Peterson", "Patty Gray", "Qiana Ramirez", "Rose James", "Sue Watson", "Tara Brooks"]},
        {"idx": 8, "orig_name": "David Garcia", "orig_age": 68, "names": ["Chris Kelly", "Dan Sanders", "Eric Price", "Fred Bennett", "Greg Wood", "Hank Barnes", "Ike Ross", "Jim Henderson", "Kyle Coleman"]},
        {"idx": 9, "orig_name": "William Johnson", "orig_age": 66, "names": ["Leo Jenkins", "Mike Perry", "Nick Powell", "Oscar Long", "Paul Patterson", "Quentin Hughes", "Ray Flores", "Sam Washington", "Tim Butler"]}
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
                print(f"Warning: Missing variation for Note {idx}, Style {style_num}")
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