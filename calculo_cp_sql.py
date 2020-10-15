import pandas as pd
import numpy as np
import math
import mysql.connector as mysql
import datetime
import matplotlib.pyplot as plt
from tkinter import *
from calculos import cp,cpk,cpl,cpu,filtrar
from interfaz import introducemodelo,modelovar
from query import querys


try:
    db = mysql.connect(host='10.73.83.220', user='calidad', password='Pamp3701', db='opcua_client_db')

except mysql.Error as err:
        print ('error de conexion ala BBDD'+str(err))

introducemodelo()
modelo=modelovar()

try:
    for i in range(13):
        n=i+1
        #modelo='P5802450411'
        '''mysql query data'''
        query_select_mysql = 'SELECT Button' + str(n) + '_Value     FROM opcua_client_db.test_result where test_result.Modelo="' + modelo + '" ORDER BY Id DESC limit 50'
        query_select_mysql_nm = 'SELECT Button' + str(n) + '_Value FROM opcua_client_db.test_result ORDER BY Id DESC limit 200'
        query=querys(modelo,query_select_mysql,query_select_mysql_nm)
        data = pd.read_sql(query, con=db)
        data.columns = ['valores']
        dataf=filtrar(data)

        '''mysql select modelos'''
        query_modelos_mysql="SELECT Button, tol_inf_n, tol_sup_n FROM modelos WHERE Button='Button"+str(n)+"_Value' AND Modelo='"+str(modelo)+"'"
        query_modelos_mysql_nm="SELECT Button, tol_inf_n, tol_sup_n FROM modelos WHERE Button='Button"+str(n)+"_Value' AND Modelo='P5802450411'"
        query=querys(modelo,query_modelos_mysql,query_modelos_mysql_nm)
        modelos=pd.read_sql(query,con=db)
        toli=modelos.iloc[0, 1]
        tols=modelos.iloc[0,2]
        cp_sql = cp(dataf, tols, toli)  # Calcular cpks
        cpk_sql = cpk(dataf, tols, toli)
        fcpu = cpu(dataf, tols)
        fcpl = cpl(dataf, toli)
        mean = dataf['valores'].mean()
        mean = round(mean, 2)
        cp_sql=round(cp_sql,2)
        cpk_sql = round(cpk_sql, 2)
        fcpu=round(fcpu,2)
        fcpl=round(fcpl,2)
        Button=modelos.iloc[0,0]

        if math.isnan(mean):
            mean=0
        if math.isnan(cp_sql):
            cp_sql=0
        if math.isnan(cpk_sql):
            cpk_sql=0
        date = datetime.datetime.now()
        cp_sql=float(cp_sql)
        cpk_sql=float(cpk_sql)
        print(date, Button, mean, toli, tols, (cp_sql), (cpk_sql))

        """Guardar los datos en la tabla results cpk"""

        query_insert = "INSERT  opcua_client_db.results_cpk_ (Date,Button,Media,Tol_inf,Tol_sup,cp,cpk,modelo) VALUES ('"+str(date)+"','"+Button+"','"+str(mean)+"','"+str(toli)+"','"+str(tols)+"','"+str(cp_sql)+"','"+str(cpk_sql)+"','"+str(modelo)+"')"
        query_insert_nm = "INSERT  opcua_client_db.results_cpk_ (Date,Button,Media,Tol_inf,Tol_sup,cp,cpk,modelo) VALUES ('" + str(date) + "','" + Button + "','" + str(mean) + "','" + str(toli) + "','" + str(tols) + "','" + str(cp_sql) + "','" + str(cpk_sql) + "','todos')"
        query=querys(modelo,query_insert,query_insert_nm)
        cursor=db.cursor()
        cursor.execute(query)
        db.commit()

        """graficar"""
        if mean != 0:
            fig, axes= plt.subplots(1,2)
            axes[0].plot(dataf,label='datos')
            axes[0].plot(data,'--',label='sinfiltrar')
            axes[0].plot([toli]*len(dataf),'red',label='tol inf')
            axes[0].plot([tols]*len(dataf),'red',label='tol sup')
            axes[0].plot([fcpl]*len(data),'green',label='lsl')
            axes[0].plot([fcpu]*len(data), 'green',label='usl')
            axes[0].legend(loc='upper right')
            plt.ylabel('muestras')
            plt.xlabel('Nm')
            plt.title("grafica "+Button+" CPK "+str(cpk_sql)+" cp "+str(cp_sql),)
            axes[1].hist(dataf)
            axes[1].set_xlim(0,180)
            plt.show()
        else:
            print('No data'+Button)
    print('endoflines')
except:
    print('error total')