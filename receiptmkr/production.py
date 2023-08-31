from receiptmkr.settings import *
import environ
env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['oxos-receiptmkr.onrender.com', '127.0.0.1']

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ADMIN_MEDIA_PREFIX = '/static/admin/'   
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('NAME'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT': env('PORT'),
        'USER': env('USER'),

    }
}
# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'neondb',
#     'USER': 'mezardini',
#     'PASSWORD': '4PmLBUDY5FqJ',
#     'HOST': 'ep-shy-dawn-89894175.us-east-2.aws.neon.tech',
#     'PORT': '5432',
#   }
# }


# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


#_psycopg2

# SITE_ID = 1

# LOGIN_REDIRECT_URL = 'https://mezzala.onrender.com/'
# LOGOUT_REDIRECT_URL = 'https://mezzala.onrender.com/'

SITE_ID = 1
# LOGIN_REDIRECT_URL = 'https://oxos-receiptmkr.onrender.com/dashboard/'
# LOGIN_REDIRECT_URL = 'https://oxos-receiptmkr.onrender.com/dashboard/'
# USE_X_FORWARDED_HOST = True

ADMIN_MEDIA_PREFIX = '/static/admin/'   
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'