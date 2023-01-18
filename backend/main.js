

const WebSocketServer = require("ws").Server;
const wss = new WebSocketServer({ port: 8083 });
var http = require('http');
var formidable = require('formidable');
var fs = require('fs');

const { spawn } = require("child_process");
const py = spawn("python3", ['-u',"./ai.py"]);

requestsDict = {}

py.stdout.on("data", (data) => {
    data = data.toString();
    try{
        data=JSON.parse(data);
        }
        catch{
            console.log('pydebug '+data)
            return
        }
        console.log('pyresponse'+data)
        for(header in data){
            requestsDict[header].send(
                JSON.stringify({
                    action:header, parameters:{'data': data[header]}
                })
            )
        }
    



    

});

py.stdout.on("error", (err) => {
    console.log(err);
});

wss.on("connection", (ws) => {
    ws.on("message", (message) => {
        const data = JSON.parse(message);
        const action = data.action
        switch(action){
            case 'useAI':
                requestsDict[data.parameters.userNameAction]=ws
                if (py.exitCode)
                    return;
                py.stdin.write(JSON.stringify(data.parameters) + " \n");
                break
            
            case 'login':
                const pass = data.parameters.passwd
                const usr = data.parameters.usr
                if(checkUsrLogin(usr, pass)=='admin')
                    ws.send(JSON.stringify({action:'loggedIn'}))
                break
        }
        

        

    });


});

function checkUsrLogin(u, p){
    return 'admin'
}

http.createServer(function (req, res) {
    if (req.url == '/fileupload') {
      var form = new formidable.IncomingForm();
      form.parse(req, function (err, fields, files) {
        var oldpath = files.photo.filepath;
        var newpath = './pdfUploads/' + files.photo.originalFilename;
        fs.rename(oldpath, newpath, function (err) {
          if (err) throw err;
          console.log('file received')
         // for (const informIp in ws._socket.remoteAddress            )
          wss.clients.forEach(function each(client) {
            if(client._socket.remoteAddress == req.socket.remoteAddress)
            client.send(
                JSON.stringify({
                    action:'remotePDF4Annotate', parameters:{'fName': files.photo.originalFilename}
                })
            )
            //res.write('File uploaded and moved!');
        res.end();
         });
        });
   });
    } else {
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write('<form action="fileupload" method="post" enctype="multipart/form-data">');
      res.write('<input type="file" name="filetoupload"><br>');
      res.write('<input type="submit">');
      res.write('</form>');
      return res.end();
    }
  }).listen(8081);