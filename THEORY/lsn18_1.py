from UTILS.APP_RUN import app_run
from THEORY.BIG_APPS.APP.main import app

"""
Запуск приложения из THEORY.BIG_APPS.APP.main
"""

if __name__ == '__main__':
    app_run(file=__file__, app_name=getattr(app, 'name', 'app'))
