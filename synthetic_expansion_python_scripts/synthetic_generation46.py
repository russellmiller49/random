import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_046.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each note index (0-9).
    Styles:
    1. Terse Surgeon
    2. Academic Attending
    3. Billing Coder
    4. Trainee/Resident
    5. Sloppy Dictation
    6. Header-less
    7. Templated
    8. Narrative Flow
    9. Synonym Swapper
    """
    variations = {
        0: { # Note 0: Maria Lopez (Therapeutic Aspiration 31645)
            1: "Indication: Hypoxemia, mucus plugging.\nProc: Therapeutic bronchoscopy.\nFindings: Thick secretions R lung.\nAction: Suctioned R main/RML/RLL. Saline lavage.\nResult: Airways patent. Improved saturations.\nPlan: Wean vent.",
            2: "PROCEDURE NOTE: Bedside Therapeutic Bronchoscopy.\nINDICATION: Acute hypoxemic respiratory failure secondary to severe pneumonia and suspected mucus plugging.\nPROCEDURE: The bronchoscope was introduced via the endotracheal tube. Significant tenacious, purulent secretions were identified obstructing the right bronchial tree. Extensive therapeutic aspiration and saline lavage were performed until the airways were patent. The left lung was relatively clear. \nIMPRESSION: Successful clearance of mucous plugs leading to immediate improvement in ventilator mechanics.",
            3: "Code Selection: 31645 (Therapeutic aspiration of tracheobronchial tree).\nJustification: Procedure performed for initial therapeutic purposes to resolve mucus plugging causing respiratory failure. Extensive suctioning and lavage required to clear right mainstem, RML, and RLL bronchi. No biopsy or diagnostic washing performed.",
            4: "Procedure: Bronchoscopy (ICU)\nResident: Dr. Resident\nAttending: Dr. Holloway\n1. Time out.\n2. Scope down ETT.\n3. R lung full of mucus. Suctioned.\n4. Lavaged with saline.\n5. Cleared RML/RLL.\n6. L lung okay.\n7. Pt tolerated well.",
            5: "bedside bronch for mrs lopez shes clogging up again tube in place went down with the scope tons of thick junk on the right side vacuumed it all out used some saline took a while but got it open left side looked fine no masses or anything just pneumonia improving sats afterwards.",
            6: "Flexible bronchoscopy was performed at the bedside for mucus plugging. The patient was already intubated. Examination revealed copious thick secretions in the right lung. These were aspirated. Saline was instilled to facilitate removal. The right middle and lower lobes were cleared. The left lung was inspected and found to be patent. The patient's respiratory status improved following the intervention.",
            7: "[Indication]\nAcute hypoxemic respiratory failure, mucus plugging.\n[Anesthesia]\nICU Sedation (Propofol/Fentanyl).\n[Description]\nTherapeutic aspiration performed. Large mucus plugs removed from R main/RML/RLL. Lavage utilized. Airways cleared.\n[Plan]\nContinue mechanical ventilation. Monitor secretions.",
            8: "Dr. Holloway performed a bedside bronchoscopy on Ms. Lopez to address her dropping oxygen levels. We passed the scope through her breathing tube and immediately found heavy mucus blocking the right lung. We spent significant time suctioning and washing the area with saline until the breathing tubes were clear. The left side looked much better. Afterward, her ventilator pressures went down, which is a good sign.",
            9: "Intervention: Bronchoscopic airway clearance.\nReason: Compromised oxygenation due to bronchial obstruction.\nTechnique: The endoscope was navigated through the airway. Copious exudate was evacuated from the right hemithorax using suction and lavage. The bronchial lumen was restored. \nOutcome: Improved aeration.",
        },
        1: { # Note 1: Samuel Norris (Stent Revision 31638)
            1: "Indication: Migrated L main stent.\nProc: Stent Revision.\nFindings: Stent proximal migration.\nAction: Grasped w/ forceps, pushed distal. Balloon dilated 12mm.\nResult: Stent re-centered. Good position.\nPlan: Admit.",
            2: "OPERATIVE REPORT: Mr. Norris presented with symptomatic migration of a left mainstem bronchial stent. Under general anesthesia, bronchoscopy revealed the covered metal stent protruding into the distal trachea. The stent was manipulated distally using alligator forceps and repositioned into the appropriate anatomic location. Balloon dilation was performed to ensure apposition to the bronchial wall. The airway is now patent.",
            3: "CPT Code: 31638 (Revision of tracheobronchial stent).\nDetail: Existing stent was manipulated and repositioned (not removed/replaced). Balloon dilation (bundled) used to seat the stent. Fluoroscopy confirmed position. Meets criteria for revision.",
            4: "Procedure: Stent Revision\nPatient: Samuel Norris\n1. ETT 8.0.\n2. Scope inserted.\n3. Stent migrated proximal.\n4. Used forceps/snare to push it back.\n5. Ballooned it (12mm).\n6. Looks good now.\n7. No bleeding.",
            5: "samuel norris his stent moved up into the trachea causing coughing. went in with the scope grabbed the edge of the stent and pushed it back down into the left main where it belongs. dilated it with a balloon so it sticks better. looks fine now no tumor growth just migration.",
            6: "Flexible bronchoscopy performed for stent migration. The previously placed left mainstem stent was found to have migrated proximally. Using grasping instruments the stent was repositioned distally into the correct location. Balloon dilation was performed within the stent. Final inspection showed adequate patency and position. Patient tolerated well.",
            7: "[Indication]\nStent migration LMSB.\n[Anesthesia]\nGeneral.\n[Description]\nVisualization: Stent proximal. Action: Repositioned distal using forceps. Balloon dilation 10-12mm. Position corrected.\n[Plan]\nExtubate. Obs.",
            8: "We took Mr. Norris to the OR to fix his lung stent. It had slipped up into his windpipe. We put him to sleep and used a scope to carefully push the stent back down into the left lung airway where it belongs. We used a balloon to widen it so it stays put. He is breathing better now.",
            9: "Procedure: Repositioning of bronchial prosthesis.\nIndication: Displacement of airway device.\nMethod: The device was mobilized and translocated to the target site using endoscopic tools. Radial expansion was applied to secure the device. \nResult: Restoration of airway architecture.",
        },
        2: { # Note 2: Hannah Keller (Balloon Dilation 31630)
            1: "Indication: Tracheal stenosis.\nProc: Balloon Dilation.\nFindings: 60% subglottic stenosis.\nAction: CRE balloon (8/10/12mm). Serial inflations.\nResult: 80% patency.\nPlan: D/C.",
            2: "PROCEDURE NOTE: Bronchoscopic Dilation of Tracheal Stenosis.\nINDICATION: Symptomatic idiopathic subglottic stenosis.\nFINDINGS: A circumferential stricture was identified in the proximal trachea reducing the lumen by 60%. \nINTERVENTION: Radial dilation was performed using a CRE wire-guided balloon with progressive inflation to 12mm. Post-dilation inspection revealed significant improvement in airway caliber to approximately 80% of normal.",
            3: "Billing: 31630 (Bronchoscopy with dilation of trachea).\nTechnique: Balloon dilation of a single stricture in the trachea. Serial inflations performed. No stent placed. No biopsy performed.",
            4: "Resident Note: Airway Dilation\nPatient: Hannah Keller\n1. ETT 6.5.\n2. Stenosis seen subglottic (60%).\n3. Balloon catheter passed.\n4. Inflated 8mm -> 10mm -> 12mm.\n5. Mucosa split slightly (expected).\n6. Airway much more open now.",
            5: "hannah keller has that tracheal stenosis again hard to breathe. put her to sleep dilated it with the balloon 8 10 then 12 millimeters. opened up nice looks like 80 percent open now little bit of bleeding but stopped. sending her home.",
            6: "Bronchoscopy with balloon dilation performed for idiopathic tracheal stenosis. The stenotic segment was identified and traversed. A CRE balloon was utilized for serial dilations up to 12mm. Post-procedure lumen was significantly improved. Patient extubated and stable.",
            7: "[Indication]\nIdiopathic tracheal stenosis.\n[Anesthesia]\nGeneral.\n[Description]\nStenosis ID'd. CRE Balloon dilation (8-12mm). Patency improved from 40% to 80%.\n[Plan]\nDischarge. F/U ENT.",
            8: "Ms. Keller had her windpipe dilated today. She has a narrowing just below her vocal cords. We used a special balloon that we inflated inside the narrow part to stretch it open. We did this three times with increasing pressure. The airway is much wider now, which should help her breathing.",
            9: "Intervention: Endoscopic tracheal expansion.\nPathology: Subglottic stricture.\nTechnique: Radial force applied via pneumatic dilator. \nOutcome: Luminal enlargement achieved.",
        },
        3: { # Note 3: Jacob Carter (Foreign Body 31635)
            1: "Indication: Aspiration (Peanut).\nProc: Foreign Body Removal.\nFindings: R main/RLL occluded by nuts.\nAction: Basket/Forceps removal piecemeal.\nResult: Airways cleared.\nPlan: CXR, extubate tomorrow.",
            2: "OPERATIVE SUMMARY: Emergent bronchoscopy was performed for acute airway obstruction. Inspection confirmed a foreign body (peanut fragments) occluding the right mainstem bronchus. Using a retrieval basket and forceps, the foreign material was extracted piecemeal. Following removal, the distal airways were inspected and found to be patent and free of residual debris.",
            3: "Code: 31635 (Bronchoscopy with removal of foreign body).\nDetail: Removal of aspirated organic material from Right Mainstem/RLL using basket and forceps. Complexity: Piecemeal removal required.",
            4: "Emergency Bronch Note\nPatient: Jacob Carter\n1. Intubated for aspiration.\n2. Scope down -> Peanut parts in R lung.\n3. Used basket and forceps.\n4. Pulled out multiple pieces.\n5. Suctioned clear.\n6. R lung reinflated.\n7. Done.",
            5: "jacob carter choked on a peanut ems intubated him. right lung down. went in with the scope giant peanut mess in the right main. used the basket and grabbers took a while to get it all out in pieces. cleaned it up nicely lung is up now on xray.",
            6: "Emergency bronchoscopy for foreign body aspiration. The patient presented with right lung collapse. Bronchoscopy revealed peanut fragments obstructing the right mainstem. These were removed using a combination of basket and forceps. The airway was cleared of all visible foreign material. Ventilation improved immediately.",
            7: "[Indication]\nForeign body aspiration, respiratory failure.\n[Anesthesia]\nGeneral (Propofol/Fentanyl).\n[Description]\nFB identified (Peanut) R lung. Removal via basket/forceps. Airways patent post-removal.\n[Plan]\nWean vent. CXR.",
            8: "We performed an emergency procedure on Mr. Carter to remove a peanut he inhaled. It was blocking his right lung. Using a small basket and grippers through the scope, we removed the peanut in several pieces. Once it was all out, we suctioned the airway clean, and his lung re-expanded.",
            9: "Procedure: Retrieval of aspirated foreign material.\nTarget: Right bronchial tree.\nMethod: Extraction utilizing wire basket and forceps.\nOutcome: Restoration of bronchial patency.",
        },
        4: { # Note 4: Linda Reyes (EBUS-TBNA 31652)
            1: "Indication: Mediastinal LAD.\nProc: EBUS-TBNA.\nStations: 7, 11R.\nROSE: Granulomas.\nResult: 2 stations sampled.\nPlan: D/C.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nFINDINGS: The mediastinum was systematically staged. Enlarged lymph nodes were identified at stations 7 (subcarinal) and 11R (right interlobar). TBNA was performed at both stations under real-time ultrasound guidance. Cytopathology suggests a granulomatous process consistent with sarcoidosis.",
            3: "Code: 31652 (EBUS-TBNA, 1-2 stations).\nSpecifics: Sampled Station 7 and Station 11R (Total 2 stations). This qualifies for the base EBUS code 31652, not the multiple station code 31653.",
            4: "EBUS Note\nPatient: Linda Reyes\n1. ETT 8.0.\n2. EBUS scope in.\n3. Station 7: 4 passes -> Granulomas.\n4. Station 11R: 3 passes -> Granulomas.\n5. No other nodes sampled.\n6. Pt stable.",
            5: "linda reyes for ebus checking for sarcoid. lymph nodes looked big at 7 and 11r. poked them with the needle got good samples rose said granulomas. didn't see anything else weird. patient woke up fine going home.",
            6: "Linear EBUS bronchoscopy performed for mediastinal staging. Lymph nodes at station 7 and 11R were identified and sampled via transbronchial needle aspiration. Rapid on-site evaluation showed granulomatous inflammation. No complications occurred.",
            7: "[Indication]\nMediastinal adenopathy, ?Sarcoid.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA Stations 7 & 11R. ROSE: Granulomas.\n[Plan]\nDischarge. Follow-up ILD clinic.",
            8: "Dr. Cole performed an EBUS procedure on Ms. Reyes to investigate her swollen lymph nodes. We used a special ultrasound scope to guide a needle into nodes in the center of her chest and the right side. The preliminary results show granulomas, which points towards sarcoidosis. We sampled two areas total.",
            9: "Procedure: Endosonographic nodal sampling.\nTechnique: Transbronchial needle aspiration under linear ultrasound guidance.\nTargets: Subcarinal and right interlobar nodes.\nPathology: Granulomatous inflammation detected.",
        },
        5: { # Note 5: Danielle Morgan (Bronchial Thermoplasty 31661)
            1: "Indication: Severe Asthma.\nProc: Bronchial Thermoplasty (Session 2/3).\nTarget: RLL, LLL.\nActivations: 92 total.\nComplication: Mild bronchospasm (treated).\nPlan: D/C.",
            2: "OPERATIVE NOTE: Bronchial Thermoplasty, Session 2.\nINDICATION: Refractory asthma.\nPROCEDURE: The lower lobes were targeted for this session. The Alair catheter was deployed systematically in the segmental and subsegmental bronchi of the right and left lower lobes. A total of 92 radiofrequency activations were delivered. The patient tolerated the procedure with only mild, transient bronchospasm managed pharmacologically.",
            3: "Code: 31661 (Bronchial Thermoplasty, 2 or more lobes).\nDetails: Treated RLL and LLL (2 lobes). Total activations: 92. Session 2 of standard protocol.",
            4: "Procedure: BT Session 2\nPatient: Danielle Morgan\n1. General Anesthesia.\n2. Treated RLL (48 hits) and LLL (44 hits).\n3. Total 92 activations.\n4. Pt got wheezy, gave albuterol/solumedrol.\n5. Improved.\n6. Extubated.",
            5: "danielle morgan back for her second thermoplasty session doing the lower lobes today. went smoothly did about 90 burns total in the right and left lower lobes. she got a little tight during the case gave some nebs and steroids she opened up. going home today.",
            6: "Bronchial thermoplasty performed for severe asthma. This was the second of three planned sessions targeting the lower lobes. Radiofrequency energy was delivered to the visible airways of the RLL and LLL. 92 activations total. Procedure complicated by mild bronchospasm which responded to medical therapy.",
            7: "[Indication]\nSevere Asthma.\n[Anesthesia]\nGeneral.\n[Description]\nBronchial Thermoplasty RLL & LLL. 92 Activations. \n[Complications]\nTransient bronchospasm.\n[Plan]\nDischarge. Session 3 in 3 weeks.",
            8: "Ms. Morgan came in for her second bronchial thermoplasty treatment for her asthma. Today we treated the bottom sections of both lungs. We used a special catheter to warm the airway walls to reduce muscle thickness. We did 92 treatments in total. She had a little asthma flare during the procedure but we treated it quickly and she is doing fine now.",
            9: "Intervention: Bronchial thermal remodeling.\nIndication: Refractory reactive airway disease.\nTechnique: Radiofrequency energy application to the distal airways of the lower lobes.\nOutcome: Successful completion of protocol session 2.",
        },
        6: { # Note 6: Anil Patel (Thoracentesis 32555)
            1: "Indication: Pleural effusion (HF).\nProc: US Thoracentesis.\nSite: Left, 8th ICS.\nAmount: 1.3L clear fluid.\nLabs: Sent.\nComplication: None.",
            2: "PROCEDURE NOTE: Ultrasound-Guided Left Thoracentesis.\nINDICATION: Symptomatic pleural effusion refractory to diuretic therapy.\nDESCRIPTION: The largest fluid pocket was localized via bedside ultrasound. Under local anesthesia, a catheter was introduced using Seldinger technique. 1300 mL of serous fluid was drained for symptomatic relief and diagnostic analysis. Post-procedure ultrasound ruled out pneumothorax.",
            3: "Code: 32555 (Thoracentesis with imaging guidance).\nSpecifics: Ultrasound used for localization and real-time guidance (documented). 1.3L removed. No chest tube placed.",
            4: "Procedure: Thoracentesis\nPatient: Anil Patel\n1. Sitting up.\n2. US check: Left effusion.\n3. Prepped/numbed 8th ICS.\n4. Needle in -> fluid -> catheter in.\n5. Drained 1.3L straw fluid.\n6. Pulled catheter.\n7. Bandaged.",
            5: "anil patel fluid on the left lung heart failure. did a tap at the bedside used the ultrasound to find a good spot. drained 1.3 liters of yellow fluid he feels better breathing now. sent fluid to lab no complications.",
            6: "Diagnostic and therapeutic thoracentesis performed on the left hemithorax. Ultrasound guidance utilized. 1300 mL of clear straw-colored fluid evacuated. Catheter removed. Patient tolerated well with improvement in dyspnea.",
            7: "[Indication]\nLeft pleural effusion, symptomatic.\n[Anesthesia]\nLocal (Lidocaine).\n[Description]\nUS-guided thoracentesis. 1.3L removed. Samples sent.\n[Plan]\nMonitor O2. Diuretics.",
            8: "Dr. Simmons performed a procedure to drain fluid from around Mr. Patel's left lung. Using ultrasound to guide the needle, we removed 1.3 liters of fluid. This helped his breathing immediately. We sent the fluid to the lab to make sure there is no infection.",
            9: "Procedure: Ultrasound-guided pleural drainage.\nIndication: Pleural effusion causing dyspnea.\nAction: Percutaneous catheter insertion. Evacuation of 1300mL effusate.\nOutcome: Symptomatic improvement.",
        },
        7: { # Note 7: Thomas Nguyen (Chest Tube 32551)
            1: "Indication: Large PTX.\nProc: Chest Tube (28Fr).\nSite: R 5th ICS.\nResult: Air rush, lung re-expanded.\nPlan: Admit, suction -20.",
            2: "PROCEDURE NOTE: Tube Thoracostomy.\nINDICATION: Primary spontaneous pneumothorax.\nPROCEDURE: The right hemithorax was prepped. Local anesthesia was infiltrated. A 28 French chest tube was inserted via blunt dissection at the 5th intercostal space. Significant air release was confirmed. The tube was secured and placed to suction. Post-procedure imaging confirmed lung re-expansion.",
            3: "Code: 32551 (Tube thoracostomy).\nSpecifics: Open/blunt dissection technique used (not percutaneous/Seldinger). 28Fr tube placed. Connected to suction.",
            4: "Procedure: Chest Tube\nPatient: Thomas Nguyen\n1. Prep R chest.\n2. Lidocaine/Fentanyl.\n3. Cut at 5th ICS.\n4. Clamp dissection into pleura.\n5. Finger sweep.\n6. Tube (28Fr) in.\n7. Stitch and tape.\n8. CXR: Lung up.",
            5: "thomas nguyen young guy spontaneous pneumo right side. pigtail didn't work so put in a real chest tube. 28 french right side 5th intercostal. big rush of air lung came up nicely on the xray. hooked to suction admitting him.",
            6: "Right-sided tube thoracostomy performed for spontaneous pneumothorax. Standard landmark technique utilized. A 28 Fr tube was placed and secured. Connected to -20cmH2O suction with resolution of pneumothorax on imaging.",
            7: "[Indication]\nRight Pneumothorax.\n[Anesthesia]\nLocal + Moderate analgesia.\n[Description]\n28Fr Chest Tube placed R 5th ICS. Air evacuated. Lung re-expanded.\n[Plan]\nAdmit. Suction.",
            8: "We placed a chest tube in Mr. Nguyen's right side to treat his collapsed lung. We numbed the area and inserted a large tube between the ribs. A lot of air came out, and his breathing improved. The X-ray showed the lung is back up. He is admitted to the hospital.",
            9: "Intervention: Tube thoracostomy.\nIndication: Pneumothorax.\nTechnique: Surgical insertion of pleural drain.\nOutcome: Re-expansion of pulmonary parenchyma.",
        },
        8: { # Note 8: Evelyn Sanders (Medical Thoracoscopy 32604)
            1: "Indication: Exudative effusion, nodules.\nProc: Med Thoracoscopy + Biopsy.\nFindings: Diffuse nodules parietal pleura.\nAction: Drained 900cc. 10 biopsies taken.\nResult: No complications. Pigtail removed.\nPlan: Admit.",
            2: "OPERATIVE REPORT: Medical Thoracoscopy.\nINDICATION: Undiagnosed pleural effusion.\nFINDINGS: Visual inspection of the right pleural space revealed diffuse nodularity of the parietal pleura. \nPROCEDURE: The space was accessed via a single port. 900 mL of fluid was evacuated. Multiple forceps biopsies were obtained from the parietal pleura for diagnostic evaluation. The lung was re-expanded and the catheter removed.",
            3: "Code: 32604 (Thoracoscopy with pleural biopsy).\nDetails: Diagnostic inspection + Biopsy of parietal pleura. No talc (32650) or lung biopsy (32609) performed. Catheter was removed at end of case, so no chest tube code.",
            4: "Procedure: Pleuroscopy\nPatient: Evelyn Sanders\n1. Port in R 6th ICS.\n2. Drained 900cc fluid.\n3. Saw nodules everywhere.\n4. Biopsied x10.\n5. Lung expanded.\n6. Pulled tube, closed skin.",
            5: "evelyn sanders fluid on the right lung looks like cancer. did the thoracoscopy looked inside nodules all over the wall. took a bunch of biopsies like 10 of them. drained the fluid out. didn't leave a chest tube just stitched it up. waiting on path.",
            6: "Medical thoracoscopy performed for pleural effusion. Right pleural space accessed. 900cc fluid removed. Parietal pleura showed diffuse studding; multiple biopsies taken. No pleurodesis performed. Catheter removed at conclusion. Patient stable.",
            7: "[Indication]\nPleural effusion, r/o malignancy.\n[Anesthesia]\nModerate Sedation.\n[Description]\nThoracoscopy R chest. Parietal pleura biopsies x10. Fluid drained. No drain left.\n[Plan]\nAdmit. Path pending.",
            8: "Dr. Rahman performed a thoracoscopy on Ms. Sanders. We made a small cut in her side and put a camera into the chest cavity. We drained the fluid and saw many small lumps on the lining of the chest wall. We took samples of these lumps to test for cancer. We didn't need to leave a tube in.",
            9: "Procedure: Diagnostic pleuroscopy with tissue sampling.\nFindings: Diffuse pleural nodularity.\nAction: Evacuation of effusion and biopsy of parietal pleura.\nDisposition: Hospital admission.",
        },
        9: { # Note 9: Teresa Johnson (Nav Bronch 31627)
            1: "Indication: 2 nodules (RUL, RLL).\nProc: Robotic Nav + REBUS + TBBx.\nTargets: RUL post (1.6cm), RLL sup (2.1cm).\nAction: Navigated, confirmed REBUS. Biopsied both.\nResult: Samples obtained.\nPlan: D/C.",
            2: "OPERATIVE NOTE: Robotic Navigational Bronchoscopy.\nINDICATION: Bilateral pulmonary nodules.\nPROCEDURE: A pre-operative CT was utilized for path planning. Using the robotic platform, the bronchoscope was navigated sequentially to the RUL posterior and RLL superior segments. Radial EBUS confirmed lesion location at both sites. Transbronchial biopsies were obtained from both targets without complication.",
            3: "Codes: 31627 (Navigational Bronch), 31654 (REBUS), 31628 (TBBx 1st lobe), 31632 (TBBx addl lobe).\nDetails: Navigation used. REBUS used. Biopsies taken from RUL and RLL (2 separate lobes).",
            4: "Procedure: Robotic Bronch\nPatient: Teresa Johnson\n1. Navigated to RUL nodule -> REBUS confirm -> Biopsy x3.\n2. Navigated to RLL nodule -> REBUS confirm -> Biopsy x4.\n3. Fluoroscopy used.\n4. No pneumo.\n5. Good samples.",
            5: "teresa johnson two spots on the lung right side. used the robot to get out there. found the top one with the ultrasound took some bites. then went to the bottom one found that too took more bites. everything went smooth no bleeding patient went home.",
            6: "Robotic assisted navigational bronchoscopy performed for peripheral pulmonary nodules. Targets in RUL and RLL localized using digital path planning and radial EBUS confirmation. Transbronchial forceps biopsies obtained from both sites. No complications.",
            7: "[Indication]\nLung nodules RUL/RLL.\n[Anesthesia]\nGeneral.\n[Description]\nRobotic Nav to RUL & RLL. REBUS confirmation. Transbronchial biopsies performed x2 lobes.\n[Plan]\nDischarge. CT f/u.",
            8: "Ms. Johnson had a robotic bronchoscopy today to biopsy two spots in her right lung. We used the robot to steer the camera deep into the lung to reach the spots in the upper and lower lobes. We confirmed we were in the right place with ultrasound and took biopsies from both. She did very well.",
            9: "Procedure: Computer-assisted navigational bronchoscopy.\nTargets: RUL and RLL peripheral lesions.\nVerification: Radial endobronchial ultrasound.\nIntervention: Transbronchial biopsy of multiple lobes.\nOutcome: Tissue acquisition successful.",
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data to ensure consistency in generated names/ages for the specific indices 
    aligned with the styles.
    """
    return [
        {"idx": 0, "orig_name": "Maria Lopez", "orig_age": 68, "names": ["Jane Doe", "Margaret H. Thatcher", "Susan Black", "Maria L.", "maria lopez", "Anonymous Female", "Maria Lopez", "Mrs. Lopez", "Subject 781"]},
        {"idx": 1, "orig_name": "Samuel Norris", "orig_age": 63, "names": ["John Smith", "Arthur P. Henderson", "Frank Miller", "Sam N.", "samuel norris", "Anonymous Male", "Samuel Norris", "Mr. Norris", "Subject 442"]},
        {"idx": 2, "orig_name": "Hannah Keller", "orig_age": 47, "names": ["Betty White", "Elena M. Rodriguez", "Jane D.", "Hannah K.", "hannah keller", "Anonymous Female", "Hannah Keller", "Ms. Keller", "Subject 739"]},
        {"idx": 3, "orig_name": "Jacob Carter", "orig_age": 32, "names": ["James Dean", "William T. Riker", "David White", "Jake C.", "jacob carter", "Anonymous Male", "Jacob Carter", "Mr. Carter", "Subject 502"]},
        {"idx": 4, "orig_name": "Linda Reyes", "orig_age": 61, "names": ["Maria Garcia", "Sarah J. Connor", "Patricia Moore", "Linda R.", "linda reyes", "Anonymous Female", "Linda Reyes", "Mrs. Reyes", "Subject 882"]},
        {"idx": 5, "orig_name": "Danielle Morgan", "orig_age": 49, "names": ["Linda Hamilton", "Ripley Alien", "Sarah Connor", "Dani M.", "danielle morgan", "Anonymous Female", "Danielle Morgan", "Ms. Morgan", "Subject 774"]},
        {"idx": 6, "orig_name": "Anil Patel", "orig_age": 73, "names": ["Gary Wilson", "Thomas R. Davies", "Robert Jones", "Anil P.", "anil patel", "Anonymous Male", "Anil Patel", "Mr. Patel", "Subject 660"]},
        {"idx": 7, "orig_name": "Thomas Nguyen", "orig_age": 27, "names": ["Peter Parker", "Bruce Wayne", "Clark Kent", "Tom N.", "thomas nguyen", "Anonymous Male", "Thomas Nguyen", "Mr. Nguyen", "Subject 559"]},
        {"idx": 8, "orig_name": "Evelyn Sanders", "orig_age": 69, "names": ["Judy Dench", "Maggie Smith", "Helen Mirren", "Eve S.", "evelyn sanders", "Anonymous Female", "Evelyn Sanders", "Mrs. Sanders", "Subject 940"]},
        {"idx": 9, "orig_name": "Teresa Johnson", "orig_age": 59, "names": ["Meryl Streep", "Glenn Close", "Sigourney Weaver", "Terry J.", "teresa johnson", "Anonymous Female", "Teresa Johnson", "Ms. Johnson", "Subject 821"]},
    ]

def main():
    # Load original data
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    generated_notes = []
    
    # Process each note
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Create 9 variations
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # 1. Update Note Text
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # 2. Randomize Date (Year 2025 fixed)
            new_date = generate_random_date(2025, 2025).strftime("%Y-%m-%d")
            
            # 3. Randomize Age
            new_age = orig_age + random.randint(-3, 3)
            
            # 4. Update Name/MRN/Metadata
            new_name = record['names'][style_num - 1]
            
            # Update Registry Fields
            if "registry_entry" in note_entry:
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = new_date
                
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"

            # 5. Add Synthetic Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Ensure output directory exists
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    # Save to file
    output_file = output_path / "synthetic_blvr_notes_part_046.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2)
        
    print(f"Generated {len(generated_notes)} notes saved to {output_file}")

if __name__ == "__main__":
    main()