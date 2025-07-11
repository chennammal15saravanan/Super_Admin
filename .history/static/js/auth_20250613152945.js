// Show Login Form
function showLogin() {
  document.getElementById("signup-form").classList.add("hidden");
  document.getElementById("login-form").classList.remove("hidden");
}

// Show Sign-Up Form
function showSignUp() {
  document.getElementById("login-form").classList.add("hidden");
  document.getElementById("signup-form").classList.remove("hidden");
}

// Login Form Submission
document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  try {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    if (result.status === "success") {
      alert("✅ " + result.message);
      window.location.href = "/dashboard";  // Redirect to dashboard
    } else {
      alert("❌ " + result.message);
    }

  } catch (error) {
    console.error("Login error:", error);
    alert("⚠️ Failed to connect to the server.");
  }
});
