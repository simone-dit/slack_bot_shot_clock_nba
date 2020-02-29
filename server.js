var http = require('http'),
    url = require('url'),
    qs = require('querystring');

var server = http.createServer(function (req, res) {
    var urlParts = url.parse(req.url, true),
        urlParams = urlParts.query,
        urlPathname = urlParts.pathname,
        body = '',
        reqInfo = {};

    req.on('data', function (data) {
        body += data;
    });

    req.on('end', function () {
        reqInfo.urlPathname = urlPathname; //sample value: /api/employee
        reqInfo.urlParams = urlParams; //sample value: {"id": "12345","name": "Kay"}
        reqInfo.body = qs.parse(body); //sample value: {"firstname": "Clarkson","lastname": "Nick"}
        reqInfo.urlParts = urlParts;

        console.log(reqInfo);
        res.writeHead(200, {'Content-type':'application/json'});
        res.end(JSON.stringify(reqInfo));
    });

});
server.listen(8000);
console.log("Server running at http://localhost:3333");