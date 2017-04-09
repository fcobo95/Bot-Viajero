function rutas() {
    var origen = $("#Origen").val();
    var destino = $("#Destino").val();
    var prioridad = $("#Prioridad").val();
    event.preventDefault();
    var ip = "192.168.1.27";
    var local = "127.0.0.1";
    var port = "5000";
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://" + local + ":" + port + "/api/get-route",
        "method": "POST",
        "headers": {
            "authorization": "Basic " + btoa(sessionStorage.getItem("Token")),
            "content-type": "application/json"
        },
        "processData": false,
        "data": JSON.stringify({Origen: origen, Destino: destino, Prioridad: prioridad}),
        success: function (response) {
            var index = 0;

            var ruta = response['Orden'];
            var viajes = ruta.length - 1;
            var html = "<div class='container-fluid' id='contenedor'>";
            html += "<div id='ruta-nodo'>";
            html += "<h2>Ruta: " + ruta + "</h2>";
            html += "</div>";
            for (var i = 0; i < viajes; i++) {
                var transporte = response[ruta[i]];
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
            var rutas = $("#detalles-ruta");
            rutas.html(html);
            rutas.css({"color": "red", "opacity": "0.3"});
            rutas.animate({"color": "grey", "opacity": "1", "fontSize": "1.5em", "padding": "50px"}, 3000);

            var ruta_nodo = $("#ruta-nodo");
            ruta_nodo.children().css(
                {
                    "color": "green"
                }
            );
        },
        error: function (response) {
            console.log(response);
            alert("Error: " + response['Mensaje'])
        }
    };

    $.ajax(settings).done(function (response) {
        console.log(response)
    });
}

function logout() {
    sessionStorage.clear();
    window.location.href = 'login.html'
}