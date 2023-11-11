url="http://127.0.0.1:5000"

// This is how you get the teacher id passed through the backend routing
const teacherId = document.getElementById("teacher_id").value; 


function showCourse(t_id){
    request = new XMLHttpRequest();
    const apiUrl = `${url}/teacher/${t_id}/c`;
    request.open("GET", apiUrl)
    request.send()
    request.onload = function() {
        
    }
}



function showStudentsGrade(c_id){
    request = new XMLHttpRequest();
    const apiUrl = `${url}/course/${c_id}`;
    request.open("GET", apiUrl)
    request.send()
    request.onload = function() {

    }
}

function editStudentGrade(g_id){
    request = new XMLHttpRequest();
    const apiUrl = `${url}/grade/${g_id}`;
    request.open("PUT", apiUrl)
    request.send()
    request.onload = function() {

    }
}