document.addEventListener("DOMContentLoaded", function(event) {
    var socket = io.connect();
    var vid_context = [
        document.getElementById('video_0').getContext('2d'),
        document.getElementById('video_1').getContext('2d'),
    ];

    var current_vid = 0;
    socket.emit('stream', {vid_id: 0});

    socket.on('stream', function(data) {
        var img = new Image();
        img.src = data.raw;
        vid_context[current_vid].drawImage(img, 0, 0);

        if (current_vid == 0) {
            current_vid = 1;
        } else {
            current_vid = 0;
        }

        socket.emit('stream', {vid_id: current_vid});
    });

    socket.on('receiver_input', function(data) {

    });


});

