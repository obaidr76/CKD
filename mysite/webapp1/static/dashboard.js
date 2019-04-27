// JavaScript source code
/* LOGIN - MAIN.JS - dp 2017 */



var div1 = document.getElementById('personal_tab1'),
    div2 = document.getElementById('personal_tab2');
function switchVisible() {
    if (!div1) return;
    if (getComputedStyle(div1).display == 'block') {
        div1.style.display = 'none';
        div2.style.display = 'block';
    } else {
        div1.style.display = 'block';
        div2.style.display = 'none';
    }
}
document.getElementById('personal_button').addEventListener('click', switchVisible);





var div3 = document.getElementById('address_tab1'),
    div4 = document.getElementById('address_tab2');
function switchVisible2() {
    if (!div3) return;
    if (getComputedStyle(div3).display == 'block') {
        div3.style.display = 'none';
        div4.style.display = 'block';
    } else {
        div3.style.display = 'block';
        div4.style.display = 'none';
    }
}
document.getElementById('address_button').addEventListener('click', switchVisible2);
