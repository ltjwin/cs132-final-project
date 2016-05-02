window.addEventListener('load', function(){
    
  
    var submitButton = $('submitButtonID')[0];
    submitButton.addEventListener('submit', sendQuery, false);
     


    function sendQuery(e) {
        // prevent the page from redirecting
        e.preventDefault();
        
        // get the parameters for query
        var warningType = $('#warningTypeID')[0].attr("value");
        var countyCode = $('#countyCodeID')[0].attr("value");

        //In MM/DD/YYYY format
        var startDate = $('#startDateID')[0].attr("value");
        var endDate = $('#endDateID')[0].attr("value");
 
        if (warningType!== "" && countyCode!=="" && startDate!=="" && endDate!==""){
            // create a request object
            var request = new XMLHttpRequest();

            // specify the HTTP method, URL, and asynchronous flag
            request.open('GET', '/findWarning/' + warningType + '/' + countyCode + '/' + startDate + '/' + endDate, true);

            request.addEventListener('load', function(e){
                // inside your Ajax response handler
                
                if (request.status == 200){
                    //alert("HELLO HERE");
                    var content = request.responseText;
                    //console.log("content: "+content);
                    
                    var data = JSON.parse(content);
                    
                    // we have a list of Query results by different dates
                    
                    //var ul = document.getElementById('messages');

                    //display on page
                    for (i = 0; i < data.length; i++) {
                        var date = data[i].date;
                        var warning = data[i].warning;
                        var text = date[i].text;
                    }

                }else{
                    console.log('Something went wrong, check the request status');
                }
          
            });
            request.send(null);
        }
    }
}, false);


