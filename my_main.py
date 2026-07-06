import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\Users\Saksham\Desktop\data.csv')


#Data Cleaning
df=df.drop_duplicates()
df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)

#Numeric Data Cleaning
df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).astype(int)
df["rate_per_sqft"] = pd.to_numeric(df["rate_per_sqft"].str.replace(",", ""), errors="coerce").fillna(0).astype(int)


#Categorical Data Cleaning
df['status'] = df['status'].str.strip().str.lower()
df["rera_approval"] = df["rera_approval"].str.strip().str.lower().map({"approved by rera": True, "not approved by rera": False})
df['flat_type'] = df['flat_type'].str.strip().str.lower()

df=df.drop_duplicates()
print(df.info())
print(df)

#Q-1 : Which is the costliest flat in the dataset
costliest_flat = df.loc[df["price"].idxmax()]
print(f"The costliest flat is a {costliest_flat['bhk_count']} BHK flat located in {costliest_flat['locality']} priced at {costliest_flat['price']/10000000} crores in {costliest_flat['society']} society.")

#Q-2 : Which locality has the highest average price?
highest_avg_price_locality = df.groupby("locality")["price"].mean().idxmax()
print(f"The locality with the highest average price is {highest_avg_price_locality}.")  

#Q-3 : Which locality has the highest rate per square foot?
highest_rate_locality = df.groupby("locality")["rate_per_sqft"].mean().idxmax()
print(f"The locality with the highest rate per square foot is {highest_rate_locality}.")

#Q-4 : Do ready-to-move properties cost more than under-construction properties?
avg_price = df.groupby("status")["price"].mean()

if avg_price["ready to move"] > avg_price["under construction"]:
    print("Ready-to-move properties cost more than under-construction properties.")
else:
    print("Under-construction properties cost more than ready-to-move properties.")

#Q-5 : Do RERA-approved properties command a price premium? (Kya RERA-approved properties ki average price, non-RERA-approved properties ki average price se zyada hai?)
avg_price = df.groupby("rera_approval")["price"].mean()

if avg_price[True] > avg_price[False]:
    print("RERA-approved properties command a price premium.")
else:
    print("RERA-approved properties do not command a price premium.")

#Q-6 : How does area (sqft) impact property price? (Flat ka area badhne se uski price par kya asar padta hai?)
correlation = df["area"].corr(df["price"])
print(f"Correlation between area and price: {correlation:.2f}")

if correlation > 0.7:
    print("There is a strong positive relationship between area and property price.")
elif correlation > 0.3:
    print("There is a moderate positive relationship between area and property price.")
elif correlation > 0:
    print("There is a weak positive relationship between area and property price.")
elif correlation < -0.3:
    print("There is a negative relationship between area and property price.")
else:
    print("There is little or no relationship between area and property price.")


plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="area", y="price")
plt.title("Area vs Property Price")
plt.xlabel("Area (sqft)")
plt.ylabel("Property Price")
plt.show()

# There is a weak positive relationship between property area and price (correlation = 0.20). This indicates that larger properties tend to have higher prices, but the relationship is not strong. The scatter plot also shows a wide spread of data points and some outliers, suggesting that property price is influenced by several other factors such as locality, property type, builder, amenities, and RERA approval, not just area.

#Q-7 : Which BHK configuration is most expensive based on per sqft rate?
avg_price = df.groupby("bhk_count")["price"].mean()
most_expensive_bhk = avg_price.idxmax()
print(f"The most expensive BHK configuration on average is {most_expensive_bhk} BHK.")

#Q-8 : Which property type (Apartment, Floor, Plot) is the costliest?
avg_price = df.groupby("flat_type")["price"].mean()
costliest_property_type = avg_price.idxmax()
print(f"The costliest property type on average is {costliest_property_type}.")

#Q-9 : Do certain builders or companies consistently price higher?
avg_builder_price = df.groupby("builder_name")["price"].mean()
highest_builder_price = avg_builder_price.idxmax()

avg_company_price = df.groupby("company_name")["price"].mean()
highest_company_price = avg_company_price.idxmax()

print(f"The builder with the highest average price is {highest_builder_price}.")
print(f"The company with the highest average price is {highest_company_price}.")

#Q-10 : Are larger homes always more expensive per square foot? 
correlation = df["area"].corr(df["rate_per_sqft"])

print(f"Correlation between area and rate per sqft: {correlation:.2f}")

if correlation > 0.3:
    print("Larger homes generally have a higher price per square foot.")
elif correlation < -0.3:
    print("Larger homes generally have a lower price per square foot.")
else:
    print("There is little or no relationship between home size and price per square foot.")

plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="area", y="rate_per_sqft")
plt.title("Area vs Rate per Square Foot")
plt.xlabel("Area (sqft)")
plt.ylabel("Rate per Sqft")
plt.show()

# The correlation between area and rate per square foot is approximately 0 (-0.00), indicating almost no relationship between property size and the price per square foot. The scatter plot also does not show any clear upward or downward trend. Therefore, larger homes are not necessarily more expensive per square foot. Other factors such as locality, builder, property type, and amenities likely have a greater influence on the rate per square foot.

# Top 10 Localities by Average Price
top_localities = df.groupby("locality")["price"].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top_localities.values, y=top_localities.index)
plt.title("Top 10 Localities by Average Price")
plt.xlabel("Average Price")
plt.ylabel("Locality")
plt.tight_layout()
plt.show()