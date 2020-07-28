//------------------------------------//
// Questionnaires
//------------------------------------//

// Welcome screen
var WELCOME = {
  type: 'instructions',
  pages: [
    "<b>Welcome to the experiment!</b><br><br>We will get started with some surveys.<br>Please read each survey carefully and respond truthfully."
  ],
  show_clickable_nav: true,
  button_label_previous: 'Prev',
  button_label_next: 'Next'
}

// Demographics questionnaire
var DEMO = {
  type: 'survey-demo',
  data: {survey: 'demographics'}
};

// Demographics questionnaire
var DEBRIEF = {
  type: 'survey-debrief',
  data: {survey: 'debrief'}
};

// Penn State Worry Questionnaire
var pswq = {
  type: 'survey-template',
  items: [
    "If I don't have enough time to do everything, I do not worry about it.",
    "My worries overwhelm me.",
    "I do not tend to worry about things.",
    "Many situations make me worry.",
    "I know I should not worry about things, but I just can't help it.",
    "When I'm under pressure I worry a lot.",
    "I'm always worrying about something.",
    "I find it easy to dismiss worrisome thoughts.",
    "As soon as I finish one task, I start to worry about everything else I have to do.",
    "I never worry about anything.",
    "When there's nothing more I can do about a concern, I don't worry about it any more.",
    "I have been a worrier all my life.",
    "I notice that I have been worrying about things.",
    "Once I start worrying, I can't stop.",
    "I worry all the time.",
    "I worry about projects until they are done."
  ],
  scale: [
    "Not at all<br>typical of me",              // scored as 0
    "Not very<br>typical of me",                // scored as 1
    "Somewhat<br>typical of me",                // scored as 2
    "Fairly<br>typical of me",                  // scored as 3
    "Very<br>typical of me"                     // scored as 4
  ],
  reverse: [
    false, false, true, false, false, false, false, true,
    false, true, true, false, false, false, false, false
  ],
  instructions: 'Select the option that best describes how typical or characteristic each item is of you.',
  randomize_question_order: true,
  scale_repeat: 9,
  survey_width: 80,
  item_width: 40,
  data: {survey: 'pswq'}
}

// Intolerance of Uncertainty Questionnaire
var ius12 = {
  type: 'survey-template',
  items: [
    "Unforeseen events upset me greatly.",
    "It frustrates me not having all the information I need.",
    "Uncertainty keeps me from living a full life.",
    "One should always look ahead so as to avoid surprises.",
    "A small unforeseen event can spoil everything, even with the best of planning.",
    "When it's time to act, uncertainty paralyses me.",
    "When I am uncertain I can't function very well.",
    "I always want to know what the future has in store for me.",
    "I can't stand being taken by surprise.",
    "The smallest doubt can stop me from acting.",
    "I should be able to organize everything in advance.",
    "I must get away from all uncertain situations."
  ],
  scale: [
    "Not at all<br>characteristic<br>of me",
    "A little<br>characteristic<br>of me",
    "Somewhat<br>characteristic<br>of me",
    "Very<br>characteristic<br>of me",
    "Entirely<br>characteristic<br>of me"
  ],
  reverse: [
    false, false, false, false, false, false,
    false, false, false, false, false, false
  ],
  instructions: "Read each statement carefully and select which best describes you.",
  randomize_question_order: true,
  scale_repeat: 7,
  survey_width: 80,
  item_width: 42,
  data: {survey: 'ius12'}
}

// Need for Closure Scale
var nfc = {
  type: 'survey-template',
  items: [
    "I don't like situations that are uncertain.",
    "I dislike questions which could be answered in many different ways.",
    "I find that a well ordered life with regular hours suits my temperament.",
    "I feel uncomfortable when I don't understand the reason why an event occurred in my life.",
    "I feel irritated when one person disagrees with what everyone else in a group believes.",
    "I don't like to go into a situation without knowing what I can expect from it.",
    "When I have made a decision, I feel relieved.",
    "When I am confronted with a problem, I'm dying to reach a solution very quickly.",
    "I would quickly become impatient and irritated if I would not find a solution to a problem immediately.",
    "I don't like to be with people who are capable of unexpected actions.",
    "I dislike it when a person's statement could mean many different things.",
    "I find that establishing a consistent routine enables me to enjoy life more.",
    "I enjoy having a clear and structured mode of life.",
    "I do not usually consult many different opinions before forming my own view.",
    "I dislike unpredictable situations."
  ],
  scale: [
    "Strongly<br>disagree",
    "Moderately<br>disagree",
    "Slightly<br>disagree",
    "Slightly<br>agree",
    "Moderately<br>agree",
    "Strongly<br>agree"
  ],
  reverse: [
    false, false, false, false, false, false, false, false,
    false, false, false, false, false, false, false
  ],
  instructions: "Read each of the following statements and decide how much you agree with each according to your beliefs and experiences.",
  randomize_question_order: true,
  scale_repeat: 8,
  survey_width: 80,
  item_width: 42,
  data: {survey: 'nfc'}
}

// Define survey block
SURVEYS = jsPsych.randomization.shuffle([pswq, ius12, nfc]);
