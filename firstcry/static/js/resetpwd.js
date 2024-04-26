//  For Resetting password-------------------


var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
$(document).ready(function(){
    $("#reset").click(function(){
        // Perform actions when the button with ID 'reset' is clicked
        console.log("Button clicked"); // Example: Log a message to the console
        // Add your code here to handle the click event
        var newPassword = $('#npwd').val();
        var repeatPassword = $('#rnpwd').val();
        
        if (newPassword === '' ||  repeatPassword === ''){
            $('#msg').text("Should not be empty");
        }
        else if (newPassword.length < 6 || repeatPassword.length < 6) {
            $('#msg').text("Passwords must contain at least 6 characters");
        } else if (newPassword != repeatPassword) {
            $('#msg').text("Passwords do not match");
        }  else {
            
                $.ajax({
                    type: 'POST',
                    url: "forgotpwd",
                    data: {'pwd':repeatPassword},
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    success: function(response) {
                        console.log(response)
                        Swal.fire("congratulations!","Your Password Changed success Please Login","success").then((value) => {
                            window.location.href ="logout/"
                    });
                    }

                });


        }
    });
});