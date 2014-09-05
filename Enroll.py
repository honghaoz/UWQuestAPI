import QuestClass
import requests
import QuestParser
from bs4 import BeautifulSoup

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

def postEnroll_searchForClasses():
	pass

def main():
	myQuest = QuestClass.QuestSession("", "") # "userid", "password"
	myQuest.login()

	myQuest.postEnroll()

	# myQuest.gotoEnroll_myClassSchedule()
	# print QuestParser.API_enroll_myClassScheduleResponse(myQuest)

	# myQuest.postEnroll_myClassSchedule_termIndex(0)
	# print QuestParser.API_enroll_myClassScheduleTermResponse(myQuest)

	myQuest.gotoEnroll_searchForClasses()
	print QuestParser.API_enroll_searchForClassesResponse(myQuest)

if __name__ == '__main__':
    main()