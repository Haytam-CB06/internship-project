
window.addEventListener('DOMContentLoaded', () => {
  const signupButton = document.querySelector('.animated-button');

  signupButton.addEventListener('click', async function (e) {
    e.preventDefault(); 

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const cpassword = document.getElementById("comfrim_password").value;
    const role = document.getElementById("role").value;
    const admin_code = document.getElementById("admin_code").value;
    const termsChecked = document.getElementById("terms").checked;
    


    if (password !== cpassword) {
      alert("Passwords do not match!");
      return;
    }
     if (!termsChecked) {
    alert("You must agree to the terms and conditions to sign up.");
    return;
    }
    
    const data = {
      username,
      password,
      cpassword,
      role,
      admin_code
    };

    try {
      const response = await fetch('/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok) {
        alert(result.message || "Signup successful!");
        window.location.href = "/login";
      } else {
        alert(result.detail || "Signup failed.");
      }

    } catch (err) {alert("Request failed: " + err.message);}
  });
});
      var navlinks=document.getElementById("navlinks");
      function showmenu(){navlinks.style.right="0"; }

      function hidemenu(){navlinks.style.right="-200px";}

      let eyeicon = document.getElementById("eyeicon");
      let eye_icon = document.getElementById("eye_icon");
      let password = document.getElementById("password");
      let c_password=document.getElementById("comfrim_password")
      
      eyeicon.onclick=function show(){
        if (password.type == "password" || c_password=="password" ){
          password.type="text";
          c_password.type="text"
        }
        else {password.type="password";c_password.type="password"}
      }

