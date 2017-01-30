$(document).ready(function() {
    $(".input-section").hide();
    $(".cancel-button").hide();
    $(".save-button").hide();
    $(".add-button").click(function() {
        $(this).hide();
        $(".cancel-button").show();
        $(".save-button").show();
        $(this).parent().parent().parent().find(".input-section").toggle();
    });

    $(".edit-button").click(function() {
        var title = $(this).data('title');
        var desc = $(this).data('desc');
        $(".modal-body #title").val( title );
        $(".modal-body #description").val( desc );
    });

    $(".cancel-button").click(function() {
        $(this).hide();
        $(".save-button").hide();
        $(".add-button").show();
        $(this).parent().parent().parent().find(".input-section").toggle();
    });


});
