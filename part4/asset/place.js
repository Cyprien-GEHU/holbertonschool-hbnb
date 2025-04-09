document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();
  try {
      if (token && placeId)  {
       fetchPlaceDetails(token, placeId);
      }
    }catch (error) {
      console.error(error)
    }
})

/* Check if we have token and */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-button')

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
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
    <h1>${dataPlace.title}</h1>
    <p>Description: ${dataPlace.description}</p>
    <p>Price: ${dataPlace.price}</p>
    <p>Amenities: ${dataPlace.amenities.map(review => review.name).join(', ')}</p>
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
  document.getElementById('add-review').innerHTML = `
    <a href="add_review.html?id=${dataPlace.id}">
    <button type="submit" class="button-review">Add Review</button>
    </a>
  `;
}