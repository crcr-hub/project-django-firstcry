const addAddressBtn = document.getElementById('addAddressBtn');
const popup = document.getElementById('popup');
const newaddrBtn = document.getElementById('newaddrs')
const popupaddaddrs = document.getElementById('popupaddaddrs')


newaddrBtn.addEventListener('click',() => {
    openAddAddrs();
});
function openAddAddrs(){
    closePopup();
    popupaddaddrs.style.display = 'block'
}

function closeAddAddrs(){
    popupaddaddrs.style.display = 'none'
}

addAddressBtn.addEventListener('click', () => {
    openPopup();
});

function openPopup() {
    popup.style.display = 'block';
}

function closePopup() {
    popup.style.display = 'none';
}

// Coupon popup
const viewcoupon = document.getElementById('viewcoupon');
const couponpopup = document.getElementById('couponpopup')
viewcoupon.addEventListener('click',() => {
    console.log("clickinf")
        couponpopup.style.display = 'block';
});

function closecouponPopup(){
    console.log("ok")
    couponpopup.style.display = 'none';
}



