# ======================================================================================
__author__ = "Alexandre Coumes"
# ======================================================================================
import mne
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
# ======================================================================================
def charger_filtrer_alpha(fichier_gdf, l_freq=8, h_freq=12, picks=['P3', 'Pz', 'P4'], graph=True):
    """
    Charge un fichier GDF, filtre passe bande,
    et retourne les signaux EEG filtrés (data) et la fréquence d'échantillonnage (sfreq)

    :param : fichier_gdf (str) : du fichier à charger
    l_freq (float): fréquence basse du passa bande
    h_frq (float): fréquence haute du passe bande
    picks(list) : Liste des électrodes à extraire
    graph(bool) : Si graph alors affichage graphique
    """
    raw = mne.io.read_raw_gdf(fichier_gdf, preload=True) # Charge et lis le ficher .gdf
    raw_alpha = raw.copy().filter(l_freq=l_freq, h_freq=h_freq, picks=picks) # Applique le filtre passe bande (8-12)
    data, times = raw_alpha[picks, :] # Récupère les données des électrodes choisis
    sfreq = int(raw.info['sfreq']) # Fréquence d'échantillonnage
    # Trace les graphiques avec la bibliothèque MNE si graph == True
    if graph:
        raw.plot(n_channels=3, duration=10, scalings='auto', title='Signal EEG brut')
        raw_alpha.plot(n_channels=3, duration=10, scalings='auto', title='Bande alpha (8–12 Hz)', picks=picks)
    return data, sfreq

# ======================================================================================
def calcul_frequence_dominante(data, sfreq, fmin=8, fmax=12):
    """
    Calcule la fréquence dominante dans la bande alpha (8–12 Hz) chaque seconde.
    Retourne une liste de listes contenant les fréquences dominantes

    :param: data(ndarray) : Données EEG filtrées
    sfreq (int) : Fréquence d'échantillonnage
    fmin (float) : Borne inférieur
    fmax (flaot) : Borne supérieur
    """
    n_canaux, n_samples = data.shape # Nombre de canaux
    secondes = n_samples // sfreq # Nombre de secondes
    freq_dom = [] # Stockage des freq dominantes

    # Boucel pour chaque électrodes
    for ch in range(n_canaux):
        freqs_ch = []
        # Boucle pour chaque seconde
        for s in range(secondes):
            segment = data[ch, s * sfreq : (s + 1) * sfreq] # Extrait un segment d'une seconde
            fft = np.abs(np.fft.rfft(segment)) # FFT et on retire partie complexe
            freqs = np.fft.rfftfreq(len(segment), d=1/sfreq) # d = pas temporel / Crée un axe des fréquences en Hz
            mask = (freqs >= fmin) & (freqs <= fmax) # masque pour nos ondes alphas
            if np.any(mask):
                dom_freq = freqs[mask][np.argmax(fft[mask])] # entier / calcul la fréquence dominante dans alpha
            else:
                dom_freq = np.nan
            freqs_ch.append(dom_freq) # Ajoute de la fréquence dominante dans cette seconde
        freq_dom.append(freqs_ch) # Ajout d'une électrodes traités

    return np.arange(secondes), np.array(freq_dom)
# ======================================================================================
def estimer_IAF(data, sfreq, fmin=8, fmax=12):
    """
    Estime la fréquence alpha individuelle (IAF) sur un segment EEG

    :param: data(ndarray) : Données EEG filtrées
    sfreq (int) : Fréquence d'échantillonnage
    fmin (float) : Borne inférieur
    fmax (flaot) : Borne supérieur
    """
    iafs = [] # Stock des IAF
    # Boucle pour chaque électrodes
    for ch_data in data:
        freqs, psd = welch(ch_data, sfreq, nperseg=sfreq*2) # On applique la méthode de welch
        mask = (freqs >= fmin) & (freqs <= fmax) # Masque onde alpha
        iaf = freqs[mask][np.argmax(psd[mask])] # Fréquence avec la puissance maximale
        iafs.append(iaf)
    return np.mean(iafs) # Moyenne des iaf de mes électrodes
