#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Para crear formularios
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Button, Submit, HTML
from crispy_forms.bootstrap import FormActions, PrependedText, AppendedText
from django.contrib.auth.models import User

# Para crear formularios basados en modelos
from django.forms import ModelForm
from .models import Registro

class forma_login(forms.Form):
    mail = forms.CharField(label="E-Mail", max_length=30, required=False)
    mail.widget.attrs['autofocus'] = True
    password = forms.CharField(label="Password",max_length=12, widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(forma_login, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class  = 'form-horizontal'
        self.helper.field_class = 'col-xs-12'
        self.helper.form_method = 'post'
        self.helper.form_action = 'base:login'

        self.helper.layout = Layout(Fieldset(None,Field('mail', placeholder='E-Mail'),
                                             Field('password', placeholder='Password')),
                                    FormActions(Submit('ingresar','Ingresar')))

        self.helper.form_show_labels = False

class forma_contacto(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100, required=True)
    nombre.widget.attrs['autofocus'] = True
    email = forms.EmailField(label="E-Mail", max_length=50, required=True)
    phone = forms.CharField(label="Teléfono", max_length=50, required=False)
    msj = forms.CharField(label="Mensaje", max_length=1000, widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super(forma_contacto, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-xs-12'
        self.helper.field_class = 'col-xs-12'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

        self.helper.layout = Layout(Fieldset(None,Field('nombre', placeholder='Nombre y apellido'),
                                             Field('email', placeholder='E-Mail'),
                                             Field('phone', placeholder=u'(+ Código de Área) Teléfono'),
                                             Field('msj', placeholder='Mensaje'),),
                                    FormActions(Submit('enviar','Enviar formulario')))

        self.helper.form_show_labels = False

class forma_peso(forms.Form):
    fecha   = forms.DateField(label=u'Fecha', widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    peso    = forms.FloatField(label=u'Peso', required=False)

    def __init__(self, *args, **kwargs):
        super(forma_peso, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = 'base:descenso'
        # self.helper.label_class = 'col-xs-3'
        # self.helper.field_class = 'col-xs-6'

        self.helper.layout = Layout(HTML('<span style="color: #006076; font-size: large;">Registro Semanal de Peso:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'),
                                    Field('fecha', placeholder='YYYY-MM-DD'), AppendedText('peso', 'Kg', placeholder='Peso'),
                                    Submit('anotar_peso','Anotar'),
                                    Submit('consultar_peso', 'Consultar', css_class='btn btn-success')
                                    )

        # self.helper.layout = Layout(Fieldset('Registro Semanal de Peso', Field('fecha', placeholder='Fecha mm/dd/yy'),
        #                                      AppendedText('peso', 'Kg', placeholder='Peso')),
        #                             FormActions(Submit('anotar','Anotar'),
        #                                         Submit('consultar','Consultar', css_class='btn btn-success'))
        #                             )

        self.helper.form_show_labels = False

class forma_perimetro(forms.Form):
    fecha   = forms.DateField(label=u'Fecha', widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    cintura = forms.FloatField(label=u'Cintura', required=False)
    cadera = forms.FloatField(label=u'Cadera', required=False)

    def __init__(self, *args, **kwargs):
        super(forma_perimetro, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = 'base:descenso'

        self.helper.layout = Layout(HTML('<span style="color: #006076; font-size: large;">Perimetro:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'),
                                    Field('fecha', placeholder='YYYY-MM-DD'), AppendedText('cintura', 'cm', placeholder='Cintura'),
                                    AppendedText('cadera', 'cm', placeholder='Cadera'),
                                    Submit('anotar_perimetro','Anotar'),
                                    Submit('consultar_perimetro', 'Consultar', css_class='btn btn-success')
                                    )

        self.helper.form_show_labels = False

class forma_user_config(forms.Form):
    # usuario = forms.CharField(label=u'Usuario:', max_length=12)
    mail = forms.CharField(label=u'Mail:', max_length=100)
    nombre = forms.CharField(label=u'Nombre:', max_length=100)
    apellido = forms.CharField(label=u'Apellido:', max_length=100)

    def __init__(self, *args, **kwargs):
        super(forma_user_config, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-3'
        self.helper.form_method = 'post'
        self.helper.form_action = 'base:cuenta'

        # self.helper.layout = Layout(Fieldset(None, Field('usuario'),Field('nombre'),Field('apellido'),
        #                                      Field('mail'),),
        #                             FormActions(Submit('guardar','Guardar', css_class='btn btn-success')))
        self.helper.layout = Layout(Fieldset(None, Field('mail', disabled=True),Field('nombre'),Field('apellido'),),
                                    FormActions(Submit('guardar','Guardar', css_class='btn btn-success')))

class forma_chg_psw(forms.Form):
    psw1 = forms.CharField(label="Password",max_length=12, widget=forms.PasswordInput)
    psw2 = forms.CharField(label="Repetir Password",max_length=12, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(forma_chg_psw, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-3'
        self.helper.form_method = 'post'
        self.helper.form_action = 'base:cuenta'

        self.helper.layout = Layout(Fieldset(None, Field('psw1'), Field('psw2')),
                                    FormActions(Submit('psw_chg','Cambiar', css_class='btn btn-warning')))

class forma_verComo(forms.Form):
    ver_como = forms.ChoiceField(label="Ver como", choices=[])

    def __init__(self, *args, **kwargs):
        super(forma_verComo, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = 'base:control'

        self.helper.layout = Layout(HTML('<span style="color: #006076; font-size: large;">Ver Como:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'),
                                    Field('ver_como'), Submit('ver','Ver'))

        self.helper.form_show_labels = False

