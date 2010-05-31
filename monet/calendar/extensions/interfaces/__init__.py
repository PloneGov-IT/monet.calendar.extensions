from zope.interface import Interface
from monet.calendar.event.interfaces import IMonetCalendar

class IMonetCalendarSection(IMonetCalendar):
    """Identifies folders on which you can use the view search events"""
    
    # -*- schema definition goes here -*-

class IMonetCalendarSearchRoot(Interface):
    """Identifies sub-folders, called sub-sites"""
    
    # -*- schema definition goes here -*-