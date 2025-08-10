from scrapeo_fbref import *
from etl import *
from models import *
from models_separados import *
from visualizacions import *


#1. EXTRACCIÓN DE LOS DATOS 

#Se llama a la clase, argumento obligatorio de la temporada de interés
fbref = FBrefStatsGroups(temporada='2024-2025')

#Se guarda la tabla scrapeada con una variable significativa según la estadística de interés
df_stats_sucio = fbref.scrape_group("stats")
df_shooting_sucio = fbref.scrape_group("shooting")
df_passing_sucio  = fbref.scrape_group("passing")
df_passingype_sucio  = fbref.scrape_group("passing_types")
df_gca_sucio = fbref.scrape_group("gca")
df_defensive_sucio  = fbref.scrape_group("defense")
df_possession_sucio  = fbref.scrape_group("possession")
df_misc_sucio  = fbref.scrape_group("misc")
df_playingtime_sucio  = fbref.scrape_group("playingtime")





#2. LIMPIEAZA Y TRANSFORMACIÓN DE LOS DATOS 

#Se generan copias para asegurar no tocar los dataframes iniciales

df_stats_gestion= df_stats_sucio.copy()
df_shooting_gestion= df_shooting_sucio.copy()
df_passing_gestion= df_passing_sucio.copy()
df_passingype_gestion= df_passingype_sucio.copy()
df_gca_gestion= df_gca_sucio.copy()
df_defensive_gestion= df_defensive_sucio.copy()
df_possession_gestion= df_possession_sucio.copy()
df_misc_gestion= df_misc_sucio.copy()
df_playingtime_gestion= df_playingtime_sucio.copy()


#Se limpia el dataset y filtramos  a los jugadores que contienen DF EN LA COLUMNA 'POSICION'
df_limpio_stats_defensas= limpiar_filas_estadisticas(df_stats_gestion)
df_limpio_shooting_defensas= limpiar_filas_estadisticas(df_shooting_gestion)
df_limpio_passing_defensas= limpiar_filas_estadisticas(df_passing_gestion)
df_limpio_passingtype_defensas= limpiar_filas_estadisticas(df_passingype_sucio)
df_limpio_gca_defensas= limpiar_filas_estadisticas(df_gca_gestion)
df_limpio_defenisve_defensas= limpiar_filas_estadisticas(df_defensive_gestion)
df_limpio_possession_defensas= limpiar_filas_estadisticas(df_possession_gestion)
df_limpio_misc_defensas= limpiar_filas_estadisticas(df_misc_gestion)
df_limpio_playingtime_defensas= limpiar_filas_estadisticas(df_playingtime_sucio)

df_playingtime_1partido= limpiar_playingtime_min_un_partido(df_limpio_playingtime_defensas)



#-------------------------------------------SE ESCOJEN LAS COLUMNAS DE INTERÉS EN CADA DATAFRAME PARA EL ESTUDIO-----------------------------------

