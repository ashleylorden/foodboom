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
    var url ="http://foodboom.herokuapp.com/similar/" + yelp_id + "/" + coords;
    if (bearing != undefined) {
        url += '/' + bearing;
    }
    $.get(url, function(data) {
        restaurants = jQuery.parseJSON(data);
        $('#search').empty();
        for (var i=0; i<3; i++) {
            console.log(restaurants[i]);
            $("#search").append(
                '<li data-theme="b">' +
                    '<a href="' + restaurants[i].mobile_url + 
                        '" data-transition="slide">' + 
                        '<span style="font-size:22px;">'+restaurants[i].name + '</span> ' +
                        ' ' + '<span class="ui-li-count" style="font-size:21px;background-color:yellow;"> ' + restaurants[i].rating + '</span>' +
                        '<p class="distance" style=font-size:14px;>' + Math.round((restaurants[i].distance)/100) + ' blocks away' + '</p>'+
                        '<p style=font-size:14px;padding-top:-10px;>' + restaurants[i].address + '</p>' + '<p id="' + restaurants[i].yelp_id + '></p>'+ 
                    '</a>' +
                '</li>');
/*
                var cat_list = [];
                for (c in restaurants[i].categories) {
                    cat_list.push(c[0]);
                    alert(c);
                }
                alert(cat_list);
                $('#'+restaurants[i].yelp_id).append(cat_list.join());
  
*/
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
var bearing;
$(document).ready(function(){
    $('#search').parent().find('input').val('');
    $('#search').parent().find('input').focus();
    $('#search').parent().find('input').keyup(function(){
        $('#intro-text').hide();
        if($(this).val().length > 2 && term != $(this).val()){
            hide_loading();
            window.clearTimeout(to);
            term = $(this).val();
            to = setTimeout(function(){ search(term) }, 700);
        }
    });
    $('body').on('click', 'a.search-result', function(){
        if (navigator.compass != undefined) {
            navigator.compass.getCurrentHeading(onSuccess, onError);
        }
        $('#search').parent().find('input').val($(this).text());
        // $('#search').parent().find('input').attr('readonly', 'readonly');
        show_similar($(this).attr('id'));
    });

    // Get location
    navigator.geolocation.getCurrentPosition(set_coords);
    //navigator.compass.getCurrentHeading(onSuccess, onError);
    $('#compass').click(function(){
        navigator.compass.getCurrentHeading(onSuccess, onError);
    })
        
});

// onSuccess: Get the current heading
//
function onSuccess(heading) {
    bearing = heading.trueHeading;
}

// onError: Failed to get the heading
//
function onError() {
    alert('onError!');
}


