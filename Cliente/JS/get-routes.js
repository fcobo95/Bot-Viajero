function rutas() {
    /* *******************************************************************
     *
     * HACEMOS TARGET A LOS BOTONES DEL HTML DE ROUTES, PARA ASI
     * PODER BRINDARLES CIERTAS BONDADES, APLICANDO EN ALGUNOS CASOS
     * CLASES COMO BTN Y BTN-PRIMARY O .BUTTON() O .SELECT(), EN EL CASO
     * DE LOS DROPDOWN MENUS DE ORIGEN Y DESTINO. TAMBIEN, ESTAMOS DECLARANDO
     * CIERTOS ATRIBUTOS QUE VAN A SER UTILIZADOS PARA ARMAR LOS SETTINGS DEL
     * CLIENTE PARA PODER HACER LOS PEDIDOS AJAX Y CORS.
     *
     * ****************************************************************** */
    var origen = $("#Origen").val();
    var destino = $("#Destino").val();
    var prioridad = $("#Prioridad").val();
    var ip = "192.168.1.27";
    var local = "127.0.0.1";
    var port = "5000";
    event.preventDefault();

    /* ******************************************************************
     *
     * AQUI CREAMOS LOS HEADERS QUE VAMOS A ENVIAR POR MEDIO DE AJAX
     * TAMBIEN, SETEAMOS CIERTOS ATRIBUTOS PARA PODER HACER PEDIDOS
     * ASINCRONOS, CROSSDOMAIN, Y PARA QUE EL SERVIDOR NOS DEVUELVA
     * UN POST CON LOS DATOS SOLICITADOS A LA RUTA QUE SE ESPECIFICA
     * EN EL URL. TAMBIEN, CABE MENCIONAR QUE LO QUE VA A RECIBIR EL
     * CLIENTE ES UNA RESPUESTA JSON, LOS CUALES SON FORMATEADOS CON
     * LA LOGICA QUE SE ENCUENTRA EN ESTE ARCHIVO.
     *
     * TAMBIEN, TENEMOS LA AUTENTICACION POR MEDIO DE TOKEN, LA CUAL
     * SE GUARDA EN EL LOCAL STORAGE DEL NAVEGADOR WEB.
     *
     * ****************************************************************** */
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
            /* ******************************************************************
             *
             * AQUI, CREAMOS LA ESTRUCTURA QUE VA A CONTENER LOS DATOS QUE VIENEN EN EL JSON
             * DE LA RESPUESTA DEL LLAMADO AJAX.
             *
             * SE CREA TODA LA ESTRUCUTRA DEL HTML. POR MEDIO DE CICLOS ACCEDEMOS LA INFORMACION
             * QUE VIENE EN EL JSON Y LA IMPRIMIMOS EN SUS RESPECTIVOS LUGARES. SE VERIFICA CADA
             * LLAVE Y EL VALOR QUE TIENE LA LLAVE, PARA ASI PODER IMPRIMIR LA LLAVE ADECUADA CON
             * SU VALOR CORRESPONDIENTE.
             *
             * ****************************************************************** */
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

            /* ******************************************************************
             *
             * AQUI, FORMATEAMOS POR MEDIO DE TARGETS EL CSS DE LOS ELEMENTOS QUE SE CREAN
             * EN LA FUNCION DE SUCCESS. ESTOS ELEMENTOS NO SE CREAN DIRECTAMENTE EN EL HTML
             * DE RUTAS, SINO QUE SE CREAN POR MEDIO DE REFERENCIAS Y MEMORIA. ESTA ESTRUCTURA
             * UNICAMENTE VIVE CUANDO SE CREA UN LLAMADO AJAX, YA QUE FISICAMENTE, NO SE ENCUENTRA
             * EN EL CODIGO HTML.
             *
             * ***************************************************************** */
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

    /* ******************************************************************
     *
     * SE CARGAN LOS SETTINGS ANTERIORES Y SE ENVIA EL REQUEST AJAX.
     *
     * ***************************************************************** */

    $.ajax(settings).done(function (response) {
        console.log(response)
    });
}

function logout() {
    sessionStorage.clear();
    window.location.href = 'login.html'
}