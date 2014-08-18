import BasicQuestClass
import requests

from BasicQuestClass import BasicQuestSession

class MyAcademicQuestSession(BasicQuestSession):
	""" Subclass for myAcademic"""

	myAcademicsURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL"
	myAcademicsGraduateURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/UW_SS_MENU.UW_SS_MYPROG_GRD.GBL"
	myAcademicsGraduateGradesURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL"
	myAcademicsGraduateUnofficialTranscriptURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SS_AA_REPORT1.GBL"

	myAcademicsUndergraduateURL = ""

	def gotoMyAcademics(self):
		''' Go to My Academics (default tab is first one)
			@Param
			@Return True/False
		'''
		postMyAcademics = self.getBasicParameters()
		postMyAcademics['ICAction'] = 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR1' # FIXME: Constant?

		# print "POST: My Academics Page"
		response = self.session.post(self.myAcademicsURL, data = postMyAcademics)
		if response.status_code == requests.codes.ok:
			print "POST My Academics OK"
			self.gotoMyAcademics_myProgram()
		else:
			print "POST My Academics Failed"
			return False
	def gotoMyAcademics_myProgram(self):
		''' Go to my undergrad(grad) program
			@Param
			@Return True/False
		'''
		# if self.isUndergraduate:
		# 	pass
		getMyProgramData = {
			'Page': 'UW_SS_MYPROG_GRD',
			'Action': 'U',
			'ExactKeys': 'Y',
			'TargetFrameName': 'None'
		}
		response = self.session.get(self.myAcademicsGraduateURL, data = getMyProgramData)
		if response.status_code == requests.codes.ok:
			print "GET My Graduate Program Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET My Graduate Program Page Failed"
			return False
	def gotoMyAcademics_grades(self):
		''' Go to my grades
			@Param
			@Return True/False
		'''
		getGradesData = {
			'Page': 'SSR_SSENRL_GRADE',
			'Action': 'A'
		}
		response = self.session.get(self.myAcademicsGraduateGradesURL, data = getGradesData)
		if response.status_code == requests.codes.ok:
			print "GET Grades Page OK"
			self.updateStateNum(response)
			# print response.content
			return True
		else:
			print "GET Grades Page Failed"
			return False

	def gotoMyAcademics_unofficialTranscript(self):
		''' Go to my Unofficial Transcript
			@Param
			@Return True/False
		'''
		getUnofficialTranscriptData = {
			'Page': 'SS_ES_AARPT_TYPE2',
			'Action': 'A'
		}
		response = self.session.get(self.myAcademicsGraduateUnofficialTranscriptURL, data = getUnofficialTranscriptData)
		if response.status_code == requests.codes.ok:
			print "GET Unofficial Transcript Page OK"
			self.updateStateNum(response)
			print response.content
			return True
		else:
			print "GET Unofficial Transcript Page Failed"
			return False

def main():
	myQuest = MyAcademicQuestSession("", "")# "userid", "password"
	myQuest.login()
	myQuest.gotoStudentCenter()
	myQuest.gotoMyAcademics()
	myQuest.gotoMyAcademics_grades()
	myQuest.gotoMyAcademics_unofficialTranscript()

if __name__ == '__main__':
    main()
		

# ################ Login and set cookies ################
# # Start a session to manage cookies
# s = Session()

# questLoginURL = 'https://quest.pecs.uwaterloo.ca/psp/SS/?cmd=login&languageCd=ENG'
# postLoginData = {
# 	'userid': 'h344zhan',
# 	'pwd': 'Zhh358279765099',
# 	'timezoneOffset': '240', # Fix Me
# 	'httpPort': ''
# }

# loginResponse = s.post(questLoginURL, data = postLoginData)
# if loginResponse.status_code == requests.codes.ok:
# 	print "Login Successfully!"

# ################ Operations ################

# print "GET: studentCenter Page"

# # Get main page
# studentCenterURL = 'https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL'
# getMainPageData = {
# 	'PORTALPARAM_PTCNAV': 'HC_SSS_STUDENT_CENTER',
# 	'EOPP.SCNode': 'SA',
# 	'EOPP.SCPortal': 'ACADEMIC',
# 	'EOPP.SCName': 'CO_EMPLOYEE_SELF_SERVICE',
# 	'EOPP.SCLabel': 'Self Service',
# 	'EOPP.SCPTfname': 'CO_EMPLOYEE_SELF_SERVICE',
# 	'FolderPath': 'PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_SSS_STUDENT_CENTER',
# 	'IsFolder': 'false',
# 	'PortalActualURL': 'https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL',
# 	'PortalRegistryName': 'ACADEMIC',
# 	'PortalServletURI': 'https://quest.pecs.uwaterloo.ca/psp/SS/',
# 	'PortalURI': 'https://quest.pecs.uwaterloo.ca/psc/SS/',
# 	'PortalHostNode': 'SA',
# 	'NoCrumbs': 'yes',
# 	'PortalKeyStruct': 'yes',
# }

# mainPageResponse = s.get(studentCenterURL, data = getMainPageData)

# icsid = getICSID(mainPageResponse.content)
# currentStateNum = getStateNum(mainPageResponse.content)

