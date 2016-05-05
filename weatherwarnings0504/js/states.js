/* ======================================================================
DESC: javascript common to all state HTML files in the NAWRS site.
PLATFORMS: all client side systems using browsers which accept Javascript 1.3
====================================================================== */
MaxIndex = 30;
StatusBarLocked = 0;
var countyCode = -1;
var warningType;
var countyCodeVar;

function DisplaySites(string) {
    //console.log("DisplaySites function");
    var i, index;
    var zoneString, zoneNbr, preString, postString, totalString, editString;

    zoneString = string.substring(3, 6);
    editString = string.substring(0, 6);
    i = parseInt(zoneString);
    if (isNaN(i)) { // is this an alpha zone?
        postString = zoneString.substring(2, 3); // yes
        zoneString = '09' + postString; // substitue numeric index
        preString = editString.substring(0, 3);
        editString = preString + '00' + postString;
    }

    index = zoneString.indexOf('00');
    if (index != 0) { // is this 2 leading zeroes?
        index = zoneString.indexOf('0'); // no
        if (index != 0) // is this a single leading zero?
            index = -1; // no, use entire zoneString
    } else index = 1; // yes, we have 2 leading zeroes

    if (index > -1) {
        postString = zoneString.substring(++index);
        preString = ' ';

        if (index == 2)
            preString = '  ';

        zoneString = preString + postString;
    }

    zoneNbr = parseInt(zoneString);

    if (DisplaySites.arguments.length == 1) // do we have only one argument?
        totalString = zoneString + ' ' + ZoneName[zoneNbr] + ':' + string; // yes
    else { // no, two arguments
        param2 = DisplaySites.arguments[1]; // fetch 2nd argument
        //countyCode=param2;
        zoneString = param2.substring(3, 6);
        index = zoneString.indexOf('00');
        if (index != 0) { // is this 2 leading zeroes?
            index = zoneString.indexOf('0'); // no
            if (index != 0) // is this a single leading zero?
                index = -1; // no, use entire zoneString
        } else index = 1; // yes, we have 2 leading zeroes

        if (index > -1) {
            postString = zoneString.substring(++index);
            preString = ' ';

            if (index == 2)
                preString = '  ';

            zoneString = preString + postString;
            totalString = zoneString + ' ' + ZoneName[zoneNbr] + ':' + param2;
        }
    }
    //console.log("totalString: " + totalString);
    countyCode = totalString.substring(totalString.indexOf(":") + 1);
    localStorage.setItem("countyCodeCookie", countyCode);
    localStorage.setItem("zone", zoneString + ' ' + ZoneName[zoneNbr]);
    localStorage.setItem("displayTotal", 'Zone:' + zoneString + ' ' + ZoneName[zoneNbr]); //added this line
    //console.log("Inside Displaysites countyCode: " + countyCode);


    // Ensure that drop down list selects a value when zone map is clicked
    var stopIndex = totalString.indexOf(":");
    var startIndex = 0;
    while (totalString.substring(startIndex, startIndex + 1) == " ") {
        startIndex = startIndex + 1;
    }
    //console.log(totalString.substring(startIndex, stopIndex));
    var selectObj = document.DropDown1.Zones;
    for (var i = 0; i < selectObj.options.length; i++) {
        if (selectObj.options[i].text == totalString.substring(startIndex, stopIndex)) {
            selectObj.options[i].selected = true;
        }
    }
}


