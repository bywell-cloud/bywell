document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#viewone').style.display = 'none';
    //document.getElementById(viewone).style.display = "none";
    document.querySelector('#viewall').style.display = 'block'; 
    document.querySelector('#btnright1').style.display = 'none';
    document.querySelector('#btnright').style.display = 'block';
    document.querySelector('#pall').style.display = 'block';
    document.querySelector('#btnrightspecific').style.display = 'none';
    document.querySelector('#btnrightall').style.display = 'block';
    document.querySelector('#pone').style.display = 'none';
    document.querySelector('#searchaall').style.display = 'block';
    document.querySelector('#searchspecific').style.display = 'none';
})
function search(){
    document.querySelector('#btnrightspecific').style.display = 'block';
    document.querySelector('#btnrightall').style.display = 'none';





    
    document.querySelector('#searchspecific').style.display = 'block';
    document.querySelector('#searchaall').style.display = 'none';
}
function searchaall(){
    document.querySelector('#btnrightspecific').style.display = 'none';
    document.querySelector('#btnrightall').style.display = 'block';
    document.querySelector('#searchspecific').style.display = 'none';
    document.querySelector('#searchaall').style.display = 'block';
}

function viewtasks()
{
    document.querySelector('#pone').style.display = 'block'; 
    document.querySelector('#pall').style.display = 'none';
    document.querySelector('#viewone').style.display = 'block';
    document.querySelector('#viewall').style.display = 'none';
    document.querySelector('#btnright1').style.display = 'block';
    document.querySelector('#btnright').style.display = 'none';
}
function viewtasksall() {
    document.querySelector('#pall').style.display = 'block';
    document.querySelector('#pone').style.display = 'none';
    document.querySelector('#viewone').style.display = 'none';
    document.querySelector('#viewall').style.display = 'block';
    document.querySelector('#btnright1').style.display = 'none';
    document.querySelector('#btnright').style.display = 'block';
}