import os
from datetime import datetime

if __name__=="__main__":
    command=[
        "python ./cnnafricaNews.py",
        "python ./cnnamericasNews.py",
        "python ./cnnasiaNews.py",
        "python ./cnnaustraliaNews.py",
        "python ./cnneuropeNews.py",
        "python ./cnnmiddleeastNews.py",
        "python ./cnnukNews.py",
        "python ./cnnusNews.py",
        "python ./financeNews.py",
        "python ./epochtimes.py",
        "python ./bbcchineseNews.py",
        "python ./chinadailyNews.py",
        "python ./voachineseNews.py",
        "python ./yahooUS.py",
        "python ./51CTONews.py"
    ]

    runStripts=[]
    noRun=[]

    for i in command:
        print(i[9:-3]+" started")
        try:
            os.system(i)
            runStripts.append(i[9:-3])
        except ConnectionError:
            print(i+" failed")
            noRun.append(i[9:-3])
            pass

    print("====================================")
    print(str(datetime.now().date())+" total %d have ran successfully. They are:"%len(runStripts))
    print(runStripts)
    print( "%d have failed to download."%len(noRun))


