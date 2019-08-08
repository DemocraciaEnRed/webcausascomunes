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
        if (dtHeadersArr[i].name == 'Importe')
            dtHeadersArr[i]['render'] = function(data, type, row, meta){
                if(type === 'display'){
                    data = floatToStr(data);
                }
                return data;
            }
    }

    console.log(dtHeadersArr)

    dtApi = $('#data-csv').DataTable({
        // cargamos nombres de columnas
        "columns": dtHeadersArr,
        columnDefs: [
            {
                // mala práctica, hardié el num de la columna importe
                targets: 1,
                className: 'dt-body-right'
            }
        ],

        // cargamos textos en español para los botones y demás
        "language": {
            "url": _datatable_spa_json_url
        },

        // habilitamos es scroll horizontal
        "scrollX": true,

        // que arranque ordenado por fecha, los más recientes primero
        "order": [[ 0, 'desc' ]],

        // que arranque mostrando de a 25 registros
        "pageLength": 25,

        // esta función se ejecuta al terminar de cargar/renderear la DataTable
        "initComplete": function(settings, json) {
            // fix bug de que se pisan los textos del paginador con el msj de 'mostrando X registros...'
            $('#data-csv_info').parent().removeClass('col-md-5').addClass('col-xl-5')
            $('#data-csv_paginate').parent().removeClass('col-md-7').addClass('col-xl-7')
        }
    });

    createGraficoCatesImportes()
    createGraficoConcepsImportes()
    createGraficoGastosTiempo()
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

function tooltipFloat2strCb(tooltipItem, data) {
    var label = data.labels[tooltipItem.index] || '';

    if (label) {
        label += ': ';
    }
    floatData = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
    label += floatToStr(floatData);
    return label;
}

function createGraficoCatesImportes(){
    cates = dtApi.column('Categoria:name').data()
    importes = dtApi.column('Importe:name').data()

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
    for (i=0; i<catesLabels.length; i++){
        if (catesLabels[i]=='LEGAL CONTABLE FINANCIERO ADMINISTRATIVO')
            catesLabels[i]='ADMINISTRATIVO'
        else if (catesLabels[i]=='COMISIONES BANCARIAS, IMPUESTOS')
            catesLabels[i]='COMISIONES BANCARIAS'
    }
    strArrToTitle(catesLabels)

    var chart = new Chart($('#chart-importe-categoria'), {
        type: 'doughnut',
        data: {
            datasets: [{
                label: 'Gastos por categoría',
                backgroundColor: bgCols,
                data: Object.values(catesImporte)
            }],
            labels: catesLabels
        },
        options: {
            legend: {position:'left'},
            tooltips: {
                callbacks: {
                    label: tooltipFloat2strCb
                }
            }
        }
    });
    return chart
}


function createGraficoConcepsImportes(){
    conceps = dtApi.column('Concepto:name').data()
    importes = dtApi.column('Importe:name').data()

    concepsImporte = {}
    bgCols = []
    for (i=0; i<conceps.length; i++){
        conItem=conceps[i].replace('&amp;','&').toLowerCase()
        impItem=parseFloat(importes[i])

        if (conItem.indexOf('honorarios profesionales') != -1)
            conItem = 'honorarios profesionales'

        if (conItem in concepsImporte)
            concepsImporte[conItem] += impItem
        else
            concepsImporte[conItem] = impItem

        bgCols.push(window.chartColors[Object.keys(window.chartColors)[(i+1)%Object.keys(window.chartColors).length]])
    }

    concepsImporte = sortedDict(concepsImporte)

    var chart = new Chart($('#chart-importe-concepto'), {
        type: 'doughnut',
        data: {
            datasets: [{
                label: 'Gastos por concepto',
                backgroundColor: bgCols,
                data: Object.values(concepsImporte)
            }],
            labels: strArrToTitle(Object.keys(concepsImporte))
        },
        options: {
            legend: {
                position:'left',
            },
            tooltips: {
                callbacks: {
                    label: tooltipFloat2strCb
                }
            }
        }
    });
    return chart
}


function createGraficoGastosTiempo(){
    fechas = dtApi.column('Fecha:name').data()
    importes = dtApi.column('Importe:name').data()

    fechasImporte = {}
    bgCols = []
    for (i=0; i<fechas.length; i++){
        fecItem=strToDate(fechas[i])
        impItem=parseFloat(importes[i])

        month=fecItem.getMonth()

        if (month in fechasImporte)
            fechasImporte[month] += impItem
        else
            fechasImporte[month] = impItem

        bgCols.push(window.chartColors[Object.keys(window.chartColors)[i%Object.keys(window.chartColors).length]])
    }

    monthNums = Object.keys(fechasImporte)
    monthNames = []
    for (i in monthNums){
        monthDate=new Date(1, monthNums[i], 1)
        monthNames.push(monthDate.toLocaleString('es', { month: 'long' }))
    }

    var ctx = document.getElementById('chart-bars-gastos').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                label: 'Egresos',
                backgroundColor: bgCols,
                data: Object.values(fechasImporte)
            }],
            labels: monthNames
        },
        options: {
            legend: {display: false},
            tooltips: {
                callbacks: {
                    label: tooltipFloat2strCb
                }
            }
        }
    });
    return chart
}