#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import os
import codecs
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime
import time
import winsound
import random
import newprocess
import json
from threading import Timer
import urllib


clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer


class Settings(object):
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.humbleName = ""

	def reload(self, jsonData):
		self.__dict__ = json.loads(jsonData, encoding="utf-8")


#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Humble Script"
Website = "https://www.twitch.tv/SmartASCII"
Description = "Link directly to the game you're playing with your partner account"
Creator = "SmartASCII"
Version = "1.0.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------


global m_scriptDir
m_scriptDir = ""
global m_partnerName
m_partnerName = ""

SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
ScriptSettings = None

def ReloadSettings(jsonData):
	# Execute json reloading here
	global m_partnerName
	
	Parent.Log("humbleScript","Settings reloaded")
	ScriptSettings.reload(jsonData)
	m_partnerName = ScriptSettings.humbleName
	return
	
def Init():
	
	m_scriptDir = os.path.join(os.getcwd(),"Services","Scripts",ScriptName)
	m_scriptDir = m_scriptDir.replace("\\","\\")
	
	# Globals
	global ScriptSettings
	global m_partnerName

	# Load saved settings and validate values
	ScriptSettings = Settings(SettingsFile)
	
	m_partnerName = ScriptSettings.humbleName
	return
	
def callback(jsonString):
	return
#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------

		
def pageFound(strPage):
	result = Parent.GetRequest("http://www.humblebundle.com/store/" + strPage,{})
	jsonResult = json.loads(result)
	status = jsonResult['status']
	if status == 404:
		return False
	return True
def humbleSearch(strTerm):
	return
def sanitize(strTitle):
	strTitle = strTitle.replace(" ","-")
	strTitle = strTitle.replace("'","")
	strTitle = strTitle.replace(":","")
	strTitle = strTitle.replace("!","")
	strTitle = strTitle.replace("?","")
	return urllib.quote(strTitle.lower())

   
def Execute(data):

	if data.IsChatMessage():
	
		if data.GetParam(0).lower() == "!humble":
			if len(m_partnerName) == 0:
				Parent.SendStreamMessage("This script is enabled but a partner name has not been set! Please check script settings.")
				return
			rawInput = data.Message.replace("!humble", "")
			rawInput = rawInput.strip()
			searchFor = sanitize(rawInput)
			if len(searchFor) > 0:
				#Search by title
				if pageFound(searchFor):
					#Found exact match
					Parent.SendStreamMessage("Buy using " + Parent.GetChannelName() + "'s partner link and help support the channel! " + "http://www.humblebundle.com/store/" + searchFor + "?partner=" + m_partnerName)
				else:
					Parent.SendStreamMessage("Exact match not found. Maybe try a search? https://www.humblebundle.com/store/search?sort=bestselling&search=" + urllib.quote(rawInput) + "&partner=" + m_partnerName)
					
			else:
				#Search by current category
				theGame = Parent.GetRequest("https://api.crunchprank.net/twitch/game/" + Parent.GetChannelName(),{})
				response = json.loads(theGame)
				theGame = response['response']
				if pageFound(sanitize(theGame)):
					#Found exact match
					Parent.SendStreamMessage("Buy using " + Parent.GetChannelName() + "'s partner link and help support the channel! " + "http://www.humblebundle.com/store/" + sanitize(theGame) + "?partner=" + m_partnerName)
				else:
					Parent.SendStreamMessage("Exact match not found. Maybe try a search? https://www.humblebundle.com/store/search?sort=bestselling&search=" + urllib.quote(theGame) + "&partner=" + m_partnerName)
			
			return
			
		
		
	return
 
 
#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
 return
 