# encoding: utf-8
# author:yangyongzhen
# 文章和总阅读量统计

#文章访问量统计
#param:名称，访问量，评论量
class ArtStat:
    def __init__(self, title,visitCnt,cmtCnt):
        self.title = title
        self.visitCnt = visitCnt
        self.commentCnt = cmtCnt
  
#总的统计        
class AllStat:
    #Notice通知
    notice = ''
    top_art= ''
    def __init__(self):
        #总访问量
        self.totalVisit = 0
        self.artStat = {}


if __name__=="__main__":
    pass