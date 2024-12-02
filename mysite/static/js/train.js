const but = document.getElementById("but");
const close_btn = document.getElementById("close_btn");
var main = document.getElementById("main");
const navigation = document.querySelector(".navigation");


// true в конце чтобы при клике на всю страницу все закрывалось игнорируя второй клик
main.addEventListener('click', () => {
    navigation.classList.remove("active_navigation");
    main.classList.remove("active_main");
    document.body.style.overflow_y = 'scroll';
    main.style.height = "";
}, true);

but.addEventListener('click', () => {
    navigation.classList.add("active_navigation");
    main.classList.add("active_main");
    navigation.style.position = "fixed";
    document.body.style.overflow_y = 'hidden';
});

close_btn.addEventListener('click', () => {
    navigation.classList.remove("active_navigation");
    main.classList.remove("active_main");
    document.body.style.overflow_y = 'scroll';
    main.style.height = "";
});