// Handle drop-down box for zone strings
function DisplayStrings(flag) {
    //console.log("DisplayStrings : " + flag);
    var zoneString, param1, param2, comma;
    if (flag == 1)
        zoneString = document.DropDown1.Zones.options[document.DropDown1.Zones.selectedIndex].value;
    
    if (zoneString.indexOf("999") == -1) {
        if (flag == 1)
            document.DropDown1.Zones.options.selectedIndex = document.DropDown1.Zones.selectedIndex;
    
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

var startdate, stopdate;
var startday, startmonth, startyear;
var currentyear;
var endday, endmonth, endyear;
var years;
var daycount = 0;

function initializeDates() {
    startdate = document.getElementById("begin_date").value;
    var start = startdate.split("-");
    startday = start[2];
    if (startday < 10) {
        startday = startday[1];
    }
    startmonth = start[1];
    if (startmonth < 10) {
        startmonth = startmonth[1];
    }
    startyear = start[0];

    //console.log("start day: " + startday + " start month: " + startmonth + " start year: " + startyear);
    currentyear = startyear;

    stopdate = document.getElementById("end_date").value;
    var end = stopdate.split("-");
    endday = end[2];
    if (endday < 10) {
        endday = endday[1];
    }
    endmonth = end[1];
    if (endmonth < 10) {
        endmonth = endmonth[1];
    }
    endyear = end[0];
    //console.log("end day: " + endday + " end month: " + endmonth + " end year: " + endyear);

    years = parseInt(endyear) - parseInt(startyear) + 1;
}

function monthToDays(month, year) {
    numDays = 0;
    if (month == 4 || month == 6 || month == 9 || month == 11) {
        numDays = 30;
    } else if (month == 2 && parseInt(year % 4) == 0) {
        numDays = 29;
    } else if (month == 2 && parseInt(year % 4) != 0) {
        numDays = 28;
    } else {
        numDays = 31;
    }

    return numDays;
}

function numberToMonth(monthnumber) {
    if (monthnumber === 1)
        return "January";
    if (monthnumber === 2)
        return "February";
    if (monthnumber === 3)
        return "March";
    if (monthnumber === 4)
        return "April";
    if (monthnumber === 5)
        return "May";
    if (monthnumber === 6)
        return "June";
    if (monthnumber === 7)
        return "July";
    if (monthnumber === 8)
        return "August";
    if (monthnumber === 9)
        return "September";
    if (monthnumber === 10)
        return "October";
    if (monthnumber === 11)
        return "November";
    if (monthnumber === 0)
        return "December";
}

function isValidDay(monthnumber, day) {
    if (monthnumber === 2 && parseInt(day) > 28) {
        if (parseInt(currentyear % 4) === 0 && day === 29) {
            return true;
        }
        return false;
    } else if (monthnumber === 4 && day === 31) {
        return false;
    } else if (monthnumber === 6 && day === 31) {
        return false;
    } else if (monthnumber === 9 && day === 31) {
        return false;
    } else if (monthnumber === 11 && day === 31) {
        return false;
    }
    return true;
}

function createTable(datearray) {
    var tablediv = document.getElementById('tableContainer');
    var mytable = document.createElement('table');

    mytable.setAttribute("align", "center");

    var j = 1;
    var finish = 12;
    var row = mytable.insertRow(0);

    for (i = 0; i < 32; i++) {
        var cell1 = row.insertCell(i);

        if (i === 0) {
            cell1.innerHTML = "Year " + currentyear;
        } else if (i < 10) {
            cell1.innerHTML = " 0" + parseInt(i) + " ";
        } else {
            cell1.innerHTML = " " + parseInt(i) + " ";
        }
    }

    var count = 1;
    if (currentyear === startyear) {
        j = startmonth;
    }

    if (parseInt(currentyear) === parseInt(endyear)) {
        finish = endmonth;
    }

    //console.log(finish);

    for (var k = j; parseInt(k) <= parseInt(finish); k++) {

        if (k < 4 || k > 10) {
            continue;
        }

        var row = mytable.insertRow(count);
        var month = parseInt(k % 12);
        count++;

        for (i = 0; i < 32; i++) {
            var cell1 = row.insertCell(i);

            if (i === 0) {
                cell1.innerHTML = "" + numberToMonth(month);
            } else if (isValidDay(month, parseInt(i)) == false) {
                cell1.style.backgroundColor = "white"; //changed from #A4A4A4A4
            } else if (parseInt(month) === parseInt(startmonth % 12) && parseInt(i) < parseInt(startday) && currentyear == startyear) {
                cell1.style.backgroundColor = "white"; //changed from #A4A4A4A4
            } else if (parseInt(month) === parseInt(endmonth % 12) && parseInt(i) > parseInt(endday) && currentyear == endyear) {
                cell1.style.backgroundColor = "white"; //changed from #A4A4A4A4
            } else if (parseInt(month) > 3 || parseInt(month) < 11) {
                if (parseInt(datearray[daycount]) == 1) {
                    cell1.style.backgroundColor = "#5EFB6E"; //changed from red color
                } else {
                    cell1.style.backgroundColor = "white" //"#1F45FC"; //changed from different blue color
                }

                daycount++;
            }
        }

        if (parseInt(month) == 10 && currentyear !== endyear) {
            tablediv.appendChild(mytable);
            var space = document.createElement('br');
            tablediv.appendChild(space);
            var anotherspace = document.createElement('br');
            tablediv.appendChild(anotherspace);
        }

    }

    if (parseInt(currentyear) === parseInt(endyear)) {
        tablediv.appendChild(mytable);
        var penulspace = document.createElement('br');
        tablediv.appendChild(penulspace);
        var finalspace = document.createElement('br');
        tablediv.appendChild(finalspace);
    }

    currentyear++;

}

var datearray, tableCreated = 0;

//window.addEventListener('load', function() {
//$( window ).load(function() {  
$(document).ready(function() {
    var csvArray;
    $('.state').click(function(event) {
        event.preventDefault();
        var url = $(this).attr('href');
        var ID = document.getElementById('state_pic');
        ID.src = url;
        ID.style.visibility = 'visible';
        newheight = 700; //ID.contentWindow.document.body.scrollHeight;
        newwidth = 600; //ID.contentWindow.document.body.scrollWidth;
        ID.height = (newheight) + "px";
        ID.width = (newwidth) + "px";
    });

    var submitButton = $('#submitButtonID2')[0];
    submitButton.addEventListener('click', sendQuery, false);


    function myFunction(text) {
        alert(text);
    }

    function sendQuery() {

        csvArray = [];

        $("#table2").find("tr:gt(0)").remove();
        
        // get the parameters for query
        warningType = "";
        
        if ($('#heat').is(':checked')) {
            warningType = "heat";
        }
        if ($('#wind').is(':checked')) {
            warningType = "wind";
        }
        if ($('#air_stagnation').is(':checked')) {
            warningType = "air";
        }
        

        if (tableCreated == 1) {
            var tableIdToRemove = document.getElementById("tableContainer");
            document.body.removeChild(tableIdToRemove);
            tableCreated = 0;
        }
        
        //In YYYY-MM-DD format
        var startDate = $('#begin_date').val();
        //console.log("startDate: " + startDate);
        var endDate = $('#end_date').val();
        //console.log("endDate: " + endDate);
        initializeDates();


        var min = new Date("2001-01-01");
        var max = new Date("2012-12-31");

        var date_regex = /^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/;

        //changed all alerts to sweetAlert and changed ordering of conditionals
        //first checks if start date and end date are valid, then checks if start date and end date are in the correct range
        //finally it checks if start date is before end date
        if (!(date_regex.test(startDate))) {
            sweetAlert("Please enter a valid start date"); //changed alert to sweetAlert
            return;
        }

        if (!(date_regex.test(endDate))) {
            sweetAlert("Please enter a valid end date");
            return;
        }

        if (new Date(startDate) < min || new Date(startDate) > max) {
            sweetAlert("Please enter a start date between 2001-01-01 and 2012-12-31");
            return;
        }

        if (new Date(endDate) < min || new Date(endDate) > max) {
            sweetAlert("Please enter a valid end date between 2001-01-01 and 2012-12-31");
            return;
        }

        if (startDate > endDate) {
            sweetAlert("The end date must be after the start date.");
            return;
        }

        initializeDates();
        datearray = new Array((parseInt(years) - 1) * 2);

        countyCodeVar = localStorage.getItem("countyCodeCookie");
        var zzone = localStorage.getItem("displayTotal"); //changed to displayTotal from previous value
        $('#location').text(zzone)
        $('#location').val(zzone)
        //console.log("cookieValue: " + countyCodeVar);
        if (warningType !== "" && countyCodeVar !== "" && startDate !== "" && endDate !== "") {
            //console.log("We got a valid user input");
            // create a request object
            $('#spinner').fadeIn(function() {
                queryDB(warningType, countyCodeVar, startDate, endDate, function() {
                    $('#spinner').fadeOut();
                });
            });


        }
    }

    function massageData(data, startDate, endDate) {
        //console.log("Total data received: " + data.length)


        var result = {}
        for (i = 0; i < data.length; i++) {
            str = JSON.stringify(data[i], null, 4);
            //console.log("Elem : " + data[i].date)
            warning = data[i]
            if (!(warning['date'] in result)) {
                result[warning.date] = warning
            } else {
                //console.log("DUPLICATE DATE !!!!")
            }
        }
        //console.log(startDate+"\t"+endDate)
        var startDateM = moment(startDate, 'YYYY-MM-DD');
        var endDateM = moment(endDate, 'YYYY-MM-DD');
        //console.log(startDateM+"\t"+endDateM)
        var diffDays = endDateM.diff(startDateM, 'days');
        effectiveDateM = startDateM
        var resultArray = []
        for (i = 0; i <= diffDays; i++) {
            var effectiveDateM = moment(startDate, 'YYYY-MM-DD');
            var date = effectiveDateM.add(i, 'day').format('YYYY-MM-DD')
                //console.log(date)
            if (date in result) {
                resultArray[i] = result[date]
            } else {
                var emptyWarning = {};
                emptyWarning['date'] = date;
                emptyWarning['warning'] = 0;
                emptyWarning['text'] = "Not Found";
                resultArray[i] = emptyWarning
                    //console.log(emptyWarning['date'])
            }
        }

        return resultArray
    }

    function queryDB(warningType, countyCodeCookie, startDate, endDate, callback) {
        var request = new XMLHttpRequest();
        // specify the HTTP method, URL, and asynchronous flag
        request.open('GET', '/findWarning/' + warningType + '/' + countyCodeCookie + '/' + startDate + '/' + endDate, true); //$('#countyCode').val()
        request.addEventListener('load', function(e) {
            csvArray = [
                ["Date", "Warning", "Warning Text"]
            ];
            // inside your Ajax response handler
            if (request.status == 200) {
                var content = request.responseText;
                var data = JSON.parse(content);
                data = massageData(data, startDate, endDate);
                // we have a list of Query results by different dates
                //console.log("length of content: " + data.length);
                //console.log("data: " + data);

                //counter for date array
                var counter = 0;

                for (i = 0; i < data.length; i++) {
                    var date = data[i].date;
                    var warning = data[i].warning;
                    //get current month to ensure that heatmap only displays warnings from april to october
                    var curdate = date.split("-");
                    var curmonth = curdate[1];
                    if (parseInt(curmonth) > 3 && parseInt(curmonth) < 11) {
                        datearray[counter] = warning;
                        counter++;
                    }
                    var text = data[i].text;
                    var wText = text;
                    localStorage.setItem("text" + i, text);
        
                    var table = document.getElementById('table2');
        
                    if (warning == "1") {
                        var tr = document.createElement('tr');
                        var td1 = document.createElement('td');
                        td1.innerHTML = date;
                        tr.appendChild(td1);

                        //var td2 = document.createElement('td');
                        //td2.innerHTML = warning;
                        //tr.appendChild(td2);

                        var td3 = document.createElement('td');
                        var button = document.createElement('button');
                        button.className = "btn btn-primary center-block showSourceText"; //added to ensure that buttons in table match other buttons

                        var textN = document.createTextNode("Show Source Text");
                        button.appendChild(textN);
                        button.id = "text" + i;
        
                        button.onclick = function() {
                            //console.log("this id: " + this.id);
                            sweetAlert(localStorage.getItem(this.id))
                        };

                        td3.appendChild(button);
                        tr.appendChild(td3);
                        table.appendChild(tr);
                    }
                    newRow = [];
                    newRow.push(date);
                    newRow.push(warning);
                    var text2 = '"' + text + '"';
                    newRow.push(text2);
                    //console.log(newRow[2]);
                    csvArray.push(newRow);
                }

                // Create divison and store heat map inside
                var tablediv = document.createElement("div");
                tablediv.id = 'tableContainer';
                document.body.appendChild(tablediv);
                var space = document.createElement('br');
                tablediv.appendChild(space);
                var anotherspace = document.createElement('br');
                tablediv.appendChild(anotherspace);
                for (var m = 0; m < years; m++) {
                    createTable(datearray);
                }
                daycount = 0;
                datearray = [];
                tableCreated = 1;

                callback();
            } else {
                console.log('Something went wrong, check the request status');
                callback();
            }
        });
        //console.log(csvArray.length);
        request.send(null);

    }


    var exportButton = $('#export')[0];
    //console.log(countyCode);
    exportButton.addEventListener('click', download, false);

    function download() {
        downloadCSV({
            filename: csvArray.csv
        });
    }

    function convertArrayOfObjectsToCSV(args) {
        var result, ctr, keys, columnDelimiter, lineDelimiter, data;

        data = args.data || null;
        if (data == null || !data.length) {
            return null;
        }

        columnDelimiter = args.columnDelimiter || ',';
        lineDelimiter = args.lineDelimiter || '\n';

        keys = Object.keys(data[0]);
        result = '';

        data.forEach(function(item) {
            ctr = 0;
            keys.forEach(function(key) {
                if (ctr > 0) result += columnDelimiter;

                result += item[key];
                ctr++;
            });
            result += lineDelimiter;
        });

        // console.log(result);
        return result;
    }

    function downloadCSV(args) {
        var data, filename, link;

        var csv = convertArrayOfObjectsToCSV({
            data: csvArray
        });
        if (csv == null) return;
        filename = String(countyCodeVar) + '/' + String(warningType) + '/' + 'export.csv';

        if (!csv.match(/^data:text\/csv/i)) {
            csv = 'data:text/csv;charset=utf-8,' + csv;
        }
        data = encodeURI(csv);

        link = document.createElement('a');
        link.setAttribute('href', data);
        link.setAttribute('download', filename);
        link.click();
    }

    var ALERT_TITLE = "Oops!";
    var ALERT_BUTTON_TEXT = "Ok";

    if (document.getElementById) {
        window.alert = function(txt) {
            createCustomAlert(txt);
        }
    }

    function createCustomAlert(txt) {
        d = document;

        if (d.getElementById("modalContainer")) return;

        mObj = d.getElementsByTagName("body")[0].appendChild(d.createElement("div"));
        mObj.id = "modalContainer";
        mObj.style.height = d.documentElement.scrollHeight + "px";
        alertObj = mObj.appendChild(d.createElement("div"));
        alertObj.id = "alertBox";

        if (d.all && !window.opera) alertObj.style.top = document.documentElement.scrollTop + "px";

        alertObj.style.left = (d.documentElement.scrollWidth - alertObj.offsetWidth) / 2 + "px";
        alertObj.style.visiblity = "visible";
        h1 = alertObj.appendChild(d.createElement("h1"));
        h1.appendChild(d.createTextNode(ALERT_TITLE));
        msg = alertObj.appendChild(d.createElement("p"));
        //msg.appendChild(d.createTextNode(txt));
        msg.innerHTML = txt;
        btn = alertObj.appendChild(d.createElement("a"));
        btn.id = "closeBtn";
        btn.appendChild(d.createTextNode(ALERT_BUTTON_TEXT));
        btn.href = "#";
        btn.focus();
        btn.onclick = function() {
            removeCustomAlert();
            return false;
        }

        alertObj.style.display = "block";
    }

    function removeCustomAlert() {
        document.getElementsByTagName("body")[0].removeChild(document.getElementById("modalContainer"));
    }

    function ful() {
        alert('Alert this pages');
    }

    $(window).resize(function() {
        $(".sweet-alert").css("margin-top", -$(".sweet-alert").outerHeight() / 2);
    });

    var dropdownlist = $("#dropdown").data("kendoDropDownList");
    dropdownlist.list.width("auto");
});