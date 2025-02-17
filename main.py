import requests
from bs4 import BeautifulSoup

# 네이버 야구 뉴스 URL
URL = "https://sports.news.naver.com/kbaseball/news/index.nhn?isphoto=N&type=latest"
HEADERS = {"User-Agent": "Mozilla/5.0"} # 크롤링 차단 방지(브라우저처럼 요청하기)

# 뉴스 목록 크롤링
def get_articles():
    """네이버 스포츠 뉴스에서 '김택연' 관련 기사 가져오기"""
    response = requests.get(URL, headers=HEADERS) #웹페이지 요청(GET)
    soup = BeautifulSoup(response.text, "html.parser") #HTML 파싱
    #beautifulsoup을 사용해 html을 python이 다룰 수 있는 객체로 변환

    articles = soup.select("ul.NewsList_news_list__kZ6GC li.NewsList_news_item__1nchX")  # 뉴스 목록 선택
    news_list = []

    for article in articles:
        title_tag = article.select_one("em.NewsList_title__2_pof")  # 기사 제목 태그
        link_tag = article.select_one("a.NewsList_link_news__3-GnG")  # 기사 링크 태그

        if title_tag and link_tag: # 제목가 링크가 존재하는 경우 
            title = title_tag.text.strip() # 기사 제목 가져오기 
            link = link_tag["href"] # 기사 링크 가져오기 

            # 상대 경로일 경우 전체 URL로 변환
            if link.startswith("/kbaseball"):
                link = "https://sports.news.naver.com" + link

            news_list.append({"title": title, "link": link})
            print(f"[NEW] {title} → {link}")

    return news_list
   
   
# 테스트 실행
if __name__ == "__main__":
    get_articles()
