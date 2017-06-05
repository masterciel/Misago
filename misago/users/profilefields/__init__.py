from django.utils.module_loading import import_string

from misago.conf import settings

from .base import ProfileField, TextProfileField, TextareaProfileField


class ProfileFields(object):
    def __init__(self, fields_groups):
        self.is_loaded = False

        self.fields_groups = fields_groups
        self.fields_dict = {}

    def load(self):
        self.fields_dict = {}

        for group in self.fields_groups:
            for field_path in group['fields']:
                field = import_string(field_path)
                field._field_path = field_path
                if not field.fieldname:
                    raise ValueError(
                        "{} profile field has to specify fieldname attribute".format(
                            field._field_path,
                        )
                    )
                if field.fieldname in self.fields_dict:
                    raise ValueError(
                        (
                            '{} profile field defines fieldname "{}" '
                            'that is already in use by the {}'
                        ).format(
                            field._field_path,
                            field.fieldname,
                            dict_from_map[field.fieldname]._field_path,
                        )
                    )
                self.fields_dict[field_path] = field()

        self.is_loaded = True

    def update_admin_form(self, form):
        if not self.is_loaded:
            self.load()

        for group in self.fields_groups:
            group_dict = {
                'name': group['name'],
                'fields': [],
            }

            for field_path in group['fields']:
                field = self.fields_dict[field_path]
                admin_field = field.get_admin_field(form.instance)
                if admin_field:
                    form.fields[field.fieldname] = admin_field
                    group_dict['fields'].append(field.fieldname)

            form._profile_fields_groups.append(group_dict)

    def clean_admin_form(self, form, data):
        for field in self.fields_dict.values():
            data = field.clean_admin_form(form, data) or data
        return data

    def admin_update_extra(self, user, cleaned_data):
        for field in self.fields_dict.values():
            field.admin_update_extra(user, cleaned_data)


profilefields = ProfileFields(settings.MISAGO_PROFILE_FIELDS)
