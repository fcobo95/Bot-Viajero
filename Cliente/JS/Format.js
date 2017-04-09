$(document).ready(function () {
    $(function () {
        var alternatives = $("#get-alternatives", function () {
            $("#get-route").click(function () {
                alternatives.css({"width": "1px", "height": "1px", "border-radius": "20%", "display": "inline"});
                alternatives.animate({
                    "width": "150px",
                    "height": "40px",
                    "margin": "30px 850px",
                    "border-radius": "5%",
                    "margin-left": "68%",
                    "text-align": "center",
                    "background-color": "rgb(0,0,255)"
                }, 1800)
            });
            alternatives.css("display", "none");
        });

        var rutas = $("#get-route").button();
        rutas.css({"width": "1px", "height": "1px", "border-radius": "20%"});
        rutas.animate({
            "width": "150px",
            "height": "40px",
            "margin": "10px",
            "margin-left": "68%",
            "border-radius": "5%",
            "text-align": "center",
            "background-color": "rgb(29,181,24)"
        }, 1800);

        var body = $("body");
        body.css({"background-repeat": "no-repeat", "background-attachment": "fixed"});

        var mapa = $(".map");
        mapa.css({"width": "10", "border-radius": "5%"});
        mapa.addClass("img-responsive");
        mapa.animate({"width": "450"}, "slow");

        var origen = $("#Origen");
        var origen_field = $("#origen-field");
        origen.select();
        origen.css({
            "width": "1px",
            "height": "25px",
            "border": "3px solid black",
            "border-radius": "0%",
            "margin": "0px",
            "background-color": "rgb(0,0,0)"
        });
        origen_field.css({"width": "1px", "height": "25px", "border-radius": "0%", "margin-left": "33.3%"});
        origen.animate({
            "width": "150px",
            "height": "25px",
            "border-radius": "25%",
            "background-color": "rgb(180,220,220)",
            "margin": "20px",
            "margin-left": "33.3%"
        }, 1800);

        var destino = $("#Destino");
        var destino_field = $("#destino-field");
        destino.select();
        destino.css({
            "width": "1px",
            "height": "25px",
            "border": "3px solid black",
            "border-radius": "0%",
            "margin": "0px",
            "background-color": "rgb(0,0,0)"
        });
        destino_field.css({"width": "1px", "height": "25px", "border-radius": "0%", "margin-left": "33.3%"});
        destino.animate({
            "width": "150px",
            "height": "25px",
            "border-radius": "25%",
            "background-color": "rgb(180,220,220)",
            "margin": "20px",
            "margin-left": "33.3%"
        }, 1800);

        var prioridad = $("#Prioridad");
        var prioridad_field = $("#prioridad-field");
        prioridad.select();
        prioridad.css({
            "width": "1px",
            "height": "25px",
            "border": "3px solid black",
            "border-radius": "0%",
            "margin": "0px",
            "background-color": "rgb(0,0,0)"
        });
        prioridad_field.css({"width": "1px", "height": "25px", "border-radius": "0%", "margin-left": "33.3%"});
        prioridad.animate({
            "width": "150px",
            "height": "25px",
            "border-radius": "25%",
            "background-color": "rgb(180,220,220)",
            "margin": "20px",
            "margin-left": "33.3%"
        }, 1800);

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


        var h2 = $("h2");
        h2.css({"color": "white", "text-align": "center"});

        var h3 = $("h3");
        h3.css({"color": "white", "text-align": "right"})
    });
});
