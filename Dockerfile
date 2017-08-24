FROM django:1.8-python2
RUN apt-get update
RUN apt-get install libldap2-dev libsasl2-dev -y
RUN pip install django_admin_bootstrapped gunicorn python-ldap
ADD ./  /usr/src/app
WORKDIR /usr/src/app
VOLUME ["/usr/src/app/uploads","/usr/src/app/static"]
#CMD ["gunicorn", "dx.wsgi", "-w", "2", "-b", "0.0.0.0:8000"]
CMD ["/usr/local/bin/python","manage.py","runserver","0.0.0.0:8000"]
EXPOSE 8000
