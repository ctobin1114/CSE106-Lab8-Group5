let studentId
const url = 'http://127.0.0.1:5000'

window.onload = function() {
  studentId = parseInt(document.getElementById("studentid").value)
  displayRegisteredCourses()
}

/* Utility function for updating the dataTable with the given json's data */
function updateStudentTable(jsonData) {
    // Remove old table body
    var table = document.getElementsByClassName('studentTable')[0]
    var child = table.children[1]
    table.removeChild(child)

    table.classList.remove('hide')

    // Create new table body
    let tbody = document.createElement('tbody')

    // Iterate through json data
    for (var course of jsonData) {
        let tr = document.createElement('tr') // Create new table row

        // CourseName cell
        let tdCourseName = document.createElement('td')
        tdCourseName.innerText = `${course.course}` // Set the value as the text of the table cell
        tr.appendChild(tdCourseName) // Append the table cell to the table row

        // Teacher cell
        let tdTeacher = document.createElement('td')
        tdTeacher.innerText = `${course.teacher}` // Set the value as the text of the table cell
        tr.appendChild(tdTeacher) // Append the table cell to the table row

        // Schedule cell
        let tdSchedule = document.createElement('td')
        tdSchedule.innerText = `${course.schedule}` // Set the value as the text of the table cell
        tr.appendChild(tdSchedule) // Append the table cell to the table row

        // Grade cell
        let tdGrade = document.createElement('td')
        tdGrade.innerText = `${course.grade}` // Set the value as the text of the table cell
        tr.appendChild(tdGrade) // Append the table cell to the table row

        tbody.appendChild(tr) // Append the table row to the table
    }

    table.appendChild(tbody) // Append new table body to table
}


/* Utility function for updating the dataTable with the given json's data */
function updateRegistrationTable(jsonData) {
    // Remove old table body
    var table = document.getElementsByClassName('registrationTable')[0]
    var child = table.children[1]
    table.removeChild(child)
    
    table.classList.remove('hide')

    // Create new table body
    let tbody = document.createElement('tbody')

    // Iterate through json data
    for (var course of jsonData) {
        let tr = document.createElement('tr') // Create new table row

        // CourseName cell
        let tdCourseName = document.createElement('td')
        tdCourseName.innerText = `${course.course}` // Set the value as the text of the table cell
        tr.appendChild(tdCourseName) // Append the table cell to the table row

        // Teacher cell
        let tdTeacher = document.createElement('td')
        tdTeacher.innerText = `${course.teacher}` // Set the value as the text of the table cell
        tr.appendChild(tdTeacher) // Append the table cell to the table row
        
        // Schedule cell
        let tdSchedule = document.createElement('td')
        tdSchedule.innerText = `${course.schedule}` // Set the value as the text of the table cell
        tr.appendChild(tdSchedule) // Append the table cell to the table row

        // Enrollment cell
        let tdEnrollment = document.createElement('td')
        tdEnrollment.innerText = `${course.enrollment}/${course.capacity}` // Set the value as the text of the table cell
        tr.appendChild(tdEnrollment) // Append the table cell to the table row

        // Enrolled cell
        let tdEnrolled = document.createElement('button')
        if (course.student_enrolled == true) {
            tdEnrolled.innerText = `Drop`
            tdEnrolled.classList.add("btn-red")
        }
        else {
            tdEnrolled.innerText = `Add`
            tdEnrolled.classList.add("btn-green")
        }
        const courseid = course.c_id
        tdEnrolled.addEventListener('click', () => {
            registerOrDropCourses(courseid)
        })
        tr.appendChild(tdEnrolled) // Append the table cell to the table row

        tbody.appendChild(tr) // Append the table row to the table
    }

    table.appendChild(tbody) // Append new table body to table
}


function hideTables() {
  var registrationTable = document.getElementsByClassName('registrationTable')[0]
  var studentTable = document.getElementsByClassName('studentTable')[0]
  
  registrationTable.classList.add("hide")
  studentTable.classList.add("hide")
}


// GET API call to receive a student's registered courses
// Displays courses for registration
function displayRegisteredCourses() {
  var request = new XMLHttpRequest()
  const apiUrl = `${url}/student/${studentId}/c`
  request.open('GET', apiUrl, true)

  request.send()
  request.onload = function() {
    var jsonData = JSON.parse(this.responseText).payload
    hideTables()
    updateStudentTable(jsonData)
  }
}

// GET API call to receive courses for registration
function displayOfferedCourses() {
  var request = new XMLHttpRequest()
  const apiUrl = `${url}/student/${studentId}/r`
  request.open('GET', apiUrl, true)

  request.send()
  request.onload = function() {
    var jsonData = JSON.parse(this.responseText).payload
    hideTables()
    updateRegistrationTable(jsonData)
  }
}

function registerOrDropCourses(c_id) {
  var registeredCheck = new XMLHttpRequest()
  const apiUrl = `${url}/register/${studentId}/${c_id}`
  registeredCheck.open('PUT', apiUrl, true)

  registeredCheck.setRequestHeader('Content-Type', 'application/json')

  registeredCheck.onreadystatechange = function() {
    if (registeredCheck.readyState == 4) {
      if (registeredCheck.status == 200) {
        console.log(JSON.parse(registeredCheck.responseText).message)
        
      } else {
        console.error('Error: ' + registeredCheck.status)
      }
    }
  }
  registeredCheck.send()
  registeredCheck.onload = function() {
    if(registeredCheck.status == 200) {
      displayOfferedCourses();
    }
    else {
      window.alert("Registration Failed!")
    }
  }
}
