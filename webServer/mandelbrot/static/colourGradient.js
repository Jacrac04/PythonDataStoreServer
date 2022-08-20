
function createGradient(colours, interpolation="linear", numOfColours=256){
    let X = [];
    let amountOfColours = colours.length;
    for (var i=0; i<amountOfColours; i++){
        X[i] = i/(amountOfColours-1)
    }
    let Y = [[], [], []];
    for (var i=0; i<3; i++){
        for (var j = 0; j<amountOfColours; j++){
            Y[i][j] = colours[j][i];
        }
    }
    let nums = [];
    for (var i=0; i<numOfColours; i++){
        nums[i] = i * (1/numOfColours);
    }
    let grad = [[], [], []];
    grad[0] = everpolate.linear(nums, X, Y[0]);
    grad[1] = everpolate.linear(nums, X, Y[1]);
    grad[2] = everpolate.linear(nums, X, Y[2]);
    let gradient = [];
    for (var i=0; i<grad[0].length; i++){
        gradient[i] = [grad[0][i]*256, grad[1][i]*256, grad[2][i]*256];
    }
    return gradient;

}
function getColours(){
    let colours = [];
    const colContainer = document.getElementById("colours");
    const cols = colContainer.children;
    for (var i=0; i<cols.length; i++){
        color = cols[i].value
        const r = parseInt(color.substr(1,2), 16)
        const g = parseInt(color.substr(3,2), 16)
        const b = parseInt(color.substr(5,2), 16)
        colours[i] = [r/256, g/256, b/256];
    }
    return colours;

}


