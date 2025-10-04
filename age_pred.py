# ======================================================================================
__author__ = "Alexandre Coumes"
# ======================================================================================
import matplotlib.pyplot as plt
import pandas as pd
# ======================================================================================
# Nettoyage des données
df = pd.read_excel("a-demo-pop-proj-age.xlsx", engine="openpyxl", skiprows=3)
df = df.head(5)

# Récupération des pourcentage de plus de 60 ans.
annee = df["Année"]
age_60_64 = df["60-64 ans"]
age_65_74 = df["65-74 ans"]
age_75_plus = df["75 ans\nou plus"]
age_60_plus = age_60_64 + age_65_74 + age_75_plus
age_64_plus = age_65_74 + age_75_plus

# Affichage Graphique
plt.figure(figsize=(8, 5))
plt.plot(annee, age_60_plus, marker='.', label='60 ans et plus')
plt.plot(annee, age_64_plus, marker='.', label='64 ans et plus')
plt.title("Évolution du pourcentage de personnes de 60 ans et plus")
plt.xlabel("Année")
plt.ylabel("Pourcentage dans la population française (%)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
