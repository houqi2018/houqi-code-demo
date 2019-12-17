class Boid {
    /**
     * @param {number} x    - initial X position
     * @param {number} y    - initial Y position
     * @param {number} vx   - initial X velocity
     * @param {number} vy   - initial Y velocity
     */
    constructor(x,y,vx=1,vy=0) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.alternateColor = "red";
        this.timeFrame = 0;  // Turn red for 3 seconds
    }

    draw(context) {
        context.save();
        context.translate(this.x, this.y);
        context.beginPath();
        context.moveTo(0,0);
        let mob = 7;
        if (this.vx === 0 && this.vy === -1) { 
            context.lineTo(-mob, mob);
            context.lineTo(mob, mob);
        }
        else if (this.vx === 0 && this.vy === 1) { 
            context.lineTo(-mob,-mob);
            context.lineTo(+mob, -mob);
        }
        else if (this.vx === -1 && this.vy === 0) {
            context.lineTo(mob, -mob);
            context.lineTo(mob, mob);
        }
        else if (this.vx === 1 && this.vy === 0) { 
            context.lineTo(-mob, -mob);
            context.lineTo(-mob, mob);
        }
        context.closePath();
        // Determine the color
        if (this.timeFrame > 0) {
            context.fillStyle = "#FF0000";
            this.timeFrame -= 1;
        }
        context.fill();
        context.restore();
    }

    /**
     * Perform the "steering" behavior
     * @param {Array<Boid>} flock 
     */
    steer(flock) {
        let x = this.x;
        let y = this.y;
        let distance = 0;
        let alignmentX = 0;
        let alignmentY = 0;
        flock.forEach(function(boid) {
            distance = Math.sqrt((boid.x - x) * (boid.x - x) + (boid.y - y) * (boid.y - y)) || 11;
            // Alignment: only consider near neighbors, i.e., average is weighted
            if (distance < 10) {
                let tempSum = boid.vx * boid.vx + boid.vy * boid.vy;
                alignmentX += Math.ceil( 0.1 * (10 - distance) * boid.vx / tempSum);
                alignmentY += Math.ceil( 0.1 * (10 - distance) * boid.vy / tempSum);
                
            }
        })
        // Change the velocity of boid, normalize
        let tmp1 = this.vx + Math.ceil(alignmentX / 10.0);
        let tmp2 = this.vy + Math.ceil(alignmentY / 10.0);
        let tempSum = tmp1 * tmp1 + tmp2 * tmp2;
        tmp1 /= tempSum;
        tmp2 /= tempSum;

        if (tmp1 !== 0 && tmp2 !== 0) {
            this.vx = tmp1;
            this.vy = tmp2;
        }
    }
}

window.onload = function() {
    /** @type Array<Boid> */
    let theBoids = [];
    let canvas = /** @type {HTMLCanvasElement} */ (document.getElementById("flock"));
    let context = canvas.getContext("2d");
    let speedSlider =/** @type {HTMLInputElement} */ (document.getElementById("speed"));

    function draw() {
        context.clearRect(0,0,canvas.width,canvas.height);
        theBoids.forEach(boid => boid.draw(context));
    }

    theBoids.push(new Boid(100,100));
    theBoids.push(new Boid(200,200,-1,0));
    theBoids.push(new Boid(300,300,0,-1));
    theBoids.push(new Boid(400,400,0,1));

    document.getElementById("add").onclick = function () {
        for (let i = 0; i < 10; i++) {
            let max = canvas.width;
            var random1 = Math.floor(Math.random() * Math.floor(max));
            var random2 = Math.floor(Math.random() * Math.floor(max));
            var randomIndex = Math.floor(Math.random() * Math.floor(4));
            var velocityOptions = [{'velocityX':1,"velocityY":0}, {'velocityX':-1,"velocityY":0}, {'velocityX':0,"velocityY":-1}, {'velocityX':0,"velocityY":1}];
            var velocityPair = velocityOptions[randomIndex];
            var velocityX = velocityPair.velocityX;
            var velocityY = velocityPair.velocityY;
            theBoids.push(new Boid(random1, random2, velocityX, velocityY));
        }
    };
    document.getElementById("clear").onclick = function() {
        theBoids = [];
    };

    function loop() {
        // change directions
        theBoids.forEach(boid => boid.steer(theBoids));
        // move forward
        let speed = Number(speedSlider.value);
        theBoids.forEach(function(boid) {
            boid.x += boid.vx * speed;
            boid.y += boid.vy * speed;
        });
        // make sure that we stay on the screen
        theBoids.forEach(function(boid) {
            let timeFrame = 20;
            // Revert velocity when hitting edge
            if (boid.x >= canvas.width) {
                boid.vx = - boid.vx;
                boid.timeFrame = timeFrame;
            }
            if (boid.y >= canvas.height) {
                boid.vy = - boid.vy;
                boid.timeFrame = timeFrame;
            }
            if (boid.x < 0) {
                boid.vx = - boid.vx;
                boid.timeFrame = timeFrame;
            }
            if (boid.y < 0) {
                boid.vy = - boid.vy;
                boid.timeFrame = timeFrame;
            }
        });
        draw();
        window.requestAnimationFrame(loop);
    }
    loop();
};
