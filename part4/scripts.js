/* login part*/
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;
          try {
            await loginUser(email, password);
          } catch (error) {
            console.log('Error:', error);
          }
      });
  }
  });

async function loginUser(email, password) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
  
}

/* check user part*/
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-button');

  if (!token) {
      loginLink.style.display = 'block';
  } else {
      loginLink.style.display = 'none';
      // Fetch places data if the user is authenticated
      fetchPlaces(token);
  }
}
function getCookie(name) {
  const cookie = document.cookie
  .split("; ")
  .find((row) => row.startsWith(name))
  ?.split("=")[1];
  return cookie
}

/* place part*/
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/');
    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('try again:' + error );
  }
}

function displayPlaces(places) {
  const placeList = document.getElementById('place');
  placeList.innerHTML = '';

  places.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    placeCard.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price ${place.price}</p>
      <button class="details-button">More details</button}
    `;
    placeList.appendChild(placeCard);
  });
}
