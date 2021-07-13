# -*- coding: utf-8 -*-

# python manage.py check_bday
# El resultado es en base a la fecha y hora universal (UTC)
# El cron job relacionado debe estar en /var/lib/openshift/53760892e0b8cdb5e9000b22/app-root/runtime/repo/.openshift

# Para comandos
from django.core.management.base import BaseCommand, CommandError

# Para consultas a la BD
from django.contrib.auth.models import User
import os, datetime
cmd_f = os.path.dirname(__file__)                   #coprovis/wsgi/myproject/base/management/commands
base = os.path.dirname(os.path.dirname(cmd_f))      #coprovis/wsgi/myproject/base
from base.models import Ficha

# Para mails
from myproject import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from email.mime.image import MIMEImage
from django.template.loader import get_template
from django.template import Context

class Command(BaseCommand):
    args = 'No requiere argumentos'
    help = 'Identifica los cumpleañeros del día'

    def handle(self, *args, **options):

        hoy = datetime.date.today()
        # hoy = datetime.date(2016,9,16)      # Fecha para realizar pruebas

        # IDs de Usuario de los cumpleañeros
        mi_query = Ficha.objects.filter(nacimiento__month=str(hoy.month), nacimiento__day=str(hoy.day)).order_by('nacimiento').values_list('usuario', flat=True)

        # Si hay cumpleañeros
        if mi_query:

            # Inicializa lista de cumpleañeros y mensaje inicial en consola
            cumples = []

            # Genera lista de cumpleañeros y salida en consola
            for i in mi_query:
                cumples.append([User.objects.get(id=i).first_name, User.objects.get(id=i).last_name, User.objects.get(id=i).is_active])

            # Establece conexión con el from_mail
            mail_cnx = get_connection()
            mail_cnx.open()

            # Define asunto del mail para los administradores y los templates a usar para los mensajes de texto y html
            asunto = u'Recordatorio Cumpleaños Miembros'
            txt_temp = get_template('base/mails/cumple_recor.txt')
            html_temp = get_template('base/mails/cumple_recor.html')

            # Renderiza los templates con el contexto apropiado
            contexto = Context({'cumples': cumples, 'hoy': hoy})
            txt_cnt = txt_temp.render(contexto)
            html_cnt = html_temp.render(contexto)

            try:
                # Se construye un objeto de mail al cual pueda ser adherido una alternativa html
                correo = EmailMultiAlternatives(subject=asunto, body=txt_cnt,
                                                from_email=settings.DEFAULT_FROM_EMAIL,
                                                to=['maravape@gmail.com', 'jacquelinne.valencia@gmail.com', 'leonelcarri055@gmail.com'],
                                                # to=['maravape@gmail.com'],
                                                connection=mail_cnx)

                # Se adhiere alternativa html e imágenes preparadas
                correo.attach_alternative(html_cnt, "text/html")

                # Se declara el mixed subtype
                correo.mixed_subtype = 'related'

                # Se envía el mail
                correo.send(fail_silently=False)

            except:
                pass

            # Define asunto del mail para los cumpleañeros y los templates a usar para los mensajes de texto y html
            asunto = u'Feliz Cumpleaños!!'
            txt_temp = get_template('base/mails/cumple.txt')
            html_temp = get_template('base/mails/cumple.html')

            for miembro in mi_query:

                # Renderiza los templates con el contexto apropiado
                contexto = Context({'nombre': User.objects.get(id=miembro).first_name})
                txt_cnt = txt_temp.render(contexto)
                html_cnt = html_temp.render(contexto)

                try:
                    # Se construye un objeto de mail al cual pueda ser adherido una alternativa html
                    correo = EmailMultiAlternatives(subject=asunto, body=txt_cnt,
                                                    from_email=settings.DEFAULT_FROM_EMAIL,
                                                    to=[User.objects.get(id=miembro).email],
                                                    connection=mail_cnx)

                    # Se adhiere alternativa html e imágenes preparadas
                    correo.attach_alternative(html_cnt, "text/html")

                    # Se declara el mixed subtype
                    correo.mixed_subtype = 'related'

                    # Se envía el mail
                    correo.send(fail_silently=False)

                except: pass

            # Cierra conexión con el from_mail
            mail_cnx.close()

            # Mensaje expuesto en Bash (si hay caracteres no ASCII se  produce un error pero los mails fueron enviados
            print 'Cumpleaneros de hoy!!! ({})'.format(hoy.strftime('%d de %b de %Y'))
            for i in mi_query:
                print u'{} {}, Usuario Activo? {}'.format(User.objects.get(id=i).first_name, User.objects.get(id=i).last_name, User.objects.get(id=i).is_active)

        # Si no hay cumpleañeros
        else:
            print 'Este dia no hay cumpleaneros... ({})'.format(hoy.strftime('%d de %b de %Y'))