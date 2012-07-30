$(function(){
    /* Masonry
       -------------------------------------------------------------- */

    var grid = $('section.grid');
    grid.masonry({ 
        singleMode: true,
        itemSelector: 'article',
    });

    grid.infinitescroll({
        loading: {
            finished: undefined,
        finishedMsg: "No more pages to load.",
        img: "/static/images/ajax-loader.gif",
        msg: null,
        msgText: "Loading...",
        selector: null,
        speed: 'fast',
        start: undefined
        },

        navSelector  : '#pagination',  // selector for the paged navigation 
        nextSelector : '#pagination a.next',  // selector for the NEXT link (to page 2)
        itemSelector : 'article',     // selector for all items you'll retrieve
        state: {currPage: 0},
        pathParse: function() {
            return ['/photos/all/','']
        },
        debug: true,
        errorCallback: function() { 
            // fade out the error message after 2 seconds
            $('#infscr-loading').animate({opacity: 0.8},2000).fadeOut('normal');   
        }

    },
        // call masonry as a callback
        function( newElements ) { 
            var $newElems = $( newElements ).css({ opacity: 0 });
            // ensure that images load before adding to masonry layout
            $newElems.imagesLoaded(function(){
                // show elems now they're ready
                $newElems.animate({ opacity: 1 });
                grid.masonry( 'appended', $newElems, true ); 
            });
        }
    );

    /* Article hover
       -------------------------------------------------------------- */

    $('article').live('mouseover', function(){
        $(this).find('.overlay').stop().fadeTo('fast', 100); 
    });

    $('article').live('mouseout', function(){
        $(this).find('.overlay').stop().fadeTo('fast', 0);
    });


    /* Expand click zone
       -------------------------------------------------------------- */

    $('article').live('click', function(){

        var href = $(this).find('h3 a').attr('href');

        window.location = href;

    });
});
