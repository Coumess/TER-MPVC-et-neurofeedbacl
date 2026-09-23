# Une thérapie innovante pour contrer les atteintes cognitives dû à la Maladie des Petits Vaisseaux Cérébraux

**Auteurs : Angely Charles, Coumes Alexandre et Poisson Eliott** \
**Superviseurs : Mazon Cécile et Pech Marion** \
**Institution : L3 MIASHS, Année universitaire 2024-2025**

Ce projet propose une thérapie non médicamenteuse innovante pour les patients atteints de la maladie des petits vaisseaux cérébraux (MPVC) et présentant des troubles cognitifs légers (MCI). La MPVC étant un facteur de risque majeur de déclin cognitif sans traitement curatif médicamenteux spécifique, ce projet a pour but de prévenir ce déclin et de préserver l'autonomie des patients. Pour atteindre cet objectif, nous explorons une approche combinant un entraînement cognitif et du neurofeedback par électroencéphalogramme (EEG).

## Méthodologie :
*   **Protocole :** Le projet propose le design d'une étude longitudinale s'étalant sur 8 semaines, avec une évaluation des fonctions cognitives au jour 0 et au jour 56.
*   **Participants :** La population cible est constituée d'individus âgés de 65 à 70 ans, atteints de la MPVC avec des troubles cognitifs légers, identifiés par un score de 0.5 à l'échelle Clinical Dementia Rating.
*   **Groupes :** Le protocole prévoit de diviser les participants en quatre groupes : un groupe contrôle (sans intervention), un groupe avec entraînement cognitif uniquement, un groupe avec neurofeedback uniquement, et un groupe combinant les deux interventions.
*   **Neurofeedback :** L'approche utilise un casque EEG portable (neuroNicle FX2) qui permet aux participants de visualiser et de moduler l'activité de leurs ondes alpha et alpha supérieures.
*   **Entraînement cognitif :** Les participants réalisent des exercices ciblés principalement sur la vitesse de traitement visuel, la vitesse de traitement auditif et la mémoire de travail.
*   **Développement Informatique :** Dans le cadre de ce projet, une interface de simulation de neurofeedback a été développée en Python. Elle s'appuie sur la bibliothèque MNE pour le traitement et le filtrage du signal EEG, ainsi que sur la bibliothèque ezTK pour générer l'interface graphique interactive.

## Résultats et Discussion :
*   Ce travail pose le cadre expérimental d'une future étude clinique.
*   Notre hypothèse principale est que les groupes bénéficiant d'une intervention (neurofeedback, entraînement cognitif, ou les deux) présenteront une amélioration ou une stabilisation de leurs performances cognitives par rapport au groupe contrôle.
*   L'hypothèse secondaire suggère que le groupe recevant la double intervention montrera des bénéfices plus marqués, indiquant un potentiel effet cumulatif des deux thérapies.
*   Sur le plan technique, le programme de neurofeedback conçu constitue une preuve de concept fonctionnelle.
*   Bien qu'il n'ait pas été testé sur des sujets réels, le programme est capable d'analyser une base de données EEG existante et de fournir un retour visuel (des carrés devenant plus ou moins rouges) qui s'adapte en temps réel en fonction de la fréquence dominante ou de la puissance spectrale de la bande alpha.

# Lire le rapport complet (PDF)
Ce README n'est qu'un aperçu de notre étude. [Cliquez ici pour lire le rapport complet](https://github.com/Coumess/TER-MPVC-et-neurofeedbacl/blob/main/TER%20Maladiesdes%20Petits%20Vaisseaux%20C%C3%A9r%C3%A9braux.pdf)
