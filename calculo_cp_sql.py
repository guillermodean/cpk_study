import math
import datetime
from helpers.calculos import cp, cpk, cpl, cpu
from helpers.interfaz import introducemodelo, modelovar
from helpers.query import querys
from helpers.conexion import conexion
from helpers.getdata import getdata
from helpers.graficar import graficar
import time
while True:
    #introducemodelo()
    #modelo = modelovar()
    modelo='' # salto la interfaz para introducir el modelo cogiendo todos dejando la variable modelo en blanco.
    db=conexion()

    try:
        for i in range(13):
            n = i + 1
            dataf,toli,tols,modelos,data= getdata(n, db, modelo)
            cp_sql = cp(dataf, tols, toli)  # Calcular cpks
            cpk_sql = cpk(dataf, tols, toli)
            fcpu = cpu(dataf, tols)
            fcpl = cpl(dataf, toli)
            mean = dataf['valores'].mean()
            mean = round(mean, 2)
            cp_sql = round(cp_sql, 2)
            cpk_sql = round(cpk_sql, 2)
            fcpu = round(fcpu, 2)
            fcpl = round(fcpl, 2)
            Button = modelos.iloc[0, 0]

            if math.isnan(mean):
                mean = 0
            if math.isnan(cp_sql):
                cp_sql = 0
            if math.isnan(cpk_sql):
                cpk_sql = 0
            date = datetime.datetime.now()
            cp_sql = float(cp_sql)
            cpk_sql = float(cpk_sql)
            print(date, Button, mean, toli, tols, cp_sql, cpk_sql)

            """Guardar los datos en la tabla results cpk"""

            query_insert = "INSERT  opcua_client_db.results_cpk_ (Date,Button,Media,Tol_inf,Tol_sup,cp,cpk,modelo) VALUES " \
                           "('" + str(
                date) + "','" + Button + "','" + str(mean) + "','" + str(toli) + "','" + str(tols) + "','" + str(
                cp_sql) + "','" + str(cpk_sql) + "','" + str(modelo) + "')"
            query_insert_nm = "INSERT  opcua_client_db.results_cpk_ (Date,Button,Media,Tol_inf,Tol_sup,cp,cpk,modelo) " \
                              "VALUES ('" + str(
                date) + "','" + Button + "','" + str(mean) + "','" + str(toli) + "','" + str(tols) + "','" + str(
                cp_sql) + "','" + str(cpk_sql) + "','todos')"
            query = querys(modelo, query_insert, query_insert_nm)
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            recuento = len(dataf['valores'])

            """graficar"""

            graficar(mean, Button, cpk_sql, cp_sql, recuento, dataf, data, toli, tols, fcpl, fcpu, n)


        print('endoflines')
        time.sleep(86400)
    except:
        print('error total')
