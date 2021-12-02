document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#searchspecific').style.display = 'none';
    document.querySelector('#searchaall').style.display = 'block'; 
    //document.querySelector('#btnright1').style.display = 'none';
    //document.querySelector('#btnright').style.display = 'block';
})
function search(id) {
    fetch(`/search/${id}`,{
        
        method="GET"

        
    })
    .then(response => response.json())
    .then(stask => {
  
      
      
      stask.forEach(element => {
        console.log(element);
        var item = document.createElement("DIV");
     // item.className = `${class_read}`;
     // var item = document.createElement("DIV");
      item.innerHTML = `  <div>
      <b>1</b><b>-</b> &nbsp &nbsp | &nbsp <b>Sub: </b> ${element.name} &nbsp &nbsp | &nbsp ${element.status}
      </div>`;
     document.querySelector('#searchspecific').style.display = 'none';
    document.querySelector('#searchaall').style.display = 'none';
      document.querySelector("#view").appendChild(item);
      
    }); 

    
}    