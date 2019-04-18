import pymysql
from utils import *


class DB:
    def __init__(self, username, passwd, database, host="localhost", port=3306):
        try:
            self.conn = pymysql.connect(host=host, port=port, user=username, password=passwd, database=dbbase)
        except Exception as e:
            print(e)
        self.cursor = self.conn.cursor()

    # def fetchone(self, table, col, cond):
    #     sql = "SELECT {col} FROM {table}".format(col=" , ".join(col), table=table)
    #     if cond:
    #         sql += " WHERE {condition} ".format(
    #             condition=" and ".join(cond))
    #     sql += " limit 0, 1 "
    #     result = None
    #
    #     try:
    #         result = self.cursor.execute(sql)
    #         print_msg("sql执行完成: {sql}".format(sql))
    #     except Exception as e:
    #         print_msg("sql执行失败: {sql}".format(sql), "ERROR")
    #         print_msg(e, "ERROR")
    #
    #     return result[0] if not result else result
    #
    # def fetchall(self, table, col, offset=None, limit=None, cond=None):
    #     sql = "SELECT {col} FROM {table}".format(col=" , ".join(col), table=table)
    #     if cond:
    #         sql += " WHERE {condition} ".format(condition=" and ".join(cond))
    #     if offset and limit:
    #         sql += " limit {offset} {limit};".format(limit=limit, offset=offset)
    #
    #     result = None
    #
    #     try:
    #         result = self.cursor.fetchall(sql)
    #         print_msg("sql执行完成: {sql}".format(sql=sql))
    #     except Exception as e:
    #         print_msg("sql执行失败: {sql}".format(sql=sql), "ERROR")
    #         print_msg(e, "ERROR")
    #
    #     return result

    def insert(self, table, k, v):
        sql = "INSERT {table} ({k}) VALUES (v)".format(table=table, k=",".join(k), v=",".joint(v))
        try:
            self.cursor.execute(sql)
            print_msg("sql执行完成: {sql}".format(sql))
            return True
        except Exception as e:
            print_msg("sql执行失败: {sql}".format(sql), "ERROR")
            print_msg(e, "ERROR")
            return False

    def delete(self, table, **conditions):
        sql = "DELETE FROM {table} WHERE {conditions}".format(conditions=" and ".join([k + " = " + str(v) for k, v in conditions.items()]))
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print_msg("sql执行完成: {sql}".format(sql))
            return True
        except Exception as e:
            print_msg("sql执行失败: {sql}".format(sql), "ERROR")
            print_msg(e, "ERROR")
            return False

    def update(self, valuesdict, **condition):
        sql = "UPDATE {table} set {valuesdict} where {condition}".format(table=table, valuesdict=",".join([k+"="+str(v) for k, v in valuesdict.items()]), condition=",".join([k+"="+str(v) for k, v in condition.items()]))
        try:
            self.cursor.execute(sql)
            print_msg("sql执行完成: {sql}".format(sql))
            return True
        except Exception as e:
            print_msg("sql执行失败: {sql}".format(sql), "ERROR")
            print_msg(e, "ERROR")
            return False

    def excute(self, sql):
        result = None
        try:
            result = self.cursor.execute(sql)
            print_msg("sql执行完成: {sql}".format(sql))
        except Exception as e:
            print_msg("sql执行失败: {sql}".format(sql), "ERROR")
            print_msg(e, "ERROR")
        finally:
            return result

    def fetchall(self, sql):
        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            print_msg("sql执行完成: {sql}".format(sql))
        except Exception as e:
            print_msg("sql执行失败: {sql}".format(sql), "ERROR")
            print_msg(e, "ERROR")
        finally:
            return result

    def fetchone(self, sql):
        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            print_msg("sql执行完成: {sql}".format(sql))
        except Exception as e:
            print_msg("sql执行失败: {sql}".format(sql), "ERROR")
            print_msg(e, "ERROR")
        finally:
            return result