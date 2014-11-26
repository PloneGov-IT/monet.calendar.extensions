from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime
from monet.calendar.extensions.browser.usefulforsearch import UsefulForSearchEvents
from plone import api


class IMonetSearchPortlet(IPortletDataProvider):
    """ """


class Assignment(base.Assignment):
    implements(IMonetSearchPortlet)

    @property
    def title(self):
        return 'Form ricerca eventi'


class Renderer(base.Renderer, UsefulForSearchEvents):

    _template = ViewPageTemplateFile('searchportlet.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        now = DateTime()
        self.today = now.strftime("%Y-%m-%d").split("-")
        self.pl = api.portal.get_tool('portal_languages')

    def render(self):
        return xhtml_compress(self._template())

    def getDefaultEventType(self):

        form = self.request.form

        if 'getEventType' in form:
            return form.get('getEventType')
        else:
            return ''

    def getDefaultDataParameter(self, elem, arg):

        form = self.request.form

        if arg in form:
            return int(elem['value']) == form.get(arg)
        else:
            # return today date
            if arg == 'fromDay' or arg == 'toDay':
                return int(self.today[2]) == int(elem['value'])
            elif arg == 'fromMonth' or arg == 'toMonth':
                return int(self.today[1]) == int(elem['value'])
            elif arg == 'fromYear' or arg == 'toYear':
                return int(self.today[0]) == int(elem['value'])

    def usedEventTypes(self):
        translation_service = api.portal.get_tool('translation_service')
        pc = api.portal.get_tool('portal_catalog')
        used_event_types = []
        #add first element
        label = translation_service.utranslate(msgid=u'label_all_events',
                                               default=u'-- All events --',
                                               domain="monet.calendar.extensions",
                                               context=self)
        first_element = [('', label), ]
        #get the EventType
        try:
            used_get_event_type = pc.uniqueValuesFor('getEventType')
        except KeyError:
            used_get_event_type = []
        for event_type in used_get_event_type:
            if not isinstance(event_type, unicode):
                event_type = event_type.decode('utf8')
            label = translation_service.utranslate(msgid=event_type,
                                                   default=event_type,
                                                   domain="monet.calendar.extensions",
                                                   context=self)
            used_event_types.append((event_type, label))
        used_event_types.sort(key=lambda event: event[1].lower())
        return first_element + used_event_types


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
