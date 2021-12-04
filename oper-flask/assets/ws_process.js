
function processData(data) {
    console.log(data)
    // set images

    let tmpImage = new Image()
    tmpImage.src = "data:image/jpeg;base64," + data[0]['trash_image'];
    cart1.thrashImage.image(tmpImage)
    let tmpImage2= new Image()
    tmpImage2.src = "data:image/jpeg;base64," + data[0]['number_image'];
    cart1.numberImage.image(tmpImage2)
    cart1.cartNumber.text('Номер: ' + data[0]['cart_number'])
    cart1.cartWeight.text('Вес: ' + data[0]['cart_weight'])
    cart1.trashPercent.text('Процент брака: '+data[0]['trash_percent'])

    let tmpImage3 = new Image()
    tmpImage3.src = "data:image/jpeg;base64," + data[1]['trash_image'];
    cart2.thrashImage.image(tmpImage3)
    let tmpImage4= new Image()
    tmpImage4.src = "data:image/jpeg;base64," + data[1]['number_image'];
    cart2.numberImage.image(tmpImage4)
    cart2.cartNumber.text('Номер: ' + data[1]['cart_number'])
    cart2.cartWeight.text('Вес: ' + data[1]['cart_weight'])
    cart2.trashPercent.text('Процент брака: '+data[1]['trash_percent'])

    let tmpImage5 = new Image()
    tmpImage5.src = "data:image/jpeg;base64," + data[2]['trash_image'];
    cart3.thrashImage.image(tmpImage5)
    let tmpImage6= new Image()
    tmpImage6.src = "data:image/jpeg;base64," + data[2]['number_image'];
    cart3.numberImage.image(tmpImage6)
    cart3.cartNumber.text('Номер: ' + data[2]['cart_number'])
    cart3.cartWeight.text('Вес: ' + data[2]['cart_weight'])
    cart3.trashPercent.text('Процент брака: '+data[2]['trash_percent'])
    // set numerical data
    // cartNumber.text(data['cart_number'])
}


var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', () => {
    console.log('connected')

})
socket.on('disconnect', () => {
    console.log('disconnected')
})
socket.on('data', (data) => processData(data))

setInterval(()=>{socket.emit('get_data')}, 3000)
