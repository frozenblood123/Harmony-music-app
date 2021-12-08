
document.writeln("<script type='text/javascript' src='https://unpkg.com/axios/dist/axios.min.js'></script>");

var user_curr = {
  "firstname": "veerabhadra",
  "lastname" : "Khandelot",
  "dob" : "12/03/2000",
  "email" : "veerigcse@gmail.com",
};
axios.post('http://localhost:90/get-user/', {
  "email": "harsh13092001@gmail.com"

}, {})
  .then(response => {
    user_response = response["data"];
    user_curr.firstname = user_response.firstname;
    user_curr.lastname = user_response.lastname;

    user_curr.email = user_response.email;
    user_curr.dob = user_response.dob;
    console.log(user_curr);

  })
  .catch(err1 => {
    console.log(err1);
  });




var profile_name = document.querySelector("#user_fname").innerHTML;
// var profile_page_name = document.querySelector("#user_fname2").innerHTML;
// var email = document.querySelector("#email_field");

document.querySelector("#user_fname").innerHTML = profile_name.replace("Profile", user_curr.firstname);

// document.querySelector("#user_fname2").innerHTML = profile_page_name.replace("Name", user_curr.firstname);

// email.value = user_curr.email;

// onclick(){ document.querySelector("email_field").removeAttribute("readonly")};
