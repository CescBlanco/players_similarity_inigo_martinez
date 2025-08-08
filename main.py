from scrapeo_fbref import *
from etl import *


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