from selenium import webdriver as wd
from bs4 import BeautifulSoup
from konlpy.tag import Okt
# from wordcloud import WordCloud
# import pandas as pd
# import matplotlib.pyplot as plt
import time
import re
import json
import sys


url = [sys.argv[1]]

def craw(url):
    options = wd.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51')
    
    driver = wd.Chrome(executable_path="C:/users/dnd/desktop/git capstone/public/python/chromedriver", options=options)
    
    full_comments = []
    comments = []
    sorted_comments = []
    words = []
    title = []
        
    wordCount = {}

    for x in range(len(url)):
        driver.get(url[x])
        
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        while True: 
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") 
            time.sleep(3.0)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            
            if new_page_height == last_page_height:
                break 
            last_page_height = new_page_height
        
        html = driver.page_source 
        
        soup = BeautifulSoup(html, "html.parser")

        likes = []
        get_likes = soup.findAll("span", {"id" : "vote-count-left"})
        
        for i in range(0, len(get_likes)):
            like_tmp = get_likes[i].text
            like_tmp = like_tmp.replace('\n', '')
            like_tmp = like_tmp.replace('    ', '')
            like_tmp = like_tmp.replace('  ', '')
            like_tmp = like_tmp.replace(' ', '')
            if '.' in like_tmp:
                like_tmp = like_tmp.replace('.', '')
                like_tmp = like_tmp.replace('천', '00')
                like_tmp = like_tmp.replace('만', '000')    
            else:
                like_tmp = like_tmp.replace('천', '000')
                like_tmp = like_tmp.replace('만', '0000')
            likes.append(int(like_tmp))
        
        youtube_title = soup.select('h1')
        
        title_tmp = str(youtube_title[0].text)
        title_tmp = title_tmp.replace('/', '')
        title_tmp = title_tmp.replace('?', '')
        title_tmp = title_tmp.replace('*', '')
        title_tmp = title_tmp.replace('"', '')
        title_tmp = title_tmp.replace('|', '')
        title.append(title_tmp)
    
        okt = Okt()
        
        str_youtube_comments = []
        
        
        hangul = re.compile('[가-힣]+')
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        youtube_comments = soup.select('yt-formatted-string#content-text')
        
        tmp_comments = []
        
        for i in range(len(youtube_comments)):
            com_tmp = str(youtube_comments[i].text)
            com_tmp = com_tmp.replace('\n', ' ')
            com_tmp = com_tmp.replace("'", '')
            com_tmp = com_tmp.replace('"', '')
            com_tmp = com_tmp.replcae('(', '')
            com_tmp = com_tmp.replcae(')', '')
            com_tmp = com_tmp.replcae('-', '')
            com_tmp = re.sub(emoji_pattern,'', com_tmp)
            
            full_comments.append(com_tmp)
            tmp_comments.append(com_tmp)
            
            com_tmp = okt.nouns(com_tmp)              
            com_tmp = re.findall(hangul, str(com_tmp)) 
            str_youtube_comments.append(com_tmp)
    
        lnc = list(zip(likes, tmp_comments))
        lnc = sorted(lnc, reverse=True)
    
        for i in range(0, 20):
            comments.append(lnc[i])
    
        filter_list = ['', '진짜', '다', '너무', '잘', '저', '더','이','엄마','로그','덕분','는','사시','건가','삶'
                        , '왜', '수', '이걸', '내가', '그냥', '이거', '근데', '한','이모','응원','일','직접','가출'
                        , '내', '저는', '안', '그', '뭔가', '계속', '정말', '나만','행복','본인','우리','가요','볼때'           
                        , '이렇게', '저렇게', '와', '지금', '전', '너무너무', '항상','사랑','힐링','화이팅','역시','듯'
                        ,'개수','감사','한국','쓰',"거","하루","요","사람","아이",'제발','알','좀','사생활','가까이'
                        , '많이', '저도', '보고', '제가', '것','얼마나','예쁜','꼭', '제','세상','브이','킹','곳','혹시'
                        ,'행복한','처음','니', '말', '마음', '시간', '뭐', '언니', '영상','가족','걱정','딸','해','동영상'
                        , '오늘도', '같아요', '아니', '아', '헉', '다시', '언니가', '알았는데','삼','씨','형','분','살'
                        ,'넘', '또', '같이','자주','요즘','오늘','귀여워','귀여워요','좋아','구독','축하','독자','하나'
                        , '늘', '댓글', '때', '나', '데','음','앞','진심','생각','조','중','공감','대리','내일','중간'
                        ,'관리','모습','지역','동네','완전','저런','저희','동생','오빠','아빠','급상승','인기','사이'
                        ,'이제','감동','눈물','음버','느낌','바로','유산','한번', '당신','추가','정보','여기','누나','최고'
                        ,'이건','알고리즘','썸네일','홀린','사투리','썸넬','어디','갑자기','관심','주행','분위기','매력'
                        ,'유튜브','개','기네','만','로','줄','도','혹시알','보기','다행','너','용','아랍인','위','구매처'
                        ,'후','워','절음','부분','선생님','대박','발','륜쌩님','오','매번','사용','튜브','건','디테'
                        ]
    
        for i in range(0, len(str_youtube_comments)):
            for word in str_youtube_comments[i]:
                if word in filter_list:
                    continue
                else:
                    wordCount[word] = wordCount.get(word, 0) + 1
                    
    comments = sorted(comments, reverse=True)
    
    for i in range(0, 20):
        sorted_comments.append(comments[i])
                
    result = sorted(wordCount.items(), key=lambda x:-x[1])
    
    for i in range(0, 20):
        words.append(result[i])
        
    full_comments = sorted(lnc, reverse=True)
    
    driver.close()
    
    return words, sorted_comments, full_comments, title
    
        # wordincomment = []
            
        #     for i in range(len(topword)):
        #         for j in range(len(lnc)):
        #             word = topword[i]
        #             if word in str(lnc[j][1]):
        #                 wordincomment.append(str(lnc[j][1]))
        #                 del(lnc[j])
        #                 break
                    
        #     topword.insert(0, title)
        #     wordincomment.insert(0, url[x])        
        
            # print('영상 제목 : ' + title)
