import pandas as pd

# 读取数据
weather = pd.read_csv("weather.csv", index_col=0)

# 探索数据
print(weather.head())
print(weather.info())

# 删除与预测无关的特征
weather.drop(["Date", "Location"],inplace=True, axis=1)

# 删除缺失值
weather.dropna(inplace=True)

# 重置索引
weather.index = range(len(weather))
print(weather.info())

# 随机抽样，重置索引
weather_sample = weather.sample(10000)
weather_sample.index = range(len(weather_sample))

# 1.WindGustDir WindDir9am WindDir3pm 属于定性数据中的无序数据——OneHotEncoder
# 2.Cloud9am Cloud3pm  属于定性数据中的有序数据——OrdinalEncoder
# 3.RainTomorrow 属于标签变量——LabelEncoder

# 为了简便起见，WindGustDir WindDir9am WindDir3pm 三个风向中只保留第一个
weather_sample.drop(["WindDir9am", "WindDir3pm"], inplace=True, axis=1)
print(weather_sample.info()

# 编码分类变量
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,LabelEncoder

print(np.unique(weather_sample["RainTomorrow"]))
print(np.unique(weather_sample["WindGustDir"]))
print(np.unique(weather_sample["Cloud9am"]))
print(np.unique(weather_sample["Cloud3pm"]))

# 查看样本不均衡问题
print(weather_sample["RainTomorrow"].value_counts())

# 编码标签
weather_sample["RainTomorrow"] = pd.DataFrame(LabelEncoder().fit_transform(weather_sample["RainTomorrow"]))

# 编码Cloud9am Cloud3pm
oe = OrdinalEncoder().fit(weather_sample["Cloud9am"].values.reshape(-1, 1))

weather_sample["Cloud9am"] = pd.DataFrame(oe.transform(weather_sample["Cloud9am"].values.reshape(-1, 1)))
weather_sample["Cloud3pm"] = pd.DataFrame(oe.transform(weather_sample["Cloud3pm"].values.reshape(-1, 1)))

# 编码WindGustDir
ohe = OneHotEncoder(sparse=False)
ohe.fit(weather_sample["WindGustDir"].values.reshape(-1, 1))
WindGustDir_df = pd.DataFrame(ohe.transform(weather_sample["WindGustDir"].values.reshape(-1, 1)), columns=ohe.get_feature_names())

# 合并数据
weather_sample_new = pd.concat([weather_sample,WindGustDir_df],axis=1)
weather_sample_new.drop(["WindGustDir"], inplace=True, axis=1)
print(weather_sample_new)

# 调整列顺序
Cloud9am = weather_sample_new.iloc[:,12]
Cloud3pm = weather_sample_new.iloc[:,13]

weather_sample_new.drop(["Cloud9am"], inplace=True, axis=1)
weather_sample_new.drop(["Cloud3pm"], inplace=True, axis=1)

weather_sample_new["Cloud9am"] = Cloud9am
weather_sample_new["Cloud3pm"] = Cloud3pm

RainTomorrow = weather_sample_new["RainTomorrow"]
weather_sample_new.drop(["RainTomorrow"], inplace=True, axis=1)
weather_sample_new["RainTomorrow"] = RainTomorrow

print(weather_sample_new.head())

# 处理异常值
weather_sample_new.describe([0.01,0.99])

# 对数值型变量和分类变量进行切片
weather_sample_mv = weather_sample_new.iloc[:,0:14]
weather_sample_cv = weather_sample_new.iloc[:,14:33]

# 盖帽法处理数值型变量的异常值
def cap(df,quantile=[0.01,0.99]):
    for col in df:
        # 生成分位数
        Q01,Q99 = df[col].quantile(quantile).values.tolist()
        
        # 替换异常值为指定的分位数
        if Q01 > df[col].min():
            df.loc[df[col] < Q01, col] = Q01
        
        if Q99 < df[col].max():
            df.loc[df[col] > Q99, col] = Q99
        

cap(weather_sample_mv)
weather_sample_mv.describe([0.01,0.99])


# 数据归一化
from sklearn.preprocessing import StandardScaler

weather_sample_mv = pd.DataFrame(StandardScaler().fit_transform(weather_sample_mv))
weather_sample_mv

# 重新合并数据
weather_sample = pd.concat([weather_sample_mv, weather_sample_cv], axis=1)
print(weather_sample.head())

# 划分特征与标签
X = weather_sample.iloc[:,:-1]
y = weather_sample.iloc[:,-1]

from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score, recall_score

# 寻找最好的核函数
for kernel in ["linear","poly","rbf"]:
    accuracy = cross_val_score(SVC(kernel=kernel), X, y, cv=5, scoring="accuracy").mean()
    print("{}:{}".format(kernel,accuracy))















