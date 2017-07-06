
# -*- coding=utf-8 -*-
import math
import sys,codecs
from texttable import Texttable
from collections import defaultdict
from operator import itemgetter

#读取文件
def readFile(fileData):
    data=[]
    rates=[]
    f=open(fileData,"r")
    data=f.readlines()
    f.close()
    for line in data:
        dataLine=line.split("\t")
        rates.append([int(dataLine[0]),int(dataLine[1]),int(dataLine[2])])

    return rates

#   创建字典，生成用户评分的数据结构
#   输入：数据集合，格式：用户id\t硬盘id\t用户评分
#   输出:1.用户字典：dic[用户id]=[(电影id,电影评分)...]
#        2.电影字典：dic[电影id]=[用户id1,用户id2...]
def createDict(rates):
    user_dict={}
    movie_dict={}
    for i in rates:
        if i[0] in user_dict:
            user_dict[i[0]].append((i[1],i[2]))
        else:
            user_dict[i[0]]=[(i[1],i[2])]
        if i[1] in movie_dict:
            movie_dict[i[1]].append(i[0])
        else:
            movie_dict[i[1]]=[i[0]]
    return user_dict,movie_dict


#建立物品倒排表,计算物品相似度
def itemCF(user_dict):
    N=dict()
    C=defaultdict(defaultdict)
    W=defaultdict(defaultdict)
    for key in user_dict:
        for i in user_dict[key]:
            if i[0] not in N.keys(): #i[0]表示movie_id
                N[i[0]]=0
            N[i[0]]+=1               #N[i[0]]表示评论过某电影的用户数
            for j in user_dict[key]:
                if i==j:
                    continue
                if j not in C[i[0]].keys():
                    C[i[0]][j[0]]=0
                C[i[0]][j[0]]+=1      #C[i[0]][j[0]]表示电影两两之间的相似度，eg：同时评论过电影1和电影2的用户数
    for i,related_item in C.items():
        for j,cij in related_item.items():
            W[i][j]=cij/math.sqrt(N[i]*N[j])
    return W

#结合用户喜好对物品排序
def recommondation(user_id,user_dict,K):
    rank=defaultdict(int)
    l=list()
    W=itemCF(user_dict)
    for i,score in user_dict[user_id]: #i为特定用户的电影id，score为其相应评分
        for j,wj in sorted(W[i].items(),key=itemgetter(1),reverse=True)[0:K]: #sorted()的返回值为list,list的元素为元组
            if j in user_dict[user_id]:
                continue
            rank[j]+=score*wj #先找出用户评论过的电影集合，对每一部电影id，假设其中一部电影id1,找出与该电影最相似的K部电影，计算出在id1下用户对每部电影的兴趣度，接着迭代整个用户评论过的电影集合，求加权和，再排序，可推荐出前n部电影，我这里取10部。
    l=sorted(rank.items(),key=itemgetter(1),reverse=True)[0:10]
    return l


#获取电影列表
def getMovieList(item):
    items={}
    f=codecs.open(item,"r",encoding="utf-8")
    movie_content=f.readlines()
    f.close()
    for movie in movie_content:
        movieLine=movie.split("|")
        items[int(movieLine[0])]=movieLine[1:]
    return items

#主程序
if __name__=='__main__':
    itemTemp=getMovieList("./ml-100k/u.item") #获取电影列表
    fileTemp=readFile("./ml-100k/u.data")     #读取文件
    user_dic,movie_dic=createDict(fileTemp)                     #创建字典
    user_id=1
    movieTemp=recommondation(user_id,user_dic,80)               #对电影排序

    rows=[]
    table=Texttable()                                           #创建表格并显示
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t','f','a'])
    table.set_cols_align(["l","l","l"])
    rows.append(["user name","recommondation_movie","from userid"])
    for i in movieTemp:
        rows.append([user_id,itemTemp[i[0]][0],""])
    table.add_rows(rows)
    print(table.draw())