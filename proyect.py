import getopt
import sys
import re
import requests
import urllib
import urllib2
import mechanize

arg = ''
ip = ''
rep = ''
site = ''
var = ''
met = ''
h = ''
vers = ''
####Definicion de la funcion principal que solicita los parametros######
####Introducir los parametros en este orden: -s -R -r###################
def getParams(ip,site):
	try:
		opts, args = getopt.getopt(sys.argv[1:], 's:R:r:v:m:h', ['ip=', 'site=','report=','var=','method=','help'])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt,arg in opts:
		if opt in ('-s', '--ip'):
			ip = arg
			if(validaIp(ip) == False):
				print "Error, ip no validencia"
		elif opt in ('-R', '--site'):
			site = arg
####Parametros del reporte##############################################
		elif opt in ('-r', '--report'):
			writeFile(ip,site,rep=arg)
			code = (ip)
			code1= (site)
			code2=(getVersion())
###Validacion SQL INJECTION para HTML###################################			
			
			if(sqlInj(ip,site) == True):
				code3=('Recomendaciones para evitar SQL Injection:\n'
						 '-Parametrizar las consultas,\n'
						 '-Hacer uso de una cuenta con permisos restringidos para el acceso a la base de datos,\n'
						 '-No mostrar la informacion de error al usuario,\n'
						 '-Rechazar peticiones con caracteres sospechosos como: ; \' - \n')
			else:
				code3=('No es vulnerable a SQL Injection :,v\n')
###Validacion XSS HTML##################################################			
			if(xss(ip,site) == True):
				code4=('Recomendaciones para evitar Cross Site Scripting:\n'
						 '-Analizar y filtrar las entradas de datos,\n'
						 '-Codificar los datos no confiables basados en HTML,\n'
						 '-Uso de bibliotecas de sanitizacion del OWASP.\n')

			else:
				code4=('No es vulnerable a Cross Site Scripting:,v\n')
###Validacion HTML CSRF##################################################
			if(csrf(ip,site) == True):
				code5=('Recomendaciones para evitar Cross Site Request Forgery:\n'
						 '-Asegurarse que no existen vulnerabilidades XSS,\n'
						 '-Re-autenticar al usuario,\n'
						 '-Evitar hacer uso del metodo GET,\n'
						 '-Hacer uso de autenticaciones externas junto con el metodo POST\n')
			else:
				code5=('No es vulnerable a CSRF :,v\n')
###ValidacionHTML RFD###################################################			
			if(rfd(ip,site) == True):	
				code6=('Recomendaciones para evitar Remote File Disclosure:\n'
						 '-Verificar las peticiones que se realizan al servidor,\n'
					     '-Verificar los parametros mostrados en la URL,\n'
					     '-Verificar el manejo de cookies,\n')
			else:
				code6=('No es vulnerable a RFD :,v\n')		
###Construccion del HTML################################################					
			f = open('reporte.html','w')
			html = """\
				<html>
				  <head></head>
				  <body>
					<center> <p><h1>Reporte de vulnerabilidades</h1><br></center>
					 <center> <p><h2>Mamu content:</h2><br></center>
					   <h1><p>Direccion IP:<br></h1>
					   <br><br>{code}<br>
					   <h1>	<p>Recurso:<br></h1>
					   <br><br>{code1}<br>
					   <h1>	<p>Version Moodle:<br></h1>
					   <br><br>{code2}<br>
					   <h1>	<p>SQL Injection<br></h1>
					   <br><br>{code3}<br>
					   <h1><p>XSS<br></h1>
					   <br><br>{code4}<br>	
					   <h1><p>CSRF<br></h1>
					   <br><br>{code5}<br>
					   <h1>	<p>RFD<br></h1>
					   <br><br>{code6}<br>	 
					   <h1>	<p>Momazo<br></h1>rx
					   <img src="http://i2.esmas.com/galerias/fotos/2014/08/04/_f1f84c55_7c11_0ee4_74f8_04a66e44645d.jpg">
					</p>
				  </body>
				</html>
				""".format(code=code,code1=code1,code2=code2,code3=code3,code4=code4,code5=code5,code6=code6)
			f.write(html)
			f.close()
		
		elif opt in ('-v', '--var'):
			var = arg
			print var
			
		elif opt in ('-m', '--method'):
			met = arg			
			if(met.upper() == 'GET'):
				sqlInj(ip,site)
				xss(ip,site)
				rfd(ip,site)
				csrf(ip,site)
				
				
			elif met.upper() == 'POST':
				sqlInj(ip,site)
				xss(ip,site)
				rfd(ip,site)
				csrf(ip,site)
				
			else:
				print "Metodo no valido >:v"
				
		elif opt in ('-h', '--help'):
			h = arg
			ayuda()

		else:
			usage()
			sys.exit(2)
