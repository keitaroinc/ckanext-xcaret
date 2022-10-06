import six
import re

from ckan.common import g, config
import ckan.lib.helpers as h
from flask import Blueprint
import ckan.logic as logic
from ckan.common import g, _, config, request
import ckan.lib.base as base
from flask.views import MethodView
import ckan.lib.navl.dictization_functions as dict_fns
from ckan.views.home import CACHE_PARAMETERS
import ckan.lib.uploader as uploader
import ckan.lib.navl.dictization_functions as dfunc

_validate = dfunc.validate


xcaret = Blueprint('xcaret', __name__)


def _get_config_options_xcaret():
    styles = [{
        u'text': u'Default',
        u'value': u'/base/css/main.css'
    }, {
        u'text': u'Red',
        u'value': u'/base/css/red.css'
    }, {
        u'text': u'Green',
        u'value': u'/base/css/green.css'
    }, {
        u'text': u'Maroon',
        u'value': u'/base/css/maroon.css'
    }, {
        u'text': u'Fuchsia',
        u'value': u'/base/css/fuchsia.css'
    }]

    homepages = [{
        u'value': u'1',
        u'text': (u'Introductory area, search, featured'
                  u' group and featured organization')
    }, {
        u'value': u'2',
        u'text': (u'Search, stats, introductory area, '
                  u'featured organization and featured group')
    }, {
        u'value': u'3',
        u'text': u'Search, introductory area and stats'
    }, {
        u'value': u'4',
        u'text': u'XCaret theme'
    }]

    return dict(styles=styles, homepages=homepages)


class ConfigViewXCaret(MethodView):
    def get(self):
        items = _get_config_options_xcaret()
        schema = logic.schema.update_configuration_schema()
        data = {}

        for key in schema:
            data[key] = config.get(key)

        vars = dict(data=data, errors={}, **items)

        return base.render(u'admin/config.html', extra_vars=vars)

    def post(self):
        try:
            req = request.form.copy()
            req.update(request.files.to_dict())

            data_dict = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(
                        logic.parse_params(req,
                                           ignore_keys=CACHE_PARAMETERS))))

            del data_dict['save']

            upload = uploader.get_uploader('admin')
            upload.update_data_dict(data_dict, 'ckan.hero',
                                    'hero_upload', 'clear_hero_upload')
            upload.upload(uploader.get_max_image_size())

            for key, value in six.iteritems(data_dict):

                # Set full Logo url
                if key == 'ckan.hero' and value and not value.startswith('http')\
                        and not value.startswith('/'):
                    image_path = 'uploads/admin/'

                    value = h.url_for_static('{0}{1}'.format(image_path, value))
                    data_dict[key] = value

            # update ckan.site_custom_css
            custom_css = create_custom_css(data_dict)
            
            data_dict['ckan.site_custom_css'] = custom_css
                  
            data = logic.get_action(u'config_option_update')({
                u'user': g.user
            }, data_dict)

        except logic.ValidationError as e:
            items = _get_config_options_xcaret()
            data = request.form
            errors = e.error_dict
            error_summary = e.error_summary
            vars = dict(data=data,
                        errors=errors,
                        error_summary=error_summary,
                        form_items=items,
                        **items)
            return base.render(u'admin/config.html', extra_vars=vars)

        return h.redirect_to(u'admin.config')


def create_custom_css(config):
    # Generate custom css according to selected colors
    site_custom_css = ''
    hero = config.get('ckan.hero')

    if len(hero) > 0:
        hero_css = '.hero-upload { background: url("' +  hero + '"); background-position: center; background-repeat: no-repeat; background-size: cover;}'
        site_custom_css += hero_css

    custom_css = config.get('ckan.site_custom_css')
    custom_css = re.sub('.hero-upload.*}', '', custom_css)

    if len(custom_css) != 0:
        site_custom_css += custom_css

    return site_custom_css


xcaret.add_url_rule(u'/ckan-admin/config', view_func=ConfigViewXCaret.as_view(str(u'config')))