import requests
from requests import Request, Session
from bs4 import BeautifulSoup
import re
import copy

################ Helper Functions ################

# Get ICSID from html code, ICSID is used for POST method
def getICSID(html):
	return re.findall("<input type='hidden' name='ICSID' id='ICSID' value='(.*)'", html)[0]

# Get StateNum from html code, StateNum is used for POST method
def getStateNum(html):
	return int(re.findall("<input type='hidden' name='ICStateNum' id='ICStateNum' value='(\d+)'", html)[0])

def getAddress(html):
	soup = BeautifulSoup(html)

	# addressTable contains address information
	addressTable = soup.find(id="SCC_ADDR_H$scroll$0")

	# Clean tags
	tableString = str(addressTable)
	x = re.sub("\<.*?\>", "", tableString);
	# clean result list
	resultList = filter(lambda x: len(x) > 0, x.replace(" \r", ", ").split("\n"))
	del(resultList[2])
	# resultList contains
	print resultList

	# Three <tr> tags contain one head and two(maybe more?) rows
	# addressTRs = soup.body.form.find(id="win0divPAGECONTAINER").table.tr.td.find(id="win0divPSPAGECONTAINER").table.find_all(id="win0divSCC_ADDR_H$0")[0].table.tr.td.table.find_all('tr')
	# # Table head
	# addressHeads = addressTRs[0].find_all('th')
	# print addressHeads[0].a.string + "\t" + addressHeads[1].a.string

	# # Addresses
	# numberOfAddresses = len(addressTRs)
	# for i in range(1, numberOfAddresses):
	# 	eachAddr = addressTRs[i]
	# 	print eachAddr.td.div.span.string + "\t" + eachAddr.td.next_sibling.next_sibling.div.span.get_text().replace(" \r", ", ")

# TODO: timeout handling, network error handling
class BasicQuestSession:
	session = Session()
	isLogin = False
	userid = ""
	password = ""
	icsid = ""
	currentStateNum = 0
	isUndergraduate = True
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
	studentCenterURL = 'https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL'
	

	# Initialization
	def __init__(self, userid, password):
	    """ Initialization """
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
			'timezoneOffset': '240', # Fix Me
			'httpPort': ''
		}
		response = self.session.post(self.questLoginURL, data = postLoginData)
		if response.status_code == requests.codes.ok:
			print "Login Successfully!"
			self.isLoginisLogin = True
			return True
		else:
			print "Login Failed!"
			self.isLoginisLogin = False
			return False

	def checkIsExpiration(self):
		''' Check whether login is expired, return True if expired
			@Param 
			@Return True if expired
		'''
		return False
	# TODO
	def checkIsUndergraduate(self, response):
		''' Check whether logined account is undergraduate
			@Param requests response
			@Return 
		'''
		pass
	def updateICSID(self, response):
		''' Update ICSID and StateNum
			@Param requests response
			@Return 
		'''
		self.icsid = getICSID(response.content)
		# Print ICSID
		print "ICSID: " + self.icsid
		self.updateStateNum(response)

	def updateStateNum(self, response):
		''' Update StateNum
			@Param requests response
			@Return 
		'''
		self.currentStateNum = getStateNum(response.content)
		# Print current state num
		print "Current StateNum: " + str(self.currentStateNum)

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

		response = self.session.get(self.studentCenterURL, data = getStudentCenterData)
		if response.status_code == requests.codes.ok:
			print "GET Student Center OK"
			self.updateICSID(response)
			# self.updateStateNum(response)
			return True
		else:
			print "GET Student Center Failed"
			return False

def main():
	myQuest = BasicQuestSession("", "")# "userid", "password"
	myQuest.login()
	myQuest.gotoStudentCenter()

if __name__ == '__main__':
    main()
