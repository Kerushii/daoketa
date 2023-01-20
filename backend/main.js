const WebSocketServer = require("ws").Server;
const py = spawn("python3", ['-u',"./ai.py"]);
var aiWorker
const { spawn } = require("child_process");
py.stdout.on("data", (data) => {
    data = data.toString();
    console.log(daya)


});

py.stdout.on("error", (err) => {
    console.log(err);
});


var crypto = require('crypto');
var base64url = require('base64url');
const tokens2Client = {}
const wss = new WebSocketServer({ port: 8083 });
function checkUsrLogin(u, p){
    return 'admin'
}
wss.on("connection", (ws) => {
    ws.on("message", (message) => {
        const data = JSON.parse(message);
        const action = data.action
        let token = ''
        switch(action){
            case 'useAI4Assist':
                token = base64url(crypto.randomBytes(45));
                data.parameters.toekn = token
                tokens2Client.token = ws
                ws.send(JSON.stringify({action:'useAIConfirm', parameters:{token}}))
                aiWorker.send(JSON.stringify(data))
                break
            
            case 'useAI4Annotate':
                token = base64url(crypto.randomBytes(45));
                data.parameters.toekn = token
                tokens2Client.token = ws
                ws.send(JSON.stringify({action:'useAIConfirm', parameters:{token}}))
                aiWorker.send(JSON.stringify(data))
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


var http = require('http');
var formidable = require('formidable');
var fs = require('fs');
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