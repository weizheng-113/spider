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

    # 将当前城市的dataframe追加到总的dataframe中
    all_data = pd.concat([all_data, df], ignore_index=True)

# 计算每个城市的平均租金
average_rent = all_data.groupby('city')['price'].mean().reset_index()

# 生活质量指数
quality_of_life_index = {
    '北京': 115.59,
    '上海': 118.72,
    '广州': 127.11,
    '深圳': 147.55,
    '郑州': 108.39
}

# 将生活质量指数添加到平均租金的DataFrame中
average_rent['quality_of_life_index'] = average_rent['city'].map(quality_of_life_index)
average_rent['ratio'] = average_rent['price'] / average_rent['quality_of_life_index']

# 绘制生活质量指数图
plt.figure(figsize=(10, 6))
sns.barplot(x='city', y='quality_of_life_index', data=average_rent)
plt.title('各城市生活质量指数')
plt.ylabel('生活质量指数')
plt.xlabel('城市')
plt.savefig('各城市生活质量指数.png')  # 保存图表
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='quality_of_life_index', y='price', data=average_rent, hue='city', s=100)
plt.title('各城市平均租金与生活质量指数的关系')
plt.xlabel('生活质量指数')
plt.ylabel('平均租金 (元)')
plt.grid(True)
plt.savefig('各城市平均租金与生活质量指数的关系_scatter.png')  # 保存图表
plt.show()


plt.figure(figsize=(10, 6))
sns.scatterplot(x='quality_of_life_index', y='price', size='ratio', sizes=(50, 300), hue='city', data=average_rent)
plt.title('各城市平均租金与生活质量指数的关系（气泡图）')
plt.xlabel('生活质量指数')
plt.ylabel('平均租金 (元)')
plt.grid(True)
plt.savefig('各城市平均租金与生活质量指数的关系_bubble.png')  # 保存图表
plt.show()

# 绘制平均租金与生活质量指数的比值图
plt.figure(figsize=(10, 6))
sns.barplot(x='city', y='ratio', data=average_rent)
plt.title('各城市平均租金与生活质量指数的比值')
plt.ylabel('平均租金/生活质量指数')
plt.xlabel('城市')
plt.savefig('各城市平均租金与生活质量指数的比值.png')  # 保存图表
plt.show()

# 输出统计数据
print("各城市平均租金及生活质量指数:")
print(average_rent[['city', 'price', 'quality_of_life_index', 'ratio']])