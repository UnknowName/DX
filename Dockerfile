FROM django:1.8-python2
RUN pip install django_admin_bootstrapped gunicorn
ADD ./  /usr/src/app
WORKDIR /usr/src/app
VOLUME ["/usr/src/app/uploads","/usr/src/app/static"]
CMD ["/usr/local/bin/python","manage.py","runserver","0.0.0.0:8000"]
EXPOSE 8000
