import json
import random
import datetime
import copy
from pathlib import Path

# Configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_092.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date object between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Mock names and original ages for the 10 notes in part_092.
    Indices 0-4: Airway Dilation Notes
    Indices 5-9: Cryotherapy Notes
    """
    return [
        # --- Airway Dilation Notes ---
        {"idx": 0, "orig_name": "Margaret A. Thompson", "orig_age": 68, "names": ["Helen R. Davis", "Martha Lewis", "Joan P. Miller", "Betty K. Wilson", "Dorothy Evans", "Nancy T. Roberts", "Alice Clark", "Shirley Wright", "Ruth Hall"]},
        {"idx": 1, "orig_name": "Robert J. Williams", "orig_age": 53, "names": ["James L. Carter", "William H. Turner", "David R. Phillips", "Michael S. Campbell", "Richard A. Parker", "Joseph E. Evans", "Thomas G. Edwards", "Charles B. Collins", "Daniel F. Stewart"]},
        {"idx": 2, "orig_name": "Maria L. Garcia", "orig_age": 76, "names": ["Carmen Rodriguez", "Elena M. Martinez", "Rosa I. Hernandez", "Ana P. Lopez", "Teresa G. Gonzalez", "Lucia D. Perez", "Silvia A. Sanchez", "Isabel R. Ramirez", "Dolores J. Torres"]},
        {"idx": 3, "orig_name": "James T. Anderson", "orig_age": 59, "names": ["Robert K. Peterson", "John D. Gray", "William M. Ramirez", "David L. Hughes", "Richard P. Price", "Joseph T. Bennet", "Charles H. Wood", "Thomas J. Barnes", "Christopher L. Ross"]},
        {"idx": 4, "orig_name": "Thi H. Nguyen", "orig_age": 72, "names": ["Mai L. Tran", "Kim T. Pham", "Lan P. Le", "Hoa K. Hoang", "Bich N. Do", "Tuyet V. Bui", "Hue M. Dang", "Phuong T. Vo", "Thu A. Duong"]},
        
        # --- Cryotherapy Notes ---
        {"idx": 5, "orig_name": "Carlos R. Martinez", "orig_age": 66, "names": ["Juan P. Rivera", "Jose M. Gomez", "Luis A. Diaz", "Pedro S. Reyes", "Manuel O. Morales", "Antonio R. Ortiz", "Jorge L. Gutierrez", "Ricardo E. Chavez", "Miguel A. Ramos"]},
        {"idx": 6, "orig_name": "Patricia A. Johnson", "orig_age": 63, "names": ["Linda S. Williams", "Barbara J. Jones", "Elizabeth M. Brown", "Jennifer L. Davis", "Maria C. Miller", "Susan K. Wilson", "Margaret R. Moore", "Dorothy A. Taylor", "Lisa P. Anderson"]},
        {"idx": 7, "orig_name": "William M. Davis", "orig_age": 69, "names": ["James R. Wilson", "John T. Taylor", "Robert E. Moore", "Michael W. Jackson", "David P. White", "Richard L. Harris", "Joseph A. Martin", "Thomas S. Thompson", "Charles D. Garcia"]},
        {"idx": 8, "orig_name": "Sandra K. Brown", "orig_age": 75, "names": ["Patricia L. Davis", "Linda M. Wilson", "Barbara J. Taylor", "Elizabeth A. Moore", "Jennifer S. Jackson", "Maria D. White", "Susan E. Harris", "Margaret K. Martin", "Dorothy R. Thompson"]},
        {"idx": 9, "orig_name": "David H. Lee", "orig_age": 61, "names": ["Michael J. Kim", "James S. Park", "Robert Y. Choi", "John W. Chen", "William D. Wang", "Richard T. Liu", "Joseph K. Zhang", "Thomas L. Yang", "Charles H. Huang"]}
    ]

def get_variations():
    """
    Returns a dictionary of text variations.
    Key: Note Index (0-9) -> Key: Style Index (1-9) -> Value: Variation Text
    """
    variations = {
        # Note 0: Margaret Thompson (Subglottic Stenosis, Balloon)
        0: {
            1: "Pre-op: Post-intubation subglottic stenosis.\nAnesthesia: GA, Jet ventilation.\nAction: Flex bronch. Web-like stenosis 2cm below cords (70%). CRE Balloon dilation: 10mm -> 12mm -> 14mm (8 ATM x 60s). \nResult: Lumen 90% patent. Minimal bleeding.\nPlan: D/C. Re-scope 6-8 wks.",
            2: "INDICATION: The patient, a 68-year-old female, presented with stridor following prolonged intubation. Radiographic evaluation demonstrated critical subglottic stenosis.\nPROCEDURE: General anesthesia utilizing jet ventilation was induced. Bronchoscopic inspection revealed a fibrous circumferential stricture 2 cm subglottically, compromising 70% of the lumen. Intervention proceeded with sequential hydrostatic balloon dilation utilizing a CRE catheter graduated to 14mm at 8 atmospheres. Post-procedural assessment confirmed restoration of airway caliber to approximately 90% of expected diameter. Hemostasis was maintained.\nDISPOSITION: The patient was transferred to the PACU in stable condition.",
            3: "Procedure: Bronchoscopy with Balloon Dilation (CPT 31630).\nTechnique: Flexible bronchoscope introduced via oral route under general anesthesia (Jet Ventilation).\nFindings: 70% stenosis identified in subglottic trachea.\nIntervention: Controlled Radial Expansion (CRE) balloon dilator utilized. Sequential inflations performed at 10mm, 12mm, and 14mm diameters. Pressure maintained at 8 ATM for 60 seconds per cycle.\nOutcome: Successful dilation to 14mm; >90% patency achieved. Medical necessity supported by symptomatic stenosis.",
            4: "Resident Procedure Note\nPatient: [Name]\nAttending: Dr. Rodriguez\nDiagnosis: Subglottic stenosis\nSteps:\n1. Time out. GA/Jet vent.\n2. Scope inserted. Saw 70% stenosis subglottic.\n3. Dilation performed: Used CRE balloon. Sizes 10, 12, 14mm.\n4. Held for 60s at 8atm.\n5. Checked airway: Looks good, 90% open.\nPlan: PPIs, follow up 2 months.",
            5: "Procedure note for [Name] for the tracheal stenosis dilation used jet ventilation patient asleep. Went in with the flexible scope saw the narrowing about 70 percent block. Did the balloon dilation started at 10 went up to 14 millimeters held it for a minute each time at 8 atmospheres. Opened up nice to about 90 percent no tearing really just a little blood. Woke up fine sending to recovery plan for repeat scope later.",
            6: "The patient was brought to the operating room and placed under general anesthesia with jet ventilation. Flexible bronchoscopy revealed circumferential web-like stenosis 2cm below vocal cords with 65-70% luminal obstruction. Sequential balloon dilation performed using CRE balloon dilator, starting at 10mm, progressed to 12mm, then 14mm over three cycles. Each inflation held for 60 seconds at 8 ATM. Post-dilation exam showed adequate lumen restored to approximately 90% patency. No mucosal tears. Minimal bleeding controlled with observation.",
            7: "[Indication]\nPost-intubation subglottic stenosis, symptomatic with stridor.\n[Anesthesia]\nGeneral anesthesia, Jet ventilation.\n[Description]\nCircumferential stenosis 2cm below cords (70%). Sequential CRE balloon dilation performed (10, 12, 14mm) at 8 ATM x 60s. Lumen restored to 90% patency. Minimal bleeding.\n[Plan]\nDischarge today. PPI. Repeat bronchoscopy 6-8 weeks.",
            8: "Ms. [Name] was brought to the suite for management of her subglottic stenosis. Under general anesthesia with jet ventilation, we advanced the bronchoscope and visualized the stricture, which was narrowing the airway by about 70%. We used a CRE balloon to dilate the area, sequentially increasing the size from 10mm to 14mm. We held the inflations for 60 seconds at 8 atmospheres. The airway opened up significantly to about 90% patency. There was only minimal bleeding which stopped on its own.",
            9: "PRE-OP DX: Post-intubation tracheal constriction\nPROCEDURE: Bronchoscopy with pneumatic expansion of tracheal constriction\nDETAILS: Patient anesthetized via jet ventilation. Scope revealed circumferential web-like constriction 2cm below vocal cords with 70% blockage. Sequential pneumatic expansion executed using CRE dilator, starting at 10mm, progressed to 14mm. Each inflation maintained for 60 seconds. Post-expansion exam showed adequate airway restored to 90% openness. No mucosal lacerations."
        },
        # Note 1: Robert Williams (RMS Stenosis, Rigid Dilation)
        1: {
            1: "Dx: RMS anastomotic stenosis (post-transplant).\nAnesthesia: GA, 8.0 ETT.\nProcedure:\n- Flex bronch: 80% web stenosis RMS.\n- Rigid bronch inserted.\n- Rigid dilation: 7mm -> 9mm -> 11mm.\n- Result: 12mm lumen achieved.\nComplications: Mild edema, no bleeding.\nPlan: Admit obs. Re-scope 4 weeks.",
            2: "HISTORY: The patient, status post bilateral lung transplantation, presented with dyspnea. Surveillance imaging suggested anastomotic stricture.\nOPERATIVE REPORT: Under general anesthesia (ETT 8.0), flexible bronchoscopy confirmed a severe, web-like stenosis at the right mainstem (RMS) anastomosis (80% obstruction). Transition was made to rigid bronchoscopy. Mechanical dilation was performed utilizing sequential rigid dilators sized 7mm through 11mm. The final luminal diameter was estimated at 12mm. Inspection revealed mild mucosal edema but hemostasis was preserved.\nCONCLUSION: Successful rigid dilation of transplant anastomosis.",
            3: "CPT: 31630 (Bronchoscopy with dilation).\nMethod: Rigid bronchoscopy with mechanical dilation.\nTarget: Right Mainstem Bronchus (Anastomosis).\nDetails:\n- Initial inspection via flexible scope.\n- Rigid scope introduction.\n- Sequential passage of rigid dilators (7mm, 9mm, 11mm).\n- Final diameter achieved: 12mm.\nJustification: Severe symptomatic stenosis (80%) requiring rigid mechanics for patency.",
            4: "Resident Note\nPatient: [Name]\nDx: Transplant stenosis RMS\nProcedure: Rigid dilation\nSteps:\n1. GA, ETT placed.\n2. Looked with flex scope, saw tight RMS stenosis.\n3. Put in rigid scope.\n4. Used rigid dilators 7, 9, 11 mm.\n5. Opened up to ~12mm.\n6. No bleeding.\nPlan: Obs, surveillance bronch in a month.",
            5: "Procedure note for [Name] lung transplant patient with the RMS stenosis. General anesthesia tube size 8. Looked with the flex scope confirmed the web about 80 percent blocked. Switched to rigid bronchoscopy and did the dilation with the rigid tubes 7 9 and 11 millimeters. Got it open to about 12 millimeters looks good. Mild swelling no real bleeding. Watch him overnight thanks.",
            6: "Flexible bronchoscopy with rigid bronchoscopy and bronchial dilation. 53 y/o male 8 months post bilateral lung transplant with worsening dyspnea. Surveillance bronch showed 80% stenosis at right mainstem anastomosis. General anesthesia via ETT 8.0. Flexible bronch confirmed severe web-like stenosis at RMS anastomosis. Rigid bronchoscopy performed through laryngeal mask. Sequential dilation with rigid dilators (7mm, 9mm, 11mm). Final lumen approximately 12mm achieved. Mild mucosal edema post-dilation. No significant bleeding. Left system normal.",
            7: "[Indication]\nPost-lung transplant anastomotic stenosis, RMS (80%).\n[Anesthesia]\nGeneral, ETT 8.0 -> Rigid Bronchoscopy.\n[Description]\nWeb-like stenosis identified. Rigid dilation performed sequentially (7mm, 9mm, 11mm). Final lumen ~12mm. Mucosa edematous but intact.\n[Plan]\nInpatient observation. Surveillance bronchoscopy 4 weeks.",
            8: "Mr. [Name] underwent a dilation of his right mainstem bronchus today due to a narrowing at his transplant connection. We started with general anesthesia and a standard breathing tube. After confirming the 80% blockage with a flexible scope, we switched to a rigid bronchoscope. We used a series of rigid dilators, increasing in size from 7mm to 11mm, to mechanically open the airway. By the end, we achieved a 12mm opening. There was some swelling but no bleeding.",
            9: "Dx: RMS bronchus constriction post lung transplant\nProcedure: Flexible bronchoscopy with rigid bronchoscopy and bronchial expansion\nDETAILS: General anesthesia via ETT. Flexible bronch confirmed severe web-like constriction at RMS anastomosis. Rigid bronchoscopy performed. Sequential expansion with rigid instruments (7mm, 9mm, 11mm). Final caliber approximately 12mm achieved. Mild mucosal edema post-expansion. No significant hemorrhage."
        },
        # Note 2: Maria Garcia (LMS Granulation, Balloon)
        2: {
            1: "Indication: LMS stenosis (granulation tissue post-stent).\nAnesthesia: GA, 7.5 ETT.\nFindings: 60% LMS obstruction, granulation tissue 1cm from carina.\nAction: CRE Balloon dilation (12mm x 40mm). 3 cycles @ 6 ATM.\nResult: 85% patency. Minor mucosal tear, no active bleed.\nPlan: Obs. CXR. F/U 6 wks.",
            2: "OPERATIVE NARRATIVE: The patient presented with recurrent dyspnea following silicone stent removal. Inspection of the left mainstem (LMS) bronchus revealed circumferential granulation tissue resulting in 60% luminal compromise. Therapeutic intervention consisted of balloon bronchoplasty. A 12mm x 40mm CRE balloon was deployed and inflated to 6 atmospheres for three 60-second cycles. Post-dilation assessment demonstrated improved patency to 85%. A superficial mucosal disruption was noted at the 3 o'clock position, requiring no hemostatic intervention.",
            3: "Service: Bronchoscopy/Dilation (31630).\nSite: Left Mainstem Bronchus.\nPathology: Granulation tissue stenosis (post-stent).\nTechnique: Balloon dilation.\nEquipment: 12mm x 40mm CRE balloon.\nMetrics: Inflated to 6 ATM x 3 cycles.\nOutcome: Obstruction reduced from 60% to 15%. Minor mucosal tear noted (expected outcome of tissue disruption).",
            4: "Resident Procedure Note\nPatient: [Name], 76F\nProcedure: LMS Balloon Dilation\nSteps:\n1. Intubated 7.5 ETT.\n2. Bronch showed granulation tissue in LMS (60% blocked).\n3. Used 12mm balloon.\n4. Dilated 3 times at 6 atm.\n5. Airway opened to 85%.\n6. Small tear, no bleeding.\nPlan: CXR, follow up bronch 6 weeks.",
            5: "Note for [Name] she has that granulation tissue in the left mainstem after we took the stent out. General anesthesia tube 7.5. Scope showed about 60 percent blockage. Used the balloon 12 by 40 millimeters did three inflations at 6 atmospheres. Opened up nicely to about 85 percent. Little tear at 3 oclock but stopped bleeding on its own. Recovery and check xray.",
            6: "Bronchoscopy with balloon dilation of left mainstem bronchus. 76 y/o female with history of LMS silicone stent removed 3 months ago, now with recurrent dyspnea. CT chest shows 60% narrowing at prior stent site with granulation tissue. Flexible bronchoscopy performed. RMS and right bronchial tree patent. LMS with circumferential granulation tissue causing 55-60% obstruction starting 1cm from carina extending 1.5cm. Balloon dilation performed with 12mm x 40mm CRE balloon, 3 cycles at 6 ATM x 60 seconds each. Post-dilation patency approximately 85%. Small mucosal tear at 3 o'clock position, no active bleeding.",
            7: "[Indication]\nLMS stenosis (granulation tissue) post-stent removal.\n[Anesthesia]\nGeneral, ETT 7.5.\n[Description]\n60% obstruction LMS. Balloon dilation (12mm x 40mm) performed x3 at 6 ATM. Patency improved to 85%. Minor mucosal tear, hemostasis stable.\n[Plan]\nOvernight observation. CXR. Repeat bronch 6 weeks.",
            8: "Mrs. [Name] underwent a bronchoscopy to treat scar tissue narrowing her left main airway. Under general anesthesia, we found the granulation tissue was blocking about 60% of the airway. We used a 12mm balloon to dilate the area, inflating it three times at 6 atmospheres of pressure. This successfully opened the airway to about 85% normal size. There was a tiny tear in the lining, which is common, and it did not bleed significantly.",
            9: "PREOPERATIVE DIAGNOSIS: Left mainstem bronchus constriction secondary to granulation tissue\nPROCEDURE: Bronchoscopy with pneumatic expansion of left mainstem bronchus\nFINDINGS: LMS with circumferential granulation tissue causing 60% blockage. Pneumatic expansion performed with 12mm x 40mm CRE balloon, 3 cycles at 6 ATM. Post-expansion patency approximately 85%. Small mucosal fissure at 3 o'clock position, no active hemorrhage."
        },
        # Note 3: James Anderson (Tracheal Stenosis, Rigid/Balloon)
        3: {
            1: "Dx: Tracheal stenosis (stoma site).\nAnesthesia: GA, Rigid Bronch.\nFindings: Complex stenosis (granulation/web) 75% obstruction.\nAction: Rigid dilation (Size 8->9) followed by Balloon (15mm, 10 ATM).\nResult: 80% patency achieved.\nPlan: Admit. Consider T-tube if recurrence.",
            2: "OPERATIVE SUMMARY: The patient, with a history of tracheostomy, presented with complex tracheal stenosis. Under general anesthesia, rigid bronchoscopy was initiated. Evaluation of the prior stoma site revealed a mixed stenosis (granulation/fibrosis) occluding 75% of the lumen. Mechanical dilation was first performed with the rigid barrel (sizes 8 and 9), followed by definitive hydrostatic dilation using a 15mm balloon at 10 atmospheres. Final inspection demonstrated an estimated 80% luminal patency.",
            3: "Code: 31630 (Tracheal Dilation).\nModality: Combined Rigid and Balloon Dilation.\nLocation: Mid-trachea (prior stoma).\nTechnique:\n1. Mechanical dilation via rigid scope (Size 9).\n2. Balloon dilation (15mm diameter) x 3 inflations @ 10 ATM.\nOutcome: Stenosis reduction from 75% to 20%.",
            4: "Resident Note\nPatient: [Name]\nProcedure: Tracheal Dilation (Rigid + Balloon)\nSteps:\n1. GA, rigid scope inserted.\n2. Saw 75% stenosis at old trach site.\n3. Dilated with the rigid scope first.\n4. Then used 15mm balloon at 10 atm.\n5. Airway looks 80% open now.\nPlan: Obs, maybe T-tube next time.",
            5: "Mr [Name] here for the tracheal stenosis dilation. He had a trach before. Used the rigid scope general anesthesia. Saw the narrowing about 75 percent block granulation and scar. Dilated with the rigid tube then used the big 15 millimeter balloon. Inflated it three times. Looks much better about 80 percent open. No bleeding. Thinking maybe a t-tube if it comes back.",
            6: "Rigid bronchoscopy with mechanical dilation and balloon dilation. 59 y/o male with history of traumatic brain injury requiring prolonged mechanical ventilation and tracheostomy 4 months ago. Progressive stridor. General anesthesia with spontaneous ventilation through rigid bronchoscope. At level of prior tracheostomy site, complex stenosis noted with combination of granulation tissue and fibrous web causing 70-75% obstruction. Initial mechanical dilation with rigid bronchoscope (size 8, then 9). Balloon dilation with 15mm diameter balloon x 3 inflations at 10 ATM. Final patency approximately 80%.",
            7: "[Indication]\nPost-tracheostomy tracheal stenosis (75%).\n[Anesthesia]\nGeneral, Rigid Bronchoscope.\n[Description]\nComplex stenosis at stoma site. Mechanical dilation with rigid scope (size 9). Balloon dilation (15mm) x3 at 10 ATM. Patency improved to 80%.\n[Plan]\nInpatient obs. Pulmonary rehab. Re-eval 4-6 weeks.",
            8: "We treated Mr. [Name] for narrowing of his windpipe at his old tracheostomy site. Using a rigid bronchoscope under general anesthesia, we saw the airway was 75% blocked by scar tissue. We used the rigid scope itself to gently stretch the area, followed by a 15mm balloon which we inflated to high pressure to fully dilate the stricture. The airway is now about 80% open, which is a good result.",
            9: "PREOP DIAGNOSIS: Tracheal constriction post tracheostomy\nPROCEDURE: Rigid bronchoscopy with mechanical expansion and pneumatic expansion\nDETAILS: At level of prior tracheostomy site, complex constriction noted causing 75% obstruction. Initial mechanical expansion with rigid bronchoscope. Pneumatic expansion with 15mm diameter balloon x 3 inflations at 10 ATM. Final patency approximately 80%."
        },
        # Note 4: Thi Nguyen (Bronchus Intermedius, Balloon)
        4: {
            1: "Indication: BI stenosis (post-sleeve resection).\nAnesthesia: Moderate sedation (Midaz/Fent).\nFindings: 70% pinhole stenosis at anastomosis.\nAction: Sequential balloon dilation (8mm->10mm->12mm). Max 6 ATM.\nResult: 85% patency. RLL visible.\nPlan: Antibiotics. F/U 8 wks.",
            2: "PROCEDURE NOTE: The patient, status post RLL sleeve resection, presented with anastomotic stenosis. Under moderate sedation, flexible bronchoscopy identified a severe circumferential stricture at the bronchus intermedius (70% obstruction). A graded balloon dilation strategy was employed utilizing 8mm, 10mm, and 12mm balloons. Inflation pressures reached 6 atmospheres. Post-intervention inspection confirmed restoration of luminal patency to 85%, permitting visualization of the basilar segments.",
            3: "CPT: 31630 (Bronchial Dilation).\nTarget: Bronchus Intermedius (Anastomosis).\nTechnique: Balloon dilation under moderate sedation.\nDetails:\n- Pre-dilation: 70% stenosis.\n- Device: CRE Balloon (12mm max).\n- Protocol: Sequential sizing 8mm/10mm/12mm.\n- Post-dilation: 85% patency.\nMedical Necessity: Symptomatic post-surgical stenosis.",
            4: "Resident Note\nPatient: [Name]\nProcedure: BI Dilation\nSteps:\n1. Mod sedation.\n2. Scope in right nare.\n3. Found tight stenosis at BI (70%).\n4. Used balloon: 8mm, then 10mm, then 12mm.\n5. Airway opened to 85%.\n6. Minimal bleeding.\nPlan: Continue abx, re-scope in 2 months.",
            5: "Procedure on [Name] for the bronchus intermedius stenosis she had that sleeve surgery. Moderate sedation used midaz and fentanyl. Went in through the nose saw the narrowing about 70 percent. Used the balloons started small 8mm went to 10 then 12. Held them for a minute. Opened up real nice can see the lower lobe now. Little bleeding stopped on its own. antibiotics and follow up.",
            6: "Flexible bronchoscopy. Balloon dilation of bronchus intermedius. 72 y/o female with history of RLL sleeve resection 18 months ago. CT demonstrates 70% stenosis at surgical anastomosis. Moderate sedation. At bronchus intermedius, severe circumferential stenosis noted at anastomotic site with approximately 65-70% obstruction. Sequential balloon dilation performed: 8mm x 20mm CRE balloon, then 10mm, finally 12mm. Post-dilation patency estimated at 80-85%. RLL basilar segments now visible and patent. Minimal bleeding, resolved spontaneously.",
            7: "[Indication]\nPost-surgical anastomotic stenosis, Bronchus Intermedius (70%).\n[Anesthesia]\nModerate Sedation.\n[Description]\nSequential balloon dilation performed (8mm, 10mm, 12mm). Max pressure 6 ATM. Lumen restored to 85%. RLL visualized. Minimal bleeding.\n[Plan]\nContinue antibiotics. Surveillance bronchoscopy 8 weeks.",
            8: "Ms. [Name] required dilation of her airway due to scar tissue from her previous lung surgery. Using moderate sedation, we passed a scope through her nose and found the intermediate bronchus was 70% narrowed. We successfully stretched this open using a series of balloons, ending with a 12mm size. The airway is now about 85% open and we can clearly see the lower lung segments.",
            9: "PREOPERATIVE DIAGNOSIS: Bronchus intermedius constriction\nPROCEDURE: Balloon expansion of bronchus intermedius\nNARRATIVE: Severe circumferential constriction noted at anastomotic site with 70% obstruction. Sequential pneumatic expansion performed: 8mm, then 10mm, finally 12mm balloon. Post-expansion patency estimated at 85%. RLL basilar segments now visible and patent. Minimal hemorrhage."
        },
        # Note 5: Carlos Martinez (RUL SCC, Cryo)
        5: {
            1: "Indication: RUL SCC obstruction (80%). Palliative.\nAnesthesia: GA, Rigid.\nAction: Cryotherapy (Erbe). 7 cycles (30s each) to RUL/BI tumor.\nResult: Necrosis/Debridement. RUL 50% open, BI 80% open.\nComplications: Mod bleeding (controlled).\nPlan: Repeat 1 week. Rad Onc consult.",
            2: "OPERATIVE REPORT: The patient presented with advanced squamous cell carcinoma causing critical RUL obstruction. Under general anesthesia via rigid bronchoscopy, a large exophytic tumor was visualized occluding 80% of the RUL and extending into the bronchus intermedius. Cryotherapeutic ablation was executed using an Erbe flexible probe. Multiple freeze-thaw cycles were applied to the tumor surface. Necrotic tissue was mechanically debrided. Hemostasis was achieved following moderate hemorrhage. Luminal patency was significantly improved.",
            3: "CPT: 31641 (Tumor destruction via cryotherapy).\nMethod: Rigid bronchoscopy with cryo-ablation.\nTarget: RUL and Bronchus Intermedius.\nDetails:\n- Tumor debulking performed.\n- 7 freeze-thaw cycles utilized.\n- Mechanical debridement of necrotic tissue.\n- Hemostasis managed (EBL 75ml).\nOutcome: Relief of obstruction (RUL 80%->50% block).",
            4: "Resident Note\nPatient: [Name]\nDx: RUL SCC tumor\nProcedure: Cryo debulking\nSteps:\n1. GA, Rigid scope.\n2. Big tumor in RUL/BI.\n3. Used cryo probe to freeze it (7 cycles).\n4. Pulled out dead tissue.\n5. Bleeding controlled with cold saline.\n6. Airway looks better.\nPlan: Do it again next week.",
            5: "Procedure for [Name] palliative debulking for the cancer. Rigid bronchoscopy general anesthesia. Big tumor blocking the right upper lobe. Used the cryo probe froze it a bunch of times about 30 seconds each. Pulled out the dead pieces. Some bleeding about 75cc but stopped it with epinephrine. Got the airway open a bit more. Will bring him back next week for more.",
            6: "Rigid bronchoscopy with cryotherapy ablation. 66 y/o male with advanced squamous cell lung cancer. Progressive dyspnea with near-complete RUL obstruction. Large exophytic tumor at RUL orifice causing 80% obstruction with extension into bronchus intermedius. Cryotherapy performed using Erbe Erbokryo CA unit with flexible cryoprobe. Multiple freeze-thaw cycles applied to tumor surface. Significant tumor necrosis achieved. Necrotic tissue debrided with rigid suction. Post-procedure patency improved to approximately 50% at RUL, BI now 80% patent.",
            7: "[Indication]\nMalignant airway obstruction (SCC), RUL (80%).\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nCryotherapy ablation performed (7 cycles, 30s). Necrotic tissue debrided. RUL patency improved to 50%, BI to 80%. Moderate bleeding controlled.\n[Plan]\nRepeat bronchoscopy 1 week. Rad Onc consult.",
            8: "We performed a palliative procedure on Mr. [Name] to clear the tumor blocking his right lung. Using a rigid bronchoscope, we applied freezing therapy (cryotherapy) to the tumor mass in the right upper lobe. This killed the surface tissue which we then removed. We managed to open the airway significantly, though some blockage remains. There was some bleeding which we controlled during the case.",
            9: "PRE-OP DX: Endobronchial squamous cell carcinoma, RUL with 80% obstruction\nPROCEDURE: Rigid bronchoscopy with cryotherapy destruction\nDETAILS: Large exophytic tumor at RUL orifice. Cryotherapy performed using Erbe unit. Multiple freeze-thaw cycles applied. Significant tumor necrosis achieved. Necrotic tissue extracted with rigid suction. Post-procedure patency improved. Moderate hemorrhage controlled."
        },
        # Note 6: Patricia Johnson (LMS Carcinoid, Cryo)
        6: {
            1: "Dx: LMS Carcinoid (40% block).\nAnesthesia: GA, 7.5 ETT.\nAction: Cryotherapy ablation (Erbe). 5 cycles (20s freeze).\nResult: Tumor blanched/devitalized. Lumen stable.\nPlan: D/C. Re-scope 6 wks.",
            2: "PROCEDURE NOTE: The patient presented for management of a biopsied LMS carcinoid tumor. Under general anesthesia, the lesion was identified on the posterior wall, causing 40% obstruction. Cryotherapy was selected as the primary modality. Five freeze-thaw cycles were delivered circumferentially to the tumor base using an Erbe probe. Visual confirmation of tissue blanching and early necrosis was obtained. The airway remained patent with no immediate complications.",
            3: "CPT: 31641 (Tumor destruction, cryotherapy).\nTarget: Left Mainstem Bronchus.\nPathology: Typical Carcinoid.\nTechnique: Flexible bronchoscopy with contact cryotherapy.\nDosimetry: 5 cycles, 20s freeze/10s thaw.\nOutcome: Successful ablation/devitalization of tumor mass. No biopsy taken (prior dx).",
            4: "Resident Note\nPatient: [Name]\nDx: LMS Carcinoid\nProcedure: Cryo ablation\nSteps:\n1. GA, ETT.\n2. Saw tumor in LMS (pink, vascular).\n3. Used cryo probe.\n4. Froze it 5 times.\n5. Tumor turned white (dead).\n6. No bleeding.\nPlan: Home today, check back in 6 weeks.",
            5: "Note for [Name] treating the carcinoid in the left main. General anesthesia. Saw the tumor about 40 percent block. Used the cryo probe on it did 5 freezes. Turned white looks dead. No bleeding really. She can go home today check it again in a month and a half.",
            6: "Flexible bronchoscopy with cryotherapy ablation of endobronchial tumor. 63 y/o female with LMS carcinoid tumor. LMS with polypoid tumor arising from posterior wall, 15mm in size, causing approximately 40% obstruction. Cryotherapy performed using Erbe cryoprobe: 5 freeze-thaw cycles applied circumferentially to tumor base. Visible blanching and early necrosis noted. Post-procedure: Tumor appears devitalized. Lumen maintained. No significant bleeding.",
            7: "[Indication]\nLMS Carcinoid tumor (40% obstruction).\n[Anesthesia]\nGeneral, ETT 7.5.\n[Description]\nCryotherapy ablation performed. 5 freeze-thaw cycles to tumor base. Tissue devitalized. No bleeding.\n[Plan]\nDischarge. Surveillance bronchoscopy 6 weeks.",
            8: "Mrs. [Name] came in for treatment of a carcinoid tumor in her left main airway. We used a freezing probe (cryotherapy) to treat the tumor without needing surgery. We applied the freezing cycles five times to the base of the tumor. We could see the tissue turn white, indicating the treatment was effective. She tolerated it well with no bleeding.",
            9: "PREOPERATIVE DIAGNOSIS: Left mainstem endobronchial carcinoid tumor\nPROCEDURE: Flexible bronchoscopy with cryotherapy destruction of endobronchial tumor\nNARRATIVE: LMS with polypoid tumor arising from posterior wall. Cryotherapy performed using Erbe cryoprobe: 5 freeze-thaw cycles applied to tumor base. Visible blanching and early necrosis noted. Post-procedure: Tumor appears devitalized."
        },
        # Note 7: William Davis (RMS Granulation, Spray Cryo)
        7: {
            1: "Indication: RMS granulation (post-stent).\nAnesthesia: Mod Sedation.\nAction: Spray Cryotherapy (TrueFreeze). 10 applications (5s each).\nResult: Blanching/Edema. Expect sloughing.\nPlan: D/C. Re-scope 2 wks.",
            2: "OPERATIVE SUMMARY: The patient presented with recurrent granulation tissue following stent explantation. Flexible bronchoscopy under moderate sedation demonstrated circumferential RMS stenosis (50%). Spray cryotherapy was utilized for ablation (CSA Medical TrueFreeze). Ten total applications of 5 seconds each were delivered to the anterior, posterior, and lateral walls. Immediate mucosal blanching confirmed therapeutic effect. The patient tolerated the procedure without complication.",
            3: "CPT: 31641 (Destruction of lesion, cryotherapy).\nDevice: CSA Medical TrueFreeze (Spray Cryo).\nLocation: Right Mainstem Bronchus.\nIndication: Granulation tissue stenosis.\nTechnique: Non-contact spray ablation.\nApplications: 10 sprays x 5 seconds.\nOutcome: Tissue blanching achieved.",
            4: "Resident Note\nPatient: [Name]\nProcedure: Spray Cryo RMS\nSteps:\n1. Propofol sedation.\n2. Saw granulation tissue in RMS.\n3. Used the spray cryo catheter.\n4. Sprayed 10 times around the airway.\n5. Tissue turned white.\n6. No bleeding.\nPlan: Follow up bronch in 2 weeks to clean it up.",
            5: "Procedure for [Name] granulation tissue in the RMS from that old stent. Used moderate sedation propofol. Went in saw the tissue blocking half the airway. Used the spray cryo machine TrueFreeze. Did about 10 sprays 5 seconds each. Froze it good looks white now. Should fall off in a couple weeks. Recheck him then.",
            6: "Bronchoscopy with cryotherapy for granulation tissue ablation. 69 y/o male s/p RMS silicone stent for malignant CAO. RMS with circumferential granulation tissue at 2cm from carina, 50% obstruction. Cryotherapy (spray cryotherapy, CSA Medical TrueFreeze) applied to granulation tissue: Anterior wall: 3 applications x 5 seconds each. Posterior wall: 3 applications. Lateral walls: 2 applications each. Immediate tissue blanching and edema noted.",
            7: "[Indication]\nRMS granulation tissue (50% stenosis).\n[Anesthesia]\nModerate Sedation.\n[Description]\nSpray cryotherapy (TrueFreeze) applied x10 cycles (5s each). Circumferential blanching achieved. No bleeding.\n[Plan]\nDischarge. Repeat bronchoscopy 2 weeks for debridement.",
            8: "Mr. [Name] had some scar tissue growing back where his stent used to be. We treated this using a spray cryotherapy device, which sprays liquid nitrogen to freeze the tissue without touching it. We treated the entire circle of the airway. The tissue turned white as expected, and it should slough off over the next week or two, opening the airway further.",
            9: "Dx: Recurrent granulation tissue post RMS stent removal\nProcedure: Bronchoscopy with cryotherapy for granulation tissue destruction\nDETAILS: RMS with circumferential granulation tissue, 50% obstruction. Cryotherapy (spray cryotherapy, CSA Medical TrueFreeze) applied to granulation tissue. Immediate tissue blanching and edema noted. Post-treatment lumen slightly improved."
        },
        # Note 8: Sandra Brown (RUL SCLC, Cryo + Debridement)
        8: {
            1: "Dx: RUL SCLC obstruction.\nAnesthesia: GA, Rigid.\nAction: Cryo-adhesion/Debridement. 10 cycles. Tumor core removed.\nResult: RUL 40% open (was 0%). BI 90% open. 100mL blood loss (controlled).\nPlan: ICU. Antibiotics. Repeat 5-7 days.",
            2: "OPERATIVE REPORT: The patient with SCLC presented with RUL collapse. General anesthesia with jet ventilation facilitated rigid bronchoscopy. A friable tumor occluded the RUL and compromised the bronchus intermedius. Cryotherapy (Erbe) was applied for both ablation and adhesion-extraction. Significant tumor bulk was debrided en bloc. The RUL orifice was recanalized to 40% patency. Hemostasis was secured after 100mL blood loss using cold saline lavage.",
            3: "CPT: 31641 (Tumor destruction, cryotherapy).\nMethod: Rigid bronchoscopy.\nTarget: RUL and Bronchus Intermedius.\nTechnique: Cryo-debridement (Freezing and manual extraction).\nFindings: Complete RUL occlusion resolved to partial patency.\nComplications: 100mL hemorrhage, managed intraoperatively.\nDisposition: ICU for monitoring.",
            4: "Resident Note\nPatient: [Name]\nDx: SCLC RUL block\nProcedure: Cryo / Rigid\nSteps:\n1. Rigid scope in.\n2. Tumor blocking RUL completely.\n3. Used cryo to freeze and pull chunks out.\n4. Got a big core out.\n5. RUL is open a bit now (40%).\n6. Bleeding was moderate, used saline.\nPlan: ICU, antibiotics, come back next week.",
            5: "Note for [Name] small cell cancer blocking the right lung. General anesthesia rigid bronch. Tumor was totally blocking the RUL. Used the cryo probe to freeze and pull. Got a lot of it out. RUL is open now maybe 40 percent. Bleeding was about 100cc but we stopped it. Sending her to ICU to watch. Needs chemo.",
            6: "Rigid bronchoscopy. Cryotherapy ablation of endobronchial tumor. Mechanical debridement. 75 y/o female with extensive stage small cell lung cancer. RUL collapse. RMS with tumor extending from RUL orifice, completely occluding RUL takeoff. Cryotherapy (Erbe Erbokryo) applied to tumor bulk. Mechanical debridement using rigid suction and forceps. Tumor core extracted en bloc. Result: RUL orifice now 40% patent (was 0%). BI improved to 90% patency.",
            7: "[Indication]\nSCLC with RUL obstruction/collapse.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nCryo-debridement performed. Tumor core extracted. RUL patency restored to 40%. BI patency 90%. Hemostasis achieved (EBL 100mL).\n[Plan]\nICU admission. IV Antibiotics. Repeat bronchoscopy 5-7 days.",
            8: "Ms. [Name] needed an urgent procedure to open her right upper lung which was blocked by tumor. Using a rigid bronchoscope, we used a freezing probe to grab and pull out large pieces of the tumor. We successfully opened the airway from 0% to about 40%. There was some bleeding which we washed out. She is going to the ICU for close monitoring.",
            9: "PREOPERATIVE DIAGNOSIS: Small cell lung cancer with endobronchial disease\nPROCEDURE: Rigid bronchoscopy with cryotherapy destruction of endobronchial tumor\nNARRATIVE: RMS with tumor extending from RUL orifice. Cryotherapy applied to tumor bulk. Mechanical debridement using rigid suction. Tumor core extracted en bloc. Result: RUL orifice now 40% patent. BI improved to 90% patency."
        },
        # Note 9: David Lee (Tracheal Papillomatosis, Cryo)
        9: {
            1: "Dx: Tracheal Papillomatosis.\nAnesthesia: GA, LMA.\nAction: Cryo ablation of 6 lesions (Mid-trachea). 15 cycles total.\nResult: Lesions blanched/treated. No bleeding.\nPlan: Oral steroids. ENT f/u. Bronch 8-12 wks.",
            2: "PROCEDURE NOTE: The patient with recurrent respiratory papillomatosis underwent bronchoscopic intervention. Under general anesthesia (LMA), the mid-trachea was inspected, revealing six papillomatous lesions (30% obstruction). Cryotherapy was applied systematically using a flexible probe. Each lesion received 2-3 freeze-thaw cycles, totaling 15 applications. Complete blanching of all visible disease was achieved without hemorrhage.",
            3: "CPT: 31641 (Destruction of lesion, cryotherapy).\nPathology: Respiratory Papillomatosis (RRP).\nLocation: Mid-trachea.\nTechnique: Contact cryotherapy.\nDetails: 6 lesions treated, 15 total freeze cycles.\nOutcome: Immediate blanching/destruction of lesions.\nMedical Necessity: Symptomatic airway obstruction.",
            4: "Resident Note\nPatient: [Name]\nDx: Tracheal Papillomas\nProcedure: Cryo ablation\nSteps:\n1. LMA placed.\n2. Saw 6 papillomas in trachea.\n3. Used cryo probe on all of them.\n4. Froze each one 2-3 times.\n5. They turned white.\n6. No bleeding.\nPlan: Steroids, see ENT, come back in 2 months.",
            5: "Mr [Name] here for the papillomas in the trachea. Recurrent issue. General anesthesia LMA. Saw about 6 of them in the middle of the trachea. Used the cryo probe to freeze them. Did about 15 freezes total. They look treated. No bleeding. Steroids for swelling and follow up in a few months.",
            6: "Flexible bronchoscopy with cryotherapy ablation of tracheal papillomas. 61 y/o male with recurrent respiratory papillomatosis (RRP). Mid-trachea (4-6cm below cords) with multiple papillomatous lesions, largest 8mm, total of 6 lesions causing approximately 30% obstruction collectively. Cryotherapy performed using flexible cryoprobe (Erbe): Each papilloma treated with 2-3 freeze-thaw cycles. All visible lesions treated. Immediate blanching noted. No significant bleeding.",
            7: "[Indication]\nRecurrent Respiratory Papillomatosis, tracheal extension.\n[Anesthesia]\nGeneral, LMA.\n[Description]\n6 papillomas identified mid-trachea. Cryotherapy applied (15 cycles total). Lesions blanched. No bleeding.\n[Plan]\nOral steroids. ENT follow-up. Repeat bronchoscopy 8-12 weeks.",
            8: "Mr. [Name] has a history of papillomas in his airway. Today we treated new growths in his windpipe. Using a flexible scope, we froze each of the six small growths using a cryotherapy probe. This kills the tissue and helps keep the airway open. The procedure went very smoothly with no bleeding.",
            9: "PREOP DIAGNOSIS: Tracheal papillomatosis\nPROCEDURE: Flexible bronchoscopy with cryotherapy destruction of tracheal papillomas\nDETAILS: Mid-trachea with multiple papillomatous lesions. Cryotherapy performed using flexible cryoprobe. Each papilloma treated with 2-3 freeze-thaw cycles. All visible lesions treated. Immediate blanching noted."
        }
    }
    return variations

def main():
    # Load source data
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return
    
    # Flatten the notes list to match our index-based variation dictionary
    # Order: Airway Dilation (0-4) then Cryotherapy (5-9)
    all_notes = []
    if "airway_dilation_notes" in source_data:
        all_notes.extend(source_data["airway_dilation_notes"])
    if "cryotherapy_notes" in source_data:
        all_notes.extend(source_data["cryotherapy_notes"])
        
    print(f"Loaded {len(all_notes)} notes from {SOURCE_FILE}")
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through notes
    for idx, original_note in enumerate(all_notes):
        if idx >= len(base_data):
            print(f"Warning: No mock data for note index {idx}. Skipping.")
            continue
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Iterate through 9 styles
        for style_num in range(1, 10):
            # Deep copy to preserve structure
            note_entry = copy.deepcopy(original_note)
            
            # 1. Update Name and Age
            new_name = record['names'][style_num - 1]
            new_age = orig_age + random.randint(-3, 3)
            
            # 2. Update Date (Random within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # 3. Apply Text Variation
            # If we don't have a variation for this style, keep original (fallback)
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # 4. Update Registry Data (to keep consistency with text changes)
            if "registry_entry" in note_entry:
                reg = note_entry["registry_entry"]
                
                # Update ID
                if "patient_mrn" in reg:
                    reg["patient_mrn"] = f"{reg['patient_mrn']}_syn_{style_num}"
                
                # Update Date
                if "procedure_date" in reg:
                    reg["procedure_date"] = rand_date_str
                
                # Update Patient Demographics if present
                if "patient_demographics" in reg:
                    reg["patient_demographics"]["age_years"] = new_age
                    # No name field in demographics usually, but if providers/attending changed in text, 
                    # we aren't changing provider fields in registry to match text styles 4/5 
                    # because the prompt asks to keep extraction data *valid*, not necessarily sync style-specific hallucinated doctor names.
                    # We ONLY update patient specifics.
            
            # 5. Add Synthetic Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "note_type": "airway_dilation" if idx < 5 else "cryotherapy",
                "style_type": style_num,
                "generated_patient_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            # Inject the generated name into the note text if the placeholder [Name] exists
            if "[Name]" in note_entry["note_text"]:
                note_entry["note_text"] = note_entry["note_text"].replace("[Name]", new_name)
            
            generated_notes.append(note_entry)

    # Output to JSON
    output_filename = output_dir / "synthetic_interventional_notes_part_092.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()