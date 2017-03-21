#!/bin/bash
if [ $# -lt 4 ]
then
	echo "Database Connect Tools"
	echo "Usage: base $0 type ip user pass [port]"
	exit
fi

database_type=$1
ip=$2
user=$3
pass=$4
port=$5

#mysql
if [ $database_type = "mysql" ]
then
	p=${port:-3306}
	str="com.mysql.jdbc.Driver"
	jdbc="jdbc:mysql://${ip}:${p}/mysql"
elif [ $database_type = "mssql" ]
then
	p=${port:-1433}
	str="com.microsoft.sqlserver.jdbc.SQLServerDriver"
	jdbc="jdbc:sqlserver://${ip}:${p};databaseName=master"
elif [ $dayabase_type = "oracle" ]
then
	p=${port:-1521}
	str="oracle.jdbc.driver.OracleDriver"
	jdbc="jdbc:oracle:thin:@${ip}:${p}:orcl"
else 
	echo "Unsupport Database"
	exit
fi
echo $jdbc
echo "Exec Sql...."
java -jar sqlplus.jar $str $jdbc $user $pass "select 'test ok'"
