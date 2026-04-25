import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
import seaborn as sns

df = pd.read_csv("/workspaces/Project-2/data/Synthetic_Turf_Fields_20260417.csv")

#Step 1: Clean the data

#Remove unnecessary columns
df = df.drop(columns=["Contract_Type", 
                      "Contract_Number", 
                      "Shape", 
                      "Maint_By_Spec", 
                      "Construction_Entity_Spec"])

#Rename columns to relevant descriptions in snake_case
df = df.rename(columns={"SYSTEM":"Field_ID",
                   "PARENTID":"Parent_ID",
                   "DEPARTMENT":"Department",
                   "DESCRIPTION":"Location_Description",
                   "Maint_By":"Maintained_By",
                   "SYNTURF_Location":"Cross_Streets",
                   "RETIRED":"Retired",
                   "FeatureStatus":"Status"
                   })


#Drop the parent_ID and "SYNTURF" from the Field_ID
df["Field_ID"] = df["Field_ID"].str.extract(r"(0\d+$)")

#remove the borough information from Parent_ID
df["Parent_ID"] = df["Parent_ID"].str.extract(r"(\d+$)")

#Change "Commission_Date" to datetime object
df["Commission_Date"] = pd.to_datetime(df["Commission_Date"], format="%m/%d/%Y")

#Replace all "Unknown" with NaN
df.replace(["Unknown", "Not Applicable"], pd.NA, inplace =True)

#Change "JOP" type to bool
df["JOP"] = df["JOP"].astype(bool)

#If the location contains "&" change it to "and"
df["Cross_Streets"] = df["Cross_Streets"].replace(r"\s&\s", " and ", regex=True)

#Combine "crumb rubber" and "rubber crumb" infill material types
df["Infill_Material"] = df["Infill_Material"].replace("Crumb Rubber", "Rubber Crumb")

#Expand borough names
df["Borough"] = df["Borough"].replace({"B":"Brooklyn",
                                       "M": "Manhattan",
                                       "Q": "Queens",
                                       "X": "Bronx",
                                       "R": "Staten Island"})


# Step 2: Start to answer analytical questions with the data

#Q1: What boroughs have the most turf fields? Are they new and maintained or old?

#Which borough has the most turf fields? 
df.groupby("Borough").size() #Brooklyn contains the most with 104 fields
b_fields = df[df["Borough"] == "Brooklyn"]

#What percentage of those fields have 'infill' turf type?
percent_infill = (b_fields["Turf_Type"] == "Infill").sum() / b_fields.shape[0] *100
percent_infill = round(percent_infill, 1) #72.1% of fields are type "infill"

#What does the distribution of infill materials look like?
materials = b_fields.groupby("Infill_Material").size().drop("Non-Infill").sort_values(ascending=False)

#How many fields are inactive?
percent_inactive = (b_fields["Status"] != "Active").sum() / b_fields.shape[0] * 100
percent_inactive = round(percent_inactive, 1) #20.2% of fields were archived, removed or inactive
retired_count = b_fields["Retired"].sum() #0 fields are retired!

#How many fields are less than 5 years old?
newest_count = b_fields[b_fields["Commission_Date"] >= "2021-01-01"].shape[0] #27 fields are new(less than 5 years old)

#How many fields are actively maintained by a company?
percent_maintained = b_fields["Maintained_By"].notna().sum() / b_fields.shape[0] * 100
percent_maintained = round(percent_maintained, 1) #91.3% of fields are maintained by a company!
owners = b_fields.groupby("Maintained_By").size().sort_values(ascending=False) #Most of the fields are maintained by DPR.

#Summary: NYC synthetic turf fields are concentrated in Brooklyn and show high quality and availability.

#Q2: Who maintains most of the fields and where?

#Who maintains the most fields and in what boroughs?
df_quality = df[["Turf_Type", "Maintained_By", "Retired", "Borough", "Status" ]]

owners_and_location = df_quality.groupby(["Maintained_By", "Borough"]).size() #DPR owns the most and they are the most evenly distributed across all five boroughs

#Are they active and not retired?
dpr_fields = df[df_quality["Maintained_By"] == "DPR"]
dpr_inactive = dpr_fields["Retired"].sum() + (dpr_fields["Status"] != "Active").sum()
percent_inactive = round(dpr_inactive / dpr_fields.shape[0] * 100, 1) # 28% of DPR owned fields are archived, removed or inactive, but none are retired

