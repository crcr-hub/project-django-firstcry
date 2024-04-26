const alertBox = document.getElementById('alert-box');
const imageBox = document.getElementById('image-box');
const imageForm = document.getElementById('image-form');
const confirmBtn = document.getElementById('confirm-btn');
const input = document.getElementById('testing');
const hiddenInput = document.getElementById('fd-input');
const submit = document.getElementById('submit-btn')

const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

input.addEventListener('change', () => {
    alertBox.innerHTML = '';
    console.log("running")
    confirmBtn.classList.remove('not-visible');
    const imgData = input.files[0];
    const url = URL.createObjectURL(imgData);

    imageBox.innerHTML = `<img src="${url}" id="image" width="700px">`;
    var $image = $('#image');
    console.log("thishs", $image);

    $image.cropper({
        aspectRatio: 438 / 531,
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
    confirmBtn.addEventListener('click', () => {
        confirmBtn.classList.add('not-visible');
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed');
            console.log(blob);
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrfToken);
            fd.append('file', blob, 'my-image.png');
            fd.append('name',$('#name').val());
            fd.append('sss',$('#test').val());
            console.log(fd);
            var concatenatedValue = 'file: ' + blob + ', filename: my-image.png';
            //textBox.value = concatenatedValu

            imageBox.innerHTML = "";

            submit.addEventListener('click',()=>{
                $.ajax({
                type: 'POST',
                url: "crop-image/",
                data: fd,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                processData: false,
                contentType: false,
                success: function (response) {
                    console.log('Thishs response', response);
                    alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                            Successfully saved and cropped the selected image
                                        </div>`;
                    confirmBtn.classList.add('not-visible');
                    imageBox.innerHTML = '';
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
