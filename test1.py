# -*- coding: UTF-8 -*-
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings("ignore")
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import sys
# sys.path.extend(['D:\\workspacePy', 'D:\workspacePy\RecQ\RecQ-master-Help','D:\workspacePy\RecQ\RecQ-master-Help\main1'])
import numpy as np
import pymysql
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt

def get_sql_data():
    # 连接mysql
    con = pymysql.connect(host="localhost", user="root", password="blwy1113", db="deliciousfoods")
    cursor = con.cursor()  # 创建游标
    # 读取表数据
    data_sql_pd = pd.read_sql("select * from user_info", con)
    # print(data_sql_pd.head(), data_sql_pd.shape)  # Dataframe类型
    return data_sql_pd,cursor,con

if __name__=="__main__":
    data_sql_pd,cursor,conn=get_sql_data()  # 读取所有表数据
    useful_data=data_sql_pd[['id','name','password','nickName','sex','age','birthday','phone','address','email','cardId','level']]
    useful_data = useful_data.drop_duplicates(subset=['id'], keep='last', inplace=False)  # 评分去重
    userdict=dict(zip(range(len(useful_data['id'].values.tolist())),useful_data['id'].values.tolist()))
    useful_data=useful_data[['sex', 'age','address','level']]

    dict_address=dict(zip(list(set(useful_data['address'].values.tolist())),range(len(list(set(useful_data['address'].values.tolist()))))))
    useful_data['address'] = useful_data['address'].map(dict_address)
    print(useful_data)

    dict_sex=dict(zip(list(set(useful_data['sex'].values.tolist())),range(len(list(set(useful_data['sex'].values.tolist()))))))
    useful_data['sex'] = useful_data['sex'].map(dict_sex)
    useful_data=useful_data.fillna(useful_data.mean())
    print(useful_data)

    df = useful_data

    content = df.apply(pd.to_numeric, errors='coerce')

    a=np.array(content)
    # #创建绘制三维图的环境
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # #绘制图像
    # ax.scatter(content[0], content[2], content[3], c=content[3], cmap='rainbow')
    # #调整观察角度和方位角。这里将俯仰角设为30度，把方位角调整为-45度
    # ax.view_init(30, -45)
    # plt.show()

    #生成空矩阵用于存储各簇的数据
    b=np.zeros(0)
    c=np.zeros(0)
    d=np.zeros(0)


    res=[]
    #随机选择三个中心点，计算所有值到中心点的距离
    for i in range(0,len(a)):
        dis1=np.linalg.norm(a[i:i+1]-a[1:2])
        dis2=np.linalg.norm(a[i:i+1]-a[2:3])
        dis3=np.linalg.norm(a[i:i+1]-a[3:4])
        # 根据每个点与各个簇中心的距离将每个对象重新赋给最近的簇
        if min(dis1,dis2,dis3)==dis1:
            b=np.append(b,a[i:i+1])
            x=int(len(b)/4)
            b=np.reshape(b,newshape=(x,4))
        if min(dis1,dis2,dis3)==dis2:
            c=np.append(c,a[i:i+1])
            x=int(len(c)/4)
            c=np.reshape(c,newshape=(x,4))
        if min(dis1,dis2,dis3)==dis3:
            d=np.append(d,a[i:i+1])
            x=int(len(d)/4)
            d=np.reshape(d,newshape=(x,4))
    #对新生成的簇的所有值求平均值来获得新的簇中心点
    b=np.mean(b,axis=0)
    c=np.mean(c,axis=0)
    d=np.mean(d,axis=0)
    #创建k_mean函数
    def k_mean(b,c,d):
        #储存新的簇中的所有点
        list1 = []
        list2 = []
        list3 = []
        #储存新的簇中心点
        gap1 = b
        gap2 = c
        gap3 = d
        #生成空矩阵用于存储各簇的数据
        b = np.zeros(0)
        c = np.zeros(0)
        d = np.zeros(0)
        #计算所有值到新的簇中心点的距离
        for i in range(0,len(a)):
            dis1=np.linalg.norm(a[i:i+1]-gap1)
            dis2=np.linalg.norm(a[i:i+1]-gap2)
            dis3=np.linalg.norm(a[i:i+1]-gap3)
            # 根据每个点与各个簇中心的距离将每个对象重新赋给最近的簇
            if min(dis1, dis2, dis3) == dis1:
                list1.append(userdict[i])
                b = np.append(b, a[i:i + 1])
                x = int(len(b) / 4)
                b = np.reshape(b, newshape=(x, 4))
            if min(dis1, dis2, dis3) == dis2:
                list2.append(userdict[i])
                c = np.append(c, a[i:i + 1])
                x = int(len(c) / 4)
                c = np.reshape(c, newshape=(x, 4))
            if min(dis1, dis2, dis3) == dis3:
                list3.append(userdict[i])
                d = np.append(d, a[i:i + 1])
                x = int(len(d) / 4)
                d = np.reshape(d, newshape=(x, 4))
        #将新生成的簇的所有值转化为多维向量
        line1= pd.DataFrame(b)
        line2=pd.DataFrame(c)
        line3=pd.DataFrame(d)
        #对新生成的簇的所有值求平均值来获得新的簇中心点
        b=np.mean(b,axis=0)
        c=np.mean(c,axis=0)
        d=np.mean(d,axis=0)
        #当簇的中心点不再发生明显的变化时停止递归
        if abs(sum(b - gap1))+abs(sum(c - gap2))+abs(sum(d - gap3))<10**(-64):
            # 创建out_file用于存储输出结果
            out_file = open('out_file1.txt', 'w')
            out_file.write('class1\n')
            out_file.writelines(str(list1))
            out_file.write('\nclass2\n')
            out_file.writelines(str(list2))
            out_file.write('\nclass3\n')
            out_file.writelines(str(list3))
            res.append(list1)
            res.append(list2)
            res.append(list3)

            # 三维散点的数据
            x1 = line1[0]
            y1 = line1[2]
            z1 = line1[3]
            x2 = line2[0]
            y2 = line2[2]
            z2 = line2[3]
            x3 = line3[0]
            y3 = line3[2]
            z3 = line3[3]
            #创建绘制三维图的环境
            fig = plt.figure()
            ax = Axes3D(fig)
            # 绘制散点图
            ax.scatter(x1, y1, z1,cmap='Blues',label='Setosa')
            ax.scatter(x2, y2, z2,c='g',label='Versicolor',marker='D')
            ax.scatter(x3, y3, z3,c='r',label='Virginica')
            ax.legend(loc='best')
            # 调整观察角度和方位角。这里将俯仰角设为30度，把方位角调整为-45度
            ax.view_init(30, -45)
            plt.show()
        #当簇的中心点发生明显的变化时继续递归k_mean函数
        else:
            gap1=b
            gap2=c
            gap3=d
            return k_mean(b,c,d)
    #运行k_mean函数
    k_mean(b,c,d)

    # 查找某个具体用户所在簇
    for cur in res:
        if 1 in cur:
            # 读取表数据
            query = "SELECT * FROM praise_info WHERE userId IN %s" % str(cur).replace("[", "(").replace("]", ")")
            data_zan = pd.read_sql(query, conn)
            data_zan = data_zan.dropna(axis='index', how='all', subset=['foodsId'])
            foodslist = list(set(data_zan['foodsId'].values.tolist()))
            foodslist = [int(i) for i in foodslist]
            if len(foodslist) > 10:
                foodslist = foodslist[:10]
            else:
                while len(foodslist) < 10:
                    for j in range(1, 11):
                        if j not in foodslist:
                            foodslist.append(int(j))
                        if len(foodslist) == 10:
                            break
                    if len(foodslist) == 10:
                        break
            if len(foodslist) < 10:
                foodslist = ['pizza', 'burger', 'fries', 'salad', 'steak', 'sushi']
            # 输出食品列表
            print(foodslist)
            foodslist = foodslist[::-1]
            random.shuffle(foodslist)
            print(foodslist)
query = "SELECT * FROM praise_info WHERE userId IN %s" % str(cur).replace("[","(").replace("]",")")
data_zan = pd.read_sql(query, conn)
data_zan = data_zan.dropna(axis='index', how='all', subset=['foodsId'])
foodslist = list(set(data_zan['foodsId'].values.tolist()))
foodslist = [int(i) for i in foodslist]
if len(foodslist) > 10:
    foodslist = foodslist[:10]
else:
    while len(foodslist) < 10:
        for j in range(1, 11):
            if j not in foodslist:
                foodslist.append(int(j))
            if len(foodslist) == 10:
                break
        if len(foodslist) == 10:
            break
if len(foodslist) < 10:
    foodslist = ['pizza', 'burger', 'fries', 'salad', 'steak', 'sushi']
# 输出食品列表
foodslist = foodslist[::-1]
random.shuffle(foodslist)
print(foodslist)






