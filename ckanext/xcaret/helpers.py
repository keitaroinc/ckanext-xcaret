from ckan import model
import ckan.plugins as p
from ckan.common import c
import ckan.logic as logic

def get_all_organizations(include_dataset_count=True):
    '''Return a list of organizations that the current user has the specified
    permission for.
    '''
    context = {'user': c.user}
    data_dict = {
        'include_dataset_count': include_dataset_count,
        'all_fields': True}
    return logic.get_action('organization_list')(context, data_dict)


def get_latest_datasets():
    '''Return a list of the latest datasets that the current user has the specified
    permission for.
    '''
    context = {'user': c.user}
    data_dict = {'sort': 'metadata_modified desc', 'rows': 4 }

    datasets = logic.get_action('package_search')(context, data_dict)
    return datasets.get('results', [])


def get_featured_pages(limit=3):
    data_dict = {'org_id': None, 'page_type': 'blog'}
    context = {'model': model, 'user': c.user,
               'auth_user_obj': c.userobj}
    pages = p.toolkit.get_action('ckanext_pages_list')(context, data_dict)
    pages = pages[:limit]
    #featured = [page for page in pages if page['featured']]
    return pages[:limit]
