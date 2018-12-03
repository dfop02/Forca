#-*- coding: utf-8 -*-
import os, sys, stat
from shutil import copy

#################### IMPORTANT ####################

# Principal arquivo do seu programa
main = "menu.py"
# Pacotes necessario para o instalador funcionar
deps = ["pipreqs"]
# Nome do seu programa (Nome do atalho na area de trabalho)
name = "Jogo da Forca"
# Comentario no atalho (Opicional, apenas para Linux)
comment = "Jogo da Forca"
# Imagem do icone do jogo precisa estar em formado .png e na pasta img
icon = "icon.png"

##################################################

def getPythonVersion():
	return sys.version_info

def getVersion():
	with open("version.txt", "r") as v:
		for x in v: return x.split("=")[-1]

def getPath():
	return os.path.dirname(os.path.abspath(__file__))

def checkUser():
	system = getSystem()
	# Forca diretorio
	forcaDir = getPath()
	# Desktop diretorio
	root = os.path.join(os.path.join(os.path.expanduser('~')), 'Área de Trabalho')
	if not os.path.isdir(root):
		root = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

	if system == "Windows":
		routesPath = forcaDir.split('//')
		routesRoot = root.split('//')
	else:
		routesPath = forcaDir.split('/')
		routesRoot = root.split('/')

	if routesPath[2] != routesRoot[2]:
		if system == "Windows":
			realRoot = "//" + routesRoot[1] + "//" + routesPath[2] + "//" + routesRoot[3]
		else:
			realRoot = "/" + routesRoot[1] + "/" + routesPath[2] + "/" + routesRoot[3]
		return realRoot
	else:
		return root

def setPythonFile():
	python2Exe = "#!/usr/bin/env python\n"
	python3Exe = "#!/usr/bin/env python3\n"
	macPython2 = "#!/usr/local/bin/python"
	macPython3 = "#!/usr/local/bin/python3"
	system = getSystem()
	exe = True
	with open(main, "r+") as py:
		firstLine = py.readlines()
		for lines in firstLine:
			if system == 'Linux':
				if not python2Exe == lines or python3Exe == lines:
					exe = False
					if getPythonVersion() >= (3,0):
						firstLine.insert(0,python3Exe)
					else:
						firstLine.insert(0,python2Exe)
					break
				else:
					break
			elif system == 'Darwin':
				if not macPython2 == lines or macPython3 == lines:
					exe = False
					if getPythonVersion() >= (3,0):
						firstLine.insert(0,macPython3)
					else:
						firstLine.insert(0,macPython2)
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
	except OSError as error:
		print (error)
		print ("Erro de permissao... Instalacao abortada.")
		exit()

def getPipVersion():
	import pip
	vers = ''
	for x in pip.__version__.split('.'): 
		if x != pip.__version__.split('.')[-1]: 
			vers += x + '.'
	return float(vers[:-1])

def searchPkg(path):
	if os.path.isfile(path + "/requirements.txt"):
		os.system("pipreqs --force" + path)
	else:
		os.system("pipreqs " + path)

def installPkg():
	system = getSystem()
	if system == 'Linux':
		os.system("sudo pip3 install -r requirements.txt")
	else:
		os.system("pip3 install -r requirements.txt")

