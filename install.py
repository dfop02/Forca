#-*- coding: utf-8 -*-
import os, time, stat
from shutil import copy

#################### IMPORTANT ####################

# Principal arquivo do seu programa
main = "menu.py"
# Pacotes necessario para seu programa funcionar
deps = ["string", "random", "pygame"]
# Nome do seu programa (Nome do atalho na area de trabalho)
name = "Jogo da Forca"
# Comentario no atalho (Opicional)
comment = "Jogo da Forca"

##################################################

def getVersion():
	with open("version.txt", "r") as v:
		for x in v: return x.split("=")[-1]

def getPath():
	return os.path.dirname(os.path.abspath(__file__))

def checkUser(path, root):
	routesPath = path.split('/')
	routesRoot = root.split('/')
	if routesPath[2] != routesRoot[2]:
		realRoot = "/" + routesRoot[1] + "/" + routesPath[2] + "/" + routesRoot[3]
		return realRoot
	else:
		return root

def setPythonFile():
	pythonExe = "#!/usr/bin/env python\n"
	exe = True
	with open(main, "r+") as py:
		firstLine = py.readlines()
		for lines in firstLine:		
			if not pythonExe == lines:
				exe = False
				firstLine.insert(0,pythonExe)
				break
			else:
				break
	if not exe:
		with open(main, "w") as py:
			print ("Adicionando comando ao arquivo .py")
			py.writelines(firstLine)

def turnRun(File):
	try:
		st = os.stat(File)
		# Torna o arquivo executavel
		os.chmod(File, st.st_mode | stat.S_IEXEC)
		# Caso instale por outro usuario, da a permissao necessaria
		os.chmod(File, 0o777)
	except IOError as error:
		print (error)

def install(package):
	import importlib
	try:
		importlib.import_module(package)
		print (package + " ja instalado.")
	except ImportError:
		try:
			print (package + " nao instalado. Instalando...")
			import pip
			if float(pip.__version__) < 18.0:
				print ("Seu pip esta desatualizado...")
				print ("Atualizando seu pip do " + pip.__version__ + " para o 18.0")
				os.system('sudo pip install -U pip')
			os.system('sudo pip install ' + package)
		except ImportError:
			try:
				print ("Pip nao instalado... Instalando...")
				# Instala o pip 1.5 e depois atualiza para o pip 18.0
				os.system('sudo apt install python-pip && sudo pip install -U pip')
			except:
				print ("Erro ao instalar o pip.")
			finally:
				import pip
				print ("Tentando novamente... Instalando " + package + "...")
				os.system('sudo pip install ' + package)

def installDeps():
	# As Deps sao declaradas la no comeco
	for lib in deps:
		install(lib)

def createShortcut(path, version, currentRoot):
	os.chdir(currentRoot)
	with open(name + ".desktop", "w") as shortcut:
		shortcut.write("[Desktop Entry]\n")
		shortcut.write("Version=" + version + "\n")
		shortcut.write("Name=" + name + "\n")
		shortcut.write("Comment=" + comment + "\n")
		shortcut.write("Exec=" + path + "/" + main + "\n")
		shortcut.write("Icon=" + path + "/img/icon.png\n")
		shortcut.write("Type=Application\n")
		shortcut.write("Terminal=false")
	try:
		copy(getPath() + "/" + name + ".desktop", os.path.expanduser('~/.local/share/applications'))
	except IOError as error:
		print (error)
	turnRun(name + ".desktop")

if __name__ == '__main__':
	# Forca diretorio
	forcaDir = getPath()
	# Root diretorio
	root = os.path.join(os.path.join(os.path.expanduser('~')), 'Área de Trabalho')
	if not os.path.isdir(root):
		root = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
	# Corrige o root caso tente instalar por outro usuario...
	currentRoot = checkUser(forcaDir, root)

	print ("Instalando Jogo da Forca...")
	print ("Procurando pacotes pendentes...")
	installDeps()

	print ("Tornando o arquivo executavel...")
	setPythonFile()
	turnRun(main)

	print ("Criando um atalho na area de trabalho...")
	try:
		print ("Configurando atalho...")
		createShortcut(getPath(), getVersion(), currentRoot)
		print ("Arquivo criado com sucesso!")
	except IOError as error:
		print (error)

	print ("Instalacao concluida!")
