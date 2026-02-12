import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib
matplotlib.use('TkAgg')

#  output directory for visuals
os.makedirs('visualizations', exist_ok=True)

#  Load data set
df = pd.read_csv('All_Diets.csv')
print("\nMissing values:")
print(df.isnull().sum())

numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']

# handle missing data
df.fillna(df.mean(numeric_only=True), inplace=True)

# Average macronutrient content for each diet type
avg_macros = df.groupby('Diet_type')[numeric_cols].mean()
print("\nAverage Macronutrients by Diet Type")
print(avg_macros.round(2))

# Top 5 protein rich recipes per diet type
top_protein = (df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5))

print("\nTop 5 Protein-Rich Recipes per Diet Type")
for diet, group in top_protein.groupby('Diet_type'):
	print(diet.upper() + ":")
	for _, row in group.iterrows():
		print(" ", row['Recipe_name'], "-", row['Protein(g)'], "g")
		
# Diet type with highest average protein
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
print("\nDiet with Highest Avg Protein:", highest_protein_diet,
	avg_macros.loc[highest_protein_diet, 'Protein(g)'].round(2), "g")
	
# Most common cuisines per diet tpe
common_cuisines = (df.groupby('Diet_type')['Cuisine_type'].apply(lambda x: x.value_counts().head(3)))
print("\nMost Common Cuisines per Diet Type")
print(common_cuisines)

# new metrics ratios
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

# Bar chart for protein
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.ylabel('Average Protein (g)')
plt.savefig('visualizations/bar_protein.png', dpi=150)
plt.show()

# Bar chart for carb
sns.barplot(x=avg_macros.index, y=avg_macros['Carbs(g)'])
plt.title('Average Carbs by Diet Type')
plt.ylabel('Average Carbs (g)')
plt.savefig('visualizations/bar_carbs.png', dpi=150)
plt.show()

# Bar chart for fat
sns.barplot(x=avg_macros.index, y=avg_macros['Fat(g)'])
plt.title('Average Fat by Diet Type')
plt.ylabel('Average Fat (g)')
plt.savefig('visualizations/bar_fat.png', dpi=150)
plt.show()

# Heatmap macronutrient content vs diet types
plt.figure(figsize=(10, 6))
sns.heatmap(avg_macros, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=0.5)
plt.title('Heatmap: Average Macronutrient Content by Diet Type')
plt.tight_layout()
plt.savefig('visualizations/heatmap_macros.png', dpi=150)
plt.show()

# Scatter plot  top 5 protein-rich recipes across cuisines
plt.figure(figsize=(12, 8))
sns.scatterplot(data=top_protein, x='Cuisine_type', y='Protein(g)',
                hue='Diet_type', size='Protein(g)',
                sizes=(50, 300), alpha=0.7, palette='Set2')
plt.title('Top 5 Protein Rich Recipes by Cuisine')
plt.xlabel('Cuisine Type')
plt.ylabel('Protein (g)')
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualizations/scatter_top_protein.png', dpi=150)
plt.show()