#What about non-DPR fields?
others = df[df["Maintained_By"] != "DPR"].dropna()
status = others[["Maintained_By", "Status"]]

#How many total fields in the city are actively maintained?
percent_maintained = round(df["Maintained_By"].notna().sum() / df.shape[0] * 100, 1)
dpr_maintained = round((df["Maintained_By"] == "DPR").sum() / df.shape[0] * 100, 1)


#Summary: DPR owns most of the fields in an even distribution across all boroughs - none are retired and 72% indicate "active" status

#Q3: How many fields are within a Jointly Operated Playground(JOP)? How many other fields are apart of a playground system?

#What percent of fields are located within a JOP?
percent_jop = round(df["JOP"].sum() / df.shape[0] * 100, 1) #21.7% of fields are located within a JOP

#How many fields are located in a play area, but not within a JOP?
play_area = df[df["System_Type"] == "Play Area"]
play_area = play_area[play_area["JOP"] == False]
additional_fields = play_area.shape[0] #There are an additional 35 fields in the city that are located in a play area, just not specifically a JOP

#Where are the fields concentrated?
jop_fields = df[df["JOP"]]
jop_distribution = jop_fields.groupby("Borough").size()
play_area_fields = play_area
play_area_distribution = play_area.groupby("Borough").size() #Both JOP fields and additional play area fields are fairly evenly distributed across all 5 boroughs

#What is the total percentage of fields located within or near a playground?
total_play_fields = additional_fields + jop_fields.shape[0]
percent_play_fields = round(total_play_fields / df.shape[0] * 100, 1)

#Summary: 21.7% of fields are located within a JOP. Out of the fields that aren't, an additional 35 are located in a play area. Both are evenly distributed across all 5 boroughs. 

#Step 3: Produce visuals to support findings

#Q1: ##bar chart - distribution of all synthetic turf fields across the city

plt.figure(figsize=(10,6))
sns.countplot(data = df,
              x = "Borough",
              hue = "Borough",
              legend=False,
              palette = "deep")
plt.title("Prevalence of turf fields across boroughs")
plt.savefig("/workspaces/Project-2/figures/fig_2_fields_across_boroughs.png")

   ##map of NYC boroughs to emphasize Brooklyn
url = "https://ontheworldmap.com/usa/city/new-york-city/map-of-new-york-city-max.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.save("/workspaces/Project-2/figures/fig_1_borough_map.jpg")


#Q2: double bar chart with showing company management for each borough 
maintenance_distribution = df[["Maintained_By", "Borough"]]

plt.figure(figsize=(8,4))
sns.countplot(maintenance_distribution,
              x = "Borough",
              hue = "Maintained_By")
plt.title("Maintenance of turf fields across boroughs")
plt.savefig("/workspaces/Project-2/figures/fig_4_maintenance_across_boroughs.png")

    #table showing percent managed fields for each borough (Use percentages to create a markdown table in jupyter with boroughs ordered according to sns order)
maintained = df[df["Maintained_By"].notna()].groupby("Borough").size().reset_index(name="Count Maintained")
total_per_borough = df.groupby("Borough").size().reset_index(name="Field Count")

percent_maintained = round(maintained["Count Maintained"] / total_per_borough["Field Count"] * 100, 1)


#Q3: #bar chart showing JOP and other play area fields distribution across boroughs
all_play_fields = pd.concat([jop_fields, play_area_fields], axis=0)

plt.figure(figsize=(6,3))
sns.countplot(data= all_play_fields,
              x = "Borough",
              hue= "Borough",
              order = ["Queens", "Brooklyn", "Bronx", "Manhattan", "Staten Island"],
              palette = "deep")
plt.title("Total JOP and play area-associated fields per borough")
plt.tight_layout()
plt.savefig("/workspaces/Project-2/figures/fig_5_all_play_fields_across_boroughs")


#Step 4: Summary stats
percent_infill = round(df[df_quality["Turf_Type"] == "Infill"].shape[0] / df.shape[0] * 100, 1)
percent_active = round(df[df["Status"] == "Active"].shape[0] / df.shape[0] * 100, 1)
percent_retired = round(df[df["Retired"]].shape[0] / df.shape[0] * 100, 1)
percent_new = round(df[df["Commission_Date"] >= "2021-01-01"].shape[0] / df.shape[0] *100, 1)
percent_play_fields = round((additional_fields + jop_fields.shape[0]) / df.shape[0] * 100, 1)




































