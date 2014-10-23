from contextlib import contextmanager
from fabric.colors import green, magenta, yellow
from fabric.contrib.files import upload_template, exists
from fabric.decorators import task
from fabric.operations import local

from fabric.api import *

env.hosts = ['54.173.21.90']
env.server_name = 'ec2-54-173-21-90.compute-1.amazonaws.com'
env.user = 'ubuntu'
env.key_filename = '~/.ssh/blog_analytics.pem'
env.virtualenv_name = 'blog_analytics'
env.project_name = 'rocketu_blog_analytics'
env.project_path = '/home/ubuntu/rocketu_blog_analytics_2'
env.github_https = 'https://github.com/brittkistner/rocketu_blog_analytics.git'
env.db_password = 'hello'
env.db_name = 'blog_analytics'
env.db_user = 'blog_analytics'
# env.shell = "/bin/bash -l -i -c"

@task
def hello():
    print(green("I'm alive!"))

@task
def create_file(file_name):
    local("touch ~/Desktop/{}.txt".format(file_name))

@task
def create_directory():
    local("mkdir ~/Desktop/my_directory")

@task
def create_folder_in_directory(folder_name, directory_path):
    local("mkdir {}/{}".format(directory_path, folder_name))

@task
def ubuntu_hello():
    with hide("stdout"):
        output = run("lsb_release -a")
        print(yellow(output))

def restart_app():
    sudo("service supervisor restart")
    sudo("service nginx restart")

@contextmanager
def virtualenv():
    """
    Runs commands within the project's virtualenv.
    """
    if not exists("source ~/.virtualenvs/{}/bin/activate".format(env.virtualenv_name)):
        run("mkdir source ~/.virtualenvs/{}/bin/activate".format(env.virtualenv_name))
    with cd(env.virtualenv_name):
        with prefix("source ~/.virtualenvs/{}/bin/activate".format(env.virtualenv_name)):
            yield

@task
def deploy():
    # with prefix("source ~/.virtualenvs/blog_analytics/bin/activate"):
    with virtualenv():
        with cd(env.project_path):
            run("git pull origin master")
            run("pip install -r requirements.txt")
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")
    restart_app()

@task
def setup_postgres():
    sudo("adduser {}".format(env.db_name))
    sudo("apt-get install postgresql postgresql-contrib libpq-dev")

    with settings(sudo_user='postgres'):
        sudo("createuser {}".format(env.db_user))
        sudo("createdb {}".format(env.db_name))
        alter_user_statement = "ALTER USER {} WITH PASSWORD '{}';".format(env.db_user, env.db_password)
        sudo('psql -c "{}"'.format(alter_user_statement))

@task
def setup_nginx():  #project_name is what is being called with the .conf file, server name = ec2 url
    upload_template("./deploy/nginx.conf",
                    "/etc/nginx/sites-enabled/{}.conf".format(env.project_name),
                    {'server_name': env.server_name},
                    use_sudo=True,
                    backup=False)

    restart_app()

@task
def create_symlinks():
    run("rm /etc/nginx/sites-enabled/default")
    restart_app()
    # run("ln -s /etc/nginx/sites-available/{}".format(env.project_name),
    #        "/etc/nginx/sites-enabled/{}".format(env.project_name)
    #        )
    restart_app()
    #check that nginx is actually running

@task
def setup_gunicorn(workers):
    # create directory
    upload_template("./deploy/gunicorn.conf",
                    "{}/gunicorn.conf.py".format(env.project_name),
                    # pip install similar to the deploy setup with prefix
                    {"proc_name": env.project_name, "workers": workers},
                    use_sudo=True,
                    backup=False)
    restart_app()

@task
def setup_supervisor():
    # create directory
    upload_template("./deploy/supervisor.conf",
                    "/etc/supervisor/conf.d/{}.conf".format(env.project_name),
                    {"project_name": env.project_name, "virtual_env_name": env.virtualenv_name},
                    use_sudo=True,
                    backup=False)
    restart_app()


@task
def pip(packages):
    """
    Installs one or more Python packages within the virtual environment.
    """
    with virtualenv():
        return sudo("pip install %s" % packages)

def create_local_settings():
    local_settings_path = run('mkdir {}/local_settings.py'.format(env.project_path))
    upload_template("./deploy/local_settings.conf",
                    local_settings_path,
                    {"db_name": env.db_name,
                     "db_user": env.db_user,
                     "db_password": env.db_password,
                     "server_name": env.server_name},
                    use_sudo=False,
                    backup=False)
    #check on sudo for this case

#django manage.py commands, apt-get

@task
def startup(workers):
    """
    Runs commands to startup project.
    Installs and completes setup for postgres, nginx, gunicorn, and supervisor.
    """
    sudo("apt-get update")
    sudo("apt-get upgrade")
    sudo("apt-get install nginx")
    if not exists(env.project_path):
        run("mkdir {}".format(env.project_path))
    sudo("apt-get install git")
    if not exists("{}/.git".format(env.project_path)):
        run("git clone {} {}".format(env.github_https, env.project_path))
    # ensure ubuntu user owns the repo folder
    sudo("apt-get install python-pip python-dev build-essential")
    sudo("pip install pip --upgrade")
    # create virtualenv folder
    # with virtualenv():
    create_local_settings()
    setup_postgres()
    deploy()
    setup_nginx()
    setup_gunicorn(workers)
    setup_supervisor()
    #create_symlinks()
    #launch site

