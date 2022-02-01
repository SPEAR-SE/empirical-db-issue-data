import pandas as pd

app_list = ['broadleafcommerce', 'metasfresh',  'openfire', 'adempiere', 'dbeaver', 'dotcms', 'openmrs']


def main():
    # import all studied bug issues
    data = pd.read_excel(r'.\studied bug issues.xlsx', 'Sheet1', engine='openpyxl')
    issues_df = pd.DataFrame(data)

    for index_app, app in enumerate(app_list):
        print(app)
        db_issue_df = issues_df[(issues_df["app"] == app) & (issues_df["is_db_bug"] == True) & (issues_df["number_commit_files"] != 0)]
        non_db_issue_df = issues_df[(issues_df['app'] == app) & (issues_df['is_db_bug'] == False) & (issues_df["number_commit_files"] != 0)]

        # unique changed files
        db_files_names_set = set()
        non_db_files_names_set = set()

        db_files_modified_list = db_issue_df['commit_files'].tolist()
        non_db_files_modified_list = non_db_issue_df['commit_files'].tolist()
        # base/src/org/compiere/acct/Doc_Invoice.java:6:8,base/src/org/compiere/model/MCostDetail.java:1:0|base/src/org/compiere/acct/Doc_Invoice.java:6:6,base/src/org/compiere/model/MCostDetail.java:1:1|base/src/org/compiere/model/MCostDetail.java:1:1
        for files_loc_modified_str in db_files_modified_list:
            file_name_set = extract_file_names(files_loc_modified_str)
            db_files_names_set.update(file_name_set)
        for files_loc_modified_str in non_db_files_modified_list:
            file_name_set = extract_file_names(files_loc_modified_str)
            non_db_files_names_set.update(file_name_set)
        union_file_names_set = db_files_names_set.union(non_db_files_names_set)
        intersection_file_names_set = db_files_names_set.intersection(non_db_files_names_set)
        jaccard_similarity = len(intersection_file_names_set) / len(union_file_names_set)
        print('{' + str(len(db_files_names_set)) + '\\\\' + str(len(non_db_files_names_set)) + '}&' + str(len(intersection_file_names_set)) + '&' + '{:.2f}'.format(jaccard_similarity))
        print('------------------------------------------')


def extract_file_names(files_loc_modified_str):
    """

    :param files_loc_modified_str:
    base/src/org/compiere/acct/Doc_Invoice.java:6:8|base/src/org/compiere/model/MCostDetail.java:1:0|base/src/org/compiere/acct/Doc_Invoice.java:6:6,base/src/org/compiere/model/MCostDetail.java:1:1|base/src/org/compiere/model/MCostDetail.java:1:1
    :return:
    """
    file_name_set = set()
    str_array = files_loc_modified_str.split('|')
    if len(str_array) >= 1:
        for str in str_array:
            if str != '':   # common/src/main/java/org/broadleafcommerce/common/payment/service/PaymentGatewayTransactionService.java:3:3||common/src/main/java/org/broadleafcommerce/common/payment/service/FailureCountExposable
                str_array_three = str.split(':')
                if len(str_array_three) != 3:
                    print(files_loc_modified_str)
                    continue
                # assert len(str_array_three) == 3
                file_name_set.add(str_array_three[0])
    return file_name_set


if __name__ == "__main__":
    main()
