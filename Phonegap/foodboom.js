function search(term){
    show_loading();
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
            hide_loading();
        });
}

function show_similar(yelp_id) {
    show_loading()
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
        hide_loading();
   });
}

function set_coords(position){
    lat = position.coords.latitude;
    lon = position.coords.longitude;
}

function show_loading(){
    $.mobile.loading( 'show', {
        text: 'Searching',
        textVisible: true,
        theme: 'b',
        html: ""
    });
}

function hide_loading(){
    $.mobile.loading( 'hide', {
    });
}



var to;
var term;
var lat;
var lon;
$(document).ready(function(){
    $('#search').parent().find('input').val('');
    $('#search').parent().find('input').focus();
    $('#search').parent().find('input').keyup(function(){
        if($(this).val().length > 2 && term != $(this).val()){
            hide_loading();
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
