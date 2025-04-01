$(document).ready(function() {
    // Basic check for matching passwords on registration
    $("form").on("submit", function(e) {
        var password = $("#password").val();
        var confirmPassword = $("#confirm_password").val();
        if (confirmPassword && password !== confirmPassword) {
            alert("Passwords do not match!");
            e.preventDefault();
        }
    });
});
