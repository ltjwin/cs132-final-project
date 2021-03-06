var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var anyDB = require('any-db');
var conn = anyDB.createConnection('sqlite3://warnings0420.db');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json())

var moment = require('moment');
app.use(express.static(__dirname));


var engines = require('consolidate');
app.engine('html', engines.hogan); // tell Express to run .html files through Hogan

app.set('views', __dirname); // tell Express where to find templates


//Add one more query for state
//LIKE %twoLettersOfCountyCode

//Returns sourceText
function findWarning(countyCode, date, warningType, warnings, res, currentIndex, lastIndex){
    console.log(date +  "%"+warningType+"%"+ countyCode+"\n")
    conn.query('SELECT * FROM warningInfo1 AS w1 JOIN (SELECT info1_id, effective_date, warning_type, cancellation, location FROM warningInfo2 WHERE effective_date=$1 AND warning_type LIKE $2 AND location=$3) AS w2 ON w1.info1_id = w2.info1_id;',  [date, "%"+warningType+"%", countyCode], function(error, result) {
        
        if (error) {
            console.log("error found during querying: " + error);
            if (currentIndex===lastIndex){
                console.log("Error Found!!!!!!!!!!!!!!!!1");
                res.json(warnings);
            }
        } else{
            console.log("inputted date: " + date);
            
            if (result.rows[0]===undefined){
            //if (typeof result !== 'undefined' && result.rows.length > 0){
                //no warning exists, output 0 as Boolean value
                console.log("No such warning exists!");
                var warning = {};
                warning['date'] = date;
                warning['warning'] = 0;
                warning['text'] = "Not Found";
                
                warnings[currentIndex] = warning;
                if (currentIndex===lastIndex){
                    res.json(warnings);
                }

                /*
                warnings.push(warning);
                if(warnings.length===(lastIndex+1)){
                   res.json(warnings); 
                }
                */
            } else{
                console.log("Such a warning Exists!");
                var sourceText="";
                console.log("sourceText: "+result.rows[0])
                for (i = 0; i < result.rows.length; i++){
                    sourceText = sourceText + "Source " + (i+1) +": \n" + result.rows[i].source_text + "\n\n";
                    console.log("sourceText: "+sourceText)
                }
                var warning = {};
                warning['date'] = date;
                warning['warning'] = 1;
                warning['text'] = sourceText;

                
                warnings[currentIndex] = warning;
                if (currentIndex===lastIndex){
                    res.json(warnings);
                }

                /*
                warnings.push(warning);
                if(warnings.length===(lastIndex+1)){
                   res.json(warnings); 
                }*/
            }            
        }
    });        
}

app.get('/', function(request, response){
    console.log('Request received:');
    response.render('usmap.html');
});

app.get("/findWarning/:warningType/:countyCode/:startDate/:endDate", function(req, res) {
    console.log("HERE!!!!");
    console.log("raw startDate: " + req.params.startDate);
    console.log("raw endDate: " + req.params.endDate);
    var startDateM = moment(req.params.startDate, 'YYYY-MM-DD');
    var endDateM = moment(req.params.endDate, 'YYYY-MM-DD');

    //var startDateString = startDateM.format('YYYY-MM-DD');
    var diffDays = endDateM.diff(startDateM, 'days');
    console.log("DiffDays: "+ diffDays);
    var warnings = [];
    for (i=0; i<=diffDays; i++){
        var effectiveDateM = moment(req.params.startDate, 'YYYY-MM-DD');
        findWarning(req.params.countyCode, effectiveDateM.add(i, 'day').format('YYYY-MM-DD'), req.params.warningType, warnings, res, i, diffDays);        
    }

    //console.log("Done sending queries!!!");    
});



app.listen(8080);
