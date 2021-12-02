document.addEventListener('DOMContentLoaded', function() {
   
    document.querySelector('#searchaall').style.display = 'block'; 
    
})
function search() {
  document.querySelector('#searchaall').style.display = 'none';
  
  id=form1.elements["stxt"].value;
  fetch(`/search/${id}`)
    .then(response => response.json())
    .then(task => {
  
       // var itemt = document.createElement("DIV");
        document.querySelector('#tb').innerHTML = `<table class="table" width="100%">
        <tr bgcolor="#00cc33"  id ="searchspecific">
            <font color="#ffffff">
                <th width='8%' > Name</th>
                
                
                <th width='16%'>Description</th>
                <th width='14%'>Expected to Start</th>
                <th width='14%'>Due Date</th>
                <th width='8%'>Project</th>
                <th width='6%'>Assiged By</th>
                
                <th width='6%'>%Progress</th>
                <th width='7%'>Progress/<br>Problems</th>
                <th width='12%'>Status</th>
                <th width='17%'>Action</th>
    
    
            </font>
        
        </tr>
        
                 
    
    </table>`;
    document.querySelector("#second").innerHTML = `<h6></h6>`;
    document.querySelector("#second").value=" ";
      
      task.forEach(element => {
      
        console.log(element);
       
        var item = document.createElement("DIV");
           item.innerHTML = `<table class="table" width="100%">
           <tr>
               <td width='8%'>${element.name}</td>
               <td width='16%'>${element.t_description}</td>
               <td width='16%'>${element.start_time}</td>
               <td width='16%'>${element.expected_end}</td>
               <td width='8%'>${element.project}</td>
               <td width='8%'>${element.tuser}</td>
               
               
               <td width="9%"><div class='progress'>
                  <div class='progress-bar' role='progressbar' aria-valuenow='${element.status}'
                  aria-valuemin='0' aria-valuemax='100' style='width:${element.status}%'>
              </div>
          </div>${element.status}% Done</td><td><!-- Modal HTML embedded directly into document -->
          <div id="ex1${element.id}" style="display:none;">
              <textarea readonly class="form-control"> ${element.progress} </textarea> <a href="#" rel="modal:close">Close</a> or press ESC</p>
            </div>     
          <!-- Link to open the modal -->
          <p><a href="#ex1${element.id}" rel="modal:open">View</a></p><td>
               <td width="12%">${element.chck} </td>
               <td width = '17%'><a href='action/${element.id}' class='btn-outline-success'>Update Progress <hr></a>
                  </td>
               
            </tr>   </table>
               
             
      `;
      
    document.querySelector('#searchaall').style.display = 'none';
    document.querySelector("#second").appendChild(item);
      
    });
    
}) 

    
}    