import pandas as pd;
import matplotlib.pyplot as plt;

df = pd.read_csv("netflix_titles.csv")

print("DATA DESCRIPTION")
print("the first five entries: ",df.head())
print("length of dataset: ", len(df))
print("coloumns in the dataset: ", df.columns)
print("shape of dataset: ", df.shape)
print("datatypes of dataset: ", df.dtypes)

#handling missing values
print("\n HANDLING MISSING VALUES")
missing_val = df.isnull().sum()
print(missing_val[missing_val>0]) 

#data cleaning 

df_copy = df.copy()
print("\nNumber of rows before cleaning: ",len(df_copy))

df_copy = df_copy.dropna(subset = ["title","duration","type","release_year"])

catego_col = ["director","show_id","cast","country","date_added","rating","listed_in","description"]
for col in catego_col:
    df_copy[col] = df_copy[col].fillna("unknown")

#making the relase year between 1900 and 2024
df_copy = df_copy[df_copy['release_year'].between(1900,2024)]

print("\n After cleaning the remaining rows are:", len(df_copy))
print("\n number of rows removed in cleaning is :", len(df) - len(df_copy))

#print(df_copy.isnull().sum())

# #ANALYTICS AND VISUALIZATION 

# #1. Movies vs tv shows 
type_counts = df_copy["type"].value_counts() # movie : 100, tv show : 50 (index : value)
print("number of movies and tv shows: \n",type_counts)

plt.bar(type_counts.index,type_counts.values, color = ["red","blue"])
plt.xlabel("type")
plt.ylabel("count")
plt.title("Movies vs Tv show")
plt.savefig('1.barchart.png')
plt.show()

#2. content rating destribution 
rating_count = df_copy["rating"].value_counts()

plt.pie(rating_count.values, labels = rating_count.index, autopct = "%1.1f%%")
plt.title("content rating distribution")
plt.savefig("2.piechart _rating.png")
plt.show()

#3. release over year 
release_count = df_copy["release_year"].value_counts().sort_index() #1980:3 releases
plt.plot(release_count.index,release_count.values, marker = 'o')
plt.xlabel("release year")
plt.ylabel("number of releases")
plt.title("release over year")

plt.savefig("3.release_over_year.png")
plt.show()

#4. movie durations 
movies = df_copy[df_copy['type'] == 'Movie'].copy()
movies['duration_min'] = movies['duration'].str.extract('(\d+)').astype(int)

plt.hist(movies["duration_min"],bins=20, color = 'red')
plt.title("Movie duration distribution")
plt.xlabel("duration")
plt.ylabel("number of movies")
plt.savefig("4.movie_duration_histogram.png")
plt.show()

#5. top 10 countries with most releases

# Get first country from each title (some have multiple countries)
df_copy['first_country'] = df_copy['country'].str.split(',').str[0].str.strip()
country_counts = df_copy['first_country'].value_counts().head(10)

plt.barh(country_counts.index, country_counts.values, color='red')
plt.title('Top 10 Countries with Most Netflix Content')
plt.xlabel('Number of Titles')
plt.tight_layout()
plt.savefig("5.top_10_country_with_most_releases.png")
plt.show()

#6. Movies vs tv shows over time
movies_by_year = df_copy[df_copy['type'] == 'Movie']['release_year'].value_counts().sort_index()
shows_by_year = df_copy[df_copy['type'] == 'TV Show']['release_year'].value_counts().sort_index()

plt.plot(movies_by_year.index, movies_by_year.values, label='Movies', 
         marker='o', linewidth=2, markersize=4)
plt.plot(shows_by_year.index, shows_by_year.values, label='TV Shows', 
         marker='s', linewidth=2, markersize=4)
plt.title('Movies vs TV Shows Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Titles')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("6.tv_show_vs_movies.png")
plt.show()


