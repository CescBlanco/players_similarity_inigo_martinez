from datetime import datetime

from functools import reduce
import pandas as pd

#-----------------------------------FUNCIÓN PARA LIMPIAR EL CONTENIDO DELOS DATAFRAMES----------------------------------------------

def limpiar_filas_estadisticas(df):
    
    mapeo_columns= {
    #stats
    'stats_ranker': 'ranker',
    'stats_player': 'jugador',
    'stats_nationality': 'nacionalidad',
    'stats_position': 'posicion',
    'stats_team': 'equipo',
    'stats_comp_level': 'competicion',
    'stats_age': 'edad',
    'stats_birth_year': 'año',
    'stats_playingtime_minutes_90s': 'minutos jugados/90',
    'stats_playingtime_minutes': 'minutos jugados',
    'stats_matches': 'matches', 
        
    #shooting
    'shooting_ranker': 'ranker',
    'shooting_player': 'jugador',
    'shooting_nationality': 'nacionalidad',
    'shooting_position': 'posicion',
    'shooting_team': 'equipo',
    'shooting_comp_level': 'competicion',
    'shooting_age': 'edad',
    'shooting_birth_year':'año',
    'shooting_minutes_90s': 'minutos jugados/90',
    'shooting_matches': 'matches',

    #passing

    'passing_ranker': 'ranker',
    'passing_player':'jugador',
    'passing_nationality':'nacionalidad',
    'passing_position':'posicion',
    'passing_team':'equipo',
    'passing_comp_level': 'competicion',
    'passing_age': 'edad',
    'passing_birth_year': 'año',
    'passing_minutes_90s': 'minutos jugados/90',
    'passing_matches': 'matches',

    #passingtype
    'passing_types_ranker': 'ranker', 
    'passing_types_player': 'jugador',
    'passing_types_nationality': 'nacionalidad',
    'passing_types_position': 'posicion',
    'passing_types_team': 'equipo',
    'passing_types_comp_level': 'competicion',
    'passing_types_age': 'edad',
    'passing_types_birth_year': 'año',
    'passing_types_minutes_90s':'minutos jugados/90',
    'passing_types_matches': 'matches',

    #gca
    'gca_ranker': 'ranker',
    'gca_player': 'jugador',
    'gca_nationality': 'nacionalidad',
    'gca_position': 'posicion',
    'gca_team': 'equipo',
    'gca_comp_level': 'competicion',
    'gca_age': 'edad',
    'gca_birth_year': 'año',
    'gca_minutes_90s': 'minutos jugados/90',
    'gca_matches': 'matches', 
    

    #defensive
    'defense_ranker': 'ranker',
    'defense_player': 'jugador',
    'defense_nationality':'nacionalidad',
    'defense_position': 'posicion',
    'defense_team': 'equipo',
    'defense_comp_level': 'competicion',
    'defense_age': 'edad',
    'defense_birth_year': 'año',
    'defense_minutes_90s': 'minutos jugados/90',
    'defense_matches': 'matches', 

    #possession
    'possession_ranker': 'ranker', 
    'possession_player': 'jugador',
    'possession_nationality': 'nacionalidad',
    'possession_position':'posicion',
    'possession_team': 'equipo',
    'possession_comp_level': 'competicion',
    'possession_age': 'edad',
    'possession_birth_year':'año',
    'possession_minutes_90s': 'minutos jugados/90',
    'possession_matches': 'matches',
    
    #misc
    'misc_ranker':'ranker', 
    'misc_player': 'jugador',
    'misc_nationality': 'nacionalidad',
    'misc_position': 'posicion',
    'misc_team': 'equipo',
    'misc_comp_level': 'competicion',
    'misc_age': 'edad',
    'misc_birth_year': 'año',
    'misc_minutes_90s': 'minutos jugados/90',
    'misc_matches': 'matches', 

    #playingtime
    'playingtime_ranker': 'ranker', 
    'playingtime_player': 'jugador',
    'playingtime_nationality':'nacionalidad',
    'playingtime_position': 'posicion',
    'playingtime_team': 'equipo',
    'playingtime_comp_level': 'competicion',
    'playingtime_age': 'edad',
    'playingtime_birth_year': 'año',
    'playingtime_playingtime_minutes': 'minutos jugados',
    'playingtime_playingtime_minutes_90s': 'minutos jugados/90',
    'playingtime_matches': 'matches'

    }

    df.columns = [mapeo_columns[col] if col in mapeo_columns else col for col in df.columns]

    if 'nacionalidad' in df.columns:
        # Extraer la Nacionalidad	 de la columna 'Nacionalidad	'
        df["nacionalidad"] = df["nacionalidad"].astype(str).str.extract(r'([A-Z]+)$')
    if "edad" in df.columns:
    # Extraer la edad de la columna 'Edad' y convertirla a string
        df["edad"] = df["edad"].astype(str).str.split('-').str[0]
    if "competicion" in df.columns:
        # Extraer la competición de la columna 'Competicion'
        df["competicion"] = df["competicion"].str.replace(r'^[a-z]+', '', regex=True)
    
    if "minutos jugados" in df.columns:
        df['minutos jugados'] = (df['minutos jugados'].astype(str).str.replace(',', '', regex=False).str.extract(r'(\d+)').fillna(0).astype(int))
    
    df = df.drop(['ranker', 'matches'], axis=1)

    columnas_excluir = ['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'año', 'player_url']

    # Identificamos las columnas a convertir (todas menos las excluidas)
    columnas_convertir = [col for col in df.columns if col not in columnas_excluir]

    # Convertimos a numérico (inplace si quieres evitar crear otra variable)
    df[columnas_convertir] = df[columnas_convertir].apply(pd.to_numeric, errors='coerce')

    df[columnas_convertir] = df[columnas_convertir].fillna(0)

    df =df[df['posicion'].str.contains('DF', na=False)].reset_index(drop=True)
    
    return df


#------------------------FUNCIÓN PARA FILTRAR JUGADORES QUE HAYAN JUGADO +0 PARTIDOS PARA EVITAR SESGO------------------------------

def limpiar_playingtime_min_un_partido(df):

    df = df[df['playingtime_playingtime_games']>0].reset_index(drop=True)

    return df

#------------------------FUNCIÓN PARA UNIR TODAS LAS ESTADÍSTICAS DE LOS JUGADORES EN UN DATAFRAME----------------------------------
def union_dataframes(dfs):
    
    # Unión progresiva por jugador
    df_final = reduce(lambda left, right: pd.merge(left, right, on=['jugador', 'equipo', 'posicion'], how='outer'), dfs)
    df_final = df_final[df_final['minutos jugados/90'] > 0].reset_index(drop=True)
    
    return df_final


#------------------------------------------------------FUNCIÓN PARA LA CONVERSION DE DATOS A 90'--------------------------------------
def conversion_columnas90(df, df_final_columns):

    #Detectar columnas porcentuales (no se tocan)

    porcentuales = [col for col in df_final_columns if 'pct' in col.lower() or '_pct' in col.lower() or 'porcentaje' in col.lower()]

    # Columnas ya por 90 (tampoco se tocan)

    ya_por90 = [col for col in df_final_columns if '/90' in col or '_per90' in col]

    # Columnas que sí se deben convertir

    acumulativas = [col for col in df_final_columns if col not in porcentuales + ya_por90 + 
                    ['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'edad', 'año', 
                    'minutos jugados', 'minutos jugados/90', 'playingtime_teamsuccess_points_per_game']]

    # Crear nuevas columnas por90 solo para las acumulativas

    for col in acumulativas:
        df[col] = df.apply(lambda row: row[col] if row['minutos jugados/90'] == 0 
                                       else round(row[col] / row['minutos jugados/90'],2), axis=1)
        
    return df


#------------------------------------FUNCIÓN PARA FILTRAR EL DATAFRAME UNIDO POR LA METRICA MINUTOS JUGADOS/90--------------------------

def filtro_jugadores_minutosjugados90(df):

    df_reducido_final= df[df['minutos jugados/90']>=20].reset_index(drop=True)
    
    return df_reducido_final