# Spider-Douban
Python 2018 课程大作业，根据电影 id 爬取特定豆瓣电影的评论，并调用百度 AI 开放平台 api 对评论进行简单的情感分析。

## 目录

[TOC]

## 前言

### 背景与目的

豆瓣是国内权威的评论网站，通过分析豆瓣中热门的用户评论，可对当前热门的影视、书籍内容与社会风潮得到概略的了解。本例尝试使用 request， beautifulSoup 库获取豆瓣网友对某一部电影的评论，并调用百度 AI 情感分析 API， 对爬取的评论进行情感分析，以获取对某一部影视作品大众的理解与看法。

### 不足与问题

目前该项目功能过于简单，基本通过调库实现，缺乏自定义的分析过程。项目缺乏异常处理机制，部分运行时异常(如部分爬取到的 GBK 编码内容重编码为 UTF-8 时带来的运行时错误)抛出后没有做处理。交互界面比较简易，大部分内容以静态页面的方式显示，未使用数据库故缺乏本地持久化。处理耗时操作时采用阻塞形式，没有实现多线程。

### 数据来源

https://movie.douban.com/



## 项目介绍

### 生成结果

评论列表与词云：

![屏幕快照 2019-03-29 下午7.35.23](https://ws4.sinaimg.cn/large/006tKfTcly1g1jwe70mqlj31c00u0e81.jpg)

评论列表情绪分析：

![屏幕快照 2019-03-29 下午7.35.43](https://ws3.sinaimg.cn/large/006tKfTcly1g1jwe7oxmhj31c00u07q8.jpg)

### to-do

使用 RASA_NLU 训练对话模型



### 本地部署

```shell
$ git clone https://github.com/ShiroCheng/Spider-Douban.git
$ cd Spider-Douban
$ pip install -r requirements.txt
$ cd app
$ python app.py		//浏览器访问对应端口
```

### 项目结构

```
.								
├── app							
│   ├── app.py					    //项目入口文件
│   ├── scripts					    //脚本目录
│   │   ├── getComment.py		    //获取数据脚本
│   │   └── showInCloud.py		    //处理数据脚本
│   ├── static					    //静态目录
│   │   ├── css				
│   │   │   └── style.css		    //全局样式
│   │   ├── img					    //图片目录
│   │   │   └── result.jpg          //(运行时生成)
│   │   └── text				    //数据存储目录
│   │       ├── Comments.txt        //(运行时生成)
│   │       ├── NlpResult.txt       //(运行时生成)
│   │       └── showComments.txt    //(运行时生成)
│   └── templates				    //模板
│       └── test.html
├── README.md
└── requirements.txt			    //依赖列表

```

### 技术栈

#### 依赖库

- `Flask` python 简易 web 框架
- `beautifulsoup4` 解析 html 内容：
- `baidu_aip` 调用百度 ai 开放平台的情绪分析 api
- `jieba` 对爬取内容分词
- `wordcloud` 基于词语生成词云
- `Materialize` 开源 MaterialDesign 风格的前端组件库
- `jquery` 操纵页面元素，实现视觉效果

#### WebServer 

基于 Flask，配置对不同路由访问时的相应，当写入表单内容时(处理 `POST` 方法)，通过全局的访问参数 `request.form['key']`获取对应表单的值，并在路由方法中调用不同的 python 脚本。

```python
@app.route('/', methods=['POST', 'GET'])
def hello(wordlist=None):
    if request.method == 'POST':			#表单提交，线程阻塞
        subject = request.form['subject']	#获取表单数据
        writeData(subject)					#爬取评论
        setWordCloud()						#设置词云
        sentimentClassify()					#情感分析
        print(wordlist)				
        return render_template('test.html')	#渲染页面

    elif request.method == 'GET':
        return render_template('test.html')
```
#### 评论爬取

基于` request ` 及 ` beautifulsoup `库爬取并解析 html 内容，并将结果写入到文件中，比较简单


#### 评论处理

调用 `jieba`对评论进行分词，并调用 `wordcloud`将分词的结果显示为词云。

注册并免费申请后，调用百度 ai 开放平台 api 完成对评论的情感分析：

```python
# 百度AI开放平台 api
APP_ID = "xxxxxxx"
API_KEY = "xxxxxxx"
SECURITY_KEY = "xxxxxxx"
client = AipNlp(APP_ID, API_KEY, SECURITY_KEY)

text = "这一季里有一集bernadett下班躲在playhouse里，Howard其实从头到尾都知道这段很是感动" #示例
    
result = client.sentimentClassify(text)
```

返回结果示例：

```json
{
    "log_id": 6149225674455447000, 
    "text": "这一季里有一集bernadett下班躲在playhouse里，Howard其实从头到尾都知道这段很是感动", 
    "items": [
        {
            "positive_prob": 0.860074, 
            "confidence": 0.689054, 
            "negative_prob": 0.139926, 
            "sentiment": 2
        }
    ]
}
```



