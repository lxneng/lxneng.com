$(function(){
    $(window).scroll(function(){$(window).scrollTop()=="0"?$("#goTop").fadeOut("slow"):$("#goTop").fadeIn("slow")});
});
$('.nav li').hover(
    function() { $(this).children('.submenu').show() },
    function() { $(this).children('.submenu').hide() }
);