###Construccion del archivo txt#########################################
def writeFile(ip,site,rep):

	target = open(rep,'a')
	if(validaIp(ip) == True):
		target.write("IP: " + ip)
		target.write("\n")
		target.write("URL: " + site)
		target.write("\n")
		target.write("Version: ")
		target.write(getVersion())
		target.write("\n")
		target.write("\n")
		target.close()
		
		if(sqlInj(ip,site) == True):
			target = open(rep,'a')
			target.write('Recomendaciones para evitar SQL Injection:\n'
						 '-Parametrizar las consultas,\n'
						 '-Hacer uso de una cuenta con permisos restringidos para el acceso a la base de datos,\n'
						 '-No mostrar la informacion de error al usuario,\n'
						 '-Rechazar peticiones con caracteres sospechosos como: ; \' - \n')
			target.close()
		else:
			target = open(rep,'a')
			target.write('No es vulnerable a SQL Injection :,v\n')
			target.write('\n')
			target.close()
			
		if(xss(ip,site) == True):
			target = open(rep,'a')
			target.write('Recomendaciones para evitar Cross Site Scripting:\n'
						 '-Analizar y filtrar las entradas de datos,\n'
						 '-Codificar los datos no confiables basados en HTML,\n'
						 '-Uso de bibliotecas de sanitizacion del OWASP.\n')
			target.write('\n')
			target.close()
		else:
			target = open(rep,'a')
			target.write('No es vulnerable a Cross Site Scripting:,v\n')
			target.write('\n')
			target.close()
		
		if(csrf(ip,site) == True):
			target = open(rep,'a')
			target.write('Recomendaciones para evitar Cross Site Request Forgery:\n'
						 '-Asegurarse que no existen vulnerabilidades XSS,\n'
						 '-Re-autenticar al usuario,\n'
						 '-Evitar hacer uso del metodo GET,\n'
						 '-Hacer uso de autenticaciones externas junto con el metodo POST\n')
			target.write('\n')
			target.close()
		else:
			target = open(rep,'a')
			target.write	
			target.close()
			
		if(rfd(ip,site) == True):
			target = open(rep,'a')
			target.write('Recomendaciones para evitar Remote File Disclosure:\n'
						 '-Verificar las peticiones que se realizan al servidor,\n'
					     '-Verificar los parametros mostrados en la URL,\n'
					     '-Verificar el manejo de cookies,\n')
			target.write('\n')
			target.close()
		else:
			target = open(rep,'a')
			target.write('No es vulnerable a RFD :,v\n')
			target.close()
	else:
		print "No se escribio en el archivo, hubo un error en la ip >:v\n"
###Funcion de ayuda#####################################################
def ayuda():
	print('-s, --ip Ip del sitio a analizar, ejemplo: 127.0.0.1\n'
	'-r, --report Genera el reporte con el nombre del archivo, ejemplo: Reporte.txt\n'
	'-R, --site Recurso que se quiere analizar, ejemplo: index.php\n'
	'-v, --var Variable que se le va a pasar para realizar el ataque, ejemplo: alert("XSS")\n'
	'-m, --method Metodo con el que se hara la peticion, ejemplo: GET o POST\n'
	'-h, --help Muestra la ayuda para los comandos a ejecutar\n')

