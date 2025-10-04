# ======================================================================================
__author__ = "Alexandre Coumes"
# ======================================================================================
from ezTK import *
from EEG import *
import numpy as np
# ======================================================================================
class EEG_GUI(Win):
    def __init__(self, temps, alpha_data, picks):
        super().__init__(title="Neurofeedback", bg='white', font="Times 16", flow='E', grow=False)
        print("📌 Initialisation EEG_GUI")

        self.t = temps
        self.alpha_data = alpha_data
        self.picks = picks
        self.index = 0
        self.bricks = []

        for i, pick in enumerate(picks):
            frame = Frame(self, flow='S')
            brick = Brick(frame, width=400, height=400, bg='black')
            label = Label(frame, text=pick, bg='white')
            self.bricks.append(brick)

        print("✅ EEG_GUI prêt, démarrage animation")
        self.after(200, self.step)

    def step(self):
        if self.index < len(self.t):
            for i in range(len(self.picks)):
                power = self.alpha_data[i, self.index]
                if np.isnan(power): continue
                # Échelle dynamique : normaliser entre 0 et 1 par rapport au max global
                norm_power = min(max(power / self.max_power, 0), 1)
                red = int(255 * norm_power)
                color = f'#{red:02x}0000'
                self.bricks[i]['bg'] = color
            self.index += 1
            self.after(1000, self.step)

    def set_max_power(self, max_power):
        self.max_power = max_power


# ======================================================================================
if __name__ == '__main__':
    fichier = "B63_CE_baseline.gdf"
    fifi = "B63_OE_baseline.gdf"
    picks = ['P3', 'Pz', 'P4']

    # Étapes classiques
    data, sfreq = charger_filtrer_alpha(fifi, picks=picks, graph=False)
    d2, s2 = charger_filtrer_alpha(fichier, picks=picks, graph=False)
    iaf = estimer_IAF(d2, s2)
    t_puiss, puissances = calcul_puissance_alpha_superieur(data, sfreq, iaf, clean=True)

    # Interface graphique
    app = EEG_GUI(t_puiss, puissances, picks)
    app.set_max_power(np.nanpercentile(puissances, 95))
    app.loop()
