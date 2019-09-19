window.chartColors = {
    blue: "rgb(54, 162, 235)",
    green: "rgb(75, 192, 192)",
    orange: "rgb(255, 159, 64)",
    purple: "rgb(153, 102, 255)",
    red: "rgb(255, 99, 132)",
    grey: "rgb(201, 203, 207)",
    yellow: "rgb(255, 205, 86)"
}

dtApi = null

$(document).ready(function() {
    dtHeadersArr = []
    // cargamos headers del server
    for (i in _datatable_headers)
        dtHeadersArr.push( { 'name': _datatable_headers[i] } )

    // setteamos renderer de la columna 'original' para que genere anchors de sus urls
    for (i in dtHeadersArr){
        /*if (dtHeadersArr[i].name == 'Original')
            dtHeadersArr[i]['render'] = function(data, type, row, meta){
                if(type === 'display' && data && data != 'N/A'){
                    data = '<a href="' + data + '" target="_blank">' + data + '</a>';
                }
                return data;
            }*/
        if (dtHeadersArr[i].name == 'Tiempo')
            dtHeadersArr[i]['render'] = function(data, type, row, meta){
                if(type === 'display' && data){
					if (data=="1")
                    	data += " hora";
					else
                    	data += " horas";
                }
                return data;
            }
    }

    console.log(dtHeadersArr)

    dtApi = $('#data-csv').DataTable({
        // cargamos nombres de columnas
        "columns": dtHeadersArr,

        // cargamos textos en español para los botones y demás
        "language": {
            "url": _datatable_spa_json_url
        },

        // que arranque ordenado por fecha, los más recientes primero
        "order": [[ 0, 'desc' ]],

        // habilitamos es scroll horizontal
        "scrollX": true,

        // esta función se ejecuta al terminar de cargar/renderear la DataTable
        "initComplete": function(settings, json) {
            // fix bug de que se pisan los textos del paginador con el msj de 'mostrando X registros...'
            $('#data-csv_info').parent().removeClass('col-md-5').addClass('col-xl-5')
            $('#data-csv_paginate').parent().removeClass('col-md-7').addClass('col-xl-7')
        }
    });

    createGraficoDestinoTiempos()
    createGraficoMesesTiempo()
} );


function strToDate(s){
    var parts = s.split('/');
    return new Date(parts[2], parts[1] - 1, parts[0]);
}

function roundFloat(f, nDecimals){
    pw10 = Math.pow(10, nDecimals);
    return Math.round(f * pw10) / pw10
}

_decimalChar = ','
function floatToStr(f){
    fStr = (roundFloat(parseFloat(f), 2)).toLocaleString('es')

    decI = fStr.indexOf(_decimalChar)
    if (decI == -1)
        fStr += _decimalChar + '00'
    else if (decI == fStr.length - 2)
        fStr += '0'

    return fStr;
}

function sortedDict(dict){
    var items = Object.keys(dict).map(function(key) {
      return [key, dict[key]];
    });

    // Sort the array based on the second element
    items.sort(function(first, second) {
      return second[1] - first[1];
    });

    retDict={}
    for (i in items)
        retDict[items[i][0]] = items[i][1]
    return retDict;
}

function roundDictVals(dict){
    for (k in dict){
        if (typeof(dict[k]) === 'number')
            dict[k] = roundFloat(dict[k], 2)
    }
    return dict
}

function strArrToTitle(arr){
    for (i=0; i<arr.length; i++){
        allLower = arr[i].toLowerCase();
        arr[i] = allLower[0].toUpperCase() + allLower.slice(1);
    }
    return arr;
}

function tooltipInt2Horas(tooltipItem, data) {
    horas = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
    var horasString;
	if (horas == '1')
		horasString = horas + ' hora';
	else
		horasString = horas + ' horas';
    return horasString;
}

function createGraficoDestinoTiempos(){
	//me da fiaca cambiar los nombres de las variables =)
    cates = dtApi.column('Destino:name').data()
    importes = dtApi.column('Tiempo:name').data()

    catesImporte = {}
    bgCols = []
    for (i=0; i<cates.length; i++){
        catItem=cates[i].replace('&amp;','&')
        impItem=parseFloat(importes[i])

        if (catItem in catesImporte)
            catesImporte[catItem] += impItem
        else
            catesImporte[catItem] = impItem

        bgCols.push(window.chartColors[Object.keys(window.chartColors)[i%Object.keys(window.chartColors).length]])
    }

    catesImporte = sortedDict(catesImporte)
    catesLabels = Object.keys(catesImporte)

    var chart = new Chart($('#chart-tiempos-destino'), {
        type: 'doughnut',
        data: {
            datasets: [{
                label: 'Tiempos por destino',
                backgroundColor: bgCols,
                data: Object.values(catesImporte)
            }],
            labels: catesLabels
        },
        options: {
            legend: {position:'left'},
            tooltips: {
                callbacks: {
                    label: tooltipInt2Horas
                }
            }
        }
    });
    return chart
}



function createGraficoMesesTiempo(){
	//me da fiaca cambiar los nombres de las variables =)
    fechas = dtApi.column('Fecha:name').data()
    importes = dtApi.column('Tiempo:name').data()

    fechasImporte = {}
    bgCols = []
    for (i=0; i<fechas.length; i++){
        fecItem=fechas[i]
        impItem=parseInt(importes[i])
		console.log(fecItem)
        if (fecItem in fechasImporte)
            fechasImporte[fecItem] += impItem
        else
            fechasImporte[fecItem] = impItem
    		bgCols.push(window.chartColors[Object.keys(window.chartColors)[(i+3)%Object.keys(window.chartColors).length]])
    }
	console.log(Object.values(fechasImporte), Object.keys(fechasImporte))

    var ctx = document.getElementById('chart-bars-tiempos').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                label: 'Tiempos',
                backgroundColor: bgCols,
                data: Object.values(fechasImporte)
            }],
            labels: Object.keys(fechasImporte)
        },
        options: {
            legend: {display: false},
			
			// que arranque en zero el Y-axis y no en el menor valor
		    scales: {
		        yAxes: [{
		            ticks: {
		                beginAtZero: true
		            }
		        }]
		    },

            tooltips: {
                callbacks: {
                    label: tooltipInt2Horas
                }
            }
        }
    });
    return chart
}