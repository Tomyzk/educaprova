__all__ = []

# Allow using PyMySQL as MySQLdb if mysqlclient is not installed
try:
    import pymysql  # type: ignore

    pymysql.install_as_MySQLdb()
except Exception:
    pass
