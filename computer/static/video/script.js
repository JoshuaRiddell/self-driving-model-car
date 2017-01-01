document.addEventListener("DOMContentLoaded", function(event) {
    var socket = io.connect();
    var vid_context = document.getElementById('video').getContext('2d');
    var new_frame = function() {socket.emit('stream', {vid_id: VID_ID})};

    new_frame();
    socket.on('stream', function(data) {
        var img = new Image();
        img.src = data.raw;
        vid_context.drawImage(img, 0, 0);
        new_frame();
    });
});


