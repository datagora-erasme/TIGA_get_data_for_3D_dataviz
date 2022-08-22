"""
This script ensures all the datapipeline and data treatment
in order to get all the industry facilities in some french areas
in order to know where do people work in industry in France
"""
import json
import time
import csv
import re
import requests
import pandas as pd

def get_interesting_naf_codes():
    """
    Fonction qui va chercher sur la page notion ==>
    https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81
    les codes NAFs intéressants
    Cette page Notion est une copie de la page NOTION ERASME :
    https://www.notion.so/erasme/Atelier-nouveaux-usages-991f34f08e61463b9027eb666ac554e1
    TODO : gérer les MAJ en intégrant directement la page NOTION ERASME
    (demander à être admin ou un token )
    """

    codes_naf = []
    codes_sp = []
    definitions = []
    groupes = []
    groupes_distinct = []

    urls = [
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#cca152a983b148bbb4ef4323a4cbeb50",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#3258f0238d2847a0a5d5c17215893ecc",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#ff3f205c57e743bcbb1fd3b3f06abc4e",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#f499d30971934fe19aeeaf26747f8f39",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#6ce53a54a2bd4256afbaf077fbba9d1e",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#7cd489356fb5478283124624cd5b9b4d",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#20bffa6fd5124de69cca9d4a6fffd482",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#b0d7ef12ffd04774b8e077604ee6970c",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#218a03f964734edca85da19d766dc826",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#3e6ba423acf24ee0b5b3a3254c23f3f4",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#f3053073078e423ab26535febf14945d",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#d33b3788699f44b086a419d3eb0a6bc7",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#ebb8dd6dd5954002bb62c03781ad58e7",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#b7c9a63139c04c89a86f4c052fe0f8e9",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-"
        "5198447ed79746c590da4c3c9cb0cc81#b8cece22716a454796414766c310fc2c"
    ]

    for url in urls:

        print("Extraction des NAFs codes : ", int(urls.index(url) / len(urls) * 100), '% \n')

        block_id = url[112:]
        # print(block_id)
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

        # codes_list est la liste des codes naf récupérés sur la page
        codes_list = re.findall(r"\d\d\d\d[A-Z]", text)
        # print("\n A :", a)
        codes_list = codes_list[:(len(codes_list) // 2)]
        # definition est la définition donnée au code NAF correspondant
        definition = re.findall(r"\((.*?)\)", text)
        definition = definition[:(len(definition) // 2)]
        definition = definition[1:]
        # print("Définitions : ", definition)
        definitions += definition

        for code in codes_list:
            # get_definition of NAF
            i = text.index(code)
            # print("indice de debut", i)
            codes_sp.append(code)
            code_naf = code[0:2] + '.' + code[2:]
            codes_naf.append(code_naf)
            groupes.append(nom_groupe)


    #save the list of NAF codes in order to reuse it later
    with open("interesting_naf_codes.csv", "w", encoding='utf-8') as file:
        # écriture du header
        file.write("Code NAF|Définition|Groupe \n")
        for i in range(len(codes_sp)):
            file.write(codes_sp[i])
            file.write('|')
            file.write(definitions[i])
            file.write('|')
            file.write(groupes[i])
            file.write('\n')

    print("Extraction des NAFs codes : 100% terminé")

def update_geoloc(depts):
    """
    create the function to process the geolocated siret file
    """

    chunk_size = 500000
    batch_no = 1
    types = {
        'siret': 'int64',
        'x_longitude': 'float32',
        'y_latitude': 'float32',
        'plg_code_commune': 'int32'
    }

    path = "data/GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.csv"
    for chunk in pd.read_csv(path, chunksize=chunk_size, delimiter=';'):
        # division du large csv en plusieurs chunks
        # on ne sélectionne que la data qui nous intéresse
        chunk = chunk[['siret', 'x_longitude', 'y_latitude', 'plg_code_commune']]

        # on sélectionne les datas dans les départements qui nous intéressent
        temp_chunk = chunk[chunk['plg_code_commune'].str[:2] == depts[0]]
        for dept in depts[1:]:
            temp_chunk = pd.concat([temp_chunk, chunk[chunk['plg_code_commune'].str[:2] == dept]])

        chunk = temp_chunk
        chunk = chunk.astype(types)
        if batch_no == 1:
            final_chunk = chunk
        else:
            final_chunk = pd.concat([final_chunk, chunk])
        batch_no += 1
        print("Process update Geoloc", int(batch_no*chunk_size/32562762*100), '%')

    # save final_chunk as a csv
    final_chunk.to_csv("data/GeolocProcessed.csv")

def update_etablissement(depts):
    """
    create the function to process the Etablissement file
    """

    chunk_size = 100000
    batch_no = 1

    headers_to_keep = [
        'siren',
        'siret',
        'trancheEffectifsEtablissement',
        'activitePrincipaleEtablissement',
        'codeCommuneEtablissement'
    ]

    for input_df in pd.read_csv("data/StockEtablissement_utf8.csv", chunksize=chunk_size):
        input_df = input_df[headers_to_keep]

        temp_df = input_df[input_df['codeCommuneEtablissement'].str[:2] == depts[0]]
        for dept in depts[1:]:
            temp_df = pd.concat([
                temp_df,
                input_df[input_df['codeCommuneEtablissement'].str[:2] == dept]
            ])

        temp_df = temp_df.dropna()
        temp_df = temp_df[temp_df['trancheEffectifsEtablissement'] != 'NN']

        if batch_no == 1:
            final_df = temp_df
        else:
            final_df = pd.concat([final_df, temp_df])
        batch_no += 1
        print("Process update_Etablissement", int(batch_no*chunk_size/32783873*100), '%')

    #save processed df as a csv
    final_df.to_csv("data/EtablissementProcessed.csv")

def etablissement_interesting_naf():
    """
    function that process EtablissementProcessed in order to select
    only the interesting naf codes sirets
    """

    input_df = pd.read_csv("data/EtablissementProcessed.csv")

    # chargement en mémoire des codes nafs
    naf_codes = []
    with open("interesting_naf_codes.csv", 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='|')
        for line in reader:
            naf_codes.append(line["Code NAF"][:2] + '.' + line["Code NAF"][2:])

    input_df = input_df.astype('string')

    final_df = input_df[input_df['activitePrincipaleEtablissement'] == naf_codes[0]]
    for code in naf_codes[1:]:
        new_df = input_df[input_df['activitePrincipaleEtablissement'] == code]
        final_df = pd.concat([final_df, new_df])

    #save the final_df
    final_df.to_csv("data/EtablissmentNAFProcessed.csv")

def joint_geoloc_etablissement():
    """
    funcion that joins Geoloc and Etablissement in order to create the output file
    """

    df_geoloc = pd.read_csv('data/EtablissmentNAFProcessed.csv')
    df_etablissement = pd.read_csv('data/GeolocProcessed.csv')

    output_df = pd.merge(df_etablissement, df_geoloc, on='siret')
    col_interest = [
        "siret",
        "x_longitude",
        "y_latitude",
        "siren",
        "trancheEffectifsEtablissement",
        "activitePrincipaleEtablissement"
    ]
    output_df = output_df[col_interest]
    output_df.rename(columns={
        'x_longitude': 'lng',
        'y_latitude': 'lat',
        'trancheEffectifsEtablissement': 'RH',
        'activitePrincipaleEtablissement': 'NAF'
    }, inplace=True)

    # Get the definition of RH workforce on
    # https://www.sirene.fr/static-resources/doc/Description%20liste%20sirene-fr.pdf?version=1.33.25

    dict_rh = {
        0: '0 salarié',
        1: '1 ou 2 salariés',
        2: '3 à 5 salariés',
        3: '6 à 9 salariés',
        11: '10 à 19 salariés',
        12: '20 à 49 salariés',
        21: '50 à 99 salariés',
        22: '100 à 199 salariés',
        31: '200 à 249 salariés',
        32: '250 à 499 salariés',
        41: '500 à 999 salariés',
        42: '1 000 à 1 999 salariés',
        51: '2 000 à 4 999 salariés',
        52: '5 000 à 9 999 salariés',
        53: '10 000 salariés et plus'
    }

    for item in dict_rh.items():
        output_df.loc[(output_df.RH == item[0], 'RH')] = item[1]

    new_dict_rh = {
        '0 salarié': 0,
        '1 ou 2 salariés': 2,
        '3 à 5 salariés': 4,
        '6 à 9 salariés': 8,
        '10 à 19 salariés': 15,
        '20 à 49 salariés': 35,
        '50 à 99 salariés': 75,
        '100 à 199 salariés': 150,
        '200 à 249 salariés': 225,
        '250 à 499 salariés': 350,
        '500 à 999 salariés': 750,
        '1 000 à 1 999 salariés': 1500,
        '2 000 à 4 999 salariés': 3500,
        '5 000 à 9 999 salariés': 7500,
        '10 000 salariés et plus': 1000
    }

    for item in new_dict_rh.items():
        output_df.loc[(output_df.RH == item[0], 'RH')] = item[1]
    output_df = output_df.astype({'RH': int})

    # Add groupe and définitions
    df_interesting = pd.read_csv("interesting_naf_codes.csv", delimiter='|')
    df_interesting = df_interesting.astype('string')
    df_interesting.rename(columns={'Code NAF': 'NAF'}, inplace=True)
    df_interesting['NAF'] = df_interesting['NAF'].apply(lambda x: x[:2] + '.' + x[2:])

    output_df = pd.merge(output_df, df_interesting, on="NAF")
    output_df.rename(columns={"Groupe ": 'Groupe', "Définition": "Activité"}, inplace=True)

    # export data to csv
    output_df.to_csv("output.csv", index=False)

    #export data to geoJSON
    geo_json = df_to_geojson(dataframe=output_df)
    with open('output.json', 'w', encoding='utf-8') as file:
        json.dump(geo_json, file)

def df_to_geojson(dataframe, latitude='lat', longitude='lng'):
    """
    function that creates a geoJSON file from the output file
    :param dataframe: the dataframe to export in geoJSON
    :param latitude: the string of the column containing the latitude data
    :param longitude: the string of the column containing the longitude data
    :return: Python dictionary formatted as a geoJSON dict
    """

    geojson = dict(type="FeatureCollection")
    geojson['features'] = []

    for _, row in dataframe.iterrows():
        # create a feature template
        feature = dict(type='Feature')
        feature['properties'] = {}
        feature['geometry'] = {
            'type': 'Point',
            'coordinates': []
        }
         # fill in the coordinates
        feature['geometry']['coordinates'] = [row[longitude], row[latitude]]
        # fill in the properties
        for prop in dataframe.columns:
            feature['properties'][prop] = row[prop]
        #add this feature to the list of features
        geojson['features'].append(feature)
    return geojson

if __name__ == '__main__':

    departements = [
        '69'
    ]

    t0 = time.time()
    #get_interesting_naf_codes()
    #update_geoloc(departements)
    #update_etablissement(departements)
    #etablissement_interesting_naf()
    joint_geoloc_etablissement()
    t1 = time.time()
    print("fini en : ", t1-t0, 's')
