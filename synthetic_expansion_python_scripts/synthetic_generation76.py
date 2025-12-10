import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_076.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations for the 10 source notes.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Taylor, John (Right, Biopsy x7, Talc)
            1: "Proc: Rt Med Thoracoscopy w/ Biopsy & Talc.\nFindings: Diffuse pleural nodularity.\nActions:\n- 7 biopsies taken from parietal pleura.\n- Diaphragmatic biopsies taken.\n- Talc poudrage performed.\n- Fluid evacuated.\n- Chest tube placed.\nStatus: Hemostasis achieved. No leak.",
            2: "OPERATIVE NARRATIVE: The patient underwent a right-sided medical thoracoscopy under moderate sedation. Inspection of the pleural cavity revealed diffuse nodularity involving the parietal surface. Histological sampling was performed, yielding seven distinct specimens from the parietal pleura, alongside diaphragmatic sampling. Following biopsy, chemical pleurodesis was achieved via talc insufflation (poudrage) to address the malignant effusion. A chest tube was secured post-evacuation.",
            3: "Code Justification:\n- 32609 (Thoracoscopy with biopsy): Right pleural space accessed. Diffuse nodules visualized. Biopsy forceps used to obtain 7 specimens from parietal pleura.\n- 32650 (Thoracoscopy with pleurodesis): Talc poudrage insufflated under direct visualization for pleurodesis.\nDevice: Semi-rigid pleuroscope. Outcome: Fluid drained, tube placed.",
            4: "Procedure Note: Right Thoracoscopy\nSteps:\n1. Time out/Sedation.\n2. Port created 6th ICS mid-axillary.\n3. Scope inserted; diffuse nodules seen.\n4. Biopsies x7 taken from parietal pleura; additional from diaphragm.\n5. Talc poudrage performed for pleurodesis.\n6. Chest tube placed to suction.\nComplications: None.",
            5: "did a right thoracoscopy on mr taylor saw a lot of nodules on the pleura took about 7 biopsies from the wall and some from the diaphragm sent for path then we did talc poudrage to stop the fluid chest tube is in place no air leak patient fine",
            6: "Under moderate sedation, a right-sided single-port thoracoscopy was performed. The pleural space demonstrated diffuse nodularity. Seven biopsies were obtained from the parietal pleura, with additional samples from the diaphragm. Given the findings, talc poudrage was performed for pleurodesis. All fluid was evacuated and a chest tube was placed. Hemostasis was confirmed.",
            7: "[Indication] Suspected mesothelioma.\n[Anesthesia] Moderate sedation, local.\n[Description] Right thoracoscopy performed. Findings: Diffuse pleural nodularity. Actions: 7 biopsies parietal pleura, plus diaphragmatic biopsies. Talc poudrage performed.\n[Plan] Admit, chest tube to suction, path pending.",
            8: "We performed a right medical thoracoscopy on Mr. Taylor. Upon entering the pleural space, we observed diffuse nodularity throughout. We proceeded to obtain seven biopsies from the parietal pleura and additional samples from the diaphragm. Following the biopsies, we performed talc poudrage for pleurodesis. The fluid was evacuated and a chest tube was inserted.",
            9: "Right pleuroscopy performed. Pleura demonstrated diffuse nodularity. Seven tissue samples harvested from the parietal wall, with additional sampling of the diaphragm. Talc insufflation executed for symphysis. Fluid drained and catheter inserted. Hemostasis secured."
        },
        1: { # Rivera, Susan (Right, Biopsy x12, No Talc)
            1: "Proc: Rt Med Thoracoscopy w/ Biopsy.\nFindings: Inflammatory changes. No nodules.\nActions:\n- 12 biopsies from parietal pleura.\n- Diaphragmatic biopsies taken.\n- Fluid evacuated.\n- Chest tube placed.\n- No pleurodesis performed.\nStatus: Stable.",
            2: "PROCEDURE RECORD: Right-sided medical thoracoscopy was initiated for exudative effusion. Visual inspection demonstrated significant inflammatory changes lacking distinct nodularity. Extensive sampling was conducted, with twelve biopsies harvested from the parietal pleura and additional tissue from the diaphragm for immunohistochemistry. Fluid was fully evacuated. No chemical pleurodesis was undertaken. A thoracostomy tube was positioned.",
            3: "Billing: 32609 (Thoracoscopy with pleura biopsy).\nTechnique: Right 6th ICS entry. Visual inspection showed inflammation. Biopsy forceps utilized to obtain 12 specimens from parietal pleura and additional from diaphragm to rule out malignancy. No therapeutic pleurodesis (32650) performed. Chest tube inserted.",
            4: "Resident Note: Right Medical Thoracoscopy\nSteps:\n1. Moderate sedation.\n2. Trocar placement right chest.\n3. Visualization: Inflammatory changes, no masses.\n4. Biopsy: 12 parietal specimens + diaphragm samples.\n5. Fluid drainage complete.\n6. Chest tube secured. No air leak.",
            5: "right side thoracoscopy done for effusion looked mostly inflammatory didn't see nodules but we took a lot of biopsies anyway 12 from the parietal pleura and some from diaphragm just to be sure drained the fluid put the chest tube in no talc used today",
            6: "Right medical thoracoscopy was performed under local anesthesia and sedation. The pleural space revealed inflammatory changes without obvious nodularity. Twelve biopsies were taken from the parietal pleura, along with diaphragmatic biopsies. The specimens were sent for pathology. Fluid was drained and a chest tube was placed. The patient tolerated the procedure well.",
            7: "[Indication] Cytology-negative effusion.\n[Anesthesia] Moderate.\n[Description] Right thoracoscopy. Findings: Inflammatory changes. Interventions: 12 biopsies parietal pleura, plus diaphragmatic samples. Fluid drained. Chest tube placed.\n[Plan] Path review, oncology consult if positive.",
            8: "Ms. Rivera underwent a right medical thoracoscopy. The inspection revealed inflammatory changes but no distinct nodularity. We obtained twelve biopsies from the parietal pleura and additional samples from the diaphragm to ensure a comprehensive evaluation. All fluid was evacuated, and a chest tube was placed. No pleurodesis was performed.",
            9: "Right pleuroscopy executed. Visual assessment showed inflammatory alterations without nodularity. Twelve tissue samples harvested from the parietal pleura, with further sampling of the diaphragm. Effusion drained. Catheter deployed. No sclerosing agent utilized."
        },
        2: { # Wilson, Gary (Right, Biopsy x12, Talc)
            1: "Proc: Rt Thoracoscopy, Biopsy, Pleurodesis.\nFindings: Mass on diaphragmatic pleura.\nActions:\n- 12 biopsies parietal pleura.\n- Diaphragmatic biopsies.\n- Talc poudrage.\n- Tube placed.\nStatus: Hemostasis confirmed.",
            2: "OPERATIVE REPORT: The patient underwent a right medical thoracoscopy for staging. A distinct mass lesion was identified on the diaphragmatic pleura. Twelve biopsies were excised from the parietal pleura, with additional targeted sampling of the diaphragmatic mass. Given the findings, palliative pleurodesis was induced via talc poudrage. The hemithorax was drained and a chest tube inserted.",
            3: "Coding: 32609 (Biopsy) & 32650 (Talc Pleurodesis).\nSite: Right Hemithorax.\nDetails: Mass visualized. 12 parietal biopsies obtained. Diaphragmatic biopsies obtained. Talc insufflated for pleurodesis due to malignant appearance. Chest tube placed for drainage.",
            4: "Procedure: Right Thoracoscopy + Biopsy + Talc\nSteps:\n1. Sedation start.\n2. Entry right 6th ICS.\n3. Findings: Diaphragmatic mass.\n4. Biopsies: 12 parietal + diaphragm.\n5. Intervention: Talc poudrage.\n6. Tube placed.\nPlan: Admit.",
            5: "did the right thoracoscopy on mr wilson saw a mass on the diaphragm took 12 biopsies from the wall and some from the diaphragm too decided to do the talc poudrage while we were in there drained the fluid chest tube is in looks good",
            6: "Under moderate sedation, a right medical thoracoscopy was performed. A mass lesion was noted on the diaphragmatic pleura. Twelve biopsies were obtained from the parietal pleura, and additional samples were taken from the diaphragm. Talc poudrage was performed for pleurodesis. The fluid was evacuated, and a chest tube was placed without complication.",
            7: "[Indication] Staging lung cancer.\n[Anesthesia] Moderate.\n[Description] Right thoracoscopy. Mass on diaphragm. 12 parietal biopsies taken. Diaphragmatic biopsies taken. Talc poudrage performed.\n[Plan] Monitor output, await path.",
            8: "We performed a right medical thoracoscopy on Mr. Wilson. We visualized a mass on the diaphragmatic pleura. To ensure accurate staging, we took twelve biopsies from the parietal pleura and additional samples from the diaphragm. Given the appearance, we proceeded with talc poudrage for pleurodesis before placing the chest tube.",
            9: "Right pleuroscopy completed. Diaphragmatic mass observed. Twelve tissue samples harvested from parietal pleura; diaphragm also sampled. Talc insufflation executed for symphysis. Fluid drained and catheter deployed."
        },
        3: { # Jones, Jeffrey (Right, Diagnostic 32601 - Note: Orig text says "Medical Thoracoscopy (Pleuroscopy) - Diagnostic" but describes nodules. No biopsy count. Just "evacuated". 32601 is correct.)
            1: "Proc: Rt Diagnostic Thoracoscopy.\nFindings: Thickened parietal pleura, nodules.\nActions:\n- Visual inspection.\n- Fluid evacuated.\n- Chest tube placed.\nStatus: Lung expanded. No leak.",
            2: "PROCEDURE NOTE: Right-sided diagnostic medical thoracoscopy was performed. Inspection revealed significant thickening of the parietal pleura studded with nodularity. The visceral and diaphragmatic surfaces were visualized. Fluid was completely evacuated under direct vision. A thoracostomy tube was placed to water seal. The lung was observed to re-expand.",
            3: "Billing: 32601 (Diagnostic Thoracoscopy).\nRationale: Right pleural space inspected. Thickened pleura/nodules noted. Fluid drained. No biopsies performed or coded (included in diag if minor, but here focusing on diagnostic code). No pleurodesis. Chest tube placed.",
            4: "Resident Note: Right Diagnostic Pleuroscopy\nSteps:\n1. Sedation.\n2. Single port 6th ICS.\n3. Exam: Thickened pleura with nodules.\n4. Drainage: All fluid removed.\n5. Closure: Chest tube placed.\nPlan: Path review (if fluid sent).",
            5: "diagnostic scope on the right side saw some thickened pleura and nodules didn't do biopsies just drained the fluid and put the tube in lung came up fine no air leak sending to floor",
            6: "A right diagnostic medical thoracoscopy was performed. The parietal pleura appeared thickened with multiple nodules. The visceral and diaphragmatic pleura were also visualized. Remaining pleural fluid was evacuated. A chest tube was inserted, and the lung expanded well. No air leak was noted.",
            7: "[Indication] Pleural nodularity.\n[Anesthesia] Moderate.\n[Description] Right diagnostic thoracoscopy. Findings: Thickened parietal pleura with nodules. Interventions: Fluid evacuation. Chest tube placement.\n[Plan] Monitor drainage.",
            8: "Mr. Jones underwent a right diagnostic medical thoracoscopy. Upon inspection, we noted thickened parietal pleura with nodules. We visualized the visceral and diaphragmatic surfaces as well. We evacuated all remaining fluid under direct visualization and placed a chest tube. The lung expanded appropriately.",
            9: "Right diagnostic pleuroscopy executed. Observed thickened parietal membrane with nodules. Effusion drained. Catheter deployed. Lung re-expansion confirmed."
        },
        4: { # Moore, Karen (Right, Biopsy x11, Talc)
            1: "Proc: Rt Thoracoscopy w/ Biopsy & Talc.\nFindings: Inflammatory changes.\nActions:\n- 11 biopsies parietal pleura.\n- Diaphragmatic biopsies.\n- Talc poudrage.\n- Tube placed.\nStatus: No leak.",
            2: "OPERATIVE SUMMARY: The patient underwent right-sided medical thoracoscopy. The pleural surfaces exhibited inflammatory changes without distinct nodularity. Eleven biopsies were obtained from the parietal pleura, with additional sampling of the diaphragm. Talc poudrage was administered for pleurodesis. The chest was drained and a tube secured.",
            3: "Codes: 32609 (Biopsy) + 32650 (Pleurodesis).\nSite: Right.\nTech: 11 specimens taken from parietal pleura via forceps. Diaphragm sampled. Talc insufflated for chemical pleurodesis. Chest tube inserted.",
            4: "Procedure: Right Thoracoscopy\nSteps:\n1. Sedation.\n2. Scope inserted right 6th ICS.\n3. Findings: Inflammation.\n4. Biopsies: 11 parietal + diaphragm.\n5. Talc poudrage.\n6. Chest tube placed.\nPlan: Admit.",
            5: "right thoracoscopy for karen she had inflammation no nodules took 11 biopsies from the wall plus some from diaphragm did the talc poudrage too drained it all chest tube in place no leaks",
            6: "Right medical thoracoscopy was performed under local anesthesia. Inflammatory changes were noted without nodularity. Eleven biopsies were obtained from the parietal pleura, along with diaphragmatic biopsies. Talc poudrage was performed for pleurodesis. Fluid was evacuated and a chest tube was placed.",
            7: "[Indication] Suspected TB pleuritis.\n[Anesthesia] Moderate.\n[Description] Right thoracoscopy. Inflammatory changes. 11 parietal biopsies. Diaphragmatic biopsies. Talc poudrage.\n[Plan] Path results.",
            8: "We performed a right medical thoracoscopy on Ms. Moore. The pleura showed inflammatory changes. We collected eleven biopsies from the parietal pleura and additional samples from the diaphragm. We then performed talc poudrage for pleurodesis and placed a chest tube.",
            9: "Right pleuroscopy performed. Inflammatory alterations observed. Eleven tissue samples harvested from parietal pleura; diaphragm also sampled. Talc insufflation executed. Fluid drained and catheter deployed."
        },
        5: { # Lopez, Timothy (Left, Diagnostic 32601 - "Fibrinous adhesions with trapped lung")
            1: "Proc: Lt Diagnostic Thoracoscopy.\nFindings: Fibrinous adhesions, trapped lung.\nActions:\n- Adhesions visualized.\n- Fluid evacuated.\n- Chest tube placed.\nStatus: Lung expanded (despite trapped lung diagnosis, note says lung expanded - sticking to source text).",
            2: "PROCEDURE NOTE: Left-sided diagnostic thoracoscopy was undertaken. Examination revealed extensive fibrinous adhesions consistent with trapped lung physiology. Parietal and visceral surfaces were inspected. Fluid was evacuated. A chest tube was placed to water seal. The lung was noted to expand.",
            3: "Billing: 32601 (Diagnostic Thoracoscopy).\nRationale: Left pleural space accessed. Adhesions/trapped lung documented. Fluid drained. No biopsies (32609) or lysis (32651) documented in source. Chest tube placed.",
            4: "Resident Note: Left Diagnostic Pleuroscopy\nSteps:\n1. Sedation.\n2. Port 6th ICS.\n3. Findings: Adhesions, trapped lung.\n4. Fluid drained.\n5. Chest tube placed.\nPlan: Monitor.",
            5: "left side diagnostic scope saw a lot of adhesions and trapped lung didn't biopsy just drained the fluid and put the tube in lung expanded okay no air leak",
            6: "A left diagnostic medical thoracoscopy was performed. Fibrinous adhesions and trapped lung were observed. The parietal, visceral, and diaphragmatic pleura were visualized. All fluid was evacuated, and a chest tube was placed. The lung expanded, and no air leak was noted.",
            7: "[Indication] Suspected mesothelioma.\n[Anesthesia] Moderate.\n[Description] Left diagnostic thoracoscopy. Findings: Fibrinous adhesions, trapped lung. Interventions: Fluid evacuation. Chest tube placement.\n[Plan] Path review.",
            8: "Mr. Lopez underwent a left diagnostic medical thoracoscopy. We observed fibrinous adhesions and evidence of trapped lung. We visualized the pleural surfaces and evacuated the remaining fluid. A chest tube was placed, and the lung expanded without air leak.",
            9: "Left diagnostic pleuroscopy executed. Observed fibrinous synechiae and trapped lung. Effusion drained. Catheter deployed. Lung re-expansion confirmed."
        },
        6: { # Smith, Elizabeth (Right, Biopsy x10, Talc)
            1: "Proc: Rt Thoracoscopy w/ Biopsy & Talc.\nFindings: Malignant nodules.\nActions:\n- 10 biopsies parietal pleura.\n- Diaphragmatic biopsies.\n- Talc poudrage.\n- Tube placed.\nStatus: No leak.",
            2: "OPERATIVE REPORT: Right medical thoracoscopy was performed for persistent effusion. Multiple nodules with a malignant appearance were identified on the parietal pleura. Ten biopsies were harvested from the parietal surface, with additional sampling of the diaphragm. Talc poudrage was performed for pleurodesis. The chest was drained and a tube placed.",
            3: "Codes: 32609 (Biopsy) + 32650 (Pleurodesis).\nSite: Right.\nTech: 10 specimens taken from parietal pleura. Diaphragm sampled. Talc insufflated. Chest tube inserted.",
            4: "Procedure: Right Thoracoscopy\nSteps:\n1. Sedation.\n2. Scope inserted right 6th ICS.\n3. Findings: Malignant nodules.\n4. Biopsies: 10 parietal + diaphragm.\n5. Talc poudrage.\n6. Chest tube placed.\nPlan: Oncology consult.",
            5: "right thoracoscopy for elizabeth saw nodules looked malignant took 10 biopsies from the wall plus some from diaphragm did the talc poudrage too drained it all chest tube in place",
            6: "Right medical thoracoscopy was performed. Multiple malignant-appearing nodules were noted. Ten biopsies were obtained from the parietal pleura, along with diaphragmatic biopsies. Talc poudrage was performed for pleurodesis. Fluid was evacuated and a chest tube was placed.",
            7: "[Indication] Persistent effusion.\n[Anesthesia] Moderate.\n[Description] Right thoracoscopy. Malignant nodules. 10 parietal biopsies. Diaphragmatic biopsies. Talc poudrage.\n[Plan] Path results.",
            8: "We performed a right medical thoracoscopy on Ms. Smith. The pleura showed multiple malignant-appearing nodules. We collected ten biopsies from the parietal pleura and additional samples from the diaphragm. We then performed talc poudrage for pleurodesis and placed a chest tube.",
            9: "Right pleuroscopy performed. Malignant nodules observed. Ten tissue samples harvested from parietal pleura; diaphragm also sampled. Talc insufflation executed. Fluid drained and catheter deployed."
        },
        7: { # Lee, Kathleen (Left, Biopsy x11, Talc)
            1: "Proc: Lt Thoracoscopy w/ Biopsy & Talc.\nFindings: Visceral tumor implants.\nActions:\n- 11 biopsies parietal pleura.\n- Diaphragmatic biopsies.\n- Talc poudrage.\n- Tube placed.\nStatus: No leak.",
            2: "PROCEDURE NOTE: Left-sided medical thoracoscopy revealed tumor implants on the visceral pleura. Eleven biopsies were obtained from the parietal pleura, along with diaphragmatic sampling. Talc poudrage was utilized for pleurodesis. Fluid was evacuated and a chest tube positioned.",
            3: "Billing: 32609 (Biopsy) & 32650 (Talc).\nSite: Left.\nDetails: Visceral implants seen. 11 parietal biopsies taken. Diaphragmatic biopsies taken. Talc poudrage performed. Chest tube placed.",
            4: "Resident Note: Left Thoracoscopy\nSteps:\n1. Sedation.\n2. Entry left 6th ICS.\n3. Findings: Tumor implants.\n4. Biopsies: 11 parietal + diaphragm.\n5. Talc poudrage.\n6. Chest tube placed.\nPlan: Admit.",
            5: "left thoracoscopy on kathleen saw tumor implants took 11 biopsies from parietal pleura and some from diaphragm did talc poudrage drained the fluid put the chest tube in",
            6: "Left medical thoracoscopy was performed. Visceral pleural tumor implants were visualized. Eleven biopsies were obtained from the parietal pleura, along with diaphragmatic biopsies. Talc poudrage was performed for pleurodesis. Fluid was evacuated and a chest tube was placed.",
            7: "[Indication] Persistent effusion.\n[Anesthesia] Moderate.\n[Description] Left thoracoscopy. Visceral tumor implants. 11 parietal biopsies. Diaphragmatic biopsies. Talc poudrage.\n[Plan] Path results.",
            8: "We performed a left medical thoracoscopy on Ms. Lee. We observed visceral pleural tumor implants. We collected eleven biopsies from the parietal pleura and additional samples from the diaphragm. We then performed talc poudrage for pleurodesis and placed a chest tube.",
            9: "Left pleuroscopy performed. Visceral tumor implants observed. Eleven tissue samples harvested from parietal pleura; diaphragm also sampled. Talc insufflation executed. Fluid drained and catheter deployed."
        },
        8: { # Lee, William (Left, Biopsy x12, No Talc)
            1: "Proc: Lt Thoracoscopy w/ Biopsy.\nFindings: Inflammatory changes.\nActions:\n- 12 biopsies parietal pleura.\n- Diaphragmatic biopsies.\n- Fluid evacuated.\n- Tube placed.\n- No talc.\nStatus: No leak.",
            2: "OPERATIVE REPORT: Left medical thoracoscopy was performed for suspected malignancy. Inflammatory changes were noted without distinct nodularity. Twelve biopsies were harvested from the parietal pleura, with additional diaphragmatic sampling. Fluid was evacuated. No pleurodesis was performed. A chest tube was placed.",
            3: "Code: 32609 (Biopsy).\nSite: Left.\nTech: 12 parietal biopsies obtained. Diaphragm sampled. No talc used. Chest tube inserted.",
            4: "Procedure: Left Thoracoscopy\nSteps:\n1. Sedation.\n2. Scope inserted left 6th ICS.\n3. Findings: Inflammation.\n4. Biopsies: 12 parietal + diaphragm.\n5. Fluid drained.\n6. Chest tube placed.\nPlan: Path review.",
            5: "left thoracoscopy for william inflammation seen no nodules took 12 biopsies from the wall and some from diaphragm drained fluid chest tube in no talc",
            6: "Left medical thoracoscopy was performed. Inflammatory changes were noted without nodularity. Twelve biopsies were obtained from the parietal pleura, along with diaphragmatic biopsies. Fluid was evacuated and a chest tube was placed.",
            7: "[Indication] Biopsy-negative malignancy.\n[Anesthesia] Moderate.\n[Description] Left thoracoscopy. Inflammatory changes. 12 parietal biopsies. Diaphragmatic biopsies. Fluid drained. Chest tube placed.\n[Plan] Path results.",
            8: "We performed a left medical thoracoscopy on Mr. Lee. The pleura showed inflammatory changes. We collected twelve biopsies from the parietal pleura and additional samples from the diaphragm. We evacuated the fluid and placed a chest tube. No pleurodesis was done.",
            9: "Left pleuroscopy performed. Inflammatory alterations observed. Twelve tissue samples harvested from parietal pleura; diaphragm also sampled. Effusion drained. Catheter deployed."
        },
        9: { # Young, Matthew (Right, Diagnostic? Wait, text says "Talc poudrage performed". Code is 32650. No biopsy mentions.)
            1: "Proc: Rt Thoracoscopy w/ Pleurodesis.\nFindings: Inflammatory changes.\nActions:\n- Visualization.\n- Talc poudrage.\n- Fluid evacuated.\n- Tube placed.\nStatus: Lung expanded.",
            2: "PROCEDURE NOTE: Right-sided medical thoracoscopy was performed. Inspection revealed inflammatory changes without nodularity. Parietal and visceral surfaces were visualized. Talc poudrage was performed for pleurodesis. Fluid was evacuated. A chest tube was placed.",
            3: "Billing: 32650 (Pleurodesis).\nRationale: Right pleural space accessed. Inflammatory changes seen. Talc poudrage performed for pleurodesis. Chest tube placed.",
            4: "Resident Note: Right Thoracoscopy + Talc\nSteps:\n1. Sedation.\n2. Entry right 6th ICS.\n3. Findings: Inflammation.\n4. Talc poudrage.\n5. Fluid drained.\n6. Chest tube placed.\nPlan: Monitor.",
            5: "right thoracoscopy on matthew inflammation seen no nodules did talc poudrage drained the fluid put the chest tube in",
            6: "Right medical thoracoscopy was performed. Inflammatory changes were noted without nodularity. Talc poudrage was performed for pleurodesis. All remaining fluid was evacuated, and a chest tube was placed. The lung expanded well.",
            7: "[Indication] Malignant pleural disease.\n[Anesthesia] Moderate.\n[Description] Right thoracoscopy. Inflammatory changes. Talc poudrage performed. Fluid evacuated. Chest tube placed.\n[Plan] Monitor.",
            8: "Mr. Young underwent a right medical thoracoscopy. We observed inflammatory changes but no nodules. We performed talc poudrage for pleurodesis after draining the fluid. A chest tube was placed, and the lung expanded.",
            9: "Right pleuroscopy executed. Inflammatory alterations observed. Talc insufflation executed for symphysis. Effusion drained. Catheter deployed."
        }
    }
    return variations

