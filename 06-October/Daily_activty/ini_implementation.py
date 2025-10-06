import configparser

config = configparser.ConfigParser()

config["database"]={
    "host":"localhost",
    "user":"root",
    "password":"1234",
    "port":"3306"
}

with open("app.ini","w") as configfile:
    config.write(configfile)

config.read("app.ini")
print(config["database"]["host"])
