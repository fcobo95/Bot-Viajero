function rutas() {
    var origen = $("#Origen").val();
    var destino = $("#Destino").val();
    var prioridad = $("#Prioridad").val();
    event.preventDefault();

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://127.0.0.1:5000/api/get-route",
        "method": "POST",
        "headers": {
            "authorization": "Basic " + btoa(localStorage.getItem("Token")),
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
            var rutas = $("#detalles-ruta");
            rutas.html(html);
            rutas.css({"color": "red", "opacity": "0.3"});
            rutas.animate({"color": "grey", "opacity": "1", "fontSize": "2.5em", "padding": "100px"}, 3000);
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
    localStorage.removeItem("Token")
    window.location.href = 'login.html'
}