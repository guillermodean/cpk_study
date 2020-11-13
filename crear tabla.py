import pandas as pd
import mysql.connector as mysql
import seaborn as sns
import matplotlib.pyplot as plt
from calculos import filtrar
import numpy as np

try:
    db = mysql.connect(host='10.73.83.220', user='calidad', password='Pamp3701', db='opcua_client_db')

except mysql.Error as err:
        print ('error de conexion ala BBDD'+str(err))

familias=pd.read_csv('familias.csv',sep=';',names=['modeloISRI','Modelo','nombre','familia'])
query = 'SELECT * FROM opcua_client_db.test_result  ORDER BY Id DESC'
data = pd.read_sql(query, con=db)

def means(data,fecha):
    #print(data.info())

    datafecha=data[data['Date']>fecha]
    #print(datafecha.info())
    dataall=datafecha.merge(familias,on='Modelo')
    dataall=dataall.drop(['Id'],axis=1)
    dataall = dataall[['Modelo','familia','Button1_Value','Button2_Value','Button3_Value','Button4_Value','Button5_Value','Button6_Value','Button7_Value','Button8_Value','Button9_Value','Button10_Value','Button11_Value','Button12_Value','Button13_Value']]
    dataxfamilia = dataall.pivot(columns='familia',values=['Button1_Value','Button2_Value','Button3_Value','Button4_Value','Button5_Value','Button6_Value','Button7_Value','Button8_Value','Button9_Value','Button10_Value','Button11_Value','Button12_Value','Button13_Value'])
    #print(dataxfamilia)

    return dataxfamilia

def results():
    familias = pd.read_csv('familias.csv', sep=';', names=['modeloISRI', 'Modelo', 'nombre', 'familia'])
    query='SELECT * FROM opcua_client_db.results_cpk_ ORDER BY Id DESC'
    names=["Id", "Date", "Button","Media","Tol_inf","Tol_sup","cp","cpk","Modelo"]
    results = pd.read_sql(query, con=db)
    results.columns=names
    resultsporfamilia=results.merge(familias,on='Modelo')
    resultsmean=resultsporfamilia.groupby(['familia']).mean()

    return resultsmean

def graficamedias(data):
    #print(data.describe())
    datafecha=data[data['Date']>'2020-09-01']
    dataall=datafecha.merge(familias,on='Modelo')
    dataall=dataall.drop(['Id'],axis=1)
    dataporfamilia = dataall.groupby(['familia']).agg(['mean', 'std', 'size'])
    dataporfamilia.to_csv('medias.csv', sep=';')
    return dataporfamilia

def boxplot(data):
    dataf=data.drop(columns=['Button1_State','Button2_State','Button3_State','Button4_State','Button5_State','Button6_State','Button7_State','Button8_State','Button9_State','Button10_State','Button11_State','Button12_State','Button13_State','Side','Resultado_OK','Isri_Order','Id'])
    datafm=pd.merge(dataf,familias,how='inner',on='Modelo')
    datapivotf = datafm.pivot_table(dataf, columns='familia')
    #print(datapivotf)
    corr=datapivotf.corr()
    #sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns)
    #plt.show()
    #print(corr)
    return datafm


dataporfamilia=graficamedias(data)
#print(dataporfamilia)



"""for i in range(13):
    a = i + 1
    fig = plt.figure()
    date = '2020-10-01'
    datafamily=means(data,date)
    datafamily1=(datafamily['Button'+str(a)+'_Value'])
    recuento = len(datafamily1)
    datafamily1=datafamily1.dropna(how='all', axis=0)

    for label, content in datafamily1.items():
        df=content.to_frame()
        df = df.dropna(how='all', axis=0)
        count=len(df)
        name=label
        print(count,label)
        sns.distplot(df, label=label, hist=False)
    plt.title('Button' + str(a) + '_Value n=' + str(count))
    fig.legend()
"""
databoxplot=boxplot(data)

for i in range(13):
    a = i + 1
    datacol=data['Button'+str(a)+'_Value']
    datacol = datacol.replace(0, np.nan)
    datacol = datacol.dropna(how='all', axis=0)
    x = pd.Series(datacol, name='Button'+str(a)+'_Value')

    date = '2020-10-01'
    datafamily = means(data, date)
    datafamily1 = (datafamily['Button' + str(a) + '_Value'])
    recuento = len(datafamily1)
    datafamily1 = datafamily1.dropna(how='all', axis=0)
    fig, axes = plt.subplots(1, 3, figsize=(10, 5))
    fig.suptitle('Title')
    axes[0].set_title('DIST')
    axes[1].set_title('BOX')

    for label, content in datafamily1.items():
        df = content.to_frame()
        df = df.dropna(how='all', axis=0)
        count = len(df)
        name = label
        #print(count, label)
        axes[2].set_title('Button' + str(a) + '_Value n=' + str(count))
        ax2=sns.distplot(df,ax=axes[2], label=label, hist=False)
        ax = sns.distplot(x,ax=axes[0])
        ax1 = sns.boxplot(ax=axes[1],data=databoxplot, x='familia', y=('Button' + str(a) + '_Value'))
        ax2.legend()
plt.show()