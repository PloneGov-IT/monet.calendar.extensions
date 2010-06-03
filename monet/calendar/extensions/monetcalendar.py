from plone.app.portlets.portlets.calendar import Assignment,Renderer,AddForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Assignment(Assignment):
    """"""

class Renderer(Renderer):
    """"""
    _template = ViewPageTemplateFile('monetcalendar.pt')
    
    def getDateString(self,daynumber):
        return '%s-%s-%s' % (self.year, self.month, daynumber)
        
class AddForm(AddForm):
    """"""
