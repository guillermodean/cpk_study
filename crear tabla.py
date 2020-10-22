import pandas as pd
import mysql.connector as mysql

try:
    db = mysql.connect(host='10.73.83.220', user='calidad', password='Pamp3701', db='opcua_client_db')

except mysql.Error as err:
        print ('error de conexion ala BBDD'+str(err))
familias=pd.read_csv('familias.csv',sep=';',names=['modeloISRI','Modelo','nombre','familia'])
n=1
query = 'SELECT * FROM opcua_client_db.test_result  ORDER BY Id DESC'
data = pd.read_sql(query, con=db)
dataall=data.merge(familias,on='Modelo')
dataporfamilia=dataall.groupby(['familia']).mean()
dataporfamilia.to_csv('medias.csv',sep=';')