# # Print ICSID
# print "ICSID: " + icsid
# # Print current state num
# print "currentStateNum: " + str(currentStateNum) + '\n'

# # headers={
# # 	'Accept':'*/*',
# # 	'Accept-Encoding':'gzip,deflate,sdch',
# # 	'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6',
# # 	'Connection': 'keep-alive',
# # 	'Content-Length': '356',
# # 	'Origin': 'https://quest.pecs.uwaterloo.ca',
# # 	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
# # 	'Content-Type': 'application/x-www-form-urlencoded',
# # }

# # postPersonalInfoData = {
# # 	'ICAJAX': '1',
# # 	'ICNAVTYPEDROPDOWN': '0',
# # 	'ICType': 'Panel',
# # 	'ICElementNum': '0',
# # 	'ICStateNum': str(currentStateNum),
# # 	'ICAction': 'DERIVED_SSS_SCL_SSS_PERSONAL_INFO',
# # 	'ICXPos': '0',
# # 	'ICYPos': '87',
# # 	'ResponsetoDiffFrame': '-1',
# # 	'TargetFrameName': 'None',
# # 	'FacetPath': 'None',
# # 	'ICFocus': '',
# # 	'ICSaveWarningFilter': '0',
# # 	'ICChanged': '-1',
# # 	'ICResubmit': '0',
# # 	'ICSID': icsid,
# # 	'ICActionPrompt': 'false',
# # 	'ICFind': '',
# # 	'ICAddCount': '',
# # 	'ICAPPCLSDATA': ''
# # }

# # personalInfoResponse = s.post(studentCenterURL, data = postPersonalInfoData)

# # print personalInfoResponse.content

# # personalInfoAddressGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_ADDRESSES.GBL"
# # getAddressData = {
# # 	'Page': 'SS_ADDRESSES',
# # 	'Action': 'C'
# # }

# # addressResponse = s.get(personalInfoAddressGetURL, data = getAddressData)

# # # print addressResponse.content
# # getAddress(addressResponse.content)

# # currentStateNum = getStateNum(addressResponse.content)
# # # Print current state num
# # print "currentStateNum: " + str(currentStateNum) + '\n'

# # personalInfoNameGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_NAMES.GBL?"
# # getNameData = {
# # 	'Page': 'SS_CC_NAME',
# # 	'Action': 'C'
# # }

# # nameResponse = s.get(personalInfoNameGetURL, data = getNameData)

# # # print nameResponse.content

# # currentStateNum = getStateNum(nameResponse.content)
# # # Print current state num
# # print "currentStateNum: " + str(currentStateNum) + '\n'


# # personalInfoPhoneGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_PERS_PHONE.GBL"
# # getPhoneData = {
# # 	'Page': 'SS_CC_PERS_PHONE',
# # 	'Action': 'U'
# # }

# # phoneResponse = s.get(personalInfoPhoneGetURL, data = getPhoneData)

# # # print phoneResponse.content

# # currentStateNum = getStateNum(phoneResponse.content)
# # # Print current state num
# # print "currentStateNum: " + str(currentStateNum) + '\n'



# # personalInfoEmailGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_EMAIL_ADDR.GBL"
# # getEmailData = {
# # 	'Page': 'SS_CC_EMAIL_ADDR',
# # 	'Action': 'U'
# # }

# # emailResponse = s.get(personalInfoEmailGetURL, data = getEmailData)

# # # print emailResponse.content

# # currentStateNum = getStateNum(emailResponse.content)
# # # Print current state num
# # print "currentStateNum: " + str(currentStateNum) + '\n'



# # personalInfoDemographicInfoGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_DEMOG_DATA.GBL"
# # getDemographicInfoData = {
# # 	'Page': 'SS_CC_DEMOG_DATA',
# # 	'Action': 'U'
# # }

# # demographicInfoResponse = s.get(personalInfoDemographicInfoGetURL, data = getDemographicInfoData)

# # # print demographicInfoResponse.content

# # currentStateNum = getStateNum(demographicInfoResponse.content)
# # # Print current state num
# # print "currentStateNum: " + str(currentStateNum) + '\n'




# # personalInfoCitizenshipGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/UW_SS_MENU.UW_SS_CC_VISA_DOC.GBL"
# # getCitizenshipData = {
# # 	'Page': 'UW_SS_CC_VISA_DOC',
# # 	'Action': 'U'
# # }

# # citizenshipResponse = s.get(personalInfoCitizenshipGetURL, data = getCitizenshipData)

# # # print citizenshipResponse.content

# # currentStateNum = getStateNum(citizenshipResponse.content)
# # # Print current state num
# # print "currentStateNum: " + str(currentStateNum) + '\n'

# # classSearchURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.UW_SSR_CLASS_SRCH.GBL"
# # postClassSearch = {
# # 	'ICAJAX': '1',
# # 	'ICNAVTYPEDROPDOWN': '0',
# # 	'ICType': 'Panel',
# # 	'ICElementNum': '0',
# # 	'ICStateNum': str(currentStateNum),
# # 	'ICAction': 'UW_DERIVED_SR_SSR_PB_CLASS_SRCH',
# # 	'ICXPos': '0',
# # 	'ICYPos': '0',
# # 	'ResponsetoDiffFrame': '-1',
# # 	'TargetFrameName': 'None',
# # 	'FacetPath': 'None',
# # 	'ICFocus': '',
# # 	'ICSaveWarningFilter': '0',
# # 	'ICChanged': '-1',
# # 	'ICResubmit': '0',
# # 	'ICSID': icsid,
# # 	'ICActionPrompt': 'false',
# # 	'ICFind': '',
# # 	'ICAddCount': '',
# # 	'ICAPPCLSDATA': '',
# # 	'DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$': '9999',
# # 	'CLASS_SRCH_WRK2_INSTITUTION$31$': 'UWATR',
# # 	'CLASS_SRCH_WRK2_STRM$35$': '1145',
# # 	'CLASS_SRCH_WRK2_SUBJECT$7$': 'CS',
# # 	'CLASS_SRCH_WRK2_CATALOG_NBR$8$': '350',
# # 	'CLASS_SRCH_WRK2_SSR_EXACT_MATCH1': 'E',
# # 	'CLASS_SRCH_WRK2_ACAD_CAREER': 'UG',
# # 	'CLASS_SRCH_WRK2_SSR_OPEN_ONLY$chk': 'Y',
# # 	'CLASS_SRCH_WRK2_SSR_OPEN_ONLY': 'Y',
# # 	'DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$': '9999',
# # }

# # classSearchResponse = s.post(classSearchURL, data = postClassSearch)

# # print classSearchResponse.content

# basicData = {
# 	'ICAJAX':'1',
# 	'ICNAVTYPEDROPDOWN':'0',
# 	'ICType':'Panel',
# 	'ICElementNum':'0',
# 	'ICStateNum': '0', # Need to change
# 	'ICAction':'', # Need to change
# 	'ICXPos':'0',
# 	'ICYPos':'0',
# 	'ResponsetoDiffFrame':'-1',
# 	'TargetFrameName':'None',
# 	'FacetPath':'None',
# 	'ICFocus':'',
# 	'ICSaveWarningFilter':'0',
# 	'ICChanged':'-1',
# 	'ICResubmit':'0',
# 	'ICSID': icsid, # Need to change
# 	'ICActionPrompt':'false',
# 	'ICFind':'',
# 	'ICAddCount':'',
# 	'ICAPPCLSDATA':'',
# 	# More keys maybe added
# }

# print "POST: My Academics Page"

# myAcademicsURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL"
# postMyAcademics = basicData
# postMyAcademics['ICStateNum'] = str(currentStateNum)
# postMyAcademics['ICAction'] = 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR1'

# s.post(myAcademicsURL, data = postMyAcademics)

# print "GET: My Graduate Program Page"
# myAcademicsResponse = s.get("https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/UW_SS_MENU.UW_SS_MYPROG_GRD.GBL?Page=UW_SS_MYPROG_GRD&Action=U&ExactKeys=Y&TargetFrameName=None")

# # print myAcademicResponse.content

# currentStateNum = getStateNum(myAcademicsResponse.content)
# print "currentStateNum: " + str(currentStateNum) + '\n'

#####################

# print "GET: Grades Page"
# gradesResponse = s.get("https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&Action=A")
# currentStateNum = getStateNum(gradesResponse.content)
# print "currentStateNum: " + str(currentStateNum) + '\n'


# gradesURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL"
# postGrades = basicData
# postGrades['ICStateNum'] = str(currentStateNum)
# postGrades['ICAction'] = 'DERIVED_SSS_SCT_SSR_PB_GO'
# postGrades['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
# postGrades['SSR_DUMMY_RECV1$sels$0']  = '0'
# postGrades['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] ='9999'

# print "POST: Grades Page"
# # s.post(gradesURL, data = postsGrade)
# gradesResponse = s.post(gradesURL, data = postGrades)
# # print gradesResponse.content

# currentStateNum = getStateNum(gradesResponse.content)
# print "currentStateNum: " + str(currentStateNum) + '\n'

# postGrades['ICStateNum'] = str(currentStateNum)
# postGrades['ICAction'] = 'DERIVED_SSS_SCT_SSS_TERM_LINK'
# postGrades.pop('SSR_DUMMY_RECV1$sels$0')
# # postGrades['SSR_DUMMY_RECV1$sels$0']  = '1'
# print "POST: Grades Page Return"

# gradesResponse = s.post(gradesURL, data = postGrades)
# # print gradesResponse.content

# currentStateNum = getStateNum(gradesResponse.content)
# print "currentStateNum: " + str(currentStateNum) + '\n'


# postGrades['ICStateNum'] = str(currentStateNum)
# postGrades['ICAction'] = 'DERIVED_SSS_SCT_SSR_PB_GO'
# postGrades['SSR_DUMMY_RECV1$sels$0']  = '1'
# print "POST: Grades Page"

# gradesResponse = s.post(gradesURL, data = postGrades)
# print gradesResponse.content

# currentStateNum = getStateNum(gradesResponse.content)
# print "currentStateNum: " + str(currentStateNum) + '\n'