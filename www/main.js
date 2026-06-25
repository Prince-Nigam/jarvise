$(document).ready(function () {

    function showAssistantText(message) {
        if (!message) {
            return;
        }
        $('.siri-message').text(message);
    }

    function addChatMessage(message, side) {
        if (!message || !message.trim()) {
            return;
        }
        const chatBox = document.getElementById('chat-canvas-body');
        if (!chatBox) {
            return;
        }
        const cssClass = side === 'sender' ? 'sender_message' : 'receiver_message';
        chatBox.innerHTML += `<div class="row ${side === 'sender' ? 'justify-content-end' : 'justify-content-start'} mb-4"><div class="width-size"><div class="${cssClass}">${message}</div></div></div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function buildFallbackReply(message) {
        const text = (message || '').toLowerCase();
        if (text.includes('time')) {
            return `The current time is ${new Date().toLocaleTimeString()}`;
        }
        if (text.includes('date')) {
            return `Today is ${new Date().toLocaleDateString()}`;
        }
        if (text.includes('hello') || text.includes('hi')) {
            return 'Hello! Jarvis is ready in fallback mode.';
        }
        return `You said: ${message}. I am ready for your next command.`;
    }

    function processAssistantMessage(message) {
        const text = (message || '').trim();
        if (!text) {
            showAssistantText('Listening...');
            return;
        }

        addChatMessage(text, 'sender');
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        showAssistantText('Working on it...');

        if (typeof eel !== 'undefined') {
            try {
                eel.allCommands(text);
                return;
            } catch (err) {
                console.log('Eel command skipped:', err);
            }
        }

        setTimeout(function () {
            const reply = buildFallbackReply(text);
            addChatMessage(reply, 'receiver');
            showAssistantText(reply);
            $('#Oval').attr('hidden', false);
            $('#SiriWave').attr('hidden', true);
        }, 600);
    }

    if (typeof eel !== 'undefined') {
        try {
            eel.init();
        } catch (err) {
            console.log('Eel init skipped:', err);
        }
    }

    try {
        $('.text').textillate({
            loop: true,
            sync: true,
            in:{
                effect: "bounceIn",
            },
            out:{
                effect: "bounceOut",
            },
        });
    } catch (err) {
        console.log('Textillate init skipped:', err);
    }

    // Siri configuration
    try {
        if (typeof SiriWave !== 'undefined') {
            new SiriWave({
                container: document.getElementById("siri-container"),
                width: 800,
                height: 200,
                style: "ios9",
                amplitude: "1",
                speed: "0.30",
                autostart: true
            });
        }
    } catch (err) {
        console.log('SiriWave init skipped:', err);
    }

    try {
        $('.siri-message').textillate({
            loop: true,
            sync: true,
            in:{
                effect: "fadeInUp",
                sync: true,
            },
            out:{
                effect: "fadeOutUp",
                sync: true,
            },
        });
    } catch (err) {
        console.log('Siri message animation skipped:', err);
    }

    // Mic button click event 

    $("#MicBtn").click(function () {
        if (typeof eel !== 'undefined') {
            try {
                eel.playAssistantSound();
            } catch (err) {
                console.log('Eel sound skipped:', err);
            }
        }
        processAssistantMessage($('#chatbox').val() || 'hello');
    });

    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {   //window key + j activate jarvis
            if (typeof eel !== 'undefined') {
                try {
                    eel.playAssistantSound();
                } catch (err) {
                    console.log('Eel sound skipped:', err);
                }
            }
            processAssistantMessage('hello');
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);


    function PlayAssistant(message) {

        if (message != "") {
            processAssistantMessage(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

     function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });

    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });

    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

});