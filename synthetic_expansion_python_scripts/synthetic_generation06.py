import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_006.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for the notes in bronch_notes_part_006.json.
    Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    """
    
    variations = {
        0: { # Note 0: LUL Mass (Navigational Bronchoscopy with Needle, Brush, Forceps)
            1: "Indication: LUL mass.\nAnesthesia: General, LMA.\nAction: Airway inspection normal. Navigational bronchoscopy (SuperDimension) to LUL target using 90-degree catheter. Radial EBUS confirmed concentric view. Samples taken via peripheral needle, standard brush, triple needle brush, and forceps under fluoro. \nOutcome: Adequate samples. Est blood loss <5cc. No complications.",
            2: "OPERATIVE NARRATIVE: The patient was brought to the bronchoscopy suite for evaluation of a left upper lobe pulmonary nodule. Following the induction of general anesthesia and placement of a laryngeal mask airway, a comprehensive airway inspection was performed using an Olympus Q190 bronchoscope, revealing normal anatomy. The diagnostic scope was exchanged for a therapeutic T190 model to facilitate electromagnetic navigation. A SuperDimension navigational catheter (90-degree edge) was successfully guided to the LUL lesion. Radial endobronchial ultrasound (REBUS) confirmed probe placement with a distinct concentric acoustic signature. Diagnostic sampling was rigorously performed utilizing transbronchial needle aspiration, cytology brushing (including triple needle brush), and biopsy forceps. Hemostasis was maintained throughout.",
            3: "Code Justification:\n- Diagnostic Bronchoscopy (31622): Performed initially; airway normal.\n- Navigation (31627): SuperDimension system used to plan and guide access to LUL lesion.\n- Radial EBUS (31654): Utilized to verify concentric probe position within the peripheral lesion.\n- TBNA (31629): Peripheral needle aspiration performed on LUL mass.\n- Brushing (31623): Triple needle brush and standard brush used.\n- Biopsy (31628 - bundled): Forceps biopsies also obtained.\nSummary: Multimodal sampling of a single LUL lesion facilitated by ENB and REBUS.",
            4: "Procedure Note\nAttending: [Attending Name]\nResident: [Resident Name]\n\nProcedure Steps:\n1. Time out/Consent verified.\n2. General anesthesia induced; LMA placed.\n3. Routine inspection with Q190: Normal anatomy.\n4. Navigation phase: SuperDimension catheter advanced to LUL.\n5. Confirmation: Radial EBUS showed concentric view.\n6. Sampling: Needle, Brush, and Forceps biopsies taken under fluoro guidance.\n7. Conclusion: Scope removed. Patient stable.",
            5: "patient came in for lul mass we gave propofol and put in an lma. looked around first everything looked okay no masses in the central airway. switched to the nav scope and used the superdimension stuff to get out to the edge. got a good concentric view on the ultrasound so we knew we were in the right spot. took a bunch of samples with the needle and the brush and the forceps. barely any bleeding maybe 5cc. woke up fine no issues.",
            6: "Indications Left upper lobe mass Medications Propofol infusion via anesthesia assistance Medications General Anesthesia Procedure risks benefits and alternatives were explained to the patient All questions were answered and informed consent was documented as per institutional protocol A history and physical were performed and updated in the pre procedure assessment record Laboratory studies and radiographs were reviewed A time out was performed prior to the intervention Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree the Q190 video bronchoscope was introduced through the mouth via laryngeal mask airway and advanced to the tracheobronchial tree The laryngeal mask airway was in good position The vocal cords appeared normal The subglottic space was normal The trachea was of normal caliber The carina was sharp The tracheobronchial tree was examined to at least the first subsegmental level Bronchial mucosa and anatomy were normal there are no endobronchial lesions We then removed the diagnostic Q190 bronchoscopy and the super dimension navigational catheter was inserted through the T190 therapeutic bronchoscope and advanced into the airway Using navigational map we attempted to advance the 90 degree edge catheter into the proximity of the lesion within the left upper lobe Confirmation of placement once at the point of interest with radial ultrasound showed a concentric view within the lesion Biopsies were then performed with a variety of instruments to include peripheral needle brush triple needle brush and forceps under fluoroscopic visualization After adequate samples were obtained the bronchoscope was removed and the procedure completed Complications No immediate complications Estimated Blood Loss Less than 5 cc",
            7: "[Indication]\nLeft Upper Lobe Mass.\n[Anesthesia]\nGeneral, LMA, Propofol.\n[Description]\nDiagnostic bronchoscopy revealed normal anatomy. Navigational bronchoscopy performed using SuperDimension system. 90-degree catheter navigated to LUL target. Radial EBUS confirmed concentric position. Biopsies obtained using peripheral needle, brush, and forceps.\n[Plan]\nAwait pathology. Discharge home.",
            8: "The patient presented for evaluation of a left upper lobe mass. After obtaining informed consent and inducing general anesthesia with propofol, we placed an LMA. We initially inspected the airway with a Q190 bronchoscope, finding normal anatomy and no endobronchial lesions. We then switched to a T190 therapeutic scope to deploy the SuperDimension navigational system. Using the map, we guided a 90-degree catheter to the target lesion. We confirmed our location with radial EBUS, observing a concentric view. We proceeded to sample the lesion extensively using a peripheral needle, brushes, and forceps under fluoroscopy. The procedure was concluded without complications.",
            9: "Indications: Left upper lobe mass. The Q190 video bronchoscope was inserted through the mouth. The tracheobronchial tree was surveyed. We then withdrew the diagnostic scope and the super-dimension navigational catheter was deployed through the T190 therapeutic bronchoscope. Using the navigational map we guided the 90 degree edge catheter into the proximity of the lesion. Verification of location with radial ultrasound displayed a concentric view. The lesion was sampled with instruments including peripheral needle, brush, and forceps. The bronchoscope was extracted and the procedure finalized."
        },
        1: { # Note 1: LUL Mass + EBUS (11R, 4L)
            1: "Indication: LUL mass.\nProcedure: Bronchoscopy, EBUS, Navigational Biopsy.\nEBUS: Sampled 11Ri, 11Rs, 4L. 21G needle used.\nNavigation: SuperDimension to LUL. 180-degree catheter. REBUS concentric.\nBiopsy: LUL mass biopsied with needle, triple needle brush, forceps.\nComplication: Post-procedure hypoxia, admitted.",
            2: "PROCEDURE SUMMARY: The patient underwent combined endobronchial ultrasound (EBUS) staging and electromagnetic navigational bronchoscopy for a left upper lobe mass. Initially, a diagnostic inspection revealed normal airway anatomy. The EBUS scope (UC180F) was utilized to systematically survey the mediastinum. Lymph node stations 11Ri, 11Rs, and 4L met criteria and were sampled via transbronchial needle aspiration (TBNA) using a 21G needle. Following EBUS, a therapeutic bronchoscope and SuperDimension navigation system (180-degree catheter) were used to locate the peripheral LUL lesion. Radial EBUS confirmed a concentric orientation. The lesion was biopsied using a peripheral needle, triple needle brush, and forceps. Post-procedurally, the patient exhibited mild hypoxia necessitating overnight admission.",
            3: "CPT Coding Analysis:\n- 31652: EBUS-TBNA performed on 2 distinct stations (11R and 4L).\n- 31628: Transbronchial lung biopsy of the LUL mass (separate lesion).\n- 31627: Navigational bronchoscopy used for target planning and guidance.\n- 31654: Radial EBUS used for peripheral lesion confirmation.\nNote: Peripheral TBNA and brushing of the mass are bundled into 31628 per NCCI edits for the same lesion.",
            4: "Resident Procedure Note\nPatient: [Patient Name]\nAttending: [Attending Name]\n\n1. General Anesthesia/Propofol.\n2. Airway inspection: Normal.\n3. EBUS: Sampled stations 11R and 4L with 21G needle.\n4. Navigation: SuperDimension used to reach LUL mass.\n5. Verification: Radial EBUS showed concentric view.\n6. Biopsy: Needle, brush, and forceps used on LUL mass.\n7. Complications: Patient hypoxic in recovery -> Admitted.",
            5: "procedure note for lul mass. we did the airway exam first looked fine. then we did ebus sampled the 11R and 4L nodes sent for cyto. switched to the nav scope used the 180 degree catheter to get to the lul spot. ultrasound looked concentric so we took biopsies with the needle and the brush and forceps. no pneumo on fluoro. patient was a bit low on oxygen after so we are keeping them overnight just to be safe.",
            6: "Indications Left upper lobe mass Medications Propofol infusion via anesthesia assistance Procedure risks benefits and alternatives were explained to the patient Following intravenous medications as per the anesthesia record and topical anesthesia to the upper airway and tracheobronchial tree the Q190 video bronchoscope was introduced through the mouth The vocal cords appeared normal The subglottic space was normal The trachea is of normal caliber The carina was sharp All left and right sided airways were normal without endobronchial disease The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced through the mouth and advanced to the tracheobronchial tree A systematic hilar and mediastinal lymph node survey was carried out Sampling criteria 5mm short axis diameter were met in station 11Ri 50 mm and 11Rs 66 mm Additionally the 4L was 49 mm but slightly hypoechoic and decision was made to sample this node as well Sampling by transbronchial needle aspiration was performed in these lymph nodes using an Olympus Visioshot 2 EBUSTBNA 21 gauge needle All samples were sent for routine cytology We then removed the EBUS bronchoscopy and the super dimension navigational catheter was inserted through the therapeutic bronchoscope and advanced into the airway Using navigational map we advanced the 180 degree edge catheter into the proximity of the lesion within the left upper lobe Confirmation of placement once at the point of interest with radial ultrasound showed a concentric view Biopsies were then performed with a variety of instruments to include peripheral needle triple needle brush and forceps under fluoroscopic visualization After adequate samples were obtained the bronchoscope was removed Fluoroscopic inspection was performed and no pneumothorax was visualized at the conclusion of the procedure",
            7: "[Indication]\nLUL Mass, Staging.\n[Anesthesia]\nDeep Sedation (Propofol).\n[Description]\n1. Diagnostic bronchoscopy: Normal.\n2. EBUS: Sampled stations 11R and 4L (21G needle).\n3. Navigation: LUL lesion located (SuperDimension).\n4. REBUS: Concentric view.\n5. Biopsy: Needle, brush, forceps of LUL mass.\n[Plan]\nAdmit for hypoxia monitoring. Await pathology.",
            8: "We performed a bronchoscopy for a left upper lobe mass. After inducing anesthesia, we inspected the airways and found them normal. We then introduced the EBUS scope and sampled lymph nodes at stations 11R and 4L using a 21-gauge needle. Following this, we utilized the SuperDimension navigation system with a 180-degree catheter to reach the LUL lesion. Radial ultrasound provided a concentric view, confirming our position. We proceeded to biopsy the mass using a peripheral needle, triple needle brush, and forceps. Although there were no immediate operative complications, the patient was admitted for observation due to post-procedure hypoxia.",
            9: "Indications: Left upper lobe mass. The Q190 video bronchoscope was inserted. The airway was examined. The video bronchoscope was withdrawn and the UC180F convex probe EBUS bronchoscope was inserted. Sampling by transbronchial needle aspiration was conducted in lymph nodes 11Ri, 11Rs, and 4L. We then withdrew the EBUS bronchoscopy and the navigational catheter was inserted. Using the map we guided the 180 degree edge catheter into the proximity of the lesion. Verification of placement with radial ultrasound displayed a concentric view. The lesion was sampled with instruments including peripheral needle, triple needle brush and forceps. The bronchoscope was extracted."
        },
        2: { # Note 2: Research Biopsies + EBUS + Nav Failed + TBLB
            1: "Indication: LUL mass.\nProcedures:\n- Research biopsies: RUL, RML, LUL.\n- EBUS: 11R, 7, 11L sampled (22G).\n- Nav: Attempted, failed visualization.\n- LUL Mass: Located via white light/REBUS. Biopsied (needle, forceps) + BAL.\nROSE: Malignancy in LUL mass.\nComplications: None.",
            2: "OPERATIVE REPORT: The patient underwent bronchoscopy for evaluation of a left upper lobe mass. Initial inspection was normal. Per DECAMP protocol, endobronchial biopsies were obtained from the RUL, RML, and LUL for research. EBUS staging was performed, sampling stations 11R, 7, and 11L with a 22G needle. Electromagnetic navigation was attempted using a 45-degree catheter but failed to confirm the target via radial EBUS. The navigational catheter was removed. The lesion was subsequently localized using anatomical landmarks and verified with radial EBUS alone. Transbronchial biopsies and needle aspiration were performed, followed by BAL. ROSE confirmed malignancy. No pneumothorax noted.",
            3: "Billing Summary:\n31653: EBUS-TBNA 3+ stations (11R, 7, 11L).\n31628: Transbronchial biopsy LUL mass (Primary lesion).\n31625: Endobronchial biopsies (Research protocol sites).\n31624: BAL LUL.\n31627: Navigation initiated/attempted.\n31654: Radial EBUS used for confirmation.",
            4: "Procedure Note\nPatient: [Name]\n1. Airway inspection normal.\n2. Research biopsies taken: RUL, RML, LUL.\n3. EBUS performed: Stations 11R, 7, 11L sampled.\n4. Navigation attempted for LUL mass but radial EBUS did not confirm position.\n5. Lesion located via standard scope and radial EBUS.\n6. Biopsies taken (needle, forceps). ROSE positive for cancer.\n7. BAL performed.\n8. Stable.",
            5: "did a bronch for a lul mass. started with the research biopsies in the rul rml and lul. then did ebus hit stations 11r 7 and 11l. tried to use superdimension for the mass but the radial ebus just wouldn't show it so we ditched the nav catheter. found it with the regular scope and radial ebus instead. biopsied it with needle and forceps and did a wash. rose says cancer. no pneumo.",
            6: "Indications Left upper lobe mass Medications Propofol infusion via anesthesia assistance Procedure risks benefits and alternatives were explained to the patient Following intravenous medications as per the anesthesia record and topical anesthesia to the upper airway and tracheobronchial tree the Q190 video bronchoscope was introduced through the mouth The vocal cords appeared normal The subglottic space was normal The trachea is of normal caliber The carina was sharp All left and right sided airways were normal without endobronchial disease Endobronchial brushing was performed at the takeoff of the right upper lobe followed by endobronchial biopsies within the right upper right middle and left upper lobe for research purposes as per standard DECAMP protocol The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced through the mouth and advanced to the tracheobronchial tree A systematic hilar and mediastinal lymph node survey was carried out Sampling criteria 5mm short axis diameter were met in station 11Rs and station 711L lymph nodes Sampling by transbronchial needle aspiration was performed in these lymph nodes using an Olympus EBUSTBNA 22 gauge needle Further details regarding nodal size and number of samples are included in the attached EBUS procedural sheet All samples were sent for routine cytology We then removed the EBUS bronchoscopy and the super dimension navigational catheter was inserted through the therapeutic bronchoscope and advanced into the airway Using navigational map we attempted to advance the 45 degree edge catheter into the proximity of the lesion within the left upper lobe Confirmation of placement once at the point of interest with radial ultrasound failed to confirm location on multiple attempts and we subsequently removed the ENB catheter and were able to locate the lesion based on anatomical knowledge with the white light bronchoscope and confirm target with radial EBUS Biopsies were then performed with a variety of instruments to include peripheral needle and forceps under fluoroscopic visualization followed by BAL of the segment ROSE showed malignancy within the target lesion in the left upper lobe",
            7: "[Indication]\nLUL Mass.\n[Anesthesia]\nGeneral.\n[Description]\nResearch biopsies obtained (RUL, RML, LUL). EBUS staging performed on stations 11R, 7, and 11L. Navigation attempted but unsuccessful. Lesion localized via anatomic landmarks and radial EBUS. Diagnostic biopsies (needle, forceps) and BAL performed. ROSE positive.\n[Plan]\nOncology referral.",
            8: "We brought the patient back for a left upper lobe mass biopsy. After inducing anesthesia, we first performed research-protocol endobronchial biopsies in the RUL, RML, and LUL. We then switched to the EBUS scope and sampled lymph nodes at stations 11R, 7, and 11L. We attempted to use electromagnetic navigation to reach the LUL mass, but could not confirm the location with radial ultrasound. We abandoned the navigation system and successfully located the lesion using the white light bronchoscope and radial EBUS. We took biopsies and a BAL; preliminary results show malignancy.",
            9: "Indications: Left upper lobe mass. Endobronchial brushing was conducted at the right upper lobe takeoff followed by endobronchial biopsies. The video bronchoscope was withdrawn and the EBUS bronchoscope was inserted. Sampling by transbronchial needle aspiration was executed in station 11Rs and station 711L lymph nodes. We then withdrawn the EBUS bronchoscopy and the navigational catheter was inserted. Using the map we attempted to guide the 45 degree edge catheter. Verification of placement failed. We subsequently removed the ENB catheter and located the lesion. The lesion was sampled with peripheral needle and forceps."
        },
        3: { # Note 3: LUL Nodule + EBUS + Failed Stn 5 + Emergency Intubation + Failed Nav
            1: "Indication: LUL nodule.\nEvents:\n- EBUS: Stations 7, 11L sampled (19G).\n- Stn 5 not accessible via EBUS.\n- Complication: Laryngospasm/Loss of IV -> Emergent 8.5 ETT placement.\n- Stn 5: Attempted TBNA via airway/REBUS -> Unrevealing.\n- Nav: Attempted for LUL nodule. Failed to visualize. Procedure aborted.\nStatus: Stable for discharge.",
            2: "PROCEDURE NOTE: The patient presented for evaluation of a left upper lobe nodule. EBUS was performed initially; stations 7 and 11L were sampled using a 19G needle. Transvascular sampling of Station 5 was attempted but aborted due to poor visualization. The EBUS scope was removed. The patient subsequently lost IV access and developed severe laryngospasm, necessitating emergent bronchoscopic intubation with an 8.5 ETT. Once the airway was secured, we attempted to sample Station 5 via a transbronchial approach using radial EBUS; ROSE was negative. We then attempted electromagnetic navigation to the peripheral LUL nodule. Despite multiple attempts, the lesion could not be visualized with radial ultrasound. The procedure was terminated without sampling the peripheral lesion.",
            3: "Billing Codes:\n- 31652: EBUS-TBNA 1-2 stations (7, 11L).\n- 31629-XS: Conventional TBNA of Station 5 (separate site/method).\n- 31627: Navigation initiated/attempted (services rendered despite failure to sample).\nNote: 31654 not billed as peripheral lesion not visualized. Intubation bundled.",
            4: "Resident Note\nPatient: [Name]\n1. EBUS: Sampled 7 and 11L.\n2. Attempted Stn 5 transvascular - failed.\n3. EVENT: Laryngospasm. Emergent intubation (8.5 ETT).\n4. Attempted Stn 5 TBNA via airway - ROSE neg.\n5. Nav attempted to LUL nodule - could not find lesion.\n6. Procedure ended.",
            5: "tried to biopsy a lul nodule. started with ebus hit 7 and 11l. tried station 5 but couldn't see it well. then patient lost iv and had laryngospasm so we had to intubate fast with an 8.5 tube. after that we tried to get station 5 from the airway side but rose was negative. tried to navigate to the lul nodule but radial ebus just wouldn't pick it up so we stopped. no sample from the nodule.",
            6: "Indications Left upper lobe nodule Medications Propofol infusion via anesthesia assistance Procedure risks benefits and alternatives were explained to the patient Following intravenous medications as per the anesthesia record and topical anesthesia to the upper airway and tracheobronchial tree the Q190 video bronchoscope was introduced through the mouth The vocal cords appeared normal The subglottic space was normal The trachea is of normal caliber The carina was sharp All left and right sided airways were normal without endobronchial disease The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced through the mouth and advanced to the tracheobronchial tree A systematic hilar and mediastinal lymph node survey was carried out Sampling criteria 5mm short axis diameter were met in station 7 and 11L Sampling by transbronchial needle aspiration was performed in these lymph nodes using an Olympus Visioshot EBUSTBNA 19 gauge needle All samples were sent for routine cytology We then tried to visualize the FDG avid station 5 lymph node seen on PET CT through the pulmonary artery but were unable to clearly visualize the node and thus could not sample from the mainstem approach transvascular We then removed the EBUS bronchoscopy At this point the patient had lost her IV access and developed laryngospasm prompting us to bronchoscopically intubate the patient with a size 85 ETT which was easily passed through the vocal cords and into the lower trachea before being secured in place The Q190 bronchscope was then advanced using anatomical knowledge into the proximal left upper lobe adjacent to the station 5 lymph node and utilizing radial EBUS attempted to sample this node through an airway approach with a transbronchial needle approach ROSE was unrevealing and we subsequently the super dimension navigational catheter was inserted through the therapeutic bronchoscope and advanced into the airway Using navigational map we advanced the 180 degree edge catheter into the proximity of the lesion within the left upper lobe Confirmation of placement was attempted once we were in the vicinity of the point of interest with radial ultrasound The lesion however could not be adequately visualized Multiple attempts to navigate to the lesion were unfruitful and we subsequently completed the procedure without attempting to sample the left upper lobe peripheral lesion",
            7: "[Indication]\nLUL Nodule, Staging.\n[Complication]\nIntra-operative laryngospasm requiring intubation.\n[Description]\nEBUS sampling of 7 and 11L. Transvascular Stn 5 failed. Emergent intubation. Transbronchial needle of Stn 5 negative. Navigation to LUL nodule attempted but target not visualized.\n[Outcome]\nNegative EBUS. LUL nodule not sampled.",
            8: "The procedure began with EBUS staging for a left upper lobe nodule. We successfully sampled stations 7 and 11L. We attempted to sample Station 5 transvascularly but could not visualize it. The procedure was complicated by the patient losing IV access and developing laryngospasm, requiring immediate bronchoscopic intubation. Once stable, we attempted to sample Station 5 via the airway using radial EBUS, but results were unrevealing. Finally, we attempted electromagnetic navigation to the LUL nodule, but were unable to locate the lesion with radar. The procedure was concluded without a biopsy of the primary nodule.",
            9: "Indications: Left upper lobe nodule. The Q190 video bronchoscope was inserted. The EBUS bronchoscope was inserted. Sampling by transbronchial needle aspiration was conducted in station 7 and 11L. We then attempted to view the FDG avid station 5 lymph node. We then withdrawn the EBUS bronchoscopy. The patient developed laryngospasm prompting us to intubate the patient. The Q190 bronchscope was advanced. We attempted to sample this node. We subsequently inserted the navigational catheter. Using the map we guided the 180 degree edge catheter. Verification of placement was attempted. The lesion could not be visualized. We completed the procedure."
        },
        4: { # Note 4: LUL Tumor + Extensive Staging (N3)
            1: "Indication: LUL Tumor Staging.\nEBUS Findings:\n- Sampled: 11R, 7, 4R, 2R, 11L.\n- 2R/4R: ROSE Positive (Malignant).\n- 11L: Large, 8 passes for molecular/flow.\nDiagnosis: N3 Disease.\nPlan: Oncology.",
            2: "OPERATIVE REPORT: The patient underwent bronchoscopy and EBUS for staging of a left upper lobe tumor. Diagnostic bronchoscopy showed extrinsic compression of the LLL origin. EBUS was used to sample stations 11R, 7, 4R, 2R, 4L, and 11L. Rapid on-site evaluation (ROSE) identified malignant cells in stations 4R and 2R, confirming N3 nodal disease. We then performed extensive sampling (8 passes) of the large 11L node for molecular profiling and flow cytometry. The procedure was uncomplicated.",
            3: "Coding: 31653 (EBUS 3+ stations).\nStations Sampled: 11R, 7, 4R, 2R, 11L (Total 5).\nPathology: Malignancy confirmed in mediastinal nodes (N3).\nTechnique: 22G needle used for all aspirates. Dedicated passes taken for molecular testing.",
            4: "Procedure Note\nPatient: [Name]\n1. Airway Exam: LLL compression.\n2. EBUS Staging: \n   - 11R, 7, 4R, 2R sampled.\n   - ROSE positive at 4R/2R (Contralateral/N3).\n   - 11L sampled x8 for molecular.\n3. Outcome: N3 disease confirmed. No complications.",
            5: "did a staging ebus for a lul tumor. airway looked okay except some compression in the lll. ebus survey found lots of nodes. we stuck 11r 7 4r 2r and 11l. rose said 4r and 2r were cancer so that's n3. got a bunch of extra passes from the big 11l node for the molecular labs. patient did fine minimal bleeding.",
            6: "Indications lung cancer diagnosis and staging left upper lobe tumor Medications General Anesthesia Procedure risks benefits and alternatives were explained to the patient Following intravenous medications as per the record and topical anesthesia to the upper airway and tracheobronchial tree the Q190 video bronchoscope was introduced through the mouth via laryngeal mask airway and advanced to the tracheobronchial tree The laryngeal mask airway was in good position The vocal cords appeared normal The subglottic space was normal The trachea was of normal caliber The carina was sharp The tracheobronchial tree was examined to at least the first sub segmental level Bronchial mucosa and anatomy were normal there are no endobronchial lesions except for in the left lower lobe in which the proximal origin was mildly extrinsically compressed The video bronchoscope was then removed and the UC180F convex probe EBUS bronchoscope was introduced through the mouth via laryngeal mask airway and advanced to the tracheobronchial tree A systematic hilar and mediastinal lymph node survey was carried out Sampling criteria 5mm short axis diameter were met in station 11Rs 67mm 10R 57mm 4R 91mm 2R 71 mm 7 157mm 4L 69mm and 11L 211mm lymph nodes Sampling by transbronchial needle aspiration was performed beginning with the 11Rs Lymph node followed by 7 and 4R 2R lymph nodes using an Olympus EBUSTBNA 22 gauge needle ROSE showed malignant cells in the 4R and 2R station consistent with N3 disease We then moved to the large 11L lymph node and took 8 additional passes for molecular studies All samples were sent for routine cytology and a dedicated pass from the 11L was sent for flow cytometry The Q190 video bronchoscope was then re inserted and after suctioning blood and secretions there was no evidence of active bleeding and the bronchoscope was subsequently removed",
            7: "[Indication]\nLUL Tumor Staging.\n[Anesthesia]\nGeneral.\n[Description]\nDiagnostic bronchoscopy showed LLL compression. EBUS sampling of 11R, 7, 4R, 2R, 11L. ROSE confirmed malignancy in 4R and 2R (N3 disease). Extensive sampling of 11L for ancillary studies.\n[Plan]\nDischarge. Oncology follow-up.",
            8: "The patient underwent general anesthesia for staging of a left upper lobe tumor. Our initial inspection revealed mild extrinsic compression of the left lower lobe. We proceeded with EBUS, identifying and sampling multiple enlarged nodes. We biopsied stations 11R, 7, 4R, and 2R. ROSE analysis confirmed malignancy in the 4R and 2R nodes, indicating N3 disease. We also obtained eight passes from a large 11L node for molecular testing and flow cytometry. The procedure concluded with hemostasis confirmed.",
            9: "Indications: lung cancer diagnosis. The Q190 video bronchoscope was inserted. The tracheobronchial tree was surveyed. The video bronchoscope was withdrawn and the EBUS bronchoscope was inserted. Sampling by transbronchial needle aspiration was executed beginning with the 11Rs Lymph node followed by 7, and 4R, 2R lymph nodes. We then moved to the large 11L lymph node and took 8 additional passes. The Q190 video bronchoscope was re-inserted and the bronchoscope was extracted."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data to assign consistent names and demographics to the 5 records.
    Original file has 'UNKNOWN' for names and dates.
    """
    return [
        {"idx": 0, "orig_name": "James Wilson", "orig_age": 65, "names": ["Robert Smith", "David Johnson", "Michael Williams", "William Brown", "Richard Jones", "Joseph Garcia", "Thomas Miller", "Charles Davis", "Christopher Rodriguez"]},
        {"idx": 1, "orig_name": "Mary Johnson", "orig_age": 70, "names": ["Patricia Martinez", "Linda Hernandez", "Barbara Lopez", "Elizabeth Gonzalez", "Jennifer Wilson", "Maria Anderson", "Susan Thomas", "Margaret Taylor", "Dorothy Moore"]},
        {"idx": 2, "orig_name": "John Smith", "orig_age": 62, "names": ["James Jackson", "John Martin", "Robert Lee", "Michael Perez", "William Thompson", "David White", "Richard Harris", "Joseph Sanchez", "Thomas Clark"]},
        {"idx": 3, "orig_name": "Patricia Williams", "orig_age": 55, "names": ["Sarah Lewis", "Karen Robinson", "Nancy Walker", "Lisa Young", "Betty Allen", "Helen King", "Sandra Wright", "Donna Scott", "Carol Torres"]},
        {"idx": 4, "orig_name": "Michael Brown", "orig_age": 68, "names": ["Daniel Nguyen", "Matthew Hill", "Anthony Flores", "Mark Green", "Donald Adams", "Steven Nelson", "Paul Baker", "Andrew Hall", "Joshua Rivera"]}
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
                continue # Skip if no text
            
            # Update registry_entry/metadata fields if they exist
            # Note: The structure of registry_entry varies in different files.
            # We check for keys before updating.
            
            if "registry_entry" in note_entry and note_entry["registry_entry"]:
                reg = note_entry["registry_entry"]
                
                # Update MRN
                base_mrn = reg.get("patient_mrn", "UNKNOWN")
                if base_mrn is None: base_mrn = "UNKNOWN"
                reg["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
                
                # Update Date
                reg["procedure_date"] = rand_date_str
                
                # Update demographics if present
                if "patient_demographics" in reg and reg["patient_demographics"]:
                    reg["patient_demographics"]["age_years"] = new_age
                    # Assume gender matches name list logic (Male/Female alternating in mock lists essentially)
                    # For simplicity, we keep original gender logic or just age here.
                
                # Some files put age directly in registry_entry (like blvr file)
                if "patient_age" in reg:
                    reg["patient_age"] = new_age

            # Add synthetic metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON
    output_filename = output_dir / "synthetic_bronch_notes_part_006.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()