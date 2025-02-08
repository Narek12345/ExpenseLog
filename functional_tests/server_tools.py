from fabric import Connection


def _get_manage_dot_py(host):
    """Получить 'manage.py'."""
    return f'~/to_do_pro/{host}/venv/bin/python ~/to_do_pro/{host}/source/manage.py'


def reset_database(host):
    """Обнулить базу данных."""
    manage_dot_py = _get_manage_dot_py(host)
    with Connection(host=f'elspeth@{host}') as c:
        c.run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    """Создать сеанс на сервере."""
    manage_dot_py = _get_manage_dot_py(host)
    with Connection(host=f'elspeth@{host}') as c:
        result = c.run(f'{manage_dot_py} create session {email}', hide=True)
        return result.stdout.strip()
