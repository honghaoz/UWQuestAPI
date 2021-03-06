import requests
from requests import Request, Session
from bs4 import BeautifulSoup
import re
import copy
from datetime import datetime, date, time

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

# Error code constants
kErrorInvalidUserPassword = 11
kErrorUpdateICSID = 12
kErrorInvalidStudentPage = 13
kErrorHTTPStatus = 14

# TODO: timeout handling, network error handling
class QuestSession(object):
	session = Session()
	isLogin = False
	isWrongPassword = False
	userid = ""
	password = ""
	icsid = ""
	currentStateNum = 0
	isUndergraduate = True
	# currentResponse
	currentError = "" # Error message
	currentErrorCode = 0

	currentPOSTpage = "" # Log which page we are at
	# currentResult

	loginRetryTimes = 0
	loginRetryMaxTime = 3

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
	questLogoutURL = "https://quest.pecs.uwaterloo.ca/psp/SS/ACADEMIC/SA/?cmd=logout"
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
			result = self.gotoStudentCenter()
			if(result):
				self.loginRetryTimes = 0
				self.isLogin = True
				self.currentError = ""
				self.currentErrorCode = 0
				print "Login Successfully!"
				return True
			else:
				if self.currentErrorCode == kErrorInvalidUserPassword:
					self.isLogin = False
					return False
				self.loginRetryTimes += 1
				if self.loginRetryTimes < self.loginRetryMaxTime:
					return self.login()
		self.isLogin = False
		print "Login Failed!"
		return False

	def logout(self):
		response = self.session.get(self.questLogoutURL)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "Logout Successfully"
			self.isLogin = False
			return True
		else:
			print "Logout Failed!"
			return False
	
	def checkIsExpired(self):
		''' Check whether login is expired, return True if expired
			@Param 
			@Return True if expired
		'''
		# 16_Sep_2014_03:54:03_GMT
		timeString = self.currentResponse.cookies["PS_TOKENEXPIRE"]
		try:
			lastActiveTime = datetime.strptime(timeString, "%d_%b_%Y_%H:%M:%S_%Z")
			currentTime = datetime.utcnow()
			timeDelta = currentTime - lastActiveTime
			# If elasped seconds is greater than 20min, cookie is expired
			if timeDelta.seconds > 20 * 60:
				print "Cookies is expired"
				self.isLogin = False
				return True
			else:
				print "Cookies is not expired"
				return False
		except:
			print "Cookies invalid"
			self.isLogin = False
			return False

	def checkIsOnLoginPage(self):
		soup = BeautifulSoup(self.currentResponse.content)
		if self.currentResponse.status_code == requests.codes.ok:
			findLoginID = soup.find(id="login")
			if findLoginID:
				self.isWrongPassword = True
				self.isLogin = False
				return True
		self.isWrongPassword = False
		return False

	def checkIsValid(self):
		soup = BeautifulSoup(self.currentResponse.content)
		# print soup.prettify()
		isValid = soup.find(id="ICSID")
		if isValid:
			return True
		else:
			self.isLogin = False
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
			if not self.checkIsOnLoginPage():
				isValid = self.checkIsValid()
				if isValid:
					self.checkIsUndergraduate(response)
					if self.updateICSID(response) is True:
						print "GET Student Center OK"
						return True
					else:
						print "GET Student Center Failed: updateICSID failed"
						self.currentError = "GET Student Center Failed: updateICSID failed"
						self.currentErrorCode = kErrorUpdateICSID
						return False
				else:
					print "GET Student Center Failed: invalid page"
					self.currentError = "GET Student Center Failed: invalid page"
					self.currentErrorCode = kErrorInvalidStudentPage
					return False
			else:
				print "GET Student Center Failed: Wrong username/password"
				self.currentError = "GET Student Center Failed: Wrong username/password"
				self.currentErrorCode = kErrorInvalidUserPassword
				return False
		else:
			print "GET Student Center Failed: status code %s" % str(response.status_code)
			self.currentError = "GET Student Center Failed: status code %s" % str(response.status_code)
			self.currentErrorCode = kErrorHTTPStatus
			return False

	# def checkIsLogin(self):
	# 	if not self.isLogin:
	# 		if not (self.login()):
	# 			print "Cannot login!"
	# 			return False
	# 	else:
	# 		return True

	# def updateLoginSession(self):
	# 	if self.checkIsValid():
	# 		pass

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

	def postEnroll_myClassSchedule_termIndex(self, termIndex):
		return Enroll.postEnroll_myClassSchedule_termIndex(self, termIndex)

	def gotoEnroll_searchForClasses(self):
		return Enroll.gotoEnroll_searchForClasses(self)

	def postEnroll_searchForClasses(self, institution, term, course_subject, course_number, course_number_relation, course_career, open_only, class_number = ""):
		return Enroll.postEnroll_searchForClasses(self, institution, term, course_subject, course_number, course_number_relation, course_career, open_only, class_number = "")

	def postEnroll_searchForClassesDetailInfo(self, action):
		return Enroll.postEnroll_searchForClassesDetailInfo(self, action)

def main():
	myQuest = QuestSession("", "") # "userid", "password"
	myQuest.login()

	myQuest.checkIsExpired()
	# print requests.utils.dict_from_cookiejar(myQuest.currentResponse.cookies)

	# # Personal Information
	# myQuest.postPersonalInformation()

	# myQuest.gotoPersonalInformation_address()
	# print QuestParser.API_personalInfo_addressResponse(myQuest)

	# myQuest.gotoPersonalInformation_name()
	# print QuestParser.API_personalInfo_nameResponse(myQuest)

	# myQuest.gotoPersonalInformation_phoneNumbers()
	# print QuestParser.API_personalInfo_phoneResponse(myQuest)

	# myQuest.gotoPersonalInformation_email()
	# print QuestParser.API_personalInfo_emailResponse(myQuest)

	# myQuest.gotoPersonalInformation_emgencyContacts()
	# print QuestParser.API_personalInfo_emergencyContactResponse(myQuest)
	
	# myQuest.gotoPersonalInformation_demographicInfo()
	# print QuestParser.API_personalInfo_demographicInfoResponse(myQuest)
	
	# myQuest.gotoPersonalInformation_citizenship()
	# print QuestParser.API_personalInfo_citizenshipResponse(myQuest)

	# print requests.utils.dict_from_cookiejar(myQuest.currentResponse.cookies)

if __name__ == '__main__':
    main()
