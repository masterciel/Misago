from django.utils.translation import ugettext_lazy as _
from django import forms
from mptt.forms import TreeNodeChoiceField
from misago.forms import Form, YesNoSwitch
from misago.forums.models import Forum

class CategoryForm(Form):
    parent = False
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea,required=False)
    closed = forms.BooleanField(widget=YesNoSwitch,required=False)
    style = forms.CharField(max_length=255,required=False)
    
    layout = (
              (
               _("Basic Options"),
               (
                ('parent', {'label': _("Category Parent")}),
                ('name', {'label': _("Category Name")}),
                ('description', {'label': _("Category Description")}),
                ('closed', {'label': _("Closed Category")}),
                ),
              ),
              (
               _("Display Options"),
               (
                ('style', {'label': _("Category Style"), 'help_text': _('You can add custom CSS classess to this category, to change way it looks on board index.')}),
                ),
              ),
             )
    
    def __init__(self, *args, **kwargs):
        self.base_fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(include_self=True),level_indicator=u'- - ')
        super(CategoryForm, self).__init__(*args, **kwargs)
    

class ForumForm(Form):
    parent = False
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea,required=False)
    closed = forms.BooleanField(widget=YesNoSwitch,required=False)
    style = forms.CharField(max_length=255,required=False)
    prune_start = forms.IntegerField(min_value=0,initial=0)
    prune_last = forms.IntegerField(min_value=0,initial=0)
    
    layout = (
              (
               _("Basic Options"),
               (
                ('parent', {'label': _("Forum Parent")}),
                ('name', {'label': _("Forum Name")}),
                ('description', {'label': _("Forum Description")}),
                ('closed', {'label': _("Closed Forum")}),
                ),
              ),
              (
               _("Prune Forum"),
               (
                ('prune_start', {'label': _("Delete threads with first post older than"), 'help_text': _('Enter number of days since topic start after which topic will be deleted or zero to don\'t delete topics.')}),
                ('prune_last', {'label': _("Delete threads with last post older than"), 'help_text': _('Enter number of days since since last reply in topic after which topic will be deleted or zero to don\'t delete topics.')}),
                ),
              ),
              (
               _("Display Options"),
               (
                ('style', {'label': _("Forum Style"), 'help_text': _('You can add custom CSS classess to this forum to change way it looks on forums lists.')}),
                ),
              ),
             )
    
    def __init__(self, *args, **kwargs):
        self.base_fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(),level_indicator=u'- - ')
        super(ForumForm, self).__init__(*args, **kwargs)
        

class RedirectForm(Form):
    parent = False
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea,required=False)
    redirect = forms.URLField(max_length=255)
    style = forms.CharField(max_length=255,required=False)
    
    layout = (
              (
               _("Basic Options"),
               (
                ('parent', {'label': _("Redirect Parent")}),
                ('name', {'label': _("Redirect Name")}),
                ('redirect', {'label': _("Redirect URL")}),
                ('description', {'label': _("Redirect Description")}),
                ),
              ),
              (
               _("Display Options"),
               (
                ('style', {'label': _("Redirect Style"), 'help_text': _('You can add custom CSS classess to this redirect to change way it looks on forums lists.')}),
                ),
              ),
             )
    
    def __init__(self, *args, **kwargs):
        self.base_fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(),level_indicator=u'- - ')
        super(RedirectForm, self).__init__(*args, **kwargs)
    

class DeleteForm(Form):
    parent = False
   
    layout = (
              (
               _("Delete Options"),
               (
                ('parent', {'label': _("Move deleted Forum contents to")}),
                ),
              ),
             )
        
    def __init__(self, *args, **kwargs):
        self.base_fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(),required=False,empty_label=_("Remove with forum"),level_indicator=u'- - ')
        super(DeleteForm, self).__init__(*args, **kwargs)