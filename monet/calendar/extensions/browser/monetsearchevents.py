from Products.Five.browser import BrowserView

class MonetSearchEvents(BrowserView):
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
