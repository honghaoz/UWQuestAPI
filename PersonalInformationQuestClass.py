import BasicQuestClass
import requests
import QuestParser

from BasicQuestClass import BasicQuestSession

class PersonalInformationQuestSession(BasicQuestSession):
	""" Subclass for PersonalInformationQuestSession"""
	personalInfoAddressURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_ADDRESSES.GBL"
	personalInfoNameURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_NAMES.GBL"
	personalInfoPhoneNumbersURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_PERS_PHONE.GBL"
	personalInfoEmailsURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_EMAIL_ADDR.GBL"
	personalInfoEnergencyURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_EMERG_CNTCT.GBL"
	personalInfoDemographicInfoURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.SS_CC_DEMOG_DATA.GBL"
	personalInfoCitizenshipURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/UW_SS_MENU.UW_SS_CC_VISA_DOC.GBL"
	personalInfoAbsenceDeclarationURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/CC_PORTFOLIO.UW_SS_CC_ABSENCE.GBL"

	def gotoPersonalInformationStudentCenter(self):
		''' Open "Personal Information" tab on student center page
			@Param
			@Return True/False
		'''
		postPersonalInfo = self.getBasicParameters()
		postPersonalInfo['ICAction'] = 'DERIVED_SSS_SCL_SSS_PERSONAL_INFO'

		response = self.session.post(self.studentCenterURL_HRMS, data = postPersonalInfo)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "POST Personal Information (Student Center) OK"
			# self.gotoMyAcademics_myProgram()
			# print response.content
		else:
			print "POST Personal Information (Student Center) Failed"
			return False

	def gotoPersonalInformation(self):
		''' Open "Personal Information"
			@Param
			@Return True/False
		'''
		postPersonalInfo = self.getBasicParameters()
		postPersonalInfo['ICAction'] = 'DERIVED_SSS_SCL_SS_DEMO_SUM_LINK'

		response = self.session.post(self.studentCenterURL_HRMS, data = postPersonalInfo)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "POST Personal Information OK"
			# self.gotoMyAcademics_myProgram()
			# print response.content
		else:
			print "POST Personal Information Failed"
			return False

	def gotoPersonalInformation_address(self):
		''' Go to address
			@Param
			@Return True/False
		'''
		getData = {
			'Page': 'SS_ADDRESSES',
			'Action': 'C',
		}
		response = self.session.get(self.personalInfoAddressURL, data = getData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "GET Address Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET Address Page Failed"
			return False

	def gotoPersonalInformation_name(self):
		''' Go to name
			@Param
			@Return True/False
		'''
		getData = {
			'Page': 'SS_CC_NAME',
			'Action': 'C',
		}
		response = self.session.get(self.personalInfoNameURL, data = getData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "GET Name Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET Name Page Failed"
			return False

	def gotoPersonalInformation_phoneNumbers(self):
		''' Go to Phone Numbers
			@Param
			@Return True/False
		'''
		getData = {
			'Page': 'SS_CC_PERS_PHONE',
			'Action': 'U',
		}
		response = self.session.get(self.personalInfoPhoneNumbersURL, data = getData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "GET Phone Numbers Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET Phone Numbers Page Failed"
			return False

	def gotoPersonalInformation_email(self):
		''' Go to Email Addresses
			@Param
			@Return True/False
		'''
		getData = {
			'Page': 'SS_CC_EMAIL_ADDR',
			'Action': 'U',
		}
		response = self.session.get(self.personalInfoEmailsURL, data = getData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "GET Email Addresses Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET Email Addresses Page Failed"
			return False

	def gotoPersonalInformation_emgencyContacts(self):
		''' Go to Emergency Contacts
			@Param
			@Return True/False
		'''
		getData = {
			'Page': 'SS_CC_EMRG_CNTCT_L',
			'Action': 'U',
		}
		response = self.session.get(self.personalInfoEnergencyURL, data = getData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "GET Emergency Contacts Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET Emergency Contacts Page Failed"
			return False

	def gotoPersonalInformation_demographicInfo(self):
		''' Go to Demographic Information
			@Param
			@Return True/False
		'''
		getData = {
			'Page': 'SS_CC_DEMOG_DATA',
			'Action': 'U',
		}
		response = self.session.get(self.personalInfoDemographicInfoURL, data = getData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "GET Demographic Information Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET Demographic Information Page Failed"
			return False

	def gotoPersonalInformation_citizenship(self):
		''' Go to Citizenship/Immigration Documents
			@Param
			@Return True/False
		'''
		getData = {
			'Page': 'UW_SS_CC_VISA_DOC',
			'Action': 'U',
		}
		response = self.session.get(self.personalInfoCitizenshipURL, data = getData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "GET Citizenship/Immigration Documents Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET Citizenship/Immigration Documents Page Failed"
			return False

def main():
	# Create a basic quest session
	myBasicQuest = BasicQuestSession("", "")# "userid", "password"
	myBasicQuest.login()

	myPersonalInfoQuestSesson = PersonalInformationQuestSession("", "", myBasicQuest)
	# myQuest.gotoStudentCenter()
	myPersonalInfoQuestSesson.gotoPersonalInformationStudentCenter()
	myPersonalInfoQuestSesson.gotoPersonalInformation()
	myPersonalInfoQuestSesson.gotoPersonalInformation_address()
	# print QuestParser.API_account_loginResponse(myPersonalInfoQuestSesson)
	print QuestParser.API_personalInfo_addressResponse(myPersonalInfoQuestSesson)

	myPersonalInfoQuestSesson.gotoPersonalInformation_name()
	print QuestParser.API_personalInfo_nameResponse(myPersonalInfoQuestSesson)

	myPersonalInfoQuestSesson.gotoPersonalInformation_phoneNumbers()
	print QuestParser.API_personalInfo_phoneResponse(myPersonalInfoQuestSesson)

	myPersonalInfoQuestSesson.gotoPersonalInformation_email()
	print QuestParser.API_personalInfo_emailResponse(myPersonalInfoQuestSesson)

	myPersonalInfoQuestSesson.gotoPersonalInformation_emgencyContacts()
	print QuestParser.API_personalInfo_emergencyContactResponse(myPersonalInfoQuestSesson)
	
	myPersonalInfoQuestSesson.gotoPersonalInformation_demographicInfo()
	# print QuestParser.Parse_personalInfo_demographicInfo(myPersonalInfoQuestSesson.currentResponse.content)
	print QuestParser.API_personalInfo_demographicInfoResponse(myPersonalInfoQuestSesson)
	
	myPersonalInfoQuestSesson.gotoPersonalInformation_citizenship()
	print QuestParser.API_personalInfo_citizenshipResponse(myPersonalInfoQuestSesson)

if __name__ == '__main__':
    main()
