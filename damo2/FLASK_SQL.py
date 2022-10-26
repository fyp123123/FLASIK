from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

#mysql 所在主机
HOSTNAME = "127.0.0.1"
#mysql 端口号
PORT = "3306"
#链接MySQL的用户名
USERNAME = "root"
#链接数据库的密码
PASSWORD = "123456"
#连接数据库名称
DATABASE = "dbwork_base"

app.config['SQLALCHEMY_DATABASE_URI']=f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
#FLASK-SQLalchemy 在链接数据库时会从app.config中读取SQLAlchemy_database_uri 参数，以上代码
#分别设置了MySQL的主机名，端口号，用户名，密码以及数据库名称，MySQL的连接方式如下：
#MySQL +[driver]://[username]:[password]@[host]:[port]/[database]?charset=utf8,其中【】为变量需要填充

#自动追踪数据库修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

# 调试是否链接成功
# with db.engine.connect() as conn:
#     rs=conn.execute("select * from dbwork")
#     print(rs.fetchall())

#做外键多对多创建中间表，使用Table定义一个中间表，中间表一般就是包含两个模型的外键字段就可以了，并且让它们两个来作为一复合主键。
new_tag=db.Table("new_tag", #中间表名称
                 db.Column("user_id",db.Integer,db.ForeignKey("user.id"),primary_key=True), #需要关联的表字段
                 db.Column("tag_id",db.Integer,db.ForeignKey("tag.tag_id" ),primary_key=True)
              )

class User(db.Model):

    #继承db.Model,通过__tablename__属性映射到数据库中的表名
    __tablename__="user"

    #创建表字段
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,comment="id")
    username=db.Column(db.String(100),comment="用户名")
    password=db.Column(db.String(100),comment="密码")
    articles=db.relationship("Article",back_populates='author')
    tags=db.relationship("tag",back_populates='users',secondary=new_tag)


@app.route('/user/add')
def user_add():
    user=User(username="张三",password="123456")
    user1=User(username="李四",password="654321")
    user2=User(username="王五",password="879111")
    user3=User(username="大王",password="191011")
    db.session.add(user)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    return "用户添加成功"
#使用orm进行CRDU{cerate , read ,delete ,updata}操作，需要先把操作添加到会话中，通过db.session获取会话对象，如果要把会话对象提取到数据库中需要db.session.commit()
#如果要回滚需要用db.session.rollback()

@app.route('/user/updataone')
def user_updataone():
    #更新单条数据
    user=User.query.get(1)
    user.username="张三_修改后"
    db.session.commit()
    return "更新单挑数据成功"
@app.route('/user/updataall')
def user_updataall():
    #更新多条数据
    user=User.query.filter(User.username.like("%张三%")).update({"password":User.password+"_被修改"},synchronize_session=False)
    db.session.commit()
    return "更新多条数据成功"

@app.route('/user/deleteone')
def user_deleteone():
    #删除单条数据
    user=User.query.first()
    db.session.delete(user)
    db.session.commit()
    return "删除单条数据成功"
@app.route('/user/deleteall')
def user_deleteall():
    user=User.query.filter(User.username=="张三").delete(synchronize_session=False)
    db.session.commit()
    return "多条数据删除成功"

@app.route('/user/fetch')
def use_fetch():
    #获取User中所有的数据
     users=User.query.all()
    #获取主键为1的数据
     user=User.query.get(1)
     use=User.query.first()
     # for i in users:
     #     print(i.id,i.username,i.password)
     # return "查询成功"
     for i in use.articles:
         print(i.title)
         return i.title


@app.route('/user/filter')
def user_filter():
    from sqlalchemy import and_ ,or_
    user=User.query.filter_by(username="张三").all()
    users=User.query.filter(User.username.like("%张%")) #模糊查询
    user1=User.query.filter(User.username.in_(["张三","李四"])) #in
    user2=User.query.filter(~User.username.in_(["张三","李四"])) #not in
    user3=User.query.filter(User.username==None) #或者username.is_(None) 判断为None
    user4=User.query.filter(and_(User.username=="张三",User.id==1))
    use5=User.query.filter(or_(User.username=="张三",User.username=="李四"))

    print(user4)
    return "查询过滤后的数据成功"

