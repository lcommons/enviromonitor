var express = require('express');
var app = express();
app.use(express.static('/home/pi/kindleServer/static'));




app.get('/', function (req, res) {
    res.sendFile('/home/pi/kindleServer/output.html');
});
app.get('/2', function (req, res) {
    res.sendFile('/home/pi/kindleServer/output2.html');
});

app.get('/refresh', refreshPage)

function refreshPage (req, res) {
    var python = require('child_process').spawn(
	'python3',
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
