# TIGA_get_data_for_3D_dataViz

# Pour Yassin
Les données de sortie sont:
  output.json ou output.csv
  

## Description du projet

### Motivation

Ce projet fait suite à la cartographie [suivante](https://github.com/datagora-erasme/datagora_dataviz3D).


Cette cartographie avait pour intérêt de représenter les effectifs travaillant dans l'industrie sur le territoire métropolitain lyonnais. Les données utilisées par ce projet sont des données métropolitaines disponibles sur [data.grandlyon](https://data.grandlyon.com/jeux-de-donnees/base-sirene-metropole-lyon/telechargements). Ce projet récupère les effectifs des entreprises et trace un hexagone au niveau du siège social de l'entreprise avec une hauteur variable en fonction de l'effectif.

L'objectif de ce projet est de récupérer les données pour faire la même cartographie mais en prenant en compte les établissements des entreprises (c'est à dire les numéros de SIRET), ceux-ci sont plus proches de représenter les lieux réels d'activité industrielle que le numéro de SIREN attaché au siège social.

La deuxième motivation du projet est d'étendre ce projet aux départements de la Loire(42) et du Rhône(69) (en réalité il est maintenant étendable à tout département français !)

### Sources de données

Ce projet utlise deux sources de données gouvernementales.

La source de données (_Base SIRENE_) permettant de récupérer les effectifs par code SIRET des entreprises qui sont dans un département qui nous intéresse ainsi qu'avec une activité qui nous intéresse (industrie) : voir [ici](https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/)

[lien de téléchargement direct](https://www.data.gouv.fr/fr/datasets/r/0651fb76-bcf3-4f6a-a38d-bc04fa708576) (!!! Fichier d'un peu moins de 6Go !!!)

La source de données permettant de géocoder les lignes SIRET que l'on a extrait : voir [ici](https://www.data.gouv.fr/fr/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/)

### Description du traitement de données

* Récupération sur la page Notion des codes NAF (Nomenclature d'activité Française) correspondant aux industries qui nous intéressent
* Filtrage sur la source SIRENE pour n'extraire que les établissement indiqués dans le 69 et le 42 et qui ont leur code NAF inscrit dans la liste récupérée précédemment
* Filtrage du fichier contenant le géocodage des établissements (identifiés par leur numéro de SIRET) pour ne garder que les établissement dans le 69 et le 42 (afin de minimiser la taille des fichiers utilisés lors de la jointure des deux fichiers, pour une rapidité d'exécution optimale)
* Jointure des fichiers contenant les informations (trancheEffectif, activité...) des entreprises et leur géocodage
* Construction des fichiers de sortie (CSV et geoJSON)

## Installer et lancer le projet

1. Cloner le repository
2. Télécharger les données d'entrée et les placer dans le repository ./data : [CSV avec la data](https://www.data.gouv.fr/fr/datasets/r/0651fb76-bcf3-4f6a-a38d-bc04fa708576) | [CSV avec la géolocalisation](https://www.data.gouv.fr/fr/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/)
3. Installer les librairies nécessaires (pip install -r requirements.txt)
4. Spécifier les départements sur lesquels on veut traiter des données (de base '69' et '42')
5. Lancer le script de traitement des données (py main.py)

## Comment utiliser le projet

## Credits
=======
