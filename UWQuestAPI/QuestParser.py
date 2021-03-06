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
	if addressTable is None:
		return []
	# Clean tags
	tableString = str(addressTable)
	x = re.sub("\<.*?\>", "", tableString);
	# clean result list
	resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, x.replace(" \r", ", ").split("\n")))
	try:
		del(resultList[2])
		# resultList contains
		return resultList
	except:
		return []

# Return name table list
def Parse_personalInfo_name(html):
	soup = BeautifulSoup(html)
	nameTable = soup.find(id="SCC_NAMES_H$scroll$0")
	if nameTable is None:
		return []

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
	if phoneTable is None:
		return []
	rows = phoneTable.find_all("tr")

	phonesCount = len(rows) - 1
	if phonesCount < 1:
		return []
	# Phone table head
	resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(rows[0])).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))

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
	if emailTable1Description is None:
		return []
	resultList = ["Email Addresses"]
	resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1Description)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))))
	emailTable1 = soup.find(id="UW_RTG_EMAIL_VW$scroll$0")
	if emailTable1 is None:
		return []
	# print filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))
	resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable1)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))))


	emailTable2Description = soup.find(id="ACE_UW_DERIVED_CEM_GROUP_BOX_1")
	if not (emailTable2Description is None):
		resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable2Description)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))))
	
	emailTable2 = soup.find(id="SCC_EMAIL_H$scroll$0")
	if not (emailTable2 is None):
		resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(emailTable2)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n"))))
	return resultList

def Parse_personalInfo_emergencyContact(html):
	soup = BeautifulSoup(html)	
	# print soup.prettify()
	table = soup.find(id="SCC_EMERG_CNT_H$scroll$0")
	if table is None:
		isValid = soup.find(id="DERIVED_CCSRVC1_SS_TRANSACT_TITLE")
		if (not isValid is None) and isValid.text.strip() == "Emergency Contacts":
			return ["No current emergency contact information found."]
		else:
			return []
	else:
		rows = table.find_all("tr")
		contactsCount = len(rows) - 1
		if contactsCount < 1:
			return []
		resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(rows[0])).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		for i in xrange(0, contactsCount):
			newContact = []
			eachContactRow = rows[i + 1]
			resultList.append(eachContactRow.find(id="PRIMARY$chk$" + str(i))["value"])
			resultList.extend(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(eachContactRow)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n"))))
		return resultList

def Parse_personalInfo_demographicInfo(html):
	soup = BeautifulSoup(html)	
	# print soup.prettify()
	demographicTable = soup.find(id="ACE_$ICField$45$")
	demographicDict = {"demographic_information": [], "national_identification_number": [], "citizenship_information": [], "visa_or_permit_data": []}
	if demographicTable is None:
		return demographicDict
	demographicDict["demographic_information"] = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(demographicTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))

	nationalIndentificationNumberTable = soup.find(id="$ICField$2$$scroll$0")
	if nationalIndentificationNumberTable is None:
		return demographicDict
	demographicDict["national_identification_number"] = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(nationalIndentificationNumberTable)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
	
	citizenshipInformationTable = soup.find(id="CITIZENSHIP$scrolli$0")
	if citizenshipInformationTable is None:
		return demographicDict
	demographicDict["citizenship_information"] = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(citizenshipInformationTable)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))

	visaTable = soup.find(id="DRIVERS_LIC1$scrolli$0")
	if visaTable is None:
		return demographicDict
	demographicDict["visa_or_permit_data"] = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(visaTable)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))

	return demographicDict

# May return string or [(,), (,)]
def Parse_personalInfo_citizenship(html):
	soup = BeautifulSoup(html)	
	# print soup.prettify()
	requiredDocumentation = soup.find(id="VISA_PMT_SUPPRT$scroll$0")
	pastDocumentation = soup.find(id="VISA_PMT_EXPIRED$scroll$0")
	if requiredDocumentation is None:
		isValid = soup.find(id="win0div$ICField$1$")
		# print "None"
		if (not isValid is None) and isValid.text.strip() == 'Citizenship/Immigration Documents':
			# print "Valid"
			extraText = soup.find(id="win0divUW_DERIVED_DOCS_PAGETEXT1") # Some message for new student 
			if not extraText is None:
				return str(extraText.text.strip())
		return []
	resultData = []
	requiredDocList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(requiredDocumentation)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))[1:]
	
	# For required documentation, remove "upload" 
	isHasUpload = requiredDocumentation.find(id="ATTACHADD$0")
	if len(requiredDocList) == 3 and isHasUpload:
		requiredDocList = requiredDocList[:len(requiredDocList) - 1]
	requiredDocList.insert(0, "visa_type")
	requiredDocList.insert(0, "country")
	# print requiredDocList
	resultData.append(("Required Documentation", requiredDocList))

	if pastDocumentation:
		pastDocList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(pastDocumentation)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))[1:]
		pastDocList.insert(0, "visa_type")
		pastDocList.insert(0, "country")
		# print pastDocList
		resultData.append(("Past Documentation", pastDocList))
	return resultData

def Parse_myAcademics_myProgram(html):
	soup = BeautifulSoup(html)	
	# print soup.prettify()
	table = soup.find(id="ACADPROGCURRENT$scroll$0")
	if table is None:
		return []
	messageID = "win0divUW_DERIVED_SR_DESCR50$0"
	try:
		soup.find(id=messageID).extract() # Inactive term, skip it FIXIT
	except Exception, e:
		pass
	resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(table)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
	resultList.insert(0, "Current Program")
	if resultList[2] == "CurrentSubPlanGroupbox":
		resultList[2] = "Current Sub Plan"
	return resultList

