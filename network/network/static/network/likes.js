

function upedit(id) { 
 content = document.querySelector(`#post${id}`).value;
 document.querySelector('#newp').innerHTML = `${content}`;
 document.querySelector('#newp').focus();
 document.querySelector('#eddiv').style.display = 'block';
 edit1 = document.createElement("button");
      edit1.textContent  = "Edit Submit";
      edit1.className= "btn btn-outline-success";
      
      document.querySelector('#sub').style.display = 'none';
      edit1.addEventListener('click', function() 
    {
        document.querySelector('#fid').onsubmit = function() 
    {
            
        content = document.querySelector('#newp').value;
        document.querySelector('#postid').value=id;
}
})
document.querySelector('#fid').append(edit1);
}

function lik(id) {

  fetch(`/likesadd/${id}`)
  .then(response => response.json())
  .then(result => {
    
      let l1 = document.querySelector(`#total${id}`);
      let count = result.likes;
      l1.innerHTML = `Likes: ${count}`;
  });
  // Updating button
  let lbtn0 = document.querySelector(`#a${id}`);
  lbtn0.id = `una${id}`;
  lbtn0.onclick = function() {
      unlik(id);
  }
  lbtn0.innerHTML = '<img src="/static/network/images/likes.png" alt="likes" width="18" height="19"> Like';
 
}


function unlik(id) {

fetch(`/likesadd/${id}`)
  .then(response => response.json())
  .then(result => {
      
      let l1 = document.querySelector(`#total${id}`);
      let count = result.likes;
      l1.innerHTML = `Likes: ${count}`;
  });
  // Updating button
  let lbtn0 = document.querySelector(`#una${id}`);
  lbtn0.id = `a${id}`;
  lbtn0.onclick = function() {
      lik(id);
  }
  lbtn0.innerHTML = '<img src="/static/network/images/likes2.png" alt="likes" width="18" height="19">UnLike';
 }

 