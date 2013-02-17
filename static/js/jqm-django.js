$(document).ready( function () {
    /* mostly this is just sample code for how to trigger code for each page */
    $('div:jqmData(role=\'page\')').live('pagecreate',function(event){
        var page = $(this);
        page.find( '.field-wrapper' ).each( function() {
            var wrapper = $(this);
            var text = wrapper.find( '.field-help' );
            if (text.length) {
                var hidden = true;
                page.find( 'button.help-trigger' ).each( function () {
                   var trigger = $(this); 
                    trigger.click( function(event) {
                        text.toggle();
                        event.stopPropagation();
                        return false;
                    });
                });
                text.hide();
            }
        });
    });
});
