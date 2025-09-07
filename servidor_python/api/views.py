from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

import django.http
import json
import pyodbc

## Conectarse al servidor SQL
SERVER_NAME = "DESKTOP-CDJCAV7\SQLEXPRESS"
SQL_DRIVER = "{ODBC Driver 17 for SQL Server}"
DATABASE_NAME = "tarea_1_db"

## usamos los credenciales de la maquina porque siempre viven en la misma compu
conn = pyodbc.connect("DRIVER={};SERVER={};DATABASE={};Trusted_Connection=yes;Encrypt=no;".format(
	SQL_DRIVER, SERVER_NAME, DATABASE_NAME
))
crsr = conn.cursor()

## Codigo que llama a los stored procedures
sp_query = """
EXEC [dbo].[sp_Query_Empleados];
"""

## en este caso, los DECLARE y SELECT nos permiten obtener el valor de retrno
## del stored procedure
sp_insertar = """
SET NOCOUNT ON;
DECLARE @rv int;

EXEC @rv = [dbo].[sp_Insertar_Empleado] ?, ?;

SELECT @rv AS return_value;
"""

@ensure_csrf_cookie
def index(request):
	## Si es un get simplemente hace un query, lo formatea y lo retorna como JSON
	if(request.method == "GET"):
		# hacer query a la base de datos
		crsr.execute(sp_query)
		rows = crsr.fetchall()

		empleados_plain = []
		for row in rows:
			empleados_plain.append({
				"Id": row[0],
				"Nombre": row[1],
				"Salario": float(row[2])
			})

		return django.http.HttpResponse(json.dumps({
			"state": "OK",
			"description": "Los empleados fueron consultados correctamente",
			"empleados": empleados_plain
		}))
	
	## Si es un post entonces revisamos que tenga el formato correcto
	elif(request.method == "POST"):
		print(request.body)
		post_body = json.loads(request.body)
		## si no trae los datos necesarios lo descartamos y retornamos un error
		if("Nombre" not in post_body or "Salario" not in post_body):
			return django.http.HttpResponse(json.dumps({
				"state": "ERROR",
				"description": "Metodo POST con body incorrecto",
			}))
		

		## de otra manera, corremos el stored procedure y esperamos una respuesta
		crsr.execute(sp_insertar, (post_body["Nombre"], post_body["Salario"]))

		if(crsr.fetchval() == 0):
			crsr.commit()
			return django.http.HttpResponse(json.dumps({
				"state": "OK", 
				"description": "Resultado de la inserscion de un empleado",
			}))
		
		else:
			crsr.rollback()
			return django.http.HttpResponse(json.dumps({
				"state": "ERROR",
				"description": "Nombre de empleado ya existe",
			}))
