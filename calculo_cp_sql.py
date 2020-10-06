import pandas as pd
import numpy as np
import os
import math
import mysql.connector as mysql
import pyodbc
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import *


class introducemodelo():
    def __init__(self):
        self.newWindow()
    def newWindow(self):
        # define your window
        root = Tk()
        root.geometry("400x100")
        root.resizable(False, False)
        root.title("Modelo Application")
        # add labels
        label1 = Label(text='Introduce el modelo')
        label1.pack()
        canvas1 = Canvas(root)
        canvas1.pack()
        entry1 = Entry(root)
        canvas1.create_window(200, 20, window=entry1)
        def addmodelo():
            global modelo_input
            modelo_input = entry1.get()
            print('modelo addmodelo'+modelo_input)
        button1 = Button(canvas1, text='Run Report', command=addmodelo)
        canvas1.create_window(200, 50, window=button1)
        root.mainloop()


try:
    db = mysql.connect(host='10.73.83.220', user='calidad', password='Pamp3701', db='opcua_client_db')

except mysql.Error as err:
        print ('error de conexion ala BBDD'+str(err))

def cp(mylist, usl, lsl):
    sigma=mylist.std(axis=0)
    sigma=(float(sigma))
    if sigma==0:
        cp=0
        return cp
    else:
        print('sigma= '+str(sigma)+' usl'+str(usl)+' lsl'+str(lsl)+' resta'+ str(float(usl-lsl)))
        cp = float(usl - lsl) / (6 * sigma)
        return cp
def filtrar (data):
    datafiltered = data[(data != 0)]  # quitar ceros y nulos
    Q1 = datafiltered.quantile(0.15)
    Q3 = datafiltered.quantile(0.85)
    IQR = Q3 - Q1
    data_noutliers = datafiltered[~((datafiltered < (Q1 - 1.5 * IQR)) | (datafiltered > (Q3 + 1.5 * IQR))).any(axis=1)]
    return data_noutliers
def cpk(mylist, usl, lsl):
    sigma = mylist.std(axis=0)
    sigma = (float(sigma))
    if sigma==0:
        cpk=0
        return cpk
    else:
        m=mylist['valores'].mean()
        Cpu = float(usl - m) / (3 * sigma)
        Cpl = float(m - lsl) / (3 * sigma)
        cpk = np.min([Cpu, Cpl])
        return cpk
def cpu(mylist,usl):
    sigma = mylist.std(axis=0)
    sigma = (float(sigma))
    if sigma == 0:
        cpu = 0
        return cpu
    else:
        m = mylist['valores'].mean()
        Cpu = m+(sigma*3)
        return Cpu
def cpl(mylist,lsl):
    sigma = mylist.std(axis=0)
    sigma = (float(sigma))
    if sigma == 0:
        cpl = 0
        return cpl
    else:
        m = mylist['valores'].mean()
        Cpl = m-(sigma*3)
        return Cpl


introducemodelo()
modelo=modelo_input

try:
    for i in range(13):
        n=i+1
        #modelo='P5802450411'
        '''mysql query data'''
        #query_select_mysql='SELECT Button'+str(n)+'_Value FROM opcua_client_db.test_result ORDER BY Id DESC limit 50'
        query_select_mysql='SELECT Button'+str(n)+'_Value FROM opcua_client_db.test_result where test_result.Modelo="'+modelo+'" ORDER BY Id DESC limit 200'
        data=pd.read_sql(query_select_mysql,con=db)
        data.columns = ['valores']
        dataf=filtrar(data)

        '''mysql select modelos'''
        query_modelos_mysql="SELECT Button, tol_inf_n, tol_sup_n FROM modelos WHERE Button='Button"+str(n)+"_Value'"
        modelos=pd.read_sql(query_modelos_mysql,con=db)
        toli=modelos.iloc[0, 1]
        tols=modelos.iloc[0,2]
        cp_sql = cp(dataf, tols, toli)  # Tolerancias de la tabla modelos
        cpk_sql = cpk(dataf, tols, toli)
        fcpu = cpu(dataf, tols)
        fcpl = cpl(dataf, toli)
        mean = dataf['valores'].mean()
        mean = round(mean, 2)
        cp_sql=round(cp_sql,2)
        cpk_sql = round(cpk_sql, 2)
        fcpu=round(fcpu,2)
        fcpl=round(fcpl,2)
        print(fcpl,fcpl)
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
        print(type(mean))
        print(type(cpk_sql))
        print(date, Button, mean, toli, tols, (cp_sql), (cpk_sql))
        query_insert = "INSERT  opcua_client_db.results_cpk_ (Date,Button,Media,Tol_inf,Tol_sup,cp,cpk,modelo) VALUES ('"+str(date)+"','"+Button+"','"+str(mean)+"','"+str(toli)+"','"+str(tols)+"','"+str(cp_sql)+"','"+str(cpk_sql)+"','"+str(modelo)+"')"
        cursor=db.cursor()
        cursor.execute(query_insert)
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