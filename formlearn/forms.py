#用于做前端页面做校验

from wtforms import Form ,StringField
from wtforms.validators import length,email,equal_to

registed_email=['aa@example.com','bb@example.com']

class RegisterForm(Form):
    username=StringField(validators=[length(min=3,max=10,message='请输入正确长度的用户名！')])
    email=StringField(validators=[email(message='请输入正确格式')])
    password=StringField(validators=[length(min=6, max=20, message="请输入正确长度的密码！")])
    confirm_password=StringField(validators=[equal_to('password',message="两次密码不一致！")])
    #变量名必须要和HTML name名字一致
   #必须继承Form 基类 ,validators是个验证器集合，email可以用于校验是否满足邮箱格式，equal_to 是判断是否和另一个值相等

    #对邮箱进行校验
    def validate_email(self,field):
        email=field.data
        if email in registed_email:
           #如果email在列表里抛异常
            raise Exception("你已经注册过邮箱号")
        return True


