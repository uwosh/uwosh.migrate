from zope import interface, schema
from zope.formlib import form
from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase

from pagemigrater import PageMigrater

# Begin ugly hack. It works around a ContentProviderLookupError: plone.htmlhead error caused by Zope 2 permissions.
#
# Source: http://athenageek.wordpress.com/2008/01/08/contentproviderlookuperror-plonehtmlhead/
# Bug report: https://bugs.launchpad.net/zope2/+bug/176566
#

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

def _getContext(self):
    self = self.aq_parent
    while getattr(self, '_is_wrapperish', None):
        self = self.aq_parent
    return self    
            
ZopeTwoPageTemplateFile._getContext = _getContext

# End ugly hack.

class IMigrate(interface.Interface):
    root_url = schema.TextLine(title=u'Root URL', description=u'The Root URL', required=True)
    urls = schema.Text(title=u'URLs', description=u'The URLs to migrate', required=True)
    
class MigratePagesForm(formbase.PageForm):
    form_fields = form.FormFields(IMigrate)
    result_template = pagetemplatefile.ZopeTwoPageTemplateFile('migration-results.pt')

    @form.action("Migrate")
    def action_migrate(self, action, data):
       
        urls = data['urls'].split()
        
        migrater = PageMigrater(self.context)
        migrater.migrate_pages(urls, data['root_url'])
        
        self.log = migrater.get_log()
        self.errors = migrater.get_errors()
        
        return self.result_template()
        
        
  
