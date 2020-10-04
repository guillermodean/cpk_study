
import pandas as pd;
import numpy as np;
import os
import mysql.connector as mysql
try
db=mysql.connect(
    host='10.73.83.220',
    user='root',
    password='Windows2020',
    db='opc_client_db'
)

def Cp(mylist, usl, lsl):
    arr = np.array(mylist)
    arr = arr.ravel()
    sigma = np.std(arr)
    Cp = float(usl - lsl) / (6*sigma)
    return Cp
def Cpk(mylist, usl, lsl):
    arr = np.array(mylist)
    arr = arr.ravel()
    sigma = np.std(arr)
    m = np.mean(arr)

    Cpu = float(usl - m) / (3*sigma)
    Cpl = float(m - lsl) / (3*sigma)
    Cpk = np.min([Cpu, Cpl])
    return Cpk


for i in xrange(0,13):
    #importar tabla modelos y hacer for
    #Modelo='P5802450389'
    cursor=db.cursor()
    query='SELECT Button'+str(i)'_Value FROM opcua_client_db.test_result WHERE Modelo='+str(Modelo)
    cursor.execute(query)
    table_rows = db_cursor.fetchall()
    data = pd.DataFrame(table_rows)
    datafiltered=data[(data != 0) & (pd.isnull(data))] # quitar ceros y nulos
    data_noutliers = datafiltered[datafiltered.between(datafiltered.quantile(.15), datafiltered.quantile(.85))]  # without outliers
    cp_sql=Cp(data_noutliers, 10, 0)
    cpk_sql=Cpk(data_noutliers, 10, 0)

    query = "INSERT INTO CPK (CP,CPK) VALUES (%s, %s, %s)"
    ## storing values in a variable
    values = ( Modelo,'Button'+str(i)'_Value',cp_sql,cpk_sql,)
    ## executing the query with values
    cursor.execute(query, values)
    db.commit()