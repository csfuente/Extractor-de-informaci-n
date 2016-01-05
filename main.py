import urllib, urllib2
from bs4 import BeautifulSoup

loop = True
page = 1
propiedades = []
urlpropiedades = []
url = 'http://www.portalinmobiliario.com/arriendo/casa/santiago-metropolitana'
urlbase = 'http://www.portalinmobiliario.com'

print "Descargando informacion"

while(loop):
	datos = urllib.urlencode({'ca':'3','ts':'1','mn':'2','or':'','sf':'0','sp':'0','at':'0','pg':str(page)})
	print "Descargando desde " + url + '?' + datos
	web = urllib2.urlopen(url + '?' + datos)
	data = web.read()
	web.close()
	data = BeautifulSoup(data,'html.parser')
	propiedades += data.find_all('div',class_='propiedad')
	page = page + 1
	print 'Agregados ' + str(len(data.find_all('div',class_='propiedad'))) + ' datos'
	if len(data.find_all('div',class_='propiedad'))==0:
		loop=False

print ''
print 'Propiedades totales: ' + str(len(propiedades))
print ''

for propiedad in propiedades:
	urlpropiedades += [str(propiedad).split('href="')[1].split('"')[0].replace('amp;','')]

for propiedad in urlpropiedades:
	web = urllib2.urlopen(urlbase + propiedad)
	data = web.read()
	web.close
	data = BeautifulSoup(data,'html.parser')

	#Imprime longitud y latitud
	for punto in data.find('div',class_='map-box').find_all('meta'):
		print punto.get('itemprop')
		print punto.get('content')
