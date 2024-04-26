const addAddressBtn = document.getElementById('addAddressBtn');
const popup = document.getElementById('popup');

addAddressBtn.addEventListener('click', () => {
    openPopup();
});

function openPopup() {
    popup.style.display = 'block';
}

function closePopup() {
    popup.style.display = 'none';
}


const placeorder = document.getElementByClassName('ordernow')
const orderpopup = document.getElementsByClassName('orderpopup')

placeorder.addEventListener('click',() =>{
    openOrderpopup();

});

function openOrderpopup(){
    orderpopup.style.display = 'block'
}

function closeOrderpopup(){
    orderpopup.style.display = 'none'
}