from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form, YesNoSwitch

class RoleForm(Form):
    name = forms.CharField(max_length=255)
    layout = (
              (
               _("Basic Role Options"),
               (
                ('name', {'label': _("Role Name"), 'help_text': _("Role Name is used to identify this role in Admin Control Panel.")}),
                ),
              ),
             )
    