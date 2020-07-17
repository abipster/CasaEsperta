CREATE USER 'guacdb_user' IDENTIFIED by 'guacamole';
CREATE DATABASE IF NOT EXISTS guacamole;
GRANT ALL PRIVILEGES ON `guacamole%`.* TO 'guacdb_user';
FLUSH PRIVILEGES;