FROM python:3.5

MAINTAINER Anoop Macharla <149@holbertonschool.com>

# Install uWSGI
RUN pip install uwsgi

# Install Nginx ----
RUN apt-get -y update && apt-get -y install nginx

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

# tell the container what port flask will be using
EXPOSE 80 443

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Remove default configuration from Nginx and add custom
COPY url_shortener /etc/nginx/sites-available/
RUN ln -fs /etc/nginx/sites-available/url_shortener /etc/nginx/sites-enabled/default

# Move respective files to right location based on configration
# copy web_app to /var/www/url_shortener/
RUN mkdir -p /var/www/url_shortener/
COPY web_app /var/www/url_shortener/web_app

#python requirements
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt \
	&& rm -rf /requirements.txt

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*
# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

VOLUME /var/www/url_shortener/web_app
WORKDIR /var/www/url_shortener/web_app

CMD ["/usr/bin/supervisord"]
