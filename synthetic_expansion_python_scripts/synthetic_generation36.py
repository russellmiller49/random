import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_036.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Maria Rodriguez (EBV LLL)
            1: "Procedure: Bronchoscopy w/ EBV.\nIndication: LLL Emphysema.\nAction: Airway inspected. LLL target. \nIntervention: Placed 3 Zephyr valves (LB6, LB8, LB9-10). \nResult: Good seal. Complete occlusion.\nPlan: CXR, Admit.",
            2: "HISTORY: The patient, a 72-year-old female with severe heterogeneous emphysema predominantly affecting the left lower lobe, presented for bronchoscopic lung volume reduction.\nPROCEDURE: Under moderate sedation, the flexible bronchoscope was introduced. The upper airways were unremarkable. Upon inspection of the LLL, severe emphysematous changes were noted. Endobronchial valves were deployed into the target segments: LB6 (4.0mm), LB8 (4.0mm), and LB9-10 (5.5mm). \nOUTCOME: Complete lobar occlusion was visually confirmed with excellent valve seating. There were no immediate complications.",
            3: "Service: Bronchoscopy with placement of bronchial valves (31647).\nTarget: Left Lower Lobe (Initial Lobe).\nTechnique: Flexible bronchoscope inserted. Target segments LB6, LB8, and LB9-10 identified. Delivery catheter used to place 4.0mm and 5.5mm valves. \nVerification: Complete occlusion verified visually. \nMedical Necessity: Treatment of severe heterogeneous emphysema.",
            4: "Procedure Note\nAttending: Dr. Park\nResident: [Name]\nPatient: Maria Rodriguez\nProcedure Steps:\n1. Moderate sedation induced.\n2. Scope inserted via oral route.\n3. Anatomy reviewed; LLL targeted.\n4. Valves placed in LB6, LB8, LB9-10.\n5. Good seal confirmed.\nPlan: Admit for observation.",
            5: "procedure note ebv placement patient maria rodriguez 72yo we did the bronch today for the emphysema lll mainly. used moderate sedation versed fentanyl. went in normal upper airways lll looked bad emphysema. put valves in lb6 lb8 and the 9-10 segment. 4.0 and 5.5 sizes. looks like a good seal occlusion is complete no issues. chest xray next and admit thanks.",
            6: "The patient, a 72-year-old female with severe heterogeneous emphysema, underwent flexible bronchoscopy with EBV placement. Moderate sedation was used. Access was oropharyngeal. Findings included normal upper airways and severe emphysematous changes in the LLL. Interventions consisted of placing a 4.0mm EBV in LB6, a 4.0mm EBV in LB8, and a 5.5mm EBV in LB9-10. All showed a good seal. The outcome was successful complete LLL occlusion with no complications. Post-op plan includes CXR and admission for observation.",
            7: "[Indication]\nSevere heterogeneous emphysema, LLL predominant.\n[Anesthesia]\nModerate (Versed/Fentanyl).\n[Description]\nFB performed. LLL targeted. Valves placed in LB6, LB8, LB9-10. Good seal and complete occlusion achieved.\n[Plan]\nCXR, admit for observation.",
            8: "We brought Ms. Rodriguez to the procedure room for her scheduled valve placement. After achieving moderate sedation, we advanced the bronchoscope. The left lower lobe showed significant disease. We proceeded to place valves in the LB6, LB8, and LB9-10 segments. We were able to confirm a good seal on all valves, resulting in complete occlusion of the lobe. She tolerated the procedure well.",
            9: "Operation: FB with EBV implantation.\nDx: Severe heterogeneous emphysema.\nFindings: LLL severe changes.\nActions: Implantation of 4.0mm EBV in LB6, 4.0mm in LB8, and 5.5mm in LB9-10. Complete obstruction achieved.\nResult: Successful LLL isolation, no adverse events."
        },
        1: { # Emma Carlisle (Rigid Bronch Stent)
            1: "Dx: Extrinsic tracheal compression.\nProc: Rigid bronch, Y-stent.\nActions:\n- Flex bronch: 90% obstruction mid-trachea.\n- Rigid inserted.\n- Silicone Y-stent (16x13x13) customized and deployed.\n- Position confirmed.\n- Obstruction resolved.\nPlan: ICU, CXR.",
            2: "OPERATIVE REPORT: The patient presented with respiratory failure secondary to severe extrinsic tracheal compression. \nPROCEDURE: General anesthesia was induced. Initial flexible inspection revealed 90% tracheal stenosis. A 14mm rigid ventilating bronchoscope was utilized to secure the airway. A silicone Y-stent was customized (75mm tracheal limb, 15mm/30mm bronchial limbs) and deployed into the left mainstem and trachea. \nCONCLUSION: Significant restoration of airway patency was achieved immediately post-deployment.",
            3: "CPT Coding Data:\n- 31631 (Stent Placement): Silicone Y-stent deployed via rigid bronchoscopy.\n- 31630 (Dilation): Rigid barrel used to dilate tracheal stenosis prior to stenting.\n- 31622 (Diagnostic): Initial airway survey performed.\nTechnique: Rigid bronchoscopy used for visualization and deployment. Stent customized to measure.",
            4: "Procedure: Rigid Bronchoscopy & Stenting\nAttending: Dr. Miller\nSteps:\n1. GA induced.\n2. Flex scope check: 90% obstruction.\n3. Rigid scope inserted.\n4. ETT removed.\n5. Silicone Y-stent sized and placed.\n6. Airways inspected; good position.\n7. LMA placed for wake-up.\nPlan: ICU transfer.",
            5: "patient emma carlisle here for the airway compression severe. we did a rigid bronch today. started with flexible saw about 90 percent blockage in the trachea. took the tube out put the rigid scope in. measured for a y stent silicone one. cut it to fit and put it in. looks way better now airway is open. checked for bleeding none seen. sent to icu.",
            6: "Patient Emma Carlisle underwent Rigid bronchoscopy, Silicone Y-stent placement, and bronchoscopic intubation for Respiratory failure secondary to extrinsic tracheal compression. Under General Anesthesia, inflammation and 90% obstruction were visualized in the mid trachea. A 14 mm rigid bronchoscope was inserted. A customized 16x13x13 silicone Y-stent was deployed. Inspection showed the stent well placed with near complete resolution of obstruction. Recommendations include Transfer to ICU and TID hypertonic nebulizers.",
            7: "[Indication]\nSevere extrinsic tracheal compression, respiratory failure.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nRigid bronchoscopy performed. 90% tracheal obstruction noted. Silicone Y-stent customized and deployed. Airway stabilized and patent.\n[Plan]\nICU admission, Post-proc CXR, Nebulizers.",
            8: "Ms. Carlisle was brought to the OR for management of her severe tracheal compression. We started with a flexible scope which confirmed a critical 90% blockage. We then switched to the rigid bronchoscope for better control. We measured and cut a silicone Y-stent to fit her specific anatomy and deployed it successfully. The airway looked much better immediately, with the obstruction largely resolved.",
            9: "Procedure: Rigid bronchoscopy with Silicone Y-stent positioning.\nIndication: Severe extrinsic tracheal constriction.\nAction: The rigid apparatus was inserted. A Y-stent was tailored and installed. The rigid forceps and flexible tip were used to situate the limbs. \nOutcome: Successful stabilization of the airway."
        },
        2: { # Nolan Shepherd (Rigid Bronch Tumor Ablation)
            1: "Indication: Tracheal Obstruction (Tumor).\nProc: Rigid Bronch, Tumor Ablation.\nFindings: 3 polypoid lesions, 90% block. Multiple small lesions.\nActions:\n- Snare resection of large polyps.\n- APC used on base/residue.\n- 90% patency achieved.\nPlan: Ward, Oncology consult.",
            2: "OPERATIVE NARRATIVE: The patient presented with endotracheal tumor causing significant obstruction. Under general anesthesia, a rigid bronchoscopy was performed. Three large polypoid lesions causing ball-valve obstruction were identified. These were resected utilizing electrocautery snare. The remaining tumor burden and base were treated with Argon Plasma Coagulation (APC) to achieve hemostasis and further debulking. Luminal recanalization was successful, restoring approximately 90% patency.",
            3: "Procedure Code: 31641 (Tumor Destruction).\nMethod: Rigid bronchoscopy with APC and Electrocautery Snare.\nDetails: Destruction of intrinsic tracheal tumor causing 90% obstruction. \nOutcome: Relief of stenosis achieved. Stent (31631) considered but not performed per patient preference.",
            4: "Resident Note: Tumor Debulking\nAttending: Dr. Winslow\nSteps:\n1. LMA/GA.\n2. Flex scope: 90% block by polypoid lesions.\n3. Rigid scope inserted.\n4. Snare used to cut large polyps.\n5. APC used to clean up the rest.\n6. Airway open at end.\nPlan: Observe on ward.",
            5: "nolan shepherd here for the tracheal tumor. 90 percent blocked breathing hard. we did the rigid bronch. used the snare to chop off the big polyps and then the apc to burn the rest. opened it up nicely about 90 percent open now. patient didn't want a stent so we didnt put one in. watch for recurrence.",
            6: "Patient Nolan Shepherd underwent Rigid bronchoscopy with endoluminal tumor ablation for Tracheal Obstruction. Under General Anesthesia, 3 polypoid lesions were found blocking 90% of the airway. A 10mm rigid tracheoscope was inserted. The electrocautery snare was used to transect the lesions. APC was used to paint and shave the remaining tumor area. The trachea was approximately 90% open at the end. Stent placement was discussed but declined by the patient.",
            7: "[Indication]\nTracheal Obstruction, Endotracheal tumor.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nRigid bronchoscopy. Snare resection of polypoid lesions. APC ablation of base. 90% recanalization achieved.\n[Plan]\nWard admission, Oncology consult, Path results.",
            8: "We took Mr. Shepherd back for debulking of his tracheal tumor. The blockage was severe, about 90%. We used the rigid scope to access the tumor and then removed the bulk of it using a snare. We finished up with APC to handle the smaller lesions and control bleeding. The airway looks much better now. We decided against a stent for now based on his preference.",
            9: "Procedure: Rigid bronchoscopy with endoluminal tumor destruction.\nDiagnosis: Endotracheal neoplasm.\nTechnique: Electrocautery snare was utilized to sever the polypoid masses. APC was employed to incinerate the residual tumor. \nResult: Adequate luminal restoration attained."
        },
        3: { # Thomas O'Brien (BLVR LUL)
            1: "Indication: Severe LUL emphysema.\nProc: FB, BLVR.\nActions:\n- Chartis: CV negative.\n- 4 Zephyr valves placed (LB1+2, LB3, lingula).\n- Occlusion confirmed.\nPlan: Admit, CXR.",
            2: "PROCEDURE NOTE: This 70-year-old male with severe emphysema underwent bronchoscopic lung volume reduction. \nFINDINGS: The left upper lobe was identified as the target. Chartis assessment confirmed the absence of collateral ventilation (CV Negative). \nINTERVENTION: Four endobronchial valves were deployed into the LUL segments (LB1+2, LB3, Lingula). Complete lobar occlusion was verified visually. \nDISPOSITION: The patient is stable and admitted for pneumothorax monitoring.",
            3: "Coding: 31647 (Initial Lobe Valve Placement) + 31634 (Balloon Occlusion Test).\nLocation: Left Upper Lobe.\nDetails: Chartis system used to measure flow/CV status. Four valves deployed. \nDiagnosis: Severe Emphysema.",
            4: "Procedure: BLVR\nPatient: Thomas O'Brien\nSteps:\n1. Mod sedation.\n2. Airway inspection.\n3. Chartis check of LUL: Negative.\n4. Placed 4 valves in LUL.\n5. Checked for leaks: None.\nPlan: Admit.",
            5: "doing the valve procedure for mr obrien today. lul emphysema. chartis was negative so we went ahead. put in 4 zephyr valves in the upper lobe segments. sealed up good. patient is stable going to admit him check for pneumo.",
            6: "BLVR PROCEDURE 10/29/2024. Patient Thomas O'Brien with severe LUL emphysema. Chartis (-) CV in LUL. Candidate for EBV placement. Procedure included FB under mod sedation, LUL visualization, and placement of 4 Zephyr valves (LB1+2, LB3, lingula). Complete occlusion confirmed. Disposition: Admit, stable.",
            7: "[Indication]\nSevere LUL emphysema.\n[Anesthesia]\nModerate sedation.\n[Description]\nChartis assessment negative for CV. 4 Zephyr valves placed in LUL. Occlusion confirmed.\n[Plan]\nAdmit, CXR.",
            8: "We performed a lung volume reduction on Mr. O'Brien today. We targeted the left upper lobe. First, we checked for collateral ventilation using the Chartis balloon, which was negative. Then we placed four valves into the LUL airways. Everything looks sealed off perfectly. He's heading to recovery now.",
            9: "Operation: FB with EBV positioning.\nSubject: 70M, severe LUL emphysema.\nMethod: Chartis evaluation (-) CV. Four Zephyr valves installed (LB1+2, LB3, lingula).\nOutcome: Complete obstruction corroborated."
        },
        4: { # Logan Pierce (Ion Robotic)
            1: "Indication: RUL Nodule.\nProc: Robotic Bronch (Ion), TBNA, Cryo, BAL.\nFindings: 1.4cm RUL lesion.\nActions:\n- Navigated to lesion.\n- CBCT confirm.\n- TBNA x6, Cryo x5.\n- ROSE: Atypical cells.\n- Chartis LUL: CV negative.\nPlan: D/C, await path.",
            2: "PROCEDURE REPORT: The patient underwent robotic-assisted bronchoscopy for evaluation of a solitary RUL nodule. \nTECHNIQUE: The Ion platform was utilized for navigation to the Anterior Segment of the RUL. Tool-in-lesion was confirmed via Cone Beam CT. Diagnostic sampling included TBNA (21G/23G) and transbronchial cryobiopsy. BAL was also performed. \nADDITIONAL: Chartis assessment of the LUL confirmed absence of collateral ventilation for future BLVR planning.",
            3: "Codes: 31629 (TBNA), 31628 (Biopsy), 31624 (BAL), 31627 (Nav), 31634 (Balloon Test).\nSpecifics: Ion Robotic Navigation used. CBCT verification. Samples obtained via needle and cryoprobe. Separate lobe (LUL) assessed with Chartis for CV status.",
            4: "Resident Note: Robotic Bronch\nPatient: Logan Pierce\nSteps:\n1. GA / ETT.\n2. Ion robot setup and nav to RUL target.\n3. Spin CT confirm.\n4. Biopsies: Needle and Cryo.\n5. BAL performed.\n6. Chartis check on LUL (for COPD).\n7. ROSE: Atypical.\nPlan: Recovery.",
            5: "logan pierce here for the rul nodule. used the ion robot. drove out to the nodule in the rul anterior segment. spin ct showed we were right on it. took a bunch of biopsies needle and cryo. rose said atypical. also did a bal. then checked the left side with chartis for his emphysema looks like no cv there. patient did fine.",
            6: "DATE OF PROCEDURE: 2/11/2025. INDICATION: RUL nodule and COPD. Flexible Therapeutic Bronchoscope and Ion Robotic Bronchoscope used. Navigation to Anterior Segment RUL (RB3). Cone Beam CT confirmed tool placement. TBNA and Transbronchial Cryobiopsy performed. BAL performed. ROSE revealed Atypical cells. Chartis Evaluation of LUL confirmed absence of collateral ventilation. Patient tolerated well.",
            7: "[Indication]\nRUL Nodule, COPD.\n[Anesthesia]\nGeneral Anesthesia.\n[Description]\nIon Robotic nav to RUL. CBCT confirm. TBNA and Cryo samples taken. BAL performed. Chartis assess of LUL (Neg CV).\n[Plan]\nDischarge, await path, f/u for valves.",
            8: "We used the robotic bronchoscope to biopsy Mr. Pierce's lung nodule today. We navigated to the right upper lobe and confirmed our position with a 3D spin scan. We took several needle and cryo biopsies. While we were there, we also washed the area (BAL) and checked his left lung with the Chartis balloon to see if he's a candidate for valves later—looks like he is.",
            9: "Procedure: Robotic bronchoscopy with TBNA and cryobiopsy.\nTarget: RUL mass.\nTechnique: Ion platform navigation. CBCT verification. Sampling via aspiration and cryoprobe. Lavage performed. LUL physiologic assessment (Chartis) conducted.\nResult: Samples submitted, CV status established."
        },
        5: { # Harold Johnson (BLVR + Pneumo)
            1: "Indication: Air leak post-bullectomy.\nProc: EBV placement. Chest Tube.\nEvent: Valve placed RB1 -> Tension Pneumothorax.\nAction: Procedure aborted. 28Fr Chest Tube placed. Stabilized.\nAdd'l: Valve placed RB3 to reduce flow.\nPlan: ICU, Chest tube management.",
            2: "OPERATIVE SUMMARY: The patient underwent bronchoscopy for management of persistent air leak. \nCOMPLICATION: Following deployment of a Zephyr valve in RB1, the patient developed acute tension pneumothorax. \nMANAGEMENT: Emergent needle decompression and tube thoracostomy (32551) were performed. Hemodynamics stabilized. \nREVISION: A second valve was placed in RB3 to mitigate collateral flow. \nSTATUS: Critical care admission required.",
            3: "Codes: 31647 (Valve Placement), 32551 (Tube Thoracostomy).\nNarrative: Flexible bronchoscopy with valve deployment. Intraoperative development of pneumothorax required separate emergent placement of chest tube. Additional valve placed for air leak control.",
            4: "Procedure: EBV & Chest Tube\nPatient: Hal Johnson\nSteps:\n1. Sedation.\n2. Found air leak RB1.\n3. Valve placed.\n4. Patient desatted, tension pneumo.\n5. Chest tube placed stat.\n6. Placed one more valve in RB3.\nPlan: ICU.",
            5: "hal johnson here for the air leak. tried to put a valve in rb1 and he blew a pneumo right away. tension physiology so we put a chest tube in fast. stabilized him. put another valve in rb3 to help seal it. messy case but he is stable now. icu admit.",
            6: "BRONCHOSCOPY REPORT: ENDOBRONCHIAL VALVE PLACEMENT WITH COMPLICATIONS. Indication: Persistent air leak following RUL bullectomy. Procedure: Flexible bronchoscopy with EBV placement. Intervention: Valve in RB1. Complication: Tension pneumothorax. Management: Procedure aborted, Chest tube placed. Additional Valve: RB3. Final Assessment: Partial success, Air leak reduced. Plan: ICU admission.",
            7: "[Indication]\nPersistent air leak.\n[Anesthesia]\nModerate.\n[Description]\nValve placed RB1. Complicated by Tension PTX. Emergent Chest Tube placed. Additional valve in RB3.\n[Plan]\nICU, Water seal.",
            8: "Mr. Johnson had a rough time during the valve placement. We found the leak in the right upper lobe, but right after we put the first valve in, his lung collapsed causing a tension pneumothorax. We had to put a chest tube in immediately to re-expand the lung. Once he was stable, we put one more valve in a different segment to try and slow the leak down. He's going to the ICU.",
            9: "Operation: FB with EBV deployment and Tube Thoracostomy.\nComplication: Iatrogenic pneumothorax.\nAction: Immediate insertion of drainage catheter. Stabilization achieved. Secondary valve implanted in RB3.\nOutcome: Air leak attenuated."
        },
        6: { # Jacob Renfield (Rigid EBUS Debulk)
            1: "Indication: Left mainstem obstruction.\nProc: Rigid Bronch, EBUS, Debulking.\nActions:\n- Rigid scope inserted.\n- EBUS TBNA subcarinal mass (6 passes).\n- LMS tumor debulked (APC, Cryo, Forceps).\n- Balloon dilation LMS.\n- APC for hemostasis.\nPlan: Rad Onc consult.",
            2: "OPERATIVE REPORT: Rigid bronchoscopy was performed for malignant airway obstruction. \nFINDINGS: Left mainstem (LMS) occlusion by tumor. Subcarinal lymphadenopathy. \nPROCEDURE: EBUS-TBNA was performed on the subcarinal station. Mechanical debulking of the LMS tumor was executed using forceps, cryotherapy, and APC. The airway was subsequently dilated with a CRE balloon. \nRESULT: Patency restored to 50%.",
            3: "Codes: 31653 (EBUS 3+ stations/passes?), 31630 (Debulking/Dilation), 31641 (Tumor Destruction).\nNote: Code selection depends on hierarchy. 31652/3 might be applicable depending on node count. Main service is Rigid Bronchoscopy with tumor removal and dilation.",
            4: "Procedure: Rigid Bronch / EBUS / Debulk\nAttending: Dr. Miller\nSteps:\n1. GA / Rigid scope.\n2. EBUS TBNA of subcarinal node.\n3. Debulked left main tumor (APC/Cryo).\n4. Dilated with balloon.\n5. Bleeding controlled.\nPlan: Radiation.",
            5: "jacob renfield has the lung mass blocking the left side. we did a rigid bronch. ebus first to biopsy the nodes under the carina. then went after the tumor in the left main. chopped it out with forceps and burned it with apc. dilated it open. looks better about half open now. needs radiation asap.",
            6: "DATE OF PROCEDURE: December 17 2018. PROCEDURE PERFORMED: Rigid bronchoscopy. Indication: left mainstem obstruction. Findings: Left mainstem completely obstructed. EBUS bronchoscope inserted, subcarinal mass biopsied. Tumor debulked using APC, electrocautery, cryotherapy. Left mainstem dilated with balloon. Argon plasma coagulation used for hemostasis. Recommendations: Radiation oncology consultation.",
            7: "[Indication]\nLeft mainstem obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. EBUS TBNA subcarinal. Tumor debulking (APC, Cryo). Balloon dilation LMS.\n[Plan]\nRad Onc, monitor hemoptysis.",
            8: "We performed a rigid bronchoscopy on Mr. Renfield to open up his airway. The tumor was blocking the left main bronchus. We biopsied the lymph nodes first, then spent time chipping away at the tumor with forceps and cautery. We dilated it with a balloon and got it about 50% open. He's going to need radiation to keep it that way.",
            9: "Procedure: Rigid bronchoscopy with EBUS sampling and tumor recanalization.\nDx: Malignant airway obstruction.\nIntervention: EBUS-guided needle aspiration. Mechanical resection of endoluminal tumor via forceps and cryotherapy. Balloon dilation.\nOutcome: Partial restoration of airway caliber."
        },
        7: { # Patricia Thompson (Coils)
            1: "Indication: Severe Homogeneous Emphysema.\nProc: Bilateral Coil Placement.\nActions:\n- RUL: 10 Coils (125mm).\n- LUL: 10 Coils (125mm).\n- Fluoro guidance.\nResult: No complications. Good coil configuration.\nPlan: Admit, Prednisone taper.",
            2: "PROCEDURE NOTE: Bronchoscopic lung volume reduction via endobronchial coil placement. \nINDICATION: GOLD Stage IV homogeneous emphysema. \nTECHNIQUE: Under fluoroscopic guidance, 10 RepneuCoils were deployed in the Right Upper Lobe and 10 in the Left Upper Lobe. \nFINDINGS: Systematic airway inspection was normal. Coils were deployed without incident in a 'pigtail' configuration. \nCONCLUSION: Successful bilateral LVR.",
            3: "Code: 31622 (Diagnostic Bronchoscopy - Generic for Coils if no specific code).\nProcedure: Placement of 20 Endobronchial Coils (10 RUL, 10 LUL).\nGuidance: Fluoroscopy utilized.\nMedical Necessity: Severe homogeneous emphysema refractory to medical therapy.",
            4: "Procedure: Coils (LVR)\nPatient: Pat Thompson\nSteps:\n1. Mod sedation.\n2. Scope in.\n3. RUL: 10 coils placed.\n4. LUL: 10 coils placed.\n5. Fluoro check: Good.\nPlan: Admit, antibiotics, steroids.",
            5: "patricia thompson here for coils. she has diffuse emphysema. we put 10 coils in the right upper and 10 in the left upper using the scope and fluoro. went smooth no bleeding. chest xray looks good. admit for observation start prednisone.",
            6: "INTERVENTIONAL PULMONOLOGY PROCEDURE REPORT. Bronchoscopic Lung Volume Reduction via Endobronchial Coil Placement. Patient: Patricia Thompson. Indication: Severe homogeneous emphysema. Procedure: RUL Coil Placement (10 coils), LUL Coil Placement (10 coils). Fluoroscopy used. Complications: None. Assessment: Successful bilateral endobronchial coil placement. Plan: Admit, Prednisone taper.",
            7: "[Indication]\nHomogeneous Emphysema.\n[Anesthesia]\nModerate.\n[Description]\nBilateral coil placement. 10 coils RUL, 10 coils LUL. Fluoroscopic confirmation.\n[Plan]\nAdmit, CXR, Steroids.",
            8: "Ms. Thompson came in for her coil procedure today. Since her emphysema is spread out evenly, coils are the best option. We placed 10 coils in the right top lobe and 10 in the left top lobe. We used x-ray guidance to make sure they were sitting right. Everything went perfectly, no issues at all.",
            9: "Operation: Bronchoscopic Lung Volume Reduction via Coil Implantation.\nTarget: Bilateral Upper Lobes.\nAction: Deployment of 20 RepneuCoils under fluoroscopic visualization.\nOutcome: Satisfactory coil positioning, no immediate adverse events."
        },
        8: { # Sharon Kim (Teaching Case)
            1: "Indication: Alpha-1 Emphysema (LLL).\nProc: BLVR LLL (Teaching).\nActions:\n- Chartis: CV Negative.\n- Valve selection: 5.5mm (LB6), 4.0mm (LB8-10).\n- Fellow placed valves. Repositioning required for first.\n- Final: Complete occlusion.\nPlan: Admit.",
            2: "PROCEDURE NOTE (TEACHING): 69F with Alpha-1 antitrypsin deficiency. \nSUPERVISION: Dr. Williams supervising Dr. Lee (Fellow). \nDETAILS: Chartis assessment of LLL indicated absent collateral ventilation. Valve sizing was performed based on CT. The fellow deployed valves in LB6 and LB8-10. Correction of valve orientation was performed under guidance. \nOUTCOME: Successful lobar occlusion confirmed.",
            3: "Coding: 31647 (Valve Placement), 31634 (Chartis). \nNote: Teaching physician present. \nLobe: Left Lower Lobe.\nDetails: Chartis confirmed negative CV. Valves placed in LB6 and LB8-10.",
            4: "Procedure: BLVR (Teaching)\nAttending: Dr. Williams\nFellow: Dr. Lee\nSteps:\n1. Airway exam.\n2. Chartis LLL: Negative.\n3. Measured bronchi.\n4. Placed 2 valves (LB6, LB8-10).\n5. Had to fix the first one, second one perfect.\nPlan: Admit.",
            5: "sharon kim here for valves she has alpha 1. i let the fellow dr lee do the procedure. we checked the lll with chartis it was good. fellow had a little trouble with the first valve had to move it but got it eventually. second one was fine. lobe is sealed up. good teaching case.",
            6: "Procedure Date: 01/17/2025. Patient: Sharon Kim. Procedure: BLVR LLL. Teaching case with Fellow. Chartis Assessment: Target LLL, NEGATIVE CV. Valve Deployment: LB6 (5.5mm), LB8-10 (4.0mm). First valve required repositioning. Final bronchoscopy: Both valves well-positioned, complete occlusion confirmed. Patient Outcome: Tolerated well.",
            7: "[Indication]\nAlpha-1 Emphysema.\n[Anesthesia]\nModerate.\n[Description]\nTeaching case. Chartis LLL negative. Valves placed LB6, LB8-10. Repositioning required. Occlusion achieved.\n[Plan]\nAdmit.",
            8: "This was a teaching case with Dr. Lee. We treated Ms. Kim for her Alpha-1 emphysema. We confirmed the left lower lobe was a good target with the Chartis system. Dr. Lee placed the valves. We had to adjust the first one to get a perfect seal, but the second one went in easily. The lobe is completely blocked off now.",
            9: "Procedure: Bronchoscopic lung volume reduction (Educational).\nSubject: Alpha-1 antitrypsin deficiency.\nMethod: Chartis evaluation. Deployment of endobronchial valves in LLL. One valve required realignment.\nResult: Total lobar obstruction."
        },
        9: { # Chloe Whitford (Diagnostic Multi-biopsy)
            1: "Indication: Bilateral lung masses.\nProc: Diagnostic Bronch.\nActions:\n- RUL Mass: TBNA x5, Forceps x6.\n- LLL Lesion: Radial EBUS, TBNA x4, Forceps x5.\n- BAL LLL.\n- ROSE: Malignant (RUL).\nPlan: PACU, Oncology.",
            2: "OPERATIVE REPORT: Diagnostic bronchoscopy for suspected malignancy. \nFINDINGS: Fungating mass RUL, peripheral lesion LLL. \nSAMPLING: \n1. RUL Mass: TBNA and endobronchial forceps biopsy. ROSE positive for malignancy. \n2. LLL Lesion: Localized via Radial EBUS. TBNA and forceps biopsy performed. \n3. BAL: LLL superior segment. \nCONCLUSION: Successful sampling of bilateral lesions.",
            3: "Codes: 31629 (TBNA), 31625 (Forceps Biopsy), 31654 (Radial EBUS), 31624 (BAL).\nSites: RUL (Endobronchial), LLL (Peripheral).\nDetails: Multiple modalities used for diagnosis/staging. ROSE confirmed malignancy in RUL.",
            4: "Procedure: Diagnostic Bronch\nPatient: Chloe Whitford\nSteps:\n1. GA / 8.5 ETT.\n2. Saw mass in RUL -> Biopsied (Needle & Forceps).\n3. Radial EBUS for LLL nodule -> Biopsied.\n4. BAL LLL.\n5. ROSE said RUL is cancer.\nPlan: Wait for final path.",
            5: "chloe whitford has bilateral masses. we went in with the scope. big fungating thing in the rul took a bunch of bites and needle passes. rose says cancer. then went to the lll used the radial ebus to find the spot and biopsied that too. washed the lll. shes stable.",
            6: "Chloe Whitford. Date: 3/20/24. Indications: Bilateral lung masses. Initial Airway Inspection: Endobronchial fungating mass RUL. Tissue Sampling: RUL Endobronchial Biopsy (TBNA, Forceps). LLL Lesion Biopsy (Radial EBUS, TBNA, Forceps). BAL LLL. ROSE: RUL malignant. Final Airway Re-Inspection: No active bleeding. Disposition: PACU.",
            7: "[Indication]\nSuspected lung malignancy.\n[Anesthesia]\nGeneral.\n[Description]\nRUL mass biopsied (TBNA/Forceps). LLL lesion localized w/ REBUS and biopsied. BAL LLL. ROSE positive.\n[Plan]\nPathology pending.",
            8: "Ms. Whitford has masses in both lungs. We did a bronchoscopy to find out what they are. The one in the right upper lobe was visible inside the airway, so we biopsied it directly—the preliminary result is cancer. The one in the left lower lobe was deeper, so we used a special ultrasound (radial EBUS) to find it and get samples. We also washed the area. We'll wait for the full report.",
            9: "Procedure: Diagnostic bronchoscopy with tissue sampling.\nFindings: Obstructing RUL mass, peripheral LLL lesion.\nIntervention: Transbronchial needle aspiration and forceps biopsy of RUL. Radial EBUS localization and sampling of LLL. Bronchoalveolar lavage.\nDiagnosis: Suspected malignancy confirmed by ROSE."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the prompt's examples
    # (In a real script, this data comes from reading the source JSON)
    return [
        {"idx": 0, "orig_name": "Maria Rodriguez", "orig_age": 72, "names": ["Ana Silva", "Elena Gomez", "Isabella Torres", "Sofia Ramirez", "Camila Vargas", "Valentina Morales", "Lucia Castillo", "Martina Reyes", "Gabriela Mendoza"]},
        {"idx": 1, "orig_name": "Emma Carlisle", "orig_age": 45, "names": ["Olivia Bennett", "Charlotte Ross", "Amelia Hughes", "Harper Foster", "Evelyn Powell", "Abigail Butler", "Emily Russell", "Elizabeth Cole", "Sofia Hayes"]}, # Age inferred/random if not in snippets
        {"idx": 2, "orig_name": "Nolan Shepherd", "orig_age": 55, "names": ["Liam Mason", "Noah Brooks", "Oliver Price", "Elijah Sanders", "William Henderson", "James Coleman", "Benjamin Jenkins", "Lucas Perry", "Henry Long"]},
        {"idx": 3, "orig_name": "Thomas O'Brien", "orig_age": 70, "names": ["Jack Sullivan", "Connor McCarthy", "Ryan Murphy", "Daniel O'Connor", "Michael Kennedy", "Patrick Walsh", "Sean Ryan", "Liam Doherty", "Aidan Kelly"]},
        {"idx": 4, "orig_name": "Logan Pierce", "orig_age": 76, "names": ["Mason Alexander", "Ethan Graham", "Jacob Wallace", "Michael West", "Daniel Reynolds", "Matthew Fisher", "Christopher Ellis", "Andrew Harrison", "Joseph Gibson"]},
        {"idx": 5, "orig_name": "Harold Johnson", "orig_age": 74, "names": ["Robert Smith", "William Jones", "James Brown", "Charles Davis", "George Miller", "Edward Wilson", "Frank Moore", "Thomas Taylor", "Richard Anderson"]},
        {"idx": 6, "orig_name": "Jacob Renfield", "orig_age": 68, "names": ["Samuel Peters", "David Evans", "Joseph Phillips", "Charles Mitchell", "Thomas Turner", "Christopher Campbell", "Daniel Parker", "Matthew Collins", "Anthony Stewart"]},
        {"idx": 7, "orig_name": "Patricia Thompson", "orig_age": 72, "names": ["Linda Harris", "Barbara Martin", "Elizabeth Thompson", "Jennifer Garcia", "Maria Martinez", "Susan Robinson", "Margaret Clark", "Dorothy Rodriguez", "Lisa Lewis"]},
        {"idx": 8, "orig_name": "Sharon Kim", "orig_age": 69, "names": ["Michelle Lee", "Jennifer Park", "Sarah Choi", "Jessica Jung", "Amanda Yoon", "Stephanie Kang", "Melissa Cho", "Nicole Hwang", "Christine Shin"]},
        {"idx": 9, "orig_name": "Chloe Whitford", "orig_age": 50, "names": ["Rachel Green", "Monica Geller", "Phoebe Buffay", "Janice Hosenstein", "Carol Willick", "Susan Bunch", "Judy Geller", "Ursula Buffay", "Emily Waltham"]},
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
                # Fallback if variation is missing
                note_entry["note_text"] = f"VARIATION MISSING for Note {idx} Style {style_num}"

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
    output_filename = output_dir / "synthetic_blvr_notes_part_036.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()