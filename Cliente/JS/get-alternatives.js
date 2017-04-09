function alternativas() {
    var origen = $("#Origen").val();
    var destino = $("#Destino").val();
    var prioridad = $("#Prioridad").val();
    var ip = "192.168.1.27";
    var port = "5000";
    event.preventDefault();

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://" + ip + ":" + port + "/api/get-alternatives",
        "method": "POST",
        "headers": {
            "authorization": "Basic " + btoa(sessionStorage.getItem("Token")),
            "content-type": "application/json"
        },
        "processData": false,
        "data": JSON.stringify({Origen: origen, Destino: destino, Prioridad: prioridad}),
        success: function (response) {
            var html = "";
            var index = 1;
            $.each(response, function (llave, valor) {
                var ruta = response[llave]['Orden'];
                var viajes = ruta.length - 1;
                html += "<div class='container-fluid' id='contenedor" + index + "'>";
                html += "<div>";
                html += "<h2>Alternativa #" + index + "</h2>";
                html += "</div>";
                html += "<div id='ruta-nodo-alternatives'>";
                html += "<h2>Ruta: " + ruta + "</h2>";
                html += "</div>";
                for (var i = 0; i < viajes; i++) {
                    var transporte = response[llave][ruta[i]];
                    var nodo = ruta[i];
                    html += "<div id='nodo'" + index + "  class='row'>";
                    html += "<div id='titulo-nodo'>";
                    html += "<label>" + (i + 1) + ') ' + nodo + "</label>";
                    html += "</div>";
                    if (transporte.hasOwnProperty('Bus')) {
                        html += "<div id='transporte-nodo' class='col'>";
                        html += "<label>Transporte: Bus</label>";
                        html += "</div>";
                        html += "<div id='lista-nodo' class='col'>";
                        html += "<ul>";
                        for (var key in transporte['Bus']) {
                            if (key !== 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Bus'][key] + "</li>";
                            }
                        }
                        html += "</ul>";
                        html += "</div>";
                        html += "</div>";
                        html += "</div>";
                    } else if (transporte.hasOwnProperty('Taxi')) {
                        html += "<div id='transporte-nodo' class='col'>";
                        html += "<label>Transporte: Taxi</label>";
                        html += "</div>";
                        html += "<div id='lista-nodo' class='col'>";
                        html += "<ul>";
                        for (var key in transporte['Taxi']) {
                            if (key !== 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Taxi'][key] + "</li>";
                            }

                            if (key === 'Conductor') {
                                html += "<ul>";
                                for (var value in transporte['Taxi']['Conductor']) {
                                    html += "<li>" + value + " : " + transporte['Taxi']['Conductor'][value] + "</li>";
                                }
                            }

                        }
                        html += "</ul>";
                        html += "</div>";
                        html += "</div>";
                        html += "</div>";

                    } else if (transporte.hasOwnProperty('Tren')) {
                        html += "<div id='transporte-nodo' class='col'>";
                        html += "<label>Transporte: Tren</label>";
                        html += "</div>";
                        html += "<div id='lista-nodo' class='col'>";
                        html += "<ul>";
                        for (var key in transporte['Tren']) {
                            if (key !== 'Ruta') {
                                html += "<li>" + key + " : " + transporte['Tren'][key] + "</li>";
                            }

                            if (key === 'Horario') {
                                html += "<ul>";
                                for (var value in transporte['Tren']['Horario']) {
                                    html += "<li>" + value + " : " + transporte['Tren']['Horario'][value] + "</li>";
                                }
                                html += "</ul>"
                            }
                        }
                        html += "</ul>";
                        html += "</div>";
                        html += "</div>";
                        html += "</div>";
                    } else {
                        html += "<div id='transporte-nodo' class='col'>";
                        html += "<label>Transporte: Avion</label>";
                        html += "</div>";
                        html += "<div id='lista-nodo' class='col'>";
                        html += "<ul>";
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
                        html += "</ul>";
                        html += "</div>";
                        html += "</div>";
                        html += "</div>";
                    }
                }
                index++;
            });

            var alternativas = $("#rutas-alternativas");
            alternativas.html(html);
            alternativas.css({"color": "red", "opacity": "0.3"});
            alternativas.animate({"color": "grey", "opacity": "1", "fontSize": "1.5em", "padding": "50px"}, 3000);

            var rutas_nodo = $("#ruta-nodo-alternatives");
            rutas_nodo.children().css("color", "green")
        },
        error: function (response) {
            console.log(response);
            alert("Error: " + response['Mensaje'])
        }
    };
    alert("Evaluando posibilidades. Por favor espere un momento.");
    $.ajax(settings).done(function (response) {
        console.log(response);
    });


}