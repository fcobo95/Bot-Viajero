/**
 * Created by Erick Fernando Cobo on 4/6/2017.
 */

$(document).ready(function () {
    $(function () {

        var mapa = $(".map");
        mapa.css({"width": "10", "border-radius": "5%"});
        mapa.addClass("img-responsive");
        mapa.animate({"width": "480"}, "slow");

        var origen = $("#Origen");
        origen.select();
        origen.css({"width": "1px", "height": "25px", "border-radius": "5%"});
        origen.animate({"width": "150px", "height": "25px", "border-radius": "5%", "background-color": "rgb(180,220,220)"}, 1800);

        var destino = $("#Destino");
        destino.select();
        destino.css({"width": "1px", "height": "25px", "border-radius": "5%"});
        destino.animate({"width": "150px", "height": "25px", "border-radius": "5%", "background-color": "rgb(220,220,180)"}, 1800);

        var prioridad = $("#Prioridad");
        prioridad.select();
        prioridad.css({"width": "1px", "height": "25px", "border-radius": "5%"});
        prioridad.animate({"width": "150px", "height": "25px", "border-radius": "5%", "background-color": "rgb(220,180,220)"}, 1800);

        var sign_out = $("#sign-out");
        sign_out.css({"width": "100px"});

        var header = $(".rutass");
        header.addClass("text-center");
        header.css({
            "color": "white",
            "opacity": "0.1"
        });
        header.animate({"opacity": "0.9"}, "slow");

        var crc = $("#crc");
        crc.css({
            "color": "white",
            "opacity": "0.1"
        });
        crc.animate({"opacity": "0.9"});
    });
});
