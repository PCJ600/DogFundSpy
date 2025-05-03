import akshare as ak
import pandas as pd

# 1. 获取场内交易数据（保留所有字段）
market_df = ak.fund_etf_hist_sina(symbol="sh501305")
market_df['date'] = pd.to_datetime(market_df['date']).dt.strftime('%Y-%m-%d')  # 标准化日期格式

# 2. 计算振幅（最高价 - 最低价）
market_df['amplitude'] = (market_df['high'] - market_df['low']).round(4)  # 保留4位小数

# 3. 获取单位净值数据
nav_df = ak.fund_open_fund_info_em(symbol='501305', indicator='单位净值走势')
nav_df = nav_df[['净值日期', '单位净值']].rename(columns={'净值日期': 'date', '单位净值': 'nav'})
nav_df['date'] = pd.to_datetime(nav_df['date']).dt.strftime('%Y-%m-%d')  # 标准化日期格式

# 4. 合并数据（按日期左连接，保留所有交易日数据）
merged_df = pd.merge(market_df, nav_df, on='date', how='left')

# 5. 计算溢价率（若当天无净值数据则设为NaN）
merged_df['premium_rate'] = (merged_df['close'] / merged_df['nav'] - 1) * 100
merged_df['premium_rate'] = merged_df['premium_rate'].round(2)  # 保留2位小数

# 6. 按日期倒序排列并输出
merged_df = merged_df.sort_values('date', ascending=False)
print(merged_df.head())

# 7. 保存结果
merged_df.to_csv('501305_full_data.csv', index=False)
print("数据已保存为 501305_full_data.csv")
