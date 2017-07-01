var app = app || {};

app.dom = {
    domManipula: function() {
        console.log('hello world');
        var mainTable = document.getElementById('planets');
        var container = document.createElement('div');
        container.className = 'container';

        var divRow = document.createElement('div');
        divRow.className = "row";
        container.appendChild(divRow);
        var nameCol = document.createElement('div');
        nameCol.className = 'col-sm-1';
        divRow.appendChild(nameCol);
        for (var i = 0; i < 7; i++) {
            var nameField = document.createElement('h2');
            if (i === 0) {
                var nameText = document.createTextNode("Name");
            } else if (i === 1) {
                var nameText = document.createTextNode("Diameter");
            } else if (i === 2) {
                var nameText = document.createTextNode("Climate");
            } else if (i === 3) {
                var nameText = document.createTextNode("Terrain");
            } else if (i === 4) {
                var nameText = document.createTextNode("Surface Water");
            } else if (i === 5) {
                var nameText = document.createTextNode("Population");
            } else if (i === 6) {
                var nameText = document.createTextNode("Residents");
            }
            nameField.appendChild(nameText);
            nameCol.appendChild(nameField);
        }
    }
}

function domElements() {
    $.ajax({
        dataType: "json",
        url: 'https://swapi.co/api/planets/',
        success: function(response) {

        }
    })
}
function getResident(residentList) {
    var infoToShow = [];
    for (var i = 0; i < residentList.length; i++) {
        //im sure there is a better solution
        $.ajax({
            dataType: "json",
            url: residentList[i],
            success: function(response) {
                infoToShow.push({'name': response['name'],
                                'height': response['height'],
                                'mass': response['mass'],
                                'skin_color': response['skin_color'],
                                'hair_color': response['hair_color'],
                                'eye_color': response['eye_color'],
                                'birth_year': response['birth_year'],
                                'gender': response['gender']});
                modaManipula(infoToShow);
            },
        });
    }
}

function vote(votedId) {
    var id = document.getElementById('user').value;
    console.log(id);
    var voted = document.getElementById(votedId).innerHTML;
    var times = document.getElementById(voted).value;
    times = Number(times)+1;
    document.getElementById(voted).value = times;
    document.getElementById(voted).innerHTML = times;
    console.log(id, votedId, voted, times);
    document.cookie = id+'+'+voted+'='+times+'+'+votedId;
}


function modaManipula(whatToManipula) {
    document.getElementById('modala').innerHTML = '';
    for (var i = 0; i < whatToManipula.length; i++) {
        var modal = document.getElementById('modala');
        var resiDiv = document.createElement('div');
        modal.appendChild(resiDiv);
        var table = document.createElement('table');
        table.className = "table"
        resiDiv.appendChild(table);

        var tHead = document.createElement('thead');function domManipula() {
    var table = document.getElementById('mainTable')
    
}
        table.appendChild(tHead);
        var tRowHead = document.createElement('tr');
        tHead.appendChild(tRowHead);
        var tH = document.createElement('th');
        tRowHead.appendChild(tH);
        var residentName = document.createTextNode(whatToManipula[i]['name']);
        tH.appendChild(residentName);
        
        var tBody = document.createElement('tbody');
        table.appendChild(tBody);
        var tRowBody = document.createElement('tr');
        tBody.appendChild(tRowBody);
        
        var tDHeight = document.createElement('td');
        tRowBody.appendChild(tDHeight);
        var height = document.createTextNode('Height: '+whatToManipula[i]['height']);
        tDHeight.appendChild(height);

        var tDMass = document.createElement('td');
        tRowBody.appendChild(tDMass);
        var mass = document.createTextNode('Mass: '+whatToManipula[i]['mass']);
        tDMass.appendChild(mass);

        var tDSkin = document.createElement('td');
        tRowBody.appendChild(tDSkin);
        var skin = document.createTextNode('Skin Color: '+whatToManipula[i]['skin_color']);
        tDSkin.appendChild(skin);

        var tDHair = document.createElement('td');
        tRowBody.appendChild(tDHair);
        var hair = document.createTextNode('Hair color: '+whatToManipula[i]['hair_color']);
        tDHair.appendChild(hair);

        var tDEye = document.createElement('td');
        tRowBody.appendChild(tDEye);
        var eye = document.createTextNode('Eye color: '+whatToManipula[i]['eye_color']);
        tDEye.appendChild(eye);

        var tDBirth = document.createElement('td');
        tRowBody.appendChild(tDBirth);
        var birth = document.createTextNode('Birth date: '+whatToManipula[i]['birth_date']);
        tDBirth.appendChild(birth);

        var tDGender = document.createElement('td');
        tRowBody.appendChild(tDGender);
        var gender = document.createTextNode('Gender: '+whatToManipula[i]['gender']);
        tDGender.appendChild(gender);
    }
}

function fakme() {
    $.ajax({
        dataType: "json",
        url: document.getElementById('next'),
        success: function(response) {
            console.log(response)
        }
    })
}
