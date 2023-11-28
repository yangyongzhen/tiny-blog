# encoding: utf-8
# author:yangyongzhen
from flask import  Flask,render_template,request,redirect
import articles
import statistic
import atexit
import json
import sys

app=Flask(__name__,template_folder="templates", static_folder="static", static_url_path="/static")

ItemMap = {}
ArtRouteMap = {}
ItemList = []

# NewPosts 总的文章，按时间排过序的
NewPosts = []
# NewArts 最新文章
NewArts = []
# HotArts 热门文章
HotArts = []


@app.route('/')
def index():
    articles.Stat.totalVisit += 1
    page = 1
    page = request.args.get('page',1,int)
    print(page)
    nums = len(NewPosts)
    print(nums)
    allpage = nums / 5
    if nums %5 != 0:
        allpage = int(nums/5) + 1
    print(allpage)

    curArts = NewPosts
    if (page * 5) < nums :
        curArts = NewPosts[(page-1)*5 : page*5]
    else:
        curArts = NewPosts[(page-1)*5 : nums]
    #分页表
    tabs = []
    for i in range(0,allpage+2):
        print(i)
        tabs.append(i)
    print(tabs)
    return render_template("index.html")  #加入变量传递

@app.route('/about')
def about():
    msg="my name is caojianhua, China up!"
    return render_template("about.html",data=msg)  #加入变量传递

@app.route('/items')
def items():
    try:
        id = request.args.get('id')
        print(id)
        item = ItemList[int(id)]
        print(item)
        all = ItemMap[item]
        print(all)
        msg="my name is caojianhua, China up!"
        return render_template("items.html",data=msg) 
    except Exception as e:
        return render_template('404.html')

@app.route('/article_detail')
def article_detail():
    art = articles.Article("","","","","","","","",0,0)
    item_index = 0
    try:
        id = request.args.get('id')
        #print(id)
        #取出分类
        item = ArtRouteMap[id]['item']
        #print(item)
        art = ItemMap[item][id]  
        item_index = ItemList.index(item)
        #art_index  = NewPosts.index(id)
        articles.Stat.artStat[id]['visitCnt'] += 1
        articles.Stat.totalVisit += 1
        ItemMap[item][id]['visitCnt'] = articles.Stat.artStat[id]['visitCnt']
        #print(art)
        print(item_index)
        #print(art_index)
        #Stat.artStat[id] = 
        return render_template("article_detail.html",data=art,itmIdx = str(item_index) ) 
    except Exception as e:
        print(e)
        return render_template('404.html')
   
@app.route('/moodList')
def moodList():
    msg="my name is caojianhua, China up!"
    return render_template("moodList.html",data=msg) 

@app.route('/comment')
def comment():
    msg="my name is caojianhua, China up!"
    return render_template("comment.html",data=msg) 

@app.route('/404')
def error_404():
    print("error_404")
    return render_template("404.html") 

@app.errorhandler(404)
def page_not_found(e):
    print("page_not_found")
    print(e)
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_exception(e):
    # 捕获其他异常
    print("handle_exception")
    print(e)
    return render_template('404.html'), 500
 
def saveData():
    #保存访问量数据       
    with open('statistic.json1', 'w',encoding='utf-8') as f:
        json.dump(articles.Stat.__dict__, f,ensure_ascii=False)
           
# 监控退出时保存统计信息
@atexit.register
def exit_handler():
    print("应用程序退出")
    saveData()

if __name__=="__main__":
    #启动时加载访问量数据
    ItemMap,ArtRouteMap,ItemList = articles.getPosts()
    #遍历字典
    for key, val in ItemMap.items():
        for idx,art in val.items():
            NewPosts.append(art)
            HotArts.append(art)        
    #print((NewPosts[0]))
    #按日期排序
    NewPosts.sort(key=lambda x: x['date'],reverse=True)
    #按访问量排序
    HotArts.sort(key=lambda x: x['visitCnt'],reverse=True)
    print((HotArts[0]))
    app.run(port=8000,host="127.0.0.1",debug=False)
    print("over")