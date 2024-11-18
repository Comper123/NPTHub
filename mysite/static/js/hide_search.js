const btn = document.getElementById("show_search");
const form = document.querySelector(".search_form");
var is_shown = false;

btn.addEventListener('click', () => {
    if (is_shown){
        form.classList.remove("shown_form");
        btn.classList.remove("btn_show");
    } else {
        form.classList.add("shown_form");
        btn.classList.add("btn_show");
    }
    is_shown = !is_shown;
  });