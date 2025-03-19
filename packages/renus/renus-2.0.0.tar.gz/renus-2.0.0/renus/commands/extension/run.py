import shutil
import zipfile
from io import BytesIO
from importlib.metadata import version as md_version
import requests

from renus.commands.extension.remove import remove_all, remove
from renus.commands.help import bc
from renus.commands.extension.build import _add_route, _add_admin_templates, _add_index_templates, \
    _add_cls, _add_imprt, _add_config


def download(app, version, installed, isUpdate=False):
    if app in installed:
        if isUpdate and installed[app] == version:
            return version
        elif not isUpdate:
            return version

    print(f'{bc.OKGREEN}downloading {app}/{version}{bc.ENDC}')

    res = requests.get(f'https://reapp.codenus.com/app/{app}/{version}')

    if res.status_code != 200:
        print(f'{bc.FAIL}download error{bc.ENDC}')
        return

    if app in installed:
        if isUpdate and installed[app] == res.headers['version']:
            print('   same version', res.headers['version'])
            return res.headers['version']
        elif not isUpdate:
            print('   currently installed version', installed[app])
            return res.headers['version']

    installed[app] = res.headers['version']
    f = zipfile.ZipFile(BytesIO(res.content))
    shutil.rmtree(f"extension/{app}", True)
    f.extractall(f"extension/{app}")

    install_app(app, installed,isUpdate)
    if isUpdate:
        print(f'{bc.OKBLUE}   updated to version {res.headers["version"]}{bc.ENDC}')
    return res.headers['version']


def rewrite(installed):
    print('   rewrite installed')
    pre_line = ''
    with open('extension/install.py', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.find('installed') != -1:
                break
            pre_line += line
    with open('extension/install.py', 'w') as f:
        f.write(pre_line)
        f.write('installed = {\n')
        for app, version in installed.items():
            f.write(f'  "{app}":"{version}",\n')
        f.write('}')


def check_version(install,app):
    renus_requires = install.renus_requires
    min=renus_requires['min'].split('.')
    max=renus_requires['max'].split('.')
    renus_version = md_version('renus')
    version = renus_version.split('.')
    for i in range(len(min)):
        if int(version[i]) < int(min[i]):
            raise RuntimeError(f"{app}: renus version too low. {renus_version} < {renus_requires['min']}")
    for i in range(len(max)):
        if int(version[i]) >= int(min[i]):
            raise RuntimeError(f"{app}: renus version too high. {renus_version} >= {renus_requires['max']}")


def install_app(app, installed,isUpdate):
    print(f'   install {app}')
    try:
        install = __import__(f"extension.{app.replace('/', '.')}.install", fromlist=[''])

    except Exception as exc:
        print('   ' + bc.WARNING + str(exc) + bc.ENDC)
        return

    check_version(install,app)_

    if hasattr(install, 'dependencies'):
        print(f'   install {app} dependencies...')
        for dep in install.dependencies:
            download(dep, '*', installed)

    if not isUpdate:
        if hasattr(install, 'cls'):
            print(f'   add {app} class...')
            try:
                _add_cls(install, app)
            except Exception as exc:
                print('   ' + bc.FAIL + str(exc) + bc.ENDC)

        if hasattr(install, 'route'):
            print(f'   add {app} route...')
            _add_route(install,app)

        if hasattr(install, 'imprt'):
            print(f'   add {app} imports...')
            try:
                _add_imprt(install, app)
            except Exception as exc:
                print('   ' + bc.FAIL + str(exc) + bc.ENDC)

        if hasattr(install, 'admin_templates'):
            print(f'   add {app} admin_templates...')
            try:
                if install.admin_templates:
                    _add_admin_templates(install,app)
            except Exception as exc:
                print('   ' + bc.FAIL + str(exc) + bc.ENDC)

        if hasattr(install, 'index_templates'):
            print(f'   add {app} index_templates...')
            try:
                if install.index_templates:
                    _add_index_templates(install,app)
            except Exception as exc:
                print('   ' + bc.FAIL + str(exc) + bc.ENDC)

        if hasattr(install, 'config'):
            print(f'   add {app} config...')
            try:
                _add_config(install)
            except Exception as exc:
                print('   ' + bc.FAIL + str(exc) + bc.ENDC)

        if hasattr(install, 'setup'):
            print(f'   setup {app}...')
            try:
                install.setup()
            except Exception as exc:
                print('   ' + bc.FAIL + str(exc) + bc.ENDC)
    else:
        if hasattr(install, 'setup_update'):
            print(f'   setup update {app}...')
            try:
                install.setup_update()
            except Exception as exc:
                print('   ' + bc.FAIL + str(exc) + bc.ENDC)


def install_all(apps, installed, isUpdate):
    d = apps
    if isUpdate:
        d = installed
    for app, version in d.items():
        download(app, '*' if isUpdate else version, installed, isUpdate)


def run(args=None):
    print('start...')
    try:
        from extension.install import apps, installed
    except:
        apps = {}
        installed = {}

    isUpdate = False
    isRemove = False

    if args and '--update' in args:
        isUpdate = True
        args.remove('--update')
    if args and '--remove' in args:
        isRemove = True
        args.remove('--remove')
    if isUpdate and isRemove:
        raise RuntimeError("use one of '--update' or '--remove'")

    if args is None or len(args) == 0:
        if isRemove:
            remove_all(installed)
        else:
            install_all(apps, installed, isUpdate)
    else:
        s = args[0].split('==')
        version = "*"
        if len(s) > 1:
            version=s[1]
        if isRemove:
            remove(s[0],installed)
        else:
            download(s[0], version, installed, isUpdate)

    rewrite(installed)

    print(f'{bc.OKBLUE}finished{bc.ENDC}')
