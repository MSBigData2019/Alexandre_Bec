import pandas as pd
import numpy as np

# Répartition des médecins par spécialité et par département
skip = np.arange(1,17)
densite_medecin = pd.read_excel('data/rpps-medecins18-tab7.xlsx'
                                ,encoding = "utf-8"
                                ,skiprows = skip)

densite_medecin = densite_medecin.rename(columns={'ZONE INSCRIPT': 'Departement'})
densite_medecin['Departement'] = densite_medecin['Departement'].str[:2]
densite_medecin = densite_medecin.set_index('Departement')

# Répartition de la population
colonnes_population = ['Départements'
                    ,'Total']

df_population_xl = pd.read_excel('data/estim-pop-dep-975-2018.xls'
                    , encoding = "utf-8"
                    , sheetname="2018")

df_population = df_population_xl[colonnes_population]
df_population = df_population.groupby(['Départements']).sum()