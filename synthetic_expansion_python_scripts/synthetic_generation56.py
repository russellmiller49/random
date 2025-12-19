import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_056.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each note index (0-9) 
    across 9 specific styles.
    """
    variations = {
        # Note 0: Sarah Green (Right Thoracoscopy w/ Biopsy & Talc Poudrage)
        0: {
            1: "Pre-op: Lung Ca staging. Right side.\nProc: Thoracoscopy + Biopsy + Talc.\n- 6th ICS entry.\n- Findings: Thickened parietal pleura, nodules.\n- Action: 6 biopsies taken. Talc poudrage performed.\n- Chest tube placed.\nPlan: Admit. Path pending.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the endoscopy suite for right-sided medical thoracoscopy to assess for pleural carcinomatosis. Under moderate sedation, the pleural space was accessed via the 6th intercostal space. Inspection revealed significant parietal pleural thickening with distinct nodularity. Extensive biopsies were harvested from the parietal surface (six specimens) and the diaphragm. Given the macroscopic appearance suggestive of malignancy, talc poudrage was instigated for pleurodesis. The procedure concluded with chest tube placement; hemostasis was secured.",
            3: "Procedure: Thoracoscopy, surgical; with biopsy of pleura (32609) and with pleurodesis (32650).\nSite: Right Hemithorax.\nTechnique: Single port access. Semi-rigid pleuroscope utilized.\nIntervention: Directed biopsy of thickened parietal pleura (6 samples) and diaphragmatic pleura. Talc insufflation performed for chemical pleurodesis based on findings.\nDevice: 24Fr chest tube placed.",
            4: "Procedure Note\nPatient: 79F\nProcedure: Right Medical Thoracoscopy w/ Biopsy & Talc\nAttending: Dr. Williams\nSteps:\n1. Timeout.\n2. Local + Moderate Sedation.\n3. Trocar entry 6th ICS.\n4. Survey: Nodules on parietal pleura.\n5. Biopsied parietal (x6) and diaphragm.\n6. Talc poudrage.\n7. Chest tube secured.",
            5: "pt is here for staging lung ca right side. we did the thoracoscopy under sedation entered at the 6th rib space. saw thickened pleura and nodules took about 6 biopsies from the wall and some from the diaphragm. looked malignant so we did the talc poudrage right then. put a chest tube in no air leak. admitting to floor for pain control and tube management.",
            6: "Medical Thoracoscopy with Pleural Biopsy and Talc Poudrage. Under moderate sedation with local anesthesia, a single-port entry was made at the 6th intercostal space, mid-axillary line. The semi-rigid pleuroscope was inserted. Inspection revealed thickened parietal pleura with nodules. Multiple biopsies were obtained from the parietal pleura (6 specimens) and diaphragmatic pleura. Specimens were sent for histopathology. Talc poudrage was performed for pleurodesis. All fluid was evacuated and a chest tube was placed.",
            7: "[Indication]\nStaging for lung cancer pleural involvement.\n[Anesthesia]\nModerate sedation, local anesthesia.\n[Description]\nRight-sided entry (6th ICS). Findings: Thickened parietal pleura with nodules. Interventions: Parietal biopsies (6), diaphragmatic biopsies, Talc poudrage pleurodesis. Chest tube placed.\n[Plan]\nAdmit. Oncology consult if pos.",
            8: "The patient underwent a right-sided medical thoracoscopy for staging purposes. Upon entering the pleural space through the sixth intercostal space, we observed thickened parietal pleura studded with nodules. We proceeded to take multiple biopsies, specifically six from the parietal pleura and additional samples from the diaphragm. Due to the high suspicion of malignancy, we performed a talc poudrage to prevent fluid recurrence. The lung was re-expanded, and a chest tube was secured.",
            9: "Procedure: Medical Thoracoscopy with Pleural Sampling and Pleurodesis.\nSite: Right.\nFindings: Indurated parietal pleura with nodularity.\nActions: Sampled parietal pleura (6 fragments) and diaphragmatic surface. Administered talc poudrage for symphysis. Evacuated effusion. Anchored chest drain."
        },
        # Note 1: George Martinez (Right Diagnostic Thoracoscopy)
        1: {
            1: "Indication: Mesothelioma suspicion.\nProc: Dx Thoracoscopy (Right).\n- Diffuse nodularity seen.\n- Fluid removed.\n- No biopsy mentioned in this specific note text (Diagnostic code only).\n- Chest tube in.\nPlan: Admit.",
            2: "OPERATIVE REPORT: The patient presented for diagnostic evaluation of the right pleural space due to suspected mesothelioma. Following access at the 6th intercostal space, the pleuroscope was introduced. The inspection demonstrated diffuse pleural nodularity involving the parietal, visceral, and diaphragmatic surfaces. The pleural effusion was completely evacuated under direct visualization. A thoracostomy tube was placed. The lung expanded appropriately without air leak.",
            3: "Billing Code: 32601 (Thoracoscopy, diagnostic).\nLocation: Right.\nDetails: Visualization of parietal, visceral, and diaphragmatic pleura. Findings included diffuse pleural nodularity. Complete fluid evacuation performed. No biopsies recorded in this specific encounter note (Pathology pending from fluid/prior).",
            4: "Resident Note: Right Medical Thoracoscopy (Diagnostic)\nIndication: R/O Mesothelioma\n1. Prep/Drape.\n2. Entry 6th ICS mid-axillary.\n3. Findings: Diffuse nodules.\n4. Suctioned fluid.\n5. Placed chest tube.\nNo complications. Lung up.",
            5: "procedure on mr martinez right side thoracoscopy just diagnostic today. saw a lot of nodules diffuse all over the pleura. sucked out the rest of the fluid. put the tube in 6th intercostal space. lung came up fine no air leak. plan to keep him on the floor until drainage slows down.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Under moderate sedation with local anesthesia, entry was achieved at the 6th intercostal space, mid-axillary line. The semi-rigid pleuroscope was inserted. Findings included diffuse pleural nodularity. Parietal, visceral, and diaphragmatic pleura were visualized. All remaining fluid was evacuated under direct visualization. A chest tube was placed. There was no air leak and the lung expanded.",
            7: "[Indication]\nSuspected mesothelioma.\n[Anesthesia]\nModerate sedation.\n[Description]\nRight side accessed (6th ICS). Visualized diffuse pleural nodularity across parietal/visceral surfaces. Fluid evacuated. Chest tube placed.\n[Plan]\nFloor admission. Path f/u.",
            8: "We performed a diagnostic thoracoscopy on the right side to investigate suspected mesothelioma. Upon inspection via the sixth intercostal space, we noted diffuse nodularity throughout the pleural cavity. We ensured all remaining fluid was suctioned out under direct vision. The procedure was concluded by placing a chest tube; the lung was fully expanded with no evidence of an air leak.",
            9: "Procedure: Diagnostic Pleuroscopy.\nSide: Right.\nObservations: Widespread pleural nodularity.\nExecution: Visualized parietal, visceral, and diaphragmatic surfaces. Extracted remaining effusion. Inserted thoracostomy drain. Confirmed lung re-expansion."
        },
        # Note 2: Jacob Martinez (Right Biopsy + Talc)
        2: {
            1: "Dx: Pleural nodularity.\nProc: Right Thoracoscopy + Biopsy + Talc.\n- Inflammatory changes seen.\n- 6 biopsies parietal pleura + diaphragm.\n- Talc poudrage done.\n- Chest tube to suction.",
            2: "PROCEDURE RECORD: Mr. Martinez underwent a right-sided medical thoracoscopy. The indication was radiographic pleural nodularity. Intraoperative inspection revealed inflammatory changes lacking distinct nodularity, contrary to imaging. Nevertheless, six biopsies were harvested from the parietal pleura and additional tissue from the diaphragm to rule out occult disease. Talc poudrage was instilled to achieve pleurodesis. A chest tube was inserted.",
            3: "CPT Justification:\n- 32609: Thoracoscopy with biopsy (6 parietal samples obtained).\n- 32650: Thoracoscopy with pleurodesis (Talc poudrage).\nSite: Right.\nFindings: Inflammatory changes.\nDisposition: Inpatient.",
            4: "Steps:\n1. Right side prep.\n2. Scope in 6th ICS.\n3. Looked around: Inflammatory changes, no obvious nodules.\n4. Took 6 biopsies anyway (parietal) + diaphragm.\n5. Puffed Talc.\n6. Chest tube in.\nRes: Dr. Walsh.",
            5: "jacob martinez right thoracoscopy. indications were nodules on ct but inside it just looked inflammatory. we took biopsies anyway 6 from the wall and some from diaphragm. did the talc procedure just in case. chest tube placed to suction. no air leak hemostasis good.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Under moderate sedation, single-port entry at 6th intercostal space. Semi-rigid pleuroscope inserted. Findings: Inflammatory changes without nodularity. Multiple biopsies obtained from parietal pleura (6 specimens). Additional biopsies from diaphragmatic pleura. Given findings, talc poudrage performed for pleurodesis. Chest tube placed.",
            7: "[Indication]\nPleural nodularity on imaging.\n[Anesthesia]\nModerate.\n[Description]\nRight side. Findings: Inflammatory changes. Action: 6 parietal biopsies, diaphragm biopsy, Talc poudrage. Fluid evacuated.\n[Plan]\nAdmit to floor. Suction.",
            8: "We carried out a right medical thoracoscopy on Mr. Martinez. Although imaging suggested nodules, direct visualization showed mostly inflammatory changes. We proceeded to biopsy the parietal pleura six times and sampled the diaphragm as well. To manage the effusion, we performed talc poudrage. The chest tube was placed without complication, and the lung expanded well.",
            9: "Procedure: Pleuroscopy with Tissue Sampling and Sclerosant Administration.\nSide: Right.\nFindings: Phlegmonous/inflammatory changes.\nAction: Acquired 6 parietal specimens. Instilled talc for pleurodesis. Drained effusion and sited chest catheter."
        },
        # Note 3: Amanda Ramirez (Left Diagnostic)
        3: {
            1: "Indication: Recurrent effusion.\nProc: Left Diagnostic Thoracoscopy.\n- Nodules found (malignant appearance).\n- Fluid drained.\n- Chest tube placed.\n- No biopsy recorded in this note.",
            2: "OPERATIVE NOTE: The patient underwent a diagnostic medical thoracoscopy on the left side for recurrent effusion of unknown etiology. The pleural space was entered via the 6th intercostal space. Visualization revealed multiple pleural nodules with a malignant macroscopic appearance. The remaining pleural fluid was evacuated. A chest tube was positioned, confirming lung re-expansion and absence of air leak.",
            3: "Code: 32601 (Diagnostic Thoracoscopy).\nSide: Left.\nFindings: Multiple malignant-appearing nodules.\nWork: Visualization of parietal/visceral/diaphragmatic pleura. Evacuation of fluid. Placement of tube. (Note: Biopsy 32609 not documented in this specific text, coding strictly to documentation).",
            4: "Procedure: Left Pleuroscopy (Diagnostic)\nPt: Ramirez, 54F\n1. Port 6th ICS.\n2. Saw multiple nodules (look bad).\n3. Drained fluid.\n4. Chest tube placed.\nPlan: Admit, wait for path/cytology.",
            5: "amanda ramirez left side scope. looking for why the effusion keeps coming back. went in saw a bunch of nodules they look malignant. drained the fluid put a tube in. no air leak. sending to floor.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Single-port entry at 6th intercostal space, mid-axillary line on the Left. Findings: Multiple pleural nodules - malignant appearing. Parietal, visceral, and diaphragmatic pleura visualized. All remaining fluid evacuated. Chest tube placed. No air leak. Lung expanded.",
            7: "[Indication]\nRecurrent pleural effusion, unknown etiology.\n[Anesthesia]\nModerate.\n[Description]\nLeft side. Multiple malignant-appearing nodules visualized. Fluid evacuated. Chest tube placed.\n[Plan]\nAdmit. Tube to water seal.",
            8: "Ms. Ramirez underwent a diagnostic thoracoscopy on the left side to investigate her recurrent effusion. Upon inspection, we identified multiple nodules that appeared malignant. We ensured all fluid was removed and placed a chest tube. The lung expanded fully, and there was no evidence of an air leak.",
            9: "Procedure: Diagnostic Pleuroscopy.\nSide: Left.\nVisualization: Numerous nodules with malignant features.\nTask: Evacuated pleural fluid. Inserted intercostal drain. Verified lung inflation."
        },
        # Note 4: Timothy Scott (Left Diagnostic)
        4: {
            1: "Dx: Left pleural nodularity.\nProc: Dx Thoracoscopy.\n- Mass lesion on diaphragm.\n- Fluid evacuated.\n- Chest tube placed.\n- No biopsy in note.",
            2: "PROCEDURE: Left-sided diagnostic medical thoracoscopy. The instrument was introduced into the 6th intercostal space. Exploration of the hemithorax revealed a distinct mass lesion situated on the diaphragmatic pleura. The parietal and visceral surfaces were otherwise visualized. Effusion was cleared, and a chest tube was sited. The lung was fully expanded.",
            3: "Service: 32601 (Diagnostic Thoracoscopy).\nSite: Left.\nFindings: Diaphragmatic mass lesion.\nProcedure: Visual inspection of all pleural surfaces. Drainage of residual fluid. Chest tube placement. No tissue sampling documented.",
            4: "Left Thoracoscopy\nIndication: Nodules on CT.\nFindings: Mass on diaphragm.\nSteps: Entry 6th ICS -> Looked around -> Drained fluid -> Tube in.\nNo complications.",
            5: "timothy scott left side. went in to look at the nodules. saw a big mass on the diaphragm. looked at the rest of the pleura. drained the fluid put the chest tube in. patient did fine.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Under moderate sedation, single-port entry at 6th intercostal space, mid-axillary line (Left). Semi-rigid pleuroscope inserted. Findings: Mass lesion on diaphragmatic pleura. Parietal, visceral, and diaphragmatic pleura visualized. All remaining fluid evacuated. Chest tube placed.",
            7: "[Indication]\nPleural nodularity.\n[Anesthesia]\nModerate.\n[Description]\nLeft entry. Findings: Mass lesion on diaphragm. Fluid evacuated. Chest tube to water seal.\n[Plan]\nAdmit. Pull tube when <150mL.",
            8: "We performed a diagnostic thoracoscopy on the left side for Mr. Scott. The exam revealed a specific mass lesion located on the diaphragmatic pleura. We visualized the remaining pleural surfaces and evacuated the fluid. A chest tube was placed, and the lung was confirmed to be expanded.",
            9: "Procedure: Exploratory Pleuroscopy.\nSide: Left.\nDiscovery: Mass situated on the diaphragmatic surface.\nAction: Cleared pleural effusion. Installed chest drain. Lung re-inflation confirmed."
        },
        # Note 5: Edward Lopez (Right Diagnostic)
        5: {
            1: "Indication: Exudative effusion (neg cytology).\nProc: Right Dx Thoracoscopy.\n- Findings: Pleural plaques.\n- Fluid evacuated.\n- Chest tube placed.",
            2: "OPERATIVE SUMMARY: The patient underwent right diagnostic thoracoscopy for evaluation of a cytology-negative exudative effusion. Access was established at the 6th intercostal space. Intraoperative findings were notable for pleural plaques consistent with prior exposure. The pleural cavity was drained of fluid, and a chest tube was secured. Lung expansion was satisfactory.",
            3: "CPT: 32601 (Diagnostic).\nLocation: Right.\nFindings: Pleural plaques.\nTechnique: Single port 6th ICS. Inspection of parietal/visceral/diaphragmatic pleura. Fluid evacuation. Tube placement.",
            4: "Procedure: Right Thoracoscopy\nFindings: Pleural plaques.\nSteps: \n1. Sedation.\n2. Port placement.\n3. Scope inspection.\n4. Fluid drainage.\n5. Chest tube.\nLung up, no leak.",
            5: "edward lopez right side. effusion with neg cytology. did the scope saw pleural plaques. drained it all out. put a chest tube in. no air leak. sending to floor.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Single-port entry at 6th intercostal space, mid-axillary line (Right). Findings: Pleural plaques. Parietal, visceral, and diaphragmatic pleura visualized. All remaining fluid evacuated under direct visualization. Chest tube placed. No air leak. Lung expanded.",
            7: "[Indication]\nExudative effusion, neg cytology.\n[Anesthesia]\nModerate.\n[Description]\nRight side. Findings: Pleural plaques. Fluid removed. Chest tube inserted.\n[Plan]\nAdmit. Monitor output.",
            8: "Mr. Lopez had a right-sided diagnostic thoracoscopy today to investigate his effusion. We found pleural plaques upon inspection. We made sure to remove all the remaining fluid and placed a chest tube. The lung re-expanded well without any air leaks.",
            9: "Procedure: Diagnostic Pleuroscopy.\nSide: Right.\nObservations: Pleural plaques identified.\nExecution: Visualized pleural surfaces. Drained exudative fluid. Sited thoracostomy tube."
        },
        # Note 6: Karen White (Right Biopsy)
        6: {
            1: "Indication: Persistent effusion/trapped lung.\nProc: Right Thoracoscopy + Biopsy.\n- Findings: Fibrinous adhesions, trapped lung.\n- 8 biopsies parietal pleura.\n- Fluid evacuated. Chest tube in.",
            2: "PROCEDURE NOTE: Mrs. White underwent right medical thoracoscopy. The pleural space was accessed at the 6th intercostal space. We encountered significant fibrinous adhesions and evidence of trapped lung. Extensive adhesiolysis was not performed, but eight biopsies were obtained from the parietal pleura for characterization. The fluid was evacuated and a chest tube placed to suction.",
            3: "Coding: 32609 (Thoracoscopy w/ biopsy).\nSite: Right.\nFindings: Adhesions, trapped lung.\nSpecimens: 8 parietal pleural biopsies.\nNote: No pleurodesis performed (likely due to trapped lung contraindication).",
            4: "Right Thoracoscopy w/ Biopsy\nPt: White, 81F\nFindings: Trapped lung, adhesions.\nAction: Took 8 biopsies from parietal wall. Drained fluid. Chest tube placed.\nPlan: Suction.",
            5: "karen white right side. effusion not going away. went in with the scope. lung is trapped lots of adhesions. took 8 biopsies from the wall. drained the fluid put the tube in. hope it expands.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Indication: Persistent effusion despite thoracentesis. Right side. Findings: Fibrinous adhesions with trapped lung. Multiple biopsies obtained from parietal pleura (8 specimens). Additional biopsies from diaphragmatic pleura. All fluid evacuated. Chest tube placed.",
            7: "[Indication]\nPersistent effusion, trapped lung.\n[Anesthesia]\nModerate.\n[Description]\nRight entry. Findings: Adhesions, trapped lung. Action: 8 parietal biopsies. Fluid drained. Chest tube placed.\n[Plan]\nAdmit. Suction.",
            8: "We performed a right thoracoscopy on Mrs. White. We found fibrinous adhesions and a trapped lung, which explains the persistent effusion. We took eight biopsies from the parietal pleura to determine the cause. We drained the fluid and placed a chest tube, placing it to suction to encourage expansion.",
            9: "Procedure: Medical Pleuroscopy with Tissue Sampling.\nSide: Right.\nFindings: Fibrinous synechiae and unexpandable lung.\nAction: Harvested 8 parietal specimens. Evacuated effusion. Inserted chest drain."
        },
        # Note 7: Nicholas Green (Left Diagnostic)
        7: {
            1: "Indication: Exudative effusion.\nProc: Left Dx Thoracoscopy.\n- Findings: Fibrinous adhesions, trapped lung.\n- Fluid evacuated.\n- Chest tube placed.\n- No biopsy mentioned.",
            2: "OPERATIVE REPORT: Left diagnostic thoracoscopy. Entry at the 6th intercostal space. Inspection revealed fibrinous adhesions and the appearance of a trapped lung. The parietal, visceral, and diaphragmatic surfaces were visualized within the limits of the adhesions. Fluid was evacuated and a chest tube was placed.",
            3: "Code: 32601 (Diagnostic).\nSide: Left.\nFindings: Adhesions, trapped lung.\nAction: Visualization and fluid evacuation. Chest tube placement. No biopsy or pleurodesis documented.",
            4: "Left Thoracoscopy\nFindings: Trapped lung, adhesions.\nSteps: Entry -> Looked around -> Drained fluid -> Tube.\nNo biopsy. Lung expanded poorly (trapped).",
            5: "nicholas green left side. diagnostic scope. saw adhesions and trapped lung. drained fluid put tube in. no biopsy just looked.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Single-port entry at 6th intercostal space, mid-axillary line (Left). Findings: Fibrinous adhesions with trapped lung. Parietal, visceral, and diaphragmatic pleura visualized. All remaining fluid evacuated. Chest tube placed.",
            7: "[Indication]\nExudative effusion.\n[Description]\nLeft side. Visualized fibrinous adhesions and trapped lung. Fluid evacuated. Chest tube placed.\n[Plan]\nAdmit. Water seal.",
            8: "We looked inside Mr. Green's left chest with the thoracoscope. We found adhesions and what looks like a trapped lung. We drained the fluid and put a chest tube in, but didn't take any biopsies this time.",
            9: "Procedure: Diagnostic Pleuroscopy.\nSide: Left.\nObservations: Fibrinous bands and entrapped parenchyma.\nAction: Drained effusion. Placed intercostal catheter."
        },
        # Note 8: Donald Flores (Left Biopsy)
        8: {
            1: "Indication: TB pleuritis suspicion.\nProc: Left Thoracoscopy + Biopsy.\n- Findings: Inflammatory changes.\n- 9 biopsies parietal pleura + diaphragm.\n- Fluid evacuated. Chest tube in.",
            2: "PROCEDURE NOTE: Left medical thoracoscopy for suspected tuberculous pleuritis. Access via 6th intercostal space. The pleura exhibited inflammatory changes without distinct nodularity. To ensure diagnostic yield, nine biopsies were obtained from the parietal pleura, along with diaphragmatic sampling. Fluid was evacuated and a chest tube inserted.",
            3: "CPT: 32609 (Biopsy).\nSide: Left.\nFindings: Inflammatory.\nSamples: 9 parietal biopsies.\nNote: High biopsy count to r/o TB. No talc.",
            4: "Left Thoracoscopy w/ Biopsy\nIndication: ?TB\nFindings: Inflamed pleura.\nAction: 9 biopsies taken from parietal wall. Diaphragm sampled. Fluid out. Tube in.",
            5: "donald flores left side. think its TB. went in saw inflammation. took a lot of biopsies 9 of them plus diaphragm just to be sure. put the tube in. no air leak.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Indication: Suspected tuberculous pleuritis. Left side. Findings: Inflammatory changes without nodularity. Multiple biopsies obtained from parietal pleura (9 specimens). Additional biopsies from diaphragmatic pleura. All fluid evacuated. Chest tube placed.",
            7: "[Indication]\nSuspected TB pleuritis.\n[Anesthesia]\nModerate.\n[Description]\nLeft side. Inflammatory changes. 9 parietal biopsies taken. Fluid drained. Chest tube in.\n[Plan]\nAdmit. Await path.",
            8: "We performed a left-sided thoracoscopy on Mr. Flores to check for TB. The pleura looked inflamed but didn't have nodules. We took nine biopsies from the chest wall and some from the diaphragm to send for analysis. We drained the fluid and left a chest tube in place.",
            9: "Procedure: Pleuroscopy with Multiple Biopsies.\nSide: Left.\nFindings: Pleuritis/inflammation.\nAction: Acquired 9 parietal tissue samples. Evacuated fluid. Positioned thoracostomy tube."
        },
        # Note 9: Melissa Wilson (Right Diagnostic)
        9: {
            1: "Indication: Suspected malignancy.\nProc: Right Dx Thoracoscopy.\n- Findings: Normal appearing pleura.\n- Fluid evacuated.\n- Chest tube placed.",
            2: "OPERATIVE REPORT: Right diagnostic thoracoscopy for suspected malignant pleural disease. Upon inspection via the 6th intercostal space, the parietal, visceral, and diaphragmatic pleura appeared normal. No nodules or masses were identified. The effusion was evacuated, and a chest tube was placed. Lung expansion was confirmed.",
            3: "Code: 32601 (Diagnostic).\nSide: Right.\nFindings: Normal pleura.\nAction: Visual inspection, fluid drainage, chest tube. No biopsy performed (grossly normal).",
            4: "Right Thoracoscopy\nIndication: R/O Cancer.\nFindings: Normal pleura.\nSteps: Entry -> Exam -> Drainage -> Tube.\nNo biopsy taken.",
            5: "melissa wilson right side. thought it was cancer but pleura looks normal. drained the fluid put the tube in. no biopsy needed.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Single-port entry at 6th intercostal space, mid-axillary line (Right). Findings: Normal-appearing pleura. Parietal, visceral, and diaphragmatic pleura visualized. All remaining fluid evacuated. Chest tube placed. No air leak.",
            7: "[Indication]\nSuspected malignancy.\n[Description]\nRight side. Normal appearing pleura. Fluid drained. Chest tube placed.\n[Plan]\nAdmit. Water seal.",
            8: "We did a diagnostic thoracoscopy on Ms. Wilson's right side. Surprisingly, the pleura looked completely normal despite the suspicion of cancer. We drained the fluid and placed a chest tube, but didn't see anything to biopsy.",
            9: "Procedure: Diagnostic Pleuroscopy.\nSide: Right.\nObservations: Unremarkable pleural surfaces.\nAction: Drained effusion. Inserted chest drain. Confirmed re-expansion."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data to generate random names/ages for the variations.
    Aligned with the 10 notes in the source file.
    """
    return [
        {"idx": 0, "orig_name": "Green, Sarah", "orig_age": 79, "names": ["Alice Thompson", "Betty White", "Carol Davis", "Diana Miller", "Evelyn Wilson", "Frances Moore", "Gloria Taylor", "Helen Anderson", "Irene Thomas"]},
        {"idx": 1, "orig_name": "Martinez, George", "orig_age": 57, "names": ["Arthur King", "Ben Scott", "Carl Green", "David Baker", "Edward Adams", "Frank Nelson", "George Carter", "Henry Mitchell", "Ian Roberts"]},
        {"idx": 2, "orig_name": "Martinez, Jacob", "orig_age": 74, "names": ["Jack Phillips", "Kevin Campbell", "Larry Evans", "Mike Turner", "Nathan Parker", "Oscar Collins", "Paul Edwards", "Quinn Stewart", "Ralph Sanchez"]},
        {"idx": 3, "orig_name": "Ramirez, Amanda", "orig_age": 54, "names": ["Jane Morris", "Kelly Rogers", "Lisa Reed", "Mary Cook", "Nancy Morgan", "Olivia Bell", "Patricia Murphy", "Rachel Bailey", "Sarah Rivera"]},
        {"idx": 4, "orig_name": "Scott, Timothy", "orig_age": 60, "names": ["Steve Cooper", "Tom Richardson", "Victor Cox", "Walter Howard", "Xavier Ward", "Yves Torres", "Zachary Peterson", "Adam Gray", "Brian James"]},
        {"idx": 5, "orig_name": "Lopez, Edward", "orig_age": 52, "names": ["Charles Watson", "Daniel Brooks", "Eric Kelly", "Fred Sanders", "Greg Price", "Harry Bennett", "Ivan Wood", "John Barnes", "Kyle Ross"]},
        {"idx": 6, "orig_name": "White, Karen", "orig_age": 81, "names": ["Laura Henderson", "Martha Coleman", "Nora Jenkins", "Opal Perry", "Paula Powell", "Queen Long", "Rose Patterson", "Susan Hughes", "Tina Flores"]},
        {"idx": 7, "orig_name": "Green, Nicholas", "orig_age": 71, "names": ["Leo Washington", "Max Butler", "Nick Simmons", "Oliver Foster", "Peter Gonzales", "Quincy Bryant", "Ray Alexander", "Sam Russell", "Ted Griffin"]},
        {"idx": 8, "orig_name": "Flores, Donald", "orig_age": 59, "names": ["Ulysses Diaz", "Vince Hayes", "Will Myers", "Xander Ford", "Yusuf Hamilton", "Zane Graham", "Aaron Sullivan", "Bob Wallace", "Chris Woods"]},
        {"idx": 9, "orig_name": "Wilson, Melissa", "orig_age": 54, "names": ["Uma Cole", "Violet West", "Wendy Jordan", "Xena Owens", "Yvonne Reynolds", "Zoe Fisher", "Amy Ellis", "Bella Harrison", "Cathy Gibson"]}
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
            
            # Get the specific name
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