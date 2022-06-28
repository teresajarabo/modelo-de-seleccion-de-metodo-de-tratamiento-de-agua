import pandas as pd

df = pd.read_csv('model_data.csv') # Base de datos
df_fuente = pd.read_csv('fuente_agua.csv')
df_suelos = pd.read_csv('uso_suelos.csv')
df_color_sabor = pd.read_csv('color_sabor.csv')
df_pH = pd.read_csv('pH_agua.csv')

# Drop down menu -> No hay opción de equivocarse
input_elec = input('¿Hay electricidad disponible? (Y o N) ')
input_red = input('¿Existe una red de distribución? (Y o N) ')
input_uso_edificio = input('¿El edificio es de uso individual (I) o colectivo (C)? ')
input_usuarios = int(input('¿Cuál es el número usual de usuarios?' ))
caudal = input_usuarios * 4

# Preguntas relacionadas con la calidad:
# Usar drop down menu -> cómo??
# Incluir: 'De las siguientes opciones, escoja la que más se ajuste: '
input_fuente = input('Escoja la fuente de agua: ')
input_uso_suelos = input('Escoja los usos de suelo cercano: ') ## Más de una opción
input_color_sabor = input('¿El agua tiene un color o sabor particular? ') ## Más de una opción
input_pH = int(input('¿Cuál es el pH del agua? '))
if input_pH < 6.5:
    pH_agua = 'Acido'
elif input_pH > 8.5:
    pH_agua = 'Basico'
else:
    pH_agua = 'Neutro'


# Función para buscar la calidad del agua
## ¿Dar la opción de escoger más de una?
def calcular_calidad(fuente, suelos, color_sabor, pH):
    # Calidad microbiológica -> obtengo tablas de una fila
    new_df_fuente = df_fuente.loc[df_fuente['Nombre'] == fuente]
    new_df_suelos = df_suelos.loc[df_suelos['Nombre'] == suelos]
    new_df_color_sabor = df_color_sabor.loc[df_color_sabor['Nombre'] == color_sabor]
    new_df_pH = df_pH.loc[df_pH['Nombre'] == pH]

    # microb está en la columna 3
    microb = max(new_df_fuente.iloc[-1, 2], new_df_suelos.iloc[-1, 2], new_df_color_sabor.iloc[-1, 2], new_df_pH.iloc[-1, 2])
    #microb = max(int(new_df_fuente.iloc[1, 2]), int(new_df_suelos.iloc[1, 2]), int(new_df_color_sabor.iloc[1, 2]), int(new_df_pH.iloc[1, 2]))
    ## microb = max(new_df_fuente.iloc[1, 2], new_df_suelos.iloc[1:, 2], new_df_color_sabor.iloc[1:, 2], new_df_pH.iloc[1, 2])
    # quimic está en la columna 4
    quimic = max(new_df_fuente.iloc[-1, 3], new_df_suelos.iloc[-1, 3], new_df_color_sabor.iloc[-1, 3], new_df_pH.iloc[-1, 3])
    ## quimic = max(new_df_fuente.iloc[1, 3], new_df_suelos.iloc[1:, 3], new_df_color_sabor.iloc[1:, 3], new_df_pH.iloc[1, 3])
    # turb está en la columna 5
    turb = max(new_df_fuente.iloc[-1, -1], new_df_suelos.iloc[-1, -1], new_df_color_sabor.iloc[-1, -1], new_df_pH.iloc[-1, -1])
    ## turb = max(new_df_fuente.iloc[1, 4], new_df_suelos.iloc[1:, 4], new_df_color_sabor.iloc[1:, 4], new_df_pH.iloc[1, 4])
    
    return [microb, quimic, turb]


calidad = calcular_calidad(input_fuente, input_uso_suelos, input_color_sabor, pH_agua)

# Imprimir el resumen de los parámetros
param_input = [input_elec, input_red, input_uso_edificio, input_usuarios] + calidad
print(param_input)

# Filtrar tabla de datos según los param_input
# 0: No necesita x, Individual
# 1: Necesita x, Colectivo
# 2: Funciona con ambos, Ambos
new_df = df

if input_elec.upper() == 'N':
    # Me quedo solo con los métodos que no usen electricidad o funcionen con ambos
    new_df = new_df.loc[(df['Electricidad'] == 0) | (df['Electricidad'] == 2)]

if input_red.upper() == 'N':
    # Me quedo solo con los mét. que no necesiten red de distribución o funcionen con ambos
    new_df = new_df.loc[(df['Uso de red'] == 0) | (df['Uso de red'] == 2)]

if input_uso_edificio.upper() == 'I':
    new_df = new_df.loc[(df['Uso del edificio'] == 0) | (df['Uso del edificio'] == 2)]
else:
    new_df = new_df.loc[(df['Uso del edificio'] == 1) | (df['Uso del edificio'] == 2)]

new_df = new_df.loc[(new_df['Caudal'] >= caudal) & 
                    (new_df['Calidad microbiologica'] >= calidad[0]) & 
                    (new_df['Calidad quimica'] >= calidad[1]) & 
                    (new_df['Turbiedad'] >= calidad[2])]

# Save in a modified .csv
new_df = new_df.reset_index()
new_df.to_csv('modified.csv', index=False)
new_df

## Filtrar una base de datos de salida que incluye instal, mantenim y precio para que el usuario pueda filtrar
## Incluir la posibilidad de usar varios depósitos o filtros en paralelo... 