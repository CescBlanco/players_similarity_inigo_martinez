from scrapeo_fbref import *


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


