/**
 * Created by Erick Fernando Cobo on 3/23/2017.
 */

url_base = 'http://localhost:5000/';
api = 'nombre/erick';
url = url_base + api;

$(document).ready(function () {
    $(".graph").click(function () {
        $.post(url, function () {
            alert("Nameeeee")
        });
        alert("You clicked the button!")
    })
});


// $(document).ready(function () {
//     $(".graph").on().post(url, function(){
//         alert("Got the map!.")
//     })
// });