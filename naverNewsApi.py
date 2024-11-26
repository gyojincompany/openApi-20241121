import urllib.request
import datetime
import json

client_id = ""
client_secret = ""
# 해당 url에 대한 접속 요청 후 정상적인 응답을 확인해서 결과를 반환해주는 함수
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    try:
        response = urllib.request.urlopen(req)  # 요청에 대한 응답 결과
        if response.getcode() == 200:  # 200->정상적인 응답 코드
            print(f"요청에 대한 응답 성공 [{datetime.datetime.now()}]")  # 요청 성공시 성공 텍스트 출력, 성공한 시간 출력
            return response.read().decode("utf-8")  # 응답 결과(뉴스 검색 결과) 반환
    except Exception as e:
        print(e)  # 에러의 내용을 출력
        print(f"요청에 대하여 에러 발생 url : {url} [{datetime.datetime.now()}]")  # 요청 에러 발생한 url과, 에러 발생한 시간 출력
        return None  # 요청 실패 했을 경우 아무 것도 반환하지 않음

## getRequestUrl 함수 테스트
# encText = urllib.parse.quote("프로야구")
# url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과
#
# result = getRequestUrl(url)
# print(result)

def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = f"/{node}.json"
    encText = urllib.parse.quote(srcText)
    parameters = f"?query={encText}$start={start}&display={display}"

    url = base + node + parameters
    responseDecode = getRequestUrl(url)  # 네이버 api 뉴스검색 결과 반환 받음

    if responseDecode == None:  # True->에러 발생 검색 실패
        return None
    else:  # 응답 성공 
        return json.loads(responseDecode)  # 파이썬에서 사용가능한 객체로 변환해서 반환

print(getNaverSearch("news","프로야구","1","20"))


