import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve


def bool2result(bool_value):
    if bool_value:
        result = '越大越好'
    else:
        result = '越大越坏'
    return result



def get_auc_ks(y_true, y_pred):
    try:
        auc = roc_auc_score(y_true, y_pred)
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        ks = max(abs(tpr - fpr))
    except:
        auc = np.nan
        ks = np.nan

    return [auc, ks]


# ---------------------------------------------------------------------------------------

def get_bins_lift(df, groupby_col, label, mapping):
    res = df.groupby(groupby_col).agg(
        total=(label, 'count'),
        bad=(label, 'sum')
    ).reset_index()
    
    res['bad%'] = res['bad'] / res['total']
    res['t/sum.t'] = res['total'] / res['total'].sum()
    res['lift'] = res['bad%'] / (res['bad'].sum() / res['total'].sum())
    
    res['bins_index'] = res[groupby_col].apply(lambda x: mapping.get(str(x), '0'))
    
    return res


def get_base_bins2(df, col, q, invalid_list):
    valid_data = df.loc[~df[col].isin(invalid_list), col]

    if valid_data.nunique() < 10:
        return 0, {}
    
    bins = pd.qcut(valid_data, q=q, retbins=True, duplicates='drop')[1]
    intervals = pd.cut(df[col], bins=bins, include_lowest=True).astype(str).unique()
    intervals = [interval for interval in intervals if interval != 'nan']
    
    sorted_intervals = sorted(intervals, key=lambda x: float(x.strip('()').split(',')[0]))
    bins_mapping = {interval: str(idx + 1).zfill(2) for idx, interval in enumerate(sorted_intervals)}
    
    return bins, bins_mapping


# def get_base_bins2(df, col, q, invalid_list):
#     valid_data = df.loc[~df[col].isin(invalid_list), col]

#     if valid_data.nunique() < 10:
#         return 0, {}

#     bins = pd.qcut(valid_data, q=q, retbins=True, duplicates='drop')[1]
#     df['bins'] = pd.cut(df[col], bins=bins, include_lowest=True)
#     intervals = [interval for interval in df['bins'].astype(str).unique() if interval != 'nan']
#     sorted_intervals = sorted(intervals, key=get_left_endpoint)
#     bins_mapping = {interval: str(idx + 1).zfill(2) for idx, interval in enumerate(sorted_intervals)}

#     return bins, bins_mapping

# def get_left_endpoint(interval):
#     return float(interval.strip('()').split(',')[0])


def feature_binned_one_period(df, col, label, base_bins, bins_mapping, invalid_list):
    df_invalid = df[df[col].isin(invalid_list)].copy()
    df_miss = df[df[col].isnull()].copy()
    df_valid = df[(df[col].notnull()) & (~df[col].isin(invalid_list))].copy()
    
    if isinstance(base_bins, int):
        df_valid['bins'] = df_valid[col].astype(str)
        bins_mapping = {str(x): str(int(float(x))).zfill(2) for x in df_valid['bins'].unique()}
    else:
        df_valid['bins'] = pd.cut(df_valid[col], bins=base_bins, include_lowest=True)
    
    # 合并无效值和缺失值
    if not df_invalid.empty:
        df_invalid['bins'] = df_invalid[col].astype(str)
        df_valid = pd.concat([df_valid, df_invalid], ignore_index=True)
        bins_mapping.update({str(x): str(x).zfill(2) for x in invalid_list})
    
    if not df_miss.empty:
        df_miss['bins'] = '-99999'
        df_valid = pd.concat([df_valid, df_miss], ignore_index=True)
        bins_mapping['-99999'] = '99'
    
    # 计算统计指标并排序
    res = get_bins_lift(df_valid, 'bins', label, bins_mapping)
    res.sort_values(by='bins_index', inplace=True)
    res['bins_sorted'] = res['bins_index'].astype(str) + '.' + res['bins'].astype(str)
    
    return res

