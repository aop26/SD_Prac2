const express = require("express");
const app = express();
// Se define el puerto
const port=3000;
app.get("/",(req, res) => {
	res.json({message:'Página de inicio de aplicación de ejemplo de SD'})
});
// Ejecutar la aplicacion
app.listen(port, () => {
	console.log(`Ejecutando la aplicación API REST de SD en el puerto ${port}`);
});



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






// Andres fuma porros y esto tal vez no hace falta


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
app.get("/:name/:password",(request, response) => {

	const key = GetKey();
	const name = CryptoJS.AES.decrypt(request.body.name, key);
	const passwd = CryptoJS.AES.decrypt(request.body.password, key);

	const sql = `SELECT * FROM Usuarios where username='${name}' and password='${password}'`;

	connection.query(sql,(error,resultado)=>{
		if (error) throw error;
		if (resultado.length > 0){
			response.send(); //response.json(resultado);
		} else {
			response.send('No hay resultados');
		}
	});
});


app.post("/",(request, response) => {
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


app.put("/:id",(request, response) => {
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


app.delete("/:id",(request, response) => {
	const key = GetKey();
	const id = CryptoJS.AES.decrypt(request.body.id, key);


	//const {id} = request.params;
	sql = `DELETE FROM Usuarios WHERE idUsuario= ${id}`;
	connection.query(sql,error => {
	if (error) throw error;
		response.send('Usuario borrado');
	});
});


