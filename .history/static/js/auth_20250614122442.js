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

function showToast(message, type = "success") {
  let emoji = "";
  let bgColor = "";

  if (type === "success") {
    emoji = "✅";
    bgColor = "#0d6efd";  // Blue
  } else if (type === "error") {
    emoji = "❌";
    bgColor = "#dc3545";  // Red
  } else if (type === "warning") {
    emoji = "⚠️";
    bgColor = "#ffc107";  // Yellow
  }

  Toastify({
    text: `${emoji} ${message}`,
    duration: 3000,
    gravity: "top",
    position: "right",
    backgroundColor: bgColor,
    close: false // ❌ Hides the close button
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
