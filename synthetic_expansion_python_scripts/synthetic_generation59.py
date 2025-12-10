import json
import random
import datetime
import copy
from pathlib import Path

# Source file configuration
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_059.json"
OUTPUT_DIR = "Synthetic_expansions"
OUTPUT_FILENAME = "synthetic_stent_debulking_notes_part_059.json"

def generate_random_date(year=2025):
    """Generates a random date within the specified year."""
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each note index.
    Structure: { Note_Index (0-9): { Style_Index (1-9): "Variation Text" } }
    """
    variations = {
        0: { # Barbara Williams (Stent LMS)
            1: "Proc: Rigid bronch w/ stent.\nInd: Esophageal CA, tracheal inv.\nActions:\n- Jet vent.\n- APC tumor ablation.\n- Novatech Silicone stent (14x60mm) placed Left mainstem.\n- Patency confirmed.\nPost-op: 14% obstruct. No comp.",
            2: "HISTORY: Ms. Williams, an 81-year-old female with esophageal carcinoma and secondary tracheal invasion, presented for therapeutic intervention.\nOPERATIVE REPORT: Under general anesthesia utilizing jet ventilation, the airway was accessed via rigid bronchoscopy. Significant obstruction was noted in the Left Mainstem (LMS). Argon Plasma Coagulation (APC) was utilized for thermal ablation of the endoluminal tumor component. Subsequently, the airway dimensions were sized, and a 14x60mm Novatech Silicone (Dumon) stent was deployed. Immediate relief of obstruction was visualized, with residual stenosis estimated at 14%.",
            3: "Procedures Performed:\n1. Therapeutic Rigid Bronchoscopy (31641): Destruction of tumor utilizing Argon Plasma Coagulation to prepare airway.\n2. Bronchial Stent Placement (31636): Deployment of Novatech Silicone stent, 14mm x 60mm, into the Left Mainstem Bronchus.\nMedical Necessity: 72% malignant obstruction reduced to 14% to restore patency.",
            4: "Resident Procedure Note\nAttending: Dr. Martinez\nPatient: Barbara Williams\nProcedure: Rigid Bronchoscopy, Stent Placement\nSteps:\n1. Timeout performed.\n2. General anesthesia with jet ventilation.\n3. Rigid scope inserted. 72% obstruction seen in LMS.\n4. APC used to ablate tumor tissue (31641).\n5. Novatech stent 14x60mm deployed (31636).\n6. Good expansion confirmed.\nPlan: Admit for observation.",
            5: "Note for Barbara Williams we did the bronchoscopy today used the rigid scope because of the cancer invading the trachea. Dr Martinez was attending. We used the APC to burn the tumor a bit then put in a novatech silicone stent size 14 by 60 in the left main. looks much better now maybe 14 percent blocked. patient tolerated it fine minimal bleeding sending to recovery then floor thanks.",
            6: "Esophageal cancer with tracheal invasion necessitating intervention. Pre-procedure obstruction approximately 72% at Left mainstem. Under general anesthesia with jet ventilation, rigid bronchoscopy was performed. APC was utilized for tumor ablation prior to stent placement. The airway was measured and a Novatech Silicone - Dumon stent (14x60mm) was deployed in the Left mainstem. Stent position confirmed with good expansion and patency. Post-procedure obstruction was reduced to approximately 14%. There were no complications and EBL was minimal. Plan is for clinic follow up in 4-6 weeks.",
            7: "[Indication]\nEsophageal cancer, tracheal invasion, 72% LMS obstruction.\n[Anesthesia]\nGeneral, Jet Ventilation.\n[Description]\nRigid bronchoscopy. APC ablation performed. Novatech Silicone stent (14x60mm) deployed in LMS. Obstruction reduced to 14%.\n[Plan]\nAdmit overnight. Clinic f/u 4-6 wks.",
            8: "The patient was brought to the operating room and placed under general anesthesia with jet ventilation. We performed a rigid bronchoscopy to address the esophageal cancer invasion. First, we used APC to ablate the tumor tissue. Once the airway was prepared, we measured the defect and deployed a 14x60mm Novatech Silicone stent into the Left Mainstem. The stent expanded well, and the obstruction was significantly reduced.",
            9: "Under general anesthesia with jet ventilation, rigid bronchoscopy was conducted. APC was employed for tumor destruction preceding stent insertion. The airway was gauged and a Novatech Silicone - Dumon stent (14x60mm) was positioned in the Left mainstem. Stent location was verified with adequate expansion. Post-procedure blockage was ~14%. No adverse events."
        },
        1: { # Donald Thomas (Laser BI)
            1: "Dx: Esophageal CA, tracheal inv.\nProc: Rigid bronch, Laser ablation.\nSite: Bronchus Intermedius (BI).\nOp:\n- Tumor at BI.\n- Laser used for sequential removal.\n- Max debulking achieved.\nResult: 15% residual. EBL 50mL.\nPlan: ICU obs.",
            2: "OPERATIVE NARRATIVE: The patient, Mr. Thomas, presented with 79% obstruction at the Bronchus Intermedius due to invasive esophageal carcinoma. Rigid bronchoscopy was initiated under general anesthesia. An endobronchial mass was identified. We proceeded with Laser ablation (CPT 31640), performing multiple passes to excise the tumor tissue sequentially. Excellent hemostasis was maintained. The airway caliber was significantly improved, leaving only 15% residual obstruction.",
            3: "Coding Data:\nPrimary Procedure: 31640 (Bronchoscopy with tumor excision).\nModality: Laser Ablation.\nLocation: Bronchus Intermedius.\nDetails: Visualization of 79% obstruction. Systematic laser excision performed to debulk tumor. Specimens sent for histology. Hemostasis achieved. Code 31640 supported by excision of endobronchial tumor.",
            4: "Procedure: Rigid Bronchoscopy with Laser Ablation\nPatient: Donald Thomas\nStaff: Dr. Lee\nSteps:\n1. General anesthesia induced.\n2. Rigid scope advanced to BI.\n3. Tumor identified.\n4. Laser used to ablate and remove tumor in pieces.\n5. Hemostasis good.\n6. Residual stenosis ~15%.\nDisposition: ICU.",
            5: "donald thomas procedure note. we took him to the OR for the esophageal cancer blocking the airway. used the laser to burn the tumor out of the bronchus intermedius. did a few passes to get it all out. bleeding was about 50ml pretty standard. looks like we got it down to 15% blockage. sending him to the ICU tonight just to watch him.",
            6: "Esophageal cancer with tracheal invasion. Pre-procedure 79% obstruction at BI. Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at BI. Laser ablation performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Post-procedure 15% residual obstruction. EBL 50mL. Hemostasis achieved. Specimens sent for histology. Recovery then ICU observation overnight.",
            7: "[Indication]\nEsophageal cancer, 79% obstruction at BI.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Laser ablation utilized for tumor excision. Multiple passes for debulking. Residual obstruction 15%.\n[Plan]\nICU admission. Oncology follow-up.",
            8: "We performed a rigid bronchoscopy on Mr. Thomas to address the obstruction in his Bronchus Intermedius. Upon visualization, we used laser ablation to carefully excise the tumor. We made multiple passes to ensure maximal debulking was achieved. The procedure was successful, reducing the obstruction from 79% down to 15%, with minimal blood loss.",
            9: "Under general anesthesia, rigid bronchoscopy was executed. An endobronchial neoplasm was found at the BI. Laser destruction was carried out with sequential tumor extraction. Several passes were completed to attain maximal reduction. Post-procedure residual blockage was ~15%. Hemostasis secured."
        },
        2: { # Melissa Young (Stent BI)
            1: "Indication: Thyroid CA, tracheal compression.\nProc: Rigid bronch, APC, Stent.\nDevice: Ultraflex SEMS Covered (20x40mm).\nLoc: Bronchus Intermedius.\nOutcome: 83% -> 24% obstruction.\nPlan: Admit floor.",
            2: "PREOPERATIVE DIAGNOSIS: Thyroid carcinoma with extrinsic tracheal compression and invasion.\nPROCEDURE: Rigid bronchoscopy with therapeutic stenting.\nFINDINGS: Critical stenosis (83%) noted at the Bronchus Intermedius. The lesion was pre-treated with APC ablation to facilitate stent seating. An Ultraflex Self-Expanding Metallic Stent (Covered, 20x40mm) was successfully deployed. Verification of stent expansion confirmed restoration of airway patency (24% residual stenosis).",
            3: "Billing Explanation:\n- 31636: Placement of bronchial stent (Ultraflex SEMS) in Bronchus Intermedius.\n- 31641: Destruction of tumor via APC prior to stenting.\nMedical Necessity: Relief of 83% malignant obstruction caused by thyroid cancer.",
            4: "Resident Note: Melissa Young\nAttending: Dr. Lee\nProcedure: Bronchoscopy with Stent\n1. Inducted GA/Jet vent.\n2. Scope to Bronchus Intermedius.\n3. APC used for prep/ablation.\n4. Ultraflex Covered stent 20x40mm deployed.\n5. Checked position: Good.\nNo complications.",
            5: "note for melissa young 70yo female with thyroid cancer compressing the airway. we went in with the rigid scope. used apc to clear some space then put in an ultraflex covered stent 20 by 40 in the bronchus intermedius. opened up nicely. went from 83 percent blocked to maybe 24. admitting her to the floor.",
            6: "Thyroid cancer with tracheal compression. Pre-procedure obstruction approximately 83% Bronchus intermedius. Under general anesthesia with jet ventilation, rigid bronchoscopy performed. APC used for tumor ablation prior to stent placement. Airway measured and Ultraflex SEMS - Covered stent (20x40mm) deployed in Bronchus intermedius. Stent position confirmed with good expansion and patency. Post-procedure obstruction approximately 24%. No complications.",
            7: "[Indication]\nThyroid CA, 83% BI obstruction.\n[Anesthesia]\nGeneral, Jet Vent.\n[Description]\nRigid bronchoscopy. APC ablation. Ultraflex SEMS Covered (20x40mm) deployed in BI. Residual obstruction 24%.\n[Plan]\nFloor admission. Repeat bronch 4-6 wks.",
            8: "Ms. Young underwent rigid bronchoscopy under general anesthesia due to tracheal compression from thyroid cancer. We first utilized APC to ablate the tumor and prepare the airway. Following this, we measured the stenosis and deployed a 20x40mm Ultraflex Covered SEMS into the Bronchus Intermedius. The stent expanded well, significantly improving airway patency.",
            9: "Under general anesthesia with jet ventilation, rigid bronchoscopy was undertaken. APC was applied for tumor destruction before stent insertion. The airway was sized and an Ultraflex SEMS - Covered stent (20x40mm) was positioned in the Bronchus intermedius. Stent placement was verified with satisfactory dilation."
        },
        3: { # Anthony Taylor (Debulk BI)
            1: "Ind: Met lung cancer, 60% BI obstruct.\nProc: Rigid bronch debulking.\nTools: Biopsy forceps, APC/Laser.\nAction: Mechanical removal + thermal ablation base.\nResult: 32% residual. 75mL EBL.\nPlan: ICU.",
            2: "PROCEDURE REPORT: Mr. Taylor, a 61-year-old male with metastatic lung cancer, underwent therapeutic rigid bronchoscopy. A 60% obstruction was visualized at the Bronchus Intermedius. Mechanical debulking was performed utilizing rigid biopsy forceps for piecemeal excision. Following bulk removal, APC and Laser were employed for hemostasis and ablation of the tumor base (CPT 31641). Anatomical patency was improved to 32% residual stenosis.",
            3: "Code: 31641 (Bronchoscopy with destruction/ablation).\nSupport: Use of APC and Laser for tumor base ablation following mechanical debulking.\nTarget: Bronchus Intermedius.\nPathology: Metastatic malignancy.\nOutcome: Improvement from 60% to 32% obstruction.",
            4: "Procedure: Rigid Bronchoscopy Debulking\nPt: Anthony Taylor\nSteps:\n1. GA induced.\n2. Tumor seen at BI (60%).\n3. Forceps used to remove tumor chunks.\n4. Laser/APC used to burn the base and stop bleeding.\n5. Suctioned clear.\n6. Est residual: 32%.\nPlan: ICU.",
            5: "anthony taylor dictation. he has lung cancer mets causing blockage in the BI. we did a rigid bronch today. used the biopsy forceps to grab the tumor out piece by piece. then used the laser and apc to clean up the base and stop the bleeding. blood loss maybe 75ml. airway looks better about 32% blocked now. sending to ICU.",
            6: "Metastatic lung cancer with bronchial obstruction. Pre-procedure 60% obstruction at BI. Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at BI. Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC/laser used for hemostasis and tumor base ablation. Post-procedure 32% residual obstruction. EBL 75mL.",
            7: "[Indication]\nMetastatic lung CA, 60% BI obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Mechanical debulking with forceps. APC/Laser ablation of tumor base. Residual obstruction 32%.\n[Plan]\nICU observation. Oncology f/u.",
            8: "We performed a rigid bronchoscopy on Mr. Taylor to manage his metastatic lung cancer obstruction. Using biopsy forceps, we mechanically debulked the tumor in the Bronchus Intermedius. We followed this with APC and laser treatment to ablate the remaining tumor base and ensure hemostasis. The procedure successfully reduced the blockage from 60% to 32%.",
            9: "Under general anesthesia, rigid bronchoscopy was carried out. An endobronchial lesion was located at the BI. Rigid bronchoscopy debulking with biopsy forceps was executed with sequential tumor extraction. Supplemental APC/laser was used for hemostasis and tumor base destruction. Post-procedure ~32% residual blockage."
        },
        4: { # Thomas Allen (Stent Trachea)
            1: "Dx: Lung Adenocarcinoma, Tracheal CAO.\nProc: Rigid bronch, Stent.\nImplant: Novatech Silicone 20x60mm Trachea.\nResult: 76% -> 15% obstruction.\nComplications: None.\nPlan: Floor admit.",
            2: "OPERATIVE NOTE: Mr. Allen presented with critical central airway obstruction (76% Trachea) secondary to primary lung adenocarcinoma. Rigid bronchoscopy was performed under general anesthesia. The tracheal lumen was sized, and a 20x60mm Novatech Silicone (Dumon) stent was deployed. Post-deployment inspection confirmed excellent expansion and restoration of airway caliber (15% residual).",
            3: "CPT Justification: 31631 (Bronchoscopy with placement of tracheal stent).\nDevice: Novatech Silicone Stent (20x60mm).\nLocation: Trachea (Distinct from bronchial codes).\nIndication: 76% obstruction reduced to 15%.",
            4: "Resident: Dr. Liu\nAttending: Dr. Chen\nPt: Thomas Allen\nProc: Tracheal Stent\n1. Rigid scope inserted.\n2. Measured tracheal stenosis (76%).\n3. Deployed Novatech stent 20x60mm.\n4. Verified patency.\n5. No complications.\nPlan: Admit.",
            5: "procedure note for thomas allen. he has lung cancer blocking the trachea pretty bad about 76 percent. dr chen and i did a rigid bronch. put in a dumon silicone stent 20 by 60 right in the trachea. opened up great residual is only 15 percent now. no bleeding issues. admit to floor for observation.",
            6: "Primary lung adenocarcinoma with CAO. Pre-procedure obstruction 76% Trachea. Under general anesthesia with jet ventilation, rigid bronchoscopy performed. Airway measured and Novatech Silicone - Dumon stent (20x60mm) deployed in Trachea. Stent position confirmed with good expansion and patency. Post-procedure obstruction 15%. No complications. EBL minimal. Recovery then floor admission for overnight observation.",
            7: "[Indication]\nLung AdenoCA, 76% Tracheal obstruction.\n[Anesthesia]\nGeneral, Jet Vent.\n[Description]\nRigid bronchoscopy. Novatech Silicone stent (20x60mm) deployed in Trachea. Expansion confirmed. Residual obstruction 15%.\n[Plan]\nFloor admission. Repeat bronch 4-6 wks.",
            8: "Mr. Allen was treated for a significant tracheal obstruction caused by lung adenocarcinoma. Under general anesthesia, we advanced the rigid bronchoscope and measured the affected area. We then successfully deployed a 20x60mm Novatech Silicone stent. The stent expanded fully, reducing the obstruction from 76% to 15%, providing immediate relief.",
            9: "Under general anesthesia with jet ventilation, rigid bronchoscopy was performed. The airway was measured and a Novatech Silicone - Dumon stent (20x60mm) was inserted in the Trachea. Stent placement was verified with good expansion and patency. Post-procedure blockage was ~15%. No adverse events."
        },
        5: { # Ronald Young (Cryo RMS)
            1: "Ind: Squamous cell CA, RMS block.\nProc: Rigid bronch, Cryoextraction.\nAction: Tumor frozen/removed piecemeal. Laser/APC for base.\nResult: 77% -> 22% obstruction.\nEBL: 50mL.\nPlan: ICU.",
            2: "PROCEDURE: Rigid bronchoscopy with cryotherapy for malignant airway obstruction.\nPATIENT: Mr. Young, 58M.\nFINDINGS: 77% obstruction of the Right Mainstem (RMS) by squamous cell carcinoma. Cryoextraction was utilized to debulk the exophytic tumor component. Following bulk removal, the tumor base was treated with APC and Laser to ensure hemostasis and further ablation (CPT 31641). Final airway inspection revealed 22% residual stenosis.",
            3: "Service: Bronchoscopy with tumor destruction (31641).\nMethod: Cryoextraction and Laser/APC ablation.\nSite: Right Mainstem Bronchus.\nPre-op: 77% occlusion.\nPost-op: 22% occlusion.\nSpecimens: Sent for histology.",
            4: "Procedure: Rigid Bronch w/ Cryo\nPatient: Ronald Young\nSteps:\n1. GA. Rigid scope to RMS.\n2. Tumor found.\n3. Cryo probe used to freeze and pull tumor chunks.\n4. Laser used to clean up base.\n5. Good hemostasis.\n6. Residual 22%.\nPlan: ICU.",
            5: "ronald young dictation. squamous cell cancer blocking the right mainstem. we used the cryo probe to pull the tumor out frozen. did a bunch of passes. then used the laser to stop the bleeding at the base. went from 77 percent blocked to 22 percent. pretty good result. 50ml blood loss. sending him to icu.",
            6: "Squamous cell carcinoma with airway compromise. Pre-procedure 77% obstruction at RMS. Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at RMS. Cryoextraction performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Additional APC/laser used for hemostasis and tumor base ablation. Post-procedure 22% residual obstruction. EBL 50mL.",
            7: "[Indication]\nSquamous Cell CA, 77% RMS obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Cryoextraction for debulking. APC/Laser for base ablation. Residual obstruction 22%.\n[Plan]\nICU admission.",
            8: "We brought Mr. Young to the OR to address the blockage in his right mainstem bronchus. Using a rigid bronchoscope, we employed cryoextraction to freeze and remove the tumor in sections. We then used APC and laser to treat the base of the tumor and control bleeding. The obstruction was reduced from 77% to 22%.",
            9: "Under general anesthesia, rigid bronchoscopy was executed. An endobronchial tumor was identified at the RMS. Cryoextraction was carried out with sequential tumor extraction. Several passes were completed to attain maximal reduction. Supplemental APC/laser was used for hemostasis and tumor base destruction."
        },
        6: { # Jason Green (Microdebrider LMS)
            1: "Dx: Thyroid CA, LMS compression.\nProc: Rigid bronch, Microdebrider.\nAction: Sequential shaving of tumor. 76% -> 31%.\nEBL: 50mL.\nPlan: ICU obs.",
            2: "OPERATIVE SUMMARY: Mr. Green presented with 76% obstruction of the Left Mainstem Bronchus due to thyroid malignancy. Under general anesthesia, a rigid bronchoscope was introduced. The microdebrider blade was utilized to shave and aspirate the endoluminal tumor component (CPT 31640). Multiple passes achieved significant luminal gain, resulting in 31% residual obstruction. Hemostasis was maintained.",
            3: "Code: 31640 (Bronchoscopy with excision of tumor).\nTool: Microdebrider.\nLocation: Left Mainstem Bronchus.\nJustification: Mechanical excision of malignant tissue to relieve 76% obstruction. Pathology specimens generated.",
            4: "Resident Note: Jason Green\nProcedure: Microdebrider Debulking\n1. Rigid scope inserted.\n2. Tumor at LMS identified.\n3. Microdebrider used to resect tumor.\n4. Suctioned clear.\n5. Residual block 31%.\n6. Hemostasis achieved.\nPlan: ICU.",
            5: "jason green procedure note. thyroid cancer pushing into the LMS. we used the microdebrider to shave it down. took a while but we got it from 76 percent down to 31 percent. bleeding was controlled. sending him to the icu to watch overnight.",
            6: "Thyroid cancer with tracheal compression. Pre-procedure 76% obstruction at LMS. Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at LMS. Microdebrider assisted tumor removal performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Post-procedure 31% residual obstruction. EBL 50mL. Hemostasis achieved.",
            7: "[Indication]\nThyroid CA, 76% LMS obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Microdebrider excision of tumor. Residual obstruction 31%.\n[Plan]\nICU admission.",
            8: "Mr. Green underwent rigid bronchoscopy for a thyroid cancer tumor invading the left mainstem bronchus. We utilized a microdebrider to carefully excise the tumor tissue. After multiple passes, we successfully debulked the lesion, improving the airway patency from 76% obstruction to 31%.",
            9: "Under general anesthesia, rigid bronchoscopy was performed. An endobronchial tumor was identified at the LMS. Microdebrider assisted tumor extraction was performed with sequential tumor removal. Several passes were completed to attain maximal reduction. Post-procedure ~31% residual blockage."
        },
        7: { # Rebecca Miller (Debulk/Balloon RLL)
            1: "Ind: Malignant CAO, RLL.\nProc: Rigid bronch, Forceps debulk, Balloon dilation.\nAction: Mech removal + dilation of stenosis.\nResult: 72% -> 15%.\nEBL: 75mL.\nPlan: ICU.",
            2: "PROCEDURE NOTE: Ms. Miller underwent rigid bronchoscopy for malignant obstruction of the Right Lower Lobe (RLL) orifice. Initial inspection revealed 72% occlusion. Mechanical debulking was performed using biopsy forceps (CPT 31640). Following tumor removal, residual stenosis was addressed via balloon dilation to maximize airway diameter. Final obstruction was estimated at 15%.",
            3: "Coding: 31640 (Tumor excision via forceps).\nNote: Balloon dilation performed for residual stenosis (incidental to debulking or separate 31630 depending on payer rules, here coded as 31640 primary modality).\nSite: RLL Orifice.\nOutcome: Significant patency improvement.",
            4: "Procedure: Forceps Debulking + Balloon\nPt: Rebecca Miller\nSteps:\n1. GA induced.\n2. Tumor at RLL (72%).\n3. Forceps used to remove tumor.\n4. Balloon used to dilate the area.\n5. Good result (15% residual).\nPlan: ICU.",
            5: "rebecca miller note. she has a tumor blocking the RLL. we went in with the rigid scope and grabbed the tumor with the forceps. cleared most of it out. then used a balloon to stretch it open a bit more. looks good now only 15 percent blocked. blood loss 75ml. icu for tonight.",
            6: "Malignant central airway obstruction. Pre-procedure 72% obstruction at RLL orifice. Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at RLL orifice. Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal. Balloon dilation performed for residual stenosis. Post-procedure 15% residual obstruction. EBL 75mL.",
            7: "[Indication]\nMalignancy, 72% RLL obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Forceps debulking. Balloon dilation. Residual obstruction 15%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy on Ms. Miller to treat a malignant obstruction in the Right Lower Lobe orifice. We primarily used biopsy forceps to mechanically remove the tumor. After the bulk was removed, we used a balloon to dilate the airway and treat the residual stenosis. The obstruction was reduced from 72% to 15%.",
            9: "Under general anesthesia, rigid bronchoscopy was executed. An endobronchial tumor was found at the RLL orifice. Rigid bronchoscopy debulking with biopsy forceps was carried out with sequential tumor extraction. Balloon dilation was performed for residual stenosis. Post-procedure ~15% residual blockage."
        },
        8: { # Robert Johnson (Microdebrider BI)
            1: "Ind: Met lung CA, 85% BI block.\nProc: Rigid bronch, Microdebrider.\nAction: Aggressive debulking.\nResult: 85% -> 25%.\nEBL: 50mL.\nPlan: ICU.",
            2: "OPERATIVE REPORT: Mr. Johnson presented with severe (85%) obstruction of the Bronchus Intermedius due to metastatic lung cancer. Under general anesthesia, therapeutic rigid bronchoscopy was performed. The microdebrider was employed to excise the endobronchial tumor mass (CPT 31640). Systemic debulking resulted in a patent airway with 25% residual narrowing. Hemostasis was excellent.",
            3: "Code: 31640 (Excision of tumor).\nInstrument: Microdebrider.\nSite: Bronchus Intermedius.\nRationale: Excision of 85% obstructing mass to restore ventilation. Specimens sent for path.",
            4: "Procedure: Microdebrider Debulking\nPt: Robert Johnson\nSteps:\n1. GA/Rigid scope.\n2. 85% block at BI.\n3. Microdebrider used to clear tumor.\n4. Multiple passes.\n5. Residual 25%.\nPlan: ICU.",
            5: "robert johnson note. lung cancer blocking the bronchus intermedius almost completely 85 percent. used the microdebrider to open it up. worked well. got it down to 25 percent. minimal bleeding. sending him to the icu to recover.",
            6: "Metastatic lung cancer with bronchial obstruction. Pre-procedure 85% obstruction at BI. Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at BI. Microdebrider assisted tumor removal performed with sequential tumor removal. Multiple passes performed to achieve maximal debulking. Post-procedure 25% residual obstruction. EBL 50mL.",
            7: "[Indication]\nMetastatic lung CA, 85% BI obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Microdebrider excision. Residual obstruction 25%.\n[Plan]\nICU admission.",
            8: "Mr. Johnson required urgent intervention for an 85% obstruction in his Bronchus Intermedius caused by metastatic lung cancer. We performed a rigid bronchoscopy and utilized a microdebrider to shave away the tumor. We made multiple passes until the airway was significantly more open, leaving only a 25% residual obstruction.",
            9: "Under general anesthesia, rigid bronchoscopy was performed. An endobronchial tumor was identified at the BI. Microdebrider assisted tumor extraction was performed with sequential tumor removal. Several passes were completed to attain maximal reduction. Post-procedure ~25% residual blockage."
        },
        9: { # Stephanie Allen (Microdebrider/APC LMS)
            1: "Ind: Met lung CA, 62% LMS.\nProc: Rigid bronch, Microdebrider, APC.\nAction: Excision + Ablation.\nResult: 62% -> 39%.\nEBL: 50mL.\nPlan: ICU.",
            2: "PROCEDURE NOTE: Ms. Allen underwent rigid bronchoscopy for metastatic obstruction of the Left Mainstem (62%). The microdebrider was used for bulk excision of the tumor. Following mechanical removal, APC/Laser was utilized to ablate the tumor base and ensure hemostasis (CPT 31641). The airway was successfully recanalized to 39% residual obstruction.",
            3: "Code: 31641 (Destruction/Ablation).\nSupport: Combination of Microdebrider for debulking and APC/Laser for thermal ablation of base.\nSite: Left Mainstem.\nOutcome: Partial restoration of patency.",
            4: "Procedure: Debulking (Microdebrider + APC)\nPt: Stephanie Allen\nSteps:\n1. GA induced.\n2. LMS obstruction 62%.\n3. Microdebrider used to remove bulk.\n4. APC used on base.\n5. Residual 39%.\nPlan: ICU.",
            5: "stephanie allen note. she has mets to the LMS blocking it about 62 percent. we used the microdebrider to take out the bulk of it. then used the laser and apc to burn the rest and stop bleeding. residual is 39 percent. blood loss 50ml. icu for observation.",
            6: "Metastatic lung cancer with bronchial obstruction. Pre-procedure 62% obstruction at LMS. Under general anesthesia, rigid bronchoscopy performed. Endobronchial tumor identified at LMS. Microdebrider assisted tumor removal performed with sequential tumor removal. Additional APC/laser used for hemostasis and tumor base ablation. Post-procedure 39% residual obstruction. EBL 50mL.",
            7: "[Indication]\nMetastatic lung CA, 62% LMS obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Microdebrider excision. APC/Laser ablation. Residual obstruction 39%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy on Ms. Allen to address a 62% obstruction in the Left Mainstem. We used a microdebrider to mechanically remove the tumor bulk. Following this, we used APC and laser to ablate the tumor base and control bleeding. The obstruction was reduced to 39%.",
            9: "Under general anesthesia, rigid bronchoscopy was executed. An endobronchial tumor was found at the LMS. Microdebrider assisted tumor extraction was performed with sequential tumor removal. Supplemental APC/laser was used for hemostasis and tumor base destruction. Post-procedure ~39% residual blockage."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns a list of mock data dictionaries for the 10 patients.
    Each entry corresponds to an index in the source file.
    Includes original name/age and 9 variations for names.
    """
    return [
        {
            "idx": 0, "orig_name": "Barbara Williams", "orig_age": 81,
            "names": ["Mary Jones", "Patricia Brown", "Linda Davis", "Elizabeth Miller", "Barbara Wilson", "Margaret Moore", "Susan Taylor", "Dorothy Anderson", "Lisa Thomas"]
        },
        {
            "idx": 1, "orig_name": "Donald Thomas", "orig_age": 76,
            "names": ["James Jackson", "John White", "Robert Harris", "Michael Martin", "William Thompson", "David Garcia", "Richard Martinez", "Charles Robinson", "Joseph Clark"]
        },
        {
            "idx": 2, "orig_name": "Melissa Young", "orig_age": 70,
            "names": ["Nancy Rodriguez", "Karen Lewis", "Betty Lee", "Helen Walker", "Sandra Hall", "Donna Allen", "Carol Young", "Ruth Hernandez", "Sharon King"]
        },
        {
            "idx": 3, "orig_name": "Anthony Taylor", "orig_age": 61,
            "names": ["Thomas Wright", "Christopher Lopez", "Daniel Hill", "Paul Scott", "Mark Green", "Donald Adams", "George Baker", "Kenneth Gonzalez", "Steven Nelson"]
        },
        {
            "idx": 4, "orig_name": "Thomas Allen", "orig_age": 81,
            "names": ["Edward Carter", "Brian Mitchell", "Ronald Perez", "Anthony Roberts", "Kevin Turner", "Jason Phillips", "Matthew Campbell", "Gary Parker", "Timothy Evans"]
        },
        {
            "idx": 5, "orig_name": "Ronald Young", "orig_age": 58,
            "names": ["Frank Edwards", "Larry Collins", "Scott Stewart", "Stephen Sanchez", "Andrew Morris", "Raymond Rogers", "Gregory Reed", "Joshua Cook", "Jerry Morgan"]
        },
        {
            "idx": 6, "orig_name": "Jason Green", "orig_age": 66,
            "names": ["Dennis Bell", "Walter Murphy", "Patrick Bailey", "Peter Rivera", "Harold Cooper", "Douglas Richardson", "Henry Cox", "Carl Howard", "Arthur Ward"]
        },
        {
            "idx": 7, "orig_name": "Rebecca Miller", "orig_age": 70,
            "names": ["Michelle Torres", "Laura Peterson", "Sarah Gray", "Kimberly Ramirez", "Deborah James", "Jessica Watson", "Shirley Brooks", "Cynthia Kelly", "Angela Sanders"]
        },
        {
            "idx": 8, "orig_name": "Robert Johnson", "orig_age": 72,
            "names": ["Jose Price", "Adam Bennett", "Nathan Wood", "Ben Barnes", "Samuel Ross", "Willie Henderson", "Roy Coleman", "Gerald Jenkins", "Billy Perry"]
        },
        {
            "idx": 9, "orig_name": "Stephanie Allen", "orig_age": 56,
            "names": ["Brenda Powell", "Amy Long", "Anna Patterson", "Virginia Hughes", "Kathleen Flores", "Pamela Washington", "Martha Butler", "Debra Simmons", "Amanda Foster"]
        }
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
            rand_date_obj = generate_random_date(2025)
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
    output_filename = output_dir / OUTPUT_FILENAME
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()