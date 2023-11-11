let teacherId
const url = 'http://127.0.0.1:5000'

window.onload = function() {
  teacherId = parseInt(document.getElementById("teacherid").value)
  showCourse();
}

/* Utility function for updating the dataTable with the given json's data */
function updateTeacherCourseTable(jsonData) {
  // Remove old table body
  var table = document.getElementsByClassName('teacherTable')[0]
  var child = table.children[1]
  table.removeChild(child)
  
  table.classList.remove('hide')

  // Create new table body
  let tbody = document.createElement('tbody')

  // Iterate through json data
  for (let course of jsonData) {
    let tr = document.createElement('tr') // Create new table row

    // CourseName cell
    let tdCourseName = document.createElement('button')
    tdCourseName.innerText = `${course.course}` // Set the value as the text of the table cell
    //Makes course name clickable to show student grade
    tdCourseName.addEventListener('click', function () {
      let course_id = course.c_id
      showStudentsGrade(course_id);
    });
    tr.appendChild(tdCourseName) // Append the table cell to the table row

    // Schedule cell
    let tdSchedule = document.createElement('td')
    tdSchedule.innerText = `${course.schedule}` // Set the value as the text of the table cell
    tr.appendChild(tdSchedule) // Append the table cell to the table row
    
    // Enrollment cell
    let tdEnrollment = document.createElement('td')
    tdEnrollment.innerText = `${course.enrollment}/${course.capacity}` // Set the value as the text of the table cell
    tr.appendChild(tdEnrollment) // Append the table cell to the table row

    tbody.appendChild(tr) // Append the table row to the table
  }

  table.appendChild(tbody) // Append new table body to table
}

  /* Utility function for updating the dataTable with the given json's data */
function updateGradeTable(jsonData) {
  // Remove old table body
  var table = document.getElementsByClassName('gradeTable')[0]
  var child = table.children[1]
  table.removeChild(child)
  
  table.classList.remove('hide')

  // Create new table body
  let tbody = document.createElement('tbody')

  // Iterate through json data
  for (let grade of jsonData) {
    let tr = document.createElement('tr') // Create new table row

    // StudentName cell
    let tdStudentName = document.createElement('td')
    tdStudentName.innerText = `${grade.student}` // Set the value as the text of the table cell
    //Makes course name clickable to show student grade
    tr.appendChild(tdStudentName) // Append the table cell to the table row

    // Grade cell
    let tdGrade = document.createElement('input')
    tdGrade.type = "text"
    tdGrade.value = `${grade.grade}` // Set the value as the text of the table cell
    tr.appendChild(tdGrade) // Append the table cell to the table row
    
    // Update button
    let btnUpdate = document.createElement('button')
    btnUpdate.innerText = `Update Grade` // Set the value as the text of the table cell
    const gradeId = grade.g_id
    btnUpdate.addEventListener('click', () => {
      editStudentGrade(gradeId, tdGrade.value)
    })
    tr.appendChild(btnUpdate) // Append the table cell to the table row

    tbody.appendChild(tr) // Append the table row to the table
  }

  table.appendChild(tbody) // Append new table body to table
}

function hideTables() {
  var teacherTable = document.getElementsByClassName('teacherTable')[0]
  var gradeTable = document.getElementsByClassName('gradeTable')[0]
  
  teacherTable.classList.add("hide")
  gradeTable.classList.add("hide")
}


function showCourse(){
    request = new XMLHttpRequest();
    const apiUrl = `${url}/teacher/${teacherId}/c`;
    request.open("GET", apiUrl, true)
    request.send()
    request.onload = function() {
        var jsonData = JSON.parse(this.responseText).payload
        hideTables()
        updateTeacherCourseTable(jsonData)
    }
}

function showStudentsGrade(c_id){
    request = new XMLHttpRequest();
    const apiUrl = `${url}/course/${c_id}`;
    request.open("GET", apiUrl, true)
    request.send()
    request.onload = function() {
        var jsonData = JSON.parse(this.responseText).payload;
        hideTables()
        updateGradeTable(jsonData)
    }
    
}

function editStudentGrade(g_id, grade){
  let parsed_grade = parseFloat(grade)
  if (!isNaN(parsed_grade)){
    request = new XMLHttpRequest();
    const apiUrl = `${url}/grade/${g_id}/${parsed_grade}`;
    request.open("PUT", apiUrl)
    request.send()
    request.onload = function() {
      alert("Updated student's grade")
    }
  }
  else {
    alert("Improper grade inputted")
  }
}
