
document.writeln("<script type='text/javascript' src='https://unpkg.com/axios/dist/axios.min.js'></script>");




function get_user_profile() {
  var user_curr_ = {
    "firstname": "Harsh",
    "lastname": "Malani",
    "email": "harsh13092001@gmail.com",
    "dob": "13-09-2001",
  };
axios.post('http://localhost:90/get-user/', {
  "email": "harsh13092001@gmail.com"

}, {})
  .then(response => {


    user_response = response["data"];
    user_curr_["firstname"] = user_response["firstname"];
    user_curr_.lastname = user_response.lastname;

    user_curr_.email = user_response.email;
    user_curr_.dob = user_response.dob;


  })
  .catch(err1 => {
    console.log(err1);
  });
  return user_curr_;
}

var user_curr;
user_curr = get_user_profile();
console.log(user_curr.firstname);
var profile_name = document.querySelector("#user_fname").innerHTML;
// var profile_page_name = document.querySelector("#user_fname2").innerHTML;
// var email = document.querySelector("#email_field");

document.querySelector("#user_fname").innerHTML = profile_name.replace("Profile", user_curr.firstname);

// document.querySelector("#user_fname2").innerHTML = profile_page_name.replace("Name", user_curr.firstname);

// email.value = user_curr.email;

// onclick(){ document.querySelector("email_field").removeAttribute("readonly")};
