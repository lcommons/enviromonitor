var express = require('express');
//var http = require('http');
//var fs = require('fs');
//var index = fs.readFileSync('output.html');
var app = express();
app.use(express.static('/home/pi/kindleServer/static'));
/*http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(index);
}).listen(80);
console.log("Server running on port 80");
*/



app.get('/', function (req, res) {
   // res.send('Hello World!');
//    res.end(index);
    res.sendFile('/home/pi/kindleServer/output.html');
});
app.get('/2', function (req, res) {
   // res.send('Hello World!');
//    res.end(index);
    res.sendFile('/home/pi/kindleServer/output2.html');
});

app.get('/refresh', refreshPage)

function refreshPage (req, res) {
    var python = require('child_process').spawn(
	'python3',
     // second argument is array of parameters, e.g.:
     ["/home/pi/kindleServer/getWeather.py"]
    );
    var output = "";
    python.stdout.on('data', function(data){ output += data });
    python.on('close', function(code){ 
	if (code !== 0) {  
            return res.send(500, code); 
	}
	return res.send(200, output);
    });
    res.sendFile('/home/pi/kindleServer/output.html');
}

var server = app.listen(80, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Weather page server listening on port %s', port);
});