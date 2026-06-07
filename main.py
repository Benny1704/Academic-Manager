from services import UserService


# print("---------Register User---------")
# username = input("Enter Username: ")
# email = input("Enter Email: ")
# phone = input("Enter Phone: ")
# password = input("Enter Password: ")
# role = input("Enter Role: ")

# userService = UserService("data/users.json")
# result = userService.register_user(username = username, email = email, phone = phone, password = password, role = role)

print("---------Login User---------")
username = input("Enter Username: ")
email = input("Enter Email: ")
password = input("Enter Password: ")
userService = UserService("data/users.json")
result = userService.login_user(username = username ,email = email, password = password)

print(result)