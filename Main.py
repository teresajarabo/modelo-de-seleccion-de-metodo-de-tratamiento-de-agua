import streamlit as st
import pandas as pd

df = pd.read_csv('model_data.csv') # Base de datos
df_fuente = pd.read_csv('fuente_agua.csv')
df_suelos = pd.read_csv('uso_suelos.csv')
df_color_sabor = pd.read_csv('color_sabor.csv')
df_pH = pd.read_csv('pH_agua.csv')
df_comparativa = pd.read_csv('tabla_comparativa.csv')


# to run use: streamlit run Main.py


header = st.container()
dataset = st.container()
seleccion_input = st.container()
seleccion_modelo = st.container()
ordenar_resultados = st.container()


with header:  # use for the title of the webpage
    st.title('¿Cuál es el método de tratamiento de agua más adecuado?')
    st.markdown('Dados unos parámetros de entrada simples, este modelo de selección obtiene el método de tratamiento de agua más adecuado.')


with dataset:
    st.header('Base de Datos')
    st.markdown('El modelo emplea como base de datos 27 métodos de tratamiento incluidos en la siguiente tabla.')

    st.subheader('Base de datos del modelo de selección')
    #st.write(df.head())
    st.table(df.head().style.format(subset=['Caudal'], formatter="{:.2f}"))
    
    st.caption('El caudal está en litros por minuto')

    st.markdown('Los valores mostrados en la tabla son el resultado del análisis de los distintos métodos de tratamiento.')

    # Para ver la tabla
    with st.expander('Tabla completa'):
        st.table(df.style.format(subset=['Caudal'], formatter="{:.2f}"))


