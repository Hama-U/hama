import pandas as pd     #pandaの導入, コマンドラインで%pip3 install pandasと打つ

dataset_test = pd.read_csv("test.csv")   #detasetという変数にtestdataを読み込む
#dataset_fx = pd.read_csv("testdata.csv")  #多分日本語が入ってるからエラーはく

print(dataset_test)      #読み込めたか出力してみる
#print(dataset_fx)

