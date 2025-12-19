import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_084.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-9) -> Style_Index (1-9) -> Text
    # Styles: 1:Terse, 2:Academic, 3:Billing, 4:Trainee, 5:Sloppy, 6:Header-less, 7:Templated, 8:Narrative, 9:Synonym
    
    variations = {
        0: { # Jasmine Young (RML Carcinoid, Flexible, Snare/Forceps)
            1: "Indication: RML carcinoid.\nProcedure: Flex bronch, mech debulking (31640).\nFindings: 70% obstruction RML.\nActions: Snare resection + forceps debulking. No thermal ablation.\nEBL: 20cc. Cold saline hemostasis.\nPlan: D/C home.",
            2: "HISTORY: Ms. Sarah Miller presented with recurrent pneumonia secondary to a typical carcinoid tumor within the right middle lobe bronchus.\nPROCEDURE: The airway was accessed via flexible bronchoscopy under moderate sedation. The target lesion, a vascular mass occluding 70% of the RML orifice, was identified. Mechanical excision was pursued utilizing a combination of electrocautery-independent snare resection and forceps debulking. No thermal ablation modalities were employed. Hemostasis was achieved via cold saline lavage.\nIMPRESSION: Successful mechanical debulking of RML endobronchial tumor.",
            3: "Service: Bronchoscopy with tumor excision (CPT 31640).\nMethod: Mechanical debulking only.\nTools: Polypectomy Snare, Biopsy Forceps.\nTarget: Right Middle Lobe (RML) bronchus.\nDetails: Visualized obstructing mass. Used snare to resect bulk of tumor. Residual tissue removed with forceps. No laser or APC used. Hemostasis maintained with saline.\nJustification: Removal of obstructing tumor to restore airway patency.",
            4: "Procedure Note\nPatient: Emily Davis, 40F\nAttending: Dr. Farouk\nSteps:\n1. Moderate sedation initiated.\n2. LMA placed.\n3. Flex scope passed to RML.\n4. Identified carcinoid tumor.\n5. Used snare and forceps to mechanically debulk the lesion.\n6. No heat used.\n7. Bleeding controlled with saline/epi.\nPlan: Follow up in IP clinic.",
            5: "patient is jessica williams 38 female here for debulking of that carcinoid in the RML we used moderate sedation and an lma scope went down saw the tumor blocking about 70 percent used the snare to chop it out and then forceps to grab the rest no ablation or heat used just mechanical removing bleeding was minimal 20ml or so stopped with cold saline discharged home same day followup in a month",
            6: "INTERVENTIONAL PULMONOLOGY MECHANICAL DEBULKING OF CARCINOID Patient Amanda Brown 39-year-old female Date 2024-11-20 Facility Lakeshore University Hospital Indication Endobronchial typical carcinoid in right middle lobe bronchus causing recurrent pneumonia Procedure Flexible bronchoscopy with mechanical debulking excision of carcinoid CPT 31640 Anesthesia Moderate sedation with propofol and fentanyl Findings Rounded vascular mass at RML bronchus origin with 70% obstruction Interventions Snare resection and forceps debulking were used to mechanically excise and debulk the tumor No thermal ablation performed Hemostasis Controlled with cold saline short application of topical epinephrine EBL 20 mL Disposition Discharged home.",
            7: "[Indication]\nEndobronchial typical carcinoid, RML bronchus, recurrent infections.\n[Anesthesia]\nModerate sedation (Propofol/Fentanyl), LMA.\n[Description]\nFlexible bronchoscopy performed. 70% obstruction at RML origin identified. Mechanical debulking performed using snare resection and forceps excision. No thermal energy applied. Hemostasis achieved with cold saline and epinephrine.\n[Plan]\nDischarge home. Antibiotics. Clinic f/u 4 weeks.",
            8: "Ms. Ashley Wilson presented for bronchoscopic management of her RML carcinoid. Under moderate sedation, we advanced the flexible bronchoscope and located the tumor, which was causing significant obstruction. We proceeded to remove the tumor mechanically. First, we used a snare to resect the bulk of the mass, followed by forceps to clean up the remaining tissue. We did not use any thermal ablation devices. The bleeding was minor and easily managed with cold saline. She tolerated the procedure well.",
            9: "Indication: Endobronchial typical carcinoid in right middle lobe bronchus triggering recurrent pneumonia.\nProcedure: Flexible bronchoscopy with physical removal/extraction of carcinoid.\nFindings: Rounded, vascular mass at RML bronchus origin with ~70% blockage.\nInterventions: Snare cutting and forceps removal were utilized to physically excise and debulk the growth. No thermal destruction performed.\nHemostasis: Managed with chilled saline; brief use of topical epinephrine.\nDisposition: Sent home same day.",
        },
        1: { # Kevin Brooks (Tracheal Tumor, Rigid, Coring/Snare)
            1: "Indication: Tracheal tumor, dyspnea.\nApproach: Rigid bronchoscopy.\nAction: Coring and forceps debulking of proximal tracheal mass. Snare used for pedunculated portion. No ablation.\nResult: Lumen patency improved from 30% to patent.\nEBL: 15mL.\nPlan: D/C to home.",
            2: "OPERATIVE REPORT: Mr. James Anderson, presenting with stridor secondary to a proximal tracheal neoplasm, underwent rigid bronchoscopy. The airway was secured, and the lesion—a sessile mass occluding 70% of the lumen—was visualized. Mechanical resection was executed utilizing the rigid bronchoscope barrel for coring, supplemented by forceps extraction and snare resection of pedunculated elements. Thermal modalities were strictly avoided. Hemostasis was spontaneous or assisted by cold saline lavage.",
            3: "CPT: 31640 (Excision of Tumor).\nTechnique: Rigid Bronchoscopy with Mechanical Debulking.\nTools: Rigid scope (coring), Forceps, Snare.\nSite: Proximal Trachea.\nNarrative: The patient was anesthetized. Rigid scope inserted. Tumor mechanically cored and removed with forceps. Snare used for polypoid component. No laser or cryotherapy utilized. Pathologic specimen collected.",
            4: "Resident Note: Tracheal Debulking\nPatient: Robert Martinez, 55M\nStaff: Dr. Shah\n1. General Anesthesia induced.\n2. Rigid bronchoscope inserted.\n3. Proximal tracheal tumor identified (70% stenosis).\n4. Performed mechanical debulking using rigid coring technique and forceps.\n5. Snare used for one piece.\n6. No complications. Minimal bleeding.\nPlan: Extubate, PACU, Home.",
            5: "Procedure note for William Taylor he has that tracheal tumor causing noisy breathing we took him to the OR for rigid bronchoscopy did the mechanical debulking used the rigid scope to core it out and forceps to grab the pieces also used a snare for a hanging part no balloons or burning used just mechanical removal bleeding was minimal 15ml he did fine extubated sent to pacu then home later",
            6: "BRONCHOSCOPY PROCEDURE NOTE MECHANICAL DEBULKING OF TRACHEAL TUMOR Patient David Thomas 56-year-old male Date 2024-12-05 Location Capital Regional Hospital Indication Proximal tracheal tumor with noisy breathing and exertional dyspnea Procedure Rigid bronchoscopy with mechanical debulking excision of proximal tracheal mass CPT 31640 Anesthesia General anesthesia with rigid tracheoscope ASA class III Findings Sessile tumor on anterior proximal tracheal wall narrowing lumen to 70% Interventions Rigid coring and forceps debulking removed most of the lesion Snare resection used to excise a pedunculated portion No ablation or balloon used Hemostasis Minimal controlled with cold saline EBL 15 mL.",
            7: "[Indication]\nProximal tracheal tumor, stridor, exertional dyspnea.\n[Anesthesia]\nGeneral Anesthesia, Rigid Bronchoscopy.\n[Description]\nRigid scope inserted. 70% occlusion of proximal trachea noted. Mechanical debulking performed via rigid coring, forceps excision, and snare resection. No thermal ablation. Hemostasis secured with cold saline.\n[Plan]\nExtubate. Discharge home after recovery.",
            8: "Mr. Richard Hernandez underwent rigid bronchoscopy to treat a tumor in his windpipe. Once he was asleep, we inserted the rigid scope and saw the mass blocking about 70% of the airway. We used the sharp edge of the scope to core through the tumor and forceps to pull the pieces out. We also used a snare to cut off a hanging piece. We didn't use any heat or balloons. The bleeding was very light and stopped with some cold saltwater. He went home the same day.",
            9: "Indication: Proximal tracheal tumor with noisy respiration and exertional breathlessness.\nProcedure: Rigid bronchoscopy with physical reduction/extraction of proximal tracheal mass.\nInterventions: Rigid coring and forceps removal eliminated most of the lesion. Snare excision utilized to remove a pedunculated segment. No destruction or balloon employed.\nHemostasis: Minimal; managed with chilled saline.",
        },
        2: { # Jonas Meyer (RMS NSCLC, Rigid, Coring/Forceps)
            1: "Dx: RMS obstruction (NSCLC).\nProc: Rigid bronch, mech debulking.\nFindings: 85% occlusion RMS.\nActions: Rigid coring + forceps excision. No ablation.\nEBL: 50cc. Epi/Saline used.\nDisp: Admit Oncology.",
            2: "PROCEDURE: Therapeutic Rigid Bronchoscopy.\nINDICATION: Mr. Charles Moore presented with significant right mainstem bronchial obstruction secondary to non-small cell lung carcinoma.\nTECHNIQUE: Under general anesthesia, the rigid bronchoscope was introduced. The right mainstem bronchus was found to be 85% compromised by tumor burden. Mechanical recanalization was achieved via rigid coring and biopsy forceps excision. No thermal ablation or balloon dilation was required. Hemostasis was achieved with topical epinephrine and cold saline.",
            3: "Code Selection: 31640 (Bronchoscopy; with excision of tumor).\nMethod: Mechanical.\nTools: Rigid Bronchoscope (Coring), Forceps.\nAnatomy: Right Mainstem Bronchus.\nDescription: Mechanical debulking of malignant tumor causing central airway obstruction. Tumor cored and removed piecemeal. No destruction methods (laser/cryo) coded.",
            4: "Procedure: Rigid Bronch Debulking\nPatient: Joseph Jackson, 66M\nIndication: Ca Lung, RMS obstruction.\nSteps:\n1. GA / Rigid Scope.\n2. Visualized tumor in RMS (85% blocked).\n3. Used rigid scope to core the tumor.\n4. Used forceps to remove debris.\n5. No ablation.\n6. Hemostasis with epi.\nPlan: Admit to floor.",
            5: "Thomas White here for the debulking of the right mainstem tumor its nsclc blocking about 85 percent used the rigid scope under general anesthesia to core it out and forceps to pull the rest we didnt use any ablation or balloons just mechanical debulking bleeding was moderate about 50ml controlled with epi and saline patient extubated and going to oncology floor",
            6: "INTERVENTIONAL PULMONOLOGY OPERATIVE REPORT MECHANICAL DEBULKING Patient Christopher Harris 67-year-old male Date 2025-01-10 Hospital Pacific Coast Cancer Center Indication Malignant obstruction of right mainstem bronchus from non small cell lung cancer Procedure Rigid bronchoscopy with mechanical debulking of right mainstem tumor CPT 31640 Anesthesia General anesthesia rigid bronchoscope ASA class III Findings Tumor narrowing right mainstem lumen by 85% with retained secretions Interventions Rigid coring and forceps debulking used to mechanically debulk and excise the tumor No ablation or balloon dilation employed Hemostasis Moderate oozing controlled with cold saline and epinephrine EBL 50 mL.",
            7: "[Indication]\nMalignant obstruction, Right Mainstem Bronchus (NSCLC).\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n85% obstruction of RMS identified. Mechanical debulking performed using rigid coring and forceps excision. Airway patency restored. No thermal ablation used.\n[Plan]\nAdmit to oncology floor.",
            8: "Mr. Daniel Martin needed a procedure to open up his right main airway, which was blocked by lung cancer. We used a rigid bronchoscope under general anesthesia. We mechanically cored out the tumor using the scope itself and removed the pieces with large forceps. We didn't need to burn or freeze anything. There was some oozing, but we stopped it with medication and cold water. He is being admitted to the oncology floor for recovery.",
            9: "Indication: Malignant blockage of right mainstem bronchus from non–small cell lung cancer.\nProcedure: Rigid bronchoscopy with physical reduction of right mainstem tumor.\nInterventions: Rigid coring and forceps removal utilized to physically reduce and excise the tumor. No destruction or balloon expansion employed.\nHemostasis: Moderate oozing managed with chilled saline and epinephrine.",
        },
        3: { # Natalie Ortiz (Trach Granulation, Flex, Forceps/Snare)
            1: "Indication: Trach site obstruction (granulation/tumor).\nProc: Flex bronch via trach.\nAction: Mech debulking (forceps/snare). No ablation.\nFindings: 60% obstruction.\nEBL: 15cc.\nPlan: Floor, home vent settings.",
            2: "HISTORY: Mrs. Patricia Thompson, a 62-year-old female with a tracheostomy, presented with dyspnea due to granulation tissue and tumor recurrence at the stoma site.\nPROCEDURE: Flexible bronchoscopy was performed through the tracheostomy. Inspection revealed nodular tumor and granulation tissue encroaching on the tracheal lumen. Mechanical excision was performed utilizing forceps and snare resection techniques. Thermal ablation was withheld. The airway caliber was significantly improved post-debulking.",
            3: "Billing: 31640 (Excision of tumor/granulation).\nApproach: Via Tracheostomy.\nTechnique: Mechanical excision.\nTools: Forceps, Snare.\nLocation: Trachea (stoma site).\nDetails: 60% obstruction reduced mechanically. No laser/APC/Cryo used. Medical necessity: Symptomatic airway obstruction.",
            4: "Resident Note: Trach Debulking\nPatient: Linda Garcia, 62F\nIndication: Granulation/Tumor at trach site.\nSteps:\n1. Moderate sedation.\n2. Scope via trach.\n3. Saw tissue blocking 60%.\n4. Used forceps and snare to remove it.\n5. No burning/ablation.\n6. Minimal bleeding.\nPlan: Back to ward, keep on vent settings.",
            5: "barbara martinez needing the bronchoscopy through her trach she has granulation and tumor growing there blocking the airway we used the flexible scope with moderate sedation used forceps to grab the tissue and a snare to cut it out mechanical removal only no ablation used bleeding was mild stopped with saline shes going back to the floor on her vent settings",
            6: "BRONCHOSCOPY PROCEDURE NOTE MECHANICAL DEBULKING IN PATIENT WITH TRACHEOSTOMY Patient Elizabeth Robinson 63-year-old female Date 2025-01-28 Location Coastal Veterans Hospital Indication Granulation tissue and tumor regrowth around tracheostomy stoma extending into tracheal lumen with dyspnea Procedure Flexible bronchoscopy via tracheostomy with mechanical debulking of granulation tumor CPT 31640 Anesthesia Sedation Moderate sedation midazolam fentanyl and topical lidocaine via tracheostomy Findings Granulation tissue and nodular tumor at distal tracheostomy site protruding into tracheal lumen 60% obstruction Interventions Forceps debulking and snare resection were used to mechanically excise granulation and tumor tissue No ablation used.",
            7: "[Indication]\nTracheostomy stoma obstruction (Granulation/Tumor).\n[Anesthesia]\nModerate Sedation via Tracheostomy.\n[Description]\nFlexible bronchoscopy via trach. 60% obstruction noted. Mechanical debulking performed using forceps and snare resection. No thermal ablation. Hemostasis with cold saline.\n[Plan]\nReturn to ward. Home vent settings. F/u 6 weeks.",
            8: "Mrs. Jennifer Clark has a tracheostomy and developed tissue growth blocking her windpipe. We went in with a flexible scope through her trach tube. We found a mix of tumor and granulation tissue blocking about 60% of the airway. We used forceps and a snare to mechanically cut and pull the tissue out. We didn't use any heat treatment. There was very little bleeding. She went back to her room on her usual ventilator settings.",
            9: "Indication: Granulation tissue and tumor regrowth around tracheostomy stoma extending into tracheal lumen with breathlessness.\nProcedure: Flexible bronchoscopy via tracheostomy with physical reduction of granulation/tumor.\nInterventions: Forceps removal and snare cutting were utilized to physically excise granulation and tumor tissue. No destruction used.\nHemostasis: Mild; managed with chilled saline.",
        },
        4: { # Olivia Martin (LMS Mass, Rigid, Microdebrider/Coring)
            1: "Indication: LMS obstruction (90%).\nProc: Rigid bronch (31640).\nAction: Coring, forceps, microdebrider. No ablation.\nResult: Patent LMS.\nEBL: 55cc.\nPlan: Extubate, Step-down.",
            2: "OPERATIVE SUMMARY: Ms. Maria Rodriguez presented with near-complete obstruction of the left mainstem bronchus. Rigid bronchoscopy was undertaken. The bulky tumor was mechanically debulked utilizing the beveled tip of the rigid bronchoscope for coring, followed by forceps extraction. Final airway contouring was achieved with a microdebrider. No thermal energy was applied. Hemostasis was secured with epinephrine and saline lavage.",
            3: "CPT Code: 31640.\nProcedure: Bronchoscopy with excision of tumor.\nModality: Mechanical (Rigid coring, Forceps, Microdebrider).\nSite: Left Mainstem Bronchus.\nIndication: Malignant airway obstruction.\nNote: No thermal ablation codes applicable. Purely mechanical resection.",
            4: "Procedure: Rigid Bronch LMS\nPatient: Susan Lewis, 64F\nSteps:\n1. General Anesthesia.\n2. Rigid scope to LMS.\n3. 90% blockage found.\n4. Cored with scope, pulled with forceps.\n5. Used microdebrider to clean it up.\n6. No ablation.\n7. Bleeding controlled.\nPlan: Step-down unit.",
            5: "procedure note for margaret lee she has that left mainstem mass blocking almost everything 90 percent we did a rigid bronch under GA used the rigid scope to core through it and forceps to get the bulk then used the microdebrider to finish up mechanical removal only no burning or balloons bleeding was about 55ml controlled with meds shes going to step down",
            6: "INTERVENTIONAL PULMONOLOGY MECHANICAL DEBULKING OF LMS MASS Patient Dorothy Walker 65-year-old female Date 2025-02-12 Hospital Seaside Oncology Center Indication Left mainstem endobronchial mass with near complete obstruction and dyspnea at rest Procedure Rigid bronchoscopy with mechanical debulking of left mainstem tumor CPT 31640 Anesthesia General anesthesia rigid bronchoscope ASA class III Findings Bulky tumor at left mainstem origin narrowing lumen 90% Interventions Rigid coring and forceps debulking were used to mechanically remove tumor Microdebrider used for final debulking No ablation Hemostasis Moderate oozing controlled with cold saline and epinephrine.",
            7: "[Indication]\nLeft Mainstem Bronchus obstruction, dyspnea at rest.\n[Anesthesia]\nGeneral, Rigid Bronchoscope.\n[Description]\n90% obstruction of LMS. Mechanical debulking performed via rigid coring, forceps, and microdebrider. No thermal ablation. Hemostasis achieved.\n[Plan]\nExtubate. Admit to step-down.",
            8: "Ms. Lisa Hall had a large tumor blocking her left main airway almost completely. We performed a rigid bronchoscopy to clear it. We mechanically cored out the tumor and removed large pieces with forceps. We also used a microdebrider tool to smooth out the airway. We didn't use any lasers or heat. The bleeding was moderate but we stopped it with medicine. She is going to the step-down unit for monitoring.",
            9: "Indication: Left mainstem endobronchial mass with near-complete blockage and breathlessness at rest.\nProcedure: Rigid bronchoscopy with physical reduction of left mainstem tumor.\nInterventions: Rigid coring and forceps removal were utilized to physically extract tumor. Microdebrider utilized for final reduction. No destruction.\nHemostasis: Moderate oozing managed with chilled saline and epinephrine.",
        },
        5: { # Marcus Allen (RLL Lesion, Flex, Snare/Forceps)
            1: "Indication: RLL polypoid lesion.\nProc: Flex bronch, mech debulking.\nTools: Snare, Forceps.\nFindings: 70% obstruction RLL superior segment.\nNo ablation.\nEBL: 10ml.\nPlan: Home.",
            2: "PROCEDURE NOTE: Mr. Kenneth Young underwent therapeutic flexible bronchoscopy for a polypoid endobronchial lesion within the superior segment of the right lower lobe bronchus. Mechanical excision was performed utilizing a wire snare for en bloc resection, followed by forceps debulking of the base. Thermal ablation was not required. The airway patency was successfully restored.",
            3: "Code: 31640.\nTechnique: Mechanical Excision.\nInstrumentation: Snare, Biopsy Forceps.\nLocation: RLL (Superior Segment).\nNarrative: Endobronchial lesion mechanically resected to relieve obstruction. No thermal modalities used. Hemostasis with saline.",
            4: "Resident Note: RLL Debulking\nPatient: Steven Hernandez, 58M\nAttending: Dr. Nguyen\n1. Mod sedation/LMA.\n2. Scope to RLL superior segment.\n3. Found polypoid lesion.\n4. Snared it off.\n5. Used forceps for the rest.\n6. No heat/ablation.\nPlan: Discharge home.",
            5: "patient is edward king 58 male here for that rll lesion causing pneumonia we did a flex bronch with moderate sedation used a snare to cut the polyp and forceps to grab the rest mechanical removal only no burning or balloons minimal bleeding 10cc discharged home follow up with ct later",
            6: "BRONCHOSCOPY PROCEDURE NOTE MECHANICAL DEBULKING OF RLL BRONCHUS LESION Patient Brian Wright 59-year-old male Date 2025-02-27 Institution Highland Pulmonary Center Indication Right lower lobe endobronchial lesion with recurrent post obstructive pneumonia Procedure Flexible bronchoscopy with mechanical debulking excision of RLL bronchus lesion CPT 31640 Anesthesia Sedation Moderate sedation propofol fentanyl via LMA Findings Polypoid lesion at superior segment RLL bronchus with 70% obstruction Interventions Snare resection and forceps debulking used to mechanically remove the lesion No thermal ablation or balloon dilation Hemostasis Minimal controlled with cold saline.",
            7: "[Indication]\nRLL endobronchial lesion, recurrent pneumonia.\n[Anesthesia]\nModerate Sedation, LMA.\n[Description]\nFlexible bronchoscopy. 70% obstruction RLL superior segment. Mechanical debulking via snare resection and forceps. No thermal ablation. Hemostasis with cold saline.\n[Plan]\nDischarge home. F/u CT and bronch.",
            8: "Mr. Ronald Lopez came in for a lesion in his right lower lung that was causing pneumonia. We used a flexible scope and moderate sedation. We mechanically removed the growth using a snare loop and forceps. We didn't need to use any heat to burn it. There was barely any bleeding. He went home after we watched him for a bit.",
            9: "Indication: Right lower lobe endobronchial lesion with recurrent post-obstructive pneumonia.\nProcedure: Flexible bronchoscopy with physical reduction/extraction of RLL bronchus lesion.\nInterventions: Snare cutting and forceps removal utilized to physically withdraw the lesion. No thermal destruction or balloon expansion.\nHemostasis: Minimal; managed with chilled saline.",
        },
        6: { # Sofia Delgado (Carina/LMS, Rigid, Coring/Forceps)
            1: "Indication: Carina/LMS tumor.\nProc: Rigid bronch debulking.\nAction: Coring, forceps. No ablation.\nFindings: 80% obstruction.\nEBL: 40ml.\nPlan: Extubate, Step-down.",
            2: "OPERATIVE REPORT: Ms. Nancy Scott presented with a central airway obstruction involving the carina and left mainstem bronchus. Rigid bronchoscopy was performed. The tumor was mechanically debrided using the rigid coring technique and forceps excision to restore airway patency. No thermal ablation was utilized during this intervention. Hemostasis was adequate.",
            3: "CPT 31640: Bronchoscopy with excision of tumor.\nTechnique: Mechanical (Rigid coring, Forceps).\nLocation: Carina and Left Mainstem.\nNote: Documentation supports mechanical removal of obstructing tumor. No APC/Laser used.",
            4: "Procedure: Rigid Bronch\nPatient: Karen Green, 50F\nIndication: Carinal tumor.\nSteps:\n1. GA, rigid scope.\n2. Tumor at carina/LMS (80%).\n3. Cored it out.\n4. Forceps removal.\n5. No ablation.\n6. Epi for bleeding.\nPlan: Step-down unit.",
            5: "betty adams here for the carinal tumor rigid bronchoscopy under general anesthesia saw the tumor blocking the left side and carina about 80 percent used the rigid scope to core it and forceps to pull it out mechanical debulking only no heat used bleeding was 40ml controlled well shes going to step down",
            6: "INTERVENTIONAL PULMONOLOGY RIGID BRONCHOSCOPY WITH MECHANICAL DEBULKING Patient Helen Baker 51-year-old female Date 2025-03-14 Hospital Union Square Medical Center Indication Mixed carinal and left mainstem obstruction from endobronchial lung cancer Procedure Rigid bronchoscopy with mechanical debulking of carinal LMS tumor CPT 31640 Anesthesia General anesthesia rigid bronchoscope ASA class III Findings Tumor projecting from left side of carina into LMS with 80% obstruction Interventions Rigid coring and forceps debulking to mechanically debulk tumor at carina and LMS No thermal ablation Hemostasis Controlled with cold saline and epinephrine EBL 40 mL.",
            7: "[Indication]\nCarinal and Left Mainstem obstruction (Lung Cancer).\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n80% obstruction identified. Mechanical debulking performed using rigid coring and forceps. No thermal ablation. Hemostasis secured.\n[Plan]\nExtubate. Admit to step-down.",
            8: "Ms. Sandra Nelson had a tumor growing at the split of her windpipe going into the left lung. We performed a rigid bronchoscopy to clear it out. We used the metal scope to core through the tumor and forceps to grab the chunks. We did this mechanically without using any heat or lasers. We controlled the bleeding with medicine and she is recovering in the step-down unit.",
            9: "Indication: Mixed carinal and left mainstem blockage from endobronchial lung cancer.\nProcedure: Rigid bronchoscopy with physical reduction of carinal/LMS tumor.\nInterventions: Rigid coring and forceps removal to physically reduce tumor at carina and LMS. No thermal destruction.\nHemostasis: Managed with chilled saline and epinephrine.",
        },
        7: { # Henry Thompson (Tracheal Stenosis, Flex, Forceps/Snare)
            1: "Indication: Post-intubation stenosis.\nProc: Flex bronch debulking.\nFindings: Granulation ring distal trachea.\nAction: Forceps/Snare. No balloon/ablation.\nEBL: 5ml.\nPlan: D/C home.",
            2: "PROCEDURE NOTE: Mr. Donald Carter presented with post-intubation tracheal stenosis. Flexible bronchoscopy revealed a circumferential ring of granulation tissue in the distal trachea. Mechanical excision was performed utilizing biopsy forceps and snare resection to restore luminal patency. No balloon dilation or thermal ablation was employed.",
            3: "Code: 31640.\nDiagnosis: Tracheal Stenosis (Granulation).\nMethod: Mechanical Excision (Forceps, Snare).\nLocation: Distal Trachea.\nNote: Mechanical removal of granulation tissue. No dilation (31630) or ablation (31641) performed.",
            4: "Resident Note: Tracheal Debulking\nPatient: Timothy Mitchell, 72M\nIndication: Tracheal granulation.\nSteps:\n1. Mod sedation.\n2. Scope to distal trachea.\n3. Saw granulation ring.\n4. Removed with forceps and snare.\n5. No balloon used.\n6. Minimal bleeding.\nPlan: Home, f/u 2 months.",
            5: "george perez has that tracheal narrowing from his tube before we went in with the flex scope saw the granulation tissue blocking it used forceps and a snare to cut it out mechanical only no balloon or burning used bleeding was nothing really 5ml sent him home",
            6: "BRONCHOSCOPY PROCEDURE NOTE MECHANICAL DEBULKING Patient Kenneth Roberts 73-year-old male Date 2025-04-01 Facility Riverbend Community Hospital Indication Post intubation tracheal stenosis with progressive dyspnea Procedure Flexible bronchoscopy with mechanical debulking of granulation tissue CPT 31640 Anesthesia Sedation Moderate sedation with midazolam and fentanyl topical lidocaine Findings Short circumferential granulation ring in distal trachea causing 60 to 70% narrowing Interventions Forceps debulking and snare resection used to mechanically excise granulation tissue No balloon or ablation Hemostasis Minimal controlled with cold saline.",
            7: "[Indication]\nPost-intubation tracheal stenosis (Granulation).\n[Anesthesia]\nModerate Sedation.\n[Description]\nGranulation ring in distal trachea. Mechanical debulking performed with forceps and snare. No balloon dilation or ablation used.\n[Plan]\nDischarge home. F/u 2-3 months.",
            8: "Mr. Edward Turner had scar tissue growing in his windpipe from a previous breathing tube. We used a flexible scope to go down and remove it. We used small forceps and a snare to mechanically cut away the tissue. We didn't use a balloon or any heat. The airway opened up nicely, and there was hardly any bleeding. He went home the same day.",
            9: "Indication: Post-intubation tracheal narrowing with progressive breathlessness.\nProcedure: Flexible bronchoscopy with physical reduction of granulation tissue.\nInterventions: Forceps removal and snare cutting utilized to physically excise granulation tissue. No balloon or destruction.\nHemostasis: Minimal; managed with chilled saline.",
        },
        8: { # David Price (LMS Tumor, Rigid, Microdebrider)
            1: "Indication: LMS tumor, pneumonia.\nProc: Rigid bronch (31640).\nAction: Coring, forceps, microdebrider. No heat.\nFindings: 85% obstruction.\nEBL: 60ml.\nPlan: Admit Oncology.",
            2: "OPERATIVE SUMMARY: Mr. Brian Campbell underwent rigid bronchoscopy for a symptomatic left mainstem neoplasm. The lesion was friable and occlusive. Mechanical debulking was executed via rigid coring, forceps resection, and microdebrider application. Thermal ablation modalities were not utilized. Hemostasis was achieved pharmacologically and with lavage.",
            3: "CPT: 31640.\nMethod: Mechanical (Rigid, Forceps, Microdebrider).\nSite: Left Mainstem.\nJustification: Excision of tumor for airway clearance. No thermal energy used.",
            4: "Procedure: Rigid Bronch\nPatient: Anthony Phillips, 63M\nIndication: LMS Tumor.\nSteps:\n1. GA.\n2. Rigid scope inserted.\n3. LMS mass debulked with coring/forceps.\n4. Microdebrider used.\n5. No ablation.\n6. Epi used for bleeding.\nPlan: Admit.",
            5: "jason parker has the left mainstem tumor causing pneumonia we did the rigid bronchoscopy under GA cored it out with the scope used forceps and the microdebrider too mechanical only no heat used bleeding was 60ml controlled with epi admitted to the ward",
            6: "INTERVENTIONAL PULMONOLOGY RIGID BRONCHOSCOPY WITH MECHANICAL DEBULKING Patient Kevin Evans 64-year-old male Date 2025-04-16 Hospital Meridian Cancer Institute Indication Left mainstem endobronchial tumor with recurrent post obstructive pneumonia and weight loss Procedure Rigid bronchoscopy with mechanical debulking excision of left mainstem tumor CPT 31640 Anesthesia General anesthesia rigid bronchoscope ASA class III Findings Friable LMS mass causing 80 to 85% obstruction Interventions Rigid coring forceps debulking and microdebrider used for mechanical debulking and excision No thermal methods Hemostasis Moderate oozing controlled with cold saline and epinephrine EBL 60 mL.",
            7: "[Indication]\nLeft Mainstem Bronchus tumor, recurrent pneumonia.\n[Anesthesia]\nGeneral, Rigid Bronchoscope.\n[Description]\nFriable mass in LMS (85% obstruction). Mechanical debulking performed via rigid coring, forceps, and microdebrider. No thermal ablation. Hemostasis secured.\n[Plan]\nAdmit to oncology ward.",
            8: "Mr. Jeffrey Edwards had a tumor blocking his left lung airway. We did a procedure with a rigid tube while he was asleep. We mechanically removed the tumor by coring it, pulling pieces out with forceps, and using a microdebrider tool. We avoided using any heat treatments. There was some bleeding which we stopped with medication. He is staying in the hospital for recovery.",
            9: "Indication: Left mainstem endobronchial tumor with recurrent post-obstructive pneumonia and weight loss.\nProcedure: Rigid bronchoscopy with physical reduction/extraction of left mainstem tumor.\nInterventions: Rigid coring, forceps removal, and microdebrider utilized for physical reduction and excision. No thermal methods.\nHemostasis: Moderate oozing managed with chilled saline and epinephrine.",
        },
        9: { # Chloe Bennett (Tracheal Tumor, Rigid, Coring/Snare)
            1: "Indication: Tracheal tumor, stridor.\nProc: Rigid bronch (31640).\nAction: Coring, forceps, snare. No ablation.\nFindings: 75% narrowing.\nEBL: 20ml.\nPlan: Step-down.",
            2: "PROCEDURE NOTE: Ms. Lisa Collins presented with critical tracheal stenosis secondary to malignancy. Rigid bronchoscopy was performed. The mid-tracheal tumor was mechanically resected using the rigid coring technique, forceps extraction, and snare resection for pedunculated components. Thermal ablation was not required. The airway was successfully recanalized.",
            3: "Code: 31640.\nService: Bronchoscopy with tumor excision.\nMethod: Mechanical (Rigid coring, Snare, Forceps).\nSite: Mid-trachea.\nNote: Mechanical debulking only. No thermal ablation performed.",
            4: "Procedure: Rigid Tracheal Debulking\nPatient: Betty Stewart, 48F\nIndication: Stridor.\nSteps:\n1. GA, rigid scope.\n2. Mid-trachea tumor found.\n3. Cored and snared the tumor.\n4. Forceps used for debris.\n5. No ablation.\n6. Minimal bleeding.\nPlan: Step-down unit.",
            5: "sandra morris here for the tracheal tumor she has stridor we did a rigid bronchoscopy under GA cored out the tumor used forceps and a snare too mechanical removal only no burning or balloons bleeding was minimal 20ml shes going to step down for the night",
            6: "BRONCHOSCOPY PROCEDURE NOTE MECHANICAL DEBULKING IN PATIENT WITH MALIGNANT TRACHEAL TUMOR Patient Ashley Sanchez 49-year-old female Date 2025-05-01 Facility Horizon Academic Medical Center Indication Proximal mid tracheal tumor with progressive stridor and exertional dyspnea Procedure Rigid bronchoscopy with mechanical debulking excision of tracheal tumor CPT 31640 Anesthesia General anesthesia rigid bronchoscope ASA class III Findings Tumor involving anterior and lateral walls of mid trachea causing 75% narrowing Interventions Rigid coring and forceps debulking used to mechanically debulk and excise tumor tissue Snare resection of a pedunculated component No thermal ablation Hemostasis Mild controlled with cold saline EBL 20 mL.",
            7: "[Indication]\nMid-tracheal tumor, stridor.\n[Anesthesia]\nGeneral, Rigid Bronchoscopy.\n[Description]\n75% tracheal narrowing. Mechanical debulking performed using rigid coring, forceps, and snare resection. No thermal ablation. Hemostasis secured.\n[Plan]\nExtubate. Admit to step-down.",
            8: "Ms. Kimberly Rogers had a tumor in her windpipe causing difficulty breathing. We used a rigid scope to remove it while she was under anesthesia. We cut the tumor out mechanically using the scope edge, forceps, and a snare. We didn't use any heat. The bleeding was minor. She is breathing much better and will stay overnight in the step-down unit.",
            9: "Indication: Proximal/mid tracheal tumor with progressive stridor and exertional breathlessness.\nProcedure: Rigid bronchoscopy with physical reduction/extraction of tracheal tumor.\nInterventions: Rigid coring and forceps removal utilized to physically reduce and excise tumor tissue. Snare excision of a pedunculated component. No thermal destruction.\nHemostasis: Mild; managed with chilled saline.",
        }
    }
    return variations

