$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        let text = $('#toggleMenu').text();
        if (text[0] == 'С'){
           $('#toggleMenu').text('Показать меню');
        }
        else{
           $('#toggleMenu').text('Скрыть меню');
        }
    });

    let articlePage = document.getElementById('main-text');
    
    let pagesUrl = 'http://127.0.0.1:8000/course/api/pages/';
    
    fetch(pagesUrl).then(function(elem){
        return elem.json();
    }).then(function(res){
        let themes = res.map(x => x.title);
        for (let theme of themes){
            $('#' + theme).on('click', function () {
                let url = `http://127.0.0.1:8000/course/api/pages/${'?title=' + theme}`;
                fetch(url).
                then(function(article){
                    return article.json();
                }).then(function(json){
                    articlePage.innerHTML = json.text;
                    console.log(json);
                });
            });
        }
    });
});