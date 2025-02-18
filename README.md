# The recipe for a successful 
**Link for the data story:** [https://ferioliste.github.io/theblockbusters-datastory/](https://ferioliste.github.io/theblockbusters-datastory/)

### Abstract
The goal of this project is to explore the factors that contribute to a film's success. First, we argue what success really means in the context of the film industry, considering multiple dimensions such as the box office revenue, the critical acclaim, and the ROI. We then examine a range of factors that may influence these success metrics, including genres, casts' composition, production companies and country of origin. In some cases go beyond simple correlation and establish causal relationships between these factors and movie success. This approach helps us identify elements that truly impact a film’s performance rather than coincidental associations. Finally, we consolidate our findings into two comprehensive models that illustrate how different aspects contribute together to a film's success.
<br><br>

### Research questions
**Main research question:** What factors contribute to the success of a movie?

**Sub-questions:**
- How do we measure success? Is box-office the only metric? Are different metrics correlated?
- Are there countries that produce more successful movies? Are there countries that have an advantage?
- Does the genre of a movie impact its performance? What are the most successful genres?
- How the cast impact the success of a movie? Does the age the actors impact the success of a movie? Does the diversity within the cast influence a movie's success? Do renowned actors and directors contribute positively to a film's success?
- How much does the movie budget impact its overall performance? How important is the production company?
<br><br>

### Conclusions
- Among all the explored metrics to measure success, the most promising and reliable is the so-called 'popularity'. This metric is defined as the logarithm of the number of votes a movie received. We choose to take the logarithms since we are more interested in the order of magnitude of the number of reviews. 'Popularity' works as a metric for success, not only because there is a lot of available data, but also because we were able to establish significant correlations with both revenues and rating.
- The composition of the cast influences a movie's success. Multiculturality within the cast (actors originating from different countries) and cast fame both exhibit positive correlations with popularity. This suggests that diverse and renowned casts contribute to increasing a film’s reach and appeal.
- Genre plays a key role in shaping a film’s popularity. Widely appreciated genres like horror, thriller, or sci-fi tend to attract  a larger audience. Conversely, more niche or sophisticated genres, such as music or historical films, generally receive fewer reviews and exhibit lower popularity.
- The country of production does impact on a movie's success. Using a propensity score approach, we established causality between a movie's success and U.S. production. Films produced in the United States consistently achieve higher visibility and engagement compared to those from other countries.
- Finally, both production company and budget have high explanatory power for a movie's popularity.
<br><br>

### Additional datasets
We incorporated data from three additional sources

#### 1. The Movie Database (TMDB)
- **Description:** Provides movie metadata, including revenue, budget, genres and additional attributes.
- **Source:** Downloaded from [Kaggle](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies).
- **Size:** Approximately 1.07 million entries, manageable within memory.

#### 2. Internet Movie Database (IMDB)
- **Description:** Offers comprehensive film attributes such as ratings, number of ratings, genres. In addition, it provides detailed information about the cast, including actor names, roles, and the order of importance within the film.
- **Source:** Obtained from [IMDB Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/).
- **Size:** The entire dataset is too large to fit into memory. To handle the dataset, we have loaded each part individually and filtered out all the non-movie entries before continuing processing the data. This process ensured that we could work agily with the dataset. The code utilized is contained in the notebook `src/scripts/imbd_dataset_filtering.ipynb`.

#### 3. Wikidata
- **Description:** We wrote a script that utilizes the [Wikidata Query Service](https://query.wikidata.org/) to automatically retrieve extensive information about movies, casts, and related people. The code utilized is contained in the notebook `src/scripts/scrape_wikidata.ipynb`.
- **Integration:** This dataset enhances our analysis with additional movies' and people's metadata and identifier mappings.

#### Combining the datasets
We have combined these datasets into a unified dataset. The complete integration code is available in the `src/scripts` folder of the repository.
<br><br>

### Methods
**Statistical Tests**: We use a variety of statistical tests to assess whether different groups exhibit significantly distinct properties. This includes independence tests, Z-tests for comparing group averages. These tests help determine if certain film characteristics are associated with higher success metrics.

**Regression Analysis**: We use logistic regression for predictive modelling and interpretation. This helps assess and quantify the impact of the different aspects of a movie on its success.

**Decision Trees**: We use a decision tree in order to get an intuitive, easy-to-interpret picture of how different factors interact and contribute to a movie’s success. In our case, we use one to predict high or low popularity.

**Data Visualization**: We interpret plots and try to extrapolate trends, variability, and potential outliers. When relevant, we pay particular attention to error bars and uncertainty in the data.

**Causal analysis**: When considering the movies produced in the USA and not, we compute the propensity scores and use them to control for confounding factors.
<br><br>

### Roles within the team

**Stefano**: Data integration and cleaning, analysis on genres and countries, datastory

**Luca**: Analysis on production companies, datastory

**Hugo**: Decision tree model, overall OLS model, in depth overall check

**Mouhamad**: Exploratory data analysis, analysis on cast and genres, in depth overall check

**Francesco**: Exploratory data analysis, analysis of success metrics, results merging
