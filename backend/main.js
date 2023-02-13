const WebSocketServer = require("ws").Server;
const { spawn } = require("child_process");
var pdfUtil = require('pdf-to-text');

var aiWorker = null
/*
const py = spawn("python3", ['-u',"./ai.py"]);

py.stdout.on("data", (data) => {
    data = data.toString();
    // console.log(daya)


});

py.stdout.on("error", (err) => {
    console.log(err);
});
*/

const pyws = new WebSocketServer({ port: 8084 });
pyws.on("connection", (ws) => {
    aiWorker = ws
    console.log('ai worker connected')
    ws.on("message", (message) => {
        // console.log(data)
        const data = JSON.parse(message);
        const token = data.token
        console.log(data)
        const action = data.action
        switch(action){
            case 'trialToken':
                tokens2Client[token].send(JSON.stringify({action:data.action, parameters:{text: data.response, token: data.token}}))
                break
            
            default:
                const rtText = data.response
                tokens2Client[token].send(JSON.stringify({action:data.action, parameters:{text: rtText, token: data.token}}))
        }

    });


});


var crypto = require('crypto');
var base64url = require('base64url');
const tokens2Client = {}
const wss = new WebSocketServer({ port: 8083 });
function checkUsrLogin(u, p){
    return 'admin'
}
wss.on("connection", (ws) => {
    const token = base64url(crypto.randomBytes(45));
    ws.send(JSON.stringify({action:'token', parameters:{token}}))
    ws.on("message", (message) => {

        const data = JSON.parse(message);
        const action = data.action
        switch(action){
            case 'useAI4Assist':
                // token = base64url(crypto.randomBytes(45));
                // data.parameters.token = token

                tokens2Client[token] = ws
                // data.parameters.text = data.parameters.text.substring(0, 1024)
                // get the last 1024 characters
                data.parameters.text = data.parameters.text
                //vws.send(JSON.stringify({action:'useAIConfirm', parameters:{token}}))
                aiWorker.send(JSON.stringify({"len":data.parameters.len,"temp":data.parameters.temp,"ai":data.parameters.ai,"token":data.parameters.token,"text":data.parameters.text,"action":data.action}))
                break
            
            case 'useAI4Annotate':
                // token = base64url(crypto.randomBytes(45));
                // data.parameters.toekn = token
                tokens2Client[token] = ws
                data.parameters.text = data.parameters.text
                // ws.send(JSON.stringify({action:'useAIConfirm', parameters:{token}}))
                aiWorker.send(JSON.stringify({"len":data.parameters.len,"temp":data.parameters.temp,"ai":data.parameters.ai,"token":data.parameters.token,"text":data.parameters.text,"action":data.action}))
                break
            
            case 'login':
                const pass = data.parameters.passwd
                const usr = data.parameters.usr
                if(checkUsrLogin(usr, pass)=='admin')
                    ws.send(JSON.stringify({action:'loggedIn'}))
                break
            
            case 'trialToken':
                tokens2Client[token] = ws
                // data.parameters.text = data.parameters.text.substring(0, 1024)
                // get the last 1024 characters
                data.parameters.text = data.parameters.text
                //vws.send(JSON.stringify({action:'useAIConfirm', parameters:{token}}))
                aiWorker.send(JSON.stringify({"ai":data.parameters.ai,"token":data.parameters.token,"text":data.parameters.text,"action":data.action}))
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
            {client.send(
                JSON.stringify({
                    action:'remotePDF4Annotate', parameters:{'fName': files.photo.originalFilename}
                })
            )
            pdfUtil.pdfToText(newpath, function(err, data) {
                if (err) console.log(err);
                console.log(data); //print all text    
              });
        }

         });
         res.write(newpath);
         res.end();
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
