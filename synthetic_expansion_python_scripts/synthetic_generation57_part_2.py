import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_057_part2.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_base_data_mocks():
    """
    Returns mock data for names and ages corresponding to the 10 patients 
    in consolidated_verified_notes_v2_8_part_057_part2.json.
    """
    return [
        # Note 0: Ian Murphy (65)
        {"idx": 0, "orig_name": "Ian Murphy", "orig_age": 65, "names": ["Robert Cole", "James Sullivan", "Arthur Dent", "William Thorne", "Henry Cabot", "George Miller", "Edward Vance", "Richard Hall", "Thomas Wright"]},
        # Note 1: Doris Hill (74)
        {"idx": 1, "orig_name": "Doris Hill", "orig_age": 74, "names": ["Martha Stewart", "Betty White", "Helen Mirren", "Barbara Bush", "Nancy Reagan", "Margaret Thatcher", "Judith Dench", "Maggie Smith", "Angela Lansbury"]},
        # Note 2: Anthony Green (68)
        {"idx": 2, "orig_name": "Anthony Green", "orig_age": 68, "names": ["Bruce Banner", "Tony Stark", "Steve Rogers", "Clint Barton", "Natasha Romanoff", "Nick Fury", "Phil Coulson", "Sam Wilson", "Bucky Barnes"]},
        # Note 3: Nina Alvarez (67)
        {"idx": 3, "orig_name": "Nina Alvarez", "orig_age": 67, "names": ["Maria Garcia", "Elena Rodriguez", "Sofia Martinez", "Isabella Lopez", "Camila Hernandez", "Valentina Gonzalez", "Gabriela Perez", "Daniela Sanchez", "Martina Romero"]},
        # Note 4: James Porter (52)
        {"idx": 4, "orig_name": "James Porter", "orig_age": 52, "names": ["Harry Potter", "Ron Weasley", "Draco Malfoy", "Neville Longbottom", "Seamus Finnigan", "Dean Thomas", "Oliver Wood", "Percy Weasley", "Fred Weasley"]},
        # Note 5: Harriet Cole (62)
        {"idx": 5, "orig_name": "Harriet Cole", "orig_age": 62, "names": ["Jane Austen", "Charlotte Bronte", "Emily Bronte", "Anne Bronte", "Virginia Woolf", "George Eliot", "Mary Shelley", "Louisa May Alcott", "Edith Wharton"]},
        # Note 6: Walter Young (80)
        {"idx": 6, "orig_name": "Walter Young", "orig_age": 80, "names": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Charles Darwin", "Nikola Tesla", "Thomas Edison", "Alexander Graham Bell", "Marie Curie", "Louis Pasteur"]},
        # Note 7: Chloe Harris (55)
        {"idx": 7, "orig_name": "Chloe Harris", "orig_age": 55, "names": ["Rachel Green", "Monica Geller", "Phoebe Buffay", "Janice Hosenstein", "Carol Willick", "Susan Bunch", "Emily Waltham", "Tag Jones", "Gunther Centralperk"]},
        # Note 8: Xavier Bennett (69)
        {"idx": 8, "orig_name": "Xavier Bennett", "orig_age": 69, "names": ["Charles Xavier", "Erik Lehnsherr", "Logan Howlett", "Scott Summers", "Hank McCoy", "Jean Grey", "Ororo Munroe", "Kurt Wagner", "Piotr Rasputin"]},
        # Note 9: Evelyn Ross (73)
        {"idx": 9, "orig_name": "Evelyn Ross", "orig_age": 73, "names": ["Rose Tyler", "Martha Jones", "Donna Noble", "Amy Pond", "Rory Williams", "Clara Oswald", "Bill Potts", "Yasmin Khan", "Ryan Sinclair"]},
    ]

def get_variations():
    """
    Returns a dictionary of stylistic variations for the 10 notes.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Ian Murphy - Left mainstem RCC
            1: "Procedure: Rigid bronchoscopy.\nTarget: Left mainstem.\nAction: Mechanical debulking of vascular tumor (80% -> 25%).\nTools: Coring, suction, forceps, microdebrider.\nComplications: Brisk bleeding, controlled w/ iced saline/epi/tamponade.\nPlan: MICU, abx.",
            2: "OPERATIVE REPORT: The patient, a 65-year-old male with metastatic renal cell carcinoma, presented with post-obstructive pneumonia. Under general anesthesia, rigid bronchoscopy was employed. A polypoid, vascular lesion in the proximal left mainstem bronchus was identified, causing approximately 80% stenosis. Mechanical debulking was executed utilizing the rigid barrel for coring, alongside suction and forceps. A microdebrider facilitated fine excision. Hemostasis was achieved following brisk hemorrhage using cold saline, epinephrine, and tamponade. The final lumen caliber was estimated at 75% patency.",
            3: "CPT 31640 Justification: Bronchoscopy with excision of tumor.\nTechnique: Rigid bronchoscopy used to access left mainstem.\nPathology: Metastatic RCC causing obstruction.\nIntervention: Mechanical excision performed using rigid coring and microdebrider techniques. Multiple fragments removed. Hemostasis managed.\nOutcome: Improvement from 80% to 25% obstruction.",
            4: "Procedure Note\nResident: Dr. Morgan\nAttending: Dr. Ramos\nSteps:\n1. Induced GA.\n2. Inserted rigid bronchoscope.\n3. Identified L mainstem tumor (RCC met).\n4. Debulked using rigid coring and forceps.\n5. Controlled bleeding with saline/epi/barrel tamponade.\n6. Suctioned purulence.\nPlan: MICU for monitoring.",
            5: "Ian Murphy 65M renal cell ca met to left main. Did rigid bronch today under GA. Big vascular tumor there blocking 80 percent. Cored it out with the rigid scope and used the microdebrider too. Bled a lot at first but we stopped it with ice saline and holding pressure with the scope. Got it open to like 25 percent residual. Sent him to MICU for the pneumonia treatment.",
            6: "Under general anesthesia with rigid bronchoscopy, a 65-year-old male underwent mechanical debulking of a left mainstem tumor secondary to metastatic renal cell carcinoma. The tumor caused 80% compromise. Utilizing rigid coring, suction, forceps, and a microdebrider, the lesion was excised. Brisk bleeding was encountered and controlled with iced saline, epinephrine, and tamponade. Final airway narrowing was reduced to 25%. The patient remained intubated and was transferred to the MICU.",
            7: "[Indication]\nLeft mainstem obstruction, metastatic renal cell carcinoma, post-obstructive pneumonia.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\nVascular polypoid tumor in proximal LMS (80% stenosis). Mechanically debulked via rigid coring and microdebrider. Bleeding controlled. Lumen restored to ~75% patency.\n[Plan]\nMICU admission, antibiotics.",
            8: "The patient was brought to the operating room for management of a left mainstem obstruction caused by metastatic renal cell carcinoma. Following the induction of general anesthesia, a rigid bronchoscope was introduced. We encountered a vascular, polypoid tumor obstructing 80% of the lumen. We proceeded to debulk the tumor mechanically using the rigid barrel, forceps, and a microdebrider. Although brisk bleeding occurred, it was successfully managed. We achieved a near-circular lumen with only 25% residual narrowing.",
            9: "Procedure: Rigid endoscopy with tumor resection.\nPatient: Ian Murphy.\nDetails: A vascular mass arising from the left mainstem was resected using rigid coring and microdebrider. The lesion, causing significant occlusion, was excised to restore patency. Hemorrhage was managed with vasoconstrictors and tamponade. The airway was cleared of purulent secretions."
        },
        1: { # Doris Hill - Right bronchus intermedius NSCLC
            1: "Dx: NSCLC, Right Bronchus Intermedius obstruction.\nProc: Rigid bronch, mechanical debulking.\nFindings: 75% obstruction, distal mucous plugging.\nAction: Cored tumor, removed fragments, microdebrider for cleanup.\nResult: 30% residual narrowing. Mild bleeding.\nDisp: Floor.",
            2: "PROCEDURE: Rigid Bronchoscopy with Mechanical Tumor Debulking.\nINDICATION: Recurrent post-obstructive pneumonia secondary to NSCLC involving the bronchus intermedius.\nNARRATIVE: The patient was placed under general anesthesia. Rigid bronchoscopic inspection revealed an exophytic lesion obstructing 75% of the bronchus intermedius. Mechanical excision was performed utilizing the rigid barrel and forceps, followed by microdebrider refinement. The airway was recanalized to approximately 70% patency. Hemostasis was maintained throughout.",
            3: "Billing Code: 31640 (Bronchoscopy; with excision of tumor).\nLocation: Right Bronchus Intermedius.\nMethod: Mechanical debulking via rigid bronchoscopy.\nDetails: Tumor obstructing 75% of lumen was cored and excised using microdebrider. Suction used to clear distal mucous plugging. Hemostasis achieved.",
            4: "Resident Note: Rigid Bronchoscopy\nPatient: Doris Hill\nStaff: Dr. Reed\n1. General anesthesia induced.\n2. Rigid scope inserted.\n3. Tumor found in bronchus intermedius (75% occluded).\n4. Mechanical debulking performed (coring/forceps).\n5. Microdebrider used for residual.\n6. Hemostasis with cold saline.\nPlan: Floor admission, pneumonia mgmt.",
            5: "Doris Hill 74F nsclc right lung. Bronchus intermedius blocked about 75 percent causing pneumonia. We went in with the rigid scope under general. Cored out the tumor used the sucker and forceps to get the big chunks. Used the microdebrider to smooth it out. Bleeding wasn't bad used some epi. Airway looks way better now maybe 30 percent narrow. Extubated and sent to floor.",
            6: "A 74-year-old female underwent rigid bronchoscopy for a right bronchus intermedius obstruction due to non-small cell lung cancer. An exophytic tumor causing 75% obstruction was identified. Mechanical debulking was performed using the rigid barrel, suction, and forceps, followed by microdebrider excision. The airway lumen was restored with approximately 30% residual narrowing. Mild bleeding was controlled with cold saline. The patient was extubated and admitted to the medical floor.",
            7: "[Indication]\nRight bronchus intermedius obstruction, NSCLC, recurrent pneumonia.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\nExophytic tumor in BI (75% block). Mechanically debulked via rigid coring and microdebrider. Large fragments removed. Residual narrowing ~30%.\n[Plan]\nFloor admission, antibiotics.",
            8: "Mrs. Hill presented for management of a right bronchus intermedius obstruction. Under general anesthesia, we utilized a rigid bronchoscope to visualize the exophytic tumor causing 75% obstruction. We performed mechanical debulking using the rigid barrel to core out the tumor, removing large fragments with forceps. A microdebrider was then used to excise residual tissue. We successfully restored the airway lumen, leaving only about 30% residual narrowing.",
            9: "Intervention: Rigid endoscopy with lesion excision.\nTarget: Bronchus intermedius.\nAction: The obstructing mass was resected using mechanical coring and microdebrider tools. The airway was cleared of obstruction and distal secretions. Hemostasis was secured. The patient was admitted for continued care."
        },
        2: { # Anthony Green - Distal Trachea/Carina Stent
            1: "Indication: Critical distal tracheal obstruction (95%).\nProcedure: Rigid bronch, debulking, silicone stent (14x40mm).\nFindings: Bulky tumor at carina.\nAction: Aggressive debulking to patent lumen. Stent deployed bridging carina.\nResult: 30% residual narrowing, good airflow.\nPlan: ICU.",
            2: "OPERATIVE NOTE: This 68-year-old male presented with near-critical airway obstruction. Rigid bronchoscopy was performed under general anesthesia. A bulky exophytic tumor was noted at the distal trachea extending to the carina, causing 95% obstruction. Aggressive mechanical debulking was executed to restore patency. Subsequently, a 14 x 40 mm silicone stent was deployed to maintain the airway caliber. Post-procedure inspection revealed robust airflow to both mainstems.",
            3: "Codes Submitted: 31640 (Excision), 31631 (Stent placement).\nRationale: Distinct procedural steps performed. First, aggressive mechanical excision of tracheal tumor (31640) was required to create a patent lumen. Second, a silicone tracheal stent (31631) was placed to prevent re-obstruction of the distal trachea/carina.",
            4: "Procedure: Rigid Bronch + Stent\nSteps:\n1. GA / Jet ventilation.\n2. Rigid scope to distal trachea.\n3. Found 95% obstruction at carina.\n4. Debulked with coring/forceps/microdebrider.\n5. Sized and placed 14x40mm silicone stent.\n6. Confirmed patency.\nNo major complications.",
            5: "Anthony Green 68M really bad airway obstruction distal trachea almost closed off. We did emergent rigid bronch. Scraped out the tumor aggressively with the rigid tip and forceps. Once we got it open enough we put in a silicone stent 14 by 40. Covers the carina area nicely. Breathing much better now. ICU for watch.",
            6: "Under general anesthesia, a 68-year-old male with critical distal tracheal obstruction underwent rigid bronchoscopy. A bulky tumor causing 95% blockage was identified. Mechanical debulking was performed using rigid coring and forceps to establish a patent lumen. A 14 x 40 mm silicone stent was then deployed across the lesion, bridging the carina. Final assessment showed 30% residual narrowing with good airflow. Complications were limited to mild bleeding.",
            7: "[Indication]\nCritical distal tracheal tumor, impending respiratory failure.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\n95% obstruction at distal trachea/carina. Aggressive mechanical debulking performed. 14x40mm silicone stent deployed. Airway patency restored.\n[Plan]\nICU admission, airway monitoring.",
            8: "Mr. Green arrived with critical airway compromise due to a distal tracheal tumor. We proceeded with rigid bronchoscopy under general anesthesia. Upon visualization, the tumor was occluding 95% of the airway. We performed aggressive mechanical debulking to clear the obstruction. To ensure continued patency, we deployed a 14 x 40 mm silicone stent across the distal trachea and carina. The patient was transferred to the ICU for close monitoring.",
            9: "Procedure: Rigid endoscopy with tumor resection and prosthesis insertion.\nFindings: Critical stenosis of the distal trachea.\nAction: The obstructing mass was excised to creating a channel. A silicone prosthesis was positioned to scaffold the airway. Hemostasis was achieved. Airflow was significantly improved."
        },
        3: { # Nina Alvarez - Tracheal Granulation
            1: "Dx: Post-radiation tracheal granulation.\nProc: Flex/Rigid bronch, resection.\nFindings: Pedunculated polyp, 60% narrowing.\nAction: Snare resection, microdebrider, rigid coring.\nResult: 15% residual narrowing. No stent.\nDisp: Home same day.",
            2: "PROCEDURE NOTE: The patient underwent rigid and flexible bronchoscopy for management of symptomatic tracheal granulation tissue. A pedunculated polypoid lesion was identified on the anterior tracheal wall, approximately 3 cm proximal to the carina. The lesion was resected en bloc using a snare, followed by microdebrider debridement of the base. Rigid coring was utilized to smooth the tracheal wall. Hemostasis was excellent.",
            3: "Billing: 31640 (Excision of tumor/tissue).\nJustification: Mechanical removal of obstructing granulation tissue in the trachea.\nTools: Snare, microdebrider, rigid scope.\nOutcome: Improvement from 60% to 15% obstruction. No stent required.",
            4: "Resident Note: Tracheal Resection\nPatient: Nina Alvarez\n1. GA with ETT.\n2. Identified granulation tissue mid-trachea.\n3. Snare removal of polyp.\n4. Microdebrider to base.\n5. Rigid coring for smoothing.\n6. Minimal bleeding.\nPlan: Discharge home.",
            5: "Nina Alvarez 67F here for tracheal granulation tissue from radiation. Did the bronch today flexible and rigid. Saw the polyp hanging off the front wall about 3cm up from carina. Snared it off then shaved the rest with the microdebrider. Looks way better now open airway. Little bleeding cold saline fixed it. Going home today.",
            6: "A 67-year-old female with post-radiation tracheal granulation tissue underwent flexible and rigid bronchoscopy. A pedunculated polyp causing 60% narrowing was identified on the anterior tracheal wall. The lesion was resected using a snare, followed by microdebrider shaving and rigid coring. The final airway lumen showed approximately 15% residual narrowing. No complications occurred, and the patient was discharged the same day.",
            7: "[Indication]\nPost-radiation tracheal granulation tissue, dyspnea.\n[Anesthesia]\nGeneral, ETT.\n[Description]\nPolypoid lesion anterior trachea (60% block). Snare resection and microdebrider debridement performed. Lumen restored.\n[Plan]\nOutpatient discharge, f/u 6-8 weeks.",
            8: "Ms. Alvarez presented with exertional dyspnea due to tracheal granulation tissue. We performed a combined flexible and rigid bronchoscopy. A polypoid lesion was found obstructing 60% of the trachea. We successfully removed the lesion using snare resection and a microdebrider. Rigid coring was used to ensure a smooth airway wall. The patient tolerated the procedure well and was discharged home.",
            9: "Intervention: Endoscopic resection of tracheal tissue.\nPathology: Benign granulation.\nTechnique: The obstructing tissue was excised using a snare and microdebrider. The airway wall was smoothed. Hemostasis was secured. The patient was discharged to home."
        },
        4: { # James Porter - Left Mainstem Carcinoid
            1: "Indication: Left mainstem carcinoid, hemoptysis.\nProcedure: Rigid bronch, excision.\nFindings: Pedunculated lesion, medial wall LMS, 65% obs.\nAction: Snare resection, base debridement.\nResult: 10-15% residual irregularity. Margins clear.\nDisp: Ward.",
            2: "OPERATIVE REPORT: 52-year-old male with endobronchial carcinoid. Rigid bronchoscopy was performed. A smooth, vascular, pedunculated tumor was visualized arising from the medial wall of the left mainstem bronchus. The tumor stalk was resected en bloc via snare. The base was treated with rigid coring and microdebrider to ensure clearance. Gross margins appeared negative. Hemostasis was achieved with topical epinephrine.",
            3: "CPT 31640: Bronchoscopy with excision of tumor.\nSite: Left Mainstem Bronchus.\nPathology: Carcinoid.\nTechnique: Snare resection of stalk followed by microdebrider of base. Rigid scope used for access and control.",
            4: "Procedure: Bronchoscopic Excision\nPatient: James Porter\n1. General Anesthesia.\n2. Rigid bronchoscopy.\n3. Tumor in L mainstem (carcinoid).\n4. Snare resection performed.\n5. Base cleaned with microdebrider.\n6. Hemostasis achieved.\nPlan: Admit to floor.",
            5: "James Porter 52M carcinoid tumor left main bronchus. We went in with the rigid scope. Saw the tumor it was pedunculated on the medial wall. Snared it off in one piece mostly. Cleaned up the base with the microdebrider. Bleeding was mild used some epi. Airway looks great now almost normal. Sending him to the floor.",
            6: "A 52-year-old male with a left mainstem carcinoid tumor underwent rigid bronchoscopy for excision. A pedunculated lesion causing 65% obstruction was identified. The tumor was resected using a snare, and the base was debrided with a microdebrider. The airway lumen was restored with minimal residual irregularity. Mild bleeding was controlled with iced saline and epinephrine. The patient was extubated and admitted to the ward.",
            7: "[Indication]\nLeft mainstem endobronchial carcinoid, hemoptysis.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\nPedunculated tumor medial LMS. Snare resection and microdebrider excision performed. Margins grossly clear.\n[Plan]\nFloor admission, surveillance.",
            8: "Mr. Porter underwent rigid bronchoscopy for removal of a carcinoid tumor in the left mainstem bronchus. We identified a pedunculated lesion obstructing about 65% of the airway. Using a snare, we resected the tumor stalk en bloc. We then used a microdebrider to remove any residual tissue at the base. The airway lumen was effectively restored, and bleeding was minimal.",
            9: "Procedure: Rigid endoscopy with lesion resection.\nDiagnosis: Typical carcinoid.\nAction: The pedunculated mass was excised using a snare. The attachment site was debrided. Hemostasis was maintained. The airway was fully recanalized."
        },
        5: { # Harriet Cole - Bronchus Intermedius
            1: "Indication: BI tumor, acute dyspnea.\nProcedure: Rigid bronch, debulking.\nFindings: 85% obstruction BI, friable.\nAction: Rigid coring, suction, microdebrider.\nResult: 30% residual narrowing. No stent.\nDisp: Oncology ward.",
            2: "PROCEDURE NOTE: The patient presented with acute dyspnea secondary to a tumor in the bronchus intermedius. Rigid bronchoscopy was initiated. An irregular, friable tumor was found occluding 85% of the lumen. Mechanical debulking was performed via rigid coring and forceps extraction. A microdebrider was employed for fine excision along the airway wall. Patency was improved to approximately 70%.",
            3: "Billing: 31640 (Excision of tumor).\nLocation: Bronchus Intermedius (Right).\nMethod: Mechanical debulking with rigid barrel and microdebrider.\nNecessity: Symptomatic 85% obstruction causing lobar collapse.",
            4: "Resident Note: Tumor Debulking\nPatient: Harriet Cole\n1. GA / Rigid Bronch.\n2. Tumor found in bronchus intermedius.\n3. 85% obstruction.\n4. Cored out with rigid scope.\n5. Removed fragments.\n6. Bleeding controlled.\nPlan: Oncology admission.",
            5: "Harriet Cole 62F tumor in the bronchus intermedius causing breathing trouble. Rigid bronch done under GA. It was blocking like 85 percent. Cored it out with the barrel and used the sucker to get the pieces. Microdebrider to clean the walls. Got it open pretty good maybe 30 percent left. No stent needed chemo coming up. Admitted to onc.",
            6: "A 62-year-old female with a bronchus intermedius tumor underwent rigid bronchoscopy for mechanical debulking. The tumor, causing 85% obstruction, was cored out using the rigid barrel. Large fragments were removed with suction and forceps, and a microdebrider was used for residual tissue. The final airway lumen showed 30% residual narrowing. Mild bleeding was controlled. The patient was admitted to the oncology ward.",
            7: "[Indication]\nBronchus intermedius tumor, acute dyspnea.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\n85% obstruction in BI. Mechanical debulking via coring and microdebrider. Lumen restored to ~70% patency.\n[Plan]\nOncology ward, systemic therapy.",
            8: "Ms. Cole was admitted with worsening dyspnea due to a tumor in the bronchus intermedius. We performed rigid bronchoscopy to debulk the lesion. The tumor was friable and obstructed 85% of the airway. We mechanically cored out the tumor and used a microdebrider to clean the airway walls. We achieved a significant improvement in airway patency, leaving about 30% narrowing.",
            9: "Intervention: Rigid endoscopy with tumor excision.\nSite: Bronchus intermedius.\nTechnique: The obstructing mass was resected using mechanical coring and debridement tools. The airway channel was widened. Hemostasis was secured."
        },
        6: { # Walter Young - Emergent Carina/Trachea
            1: "Indication: Emergent airway obstruction, distress.\nProcedure: Rigid bronch, debulking.\nFindings: >90% obstruction distal trachea/carina.\nAction: Rapid coring/forceps removal. Microdebrider at carina.\nResult: 35% residual narrowing. No stent (unstable).\nDisp: MICU intubated.",
            2: "OPERATIVE SUMMARY: 80-year-old male with emergent central airway obstruction. Rigid bronchoscopy was performed under general anesthesia. A large, friable tumor was identified at the distal trachea and carina, causing >90% obstruction. Emergent mechanical debulking was performed using rigid coring and forceps to restore ventilation. Residual tumor at the carina was excised with a microdebrider. Due to hemodynamic instability, no stent was placed. The airway was patent with 35% residual narrowing.",
            3: "Code: 31640 (Excision of tumor).\nContext: Emergent.\nSite: Distal Trachea and Carina.\nTechnique: Rigid bronchoscopy with mechanical debulking.\nJustification: Critical airway compromise requiring immediate excision to restore ventilation.",
            4: "Procedure: Emergent Rigid Bronch\nPatient: Walter Young\n1. GA / Jet vent / Pressors.\n2. Critical obstruction distal trachea (>90%).\n3. Rapid debulking with coring/forceps.\n4. Airway established.\n5. Microdebrider cleanup.\n6. Hemodynamically unstable - no stent.\nPlan: MICU.",
            5: "Walter Young 80M came in crashing respiratory distress. Tumor at the carina blocking everything. We rushed to OR for rigid bronch. Scraped out the tumor fast to get air in. Used the coring method and forceps. Bleeding was moderate but we managed. BP dropped a few times had to use pressors. Got it open enough to ventilate. Sent to MICU still intubated.",
            6: "An 80-year-old male presented with emergent central airway obstruction and acute respiratory distress. Emergent rigid bronchoscopy was performed. A large tumor at the distal trachea and carina caused >90% obstruction. Rapid mechanical debulking using rigid coring and forceps restored airway patency. A microdebrider was used for residual tumor. Due to hemodynamic instability, no stent was placed. The patient remained intubated and was transferred to the MICU.",
            7: "[Indication]\nEmergent central airway obstruction, respiratory distress.\n[Anesthesia]\nGeneral, rigid bronchoscopy, pressors.\n[Description]\n>90% block distal trachea/carina. Rapid mechanical debulking performed. Airway patency restored. No stent placed.\n[Plan]\nMICU, hemodynamic stabilization.",
            8: "Mr. Young presented in acute respiratory distress due to a tracheal tumor. We performed an emergent rigid bronchoscopy. The tumor was critically obstructing the distal trachea and carina. We rapidly debulked the tumor using coring and forceps to establish an airway. Although the patient experienced transient hypotension, we successfully restored patency. We decided against stenting at this time due to his instability.",
            9: "Procedure: Emergent rigid endoscopy with mass resection.\nFinding: Critical stenosis of the carina.\nAction: The obstructing lesion was urgently excised to permit ventilation. Hemodynamic support was required. The airway was recanalized."
        },
        7: { # Chloe Harris - Right Mainstem
            1: "Indication: Right mainstem tumor, incidental.\nProcedure: Rigid bronch, excision.\nFindings: Sessile lesion, proximal RMS, 60% obs.\nAction: Snare, coring, microdebrider.\nResult: 10% residual. Complete removal.\nDisp: Home.",
            2: "PROCEDURE NOTE: The patient underwent rigid bronchoscopy for a right mainstem endobronchial tumor. A sessile lesion was visualized on the lateral wall of the proximal right mainstem bronchus, causing 60% narrowing. Mechanical excision was accomplished using snare resection, followed by rigid coring and microdebrider debridement. The tumor was completely removed, leaving minimal residual irregularity.",
            3: "Billing: 31640 (Bronchoscopy with excision).\nSite: Right Mainstem Bronchus.\nMethod: Rigid bronchoscopy with snare and microdebrider.\nOutcome: Restoration of patent airway.",
            4: "Resident Note: Tumor Excision\nPatient: Chloe Harris\n1. GA / Rigid Scope.\n2. RMS tumor identified (60%).\n3. Snare resection.\n4. Microdebrider to base.\n5. Rigid coring.\n6. No bleeding.\nPlan: Discharge home.",
            5: "Chloe Harris 55F right mainstem tumor found on CT. Did the rigid bronch to take it out. Sessile lesion on the lateral wall. Snared what we could then cored the rest and used the microdebrider. Got it all out looks clean. No bleeding really. She did fine going home.",
            6: "A 55-year-old female underwent rigid bronchoscopy for a right mainstem endobronchial tumor. A sessile lesion causing 60% narrowing was identified. Mechanical debulking was performed using snare resection, rigid coring, and a microdebrider. All visible tumor was removed, and the final lumen showed 10% residual irregularity. Complications were minimal, and the patient was discharged home.",
            7: "[Indication]\nRight mainstem endobronchial tumor.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\nSessile lesion proximal RMS (60% block). Snare resection and mechanical debulking performed. Tumor excised.\n[Plan]\nOutpatient discharge, f/u 2 weeks.",
            8: "Ms. Harris came in for removal of a right mainstem tumor found incidentally. We performed a rigid bronchoscopy. The tumor was sessile and obstructed about 60% of the airway. We used a combination of snare resection, rigid coring, and microdebrider to remove the lesion completely. The airway is now widely patent with minimal residual irregularity.",
            9: "Intervention: Rigid endoscopy with lesion resection.\nLocation: Right mainstem.\nTechnique: The mass was excised using snare and mechanical debridement. The airway was fully opened. Hemostasis was excellent."
        },
        8: { # Xavier Bennett - Mid-trachea SCC
            1: "Indication: Mid-tracheal SCC, dyspnea.\nProcedure: Rigid bronch, debulking.\nFindings: Fungating mass posterior wall, 75% obs.\nAction: Coring, snare, microdebrider.\nResult: Patent lumen (25% residual). No stent.\nDisp: Admit floor.",
            2: "OPERATIVE REPORT: 69-year-old male with mid-tracheal squamous cell carcinoma. Rigid bronchoscopy was performed. A fungating mass was noted on the posterior mid-tracheal wall, causing 75% stenosis. The tumor was debulked utilizing rigid coring, snare excision, and microdebrider until a patent airway was achieved. No stent was placed due to adequate residual lumen and planned radiation therapy.",
            3: "Code 31640: Excision of tracheal tumor.\nTechnique: Rigid bronchoscopy with mechanical debulking.\nFindings: 75% obstruction of mid-trachea.\nOutcome: Successful restoration of airway patency.",
            4: "Procedure: Tracheal Debulking\nPatient: Xavier Bennett\n1. General Anesthesia.\n2. Rigid bronchoscopy.\n3. Mid-tracheal mass (SCC).\n4. Debulked with coring/snare/microdebrider.\n5. Hemostasis confirmed.\n6. No stent.\nPlan: Admit for obs.",
            5: "Xavier Bennett 69M mid tracheal scc having trouble breathing. We went in with the rigid scope. Big fungating mass on the back wall blocking 75 percent. We cored it out and used the snare and microdebrider. Got it open pretty good. Didnt put a stent in cause he is getting radiation soon. Admitted for the night.",
            6: "A 69-year-old male with mid-tracheal squamous cell carcinoma underwent rigid bronchoscopy for mechanical debulking. A fungating mass causing 75% narrowing was identified. The tumor was excised using rigid coring, snare excision, and a microdebrider. A patent lumen was achieved, and no stent was placed. Mild bleeding was controlled. The patient was admitted for observation.",
            7: "[Indication]\nMid-tracheal SCC, symptomatic obstruction.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\n75% obstruction mid-trachea. Mechanical debulking performed. Lumen restored. No stent.\n[Plan]\nFloor admission, radiation oncology consult.",
            8: "Mr. Bennett presented with dyspnea due to a mid-tracheal tumor. We performed rigid bronchoscopy to debulk the lesion. The tumor was fungating and obstructed 75% of the trachea. We used rigid coring, snare excision, and a microdebrider to remove the tumor and restore the airway. We decided against stenting as he is scheduled for radiation therapy.",
            9: "Procedure: Rigid endoscopy with tumor excision.\nDiagnosis: Squamous cell carcinoma of the trachea.\nAction: The obstructing lesion was resected using mechanical tools. Airway patency was re-established. Hemostasis was secured."
        },
        9: { # Evelyn Ross - Distal Trachea Recurrence
            1: "Indication: Recurrent distal tracheal tumor.\nProcedure: Rigid bronch, debulking.\nFindings: Nodular tumor above carina, 70% obs.\nAction: Coring, microdebrider, forceps.\nResult: 25% residual. No stent.\nDisp: Admit floor.",
            2: "PROCEDURE NOTE: The patient presented with recurrent distal tracheal tumor following chemoradiation. Rigid bronchoscopy revealed an irregular nodular tumor at the distal trachea, just proximal to the carina, causing 70% narrowing. Mechanical debulking was performed using rigid coring, microdebrider, and forceps to excise tissue and widen the lumen. A patent airway was restored with 25% residual narrowing.",
            3: "Billing: 31640 (Excision of tumor).\nSite: Distal Trachea.\nContext: Recurrence post-chemoradiation.\nMethod: Rigid bronchoscopy mechanical debulking.\nOutcome: Improvement in airway caliber.",
            4: "Resident Note: Tumor Debulking\nPatient: Evelyn Ross\n1. GA / Rigid Scope.\n2. Recurrent tumor distal trachea.\n3. 70% obstruction.\n4. Cored out and microdebrided.\n5. Hemostasis achieved.\nPlan: Admit for observation.",
            5: "Evelyn Ross 73F recurrent tumor in distal trachea after radiation. Having trouble breathing. Rigid bronch done. Saw the nodular tumor above the carina blocking 70 percent. Scraped it out with the rigid and used the microdebrider. Opened it up nicely. No stent this time. Keeping her overnight.",
            6: "A 73-year-old female with recurrent distal tracheal tumor underwent rigid bronchoscopy for debulking. An irregular nodular tumor causing 70% narrowing was identified. Mechanical debulking using rigid coring, microdebrider, and forceps was performed. The airway lumen was widened with 25% residual narrowing. No stent was placed. The patient was admitted for observation.",
            7: "[Indication]\nRecurrent distal tracheal tumor, dyspnea.\n[Anesthesia]\nGeneral, rigid bronchoscopy.\n[Description]\n70% obstruction distal trachea. Mechanical debulking performed. Lumen restored to ~75% patency.\n[Plan]\nFloor admission, oncology follow-up.",
            8: "Ms. Ross returned with a recurrence of her distal tracheal tumor. We performed rigid bronchoscopy to improve her airway. The tumor was nodular and obstructed 70% of the trachea. We mechanically debulked the lesion using coring and a microdebrider. We successfully widened the lumen and decided not to place a stent given the prior radiation changes.",
            9: "Intervention: Rigid endoscopy with mass resection.\nSite: Distal trachea.\nAction: The recurrent lesion was excised using mechanical debridement. The airway channel was enlarged. Hemostasis was maintained."
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
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            # Handle potential missing index in dictionary safely
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing text variation for Note {idx}, Style {style_num}")
                note_entry["note_text"] = "Text generation error."

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
    output_filename = output_dir / "synthetic_ip_notes_part_057.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()