import pandas as pd
import numpy as np
from datetime import datetime


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
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        connection.close()
        
    return df


def load_src_data(table_name, data_src_id, need_colnames):
    sql = f"""
    SELECT a.*, {need_colnames}
    FROM
    (SELECT CAST(task_id AS CHAR) AS task_id, data_src_req_id FROM bmd_rc_base.risk_engine_data_src_map redsm 
    WHERE data_src_id = {data_src_id})a
    LEFT JOIN {table_name} dsi ON a.data_src_req_id = dsi.id
    """
    connection = get_database_connection()
    df = get_data(connection, sql)
    return df



def load_data_from_test(table_name, user_id):
    sql = f"""
    SELECT CAST(rei.champion_task_id AS CHAR) AS champion_task_id, a.*
    FROM {table_name} a
    LEFT JOIN bmd_rc_base.risk_engine_input rei ON CAST(SUBSTRING(a.{user_id}, 3) AS signed) = rei.id
    """
    connection = get_database_connection()
    df = get_data(connection, sql)
    return df


def label_map(df):
    label_map = {'fpd1':'00.fpd1', 'fpd3':'01.fpd3', 'fpd7':'02.fpd7', 'fpd10':'03.fpd10', 'fpd30':'04.fpd30'
                 ,'cpd1':'05.cpd1', 'cpd3':'06.cpd3', 'cpd7':'07.cpd7', 'cpd10':'08.cpd10'
                 ,'spd1':'09.spd1', 'spd3':'10.spd3', 'spd7':'11.spd7', 'spd10':'12.spd10', 'spd30':'13.spd30'
                 ,'tpd30':'14.tpd30'}
    rename_dic = {key: label_map[key] for key in df.columns if key in label_map.keys()}
    df.rename(columns=rename_dic, inplace=True)
    return df


