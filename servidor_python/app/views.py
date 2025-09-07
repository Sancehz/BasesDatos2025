from django.shortcuts import render
import django.http
from pathlib import Path

def index(request):
	## simplemente se busca el archivo html y se sirve como texto al browser
	html_filepath = Path(__file__) / "../../../presentacion_web/index.html"
	html_content = ""
	with open(html_filepath) as f:
		html_content = f.read()

	return django.http.HttpResponse(html_content)

#teccr123123bdatos