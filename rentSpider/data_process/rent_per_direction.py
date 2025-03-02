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

# 处理面积字段
data['area'] = data['area'].astype(float)

# 计算单位面积租金
data['unit_price'] = data['price'] / data['area']

# 处理朝向字段，将"南/北"等拆分为两个方向
def split_direction(direction):
    directions = direction.split('/')
    return directions if len(directions) > 1 else [direction]

# 通过拆分朝向字段来扩展数据
expanded_data = data.explode('direction', ignore_index=True)

# 确保方向是标准的八个方向
valid_directions = ['东', '南', '西', '北', '东南', '西南', '东北', '西北']
expanded_data = expanded_data[expanded_data['direction'].isin(valid_directions)]

# 将 direction 列转为类别型，并指定顺序
expanded_data['direction'] = pd.Categorical(expanded_data['direction'], categories=['东', '南', '西', '北', '东南', '西南', '东北', '西北'], ordered=True)

# 计算每个城市每个朝向的单位面积租金
direction_avg_price = expanded_data.groupby(['city', 'direction'])['unit_price'].mean().reset_index()

# 输出每个城市每个朝向的单位面积租金
print("各城市各朝向单位面积租金情况:")
print(direction_avg_price)

# ---- 绘制单位面积租金分布箱型图 ----
plt.figure(figsize=(14, 8))
sns.boxplot(x='city', y='unit_price', hue='direction', data=expanded_data)
plt.title('各城市不同朝向的单位面积租金分布')
plt.xlabel('城市')
plt.ylabel('单位面积租金 (元/㎡)')
plt.savefig('各城市不同朝向的单位面积租金分布箱型图.png')
plt.show()

# ---- 计算并输出哪个方向最高，哪个方向最低 ----
direction_max = direction_avg_price.loc[direction_avg_price.groupby('city')['unit_price'].idxmax()]
direction_min = direction_avg_price.loc[direction_avg_price.groupby('city')['unit_price'].idxmin()]

print("\n各城市最高单位面积租金方向:")
print(direction_max[['city', 'direction', 'unit_price']])

print("\n各城市最低单位面积租金方向:")
print(direction_min[['city', 'direction', 'unit_price']])

# ---- 绘制各城市的热力图 ----
for city in cities:
    city_data = direction_avg_price[direction_avg_price['city'] == city]

    # 将数据转换为透视表形式，用于热力图绘制
    city_pivot = city_data.pivot(index='direction', columns='city', values='unit_price')

    # 绘制热力图
    plt.figure(figsize=(6, 5))
    sns.heatmap(city_pivot, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5,
                cbar_kws={'label': '单位面积租金 (元/㎡)'})
    plt.title(f'{city} 各朝向单位面积租金热力图')
    plt.xlabel('城市')
    plt.ylabel('朝向')
    plt.savefig(f'{city} 各朝向单位面积租金热力图.png')
    plt.show()
