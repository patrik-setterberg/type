const toggleButton = document.querySelector('.instructions-toggle');
const instructions = document.querySelector('.sentence-instructions');

// Button labels for expanding and collapsing: Font Awesome icons
const EXP_LABEL = '<i class="fas fa-plus"></i>';
const COLL_LABEL = '<i class="fas fa-minus"></i>';

window.onload = () => {
    instructions.style.display = 'none';

    toggleButton.onclick = () => {
        toggle(toggleButton, instructions);
    };
}

const toggle = (btn, elem) => {
    if (elem.style.display === 'none') {
        elem.style.display = 'block';
        btn.innerHTML = COLL_LABEL;
        btn.classList.add('color-splash');
    } else {
        elem.style.display = 'none';
        btn.innerHTML = EXP_LABEL;
        btn.classList.remove('color-splash');
    }
}