from requests import Request, Session
from bs4 import BeautifulSoup
import re

################ Helper Functions ################

# Get ICSID from html code, ICSID is used for POST method
# <input type='hidden' name='ICSID' id='ICSID' value='mioRfZRLx/IJL+P2KY8kGL/aj+qAtaHCd1KjrNRrTh8=' />
def getICSID(html):
	return re.findall("<input type='hidden' name='ICSID' id='ICSID' value='(.*)'", html)[0]

# Get StateNum from html code, StateNum is used for POST method
# <input type='hidden' name='ICStateNum' id='ICStateNum' value='1' />
def getStateNum(html):
	return int(re.findall("<input type='hidden' name='ICStateNum' id='ICStateNum' value='(\d+)'", html)[0])

def getAddress(html):
	soup = BeautifulSoup(html)

	addressTRs = soup.find(id="SCC_ADDR_H$scroll$0")

	tableString = str(addressTRs)
	x = re.sub("\<.*?\>", "", tableString);
	resultList = filter(lambda x: len(x) > 0, x.replace(" \r", ", ").split("\n"))
	del(resultList[2])
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

################ Login and set cookies ################
# Start a session to manage cookies
s = Session()

questLoginURL = 'https://quest.pecs.uwaterloo.ca/psp/SS/?cmd=login&languageCd=ENG'
postLoginData = {
	'userid': 'h344zhan',
	'pwd': 'Zhh358279765099',
	'timezoneOffset': '240',
	'httpPort': ''
}

s.post(questLoginURL, data = postLoginData)

################ Operations ################

