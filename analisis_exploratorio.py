import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # permite guardar gráficos sin abrir ventanas
import matplotlib.pyplot as plt

# Carpetas de salida (rutas relativas)
os.makedirs("resultados/tablas", exist_ok=True)
os.makedirs("resultados/figuras", exist_ok=True)

# 1. Cargar el dataset
print("Cargando el dataset")
df_completo = pd.read_csv("datos/globalterrorismdb_0718dist.csv", encoding="latin1", low_memory=False)

# 2. Seleccionar SOLO las 7 columnas que nos interesan para el EDA
columnas_clave = [
    'iyear',           # Año del ataque (Temporal)
    'region_txt',      # Región del mundo (Categórica)
    'country_txt',     # País (Categórica)
    'attacktype1_txt', # Tipo de ataque (Categórica)
    'weaptype1_txt',   # Tipo de arma usada (Categórica)
    'nkill',           # Cantidad de muertos (Numérica)
    'nwound'           # Cantidad de heridos (Numérica)
]

# Creamos un nuevo DataFrame solo con estas columnas para liberar memoria
df_limpio = df_completo[columnas_clave].copy()

# 3. Limpieza de Valores Nulos (NaN)
df_limpio['nkill'] = df_limpio['nkill'].fillna(0)
df_limpio['nwound'] = df_limpio['nwound'].fillna(0)

# 4. Verificación
print("\n--- RESUMEN DE LA LIMPIEZA ---")
print(f"Total de registros finales: {df_limpio.shape[0]:,}")
print(f"Total de columnas retenidas: {df_limpio.shape[1]}")
print("\nVerificación de valores nulos:")
print(df_limpio.isnull().sum())

print("\n--- PRIMERAS 5 FILAS DEL DATASET LIMPIO ---")
print(df_limpio.head())


# 5. Calidad de los datos 
registros_entrada = len(df_completo)
if registros_entrada < 50000:
    print("ERROR: el dataset tiene menos de 50.000 registros")

nulos_nkill = df_completo["nkill"].isnull().sum() #numero de muertos
nulos_nwound = df_completo["nwound"].isnull().sum() #numero de heridos 
duplicados_id = df_completo.duplicated(subset="eventid").sum()# mismo evento repetido
 
print("\nCALIDAD")
print("Registros de entrada:", registros_entrada)
print("Nulos en nkill:", nulos_nkill, "| Nulos en nwound:", nulos_nwound)
print("Duplicados por eventid:", duplicados_id)

# Si hubiera eventos repetidos, se eliminan
df_limpio = df_limpio[df_completo["eventid"].duplicated() == False]

# Registro de limpieza
registro = pd.DataFrame({
    "paso": ["Registros de entrada", "Duplicados por eventid eliminados", "Nulos de nkill rellenados con 0",
             "Nulos de nwound rellenados con 0", "Registros finales"],
    "cantidad": [registros_entrada, duplicados_id, nulos_nkill, nulos_nwound, len(df_limpio)]})
print(registro)

# 6. Estadística descriptiva
print("\nESTADÍSTICA DESCRIPTIVA") #la mediana 
descriptiva = df_limpio[["nkill", "nwound"]].describe()
print(descriptiva)
print("Mediana nkill:", df_limpio["nkill"].median(), "| Mediana nwound:", df_limpio["nwound"].median())

# Frecuencias y porcentajes de una variable categórica
frecuencia_region = df_limpio["region_txt"].value_counts() #cuenta las veces que sale aquella region en eventos
porcentaje_region = df_limpio["region_txt"].value_counts(normalize=True) * 100 #calcula la frecuencia relativa y se multiplica por 100 para convertirlas en %
print(frecuencia_region) #conteo por region 
print(porcentaje_region.round(2)) #redondea % en 2 decimales

# Comparación entre grupos
muertos_por_region = df_limpio.groupby("region_txt")["nkill"].mean().sort_values() #de menor a mayor promedio (muertos por region)
muertos_por_ataque = df_limpio.groupby("attacktype1_txt")["nkill"].mean().sort_values()  #de menor a mayor promedio (muertos por ataque)
print(muertos_por_region.round(2))
print(muertos_por_ataque.round(2))

# Evolución en el tiempo
eventos_por_anio = df_limpio.groupby("iyear")["nkill"].count() #evento con muerto, sacando la cantidad de eventos por año
muertos_por_anio = df_limpio.groupby("iyear")["nkill"].sum()#cuanta la cantidad de muertos por año

