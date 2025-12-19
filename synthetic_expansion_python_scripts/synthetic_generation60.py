import json
import random
import datetime
import copy
from pathlib import Path

# Source file configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_060.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock name lists and original ages for the 10 notes in Part 060.
    Ensures consistency in generated names across styles.
    """
    return [
        {"idx": 0, "orig_name": "Jackson, John", "orig_age": 51, "names": ["Robert Smith", "David Johnson", "Michael Brown", "James Williams", "William Jones", "Richard Miller", "Joseph Davis", "Thomas Garcia", "Charles Rodriguez"]},
        {"idx": 1, "orig_name": "Wilson, William", "orig_age": 52, "names": ["Christopher Martinez", "Daniel Hernandez", "Matthew Lopez", "Anthony Gonzalez", "Donald Wilson", "Paul Anderson", "Mark Thomas", "George Taylor", "Kenneth Moore"]},
        {"idx": 2, "orig_name": "Baker, Kenneth", "orig_age": 64, "names": ["Steven Jackson", "Edward Martin", "Brian Lee", "Ronald Perez", "Kevin Thompson", "Jason White", "Jeffrey Harris", "Frank Sanchez", "Scott Clark"]},
        {"idx": 3, "orig_name": "Green, Margaret", "orig_age": 78, "names": ["Mary Ramirez", "Patricia Lewis", "Jennifer Robinson", "Linda Walker", "Elizabeth Young", "Barbara Allen", "Susan King", "Jessica Wright", "Sarah Scott"]},
        {"idx": 4, "orig_name": "Green, Kenneth", "orig_age": 54, "names": ["Timothy Torres", "Jose Nguyen", "Larry Hill", "Jeffrey Flores", "Frank Green", "Scott Adams", "Eric Nelson", "Stephen Baker", "Andrew Hall"]},
        {"idx": 5, "orig_name": "Jones, Ronald", "orig_age": 73, "names": ["Raymond Rivera", "Gregory Campbell", "Joshua Mitchell", "Jerry Carter", "Dennis Roberts", "Walter Gomez", "Patrick Phillips", "Peter Evans", "Harold Turner"]},
        {"idx": 6, "orig_name": "Baker, Nicholas", "orig_age": 54, "names": ["Douglas Diaz", "Henry Parker", "Carl Cruz", "Arthur Edwards", "Ryan Collins", "Roger Reyes", "Joe Stewart", "Juan Morris", "Albert Morales"]},
        {"idx": 7, "orig_name": "Adams, Ashley", "orig_age": 66, "names": ["Karen Murphy", "Nancy Cook", "Lisa Rogers", "Betty Morgan", "Margaret Peterson", "Sandra Cooper", "Ashley Reed", "Kimberly Bailey", "Emily Bell"]},
        {"idx": 8, "orig_name": "Lewis, Melissa", "orig_age": 75, "names": ["Donna Gomez", "Carol Kelly", "Ruth Howard", "Sharon Ward", "Michelle Cox", "Laura Diaz", "Sarah Richardson", "Kim Wood", "Jessica Watson"]},
        {"idx": 9, "orig_name": "Jackson, Nancy", "orig_age": 70, "names": ["Cynthia Brooks", "Kathleen Bennett", "Amy Gray", "Shirley James", "Angela Reyes", "Helen Cruz", "Anna Hughes", "Brenda Price", "Pamela Myers"]},
    ]

def get_variations():
    """
    Returns the dictionary of text variations for the notes.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Jackson, John (Rigid bronch, BI debulking, APC/laser)
            1: "Pre-op: 75% BI obstruction (Adenocarcinoma).\nAnesthesia: General/Rigid Bronchoscopy.\nActions:\n- Tumor at BI visualized.\n- Forceps debulking performed (multiple passes).\n- APC and laser used for hemostasis/base ablation.\nResult: 12% residual. EBL 75mL.\nPlan: ICU. Oncology follow-up.",
            2: "OPERATIVE REPORT: The patient, presenting with a primary lung adenocarcinoma and severe central airway obstruction (75% at the bronchus intermedius), was brought to the operating suite. Following the induction of general anesthesia, a rigid bronchoscope was introduced. Significant endobronchial tumor burden was identified at the BI. We proceeded with mechanical debulking utilizing biopsy forceps, executing multiple sequential passes to maximize luminal patency. Adjunctive thermal ablation via Argon Plasma Coagulation (APC) and laser therapy was applied to the tumor base for both hemostasis and further tissue destruction. Post-intervention assessment revealed a patent airway with approximately 12% residual obstruction. Hemostasis was excellent.",
            3: "Procedure: Therapeutic Rigid Bronchoscopy with Debulking (CPT 31640/31641 utilized for varying modalities).\nLocation: Bronchus Intermedius (BI).\nTechnique:\n1. Mechanical removal of 75% obstructing tumor using rigid forceps.\n2. Destruction of residual tumor base and hemostasis using APC and Laser energy.\nOutcome: Significant restoration of airway patency (reduced to 12% obstruction). Medical necessity supported by malignancy with CAO.",
            4: "Procedure Note\nAttending: Dr. Rodriguez\nPt: 51M w/ Lung CA.\nSteps:\n1. GA induced. Rigid scope inserted.\n2. Saw tumor at BI (75% blocked).\n3. Used forceps to debulk the mass.\n4. Used APC and laser to burn the rest and stop bleeding.\n5. Airway looks much better (~12% residual).\n6. Pt stable.\nPlan: ICU obs.",
            5: "pt is here for the debulking of the lung cancer in the BI it was about 75 percent blocked rigid bronch used general anesthesia. we used the forceps to pull out the tumor pieces and then hit it with the apc and laser to stop the bleeding and burn the base. ebl was like 75ml. airway opens up to 12 percent obstruction patient goes to icu thanks.",
            6: "Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at BI. Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC/laser used for hemostasis and tumor base ablation. Post-procedure: ~12% residual obstruction. EBL: ~75mL. Hemostasis achieved. Specimens sent for histology.",
            7: "[Indication]\nPrimary lung adenocarcinoma with 75% obstruction at BI.\n[Anesthesia]\nGeneral anesthesia, Rigid Bronchoscopy.\n[Description]\nEndobronchial tumor identified at BI. Mechanical debulking performed using biopsy forceps. Additional tumor destruction and hemostasis achieved via APC and laser. Residual obstruction ~12%. EBL 75mL.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "Mr. Jackson was brought to the operating room for management of his airway obstruction. Under general anesthesia, we inserted the rigid bronchoscope and located the tumor in the bronchus intermedius, which was causing about 75% blockage. We used biopsy forceps to mechanically remove the bulk of the tumor through several passes. Following this, we utilized both APC and laser to ablate the remaining tumor base and ensure hemostasis. The airway was significantly improved, with only about 12% residual obstruction remaining.",
            9: "Operation: Rigid bronchoscopy with tumor excision.\nDetails: The endobronchial neoplasm at the BI was visualized. Mechanical resection was executed using biopsy forceps. Subsequent ablation of the tumor base was performed using APC and laser energy to ensure hemostasis. The obstruction was reduced from 75% to approximately 12%."
        },
        1: { # Wilson, William (Rigid bronch, Trachea, Balloon, Dumon Y-Stent)
            1: "Indication: Malignant tracheal obstruction (78%).\nProcedure: Rigid Bronchoscopy.\nActions:\n- Balloon dilation of tracheal stenosis.\n- Dumon Y-Stent (20x40mm) deployed.\n- Expansion/patency confirmed.\nResult: 21% residual obstruction.\nPlan: Admit floor. F/U 4-6 wks.",
            2: "PROCEDURE NARRATIVE: The patient, suffering from malignant central airway obstruction localized to the trachea (~78% stenosis), underwent rigid bronchoscopy under general anesthesia with jet ventilation. The stenotic segment was first addressed via sequential balloon dilation to prepare the airway. Subsequently, airway sizing was performed, and a silicone Dumon Y-Stent (20x40mm) was successfully deployed within the trachea. Post-deployment visualization confirmed excellent stent expansion and marked improvement in airway caliber (residual obstruction ~21%).",
            3: "Service: Bronchoscopy with Stent Placement (CPT 31636).\nAnatomy: Trachea.\nDevice: Dumon Y-Stent (20x40mm).\nTechnique: Rigid bronchoscopy access. Predilation performed with balloon (CPT 31630). Stent measured and deployed. Visual confirmation of placement and patency documented.\nMedical Necessity: 78% malignant obstruction reduced to 21%.",
            4: "Resident Procedure Note\nPt: William Wilson, 52M\nDx: Tracheal malignancy.\nSteps:\n1. Rigid bronch inserted (GA/Jet).\n2. Dilated tracheal narrowing with balloon.\n3. Deployed Dumon Y-Stent 20x40mm.\n4. Stent looks good, open.\n5. Obstruction down to 21%.\nPlan: Admit to floor.",
            5: "Procedure for Mr. Wilson he has the malignant obstruction in the trachea about 78 percent. We did the rigid bronch with jet vent. Used a balloon to dilate it open first. Then we put in the Dumon Y-Stent size 20 by 40 mm. Looks good nice and open now obstruction is down to 21 percent. Minimal bleeding sending him to the floor.",
            6: "Under general anesthesia with jet ventilation, rigid bronchoscopy performed. Sequential balloon dilation of trachea stenosis performed. Airway measured and Dumon Y-Stent Y-Stent stent (20x40mm) deployed in Trachea. Stent position confirmed with good expansion and patency. Post-procedure obstruction: ~21% No complications. EBL minimal.",
            7: "[Indication]\nMalignant central airway obstruction, 78% Trachea.\n[Anesthesia]\nGeneral with Jet Ventilation.\n[Description]\nRigid bronchoscopy. Balloon dilation of tracheal stenosis. Deployment of Dumon Y-Stent (20x40mm). Stent patent and well-positioned. Residual obstruction 21%.\n[Plan]\nAdmit to floor. Clinic 4-6 weeks.",
            8: "We performed a rigid bronchoscopy on Mr. Wilson to address his 78% tracheal obstruction. After inducing anesthesia, we used a balloon to sequentially dilate the stenosis. Once the airway was prepared, we deployed a 20x40mm Dumon Y-Stent into the trachea. The stent expanded well, and we confirmed good patency with a residual obstruction of only 21%. The patient tolerated the procedure well.",
            9: "Procedure: Rigid bronchoscopy with insertion of endobronchial prosthesis.\nTarget: Trachea.\nAction: The stenosis was expanded using balloon angioplasty. A Dumon Y-Stent (20x40mm) was positioned within the trachea. Verification confirmed satisfactory expansion.\nOutcome: Obstruction decreased to 21%."
        },
        2: { # Baker, Kenneth (Rigid bronch, LMS mechanical debulk + balloon)
            1: "Dx: CAO at LMS (72%).\nMethod: Rigid Bronchoscopy (GA).\nActions:\n- Mechanical debulking of LMS tumor.\n- Balloon dilation of residual stenosis.\nResult: 16% residual. EBL 200mL. Hemostasis ok.\nPlan: ICU obs.",
            2: "OPERATIVE SUMMARY: Mr. Baker presented with malignant obstruction of the Left Main Stem (LMS) bronchus estimated at 72%. Rigid bronchoscopy was initiated under general anesthesia. The endobronchial lesion was targeted for mechanical debulking, utilizing the rigid barrel to core out tumor tissue sequentially. Following mechanical resection, balloon dilation was employed to treat the residual stenosis. This multimodal approach resulted in a residual obstruction of approximately 16%. Hemostasis was achieved after an estimated blood loss of 200mL.",
            3: "Code Selection: 31641 (Bronchoscopy with tumor destruction/debulking).\nSite: Left Main Stem (LMS).\nModality: Mechanical debulking via rigid scope + Balloon dilation (Note: Balloon often bundled or used for dilation, coded as 31630 if distinct). \nDetails: 72% obstruction reduced to 16% via mechanical removal and dilation.\nComplexity: Moderate bleeding (200mL) managed.",
            4: "Procedure: Rigid Bronch Debulking\nPatient: Kenneth Baker, 64M\nIndication: LMS tumor.\nSteps:\n1. Rigid scope down.\n2. Coring/mechanical debulking of LMS tumor.\n3. Balloon dilation performed.\n4. Suctioned blood (~200cc).\n5. Good result, 16% residual.\nPlan: ICU.",
            5: "Kenneth Baker 64 male here for airway obstruction LMS about 72 percent. Did the rigid bronchoscopy today. We mechanically debulked the tumor scraped it out essentially. Then we used a balloon to open it up more. Bleeding was a bit more like 200 ml but we got it stopped. Airway looks way better 16 percent residual. ICU for observation.",
            6: "Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at LMS. Rigid bronchoscopy mechanical debulking performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Balloon dilation performed for residual stenosis. Post-procedure: ~16% residual obstruction. EBL: ~200mL. Hemostasis achieved. Specimens sent for histology.",
            7: "[Indication]\nMalignant CAO at LMS, 72% obstruction.\n[Anesthesia]\nGeneral anesthesia.\n[Description]\nRigid bronchoscopy performed. Mechanical debulking of LMS tumor completed. Balloon dilation of residual stenosis. Residual obstruction 16%. EBL 200mL.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "Mr. Baker underwent rigid bronchoscopy to treat a 72% obstruction in his left main stem bronchus. We mechanically debulked the tumor using the rigid scope and forceps, removing significant tissue. Afterward, we performed balloon dilation to further open the airway. The procedure successfully reduced the obstruction to 16%. There was about 200mL of blood loss, but hemostasis was secured before the end of the case.",
            9: "Operation: Rigid bronchoscopy with mechanical resection of tumor.\nSite: Left Main Stem.\nAction: The neoplasm was mechanically excised. The residual stenosis was expanded via balloon plasty.\nResult: Obstruction lessened from 72% to 16%. Hemostasis secured."
        },
        3: { # Green, Margaret (Rigid bronch, RMS, Balloon, Covered SEMS)
            1: "Indication: RCC met to RMS (89% block).\nProcedure: Rigid Bronchoscopy (Jet Vent).\nActions:\n- Balloon dilation of RMS.\n- Ultraflex Covered SEMS (18x30mm) placed.\nResult: 25% residual. Minimal EBL.\nPlan: Floor admit.",
            2: "PROCEDURE: Ms. Green, with a known history of renal cell carcinoma, presented with an 89% metastatic obstruction of the Right Main Stem (RMS) bronchus. Under general anesthesia utilizing jet ventilation, rigid bronchoscopy was performed. The stenotic segment underwent sequential balloon dilation. Subsequently, an 18x30mm Ultraflex Self-Expanding Metallic Stent (SEMS, covered) was deployed across the lesion. Confirmation of stent position demonstrated good radial expansion and patency, reducing the obstruction to approximately 25%.",
            3: "CPT: 31641 (Tumor Debulking? No, Stent placement = 31636).\nCorrect Coding: 31636 (Bronchial Stent) + 31630 (Balloon Dilation).\nDevice: Ultraflex SEMS Covered (18x30mm).\nLocation: Right Main Stem.\nJustification: 89% critical obstruction requiring structural support.",
            4: "Resident Note\nPt: Margaret Green, 78F\nDx: RCC met to RMS.\nSteps:\n1. Rigid bronch with jet vent.\n2. Balloon dilation of RMS.\n3. Placed Ultraflex Covered SEMS 18x30mm.\n4. Checked position, looks good.\n5. RMS much more open now (25% obs).\nPlan: Floor.",
            5: "Margaret Green here for the RMS obstruction its a met from renal cell. 89 percent blocked. We did the rigid bronch with jet ventilation. Dilated it with the balloon first. Then put in the Ultraflex covered stent 18 by 30. It opened up nice residual is 25 percent. No complications she is going to the floor.",
            6: "Under general anesthesia with jet ventilation, rigid bronchoscopy performed. Sequential balloon dilation of RMS stenosis performed. Airway measured and Ultraflex SEMS - Covered stent (18x30mm) deployed in Right mainstem. Stent position confirmed with good expansion and patency. Post-procedure obstruction: ~25% No complications. EBL minimal.",
            7: "[Indication]\nRenal cell carcinoma met to RMS, 89% obstruction.\n[Anesthesia]\nGeneral with Jet Ventilation.\n[Description]\nRigid bronchoscopy. Balloon dilation of RMS. Deployment of Ultraflex Covered SEMS (18x30mm). Stent expanded well. Residual obstruction 25%.\n[Plan]\nFloor admission. Repeat bronchoscopy 4-6 weeks.",
            8: "Due to Ms. Green's 89% blockage in the right mainstem bronchus from metastatic cancer, we proceeded with stent placement. Under general anesthesia, we first dilated the narrowing with a balloon. We then deployed an 18x30mm covered Ultraflex SEMS. The stent expanded well, improving the airway patency significantly to a residual obstruction of 25%.",
            9: "Procedure: Rigid bronchoscopy with implantation of self-expanding metallic stent.\nFocus: Right Main Stem.\nAction: The stenosis was dilated via balloon. An Ultraflex Covered SEMS (18x30mm) was deployed. Visualization confirmed adequacy.\nOutcome: Occlusion reduced to 25%."
        },
        4: { # Green, Kenneth (Rigid bronch, RLL APC debulk, APC/laser)
            1: "Dx: Thyroid CA compression/invasion RLL (80%).\nProcedure: Rigid Bronchoscopy.\nActions:\n- APC debulking of RLL tumor.\n- Multiple passes.\n- APC/Laser for hemostasis.\nResult: 24% residual. EBL 200mL.\nPlan: ICU.",
            2: "OPERATIVE REPORT: Mr. Green presented with airway compromise due to thyroid carcinoma invading the Right Lower Lobe (RLL) orifice (80% obstruction). Rigid bronchoscopy was undertaken. The tumor was addressed primarily via Argon Plasma Coagulation (APC) for devitalization and debulking, performed in sequential passes. Laser energy was utilized adjunctively for tumor base ablation and hemostasis. Post-procedure evaluation showed a patent RLL orifice with 24% residual obstruction. EBL was approximately 200mL.",
            3: "Coding: 31641 (Bronchoscopy with destruction of tumor, e.g., laser, APC, cryo).\nSite: RLL Orifice.\nTechnique: APC debulking and Laser ablation.\nCondition: Malignant obstruction (Thyroid CA).\nOutcome: Improvement from 80% to 24% obstruction.",
            4: "Procedure: RLL APC Debulking\nPt: Kenneth Green, 54M\nIndication: Thyroid CA.\nSteps:\n1. GA, Rigid scope.\n2. Found RLL tumor.\n3. Used APC to debulk it.\n4. Used Laser for bleeding/cleanup.\n5. RLL open now (24% residual).\n6. 200cc blood loss, controlled.\nPlan: ICU.",
            5: "Kenneth Green 54 male thyroid cancer pushing into the RLL about 80 percent blocked. We went in with the rigid scope. Used the APC to burn and remove the tumor. Did a bunch of passes. Used laser too for the bleeding. Lost about 200ml blood but stopped it. RLL is open to 24 percent obstruction now. ICU for him.",
            6: "Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at RLL orifice. Apc (argon plasma coagulation) performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC/laser used for hemostasis and tumor base ablation. Post-procedure: ~24% residual obstruction. EBL: ~200mL. Hemostasis achieved. Specimens sent for histology.",
            7: "[Indication]\nThyroid cancer with 80% obstruction at RLL orifice.\n[Anesthesia]\nGeneral anesthesia.\n[Description]\nRigid bronchoscopy. APC debulking of RLL tumor performed. Laser used for hemostasis. Residual obstruction 24%. EBL 200mL.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "We performed a rigid bronchoscopy on Mr. Green to manage the tumor obstructing his RLL orifice. Using Argon Plasma Coagulation (APC), we sequentially debulked the tumor tissue. We also used laser therapy to ablate the base and control bleeding. The procedure successfully reduced the obstruction from 80% to 24%, with about 200mL of blood loss which was controlled.",
            9: "Procedure: Rigid bronchoscopy with thermal ablation of neoplasm.\nSite: RLL orifice.\nMethod: Argon Plasma Coagulation (APC) was employed for tumor reduction. Laser energy was applied for hemostasis.\nResult: Blockage reduced to 24%."
        },
        5: { # Jones, Ronald (Rigid bronch, Trachea, Balloon, Novatech Silicone Dumon)
            1: "Indication: Esophageal CA invasion Trachea (85%).\nProcedure: Rigid Bronch (Jet Vent).\nActions:\n- Balloon dilation.\n- Novatech Silicone Dumon Stent (20x50mm) placed.\nResult: 7% residual.\nPlan: Floor.",
            2: "PROCEDURE NOTE: Mr. Jones, with esophageal carcinoma invading the trachea (85% stenosis), underwent palliative rigid bronchoscopy. Jet ventilation was employed. The critical tracheal stenosis was managed first with sequential balloon dilation. To maintain patency, a Novatech Silicone Dumon stent (20x50mm) was sized and deployed. Verification showed excellent apposition and patency, reducing the obstruction to a minimal 7%.",
            3: "Code: 31631 (Placement of Tracheal Stent).\nAdditional: 31630 (Balloon dilation).\nDevice: Novatech Silicone Dumon (20x50mm).\nIndication: Critical 85% tracheal stenosis.\nOutcome: 7% residual obstruction.",
            4: "Resident Note\nPt: Ronald Jones, 73M\nDx: Esophageal CA -> Trachea.\nSteps:\n1. Rigid bronch/Jet vent.\n2. Balloon dilated trachea.\n3. Put in Novatech Silicone stent 20x50.\n4. Looks great, only 7% obstruction left.\nPlan: Floor.",
            5: "Ronald Jones 73 male esophageal cancer eating into the trachea 85 percent blocked. We did the rigid bronch with jet ventilation. Ballooned it open. Then put in a Novatech silicone stent 20 by 50 mm. Its wide open now only 7 percent blocked. No bleeding really. Floor admit.",
            6: "Under general anesthesia with jet ventilation, rigid bronchoscopy performed. Sequential balloon dilation of trachea stenosis performed. Airway measured and Novatech Silicone - Dumon stent (20x50mm) deployed in Trachea. Stent position confirmed with good expansion and patency. Post-procedure obstruction: ~7% No complications. EBL minimal.",
            7: "[Indication]\nEsophageal cancer with 85% tracheal invasion.\n[Anesthesia]\nGeneral with Jet Ventilation.\n[Description]\nRigid bronchoscopy. Balloon dilation performed. Novatech Silicone Dumon stent (20x50mm) deployed in trachea. Residual obstruction 7%.\n[Plan]\nFloor admission. Repeat bronchoscopy 4-6 weeks.",
            8: "Mr. Jones required urgent intervention for an 85% tracheal obstruction caused by his esophageal cancer. Under general anesthesia, we used a balloon to dilate the narrowed airway. We then successfully placed a 20x50mm Novatech Silicone Dumon stent. The airway is now widely patent with only 7% residual obstruction, and he is recovering well.",
            9: "Procedure: Rigid bronchoscopy with deployment of silicone airway prosthesis.\nLocation: Trachea.\nAction: Balloon dilation was performed. A Novatech Silicone Dumon stent (20x50mm) was inserted.\nResult: Tracheal obstruction minimized to 7%."
        },
        6: { # Baker, Nicholas (Rigid bronch, BI mechanical debulk, APC/laser)
            1: "Dx: Malignant CAO at BI (76%).\nProcedure: Rigid Bronchoscopy.\nActions:\n- Mechanical debulking (forceps).\n- APC/Laser for hemostasis/base.\nResult: 19% residual. EBL 75mL.\nPlan: ICU.",
            2: "OPERATIVE NARRATIVE: Mr. Baker presented with a 76% malignant obstruction of the Bronchus Intermedius (BI). Rigid bronchoscopy was performed under general anesthesia. The tumor was addressed via mechanical debulking, using the rigid scope and forceps to remove tissue in a sequential fashion. Adjunctive APC and laser were applied to the tumor bed to ensure hemostasis and ablate residual tissue. The airway patency was significantly restored, leaving approximately 19% residual obstruction.",
            3: "Code: 31640 (Bronchoscopy with excision of tumor).\nSite: Bronchus Intermedius (BI).\nTechnique: Mechanical debulking + APC/Laser.\nStats: 76% -> 19% obstruction.\nEBL: 75mL.",
            4: "Procedure: BI Debulking\nPt: Nicholas Baker, 54M\nSteps:\n1. Rigid scope inserted.\n2. Saw BI tumor (76%).\n3. Mechanically debulked with forceps.\n4. APC/Laser for the rest.\n5. Good result, 19% residual.\nPlan: ICU.",
            5: "Nicholas Baker here for the BI tumor 76 percent blocked. Rigid bronch done. We used the forceps to mechanically debulk it basically ripped it out. Then used APC and laser to clean it up. Bleeding was 75ml controlled. Airway is 19 percent obstructed now much better. ICU.",
            6: "Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at BI. Rigid bronchoscopy mechanical debulking performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC/laser used for hemostasis and tumor base ablation. Post-procedure: ~19% residual obstruction. EBL: ~75mL. Hemostasis achieved. Specimens sent for histology.",
            7: "[Indication]\nMalignant CAO at BI, 76% obstruction.\n[Anesthesia]\nGeneral anesthesia.\n[Description]\nRigid bronchoscopy. Mechanical debulking of BI tumor using forceps. APC and laser used for hemostasis. Residual obstruction 19%. EBL 75mL.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "We took Mr. Baker to the OR to address the tumor blocking his bronchus intermedius. Using the rigid bronchoscope, we mechanically removed the majority of the tumor with forceps. We followed this with APC and laser treatment to stop any bleeding and ablate the remaining tissue. The obstruction was reduced from 76% to 19%.",
            9: "Procedure: Rigid bronchoscopy with mechanical tumor excision.\nSite: Bronchus Intermedius.\nAction: Forceps were utilized for mechanical resection. APC and laser provided hemostasis and ablation.\nResult: Obstruction reduced to 19%."
        },
        7: { # Adams, Ashley (Rigid bronch, RMS, Balloon, Covered SEMS)
            1: "Indication: Esophageal CA invasion RMS (89%).\nProcedure: Rigid Bronch (Jet Vent).\nActions:\n- Balloon dilation.\n- Ultraflex Covered SEMS (16x50mm) placed.\nResult: 11% residual.\nPlan: Floor admit.",
            2: "PROCEDURE: Ms. Adams presented with high-grade obstruction (89%) of the Right Main Stem (RMS) bronchus secondary to esophageal malignancy. Rigid bronchoscopy with jet ventilation was initiated. The stenosis was dilated using a balloon catheter. Following dilation, a 16x50mm Ultraflex Covered SEMS was deployed. Inspection confirmed optimal stent expansion and patency, reducing the obstruction to 11%.",
            3: "CPT: 31636 (Bronchial Stent).\nAncillary: 31630 (Balloon Dilation).\nDevice: Ultraflex Covered SEMS (16x50mm).\nSite: Right Main Stem.\nImprovement: 89% to 11% obstruction.",
            4: "Resident Note\nPt: Ashley Adams, 66F\nDx: Esophageal CA -> RMS.\nSteps:\n1. Rigid bronch/Jet.\n2. Balloon dilated RMS.\n3. Placed Ultraflex Covered SEMS 16x50.\n4. Good position.\n5. Residual obs 11%.\nPlan: Floor.",
            5: "Ashley Adams 66 female esophageal cancer into the RMS 89 percent blocked. We did the rigid bronch with jet vent. Ballooned the stenosis. Then put in a Ultraflex covered stent 16 by 50 mm. Looks great 11 percent obstruction left. No bleeding. Floor.",
            6: "Under general anesthesia with jet ventilation, rigid bronchoscopy performed. Sequential balloon dilation of RMS stenosis performed. Airway measured and Ultraflex SEMS - Covered stent (16x50mm) deployed in Right mainstem. Stent position confirmed with good expansion and patency. Post-procedure obstruction: ~11% No complications. EBL minimal.",
            7: "[Indication]\nEsophageal cancer, 89% RMS obstruction.\n[Anesthesia]\nGeneral with Jet Ventilation.\n[Description]\nRigid bronchoscopy. Balloon dilation of RMS. Deployment of Ultraflex Covered SEMS (16x50mm). Stent patent. Residual obstruction 11%.\n[Plan]\nFloor admission. Repeat bronchoscopy 4-6 weeks.",
            8: "Ms. Adams underwent rigid bronchoscopy to treat a severe 89% blockage in her right mainstem bronchus. We utilized a balloon to dilate the area before placing a 16x50mm covered Ultraflex SEMS. The stent deployed perfectly, restoring the airway to just 11% obstruction. She is stable and moving to the floor.",
            9: "Procedure: Rigid bronchoscopy with endobronchial stenting.\nTarget: Right Main Stem.\nAction: Balloon angioplasty was performed. An Ultraflex Covered SEMS (16x50mm) was implanted.\nResult: Patency improved; obstruction reduced to 11%."
        },
        8: { # Lewis, Melissa (Rigid bronch, RMS, Forceps debulk)
            1: "Dx: Metastatic lung CA at RMS (76%).\nProcedure: Rigid Bronchoscopy.\nActions:\n- Forceps debulking (multiple passes).\nResult: 30% residual. EBL 75mL.\nPlan: ICU.",
            2: "OPERATIVE REPORT: Ms. Lewis presented with metastatic lung cancer causing a 76% obstruction of the Right Main Stem (RMS). Rigid bronchoscopy was performed under general anesthesia. The tumor was mechanically debulked using biopsy forceps through multiple passes to core out the lesion. Post-procedure inspection revealed improvement to 30% residual obstruction. Hemostasis was achieved with approximately 75mL blood loss.",
            3: "Code: 31640 (Bronchoscopy with excision of tumor).\nMethod: Mechanical debulking via forceps.\nLocation: RMS.\nStats: 76% -> 30% obstruction.\nEBL: 75mL.",
            4: "Procedure: RMS Debulking\nPt: Melissa Lewis, 75F\nSteps:\n1. Rigid scope in.\n2. Saw RMS tumor.\n3. Used forceps to debulk.\n4. 30% residual obstruction now.\nPlan: ICU.",
            5: "Melissa Lewis 75 female met lung cancer RMS 76 percent blocked. Rigid bronch used. We used the biopsy forceps to debulk it took a few passes. Got it down to 30 percent. Bleeding 75ml. ICU for her.",
            6: "Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at RMS. Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Post-procedure: ~30% residual obstruction. EBL: ~75mL. Hemostasis achieved. Specimens sent for histology.",
            7: "[Indication]\nMetastatic lung cancer, 76% RMS obstruction.\n[Anesthesia]\nGeneral anesthesia.\n[Description]\nRigid bronchoscopy. Mechanical debulking of RMS tumor using forceps. Residual obstruction 30%. EBL 75mL.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "We performed a rigid bronchoscopy on Ms. Lewis to address the tumor blocking her right mainstem bronchus. Using biopsy forceps, we mechanically removed the tumor in pieces. We managed to reduce the obstruction from 76% down to 30% with minimal blood loss.",
            9: "Procedure: Rigid bronchoscopy with mechanical resection.\nSite: Right Main Stem.\nAction: Biopsy forceps were employed for tumor excision.\nResult: Obstruction decreased to 30%."
        },
        9: { # Jackson, Nancy (Rigid bronch, Distal trachea, Mechanical debulk + APC/laser)
            1: "Dx: SCC distal trachea (76%).\nProcedure: Rigid Bronchoscopy.\nActions:\n- Mechanical debulking.\n- APC/Laser ablation.\nResult: 39% residual. EBL 150mL.\nPlan: ICU.",
            2: "OPERATIVE NARRATIVE: Ms. Jackson presented with squamous cell carcinoma compressing the distal trachea (76% obstruction). Rigid bronchoscopy was utilized. The tumor was first addressed with mechanical debulking to remove bulk tissue. Subsequently, APC and laser energy were applied for hemostasis and further ablation of the tumor base. The airway was improved to approximately 39% residual obstruction. EBL was 150mL.",
            3: "Code: 31640 (Excision) + 31641 (Destruction).\nSite: Distal Trachea.\nTechnique: Mechanical excision followed by APC/Laser ablation.\nOutcome: 76% -> 39% obstruction.\nEBL: 150mL.",
            4: "Procedure: Tracheal Debulking\nPt: Nancy Jackson, 70F\nSteps:\n1. Rigid scope.\n2. Distal trachea tumor (76%).\n3. Mechanical debulking.\n4. APC/Laser cleanup.\n5. 39% residual.\nPlan: ICU.",
            5: "Nancy Jackson 70 female SCC distal trachea 76 percent blocked. Rigid bronch done. We mechanically debulked it first then used the APC and laser to burn the rest. Bleeding 150ml. Residual is 39 percent. ICU.",
            6: "Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at distal trachea. Rigid bronchoscopy mechanical debulking performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC/laser used for hemostasis and tumor base ablation. Post-procedure: ~39% residual obstruction. EBL: ~150mL. Hemostasis achieved. Specimens sent for histology.",
            7: "[Indication]\nSCC distal trachea, 76% obstruction.\n[Anesthesia]\nGeneral anesthesia.\n[Description]\nRigid bronchoscopy. Mechanical debulking performed. APC and laser used for ablation/hemostasis. Residual obstruction 39%. EBL 150mL.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "Ms. Jackson underwent rigid bronchoscopy for her distal tracheal obstruction. We mechanically debulked the squamous cell carcinoma and then used APC and laser to treat the base and control bleeding. We successfully reduced the blockage from 76% to 39%.",
            9: "Procedure: Rigid bronchoscopy with tumor excision and ablation.\nSite: Distal Trachea.\nAction: Mechanical resection was performed. Thermal ablation (APC/Laser) was utilized for remaining tissue.\nResult: Obstruction reduced to 39%."
        }
    }
    return variations

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
    output_filename = output_dir / "synthetic_debulking_notes_part_060.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()