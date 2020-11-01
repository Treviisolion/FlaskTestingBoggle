"use strict"

$(async function () {
    const $games = $("#games")
    const $score = $("#score")
    const $submitWord = $("#submitWord")
    const $result = $("#result")

    const timer = 60 //in seconds
    const words = [] //All valid words submitted
    let score = 0

    /**
     * Updates the score
     * @param {the amount of points to add to the score} points 
     */
    const updateScore = points => {
        score += points
        $score.text(`Score: ${score}`)
    }

    /**
     * Sends the word submitted by the user to the server to check if its a valid word on the board.
     * The response is shown to the user and if valid, the score is incremented by the lenght of the word.
     */
    $submitWord.on("submit", async function (evt) {
        evt.preventDefault();

        const word = $("#wordguess").val()
        if (!words.includes(word)) {
            const response = await axios.post('/api/submitword', {
                word
            })
            $result.text(`${word} is ${response.data}`)

            if (response.data === "ok") {
                updateScore(word.length)
                words.push(word) //Prevents resubmitting the same word
            }
        } else {
            $result.text(`${word} already used`)
        }
    });

    /**
     * Disables the form after a set amount of time and sends the score to the server, then shows the number of games and highscore to the user
     */
    setTimeout(async function () {
        $submitWord.hide()
        $result.text("Game Over")

        const response = await axios.post('/api/gameover', {
            score
        })

        $games.text(`Games: ${response.data.num_of_games} HighScore: ${response.data.highscore}`)
    }, timer * 1000)
});