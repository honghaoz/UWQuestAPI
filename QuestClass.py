import requests
from requests import Request, Session
from bs4 import BeautifulSoup
import re
import copy

# Import outer files
import QuestParser
import PersonalInformation
import MyAcademics
import Enroll

################ Helper Functions ################

# Get ICSID from html code, ICSID is used for POST method
def getICSID(html):
	s = re.findall("<.*?id=['\"]ICSID['\"].*?>", html)[0]
	s = re.findall("value=['\"].*?['\"]", s)[0]
	s = s.replace("value=","").replace('"',"").replace("'","")
	return s

# Get StateNum from html code, StateNum is used for POST method
def getStateNum(html):
	s = re.findall("<.*?id=['\"]ICStateNum['\"].*?>", html)[0]
	s = re.findall("value=['\"].*?['\"]", s)[0]
	s = s.replace("value=","").replace('"',"").replace("'","")
	return int(s)

# TODO: timeout handling, network error handling
class QuestSession(object):
	session = Session()
	isLogin = False
	userid = ""
	password = ""
	icsid = ""
	currentStateNum = 0
	isUndergraduate = True
	# currentResponse
	currentError = "" # Error message

	currentPOSTpage = "" # Log which page we are at
	# currentResult

	# Post parameters
	basicPostData = {
		'ICAJAX':'1',
		'ICNAVTYPEDROPDOWN':'0',
		'ICType':'Panel',
		'ICElementNum':'0',
		'ICStateNum': str(currentStateNum), # Need to change
		'ICAction':'', # Need to change
		'ICXPos':'0',
		'ICYPos':'0',
		'ResponsetoDiffFrame':'-1',
		'TargetFrameName':'None',
		'FacetPath':'None',
		'ICFocus':'',
		'ICSaveWarningFilter':'0',
		'ICChanged':'-1',
		'ICResubmit':'0',
		'ICSID': icsid, # Need to change
		'ICActionPrompt':'false',
		'ICFind':'',
		'ICAddCount':'',
		'ICAPPCLSDATA':'',
		# More keys maybe added
	}

	# Login
	questLoginURL = 'https://quest.pecs.uwaterloo.ca/psp/SS/?cmd=login&languageCd=ENG'
	studentCenterURL_SA = 'https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL'
	studentCenterURL_HRMS = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL"

 	def __init__(self, userid, password):
 		""" Initialization
 			Initilize a new one session, only provide userid and password
 		"""
 		print "Initilize new one"
 		self.session = Session()
 		self.isLogin = False
 		self.userid = userid
 		self.password = password

	# Login
	# Side effects: isLogin is changed
	def login(self):
		''' Login
			@Param 
			@Return True if Successful
		'''
		print "Login Start..."
		postLoginData = {
			'userid': self.userid,
			'pwd': self.password,
			'timezoneOffset': '0', # Fix Me '240'
			'httpPort': ''
		}
		response = self.session.post(self.questLoginURL, data = postLoginData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			# Go to student center
			if(self.gotoStudentCenter()):
				self.isLogin = True
				print "Login Successfully!"
				return True
		self.isLogin = False
		print "Login Failed!"
		return False
	
	# TODO
	def checkIsExpiration(self):
		''' Check whether login is expired, return True if expired
			@Param 
			@Return True if expired
		'''
		return False

	def checkIsUndergraduate(self, response):
		''' Check whether logined account is undergraduate
			@Param requests response
			@Return 
		'''
		soup = BeautifulSoup(response.content)
		academicTable = soup.find(id='ACE_DERIVED_SSS_SCL_SS_ACAD_INFO_LINK')
		resultList = map(lambda x: x.strip(), filter(lambda x: len(x) > 0, re.sub("\<.*?\>", "", str(academicTable)).replace(" \r", ", ").replace("\xc2\xa0", "").split("\n")))
		# FIXME
		if len(resultList) == 3:
			print "Graduate student"
			self.isUndergraduate = False
		else:
			print "Undergraduate student"
			self.isUndergraduate = True

	def updateICSID(self, response):
		''' Update ICSID and StateNum
			@Param requests response
			@Return 
		'''
		try:
			self.icsid = getICSID(response.content)
			# Print ICSID
			print "ICSID: " + self.icsid
		except:
			return False
		return self.updateStateNum(response)

	def updateStateNum(self, response):
		''' Update StateNum
			@Param requests response
			@Return 
		'''
		try:
			self.currentStateNum = getStateNum(response.content)
			# Print current state num
			print "Current StateNum: " + str(self.currentStateNum)
		except:
			return False
		return True

	def getBasicParameters(self):
		''' return a new post data dictionary with updated ICSID and StateNum
			@Param
			@Return new post data dictionary
		'''
		newPostData = copy.copy(self.basicPostData)
		newPostData['ICStateNum'] = str(self.currentStateNum)
		newPostData['ICSID'] = self.icsid
		return newPostData

	def gotoStudentCenter(self):
		''' Go to Student Center Page (main page)
			@Param 
			@Return True/False
		'''
		getStudentCenterData = {
			'PORTALPARAM_PTCNAV': 'HC_SSS_STUDENT_CENTER',
			'EOPP.SCNode': 'SA',
			'EOPP.SCPortal': 'ACADEMIC',
			'EOPP.SCName': 'CO_EMPLOYEE_SELF_SERVICE',
			'EOPP.SCLabel': 'Self Service',
			'EOPP.SCPTfname': 'CO_EMPLOYEE_SELF_SERVICE',
			'FolderPath': 'PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_SSS_STUDENT_CENTER',
			'IsFolder': 'false',
			'PortalActualURL': 'https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL',
			'PortalRegistryName': 'ACADEMIC',
			'PortalServletURI': 'https://quest.pecs.uwaterloo.ca/psp/SS/',
			'PortalURI': 'https://quest.pecs.uwaterloo.ca/psc/SS/',
			'PortalHostNode': 'SA',
			'NoCrumbs': 'yes',
			'PortalKeyStruct': 'yes',
		}

		response = self.session.get(self.studentCenterURL_SA, data = getStudentCenterData)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			self.checkIsUndergraduate(response)
			if self.updateICSID(response) is True:
				print "GET Student Center OK"
				return True
		print "GET Student Center Failed"
		return False

	# Personal Information
	def postPersonalInformation(self):
		return PersonalInformation.postPersonalInformation(self)

	def gotoPersonalInformation_address(self):
		return PersonalInformation.gotoPersonalInformation_address(self)

	def gotoPersonalInformation_name(self):
		return PersonalInformation.gotoPersonalInformation_name(self)

	def gotoPersonalInformation_phoneNumbers(self):
		return PersonalInformation.gotoPersonalInformation_phoneNumbers(self)

	def gotoPersonalInformation_email(self):
		return PersonalInformation.gotoPersonalInformation_email(self)
	
	def gotoPersonalInformation_emgencyContacts(self):
		return PersonalInformation.gotoPersonalInformation_emgencyContacts(self)

	def gotoPersonalInformation_demographicInfo(self):
		return PersonalInformation.gotoPersonalInformation_demographicInfo(self)

	def gotoPersonalInformation_citizenship(self):	
		return PersonalInformation.gotoPersonalInformation_citizenship(self)

	# My Academics
	def postMyAcademics(self):
		return MyAcademics.postMyAcademics(self)

	def gotoMyAcademics_myProgram(self):
		return MyAcademics.gotoMyAcademics_myProgram(self)

	def gotoMyAcademics_grades(self):
		return MyAcademics.gotoMyAcademics_grades(self)

	def postMyAcademics_grades_termIndex(self, termIndex):
		return MyAcademics.postMyAcademics_grades_termIndex(self, termIndex)

	def postMyAcademics_grades_termLink(self):
		return MyAcademics.postMyAcademics_grades_termLink(self)

	def gotoMyAcademics_unofficialTranscript(self):
		return MyAcademics.gotoMyAcademics_unofficialTranscript(self)

	def postMyAcademics_unofficialTranscript_option(self, academic_option, type_option):
		return MyAcademics.postMyAcademics_unofficialTranscript_option(self, academic_option, type_option)

	def postMyAcademics_unofficialTranscript_optionLink(self):
		return MyAcademics.postMyAcademics_unofficialTranscript_optionLink(self)

	def gotoMyAcademics_advisors(self):
		return MyAcademics.gotoMyAcademics_advisors(self)

	# def gotoMyAcademics_graduateOfferLetters(self):
	# 	return MyAcademics.gotoMyAcademics_graduateOfferLetters(self)

	# Enroll
	def postEnroll(self):
		return Enroll.postEnroll(self)

	def gotoEnroll_myClassSchedule(self):
		return Enroll.gotoEnroll_myClassSchedule(self)

def main():
	myQuest = QuestSession("", "") # "userid", "password"
	myQuest.login()

	# Personal Information
	myQuest.postPersonalInformation()

	myQuest.gotoPersonalInformation_address()
	print QuestParser.API_personalInfo_addressResponse(myQuest)

	myQuest.gotoPersonalInformation_name()
	print QuestParser.API_personalInfo_nameResponse(myQuest)

	myQuest.gotoPersonalInformation_phoneNumbers()
	print QuestParser.API_personalInfo_phoneResponse(myQuest)

	myQuest.gotoPersonalInformation_email()
	print QuestParser.API_personalInfo_emailResponse(myQuest)

	myQuest.gotoPersonalInformation_emgencyContacts()
	print QuestParser.API_personalInfo_emergencyContactResponse(myQuest)
	
	myQuest.gotoPersonalInformation_demographicInfo()
	print QuestParser.API_personalInfo_demographicInfoResponse(myQuest)
	
	myQuest.gotoPersonalInformation_citizenship()
	print QuestParser.API_personalInfo_citizenshipResponse(myQuest)

if __name__ == '__main__':
    main()
