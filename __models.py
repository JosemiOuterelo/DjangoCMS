from django.db import models
from cms.models.pagemodel import Page
from cms.models.permissionmodels import PageUser
from django.contrib.auth.models import Permission, User
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from django_auth_ldap.backend import LDAPBackend

from cms import constants
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms import api
from django.utils.translation import activate

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def alta(sender,user,request,**kwargs):
	if user.username != "administrador":
		activate('en')
		try:
			Page.objects.get(created_by=user.username)
		except Page.DoesNotExist:
			permisos=['Can add boostrap3 panel body plugin','Can change boostrap3 panel body plugin','Can add boostrap3 panel plugin','Can change boostrap3 panel plugin','Can add article','Can change article','Can delete article','Can add cms plugin','Can change cms plugin','Can delete cms plugin','Can add placeholder','Can change placeholder','Can delete placeholder','Can use Structure mode','Can add placeholder reference','Can change placeholder reference','Can add content type','Can change content type','Can delete content type']
			usuario=User.objects.get(username=user.username)
			for p in permisos:
				per=Permission.objects.get(name=str(p))
               	        	usuario.user_permissions.add(per)
                	usuario.save()				
			api.create_page_user(created_by=usuario,user=usuario,can_add_page=True)
			blog=NewsBlogConfig()
			blog.app_title=usuario.username
			blog.namespace=usuario.username
			blog.save()
			pagina=api.create_page(title=usuario.username,language='en',template=TEMPLATE_INHERITANCE_MAGIC,parent=None,created_by=usuario,apphook='NewsBlogApp',apphook_namespace=usuario.username) 
			api.assign_user_to_page(pagina,usuario,can_add=True,can_change=True,can_delete=True)
			pagina.publish('en')
			print("Usuario creado con su pagina y blog propios")
		else:
			print("El usuario ya tiene una pagina y blog.")

