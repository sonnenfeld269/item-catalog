$(document).ready(function() {
    /* Add item */
    $(".input-section").hide();
    $(".cancel-button").hide();
    $(".save-button").hide();
    $(".add-button").click(function() {
        $(this).hide();
        $(".cancel-button").show();
        $(".save-button").show();
        $(this).parent().parent().parent().find(".input-section").toggle();
    });
    $(".cancel-button").click(function() {
        $(this).hide();
        $(".save-button").hide();
        $(".add-button").show();
        $(this).parent().parent().parent().find(".input-section").toggle();
    });

    /* Add active class to category list */
    $('.nav').on('click', 'li', function(){
        $('.nav li').removeClass('active');
        $(this).addClass('active');
    });
});
