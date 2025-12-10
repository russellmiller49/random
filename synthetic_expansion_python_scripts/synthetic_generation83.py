import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_083.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of pre-written text variations for the 10 notes in Part 083.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
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
        0: { # Michael Brown (Flexible bronch, tracheal granulation, forceps/snare)
            1: "Indication: Tracheal granulation, cough.\nProc: Flex bronch, mechanical debulking.\nActions:\n- Visualization: Mid-trachea circumferential granulation (60% stenosis).\n- Intervention: Forceps removal, snare resection.\n- No thermal/ablation used.\nResult: Lumen improved.\nComplications: None.",
            2: "OPERATIVE NARRATIVE: The patient presented with symptomatic post-tracheostomy sequelae. Upon bronchoscopic evaluation, circumferential mid-tracheal granulation tissue was identified, compromising the airway lumen. A strictly mechanical approach was adopted; the tissue was systematically excised utilizing biopsy forceps for piecemeal debridement and a snare for pedunculated elements. No thermal ablative modalities were employed. Hemostasis was achieved via cold saline lavage.",
            3: "Service Performed: Bronchoscopy with Excision of Tumor/Granulation (CPT 31640).\nMethod: Mechanical debulking.\nTools: Biopsy forceps and snare.\nDetails: The obstructing tissue in the mid-trachea was physically excised. Forceps were used to grasp and remove tissue fragments. A snare was used to amputate the pedunculated portion. This constitutes mechanical excision separate from biopsy.\nMedical Necessity: 60% airway obstruction causing symptoms.",
            4: "Procedure Note\nResident: Dr. Smith\nAttending: Dr. Patel\nIndication: Tracheal granulation.\nSteps:\n1. Moderate sedation.\n2. Airway inspected; 60% narrowing at old trach site.\n3. Forceps used to debulk tissue.\n4. Snare used for larger piece.\n5. Saline for hemostasis.\nPlan: PPI and follow-up.",
            5: "patient michael brown here for cough he has granulation tissue at the old trach site so we did a bronchoscopy under sedation. saw the tissue narrowing the trachea about 60 percent. used forceps to pull it out piece by piece and a snare for the big part just mechanical removal no laser or anything. stopped the bleeding with cold saline patient did fine discharging him home thanks",
            6: "Michael Brown, 70M. Chronic cough and wheeze from tracheal granulation. Flexible bronchoscopy with mechanical debulking performed. Moderate sedation used. Findings included irregular granulation tissue circumferentially at the mid-trachea narrowing lumen to 60%. Multiple passes of forceps debulking were performed to remove tissue. Snare resection used for pedunculated portion. No ablation. Minor oozing controlled. Patient discharged home.",
            7: "[Indication]\nChronic cough, tracheal granulation.\n[Anesthesia]\nModerate sedation (midazolam/fentanyl).\n[Description]\nCircumferential granulation at mid-trachea (60% stenosis). Mechanically debulked using forceps and snare. No thermal therapy. Hemostasis achieved.\n[Plan]\nInhaled steroids, PPI, surveillance in 3 months.",
            8: "The patient arrived for elective bronchoscopy to address chronic cough related to tracheal granulation. Under moderate sedation, we advanced the bronchoscope and visualized the mid-tracheal stenosis. We proceeded to remove the granulation tissue mechanically. Using forceps, we cleared the sessile tissue in a piecemeal fashion, and we used a snare to resect a specific pedunculated area. The airway caliber was significantly improved by the end of the case.",
            9: "Indication: Persistent tussis and wheezing.\nProcedure: Flexible bronchoscopy with physical extraction of tracheal overgrowth.\nFindings: Circumferential tissue obstructing the mid-trachea.\nInterventions: Multiple passes of grasping instruments were performed to extract the tissue. A wire loop was utilized to sever a pedunculated section. No cautery was applied.\nOutcome: Hemostasis secured with chilled saline."
        },
        1: { # Hannah Lee (Rigid bronch, RLL/Bronchus Intermedius tumor, rigid coring)
            1: "Indication: Malignant obstruction BI/RLL.\nAnesthesia: General, Rigid Bronch.\nFindings: 90% obstruction Bronchus Intermedius (BI).\nAction: Rigid coring + forceps debulking.\nResult: Lumen opened to 50-60%. No ablation.\nEBL: 40mL.\nDisp: ICU.",
            2: "HISTORY: Patient with SCLC and RLL collapse.\nPROCEDURE: Rigid bronchoscopy with mechanical tumor debridement.\nFINDINGS: Significant endobronchial tumor burden occluding the bronchus intermedius. The right lower lobe was atelectatic.\nTECHNIQUE: The rigid barrel was utilized to mechanically core through the exophytic mass. Subsequent forceps excision removed residual tumor burden. This mechanical recanalization restored partial patency without the use of thermal energy.",
            3: "CPT 31640: Bronchoscopy with excision of tumor.\nTechnique: Rigid Coring and Forceps Excision.\nSite: Bronchus Intermedius.\nJustification: Patient presented with 90% obstruction. The rigid bronchoscope was used as a coring device to mechanically shear the tumor. Forceps were used to extract the cored fragments. This is distinct from destruction (31641) as the tissue was physically removed/excised.",
            4: "Procedure: Rigid Bronchoscopy / Debulking\nPatient: Hannah Lee\nStaff: Dr. Chang\nSteps:\n1. GA induced. Rigid scope inserted.\n2. Tumor seen in Bronchus Intermedius (90% blocked).\n3. Rigid coring performed to debulk.\n4. Forceps used for cleanup.\n5. Epi used for bleeding.\nDisposition: ICU intubated.",
            5: "Op note for hannah lee she has small cell lung cancer and a blocked lung. took her to the OR for rigid bronch. saw the tumor blocking the bronchus intermedius almost completely. used the rigid scope to core it out and forceps to grab the rest. opened it up to maybe 60 percent. bleeding was a bit moderate used epi and cold saline. kept her intubated for the ICU.",
            6: "Rigid bronchoscopy with mechanical debulking of bronchus intermedius tumor. Patient is a 47-year-old female with malignant obstruction. Bulky endobronchial tumor in the bronchus intermedius with 90% obstruction found. Rigid coring performed with the rigid bronchoscope to mechanically debulk the tumor. Forceps debulking removed remaining fragments. No balloon dilation or thermal ablation used. Hemostasis controlled. Transferred to ICU.",
            7: "[Indication]\nMalignant obstruction of bronchus intermedius, RLL collapse.\n[Anesthesia]\nGeneral, Rigid Bronchoscope.\n[Description]\n90% occlusion of BI. Mechanical debulking via rigid coring and forceps excision. Lumen restored to 60%. No thermal ablation.\n[Plan]\nICU admission, ventilatory support.",
            8: "We performed a rigid bronchoscopy on Ms. Lee to address the collapse of her right lower lobe. Upon inserting the rigid scope, we encountered a large tumor obstructing the bronchus intermedius. We used the beveled tip of the scope to mechanically core through the tumor mass. Following this, large forceps were used to remove the debris. We successfully reopened the airway to about 60% patency without needing any laser or heat therapy.",
            9: "Procedure: Rigid endoscopy with physical reduction of tumor burden.\nIndication: Malignant blockage of the intermediate bronchus.\nAction: The rigid barrel was employed to shear the endobronchial mass. Grasping tools extracted the severed fragments. The airway channel was mechanically widened to approximately 60%.\nHemostasis: Achieved via irrigation and vasoconstrictors."
        },
        2: { # Christopher Adams (Rigid bronch, Distal trachea/carina, rigid coring/snare)
            1: "Dx: Squamous cell CA, distal trachea/carina obstruction.\nProc: Rigid bronch, mechanical debulking.\nTech: Rigid coring + Forceps + Snare.\nNo ablation.\nOutcome: Airway patency improved, mainstems visible.\nPlan: Floor admission.",
            2: "INDICATION: Central airway obstruction involving the distal trachea and carina secondary to squamous cell carcinoma.\nOPERATIVE REPORT: Under general anesthesia, the rigid bronchoscope was introduced. The lesion was found to compromise 75% of the lumen. Mechanical recanalization was achieved utilizing a combination of rigid coring, forceps excision, and snare resection for polypoid components. Hemostasis was maintained. The airway was successfully opened to allow visualization of both mainstem bronchi.",
            3: "Code: 31640 (Excision of tumor).\nLocations: Distal Trachea, Carina.\nMethodology: Mechanical removal only.\n- Rigid scope tip used for coring.\n- Forceps used for extraction.\n- Snare used for amputation.\nNote: No destruction codes (31641) applicable as no ablation was performed.",
            4: "Resident Note: Rigid Bronchoscopy\nIndication: Carinal tumor.\nSteps:\n1. General anesthesia.\n2. Rigid scope to carina.\n3. 75% obstruction seen.\n4. Coring and forceps used to remove tumor.\n5. Snare used for one piece.\n6. Suctioned clear.\nResult: Better airflow.",
            5: "Christopher Adams 62 male with lung cancer blocking his windpipe down low. Did a rigid bronchoscopy today. Tumor was at the carina blocking the right side mostly. We cored it out with the scope and used the grabbers to pull the pieces out. Also used a snare. Didnt use any laser or burning. Bleeding wasn't too bad. Woke him up and sent him to the floor.",
            6: "Rigid bronchoscopy with mechanical debulking of distal tracheal and carinal tumor. Indication was mixed obstructive lesion at distal trachea. Tumor occupying distal trachea and encroaching on carina reducing lumen by 75%. Mechanical debulking performed using rigid coring and forceps. Snare resection used for polypoid component. No ablation used. Final airway patency improved. Extubated and monitored.",
            7: "[Indication]\nDistal tracheal and carinal obstruction (SCC).\n[Anesthesia]\nGeneral, Rigid.\n[Description]\n75% stenosis. Mechanical excision performed using rigid coring, forceps, and snare. No RFA/PDT. Mainstems visualized post-debulking.\n[Plan]\nAdmit to oncology floor.",
            8: "Mr. Adams required urgent airway intervention due to a tumor at his carina. We utilized a rigid bronchoscope under general anesthesia. The tumor was obstructing the distal trachea significantly. We mechanically removed the tissue by coring with the scope and pulling the tissue free with forceps. A snare was also utilized. By the end of the procedure, we had established good airflow to both lungs.",
            9: "Procedure: Rigid airway endoscopy with physical tumor excision.\nFindings: Neoplasm encroaching on the distal windpipe and bifurcation.\nIntervention: The obstruction was physically reduced using the rigid barrel for coring. Grasping instruments and a wire loop were used to extract the mass. No thermal destruction was applied.\nResult: Bilateral mainstem orifices were discernible."
        },
        3: { # Aisha Khan (Flex bronch, RUL tumor, forceps/snare)
            1: "Indication: RUL collapse, tumor.\nProc: Flex bronch, mechanical debulking.\nTools: Forceps, Snare.\nFindings: 80% obstruction RUL bronchus.\nAction: Piecemeal excision.\nNo thermal modalities.\nResult: RUL patent.",
            2: "PROCEDURE: Flexible bronchoscopy with mechanical excision of endobronchial neoplasm.\nCLINICAL CONTEXT: Patient with persistent RUL atelectasis.\nFINDINGS: A polypoid lesion was visualized occluding the right upper lobe orifice. \nINTERVENTION: Using a therapeutic flexible bronchoscope, the lesion was resected using a combination of biopsy forceps and electrosurgical snare (mechanical cutting). The tumor was removed in piecemeal fashion until the lobar orifice was patent. No vaporizing or coagulating ablation was performed.",
            3: "Billing: 31640 (Bronchoscopy with excision of tumor).\n- Target: Right Upper Lobe Bronchus.\n- Technique: Snare resection and forceps debulking.\n- Documentation confirms removal of tissue, not just biopsy.\n- No thermal ablation codes (31641) utilized.",
            4: "Procedure: RUL Tumor Debulking\nPatient: Aisha Khan\nSteps:\n1. LMA placed. Propofol sedation.\n2. Scope to RUL.\n3. Polypoid tumor seen.\n4. Snared the tumor and removed pieces with forceps.\n5. RUL opened up.\n6. Minimal bleeding.\nPlan: CT in 6 weeks.",
            5: "Procedure note for Aisha Khan she has that collapsed right upper lobe from a tumor. Went in with the flexible scope through an LMA. Found the tumor blocking the RUL almost totally. Used the snare to cut it and forceps to clear it out. Did not use the laser or APC. Just mechanical removal. Bleeding stopped with saline. She went home fine.",
            6: "Flexible bronchoscopy with mechanical debulking of RUL tumor. Patient is 59F with persistent collapse of RUL. Polypoid tumor at origin of RUL bronchus causing 80% obstruction found. Mechanical debulking performed using forceps and snare resection. Tumor removed in piecemeal fashion until RUL bronchus was widely patent. No thermal techniques used. Discharged home.",
            7: "[Indication]\nRUL collapse, endobronchial tumor.\n[Anesthesia]\nModerate sedation, LMA.\n[Description]\n80% obstruction RUL. Mechanical excision via snare and forceps. No APC/Laser. RUL patent.\n[Plan]\nDischarge, follow-up CT 6 weeks.",
            8: "Ms. Khan presented with a collapsed lung lobe due to a tumor blockage. We performed a flexible bronchoscopy to clear the airway. Upon reaching the right upper lobe, we found the tumor blocking the entrance. We used a snare to loop around the tumor and cut it, and forceps to pull the pieces out. We continued this until the airway was open again. No heat therapy was needed.",
            9: "Procedure: Flexible endoscopy with physical resection of RUL mass.\nFindings: Exophytic growth obstructing the RUL orifice.\nAction: The mass was excised using a wire loop and grasping tools. The growth was extracted piecemeal. No thermal destruction was utilized.\nResult: The lobar entrance was patent."
        },
        4: { # Robert Wilson (Rigid bronch, Carina/Right Main, coring/microdebrider)
            1: "Indication: Severe dyspnea, Carinal/RMS tumor.\nProc: Rigid bronch, mechanical debulking.\nTools: Rigid coring, Forceps, Microdebrider.\nResult: 50% patency achieved. No thermal ablation.\nComplication: Transient desat -> recovered.\nDisp: ICU.",
            2: "OPERATIVE REPORT: Rigid bronchoscopy for central airway obstruction.\nINDICATION: NSCLC with carinal involvement.\ntechnique: Under general anesthesia, the rigid bronchoscope was engaged to mechanically core the tumor at the carina and right mainstem. Following gross debulking with forceps, a microdebrider blade was employed to shave and contour the residual tumor base. This was a strictly mechanical intervention.\nOUTCOME: Airway caliber improved from 15% to 50%.",
            3: "CPT 31640: Excision of tumor.\nDevice(s): Rigid bronchoscope (coring), Microdebrider (shaving/excision), Forceps.\nAnatomy: Carina and Right Mainstem Bronchus.\nNote: Microdebrider acts as a mechanical cutting tool, supporting code 31640. No laser/APC used.",
            4: "Procedure: Rigid Debulking\nAttending: Dr. Li\nSteps:\n1. Patient intubated with rigid scope.\n2. Big tumor at carina/right main.\n3. Used scope to core it out.\n4. Used microdebrider to clean it up.\n5. Bleeding controlled with epi.\nEvents: SpO2 dropped to 90 briefly.\nPlan: ICU.",
            5: "Robert Wilson 73 male with bad lung cancer blocking the main airway. Did a rigid bronch today. Tumor was huge at the carina and right mainstem. We cored through it with the rigid tube and used the microdebrider to shave it down. No burning used just cutting. He desatted for a minute but came back up. Leaving him intubated for the ICU.",
            6: "Rigid bronchoscopy with mechanical debulking of carinal/right mainstem tumor. Severe dyspnea from NSCLC. Tumor occupying right side of carina and proximal right mainstem with 85% obstruction. Mechanical debulking with rigid coring and forceps performed. Microdebrider used to smooth tumor base. Debulking was entirely mechanical. Transient desaturation resolved. Admitted to ICU.",
            7: "[Indication]\nCarinal/RMS obstruction, NSCLC.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\n85% obstruction. Rigid coring, forceps, and microdebrider used for mechanical excision. No thermal ablation. Patency improved to 50%.\n[Plan]\nICU admission.",
            8: "We took Mr. Wilson to the OR for a rigid bronchoscopy to help him breathe. The cancer was blocking his right main airway and the carina. We used the rigid scope to mechanically core out the center of the tumor. Then, we used a microdebrider tool to shave away the remaining tissue and smooth the airway walls. We managed to open the airway significantly without using any heat ablation.",
            9: "Indication: Critical airway stenosis.\nProcedure: Rigid endoscopy with physical debridement.\nIntervention: The rigid barrel was used to shear the tumor mass. A micro-debriding instrument was employed to excise residual tissue. No thermal energy was applied.\nResult: Significant luminal restoration."
        },
        5: { # Emily Garcia (Flex bronch, LLL tumor, forceps/snare)
            1: "Indication: Recurrent pneumonia LLL, tumor.\nProc: Flex bronch (31640).\nAction: Forceps debulking, snare resection.\nFindings: 75% LLL obstruction.\nNo thermal modalities.\nResult: Improved patency.",
            2: "PROCEDURE: Therapeutic bronchoscopy for malignant airway obstruction.\nINDICATION: Post-obstructive pneumonia, LLL.\nFINDINGS: An exophytic lesion was identified occluding the left lower lobe bronchus.\nINTERVENTION: Mechanical recanalization was performed. The tumor was resected using a polypectomy snare and biopsy forceps. Purulent secretions were lavaged. No cryotherapy or thermal ablation was utilized.",
            3: "Code Selection: 31640.\nRationale: Procedure involved mechanical removal of tumor tissue causing obstruction.\nInstruments: Snare and Forceps.\nSite: Left Lower Lobe Bronchus.\nNote: Exclusion of thermal/cryo methods confirms 31640 over 31641.",
            4: "Procedure: LLL Debulking\nPatient: Emily Garcia\nSteps:\n1. Propofol sedation.\n2. Scope down. LLL blocked by mass.\n3. Suctioned pus.\n4. Snared the mass.\n5. Picked out pieces with forceps.\n6. No complications.\nPlan: Antibiotics and follow-up.",
            5: "Emily Garcia is here for the LLL mass causing pneumonia. Did the bronch with an LMA. Saw the tumor blocking the LLL about 75 percent. Used a snare to cut it off and forceps to clean it up. Sucked out a lot of pus too. Didn't use any fancy ablation just mechanical tools. Bleeding was minimal. Sending her home with antibiotics.",
            6: "Flexible bronchoscopy with mechanical debulking of LLL endobronchial tumor. Indication was recurrent post-obstructive pneumonia. Exophytic lesion at origin of LLL bronchus with 75% obstruction found. Forceps debulking and snare resection used to mechanically debulk and excise tumor. No cryotherapy or thermal techniques used. Discharged home with antibiotics.",
            7: "[Indication]\nPost-obstructive pneumonia, LLL tumor.\n[Anesthesia]\nModerate sedation.\n[Description]\n75% LLL stenosis. Snare resection and forceps debulking performed. Secretions cleared. No ablation.\n[Plan]\nAntibiotics, follow-up 3 months.",
            8: "Ms. Garcia has been suffering from pneumonia due to a tumor blocking her lower left lung. We performed a bronchoscopy to clear the blockage. We found the tumor and used a snare loop to cut it away, followed by forceps to remove the pieces. We also washed out the infection behind the blockage. The airway is now open.",
            9: "Procedure: Flexible endoscopy with physical excision of LLL neoplasm.\nFindings: Obstructive growth in the basal airway.\nAction: The growth was resected using a wire loop and grasping instruments. Purulence was aspirated. No thermal or cryo-ablation was employed.\nOutcome: LLL orifice patent."
        },
        6: { # Steven Park (Rigid bronch, Distal trachea, rigid coring/microdebrider)
            1: "Indication: Critical distal tracheal obstruction (SCC).\nProc: Rigid bronch, mechanical debulking.\nTech: Rigid coring, forceps, microdebrider.\nFindings: Pinpoint lumen.\nAction: Mechanical excision only. No ablation.\nComplication: Desat to 80s -> resolved.\nDisp: ICU.",
            2: "OPERATIVE SUMMARY: Emergent rigid bronchoscopy for critical airway stenosis.\nFINDINGS: Near-total occlusion of the distal trachea by squamous cell carcinoma.\nPROCEDURE: Mechanical debulking was initiated using the bevel of the rigid bronchoscope for coring. Residual mural tumor was excised utilizing a microdebrider to restore lumen geometry. No thermal ablation was applied due to the critical nature of the airway and efficacy of mechanical removal.",
            3: "CPT: 31640 (Tumor excision).\nJustification: Use of rigid coring and microdebrider constitutes mechanical excision.\nAnatomy: Distal Trachea.\nComplexity: Critical obstruction requiring general anesthesia and rigid instrumentation.\nExclusions: No laser or cryotherapy utilized.",
            4: "Procedure: Emergency Rigid Bronch\nPatient: Steven Park\nSteps:\n1. GA. Rigid scope inserted.\n2. Distal trachea almost closed off.\n3. Cored through with scope.\n4. Used microdebrider to widen it.\n5. Pulled out pieces with forceps.\n6. Sats dropped but came back up.\nPlan: ICU intubated.",
            5: "Steven Park 60M with critical airway blockage. Taking him to OR for rigid. Tumor was choking off the distal trachea. We rammed the rigid scope through to core it out then used the microdebrider to clean the walls. Just mechanical work no burning. He desatted a bit during the coring but is okay now. ICU admission.",
            6: "Rigid bronchoscopy with mechanical debulking of distal tracheal tumor. Critical distal tracheal obstruction from bulky squamous cell carcinoma. Nearly occlusive exophytic tumor found. Rigid coring performed repeatedly through tumor. Microdebrider used to further debulk residual tumor. Debulking was entirely mechanical with explicit tumor excision. Moderate bleeding controlled. Admitted to ICU.",
            7: "[Indication]\nCritical distal tracheal stenosis, SCC.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\nPinpoint lumen. Mechanical recanalization via rigid coring and microdebrider. Forceps removal of debris. No ablation.\n[Plan]\nICU, ventilatory support.",
            8: "Mr. Park was in critical condition with a tumor nearly closing off his windpipe. We performed an emergency rigid bronchoscopy. We used the metal tube of the scope to mechanically core a path through the tumor. We then used a shaving tool called a microdebrider to widen the opening further. We successfully restored the airway without using laser or heat, though his oxygen levels dipped briefly during the procedure.",
            9: "Procedure: Rigid airway endoscopy with physical tumor reduction.\nIndication: Impending airway closure.\nIntervention: The rigid instrument was used to shear the obstructive mass. A rotating blade instrument (microdebrider) excised the remaining tissue. No thermal devices were used.\nResult: Lumen patency restored."
        },
        7: { # Laura Perez (Flex bronch, benign stenosis, forceps/snare)
            1: "Indication: Benign tracheal stenosis.\nProc: Flex bronch, mechanical debulking.\nFindings: 65% stenosis mid-trachea (scar/granulation).\nAction: Forceps removal, snare of fibrotic ridge.\nNo balloon, no ablation.\nResult: Mild residual narrowing.",
            2: "PROCEDURE: Bronchoscopic management of benign tracheal stenosis.\nFINDINGS: Post-intubation scarring and granulation tissue narrowing the mid-trachea.\nTECHNIQUE: Mechanical excision was performed. Granulation tissue was avulsed using biopsy forceps. A distinct fibrotic ridge was resected using an electrosurgical snare. No balloon dilation or thermal ablation was required to achieve satisfactory patency.",
            3: "Billing Code: 31640.\nDiagnosis: Benign Tracheal Stenosis.\nTechnique: Excision of tracheal tissue (scar/granulation) using forceps and snare.\nNote: This is coded as excision (31640) rather than dilation (31630) or ablation (31641) because the primary method was removal of tissue.",
            4: "Procedure: Tracheal Debulking\nPatient: Laura Perez\nSteps:\n1. Moderate sedation.\n2. Scope inserted.\n3. Scar tissue seen in trachea.\n4. Used forceps to grab granulation.\n5. Snared a ridge of scar.\n6. Airway looks better.\nPlan: Home.",
            5: "Laura Perez here for that tracheal scar from her breathing tube last year. Went in with the flex scope. Saw the narrowing about 65 percent. Used forceps to pick away the granulation and a snare to cut the scar band. Didn't use a balloon this time just mechanical removal. Bleeding was minimal. She can go home.",
            6: "Flexible bronchoscopy with mechanical debulking of granulation tissue and scar. Benign post-intubation tracheal stenosis. Short-segment circumferential granulation in mid-trachea narrowing lumen by 65%. Mechanical debulking done with forceps to remove granulation tissue. Snare resection of fibrotic ridge. No balloon dilation or ablation. Tracheal lumen improved.",
            7: "[Indication]\nBenign tracheal stenosis, dyspnea.\n[Anesthesia]\nModerate sedation.\n[Description]\n65% mid-tracheal narrowing. Mechanical excision using forceps and snare. No balloon/ablation.\n[Plan]\nDischarge, monitor for restenosis.",
            8: "Ms. Perez has scarring in her trachea from a previous intubation. We went in with a bronchoscope and found the scar tissue narrowing her airway. We used small forceps to remove the granulation tissue and a snare loop to cut away a ridge of scar. We didn't need to stretch it with a balloon or burn it; simple mechanical removal opened it up nicely.",
            9: "Procedure: Flexible endoscopy with physical excision of cicatrix.\nIndication: Benign airway constriction.\nAction: Granulation tissue was extracted via grasping tools. A fibrotic band was resected with a wire loop. Neither dilation nor thermal ablation was utilized.\nResult: Lumen caliber improved."
        },
        8: { # Daniel Scott (Rigid bronch, Left Mainstem, rigid coring/forceps)
            1: "Indication: LMS obstruction (NSCLC).\nProc: Rigid bronch, mechanical debulking.\nFindings: 85% obstruction LMS.\nAction: Rigid coring + forceps excision.\nNo ablation/balloon.\nResult: Moderate residual narrowing, lobar orifices visible.\nEBL: 40mL.",
            2: "OPERATIVE NOTE: Rigid bronchoscopy for malignant left mainstem obstruction.\nFINDINGS: Friable tumor burden occluding the left mainstem bronchus.\nINTERVENTION: The rigid bronchoscope was utilized to mechanically core the central aspect of the tumor. Forceps were employed to excise the remaining peripheral tumor burden. This mechanical debridement successfully restored visualization of the distal lobar takeoffs without the use of adjuvant thermal therapy.",
            3: "CPT 31640: Bronchoscopy with tumor excision.\nSite: Left Mainstem Bronchus.\nTechnique: Rigid coring and forceps removal.\nMedical Necessity: 85% obstruction causing symptoms.\nExclusions: No destruction (31641) or stent (31636) performed.",
            4: "Procedure: Left Main Debulking\nPatient: Daniel Scott\nSteps:\n1. GA / Rigid Scope.\n2. Left main is 85% blocked.\n3. Cored it out with the scope.\n4. Grabbed pieces with forceps.\n5. Can see lobes now.\n6. Bleeding stopped with cold saline.\nDisposition: Floor.",
            5: "Daniel Scott 68M has a tumor in the left main bronchus. Did a rigid bronch. Tumor was friable and blocking most of the airway. We used the rigid scope to cut through it and forceps to clean it out. Mechanical removal only no burning. Opened it up enough to see the lobes. Admitted him to oncology.",
            6: "Rigid bronchoscopy with mechanical debulking of left mainstem tumor. Central obstruction of left mainstem from non–small cell lung cancer. Friable tumor filling 85% of left mainstem lumen found. Rigid coring and forceps debulking used to mechanically debulk and excise obstructing tumor. No ablation or balloon dilation performed. Lumen improved to moderate residual narrowing.",
            7: "[Indication]\nLMS obstruction, NSCLC.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\n85% obstruction. Mechanical excision via rigid coring and forceps. No ablation. Lobar orifices visualized.\n[Plan]\nAdmit to floor.",
            8: "Mr. Scott had a tumor blocking his left main airway. We used a rigid bronchoscope to fix this. We physically cored out the tumor using the end of the scope and used forceps to remove the pieces. We didn't use any lasers. We managed to open the airway enough to see the branches going to the upper and lower lobes.",
            9: "Procedure: Rigid endoscopy with physical tumor extraction.\nLocation: Left principal bronchus.\nIntervention: The rigid barrel was used to shear the mass. Grasping instruments extracted the tissue. No thermal destruction was applied.\nResult: Distal lobar orifices were visually confirmed."
        },
        9: { # Isabel Ramos (Rigid bronch, Bronchus Intermedius, rigid coring/forceps)
            1: "Indication: BI obstruction (tumor).\nProc: Rigid bronch, mechanical debulking.\nFindings: 80% obstruction Bronchus Intermedius.\nAction: Rigid coring, forceps excision.\nNo thermal/balloon.\nResult: 60% patency.\nEBL: 15mL.",
            2: "PROCEDURE: Rigid bronchoscopic recanalization of the bronchus intermedius.\nINDICATION: Symptomatic malignant airway obstruction.\nTECHNIQUE: Mechanical debulking was performed. The rigid scope was advanced to core the polypoid mass. Forceps were utilized for piecemeal excision of the tumor fragments. No thermal energy or balloon dilation was applied. \nOUTCOME: Improvement in lumen patency to approximately 60%.",
            3: "Code: 31640.\nService: Excision of tumor.\nLocation: Bronchus Intermedius.\nTools: Rigid scope (coring), Forceps.\nRationale: Documentation supports physical removal of tissue to relieve obstruction. No thermal ablation was used.",
            4: "Procedure: BI Tumor Debulking\nPatient: Isabel Ramos\nSteps:\n1. GA / Rigid.\n2. Mass in Bronchus Intermedius.\n3. Cored it and pulled pieces with forceps.\n4. No laser used.\n5. Airway is 60% open now.\nPlan: Floor obs.",
            5: "Isabel Ramos has a tumor in the bronchus intermedius causing cough. Taking her for rigid bronch. Mass was polypoid blocking 80 percent. We cored it out and grabbed the pieces. Just mechanical stuff no balloon or heat. Bleeding was mild. She is going to the floor.",
            6: "Rigid bronchoscopy with mechanical debulking of BI tumor. Obstruction of bronchus intermedius from endobronchial tumor. Polypoid mass in bronchus intermedius with 80% obstruction. Rigid coring and forceps debulking used to mechanically debulk and excise tumor. Tumor removed in piecemeal fashion. No thermal ablation or balloon used. Extubated and discharged to floor.",
            7: "[Indication]\nBI obstruction, tumor.\n[Anesthesia]\nGeneral, Rigid.\n[Description]\n80% stenosis. Mechanical excision via rigid coring and forceps. No ablation. Lumen 60% patent.\n[Plan]\nOvernight observation.",
            8: "Ms. Ramos had a polyp-like tumor blocking her intermediate bronchus. We performed a rigid bronchoscopy to remove it. We used the sharp edge of the rigid scope to cut the tumor and forceps to remove it in pieces. We opened the airway to about 60% of its normal size without needing to use any burning tools.",
            9: "Procedure: Rigid endoscopy with physical resection of BI mass.\nFindings: Polypoid growth obstructing the intermediate airway.\nIntervention: The rigid instrument was used to shear the growth. Grasping tools were employed for extraction. No thermal devices were utilized.\nResult: Partial restoration of airway caliber."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the 10 patients to ensure consistent random name generation 
    across the variations, matching the style indices.
    """
    return [
        {"idx": 0, "orig_name": "Michael Brown", "orig_age": 70, "names": ["James Smith", "Robert Johnson", "William Williams", "David Brown", "Richard Jones", "Joseph Garcia", "Thomas Miller", "Charles Davis", "Christopher Rodriguez"]},
        {"idx": 1, "orig_name": "Hannah Lee", "orig_age": 47, "names": ["Mary Martinez", "Patricia Hernandez", "Jennifer Lopez", "Linda Gonzalez", "Elizabeth Wilson", "Barbara Anderson", "Susan Thomas", "Jessica Taylor", "Sarah Moore"]},
        {"idx": 2, "orig_name": "Christopher Adams", "orig_age": 62, "names": ["Daniel Jackson", "Paul Martin", "Mark Lee", "Donald Perez", "George Thompson", "Kenneth White", "Steven Harris", "Edward Sanchez", "Brian Clark"]},
        {"idx": 3, "orig_name": "Aisha Khan", "orig_age": 59, "names": ["Karen Ramirez", "Nancy Lewis", "Lisa Robinson", "Betty Walker", "Margaret Young", "Sandra Allen", "Ashley King", "Kimberly Wright", "Emily Scott"]},
        {"idx": 4, "orig_name": "Robert Wilson", "orig_age": 73, "names": ["Ronald Torres", "Anthony Nguyen", "Kevin Hill", "Jason Flores", "Matthew Green", "Gary Adams", "Timothy Nelson", "Jose Baker", "Larry Hall"]},
        {"idx": 5, "orig_name": "Emily Garcia", "orig_age": 52, "names": ["Donna Rivera", "Michelle Campbell", "Dorothy Mitchell", "Carol Carter", "Amanda Roberts", "Melissa Gomez", "Deborah Phillips", "Stephanie Evans", "Rebecca Turner"]},
        {"idx": 6, "orig_name": "Steven Park", "orig_age": 60, "names": ["Frank Diaz", "Scott Parker", "Eric Cruz", "Stephen Edwards", "Andrew Collins", "Raymond Reyes", "Gregory Stewart", "Joshua Morris", "Jerry Morales"]},
        {"idx": 7, "orig_name": "Laura Perez", "orig_age": 44, "names": ["Sharon Murphy", "Kathleen Cook", "Cynthia Rogers", "Helen Morgan", "Amy Peterson", "Shirley Cooper", "Angela Reed", "Anna Bailey", "Ruth Bell"]},
        {"idx": 8, "orig_name": "Daniel Scott", "orig_age": 68, "names": ["Dennis Gomez", "Walter Kelly", "Patrick Howard", "Peter Ward", "Harold Cox", "Douglas Diaz", "Henry Richardson", "Carl Wood", "Arthur Watson"]},
        {"idx": 9, "orig_name": "Isabel Ramos", "orig_age": 57, "names": ["Brenda Brooks", "Pamela Bennett", "Nicole Gray", "Katherine James", "Samantha Reyes", "Christine Cruz", "Catherine Hughes", "Virginia Price", "Debra Myers"]}
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
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}")
            
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
    output_filename = output_dir / "synthetic_mechanical_debulking_part_083.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()