import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置matplotlib字体以正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# Pandas选项设置，以便更好地查看数据
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.width', None)  # 设置为自动调整宽度

# 定义文件路径和对应的城市名称
files = {
    'bj.csv': '北京',
    'sh.csv': '上海',
    'gz.csv': '广州',
    'sz.csv': '深圳',
    'zz.csv': '郑州'
}

# 创建一个空的DataFrame用于存储所有数据
all_data = pd.DataFrame()

# 遍历每个csv文件并读取内容到DataFrame中
for file, city in files.items():
    df = pd.read_csv(f'D:\\rentSpider\\rentSpider\\{file}')
    df['city'] = city  # 添加城市列

    # 清理和转换数据
    df['price'] = df['price'].astype(float)  # 转换为浮点数
    df['bedroom'] = df['types'].apply(lambda x: int(x.split('室')[0]))  # 提取室数（1室、2室、3室）

    # 将当前城市的dataframe追加到总的dataframe中
    all_data = pd.concat([all_data, df], ignore_index=True)

# 选择一居、二居、三居的数据
filtered_data = all_data[all_data['bedroom'].isin([1, 2, 3])]

# 计算各类统计数据
summary = filtered_data.groupby(['city', 'bedroom']).agg(
    avg_price=('price', 'mean'),
    max_price=('price', 'max'),
    min_price=('price', 'min'),
    median_price=('price', 'median')
).reset_index()

# 输出统计数据
print("各城市各户型租金统计信息:")
print(summary)

# ---- 绘制均价比较图 ----
plt.figure(figsize=(10, 6))
sns.barplot(x='city', y='avg_price', hue='bedroom', data=summary)
plt.title('各城市各户型均价比较')
plt.ylabel('均价 (元)')
plt.xlabel('城市')
plt.savefig('各城市各户型均价比较.png')  # 保存图表
plt.show()

# ---- 绘制最大值比较图 ----
plt.figure(figsize=(10, 6))
sns.barplot(x='city', y='max_price', hue='bedroom', data=summary)
plt.title('各城市各户型最大租金比较')
plt.ylabel('最大租金 (元)')
plt.xlabel('城市')
plt.savefig('各城市各户型最大租金比较.png')  # 保存图表
plt.show()

# ---- 绘制最小值比较图 ----
plt.figure(figsize=(10, 6))
sns.barplot(x='city', y='min_price', hue='bedroom', data=summary)
plt.title('各城市各户型最小租金比较')
plt.ylabel('最小租金 (元)')
plt.xlabel('城市')
plt.savefig('各城市各户型最小租金比较.png')  # 保存图表
plt.show()

# ---- 绘制中位数比较图 ----
plt.figure(figsize=(10, 6))
sns.barplot(x='city', y='median_price', hue='bedroom', data=summary)
plt.title('各城市各户型中位数租金比较')
plt.ylabel('中位数租金 (元)')
plt.xlabel('城市')
plt.savefig('各城市各户型中位数租金比较.png')  # 保存图表
plt.show()

# ---- 绘制租金箱型图 ----
plt.figure(figsize=(12, 6))
sns.boxplot(x='city', y='price', hue='bedroom', data=filtered_data)
plt.title('各城市各户型租金分布')
plt.ylabel('租金 (元)')
plt.xlabel('城市')
plt.savefig('各城市各户型租金分布_boxplot.png')  # 保存图表
plt.show()

# ---- 绘制小提琴图展示租金分布 ----
plt.figure(figsize=(12, 6))
sns.violinplot(x='city', y='price', hue='bedroom', data=filtered_data, split=True)
plt.title('各城市各户型租金分布')
plt.ylabel('租金 (元)')
plt.xlabel('城市')
plt.savefig('各城市各户型租金分布_violin.png')  # 保存图表
plt.show()

# 计算并展示中位数
median_data = filtered_data.groupby(['city', 'bedroom'])['price'].median().reset_index()
print("各城市各户型中位数租金:")
print(median_data)