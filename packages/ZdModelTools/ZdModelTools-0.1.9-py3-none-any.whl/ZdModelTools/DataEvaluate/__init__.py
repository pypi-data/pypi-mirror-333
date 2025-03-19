from .Data_Evaluate import *
from .load_inner_score_log_result import main as load_main
import pandas as pd
# from .config import config


def save_eval_result(output_path, df, label_cols, score_cols, month_col, projec_col):
    eval_v1 = evaluator(df, label_cols, score_cols, month_col, projec_col)
    eval_result_dict = get_all_eval_result(eval_v1)
    ## 若保存不成功，会print failed
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for key in eval_result_dict:
            try:
                eval_result_dict[key].to_excel(writer, sheet_name=key, index=False)
            except:
                print(f"File '{key}' failed to save!")


def get_all_eval_result(evaluator):
    eval_result_dict = {}
    eval_result_names = [
    'auc_ks_byMonth',
    'auc_ks_byProject',
    'binned_byMonth',
    'binned_byPorject',
    'psi',
    'correlation',
    ]
        
    for key in eval_result_names:
        try:
            eval_temp = get_one_eval_result(evaluator, key)
            eval_result_dict[key] = eval_temp
            print(f'{key} is finished')
        except:
            print(f'{key} is calculated failed')

    return eval_result_dict


def get_one_eval_result(evaluator, name):
    if name == 'auc_ks_byMonth':
        evaluate_result = evaluator.auc_ks_byMonth()
    elif name == 'auc_ks_byProject':
        evaluate_result = evaluator.auc_ks_byProject(after_month='2024-07')
    elif name == 'binned_byMonth':
        evaluate_result = evaluator.binned_lift_byMonth()
    elif name == 'binned_byPorject':
        evaluate_result = evaluator.binned_lift_byProject(after_month='2024-07')
    elif name == 'psi':
        evaluate_result = evaluator.get_psi(base_month_list= ['2024-10','2024-11','2024-09','2024-12'])
    elif name == 'correlation':
        df_inner_scores = load_main()
        evaluate_result = evaluator.get_correlation(df_inner_scores, 'task_id')
    else:
        evaluate_result = pd.DataFrame()
    return evaluate_result

