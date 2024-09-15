let modal = document.getElementById('id01');
let modal = document.getElementById('id02');

//Когда пользователь кликнет за пределами модального окна, закроем его
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
