from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cdist


#------------------------------------------------FUNCION PARA DEFINIR RANGOS DE EDAD----------------------------------------------------
def clasificar_edad(edad):
    if edad < 23:
        return 'joven'
    elif 23 <= edad <= 28:
        return 'intermedio'
    else:
        return 'veterano'
    

#-------------------------FUNCIÓN PARA OBTENER TOP 10 JUGADORES SIMILARES UTILIZANDO COSINE SIMILARITY-------------------------------------

def top_similares_cosine_similarity_separado(df, grupo, vector_objetivo, jugador_objetivo, n=10):
    
    df_grupo = df[df['grupo_edad'] == grupo].copy()
    
    cols_metricas = df_grupo.drop(columns=['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'año', 'grupo_edad']).columns
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_grupo[cols_metricas])
    
    vector_objetivo_scaled = scaler.transform(vector_objetivo)
    
    similitudes = cosine_similarity(X_scaled, vector_objetivo_scaled).flatten()
    
    df_grupo['cosine_similitud'] = similitudes
    
    # Excluir jugador objetivo
    df_grupo = df_grupo[df_grupo['jugador'] != jugador_objetivo]
    
    top_n = df_grupo.sort_values(by='cosine_similitud', ascending=False).head(n)
    
    return top_n[['jugador', 'edad', 'equipo', 'cosine_similitud']]



def top_similares_distancia_eucludian_separado(df, grupo, vector_objetivo, metric='euclidean', n=10, min_minutos_90=20):
    # Filtrar por grupo edad y minutos jugados/90
    df_grupo = df[(df['grupo_edad'] == grupo) & (df['minutos jugados/90'] >= min_minutos_90)].copy()
    
    # Excluir jugador objetivo para no salir en resultados
    df_grupo = df_grupo[df_grupo['jugador'] != 'Iñigo Martínez']
    
    # Columnas numéricas (métricas)
    cols_metricas = df_grupo.drop(columns=['jugador', 'nacionalidad', 'posicion', 'equipo', 'competicion', 'año', 'grupo_edad']).columns
    
    # Escalado
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_grupo[cols_metricas])
    vector_objetivo_scaled = scaler.transform(vector_objetivo)
    
    # Calcular distancias entre cada jugador y vector objetivo
    distancias = cdist(X_scaled, vector_objetivo_scaled, metric=metric).flatten()
    
    df_grupo['distancia_euclidean'] = distancias
    
    # Ordenar por menor distancia y coger top n
    top_n = df_grupo.sort_values(by='distancia_euclidean').head(n)
    
    return top_n[['jugador', 'edad', 'equipo', 'distancia_euclidean']]
