window.onload = function(){
	var slides = document.querySelectorAll('#slider .slider_item');
    var currentSlide = 0;
    slides[0].classList.add('show');
    var slideInterval = setInterval(nextSlide, 2000);
    
};


function nextSlide() {
    slides[currentSlide].classList.remove('show');
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add('show');
}