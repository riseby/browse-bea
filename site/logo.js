let xySize = 100
let maxRadius = xySize/2
let minRadius = 35
let noiseWeight = maxRadius - minRadius
let n = 0.0
let nincrement = 0.01

function setup() {
  var canvas = createCanvas(xySize, xySize)
  canvas.parent('logo')
  frameRate(30)
  smooth()
}

function draw() {
  clear()
  let c = color(255, 204, 0)

  fill(c)
  stroke('black')
  strokeWeight(1.5)
  translate(height/2,width/2)
  n += nincrement
  beginShape()
    for(var i = 0;i < TWO_PI;i += 0.2){
      var x = cos(i)
      var y = sin(i)
      var r = noise(x+10,y+10,n)
      var dx = cos(i)*(r*noiseWeight+minRadius)
      var dy = sin(i)*(r*noiseWeight+minRadius)
      vertex(dx,dy)
    }
  endShape(CLOSE)
}
