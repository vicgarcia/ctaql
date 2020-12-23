setup ctaql user and app install path

```
useradd --system ctaql
mkdir /opt/ctaql && chown -R ctaql:ctaql /opt/ctaql
```

setup python 3.8 + pipenv

```
add-apt-repository ppa:deadsnakes/ppa
apt install python3.8
apt install python3.8-venv
apt install python-pip
pip install pipenv

# https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/
```

generate ssl certificate for ctaql.cc + www.ctaql.cc

```
certbot --nginx -d ctaql.cc -d www.ctaql.cc -m vicg4rcia@gmail.com --agree-tos -n
```

clone ctaql repo, setup virtualenv, install dependencies

```
su - ctaql -c "git clone https://github.com/vicgarcia/ctaql.git /opt/ctaql"
su - ctaql -c "cd /opt/ctaql && export PIPENV_VENV_IN_PROJECT=1 && pipenv install"
su - ctaql -c "cd /opt/ctaql && pipenv run python application/manage.py collectstatic"
su - ctaql -c "cd /opt/ctaql && cp .env.example .env && vim .env"
```

add nginx config

```
cp /opt/ctaql/application/production/nginx.conf /etc/nginx/sites-available/ctaql.cc
ln -s /etc/nginx/sites-available/ctaql.cc /etc/nginx/sites-enabled/
```

add systemd service

```
cp /opt/ctaql/application/production/systemd.service /etc/systemd/system/ctaql.service
```

start things

```
service ctaql restart
service nginx restart
```