# Get main page
studentCenterURL = 'https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL'
getMainPageData = {
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

mainPageResponse = s.get(studentCenterURL, data = getMainPageData)

icsid = getICSID(mainPageResponse.content)
currentStateNum = getStateNum(mainPageResponse.content)

# Print ICSID
print "ICSID: " + icsid
# Print current state num
print "currentStateNum: " + str(currentStateNum) + '\n'

# headers={
# 	'Accept':'*/*',
# 	'Accept-Encoding':'gzip,deflate,sdch',
# 	'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6',
# 	'Connection': 'keep-alive',
# 	'Content-Length': '356',
# 	'Origin': 'https://quest.pecs.uwaterloo.ca',
# 	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
# 	'Content-Type': 'application/x-www-form-urlencoded',
# }

postPersonalInfoData = {
	'ICAJAX': '1',
	'ICNAVTYPEDROPDOWN': '0',
	'ICType': 'Panel',
	'ICElementNum': '0',
	'ICStateNum': str(currentStateNum),
	'ICAction': 'DERIVED_SSS_SCL_SSS_PERSONAL_INFO',
	'ICXPos': '0',
	'ICYPos': '87',
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
	'ICAPPCLSDATA': ''
}

personalInfoResponse = s.post(studentCenterURL, data = postPersonalInfoData)

print personalInfoResponse.content

# personalInfoAddressGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_ADDRESSES.GBL"
# getAddressData = {
# 	'Page': 'SS_ADDRESSES',
# 	'Action': 'C'
# }

# addressResponse = s.get(personalInfoAddressGetURL, data = getAddressData)

# # print addressResponse.content
# getAddress(addressResponse.content)

# currentStateNum = getStateNum(addressResponse.content)
# # Print current state num
# print "currentStateNum: " + str(currentStateNum) + '\n'

# personalInfoNameGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_NAMES.GBL?"
# getNameData = {
# 	'Page': 'SS_CC_NAME',
# 	'Action': 'C'
# }

# nameResponse = s.get(personalInfoNameGetURL, data = getNameData)

# # print nameResponse.content

# currentStateNum = getStateNum(nameResponse.content)
# # Print current state num
# print "currentStateNum: " + str(currentStateNum) + '\n'


# personalInfoPhoneGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_PERS_PHONE.GBL"
# getPhoneData = {
# 	'Page': 'SS_CC_PERS_PHONE',
# 	'Action': 'U'
# }

# phoneResponse = s.get(personalInfoPhoneGetURL, data = getPhoneData)

# # print phoneResponse.content

# currentStateNum = getStateNum(phoneResponse.content)
# # Print current state num
# print "currentStateNum: " + str(currentStateNum) + '\n'



# personalInfoEmailGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_EMAIL_ADDR.GBL"
# getEmailData = {
# 	'Page': 'SS_CC_EMAIL_ADDR',
# 	'Action': 'U'
# }

# emailResponse = s.get(personalInfoEmailGetURL, data = getEmailData)

# # print emailResponse.content

# currentStateNum = getStateNum(emailResponse.content)
# # Print current state num
# print "currentStateNum: " + str(currentStateNum) + '\n'



# personalInfoDemographicInfoGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/CC_PORTFOLIO.SS_CC_DEMOG_DATA.GBL"
# getDemographicInfoData = {
# 	'Page': 'SS_CC_DEMOG_DATA',
# 	'Action': 'U'
# }

# demographicInfoResponse = s.get(personalInfoDemographicInfoGetURL, data = getDemographicInfoData)

# # print demographicInfoResponse.content

# currentStateNum = getStateNum(demographicInfoResponse.content)
# # Print current state num
# print "currentStateNum: " + str(currentStateNum) + '\n'




# personalInfoCitizenshipGetURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/UW_SS_MENU.UW_SS_CC_VISA_DOC.GBL"
# getCitizenshipData = {
# 	'Page': 'UW_SS_CC_VISA_DOC',
# 	'Action': 'U'
# }

# citizenshipResponse = s.get(personalInfoCitizenshipGetURL, data = getCitizenshipData)

# # print citizenshipResponse.content

# currentStateNum = getStateNum(citizenshipResponse.content)
# # Print current state num
# print "currentStateNum: " + str(currentStateNum) + '\n'

# classSearchURL = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.UW_SSR_CLASS_SRCH.GBL"
# postClassSearch = {
# 	'ICAJAX': '1',
# 	'ICNAVTYPEDROPDOWN': '0',
# 	'ICType': 'Panel',
# 	'ICElementNum': '0',
# 	'ICStateNum': str(currentStateNum),
# 	'ICAction': 'UW_DERIVED_SR_SSR_PB_CLASS_SRCH',
# 	'ICXPos': '0',
# 	'ICYPos': '0',
# 	'ResponsetoDiffFrame': '-1',
# 	'TargetFrameName': 'None',
# 	'FacetPath': 'None',
# 	'ICFocus': '',
# 	'ICSaveWarningFilter': '0',
# 	'ICChanged': '-1',
# 	'ICResubmit': '0',
# 	'ICSID': icsid,
# 	'ICActionPrompt': 'false',
# 	'ICFind': '',
# 	'ICAddCount': '',
# 	'ICAPPCLSDATA': '',
# 	'DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$': '9999',
# 	'CLASS_SRCH_WRK2_INSTITUTION$31$': 'UWATR',
# 	'CLASS_SRCH_WRK2_STRM$35$': '1145',
# 	'CLASS_SRCH_WRK2_SUBJECT$7$': 'CS',
# 	'CLASS_SRCH_WRK2_CATALOG_NBR$8$': '350',
# 	'CLASS_SRCH_WRK2_SSR_EXACT_MATCH1': 'E',
# 	'CLASS_SRCH_WRK2_ACAD_CAREER': 'UG',
# 	'CLASS_SRCH_WRK2_SSR_OPEN_ONLY$chk': 'Y',
# 	'CLASS_SRCH_WRK2_SSR_OPEN_ONLY': 'Y',
# 	'DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$': '9999',
# }

# classSearchResponse = s.post(classSearchURL, data = postClassSearch)

# print classSearchResponse.content

