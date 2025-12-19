import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_013.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between the start and end years."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations for each note index.
    Structure: Note_Index (0-3) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Note 1: Stent eval, granulation, secretions
            1: "Procedure: Diagnostic Flex Bronch.\nIndication: Stent eval.\n- Scope passed nasal route. Vocal cords normal.\n- Y-stent in place.\n- Findings: Thick purulent mucus suctioned. Granulation tissue at distal limbs: RMS 50%, LMS 60% obstruction.\n- Lower lobes: Copious purulent secretions suctioned.\n- Complication: Transient hypoxia, fixed with O2.\nPlan: Clinic f/u Jan 3. Stent removal in OR Jan 6.",
            2: "OPERATIVE NARRATIVE: The patient presented for evaluation of an indwelling airway stent. Under moderate sedation, a Q190 videobronchoscope was navigated transnasally. The laryngeal structures were unremarkable. Upon tracheal intubation, the Y-stent was visualized in situ. Significant purulence was noted and evacuated. Examination of the distal stent limbs revealed exuberant granulation tissue compromising the lumen (approx. 50% stenosis right, 60% left). Beyond the stenosis, the lower lobar segments contained tenacious purulent secretions which were cleared. Desaturation occurred intraoperatively, necessitating direct intratracheal oxygen insufflation, which corrected the hypoxemia. The procedure concluded without further incident.",
            3: "CPT 31645 (Bronchoscopy with therapeutic aspiration): Cleared copious purulent mucous from stent and lower lobes.\nProcedure Note: Flexible bronchoscopy performed. Y-stent visualized. Significant granulation tissue noted at distal limbs (50% RMS, 60% LMS), but no destruction/excision performed (supports diagnostic only + aspiration). Therapeutic suctioning required for thick secretions in bilateral lower lobes causing hypoxia. Oxygen provided via working channel. Plan for future stent removal.",
            4: "Procedure: Flex Bronchoscopy\nAttending: Dr. Trentacosta\nPatient: [Patient Name]\nSteps:\n1. Moderate sedation (Versed/Fentanyl).\n2. Scope inserted nose -> trachea.\n3. Y-stent inspected. Full of mucus.\n4. Suctioned stent.\n5. Noted granulation tissue: Right limb 50% blocked, Left limb 60% blocked.\n6. Suctioned pus from lower lobes.\n7. Patient desatted -> gave O2 via scope -> improved.\nPlan: Stent removal next week.",
            5: "We did a bronch today for stent check on this patient gave versed and fentanyl scope went in nose no problem cords look fine y stent is there but its got a lot of thick nasty mucus in it we sucked that out then looked at the ends of the stent there is granulation tissue blocking about half the right side and more on the left maybe 60 percent we went past that and found more pus in the lower lobes sucked that out too patient dropped sats a bit so we hooked up o2 to the scope and he came back up plan is to take the stent out in the OR on the 6th or sooner if needed.",
            6: "The procedure was performed in the bronchoscopy suite under moderate sedation. Following intravenous medications as per the record and topical anesthesia to the upper airway, the Q190 video bronchoscope was introduced through the nose, into the oropharynx. The oropharynx and larynx were well visualized and normal. Topical anesthesia with 1% lidocaine was applied to the vocal cords and the flexible bronchoscope was then advanced through the larynx into the trachea. The patient’s Y stent was well placed. There was thick purulent mucous throughout the stent which was suctioned. At the distal aspect of the right mainstem limb there was granulation tissue causing about 50% obstruction and at the distal aspect of the left mainstem limb there was granulation tissue causing about 60% after bypassing the granulation tissue there were thick copious purulent secretions through the lower lobes which were suctioned. During the procedure, the patient did develop some intermittent hypoxia, requiring attachment of the oxygen supply to the bronchoscope working channel for direct tracheal oxygen administration which resolved the hypoxia. Once we were satisfied that there was no active bleeding, the bronchoscope was removed and the procedure completed.",
            7: "[Indication]\nAirway stent evaluation for severe tracheobronchomalacia.\n[Sedation]\nModerate (Versed 3mg, Fentanyl 75mcg).\n[Description]\nScope introduced transnasally. Y-stent in place. Thick purulent mucus suctioned. Granulation tissue noted at distal limbs (RMS 50%, LMS 60%). Copious purulent secretions in lower lobes suctioned. Transient hypoxia managed with tracheal O2.\n[Plan]\nRTC Jan 3. Stent removal in OR Jan 6. Hypertonic saline.",
            8: "The patient was brought to the bronchoscopy suite for evaluation of their airway stent. After obtaining consent and administering moderate sedation, we introduced the scope through the nose. The vocal cords were normal. We found the Y-stent in good position but filled with thick, purulent mucus, which we cleared. Inspecting the distal ends, we found granulation tissue obstructing the right limb by 50% and the left by 60%. We navigated past this tissue and found more copious pus in the lower lobes, which was also suctioned. The patient experienced some transient hypoxia during the suctioning, which we managed by administering oxygen directly through the scope channel. The procedure was otherwise uncomplicated.",
            9: "PREOPERATIVE DIAGNOSIS: Severe tracheobronchomalacia. PROCEDURE PERFORMED: Flexible bronchoscopy, diagnostic. INDICATIONS: Airway stent assessment. DESCRIPTION: The procedure was executed in the bronchoscopy suite under moderate sedation. The Q190 video bronchoscope was inserted through the nose. The larynx was visualized and normal. The bronchoscope was advanced into the trachea. The Y stent was situated correctly. Thick purulent mucous was aspirated from the stent. At the distal aspect of the right mainstem limb, granulation tissue was occluding about 50% of the lumen, and at the distal aspect of the left mainstem limb, granulation tissue was occluding about 60%. After navigating past the granulation tissue, thick copious purulent secretions were found in the lower lobes and were aspirated. The patient developed intermittent hypoxia, treated with oxygen via the working channel. The bronchoscope was withdrawn.",
        },
        1: { # Note 2: Complex TBM, Dynamic Y placed -> removed -> Dumon Y placed
            1: "Indication: Severe TBM.\nAnesthesia: GA, LMA -> Rigid.\nProcedure:\n1. Flex bronch via LMA: Severe collapse trachea/mainstems. Purulent secretions suctioned.\n2. Dynamic Y-stent placed. LMA removed. Rigid bronch inserted to adjust.\n3. PACU: CXR showed stent migration/short limb.\n4. Return to OR. Rigid bronch (14mm). Dynamic stent removed.\n5. Dumon Y-stent (18x14x14) customized and deployed via rigid.\n6. Position confirmed flex/rigid. Airway stable.\nPlan: Admit. Nebs.",
            2: "OPERATIVE REPORT: The patient presented with severe tracheobronchomalacia. Initial flexible bronchoscopy under general anesthesia confirmed near-complete expiratory collapse. A Dynamic Y-stent was initially deployed; however, post-operative imaging revealed proximal migration and inadequate limb length. The patient returned to the operating room for revision. Using a 14mm ventilating rigid bronchoscope, the initial prosthesis was extracted. A customized silicone Dumon Y-stent (18x14x14) was then deployed. Subsequent inspection demonstrated excellent patency and stabilization of the central airways. The patient was extubated and transferred to the ward in stable condition.",
            3: "CPT Coding Data:\n- 31631 (Placement of tracheal stent): Initial placement of Dynamic Y-stent.\n- 31638-78 (Revision of tracheal stent): Unplanned return to OR for removal of migrated stent and placement of new Dumon stent.\n- 31645-59 (Therapeutic aspiration): Suctioning of thick purulent secretions from bilateral lower lobes distinct from stenting.\nNote: Rigid bronchoscopy used for stent exchange.",
            4: "Procedure Note\nPatient: [Patient Name]\nDiagnosis: TBM\nProcedure: Bronchoscopy with Stent Placement\nSteps:\n1. GA/LMA. Flex scope verified severe collapse.\n2. Suctioned pus from LLL/RLL.\n3. Placed Dynamic Y-stent. Checked with rigid scope.\n4. In PACU, xray showed stent moved. Brought back to OR.\n5. Rigid bronch inserted. Old stent removed.\n6. New Dumon Y-stent placed. Fits better.\n7. Final check showed good airway patency.\nPlan: Admit, saline nebs.",
            5: "we took the patient to the OR for TBM symptoms severe cough and pneumonia put them under GA and put in a lma scope showed bad collapse everywhere plus a lot of pus which we sucked out so we put in a dynamic y stent used the rigid to seat it looked okay sent to pacu but then the xray showed it migrated and was too short on the right so back to the OR we went put the rigid back in took out the first stent customized a dumon y stent and put that in instead fits much better airways open now no bleeding wake up was fine send to floor.",
            6: "The procedure was performed in the main operating room. After administration of sedatives an LMA was inserted and the Q190 flexible bronchoscope was passed through the vocal cords and into the trachea. Approximately 4 cm proximal to the main carina there was near complete expiratory collapse of the airway which extended into the bilateral mainstem bronchi and bronchus intermedius. The tracheobronchial tree was examined to at least the first sub-segmental level. Bronchial mucosa was boggy throughout, with the exception of the severe dynamic collapse anatomy were otherwise normal with no endobronchial lesions seen to at least the first sub-segments. There was thick purulent secretions within the bilateral lower lobes (likely secondary to chronic post-obstructive pneumonia from severe airway collapse) which were suctioned. Measurements of the collapsible central airways were obtained. We then removed the LMA. A MAC 3 video laryngoscope (C-MAC) was then used to expose the larynx with a grade 1 view obtained. The customized 15x12x12 Dynamic Y-stent with a tracheal length of 80mm, right mainstem limb of 10mm and left mainstem limb which was collapsed and secured with Freitag forceps was then passed through the vocal cords and into the trachea. The forceps were opened and once resistance was met indicating the stent had reached the main carina the forceps were removed. Subsequently a 12mm rigid non-ventilating tracheoscope was inserted into the subglottic space and attached to the jet ventilator. The flexible bronchoscope was inserted through the rigid tracheoscope and the stent required minimal adjustment to seat in the desired location. Once this was completed the rigid bronchoscope was removed and the procedure completed. Patient was recovering without issues in the PACU and post-procedure chest x-ray was performed which showed some proximal stent migration and the right sided limb appeared to be of inadequate length to ensure stability. CT was then performed which confirmed the inadequate length f the right sided limb. The patient was then subsequently taken back to the operating room where after induction and administration of paralytics a 12 mm non-ventilating rigid bronchoscope was inserted through the mouth into the subglottic space and attached to the jet ventilation. Using optical forceps we attempted to remove the original Y-stent however the size of the tracheoscope was inadequate and we converted to a 14 mm ventilating rigid bronchoscope which allowed us to easily removed the stent with optical forceps. After-resizing the airways an 18x14x14 Dumon tracheal Y-stent was customized to a tracheal length of 80mm right mainstem length of 30mm and left mainstem limb of 40mm. The stent was then loaded into the Novatech Ton stent deployment device. The rigid bronchoscope was then advanced into the left mainstem and the stent was deployed. Through the use of flexible forceps, and manipulation with the tip of the flexible bronchoscope we were able to adequately position the limbs within the proper airways resulting in successful stabilization of the airway. At this point inspection was performed a flexible bronchoscopic inspection to evaluate for any bleeding or other complications and none was seen. The rigid bronchoscope was then removed and an LMA was inserted. A repeat inspection was performed with the flexible bronchoscope and showed the stent well placed with near complete resolution of central airway collapse. The bronchoscope was then removed and once the patient was awake and protecting airway the LMA was removed and the procedure was completed.",
            7: "[Indication]\nSevere symptomatic tracheobronchomalacia.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\n1. Flex bronch confirmed severe collapse. Purulent secretions aspirated.\n2. Dynamic Y-stent placed via larynx, adjusted with rigid bronch.\n3. Post-op imaging showed migration. Return to OR.\n4. Rigid bronchoscopy performed. Dynamic stent removed.\n5. Dumon Y-stent customized and deployed. Good position/patency confirmed.\n[Plan]\nAdmit. 3% saline nebs. CXR.",
            8: "The patient underwent bronchoscopy for severe tracheobronchomalacia. Initially, we placed a Dynamic Y-stent, but post-procedure imaging in the PACU revealed it had migrated and the right limb was too short. Therefore, we took the patient back to the OR for revision. Using a rigid bronchoscope, we removed the first stent. We then sized and placed a Dumon silicone Y-stent. This second stent provided excellent stabilization of the airway and resolved the collapse. The patient tolerated the revision well and was transferred to the ward.",
            9: "PREOPERATIVE DIAGNOSIS: Severe tracheobronchomalacia. PROCEDURE: Rigid and flexible bronchoscopy with Dynamic Y stent insertion, followed by removal and Dumon Y stent insertion. INDICATION: Chronic symptoms of TBM. DESCRIPTION: Under general anesthesia, the flexible scope verified severe airway collapse. Purulent secretions were aspirated. A Dynamic Y-stent was positioned. Post-procedure imaging indicated migration. The patient returned to the OR. A rigid bronchoscope was utilized to extract the Dynamic stent. A Dumon Y-stent was then deployed using the Novatech device. The limbs were positioned to stabilize the airway. Final inspection showed resolution of collapse."
        },
        2: { # Note 3: Malignant CAO, Embedded Stent Removal, Y-Stent
            1: "Indication: Malignant CAO, Embedded stent.\nProcedure: Rigid bronchoscopy, Stent removal, Tumor debulking, Y-stent.\nFindings: RMS 70% obstruction (tumor). LMS 75% obstruction + embedded stent. TBM mid-trachea.\nActions:\n- Diagnostic flex bronch.\n- Rigid bronch inserted.\n- LMS: APC/debulking/balloon dilation. Metallic stent removed piecemeal.\n- RMS: APC debulking.\n- Customized Y-stent placed (hole cut for RUL).\nPlan: Radiation oncology consult. Removal in 2 weeks.",
            2: "OPERATIVE REPORT: The patient presented with malignant central airway obstruction and a retained metallic stent. Examination revealed significant tumor burden in the right mainstem and granulation/tumor encasing the stent in the left mainstem. A multimodal approach was employed using rigid bronchoscopy. The left-sided metallic stent was liberated using APC, balloon dilation, and mechanical dissection, then extracted. Residual tumor was debulked using cryotherapy and APC. To maintain airway patency, a customized silicone Y-stent was fashioned and deployed, securing ventilation to both lungs. The patient remains intubated for transfer.",
            3: "Codes Support:\n- 31641-22: Complex destruction of tumor/relief of stenosis (APC, Cryo, balloon mechanical) in RMS and LMS.\n- 31635-59: Removal of foreign body (embedded metallic stent) requiring significant dissection.\n- 31631: Placement of tracheal/bronchial Y-stent.\n- 31624-59: BAL for culture.\nTools: Rigid bronch, APC, Cryo probe, Merit balloon, Silicone Y-stent.",
            4: "Procedure: Stent Removal + Y-Stent\nIndication: Cancer, blocked stent.\nSteps:\n1. GA, LMA. Flex scope check.\n2. Saw tumor in RMS and blocked stent in LMS.\n3. Switched to Rigid Bronch.\n4. Used APC and balloon to free up the old stent in LMS. Pulled it out.\n5. Cleaned up tumor with APC/Cryo.\n6. Measured and cut a new Y-stent.\n7. Placed Y-stent. Good position.\nPlan: Admit for Rad Onc.",
            5: "Patient has small cell lung cancer and a stuck stent in the left side we did a rigid bronchoscopy today under general anesthesia airway looked bad dynamic collapse in trachea tumor in the right mainstem and the stent in the left mainstem was full of pus and overgrown with tissue we washed the pus out then used the rigid scope and APC to burn away the tissue holding the stent used a balloon to break it free and pulled it out with forceps then we treated the tumor on the right side with APC and put a new silicone Y stent in made a hole for the right upper lobe looks much better now plan to remove it in two weeks after radiation.",
            6: "The procedure was performed in the main operating room. Following intravenous medications as per the record a laryngeal mask airway was inserted to ensure the patient could be adequately ventilation. Topical anesthesia was then applied to the upper airway and the Boston Scientific Model B diagnostic disposable video bronchoscope was introduced through the mouth, via laryngeal mask airway and advanced to the tracheobronchial tree. The laryngeal mask airway was in good position. The vocal cords appeared normal. The subglottic space was normal. The proximal trachea was normal. The mid trachea was free of tumor but moderate to severe dynamic collapse was visualized (TBM). The right mainstem was extrinsically compressed from the posterior aspect with additional tumor studding and submucosal disease seen throughout the airway causing approximately 70% obstruction. There were a few small tumor nodules present in the distal trachea mostly on the posterior membrane. The proximal left mainstem was mildly compressed externally with submucosal tumor within the airway wall. In the mid left mainstem there was extensive granulation tissue causing about 75% airway obstruction just proximal to the proximal end of known airway stent. After gently passing the bronchoscope through the area of granulation tissue the stent was visualized with thick purulent mucous throughout. 10cc of bicarbonate solution was instilled to thin secretions and then the secretions were suctioned and cleared. Significant post-obstructive puss was noted distal to the stent primarily originating from the lower lobe bronchus and mini lavage was performed for culture. After suctioning clear, tumor infiltration could be seen extending into the proximal aspect of the lower lobe and growing through the stent wall. The left upper lobe however appeared free of disease. At this point the flexible bronchoscope and LMA were removed and a 12mm ventilating rigid bronchoscope was subsequently inserted into the trachea and advanced into the left mainstem bronchus and was then connected to the JET ventilator. The rigid optic was removed and the Olympus T190 Therapeutic bronchoscope was inserted through the rigid lumen and advanced to the proximal edge to the stent. APC was used followed by gentile shaving of coagulated tissue with the tip of the bronchoscope to remove granulation tissue. We the utilized APC to burn the inner silicone coating from the stent and then gently placed flexible forceps through the wall of the stent to peel it from the mucosa. After this a size 4-5-6 Merit dilatational balloon was guided in a similar fashion outside of the stent and used to further break adhesions with the underlying airway wall. Open which we repeated multiple times attempting to slowly re-cannulate the airway. We then removed the flexible bronchoscope and utilized rigid forceps to grasp and remove the stent. APC was then used to cauterize the underlying inflamed mucosa and a 2.1 mm cryotherapy probe was used to remove debris. Significant obstruction both from endobronchial disease and extrinsic compressor however was still present. At this point we took our attention to the right sided airway and utilizing APC with the burn and shave technique attempting to re-cannulate the airway with partial success however obstruction remained > 50% in the right mainstem with tumor extending through the bronchus intermedius. Measurements of the airway were then taken in anticipation of airway stent placement. We customized a customized a 14x10x10 silicone Y-stent to a length of 30mm in the tracheal limb, 35mm in the right limb and 35 mm in the left mainstem limb. We also created a 10mm hole in the right sided limb to allow for the right upper lobe to remain ventilated while maintaining patency of the bronchus intermedius. The rigid bronchoscope was then advanced into the right mainstem and the stent was deployed. After deployment, the rigid forceps were used to manipulate the stent to adequately position the limbs within the proper airways resulting in successful stabilization of the airway. Persistent tumor beyond the stent remained bilaterally with small isolates of tumor in the distal bronchus intermedius and significant residual tumor in the left lower lobe bronchus. The rigid bronchoscope was removed and an LMA was inserted and the procedure was turned over to anesthesia for post-procedural care.",
            7: "[Indication]\nMalignant central airway obstruction, retained metallic stent.\n[Anesthesia]\nGeneral.\n[Description]\n1. Flex bronch: TBM, RMS tumor, LMS embedded stent with pus. BAL done.\n2. Rigid bronch inserted.\n3. LMS: Stent removal using APC, balloon dilation, and forceps.\n4. RMS: Tumor debulking via APC.\n5. Customized Y-stent placed to patent airways.\n[Plan]\nAdmit. Rad Onc consult. Stent removal 2 wks.",
            8: "We performed a rigid bronchoscopy to manage this patient's malignant airway obstruction and remove an embedded metallic stent. The right mainstem had significant tumor, and the left held the old stent which was overgrown with tissue and full of pus. We performed a lavage for culture. Using the rigid scope, APC, and balloons, we carefully dissected the metallic stent from the left mainstem and removed it. We also debulked the tumor on the right. Finally, we customized a silicone Y-stent and deployed it to stent open the trachea and both mainstems. The patient was stable at the end of the procedure.",
            9: "PROCEDURE: Rigid bronchoscopy with foreign body retrieval and stent insertion. INDICATION: Malignancy and retained stent. FINDINGS: TBM and bilateral obstruction. ACTION: Diagnostic bronchoscopy performed. Rigid scope utilized. The embedded stent in the left mainstem was liberated using APC and balloon dilation, then extracted. Tumor in the right mainstem was ablated. A customized Y-stent was implanted. CONCLUSION: Airway patency restored."
        },
        3: { # Note 4: Airway Injury, Pneumothorax, Procedure Aborted
            1: "Indication: Left mainstem obstruction (Wegener's).\nProcedure: Rigid bronchoscopy, APC, Balloon Dilation, Fibrin Glue, Chest Tube.\nFindings: LMS 90-100% stenosed. Attempted recanalization (knife, balloon, APC, coring).\nComplication: Visualization of pulsatile vessel (PA) via false lumen. No rupture.\nAction: Fibrin glue applied. Procedure aborted. Patient intubated. Chest tube (14F) placed for pneumothorax.\nPlan: ICU. CT Surgery consult. CT Chest.",
            2: "OPERATIVE SUMMARY: The patient underwent attempted rigid bronchoscopic recanalization of a complete left mainstem stenosis secondary to granulomatosis with polyangiitis. Despite methodical dissection using radial cuts, balloon dilation, and APC, the distal lumen could not be identified. At 3cm depth, a pulsatile structure consistent with the pulmonary artery was visualized through a false lumen. The procedure was immediately aborted. Fibrin sealant was applied. A subsequent pneumothorax necessitated tube thoracostomy. The patient remains intubated for critical care management and surgical evaluation.",
            3: "Billing Codes:\n- 31641: Relief of stenosis (APC, mechanical).\n- 31630-59: Balloon dilation (distinct effort).\n- 32551: Chest tube placement for pneumothorax complication.\nNote: High complexity. Procedure aborted due to iatrogenic injury/risk (PA exposure).",
            4: "Procedure: Rigid Bronch/Attempted Dilation\nComplication: Airway Perforation/Pneumo\nSteps:\n1. GA. Flex scope showed complete LMS blockage.\n2. Switched to Rigid. Used knife, balloon, APC to try to open it.\n3. Saw pulmonary artery through a hole in the airway. Stopped immediately.\n4. Put fibrin glue in.\n5. Patient got a pneumothorax -> put in pigtail chest tube.\n6. Sent to ICU intubated.\nPlan: CT Surgery consult.",
            5: "Attempted to open up the left mainstem today patient has wegener's granulation blockage was total we tried everything knife balloon apc rigid coring managed to get about 3cm in but then we saw the pulmonary artery beating through a hole in the airway wall scary stuff so we stopped put in glue and intubated him cxr showed a pneumo so we put a chest tube in sending him to the picu hope he doesnt need a pneumonectomy.",
            6: "The procedure was performed in the main operating room. I-gel LMA was placed for initial airway inspection and the diagnostic flexible bronchoscope was inserted through the airway device. The vocal cords were visualized and normal. The upper trachea was normal. The distal third of the trachea was erythematous and inflamed in a circumferential pattern but without and endoluminal obstruction. On the right there was minimal structuring of the BI . On the left the proximal mainstem was about 90% obstructed circumferentially and approximately 1 cm into the left mainstem the airway was completely occluded. Radial knife cuts were performed within the proximal left mainstem followed by attempted CRE balloon dilatation however due to the proximal obstruction dilatation was difficult as only the balloon tip could be inserted into the left mainstem due to the complete distal obstruction. We attempted to place a jagwire through the obstruction as well but unsuccessfully. The flexible bronchoscope was removed and the 12 mm ventilating rigid bronchoscope was subsequently inserted into the mid trachea and attached to the jet ventilator. The rigid optic was then removed and the flexible bronchoscope was inserted through the rigid bronchoscope. At this point we performed APC to the left maintem followed by gentile shaving of coagulated tissue which we repeated multiple times attempting to slowly re-cannulate the airway. We periodically would reinsert the CRE balloon and dilate as the airway lumen slowly re-opened but we were unable to visualize any distal airway. This was performed in a slow methodical fashion given the concern for airway perforation without obvious distal airway targets however once we had dilated approximately 3 cm into the left mainstem a pulsatile vessel was seen which was likely the pulmonary artery through a small (2mm) false lumen. The PA was intact and there was no evidence of rupture. At this point to protect from major vascular bleeding we instilled fibrin glue into the left mainstem after which we removed the rigid bronchoscope and intubated the patient. Chest radiograph was performed which showed his previously elevated left hemi-diaphragm was significantly lower and there was a questionable deep sulcus concerning for pneumothorax and in the setting of a known airway tear and need for positive pressure ventilation felt that chest tube placement was warranted. After prepping the left mid-axillary area a 14F pigtail catheter was placed without complications and the patient was transferred to the PICU in stable condition.",
            7: "[Indication]\nLeft mainstem obstruction (GPA).\n[Anesthesia]\nGeneral.\n[Description]\n1. Flex bronch: Total LMS occlusion.\n2. Rigid bronch: Attempted recanalization w/ knife, balloon, APC.\n3. Complication: False lumen created, PA visualized. Procedure halted.\n4. Intervention: Fibrin glue applied. Patient intubated.\n5. Chest tube placed for pneumothorax.\n[Plan]\nICU. CT Surgery consult. CT Chest.",
            8: "We attempted to open a complete blockage of the left mainstem bronchus caused by Wegener's granulomatosis. Using a rigid bronchoscope, we employed multiple techniques including electrosurgery, balloon dilation, and coring to tunnel through the scar tissue. Unfortunately, after advancing about 3cm, we encountered the pulmonary artery via a false lumen. We immediately stopped, applied fibrin glue to seal the defect, and intubated the patient. A post-procedure x-ray suggested a pneumothorax, so we placed a chest tube. The patient is currently stable in the ICU awaiting surgical opinion.",
            9: "PROCEDURE: Rigid bronchoscopy with attempted recanalization and tube thoracostomy. INDICATION: Left mainstem stenosis. FINDINGS: Complete occlusion. ACTION: Recanalization attempted via electrocautery, dilation, and APC. A false lumen revealing the pulmonary artery was encountered. The procedure was terminated. Fibrin sealant was instilled. A chest tube was inserted for subsequent pneumothorax. DISPOSITION: ICU."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for names and ages to correspond with the 4 notes.
    Since there are only 4 notes, we map indices 0-3.
    """
    return [
        {"idx": 0, "orig_name": "Logan Pierce", "orig_age": 67, "names": ["John Vance", "Arthur Higgins", "Robert Kinsley", "William O'Connor", "James P. Miller", "Edward Stone", "Richard Davis", "Thomas Clark", "Gary Wright"]},
        {"idx": 1, "orig_name": "Patricia Morales", "orig_age": 63, "names": ["Sarah Jenkins", "Linda Carter", "Nancy Hughes", "Karen Smith", "Barbara Lopez", "Mary Ann Davidson", "Susan White", "Margaret Lewis", "Betty King"]},
        {"idx": 2, "orig_name": "Ethan Cole", "orig_age": 70, "names": ["Michael Foster", "Robert G. Turner", "David Myers", "Joseph Anderson", "Frank Mitchell", "Paul Reynolds", "George Baker", "Kenneth Roberts", "Steven Phillips"]},
        {"idx": 3, "orig_name": "Renee Thompson", "orig_age": 59, "names": ["Marie Hall", "Patricia Campbell", "Elizabeth Allen", "Jennifer Young", "Linda Hernandez", "Barbara King", "Dorothy Wright", "Helen Scott", "Carol Green"]}
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
        # Use a default age if 'patient_age' is missing or null in original, though we prefer existing
        orig_age = 60 # Default fallback
        if "registry_entry" in original_note and "patient_demographics" in original_note["registry_entry"]:
             # Note: The source json has 'age_years' inside 'patient_demographics' which is often null in the example
             # But let's check registry_entry root or demographics
             pass # We will use the base_data mock age as the starting point since source is null
        
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
                note_entry["note_text"] = "MISSING VARIATION TEXT"

            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                # Update MRN
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"SYN_{idx}_{style_num}_{random.randint(1000,9999)}"
                
                # Update Procedure Date
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update Age (The source JSON structure puts age in patient_demographics -> age_years)
                if "patient_demographics" in note_entry["registry_entry"]:
                    if note_entry["registry_entry"]["patient_demographics"] is None:
                        note_entry["registry_entry"]["patient_demographics"] = {}
                    note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age

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
    output_filename = output_dir / "synthetic_bronch_notes_part_013.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()