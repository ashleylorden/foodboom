function search(term){
    var results = $.get(
        'http://foodboom.herokuapp.com/search/' + term,
        function(data){ 
            $('#search').empty();
            var restaurants = jQuery.parseJSON(data);
            for (r in restaurants) {
                $('#search').append(
                    '<li data-theme="c">' + 
                        '<a href="#" class="search-result" id="' + restaurants[r].yelp_id + '">' +
                        restaurants[r].name + ' <span class="address">(' + restaurants[r].address + ')</span>'+ 
                        '</a>' +
                    '</li>'
                );
            }
            $('ul').listview('refresh');
        });
}

function show_similar(yelp_id) {
    var coords = lat + ',' + lon;
    $.get("http://foodboom.herokuapp.com/similar/" + yelp_id + "/" + coords, function(data) {
        restaurants = jQuery.parseJSON(data);
        $('#search').empty();
        for (var i=0; i<3; i++) {
            $("#search").append(
                '<li data-theme="b">' +
                    '<a href="' + restaurants[i].mobile_url + 
                        '" data-transition="slide">' + 
                        restaurants[i].name + ' ' +
                        ' - ' + restaurants[i].rating + ' stars - ' +
                        Math.round(restaurants[i].distance) + ' mts away' +
                    '</a>' +
                '</li>'
            );
            $('ul').listview('refresh');
       }
   });
}

function set_coords(position){
    lat = position.coords.latitude;
    lon = position.coords.longitude;
}


var to;
var term;
var lat;
var lon;
$(document).ready(function(){
    $('#search').parent().find('input').val('');
    $('#search').parent().find('input').keyup(function(){
        if($(this).val().length > 2 && term != $(this).val()){
            window.clearTimeout(to);
            term = $(this).val();
            to = setTimeout(function(){ search(term) }, 700);
        }
    });
    $('body').on('click', 'a.search-result', function(){
        $('#search').parent().find('input').val($(this).text());
        // $('#search').parent().find('input').attr('readonly', 'readonly');
        show_similar($(this).attr('id'));
    });

    // Get location
    navigator.geolocation.getCurrentPosition(set_coords);
    
});
