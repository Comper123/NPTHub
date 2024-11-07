const but = document.getElementById("but");
const close_btn = document.getElementById("close_btn");
const main = document.querySelector(".main");
const navigation = document.querySelector(".navigation");


but.addEventListener('click', () => {
  navigation.classList.add("active_navigation");
  main.classList.add("active_main");
  main.style.height = "100vh";
  main.style.overflow = 'hidden';
});

close_btn.addEventListener('click', () => {
    navigation.classList.remove("active_navigation");
    main.classList.remove("active_main");
    main.style.overflow = 'scroll';
    main.style.height = "";
});