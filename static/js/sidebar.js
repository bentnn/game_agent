$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        let text = $('#toggleMenu').text();
        if (text == 'Скрыть меню'){
           $('#toggleMenu').text('Показать меню');
        }
        else{
           $('#toggleMenu').text('Скрыть меню');
        }
    });

    let articlePage = document.getElementById('main-text');
    
    fetch(pagesUrl).then(function(elem){
        return elem.json();
    }).then(function(res){
        let themes = res.map(x => x.title);
        for (let theme of themes){
            $('#' + theme).on('click', function () {
                let prop = $('#' + theme).attr('disabled');
                if (prop === "disabled"){
                    return;
                }
                let url = $('#' + theme).val();
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