def install(package):
	import importlib
	system = getSystem()
	try:
		importlib.import_module(package)
		print (package + " ja instalado.")
	except ImportError:
		try:
			print (package + " nao instalado. Instalando...")
			import pip
			print (getPipVersion())
			if (getPipVersion() < 18.0):
				print ("Seu pip esta desatualizado...")
				print ("Atualizando seu pip do " + pip.__version__ + " para o 18.0")
				if system == 'Linux':
					if getPythonVersion() >= (3,0):
						os.system('sudo pip3 install -U pip')
						os.system('sudo pip3 install ' + package)
					else:
						os.system('sudo pip install -U pip')
						os.system('sudo pip install ' + package)
				elif system == 'Darwin' or system == 'Windows':
					if getPythonVersion() >= (3,0):
						os.system('pip3 install -U pip')
						os.system('pip3 install ' + package)
					else:
						os.system('pip install -U pip')
						os.system('pip install ' + package)					
			else:
				if system == 'Linux':
					if getPythonVersion() >= (3,0):
						os.system('sudo pip3 install ' + package)
					else:
						os.system('sudo pip install ' + package)
				elif system == 'Darwin' or system == 'Windows':
					if getPythonVersion() >= (3,0):
						os.system('pip3 install ' + package)
					else:
						os.system('pip install ' + package)
			importlib.reload(pip)
			print (getPipVersion())
			if (getPipVersion() < 18.0):
				print ("Falha ao atualizar o pip... Instalacao abortada.")
				exit()
		except ImportError:
			try:
				print ("Pip nao instalado... Instalando...")
				if system == 'Linux':
					if getPythonVersion() >= (3,0):
						os.system('sudo apt-get install python3-pip && sudo pip3 install -U pip')
					else:
						os.system('sudo apt-get install python-pip && sudo pip install -U pip')
				elif system == 'Windows':
					print('Not implemented yet.')
				elif system == 'Darwin':
					if getPythonVersion() >= (3,0):
						os.system('brew install python3 && pip3 install -U pip')
					else:
						os.system('brew install python && pip install -U pip')
			except IOError as error:
				print (error)
				print ("Erro ao instalar o pip... Instalacao abortada.")
				exit()
			finally:
				import pip
				print ("Tentando novamente... Instalando " + package + "...")
				if system == 'Linux':
					if getPythonVersion() >= (3,0):
						os.system('sudo pip3 install ' + package)
					else:
						os.system('sudo pip install ' + package)
				elif system == 'Darwin' or system == 'Windows':
					if getPythonVersion() >= (3,0):
						os.system('pip3 install ' + package)
					else:
						os.system('pip install ' + package)

def installDeps():
	# As Deps sao declaradas la no comeco
	print ("Procurando pacotes pendentes...")
	for lib in deps:
		install(lib)

def getSystem():
	import platform
	return platform.system()

def createShortcut(path, version, currentRoot):
	os.chdir(currentRoot)
	system = getSystem()

	if system == 'Linux':
		with open(name + ".desktop", "w") as shortcut:
			shortcut.write("[Desktop Entry]\n")
			shortcut.write("Version=" + version + "\n")
			shortcut.write("Name=" + name + "\n")
			shortcut.write("Comment=" + comment + "\n")
			shortcut.write("Exec=" + path + "/" + main + "\n")
			shortcut.write("Icon=" + path + "/img/" + icon + "\n")
			shortcut.write("Type=Application\n")
			shortcut.write("Terminal=false")
		try:
			copy(getPath() + "/" + name + ".desktop", os.path.expanduser('~/.local/share/applications'))
		except IOError as error:
			print (error)
			print ("Erro de permissao... Instalacao abortada.")
			exit()
		turnRun(name + ".desktop")

	elif system == 'Darwin':		
		createMacApp(path)		
		turnRun(name + ".command")

	elif system == 'Windows':
		print('System desktop file not implemented yet.')

def createMacApp(path):
	with open(name + ".command", "w") as shortcut:
		shortcut.write("#!/bin/sh\npython3 " + path + "/" + main)

if __name__ == '__main__':
	# Corrige o path caso tente instalar por outro usuario...
	currentRoot = checkUser()
	print ("Instalando dependencias do instalador...")
	installDeps()
	print ("Instalando " + name + "...")
	searchPkg(getPath())
	installPkg()

	print ("Tornando o arquivo executavel...")
	setPythonFile()
	turnRun(main)

	print ("Criando um atalho na area de trabalho...")
	try:
		print ("Configurando atalho...")
		createShortcut(getPath(), getVersion(), currentRoot)
	except IOError as error:
		print (error)
		print ("Erro de permissao... Instalacao abortada.")
		exit()
	print ("Arquivo criado com sucesso!")
	print ("Instalacao concluida!")
