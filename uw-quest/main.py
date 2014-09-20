#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import sys
import os
import jinja2
import json
import hashlib
import copy

import logging
from google.appengine.ext import ndb
from google.appengine.api import memcache

sys.path.insert(0, 'libs')
import requests

from UWQuestAPI.QuestClass import QuestSession

from UWQuestAPI.PersonalInformation import postPersonalInformation
from UWQuestAPI import QuestParser
from UWQuestAPI.QuestParser import getFullResponseDictionary, getEmptyMetaDict

# Global variables for jinja environment
template_dir = os.path.join(os.path.dirname(__file__), 'html_template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

# Basic Handler
class BasicHandler(webapp2.RequestHandler):
    # rewrite the write, more neat
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
    # render helper function, use jinja2 to get template
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    # render page using jinja2
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def checkKey(self):
        key = self.request.get("key")
        try:
            key = int(key)
        except Exception, e:
            self.write("Wrong key type")
        if key == 77881122:
            return True
        return False
    def dumpJSON(self, dict):
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(dict))

class MainHandler(BasicHandler):
    """Handle for '/' """
    def get(self):
        self.render('home.html')
        # PersonalInformationQuestClass.main()

def hashSID(userid, password, icsid):
    combinedString = userid + "_"+ password + "_" + icsid
    print combinedString
    sidHash = hashlib.sha1(combinedString).hexdigest()
    print sidHash
    return sidHash

class SessionStore(object):
    """docstring for SessionStore
        SessionStore has a storeDict, this storeDict use userid and sid as key and point to the same [sid, userid, password, icsid]
    """
    storeDict = {}
    def __init__(self):
        logging.info("SessionStore init()")

    def find(self, anyID): # id is userid or sid
        return (anyID in self.storeDict)

    def getUserID(self, sid):
        if self.find(sid):
            return copy.copy(self.storeDict[sid][1])
        else:
            return None

    def getSID(self, userid):
        if self.find(userid):
            return copy.copy(self.storeDict[userid][0])
        else:
            return None

    def getSession(self, anyID):
        if self.find(anyID):
            return self.storeDict[anyID][3]
        else:
            return None

    def add(self, userid, password, questSession):
        # Make sure no duplicate entries
        if self.find(userid):
            logging.info("Remove old")
            self.removeWithUserID(userid)
        newSID = hashSID(userid, password, questSession.icsid)        
        if self.find(newSID):
            self.removeWithSID(newSID)
        else:
            logging.info("Added new")
        value = [newSID, userid, password, questSession]
        self.storeDict[newSID] = value
        self.storeDict[userid] = value
        return True
    
    def removeWithUserID(self, userid):
        try:
            sid = self.getSID(userid)
            # print sid
            self.storeDict.pop(sid)
            self.storeDict.pop(userid)
            logging.info("removed successfully with %s" % userid)
            return True
        except Exception, e:
            logging.error("removed failed with %s, %s" % (userid, e))
            return False

    def removeWithSID(self, sid):
        try:
            userid = self.getUserID(sid)
            self.storeDict.pop(sid)
            self.storeDict.pop(userid)
            logging.info("removed successfully with %s" % sid)
            return True
        except Exception, e:
            logging.error("removed failed with %s, %s" % (sid, e))
            return False

    def clear(self):
        return self.storeDict.clear()

    def printOut(self):
        print self.storeDict
        # for key, value in self.storeDict:
            # print key + "\t: " + value
        # print json.dumps(self.storeDict, indent=4, sort_keys=True)
        
sessionStore = SessionStore()

class LoginHandler(BasicHandler):
    def post(self):
        self.loginOperation()

    def get(self):
        self.loginOperation()
        
    def loginOperation(self):
        meta = getEmptyMetaDict()
        data = {}
        if self.checkKey():
            userid = self.request.get("userid")
            password = self.request.get("password")
            global sessionStore
            # Init for the first time
            if not sessionStore:
                sessionStore = SessionStore()

            if sessionStore.find(userid):
                # Found existing userid
                foundSession = sessionStore.getSession(userid)
                if (not foundSession.checkIsExpired()) and (foundSession.isLogin):
                    # Not expired and isLogin
                    self.dumpJSON(QuestParser.API_account_loginResponse(foundSession, sessionStore.getSID(userid)))
                    sessionStore.printOut()
                    return

            newQuestSession = QuestSession(userid, password)
            newQuestSession.login()
            sid = ""
            if newQuestSession.isLogin:
                sessionStore.add(userid, password, newQuestSession)
                sid = sessionStore.getSID(userid)
            self.dumpJSON(QuestParser.API_account_loginResponse(newQuestSession, sid))
            sessionStore.printOut()
        else:
            meta["status"] = "failure"
            meta["message"] = "Invalid key"
            self.dumpJSON(getFullResponseDictionary(meta, data))
        
