const stage = new Konva.Stage({
    container: 'container',
    width: 1500,
    height: 800,
})
let bg_layer = new Konva.Layer()

const center = {x: stage.width()/2, y: stage.height()/2}

var tmpImage = new Image();
tmpImage.src = '/assets/mnemosheme.png';
tmpImage.onload = function() {
    var bgImage = new Konva.Image({
        x: 0,
        y: 0,
        image: tmpImage,
        width: stage.width(),
        height: stage.height()
    });
    bg_layer.add(bgImage);
    bg_layer.draw()
};



let anim_layer = new Konva.Layer()
let static_layer = new Konva.Layer()

// Рамка вокруг рабочей области
let outerFrame = new Konva.Rect({
    x: 0,
    y: 0,
    width: stage.width(),
    height: stage.height(),
    stroke: 'black',
    strokeWidth: 4
})
bg_layer.add(outerFrame)


// Вагоны
// const cartRectParams = {

// }

cartImageParams = {
    width: 200,
    height: 150,
    image: new Image()
}
var thrashImage = new Konva.Image({
    x: 200,
    y: 50,
    ...cartImageParams
})
anim_layer.add(thrashImage)
var numberImage = new Konva.Image({
    x: 500,
    y: 200,
    ...cartImageParams
})
anim_layer.add(numberImage)

stage.add(bg_layer)
stage.add(anim_layer)
stage.add(static_layer)
bg_layer.draw()
anim_layer.draw()
static_layer.draw()
