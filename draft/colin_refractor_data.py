import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns

# Url,BathroomCount,BedroomCount,ConstructionYear,Country,District,Fireplace,FloodingZone,Furnished,Garden,GardenArea,Kitchen,LivingArea,Locality,MonthlyCharges,NumberOfFacades,PEB,PostalCode,Price,PropertyId,Province,Region,RoomCount,ShowerCount,StateOfBuilding,SubtypeOfProperty,SurfaceOfPlot,SwimmingPool,Terrace,ToiletCount,TypeOfProperty,TypeOfSale

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
    df['NumberOfFacades'] = df['NumberOfFacades'].apply(lambda x: 4 if x >= 4 else x)
    
    df_filtered = df[
        (df['PostalCode'] >= 1000) & (df['PostalCode'] <= 9999) &
        (df['Price'] > 0) & (df['Price'] < 15000000) &  
        (df['LivingArea'] > 0) & (df['LivingArea'] < 10000) &
        (df['BathroomCount'] <= df['BedroomCount']) &
        (df['ConstructionYear'] <= datetime.date.today().year + 10) &
        (df['NumberOfFacades'] <= 4) &
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

def median(df, type, color='blue'):
    df_sales = df[df['TypeOfSale'] == type]
    df_sales['Province'] = df_sales['PostalCode'].apply(get_province)
    mean_prices = df_sales.groupby('Province')['Price'].median()
    
    plt.figure(figsize=(15, 7))
    mean_prices.plot(kind='bar', color=color)
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
    if year < 1799:
        return 'Before 1800'
    elif year <= 1900:
        return '1800-1900'
    elif year <= 1950:
        return '1900-1950'
    elif year <= 2000:
        return '1950-2000'
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
    
def categorize_BedroomCount(count):
    if count <= 2:
        return '2 Bedrooms or less'
    elif count <= 5:
        return '3 to 5 Bedrooms'
    elif count <= 10:
        return '6 to 10 Bedrooms'
    elif count <= 20:
        return '11 to 20 Bedrooms'
    else:
        return 'More than 20'

def replace_0_1_with_bool(df, columns):
    for column in columns:
        df[column] = df[column].replace({0: False, 1: True})
    return df

def format_column_name(name):
    if isinstance(name, str):
        return name.replace('_', ' ').title()
    else:
        return name

def plot_generic(ax, df, column, title, xlabel, ylabel, color, categories=None, remove_unknown=True):
    if remove_unknown:
        df = df[df[column] != 'Unknown']
    
    df_grouped = df.groupby(column)['Price'].median()
    
    if categories:
        df[column] = pd.Categorical(df[column], categories=categories, ordered=True)
        df_grouped = df_grouped.reindex(categories)
    else:
        df_grouped = df_grouped.sort_values(ascending=True)

    df_grouped.index = [format_column_name(name) for name in df_grouped.index]

    df_grouped.plot(kind='bar', color=color, edgecolor='black', ax=ax)

    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.2)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    ax.tick_params(axis='x', which='major', labelsize=8)

