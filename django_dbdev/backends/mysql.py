from subprocess import check_call
from django.conf import settings

from .base import BaseDbdevBackend


class MySqlBackend(object):
    def __init__(self, command):
        self.command = command

    # @property
    # def _mysqld_executable(self):
    #     return getattr(settings, 'MYSQLD_PATH', 'mysqld')

    @property
    def _mysql_executable(self):
        return getattr(settings, 'MYSQL_PATH', 'mysql')

    def execute_sql_using_dbshell(self, user, password, sql):
        cmd = [
            self._mysql_executable,
            '--user={}'.format(user),
            '--password={}'.format(password),
            '-e', sql,
        ]
        check_call(cmd)

    def drop_user(self, adminuser, adminuserpassword):
        self.execute_sql_using_dbshell(
            adminuser, adminuserpassword,
            "DROP USER '{dbuser}'@'localhost';".format(dbuser=self.command.dbuser))

    def create_user(self, adminuser, adminuserpassword):
        self.execute_sql_using_dbshell(
            adminuser, adminuserpassword,
            ("CREATE USER '{dbuser}'@'localhost' IDENTIFIED BY '{dbpassword}';"
             "GRANT ALL PRIVILEGES ON *.* TO '{dbuser}'@'localhost';"
            ).format(
                dbuser=self.command.dbuser,
                dbpassword=self.command.dbpassword,
                dbname=self.command.dbname)
        )