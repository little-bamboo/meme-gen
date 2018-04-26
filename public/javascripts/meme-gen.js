function createMeme(formData) {
    // Global canvas width and height

    console.log('loading meme-gen');

    for (var p of formData) {
        console.log(p);
    }
    var gCanvasWidth = 1000;
    var gCanvasHeight = 1000;

    var memeSize = 300;
    var memeWidth = 0;
    var memeHeight = 0;

    var canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');


    // Set the text style to that to which we are accustomed
    canvas.width = gCanvasWidth;
    canvas.height = gCanvasHeight;

//  Grab the nodes

    // Build the image node, file reader, and file object used to create the meme background
    var img = new Image();
    var reader = new FileReader();
    var file = formData.get('memeFile');
    console.log(file);

    // read the data url by passing it the file object
    reader.readAsDataURL(file);

    // add event listener to load the image src once the file has been read
    reader.addEventListener("load", function () {
        img.src = reader.result;
        console.log(img);

    }, false);


    var topText = formData.get('topText');
    var bottomText = formData.get('bottomText');

// When the image has loaded...
    img.onload = function () {
        calculateCanvasSize();
        drawMeme();
    }


    function drawMeme() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.drawImage(img, 0, 0, memeWidth, memeHeight);

        ctx.lineWidth = 8;
        ctx.font = 'bold 50pt Impact';
        ctx.strokeStyle = 'black';
        ctx.mutterLine = 2;
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';

        var text1 = topText;
        //var text1 = bottomText;
        text1 = text1.toUpperCase();
        x = memeWidth / 2;
        y = 0;

        wrapText(ctx, text1, x, y, memeWidth, 1.6, false, 50);
        //writeText(text1, x, y);

        ctx.textBaseline = 'bottom';
        var text2 = bottomText;
        text2 = text2.toUpperCase();
        y = memeHeight;

        wrapText(ctx, text2, x, y, memeWidth, 1.6, true, 50);

    }

    function wrapText(context, text, x, y, maxWidth, lineHeightRatio, fromBottom, fontSize) {

        context.font = 'bold ' + fontSize + 'pt Impact';
        // If from the bottom, use unshift so the lines can be added to the top of the array.
        // Required since the lines at the bottom are laid out from bottom up.
        var pushMethod = (fromBottom) ? 'unshift' : 'push';

        _lineHeightRatio = (fromBottom) ? -lineHeightRatio : lineHeightRatio;
        var lineHeight = _lineHeightRatio * fontSize;
        console.log('lineH', lineHeight, lineHeightRatio, fontSize);
        var lines = [];
        var y = y;
        var line = '';
        var words = text.split(' ');

        for (var n = 0; n < words.length; n++) {
            var testLine = line + ' ' + words[n];
            var metrics = context.measureText(testLine);
            var testWidth = metrics.width;

            if (testWidth > maxWidth) {
                lines[pushMethod](line);
                line = words[n] + ' ';
            } else {
                line = testLine;
            }
        }
        lines[pushMethod](line);

        if (lines.length > 2) {
            console.log('Too big.', fontSize);
            wrapText(context, text, x, y, maxWidth, lineHeightRatio, fromBottom, fontSize - 10);
        }
        else {
            for (var k in lines) {
                context.strokeText(lines[k], x, y + lineHeight * k);
                context.fillText(lines[k], x, y + lineHeight * k);
            }
        }

    }

    function calculateCanvasSize() {
        console.log(img.width, img.height);
        if (img.width > img.height) {
            canvas.height = img.height / img.width * canvas.width;
            memeWidth = canvas.width;
            memeHeight = canvas.height;
            console.log(canvas.width, canvas.height);
        }
    }

    var writeText = function (text, x, y) {
        var f = 60; // Font size (in pt)
        for (; f >= 30; f -= 1) {
            ctx.font = "bold " + f + "pt Impact";
            if (ctx.measureText(text).width < memeWidth - 10) {
                ctx.fillText(text, x, y);
                ctx.strokeText(text, x, y);
                break;
            }
        }
    };
    // img.src = 'https://www.bellanaija.com/wp-content/uploads/2013/08/Seyi-Law-August-2013-BellaNaija.jpg';
}