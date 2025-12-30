/* Glow Ecommerce - Global JavaScript Helper Library
   Handles Authentication, API Requests, Simple UI Interactions
   Place this script in all pages before their per-page JS!
*/

// ==== CONFIG ====
const API_BASE = 'http://localhost:8000/api';

// ==== AUTH ====
function saveToken(token) {
  localStorage.setItem('access_token', token);
}

function getToken() {
  return localStorage.getItem('access_token');
}

function clearToken() {
  localStorage.removeItem('access_token');
}

function isLoggedIn() {
  return !!getToken();
}

// Fetch and parse JWT user payload (if you want to use for navbar/profile)
function parseJwt(token) {
  if (!token) return null;
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
}

// ==== API Request Helper ====
/*
  apiRequest(endpoint, method, data, auth)
    - endpoint: e.g. '/products/'
    - method: 'GET', 'POST', etc.
    - data: object (will be sent as JSON)
    - auth: true/false (attach Bearer token?)

  Returns: Promise with parsed response, throws error if status not ok
*/
async function apiRequest(endpoint, method='GET', data=null, auth=false) {
  let url = API_BASE + endpoint;
  let options = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (auth && getToken()) {
    options.headers['Authorization'] = 'Bearer ' + getToken();
  }
  if (data) {
    options.body = JSON.stringify(data);
  }
  let res = await fetch(url, options);
  if (!res.ok) {
    let err;
    try {
      err = await res.json();
    } catch {
      err = { detail: 'Unknown error. Please try again.' }
    }
    throw new Error(err.detail || 'Error');
  }
  if (res.status === 204) return null; // No content
  return res.json();
}

// ==== AUTH API ====
async function login(email, password) {
  // Your API expects {username, password} as form data, not JSON!
  const form = new URLSearchParams();
  form.append('username', email);
  form.append('password', password);
  const res = await fetch(API_BASE + '/auth/login', {
    method: 'POST',
    body: form
  });
  if (!res.ok) {
    let err = await res.json();
    throw new Error(err.detail || 'Login failed');
  }
  return res.json();
}

async function register(userData) {
  // userData: { first_name, last_name, email, password }
  return apiRequest('/auth/register', 'POST', userData, false);
}

// ==== LOGOUT ====
function logout() {
  clearToken();
  window.location.href = 'login.html';
}

// ==== GLOBAL NAVBAR UI ====
function showUserNav() {
  const loginLink = document.getElementById('nav-login');
  const registerLink = document.getElementById('nav-register');
  const userMenu = document.getElementById('nav-user');
  if (isLoggedIn()) {
    if (loginLink) loginLink.style.display = 'none';
    if (registerLink) registerLink.style.display = 'none';
    if (userMenu) userMenu.style.display = '';
  } else {
    if (loginLink) loginLink.style.display = '';
    if (registerLink) registerLink.style.display = '';
    if (userMenu) userMenu.style.display = 'none';
  }
}

// Call on every page load in per-page JS:
//   document.addEventListener('DOMContentLoaded', showUserNav);

// ==== LOADER ====
function showLoader(id) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = '<div class="loader"></div>';
}
function hideLoader(id) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = '';
}

// ==== ERROR/SUCCESS MESSAGES ====
function showError(id, msg) {
  const el = document.getElementById(id);
  if (el) {
    el.innerHTML = `<div class="error-message">${msg}</div>`;
    el.style.display = '';
  }
}
function showSuccess(id, msg) {
  const el = document.getElementById(id);
  if (el) {
    el.innerHTML = `<div class="success-message">${msg}</div>`;
    el.style.display = '';
  }
}
function clearMessage(id) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = '';
}

// ==== REDIRECT IF NOT LOGGED IN (for protected pages) ====
function requireLogin() {
  if (!isLoggedIn()) {
    window.location.href = 'login.html';
  }
}

export {
  API_BASE, saveToken, getToken, clearToken, isLoggedIn, parseJwt,
  apiRequest, login, register, logout,
  showUserNav, showLoader, hideLoader, showError, showSuccess, clearMessage, requireLogin
};