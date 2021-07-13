#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from .models import Registro, Ficha

# Para mails y mensajes
import os
from her_copro import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from email.mime.image import MIMEImage
from django.template.loader import get_template
from django.template import Context
from django.contrib.messages import SUCCESS, INFO, WARNING, ERROR, DEBUG

# -------------------------------------------- Modificación del AdminSite --------------------------------------------

admin.AdminSite.index_title = 'Tablas'
admin.AdminSite.site_title = 'Admin Coprovis'
admin.AdminSite.site_header = u'Administración WebSite Coprovis'
admin.AdminSite.site_url = '/control/'

# ------------------------------------------------- Acciones -------------------------------------------------

# Envía mail de bienvenida y enlace para generar password
def dar_bienvenida(modeladmin, request, queryset):

    # Establece conexión con el from_mail
    mail_cnx = get_connection()
    mail_cnx.open()

    # Inicializa lista de miembros sin correo asignado y asunto de los mails
    no_mail = ''
    asunto = 'Bienvenido a Coprovis'

    # Define los templates a usar para los mensajes de texto y html
    txt_temp    = get_template('base/mails/bienvenida.txt')
    html_temp   = get_template('base/mails/bienvenida.html')

    # Prepara imágenes que irán dentro del mail
    logo_url = os.path.join(settings.STATIC_ROOT, 'css/base/images/Coprovis.png')
    fp = open(logo_url, 'rb')
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header('Content-ID', '<{}>'.format('logo'))

    for miembro in queryset:

        # Renderiza los templates con el contexto apropiado
        # contexto    = Context({'nombre': miembro.usuario.first_name, 'sexo': miembro.sexo})
        contexto = {'nombre': miembro.usuario.first_name, 'sexo': miembro.sexo}
        txt_cnt     = txt_temp.render(contexto)
        html_cnt    = html_temp.render(contexto)

        try:
            # Se construye un objeto de mail al cual pueda ser adherido una alternativa html
            correo = EmailMultiAlternatives(subject = asunto, body = txt_cnt,
                                            from_email = settings.DEFAULT_FROM_EMAIL,
                                            to = [miembro.usuario.email],
                                            connection=mail_cnx)

            # Se adhiere alternativa html e imágenes preparadas
            correo.attach_alternative(html_cnt, "text/html")
            correo.attach(msg_img)

            # Se declara el mixed subtype
            correo.mixed_subtype = 'related'

            # Se envía el mail
            correo.send(fail_silently=False)

        except: no_mail += ', ' + miembro.usuario.username

    if len(no_mail) > 0:
        modeladmin.message_user(request,'Los usuarios: {} no tienen E-Mail asignado! Por favor asigne los emails en la Base de Datos "Usuarios"'.format(no_mail[2:]), level=ERROR)

    # Cierra conexión con el from_mail
    mail_cnx.close()

    return

# -------------------------------------------- Registro de Modelos --------------------------------------------

# # Hace visible el modelo User en el sitio del administrador
# @admin.register(User, site=mi_admin)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'email')
#     search_fields = ['username', 'first_name', 'last_name', 'email']

# Hace visible el modelo Ficha en el sitio del administrador
@admin.register(Ficha)
class FichaAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def ultimo_ingreso(self, instance):
        return instance.usuario.last_login
    def Nombre(self, instance):
        return instance.usuario.first_name
    def Apellido(self, instance):
        return instance.usuario.last_name
    def Mail(self, instance):
        return instance.usuario.email
    list_display = ('usuario', 'ultimo_ingreso','Nombre', 'Apellido', 'Mail', 'cel', 'pais', 'sexo', 'nacimiento', 'altura', 'kg_ini', 'kg_max',
                    'y_ow', 'kg_sal', 'cmplx', 'plan', 'inscrip')
    # list_editable = ('cel', 'pais', 'sexo', 'nacimiento', 'altura', 'kg_ini', 'kg_max','y_ow', 'kg_sal', 'cmplx',
    #                  'plan', 'inscrip')
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__email']
    radio_fields = {'sexo': admin.HORIZONTAL, 'cmplx': admin.HORIZONTAL, 'plan': admin.HORIZONTAL}
    actions = [dar_bienvenida]

# Hace visible el modelo Registro en el sitio del administrador
@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    def Nombre(self, instance):
        return instance.usuario.first_name
    def Apellido(self, instance):
        return instance.usuario.last_name
    def Mail(self, instance):
        return instance.usuario.email
    list_display = ('usuario', 'Nombre', 'Apellido', 'Mail', 'fecha', 'tipo', 'medida')
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__email']