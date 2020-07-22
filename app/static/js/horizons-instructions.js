//------------------------------------//
// Define parameters.
//------------------------------------//

// Define image scaling CSS.
const style = "width:auto; height:auto; max-width:100%; max-height:50vh;";

//------------------------------------//
// Define images for preloading.
//------------------------------------//

preload_images = [
  "../static/img/instr01.png",
  "../static/img/instr02.png",
  "../static/img/instr03.png",
  "../static/img/instr04.png",
  "../static/img/instr05.png",
  "../static/img/instr06.png",
  "../static/img/instr07.png",
  "../static/img/instr08.png",
  "../static/img/instr09.png",
  "../static/img/instr10.png",
];

//------------------------------------//
// Define instructions.
//------------------------------------//

// Instructions (part 01)
var INSTRUCTIONS_01 = {
  type: 'instructions',
  pages: [
    "<p><b>We are now beginning the experiment.</b><br>Use the right arrow key to move forward through these instructions.</p>",
    "<p>In this task, you will be playing a series of gambling games.<br>In each game you will be choosing between two <b>slot machines</b><br>of the sort you might find in a casino.</p>",
    `<p><img src='../static/img/instr01.png' style="${style}"></img></p><p>The slot machines will look like the ones above.</p>`,
    `<img src='../static/img/instr02.png' style="${style}"></img><p>Every time you choose to play a particular machine, its payout will be shown.<br>For example, in this case, the left machine was played and paid out 38 points.</p>`,
    `<p>During a game, a slot machine will pay out around the same number of points on average,<br>but there will be variability in the points on any given play.</p>`,
    `<p><img src='../static/img/instr03.png' style="${style}"></img></p><p>For example, the machine on the right might give out 50 points on average,<br>but on the first play you might see a reward of 49 points because of the variability...</p>`,
    `<img src='../static/img/instr04.png' style="${style}"></img></p><p>... on the second play you might get 56 points ...</p>`,
    `<p><img src='../static/img/instr05.png' style="${style}"></img></p><p>... if you play the right a third time you might get 37 points ...</p>`,
    `<img src='../static/img/instr06.png' style="${style}"></img></p><p>... and so on, such that if you were to play the right machine 10 times<br>in a row you might see these payouts ...</p>`,
    "<p>Both machines will have the same kind of variability and<br>this variability will stay constant throughout the task.</p>",
    "<p>In a game, one of the machines will always pay more on average and<br>hence is the better option to choose overall.</p>",
    `<p><img src='../static/img/instr07.png' style="${style}"></img></p>On any turn of a game, you can only choose to play one of the two machines and the number of trials in each game is determined by the height of the machines. For example, when the machines are 10 boxes high, there are 10 trials in that game ...`,
    `<p><img src='../static/img/instr01.png' style="${style}"></img></p><p>... when the stacks are 5 boxes high there are only 5 trials in the game</p>`,
    `<p><img src='../static/img/instr08.png' style="${style}"></img></p><p>The first 4 trials in each game are instructed trials. These instructed trials will be indicated by a green square inside the machine we want you to choose. You MUST press the button to choose this option. For example, if you are instructed to choose the left machine on the first turn, you will see the above.</p>`,
    `<p><img src='../static/img/instr09.png' style="${style}"></img></p><p>If you are instructed to choose the right machine on the second turn, you will see the above.</p>`,
    `<p><img src='../static/img/instr10.png' style="${style}"></img></p><p>Once these instructed trials are complete, you will have a free choice between the two stacks that is indicated by two green squares inside the two boxes you are choosing between.</p>`,
    "So to be sure that everything makes sense let's work through a few example games ... <p>Press the <strong>left arrow</strong> to play the left machine</p><p>Press the <strong>right arrow</strong> to play the right machine</p>",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next"
}

// Practice games
var PRACTICE_H5 = {
  type: "horizons-task",
  horizon: 5,
  colors: ["orange", "lightblue"],
  means: [40, 20],
  forced_choices: ['rightarrow', 'leftarrow', 'rightarrow', 'rightarrow']
}

var PRACTICE_H10 = {
  type: "horizons-task",
  horizon: 10,
  colors: ["lightblue", "orange"],
  means: [60, 70],
  forced_choices: ['leftarrow', 'leftarrow', 'rightarrow', 'rightarrow']
}

// Instructions (part 02)
var INSTRUCTIONS_02 = {
  type: "instructions",
  pages: [
    "Great job! Now you know the rule!",
    "Just to repeat, to make your choice:<p>Press the <strong>left arrow</strong> to play the left machine</p><p>Press the <strong>right arrow</strong> to play the right machine</p>",
    "<p>At the end of the task, the total number of points you've<br>earned will be converted into a <b>performance bonus.</b></p>",
    "<p>Next, we will ask you some questions about the task.<br>You need to answer all questions correctly to proceed.</p>",  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next"
}

// Define instructions loop.
var INSTRUCTIONS = {
  timeline: [
    INSTRUCTIONS_01,
    PRACTICE_H5,
    PRACTICE_H10,
    INSTRUCTIONS_02
  ]
}

//------------------------------------//
// Define transition screens.
//------------------------------------//

var READY_01 = {
  type: 'instructions',
  pages: [
    "Great job! You've passed the comprehension check.",
    "Get ready to begin <b>Block 1/2</b>. It will take ~X minutes.<br>Press next when you're ready to start.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(trial) {
    pass_message('starting block 1');
  }
}

var READY_02 = {
  type: 'instructions',
  pages: [
    "Take a break for a few moments and press any button when you are ready to continue.",
    "Get ready to begin <b>Block 2/2</b>. It will take ~X minutes.<br>Press next when you're ready to start.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(trial) {
    pass_message('starting block 2');
  }
}
