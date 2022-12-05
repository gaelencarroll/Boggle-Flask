class BoggleComponents{
    constructor(id, time=60){
        this.time = time
        this.words = new Set()
        this.boggle_board = $('#'+ id)
        this.score = 0
        $('.new-word',this.boggle_board).on('submit',this.handleSubmit.bind(this))
        this.clock = setInterval(this.timer.bind(this),1000)
    }

    async handleSubmit(evt){
        evt.preventDefault()
        const $word = $('.word',this.boggle_board)
        let word = $word.val()
        
        if (this.words.has(word)){
            this.displayMessage(`You have already found this word: ${word}`,'err')
            return 
        }

        const res = await axios.get('/guess-word',{ params :{word: word}})
        console.log(res)
        if(res.data.result === 'not-on-board'){
            this.displayMessage(`The word, ${word} does not exist on this board. Please try again.`,'err')
        }
        else if (res.data.result === 'not-word'){
            this.displayMessage(`${word} is not a valid word. Please try again.`,'err')
        }
        else if (res.data.result === 'ok'){
            this.wordList(word)
            this.words.add(word)
            this.displayMessage(`Correct! Accepted word: ${word}`,'ok')
            this.score += word.length
            this.updateScore()
        }
        }

    displayMessage(message,cls){
        $('.message', this.boggle_board).text(message).removeClass().addClass(`message ${cls}`)
    }

    wordList(word){
        $('.words-list', this.boggle_board).append($('<li>',{text:word}))
    }

    updateScore(){
        $('.score-num', this.boggle_board).text(this.score)
    }

    displayTimer(){
        $('.timer-num', this.boggle_board).text(this.time)
    }

    async timer(){
        let seconds = this.time -= 1
        this.displayTimer()
        if (seconds === 0){
            clearInterval(this.clock)
            await this.endOfGame()
        }
    }

    async endOfGame(){
        const res = await axios.post('/update-score',{score: this.score})
        if (res.data.record){
            this.displayMessage(`Congrats! You beat your record. Your new high score is: ${this.score}`,'ok')
        }
        else{
            this.displayMessage(`Your final score is: ${this.score}`,'ok')
        }
        $('.new-word',this.boggle_board).hide()
        $('.timer', this.boggle_board).hide()
    }


}