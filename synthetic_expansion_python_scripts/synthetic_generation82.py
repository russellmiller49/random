import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (as provided in prompt)
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_082.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each of the 10 source notes.
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
        0: { # Thomas Keller: Rigid bronch, L mainstem tumor, mechanical debulking
            1: "Procedure: Rigid Bronchoscopy w/ excision.\n- Intubated with size 12 rigid scope.\n- Tumor found medial wall LMS, 90% obstruction.\n- Actions: Mechanical coring with scope bevel. Forceps removal of fragments. Microdebrider for residuals.\n- Result: LMS <20% obstructed. Airways patent.\n- EBL: 25mL.\n- Plan: ICU.",
            2: "OPERATIVE NARRATIVE: The patient was subjected to general anesthesia and intubated with a rigid bronchoscope to address a high-grade obstruction of the left mainstem bronchus. Visualization confirmed an exophytic squamous cell carcinoma. A multimodal mechanical approach was utilized, employing the rigid barrel for core resection, followed by precise excision with biopsy forceps and microdebrider. This mechanical debulking successfully re-established airway patency without the utilization of thermal ablative technologies. Hemostasis was achieved via cold saline lavage.",
            3: "Procedure Code: 31640 (Bronchoscopy with tumor excision).\nTechnique: Mechanical Debulking.\nTools: Rigid bronchoscope bevel (coring), Forceps, Microdebrider.\nLocation: Left Mainstem Bronchus.\nDetails: The obstructing tumor was physically excised and removed in piecemeal fashion. No laser or APC was utilized, confirming the mechanical nature of the excision. The airway lumen was restored from 90% obstruction to <20% obstruction.",
            4: "Procedure Note\nResident: Dr. Santos\nAttending: Dr. Brennan\nIndication: LMS obstruction.\nSteps:\n1. Time out/GA.\n2. Rigid scope inserted.\n3. Identified tumor in LMS.\n4. Used bevel to core tumor.\n5. Removed bulk with forceps.\n6. Microdebrider to finish.\n7. Suctioned blood/secretions.\nComplications: None.\nDisposition: ICU.",
            5: "We did the rigid bronchoscopy on mr keller today for that left mainstem tumor... uh went in with the size 12 scope general anesthesia... saw the mass causing about 90 percent blockage pretty friable... used the scope to core it out and then grabbed the pieces with forceps... used the microdebrider too to clean it up... no laser needed... bleeding was minor stopped with saline... airway looks good now open to less than 20 percent obstruction... sent him to ICU.",
            6: "The patient was brought to the operating room and placed under general anesthesia. A size 12 rigid bronchoscope was introduced. An exophytic tumor was noted on the medial wall of the left mainstem bronchus causing 90% obstruction. Mechanical debulking was performed using rigid coring, forceps extraction, and microdebrider application. No thermal ablation was employed. Hemostasis was achieved with cold saline. The airway was restored to near patency. The patient was extubated and transferred to the ICU.",
            7: "[Indication]\nMalignant central airway obstruction, left mainstem bronchus.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nRigid coring and mechanical debulking performed on LMS tumor. Forceps and microdebrider used to excise tissue. Obstruction reduced from 90% to <20%. No thermal ablation.\n[Plan]\nICU monitoring.",
            8: "Under general anesthesia, a size 12 rigid bronchoscope was inserted to address the left mainstem obstruction. We identified a friable tumor causing significant blockage. The bevel of the scope was used to mechanically core through the lesion. We then used forceps to remove the bulk of the tumor and a microdebrider to clear the remaining tissue. This mechanical excision restored the airway patency significantly. There was only mild bleeding, which we managed with cold saline.",
            9: "Rigid endoscopy performed for airway clearance. The left mainstem neoplasm was cored and extracted using the rigid barrel and grasping instruments. A rotary shaver was employed to shave down residual tissue. The obstructing mass was physically removed piecemeal. The passage was recanalized successfully. Minimal hemorrhaging occurred and was halted with lavage."
        },
        1: { # Maria Lopez: Flex bronch, distal tracheal granulation, forceps/snare
            1: "Dx: Tracheal stenosis (granulation).\nRx: Flex bronch w/ mechanical debulking.\n- 2cm above carina.\n- Forceps used to remove granulation.\n- Snare excision of fibrotic band.\n- Lumen opened.\n- No thermal energy used.\n- D/C home.",
            2: "PROCEDURE: Therapeutic flexible bronchoscopy.\nCLINICAL CONTEXT: Post-intubation stenosis.\nFINDINGS: Circumferential granulation tissue at the distal trachea.\nTECHNIQUE: Mechanical excision was prioritized. Large alligator forceps were utilized to debride the friable tissue. Subsequently, an electrocautery-independent snare technique was employed to resect a central fibrotic band, effectively disrupting the stenotic ring and restoring luminal diameter.",
            3: "CPT 31640 Justification:\nService: Bronchoscopy with excision of tumor/tissue.\nMethod: Mechanical removal using alligator forceps and snare.\nSite: Distal Trachea.\nNote: No balloon dilation or thermal ablation codes are applicable as the primary method of opening the airway was physical excision of the obstructing granulation tissue.",
            4: "Procedure: Bronchoscopy (Flexible)\nIndication: Tracheal stenosis.\nSteps:\n1. Moderate sedation.\n2. Scope introduced.\n3. Granulation tissue found distally.\n4. Forceps used to remove tissue pieces.\n5. Snare used to cut band.\n6. Airway opened up.\nPlan: Inhaled steroids, f/u 6 weeks.",
            5: "Procedure note for maria lopez... she has that tracheal stenosis from the tube before... we did a flex bronch with sedation... saw the granulation tissue above the carina... used the alligator forceps to pull it out piece by piece... also used a snare to cut a band of tissue... opened it up nice... no bleeding really... patient tolerated it well going home on steroids.",
            6: "Under moderate sedation the flexible bronchoscope was inserted. The distal trachea showed 70% obstruction from granulation tissue. Mechanical debulking was executed using large alligator forceps to remove tissue. A snare was then used to resect a fibrotic band. No thermal ablation was required. The airway lumen was significantly improved. The patient was stable and discharged to home.",
            7: "[Indication]\nSymptomatic benign distal tracheal stenosis.\n[Anesthesia]\nModerate Sedation.\n[Description]\nMechanical debulking of granulation tissue using forceps and snare resection. Tracheal lumen restored. No thermal ablation.\n[Plan]\nDischarge on inhaled steroids.",
            8: "The patient underwent flexible bronchoscopy for tracheal stenosis. We identified a ring of granulation tissue causing obstruction. Using alligator forceps, we mechanically removed the tissue in a piecemeal fashion. We also utilized a snare to resect a fibrous band within the trachea. These mechanical interventions successfully opened the airway without the need for laser or balloon dilation.",
            9: "Flexible endoscopy performed to clear the airway. The tracheal obstruction was dismantled using grasping forceps. The constricting tissue was avulsed and extracted. A loop snare was used to slice through the fibrotic stricture. The tracheal passage was widened via physical removal of the offending tissue."
        },
        2: { # David Nguyen: Rigid bronch, Carinal/LMS Small Cell, coring/microdebrider
            1: "- Rigid bronch, GA.\n- Carinal/LMS mass (SCLC).\n- Suctioned clots.\n- Rigid coring of tumor.\n- Forceps/microdebrider excision.\n- Lumen 90% -> 30% obstruction.\n- Bleeding controlled w/ balloon/epi.\n- ICU.",
            2: "OPERATIVE SUMMARY: The patient presented with critical central airway obstruction secondary to small cell carcinoma. Rigid bronchoscopy was initiated. The carina and proximal left mainstem were occluded by neoplastic tissue. Aggressive mechanical debulking was performed utilizing the rigid bevel for coring, followed by piecemeal excision with forceps and microdebridement. This resulted in significant recanalization of the left mainstem bronchus.",
            3: "Code 31640: Bronchoscopy with excision of tumor.\nTarget: Carina and Left Mainstem.\nInstruments: Rigid Bronchoscope (coring), Forceps, Microdebrider.\nDescription: Mechanical removal of obstructing tumor tissue. No ablative therapies (laser/cryo) employed. Procedure focused on physical excision to restore airway patency.",
            4: "Procedure: Rigid Bronchoscopy\nPatient: David Nguyen\nSteps:\n1. GA/Jet vent.\n2. Scope to carina.\n3. Tumor coring with rigid scope.\n4. Forceps removal of chunks.\n5. Microdebrider cleanup.\n6. Hemostasis with epi/balloon.\n7. Airway patent.\nPlan: ICU admission.",
            5: "Operative report for mr nguyen... came in with hemoptysis and dyspnea... has small cell cancer... we did a rigid bronch... tumor was all over the carina and left main... cored it out with the scope bevel... pulled out big pieces with forceps... used the microdebrider too... bit of bleeding handled with balloon and epi... airway is much better now... kept him intubated for the ICU.",
            6: "General anesthesia was induced and a rigid bronchoscope inserted. A friable tumor obstructing the carina and left mainstem was identified. Mechanical debulking was performed via rigid coring, forceps excision, and microdebrider aspiration. Significant tumor volume was removed restoring the lumen. Brisk bleeding was controlled with tamponade and epinephrine. The patient was transferred to the ICU intubated.",
            7: "[Indication]\nSmall cell lung cancer, carinal/LMS obstruction.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nMechanical excision of tumor using rigid coring, forceps, and microdebrider. Left mainstem recanalized. Hemostasis achieved.\n[Plan]\nICU, Chemotherapy.",
            8: "We performed a rigid bronchoscopy to address the patient's severe airway obstruction. The tumor at the carina and left mainstem was mechanically debulked. We used the bevel of the rigid scope to core through the mass, then removed the fragments with forceps. A microdebrider was used to clean up the edges. This physical removal of the tumor opened the airway significantly. We managed some bleeding with a balloon and epinephrine.",
            9: "Rigid endoscopy utilizing jet ventilation. The carinal neoplasm was excavated using the rigid barrel. Tissue fragments were plucked with forceps. A rotary cutting tool was used to shave the residual mass. The airway caliber was augmented via physical extraction of the malignancy. Hemorrhage was stemmed with tamponade."
        },
        3: { # Sarah Ibrahim: Rigid bronch, RMS Renal Cell, coring/forceps/microdebrider
            1: "Procedure: Rigid bronch debulking.\nSite: R mainstem (RCC met).\nAction: Rigid coring, forceps excision, microdebrider.\nResult: 80% obstruction reduced to 20-30%.\nComplication: None.\nPlan: Floor admit.",
            2: "SURGICAL REPORT: The patient underwent rigid bronchoscopy for management of a metastatic renal cell carcinoma obstructing the right mainstem bronchus. Inspection revealed a vascular, polypoid lesion. Mechanical resection was achieved through a combination of rigid coring, forceps excision, and microdebridement. This approach effectively excised the intraluminal component of the tumor, restoring ventilation to the right lung lobes.",
            3: "Service: Bronchoscopy with Tumor Excision (31640).\nAnatomy: Right Mainstem Bronchus.\nMethod: Mechanical excision only (Coring, Forceps, Microdebrider).\nNote: High vascularity managed with cold saline/epi; no thermal ablation codes utilized. Documentation supports mechanical removal of obstructing tissue.",
            4: "Resident Note: R Mainstem Debulking\nAttending: Dr. Kim\n1. Rigid scope inserted.\n2. Tumor mapped in RMS.\n3. Cored with bevel.\n4. Forceps removal.\n5. Microdebrider used.\n6. Hemostasis good.\n7. Extubated -> Recovery.",
            5: "Procedure note sarah ibrahim... renal cell met to the right mainstem... rigid bronch used... tumor was pretty vascular... we cored it with the scope and used forceps to pull pieces out... microdebrider finished it off... bleeding wasnt too bad used some epi... airway looks open now about 80 percent... extubated and sent to recovery.",
            6: "Under general anesthesia the rigid bronchoscope was advanced to the right mainstem bronchus. An obstructing tumor consistent with metastatic RCC was identified. Mechanical debulking was performed using the rigid bevel for coring followed by forceps excision and microdebridement. The airway was recanalized to 80% patency. Hemostasis was maintained with epinephrine and saline. The patient was extubated and stable.",
            7: "[Indication]\nRight mainstem obstruction, metastatic RCC.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nMechanical debulking of RMS tumor via rigid coring, forceps, and microdebrider. Lumen patency restored. No thermal ablation.\n[Plan]\nFloor admission.",
            8: "The patient was brought to the OR for management of a right mainstem tumor. Using a rigid bronchoscope, we mechanically excised the mass. This involved coring the tumor with the scope's tip, pulling out pieces with forceps, and smoothing the airway with a microdebrider. We avoided thermal energy due to the mechanical nature of the removal. The airway was successfully opened, and the patient recovered well.",
            9: "Rigid endoscopy for airway recanalization. The right mainstem metastasis was scooped out using the rigid bevel. Grasping instruments extracted the bulk. A powered shaver eliminated the remainder. The obstruction was physically cleared. Minor bleeding was arrested with vasoconstrictors."
        },
        4: { # James Patel: Rigid bronch, Proximal Trachea Adenoid Cystic, forceps/snare
            1: "Indication: Proximal tracheal tumor.\nTechnique: Rigid bronch.\nIntervention: Forceps excision, rigid bevel shaving, snare resection.\nResult: Airway open. No laser used.\nStatus: Extubated, stable.",
            2: "OPERATIVE NOTE: The patient presented with a proximal tracheal mass suggestive of adenoid cystic carcinoma. Rigid bronchoscopy facilitated mechanical excision. The tumor was resected in a piecemeal fashion utilizing rigid forceps and the bevel of the scope for shaving. A snare was employed to amputate a pedunculated component. The procedural goal of establishing a patent airway via mechanical tumor excision was achieved.",
            3: "Billing Code 31640: Bronchoscopy with excision of tumor.\nSite: Proximal Trachea.\nMethodology: Mechanical instruments only (Rigid forceps, Bevel shaving, Snare).\nExclusions: No laser, cryotherapy, or APC used. Purely mechanical debulking supported.",
            4: "Procedure: Tracheal Debulking\n1. GA established.\n2. Rigid scope to trachea.\n3. Mass seen 3cm below cords.\n4. Removed pieces with forceps.\n5. Snare used for stalk.\n6. Shaved base with scope.\n7. Extubated.",
            5: "Dictation for james patel... proximal tracheal tumor... did a rigid bronch... used the forceps to grab and remove pieces... then used the scope to shave it down flush... also used a snare to cut off a piece... no laser or anything... airway looks good now... extubated in OR... path sent.",
            6: "The patient was intubated with a rigid bronchoscope. A proximal tracheal tumor was visualized causing obstruction. Mechanical excision was performed using rigid forceps and bevel shaving. A snare loop resected a pedunculated portion. No thermal ablation was utilized. The airway was successfully cleared. The patient was stable and extubated.",
            7: "[Indication]\nProximal tracheal obstruction, adenoid cystic carcinoma.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nMechanical excision of tracheal tumor using forceps, rigid bevel, and snare. Lumen patent. No thermal energy.\n[Plan]\nPathology pending, Radiation oncology f/u.",
            8: "We proceeded with rigid bronchoscopy to treat the patient's tracheal tumor. The mass was mechanically removed. We utilized rigid forceps to grasp and pull out tumor fragments and used the edge of the scope to shave down the base. A snare was also used to cut off a hanging piece of the tumor. These mechanical methods cleared the obstruction without the need for laser therapy.",
            9: "Rigid endoscopy for tracheal clearance. The subglottic neoplasm was avulsed using rigid graspers. The scope edge scraped away the sessile component. A wire loop amputated the stalk. The luminal blockage was physically excised. Minimal oozing occurred."
        },
        5: { # Evelyn Brooks: Rigid bronch, Bronchus Intermedius, coring/microdebrider
            1: "Dx: BI obstruction (Adeno).\nProc: Rigid bronch debulking.\nActions: Suction/lavage. Rigid coring. Microdebrider.\nOutcome: 85% -> 30% obstruction. RML/RLL patent.\nEBL: 35ml.\nPlan: Admit floor.",
            2: "PROCEDURE PERFORMED: Rigid bronchoscopy with mechanical tumor excision.\nFINDINGS: Exophytic adenocarcinoma obstructing the bronchus intermedius.\nINTERVENTION: The rigid bronchoscope was utilized to perform core resection of the tumor mass. Following this, a microdebrider was employed to mechanically excise residual tissue and clear the bronchial lumen. This achieved restoration of patency to the right middle and lower lobes without thermal ablation.",
            3: "CPT 31640: Bronchoscopy with excision of tumor.\nLocation: Bronchus Intermedius.\nTechnique: Mechanical excision via rigid coring and microdebrider.\nDocumentation: Explicitly states 'Rigid coring and mechanical debulking'. No thermal energy codes apply.",
            4: "Resident Note: BI Debulking\nPatient: Evelyn Brooks\n1. Rigid scope inserted.\n2. BI tumor found.\n3. Cored with scope.\n4. Microdebrider used for cleanup.\n5. Secretions suctioned.\n6. Bleeding controlled.\n7. Extubated.",
            5: "Procedure note evelyn brooks... bronchus intermedius tumor causing pneumonia... went in with rigid scope... cored out the tumor with the bevel... used the microdebrider to get the rest... cleaned out the pus... airway is open now can see the lower lobes... bleeding stopped with tamponade... admitted for antibiotics.",
            6: "General anesthesia was administered. Rigid bronchoscopy revealed an 85% obstruction of the bronchus intermedius by tumor. Mechanical debulking was performed via rigid coring and microdebridement. Secretions were cleared. The airway was restored to near patency. Hemostasis was achieved with epinephrine. The patient was transferred to the floor.",
            7: "[Indication]\nBronchus Intermedius obstruction, Adenocarcinoma.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nMechanical debulking using rigid coring and microdebrider. Airway opened. Secretions cleared.\n[Plan]\nIV Antibiotics, Floor admit.",
            8: "The patient underwent rigid bronchoscopy for a tumor in the bronchus intermedius. We used the rigid scope to mechanically core through the center of the tumor. A microdebrider was then used to excise the remaining tissue and clean the airway walls. This mechanical removal opened the bronchus and allowed us to clear the infection behind the blockage. No laser was needed.",
            9: "Rigid endoscopy for bronchial recanalization. The intermediate bronchial mass was excavated via rigid coring. A rotary shaver debrided the remaining tissue. The obstruction was physically eliminated. Purulence was aspirated. Hemostasis was secured."
        },
        6: { # Omar Hassan: Flex bronch, LLL carcinoid, snare/forceps
            1: "Indication: LLL carcinoid.\nProcedure: Flex bronch w/ excision.\nTechnique: Snare resection of stalk. Forceps debulking.\nResult: Lumen cleared. No laser.\nDisposition: Outpatient.",
            2: "OPERATIVE SUMMARY: The patient underwent flexible bronchoscopy for management of a left lower lobe endobronchial carcinoid. The lesion was pedunculated. An electrosurgical snare was used to transect the stalk, effectively resecting the primary mass. Remnant tissue was excised mechanically using biopsy forceps. The left lower lobe bronchus was successfully recanalized.",
            3: "Code Selection: 31640.\nRationale: Excision of tumor via bronchoscopy.\nTools: Snare (mechanical/cautery snare) and Forceps.\nSite: Left Lower Lobe.\nNote: Procedure described as mechanical debulking and snare resection.",
            4: "Procedure: LLL Tumor Resection\n1. LMA/Sedation.\n2. Flex scope to LLL.\n3. Carcinoid seen.\n4. Snared off the stalk.\n5. Forceps used to clean up base.\n6. Bleeding stopped.\n7. Discharged.",
            5: "Note for omar hassan... has that carcinoid in the LLL... did a flex bronch with lma... used a snare to cut it off at the base... then grabbed the rest with forceps... came out nicely... airway is open... no complications... going home today.",
            6: "Moderate sedation was utilized. Flexible bronchoscopy identified a pedunculated carcinoid in the LLL. Snare resection was performed on the stalk. Forceps were used to mechanically debulk residual fragments. The airway was cleared. No significant bleeding occurred. Patient discharged home.",
            7: "[Indication]\nLLL obstruction, Carcinoid tumor.\n[Anesthesia]\nModerate Sedation, LMA.\n[Description]\nSnare resection and mechanical forceps debulking of endobronchial tumor. Lumen patent. No complications.\n[Plan]\nSurveillance in 3 months.",
            8: "We performed a flexible bronchoscopy to remove a carcinoid tumor in the left lower lobe. The tumor was attached by a stalk, which we cut through using a snare. We then used forceps to mechanically remove the remaining pieces of the tumor. This cleared the blockage in the airway completely. There was very little bleeding.",
            9: "Flexible endoscopy for tumor removal. The LLL polyp was amputated using a wire loop. Fragments were plucked with grasping forceps. The bronchial obstruction was physically resected. The lumen is now patent."
        },
        7: { # Lin Chen: Rigid bronch, LMS squamous, coring/forceps/microdebrider
            1: "Emergent Rigid Bronch.\n- LMS obstructed 95% (Squamous).\n- Hypoxic failure.\n- Rigid coring + forceps + microdebrider.\n- Mechanical excision only.\n- Lumen open, lung re-expanded.\n- ICU intubated.",
            2: "PROCEDURE: Emergent rigid bronchoscopy.\nINDICATION: Acute respiratory failure secondary to malignant left mainstem obstruction.\nTECHNIQUE: The rigid bronchoscope was employed as a coring device to mechanically debulk the central tumor mass. Large volume resection was facilitated by forceps extraction. Fine debridement was completed with a microdebrider. This mechanical excision successfully relieved the obstruction without the use of ablative energy.",
            3: "Billing: 31640 (Excision of tumor).\nContext: Emergent/Salvage.\nMethod: Mechanical (Rigid Coring, Forceps, Microdebrider).\nSite: Left Mainstem.\nComplexity: ASA IV, hypoxic failure. No thermal ablation used.",
            4: "Resident Note: Emergency Debulking\nPatient: Lin Chen\n1. GA/Rigid scope.\n2. LMS 95% blocked.\n3. Cored with scope.\n4. Removed chunks with forceps.\n5. Microdebrider used.\n6. Lung re-expanded on fluoro/cxr.\n7. To ICU intubated.",
            5: "Emergency bronch for lin chen... hypoxic failure from lms tumor... rigid scope used... cored out the tumor aggressively... pulled pieces with forceps... used microdebrider... no laser... bleeding controlled... lung popped back up... sent to icu on vent.",
            6: "The patient was intubated with a rigid bronchoscope due to respiratory failure. A 95% obstruction of the left mainstem was noted. Mechanical debulking was performed using rigid coring, forceps, and microdebrider. The airway was recanalized. No thermal ablation was used. The patient remained intubated and was transferred to the ICU.",
            7: "[Indication]\nAcute respiratory failure, LMS malignant obstruction.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nMechanical excision of tumor via coring, forceps, and microdebrider. Left lung re-expanded. No thermal energy.\n[Plan]\nICU, Mechanical Ventilation.",
            8: "This was an emergency procedure for a blocked left mainstem bronchus. We used a rigid bronchoscope to mechanically core out the tumor. Large pieces were removed with forceps, and a microdebrider cleaned the rest. This physical removal of the blockage allowed the left lung to re-expand. We did not use any heat or laser treatments.",
            9: "Rigid endoscopy for salvage airway clearance. The left bronchial malignancy was bored out with the rigid bevel. Tissue chunks were extracted via graspers. A powered shaver was used for final clearance. The obstruction was physically excised. Ventilation improved."
        },
        8: { # Jacob Morales: Rigid bronch, RMS squamous, coring/forceps/microdebrider
            1: "Proc: Rigid bronch debulking RMS.\nInd: Hemoptysis/Dyspnea.\nAction: Clot suctioned. Rigid coring of tumor. Forceps/microdebrider.\nResult: Lumen 70% open.\nBleeding: Moderate, controlled.\nPlan: Step-down.",
            2: "OPERATIVE REPORT: The patient presented with symptomatic right mainstem obstruction. Rigid bronchoscopy was performed. The tumor was mechanically debrided using the bevel of the rigid scope for coring, followed by forceps excision of fragments. A microdebrider was utilized to contour the bronchial wall. This mechanical debulking restored airway patency and resolved the immediate obstruction.",
            3: "Code 31640.\nSite: Right Mainstem Bronchus.\nMethod: Mechanical excision (Coring, Forceps, Microdebrider).\nNote: Procedure addresses airway obstruction via physical removal of tumor tissue. No ablation codes applicable.",
            4: "Procedure: RMS Tumor Removal\n1. GA/Rigid scope.\n2. Suctioned clots.\n3. Cored tumor with scope.\n4. Forceps used.\n5. Microdebrider for base.\n6. Hemostasis achieved.\n7. Extubated.",
            5: "Jacob morales procedure note... right mainstem tumor bleeding... rigid bronch... sucked out the blood... cored the tumor with the scope... grabbed pieces with forceps... microdebrider used to smooth it... bleeding stopped with epi... airway open now... step down unit.",
            6: "General anesthesia was used. Rigid bronchoscopy revealed a right mainstem tumor with clot. Mechanical debulking was performed using rigid coring, forceps, and microdebrider. The airway was opened to 70%. Hemostasis was secured. The patient was extubated and sent to the step-down unit.",
            7: "[Indication]\nHemoptysis, RMS obstruction.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nMechanical debulking of tumor and clot. Rigid coring, forceps, microdebrider used. Lumen restored. Hemostasis achieved.\n[Plan]\nStep-down admission.",
            8: "We performed a rigid bronchoscopy to treat the patient's bleeding tumor in the right mainstem bronchus. After clearing the blood clots, we mechanically cored out the tumor using the scope. We used forceps to remove the pieces and a microdebrider to smooth the airway. This mechanical excision opened the airway and stopped the source of the bleeding.",
            9: "Rigid endoscopy for airway patency. The right bronchial neoplasm was excavated via rigid coring. Fragments were avulsed with forceps. A rotary shaver debrided the base. The blockage was physically removed. Hemostasis was obtained."
        },
        9: { # Priya Singh: Rigid bronch, LMS Breast Met, snare/forceps
            1: "Dx: LMS obstruction (Breast met).\nProc: Rigid bronch excision.\nActions: Bevel debulking. Forceps removal. Snare resection of pedunculated part.\nResult: Lumen 60% open.\nEBL: 20ml.\nDisp: Floor.",
            2: "OPERATIVE NOTE: A rigid bronchoscopy was undertaken for a metastatic lesion obstructing the left mainstem bronchus. Mechanical excision was the primary modality. The rigid bevel was used to shear tumor tissue, while forceps were employed for debulking. A snare was utilized to resect a pedunculated component. The procedure successfully restored luminal patency via mechanical means.",
            3: "CPT: 31640 (Excision of tumor).\nSite: Left Mainstem.\nTools: Rigid Bevel, Forceps, Snare.\nRationale: Mechanical removal of obstructing tissue documented. No thermal destruction utilized.",
            4: "Procedure: LMS Debulking\n1. GA/Rigid scope.\n2. Tumor in LMS.\n3. Scraped with bevel.\n4. Forceps used.\n5. Snare for hanging piece.\n6. Airway opened.\n7. Extubated.",
            5: "Priya singh procedure... breast cancer met to left main... rigid bronch... used the scope to scrape it... forceps to pull pieces... snare for the pedunculated part... opened it up to about 60 percent... no bleeding issues... admitted to floor.",
            6: "Under general anesthesia a rigid bronchoscope was inserted. A left mainstem tumor was identified. Mechanical debulking was performed using the scope bevel and forceps. Snare resection removed a pedunculated component. No thermal ablation was used. The airway was recanalized. Patient extubated and stable.",
            7: "[Indication]\nLMS obstruction, Metastatic Breast Cancer.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nMechanical excision of tumor using rigid bevel, forceps, and snare. Lumen patent. No thermal energy.\n[Plan]\nOncology admission.",
            8: "The patient underwent rigid bronchoscopy for a metastatic tumor blocking the left mainstem bronchus. We mechanically removed the tumor using the tip of the scope and forceps. We also used a snare to cut off a piece of the tumor that was hanging into the airway. These mechanical actions opened the airway significantly without the use of heat or lasers.",
            9: "Rigid endoscopy for tumor extraction. The left bronchial metastasis was sheared with the rigid bevel. Tissue was plucked with graspers. A wire loop amputated the stalk. The obstruction was physically resected. The airway was restored."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the prompt's examples
    # (In a real script, this data comes from reading the source JSON)
    return [
        {"idx": 0, "orig_name": "Thomas Keller", "orig_age": 67, "names": ["Robert Smith", "James Johnson", "Michael Williams", "David Brown", "Richard Jones", "Charles Garcia", "Joseph Miller", "Thomas Davis", "Christopher Rodriguez"]},
        {"idx": 1, "orig_name": "Maria Lopez", "orig_age": 58, "names": ["Mary Martinez", "Patricia Hernandez", "Jennifer Lopez", "Linda Gonzalez", "Elizabeth Wilson", "Barbara Anderson", "Susan Thomas", "Jessica Taylor", "Sarah Moore"]},
        {"idx": 2, "orig_name": "David Nguyen", "orig_age": 72, "names": ["Daniel Jackson", "Paul Martin", "Mark Lee", "Donald Perez", "George Thompson", "Kenneth White", "Steven Harris", "Edward Sanchez", "Brian Clark"]},
        {"idx": 3, "orig_name": "Sarah Ibrahim", "orig_age": 63, "names": ["Lisa Ramirez", "Karen Lewis", "Nancy Robinson", "Betty Walker", "Margaret Young", "Sandra Allen", "Ashley King", "Kimberly Wright", "Emily Scott"]},
        {"idx": 4, "orig_name": "James Patel", "orig_age": 69, "names": ["Ronald Torres", "Anthony Nguyen", "Kevin Hill", "Jason Flores", "Matthew Green", "Gary Adams", "Timothy Nelson", "Jose Baker", "Larry Hall"]},
        {"idx": 5, "orig_name": "Evelyn Brooks", "orig_age": 54, "names": ["Donna Rivera", "Michelle Campbell", "Dorothy Mitchell", "Carol Carter", "Amanda Roberts", "Melissa Gomez", "Deborah Phillips", "Stephanie Evans", "Rebecca Turner"]},
        {"idx": 6, "orig_name": "Omar Hassan", "orig_age": 61, "names": ["Jeffrey Diaz", "Frank Parker", "Scott Cruz", "Eric Edwards", "Stephen Collins", "Andrew Reyes", "Raymond Stewart", "Gregory Morris", "Joshua Morales"]},
        {"idx": 7, "orig_name": "Lin Chen", "orig_age": 49, "names": ["Sharon Murphy", "Kathleen Cook", "Cynthia Rogers", "Helen Morgan", "Amy Peterson", "Shirley Cooper", "Angela Reed", "Anna Bailey", "Ruth Bell"]},
        {"idx": 8, "orig_name": "Jacob Morales", "orig_age": 76, "names": ["Dennis Gomez", "Walter Kelly", "Patrick Howard", "Peter Ward", "Harold Cox", "Douglas Diaz", "Henry Richardson", "Carl Wood", "Arthur Watson"]},
        {"idx": 9, "orig_name": "Priya Singh", "orig_age": 65, "names": ["Brenda Brooks", "Pamela Bennett", "Nicole Gray", "Katherine James", "Samantha Reyes", "Christine Cruz", "Debra Hughes", "Rachel Price", "Carolyn Myers"]}
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
            
            # Determine new random date (within 2024-2025)
            rand_date_obj = generate_random_date(2024, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned in base_data for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation is missing (should not happen with complete dictionary)
                note_entry["note_text"] = f"Variation {style_num} for note {idx} not found."
            
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
    output_filename = output_dir / "synthetic_part_082.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()