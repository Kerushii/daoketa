

const WebSocketServer = require("ws").Server;
const wss = new WebSocketServer({ port: 8080 });

// run ai.py in this dir
const { spawn } = require("child_process");
const py = spawn("python3", ['-u',"./ai.py"]);

requestsDict = {}



// listen for messages from stdio
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
        requestsDict[data.userNameAction]=ws
        if (py.exitCode)
            return;
        py.stdin.write(JSON.stringify(data) + " \n");

        

    });


});

