from plone.app.layout.viewlets.common import ViewletBase
from monet.calendar.extensions import eventMessageFactory as _

class SearchBar(ViewletBase):
    """"""
    
    def monetAllEvents(self):
        return _(u'label_all_events', default=u'-- All events --')
    
    def valueGetEventType(self,value):
        if value=='all_events':
            return ''
        else:
            return value
        