

const imagebox1 = document.getElementById('image-box');
const imageForm = document.getElementById('image-form');
const confirmbtn1 = document.getElementById('confirm-btn');
const input1 = document.getElementById('select-image');
const hiddenInput = document.getElementById('fd-input');
const submitbtn1 = document.getElementById('submit-btn');
const popup1 = document.getElementById('popup');


const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

input1.addEventListener('change', () => {
    console.log("hello")
    id = $('#brand-id').val();
    console.log(id)
    popup1.style.display = 'block';
    console.log("running")
    const imgData = input1.files[0];
    const url = URL.createObjectURL(imgData);

    imagebox1.innerHTML = `<img src="${url}" id="image" width="400px">`;
    var $image = $('#image');
    console.log("thishs", $image);

    $image.cropper({
        aspectRatio: 130 / 98,
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

    var cropper = $image.data('cropper');
    confirmbtn1.addEventListener('click', () => {
        popup1.style.display = 'none';
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed');
            console.log(blob);
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrfToken);
            fd.append('logo', blob, 'my-image.png');
            fd.append('name',$('#name').val());
            fd.append('description',$('#description').val());
            fd.append('specs',$('#specs').val());
            console.log(fd);


            imagebox1.innerHTML = "";

            submitbtn1.addEventListener('click',()=>{
                $.ajax({
                type: 'POST',
                url: '/update_brand/' + id +'/' ,
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
                        title: "Brand successfully updated",
                        showConfirmButton: false,
                        timer: 1500
                      });
                      setTimeout(function() {
                        window.location.href = '/view_brand';
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
