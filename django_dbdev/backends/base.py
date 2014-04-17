
class BaseDbdevBackend(object):
    def execute_sql_using_dbshell(self, user, password, sql):
        raise NotImplementedError()