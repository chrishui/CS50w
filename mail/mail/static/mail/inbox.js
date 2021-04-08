document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // Send email on submit
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load inbox
  load_mailbox('inbox');
});

// Compose email
function compose_email(email_id) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#indiv-email-view').style.display = 'none';

  // To compose email
  if (email_id === null) {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  // To reply to email
  else if (email_id) {
    // Get request for email info user will reply to
    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      console.log(`${email.subject}`)
      // Pre-populate recipient field
      document.querySelector('#compose-recipients').value = `${email.sender}`;
      // Pre-populate 'RE:' in subject field
      if (`${email.subject}`.includes("RE:")) {
        document.querySelector('#compose-subject').value =  `${email.subject}`;
      }
      else {
        document.querySelector('#compose-subject').value = `'RE: ${email.subject}'`;
      }
      // Pre-populate body field
      document.querySelector('#compose-body').value = `\n'On ${email.timestamp}' ${email.sender} wrote: ${email.body}`;
    });
  }
}

// Load Mailbox
function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#indiv-email-view').style.display = 'none';

  // Show selected mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // GET request to selected mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(data => {

    // Create 'div' for each email
    data.forEach(element => {
      console.log(element);
      // Create 'div'
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
          </table>
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
        </table>
        `;
      }
      // Div contents for 'archive', unread emails
      else if (mailbox === 'archive'){
        div.innerHTML = `
        <table id="indiv-email">
          <tr>
            <td id="sender">${element.sender}</td>
            <td id="subject">${element.subject}</td>
            <td id="timestamp">${element.timestamp}</td>
          </tr>
        </table>
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
        </table>
        `;
      }
      // Event handler when the div is clicked, views individual email
      div.addEventListener('click', () => check_email(element.id, mailbox));
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

// Check email
function check_email(email_id, mailbox) {
  // Hide mailboxs and show user's chosen email
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#indiv-email-view').style.display = 'block';

  // GET request to selected email
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Clear view element
    document.querySelector('#indiv-email-view').innerHTML = '';
    // Create div element for email details
    const div = document.createElement('div');
    div.innerHTML = `
    <p><strong>From:</strong>${email.sender}</p>
    <p><strong>To:</strong>${email.recipients}</p>
    <p><strong>Subject:</strong>${email.subject}</p>
    <p><strong>Timestamp:</strong>${email.timestamp}</p>
    <hr>
    <p>${email.body}</p>
    `;
    // Append indiviudal email div view
    document.querySelector('#indiv-email-view').append(div);

    // Archive button for 'inbox' or 'archive' mailboxes
    if (mailbox === 'inbox' || mailbox === 'archive') {
      var buttonDiv = document.createElement('div');

      // if email is not archived
      if (email.archived === false) {
        buttonDiv.innerHTML = `<button class="btn btn-sm btn-outline-primary">Archive</button>`;
        // Event handler when the button is clicked, archive email
        buttonDiv.addEventListener('click', () => {
          fetch(`/emails/${email_id}`,{
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
          // Load user's inbox
          load_mailbox('inbox');
        });
      }

      // Else, if email is archived
      else if (email.archived === true) {
        buttonDiv.innerHTML = `<button class="btn btn-sm btn-outline-primary">Unarchive</button>`;
        // Event handler when the button is clicked, archive email
        buttonDiv.addEventListener('click', () => {
          fetch(`/emails/${email_id}`,{
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
          // Load user's inbox
          load_mailbox('inbox');
        });
      }

      // 'Reply' button, redirects to compose email
      const replyButtonDiv = document.createElement('div');
      replyButtonDiv.innerHTML = `<button class="btn btn-sm btn-outline-primary">Reply</button>`;
      replyButtonDiv.addEventListener('click', () => { compose_email(email_id)});

      // Append 'Archive' and 'Reply' buttons
      document.querySelector('#indiv-email-view').append(buttonDiv);
      document.querySelector('#indiv-email-view').append(replyButtonDiv);
    }
  })

  // Mark email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}
