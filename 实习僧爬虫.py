#!/usr/bin/env python
# coding: utf-8

# ![logo.png](logo.png)

# # <center>《商业数据分析》期末作品报告</center>

# ### 学 院 名 称：<u>   媒体工程学  </u>
# 
# ### 作 品 名 称：<u>前端岗位数据——关联规则</u>
# 
# ### 学       号：<u>190808139</u>
# 
# ### 姓       名：<u>郑林</u>
# 
# ### 班       级：<u>19软件工程1班</u>
# 
# ### 任 课 教 师：<u>     孙煦雪    </u>
# 
# ### 学       期：<u>    2021–2022-2    </u>
# 

# ##   <center>前端岗位数据——关联规则 </center>

# ### 一、作品简介

# 对爬取数据进行关联规则数据分析

# ### 二、作品实现

# In[ ]:


通过现有爬虫知识获取数据，再进行简单数据预处理及分析，最后对数据进行关联规则数据分析。


# ### 三、程序源码

# In[ ]:


import requests
import xlwt
import urllib.parse
from lxml import etree
import re
from fontTools.ttLib import TTFont

font = TTFont("file.ttf")
font.saveXML("font.xml")

def get_dict():
    #打开并读取font.xml
    with open('font.xml') as f:
        xml = f.read()        
    #正则表达式提取code和name
    keys = re.findall('<map code="(0x.*?)" name="uni.*?"/>', xml)
    values = re.findall('<map code="0x.*?" name="uni(.*?)"/>', xml)
    word_dict={}
    # 将name解码成中文并作为值写入字典word_dict，该字典的键为keys
    for i in range(len(values)):
        if len(values[i]) < 4:
            values[i] = ('\\u00' + values[i]).encode('utf-8').decode('unicode_escape')
        else:
            values[i] = ('\\u' + values[i]).encode('utf-8').decode('unicode_escape')
        word_dict[keys[i]]=values[i]
    print(word_dict)
    return word_dict
dict=get_dict()

#输入要爬取的岗位名称并转urlencode编码
job=input('请输入你要在实习僧爬取的实习岗位名称：')
job_urlencode=urllib.parse.quote(job)
def spider_sxs():
    #创建execl并设置列名
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet1 = workbook.add_sheet('{}'.format(job))
    sheet1.write(0,0,'职位名称')
    sheet1.write(0,1,'工资')
    sheet1.write(0,2,'城市')
    sheet1.write(0,3,'出勤要求')
    sheet1.write(0,4,'学历要求')
    sheet1.write(0,5,'实习周期')
    sheet1.write(0,6,'职位福利')
    sheet1.write(0,7,'公司名称')
    sheet1.write(0,8,'所属行业')
    sheet1.write(0,9,'公司规模')
    sheet1.write(0,10,'岗位详细')
    sheet1.write(0,11,'投递链接')
   

    # 设置excel列宽度
    sheet1.col(0).width = 256 * 30
    sheet1.col(1).width = 256 * 20
    sheet1.col(2).width = 256 * 10
    sheet1.col(3).width = 256 * 15
    sheet1.col(4).width = 256 * 15
    sheet1.col(5).width = 256 * 15
    sheet1.col(6).width = 256 * 60
    sheet1.col(7).width = 256 * 20
    sheet1.col(8).width = 256 * 20
    sheet1.col(9).width = 256 * 15
    sheet1.col(10).width = 256 * 150
    sheet1.col(11).width = 256 * 30
  

    sheet1_row=0
    url2 = [] # 跳转岗位详细url
    # 解析网页源代码
    for i in range(1,int(input('请输入要爬取{}岗位的页数：'.format(job)))+ 1):
        url='https://www.shixiseng.com/interns?page={}&type=intern&keyword={}&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend='.format(i,job_urlencode)
        print('第{}页的链接是：{}'.format(i,url))
        response=requests.get(url)
        response_text=response.text.replace('&#','0')       #将源码中&#xefed=>0xefed
        for key in dict:
            response_text=response_text.replace(key,dict[key])      #0xefed格式=>对应的字典的值
        html_sxs=etree.HTML(response_text)
        
        all_div=html_sxs.xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[1]//div[@class="intern-wrap intern-item"]')

        # 循环语句获取数据并存入excel
        for item in all_div:        
            try:
#                 print(0)
                # 获取数据
                job_name = item.xpath('.//a[@class="title ellipsis font"]/text()')[0]        #职位名称
#                 print(job_name)
                wages = item.xpath('.//span[@class="day font"]/text()')[0]      #工资
#                 print(2)
                city = item.xpath('.//span[@class="city ellipsis"]/text()')[0]      #城市
#                 print(3)
                week_time = item.xpath('.//span[@class="font"]/text()')[0]      #出勤要求   
