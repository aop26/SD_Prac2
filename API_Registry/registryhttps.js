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

// Se define el puerto
const port=3000;
mrouter.map(function(){

	this.root.bind(function (req,res){
		res.send("Bienvenido al API REST sobre https")
	})
	/*this.get("/",(req, res) => {
		res.json({message:'Página de inicio de aplicación de ejemplo de SD'})
	});*/
	// Ejecutar la aplicacion
	//this.listen(port, () => {
	//	console.log(`Ejecutando la aplicación API REST de SD en el puerto ${port}`);
	//});


	// FORMATO REQUEST
	// name
	// password
	// id
	// x
	// y
	// ya esta?




	// -- CRUD --

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


	// POST crea un usuario nuevo, se devuelve si se ha creado o no
	// https://localhost:3000/newusr/mlb/cntr/lol
	this.post(/^newusr\/([A-Za-z0-9_]+)\/cntr+\/([A-Za-z0-9_]+)$/).bind(function (request, response, usr, cntr, data) {
		
		console.log("Llamada a POST para: "+usr+" - "+cntr);
		
		let db = new sqlite3.Database('/home/miquel/Escritorio/SD_Prac2/database.db', sqlite3.OPEN_READWRITE, (err) => {
			if (err) {
			  console.error(err.message);
			} else{
				console.log('Connected to the database.');
			}
		});

		db.run(`INSERT into CLIENT(username, password) VALUES('${usr}', '${cntr}') `, (err) => {
			if (err) {
				console.error(err.message);
				response.send("error");
			} else{
				response.send("done");
			}
		});

		db.close()
	});


	// PUT actualiza el usuario especificado, devuelve si lo ha hecho
	// https://localhost:3000/oldusr/mlb/newU/jaja/newC/lol
	this.put(/^oldusr\/([A-Za-z0-9_]+)\/newU+\/([A-Za-z0-9_]+)\/newC+\/([A-Za-z0-9_]+)$/).bind(function (request, response, oldusr, newusr, cntr, data) {
		console.log("Llamada a PUT para: "+oldusr);
	
		let db = new sqlite3.Database('/home/miquel/Escritorio/SD_Prac2/database.db', sqlite3.OPEN_READWRITE, (err) => {
			if (err) {
			  console.error(err.message);
			} else{
				console.log('Connected to the database.');
			}
		});

		db.run(`UPDATE CLIENT SET username='${newusr}', password='${cntr}' where username= '${oldusr}'`, (err) => {
			if (err) {
				console.error(err.message);
				response.send("error");
			} else{
				response.send("done");
			}
		});

		db.close()
	});


	// DELETE borra el usuario especificado, devuelve si lo ha hecho
	// la funcion this.delete no existe, se usa get
	// https://localhost:3000/delete/mlb
	this.get(/^delete\/([A-Za-z0-9_]+)$/).bind(function (request, response, usr) {
		console.log("Llamada a DELETE  para: "+usr);

		let db = new sqlite3.Database('/home/miquel/Escritorio/SD_Prac2/database.db', sqlite3.OPEN_READWRITE, (err) => {
			if (err) {
			  console.error(err.message);
			} else{
				console.log('Connected to the database.');
			}
		});

		db.run(`DELETE FROM CLIENT where username= '${usr}'`, (err) => {
			if (err) {
				console.error(err.message);
				response.send("error");
			} else{
				response.send("done");
			}
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