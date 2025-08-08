#Importamos las líbrerias necesarias
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


#----------------------------------CREACIÓN FUNCIÓN DE SCRAPEO PARA CADA ESTADÍSITICA-------------------------------

def scrape_fbref_estadistica_unica(url, table_id, stat_group_name):
    """
    Extrae una tabla de FBref y genera nombres de columna jerárquicos con formato:
    <grupo_general>_<over_header>_<data-stat>
    
    :param url: URL de la tabla
    :param table_id: ID de la tabla HTML
    :param stat_group_name: Nombre general del grupo estadístico (ej: 'playingtime', 'shooting', etc.)
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': table_id})
    if table is None:
        raise ValueError(f"No se encontró ninguna tabla con id='{table_id}'")

    # Encuentra el último row de thead (donde están los th con data-stat)
    header_row = table.find('thead').find_all('tr')[-1]
    columns = []
    for th in header_row.find_all('th'):
        data_stat = th.get('data-stat')
        if not data_stat or data_stat.strip() == '':
            continue
        
        over_header = th.get('data-over-header')
        if over_header:
            col_name = f"{stat_group_name.lower()}_{over_header.lower().replace(' ', '')}_{data_stat}"
        else:
            col_name = f"{stat_group_name.lower()}_{data_stat}"
        columns.append(col_name)

    # Añadimos columna adicional para la URL del jugador
    columns.append('player_url')

    # Extraer filas del cuerpo
    data_rows = []
    for row in table.find('tbody').find_all('tr'):
        if row.get('class') and 'thead' in row.get('class'):
            continue

        row_data = []
        for th in header_row.find_all('th'):
            data_stat = th.get('data-stat')
            if not data_stat or data_stat.strip() == '':
                continue

            cell = row.find('td', {'data-stat': data_stat}) or row.find('th', {'data-stat': data_stat})
            row_data.append(cell.get_text(strip=True) if cell else None)

        # Añadir URL del jugador
        player_cell = row.find('td', {'data-stat': 'player'})
        if player_cell and player_cell.find('a'):
            player_url = 'https://fbref.com' + player_cell.find('a')['href']
        else:
            player_url = None
        row_data.append(player_url)

        data_rows.append(row_data)

    df = pd.DataFrame(data_rows, columns=columns)
    
    return df


#-----------------------------------------CREACIÓN CLASE--------------------------------------------------------
class FBrefStatsGroups:
    def __init__(self, temporada: str = '2024-2025'):
        
        self.temporada = temporada

        # URLs de jugadores de campo
        self.urls_field_players = {
            'stats': 'https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats',
            'shooting': 'https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats',
            'passing': 'https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats',
            'passing_types': 'https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats',
            'gca': 'https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats',
            'defense': 'https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats',
            'possession': 'https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats',
            'playingtime': 'https://fbref.com/en/comps/Big5/playingtime/players/Big-5-European-Leagues-Stats',
            'misc': 'https://fbref.com/en/comps/Big5/misc/players/Big-5-European-Leagues-Stats',
        }

                # Generar URLs dinámicamente por temporada
        self.urls_field_players = {
            key: f"https://fbref.com/en/comps/Big5/{self.temporada}/{key}/players/{self.temporada}-Big-5-European-Leagues-Stats"
            for key in [
                'stats', 'shooting', 'passing', 'passing_types', 'gca',
                'defense', 'possession', 'playingtime', 'misc'
            ]
        }



        # Table IDs por tipo
        self.table_ids = {
            'stats': 'stats_standard',
            'shooting': 'stats_shooting',
            'passing': 'stats_passing',
            'passing_types': 'stats_passing_types',
            'gca': 'stats_gca',
            'defense': 'stats_defense',
            'possession': 'stats_possession',
            'playingtime': 'stats_playing_time',
            'misc': 'stats_misc',
        }

        # stat_group extraído del nombre del bloque (igual al nombre de la clave en las URLs)
        self.stat_groups = {**self.urls_field_players}

    def get_url(self, group_name: str) -> str:
        return self.urls_field_players.get(group_name) 

    def get_table_id(self, group_name: str) -> str:
        return self.table_ids.get(group_name)

    def get_stat_group(self, group_name: str) -> str:
        return group_name  
    

    #FUNCION PARA SCRAPEAR UNA UNICA ESTADISTICA CONCRETA (SUCIO)
    def scrape_group(self, group_name: str) -> pd.DataFrame:
        url = self.get_url(group_name)
        table_id = self.get_table_id(group_name)
        stat_group = self.get_stat_group(group_name)
        print(f"Scraping {group_name} → {url}")
        return scrape_fbref_estadistica_unica(url, table_id, stat_group)
