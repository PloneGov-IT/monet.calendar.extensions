# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from monet.calendar.event.interfaces import IMonetEvent
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from datetime import datetime, timedelta
from monet.calendar.extensions import eventMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory
from Products.Archetypes.atapi import DisplayList

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

try:
    # python2.6
    import json
except ImportError:
    # python2.4
    import simplejson as json


PLMF = MessageFactory('plonelocales')

SlotsVocab = {'morning':_(u'Morning'),
              'afternoon':_(u'Afternoon'),
              'night':_(u'Evening'),
              'allday':_(u'All day long')}

ParameterDatesList = ['fromYear',
                      'fromMonth',
                      'fromDay',
                      'toYear',
                      'toMonth',
                      'toDay']

class MonetFormSearchValidation(BrowserView):
    """Simple view for perform AJAX form validation"""

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self._translation_service = getToolByName(self.context, 'translation_service')

    def _validate(self, date_from, date_to, directLocalization=False):
        """Perform a date validation
        return the error message or an empty string is validation pass
        """
        key = default = None
        message_error = ''
        if not date_from or not date_to:
            key, default = (u'label_failed_arguments',
                            u'Dates are not valid, please retry.')
        elif self.checkInvalidDateGreaterThan(date_from,date_to):
            key, default = (u'label_failed_gtinterval',
                            u'The second date (TO) must be greater than or equal to the first date (FROM). Please re-enter dates.')
        elif self.checkInvalidDateInterval(date_from,date_to):
            key, default = (u'label_failed_interval',
                            u'The search of events must be inside a range or 30 days. Please re-enter dates.')
        if key:
            if not directLocalization:
                message_error = _(key, default=default)
            else:
                translation_service = getToolByName(self.context,'translation_service')
                message_error = self._translation_service.utranslate(domain='monet.calendar.extensions',
                                                                     msgid=key,
                                                                     default=default,
                                                                     context=self.context)
        return message_error

    def checkInvalidDateGreaterThan(self,date_from,date_to):
        """Check the dates DAL AL"""
        if date_to >= date_from:
            return False
        else:
            return True
        
    def checkInvalidDateInterval(self,date_from,date_to):
        """Check the dates DAL AL"""
        if not (date_to - date_from).days > 30:
            return False
        else:
            return True

    def writeDate(self, day, month, year):
        """Up the date"""
        try:
            date = datetime(int(year),int(month),int(day)).date()
            return date
        except StandardError:
            self.context.plone_log("Error in date conversion: %s" % str(int(year),int(month),int(day)))
            return ''

    def __call__(self, *args, **kw):
        response = self.request.response
        response.setHeader('content-type','application/json');
        response.addHeader("Cache-Control", "no-cache")
        response.addHeader("Pragma", "no-cache")

        form = self.request.form
        date_from = self.writeDate(form.get('fromDay'),form.get('fromMonth'),form.get('fromYear'))
        date_to = self.writeDate(form.get('toDay'),form.get('toMonth'),form.get('toYear'))
        message_error = self._validate(date_from, date_to, directLocalization=True)
        
        return json.dumps({'title': u'!!!',
                           'error': message_error})


