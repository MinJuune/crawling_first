from selenium import webdriver
from selenium.webdriver.common.by import By
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

def find_last_page():
    """현재 날짜에서 마지막 페이지 번호 찾기"""
    time.sleep(2)  # 페이지 로딩 대기
    page_numbers = driver.find_elements(By.XPATH, "//a[@data-id]")  # 페이지 번호 요소 찾기
    
    if not page_numbers:
        return 1  # 페이지가 1개뿐이라면 1페이지 반환

    last_page = max([int(p.get_attribute("data-id")) for p in page_numbers])
    return last_page

def crawl_news_by_date(date, keyword):
    """특정 날짜의 모든 뉴스 크롤링 (키워드 포함된 것만)"""
    url = f"https://sports.news.naver.com/kbaseball/news/index.nhn?isphoto=N&type=latest&date={date}"
    driver.get(url)
    time.sleep(2)  # 첫 페이지 로딩 대기

    last_page = find_last_page()  # 마지막 페이지 찾기
    print(f"{date} - 마지막 페이지: {last_page}")

    for page in range(1, last_page + 1):
        print(f"{date} - {page}페이지 크롤링 중...")
        articles = get_articles(keyword)

        for idx, article in enumerate(articles, start=1):
            print(f"{idx}. {article['title']}")
            print(f"   링크: {article['link']}\n")

        # 마지막 페이지 도달하면 종료
        if page == last_page:
            print(f"{date} - 마지막 페이지까지 크롤링 완료")
            break  

        # 다음 페이지 버튼 클릭
        next_button = driver.find_element(By.XPATH, f"//a[@data-id='{page + 1}']")
        next_button.click()
        time.sleep(2)  # 페이지 로딩 대기

# 실행 테스트
if __name__ == "__main__":
    today = datetime.today()  # 오늘 날짜 가져오기
    days_to_crawl = 7  # 최근 7일간 크롤링 
    keyword = "김택연"  # 찾고 싶은 키워드

    for i in range(1, days_to_crawl + 1):  # 어제부터 최근 N일간 크롤링
        crawl_date = (today - timedelta(days=i)).strftime("%Y%m%d")  # YYYYMMDD 형식 변환
        print(f"\n{crawl_date} 뉴스 크롤링 시작...")
        crawl_news_by_date(crawl_date, keyword)

    driver.quit()  # 실행 후 드라이버 종료