class LogoutHandler(BasicHandler):
    def post(self):
        self.logoutOperation()

    def get(self):
        self.logoutOperation()
        
    def logoutOperation(self):
        meta = getEmptyMetaDict()
        data = {}
        if self.checkKey():
            sid = self.request.get("sid")
            global sessionStore
            if sessionStore.find(sid):
                userid = sessionStore.getUserID(sid)
                if sessionStore.removeWithSID(sid):
                    sessionStore.printOut()
                    meta["status"] = "success"
                    meta["message"] = "%s has logged out" % userid
                    data["sid"] = sid
                else:
                    meta["status"] = "failure"
                    meta["message"] = "logout %s sid failed" % userid
                    data["sid"] = sid
            else:
                meta["status"] = "failure"
                meta["message"] = "sid not Found"
            self.dumpJSON(getFullResponseDictionary(meta, data))
        else:
            meta["status"] = "failure"
            meta["message"] = "Invalid key"
            self.dumpJSON(getFullResponseDictionary(meta, data))

class personalinformationHandler(BasicHandler):
    def post(self, category):
        self.personalinformationOperation(category)

    def get(self, category):
        self.personalinformationOperation(category)

    def personalinformationOperation(self, category):
        sid = self.request.get("sid")
        logging.info("category: " + category)
        logging.info("sid: " + sid)
        if self.checkKey():
            global sessionStore
            if sessionStore.find(sid):
                foundSession = sessionStore.getSession(sid)
                if (not foundSession.checkIsExpired()) and (foundSession.isLogin):
                    # Found valid session
                    self.processPersonalInfoReuqest(foundSession, category)
                else:
                    # Found session is invalid, need relogin
                    response = {"meta": {"status": "failure", "message": "Session is timeout"}, "data": []}
                    self.dumpJSON(response)
            else:
                # Not found sid, invalid sid
                response = {"meta": {"status": "failure", "message": "Invalid sid"}, "data": []}
                self.dumpJSON(response)
        else:
            # Invalid key
            meta["status"] = "failure"
            meta["message"] = "Invalid key"
            self.dumpJSON(getFullResponseDictionary(meta, data))

    # PRO: personalInfoQuestSesson must be valid
    def processPersonalInfoReuqest(self, personalInfoQuestSesson, category):
        if category == "addresses":
            personalInfoQuestSesson.gotoPersonalInformation_address()
            response = QuestParser.API_personalInfo_addressResponse(personalInfoQuestSesson)
        elif category == "names":
            personalInfoQuestSesson.gotoPersonalInformation_name()
            response = QuestParser.API_personalInfo_nameResponse(personalInfoQuestSesson)
        elif category == "phone_numbers":
            personalInfoQuestSesson.gotoPersonalInformation_phoneNumbers()
            response = QuestParser.API_personalInfo_phoneResponse(personalInfoQuestSesson)
        elif category == "email_addresses":
            personalInfoQuestSesson.gotoPersonalInformation_email()
            response = QuestParser.API_personalInfo_emailResponse(personalInfoQuestSesson)
        elif category == "emergency_contacts":
            personalInfoQuestSesson.gotoPersonalInformation_emgencyContacts()
            response = QuestParser.API_personalInfo_emergencyContactResponse(personalInfoQuestSesson)
        elif category == "demographic_information":
            personalInfoQuestSesson.gotoPersonalInformation_demographicInfo()
            response = QuestParser.API_personalInfo_demographicInfoResponse(personalInfoQuestSesson)
        elif category == "citizenship_immigration_documents":
            personalInfoQuestSesson.gotoPersonalInformation_citizenship()
            response = QuestParser.API_personalInfo_citizenshipResponse(personalInfoQuestSesson)
        else:
            response = {"meta": {"status": "failure", "message": "Invalid endpoint"}, "data": []}                    
        self.dumpJSON(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/personalinformation/%s' % r'([a-z\_]+)', personalinformationHandler)
    # ('/personalinformation/names', personalinformation_namesHandler),
    # ('/personalinformation/phone_numbers', personalinformation_phoneNumbersHandler),
    # ('/personalinformation/email_addresses', personalinformation_emailAddressesHandler),
    # ('/personalinformation/emergency_contacts', personalinformation_emergencyContactsHandler),
    # ('/personalinformation/demographic_information', personalinformation_demographicInformationHandler),
    # ('/personalinformation/citizenship_immigration_documents', personalinformation_citizenshipImmigrationDocumentsHandler),
], debug=True)
