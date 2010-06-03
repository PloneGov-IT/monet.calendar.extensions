from monet.calendar.extensions.interfaces import IMonetCalendarSection, IMonetCalendarSearchRoot
from Acquisition import aq_chain
from Products.CMFCore.utils import getToolByName

class UsefulForSearchEvents(object):
        
    def getSubSiteParentFolder(self):
        """Return the first parent folder found that implements the interface IMonetCalendarSearchRoot"""
        for parent in aq_chain(self):
            if IMonetCalendarSearchRoot.providedBy(parent):
                return parent
        return None
        
    def getCalendarSection(self,subsite):
        """Return the first folder found that implements the interface IMonetCalendarSection"""
        pcatalog = getToolByName(self, 'portal_catalog')
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
        portal=getToolByName(self, 'portal_url').getPortalObject()
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
        return calendarsection.getObject().absolute_url()