# import pymysql
#
# pymysql.install_as_MySQLdb()
from component.mysql_pool import patch_mysql

patch_mysql()
