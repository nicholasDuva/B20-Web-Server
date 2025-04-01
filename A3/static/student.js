// static/student.js
$(document).ready(function(){
    // Toggle the remark request input box
    $(".remark-btn").click(function(){
        $(this).siblings(".remark-box").toggle();
    });
    
    // Submit remark request using AJAX
    $(".submit-remark").click(function(){
        var assignment = $(this).data("assignment");
        var reason = $(this).siblings(".remark-reason").val();
        var button = $(this);
        $.post("/remark_requests", {assignment_name: assignment, reason: reason}, function(data){
            alert(data.message);
            // Optionally hide the input box after submission
            button.parent().hide();
        }).fail(function(xhr){
            alert("Error: " + xhr.responseJSON.error);
        });
    });
});
