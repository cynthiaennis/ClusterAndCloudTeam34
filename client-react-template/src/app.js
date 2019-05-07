


/*
// const express = require('express');
// const bodyParser = require('body-parser');
const path = require('path');
const NodeCouchDb = require('node-couchdb');

const dbName = 'customer';
const viewUrl = '_design/all_customers/_view/all';

const couch = new NodeCouchDb({
    auth: {
        user: 'admin',
        password: '123456'
    }
});

couch.listDatabases().then(function (dbs) {
    console.log(dbs);
});
// const app = express();


app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.get('/', function (req, res) {
    couch.get(dbName, viewUrl).then(
        function (data, headers, status) {
            console.log(data);
            res.render('index',{
                customers:data
            });
        },
        function (err) {
            res.send(err)
        });
});

export function showData(){
    return app.get;
}

//
// app.listen(3000, function () {
//     console.log('Server Started On Port 3000')
// });
//
*/
