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
from handlers.main_handler import * 
from handlers.login_handler import *
from handlers.signup_handler import *
from handlers.welcome_handler import *
from handlers.logout_handler import *
from handlers.newpost_handler import *
from handlers.permalink_handler import *

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login/?', LoginHandler),
    ('/signup/?', SignupHandler),
    ('/welcome/?', WelcomeHandler),
    ('/logout/?', LogoutHandler),
    ('/newpost/?', NewpostHandler),
    ('/([0-9]+)/?', PermalinkHandler)
], debug=True)
