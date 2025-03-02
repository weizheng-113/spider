import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取5个城市的租房数据文件
files = ['D:\\rentSpider\\rentSpider\\bj.csv', 'D:\\rentSpider\\rentSpider\\sh.csv',
         'D:\\rentSpider\\rentSpider\\gz.csv', 'D:\\rentSpider\\rentSpider\\sz.csv',
         'D:\\rentSpider\\rentSpider\\zz.csv']
cities = ['北京', '上海', '广州', '深圳', '郑州']
df_list = []

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 读取所有城市的CSV文件并添加城市标签
for i, file in enumerate(files):
    df = pd.read_csv(file)
    df['city'] = cities[i]  # 添加城市列
    df_list.append(df)

# 合并数据
data = pd.concat(df_list, ignore_index=True)

# 处理价格字段
data['price'] = data['price'].astype(float)

# 计算每个板块（district）的均价
district_avg_price = data.groupby(['city', 'district'])['price'].mean().reset_index()

# 设置子图，5个城市分别展示
fig, axes = plt.subplots(1, 5, figsize=(20, 8))  # 创建5个子图
fig.tight_layout(pad=5.0)  # 设置子图间距

for i, city in enumerate(cities):
    ax = axes[i]
    # 获取每个城市的数据
    city_data = district_avg_price[district_avg_price['city'] == city]

    # 将每个城市的数据转换为透视表
    pivot_table = city_data.pivot(index='district', columns='city', values='price')

    # 绘制热力图，不显示数值
    sns.heatmap(pivot_table, annot=False, cmap='coolwarm', linewidths=0.5, ax=ax)

    # 设置标题和标签
    ax.set_title(f'{city} 各板块租金均价')
    ax.set_xlabel('城市')
    ax.set_ylabel('板块')

plt.savefig('各城市各板块租金分布热力图.png')
plt.show()