with seleccion_input:
    st.markdown('___')
    st.header('Selección de los parámetros de entrada:')

    # Explicar los parámetros de entrada. ¿Hacer aquí o si se pincha sobre el parámetro?

    st.markdown('Seleccione la opción que mejor se ajuste a su situación.')

    # Drop-down menus
    #sel_col, disp_col = st.columns(2)
    # Electricidad:
    st.subheader('Perfil del usuario')
    st.markdown('* **Electricidad:**')  # incluir después de esto la explicación
    st.markdown('''
    Indique si dispone de electricidad en el punto de tratamiento del agua. 
    Puede venir de la red o de un generador separado (p. ej. placa solar).''')
    input_elec = st.selectbox('¿Hay electricidad disponible?', options=[
                                   'Si', 'No'])
    
    # Red de distribución
    st.markdown('* **Red de distribución:**')
    st.markdown('''
    Se entiende por red de distribución un sistema de tuberías que transporta el agua desde la fuente de agua 
    hasta el punto de tratamiento, o en el propio edificio.''')
    input_red = st.selectbox('¿Existe una red de distribución?', options=[
                                  'Si', 'No'])

    # Uso del edificio
    st.markdown('* **Uso del edificio:**')
    st.markdown('''
    Un edificio es de uso **individual** cuando el agua es tratada en el punto de consumo y es empleada por un solo grupo (p. ej., domicilio, colegio, comunidad). \n
    Un edificio de uso **colectivo** cuenta con un sistema de tratamiento central, y el agua es consumida por distintos 
    grupos de personas (p. ej., domicilio, colegio, hospital, oficina, comunidad).''')
    input_uso_edificio = st.selectbox('¿El edificio es de uso individual o colectivo?', options=[
                                           'Individual', 'Colectivo'])

    # Introducir el número de usuarios
    # chequear si está introduciendo un número entero
    st.markdown('* **Número de usuarios:**')
    st.markdown('''El número de usuarios determina el caudal que se necesita obtener del método de tratamiento. 
    La OMS estima que una persona adulta consume 2 litros de agua al día. Aparte de hidratarse, el ser humano consume
    agua para lavar alimentos, cocinar y la higiene personal.
    Se plantea un consumo mínimo de 4 litros por día por persona. Sin embargo, se da la opción de introducir un consumo por parte del usuario.
    El rango del consumo por persona debe estar entre **4 y 20** litros por persona y por día.''')
    input_usuarios = st.number_input(
        '¿Cuál es el número usual de usuarios?', min_value=0, max_value=100000)
    consumo_agua = st.slider('Introduzca el consumo de agua requerido (L/día):', min_value=4, max_value=20, value=4)
    caudal = input_usuarios * consumo_agua  # 4 L/día


    # Calidad del agua
    st.subheader('Calidad del agua')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('* **Fuente de agua:**')
        input_fuente = st.selectbox('Escoja la fuente de agua:', options=[
                                        'Pozos', 
                                        'Manantiales o rios', 
                                        'Acuiferos confinados', 
                                        'Lagos o embalses', 
                                        'Mar', 
                                        'Lluvia', 
                                        'Ninguna'])
    with col2:
        st.markdown('* **Uso de los suelos:**')
        input_uso_suelos = st.selectbox('Escoja el uso de suelo cercano:', options=[
                                            'Industria', 
                                            'Agricultura', 
                                            'Mineria', 
                                            'Perforacion de pozos de gas o petroleo', 
                                            'Gasolineras', 
                                            'Casas con pozo septico', 
                                            'Deshielo de carreteras', 
                                            'Ninguno'])
    with col3:
        st.markdown('* **Color y sabor del agua:**')
        input_color_sabor = st.selectbox('¿El agua tiene un color o sabor particular?', options=[
                                            'Manchas color cafe anaranjadas y sabor metalico', 
                                            'Motas o manchas negras', 
                                            'Pelicula blanca o gris y necesidad de mayor uso de jabon', 
                                            'Sabor salado', 
                                            'Manchas azules y verdosas y sabor metalico', 
                                            'Ninguno'])

    st.markdown('* **pH del agua:**')
    st.markdown('''Se considera que si el pH del agua está entre **6,5 y 8**, esta puede ser consumida. 
    Un pH inferior a 6,5 indica que el agua es ácida, y habrá que prestar atención a los contaminantes químicos.
    Un pH superior a 8 indica que el agua es básica e incrementará su dureza, por lo que se revisará su turbidez.''')
    pH_conocido = st.checkbox('¿Se dispone del pH del agua?')
    if pH_conocido:
        input_pH = st.number_input('¿Cuál es el pH del agua?',min_value=0.0,max_value=14.0,value=7.0)
        if float(input_pH) < 6.5:
            pH_agua = 'Acido'
        elif float(input_pH) > 8:
            pH_agua = 'Basico'
        else:
            pH_agua = 'Neutro'
        
        if (float(input_pH) > 10) | (float(input_pH) < 5):
            st.warning('Es recomendable que *busque otra fuente de agua.*')
    else:
        pH_agua = 'Neutro'
    

    # BOTONES PRETRATAMIENTO Y DESINFECCION
    st.subheader('Pretratamiento y desinfección')
    pretratamiento = st.checkbox('¿Desea incluir un pretratamiento?', 
                            help='El pretratamiento consiste en un filtro de arena o un filtro de gravedad que reduce la turbidez del agua')

    desinfeccion = st.checkbox('¿Desea incluir desinfección?', 
                            help='La desinfección reduce los contaminantes microbiológicos')


    def calcular_calidad(fuente, suelos, color_sabor, pH):
        # Calidad microbiológica -> obtengo tablas de una fila
        new_df_fuente = df_fuente.loc[df_fuente['Nombre'] == fuente]
        new_df_suelos = df_suelos.loc[df_suelos['Nombre'] == suelos]
        new_df_color_sabor = df_color_sabor.loc[df_color_sabor['Nombre'] == color_sabor]
        new_df_pH = df_pH.loc[df_pH['Nombre'] == pH]

        # microb está en la columna 2
        microb = max(new_df_fuente.iloc[0, 1], new_df_suelos.iloc[0, 1],
                    new_df_color_sabor.iloc[0, 1], new_df_pH.iloc[0, 1])
        #microb = max(int(new_df_fuente.iloc[1, 2]), int(new_df_suelos.iloc[1, 2]), int(new_df_color_sabor.iloc[1, 2]), int(new_df_pH.iloc[1, 2]))
        ## microb = max(new_df_fuente.iloc[1, 2], new_df_suelos.iloc[1:, 2], new_df_color_sabor.iloc[1:, 2], new_df_pH.iloc[1, 2])
        # quimic está en la columna 3
        quimic = max(new_df_fuente.iloc[0, 2], new_df_suelos.iloc[0, 2],
                    new_df_color_sabor.iloc[0, 2], new_df_pH.iloc[0, 2])
        ## quimic = max(new_df_fuente.iloc[1, 3], new_df_suelos.iloc[1:, 3], new_df_color_sabor.iloc[1:, 3], new_df_pH.iloc[1, 3])
        # turb está en la columna 4
        turb = max(new_df_fuente.iloc[0, 3], new_df_suelos.iloc[0, 3],
                new_df_color_sabor.iloc[0, 3], new_df_pH.iloc[0, 3])
        ## turb = max(new_df_fuente.iloc[1, 4], new_df_suelos.iloc[1:, 4], new_df_color_sabor.iloc[1:, 4], new_df_pH.iloc[1, 4])

        return [microb, quimic, turb]


    calidad = calcular_calidad(input_fuente, input_uso_suelos, input_color_sabor, pH_agua)
    

    # Modificar calidad microbiológica y turbidez si se selecciona pretratamiento y desinfección
    if pretratamiento:
        calidad[2] = 1
    if desinfeccion:
        calidad[0] = 0