@app.route('/user/asc')
def user_asc():
    #查询数据升序
    user=User.query.order_by(User.id.asc())
    for i in user:
        print(i.id)
    return "升序查询成功"

@app.route('/user/desc')
def user_desc():
    user=User.query.order_by(User.id.desc())
    for i in user:
        print(i.id)
    return "降序查询成功"

@app.route('/user/group')
def user_group():
    #分组统计
    from sqlalchemy import func
    user=db.session.query(User.username,func.count(User.id)).group_by("username").all()
    print(user)
    return "分组统计"

class Article(db.Model):
    #创建一个新表article,用于关联user表的id,新增外键 ,一对一外键
    __tablename__ = 'article'
    id =db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(10),nullable=False)
    title=db.Column(db.String(10),nullable=False)
    article_id=db.Column(db.Integer,db.ForeignKey(User.id))
    author=db.relationship('User',back_populates='articles')  #relationship里的第一个参数是引号+类,关联User
db.create_all()

@app.route('/article/add')
def article_add():
    use=User.query.first()
    #插入数据
    article=Article(title="aa",name="bb",author=use)
    db.session.add(article)
    db.session.commit()

    article=Article.query.filter_by(title="aa").first()  #查找title=aa的第一条记录
    return article.author.username      #返回通过article_id关联后对应User表里的unsername数据


# 外键多对多的关系需要通过一张中间表来绑定他们之间的关系。
# 先把两个需要做多对多的模型定义出来
# 使用Table定义一个中间表，中间表一般就是包含两个模型的外键字段就可以了，并且让它们两个来作为一复合主键。
# 在两个需要做多对多的模型中随便选择一个模型，定义一个relationship属性，来绑定三者之间的关系，在使用relationship的时候，需要传入一个secondary=中间表对象名。

class tag(db.Model):
    __tablename__ = 'tag'
    tag_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(10),nullable=False)
    #建立多对多关系
    users=db.relationship("User",back_populates='tags',secondary=new_tag)    #在使用relationship的时候，需要传入一个secondary=中间表对象名
db.create_all()

@app.route('/many2many')
def many2many():
    user1=User(username='模拟',password="98111")
    user2=User(username='测试',password="12811")
    tag1=tag(name='tag的名字1')
    tag2=tag(name='tag的名字2')
    user1.tags.append(tag1)
    user1.tags.append(tag2)
    user2.tags.append(tag1)
    user2.tags.append(tag2)
    db.session.add_all([user1,user2])
    db.session.commit()
    return "多对多添加成功"

class Category(db.Model):
    #级联操作
    __tablename__ ='category'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(10))
    # newses=db.relationship('News',back_populates='category')
    #cascade='delete,delete-orphan' 表示某个对象被父表解除关联后此对象会被自动删除
    newses=db.relationship('News',back_populates='category',cascade='delete,delete-orphan',single_parent=True)
    # db.create_all()

class News(db.Model):
    __tablename__='news'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(10))
    content=db.Column(db.Text)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category =db.relationship('Category',back_populates='newses',cascade='save-update')  #cascade='save-update'是默认选项
    # db.create_all()
def create_data():
    categorys=Category(name='军事')
    news=News(title='新闻1',content='新闻类容1')
    news.category=categorys
    db.session.add(news)
    db.session.commit()     #上方cascade='save-update'的作用是当某个对象被添加到会话中，与此对应关联的对应也会被添加到会话中

def delete():
    category=Category.query.first()
    db.session.delete(category)
    db.session.commit()
    return "删除某个对象他对应关联的对象也会被删除"
    # news=News.query.first()
    # db.session.delete(news)
    # db.session.commit()
    # return "删除副表后，主表对应被关联的也会删除"

def remove():
    #将Category表的第一条数据查询出来与News表关联的字段给赋值
    category=Category.query.first()
    news=News(title='新闻二',content='新闻内容2')
    category.newses.append(news)
    # db.session.add(news)
    db.session.commit()
    将news从category中解除关联
    category.newses.remove(news)
    db.session.commit()

if __name__ == '__main__':
    # 通过db.create_all把user模型映射到数据库中的表

    app.run()
    remove()
