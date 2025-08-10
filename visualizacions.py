import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os
import matplotlib.patches as mpatches


METRICAS_BARCELONA = {
    
        'passing_total_passes_pct': '% Pases completados',
        'passing_progressive_passes': 'Pases progresivos/90',
        'passing_passes_into_final_third': 'Pases último tercio/90',
        'passing_long_passes_pct_long': '% Pases largos completados',
        'passing_expected_pass_xa': 'Asistencias Esperadas/90',
        'possession_carries_progressive_carries': 'Conducciones progresivas/90',
        'possession_carries_carries_into_final_third': 'Conducciones último tercio/90' ,
        'gca_gcatypes_gca_passes_live':'Acciones creadoras de gols (Pases vivos)/90',
        'passing_types_passtypes_passes_switches': 'Pases: cambios orientacion/90',

        'defense_tackles_tackles_won': 'Entradas ganadas/90',
        'defense_challenges_challenge_tackles_pct': '% Duelos ganados',
        'defense_interceptions': 'Intercepciones/90',
        'defense_blocks_blocked_shots': 'Tiros bloqueados/90',
        'misc_aerialduels_aerials_won_pct': '% Duelos aéreos ganados',
        'defense_clearances': 'Despejes/90',
        'defense_errors': 'Errores/90',
        'misc_performance_fouls': 'Faltas cometidas/90',
 
    
        'possession_touches_touches_def_3rd': 'Toques tercio defensivo/90',
        'possession_carries_carries': 'Total conducciones/90',
        'possession_carries_carries_distance': 'Distancia total conducciones/90',
        'minutos jugados/90': 'Minutos jugados/90',
        'playingtime_teamsuccess_points_per_game': 'Puntos por partido'    
}

METRICAS_DESTACADAS_INIGO = {
    'minutos jugados/90': 'Minutos jugados/90',
    'passing_total_passes_pct': '% Pases completados',
    'passing_passes_into_final_third': 'Pases último tercio/90',
    'passing_long_passes_pct_long': '% Pases largos completados',
    'passing_types_passtypes_passes_switches': 'Pases: cambios orientación/90',
    'defense_challenges_challenge_tackles_pct': '% Duelos ganados',
    'defense_errors': 'Errores/90',
    'possession_carries_carries_distance': 'Distancia conducciones/90',
    'playingtime_teamsuccess_points_per_game': 'Puntos por partido',
    'misc_aerialduels_aerials_won_pct': '% Duelos aéreos ganados'
}

