from flask import Flask, request
from bs4 import BeautifulSoup
import requests



app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def process_webhook():
    request_json = request.json

    # naver-book 인텐트 중 book 파라미터 데이터 추출
    query = request_json["queryResult"]["parameters"]["movie"]
    print(query)
    # 인증 정보
    client_id = "jNok5qfqfnVlZR_wV1ns"
    client_secret = "IiwFA0bYPc"

    # 기본 url 정보
    url = "https://openapi.naver.com/v1/search/movie.json"

    # url 호출 시 전달할 요청 변수 정보
    params = {"query": query,
              "display": 1}

    # requests 라이브러리를 이용한 책 검색 api 호출
    # get 방식으로 호출(url)/ 요청 변수 전달(params)/ 인증 정보 및 인코딩 정보 전달(header)
    response = requests.get(url=url, params=params,
                            headers={"X-Naver-Client-Id": client_id,
                                     "X-Naver-Client-Secret": client_secret,
                                     "Content-Type": "application/json; charset=utf-8"})
    # 호출 처리 상태 정보 recode 변수에 할당
    rescode = response.status_code

    if (rescode == 200):
        # 호출 처리 상태가 정상(200) 일 경우리턴 받은 책 조회 정보 출력
        # pprint.pprint(response.json())
        data = response.json()
    else:
        print("Error Code:", rescode)

    # print(data)
    # Naver 책 검색 API 응답 중 실제 책 아이템 데이터 추출 및 출력
    item_list = data["items"]
    # pprint.pprint(item_list)
    # print(item_list[0]['actor'])

    # print(answer)
    # Dialogflow로 응답되는 최종 문자열 데이터 구성
    # book_list = ""
    # for item in item_list:
    #     book_list += item["title"]
    #     book_list += " "

    # Dialogflow로 응답되는 최종 데이터 확인
    # print(book_list)
    title = BeautifulSoup(item_list[0]['title'],'html.parser').text

    return {"fulfillmentText": "This is a text response",
      "fulfillmentMessages": [
        {
          "card": {
            "title": title,
            "subtitle": "출연진:"+item_list[0]['actor']+'\n'+"평점:"+item_list[0]['userRating']+"\n"+"감독 : "+item_list[0]['director']+'\n'+"개봉년도:"+item_list[0]['pubDate'],
            "imageUri": item_list[0]['image'],
            "buttons": [
              {
                "text": "button text",
                # "postback": "https://assistant.google.com/"
              }
            ]
          }
        }
      ]}


if __name__ == '__main__':
    app.run(debug=True)