with seleccion_modelo:
    st.markdown('___')
    st.header('Métodos de tratamiento recomendados:')

    # Mostrar las entradas del modelo según las opciones seleccionadas:
    st.markdown('El modelo recibe como entrada los siguientes valores:')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'* **Disponibilidad de electricidad:** {input_elec}')
        st.markdown(f'* **Disponibilidad de red de distribución:** {input_red}')
        st.markdown(f'* **Uso del edificio:** {input_uso_edificio}')
        st.markdown(f'* **Caudal:** {caudal} L/día')
    with col2:
        st.markdown(f'* **Fuente de agua:** {input_fuente}')
        st.markdown(f'* **Uso de los suelos:** {input_uso_suelos}')
        st.markdown(f'* **Color y sabor del agua:** {input_color_sabor}')
        st.markdown(f'* **pH del agua:** {pH_agua}')
    with col3:
        st.markdown('Calidad del agua:')
        st.markdown(f'* **Calidad microbiológica:** {calidad[0]}')
        st.markdown(f'* **Calidad química:** {calidad[1]}')
        st.markdown(f'* **Turbidez:** {calidad[2]}')


    new_df = df

    if input_elec == 'No':
        # Me quedo solo con los métodos que no usen electricidad o funcionen con ambos
        new_df = new_df.loc[(df['Electricidad'] == 0) | (df['Electricidad'] == 2)]

    if input_red == 'No':
        # Me quedo solo con los mét. que no necesiten red de distribución o funcionen con ambos
        new_df = new_df.loc[(df['Uso de red'] == 0) | (df['Uso de red'] == 2)]

    if input_uso_edificio == 'Individual':
        new_df = new_df.loc[(df['Uso del edificio'] == 0) | (df['Uso del edificio'] == 2)]
    else:
        new_df = new_df.loc[(df['Uso del edificio'] == 1) | (df['Uso del edificio'] == 2)]

    # Número de máquinas
    st.write('')
    st.markdown('''
                    En ocasiones, es común instalar más de una máquina para llevar a cabo el tratamiento. 
                    Especialmente si el caudal es elevado.''')
    n_maquinas = st.slider('Modifique el número de máquinas que puede instalar:', min_value=1, max_value=20)

    new_df = new_df.loc[(new_df['Caudal'] >= caudal/n_maquinas) & 
                        (new_df['Calidad microbiologica'] >= calidad[0]) & 
                        (new_df['Calidad quimica'] >= calidad[1]) & 
                        (new_df['Turbidez'] >= calidad[2])]
    st.markdown(f'Cadual por máquina: {caudal/n_maquinas:0.2f} L/día' )
    

    ## EXCEPCIONES:
    if input_fuente == 'Mar':
        # new_df = new_df.append(df.loc[df['Metodo'] == 'Filtracion por osmosis inversa'])
        new_df = pd.concat([new_df, df.loc[df['Metodo'] == 'Filtracion por osmosis inversa']])
    
    if pH_agua == 'Basico':
        # new_df = new_df.append(df.loc[df['Metodo'] == 'Filtros de cal o descalcificadores'])
        new_df = pd.concat([new_df, df.loc[df['Metodo'] == 'Filtros de cal o descalcificadores']])

    st.markdown('Dados los parámetros de entrada introducidos por el usuario, los modelos de selección que permitirán obtener un agua potable de calidad son:')
    st.table(new_df.style.format(subset=['Caudal'], formatter="{:.2f}"))
    st.caption('El caudal está en litros por minuto')

    
with ordenar_resultados:
    st.markdown('___')
    st.subheader('Resumen de los resultados')
    # Guardo los métodos en una cadena
    metodos = new_df['Metodo']

    st.markdown('''
            En la siguiente tabla puede filtrar los métodos de tratamiento según la dificultad de instalación, 
            la dificultad de mantenimiento y el precio relativo.''')

    new_tabla = pd.DataFrame()

    for metodo in metodos:
        new_row = df_comparativa.loc[df_comparativa['Metodo'] == metodo]
        # new_tabla = new_tabla.append(new_row)
        new_tabla = pd.concat([new_tabla, new_row])
    
    ordenar = st.selectbox('Seleccione la característica con la que quiere ordenar los métodos:', options=[
                                'Instalacion',
                                'Mantenimiento',
                                'Precio relativo'])


    st.markdown('*Tabla ordenada:*')
    new_tabla.sort_values(ordenar)
    st.table(new_tabla.sort_values(ordenar, ascending=True).style.format(subset=['Caudal'], formatter="{:.2f}"))
    st.caption('El caudal está en litros por minuto')

    if pretratamiento:
        st.markdown('* Ha seleccionado incluir un **pretratamiento** por lo que debe instalar un **filtro de arena** o un **filtro de gravedad**.')

    if desinfeccion:
        st.markdown('* Ha seleccionado incluir **desinfección**.')
        if input_elec == 'No':
            st.markdown('Como **no** dispone de electricidad, debe instalar **Cloración con hipoclorito de sodio**.')
        elif input_elec == 'Si':
            st.markdown('Como dispone de electricidad, puede usar **cloración con hipoclorito de sodio, gas de cloro licuado o la ozonización**.')
# pipreqs ./
