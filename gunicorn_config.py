# gunicorn_config.py

bind = "0.0.0.0:8080"
module = "aurigaone.wsgi:application"

workers = 4  # Adjust based on your server's resources
worker_connections = 1000
threads = 4

certfile = "/etc/letsencrypt/live/baclendfloristika.life/fullchain.pem"
keyfile = "/etc/letsencrypt/live/baclendfloristika.life/privkey.pem"