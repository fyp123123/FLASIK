from flask import Flask, request,Response,flash
import json
from damo2 import config
from flask import redirect
from flask import url_for
from flask import render_template
import time
import os


app = Flask(__name__)
app.config['debug']=True
app.config['port']=8080
app.config['SECRET_KEY']=os.urandom(24)
# app.config.from_object(config)
# print(app.config['TOKEN_KEY'])        通过config 文件读取配置文件


@app.route('/')
def hello_world():
    r = request.args.get('p')   #get请求添加参数p
    return r
@app.route('/a')
def hell():
    r=request.args.getlist('p')
    return str(r)
@app.route('/register',methods=['post'])
def register():
    r=request.form.get('name')         #post请求添加参数 form_data格式
    b=request.form.get('paswod')
    return r+b

@app.route('/add',methods=['post'])
def add():
    result={'sum':request.json.get('a')+request.json.get('b')}        #post请求添加JSON格式的参数
    return Response(json.dumps(result),mimetype='application/json')  #设置响应体

@app.route('/user/<username>')
def user(username):
    return "user is "+username

@app.route('/page/<int:num>')        #指定参数int类型，分页控制
def page(num):
    return "当前页是:"+str(num)

@app.route('/blog/list/<any(python,flask,django):type>')  #any类型是指备选中任意一个
def list(type):
    return "选择的类型是：%s"%type

@app.route('/blog/list/<int:use_id>')        #2个视图函数，参数设置默认值，url简洁
@app.route('/blog/list/<int:use_id>/<int:page>')
def blog_list(use_id,page=1):
    return "用户ID为%s,当前页为%s"%(use_id,page)

@app.get('/login')
def login():
    if request.method=='get':
        return "@app.get=@app.rourt('login',methods=['get'])"
    else:
        return "@app.post=@app.rourt('login',methods=['post'])"

@app.route('/profile')
def profie():
    name=request.args.get("name")
    if not name:
        return  redirect('/login',code=302)  #如果name为空就重定向到login页面
    else:
        return name

@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    return "查找的博客ID为：%s"%blog_id
@app.route('/urlfor')
def get_url_for():

    url=url_for('blog_detail',blog_id=2,user='admin')
    return url

@app.route('/varibale')
def varibale():
    game="游戏"
    interest = '打球'
    #参数关联HTML参数
    return render_template('index.html',game=game,interest=interest)

class User:
    def __init__(self,usename,age):
        self.usename=usename
        self.age=age
@app.route('/index')
def index():
    person={"name":"libai",
            "age":20

    }

    user=User("田军",55)

    return  render_template("index.html",person=person,user=user)
    #写法二，用于变量多的情况下 ,推荐用这个
    # context={
    #     "user":user,
    #          "person":person
    #
    # }
    # return render_template("index.html",**context)

@app.route("/if")
def if_statement():
    age = 20
    return render_template('demo.html',age=age)
@app.route('/for')
def for_statement():
    books=[{
        "name":"三国演义",
        "author":"罗贯中",
        "price":100

    },{
        "name":"西游记",
        "author":"吴承恩",
        "price":101
    },{
        "name":"水浒传",
        "author":"施耐庵",
        "price":102
    },{
        "name":"红楼梦",
        "author":"曹雪芹",
        "price":103
    }
    ]
    return  render_template('demo2.html',books=books)

@app.route('/macro')
def macro():
    return render_template('macro.html')
@app.route('/product')
def product():
    return render_template('produ.html')

@app.context_processor   #上下文处理器，可以快速做变量
def get_current_time():
    def get_time(timeFormat="%b %d, %Y - %H:%M:%S"):
         return time.strftime(timeFormat)
    return dict(current_time=get_time)

@app.template_global() #全局函数
def get_global(name):
    return "欢迎回来%s"%name

@app.route("/flash")
def myflash():
    return render_template("flash.html")

@app.route("/logins",methods=['post','get'])
def logins():
    error = None
    # print(request.method)
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            # flash('您已成功登录')
            flash('You were successfully logged in')
            return redirect(url_for('flash'))
    return render_template('login.html', error=error)



if __name__ == '__main__':
    app.run(debug=app.config['debug'],port=app.config['port'])