let xySize = 100
let maxRadius = xySize/2
let minRadius = 35
let noiseWeight = maxRadius - minRadius
let n = 0.0
let nincrement = 0.01

var c1noB = 'black'
var c2noB = 'white'
var c1B = [255, 193, 7]
var c2B = [33, 37, 41]

var c1 = c1noB
var c2 = c2noB

function setup() {
  var canvas = createCanvas(xySize, xySize)
  canvas.parent('logo')
  frameRate(30)
  textSize(50);
  textAlign(CENTER, CENTER);
  smooth()
}

function draw() {
  clear()
  let fc = color(c1)
  let sc = color(c2)
  //let sc = color('white')
  //let w = color('gray')

  fill(fc)
  //stroke(sc)
  noStroke()
  strokeWeight(1.3)
  translate(height/2,width/2)
  n += nincrement
  beginShape()
    for(var i = 0;i < TWO_PI;i += 0.1){
      var x = cos(i)
      var y = sin(i)
      var r = noise(x+10,y+10,n)
      var dx = cos(i)*(r*noiseWeight+minRadius)
      var dy = sin(i)*(r*noiseWeight+minRadius)
      vertex(dx,dy)
    }
  endShape(CLOSE)
  noStroke()
  fill(sc)
  text("B", 0, (textAscent()- textDescent())/4)
}

function setBeaLogoColors(b) {
  if(b){
    c1 = c1B
    c2 = c2B
  } else {
    c1 = c1noB
    c2 = c2noB
  }
}
