import pandas as pd
import shutil
import datetime

# 定义CSV文件路径
file_path = 'D:\\rentSpider\\rentSpider\\bj.csv'

# 创建备份文件
backup_file_path = f'D:\\rentSpider\\rentSpider\\bj_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
shutil.copy(file_path, backup_file_path)
print(f"原始文件已备份至: {backup_file_path}")

# 读取CSV文件
df = pd.read_csv(file_path)

# 查看原始数据
print("原始数据:")
print(df)

# 检查是否有重复项
print("\n检查重复项:")
print(df.duplicated().sum())

# 去除重复项，保留第一次出现的记录
# 根据所有列去重
df_cleaned = df.drop_duplicates(subset=['title', 'district', 'area', 'direction', 'price', 'types'], keep='first')

# 查看清理后的数据
print("\n清理后的数据:")
print(df_cleaned)

# 保存清理后的数据回到原始CSV文件，覆盖原文件
df_cleaned.to_csv(file_path, index=False)

print(f"\n去重后的数据已保存到 {file_path}")