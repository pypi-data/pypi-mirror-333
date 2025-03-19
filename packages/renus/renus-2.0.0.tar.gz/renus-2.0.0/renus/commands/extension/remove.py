import shutil

from renus.commands.extension.build import _remove_route, _remove_admin_templates, _remove_index_templates, _remove_config
from renus.commands.help import bc


def remove_all(installed:dict):
    items=installed.copy()
    for app, version in items.items():
        remove(app,installed)

def remove(app,installed):
    print(f'   remove {app}')
    del installed[app]
    try:
        install = __import__(f"extension.{app.replace('/', '.')}.install", fromlist=[''])

    except Exception as exc:
        print('   ' + bc.WARNING + str(exc) + bc.ENDC)
        return

    if hasattr(install, 'setup_remove'):
        print(f'   setup remove {app}...')
        try:
            install.setup_remove()
        except Exception as exc:
            print('   ' + bc.FAIL + str(exc) + bc.ENDC)

    if hasattr(install, 'route'):
        print(f'   remove {app} route...')
        _remove_route(install, app)


    if hasattr(install, 'admin_templates'):
        print(f'   remove {app} admin_templates...')
        try:
            _remove_admin_templates(install,app)
        except Exception as exc:
            print('   ' + bc.FAIL + str(exc) + bc.ENDC)

    if hasattr(install, 'index_templates'):
        print(f'   remove {app} index_templates...')
        try:
            _remove_index_templates(install,app)
        except Exception as exc:
            print('   ' + bc.FAIL + str(exc) + bc.ENDC)


    if hasattr(install, 'config'):
        print(f'   remove {app} config...')
        try:
            _remove_config(install)
        except Exception as exc:
            print('   ' + bc.FAIL + str(exc) + bc.ENDC)


    print(f'   remove {app} folder...')
    try:
        shutil.rmtree('./app/extension/' + app)
        shutil.rmtree('./extension/' + app)
    except Exception as exc:
        print('   ' + bc.FAIL + str(exc) + bc.ENDC)