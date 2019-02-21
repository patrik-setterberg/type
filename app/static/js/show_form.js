const nounFormBtn = document.querySelector('.noun-link');
const adjFormBtn = document.querySelector('.adj-link');
const verbFormBtn = document.querySelector('.verb-link');
const advFormBtn = document.querySelector('.adv-link');
const propNounFormBtn = document.querySelector('.prop-noun-link');
const specialFormBtn = document.querySelector('.special-link');

const nounForm = document.querySelector('.noun-form');
const adjForm = document.querySelector('.adj-form');
const verbForm = document.querySelector('.verb-form');
const advForm = document.querySelector('.adv-form');
const propNounForm = document.querySelector('.prop-noun-form');
const specialForm = document.querySelector('.special-form');

const nouns = document.querySelector('.nouns');
const adjs = document.querySelector('.adjectives');
const verbs = document.querySelector('.verbs');
const advs = document.querySelector('.adverbs');
const propNouns = document.querySelector('.proper-nouns');
const specials = document.querySelector('.special-words');

const nounsBtn = document.querySelector('.nouns-button');
const adjsBtn = document.querySelector('.adjectives-button');
const verbsBtn = document.querySelector('.verbs-button');
const advsBtn = document.querySelector('.adverbs-button');
const propNounsBtn = document.querySelector('.proper-nouns-button');
const specialsBtn = document.querySelector('.specials-button');

const formArr = [nounForm, adjForm, verbForm, advForm, propNounForm, specialForm];
const wordsArr = [nouns, adjs, verbs, advs, propNouns, specials];

// Button labels for expanding and collapsing: Font Awesome icons
const EXP_LABEL = '<i class="fas fa-plus"></i>';
const COLL_LABEL = '<i class="fas fa-minus"></i>';

// Hide all forms and words (on page load)
const hideAll = (arr) => {
    arr.forEach((element) => {
        element.style.display = 'none';
    });
}

window.onload = () => {
    
    hideAll(formArr);
    hideAll(wordsArr);

    nounFormBtn.onclick = () => {
        toggle(nounFormBtn, nounForm);
    }

    adjFormBtn.onclick = () => {
        toggle(adjFormBtn, adjForm);
    }

    verbFormBtn.onclick = () => {
        toggle(verbFormBtn, verbForm);
    }

    advFormBtn.onclick = () => {
        toggle(advFormBtn, advForm);
    }

    propNounFormBtn.onclick = () => {
        toggle(propNounFormBtn, propNounForm);
    }

    specialFormBtn.onclick = () => {
        toggle(specialFormBtn, specialForm);
    }

    nounsBtn.onclick = () => {
        toggle(nounsBtn, nouns);
    }

    adjsBtn.onclick = () => {
        toggle(adjsBtn, adjs);
    }

    verbsBtn.onclick = () => {
        toggle(verbsBtn, verbs);
    }

    advsBtn.onclick = () => {
        toggle(advsBtn, advs);
    }

    propNounsBtn.onclick = () => {
        toggle(propNounsBtn, propNouns);
    }

    specialsBtn.onclick = () => {
        toggle(specialsBtn, specials);
    }
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