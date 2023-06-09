# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 10:38:58 2022

@author: marinas
"""

import pandas as pd
import numpy as np
import math
import pickle


#%% Funciones
def obtener(val):
    # Cambiar valor NaN por '-'
    try:
        if math.isnan(val):
            return('-')
        else:
            return(val)
    except:
        return(val)
    
def get_search(lista):
    # Obtener lista con strings de búsqueda para obtner el CS
    search = []
    for ele in lista:
        if obtener(ele) != '-':
            search.append(str(ele))
    return(search)
    
    
def get_CS(lista):
    # Obtener el CS que contiene en el TITL el string de búsqueda 'LISTA'
    df_search = df_cs
    for ele in lista:
        df_search = df_search[df_search['TITL'].str.contains(str(ele))==True]
    
    cs = df_search.iloc[0,0]
    return(cs)
    
def fases_csm(NO, TYPE, T, RH, TEMP, NCRE, PROB, LAUN, LAU2, FACV, CANT, ICS1,
              FACP, TITL):
    coman = ['NO', 'TYPE', 'T', 'RH', 'TEMP', 'NCRE', 'PROB', 'LAUN', 'LAU2', \
             'FACV', 'CANT', 'ICS1', 'FACP', 'TITL']
    value = [obtener(NO), obtener(TYPE), obtener(T), obtener(RH), \
             obtener(TEMP), obtener(NCRE), obtener(PROB), obtener(LAUN), \
             obtener(LAU2), obtener(FACV), obtener(CANT), obtener(ICS1), \
             obtener(FACP), obtener(TITL)]
    salida = 'CS '
    i = 0
    for comando in coman:
        if value[i] != '-':
            if comando == 'TITL':
                salida = salida + comando + ' "' + value[i] + '"'
            elif comando == 'NCRE' or comando == 'ICS1':
                salida = salida + comando + ' ' + str(int(value[i])) + ' '
            else:
                salida = salida + comando + ' ' + str(value[i]) + ' '
        i += 1
    return salida
        

def grp_csm(NO, VAL, ASTI, HFIX, BEDD, SITU, T0, TS, FAC1, ICSD, PHIF, QUEA, 
            QEMX, FACD, K1_CS_ini, K2_CS_ini, K3_CS_ini, K1_CS_fin, K2_CS_fin,
            K3_CS_fin, Comentario):
    coman = ['NO', 'ICS1', 'ATIL', 'VAL', 'ASTI', 'HFIX', 'BEDD', 'SITU', \
             'T0', 'TS', 'FAC1', 'ICSD', 'PHIF', 'QUEA', 'QEMX', 'FACD']

    # Búsqueda del ICS1 y el ATIL
    search_ini = get_search([K1_CS_ini, K2_CS_ini, K3_CS_ini])
    search_fin = get_search([K1_CS_fin, K2_CS_fin, K3_CS_fin])
 
    try:
        ICS1 = get_CS(search_ini)
    except:
        print(f'No se ha encontrado {search_ini}')
    
    if search_fin != []:
        try:
            ATIL = get_CS(search_fin) - 1
        except:
            print(f'No se ha encontrado {search_fin}')
    else:
        ATIL = '-'
    
    # Comentario
    if obtener(Comentario) == '-':
        Comentario = ''
        for texto in search_ini:
            Comentario = Comentario + texto + ' '
    
    # Generación de otuput
    value = [obtener(NO), obtener(ICS1), obtener(ATIL), obtener(VAL),  \
              obtener(ASTI), obtener(HFIX), obtener(BEDD), obtener(SITU), \
              obtener(T0), obtener(TS), obtener(FAC1), obtener(ICSD), \
              obtener(PHIF), obtener(QUEA), obtener(QEMX), obtener(FACD)]
    salida = 'GRP '
    i = 0
    for comando in coman:
        if value[i] != '-':
            salida = salida + comando + ' ' + str(value[i]) + ' '
        i += 1
    salida = salida + ' $ ' + Comentario

    return [salida, ICS1, ATIL, Comentario]


def lc_csm(NO, FACT, K1_CS_ini, K2_CS_ini, K3_CS_ini, K1_CS_fin, K2_CS_fin,
            K3_CS_fin, Comentario):
    coman = ['NO', 'ICS1', 'ATIL', 'FACT']

    # Búsqueda del ICS1 y el ATIL
    search_ini = get_search([K1_CS_ini, K2_CS_ini, K3_CS_ini])
    search_fin = get_search([K1_CS_fin, K2_CS_fin, K3_CS_fin])
 
    try:
        ICS1 = get_CS(search_ini)
    except:
        print(f'No se ha encontrado {search_ini}')
    
    if search_fin != []:
        try:
            ATIL = get_CS(search_fin) - 1
        except:
            print(f'No se ha encontrado {search_fin}')
    else:
        ATIL = '-'
    
    # Comentario
    if obtener(Comentario) == '-':
        Comentario = ''
        for texto in search_ini:
            Comentario = Comentario + texto + ' '
    
    # Generación de otuput
    value = [obtener(NO), obtener(ICS1), obtener(ATIL), obtener(FACT)]
    salida = 'LC '
    i = 0
    for comando in coman:
        if value[i] != '-':
            salida = salida + comando + ' ' + str(value[i]) + ' '
        i += 1
    salida = salida + ' $ ' + Comentario

    return [salida, ICS1, ATIL, Comentario]

def grcs_csm(NO, FACS, FACL, PREX, K1_CS_apd, K2_CS_apd, K3_CS_apd, 
             K1_CS_ad, K2_CS_ad, K3_CS_ad, Comentario):
    coman = ['NO', 'CS', 'FACS', 'FACL', 'PREX']

    # Búsqueda del CS
    search_apd = get_search([K1_CS_apd, K2_CS_apd, K3_CS_apd])
    search_ad = get_search([K1_CS_ad, K2_CS_ad, K3_CS_ad])
    
    try:
        CS_apd = get_CS(search_apd)
    except:
        print(f'No se ha encontrado {search_apd}')
        
    if search_ad != []:
        try:
            CS_ad = get_CS(search_ad)
        except:
            print(f'No se ha encontrado {search_ad}')
    else:
        CS_ad = '-'
    
    # Si no hay modificador de rigidez final, sólo se aplica el GRCS para ese CS
    if CS_ad == '-':
        CS = [CS_apd]
                    
    # Si hay modificador de rigidez final, entonces se aplica el GRCS a todos
    # los casos de carga entre CS_apd y CS_ad (sin incluirlos):
    else:        
        cs_afect = df_cs[(df_cs['NO'] > CS_apd) & 
                         (df_cs['NO'] < CS_ad)]['NO'].to_list()
        CS = cs_afect
        # CS_inter = ''
        # for csaf in cs_afect:
        #     CS_inter = CS_inter + str(csaf) + ','
        # CS = CS_inter[:-1]
        
    # Generación de otuput
    if CS != []: # Eliminamos el caso en el que el CS de tesado va justo 
                 # después del CS de instalación
        
        out_sal = []
        
        for st in CS:
            value = [obtener(NO), st, obtener(FACS), obtener(FACL), obtener(PREX)]
            salida = 'GRCS '
            i = 0
            for comando in coman:
                if value[i] != '-':
                    salida = salida + comando + ' ' + str(value[i]) + ' '
                i += 1
            salida = salida + ' $ ' + obtener(Comentario)
            out_sal.append(salida)
    else:
        salida = ''
        out_sal = [salida]

    return out_sal

def fichero_bin(nombre, info):
    # Creación de fichero con acceso de escritura binaria:
    fichero_bin = open(nombre, "wb")
    
    # Volcado de la lista a ese fichero externo:
    pickle.dump(info, fichero_bin) 
    
    # Se cierra el fichero:
    fichero_bin.close()
    
    # Borrado de la memoria del fichero:
    del(fichero_bin)


#%% Lectura de excel de datos   

# Volcado dataframes por hojas
# ----------------------------
excel_maestro = 'Sacador_CSM_definitivo.xlsm'
df_cab = pd.read_excel(excel_maestro, sheet_name='CTRL',
                     header = None)
df_cs = pd.read_excel(excel_maestro, sheet_name='CS')
df_grp = pd.read_excel(excel_maestro, sheet_name='GRP')
df_lc = pd.read_excel(excel_maestro, sheet_name='LC')
df_grcs = pd.read_excel(excel_maestro, sheet_name='GRCS')
df_extra = pd.read_excel(excel_maestro, sheet_name='Extra',
                     header = None) #.iloc[:, 2:]

#%% Texto fichero CSM

# Fases
# -----
fases_txt = np.vectorize(fases_csm)(NO = df_cs['NO'], 
                        TYPE = df_cs['TYPE'], 
                        T = df_cs['T'], 
                        RH = df_cs['RH'], 
                        TEMP = df_cs['TEMP'], 
                        NCRE = df_cs['NCRE'], 
                        PROB = df_cs['PROB'], 
                        LAUN = df_cs['LAUN'], 
                        LAU2 = df_cs['LAU2'], 
                        FACV = df_cs['FACV'], 
                        CANT = df_cs['CANT'], 
                        ICS1 = df_cs['ICS1'], 
                        FACP = df_cs['FACP'], 
                        TITL = df_cs['TITL'])

# Número de fases:
num_fases = df_cs['NO'].tolist()
max_fase = num_fases[-1] 

# Número de fases en el modelo (se añaden las de reológicas):
list_NCRE = df_cs['NCRE'].tolist()
cont = 0
num_fases_reales = []
for ncre in list_NCRE:
    if np.isnan(ncre):
        num_fases_reales.append(num_fases[cont])
    else:
        for reo in range(int(ncre)):
            num_fases_reales.append(num_fases[cont] + reo)
        pass
    cont += 1

# Grupos
# ------
grupos_txt = np.vectorize(grp_csm, otypes = [list])(
                                    NO         =  df_grp['NO'],       
                                    VAL        =  df_grp['VAL'],      
                                    ASTI       =  df_grp['ASTI'],     
                                    HFIX       =  df_grp['HFIX'],     
                                    BEDD       =  df_grp['BEDD'],     
                                    SITU       =  df_grp['SITU'],     
                                    T0         =  df_grp['T0'],       
                                    TS         =  df_grp['TS'],       
                                    FAC1       =  df_grp['FAC1'],     
                                    ICSD       =  df_grp['ICSD'],     
                                    PHIF       =  df_grp['PHIF'],     
                                    QUEA       =  df_grp['QUEA'],     
                                    QEMX       =  df_grp['QEMX'],     
                                    FACD       =  df_grp['FACD'],     
                                    K1_CS_ini  =  df_grp['K1 CS ini'],
                                    K2_CS_ini  =  df_grp['K2 CS ini'],
                                    K3_CS_ini  =  df_grp['K3 CS ini'],
                                    K1_CS_fin  =  df_grp['K1 CS fin'],
                                    K2_CS_fin  =  df_grp['K2 CS fin'],
                                    K3_CS_fin  =  df_grp['K3 CS fin'],
                                    Comentario =  df_grp['Comentario']
                                    )

df_grp_resumen = df_grp[['NO', 'ICS1', 'ATIL']].copy()
lst_grp_ICS1 = []
lst_grp_ATIL = []
lst_grp_CMN = []
for i in grupos_txt:
    lst_grp_ICS1.append(i[1])
    lst_grp_ATIL.append(i[2])
    lst_grp_CMN.append(i[3])
df_grp_resumen['ICS1'] = np.array(lst_grp_ICS1)
df_grp_resumen['ATIL'] = np.array(lst_grp_ATIL)
df_grp_resumen['Comentario'] = np.array(lst_grp_CMN)

# Cargas
# ------
lc_txt = np.vectorize(lc_csm, otypes = [list])(
                                    NO         =  df_lc['NO'],       
                                    FACT       =  df_lc['FACT'],     
                                    K1_CS_ini  =  df_lc['K1 CS ini'],
                                    K2_CS_ini  =  df_lc['K2 CS ini'],
                                    K3_CS_ini  =  df_lc['K3 CS ini'],
                                    K1_CS_fin  =  df_lc['K1 CS fin'],
                                    K2_CS_fin  =  df_lc['K2 CS fin'],
                                    K3_CS_fin  =  df_lc['K3 CS fin'],
                                    Comentario =  df_lc['Comentario']
                                    )

df_lc_resumen = df_lc[['NO', 'ICS1', 'ATIL']].copy()
lst_lc_ICS1 = []
lst_lc_ATIL = []
lst_lc_CMN = []
for i in lc_txt:
    lst_lc_ICS1.append(i[1])
    lst_lc_ATIL.append(i[2])
    lst_lc_CMN.append(i[3])
df_lc_resumen['ICS1'] = np.array(lst_lc_ICS1)
df_lc_resumen['ATIL'] = np.array(lst_lc_ATIL)
df_lc_resumen['Comentario'] = np.array(lst_lc_CMN)

# GRCS
# ----
grcs_txt = np.vectorize(grcs_csm, otypes = [list])(
                                    NO         =  df_grcs['NO'],       
                                    FACS       =  df_grcs['FACS'],     
                                    FACL       =  df_grcs['FACL'],     
                                    PREX       =  df_grcs['PREX'],     
                                    K1_CS_apd  =  df_grcs['K1 CS a p d'],
                                    K2_CS_apd  =  df_grcs['K2 CS a p d'],
                                    K3_CS_apd  =  df_grcs['K3 CS a p d'],
                                    K1_CS_ad   =  df_grcs['K1 CS a d'],
                                    K2_CS_ad   =  df_grcs['K2 CS a d'],
                                    K3_CS_ad   =  df_grcs['K3 CS a d'],
                                    Comentario =  df_grcs['Comentario']
                                    )

# GENERACIÓN FICHERO
# ------------------
with open('CSM_automatico.dat', 'w') as file:
    file.write('+PROG CSM\n\n')
    for i in df_cab.iloc[:, 0]:
        try:
            math.isnan(i)
        except:
            file.write(i + '\n')
    file.write('\n!*!Label Construction stages\n')
    for i in fases_txt:
        file.write(i + '\n')
    
    file.write('\n!*!Label Group activation\n')
    for i in grupos_txt:
        file.write(i[0] + '\n')
    
    file.write('\n!*!Label Loadcase activation\n')
    for i in lc_txt:
        file.write(i[0] + '\n')
    
    if not df_grcs.empty:
        file.write('\n!*!Label Group-stage special settings\n')
        for i in grcs_txt:
            for k in i:
                file.write(k + '\n')
    
    if not df_extra.empty:    
        file.write('\n!*!Label Additional information\n')        
        for i in df_extra.iloc[:, 0]:
            try:
                math.isnan(i)
            except:
                file.write(i + '\n')            
    file.write('\nEND\n')
    file.write('\n+APPLY "$(NAME)_csm.dat"\n')
    
    
#%% Gráfico  
def genera_graf(NO, ICS1, ATIL, COM):
    resul = {'Nombre': COM, 'Nr': NO}
    for fase in num_fases:
        if fase < int(ICS1):
            resul[fase] = ''
        elif fase == int(ICS1):
            resul[fase] = 'E'
        else:
            if ATIL != '-':
                ult = int(ATIL) + 1
                if fase < ult:
                    resul[fase] = 'x'
                elif fase == ult:
                    resul[fase] = 'S'
                else:
                    resul[fase] = ''
            else:
                resul[fase] = 'x'
    return resul       

df_grp_lc = pd.concat([df_grp_resumen, df_lc_resumen])    
dic_rell = np.vectorize(genera_graf, otypes = [dict])(
                                    NO         =  df_grp_lc['NO'],       
                                    ICS1       =  df_grp_lc['ICS1'],       
                                    ATIL       =  df_grp_lc['ATIL'],       
                                    COM =  df_grp_lc['Comentario']       
                                    )
df_grafico = pd.DataFrame(dic_rell.tolist())
df_grafico.set_index(['Nombre', 'Nr'], inplace = True)
df_grafico.columns = [df_cs['TITL'].tolist(), num_fases]

df_grafico.to_excel('grafico_csm.xlsx', sheet_name = 'CSM', 
                    freeze_panes = (2,2))
    
# https://xlsxwriter.readthedocs.io/example_pandas_column_formats.html

#%% Obtención de datos para la matriz de tesado

# # Obtención de LC con tesado 2 de tirantes:
# df_lc_tirantes = df_lc_resumen[df_lc_resumen['NO'].isin(
#                  list(range(10300, 10501)))][['Comentario', 'NO', 'ICS1']]
# df_lc_tirantes['Comentario'] = df_lc_tirantes['Comentario'].str.replace(
#                                'Tes.','Tesado', regex = True)
# fases_tirantes2 = df_lc_tirantes.values.tolist()

# # Obtención de las fases de activación de tirantes:
# df_grp_tirantes = df_grp_resumen[df_grp_resumen['NO'].isin(
#                   list(range(301, 501)))][['Comentario', 'NO', 'ICS1']]
# df_grp_tirantes.rename(columns={'Comentario': 'Nombre', 'NO': 'Nr',
#                               'ICS1': 'CS ini'}, inplace=True)

# # Fases de tesado 1                                                           
# df_lc_tirantes1 = df_lc_resumen[df_lc_resumen['NO'].isin(
#                  list(range(10500, 10701)))][['Comentario', 'NO', 'ICS1']]
# df_lc_tirantes1['Comentario'] = df_lc_tirantes1['Comentario'].str.replace(
#                                'Tes.','Tesado', regex = True)
# fases_tirantes1 = df_lc_tirantes1.values.tolist()              

# # Fases de desapeo (incluye la fase donde se mete la fuerza auxiliar, y la
# # fase donde se quita esa fuerza, para lo que hay que sumar 1 a lo que hay
# # en df_lc_red, ya que en teddy hay que meter la última fase en la que está
# # la fuerza)                                                           
# df_lc_desapeo = df_lc_resumen[df_lc_resumen['NO'].isin(
#     list(range(14000, 14200)))][['Comentario', 'NO', 'ICS1', 'ATIL']]
# df_lc_desapeo['Comentario'] = df_lc_desapeo['Comentario'].str.replace(
#                                'F. desbloq.','Fuerza', regex = True)
# df_lc_desapeo['Comentario'] = df_lc_desapeo['Comentario'].str.replace(
#                                'F. desap.','Fuerza', regex = True)
# df_lc_desapeo['Comentario'] = df_lc_desapeo['Comentario'].str[:-1]
# df_lc_desapeo.reset_index(drop = True, inplace = True)
# df_lc_desapeo.rename(columns={'Comentario': 'Nombre', 
#                               'ICS1': 'CS ini',
#                               'ATIL': 'CS fin'}, inplace=True)
# df_lc_desapeo = df_lc_desapeo.astype({'CS fin': int, 'NO': int})
# df_lc_desapeo['CS fin'] = df_lc_desapeo['CS fin'] + 1

# fase_quitar = []

# dfnn = df_cs[['TITL', 'NO']] # Fases y sus números, para buscar
#                                 # la fase donde se hace efectivo el desapeo
# for index, row in df_lc_desapeo.iterrows():
#     fini = row['CS ini']
#     ffin = row['CS fin']
#     fase_quitar.append(dfnn.loc[(dfnn['TITL'].str.contains('Desap') | 
#                                   dfnn['TITL'].str.contains('Desbloq')) & 
#                                 (dfnn['NO'] > fini) & (dfnn['NO'] < ffin
#                                                        )].iloc[0, 1])
# df_lc_desapeo['CS des'] = fase_quitar
# fases_desapeo = df_lc_desapeo.values.tolist()     

# # Obtención de los grupos de apeos:
# df_grp_apeos = df_grp_resumen[df_grp_resumen['NO'].isin(
#                   list(range(80, 200)))][['Comentario', 'NO', 'ICS1']]
# df_grp_apeos.rename(columns={'Comentario': 'Nombre', 'NO': 'Nr',
#                               'ICS1': 'CS ini'}, inplace=True)

                                                           
# # Obtención de fases objetivo de tesado 1:
# fase_tes1 = []
# nom_fase_tes1 = []
# df_fase_tes1 = dfnn.loc[dfnn['TITL'].str.contains('Tes. 1') &
#                         dfnn['TITL'].str.contains('vac.')] #.iloc[:, :]
# fases_tes1 = df_fase_tes1.values.tolist() 

                                           
                                                           
# # Guardado de ficheros con la información para el tesado
# fichero_bin('01_lista_lc', num_fases_reales)
# fichero_bin('01_lista_lc_tirantes_tes2', fases_tirantes2)
# fichero_bin('01_dataframe_grp_tirantes', df_grp_tirantes) # Cuidado, activación inicial de tirantes
# fichero_bin('01_lista_lc_tirantes_tes1', fases_tirantes1) 
# fichero_bin('01_lista_lc_desapeos', fases_desapeo) 
# fichero_bin('01_dataframe_grp_apeos', df_grp_apeos) # Cuidado, activación inicial de apeos
# fichero_bin('01_fases_objetivo_tes1', fases_tes1) 

#%% Output de finalización

print("Generado el .dat del CSM")