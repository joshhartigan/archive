var editor = ace.edit('editor')

editor.setTheme('ace/theme/monokai')
editor.getSession().setMode('ace/mode/python')
editor.getSession().setTabSize(2)
editor.getSession().setUseSoftTabs(true)
editor.insert('# welcome to frankenlamp.\n# you can insert code here\n')

var frame = document.getElementsByClassName('frame')[0]

function evalLamp(line) {
  if (line[0] === 'print') {
    var printer = eval(line.slice(1).join(' '))
    frame.innerHTML += printer + '<br />'
  }
}

function runCode(code) {
  frame.innerHTML = ''

  var lines = code.split('\n')
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i].split(' ')
    evalLamp(line)
  }
}

editor.commands.addCommand({
  name: 'run',
  bindKey: { win: 'Shift-Enter', mac: 'Shift-Enter' },
  exec: function(editor) {
    runCode(editor.getValue())
  },
  readOnly: true
})

