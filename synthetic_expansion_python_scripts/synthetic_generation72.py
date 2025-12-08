import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_072.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-5) -> Style_Index (1-9) -> Text
    variations = {
        0: { # FB001: Flexible Bronch, Nut removal RML
            1: "Indication: Aspiration/RML collapse.\nProcedure: Flexible bronchoscopy.\nFindings: Pistachio fragment RML medial segment.\nAction: 1.8mm basket deployed. Fragment captured and removed en bloc. Residual piece suctioned.\nOutcome: Airway patent. No bleeding.\nPlan: Discharge.",
            2: "HISTORY: A 32-year-old female presented with unilateral wheeze following organic aspiration. Radiography suggested right middle lobe atelectasis.\nPROCEDURE: Moderate sedation was induced. The tracheobronchial tree was systematically inspected. An organic foreign body, consistent with a nut fragment, was identified obstructing the RML medial segment. Using a flexible retrieval basket, the object was successfully ensnared and extracted. A subsequent pass cleared a minor residual fragment. The mucosa demonstrated localized edema but no active hemorrhage.\nIMPRESSION: Successful bronchoscopic retrieval of organic foreign body.",
            3: "Service: Bronchoscopy with removal of foreign body (CPT 31635).\nTechnique: Flexible video bronchoscope introduced.\nVisualization: Organic foreign body (nut) identified in Right Middle Lobe medial segment.\nRemoval Method: Flexible retrieval basket passed through working channel. Object captured and removed en bloc.\nMedical Necessity: Object caused airway obstruction and lobar collapse.\nStatus: Complete removal achieved.",
            4: "Procedure: Bronchoscopy FB Removal\nPatient: 32F\nAttending: Dr. IP_Attending_01\nSteps:\n1. Time out. Moderate sedation.\n2. Scope inserted orally.\n3. Identified nut fragment in RML medial segment.\n4. Used basket to grab and remove it.\n5. Suctioned small piece.\n6. Re-looked: clear.\nPlan: DC home.",
            5: "patient came in for aspiration 32 yo female we did the scope with midaz and fent went down to the right lung found a pistachio nut in the RML medial part looks like it was stuck used the basket to get it out took two tries to get it all but we got it no bleeding patient did fine going home today.",
            6: "Flexible bronchoscopy with foreign body removal was performed on a 32-year-old female for suspected organic food aspiration with right middle lobe collapse. Moderate sedation with IV midazolam and fentanyl was used. After standard time-out, a flexible video bronchoscope was advanced. In the right middle lobe medial segment bronchus, a tan friable foreign body consistent with pistachio nut fragment was visualized. A 1.8 mm flexible retrieval basket was deployed to capture the fragment. The basket and bronchoscope were withdrawn en bloc. A small residual fragment was removed on a second pass. No additional foreign material was seen. There was mild mucosal erythema without active bleeding.",
            7: "[Indication]\nSuspected organic food aspiration, RML collapse.\n[Anesthesia]\nModerate sedation (Midazolam/Fentanyl).\n[Description]\nScope advanced. Pistachio nut fragment visualized in RML medial segment. Retrieval basket used to capture and remove fragment. Small residual piece suctioned. Airway cleared.\n[Plan]\nDischarge home with return precautions.",
            8: "The patient, a 32-year-old female, presented with a cough after choking on mixed nuts. We proceeded with a flexible bronchoscopy under moderate sedation. Upon inspection, we found a piece of a pistachio nut blocking the medial segment of the right middle lobe. We used a retrieval basket to grab the nut and pulled it out along with the scope. We had to go back down once more to suction up a tiny leftover piece, but after that, the airway was completely clear. There wasn't any significant bleeding, just some redness where the nut had been.",
            9: "Operation: Flexible bronchoscopy with extraction of foreign body.\nReason: Presumed organic food inhalation.\nDetails: A flexible scope was navigated through the mouth. In the RML medial segment, a nut fragment was observed. A flexible retrieval basket was utilized to snare the fragment. The basket and scope were retracted together. A remnant was aspirated on a subsequent pass. No further debris was observed.\nResult: Organic nut fragment eliminated."
        },
        1: { # FB002: Flexible Bronch, Denture removal RLL
            1: "Dx: Denture aspiration.\nAx: Moderate sedation. Flexible bronch.\nFindings: Metal denture clasp RLL basal segment.\nIntervention: Alligator forceps used under fluoro. Clasp grasped and removed.\nResult: Clear airway. Mucosa erythematous.\nPlan: Admit for obs (COPD).",
            2: "INDICATION: The patient, a 68-year-old male with COPD, presented with a history of denture aspiration and focal right lower lobe findings.\nOPERATIVE REPORT: Flexible bronchoscopy was initiated under moderate sedation. Inspection revealed an inorganic, metallic object lodged in the RLL basal segment bronchus. Fluoroscopic guidance was employed to verify the object's orientation. Flexible alligator forceps were utilized to secure the denture clasp, which was then extracted intact. Post-extraction inspection confirmed the absence of residual debris or significant trauma.\nCONCLUSION: Uncomplicated removal of inorganic foreign body.",
            3: "CPT Code: 31635 (Bronchoscopy with removal of foreign body).\nLocation: Right Lower Lobe (Basal Segment).\nObject: Inorganic Foreign Body (Denture fragment).\nTool: Flexible alligator forceps.\nGuidance: Fluoroscopy (included in procedure).\nDetails: Scope advanced to lesion. Forceps deployed to grasp proximal edge. Item removed intact. Airway patent post-procedure.",
            4: "Procedure: FB Removal (Denture)\nPatient: 68M w/ COPD\nSteps:\n1. Sedation (Midaz/Fent).\n2. Scope down. Saw metal clasp in RLL basal segment.\n3. Used alligator forceps to grab it.\n4. Pulled it out under fluoro guidance.\n5. Checked for bleeding - none.\nPlan: Admit for observation.",
            5: "Procedure note for the denture removal patient has copd so we kept him overnight. Used moderate sedation scope went in fine saw the metal clasp in the right lower lobe basal segment. Used the alligator forceps to grab onto it had to use a little fluoro to make sure we had it right. Pulled it out no problem. Rechecked and it looked clear just a little red.",
            6: "Flexible bronchoscopy with foreign body removal. Indication was inorganic foreign body aspiration (denture fragment) with right lower lobe wheeze. 68-year-old male with COPD. Moderate sedation was used. In the right lower lobe basal segment bronchus, a shiny metallic-appearing foreign body consistent with a denture clasp was lodged. Under brief fluoroscopic guidance, a flexible alligator forceps was used to grasp the clasp. The bronchoscope and forceps were withdrawn together with the denture fragment intact. Repeat bronchoscopy confirmed no residual foreign material or bleeding. Inorganic metallic denture fragment completely removed.",
            7: "[Indication]\nDenture aspiration, RLL wheeze.\n[Anesthesia]\nModerate sedation, native airway.\n[Description]\nBronchoscope inserted. Metal denture clasp identified in RLL basal segment. Alligator forceps used to grasp object under fluoroscopy. Object removed intact.\n[Plan]\nAdmit to floor for observation.",
            8: "Mr. Jones swallowed a piece of his denture while lying down, so we brought him in for a bronchoscopy. We found the metal clasp stuck in the bottom part of his right lung. Using alligator forceps and a quick look with the x-ray machine (fluoroscopy) to guide us, we grabbed the edge of the clasp and pulled it out. We checked again to make sure we got it all and didn't cause any bleeding. He's doing fine but we'll keep him overnight because of his COPD.",
            9: "Procedure: Flexible bronchoscopy with retrieval of foreign body.\nIndication: Inorganic material inhalation.\nAction: A video bronchoscope was guided to the RLL basal segment where a metallic denture clasp was lodged. Flexible alligator forceps were employed to clutch the object. The scope and forceps were extracted simultaneously with the fragment. Repeat survey confirmed no remaining material.\nOutcome: Inorganic fragment eliminated."
        },
        2: { # FB003: Rigid Bronch, Coin removal Left Main
            1: "Indication: Coin aspiration, pediatric.\nTechnique: Rigid bronchoscopy, jet ventilation.\nFindings: Coin in left mainstem bronchus.\nAction: Rigid optical forceps used. Coin rotated and removed en bloc.\nOutcome: Minimal abrasion. No bleeding.\nPlan: Peds floor admission.",
            2: "INDICATION: A 5-year-old male presented with acute wheeze following coin ingestion/aspiration.\nPROCEDURE: General anesthesia was induced. A pediatric rigid bronchoscope was introduced, serving as the airway. Examination revealed a metallic foreign body occluding the left mainstem bronchus. Rigid optical grasping forceps were utilized to manipulate and securely grasp the object. The coin was reoriented and extracted through the rigid barrel. The bronchial mucosa exhibited minimal trauma.\nIMPRESSION: Successful rigid bronchoscopic removal of left mainstem foreign body.",
            3: "Procedure: 31635 (Bronchoscopy with removal of foreign body).\nTechnique: Rigid Bronchoscopy (Pediatric).\nTarget: Left Mainstem Bronchus.\nObject: Radiopaque coin.\nInstrumentation: Rigid optical grasping forceps.\nDetails: Visualization of obstruction. Mechanical grasping and rotation of object. En bloc removal. Verification of airway patency.",
            4: "Procedure: Rigid Bronch / FB Removal\nPatient: 5yo Male\nSteps:\n1. GA / Jet ventilation.\n2. Rigid scope inserted.\n3. Found coin in Left Mainstem.\n4. Used rigid forceps to grab and turn the coin.\n5. Pulled it out.\n6. Check for bleeding: minimal abrasion.\nPlan: Admit peds floor.",
            5: "kid swallowed a coin well breathed it in actually 5 years old. took him to the OR for rigid bronchoscopy under general. saw the coin in the left main bronchus tight fit. used the optical forceps took a few tries to get a grip then turned it sideways and pulled it out. airway looks okay little scratch but no bleeding. admit for observation.",
            6: "Rigid bronchoscopy with foreign body removal. Pediatric patient with suspected coin aspiration and unilateral wheeze. General anesthesia with rigid bronchoscope used as the airway. At the left mainstem bronchus, a circular metallic foreign body consistent with a coin was lodged against the bronchial wall. Multiple attempts were required to obtain a secure purchase using rigid optical grasping forceps. The coin was rotated into a favorable orientation and removed en bloc through the rigid bronchoscope. The left bronchial tree was reinspected and was free of additional foreign material.",
            7: "[Indication]\nPediatric coin aspiration, left wheeze.\n[Anesthesia]\nGeneral, Rigid Bronchoscope/Jet Vent.\n[Description]\nRigid scope passed. Coin identified in Left Mainstem Bronchus. Optical forceps used to grasp and rotate coin. Removed en bloc. Minimal mucosal abrasion.\n[Plan]\nPediatric floor observation.",
            8: "This 5-year-old boy inhaled a coin, which got stuck in his left main airway. We put him under general anesthesia and used a rigid metal tube (bronchoscope) to reach the coin. It was tight, but we used special forceps to grab the coin, turn it so it would fit, and pulled it out. We double-checked the airway afterwards and everything looked clear with just a tiny scrape. He's going to the pediatric floor for the night.",
            9: "Operation: Rigid bronchoscopy with extraction of foreign body.\nSubject: 5-year-old male.\nDetails: Under general anesthesia, a rigid scope was inserted. A metallic coin was observed obstructing the left mainstem. Rigid optical forceps were employed to clutch the object. The coin was pivoted and withdrawn en bloc. The bronchial tree was re-examined and found clear.\nResult: Metallic foreign body eliminated."
        },
        3: { # ABL001: Microwave RUL
            1: "Indication: RUL nodule (2.1cm), cancer susp.\nProcedure: Nav bronch + Microwave ablation.\nTarget: Posterior segment RUL.\nGuidance: EMN + Radial EBUS + Cone-beam CT.\nAblation: 65W for 7 mins.\nResult: Ablation zone >5mm margin. No pneumothorax.\nPlan: Admit/Telemetry.",
            2: "INDICATION: Evaluation and treatment of a PET-avid peripheral RUL nodule in a non-surgical candidate.\nPROCEDURE: Electromagnetic navigation was utilized to cannulate the posterior segment of the RUL. Radial EBUS confirmed a concentric lesion signature. Following verification via cone-beam CT, microwave ablation was delivered (65W/7min). Post-procedural imaging confirmed an adequate ablation zone encompassing the target with circumferential margins.\nIMPRESSION: Successful bronchoscopic microwave ablation of RUL malignancy.",
            3: "Codes: 31641 (Destruction of tumor, primary), 31627 (Navigational add-on), 31654 (REBUS add-on).\nTechnique: Electromagnetic Navigation Bronchoscopy (EMN).\nTarget: RUL Posterior Segment Nodule (2.1 cm).\nTherapy: Microwave Ablation (65 Watts, 7 mins).\nVerification: Radial EBUS (concentric) and Cone-Beam CT.\nOutcome: Technical success, adequate margins achieved.",
            4: "Procedure: Nav Bronch / Microwave Ablation\nPatient: 74F\nSteps:\n1. EMN mapping to RUL posterior nodule.\n2. Radial EBUS: concentric view.\n3. CBCT: confirmed tool in lesion.\n4. Microwave catheter in.\n5. Burned at 65W for 7 min.\n6. Post-burn CBCT: good margins.\nPlan: Admit.",
            5: "Procedure note for microwave ablation on the 74 year old lady with the RUL spot. Used the navigation system to get out there radial ebus showed we were right in the middle. Spun the patient for cone beam to double check. Put the microwave probe in and cooked it for 7 minutes at 65 watts. Margins looked good on the scan after. No pneumothorax. sending to floor.",
            6: "Navigational bronchoscopy with microwave ablation of a peripheral right upper lobe nodule. 2.1 cm PET-avid peripheral right upper lobe nodule. General anesthesia with endotracheal tube. Using electromagnetic navigation bronchoscopy, a steerable catheter was guided to a posterior segment right upper lobe peripheral target. Radial EBUS demonstrated a concentric ultrasound signal. After confirming catheter position with cone-beam CT, a microwave ablation catheter was advanced. A single ablation cycle was performed at 65 W for 7 minutes. Post-ablation cone-beam CT demonstrated an ablation zone encompassing the nodule with at least a 5 mm circumferential margin.",
            7: "[Indication]\n2.1 cm RUL nodule, poor surgical candidate.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nEMN guidance to RUL posterior segment. Radial EBUS concentric. Cone-beam CT confirmation. Microwave ablation 65W x 7 min. Margins confirmed via CBCT.\n[Plan]\nOvernight telemetry.",
            8: "This patient has a suspected cancer in her right upper lobe but can't have surgery, so we performed a microwave ablation. We navigated a catheter out to the nodule using electromagnetic guidance. We checked our position with both ultrasound (EBUS) and a specialized CT scan (cone-beam) right in the room. Once we were sure we were in the center of the nodule, we used the microwave catheter to burn the tumor for 7 minutes. The follow-up scan showed we successfully treated the whole nodule with a safe margin around it.",
            9: "Procedure: Navigational bronchoscopy with microwave destruction of a peripheral RUL nodule.\nMethod: Electromagnetic navigation guided a catheter to the posterior segment target. Radial EBUS displayed a concentric signal. Position was validated with cone-beam CT. A microwave ablation catheter was deployed. A single cycle was executed at 65 W for 7 minutes. Post-procedure imaging showed an ablation zone surrounding the nodule."
        },
        4: { # ABL002: RFA RLL
            1: "Indication: RLL Adenocarcinoma (2.0cm).\nProcedure: Nav bronch + RFA.\nTarget: Superior segment RLL.\nGuidance: EMN + Radial EBUS (eccentric) + CBCT.\nAblation: 3 cycles (50W, 5 min each). Temp 105C.\nResult: Good ablation zone. No complications.\nPlan: Admit.",
            2: "INDICATION: Treatment of biopsy-proven adenocarcinoma in the RLL superior segment in a patient with GOLD III COPD.\nPROCEDURE: Following general anesthesia, virtual bronchoscopic navigation facilitated access to the target lesion. Radial EBUS revealed an eccentric orientation. Radiofrequency ablation was selected as the modality. Three overlapping cycles were delivered at 50 Watts/5 minutes, achieving tip temperatures of 105 degrees Celsius. Cone-beam CT verified the extent of the ablation zone.\nIMPRESSION: Successful radiofrequency ablation of RLL malignancy.",
            3: "Coding: 31641 (Tumor destruction), 31627 (Navigation), 31654 (REBUS).\nModality: Radiofrequency Ablation (RFA).\nTarget: Right Lower Lobe Superior Segment (2.0 cm).\nTechnique: Navigation to lesion, EBUS confirmation, RFA catheter deployment.\nDosimetry: 3 cycles x 50W x 5 min.\nOutcome: Ablation zone encompassed nodule on CBCT.",
            4: "Procedure: Nav Bronch / RFA\nPatient: 66M (COPD)\nSteps:\n1. Navigated to RLL superior segment.\n2. EBUS showed eccentric view.\n3. Adjusted and verified with CBCT.\n4. RFA probe inserted.\n5. 3 cycles of burning (50W, 5 min each).\n6. Temps hit 105C.\nPlan: Admit overnight.",
            5: "did an RFA on the guy with the RLL cancer 66 year old. Navigated down there ebus was a bit eccentric but we adjusted. Used the cone beam to confirm. Did three burns with the radiofrequency catheter 50 watts each for 5 mins. Got it nice and hot 105 degrees. Scan after showed we got the whole thing. No bleeding no pneumo.",
            6: "Navigational bronchoscopy with radiofrequency ablation of a peripheral right lower lobe nodule. 2.0 cm peripheral right lower lobe nodule, biopsy-proven adenocarcinoma. General anesthesia with endotracheal tube. A navigation catheter was advanced using CT-based virtual bronchoscopy planning to a superior segment right lower lobe target. Radial EBUS confirmed an eccentric image. A radiofrequency ablation catheter was then advanced. Three overlapping ablation cycles (each 50 W for 5 minutes) were delivered with careful monitoring of impedance and tip temperature. Post-ablation cone-beam CT demonstrated an ablation zone encompassing the nodule.",
            7: "[Indication]\n2.0 cm RLL adenocarcinoma, limited reserve.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nNavigation to RLL superior segment. EBUS eccentric. CBCT confirmation. RFA: 3 cycles, 50W, 5 mins. Max temp 105C. Ablation zone verified.\n[Plan]\nAdmit for observation.",
            8: "We treated this gentleman's lung cancer with radiofrequency ablation (RFA) because his COPD makes surgery too risky. We used a navigation system to guide a catheter down to the tumor in his right lower lobe. Once we confirmed we were in the right spot using ultrasound and a CT scan, we used the RFA probe to heat and destroy the tumor. We did this three times to make sure we got it all. The scan afterwards showed a good burn area covering the tumor.",
            9: "Procedure: Navigational bronchoscopy with radiofrequency destruction of a peripheral RLL nodule.\nDetails: A navigation catheter was guided to the superior segment target. Radial EBUS confirmed an eccentric image. The position was refined and validated. A radiofrequency ablation catheter was deployed. Three overlapping destruction cycles were administered. Post-procedure imaging showed a destruction zone covering the nodule."
        },
        5: { # ABL003: Cryoablation LLL
            1: "Indication: LLL nodule (1.4cm), PET+.\nProcedure: Nav bronch + Cryoablation.\nTarget: Lateral basal segment LLL.\nGuidance: EMN + Radial EBUS (concentric) + CBCT.\nAblation: 3 freeze-thaw cycles (10 min freeze each). Temp -60C.\nResult: Ice ball covered nodule. No pneumothorax.\nPlan: Admit.",
            2: "INDICATION: Ablative therapy for a solitary pulmonary nodule in the LLL lateral basal segment in a post-lobectomy patient.\nPROCEDURE: Navigational bronchoscopy was employed to localize the target. Radial EBUS demonstrated a concentric lesion. Following cone-beam CT verification, a cryoablation probe was deployed. The protocol consisted of three freeze-thaw cycles (10-minute freeze), achieving a nadir temperature of -60 C. Intraprocedural imaging visualized the ice ball extending beyond the tumor margins.\nIMPRESSION: Successful cryoablation of LLL nodule.",
            3: "CPT Justification: 31641 (Tumor destruction via cryo), 31627 (Nav), 31654 (REBUS).\nTechnique: Cryoablation.\nTarget: Left Lower Lobe Lateral Basal Segment (1.4 cm).\nTools: EMN, Radial EBUS, Cryoprobe.\nProtocol: 3 cycles of 10-minute freeze.\nVerification: CBCT visualization of ice ball margins.",
            4: "Procedure: Nav Bronch / Cryoablation\nPatient: 59F\nSteps:\n1. Navigated to LLL lateral basal.\n2. EBUS: Concentric.\n3. CBCT confirmed position.\n4. Cryoprobe in.\n5. 3 cycles: 10 min freeze, passive thaw.\n6. Saw ice ball on scan covering the nodule.\nPlan: Admit.",
            5: "cryoablation for the 59 year old female with the LLL nodule. She had a lobectomy before so saving lung. Navigated to the lateral basal segment ebus was concentric. Confirmed with the cone beam. Used the cryo probe 3 cycles of freezing 10 mins each got down to minus 60. Ice ball looked good on the scan covered the whole thing. No issues.",
            6: "Navigational bronchoscopy with cryoablation of a peripheral left lower lobe nodule. 1.4 cm peripheral left lower lobe pulmonary nodule. General anesthesia with endotracheal tube. Using CT-based navigational bronchoscopy, a steerable catheter was guided to a lateral basal segment left lower lobe target. Radial EBUS confirmed a concentric image. A dedicated endobronchial cryoprobe was advanced. Three freeze–thaw cycles were performed (10-minute freeze followed by passive thaw). Cone-beam CT after the final cycle demonstrated an ice ball encompassing the nodule with appropriate margins.",
            7: "[Indication]\n1.4 cm LLL nodule, prior contralateral lobectomy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nNavigation to LLL lateral basal. EBUS concentric. CBCT confirmation. Cryoablation: 3 cycles x 10 min freeze. Ice ball confirmed on imaging.\n[Plan]\nAdmit for observation.",
            8: "We performed a cryoablation procedure on this patient to freeze her lung nodule. Since she's had lung surgery before, we wanted to preserve as much tissue as possible. We used navigation to guide the probe to the spot in her left lower lobe. Once we confirmed we were in the center using ultrasound and CT, we froze the tumor for three cycles of 10 minutes each. We could see the 'ice ball' on the scan forming around the tumor, ensuring it was fully treated.",
            9: "Procedure: Navigational bronchoscopy with cryo-destruction of a peripheral LLL nodule.\nAction: A steerable catheter was guided to the lateral basal segment target. Radial EBUS confirmed a concentric position. A cryoprobe was inserted. Three freeze–thaw cycles were executed. Cone-beam CT demonstrated an ice ball surrounding the nodule.\nOutcome: Peripheral LLL nodule treated."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages
    return [
        {"idx": 0, "orig_name": "Unknown", "orig_age": 32, "names": ["Jessica Miller", "Ashley Davis", "Sarah Wilson", "Emily Moore", "Amanda Taylor", "Jennifer Anderson", "Melissa Thomas", "Nicole Jackson", "Stephanie White"]},
        {"idx": 1, "orig_name": "Unknown", "orig_age": 68, "names": ["Robert Smith", "James Johnson", "William Williams", "David Brown", "Richard Jones", "Charles Garcia", "Joseph Miller", "Thomas Davis", "Christopher Rodriguez"]},
        {"idx": 2, "orig_name": "Unknown", "orig_age": 5, "names": ["Noah Martinez", "Liam Hernandez", "Mason Lopez", "Jacob Gonzalez", "William Wilson", "Ethan Anderson", "Michael Thomas", "Alexander Taylor", "Daniel Moore"]},
        {"idx": 3, "orig_name": "Unknown", "orig_age": 74, "names": ["Mary Martin", "Patricia Jackson", "Linda Thompson", "Barbara White", "Elizabeth Harris", "Jennifer Sanchez", "Maria Clark", "Susan Ramirez", "Margaret Lewis"]},
        {"idx": 4, "orig_name": "Unknown", "orig_age": 66, "names": ["John Robinson", "Robert Walker", "Michael Young", "William Allen", "David King", "Richard Wright", "Joseph Scott", "Thomas Torres", "Charles Nguyen"]},
        {"idx": 5, "orig_name": "Unknown", "orig_age": 59, "names": ["Lisa Hill", "Nancy Flores", "Karen Green", "Betty Adams", "Helen Nelson", "Sandra Baker", "Donna Hall", "Carol Rivera", "Ruth Campbell"]},
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
            
            # Determine new random age (+/- 3 years, but keep Note 2 pediatric close to 5)
            if orig_age == 5:
                new_age = orig_age + random.randint(-1, 1) # 4-6 years old
            else:
                new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            note_entry["note_text"] = variations_text[idx][style_num]
            
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
    output_filename = output_dir / "synthetic_blvr_notes_part_072.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()