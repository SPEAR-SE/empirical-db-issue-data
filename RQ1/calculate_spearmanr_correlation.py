import pandas as pd
import maya
import matplotlib.pyplot as plt
from dateutil.relativedelta import *
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import statistics
from pandas.plotting import register_matplotlib_converters

app_list = ['broadleafcommerce', 'metasfresh',  'openfire', 'adempiere', 'dbeaver', 'dotcms', 'openmrs']


def main():
    # import all studied bug issues
    data = pd.read_excel(r'.\studied bug issues.xlsx', 'Sheet1', engine='openpyxl')
    issues_df = pd.DataFrame(data)

    for app in app_list:
        print(app)
        all_issues_df = issues_df[issues_df["app"] == app]
        create_time_list_db = list()
        create_time_list_non_db = list()
        for index, row in all_issues_df.iterrows():
            is_db_bug = row["is_db_bug"]
            created_at = maya.parse(row["created_at"]).datetime()
            assert is_db_bug in [True, False]

            if is_db_bug is True:
                create_time_list_db.append(created_at)
            elif is_db_bug is False:
                create_time_list_non_db.append(created_at)

        # calculate the spearman at different intervals
        mean_correlation_intervals = 'correlation:'
        for interval in [3, 6]:
            mean_frequency_db, corr_spearman = calculate_corr_spearman(create_time_list_db, create_time_list_non_db, interval)
            mean_correlation_intervals += ('&{:.1f}'.format(corr_spearman))
        print(mean_correlation_intervals)


def calculate_corr_spearman(create_time_list_db, create_time_list_non_db, interval):
    # get the range of studied period
    start_time = min(min(create_time_list_db), min(create_time_list_non_db))
    end_time = max(max(create_time_list_db), max(create_time_list_non_db))

    # set the day with 1
    start_time = start_time.replace(day=1, hour=0, minute=0, second=0)
    end_time = end_time.replace(day=1, hour=0, minute=0, second=0)
    # print(start_time)
    # print(end_time)

    frequency_db = get_frequency(create_time_list_db, start_time, end_time, interval)
    frequency_non_db = get_frequency(create_time_list_non_db, start_time, end_time, interval)
    # print(frequency_db)
    # print(len(frequency_db))
    # print(frequency_non_db)
    # print(len(frequency_non_db))
    corr_pearson, _ = pearsonr(frequency_db, frequency_non_db)
    corr_spearman, _ = spearmanr(frequency_db, frequency_non_db)
    return statistics.mean(frequency_db), corr_spearman


def get_frequency(create_time_list, start_time, end_time, interval):
    """
    get frequency according to breaks
    :param create_time_list:
    :param start_time:
    :param end_time:
    :param interval:
    :return:
    """
    bins = list()
    data_time_breaks_list = get_breaks_time(start_time, end_time, interval)
    for break_time_point in data_time_breaks_list:
        bins.append(break_time_point.toordinal())
    [n, bins, patches] = plt.hist(create_time_list, bins=bins, edgecolor='k', alpha=0.35)
    # print(n)
    # print(bins)
    return n


def get_breaks_time(start_time, end_time, month_number):
    """
    get sequence of time period
    :param start_time: 2013-04-01
    :param end_time: 2016-01-01
    :param month_number: number of month, 1, 2, ...
    :return:
    """
    # use_date = use_date + datetime.timedelta(minutes=+10)
    # use_date = use_date + datetime.timedelta(hours=+1)
    # use_date = use_date + datetime.timedelta(days=+1)
    # use_date = use_date + datetime.timedelta(weeks=+1)
    result_list = list()
    result_list.append(start_time)
    iterator_time = start_time
    while iterator_time < end_time:
        iterator_time = iterator_time + relativedelta(months=+month_number)
        result_list.append(iterator_time)
    return result_list


if __name__ == "__main__":
    register_matplotlib_converters()
    main()

    
