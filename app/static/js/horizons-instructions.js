//------------------------------------//
// Define parameters.
//------------------------------------//

// Define comprehension threshold.
var max_errors = 0;
var max_loops = 2;
var num_loops = 0;

//------------------------------------//
// Define images for preloading.
//------------------------------------//

preload_images = [
  "../static/img/instructions01.png",
  "../static/img/instructions02.png",
  "../static/img/instructions03.png",
  "../static/img/instructions04.png",
  "../static/img/instructions05.png",
  "../static/img/instructions06.png",
  "../static/img/instructions07.png",
  "../static/img/instructions08.png",
  "../static/img/instructions09.png",
  "../static/img/instructions10.png",
  "../static/img/instructions11.png",
  "../static/img/instructions12.png",
  "../static/img/instructions13.png",
  "../static/img/instructions14.png",
];

//------------------------------------//
// Define instructions.
//------------------------------------//

// Define image scaling CSS.
const style = "width:auto; height:auto; max-width:100%; max-height:75vh;";

// Instructions (part 01)
var INSTRUCTIONS_01 = {
  type: 'instructions',
  pages: [
    `<img src='../static/img/instructions01.png' style="${style}"></img>`,
    `<img src='../static/img/instructions02.png' style="${style}"></img>`,
    `<img src='../static/img/instructions03.png' style="${style}"></img>`,
    `<img src='../static/img/instructions04.png' style="${style}"></img>`,
    `<img src='../static/img/instructions05.png' style="${style}"></img>`,
    `<img src='../static/img/instructions06.png' style="${style}"></img>`,
    `<img src='../static/img/instructions07.png' style="${style}"></img>`,
    `<img src='../static/img/instructions08.png' style="${style}"></img>`,
    `<img src='../static/img/instructions09.png' style="${style}"></img>`,
    `<img src='../static/img/instructions10.png' style="${style}"></img>`,
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
    `<img src='../static/img/instructions11.png' style="${style}"></img>`,
    `<img src='../static/img/instructions12.png' style="${style}"></img>`,
    `<img src='../static/img/instructions13.png' style="${style}"></img>`,
    `<img src='../static/img/instructions14.png' style="${style}"></img>`,
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next"
}

// Comprehension check.
var COMPREHENSION = {
  type: 'horizons-comprehension'
}

// Define instructions loop.
var INSTRUCTIONS = {
  timeline: [
    INSTRUCTIONS_01,
    PRACTICE_H5,
    PRACTICE_H10,
    INSTRUCTIONS_02,
    COMPREHENSION
  ],
  loop_function: function(data) {

    // Extract number of errors.
    const num_errors = data.values().slice(-1)[0].num_errors;

    // Check if instructions should repeat.
    if (num_errors > max_errors) {
      num_loops++;
      if (num_loops >= max_loops) {
        low_quality = true;
        return false;
      } else {
        return true;
      }
    } else {
      return false;
    }

  }
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
