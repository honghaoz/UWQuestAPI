from requests import Request, Session
#from bs4 import BeautifulSoup
import re

courseName = "CS"
courseNumber = "350"
termCode = "1145"
studentID = ""
userID = ""
password = ""
#usage

##################################implementation#################################################
icsid = ""
currentStateNum = ""
def getICSID(html):
	s = re.findall("<.*?id=['\"]ICSID['\"].*?>", html)[0]
	s = re.findall("value=['\"].*?['\"]", s)[0]
	s = s.replace("value=","").replace('"',"").replace("'","")
	return s

def getStateNum(html):
	s = re.findall("<.*?id=['\"]ICStateNum['\"].*?>", html)[0]
	s = re.findall("value=['\"].*?['\"]", s)[0]
	s = s.replace("value=","").replace('"',"").replace("'","")
	return int(s)

def escapeChar(s):
	return s.replace("+","%2B").replace(" ","%20").replace("=","%3D").replace("/","%2F")

def insertSession(s):
	return s.replace("ICStateNum=XXX","ICStateNum="+str(currentStateNum)).replace("ICSID=XXX","ICSID="+escapeChar(icsid))

s = Session()

############# Login and set cookies #####################
questLoginURL = 'https://quest.pecs.uwaterloo.ca/psp/SS/?cmd=login&languageCd=ENG'
postLoginData = {
	'userid': userID,
	'pwd': password,
	'timezoneOffset': '240',
	'httpPort': ''
}
mainPageResponse = s.post(questLoginURL, data = postLoginData)
#print mainPageResponse.content

############# Jump to real URL #####################
jumpURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?PORTALPARAM_PTCNAV=HC_SSS_STUDENT_CENTER&EOPP.SCNode=SA&EOPP.SCPortal=ACADEMIC&EOPP.SCName=CO_EMPLOYEE_SELF_SERVICE&EOPP.SCLabel=Self%20Service&EOPP.SCPTfname=CO_EMPLOYEE_SELF_SERVICE&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_SSS_STUDENT_CENTER&IsFolder=false&PortalActualURL=https%3a%2f%2fquest.pecs.uwaterloo.ca%2fpsc%2fSS%2fACADEMIC%2fSA%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalRegistryName=ACADEMIC&PortalServletURI=https%3a%2f%2fquest.pecs.uwaterloo.ca%2fpsp%2fSS%2f&PortalURI=https%3a%2f%2fquest.pecs.uwaterloo.ca%2fpsc%2fSS%2f&PortalHostNode=SA&NoCrumbs=yes&PortalKeyStruct=yes"

jumpResponse = s.get(jumpURL)
#print jumpResponse.content

############# enroll #####################
enrollURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL?Page=SSR_SSENRL_LIST&Action=A&ExactKeys=Y&TargetFrameName=None"
enrollResponse = s.get(enrollURL)
#print enrollResponse.content

############# search #####################
searchTabURL ="https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.UW_SSR_CLASS_SRCH.GBL?Page=UW_SSR_CLSRCH_ENTR&Action=U&ACAD_CAREER=CAR&EMPLID="+studentID+"&ENRL_REQUEST_ID=&INSTITUTION=INST&STRM=TERM"
response = s.get(searchTabURL)
#print response.content

classSearchURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.UW_SSR_CLASS_SRCH.GBL"
icsid = getICSID(response.content)
currentStateNum = getStateNum(response.content)

classSearchData = {
	'ICAJAX': '1',
	'ICNAVTYPEDROPDOWN': '0',
	'ICType': 'Panel',
	'ICElementNum': '0',
	'ICStateNum': currentStateNum,
	'ICAction': 'UW_DERIVED_SR_SSR_PB_CLASS_SRCH',
	'ICXPos': '0',
	'ICYPos': '0',
	'ResponsetoDiffFrame': '-1',
	'TargetFrameName': 'None',
	'FacetPath': 'None',
	'ICFocus': '',
	'ICSaveWarningFilter': '0',
	'ICChanged': '-1',
	'ICResubmit': '0',
	'ICSID': icsid,
	'ICActionPrompt': 'false',
	'ICFind': '',
	'ICAddCount': '',
	'ICAPPCLSDATA': '',
	'DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$': '9999',
	'CLASS_SRCH_WRK2_INSTITUTION$31$': 'UWATR',
	'CLASS_SRCH_WRK2_STRM$35$': termCode,
	'CLASS_SRCH_WRK2_SUBJECT$7$': courseName,
	'CLASS_SRCH_WRK2_CATALOG_NBR$8$': courseNumber,
	'CLASS_SRCH_WRK2_SSR_EXACT_MATCH1': 'E',
	'CLASS_SRCH_WRK2_ACAD_CAREER': 'UG',
	'CLASS_SRCH_WRK2_SSR_OPEN_ONLY$chk': 'N',
	'DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$': '9999',
}

response = s.post(classSearchURL, data = classSearchData)
print response.content
