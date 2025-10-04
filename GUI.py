# ======================================================================================
__author__ = "Alexandre Coumes"
# ======================================================================================
from ezTK import *
from EEG import *
import numpy as np
# ======================================================================================
class EEG_GUI(Win):
    def __init__(self, temps, alpha_data, picks, mode='frequence'):
        """
        :param: temps(ndarray): vecteur de temps
        alpha_data: tableau 2D
        picks: liste des électrodes utilisées
        mode: 'frequence' ou 'puissance'
        """
        super().__init__(title="Neurofeedback", bg='white', font="Times 16", flow='E', grow=False)
        print("📌 Initialisation EEG_GUI en mode:", mode)

        self.t = temps
        self.alpha_data = alpha_data
        self.picks = picks
        self.mode = mode
        self.index = 0
        self.max_power = 1
        self.bricks = []

        # Création des carrés avec leurs noms pour chaque électrodes
        for pick in picks:
            frame = Frame(self, flow='S')
            brick = Brick(frame, width=400, height=400, bg='black')
            Label(frame, text=pick, bg='white')
            self.bricks.append(brick)

        # Légende visuelle de l’échelle de rouge (à droite de l'interface)
        legend_frame = Frame(self, flow='S', bg='white')
        Label(legend_frame, text="Echelle d'activité", bg='white', font='Times 14 bold')

        Brick(legend_frame, width=100, height=40, bg='#200000')
        Label(legend_frame, text="Faible activité", bg='white')

        Brick(legend_frame, width=100, height=40, bg='#800000')
        Label(legend_frame, text="Activité moyenne", bg='white')

        Brick(legend_frame, width=100, height=40, bg='#ff0000')
        Label(legend_frame, text="Activité maximale", bg='white')

        print("✅ EEG_GUI prêt, démarrage animation")

        # Choix du mode
        if mode == 'frequence':
            self.after(1000, self.step_frequence)
        elif mode == 'puissance':
            self.after(1000, self.step_puissance)

    def step_puissance(self):
        if self.index < len(self.t):
            for i in range(len(self.picks)):
                power = self.alpha_data[i, self.index]
                if np.isnan(power): continue
                # Échelle dynamique : normaliser entre 0 et 1 par rapport au max global
                norm_power = min(max(power / self.max_power, 0), 1)
                red = int(255 * norm_power)
                color = f'#{red:02x}0000' # On ne change que le rouge 0000 sont pour green et blue
                self.bricks[i]['bg'] = color
            self.index += 1
            self.after(1000, self.step_puissance)

    def step_frequence(self):
        if self.index < len(self.t):
            for i in range(len(self.picks)):
                freq = self.alpha_data[i, self.index]
                if np.isnan(freq): continue
                intensity = max(0, min((freq - 8) / 4, 1))
                red = int(255 * intensity)
                color = f'#{red:02x}0000'
                self.bricks[i]['bg'] = color
            self.index += 1
            self.after(1000, self.step_frequence)
    def set_max_power(self, max_power):
        self.max_power = max_power
# ======================================================================================
if __name__ == "__main__":
    mode = 'puissance'

    picks = ['P3', 'Pz', 'P4']

    if mode == 'frequence':
        fichier = "B63_OE_baseline.gdf"
        data, sfreq = charger_filtrer_alpha(fichier, picks=picks, graph=False)
        t, freq_dom = calcul_frequence_dominante(data, sfreq)
        app = EEG_GUI(t, freq_dom, picks, mode='frequence')
        app.loop()

    elif mode == 'puissance':
        fichier_fermes = "B63_CE_baseline.gdf"
        fichier_ouverts = "B63_OE_baseline.gdf"

        # 1. Estimation de l'IAF avec yeux fermés
        data_fermes, sfreq = charger_filtrer_alpha(fichier_fermes, picks=picks, graph=False)
        iaf = estimer_IAF(data_fermes, sfreq)

        # 2. Données yeux ouverts pour analyse
        data_ouverts, _ = charger_filtrer_alpha(fichier_ouverts, picks=picks, graph=False)
        t_puiss, puissances = calcul_puissance_alpha_superieur(data_ouverts, sfreq, iaf, clean=True)

        # 3. Interface graphique avec normalisation réaliste
        app = EEG_GUI(t_puiss, puissances, picks, mode='puissance')
        app.set_max_power(np.nanpercentile(puissances, 95))
        app.loop()