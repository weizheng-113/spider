import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import os

# 指定文件所在的目录
directory = 'D:\\rentSpider\\rentSpider'

# 设置matplotlib字体以正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# Pandas选项设置，以便更好地查看数据
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
stats.columns = ['_'.join(col).strip() for col in stats.columns]  # 移除可能存在的多余空格

# 打印统计信息
print(stats)

# 定义一个函数来绘制包含四个子图的图表，并保存图表
def plot_stats(stats_df, title_prefix, price_col, save_filename):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'{title_prefix}对比', fontsize=16)

    # 平均值
    sns.barplot(x=stats_df.index, y=f'{price_col}_mean', data=stats_df, ax=axes[0, 0])
    axes[0, 0].set_title(f'平均{price_col}')
    axes[0, 0].set_xlabel('城市')
    axes[0, 0].set_ylabel(price_col)

    # 最高值
    sns.barplot(x=stats_df.index, y=f'{price_col}_max', data=stats_df, ax=axes[0, 1])
    axes[0, 1].set_title(f'最高{price_col}')
    axes[0, 1].set_xlabel('城市')
    axes[0, 1].set_ylabel(price_col)

    # 最低值
    sns.barplot(x=stats_df.index, y=f'{price_col}_min', data=stats_df, ax=axes[1, 0])
    axes[1, 0].set_title(f'最低{price_col}')
    axes[1, 0].set_xlabel('城市')
    axes[1, 0].set_ylabel(price_col)

    # 中位数
    sns.barplot(x=stats_df.index, y=f'{price_col}_median', data=stats_df, ax=axes[1, 1])
    axes[1, 1].set_title(f'中位数{price_col}')
    axes[1, 1].set_xlabel('城市')
    axes[1, 1].set_ylabel(price_col)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # 保存图表
    plt.savefig(save_filename)
    plt.show()

# 绘制各个城市房租均价、最高价、最低价、中位数的对比并保存
plot_stats(stats, '各城市房租', 'price', '各城市房租对比.png')

# 绘制各个城市单位面积房租均价、最高价、最低价、中位数的对比并保存
plot_stats(stats, '各城市单位面积房租', 'price_per_area', '各城市单位面积房租对比.png')

# 绘制箱形图展示价格分布并保存
plt.figure(figsize=(14, 7))
sns.boxplot(x='city', y='price', data=all_data)
plt.title('各城市租金分布')
plt.xlabel('城市')
plt.ylabel('租金 (元)')
plt.savefig('各城市租金分布_boxplot.png')  # 保存箱形图
plt.show()

# 绘制箱形图展示单位面积租金分布并保存
plt.figure(figsize=(14, 7))
sns.boxplot(x='city', y='price_per_area', data=all_data)
plt.title('各城市单位面积租金分布')
plt.xlabel('城市')
plt.ylabel('单位面积租金 (元/平米)')
plt.savefig('各城市单位面积租金分布_boxplot.png')  # 保存箱形图
plt.show()