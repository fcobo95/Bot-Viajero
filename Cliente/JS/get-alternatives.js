function alternativas() {
    $("#get-alternatives").click(function (event) {
        var origen = $("#Origen").val();
        var destino = $("#Destino").val();
        var prioridad = $("#Prioridad").val();
        event.preventDefault();
        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://127.0.0.1:5000/api/get-alternatives",
            "method": "POST",
            "headers": {
                "authorization": "Basic " + btoa(localStorage.getItem("Token")),
                "content-type": "application/json"
            },
            "processData": false,
            "data": JSON.stringify({Origen: origen, Destino: destino, Prioridad: prioridad}),
            success: function (response) {
                for (var alternativa = 0; alternativa < 4; alternativa++) {
                    var index = 1;
                    var ruta = response['Orden'];
                    var viajes = ruta.length - 1;
                    var html = "<div class='container-fluid col-md-3' id='alternativa'><h4>Ruta: " + ruta + "</h4>";
                    if (ruta[i['Alternativa' + index]]) {
                        for (var i = 0; i < viajes; i++) {
                            var transporte = response[ruta[i]];
                            var nodo = ruta[i];
                            html += "<div id='nodo'><label>" + (i + 1) + ") " + nodo + "</label><br>";
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
                    }
                    index++;
                }
                var alternativas = $("#rutas-alternativas");
                alternativas.html(html);
                alternativas.css({"color": "red", "opacity": "0.3"});
                alternativas.animate({"color": "white", "opacity": "1", "fontSize": "2.2em", "padding": "100px"}, 2000);
                console.log(response);
            },
            error: function (response) {
                console.log(response);
                alert("Error: " + response['Mensaje'])
            }
        };

        $.ajax(settings).done(function (response) {
            console.log(response);
        });
    });


}