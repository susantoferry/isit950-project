let accMenuToggle = document.querySelector('.dropdown-menu-acc');
let dropdownToggle = document.querySelector('.dropdown-acc')
$(dropdownToggle).click(function () {
    console.log("a")
    accMenuToggle.classList.toggle('show')
})