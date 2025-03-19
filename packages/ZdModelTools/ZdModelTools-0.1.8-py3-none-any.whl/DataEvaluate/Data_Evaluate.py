import pandas as pd
from .Evaluate_Tools import *


class evaluator:
    def __init__(self, df, label_cols=['fpd10'], score_cols=['score1'], month_col='input_month', project_col='channel_id'):
        self.df = df
        self.label_cols = label_cols
        self.month_col = month_col
        self.score_cols = score_cols
        self.project_col = project_col


    def auc_ks_byMonth(self):
        df = self.df.copy()
        result = []
        for y in self.label_cols:
            for score in self.score_cols:
                select_content = (df[y].notnull())&(df[score].notnull())
                for m, m_data in df.loc[select_content, [score, y, self.month_col]].groupby(self.month_col):
                    auc, ks = get_auc_ks(m_data[y], m_data[score])
                    result.append([y, score, m, len(m_data), m_data[y].sum(), m_data[y].mean(), auc, ks])
        
        result = pd.DataFrame(result, columns=['label','score','month','total','bad','bad%','auc','ks'])
        return result
    
    def auc_ks_byProject(self, after_month):
        df = self.df[self.df[self.month_col] > after_month].copy()
        result = []
        for y in self.label_cols:
            for score in self.score_cols:
                select_content = (df[y].notnull())&(df[score].notnull())
                for m, m_data in df.loc[select_content, [score, y, self.project_col]].groupby(self.project_col):
                    auc, ks = get_auc_ks(m_data[y], m_data[score])
                    result.append([y, score, m, len(m_data), m_data[y].sum(), m_data[y].mean(), auc, ks])

        result = pd.DataFrame(result, columns=['label','score','project','total','bad','bad%','auc','ks'])
        return result


    def binned_lift_byMonth(self, q=10, invalid_list=[0, -1,-2,-3,7777,8888,9999]):
        df = self.df.copy()
        group_list = df[self.month_col].unique().tolist()
        result = pd.DataFrame()
        for y in self.label_cols:
            for col in self.score_cols:
                base_bins, bins_mapping = get_base_bins2(df, col, q, invalid_list)
                for g in group_list:
                    res = feature_binned_one_period(df.loc[df[self.month_col] == g, [col, y]], col, y, base_bins, bins_mapping, invalid_list)
                    res.insert(0, 'month', g)
                    res.insert(0, 'score', col)
                    res.insert(0, 'label', y)

                    result = pd.concat([result, res], axis=0, ignore_index=True)
        return result


    def binned_lift_byProject(self, after_month, q=10, invalid_list=[0, -1,-2,-3,7777,8888,9999]):
        df = self.df[self.df[self.month_col] > after_month].copy()
        group_list = df[self.project_col].unique().tolist()
        result = pd.DataFrame()
        for y in self.label_cols:
            for col in self.score_cols:
                base_bins, bins_mapping = get_base_bins2(df, col, q, invalid_list)
                for g in group_list:
                    res = feature_binned_one_period(df.loc[df[self.project_col] == g, [col, y]], col, y, base_bins, bins_mapping, invalid_list)
                    res.insert(0, 'project', g)
                    res.insert(0, 'score', col)
                    res.insert(0, 'label', y)

                    result = pd.concat([result, res], axis=0, ignore_index=True)
        return result


    def get_psi(self, base_month_list):
        df = self.df.copy()
        psi_result = pd.DataFrame()
        for score in self.score_cols:
            base_list = df.loc[df[self.month_col].isin(base_month_list), score]
            psi_temp = pd.DataFrame()
            psi_list = ['psi']
            test_month_list = sorted(df[self.month_col].unique().tolist())
            for month_name in test_month_list:
                test_list = df.loc[df[self.month_col]==month_name, score]
                res_temp = calculate_sample_psi_df(base_list, test_list, score, month_name)
                if psi_temp.empty:
                    psi_temp = res_temp[['base_bins',f'{month_name}_percentage']].copy()
                    psi_list.append(res_temp[f'{month_name}_psi'].sum())
                else:
                    psi_temp = pd.concat([psi_temp, res_temp[[f'{month_name}_percentage']]], axis=1)
                    psi_list.append(res_temp[f'{month_name}_psi'].sum())
            psi_list = pd.DataFrame(psi_list).T
            psi_list.columns = psi_temp.columns
            psi_temp = pd.concat([psi_temp, psi_list], axis=0, ignore_index=True)
            psi_temp.insert(0, 'score', score)
            psi_result = pd.concat([psi_result, psi_temp], axis=0, ignore_index=True)

        return(psi_result)


    def get_correlation(self, df_inner_scores, id_col):
        df = self.df.copy()
        try:
            df = pd.merge(df, df_inner_scores, left_on='champion_task_id', right_on=id_col, how='left')
        except:
            df = pd.merge(df, df_inner_scores, left_on='task_id', right_on=id_col, how='left')
        inner_scores = df_inner_scores.columns.tolist()[1:]
        corr_result = df.loc[df[self.month_col]>'2024-07', self.score_cols + inner_scores].corr()

        return(corr_result)




if __name__ == '__main__':
    df = pd.DataFrame({'A':[0,1,1,0,0,0,1], 
                       'B':[0.23, 0.59, 0.79,0.30,0.29,0.19,0.86], 
                       'C':['2024-01','2024-02','2024-03','2024-01','2024-02','2024-03','2024-01']})
    eva = evaluator(df, ['A'], ['B'], 'C')
    print(eva.auc_ks_byMonth())