/**
 * Calendar viewlet controls
 */

;(function($){

	var plonesimplemessage = function(title, message, element) {
	    element.empty().append('<dt>'+title+'</dt>').append('<dd>'+message+'</dd>').slideDown('fast');
	};
	
	$(document).ready(function() {
	    
	    if (!$.datepicker) {
	        return;
	    };
	    
	    $("head").append('<style type="text/css">#ui-datepicker-div {z-index: 10}</style>');
	    
	    /**
	     * Context URL to be used for all AJAX call
	     */
	    var call_context = $("head base").attr('href');
	    if (call_context.charAt(call_context.length-1)!='/') call_context=call_context+'/';
	
	    /*
	     * Don't want to call the context when is in the portal factory. See the Ale's blog post:
	     * http://blog.redturtle.it/redturtle-blog/2010/03/11/careful-with-that-ajax-eugene
	     */
	    if (call_context.indexOf('/portal_factory')>-1) {
	        call_context=call_context.substring(0,call_context.indexOf('/portal_factory')+1);
	    };
	    
	    var lang = $("html").attr("lang") || 'en';
	    if (lang !== 'en') {
	        $("head").append('<script type="text/javascript" src="jquery.ui.datepicker-' + lang + '.js"></script>');
	    };
	    
	    /**
	     * Perform an AJAX call to validate the date fields
	     */
	    var paramsRemoteValidation = function() {
	        $.getJSON(call_context+ '/@@monetsearchevents_validation',
	                   {
	                       fromDay: $("#fromDay").val(), fromMonth: $("#fromMonth").val(), fromYear: $("#fromYear").val(),
	                       toDay: $("#toDay").val(), toMonth: $("#toMonth").val(), toYear: $("#toYear").val()
	                   },
	                   function(data, textStatus) {
	                        if (data.error) {
	                           $.plonesimplemessage(data.title, data.error, $("#dateErrors"));
	                           $("#searchEvents").addClass("searchDisabled");                                                
	                        } else {
	                            $("#dateErrors").slideUp('fast');
	                            $("#searchEvents").removeClass('searchDisabled');
	                        }
	                   }
	        );
	    };
	    
	    var messages = $('<dl id="dateErrors" class="portalMessage error" style="display:none"></dl>');
	    $("#searchBar").prepend(messages);
	    
	    // Controls over the calendars
	    var suffixes = ['from', 'to'];
	    $(".searchBarFrom,.searchBarTo").each(function(index, elem) {
	        // from searchBarXXX get XXX
	        var suffix = suffixes[index];
	        var dateField = $('<input type="hidden" value="" />');
	        $(elem).append(dateField);
	        dateField.datepicker({showOn: 'button', 
	                              buttonImage: call_context+'/popup_calendar.gif', 
	                              buttonImageOnly: true,
	                              showAnim: '',    
	                              dateFormat: 'yy-mm-dd',
	                              beforeShow: function(input, inst) {
	                                $(this).val($("#"+suffix+"Year").val()+"-"+$("#"+suffix+"Month").val()+'-'+parseInt($("#"+suffix+"Day").val()));
	                                return {}
	                              },
	                              onSelect: function(dateText, inst) {
	                                    var ds = dateText.split("-");
	                                    $("#"+suffix+"Year").val(ds[0]);
	                                    $("#"+suffix+"Month").val(ds[1]);
	                                    $("#"+suffix+"Day").val(ds[2]);
	                                    // Now the AJAX validation
	                                    paramsRemoteValidation();
	                              },
	                            }, $.datepicker.regional[lang]
	        );
	        
	        $("#searchEvents").click(function(e) {
	            if ($(this).hasClass("searchDisabled")) e.preventDefault();
	        });
	    });
	    
	    // Controls over combos
	    $(".searchBarFrom select,.searchBarTo select").change(function(e) {
	        // Now the AJAX validation
	        paramsRemoteValidation();
	    });
	    
	});
	
})(jQuery);
