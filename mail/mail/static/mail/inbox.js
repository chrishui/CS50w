document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email
  document.querySelector('#compose-form').onsubmit = send_email;


  // By default, load the inbox
  load_mailbox('inbox');
});

// Compose mail
function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Load Mailbox
function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show selected mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // GET request to selected mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(data => {

    // Create div for each email
    data.forEach(element => {
      console.log(element);
      // Create div
      const div = document.createElement('div');
      // Div contents for 'inbox', read emails
      if (mailbox === 'inbox' && element.read === true){
        div.innerHTML = `
        <table id="indiv-email">
          <tr style="background-color: #ffffff;">
            <td id="sender">${element.sender}</td>
            <td id="subject">${element.subject}</td>
            <td id="timestamp">${element.timestamp}</td>
          </tr>
        `;
      }
      // Div contents for 'inbox', unread emails
      else if (mailbox === 'inbox' && element.read === false){
        div.innerHTML = `
        <table id="indiv-email">
          <tr style="background-color: #ddd;">
            <td id="sender">${element.sender}</td>
            <td id="subject">${element.subject}</td>
            <td id="timestamp">${element.timestamp}</td>
          </tr>
        `;
      }
      // Div contents for 'sent'
      else {
        div.innerHTML = `
        <table id="indiv-email">
          <tr>
            <td id="sender">${element.recipients}</td>
            <td id="subject">${element.subject}</td>
            <td id="timestamp">${element.timestamp}</td>
          </tr>
        `;
      }

      // Append div to emails-view
      document.querySelector('#emails-view').append(div);
    })
  })
}

// Send email
function send_email() {
  // Email details from user input
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // POST request to urls /emails route
  fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      // Display error message if there is error
      if ('error' in result) {
        document.querySelector('#message').innerHTML = result.error;
      }
      // Load user's sent mailbox once email has been sent
      else {
        load_mailbox('sent');
      }
    });

  // Stop form from submitting
  return false;

}
