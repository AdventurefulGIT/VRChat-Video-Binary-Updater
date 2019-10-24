from termcolor import colored
from colorama import init
import win32api
import requests
import winreg
import re

class VRChatStreaming:
	def __init__(self):
		init()
		self.steamPath = self.getSteamInstallFolder()
		self.streaming = self.getFileVersion(self.steamPath)
		self.latest    = self.getLatestVersion()
		self.setup()
	def getFileVersion(self, fname):
		try:
			fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
			version = "%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
					fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536)
			return version
		except:
			return False

	def getLatestVersion(self):
		try:
			r = requests.get('https://youtube-dl.org/')
			regex = re.compile('\(v(.*)\) downloads')
			return regex.findall(r.text)[0]
		except:
			return self.getLatestVersion()
	def getSteamInstallFolder(self):
		print('[' + colored('!', 'cyan') + colored('] Attempting to find steam folder', 'white'))
		try:
			key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam")
		except:
			try:
				key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software\\Valve\\Steam")
			except:
				print('[' + colored('!', 'red') + colored("] We couldn't find the path to your steam folder, please enter it manually...", 'white'))
				path = str(input('> ')+ '/steamapps/common/VRChat/VRChat_Data/StreamingAssets/youtube-dl.exe')
				print('')
				return path
		return str(winreg.EnumValue(key, 1)[1]).replace('/steam.exe', '') + '/steamapps/common/VRChat/VRChat_Data/StreamingAssets/youtube-dl.exe'

	def downloadUpdate(self, path):
		r = requests.get('https://youtube-dl.org/downloads/latest/youtube-dl.exe')
		open(path, 'wb').write(r.content)
		return True

	def setup(self):
		if self.steamPath:
			print('[' + colored('!', 'cyan') + colored('] Steam file path found', 'white'))
			if self.streaming:
				print('[' + colored('!', 'cyan') + colored('] youtube-dl.exe found', 'white'))
				if str(self.streaming) == str(self.latest):
					return print('[' + colored('!', 'green') + colored('] youtube-dl.exe is up to date!', 'white'))		
		print('\n[' + colored('!', 'yellow') + colored('] Looks like youtube-dl.exe had issues, updating...', 'white'))
		if self.downloadUpdate(self.steamPath):
			return print('[' + colored('!', 'green') + colored('] youtube-dl.exe is up to date!', 'white'))


VRChatStreaming()
input('\nPress ENTER to close the program.')
