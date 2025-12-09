import pandas as pd
import re

# 1. Load Data (Ensure this file is in your working directory)
filename = "Synthetic notes clean.xlsx"
df = pd.read_excel(filename)

# 2. Define Definitions
code_info = {
    '31600': {'desc': 'Tracheostomy', 'keywords': ['tracheostomy', 'trach', 'percutaneous']},
    '31623': {'desc': 'Bronchoscopy w/ Brushing', 'keywords': ['brush', 'brushing']},
    '31624': {'desc': 'Bronchoscopy w/ BAL', 'keywords': ['bal', 'lavage', 'wash', 'bronchoalveolar']},
    '31625': {'desc': 'Bronchoscopy w/ Bronchial Biopsy', 'keywords': ['biopsy', 'forceps', 'endobronchial']},
    '31626': {'desc': 'Bronchoscopy w/ Fiducial Placement', 'keywords': ['fiducial', 'marker', 'seed']},
    '31627': {'desc': 'Navigational Bronchoscopy', 'keywords': ['navigation', 'robotic', 'ion', 'monarch', 'enb', 'electromagnetic', 'veran']},
    '31628': {'desc': 'Transbronchial Lung Biopsy', 'keywords': ['transbronchial', 'tblb', 'parenchyma', 'nodule biopsy']},
    '31629': {'desc': 'Transbronchial Needle Aspiration', 'keywords': ['tbna', 'needle', 'aspiration']},
    '31630': {'desc': 'Bronchoscopy w/ Dilation', 'keywords': ['dilation', 'balloon dilation', 'stricture']},
    '31631': {'desc': 'Bronchoscopy w/ Stent Placement', 'keywords': ['stent', 'placement']},
    '31632': {'desc': 'Bronchoscopy w/ Biopsy (Addl)', 'keywords': ['biopsy', 'additional lobe']},
    '31634': {'desc': 'Bronchoscopy w/ Balloon Occlusion', 'keywords': ['balloon occlusion', 'chartis', 'sizing']},
    '31635': {'desc': 'Bronchoscopy w/ Foreign Body Removal', 'keywords': ['foreign body', 'removal', 'retrieve', 'basket', 'snare']},
    '31636': {'desc': 'Bronchoscopy w/ Stent (Initial)', 'keywords': ['stent']},
    '31637': {'desc': 'Bronchoscopy w/ Stent (Addl)', 'keywords': ['stent', 'additional']},
    '31640': {'desc': 'Bronchoscopy w/ Tumor Excision', 'keywords': ['excision', 'resection', 'debulking', 'snare']},
    '31641': {'desc': 'Bronchoscopy w/ Tumor Destruction', 'keywords': ['destruction', 'ablation', 'rfa', 'cryo', 'laser', 'apc', 'electrocautery']},
    '31645': {'desc': 'Bronchoscopy w/ Therapeutic Aspiration', 'keywords': ['aspiration', 'mucus', 'secretions', 'toilet', 'plug']},
    '31647': {'desc': 'Bronchial Valve Insertion (Initial)', 'keywords': ['valve', 'zephyr', 'spiration', 'placement', 'insertion']},
    '31648': {'desc': 'Bronchial Valve Removal (Initial)', 'keywords': ['valve', 'removal', 'retrieve']},
    '31652': {'desc': 'EBUS (1-2 Stations)', 'keywords': ['ebus', 'ultrasound', 'node', 'station']},
    '31653': {'desc': 'EBUS (3+ Stations)', 'keywords': ['ebus', 'ultrasound', 'node', 'station']},
    '31654': {'desc': 'Radial EBUS', 'keywords': ['radial', 'rebus', 'peripheral', 'probe']},
    '32550': {'desc': 'Tunneled Pleural Catheter', 'keywords': ['pleurx', 'tunneled', 'indwelling', 'catheter']},
    '32555': {'desc': 'Thoracentesis', 'keywords': ['thoracentesis', 'tap']},
    '32560': {'desc': 'Pleurodesis (Chemical)', 'keywords': ['pleurodesis', 'talc', 'doxycycline', 'agent']},
    '32601': {'desc': 'Diagnostic Thoracoscopy', 'keywords': ['thoracoscopy', 'vats', 'inspection']},
    '32609': {'desc': 'Thoracoscopy w/ Pleural Biopsy', 'keywords': ['biopsy', 'pleura', 'parietal']},
    '32650': {'desc': 'Thoracoscopy w/ Pleurodesis', 'keywords': ['pleurodesis', 'talc', 'poudrage']},
    '32997': {'desc': 'Total Lung Lavage', 'keywords': ['lavage', 'whole lung', 'pap', 'proteinosis']}
}

# 3. Define Logic
def clean_and_split(code_str):
    code_str = str(code_str).replace(',', '').replace(' ', '')
    return [code_str[i:i+5] for i in range(0, len(code_str), 5)]

def verify_and_rationale_v2(row):
    text = row['note_text'].lower()
    codes = clean_and_split(row['verified_cpt_codes'])
    rationales = []
    
    # Regex to find "Station 4R", "Station 7", etc. to count unique stations
    station_matches = re.findall(r'station\s+\w+', text)
    unique_stations = len(set(station_matches))
    
    for code in codes:
        if code in code_info:
            info = code_info[code]
            found_kw = [kw for kw in info['keywords'] if kw in text]
            
            # Special logic for EBUS distinction
            if code == '31653':
                if unique_stations >= 3:
                    found_kw.append(f"{unique_stations} stations identified")
                elif 'station' in text:
                     found_kw.append("stations mentioned (count unclear)")
            elif code == '31652':
                 if unique_stations > 0:
                    found_kw.append(f"{unique_stations} stations identified")
            
            if found_kw:
                rationale = f"Code {code} ({info['desc']}) is supported by keywords: {', '.join(set(found_kw))}."
            else:
                rationale = f"Code {code} ({info['desc']}) - No direct keywords found, check context."
        else:
            rationale = f"Code {code} not in dictionary."
        rationales.append(rationale)
        
    return " ".join(rationales)

# 4. Apply & Save
df['Rationale'] = df.apply(verify_and_rationale_v2, axis=1)
df.to_excel('Synthetic notes clean.xlsx', index=False)
print("File saved successfully.")