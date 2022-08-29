import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.xcaret.blueprint import xcaret
from ckanext.xcaret import helpers as h

class XcaretPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)    

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'xcaret')
        toolkit.add_resource('assets', 'xcaret')

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        unicode_safe = toolkit.get_validator('unicode_safe')
        validators = [ignore_missing, str]

        schema.update({
            'ckan.hero': validators,
        'hero_upload': [ignore_missing, unicode_safe],
        'clear_hero_upload': [ignore_missing, unicode_safe],            
        })

        return schema


    def get_blueprint(self):
        return [xcaret]

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'all_organizations': h.get_all_organizations,
            'latest_datasets': h.get_latest_datasets,
            'featured_pages': h.get_featured_pages

        }
