//------------------------------------//
// Define horizons task games.
//------------------------------------//

// Preallocate space.
var HORIZONS = []

function generate_games(){

  var forced_22 = [] // choices for a [2,2] game
  for (var i = 0; i < 3; i++) {
    forced_22.push(['leftarrow', 'leftarrow', 'rightarrow', 'rightarrow']);
    forced_22.push(['leftarrow', 'rightarrow', 'leftarrow', 'rightarrow']);
    forced_22.push(['leftarrow', 'rightarrow', 'rightarrow', 'leftarrow']);
    forced_22.push(['rightarrow', 'leftarrow', 'rightarrow', 'leftarrow']);
    forced_22.push(['rightarrow', 'rightarrow', 'leftarrow', 'leftarrow']);
    forced_22.push(['rightarrow', 'leftarrow', 'leftarrow', 'rightarrow']);
  }
  forced_22.push(['leftarrow', 'rightarrow', 'leftarrow', 'rightarrow']);
  forced_22.push(['rightarrow', 'leftarrow', 'leftarrow', 'rightarrow']);

  var forced_31 = [] // choices for a [3,1] and [1,3] game
  for (var i = 0; i < 2; i++) {
    forced_31.push(['leftarrow', 'leftarrow', 'leftarrow', 'rightarrow']);
    forced_31.push(['leftarrow', 'leftarrow', 'rightarrow', 'leftarrow']);
    forced_31.push(['leftarrow', 'rightarrow', 'leftarrow', 'leftarrow']);
    forced_31.push(['rightarrow', 'leftarrow', 'leftarrow', 'leftarrow']);
    forced_31.push(['rightarrow', 'rightarrow', 'rightarrow', 'leftarrow']);
    forced_31.push(['rightarrow', 'rightarrow', 'leftarrow', 'rightarrow']);
    forced_31.push(['rightarrow', 'leftarrow', 'rightarrow', 'rightarrow']);
    forced_31.push(['leftarrow', 'rightarrow', 'rightarrow', 'rightarrow']);
  }
  forced_31.push(['leftarrow', 'leftarrow', 'rightarrow', 'leftarrow']);
  forced_31.push(['rightarrow', 'leftarrow', 'leftarrow', 'leftarrow']);
  forced_31.push(['rightarrow', 'rightarrow', 'leftarrow', 'rightarrow']);
  forced_31.push(['leftarrow', 'rightarrow', 'rightarrow', 'rightarrow']);

  var colors = [];
  for (var i = 0; i < 10; i++) {
    colors.push(["orange", "lightblue"]);
    colors.push(["lightblue", "orange"]);
  }

  var means = [
    [40, 10], [40, 20], [40, 28], [40, 32], [40, 36],
    [40, 44], [40, 48], [40, 52], [40, 60], [40, 70],
    [60, 30], [60, 40], [60, 48], [60, 52], [60, 56],
    [60, 64], [60, 68], [60, 72], [60, 80], [60, 90]
  ]

  forced_22 = jsPsych.randomization.shuffle(forced_22)
  forced_31 = jsPsych.randomization.shuffle(forced_31)
  colors = jsPsych.randomization.shuffle(colors)
  means = jsPsych.randomization.shuffle(means)

  for (var i = 0; i < 20; i++) {
    game_h1_22 = {
      type: "horizons-task",
      horizon: 5,
      colors: colors[i],
      means: means[i],
      forced_choices: forced_22[i],
      data: {phase: "task"}
    }

    game_h6_22 = {
      type: "horizons-task",
      horizon: 10,
      colors: colors[i],
      means: means[i],
      forced_choices: forced_22[i],
      data: {phase: "task"}
    }

    game_h1_31 = {
      type: "horizons-task",
      horizon: 5,
      colors: colors[i],
      means: means[i],
      forced_choices: forced_31[i],
      data: {phase: "task"}
    }

    game_h6_31 = {
      type: "horizons-task",
      horizon: 10,
      colors: colors[i],
      means: means[i],
      forced_choices: forced_31[i],
      data: {phase: "task"}
    }

    HORIZONS.push(game_h1_22);
    HORIZONS.push(game_h6_22);
    HORIZONS.push(game_h1_31);
    HORIZONS.push(game_h6_31);
  }
  
}

// generate all games before the participant enters the experiment
generate_games();
HORIZONS = jsPsych.randomization.shuffle(HORIZONS);
