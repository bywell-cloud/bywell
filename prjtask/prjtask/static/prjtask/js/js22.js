document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#viewone').style.display = 'none';
    //document.getElementById(viewone).style.display = "none";
    document.querySelector('#viewall').style.display = 'block'; 
    document.querySelector('#btnright1').style.display = 'none';
    document.querySelector('#btnright').style.display = 'block';
    
})

function viewtasks()
{
 
    document.querySelector('#viewone').style.display = 'block';
    document.querySelector('#viewall').style.display = 'none';
    document.querySelector('#btnright1').style.display = 'block';
    document.querySelector('#btnright').style.display = 'none';
}
function viewtasksall() {
    
    document.querySelector('#viewone').style.display = 'none';
    document.querySelector('#viewall').style.display = 'block';
    document.querySelector('#btnright1').style.display = 'none';
    document.querySelector('#btnright').style.display = 'block';
}