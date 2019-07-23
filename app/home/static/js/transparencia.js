
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
        "order": [[ 0, 'desc' ]]
    });
    createGraficoCatesImportes()
    createGraficoGastosTiempo()
} );


function createGraficoCatesImportes(){
    cates = dtApi.column(2).data()
    importes = dtApi.column(1).data()

    catesImporte = {}
    bgCols = []
    for (i=0; i<cates.length; i++){
        catItem=cates[i].toLowerCase()
        impItem=parseFloat(importes[i])

        if (catItem.indexOf('honorarios profesionales') != -1)
            catItem = 'honorarios profesionales'

        if (catItem in catesImporte)
            catesImporte[catItem] += impItem
        else
            catesImporte[catItem] = impItem

        bgCols.push(window.chartColors[Object.keys(window.chartColors)[i%Object.keys(window.chartColors).length]])
    }

    var ctx = document.getElementById('chart-importe-categoria').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                label: 'My First dataset',
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


function createGraficoGastosTiempo(){
    cates = dtApi.column(2).data()
    importes = dtApi.column(1).data()

    catesImporte = {}
    bgCols = []
    for (i=0; i<cates.length; i++){
        catItem=cates[i].toLowerCase()
        impItem=parseFloat(importes[i])

        if (catItem.indexOf('honorarios profesionales') != -1)
            catItem = 'honorarios profesionales'

        if (catItem in catesImporte)
            catesImporte[catItem] += impItem
        else
            catesImporte[catItem] = impItem

        bgCols.push(window.chartColors[Object.keys(window.chartColors)[i%Object.keys(window.chartColors).length]])
    }

    var ctx = document.getElementById('chart-bars-gastos').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                label: 'My First dataset',
                backgroundColor: bgCols,
                data: Object.values(catesImporte)
            }],
            labels: Object.keys(catesImporte)
        },
        options: {
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
    return chart
}