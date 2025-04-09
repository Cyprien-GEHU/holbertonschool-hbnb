document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const reviewForm = document.getElementById('review-form');
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();
  
  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
              
      const text = document.getElementById('review').value;
      const rating = document.getElementById('rating').value;
  
      try {
        submitReview(token, placeId, text, rating);
      } catch (error) {
        console.error(error)
      }
    });
  }
});

/* Check if we have token and */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-button')
  const logoutLink = document.getElementById('logout-button')
  
  if (!token) {
    loginLink.style.display = 'block';
    logoutLink.style.display = 'none';
  } else {
    loginLink.style.display = 'none';
    logoutLink.style.display = 'block';
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

async function submitReview(token, placeId, reviewText, rating) {
  try {
    console.log(token);
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: reviewText,
        rating: parseInt(rating, 10),
        place_id: placeId
      }),
    });
  
    handleResponse(response)
  } catch (error) {
    console.error('bonjour:' + error );
  }
}
  
function handleResponse(response) {
  if (response.ok) {
    alert('Review submitted successfully!');
    document.getElementById('review-form').reset();
  } else {
    alert('Failed to submit review');
  }
}