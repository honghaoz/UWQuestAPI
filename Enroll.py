import QuestClass
import requests
import QuestParser
from bs4 import BeautifulSoup

enroll_myClassScheduleURL_HRMS = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"


def postEnroll(questSession):
	''' Go to Enroll
		@Param
		@Return True/False
	'''
	if questSession.currentPOSTpage is "ENROLL_HOME":
		print "POST Enroll: Already In"
		return True
	else :	
		postData = questSession.getBasicParameters()
		postData['ICAction'] = 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR2'

		response = questSession.session.post(questSession.studentCenterURL_HRMS, data = postData, allow_redirects = False)
		questSession.currentResponse = response
		if response.status_code == requests.codes.ok:
			print "POST Enroll OK"
			questSession.currentPOSTpage = "ENROLL_HOME"
			# questSession.gotoMyAcademics_myProgram()
			return True
		else:
			print "POST Enroll Failed"
			return False

def gotoEnroll_myClassSchedule(questSession):
	''' Go to my my class schedule
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'SSR_SSENRL_LIST',
		'Action': 'A',
		'ExactKeys': 'Y',
		'TargetFrameName': 'None'
	}
	response = questSession.session.get(enroll_myClassScheduleURL_HRMS, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if (questSession.updateStateNum(response)):
			print "GET My Class Schedule Page OK"
			# print response.content
			return True
	print "GET My Class Schedule Page Failed"
	return False

# def gotoMyAcademics_grades(questSession):
# 	''' Go to my grades
# 		@Param
# 		@Return True/False
# 	'''
# 	getGradesData = {
# 		'Page': 'SSR_SSENRL_GRADE',
# 		'Action': 'A'
# 	}
# 	response = questSession.session.get(myAcademicsGraduateGradesURL_HRMS, data = getGradesData, allow_redirects = False)
# 	questSession.currentResponse = response
# 	if response.status_code == requests.codes.ok:
# 		if (questSession.updateStateNum(response)):
# 			print "GET Grades Page OK"
# 			# print response.content
# 			return True
# 	print "GET Grades Page Failed"
# 	return False

# def postMyAcademics_grades_termIndex(questSession, termIndex):
# 	''' POST to get grades for one term
# 		@Param term index return from gotoMyAcademics_grades
# 		@Return True/False
# 	'''
# 	# If not in the right post postition, change to right post position
# 	if not (questSession.currentPOSTpage is "MY_ACADEMICS_HOME"): # or questSession.currentPOSTpage is "MY_ACADEMICS_GRADES_TERM_LINK"):
# 		if not gotoMyAcademics_grades(questSession): #questSession.postMyAcademics_grades_termLink():
# 			print "POST grades with index: %d Failed" % termIndex
# 			return False

# 	# Start to post
# 	postGradesData = questSession.getBasicParameters()
# 	postGradesData['ICAction'] = 'DERIVED_SSS_SCT_SSR_PB_GO'
# 	postGradesData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
# 	postGradesData['SSR_DUMMY_RECV1$sels$0'] = termIndex # str(termIndex)
# 	postGradesData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
# 	print postGradesData["ICStateNum"]

# 	response = questSession.session.post(myAcademicsGraduateGradesURL_HRMS, data = postGradesData, allow_redirects = False)
# 	questSession.currentResponse = response
# 	if response.status_code == requests.codes.ok:
# 		print "POST grades with index: %d OK" % termIndex
# 		questSession.currentStateNum += 1
# 		questSession.currentPOSTpage = "MY_ACADEMICS_GRADES_ONE_TERM"
# 		# questSession.gotoMyAcademics_myProgram()
# 		return True
# 	else:
# 		print "POST grades with index: %d Failed" % termIndex
# 		return False
		
