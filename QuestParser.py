from bs4 import BeautifulSoup
import re
from xml.sax.saxutils import unescape

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
	resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, x.replace(" \r", ", ").split("\n")))
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
	resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, x.replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
	return resultList

# Return phone table list
def Parse_personalInfo_phone(html):
	soup = BeautifulSoup(html)
	phoneTable = soup.find(id="SCC_PERS_PHN_H$scroll$0")
	rows = phoneTable.find_all("tr")
	# Phone table head
	resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(rows[0])).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
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
	resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1Description)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))))
	emailTable1 = soup.find(id="UW_RTG_EMAIL_VW$scroll$0")
	# print filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))
	resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))))

	emailTable2Description = soup.find(id="ACE_UW_DERIVED_CEM_GROUP_BOX_1")
	resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable2Description)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))))
	emailTable2 = soup.find(id="SCC_EMAIL_H$scroll$0")
	resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable2)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))))
	return resultList

def Parse_personalInfo_emergencyContact(html):
	soup = BeautifulSoup(html)	
	# return soup.prettify()
	table = soup.find(id="SCC_EMERG_CNT_H$scroll$0")
	if table is None:
		return ["No current emergency contact information found."]
	else:
		rows = table.find_all("tr")
		contactsCount = len(rows) - 1
		resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(rows[0])).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		for i in xrange(0, contactsCount):
			newContact = []
			eachContactRow = rows[i + 1]
			resultList.append(eachContactRow.find(id="PRIMARY$chk$" + str(i))["value"])
			resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(eachContactRow)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n"))))
		return resultList

def Parse_personalInfo_demographicInfo(html):
	soup = BeautifulSoup(html)	
	# return soup.prettify()
	demographicTable = soup.find(id="ACE_$ICField$45$")
	demographicDict = {}
	demographicDict["demographic_information"] = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(demographicTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))

	nationalIndentificationNumberTable = soup.find(id="$ICField$2$$scroll$0")
	demographicDict["national_identification_number"] = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(nationalIndentificationNumberTable)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
	
	citizenshipInformationTable = soup.find(id="CITIZENSHIP$scrolli$0")
	demographicDict["citizenship_information"] = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(citizenshipInformationTable)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))

	visaTable = soup.find(id="DRIVERS_LIC1$scrolli$0")
	demographicDict["visa_or_permit_data"] = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(visaTable)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))

	return demographicDict

def Parse_personalInfo_citizenship(html):
	soup = BeautifulSoup(html)	
	# return soup.prettify()
	citizenshipTable = soup.find(id="VISA_PMT_SUPPRT$scroll$0")
	resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(citizenshipTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))[1:]
	resultList.insert(0, "visa_type")
	resultList.insert(0, "country")
	return resultList

def Parse_myAcademics_myProgram(html):
	soup = BeautifulSoup(html)	
	# return soup.prettify()
	table = soup.find(id="ACADPROGCURRENT$scroll$0")
	resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(table)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
	resultList.insert(0, "Current Program")
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
		meta["message"] = "response page contains no email information"
	return getFullResponseDictionary(meta, data)

