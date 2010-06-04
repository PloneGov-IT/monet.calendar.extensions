from plone.app.portlets.portlets.calendar import Assignment,Renderer,AddForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from monet.calendar.extensions.browser.usefulforsearch import UsefulForSearchEvents
from plone.memoize.compress import xhtml_compress

class Assignment(Assignment):
    """"""

class Renderer(Renderer,UsefulForSearchEvents):
    """"""
    _template = ViewPageTemplateFile('monetcalendar.pt')
    
    def getDateString(self,daynumber):
        return '%s-%s-%s' % (self.year, self.month, daynumber)

    def render(self):
        return xhtml_compress(self._template())

  
class AddForm(AddForm):
    """"""
