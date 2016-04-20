/* ======================================================================
DESC: javascript common to all state HTML files in the NAWRS site.

PLATFORMS: all client side systems using browsers which accept Javascript 1.3
====================================================================== */

MaxIndex = 30;
StatusBarLocked = 0;
var countyCode = -1;

function DisplaySites(string)   {
  console.log("DisplaySites function");
  var i, index;
  var zoneString, zoneNbr, preString, postString, totalString, editString;
  
  
  zoneString = string.substring(3, 6);
  editString = string.substring(0, 6);
  i = parseInt(zoneString);
  if (isNaN(i))  {  // is this an alpha zone?
    postString = zoneString.substring(2, 3);  // yes
    zoneString = '09' + postString;  // substitue numeric index
    preString = editString.substring(0, 3);
    editString = preString + '00' + postString;
  }
  
  index = zoneString.indexOf('00');
  if (index != 0)  {  // is this 2 leading zeroes?
    index = zoneString.indexOf('0');  // no
    if (index != 0)  // is this a single leading zero?
      index = -1;  // no, use entire zoneString
  }
  else index = 1;  // yes, we have 2 leading zeroes
  
  if (index > -1) {
    postString = zoneString.substring(++index);
    preString = ' ';
    
    if (index == 2)
      preString = '  ';
    
    zoneString = preString + postString;
  }

  zoneNbr = parseInt(zoneString);
  
  if (DisplaySites.arguments.length == 1)  // do we have only one argument?
    totalString = zoneString + ' ' + ZoneName[zoneNbr] + ':' + string;  // yes
  else {   // no, two arguments
    param2 = DisplaySites.arguments[1];   // fetch 2nd argument
    //countyCode=param2;
    zoneString = param2.substring(3, 6);
    index = zoneString.indexOf('00');
    if (index != 0)  {  // is this 2 leading zeroes?
      index = zoneString.indexOf('0');  // no
      if (index != 0)  // is this a single leading zero?
          index = -1;  // no, use entire zoneString
    }
    
    else index = 1;  // yes, we have 2 leading zeroes
    
    if (index > -1) {
      postString = zoneString.substring(++index);
      preString = ' ';
      
      if (index == 2) 
        preString = '  ';
      
      zoneString = preString + postString;
      totalString = zoneString + ' ' + ZoneName[zoneNbr] + ':' + param2;
    }
  }
  
  console.log("totalString: "+totalString);
  countyCode=totalString.substring(totalString.indexOf(":")+1);
  localStorage.setItem("countyCodeCookie", countyCode);
  console.log("Inside Displaysites countyCode: " + countyCode);
  // $('#countyCodeHidden').text(countyCode);
  // $('#countyCodeHidden').val(countyCode);
  // var par =document.getElementById('countyCodeHidden');
  // par.innerHTML = countyCode
  var temp = $('#countyCode').val();
  console.log("get text from html: " + temp);
        
}
      
   
// Handle drop-down box for zone strings
function DisplayStrings(flag)  {
  console.log("DisplayStrings : " + flag); 
  var zoneString, param1, param2, comma;
  if (flag == 1)
     zoneString = document.DropDown1.Zones.options[document.DropDown1.Zones.selectedIndex].value;
  else
    zoneString = document.DropDown2.Cities.options[document.DropDown2.Cities.selectedIndex].value;

  if (zoneString.indexOf("999") == -1)  {
    if (flag == 1)
      document.DropDown1.Zones.options.selectedIndex = 0;
    else
      document.DropDown2.Cities.options.selectedIndex = 0;
    
    comma = zoneString.indexOf(",");

    if (comma == -1)
      DisplaySites(zoneString);
    else {
      param1 = zoneString.substring(0, comma);
      param2 = zoneString.substr(++comma, zoneString.length - comma);
      DisplaySites(param1, param2);
    }
  }
}

//window.addEventListener('load', function() {
//$( window ).load(function() {  
$(document).ready(function() {
        $('.state').click(function (event) { 
          event.preventDefault(); 
          var url = $(this).attr('href');
          var ID=document.getElementById('state_pic');
          ID.src = url;
          ID.style.visibility='visible';
          newheight = 600;//ID.contentWindow.document.body.scrollHeight;
          newwidth = 600;//ID.contentWindow.document.body.scrollWidth;
          ID.height = (newheight) + "px";
          ID.width = (newwidth) + "px";
          //console.log(url);
          // $.get(url, function(data) {
          //     alert(data);
          // });
        });

        var submitButton = $('#submitButtonID2')[0];
        //console.log(countyCode);
        submitButton.addEventListener('click', sendQuery, false);


      function sendQuery() {
            //console.log("cCode: " + cCode);
            console.log("Inside Send Query");
            // get the parameters for query
            
            var warningType = "frost";
            console.log("warningType: " + warningType);

            //console.log("Inside sendQuery countyCode: " + countyCode);
            
            //In YYYY-MM-DD format
            var startDate = $('#begin_date').val();
            console.log("startDate: " + startDate);
            var endDate = $('#end_date').val();
            console.log("endDate: " + endDate);
            console.log("countyCode: " + $('#countyCode').val());
            
            var cookieValue = localStorage.getItem("countyCodeCookie");
            console.log("cookieValue: " + cookieValue);
            if (warningType!== "" && $('#countyCode').val()!=="" && startDate!=="" && endDate!==""){
              console.log("We got a valid user input");
              // create a request object
              var request = new XMLHttpRequest();
              // specify the HTTP method, URL, and asynchronous flag
              request.open('GET', '/findWarning/' + warningType + '/' + cookieValue + '/' + startDate + '/' + endDate, true); //$('#countyCode').val()
              request.addEventListener('load', function(e){
              
                // inside your Ajax response handler
                if (request.status == 200){
                  var content = request.responseText;
                  var data = JSON.parse(content);

                  // we have a list of Query results by different dates
                  console.log("length of content: " + data.length);
                  //console.log("data: " + data);

                  for (i = 0; i < data.length; i++) {
                    var date = data[i].date;
                    var warning = data[i].warning;
                    var text = data[i].text;
                    console.log("date: "+date);
                    console.log("warning: "+warning);
                    console.log("text: " + text);
                  }
                } else {
                  console.log('Something went wrong, check the request status');
                }
              });
              
              request.send(null);
            }
      }


   
});




