# # def postMyAcademics_grades_termLink(questSession):
# # 	if questSession.currentPOSTpage is "MY_ACADEMICS_GRADES_TERM_LINK":
# # 		print "POST Grades term link: Already In"
# # 		return True
# # 	else :
# # 		postData = questSession.getBasicParameters()
# # 		postData['ICAction'] = 'DERIVED_SSS_SCT_SSS_TERM_LINK'
# # 		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
# # 		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
# # 		print postData["ICStateNum"]
# # 		response = questSession.session.post(myAcademicsGraduateGradesURL_HRMS, data = postData, allow_redirects = False)
# # 		questSession.currentResponse = response
# # 		if response.status_code == requests.codes.ok:
# # 			# print response.content
# # 			print "POST grades term link OK"
# # 			questSession.currentStateNum += 1
# # 			questSession.currentPOSTpage = "MY_ACADEMICS_GRADES_TERM_LINK"
# # 			return True
# # 		else:
# # 			print "POST grades term link Failed"
# # 			return False


# def gotoMyAcademics_unofficialTranscript(questSession):
# 	''' Go to my Unofficial Transcript
# 		@Param
# 		@Return True/False
# 	'''
# 	getUnofficialTranscriptData = {
# 		'Page': 'SS_ES_AARPT_TYPE2',
# 		'Action': 'A'
# 	}
# 	response = questSession.session.get(myAcademicsGraduateUnofficialTranscriptURL_HRMS, data = getUnofficialTranscriptData, allow_redirects = False)
# 	questSession.currentResponse = response
# 	if response.status_code == requests.codes.ok:
# 		if (questSession.updateStateNum(response)):
# 			print "GET Unofficial Transcript Page OK"
# 			# print response.content
# 			return True
# 	print "GET Unofficial Transcript Page Failed"
# 	return False

# # Transcript is stored in questSession.currentResult
# def postMyAcademics_unofficialTranscript_option(questSession, academic_option, type_option):
# 	# If not in the right post postition, change to right post position
# 	if not (questSession.currentPOSTpage is "MY_ACADEMICS_HOME"): #or questSession.currentPOSTpage is "MY_ACADEMICS_UNOFFICIAL_OPTION_LINK"):
# 		if not gotoMyAcademics_unofficialTranscript(questSession): #questSession.postMyAcademics_unofficialTranscript_optionLink():
# 			print "POST Unofficial with option: (%s, %s) Failed" % (academic_option, type_option)
# 			return False

# 	# Start to post
# 	postData = questSession.getBasicParameters()
# 	postData['ICAction'] = 'DERIVED_AA2_TSCRPT_TYPE3'
# 	postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
# 	postData['SA_REQUEST_HDR_INSTITUTION'] = academic_option
# 	postData['DERIVED_AA2_TSCRPT_TYPE3'] = type_option
# 	postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
# 	print postData["ICStateNum"]
# 	response = questSession.session.post(myAcademicsGraduateUnofficialTranscriptURL_HRMS, data = postData, allow_redirects = False)
# 	questSession.currentResponse = response
# 	if response.status_code == requests.codes.ok:
# 		questSession.currentStateNum += 1
# 		print "POST Unofficial with option: (%s, %s) send OK" % (academic_option, type_option)
# 		postData = questSession.getBasicParameters()
# 		postData["ICAction"] = "GO"
# 		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
# 		postData['SA_REQUEST_HDR_INSTITUTION'] = academic_option
# 		postData['DERIVED_AA2_TSCRPT_TYPE3'] = type_option
# 		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
# 		print postData["ICStateNum"]
# 		response = questSession.session.post(myAcademicsGraduateUnofficialTranscriptURL_HRMS, data = postData, allow_redirects = False)
# 		questSession.currentResponse = response
# 		if response.status_code == requests.codes.ok:
# 			questSession.currentStateNum += 1
# 			print "POST Unofficial with option: (%s, %s) GO OK" % (academic_option, type_option)
			
