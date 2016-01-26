# -*- coding: utf-8 -*-
import urllib, urllib2
from bs4 import BeautifulSoup
import time
import inspect


loop = True
page = 1
propiedades = []
destacados = []
urlpropiedades = []
urldestacados = []
#arrovent = ['arriendo','venta']
#arrovent = ['arriendo']
arrovent = ['venta']
#tipo = ['casa','departamento','oficina','sitio','comercial','industrial','agricola','loteo','bodega','parcela','estacionamiento','terreno-en-construccion']
#tipo = ['terreno-en-construccion']
tipo = ['departamento']
#tipo = ['casa']
ciudad = ['concepcion-biobio']
#ciudad = ['arica-y-parinacota','atacama','biobio']
#ciudad = ['arica-y-parinacota']
url = 'http://www.portalinmobiliario.com/arriendo/casa/santiago-metropolitana'
urlbase = 'http://www.portalinmobiliario.com'
intentos = 1


print "Descargando lista de propiedades"

for arriendoventa in arrovent:
	for tip in tipo:
		for lugar in ciudad:
			while(loop):
				cont = 0
				try:
					datos = urllib.urlencode({'ca':'3','ts':'1','mn':'2','or':'','sf':'0','sp':'0','at':'0','pg':str(page)})
					print "Descargando desde " + urlbase + '/' + arriendoventa + '/'+ tip + '/'+ lugar + '?' + datos
					web = urllib2.urlopen(urlbase + '/' + arriendoventa + '/'+ tip + '/'+ lugar + '?' + datos, timeout= 5)
					data = web.read()
					web.close()
					data = BeautifulSoup(data,'html.parser')
					propiedades += data.find_all('div',class_='propiedad')
					cont += len(data.find_all('div',class_='propiedad'))
					#destacados  += data.find_all('div',class_='proyecto')
					cont += len(data.find_all('div',class_='proyecto'))
					page = page + 1
					#print 'Agregados ' + str(len(data.find_all('div',class_='propiedad'))) + ' propiedades'
					print 'Agregados ' + str(len(data.find_all('div',class_='pagada'))) + ' proyectos'
					if cont==0:
						page = 1
						loop = False
					intentos = 1
					##time.sleep(5)
				except:
					print 'Problemas con URL, esperando ' + str(2**intentos)  +' segundos para reintentar'
					time.sleep(2**intentos)
					intentos += 1
			loop = True

print ''
print 'Propiedades totales: ' + str(len(propiedades))
#print 'Propiedades totales: ' + str(len(destacados))
print ''

for propiedad in propiedades:
	urlpropiedades += [str(propiedad).split('href="')[1].split('"')[0].replace('amp;','')]

for destacado in destacados:
	urldestacados  += [str(destacado).split('href="')[1].split('"')[0].replace('amp;','')]

archivo = open(inspect.stack()[0][1].split('.')[0]+'.csv','w')
archivo.write('Nombre;Precio ($);Precio (UF);Codigo interno;Direccion;Superficie;Longitud;Latitud;Logo contacto;Nombre contacto;Direccion contacto;arriendo o venta;tipo;region\n')

page = 1
loop=True
for propiedad in urlpropiedades:
	loop=True
	while(loop):
		try:
			print 'Procesando propiedad: ' + str(page)
			web = urllib2.urlopen(urlbase + propiedad,timeout = 5)
			data = web.read()
			web.close()
			data = BeautifulSoup(data,'html.parser')
			intentos = 1
		except:
			print "Problema de Timeout, se intentara en "+ str(2**intentos)  +" segundos"
			time.sleep(2**intentos)
			intentos +=1
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
			linea += str(data.find('div',class_='property-title').ol.find_all('li')[3].get_text().encode('utf-8')).replace(';',',').replace('\n',' ')

			#url
			#linea += urlbase + propiedad

			archivo.write(linea+'\n')

			page += 1
			loop=False
			#time.sleep(5)

page = 1
loop = True
for destacado in urldestacados:
	loop = True
	while(loop):
		try:
			print 'Procesando proyecto: ' + str(page)
			web = urllib2.urlopen(urlbase + destacado,timeout = 5)
			data = web.read()
			web.close()
			data = BeautifulSoup(data,'html.parser')
		except:
			print "Problema de Timeout, intentando nuevamente"
		else:
			linea = ''
			#Nombre
			try:
				linea += str(data.find('div',class_='prj-name').h1.get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'
			#Precio $ y UF, Solo precios en UF para proyectos
			try:
				linea += ';' + str(data.find('div',class_='prj-price-range').get_text().encode('utf-8')).replace(';',',').replace('\n',' ').split('   ')[-1] + ';'
			except:
				linea += ';;'

			#Codigo interno
			try:
				linea += str(data.find('span',class_='prj-code').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'
			#Direccion
			try:
				linea += str(data.find('p',class_='prj-map-addr-obj').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea += ';'
			#Superficie
			try:
				linea += str(data.find_all('span',class_='project-feature-details')[3].get_text().encode('utf-8')).replace(';',',').replace('\n',' ').replace('Superficie ','') + ';'
			except:
				linea += ';'
			#Longitud y latitud
			try:
				linea += data.find('meta',property='og:longitude').get('content').encode('utf-8') + ';'
				linea += data.find('meta',property='og:latitude').get('content').encode('utf-8') + ';'
				#linea += str(data.find(attrs={'property':'og:longitude'}).get('content').encode('utf.8')).replace(';',',').replace('\n',' ') + ';'
				#linea += str(data.find(attrs={'property':'og:latitude'}).get('content').encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
			except:
				linea +=';;'
			#Descripcion
			#linea += str(data.find('div',class_='propiedad-descr').get_text().encode('utf-8')).replace(';',',').replace('\n',' ').replace('\n',' ') + ';'

			#Datos de contacto
			#logo
			try:
				#linea += urlbase + str(data.find('div',class_='col-md-3 col-sm-3').img.get('src').encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
				linea += ';'
			except:
				linea += ';'
			#nombre
			try:
				linea += str(data.find('div',class_='prj-other-info-items').findAll('div')[1].get_text().encode('utf-8')).replace(';',',').replace('\n',' ').replace('Acerca de ','') + ';'
			except:
				linea += ';'
			#direccion
			try:
				#linea += str(data.find('p',class_='operation-owner-address').get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'
				linea += ';'
			except:
				linea += ';'
			#arriendo o venta
			linea += str(data.find('div',class_='prj-bcrumbs').find_all('span')[1].get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'

			#tipo
			linea += str(data.find('div',class_='prj-bcrumbs').find_all('span')[3].get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'

			#region
			linea += str(data.find('div',class_='prj-bcrumbs').find_all('span')[5].get_text().encode('utf-8')).replace(';',',').replace('\n',' ') + ';'

			archivo.write(linea+'\n')

			page += 1
			loop=False

	
archivo.close()
