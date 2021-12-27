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
	// hay que modificar los metodos para que lea de nuestra base de datos

	// la string random esta 
	this.get("/usuario/:name",(request, response) => {

		//const key = GetKey();
		//const name = CryptoJS.AES.decrypt(request.body.name, key);
		//const passwd = CryptoJS.AES.decrypt(request.body.password, key);
//
		//const sql = `SELECT * FROM Usuarios where username='${name}' and password='${password}'`;
		console.log(`Llamada a GET`);
		//connection.query(sql,(error,resultado)=>{
		//	if (error) throw error;
		//	if (resultado.length > 0){
		//		response.send(); //response.json(resultado);
		//	} else {
		//		response.send('No hay resultados');
		//	}
		//});
	});


	/*this.post("/",(request, response) => {
		const key = GetKey();
		const name = CryptoJS.AES.decrypt(request.body.name, key);
		const passwd = CryptoJS.AES.decrypt(request.body.password, key);


		const sql = 'INSERT INTO Usuarios SET ?';
		const usuarioObj = {
			nombre: request.body.nombre,
			ciudad: request.body.ciudad,
			correo: request.body.correo
		}
		connection.query(sql,usuarioObj,error => {
		if (error) throw error;
			response.send('Usuario creado');
		});
	});


	this.put("/:id",(request, response) => {
		const key = GetKey();
		const name = CryptoJS.AES.decrypt(request.body.name, key);
		const passwd = CryptoJS.AES.decrypt(request.body.password, key);
		const id = CryptoJS.AES.decrypt(request.body.id, key);

		const sql = `UPDATE Usuarios SET nombre='${name}', password.='${passwd}' WHERE idUsuario=${id}`;

		connection.query(sql,error => {
		if (error) throw error;
			response.send('Usuario modificado');
		});
	});


	this.delete("/:id",(request, response) => {
		const key = GetKey();
		const id = CryptoJS.AES.decrypt(request.body.id, key);


		//const {id} = request.params;
		sql = `DELETE FROM Usuarios WHERE idUsuario= ${id}`;
		connection.query(sql,error => {
		if (error) throw error;
			response.send('Usuario borrado');
		});
	});*/


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