from cms.models.pagemodel import Page
from cms.models.permissionmodels import PageUser
from django.contrib.auth.models import Permission, User
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from django_auth_ldap.backend import LDAPBackend

from django.core.management.base import BaseCommand, CommandError

from cms import constants
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms import api
from django.utils.translation import activate

class Command(BaseCommand):
	
	def add_arguments(self, parser):
		parser.add_argument('user',type=str)
		 
	def handle(self, *args, **options):
		activate('en')
		user=options['user']
		permisos=['Can add boostrap3 panel body plugin','Can change boostrap3 panel body plugin','Can add boostrap3 panel plugin','Can change boostrap3 panel plugin','Can add article','Can change article','Can delete article','Can add cms plugin','Can change cms plugin','Can delete cms plugin','Can add placeholder','Can change placeholder','Can delete placeholder','Can use Structure mode','Can add placeholder reference','Can change placeholder reference','Can add content type','Can change content type','Can delete content type']
	
		usuario=LDAPBackend().populate_user(user)
		if usuario is None:
			self.stdout.write(self.style.SUCCESS('No existe ese usuario en LDAP.'))
		else:
			for p in permisos:
				per=Permission.objects.get(name=str(p))
				usuario.user_permissions.add(per)
			usuario.save()
				
			if Page.objects.filter(created_by=user).count() <= 0:
				api.create_page_user(created_by=usuario,user=usuario,can_add_page=True)

				blog=NewsBlogConfig()
				blog.app_title=usuario.username
				blog.namespace=usuario.username
				blog.save()

				pagina=api.create_page(title=usuario.username,language='en',template=TEMPLATE_INHERITANCE_MAGIC,parent=None,in_navigation=True,created_by=usuario,apphook='NewsBlogApp',apphook_namespace=usuario.username) 
				api.assign_user_to_page(pagina,usuario,can_add=True,can_change=True,can_delete=True)
				pagina.publish('en')
				self.stdout.write(self.style.SUCCESS('Usuario creado con su pagina y blog propios.'))
			else:
				self.stdout.write(self.style.SUCCESS('El usuario ya tiene una pagina y blog.'))
