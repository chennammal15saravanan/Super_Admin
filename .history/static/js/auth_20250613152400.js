import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://YOUR_PROJECT_ID.supabase.co';
const SUPABASE_ANON_KEY = 'YOUR_ANON_KEY';
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

function showLogin() {
  document.getElementById("signup-form").classList.add("hidden");
  document.getElementById("login-form").classList.remove("hidden");
}

function showSignUp() {
  document.getElementById("login-form").classList.add("hidden");
  document.getElementById("signup-form").classList.remove("hidden");
}



  const result = await response.json();
  if (result.status === "success") {
    alert(result.message);
    window.location.href = "/dashboard";
  } else {
    alert(result.message);
  }
});
