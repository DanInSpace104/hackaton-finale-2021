
const trash_image = document.getElementById('image1');
function processData(data) {
    console.log(data)
    // set images
    let tmpImage = new Image()
    tmpImage.src = "data:image/jpeg;base64," + data['trash_image'];
    thrashImage.image(tmpImage)
    let tmpImage2= new Image()
    tmpImage2.src = "data:image/jpeg;base64," + data['number_image'];
    numberImage.image(tmpImage2)
    // set numerical data

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
