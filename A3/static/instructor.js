// static/instructor.js
$(document).ready(function(){
    // Update remark request status using AJAX
    $(".update-remark").click(function(){
        var remarkId = $(this).data("id");
        var newStatus = $(this).data("status");
        var statusCell = $("#status-" + remarkId);
        $.post("/instructor/update_remark", {remark_id: remarkId, new_status: newStatus}, function(data){
            alert(data.message);
            statusCell.text(newStatus);
        }).fail(function(xhr){
            alert("Error: " + xhr.responseJSON.error);
        });
    });

    // Mark feedback as reviewed (for demo purposes, simply visually mark the row)
    $(".mark-reviewed").click(function(){
        $(this).closest("tr").css("background-color", "#d3d3d3");
        alert("Feedback marked as reviewed.");
    });
});
