import pandas as pd

df = pd.read_csv("MoviesOnStreamingPlatforms.csv")

# Keep only relevant columns
df = df[['Title', 'Year', 'Age', 'Rotten Tomatoes', 'Netflix', 'Hulu', 'Prime Video', 'Disney+']]

# Clean Rotten Tomatoes: '98/100' -> 98
df['Rotten Tomatoes'] = df['Rotten Tomatoes'].str.split('/').str[0].astype(float)

# Ensure streaming columns are integers
for col in ['Netflix','Hulu','Prime Video','Disney+']:
    df[col] = df[col].astype(int)

# Save cleaned CSV
df.to_csv("Movies_clean.csv", index=False)
