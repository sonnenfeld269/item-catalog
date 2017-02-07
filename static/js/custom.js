$(document).ready(function() {
    /* Add item */
    $(".add-form").hide();
    $(".add-button").click(function() {
        $(this).hide();
        $(".add-form").toggle();
    });
    $(".cancel-button").click(function() {
        $(".add-button").show();
        $(".add-form").toggle();
    });
});