def generate_grouped_plots(df):
    df_sales = df[df['TypeOfSale'] == 1]

    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    fig.suptitle('General Property Characteristics', fontsize=12)

    plot_generic(axs[0], df_sales, 'SubtypeOfProperty', 'Median Price by Subtype of Property (Sales Only)', 'Subtype of Property', 'Median Price', '#8705e4')
    plot_generic(axs[1], df_sales, 'Province', 'Median Price by Province (Sales Only)', 'Province', 'Median Price', '#6b5b95')

    fig.tight_layout(rect=[0, 0, 1, 0.96])  

    fig, axs = plt.subplots(3, 2, figsize=(10, 15))
    fig.suptitle('Interior Characteristics', fontsize=12)
    
    plot_generic(axs[0, 0], df_sales, 'BedroomCount', 'Median Price by Number of Bedrooms (Sales Only)', 'Number of Bedrooms', 'Median Price', '#d61a1f', categories=['2 Bedrooms or less', '3 to 5 Bedrooms', '6 to 10 Bedrooms', '11 to 20 Bedrooms', 'More than 20'])
    plot_generic(axs[0, 1], df_sales, 'RoomCount', 'Median Price by Number of Rooms (Sales Only)', 'Number of Rooms', 'Median Price', '#ff7f50')
    plot_generic(axs[1, 0], df_sales, 'BathroomCount', 'Median Price by Number of Bathrooms (Sales Only)', 'Number of Bathrooms', 'Median Price', '#6495ed')
    plot_generic(axs[1, 1], df_sales, 'Kitchen', 'Median Price by Type of Kitchen (Sales Only)', 'Type of Kitchen', 'Median Price', '#ff06c1')
    plot_generic(axs[2, 0], df_sales, 'Fireplace', 'Median Price by Has Fireplace (Sales Only)', 'Has Fireplace', 'Median Price', '#8b0000')
    plot_generic(axs[2, 1], df_sales, 'Furnished', 'Median Price by Furnished Status (Sales Only)', 'Furnished Status', 'Median Price', '#ffa500')

    fig.tight_layout(rect=[0, 0, 1, 0.96])  

    fig, axs = plt.subplots(3, 2, figsize=(10, 15))
    fig.suptitle('Exterior and Specific Characteristics', fontsize=12)

    plot_generic(axs[0, 0], df_sales, 'Garden', 'Median Price by Has Garden (Sales Only)', 'Has Garden', 'Median Price', '#228b22')
    plot_generic(axs[0, 1], df_sales, 'SwimmingPool', 'Median Price by Has Swimming Pool (Sales Only)', 'Has Swimming Pool', 'Median Price', '#20b2aa')
    plot_generic(axs[1, 0], df_sales, 'Terrace', 'Median Price by Has Terrace (Sales Only)', 'Has Terrace', 'Median Price', '#ffa07a')
    plot_generic(axs[1, 1], df_sales, 'NumberOfFacades', 'Median Price by Number of Facades (Sales Only)', 'Number of Facades', 'Median Price', '#8c1aff')
    fig.delaxes(axs[2, 0]) 
    fig.delaxes(axs[2, 1])

    fig.tight_layout(rect=[0, 0, 1, 0.96])  
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('Condition and Construction', fontsize=12)

    plot_generic(axs[0], df_sales, 'ConstructionYearCategory', 'Median Price by Year of Construction (Sales Only)', 'Year of Construction', 'Median Price', '#2e8b57', ['Before 1800', '1800-1900', '1900-1950', '1950-2000', '2000+'])
    plot_generic(axs[1], df_sales, 'StateOfBuilding', 'Median Price by State of Building (Sales Only)', 'State of Building', 'Median Price', '#767bb2')

    fig.tight_layout(rect=[0, 0, 1, 0.96])  

    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    fig.suptitle('Other Characteristics', fontsize=12)

    plot_generic(axs[0], df_sales, 'PEB', 'Median Price by PEB Rating (Sales Only)', 'PEB Rating', 'Median Price', '#ff6347')
    plot_generic(axs[1], df_sales, 'FloodingZone', 'Median Price by Flooding Zone (Sales Only)', 'Flooding Zone', 'Median Price', '#5F9EA0')

    fig.tight_layout(rect=[0, 0, 1, 0.96]) 
    plt.show()

if __name__ == "__main__":
    data = pd.read_csv('../data/csvfile.csv')
    df = pd.DataFrame(data)

    # Step 1: Data Cleaning
    noduply = no_duplicates(df)
    striped = strip_data(noduply)
    not_nulled = no_null(striped)
    df_not_nulled = not_nulled[0]
    missing_percentage = not_nulled[1]

    boolean_columns = ['Fireplace', 'FloodingZone', 'Furnished', 'Garden', 'SwimmingPool', 'Terrace']
    df_not_nulled = replace_0_1_with_bool(df_not_nulled, boolean_columns)

    df_no_error = data_error(df_not_nulled)

    # Step 2: Data Analysis
    print("======================")
    print(f"Nb of line : {len(df_no_error.index)}")
    print(f"Nb of columns : {len(df_no_error.columns)}")
    print("======================")

    #median(df_no_error, 1, color='blue')
    
    df_sales = df_no_error[df_no_error['TypeOfSale'] == 1]
    
    fig, axs = plt.subplots(1, 2, figsize=(20, 6))

    df_wallonie = df_sales[df_sales['Region'] == 'Wallonie']
    plot_generic(axs[0], df_wallonie, 'District', 'Median Price by District in Wallonie', 'District', 'Median Price', '#940e0a')

    df_flanders = df_sales[df_sales['Region'] == 'Flanders']    
    plot_generic(axs[1], df_flanders, 'District', 'Median Price by District in Flanders', 'District', 'Median Price', '#022930')

    plt.tight_layout()
    plt.show()
    

    df_no_error['LivingAreaCategory'] = df_no_error['LivingArea'].apply(categorize_living_area)
    df_no_error['ConstructionYearCategory'] = df_no_error['ConstructionYear'].apply(categorize_construction_year)
    df_no_error['GardenAreaCategory'] = df_no_error['GardenArea'].apply(categorize_garden_area)
    df_no_error['BedroomCount'] = df_no_error['BedroomCount'].apply(categorize_BedroomCount)

    generate_grouped_plots(df_no_error)
    
    
    numeric_cols = df_no_error.select_dtypes(include=['float64', 'int64']).columns
    data = df_no_error[numeric_cols].drop(columns=[], errors='ignore')

    corr_matrix = data.corr(method='pearson')

    plt.figure(figsize=(16, 12))
    heatmap = sns.heatmap(
        corr_matrix, 
        cmap='icefire', 
        annot=True, 
        fmt=".2f", 
        linewidths=.5, 
        cbar_kws={"shrink": .8}, 
        annot_kws={"size": 10}
    )
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize': 16, 'fontweight': 'bold'}, pad=20)

    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    for text in heatmap.texts:
        text.set_size(9)

    plt.tight_layout()

    plt.show()    
    
 