###Validacion de la IP##################################################	
def validaIp(ip):
	if len(ip.split()) == 1:
		ipList = ip.split('.')
		if len(ipList) == 4:
			for i, item in enumerate(ipList):
				try:
					#Para cuando tiene menos de 4 octetos o tiene algun caracter que no sea un numero
					ipList[i] = int(item)
				except:
					return False
				if not isinstance(ipList[i],int):
					return False
			if max(ipList) < 256:
				return True
			else:
				#Cuando el valor es mayor a 255
				return False
		else:
			#Cuando se introducen mas octetos de los permitidos
			return False
	else:
		#Cuando no se introduce nada :v
		return False

###Funcion para obetener la version del moodle##########################

def getVersion():
	s = requests.session()
	url = 'http://localhost/moodle/login/index.php'
	url1 = 'http://localhost/moodle/admin/index.php'
	payload = {'username':'admin','password':'Hola123.,'}
	r = s.post(url, data=payload)

	r1 = s.post(url1)

	vers = open('version.txt','w')
	vers.write(r1.content)
	vers.close()


	algo = open('version.txt',"r")
	for line in algo:
		versionencia = re.search(r'([0-9]\.){2}[0-9]{1,3}',line)
		if versionencia:
			return versionencia.group()
	algo.close()

###Funcion del SQL Injection############################################
def sqlInj(ip,site):
	#fullurl = ("localhost/moodle/index.php?")
	
	fullurl = ( ip +  site + '?')
	#print fullurl
	#fullurl = ("http://testphp.vulnweb.com/artists.php?artist")
	#resp = urllib2.Request(fullurl + "?artist=1\'")
	try:
		resp = urllib2.Request(fullurl + "=1\' or \'1\'=\'1\'")
		response = urllib2.urlopen(resp)
		body = response.read()
		
		if "Warning: mysql_fetch_array"  in body:
			#print ("SQL vulnerable!")
			return True
		elif "You have an error in your SQL syntax" in body:
			#print ("SQL vulnerable!")
			return True
		else:
			#print ("No es vulnerable a SQL Injection")
			return False
	except ValueError: 
			#print ("No es vulnerable a SQL Injection")
			return False
###Funcion XSS##########################################################
def xss(ip,site):
    try:
		url = 'http://' + ip  + site
		#url = "http://localhost/siteVuln/form.php"
		#url="http://localhost/moodle/login/index.php"
		#url = "http://www.webscantest.com/crosstraining/aboutyou.php"
		browser = mechanize.Browser()
		attackNumber = 1
		with open('XSS-vectors.txt') as f:
			for line in f:
				browser.open(url)
				browser.select_form(nr=0)
				browser["fname"] = line
				res = browser.submit()
				content = res.read()
				if content.find(line) > 0:
					#print "Possible XXS"
					return True
				else:
					#print "No vulnerable"
					return False
				print attackNumber
				attackNumber += 1
    except:
		#print "No vulnerable"
		return False
###Funcion RFD##########################################################

def rfd(ip,site):
	try:
		textfile = file('depth_1.txt','wt')
		myurl = 'http://' + ip  + site
		#myurl = ("http://localhost/moodle/login/admin/")
		for i in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(myurl).read(), re.I):
			if i.endswith('index.php'):
				#print "Eres vulnerable >:V en: " + i
				return True
			for ee in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(i).read(), re.I):
				textfile.write(ee+'\n')
				if ee.endswith('index.php'):
					#print "Eres vulnerable >:v en: " + ee
					return True
		textfile.close()

	except:
		#print "No vulnerable a RFD"
		return False
###Funcion CRSF#########################################################

def csrf(ip,site):
	try:
		s = requests.session()
		
		url = 'http://' + ip  + site
		
		#url = 'http://localhost/moodle/login/index.php'
		payload = {'username':'admin','password':'Hola123,'}
		r = s.post(url, data=payload)
	
		payloadfake = {'username' : 'meme', 'password' : 'pass'}
		r1 = s.post(url, data=payloadfake)
	
		word = 'not'
		if(word in r1.content):
			#print "No Vulnerable a CSRF >:v"
			return False
		else:
			#print "Vulnerable a CSRF"
			return True
	except:
		#print "No vulnerable a CSRF >:v"
		return False
		

getParams(ip,site)

