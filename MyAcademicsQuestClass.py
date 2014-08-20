import BasicQuestClass
import requests
import QuestParser
from BasicQuestClass import BasicQuestSession

class MyAcademicQuestSession(BasicQuestSession):
	""" Subclass for myAcademic"""

	myAcademicsGraduateURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/UW_SS_MENU.UW_SS_MYPROG_GRD.GBL"
	myAcademicsGraduateGradesURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL"
	myAcademicsGraduateUnofficialTranscriptURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SS_AA_REPORT1.GBL"
	myAcademicsGraduateAdvisorsURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSR_SSADVR.GBL"
	myAcademicsGraduateGradOfferURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/UW_SS_MENU.UW_SS_GRD_OFFR_CTR.GBL"

	# TODO:
	myAcademicsUndergraduateURL = ""
	myAcademicsUndergraduateGradesURL = ""
	myAcademicsUndergraduateUnofficialTranscriptURL = ""

	def postMyAcademics(self):
		''' Go to My Academics (default tab is first one)
			@Param
			@Return True/False
		'''
		if self.currentPOSTpage is "MY_ACADEMICS_HOME":
			print "POST My Academics: Already In"
			return True
		else :	
			postMyAcademics = self.getBasicParameters()
			postMyAcademics['ICAction'] = 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR1'

			# print "POST: My Academics Page"
			response = self.session.post(self.studentCenterURL_HRMS, data = postMyAcademics, allow_redirects = False)
			self.currentResponse = response
			if response.status_code == requests.codes.ok:
				print "POST My Academics OK"
				self.currentPOSTpage = "MY_ACADEMICS_HOME"
				# self.gotoMyAcademics_myProgram()
				return True
			else:
				print "POST My Academics Failed"
				return False

	def gotoMyAcademics_myProgram(self):
		''' Go to my undergrad(grad) program
			@Param
			@Return True/False
		'''
		if self.isUndergraduate:
			# TODO
			pass
		else:
			getMyProgramData = {
				'Page': 'UW_SS_MYPROG_GRD',
				'Action': 'U',
				'ExactKeys': 'Y',
				'TargetFrameName': 'None'
			}
			response = self.session.get(self.myAcademicsGraduateURL, data = getMyProgramData, allow_redirects = False)
			self.currentResponse = response
			if response.status_code == requests.codes.ok:
				if (self.updateStateNum(response)):
					print "GET My Graduate Program Page OK"
					# print response.content
					return True
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
		response = self.session.get(self.myAcademicsGraduateGradesURL, data = getGradesData, allow_redirects = False)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			if (self.updateStateNum(response)):
				print "GET Grades Page OK"
				# print response.content
				return True
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
		response = self.session.get(self.myAcademicsGraduateUnofficialTranscriptURL, data = getUnofficialTranscriptData, allow_redirects = False)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			if (self.updateStateNum(response)):
				print "GET Unofficial Transcript Page OK"
				# print response.content
				return True
		print "GET Unofficial Transcript Page Failed"
		return False

	def gotoMyAcademics_advisors(self):
		''' Go to my My Advisors
			@Param
			@Return True/False
		'''
		getAdvisorsData = {
			'Page': 'SSR_SSADVR',
			'Action': 'U'
		}
		response = self.session.get(self.myAcademicsGraduateAdvisorsURL, data = getAdvisorsData, allow_redirects = False)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			if (self.updateStateNum(response)):
				print "GET My Advisors Page OK"
				# print response.content
				return True
		print "GET My Advisors Page Failed"
		return False

	def gotoMyAcademics_graduateOfferLetters(self):
		''' Go to my Graduate Offer Letters
			@Param
			@Return True/False
		'''
		getGraduateOfferData = {
			'Page': 'UW_SS_GRD_OFFR_CTR',
			'Action': 'U'
		}
		response = self.session.get(self.myAcademicsGraduateGradOfferURL, data = getGraduateOfferData, allow_redirects = False)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			if (self.updateStateNum(response)):
				print "GET Graduate Offer Letters Page OK"
				# print response.content
				return True
		print "GET Graduate Offer Letters Page Failed"
		return False

def main():
	myBasicQuest = BasicQuestSession("", "")# "userid", "password"
	myBasicQuest.login()

	myAcamedicsQuestSession = MyAcademicQuestSession("", "", myBasicQuest)
	myAcamedicsQuestSession.postMyAcademics()

	myAcamedicsQuestSession.gotoMyAcademics_myProgram()
	print QuestParser.API_myAcademics_myProgramResponse(myAcamedicsQuestSession)

	myAcamedicsQuestSession.gotoMyAcademics_grades()
	print QuestParser.API_myAcademics_gradesResponse(myAcamedicsQuestSession)

	# myAcamedicsQuestSession.gotoMyAcademics_unofficialTranscript()
	# myAcamedicsQuestSession.gotoMyAcademics_advisors()
	# myAcamedicsQuestSession.gotoMyAcademics_graduateOfferLetters()

if __name__ == '__main__':
    main()
		
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