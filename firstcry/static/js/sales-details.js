



$(document).ready(function() {
    $('#clickbtn').click(function() {
      
        var name = $('#order').val();
        var times = $('#period').val();
        console.log(name)
        console.log(times)
        $.ajax({
            url:  '/listSales',
            type: 'GET',
            data: {
                'details': name,
                'period': times
            },

            success: function(data) {
              
         
               // $('#msg').text('Operation successful');
            
                $("#table").html(data);
             
            }
        });
    });
});

