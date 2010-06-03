from plone.app.portlets.portlets.calendar import Assignment,Renderer,AddForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Assignment(Assignment):
    """"""

class Renderer(Renderer):
    """"""
    _template = ViewPageTemplateFile('monetcalendar.pt')

class AddForm(AddForm):
    """"""
