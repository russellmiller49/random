import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_078.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    # These variations correspond to the 10 stent/debulking notes in Part 78
    variations = {
        0: { # John Keller (Tracheal Stent 31631)
            1: "Indication: Malignant distal tracheal obstruction (SCC). Stridor.\nProcedure: Rigid bronch + dilation + stent.\nAnesthesia: GA, jet vent.\nFindings: 80% distal tracheal narrowing. Tumor cored/suctioned. Dilation to 14mm.\nDevice: 14x40mm silicone straight stent deployed 2cm above carina.\nResult: Widely patent lumen. 20% residual narrowing.\nComplications: Minor oozing. No pneumo.\nPlan: ICU observation.",
            2: "HISTORY: Mr. Keller, a 72-year-old male with known squamous cell carcinoma, presented with critical central airway obstruction manifesting as stridor and dyspnea. Radiographic review confirmed significant distal tracheal stenosis.\nOPERATIVE NARRATIVE: The patient was inducted under general anesthesia with jet ventilation via rigid bronchoscopy. Examination revealed a circumferential, friable tumor obstructing 80% of the distal trachea. The lesion was mechanically debulked using the rigid barrel to re-establish patency. Subsequent balloon dilation was performed serially up to 14 mm. A 14 x 40 mm silicone tracheal stent was then deployed over a guidewire, seated approximately 2 cm proximal to the carina. Post-deployment inspection confirmed excellent radial expansion and restoration of the airway caliber.\nDISPOSITION: The patient was transferred to the Intensive Care Unit for close airway monitoring.",
            3: "Procedure: Bronchoscopy with Tracheal Stent Placement (CPT 31631).\nIndication: Malignant Obstruction.\nTechnique:\n1. Rigid Bronchoscope inserted.\n2. Tumor cored to create channel.\n3. Balloon dilation performed (bundled).\n4. Stent Deployment: 14 x 40 mm Silicone Stent placed in distal trachea.\nResult: Lumen patent.\nNote: Mechanical dilation (31630) is inherent to the stent placement code and not separately billable.",
            4: "Procedure: Rigid Bronchoscopy, Stent Placement\nPatient: John Keller\nAttending: Dr. Rivera\nSteps:\n1. Time out completed.\n2. General anesthesia with jet ventilation.\n3. Rigid scope inserted. Visualized 80% tracheal stenosis.\n4. Cored tumor, suctioned debris.\n5. Dilated with balloon to 14 mm.\n6. Deployed 14x40 mm silicone stent.\n7. Confirmed position 2cm above carina.\nComplications: Minimal bleeding, hemostasis achieved.\nPlan: ICU admission.",
            5: "Procedure note for mr keller he has the squamous cell ca causing tracheal blockage. We did the rigid bronch today anesthesia gave general with jet. Saw the narrowing about 80 percent down low. Used the barrel to core it out then dilated it up. Put in a silicone stent 14 by 40 size looks good now wide open. Little bleeding nothing major used some cold saline. Sending him to the unit to watch him thanks.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: John Keller 72/M Date: 2025-01-10 Indication: Malignant distal tracheal obstruction from squamous cell carcinoma with dyspnea and stridor. Procedure: Rigid bronchoscopy with mechanical dilation and placement of silicone tracheal stent. Anesthesia: General anesthesia with jet ventilation via rigid bronchoscope provided by Anesthesia. Findings: Approximately 80% circumferential narrowing of the distal trachea over 2 cm with friable endobronchial tumor; right mainstem partially compressed by tumor bulk. Intervention: Tumor was gently cored with the rigid barrel and suctioned to establish a lumen, followed by serial balloon dilation up to 14 mm. Over a guidewire a 14 x 40 mm straight silicone tracheal stent was deployed across the stenosis and positioned ~2 cm above the carina. Post-deployment the airway lumen was widely patent with about 20% residual narrowing. Complications: Mild oozing controlled with topical epinephrine and iced saline; no hypoxia or pneumothorax. Disposition: Patient remained intubated and was transported to the ICU in stable condition for overnight airway observation.",
            7: "[Indication]\nMalignant distal tracheal obstruction, squamous cell carcinoma.\n[Anesthesia]\nGeneral, jet ventilation.\n[Description]\nRigid bronchoscopy performed. 80% narrowing identified. Tumor cored. Balloon dilation to 14mm. 14x40mm silicone stent deployed. Lumen patent.\n[Plan]\nICU admission. Surveillance in 4 weeks.",
            8: "We brought Mr. Keller to the operating room to address his severe tracheal obstruction caused by his cancer. Under general anesthesia using jet ventilation, we inserted the rigid bronchoscope. We found the distal trachea was about 80% blocked. We carefully cored out the tumor to make space and then used a balloon to dilate the airway further. Finally, we placed a 14 by 40 millimeter silicone stent. It sat perfectly just above the carina, and the airway looked much better afterwards.",
            9: "Indication: Malignant distal tracheal blockage.\nProcedure: Rigid bronchoscopy with mechanical expansion and insertion of silicone tracheal stent.\nFindings: 80% circumferential constriction of the distal trachea.\nIntervention: Tumor was gently excavated with the rigid barrel. Serial balloon expansion up to 14 mm was performed. A 14 x 40 mm straight silicone tracheal stent was installed across the stenosis. Post-installation the airway lumen was widely open.\nComplications: Mild oozing managed with cold saline."
        },
        1: { # Maria Lopez (Right Mainstem Stent 31636)
            1: "Dx: RUL SCC with 90% RMS obstruction.\nProcedure: Rigid/Flex Bronch + RMS Stent.\nAnesthesia: GA, ETT -> Rigid.\nFindings: 90% eccentric narrowing RMS.\nAction: Debulked via rigid. Dilated to 12mm. Deployed 12x40mm self-expanding metallic stent.\nOutcome: Good expansion. Residual narrowing 20%.\nComplications: Mild contact bleed. No desat.\nPlan: Extubate. Floor.",
            2: "PREOPERATIVE DIAGNOSIS: Right mainstem bronchial obstruction secondary to locally advanced squamous cell carcinoma.\nPROCEDURE: The patient was intubated and placed under general anesthesia. Initial inspection with the rigid bronchoscope revealed a critical 90% stenosis of the proximal right mainstem bronchus. Mechanical debulking was performed to facilitate access. Following guidewire placement, the stenosis was dilated to 12 mm via balloon angioplasty. A 12 x 40 mm uncovered self-expanding metallic stent was subsequently deployed under fluoroscopic guidance. The stent achieved excellent apposition to the bronchial wall, relieving the obstruction.\nPOST-OPERATIVE PLAN: The patient was extubated and transferred to the surgical floor.",
            3: "Code Selection: 31636 (Bronchoscopy with stent placement, initial bronchus).\nSite: Right Mainstem Bronchus.\nMedical Necessity: 90% malignant obstruction.\nDetails:\n- Rigid bronchoscopy used for access.\n- Mechanical debulking (bundled) performed.\n- Balloon dilation (bundled) to 12mm.\n- Placement of 12x40mm metallic stent.\n- Fluoroscopy utilized for verification.",
            4: "Resident Procedure Note\nPatient: Maria Lopez\nProcedure: RMS Stent\nKey Steps:\n1. GA induced. ETT placed.\n2. Exchanged for rigid scope.\n3. Saw 90% block in RMS.\n4. Debulked tumor.\n5. Dilated with balloon.\n6. Placed 12x40 metallic stent in RMS.\n7. Checked with fluoro.\nNo issues. Extubated to PACU.",
            5: "Maria Lopez here for the airway stent she has that tumor pushing on the right mainstem. We put her under general switched the tube for the rigid scope. It was tight about 90 percent closed. Cleared some out then dilated it. Put in a metal stent 12 by 40. Looks way better now open good air movement. Bleeding was minimal. She goes to the floor thanks.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: Maria Lopez 64/F Date: 2025-02-03 Indication: Symptomatic right mainstem bronchial obstruction from locally advanced right upper lobe squamous cell carcinoma. Procedure: Rigid and flexible bronchoscopy with mechanical dilation and placement of a right mainstem bronchial stent. Anesthesia: General anesthesia with ETT; anesthesia provided by separate anesthesia service. Findings: About 90% eccentric narrowing of the proximal right mainstem bronchus from intraluminal tumor and extrinsic compression; mucosa friable with contact bleeding. Intervention: Tumor bulk was gently debulked mechanically using the rigid barrel and suction. A guidewire was passed into the right lower lobe and the ETT exchanged to a rigid bronchoscope. Serial balloon dilations to 12 mm were performed. A 12 x 40 mm self-expanding metallic stent was deployed in the right mainstem under fluoroscopic and bronchoscopic visualization with good expansion and coverage of the lesion. Residual narrowing estimated at 20%. Complications: Mild bleeding controlled with iced saline; no sustained desaturation or arrhythmia. Disposition: Extubated in OR and transferred to PACU, then surgical floor in stable condition.",
            7: "[Indication]\nSymptomatic RMS obstruction, squamous cell CA.\n[Anesthesia]\nGeneral, ETT/Rigid.\n[Description]\n90% narrowing RMS. Debulked. Dilated to 12mm. 12x40mm metallic stent deployed. Good expansion confirmed on fluoro.\n[Plan]\nFloor admission. CXR. F/U bronch 6 weeks.",
            8: "Ms. Lopez had a significant blockage in her right main bronchial tube due to her tumor. We took her to the OR and, under general anesthesia, used a rigid bronchoscope to clear some of the tumor out. We then stretched the airway open with a balloon and placed a metal stent, 12 by 40 millimeters. The stent opened up the airway nicely, and she was breathing much better by the end of the case.",
            9: "Indication: Symptomatic right mainstem bronchial blockage.\nProcedure: Rigid and flexible bronchoscopy with mechanical expansion and insertion of a right mainstem bronchial stent.\nIntervention: Tumor bulk was gently reduced mechanically. Serial balloon expansions to 12 mm were executed. A 12 x 40 mm self-expanding metallic stent was positioned in the right mainstem under fluoroscopic and bronchoscopic visualization. Good expansion and coverage of the lesion were noted."
        },
        2: { # George Patel (Tracheal + RMS Stent 31631, 31636)
            1: "Indication: Combined distal tracheal (70%) and RMS (80%) obstruction.\nProcedure: Rigid Bronch + Stents x2.\nAnesthesia: GA, jet.\nIntervention:\n- Trachea: Debulked, 14x40mm silicone stent placed (31631).\n- RMS: Dilated, 12x30mm metallic stent placed (31636).\nResult: Both airways patent (<20% residual).\nComplications: Transient desat, resolved. No pneumo.\nPlan: ICU.",
            2: "INDICATION: Complex carinal obstruction involving the distal trachea and right mainstem bronchus secondary to bulky NSCLC.\nPROCEDURE: Rigid bronchoscopy was initiated under general anesthesia. The distal trachea exhibited 70% stenosis, and the proximal RMS showed 80% stenosis. Both sites were mechanically debulked. A 14 x 40 mm straight silicone stent was deployed in the trachea to secure the central airway. Subsequently, a 12 x 30 mm metallic stent was deployed in the right mainstem bronchus. Fluoroscopy confirmed satisfactory positioning of both devices with restoration of aeration to the right lung.\nDISPOSITION: The patient was transferred to the ICU for monitoring.",
            3: "Coding Summary:\n- 31631: Placement of tracheal stent (Silicone, 14x40mm).\n- 31636: Placement of bronchial stent, initial bronchus (Metallic, 12x30mm, Right Mainstem).\nRationale: Distinct anatomic sites (trachea and RMS) treated with separate devices. Limited debulking and dilation performed to facilitate placement (bundled).\nRVU Note: Multiple procedure reduction may apply to secondary code.",
            4: "Procedure: Double Stent Placement (Trachea + RMS)\nPatient: George Patel\nSteps:\n1. GA/Jet vent.\n2. Rigid scope in.\n3. Saw blockages in trachea and RMS.\n4. Cleaned it out a bit.\n5. Put silicone stent in trachea (14x40).\n6. Put metal stent in RMS (12x30).\n7. Checked flow - good.\nPlan: ICU overnight.",
            5: "Procedure note for Mr Patel he has that big tumor at the carina blocking trachea and right side. We went in with the rigid scope. Cleaned out the tumor a bit then put in two stents. One silicone for the trachea 14 by 40. One metal for the right main 12 by 30. Both looked good open well. He desatted for a sec but came right back up. Going to ICU thanks.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: George Patel 69/M Date: 2025-02-21 Indication: Combined distal tracheal and right mainstem obstruction from bulky non-small cell lung cancer with progressive dyspnea. Procedure: Rigid bronchoscopy with tracheal and right mainstem bronchial stent placement after limited mechanical debulking. Anesthesia: General anesthesia with rigid bronchoscopy; anesthesia team present. Findings: 70% circumferential narrowing of the distal trachea and separate 80% narrowing of the proximal right mainstem bronchus from tumor and external compression. Intervention: Limited mechanical debulking with the rigid barrel and suction was performed to open both segments. A 14 x 40 mm straight silicone tracheal stent was deployed across the distal tracheal lesion. A separate 12 x 30 mm metallic stent was then placed in the right mainstem bronchus under fluoroscopic guidance. Both stents were well positioned with brisk air entry to the right lung; residual narrowing <20% in both locations. Complications: No major bleeding; transient desaturation to high 80s resolved with recruitment maneuvers. Disposition: Extubated in OR and transferred to PACU in stable condition, then ICU for overnight monitoring.",
            7: "[Indication]\nCombined tracheal/RMS obstruction, NSCLC.\n[Anesthesia]\nGeneral, Jet.\n[Description]\nLimited debulking performed. Tracheal stent (silicone 14x40) deployed. RMS stent (metal 12x30) deployed. Both patent.\n[Complications]\nTransient desaturation.\n[Plan]\nICU admission. Repeat bronch 4-6 weeks.",
            8: "Mr. Patel had a complex blockage affecting both his windpipe and the main tube to his right lung. We used a rigid bronchoscope to clear some space. We decided to place two different stents: a silicone one for the trachea and a metal one for the right mainstem. Both went in smoothly under X-ray guidance. Airflow to the right lung improved immediately. He's heading to the ICU for observation.",
            9: "Indication: Combined distal tracheal and right mainstem blockage.\nProcedure: Rigid bronchoscopy with tracheal and right mainstem bronchial stent insertion.\nIntervention: Limited mechanical reduction was performed. A 14 x 40 mm straight silicone tracheal stent was installed across the distal tracheal lesion. A separate 12 x 30 mm metallic stent was then positioned in the right mainstem bronchus. Both stents were well situated."
        },
        3: { # Elaine Young (LMS + LLL Stent 31636, 31637)
            1: "Indication: Malignant obstruction LMS (85%) and LLL (80%).\nProcedure: Rigid Bronch + Stents x2 (LMS + LLL).\nAnesthesia: GA, ETT.\nIntervention:\n- Debulked LMS/LLL.\n- Dilated LMS to 12mm.\n- Stent 1: 12x40mm metal in LMS.\n- Stent 2: 10x30mm metal in LLL (extension).\nResult: <20% residual narrowing. Improved ventilation.\nPlan: ICU.",
            2: "OPERATIVE REPORT: Mrs. Young presented with severe dyspnea secondary to contiguous obstruction of the left mainstem and left lower lobe bronchi. Under general anesthesia, the airway was secured. Significant tumor burden was noted. Following mechanical debulking and balloon dilation, a 12 x 40 mm metallic stent was deployed in the left mainstem bronchus (Initial Bronchus). To address the distal extent of the disease, a second 10 x 30 mm metallic stent was deployed in the left lower lobe bronchus (Additional Major Bronchus). Post-procedure inspection showed patent lumens and improved distal aeration.",
            3: "Billing Codes:\n- 31636: Stent placement, initial bronchus (Left Mainstem).\n- 31637: Stent placement, each additional major bronchus (Left Lower Lobe).\nNotes: Procedure required treating two separate major bronchial segments to restore ventilation. Rigid bronchoscopy and fluoroscopy were utilized. Debulking and dilation are included services.",
            4: "Resident Note\nPatient: Elaine Young\nProcedure: LMS and LLL Stenting\nSteps:\n1. GA/ETT.\n2. Rigid bronchoscopy.\n3. Saw tumor in LMS and LLL.\n4. Debulked and dilated.\n5. Placed 12x40 stent in LMS.\n6. Placed 10x30 stent in LLL.\n7. Good result.\nNo complications.",
            5: "Elaine Young here for the left side stents. She had blockage in the mainstem and the lower lobe. We went in cleaned it out and put two metal stents in. One in the main 12 by 40. One in the lower lobe 10 by 30. They overlap a bit but flow is good. Bleeding stopped with ice saline. She is stable going to ICU.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: Elaine Young 61/F Date: 2025-03-05 Indication: Malignant obstruction of left mainstem and left lower lobe bronchus with dyspnea at rest. Procedure: Rigid and flexible bronchoscopy with mechanical dilation and placement of stents in left mainstem and left lower lobe bronchus. Anesthesia: General anesthesia with ETT, anesthesia by separate service. Findings: About 85% narrowing of the left mainstem and 80% narrowing at the origin of the left lower lobe bronchus from tumor and extrinsic compression; copious secretions. Intervention: Mechanical debulking with the rigid barrel and suction restored a small lumen. Balloon dilation to 12 mm in the left mainstem followed by deployment of a 12 x 40 mm metallic stent. A second 10 x 30 mm metallic stent was placed in the left lower lobe bronchus as an extension. Final appearance showed <20% residual narrowing and markedly improved ventilation. Complications: Brief bleeding <30 mL, controlled with iced saline; no hypoxia. Disposition: Extubated in OR and discharged to surgical ICU in stable condition.",
            7: "[Indication]\nLMS and LLL obstruction, Stage III NSCLC.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nTumor debulked. LMS dilated. 12x40mm stent placed in LMS. 10x30mm stent placed in LLL. Ventilation improved.\n[Plan]\nICU admission. Secretion management.",
            8: "We treated Mrs. Young for blockages in her left lung today. The tumor was closing off both the main airway and the lower branch. We cleared some of the tumor and then placed two metal stents connected to each other—one in the main tube and one extending down into the lower lobe. This opened everything up nicely, and she should breathe much easier.",
            9: "Indication: Malignant blockage of left mainstem and left lower lobe bronchus.\nProcedure: Rigid and flexible bronchoscopy with mechanical expansion and insertion of stents in left mainstem and left lower lobe bronchus.\nIntervention: Mechanical reduction restored a small lumen. Balloon expansion to 12 mm was performed. A 12 x 40 mm metallic stent was deployed in the left mainstem. A second 10 x 30 mm metallic stent was positioned in the left lower lobe bronchus."
        },
        4: { # Kevin Moore (Benign Tracheal Stent 31631)
            1: "Indication: Benign post-intubation tracheal stenosis (75%).\nProcedure: Rigid Bronch + Silicone Stent.\nAnesthesia: GA.\nIntervention:\n- Dilation to 12mm (balloon).\n- 12x30mm silicone straight stent deployed.\nResult: Widely patent.\nComplications: None.\nPlan: Step-down unit.",
            2: "INDICATION: Symptomatic benign tracheal stenosis secondary to prior intubation.\nPROCEDURE: The patient was brought to the operating room and placed under general anesthesia. Evaluation with the rigid bronchoscope revealed a fibrotic stricture in the distal trachea reducing the lumen by approximately 75%. Serial balloon dilation was performed to 12 mm. To maintain patency, a 12 x 30 mm silicone tracheal stent was deployed. The stent was confirmed to be well-seated above the carina with no migration.\nDISPOSITION: The patient was extubated and transferred to the step-down unit in stable condition.",
            3: "Code: 31631 (Tracheal stent placement).\nDx: Benign tracheal stenosis.\nMethod:\n- Rigid bronchoscopy.\n- Balloon dilation (bundled).\n- Deployment of 12x30mm silicone stent.\nJustification: Fixed fibrotic stenosis refractory to simple dilation, requiring stenting for luminal maintenance.",
            4: "Procedure: Tracheal Stent (Benign)\nPatient: Kevin Moore\nSteps:\n1. GA/ETT.\n2. Visualized tracheal stenosis (fibrotic).\n3. Dilated with balloon to 12mm.\n4. Placed 12x30 silicone stent.\n5. Checked position.\nNo complications. Extubated.",
            5: "Kevin Moore here for the tracheal narrowing he had a breathing tube before and it scarred up. We went in dilated it with the balloon. Then put a silicone stent in 12 by 30. It looks good holding the airway open. No bleeding. He is awake and breathing okay sending to step down.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: Kevin Moore 58/M Date: 2025-01-22 Indication: Benign post-intubation distal tracheal stenosis with exertional dyspnea and biphasic stridor. Procedure: Rigid and flexible bronchoscopy with tracheal balloon dilation and silicone stent placement. Anesthesia: General anesthesia with ETT; anesthesia team present. Findings: Short-segment circumferential fibrotic ring in distal trachea causing ~75% narrowing; no mass lesion. Intervention: Serial balloon dilations up to 12 mm were performed across the stenosis. A 12 x 30 mm straight silicone stent was deployed across the narrowed segment and positioned just above the carina. Post-procedure lumen appeared widely patent with residual narrowing <20%. Complications: No significant bleeding; no hypoxia or hemodynamic instability. Disposition: Extubated in the OR and discharged to step-down unit in stable condition.",
            7: "[Indication]\nBenign post-intubation tracheal stenosis.\n[Anesthesia]\nGeneral.\n[Description]\nFibrotic ring dilated to 12mm. 12x30mm silicone stent placed. Lumen patent.\n[Plan]\nStep-down unit. Re-scope in 4 weeks.",
            8: "Mr. Moore has a scar in his windpipe from a previous breathing tube that was making it hard to breathe. We went in and stretched that scar tissue open with a balloon. To keep it open, we placed a silicone stent. It fits perfectly and his airway is wide open now.",
            9: "Indication: Benign post-intubation distal tracheal constriction.\nProcedure: Rigid and flexible bronchoscopy with tracheal balloon expansion and silicone stent insertion.\nFindings: Short-segment circumferential fibrotic ring in distal trachea.\nIntervention: Serial balloon expansions up to 12 mm were executed. A 12 x 30 mm straight silicone stent was installed across the narrowed segment. Post-procedure lumen appeared widely open."
        },
        5: { # Oliver Grant (LMS Stent 31636)
            1: "Indication: Left mainstem anastomotic stricture (Lung Tx).\nProcedure: Flex/Rigid Bronch + Metal Stent.\nAnesthesia: GA.\nFindings: 70% fibrotic narrowing LMS anastomosis.\nAction: Balloon dilation to 12mm. 12x30mm metallic stent deployed.\nResult: <20% residual narrowing.\nPlan: ICU.",
            2: "INDICATION: Post-transplant anastomotic stricture of the left mainstem bronchus.\nPROCEDURE: Under general anesthesia, the airway was inspected. A concentric stricture was identified at the left bronchial anastomosis. Balloon angioplasty was performed to a diameter of 12 mm. To preventing restenosis, a 12 x 30 mm uncovered self-expanding metallic stent was deployed across the anastomosis under fluoroscopic guidance. Excellent airway patency was restored.\nDISPOSITION: Returned to CT-ICU for monitoring.",
            3: "Code: 31636 (Bronchial stent, initial).\nSite: Left Mainstem Bronchus.\nIndication: Anastomotic stricture (T86.81).\nTechnique: Balloon dilation (bundled) followed by deployment of 12x30mm metallic stent using flexible bronchoscopy and fluoroscopy.",
            4: "Procedure: LMS Stent (Transplant)\nPatient: Oliver Grant\nSteps:\n1. GA.\n2. Scope down. Saw stricture at LMS anastomosis.\n3. Dilated with balloon.\n4. Placed 12x30 metal stent.\n5. Fluoro confirmed position.\nStable. Back to ICU.",
            5: "Mr Grant is a lung transplant patient with a tight left airway. We went in dilated the stricture up to 12. Put a metal stent in 12 by 30 to keep it open. Airway looks much better now. No bleeding. Back to the transplant ICU.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: Oliver Grant 63/M Date: 2025-03-12 Indication: Left mainstem bronchial anastomotic stricture after left lung transplant with dyspnea and wheeze. Procedure: Flexible and rigid bronchoscopy with balloon dilation and placement of a left mainstem bronchial stent. Anesthesia: General anesthesia with ETT; anesthesia care by transplant anesthesia team. Findings: Concentric fibrotic narrowing at the bronchial anastomosis resulting in ~70% narrowing; mild mucosal edema; no mass. Intervention: Balloon dilation to 10 and 12 mm was performed across the stricture. A 12 x 30 mm self-expanding metallic stent was deployed in the left mainstem across the anastomosis under fluoroscopic guidance. Airway lumen improved with <20% residual narrowing and symmetric ventilation. Complications: No significant bleeding; no hypoxia or hemodynamic instability. Disposition: Extubated in OR and returned to cardiothoracic ICU for routine post-transplant monitoring.",
            7: "[Indication]\nLMS anastomotic stricture, post-transplant.\n[Anesthesia]\nGeneral.\n[Description]\nStricture dilated. 12x30mm metallic stent deployed. Lumen improved.\n[Plan]\nCT-ICU. Follow-up bronch 2-4 weeks.",
            8: "Mr. Grant developed a narrowing where his transplanted lung was connected on the left side. We dilated that narrowing with a balloon and placed a metal stent to keep it from closing up again. The airway looks great now, and he's heading back to the ICU.",
            9: "Indication: Left mainstem bronchial anastomotic constriction after left lung transplant.\nProcedure: Flexible and rigid bronchoscopy with balloon expansion and insertion of a left mainstem bronchial stent.\nIntervention: Balloon expansion to 10 and 12 mm was performed. A 12 x 30 mm self-expanding metallic stent was installed in the left mainstem. Airway lumen improved."
        },
        6: { # Sarah Jenkins (Bilateral Stents 31636, 31637)
            1: "Indication: Bilateral RMS/LMS anastomotic strictures (Lung Tx).\nProcedure: Flex Bronch + Bilateral Stents.\nAnesthesia: GA.\nIntervention:\n- RMS: Dilated, 12x30mm metal stent (31636).\n- LMS: Dilated, 12x30mm metal stent (31637).\nResult: Bilateral patency restored.\nPlan: ICU.",
            2: "INDICATION: Bilateral mainstem bronchial stenosis following bilateral lung transplantation.\nPROCEDURE: The patient was placed under general anesthesia. Bronchoscopy revealed significant strictures at both the right and left anastomoses. Both sites were dilated via balloon. A 12 x 30 mm metallic stent was deployed in the right mainstem bronchus (Initial). A second 12 x 30 mm metallic stent was deployed in the left mainstem bronchus (Additional). Fluoroscopy confirmed symmetric expansion and proper placement of both prostheses.\nDISPOSITION: The patient was transferred to the CT-ICU.",
            3: "Codes:\n- 31636: Stent, initial bronchus (Right Mainstem).\n- 31637: Stent, additional bronchus (Left Mainstem).\nRationale: Patient required stenting of two separate major bronchi (bilateral mainstems) for anastomotic strictures. Dilation included.",
            4: "Procedure: Bilateral Stents\nPatient: Sarah Jenkins\nSteps:\n1. GA.\n2. Saw narrowing in both RMS and LMS.\n3. Dilated both sides.\n4. Put 12x30 metal stent in Right.\n5. Put 12x30 metal stent in Left.\n6. Both look open.\nNo complications.",
            5: "Sarah Jenkins here for bilateral airway narrowing after her transplant. We dilated both sides then put metal stents in. Right side got a 12 by 30. Left side also got a 12 by 30. Both airways are wide open now. Minimal bleeding. Sending her to ICU.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: Sarah Jenkins 55/F Date: 2025-04-02 Indication: Bilateral bronchial anastomotic strictures after bilateral lung transplant with exertional dyspnea. Procedure: Flexible bronchoscopy with balloon dilation and bilateral bronchial stent placement (right and left mainstem). Anesthesia: General anesthesia with ETT; anesthesia team present. Findings: Approximately 60–70% concentric narrowing at both right and left mainstem bronchial anastomoses; no mass; mild mucus plugging. Intervention: Balloon dilation to 10 and 12 mm was performed at each anastomosis. A 12 x 30 mm metallic stent was deployed in the right mainstem (initial bronchus), followed by placement of a 12 x 30 mm metallic stent in the left mainstem as an additional major bronchus. Final lumen on both sides showed <20% residual narrowing with symmetric ventilation. Complications: Minimal bleeding; no hypoxia. Disposition: Extubated in OR and admitted to cardiothoracic ICU.",
            7: "[Indication]\nBilateral anastomotic strictures.\n[Anesthesia]\nGeneral.\n[Description]\nRMS and LMS dilated. 12x30mm metallic stent placed in RMS. 12x30mm metallic stent placed in LMS. Bilateral patency achieved.\n[Plan]\nICU. Surveillance bronch 4 weeks.",
            8: "Ms. Jenkins had narrowing in both of her main airways from her transplant. We fixed both sides today. We used balloons to stretch the narrow spots and then placed identical metal stents in the right and left main airways. Everything looks symmetrical and open now.",
            9: "Indication: Bilateral bronchial anastomotic constrictions after bilateral lung transplant.\nProcedure: Flexible bronchoscopy with balloon expansion and bilateral bronchial stent insertion.\nIntervention: Balloon expansion was performed at each anastomosis. A 12 x 30 mm metallic stent was installed in the right mainstem, followed by insertion of a 12 x 30 mm metallic stent in the left mainstem. Final lumen on both sides showed <20% residual narrowing."
        },
        7: { # Lila Shah (Tracheal Stent 31631)
            1: "Indication: Extrinsic tracheal compression (Lymphoma).\nProcedure: Rigid Bronch + Silicone Stent.\nFindings: 65% mid-distal tracheal narrowing.\nAction: Dilated to 13mm. Placed 13x50mm silicone stent.\nResult: Lumen patent.\nPlan: Oncology floor.",
            2: "INDICATION: Critical airway compromise due to mediastinal lymphoma compressing the trachea.\nPROCEDURE: Rigid bronchoscopy was performed under general anesthesia. Significant extrinsic compression of the mid-to-distal trachea was noted. The airway was gently dilated to accept a prosthesis. A 13 x 50 mm silicone tracheal stent was deployed, spanning the length of the compression. Post-deployment visualization confirmed restoration of the airway lumen and relief of the obstruction.\nDISPOSITION: Admitted to oncology service.",
            3: "Code: 31631 (Tracheal Stent).\nDx: Lymphoma with tracheal compression.\nDevice: 13x50mm Silicone Stent.\nNote: Stent used to maintain patency against extrinsic compression. Dilation bundled.",
            4: "Procedure: Tracheal Stent\nPatient: Lila Shah\nSteps:\n1. GA/Rigid scope.\n2. Saw compression from lymphoma.\n3. Dilated.\n4. Placed 13x50 silicone stent.\n5. Airway looks much better.\nExtubated to floor.",
            5: "Lila Shah has lymphoma pushing on her windpipe. We used the rigid scope to open it up. Put in a long silicone stent 13 by 50 to hold the airway open against the pressure. It looks good now breathing is better. No bleeding. Back to the floor.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: Lila Shah 49/F Date: 2025-03-27 Indication: Extrinsic tracheal compression from mediastinal lymphoma with progressive stridor. Procedure: Rigid bronchoscopy with mechanical dilation and silicone tracheal stent placement. Anesthesia: General anesthesia with rigid bronchoscopy; anesthesia team present. Findings: Long-segment mid to distal tracheal narrowing (~65% reduction in lumen) from external compression; mucosa intact. Intervention: Gentle mechanical dilatation with the rigid barrel and serial balloon inflations up to 13 mm restored tracheal caliber. A 13 x 50 mm silicone tracheal stent was deployed spanning the compressed segment. Post-placement, tracheal lumen was widely patent with minimal residual narrowing and improved airflow. Complications: None immediate. Disposition: Extubated in OR and admitted to oncology floor for ongoing lymphoma management.",
            7: "[Indication]\nTracheal compression, Lymphoma.\n[Anesthesia]\nGeneral.\n[Description]\nExtrinsic compression dilated. 13x50mm silicone stent placed. Airway secured.\n[Plan]\nOncology admission.",
            8: "Ms. Shah's lymphoma was pressing on her trachea from the outside, making it narrow. We went in and placed a silicone stent—kind of like a stiff tube—inside the trachea to hold it open against that pressure. It worked well, and the airway is nice and wide now.",
            9: "Indication: Extrinsic tracheal compression from mediastinal lymphoma.\nProcedure: Rigid bronchoscopy with mechanical expansion and silicone tracheal stent insertion.\nIntervention: Gentle mechanical expansion was performed. A 13 x 50 mm silicone tracheal stent was installed spanning the compressed segment. Post-placement, tracheal lumen was widely open."
        },
        8: { # Robert Fields (Debulking 31640)
            1: "Indication: RMS tumor (SCC), lung collapse.\nProcedure: Rigid Bronch + Mechanical Debulking.\nFindings: 90% occlusion RMS.\nAction: Cored with rigid, forceps removal, microdebrider. No stent.\nResult: 30% residual narrowing. Airflow restored.\nComplications: Moderate bleeding (80ml), controlled.\nPlan: ICU.",
            2: "INDICATION: Critical right mainstem obstruction due to endobronchial carcinoma.\nPROCEDURE: Rigid bronchoscopy was performed. A large exophytic tumor was visualizing occluding the proximal RMS. Mechanical debulking was executed utilizing the rigid bronchoscope barrel for coring, followed by forceps extraction and microdebrider resection. The airway was successfully recanalized, leaving approximately 30% residual stenosis. Hemostasis was achieved after moderate bleeding.\nDISPOSITION: The patient was transferred to the ICU intubated for monitoring.",
            3: "Code: 31640 (Bronchoscopy with excision of tumor).\nTechnique: Mechanical debulking (rigid coring, forceps, microdebrider).\nSite: Right Mainstem Bronchus.\nOutcome: Restoration of patency. No stent placed (excludes 31636).",
            4: "Procedure: Tumor Debulking\nPatient: Robert Fields\nSteps:\n1. GA/Rigid scope.\n2. RMS 90% blocked by tumor.\n3. Cored it out, used forceps and microdebrider.\n4. Got it open to 70% patency.\n5. Some bleeding, controlled with epi/saline.\nPlan: ICU.",
            5: "Mr Fields has a tumor blocking his right lung. We went in with the rigid scope and cored it out. Used the grabbers and the shaver to get the rest. Opened it up pretty good. There was some bleeding about 80 cc but we stopped it. No stent needed right now. He is going to ICU intubated.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: Robert Fields 59/M Date: 2025-02-14 Indication: Critical right mainstem endobronchial tumor causing dyspnea at rest and right lung collapse. Procedure: Rigid bronchoscopy with mechanical debulking of right mainstem tumor. Anesthesia: General anesthesia with rigid bronchoscopy; anesthesia service present. Findings: Friable exophytic squamous cell carcinoma arising from the medial wall of the proximal right mainstem bronchus causing ~90% occlusion; copious blood-tinged secretions. Intervention: The tumor was mechanically debulked using rigid coring, suction, and forceps. A microdebrider was then used to excise residual tumor until the airway lumen was restored. Multiple tumor fragments were removed with suction and forceps and sent for pathology. Final lumen showed approximately 30% residual narrowing with improved airflow to the right lung; no stent placed. Complications: Transient moderate bleeding controlled with iced saline and dilute epinephrine; no hemodynamic instability. Disposition: Patient remained intubated and was transferred to the ICU for overnight monitoring.",
            7: "[Indication]\nRMS obstruction, SCC.\n[Anesthesia]\nGeneral.\n[Description]\nTumor cored and resected with forceps/microdebrider. Lumen restored to 70% patency. Hemostasis achieved.\n[Plan]\nICU. Re-eval 48-72h.",
            8: "Mr. Fields had a tumor almost completely blocking his right main airway. We used the rigid bronchoscope and various tools to physically remove the tumor chunks. We cleared enough of it to get air moving into the right lung again. There was some bleeding, which we expected and controlled, but we decided to keep him on the breathing machine in the ICU for a day or two to be safe.",
            9: "Indication: Critical right mainstem endobronchial tumor.\nProcedure: Rigid bronchoscopy with mechanical reduction of right mainstem tumor.\nIntervention: The tumor was mechanically reduced using rigid coring, suction, and forceps. A microdebrider was then used to excise residual tumor. Final lumen showed approximately 30% residual narrowing with improved airflow."
        },
        9: { # Margaret Stone (Debulking 31640)
            1: "Indication: Mid-tracheal mass (Adenoid Cystic Ca).\nProcedure: Rigid Bronch + Debulking.\nFindings: 70% tracheal lumen compromised.\nAction: Cored, snared, microdebrider. No stent.\nResult: 20% residual narrowing.\nPlan: Step-down.",
            2: "INDICATION: Symptomatic mid-tracheal obstruction secondary to adenoid cystic carcinoma.\nPROCEDURE: Under general anesthesia, rigid bronchoscopy revealed a broad-based tumor obstructing the mid-trachea. Resection was accomplished via a combination of rigid coring, snare technique, and microdebridement. The airway caliber was significantly improved. Hemostasis was maintained throughout. No stent was required at this time.\nDISPOSITION: The patient was extubated and transferred to the step-down unit.",
            3: "Code: 31640 (Bronchoscopy with excision of tumor).\nSite: Trachea.\nMethod: Mechanical resection (coring, snare, microdebrider).\nOutcome: Lumen restored. No stent placed.",
            4: "Procedure: Tracheal Debulking\nPatient: Margaret Stone\nSteps:\n1. GA/Rigid.\n2. Saw tracheal mass (70% block).\n3. Resected using snare and microdebrider.\n4. Airway open now.\n5. Minor bleeding.\nExtubated to step-down.",
            5: "Margaret Stone has a tumor in her windpipe. We used the rigid scope to clean it out. Used a snare and the shaver tool. Got most of it out breathing looks much better. No stent today. She woke up fine going to step down.",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT Patient: Margaret Stone 71/F Date: 2025-01-18 Indication: Mid-tracheal endobronchial mass from adenoid cystic carcinoma with progressive dyspnea. Procedure: Rigid bronchoscopy with mechanical debulking of tracheal tumor. Anesthesia: General anesthesia with rigid bronchoscopy; anesthesia team present. Findings: Broad-based tracheal mass on posterior wall at T3 level causing ~70% lumen compromise; no distal involvement. Intervention: Tumor was resected using rigid coring, snare resection of the bulk, and microdebrider to shave residual tissue. Multiple tumor fragments were removed and sent for histology. Final airway lumen showed approximately 20% residual narrowing without immediate need for stent. Complications: Mild bleeding controlled with iced saline; no desaturation or pneumothorax. Disposition: Extubated in OR and discharged to step-down unit.",
            7: "[Indication]\nTracheal Adenoid Cystic Carcinoma.\n[Anesthesia]\nGeneral.\n[Description]\nTumor resected via coring/snare/microdebrider. Lumen restored. 20% residual narrowing.\n[Plan]\nStep-down. Radiation oncology consult.",
            8: "Ms. Stone had a tumor growing in the middle of her windpipe. We went in and removed the bulk of it using special tools through the bronchoscope. We opened the airway up nicely, so we didn't need to leave a stent in. She's breathing much better and recovering in the step-down unit.",
            9: "Indication: Mid-tracheal endobronchial mass.\nProcedure: Rigid bronchoscopy with mechanical reduction of tracheal tumor.\nIntervention: Tumor was resected using rigid coring, snare resection of the bulk, and microdebrider. Multiple tumor fragments were removed. Final airway lumen showed approximately 20% residual narrowing."
        }
    }
    return variations

