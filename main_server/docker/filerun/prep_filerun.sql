CREATE USER 'filerun' IDENTIFIED by 'filerun';
CREATE DATABASE IF NOT EXISTS filerun;
GRANT ALL PRIVILEGES ON `filerun`.* TO 'filerun';
FLUSH PRIVILEGES;