# encoding: utf-8
# author:yangyongzhen
import glob
import os
import pprint
import hashlib
import json
import statistic

#访问量阅读量统计信息
Stat = statistic.AllStat()

# AllArts 总的文章，(按时间排过序的)
AllArts = []
# NewArts 最新文章
NewArts = []
# HotArts 热门文章
HotArts = []
# 文章分类信息
ItemList = []

ItemMap = {}
ArtRouteMap = {}

#文章信息类定义
class Article(object):
    def __init__(self, id, item, title, date, summary, body, imgFile, author, cmtCnt, visitCnt):
        self.id = id
        self.item = item
        self.title = title
        self.date = date
        self.summary = summary
        self.body = body
        self.imgFile = imgFile
        self.author = author
        self.cmtCnt = cmtCnt
        self.visitCnt = visitCnt
    
    def mPrint(self):
        print(self.id)
        print(self.item)
        print(self.title)
        print(self.date)
        print(self.summary)
        print(self.body)
        print(self.imgFile)
        print(self.author)


class ArticlesData():
    def __init__(self):
        self.item = ""
        self.articlesMap = {}


# ArticleRoute 文章的分类和路径信息
class ArticleRoute:
    def __init__(self, item, name):
        self.item = item
        self.name = name

#文章分类 是个集合类型，无重复元素
class ItemCfg:
    def __init__(self):
        self.items = set()
        
        
def strTrip(src):
    str = src.replace(" ", "")
    str = str.replace("\r", "")
    str = str.replace("\n", "")
    return str


#从文件中读取信息,并返回itemMap,artRouteMap,items
def getPosts():
    global ItemMap,ArtRouteMap,ItemList,NewArts
    # 打开访问量统计JSON文件并读取内容
    try:
        with open('statistic.json1', 'r',encoding='utf-8') as f:
            json_data = f.read()
            # 将JSON字符串反序列化为字典对象
            Stat.__dict__ = json.loads(json_data)
            print(Stat.totalVisit)
    except Exception as e:
        with open('statistic.json1', 'w',encoding='utf-8') as f:
            json.dump(Stat.__dict__, f,ensure_ascii=False)

    # 获取"posts/"目录下的所有文件
    files = glob.glob("posts/*")
    # 按修改日期进行排序
    files = sorted(files, key=lambda x: os.path.getmtime(x))
    articleMap = {}
    itemMap = {}
    artRouteMap = {}
    #文章分类，是个集合类型，无重复
    items = set()
    # 遍历文件列表
    for i, f in enumerate(files):
        #print(i)
        #print(f)

        file = f
        file = os.path.basename(file) # 转换路径分隔符
        print(file)
        file = os.path.splitext(file)[0]  # 移除".md"后缀
        fileread = open(f, 'r',encoding='utf-8').read()
        lines = fileread.split('\n')
        #print(lines)
        title = lines[0].strip()
        date = strTrip(lines[1].strip())
        summary = lines[2].strip()
        imgfile = lines[3].strip()
        id = hashlib.md5(file.encode(encoding='UTF-8'))
        id = id.hexdigest()
        #print(id.hexdigest())
        item = strTrip(lines[4].strip())
        author = lines[5].strip()
        imgfile = strTrip(imgfile)
        body = '\n'.join(lines[6:])  # 获取第6行及以后的行
        ar = ArticleRoute(item, title)
        artRouteMap[id] = ar.__dict__
        visitCnt = 0 #访问量
        commentCnt = 0 #评论数
        if id in Stat.artStat:
           visitCnt = Stat.artStat[id]['visitCnt']
           commentCnt = Stat.artStat[id]['commentCnt']
           #print(visitCnt)
        else:
            Stat.artStat[id] = statistic.ArtStat(title,visitCnt,commentCnt).__dict__
        post = Article(id,item,title, date, summary, body, imgfile, author, 0,visitCnt)
        articleMap[id] = post
        items.add(item)
    #json_data = json.dumps(posts,ensure_ascii=False)
    #print(json_data)
    itemList = []
    for itm in items:
        itmMp= {}
        for v in articleMap.values():
            if(v.item == itm):
                itmMp[v.id] = v.__dict__
        itemMap[itm] = itmMp
        itemList.append({'item':itm,'count':len(itemMap[itm])})
            
        
    #保存为json文件
    with open('Articles.json1', 'w',encoding='utf-8') as f:
        json.dump(itemMap, f,ensure_ascii=False)
        
    with open('artRouteMap.json1', 'w',encoding='utf-8') as f:
        json.dump(artRouteMap, f,ensure_ascii=False)
        
    with open('itemList.json1', 'w',encoding='utf-8') as f:
        json.dump(itemList, f,ensure_ascii=False)
    
    #遍历字典
    for key, val in itemMap.items():
        for idx,art in val.items():
            AllArts.append(art)
            HotArts.append(art)        
    #按日期排序
    AllArts.sort(key=lambda x: x['date'],reverse=True)
    #按访问量排序
    HotArts.sort(key=lambda x: x['visitCnt'],reverse=True)
    NewArts = AllArts
    ItemList = itemList
    #print((HotArts[0]))
    ItemMap = itemMap
    ArtRouteMap = artRouteMap
    return itemMap,artRouteMap,itemList

if __name__=="__main__":
    p,p1,items = getPosts()
    #print(p)
    print(type(p))
    print(type(p1))
    print(p['go学习笔记'])
    print(p1['3eaf98ad2b949b3f93d16aeaa1f45ab0'])
    print(items)