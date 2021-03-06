const https = require("https");
const fs = require('fs');
const app = require('express')();
//const app = express();
//var mrouter = new (journey.Router)();
function readMap(){
    return fs.readFileSync('../map.txt','utf8')
}
function isNumeric(s) {
    return !isNaN(s - parseFloat(s));
}
function strToMap(str) {
    var m = Array(20).fill(0).map(x => Array(20).fill(0));
    var currentCount = 0;
    for (let i = 0; i < str.length; i++) {
        if(str[i]=='r'){
            var auxStr = "";
            i++;
            while(i<str.length && isNumeric(str[i])){
                auxStr+=str[i];
                i++;
            }
            i--;
            m[currentCount-parseInt(currentCount/20)*20-1][parseInt(currentCount/20)-1]=auxStr;
        }else if(str[i]=='u'){
            var auxStr = "";
            i++;
            while(i< str.length && isNumeric(str[i])){
                auxStr+=str[i];
                i+=1;
            }
            i--;
            m[currentCount-parseInt(currentCount/20)*20-1][parseInt(currentCount/20)-1]="/img/"+auxStr;
        }
        currentCount++;
    }
    //console.log(str, m)
    return m
}
function mapHtml(host){
    var start = '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="1"><style>th {border: 1px solid black;padding:0;width:40px; height:40px;}th.first{background-color:#FF8080}th.second{background-color:#80FF80}th.third{background-color:#8080FF}th.fourth{background-color:#FFFF80}</style></head><body><table>';
    var end = '</table></body></html>'
    var body = ''
    m = strToMap(readMap());
    for (let i = 0; i < m.length; i++) {
        body+='<tr>'
        for (let j = 0; j < m[i].length; j++) {
            var clase = 'first';
            if(j < 10){
                if(i > 9){
                    clase = 'third';
                }
            }else{
                if(i < 10){
                    clase = 'second';
                }else{
                    clase = 'fourth';
                }
            }
            body+='<th class="'+clase+'">'
            var element = m[j][i];
            //console.log(element)
            if(element!=0){
                if(isNumeric(element)){
                    body+=element;
                }else{
                    body+='<img src="https://'+host+element+'" alt="'+element+'" width="40" height="40">';
                }
            }
            body+='</th>'
        }
        body+='</tr>'
        
    }
    return start + body + end;
}

const options ={
	key: fs.readFileSync('cert/key.pem'),
	cert: fs.readFileSync('cert/cert.pem')
}
	
// Se define el puerto
const port=3001;

app.get('/',function(req,res) {
    res.send(mapHtml(req.get('host')))
})
app.get('/img/:img', function(req,res){
    var path = require('path')
    res.sendFile(path.resolve(__dirname+"/../img/"+req.params['img']))
})


https.createServer(options, app).listen(port);