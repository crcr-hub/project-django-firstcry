

var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
$(document).ready(function(){


    $(".paywithcod").click(function(){
        console.log("clicked")
        var total = $('#total').val();
        var couponid = $('#cpnid').val();
        console.log(total)
        console.log("thishs",couponid)
        $.ajax({
            url:  "/order",
            type: 'POST',
            data: {
                'paymentmode':'CashOnDelivery',
                'cid':couponid,
                'total':total,
            },
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(data) {
              
         
                // $('#msg').text('Operation successful');
             
                 console.log("success")
                 Swal.fire("congratulations!",data.status,"success").then((value) => {
                    window.location.href ="/orderhistory"
            });
              
             }

        });


    });






    $(".paywithRazor").click(function(e){ // click event to buttons with class 
        e.preventDefault();
        console.log("clicked")
        var name = $("[name='name']").val();
        var hname =$("[name='house']").val();
        var street =$("[name='street']").val();
        var city =$("[name='city']").val();
        var state =$("[name='state']").val();
        var pin =$("[name='pin']").val();
        var mob =$("[name='mob']").val();
        var country = "India"
        var total_amount = $('#total_amount').val()
        var cid = $('#cid').val()
        console.log(name)


        $.ajax({
            method: "GET",
            url:"/paytoproceed",
            success: function(response){
                console.log(response.total)
                const total1 = response.total
                var options = {
                    "key": "rzp_test_py8LwfbmVzKjQ4", // Enter the Key ID generated from the Dashboard
                    "amount": total_amount*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "FirstCry", //your business name
                    "description": "Thank You for buying with us",
                    //"image": "https://example.com/your_logo",
                    //"order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (res){
                        $.ajax({
                            methos: "GET",
                            url: "/order",
                            data: {"paymentmode":"Paid by Razorpay",
                                    "payment_id":res.razorpay_payment_id,
                                    "total":total_amount,
                                    'cid':cid,
                                    },
                            datatype: "datatype",
                            success: function(responsea){
                                Swal.fire("congratulations!",responsea.status,"success").then((value) => { 
                                    console.log("Test: Swal alert closed.");
                                        window.location.href ="/orderhistory"
                                });

                            }
                            
                        });
                       
                    },
                    "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                        "name": name, //your customer's name
                        "email": "gaurav.kumar@example.com", 
                        //"contact": mob  //Provide the customer's phone number for better conversion rates 
                    },
                    
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                // var rzp1 = new Razorpay(options);
                // rzp1.open();
                var rzp1 = new Razorpay(options);
                    rzp1.on('payment.failed', function (res){
                        console.log(total1)
                        rzp1.close();
                        
                         
                            $.ajax({
                               
                                methos: "GET",
                                url: "/order",
                                data: {"paymentmode":"Pending",
                                        "payment_id":res.razorpay_payment_id,
                                        "total":total_amount,
                                        'cid':cid,
                                        },
                                datatype: "datatype",
                                success: function(respon){
                               
                                  
                                    Swal.fire({
                                        position: "top-end",
                                        icon: "error",
                                        title: "Your Order has been saved",
                                        showConfirmButton: false,
                                        timer: 2000, // Duration in milliseconds (1.5 seconds)
                                        timerProgressBar: true // Show a progress bar
                                    }).then(() => {
                                        // Redirect to another page once the alert is closed
                                        console.log("okkkk")
                                        window.location.href = "/orderhistory";
                                    })
                                    console.log("failed2")
    
                                }
                                
                            });
                           
                         
  
                    });
                   
                        rzp1.open();
                        e.preventDefault();
                    

            } , 
            error: function(xhr, status, error) {
                console.log("Request failed:");
            
            }
            
        });
    });       
});

