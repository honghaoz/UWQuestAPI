from bs4 import BeautifulSoup
import re

################# Parser ################

# def Parse_personalInfo_menu():
# 	pass

# Return ['Address Type', 'Address', 
#	'Home', '101-137 UNIVERSITY AVE. W, WATERLOO Ontario N2L 3E6', 
#	'Mail', '101-137 UNIVERSITY AVE. W, WATERLOO Ontario N2L 3E6']
def Parse_personalInfo_address(html):
	soup = BeautifulSoup(html)

	# addressTable contains address information
	addressTable = soup.find(id="SCC_ADDR_H$scroll$0")

	# Clean tags
	tableString = str(addressTable)
	x = re.sub("\<.*?\>", "", tableString);
	# clean result list
	resultList = filter(lambda x: len(x) > 0, x.replace(" \r", ", ").split("\n"))
	print "le: " + str(len(resultList[2]))
	del(resultList[2])
	# resultList contains
	return resultList

def Parse_personalInfo_name(html):
	soup = BeautifulSoup(html)
	nameTable = soup.find(id="SCC_NAMES_H$scroll$0")

	# Clean tags
	tableString = str(nameTable)
	x = re.sub("\<.*?\>", "", tableString);
	# clean result list
	resultList = filter(lambda x: len(x) > 0, x.replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n"))
	return resultList

################# API ################

# Passed in meta and data dictionary and return full response dictionary
def getFullResponseDictionary(meta, data):
	return {"meta": meta, "data": data}

def getEmptyMetaDict():
	return {"status": "", "message": ""}

# Return acount login response dictionary
def API_account_loginResponse(questSession):
	meta = getEmptyMetaDict()
	data = {}
	if questSession.isLogin:
		meta["status"] = "success"
		data["sid"] = questSession.icsid
	else:
		meta["status"] = "failure"
		meta["message"] = questSession.currentError
	return getFullResponseDictionary(meta, data)

def API_account_logoutResponse(questSession):
	meta = getEmptyMetaDict()
	data = {}
	# TODO: complete logout call

def API_personalInfo_addressResponse(questSession):
	addressList = Parse_personalInfo_address(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if not len(addressList) < 2:
		meta["status"] = "success"
		addressCount = (len(addressList) - 2) / 2
		for i in xrange(0, addressCount):
			addressDict = {}
			addressDict["address_type"] = addressList[(i + 1) * 2]
			addressDict["address"] = addressList[(i + 1) * 2 + 1]
			data.append(addressDict)
			# addressDict[addressList[(i + 1) * 2]] = addressList[(i + 1) * 2 + 1]
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no address information"
	return getFullResponseDictionary(meta, data)

def API_personalInfo_nameResponse(questSession):
	nameList = Parse_personalInfo_name(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if not len(nameList) < 6:
		meta["status"] = "success"
		nameCount = len(nameList) / 6 - 1
		for i in xrange(0, nameCount):
			nameDict = {}
			nameDict["name_type"] = nameList[(i + 1) * 6]
			nameDict["name_prefix"] = nameList[(i + 1) * 6 + 1]
			nameDict["first_name"] = nameList[(i + 1) * 6 + 2]
			nameDict["middle_name"] = nameList[(i + 1) * 6 + 3]
			nameDict["last_name"] = nameList[(i + 1) * 6 + 4]
			nameDict["name_suffix"] = nameList[(i + 1) * 6 + 5]
			data.append(nameDict)
			# addressDict[addressList[(i + 1) * 2]] = addressList[(i + 1) * 2 + 1]
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no name information"
	return getFullResponseDictionary(meta, data)