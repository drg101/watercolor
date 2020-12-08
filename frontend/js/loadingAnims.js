/**
* Builds the request then auto-calls @function makeRequest
* This is called by the request button
* @function setLoading
* @param {boolean} loading is the client loading something?  
* @returns {boolean} true if successful
*/
function setLoading(loading){
    //document.getElementById("loader").style.display = loading ? "block" : "none";
    document.getElementById("loader").style.left = loading ? 0 : window.innerWidth;
}