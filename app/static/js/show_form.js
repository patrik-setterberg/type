const nounForm = document.querySelector('.noun-form');
const adjForm = document.querySelector('.adj-form');
const verbForm = document.querySelector('.verb-form');
const advForm = document.querySelector('.adv-form');
const propNounForm = document.querySelector('.prop-noun-form');
const specialForm = document.querySelector('.special-form');

const div_arr = [nounForm, adjForm, verbForm, advForm, propNounForm, specialForm];


function hideAll(arr) {
    for (let i = 0; i < arr.length; i++){
        arr[i].style.display = 'none';
    }
}

window.onload = function() {
    
    hideAll(div_arr);

    document.querySelector('.noun-link').onclick = function() {
        hideAll(div_arr);
        nounForm.style.display = 'block';
        return false;
    }
    document.querySelector('.adj-link').onclick = function() {
        hideAll(div_arr);
        adjForm.style.display = 'block';
        return false;
    }
    document.querySelector('.verb-link').onclick = function() {
        hideAll(div_arr);
        verbForm.style.display = 'block';
        return false;
    }
    document.querySelector('.adv-link').onclick = function() {
        hideAll(div_arr);
        advForm.style.display = 'block';
        return false;
    }
    document.querySelector('.prop-noun-link').onclick = function() {
        hideAll(div_arr);
        propNounForm.style.display = 'block';
        return false;
    }
    document.querySelector('.special-link').onclick = function() {
        hideAll(div_arr);
        specialForm.style.display = 'block';
        return false;
    }
}