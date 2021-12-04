const stage = new Konva.Stage({
    container: 'holst',
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
    draggable: true,
    stroke: 'green',
    strokeWidth: 3,
    image: new Image()
}


// add carts


var rectParams = {
    width: 160,
    height: 80,
    stroke: 'black',
    strokeWidth: 5,
    fill: 'gray'
}
class Cart {
    constructor(x, y){
        this.thrashImage = new Konva.Image({
            x: -100, y:-180,
            visible: false,
            ...cartImageParams
        })
        this.numberImage = new Konva.Image({
            x: 100, y:-180,
            visible: false,
            ...cartImageParams
        })
        this.cartNumber = new Konva.Text({
            x: 0,
            y: 85,
            text: '',
            fontSize: 20,
            fill: 'white',
            visible: false,
        })
        this.cartWeight = new Konva.Text({
            x: 0,
            y: 105,
            text: '',
            fontSize: 20,
            fill: 'white',
            visible: false,
        })
        this.trashPercent = new Konva.Text({
            x: 0,
            y: 125,
            text: '',
            fontSize: 20,
            fill: 'white',
            visible: false,
        })
        this.rect = new Konva.Rect({...rectParams})
        this.group = new Konva.Group({x: x, y: y, draggable:true})
        this.group.add(this.rect)
        this.group.add(this.thrashImage)
        this.group.add(this.numberImage)
        this.group.add(this.cartNumber)
        this.group.add(this.cartWeight)
        this.group.add(this.trashPercent)
        anim_layer.add(this.group)
        this.rect.on('click', ()=>{this.onclick()})
        this.visible = false
    }
    onclick() {
        // this.car
        console.log('click')
        if (this.visible){
            this.visible = false
            this.thrashImage.hide()
            this.numberImage.hide()
            this.cartNumber.hide()
            this.cartWeight.hide()
            this.trashPercent.hide()
        } else {
            this.visible = true
            this.thrashImage.show()
            this.numberImage.show()
            this.cartNumber.show()
            this.cartWeight.show()
            this.trashPercent.show()
        }
        return
    }
}

var cart1 = new Cart(x=100, y=center.y-70)
var cart2 = new Cart(x=300, y=center.y-70)
var cart3 = new Cart(x=500, y=center.y-70)

// var cart1 = {
//     group: new Konva.Group({...center, draggable: true}),
//     box: new Konva.Rect({...cartRectParams}),
//     text: new Konva.Text(),
// }
// cart1.group.add(cart1.box)
// cart1.group.add(cart1.text)
// anim_layer.add(cart1.group)

// cart1.box.on('click', function () {
//    console.log('click')
// });


stage.add(bg_layer)
stage.add(anim_layer)
stage.add(static_layer)
bg_layer.draw()
anim_layer.draw()
static_layer.draw()
