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

from UWQuestAPI import QuestClass
from UWQuestAPI.QuestClass import QuestSession

from UWQuestAPI.PersonalInformation import postPersonalInformation
from UWQuestAPI import QuestParser
from UWQuestAPI.QuestParser import getFullResponseDictionary, getEmptyMetaDict

# Global variables for jinja environment
template_dir = os.path.join(os.path.dirname(__file__), 'html_template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

# Error code constants
kErrorInvalidKey = 1 # yes
kErrorInvalidSID = 2 # yes
kErrorInvalidSession = 3 # timeout or not logged in, yes
kErrorInvalidUserPassword = 4 
kErrorParseContent = 5
kErrorOther = 6

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
            logging.error("Wrong key type")
            # self.write("Wrong key type")
        if key == 77881122:
            return True
        return False
    def responseInvalidKey(self):
        meta = getEmptyMetaDict()
        data = {}
        meta["status"] = "failure"
        meta["message"] = "Invalid key"
        meta["error_code"] = kErrorInvalidKey
        self.dumpJSON(getFullResponseDictionary(meta, data))

    def dumpJSON(self, dict):
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(dict))

    def responseInvalidSid(self):
        meta = getEmptyMetaDict()
        data = {}
        meta["status"] = "failure"
        meta["message"] = "Invalid sid"
        meta["error_code"] = kErrorInvalidSID
        self.dumpJSON(getFullResponseDictionary(meta, data))

    def responseInvalidSession(self):
        meta = getEmptyMetaDict()
        data = {}
        meta["status"] = "failure"
        meta["message"] = "Session is timeout"
        meta["error_code"] = kErrorInvalidSession
        self.dumpJSON(getFullResponseDictionary(meta, data))

    def responseInvalidPassword(self):
        meta = getEmptyMetaDict()
        data = {}
        meta["status"] = "failure"
        meta["message"] = "Invalid Userid/Password"
        meta["error_code"] = kErrorInvalidUserPassword
        self.dumpJSON(getFullResponseDictionary(meta, data))

    # Add error code for parsed result from UWQuestAPI library
    def responseParseResult(self, parseResult, error_code):
        metaDict = parseResult["meta"]
        if metaDict["status"] == "failure":
            metaDict["error_code"] = error_code
        self.dumpJSON(parseResult)

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


class ActivateHandler(BasicHandler):
    def post(self):
        self.activateOperation()

    def get(self):
        self.activateOperation()

    def activateOperation(self):
        meta = getEmptyMetaDict()
        if self.checkKey():
            meta["status"] = "success"
        else:
            meta["status"] = "failure"
        self.dumpJSON(getFullResponseDictionary(meta, {}))

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
            logging.info(userid + " " + password)
            global sessionStore

            # Init session store for the first time
            if not sessionStore:
                sessionStore = SessionStore()

            if sessionStore.find(userid):
                # Found existing userid
                logging.info("Found existing session")
                foundSession = sessionStore.getSession(userid)
                if (not foundSession.checkIsExpired()) and (foundSession.isLogin):
                    # Not expired and isLogin
                    self.responseParseResult(QuestParser.API_account_loginResponse(foundSession, sessionStore.getSID(userid)), kErrorInvalidSession)
                    # self.dumpJSON(QuestParser.API_account_loginResponse(foundSession, sessionStore.getSID(userid)))
                    sessionStore.printOut()
                    return

            logging.info("Start a new session")
            newQuestSession = QuestSession(userid, password)
            newQuestSession.login()
            sid = ""
            if newQuestSession.isLogin:
                sessionStore.add(userid, password, newQuestSession)
                sid = sessionStore.getSID(userid)
                self.responseParseResult(QuestParser.API_account_loginResponse(newQuestSession, sid), 0) # Must be success
                sessionStore.printOut()
            else:
                # Login failed
                errorCodeFromLib = newQuestSession.currentErrorCode
                errorCodeAPI = 0
                if errorCodeFromLib == QuestClass.kErrorInvalidUserPassword:
                    errorCodeAPI = kErrorInvalidUserPassword
                else:
                    errorCodeAPI = kErrorOther
                self.responseParseResult(QuestParser.API_account_loginResponse(newQuestSession, sid), errorCodeAPI)
        else:
            self.responseInvalidKey()
        
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
                session = sessionStore.getSession(sid)
                session.logout()
                if sessionStore.removeWithSID(sid):
                    sessionStore.printOut()
                    meta["status"] = "success"
                    meta["message"] = "%s has logged out" % userid
                    data["sid"] = sid
                else:
                    meta["status"] = "failure"
                    meta["message"] = "logout %s sid failed" % userid
                    data["sid"] = sid
                self.dumpJSON(getFullResponseDictionary(meta, data))
            else:
                self.responseInvalidSid()
        else:
            self.responseInvalidKey()

