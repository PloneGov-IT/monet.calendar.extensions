from plone.app.layout.viewlets.common import ViewletBase
from monet.calendar.extensions import eventMessageFactory as _
from monet.calendar.extensions.browser.usefulforsearch import UsefulForSearchEvents

class SearchBar(ViewletBase,UsefulForSearchEvents):
    """"""
    
    def monetAllEvents(self):
        return _(u'label_all_events', default=u'-- All events --')
    
    def valueGetEventType(self,value):
        if value=='all_events':
            return ''
        else:
            return value
        
    def getDefaultEventType(self):
        
        form = self.request.form
        
        if form.has_key('getEventType'):
            return form.get('getEventType')
        else:
            return ''
    
    def getDefaultDataParameter(self,elem,arg):
        
        form = self.request.form
        
        if form.has_key(arg):
            return int(elem['value']) == form.get(arg)
        else:
            return elem['selected']