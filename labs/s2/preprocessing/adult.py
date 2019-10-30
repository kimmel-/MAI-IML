import pandas as pd
import matplotlib.pyplot as plt

from utils.dataset import read_dataset

import os


def preprocess():
    dataset = read_dataset('adult')
    data = dataset['data']

    df = pd.DataFrame(data)
    y = df['class'].copy()
    df = df.drop(columns=['class'])
    df = df.applymap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

    categorical_features = ['workclass', 'education', 'marital-status', 'occupation',
                            'relationship', 'race', 'sex', 'native-country']

    numerical_features = ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']

    # ### Check missing values

    missing = df.isnull().sum()
    missing_rows = df.isnull().any(axis=1).sum()

    percent_missing = 100 * missing.sum() / (df.shape[0] * df.shape[1])
    percent_missing_rows = 100 * missing_rows / df.shape[0]

    print(missing, '\n')
    print(f'Missing values:           {percent_missing:.4}% ({missing.sum()}/{(df.shape[0] * df.shape[1])})')
    print(f'Rows with missing values: {percent_missing_rows:.4f}% ({missing_rows}/{df.shape[0]})')

    # The dataset `adult` has a few missing values in three categorical attributes: `workclass`, `occupation` and `native-country`. There are several ways to deal with missing values for categorical attributes:
    # 
    # 1. **Deletion: Remove rows containing missing values**
    # 
    # Given huge datasets, if the number of missing values is small, the simplest action to perform is to remove rows which contain some of these. Remove data leads to lose of information, but if the percentage is so small, we are adding just some negligible bias. In fact, this is our case, where we would delete just 7.5% of the rows. Despite of being a small percentage, it may not be negligible, so we will also consider other methods.
    # 
    # **2. Deletion: Remove columns with > 75% missing values**
    # 
    # If a column (or attribute) has almost none of its values, we can consider that information as 'useless', as creating syntetically most of the values from a small unrepresentative set will probably lead us to worse results than just dropping that attribute. We can forget about this method, as the column with more NAs has just a 5.7307% of missing values.
    # 
    # **2. K-NN Imputation**
    # 
    # For imputing categorical variables, we can use a neighbours algorithm, computing with a *distance function* the K-th more similar rows and inputing what the majority of these K rows has in that attribute.
    # 
    # We will select this one

    # ### Outliers

    # Before normalizing or standarizing the numerical data we must check the possible presence of outliers. *E.g.* If we don't do this analysis, when calculating the mean and std to standarize we may have into account it may appear shifted due to some points that differ significantly from the distribution.

    f, ax = plt.subplots(3, 2, figsize=(15, 10))

    df.boxplot('age', ax=ax[0][0])
    df.boxplot('fnlwgt', ax=ax[0][1])
    df.boxplot('education-num', ax=ax[1][0])
    df.boxplot('capital-gain', ax=ax[1][1])
    df.boxplot('capital-loss', ax=ax[2][0])
    df.boxplot('hours-per-week', ax=ax[2][1])

    plt.show()

    # ### Categorical Attributes

    # The categorical attributes are:
    # - workclass
    # - education
    # - marital-status
    # - ocupation
    # - relationship
    # - race
    # - sex
    # - native-country

    for feat in categorical_features:
        print(f'{feat:14} has {len(df[feat].unique()):2} unique values')

    from sklearn.preprocessing import OneHotEncoder

    ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)
    X_categorical = ohe.fit_transform(df[categorical_features])

    columns = ohe.get_feature_names(input_features=categorical_features)
    X_categorical = pd.DataFrame(data=X_categorical, columns=columns)

    X_categorical.head()

    # ### Numerical Attributes

    # The numerical features are.
    # - age
    # - fnlwgt
    # - education-num
    # - capital-gain
    # - capital-loss
    # - hours-per-week

    for feat in numerical_features:
        print(f'Range({feat}) in [{df[feat].min()}, {df[feat].max()}]')

    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    X_numerical = scaler.fit_transform(df[numerical_features])

    X_numerical = pd.DataFrame(data=X_numerical, columns=numerical_features)

    X_numerical.head()

    X_df_enc = pd.concat((X_categorical, X_numerical), axis=1)
    X_df = pd.concat((df[categorical_features], X_numerical), axis=1)

    X_df.head()

    with open(os.path.join('datasets', 'adult-clean_enc.csv'), mode='w') as f:
        X_df_enc.to_csv(f, index=False)

    with open(os.path.join('datasets', 'adult-clean.csv'), mode='w') as f:
        X_df.to_csv(f, index=False)

    with open(os.path.join('datasets', 'adult-clean-y.csv'), mode='w') as f:
        y.to_csv(f, index=False)

    return 'adult-clean.csv', 'adult-clean_enc.csv', 'adult-clean-y.csv'