document.addEventListener('DOMContentLoaded',checkAuthentication());

/* Check if we have token and */
function checkAuthentication() {
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();
  const loginLink = document.getElementById('login-button')
  const logoutLink = document.getElementById('logout-button')

  if (!token) {
    loginLink.style.display = 'block';
    logoutLink.style.display = 'none';
  } else {
    loginLink.style.display = 'none';
    logoutLink.style.display = 'block';
    fetchPlaceDetails(token, placeId);
  }

  if (logoutLink) {
    logoutLink.addEventListener("click", function (event) {
      event.preventDefault(); 
      deleteCookie();
      window.location.href = "login.html"; 
    });
  }
}

/* function to get the token */
function getCookie(name) {
  const cookie = document.cookie
  .split("; ")
  .find((row) => row.startsWith(name))
   ?.split("=")[1];
  return cookie
}

function deleteCookie(){
  document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

/* Get the place id with the url*/
function getPlaceIdFromURL() {
  const placeID = new URLSearchParams(window.location.search);
  return placeID.get('id');
}

/* the function request to the backend to get the place with the id of the place */
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
    const dataPlace = await response.json();
    displayPlaceDetails(dataPlace);
  } catch (error) {
    console.error('try:' + error );
  }
}

/* the function display all details of the place */
function displayPlaceDetails(dataPlace) {
  document.getElementById('place-details').innerHTML = `
    <h1 class="title-card">${dataPlace.title}</h1>
    <p class="space-card">Description: ${dataPlace.description}</p>
    <p class="space-card">Price: ${dataPlace.price} euros per night</p>
    <p class="space-card">Amenities: ${dataPlace.amenities.map(review => review.name).join(', ')}</p>
  `;
  
  const reviewPlace = document.getElementById('review');
  reviewPlace.innerHTML = "<h2> Reviews</h2>"
  
  if (dataPlace.reviews && dataPlace.reviews.length > 0) {
    dataPlace.reviews.forEach(rev => {
      user(rev)
  });
  } else {
    reviewPlace.innerHTML += '<p id="noReview">On a pas de review pour le moment</p>'
  }

  document.getElementById('add-review').innerHTML = `
    <a href="add_review.html?id=${dataPlace.id}">
    <button type="submit" class="button-review">Add Review</button>
    </a>
  `;
}

async function user(rev) {
  const reviewPlace = document.getElementById('review');
  const data = await fetch(`http://127.0.0.1:5000/api/v1/users/${rev.user_id}`);
  const user = await data.json();
  const div = document.createElement('div')
    div.classList.add('review-card')
    div.innerHTML =`
    <p class="user-review">${user.first_name} ${user.last_name}:</p>
    <p class="space-card">${rev.text}</p>
    <p class="space-card">Rating: ${rev.rating}&starf;</p>
  `;
  reviewPlace.appendChild(div)
}