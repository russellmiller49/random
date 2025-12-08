import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements (Bronchial Thermoplasty Notes)
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_070.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-7) -> Style_Index (1-9) -> Text
    variations = {
        0: { # Amelia Green (Session 1: RLL)
            1: "Pre-op: Severe asthma. \nProcedure: RLL Thermoplasty.\nAction: Alair catheter to RLL segments. 52 activations delivered. Good contact/blanching.\nComplications: Mild wheeze, no desat.\nPlan: D/C home. Prednisone burst.",
            2: "HISTORY: Ms. Green, a 44-year-old female with refractory asthma, presented for the initial stage of bronchial thermoplasty targeting the right lower lobe.\nPROCEDURE: Under moderate sedation, the bronchial tree was mapped. The Alair system was deployed into the basilar and superior segments of the RLL. Fifty-two radiofrequency activations were systematically delivered, resulting in characteristic mucosal blanching. \nCOMPLICATIONS: Transient bronchospasm was noted intraoperatively, resolving spontaneously.\nDISPOSITION: The patient was discharged in stable condition with instructions for a corticosteroid taper.",
            3: "Procedure: Bronchial Thermoplasty, single lobe (CPT 31660).\nTarget: Right Lower Lobe (RLL).\nTechnique: Flexible bronchoscopy. Alair catheter positioned in distal segmental bronchi. RF energy applied.\nUtilization: 52 distinct activations delivered to treat airway smooth muscle.\nMedical Necessity: Severe persistent asthma (J45.50) refractory to maximal medical therapy.\nOutcome: Procedure completed without significant adverse event.",
            4: "Procedure: Bronchial Thermoplasty (RLL)\nAttending: Dr. Grant\nSteps:\n1. Time out. Mod sedation.\n2. Airway inspection: clear.\n3. Catheter to RLL.\n4. 52 activations delivered to segments/subsegments.\n5. Suctioned secretions.\nComplications: Mild cough.\nPlan: Discharge, return for LLL in 3 weeks.",
            5: "patient amelia green here for first thermoplasty right lower lobe severe asthma moderate sedation used. went down with the scope no issues anatomy looks normal. put the catheter in the RLL did about 52 hits with the rf energy got good blanching. she coughed a bit and wheezed but sat stayed up no big deal. sent to recovery will go home on prednisone thanks.",
            6: "Bronchial thermoplasty session 1 treating right lower lobe performed on 44-year-old female with severe persistent asthma. Moderate sedation utilized. Flexible bronchoscope advanced. Bronchial thermoplasty catheter deployed to segmental and subsegmental branches of the right lower lobe. Approximately 52 radiofrequency activations were delivered with good contact and visible airway wall blanching. Mild transient wheezing and cough during activations. Observed in recovery and discharged home on prednisone burst.",
            7: "[Indication]\nSevere persistent asthma, frequent exacerbations, maximal therapy.\n[Anesthesia]\nModerate sedation (Midazolam/Fentanyl).\n[Description]\nScope to RLL. Alair catheter deployment. 52 activations delivered to RLL segments. Visible blanching confirmed.\n[Plan]\nDischarge home. Prednisone taper. Return 3 weeks for LLL.",
            8: "Ms. Green presented for her first bronchial thermoplasty session targeting the right lower lobe. After inducing moderate sedation, we advanced the bronchoscope and inspected the airway. We then utilized the thermoplasty catheter to treat the segmental and subsegmental airways of the RLL, delivering a total of 52 activations. We observed good tissue effect with blanching. The patient experienced some mild coughing during the energy delivery but remained stable throughout. She was discharged after a period of observation.",
            9: "Operation: Bronchial thermoplasty, initial session, right lower lobe.\nSubject: Amelia Green, 44.\nDetails: The bronchoscope was navigated to the RLL. The thermal catheter was situated in the segmental branches. Approximately 52 RF pulses were administered, achieving tissue whitening. Secretions were aspirated.\nAdverse Events: Minor temporary wheezing.\nStrategy: Release to home with steroid regimen."
        },
        1: { # Noah King (Session 1: RLL)
            1: "Dx: Severe asthma.\nAnesthesia: GA, ETT.\nTarget: RLL.\nAction: 49 activations via Alair system. \nFindings: Patent airways, no edema.\nIssues: None.\nPlan: Extubate, D/C home.",
            2: "INDICATION: Mr. King presents with severe, biologic-refractory asthma for RLL bronchial thermoplasty.\nOPERATIVE REPORT: General anesthesia was induced and the airway secured. The right lower lobe bronchi were systematically treated utilizing the Alair thermoplasty system. A total of 49 activations were successfully delivered to the segmental and subsegmental airways, adhering to standard temperature and duration parameters. Post-treatment inspection revealed patent airways.\nCONCLUSION: Uncomplicated RLL thermoplasty.\nPLAN: Steroid taper and scheduled follow-up for the left side.",
            3: "Code: 31660 (Bronchial Thermoplasty, 1 lobe).\nLobe Treated: Right Lower Lobe.\nDevice: Alair System.\nActivations: 49.\nSetting: Bronchoscopy suite, General Anesthesia.\nJustification: Treatment of airway smooth muscle for severe asthma. No additional bronchoscopic procedures (biopsy/lavage) performed.",
            4: "Resident Note\nPatient: Noah King\nProcedure: BT Session 1 (RLL)\nSteps:\n1. GA induced. ETT placed.\n2. Scope to RLL.\n3. Systematically treated RLL segments with Alair catheter.\n4. Total 49 activations.\n5. Re-inspected: No bleeding/edema.\nPlan: Extubate, discharge.",
            5: "procedure note for noah king he has bad asthma biologic failure. doing the rll thermoplasty today under ga. tube in scope down. went to the right lower lobe did the activations got 49 of them in. looks patent no bleeding or spasm. woke him up fine sent to recovery. discharge later today on steroids.",
            6: "Interventional Pulmonology Procedure Note. Procedure: Bronchial thermoplasty session 1 treating right lower lobe. Patient: Noah King, 50-year-old male. Anesthesia: General anesthesia with endotracheal intubation. Flexible bronchoscope passed through endotracheal tube. Bronchial thermoplasty catheter sequentially positioned in segmental and subsegmental right lower lobe bronchi. Forty-nine activations delivered respecting manufacturer-specified temperature. Airways inspected post-treatment and noted to be patent. No significant intra-procedural bronchospasm. Extubated and discharged.",
            7: "[Indication]\nSevere asthma uncontrolled on biologics.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nRLL cannulated. 49 activations delivered to RLL segments using Alair catheter. Airways patent post-procedure.\n[Plan]\nDischarge home. Return 2-3 weeks for LLL.",
            8: "Mr. King underwent his first bronchial thermoplasty session today for the right lower lobe. We placed him under general anesthesia for patient comfort and airway control. Using the flexible bronchoscope, we targeted the RLL segments and delivered 49 separate activations of radiofrequency energy. The airways looked good immediately after treatment with no signs of trauma. He was extubated in the room and will go home today with a steroid taper.",
            9: "Procedure: Bronchial thermoplasty, phase 1, right lower lobe.\nPatient: Noah King.\nMethod: Under general anesthesia, the scope was guided through the ETT. The thermal probe was sequentially placed in the RLL bronchi. Forty-nine pulses were discharged. Airways were examined and found open.\nComplications: Nil.\nDisposition: Extubated and released."
        },
        2: { # Amelia Green (Session 2: LLL)
            1: "Hx: Post-RLL BT (3 wks ago).\nProc: LLL Thermoplasty.\nSedation: MAC (Propofol).\nDetails: 48 activations to LLL segments.\nComplications: None.\nPlan: D/C home. Return for upper lobes.",
            2: "INTERVAL HISTORY: Ms. Green returns for the second stage of bronchial thermoplasty (Left Lower Lobe) three weeks following uncomplicated RLL treatment.\nPROCEDURE: Under monitored anesthesia care, the left bronchial tree was accessed. The Alair catheter was advanced into the LLL. Forty-eight radiofrequency activations were distributed evenly throughout the segmental anatomy. Visual inspection confirmed appropriate tissue effect without charring or bleeding.\nIMPRESSION: Successful LLL thermoplasty (Session 2).",
            3: "Service: Bronchoscopy with Bronchial Thermoplasty (31660).\nAnatomy: Left Lower Lobe (1 lobe treated).\nDosimetry: 48 activations.\nAnesthesia: MAC.\nNote: This represents the second session in the standard 3-session protocol (RLL -> LLL -> Bilateral Upper).",
            4: "Procedure: BT Session 2 (LLL)\nPatient: Amelia Green\nSteps:\n1. MAC sedation.\n2. Scope to LLL.\n3. Treated all accessible LLL segments.\n4. Count: 48 activations.\n5. No trauma noted.\nPlan: Home today. S/p 4 hours obs.",
            5: "amelia green back for round two left lower lobe this time. used propofol for sedation. went into the LLL and did the thermoplasty. got 48 activations in there. everything looks good no bleeding no spasm. she can go home after observation same plan as last time.",
            6: "Bronchial thermoplasty session 2 treating left lower lobe performed on Amelia Green. Sedation: Monitored anesthesia care with propofol infusion. Flexible bronchoscope advanced to the left lower lobe. The thermoplasty catheter was advanced into segmental and subsegmental branches, and 48 activations were delivered evenly throughout the left lower lobe. No lavage, biopsy, or additional interventions. No significant bronchospasm. Recovered uneventfully and discharged.",
            7: "[Indication]\nStaged BT, session 2 (LLL).\n[Anesthesia]\nMAC (Propofol).\n[Description]\nScope to LLL. 48 activations delivered via Alair system. Good distribution. No trauma.\n[Plan]\nDischarge. Return 3 weeks for Upper Lobes.",
            8: "Ms. Green returned today for the treatment of her left lower lobe, having recovered well from the first session. Under MAC sedation, we navigated to the left side and treated the LLL segments. We delivered a total of 48 activations. The procedure went smoothly with no coughing or bleeding. She is set to return in a few weeks for the final session treating the upper lobes.",
            9: "Operation: Bronchial thermoplasty, second stage, left lower lobe.\nPatient: Amelia Green.\nAction: The scope was directed to the LLL. The RF catheter was inserted into the subsegments. 48 energy pulses were applied. No additional maneuvers performed.\nOutcome: No bronchospasm.\nPlan: Release to home."
        },
        3: { # Noah King (Session 2: LLL)
            1: "Proc: LLL BT (Session 2).\nAnesthesia: GA, ETT.\nAction: 50 activations to LLL.\nFindings: Good blanching. No injury.\nComp: Post-proc cough only.\nPlan: D/C home.",
            2: "PROCEDURE NOTE: Bronchial Thermoplasty, Session 2 (Left Lower Lobe).\nPATIENT: Mr. King, 50M.\nTECHNIQUE: Following induction of general anesthesia, the bronchoscope was advanced. The left lower lobe was systematically treated. Fifty activations were delivered to the basilar and superior segments. Post-treatment bronchoscopic inspection revealed no evidence of thermal injury beyond expected blanching. No bleeding or edema was observed.\nDISPOSITION: The patient was extubated and transferred to recovery in stable condition.",
            3: "CPT: 31660 (Thermoplasty, 1 lobe).\nSite: Left Lower Lobe.\nQuantity: 50 activations.\nModality: Radiofrequency energy ablation of airway smooth muscle.\nContext: Session 2 of 3.\nComplications: None reported.",
            4: "Resident Note\nPatient: Noah King\nProcedure: BT LLL\nSteps:\n1. ETT placed (GA).\n2. Navigated to LLL.\n3. Performed 50 activations.\n4. Checked airway: clear.\n5. Suctioned.\nPlan: Extubate, home.",
            5: "noah king here for session 2 left lower lobe. general anesthesia again. went down with the scope treated the lll segments. 50 hits total. airway looks fine just a little cough after we pulled the tube. sending him home today.",
            6: "Interventional Pulmonology Procedure Note. Procedure: Bronchial thermoplasty session 2 treating left lower lobe. General anesthesia with endotracheal tube. Flexible bronchoscopy performed. Bronchial thermoplasty catheter positioned in left lower lobe segmental and subsegmental bronchi. Fifty activations delivered with adequate contact. No lavage or biopsies. None beyond expected post-procedure cough. Extubated and discharged.",
            7: "[Indication]\nSevere asthma, Session 2 (LLL).\n[Anesthesia]\nGeneral, ETT.\n[Description]\n50 activations delivered to LLL. Catheter contact good. No injury.\n[Plan]\nDischarge. Return for final session (Upper Lobes).",
            8: "Mr. King underwent the second stage of his thermoplasty treatment today, focusing on the left lower lobe. Under general anesthesia, we treated the LLL airways with 50 activations of the device. We saw the expected whitening of the airway walls but no charring or bleeding. He woke up with a mild cough but is otherwise doing well and will go home today.",
            9: "Procedure: Bronchial thermoplasty, session two, left lower lobe.\nSubject: Noah King.\nTechnique: Under general anesthesia, the probe was situated in the LLL. Fifty discharges of RF energy were completed. Airways were reviewed and found patent.\nResult: Minor cough.\nPlan: Outpatient release."
        },
        4: { # Amelia Green (Session 3: Bilateral Upper)
            1: "Proc: BT Session 3 (RUL/LUL).\nAnesthesia: GA, LMA.\nAction: 60 activations total (30 RUL, 30 LUL).\nFindings: Stable pressures. No trauma.\nPlan: Admit overnight (standard protocol).",
            2: "PROCEDURE: Completion Bronchial Thermoplasty (Bilateral Upper Lobes).\nCLINICAL SUMMARY: Ms. Green presents for the final session targeting the RUL and LUL.\nOPERATIVE DETAILS: A laryngeal mask airway was placed. The bronchoscope was advanced to the right upper lobe, where approximately 30 activations were delivered. Attention was turned to the left upper lobe, where an additional 30 activations were performed (Total: 60). Airway inspection showed expected blanching with no excessive edema.\nDISPOSITION: The patient was admitted to the pulmonary floor for routine overnight observation given the extent of the treated area (2 lobes).",
            3: "Code: 31661 (Bronchial thermoplasty, 2 or more lobes).\nTarget: Right Upper Lobe AND Left Upper Lobe.\nActivations: 60 total.\nRationale: This code captures the increased work and risk of treating multiple lobes in the final session of the standard protocol.\nSetting: Inpatient admission (Overnight).",
            4: "Resident Note\nPatient: Amelia Green\nProcedure: BT Session 3 (Upper Lobes)\nSteps:\n1. GA with LMA.\n2. Treated RUL (~30 hits).\n3. Treated LUL (~30 hits).\n4. Total 60 activations.\n5. No desats.\nPlan: Admit for obs.",
            5: "amelia green here for the final session upper lobes. used an lma and general anesthesia. treated the right upper then the left upper. about 30 hits each side so 60 total. went well no spasm. admitting her overnight just to watch her like usual for the upper lobes.",
            6: "Bronchial thermoplasty session 3 treating bilateral upper lobes. Patient: Amelia Green. Anesthesia: General anesthesia with laryngeal mask airway. Thermoplasty catheter advanced sequentially to the right and left upper lobe segmental and subsegmental bronchi. Total of 60 activations delivered (approximately 30 per upper lobe) with stable airway pressures. Mild post-procedure cough only. Recovered in PACU and admitted overnight.",
            7: "[Indication]\nCompletion BT (RUL + LUL).\n[Anesthesia]\nGeneral, LMA.\n[Description]\nSequential treatment of RUL and LUL. 60 total activations delivered. Airway appearance satisfactory.\n[Plan]\nAdmit overnight. Monitor for edema.",
            8: "Ms. Green came in for her final thermoplasty session. We treated both the right and left upper lobes today under general anesthesia. We did about 30 activations on each side for a total of 60. The procedure went very smoothly with no breathing issues noted. Because we treated two lobes, we are keeping her in the hospital overnight for observation as per protocol.",
            9: "Operation: Bronchial thermoplasty, final stage, bilateral upper lobes.\nPatient: Amelia Green.\nMethod: Via LMA, the catheter was deployed in the RUL and LUL. 60 energy pulses were administered in total. No airway trauma observed.\nOutcome: Minor cough.\nStrategy: Inpatient monitoring."
        },
        5: { # Noah King (Session 3: Bilateral Upper)
            1: "Proc: BT Session 3 (RUL + LUL).\nAnesthesia: GA, ETT.\nAction: 58 activations total to upper lobes.\nFindings: Patent airways. No spasm.\nPlan: Admit step-down. Steroid taper.",
            2: "PROCEDURE: Bilateral Upper Lobe Bronchial Thermoplasty.\nPATIENT: Mr. King, 50M.\nNARRATIVE: The patient was intubated. The RUL and LUL segmental bronchi were sequentially identified and treated. A total of 58 radiofrequency activations were applied. The procedure was uncomplicated, with no evidence of bronchospasm or bleeding. Post-procedure airway inspection confirmed patency.\nDISPOSITION: The patient was transferred to the step-down unit for overnight monitoring and initiation of a systemic steroid taper.",
            3: "Code: 31661 (Bronchial thermoplasty, 2 or more lobes).\nSites: Right Upper Lobe, Left Upper Lobe.\nActivations: 58.\nAnesthesia: General (ETT).\nStatus: Procedure completed successfully. No complications recorded.\nDisposition: Inpatient (Step-down).",
            4: "Resident Note\nPatient: Noah King\nProcedure: BT Bilateral Upper Lobes\nSteps:\n1. Intubation.\n2. Treated RUL segments.\n3. Treated LUL segments.\n4. Total 58 activations.\n5. No issues.\nPlan: Admit to step-down, steroids.",
            5: "noah king final session upper lobes. tube is in. went to the rul and lul. did 58 activations total. everything looks good no spasm or anything. sending him to step down for the night will taper his steroids.",
            6: "Interventional Pulmonology Procedure Note. Procedure: Bronchial thermoplasty session 3 treating bilateral upper lobes. Patient: Noah King. General anesthesia with endotracheal intubation. Flexible bronchoscopy performed via endotracheal tube. Bronchial thermoplasty catheter sequentially deployed in the right and left upper lobe segmental bronchi. Fifty-eight activations delivered. Airways re-inspected and remained hemostatic and patent. Admitted overnight to the step-down unit.",
            7: "[Indication]\nCompletion BT (RUL + LUL).\n[Anesthesia]\nGeneral, ETT.\n[Description]\nRUL and LUL treated. 58 activations total. Good contact. Airways patent.\n[Plan]\nAdmit step-down. Systemic steroid taper.",
            8: "Mr. King finished his thermoplasty treatment today with the upper lobes. Under general anesthesia, we treated segments in both the right and left upper lobes, delivering 58 activations in total. He tolerated it well with no bronchospasm. We are admitting him to the step-down unit for tonight just to be safe and will start his steroid taper.",
            9: "Procedure: Bronchial thermoplasty, conclusion, bilateral upper lobes.\nSubject: Noah King.\nAction: Using an ETT, the probe was positioned in the RUL and LUL. 58 RF discharges were completed. Airways remained open.\nResult: No immediate bronchospasm.\nDisposition: Step-down unit admission."
        },
        6: { # Sofia Martinez (Session 2: LLL + Complication)
            1: "Proc: LLL Thermoplasty.\nEvent: Severe bronchospasm/desat at 45 activations.\nAction: Procedure paused. Rx: Albuterol, Mg, Solu-Medrol.\nOutcome: Sats improved. No intubation needed.\nPlan: Admit pulmonary floor. Close monitoring.",
            2: "PROCEDURE: Bronchial Thermoplasty (Left Lower Lobe).\nCOMPLICATION: The procedure was complicated by moderate intra-operative bronchospasm after 45 activations. The patient desaturated to 88%. The procedure was paused. Pharmacologic rescue with nebulized albuterol, IV magnesium, and IV methylprednisolone was successful in restoring baseline saturation without the need for invasive ventilation.\nDISPOSITION: The patient was admitted to the pulmonary floor for close observation.",
            3: "Code: 31660 (Bronchial thermoplasty, 1 lobe).\nLobe: Left Lower Lobe.\nActivations: 45 (Goal not fully met due to adverse event).\nComplication: Intra-procedural bronchospasm (J98.01) requiring medical management.\nNote: Despite complication, the base procedure code 31660 is reported as the service was performed substantially.",
            4: "Resident Note\nPatient: Sofia Martinez\nProcedure: BT LLL\nEvents:\n1. Started LLL treatment.\n2. At 45 hits, patient got tight/wheezy.\n3. Sats dropped to 88%.\n4. Stopped. Gave nebs, mg, steroids.\n5. Improved.\nPlan: Admit to floor.",
            5: "sofia martinez here for LLL thermoplasty. shes pretty brittle. we got through 45 activations and she clamped down hard. sats dropped into the 80s. had to stop. gave her everything albuterol mag steroids. she opened up eventually didnt have to tube her. keeping her on the floor tonight definitely.",
            6: "Interventional Pulmonology Procedure Note. Bronchial thermoplasty session 2 treating left lower lobe. Patient: Sofia Martinez. Sedation: Moderate. Flexible bronchoscopy performed. Thermoplasty catheter advanced to left lower lobe. Forty-five activations delivered; procedure briefly paused because of increased airway resistance and wheeze. Moderate intra-procedural bronchospasm with transient desaturation to 88% managed with inhaled albuterol, IV magnesium, and IV methylprednisolone. Observed overnight on the pulmonary floor.",
            7: "[Indication]\nSevere asthma, Session 2 (LLL).\n[Anesthesia]\nModerate Sedation.\n[Description]\n45 activations delivered to LLL. Procedure paused due to bronchospasm and desaturation (88%). Medical management successful (Albuterol/Mg/Steroids).\n[Plan]\nAdmit to floor. Scheduled nebs.",
            8: "Ms. Martinez had a rough time with her LLL thermoplasty today. We managed to deliver 45 activations, but then she developed significant bronchospasm and her oxygen levels dropped. We had to stop and treat her aggressively with nebs and IV meds. Fortunately, she turned around and we didn't have to intubate her. We are admitting her to the floor to keep a close eye on her breathing.",
            9: "Procedure: Bronchial thermoplasty, session two, left lower lobe.\nPatient: Sofia Martinez.\nComplication: Intra-operative airway constriction.\nDetails: After 45 pulses, the patient exhibited wheezing and hypoxemia. The session was suspended. Pharmacologic rescue was effective.\nDisposition: Inpatient observation."
        },
        7: { # Liam Patel (Session 3: Bilateral Upper Aborted)
            1: "Proc: Attempted BT Bilateral Upper Lobes.\nEvent: Severe bronchospasm at 34 activations.\nAction: Aborted procedure. Intubated. ICU transfer.\nFindings: Acute respiratory failure.\nPlan: ICU care. Mech vent.",
            2: "OPERATIVE NARRATIVE: The patient presented for completion thermoplasty of the upper lobes. Following induction, the catheter was deployed in the RUL and LUL. After 34 activations, the patient developed precipitous airway expiratory obstruction and severe wheeze consistent with status asthmaticus. \nINTERVENTION: The procedure was immediately aborted. Anesthesia was deepened, and pharmacologic resuscitation initiated. The patient remained intubated for mechanical ventilation.\nDISPOSITION: Transfer to ICU for critical care management.",
            3: "Code: 31660 (Bronchial thermoplasty, 1 lobe).\nRationale: Although bilateral treatment was intended (31661), the procedure was aborted early due to life-threatening bronchospasm. 34 activations suggests treatment of roughly one lobe's worth of tissue before termination.\nComplication: Acute respiratory failure (J96.00).\nDisposition: ICU.",
            4: "Resident Note\nPatient: Liam Patel\nProcedure: BT Upper Lobes (Aborted)\nEvents:\n1. Started treatment RUL/LUL.\n2. Got to 34 hits.\n3. Huge bronchospasm, high pressures.\n4. Stopped procedure.\n5. Patient stayed intubated, went to ICU.\nPlan: ICU vent management.",
            5: "liam patel here for the last session upper lobes. started fine but at 34 hits he just clamped off totally. pressures went sky high severe wheeze. we had to stop. kept him asleep and intubated. sent him straight to the icu. scary case.",
            6: "Interventional Pulmonology Procedure Note. Procedure: Bronchial thermoplasty session 3 treating bilateral upper lobes (aborted early). Patient: Liam Patel. General anesthesia with endotracheal intubation. Bronchial thermoplasty catheter positioned in right and left upper lobe segmental bronchi. Thirty-four activations delivered before abrupt increase in airway pressures and severe wheeze prompted early termination. Severe bronchospasm with acute hypoxemic respiratory failure. Procedure aborted; patient transported intubated to the ICU.",
            7: "[Indication]\nCompletion BT (Upper Lobes).\n[Anesthesia]\nGeneral, ETT.\n[Description]\nCatheter deployed. 34 activations delivered. Severe bronchospasm encountered. Procedure aborted.\n[Complications]\nAcute respiratory failure. Intubated.\n[Plan]\nICU admission. Mechanical ventilation.",
            8: "Mr. Patel's procedure had to be stopped early today. We were treating the upper lobes and had delivered 34 activations when he went into severe bronchospasm. His airway pressures spiked and we couldn't ventilate him well. We stopped the thermoplasty immediately and focused on stabilizing him. He is currently intubated and sedated in the ICU.",
            9: "Procedure: Bronchial thermoplasty, final stage, upper lobes (Terminated).\nPatient: Liam Patel.\nEvent: During the 34th pulse, acute airway obstruction occurred. The operation was ceased.\nAction: Deepened sedation, administered epinephrine.\nOutcome: Patient remains mechanically ventilated.\nDisposition: Intensive Care Unit."
        }
    }
    return variations

