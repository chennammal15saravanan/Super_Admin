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

// ✅ Login Form Submission
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

// ✅ Sign-Up Form Submission
document.getElementById("signup-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("signup-username").value;
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;
  const confirmPassword = document.getElementById("signup-repassword").value;
  const termsAccepted = document.getElementById("terms").checked;

  if (!termsAccepted) {
    alert("❗ Please accept the Terms and Conditions.");
    return;
  }

  if (password !== confirmPassword) {
    alert("❌ Passwords do not match.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    const result = await response.json();

    if (result.status === "success") {
      alert("✅ " + result.message);
      showLogin(); // Show login form after signup
    } else {
      alert("❌ " + result.message);
    }

  } catch (error) {
    console.error("Signup error:", error);
    alert("⚠️ Failed to connect to the server.");
  }
});
