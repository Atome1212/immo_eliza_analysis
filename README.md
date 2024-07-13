# 🏠🏢 Immo Property Data Analysis


## 📜 Description


- This project involves the cleaning and analysis of the dataset created during the last challenge.

- Using pandas and matplotlib, the objectives were to find and understand correlations between dataset's variables.

- This project involves thinking outside the box and to be able to find and answer creative questions about data.

<p align="center">
  <img src="./Images/Image 1.jpg" style="max-width: 35%; height: auto;">
</p>

## 📦 Installation
 
- To run this project, you need to have Python installed on your machine.
  You also need the following Python libraries:

- 🌍 `geopandas`

- 🧮 `matplotlib`

- 🐼 `pandas`

- 🌊 `seaborn`

- 🕥 `datetime`


## 🛠️ Usage
  
### 1. 🧹 Data Cleaning

Making sure dataset is free of:

	•	Duplicates
	•	Blank spaces (e.g., “ I love python “ should be “I love python”)
	•	Errors
	•	Empty values


<p align="center">
  <img src="./Images/Image 2.jpg" style="max-width: 35%; height: auto;">
</p>


### 2. 📊 Data Analysis



Analyze the cleaned dataset using tools such as matplotlib, seaborn, or plotly. Address the following questions with correct visualizations:

	•	How many rows and columns?
	•	What is the correlation between the variables and the price?
	•	How are variables correlated to each other?
	•	Which variables have the greatest influence on the price?
	•	Which variables have the least influence on the price?
	•	How many qualitative and quantitative variables are there? How would you transform these values into numerical values?
	•	Percentage of missing values per column?

### 3. 🔄 📝 Communication

Afterwards, we need to communicate our analysis clearly with simple words and visual aids and address the following questions:

	•	Plot the outliers.
	•	Which variables would you delete and why?
	•	Represent the number of properties according to their surface using a histogram.
	•	Which 5 variables are the most important and why?
	•	What are the most expensive municipalities in Belgium? (Average price, median price, price per square meter)
	•	What are the most expensive municipalities in Wallonia? (Average price, median price, price per square meter)
	•	What are the most expensive municipalities in Flanders? (Average price, median price, price per square meter)
	•	What are the least expensive municipalities in Belgium? (Average price, median price, price per square meter)
	•	What are the least expensive municipalities in Wallonia? (Average price, median price, price per square meter)
	•	What are the least expensive municipalities in Flanders? (Average price, median price, price per square meter)

### 4. 📉 Presentation

- Finally, we need to create a compelling presentation that tells a story from the data.

## 🦄 Features

### 🖥️ Data Collection and Processing:

- Automated data cleaning.

- Analysis and transformation of JSON data to csv format.

### 📋 Data Points:

- Detailed visual overview of different properties all across Belgium.


## 🧑‍💻🎯 Project Components: Functions and Descriptions

-  `drop_duplicates()`: Compare the rows from the DataFrame. If two rows have the same date in the columns:'BedroomCount','District','Price','Garden','GardenArea','RoomCount',
'SurfaceOfPlot','TypeOfSale' except for the columns ‘Url’, ‘PropertyId’, and ‘SubtypeOfProperty’, keep the first occurence and delete the other(s).

- `replace_0_1_with_bool()`: If a column contains only 0 and 1 value, replace them to boolean value.

- `no_null()`: Handles missing values by filling them with appropriate default values based on data type.

- `data_error(df)`:  Filters out erroneous data based on predefined criteria and corrects some values.

- `format_column_name()`: Take the column's name and replace the '_' in spaces

- `plot_generic()`: Create a plot showing the median prices from the Dataframe based on a specific column. It can also filter out 'Unknown' values and customize the chart's look.

- `categorize_construction_year`: Groups construction years into 5 categories and  adds them to the Dataframe. Then, makes two bar charts showing median prices by construction year and building state.

- `categorize_livingArea(livingArea)`: Categorizes the living area into defined ranges.
  
- `categorize_gardenArea(gardenArea)`: Categorizes the garden area into defined ranges.

- `categorize_number_bedrooms(bedrooms)`: Categorizes the number of bedrooms into defined ranges.

- `categorize_number_bathrooms(bathrooms)`: Categorizes the number of bathrooms into defined ranges.
    


## 👥 Contributors


<table style="width: 100%;" >
<tbody>
<tr>
<td style="border: 1px solid #ffffff00" width="90%">
Colin Gregoire <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> https://github.com/Atome1212<br>
Ben Ozfirat <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> https://github.com/benozfirat<br>
Alisher Jardemaliyev <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> https://github.com/AlisherJard
</td>
<td>
<img src="https://github.com/kaiyungtan/challenge-data-analysis/blob/master/Visualisation/Immoweb%20house%20logo.png?raw=true">
</td>
</tr>
</tbody>
</table>


## 📅 Timeline

- `Day 1`: Project setup, library installation, and initial testing.

- `Day 2-3`: Exploratory data analysis.

- `Day 4`: Graph plotting and creation of a story.

- `Day 5`: Documentation and final testing.

