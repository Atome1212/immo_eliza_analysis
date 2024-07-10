import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime


#Url,BathroomCount,BedroomCount,ConstructionYear,Country,District,Fireplace,FloodingZone,Furnished,Garden,GardenArea,Kitchen,LivingArea,Locality,MonthlyCharges,NumberOfFacades,PEB,PostalCode,Price,PropertyId,Province,Region,RoomCount,ShowerCount,StateOfBuilding,SubtypeOfProperty,SurfaceOfPlot,SwimmingPool,Terrace,ToiletCount,TypeOfProperty,TypeOfSale


# group by colonne province
postal_code_to_province = {
    range(1000, 1299): 'Région de Bruxelles-Capitale',
    range(1300, 1499): 'Brabant wallon',
    range(1500, 1999): 'Brabant flamand',
    range(2000, 2999): 'Anvers',
    range(3000, 3499): 'Brabant flamand (Louvain)',
    range(3500, 3999): 'Limbourg',
    range(4000, 4999): 'Liège',
    range(5000, 5999): 'Namur',
    range(6000, 6599): 'Hainaut',
    range(6600, 6999): 'Luxembourg',
    range(7000, 7999): 'Hainaut (2)',
    range(8000, 8999): 'Flandre-Occidentale',
    range(9000, 9999): 'Flandre-Orientale'
}

def no_duplicates(df):
    df_without_url = df.drop(columns=['Url', 'PropertyId', 'SubtypeOfProperty'])
    df_unique = df_without_url.drop_duplicates()
    df_result = df.loc[df_unique.index]

    return df_result

def strip_data(df):
    for i in df.columns:
        df[i] = df[i].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def no_null(df):    
    missing_percentage = df.isnull().mean() * 100

    for i in df.columns:
        if pd.api.types.is_bool_dtype(df[i]):
            df[i] = df[i].fillna(False)
        elif pd.api.types.is_integer_dtype(df[i]):
            df[i] = df[i].fillna(0)
        elif pd.api.types.is_float_dtype(df[i]):
            df[i] = df[i].fillna(0)
            df[i] = df[i].astype(int)
        else:
            df[i] = df[i].fillna("Unknown")
            
    return df, missing_percentage

def data_error(df):
    df_filtered = df[
        (df['PostalCode'] >= 1000) & (df['PostalCode'] <= 9999) &
        (df['Price'] > 0) & (df['Price'] < 15000000) &  
        (df['LivingArea'] > 0) & (df['LivingArea'] < 10000) &
        (df['BathroomCount'] <= df['BedroomCount']) &
        (df['ConstructionYear'] <= datetime.date.today().year+10) &
        (df['NumberOfFacades'] <= 4) & # si > mettre 4 facades
        (df['ToiletCount'] < df['RoomCount']) &
        (df['ShowerCount'] <= df['BathroomCount']) &
        (df['TypeOfSale'] != "annuity_monthly_amount") &
        (df['TypeOfSale'] != "annuity_without_lump_sum") &
        (df['TypeOfSale'] != "annuity_lump_sum")
    ]

    df_filtered['TypeOfSale'] = df_filtered['TypeOfSale'].replace('residential_sale', 1)
    df_filtered['TypeOfSale'] = df_filtered['TypeOfSale'].replace('residential_monthly_rent', 2)
        
    return df_filtered

def get_province(postal_code):
    for postal_range, province in postal_code_to_province.items():
        if postal_code in postal_range:
            return province
    return 'Other'

def median(df, type):
    df_sales = df[df['TypeOfSale'] == type]

    df_sales['Province'] = df_sales['PostalCode'].apply(get_province)

    mean_prices = df_sales.groupby('Province')['Price'].median()

    plt.figure(figsize=(15, 7))
    mean_prices.plot(kind='bar', color='blue')
    plt.title('Median Prices by Province')
    plt.xlabel('Province')
    plt.ylabel('Median Price')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    
    plt.show()

def categorize_living_area(area):
    if area < 50:
        return '0-50'
    elif area < 100:
        return '51-100'
    elif area < 150:
        return '101-150'
    elif area < 200:
        return '151-200'
    elif area < 250:
        return '201-250'
    elif area < 300:
        return '251-300'
    elif area < 400:
        return '301-400'
    elif area < 500:
        return '401-500'
    elif area < 1000:
        return '501-1000'
    else:
        return '1001+'

def categorize_construction_year(year):
    if year < 1900:
        return 'Before 1900'
    elif year < 1950:
        return '1900-1949'
    elif year < 2000:
        return '1950-1999'
    else:
        return '2000+'

def categorize_garden_area(area):
    if area == 0:
        return 'No Garden'
    elif area < 50 and area >= 1:
        return '1-50'
    elif area < 100:
        return '51-100'
    elif area < 200:
        return '101-200'
    elif area < 500:
        return '201-500'
    elif area < 1000:
        return '501-1000'
    else:
        return '1001+'

