var btn12 = document.getElementById('pdfBtn');
var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
$(document).ready(function(){
    $(btn12).click(function(){
        console.log("ok")
        var name = $('#order').val();
        var times = $('#period').val();
        console.log(name)
        console.log(times)
        $.ajax({
            url:  'generate_pdf/',
            type: 'POST',
            data: {
                'details': name,
                'period': times
            },
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(data) {
              
         
               // $('#msg').text('Operation successful');
            
                console.log("success")
             
            }
        })
    });

});