class personalinformationHandler(BasicHandler):
    retryTime = 2
    def restoreRetryTime(self):
        self.retryTime = 2

    def shouldRetry(self):
        self.retryTime -= 1
        return (not self.retryTime == 0)

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
                    self.responseInvalidSession()
            else:
                # Not found sid, invalid sid
                self.responseInvalidSid()
        else:
            # Invalid key
            self.responseInvalidKey()

    # PRO: personalInfoQuestSesson must be valid
    def processPersonalInfoReuqest(self, personalInfoQuestSesson, category):
        if category == "addresses":
            if personalInfoQuestSesson.gotoPersonalInformation_address():
                response = QuestParser.API_personalInfo_addressResponse(personalInfoQuestSesson)
            else:
                # Retry
                if self.shouldRetry():
                    return self.processPersonalInfoReuqest(personalInfoQuestSesson, category)
                else:
                    return self.responseInvalidSession()

        elif category == "names":
            if personalInfoQuestSesson.gotoPersonalInformation_name():
                response = QuestParser.API_personalInfo_nameResponse(personalInfoQuestSesson)
            else:
                # Retry
                if self.shouldRetry():
                    return self.processPersonalInfoReuqest(personalInfoQuestSesson, category)
                else:
                    return self.responseInvalidSession()
        elif category == "phone_numbers":
            if personalInfoQuestSesson.gotoPersonalInformation_phoneNumbers():
                response = QuestParser.API_personalInfo_phoneResponse(personalInfoQuestSesson)
            else:
                # Retry
                if self.shouldRetry():
                    return self.processPersonalInfoReuqest(personalInfoQuestSesson, category)
                else:
                    return self.responseInvalidSession()
        elif category == "email_addresses":
            if personalInfoQuestSesson.gotoPersonalInformation_email():
                response = QuestParser.API_personalInfo_emailResponse(personalInfoQuestSesson)
            else:
                # Retry
                if self.shouldRetry():
                    return self.processPersonalInfoReuqest(personalInfoQuestSesson, category)
                else:
                    return self.responseInvalidSession()
        elif category == "emergency_contacts":
            if personalInfoQuestSesson.gotoPersonalInformation_emgencyContacts():
                response = QuestParser.API_personalInfo_emergencyContactResponse(personalInfoQuestSesson)
            else:
                # Retry
                if self.shouldRetry():
                    return self.processPersonalInfoReuqest(personalInfoQuestSesson, category)
                else:
                    return self.responseInvalidSession()
        elif category == "demographic_information":
            if personalInfoQuestSesson.gotoPersonalInformation_demographicInfo():
                response = QuestParser.API_personalInfo_demographicInfoResponse(personalInfoQuestSesson)
            else:
                # Retry
                if self.shouldRetry():
                    return self.processPersonalInfoReuqest(personalInfoQuestSesson, category)
                else:
                    return self.responseInvalidSession()
        elif category == "citizenship_immigration_documents":
            if personalInfoQuestSesson.gotoPersonalInformation_citizenship():
                response = QuestParser.API_personalInfo_citizenshipResponse(personalInfoQuestSesson)
            else:
                # Retry
                if self.shouldRetry():
                    return self.processPersonalInfoReuqest(personalInfoQuestSesson, category)
                else:
                    return self.responseInvalidSession()
        else:
            response = {"meta": {"status": "failure", "message": "Invalid endpoint"}, "data": []}                    
        self.responseParseResult(response, kErrorParseContent)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/activate', ActivateHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/personalinformation/%s' % r'([a-z\_]+)', personalinformationHandler)
], debug=True)
