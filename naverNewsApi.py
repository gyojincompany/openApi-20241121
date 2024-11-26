import urllib.request
import datetime
import json

client_id = "oNkjxMAROssEBw5enKkU"
client_secret = "e98SgRiuR2"


# 해당 url에 대한 접속 요청 후 정상적인 응답을 확인해서 결과를 반환해주는 함수
jsonResult = []
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

# print(getNaverSearch("news","프로야구","1","20"))



def getPostData(post, jsonResult, cnt):
    title = post["title"]  # 뉴스 제목
    description = post["description"]  # 뉴스 요약
    org_link = post["originallink"]  # 뉴스 기사의 원본 신문사 링크
    link = post["link"]  # 네이버에서 링크한 기사 링크
    # post["pubDate"]
    pDate = datetime.datetime.strptime(post["pubDate"], "%a, %d %b %Y %H:%M:%S +0900")
    # 원본 시간형식 'Wed, 19 Jul 2023 17:24:00 +0900' 에서 각 값을 가져오기
    pDate = pDate.strftime("%Y-%m-%d %H:%M:%S")   # 2024-11-26 10:29:37 형식으로 변환
    jsonResult.append({"cnt":cnt, "title":title, "description":description, "org_link":org_link, "link":link, "pDate":pDate})

    return jsonResult

node = "news"  # 검색할 카테고리
srcText = "프로야구"  # 검색어

# news 카테고리에서 "프로야구" 검색어로 1번부터 100번까지 100개의 검색 결과를 가져옴
jsonResponse = getNaverSearch(node, srcText, "1", "100")
# jsonResponse = getNaverSearch(node, srcText, 101, 100) True
# jsonResponse = getNaverSearch(node, srcText, 201, 100) True
# jsonResponse = getNaverSearch(node, srcText, 301, 100) True  -> total이 330개라 가정하면 마지막 30개의 결과만 들어있음
# jsonResponse = getNaverSearch(node, srcText, 401, 100) False -> None 값으로 반환


total = jsonResponse["total"]  # 검색된 뉴스 기사의 총 개수
resultList = []  # 최종 결과가 들어갈 빈 리스트 선언
cnt = 0

while (jsonResponse != None) and (jsonResponse["display"] != 0):
    for post in jsonResponse["items"]:
        cnt = cnt + 1
        getPostData(post, resultList, cnt)

    start = jsonResponse["start"] + jsonResponse["display"]
    jsonResponse = getNaverSearch(node, srcText, start, "100")


print(f"검색된 총 뉴스 기사 수 : {total}건")

with open(f"{srcText}_naver_{node}.json","w",encoding="utf-8") as outfile:
    jsonFile = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(jsonFile)

print(f"네이버 Api에서 가져온 총 뉴스 데이터 수 : {cnt}")

## 파일 불러오기 참고
# f = open("abc.txt","w")
# f.write("안녕하세요")
# f.close()
#
# with open("abc.txt","w") as f:
#     f.write("안녕하세요")









