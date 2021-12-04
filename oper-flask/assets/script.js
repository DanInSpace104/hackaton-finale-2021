const stage = new Konva.Stage({
    container: 'container',
    width: 1500,
    height: 800,
})

const center = {x: stage.width()/2, y: stage.height()/2}

let bg_layer = new Konva.Layer()
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

// Пути поездов
const trainLineParams = {
    stroke: 'black',
    strokeWidth: 15,
    lineJoin: 'round',
    dash: [4, 15, 4, 15],
}
let midTrainLine = new Konva.Line({
    points: [0, center.y, stage.width(), center.y],
    ...trainLineParams
  });
static_layer.add(midTrainLine)
let topTrainLine = new Konva.Line({
    points: [0, center.y, stage.width()/4, center.y-15, center.x, center.y/2, stage.width(), center.y/2-15],
    tension: 0.3,
    ...trainLineParams
})
static_layer.add(topTrainLine)
let bottomTrainLine = new Konva.Line({
    points: [0, center.y, stage.width()/4, center.y+15, center.x, center.y+center.y/2, stage.width(), center.y+center.y/2+15],
    tension: 0.3,
    ...trainLineParams
})
static_layer.add(bottomTrainLine)

// краны
const craneRectParams = {
    width: 80,
    height: 60,
    stroke: 'black',
    strokeWidth: 4,
    fill: 'gray'
}
let midCrane = new Konva.Rect({
    x: center.x,
    y: center.y - 90,
    ...craneRectParams
})
anim_layer.add(midCrane)
// let midCrane = new Konva.Rect({
//     x: center.x,
//     y: center.y - 90,
//     ...craneRectParams
// })
// anim_layer.add(midCrane)


stage.add(bg_layer)
stage.add(anim_layer)
stage.add(static_layer)
bg_layer.draw()
anim_layer.draw()
static_layer.draw()
