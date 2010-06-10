from plone.app.layout.viewlets.common import ViewletBase
from monet.calendar.extensions import eventMessageFactory as _
from monet.calendar.extensions.browser.usefulforsearch import UsefulForSearchEvents
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import DisplayList

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
        
    def getEventTypeName(self,key):
        mp = getToolByName(self,'portal_properties')
        
        event_types_pro = mp.monet_calendar_event_properties.event_types
        event_types = DisplayList()
        for etype in event_types_pro:
            event_types.add(etype,_(etype))
        
        return event_types.getValue(key)