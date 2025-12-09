import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "consolidated_verified_notes_v2_8_part_055_part2.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of stylistic variations for the 10 notes in Part 055.
    Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Barbara Williams - Stent LMS (31636, 31641)
            1: "• Indication: Esophageal ca, tracheal invasion.\n• Anesthesia: GA, Jet vent.\n• Action: Rigid scope inserted. 72% obstruction LMS.\n• APC ablation performed on tumor.\n• Novatech Dumon stent (14x60mm) deployed LMS.\n• Result: Patent airway, <15% obstruction.\n• Plan: Admit.",
            2: "Operative Report: The patient, an 81-year-old female with advanced esophageal carcinoma complicated by tracheal invasion, was brought to the operating theater. Under general anesthesia utilizing jet ventilation, rigid bronchoscopic interrogation revealed a significant obstruction of the left mainstem bronchus. Argon Plasma Coagulation (APC) was utilized to ablate the intraluminal tumor burden. Subsequently, a 14x60mm Novatech silicone Dumon stent was precisely deployed. Post-deployment evaluation confirmed excellent stent expansion and restoration of airway patency.",
            3: "Procedure: Therapeutic Bronchoscopy (31636, 31641).\nTechnique: Rigid bronchoscopy used to access the airway. Tumor destruction performed using APC (31641) to prepare the bed. Measurements taken. A bronchial stent (Novatech Dumon, 14x60mm) was then inserted into the Left Mainstem (31636). Visual confirmation of patency and position achieved.",
            4: "Procedure Note\nAttending: Dr. Martinez\nIndication: CAO due to esophageal cancer.\nSteps:\n1. GA/Jet ventilation.\n2. Rigid bronchoscopy.\n3. APC ablation of tumor in LMS.\n4. Placement of 14x60mm Dumon stent in LMS.\n5. Confirmed patency.\nPlan: Admit for observation.",
            5: "pt brought to room for bronchoscopy under general anesthesia jet ventilation used. rigid scope went down found the obstruction in the left mainstem like 72%. used apc to burn the tumor back a bit then put in a novatech stent 14 by 60 mm. looks good now open. minimal bleeding recovery then floor.",
            6: "Under general anesthesia with jet ventilation rigid bronchoscopy performed APC used for tumor ablation prior to stent placement Airway measured and Novatech Silicone Dumon stent 14x60mm deployed in Left mainstem Stent position confirmed with good expansion and patency Post procedure obstruction 14% No complications EBL minimal Disposition Recovery then floor admission for overnight observation.",
            7: "[Indication]\nEsophageal cancer with tracheal invasion causing LMS obstruction.\n[Anesthesia]\nGeneral anesthesia, jet ventilation.\n[Description]\nRigid bronchoscopy. APC tumor ablation performed. Novatech Dumon stent (14x60mm) deployed in Left Mainstem. Obstruction reduced from 72% to ~14%.\n[Plan]\nAdmit for observation. F/U 4-6 weeks.",
            8: "The patient was placed under general anesthesia with jet ventilation for a rigid bronchoscopy. We identified the obstruction in the left mainstem caused by esophageal cancer invasion. We utilized APC for tumor ablation to clear the pathway. Following this, we measured the airway and deployed a Novatech Silicone Dumon stent, sized 14x60mm, into the Left Mainstem. The stent expanded well, and patency was confirmed with minimal residual obstruction.",
            9: "Under general anesthesia, rigid bronchoscopy was executed. APC was utilized for tumor destruction before stent insertion. The airway was gauged, and a Novatech Silicone Dumon stent (14x60mm) was positioned in the Left mainstem. Stent location was verified with adequate expansion and patency. Post-procedure blockage was ~14%. No adverse events."
        },
        1: { # Donald Thomas - Laser Debulking BI (31640)
            1: "• Dx: Esophageal ca, tracheal invasion.\n• Anesthesia: General.\n• Procedure: Rigid bronch.\n• 79% obstruction Bronchus Intermedius (BI).\n• Laser ablation/excision performed. Multiple passes.\n• Residual: 15%.\n• EBL: 50mL.\n• Plan: ICU.",
            2: "Operative Narrative: The patient, presenting with esophageal carcinoma and tracheal invasion, underwent rigid bronchoscopy under general anesthesia. An endobronchial tumor mass was visualized obstructing the Bronchus Intermedius (BI). Laser ablation was meticulously performed to excise the tumor in a sequential fashion. Maximal debulking was achieved through multiple passes, resulting in a patent airway with minimal residual stenosis. Hemostasis was secured.",
            3: "Billing Justification: Bronchoscopy with excision of tumor (31640). The rigid bronchoscope was introduced. The tumor at the Bronchus Intermedius was identified. Laser energy was applied to excise the tissue. Debridement was performed to remove the tumor mass (debulking). Adequate hemostasis was verified.",
            4: "Resident Note\nPatient: Donald Thomas.\nProcedure: Rigid Bronchoscopy/Debulking.\nStaff: Dr. Lee.\nSteps:\n1. Induced GA.\n2. Identified tumor at BI.\n3. Performed laser ablation/excision.\n4. Debulked tumor sequentially.\n5. Hemostasis achieved.\nPlan: ICU monitoring.",
            5: "procedure note for mr thomas rigid bronch done under ga found tumor in the bronchus intermedius blocking about 79% used the laser to cut it out and remove it took a few passes but looks much better now maybe 15% left bleeding was minimal 50ml sent tissue to lab going to icu tonight.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at BI Laser ablation performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Post procedure 15% residual obstruction EBL 50mL Hemostasis achieved Specimens sent for histology Disposition Recovery then ICU observation overnight.",
            7: "[Indication]\nEsophageal cancer with airway invasion.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy to BI. 79% obstruction. Laser ablation and excision of tumor performed. Multiple passes for debulking. Obstruction reduced to 15%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy under general anesthesia. Upon inspection, an endobronchial tumor was identified obstructing the Bronchus Intermedius. We proceeded with laser ablation to excise the tumor sequentially. We made multiple passes to ensure maximal debulking was achieved. The post-procedure obstruction was estimated at 15%, and hemostasis was secured with an estimated blood loss of 50mL.",
            9: "Under general anesthesia, rigid bronchoscopy was conducted. An endobronchial lesion was spotted at the BI. Laser destruction was carried out with sequential tumor extraction. Several passes were executed to attain maximal debulking. Post-procedure residual obstruction was ~15%. Hemostasis was attained."
        },
        2: { # Melissa Young - Stent BI (31636, 31641)
            1: "• Indication: Thyroid ca, tracheal compression.\n• Anesthesia: GA, Jet vent.\n• 83% obstruction BI.\n• APC ablation performed.\n• Ultraflex Covered Stent (20x40mm) placed BI.\n• Patency confirmed.\n• Plan: Admit.",
            2: "Procedure Note: Ms. Young, with a history of thyroid carcinoma causing tracheal compression, was brought for rigid bronchoscopy. Following induction of general anesthesia and jet ventilation, the airway was examined, revealing severe obstruction at the Bronchus Intermedius. Argon Plasma Coagulation (APC) was applied for tumor destruction. An Ultraflex SEMS (Covered, 20x40mm) was then accurately deployed to stent the BI. Post-deployment imaging confirmed restoration of airway caliber.",
            3: "Codes: 31641 (Destruction), 31636 (Stent). Rigid bronchoscopy performed. Tumor tissue at the BI was ablated using APC to facilitate stent entry. An Ultraflex covered stent (20x40mm) was inserted into the Bronchus Intermedius to maintain patency. Excellent result achieved.",
            4: "Procedure: Therapeutic Bronchoscopy\nSupervision: Dr. Lee\nSteps:\n1. GA / Jet ventilation.\n2. Rigid scope to BI.\n3. APC used for tumor ablation.\n4. Ultraflex Stent (20x40mm) deployed.\n5. Checked positioning.\nPlan: Floor admission.",
            5: "melissa young here for the stent placement due to thyroid cancer pushing on the airway rigid bronch used apc to burn some tumor away first then put in the ultraflex stent 20 by 40 in the bronchus intermedius opened up nicely down to 24% obstruction no complications watchful waiting on the floor.",
            6: "Under general anesthesia with jet ventilation rigid bronchoscopy performed APC used for tumor ablation prior to stent placement Airway measured and Ultraflex SEMS Covered stent 20x40mm deployed in Bronchus intermedius Stent position confirmed with good expansion and patency Post procedure obstruction 24% No complications EBL minimal.",
            7: "[Indication]\nThyroid cancer, tracheal/bronchial compression.\n[Anesthesia]\nGeneral, jet ventilation.\n[Description]\nAPC ablation of tumor at BI. Ultraflex Covered Stent (20x40mm) deployed. Obstruction reduced from 83% to 24%.\n[Plan]\nAdmit overnight.",
            8: "Under general anesthesia and utilizing jet ventilation, we performed a rigid bronchoscopy. We utilized APC for tumor ablation to prepare the site before stent placement. We measured the airway and deployed an Ultraflex SEMS covered stent (20x40mm) into the Bronchus Intermedius. We confirmed the stent position with good expansion and patency, noting the post-procedure obstruction was reduced to approximately 24%.",
            9: "Under general anesthesia with jet ventilation, rigid bronchoscopy was undertaken. APC was employed for tumor destruction preceding stent insertion. The airway was sized and an Ultraflex SEMS Covered stent (20x40mm) was positioned in the Bronchus intermedius. Stent location was verified with favorable expansion and patency."
        },
        3: { # Anthony Taylor - Forceps Debulking BI (31641)
            1: "• Indication: Mets lung ca, BI obstruction (60%).\n• Anesthesia: GA, Rigid bronch.\n• Procedure: Mechanical debulking w/ forceps.\n• APC/Laser used for hemostasis/base ablation.\n• Result: 32% obstruction.\n• Plan: ICU.",
            2: "Operative Report: Mr. Taylor presented with metastatic lung carcinoma compromising the Bronchus Intermedius. Under general anesthesia, rigid bronchoscopy was initiated. The tumor was mechanically debulked using rigid biopsy forceps in a sequential manner. Following mechanical removal, APC and laser modalities were applied to the tumor base for ablation and hemostasis. The airway caliber was significantly improved.",
            3: "Billing: 31641 (Destruction of tumor). Rigid bronchoscopy facilitated access to the BI. Mechanical debulking performed with biopsy forceps. Additional destruction of the tumor base and hemostasis achieved using APC and laser thermal energy. Multiple modalities required for therapeutic effect.",
            4: "Resident Procedure Note\nPatient: Anthony Taylor\nProcedure: Rigid Bronchoscopy with Debulking.\nSteps:\n1. GA induced.\n2. Tumor identified at BI.\n3. Mechanical debulking (forceps).\n4. APC/Laser for base ablation.\n5. Hemostasis confirmed.\nPlan: ICU.",
            5: "patient anthony taylor had the debulking done today rigid scope used forceps to grab the tumor chunks out of the bi multiple passes to get it open then used the laser and apc to stop the bleeding and burn the base minimal bleeding really tumor went from 60% to 32% obstruction icu for monitoring.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at BI Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Additional APC laser used for hemostasis and tumor base ablation Post procedure 32% residual obstruction EBL 75mL Hemostasis achieved.",
            7: "[Indication]\nMetastatic lung cancer, BI obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Mechanical debulking of BI tumor with forceps. APC/Laser ablation of base. Obstruction reduced 60% -> 32%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy under general anesthesia. The endobronchial tumor at the Bronchus Intermedius was identified and debulked using rigid biopsy forceps for sequential tumor removal. We made multiple passes to achieve maximal debulking. Additionally, APC and laser were used for hemostasis and tumor base ablation. The residual obstruction was approximately 32%, and hemostasis was achieved.",
            9: "Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm was found at the BI. Rigid bronchoscopy debulking with biopsy forceps was carried out with sequential tumor extraction. Several passes were done to attain maximal debulking. Supplemental APC/laser was utilized for hemostasis and tumor base destruction."
        },
        4: { # Thomas Allen - Tracheal Stent (31631)
            1: "• Indication: Lung adenocarcinoma, Tracheal CAO (76%).\n• Anesthesia: GA, Jet vent.\n• Procedure: Rigid bronch.\n• Stent: Novatech Dumon (20x60mm) in Trachea.\n• Result: 15% residual.\n• Plan: Admit.",
            2: "Procedure Narrative: Mr. Allen, diagnosed with primary lung adenocarcinoma and central airway obstruction, underwent rigid bronchoscopy. General anesthesia with jet ventilation was employed. Measurement of the tracheal stenosis dictated the selection of a 20x60mm Novatech silicone Dumon stent. The stent was deployed without complication, resulting in immediate relief of the obstruction and restoration of tracheal patency.",
            3: "Coding: 31631 (Placement of Tracheal Stent). Rigid bronchoscopy performed to access the trachea. The airway was sized. A silicone stent (Novatech Dumon, 20x60mm) was placed in the trachea to treat the obstruction. Position confirmed.",
            4: "Procedure Note\nStaff: Dr. Chen\nIndication: Tracheal obstruction.\nSteps:\n1. GA/Jet ventilation.\n2. Rigid scope insertion.\n3. Trachea measured.\n4. Novatech Dumon 20x60mm deployed.\n5. Expansion confirmed.\nPlan: Floor admission.",
            5: "thomas allen procedure note rigid bronchoscopy for the tracheal tumor we used jet ventilation general anesthesia measured the airway and put in a novatech dumon stent 20 by 60 mm right in the trachea opened up good from 76% down to 15% blockage no issues admit to floor.",
            6: "Under general anesthesia with jet ventilation rigid bronchoscopy performed Airway measured and Novatech Silicone Dumon stent 20x60mm deployed in Trachea Stent position confirmed with good expansion and patency Post procedure obstruction 15% No complications EBL minimal Disposition Recovery then floor admission for overnight observation.",
            7: "[Indication]\nLung adenocarcinoma, Tracheal obstruction.\n[Anesthesia]\nGeneral, jet ventilation.\n[Description]\nRigid bronchoscopy. Novatech Silicone Dumon stent (20x60mm) deployed in Trachea. Obstruction reduced 76% -> 15%.\n[Plan]\nAdmit for observation.",
            8: "Under general anesthesia with jet ventilation, a rigid bronchoscopy was performed. We measured the airway and deployed a Novatech Silicone Dumon stent (20x60mm) into the Trachea. The stent position was confirmed with good expansion and patency. Post-procedure obstruction was estimated at 15%. There were no complications, and estimated blood loss was minimal.",
            9: "Under general anesthesia with jet ventilation, rigid bronchoscopy was conducted. The airway was sized and a Novatech Silicone Dumon stent (20x60mm) was positioned in the Trachea. Stent placement was verified with good expansion and patency. Post-procedure blockage was ~15%. No adverse events."
        },
        5: { # Ronald Young - Cryoextraction RMS (31641)
            1: "• Indication: SCC, RMS obstruction (77%).\n• Anesthesia: GA.\n• Procedure: Rigid bronch, Cryoextraction.\n• APC/Laser for base.\n• Result: 22% residual.\n• Plan: ICU.",
            2: "Operative Note: Mr. Young presented with squamous cell carcinoma compromising the Right Mainstem (RMS). Rigid bronchoscopy was performed under general anesthesia. The tumor was debulked via cryoextraction, allowing for the removal of large tissue specimens. Following cryotherapy, APC and laser were utilized to ablate the tumor base and ensure hemostasis. The airway caliber was markedly improved.",
            3: "Billing: 31641 (Destruction/Relief of obstruction). Rigid bronchoscopy performed. Cryoextraction (destruction) used to remove tumor from RMS. Secondary destruction performed with APC/Laser to the base. Hemostasis achieved.",
            4: "Resident Note\nPatient: Ronald Young\nProcedure: Cryo-debulking.\nSteps:\n1. GA induced.\n2. Tumor visualization RMS.\n3. Cryoextraction passes.\n4. APC/Laser touch-up.\n5. Hemostasis.\nPlan: ICU.",
            5: "ronald young here for the airway obstruction rigid bronch used cryo probe to freeze and pull out chunks of the tumor in the right mainstem took a few tries but got most of it out used laser and apc to clean up the base and stop bleeding obstruction down to 22% going to icu.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at RMS Cryoextraction performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Additional APC laser used for hemostasis and tumor base ablation Post procedure 22% residual obstruction EBL 50mL Hemostasis achieved.",
            7: "[Indication]\nSCC with airway compromise (RMS).\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Cryoextraction of RMS tumor. APC/Laser ablation of base. Obstruction reduced 77% -> 22%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy under general anesthesia. An endobronchial tumor was identified at the Right Mainstem (RMS). Cryoextraction was performed with sequential tumor removal. We made multiple passes to achieve maximal debulking. Additionally, APC and laser were used for hemostasis and tumor base ablation. The post-procedure residual obstruction was approximately 22%.",
            9: "Under general anesthesia, rigid bronchoscopy was undertaken. Endobronchial neoplasm was identified at the RMS. Cryoextraction was executed with sequential tumor extraction. Multiple passes were done to attain maximal debulking. Supplemental APC/laser was utilized for hemostasis and tumor base destruction."
        },
        6: { # Jason Green - Microdebrider LMS (31640)
            1: "• Indication: Thyroid ca, LMS obstruction (76%).\n• Anesthesia: GA.\n• Procedure: Microdebrider tumor removal.\n• Multiple passes.\n• Result: 31% residual.\n• Plan: ICU.",
            2: "Procedure Narrative: Mr. Green underwent rigid bronchoscopy for management of tracheal compression/invasion by thyroid carcinoma affecting the Left Mainstem (LMS). Under general anesthesia, the microdebrider was employed to shave and aspirate the endobronchial tumor component. Sequential passes resulted in significant debulking and improvement of the airway lumen.",
            3: "Code: 31640 (Excision of tumor). Rigid bronchoscopy provided access. A microdebrider tool was used to excise and remove tumor tissue from the Left Mainstem bronchus. Hemostasis controlled.",
            4: "Procedure Note\nStaff: Dr. Davis\nIndication: LMS obstruction.\nSteps:\n1. GA.\n2. Rigid scope.\n3. Microdebrider excision of LMS tumor.\n4. Multiple passes.\n5. Hemostasis.\nPlan: ICU.",
            5: "jason green procedure note rigid bronchoscopy for thyroid cancer blocking the left mainstem used the microdebrider to shave it down worked well took multiple passes bleeding was fine about 50ml tumor went from 76% to 31% obstruction icu tonight.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at LMS Microdebrider assisted tumor removal performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Post procedure 31% residual obstruction EBL 50mL Hemostasis achieved Specimens sent for histology.",
            7: "[Indication]\nThyroid cancer, LMS obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Microdebrider excision of LMS tumor. Multiple passes. Obstruction reduced 76% -> 31%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy under general anesthesia. An endobronchial tumor was identified at the Left Mainstem (LMS). We utilized a microdebrider for tumor removal, performing sequential excision. Multiple passes were made to achieve maximal debulking. The post-procedure residual obstruction was approximately 31%. Estimated blood loss was 50mL, and hemostasis was achieved.",
            9: "Under general anesthesia, rigid bronchoscopy was conducted. Endobronchial lesion was spotted at the LMS. Microdebrider-assisted tumor extraction was carried out with sequential tumor excision. Several passes were executed to attain maximal debulking. Post-procedure residual obstruction was ~31%."
        },
        7: { # Rebecca Miller - Forceps/Balloon RLL (31640)
            1: "• Indication: Malignant CAO, RLL (72%).\n• Anesthesia: GA.\n• Procedure: Rigid bronch debulking (forceps).\n• Balloon dilation for residual stenosis.\n• Result: 15% residual.\n• Plan: ICU.",
            2: "Operative Report: Ms. Miller presented with malignant central airway obstruction involving the RLL orifice. Rigid bronchoscopy was performed under general anesthesia. The tumor was mechanically debulked using biopsy forceps. Following tumor removal, balloon dilation was performed to address residual stenosis and optimize airway patency.",
            3: "Billing: 31640 (Excision of tumor). Rigid bronchoscopy used. Tumor excised from RLL orifice using biopsy forceps (debulking). Balloon dilation performed as an adjunct to the excision to maximize patency (included in 31640 logic for this session/site or separate depending on payer, here focused on excision).",
            4: "Resident Note\nPatient: Rebecca Miller\nProcedure: Debulking + Dilation.\nSteps:\n1. GA.\n2. Tumor at RLL orifice.\n3. Forceps debulking.\n4. Balloon dilation.\n5. Hemostasis.\nPlan: ICU.",
            5: "rebecca miller procedure note rigid bronch for the rll tumor obstruction was 72% used the biopsy forceps to pull it out piece by piece then used a balloon to dilate the rest open looks much better now 15% residual bleeding controlled sent samples to lab.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at RLL orifice Rigid bronchoscopy debulking with biopsy forceps performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Balloon dilation performed for residual stenosis Post procedure 15% residual obstruction EBL 75mL Hemostasis achieved.",
            7: "[Indication]\nMalignant CAO, RLL orifice.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Mechanical forceps debulking of RLL tumor. Balloon dilation performed. Obstruction reduced 72% -> 15%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy under general anesthesia. An endobronchial tumor was identified at the RLL orifice. We performed rigid bronchoscopy debulking with biopsy forceps for sequential tumor removal. Multiple passes were made to achieve maximal debulking. Additionally, balloon dilation was performed for residual stenosis. The post-procedure residual obstruction was approximately 15%.",
            9: "Under general anesthesia, rigid bronchoscopy was executed. Endobronchial neoplasm was identified at the RLL orifice. Rigid bronchoscopy debulking with biopsy forceps was carried out with sequential tumor extraction. Several passes were done to attain maximal debulking. Balloon dilation was executed for residual stenosis."
        },
        8: { # Robert Johnson - Microdebrider BI (31640)
            1: "• Indication: Mets lung ca, BI (85%).\n• Anesthesia: GA.\n• Procedure: Microdebrider excision.\n• Multiple passes.\n• Result: 25% residual.\n• Plan: ICU.",
            2: "Procedure Narrative: Mr. Johnson presented with high-grade obstruction of the Bronchus Intermedius (BI) due to metastatic lung cancer. Rigid bronchoscopy was undertaken with general anesthesia. The microdebrider was utilized to excise the tumor mass sequentially. Maximal debulking was pursued, resulting in a marked reduction of the obstruction from 85% to 25%.",
            3: "Code: 31640 (Excision). Rigid bronchoscopy performed. Microdebrider tool used to excise tumor tissue from the Bronchus Intermedius. Debulking achieved.",
            4: "Procedure Note\nStaff: Dr. Davis\nIndication: BI obstruction.\nSteps:\n1. GA.\n2. Scope to BI.\n3. Microdebrider debulking.\n4. Hemostasis.\nPlan: ICU.",
            5: "robert johnson procedure note rigid bronch used the microdebrider on the tumor in the bronchus intermedius was 85% blocked cleaned it out pretty good down to 25% took a few passes bleeding was minimal 50ml icu for observation.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at BI Microdebrider assisted tumor removal performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Post procedure 25% residual obstruction EBL 50mL Hemostasis achieved Specimens sent for histology.",
            7: "[Indication]\nMetastatic lung cancer, BI obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Microdebrider excision of BI tumor. Multiple passes. Obstruction reduced 85% -> 25%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy under general anesthesia. An endobronchial tumor was identified at the Bronchus Intermedius (BI). We utilized a microdebrider for tumor removal, performing sequential excision. Multiple passes were made to achieve maximal debulking. The post-procedure residual obstruction was approximately 25%. Estimated blood loss was 50mL, and hemostasis was achieved.",
            9: "Under general anesthesia, rigid bronchoscopy was conducted. Endobronchial lesion was spotted at the BI. Microdebrider-assisted tumor extraction was carried out with sequential tumor excision. Several passes were executed to attain maximal debulking. Post-procedure residual obstruction was ~25%."
        },
        9: { # Stephanie Allen - Microdebrider/APC LMS (31641)
            1: "• Indication: Mets lung ca, LMS (62%).\n• Anesthesia: GA.\n• Procedure: Microdebrider debulking.\n• APC/Laser for base/hemostasis.\n• Result: 39% residual.\n• Plan: ICU.",
            2: "Operative Note: Ms. Allen underwent rigid bronchoscopy for metastatic disease obstructing the Left Mainstem (LMS). Under general anesthesia, the microdebrider was used for initial tumor excision. Following mechanical removal, APC and laser therapies were applied to the tumor base to ensure complete ablation and hemostasis. The airway was successfully recanalized.",
            3: "Billing: 31641 (Destruction of tumor). Rigid bronchoscopy performed. Microdebrider used for debulking (excision). APC and Laser used for destruction of the tumor base and hemostasis. Combination of modalities supports therapeutic coding.",
            4: "Resident Note\nPatient: Stephanie Allen\nProcedure: Microdebrider + APC.\nSteps:\n1. GA.\n2. LMS tumor visualized.\n3. Microdebrider excision.\n4. APC/Laser ablation.\n5. Hemostasis.\nPlan: ICU.",
            5: "stephanie allen procedure note rigid bronch for lms tumor microdebrider used to debulk it then used apc and laser to burn the rest and stop bleeding went from 62% to 39% obstruction no complications icu for the night.",
            6: "Under general anesthesia rigid bronchoscopy performed Endobronchial tumor identified at LMS Microdebrider assisted tumor removal performed with sequential tumor removal Multiple passes performed to achieve maximal debulking Additional APC laser used for hemostasis and tumor base ablation Post procedure 39% residual obstruction EBL 50mL Hemostasis achieved.",
            7: "[Indication]\nMetastatic lung cancer, LMS obstruction.\n[Anesthesia]\nGeneral.\n[Description]\nRigid bronchoscopy. Microdebrider excision of LMS tumor. APC/Laser ablation of base. Obstruction reduced 62% -> 39%.\n[Plan]\nICU admission.",
            8: "We performed a rigid bronchoscopy under general anesthesia. An endobronchial tumor was identified at the Left Mainstem (LMS). We utilized a microdebrider for tumor removal, performing sequential excision. Multiple passes were made to achieve maximal debulking. Additionally, APC and laser were used for hemostasis and tumor base ablation. The post-procedure residual obstruction was approximately 39%.",
            9: "Under general anesthesia, rigid bronchoscopy was undertaken. Endobronchial neoplasm was identified at the LMS. Microdebrider-assisted tumor extraction was executed with sequential tumor excision. Multiple passes were done to attain maximal debulking. Supplemental APC/laser was utilized for hemostasis and tumor base destruction."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data to replace names and ages for the 10 source notes.
    """
    return [
        {"idx": 0, "orig_name": "Barbara Williams", "orig_age": 81, "names": ["Alice Smith", "Mary Johnson", "Patricia Brown", "Linda Davis", "Elizabeth Miller", "Barbara Wilson", "Susan Moore", "Jessica Taylor", "Sarah Anderson"]},
        {"idx": 1, "orig_name": "Donald Thomas", "orig_age": 76, "names": ["James Jackson", "John White", "Robert Harris", "Michael Martin", "William Thompson", "David Garcia", "Richard Martinez", "Joseph Robinson", "Charles Clark"]},
        {"idx": 2, "orig_name": "Melissa Young", "orig_age": 70, "names": ["Karen Rodriguez", "Nancy Lewis", "Lisa Lee", "Betty Walker", "Margaret Hall", "Sandra Allen", "Ashley Young", "Kimberly Hernandez", "Donna King"]},
        {"idx": 3, "orig_name": "Anthony Taylor", "orig_age": 61, "names": ["Thomas Wright", "Daniel Lopez", "Paul Hill", "Mark Scott", "Donald Green", "George Adams", "Kenneth Baker", "Steven Gonzalez", "Edward Nelson"]},
        {"idx": 4, "orig_name": "Thomas Allen", "orig_age": 81, "names": ["Brian Carter", "Ronald Mitchell", "Anthony Perez", "Kevin Roberts", "Jason Turner", "Matthew Phillips", "Gary Campbell", "Timothy Parker", "Jose Evans"]},
        {"idx": 5, "orig_name": "Ronald Young", "orig_age": 58, "names": ["Larry Edwards", "Jeffrey Collins", "Frank Stewart", "Scott Sanchez", "Eric Morris", "Stephen Rogers", "Andrew Reed", "Raymond Cook", "Gregory Morgan"]},
        {"idx": 6, "orig_name": "Jason Green", "orig_age": 66, "names": ["Joshua Bell", "Jerry Murphy", "Dennis Bailey", "Walter Rivera", "Patrick Cooper", "Peter Richardson", "Harold Cox", "Douglas Howard", "Henry Ward"]},
        {"idx": 7, "orig_name": "Rebecca Miller", "orig_age": 70, "names": ["Carol Torres", "Michelle Peterson", "Emily Gray", "Helen Ramirez", "Amanda James", "Melissa Watson", "Deborah Brooks", "Stephanie Kelly", "Rebecca Sanders"]},
        {"idx": 8, "orig_name": "Robert Johnson", "orig_age": 72, "names": ["Carl Price", "Arthur Bennett", "Ryan Wood", "Roger Barnes", "Joe Ross", "Juan Henderson", "Jack Coleman", "Albert Jenkins", "Jonathan Perry"]},
        {"idx": 9, "orig_name": "Stephanie Allen", "orig_age": 56, "names": ["Sharon Powell", "Cynthia Long", "Kathleen Patterson", "Amy Hughes", "Shirley Flores", "Angela Washington", "Anna Butler", "Ruth Simmons", "Brenda Foster"]}
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
            
            # Get the specific name assigned for this variation
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            # Use safe get just in case index logic drifts
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Variation text missing for Note {idx} Style {style_num}. Using original.")
            
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
    output_filename = output_dir / "synthetic_stent_notes_part_055.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()