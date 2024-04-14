import os

def env_variables(request):
    return {
        'FRONTEND_URL': os.environ.get('FRONTEND_URL', 'http://localhost:3000/')
    }