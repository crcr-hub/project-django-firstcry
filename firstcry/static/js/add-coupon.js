
var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;




$(document).ready(function() {

    
    $('#couponBtn1').click(function() {




        function redirectToConfirmOrder(url, data) {
            // Create a form element
            var form = document.createElement('form');
            
            // Set the form's action attribute to the URL
            form.action = url;
            
            // Set the form's method attribute to POST
            form.method = 'POST';
            
            // Retrieve CSRF token from the existing input field in the HTML document
            var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            var csrfToken = csrfTokenInput ? csrfTokenInput.value : null;
            
            // If a CSRF token was found, add it to the form as a hidden input field
            if (csrfToken) {
                var csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);
            }
            
            // Add data to the form as hidden input fields
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    input.value = data[key];
                    form.appendChild(input);
                }
            }
            
            // Append the form to the body
            document.body.appendChild(form);
            
            // Submit the form
            form.submit();
        }




        var checkingid = $('#checkingid').val();
        console.log("thishs id",checkingid)
      
        var coupon = $('#couponvalue').val();
        var total = $('#total').val();
        var ordid = $('#ordid').val();
        console.log("orderid",ordid)
 
     

        $.ajax({
            url:  'coupon_check',
            type: 'GET',
            data: {'coupon':coupon,
                    'total':total
                },
    
            success: function(data) {
              
                console.log("thishs success msg",data.Success)
                if (data.error){
                    $("#errormsg").text(data.error);
           
                }
                else{
                    var cop = data.Success
                    console.log(cop)
                    
                    if (checkingid == '1') {
                        // Retrieve the CSRF token from the page
                        var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
                        var csrfToken = csrfTokenInput ? csrfTokenInput.value : null;
                        console.log(csrfTokenInput)
                        
                        redirectToConfirmOrder("confirm_order", {
                            'cid': cop,
                            'id' : ordid
                        });

                     
             
                    }
                    else{
                        window.location.href = "confirm_order?val="+ cop;
                    }
                }
               
   
             
            },
            error: function(xhr, status, error) {
               // console.log(xhr.responseText);
                // Handle error response
                }
        });





        
    });




    // Applying coupon from the coupon popup window
    $(document).on('click', '.couponBtn2', function(event){

        function redirectToConfirmOrder(url, data) {
            // Create a form element
            var form = document.createElement('form');
            
            // Set the form's action attribute to the URL
            form.action = url;
            
            // Set the form's method attribute to POST
            form.method = 'POST';
            
            // Retrieve CSRF token from the existing input field in the HTML document
            var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            var csrfToken = csrfTokenInput ? csrfTokenInput.value : null;
            
            // If a CSRF token was found, add it to the form as a hidden input field
            if (csrfToken) {
                var csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);
            }
            
            // Add data to the form as hidden input fields
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    input.value = data[key];
                    form.appendChild(input);
                }
            }
            
            // Append the form to the body
            document.body.appendChild(form);
            
            // Submit the form
            form.submit();
        }








        var id = $('#checkingid').val();
        console.log("thishs id",id)
        var ordid = $('#ordid').val();
        console.log("orderid",ordid)
  
        console.log("clicked")
        var total = $('#total').val();
        var button = $(this);
        var couponId = button.data('id');
        const label = $('label[data-id="' + couponId + '"]');
        console.log("thishis",label)
        //const label = document.querySelector(`label[data-id="${couponId}"]`);
       
        

      
        $.ajax({
            url:  'coupon_check',
            type: 'GET',
            data: {'couponId':couponId,
                    'total':total
                },
    
            success: function(data) {
              
                console.log("thishs",data.Success)
                if (data.error){
                    if (label.length > 0) {
            
                        label.text(data.error);
                    }else{
                        console.log("no")
                    }
           
                }
                else{
                    var cop = data.Success
                    console.log("id",id)
                  
                    if (id == '1'){
                        redirectToConfirmOrder("confirm_order", {
                            'cid': cop,
                            'id' : ordid
                        });


                       }
                    else{
                        window.location.href = "confirm_order?val="+ cop;
                    }
                }
               
   
             
            },
            error: function(xhr, status, error) {
               // console.log(xhr.responseText);
                // Handle error response
                }
        });

    
    });

});

