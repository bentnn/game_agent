const codemirrorEditor = CodeMirror(document.getElementById('editor'), {
    lineNumbers: true,
    mode: "javascript",
    theme: "base16-dark"
  });

var editorClass = document.getElementsByClassName("CodeMirror");
for(var i = 0; i < editorClass.length; i++){
    editorClass[i].style.height = "100%";
}