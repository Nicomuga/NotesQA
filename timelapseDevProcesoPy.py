import pandas as pd
#from datetime import datetime
import matplotlib.pyplot as plt

# Ruta del archivo CSV
file_path = "timelapseDevolucionAProceso/timelapseDevProceso.csv"

# Leer el archivo CSV en un DataFrame
df = pd.read_csv(file_path)

# Realizar las operaciones necesarias con el DataFrame
# ...



df['fecha_recepcion'] = pd.to_datetime(df['fecha_recepcion'])

#normaliza el horario a horario chileno
df['fecha_recepcion_adjusted'] = df['fecha_recepcion'] - pd.Timedelta(hours=4)

#ajusta la fecha acorde al contrato. Despues de las 5 corresponde al día siguiente, si es viernes despues de 5 es lunes
df['contract_date'] = df['fecha_recepcion_adjusted']
df.loc[df['contract_date'].dt.hour >= 17, 'contract_date'] += pd.Timedelta(days=1)
df.loc[df['contract_date'].dt.dayofweek == 5, 'contract_date'] += pd.Timedelta(days=2)

df['contract_date'] = df['contract_date'].dt.date

df['estado_final_lm'].fillna(0, inplace=True)

#date_to_compare = datetime.strptime('2024-05-22', '%Y-%m-%d').date()

#df2 = df[df['contract_date'].isin(df_after_may_22['contract_date'])]

grouped_df = df.groupby('contract_date')['estado_final_lm'].value_counts().unstack().fillna(0)

grouped_df_complete = df.groupby('contract_date')['estado_final_lm'].value_counts().unstack().fillna(0)

grouped_df_complete['total'] = grouped_df_complete.sum(axis=1)

# Calculamos la fila total sumando cada columna del DataFrame
total_row = grouped_df_complete.sum(axis=0)

# Añadimos la fila total al final del DataFrame
grouped_df_complete.loc['total'] = total_row

print(grouped_df_complete)

# Plot the graph
grouped_df.plot(kind='line', figsize=(10, 6))
plt.xlabel('Contract Date')
plt.xticks(rotation='vertical')
plt.ylabel('Count')
plt.title('Evolution of Estado Final LM')
plt.legend(title='Estado Final LM')
plt.show()
