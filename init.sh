python3 -m venv env
source env/bin/activate
python -m pip install django
python -m pip freeze > requirements.txt

## For Amazon Linux 2
sudo yum install python3-devel mysql-devel
pip install mysqlclient