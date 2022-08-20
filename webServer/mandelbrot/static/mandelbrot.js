// ------ OLD CODE NOT USED ------
function notInf(c, ittr_num) {
    /* Function to check if a complex number point goes to infinity.
    Takes a complex number and the number of iterations as the arguments.
    Returns true if the number doesn't go to infinity, false otherwise. */
    var z = 0;
    for (var _ = 0; _ < ittr_num; _++) {
        z = math.add((math.multiply(z,z)),  c);  // z = z^2 + c
    }
    return Math.abs(z) <= 2; // if abs(z) > 2, then it goes to infinity
}

function point_where_dips(self, c) {
    var z = 0;
    for (var ittr = 0; ittr < self.max_ittr; ittr++) {
        z = math.add((math.multiply(z,z)),  c);
        if (Math.abs(z) >= 2) {
            return ittr;
        }
    }
    return ittr;
}
// --- END OF OLD CODE NOT USED ---


/* Class MandelbrotSet */
class MandelbrotSet {
    constructor(max_ittr, escape_radius) {
        /* Constructor for the MandelbrotSet class. 
        Takes the maximum number of iterations and the escape radius as the arguments. */
        this.max_ittr = max_ittr;
        this.escape_radius = escape_radius;
    }

    contains(c) {
        /* Function to check if a complex number point is in the Mandelbrot set.
        Takes a complex number as the argument.
        Returns true if the number is in the set, false otherwise. */
        return this.stability(c) == 1;
    }

    stability(c) {
        /* Function to get the stability of a complex number point.
        Takes a complex number as the argument.
        Returns a number between 0 and 1, where 1 is stable (in the set) and 0 is unstable. */
        return this.point_where_dips(c) / this.max_ittr;
    }

    point_where_dips(c) {
        /* Function to get the number of iterations until a complex number point goes past the escape radius.
        Takes a complex number as the argument.
        Returns the number of iterations taken before passing the escape radius or the max iteration if it reaches that first. */
        let z = 0;

        for (let ittr = 0; ittr < (this.max_ittr +1 ); ittr++) {
            // Repeatedly performs z = z^2 + c until the point goes past the escape radius or it reaches the max iteration.
            z = math.add((math.multiply(z,z)),  c); // z = z^2 + c
            if (this.abs(z) >= this.escape_radius) { // if abs(z) > escape_radius, then it goes past the escape radius
                return ittr; // return the number of iterations taken before passing the escape radius
            }
        }

        return this.max_ittr; // if it reaches the max iteration, then it does not go past the escape radius
    }

    abs(c) {
        /* Function to get the absolute value of a complex number.
        Takes a complex number as the argument.
        Returns the absolute value of the complex number. */
        return math.sqrt((math.re(c)) * (math.re(c)) + (math.im(c)) * (math.im(c))); // sqrt(re^2 + im^2)
    }
}

/* Class ImageMgr 
This is used to manage the actual drawing and representation of the Mandelbrot set*/
class ImageMgr {
    constructor(canvas, center, width) {
        /* Constructor for the ImageMgr class.
        Takes the canvas element and the center and width of the imageMgr as the arguments. */
        this.image = canvas;
        this.context = canvas.getContext("2d");
        this.center = center;
        this.width = width;
    }

    get height() {
        /* Function to get the height of the imageMgr.
        Returns the height of the imageMgr. */
        return this.scale * this.image.height;
    }
    get offset() {
        /* Function to get the offset of the imageMgr.
        Returns the offset of the imageMgr. */
        return math.multiply(math.add(this.center, math.complex(-this.width, this.height)), 0.5); // (center + (-width, height)) * 0.5
    }
    get scale() {
        /* Function to get the scale of the imageMgr.
        Returns the scale of the imageMgr. */
        return this.width / this.image.width;
    }

    *[Symbol.iterator]() {
        /* Function to get an iterator for the imageMgr.
        Returns an iterator for the imageMgr made up of the Pixels in the imageMgr. */
        for (let y = 0; y < this.image.height; y++) {
            for (let x = 0; x < this.image.width; x++) {
                yield new Pixel(this, x, y);
            }
        }
    }
}
/* Class Pixel */
class Pixel {
    constructor(imageMgr, x, y) {
        /* Constructor for the Pixel class.
        Takes the imageMgr and the x and y coordinates of the pixel as the arguments. */
        this.imageMgr = imageMgr;
        this.x = x;
        this.y = y;
    }
    get color() { // Not Implemented
        /* Function to get the color of the pixel.
        Returns the color of the pixel. */
        return NaN // Not Implemented
    }
    set color(value) {
        /* Function to set the color of the pixel.
        Takes the color of the pixel as an array as the argument. */
        let g = value[1];
        let b = value[2];
        let r = value[0];
        this.imageMgr.context.fillStyle = "rgba("+r+","+g+","+b+","+(255/255)+")"; // set the color for the fill
        this.imageMgr.context.fillRect( this.x, this.y, 1, 1 ); // Fills a 1x1 rectangle at the pixel location 
        
    }
    __complex__() {
        /* Function to get the complex number of the pixel.
        Returns the complex number of the pixel. */
        return (
            math.add(math.multiply(math.complex(this.x, -this.y), this.imageMgr.scale), this.imageMgr.offset)); // (x, -y) * scale + offset
        
    }
}

/* An example fo this code which creates the Mandelbrot set. */
function createSet(canvas) {
    /* Function to create the Mandelbrot set. 
    Takes the canvas element as the argument. */

    // Creates an instance of the MandelbrotSet class with max iterations of 20 and escape radius of 2.
    mandelbrot_set = new MandelbrotSet(20, 2);     

    // Creates an instance of the ImageMgr class with the canvas, the center of (-0.5, oi) and width of 3.
    imageMgr_obj = new ImageMgr(canvas, math.complex(-0.5, 0), 3);
    
    // Iterates through the imageMgr
    for (var pixel of imageMgr_obj) {
        
        // Gets the pixel as a complex number
        var c = pixel.__complex__();
        
        // Gets the stability of the number as a number between 0 and 1
        let stability = mandelbrot_set.stability(c);

        // Sets the color of the pixel to white times the stability
        pixel.color = [stability * 255, stability * 255, stability * 255];
    }
}