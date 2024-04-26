
const addAddressBtn = document.getElementById('addAddressBtn');
const popup = document.getElementById('popup');

;
//const msg = document.getElementById('msg').val();

addAddressBtn.addEventListener('click', () => {
    console.log("clicked");
    openPopup();
});



function openPopup() {
    popup.style.display = 'block';
}

function closePopup() {
    console.log("clicked");
    popup.style.display = 'none';
    $('#msg').text('');

    
}



$(document).ready(function() {
    $('#submitButton').click(function() {
        var name = $('#name').val();
        var code = $('#hex').val();
        console.log(name)
        console.log(code)
        $.ajax({
            url:  '/add_color_js',
            type: 'GET',
            data: {
                'name': name,
                'code': code
            },
            success: function(data) {
              
                console.log(data)
                $('#msg').text('Operation successful');
            
                $(" #reload ").html(data);
             
            }
        });
    });
});

