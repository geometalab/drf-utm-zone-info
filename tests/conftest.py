import os

test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')

postgres_container_userland_port = 65432  # required for travis, so using it everywhere


def pytest_configure():
    from django.conf import settings
    import environ

    settings.configure(
        ROOT_DIR=environ.Path(__file__) - 1,
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'postgres',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'PORT': '54321',
                'HOST': '127.0.0.1',
            }
        },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        INSTALLED_APPS=(
            'django.contrib.gis',
        ),
    )
