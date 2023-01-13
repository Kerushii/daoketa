

const WebSocketServer = require("ws").Server;
const wss = new WebSocketServer({ port: 8080 });

// run ai.py in this dir
const { spawn } = require("child_process");
const py = spawn("python3", ["./ai.py"]);


clientRequest = null;

// for every second, send the request to the ipc server
setInterval(() => {
    // return if py is no longer running
    if (py.exitCode)
        return;

    if (clientRequest) {
        // send the client request to stdio and include a new line
        py.stdin.write(JSON.stringify(clientRequest) + " \n");

    clientRequest=null;
    }
}, 1000);

// listen for messages from stdio
py.stdout.on("data", (data) => {
    // decode the stdio message
    console.log('py responded:'+data)
    data = data.toString();
    if(!data.includes('fdgerguhyGTYGVTFYTYGRtfgycyrtfGYVYTGYTvGTVYGUBYU'))
        return;
    // get all string after "fdgerguhyGTYGVTFYTYGRtfgycyrtfGYVYTGYTvGTVYGUBYU"
    data = data.slice(data.indexOf("fdgerguhyGTYGVTFYTYGRtfgycyrtfGYVYTGYTvGTVYGUBYU") + 48);




    
    wss.clients.forEach((client) => {
        client.send(data);
    })
});

py.stdout.on("error", (err) => {
    console.log(err);
});




wss.on("connection", (ws) => {
    ws.on("message", (message) => {
        // parse the message as json
        const data = JSON.parse(message);
        console.log(data)
        // add the request to the list of requests
        clientRequest = data;

    });


});

