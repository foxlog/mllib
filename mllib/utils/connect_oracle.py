# -*- coding: utf-8 -*-

import cx_Oracle, string
from utils import getpassword
import pandas as pd

# Get password
#key_environment = "test5-apps"
key_environment = "prd5-quapps"
pswd = getpassword.get_key_value(key_environment, "password")

# Build connection string
user = getpassword.get_key_value(key_environment, "username")
host = getpassword.get_key_value(key_environment, "host")
port = getpassword.get_key_value(key_environment, "port")
sid = getpassword.get_key_value(key_environment, "sid")
dsn = cx_Oracle.makedsn (host, port, sid)

def have_try_character():
    #import os
    #os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

    #import cx_Oracle
    db = getConnection()
    cursor = db.cursor()
    rs = cursor.execute('select * from cuc_eam.arch_org ao')
    li =rs.fetchall()
    print(li[0][1])


    db.commit()
    db.close()
# Connect to Oracle and test
def main():
    connection = getConnection()
    if (connection):
        print("Connection successful")
        print(connection.version)

        cursor = connection.cursor()

        try:
            cursor.execute('SELECT * from cuc_eam.eam_equipments_info eei')
            content = cursor.fetchone ()
            print('Count = %s\n',content)
        except cx_Oracle.DatabaseError as exception:
            print('Failed to select from EMP\n')
            print(exception)
            exit(1)
        finally:
            cursor.close()
            connection.close()
    else:
        print("Connection not successful")

def getConnection():
    connection = cx_Oracle.connect (user, pswd, dsn)
    return connection

def closeConnection(conn):
    if conn:
        conn.close()


def select():
    connection = getConnection()
    cursor = connection.cursor ()
    sql = "select * from cuc_eam.arch_org ao"

    try:
        rs = cursor.execute(sql)
    except cx_Oracle.DatabaseError as exception:
        print('Failed to select from EMP\n')
        print(exception)

    result = rs.fetchall ()
    for row in result:

        print(" %s;%s;%s\n" % (row[0],row[1],row[2]))

    closeConnection(connection)

def export_csv():
    import csv
    connection = getConnection()
    cursor = connection.cursor() # assuming you know how to connect to your oracle db
    cursor.execute('select * from cuc_eam.arch_org ao')
    with open('output_file.csv', 'wb') as fout:
        writer = csv.writer(fout)
#        writer.writerow([ i[0] for i in cursor.description ]) # heading row
        #writer.writerows(cursor.fetchall())
        for record in cursor:
            writer.writerow(record.encode("utf-8"))

def export_csv_2():
    import csv
    db     = getConnection()
    cursor = db.cursor()
    SQL    = "select * from cuc_eam.arch_org ao"
    cursor.execute(SQL)

    # Extract headers from cursor.description:
    headers = [i[0] for i in cursor.description]

    print(headers)
    # Open a file for writing, and create a csv.writer instance:
    with open("DATA.csv", "w") as f:

        fcsv = csv.writer(f)

        # Write header row, then write the rest of the data:
        fcsv.writerow(headers)
        for record in cursor:
            fcsv.writerow(record)

    assert f.closed

    # Reading written file back; result will be a list of lists:
    with open("DATA.csv", "r") as f:

        fcsv = csv.reader(f)
        for record in fcsv:
            print(record)




# 处理表头
def _process_table_header(sql, con):
    import pandas as pd
    if "where" in sql or "WHERE" in sql:
        sql += " AND 1 != 1"
    else:
        sql += " WHERE 1 != 1"
    df_ora = pd.read_sql(sql, con=con)
    return df_ora

