// =====================================. query selector =================================

header = document.querySelector("#heading");
start = document.querySelector("#start");
pie = document.querySelector("#pie");
result = document.querySelector("#result");


//=================================== Variables ==========================================

var map, heatmap,mvc , mcvR;
var numDeltas = 10;
var delay = 10; //milliseconds
var i =0;
var data;
var count1 = 0 ,count2 = 0;
var heatmap, heatmap1;
var executed = false;

//   ============================= Color Changing Function =====================
function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}


function setColor()
{
	header.style.color = getRandomColor();
	result.style.color = getRandomColor();
  

}


setInterval(setColor,500);


// ===============================Map Event Listerner=============================================

start.addEventListener('click',initMap);


// ====================== Map Fuction ============================================================
    
    function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: {lat: 18.775, lng: -90.434},
          mapTypeId: 'satellite'
        });
          


        mvc = new google.maps.MVCArray(); //=======================================infected============
        mvcR = new google.maps.MVCArray(); //======================================recovery =================

        console.log(points.length);
        
           // ================== Infection heatmap =============================
        heatmap = new google.maps.visualization.HeatmapLayer({
                    data: mvc,
                     map: map,
                     radius : 10

                    });


        // ================== Recovery heatmap ================================

        heatmap1 = new google.maps.visualization.HeatmapLayer({
                    data: mvcR,
                     map: map,
                     radius : 5,
                    });

        move();

                
       }

       //=======================================Heatmap Plotting move function ===========================

       function move()
        {

                  for(var k = i;k< i+50 && k < points.length;k++)
                  {
                        var cur = new google.maps.LatLng(points[k]['lat'],points[k]['lng'])     
                    
                         mvc.push(cur);

                   }
                         
                         i = k;
                         if (i< points.length)
                         {
		                         if(i > points.length/3)
		                         {
		                         	 somthing();
		                         	
							               }
                             // else
                             // {



                             // }                        	

		                        
                            count1 = i;
                            setTimeout(move,0); 
                         
                         }
       }

  // =================================================== Map Function End ==================================

  // ============================================== Pie Chart Function ================================


	pie.addEventListener('click',function()
		{
				google.charts.setOnLoadCallback(drawChart);	
		});
 
      google.charts.load('current', {'packages':['corechart']});

       function drawChart() {



      var data = google.visualization.arrayToDataTable([
          ['No of people', 'Hours per Day'],        
          ['Saved', count2],
          ['Infected',     count1],

          ['Total',points.length]
          
        ]);

        var options = {
          title: 'Infection Activity'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));


        chart.draw(data, options);
        data.setValue(0, 1,count1);
        data.setValue(1, 1,count2);
        setInterval(drawChart,5000)
      }


// ============================= Date worker ==============================

//    worker.onmessage = function (event) {
//      document.getElementById('result').textContent = event.data;
//    };// var worker = new Worker('worker1.js');
//



// ==================================== Color changing of  recovery map =========================================


function changeGradient() {
        var gradient = [
          'rgba(0, 0, 0, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(0, 0, 0, 1)'
        ]
       
          heatmap1.set('gradient', heatmap1.get('gradient') ? null : gradient);

      }


// ============================================== Background Process Implementation of Recovery Map ===============================
   

   function somthing() {

          console.log("rahuk");

   	
   		    if (!executed) {
            executed = true;
            var worker = new Worker("workerS.js");
            worker.postMessage(points.length);
            
            changeGradient();

	        worker.onmessage = function (event) {
	        		count2 = event.data;
	        	  var cur = new google.maps.LatLng(points[event.data]['lat'],points[event.data]['lng']) ;    
                    
                  mvcR.push(cur);
                            
        };
      }
}


            



               
                  

         
