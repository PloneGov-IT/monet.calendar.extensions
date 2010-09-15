# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.common import ViewletBase
from monet.calendar.extensions import eventMessageFactory as _
from monet.calendar.extensions.browser.usefulforsearch import UsefulForSearchEvents
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import DisplayList

from DateTime import DateTime

class SearchBar(ViewletBase, UsefulForSearchEvents):
    """Search form viewlet for enabled content types"""
    
    def __init__(self, context, request, view, manager):
        ViewletBase.__init__(self, context, request, view, manager)
        now = DateTime()
        self.today = now.strftime("%Y-%m-%d").split("-")
    
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
            # return today date
            if arg=='fromDay' or arg=='toDay':
                return int(self.today[2])==int(elem['value'])
            elif arg=='fromMonth' or arg=='toMonth':
                return int(self.today[1])==int(elem['value'])
            elif arg=='fromYear' or arg=='toYear':
                return int(self.today[0])==int(elem['value'])
        
    def getEventTypeName(self,key):
        mp = getToolByName(self,'portal_properties')
        
        event_types_pro = mp.monet_calendar_event_properties.event_types
        event_types = DisplayList()
        for etype in event_types_pro:
            event_types.add(etype,_(etype))
        
        return event_types.getValue(key)