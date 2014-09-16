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
    """docstring for SessionStore"""
    storeDict = {}
    def __init__(self):
        print "SessionStore init()"

    def find(self, sid):
        return (sid in self.storeDict)

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

    def getSession(self, sid):
        if self.find(sid):
            return self.storeDict[sid][3]
        else:
            return None

    def add(self, userid, password, questSession):
        if self.find(userid):
            self.removeWithUserID(userid)

        sidHash = hashSID(userid, password, questSession.icsid)        
        if self.find(sidHash):
            self.removeWithSID(sidHash)
        else:
            print "Added new"
        value = [sidHash, userid, password, questSession]
        self.storeDict[sidHash] = value
        self.storeDict[userid] = value
    
    def removeWithUserID(self, userid):
        try:
            sid = self.getSID(userid)
            # print sid
            self.storeDict.pop(sid)
            self.storeDict.pop(userid)
            print "removed successfully with %s" % userid
        except Exception, e:
            print "removed failed with %s, %s" % (userid, e)

    def removeWithSID(self, sid):
        try:
            userid = self.getUserID(sid)
            self.storeDict.pop(sid)
            self.storeDict.pop(userid)
            print "removed successfully with %s" % sid
        except Exception, e:
            print "removed failed with %s, %s" % (sid, e)

    def clear(self):
        self.storeDict.clear()

    def printOut(self):
        print self.storeDict
        # for key, value in self.storeDict:
            # print key + "\t: " + value
        # print json.dumps(self.storeDict, indent=4, sort_keys=True)
        
        
sessionStore = SessionStore()

basicQuestSession = QuestSession("", "")

class LoginHandler(BasicHandler):
    def post(self):
        self.loginOperation()

    def get(self):
        self.loginOperation()
        
    def loginOperation(self):
        key = self.request.get("key")
        try:
            key = int(key)
        except Exception, e:
            self.write("Wrong key")
        if key == 77881122:
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
                    self.write(json.dumps(QuestParser.API_account_loginResponse(foundSession, sessionStore.getSID(userid))))
                    sessionStore.printOut()
                    return

            newQuestSession = QuestSession(userid, password)
            newQuestSession.login()
            sid = ""
            if newQuestSession.isLogin:
                sessionStore.add(userid, password, newQuestSession)
                sid = sessionStore.getSID(userid)
            self.write(json.dumps(QuestParser.API_account_loginResponse(newQuestSession, sid)))
            sessionStore.printOut()
        else:
            self.write("Invalid key ")
        
class LogoutHandler(BasicHandler):
    def post(self):
        self.logoutOperation()

    def get(self):
        self.logoutOperation()
        
    def logoutOperation(self):
        sid = self.request.get("sid")
        # TODO
        # global basicQuestSession
        # basicQuestSession = BasicQuestSession(userid, password)
        # basicQuestSession.login()
        # self.write(json.dumps(QuestParser.API_account_loginResponse(basicQuestSession)))

class personalinformationHandler(BasicHandler):
    def post(self, category):
        self.personalinformationOperation(category)

    def get(self, category):
        self.personalinformationOperation(category)

    def personalinformationOperation(self, category):
        sid = self.request.get("sid")
        logging.info("category: " + category)
        logging.info("sid: " + sid)
        global basicQuestSession
        if sid == basicQuestSession.icsid:
            personalInfoQuestSesson = PersonalInformationQuestSession("", "", basicQuestSession)
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
            self.write(json.dumps(response))
        else:
            response = {"meta": {"status": "failure", "message": "Invalid sid"}, "data": []}
            self.write(json.dumps(response))

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
