'use strict'

// DOM Elements
const timeDisplay = document.querySelector('.game-time-left-p');
const gameSentence = document.querySelector('.game-sentence-p');
const gameInput = document.querySelector('.game-input');
const nextSentence = document.querySelector('.game-next-sentence-p');

const START_GAME_TRIGGER = 'go';
const GAME_DURATION = 30;

let currentPlayer = new Object();
let siteHighScore;

let playing; // boolean checking game state
let currentScore;
let initTimer;
let timeLeft;
let sentences = []; // sentence buffer
let currentSentence;

let counter; // setInterval object for pre-game countdown. Do I need this?
let gameTime; // setInterval object for game time left. Do I need this?

// Initial setup
const setupGame = () => {
    playing = false;
    getCurrentPlayer();
    getSiteHighScore();
    timeDisplay.innerHTML = 'Welcome!';
    gameSentence.innerHTML = 'Type "go" to start game.';
};

window.addEventListener('load', setupGame);

gameInput.addEventListener('input', () => {
    if(gameInput.value === START_GAME_TRIGGER && playing === false) {
        setTimeout(initGame, 300);
    } else if (playing) {
        if (gameInput.value.replace(/[^a-zA-Z-' ]/g, "").toLowerCase().trimStart() === currentSentence.rawSentence.replace(/[^a-zA-Z-' ]/g, "").toLowerCase()) {
            currentScore += currentSentence.sentenceArr.length;
            updateSentences();
            gameInput.value = '';
        }   
    }
});

const getSiteHighScore = () => {
    $.ajax({url: "/get_high_score", dataType: 'json', success: (result) => {
        siteHighScore = result.high_score;
    }});
};

const getCurrentPlayer = () => {
    $.ajax({url: "/get_name_and_score", dataType: 'json', success: (result) => {
        currentPlayer.username = result.username;
        currentPlayer.userHighScore = result.high_score;
    }});
};

const updateUserScore = (score) => {
    // get secret high score key from app.config
    $.ajax({url: "/get_high_score_key", dataType: 'json', success: (result) => {
        // obfuscate?
        let secret_cypher = result.high_score_key * score;
        let updateUserScoreURL = `/update_user_score/${secret_cypher}/${score}`;

        $.ajax({url: updateUserScoreURL, dataType: 'text', success: () => {
            return; // do I have to do something here?
        }});
    }});
    return;  // or here?
}

const initGame = () => {
    console.log(currentPlayer);
    initTimer = 4; // shows countdown from 3 on screen
    gameInput.value = '';
    gameSentence.innerHTML = 'Get ready!';
    nextSentence.innerHTML = '&nbsp;';
    populateSentencesArr();
    currentScore = 0;
    timeLeft = GAME_DURATION;
    counter = setInterval(initCountDown, 1000);
}

const initCountDown = () => {    
    if (initTimer > 1) {
        initTimer --;
        timeDisplay.innerHTML = `Game starting in: ${initTimer}`;
        if (initTimer === 1) {
            gameSentence.innerHTML = '&nbsp;';
        }
    } else {
        clearInterval(counter);
        startGame();        
    }
}

const startGame = () => {
    playing = true;
    gameInput.value = '';
    timeDisplay.innerHTML = `Time left: ${timeLeft} seconds`;
    updateSentences();
    gameTime = setInterval(countDown, 1000);
}

const updateSentences = () => {
    /* Grabs a sentence from sentence buffer,
       assigns it to currentSentence, 
       updates DOM: displays current and next sentence,
       then refills sentence buffer array */

    currentSentence = sentences.shift();
    gameSentence.innerHTML = currentSentence.rawSentence;
    nextSentence.innerHTML = sentences[0].rawSentence;
    sentences.push(getSentence());
}

const countDown = () => {
    if (timeLeft > 1) {
        timeLeft --;
        timeDisplay.innerHTML = `Time left: ${timeLeft} seconds`;
    } else {
        endGame();
        clearInterval(gameTime);
    }
}

const endGame = () => {
    playing = false;
    currentScore += countFinalSentenceScore();
    currentPlayer.finalScore = currentScore * (60 / GAME_DURATION);
    processScore(currentPlayer.finalScore, currentPlayer.userHighScore);
    gameSentence.innerHTML = 'Type "go" to start a new game.';
    nextSentence.innerHTML = '&nbsp;';
    gameInput.value = '';
}

const processScore = (score, personalBest) => {
    let gameEndMessage;
    updateUserScore(score);
    if (score > siteHighScore) {
        siteHighScore = score;
        gameEndMessage = `New Site High Score: ${score} words per minute! Congratulations!`;
    } else if (score < personalBest) {
        gameEndMessage = `You typed at ${score} words per minute!`;
    } else if (score > personalBest) {
        if (currentPlayer.username === 'anonymous') {
            gameEndMessage = `You typed at ${score} words per minute!`;
        } else {
            gameEndMessage = `New personal High Score! ${score} words per minute!`;
        }
    } else if (score === siteHighScore) {
        gameEndMessage = `Tied for a site High Score at ${score} words per minute!`;
    } else {
        gameEndMessage = 'Something went wrong, probably.';
    }
    
    timeDisplay.innerHTML = gameEndMessage;
}

const countFinalSentenceScore = () => {
    let inputSentenceArr = gameInput.value.replace(/[^a-zA-Z-' ]/g, "").toLowerCase().trimStart().split(" ");
    let shortestArrLen;
    let score = 0;

    if (inputSentenceArr.length < currentSentence.sentenceArr) {
        shortestArrLen = inputSentenceArr.length;
    } else {
        shortestArrLen = currentSentence.sentenceArr.length;
    }

    for (let i = 0; i < shortestArrLen; i++) {
        if (inputSentenceArr[i] === currentSentence.sentenceArr[i]) {
            score ++;
        }
    }
    return score;
}

const populateSentencesArr = () => {
    for (let i = 0; i < 3; i++) {
        setTimeout(function() {
            let new_sentence = getSentence();
            sentences.push(new_sentence);
        }, 0);    
    };
};

const getSentence = () => {
    let newSentence = new Object();
    $.ajax({url: "/get_sent", success: (result) => {
        newSentence.rawSentence = result;
        newSentence.sentenceArr = result.replace(/[^a-zA-Z-' ]/g, "").toLowerCase().split(" ");
    }});
    return newSentence;
};