from models_separados import *

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cdist


#LO QUE SE VA USAR 100%

#-------------------------FUNCIÓN PARA OBTENER TOP 10 JUGADORES SIMILARES UTILIZANDO COSINE SIMILARITY-------------------------------------
def top_similares_cosine(df, grupo, vector_objetivo, jugador_objetivo, min_minutos_90=20, n=10):
    df_grupo = df[(df['grupo_edad'] == grupo) & (df['minutos jugados/90'] >= min_minutos_90)].copy()
    df_grupo = df_grupo[df_grupo['jugador'] != jugador_objetivo]

    cols_metricas = df_grupo.drop(columns=['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'año', 'grupo_edad']).columns
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_grupo[cols_metricas])
    vector_objetivo_scaled = scaler.transform(vector_objetivo)
    
    similitudes = cosine_similarity(X_scaled, vector_objetivo_scaled).flatten()
    df_grupo['cosine_similitud'] = similitudes
    
    top_n = df_grupo.sort_values(by='cosine_similitud', ascending=False).head(n)
    return top_n[['jugador', 'edad', 'equipo', 'cosine_similitud']]


#-------------------------FUNCIÓN PARA OBTENER TOP 10 JUGADORES SIMILARES UTILIZANDO EUCLIDEAN-------------------------------------

def top_similares_distancia(df, grupo, vector_objetivo, jugador_objetivo, metric='euclidean', min_minutos_90=20, n=10):
    df_grupo = df[(df['grupo_edad'] == grupo) & (df['minutos jugados/90'] >= min_minutos_90)].copy()
    df_grupo = df_grupo[df_grupo['jugador'] != jugador_objetivo]
    
    cols_metricas = df_grupo.drop(columns=['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'año', 'grupo_edad']).columns
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_grupo[cols_metricas])
    vector_objetivo_scaled = scaler.transform(vector_objetivo)
    
    distancias = cdist(X_scaled, vector_objetivo_scaled, metric=metric).flatten()
    df_grupo['distancia_euclidean'] = distancias
    
    top_n = df_grupo.sort_values(by='distancia_euclidean').head(n)
    return top_n[['jugador', 'edad', 'equipo', 'distancia_euclidean']]


#-------------------------FUNCIÓN PARA RESUMEN DE LOS DOS MODELOS Y OBTENCIÓN DE RESULTADOS-------------------------------------

# Función resumen que junta todo y lo muestra limpio
def resumen_similares(df, jugador_objetivo='Iñigo Martínez', min_minutos_90=20, n=10):
    vector_objetivo = df[df['jugador'] == jugador_objetivo].drop(columns=['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'año', 'grupo_edad']).values
    
    grupos = ['joven', 'intermedio', 'veterano']
    
    resultados = {}
    
    for grupo in grupos:
        cosine_res = top_similares_cosine(df, grupo, vector_objetivo, jugador_objetivo, min_minutos_90, n)
        euclid_res = top_similares_distancia(df, grupo, vector_objetivo, jugador_objetivo, 'euclidean', min_minutos_90, n)
        
        resultados[grupo] = {
            'cosine_similarity': cosine_res,
            'euclidean_distance': euclid_res
        }
    
    # Mostrar resultados formateados
    for grupo in grupos:
        print(f"\n--- Grupo {grupo.upper()} ---")
        print("\nTop similares usando Cosine Similarity:")
        print(resultados[grupo]['cosine_similarity'].to_string(index=False))
        
        print("\nTop similares usando Euclidean Distance:")
        print(resultados[grupo]['euclidean_distance'].to_string(index=False))
    
    return resultados





#-------------------------FUNCIÓN PARA COMBINAR MODELOS Y HACER RANKING FINAL Y OBTENCIÓN DE RESULTADOS-------------------------------------

def combinar_similitudes(df_cosine, df_euclid, n=10, peso_cosine=0.5, peso_euclid=0.5):
    """
    Combina similitud coseno y distancia euclidiana en un ranking conjunto.
    
    df_cosine: dataframe con columnas ['jugador', 'similitud']
    df_euclid: dataframe con columnas ['jugador', 'distancia']
    peso_cosine: peso para la similitud coseno (entre 0 y 1)
    peso_euclid: peso para la similitud euclidiana (entre 0 y 1)
    
    Retorna dataframe con jugadores y una columna 'similitud_combinada'
    """
    # Merge por jugador
    df_merge = df_cosine.merge(df_euclid[['jugador', 'distancia_euclidean']], on='jugador')
    
    # Normalizar distancia (MinMax 0-1)
    scaler = MinMaxScaler()
    df_merge['dist_norm'] = scaler.fit_transform(df_merge[['distancia_euclidean']])
    
    # Convertir distancia en similitud (más cercano = más alto)
    df_merge['similitud_dist'] = 1 - df_merge['dist_norm']
    
    # Combinar (ponderado)
    df_merge['similitud_combinada'] = (peso_cosine * df_merge['cosine_similitud']) + (peso_euclid * df_merge['similitud_dist'])
    
    # Ordenar descendente (mayor similitud combinada primero)
    df_merge = df_merge.sort_values(by='similitud_combinada', ascending=False)
    
    # Seleccionar top n
    return df_merge[['jugador', 'edad', 'equipo', 'cosine_similitud', 'distancia_euclidean', 'similitud_combinada']].head(n)




def obtener_mejor_reemplazo(df_resultados, df_original, grupo_nombre):
    """
    Devuelve el jugador con mayor similitud_combinada y sus estadísticas completas del DataFrame original.

    Parámetros:
    - df_resultados: DataFrame con columnas ['jugador', 'similitud', 'distancia', 'similitud_combinada']
    - df_original: DataFrame completo con todas las métricas
    - grupo_nombre: string, nombre del grupo para impresión o tracking

    Retorna:
    - nombre del jugador
    - Serie con sus estadísticas (fila del DataFrame original)
    """
    # Ordenar por similitud_combinada
    mejor_fila = df_resultados.sort_values(by='similitud_combinada', ascending=False).iloc[0]
    mejor_jugador = mejor_fila['jugador']
    mejor_similitud = mejor_fila['similitud_combinada']
    
    # Buscar estadísticas completas
    stats_jugador = df_original[df_original['jugador'] == mejor_jugador].iloc[0]
    
    print(f"\n📌 Mejor reemplazo para el grupo '{grupo_nombre}': {mejor_jugador}, similitud combinada: {mejor_similitud:.3f}\n")
    
    return mejor_jugador, stats_jugador