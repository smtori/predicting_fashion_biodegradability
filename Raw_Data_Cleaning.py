"""

Fashion Textile Sustainability Project
Data Source: https://zenodo.org/records/4261101
DOI: https://doi.org/10.5281/zenodo.4261101

"""
import pandas as pd 
import altair as alt

items_path = "/Users/torismith/Desktop/DS2500/Project Files/zara_items_english.csv"
composition_path = "/Users/torismith/Desktop/DS2500/Project Files/zara_composition_english.csv"
df_items = pd.read_csv(items_path)
df_composition = pd.read_csv(composition_path)

# sort df_items by item_code, ascending
df_items = df_items.sort_values(by="item_code")

# Join data frames on item_code
merged_df = pd.merge(df_items, df_composition, on="item_code", how="inner")
merged_df.dtypes
"""
merged_df column headers and data types:
item_code           int64
item_name          object
price              object
eco_tagged         object
eco_label          object
eco_description    object
description        object
garment_part       object
material           object
composition         int64
"""


# Categorize fabrics by type
def categorize_material(textile_data):
    """
    Categorizes textiles as either natural, synthetic, or semi-synthetic based on composition. 
    Parameter: textile_data, df with material column
    Return: df with updated column
    """
    # Synthetic materials
    synthetic_material = {
        "Polyester",
        "Elastane (Spandex)",
        "Viscose (Rayon)",
        "Polyamide (Nylon)",
        "Lyocell (Tencel)",
        "Nylon",
        "Acrylic",
        "Metallic Fiber"
    }
    # Natural materials
    natural_material = {
        "Cotton",
        "Linen",
        "Wool",
        "Camel Hair"
    }
    # Semi synthetic material
    semi_synthetic_material = {
        "Modal",
        "Cupro"
    }
    def categorize(material):
        if material in synthetic_material:
            return "Synthetic"
        elif material in natural_material:
            return "Natural"
        elif material in semi_synthetic_material:
            return "Semi-Synthetic"
        else:
            return "Unknown"

    textile_data["material_category"] = textile_data["material"].apply(categorize)

    return textile_data

# Update dataframe with categorized materials 
df = categorize_material(merged_df)

# Drop unnecessary columns:
df = df.drop(columns=['eco_tagged', 'eco_label', 'eco_description', 'description', 'garment_part'])

df = df.drop_duplicates()
 
# Define which materials are natural
natural_materials = ['Cotton', 'Linen', 'Wool', 'Camel Hair']
 
# Tag each row as natural or not
df['is_natural'] = df['material'].isin(natural_materials)
 
# For each item, sum up natural % and synthetic %
item_natural = df.groupby('item_code').apply(
    lambda g: g.loc[g['is_natural'], 'composition'].sum()
).reset_index(name='natural_pct')
 
item_synthetic = df.groupby('item_code').apply(
    lambda g: g.loc[~g['is_natural'], 'composition'].sum()
).reset_index(name='synthetic_pct')
 
item_stats = item_natural.merge(item_synthetic, on='item_code')
 
 
# Assign 4-category label based on natural vs synthetic ratio
def assign_category(row):
    nat = row['natural_pct']
    syn = row['synthetic_pct']
    total = nat + syn
    if total == 0:
        return 'Synthetic'
    nat_ratio = nat / total
    if nat_ratio == 1.0:
        return 'Natural'
    elif nat_ratio == 0.0:
        return 'Synthetic'
    elif nat_ratio >= 0.5:
        return 'Blend - Mostly Natural'
    else:
        return 'Blend - Mostly Synthetic'
 
 
item_stats['material_category'] = item_stats.apply(assign_category, axis=1)
 
# Pivot each unique material becomes a column, values are composition %
composition_matrix = df.pivot_table(
    index='item_code',
    columns='material',
    values='composition',
    aggfunc='sum',
    fill_value=0
)
 
# Bring back item name and price
meta = df.groupby('item_code')[['item_name', 'price']].first().reset_index()
result = meta.merge(composition_matrix, on='item_code')
 
# Attach the new 4-category label
result = result.merge(item_stats[['item_code', 'material_category']], on='item_code')
 
# Summary
print("Category distribution:")
print(result['material_category'].value_counts())
print(f"\nFinal shape: {result.shape}")
 
# Save
result.to_csv("/Users/torismith/Desktop/DS2500/zara_knn_ready_4cat.csv", index=False)
print("\nSaved to zara_knn_ready_4cat.csv")

