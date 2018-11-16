git pull origin GF
python manage.py makemigrations openstack_dashboard
python manage.py migrate
cp -r openstack_dashboard /usr/lib/python2.7/dist-packages
bash ~/restart.bash
