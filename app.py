"""
Fichier principal d'exécution pour la récupération et le traitement des données
"""

""" import necessary libraries"""
import csv
import time
import requests
import re
import sqlite3

def get_interesting_naf_codes():
    """ 
    Fonction qui va chercher sur la page notion ==> https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81 les codes NAFs intéressants
    Cette page Notion est une copie de la page NOTION ERASME : https://www.notion.so/erasme/Atelier-nouveaux-usages-991f34f08e61463b9027eb666ac554e1
    TODO : gérer les MAJ en intégrant directement la page NOTION ERASME (demander à être admin ou un token )
    """
    
    codes_naf = []
    codes_sp = []
    definitions = []
    groupes = []
    groupes_distinct = []

    urls = [
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#cca152a983b148bbb4ef4323a4cbeb50",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#3258f0238d2847a0a5d5c17215893ecc",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#ff3f205c57e743bcbb1fd3b3f06abc4e",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#f499d30971934fe19aeeaf26747f8f39",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#6ce53a54a2bd4256afbaf077fbba9d1e",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#7cd489356fb5478283124624cd5b9b4d",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#20bffa6fd5124de69cca9d4a6fffd482",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#b0d7ef12ffd04774b8e077604ee6970c",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#218a03f964734edca85da19d766dc826",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#3e6ba423acf24ee0b5b3a3254c23f3f4",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#f3053073078e423ab26535febf14945d",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#d33b3788699f44b086a419d3eb0a6bc7",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#ebb8dd6dd5954002bb62c03781ad58e7",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#b7c9a63139c04c89a86f4c052fe0f8e9",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#b8cece22716a454796414766c310fc2c"
        ]

    for url in urls:
        
        print("Extraction des NAFs codes : ", int(urls.index(url)/len(urls)*100),'% \n')

        block_id = url[112:]
        #print(block_id)
        url = f"https://api.notion.com/v1/blocks/{block_id}"
    
        headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-02-22",
            "Authorization": "Bearer secret_VyB7EbB3zAW0SVcGE1UfuMQc80uQ1vrlurKHbMnxalK"
        }
        
        response = requests.get(url, headers=headers)
        text = response.text
        # nom_groupe est le nom que l'on voulait donner au groupement de code NAF (un par URL)
        nom_groupe = response.json()['numbered_list_item']['rich_text'][0]['text']['content']
        groupes_distinct.append(nom_groupe)
        
        pattern = "\d\d\d\d[A-Z]"
        # a est la liste des codes naf réupérés sur la page
        a = re.findall("\d\d\d\d[A-Z]", text)
        # print("\n A :", a)
        a = a[:(len(a)//2)]
        # definition est la définition donnée au code NAF correspondant
        definition = re.findall("\((.*?)\)", text)
        definition = definition[:(len(definition)//2)]
        definition = definition[1:]
        #print("Définitions : ", definition)
        definitions += definition

        for code in a:
            # get_definition of NAF
            i = text.index(code)
            #print("indice de debut", i)
            codes_sp.append(code)
            code_naf = code[0:2] + '.' + code[2:]
            codes_naf.append(code_naf)
            groupes.append(nom_groupe)

    """save the list of NAF codes in order to reuse it later"""
    with open("interesting_naf_codes.csv", "w", encoding='utf-8') as f:
        # écriture du header
        f.write("Code NAF; Définition; Groupe \n")
        for i in range(len(codes_sp)):
            f.write(codes_sp[i])
            #ajout de l'écriture f.write(',' + definition)
            f.write('; ')
            f.write(definitions[i])
            f.write('; ')
            f.write(groupes[i])
            f.write('\n')
    
    #print('\n groupes distinct : ', groupes_distinct)
    print("Extraction des NAFs codes : 100% terminé")


def filter_csv(departements):
    """
    filter_csv effectue un premier tri sur StockEtablissement_utf8.csv en ne gardant que les SIRET qui appartiennent aux départements ciblés
    et qui ont un code NAF présent dans la liste
    """
    # Prend en argument departements = liste des départements intéressants, naf_codes = liste des codes NAF intéressants

    t0 = time.time()

    # définition des champs que l'on va chercher dans les données
    filtres = [
        'siren',
        'siret',
        'trancheEffectifsEtablissement',
        'activitePrincipaleEtablissement',
        'nomenclatureActivitePrincipaleEtablissement',
        'complementAdresseEtablissement',
        'numeroVoieEtablissement',
        'indiceRepetitionEtablissement',
        'indiceRepetitionEtablissement',
        'libelleVoieEtablissement',
        'codePostalEtablissement',
        'libelleCommuneEtablissement',
        'codeCommuneEtablissement',
        'codeCedexEtablissement',
        'libelleCedexEtablissement'
    ]

    filtres_adresse = [
        'complementAdresseEtablissement',
        'numeroVoieEtablissement',
        'indiceRepetitionEtablissement',
        'indiceRepetitionEtablissement',
        'libelleVoieEtablissement',
        'codePostalEtablissement',
        'libelleCommuneEtablissement',
        'codeCommuneEtablissement',
        'codeCedexEtablissement',
        'libelleCedexEtablissement'
    ]

    # chargement en mémoire des codes nafs
    naf_codes = []
    with open("interesting_naf_codes.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            naf_codes.append(line["Code NAF"][:2]+'.'+line["Code NAF"][2:])

    # ouverture du fichier d'entrée, mise en mémoire vive (list_dic) uniquement des lignes qui nous intéressent
    entree = open(r"StockEtablissement_utf8.csv", 'r', encoding='utf-8')
    reader = csv.DictReader(entree)
    d = next(reader)
    header = {filtre: d[filtre] for filtre in filtres}
    header['adresse'] = ''
    list_dic = []       # liste des lignes ciblées

    nb_lignes_tot = 32783872
    line_index = 0

    for  line in reader:
        line_index += 1

        if line_index%100000 == 0:
            print("Extraction des données de StockEtablissement_utf8.csv : ", int(line_index/nb_lignes_tot*100), '%')

        #print(line['codeCommuneEtablissement'][:2])
        if line['codeCommuneEtablissement'][:2] in departements:
            if line["activitePrincipaleEtablissement"] in naf_codes:
                #print('\n Siret détecté qui colle aux filtres !!')
                new = {filtre: line[filtre] for filtre in filtres}
                adresse = [line[filtre] for filtre in filtres_adresse]
                str_adresse = ' '.join(filter(None,adresse))
                #print("Adresse : ", str_adresse)
                new["adresse"] = str_adresse
                list_dic.append(new)
    entree.close()

    rendu = open(r"StockEtablissement_utf8_69_42_nafs.csv", 'w', newline='')
    writer = csv.DictWriter(rendu, fieldnames=header, delimiter=";")
    writer.writeheader()
    for dic in list_dic:
        writer.writerow(dic)
    rendu.close()

    t1 = time.time()
    print("Extraction des données de StockEtablissement_utf8.csv : 100% terminé")
    print("temps écoulé", int((t1-t0)//60), 'min', int((t1-t0)%60), 's')


def get_siret_from_dept(departements):
    """
    get_siret_from_dept filtre  le fichier des SIRET géolocalisés pour ne garder que ceux dans les départements d'intérêt
    """
    lines_in_dept = []
    t0 = time.time()
    nb_lignes_tot = 32562762

    with open("GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.csv", 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        header = next(reader)
        line_index = 0
        for line in reader:
            line_index += 1
            if line["plg_code_commune"][:2] in departements:
                lines_in_dept.append(line)
            if line_index%100000 == 0:
                print("Extraction des données de GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.csv : ", int(line_index/nb_lignes_tot*100), '%')
    print("Extraction des données de GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.csv : 100% terminé")

    print("Ecriture des données ..")
    with open("GeolocalisationEtablissement_69_42.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter=";")
        writer.writeheader()
        for line in lines_in_dept:
            writer.writerow(line)
    t1 = time.time()
    print("Ecriture des données terminée ..")
    print("temps écoulé : ", int((t1-t0)//60), ' min ', int((t1-t0)%60), ' s')


def createTable(filename):
    """
    createTable va créer une BDD SQL et la remplir en créant une table par fichier (ici StockEtablissement et GeolocalisationEtablissement)
    """
    conn = sqlite3.connect('StockEtablissementGeoloc.db')
    c = conn.cursor()
    tablename = filename[:-4]
    print("tablename : ", tablename)
    with open(filename, 'r') as f:

        #supression de la table
        try:
            c.execute("DROP TABLE " + tablename)
        except:
            pass

        #création de la table
        headers = next(f).split(";")
        print(headers)
        print("longueur headers : ", len(headers))
        sql = f'CREATE TABLE ' + tablename + ' ('
        for header in headers:
            sql += str(header) + ",\n"
        sql = sql[:-3]
        sql += ')'
        print(sql)
        c.execute(sql)

        sql = "INSERT INTO " +  tablename + " VALUES ("
        for k in range(len(headers)-1):
            sql += "?,"
        sql += '?)'
        print("deuxieme sql : ", sql)
        for row in f:
            try:
                c.execute(sql, row.split(";"),)
            except:
                print(row)
    conn.commit()


    conn.close()

def join_tables(files):
    """
    join_tables va ouvrir la bdd StockEtablissementGeoloc.db et va faire la jointure entre les deux tables précédemment créées
    """
    filenames = [f[:-4] for f in files]
    print(filenames)
    ## filenames est une liste contenant le nom des tables à joindre de la database

    conn = sqlite3.connect('StockEtablissementGeoloc.db')
    c = conn.cursor()

    try:
        c.execute("DROP TABLE StockEtablissementGeoloc")
    except:
        pass

    sql = """
    CREATE TABLE StockEtablissementGeoloc AS
    SELECT * 
    FROM """
    sql += filenames[0]
    sql += """ AS a inner join  """
    sql += filenames[1]
    sql += """ AS b on a.siret = b.siret
    WHERE trancheEffectifsEtablissement IS NOT "" and trancheEffectifsEtablissement IS NOT "NN"
    """
    print("\nLe SQL pour la jointure est : ", sql)
    c.execute(sql)
    conn.commit()
    conn.close()
    print("\nTout s'est bien déroulé")

#exportation de la jointure vers un CSV

def export_data_to_csv():
    """
    export_data_to_csv permet de récupérer la table ainsi créée et de l'exportee au format csv
    """
    conn = sqlite3.connect("StockEtablissementGeoloc.db")
    c = conn.cursor()
    c.execute("SELECT * FROM StockEtablissementGeoloc")

    with open("StockEtablissementGeoloc.csv", 'w', newline='', encoding='utf-8') as f :
        writer = csv.writer(f)
        writer.writerow([i[0] for i in c.description])
        writer.writerows(c)
    
    conn.close()

def add_activite_groupe():
    """
    add_activite_groupe ajoute une colonne activité et groupe correspondant à chaque SIRET dans le CSV ainsi créé
    """
    table = open("StockEtablissementGeoloc.csv", 'r', encoding='utf-8')
    csv_reader = csv.DictReader(table)
    headers = next(csv_reader)
    headers['Activité'] = ''
    headers['Groupe'] = ''
    table.close()

    """Récupération des données NAF codes, activités et groupes correspondant"""
    nafs = []
    definitions = []
    groupes = []
    with open("interesting_naf_codes.txt", 'r') as f:
        for line in f:
            naf, defin, groupe = line.split('| ')
            # formatage du code naf comme dans le CSV
            naf = naf[:2] + '.' + naf[2:]
            nafs.append(naf)
            definitions.append(defin)
            groupes.append(groupe)


    with open("StockEtablissementGeoloc.csv", 'r', encoding='utf-8') as old_csv:
        old_reader = csv.DictReader(old_csv)
        new_csv = open("StockEtablissementGeolocActiviteGroupe.csv", 'w', encoding='utf-8', newline='')
        new_writer = csv.DictWriter(new_csv, fieldnames=headers)
        new_writer.writeheader()
        
        for line in old_reader:
            i_naf = nafs.index(line['activitePrincipaleEtablissement'])
            line['Activité'] = definitions[i_naf][:-1]
            line['Groupe'] = groupes[i_naf][:-1]
            
            new_writer.writerow(line)
        
        new_csv.close()

def from_csv_to_geojson():
    """
    from_csv_to_geojson va lire le fichier de sortie ainsi créé (StockEtablissementGeolocActiviteGroupe.csv)
    et va produire un autre fichier de sortie en geoJSON
    """
    geoJSON = dict(type="FeatureCollection")
    geoJSON["features"] = []

    with open("StockEtablissementGeolocActiviteGroupe.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            print(line)
            feature = dict(type='Feature')
            feature['properties'] = {}
            feature['properties']['Adresse'] = line['adresse']
            feature['properties']['SIRET'] = line['siret']
            feature['properties']['SIREN'] = line['siren']
            feature['properties']['Effectif'] = line['trancheEffectifsEtablissement']
            feature['properties']['activitePrincipaleEtablissement'] = line["activitePrincipaleEtablissement"]
            feature['properties']["nomenclatureActivitePrincipaleEtablissement"] = line["nomenclatureActivitePrincipaleEtablissement"]
            feature['properties']["Groupe"] = line['Groupe']
            feature['properties']["Activité"] = line['Activité']
            
            feature['geometry'] = dict(type='Point')
            feature['geometry']["coordinates"] = [float(line['x_longitude']), float(line['y_latitude'])]
            
            geoJSON['features'].append(feature)


    #save geoJSON
    with open("StockEtablissementGeolocActiviteGroupe.json", 'w', encoding='utf-8') as fp:
        json.dump(geoJSON, fp)
            



if __name__ == '__main__':

    departements = [
        '69',
        '42'
    ]
    
    # extraction des codes NAF qui nous intéressent de la page NOTION
    #get_interesting_naf_codes()

    # extraction des lignes qui sont à la fois dans un des départements d'intérêt et dans les codes NAF intéressants
    filter_csv(departements)

    # extraction de la bdd geolocalisée des SIRET uniquement les SIRET dans les départements d'intérêt
    get_siret_from_dept(departements)

    #jointure entre le fichier StockEtalissement_utf8_69_42_nafs.csv et le fichier des SIRET géolocalisés
    files = [
    "GeolocalisationEtablissement_69_42.csv",
    "StockEtablissement_utf8_69_42_nafs.csv"
    ]
    for f in files:
        # création des tables SQL
        createTable(f)
    
    #jointure entre les deux tables
    join_tables(files)

    #export des données au format CSV
    export_data_to_csv()

    # ajout de l'activité et du groupe
    add_activite_groupe()

    # export au format geoJSON
    from_csv_to_geojson()