df_stats_interes_def= df_limpio_stats_defensas[['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'edad','año','minutos jugados', 'minutos jugados/90']]


df_passing_interes_def= df_limpio_passing_defensas[['jugador', 'posicion', 'equipo', 'passing_total_passes_pct','passing_progressive_passes','passing_passes_into_final_third',
                                                 'passing_long_passes_pct_long', 'passing_xg_assist','passing_expected_pass_xa']]


df_passingtype_interes_def= df_limpio_passingtype_defensas[['jugador', 'posicion', 'equipo', 'passing_types_passtypes_passes_switches']]



df_gca_interes_def= df_limpio_gca_defensas[['jugador', 'posicion', 'equipo', 'gca_scatypes_sca_passes_live','gca_gcatypes_gca_passes_live']]



df_defensive_interes_def= df_limpio_defenisve_defensas[['jugador', 'posicion', 'equipo', 'defense_tackles_tackles_won','defense_tackles_tackles_def_3rd',
                                                 'defense_tackles_tackles_mid_3rd', 'defense_tackles_tackles_att_3rd', 'defense_challenges_challenge_tackles_pct',
                                                 'defense_interceptions','defense_blocks_blocked_shots', 'defense_blocks_blocked_passes',  'defense_clearances', 'defense_errors']]



df_possession_interes_def= df_limpio_possession_defensas[['jugador', 'posicion', 'equipo', 'possession_carries_progressive_carries','possession_carries_carries_into_final_third',
                                                 'possession_touches_touches_def_3rd', 'possession_carries_carries', 'possession_carries_carries_distance',
                                                 'possession_carries_carries_progressive_distance', 'possession_carries_miscontrols', 'possession_take-ons_take_ons_tackled_pct',
                                                 'possession_carries_dispossessed','possession_receiving_progressive_passes_received']]



df_misc_interes_def= df_limpio_misc_defensas[['jugador', 'posicion', 'equipo', 'misc_performance_fouls','misc_performance_cards_yellow', 'misc_performance_own_goals',
                                                'misc_performance_cards_red', 'misc_performance_ball_recoveries', 'misc_performance_pens_conceded','misc_aerialduels_aerials_won',
                                                'misc_aerialduels_aerials_lost','misc_aerialduels_aerials_won_pct']]



df_playingtime_interes_def= df_playingtime_1partido[['jugador', 'posicion', 'equipo', 'playingtime_playingtime_minutes_pct','playingtime_teamsuccess_points_per_game',
                                                     'playingtime_starts_games_starts']]


#-----------------------------UNIÓN DE LOS DIFERENTES DATAFRAMES-------------------------------------------------------------------------------
# Lista de dataframes ya filtrados por columnas útiles
dfs = [df_stats_interes_def, df_passing_interes_def, df_passingtype_interes_def, 
       df_gca_interes_def, df_defensive_interes_def, df_possession_interes_def, df_misc_interes_def, df_playingtime_interes_def]

df_union_dfs= union_dataframes(dfs)


#----------------------------------------------PROCESO DE CONVERSION DE METRICAS ABSOLUTAS A METRICAS POR 90------------------------------------

#Se cogen todas las columnas del dataframe 
df_final_columns = list(df_union_dfs.columns)

df_final_convertido= conversion_columnas90(df_union_dfs, df_final_columns)


#----------------------------------------------PROCESO DE FILTRO DEL DATAFRAME FINAL-------------------------------------------------

#Filtro del dataframe para obtener el dataframe final de aquellos defensas que han jugado más de 20 minutos jugados/90

df_final_defensas= filtro_jugadores_minutosjugados90(df_final_convertido)


#3. CARGA Y BUSQUEDA DE LOS JUGADORES SIMILARES POR RANGO DE EDAD PARA IÑIGO MARTÏNEZ


#--------------------------DEFINICIÓN DE LAS METRICAS DE INTERÉS DE COMPARACIÓN-----------------------------------------

metricas_interes = ['passing_total_passes_pct','passing_progressive_passes','passing_passes_into_final_third', 'passing_long_passes_pct_long',
                    'passing_xg_assist','passing_expected_pass_xa', 'passing_types_passtypes_passes_switches','gca_scatypes_sca_passes_live',
                    'gca_gcatypes_gca_passes_live','defense_tackles_tackles_won', 'defense_tackles_tackles_def_3rd',
                    'defense_tackles_tackles_mid_3rd', 'defense_tackles_tackles_att_3rd', 'defense_challenges_challenge_tackles_pct',
                    'defense_interceptions', 'defense_blocks_blocked_shots', 'defense_blocks_blocked_passes', 'defense_clearances', 'defense_errors',
                    'possession_carries_progressive_carries', 'possession_carries_carries_into_final_third', 'possession_touches_touches_def_3rd',
                    'possession_carries_carries', 'possession_carries_carries_distance', 'possession_carries_carries_progressive_distance',
                    'possession_carries_miscontrols', 'possession_take-ons_take_ons_tackled_pct', 'possession_carries_dispossessed',
                    'possession_receiving_progressive_passes_received', 'misc_performance_fouls', 'misc_performance_cards_yellow',
                    'misc_performance_own_goals', 'misc_performance_cards_red', 'misc_performance_ball_recoveries', 'misc_performance_pens_conceded',
                    'misc_aerialduels_aerials_won', 'misc_aerialduels_aerials_lost', 'misc_aerialduels_aerials_won_pct',
                    'playingtime_playingtime_minutes_pct', 'playingtime_teamsuccess_points_per_game', 'playingtime_starts_games_starts']







#--------------------------SE FILTRA LA INFORMACIÓN DEL JUGADOR OBJETIVO ------------------------------------------------

jugador_objetivo = df_final_defensas[df_final_defensas['jugador'] == 'Iñigo Martínez'].iloc[0]



#----------------------CLASSIFICAR CADA JUGADOR CON UN GRUPO DE EDAD: JOVENES, INTERMEDIO Y VETERANOS, SE FILTRA SU VECTOR-------------------

df_final_defensas['grupo_edad'] = df_final_defensas['edad'].apply(clasificar_edad)

# Vector de Iñigo (sin filtrar)
vector_inigo = df_final_defensas[df_final_defensas['jugador'] == 'Iñigo Martínez'].drop(columns=['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'año', 'grupo_edad']).values


#---------------------------------------USO DE LA FUNCIÓN PARA OBTENER LOS TOP10 MÁS SIMILARES COSINE SIMILARITY EN CADA GRUPO-------------------------------



top_jovenes_cosine = top_similares_cosine_similarity_separado(df_final_defensas, 'joven', vector_inigo, 'Iñigo Martínez')
top_intermedios_cosine = top_similares_cosine_similarity_separado(df_final_defensas, 'intermedio', vector_inigo, 'Iñigo Martínez')
top_veteranos_cosine = top_similares_cosine_similarity_separado(df_final_defensas, 'veterano', vector_inigo, 'Iñigo Martínez')


#---------------------------------------USO DE LA FUNCIÓN PARA OBTENER LOS TOP10 MÁS SIMILARES DISTANCE EUCLIDEAN EN CADA GRUPO--------

top_jovenes_euclid = top_similares_distancia_eucludian_separado(df_final_defensas, 'joven', vector_inigo, metric='euclidean')
top_intermedios_euclid = top_similares_distancia_eucludian_separado(df_final_defensas, 'intermedio', vector_inigo, metric='euclidean')
top_veteranos_euclid = top_similares_distancia_eucludian_separado(df_final_defensas, 'veterano', vector_inigo, metric='euclidean')


#----------------------------------------------EJECUTAR LA FUNCIÓN RESUMEN--------------------------------------------------
resultados = resumen_similares(df_final_defensas, jugador_objetivo='Iñigo Martínez', min_minutos_90=20, n=10)


#---------------------------PASO FINAL: COMBINACION DE SIMILITUDES Y VISUALIZACION DE RESULTADOS

# Asumiendo que ya tienes top_jovenes (cosine) y top_jovenes_euclid (euclidean)
top_jovenes_combinados = combinar_similitudes(top_jovenes_cosine, top_jovenes_euclid, n=10)
print(top_jovenes_combinados)

top_intermedios_combinados = combinar_similitudes(top_intermedios_cosine, top_intermedios_euclid, n=10)
print('')
print(top_intermedios_combinados)


top_veteranos_combinados = combinar_similitudes(top_veteranos_cosine, top_veteranos_euclid, n=10)
print('')
print(top_veteranos_combinados)

#4. VISUALIZACION DE LOS DATOS DE CADA JUGADOR SIMILAR A IÑIGO


datos_iñigo= df_final_defensas[df_final_defensas['jugador'] == 'Iñigo Martínez'].iloc[0]
print('\nDATOS IÑIGO MARTÍNEZ\n')
print(datos_iñigo)

mejor_joven, stats_joven = obtener_mejor_reemplazo(top_jovenes_combinados, df_final_defensas, 'joven')
mejor_intermedio, stats_intermedio = obtener_mejor_reemplazo(top_intermedios_combinados, df_final_defensas, 'intermedio')
mejor_veterano, stats_veterano = obtener_mejor_reemplazo(top_veteranos_combinados, df_final_defensas, 'veterano')


print('\nDATOS JUGADOR MÁS SIMILAR EN EL GRUPO DE LOS JOVENES\n')
print(stats_joven)

print('\nDATOS JUGADOR MÁS SIMILAR EN EL GRUPO DE LOS LOS INTERMEDIOS\n')
print(stats_intermedio)

print('\nDATOS JUGADOR MÁS SIMILAR EN EL GRUPO DE LOS LOS VETERANOS\n')
print(stats_veterano)


#--------------------------------------------PASO EXTRA: VISUALIZACIONES METRICAS COMPARACION Y RANKINGS--------------------------

#Comparaciones Iñigo con el primer jugador similar: 'Joško Gvardiol' 
players = ['Iñigo Martínez', 'Joško Gvardiol']
colors = ['steelblue', 'green']
output_dir = "graficos_barras_comparativos/gvardiol"

plot_comparative_bars(df_final_defensas, players, colors, METRICAS_BARCELONA, output_dir)


#Comparaciones Iñigo con el segundo jugador similar: 'Joško Gvardiol' 
players = ['Iñigo Martínez', 'Rúben Dias']
colors = ['steelblue', 'orange']
output_dir = "graficos_barras_comparativos/ruben_dias"

plot_comparative_bars(df_final_defensas, players, colors, METRICAS_BARCELONA, output_dir)


#Comparaciones Iñigo con el segundo jugador similar: 'Joško Gvardiol' 
players = ['Iñigo Martínez', 'Daley Blind']
colors = ['steelblue', 'gray']
output_dir = "graficos_barras_comparativos/daley_blind"

plot_comparative_bars(df_final_defensas, players, colors, METRICAS_BARCELONA, output_dir)

#-------------------------------------------------------------------------------------------------------------

#Posición de iñigo en ciertas métricas destacables
ranking_inigo_destacadas = ranking_metricas_jugador(df_final_defensas, 'Iñigo Martínez', METRICAS_DESTACADAS_INIGO)
tabla_final= creaciondataframe_metricas_destacadas(ranking_inigo_destacadas)
print(tabla_final)

plot_ranking_progress(tabla_final, output_path="ranking_inigo_barra_progreso.png",
                      title=None)