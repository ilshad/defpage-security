import json
import httplib2
from defpage.lib.exceptions import ServiceCallError
from defpage.security.config import system_params

def sendmail(recipients, subject, body):
    url = system_params.mail_url
    content = json.dumps({'recipients':recipients, 'subject':subject, 'body':body})
    headers = {'Content-Type':'application/json'}
    h = httplib2.Http()
    response, _c = h.request(url, "POST", content, headers)
    if response.status != 202:
        raise ServiceCallError

signup_message = u'<div style="color:#a52a2a; font-width:bold; font-size:20px;">Hello!</div>\n<p>Thank you for registering with <b>defpage.com!</b></p>\n\n<p>Verify Your Email Address Registration.\nPlease click on the confirmation link below to activate your account:\n%s</p>\n\n<p>After confirmation, use this email address and password <b><em>%s</em></b> to sign in.</p>\n\n<p>This email was sent to %s.</p>'
