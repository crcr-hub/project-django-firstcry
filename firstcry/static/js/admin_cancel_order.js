



$(document).ready(function() {
    $('#cancel-Btn').click(function() {
      
        var csrfTokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
        var csrfToken = csrfTokenElement ? csrfTokenElement.value : null;
        var order = $('#ordID').val();
        var reason = $('#reason').val();
        console.log(order)

        if (reason === ''){
            $('#msg').text("You must provide the Reason")
            
        }
        else{
            $.ajax({
                type: 'POST',
                url: '/admin_cancelOrder',
                data: {'id':order,
                    'reason':reason
                    },
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(response) {
                    console.log(response)
                    Swal.fire({
                        position: "top-end",
                        icon: "success",
                        title: "Cancelled The order",
                        showConfirmButton: false,
                        timer: 1500
                      });
                      setTimeout(function() {
                        window.location.href = '/view_order/';
                    }, 1500);

                }
            
            
            
            });
        }
        

});
});