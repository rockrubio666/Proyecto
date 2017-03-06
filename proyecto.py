import getopt
import sys


ip = ''
rep = ''
site = ''
var = ''
met = ''
met = ''
h = ''


def getParams():
		try:
			opts, args = getopt.getopt(sys.argv[1:], 's:r:R:v:m:h', ['ip=', 'report=','site=','var=','method=','help'])
		except getopt.GetoptError:
			usage()
			sys.exit(2)
		for opt,arg in opts:
			if opt in ('-s', '--ip'):
				ip = arg
				print ip
			elif opt in ('-r', '--report'):
				rep = arg
				print rep
			elif opt in ('-R', '--site'):
				site = arg
				print site
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


def ayuda():
	print('-s, --ip 		Ip del sitio a analizar, ejemplo: 127.0.0.1\n'
		  '-r, --report 	Genera el reporte con el nombre del archivo, ejemplo: Reporte.txt\n'
		  '-R, --site		Recurso que se quiere analizar, ejemplo: index.php\n'
		  '-v, --var		Variable que se le va a pasar para realizar el ataque, ejemplo: alert("XSS")\n'
		  '-m, --method		Metodo con el que se hara la peticion, ejemplo: GET o POST\n'
		  '-h, --help 		Muestra la ayuda para los comandos a ejecutar\n')

getParams()