class MonetSearchEvents(BrowserView, MonetFormSearchValidation):
    """View for the events search page"""

    template = ViewPageTemplateFile("monetsearchevent.pt")
    
    def __call__(self, *args, **kw):
        return self.template()

    def notEmptyArgumentsDate(self,day,month,year):
        """Check the date viewlets's parameters"""
        if day or month or year:
            return True
        else:
            return False

    def getFromTo(self):
        """Create dates from the parameters"""
        
        date = date_from = date_to = ''
        dates = {'date':'','date_from':'','date_to':''}
        form = self.request.form
        
        if form.get('date'):
            date = form.get('date').split('-')
            date = datetime(int(date[0]),int(date[1]),int(date[2])).date()
            
        if self.notEmptyArgumentsDate(form.get('fromDay'),form.get('fromMonth'),form.get('fromYear')) or self.notEmptyArgumentsDate(form.get('toDay'),form.get('toMonth'),form.get('toYear')):
            date_from = self.writeDate(form.get('fromDay'),form.get('fromMonth'),form.get('fromYear'))
            date_to = self.writeDate(form.get('toDay'),form.get('toMonth'),form.get('toYear'))
            message_error = self._validate(date_from, date_to)
            if message_error:
                IStatusMessage(self.request).addStatusMessage(message_error,type="error")
            
            # BBB: silly redirect... perform validation BEFORE page rendering!
            url = getMultiAdapter((self.context, self.request),name='absolute_url')()
            self.request.response.redirect(url + '/@@monetsearchevents')
        
        if date_from and date_to and date_from == date_to:
            dates = {'date':date or date_from}
        else:
            dates = {'date':date or date_from,'date_from':date_from,'date_to':date_to}
        
        if dates['date']:
            return dates
        else:
            date = datetime.now().date()
            dates = {'date':date}
            return dates

    def getEventsInParent(self):
        """Return all events found in the parent folder"""
        context = aq_inner(self.context)
        pcatalog = getToolByName(self, 'portal_catalog')
        query = {}
        query['object_provides'] = IMonetEvent.__identifier__
        query['sort_on'] = 'getObjPositionInParent'
        
        for key in self.request.form.keys():
            if not key in ParameterDatesList:
                if self.request.form.get(key):
                    query[key] = self.request.form.get(key)
        
        brains = pcatalog.searchResults(**query)
        return brains    
    
    def filterEventsByDate(self, events, date):
        """Filter events by date"""
        
        filtered_events = []
        
        for event in events:
            #event = event.getObject()
            dates_event = event.getDates
            if date in dates_event:
                filtered_events.append(event)
        return filtered_events
    
    def sortedEventsBySlots(self,events):
        """Sorted events by slot"""
        
        mp = getToolByName(self,'portal_properties')
        special_event_types_pro = mp.monet_calendar_event_properties.special_event_types
        special_event_types = DisplayList()
        for etype in special_event_types_pro:
            special_event_types.add(etype,_(etype))
    
        sorted_events = {'morning':[],
                         'afternoon':[],
                         'night':[],
                         'allday':[],
                         'sequence_slots':['morning','afternoon','night','allday']}
        sorted_events_keys = sorted_events.keys()
        
        for event in events:
            inter = list(set(event.getEventType).intersection(set(special_event_types)))
            if inter:
                if not inter[0] in sorted_events['sequence_slots']:
                    sorted_events['sequence_slots'].append(inter[0])
                    sorted_events[inter[0]] = []
                sorted_events[inter[0]].append(event)
                continue
            for key in sorted_events_keys:
                if event.getSlots() == key:
                    sorted_events[key].append(event)
        return sorted_events
    
    def getDateInterval(self,date_from,date_to):
        interval = []
        duration = (date_to - date_from).days
        while(duration > 0):
            day = date_to - timedelta(days=duration)
            interval.append(day)
            duration -= 1
        interval.append(date_to)
        return interval
    
    def getPreviousDate(self,date,date_from):
        if date == date_from:
            return None
        else:
            return date - timedelta(1)
    
    def getNextDate(self,date,date_to):
        if date == date_to:
            return None
        else:
            return date + timedelta(1)
        
    def getWeekdayName(self,date):
        msgid = date.isoweekday() == 7 and self._translation_service.day_msgid(0) or self._translation_service.day_msgid(date.isoweekday())
        english = date.isoweekday() == 7 and self._translation_service.weekday_english(0) or self._translation_service.weekday_english(date.isoweekday())
        return _(msgid, default=english)
        
    def getMonthName(self,date):
        msgid   = self._translation_service.month_msgid(date.month)
        english = self._translation_service.month_english(date.month)
        return PLMF(msgid, default=english)
    
    def getSlotsName(self,key):
        mp = getToolByName(self,'portal_properties')
        
        special_event_types_pro = mp.monet_calendar_event_properties.special_event_types
        special_event_types = DisplayList()
        for etype in special_event_types_pro:
            special_event_types.add(etype,_(etype))
        
        return (key in special_event_types) and special_event_types.getValue(key) or SlotsVocab[key]
