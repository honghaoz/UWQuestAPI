import requests
import QuestParser

personalInfoAddressURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_ADDRESSES.GBL"
personalInfoNameURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_NAMES.GBL"
personalInfoPhoneNumbersURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_PERS_PHONE.GBL"
personalInfoEmailsURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_EMAIL_ADDR.GBL"
personalInfoEnergencyURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_EMERG_CNTCT.GBL"
personalInfoDemographicInfoURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_DEMOG_DATA.GBL"
personalInfoCitizenshipURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/UW_SS_MENU.UW_SS_CC_VISA_DOC.GBL"
personalInfoAbsenceDeclarationURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.UW_SS_CC_ABSENCE.GBL"

def postPersonalInformation(questSession):
	''' Open "Personal Information"
		@Param
		@Return True/False
	'''
	if questSession.currentPOSTpage is "PERSONAL_INFORMATION":
		print "POST Personal Information: Already In"
		return True
	else :
		postPersonalInfo = questSession.getBasicParameters()
		postPersonalInfo['ICAction'] = 'DERIVED_SSS_SCL_SS_DEMO_SUM_LINK'

		response = questSession.session.post(questSession.studentCenterURL_HRMS, data = postPersonalInfo, allow_redirects = False)
		questSession.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "POST Personal Information OK"
			questSession.currentPOSTpage = "PERSONAL_INFORMATION"
			return True
		else:
			print "POST Personal Information Failed"
			return False

def gotoPersonalInformation_address(questSession):
	''' Go to address
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'SS_ADDRESSES',
		'Action': 'C',
	}
	response = questSession.session.get(personalInfoAddressURL, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if questSession.updateStateNum(response):
			print "GET Address Page OK"
			# print response.content
			return True
	print "GET Address Page Failed"
	return False

def gotoPersonalInformation_name(questSession):
	''' Go to name
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'SS_CC_NAME',
		'Action': 'C',
	}
	response = questSession.session.get(personalInfoNameURL, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if questSession.updateStateNum(response):
			print "GET Name Page OK"
			# print response.content
			return True
	print "GET Name Page Failed"
	return False

def gotoPersonalInformation_phoneNumbers(questSession):
	''' Go to Phone Numbers
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'SS_CC_PERS_PHONE',
		'Action': 'U',
	}
	response = questSession.session.get(personalInfoPhoneNumbersURL, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if questSession.updateStateNum(response):
			print "GET Phone Numbers Page OK"
			# print response.content
			return True
	print "GET Phone Numbers Page Failed"
	return False

def gotoPersonalInformation_email(questSession):
	''' Go to Email Addresses
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'SS_CC_EMAIL_ADDR',
		'Action': 'U',
	}
	response = questSession.session.get(personalInfoEmailsURL, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if questSession.updateStateNum(response):
			print "GET Email Addresses Page OK"
			# print response.content
			return True
	print "GET Email Addresses Page Failed"
	return False

def gotoPersonalInformation_emgencyContacts(questSession):
	''' Go to Emergency Contacts
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'SS_CC_EMRG_CNTCT_L',
		'Action': 'U',
	}
	response = questSession.session.get(personalInfoEnergencyURL, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if questSession.updateStateNum(response):
			print "GET Emergency Contacts Page OK"
			# print response.content
			return True
	print "GET Emergency Contacts Page Failed"
	return False

def gotoPersonalInformation_demographicInfo(questSession):
	''' Go to Demographic Information
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'SS_CC_DEMOG_DATA',
		'Action': 'U',
	}
	response = questSession.session.get(personalInfoDemographicInfoURL, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if questSession.updateStateNum(response):
			print "GET Demographic Information Page OK"
			# print response.content
			return True
	print "GET Demographic Information Page Failed"
	return False

def gotoPersonalInformation_citizenship(questSession):
	''' Go to Citizenship/Immigration Documents
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'UW_SS_CC_VISA_DOC',
		'Action': 'U',
	}
	response = questSession.session.get(personalInfoCitizenshipURL, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if questSession.updateStateNum(response):
			print "GET Citizenship/Immigration Documents Page OK"
			# print response.content
			return True
	print "GET Citizenship/Immigration Documents Page Failed"
	return False

def main():
	pass
	
	# Create a basic quest session
	# myBasicQuest = BasicQuestSession("h344zhan", "Zhh358279765099")# "userid", "password"
	# myBasicQuest.login()

	# myPersonalInfoQuestSesson = PersonalInformationQuestSession("", "", myBasicQuest)

	# myPersonalInfoQuestSesson.postPersonalInformation()

	# myPersonalInfoQuestSesson.gotoPersonalInformation_address()
	# print QuestParser.API_personalInfo_addressResponse(myPersonalInfoQuestSesson)

	# myPersonalInfoQuestSesson.gotoPersonalInformation_name()
	# print QuestParser.API_personalInfo_nameResponse(myPersonalInfoQuestSesson)

	# myPersonalInfoQuestSesson.gotoPersonalInformation_phoneNumbers()
	# print QuestParser.API_personalInfo_phoneResponse(myPersonalInfoQuestSesson)

	# myPersonalInfoQuestSesson.gotoPersonalInformation_email()
	# print QuestParser.API_personalInfo_emailResponse(myPersonalInfoQuestSesson)

	# myPersonalInfoQuestSesson.gotoPersonalInformation_emgencyContacts()
	# print QuestParser.API_personalInfo_emergencyContactResponse(myPersonalInfoQuestSesson)
	
	# myPersonalInfoQuestSesson.gotoPersonalInformation_demographicInfo()
	# print QuestParser.API_personalInfo_demographicInfoResponse(myPersonalInfoQuestSesson)
	
	# myPersonalInfoQuestSesson.gotoPersonalInformation_citizenship()
	# print QuestParser.API_personalInfo_citizenshipResponse(myPersonalInfoQuestSesson)

if __name__ == '__main__':
    main()
