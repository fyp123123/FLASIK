from damo2.FLASK_SQL import User

user=User.query.all()
print(user)
users=User.query.get(1)
print(users.id)
print("qqq")