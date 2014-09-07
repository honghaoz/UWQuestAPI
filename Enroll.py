import QuestClass
import requests
import QuestParser
from bs4 import BeautifulSoup
import json

enroll_myClassScheduleURL_HRMS = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"
enroll_searchForClassesURL_HRMS = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/HRMS/c/SA_LEARNER_SERVICES.UW_SSR_CLASS_SRCH.GBL"

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
			# print response.content
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
		'Action': 'A'#,
		#'ExactKeys': 'Y',
		#'TargetFrameName': 'None'
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

def postEnroll_myClassSchedule_termIndex(questSession, termIndex):
	''' POST to get schedule for one term
		@Param term index return from gotoEnroll_myClassSchedule
		@Return True/False
	'''
	# If not in the right post postition, change to right post position
	if not (questSession.currentPOSTpage is "ENROLL_HOME"):
		if not gotoEnroll_myClassSchedule(questSession): #questSession.postMyAcademics_grades_termLink():
			print "POST schedule with index: %d Failed" % termIndex
			return False

	# Start to post
	postData = questSession.getBasicParameters()
	postData['ICAction'] = 'DERIVED_SSS_SCT_SSR_PB_GO'
	postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
	postData['SSR_DUMMY_RECV1$sels$0'] = termIndex
	postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
	# print postGradesData["ICStateNum"]

	response = questSession.session.post(enroll_myClassScheduleURL_HRMS, data = postData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		print "POST schedule with index: %d OK" % termIndex
		questSession.currentStateNum += 1
		questSession.currentPOSTpage = "ENROLL_HOME_ONE_TERM"
		# questSession.gotoMyAcademics_myProgram()
		return True
	else:
		print "POST schedule with index: %d Failed" % termIndex
		return False

# def postEnroll_CourseSubject(questSession):
# 	pass

def gotoEnroll_searchForClasses(questSession):
	''' Go to search for classes
		@Param
		@Return True/False
	'''
	getData = {
		'Page': 'UW_SSR_CLSRCH_ENTR',
		'Action': 'U',
	}
	response = questSession.session.get(enroll_searchForClassesURL_HRMS, data = getData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		if (questSession.updateStateNum(response)):
			print "GET search for classes Page OK"
			return True
	print "GET search for classes Page Failed"
	return False

def postEnroll_searchForClasses(questSession, institution, term, course_subject, course_number, course_number_relation, course_career, open_only):
	postData = questSession.getBasicParameters()
	postData["ICAction"] = "UW_DERIVED_SR_SSR_PB_CLASS_SRCH"
	postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
	postData['CLASS_SRCH_WRK2_INSTITUTION$31$'] = institution
	postData["CLASS_SRCH_WRK2_STRM$35$"] = term
	postData["CLASS_SRCH_WRK2_SUBJECT$7$"] = course_subject
	postData["CLASS_SRCH_WRK2_CATALOG_NBR$8$"] = course_number
	postData["CLASS_SRCH_WRK2_SSR_EXACT_MATCH1"] = course_number_relation
	postData["CLASS_SRCH_WRK2_ACAD_CAREER"] = course_career
	postData["CLASS_SRCH_WRK2_SSR_OPEN_ONLY$chk"] = open_only
	postData["CLASS_SRCH_WRK2_SSR_OPEN_ONLY"] = open_only
	postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'

	response = questSession.session.post(enroll_searchForClassesURL_HRMS, data = postData, allow_redirects = False)
	questSession.currentResponse = response
	if response.status_code == requests.codes.ok:
		questSession.currentStateNum += 1
		questSession.currentPOSTpage = "ENROLL_SEARCH_FOR_CLASSES_RESULT"
		print "POST search for classes OK"
		print "institution: %s" % institution
		print "term: %s" % term
		print "course_subject: %s" % course_subject
		print "course_number: %s" % course_number
		print "course_number_relation: %s" % course_number_relation
		print "course_career: %s" % course_career
		print "open_only: %s" % open_only
		if askForContinue(response.content):
			print "Need to Continue"
			postData = questSession.getBasicParameters()
			postData["ICAction"] = "#ICSave"
			response = questSession.session.post(enroll_searchForClassesURL_HRMS, data = postData, allow_redirects = False)
			questSession.currentResponse = response
			if response.status_code == requests.codes.ok:
				questSession.currentStateNum += 1
				questSession.currentPOSTpage = "ENROLL_SEARCH_FOR_CLASSES_RESULT"
				# print response.content
				return True
		return True
	else:
		print "POST search for classes failed"
		return False

def askForContinue(html):
	soup = BeautifulSoup(html.replace("<![CDATA[", "<").replace("]]>", ">"))
	# print soup.prettify()
	isAsking = soup.find(id="win0divDERIVED_SSE_DSP_SSR_MSG_TEXT")
	if isAsking:
		return True
	else:
		return False

def postEnroll_searchForClassesDetailInfo(questSession, action):
	if questSession.currentPOSTpage is "ENROLL_SEARCH_FOR_CLASSES_DETAIL":
		if postEnroll_goBackToSearchResult(questSession):
			return postEnroll_searchForClassesDetailInfo(questSession, action)
		else:
			return False
	elif questSession.currentPOSTpage is "ENROLL_SEARCH_FOR_CLASSES_RESULT":
		postData = questSession.getBasicParameters()
		postData["ICAction"] = action
		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'

		response = questSession.session.post(enroll_searchForClassesURL_HRMS, data = postData, allow_redirects = False)
		questSession.currentResponse = response
		if response.status_code == requests.codes.ok:
			questSession.currentStateNum += 1
			questSession.currentPOSTpage = "ENROLL_SEARCH_FOR_CLASSES_DETAIL"
			print "POST class detail %s OK" % action
			# print response.content
			return True
		else:
			print "POST class detail %s failed" % action
			return False
	else:
		print "POST class detail failed: wrong post status"
		return False

def postEnroll_goBackToSearchResult(questSession):
	if not questSession.currentPOSTpage is "ENROLL_SEARCH_FOR_CLASSES_DETAIL":
		print "POST go back to search result table failed: wrong current post page"
		return False
	else:
		postData = questSession.getBasicParameters()
		postData["ICAction"] = "UW_DERIVED_SR_SSR_PB_BACK"
		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
		postData['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
		response = questSession.session.post(enroll_searchForClassesURL_HRMS, data = postData, allow_redirects = False)
		questSession.currentResponse = response
		if response.status_code == requests.codes.ok:
			questSession.currentStateNum += 1
			questSession.currentPOSTpage = "ENROLL_SEARCH_FOR_CLASSES_RESULT"
			print "POST go back to search result table success"
			return True
		else:
			return Fals

def main():
	myQuest = QuestClass.QuestSession("", "") # "userid", "password"
	myQuest.login()

	myQuest.postEnroll()

	# myQuest.gotoEnroll_myClassSchedule()
	# print QuestParser.API_enroll_myClassScheduleResponse(myQuest)

	# myQuest.postEnroll_myClassSchedule_termIndex(0)
	# print QuestParser.API_enroll_myClassScheduleTermResponse(myQuest)

	myQuest.gotoEnroll_searchForClasses()
	# print QuestParser.API_enroll_searchForClassesResponse(myQuest)
	print json.dumps(QuestParser.API_enroll_searchForClassesResponse(myQuest), indent=4, sort_keys=True)

	myQuest.postEnroll_searchForClasses(institution = "UWATR", 
										term = "1149", 
										course_subject = "CS", 
										course_number = "656", 
										course_number_relation = "E", 
										course_career = "GRD", 
										open_only = "Y")

	print json.dumps(QuestParser.API_enroll_searchForClassesResultResponse(myQuest), indent=4, sort_keys=True)

	myQuest.postEnroll_searchForClassesDetailInfo('UW_DERIVED_SR_SSR_CLASSNAME_LONG$0')
	# myQuest.postEnroll_searchForClassesDetailInfo('UW_DERIVED_SR_SSR_CLASSNAME_LONG$1')

	# print QuestParser.Parse_enroll_searchForClassesClassDetail(myQuest.currentResponse.content)
	print json.dumps(QuestParser.Parse_enroll_searchForClassesClassDetail(myQuest.currentResponse.content), indent=4, sort_keys=True)

if __name__ == '__main__':
    main()