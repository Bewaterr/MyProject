# 泰坦尼克号幸存者预测

import pandas as pd 
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt


# 导入并探索数据
data = pd.read_csv("Taitanic_data.csv")
print(data.head())
print(data.info())

"""
PassengerId => 乘客ID
Pclass => 乘客等级(1/2/3等舱位)
Name => 乘客姓名
Sex => 性别
Age => 年龄
SibSp => 堂兄弟/妹个数
Parch => 父母与小孩个数
Ticket => 船票信息
Fare => 票价
Cabin => 客舱
Embarked => 登船港口
"""


# 删除缺失值过多的列，以及和预测的y没有关系的列
data.drop(["Cabin", "Name", "Ticket"], inplace=True, axis=1)

# 处理缺失值，对于缺失较多的列进行填补，对于缺失较少的列可以直接删除该条记录
data["Age"] = data["Age"].fillna(data["Age"].mean())
data = data.dropna()

# 删除缺失值后重置索引
data.index = range(len(data))
print(data.tail())
print(data.info())

"""
在说分类变量转数值型变量之前，我们首先要清楚数据的类型
数据可以分为定量数据和定性数据，定性数据又可以分为有序数据和无序数据，定量数据可以分为离散型数据和连续型数据
这个项目中我们要处理的数据是Sex和Embarked，前者属于定性数据中的无序数据，后者属于定性数据中的有序数据
在sklearn中可以进行变量转换的类有三个：OneHotEncoder\OrdinalEncoder\LableEncoder
三者的区别在于：
1.OneHotEncoder用于编码无序数据（针对特征）
2.OrdinalEncoder用于编码有序数据（针对特征），可以保留数据的大小意义
3.LableEncoder用于编码标签变量，不会保留数据的大小意义
"""

#将分类变量转换为数值型变量
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder

# 编码Sex
ohe = OneHotEncoder(sparse=False)
data_Sex = ohe.fit_transform(data["Sex"].values.reshape(-1, 1))

# 查看编码后对应的特征名称并转换为DataFrame
ohe.get_feature_names()
data_Sex_df = pd.DataFrame(data_Sex, columns=["female","male"])

# 编码Embarked并转换为DataFrame
oe = OrdinalEncoder()
data_Embarked = oe.fit_transform(data["Embarked"].values.reshape(-1, 1))
data_Embarked_df = pd.DataFrame(data_Embarked, columns=["Embarked"])

# 删除Sex和Embarked
data.drop(["Sex", "Embarked"], inplace=True, axis=1)

# 将编码后的数据合并到原数据
newdata = pd.concat([data, data_Sex_df, data_Embarked_df], axis=1)
print(newdata)

# 划分特征与标签
X = newdata.iloc[:, newdata.columns != "Survived"]
y = newdata.iloc[:,newdata.columns == "Survived"]

# 划分训练集与测试集
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,y)

# 实例化模型
clf = DecisionTreeClassifier(random_state=666)

# 交叉验证得到最佳折数
cv_score = []
for i in range(2,10):
    score = cross_val_score(clf,X,y,cv=i).mean()
    cv_score.append(score)

best_cv = cv_score.index(max(cv_score)) + 2

# 网格搜索寻找最佳超参数
parameters = {"splitter":('best','random')
              ,"max_depth":[*range(1,5)]
              ,"min_samples_leaf":[*range(1,10)]
             }

clf = DecisionTreeClassifier(random_state=666)
GS = GridSearchCV(clf, parameters, cv=best_cv)
GS.fit(Xtrain,Ytrain)

print(GS.best_score_)
print(GS.best_params_)