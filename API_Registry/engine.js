const https = require("https");
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();
const journey = require('journey');
//const app = express();
var mrouter = new (journey.Router)();

const options ={
	key: fs.readFileSync('cert/key.pem'),
	cert: fs.readFileSync('cert/cert.pem')
}

function strToMap(str) {
    function isNumeric(s) {
        return !isNaN(s - parseFloat(s));
    }
    var m = Array(20).fill(0).map(x => Array(20).fill(0));
    for (let i = 0; i < str.length; i++) {
        if(str[i]=='r'){
            var auxStr = "";
            i++;
            while(i<str.length && isNumeric(str[i])){
                auxStr+=mapStr[i];
                i++;
            }
            i--;
            m[currentCount-(currentCount/20)*20][currentCount/20]=auxStr;
        }else if(str[i]=='u'){
            var auxStr = "";
            i++;
            while(i< str.length && isNumeric(str[i])){
                auxStr+=mapStr[i];
                i+=1;
            }
            i--;
            m[currentCount-(currentCount/20)*20][currentCount/20]="../img/"+auxStr;
        }
        
    }
    return m
}

// Se define el puerto
const port=443;
mrouter.map(function(){

	this.root.bind(function (req,res){
		res.send("<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>")
	})

	// GET lee un usr y devuelve el hash de la contraseña
	// https://localhost:3000/usr/mlb51
	this.get(/^usr\/([A-Za-z0-9_]+)$/).bind(function (request, response, usr) {

		let db = new sqlite3.Database('/home/miquel/Escritorio/SD_Prac2/database.db', sqlite3.OPEN_READWRITE, (err) => {
			if (err) {
			  console.error(err.message);
			} else{
				console.log('Connected to the database.');
			}
		});

		console.log("Llamada a GET para: "+usr);

		db.serialize(() => {
			db.each(`SELECT password FROM CLIENT where username= '${usr}'`, (err, row) => {
			  if (err) {
				console.error(err.message);
				response.send(err.message);
			  }
			  response.send(row.password);
			});
		});

		db.close()
	});


})

https.createServer(options, function(request, response){
	var body = "";

	request.addListener('data', function(chunk){body+=chunk});
	request.addListener('end', function(){
		mrouter.handle(request, body, function(result){
			response.writeHead(result.status, result.headers);
			response.end(result.body);
		})
	})
}).listen(port);