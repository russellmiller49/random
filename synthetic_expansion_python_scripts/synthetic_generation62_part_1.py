import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_062_part1.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the manually crafted text variations.
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Thomas Keller (Rigid Bronch LMS, SCC)
            1: "Dx: LMS SCC, 90% obstruction.\nProc: Rigid bronch (31640).\nAction: Mechanical coring/debulking w/ microdebrider.\nNo thermal ablation.\nResult: <20% residual obstruction.\nEBL: 25mL.\nPlan: ICU.",
            2: "OPERATIVE NARRATIVE: Mr. Keller, a 67-year-old male with biopsy-proven squamous cell carcinoma, presented with critical left mainstem (LMS) obstruction. Under general anesthesia utilizing a rigid bronchoscope, the airway was interrogated. An exophytic, friable tumor causing 90% occlusion was identified. We proceeded with mechanical tumor excision via rigid coring and microdebrider assistance. The obstructing tissue was removed piecemeal without the use of thermal energy. Post-intervention, the lumen was widely patent with less than 20% residual stenosis.",
            3: "CPT Selection: 31640 (Bronchoscopy with excision of tumor).\nMedical Necessity: 90% malignant obstruction of Left Mainstem.\nTechnique: Rigid bronchoscopy used to mechanically core and excise tumor. Microdebrider utilized for fine debulking. \nNote: No thermal ablation codes (31641) applicable as only mechanical tools were used.",
            4: "Procedure: Rigid Bronchoscopy / Debulking\nAttending: Dr. Brennan\nSteps:\n1. Induced GA.\n2. Intubated with rigid scope.\n3. Identified LMS tumor (SCC).\n4. Performed mechanical debulking using rigid bevel and microdebrider.\n5. Cleared airway to <20% obstruction.\n6. Hemostasis with epi/saline.\nPlan: ICU for monitoring.",
            5: "patient keller thomas 67 male here for airway obstruction left side squamous cell cancer rigid bronch used tube 12 general anesthesia saw the tumor blocking about 90 percent used the scope to core it out and then the microdebrider to clean it up no laser used bleeding controlled with cold saline airway looks good now maybe 20 percent blocked sent to icu thanks.",
            6: "Rigid bronchoscopy with mechanical debulking of endobronchial tumor was performed on Thomas Keller a 67 year old male General anesthesia with neuromuscular blockade Patient intubated with size 12 rigid bronchoscope intermittent jet ventilation provided through the bronchoscope barrel Exophytic friable tumor arising from the medial wall of the left mainstem bronchus causing approximately 90 percent luminal obstruction The bevel of the rigid bronchoscope was used to perform repeated rigid coring and mechanical debulking passes through the tumor Large pieces of tumor were removed with forceps and suction A microdebrider was then introduced through the rigid scope to further debulk residual tumor until the lumen was widely patent Final left mainstem obstruction estimated at under 20 percent",
            7: "[Indication]\nMalignant central airway obstruction (LMS) due to SCC.\n[Anesthesia]\nGeneral anesthesia, Rigid Bronchoscopy.\n[Description]\n90% obstruction identified in Left Mainstem. Mechanical debulking performed via rigid coring and microdebrider. Tumor excised in pieces. No thermal ablation.\n[Plan]\nICU admission. Post-op CXR.",
            8: "Mr. Keller was brought to the operating room for management of a severe left mainstem obstruction caused by squamous cell carcinoma. After inducing general anesthesia, we inserted a rigid bronchoscope. We found a large, friable tumor blocking nearly 90% of the airway. Using the bevel of the scope and a microdebrider, we mechanically excised the tumor in a piecemeal fashion. We successfully restored the airway patency significantly, leaving less than 20% residual obstruction, without needing any thermal ablation tools.",
            9: "Procedure: Rigid bronchoscopy with physical extraction of endobronchial neoplasm. Diagnosis: Malignant blockage of the left mainstem. Actions: The scope's bevel was employed to core through the lesion. Large fragments were grasped and withdrawn. A microdebrider shaved down remaining tissue. Outcome: Airway patency restored."
        },
        1: { # Maria Lopez (Flex Bronch Trachea, Granulation)
            1: "Dx: Tracheal stenosis (granulation).\nProc: Flex bronch (31640).\nAction: Mech debulking w/ alligator forceps & snare.\nResult: 70% -> Patent.\nEBL: 10mL.\nPlan: D/C home.",
            2: "PROCEDURE NOTE: Ms. Lopez presented with stridor secondary to benign post-intubation tracheal stenosis. Flexible bronchoscopy revealed circumferential granulation tissue narrowing the distal trachea by 70%. We proceeded with mechanical excision (CPT 31640). Using large alligator forceps and a snare device, the obstructing granulation tissue was systematically avulsed and resected. This mechanical disruption successfully restored luminal patency. No thermal modalities were required.",
            3: "Coding Rationale: 31640 (Bronchoscopy with excision of tumor/tissue).\nTarget: Distal Trachea.\nPathology: Benign granulation tissue.\nMethod: Mechanical excision using alligator forceps and snare resection via flexible bronchoscope.\nJustification: Removal of obstructing tissue to relieve dyspnea.",
            4: "Resident Note\nPt: M. Lopez, 58F\nIndication: Tracheal stenosis.\nTechnique: Flexible bronchoscopy.\nFindings: Granulation tissue at distal trachea (70% obs).\nIntervention: Mechanical debulking with forceps and snare.\nComplications: None.\nPlan: Discharge, PPI, ICS.",
            5: "maria lopez here for difficulty breathing has that scar tissue in her trachea from previous intubation we did a flex bronch with moderate sedation saw the granulation tissue blocking 70 percent used the alligator forceps to grab it and pull it out also used a snare to cut the band open airway looks much better now minimal bleeding sending home.",
            6: "Flexible bronchoscopy with mechanical debulking of obstructing granulation tissue Patient Maria Lopez 58 year old female Indication Progressive dyspnea and stridor due to benign post intubation granulation tissue causing distal tracheal stenosis Moderate sedation with IV midazolam and fentanyl Native airway with oral bite block At 2 cm above the carina there was circumferential granulation tissue and nodular scar narrowing the distal trachea to approximately 70 percent obstruction Using large alligator forceps through the flexible bronchoscope multiple passes of mechanical debulking were performed removing friable granulation tissue in piecemeal fashion Snare resection was then used to excise a central fibrotic band",
            7: "[Indication]\nSymptomatic distal tracheal obstruction (granulation tissue).\n[Anesthesia]\nModerate Sedation, Native Airway.\n[Description]\nFlexible bronchoscopy performed. 70% stenosis found. Mechanical debulking performed using forceps and snare resection. Airway opened significantly.\n[Plan]\nDischarge home. F/U 6-8 weeks.",
            8: "Ms. Lopez underwent a flexible bronchoscopy to address her tracheal stenosis. We identified a band of granulation tissue causing about 70% obstruction in the distal trachea. To treat this, we used alligator forceps and a snare to mechanically remove the tissue piece by piece. This mechanical debulking successfully opened the airway without the need for laser or balloon dilation.",
            9: "Procedure: Flexible bronchoscopy with physical removal of obstructing tissue. Indication: Tracheal narrowing. Findings: Granulation tissue constricting the lumen. Actions: The tissue was grasped and extracted using forceps. A snare was utilized to cut the fibrotic band. Result: Tracheal lumen widened significantly."
        },
        2: { # David Nguyen (Rigid Bronch Carina/LMS, SCLC)
            1: "Dx: SCLC Carina/LMS obstruction.\nProc: Rigid bronch (31640).\nAction: Aggressive rigid coring + microdebrider.\nResult: 90% -> 30% obstruction.\nEBL: 80mL (controlled).\nPlan: ICU.",
            2: "OPERATIVE REPORT: Mr. Nguyen, a 72-year-old male with small cell lung carcinoma, presented with near-complete obstruction of the left mainstem (LMS) and carinal involvement. Rigid bronchoscopy was utilized for emergent airway management. The tumor was mechanically debulked via rigid coring and microdebrider excision. We successfully reduced the tumor burden from ~90% to ~30% residual narrowing, restoring ventilation. Hemostasis was achieved with epinephrine.",
            3: "Code: 31640.\nProcedure: Bronchoscopy with excision of tumor.\nTools: Rigid bronchoscope bevel (coring), Microdebrider.\nLocation: Carina and Left Mainstem.\nJustification: Mechanical removal of obstructing SCLC tumor to restore airway patency.",
            4: "Procedure: Carinal/LMS Debulking\nPatient: David Nguyen\nSteps:\n1. GA / Jet Vent.\n2. Rigid scope inserted.\n3. Suctioned clots.\n4. Coring of tumor at carina/LMS.\n5. Microdebrider used for residual.\n6. Epi for bleeding.\n7. Airway opened.\nPlan: ICU.",
            5: "mr nguyen has that small cell cancer choking off the left lung and carina we rushed him to the hybrid or used the rigid scope to core out the tumor very bloody at first about 80ml but we stopped it with epi and the balloon microdebrider helped clean it up airway is open enough now sending to icu intubated.",
            6: "Rigid bronchoscopy with mechanical debulking of carinal and left mainstem tumor General anesthesia rigid bronchoscope with jet ventilation Friable circumferential tumor involving the main carina and extending into the proximal left mainstem causing approximately 85 to 90 percent obstruction with clot burden The rigid bronchoscope bevel was then used for aggressive rigid coring of the exophytic tumor at the carina and into the left mainstem Multiple large tumor fragments were removed using forceps and suction Subsequent passes with the microdebrider further debulked residual tissue",
            7: "[Indication]\nSCLC with carinal/LMS obstruction and hemoptysis.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\nTumor coring performed with rigid scope. Microdebrider used for further excision. 90% obstruction reduced to 30%.\n[Plan]\nICU admission. Systemic therapy.",
            8: "We performed an emergent rigid bronchoscopy on Mr. Nguyen due to his severe airway obstruction from small cell lung cancer. The tumor was blocking the carina and left mainstem bronchus. We mechanically cored through the tumor using the rigid scope and used forceps to remove large fragments. A microdebrider helped smooth the airway. We managed to reduce the blockage significantly, though he lost about 80mL of blood, which was controlled.",
            9: "Procedure: Rigid bronchoscopy with physical reduction of tumor burden. Indication: Hemoptysis and blockage. Actions: The rigid scope was used to gouge out the lesion. Forceps extracted the fragments. A microdebrider shaved the remaining tissue. Outcome: Airway patency restored to acceptable levels."
        },
        3: { # Sarah Ibrahim (Rigid Bronch RMS, RCC)
            1: "Dx: RCC metastasis to RMS.\nProc: Rigid bronch (31640).\nAction: Coring, forceps, microdebrider.\nResult: 80% -> 20% obstruction.\nEBL: 30mL.\nPlan: Floor.",
            2: "PROCEDURE NOTE: Ms. Ibrahim underwent rigid bronchoscopy for palliation of a right mainstem (RMS) obstruction secondary to metastatic renal cell carcinoma. The highly vascular polypoid lesion was causing 80% stenosis. Mechanical debulking was executed using the bevel of the rigid scope for coring, followed by forceps excision and microdebrider therapy. This purely mechanical approach effectively resected the tumor, improving patency to 80%.",
            3: "CPT: 31640 (Excision of tumor).\nSite: Right Mainstem Bronchus.\nMethod: Mechanical debulking (Rigid coring, forceps, microdebrider).\nNote: No thermal energy used due to vascularity/preference. EBL controlled.",
            4: "Resident Procedure Note\nPt: S. Ibrahim\nIndication: RMS obstruction (RCC).\nTechnique: Rigid bronchoscopy.\nActions:\n- Inspection with flex scope.\n- Rigid coring of RMS tumor.\n- Forceps removal.\n- Microdebrider cleanup.\nOutcome: Airway patent.\nPlan: Admit to floor.",
            5: "sarah ibrahim 63 female with renal cancer met in the right lung rigid bronch done today general anesthesia tumor was vascular but we cored it out with the scope and grabbed pieces with forceps microdebrider used too bleeding was okay 30ml airway looks good now extubated fine.",
            6: "Rigid bronchoscopy with mechanical debulking of right mainstem tumor Patient Sarah Ibrahim 63 year old female Indication Right mainstem endobronchial metastasis from renal cell carcinoma with progressive dyspnea and wheeze Polypoid highly vascular tumor arising from lateral wall of the right mainstem extending 1 point 5 cm distal to the carina and narrowing the lumen to approximately 80 percent Rigid coring of the tumor was performed with the bevel of the scope Forceps debulking removed multiple tumor fragments Final passes were made with a microdebrider to smooth the tumor base",
            7: "[Indication]\nRCC metastasis to RMS with dyspnea.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n80% obstruction in RMS. Mechanical debulking performed via coring, forceps, and microdebrider. Airway opened to ~80% patency.\n[Plan]\nResume systemic therapy.",
            8: "Ms. Ibrahim came in for a rigid bronchoscopy to treat a metastasis in her right mainstem bronchus. We found a vascular tumor blocking most of the airway. Using the rigid scope, we mechanically cored out the tumor and removed the pieces with forceps. A microdebrider was used to finish the cleanup. We successfully opened the airway without using any heat-based therapies.",
            9: "Procedure: Rigid bronchoscopy with mechanical extraction of metastasis. Diagnosis: Renal cell carcinoma blocking the right airway. Intervention: The lesion was cored and extracted using physical tools. A rotary shaving device (microdebrider) cleared the residue. Result: Improved ventilation to the right lung."
        },
        4: { # James Patel (Rigid Bronch Proximal Trachea, Adenoid Cystic)
            1: "Dx: Proximal tracheal tumor (Adenoid Cystic).\nProc: Rigid bronch (31640).\nAction: Forceps resection, snare, mechanical shaving.\nResult: 75% -> Patent.\nEBL: <10mL.\nPlan: Discharge.",
            2: "OPERATIVE REPORT: Mr. Patel presented with a proximal tracheal mass suggestive of adenoid cystic carcinoma. Rigid bronchoscopy was performed under general anesthesia. The tumor, causing 75% obstruction, was addressed via mechanical excision. We employed rigid forceps for piecemeal removal, followed by snare resection of the pedunculated component. The rigid bevel was used to shave the base flush. No thermal ablation was applied.",
            3: "Billing Code: 31640 (Bronchoscopy, rigid or flexible, with excision of tumor).\nLocation: Proximal Trachea.\nTools Used: Rigid forceps, snare loop, rigid bevel (mechanical shaving).\nOutcome: Relief of 75% obstruction.",
            4: "Procedure: Tracheal Debulking\nAttending: Dr. Wong\nPatient: J. Patel\nSteps:\n1. GA / Rigid scope.\n2. Visualized tumor 3cm below cords.\n3. Resected with forceps and snare.\n4. Shaved base with scope bevel.\n5. Hemostasis good.\nPlan: Home today.",
            5: "james patel has that tumor in his upper trachea looks like adenoid cystic rigid bronch used today we grabbed it with forceps and cut the stalk with a snare shaved it down with the scope no bleeding really maybe 10cc patient did great going home later.",
            6: "Rigid bronchoscopy with mechanical debulking and excision of proximal tracheal tumor Patient James Patel 69 year old male Indication Fixed stridor and exertional dyspnea from proximal tracheal mass thought to represent adenoid cystic carcinoma Smooth submucosal appearing tumor arising from posterior wall of the proximal trachea approximately 3 cm below the vocal cords protruding into the lumen and causing 75 percent obstruction Tumor was grasped with rigid forceps and removed in several pieces Additional mechanical debulking with the rigid bronchoscope bevel and forceps was used to shave down the residual lesion flush with the wall A snare loop was used to perform final snare resection of a pedunculated component",
            7: "[Indication]\nProximal tracheal mass (suspected Adenoid Cystic).\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n75% obstruction. Mechanical excision performed with forceps and snare. Base shaved with rigid bevel. Airway patent.\n[Plan]\nDischarge. Radiation oncology referral.",
            8: "We performed a rigid bronchoscopy on Mr. Patel to remove a tumor in his upper trachea. The mass was blocking about 75% of his airway. We used forceps to grab and remove pieces of the tumor, and a snare to cut off the main part. We then used the tip of the scope to shave the remaining tissue down flat. The procedure went very well with almost no bleeding.",
            9: "Procedure: Rigid bronchoscopy with physical excision of tracheal neoplasm. Indication: Stridor. Actions: The growth was seized and extracted. A loop device severed the stalk. The base was leveled using the scope's edge. Result: Obstruction resolved."
        },
        5: { # Evelyn Brooks (Rigid Bronch BI, Adeno)
            1: "Dx: BI Adenocarcinoma.\nProc: Rigid bronch (31640).\nAction: Coring, lavage, microdebrider.\nResult: 85% -> 60-70% open.\nEBL: 35mL.\nPlan: Admit, Abx.",
            2: "PROCEDURE NOTE: Ms. Brooks presented with recurrent pneumonia secondary to malignant obstruction of the bronchus intermedius (BI). Rigid bronchoscopy was undertaken. An exophytic adenocarcinoma was found occluding 85% of the lumen. Mechanical debulking was performed using rigid coring and a microdebrider to excise the tumor mass. Lavage was performed to clear distal purulence. We achieved approximately 60-70% patency without the use of thermal modalities.",
            3: "CPT: 31640.\nDescription: Bronchoscopy with excision of tumor.\nSite: Bronchus Intermedius.\nTechnique: Mechanical coring via rigid scope and microdebrider excision.\nJustification: Symptomatic obstruction causing infection.",
            4: "Resident Note\nPt: E. Brooks\nIndication: BI obstruction/pneumonia.\nProcedure: Rigid bronchoscopy.\nIntervention:\n- Suctioned pus.\n- Rigid coring of BI tumor.\n- Microdebrider used.\n- No laser/APC.\nOutcome: BI open to 70%.\nPlan: Admit for IV antibiotics.",
            5: "evelyn brooks has a tumor in the bronchus intermedius causing pneumonia rigid bronch done today general anesthesia suctioned out the pus then cored out the tumor with the scope used the microdebrider to get the rest opened it up to about 60 or 70 percent bleeding 35ml controlled admit to floor.",
            6: "Rigid bronchoscopy with mechanical debulking of bronchus intermedius tumor Patient Evelyn Brooks 54 year old female Indication Central airway obstruction of the bronchus intermedius from endobronchial adenocarcinoma with recurrent post obstructive pneumonia Friable exophytic tumor arising from the bronchus intermedius narrowing the lumen to 85 percent with purulent secretions in the right lower lobe bronchi Secretions were suctioned and lavage performed Rigid coring and mechanical debulking were then done using the rigid bronchoscope bevel A microdebrider was advanced through the rigid scope to further debulk the tumor",
            7: "[Indication]\nBronchus Intermedius obstruction (Adenocarcinoma) w/ pneumonia.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n85% obstruction. Pus suctioned. Mechanical debulking via coring and microdebrider. Patency improved to 60-70%.\n[Plan]\nAdmit. Antibiotics.",
            8: "Ms. Brooks underwent rigid bronchoscopy to clear a tumor blocking her bronchus intermedius and causing pneumonia. We suctioned out the infected secretions and then used the rigid scope to core through the tumor. A microdebrider was used to remove the remaining tissue. We managed to open the airway significantly, improving drainage for the lower lobe.",
            9: "Procedure: Rigid bronchoscopy with mechanical resection of BI mass. Indication: Post-obstructive infection. Actions: Secretions were evacuated. The lesion was cored and shaved using mechanical tools. Result: Airway caliber improved."
        },
        6: { # Omar Hassan (Flex Bronch LLL, Carcinoid)
            1: "Dx: LLL Carcinoid.\nProc: Flex bronch (31640).\nAction: Snare resection, forceps.\nResult: 70% -> Patent.\nEBL: 15mL.\nPlan: D/C home.",
            2: "OPERATIVE REPORT: Mr. Hassan presented with wheeze due to a carcinoid tumor in the left lower lobe (LLL). Flexible bronchoscopy was performed under moderate sedation. The pedunculated tumor was identified causing 70% obstruction. Mechanical excision was achieved by grasping the stalk with forceps and utilizing a snare for resection. Further forceps debulking cleared residual fragments. No thermal ablation was employed.",
            3: "Code: 31640 (Bronchoscopy with excision of tumor).\nModality: Flexible Bronchoscopy.\nSite: Left Lower Lobe.\nTechnique: Snare resection and forceps excision.\nPathology: Carcinoid.",
            4: "Procedure: LLL Tumor Resection\nPt: O. Hassan\nTechnique: Flex bronch.\nFindings: Carcinoid in LLL.\nAction: Snare used to cut stalk. Forceps to remove pieces.\nComplications: None.\nPlan: Discharge.",
            5: "omar hassan here for carcinoid tumor in the left lower lobe flex bronch used with sedation found the tumor blocking 70 percent used a snare to cut it off and forceps to pull it out minimal bleeding 15cc patient doing well going home.",
            6: "Flexible bronchoscopy with mechanical debulking of endobronchial carcinoid tumor Patient Omar Hassan 61 year old male Indication Worsening wheeze and recurrent collapse of left lower lobe from endobronchial carcinoid in the left lower lobe bronchus Rounded vascular pedunculated mass originating from the origin of the left lower lobe bronchus causing approximately 70 percent obstruction The tumor stalk was grasped with biopsy forceps and snare resection was performed at its base Additional mechanical debulking with forceps removed residual tumor fragments until the lumen was largely free of tumor",
            7: "[Indication]\nLLL Carcinoid tumor.\n[Anesthesia]\nModerate Sedation, Flexible Bronchoscopy.\n[Description]\nPedunculated mass in LLL. Snare resection performed. Residuals removed with forceps. Lumen patent.\n[Plan]\nDischarge. Surveillance.",
            8: "We performed a flexible bronchoscopy on Mr. Hassan to remove a carcinoid tumor in his left lower lobe. We used a snare to loop around the base of the tumor and cut it off. We then used forceps to remove the remaining pieces. The airway is now clear, and no heat therapy was needed.",
            9: "Procedure: Flexible bronchoscopy with physical extraction of carcinoid. Indication: Wheezing. Actions: The growth was severed using a wire loop (snare). Fragments were retrieved with grippers. Result: LLL bronchus cleared."
        },
        7: { # Lin Chen (Rigid Bronch LMS, SCC - Acute)
            1: "Dx: LMS SCC, Acute Respiratory Failure.\nProc: Emergent Rigid bronch (31640).\nAction: Rigid coring, forceps, microdebrider.\nResult: 95% -> Patent.\nEBL: 60mL.\nPlan: ICU.",
            2: "PROCEDURE NOTE: Ms. Chen presented in acute hypoxic respiratory failure due to critical left mainstem (LMS) obstruction (95%) from squamous cell carcinoma. Emergent rigid bronchoscopy was performed. Mechanical debulking was executed via rigid coring, forceps excision, and microdebrider therapy. This intervention successfully restored airway patency and left lung expansion without the use of ablative energy.",
            3: "CPT: 31640.\nIndication: Malignant airway obstruction (Status: Emergent).\nSite: Left Mainstem.\nMethod: Mechanical excision (Coring, Forceps, Microdebrider) via Rigid Scope.\nOutcome: Re-expansion of left lung.",
            4: "Procedure: Emergent LMS Debulking\nPt: L. Chen\nIndication: Acute failure/LMS obstruction.\nSteps:\n1. GA / Rigid intubation.\n2. Suctioned mucus.\n3. Rigid coring of tumor.\n4. Forceps removal.\n5. Microdebrider.\n6. Hemostasis.\nResult: Lung re-expanded.",
            5: "lin chen came in with respiratory failure left lung collapsed from tumor we took her to or stat rigid bronch used cored out the tumor in the left mainstem with the scope and forceps used microdebrider too bleeding 60cc controlled lung came back up on xray sending to icu.",
            6: "Rigid bronchoscopy with mechanical debulking of left mainstem tumor Patient Lin Chen 49 year old female Indication Malignant central airway obstruction from left mainstem squamous cell carcinoma with acute hypoxic respiratory failure Bulky friable tumor filling the left mainstem lumen with 95 percent obstruction copious mucus and collapse of left lung After suctioning secretions rigid coring was performed repeatedly through the tumor using the rigid bronchoscope bevel Large tumor chunks were removed with forceps A microdebrider was used for fine mechanical debulking until the airway lumen was sufficiently re opened",
            7: "[Indication]\nAcute hypoxic respiratory failure due to LMS SCC.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n95% LMS obstruction. Emergent mechanical debulking via coring/microdebrider. Left lung re-expanded.\n[Plan]\nICU. Monitor oxygenation.",
            8: "Ms. Chen was in acute respiratory failure due to a tumor blocking her left mainstem bronchus. We performed an emergency rigid bronchoscopy. Using the scope to core the tumor and forceps to remove the bulk, followed by a microdebrider, we were able to open the airway. Her left lung re-expanded on the table, and she was stable for transport to the ICU.",
            9: "Procedure: Emergency rigid bronchoscopy with mechanical tumor extraction. Indication: Respiratory collapse. Actions: The blockage was cored out. Tissue was extracted manually. A microdebrider refined the airway channel. Result: Left lung ventilation restored."
        },
        8: { # Jacob Morales (Rigid Bronch RMS, SCC)
            1: "Dx: RMS SCC w/ hemoptysis.\nProc: Rigid bronch (31640).\nAction: Coring, forceps, microdebrider.\nResult: 70% -> 60-70% patency.\nEBL: 50mL.\nPlan: Admit.",
            2: "OPERATIVE REPORT: Mr. Morales presented with hemoptysis and dyspnea secondary to right mainstem (RMS) squamous cell carcinoma. Rigid bronchoscopy was performed. The tumor, causing 70% obstruction, was mechanically debulked using rigid coring, forceps excision, and microdebrider. The procedure improved lumen patency to approximately 65% and controlled the source of hemoptysis without thermal ablation.",
            3: "Code: 31640.\nSite: Right Mainstem.\nTechnique: Mechanical excision of tumor (Coring, Forceps, Microdebrider).\nIndication: Hemoptysis/Obstruction.",
            4: "Procedure: RMS Debulking\nPt: J. Morales\nIndication: Hemoptysis.\nSteps:\n1. Rigid bronchoscopy.\n2. Suctioned blood.\n3. Cored tumor in RMS.\n4. Forceps/Microdebrider used.\n5. Bleeding controlled.\nPlan: Step-down unit.",
            5: "jacob morales 76 male with hemoptysis right mainstem tumor rigid bronch done today general anesthesia cored out the tumor and used forceps and microdebrider cleared it out pretty well bleeding stopped with epi 50ml loss admit to step down.",
            6: "Rigid bronchoscopy with mechanical debulking of right mainstem tumor Patient Jacob Morales 76 year old male Indication Hemoptysis and dyspnea due to right mainstem endobronchial squamous cell carcinoma Ulcerated friable tumor occupying 70 percent of the right mainstem lumen with clot burden Clot and secretions suctioned Rigid coring performed with the rigid scope to mechanically debulk the tumor Forceps debulking removed residual fragments A microdebrider was then used to further debulk and smooth the tumor base Tumor debulked mechanically until lumen patency improved to 60 to 70 percent",
            7: "[Indication]\nRMS SCC with hemoptysis.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n70% obstruction. Mechanical debulking (coring, forceps, microdebrider) performed. Airway opened. Hemostasis achieved.\n[Plan]\nStep-down unit.",
            8: "Mr. Morales had a tumor in his right mainstem bronchus causing bleeding. We performed a rigid bronchoscopy to treat this. We cored out the tumor mechanically and used forceps and a microdebrider to remove the tissue. This opened the airway and stopped the bleeding without using any cautery.",
            9: "Procedure: Rigid bronchoscopy with physical resection of RMS lesion. Indication: Bleeding and shortness of breath. Actions: The tumor was cored and extracted. A shaving device smoothed the lumen. Result: Hemorrhage controlled, airway cleared."
        },
        9: { # Priya Singh (Rigid Bronch LMS, Breast Met)
            1: "Dx: Breast Ca met to LMS.\nProc: Rigid bronch (31640).\nAction: Bevel debulking, forceps, snare.\nResult: 80% -> 60% open.\nEBL: 20mL.\nPlan: Oncology floor.",
            2: "PROCEDURE NOTE: Ms. Singh, with metastatic breast cancer, presented with left mainstem (LMS) obstruction. Rigid bronchoscopy revealed an irregular tumor causing 80% stenosis. Mechanical debulking was performed utilizing the rigid bronchoscope bevel, forceps, and snare resection for a pedunculated component. Lumen patency was improved to 60% with visualization of distal segments. No thermal energy was utilized.",
            3: "CPT: 31640.\nPathology: Metastatic Breast Cancer.\nLocation: Left Mainstem.\nMethod: Mechanical excision (Bevel, Forceps, Snare).\nOutcome: Relief of obstruction.",
            4: "Procedure: LMS Debulking\nPt: P. Singh\nIndication: Metastatic breast cancer.\nSteps:\n1. Rigid bronchoscopy.\n2. Identified LMS tumor.\n3. Snare resection of pedunculated part.\n4. Mechanical debulking with bevel/forceps.\n5. Hemostasis good.\nPlan: Admit.",
            5: "priya singh has breast cancer met in the left mainstem rigid bronch used general anesthesia debulked the tumor with the scope bevel and forceps used a snare too opened it up nicely bleeding minimal sending to oncology floor.",
            6: "Rigid bronchoscopy with mechanical debulking of metastatic tumor Patient Priya Singh 65 year old female Indication Left mainstem obstruction from metastatic breast cancer with progressive dyspnea and cough Irregular nodular tumor on the lateral wall of the left mainstem bronchus causing 80 percent obstruction with distal atelectasis Mechanical debulking performed using the rigid bronchoscope bevel followed by forceps debulking Snare resection was used to remove a pedunculated portion of tumor The procedure explicitly consisted of tumor excision and mechanical debulking without any thermal ablation",
            7: "[Indication]\nMetastatic breast cancer to LMS.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n80% obstruction. Snare and mechanical debulking performed. Airway opened to 60%.\n[Plan]\nAdmit to Oncology.",
            8: "Ms. Singh underwent rigid bronchoscopy for a breast cancer metastasis blocking her left mainstem bronchus. We used the rigid scope to mechanically debulk the tumor and a snare to remove a hanging piece of tissue. We successfully opened the airway to about 60% patency.",
            9: "Procedure: Rigid bronchoscopy with mechanical excision of metastasis. Indication: Airway blockage. Actions: The scope bevel scraped the lesion. Grippers and a loop device extracted the tissue. Result: LMS ventilation improved."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages to ensure consistency with the prompt's examples
    return [
        {"idx": 0, "orig_name": "Thomas Keller", "orig_age": 67, "names": ["Robert Smith", "James Johnson", "William Brown", "David Jones", "Richard Miller", "Joseph Davis", "Charles Garcia", "Thomas Rodriguez", "Christopher Wilson"]},
        {"idx": 1, "orig_name": "Maria Lopez", "orig_age": 58, "names": ["Maria Martinez", "Patricia Anderson", "Jennifer Taylor", "Linda Thomas", "Elizabeth Hernandez", "Barbara Moore", "Susan Martin", "Jessica Jackson", "Sarah Thompson"]},
        {"idx": 2, "orig_name": "David Nguyen", "orig_age": 72, "names": ["Michael White", "John Lopez", "Robert Lee", "James Gonzalez", "William Harris", "David Clark", "Richard Lewis", "Joseph Robinson", "Charles Walker"]},
        {"idx": 3, "orig_name": "Sarah Ibrahim", "orig_age": 63, "names": ["Karen Perez", "Nancy Hall", "Lisa Young", "Betty Allen", "Margaret Sanchez", "Sandra Wright", "Ashley King", "Kimberly Scott", "Emily Green"]},
        {"idx": 4, "orig_name": "James Patel", "orig_age": 69, "names": ["Daniel Baker", "Paul Adams", "Mark Nelson", "Donald Hill", "George Ramirez", "Kenneth Campbell", "Steven Mitchell", "Edward Roberts", "Brian Carter"]},
        {"idx": 5, "orig_name": "Evelyn Brooks", "orig_age": 54, "names": ["Donna Phillips", "Michelle Evans", "Dorothy Turner", "Carol Torres", "Amanda Parker", "Melissa Collins", "Deborah Edwards", "Stephanie Stewart", "Rebecca Flores"]},
        {"idx": 6, "orig_name": "Omar Hassan", "orig_age": 61, "names": ["Ronald Morris", "Anthony Nguyen", "Kevin Murphy", "Jason Rivera", "Matthew Cook", "Gary Rogers", "Timothy Morgan", "Jose Peterson", "Larry Cooper"]},
        {"idx": 7, "orig_name": "Lin Chen", "orig_age": 49, "names": ["Sharon Reed", "Cynthia Bailey", "Kathleen Bell", "Amy Gomez", "Shirley Kelly", "Angela Howard", "Helen Ward", "Anna Cox", "Brenda Diaz"]},
        {"idx": 8, "orig_name": "Jacob Morales", "orig_age": 76, "names": ["Jeffrey Richardson", "Frank Wood", "Scott Watson", "Eric Brooks", "Stephen Bennett", "Andrew Gray", "Raymond James", "Gregory Reyes", "Joshua Cruz"]},
        {"idx": 9, "orig_name": "Priya Singh", "orig_age": 65, "names": ["Pamela Hughes", "Nicole Price", "Samantha Myers", "Katherine Long", "Christine Foster", "Debra Sanders", "Rachel Ross", "Carolyn Morales", "Janet Powell"]}
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
                note_entry["note_text"] = f"Variation {style_num} for note {idx} not found in script."
            
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
    output_filename = output_dir / "synthetic_debulking_notes_part_062.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()