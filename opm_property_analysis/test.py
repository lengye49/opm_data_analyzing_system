import pandas as pd

df_heroes_configs = pd.read_excel('设计表.xlsx', sheet_name='heroes', header=0, index_col='HeroId')
df_heroes_configs.dropna(axis=0, how='all')
print(df_heroes_configs)