## 通用导出
def general_export(filename, sql, chunk_size):
    import pandas as pd
    #query = "select * from cuc_eam.eam_equipments_info ao"
    connection = getConnection()
    header_df = _process_table_header(sql, connection)
    header_df.to_csv(filename, encoding="gb18030")
    df_ora = pd.read_sql(sql, con=connection, chunksize=chunk_size)
    flag = 0
    for chunk in df_ora:
        ## // Example

        # encoding see reference here: https://docs.python.org/3/library/codecs.html#standard-encodings
        try:
            chunk.to_csv(filename, mode='a', header=False, encoding="gb18030")
            #print(chunk)
            flag += 1
        except Exception as e:
            print("出错: ", e)


        print("导出:", chunk_size)

    closeConnection(connection)




# 导出被锁定的资产流程信息
def export_in_workflow():
    import pandas as pd
    query = """
SELECT cwh.last_updated_by,(SELECT au.account from cuc_eam.arch_user au WHERE au.user_id = cwh.last_updated_by) AS ACCOUNT,  cwh.approver_name, cwh.current_node_name, cwh.order_type, cwh.remarks,ebh.bill_number,cwh.task_type,cwh.flag, cwh.to_node_name , to_char(cwh.created_date, 'YYYY-MM-DD HH24:MI:SS') as created_date, eabi.asset_tag_num, eabi.eqm_number
FROM cuc_eam.cjbpm_workflow_history cwh , cuc_eam.eam_bill_head ebh, cuc_eam.eam_asset_basic_info eabi
WHERE 1=1
AND cwh.business_id = ebh.head_id
AND ebh.bill_number = eabi.bill_number
  and eabi.BOOK_TYPE_CODE = 'CUCBJ_FA_181101'
  and eabi.FLAG = 'Y'
  and cwh.task_type ='waitfordeal'

ORDER BY eabi.eqm_number, cwh.created_date

"""
    connection = getConnection()

    df_ora = pd.read_sql_query(query, con=connection, )
    df_ora.to_csv("/Users/alex/tmp/fa_workflow.csv", encoding="GBK")


    closeConnection(connection)


if __name__ == '__main__':
    #have_try_character()
    #select()
    #export_csv_2()
    #pandas_export_equipments()
    #export_in_workflow()

    # 折旧信息导出
    dpn_sql = """
SELECT FDS.ASSET_ID,
  FDS.PERIOD_COUNTER, 
               FDS.BOOK_TYPE_CODE,
               FDS.DEPRN_RESERVE,
               FDS.DEPRN_AMOUNT,
               FDS.YTD_DEPRN
          FROM FA_DEPRN_SUMMARY FDS
         WHERE FDS.DEPRN_SOURCE_CODE = 'DEPRN'
           AND FDS.BOOK_TYPE_CODE = 'CUCBJ_FA_121101'
"""
    user_sql = "select * from cuc_eam.ARCH_USER"

    # 导出被锁资产
    eam_locked_sql = """
SELECT cwh.last_updated_by,(SELECT au.account from cuc_eam.arch_user au WHERE au.user_id = cwh.last_updated_by) AS ACCOUNT,  cwh.approver_name, cwh.current_node_name, cwh.order_type, cwh.remarks,ebh.bill_number,cwh.task_type,cwh.flag, cwh.to_node_name , to_char(cwh.created_date, 'YYYY-MM-DD HH24:MI:SS') as created_date, eabi.asset_tag_num, eabi.eqm_number
FROM cuc_eam.cjbpm_workflow_history cwh , cuc_eam.eam_bill_head ebh, cuc_eam.eam_asset_basic_info eabi
WHERE 1=1
AND cwh.business_id = ebh.head_id
AND ebh.bill_number = eabi.bill_number
  and eabi.BOOK_TYPE_CODE = 'CUCBJ_FA_181101'
  and eabi.FLAG = 'Y'
  and cwh.task_type ='waitfordeal'
ORDER BY eabi.eqm_number, cwh.created_date
"""
    equipments_sql = "select * from cuc_eam.eam_equipments_info eei"
    general_export("/Users/alex/tmp/eam.csv", equipments_sql, chunk_size=2000)
