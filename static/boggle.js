class BoggleGame{
    constructor(boardId, seconds = 60){
        // List of guessed words
        this.words = new Set();
        // establish current board
        this.board = $("#" + boardId);
        // starting score of zero
        this.score = 0;
        this.highScore = 0;
        // Game length and timer start
        this.seconds = seconds;
        this.showTimer();
        // establish a change in timer every second
        this.timer = setInterval(this.timeCount.bind(this), 1000);

        //when submit button(addword) is called on the board, call handlesubmit
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this))

        $(".replay").hide()
    }


 // Show messages
showMessage(message){
    $(".messages", this.board)
    .text(message);
}

// Show list of successfully submitted words
showWord(word){
    $(".words", this.board).append($("<li>", {text: word}));
}

//show current score
showScore(){
    $(".score", this.board)
    .text(this.score);
    $(".high-score", this.board)
    .text(this.highScore)
}
// display timer
showTimer(){
    $(".timer", this.board).text(this.seconds)
}

// handleSubmit w/out reload, axios
async handleSubmit(evt){
    evt.preventDefault();
    // grab the submitted word
    const $word = $(".word", this.board);
    let word = $word.val()

// if empty guess, return error message
if ($word.val() === ""){
    this.showMessage("Please submit a word.")
    return;
}
//if word already in set Words, return + error
if (this.words.has(word)){
    this.showMessage(`You have already submitted ${word}, please try another word.` )
    return;
}
// else, call to server to check word
const response = await axios.get("/check-word", {params: {word: word}})

if (response.data.result === "not-word"){
    this.showMessage(`Your answer, ${word}, is not a valid word. Please try again.`)
}
else if (response.data.result === "not-on-board"){
    this.showMessage(`Your word, ${word}, is not on the board. Please try again.`)
}
// if word is valid
else {
    //add word to set
    this.words.add(word)
    // note successfull addition
    this.showMessage(`Added ${word}`)
    // add word to list of successfully submitted words.
    this.showWord(word)
    // increase score
    this.score += word.length
    this.showScore()
    return;
}
}

async timeCount(){
    // reduce seconds amount on the interval, display the timer
    // this.timer = setInterval(this.timeCount.bind(this), 1000);
    this.seconds -= 1;
    this.showTimer();
//if timer reaches zero, clear timer and wait for scoregame
    if (this.seconds === 0){
        clearInterval(this.timer);
        await this.scoreGame();
    }

}


//showing score needs to be async to prevent reload 
async scoreGame(){
    const response = await axios.post("/post-score", {score: this.score});
    $(".messages").remove()
    $(".add-word").remove();
    $(".score").text("Your finale score is " + this.score);
   
// if current score > high score, update high score
    if (this.score > this.highScore){
        this.highScore = this.score;
        $(".high-score").text("Congrats! Your new high score is " + this.highScore)
        return;
    }
    // $(".replay").show()


}
}

// // // start game
// function startGame(){
//      let game = new BoggleGame("boggle")
// }

// $(".start").on("submit", startGame())

