const express = require('express');
const path = require('path');
var exec = require('child_process').exec;
//var http = require('http');
//var fs = require('fs');
//var index = fs.readFileSync('output.html');
const app = express();
app.use(express.static('static'));
/*http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(index);
}).listen(80);
console.log("Server running on port 80");
*/



app.get('/', function (req, res) {
   // res.send('Hello World!');
//    res.end(index);
    res.sendFile(path.join(__dirname,'output.html'));
});

app.get('/refresh', function (req, res) {
    exec('getWeather.py', (err, stdout, stderr) => {
	if (err) {
	    console.error(err);
	    return;
	}
	console.log(stdout);
    });
    res.sendFile(path.join(__dirname,'output.html'));
});

var server = app.listen(80, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Example app listening on port %s', port);
});
