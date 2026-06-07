from services import UserService


print("---------Register User---------")
username = input("Enter Username: ")
email = input("Enter Email: ")
phone = input("Enter Phone: ")
password = input("Enter Password: ")
role = input("Enter Role: ")

userService = UserService("data/users.json")
result = userService.register_user(username,email,phone,password,role)

print(result)