# Valores extremos: los 10 eventos con más muertos
extremos = df_limpio.sort_values("nkill", ascending=False).head(10) #muestra los 10 eventos mas mortales de forma descendiente
print(extremos)

# Correlación 
correlacion = df_limpio["nkill"].corr(df_limpio["nwound"], method="spearman") #relacion y/o tendencia entre muertos y heridos (1: siempre van juntos, 0: no hay relacion, -1: relacion inversa)
print("Correlación de Spearman entre nkill y nwound:", round(correlacion, 3))

# 7. Gráficos
# Gráfico 1: distribución de muertos 
plt.figure(figsize=(9, 5))
plt.hist(np.log10(df_limpio["nkill"] + 1), bins=40, color="steelblue")
plt.title("Fig. 1. Distribución de muertos por evento (escala log)")
plt.xlabel("log10(muertos + 1) [personas]")
plt.ylabel("Número de eventos")
plt.savefig("resultados/figuras/fig1_distribucion_muertos.png", dpi=150)
plt.close()

# Gráfico 2: valores extremos
plt.figure(figsize=(6, 6))
plt.boxplot(np.log10(df_limpio["nkill"] + 1))
plt.title("Fig. 2. Muertos por evento: valores extremos")
plt.ylabel("log10(muertos + 1) [personas]")
plt.savefig("resultados/figuras/fig2_valores_extremos.png", dpi=150)
plt.close()

# Gráfico 3: frecuencias, 10 países con más eventos
top_paises = df_limpio["country_txt"].value_counts().head(10).sort_values()
plt.figure(figsize=(9, 5))
plt.barh(top_paises.index, top_paises.values, color="steelblue")
plt.title("Fig. 3. Los 10 países con más eventos")
plt.xlabel("Número de eventos")
plt.ylabel("País")
plt.tight_layout()
plt.savefig("resultados/figuras/fig3_top10_paises.png", dpi=150)
plt.close()

# Gráfico 4: comparación entre grupos, promedio de muertos por región
plt.figure(figsize=(10, 6))
plt.barh(muertos_por_region.index, muertos_por_region.values, color="steelblue")
plt.title("Fig. 4. Promedio de muertos por evento según región")
plt.xlabel("Muertos por evento (promedio) [personas]")
plt.ylabel("Región")
plt.tight_layout()
plt.savefig("resultados/figuras/fig4_muertos_por_region.png", dpi=150)
plt.close()

# Gráfico 5: evolución en el tiempo
plt.figure(figsize=(10, 5))
plt.plot(eventos_por_anio.index, eventos_por_anio.values, color="steelblue")
plt.title("Fig. 5. Número de eventos por año")
plt.xlabel("Año")
plt.ylabel("Número de eventos")
plt.savefig("resultados/figuras/fig5_eventos_por_anio.png", dpi=150)
plt.close()

# Gráfico 6: relación muertos vs heridos
muestra = df_limpio.sample(5000, random_state=42)
plt.figure(figsize=(8, 6))
plt.scatter(muestra["nkill"], muestra["nwound"], alpha=0.3, color="steelblue")
plt.title(f"Fig. 6. Muertos vs heridos (muestra de 5.000 eventos, Spearman = {correlacion:.2f})")
plt.xlabel("Muertos [personas]")
plt.ylabel("Heridos [personas]")
plt.savefig("resultados/figuras/fig6_muertos_vs_heridos.png", dpi=150)
plt.close()

# 8. Guardar resultados
calidad = df_completo[columnas_clave].isnull().sum()
calidad.to_csv("resultados/tablas/01_nulos_originales.csv")
registro.to_csv("resultados/tablas/02_registro_limpieza.csv", index=False)
descriptiva.to_csv("resultados/tablas/03_descriptiva.csv")
frecuencia_region.to_csv("resultados/tablas/04_frecuencia_region.csv")
muertos_por_region.to_csv("resultados/tablas/05_muertos_por_region.csv")
muertos_por_ataque.to_csv("resultados/tablas/06_muertos_por_tipo_ataque.csv")
muertos_por_anio.to_csv("resultados/tablas/07_muertos_por_anio.csv")
extremos.to_csv("resultados/tablas/08_top10_extremos.csv")
df_limpio.to_csv("datos/gtd_procesado.csv", index=False)
print("\nListo, resultados estarian guardados en sus respectivos apartados (tabla, grafico)")