#                 print(4)
                url2.append(item.xpath('.//a[@class="title ellipsis font"]/@href')[0])
#                 print(5)
                work_time = item.xpath('.//span[@class="font"]/text()')[1]      #实习周期
#                 print(6) 此处有个坑，有的公司福利不在这个div中
                job_welfare = item.xpath('.//span[@class="company-label"]/text()')       #职位福利
#                 print( work_time)
                company_name = item.xpath('.//a[@class="title ellipsis"]/text()')[0]       #公司名称
#                 print(8)
                company_type = item.xpath('.//span[@class="ellipsis"]/text()')[0]       #所属行业
#                 print(9)
                company_size = item.xpath('.//span[@class="font"]/text()')[2]       #公司规模
#                 print(10)
                job_href = item.xpath('.//a[@class="title ellipsis font"]/@href')[0]    #投递链接
                # 向execl写入数据
                sheet1_row=sheet1_row+1
                sheet1.write(sheet1_row,0,job_name)
                sheet1.write(sheet1_row,1,wages)
                sheet1.write(sheet1_row,2,city)
                sheet1.write(sheet1_row,3,week_time)          
                sheet1.write(sheet1_row,5,work_time)
                sheet1.write(sheet1_row,6,job_welfare)
                sheet1.write(sheet1_row,7,company_name)
                sheet1.write(sheet1_row,8,company_type)
                sheet1.write(sheet1_row,9,company_size)
                sheet1.write(sheet1_row,11,job_href)               
            except IndexError as e:
                print(e)                
    print( sheet1_row,len(url2))  
    sheet1_row2=0
    for i in url2:
            response2 = requests.get(i)
            response_text2=response2.text.replace('&#','0')       #将源码中&#xefed=>0xefed
            for key2 in dict:
                response_text2=response_text2.replace(key2,dict[key2]) 
            html_sxs2 = etree.HTML(response_text2)  
            job_academic =str( html_sxs2.xpath('.//span[@class="job_academic"]/text()')).replace('[',"").replace('\'','').replace(']',"")   # 学历要求
            job_detail = str(html_sxs2.xpath('.//div[@class="job_detail"]/p/text()')).replace('\'','').replace('\\t','').replace('[',"")             .replace("\\n",'').replace(']',"") #岗位详细
#             job_detail2 = str(html_sxs2.xpath('.//div[@class="job_detail"]/strong/text()')).replace('\'','').replace('\\t','').replace('[',"") \
#             .replace("\\n",'').replace(']',"") #岗位详细
#             job_detail=job_detail1+job_detail2
            sheet1_row2=sheet1_row2+1
            sheet1.write(sheet1_row2,4,job_academic)
            sheet1.write(sheet1_row2,10,job_detail)            
    print( sheet1_row,len(url2))
    workbook.save('实习僧{}岗位.xls'.format(job))  
    print('爬取成功')
    print('------------------------------------------------------')
spider_sxs()


# In[41]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import warnings
warnings.filterwarnings('ignore')
data = pd.read_excel('实习僧前端岗位.xls')  
data.head()


# In[42]:


data.info()
#岗位详细中有几处是连续为空值的


# In[43]:


# 用前一个非缺失值去填充该缺失值
df=data.fillna(method='ffill')
df.info()


# In[44]:


df.公司规模.value_counts()


# In[45]:


df.所属行业.value_counts()


# In[9]:


df.学历要求.value_counts()


# In[46]:


# 该列数据需转换为数值，转换规则为取中间数
def trans_money(x):
    try:
        x1 = re.split('-|/',x)[0]
        x2 = re.split('-|/',x)[1]
        x3 = (int(x1)+int(x2))/2
    except:
        x3 = x
    return x3
# 工资为薪资面议的，默认改为100/天
df['工资'] = df.工资.map(lambda x : x.replace('/天',"").replace("薪资面议","100"))
df['工资'] = df['工资'].map(trans_money)


#
# day_salary中有 面议 ，将面议填充为均值

print(df['工资'].value_counts())


# In[47]:


df.info()
print(df.实习周期.value_counts())


# In[21]:


print(df.出勤要求.value_counts())


# In[27]:


plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams["axes.unicode_minus"]=False
fig = plt.figure(figsize=(20,10))
plt.bar(df.城市.unique(),df.城市.value_counts(),color='g')
plt.title('岗位所在城市条形图',color = 'yellow')
plt.xticks(color = 'yellow')
plt.yticks(color = 'yellow')
print(df.城市.value_counts())


# In[48]:


plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams["axes.unicode_minus"]=False
fig = plt.figure(figsize=(8,6))
# reindex对行顺序重新排序
df.groupby('公司规模')['公司规模'].count().reindex(['少于15人','15-50人','50-150人','150-500人','500-2000人','2000人以上']).plot.bar()
plt.ylabel('数目',fontsize=18)
plt.xlabel('公司规模 ',fontsize=18)
plt.tick_params(labelsize=12,rotation=0)


# In[24]:


# 不同行业对于前端实习生的需求

fig = plt.figure(figsize=(10,8))
df.groupby('所属行业')['所属行业'].count().plot.bar()
plt.ylabel('数目',fontsize=18)
plt.xlabel('所属行业',fontsize=18)
plt.tick_params(labelsize=12)

# 分析
# 互联网对前端岗位需求最大，金融、咨询随后


# In[25]:


# 各实习岗位对于实习生的基本要求：

fig = plt.figure(figsize=(15,5))
plt.ylabel('数目',fontsize=18)

plt.subplot(131)
data.groupby('出勤要求')['出勤要求'].count().plot.bar()
plt.ylabel('数目',fontsize=18)
plt.xlabel('出勤要求',fontsize=18)
plt.tick_params(labelsize=12)

plt.subplot(132)
data.groupby('实习周期')['实习周期'].count().plot.bar()
plt.xlabel('实习周期',fontsize=18)
plt.tick_params(labelsize=12)

plt.subplot(133)
data.groupby('学历要求')['学历要求'].count().plot.bar()
plt.xlabel('学历要求',fontsize=18)
plt.tick_params(labelsize=12)

plt.tight_layout()

# 分析
# 每周3-5天，至少实习3个月，本科学历是许多岗位的基本要求


# In[49]:


# 各地前端实习生的日薪（数据量太少不具有统计性，剔除数据量过少的地区）

# 将工资转变为int类型
df['工资'] = df['工资'].apply(int)

# 剔除数据量过少的地区
temp0 = df.groupby(['城市'])['城市'].count()
position = list(temp0[temp0>10].index)
temp = df[df['城市'].isin(position)].groupby(['城市'])['工资'].mean().apply(int)

fig = plt.figure(figsize=(8,6))
temp.plot.bar()
for i in range(len(list(temp))):
    v = int(list(temp)[i])
    plt.text(i,v+1,v,ha='center',fontsize=15)
plt.xlabel('城市',fontsize=18)
plt.ylabel('工资',fontsize=18)
plt.tick_params(labelsize=12,rotation=0)

# 绘制一条工资平均线
avg = int(df[df['城市'].isin(position)].工资.mean())
print(avg)
plt.axhline(y=avg,ls=":",c="k")
avg_line = plt.text(5.55,avg-1,'avg=211',fontsize=20)

# 分析
# 各地区薪酬大致相同，平均日薪211元，其中广州稍低，北京稍高


# In[50]:


#工资的转变
def changeText(x):
    if x <= 150:
        return '低'
    elif x >150 and x <=250:
        return '一般'
    else: 
        return '高'
df['工资'] = df['工资'].map(changeText)
print(df.工资.value_counts())


# In[14]:





# In[17]:


# '城市', '学历要求'和前端实习岗位的工资的关联
from efficient_apriori import apriori
df2 = df[['工资', '城市', '学历要求']]
#删除缺失值的行
df2 = df2.dropna(how='any')
apriori_data = []
#iterrows()方法就是遍历数据框，并且返回索引和带着表头的数据行内容。
for _, (salary,city,edu_back) in df2.iterrows():
    apriori_data.append((salary,city,edu_back))
#利用aprori算法进行频繁算法
itemsets1, rules1 = apriori(apriori_data, min_support=0.005,  min_confidence=0.3)
itemsets1
# 可以看出学历越高，越是在一线城市前端实习生的薪资越高


# In[51]:


# 将出勤要求和实习时间"合并"，按一个月30天，每个月四个周粗略计算
df['出勤要求'] = df.出勤要求.map(lambda x : int(x.replace('天/周',"")))
df['实习周期'] = df.实习周期.map(lambda x : int(x.replace('个月',"")))
df['time'] = df['出勤要求'] * 4 * df['实习周期']


# In[53]:


df['time'] = df.time.map(lambda x : str(x))


# In[55]:


# 实习时长，'城市', '学历要求'和前端实习岗位的工资的关联
df3 = df[['工资', '城市', '学历要求','time']]
#删除缺失值的行
df3 = df3.dropna(how='any')
apriori_data1 = []
#iterrows()方法就是遍历数据框，并且返回索引和带着表头的数据行内容。
for _, (salary,city,edu_back,time) in df3.iterrows():
    apriori_data1.append((salary,city,edu_back,time))
