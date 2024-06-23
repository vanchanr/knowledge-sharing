```
$ curl ipecho.net/plain
65.2.57.236
----------------------------------------------------------------------

$ sudo apt install mysql-server
----------------------------------------------------------------------

$ mysql --version
mysql  Ver 14.14 Distrib 5.7.37, for Linux (x86_64) using  EditLine wrapper
----------------------------------------------------------------------

$ sudo service mysql status
● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2022-02-27 13:39:51 UTC; 10s ago
 Main PID: 17359 (mysqld)
    Tasks: 27 (limit: 4686)
   CGroup: /system.slice/mysql.service
           └─17359 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid

Feb 27 13:39:50 ip-172-31-14-146 systemd[1]: Starting MySQL Community Server...
Feb 27 13:39:51 ip-172-31-14-146 systemd[1]: Started MySQL Community Server.
----------------------------------------------------------------------

$ ps aux | grep mysql
mysql    17359  0.3  4.4 1358104 177560 ?      Sl   13:39   0:00 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid
----------------------------------------------------------------------

$ sudo netstat -tlpn | grep mysql
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      17359/mysqld
----------------------------------------------------------------------

$ sudo mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.7.37-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> status
mysql  Ver 14.14 Distrib 5.7.37, for Linux (x86_64) using  EditLine wrapper

Connection id:          9
Current database:
Current user:           root@localhost
SSL:                    Not in use
Current pager:          stdout
Using outfile:          ''
Using delimiter:        ;
Server version:         5.7.37-0ubuntu0.18.04.1 (Ubuntu)
Protocol version:       10
Connection:             Localhost via UNIX socket
Server characterset:    latin1
Db     characterset:    latin1
Client characterset:    utf8
Conn.  characterset:    utf8
UNIX socket:            /var/run/mysqld/mysqld.sock
Uptime:                 12 min 31 sec

Threads: 1  Questions: 18  Slow queries: 0  Opens: 105  Flush tables: 1  Open tables: 98  Queries per second avg: 0.023
----------------------------------------------------------------------

mysql> use db;
ERROR 1049 (42000): Unknown database 'db'
mysql> create database db;
Query OK, 1 row affected (0.00 sec)

mysql> show tables;
ERROR 1046 (3D000): No database selected
mysql> use db;
Database changed
mysql> show tables;
Empty set (0.00 sec)

mysql> create table dummy(id integer, name varchar(30), primary key(id));
Query OK, 0 rows affected (0.01 sec)

mysql> show tables;
+--------------+
| Tables_in_db |
+--------------+
| dummy        |
+--------------+
1 row in set (0.00 sec)

mysql> select * from dummy;
Empty set (0.01 sec)

mysql> insert into dummy values (1, 'rahul'), (2, 'sql');
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> select * from dummy;
+----+-------+
| id | name  |
+----+-------+
|  1 | rahul |
|  2 | sql   |
+----+-------+
2 rows in set (0.00 sec)
----------------------------------------------------------------------
```

**accessing the db remotely:**
* change bind-address in `/etc/mysql/mysql.conf.d/mysqld.cnf` from `127.0.0.1 / localhost` to `0.0.0.0`
* restart mysql service
```
$ sudo service mysql restart

$ sudo netstat -tlpn | grep mysql
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      28136/mysqld
```
![image](https://user-images.githubusercontent.com/43525805/155886568-63189f6e-2047-48e7-aebb-2d7b91d3f404.png)

* open EC2 security group to port 3306

![image](https://user-images.githubusercontent.com/43525805/155886937-1f184d5f-64a8-4822-8028-a34e98c73806.png)

* grant privileges from external ip
```
mysql> GRANT ALL PRIVILEGES ON *.* TO root@'%' IDENTIFIED BY 'pass123';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

![image](https://user-images.githubusercontent.com/43525805/155887211-42326383-6a65-46a4-a68d-8d0d34e243b0.png)

