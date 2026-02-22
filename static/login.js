var navlinks=document.getElementById("navlinks");
      function showmenu(){navlinks.style.right="0";}
      function hidemenu(){navlinks.style.right="-200px"; }

      let eyeicon = document.getElementById("eyeicon");
      let password = document.getElementById("password");
      
      eyeicon.onclick=function show(){
        if (password.type == "password"){
          password.type="text";
          eyeicon.src="eye-open.png";
        }
        else {password.type="password"}}


async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"  // 👈 tells FastAPI it's JSON
       },
    body: JSON.stringify({ username, password })  // 👈 sends JSON
  });

  const result = await response.json();

  if (response.ok) {
    if (result.role === "admin") {
      window.location.href = "/test";
    } else if (result.role === "user"){
      window.location.href = "/user_dashboard";
    }
  }  else {
    alert(result.message );
  }
};