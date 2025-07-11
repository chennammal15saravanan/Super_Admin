function showLogin() {
  document.getElementById("signup-form").classList.add("hidden");
  document.getElementById("login-form").classList.remove("hidden");
}

function showSignUp() {
  document.getElementById("login-form").classList.add("hidden");
  document.getElementById("signup-form").classList.remove("hidden");
}

document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  const response = await fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const result = await response.json();
  if (result.status === "success") {
    alert(result.message);
    window.location.href = "/dashboard";
  } else {
    alert(result.message);
  }
});

