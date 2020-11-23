var express = require('express');
const jsdom = require('jsdom');
var url = require('url');
const {PythonShell} = require("python-shell");
const bodyParser = require('body-parser');

var app = express();

app.set('view engine', 'ejs')
app.engine('html', require('ejs').renderFile);

app.use(express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());


app.get('/', function(req, res){
    res.sendFile(__dirname + '/main.html');
})

var port = 3000;
var server = app.listen(port, function(){
    console.log('server on');
})

server.timeout = 1000000;

app.post('/result', function (req, res) {
    var url_tmp = req.body;
    var url = []
    for(var i = 0; i < Object.keys(url_tmp).length; i++)
        url.push(url_tmp.have_url);

    let options = {
        mode: 'json', 
        pythonPath: 'C:/Users/dnd/Anaconda3/python.exe', 
        pythonOptions: ['-u'], 
        scriptPath: (__dirname) + '/public/python/', 
        args: [url], 
        encoding: null,
    };

    PythonShell.run("temp.py", options, function(err, data) {
        // for(var i = 0; i < 20; i++){
        //     make_div.innerHTML = (i + 1) + '.' + data[0];
        //     con.appendChild(make_div);
        // }

        words = data[0];
        comments = data[1];
        full_comments = data[2];
        titles = data[3]
        
        if (err) throw err;
        res.render('result', {'words' : words, 'comments' : comments, 'full_comments' : full_comments, 'titles' : titles});
    })
})

