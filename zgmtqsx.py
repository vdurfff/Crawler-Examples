import requests
from bs4 import BeautifulSoup
import re
# from ebooklib import epub
ltitle = []
lchap = []

def get_chapinfo(chapinfo):
    for info in chapinfo:
        chap_num = info.contents[3].text
        title = info.contents[5].text
        # show the right Chinese characters, and remove all the blanks
        chap_num_text = chap_num.encode('iso-8859-1').decode('gbk').strip()
        chap_num_text = re.sub('\[.*\]','',chap_num_text)
        title_text = title.encode('iso-8859-1').decode('gbk').strip()
        # write the title information into list
        lchap.append(chap_num_text)
        ltitle.append(title_text)

headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79'
}

# get title name
# send request to jjwxc
url_title = 'https://www.jjwxc.net/onebook.php?novelid=4737103'
response_title = requests.get(url_title,headers=headers)

# make soup
soup = BeautifulSoup(response_title.text,'html.parser')
chapinfo = soup.findAll('tr',attrs={'itemprop':'chapter'})
Newchapinfo = soup.findAll('tr',attrs={'itemprop':'chapter newestChapter'})

get_chapinfo(chapinfo)
get_chapinfo(Newchapinfo)  
# print(lchap)
# print(ltitle)

fileName = "D:\系统默认\Documents\Crawler\砸锅卖铁去上学\Aug13test05.txt"
fileObject = open(fileName, "w")
error = 0

for num in range(1,338):
    fileObject.write(lchap[num-1] + ' ' + ltitle[num-1])
    fileObject.write('\n\n')

    # ask for request
    url = 'https://www.biququ.info/html/44051/55063' +str(num) + '.html'
    response = requests.get(url,headers=headers)
    # print(response.text)

    # make the soup
    soup = BeautifulSoup(response.text,'html.parser')

    # get content
    allcontent = soup.find('div',attrs={'id':'content'})
    contents = allcontent.findAll('p')
    for content in contents:
        if 'app' not in content.string:
            try:
                # print(content.string)
                fileObject.write(content.string + '\n')
            except:
                error = error+1
                fileObject.write('[ERROR]\n')
                print('ERROR: Can\'t write in chapter ', num)
    fileObject.write('\n\n')
    print('Chapter ', num, ' OK')
    # print(str(content).replace('[' and ']',''))

# Close the file
fileObject.close() 
print('DONE')
print('Num of errors: ', error)      




##########  Ebooklib --failed ##########
# book = epub.EpubBook()
# book.set_title('砸锅卖铁去上学')
# book.set_author('红刺北')
# chapter1 = epub.EpubHtml(title='第一章', file_name='chapter1.xhtml', lang='en')
# chapter1.content = content
# book.add_item(chapter1)

# book.toc = (epub.Link('chapter1.xhtml', '第一章', 'chapter1'),)
# book.add_item(epub.EpubNcx())
# book.add_item(epub.EpubNav())

# epub.write_epub('doupo.epub', book, {})