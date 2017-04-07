/**
 * Created by Erick Fernando Cobo on 4/6/2017.
 */
$(function () {
    $("#get-json").click(function (e) {
        e.preventDefault();
        var origen = $("#Origen").val();
        var destino = $("#Destino").val();
        var prioridad = $("#Prioridad").val();
        $.ajax({
            "async": true,
            "crossDomain": true,
            "url": "http://127.0.0.1:5000/api/get-route",
            "method": "POST",
            "headers": {
                "authorization": "Basic ZmNvYm85NTp2aXBlcjE4Mjk=",
                "content-type": "application/json"
            },
            "processData": false,
            "data": JSON.stringify({Origen: origen, Destino: destino, Prioridad: prioridad}),
            success: function (response) {
                var ruta = response['Orden'];
                var viajes = ruta.length - 1;
                var html = "<div class='container-fluid col-md-8' id='ruta'><h4>Ruta: " + ruta + "</h4>";
                for (var i = 0; i < viajes; i++) {
                    var transporte = response[ruta[i]];
                    var nodo = ruta[i];
                    html += "<div id='nodo'><label>"+ (i+1) + ")"+ nodo + "</label><br>";
                    if (transporte.hasOwnProperty('Bus')) {
                        html += "<label>Transporte: Bus</label><br><ul>";
                        for (var key in transporte['Bus']) {
                            if (key != 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Bus'][key] + "</li>";
                            }
                        }
                        html += "</ul></div></div>"
                    } else if (transporte.hasOwnProperty('Taxi')) {
                        html += "<label>Transporte: Taxi</label><ul>";
                        for (var key in transporte['Taxi']) {
                            if (key != 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Taxi'][key] + "</li>";
                            }
                        }
                        html += "</ul></div></div>"
                    } else if (transporte.hasOwnProperty('Tren')) {
                        html += "<label>Transporte: Tren</label><br><ul>";
                        for (var key in transporte['Tren']) {
                            if (key != 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Tren'][key] + "</li>";
                            }
                        }
                        html += "</ul></div></div>"
                    } else {
                        html += "<label>Transporte: Avion</label><br><ul>";
                        for (var key in transporte['Avion']) {
                            if (key != 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Avion'][key] + "</li>";
                            }
                        }
                        html += "</ul></div></div>"
                    }
                }
                var alternativas = $("#detalles-ruta");
                alternativas.html(html);
                alternativas.css({"color": "red", "opacity": "0.3"});
                alternativas.animate({"color": "white", "opacity": "1", "fontSize": "2.2em", "padding": "100px"}, 3000);
                console.log(response);
            },
            error: function (response) {
                console.log(response);
                alert("Error: " + response['Mensaje'])
            }
        });
    });
});
