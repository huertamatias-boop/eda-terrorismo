**Fuente:** GTD, START – Universidad de Maryland, https://www.start.umd.edu/gtd/. 

**Cada fila** = un evento. Se usa el conjunto completo. Columnas usadas: `iyear, region_txt, country_txt, attacktype1_txt, weaptype1_txt, nkill, nwound` (+ `eventid` solo para detectar duplicados).

**Requisitos:** Python 3.11+ y `pip install -r requirements.txt`

**Ejecución**
1. `python analisis_exploratorio.py`

**Genera:** `resultados/tablas/` (8 CSV), `resultados/figuras/` (6 PNG) y `datos/gtd_procesado.csv`.

**Limpieza:** se parte del código base del equipo (7 columnas, `fillna(0)` en `nkill`/`nwound` );Se eliminan solo duplicados por `eventid`; los valores extremos se conservan. Detalle en `resultados/tablas/03_registro_limpieza.csv`.

**Preguntas:** P1 distribución de `nkill`; P2 diferencias por región y tipo de ataque; P3 relación `nkill`–`nwound` (Spearman, sin causalidad); P4 evolución anual; P5 concentración de fallecidos en el 1 % de eventos más letales.
