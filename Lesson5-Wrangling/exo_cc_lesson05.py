'''
Extraire le dosage
La forme galenique
Le volume (nb de gelules)
Calculer l'equivalent traitement
'''


import pandas as pd
import requests
import re


url = "https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=paracetamol"
jsonData = requests.get(url).json()

#ICS = [f'https://www.open-medicaments.fr/api/v1/medicaments/{elm["codeCIS"]}' for elm in jsonData]
# Ne fonctionne pas dans pycharm ?

# Version boucle FOR
ICS = []
for i in range(0,len(jsonData)):
    toAppend = 'https://www.open-medicaments.fr/api/v1/medicaments/'+jsonData[i]['codeCIS']
    ICS.append(toAppend)

print("Liste des liens API :")
print(ICS)

#s = [requests.get(url).json() for url in ICS]

fiches_completes = []
for url in ICS:
    fiches_completes.append(requests.get(url).json())

print("Request pour chaque JSON complet :")
print(fiches_completes)

reg1 = r'(\d+)'
libelles = [medoc["presentations"][0]["libelle"] for medoc in fiches_completes]
gelules = pd.DataFrame({"gelules":[re.findall(reg1,lib)[-1] for lib in libelles]})
print(gelules.head())

df = pd.DataFrame(jsonData)



# On travaille uniquement sur la colonne Denomination
# Nouveau DF à partir des elements de la regex
reg = r'([\D]*)(\d+)(.*),(.*)'
serie = df["denomination"]
ds = serie.str.extract(reg)

# Colonnes de multiplicateur pour g/mg et dosage
ds["mul"] = 1000
ds["mul"] = ds["mul"].where(ds[2].str.strip()=="g",1)

ds["dosage"] = ds[1].fillna(0).astype(int)*ds["mul"]

ds["nb_gelules"] = gelules

print(ds.head())