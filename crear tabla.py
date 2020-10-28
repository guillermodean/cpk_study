import pandas as pd
import mysql.connector as mysql
from calculos import filtrar
try:
    db = mysql.connect(host='10.73.83.220', user='calidad', password='Pamp3701', db='opcua_client_db')

except mysql.Error as err:
        print ('error de conexion ala BBDD'+str(err))

def means():
    familias=pd.read_csv('familias.csv',sep=';',names=['modeloISRI','Modelo','nombre','familia'])
    query = 'SELECT * FROM opcua_client_db.test_result  ORDER BY Id DESC'
    data = pd.read_sql(query, con=db)
    #filtrar((data))
    datafecha=data[data['Date']>'2020-09-01']
    dataall=datafecha.merge(familias,on='Modelo')
    dataall=dataall.drop(['Id'],axis=1)
    dataporfamilia=dataall.groupby(['familia']).agg(['mean','std','size'])
    dataporfamilia.to_csv('medias.csv',sep=';')


    return dataporfamilia
def results():
    familias = pd.read_csv('familias.csv', sep=';', names=['modeloISRI', 'Modelo', 'nombre', 'familia'])
    query='SELECT * FROM opcua_client_db.results_cpk_ ORDER BY Id DESC'
    names=["Id", "Date", "Button","Media","Tol_inf","Tol_sup","cp","cpk","Modelo"]
    results = pd.read_sql(query, con=db)
    results.columns=names
    resultsporfamilia=results.merge(familias,on='Modelo')
    resultsmean=resultsporfamilia.groupby(['familia']).mean()

    return resultsmean
print(means())
