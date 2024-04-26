const imagebox2 = document.getElementById('image-box');
const imageForm = document.getElementById('image-form');
const confirmbtn2 = document.getElementById('confirm-btn');
const input2 = document.getElementById('select-image');
const hiddenInput = document.getElementById('fd-input');
const submitbtn2 = document.getElementById('submit-btn');
const popup2 = document.getElementById('imgcrop');
const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

input2.addEventListener('change', () => {
    console.log("hello")
    
 
    popup2.style.display = 'block';
    console.log("running")
    const imgData = input2.files[0];
    const url = URL.createObjectURL(imgData);

    imagebox2.innerHTML = `<img src="${url}" id="image1" width="550px">`;
    var $image1 = $('#image1');
    console.log("thishs", $image1);

    $image1.cropper({
        aspectRatio: 300 / 364,
        crop: function (event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
        }
    });

    var cropper = $image1.data('cropper');
    confirmbtn2.addEventListener('click', () => {
        popup2.style.display = 'none';
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed');
            console.log(blob);
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrfToken);
            fd.append('image', blob, 'my-image.png');
           
            console.log("Thishs",$('#colorSelect').val())


            imagebox2.innerHTML = "";

             submitbtn2.addEventListener('click',()=>{
                fd.append('categ',$('#mySelect').val());
                fd.append('pname',$('#pname').val())
                fd.append('brand',$('#brandSelect').val());
                fd.append('desciption',$('#desciption').val());
                fd.append('neck',$('#neck').val());
                fd.append('sleeve',$('#sleeve').val());
                fd.append('length',$('#length').val());
                fd.append('waist',$('#waist').val());
                fd.append('price',$('#original-price').val());
                fd.append('deal',$('#discount-percentage').val());
                fd.append('offer',$('#offer-price').val());
                fd.append('0to3',$('#0to3').val());
                fd.append('3to6',$('#3to6').val());
                fd.append('6to9',$('#6to9').val());
                fd.append('9to12',$('#9to12').val());
                fd.append('12to18',$('#12to18').val());
                fd.append('18to24',$('#18to24').val());
                fd.append('2to4y',$('#2to4y').val());
                fd.append('4to6y',$('#4to6y').val());
                fd.append('6to8y',$('#6to8y').val());
                fd.append('total',$('#totalstock').val());
                fd.append('color',$('#colorSelect').val());
                console.log(fd);
                console.log($('#colorSelect').val())
                
                console.log("Thishs",$('#colorSelect').val())
                $.ajax({
                type: 'POST',
                url: 'addproduct/' ,
                data: fd,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                processData: false,
                contentType: false,
                success: function (response) {
                    console.log('success', response);
                   
                    Swal.fire({
                        position: "top-end",
                        icon: "success",
                        title: "Product successfully Added",
                        showConfirmButton: false,
                        timer: 1500
                      });
                      setTimeout(function() {
                        window.location.href = '/adminproduct';
                    }, 1500);
                   
                },
                error: function (error) {
                    console.log('error', error);
                    alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                            Ups...something went wrong
                                        </div>`;
                }
            });
            
                
             })
 

   
        });
    });
});
