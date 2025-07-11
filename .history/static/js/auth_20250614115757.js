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

// ✅ Toast Notification Function
function showToast(message, type = "success") {
  Toastify({
    text: message,
    duration: 3000,
    gravity: "top",
    position: "center",
    backgroundColor: type === "success" ? "white" : "#FF4C4C",
    close: true,
  }).showToast();
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
      showToast(result.message, "success");
      setTimeout(() => window.location.href = "/dashboard", 1500);
    } else {
      showToast(result.message, "error");
    }

  } catch (error) {
    console.error("Login error:", error);
    showToast("⚠️ Failed to connect to the server.", "error");
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
    showToast("❗ Please accept the Terms and Conditions.", "error");
    return;
  }

  if (password !== confirmPassword) {
    showToast("❌ Passwords do not match.", "error");
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
      showToast("✅ You're all set! Registration successful.", "success");
      setTimeout(() => showLogin(), 1500);
    } else {
      showToast("❌ " + result.message, "error");
    }

  } catch (error) {
    console.error("Signup error:", error);
    showToast("⚠️ Failed to connect to the server.", "error");
  }
});
