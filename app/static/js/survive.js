window.addEventListener('load', init);

// Globals

// Available levels
const levels = {
    easy: 5,
    medium: 3,
    hard: 2
};

// To change level
const currentLevel = levels.medium;

let time = currentLevel;
let score = 0;
let isPlaying;
let word;

// DOM Elements
const wordInput = document.querySelector('#word-input');
const currentWord = document.querySelector('#current-word');
const scoreDisplay = document.querySelector('#score');
const timeDisplay = document.querySelector('#time');
const message = document.querySelector('#message');
const seconds = document.querySelector('#seconds');

const words = [
    'word',
    'cat',
    'dog',
    'joke',
    'bloke',
    'snus',
    'dope',
    'javascript',
    'develop',
    'undermine'
];

// Initialize Game
function init(){
    // show number of seconds in UI
    seconds.innerHTML = currentLevel;
    //load word from array
    showWord(words);
    // Start matching on word input
    wordInput.addEventListener('input', startMatch);
    // Check input for correct letters
    wordInput.addEventListener('keyup', colorLetters)
    // Call countdown every second
    setInterval(countdown, 1000);
    // Check game status
    setInterval(checkStatus, 50);
}

// Start match
function startMatch(){
    if(matchWords()){
        isPlaying = true;
        time = currentLevel + 1;
        showWord(words);
        wordInput.value = '';
        score++;
    }
    // if score is -1, display 0 instead
    if (score === -1){
        scoreDisplay.innerHTML = 0;
    } else {
        scoreDisplay.innerHTML = score;
    }
}

// Match currentWord to wordInput
function matchWords(){
    if(wordInput.value === word){
        message.innerHTML = 'Correct!';
        return true;
    } else {
        message.innerHTML = '';
        return false;
    }
}

// Pick & show random word
function showWord(words){

    currentWord.innerHTML = '';
    // Generate random array index
    const randIndex = Math.floor(Math.random() * words.length);
    word = words[randIndex];

    for (let i = 0; i < word.length; i++){
        currentWord.innerHTML += '<span id="letter_' + i + '">' + word[i] + '</span>';
    }


    // Output random word
    // currentWord.innerHTML = words[randIndex];
}

// Color correctly entered letters
function colorLetters(){
    let text = wordInput.value;
    for (let i = 0; i < word.length; i++){
        let letter = document.querySelector("#letter_" + i);
        if (text[i] === word[i]){
            letter.style.color = "green";
        } else if (text[i] == null){
            letter.style.color = "white";
        } else {
            letter.style.color = "crimson";
        }
    }
}

// Countdown timer
function countdown(){
    // Make sure time is not run out
    if(time > 0){
        // Decrement time
        time--;
    } else if (time === 0){
        // Game is over
        isPlaying = false;
    }

    // Show time
    timeDisplay.innerHTML = time;
}

// Check game status
function checkStatus(){

    if(!isPlaying && time === 0){
        message.innerHTML = 'Game Over!!!';
        score = -1;
    }
}
