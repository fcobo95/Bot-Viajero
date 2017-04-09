function alternativas() {
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
            var html = "";
            var index = 1;
            $.each(response, function (llave, valor) {
                html += "<span><label>Alternativa #" + index + "</label></span>";

                var ruta = response[llave]['Orden'];
                var viajes = ruta.length - 1;
                html += "<div class='container-fluid col-md-8' id='ruta" + index + "'><h4>Ruta: " + ruta + "</h4>";
                for (var i = 0; i < viajes; i++) {
                    var transporte = response[llave][ruta[i]];
                    var nodo = ruta[i];
                    html += "<div id='nodo'><label>" + (i + 1) + ") " + nodo + "</label><br>";
                    if (transporte.hasOwnProperty('Bus')) {
                        html += "<label>Transporte: Bus</label><br><ul>";
                        for (var key in transporte['Bus']) {
                            if (key !== 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Bus'][key] + "</li>";
                            }
                        }
                        html += "</ul></div></div>"
                    } else if (transporte.hasOwnProperty('Taxi')) {
                        html += "<label>Transporte: Taxi</label><ul>";
                        for (var key in transporte['Taxi']) {
                            if (key !== 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Taxi'][key] + "</li>";
                            }

                            if (key === 'Conductor') {
                                html += "<ul>";
                                for (var value in transporte['Taxi']['Conductor']) {
                                    html += "<li>" + value + " : " + transporte['Taxi']['Conductor'][value] + "</li>";
                                }
                                html += "</ul>";
                            }

                        }
                        html += "</ul></div></div>";

                    } else if (transporte.hasOwnProperty('Tren')) {
                        html += "<label>Transporte: Tren</label><br><ul>";
                        for (var key in transporte['Tren']) {
                            if (key !== 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Tren'][key] + "</li>";
                            }

                            if (key === 'Horario') {
                                html += "<ul>";
                                for (var value in transporte['Tren']['Horario']) {
                                    html += "<li>" + value + " : " + transporte['Tren']['Horario'][value] + "</li>";
                                }
                                html += "</ul>";
                            }
                        }
                        html += "</ul></div></div>"
                    } else {
                        html += "<label>Transporte: Avion</label><br><ul>";
                        for (var key in transporte['Avion']) {
                            if (key !== 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Avion'][key] + "</li>";
                            }

                            if (key === 'Horario') {
                                html += "<ul>";
                                for (var value in transporte['Avion']['Horario']) {
                                    html += "<li>" + value + " : " + transporte['Avion']['Horario'][value] + "</li>";
                                }
                                html += "</ul>";
                            }
                        }
                        html += "</ul></div></div>"
                    }
                }
                index++;
            });
            var alternativas = $("#rutas-alternativas");
            alternativas.html(html);
            alternativas.css({"color": "red", "opacity": "0.3"});
            alternativas.animate({"color": "white", "opacity": "1", "fontSize": "2.2em", "padding": "100px"}, 2000);
        },
        error: function (response) {
            console.log(response);
            alert("Error: " + response['Mensaje'])
        }
    };

    $.ajax(settings).done(function (response) {
        console.log(response);
    });


}