# 			for i in xrange(0, 15):
# 				postData = questSession.getBasicParameters()
# 				postData["ICAction"] = "UW_DERIVED_SR_REFRESH_BTN"
# 				postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
# 				postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
# 				print postData["ICStateNum"]
# 				response = questSession.session.post(myAcademicsGraduateUnofficialTranscriptURL_HRMS, data = postData, allow_redirects = False)
# 				questSession.currentResponse = response
# 				if response.status_code == requests.codes.ok:
# 					questSession.currentStateNum += 1
# 					if checkTranscriptIsDownloaded(questSession, response):
# 						print "Unofficial Transcript GET!"
# 						questSession.currentPOSTpage = "MY_ACADEMICS_UNOFFICIAL_OPTION"
# 						return True
# 					print "POST Unofficial with option: (%s, %s) REFRESH OK" % (academic_option, type_option)
# 					time.sleep(1)
# 				else :
# 					print "POST Unofficial with option: (%s, %s) Failed" % (academic_option, type_option)
# 					return False
# 			# Time out, return false
# 			questSession.currentPOSTpage = "MY_ACADEMICS_UNOFFICIAL_OPTION"
# 			# questSession.gotoMyAcademics_myProgram()
# 			return False
# 		return False
# 	else:
# 		print "POST Unofficial with option: (%s, %s) Failed" % (academic_option, type_option)
# 		return False

# # def postMyAcademics_unofficialTranscript_optionLink(questSession):
# # 	if questSession.currentPOSTpage is "MY_ACADEMICS_UNOFFICIAL_OPTION_LINK":
# # 		print "POST Unofficial link: Already In"
# # 		return True
# # 	else :
# # 		postData = questSession.getBasicParameters()
# # 		postData['ICAction'] = 'DERIVED_AA2_DERIVED_LINK3'
# # 		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
# # 		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
# # 		response = questSession.session.post(myAcademicsGraduateUnofficialTranscriptURL_HRMS, data = postData, allow_redirects = False)
# # 		questSession.currentResponse = response
# # 		if response.status_code == requests.codes.ok:
# # 			print "POST Unofficial link OK"
# # 			questSession.currentStateNum += 1
# # 			questSession.currentPOSTpage = "MY_ACADEMICS_UNOFFICIAL_OPTION_LINK"
# # 			return True
# # 		else:
# # 			print "POST Unofficial link Failed"
# # 			return False

# def checkTranscriptIsDownloaded(questSession, response):
# 	prettifiedContent = response.content.replace("<![CDATA[", "<").replace("]]>", ">")
# 	soup = BeautifulSoup(prettifiedContent)
# 	# print soup.prettify()
# 	transcript = soup.find(id="PrintTranscript")
# 	if not transcript is None:
# 		questSession.currentResult = prettifiedContent
# 		return True
# 	else:
# 		return False


# def gotoMyAcademics_advisors(questSession):
# 	''' Go to my My Advisors
# 		@Param
# 		@Return True/False
# 	'''
# 	getAdvisorsData = {
# 		'Page': 'SSR_SSADVR',
# 		'Action': 'U'
# 	}
# 	response = questSession.session.get(myAcademicsGraduateAdvisorsURL, data = getAdvisorsData, allow_redirects = False)
# 	questSession.currentResponse = response
# 	if response.status_code == requests.codes.ok:
# 		if (questSession.updateStateNum(response)):
# 			print "GET My Advisors Page OK"
# 			# print response.content
# 			return True
# 	print "GET My Advisors Page Failed"
# 	return False

# def gotoMyAcademics_graduateOfferLetters(questSession):
# 	''' Go to my Graduate Offer Letters
# 		@Param
# 		@Return True/False
# 	'''
# 	getGraduateOfferData = {
# 		'Page': 'UW_SS_GRD_OFFR_CTR',
# 		'Action': 'U'
# 	}
# 	response = questSession.session.get(myAcademicsGraduateGradOfferURL, data = getGraduateOfferData, allow_redirects = False)
# 	questSession.currentResponse = response
# 	if response.status_code == requests.codes.ok:
# 		if (questSession.updateStateNum(response)):
# 			print "GET Graduate Offer Letters Page OK"
# 			# print response.content
# 			return True
# 	print "GET Graduate Offer Letters Page Failed"
# 	return False

def main():
	myQuest = QuestClass.QuestSession("", "") # "userid", "password"
	myQuest.login()

	myQuest.postEnroll()

	myQuest.gotoEnroll_myClassSchedule()
	print QuestParser.API_enroll_myClassScheduleResponse(myQuest)

if __name__ == '__main__':
    main()