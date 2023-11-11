const studentId = document.getElementById("student_id").value;
url="http://127.0.0.1:5000"

/* Utility function for updating the dataTable with the given json's data */
function updateTable(jsonData) {

    // Remove old table body
    var table = document.getElementsByTagName("table")[0];
    var child = document.getElementsByTagName("tbody")[0];
    table.removeChild(child);

    // Create new table body
    let tbody = document.createElement("tbody");
    
    // Iterate through json data
    for (var student in jsonData){
        let tr = document.createElement("tr"); // Create new table row

        var courses = jsonData[student]; // Get grade via student key

        // Student cell
        let tdStudent = document.createElement("td");
        tdStudent.innerText = student; // Set the value as the text of the table cell
        tr.appendChild(tdStudent); // Append the table cell to the table row

        // Grade cell
        let tdGrade = document.createElement("td");
        tdGrade.innerText = grade; // Set the value as the text of the table cell
        tr.appendChild(tdGrade); // Append the table cell to the table row
        
        tbody.appendChild(tr);// Append the table row to the table
    }

    table.appendChild(tbody); // Append new table body to table
}


// GET API call to receive a student's registered courses
// Displays courses for registration
function displayRegistrationCourses () {
    var request = new XMLHttpRequest();
    const apiUrl = `${url}/student/${studentId}/c`;
    request.open("GET", apiUrl, true);

    request.send();
    request.onload = function() {
            updateTable(JSON.parse(this.responseText));
    };
}


// GET API call to receive courses for registration
function getAllOfferedCourses() {
    var request = new XMLHttpRequest();
    const apiUrl = `${url}/student/${studentId}/r`;
    request.open("GET", apiUrl, true);

    request.send();
    request.onload = function() {
        updateTable(JSON.parse(this.responseText));
    };
    
}

// function updateCourses() {
//     var request = new XMLHttpRequest();
//     const apiUrl = `${url}/student/${studentId}/r`

//     request.open("POST", apiUrl);
//     request.setRequestHeader("Content-Type", "application/json");

//     xhttp.send();

//     xhttp.onload = function() {
//         updateTable(JSON.parse(this.responseText));
//     };
// }






