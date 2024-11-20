const profile_btn = document.getElementById("prof");
const menu = document.querySelector(".profile_info");
var is_shown = false;

profile_btn.addEventListener('click', function() {
    if (is_shown){
        menu.classList.remove("profile_info_show");
    } else {
        menu.classList.add("profile_info_show");
    }
    is_shown = !is_shown;
});
