
//<canvas id="chart-importe-categoria"></canvas>
//<canvas id="chart-bars-gastos"></canvas>

/*var ctx = document.getElementById('chart-importe-categoria').getContext('2d');
var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45]
        }]
    },
    options: {
        animation: {
            animateScale: true,
            animateRotate: true
        }
    }
});*/
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
    dtApi = $('#data-csv').DataTable({
        "language": {
            "url": _datatable_spa_json_url
        },
        "scrollX": true,
        "order": [[ 0, 'desc' ]],
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
            dict[k] = Math.round(dict[k] * 100) / 100
    }
    return dict
}

function createGraficoCatesImportes(){
    cates = dtApi.column(2).data()
    importes = dtApi.column(1).data()

    catesImporte = {}
    bgCols = []
    for (i=0; i<cates.length; i++){
        catItem=cates[i].toLowerCase().replace('&amp;','&')
        impItem=parseFloat(importes[i])

        if (catItem in catesImporte)
            catesImporte[catItem] += impItem
        else
            catesImporte[catItem] = impItem

        bgCols.push(window.chartColors[Object.keys(window.chartColors)[i%Object.keys(window.chartColors).length]])
    }

    catesImporte = sortedDict(roundDictVals(catesImporte))

    var chart = new Chart($('#chart-importe-categoria'), {
        type: 'doughnut',
        data: {
            datasets: [{
                label: 'Gastos por categoría',
                backgroundColor: bgCols,
                data: Object.values(catesImporte)
            }],
            labels: Object.keys(catesImporte)
        },
        options: {
            legend: {position:'left'}
        }
    });
    return chart
}


function createGraficoConcepsImportes(){
    conceps = dtApi.column(3).data()
    importes = dtApi.column(1).data()

    concepsImporte = {}
    bgCols = []
    for (i=0; i<conceps.length; i++){
        conItem=conceps[i].toLowerCase().replace('&amp;','&')
        impItem=parseFloat(importes[i])

        if (conItem.indexOf('honorarios profesionales') != -1)
            conItem = 'honorarios profesionales'

        if (conItem in concepsImporte)
            concepsImporte[conItem] += impItem
        else
            concepsImporte[conItem] = impItem

        bgCols.push(window.chartColors[Object.keys(window.chartColors)[(i+1)%Object.keys(window.chartColors).length]])
    }

    concepsImporte = sortedDict(roundDictVals(concepsImporte))

    var chart = new Chart($('#chart-importe-concepto'), {
        type: 'doughnut',
        data: {
            datasets: [{
                label: 'Gastos por concepto',
                backgroundColor: bgCols,
                data: Object.values(concepsImporte)
            }],
            labels: Object.keys(concepsImporte)
        },
        options: {
            legend: {
                position:'left',
            }
        }
    });
    return chart
}


function createGraficoGastosTiempo(){
    fechas = dtApi.column(0).data()
    importes = dtApi.column(1).data()

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

    roundDictVals(fechasImporte)

    monthNums = Object.keys(fechasImporte)
    console.log(monthNums)
    monthNames = []
    for (i in monthNums){
        monthDate=new Date(1, monthNums[i], 1)
        monthNames.push(monthDate.toLocaleString('es', { month: 'long' }))
    }
    console.log(monthNames)

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
            legend: {display: false}
        }
    });
    return chart
}