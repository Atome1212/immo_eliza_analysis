import pandas as pd
from scipy import stats

file = '/home/becode/becode/immo_eliza_analysis/data/formatted_json.json'

df = pd.read_json(file)


print(f'{df.shape} number of rows and columns')

print('\n')

print(df.info())

print('\n')

print('Missing values:')
print(df.isnull().sum())
print(df['GardenArea'].mean())

print('\n')

df_copy = df.copy()
df_copy.drop('Url', axis=1, inplace=True)
print('Number of duplicates:')
print(df_copy.duplicated().sum())
for index, x in enumerate(df_copy.duplicated()):
    if x is True:
        print(index)

print('\n')

print('Ensuring all data types are correct:')
print(df.dtypes)

print('\n')


z_scores = stats.zscore(df.select_dtypes(include=[int,float]))
outliers = (abs(z_scores)>3).sum()
print(outliers)


print('\n')
print(df.isnull().sum())
print(df['GardenArea'].mean())

print('\n')

print(df['GardenArea'].value_counts())

print('\n')


df = df.drop([df.index[15775], df.index[15776]])
df.fillna({'GardenArea': 0}, inplace=True)
df.fillna({'ConstructionYear': 0}, inplace=True)
df.fillna({'Kitchen': 0}, inplace=True)
df.fillna({'StateOfBuilding': 0}, inplace=True)
df.fillna({'Heating': 0}, inplace=True)
df.fillna({'SurfaceOfGood': 0}, inplace=True)
df.fillna({'LivingArea': 0}, inplace=True)
df.fillna({'NumberOfFacades': 0}, inplace=True)


print('\n')
print(df.isnull().sum())


b = []
for x in df['GardenArea']:
    if x > 0:
        b.append(x)

print(sum(b)/len(b))
print(df['GardenArea'].mean())


