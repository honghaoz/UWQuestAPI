import QuestClass
import requests
import QuestParser
# from QuestClass import QuestSession

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
		response = self.session.get(myAcademicsGraduateURL, data = getMyProgramData, allow_redirects = False)
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
	response = self.session.get(myAcademicsGraduateGradesURL, data = getGradesData, allow_redirects = False)
	self.currentResponse = response
	if response.status_code == requests.codes.ok:
		if (self.updateStateNum(response)):
			print "GET Grades Page OK"
			# print response.content
			return True
	print "GET Grades Page Failed"
	return False

def postMyAcademics_grades_termIndex(self, termIndex):
	''' POST to get grades for one term
		@Param term index return from gotoMyAcademics_grades
		@Return True/False
	'''
	# If not in the right post postition, change to right post position
	if not (self.currentPOSTpage is "MY_ACADEMICS_HOME" or self.currentPOSTpage is "MY_ACADEMICS_GRADES_TERM_LINK"):
		if not self.postMyAcademics_grades_termLink():
			print "POST grades with index: %d Failed" % termIndex
			return False

	# Start to post
	postGradesData = self.getBasicParameters()
	postGradesData['ICAction'] = 'DERIVED_SSS_SCT_SSR_PB_GO'
	postGradesData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
	postGradesData['SSR_DUMMY_RECV1$sels$0'] = termIndex # str(termIndex)
	postGradesData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'

	response = self.session.post(myAcademicsGraduateGradesURL, data = postGradesData, allow_redirects = False)
	self.currentResponse = response
	if response.status_code == requests.codes.ok:
		print "POST grades with index: %d OK" % termIndex
		self.currentPOSTpage = "MY_ACADEMICS_GRADES_ONE_TERM"
		# self.gotoMyAcademics_myProgram()
		return True
	else:
		print "POST grades with index: %d Failed" % termIndex
		return False
		
def postMyAcademics_grades_termLink(self):
	if self.currentPOSTpage is "MY_ACADEMICS_GRADES_TERM_LINK":
		print "POST Grades term link: Already In"
		return True
	else :
		postData = self.getBasicParameters()
		postData['ICAction'] = 'DERIVED_SSS_SCT_SSS_TERM_LINK'
		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
		response = self.session.post(myAcademicsGraduateGradesURL, data = postData, allow_redirects = False)
		self.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "POST grades term link OK"
			self.currentPOSTpage = "MY_ACADEMICS_GRADES_TERM_LINK"
			return True
		else:
			print "POST grades term link Failed"
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
	response = self.session.get(myAcademicsGraduateUnofficialTranscriptURL, data = getUnofficialTranscriptData, allow_redirects = False)
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
	response = self.session.get(myAcademicsGraduateAdvisorsURL, data = getAdvisorsData, allow_redirects = False)
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
	response = self.session.get(myAcademicsGraduateGradOfferURL, data = getGraduateOfferData, allow_redirects = False)
	self.currentResponse = response
	if response.status_code == requests.codes.ok:
		if (self.updateStateNum(response)):
			print "GET Graduate Offer Letters Page OK"
			# print response.content
			return True
	print "GET Graduate Offer Letters Page Failed"
	return False

def main():
	myQuest = QuestClass.QuestSession("h344zhan", "Zhh358279765099") # "userid", "password"
	myQuest.login()

	myQuest.postMyAcademics()

	myQuest.gotoMyAcademics_myProgram()
	print QuestParser.API_myAcademics_myProgramResponse(myQuest)

	myQuest.gotoMyAcademics_grades()
	print QuestParser.API_myAcademics_gradesResponse(myQuest)

	myQuest.postMyAcademics_grades_termIndex(1)

	print QuestParser.API_myAcademics_gradesTermResponse(myQuest)
	# myQuest.postMyAcademics_grades_termIndex(1)

	# myQuest.gotoMyAcademics_unofficialTranscript()
	# myQuest.gotoMyAcademics_advisors()
	# myQuest.gotoMyAcademics_graduateOfferLetters()

if __name__ == '__main__':
    main()
		

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