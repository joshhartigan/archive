$(function () {

  var tasks = [
    "try adding 8 and 9.",
    "subtract 4 from 18."
  ];

  var answers = [
    "ADD 8,9",
    "SUB 18,4"
  ]

  var currentTask = tasks[0];
  var currentAnswer = answers[0];

  var welcome = "TryAssembly v1.0.0 -- github.com/joshhartigan\n";
  var jqconsole = $('#console').jqconsole(welcome, "asm $ ");

  // evaluate assembly instructions
  var assemble = function(instruction, arg1, arg2) {
   switch (instruction) {
    case "ADD":
      return window.eval(arg1 + "+" + arg2); break;
    case "SUB":
      return arg1 - arg2; break;
    }
  };

  // move to the next task
  var nextTask = function() {
    currentTask = tasks[tasks.indexOf(currentTask) + 1];
    currentAnswer = answers[answers.indexOf(currentAnswer) + 1];

    $("#info").html(infoText[currentTask][0]);
    $("#task").html(infoText[currentTask][1]);
  }

  // prompt for input
  var answerPrompt = function(answer, task) {
    jqconsole.Prompt(true, function (input) {
      if (input == answer) {
        var phrase = input.split(" ");
        var args = phrase.length > 1? phrase[1].split(",") : "";
        jqconsole.Write("correct: see the next task below.\n", "jqconsole-output");
        jqconsole.Write(assemble(phrase[0], args[0], args[1]) + '\n', "jqconsole-output");
        nextTask();
      } else {
        jqconsole.Write("sorry, that's not right. " + task + '\n', "jqconsole-output");
      }
      // restart prompt
      answerPrompt(currentAnswer, currentTask);
    });
  };
  answerPrompt(currentAnswer, currentTask);
});
