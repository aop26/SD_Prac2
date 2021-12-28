const https = require("https");
const fs = require('fs');
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



	// -- BASE DE DATOS --
	// falta cambiarlo a sqlite

	/*const mysql = require ("mysql");
	const bodyParser = require("body-parser");
		// Configuración de la conexión a la base de datos MySQL
	const connection = mysql.createConnection({
		host: 'localhost',
		user:'root',
		password: 'root',
		database:'SD_MYSQL'
	});

		// Comprobar conexión a la base de datos
	connection.connect(error=> {
	if (error) throw error;
		console.log('Conexión a la base de datos SD_MYSQL correcta');
	});*/




	// Funciones para encriptar y desencriptar
	// var encrypted = CryptoJS.AES.encrypt("Message", "Secret Passphrase");
	// var decrypted = CryptoJS.AES.decrypt(encrypted, "Secret Passphrase");
	//function GetKey(){
	//	var key = "";
	//
	//	const readline = require("readline"),
	//		fs = require("fs"),
	//		NOMBRE_ARCHIVO = "clave";
	//	
	//	let lector = readline.createInterface({
	//		input: fs.createReadStream(NOMBRE_ARCHIVO)
	//	});
	//
	//	lector.on("line", linea => {
	//		key = linea; //console.log("Tenemos una línea:", linea);
	//	});
	//
	//	return key;
	//}




	// FORMATO REQUEST
	// name
	// password
	// id
	// x
	// y
	// ya esta?




	// -- CRUD --

	// GET lee un usr y devuelve el hash de la contraseña
	this.get(/^usr\/([A-Za-z0-9_]+)$/).bind(function (request, response, usr) {

		//const sql = `SELECT * FROM Usuarios where username='${name}' and password='${password}'`;
		console.log("Llamada a GET para: "+usr);
		response.send('lyenedo usuario: '+usr);
		//connection.query(sql,(error,resultado)=>{
		//	if (error) throw error;
		//	if (resultado.length > 0){
		//		response.send(); //response.json(resultado);
		//	} else {
		//		response.send('No hay resultados');
		//	}
		//});
	});


	// POST crea un usuario nuevo, se devuelve si se ha creado o no
	this.post(/^newusr\/([A-Za-z0-9_]+)\/cntr+\/([A-Za-z0-9_]+)$/).
		 bind(function (request, response, usr, cntr, data) {
		
		console.log("Llamada a POST para: "+usr+" - "+cntr);
		response.send('escribiendo usuario: '+usr);

		//const sql = 'INSERT INTO Usuarios SET ?';
		//const usuarioObj = {
		//	nombre: request.body.nombre,
		//	ciudad: request.body.ciudad,
		//	correo: request.body.correo
		//}
		//connection.query(sql,usuarioObj,error => {
		//if (error) throw error;
		//	response.send('Usuario creado');
		//});
	});


	// PUT actualiza el usuario especificado, devuelve si lo ha hecho
	this.put(/^oldusr\/([A-Za-z0-9_]+)\/newU+\/([A-Za-z0-9_]+)\/newC+\/([A-Za-z0-9_]+)$/).
	     bind(function (request, response, usr, cntr, data) {
		console.log("Llamada a PUT para: "+usr);
		response.send('actualizando usuario: '+usr);
		//const sql = `UPDATE Usuarios SET nombre='${name}', password.='${passwd}' WHERE idUsuario=${id}`;
		//connection.query(sql,error => {
		//if (error) throw error;
		//	response.send('Usuario modificado');
		//});
	});


	// DELETE borra el usuario especificado, devuelve si lo ha hecho
	// la funcion this.delete no existe, se usa get
	this.get(/^delete\/([A-Za-z0-9_]+)$/).bind(function (request, response, usr) {
		console.log("Llamada a DELETE  para: "+usr);
		response.send('borrando usuario: '+usr);
		//const {id} = request.params;
		//sql = `DELETE FROM Usuarios WHERE idUsuario= ${id}`;
		//connection.query(sql,error => {
		//if (error) throw error;
		//	response.send('Usuario borrado');
		//});
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