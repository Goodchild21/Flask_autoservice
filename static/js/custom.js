/* 1. logodata */
jQuery(document).ready(function($){
    if ( $.isFunction($.fn.owlCarousel) ) {
    $('.quotation').owlCarousel({
            loop:true,
            dot:true,
            nav:false,
            autoplay:true,
            items:1,
            autoplayTimeout:3000,
            })

/* 2. clients-slider */
    $('.clients-slider').owlCarousel({
            loop:true,
            dot:false,
            nav:false,
            // autoplay:true,
            // autoplayTimeout:3000,
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:2
                },
                993:{
                    items:4
                },
                1200:{
                    items:5
                },
              }
            })
        }
        jQuery('.mobile-nav .menu-item-has-children').on('click', function($) {

          jQuery(this).toggleClass('active');

        });

        jQuery('#nav-icon4').click(function($){

            jQuery('#mobile-nav').toggleClass('open');

        });

        jQuery('.res-cross').click(function($){

           jQuery('#mobile-nav').removeClass('open');

        });


        jQuery('.bar-menu').click(function($){

            jQuery('#mobile-nav').toggleClass('open');
            jQuery('#mobile-nav').toggleClass('hmburger-menu');
            jQuery('#mobile-nav').show();

        });

        jQuery('.res-cross').click(function($){

           jQuery('#mobile-nav').removeClass('open');

        });
  }) ;

// 6. loaded
$(window).on('load', function () {
    $("body").addClass("page-loaded");
    ("loaded")
});


