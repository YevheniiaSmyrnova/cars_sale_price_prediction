from sklearn import linear_model
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd


def clean_data(input_file):
    df = pd.read_csv(input_file)

    unnecessary_columns = [u'dateCrawled', u'name', u'monthOfRegistration',
                           u'dateCreated', u'nrOfPictures',
                           u'postalCode', u'lastSeen']
    df = df.drop(unnecessary_columns, axis=1)
    df = df.dropna()

    df = df.loc[df.price < 100000]
    df = df.loc[df.price > 100]

    df = pd.get_dummies(df)
    return df


def normalize_data(df):
    for column in df.columns:
        df[column] = (df[column] - df[column].mean()) / df[column].std()
    return df


def plot(x, y, xlabel, ylabel='price (USD)'):
    plt.scatter(x, y,  color='black')
    plt.title('How the {} depends on the {}'. format(ylabel, xlabel))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(xlabel.replace(' ', '_'))
    plt.close()


def main():
    input_file = "autos.csv"
    df = clean_data(input_file)

    # print df[df.columns[1:-1]].apply(lambda x: x.corr(df['price']))

    # df = normalize_data(df)

    x_train, x_test, y_train, y_test = train_test_split(
        df.drop('price', axis=1), df['price'], test_size=0.2, random_state=42)

    reg = linear_model.Ridge(alpha=1.0)
    reg.fit(x_train, y_train)

    y_pred = reg.predict(x_test)

    print r2_score(y_test, y_pred)

    plot(x_test.yearOfRegistration, y_test, 'year of registration')
    plot(x_test.kilometer, y_test, 'distance km')
    plot(x_test.powerPS, y_test, 'power PS')

if __name__ == '__main__':
    main()