def load_fsample_label(todayIn=False):
    sql = f"""
    WITH contract AS
    (SELECT *
    FROM
            (SELECT *,ROW_NUMBER()OVER(PARTITION BY user_identity_id ORDER BY loan_pay_time ASC) AS rn
            FROM bmd_rc_view.risk_contract_info_view rciv 
            WHERE contract_status > 0
            AND credit_task_id IS NOT NULL
            AND loan_task_id IS NOT NULL)a
    WHERE a.rn = 1)
    SELECT 
    CONCAT('ZD', CAST(rei.id AS CHAR)) AS user_id
    , CAST(rei.champion_task_id AS CHAR)  AS champion_task_id
    , rei.project_id AS channel_id
    , contract.loan_task_id AS loan_task_id
    , rei.input_create_time
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=1 AND first_phase_overdue_days >= 1 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=1 AND first_phase_overdue_days < 1 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<1 THEN NULL END AS fpd1
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=3 AND first_phase_overdue_days >= 3 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=3 AND first_phase_overdue_days < 3 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<3 THEN NULL END AS fpd3
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=7 AND first_phase_overdue_days >= 7 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=7 AND first_phase_overdue_days < 7 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<7 THEN NULL END AS fpd7
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=10 AND first_phase_overdue_days >= 10 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=10 AND first_phase_overdue_days < 10 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<10 THEN NULL END AS fpd10
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=30 AND first_phase_overdue_days >= 30 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=30 AND first_phase_overdue_days < 30 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<30 THEN NULL END AS fpd30
    , CASE WHEN datediff(curdate(), third_phase_repay_date)>=30 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days, third_phase_overdue_days) >= 30 THEN 1
               WHEN datediff(curdate(), third_phase_repay_date)>=30 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days, third_phase_overdue_days) < 30 THEN 0
               WHEN datediff(curdate(), third_phase_repay_date)<30 THEN NULL END AS tpd30
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=1 AND current_overdue_days >= 1 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=1 AND current_overdue_days < 1 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<1 THEN NULL END AS cpd1
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=3 AND current_overdue_days >= 3 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=3 AND current_overdue_days < 3 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<3 THEN NULL END AS cpd3
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=7 AND current_overdue_days >= 7 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=7 AND current_overdue_days < 7 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<7 THEN NULL END AS cpd7
    , CASE WHEN datediff(curdate(), first_phase_repay_date)>=10 AND current_overdue_days >= 10 THEN 1
               WHEN datediff(curdate(), first_phase_repay_date)>=10 AND current_overdue_days < 10 THEN 0
               WHEN datediff(curdate(), first_phase_repay_date)<10 THEN NULL END AS cpd10
    , CASE WHEN datediff(curdate(), second_phase_repay_date)>=1 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) >=1 THEN 1
               WHEN datediff(curdate(), second_phase_repay_date)>=1 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) < 1 THEN 0
               WHEN datediff(curdate(), second_phase_repay_date)<1 THEN NULL END AS spd1
    , CASE WHEN datediff(curdate(), second_phase_repay_date)>=3 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) >=3 THEN 1
               WHEN datediff(curdate(), second_phase_repay_date)>=3 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) < 3 THEN 0
               WHEN datediff(curdate(), second_phase_repay_date)<3 THEN NULL END AS spd3
    , CASE WHEN datediff(curdate(), second_phase_repay_date)>=7 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) >=7 THEN 1
               WHEN datediff(curdate(), second_phase_repay_date)>=7 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) < 7 THEN 0
               WHEN datediff(curdate(), second_phase_repay_date)<7 THEN NULL END AS spd7
    , CASE WHEN datediff(curdate(), second_phase_repay_date)>=10 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) >=10 THEN 1
               WHEN datediff(curdate(), second_phase_repay_date)>=10 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) < 10 THEN 0
               WHEN datediff(curdate(), second_phase_repay_date)<10 THEN NULL END AS spd10
    , CASE WHEN datediff(curdate(), second_phase_repay_date)>=30 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) >=30 THEN 1
               WHEN datediff(curdate(), second_phase_repay_date)>=30 AND GREATEST(first_phase_overdue_days, second_phase_overdue_days) < 30 THEN 0
               WHEN datediff(curdate(), second_phase_repay_date)<30 THEN NULL END AS spd30
    FROM contract
    LEFT JOIN bmd_rc_base.risk_engine_input rei ON contract.credit_task_id = rei.champion_task_id  
    """
    connection = get_database_connection()
    df = get_data(connection, sql)
    df_final = label_map(df)

    today_datetime = datetime.combine(datetime.now().date(), datetime.min.time())

    if todayIn:
        df_end = df_final
    else:
        df_end = df_final[df_final['input_create_time'] < today_datetime].reset_index(drop=True)

    return df_end


def load_data_from_ana(table, need_input_id=False):
    if need_input_id:
        sql = f"""
        SELECT rei.id,  a.*
        FROM {table} a
        LEFT JOIN bmd_rc_base.risk_engine_input rei ON a.task_id = rei.champion_task_id
        """ 
    else:
        sql = f"SELECT * FROM {table}"
    connection = get_database_connection()
    df = get_data(connection, sql)
    return df


def load_model_log_data(model_id):
    sql = f"""
    SELECT CAST(task_id AS CHAR) AS task_id, probability_1_value
    FROM bmd_rc_view.bmd_rc_knowledge_rk_processor_request_log
    WHERE processor_id = {model_id}
    """
    connection = get_database_connection()
    df = get_data(connection, sql)
    return df



## 保存数据表到数据库
def conn_msg(dataset_name):
    from urllib.parse import quote_plus as urlquote
    user, pswd = 'bmd_rc_wangzhiyu', 'wangzhiyu@bmd'
    db_msg = ['172.16.31.54', 4000, dataset_name]
    host, port, db = db_msg
    
    return "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4&autocommit=true".format(user, urlquote(pswd), host, port, db)

def upload_data_to_database(df, table_name, db_name):
    pd.io.sql.to_sql(df, table_name, con=conn_msg(db_name), if_exists='replace',index=False)
    
    return 'Your data is uploaded!'