# def make_wordcloud(words, title):
#     wc = WordCloud(font_path='./NanumGothic.ttf',               
#                         background_color="white",
#                         width=3000,
#                         height=2000,
#                         max_words=20,
#                         max_font_size=700)
        
#     wcr = wc.generate_from_frequencies(dict(words))
#     # wcr.to_file('./results/{}'.format( + '.png'))
#     plt.figure(figsize=(10,8))
#     plt.axis('off')
#     plt.imshow(wcr)
#     plt.show()

# def make_csv(words, comments):
#       df = pd.DataFrame({'단어' : words, '댓글' : comments})
#       df.to_csv('./results/{}'.format(title[0] + '.csv'), encoding='utf-8-sig')

def search(full_comments):
    while True:
        s_comment = []
        word = input('검색할 단어를 입력하세요: ') 
        for i in range(len(full_comments)):
            if word in full_comments[i][1]:
                s_comment.append(full_comments[i][1])
        # df = pd.DataFrame({'댓글' : s_comment})
        # df.to_csv('./results/{}'.format(word + '.csv'), encoding='utf-8-sig')       

word, comment, full_comment, title = craw(url)    

words = []
comments = []
full_comments = []

for i in range(0, 20):
    words.append(word[i][0])

for i in range(0, 20):
    comments.append(comment[i][1])
    
for i in range(len(full_comment)):
    full_comments.append(full_comment[i][1])

words_json = json.dumps(words)
comments_json = json.dumps(comments)
full_comments_json = json.dumps(full_comments)
title_json = json.dumps(title)

print(words_json)
print(comments_json)
print(full_comments_json)
print(title_json)
# make_csv(words,comments)
# make_wordcloud(words, title)
# search(full_comments)