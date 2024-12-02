const confirm_block = document.getElementById("confirm_block");
const del_btn = document.getElementById("delete_project_btn");
const close_confirm_btn = document.getElementById("close_confirm_btn");
var main = document.getElementById("main");


main.addEventListener('click', () => {
    main.style.opacity = "1.0";
    confirm_block.style.display = "none";
}, true);

del_btn.addEventListener('click', () => {
    main.style.opacity = "0.3";
    confirm_block.style.display = "flex";
});

close_confirm_btn.addEventListener("click", () => {
    main.style.opacity = "1.0";
    confirm_block.style.display = "none";
});