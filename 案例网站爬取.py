import re  # 正则表达式，进行文字匹配
import urllib.error  # 制定URL，获取网页数据
import urllib.request

import xlwt  # 进行excel操作
from bs4 import BeautifulSoup  # 网页解析，获取数据的


def main():
    # 网页
    anliurl = 'https://ssr1.scrape.center/page/'
    # 爬取网页
    datalist = getData(anliurl)
    print(datalist)
    # 解析网页
    savepath = '案例网站数据爬取100条.xls'
    # 保存数据
    saveData(datalist,savepath)


# 电影链接
findlink = re.compile(r'<a data-v-7f856186 href="(.*?)" class>')
# 电影名称
findname = re.compile(r'<h2 data-v-7f856186 class="m-b-sm">(.*?)</h2>',re.S)
# 电影图片
findimg = re.compile(r'<img data-v-7f856186 src="(.*?)" class="cover">')
# 电影类型
findtype = re.compile(r'<button data-v-7f856186 type="button" class="el-button category el-button--primary el-button--mini"><span>(.*?)</span>')
# 电影上映地点
findplace = re.compile(r'<div data-v-7f856186 class="m-v-sm info"><span data-v-7f856186>(.*)</span>')
# 电影上映时间
findtime = re.compile(r'<div data-v-7f856186 class="m-v-sm info"><span data-v-7f856186>(.*)</span>',re.S)

# 爬取网页
def getData(anliurl):
    datalist = []
    for i in range(0,10): # 调用获取页面信息的函数*10次
        url = anliurl + str(i + 1)  # 每次网站加一即为后一个网站
        html = askURL(url) # 保存获取到的网站信息
        # 对网站数据逐一解析
    allcontent = BeautifulSoup(html,"html.parser") # <div data-v-7f856186 class="el-card item m-t is-hover-shadow">
    for content in allcontent.find_all('div',class_= "el-card item m-t is-hover-shadow"): # 从<div class="el-card__body"> 中获取数据
        data = [] # 保存获取的数据
        content = str(content)
        findLink = re.findall(findlink,content)
        data.append(findLink)
        findName = re.findall(findname ,content)
        data.append(findName)
        findImg = re.findall(findimg,content)
        data.append(findImg)
        findType = re.findall(findtype,content)
        data.append(findType)
        findPlace = re.findall(findplace,content)
        data.append(findPlace)
        findTime = re.findall(findtime,content)
        if (len(findTime) >= 1):
            Time=findPlace[1]
            data.append(Time)
        else:
            data.append(' ')
        datalist.append(data)
    return datalist

def askURL(url):
    # 模拟浏览器头部信息，向案例网站服务器发送消息
    head = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }# 用户代理*表示告诉案例网站服务器，我们是什么类型的机器，浏览器（本质上是告知服务器，我们可以接受什么水平的文件内容）
    request = urllib.request.Request(url , headers= head)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e :
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html.encode('gbk','ignore').decode('gbk')

# 将爬取获得的数据进行保存
def saveData(datalist,savepath):
    print("正在保存数据中..")
    book=xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet=book.add_sheet('案例网站数据爬取100条.xls',cell_overwrite_ok=True)
    col = ("电影链接","电影名称","电影图片","电影类型","电影上映地点","电影上映时间")
    for i in range(0,6):
        sheet.write(0,i,col[i])
    for i in range(0,100):
        print("第%d条" %i)
        data=datalist[i]
        for j in range(0,6):
            sheet.write(i+1,j,data[j])
    book.save(savepath)

if __name__ == '__main__':
    main()
    print("爬取成功")








