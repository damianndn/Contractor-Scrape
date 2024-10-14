from bs4 import BeautifulSoup
import requests
import certifi

url = "https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail-v2&type=es-plan-project-p&stepCode=plan-step-1&id=00ea76bd-966e-4bc8-b5c4-a0a5580a4e38&notifyId=undefined&inputResultId=undefined&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=undefined&bidMode=undefined&notifyNo=undefined&planNo=PL2400223718&pno=undefined&step=tbmt&isInternet=undefined&caseKHKQ=undefined"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url, verify=False)

print(response.status_code)