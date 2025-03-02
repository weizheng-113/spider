import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import os

# 指定文件所在的目录
directory = 'D:\\rentSpider\\rentSpider'

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.width', None)  # 设置为自动调整宽度

# 获取所有csv文件路径
file_paths = [os.path.join(directory, f) for f in ['bj.csv', 'sh.csv', 'gz.csv', 'sz.csv', 'zz.csv']]

# 创建一个空的DataFrame用于存储所有数据
all_data = pd.DataFrame()

# 遍历每个csv文件并读取内容到DataFrame中
for file_path in file_paths:
    city_data = pd.read_csv(file_path)
    # 添加一列表示城市名称（从文件名中提取）
    city_name = os.path.splitext(os.path.basename(file_path))[0].upper()
    city_data['city'] = city_name

    # 计算单位面积租金
    city_data['price_per_area'] = city_data['price'] / city_data['area']

    # 将当前城市的dataframe追加到总的dataframe中
    all_data = pd.concat([all_data, city_data], ignore_index=True)

# 计算每个城市的统计信息
stats = all_data.groupby('city').agg({
    'price': ['mean', 'max', 'min', 'median'],
    'price_per_area': ['mean', 'max', 'min', 'median']
})

# 重置列名以便后续操作
stats.columns = ['_'.join(col) for col in stats.columns]

# 打印统计信息
print(stats)

# 绘制箱形图来展示价格分布
plt.figure(figsize=(14, 7))
sns.boxplot(x='city', y='price', data=all_data)
plt.title('Rent Price Distribution by City')
plt.ylabel('Price (RMB)')
plt.show()

# 绘制箱形图来展示单位面积租金分布
plt.figure(figsize=(14, 7))
sns.boxplot(x='city', y='price_per_area', data=all_data)
plt.title('Rent Price per Area Distribution by City')
plt.ylabel('Price per Area (RMB/sq meter)')
plt.show()

# 如果需要保存图片
# plt.savefig('rent_price_distribution.png')