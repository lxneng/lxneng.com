from fabric.api import run, env, cd, run

env.hosts = ['lxneng.com']
env.user = 'root'
CODE_DIR = '/var/www/lxneng'


def deploy():
    with cd(CODE_DIR):
        run('git pull')
        run('supervisorctl restart gunicorn')


def restart_nginx():
    sudo('/etc/init.d/nginx restart')


def install_requirements():
    with cd(CODE_DIR):
        run('/root/env/bin/pip install -r requirements.txt')


def db_migrate():
    with cd(CODE_DIR):
        run('/root/env/bin/upgrade --scan lxneng\
                --db-uri mysql://root@localhost/lxneng')
