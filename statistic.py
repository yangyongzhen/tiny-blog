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
    def __init__(self,total,ntce,topArt):
        self.totalVisit = total
        self.ntce = ntce
        self.top_art= topArt
        self.artStat = {}


#访问量阅读量统计信息
Stat = AllStat(0,'','')

if __name__=="__main__":
    pass