from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

# 크롬 웹드라이버 실행
driver = webdriver.Chrome()

def get_articles(keyword):
    """현재 페이지에서 뉴스 기사 크롤링 (키워드 포함된 것만)"""
    time.sleep(2)  # 페이지 로딩 대기
    articles = driver.find_elements(By.CLASS_NAME, "title")  # 뉴스 제목 가져오기
    news_list = []

    for article in articles:
        title = article.text  # 뉴스 제목 가져오기 
        link = article.get_attribute("href")  # 기사 링크 가져오기

        if keyword in title:  # 특정 키워드 포함된 기사만 저장
            news_list.append({"title": title, "link": link})

    return news_list

def get_last_page():
    """현재 열린 페이지에서 마지막 페이지 번호 찾기 ('다음' 버튼이 없어질 때까지 확인)"""
    time.sleep(2)  # 페이지 로딩 대기
    last_page = 1  # 기본값 설정

    while True:
        # 현재 보이는 페이지 번호들 가져오기
        pages = driver.find_elements(By.XPATH, "//div[@class='paginate']//a[@data-id]")
        print(f"pages: {pages}")
        # data-id 값 가져오기 (숫자로 변환 후 리스트 생성)
        page_numbers = [int(p.get_attribute("data-id")) for p in pages if p.get_attribute("data-id") and p.get_attribute("data-id").isdigit()]
        print(f"page_numbers: {page_numbers}")
        if page_numbers:
            last_page = max(last_page, max(page_numbers))  # 가장 큰 페이지 번호 업데이트

        # '다음' 버튼이 있으면 클릭해서 다음 블록 확인
        try:
            next_button = driver.find_element(By.XPATH, "//a[@class='next']")
            next_button.click()  # '다음' 버튼 클릭
            time.sleep(2)  # 페이지 로딩 대기
        except:
            print(f"마지막 페이지: {last_page}")
            break  # '다음' 버튼이 없으면 종료

    return last_page


def crawl_news_by_date(date, keyword):
    """특정 날짜의 모든 뉴스 크롤링 (키워드 포함된 것만)"""
    
    # 해당 날짜의 첫 번째 페이지 URL 접근
    url = f"https://sports.news.naver.com/kbaseball/news/index.nhn?isphoto=N&type=latest&date={date}&page=1"
    driver.get(url)
    time.sleep(2)  # 페이지 로딩 대기

    # 마지막 페이지 번호 찾기
    last_page = get_last_page()
    print(f"{date} - 총 {last_page} 페이지 존재")

    # 1페이지부터 마지막 페이지까지 직접 URL을 변경해서 접근
    for page in range(1, last_page + 1):
        url = f"https://sports.news.naver.com/kbaseball/news/index.nhn?isphoto=N&type=latest&date={date}&page={page}"
        driver.get(url)
        time.sleep(2)  # 페이지 로딩 대기

        print(f"{date} - {page}페이지 크롤링 중...")
        articles = get_articles(keyword)

        for idx, article in enumerate(articles, start=1):
            print(f"{idx}. {article['title']}")
            print(f"   링크: {article['link']}\n")

# 실행 테스트
if __name__ == "__main__":
    today = datetime.today()  # 오늘 날짜 가져오기
    days_to_crawl = 5  # 최근 5일간 크롤링 
    keyword = "김택연"  # 찾고 싶은 키워드

    for i in range(1, days_to_crawl + 1):  # 어제부터 최근 N일간 크롤링
        crawl_date = (today - timedelta(days=i)).strftime("%Y%m%d")  # YYYYMMDD 형식 변환
        print(f"\n{crawl_date} 뉴스 크롤링 시작...")
        crawl_news_by_date(crawl_date, keyword)

    driver.quit()  # 실행 후 드라이버 종료