from fabric.api import local, settings, abort, run, cd
from fabric.operations import get, sudo
from fabric.state import env

env.user = 'iptv'
env.hosts = ['213.159.56.188:24']

IPTV_SERVICE_USER = 'iptv'
WEB_GRAB_URL = 'http://www.webgrabplus.com/sites/default/files/download/SW/V2.1.0/WebGrabPlus_V2.1_install.tar.gz'
GIT_REPO_URL = 'git@github.com:Povilas1/Skynet-IPTV-With-EPG.git'

BASE_DIR = '/opt/iptv-epg'  # arbitrary directory in which your store files
WG_DIR = '/opt/iptv-epg/wgpp'
REPO_DIR = '/opt/iptv-epg/epg-repo'


def generate_epg():
    pass

def deploy_config():
    """Deploys config edits to WG++ generator"""
    with cd('{}'.format(REPO_DIR)):
        run('git pull origin master')
        # TODO: Stills needs to be copied even if source if fresh
        run('cp {}/tools/WebGrab++.config.xml {}'.format(REPO_DIR, WG_DIR))


def download_epg(local_path='/tmp'):
    """copies epg from the generator machine."""
    remote_path = "{}/guide.xml".format(WG_DIR)
    get(remote_path=remote_path, local_path=local_path, use_sudo=True)


def install():
    run("sudo apt-get install -y mono-complete")

    with run('mkdir /opt/iptv-epg'):
        with cd('/opt/iptv-epg'):
            with run('wget {}'.format(WEB_GRAB_URL)):
                run('tar -zxvf *.tar.gz')
                run('mv .wg++ wgpp')
                run('rm *.tar.gz')
                run('git clone {} epg-repo'.format(GIT_REPO_URL))
                run('cp ./epg-repo/tools/WebGrab++.config.xml ./wgpp/')


def connection_test():
    run('whoami')


