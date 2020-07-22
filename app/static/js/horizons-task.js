//------------------------------------//
// Define horizons task games.
//------------------------------------//

// Preallocate space.
var HORIZONS = []

function generate_games(){

  // choices for a [2,2] game
  var forced_choices_two_two = []
  for (var i = 0; i < 3; i++) {
    forced_choices_two_two.push(['leftarrow', 'leftarrow', 'rightarrow', 'rightarrow']);
    forced_choices_two_two.push(['leftarrow', 'rightarrow', 'leftarrow', 'rightarrow']);
    forced_choices_two_two.push(['leftarrow', 'rightarrow', 'rightarrow', 'leftarrow']);
    forced_choices_two_two.push(['rightarrow', 'leftarrow', 'rightarrow', 'leftarrow']);
    forced_choices_two_two.push(['rightarrow', 'rightarrow', 'leftarrow', 'leftarrow']);
    forced_choices_two_two.push(['rightarrow', 'leftarrow', 'leftarrow', 'rightarrow']);
  }
  forced_choices_two_two.push(['leftarrow', 'rightarrow', 'leftarrow', 'rightarrow']);
  forced_choices_two_two.push(['rightarrow', 'leftarrow', 'leftarrow', 'rightarrow']);

  // choices for a [3,1] and [1,3] game
  var forced_choices_three_one = []
  for (var i = 0; i < 2; i++) {
    forced_choices_three_one.push(['leftarrow', 'leftarrow', 'leftarrow', 'rightarrow']);
    forced_choices_three_one.push(['leftarrow', 'leftarrow', 'rightarrow', 'leftarrow']);
    forced_choices_three_one.push(['leftarrow', 'rightarrow', 'leftarrow', 'leftarrow']);
    forced_choices_three_one.push(['rightarrow', 'leftarrow', 'leftarrow', 'leftarrow']);
    forced_choices_three_one.push(['rightarrow', 'rightarrow', 'rightarrow', 'leftarrow']);
    forced_choices_three_one.push(['rightarrow', 'rightarrow', 'leftarrow', 'rightarrow']);
    forced_choices_three_one.push(['rightarrow', 'leftarrow', 'rightarrow', 'rightarrow']);
    forced_choices_three_one.push(['leftarrow', 'rightarrow', 'rightarrow', 'rightarrow']);
  }
  forced_choices_three_one.push(['leftarrow', 'leftarrow', 'rightarrow', 'leftarrow']);
  forced_choices_three_one.push(['rightarrow', 'leftarrow', 'leftarrow', 'leftarrow']);
  forced_choices_three_one.push(['rightarrow', 'rightarrow', 'leftarrow', 'rightarrow']);
  forced_choices_three_one.push(['leftarrow', 'rightarrow', 'rightarrow', 'rightarrow']);

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

  for (var i = 0; i < 20; i++) {
    game_h1_two_two = {
      type: "horizons-task",
      horizon: 5,
      colors: function(){
        return jsPsych.randomization.sampleWithoutReplacement(colors, 1)[0];
      },
      means: function(){
        return jsPsych.randomization.sampleWithoutReplacement(means, 1)[0];
      },
      forced_choices: function(){
        return jsPsych.randomization.sampleWithoutReplacement(forced_choices_two_two, 1)[0];
      }
    }

    game_h6_two_two = {
      type: "horizons-task",
      horizon: 10,
      colors: function(){
        return jsPsych.randomization.sampleWithoutReplacement(colors, 1)[0];
      },
      means: function(){
        return jsPsych.randomization.sampleWithoutReplacement(means, 1)[0];
      },
      forced_choices: function(){
        return jsPsych.randomization.sampleWithoutReplacement(forced_choices_two_two, 1)[0];
      }
    }

    game_h1_three_one = {
      type: "horizons-task",
      horizon: 5,
      colors: function(){
        return jsPsych.randomization.sampleWithoutReplacement(colors, 1)[0];
      },
      means: function(){
        return jsPsych.randomization.sampleWithoutReplacement(means, 1)[0];
      },
      forced_choices: function(){
        return jsPsych.randomization.sampleWithoutReplacement(forced_choices_three_one, 1)[0];
      }
    }

    game_h6_three_one = {
      type: "horizons-task",
      horizon: 10,
      colors: function(){
        return jsPsych.randomization.sampleWithoutReplacement(colors, 1)[0];
      },
      means: function(){
        return jsPsych.randomization.sampleWithoutReplacement(means, 1)[0];
      },
      forced_choices: function(){
        return jsPsych.randomization.sampleWithoutReplacement(forced_choices_three_one, 1)[0];
      }
    }

    HORIZONS.push(game_h1_two_two);
    HORIZONS.push(game_h6_two_two);
    HORIZONS.push(game_h1_three_one);
    HORIZONS.push(game_h6_three_one);
  }
}

// generate all games before the participant enters the experiment
generate_games();
HORIZONS = jsPsych.randomization.shuffle(HORIZONS);
