from fabric.api import run, env, cd, sudo

env.hosts = ['direct.lxneng.com']
env.user = 'root'
CODE_DIR = '/var/www/lxneng.com'


def deploy():
    with cd(CODE_DIR):
        run('git pull && supervisorctl restart lxneng')


def restart_nginx():
    sudo('/etc/init.d/nginx restart')
