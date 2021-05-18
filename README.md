# QRCI-back-end

Bot calculo ckps maquina de fuerzas mMadrid

## Informacion
---

Esta aplicación recoge de la BBDD mysql en la 10.73.83.220 la información extraida de la máquina de fuezas con OPC client y calcula los cpks
El front end se puede acceder a traves de la URL: http://10.73.83.220/7qbs/

## Desarrollo
---

### Lenguajes:

* Python

### Desarrollada usando:

* PANDAS
* MATPLOTLIB
* mysql.connector

### BBDD:

* MySQL - 10.73.83.220@calidad.Pamp3701 - opcua_client_db


### Test de la API:

---

### Despliegue:


* Desplegada en:  `http://10.73.83.220/7qbs/`
* PM2: `10.73.82.219`

Para lanzarlo hay que abrir una consola y primero ejecutar el comando de abajo:

`PM2 ls`

Asi vemos si hay algun servicio ejecutandose
si no lanzar:
`PM2 start 1`

### Repositorios:

* Front end 
* Back end 

## Licencia
---
ISRI
## Organización
---
### Empresa ISRINGHAUSEN: 

ISRINGHAUSEN es una empresa con más de 50 años de experiencia en la fabricación de asientos para vehículos industriales. A día de hoy es suministrador de muchas de las principales marcas de automoción internacional.
