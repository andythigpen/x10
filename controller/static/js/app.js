
var updateUiTimer = null;
function enableUiUpdate() {
    updateUiTimer = setInterval(function() {
        $.getJSON('/lights', loadStatus);
    }, 3000);
}

function disableUiUpdate() {
    clearInterval(updateUiTimer);
    updateUiTimer = null;
}

function loadStatus(data) {
    if (data['A1'] > 0) {
        $("#light-switch").val("on").slider('refresh');
    } else {
        $("#light-switch").val("off").slider('refresh');
    }
    if (data['sensor']) {
        $("#sensor-value").html(data['sensor']);
    }
    if (data['ambient']) {
        $("#ambient-value").html(data['ambient'] ? "active" : "not active");
    }
    // $("#dimmer").val(data['A1']).slider('refresh');

    if (data['xbmc'] != null) {
        $("#xbmc-switch").val(data['xbmc'] ? "start" : "stop").
            slider('refresh');
    }
    if (updateUiTimer == null) {
        enableUiUpdate();
    }
}

// var dimmerTimer = null;
// function updateDimmer() {
//     disableUiUpdate();
//     $.post('/lights', {"action":"dimmer", "repeat":$("#dimmer").val()}, 
//         function(data) {
//             loadStatus(data);
//             dimmerTimer = null;
//     });
// }

$(document).ready(function() {
    updateUiTimer = setInterval(function() {
        $.getJSON('/lights', loadStatus);
    }, 3000);

    $("#light-switch").change(function() {
        disableUiUpdate();
        $.post('/lights', {"action": $(this).val()}, loadStatus);
    });

    $("#xbmc-switch").change(function() {
        disableUiUpdate();
        $.post('/programs', {"action": $(this).val(), "program":"xbmc"}, 
            loadStatus);
    });

    $("#scene-menu").change(function() {
        if ($(this).val() != "---") {
            disableUiUpdate();
            $.post('/lights', {"action": "scene", "arg":$(this).val()}, 
                loadStatus);
        }
    });

    // $("#dimmer").change(function() {
    //     console.log($(this).val());
    //     if (dimmerTimer != null) {
    //         clearTimeout(dimmerTimer);
    //     }
    //     dimmerTimer = setTimeout(function() { updateDimmer(); }, 1000);
    // });
});

