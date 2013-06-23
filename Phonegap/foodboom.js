function search(term){
    var results = $.get(
        'http://foodboom.herokuapp.com/search/' + term,
        function(data){ 
            $('#search').empty();
            var restaurants = jQuery.parseJSON(data);
            console.log(restaurants);

            for (r in restaurants) {
                $('#search').append('<li data-theme="c">' + restaurants[r].name + '</li>');
            }
            $('ul').listview('refresh');
        });
}

function show_similar(yelp_id) {
   $.get("http://foodboom.herokuapp.com/similar/" + yelp_id, function(data) {
       restaurants = jQuery.parseJSON(data);
   });
   $("#results_list").find('*').remove();
   for (var i=0; i<3; i++) {
       $("#results_list").append("<li data-theme='c'><a href='" + restaurants[i].mobile_url + "'
                                  data-transition='slide'>" + restaurants[i].name + "</a></li>");
   }
}
6:40 PM
 


$(document).ready(function(){
    var mutex = 0;
    $('#search').parent().find('input').val('');
    $('#search').parent().find('input').keyup(function(){
        if($(this).val().length > 2 && mutex == 0){
            mutex = 1;
            search($(this).val());
            mutex = 0;
        }
    });
    
});