def get_base_data_mocks():
    # Names must match the text variations in get_variations
    return [
        {"idx": 0, "orig_name": "Jasmine Young", "orig_age": 39, "names": ["N/A", "Sarah Miller", "N/A", "Emily Davis", "Jessica Williams", "Amanda Brown", "N/A", "Ashley Wilson", "N/A"]},
        {"idx": 1, "orig_name": "Kevin Brooks", "orig_age": 55, "names": ["N/A", "James Anderson", "N/A", "Robert Martinez", "William Taylor", "David Thomas", "N/A", "Richard Hernandez", "N/A"]},
        {"idx": 2, "orig_name": "Jonas Meyer", "orig_age": 66, "names": ["N/A", "Charles Moore", "N/A", "Joseph Jackson", "Thomas White", "Christopher Harris", "N/A", "Daniel Martin", "N/A"]},
        {"idx": 3, "orig_name": "Natalie Ortiz", "orig_age": 62, "names": ["N/A", "Patricia Thompson", "N/A", "Linda Garcia", "Barbara Martinez", "Elizabeth Robinson", "N/A", "Jennifer Clark", "N/A"]},
        {"idx": 4, "orig_name": "Olivia Martin", "orig_age": 64, "names": ["N/A", "Maria Rodriguez", "N/A", "Susan Lewis", "Margaret Lee", "Dorothy Walker", "N/A", "Lisa Hall", "N/A"]},
        {"idx": 5, "orig_name": "Marcus Allen", "orig_age": 58, "names": ["N/A", "Kenneth Young", "N/A", "Steven Hernandez", "Edward King", "Brian Wright", "N/A", "Ronald Lopez", "N/A"]},
        {"idx": 6, "orig_name": "Sofia Delgado", "orig_age": 50, "names": ["N/A", "Nancy Scott", "N/A", "Karen Green", "Betty Adams", "Helen Baker", "N/A", "Sandra Nelson", "N/A"]},
        {"idx": 7, "orig_name": "Henry Thompson", "orig_age": 72, "names": ["N/A", "Donald Carter", "N/A", "Timothy Mitchell", "George Perez", "Kenneth Roberts", "N/A", "Edward Turner", "N/A"]},
        {"idx": 8, "orig_name": "David Price", "orig_age": 63, "names": ["N/A", "Brian Campbell", "N/A", "Anthony Phillips", "Jason Parker", "Kevin Evans", "N/A", "Jeffrey Edwards", "N/A"]},
        {"idx": 9, "orig_name": "Chloe Bennett", "orig_age": 48, "names": ["N/A", "Lisa Collins", "N/A", "Betty Stewart", "Sandra Morris", "Ashley Sanchez", "N/A", "Kimberly Rogers", "N/A"]},
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
            
            # Get the specific name assigned (if any)
            new_name = record['names'][style_num - 1]
            if new_name == "N/A":
                # Fallback if no specific name was embedded in the text for styles 1, 3, 7, 9
                # We reuse the original name or generate a simple placeholder if needed
                # For this exercise, we keep the metadata updated even if text is generic
                new_name = f"Patient_Var_{idx}_{style_num}" 

            # Update note_text with the variation
            note_entry["note_text"] = variations_text[idx][style_num]
            
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
    output_filename = output_dir / "synthetic_blvr_notes_part_084.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()