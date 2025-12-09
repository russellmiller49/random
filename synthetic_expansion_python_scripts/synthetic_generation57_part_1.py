import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_057_part1.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Note 0: John Keller (Tracheal Stent 14x40, Silicone)
            1: "Procedure: Rigid Bronchoscopy w/ Tracheal Stent.\n- Indication: Malignant obstruction.\n- Action: Rigid scope inserted. Tumor cored. Balloon dilation to 14mm.\n- Implant: 14x40mm silicone stent placed ~2cm above carina.\n- Result: Airway widely patent. Oozing controlled.\n- Plan: ICU.",
            2: "OPERATIVE REPORT: The patient presented with critical central airway obstruction secondary to squamous cell carcinoma. Under general anesthesia with jet ventilation, the distal trachea was interrogated via rigid bronchoscopy. Significant stenosis was identified. The lesion was mechanically debulked to restore luminal patency, followed by radial expansion via balloon dilation. Subsequently, a 14 x 40 mm silicone tracheal prosthesis was deployed over a guidewire. Post-procedural evaluation demonstrated excellent stent apposition and restoration of laminar airflow.",
            3: "CPT 31631 (Bronchoscopy with tracheal stent placement) performed. Medical necessity: Malignant tracheal obstruction (80%). Technique involved rigid bronchoscopy access. Mechanical dilation (bundled) performed to 14mm. A silicone tracheal stent (14x40 mm) was precisely deployed in the distal trachea. Code 31631 is supported by the permanent placement of the indwelling stent.",
            4: "Resident Procedure Note\nAttending: Dr. Rivera\nProcedure: Rigid Bronchoscopy, Tracheal Stent\nSteps:\n1. Induced GA, established jet vent.\n2. Visualized 80% distal tracheal stenosis.\n3. Cored tumor and dilated with balloon to 14mm.\n4. Deployed 14x40mm silicone stent.\n5. Confirmed position and patency.\nComplications: Minor bleeding, controlled.\nDisposition: ICU.",
            5: "pt intubated for rigid bronch tracheal ca causing block. we went in with the rigid scope cored out some tumor then dilated it up. put in a silicone stent 14 by 40 mm looks good sitting above carina airway open now. minimal bleeding just some oozing used epi. pt to icu for watch thanks.",
            6: "The patient was brought to the OR and placed under general anesthesia with jet ventilation. A rigid bronchoscope was introduced. The distal trachea showed 80% narrowing from tumor. We cored the tumor and suctioned debris. Balloon dilation was performed up to 14 mm. A 14 x 40 mm straight silicone stent was deployed across the lesion. The airway was patent at the end of the case with minimal bleeding. Patient stable.",
            7: "[Indication]\nMalignant distal tracheal obstruction, squamous cell CA.\n[Anesthesia]\nGeneral with jet ventilation via rigid scope.\n[Description]\n80% stenosis encountered. Tumor cored and dilated to 14mm. 14x40mm silicone tracheal stent deployed. Patent lumen achieved. Hemostasis obtained.\n[Plan]\nICU admission.",
            8: "The patient, a 72-year-old male with malignant tracheal obstruction, underwent rigid bronchoscopy. After establishing anesthesia, we identified an 80% narrowing in the distal trachea. We gently cored the tumor to create a channel and then dilated the area with a balloon to 14 mm. A 14 x 40 mm silicone stent was then loaded and deployed over a guidewire, positioning it about 2 cm above the carina. The airway opened up significantly, and the patient was transferred to the ICU.",
            9: "Indication: Malignant airway blockade.\nProcedure: Rigid endoscopy with dilation and insertion of airway prosthesis.\nFindings: Severe constriction of distal trachea.\nIntervention: Lesion excised and expanded. A 14 x 40 mm silicone stent was implanted. Airway caliber restored.\nDisposition: ICU for monitoring."
        },
        1: { # Note 1: Maria Lopez (RMS Stent 12x40, Metallic)
            1: "Procedure: Rigid/Flexible Bronchoscopy, RMS Stent.\n- Indication: RUL Squamous Cell CA, RMS obstruction.\n- Action: Rigid barrel debulking. Dilation to 12mm.\n- Device: 12x40mm metallic stent deployed in Right Mainstem.\n- Result: Good expansion, <20% residual stenosis.\n- Plan: Extubate, Floor.",
            2: "OPERATIVE NARRATIVE: The patient, presenting with right mainstem bronchial obstruction, was subjected to rigid and flexible bronchoscopy. Upon visualization, a 90% eccentric stenosis was noted. Mechanical recanalization was performed using the rigid barrel, followed by balloon angioplasty to 12 mm. A 12 x 40 mm self-expanding metallic stent was subsequently deployed under fluoroscopic guidance, achieving excellent angiographic and bronchoscopic results with marked improvement in aeration.",
            3: "Service provided: Bronchoscopy with placement of bronchial stent (CPT 31636). Target site: Right Mainstem Bronchus (Initial bronchus). Technique: Rigid access, guidewire placement, and fluoroscopic guidance. Balloon dilation performed to facilitate stent delivery. A 12mm x 40mm self-expanding metallic stent was deployed, successfully treating the 90% malignant obstruction.",
            4: "Procedure Note\nPatient: Maria Lopez\nStaff: Dr. Wong\nProcedure: RMS Stent Placement\nSteps:\n1. GA, Rigid scope inserted.\n2. Debulked RMS tumor, dilated to 12mm.\n3. Advanced wire to RLL.\n4. Deployed 12x40mm metallic stent in RMS.\n5. Checked fluoro - good position.\nNo complications. To PACU.",
            5: "right mainstem blocked by tumor 90 percent. we did rigid bronch scraped some tumor out then dilated with balloon. put in a metal stent 12 by 40 mm into the right mainstem. opened up nice. bleeding was minor used saline. extubated in or sent to floor.",
            6: "Under general anesthesia the patient underwent rigid bronchoscopy for right mainstem obstruction. The 90% stenosis was debulked and dilated to 12 mm. A guidewire was placed. We deployed a 12 x 40 mm self-expanding metallic stent in the proximal right mainstem. Coverage was excellent with restored patency. Patient tolerated well and was extubated.",
            7: "[Indication]\nSymptomatic RMS obstruction, SqCC.\n[Anesthesia]\nGeneral, ETT.\n[Description]\n90% narrowing RMS. Debulked and dilated to 12mm. 12x40mm metallic stent deployed under fluoro. Good expansion. Airway patent.\n[Plan]\nAdmit to floor.",
            8: "Ms. Lopez was brought to the operating room for management of her right mainstem obstruction. We used a rigid bronchoscope to clear some of the tumor bulk and then dilated the airway to 12 mm using a balloon. Following this, we placed a 12 x 40 mm metallic stent into the right mainstem bronchus. The stent expanded well, covering the lesion and opening the airway. She was extubated and taken to recovery.",
            9: "Indication: Bronchial blockage.\nProcedure: Endoscopy with luminal expansion and prosthesis insertion.\nFindings: Tight constriction of right main bronchus.\nIntervention: Tissue cleared. 12x40 mm metallic scaffold implanted. Lumen re-established.\nResult: Successful recanalization."
        },
        2: { # Note 2: George Patel (Tracheal Silicone 14x40 + RMS Metallic 12x30)
            1: "Procedure: Rigid Bronchoscopy, Stenting x2.\n- Targets: Distal Trachea & RMS.\n- Action: Debulking performed. Dilation.\n- Implants: 14x40mm silicone stent (Trachea), 12x30mm metallic stent (RMS).\n- Result: Both airways patent.\n- Plan: ICU.",
            2: "OPERATIVE SUMMARY: This 69-year-old male with bulky non-small cell lung cancer presented with complex carinal obstruction. Rigid bronchoscopy was utilized to address synchronous stenoses in the distal trachea and right mainstem bronchus. Following mechanical debridement, a 14 x 40 mm silicone stent was positioned in the trachea. Subsequently, a 12 x 30 mm metallic stent was deployed in the right mainstem. Both prostheses showed excellent patency and position.",
            3: "Coding: 31631 (Tracheal Stent) and 31636 (Bronchial Stent). Justification: Patient required treatment of two distinct anatomical sites. 1) Distal trachea: Treated with 14x40mm silicone stent. 2) Right Mainstem Bronchus: Treated with 12x30mm metallic stent. Both deployments performed under fluoroscopic guidance after necessary preparation.",
            4: "Resident Note / Dr. Hart\nProcedure: Dual Stent Placement (Trachea + RMS)\n1. Rigid scope inserted.\n2. Debulked tumor at carina.\n3. Placed 14x40 silicone stent in trachea.\n4. Placed 12x30 metallic stent in RMS.\n5. Verified with fluoro.\nO2 sats dropped briefly but came back up. Pt to ICU.",
            5: "complex case tumor blocking trachea and right side. we went in with rigid scope cleaned it out best we could. put a silicone stent 14x40 in the trachea first then a metal one 12x30 in the right mainstem. flow looks good now both stents open. transient desat but ok. icu for him.",
            6: "Under general anesthesia rigid bronchoscopy was performed for combined tracheal and right mainstem obstruction. We debulked the lesions mechanically. A 14 x 40 mm silicone stent was deployed in the distal trachea. A separate 12 x 30 mm metallic stent was placed in the right mainstem bronchus. Both stents were well positioned with good air entry. Patient transferred to ICU.",
            7: "[Indication]\nCombined tracheal and RMS malignant obstruction.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\n70% tracheal and 80% RMS narrowing. Debulked. 14x40mm silicone stent placed in trachea. 12x30mm metallic stent placed in RMS. Airways patent.\n[Plan]\nICU monitoring.",
            8: "Mr. Patel underwent a complex procedure to open his airways. We found significant blockage in both the lower windpipe and the right main lung tube. We cleared some tumor and then placed two stents: a silicone one in the trachea (14x40mm) and a metallic one in the right mainstem (12x30mm). This dual stenting strategy successfully opened up his breathing passages. He went to the ICU for close watch.",
            9: "Indication: Carinal obstruction.\nProcedure: Rigid endoscopy with dual prosthesis implantation.\nIntervention: Mechanical clearance of tissue. Implantation of 14x40 mm silicone device in trachea. Implantation of 12x30 mm metallic device in right bronchus.\nOutcome: Airways restored."
        },
        3: { # Note 3: Elaine Young (LMS Metallic 12x40 + LLL Metallic 10x30)
            1: "Procedure: Rigid Bronchoscopy, Stenting (LMS + LLL).\n- Action: Debulking, Dilation to 12mm.\n- Stents: 12x40mm metallic (LMS), 10x30mm metallic (LLL extension).\n- Result: Airway patent, secretions cleared.\n- Plan: ICU.",
            2: "OPERATIVE REPORT: The patient underwent rigid bronchoscopic intervention for contiguous obstruction of the left mainstem and left lower lobe bronchi. Following mechanical restoration of the lumen, balloon dilation was performed. A 12 x 40 mm self-expanding metallic stent was deployed in the left mainstem. To address the distal extent of the disease, a secondary 10 x 30 mm metallic stent was telescoped into the left lower lobe bronchus. Post-deployment imaging confirmed adequate coverage.",
            3: "Codes: 31636 (Initial Bronchus Stent - LMS) and 31637 (Additional Bronchus Stent - LLL). The procedure involved stenting the Left Mainstem (12x40mm metallic) and a separate major bronchus, the Left Lower Lobe (10x30mm metallic), to bridge the malignant obstruction. Fluoroscopic guidance was utilized.",
            4: "Procedure: Stent Placement LMS and LLL\nAttending: Dr. Kim\n1. Rigid bronchoscopy initiated.\n2. Dilated LMS to 12mm.\n3. Placed 12x40 metallic stent in LMS.\n4. Placed 10x30 metallic stent in LLL.\n5. Suctioned secretions.\nGood result. To ICU.",
            5: "left side blocked up pretty bad lms and lll. did rigid bronch dilated it. put a metal stent 12 by 40 in the mainstem then another one 10 by 30 in the lower lobe to cover it all. secretions suctioned out. airway looks way better now. extubated sent to icu.",
            6: "Rigid bronchoscopy was performed for left lung obstruction. The left mainstem and left lower lobe were narrowed by tumor. We dilated the area and placed a 12 x 40 mm metallic stent in the left mainstem. We extended this with a 10 x 30 mm metallic stent into the left lower lobe. Ventilation improved significantly. Patient stable.",
            7: "[Indication]\nMalignant obstruction LMS and LLL.\n[Anesthesia]\nGeneral, ETT.\n[Description]\n85% LMS stenosis. Dilated. 12x40mm metallic stent placed in LMS. 10x30mm metallic stent placed in LLL. Patent lumen restored.\n[Plan]\nICU admission.",
            8: "Mrs. Young was treated for a blockage affecting her left main airway and the lower branch. Using a rigid scope, we opened the airway and placed two metallic stents: a larger one (12x40mm) in the mainstem and a smaller extension (10x30mm) into the lower lobe. This combination successfully reopened the path for air to reach the lower lung. She is recovering in the ICU.",
            9: "Indication: Bronchial occlusion.\nProcedure: Endoscopy with tandem prosthesis deployment.\nIntervention: Luminal expansion. 12x40 mm metallic scaffold implanted in left main. 10x30 mm metallic scaffold implanted in left lower lobe.\nResult: Ventilation improved."
        },
        4: { # Note 4: Kevin Moore (Benign Tracheal Silicone 12x30)
            1: "Procedure: Rigid Bronchoscopy, Tracheal Stent.\n- Indication: Benign post-intubation stenosis.\n- Action: Serial balloon dilation to 12mm. Placement of 12x30mm silicone stent.\n- Findings: Fibrotic ring, 75% stenosis.\n- Plan: Step-down unit.",
            2: "OPERATIVE NARRATIVE: Mr. Moore presented with benign tracheal stenosis consequent to prior intubation. Rigid bronchoscopy revealed a fibrotic cicatricial ring in the distal trachea. The lesion was managed via serial balloon dilation, followed by the deployment of a 12 x 30 mm silicone tracheal stent. The procedure yielded a widely patent airway with preservation of distal architecture.",
            3: "Coding: 31631 (Tracheal Stent Placement). Indication: Benign tracheal stenosis (J95.5). Technique: Rigid bronchoscopy with balloon dilation (bundled). A 12mm x 30mm silicone stent was deployed to maintain airway patency preventing restenosis.",
            4: "Procedure Note / Dr. Blake\nPt: Kevin Moore\nDx: Benign tracheal stenosis\n1. Rigid scope.\n2. Dilated stricture to 12mm.\n3. Placed 12x30 silicone stent.\n4. Verified position above carina.\nNo complications. Extubated.",
            5: "benign stenosis in trachea from old tube. rigid bronch used dilated it up to 12. put in a silicone stent 12x30 straight type. sits right above carina. airway open good. no bleeding. step down unit.",
            6: "Patient underwent rigid bronchoscopy for benign tracheal stenosis. A circumferential web was found in the distal trachea. We dilated this to 12 mm with a balloon. A 12 x 30 mm silicone stent was deployed. The airway is now widely patent. Patient extubated and stable.",
            7: "[Indication]\nBenign post-intubation tracheal stenosis.\n[Anesthesia]\nGeneral, ETT.\n[Description]\n75% fibrotic narrowing. Dilated to 12mm. 12x30mm silicone stent placed. Patent lumen.\n[Plan]\nStep-down unit.",
            8: "Mr. Moore came in for treatment of scar tissue in his trachea. We used a rigid scope to widen the narrowed area with a balloon. To keep it open, we placed a silicone stent measuring 12x30 mm just above the point where the windpipe splits. The procedure went smoothly without complications, and the airway looks excellent.",
            9: "Indication: Tracheal stricture.\nProcedure: Endoscopy with dilation and prosthesis insertion.\nIntervention: Fibrotic ring expanded. 12x30 mm silicone device implanted.\nOutcome: Airway caliber normalized."
        },
        5: { # Note 5: Oliver Grant (Post-transplant LMS Metallic 12x30)
            1: "Procedure: Flexible/Rigid Bronchoscopy, LMS Stent.\n- Indication: Post-transplant anastomotic stricture.\n- Action: Balloon dilation to 12mm. 12x30mm metallic stent placed.\n- Result: Improved lumen, symmetric ventilation.\n- Plan: CT ICU.",
            2: "OPERATIVE REPORT: The patient, a lung transplant recipient, presented with a left mainstem bronchial anastomotic stricture. Under general anesthesia, the stricture was addressed via balloon angioplasty to 12 mm. Subsequently, a 12 x 30 mm self-expanding metallic stent was deployed across the anastomosis. Post-deployment evaluation revealed marked improvement in luminal caliber and ventilation mechanics.",
            3: "Code 31636 (Bronchial Stent Placement). Diagnosis: Transplant complication/Stenosis. Technique: Flexible bronchoscopy with fluoroscopic guidance. Balloon dilation performed to prep the site. A 12x30mm uncovered metallic stent was deployed at the left mainstem anastomosis.",
            4: "Resident Note\nAttending: Dr. Cho\nProcedure: LMS Stent for transplant stricture\n1. Scope passed.\n2. Dilated LMS anastomosis to 12mm.\n3. Deployed 12x30 metallic stent.\n4. Checked fluoro.\nNo issues. Back to CT ICU.",
            5: "post transplant stricture left side. dilated it with balloon to 12. put a metal stent 12x30 across the anastomosis. opened up nice air moving better now. no bleeding. back to transplant icu.",
            6: "Bronchoscopy performed for left mainstem transplant stricture. 70% narrowing identified. Dilation performed to 12 mm. A 12 x 30 mm metallic stent was placed across the anastomosis. Result was excellent with less than 20% residual narrowing. Patient extubated.",
            7: "[Indication]\nLMS anastomotic stricture post-transplant.\n[Anesthesia]\nGeneral.\n[Description]\nFibrotic narrowing dilated. 12x30mm metallic stent placed in LMS. Lumen improved.\n[Plan]\nCT ICU.",
            8: "Mr. Grant required a stent for a narrowing at his left lung transplant connection site. We used a balloon to stretch the scar tissue and then placed a 12x30 mm metallic stent to hold it open. The airway opened up nicely, allowing for better breathing. He was returned to the transplant ICU for monitoring.",
            9: "Indication: Anastomotic constriction.\nProcedure: Endoscopy with angioplasty and prosthesis implantation.\nIntervention: Stricture dilated. 12x30 mm metallic scaffold implanted in left bronchus.\nOutcome: Luminal patency restored."
        },
        6: { # Note 6: Sarah Jenkins (Bilateral Metallic 12x30)
            1: "Procedure: Bilateral Bronchial Stenting.\n- Indication: Bilateral transplant strictures.\n- Action: Dilation to 12mm bilaterally. Stents: 12x30mm metallic (RMS), 12x30mm metallic (LMS).\n- Result: Bilateral patency restored.\n- Plan: CT ICU.",
            2: "OPERATIVE SUMMARY: Ms. Jenkins presented with bilateral bronchial anastomotic stenoses following lung transplantation. Sequential balloon dilation was performed on the right and left mainstem bronchi. A 12 x 30 mm metallic stent was deployed in the right mainstem, followed by an identical 12 x 30 mm stent in the left mainstem. Both anastomoses demonstrated excellent angiographic and bronchoscopic results post-intervention.",
            3: "Billing: 31636 (Stent RMS) + 31637 (Stent LMS). Medical Necessity: Bilateral anastomotic stenosis. Procedure included bilateral balloon dilation and placement of two distinct metallic stents (12x30mm each) in separate major bronchi (Right and Left Mainstem).",
            4: "Procedure: Bilateral Stents\nStaff: Dr. Carter\n1. Dilated RMS and LMS to 12mm.\n2. Placed 12x30 metal stent in RMS.\n3. Placed 12x30 metal stent in LMS.\n4. Confirmed position.\nPt tolerated well. To ICU.",
            5: "bilateral strictures transplant pt. dilated both sides. put metal stents in right and left mainstems both 12 by 30. airways look open now. no bleeding. extubated to icu.",
            6: "Patient underwent bronchoscopy for bilateral transplant strictures. Both right and left anastomoses were dilated to 12 mm. A 12 x 30 mm metallic stent was placed in the right mainstem. A second 12 x 30 mm metallic stent was placed in the left mainstem. Airflow is symmetric and improved. Extubated.",
            7: "[Indication]\nBilateral transplant anastomotic strictures.\n[Anesthesia]\nGeneral.\n[Description]\nDilated RMS and LMS. 12x30mm metallic stent placed in RMS. 12x30mm metallic stent placed in LMS. Good bilateral expansion.\n[Plan]\nCT ICU.",
            8: "Ms. Jenkins had narrowing at both of her lung transplant connections. We performed a procedure to place stents in both the right and left main breathing tubes. After dilating both sides, we inserted 12x30 mm metallic stents in each mainstem bronchus. This balanced approach restored good airflow to both lungs.",
            9: "Indication: Bilateral bronchial constriction.\nProcedure: Endoscopy with bilateral prosthesis implantation.\nIntervention: Dilated both sides. Implanted 12x30 mm metallic device in right bronchus. Implanted 12x30 mm metallic device in left bronchus.\nResult: Bilateral patency."
        },
        7: { # Note 7: Lila Shah (Tracheal Silicone 13x50 Extrinsic)
            1: "Procedure: Rigid Bronchoscopy, Tracheal Stent.\n- Indication: Extrinsic compression (Lymphoma).\n- Action: Dilation to 13mm. 13x50mm silicone stent placed.\n- Result: Trachea patent.\n- Plan: Oncology floor.",
            2: "OPERATIVE REPORT: Ms. Shah presented with symptomatic extrinsic tracheal compression secondary to mediastinal lymphoma. Rigid bronchoscopy was employed to stent the airway. Following mechanical calibration, a 13 x 50 mm silicone tracheal stent was deployed, spanning the length of the compression. The intervention successfully buttressed the tracheal wall, restoring luminal patency.",
            3: "Code 31631 (Tracheal Stent). Indication: Extrinsic tracheal compression. Technique: Rigid bronchoscopy used to measure and deploy a 13x50mm silicone stent to maintain airway patency against external mass effect. Dilation performed to facilitate placement.",
            4: "Procedure: Tracheal Stent\nAttending: Dr. Long\n1. Rigid scope inserted.\n2. Dilated compressed trachea.\n3. Placed 13x50 silicone stent.\n4. Airway open.\nPt to oncology for chemo.",
            5: "lymphoma pushing on trachea causing stridor. went in with rigid scope. dilated it up. put in a long silicone stent 13 by 50. airway looks wide open now stent holding it open against the mass. oncology to manage.",
            6: "Rigid bronchoscopy performed for extrinsic tracheal compression. 65% narrowing noted. We dilated the segment and deployed a 13 x 50 mm silicone tracheal stent. The stent successfully staved open the airway. Patient extubated and stable.",
            7: "[Indication]\nExtrinsic tracheal compression (Lymphoma).\n[Anesthesia]\nGeneral, rigid.\n[Description]\nMid-trachea compressed. Dilated. 13x50mm silicone stent placed. Airway patent.\n[Plan]\nOncology admission.",
            8: "Ms. Shah was suffering from breathing difficulties due to a lymphoma mass pressing on her windpipe. We performed a procedure to place a supportive stent. After gently dilating the area, we inserted a 13x50 mm silicone stent. This successfully pushes back against the external compression, keeping her airway open while she undergoes treatment.",
            9: "Indication: Tracheal impingement.\nProcedure: Endoscopy with prosthesis insertion.\nIntervention: Airway caliber expanded. 13x50 mm silicone scaffold implanted.\nOutcome: Compression relieved."
        },
        8: { # Note 8: Robert Fields (RMS Debulking 31640)
            1: "Procedure: Rigid Bronchoscopy, Tumor Debulking.\n- Site: RMS (Squamous cell CA).\n- Action: Mechanical coring, microdebrider, forceps.\n- Result: 90% -> 30% obstruction. No stent.\n- Plan: ICU.",
            2: "OPERATIVE NARRATIVE: Mr. Fields presented with critical right mainstem obstruction. Rigid bronchoscopy was utilized for mechanical tumor resection. Using a combination of rigid coring, forceps extraction, and microdebrider, the endobronchial tumor burden was significantly reduced. The airway was recanalized from 90% to 30% obstruction. Hemostasis was achieved, and stenting was deferred.",
            3: "Code 31640 (Bronchoscopy with excision of tumor). Technique: Mechanical debulking of Right Mainstem tumor using rigid coring, forceps, and microdebrider. Significant volume of tumor removed to restore airway. No stent placed (31636 not applicable).",
            4: "Procedure: RMS Debulking\nAttending: Dr. Bell\n1. Rigid scope.\n2. Cored out RMS tumor.\n3. Used microdebrider and forceps.\n4. Cleared to 30% residual.\nBleeding controlled. No stent. To ICU.",
            5: "big tumor in right mainstem. rigid bronch used. cored it out and used the debrider. pulled out a lot of pieces. opened up pretty good about 30 percent left. bleeding stopped with ice. no stent needed yet. icu.",
            6: "Rigid bronchoscopy for right mainstem tumor. 90% occlusion found. We debulked the tumor using coring and microdebrider. Multiple fragments removed. Airway opened significantly. No stent was placed at this time. Patient to ICU.",
            7: "[Indication]\nRMS malignant obstruction.\n[Anesthesia]\nGeneral, rigid.\n[Description]\n90% occlusion. Mechanical debulking performed (coring, forceps). Lumen restored to 30% narrowing. No stent.\n[Plan]\nICU.",
            8: "Mr. Fields had a large tumor blocking his right main bronchus. We performed a rigid bronchoscopy to physically remove the tumor. Using various tools including a coring pipe and grippers, we cleared out most of the blockage, improving the opening from 90% blocked to only 30%. We decided not to place a stent yet and will monitor him in the ICU.",
            9: "Indication: Bronchial neoplasm.\nProcedure: Endoscopy with tumor excision.\nIntervention: Lesion resected via coring and debridement. Tissue extracted. Lumen expanded.\nResult: Partial recanalization."
        },
        9: { # Note 9: Margaret Stone (Tracheal Debulking 31640)
            1: "Procedure: Rigid Bronchoscopy, Tracheal Debulking.\n- Site: Mid-trachea (Adenoid Cystic).\n- Action: Coring, snare, microdebrider.\n- Result: 70% -> 20% obstruction. No stent.\n- Plan: Floor.",
            2: "OPERATIVE REPORT: Ms. Stone presented with an adenoid cystic carcinoma obstructing the mid-trachea. Rigid bronchoscopy allowed for mechanical resection. The tumor was addressed via rigid coring and snare resection, followed by microdebrider refinement. This multimodal approach restored the tracheal lumen to near-normal caliber without the need for prosthetic stenting.",
            3: "Code 31640 (Bronchoscopy with tumor excision). Site: Trachea. Technique: Rigid bronchoscopy with snare resection and microdebrider excisional debulking. Pathology specimens obtained. No stent placed.",
            4: "Procedure: Tracheal Debulking\nAttending: Dr. Pierce\n1. Rigid scope.\n2. Snared and cored tracheal mass.\n3. Microdebrider for clean up.\n4. Good airway now.\nNo stent. To floor.",
            5: "tracheal tumor adenoid cystic. rigid bronch. we snared the big part then cleaned it up with the debrider. airway looks wide open now maybe 20 percent left. no stent. patient did well to floor.",
            6: "Rigid bronchoscopy for mid-tracheal mass. 70% obstruction. We resected the tumor using a snare and microdebrider. The airway was opened to near patency. Hemostasis achieved. No stent placement required. Patient stable.",
            7: "[Indication]\nMid-tracheal tumor.\n[Anesthesia]\nGeneral, rigid.\n[Description]\n70% narrowing. Resected via snare and microdebrider. Lumen restored. No stent.\n[Plan]\nFloor admission.",
            8: "Ms. Stone had a tumor growing in her trachea. We went in with a rigid scope and removed the mass using a snare and a shaving tool. We were able to clear most of the blockage, leaving the airway 80% open. She did not require a stent and is recovering well on the floor.",
            9: "Indication: Tracheal mass.\nProcedure: Endoscopy with lesion resection.\nIntervention: Tumor excised using snare and mechanical debridement. Tissue removed.\nOutcome: Airway patent."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for the 10 patients in the source file.
    Names are generated to ensure diversity across the 9 variations.
    """
    return [
        # Note 0: John Keller
        {"idx": 0, "orig_name": "John Keller", "orig_age": 72, "names": ["Robert Frost", "James Black", "William Green", "David White", "Michael Brown", "Thomas Gray", "Richard Blue", "Joseph Red", "Charles Gold"]},
        # Note 1: Maria Lopez
        {"idx": 1, "orig_name": "Maria Lopez", "orig_age": 64, "names": ["Anita Silva", "Carmen Diaz", "Elena Cruz", "Sofia Gomez", "Isabella Ruiz", "Lucia Ortiz", "Gabriela Ramos", "Rosa Torres", "Teresa Vega"]},
        # Note 2: George Patel
        {"idx": 2, "orig_name": "George Patel", "orig_age": 69, "names": ["Amit Singh", "Rajiv Kumar", "Sanjay Gupta", "Vikram Shah", "Rahul Sharma", "Arun Verma", "Nikhil Malhotra", "Deepak Jain", "Mohan Das"]},
        # Note 3: Elaine Young
        {"idx": 3, "orig_name": "Elaine Young", "orig_age": 61, "names": ["Susan Hall", "Karen King", "Nancy Wright", "Betty Scott", "Sandra Green", "Donna Baker", "Carol Adams", "Sharon Nelson", "Brenda Carter"]},
        # Note 4: Kevin Moore
        {"idx": 4, "orig_name": "Kevin Moore", "orig_age": 58, "names": ["Brian Wilson", "Gary Taylor", "Ronald Anderson", "Kenneth Thomas", "Paul Martinez", "Larry Robinson", "Jeffrey Clark", "Frank Rodriguez", "Scott Lewis"]},
        # Note 5: Oliver Grant
        {"idx": 5, "orig_name": "Oliver Grant", "orig_age": 63, "names": ["Peter Evans", "Walter Turner", "Harold Parker", "Arthur Collins", "Ryan Stewart", "Gregory Sanchez", "Jerry Morris", "Dennis Rogers", "Tyler Reed"]},
        # Note 6: Sarah Jenkins
        {"idx": 6, "orig_name": "Sarah Jenkins", "orig_age": 55, "names": ["Rebecca Cook", "Kathleen Morgan", "Amy Bell", "Shirley Murphy", "Angela Bailey", "Ruth Rivera", "Melissa Cooper", "Deborah Richardson", "Stephanie Cox"]},
        # Note 7: Lila Shah
        {"idx": 7, "orig_name": "Lila Shah", "orig_age": 49, "names": ["Priya Desai", "Anjali Mehta", "Meera Nair", "Kavita Reddy", "Neha Joshi", "Pooja Patel", "Riya Kaur", "Simran Singh", "Tanvi Agarwal"]},
        # Note 8: Robert Fields
        {"idx": 8, "orig_name": "Robert Fields", "orig_age": 59, "names": ["Edward Howard", "Jerry Ward", "Kyle Torres", "Adam Peterson", "Nathan Gray", "Zachary Ramirez", "Walter James", "Harold Watson", "Douglas Brooks"]},
        # Note 9: Margaret Stone
        {"idx": 9, "orig_name": "Margaret Stone", "orig_age": 71, "names": ["Helen Kelly", "Martha Sanders", "Virginia Price", "Dorothy Bennett", "Gloria Wood", "Alice Barnes", "Joyce Ross", "Frances Henderson", "Evelyn Coleman"]}
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
                    base_mrn = note_entry["registry_entry"]["patient_mrn"]
                    note_entry["registry_entry"]["patient_mrn"] = f"{base_mrn}_syn_{style_num}"
            
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
    output_filename = output_dir / "synthetic_part_057_part1.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()