def get_base_data_mocks():
    # Mock data to replace PII. One entry for each of the 10 source notes.
    # Note: Ages are based on original file to keep 'slightly' random logic valid.
    return [
        {"idx": 0, "orig_name": "Taylor, John", "orig_age": 82, "names": ["Arthur Dent", "Ford Prefect", "Zaphod Beeblebrox", "Tricia McMillan", "Marvin Android", "Slartibartfast Magrathea", "Roosta Staal", "Vogon Jeltz", "Prostetnic Vogon"]},
        {"idx": 1, "orig_name": "Rivera, Susan", "orig_age": 76, "names": ["Ellen Ripley", "Sarah Connor", "Leia Organa", "Dana Scully", "Clarice Starling", "Hermione Granger", "Katniss Everdeen", "Furiosa Road", "Trinity Matrix"]},
        {"idx": 2, "orig_name": "Wilson, Gary", "orig_age": 68, "names": ["James Kirk", "Jean-Luc Picard", "Benjamin Sisko", "Kathryn Janeway", "Jonathan Archer", "Christopher Pike", "Spock Vulcan", "Leonard McCoy", "Montgomery Scott"]},
        {"idx": 3, "orig_name": "Jones, Jeffrey", "orig_age": 71, "names": ["Gandalf Grey", "Aragorn Elessar", "Legolas Greenleaf", "Gimli Gloin", "Frodo Baggins", "Samwise Gamgee", "Meriadoc Brandybuck", "Peregrin Took", "Boromir Denethor"]},
        {"idx": 4, "orig_name": "Moore, Karen", "orig_age": 73, "names": ["Dorothy Gale", "Alice Liddell", "Wendy Darling", "Mary Poppins", "Maria Von Trapp", "Eliza Doolittle", "Annie Hall", "Sally Albright", "Vivian Ward"]},
        {"idx": 5, "orig_name": "Lopez, Timothy", "orig_age": 67, "names": ["Tony Stark", "Steve Rogers", "Bruce Banner", "Thor Odinson", "Natasha Romanoff", "Clint Barton", "Nick Fury", "Phil Coulson", "Maria Hill"]},
        {"idx": 6, "orig_name": "Smith, Elizabeth", "orig_age": 64, "names": ["Lara Croft", "Jill Valentine", "Samus Aran", "Chun Li", "Princess Peach", "Zelda Hyrule", "Tifa Lockhart", "Aerith Gainsborough", "Yuna Spira"]},
        {"idx": 7, "orig_name": "Lee, Kathleen", "orig_age": 55, "names": ["Buffy Summers", "Willow Rosenberg", "Xander Harris", "Rupert Giles", "Cordelia Chase", "Angel Liam", "Spike William", "Tara Maclay", "Anya Jenkins"]},
        {"idx": 8, "orig_name": "Lee, William", "orig_age": 58, "names": ["Fox Mulder", "Walter Skinner", "John Doggett", "Monica Reyes", "Cigarette Man", "Alex Krycek", "Deep Throat", "Lone Gunman", "Gibson Praise"]},
        {"idx": 9, "orig_name": "Young, Matthew", "orig_age": 60, "names": ["Harry Potter", "Ron Weasley", "Draco Malfoy", "Neville Longbottom", "Severus Snape", "Albus Dumbledore", "Rubeus Hagrid", "Sirius Black", "Remus Lupin"]}
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
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            # Handle cases where variation text might be missing in dictionary
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}")
                note_entry["note_text"] = f"Error: Missing variation text for Note {idx}, Style {style_num}"

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
    output_filename = output_dir / "synthetic_thoracoscopy_notes_part_076.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()