

var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
document.getElementById('changeBtn').addEventListener('click', function() {
    var password = document.getElementById('pwd').value;
    var repeatPassword = document.getElementById('rpwd').value;

    if(password === '' || repeatPassword === ''){
        document.getElementById('errorMessage').style.display = 'block';
        $('#msg').text('All Feilds should have a data')

    }
    else if (password === repeatPassword) {
        // Passwords match, proceed with Ajax
        var formData = new FormData(document.getElementById('changepwd'));
        console.log("clicked")
        $.ajax({
            type: 'POST',
            url: "changepassword/",
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    console.log("ok")
                    Swal.fire({
                        position: "top-end",
                        icon: "success",
                        title: "Password SuccessFully changed Please Login!!",
                        showConfirmButton: false,
                        timer: 1500
                      });
                      setTimeout(function() {
                        window.location.href = 'logout/';
                    }, 1500);
                    // Show success notification
                
                } else if (response.error) {
                    console.log(response.error)
                    document.getElementById('errorMessage').style.display = 'block';
                    $('#msg').text('Wrong Password')
    
                }
                // Handle success response
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.log(error)
            }
        });
    } 
  
    else {
        // Passwords do not match, show error message
        document.getElementById('errorMessage').style.display = 'block';
        $('#msg').text('Repeat password must be same')
    }
});

