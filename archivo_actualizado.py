import pandas as pd
import matplotlib.pyplot as plt
# 1. Cargar el dataset
print("Cargando el dataset masivo... (esto puede tomar unos segundos)")
df_completo = pd.read_csv("globalterrorismdb_0718dist.csv", encoding="latin1", low_memory=False)

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

# --- 3.5 Recorte de Muestra (Sample) ---
# Extraemos exactamente 50.000 datos al azar para cumplir con la pauta
# Usamos random_state=42 para que a tu compañero Nemryz le salgan los mismos 50.000 datos que a ti
df_limpio = df_limpio.sample(n=50000, random_state=42)
print(f"\n--- MUESTRA FINAL PARA EL INFORME: {df_limpio.shape[0]} registros ---")


# 4. Verificación para el informe de la Universidad
print("\n--- RESUMEN DE LA LIMPIEZA ---")
print(f"Total de registros finales: {df_limpio.shape[0]:,}")
print(f"Total de columnas retenidas: {df_limpio.shape[1]}")
print("\nVerificación de valores nulos (Debe dar 0 en todas):")
print(df_limpio.isnull().sum())

print("\n--- PRIMERAS 5 FILAS DEL DATASET LIMPIO ---")
print(df_limpio.head())