# def feature_binned_one_period(df, col, label, base_bins, bins_mapping, invalid_list):
#     df_invalid = df[df[col].isin(invalid_list)].copy()
#     df_miss = df[df[col].isnull()].copy()
#     df_t = df[(df[col].notnull())&(~df[col].isin(invalid_list))].copy()

#     if isinstance(base_bins, int):
#         df_t['bins'] = df_t[col].astype(str)
#         bins_mapping = {x: str(int(float(x))).zfill(2) for x in df_t['bins'].unique().tolist()}
#     else:
#         df_t['bins'] = pd.cut(df_t[col], bins=base_bins, include_lowest=True)
#         # temp = list(df_t['bins'].astype(str).unique())
#         # sorted_temp = sorted(temp, key=get_left_endpoint)
#         # bins_mapping = {interval: str(idx+1).zfill(2) for idx, interval in enumerate(sorted_temp)}

#     if len(df_invalid) > 0:
#         df_invalid['bins'] = df_invalid[col].astype(int).astype(str)
#         df_t = pd.concat([df_t, df_invalid], axis=0, ignore_index=True)
#         for x in invalid_list:
#             bins_mapping[str(x)] = str(x).zfill(2)

#     if len(df_miss) > 0:
#         df_miss['bins'] = '-99999'
#         df_t = pd.concat([df_t, df_miss], axis=0, ignore_index=True)
#         bins_mapping['-99999'] = '99'
#     res = get_bins_lift(df_t, 'bins', label, bins_mapping)
#     res.sort_values(by='bins_index', inplace=True)
#     res['bins2'] = res['bins_index'].astype(str) + '.' + res['bins'].astype(str)
#     return res


# ======================================================psi=====================================================================
def calculate_bins_psi(sample_count_df, base_col, test_col):
    the_df = sample_count_df.copy()
    # print(the_df.shape)
    for i in range(the_df.shape[0]):
        if the_df.loc[i, test_col] == 0:
            the_df.loc[i, test_col] = 0.000001
        if the_df.loc[i, base_col] == 0:
            the_df.loc[i, base_col] = 0.000001
    psi_name = test_col[:7] + '_psi'
    the_df[psi_name] = (the_df[test_col] - the_df[base_col]) * np.log(the_df[test_col] / the_df[base_col])
    sample_count_df = pd.concat([sample_count_df, the_df[psi_name]], axis=1)
    return sample_count_df

def calculate_sample_counts(df, group_col, score_col, missing_count, res_prefix):
    res = df.groupby(group_col).agg(count=(score_col, 'count')).reset_index()
    res = pd.concat([res, pd.DataFrame([['-99999', missing_count]], columns=['bins', 'count'])], axis=0)
    res['percentage'] = res['count'] / res['count'].sum()
    res = res.add_prefix(res_prefix)
    return res


def calculate_sample_psi_df(base_list, test_list, score_name, test_name, bins=10):
    base_df = pd.DataFrame(base_list).reset_index(drop=True)
    test_df = pd.DataFrame(test_list).reset_index(drop=True)
    min_value = min(base_list.min(), test_list.min())
    max_value = max(base_list.max(), test_list.max())

    _, base_bins = pd.qcut(base_df[score_name], q=bins, retbins=True, duplicates='drop')
    if min_value < base_bins[0]:
        base_bins.put([0], [min_value])
    if max_value > base_bins[-1]:
        base_bins.put([-1], [max_value])

    base_missing_count = base_df[score_name].isnull().sum()
    test_missing_count = test_df[score_name].isnull().sum()

    base_df['bins'] = pd.cut(base_df[score_name], bins=base_bins, include_lowest=True)
    test_df['bins'] = pd.cut(test_df[score_name], bins=base_bins, include_lowest=True)

    res1 = calculate_sample_counts(base_df, 'bins', score_name, base_missing_count, 'base_')
    res2 = calculate_sample_counts(test_df, 'bins', score_name, test_missing_count, test_name + '_')
    res = pd.concat([res1, res2.iloc[:, 1:]], axis=1).reset_index(drop=True)
    res_final = calculate_bins_psi(res, 'base_percentage', f"{test_name}_percentage")
    return res_final