def plot_comparative_bars(df, players, colors, metricas_barca, output_dir, bar_height=0.9):
    """
    Genera gráficos comparativos de métricas para jugadores y guarda las imágenes.

    Parámetros:
    - df: DataFrame con los datos de los jugadores.
    - players: lista con nombres de jugadores a comparar (el segundo será el 'jugador similar').
    - colors: lista de colores para las barras (debe coincidir con el orden de players).
    - metricas_barca: dict con clave = nombre columna métrica, valor = etiqueta para gráfico.
    - output_dir: carpeta donde se guardarán las imágenes.
    - bar_height: altura de las barras (opcional).
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for metric, metric_label in metricas_barca.items():
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Obtener valores para cada jugador
        values = []
        for player in players:
            val = df.loc[df['jugador'] == player, metric].values
            values.append(val[0] if len(val) > 0 else np.nan)
        
        # Grupo de edad del jugador similar (segundo en la lista)
        jugador_similar = players[1]
        grupo_similar = df.loc[df['jugador'] == jugador_similar, 'grupo_edad'].values[0]
        
        # Métricas del grupo similar
        metric_values = df.loc[df['grupo_edad'] == grupo_similar, metric].dropna()
        mins = metric_values.min()
        maxs = metric_values.max()
        mean = round(metric_values.mean(), 2)
        
        y_pos = np.arange(len(players))
        heights = [v - mins for v in values]
        
        # Barra rango gris
        for i, y in enumerate(y_pos):
            ax.barh(y, maxs - mins, left=mins, height=bar_height, 
                    color='lightgray', edgecolor='gray',
                    label='Rangos (min-max) del grupo' if i == 0 else "")
        
        # Barras valores jugadores
        for i, (y, h, val) in enumerate(zip(y_pos, heights, values)):
            ax.barh(y, h, left=mins, height=bar_height, color=colors[i],
                    label=players[i] if i == 0 else "")
            ax.text(mins + h + 0.01*(maxs - mins), y, f'{val:.2f}', va='center', fontsize=9,
                    fontweight='bold', color='black',
                    bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.3'))
        
        # Línea promedio
        ax.axvline(mean, color='red', linestyle='dashed', label=f'Promedio {grupo_similar}')
        
        # Etiquetas y título
        ax.set_yticks(y_pos)
        ax.set_yticklabels(players)
        ax.set_title(f"{metric_label} (Promedio: {mean})")
        
        # Ocultar ejes y mostrar min/max abajo
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.text(mins, -0.5, f"Min: {mins:.2f}", ha='left', va='center', fontsize=9, fontweight='bold')
        ax.text(maxs, -0.5, f"Max: {maxs:.2f}", ha='left', va='center', fontsize=9, fontweight='bold')
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        plt.tight_layout(rect=[1, 0, 0.85, 1])
        
        # Limpiar nombres para archivo
        metric_label_clean = re.sub(r'[^\w\-_]', '_', metric_label)
        jugador_similar_clean = re.sub(r'[^\w\-_]', '_', jugador_similar)
        filename = f"{metric_label_clean}_{jugador_similar_clean}.png"
        filepath = os.path.join(output_dir, filename)
        
        plt.savefig(filepath, transparent=True, bbox_inches='tight', dpi=300)
        plt.close()

def ranking_metricas_jugador(df, jugador_nombre, metricas_dict):
    """
    Calcula en qué posición del ranking (dentro de su grupo de edad) está el jugador
    para cada métrica en metricas_dict.
    
    Retorna un DataFrame con: 
    ['Métrica', 'Valor jugador', 'Posición en ranking', 'Total jugadores en grupo']
    """

    # 1. Localizar jugador
    jugador_row = df[df['jugador'] == jugador_nombre].iloc[0]
    grupo = jugador_row['grupo_edad']

    # 2. Filtrar solo jugadores del mismo grupo
    df_grupo = df[df['grupo_edad'] == grupo]

    resultados = []
    
    for col, nombre_legible in metricas_dict.items():
        # Ordenar desc si la métrica "más alto es mejor"
        # (aquí suponemos que todas menos 'defense_errors' y 'misc_performance_fouls'
        #  son "más es mejor")
        if col in ['defense_errors', 'misc_performance_fouls']:
            df_ordenado = df_grupo.sort_values(by=col, ascending=True)
        else:
            df_ordenado = df_grupo.sort_values(by=col, ascending=False)

        # Calcular ranking
        ranking_pos = df_ordenado.reset_index().index[df_ordenado['jugador'] == jugador_nombre][0] + 1
        total_jugadores = df_ordenado.shape[0]

        resultados.append({
            'Métrica': nombre_legible,
            'Valor jugador': jugador_row[col],
            'Posición en ranking': ranking_pos,
            'Total en grupo': total_jugadores
        })

    return pd.DataFrame(resultados)

def creaciondataframe_metricas_destacadas(df):
    # Ordenar para que salgan primero las mejores posiciones
    ranking_inigo_destacadas = df.sort_values(by='Posición en ranking').reset_index(drop=True)
    
    ranking_inigo_destacadas['Ranking'] = ranking_inigo_destacadas['Posición en ranking'].astype(str) + "º de " + ranking_inigo_destacadas['Total en grupo'].astype(str)
    tabla_final = ranking_inigo_destacadas[['Métrica', 'Valor jugador','Posición en ranking', 'Total en grupo', 'Ranking']]
    
    # Función para asignar color según ranking
    def color_por_ranking(rank):
        if rank <= 3:
            return "#FFD700"  # Oro
        elif rank <= 10:
            return "#C0C0C0"  # Plata
        else:
            return "#2F2F2F"  # Gris


    # Añadir columna de color
    tabla_final["Color"] = tabla_final["Posición en ranking"].apply(color_por_ranking)

    return tabla_final

def plot_ranking_progress(tabla_final, output_path=None, figsize=(8,5), title=None):
    """
    Grafica barras horizontales de progreso de ranking dentro de un grupo.

    Parámetros:
    - tabla_final: DataFrame con columnas 'Métrica', 'Total en grupo', 'Posición en ranking' y 'Color'.
      Se asume que las columnas están en ese orden o que tiene atributos accesibles con nombres correctos.
    - output_path: ruta para guardar la imagen (opcional). Si no se pasa, no guarda.
    - figsize: tamaño del gráfico (tupla).
    - title: título del gráfico (opcional).
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for i, row in enumerate(tabla_final.itertuples()):
        total = row._4  # Total en grupo (columna 4)
        posicion = row._3  # Posición en ranking (columna 3)
        color = row.Color
        metrica = row.Métrica

        relleno = total - posicion + 1  # Barra llena para mejor posición (1º)

        ax.barh(metrica, total, color="#E0E0E0")  # Barra fondo
        ax.barh(metrica, relleno, color=color)   # Barra progreso

        ax.text(total + 2, i, f"{posicion}º de {total}", va="center", fontsize=9, fontweight="bold")

    ax.set_xlim(0, tabla_final["Total en grupo"].max() + 10)
    ax.set_xlabel("Ranking dentro de su grupo de edad (1º = mejor)")
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Quitar bordes y ticks
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False)

    ax.invert_yaxis()
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, transparent=True, dpi=300)
    plt.show()