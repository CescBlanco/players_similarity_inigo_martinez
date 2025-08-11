
# Players_Similarity_Inigo_Martinez

Este proyecto tiene como objetivo identificar a los jugadores defensivos más similares a Iñigo Martínez en las grandes ligas europeas, facilitando la búsqueda de posibles reemplazos para el Barcelona basándose en métricas avanzadas de rendimiento. Los datos se han extraído mediante web scraping de la página [FBref](https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats), obteniendo diversas estadísticas detalladas de rendimiento. El análisis considera específicamente el estilo de juego actual del Barcelona, tomando en cuenta sus fortalezas y debilidades para seleccionar las métricas más relevantes.

## Descripción

El repositorio implementa un *informe* completo de análisis futbolístico que abarca desde la extracción de datos hasta la visualización de resultados. Inicialmente, se realiza la extracción automática de estadísticas de jugadores defensivos mediante scraping en FBref. Posteriormente, se filtran los jugadores según su posición (defensa) y se seleccionan las métricas clave alineadas con el estilo de juego del Barcelona.

Para asegurar la calidad del análisis y eliminar sesgos, las métricas originales se convierten a valores normalizados por 90 minutos jugados, y se filtran los defensas que hayan disputado un mínimo de 20 minutos por partido en promedio. Esto garantiza que solo se incluyan jugadores con una muestra significativa de juego, mejorando la fiabilidad del estudio.

A partir de estos datos procesados, se aplican modelos de similitud para identificar y rankear a los jugadores más parecidos a Iñigo Martínez en diferentes grupos de edad, facilitando así la toma de decisiones en scouting y sustitución.

## Estructura del proyecto

- **scrapeo_fbref.py**: Contiene funciones y clases para extraer datos estadísticos de FBref mediante web scraping.
- **etl.py**: Incluye funciones para limpiar, transformar y unir los diferentes dataframes de estadísticas.
- **models.py / models_separados.py**: Implementan los modelos de similitud (Cosine Similarity y Euclidean Distance) y el ranking combinado para identificar jugadores similares.
- **visualizacions.py**: Proporciona funciones para visualizar comparativas y rankings de métricas entre jugadores.
- **main.py**: Orquesta el flujo completo: extracción, limpieza, unión, modelado y visualización de resultados.
- **similar_player.ipynb**: Notebook para análisis exploratorio y visualización interactiva (no disponible para el lector)
- **requirements.txt**: Porporciona las dependencias de paquetes necesarios para ejecutar el archivo main.py.
- **README.md**: Este documento.
- **LICENSE**: Licencia MIT.

## Principales funcionalidades

- Extracción automática de estadísticas de jugadores defensivos de las principales ligas europeas.
- Limpieza y transformación de datos para asegurar la calidad del análisis.
- Modelos de similitud para comparar jugadores según métricas seleccionadas.
- Visualización de comparativas y rankings para facilitar la interpretación de resultados.
- Identificación del mejor reemplazo para Iñigo Martínez según criterios objetivos.

## Instalación

1. Clona el repositorio:
	```powershell
	git clone https://github.com/CescBlanco/players_similarity_inigo_martinez.git
	```
2. Instala las dependencias en el entorno virtual `player_venv`:
	```powershell
	.\player_venv\Scripts\activate
	pip install -r requirements.txt
	```
	*(Asegúrate de tener Python 3.11 o superior)*

## Uso

Ejecuta el script principal para realizar el análisis completo:
```powershell
python main.py
```
También puedes contactar conmigo en LinkedIn ([Cesc Blanco](https://www.linkedin.com/in/cescblanco)) para obtener acceso al informe completo y ver los resultados detallados del estudio.



## Resultados

El proyecto genera:
- Listados de los jugadores más similares a Iñigo Martínez, organizados por grupo de edad.
- Visualizaciones comparativas de métricas clave.
- Recomendaciones objetivas para posibles reemplazos.

Todos los resultados obtenidos pueden utilizarse para elaborar un informe final de scouting sobre los candidatos potenciales para sustituir a Iñigo Martínez, en caso de que el club decida realizarlo.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
