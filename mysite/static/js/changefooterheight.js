const footer = document.querySelector("footer");
// Получаем реальную высоту body
var body_height = document.getElementById("main");
// Получаем реальную высоту footer
var footer_height = footer.offsetHeight;

// Вычисляем отступ для footer 
footer.style.margin_top = String(body_height - footer_height) + "px";
console.log(footer.style.margin_top)