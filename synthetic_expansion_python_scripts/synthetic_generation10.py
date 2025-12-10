import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_010.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the specified years."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    days_between = (end - start).days
    random_days = random.randrange(days_between)
    return start + datetime.timedelta(days=random_days)

def get_variations():
    """
    Returns the dictionary of manually crafted text variations for the notes.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        # ---------------------------------------------------------------------
        # Note 0: Daniel Wilbert Conley (Stent Removal)
        # Original: Rigid bronch, removal of 2 stents (tracheal & esophageal stent interaction), TE fistula.
        # ---------------------------------------------------------------------
        0: {
            1: "Indication: Stent migration/infection.\nProc: Rigid bronch, stent removal x2.\nFindings: Purulent infection. Distal stent migrated to RMS. L main obstructed.\nAction: Lavage. Forceps removal of tracheal stents. Esophageal stent visualized covering fistula.\nPlan: PACU. Cultures. Antibiotics.",
            
            2: "OPERATIVE REPORT: Rigid bronchoscopy with removal of airway foreign bodies.\nINDICATIONS: Complicated TE fistula with stent migration and presumed infection.\nPROCEDURE: General anesthesia was induced. Initial flexible inspection revealed purulent secretions and a migrated tracheal stent occluding the left mainstem. A rigid bronchoscope was introduced. The airway was lavaged. Using rigid forceps, the migrated tracheal stent was grasped and extracted. Inspection revealed underlying mucosal inflammation but no active bleeding. The esophageal stent remained in place covering the fistula.",
            
            3: "Code: 31635 (Bronchoscopy with removal of foreign body/stent).\nJustification: Removal of migrated self-expanding tracheal stents via rigid bronchoscopy.\nComplexity: Infection present (purulence), requiring lavage and careful extraction to avoid damaging the underlying TE fistula site.",
            
            4: "Procedure: Stent Removal.\nAttending: Dr. Gallegos.\nSteps:\n1. LMA/Flex scope check.\n2. Rigid scope inserted.\n3. Lavage of pus.\n4. Migrated stent grabbed with rigid forceps.\n5. Stent removed en bloc with scope.\n6. Airway inspected - fistula covered by esophageal stent.\nPlan: Nebs, cultures.",
            
            5: "stent removal for mr conley... had a te fistula and the stent moved... lot of pus in there... used the rigid scope to pull the stent out... airway looks raw but no bleeding... the other stent in the esophagus is still covering the hole... sent pus for culture.",
            
            6: "Patient: Daniel Conley. Procedure: Rigid bronchoscopy, Stent removal. Indication: Stent migration, infection. Findings: Purulent secretions, stent in RMS. Action: Lavage, rigid forceps removal of stent. Result: Stent removed, airway patent, fistula covered by esophageal stent. Plan: Antibiotics, observation.",
            
            7: "[Indication]\nStent migration, TE fistula, infection.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Lavage of purulent material. Removal of migrated tracheal stent. Inspection of TE fistula (covered by esophageal stent).\n[Plan]\nPACU, cultures pending.",
            
            8: "Mr. Conley required removal of a migrated airway stent complicated by infection. Under general anesthesia, we used a rigid bronchoscope to access the airway. After clearing significant purulent debris, we successfully grasped and removed the migrated stent. The underlying TE fistula appeared stable, covered by his esophageal stent.",
            
            9: "Operation: Rigid bronchoscopy with extraction of prosthetic airway devices. Reason: Device displacement and sepsis. Details: Under general anesthesia, the airway was cannulated. Purulent effusions were evacuated. The displaced tracheal prosthesis was seized with rigid pincers and withdrawn. The esophageal prosthesis was observed obturating the fistula."
        },

        # ---------------------------------------------------------------------
        # Note 1: Maizie Booth (Med Thoracoscopy + IPC)
        # Original: R effusion, carcinomatosis. Biospy x12. IPC placed.
        # ---------------------------------------------------------------------
        1: {
            1: "Indication: R Pleural Effusion.\nProc: Med Thoracoscopy + IPC.\nFindings: Carcinomatosis. 1600cc fluid.\nAction: Biopsy x12. 15.5Fr IPC placed/tunneled.\nResult: Lung re-expanded. Minimal bleed.",
            
            2: "PROCEDURE NOTE: Medical Thoracoscopy and Indwelling Pleural Catheter Placement.\nCLINICAL SUMMARY: Right-sided exudative effusion. \nFINDINGS: 1.6L serosanguinous fluid drained. Diffuse parietal and visceral nodules consistent with carcinomatosis. \nINTERVENTION: Twelve biopsies were taken. A PleurX catheter was tunneled and inserted under direct visualization. Post-procedure imaging confirmed catheter position.",
            
            3: "Codes: 32601 (Dx Thoracoscopy), 32550 (IPC placement).\nRationale: Diagnostic inspection and biopsy of pleural carcinomatosis followed by placement of a tunneled catheter for long-term drainage.\nPathology: Pleural nodules biopsied.",
            
            4: "Procedure: Pleuroscopy & PleurX.\nSteps:\n1. Lateral decubitus.\n2. Trocar placement.\n3. Fluid drainage (1600cc).\n4. Biopsies of nodules (x12).\n5. PleurX catheter tunneled and placed.\n6. Closure.\nNo complications.",
            
            5: "thoracoscopy for maizie booth... drained 1600cc fluid... saw cancer nodules everywhere took 12 biopsies... put in a pleurx catheter for drainage... tunnel looks good... sent tissue to lab.",
            
            6: "Pt: Maizie Booth. Proc: Medical Thoracoscopy, IPC placement. Findings: 1600cc fluid, diffuse nodules. Action: Biopsy x12, IPC (15.5Fr) placed. Outcome: Lung re-expanded, catheter functional. Plan: Path f/u, catheter teaching.",
            
            7: "[Indication]\nRight pleural effusion, suspect malignancy.\n[Anesthesia]\nModerate/Local.\n[Description]\nThoracoscopic entry. 1600cc drained. Multiple biopsies of nodules. Indwelling pleural catheter placed and tunneled.\n[Plan]\nDischarge, catheter care education.",
            
            8: "Ms. Booth underwent a medical thoracoscopy to investigate her pleural effusion. We drained 1.6 liters of fluid and found extensive nodules, which were biopsied. To manage the recurrent fluid, we placed a tunneled pleural catheter. She tolerated the procedure well.",
            
            9: "Intervention: Medical Thoracoscopy with implantation of tunneled drainage catheter. Subject: Maizie Booth. Findings: Extensive carcinomatosis. Action: Twelve tissue samples procured. Tunneled catheter deployed for chronic drainage."
        },

        # ---------------------------------------------------------------------
        # Note 2: George Martinez (Thermal Vapor Ablation - BLVR)
        # Original: RUL emphysema. Vapor ablation (InterVapor). 14 calories total.
        # ---------------------------------------------------------------------
        2: {
            1: "Indication: Severe RUL Emphysema.\nProc: Thermal Vapor Ablation.\nTarget: RUL (RB3, RB1).\nDose: 14 Cal total (8 cal RB3, 6 cal RB1).\nResult: Good vapor delivery. No complications.\nPlan: Admit, prophylactic antibiotics/steroids.",
            
            2: "OPERATIVE REPORT: Bronchoscopic Lung Volume Reduction via Thermal Vapor Ablation.\nINDICATION: Heterogeneous RUL emphysema with collateral ventilation.\nPROCEDURE: The RUL was catheterized. The InterVapor system was used to deliver thermal energy. \nTREATMENT: \n- Anterior segment (RB3): 8 calories.\n- Apical segment (RB1): 6 calories.\nTotal energy 14 calories to a target volume of 10g. Vapor containment was confirmed fluoroscopically.",
            
            3: "Code: 31647 (BLVR - used as proxy for vapor in this system).\nTechnique: Thermal vapor ablation of emphysematous tissue.\nDosimetry: 14 Calories total delivered to RUL segments.\nMedical Necessity: Severe emphysema not suitable for valves due to CV+.",
            
            4: "Procedure: Vapor Ablation (BLVR).\nSteps:\n1. Airway sizing.\n2. Catheter to RUL.\n3. Vapor delivery RB3 (8 cal).\n4. Vapor delivery RB1 (6 cal).\n5. Checked for bleeding/pneumo.\nPlan: Antibiotics, Prednisone.",
            
            5: "vapor procedure for george... rul emphysema... put the catheter in the right upper lobe... steamed the anterior and apical segments 14 calories total... patient did fine... admit for inflammatory response watch.",
            
            6: "Pt: George Martinez. Proc: Bronchoscopic Thermal Vapor Ablation. Target: RUL. Dose: 14 cal (RB1, RB3). Complications: None. Plan: ICU observation, antibiotics, steroids for post-ablation inflammation.",
            
            7: "[Indication]\nSevere RUL emphysema, CV positive.\n[Anesthesia]\nMAC.\n[Description]\nThermal vapor ablation. RB3 (8 cal), RB1 (6 cal). Total 14 cal. Fluoroscopic confirmation.\n[Plan]\nAdmit, monitor for fever/infiltrate.",
            
            8: "Mr. Martinez underwent thermal vapor ablation for his emphysema. Because he has collateral ventilation, valves were not an option. We treated the right upper lobe segments with heated water vapor, delivering a total of 14 calories. He will be monitored for the expected inflammatory response.",
            
            9: "Operation: Bronchoscopic Lung Volume Reduction via Thermal Vapor. Target: Right Upper Lobe. Method: Instillation of heated vapor. Dosage: 14 calories. Outcome: Successful delivery, no immediate adverse events."
        },

        # ---------------------------------------------------------------------
        # Note 3: Maria Rodriguez (BLVR LLL - Valves)
        # Original: 72F, LLL emphysema. 3 Zephyr valves (LB6, LB8-10).
        # ---------------------------------------------------------------------
        3: {
            1: "Indication: Severe LLL Emphysema.\nProc: BLVR w/ Valves.\nImplants: 3 Zephyr valves (LB6, LB8, LB9-10).\nResult: Complete occlusion. No complications.\nPlan: CXR, Admit.",
            
            2: "PROCEDURE NOTE: Endobronchial Valve Placement.\nINDICATION: Heterogeneous emphysema, LLL predominant.\nPROCEDURE: Flexible bronchoscopy was performed. The LLL segments were sized and occluded.\n- LB6: 4.0mm valve\n- LB8: 4.0mm valve\n- LB9-10: 5.5mm valve\nTotal occlusion of the target lobe was achieved.",
            
            3: "Code: 31647 (Bronchoscopy with valve placement).\nDetails: 3 Zephyr valves deployed in the Left Lower Lobe (LB6, LB8, LB9-10). Complete lobar occlusion verified.",
            
            4: "Procedure: BLVR (Valves).\nAttending: Dr. Park.\nSteps:\n1. Mod sedation.\n2. Sized airways.\n3. Deployed 3 valves in LLL.\n4. Checked seal.\nResult: Good occlusion.",
            
            5: "valve placement for maria... lll emphysema... put in three zephyr valves lb6 lb8 and lb9-10... looks like a good seal... admit for pneumo watch.",
            
            6: "Pt: Maria Rodriguez. Proc: BLVR LLL. Valves: 3 Zephyr (LB6, LB8, LB9-10). Findings: Complete occlusion. Complications: None. Plan: CXR, observation.",
            
            7: "[Indication]\nSevere LLL emphysema.\n[Anesthesia]\nModerate.\n[Description]\nDeployment of 3 endobronchial valves (Zephyr) to LLL. Complete atelectasis achieved.\n[Plan]\nAdmit, serial CXRs.",
            
            8: "Mrs. Rodriguez underwent elective valve placement for her emphysema. We targeted the left lower lobe. Three valves were successfully placed in the segmental bronchi, achieving complete occlusion of the lobe. She is stable and will be monitored for pneumothorax.",
            
            9: "Procedure: Bronchoscopic Lung Volume Reduction via Valve Implantation. Target: Left Lower Lobe. Implants: Three Zephyr valves. Outcome: Total lobar obstruction accomplished."
        },

        # ---------------------------------------------------------------------
        # Note 4: Emma Carlisle (Y-Stent)
        # Original: 65F, Extrinsic compression. Silicone Y-stent.
        # ---------------------------------------------------------------------
        4: {
            1: "Indication: Tracheal compression (90%).\nProc: Rigid Bronch, Y-Stent.\nStent: Silicone 16x13x13.\nAction: Stent customized and deployed via rigid scope. Limbs positioned in trachea/LMS/RMS.\nResult: Airway patent. Hypoxia resolved.",
            
            2: "OPERATIVE REPORT: Rigid bronchoscopy with silicone Y-stent placement.\nINDICATION: Critical central airway obstruction due to extrinsic compression.\nPROCEDURE: The airway was secured with a rigid bronchoscope. Significant tracheal and carinal compression was noted. A 16x13x13 silicone Y-stent was customized and deployed. The tracheal, left, and right limbs were positioned to stent open the carina. Post-deployment inspection confirmed restored patency.",
            
            3: "Codes: 31631 (Tracheal stent), 31636 (Bronchial stent), 31637 (Bronchial stent add-on).\nJustification: Placement of a carinal Y-stent involves stenting the trachea and both mainstem bronchi to resolve complex obstruction.",
            
            4: "Procedure: Y-Stent Placement.\nSteps:\n1. GA/Paralytics.\n2. Rigid bronchoscopy.\n3. Measured airway.\n4. Customized Y-stent.\n5. Deployed stent.\n6. Confirmed position with flex scope.\nAirway open.",
            
            5: "y stent for emma... she had bad compression of the trachea and carina... used the rigid scope... cut a silicone y stent to size... deployed it... opened up the airway perfectly... no bleeding.",
            
            6: "Pt: Emma Carlisle. Indication: Tracheal compression. Proc: Rigid Bronch, Y-Stent (Silicone). Stent customized and placed. Trachea and both mainstems stented. Result: Airway patent. Plan: ICU.",
            
            7: "[Indication]\nExtrinsic tracheal/carinal compression.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Deployment of silicone Y-stent (16x13x13). Patent airway established.\n[Plan]\nICU, humidification.",
            
            8: "Ms. Carlisle presented with respiratory failure due to tracheal compression. We performed a rigid bronchoscopy and placed a silicone Y-stent. This successfully scaffolded the trachea and both mainstem bronchi, relieving the obstruction. She was transferred to the ICU in stable condition.",
            
            9: "Operation: Rigid bronchoscopy with deployment of bifurcated airway prosthesis. Indication: Critical airway stenosis. Action: A silicone Y-stent was tailored and inserted. The prosthesis successfully buttressed the trachea and both main bronchi."
        },

        # ---------------------------------------------------------------------
        # Note 5: Nolan Shepherd (Rigid Debulking - No Stent)
        # Original: 65M, Endotracheal tumor. Rigid debulking (Snare/APC). Stent deferred.
        # ---------------------------------------------------------------------
        5: {
            1: "Indication: Tracheal obstruction (tumor).\nProc: Rigid Bronch, Debulking.\nAction: Snare resection of polypoid lesions. APC to base. 90% patency achieved.\nNote: Patient declined stent.\nPlan: Oncology consult.",
            
            2: "OPERATIVE NOTE: Rigid bronchoscopy with mechanical and thermal tumor destruction.\nFINDINGS: Multiple polypoid lesions obstructing the subglottic trachea.\nPROCEDURE: The large lesions were resected using an electrocautery snare. The tumor base was treated with Argon Plasma Coagulation (APC). Excellent luminal restoration was achieved. Stent placement was discussed but deferred per patient preference.",
            
            3: "Code: 31641 (Bronchoscopy with destruction of tumor).\nTechnique: Mechanical debulking (snare) and thermal ablation (APC) of tracheal tumor. No stent placed.",
            
            4: "Procedure: Tumor Debulking.\nSteps:\n1. Rigid scope inserted.\n2. Snare used to remove polyps.\n3. APC applied to base.\n4. Suctioned debris.\n5. Airway open.\nNo stent placed.",
            
            5: "rigid bronch for nolan... he had those tracheal tumors blocking his airway... used the snare to chop them out and apc to burn the rest... airway looks much better 90 percent open... he didnt want a stent so we didnt put one in.",
            
            6: "Pt: Nolan Shepherd. Indication: Tracheal tumor. Proc: Rigid bronch, Debulking (Snare/APC). Findings: 90% obstruction reduced to minimal. Stent: None (patient refused). Plan: Oncology f/u.",
            
            7: "[Indication]\nSymptomatic tracheal tumor.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Snare resection of polypoid masses. APC ablation of base. Luminal patency restored.\n[Plan]\nOncology referral.",
            
            8: "Mr. Shepherd underwent rigid bronchoscopy to debulk a tracheal tumor causing obstruction. We used a snare to remove the bulk of the disease and APC to treat the base. We achieved 90% patency. Per his request, no stent was placed. He will follow up with oncology.",
            
            9: "Operation: Rigid bronchoscopy with endoluminal tumor ablation. Method: Electrocautery snare and Argon Plasma Coagulation. Outcome: Restoration of tracheal lumen. Prosthesis: Deferred."
        },

        # ---------------------------------------------------------------------
        # Note 6: Thomas O'Brien (BLVR - Valves + Chartis)
        # Original: 70M, LUL emphysema. Chartis (-). 4 Valves.
        # ---------------------------------------------------------------------
        6: {
            1: "Indication: LUL Emphysema.\nProc: BLVR.\nChartis: CV Negative.\nImplants: 4 Zephyr valves LUL.\nResult: Complete occlusion.\nPlan: Admit.",
            
            2: "PROCEDURE: Bronchoscopic Lung Volume Reduction.\nASSESSMENT: Chartis assessment of the LUL confirmed absence of collateral ventilation.\nINTERVENTION: Four Zephyr valves were deployed in the LUL segments (LB1+2, LB3, Lingula). Atelectasis was noted at the end of the procedure.",
            
            3: "Codes: 31647 (Valve placement), 31634 (Chartis - bundled).\nNote: Chartis assessment performed in same lobe. Primary service is valve placement.",
            
            4: "Procedure: LUL Valves.\nSteps:\n1. Mod sedation.\n2. Chartis check: No CV.\n3. Placed 4 valves.\n4. Checked seal.\nSuccess.",
            
            5: "valve procedure for thomas... lul emphysema... chartis said no cv... put in 4 valves total... looks blocked off nicely... admit.",
            
            6: "Pt: Thomas O'Brien. Proc: BLVR LUL. Chartis: Neg CV. Valves: 4 Zephyr. Result: Occlusion. Plan: Admit.",
            
            7: "[Indication]\nLUL Emphysema.\n[Anesthesia]\nModerate.\n[Description]\nChartis assessment (CV neg). 4 Zephyr valves placed in LUL. Lobar occlusion achieved.\n[Plan]\nAdmit.",
            
            8: "Mr. O'Brien underwent BLVR for his LUL emphysema. We confirmed he was a good candidate with Chartis. Four valves were placed, effectively occluding the lobe.",
            
            9: "Intervention: Valve Implantation for Emphysema. Target: LUL. Assessment: Chartis negative for collateral flow. Action: Four valves deployed. Outcome: Lobar exclusion."
        },

        # ---------------------------------------------------------------------
        # Note 7: Logan Pierce (Nav Bronch + Chartis + Biopsy)
        # Original: 76M, RUL nodule. Ion/ConeBeam. Chartis LUL.
        # ---------------------------------------------------------------------
        7: {
            1: "Indication: RUL Nodule + COPD eval.\nProc: Ion Nav Bronch + Chartis.\nAction: Nav to RUL. TBNA/Cryo/BAL of nodule. Chartis LUL (CV neg) for future BLVR.\nResult: Samples obtained. LUL is BLVR candidate.",
            
            2: "OPERATIVE REPORT: Robotic bronchoscopy and collateral ventilation assessment.\nPROCEDURE: The Ion system was navigated to an RUL nodule. CBCT confirmed position. TBNA and cryobiopsy were performed. Subsequently, Chartis assessment of the *Left* Upper Lobe was performed for future emphysema treatment planning; this confirmed CV negativity.",
            
            3: "Codes: 31627 (Nav), 31629 (TBNA), 31628 (Cryo), 31624 (BAL), 31634 (Chartis).\nNote: Chartis (31634) is distinct as it targeted the LUL, while biopsies were in the RUL.",
            
            4: "Procedure: Ion Bronch + Chartis.\nSteps:\n1. Nav to RUL nodule.\n2. Biopsy x6, Cryo x5.\n3. Chartis check of LUL (for future valves).\n4. BAL.\nPlan: D/C.",
            
            5: "logan pierce bronch... used the robot for that rul nodule... took needles and cryo samples... also checked his left lung with chartis for valves later... no cv there... waking up fine.",
            
            6: "Pt: Logan Pierce. Proc: Ion Nav Bronch (RUL nodule), Chartis (LUL). Findings: RUL nodule sampled (TBNA, Cryo). LUL Chartis negative (CV-). Plan: Path results, eval for LUL valves.",
            
            7: "[Indication]\nRUL nodule, COPD.\n[Anesthesia]\nGeneral.\n[Description]\nRobotic navigation to RUL. CBCT. Biopsy (needle/cryo). Chartis assessment of LUL (CV negative).\n[Plan]\nPath f/u.",
            
            8: "Mr. Pierce underwent a combined procedure. We used the Ion robot to biopsy a nodule in his right upper lobe. We also performed a Chartis assessment on his left upper lobe to see if he qualifies for valves in the future; the results were promising.",
            
            9: "Procedure: Robotic-assisted biopsy and physiological airway assessment. Target 1: RUL Nodule (Biopsy). Target 2: LUL (Chartis). Outcome: Specimens procured; Collateral ventilation absent in LUL."
        },

        # ---------------------------------------------------------------------
        # Note 8: Harold Johnson (BLVR - Valves w/ Pneumo)
        # Original: 74M, RUL Bulla. Valves for air leak. Pneumothorax complication.
        # ---------------------------------------------------------------------
        8: {
            1: "Indication: Persistent air leak (RUL).\nProc: Valve placement.\nComplication: Tension PTX.\nAction: Emergency chest tube placed. Stabilized. Additional valve placed RB3.\nResult: Air leak reduced. PTX managed.",
            
            2: "OPERATIVE NOTE: Endobronchial valve placement for air leak management.\nCOMPLICATION: Following placement of the first valve in RB1, the patient developed a tension pneumothorax. A chest tube was emergently placed.\nCOURSE: Once stable, a second valve was placed in RB3. The air leak was reduced. The patient was admitted to ICU.",
            
            3: "Code: 31647 (Valve placement).\nNote: Procedure performed for air leak (off-label) but technically fits valve placement code. Complication of pneumothorax managed with chest tube.",
            
            4: "Procedure: Valves for Air Leak.\nEvents:\n1. RB1 valve placed.\n2. Sats dropped -> PTX.\n3. Chest tube placed.\n4. RB3 valve placed.\n5. Leak better.\nPlan: ICU.",
            
            5: "trying to fix an air leak for harold... put a valve in the apical segment and he blew a pneumo right away... put a chest tube in fast... stabilized him... put one more valve in... leak is better but not gone.",
            
            6: "Pt: Harold Johnson. Indication: Air leak. Proc: Valves RUL. Event: Iatrogenic Tension PTX. Mgmt: Chest tube. Outcome: Air leak reduced. Disposition: ICU.",
            
            7: "[Indication]\nPersistent air leak, RUL bulla.\n[Anesthesia]\nModerate.\n[Description]\nValve placed RB1. Complication: Tension PTX. Chest tube placed. Second valve RB3. Air leak reduced.\n[Plan]\nICU.",
            
            8: "Mr. Johnson underwent valve placement to treat a persistent air leak. Unfortunately, he developed a tension pneumothorax during the procedure, which required immediate chest tube placement. We proceeded to place a second valve to help seal the leak. He is currently stable in the ICU.",
            
            9: "Intervention: Endobronchial Valve Deployment. Indication: Bronchopleural fistula. Complication: Pneumothorax. Mitigation: Thoracostomy tube. Outcome: Partial resolution of air leak."
        },

        # ---------------------------------------------------------------------
        # Note 9: Jacob Renfield (Rigid Debulking + EBUS)
        # Original: 65M, LMS obstruction. Rigid debulking. EBUS-TBNA. No stent.
        # ---------------------------------------------------------------------
        9: {
            1: "Indication: LMS obstruction.\nProc: Rigid Bronch, Debulking, EBUS.\nAction: EBUS-TBNA subcarinal. Rigid debulking LMS (APC/Cryo/Balloon). 50% improvement.\nNote: Stent deferred.\nPlan: Oncology/Radiation.",
            
            2: "OPERATIVE REPORT: Rigid bronchoscopy for malignant airway obstruction.\nPROCEDURE: EBUS-TBNA was performed on the subcarinal station. Attention was turned to the obstructed left mainstem. Using rigid coring, APC, and balloon dilation, the airway was recanalized. No stent was placed at this time.",
            
            3: "Codes: 31641 (Tumor destruction), 31652 (EBUS-TBNA 1-2 stations).\nJustification: Mechanical/thermal destruction of LMS tumor. EBUS sampling of subcarinal node. No stent codes.",
            
            4: "Procedure: Rigid Debulking.\nSteps:\n1. EBUS subcarinal.\n2. Rigid scope to LMS.\n3. Debulked tumor (APC/Mech).\n4. Balloon dilation.\n5. Airway patent.\nPlan: Radiation.",
            
            5: "rigid bronch for jacob... left main was blocked... took ebus samples first... then opened up the left main with apc and the rigid scope... dilated it too... looks better... gonna send for radiation.",
            
            6: "Pt: Jacob Renfield. Proc: Rigid Bronch, EBUS, Debulking. Findings: LMS obstruction, subcarinal LAD. Action: EBUS-TBNA, APC/Cryo debulking LMS. Result: Recanalized. Plan: Rad Onc.",
            
            7: "[Indication]\nMalignant LMS obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS-TBNA (Subcarinal). Rigid bronchoscopy. Tumor destruction (LMS) via APC/Cryo. Balloon dilation.\n[Plan]\nRadiation oncology.",
            
            8: "Mr. Renfield underwent rigid bronchoscopy for a blocked left mainstem bronchus. We first sampled the subcarinal lymph nodes with EBUS. Then, using a combination of techniques including APC and balloon dilation, we opened the obstructed airway. We decided against stenting for now and will refer for radiation.",
            
            9: "Operation: Rigid bronchoscopy with tumor ablation and EBUS. Action: EBUS-TBNA of station 7. Recanalization of Left Mainstem using thermal and mechanical methods. Prosthesis: None."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns the mock data mapping for the 10 notes.
    """
    return [
        {"idx": 0, "orig_name": "Daniel Wilbert Conley", "orig_age": 65, "names": ["James Conley", "Robert Smith", "Michael Johnson", "William Williams", "David Brown", "Richard Jones", "Charles Garcia", "Joseph Miller", "Thomas Davis"]},
        {"idx": 1, "orig_name": "Maizie Booth", "orig_age": 65, "names": ["Mary Wilson", "Linda Moore", "Barbara Taylor", "Susan Anderson", "Jessica Thomas", "Sarah Jackson", "Karen White", "Nancy Harris", "Lisa Martin"]},
        {"idx": 2, "orig_name": "George Martinez", "orig_age": 65, "names": ["Christopher Thompson", "Daniel Martinez", "Paul Robinson", "Mark Clark", "Donald Rodriguez", "George Lewis", "Kenneth Lee", "Steven Walker", "Edward Hall"]},
        {"idx": 3, "orig_name": "Maria Rodriguez", "orig_age": 72, "names": ["Betty Allen", "Dorothy Young", "Sandra Hernandez", "Ashley King", "Kimberly Wright", "Donna Lopez", "Emily Hill", "Michelle Scott", "Carol Green"]},
        {"idx": 4, "orig_name": "Emma Carlisle", "orig_age": 65, "names": ["Amanda Adams", "Melissa Baker", "Deborah Gonzalez", "Stephanie Nelson", "Rebecca Carter", "Laura Mitchell", "Sharon Perez", "Cynthia Roberts", "Kathleen Turner"]},
        {"idx": 5, "orig_name": "Nolan Shepherd", "orig_age": 65, "names": ["Jerry Phillips", "Tyler Campbell", "Aaron Parker", "Henry Evans", "Douglas Edwards", "Peter Collins", "Adam Stewart", "Nathan Sanchez", "Zachary Morris"]},
        {"idx": 6, "orig_name": "Thomas O'Brien", "orig_age": 70, "names": ["Walter Rogers", "Kyle Reed", "Harold Cook", "Arthur Morgan", "Ryan Bell", "Roger Murphy", "Joe Bailey", "Juan Rivera", "Jack Cooper"]},
        {"idx": 7, "orig_name": "Logan Pierce", "orig_age": 65, "names": ["Albert Richardson", "Jonathan Cox", "Justin Howard", "Terry Ward", "Gerald Torres", "Keith Peterson", "Samuel Gray", "Willie Ramirez", "Ralph James"]},
        {"idx": 8, "orig_name": "Harold \"Hal\" Johnson", "orig_age": 74, "names": ["Lawrence Watson", "Nicholas Brooks", "Roy Kelly", "Benjamin Sanders", "Bruce Price", "Brandon Bennett", "Frank Wood", "Scott Barnes", "Eric Ross"]},
        {"idx": 9, "orig_name": "Jacob Renfield", "orig_age": 65, "names": ["Stephen Henderson", "Andrew Coleman", "Raymond Jenkins", "Gregory Perry", "Joshua Powell", "Dennis Long", "Jerry Patterson", "Tyler Hughes", "Aaron Flores"]}
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
                # Fallback if variation is missing
                note_entry["note_text"] = f"[VARIATION MISSING FOR NOTE {idx} STYLE {style_num}]"
            
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
    output_filename = output_dir / "synthetic_part_010_variations.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()