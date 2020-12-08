let isLoading = false;
let maxLoads = 0;
/**
* Builds the request then auto-calls @function makeRequest
* This is called by the request button
* @function setLoading
* @param {int} numLoads how many things are we waiting for
* @returns {boolean} true if successful
*/
function setLoading(numLoads){
    isLoading = numLoads > 0;
    document.getElementById("loader").style.left = isLoading ? 0 : window.innerWidth;
    document.getElementById("loadLabel").innerHTML = `We are upscaling your images, this may take a moment. ${this.maxLoads - numLoads} / ${this.maxLoads} Images have finished processing.`;
}

function setMaxLoads(maxLoads){
    this.maxLoads = maxLoads;
}

document.getElementById("loader").style.left = window.innerWidth;

window.addEventListener('resize', function(event){
    if(!isLoading)
        document.getElementById("loader").style.left = window.innerWidth;
});
