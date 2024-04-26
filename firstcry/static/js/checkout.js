

var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
$(document).ready(function(){






    $(".paywithRazorfromOrder").click(function(e){ // click event to buttons with class 
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
        var ordid = $('#ordid').val();


        $.ajax({
            method: "GET",
            url:"/paytoproceed",
            data:{

            },
            success: function(response){
                console.log(response.total)
                const total = response.total
                var options = {
                    "key": "rzp_test_py8LwfbmVzKjQ4", // Enter the Key ID generated from the Dashboard
                    "amount": total_amount*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "RaijoRaj", //your business name
                    "description": "Thank You for buying with us",
                    //"image": "https://example.com/your_logo",
                    //"order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (res){
                        $.ajax({
                            methos: "GET",
                            url: "/order_product_from_orderhistory",
                            data: {"paymentmode":"Paid by Razorpay",
                                    "payment_id":res.razorpay_payment_id,
                                    "total":total_amount,
                                    'cid':cid,
                                    'ord':ordid,
                                    },
                            datatype: "datatype",
                            success: function(responsea){
                                Swal.fire("congratulations!",responsea.status,"success").then((value) => {
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
                var rzp1 = new Razorpay(options);
                rzp1.open();
        

            }  
        });
    });       
});

