import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_055_part3.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Jackson, John (Debulking BI)
            1: "Dx: Lung CA with obstruction.\nProc: Rigid bronch.\nFindings: Tumor at BI (75% obstructed).\nAction: Mech debulking w/ forceps. APC/Laser for hemostasis.\nResult: 12% residual. EBL 75cc.\nPlan: ICU. Obs.",
            2: "HISTORY: The patient presented with symptomatic central airway obstruction secondary to primary lung adenocarcinoma. \nPROCEDURE: Rigid bronchoscopy was undertaken under general anesthesia. The bronchus intermedius (BI) was visualized, revealing an endobronchial exophytic mass causing approximately 75% luminal stenosis. Mechanical debulking was executed utilizing rigid biopsy forceps in a sequential fashion. Following maximal tumor resection, thermal ablation via Argon Plasma Coagulation (APC) and laser was applied to the tumor base to ensure hemostasis and destroy residual neoplastic tissue. \nOUTCOME: Post-procedure luminal patency was significantly improved to approximately 12% residual obstruction.",
            3: "Procedure: Therapeutic Bronchoscopy.\nTechnique:\n1. Rigid Bronchoscopy (CPT 31640): Used for mechanical excision of endobronchial tumor at the Bronchus Intermedius (BI).\n2. Ablation (CPT 31641): APC and Laser utilized for destruction of residual tumor base and hemostasis.\nDocumentation of Necessity: 75% obstruction reduced to 12%. Improvement in airway mechanics achieved.",
            4: "Resident Note:\nAttending: Dr. Rodriguez\nPt: 51M w/ Lung CA.\nProcedure steps:\n1. Time out.\n2. General anesthesia induced.\n3. Rigid scope inserted.\n4. Identified tumor at BI.\n5. Debulked using forceps (multiple passes).\n6. Used APC/Laser for cleanup.\n7. Good hemostasis.\nPlan: ICU for monitoring.",
            5: "did the bronch today on mr jackson he has that tumor in the BI rigid scope used took out the tumor with forceps big chunks removed used some laser and apc to stop the bleeding looks much better now maybe 12 percent left airway looks open patient tolerated well sent to icu for watch thanks.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at BI Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Additional APC laser used for hemostasis and tumor base ablation Post procedure 12 percent residual obstruction EBL 75mL Hemostasis achieved Specimens sent for histology",
            7: "[Indication]\nPrimary lung adenocarcinoma with central airway obstruction (BI).\n[Anesthesia]\nGeneral Anesthesia, Rigid Bronchoscopy.\n[Description]\nTumor identified at BI (75% obstruction). Mechanical debulking performed via forceps. Laser/APC applied for base ablation. Residual obstruction ~12%.\n[Plan]\nICU observation. Monitor for re-obstruction.",
            8: "The patient, a 51-year-old male with primary lung adenocarcinoma, underwent rigid bronchoscopy to address a severe obstruction. Upon entering the airway, we identified an endobronchial tumor at the Bronchus Intermedius causing 75% blockage. We proceeded with rigid bronchoscopy debulking, utilizing biopsy forceps to remove the tumor sequentially. After multiple passes, we used APC and laser to ablate the tumor base and ensure hemostasis. The final result was a patent airway with only 12% residual obstruction.",
            9: "Indication: Primary lung adenocarcinoma with CAO. Pre-procedure: ~75% blockage at BI. PROCEDURE: Under general anesthesia, rigid bronchoscopy conducted. Endobronchial lesion spotted at BI. Rigid bronchoscopy resection with biopsy forceps conducted with sequential tumor extraction. Multiple passes conducted to achieve maximal reduction. Additional APC/laser utilized for coagulation and tumor base destruction. Post-procedure: ~12% residual blockage. EBL: ~75mL. Hemostasis secured. Samples dispatched for histology."
        },
        1: { # Wilson, William (Stent Trachea)
            1: "Indication: Malignant CAO.\nProc: Rigid bronch, jet vent.\nAction: Dilation of tracheal stenosis. Y-Stent (Dumon 20x40) deployed.\nResult: Obstruction reduced 78% -> 21%.\nPlan: Admit. F/U 4wks.",
            2: "OPERATIVE REPORT: The patient, Mr. Wilson, presented with malignant central airway obstruction affecting the trachea. Under general anesthesia employing jet ventilation, a rigid bronchoscope was introduced. The tracheal stenosis was addressed first via sequential balloon dilation. Subsequently, airway sizing was performed, and a silicone Dumon Y-Stent (20x40mm) was precisely deployed within the trachea. Visual inspection confirmed excellent expansion, patency, and positioning of the prosthesis. The obstruction was reduced from 78% to 21%.",
            3: "Code Selection: 31636 (Bronchoscopy with stent placement, initial bronchus).\nSpecifics:\n- Modality: Rigid Bronchoscopy.\n- Location: Trachea.\n- Device: Dumon Y-Stent (20x40mm).\n- Adjuncts: Balloon dilation performed to facilitate placement (included).\n- Outcome: Restoration of airway patency confirmed.",
            4: "Procedure: Tracheal Stent Placement\nStaff: Dr. Park / Dr. Torres\nSteps:\n1. GA / Jet ventilation.\n2. Rigid bronchoscopy.\n3. Balloon dilation of stenosis.\n4. Measured airway.\n5. Deployed Dumon Y-Stent 20x40mm.\n6. Confirmed position.\nNo complications.",
            5: "patient has malignant obstruction in the trachea we did a rigid bronch on him today general anesthesia jet vent dilated the stenosis with a balloon then put in a dumon y stent 20 by 40 size looked good after deployment airway open obstruction down to 21 percent minimal bleeding sending to floor for observation.",
            6: "Under general anesthesia with jet ventilation rigid bronchoscopy performed Sequential balloon dilation of trachea stenosis performed Airway measured and Dumon Y Stent Y Stent stent 20x40mm deployed in Trachea Stent position confirmed with good expansion and patency Post procedure obstruction 21 percent No complications EBL minimal",
            7: "[Indication]\nMalignant central airway obstruction (Trachea).\n[Anesthesia]\nGeneral with Jet Ventilation.\n[Description]\nRigid bronchoscopy. Sequential balloon dilation. Dumon Y-Stent (20x40mm) deployed. Obstruction improved from 78% to 21%.\n[Plan]\nAdmit overnight. Clinic F/U 4-6 weeks.",
            8: "We performed a rigid bronchoscopy on Mr. Wilson to address his malignant tracheal obstruction. Utilizing jet ventilation, we first dilated the stenotic area with a balloon. Once the airway was prepared, we measured and deployed a Dumon Y-Stent (20x40mm) into the trachea. The stent expanded well, and we confirmed good patency visually. The blockage was significantly reduced from 78% down to about 21%.",
            9: "Indication: Malignant central airway obstruction. Pre-procedure blockage: ~78% Trachea. PROCEDURE: Under general anesthesia with jet ventilation, rigid bronchoscopy conducted. Sequential balloon expansion of trachea stenosis conducted. Airway gauged and Dumon Y-Stent Y-Stent prosthesis (20x40mm) inserted in Trachea. Stent location verified with good dilation and openness. Post-procedure blockage: ~21%. No adverse events. EBL minimal."
        },
        2: { # Baker, Kenneth (Debulking LMS)
            1: "Dx: LMS tumor.\nProc: Rigid bronch.\nAction: Mech debulking (forceps/coring). Balloon dilation.\nFindings: 72% -> 16% obstruction.\nEBL: 200mL. Controlled.\nPlan: ICU.",
            2: "PROCEDURE NOTE: This 64-year-old male with malignant central airway obstruction underwent therapeutic rigid bronchoscopy. The left mainstem (LMS) bronchus was identified as the site of a 72% obstruction caused by endobronchial tumor. Mechanical debulking was performed using the rigid scope and biopsy forceps to core out the lesion. Following tumor removal, balloon dilation was utilized to address residual stenosis. Final inspection revealed a patent airway with only 16% residual obstruction. Hemostasis was secured after approximately 200mL EBL.",
            3: "CPT Coding Rationale:\n- 31641 (Bronchoscopy with destruction of tumor/relief of stenosis): Mechanical debulking and balloon dilation performed to relieve severe LMS obstruction.\n- Note: High complexity procedure due to location and bleeding management (EBL 200mL).",
            4: "Resident Procedure Note\nPt: K. Baker\nSite: LMS\nProcedure:\n1. Rigid bronchoscopy.\n2. Identified tumor at LMS.\n3. Mechanical debulking (multiple passes).\n4. Balloon dilation.\n5. Hemostasis achieved (EBL 200mL).\n6. Specimen to path.\nPlan: ICU admission.",
            5: "mr baker had a tumor in the left mainstem blocking about 72 percent we went in with the rigid scope general anesthesia used the scope to core out the tumor and forceps to grab the pieces then dilated with a balloon looks much better now maybe 16 percent obstruction bled about 200cc but it stopped samples sent to lab.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at LMS Rigid bronchoscopy mechanical debulking performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Balloon dilation performed for residual stenosis Post procedure 16 percent residual obstruction EBL 200mL Hemostasis achieved Specimens sent for histology",
            7: "[Indication]\nMalignant central airway obstruction (LMS).\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Mechanical debulking of LMS tumor. Balloon dilation of residual stenosis. Obstruction reduced from 72% to 16%.\n[Plan]\nICU Observation. Oncology follow-up.",
            8: "Mr. Baker was brought to the suite for management of a malignant obstruction in his left mainstem bronchus. Under general anesthesia, we used a rigid bronchoscope to mechanically debulk the tumor, effectively coring it out. We followed this with balloon dilation to maximize the airway diameter. The procedure was successful, reducing the obstruction from 72% to 16%, and bleeding was controlled before the end of the case.",
            9: "Indication: Malignant central airway obstruction. Pre-procedure: ~72% blockage at LMS. PROCEDURE: Under general anesthesia, rigid bronchoscopy conducted. Endobronchial neoplasm spotted at LMS. Rigid bronchoscopy mechanical resection conducted with sequential tumor extraction. Multiple passes conducted to achieve maximal reduction. Balloon expansion conducted for residual narrowing. Post-procedure: ~16% residual blockage. EBL: ~200mL. Hemostasis secured. Samples dispatched for histology."
        },
        3: { # Green, Margaret (Stent RMS)
            1: "Indication: RCC met to RMS.\nProc: Rigid bronch, balloon dilation, stent.\nDevice: Ultraflex Covered (18x30mm).\nResult: 89% -> 25% obstruction.\nPlan: Floor obs.",
            2: "OPERATIVE SUMMARY: The patient, a 78-year-old female with metastatic renal cell carcinoma, presented with near-total occlusion (89%) of the right mainstem (RMS) bronchus. Under general anesthesia, rigid bronchoscopy was performed. The stenosis was initially managed with sequential balloon dilation. To maintain patency, an Ultraflex Self-Expanding Metallic Stent (SEMS), covered, 18x30mm, was deployed. Post-deployment imaging confirmed excellent expansion and reduction of obstruction to approximately 25%.",
            3: "Billing: 31641 (Destruction/Relief of Stenosis) - *Note: Registry code mismatch, verify if 31636 (Stent) is preferred. Note text describes stent placement.*\nProcedure performed: Placement of bronchial stent (Ultraflex 18x30mm) in Right Mainstem.\nGuidance: Rigid bronchoscopy.\nPre-stent work: Balloon dilation.",
            4: "Procedure: RMS Stent\nAttending: Dr. Williams\nFellow: Dr. Liu\nSteps:\n1. Rigid bronchoscopy.\n2. Balloon dilation of RMS.\n3. Sized airway.\n4. Deployed Ultraflex SEMS (18x30mm).\n5. Confirmed position.\nComplications: None.",
            5: "mrs green has that renal cell met in her right mainstem we took her to the or for a stent rigid bronch used dilated it up first then put in an ultraflex covered stent 18 by 30 millimeters opened up nicely obstruction is way down minimal bleeding shes going to the floor for the night.",
            6: "Under general anesthesia with jet ventilation rigid bronchoscopy performed Sequential balloon dilation of RMS stenosis performed Airway measured and Ultraflex SEMS Covered stent 18x30mm deployed in Right mainstem Stent position confirmed with good expansion and patency Post procedure obstruction 25 percent No complications EBL minimal",
            7: "[Indication]\nRenal cell carcinoma metastasis to bronchus (RMS).\n[Anesthesia]\nGeneral, Jet Ventilation.\n[Description]\nRigid bronchoscopy. Balloon dilation. Ultraflex SEMS (Covered, 18x30mm) placed in RMS. Patency improved.\n[Plan]\nOvernight observation. Repeat bronch in 4-6 weeks.",
            8: "Due to a metastasis from renal cell carcinoma, Ms. Green had an 89% obstruction of her right mainstem bronchus. We performed a rigid bronchoscopy under general anesthesia. First, we used a balloon to dilate the narrowed area. Then, we deployed an Ultraflex covered SEMS (18x30mm) to keep the airway open. The stent expanded well, and the obstruction was reduced to 25%. She tolerated the procedure well.",
            9: "Indication: Renal cell carcinoma metastasis to bronchus. Pre-procedure blockage: ~89% Right mainstem. PROCEDURE: Under general anesthesia with jet ventilation, rigid bronchoscopy conducted. Sequential balloon expansion of RMS narrowing conducted. Airway gauged and Ultraflex SEMS - Covered prosthesis (18x30mm) inserted in Right mainstem. Stent location verified with good dilation and openness. Post-procedure blockage: ~25%. No adverse events. EBL minimal."
        },
        4: { # Green, Kenneth (Debulking RLL)
            1: "Dx: Thyroid CA tracheal compression/RLL tumor.\nProc: Rigid bronch.\nAction: APC tumor removal RLL. Laser ablation base.\nResult: 80% -> 24% obstruction.\nEBL: 200mL.\nPlan: ICU.",
            2: "PROCEDURE NOTE: The patient, Mr. Green, with a history of thyroid cancer, presented with airway compromise. Rigid bronchoscopy revealed an endobronchial tumor obstructing the Right Lower Lobe (RLL) orifice by approximately 80%. Argon Plasma Coagulation (APC) was utilized to devitalize and remove the tumor sequentially. Laser ablation was subsequently employed to address the tumor base and ensure hemostasis. Post-procedure, the airway caliber was significantly improved with only 24% residual obstruction.",
            3: "Codes:\n- 31640: Excision of tumor (APC/mechanical removal).\n- 31641: Destruction of tumor (Additional laser ablation).\nSite: RLL orifice.\nMethod: Rigid bronchoscopy with APC and Laser.",
            4: "Procedure: RLL Debulking\nPt: K. Green\nSteps:\n1. General anesthesia.\n2. Rigid bronchoscopy.\n3. Identified tumor RLL.\n4. APC used for debulking.\n5. Laser used for base ablation.\n6. Suctioned debris.\nResult: Improved aeration.",
            5: "mr green has thyroid cancer invading the airway we found a tumor at the rll orifice blocking 80 percent used apc to burn it and remove it then laser to clean up the base bleeding was moderate about 200cc but controlled airway looks much better now sending to icu.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at RLL orifice Apc argon plasma coagulation performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Additional APC laser used for hemostasis and tumor base ablation Post procedure 24 percent residual obstruction EBL 200mL Hemostasis achieved Specimens sent for histology",
            7: "[Indication]\nThyroid cancer with tracheal compression/RLL tumor.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. APC used for tumor removal at RLL. Laser used for base ablation. Obstruction reduced 80% to 24%.\n[Plan]\nICU admit. Oncology follow-up.",
            8: "Mr. Green underwent rigid bronchoscopy for an endobronchial tumor at the right lower lobe orifice associated with his thyroid cancer. We used Argon Plasma Coagulation (APC) to debulk the tumor in a sequential manner. Additional laser therapy was applied to the tumor base for ablation and hemostasis. We successfully achieved a patent airway, reducing the obstruction from 80% to 24%, with hemostasis achieved after 200mL of blood loss.",
            9: "Indication: Thyroid cancer with tracheal compression. Pre-procedure: ~80% blockage at RLL orifice. PROCEDURE: Under general anesthesia, rigid bronchoscopy conducted. Endobronchial neoplasm spotted at RLL orifice. Apc (argon plasma coagulation) conducted with sequential tumor extraction. Multiple passes conducted to achieve maximal reduction. Additional APC/laser utilized for coagulation and tumor base destruction. Post-procedure: ~24% residual blockage. EBL: ~200mL. Hemostasis secured. Samples dispatched for histology."
        },
        5: { # Jones, Ronald (Stent Trachea)
            1: "Indication: Esophageal CA, tracheal invasion.\nProc: Rigid bronch.\nAction: Balloon dilation. Novatech Silicone Stent (20x50mm) placed.\nResult: 85% -> 7%.\nPlan: Admit.",
            2: "OPERATIVE REPORT: Mr. Jones, a 73-year-old male with esophageal carcinoma complicated by tracheal invasion, underwent palliative bronchoscopy. Under general anesthesia with jet ventilation, the trachea was assessed via rigid bronchoscope. High-grade stenosis (85%) was noted. Sequential balloon dilation was performed. A Novatech Silicone (Dumon style) stent, measuring 20x50mm, was successfully deployed. Verification showed excellent stent expansion and marked improvement in airway patency to 93%.",
            3: "CPT Justification:\n- 31631 (Placement of Tracheal Stent): Novatech Silicone 20x50mm placed in trachea.\n- 31630 (Tracheal Dilation): Balloon dilation performed prior to stent placement (often bundled, but documented here as distinct steps).",
            4: "Resident Note:\nProcedure: Tracheal Stent\nSteps:\n1. Rigid bronchoscopy initiated.\n2. 85% stenosis identified in trachea.\n3. Balloon dilation performed.\n4. Stent (Novatech 20x50mm) deployed.\n5. Position checked.\nPatient stable.",
            5: "ronald has esophageal cancer growing into his trachea really tight 85 percent blocked we did a rigid bronch dilated it with a balloon then put in a novatech silicone stent 20 by 50 millimeter looks great wide open now minimal bleeding admit to floor.",
            6: "Under general anesthesia with jet ventilation rigid bronchoscopy performed Sequential balloon dilation of trachea stenosis performed Airway measured and Novatech Silicone Dumon stent 20x50mm deployed in Trachea Stent position confirmed with good expansion and patency Post procedure obstruction 7 percent No complications EBL minimal",
            7: "[Indication]\nEsophageal cancer with tracheal invasion.\n[Anesthesia]\nGeneral, Jet Ventilation.\n[Description]\nRigid bronchoscopy. Balloon dilation of trachea. Novatech Silicone Stent (20x50mm) deployed. Obstruction reduced to 7%.\n[Plan]\nObservation overnight. F/U 4-6 weeks.",
            8: "We treated Mr. Jones for tracheal invasion from his esophageal cancer. Using a rigid bronchoscope and jet ventilation, we first dilated the severe stenosis in his trachea. We then placed a Novatech Silicone Dumon stent (20x50mm). The stent seated perfectly, and the airway, which was 85% blocked, is now almost completely open. He is recovering well.",
            9: "Indication: Esophageal cancer with tracheal invasion. Pre-procedure blockage: ~85% Trachea. PROCEDURE: Under general anesthesia with jet ventilation, rigid bronchoscopy conducted. Sequential balloon expansion of trachea stenosis conducted. Airway gauged and Novatech Silicone - Dumon prosthesis (20x50mm) inserted in Trachea. Stent location verified with good dilation and openness. Post-procedure blockage: ~7%. No adverse events. EBL minimal."
        },
        6: { # Baker, Nicholas (Debulking BI)
            1: "Dx: Malignant CAO (BI).\nProc: Rigid bronch.\nAction: Mechanical debulking. APC/Laser ablation.\nResult: 76% -> 19% obstruction.\nPlan: ICU.",
            2: "PROCEDURE NOTE: Mr. Baker presented for management of malignant central airway obstruction. Rigid bronchoscopy was performed under general anesthesia. The Bronchus Intermedius (BI) demonstrated 76% occlusion by tumor. Mechanical debulking was achieved via the rigid scope and forceps. Following bulk removal, the tumor base was treated with APC and laser to ensure hemostasis and destroy residual cells. The airway was restored to approximately 81% patency.",
            3: "Coding: 31640 (Tumor Excision) + 31641 (Tumor Destruction).\nLocation: Bronchus Intermedius.\nTools: Rigid scope, Forceps (Excision), APC/Laser (Destruction).\nOutcome: Significant improvement in airway caliber.",
            4: "Procedure: BI Tumor Debulking\nPt: N. Baker\nSteps:\n1. GA induced.\n2. Rigid bronchoscopy.\n3. Tumor visualized at BI.\n4. Mechanical removal (forceps).\n5. APC/Laser applied.\n6. Hemostasis confirmed.\nPlan: ICU.",
            5: "nicholas baker here for tumor debulking in the bi rigid scope used general anesthesia scraped out the tumor with the scope and forceps then burned the base with apc and laser bleeding was mild about 75cc airway looks much better sending him to icu.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at BI Rigid bronchoscopy mechanical debulking performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Additional APC laser used for hemostasis and tumor base ablation Post procedure 19 percent residual obstruction EBL 75mL Hemostasis achieved Specimens sent for histology",
            7: "[Indication]\nMalignant central airway obstruction (BI).\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Mechanical debulking of BI tumor. APC/Laser ablation. Obstruction reduced 76% to 19%.\n[Plan]\nICU Observation. Consider stent if re-obstruction.",
            8: "Mr. Baker underwent rigid bronchoscopy to remove a tumor blocking his bronchus intermedius. We mechanically removed the bulk of the tumor using forceps and the rigid scope itself. We then used APC and laser to treat the remaining tumor tissue and control bleeding. The obstruction was reduced from 76% to 19%, and hemostasis was secured.",
            9: "Indication: Malignant central airway obstruction. Pre-procedure: ~76% blockage at BI. PROCEDURE: Under general anesthesia, rigid bronchoscopy conducted. Endobronchial neoplasm spotted at BI. Rigid bronchoscopy mechanical resection conducted with sequential tumor extraction. Multiple passes conducted to achieve maximal reduction. Additional APC/laser utilized for coagulation and tumor base destruction. Post-procedure: ~19% residual blockage. EBL: ~75mL. Hemostasis secured. Samples dispatched for histology."
        },
        7: { # Adams, Ashley (Stent RMS)
            1: "Indication: Esophageal CA invading RMS.\nProc: Rigid bronch.\nAction: Balloon dilation. Ultraflex Stent (16x50mm).\nResult: 89% -> 11%.\nPlan: Floor obs.",
            2: "OPERATIVE SUMMARY: Ms. Adams, with a history of esophageal cancer and tracheal invasion affecting the right mainstem (RMS), underwent intervention. Rigid bronchoscopy was utilized. The RMS stenosis (89%) was dilated with a balloon. Subsequently, an Ultraflex Covered SEMS (16x50mm) was deployed. The stent expanded appropriately, reducing the obstruction to 11%. No complications were noted.",
            3: "Codes:\n- 31636 (Bronchial Stent Placement): Ultraflex 16x50mm in RMS.\n- 31630 (Dilation): Balloon dilation of stenosis.\nContext: Palliation of malignant airway obstruction.",
            4: "Procedure: RMS Stent\nPatient: A. Adams\nSteps:\n1. Rigid bronchoscopy.\n2. Dilation of RMS stenosis.\n3. Deployment of Ultraflex SEMS 16x50mm.\n4. Confirmation of patency.\nPatient tolerated well.",
            5: "ms adams has esophageal cancer pushing into the right mainstem we did a rigid bronch dilated the narrowing then put in an ultraflex covered stent 16 by 50 looks good now airway is open bleeding minimal admitting for observation.",
            6: "Under general anesthesia with jet ventilation rigid bronchoscopy performed Sequential balloon dilation of RMS stenosis performed Airway measured and Ultraflex SEMS Covered stent 16x50mm deployed in Right mainstem Stent position confirmed with good expansion and patency Post procedure obstruction 11 percent No complications EBL minimal",
            7: "[Indication]\nEsophageal cancer with tracheal invasion (RMS).\n[Anesthesia]\nGeneral, Jet Ventilation.\n[Description]\nRigid bronchoscopy. Balloon dilation. Ultraflex SEMS (16x50mm) deployed in RMS. Obstruction reduced 89% to 11%.\n[Plan]\nAdmit to floor. Follow up 4-6 weeks.",
            8: "We performed a bronchoscopy on Ms. Adams to relieve the obstruction in her right mainstem bronchus caused by invasive esophageal cancer. Using a rigid scope and jet ventilation, we dilated the stricture and then placed a covered Ultraflex stent (16x50mm). The stent opened the airway significantly, reducing the blockage from 89% to 11%.",
            9: "Indication: Esophageal cancer with tracheal invasion. Pre-procedure blockage: ~89% Right mainstem. PROCEDURE: Under general anesthesia with jet ventilation, rigid bronchoscopy conducted. Sequential balloon expansion of RMS narrowing conducted. Airway gauged and Ultraflex SEMS - Covered prosthesis (16x50mm) inserted in Right mainstem. Stent location verified with good dilation and openness. Post-procedure blockage: ~11%. No adverse events. EBL minimal."
        },
        8: { # Lewis, Melissa (Debulking RMS)
            1: "Dx: Metastatic lung CA (RMS).\nProc: Rigid bronch.\nAction: Forceps debulking.\nResult: 76% -> 30%.\nPlan: ICU.",
            2: "PROCEDURE NOTE: This 75-year-old female with metastatic lung cancer presented with RMS obstruction. Rigid bronchoscopy was performed. An endobronchial tumor was identified in the Right Mainstem. Mechanical debulking was carried out using biopsy forceps in a sequential manner. Multiple passes achieved a reduction in obstruction from 76% to 30%. Hemostasis was achieved.",
            3: "Coding: 31640 (Bronchoscopy with tumor excision).\nMethod: Rigid bronchoscopy with forceps.\nLocation: Right Mainstem Bronchus.\nOutcome: Partial restoration of airway patency.",
            4: "Procedure: RMS Debulking\nPt: M. Lewis\nSteps:\n1. Rigid bronchoscopy.\n2. Tumor visualized in RMS.\n3. Forceps debulking performed.\n4. Hemostasis secured.\n5. Specimens to path.\nPlan: ICU.",
            5: "mrs lewis has metastatic lung cancer blocking the right mainstem we went in with the rigid scope and used the big forceps to pull out the tumor chunks cleared it out pretty well from 76 percent down to 30 percent bleeding stopped fine sending to icu.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at RMS Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Post procedure 30 percent residual obstruction EBL 75mL Hemostasis achieved Specimens sent for histology",
            7: "[Indication]\nMetastatic lung cancer with bronchial obstruction (RMS).\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Forceps debulking of RMS tumor. Obstruction reduced 76% to 30%.\n[Plan]\nICU observation. Oncology follow-up.",
            8: "Ms. Lewis underwent rigid bronchoscopy for a tumor obstructing her right mainstem bronchus. We identified the lesion and used biopsy forceps to manually debulk the tumor. After several passes, we managed to reduce the obstruction significantly, improving the airway diameter. Hemostasis was excellent.",
            9: "Indication: Metastatic lung cancer with bronchial obstruction. Pre-procedure: ~76% blockage at RMS. PROCEDURE: Under general anesthesia, rigid bronchoscopy conducted. Endobronchial neoplasm spotted at RMS. Rigid bronchoscopy resection with biopsy forceps conducted with sequential tumor extraction. Multiple passes conducted to achieve maximal reduction. Post-procedure: ~30% residual blockage. EBL: ~75mL. Hemostasis secured. Samples dispatched for histology."
        },
        9: { # Jackson, Nancy (Debulking Distal Trachea)
            1: "Dx: SCC airway compromise.\nProc: Rigid bronch.\nAction: Mech debulking distal trachea. APC/Laser.\nResult: 76% -> 39%.\nPlan: ICU.",
            2: "OPERATIVE REPORT: Ms. Jackson presented with squamous cell carcinoma causing distal tracheal obstruction. Rigid bronchoscopy was performed under general anesthesia. The tumor was identified and mechanically debulked using the rigid scope and forceps. Additional thermal ablation (APC/Laser) was applied for tumor base destruction and hemostasis. The obstruction was reduced to 39%.",
            3: "Codes: 31640 (Excision), 31641 (Destruction).\nSite: Distal Trachea.\nTechnique: Mechanical removal followed by Laser/APC ablation.",
            4: "Procedure: Tracheal Debulking\nPt: N. Jackson\nSteps:\n1. GA/Rigid bronch.\n2. Tumor in distal trachea.\n3. Mechanical debulking.\n4. APC/Laser for base.\n5. Hemostasis.\nPlan: ICU.",
            5: "nancy has squamous cell cancer blocking the lower trachea we used the rigid scope to clean it out scraped it and used forceps then laser and apc to burn the rest bleeding was about 150cc but stopped airway is better now.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at distal trachea Rigid bronchoscopy mechanical debulking performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Additional APC laser used for hemostasis and tumor base ablation Post procedure 39 percent residual obstruction EBL 150mL Hemostasis achieved Specimens sent for histology",
            7: "[Indication]\nSquamous cell carcinoma with airway compromise.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Mechanical debulking distal trachea. APC/Laser ablation. Obstruction reduced 76% to 39%.\n[Plan]\nICU observation.",
            8: "Ms. Jackson underwent a rigid bronchoscopy to treat a squamous cell carcinoma obstructing her distal trachea. We mechanically removed the tumor using the scope and forceps, followed by APC and laser to treat the base and stop bleeding. We achieved a reduction in obstruction to 39%.",
            9: "Indication: Squamous cell carcinoma with airway compromise. Pre-procedure: ~76% blockage at distal trachea. PROCEDURE: Under general anesthesia, rigid bronchoscopy conducted. Endobronchial neoplasm spotted at distal trachea. Rigid bronchoscopy mechanical resection conducted with sequential tumor extraction. Multiple passes conducted to achieve maximal reduction. Additional APC/laser utilized for coagulation and tumor base destruction. Post-procedure: ~39% residual blockage. EBL: ~150mL. Hemostasis secured. Samples dispatched for histology."
        }
    }
    return variations

