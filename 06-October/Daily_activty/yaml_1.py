import yaml

config={
    "model":"Random_forest",
    "params":{
        "n_estimators":100,
        "max_depth":5
    },
    "dataset":"student.csv"
}
with open("config.yaml",'w') as f:
    yaml.dump(config,f)

with open("config.yaml",'r') as f:
    data=yaml.safe_load(f)

print(data)
print(data["params"]["n_estimators"])