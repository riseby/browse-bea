let xySize = 100
let maxRadius = xySize/2
let minRadius = 30
let noiseWeight = maxRadius - minRadius
let numOfCirclePoints = 64

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

let font
function preload() {
  font = loadFont('fonts/CourierPrime-Bold.ttf');
}
function setup() {
  var canvas = createCanvas(xySize, xySize)
  canvas.parent('logo')
  frameRate(40)
  textSize(55)
  textFont(font)
  textAlign(CENTER, CENTER)
  smooth()
}

function draw() {
  clear()
  noiseDetail(5,0.5)
  let fc = color(c1)
  let sc = color(c2)

  fill(fc)
  stroke(color(c3))
  strokeWeight(1)
  translate(height/2,width/2)
  n += nincrement
  var dxTot = 0.0;
  var dyTot = 0.0;
  beginShape()
    for(var i = 0;i < numOfCirclePoints;i += 1){
      var rad = i*TWO_PI/numOfCirclePoints
      var x = cos(rad)
      var y = sin(rad)
      var no = noise(x+10,y+10,n)
      var r = no*noiseWeight+minRadius
      dxTot += x*no
      dyTot += y*no
      vertex(x*r,y*r)
    }
  endShape(CLOSE)


  noStroke()
  fill(sc)
  text("B", dxTot, dyTot)
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
  } else {
    c1 = c1noB
    c2 = c2noB
    c3 = c3noB
  }
}