def Parse_myAcademics_grades(html):
	soup = BeautifulSoup(html)	
	# print soup.prettify()
	choiceTable = soup.find(id="SSR_DUMMY_RECV1$scroll$0")
	if choiceTable is None: # There is only one chice and grade list is returned directly
		termList = soup.find(id="ACE_DERIVED_REGFRM1_SSR_STDNTKEY_DESCR")
		if termList is None:
			return []
		termList = map(lambda x: x.strip(), re.sub("\<.*?\>", "", str(termList)).split("|"))
		if len(termList) < 2:
			return []
		result = ["Term", "Career", "Institution", termList[0], "-", termList[1]]
		# print result
		return result
	else:
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(choiceTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
		try:
			del(resultList[0])
			return resultList
		except:
			return []

def Parse_myAcademics_gradesTerm(html):
	soup = BeautifulSoup(html.replace("<![CDATA[", "<").replace("]]>", ">"))
	# print soup.prettify()
	termList = soup.find(id="DERIVED_REGFRM1_SSR_STDNTKEY_DESCR$5$")
	result = {"term": "", "career": "", "institution": "", "message": "", "grades": []}
	if termList is None:
		return result
	termList = map(lambda x: x.strip(), re.sub("\<.*?\>", "", str(termList)).split("|"))
	# print termList
	if len(termList) < 2:
		return result
	# result = {}
	if len(termList) == 3:
		result["term"] = termList[0]
		result["career"] = termList[1]
		result["institution"] = termList[2]
	elif len(termList) == 2:
		result["term"] = termList[0]
		result["career"] = '-'
		result["institution"] = termList[1]
	else:
		return result

	message = soup.find(id="DERIVED_SSS_GRD_SSR_MESSAGE")
	# print message
	if not message is None:
		result["message"] = unescape(message.text.strip())

	gradesTable = soup.find(id="TERM_CLASSES$scroll$0")
	if gradesTable is None:
		return result
	result["grades"] = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(gradesTable)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
	return result

def Parse_myAcademics_unofficialTranscript(html):
	soup = BeautifulSoup(html)
	# return soup.prettify()
	result = soup.find(id="GO$span")
	if result == None:
		return {}
	soup.find(id="GO$span").clear()
	table = soup.find(id="ACE_TRANSCRIPT_TYPE_")
	if table is None:
		return {}
	keys = table.find_all("label")
	values = table.find_all("select")
	if not len(keys) == len(values):
		return {}
	keys = map(lambda x: re.sub("\<.*?\>", "", str(x)).replace("\xc2\xa0", "").strip().replace(" ", "_").lower(), keys)
	# print keys
	responseDict = {}
	count = len(keys)
	for i in xrange(0, count):
		options = values[i].find_all("option")
		optionsList = []
		for eachOption in options:
			dic = {}
			dic["value"] = eachOption["value"]
			if len(dic["value"]) == 0:
				continue
			dic["description"] = eachOption.text.strip()
			dic["selected"] = "N"
			try:
				isSelected = eachOption["selected"]
				if isSelected:
					dic["selected"] = "Y"
			except:
				pass
			optionsList.append(dic)
		responseDict[keys[i]] = optionsList
	# print responseDict
	return responseDict

def Parse_myAcademics_myAdvisors(html):
	soup = BeautifulSoup(html)
	# print soup.prettify()
	programTable = soup.find(id="ACE_DERIVED_SSSADVR_GROUPBOX2$0")
	if programTable == None:
		isValid = soup.find(id="ACE_DERIVED_SR_DESCR100")
		if (not isValid is None) and (not isValid.text.strip().find("have not been assigned") == -1):
			return [isValid.text.strip()]
		return []
	programList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(programTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
	advisorTable = soup.find(id="ADVISOR_LIST$scroll$0")
	if advisorTable == None:
		return []
	advisorList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(advisorTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
	programList.extend(advisorList)
	return programList

def Parse_enroll_myClassSchedule(html):
	soup = BeautifulSoup(html)
	# print soup.prettify()
	choiceTable = soup.find(id="SSR_DUMMY_RECV1$scroll$0")
	if choiceTable is None: 
	# 1: There is only one chice and schedule list is returned directly
	# 2: Inactive term
		termList = soup.find(id="ACE_DERIVED_REGFRM1_SSR_STDNTKEY_DESCR")
		if termList is None:
			isValid = soup.find(id="win0divDERIVED_REGFRM1_SS_MESSAGE_LONG")
			if not isValid:
				return [], "Page not valid" 
			else:
				return[isValid.text.strip()], None
		termList = map(lambda x: x.strip(), re.sub("\<.*?\>", "", str(termList)).split("|"))
		if len(termList) < 3:
			return [], "TermList length is incorrect"
		result = ["Term", "Career", "Institution", termList[0], termList[1], termList[2]]
		return result, None
	else:
		choiceList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(choiceTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
		if len(choiceList) < 3:
			return [], "ChoiceList length is incorrect"
		try:
			del(choiceList[0])
		except Exception, e:
			return [], "error: %s" % e
		return choiceList, None

def Parse_enroll_myClassScheduleTerm(html):
	soup = BeautifulSoup(html.replace("<![CDATA[", "<").replace("]]>", ">"))
	# print soup.prettify().encode('utf8')
	try:
		soup.find(id="DERIVED_SSS_SCT_SSS_TERM_LINK").clear()
	except:
		pass
	termList = soup.find(id="ACE_DERIVED_REGFRM1_SSR_STDNTKEY_DESCR")
	result = {"term": "", "career": "", "institution": "", "data": []}
	if termList is None:
		isValid = soup.find(id="win0divDERIVED_REGFRM1_SS_MESSAGE_LONG")
		if isValid:
			return (result, isValid.text.strip())
		else:
			return (result, "page error")
	termList = map(lambda x: x.strip(), re.sub("\<.*?\>", "", str(termList)).split("|"))
	if len(termList) < 3:
		return (result, "term string error")
	result = {}
	result["term"] = termList[0]
	result["career"] = termList[1]
	result["institution"] = termList[2]
	result["classes"] = []

	classTable = soup.find(id="ACE_STDNT_ENRL_SSV2$0")
	classCount = len(re.findall("['\"]win0divDERIVED_REGFRM1_DESCR20\$[\d+]['\"]", str(classTable)))
	# print classCount
	for i in xrange(0, classCount):
		classStatus = soup.find(id="SSR_DUMMY_RECVW$scroll$" + str(i)).extract()
		classComponents = soup.find(id="CLASS_MTG_VW$scroll$" + str(i)).extract()
		# Process class title
		classTitle = soup.find(id="win0divDERIVED_REGFRM1_DESCR20$" + str(i))
		classTitle = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(classTitle)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
		if not len(classTitle) is 1:
			return (result, "class title not found")
		classTitle = classTitle[0]
		classTitleList = map(lambda x: x.strip(), classTitle.split(" - "))
		if not len(classTitleList) is 2:
			return (result, "class title split error")
		classSubject_categoryNum = classTitleList[0]
		classSubject_categoryNumList = classSubject_categoryNum.split(" ")
		if not len(classSubject_categoryNumList) is 2:
			return (result, "class subject category split error")
		classSubject = classSubject_categoryNumList[0]
		classCategoryNum = classSubject_categoryNumList[1]
		classDescription = classTitleList[1]
		newClass = {}
		newClass["subject"] = classSubject
		newClass["category_number"] = classCategoryNum
		newClass["description"] = classDescription

		# Process class status
		classStatusList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(classStatus)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		keysNumber = 4
		if not len(classStatusList) is keysNumber * 2:
			return (result, "class status split error")
		for i in xrange(0, keysNumber):
			newClass[classStatusList[i].replace(" ", "_").lower()] = classStatusList[keysNumber + i]
		
		newClass["components"] = []
		# process class components
		keysNumber = 7
		classComponentsList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(classComponents)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		# print classComponentsList
		if not len(classComponentsList) % keysNumber is 0:
			return (result, "class components count error")
		componentsCount = len(classComponentsList) / keysNumber - 1
		for i in xrange(0, componentsCount):
			newDict = {}
			for j in xrange(0, keysNumber):
				# Replace MC-- 2035 to MC 2035
				if classComponentsList[j].replace(" ", "_").lower() == "room":
					classComponentsList[(i + 1) * keysNumber + j] = classComponentsList[(i + 1) * keysNumber + j].replace("-", "")

				newDict[classComponentsList[j].replace(" ", "_").lower()] = classComponentsList[(i + 1) * keysNumber + j] if (not classComponentsList[(i + 1) * keysNumber + j] is '-') else classComponentsList[(i + 1 - 1) * keysNumber + j]
			newClass["components"].append(newDict)
		result["classes"].append(newClass)

	return (result, "")

	# id="win0divDERIVED_REGFRM1_DESCR20$1" # Class Div
	# id="SSR_DUMMY_RECVW$scroll$1" # Class status table
	# id="CLASS_MTG_VW$scroll$1" # Class number table

def Parse_enroll_searchForClasses(html):
	soup = BeautifulSoup(html)
	# print soup.prettify()
	searchInstitutionID = "win0divCLASS_SRCH_WRK2_INSTITUTION$31$"
	searchTermID = "win0divCLASS_SRCH_WRK2_STRM$35$"
	#searchCourseID = ""
	searchCourseNumberMatch = "win0divCLASS_SRCH_WRK2_SSR_EXACT_MATCH1"
	searchCourseCareer = "win0divCLASS_SRCH_WRK2_ACAD_CAREER"

	keys = ["institution", "term", "course_number_relation", "course_career"]
	searchIDs = [searchInstitutionID, searchTermID, searchCourseNumberMatch, searchCourseCareer]

	responseDict = {}
	try:
		numberOfFileds = 4
		for i in xrange(0, numberOfFileds):
			key = keys[i]
			id = searchIDs[i]
			div = soup.find(id=id)
			options = div.find_all("option")
			optionsList = []
			for eachOption in options:
				# print eachOption
				dic = {}
				dic["value"] = eachOption["value"]
				if len(dic["value"]) == 0:
					continue
				dic["description"] = eachOption.text.strip()
				dic["selected"] = "N"
				try:
					isSelected = eachOption["selected"]
					if isSelected:
						dic["selected"] = "Y"
				except:
					pass

				optionsList.append(dic)
			responseDict[key] = optionsList
		responseDict["course_subject"] = []
		responseDict["course_number"] = []
		responseDict["show_open_classes_only"] = []
	except Exception, e:
		print e
		responseDict = {}
	# print responseDict
	return responseDict

def Parse_enroll_searchForClassesResult(html):
	html = html.replace("<![CDATA[", "<").replace("]]>", ">")
	soup = BeautifulSoup(html)
	# print soup.prettify().encode('utf8')
	isNoResult = soup.find(id="win0divDERIVED_CLSMSG_ERROR_TEXT")
	if isNoResult:
		# print "The search returns no results that match the criteria specified."
		return [], None
	# print soup.text.encode("utf-8")
	separatorPattern = re.compile("<.+win0divDERIVED_CLSRCH_SSR_EXPAND_COLLAP2\$\d+(?!.+\$).+>")
	splitResultList = re.split(separatorPattern, html) #re.split(seperatorPattern, soup.text)
	courseHtml = splitResultList[1:]
	courseCount = len(courseHtml)
	resultList = []
	for i in xrange(0, courseCount):
		eachCourse = courseHtml[i]
		courseDict = parseCourse(eachCourse, i)
		if courseDict:
			resultList.append(courseDict)
		else:
			return resultList, "There are errors in parsed course data"
	return resultList, None

def parseCourse(courseHtml, index):
	soup = BeautifulSoup(courseHtml)
	resultDict = {}
	try:
		courseNameChunk = soup.find(id="DERIVED_CLSRCH_DESCR200$" + str(index))
		courseString = courseNameChunk.text.strip()
		courseSubjectNumber, courseName = map(lambda x: x.strip(), courseString.split("-"))
		courseSubject, courseNumber = courseSubjectNumber.split()
		resultDict["course_subject"] = courseSubject
		resultDict["course_number"] = courseNumber
		resultDict["course_name"] = courseName
		
		sectionSeparator = re.compile("(id(?:|\s)=(?:|\s)(?:\'|\")UW_DERIVED_SR_SSR_CLASSNAME_LONG\$\d+(?:\'|\"))")
		sectionsHtml = re.split(sectionSeparator, courseHtml)[1:]
		sectionCount = len(sectionsHtml)
		assert(sectionCount % 2 == 0)
		sectionsList = []
		for i in xrange(0, sectionCount / 2):
			sectionResult = parseSection(sectionsHtml[2 * i], sectionsHtml[2 * i + 1])
			if sectionResult:
				sectionsList.append(sectionResult)
			else:
				assert(0)
		resultDict["sections"] = sectionsList
	except Exception, e:
		print e
		return None
	return resultDict

def parseSection(idString, sectionHtml):
	resultDict = {}
	try:
		valuePattern = re.compile("id(?:|\s)=(?:|\s)(?:\'|\")(UW_DERIVED_SR_SSR_CLASSNAME_LONG\$\d+)(?:\'|\")")
		indexPattern = re.compile("id(?:|\s)=(?:|\s)(?:\'|\")UW_DERIVED_SR_SSR_CLASSNAME_LONG\$(\d+)(?:\'|\")")
		requestValue =  re.findall(valuePattern, idString)[0]
		resultDict["section_info_request_value"] = requestValue
		indexString = re.findall(indexPattern, idString)[0]
		# print requestValue, indexString

		sectionStringPattern = re.compile("(?:\'|\")UW_DERIVED_SR_SSR_CLASSNAME_LONG\$%s(?:\'|\").*?>(.*?)</a>" % indexString, re.DOTALL)
		sectionString = re.findall(sectionStringPattern, sectionHtml)[0]
		pattern = re.compile("(.*)-(.*)\((.*)\)")
		# result = re.findall(pattern, sectionString)
		component_number, component_type, classNumber = re.findall(pattern, sectionString)[0]
		# print component_number, component_type, classNumber
		resultDict["component_type"] = component_type
		resultDict["component_number"] = component_number
		resultDict["class_number"] = classNumber

		soup = BeautifulSoup("<a " + sectionHtml)
		# print soup.text
		# print soup.prettify()
		status = soup.find(id="win0divDERIVED_CLSRCH_SSR_STATUS_LONG$" + indexString)
		# print status.find("img")["alt"]
		resultDict["status"] = status.find("img")["alt"].strip()
		session = soup.find(id='win0divPSXLATITEM_XLATSHORTNAME$' + indexString).text.strip()

		scheduleTable = soup.find(id="SSR_CLSRCH_MTG1$scroll$" + indexString)
		scheduleList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(scheduleTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
		# print scheduleList
		keysNumber = 4
		assert(len(scheduleList) % keysNumber == 0)
		count = len(scheduleList) / keysNumber - 1
		# print count
		scheduleResultList = []
		for i in xrange(0, count):
			dic = {}
			for keyIndex in xrange(0, keysNumber):
				key = scheduleList[keyIndex].replace(" ", "_").lower()
				if key == "room":
					# Replace MC-- 2035 to MC 2035
					dic[key] = scheduleList[(i + 1) * keysNumber + keyIndex].replace("-", "")
				else:
					dic[key] = scheduleList[(i + 1) * keysNumber + keyIndex]
			# print dic
			scheduleResultList.append(dic)
		resultDict["schedules"] = scheduleResultList
		# sectionNumberString = sectionString
		# print sectionString
	except Exception, e:
		print e
		return None
	# print resultDict
	return resultDict

def Parse_enroll_searchForClassesClassDetail(html):
	html = html.replace("<![CDATA[", "<").replace("]]>", ">")
	soup = BeautifulSoup(html)
	# print soup.prettify().encode('utf8')
	# ids for different section
	# course related
	id_course_name = "win0divDERIVED_CLSRCH_DESCR200"
	id_course_institution = "win0divDERIVED_CLSRCH_SSS_PAGE_KEYDESCR"
	# class related
	id_class_detail = "win0divSSR_CLS_DTL_WRK_GROUP1"
	id_meeting_info = "win0divSSR_CLSRCH_MTG$0"
	id_enrollment_info = "win0divSSR_CLS_DTL_WRK_GROUP2" # special case: cs 137 tut002
	id_class_availability = "win0divSSR_CLS_DTL_WRK_GROUP3"
	id_combined_section = "win0divSCTN_CMBND$0" # graduate courses
	id_unknown_GROUP4 = "win0divSSR_CLS_DTL_WRK_GROUP4" # Missing GROUP4??? TODO: 
	id_class_note = "win0divSSR_CLS_DTL_WRK_GROUP5"# cs 115 sec 001
	id_description = "win0divSSR_CLS_DTL_WRK_GROUP6"

	paresIds = [id_course_name,
				id_course_institution,
				id_class_detail,
				id_meeting_info,
				id_enrollment_info,
				id_class_availability,
				id_combined_section,
				id_unknown_GROUP4,
				id_class_note,
				id_description]

	parseFunctions = [parseClass_course_name,
					  parseClass_course_institution,
					  parseClass_detail,
					  parseClass_meeting_info,
					  parseClass_enrollment_info,
					  parseClass_class_availability,
					  parseClass_combined_section,
					  parseClass_unknown_GROUP4,
					  parseClass_class_note,
					  parseClass_description]

	resultDict = {}

	count = len(paresIds)
	for i in xrange(0, count):
		resultDict, hasError = parseUseIDandFunction(soup, resultDict, paresIds[i], parseFunctions[i])
		if hasError:
			return resultDict, hasError
	return resultDict, None

# Parse different ids with different functions, template
def parseUseIDandFunction(soup, resultDict, idString, parseFunction):
	print "Parse " + idString
	soupResult = soup.find(id=idString)
	if not soupResult:
		error = "id=" + idString + " not found"
		print error
		# For fieds must have
		if (idString == "win0divDERIVED_CLSRCH_DESCR200") or (idString == "win0divDERIVED_CLSRCH_SSS_PAGE_KEYDESCR") or (idString == "win0divSSR_CLS_DTL_WRK_GROUP1") or (idString == "win0divSSR_CLSRCH_MTG$0"):
			return resultDict, error
		else:
			return resultDict, None
	soupResult = soupResult.extract()
	result = parseFunction(soupResult)
	if not len(result) > 0:
		error = "parse " + idString + " returned none"
		print error
		return resultDict, error
	resultDict = dict(resultDict.items() + result.items())
	return resultDict, None

def parseClass_course_name(soupResult):
	resultDict = {}
	try:
		string = soupResult.text.encode('utf8').strip().replace("\xc2\xa0", "")
		first, second = map(lambda x: x.strip(), string.split("-"))
		# print first, second
		subject, number = map(lambda x: x.strip(), first.split())
		# print subject
		# print number
		resultDict["course_subject"] = subject
		resultDict["course_number"] = number
		secondList = map(lambda x: x.strip(), second.split())
		component_number = secondList[0]
		name = " ".join(secondList[1:])
		# print component_number
		# print name
		resultDict["component_number"] = component_number
		resultDict["course_name"] = name
	except Exception, e:
		print "parse course name error %s" % e
		return {}
	return resultDict

def parseClass_course_institution(soupResult):
	resultDict = {}
	try:
		string = soupResult.text.encode('utf8').strip().replace("\xc2\xa0", "")
		institution, term, component_type = map(lambda x: x.strip(), string.split("|"))
		resultDict["institution"] = institution
		resultDict["term"] = term
		resultDict["component_type"] = component_type
	except Exception, e:
		print "parse course institution error %s" % e
		return {}
	return resultDict

def parseClass_detail(soupResult):
	resultDict = {}
	try:
		# print soupResult.prettify().encode('utf8')
		subDict = {}

		# process components
		component_key = soupResult.find(id="win0divSR_LBL_WRK_CRSE_COMPONENT_LBLlbl").extract().text.strip().replace(" ", "_").lower()
		components = soupResult.find(id="win0divSSR_DUMMY_RECVW$0").extract()
		componentList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(components)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
		keysNumber = 2
		componentCount = len(componentList) / keysNumber
		aListOfComponentDict = []
		for i in xrange(0, componentCount):
			componentDict = {}
			componentDict["component_type"] = componentList[i * keysNumber]
			componentDict["is_required"] = componentList[i * keysNumber + 1]
			aListOfComponentDict.append(componentDict)
		subDict[component_key] = aListOfComponentDict

		# process other keys
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(soupResult)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		# get main key - class detail
		class_detail = resultList[0]
		resultList = resultList[1:]
		count = len(resultList)
		assert(count % 2 == 0)
		for i in xrange(0, count / 2):
			subDict[resultList[2 * i].replace(" ", "_").lower()] = resultList[2 * i + 1].strip()
		resultDict[class_detail] = subDict
	except Exception, e:
		print "parse class detail error: %s" % e
		return {}
	return resultDict


def parseClass_meeting_info(soupResult):
	# print soupResult.prettify().encode('utf8')
	resultDict = {}
	try:
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(soupResult)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		# print resultList
		meetingKey = resultList[0].replace(" ", "_").lower()
		resultList = resultList[1:]

		keysNumber = 4
		assert(len(resultList) % keysNumber == 0)
		count = len(resultList) / keysNumber - 1
		# print count
		meetingList = []
		for i in xrange(0, count):
			dic = {}
			for keyIndex in xrange(0, keysNumber):
				key = resultList[keyIndex].replace(" ", "_").lower()
				if key == "room":
					# Replace MC-- 2035 to MC 2035
					dic[key] = resultList[(i + 1) * keysNumber + keyIndex].replace("-", "")
				else:
					dic[key] = resultList[(i + 1) * keysNumber + keyIndex]
			# print dic
			meetingList.append(dic)
		resultDict[meetingKey] = meetingList
	except Exception, e:
		print "parse meeting info error: %s" % e
		return {}
	return resultDict

def parseClass_enrollment_info(soupResult):
	# print soupResult.prettify().encode('utf8')
	resultDict = {}
	try:
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(soupResult)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		# print resultList
		enrollKey = resultList[0].replace(" ", "_").lower()
		resultList = resultList[1:]
		assert(len(resultList) % 2 == 0)
		count = len(resultList) / 2
		enrollmentList = []
		for i in xrange(0, count):
			eachEnrollDict = {}
			eachEnrollDict[resultList[i * 2].replace(" ", "_").lower()] = resultList[i * 2 + 1]
			enrollmentList.append(eachEnrollDict)
		resultDict[enrollKey] = enrollmentList
	except Exception, e:
		print "parse enrollment info error: %s" % e
		return {}
	return resultDict

def parseClass_class_availability(soupResult):
	# print soupResult.prettify().encode('utf8')
	resultDict = {}
	try:
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(soupResult)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		# print resultList
		key = resultList[0].replace(" ", "_").lower()
		resultList = resultList[1:]
		assert(len(resultList) % 2 == 0)
		count = len(resultList) / 2
		availabilityList = []
		for i in xrange(0, count):
			eachEnrollDict = {}
			eachEnrollDict[resultList[i * 2].replace(" ", "_").lower()] = resultList[i * 2 + 1]
			availabilityList.append(eachEnrollDict)
		resultDict[key] = availabilityList
	except Exception, e:
		print "parse class availability info error: %s" % e
		return {}
	return resultDict

def parseClass_combined_section(soupResult):
	# print soupResult.prettify().encode('utf8')
	resultDict = {}
	try:
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(soupResult)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		# print resultList
		key = resultList[0].replace(" ", "_").lower()
		resultList = resultList[6:]
		keysNumber = 6
		assert(len(resultList) % keysNumber == 0)
		count = len(resultList) / keysNumber
		combined_section_list = []
		for i in xrange(0, count):
			section = {}
			pattern = re.compile("(.*)\s(.*)-(.*)")
			course_subject, course_number, component_number = map(lambda x: x.strip(), re.findall(pattern, resultList[i * keysNumber])[0])
			pattern = re.compile("(.*?)\s\((.*?)\)")
			component_type, class_number = map(lambda x: x.strip(), re.findall(pattern, resultList[i * keysNumber + 1])[0])
			course_name = resultList[i * keysNumber + 2]
			status = resultList[i * keysNumber + 3]
			enroll_total = resultList[i * keysNumber + 4]
			wait_total = resultList[i * keysNumber + 5]

			section["course_subject"] = course_subject
			section["course_number"] = course_number
			section["component_number"] = component_number
			section["component_type"] = component_type
			section["class_number"] = class_number
			section["course_name"] = course_name
			section["status"] = status
			section["enroll_total"] = enroll_total
			section["wait_total"] = wait_total
			combined_section_list.append(section)
		resultDict[key] = combined_section_list
	except Exception, e:
		print "parse combined section info error: %s" % e
		return {}
	return resultDict

def parseClass_unknown_GROUP4(soupResult):
	print "GROUP4 id found!"
	resultDict = {}
	try:
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(soupResult)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		# print resultList
		key = resultList[0].replace(" ", "_").lower()
		resultList = resultList[1:]
		assert(len(resultList) % 2 == 0)
		count = len(resultList) / 2
		unknowList = []
		for i in xrange(0, count):
			eachEnrollDict = {}
			eachEnrollDict[resultList[i * 2].replace(" ", "_").lower()] = resultList[i * 2 + 1]
			unknowList.append(eachEnrollDict)
		resultDict[key] = unknowList
	except Exception, e:
		print "parse unknwon GROUP4 info error: %s" % e
		return {}
	return resultDict

def parseClass_class_note(soupResult):
	# print soupResult.prettify().encode('utf8')
	resultDict = {}
	try:
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(soupResult)).replace(" \r", ", ").replace("\xc2\xa0", "-").split("\n")))
		# print resultList
		key = resultList[0].replace(" ", "_").lower()
		resultList = resultList[1:]
		assert(len(resultList) % 2 == 0)
		count = len(resultList) / 2
		resList = []
		for i in xrange(0, count):
			eachEnrollDict = {}
			eachEnrollDict[resultList[i * 2].replace(" ", "_").lower()] = resultList[i * 2 + 1]
			resList.append(eachEnrollDict)
		resultDict[key] = resList
	except Exception, e:
		print "parse class notes info error: %s" % e
		return {}
	return resultDict

def parseClass_description(soupResult):
	# print soupResult.prettify().encode('utf8')
	resultDict = {}
	try:
		resultList = map(lambda x: unescape(x.strip()), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(soupResult).replace("<br/>", "\n")).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
		# print resultList
		key = resultList[0].replace(" ", "_").lower()
		resultList = resultList[1:]
		description = "\n".join(resultList)
		# print description
		resultDict[key] = description
	except Exception, e:
		print "parse description info error: %s" % e
		return {}
	return resultDict









################# API ################

# Passed in meta and data dictionary and return full response dictionary
def getFullResponseDictionary(meta, data):
	return {"meta": meta, "data": data}

def getEmptyMetaDict():
	return {"status": "", "message": ""}

# Return acount login response dictionary
def API_account_loginResponse(questSession, sid):
	meta = getEmptyMetaDict()
	data = {}
	if questSession.isLogin:
		meta["status"] = "success"
		data["sid"] = sid
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

		# Two cases:
		# ['Email Addresses', 'Email is the primary means of communication used by the University. It is important for you to keep your email address up to date.', 'Campus Email Address', 'This is the official email address the University community will use to communicate with you as a student. Email guidelines can be found at:  http://www.adm.uwaterloo.ca/infocist/emailuse.html .', 'Campus email', 'Delivered to', 'z73huang@uwaterloo.ca', 'z73huang@connect.uwaterloo.ca', 'Alternate Email Addresses', 'The Admissions Office will use the Home email address to communicate with you as an applicant.', 'Email Type', 'Email Address', 'Home', 'huangziyuan0101@sina.cn']
		# ['Email Addresses', 'Email is the primary means of communication used by the University. It is important for you to keep your email address up to date.', 'Campus Email Address', 'This is the official email address the University community will use to communicate with you as a student. Email guidelines can be found at:  http://www.adm.uwaterloo.ca/infocist/emailuse.html .', 'Campus email', 'Delivered to', 'jran@uwaterloo.ca', 'jran012@gmail.com']
		# print emailList

		data["description"] = emailList[emailList.index("Email Addresses") + 1]

		campusEmailIndex = emailList.index("Campus Email Address")
		alternateEmailIndex = len(emailList)
		try:
			alternateEmailIndex = emailList.index("Alternate Email Addresses")
		except Exception, e:
			pass

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

		if alternateEmailCount > 0:
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
		meta["message"] = "No current emergency contact information found."
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
	responseData = Parse_personalInfo_citizenship(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}
	try:
		# Return message, no data for visa documentation
		if isinstance(responseData, str):
			meta["status"] = "success"
			meta["message"] = responseData
			return getFullResponseDictionary(meta, data)
		elif isinstance(responseData, list):
			docList = responseData
			# Process for last element 
			if not (len(docList) == 1 or len(docList) == 2):
				meta["status"] = "failure"
				meta["message"] = "Wrong length of doc list"
				return getFullResponseDictionary(meta, data)
			else:
				key = docList[len(docList) - 1][0].replace(" ", "_").lower()
				citizenList = docList[len(docList) - 1][1]
				keysNumber = 0
				if len(citizenList) % 2 == 0:
					keysNumber = len(citizenList) / 2
				else:
					assert(False)
				meta["status"] = "success"
				citizenCount = len(citizenList) / keysNumber - 1
				tempData = []
				for i in xrange(0, citizenCount):
					citizenDict = {}
					for j in xrange(0, keysNumber):
						citizenDict[citizenList[j].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber + j]
					# citizenDict[citizenList[0].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber]
					# citizenDict[citizenList[1].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber + 1]
					# citizenDict[citizenList[2].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber + 2]
					# citizenDict[citizenList[3].replace(" ", "_").lower()] = citizenList[(i + 1) * keysNumber + 3]
					tempData.append(citizenDict)
				data[key] = tempData
				# process extra one
				if len(docList) == 2:
					keysNumber = 2
					key = docList[0][0].replace(" ", "_").lower()
					requiredDocumentationList = docList[0][1]
					# print requiredDocumentationList
					requiredCount = len(requiredDocumentationList) / keysNumber - 1
					tempData = []
					for i in xrange(0, requiredCount):
						citizenDict = {}
						citizenDict[requiredDocumentationList[0].replace(" ", "_").lower()] = requiredDocumentationList[(i + 1) * keysNumber]
						citizenDict[requiredDocumentationList[1].replace(" ", "_").lower()] = requiredDocumentationList[(i + 1) * keysNumber + 1]
						tempData.append(citizenDict)
					data[key] = tempData
		else:
			meta["status"] = "failure"
			meta["message"] = "response page contains no citizenship/immigration information"
		return getFullResponseDictionary(meta, data)
	except Exception, e:
		meta["status"] = "failure"
		meta["message"] = e
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

def API_myAcademics_gradesResponse(questSession):
	resultList = Parse_myAcademics_grades(questSession.currentResponse.content)
	# print resultList
	meta = getEmptyMetaDict()
	data = []
	keysNumber = 3
	if not len(resultList) < keysNumber:
		meta["status"] = "success"
		count = len(resultList) / keysNumber - 1
		# print "count: " + str(count)
		for i in xrange(0, count):
			newDict = {}
			newDict[resultList[0].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber]
			newDict[resultList[1].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber + 1]
			newDict[resultList[2].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber + 2]
			newDict["term_index"] = i
			data.append(newDict)
	else :
		meta["status"] = "failure"
		meta["message"] = "response page contains no grades information"
	return getFullResponseDictionary(meta, data)

def API_myAcademics_gradesTermResponse(questSession):
	resultDict = Parse_myAcademics_gradesTerm(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}

	optionalKey = "message"
	keys = ["term", "career", "institution", optionalKey]
	for key in keys:
		result = resultDict[key]
		if len(result) == 0 and not key == optionalKey:
			meta["message"] = meta["message"] + ", get " + key + " error"
		else:
			data[key] = result
	keysNumber = 5
	key = "grades"
	resultList = resultDict[key]
	if len(resultList) < keysNumber:
		meta["message"] = meta["message"] + ", get grades data error"
	else :
		count = len(resultList) / keysNumber - 1
		gradesData = []
		for i in xrange(0, count):
			newDict = {}
			newDict[resultList[0].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber]
			newDict[resultList[1].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber + 1]
			newDict[resultList[2].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber + 2]
			newDict[resultList[3].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber + 3]
			newDict[resultList[4].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber + 4]
			gradesData.append(newDict)
		data[key] = gradesData

	if not len(meta["message"]) == 0:
		meta["status"] = "failure"
	else :
		meta["status"] = "success"
	return getFullResponseDictionary(meta, data)

def API_myAcademics_unofficialTranscriptResponse(questSession):
	resultDict = Parse_myAcademics_unofficialTranscript(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}
	if not len(resultDict) < 2:
		meta["status"] = "success"
		data = resultDict
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no unofficial transcript options information"
	return getFullResponseDictionary(meta, data)

def API_myAcademics_unofficialTranscriptResultResponse(questSession):
	try:
		soup = BeautifulSoup(questSession.currentResult)
	except:
		meta = getEmptyMetaDict()
		data = ""
		meta["status"] = "failure"
		meta["message"] = "get transcript time out"
		return getFullResponseDictionary(meta, data)
	# print soup.prettify()
	meta = getEmptyMetaDict()
	data = ""
	if soup.find(id="PrintTranscript"):
		meta["status"] = "success"
		data = str(soup.find(id="PrintTranscript"))
	else:
		meta["status"] = "failure"
		meta["message"] = "get transcript time out"
	return getFullResponseDictionary(meta, data)

def API_myAcademics_myAdvisorResponse(questSession):
	resultList = Parse_myAcademics_myAdvisors(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}
	if len(resultList) == 1:
		meta["status"] = "success"
		meta["message"] = resultList[0]
	elif not len(resultList) < 5:
		meta["status"] = "success"
		data[resultList[0].replace(" ", "_").lower()] = resultList[1]
		data[resultList[2].replace(" ", "_").lower()] = resultList[3]
		data[resultList[4].replace(" ", "_").lower()] = resultList[5:]
	else:
		meta["status"] = "failure"
		meta["message"] = "response page contains no advisors information"
	return getFullResponseDictionary(meta, data)

def API_enroll_myClassScheduleResponse(questSession):
	resultList, hasError = Parse_enroll_myClassSchedule(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	keysNumber = 3
	if hasError:
		meta["status"] = "failure"
		meta["message"] = hasError
	else:
		if len(resultList) == 1:
			meta["status"] = "success"
			meta["message"] = resultList[0]
		elif not len(resultList) < keysNumber:
			meta["status"] = "success"
			count = len(resultList) / keysNumber - 1
			for i in xrange(0, count):
				newDict = {}
				newDict[resultList[0].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber]
				newDict[resultList[1].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber + 1]
				newDict[resultList[2].replace(" ", "_").lower()] = resultList[(i + 1) * keysNumber + 2]
				newDict["term_index"] = i
				data.append(newDict)
		else :
			meta["status"] = "failure"
			meta["message"] = "response page contains no schedule information"
	return getFullResponseDictionary(meta, data)


def API_enroll_myClassScheduleTermResponse(questSession):
	result = Parse_enroll_myClassScheduleTerm(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}
	if len(result[1]) == 0:
		meta["status"] = "success"
		data = result[0]
	else:
		meta["status"] = "failure"
		meta["message"] = result[1] #"response page class schedule invalid"
	return getFullResponseDictionary(meta, data)

def API_enroll_searchForClassesResponse(questSession):
	resultDict = Parse_enroll_searchForClasses(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}
	if not len(resultDict) < 1:
		meta["status"] = "success"
		data = resultDict
	else:
		meta["status"] = "failure"
		meta["message"] = "parse seach for classes options error"
	return getFullResponseDictionary(meta, data)

def API_enroll_searchForClassesResultResponse(questSession):
	result, hasError = Parse_enroll_searchForClassesResult(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = []
	if hasError:
		meta["status"] = "failure"
		data = result
		meta["message"] = hasError
	else:
		meta["status"] = "success"
		data = result
		if len(result) == 0:
			meta["message"] = "The search returns no results that match the criteria specified."
	return getFullResponseDictionary(meta, data)

def API_enroll_searchForClassesClassDetail(questSession):
	resultDict, hasError =  Parse_enroll_searchForClassesClassDetail(questSession.currentResponse.content)
	meta = getEmptyMetaDict()
	data = {}
	if hasError:
		meta["status"] = "failure"
		meta["message"] = "There are some error in data"
		data = resultDict
	else:
		meta["status"] = "success"
		data = resultDict
	return getFullResponseDictionary(meta, data)