#利用aprori算法进行频繁算法
itemsets2, rules2 = apriori(apriori_data1, min_support=0.005,  min_confidence=0.3)
rules2


# In[56]:


# 在开头加上from __future__ import print_function这句之后，
# 即使在python2.X，使用print就得像python3.X那样加括号使用。
# python2.X中print不需要括号，而在python3.X中则需要。
from __future__ import print_function
import pandas as pd

#自定义连接函数，用于实现L_{k-1}到C_k的连接
def connect_string(x, ms):
#     sorted可以对所有可迭代类型进行排序，并且返回新的已排序的列表。
  x = list(map(lambda i:sorted(i.split(ms)), x))
  l = len(x[0])
  r = []
  for i in range(len(x)):
    for j in range(i,len(x)):
      if x[i][:l-1] == x[j][:l-1] and x[i][l-1] != x[j][l-1]:
        r.append(x[i][:l-1]+sorted([x[j][l-1],x[i][l-1]]))
  return r

#寻找关联规则的函数
def find_rule(d, support, confidence, ms = u'--'):
  result = pd.DataFrame(index=['support', 'confidence']) #定义输出结果
  
  support_series = 1.0*d.sum()/len(d) #支持度序列
  column = list(support_series[support_series > support].index) #初步根据支持度筛选
  k = 0
  
  while len(column) > 1:
    k = k+1
    print(u'\n正在进行第%s次搜索...' %k)
    column = connect_string(column, ms)
    print(u'数目：%s...' %len(column))
    sf = lambda i: d[i].prod(axis=1, numeric_only = True) #新一批支持度的计算函数
    
    #创建连接数据，这一步耗时、耗内存最严重。当数据集较大时，可以考虑并行运算优化。
    d_2 = pd.DataFrame(list(map(sf,column)), index = [ms.join(i) for i in column]).T
    
    support_series_2 = 1.0*d_2[[ms.join(i) for i in column]].sum()/len(d) #计算连接后的支持度
    column = list(support_series_2[support_series_2 > support].index) #新一轮支持度筛选
    support_series = support_series.append(support_series_2)
    column2 = []
    
    for i in column: #遍历可能的推理，如{A,B,C}究竟是A+B-->C还是B+C-->A还是C+A-->B？
      i = i.split(ms)
      for j in range(len(i)):
        column2.append(i[:j]+i[j+1:]+i[j:j+1])
    
    cofidence_series = pd.Series(index=[ms.join(i) for i in column2]) #定义置信度序列
 
    for i in column2: #计算置信度序列
      cofidence_series[ms.join(i)] = support_series[ms.join(sorted(i))]/support_series[ms.join(i[:len(i)-1])]
    
    for i in cofidence_series[cofidence_series > confidence].index: #置信度筛选
      result[i] = 0.0
      result[i]['confidence'] = cofidence_series[i]
      result[i]['support'] = support_series[ms.join(sorted(i.split(ms)))]
  
  result = result.T.sort_values(['confidence','support'], ascending = False) #结果整理，输出
  print(u'\n结果为：')
  print(result)
  
  return result


# In[57]:


from __future__ import print_function
import pandas as pd
import time #导入时间库用来计算用时

data = df[['工资', '城市', '学历要求','time']]

start = time.process_time() #计时开始
print(u'\n转换原始数据至0-1矩阵...')
ct = lambda x : pd.Series(1, index = x[pd.notnull(x)]) #转换0-1矩阵的过渡函数
b = map(ct, data.values) #用map方式执行
b=list(b)
data = pd.DataFrame(b).fillna(0) #实现矩阵转换，空值用0填充
end = time.process_time() #计时结束
print(u'\n转换完毕，用时：%0.2f秒' %(end-start))
del b #删除中间变量b，节省内存


support = 0.005 #最小支持度
confidence = 0.3 #最小置信度
ms = '---' #连接符，默认'--'，用来区分不同元素，如A--B。需要保证原始表格中不含有该字符

start = time.process_time() #计时开始
print('\n开始搜索关联规则...')
find_rule(data, support, confidence, ms)
end = time.process_time() #计时结束
print('\n搜索完成，用时：%0.2f秒' %(end-start))


# ### 四、结果分析和解释

# 前端实习生的招聘需求主要来源于一线、准一线城市北上广深杭州成都等地；招聘公司多属于互联网、金融、咨询等行业；招聘公司规模普遍较大；
# 众多岗位的基本要求是每周工作3 - 5天，至少实习3个月，拥有本科及以上学历；北上广深杭州成都等地的岗位薪酬相差不大，在平均薪酬211元/天上下浮动。
# 

# ### 五、总结

# 通过以后结果分析，可以看出前端岗位也是一个很卷且俩极分化严重的工作，尽量提高学历和技能储备向一线城市发展。