def get_base_data_mocks():
    # Names corresponding to the 9 styles for the 8 patients found in the input
    return [
        # Note 0: Amelia Green (44)
        {"idx": 0, "orig_name": "Amelia Green", "orig_age": 44, "names": ["Anna White", "Margaret Davis", "Susan Clark", "Jennifer Hall", "Lisa Allen", "Karen Wright", "Nancy King", "Betty Scott", "Sandra Green"]},
        # Note 1: Noah King (50)
        {"idx": 1, "orig_name": "Noah King", "orig_age": 50, "names": ["Oliver Scott", "William Baker", "James Nelson", "Robert Carter", "Michael Mitchell", "David Roberts", "Richard Phillips", "Charles Campbell", "Joseph Anderson"]},
        # Note 2: Amelia Green (44) - Session 2
        {"idx": 2, "orig_name": "Amelia Green", "orig_age": 44, "names": ["Anna White", "Margaret Davis", "Susan Clark", "Jennifer Hall", "Lisa Allen", "Karen Wright", "Nancy King", "Betty Scott", "Sandra Green"]},
        # Note 3: Noah King (50) - Session 2
        {"idx": 3, "orig_name": "Noah King", "orig_age": 50, "names": ["Oliver Scott", "William Baker", "James Nelson", "Robert Carter", "Michael Mitchell", "David Roberts", "Richard Phillips", "Charles Campbell", "Joseph Anderson"]},
        # Note 4: Amelia Green (44) - Session 3
        {"idx": 4, "orig_name": "Amelia Green", "orig_age": 44, "names": ["Anna White", "Margaret Davis", "Susan Clark", "Jennifer Hall", "Lisa Allen", "Karen Wright", "Nancy King", "Betty Scott", "Sandra Green"]},
        # Note 5: Noah King (50) - Session 3
        {"idx": 5, "orig_name": "Noah King", "orig_age": 50, "names": ["Oliver Scott", "William Baker", "James Nelson", "Robert Carter", "Michael Mitchell", "David Roberts", "Richard Phillips", "Charles Campbell", "Joseph Anderson"]},
        # Note 6: Sofia Martinez (39)
        {"idx": 6, "orig_name": "Sofia Martinez", "orig_age": 39, "names": ["Isabella Garcia", "Sophia Rodriguez", "Mia Lopez", "Elena Perez", "Gabriella Sanchez", "Maria Rivera", "Victoria Torres", "Camila Ramirez", "Natalia Flores"]},
        # Note 7: Liam Patel (56)
        {"idx": 7, "orig_name": "Liam Patel", "orig_age": 56, "names": ["Lucas Singh", "Ethan Sharma", "Aiden Gupta", "Mason Kumar", "Logan Verma", "Jacob Shah", "Elijah Joshi", "Benjamin Jain", "Alexander Mehta"]}
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
            
            # Update note_text with the variation if available
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                # Fallback if variation missing
                note_entry["note_text"] = f"[VARIATION MISSING FOR IDX {idx} STYLE {style_num}]"
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
                
                # IMPORTANT: Keep the note_text inside registry_entry synced
                if "note_text" in note_entry["registry_entry"]:
                     note_entry["registry_entry"]["note_text"] = note_entry["note_text"]

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
    output_filename = output_dir / "synthetic_bt_notes_part_070.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()