def plot_comparisons(df):
    df_sales = df[df['TypeOfSale'] == 1]
    
    comparisons = {
        'SubtypeOfProperty': ['Subtype of Property', 'bar', '#8705e4'],
        'RoomCount': ['Number of Room', 'bar', '#3DFE20'],
        'BedroomCount' : ['Number of Bedroom', 'bar', '#d61a1f'], # grouper
        'LivingAreaCategory': ['Living Area Category', 'bar', '#c7ab32'], # diminuer
        'ConstructionYearCategory': ['Year of Construction Category', 'bar', '#5453c6'], # changer col
        'StateOfBuilding': ['State of Building', 'bar', '#767bb2'], # retirer unk
        'Kitchen': ['Type of Kitchen', 'bar', '#ff06c1'], # retir unk
        'SwimmingPool': ['Has Swimming Pool', 'bar', '#ad00fa'], # true false
        'NumberOfFacades': ['Number of Facades', 'bar', '#8c1aff'], # retir 0
        'GardenAreaCategory': ['Garden Area Category', 'bar', '#00ffff'],
        'BathroomCount': ['Number of Bathrooms', 'bar', '#FF5733'],     
        'Fireplace': ['Has Fireplace', 'bar', '#33FFCE'], # true false
        'Furnished': ['Is Furnished', 'bar', '#FF33A8'], # true false
        'FloodingZone': ['Flooding Zone', 'bar', '#335BFF'], # un col inondable et un colo pas inondable
        'PEB': ['PEB Rating', 'bar', '#FF8C33'], # retirer unk
        'Terrace': ['Has Terrace', 'bar', '#33FF57'], # true false
        'ToiletCount': ['Number of Toilets', 'bar', '#FF3386'] # group
    }
    
    for column, element in comparisons.items():
        plt.figure(figsize=(18, 5))

        df_filtered = df_sales[df_sales[column] != 'Pas renseigné']
        df_grouped = df_filtered.groupby(column)['Price'].median()

        # faire automatique
        if column == 'LivingAreaCategory':
            order = ['0-50', '51-100', '101-150', '151-200', '201-250', '251-300', '301-400', '401-500', '501-1000', '1001+']
            df_sales[column] = pd.Categorical(df_sales[column], categories=order, ordered=True)
        elif column == 'ConstructionYearCategory':
            order = ['Before 1900', '1900-1949', '1950-1999', '2000+']
            df_sales[column] = pd.Categorical(df_sales[column], categories=order, ordered=True)
        elif column == 'GardenAreaCategory':
            order = ['No Garden', '1-50', '51-100', '101-200', '201-500', '501-1000', '1001+']
            df_sales[column] = pd.Categorical(df_sales[column], categories=order, ordered=True)
        
        
        df_grouped.sort_index().plot(kind=element[1], color=element[2])
        plt.title(f'Median Price by {element[0]} (Sales Only)')
        plt.xlabel(element[0])
        plt.ylabel('Median Price')
        plt.grid(axis='y', linestyle='--', alpha=0.2)
        plt.tight_layout()
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
        plt.show()

if __name__ == "__main__":
    data = pd.read_csv('../data/csvfile.csv')
    df = pd.DataFrame(data)

    #Step 1 : Data Cleaning

    #You have collected your data! So it's time to do a cleaning on it. A cleaned dataset is a dataset that doesn't contain any duplicates, is blank spaces or error-free. The rest of the analysis can be discarded if you neglect this step!

    # No duplicates
    noduply = no_duplicates(df)

    #No blank spaces (ex: `" I love python "` => `"I love python"`)
    striped = strip_data(noduply)

    #No empty values
    not_nulled = no_null(striped)
    df_not_nulled = not_nulled[0]
    missing_percentage = not_nulled[1]

    #No errors
    df_no_error = data_error(df_not_nulled)


    #Step 2 : Data Analysis

    #Now that the data has been collected and cleaned, it is time for the analysis. How many variables and inputs do you have? And so on...

    #Use the tools such as `matplotlib`/`seaborn`/`plotly`!

    #Answer the following questions with a vizualization if appropriate:

    #How many rows and columns?
    print("======================")
    print(f"Nb of line : {len(df_no_error.index)}")
    print(f"Nb of columns : {len(df_no_error.columns)}")
    print("======================")
    

    # What is the correlation between the variables and the price? (Why might that be?)


    median(df_no_error, 1)

    df_no_error['LivingAreaCategory'] = df_no_error['LivingArea'].apply(categorize_living_area)
    df_no_error['ConstructionYearCategory'] = df_no_error['ConstructionYear'].apply(categorize_construction_year)
    df_no_error['GardenAreaCategory'] = df_no_error['GardenArea'].apply(categorize_garden_area)



    plot_comparisons(df_no_error)


    #Percentage of missing values per column?
    print(f"Missing percentage per column:\n{missing_percentage}")


    ### sub plot !!!!!!!