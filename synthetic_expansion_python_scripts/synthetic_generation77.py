import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_077.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock data for the 10 patients in the source file.
    Each entry contains the original name/age and 9 synthetic names for the variations.
    """
    return [
        {"idx": 0, "orig_name": "Jennifer Allen", "orig_age": 55, "names": ["Sarah O'Connor", "Jessica Miller", "Karen Davis", "Emily Clark", "Amanda Wilson", "Betty Hall", "Laura Lewis", "Nancy Walker", "Sandra Robinson"]},
        {"idx": 1, "orig_name": "Sharon Lee", "orig_age": 71, "names": ["Margaret King", "Dorothy Wright", "Helen Scott", "Diane Green", "Martha Adams", "Carol Baker", "Ruth Nelson", "Virginia Carter", "Shirley Mitchell"]},
        {"idx": 2, "orig_name": "Angela Green", "orig_age": 62, "names": ["Brenda Phillips", "Pamela Evans", "Debra Turner", "Janet Torres", "Katherine Parker", "Maria Collins", "Donna Edwards", "Carolyn Stewart", "Christine Flores"]},
        {"idx": 3, "orig_name": "Kevin Allen", "orig_age": 54, "names": ["James Roberts", "John Campbell", "Robert Phillips", "Michael Evans", "William Turner", "David Parker", "Richard Collins", "Joseph Edwards", "Thomas Stewart"]},
        {"idx": 4, "orig_name": "Patricia Taylor", "orig_age": 59, "names": ["Elizabeth Morris", "Linda Rogers", "Barbara Reed", "Susan Cook", "Jennifer Morgan", "Maria Bell", "Margaret Murphy", "Dorothy Bailey", "Lisa Rivera"]},
        {"idx": 5, "orig_name": "Brian Allen", "orig_age": 78, "names": ["Charles Cooper", "Christopher Richardson", "Daniel Cox", "Matthew Howard", "Anthony Ward", "Donald Torres", "Mark Peterson", "Paul Gray", "Steven Ramirez"]},
        {"idx": 6, "orig_name": "Betty Jackson", "orig_age": 50, "names": ["Nancy James", "Karen Watson", "Betty Brooks", "Helen Kelly", "Sandra Sanders", "Donna Price", "Carol Bennett", "Ruth Wood", "Sharon Barnes"]},
        {"idx": 7, "orig_name": "Kathleen Carter", "orig_age": 56, "names": ["Deborah Ross", "Janet Henderson", "Debra Coleman", "Carolyn Jenkins", "Christine Perry", "Brenda Powell", "Pamela Long", "Virginia Patterson", "Martha Hughes"]},
        {"idx": 8, "orig_name": "David Garcia", "orig_age": 68, "names": ["George Flores", "Kenneth Washington", "Andrew Butler", "Edward Simmons", "Joshua Foster", "Brian Gonzales", "Kevin Bryant", "Ronald Alexander", "Timothy Russell"]},
        {"idx": 9, "orig_name": "William Johnson", "orig_age": 66, "names": ["Jason Griffin", "Jeffrey Diaz", "Ryan Hayes", "Jacob Myers", "Gary Ford", "Nicholas Hamilton", "Eric Graham", "Stephen Sullivan", "Larry Wallace"]}
    ]

def get_variations():
    """
    Contains the manually crafted text variations for the 9 styles.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Jennifer Allen (Diagnostic Thoracoscopy - Normal)
            1: "Indication: Mesothelioma susp.\nProcedure: Dx Thoracoscopy. 6th ICS entry.\nFindings: Normal pleura. No nodules. Fluid evacuated.\nAction: 24Fr chest tube placed.\nPlan: Water seal. Path pending.",
            2: "HISTORY: A 55-year-old female presented with unilateral pleural effusion suspicious for malignant mesothelioma.\nPROCEDURE: Medical thoracoscopy was performed under moderate sedation. The pleural space was accessed via the sixth intercostal space. Detailed inspection of the parietal and visceral surfaces revealed normal mesothelial architecture without evidence of gross neoplasia.\nOUTCOME: Complete evacuation of effusion. A thoracostomy tube was secured. The patient was admitted for observation.",
            3: "Service: Diagnostic Medical Thoracoscopy (CPT 32601).\nTechnique: Semi-rigid pleuroscope introduced.\nFindings: Inspection of hemithorax (parietal, visceral, diaphragmatic) performed. No biopsy taken as pleura appeared benign.\nMedical Necessity: Undiagnosed effusion.\nOutcome: Fluid drained, tube placed.",
            4: "Procedure Note\nResident: LT Torres\nAttending: Dr. Garcia\nSteps:\n1. Time out.\n2. Local anesthesia + Mod Sed.\n3. Trocar placed 6th ICS.\n4. Scope inserted. Pleura looked normal.\n5. Fluid drained.\n6. Chest tube placed.\nPlan: Admit.",
            5: "Procedure note for Jennifer Allen doing the diagnostic scope today left side suspected meso. We went in at the 6th intercostal space mild sedation used. Looked around everything looked surprisingly normal no bumps no masses. We sucked out the rest of the fluid put in a chest tube. No air leak really. Sending her to the floor check path in a few days.",
            6: "Medical thoracoscopy (pleuroscopy) diagnostic was performed on a 55-year-old female for suspected mesothelioma. Under moderate sedation and local anesthesia, a single-port entry was established at the 6th intercostal space. The semi-rigid pleuroscope was inserted. Findings included normal-appearing parietal, visceral, and diaphragmatic pleura. All remaining fluid was evacuated under direct visualization. A chest tube was placed. There was no air leak and the lung expanded. Patient admitted to floor.",
            7: "[Indication]\nSuspected mesothelioma, undiagnosed effusion.\n[Anesthesia]\nModerate sedation, local infiltration.\n[Description]\nLeft chest accessed (6th ICS). Pleura visualized; appearance normal. Fluid evacuated. Chest tube placed.\n[Plan]\nAdmit. Water seal. Await cytology.",
            8: "The patient was brought to the endoscopy suite for evaluation of a suspicious left-sided effusion. After achieving adequate sedation, we entered the chest wall at the sixth rib space. Upon inserting the camera, we were relieved to find the lining of the lung and chest wall appeared healthy and smooth, with no obvious signs of cancer. We drained the fluid that was left and secured a drain in place to ensure the lung stays up.",
            9: "Operation: Medical Thoracoscopy - Diagnostic.\nContext: Presumed mesothelioma.\nAction: The pleural cavity was accessed. The pleura was surveyed and deemed normal. Fluid was extracted. A drainage catheter was installed.\nResult: Lung re-expansion confirmed."
        },
        1: { # Sharon Lee (Biopsy + Talc)
            1: "Indication: Lung cancer staging.\nProcedure: Thoracoscopy w/ Biopsy & Talc.\nFindings: Tumor implants visceral pleura.\nActions: 11 biopsies taken. Talc poudrage performed.\nResult: Fluid drained. Chest tube in.\nPlan: Admit.",
            2: "OPERATIVE REPORT: Medical Thoracoscopy with Parietal Pleural Biopsy and Pleurodesis.\nINDICATIONS: Malignant pleural effusion staging.\nINTRAOPERATIVE FINDINGS: Extensive visceral pleural metastasis observed. Eleven biopsy specimens were harvested from the parietal surface for histopathological confirmation. Due to the malignant appearance, chemical pleurodesis was undertaken utilizing sterile talc insufflation.\nCOMPLICATIONS: None. Hemostasis achieved.",
            3: "Codes: 32609 (Thoracoscopy with biopsy); 32650 (Thoracoscopy with pleurodesis).\nRationale: Distinct procedural components performed. Biopsies (x11) obtained from parietal pleura for diagnosis. Separate therapeutic intervention (talc poudrage) performed for effusion management given gross findings.",
            4: "Resident Note: Medical Thoracoscopy\nPatient: Sharon Lee\n1. Trocar entry 6th ICS.\n2. Saw tumor implants on lung.\n3. Took 11 biopsies (parietal).\n4. Sprayed Talc for pleurodesis.\n5. Chest tube placed.\nPatient stable.",
            5: "Note for Sharon Lee doing the scope for staging. Went in left side mod sedation. Yeah there were tumor implants everywhere on the visceral pleura. We grabbed like 11 biopsies from the chest wall side. Decided to do the talc while we were there to stop the fluid coming back. Chest tube in no air leak sending to floor.",
            6: "Medical Thoracoscopy with Pleural Biopsy and Talc Poudrage. Patient is a 71-year-old female. Indication was staging for lung cancer. Under moderate sedation, the left pleural space was accessed. Findings included visceral pleural tumor implants. Multiple biopsies (11) were obtained from the parietal pleura. Talc poudrage was performed for pleurodesis. A chest tube was placed. Hemostasis was confirmed.",
            7: "[Indication]\nLung cancer staging, pleural involvement.\n[Anesthesia]\nModerate sedation.\n[Description]\nVisceral implants visualized. 11 parietal biopsies obtained. Talc poudrage performed. Chest tube placed.\n[Plan]\nAdmit. Suction. Oncology consult.",
            8: "Ms. Lee underwent a procedure to check her lung lining for cancer spread. Using a camera, we inspected the space and unfortunately saw spots on the lung surface consistent with tumor. We took eleven samples from the chest wall for the lab. Because of the fluid buildup, we also sprayed medical talc into the space to seal it up. She is recovering with a tube in place.",
            9: "Procedure: Thoracoscopy with pleural sampling and chemical sclerosis.\nFindings: Visceral pleural deposits.\nAction: Eleven specimens were harvested. Talc was insufflated for symphysis. Fluid was drained.\nDisposition: Inpatient monitoring."
        },
        2: { # Angela Green (Biopsy + Talc)
            1: "Dx: Persistent effusion.\nProc: Thoracoscopy + Bx + Talc.\nFindings: Visceral implants.\nAction: 8 biopsies (parietal). Talc insufflated.\nTube: Placed to suction.\nStatus: Stable.",
            2: "PROCEDURE RECORD: Medical Thoracoscopy.\nINDICATION: Recurrent pleural effusion refractory to thoracentesis.\nOBSERVATIONS: Direct visualization revealed metastatic deposits on the visceral pleura. Biopsies (n=8) were excised from the parietal pleura. To prevent recurrence, talc poudrage was executed. The hemithorax was evacuated and drained.",
            3: "CPT 32609: Biopsy of pleura (8 samples taken).\nCPT 32650: Induction of pleurodesis (Talc).\nJustification: Diagnostic biopsy and therapeutic pleurodesis performed in same session for malignant effusion management.",
            4: "Procedure: Thoracoscopy w/ Biopsy & Talc\nAttending: Dr. Miller\nSteps:\n- Entry 6th ICS.\n- Saw implants on lung.\n- Biopsied parietal pleura x8.\n- Talc poudrage done.\n- Chest tube placed.\nPlan: Suction, wait for path.",
            5: "Angela Green procedure note. Persistent effusion right side. We went in and saw tumor implants on the lung surface. Took 8 biopsies from the wall. Did the talc powder thing to glue it shut. Chest tube is in and verified. No air leak. Patient fine.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Indication persistent effusion. Under moderate sedation, right chest accessed. Findings: Visceral pleural tumor implants. 8 parietal biopsies taken. Talc poudrage performed. Chest tube placed. No air leak. Admitted to floor.",
            7: "[Indication]\nPersistent effusion.\n[Anesthesia]\nModerate.\n[Description]\nVisceral implants found. 8 biopsies taken. Talc pleurodesis performed. Fluid drained.\n[Plan]\nChest tube to suction. Path pending.",
            8: "We performed a scope procedure on Mrs. Green to investigate why her fluid keeps coming back. We saw some abnormal spots on the lung and took eight small samples to test. To stop the fluid, we sprayed talc powder inside the chest cavity. We left a tube in to help the lung expand fully.",
            9: "Operation: Pleuroscopy with tissue sampling and sclerotherapy.\nFindings: Visceral deposits.\nAction: Eight samples retrieved. Talc deposited. Catheter inserted.\nResult: Hemostasis secured."
        },
        3: { # Kevin Allen (Talc only - but note says "nodularity")
            1: "Indication: Exudative effusion.\nProc: Thoracoscopy + Talc.\nFindings: Diffuse nodularity.\nAction: Talc poudrage. Fluid drained. Tube placed.\nPlan: Admit.",
            2: "PROCEDURE: Diagnostic Thoracoscopy with Talc Pleurodesis.\nFINDINGS: Inspection demonstrated diffuse pleural nodularity consistent with diffuse malignancy or inflammation. The decision was made to proceed with pleurodesis via talc insufflation to manage the effusion. Complete drainage was achieved.",
            3: "Code: 32650 (Thoracoscopy with pleurodesis).\nNote: While nodularity was seen, note focuses on talc poudrage application for effusion control. Diagnostic inspection included.",
            4: "Resident Note: Kevin Allen\nIndication: Effusion.\nSteps:\n1. Scope in.\n2. Saw diffuse nodules.\n3. Sprayed Talc.\n4. Drained fluid.\n5. Chest tube in.",
            5: "Procedure for Kevin Allen undiagnosed effusion. Went in left side. Saw a lot of nodules everywhere on the pleura. Did the talc poudrage to treat the fluid. Drained it all out put a chest tube in. Water seal. Done.",
            6: "Medical Thoracoscopy (Pleuroscopy) Diagnostic with Talc Poudrage. 54-year-old male with undiagnosed exudative pleural effusion. Left side. Diffuse pleural nodularity visualized. Talc poudrage performed for pleurodesis. Chest tube placed. Lung expanded.",
            7: "[Indication]\nExudative effusion.\n[Anesthesia]\nModerate.\n[Description]\nDiffuse nodularity seen. Talc poudrage performed. Fluid evacuated.\n[Plan]\nAdmit. Tube to water seal.",
            8: "Mr. Allen underwent a thoracoscopy for his fluid buildup. We saw distinct bumpiness (nodularity) along the lining. We proceeded to treat the fluid buildup by spraying talc into the space. The fluid was drained, and he is resting comfortably.",
            9: "Procedure: Pleuroscopy with chemical sclerosis.\nFindings: Diffuse nodularity.\nAction: Talc insufflated. Fluid extracted. Drain inserted.\nDisposition: Admission."
        },
        4: { # Patricia Taylor (Biopsy only)
            1: "Indication: Susp. malignancy.\nProc: Thoracoscopy + Biopsy.\nFindings: Visceral implants.\nAction: 6 parietal biopsies taken. Fluid drained. Tube placed.\nNote: No talc.",
            2: "OPERATIVE NARRATIVE: Medical Thoracoscopy with Biopsy.\nFINDINGS: Visceral pleural tumor implants were identified. To characterize the pathology, six biopsy specimens were obtained from the parietal pleura. No chemical pleurodesis was performed at this time.\nCONCLUSION: Diagnostic samples obtained; fluid evacuated.",
            3: "CPT: 32609 (Thoracoscopy with biopsy).\nDetail: Biopsies taken from parietal pleura (x6). Visceral implants noted but not biopsied to avoid air leak. No pleurodesis performed.",
            4: "Resident Note: Patricia Taylor\n1. Left chest entry.\n2. Visceral implants seen.\n3. Biopsied parietal pleura (6 pieces).\n4. Drained fluid.\n5. Chest tube placed.\nPlan: Path pending.",
            5: "Note for Patricia Taylor. Suspected cancer. We went in with the scope left side. Saw implants on the lung itself. Took 6 biopsies from the wall instead. Drained the fluid put a tube in. No talc this time.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Indication biopsy-negative suspected malignancy. Left side. Findings: Visceral pleural tumor implants. Multiple biopsies (6) obtained from parietal pleura. Fluid evacuated. Chest tube placed. Hemostasis confirmed.",
            7: "[Indication]\nSusp. malignancy.\n[Anesthesia]\nModerate.\n[Description]\nVisceral implants seen. 6 parietal biopsies. Fluid drained. Tube placed.\n[Plan]\nAdmit. Suction.",
            8: "Ms. Taylor had a scope procedure to investigate suspicious findings. We saw implants on the lung surface. We carefully took six samples from the chest wall lining to figure out what it is. We drained the fluid and placed a tube, but did not use talc today.",
            9: "Operation: Pleuroscopy with tissue sampling.\nFindings: Visceral deposits.\nAction: Six specimens harvested. Fluid extracted. Catheter installed.\nResult: Hemostasis secured."
        },
        5: { # Brian Allen (Biopsy + Talc)
            1: "Indication: Staging.\nProc: Thoracoscopy + Bx + Talc.\nFindings: Inflammatory changes.\nAction: 6 biopsies. Talc poudrage. Tube placed.\nStatus: Stable.",
            2: "PROCEDURE: Medical Thoracoscopy.\nOBSERVATIONS: The pleural surface appeared inflammatory without distinct nodularity. Six biopsies were taken from the parietal pleura for analysis. Talc poudrage was instilled to prevent fluid recurrence.\nOUTCOME: Successful drainage and sclerosis.",
            3: "Codes: 32609 (Bx), 32650 (Talc).\nJustification: Biopsies (x6) taken to rule out occult malignancy despite inflammatory appearance. Talc applied for effusion control.",
            4: "Resident Note: Brian Allen\nRight side staging.\n- Entry 6th ICS.\n- Looks inflammatory, no nodules.\n- Biopsied anyway (6x).\n- Talc sprayed.\n- Chest tube in.",
            5: "Brian Allen procedure note. Staging for lung cancer. Went in right side. Honestly looked mostly inflammatory not really nodular. Still took 6 biopsies to be sure. Did the talc poudrage anyway to stop the fluid. Chest tube in.",
            6: "Medical Thoracoscopy with Pleural Biopsy and Talc. 78M. Indication staging. Right side. Findings: Inflammatory changes without nodularity. 6 biopsies obtained. Talc poudrage performed. Chest tube placed to suction.",
            7: "[Indication]\nStaging.\n[Anesthesia]\nModerate.\n[Description]\nInflammatory changes. 6 biopsies. Talc poudrage. Fluid drained.\n[Plan]\nAdmit. Suction.",
            8: "We performed a procedure on Mr. Allen to stage his condition. The lining looked red and inflamed but didn't have the typical bumps of cancer. We took six samples just to be sure. We also sprayed talc to keep the fluid away. A tube was left in place.",
            9: "Procedure: Pleuroscopy with sampling and sclerosis.\nFindings: Inflammatory appearance.\nAction: Six samples harvested. Talc insufflated. Drain placed.\nResult: Lung re-expanded."
        },
        6: { # Betty Jackson (Biopsy + Talc)
            1: "Indication: Nodularity.\nProc: Thoracoscopy + Bx + Talc.\nFindings: Mass on diaphragm.\nAction: 6 biopsies parietal. Talc poudrage. Tube placed.\nPlan: Admit.",
            2: "OPERATIVE REPORT: Medical Thoracoscopy.\nFINDINGS: A distinct mass lesion was identified on the diaphragmatic pleura. Biopsies (n=6) were obtained from the parietal pleura for safety and diagnosis. Talc pleurodesis was performed.\nCONCLUSION: Diagnostic tissue obtained; therapeutic sclerosis performed.",
            3: "CPT: 32609, 32650.\nDetail: Biopsy of parietal pleura (x6) and separate diaphragmatic inspection showing mass. Talc insufflation for pleurodesis.",
            4: "Resident Note: Betty Jackson\n1. Left entry.\n2. Mass on diaphragm.\n3. Took 6 biopsies from wall.\n4. Talc sprayed.\n5. Tube in.\nStable.",
            5: "Betty Jackson procedure. She had that nodularity on CT. We went in left side. Found a mass right on the diaphragm. Took 6 biopsies from the parietal wall. Sprayed talc to fix the fluid. Chest tube placed no leaks.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Indication pleural nodularity. Left side. Findings: Mass lesion on diaphragmatic pleura. 6 biopsies obtained from parietal pleura. Talc poudrage performed. Fluid drained. Tube to suction.",
            7: "[Indication]\nPleural nodularity.\n[Anesthesia]\nModerate.\n[Description]\nDiaphragmatic mass. 6 parietal biopsies. Talc poudrage. Tube placed.\n[Plan]\nAdmit.",
            8: "Ms. Jackson underwent thoracoscopy to investigate nodules seen on her scan. We found a mass on the diaphragm. We took six samples from the chest wall to test. We then used talc to prevent fluid from coming back and placed a chest tube.",
            9: "Operation: Pleuroscopy with sampling and sclerotherapy.\nFindings: Diaphragmatic mass.\nAction: Six specimens retrieved. Talc deposited. Catheter installed.\nDisposition: Inpatient."
        },
        7: { # Kathleen Carter (Diagnostic - Normal)
            1: "Indication: Undiagnosed effusion.\nProc: Dx Thoracoscopy.\nFindings: Normal pleura.\nAction: Fluid drained. Tube placed. No bx.\nPlan: Water seal.",
            2: "PROCEDURE: Diagnostic Medical Thoracoscopy.\nFINDINGS: Detailed inspection of the right hemithorax revealed normal-appearing parietal and visceral pleura. No biopsies were indicated or performed. The effusion was fully evacuated.\nOUTCOME: Diagnostic inspection complete.",
            3: "Code: 32601 (Diagnostic Thoracoscopy).\nNote: No biopsy (32609) or talc (32650) performed as pleura appeared normal. Purely diagnostic inspection and drainage.",
            4: "Resident Note: Kathleen Carter\nRight side.\n- Scope in.\n- Everything looks normal.\n- Drained fluid.\n- Chest tube placed.\n- No biopsy.",
            5: "Kathleen Carter note. Undiagnosed fluid right side. Went in with the scope. Everything looked totally normal inside. Just drained the fluid and put a tube in. No biopsy needed.",
            6: "Medical Thoracoscopy (Pleuroscopy) - Diagnostic. Indication undiagnosed exudative pleural effusion. Right side. Findings: Normal-appearing pleura. All remaining fluid evacuated. Chest tube placed. No air leak.",
            7: "[Indication]\nUndiagnosed effusion.\n[Anesthesia]\nModerate.\n[Description]\nNormal pleura. Fluid drained. Tube placed.\n[Plan]\nAdmit. Water seal.",
            8: "We took a look inside Mrs. Carter's chest to see why she had fluid. Surprisingly, the lining looked completely healthy. We drained the fluid and put in a temporary tube, but we didn't see anything suspicious enough to biopsy.",
            9: "Procedure: Pleuroscopy - Diagnostic.\nFindings: Normal anatomy.\nAction: Fluid extracted. Drain inserted.\nResult: Lung expanded."
        },
        8: { # David Garcia (Biopsy only)
            1: "Indication: Nodularity.\nProc: Thoracoscopy + Biopsy.\nFindings: Diaphragmatic mass.\nAction: 11 biopsies parietal. No talc.\nTube: Suction.\nPlan: Admit.",
            2: "OPERATIVE NARRATIVE: Medical Thoracoscopy with Biopsy.\nOBSERVATIONS: Inspection revealed a mass lesion on the diaphragmatic surface. Eleven biopsies were harvested from the parietal pleura for histopathologic evaluation. No pleurodesis was performed.\nOUTCOME: Successful sampling.",
            3: "CPT: 32609.\nDetail: Targeted biopsy of parietal pleura (11 samples) in setting of diaphragmatic mass. No pleurodesis code applicable.",
            4: "Resident Note: David Garcia\n1. Right entry.\n2. Mass on diaphragm.\n3. 11 biopsies taken (parietal).\n4. Drained fluid.\n5. Tube in.\nNo talc.",
            5: "David Garcia procedure. Nodules on imaging. Went in right side. Saw the mass on the diaphragm. Took a bunch of biopsies like 11 of them from the wall. Didn't do talc. Chest tube in.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Indication pleural nodularity. Right side. Findings: Mass lesion on diaphragmatic pleura. 11 biopsies obtained from parietal pleura. All fluid evacuated. Chest tube placed. Hemostasis confirmed.",
            7: "[Indication]\nPleural nodularity.\n[Anesthesia]\nModerate.\n[Description]\nDiaphragmatic mass. 11 parietal biopsies. Fluid drained. Tube placed.\n[Plan]\nAdmit.",
            8: "Mr. Garcia had a scope to check on some nodules. We found a mass on the diaphragm. We took eleven samples from the chest wall to send to the lab. We drained the fluid and placed a tube to help the lung heal.",
            9: "Operation: Pleuroscopy with tissue sampling.\nFindings: Diaphragmatic mass.\nAction: Eleven specimens harvested. Fluid extracted. Catheter installed.\nDisposition: Admission."
        },
        9: { # William Johnson (Biopsy + Talc)
            1: "Indication: Susp. malignancy.\nProc: Thoracoscopy + Bx + Talc.\nFindings: Thickened pleura/nodules.\nAction: 12 biopsies. Talc poudrage. Tube placed.",
            2: "PROCEDURE: Medical Thoracoscopy.\nFINDINGS: Significant thickening of the parietal pleura with distinct nodules was observed. Twelve biopsy specimens were obtained. Talc poudrage was subsequently performed for pleurodesis.\nOUTCOME: Tissue secured, pleurodesis complete.",
            3: "CPT: 32609, 32650.\nDetail: Extensive biopsy (n=12) of thickened parietal pleura. Separate therapeutic talc insufflation for effusion management.",
            4: "Resident Note: William Johnson\n1. Right entry.\n2. Thick pleura + nodules.\n3. 12 biopsies taken.\n4. Talc sprayed.\n5. Tube in.",
            5: "William Johnson note. Suspected cancer. Went in right side. Pleura looked thick with nodules. Took 12 biopsies. Sprayed talc to stop the fluid. Tube in and good.",
            6: "Medical Thoracoscopy with Pleural Biopsy. Indication biopsy-negative suspected malignancy. Right side. Findings: Thickened parietal pleura with nodules. 12 biopsies obtained. Talc poudrage performed. Fluid evacuated. Chest tube placed.",
            7: "[Indication]\nSusp. malignancy.\n[Anesthesia]\nModerate.\n[Description]\nThickened pleura, nodules. 12 biopsies. Talc poudrage. Tube placed.\n[Plan]\nAdmit.",
            8: "We performed a procedure on Mr. Johnson to investigate possible cancer. The lining of the chest wall was thick and bumpy. We took twelve samples to be sure we get a diagnosis. We also used talc powder to seal the space and prevent fluid return.",
            9: "Operation: Pleuroscopy with sampling and sclerotherapy.\nFindings: Pleural thickening/nodularity.\nAction: Twelve samples retrieved. Talc deposited. Drain inserted.\nResult: Hemostasis confirmed."
        }
    }
    return variations

