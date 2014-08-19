from bs4 import BeautifulSoup
import re

################# Parser ################

# def Parse_personalInfo_menu():
# 	pass


# Add new key for description
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
	del(resultList[2])
	# resultList contains
	return resultList

# Return name table list
def Parse_personalInfo_name(html):
	soup = BeautifulSoup(html)
	nameTable = soup.find(id="SCC_NAMES_H$scroll$0")

	# Clean tags
	tableString = str(nameTable)
	x = re.sub("\<.*?\>", "", tableString);
	# clean result list
	resultList = filter(lambda x: len(x) > 0, x.replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n"))
	return resultList

# Return phone table list
def Parse_personalInfo_phone(html):
	soup = BeautifulSoup(html)
	phoneTable = soup.find(id="SCC_PERS_PHN_H$scroll$0")
	rows = phoneTable.find_all("tr")
	# Phone table head
	resultList = filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(rows[0])).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))
	phonesCount = len(rows) - 1

	for i in xrange(0, phonesCount):
		newPhone = []
		eachPhoneRow = rows[i + 1]
		newPhone.append(eachPhoneRow.find(selected="selected").text) # selected type
		newPhone.append(eachPhoneRow.find(id="SCC_PERS_PHN_H_PHONE$" + str(i))["value"])
		newPhone.append(eachPhoneRow.find(id="SCC_PERS_PHN_H_EXTENSION$" + str(i))["value"])
		newPhone.append(eachPhoneRow.find(id="SCC_PERS_PHN_H_COUNTRY_CODE$" + str(i))["value"])
		newPhone.append(eachPhoneRow.find(id="SCC_PERS_PHN_H_PREF_PHONE_FLAG$chk$" + str(i))["value"])
		resultList.extend(newPhone)
	return resultList
		
# Return example:
# ['Email Addresses', 'Description for Email Addresses', 
# 'Campus Email Address', 'Description for Campus Email Address', 
# 'Campus email', 'Delivered to', 'x111xxx@uwaterloo.ca', 'x111xxx@connect.uwaterloo.ca', 
# 'Alternate Email Addresses', 'Description for Alternate Email Address', 
# 'Email Type', 'Email Address', 'Home', 'blablabla@gmail.com']
def Parse_personalInfo_email(html):
	soup = BeautifulSoup(html)	
	# print soup.prettify()
	emailTable1Description = soup.find(id="ACE_UW_SS_WORK_GROUP_BOX_1")
	resultList = ["Email Addresses"]
	resultList.extend(filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1Description)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
	emailTable1 = soup.find(id="UW_RTG_EMAIL_VW$scroll$0")
	# print filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))
	resultList.extend(filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))

	emailTable2Description = soup.find(id="ACE_UW_DERIVED_CEM_GROUP_BOX_1")
	resultList.extend(filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable2Description)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
	emailTable2 = soup.find(id="SCC_EMAIL_H$scroll$0")
	resultList.extend(filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable2)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
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
	keysNumber = 2 # How many columns
	addressList = Parse_personalInfo_address(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if not len(addressList) < keysNumber:
		meta["status"] = "success"
		# addressCount = (len(addressList) - 2) / keysNumber
		addressCount = len(addressList) / keysNumber - 1
		for i in xrange(0, addressCount):
			addressDict = {}
			addressDict["address_type"] = addressList[(i + 1) * keysNumber]
			addressDict["address"] = addressList[(i + 1) * keysNumber + 1]
			data.append(addressDict)
			# addressDict[addressList[(i + 1) * 2]] = addressList[(i + 1) * 2 + 1]
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no address information"
	return getFullResponseDictionary(meta, data)

def API_personalInfo_nameResponse(questSession):
	keysNumber = 6 # How many columns
	nameList = Parse_personalInfo_name(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if not len(nameList) < keysNumber:
		meta["status"] = "success"
		nameCount = len(nameList) / keysNumber - 1
		for i in xrange(0, nameCount):
			nameDict = {}
			nameDict["name_type"] = nameList[(i + 1) * keysNumber]
			nameDict["name_prefix"] = nameList[(i + 1) * keysNumber + 1]
			nameDict["first_name"] = nameList[(i + 1) * keysNumber + 2]
			nameDict["middle_name"] = nameList[(i + 1) * keysNumber + 3]
			nameDict["last_name"] = nameList[(i + 1) * keysNumber + 4]
			nameDict["name_suffix"] = nameList[(i + 1) * keysNumber + 5]
			data.append(nameDict)
			# addressDict[addressList[(i + 1) * 2]] = addressList[(i + 1) * 2 + 1]
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no name information"
	return getFullResponseDictionary(meta, data)

def API_personalInfo_phoneResponse(questSession):
	keysNumber = 5 # How many columns
	phoneList = Parse_personalInfo_phone(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if not len(phoneList) < keysNumber:
		meta["status"] = "success"
		phoneCount = len(phoneList) / keysNumber - 1
		for i in xrange(0, phoneCount):
			phoneDict = {}
			phoneDict["phone_type"] = phoneList[(i + 1) * keysNumber]
			phoneDict["telephone"] = phoneList[(i + 1) * keysNumber + 1]
			phoneDict["ext"] = phoneList[(i + 1) * keysNumber + 2]
			phoneDict["country"] = phoneList[(i + 1) * keysNumber + 3]
			phoneDict["preferred"] = phoneList[(i + 1) * keysNumber + 4]
			data.append(phoneDict)
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no phone information"
	return getFullResponseDictionary(meta, data)


def API_personalInfo_emailResponse(questSession):
	keysNumber = 2 # How many columns
	emailList = Parse_personalInfo_email(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}
	if not len(emailList) < 6:
		meta["status"] = "success"
		# {
		# 	"data" : {
		# 		"description" : ""
		# 		"campus_email_address": {
		# 			"description" : ""
		# 			"data": [{
		# 				"campus_email": ""
		# 				"delivered_to": ""
		# 			}]
		# 		}
		# 		"alternate_email_address": {
		# 			"description" : ""
		# 			"data": [{
		# 				"email_type": ""
		# 				"email_address": ""
		# 			}]
		# 		}
		# 	}
		# }

		data["description"] = emailList[emailList.index("Email Addresses") + 1]

		campusEmailIndex = emailList.index("Campus Email Address")
		alternateEmailIndex = emailList.index("Alternate Email Addresses")

		campusEmailCount = (alternateEmailIndex - (campusEmailIndex + 2)) / keysNumber - 1
		alternateEmailCount = (len(emailList) - (alternateEmailIndex + 2)) / keysNumber - 1

		campusEmailData = []
		alternateEmailData = []

		for i in xrange(0, campusEmailCount):
			emailDict = {}
			emailDict["campus_email"] = emailList[campusEmailIndex + 2 + (i + 1) * keysNumber]
			emailDict["delivered_to"] = emailList[campusEmailIndex + 2 + (i + 1) * keysNumber + 1]
			campusEmailData.append(emailDict)
		data["campus_email_address"] = {
			"description": emailList[campusEmailIndex + 1],
			"data": campusEmailData
		}

		for i in xrange(0, alternateEmailCount):
			emailDict = {}
			emailDict["email_type"] = emailList[alternateEmailIndex + 2 + (i + 1) * keysNumber]
			emailDict["email_address"] = emailList[alternateEmailIndex + 2 + (i + 1) * keysNumber + 1]
			alternateEmailData.append(emailDict)
		data["alternate_email_address"] = {
			"description": emailList[alternateEmailIndex + 1],
			"data": alternateEmailData
		}
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no phone information"
	return getFullResponseDictionary(meta, data)