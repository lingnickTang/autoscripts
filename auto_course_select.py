# post a request to validate the course selection page with a cookie
# url: http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkCourse/validateXsxkTabSfkf.do POST bqdm=dywgy
import time
import requests
import json
def get_csrf_token(headers):
    from bs4 import BeautifulSoup
    url = "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkHome/gotoChooseCourse.do"
    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    csrf_token_element = soup.find(id="csrfToken")

    if csrf_token_element:
        csrf_token = csrf_token_element.get('value')
        print(f"CSRF Token: {csrf_token}")
        return csrf_token
    else:
        print("CSRF Token not found")
        return None

def get_satisfied_course_list(headers):
    timestamp = int(time.time() * 1000)
    data = {
        "query_tabszwid": 2
    }
    url = f"http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkCourse/loadXwggkCourseInfo.do?_={timestamp}"
    response = requests.post(url, data=data, headers=headers)
    response_json = json.loads(response.text)
    datas = response_json["datas"]
    course_list = []
    for data in datas:
        if data["KXRS"] - data["DQRS"] > 0 and data["KCDM"] in ["ENGL731002", "ENGL731004", "ENGL731009", "ENGL731010"]: # and data["XQMC"] == "江湾校区":
            course_list.append(data)
    return course_list
# POST a request to url http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkCourse/choiceCourse.do with data:
# bjdm: 2024202501COMP620004.01
# lx: 8
# bqmc: 学位基础课
# csrfToken: fe8a849399254e798a08c7ce835a936
def select_course(headers):
    csrf_token = get_csrf_token(headers)
    course_list = get_satisfied_course_list(headers)
    #course_list = [{"BJDM": "2024202501COMP620004.01"}]
    print(course_list)
    for course in course_list:
        data = {
            "bjdm": course["BJDM"], 
            "csrfToken": csrf_token
        }
        timestamp = int(time.time() * 1000)
        url = f"http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkCourse/choiceCourse.do?_={timestamp}"
        response = requests.post(url, data=data, headers=headers)
        print(response.text)

if __name__ == "__main__":
    headers = {
        "cookie": "_WEU=6c*UbKn68BT2qvqFT1PIJe3UYA6dmT5nKFzlRKrl6A3PNRnT5VA_wJBcnz_NKEgT; route=ece0f9f23961d30da828feef943f594a; JSESSIONID=DhDpyajn-pQSUahy4iUVWD4Ce93LhJISlGz5wJiHqrDw_lMLJPzi!416590159; XK_TOKEN=43c77bf2-71b7-4822-9442-7643fc9f96c8"    
    }
    select_course(headers)
