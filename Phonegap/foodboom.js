function search(term){
    var results = $.get(
        'http://foodboom.herokuapp.com/search/' + term,
        function(data){ 
            console.log(data);
            // Populate <li>s
        });
}

$(document).ready(function(){
    $('#search').parent().find('input').val('');
    $('#search').parent().find('input').keyup(function(){
        if($(this).val().length > 2){
            search($(this).val());
            console.log('search');
        }
    });
});
