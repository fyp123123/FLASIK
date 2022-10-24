from jinja2 import Template

# name=input("Enter your name: ")
name="pater"
age=34
tm=Template("name is {{name}} and age is {{age}}")
msg=tm.render(name=name,age=age)
print(msg)