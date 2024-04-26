const pop = document.getElementsByClassName('detailspopup');
const btn = document.getElementById('details');
console.log(btn)
btn.addEventListener('click',function(event){
    event.preventDefault();
    console.log("clicked")
    opendetailspop();
});
console.log(pop)
function opendetailspop(){
    console.log("clicked")
    pop.style.display ='block';
}