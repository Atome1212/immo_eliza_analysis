# 🏠🏢 Immo Property Data Analysis


## 📜 Description


- This project involves being able to use pandas, as well as other data visulization libraries (matplotlib and seaborn).

- We need to clean a dataset for analysis, also establish conclusions about a dataset.

- This project involves thinking outside the box and to be able to find and answer creative questions about data.

## 📦 Installation
 
- To run this project, you need to have Python installed on your machine.
  You also need the following Python libraries:

- `geopandas`

- `matplotlib`

- `pandas`

- `seaborn`

- `datetime`


## 🛠️ Usage

### 1. 📥 Data Cleaning

Making sure dataset is free of:

	•	Duplicates
	•	Blank spaces (e.g., “ I love python “ should be “I love python”)
	•	Errors
	•	Empty values

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

-  `no_duplicates(df)`: Removes duplicate rows from the DataFrame, except for the columns ‘Url’, ‘PropertyId’, and ‘SubtypeOfProperty’.

- `strip_data(df)`: Strips leading and trailing whitespace from all string entries in the DataFrame.

- `no_null(df)`: Handles missing values by filling them with appropriate default values based on data type.

- `data_error(df)`:  Filters out erroneous data based on predefined criteria and corrects some values.

- `get_province(postal_code)`: Returns the corresponding province if the postal code falls within the range.

- `median(df, type, color='blue')`: Plots the median prices by province for a specific type of sale.

- `categorize_data(value, bins, labels)`: Categorizes a value based on predefined bins and labels(uses 'cut' method from pandas)

- `replace_0_1_with_bool(df, columns)`: Converts 0 and 1 values to boolean values in specified columns.

- `plot_generic(ax, df, column, title, xlabel, ylabel, color, categories=None, remove_unknown=True)`: Creates a generic bar plot for a specified columns.

- `generate_grouped_plots(df)`: Generates multiple grouped plots to visualize different property characteristics.

- `categorize_number_bedrooms(bedrooms)`: Categorizes the number of bedrooms into defined ranges.

- `categorize_number_bathrooms(bathrooms)`: Categorizes the number of bathrooms into defined ranges.

- `categorize_livingArea(livingArea)`: Categorizes the living area into defined ranges.

- `categorize_gardenArea(gardenArea)`: Categorizes the garden area into defined ranges.



## 👥 Contributors

- 👨‍🦰 Ben Ozfirat

- 👨‍🦰 Colin Gregoire

- 👨‍🦰 Alisher Jardemaliyev

## 📅 Timeline

- `Day 1`: Project setup, library installation, and initial testing.

- `Day 2-3`: Exploratory data analysis.

- `Day 4`: Graph plotting and creation of a story.

- `Day 5`: Documentation and final testing.