def main():
    # Load original data
    source_path = Path(SOURCE_FILE)
    if not source_path.exists():
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return

    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        return

    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")

    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Verify we have enough mock data
    if len(source_data) > len(base_data):
        print(f"Warning: Source has {len(source_data)} entries but mocks only cover {len(base_data)}. Extra notes will be skipped.")

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_notes = []

    # Iterate through each original note
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Determine the procedure date to base random dates around (keep year consistent)
        try:
            orig_date_str = original_note.get("registry_entry", {}).get("procedure_date", "2025-01-01")
            orig_year = int(orig_date_str.split("-")[0])
        except:
            orig_year = 2025

        # Generate 9 variations
        for style_num in range(1, 10):
            # Deep copy to avoid modifying original
            note_entry = copy.deepcopy(original_note)
            
            # New random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # New random date in same year
            rand_date_obj = generate_random_date(orig_year, orig_year)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # New Name
            new_name = record['names'][style_num - 1]
            
            # Update note_text
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing (shouldn't happen with full dictionary)
                note_entry["note_text"] = f"[Style {style_num}] {note_entry.get('note_text', '')}"

            # Update Registry Entry
            if "registry_entry" in note_entry:
                reg = note_entry["registry_entry"]
                reg["patient_age"] = new_age
                reg["procedure_date"] = rand_date_str
                
                # Update MRN to be unique
                if "patient_mrn" in reg:
                    reg["patient_mrn"] = f"{reg['patient_mrn']}_syn_{style_num}"
                
                # We do NOT update names in registry_entry usually as it's often not a field, 
                # but if it were there, we would.
                # However, the note_text definitely contains the name in some styles, 
                # but our pre-written text mostly avoids names or uses the template.
                # *Self-correction*: The pre-written text in get_variations() DOES contain names in Style 5 sometimes.
                # Ideally, we should dynamically replace the name in the text string if it exists.
                # For this specific script, the dictionary `variations_text` already has hardcoded names in Style 5 
                # matching the logic of the prompt's examples. 
                # (Note: In a real dynamic system, we'd use f-strings in the dictionary, but here we hardcoded them).
                
            # Add metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Save output
    output_filename = output_dir / "synthetic_thoracoscopy_notes_part_077.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()