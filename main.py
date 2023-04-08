import requests as req
import pandas as pd


def get_data():
    url = "https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json"
    resp = req.get(url)
    data = resp.json()['Infogempa']['gempa']
    df = pd.DataFrame(data)
    return df


def read_before():
    before = pd.read_csv('gempa.csv')
    return before


def get_and_combine():
    new = get_data()
    before = read_before()

    # combine dataframe
    final = pd.concat([new, before]).reset_index(drop=True)

    # change column format
    final['DateTime'] = pd.to_datetime(
        final['DateTime'], format='%Y-%m-%d %H:%M:%S.%f')

    # sort dataframe
    final = final.sort_values(by=['DateTime'], ascending=[False])

    # drop duplicates
    final = final.drop_duplicates('DateTime')

    # save dataframe to csv
    final.to_csv("gempa.csv", index=False)


def main():
    get_and_combine()


if __name__ == "__main__":
    main()
