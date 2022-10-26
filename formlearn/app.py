from flask import Flask , request ,render_template ,flash ,redirect ,url_for
from forms import RegisterForm

app=Flask(__name__)
app.secret_key='abcde'

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='GET':
        return  render_template('register.html')
    else:
        # request.form 是表单提交上来的数据
        form=RegisterForm(request.form)
        # 如果通过
        if form.validate():
            email=form.email.data
            username=form.username.data
            password=form.password.data
            confirm_password=form.confirm_password.data
            print("email:",email)
            print("username:",username)
            print("password:",password)
            print('confirm_password:',confirm_password)
            return "注册成功"
        else:
            print(form.errors)
            #取错误信息
            for errors in form.errors.values():
                print(errors)
                for error in errors:
                    #通过flash函数闪现消息
                    flash(error)
            #重定向到register页面
            return redirect(url_for("register"))








if __name__ == '__main__':
    app.run(debug=True)
    register()
