
const brandBtn = document.getElementById('addBrandBtn');
const brandpopup = document.getElementById('brandpopup');


//const msg = document.getElementById('msg').val();

brandBtn.addEventListener('click', () => {
    
    openbrandPopup();
});



function openbrandPopup() {
    brandpopup.style.display = 'block';
}

function closebrandPopup() {
    console.log("clicked");
    brandpopup.style.display = 'none';
    //$('#msg').text('');

    
}



$(document).ready(function() {
    
    $('#brandsubmitButton').click(function() {
        console.log("clicked");
        var formData = new FormData();
        var brandname = $('#brandname').val();
        var description = $('#branddescription').val();
        var specs = $('#brandspecs').val();
        var logo = $('#logo').val();
        formData.append('brandname',brandname);
    
        formData.append('logo', document.getElementById('logo').files[0]);
        console.log(formData)

        $.ajax({
            url:  '/add_brand_js',
            type: 'GET',
            data: {'brandname':brandname,
                    'description':description,
                'specs':specs,
                'logo':logo},
            success: function(data) {
              
                console.log(data)
               
                console.log(data)
             
            }
        });
    });
});

