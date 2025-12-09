import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_001.json"
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
        # Note 0: Bronch w/ RFA (CPT 31641, 31627, 31654)
        # Original: RLL nodule, squamous cell CA. ENB + REBUS. RFA 105C x 10min.
        # ---------------------------------------------------------------------
        0: {
            1: "Dx: RLL Nodule.\nProc: Nav bronch, R-EBUS, RFA.\nSteps:\n- GA/ETT.\n- ENB to RLL superior.\n- REBUS confirmed peripheral lesion.\n- RFA probe (RITA) deployed. 105C for 10 min.\n- Zone adequate. No bleed.\nPlan: Extubated. CXR. D/C if stable.",
            
            2: "OPERATIVE REPORT\nINDICATION: Patient presents with a 2.2cm right lower lobe nodule, biopsy-proven squamous cell carcinoma, for ablative therapy.\nPROCEDURE: Electromagnetic navigation bronchoscopy (ENB) with radial endobronchial ultrasound (R-EBUS) localization and radiofrequency ablation (RFA).\nNARRATIVE: Following induction of general anesthesia, the bronchoscope was introduced. The ENB system was utilized to navigate to the superior segment of the right lower lobe. Confirmation of the eccentric lesion was achieved via radial EBUS. The RFA catheter was extended into the lesion. Ablation was performed at a target temperature of 105 degrees Celsius for a duration of 10 minutes. Post-ablation inspection revealed blanching consistent with adequate thermal effect. No immediate complications were noted.",
            
            3: "Code Justification:\n31627 (Navigation): Electromagnetic planning and guidance used to access peripheral RLL target.\n31654 (REBUS): Radial probe ultrasound utilized to confirm target concentricity/location prior to ablation.\n31641 (Destruction): Radiofrequency energy applied (105C, 600s) to destroy malignant tumor tissue.\nEquipment: RITA 1500X generator, navigation catheter, radial US probe.",
            
            4: "Procedure Note\nResident: [Name]\nAttending: [Name]\nProcedure: Bronchoscopy with RFA.\nSteps:\n1. Time out.\n2. ETT placed.\n3. Navigated to RLL nodule using ENB.\n4. Verified with radial EBUS.\n5. RFA performed: 10 min cycle at 105C.\n6. Scope removed.\nNo complications.",
            
            5: "pt here for bronch rfa rll nodule squamous cell we used general anesthesia... navigation system set up and we went to the right lower lobe superior seg found it with the rebus probe... rfa probe put in set to 105 degrees for ten minutes looked good after no bleeding patient woke up fine check cxr tomorrow.",
            
            6: "Pt: Jackson, Dennis. DOB: 9/12/1959. Date: 11/10/2025. Dx: RLL nodule 2.2cm, squamous cell CA. Procedure: Bronch w/ RFA. Under GA, bronchoscopy performed. ENB to RLL superior segment. R-EBUS confirmed target. RFA probe placed (RITA 1500X, 2cm tines). Treatment: 105C x 10min. Good ablation zone. No bleeding, no complications. Extubated, stable. CXR today. CT tomorrow. D/C if OK. F/U 1mo.",
            
            7: "[Indication]\nRLL nodule, 2.2cm squamous cell carcinoma, non-surgical candidate.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nNavigation (ENB) to RLL. Radial EBUS confirmation. Radiofrequency ablation performed (105C, 10 min). Probe removed. Airway patent.\n[Plan]\nCXR, discharge pending stability.",
            
            8: "The patient, Mr. Jackson, underwent a therapeutic bronchoscopy for his RLL squamous cell carcinoma. Under general anesthesia, we utilized electromagnetic navigation to reach the target in the superior segment. We verified the location with radial EBUS. Subsequently, we applied radiofrequency energy at 105 degrees Celsius for ten minutes to ablate the lesion. The procedure was uncomplicated, and the patient was stable upon extubation.",
            
            9: "Under GA, bronchoscopy executed. Guided to RLL superior segment via electromagnetic tracking. R-EBUS verified the lesion. Ablation probe positioned (RITA 1500X). Therapy applied: 105C x 10min. Satisfactory destruction zone. No hemorrhage, no adverse events. Extubated, stable."
        },

        # ---------------------------------------------------------------------
        # Note 1: Tunneled Pleural Catheter (CPT 32550)
        # Original: 74F, metastatic breast ca, recurrent effusion. PleurX placed.
        # ---------------------------------------------------------------------
        1: {
            1: "Indication: Malignant pleural effusion.\nProc: PleurX catheter placement.\nFindings: 1200cc serous fluid removed.\nSteps: US guidance. Local lidocaine. Tunnel created. Catheter inserted. Cuff positioned. Sutured. Drng established.\nPlan: Home drainage education.",
            
            2: "PROCEDURE PERFORMED: Insertion of indwelling tunneled pleural catheter.\nCLINICAL SUMMARY: 74-year-old female with metastatic breast cancer and recurrent symptomatic right pleural effusion. Ultrasound demonstrated a large, anechoic effusion.\nTECHNIQUE: The right hemithorax was prepped. Using ultrasound guidance, the pleural space was accessed at the 5th intercostal space. A subcutaneous tunnel was created. The indwelling catheter (PleurX) was advanced through the peel-away sheath. The cuff was seated within the tunnel. 1.2L of serous fluid was drained. The patient tolerated the procedure well.",
            
            3: "CPT 32550: Insertion of indwelling tunneled pleural catheter with cuff.\nDocumentation of Medical Necessity: Recurrent malignant effusion refractory to thoracentesis.\nDetails: Ultrasound guidance used. Subcutaneous tunneling performed (>5cm). Cuff anchored. Catheter left in situ for intermittent drainage.",
            
            4: "Procedure: Tunneled Pleural Catheter (TPC).\nAttending: Dr. Green.\nSteps:\n1. US marked site.\n2. Local anesthesia.\n3. Wire placed in pleural space.\n4. Tunneler used to create tract.\n5. Catheter inserted/sheath peeled.\n6. 1200ml drained.\n7. Suture closure.\nNo complications.",
            
            5: "proc note pleurx cath placement right side pt has breast ca with fluid... prepped draped used ultrasound found good spot 5th ics lidocaine for numbing... made the tunnel put the cath in got about 1200 mls straw fluid out... stitched it up dressing applied pt did ok no pneumo on post cxr.",
            
            6: "PATIENT: Patricia Johnson. INDICATION: Recurrent malignant pleural effusion. PROCEDURE: Indwelling Tunneled Pleural Catheter Placement. US guidance used. Finder needle entered 5th ICS. Guidewire placed. Tunnel created. Catheter inserted. 1200 mL serous fluid drained. Cuff positioned. Incisions closed. No complications. Catheter functioning well.",
            
            7: "[Indication]\nRecurrent malignant pleural effusion (Breast CA).\n[Anesthesia]\nLocal (Lidocaine 1%).\n[Description]\nUltrasound guided access. Subcutaneous tunnel created. Tunneled catheter placed. 1200mL fluid drained. Cuff seated.\n[Plan]\nHome health teaching for drainage.",
            
            8: "Ms. Johnson presented with a recurrent malignant pleural effusion necessitating durable drainage. We proceeded with the placement of a tunneled pleural catheter. Under ultrasound guidance and local anesthesia, we accessed the pleural space and created a subcutaneous tunnel. The catheter was inserted, and we drained 1200 mL of fluid. The device was secured, and the patient was instructed on home drainage protocols.",
            
            9: "Ms. Johnson underwent successful implantation of a right-sided tunneled pleural catheter for recurrent malignant effusion. Operation concluded without sequelae. Patient and family instructed on catheter maintenance and home drainage protocol. Drainage every other day initially. Follow-up visit in 2 weeks."
        },

        # ---------------------------------------------------------------------
        # Note 2: Robotic Nav Bronch (CPT 31627, 31654, 31628, 31623)
        # Original: 55M, LLL nodule 1.8cm. Ion system. REBUS. Biopsy x6, Brush x2.
        # ---------------------------------------------------------------------
        2: {
            1: "Target: LLL Nodule (1.8cm).\nPlatform: Ion Robotic.\nNav: To LB9. Tool-in-lesion confirmed.\nREBUS: Concentric view.\nSampling: Forceps x6, Brush x2.\nResult: Samples obtained. No complications. Extubated.",
            
            2: "OPERATIVE SUMMARY: Robotic-assisted navigational bronchoscopy was performed for evaluation of a peripheral left lower lobe pulmonary nodule (LB9). Pre-operative CT planning was utilized. The Intuitive Ion catheter was navigated to the target. Radial EBUS confirmed a concentric lesion signal. Three-dimensional spin (Cone Beam CT) verified tool-in-lesion. Transbronchial biopsies (x6) and brushings (x2) were obtained. The patient tolerated the procedure without adverse events.",
            
            3: "Codes Submitted:\n31627: Robotic navigation used to reach peripheral LLL target.\n31654: Radial EBUS probe used for target confirmation.\n31628: Transbronchial biopsies (6 samples) taken from LLL.\n31623: Transbronchial brushing performed at same site.\nMedical Necessity: 1.8cm spiculated nodule, high suspicion for malignancy.",
            
            4: "Procedure: Robotic Bronchoscopy (Ion).\nPatient: Michael Chang.\nSteps:\n1. GA induced.\n2. Registered to CT.\n3. Navigated to LLL lateral basal.\n4. REBUS check: positive.\n5. CBCT spin: tool in lesion.\n6. Biopsies and brushings taken.\nComplications: None.",
            
            5: "robotic bronch for lll nodule 1.8cm... used the ion system navigated to the spot lb9 segment... checked with radial ebus looks concentric... did a spin to confirm tip was in the lesion... took 6 biopsies and 2 brushes all looks good no bleeding... extubated fine.",
            
            6: "PATIENT: Michael Chang. INDICATION: LLL nodule 1.8cm. PROCEDURE: Robotic Navigational Bronchoscopy (Ion), REBUS, Biopsy, Brush. GA/ETT. Navigation to LB9. REBUS concentric. CBCT confirmed tool in lesion. 6 biopsies, 2 brushes obtained. No bleeding. Patient stable. Plan: Pathology f/u.",
            
            7: "[Indication]\nLeft lower lobe nodule, 1.8cm, suspect malignancy.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nRobotic navigation to target. Radial EBUS confirmation. Cone-beam CT verification. Transbronchial biopsy x6. Brushing x2.\n[Plan]\nDischarge home. Follow up pathology.",
            
            8: "Mr. Chang underwent a robotic navigational bronchoscopy to biopsy a 1.8cm nodule in his left lower lobe. We used the Ion system to navigate to the lateral basal segment. Once in position, we confirmed the target with radial EBUS and Cone Beam CT. We successfully obtained six biopsy specimens and two brushings. There were no immediate complications, and he was discharged the same day.",
            
            9: "Mr. Chang underwent successful robotic navigational bronchoscopy with sampling of LLL nodule. Operation finished without sequelae. Post-procedure CXR shows no pneumothorax. Patient released home same day with instructions to follow up in 1 week for pathology results."
        },

        # ---------------------------------------------------------------------
        # Note 3: Medical Thoracoscopy (CPT 32650)
        # Original: 66M, R effusion. Pleural biospy x8, Talc pleurodesis.
        # ---------------------------------------------------------------------
        3: {
            1: "Proc: Med Thoracoscopy w/ Talc.\nFindings: Multiple pleural nodules. Trapped lung.\nAction: Biopsies x8. Adhesiolysis. Talc slurry (4g) insufflated. 28Fr Chest tube placed.\nPlan: Suction. Admit.",
            
            2: "OPERATIVE REPORT: Medical Thoracoscopy.\nThe right hemithorax was entered via the 5th intercostal space. Examination of the pleural cavity revealed extensive nodularity of the parietal and visceral pleura consistent with malignancy. Eight biopsies were obtained. Given the trapped lung physiology, talc pleurodesis (4g) was performed under direct visualization. A chest tube was placed for drainage.",
            
            3: "Coding: 32650 (Thoracoscopy with pleurodesis).\nRationale: Procedure involved diagnostic inspection, biopsies (bundled), and therapeutic introduction of talc for pleurodesis.\nPathology: Pleural nodules biopsied.\nDevice: 28Fr Chest tube left in place.",
            
            4: "Procedure: Pleuroscopy/Medical Thoracoscopy.\nSteps:\n1. Lateral decubitus.\n2. Local + Sedation.\n3. Trocar entry.\n4. Fluid drained (800cc).\n5. Nodules biopsied x8.\n6. Talc poudrage performed.\n7. Chest tube placed.\nEvents: Stable.",
            
            5: "medical thoracoscopy right side... entered 5th space drained bloody fluid... saw lots of nodules took 8 biopsies... lung looked trapped so we did talc pleurodesis 4 grams... put in a chest tube stitched it in place... sending fluid and tissue to path.",
            
            6: "Patient: Harold Stevens. Procedure: Medical thoracoscopy with pleural biopsies, talc pleurodesis. Right hemithorax. 800mL bloody fluid. Multiple nodules visualized. 8 biopsies taken. 4g Talc insufflated. Chest tube placed. Patient tolerated well. Plan: Suction, await path.",
            
            7: "[Indication]\nRecurrent exudative R pleural effusion, suspect malignancy.\n[Anesthesia]\nModerate sedation + Local.\n[Description]\nThoracoscopic entry. 800ml drainage. Pleural biopsies x8. Talc pleurodesis performed. Chest tube placed.\n[Plan]\nAdmit, chest tube management.",
            
            8: "Mr. Stevens underwent a medical thoracoscopy to investigate a right-sided effusion. Upon entering the pleural space, we noted significant nodularity and a trapped lung. We obtained eight biopsies for analysis. To manage the effusion, we performed a talc pleurodesis. A chest tube was secured at the end of the procedure.",
            
            9: "We discussed the need for tissue diagnosis via medical thoracoscopy. Risks including hemorrhage, infection, pneumothorax, need for chest tube, and rare sequelae such as empyema were explained. The patient understood and signed consent."
        },

        # ---------------------------------------------------------------------
        # Note 4: Tracheal Dilation (CPT 31630)
        # Original: 52M, Post-intubation stenosis. Balloon 8-12mm.
        # ---------------------------------------------------------------------
        4: {
            1: "Dx: Tracheal Stenosis (subglottic).\nProc: Bronch w/ Balloon Dilation.\nFindings: 40% narrowing, circumferential scar.\nAction: CRE balloon. Serial inflations 8/10/12mm. Patency improved to 75%.\nPlan: Admit. Decadron.",
            
            2: "PROCEDURE: Flexible bronchoscopy with therapeutic balloon dilation.\nINDICATION: Post-intubation tracheal stenosis.\nFINDINGS: A circumferential stricture was identified 3cm distal to the vocal cords with 40% luminal narrowing. \nINTERVENTION: Sequential balloon dilation was performed using a CRE balloon at diameters of 8mm, 10mm, and 12mm. Post-dilation airway caliber improved to 75% of normal. Minimal mucosal trauma was noted.",
            
            3: "CPT 31630: Bronchoscopy with tracheal/bronchial dilation.\nTechnique: Balloon dilation of tracheal stenosis.\nSpecifics: 3 inflations (max 12mm). Stenosis treated therapeutically. No stent placed.",
            
            4: "Procedure: Airway Dilation.\nAttending: Dr. Patel.\nSteps:\n1. GA induced.\n2. Stenosis identified.\n3. Balloon catheter advanced.\n4. Dilated 8mm, 10mm, 12mm.\n5. Epinephrine applied.\nOutcome: Improved diameter.",
            
            5: "bronch for tracheal stenosis... patient has stridor... saw the narrowing about 3cm down... used the balloon to dilate it up 8 10 then 12 mm... looks much better open about 75 percent now... gave some decadron... observe overnight.",
            
            6: "PT: Garcia, Roberto. INDICATION: Post-intubation tracheal stenosis. PROCEDURE: Flexible bronchoscopy + Balloon dilation. FINDINGS: Stenosis 3cm below cords. INTERVENTION: CRE balloon dilations 8mm, 10mm, 12mm. Patency improved to 75%. No significant bleeding. DISPOSITION: Admit overnight.",
            
            7: "[Indication]\nSymptomatic tracheal stenosis, post-intubation.\n[Anesthesia]\nGeneral.\n[Description]\nBronchoscopy showed 40% stenosis. CRE Balloon dilation x3 (max 12mm). Patency improved to 75%.\n[Plan]\nIV Steroids, Obs.",
            
            8: "Mr. Garcia presented with stridor due to tracheal stenosis. We performed a bronchoscopy under general anesthesia and identified the stricture. Using a balloon catheter, we dilated the area in steps up to 12mm. The airway diameter improved significantly, and the patient tolerated the procedure well.",
            
            9: "Flexible bronchoscopy + Balloon expansion (CPT 31630). SEDATION: Propofol/fentanyl. FINDINGS: Vocal cords: normal mobility. Tracheal stricture at 3cm below glottis. Pre-expansion: ~40% luminal narrowing. INTERVENTION: CRE balloon advanced. Serial expansions performed."
        },

        # ---------------------------------------------------------------------
        # Note 5: PDT (CPT 31641)
        # Original: 71F, L mainstem CA. PDT light application. 200J/cm2.
        # Note: Original text had concatenated note. Variations will focus on PDT.
        # ---------------------------------------------------------------------
        5: {
            1: "Proc: PDT Light Application.\nTarget: L Mainstem SCC.\nDosimetry: 200 J/cm2, 2.5cm diffuser.\nAction: Light delivered 500 sec @ 630nm.\nResponse: No immediate reaction (expected).\nPlan: Light precautions. Debridement in 48h.",
            
            2: "OPERATIVE NOTE: Photodynamic Therapy (Light Activation).\nINDICATION: Endobronchial squamous cell carcinoma, Left Mainstem.\nPROTOCOL: Photofrin 2mg/kg administered 48h prior. \nPROCEDURE: A 2.5cm cylindrical diffuser was positioned across the tumor bed. Laser light at 630nm was delivered to a total fluence of 200 J/cm2 (Total time 500s). The patient tolerated the light activation phase without hemodynamic instability.",
            
            3: "Billing: 31641 (Bronchoscopy with destruction of tumor).\nTechnique: Photodynamic therapy (PDT).\nSpecifics: Laser light delivery to photosensitized tissue (Photofrin). Left mainstem bronchus. Non-thermal ablation.",
            
            4: "Procedure: PDT Light Session.\nSteps:\n1. 48h post-Photofrin.\n2. Bronch to LMS.\n3. Measured tumor.\n4. Placed fiber.\n5. Delivered 200J/cm2 light.\n6. Removed scope.\nPlan: Strict light precautions.",
            
            5: "pdt light treatment for mrs anderson... she got the photofrin 2 days ago... went in with the scope left main tumor is there... put the laser fiber in cooked it for 500 seconds... no bleeding patient ok... remind her about the sunlight precautions.",
            
            6: "Patient: Anderson, Margaret. Procedure: Photodynamic therapy - Light Application. Drug: Photofrin (48h prior). Location: Left Mainstem. Laser: 630nm. Dose: 200 J/cm2. Time: 500s. No complications. Plan: Debridement bronchoscopy in 48 hours.",
            
            7: "[Indication]\nLMS Squamous Cell CA, PDT protocol.\n[Anesthesia]\nGeneral.\n[Description]\nLight application. 630nm laser. 2.5cm diffuser. 200 J/cm2 delivered to tumor.\n[Plan]\nAvoid sunlight 30 days. Return for clean-out.",
            
            8: "Ms. Anderson returned 48 hours after Photofrin injection for light activation. We positioned the diffuser fiber within the left mainstem bronchus tumor. We delivered the calculated light dose of 200 J/cm2. The procedure went smoothly, and she was reminded of strict light precautions upon discharge.",
            
            9: "Photodynamic therapy - laser light application. Flexible bronchoscopy with tumor quantification and documentation. PHOTOSENSITIZER ADMINISTRATION: Agent: Porfimer sodium. Dose: 2 mg/kg IV. Time from photosensitizer to light: 48 hours."
        },

        # ---------------------------------------------------------------------
        # Note 6: Stent Check (CPT 31645)
        # Original: 58F, L main stent. Mucous plugging. Toilet performed.
        # ---------------------------------------------------------------------
        6: {
            1: "Indication: Stent surveillance.\nFindings: 14mm Dumon stent LMS. Patent. Heavy secretions.\nAction: Aggressive suction/toilet. Cleared mucous plugs.\nResult: Stent patent. Airways clear.\nPlan: F/u 4 weeks.",
            
            2: "PROCEDURE: Therapeutic bronchoscopy for airway clearance.\nINDICATION: Surveillance of left mainstem silicone stent.\nFINDINGS: The Dumon stent was in stable position without migration. Significant mucopurulent secretions were noted compromising the lumen. \nINTERVENTION: Extensive bronchial toilet was performed to clear secretions. Post-suctioning, the stent and distal airways were patent. Minor granulation tissue noted proximally, not requiring ablation.",
            
            3: "Code: 31645 (Bronchoscopy with therapeutic aspiration).\nJustification: Patient with indwelling stent presented for check. Procedure required extensive suctioning/toilet to clear obstructing secretions from the initial tracheobronchial tree. Stent inspection included.",
            
            4: "Procedure: Bronchoscopy/Stent Check.\nSteps:\n1. Moderate sedation.\n2. Scope via trach.\n3. Stent visualized in LMS.\n4. Suctioned thick secretions (therapeutic).\n5. Checked positioning.\nPlan: Azithromycin.",
            
            5: "stent check for jennifer... she has that dumon stent in the left main... lots of mucous in there so i spent a while cleaning it out... stent looks good no migration... mild granulation but didnt do anything to it... clean now.",
            
            6: "Patient: Jennifer Wu. Procedure: Bronchoscopy (Stent Check/Toilet). 14mm Dumon stent LMS. Findings: Heavy secretions, stent patent. Action: Aggressive toilet/suction. Result: Clearance of secretions. Plan: Azithromycin x5 days, f/u 4 wks.",
            
            7: "[Indication]\nLMS Stent surveillance, secretion management.\n[Anesthesia]\nModerate.\n[Description]\nScope via trach. Stent inspected. Therapeutic aspiration of copious secretions performed. Stent patent.\n[Plan]\nAntibiotics, increased nebs.",
            
            8: "Ms. Wu came in for a routine check of her left mainstem stent. Upon inspection, we found significant mucous buildup. We performed a therapeutic aspiration to clear the airway. The stent itself remains in good position, and the distal airways are open. We will see her back in a month.",
            
            9: "So Ms. Wu came in today for her routine stent check. She's about 3 months out from when we deployed that 14mm Dumon silicone stent in her left mainstem for malignant compression from lung cancer. She's been doing pretty well overall, no new dyspnea, though she mentioned maybe a bit more cough the last week or so."
        },

        # ---------------------------------------------------------------------
        # Note 7: Cryobiopsy (CPT 31628, 31654)
        # Original: 64F, ILD. Cryo RLL x5. Radial EBUS.
        # ---------------------------------------------------------------------
        7: {
            1: "Indication: ILD diagnosis.\nProc: Cryobiopsy RLL.\nSteps: REBUS checked path. Cryoprobe 2.4mm. 5 samples taken (6s freeze). Blocker used for hemostasis.\nResult: Adequate tissue. No PTX.",
            
            2: "PROCEDURE: Transbronchial cryobiopsy for interstitial lung disease.\nTECHNIQUE: The bronchoscope was advanced to the right lower lobe. Radial EBUS was utilized to ensure a vessel-free biopsy path. The cryoprobe was positioned, and five transbronchial biopsies were obtained using a 6-second freeze time. Prophylactic balloon occlusion (Arndt blocker) was used after each biopsy to ensure hemostasis.",
            
            3: "Codes: 31628 (Transbronchial lung biopsy, single lobe), 31654 (Radial EBUS).\nDetails: Cryoprobe used for parenchymal sampling of RLL. Radial EBUS used for guidance/safety. Endobronchial blocker used for bleed control.",
            
            4: "Procedure: Cryobiopsy.\nSteps:\n1. GA/ETT.\n2. Nav to RLL.\n3. REBUS check.\n4. Cryo activation x5.\n5. Balloon blocker up.\nSamples sent for histopath.",
            
            5: "bronch for ild... went to the rll used the radial ebus to check for vessels... took 5 cryo biopsies with the freezer... used the balloon to stop bleeding worked well... samples look good size... cxr clear.",
            
            6: "PT: Davis, K. DX: ILD. PROC: Bronch w/ transbronchial cryobiopsy RLL. REBUS to RLL lateral basal. 2.4mm cryoprobe. Freeze 6sec x 5 samples. Arndt blocker utilized. Samples 5-8mm. Minimal bleeding. No PTX. IMP: Successful cryobx.",
            
            7: "[Indication]\nILD, tissue dx needed.\n[Anesthesia]\nGeneral.\n[Description]\nRLL targeted. REBUS guidance. Cryobiopsy x5. Hemostasis w/ blocker. No complications.\n[Plan]\nPathology pending.",
            
            8: "Mrs. Davis underwent a cryobiopsy to evaluate her interstitial lung disease. We targeted the right lower lobe, using radial EBUS to ensure safety. Five large biopsies were taken using the cryoprobe. Bleeding was controlled with a balloon blocker. Post-procedure imaging ruled out pneumothorax.",
            
            9: "DX: ILD, UIP pattern on imaging, needs tissue dx. PROC: Bronch w/ transbronchial cryobiopsy RLL (CPT 31632). MEDS: Propofol, fent, roc for intubation. SCOPE FINDINGS: Airways clear, no endo lesions."
        },

        # ---------------------------------------------------------------------
        # Note 8: Bedside Pleurodesis (CPT 32560)
        # Original: 68F, Malignant effusion. Talc slurry via existing chest tube.
        # ---------------------------------------------------------------------
        8: {
            1: "Proc: Chemical Pleurodesis (Bedside).\nAgent: Talc slurry (4g).\nAccess: Existing chest tube.\nSteps: Lidocaine premed. Slurry instilled. Clamped 1hr. Rotated pt. Suction resumed.\nTol: Moderate pain, managed w/ morphine.",
            
            2: "PROCEDURE NOTE: Chemical pleurodesis via thoracostomy tube.\nINDICATION: Recurrent malignant pleural effusion.\nDESCRIPTION: The existing chest tube was verified patent. 4 grams of talc in saline slurry were instilled via the tube. The tube was clamped for 60 minutes while the patient was rotated to ensure distribution. Suction was then re-established. Patient tolerated with appropriate analgesia.",
            
            3: "Code: 32560 (Chemical pleurodesis).\nMethod: Instillation of sclerosing agent (talc) into pleural space via existing chest tube.\nSetting: Bedside/ICU. No thoracoscopy performed.",
            
            4: "Procedure: Talc Pleurodesis.\nSteps:\n1. Checked tube patency.\n2. Pre-medicated.\n3. Instilled lido.\n4. Instilled talc slurry.\n5. Clamped/Rotated.\n6. Unclamped.\nResult: Successful instillation.",
            
            5: "bedside pleurodesis for rebecca... chest tube was draining well so we put the talc in... 4 grams mixed with saline... clamped it for an hour moved her around... she had some pain gave morphine... hooked back to suction draining fluid now.",
            
            6: "Name: Rebecca Martinez. Procedure: Chemical pleurodesis via chest tube. Agent: Talc slurry. Premeds given. Slurry instilled. Dwell time 60 min. Patient rotated. Suction resumed. Tolerance: Moderate discomfort controlled with IV meds. Plan: Monitor output, CXR.",
            
            7: "[Indication]\nMalignant effusion, chest tube in place.\n[Anesthesia]\nLocal/IV Analgesia.\n[Description]\nTalc slurry instilled via tube. Dwell 60 mins. Rotation complete.\n[Plan]\nDaily CXR, remove tube when output low.",
            
            8: "Ms. Martinez underwent bedside pleurodesis for her malignant effusion. Using her existing chest tube, we instilled a talc slurry. She was rotated to distribute the agent. The tube was clamped for an hour and then returned to suction. Pain was managed with IV morphine.",
            
            9: "Step 1 - Verification (Time: 14:00). Verified chest tube patency by flushing with 10mL sterile saline. Confirmed no air leak on water seal. Reviewed most recent CXR with radiologist - confirmed adequate lung expansion. Step 2 - Lidocaine Administration (Time: 14:05)."
        },

        # ---------------------------------------------------------------------
        # Note 9: Hemoptysis/Tamponade (CPT 31634)
        # Original: 57M, Massive hemoptysis. Balloon tamponade LUL.
        # ---------------------------------------------------------------------
        9: {
            1: "Indication: Massive hemoptysis.\nProc: Emergent Bronch.\nFindings: Bleeding from LUL.\nAction: Cold saline lavage. Epi. Fogarty balloon tamponade LUL -> Lingula. Bleeding stopped.\nPlan: ICU, IR consult for BAE.",
            
            2: "PROCEDURE: Emergent bronchoscopy for control of hemorrhage.\nINDICATION: Life-threatening hemoptysis.\nFINDINGS: Active hemorrhage identified originating from the left upper lobe. \nINTERVENTION: Hemostasis was attempted with cold saline and epinephrine lavage with partial response. A Fogarty balloon catheter was deployed to the LUL orifice and inflated, achieving tamponade and cessation of bleeding.\nDISPOSITION: Patient remains intubated in ICU. IR consulted for embolization.",
            
            3: "Code: 31634 (Bronchoscopy with control of hemorrhage).\nTechnique: Balloon tamponade (Fogarty catheter) required to control massive bleeding from LUL. Pharmacologic agents (Epi, TXA) also used.",
            
            4: "Procedure: Emergency Bronch/Bleed Control.\nSteps:\n1. Suctioned airways.\n2. Source LUL.\n3. Lavage/Meds failed.\n4. Balloon blocker placed LUL.\n5. Bleeding controlled.\nPlan: IR Angio.",
            
            5: "called for massive bleed icu bed 8... patient intubated... went down massive blood in trachea... source is left upper lobe... tried saline and epi didnt stop it... put the balloon up in the lul and inflated it... that stopped the bleeding... calling IR now.",
            
            6: "Pt: Marcus Johnson. CALLED FOR: Massive hemoptysis. Findings: Active bleeding LUL. Measures: Iced saline, Epi, TXA - failed. Balloon Tamponade: Fogarty to LUL. Inflated. Bleeding ceased. Plan: IR for embolization.",
            
            7: "[Indication]\nMassive hemoptysis, unstable.\n[Anesthesia]\nGeneral (Ventilated).\n[Description]\nBlood cleared. Source LUL. Balloon tamponade performed. Hemostasis achieved.\n[Plan]\nIR Embolization.",
            
            8: "We performed an emergency bronchoscopy on Mr. Johnson for massive hemoptysis. The source was localized to the left upper lobe. Standard lavage measures failed to control the hemorrhage. We successfully deployed a balloon catheter to tamponade the bleeding vessel. He is currently stable and awaiting IR intervention.",
            
            9: "EMERGENCY BRONCHOSCOPY - HEMOPTYSIS. 10/23/24 - 02:35AM. Pt: Marcus Johnson, 57M, MRN 1923847. CALLED FOR: Massive hemoptysis, ICU bed 8. Got called by ICU resident at 2am - patient with known left upper lobe cavitary lesion (likely TB vs fungal) started having massive hemoptysis."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns the mock data mapping for the 10 notes.
    """
    return [
        {"idx": 0, "orig_name": "Dennis Jackson", "orig_age": 66, "names": ["James Smith", "Robert Brown", "Michael Miller", "William Davis", "David Garcia", "Richard Rodriguez", "Charles Wilson", "Joseph Martinez", "Thomas Anderson"]},
        {"idx": 1, "orig_name": "Patricia Johnson", "orig_age": 74, "names": ["Mary Jones", "Linda Taylor", "Barbara Thomas", "Susan Hernandez", "Jessica Moore", "Sarah Martin", "Karen Jackson", "Nancy Thompson", "Lisa White"]},
        {"idx": 2, "orig_name": "Michael Chang", "orig_age": 55, "names": ["Christopher Lee", "Daniel Lopez", "Paul Harris", "Mark Clark", "Donald Lewis", "George Robinson", "Kenneth Walker", "Steven Perez", "Edward Hall"]},
        {"idx": 3, "orig_name": "Harold Stevens", "orig_age": 66, "names": ["Brian Young", "Ronald Allen", "Anthony King", "Kevin Wright", "Jason Scott", "Matthew Torres", "Gary Nguyen", "Timothy Hill", "Jose Flores"]},
        {"idx": 4, "orig_name": "Roberto Garcia", "orig_age": 52, "names": ["Larry Green", "Jeffrey Adams", "Frank Nelson", "Scott Baker", "Eric Hall", "Stephen Rivera", "Andrew Campbell", "Raymond Mitchell", "Gregory Carter"]},
        {"idx": 5, "orig_name": "Margaret Anderson", "orig_age": 71, "names": ["Betty Roberts", "Dorothy Phillips", "Sandra Evans", "Ashley Turner", "Kimberly Diaz", "Donna Parker", "Emily Cruz", "Michelle Edwards", "Carol Collins"]},
        {"idx": 6, "orig_name": "Jennifer Wu", "orig_age": 58, "names": ["Amanda Stewart", "Melissa Sanchez", "Deborah Morris", "Stephanie Rogers", "Rebecca Reed", "Laura Cook", "Sharon Morgan", "Cynthia Bell", "Kathleen Murphy"]},
        {"idx": 7, "orig_name": "K Davis", "orig_age": 64, "names": ["Amy Bailey", "Shirley Rivera", "Angela Cooper", "Helen Richardson", "Anna Cox", "Brenda Howard", "Pamela Ward", "Nicole Torres", "Samantha Peterson"]},
        {"idx": 8, "orig_name": "Rebecca Martinez", "orig_age": 68, "names": ["Katherine Gray", "Virginia Ramirez", "Debra James", "Rachel Watson", "Janet Brooks", "Emma Kelly", "Christine Sanders", "Carolyn Price", "Maria Bennett"]},
        {"idx": 9, "orig_name": "Marcus Johnson", "orig_age": 57, "names": ["Joshua Wood", "Dennis Barnes", "Jerry Ross", "Tyler Henderson", "Aaron Coleman", "Henry Jenkins", "Douglas Perry", "Peter Powell", "Adam Long"]}
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
                # Fallback if variation is missing (should not happen with complete map)
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
    output_filename = output_dir / "synthetic_part_001_variations.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()