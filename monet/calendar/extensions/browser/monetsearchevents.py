from Products.Five.browser import BrowserView
from monet.calendar.extensions.interfaces import IMonetCalendarSection, IMonetCalendarSearchRoot
from monet.calendar.event.interfaces import IMonetEvent
from Acquisition import aq_chain
from Products.CMFCore.utils import getToolByName
from datetime import datetime, timedelta
from monet.calendar.extensions import eventMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter
from monet.calendar.extensions.browser.usefulforsearch import UsefulForSearchEvents

class MonetSearchEvents(BrowserView,UsefulForSearchEvents):
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
    
    def getEventsInParent(self,parent):
        """Return all events found in the parent folder"""
        pcatalog = getToolByName(self, 'portal_catalog')
        query = {}
        query['object_provides'] = IMonetEvent.__identifier__
        query['path'] = parent.getPath()
        query['sort_on'] = 'getObjPositionInParent'
        if self.request.form.get('SearchableText'):
            query['SearchableText'] = self.request.form.get('SearchableText')
        if self.request.form.get('getEventType'):
            query['getEventType'] = self.request.form.get('getEventType')
        brains = pcatalog.searchResults(**query)
        return brains
    
    def getEventsFromTo(self,events):
        """Filter events by date"""
        
        form = self.request.form
        
        if form.get('date'):
            date = form.get('date').split('-')
            date_from = date_to = datetime(int(date[0]),int(date[1]),int(date[2])).date()
            filtered_events = self.filterEventsByDate(events,date_from,date_to)
            return filtered_events
        elif self.notEmptyArgumentsDate(form.get('fromDay'),form.get('fromMonth'),form.get('fromYear')) or self.notEmptyArgumentsDate(form.get('toDay'),form.get('toMonth'),form.get('toYear')):
            date_from = self.writeDate(form.get('fromDay'),form.get('fromMonth'),form.get('fromYear'))
            date_to = self.writeDate(form.get('toDay'),form.get('toMonth'),form.get('toYear'))
            if not date_from or not date_to:
                message_error = _(u'label_failed_arguments', default=u'The date arguments are not valid, re-enter the dates, please.')
                IStatusMessage(self.request).addStatusMessage(message_error,type="error")
                url = getMultiAdapter((self.context, self.request),name='absolute_url')()
                self.request.response.redirect(url + '/@@monetsearchevents')
                return 
            elif self.checkInvalidDateGreaterThan(date_from,date_to):
                message_error = _(u'label_failed_gtinterval', default=u'The second data parameter (TO) must be greater than or equal to the first data parameter (FROM), so that the range of days specified is not negative. Re-enter the dates, please.')
                IStatusMessage(self.request).addStatusMessage(message_error,type="error")
                url = getMultiAdapter((self.context, self.request),name='absolute_url')()
                self.request.response.redirect(url + '/@@monetsearchevents')
                return
            elif self.checkInvalidDateInterval(date_from,date_to):
                message_error = _(u'label_failed_interval', default=u'The search of events must be less than 30 days. Re-enter the dates, please.')
                IStatusMessage(self.request).addStatusMessage(message_error,type="error")
                url = getMultiAdapter((self.context, self.request),name='absolute_url')()
                self.request.response.redirect(url + '/@@monetsearchevents')
                return
            else:
                filtered_events = self.filterEventsByDate(events,date_from,date_to)
                return filtered_events
        else:
            date_from = date_to = datetime.now().date()
            filtered_events = self.filterEventsByDate(events,date_from,date_to)
            return filtered_events
        
    def notEmptyArgumentsDate(self,day,month,year):
        """Check the date viewlets's parameters"""
        if day or month or year:
            return True
        else:
            return False
    
    def writeDate(self,day,month,year):
        """Up the date"""
        try:
            date = datetime(year,month,day).date()
            return date
        except StandardError:
            return None
        
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
    
    def filterEventsByDate(self,events,date_from,date_to):
        """Filter events by date"""
        filtered_events = []
        interval = []
        duration = (date_to - date_from).days
        while(duration > 0):
            day = date_to - timedelta(days=duration)
            interval.append(day)
            duration -= 1
        interval.append(date_to)
        
        for event in events:
            dates_event = event.getObject().getDates()
            if set(interval).intersection(set(dates_event)):
                filtered_events.append(event)

        return filtered_events
        