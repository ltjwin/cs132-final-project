var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var anyDB = require('any-db');
var conn = anyDB.createConnection('sqlite3://warnings0504.db');

app.use(bodyParser.urlencoded({
    extended: false
}));
app.use(bodyParser.json())

var moment = require('moment');
app.use(express.static(__dirname));


var engines = require('consolidate');
app.engine('html', engines.hogan); // tell Express to run .html files through Hogan

app.set('views', __dirname); // tell Express where to find templates


//Add one more query for state
//LIKE %twoLettersOfCountyCode

//Returns sourceText
//function findWarning(countyCode, date, warningType, warnings, res, currentIndex, lastIndex){
function findWarning(countyCode, dateStart, dateEnd, warningType, res) {
    var start = new Date().getTime();
    //console.log(date +  "%"+warningType+"%"+ countyCode+"\n")

    //conn.query('SELECT * FROM warningInfo1 AS w1 JOIN (SELECT info1_id, effective_date, warning_type, cancellation, location FROM warningInfo2 WHERE effective_date=$1 AND warning_type LIKE $2 AND location=$3) AS w2 ON w1.info1_id = w2.info1_id;',  [date, "%"+warningType+"%", countyCode], function(error, result) {
    //conn.query('SELECT * FROM warningInfo1 AS w1 JOIN (SELECT info1_id, effective_date, warning_type, cancellation, location FROM warningInfo2 WHERE effective_date IN $1 AND warning_type LIKE $2 AND location=$3) AS w2 ON w1.info1_id = w2.info1_id;',  [date, "%"+warningType+"%", countyCode], function(error, result) {  
    conn.query('SELECT * FROM warningInfo1 AS w1 JOIN (SELECT info1_id, effective_date, warning_type, cancellation, location FROM warningInfo2 WHERE (effective_date between $1 AND $2) AND warning_type LIKE $3 AND location=$4) AS w2 ON w1.info1_id = w2.info1_id;', [dateStart, dateEnd, "%" + warningType + "%", countyCode], function(error, result) {
        if (error) {
            console.log("error found during querying: " + error);
            if (currentIndex === lastIndex) {
                console.log("Error Found!!!!!!!!!!!!!!!!1");
                res.json(warnings);
            }
        } else {
            //console.log("inputted date: " + date);

            if (result.rows[0] === undefined) {
                //if (typeof result !== 'undefined' && result.rows.length > 0){
                res.json([]);
            } else {
                console.log("Such a warning Exists! Total " + result.rows.length);
                var sourceText = "";
                var warningsDict = {}
                for (i = 0; i < result.rows.length; i++) {
                    var row = result.rows[i]
                    var warning = {};
                    warning['date'] = row.effective_date;
                    warning['warning'] = 1;

                    var key = row.effective_date + row.warning_type + row.location //row.info1_id + + row.cancellation
                    console.log(i + "\t" + key + "\t" + row.source_text.substring(0, 10))
                    if (!(key in warningsDict)) {
                        sourceText = sourceText + "Source " + ": \n" + row.source_text + "\n\n"; //+ (1)
                        warning['text'] = sourceText;
                        warningsDict[key] = {
                                1: warning
                            }
                            // console.log("if case "+warning['text'].substring(0,20) +"\t length: "+warning['text'].length)
                    } else {
                        //console.log("ELSE CASE")
                        sourceTextNumStr = Object.keys(warningsDict[key])[0]
                        sourceTextNum = parseInt(sourceTextNumStr, 10);
                        warning = warningsDict[key][sourceTextNumStr]
                        sourceTextNum += 1
                        sourceText = sourceText + "Source " + ": \n" + row.source_text + "\n\n"; //+ (sourceTextNum) 
                        warning['text'] += sourceText
                        warningsDict[key] = {}
                        warningsDict[key] = {
                                sourceTextNum: warning
                            }
                            //console.log("ielse case "+warning['text'].substring(0,20) +"\t length: "+warning['text'].length)
                            // console.log("sourceTextNum : "+sourceTextNum)
                    }
                    //console.log("sourceText: "+sourceText)
                }

                str = JSON.stringify(warningsDict, null, 4);
                console.log("\nResult dict : " + Object.keys(warningsDict).length)
                var warningsArray = []
                var i = 0
                for (key in warningsDict) {
                    //console.log("KEY :   "+key)
                    // console.log(key+"\t "+warningsDict[key]+"\t type of : "+typeof(warningsDict[key]))
                    sourceTextNum = Object.keys(warningsDict[key])[0]
                    var warning = warningsDict[key][sourceTextNum]
                    warningsArray[i] = warning
                    i += 1
                }
                str = JSON.stringify(warningsArray, null, 4);
                console.log("Result array : " + warningsArray.length)
                res.json(warningsArray);
            }
        }
    });
    var end = new Date().getTime();
    var time = end - start;
    console.log("\n\nTotal time for findWarning() function is " + time + "\n\n");
}

app.get('/', function(request, response) {
    console.log('Request received:');
    response.render('usmap.html');
});


app.get("/findWarning/:warningType/:countyCode/:startDate/:endDate", function(req, res) {
    console.log("HERE!!!!");
    console.log("raw startDate: " + req.params.startDate);
    console.log("raw endDate: " + req.params.endDate);
    var startDateM = moment(req.params.startDate, 'YYYY-MM-DD');
    var endDateM = moment(req.params.endDate, 'YYYY-MM-DD');
    var diffDays = endDateM.diff(startDateM, 'days');
    console.log("DiffDays: " + diffDays);
    findWarning(req.params.countyCode, startDateM.format('YYYY-MM-DD'), endDateM.format('YYYY-MM-DD'), req.params.warningType, res);
});



app.listen(80);