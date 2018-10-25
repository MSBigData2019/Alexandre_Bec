'''
Extraire le dosage
La forme galenique
Le volume (nb de gelules)
Calculer l'equivalent traitement
'''

import requests
import json
import pandas as pd
import re

link = "https://www.open-medicaments.fr/api/v1/medicaments?query=paracetamol&limit=100"

result = requests.get(link)
result_json = json.loads(result.content)
list_ids = []

for i in range(0,len(result_json)):
    result = result_json[i]
    list_ids.append(result['codeCIS'])

    # UTILISER PANDAS READ JSON

medic_df = pd.DataFrame({"id":list_ids})

for id in medic_df["id"]:
    link = "https://www.open-medicaments.fr/api/v1/medicaments/"+str(id)
    result = requests.get(link)
    result_json = json.loads(result.content)
    codeCIS = result_json['codeCIS']

    forme = result_json['formePharmaceutique']
    denomination = result_json.get('denomination')

    # Une seule ligne
    libelle = result_json['presentations'][0]['libelle']
    print(codeCIS, forme, libelle, denomination)
    #formePharma = result_json['formePharmaeutique']

'''
# Traitement denomination
string = 'PARACETAMOL ZYDUS 500 mg, gélule'
reg = r',(.*)'
re.findall(reg, string)


link2 = "https://www.open-medicaments.fr/api/v1/medicaments/62772966"
req = json.loads(requests.get(link2).content)
df = pd.DataFrame(req)
denomination = df['denomination']
denomination.str.extract(reg)


reg = r'([\D]*)(\d+)(.*),(.*)'
ds['mul']=1000
ds['mul'] = ds['mul'].where(ds[unité].str.strip()=='g',1)
ds['dosage'] = ds[1].fillna(0).astype(int)*ds['mul']
'''
