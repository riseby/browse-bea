let xySize = 100
let maxRadius = xySize/2
let minRadius = 30
let noiseWeight = maxRadius - minRadius
let n = 0.0
let nincrement = 0.01

var c1noB = 'black'
var c2noB = 'white'
var c3noB = c1noB

var c1H = '#dc3545'
var c2H = c2noB
var c3H = c1H

var c1B = [255, 193, 7]
var c2B = [33, 37, 41]
var c3B = '#dee2e6'

var c1 = c1noB
var c2 = c2noB
var c3 = c3noB

function setup() {
  var canvas = createCanvas(xySize, xySize)
  canvas.parent('logo')
  frameRate(40)
  textSize(60)
  textFont('Courier Prime')
  textAlign(CENTER, CENTER)
  smooth()
}

function draw() {
  clear()
  let fc = color(c1)
  let sc = color(c2)
  //let sc = color('white')
  //let w = color('gray')

  fill(fc)
  stroke(color(c3))
  //noStroke()
  strokeWeight(1)
  translate(height/2,width/2)
  n += nincrement
  var dxMax = 0.0;
  var dyMax = 0.0;
  var magMax = 0.0;

  beginShape()
    for(var i = 0;i < TWO_PI;i += 0.1){
      var x = cos(i)
      var y = sin(i)
      var r = noise(x+10,y+10,n)
      vertex(x*(r*noiseWeight+minRadius),y*(r*noiseWeight+minRadius))
    }

  endShape(CLOSE)
  stroke(color('red'))
  strokeWeight(3)
  var dxTot = 0.0;
  var dyTot = 0.0;
  for(var i = 0;i < 8;i += 1){
    var x = cos(i*PI/4)
    var y = sin(i*PI/4)
    var r = noise(x+10,y+10,n)
    dxTot += (x * (r*noiseWeight+minRadius))
    dyTot += (y * (r*noiseWeight+minRadius))

  }

  //point(dxTot, dyTot)
  noStroke()
  fill(sc)
  text("B", dxTot, dyTot + (textAscent()- textDescent())/4)
  //text("B", dxTot, dyTot)
}

function setBeaLogoColors(dayState) {
  if(dayState == 'b'){
    c1 = c1B
    c2 = c2B
    c3 = c3B
  } else if (dayState == 'h'){
    c1 = c1H
    c2 = c2H
    c3 = c3H
    console.log(c1H)
  } else {
    c1 = c1noB
    c2 = c2noB
    c3 = c3noB
  }
}
