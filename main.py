import urllib, urllib2
from bs4 import BeautifulSoup

loop = True
page = 1
propiedades = []
urlpropiedades = []
arrovent = ['arriendo','venta']
#arrovent = ['arriendo']
tipo = ['casa','departamento','oficina','sitio','comercial','industrial','agricola','loteo','bodega','parcela','estacionamiento','terreno-en-construccion']
#tipo = ['terreno-en-construccion']
#ciudad = ['metropolitana']
ciudad = ['arica-y-parinacota','atacama','biobio']
url = 'http://www.portalinmobiliario.com/arriendo/casa/santiago-metropolitana'
urlbase = 'http://www.portalinmobiliario.com'

print "Descargando lista de propiedades"

for arriendoventa in arrovent:
	for tip in tipo:
		for lugar in ciudad:
			while(loop):
				try:
					datos = urllib.urlencode({'ca':'3','ts':'1','mn':'2','or':'','sf':'0','sp':'0','at':'0','pg':str(page)})
					print "Descargando desde " + urlbase + '/' + arriendoventa + '/'+ tip + '/'+ lugar + '?' + datos
					web = urllib2.urlopen(urlbase + '/' + arriendoventa + '/'+ tip + '/'+ lugar + '?' + datos, timeout= 5)
					data = web.read()
					web.close()
					data = BeautifulSoup(data,'html.parser')
					propiedades += data.find_all('div',class_='propiedad')
					page = page + 1
					print 'Agregados ' + str(len(data.find_all('div',class_='propiedad'))) + ' datos'
					if len(data.find_all('div',class_='propiedad'))==0:
						page = 1
						loop = False
				except:
					print 'Problemas con URL, intentando nuevamente'
			loop = True

print ''
print 'Propiedades totales: ' + str(len(propiedades))
print ''

for propiedad in propiedades:
	urlpropiedades += [str(propiedad).split('href="')[1].split('"')[0].replace('amp;','')]

archivo = open('data.csv','w')
archivo.write('Nombre;Precio ($);Precio (UF);Codigo interno;Direccion;Superficie;Longitud;Latitud;Logo contacto;Nombre contacto;Direccion contacto;arriendo o venta;tipo;region;url')

page = 1
loop=True
for propiedad in urlpropiedades:
	loop=True
	while(loop):
		try:
			print 'Procesando propiedad: ' + str(page)
			web = urllib2.urlopen(urlbase + propiedad,timeout = 5)
			data = web.read()
			web.close
			data = BeautifulSoup(data,'html.parser')
		except:
			print "Problema de Timeout, intentando nuevamente"
		else:
			linea = ''
			#Nombre
			try:
				linea += str(data.find('h4',class_='media-block-title').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') +';'
			except:
				linea += ';'

			#Precio $ y UF
			try:
				linea += str(data.find('p',class_='price').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'
			try:
				linea += str(data.find('p',class_='price-ref').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'

			#Codigo interno
			try:
				linea += str(data.find('p',class_='operation-internal-code').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'

			#Direccion
			try:
				linea += str(data.find('div',class_='data-sheet-column-address').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'

			#Superficie
			try:
				linea += str(data.find('div',class_='data-sheet-column-area').get_text().encode('utf-8')).replace(';',',').replace('\n',' ').replace('Superficie ','') + ';'
			except:
				linea += ';'

			#Longitud y latitud
			try:
				for punto in data.find('div',class_='map-box').find_all('meta'):
					#linea += str(punto.get('itemprop').encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
					linea += str(punto.get('content').encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea +=';;'

			#Descripcion
			#linea += str(data.find('div',class_='propiedad-descr').get_text().encode('utf-8')).replace(';',',').replace('\n',' ').replace('\n',' ') + ';'

			#Datos de contacto
			#logo
			try:
				linea += urlbase + str(data.find('p',class_='operation-owner-logo').img.get('src').encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'
			#nombre
			try:
				linea += str(data.find('p',class_='operation-contact-name').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'
			#direccion
			try:
				linea += str(data.find('p',class_='operation-owner-address').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'

			#arriendo o venta
			linea += str(data.find('div',class_='property-title').ol.find_all('li')[1].get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'

			#tipo
			linea += str(data.find('div',class_='property-title').ol.find_all('li')[2].get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'

			#region
			linea += str(data.find('div',class_='property-title').ol.find_all('li')[3].get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'

			#url
			linea += urlbase + propiedad

			archivo.write(linea)

			page += 1
			loop=False

archivo.close()