def get_base_data_mocks():
    # Names are generated to maintain consistency with the persona but distinct from original if desired
    # For this exercise, I will generate distinct random names for the 9 variations per patient.
    
    # Structure: idx -> {orig_name, orig_age, names_list}
    # We need 9 names per patient.
    base = [
        {
            "idx": 0, "orig_name": "John Keller", "orig_age": 72,
            "names": ["Robert Smith", "James Johnson", "Michael Williams", "William Brown", "David Jones", "Richard Miller", "Joseph Davis", "Thomas Garcia", "Charles Rodriguez"]
        },
        {
            "idx": 1, "orig_name": "Maria Lopez", "orig_age": 64,
            "names": ["Mary Wilson", "Patricia Martinez", "Jennifer Anderson", "Linda Taylor", "Elizabeth Thomas", "Barbara Hernandez", "Susan Moore", "Jessica Martin", "Sarah Jackson"]
        },
        {
            "idx": 2, "orig_name": "George Patel", "orig_age": 69,
            "names": ["Christopher Thompson", "Daniel White", "Paul Lopez", "Mark Lee", "Donald Gonzalez", "George Harris", "Kenneth Clark", "Steven Lewis", "Edward Robinson"]
        },
        {
            "idx": 3, "orig_name": "Elaine Young", "orig_age": 61,
            "names": ["Karen Walker", "Nancy Perez", "Lisa Hall", "Betty Young", "Margaret Allen", "Sandra Sanchez", "Ashley Wright", "Kimberly King", "Emily Scott"]
        },
        {
            "idx": 4, "orig_name": "Kevin Moore", "orig_age": 58,
            "names": ["Brian Green", "Ronald Baker", "Anthony Adams", "Kevin Nelson", "Jason Hill", "Matthew Ramirez", "Gary Campbell", "Timothy Mitchell", "Jose Roberts"]
        },
        {
            "idx": 5, "orig_name": "Oliver Grant", "orig_age": 63,
            "names": ["Larry Carter", "Jeffrey Phillips", "Frank Evans", "Scott Turner", "Eric Torres", "Stephen Parker", "Andrew Collins", "Raymond Edwards", "Gregory Stewart"]
        },
        {
            "idx": 6, "orig_name": "Sarah Jenkins", "orig_age": 55,
            "names": ["Donna Flores", "Michelle Morris", "Dorothy Nguyen", "Carol Murphy", "Amanda Rivera", "Melissa Cook", "Deborah Rogers", "Stephanie Morgan", "Rebecca Peterson"]
        },
        {
            "idx": 7, "orig_name": "Lila Shah", "orig_age": 49,
            "names": ["Sharon Cooper", "Laura Reed", "Cynthia Bailey", "Kathleen Bell", "Amy Gomez", "Shirley Kelly", "Angela Howard", "Helen Ward", "Anna Cox"]
        },
        {
            "idx": 8, "orig_name": "Robert Fields", "orig_age": 59,
            "names": ["Joshua Diaz", "Jerry Richardson", "Dennis Wood", "Walter Watson", "Patrick Brooks", "Peter Bennett", "Harold Gray", "Douglas James", "Henry Reyes"]
        },
        {
            "idx": 9, "orig_name": "Margaret Stone", "orig_age": 71,
            "names": ["Brenda Cruz", "Pamela Hughes", "Nicole Price", "Ruth Myers", "Katherine Long", "Samantha Foster", "Christine Sanders", "Debra Ross", "Rachel Morales"]
        }
    ]
    return base

def main():
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        return

    if not isinstance(source_data, list):
        print(f"Error: Source file must be a JSON array.")
        return

    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")

    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []

    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            break
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        for style_num in range(1, 10):
            note_entry = copy.deepcopy(original_note)
            
            # Randomize Age
            new_age = orig_age + random.randint(-3, 3)
            
            # Randomize Date (2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Assign Name
            new_name = record['names'][style_num - 1]
            
            # Update Note Text
            # Note: We must ensure the variation exists
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: No text variation found for Note {idx}, Style {style_num}")
                continue

            # Update Registry Fields
            if "registry_entry" in note_entry:
                reg = note_entry["registry_entry"]
                if "patient_age" in reg:
                    reg["patient_age"] = new_age
                if "procedure_date" in reg:
                    reg["procedure_date"] = rand_date_str
                if "patient_mrn" in reg:
                    # Append syn_X to MRN
                    reg["patient_mrn"] = f"{reg['patient_mrn']}_syn_{style_num}"
            
            # Add Synthetic Metadata
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    output_filename = output_dir / "synthetic_stent_notes_part_078.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()