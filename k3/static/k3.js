vakken = document.querySelectorAll('.vakrij')
reservatiefrm = document.getElementById("reservatiefrm")
add_reserveerlistener()
add_annuleerlistener()
function add_reserveerlistener(){
    vakken.forEach(element => {
        element.addEventListener('click', reserveer_stoel)
    });
}
function remove_reserveerlistener(){
    vakken.forEach(element => {
        element.removeEventListener('click', reserveer_stoel)
    })
}
function add_annuleerlistener(){
    btnCancel = document.getElementById("btnCancel")
    if (btnCancel != null)
        btnCancel.addEventListener('click', annuleerReservatie)
}

function annuleerReservatie(event){

    vak = parseInt(element.dataset.vak)
    rij = parseInt(element.dataset.rij)
    stoel = parseInt(element.dataset.stoel)
    clearReservatieFrm(vak, rij, stoel)
}
function reserveer_stoel(event){
    element = event.srcElement
    if (element.classList.contains('vakrij-stoel') && ! element.hasAttribute('disabled')){
        vak = parseInt(element.dataset.vak)
        rij = parseInt(element.dataset.rij)
        stoel = parseInt(element.dataset.stoel)
        element.setAttribute('disabled', '')
        vulReservatieFrm(vak, rij, stoel);
        remove_reserveerlistener()
    }
}

function vulReservatieFrm(vak, rij, stoel) {
    reservatiefrm.classList.remove('hidden');
    reservatiefrm.focus();
    tekstveld = document.getElementById("stoel");
    tekstveld.innerText = "vak " + (vak) + ", rij " + (rij + 1) + ", stoel " + (stoel + 1);
    document.getElementById("vaknr").value = vak;
    document.getElementById("rijnr").value = rij;
    document.getElementById("stoelnr").value = stoel;
}

function clearReservatieFrm(vak, rij, stoel) {
    reservatiefrm.classList.add('hidden');
    gereserveerde_stoel = document.querySelector(`[data-vak="${vak}"][data-rij="${rij}"][data-stoel="${stoel}"]`)
    gereserveerde_stoel.removeAttribute('disabled')
    add_reserveerlistener()
}
