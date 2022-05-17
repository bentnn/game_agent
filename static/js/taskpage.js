const codemirrorEditor = CodeMirror(document.getElementById('editor'), {
    lineNumbers: true,
    mode: "javascript",
    theme: "base16-dark"
  });

var editorClass = document.getElementsByClassName("CodeMirror");
for(var i = 0; i < editorClass.length; i++){
    editorClass[i].style.height = "100%";
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

$(document).ready(function () {
  $('#submit-code').on('click', function () {
      let lang = $('#select-laguage').val();
      let code = codemirrorEditor.getValue();
      let obj = {
        code: code,
        lang: lang,
        task: $('#submit-code').attr('task')
      };
      console.log(JSON.stringify(obj));
      let url = `http://127.0.0.1:8000/course/api/testcode/`;
      fetch(url, {
        method: 'POST',
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(obj)
      }).then(res => {
        return res.json();
      }).then(val => {
        let str = 'Вывод: ' + val.output + '\n\n';
        let err = 'Ошибка: ' + val.error;
        $('#output-text').val(str + err);
      });
  });
});