def getresult():
    rules = ["S := abc|aSBC", "bC := bc", "CB := BC"]
    print(rules)

print(getresult())

print("Эта грамматика - контекстно-зависимая")