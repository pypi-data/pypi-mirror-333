import pandas as pd

def main():
    df_id = get_fsample_id()
    df_id['task_id'] = df_id['task_id'].astype(str)
    df_inner = get_inner_data()
    df_outer = get_external_data()
    df_blz = blz_ar_v1()

    df_inner.drop_duplicates(subset='task_id', keep='first', inplace=True)
    df_outer.drop_duplicates(subset='task_id', keep='first', inplace=True)
    df_blz.drop_duplicates(subset='task_id', keep='first', inplace=True)

    df = pd.merge(df_id, df_inner, on='task_id', how='left')
    df = pd.merge(df, df_outer, on='task_id', how='left')
    df = pd.merge(df, df_blz, on='task_id', how='left')

    return df


def get_fsample_id():
    connection = get_database_connection()
    sql = f"""
    SELECT CAST(credit_task_id AS CHAR) AS task_id
    FROM
        (SELECT *, ROW_NUMBER()OVER(PARTITION BY user_identity_id ORDER BY loan_pay_time ASC) AS rn
        FROM bmd_rc_view.risk_contract_info_view rciv 
        WHERE contract_status > 0
        AND credit_task_id IS NOT NULL
        AND loan_task_id IS NOT NULL)a
    WHERE a.rn = 1
    """
    df = get_data(connection, sql)

    return df


def get_database_connection():
    import pymysql
    username = 'bmd_rc_wangzhiyu'
    password = 'wangzhiyu@bmd'

    db_4000 = pymysql.connect(
        host = '172.16.31.54'
        , port = 4000
        , user = username
        , password = password
        , database = 'bmd_rc_base'
        , autocommit=True  # 启用 autocommit
        , charset = 'utf8'
    )
    return db_4000


def get_data(connection, sql):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            return df
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        connection.close()
    


## 利用合并表取数

def get_inner_data():
    connection = get_database_connection()
    sql_inner_model_data = f"""
    SELECT CAST(credit_task_id AS CHAR) AS task_id, a.* FROM bmd_rc_ana.bmd_rc_model_multiModelScoreMonitor_modelScore_v1 a
    """
    df = get_data(connection, sql_inner_model_data)
    drop_cols = [col for col in df.columns if col.startswith('flag')] + ['credit_task_id']
    df.drop(columns=drop_cols, inplace=True)
    return df


def get_external_data():
    connection = get_database_connection()
    sql_external_data = f"""
    SELECT * FROM bmd_rc_test.bmd_rc_ModelGroup_Result_of_Merging_External_Data_V1
    """
    df = get_data(connection, sql_external_data)
    df.drop(columns=['app_key', 'apply_time'], inplace=True)
    df.rename(columns={'credit_task_id': 'task_id'}, inplace=True)

    return df

def blz_ar_v1():
    connection = get_database_connection()
    sql = f"""
    WITH task_ids AS
    (SELECT task_id FROM bmd_rc_view.risk_credit_apply_view WHERE final_result = 20)
    SELECT CAST(task_ids.task_id AS CHAR) AS task_id, COALESCE(a.probability_1_value, b.pred) AS BLZ_AR_V1
    FROM task_ids
    LEFT JOIN (SELECT task_id, probability_1_value FROM bmd_rc_view.bmd_rc_knowledge_rk_processor_request_log WHERE processor_id = 46)a ON task_ids.task_id = a.task_id
    LEFT JOIN bmd_rc_ana.M148_XGB_BLZ_AR_v1_20241225_ssw b ON CAST(task_ids.task_id AS CHAR) = b.shouxin_task_id 
    """

    df = get_data(connection, sql)
    return df