/*
* Horizons task plugin
* runs the horizons task
* Author: Isabel Zaller
*/

jsPsych.plugins["horizons-task"] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'horizons-task',
    parameters: {
      choices: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        pretty_name: "Choices",
        default: ['leftarrow', 'rightarrow'],
        array: true,
        description: "The valid keys that the subject can press to indicate a response"
      },
      forced_choices: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        pretty_name: "Forced choices",
        array: true,
        default: undefined,
        description: "The preselected first four choices (left vs right)"
      },
      horizon: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: "Horizon",
        default: 5,
        description: "The number of rounds in the game (either 5 or 10)"
      },
      left: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        pretty_name: "left",
        default: 'leftarrow',
        description: "The key the subject presses to indicate choosing the left option"
      },
      right: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        pretty_name: "right",
        default: 'rightarrow',
        description: "The key the subject presses to indicate choosing the right option"
      },
      means: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: "Bandit mean payouts",
        array: true,
        default: [40, 50],
        description: "Array containing the mean payouts for the left and right bandits" // arr[0] = left, arr[1] = right
      },
      colors: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: "bandit colors",
        array: true,
        default: [],
        description: "The colors of the bandits"
      },
    }
  }

  // BEGINNING OF TRIAL
  plugin.trial = function(display_element, trial) {

    //--------------------------------------
    //---------SET PARAMETERS BEGIN---------
    //--------------------------------------

    //Note on '||' logical operator: If the first option is 'undefined', it evalutes to 'false' and the second option is returned as the assignment
    trial.choices = assignParameterValue(trial.choices, []);
    trial.left = assignParameterValue(trial.left, 'leftarrow');
    trial.right = assignParameterValue(trial.right, 'rightarrow');
    trial.horizon = assignParameterValue(trial.horizon, 5);
    trial.means = assignParameterValue(trial.means, [40, 50]);
    trial.colors = assignParameterValue(trial.colors, []);

    //Convert the parameter variables to those that the code below can use
    var forced_choices = trial.forced_choices; // stores the forced choices for the first four rounds
    var horizon = trial.horizon;
    var left = trial.left; // key push to indicate left

    var left_mu = trial.means[0];
    var right_mu = trial.means[1];

    var left_numbers = set_numbers(left_mu);
    var right_numbers = set_numbers(right_mu);

    var left_color = trial.colors[0];
    var right_color = trial.colors[1];
    var points_earned = 0;


    //--------------------------------------
    //----------SET PARAMETERS END----------
    //--------------------------------------



    //--------Set up Canvas begin-------

    //Create a canvas element and append it to the DOM
    var canvas = document.createElement("canvas");
    display_element.appendChild(canvas);

    //The document body IS 'display_element' (i.e. <body class="jspsych-display-element"> .... </body> )
    var body = document.getElementsByClassName("jspsych-display-element")[0];

    //Save the current settings to be restored later
    var originalMargin = body.style.margin;
    var originalPadding = body.style.padding;

    //Remove the margins and paddings of the display_element
    body.style.margin = 0;
    body.style.padding = 0;

    //Remove the margins and padding of the canvas
    canvas.style.margin = 0;
    canvas.style.padding = 0;

    //Get the context of the canvas so that it can be painted on.
    var ctx = canvas.getContext("2d");

    //Declare variables for width and height, and also set the canvas width and height to the window width and height
    var canvasWidth = canvas.width = window.innerWidth;
    var canvasHeight = canvas.height = window.innerHeight;

    var centerX = canvasWidth / 2; // midpoint of canvas
    var scalefactor = canvasHeight / 1080; // scalefactor allows different window sizes

    var w = 120 * scalefactor; // width of each box of the bandit
    var h = 90 * scalefactor; // height of each box of the bandit
    var font_size = Math.round(40 * scalefactor) + "px"; // font size for text in the bandit

    var left_x = centerX - 4 * w / 3; // x coordinate of top left corner of top box of left bandit
    var right_x = centerX; // x coordinate of top left corner of top box of right bandit
    var bandit_Y_initial = 0.05 * canvasHeight; // y coordinate of top left corner of both bandits

    //--------Set up Canvas end-------



    //--------Horizons variables and function calls begin--------

    //This is the main part of the trial that makes everything run

    // Global variable for the current round number
    var round = 0;

    var keys_pressed = []; // stores the key the subject pressed in each round (round 1 = index 0)
    var response_times = []; // stores the subject's response time for each round (round 1 = index 0)

    //Declare global variable to be defined in startKeyboardListener function and to be used in end_trial function
    var keyboardListener;

    playGame();


    //--------horizons variables and function calls end--------



    //-------------------------------------
    //-----------FUNCTIONS BEGIN-----------
    //-------------------------------------

    //----JsPsych Functions Begin----

    // function to start the first keyboard listener
    function startKeyboardListener(){
      //Start the response listener if there are choices for keys
      if (trial.choices != jsPsych.NO_KEYS) {
        //Create the keyboard listener to listen for subjects' key response
        keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
          callback_function: after_response, //Function to call once the subject presses a valid key
          valid_responses: [trial.forced_choices[0]], //The keys that will be considered a valid response and cause the callback function to be called
          rt_method: 'performance', //The type of method to record timing information.
          persist: false, //If set to false, keyboard listener will only trigger the first time a valid key is pressed. If set to true, it has to be explicitly cancelled by the cancelKeyboardResponse plugin API.
          allow_held_key: false //Only register the key once, after this getKeyboardResponse function is called. (Check JsPsych docs for better info under 'jsPsych.pluginAPI.getKeyboardResponse').
        });
      }
    }

    function end_trial(){

      //Kill the keyboard listener if keyboardListener has been defined
      if (typeof keyboardListener !== 'undefined') {
        jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
      }

      //Place all the data to be saved from this trial in one data object
      var trial_data = {
        "response_times": response_times,
        "keys_pressed": keys_pressed,
        "horizon": horizon,
        "forced_choices": forced_choices,
        "right_color": right_color,
        "left_color": left_color,
        "left_mu": left_mu,
        "right_mu": right_mu,
        "left_numbers": left_numbers,
        "right_numbers": right_numbers,
        "points_earned": points_earned
      }

      //Remove the canvas as the child of the display_element element
      display_element.innerHTML='';

      //Restore the settings to JsPsych defaults
      body.style.margin = originalMargin;
      body.style.padding = originalPadding;

      //End this trial and move on to the next trial
      jsPsych.finishTrial(trial_data);
    }

    //Function to record the first response by the subject
    function after_response(info) {

      //Kill the keyboard listener if keyboardListener has been defined
      if (typeof keyboardListener !== 'undefined') {
        jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
      }

      // reinitialize this to record multiple responses
      if (round < 3) { // forced choices
        keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
          callback_function: after_response,
          valid_responses: [trial.forced_choices[round + 1]],
          rt_method: 'performance',
          persist: false,
          allow_held_key: false
        });
      }
      else if (round < horizon - 1) { // allow choice
        keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
          callback_function: after_response,
          valid_responses: trial.choices,
          rt_method: 'performance',
          persist: false,
          allow_held_key: false
        });
      }
      else { // wait 3 seconds, then end trial
        jsPsych.pluginAPI.setTimeout(function() {
          end_trial();
        }, 1500);
      }

      // add the response to the array
      keys_pressed.push(jsPsych.pluginAPI.convertKeyCodeToKeyCharacter(info.key));
      response_times.push(info.rt);

      // determine
      var text_left = "XX";
      var text_right = "XX";
      if (jsPsych.pluginAPI.compareKeys(info.key, trial.left)) {
        text_left = left_numbers[round];
        points_earned += left_numbers[round];
      }
      else if (jsPsych.pluginAPI.compareKeys(info.key, trial.right)) {
        text_right = right_numbers[round];
        points_earned += right_numbers[round];
      }

      // draw an updated version of the bandit
      updateBandit(text_left, text_right);

      // update round number and check if we have completed the game
      round++;

    }

    //----JsPsych Functions End----

    //----horizons Functions Begin----

    // set the payout amounts for the bandits from a gaussian distribution with a fixed stdev of 8
    function set_numbers(mu){
      var numbers = [];
      for (i = 0; i < horizon; i++) {
        numbers.push(Math.max(Math.floor(gaussianRandom(mu, 8)), 0)); // ensure that no payouts are negative
      }
      return numbers;
    }

    // function to generate a number based on a normal distribution around a given mean and stddev (sigma)
    function gaussianRandom(mean, sigma) {
      let u = Math.random()*0.682;
      return ((u % 1e-8 > 5e-9 ? 1 : -1) * (Math.sqrt(-Math.log(Math.max(1e-9, u)))-0.618))*1.618 * sigma + mean;
    }

    function drawBandit(){
      ctx.lineWidth = "6"; // width of lines forming bandits
      lineWidth = ctx.lineWidth;

      // draw an outline of the bandits
      for (i = 0; i < horizon; i++) {
        // draw left bandit
        ctx.strokeStyle = left_color;
        ctx.strokeRect(left_x, bandit_Y_initial + h*i, w, h); // ...(x of upper left, y of upper left, width, height) ** top left = (0, 0)

        // draw right bandit
        ctx.strokeStyle = right_color;
        ctx.strokeRect(right_x, bandit_Y_initial + h*i, w, h); // ...(x of upper left, y of upper left, width, height) ** top left = (0, 0)
      }

      // draw arms (start at top of third box)
      var radius = 15 * scalefactor;

      // left arm
      ctx.strokeStyle = ctx.fillStyle = left_color;
      ctx.beginPath();
      ctx.moveTo(left_x, bandit_Y_initial + 2*h);
      ctx.lineTo(left_x - w, bandit_Y_initial + 1.5*h);
      ctx.stroke();
      ctx.arc(left_x - w, bandit_Y_initial + 1.5*h, radius, 0, 2 * Math.PI, false);
      ctx.fill();

      // right arm
      ctx.strokeStyle = ctx.fillStyle = right_color;
      ctx.beginPath();
      ctx.moveTo(right_x + w, bandit_Y_initial + 2*h);
      ctx.lineTo(right_x + 2*w, bandit_Y_initial + 1.5*h);
      ctx.stroke();
      ctx.arc(right_x + 2*w, bandit_Y_initial + 1.5*h, radius, 0, 2 * Math.PI, false);
      ctx.fill();

      // // draw in first forced choice
      ctx.fillStyle = 'green';
      if (jsPsych.pluginAPI.compareKeys(forced_choices[0], left)) { // force left
        ctx.fillRect(left_x + lineWidth/2, bandit_Y_initial + h*round + lineWidth/2, w - lineWidth, h - lineWidth);
      }
      else { // force right
        ctx.fillRect(right_x + lineWidth/2, bandit_Y_initial + h*round + lineWidth/2, w - lineWidth, h - lineWidth);
      }
    }

    function updateBandit(text_left, text_right){

      // clear the previous forced choice (green square)
      if (round < 4) {
        if (jsPsych.pluginAPI.compareKeys(forced_choices[round], left)) { // clear left
          ctx.clearRect(left_x + lineWidth/2, bandit_Y_initial + h*round + lineWidth/2, w - lineWidth, h - lineWidth);
        }
        else { // clear right
          ctx.clearRect(right_x + lineWidth/2, bandit_Y_initial + h*round + lineWidth/2, w - lineWidth, h - lineWidth);
        }
      }
      else if (round < horizon) {
        ctx.clearRect(left_x + lineWidth/2, bandit_Y_initial + h*round + lineWidth/2, w - lineWidth, h - lineWidth);
        ctx.clearRect(right_x + lineWidth/2, bandit_Y_initial + h*round + lineWidth/2, w - lineWidth, h - lineWidth);
      }

      // initialize text style
      ctx.textBaseline = 'middle';
      ctx.font = ctx.font.replace(/\d+px/, font_size);
      ctx.fillStyle = 'black';
      lineWidth = ctx.lineWidth;

      // write text for left bandit
      ctx.fillText(text_left, left_x + (w / 3), bandit_Y_initial + (h / 2) + h*round); // ...("text", x coord, y coord)

      // write text for right bandit
      ctx.fillText(text_right, right_x + (w / 3), bandit_Y_initial + (h / 2) + h*round); // ...("text", x coord, y coord)

      // draw in green squares for the next round
      ctx.fillStyle = 'green';
      if (round < 3) {             // draw in forced choice for the next round
        if (jsPsych.pluginAPI.compareKeys(forced_choices[round + 1], left)) { // force left
          ctx.fillRect(left_x + lineWidth/2, bandit_Y_initial + h*(round + 1) + lineWidth/2, w - lineWidth, h - lineWidth);
        }
        else { // force right
          ctx.fillRect(right_x + lineWidth/2, bandit_Y_initial + h*(round + 1) + lineWidth/2, w - lineWidth, h - lineWidth);
        }
      }
      else if (round < horizon - 1) {
        ctx.fillRect(left_x + lineWidth/2, bandit_Y_initial + h*(round + 1) + lineWidth/2, w - lineWidth, h - lineWidth);
        ctx.fillRect(right_x + lineWidth/2, bandit_Y_initial + h*(round + 1) + lineWidth/2, w - lineWidth, h - lineWidth);
      }
    }


    function playGame(){
      // display the bandit
      drawBandit();

      //Start to listen to subject's key responses
      startKeyboardListener();
    }

    //----horizons Functions End----

    //----General Functions Begin//----

    // Function to assign the default values for the staircase parameters (source: jspsych-rdk.js)
    function assignParameterValue(argument, defaultValue){
      return typeof argument !== 'undefined' ? argument : defaultValue;
    }

    //----General Functions End//----

    //-------------------------------------
    //-----------FUNCTIONS END-------------
    //-------------------------------------

  };// END OF TRIAL

  //Return the plugin object which contains the trial
  return plugin;
})();
