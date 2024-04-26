


let myChart = null;
let revenueChart = null
function createOrUpdateChart(data,data1) {
    console.log("dataq",data1)
    const ctx = document.getElementById('myChart').getContext('2d');
    const ctx1 = document.getElementById('revenueChart').getContext('2d');
    if (myChart) {
        // Update chart data
        myChart.data = data;
        revenueChart.data = data1;
        myChart.update();
        revenueChart.update();
    } else {
        // Create new chart
        myChart = new Chart(ctx, {
            type: 'bar',
            data: data,
            
        });

        revenueChart = new Chart(ctx1, {
            type: 'line',
            data: data1,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}


$(document).ready(function() {
    // Make an initial AJAX request to get the data
    // You can customize this based on your application's requirements
    $.ajax({
        url:'get_monthly_order_data/',  // URL to your Django view
        type: 'GET',
        success: function(response) {
           


            console.log(response.label)
          console.log(response.varibles)
          var lab = response.label
          var dat = response.varibles
          var ldata = response.ldata
         
       const data = {
          labels: lab,
          datasets: [{
              label: 'Monthly Data',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
              data: dat,
          }]

            };
            const data1 = {
                labels: lab,
                datasets: [{
                    label: 'Monthly Revenue',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false,
                    data: ldata,
                }]
            };

            // Create or update the chart with initial data
            createOrUpdateChart(data,data1);
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', xhr.responseText);
        }
    });
});



document.getElementById('changing_chart_data').addEventListener('change', function() {
    var selectedOption = $(this).val();
    console.log(selectedOption)
    var name = ""
    if (selectedOption == "week"){
        name = "Weekly data"
    }
    else if (selectedOption == "month"){
        name = "Monthly Data"
    }
    else{
        name = "Yearly Data"
    }

    $.ajax({
        url: 'changeChartData',  // URL to your Django view
        type: 'GET',
        data: {
            'value': selectedOption,
        },
        success: function(response) {
            console.log("success")
            const labels = response.label;
            const dat = response.varibles;
            const ldata = response.ldata;

            const data = {
                labels: labels,
                datasets: [{
                    label: name,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    data: dat,
                }]
            };
            const data1 = {
                labels: labels,
                datasets: [{
                    label: name,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false,
                    data: ldata,
                }]
            };

            // Create or update the chart
            createOrUpdateChart(data,data1);
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', xhr.responseText);
        }
    });
});












// document.getElementById('changing_chart_data').addEventListener('change', function() {

//         var selectedOption = $(this).val();
//         console.log(selectedOption)

//         $.ajax({
//             url:'changeChartData',  // URL to your Django view
//             type: 'GET',
//             data: {
//                 'value':selectedOption,
//             },
//             success: function(response) {
//                 console.log("thishs",response)

//                 const labels = [];
//                 const salesData = [];
        
//                 // Extract labels and sales data from each entry in the response array
      
//                 console.log(response.label)
//                 console.log(response.varibles)
//                 var lab = response.label
//                 var dat = response.varibles
//                 var ldata = response.ldata
               
//              const data = {
//                 labels: lab,
//                 datasets: [{
//                     label: 'Monthly Data',
//                     backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                     borderColor: 'rgba(75, 192, 192, 1)',
//                     borderWidth: 1,
//                     data: dat,
//                 }]
//             }; 

       
//             // Create a bar chart
//             const ctx19 = document.getElementById('myChart').getContext('2d');
//             console.log(myChart)
//             if (myChart) {
//                 console.log("Chart exists, destroying...");
//                 myChart.destroy();
//             } else {
//                 console.log("Chart does not exist.");
//             }
       
            
//          //   Create a new chart
//                 myChart = new Chart(ctx19, {
//                 type: 'bar',
//                 data: data,
//             });
      

//             }
//         });
//     });
