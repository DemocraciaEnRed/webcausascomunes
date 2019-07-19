var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45]
        }]
    },

    // Configuration options go here
    options: {}
});

$(document).ready(function() {
    $('#example').DataTable({
        "language": {
            "url": _datatable_spa_json_url
        }
    });
} );

/*setInterval(function(){
chart.data.datasets[0].backgroundColor="#"+((1<<24)*Math.random()|0).toString(16);
chart.data.datasets[0].borderColor="#"+((1<<24)*Math.random()|0).toString(16);
    data = chart.data.datasets[0].data;
    for (d in data)
        data[d] = Math.random()*40;
   chart.update();
}, 200)*/