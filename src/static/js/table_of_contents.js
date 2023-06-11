const hamburger = document.getElementById('hamburger');
const toc = document.getElementById('toc');
let shown = false;

hamburger.addEventListener('click', () => {
    if (shown) {
        fadeout(toc);
    } else {
        fadein(toc);
    }
    shown = !shown;
});

toc.addEventListener('click', () => {
    fadeout(toc);
    shown = false;
});

document.addEventListener('click', (event) => {
    const target = event.target;
    if (target.id !== hamburger.id && target.id !== toc.id) {
        fadeout(toc);
        shown = false;
    }
})

function fadeout(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op <= 0.1){
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ')';
        op -= op * 0.1;
    }, 5);
}

function fadein(element) {
    var op = 0.1;  // initial opacity
    element.style.opacity = op;
    element.style.display = 'block';
    var timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ')';
        op += op * 0.1;
    }, 5);
}