def get_base_data_mocks():
    return [
        {"idx": 0, "orig_name": "Jackson, John", "orig_age": 51, "names": ["John Smith", "Robert Johnson", "Michael Williams", "David Brown", "Richard Jones", "Charles Garcia", "Joseph Miller", "Thomas Davis", "Christopher Rodriguez"]},
        {"idx": 1, "orig_name": "Wilson, William", "orig_age": 52, "names": ["William Martinez", "Daniel Hernandez", "Paul Lopez", "Mark Gonzalez", "Donald Wilson", "George Anderson", "Kenneth Thomas", "Steven Taylor", "Edward Moore"]},
        {"idx": 2, "orig_name": "Baker, Kenneth", "orig_age": 64, "names": ["Kenneth Jackson", "Brian Martin", "Ronald Lee", "Anthony Perez", "Kevin Thompson", "Jason White", "Matthew Harris", "Gary Sanchez", "Timothy Clark"]},
        {"idx": 3, "orig_name": "Green, Margaret", "orig_age": 78, "names": ["Margaret Ramirez", "Lisa Lewis", "Nancy Robinson", "Karen Walker", "Betty Young", "Helen Allen", "Sandra King", "Donna Wright", "Carol Scott"]},
        {"idx": 4, "orig_name": "Green, Kenneth", "orig_age": 54, "names": ["Kenneth Torres", "Larry Nguyen", "Scott Hill", "Frank Flores", "Stephen Green", "Eric Adams", "Andrew Nelson", "Raymond Baker", "Gregory Hall"]},
        {"idx": 5, "orig_name": "Jones, Ronald", "orig_age": 73, "names": ["Ronald Rivera", "Joshua Campbell", "Jerry Mitchell", "Dennis Carter", "Walter Roberts", "Patrick Gomez", "Peter Phillips", "Harold Evans", "Douglas Turner"]},
        {"idx": 6, "orig_name": "Baker, Nicholas", "orig_age": 54, "names": ["Nicholas Diaz", "Henry Parker", "Carl Cruz", "Arthur Edwards", "Ryan Collins", "Roger Reyes", "Joe Stewart", "Juan Morris", "Jack Morales"]},
        {"idx": 7, "orig_name": "Adams, Ashley", "orig_age": 66, "names": ["Ashley Murphy", "Sarah Cook", "Kimberly Rogers", "Deborah Morgan", "Jessica Cooper", "Shirley Peterson", "Cynthia Bailey", "Angela Reed", "Melissa Kelly"]},
        {"idx": 8, "orig_name": "Lewis, Melissa", "orig_age": 75, "names": ["Melissa Howard", "Brenda Ward", "Amy Cox", "Anna Richardson", "Rebecca Wood", "Virginia Watson", "Kathleen Brooks", "Pamela Bennett", "Martha Gray"]},
        {"idx": 9, "orig_name": "Jackson, Nancy", "orig_age": 70, "names": ["Nancy James", "Debra Mendoza", "Amanda Fortin", "Stephanie Price", "Carolyn Hughes", "Christine Sanders", "Marie Myers", "Janet Ross", "Catherine Foster"]}
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
            break
            
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
    output_filename = output_dir / "synthetic_debulking_stent_notes_part_055.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()