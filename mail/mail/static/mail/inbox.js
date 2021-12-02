document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));

  
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#error-view').style.display = 'none';
  document.querySelector('#opening-mail').style.display = 'none';
  document.querySelector('#reply-mail').style.display = 'none';
  document.querySelector('#archive').style.display = 'none';
  
  
  // Clear out composition fields1
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#error-view').value = '';
  

  document.querySelector('#compose-form').onsubmit = function() {
    recipients = document.querySelector('#compose-recipients').value ;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients:recipients, 
          subject:subject, 
          body: body
          
    })
  })
    .then(response => response.json())
    .then(result => {
      
      console.log(result);
      
      load_mailbox('sent');
    });
    return false;
}
}

     


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#error-view').style.display = 'block';
  document.querySelector('#opening-mail').style.display = 'none';
  document.querySelector('#reply-mail').style.display = 'none';
  document.querySelector('#archive').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(mailbox);
    console.log(emails);
    var items1 = document.getElementById('error-view');
    

    if (emails.length == 0){    

      items1.innerHTML = `Empty ${mailbox}`;
    }
    else {

    }
    
    
    emails.forEach(element => {
      console.log(element);
      if(mailbox == "sent"){
        from_to = element.recipients;
        to = "To: ";
      }
      else{
        from_to = element.sender;
        to="";
      }
      if(mailbox == "inbox"){
        
          document.querySelector("#error-view").style.display = "block";
       
       
      
        if(element.read){class_read = "card bg-secondary text-dark  border-dark";
          
      
      }
        else{class_read = "card  text-dark border-dark";
        
      }
      }
      else{class_read = "card  text-dark border-dark"; 
       // let itemread =" card  text-dark items border-dark";
      
    }
      var item = document.createElement("DIV");
      item.className = `${class_read}`;
     // var item = document.createElement("DIV");
      item.innerHTML = `  <div class="card-body">
      <b>${to}</b><b>${from_to}</b> &nbsp &nbsp | &nbsp <b>Sub: </b> ${element.subject} &nbsp &nbsp | &nbsp ${element.timestamp}
      </div>`;
      document.querySelector('#error-view').style.display = 'none';
      document.querySelector("#emails-view").appendChild(item);
      item.addEventListener("click",()=>{
           open_mail(element.id,mailbox);
      });
    }); 
  });
}

function open_mail(id , mailbox) 
{
   // Show the Email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#error-view').style.display = 'none';
  document.querySelector('#opening-mail').style.display = 'block';
  document.querySelector('#reply-mail').style.display = 'none';
  document.querySelector('#archive').style.display = 'none';
   
   
   // Show the Email
  document.querySelector('#opening-mail').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(emails => 
    {
    document.querySelector('#reply-mail').innerHTML = "";
    document.querySelector('#archive').innerHTML = "";
    console.log(mailbox);
    console.log(emails);
    document.querySelector('#opening-mail').innerHTML = `
      <b>From: </b> ${emails.sender}
      <br>
      <b>To: </b> ${emails.recipients}
      <br>
      <b>Subject: </b> ${emails.subject}
      <br>
      <b>Time: </b> ${emails.timestamp}
      <br>
      <b>Body: </b> ${emails.body}
      <br><br>`

      if (mailbox=="archive")
      {
        document.querySelector('#archive').style.display = 'block';
        unarchived = document.createElement("button");
        unarchived.textContent  = "unarchive";
        unarchived.className= "btn btn-outline-primary";
        unarchived.addEventListener('click', ()=> 
        {
          fetch(`/emails/${id}`,
          {
            method: 'PUT',
            body: JSON.stringify(
            {
              archived: false ,
               
            })
          })
          .then (console.log("emails"))
          load_mailbox(mailbox);

        })
        document.querySelector('#archive').append(unarchived); 

        
        return false ;

      }


    if (mailbox==="inbox") 
    {

      document.querySelector('#reply-mail').style.display = 'block';

      reply = document.createElement("button");
      reply.textContent  = "Reply";
      reply.className= "btn btn-outline-success";
      reply.addEventListener('click', function() 
      {
        replyemail(emails);
      });
      
      document.querySelector('#reply-mail').append(reply);
      //return false;


      document.querySelector('#archive').style.display = 'block';
      archive = document.createElement("button");
      archive.textContent  = "archive";
      archive.className= "btn btn-outline-primary";
      archive.addEventListener('click', ()=> 
      {
        fetch(`/emails/${id}`,
        {
          method: 'PUT',
          body: JSON.stringify(
            {
              archived: true
            })
        })
        load_mailbox(mailbox);
       // .then (console.log("email2"))
      });  
      document.querySelector('#archive').append(archive);
      
    
  
      //document.querySelector('#reply-mail').style.display = 'none';
      fetch(`/emails/${id}`,
      {
        method: 'PUT',
        body: JSON.stringify(
          {
        read:true
          })

      })
      .then (console.log("email2"))

      return false;
    }
  })
}
  
function replyemail(emails) {

   // Show reply view and hide other views
   document.querySelector('#emails-view').style.display = 'none';
   document.querySelector('#compose-view').style.display = 'block';
   document.querySelector('#error-view').style.display = 'none';
   document.querySelector('#opening-mail').style.display = 'none';
   document.querySelector('#reply-mail').style.display = 'none';
   document.querySelector('#archive').style.display = 'none';
   
   
   
 
   document.querySelector('#compose-recipients').value = emails.sender;

   if (emails.subject.slice(0,4) =="Re: "){
      document.querySelector('#compose-subject').value = emails.subject;
   }
   else {

      document.querySelector('#compose-subject').value = 'Re: '+ emails.subject;
   }
   document.querySelector('#compose-body').value = 'On ' + emails.timestamp +''+ emails.recipients + ' wrote: \n' + emails.body + '\n'+'\n';
   document.querySelector('#error-view').value = '';
   
 }
 
 
function archive(id) {

}



