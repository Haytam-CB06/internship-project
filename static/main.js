// GET data from FastAPI and display it
/*function fetchData() {
  fetch('/api/data',{
    method: 'POST',
  headers: {
    'Content-Type': 'application/json',  
  },
  body: JSON.stringify({ text: 'your data here' }),
})
  .then(response => response.json())
    .then(data => {
      document.getElementById('get-result').innerText =
        `Message: ${data.message}, Items: ${data.items.join(', ')}`;
    })
    .catch(error => console.error('Error fetching data:', error));
}

// POST data from input to FastAPI
function postData() {
  const input = document.getElementById('inputData').value;

  fetch('/api/data', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ userInput: input })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('post-result').innerText =
      `Server response: ${JSON.stringify(data)}`;
  })
  .catch(error => console.error('Error posting data:', error));
}
function loadSignupForm() {
  fetch('/signup-form')
    .then(response => response.text())
    .then(html => {
      document.getElementById('form-sign').innerHTML = html;
    })
    .catch(error => {
      console.error('Error loading form:', error);
    });
}*/