from monet.calendar.extensions.interfaces import IMonetCalendarSection, IMonetCalendarSearchRoot
from Acquisition import aq_chain, aq_inner
from Products.CMFCore.utils import getToolByName

class UsefulForSearchEvents(object):
        
    def getSubSiteParentFolder(self):
        """Return the first parent folder found that implements the interface IMonetCalendarSearchRoot"""
        for parent in aq_chain(aq_inner(self.context)):
            if IMonetCalendarSearchRoot.providedBy(parent):
                return parent
        return None
        
    def getCalendarSection(self,subsite):
        """Return the first folder found that implements the interface IMonetCalendarSection"""
        pcatalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        query['object_provides'] = IMonetCalendarSection.__identifier__
        query['path'] = '/'.join(subsite.getPhysicalPath())
        query['sort_on'] = 'getObjPositionInParent'
        brains = pcatalog.searchResults(**query)
        if brains:
            return brains[0]
        return None
        
    def getCalendarSectionParentNoSubSite(self):
        """Return the first folder found in the site (no sub-site) that implements the interface IMonetCalendarSection"""
        portal=getToolByName(self.context, 'portal_url').getPortalObject()
        pcatalog = getToolByName(self, 'portal_catalog')
        query = {}
        query['object_provides'] = IMonetCalendarSection.__identifier__
        query['path'] = {'query':'/'.join(portal.getPhysicalPath()),'depth':1}
        query['sort_on'] = 'getObjPositionInParent'
        brains = pcatalog.searchResults(**query)
        if brains:
            return brains[0]
        return None
    
    def getCalendarSectionPath(self):
        subsite = self.getSubSiteParentFolder()
        if subsite:
            calendarsection = self.getCalendarSection(subsite)
        else:
            calendarsection = self.getCalendarSectionParentNoSubSite()
        if calendarsection:
            return calendarsection.getObject().absolute_url()
        else:
            return None