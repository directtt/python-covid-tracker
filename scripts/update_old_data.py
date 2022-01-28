import pandas as pd
import os
from summary import update_complete_data
from today import parse_data


if __name__ == '__main__':
    filenames = os.listdir('../danehistorycznewojewodztwa')

    for filename in filenames[-50:]:
        complete_data = pd.read_csv('../datasets/complete_data.csv')
        df = parse_data('../danehistorycznewojewodztwa/' + filename).iloc[0, 1:]

        if df['stan_rekordu_na'] not in complete_data['date'].tolist():
            update_complete_data(complete_data, df)
