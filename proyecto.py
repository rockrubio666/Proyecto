#Introducir los parametros en este orden: -s -R -r
#Si no manda error por el archivencio :,v
import getopt
import sys
import os.path 
import re


arg = ''
ip = ''
rep = ''
site = ''
var = ''
met = ''
h = ''
vers = ''
code = ''

def getParams():
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
			
		elif opt in ('-r', '--report'):
			writeFile(ip,site,rep=arg)
			code = (ip)
			code1= (site)
			f = open('reporte.html','w')
			html = """\
				<html>
				  <head></head>
				  <body>
					<center> <p><h1>Reporte de vulnerabilidades</h1><br></center>
					 <center> <p><h2>Mamu content:</h2><br></center>
					   <p>Direccion IP:<br>
					   <br><br><h1>{code}</h1><br>
					   <p>Recurso:<br>
					   <br><br><h1>{code1}</h1><br>
					   <p>Momazo<br>
					   <img src="http://i2.esmas.com/galerias/fotos/2014/08/04/_f1f84c55_7c11_0ee4_74f8_04a66e44645d.jpg">
					</p>
				  </body>
				</html>
				""".format(code=code,code1=code1)
			f.write(html)
			f.close()
			
		
		elif opt in ('-v', '--var'):
			var = arg
			print var
			
		elif opt in ('-m', '--method'):
			met = arg
			print met

		elif opt in ('-h', '--help'):
			h = arg
			ayuda()

		else:
			usage()
			sys.exit(2)

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
	else:
		print "No se escribio en el archivo, hubo un error en la ip >:v"
		
		
	
	

def ayuda():
	print('-s, --ip Ip del sitio a analizar, ejemplo: 127.0.0.1\n'
	'-r, --report Genera el reporte con el nombre del archivo, ejemplo: Reporte.txt\n'
	'-R, --site Recurso que se quiere analizar, ejemplo: index.php\n'
	'-v, --var Variable que se le va a pasar para realizar el ataque, ejemplo: alert("XSS")\n'
	'-m, --method Metodo con el que se hara la peticion, ejemplo: GET o POST\n'
	'-h, --help Muestra la ayuda para los comandos a ejecutar\n')

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


def getVersion():
	archivo = '/var/www/html/moodle/version.php'

	if (os.path.exists(archivo)) == True:
		algo = open(archivo,"r")
		for line in algo:
			vers = re.search(r'([0-9]\.){2}[0-9]{1,3}',line)
			if vers:
				return vers.group()
	else:
		print "Nio existe el archivo"

getParams()