# ======================================================================================
def calcul_puissance_alpha_superieur(data, sfreq, iaf, clean=True):
    """
    Calcule la puissance moyenne dans la bande alpha supérieure (IAF à IAF+2 Hz) par seconde

    :param: data(ndarray) : Données EEG filtrées
    sfreq (int) : Fréquence d'échantillonnage
    iaf (flaot) : Fréquence alpha individuelle
    clean : (bool) Si clean enlève la dernière valeur aberrante
    """
    n_canaux, n_samples = data.shape
    secondes = n_samples // sfreq
    puissances = []

    # On enlève la dernière valeur aberrante
    if clean:
        secondes -= 1

    for ch in range(n_canaux):
        puiss_ch = []
        for s in range(secondes):
            segment = data[ch, s * sfreq : (s + 1) * sfreq] # Découpe mon segment
            freqs, psd = welch(segment, sfreq, nperseg=sfreq) # DFT appliqué sur toute la seconde / pas de découpage supplémentaire
            mask = (freqs >= iaf) & (freqs <= iaf + 2) # Masque individuelle
            puissance = np.mean(psd[mask]) if np.any(mask) else np.nan # Moyenne de la puissance dans cette bande
            puiss_ch.append(puissance)
        puissances.append(puiss_ch)

    t = np.arange(secondes)
    puissances = np.array(puissances)

    return t, puissances

# ======================================================================================
def afficher_frequence_alpha_dominante(freqs, t, picks=['P3', 'Pz', 'P4']):
    """
    Affichage graphique de la fréquence alpha dominante par seconde pour chaque canal

    :param: freqs (ndarray): Fréquences dominantes
    t (ndarray) : Temps
    picks (liste): Noms des électrodes
    """
    for i, nom in enumerate(picks):
        plt.figure(figsize=(8, 4))
        plt.plot(t, freqs[i], marker='.')
        plt.xlabel("Temps (s)")
        plt.ylabel("Fréquence alpha dominante (Hz)")
        plt.title(f"Fréquence alpha dominante – {nom}")
        plt.ylim(7, 13)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
# ======================================================================================
def afficher_puissance_alpha_superieur(puissances, t, picks=['P3', 'Pz', 'P4']):
    """
    Affichage grapjique des alphas supérieurs en focntion du temps

    :param: puissances (ndarray) : Puissance alpha
    t (ndarray) : Temps
    picks (liste): Noms des électrodes
    """
    for i, nom in enumerate(picks):
        plt.figure(figsize=(8, 4))
        plt.plot(t, puissances[i], marker='.')
        plt.xlabel("Temps (s)")
        plt.ylabel("Puissance alpha supérieur (μV²/Hz)")
        plt.title(f"Puissance alpha supérieure – {nom}")
        plt.grid(True)
        max_val = np.max(puissances[i])
        plt.ylim(0, max_val * 1.2)
        plt.tight_layout()
        plt.show()

# ======================================================================================
if __name__ == "__main__":
    # 1. Fichier yeux fermés pour l’IAF
    fichier_fermes = "B63_CE_baseline.gdf"
    data_fermes, sfreq = charger_filtrer_alpha(fichier_fermes, picks=['P3', 'Pz', 'P4'], graph=False)
    iaf = estimer_IAF(data_fermes, sfreq)
    print(f"IAF estimée à partir des yeux fermés : {iaf:.2f} Hz")

    # 2. Fichier yeux ouverts pour l’analyse
    fichier_ouverts = "B63_OE_baseline.gdf"
    data_ouverts, _ = charger_filtrer_alpha(fichier_ouverts, picks=['P3', 'Pz', 'P4'], graph=True)

    # 3. Fréquences dominantes par seconde
    t_freq, freq_dom = calcul_frequence_dominante(data_ouverts, sfreq)
    afficher_frequence_alpha_dominante(freq_dom, t_freq, picks=['P3', 'Pz', 'P4'])

    # 4. Puissance dans la bande alpha supérieure personnalisée
    t_puiss, puissances = calcul_puissance_alpha_superieur(data_ouverts, sfreq, iaf)
    afficher_puissance_alpha_superieur(puissances, t_puiss, picks=['P3', 'Pz', 'P4'])