def API_personalInfo_emergencyContactResponse(questSession):
	keysNumber = 8 # How many columns
	contactList = Parse_personalInfo_emergencyContact(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if len(contactList) == 1:
		meta["status"] = "success"
	elif not len(contactList) < keysNumber:
		meta["status"] = "success"
		contactCount = len(contactList) / keysNumber - 1
		for i in xrange(0, contactCount):
			contactDict = {}
			contactDict[contactList[0].replace(" ", "_").lower()] = contactList[(i + 1) * keysNumber]
			contactDict[contactList[1].replace(" ", "_").lower()] = contactList[(i + 1) * keysNumber + 1]
			contactDict[contactList[2].replace(" ", "_").lower()] = contactList[(i + 1) * keysNumber + 2]
			contactDict[contactList[3].replace(" ", "_").lower()] = contactList[(i + 1) * keysNumber + 3]
			contactDict[contactList[4].replace(" ", "_").lower()] = contactList[(i + 1) * keysNumber + 4]
			contactDict[contactList[5].replace(" ", "_").lower()] = contactList[(i + 1) * keysNumber + 5]
			data.append(contactDict)
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no emergency contact information"
	return getFullResponseDictionary(meta, data)

def API_personalInfo_demographicInfoResponse(questSession):
	demographicDict = Parse_personalInfo_demographicInfo(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}
	key = "demographic_information"
	try:
		demographicInfoList = demographicDict[key]
		if len(demographicInfoList) > 1:
			numberOfFileds = len(demographicInfoList) / 2
			newDict = {}
			for i in xrange(0, numberOfFileds):
				newDict[demographicInfoList[i * 2].replace(" ", "_").lower()] = demographicInfoList[i * 2 + 1]
			data[key] = newDict
		else:
			data[key] = {}
	except:
		meta["message"] = "get demographic_information error"

	key = "national_identification_number"
	try:
		nationalList = demographicDict[key][1:]
		keysNumber = 3
		if len(nationalList) > keysNumber:
			nationalCount = len(nationalList) / keysNumber - 1
			nationalData = []
			for i in xrange(0, nationalCount):
				newDict = {}
				newDict[nationalList[0].replace(" ", "_").lower()] = nationalList[(i + 1) * keysNumber]
				newDict[nationalList[1].replace(" ", "_").lower()] = nationalList[(i + 1) * keysNumber + 1]
				newDict[nationalList[2].replace(" ", "_").lower()] = nationalList[(i + 1) * keysNumber + 2]
				nationalData.append(newDict)
			data[key] = nationalData
		else:
			data[key] = {}
	except:
		meta["message"] = meta["message"] + ", get national_identification_number error"

	key = "citizenship_information"
	try:
		citizenList = demographicDict[key][1:]
		if citizenList > 2:
			keysNumber = 4
			citizenCount = len(citizenList) / keysNumber
			citizenData = []
			for i in xrange(0, citizenCount):
				newDict = {}
				newDict[citizenList[i * keysNumber].replace(" ", "_").lower()] = citizenList[i * keysNumber + 2]
				newDict[citizenList[i * keysNumber + 1].replace(" ", "_").lower()] = citizenList[i * keysNumber + 2 + 1]
				citizenData.append(newDict)
			data[key] = citizenData
		else :
			data[key] = {}
	except:
		meta["message"] = meta["message"] + ", get citizenship_information error"

	key = "visa_or_permit_data"
	try:
		visaList = demographicDict[key][1:]
		if visaList > 2:
			data[key] = {
				"type": visaList[1] + " - " + visaList[2],
				"country": visaList[4]
			}
		else:
			data[key] = {}
	except:
		meta["message"] = meta["message"] + ", get visa_or_permit_data error"
	
	try:
		data["note"] = demographicDict[key][-1]
	except:
		meta["message"] = meta["message"] + ", get note error"
	if not len(meta["message"]) == 0:
		meta["status"] = "failure"
	else :
		meta["status"] = "success"
	return getFullResponseDictionary(meta, data)

def API_personalInfo_citizenshipResponse(questSession):
	keysNumber = 4 # How many columns
	citizenList = Parse_personalInfo_citizenship(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if not len(citizenList) < keysNumber:
		meta["status"] = "success"
		citizenCount = len(citizenList) / keysNumber - 1
		for i in xrange(0, citizenCount):
			citizenDict = {}
			citizenDict[citizenList[0].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber]
			citizenDict[citizenList[1].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber + 1]
			citizenDict[citizenList[2].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber + 2]
			citizenDict[citizenList[3].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber + 3]
			data.append(citizenDict)
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no citizenship/immigration information"
	return getFullResponseDictionary(meta, data)

def API_myAcademics_myProgramResponse(questSession):
	resultList = Parse_myAcademics_myProgram(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if not len(resultList) < 2:
		meta["status"] = "success"
		kvPairCount = len(resultList) / 2
		for i in xrange(0, kvPairCount):
			newDict = {}
			newDict[resultList[2 * i].replace(" ", "_").lower()] = resultList[2 * i + 1]
			data.append(newDict)
	else :
		meta["status"] = "failure"
		meta["message"] = "response page contains no my program information"
	return getFullResponseDictionary(meta, data)

