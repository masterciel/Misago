from django.utils.translation import ugettext_lazy as _
from misago.acl import algebra
from misago.acl.models import Role
from misago.core import forms


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Account settings")
    name_changes_allowed = forms.IntegerField(
        label=_("Allowed username changes number"),
        min_value=0,
        initial=1)
    name_changes_expire = forms.IntegerField(
        label=_("Don't count username changes older than"),
        help_text=_("Number of days since name change that makes that change no longer count to limit. Enter zero to make all changes count."),
        min_value=0,
        initial=0)
    can_have_signature = forms.YesNoSwitch(
        label=_("Can have signature"),
        initial=False)
    allow_signature_links = forms.YesNoSwitch(
        label=_("Can put links in signature"),
        initial=False)
    allow_signature_images = forms.YesNoSwitch(
        label=_("Can put images in signature"),
        initial=False)


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != 'anonymous':
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    new_acl = {
        'name_changes_allowed': 0,
        'name_changes_expire': 0,
        'can_have_signature': False,
        'allow_signature_links': False,
        'allow_signature_images': False,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
            new_acl, roles=roles, key=key_name,
            name_changes_allowed=algebra.greater,
            name_changes_expire=algebra.lower,
            can_have_signature=algebra.greater,
            allow_signature_links=algebra.greater,
            allow_signature_images=algebra.greater
            )
