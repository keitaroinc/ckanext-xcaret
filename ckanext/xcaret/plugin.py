import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultPermissionLabels
from ckan.plugins.toolkit import get_action
from ckan.authz import check_config_permission

from ckanext.xcaret.blueprint import xcaret
from ckanext.xcaret import helpers as h
from ckan.lib.plugins import DefaultTranslation

class XcaretPlugin(plugins.SingletonPlugin, DefaultTranslation, DefaultPermissionLabels):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)   
    plugins.implements(plugins.ITranslation)  
    plugins.implements(plugins.IPermissionLabels)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'xcaret')
        toolkit.add_resource('assets', 'xcaret')
        

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        unicode_safe = toolkit.get_validator('unicode_safe')
        validators = [ignore_missing, str]

        schema.update({
        'ckan.hero': validators,
        'hero_upload': [ignore_missing, unicode_safe],
        'clear_hero_upload': [ignore_missing, unicode_safe],
        'ckan.footer_links_name_1': validators,
        'ckan.footer_links_1': validators,
        'ckan.footer_links_name_1_en': validators,
        'ckan.footer_links_1_en': validators,        
        'ckan.footer_links_name_2': validators,
        'ckan.footer_links_2': validators,
        'ckan.footer_links_name_2_en': validators,
        'ckan.footer_links_2_en': validators,        
        'ckan.footer_links_name_3': validators,
        'ckan.footer_links_3': validators,
        'ckan.footer_links_name_3_en': validators,
        'ckan.footer_links_3_en': validators,        
        'ckan.footer_links_name_4': validators,
        'ckan.footer_links_4': validators,
        'ckan.footer_links_name_4_en': validators,
        'ckan.footer_links_4_en': validators,        
        'ckan.footer_links_name_5': validators,
        'ckan.footer_links_5': validators,
        'ckan.footer_links_name_5_en': validators,
        'ckan.footer_links_5_en': validators,
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

    # IPermissionLabels
    def get_dataset_labels(self, dataset_obj):
        u'''
        Use creator-*, admin-* and collaborator-*
        labels for Restricted datasets
        '''
        if dataset_obj.notes.startswith(u'Restricted:'):

            labels = [u'creator-%s' % dataset_obj.creator_user_id]

            # This gives right to the admins of the organization
            # if the dataset belongs to any
            # We can disable it if requested
            if dataset_obj.owner_org:
                labels += [u'admin-%s' % dataset_obj.owner_org]

            if check_config_permission('allow_dataset_collaborators'):
                # Add a generic label for all this dataset collaborators
                labels += [u'collaborator-%s' % dataset_obj.id]

            return labels

        return super(XcaretPlugin, self).get_dataset_labels(
            dataset_obj)

    def get_user_dataset_labels(self, user_obj):
        u'''
        Include admin-* labels for users in addition to default labels
        creator-*, collaborator-* and public
        '''
        labels = super(XcaretPlugin, self
                       ).get_user_dataset_labels(user_obj)

        # This gives right to the user to see the dataset
        # if the dataset belongs to an organization
        # and the user is admin to that organization
        # We can disable it if requested
        if user_obj:
            orgs = get_action(u'organization_list_for_user')(
                {u'user': user_obj.id}, {u'permission': u'admin'})
            labels.extend(u'admin-%s' % o['id'] for o in orgs)

        return labels
