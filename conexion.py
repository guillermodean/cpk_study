import mysql.connector as mysql

def conexion():
    try:
        db = mysql.connect(host='10.73.83.220', user='calidad', password='Pamp3701', db='opcua_client_db')

    except mysql.Error as err:
        print ('error de conexion ala BBDD'+str(err))
    return db