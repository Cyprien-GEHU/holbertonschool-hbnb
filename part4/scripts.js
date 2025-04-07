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

document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();

  try{
    if (token && placeId){
     fetchPlaceDetails(token, placeId);
    }
  }catch (error) {
    console.error(error)
  }

})

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
  const loginLink = document.getElementById('login-button')

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
    const response = await fetch('http://127.0.0.1:5000/api/v1/places');
    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('try again:' + error );
  }
}

function displayPlaces(places) {
  const placeList = document.getElementById('places-list');
  placeList.innerHTML = '';

  places.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    placeCard.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: ${place.price}</p>
      <a href="place.html?id=${place.id}">
      <button class="details-button">More details</button>
      </a>
    `;
    placeList.appendChild(placeCard);
  });
}

document.getElementById('price-filter').addEventListener('change', () => {
  const selectPrice = document.getElementById('price-filter').value;
  const places = document.querySelectorAll('.place-card')

  places.forEach(card => {  
    const value = parseInt(card.querySelector('p').textContent.replace('Price: ', ''),10);

    if (selectPrice === 'all' || value <= parseInt(selectPrice, 10)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
  }
});
})

/* details places */
function getPlaceIdFromURL() {
  const placeID = new URLSearchParams(window.location.search);
  return placeID.get('id');

}

async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
    const dataPlace = await response.json();
    displayPlaceDetails(dataPlace);
  } catch (error) {
    console.error('try:' + error );
  }
}

function displayPlaceDetails(dataPlace) {
  document.getElementById('place-details').innerHTML = `
  <h1>${dataPlace.title}</h1>
  <p>Description: ${dataPlace.description}</p>
  <p>Price: ${dataPlace.price}</p>
  <p>Amenities: ${dataPlace.amenities.map(a => a.name).join(', ')}</p>
  <p>Review: ${dataPlace.reviews.map(a => a.text)}</p>
  `;

  const reviewPlace = document.getElementById('review');
  reviewPlace.innerHTML = "<h2> Reviews</h2>"

  dataPlace.reviews.forEach(rev => {
    const div = document.createElement('div')
    div.classList.add('review-card')
    div.innerHTML =`
      <p>${rev.text}</p>
      <p>${rev.rating}</p>
    `;
    reviewPlace.appendChild(div)
  });
}

/* add review */
async function submitReview(token, placeId, reviewText) {
  // Make a POST request to submit review data
  // Include the token in the Authorization header
  // Send placeId and reviewText in the request body
  // Handle the response
}

function handleResponse(response) {
  if (response.ok) {
      alert('Review submitted successfully!');
      // Clear the form
  } else {
      alert('Failed to submit review');
  }
}