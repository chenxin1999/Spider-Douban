from flask import Flask, url_for, render_template, request, redirect
from datetime import timedelta
from scripts.getComment import writeData
from scripts.showInCloud import setWordCloud, sentimentClassify

app = Flask(__name__)
# 配置
app.config['DEBUG'] = True
# 修改浏览器最大缓存时间，使页面可以实时刷新 参考：https://cuiqingcai.com/5984.html
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.route('/', methods=['POST', 'GET'])
def hello(wordlist=None):
    if request.method == 'POST':
        subject = request.form['subject']
        writeData(subject)
        setWordCloud()
        sentimentClassify()
        print(wordlist)
        return render_template('test.html')

    elif request.method == 'GET':
        return render_template('test.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
