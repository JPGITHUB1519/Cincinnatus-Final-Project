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
from handlers.main_json_handler import *
from handlers.permalink_json_handler import *
from handlers.flushcache_handler import *
from handlers.imgserve_handler import *
from handlers.admin_handler import *
from handlers.enable_disable_handler import *
from handlers.test_handler import *
from handlers.email_signup_handler import *
from handlers.verify_handler import *

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/.json/?', mainJsonHandler),
    ('/login/?', LoginHandler),
    ('/signup/?', SignupHandler),
    ('/welcome/?', WelcomeHandler),
    ('/logout/?', LogoutHandler),
    ('/newpost/?', NewpostHandler),
    ('/([0-9]+)/?', PermalinkHandler),
    ('/([0-9]+).json/?', PermalinkJsonHandler),
    ('/flush/?', FlushcacheHandler),
    ('/admin/?', AdminHandler),
    ('/img_serve/([0-9]+/?)', ImgServe),
    ('/change_status', EnableDisableHandler),
    ('/test', TestHandler),
    ('/email_signup', EmailSignupHandler),
    ('/verify', VerifyHandler),
], debug=True)
