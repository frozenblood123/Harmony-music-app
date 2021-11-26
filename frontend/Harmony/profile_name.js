var user_curr = {
    "firstname": "veerabhadra",
    "lastname" : "Khandelot",
    "dob" : "12/03/2000",
    "email" : "veerigcse@gmail.com",
  };

var profile_name = document.querySelector("#user_fname").innerHTML;
// var profile_page_name = document.querySelector("#user_fname2").innerHTML;
// var email = document.querySelector("#email_field");

document.querySelector("#user_fname").innerHTML = profile_name.replace("Profile", user_curr.firstname);

// document.querySelector("#user_fname2").innerHTML = profile_page_name.replace("Name", user_curr.firstname);

// email.value = user_curr.email;

// onclick(){ document.querySelector("email_field").removeAttribute("readonly")};
