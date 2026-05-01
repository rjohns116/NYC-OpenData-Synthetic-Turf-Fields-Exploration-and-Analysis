# NYC Open Data Synthetic Turf Fields: Exploration and Analysis
This project focuses on cleaning, standardizing and analyzing the [Synthetic Turf Fields](https://data.cityofnewyork.us/Recreation/Synthetic-Turf-Fields/weh8-3ujf/about_data) dataset from [NYC Open Data.](https://opendata.cityofnewyork.us/) After performing a full inspection and data quality assessment, the cleaned datset was used to investigate the **quality**, **accessibility** and **effectiveness** of synthetic turf fields in NYC.


## Project structure:
```project/
├── data/
├── figures/
├── notebooks/
├── src/
├── README.md
└── requirements.txt
```

## Objectives:
- Improve the **consistency, structure** and **readability** of a real-world municipal dataset
  
- Transform raw turf field records into **analysis-ready** features to answer questions about trends in access to high-quality public health resources
  
- Use cleaned dataset to visualize the **quality** and **availability** of synthetic turf fields across the city

## Research Questions:

 ### 🏈 **What boroughs have the most turf fields? Are they new and maintained or old?**

 ### 🏈 **Who maintains most of the fields and where? Are they *active* and *accessible*?**

 ### 🏈 **How many fields are located within a *Jointly Operated Playground* (JOP)? How many other fields are apart of a playground system?**

## Methods:
  1. Loaded in and inspected the raw dataset
  2. Cleaned the dataset changing column names, data types, removing unneccessary columns and addressing empty values
  3. Generated analytical questions that can be answered based on the data
  4. Applied pandas data manipulation techniques to structure and organize the data in response to each research question
  5. Used the processed data to create visualizations that support study findings
   
## Key findings:

### **⭐ Overall, most synthetic turf fields in NYC are *well-maintained, active* and *available* for use.**


- **73.0%** of all fields in the city were constructed as "infill" type fields with high-quality materials in two layers.

- **74.2%** of fields in the city are active and ready to use

- **92%** of all fields in the city are actively maintained by a company

- This dataset contained **0** retired fields. 

- **23.9%** of fields are new (less than 5 years old, as defined as younger than *2021-01-01*)

- **32.7%** of all fields in the city are located within or near a playground system

## Acknowledgements

#### **Data source:** [Synthetic Turf Fields](https://data.cityofnewyork.us/Recreation/Synthetic-Turf-Fields/weh8-3ujf/about_data) dataset from [NYC Open Data.](https://opendata.cityofnewyork.us/)

#### The project Jupyter notebook can be found here:
[Project notebook](https://github.com/rjohns116/NYC-OpenData-Synthetic-Turf-Fields-Exploration-and-Analysis/blob/main/notebooks/turf.ipynb)

#### **Tools used:**
- **Python** - .csv file I/O, pandas, dataframes
- **Seaborn** - bar charts 
- **Jupyter notebook** - images, tables, code and project structure



#### **All figures available here**:

[Figure 1: Map of the boroughs in New York City](https://ontheworldmap.com/usa/city/new-york-city/map-of-new-york-city-max.jpg)

[Figure 2: Synthetic turf field distribution across the boroughs](https://raw.githubusercontent.com/rjohns116/Project-2/refs/heads/main/figures/fig_2_fields_across_boroughs.png)

[Figure 3: Percentage of fields in the city actively maintained by a company](/workspaces/Project-2/figures/fig_3_percent_fields_maintained.png)

[Figure 4: Distribution of maintenance by company across the boroughs](/workspaces/Project-2/figures/fig_4_maintenance_across_boroughs.png)

[Figure 5: Distribution of JOP and play area-associated fields across boroughs](/workspaces/Project-2/figures/fig_5_all_play_fields_across_boroughs.png)

